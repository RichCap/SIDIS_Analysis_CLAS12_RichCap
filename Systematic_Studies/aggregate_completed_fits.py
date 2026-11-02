#!/usr/bin/env python3
# Aggregate completed fit JSON files. Deferred and failed studies are listed and not entered as zero.

import csv
import json
import math
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys

OUTPUT = os.path.join(THIS_DIR, "physics_campaign")
MANIFEST = os.path.join(THIS_DIR, "sidis_physics_manifest.json")
COMPARISON_COLUMNS = [
    "campaign", "source", "variation", "bin", "parameter", "nominal", "variation_value",
    "signed_difference", "absolute_difference", "stat_nominal", "weight_tag", "method",
    "dimension", "status", "iteration_mismatch",
]
SOURCE_COLUMNS = [
    "campaign", "source", "bin", "parameter", "rms", "n_shifts", "combine",
    "in_total", "stat_nominal", "R_source", "flag",
]
TOTAL_COLUMNS = [
    "campaign", "bin", "parameter", "quadrature", "stat_nominal", "R_total", "flag",
]


def fit_collection(path, method, dimension):
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    if(dimension == "5D"):
        key = "Fit_Pars_from_5D_Bayesian"
    elif(method == "Bin"):
        key = "Fit_Pars_from_3D_Bin"
    else:
        key = "Fit_Pars_from_3D_Bayesian"
    if(key not in payload):
        raise SystemExit("Missing %s in %s" % (key, path))
    return payload[key]


def fit_json_for(job):
    return os.path.join(OUTPUT, "fits", job["campaign"], job["source"], str(job["variation"]), "fit.json")


def write_csv(path, rows, columns):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    handle = open(path, "w")
    writer = csv.DictWriter(handle, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    handle.close()


def latest_fit_records(registry_path):
    latest = {}
    if(not os.path.isfile(registry_path)):
        return latest
    for line in open(registry_path):
        if(not line.strip()):
            continue
        record = json.loads(line)
        if(record.get("stage") != "fit"):
            continue
        key = (record.get("campaign"), record.get("source"), str(record.get("variation")))
        latest[key] = record
    return latest


def record_is_usable(record):
    if(record is None):
        return False
    if(record.get("validation") != "ok"):
        return False
    return record.get("status") in ["completed", "completed_partial"]


def central_values_finite(observables):
    for parameter in phys.PARAMETERS:
        values = observables[parameter]
        for key in ("nominal", "variation"):
            number = float(values[key])
            if((number != number) or (number == float("inf")) or (number == float("-inf"))):
                return False
    return True


def combine_for_campaign(manifest, campaign):
    mapping = {}
    for row in manifest["variations"]:
        if(row["campaign"] != campaign):
            continue
        mapping[row["source"]] = row["combine"]
    dimension = manifest.get("dimension", {}).get(campaign, {})
    if(dimension.get("study_state") == "ready" and dimension.get("path_status") == "verified"):
        mapping["dimension"] = "independent"
    return mapping


def subdivision_shifts(report):
    # Per bin and parameter, exactly 15 signed observable shifts. Anything else stays out.
    block = report.get("subdivision", {}) if(isinstance(report, dict)) else {}
    shifts = block.get("observable_shifts")
    if(not isinstance(shifts, dict) or len(shifts) == 0):
        return None
    parsed = {}
    for bin_name, by_parameter in shifts.items():
        if(not isinstance(by_parameter, dict)):
            return None
        parsed[bin_name] = {}
        for parameter in phys.PARAMETERS:
            values = by_parameter.get(parameter)
            if((not isinstance(values, list)) or (len(values) != 15)):
                return None
            numbers = []
            for value in values:
                number = float(value)
                if((number != number) or (number == float("inf")) or (number == float("-inf"))):
                    return None
                numbers.append(number)
            parsed[bin_name][parameter] = numbers
    return parsed


def append_subdivision(groups, parsed):
    for bin_name, by_parameter in parsed.items():
        records = []
        for index in range(15):
            observables = {}
            for parameter in phys.PARAMETERS:
                shift = by_parameter[parameter][index]
                observables[parameter] = {"nominal": 0.0, "variation": shift, "stat_nominal": None}
            records.append(phys.variation_bin_record("bin_centering_subdivision", "shift_%02d" % (index + 1), bin_name, observables))
        groups.setdefault("bin_centering_subdivision", {}).setdefault(bin_name, []).extend(records)


def load_json(path):
    if(not os.path.isfile(path)):
        return {}
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return payload


def flag_index(diagnostics):
    totals = {}
    sources = {}
    for row in diagnostics:
        if("source" in row):
            sources[(row["source"], row["bin"], row["parameter"])] = row
        else:
            totals[(row["bin"], row["parameter"])] = row
    return totals, sources


def flag_counts(diagnostics):
    counts = {}
    for row in diagnostics:
        kind = "source" if("source" in row) else "total"
        flag = row.get("flag")
        key = "%s:%s" % (kind, flag)
        counts[key] = counts.get(key, 0) + 1
    return counts


def rms_summary(table):
    summary = {}
    for parameter in phys.PARAMETERS:
        values = []
        shift_counts = []
        for reduced in table.values():
            piece = reduced.get(parameter)
            if((piece is None) or (piece.get("up") is None)):
                continue
            values.append(float(piece["up"]))
            shift_counts.append(len(piece.get("shifts", [])))
        if(len(values) == 0):
            summary[parameter] = None
            continue
        ordered = sorted(values)
        summary[parameter] = {
            "bins": len(values),
            "median": ordered[(len(ordered) - 1) // 2],
            "minimum": ordered[0],
            "maximum": ordered[-1],
            "n_shifts_min": min(shift_counts) if(len(shift_counts) > 0) else 0,
            "n_shifts_max": max(shift_counts) if(len(shift_counts) > 0) else 0,
        }
    return summary


def totals_match_independent(result, combine):
    for bin_name, total in result["totals"].items():
        independent = {}
        for source, table in result["sources"].items():
            if(combine.get(source) != "independent"):
                continue
            reduced = table.get(bin_name)
            if(reduced is None):
                continue
            independent[source] = {name: values for name, values in reduced.items() if(name != "_method")}
        if(len(independent) == 0):
            expected = {parameter: {"up": None} for parameter in phys.PARAMETERS}
        else:
            expected = phys.combine_sources(independent, "quadrature")
        for parameter in phys.PARAMETERS:
            got = total.get(parameter, {}).get("up")
            want = expected.get(parameter, {}).get("up")
            if((got is None) and (want is None)):
                continue
            if((got is None) or (want is None)):
                return False
            if(abs(float(got) - float(want)) > 1.0e-6):
                return False
    return True


def single_variation_is_absolute(groups, result):
    checked = 0
    for source, by_bin in groups.items():
        for bin_name, records in by_bin.items():
            if(len(records) != 1):
                continue
            checked += 1
            for parameter in phys.PARAMETERS:
                shift = float(records[0]["observables"][parameter]["signed_difference"])
                got = float(result["sources"][source][bin_name][parameter]["up"])
                if(abs(abs(shift) - got) > 1.0e-8):
                    return False, checked
    return True, checked


def source_rows_for(campaign, result, combine, total_flags, source_flags):
    rows = []
    for source in sorted(result["sources"].keys()):
        in_total = combine.get(source) == "independent"
        for bin_name in sorted(result["sources"][source].keys()):
            reduced = result["sources"][source][bin_name]
            for parameter in phys.PARAMETERS:
                piece = reduced.get(parameter, {})
                flag_row = source_flags.get((source, bin_name, parameter), {})
                rms_value = piece.get("up")
                rows.append({
                    "campaign": campaign,
                    "source": source,
                    "bin": bin_name,
                    "parameter": parameter,
                    "rms": "" if(rms_value is None) else rms_value,
                    "n_shifts": len(piece.get("shifts", [])),
                    "combine": combine.get(source, ""),
                    "in_total": in_total,
                    "stat_nominal": "" if(piece.get("stat_nominal") is None) else piece.get("stat_nominal"),
                    "R_source": "" if(flag_row.get("R_source") is None) else flag_row.get("R_source"),
                    "flag": flag_row.get("flag", ""),
                })
    return rows


def total_rows_for(campaign, result, total_flags):
    rows = []
    for bin_name in sorted(result["totals"].keys()):
        for parameter in phys.PARAMETERS:
            piece = result["totals"][bin_name].get(parameter, {})
            flag_row = total_flags.get((bin_name, parameter), {})
            quadrature = piece.get("up")
            rows.append({
                "campaign": campaign,
                "bin": bin_name,
                "parameter": parameter,
                "quadrature": "" if(quadrature is None) else quadrature,
                "stat_nominal": "" if(flag_row.get("statistical") is None) else flag_row.get("statistical"),
                "R_total": "" if(flag_row.get("R_total") is None) else flag_row.get("R_total"),
                "flag": flag_row.get("flag", ""),
            })
    return rows


def format_summary_value(summary):
    if(summary is None):
        return "none"
    return "bins=%s median=%.8g min=%.8g max=%.8g n_shifts=%s-%s" % (
        summary["bins"], summary["median"], summary["minimum"], summary["maximum"],
        summary["n_shifts_min"], summary["n_shifts_max"],
    )


def main():
    manifest = load_json(MANIFEST)
    registry_path = os.path.join(OUTPUT, "registry", "artifacts.jsonl")
    latest = latest_fit_records(registry_path)
    bc_report = load_json(os.path.join(OUTPUT, "reports", "bin_centering.json"))
    parsed_subdivision = subdivision_shifts(bc_report)
    subdivision_state = bc_report.get("subdivision", {}).get("study_state", "missing")
    radiative = manifest.get("radiative", {})
    radiative_pending = (radiative.get("enabled") is True) and (radiative.get("study_state") == "pending")
    comparison_rows = []
    source_rows = []
    total_rows = []
    budgets = {}
    nominal_cells = {}
    kept_groups = {}
    kept_combine = {}
    failed = []
    for campaign in ["unweighted", "spline"]:
        nominal_path = fit_json_for({"campaign": campaign, "source": "nominal", "variation": "nominal"})
        nominal_cells[campaign] = fit_collection(nominal_path, "Bayesian", "3D")
        groups = {}
        combine = combine_for_campaign(manifest, campaign)
        for job in phys.fit_jobs(manifest, campaign):
            if(job["kind"] != "variation"):
                continue
            key = (campaign, job["source"], str(job["variation"]))
            record = latest.get(key)
            if(not record_is_usable(record)):
                failed.append({
                    "campaign": campaign,
                    "source": job["source"],
                    "variation": job["variation"],
                    "status": "missing" if(record is None) else record.get("status"),
                    "validation": None if(record is None) else record.get("validation"),
                })
                continue
            cells = fit_collection(fit_json_for(job), job["method"], job.get("dimension", "3D"))
            if(len(cells) == 0):
                failed.append({
                    "campaign": campaign,
                    "source": job["source"],
                    "variation": job["variation"],
                    "status": "empty_fit",
                    "validation": record.get("validation"),
                })
                continue
            bin_rows, missing = phys.collect_bin_shifts(nominal_cells[campaign], cells)
            for missing_bin in missing:
                comparison_rows.append({
                    "campaign": campaign,
                    "source": job["source"],
                    "variation": job["variation"],
                    "bin": missing_bin,
                    "parameter": "A,B,C",
                    "nominal": "",
                    "variation_value": "",
                    "signed_difference": "",
                    "absolute_difference": "",
                    "stat_nominal": "",
                    "weight_tag": job["weight_tag"],
                    "method": job["method"],
                    "dimension": job.get("dimension", "3D"),
                    "status": "missing",
                    "iteration_mismatch": False,
                })
            by_bin = {}
            for item in bin_rows:
                observables = item["observables"]
                q2y = item["bin"].split("Q2_y_Bin_")[1].split(")")[0]
                mismatch = (job["source"] == "dimension") and (int(q2y) in phys.ITERATION_MISMATCH_BINS)
                if(not central_values_finite(observables)):
                    for parameter in phys.PARAMETERS:
                        values = observables[parameter]
                        comparison_rows.append({
                            "campaign": campaign,
                            "source": job["source"],
                            "variation": job["variation"],
                            "bin": item["bin"],
                            "parameter": parameter,
                            "nominal": values["nominal"],
                            "variation_value": values["variation"],
                            "signed_difference": "",
                            "absolute_difference": "",
                            "stat_nominal": values.get("stat_nominal"),
                            "weight_tag": job["weight_tag"],
                            "method": job["method"],
                            "dimension": job.get("dimension", "3D"),
                            "status": "non_finite",
                            "iteration_mismatch": mismatch,
                        })
                    continue
                stored = phys.variation_bin_record(job["source"], job["variation"], item["bin"], observables)
                by_bin.setdefault(item["bin"], []).append(stored)
                for parameter in phys.PARAMETERS:
                    values = observables[parameter]
                    delta = float(values["variation"]) - float(values["nominal"])
                    comparison_rows.append({
                        "campaign": campaign,
                        "source": job["source"],
                        "variation": job["variation"],
                        "bin": item["bin"],
                        "parameter": parameter,
                        "nominal": values["nominal"],
                        "variation_value": values["variation"],
                        "signed_difference": delta,
                        "absolute_difference": abs(delta),
                        "stat_nominal": values.get("stat_nominal"),
                        "weight_tag": job["weight_tag"],
                        "method": job["method"],
                        "dimension": job.get("dimension", "3D"),
                        "status": "completed",
                        "iteration_mismatch": mismatch,
                    })
            for bin_name, group in by_bin.items():
                groups.setdefault(job["source"], {}).setdefault(bin_name, []).extend(group)
        subdivision_entered = False
        if((campaign == "unweighted") and (parsed_subdivision is not None)):
            append_subdivision(groups, parsed_subdivision)
            combine["bin_centering_subdivision"] = "independent"
            subdivision_entered = True
        result = phys.aggregate_campaign(groups, combine, manifest["run"].get("tolerance", 1.0e-9))
        if(not totals_match_independent(result, combine)):
            raise SystemExit("quadrature is not the independent-source sum for %s" % campaign)
        absolute_ok, absolute_count = single_variation_is_absolute(groups, result)
        if(not absolute_ok):
            raise SystemExit("single variation RMS is not the absolute difference for %s" % campaign)
        for source in ("electron_sector", "pion_sector", "unweighted_versus_spline"):
            if(source in result["sources"] and combine.get(source) == "independent"):
                raise SystemExit("%s entered the %s total" % (source, campaign))
        excluded = [
            "radiative systematic pending; no number; not zero",
            "bin-centering method blocked; systematic null; not in the sum",
            "bin-centering iteration blocked; not_combined; no number",
            "unweighted versus spline is not_combined and is not added to either total",
            "electron_sector and pion_sector stay not_combined; empty bins are omitted and are not zero",
            "bayesian 1D is disabled and contributes no number",
        ]
        if(campaign == "spline"):
            excluded.append("spline 5D is absent; no number; not zero")
            excluded.append("bin-centering subdivision is not copied into the Spline budget")
        elif(not subdivision_entered):
            excluded.append("bin-centering subdivision has no 15 observable shifts; not entered; not zero")
        reasons = ["radiative systematic pending"] if(radiative_pending) else []
        if(bc_report.get("method", {}).get("study_state") == "blocked"):
            reasons.append("bin-centering method blocked")
        if(bc_report.get("iteration", {}).get("study_state") == "blocked"):
            reasons.append("bin-centering iteration blocked")
        if((campaign == "spline") and (manifest.get("dimension", {}).get("spline", {}).get("study_state") == "blocked")):
            reasons.append("spline 5D blocked")
        if((campaign == "unweighted") and (not subdivision_entered)):
            reasons.append("bin-centering subdivision awaiting observable shifts")
        result["provisional"] = len(reasons) > 0
        result["provisional_reasons"] = reasons
        result["excluded"] = excluded
        result["subdivision_entered"] = subdivision_entered
        result["subdivision_shift_count"] = 0 if(parsed_subdivision is None) else 15
        result["subdivision_state"] = subdivision_state
        result["fit_errors_in_sum"] = False
        result["single_variation_bins_checked"] = absolute_count
        total_flags, source_flags = flag_index(result["diagnostics"])
        result["flag_counts"] = flag_counts(result["diagnostics"])
        result["rms_summary"] = {}
        for source in sorted(result["sources"].keys()):
            result["rms_summary"][source] = {
                "combine": combine.get(source, ""),
                "in_total": combine.get(source) == "independent",
                "parameters": rms_summary(result["sources"][source]),
            }
        result["total_summary"] = rms_summary(result["totals"])
        budgets[campaign] = result
        kept_groups[campaign] = groups
        kept_combine[campaign] = combine
        source_rows.extend(source_rows_for(campaign, result, combine, total_flags, source_flags))
        total_rows.extend(total_rows_for(campaign, result, total_flags))
    cross_rows, cross_missing = phys.collect_bin_shifts(nominal_cells["unweighted"], nominal_cells["spline"])
    cross_groups = {}
    for missing_bin in cross_missing:
        comparison_rows.append({
            "campaign": "cross",
            "source": "unweighted_versus_spline",
            "variation": "spline",
            "bin": missing_bin,
            "parameter": "A,B,C",
            "nominal": "",
            "variation_value": "",
            "signed_difference": "",
            "absolute_difference": "",
            "stat_nominal": "",
            "weight_tag": "Spline",
            "method": "Bayesian",
            "dimension": "3D",
            "status": "missing",
            "iteration_mismatch": False,
        })
    for item in cross_rows:
        observables = item["observables"]
        if(not central_values_finite(observables)):
            continue
        stored = phys.variation_bin_record("unweighted_versus_spline", "spline", item["bin"], observables)
        cross_groups.setdefault(item["bin"], []).append(stored)
        for parameter in phys.PARAMETERS:
            values = observables[parameter]
            delta = float(values["variation"]) - float(values["nominal"])
            comparison_rows.append({
                "campaign": "cross",
                "source": "unweighted_versus_spline",
                "variation": "spline",
                "bin": item["bin"],
                "parameter": parameter,
                "nominal": values["nominal"],
                "variation_value": values["variation"],
                "signed_difference": delta,
                "absolute_difference": abs(delta),
                "stat_nominal": values.get("stat_nominal"),
                "weight_tag": "Spline",
                "method": "Bayesian",
                "dimension": "3D",
                "status": "completed",
                "iteration_mismatch": False,
            })
    cross_combine = {"unweighted_versus_spline": manifest["comparisons"]["unweighted_versus_spline"]["combine"]}
    cross_result = phys.aggregate_campaign(
        {"unweighted_versus_spline": cross_groups},
        cross_combine,
        manifest["run"].get("tolerance", 1.0e-9),
    )
    if(cross_combine["unweighted_versus_spline"] != "not_combined"):
        raise SystemExit("unweighted versus spline was combined")
    for bin_name, total in cross_result["totals"].items():
        for parameter in phys.PARAMETERS:
            if(total.get(parameter, {}).get("up") is not None):
                raise SystemExit("cross campaign produced a quadrature total")
    cross_total_flags, cross_source_flags = flag_index(cross_result["diagnostics"])
    source_rows.extend(source_rows_for("cross", cross_result, cross_combine, cross_total_flags, cross_source_flags))
    for campaign in ["unweighted", "spline"]:
        if("unweighted_versus_spline" in budgets[campaign]["sources"]):
            raise SystemExit("cross source was copied into %s" % campaign)
        if("bin_centering_subdivision" in budgets[campaign]["sources"] and campaign == "spline"):
            raise SystemExit("subdivision was copied into spline")
    summary = {}
    for campaign, result in budgets.items():
        summary[campaign] = {
            "provisional": result["provisional"],
            "provisional_reasons": result["provisional_reasons"],
            "bins": len(result["totals"]),
            "sources_in_total": [source for source, row in result["rms_summary"].items() if(row["in_total"])],
            "sources_not_combined": [source for source, row in result["rms_summary"].items() if(not row["in_total"])],
            "subdivision_entered": result["subdivision_entered"],
            "flag_counts": result["flag_counts"],
            "rms_summary": result["rms_summary"],
            "total_summary": result["total_summary"],
        }
    payload = {
        "budgets": budgets,
        "failed": failed,
        "cross_campaign": {
            "name": "unweighted_versus_spline",
            "reference": "unweighted",
            "variation": "spline",
            "combine": "not_combined",
            "in_either_total": False,
            "sources": cross_result["sources"],
            "diagnostics": cross_result["diagnostics"],
            "rms_summary": rms_summary(cross_result["sources"]["unweighted_versus_spline"]),
        },
        "subdivision": {
            "campaign": "unweighted",
            "state": subdivision_state,
            "shift_count": 0 if(parsed_subdivision is None) else 15,
            "entered_unweighted_quadrature": budgets["unweighted"]["subdivision_entered"],
            "copied_into_spline": False,
            "substituted_zero": False,
        },
        "radiative": {
            "study_state": radiative.get("study_state"),
            "enabled": radiative.get("enabled"),
            "systematic": None,
            "entered_as_zero": False,
        },
        "campaigns_added": False,
        "fit_errors_in_sum": False,
        "summary": summary,
    }
    comparison_path = os.path.join(OUTPUT, "comparisons.csv")
    source_path = os.path.join(OUTPUT, "sources.csv")
    total_path = os.path.join(OUTPUT, "totals.csv")
    budget_path = os.path.join(OUTPUT, "budgets.json")
    write_csv(comparison_path, comparison_rows, COMPARISON_COLUMNS)
    write_csv(source_path, source_rows, SOURCE_COLUMNS)
    write_csv(total_path, total_rows, TOTAL_COLUMNS)
    phys.write_json(budget_path, payload)
    print("comparisons", len(comparison_rows))
    print("sources", len(source_rows))
    print("totals", len(total_rows))
    print("failed_or_missing", len(failed))
    print("campaigns_added", False)
    print("fit_errors_in_sum", False)
    print("subdivision_state", subdivision_state)
    print("subdivision_shifts", 0 if(parsed_subdivision is None) else 15)
    print("subdivision_entered_unweighted", budgets["unweighted"]["subdivision_entered"])
    print("radiative_pending", radiative_pending)
    print("paths", comparison_path)
    print("paths", source_path)
    print("paths", total_path)
    print("paths", budget_path)
    for campaign in ["unweighted", "spline"]:
        result = budgets[campaign]
        print("CAMPAIGN", campaign, "provisional", result["provisional"], "bins", len(result["totals"]))
        print("REASONS", campaign, "; ".join(result["provisional_reasons"]))
        print("IN_TOTAL", campaign, ", ".join(summary[campaign]["sources_in_total"]))
        print("NOT_COMBINED", campaign, ", ".join(summary[campaign]["sources_not_combined"]))
        print("TOTAL", campaign, "A", format_summary_value(result["total_summary"].get("A")))
        print("TOTAL", campaign, "B", format_summary_value(result["total_summary"].get("B")))
        print("TOTAL", campaign, "C", format_summary_value(result["total_summary"].get("C")))
        for source in sorted(result["rms_summary"].keys()):
            row = result["rms_summary"][source]
            role = "independent" if(row["in_total"]) else "not_combined"
            for parameter in phys.PARAMETERS:
                print("SOURCE", campaign, source, role, parameter, format_summary_value(row["parameters"].get(parameter)))
        print("FLAGS", campaign, json.dumps(result["flag_counts"], sort_keys=True))
    cross_summary = payload["cross_campaign"]["rms_summary"]
    for parameter in phys.PARAMETERS:
        print("SOURCE", "cross", "unweighted_versus_spline", "not_combined", parameter, format_summary_value(cross_summary.get(parameter)))


if(__name__ == "__main__"):
    main()
