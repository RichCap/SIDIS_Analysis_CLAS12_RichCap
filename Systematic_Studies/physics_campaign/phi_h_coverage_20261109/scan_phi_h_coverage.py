#!/usr/bin/env python3
# Missing phi_h coverage of the stored post-unfolding histograms.
# Reads histograms only. Does not refit, unfold, or edit budgets.

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
STUDIES = os.path.dirname(CAMP)
ANALYSIS = os.path.dirname(STUDIES)
if(ANALYSIS not in sys.path):
    sys.path.insert(0, ANALYSIS)

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)

from MyCommonAnalysisFunction_richcap import Get_Num_of_z_pT_Rows_and_Columns, skip_condition_z_pT_bins

THRESHOLDS = [90.0, 120.0, 135.0, 150.0, 180.0]
LETTERS = ("A", "B", "C")
LETTER_NAME = {"A": "A0", "B": "cos phi_h", "C": "cos 2phi_h"}
FIT_KEY = "Fit_Pars_from_3D_Bayesian"
KIND_TAG = {"Bayesian": "Bayesian", "Bin": "Bin", "RC": "RC_Bayesian", "BC": "BC_RC_Bayesian"}


def parse_args():
    parser = argparse.ArgumentParser(description="Scan missing phi_h coverage of stored post-unfolding histograms.")
    parser.add_argument("-j", "--jobs", default=os.path.join(CAMP, "review_comparisons_v3/jobs.json"))
    parser.add_argument("-sh", "--shares", default=os.path.join(CAMP, "budgets/rerun_refinement_20261108/per_bin_source_shares.json"))
    parser.add_argument("-x", "--exclusions", default=os.path.join(CAMP, "budgets/sector_fit_exclusions_20261106.json"))
    parser.add_argument("-o", "--output", default=os.path.join(HERE, "phi_h_coverage_report.md"))
    return parser.parse_args()


def histogram_name(kind, q2y_bin, zpt_bin, smear):
    smear_tag = "Smear" if(smear in [None, ""]) else str(smear)
    if(kind == "5D"):
        return "(MultiDim_5D_Histo)_(Bayesian)_(SMEAR=%s)_(Q2_y_Bin_%d)_(z_pT_Bin_%d)_(MultiDim_Q2_y_z_pT_phi_h)" % (smear_tag, int(q2y_bin), int(zpt_bin))
    tag = KIND_TAG[kind]
    return "(MultiDim_3D_Histo)_(%s)_(SMEAR=%s)_(Q2_y_Bin_%d)_(z_pT_Bin_%d)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (tag, smear_tag, int(q2y_bin), int(zpt_bin))


def lookup_names(kind, q2y_bin, zpt_bin, smear):
    primary = histogram_name(kind, q2y_bin, zpt_bin, smear)
    names = [primary]
    if("SMEAR=Smear" in primary):
        names.append(primary.replace("SMEAR=Smear", "SMEAR=''"))
    return names


def bin_key(q2y_bin, zpt_bin):
    return "(Q2_y_Bin_%d)-(z_pT_Bin_%d)" % (int(q2y_bin), int(zpt_bin))


def retained_bins():
    kept = []
    for q2y_bin in range(1, 18):
        rows, cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=q2y_bin)
        for zpt_bin in range(1, int(rows) * int(cols) + 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin)):
                continue
            kept.append((q2y_bin, zpt_bin))
    return kept


def usable_sector(cell):
    if(not isinstance(cell, dict)):
        return False
    ndf = cell.get("NDF")
    if((ndf is None) or (float(ndf) < 1.0)):
        return False
    for letter in LETTERS:
        value = cell.get("Fit_Par_%s" % letter)
        if((not isinstance(value, (int, float))) or (not math.isfinite(float(value)))):
            return False
    if((abs(float(cell["Fit_Par_B"])) > 10.0) or (abs(float(cell["Fit_Par_C"])) > 10.0) or (abs(float(cell["Fit_Par_A"])) < 1.0)):
        return False
    return True


def load_json(path):
    with open(path) as handle:
        return json.load(handle)


def weight_of(path):
    text = str(path)
    if("/unweighted/" in text):
        return "unweighted"
    if("/spline/" in text):
        return "spline"
    return "unspecified weight"


def stage_of(kind):
    if(kind == "Bayesian"):
        return "acceptance"
    if(kind == "RC"):
        return "radiative correction"
    if(kind == "BC"):
        return "bin centering"
    if(kind == "Bin"):
        return "bin-by-bin"
    if(kind == "5D"):
        return "5D acceptance"
    return str(kind)


def sector_id_of(path):
    name = os.path.basename(os.path.dirname(path))
    if(name.startswith("eS") or name.startswith("pipS")):
        return name
    return ""


def source_share(shares, source_id):
    block = shares.get(source_id)
    if(not isinstance(block, dict)):
        return None, ""
    best = None
    best_letter = ""
    for letter in LETTERS:
        if(letter not in block):
            continue
        value = float(block[letter])
        if((best is None) or (value > best)):
            best = value
            best_letter = letter
    return best, best_letter


def measure_histogram(hist):
    nbins = int(hist.GetNbinsX())
    missing = 0.0
    empty_count = 0
    nonfinite = 0
    negative = 0
    axis_low = float(hist.GetXaxis().GetBinLowEdge(1)) if(nbins > 0) else None
    axis_high = float(hist.GetXaxis().GetBinUpEdge(nbins)) if(nbins > 0) else None
    for ibin in range(1, nbins + 1):
        content = float(hist.GetBinContent(ibin))
        if(not math.isfinite(content)):
            nonfinite += 1
            continue
        if(content < 0.0):
            negative += 1
            continue
        if(content == 0.0):
            missing += float(hist.GetXaxis().GetBinWidth(ibin))
            empty_count += 1
    return {
        "missing_deg": missing,
        "empty_bins": empty_count,
        "nonfinite_bins": nonfinite,
        "negative_bins": negative,
        "nbins": nbins,
        "axis_low": axis_low,
        "axis_high": axis_high,
    }


def fetch_histogram(handle, kind, q2y_bin, zpt_bin, smear):
    for name in lookup_names(kind, q2y_bin, zpt_bin, smear):
        obj = handle.Get(name)
        if((obj is None) or (not obj) or (not obj.InheritsFrom("TH1"))):
            continue
        return obj, name
    return None, ""


def scan_file(root_path, kind, smear, population):
    handle = ROOT.TFile.Open(root_path, "READ")
    if((handle is None) or handle.IsZombie()):
        raise IOError("unreadable ROOT file: %s" % root_path)
    records = {}
    try:
        for q2y_bin, zpt_bin in population:
            key = bin_key(q2y_bin, zpt_bin)
            hist, used_name = fetch_histogram(handle, kind, q2y_bin, zpt_bin, smear)
            if(hist is None):
                records[key] = {"status": "missing", "q2y": q2y_bin, "zpt": zpt_bin}
                continue
            measured = measure_histogram(hist)
            measured["q2y"] = q2y_bin
            measured["zpt"] = zpt_bin
            measured["name"] = used_name
            if(measured["nonfinite_bins"] > 0):
                measured["status"] = "invalid"
            else:
                measured["status"] = "assessed"
            records[key] = measured
    finally:
        handle.Close()
    return records


def failure_keys(records, threshold):
    failed = []
    for key, record in records.items():
        if(record.get("status") != "assessed"):
            continue
        if(record["missing_deg"] > threshold):
            failed.append(key)
    failed.sort()
    return failed


def summarize_records(records, population):
    missing = []
    invalid = []
    assessed = []
    negative_histograms = 0
    odd_axis = 0
    for key in [bin_key(q2y_bin, zpt_bin) for q2y_bin, zpt_bin in population]:
        record = records[key]
        if(record["status"] == "missing"):
            missing.append(key)
        elif(record["status"] == "invalid"):
            invalid.append(key)
        else:
            assessed.append(key)
            if(record["negative_bins"] > 0):
                negative_histograms += 1
            low = record["axis_low"]
            high = record["axis_high"]
            if((low is None) or (abs(low) > 1.0e-6) or (abs(high - 360.0) > 1.0e-3)):
                odd_axis += 1
    counts = []
    for threshold in THRESHOLDS:
        counts.append(len(failure_keys(records, threshold)))
    return {
        "expected": len(population),
        "assessed": len(assessed),
        "missing": missing,
        "invalid": invalid,
        "failures": counts,
        "negative_histograms": negative_histograms,
        "odd_axis": odd_axis,
    }


def percent_text(count, denominator):
    if(denominator <= 0):
        return "%d/0" % count
    percent = 100.0 * float(count) / float(denominator)
    return "%d/%d (%.1f%%)" % (count, denominator, percent)


def input_label(item):
    if(item["role"] == "nominal"):
        return "nominal %s %s" % (item["weight"], item["stage"])
    return "%s / %s" % (item["source_id"], item["variation_name"])


def monotonic(counts):
    for index in range(len(counts) - 1):
        if(counts[index] < counts[index + 1]):
            return False
    return True


def wrap_bins(keys, records):
    if(len(keys) == 0):
        return "None."
    parts = []
    for key in keys:
        record = records.get(key, {})
        if("missing_deg" in record):
            parts.append("%s (%.1f°)" % (key, record["missing_deg"]))
        else:
            parts.append(key)
    lines = []
    for start in range(0, len(parts), 3):
        lines.append(", ".join(parts[start:start + 3]))
    return "\n".join(lines)


def build_inputs(jobs):
    nominals = []
    variations = []
    seen_nominal = []
    seen_variation = []
    for job in jobs:
        nominal_ident = (job["baseline_root"], job["baseline_kind"], str(job["baseline_smear"]))
        if(nominal_ident not in seen_nominal):
            seen_nominal.append(nominal_ident)
            nominals.append({
                "role": "nominal",
                "source_id": "nominal",
                "source_title": "Nominal",
                "variation_name": stage_of(job["baseline_kind"]),
                "kind": job["baseline_kind"],
                "smear": job["baseline_smear"],
                "root": job["baseline_root"],
                "fit_json": job["baseline_json"],
                "weight": weight_of(job["baseline_root"]),
                "stage": stage_of(job["baseline_kind"]),
                "sector_id": "",
                "variation_index": -1,
            })
    nominal_idents = set((item["root"], item["kind"], str(item["smear"])) for item in nominals)
    for job in jobs:
        ident = (job["variation_root"], job["variation_kind"], str(job["variation_smear"]))
        if(ident in seen_variation):
            continue
        seen_variation.append(ident)
        if(ident in nominal_idents):
            continue
        variations.append({
            "role": "variation",
            "source_id": job["source_id"],
            "source_title": job["source_title"],
            "variation_name": job["variation_name"],
            "kind": job["variation_kind"],
            "smear": job["variation_smear"],
            "root": job["variation_root"],
            "fit_json": job["variation_json"],
            "weight": weight_of(job["variation_root"]),
            "stage": stage_of(job["variation_kind"]),
            "sector_id": sector_id_of(job["variation_root"]),
            "variation_index": int(job["variation_index"]),
        })
    return nominals, variations


def order_variations(variations, shares):
    groups = {}
    for item in variations:
        groups.setdefault(item["source_id"], []).append(item)
    ranked = []
    for source_id, items in groups.items():
        share, letter = source_share(shares, source_id)
        items.sort(key=lambda item: item["variation_index"])
        ranked.append((share if(share is not None) else -1.0, source_id, letter, items))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked


def sector_rows(item, records, exclusions, nominal_cells):
    sector_id = item["sector_id"]
    listed = set(exclusions.get(sector_id, []))
    sector_cells = {}
    if(os.path.isfile(item["fit_json"])):
        sector_cells = load_json(item["fit_json"]).get(FIT_KEY, {})
        if(not isinstance(sector_cells, dict)):
            sector_cells = {}
    kept = []
    quality = []
    for key in nominal_cells:
        cell = sector_cells.get(key)
        if(not usable_sector(cell)):
            quality.append(key)
            continue
        if(key in listed):
            continue
        kept.append(key)
    quality_set = set(quality)
    rows = []
    for threshold in THRESHOLDS:
        manual_fail = []
        manual_pass = []
        other_fail = []
        other_pass = []
        for key, record in records.items():
            if(record.get("status") != "assessed"):
                continue
            fails = record["missing_deg"] > threshold
            if(key in listed):
                if(fails):
                    manual_fail.append(key)
                else:
                    manual_pass.append(key)
            else:
                if(fails):
                    other_fail.append(key)
                else:
                    other_pass.append(key)
        for bucket in (manual_fail, manual_pass, other_fail, other_pass):
            bucket.sort()
        kept_fail = []
        kept_assessed = []
        kept_unassessed = []
        for key in kept:
            record = records.get(key)
            if((record is None) or (record.get("status") != "assessed")):
                kept_unassessed.append(key)
                continue
            kept_assessed.append(key)
            if(record["missing_deg"] > threshold):
                kept_fail.append(key)
        rows.append({
            "threshold": threshold,
            "manual_fail": manual_fail,
            "manual_pass": manual_pass,
            "other_fail": other_fail,
            "other_pass": other_pass,
            "kept": kept,
            "kept_fail": kept_fail,
            "kept_assessed": kept_assessed,
            "kept_unassessed": kept_unassessed,
            "quality": quality_set,
        })
    outside = []
    missing_listed = []
    invalid_listed = []
    retained_keys = set(records.keys())
    for key in sorted(listed):
        if(key not in retained_keys):
            outside.append(key)
            continue
        status = records[key].get("status")
        if(status == "missing"):
            missing_listed.append(key)
        elif(status == "invalid"):
            invalid_listed.append(key)
    return {
        "sector_id": sector_id,
        "listed": sorted(listed),
        "outside": outside,
        "missing_listed": missing_listed,
        "invalid_listed": invalid_listed,
        "quality_count": len(quality),
        "kept_count": len(kept),
        "rows": rows,
    }


def mark_quality(keys, quality):
    marked = []
    for key in keys:
        if(key in quality):
            marked.append("%s [fit-quality omission]" % key)
        else:
            marked.append(key)
    return marked


def write_report(path, command, args, nominals, grouped, shares, sector_reports, population):
    lines = []
    lines.append("# φ_h missing-coverage scan")
    lines.append("")
    lines.append("This pass measures coverage only. It does not select a threshold and it does not recalculate systematic uncertainties.")
    lines.append("")
    lines.append("## Execution")
    lines.append("")
    lines.append("Command:")
    lines.append("")
    lines.append("```")
    lines.append(command)
    lines.append("```")
    lines.append("")
    lines.append("Inputs:")
    lines.append("")
    lines.append("- Comparison manifest: `%s`" % args.jobs)
    lines.append("- Contribution shares: `%s`" % args.shares)
    lines.append("- Manual sector exclusions: `%s`" % args.exclusions)
    lines.append("- Histogram files: the distinct baseline and variation ROOT paths in the manifest, under `physics_campaign/refinement_20261108/`.")
    lines.append("")
    lines.append("## Rules")
    lines.append("")
    lines.append("The reporting population is the retained kinematic bins, Q²–y bins 1–17, after `skip_condition_z_pT_bins` and before manual sector exclusions. This run has %d retained bins." % len(population))
    lines.append("")
    lines.append("An in-range φ_h bin is empty when its content is finite and exactly zero. Negative nonzero contents are not empty. Missing coverage is the sum of the widths of the empty bins on the full stored axis, excluding underflow and overflow, so an internal gap counts. A present histogram with every bin empty has 360° missing. Widths are read from the histogram, so a 12-bin distribution is scored in degrees.")
    lines.append("")
    lines.append("A histogram with any non-finite bin content is invalid. Invalid histograms are counted separately and are omitted from threshold pass/fail counts and from the sector comparison counts. A missing histogram object is counted separately and is not assigned a coverage.")
    lines.append("")
    lines.append("A histogram passes a threshold when its missing coverage is less than or equal to the threshold. The thresholds are 90°, 120°, 135°, 150°, and 180°. For 15° bins those limits are 6, 8, 9, 10, and 12 empty bins. The failure percentage denominator is the assessed count: histograms that are present and not invalid.")
    lines.append("")
    lines.append("A nominal failure is only a candidate bin dropped after unfolding. A variation failure is only a candidate unavailable comparison for that variation.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("Percentages are failures divided by that row's assessed count.")
    lines.append("")
    header = ["Input", "Stage", "Expected", "Assessed", "Missing", "Invalid"]
    for threshold in THRESHOLDS:
        header.append(">%.0f°" % threshold)
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    ordered = list(nominals)
    for share, source_id, letter, items in grouped:
        ordered.extend(items)
    for item in ordered:
        summary = item["summary"]
        cells = [
            input_label(item),
            "%s, %s" % (item["weight"], item["stage"]),
            str(summary["expected"]),
            str(summary["assessed"]),
            str(len(summary["missing"])),
            str(len(summary["invalid"])),
        ]
        for count in summary["failures"]:
            cells.append(percent_text(count, summary["assessed"]))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    negative_total = sum(item["summary"]["negative_histograms"] for item in ordered)
    odd_total = sum(item["summary"]["odd_axis"] for item in ordered)
    lines.append("Histograms with at least one negative nonzero bin: %d. Those bins were not counted as empty." % negative_total)
    lines.append("Histograms whose axis does not run from 0° to 360°: %d." % odd_total)
    lines.append("")
    lines.append("## Source order")
    lines.append("")
    lines.append("Variation sources are ordered by the largest of their A₀, cos φ_h, and cos 2φ_h table contribution shares in `table_shares_percent`. The share is not a fraction of the combined systematic row.")
    lines.append("")
    for share, source_id, letter, items in grouped:
        title = items[0]["source_title"]
        if(share is None):
            lines.append("- `%s` (%s): no table share was stored." % (source_id, title))
        else:
            lines.append("- `%s` (%s): largest share %.2f%% for %s." % (source_id, title, share, LETTER_NAME[letter]))
    lines.append("")
    lines.append("## Nominal failing bins")
    lines.append("")
    lines.append("These are candidate bins dropped after unfolding. They are not variation comparisons.")
    lines.append("")
    for item in nominals:
        lines.append("### %s" % input_label(item))
        lines.append("")
        lines.append("File: `%s`" % item["root"])
        lines.append("")
        summary = item["summary"]
        if(len(summary["missing"]) > 0):
            lines.append("Missing histograms:")
            lines.append("")
            lines.append(wrap_bins(summary["missing"], item["records"]))
            lines.append("")
        if(len(summary["invalid"]) > 0):
            lines.append("Invalid histograms:")
            lines.append("")
            lines.append(wrap_bins(summary["invalid"], item["records"]))
            lines.append("")
        for index, threshold in enumerate(THRESHOLDS):
            failed = failure_keys(item["records"], threshold)
            lines.append("Above %.0f° (%s):" % (threshold, percent_text(len(failed), summary["assessed"])))
            lines.append("")
            lines.append(wrap_bins(failed, item["records"]))
            lines.append("")
    lines.append("## Variation failing bins")
    lines.append("")
    for share, source_id, letter, items in grouped:
        if(share is None):
            lines.append("## Source `%s`" % source_id)
        else:
            lines.append("## Source `%s` — largest table share %.2f%% (%s)" % (source_id, share, LETTER_NAME[letter]))
        lines.append("")
        for item in items:
            lines.append("### %s" % input_label(item))
            lines.append("")
            lines.append("Stage: %s, %s. File: `%s`" % (item["weight"], item["stage"], item["root"]))
            lines.append("")
            summary = item["summary"]
            if(len(summary["missing"]) > 0):
                lines.append("Missing histograms:")
                lines.append("")
                lines.append(wrap_bins(summary["missing"], item["records"]))
                lines.append("")
            if(len(summary["invalid"]) > 0):
                lines.append("Invalid histograms:")
                lines.append("")
                lines.append(wrap_bins(summary["invalid"], item["records"]))
                lines.append("")
            for threshold in THRESHOLDS:
                failed = failure_keys(item["records"], threshold)
                lines.append("Above %.0f° (%s):" % (threshold, percent_text(len(failed), summary["assessed"])))
                lines.append("")
                lines.append(wrap_bins(failed, item["records"]))
                lines.append("")
    lines.append("## Sector exclusions")
    lines.append("")
    lines.append("Electron labels E1–E6 are `eS1o`–`eS6o`. Pion labels P1–P6 are `pipS1o`–`pipS6o`. The four counts use assessed histograms only. Fit-quality omissions use the stored acceptance fit: NDF below 1, a non-finite coefficient, `|B|>10`, `|C|>10`, or `|A|<1`. They are not manual exclusions. A bracketed note marks a disagreement that is also a fit-quality omission.")
    lines.append("")
    lines.append("| Sector | Threshold | Excluded and fails | Excluded and passes | Not excluded and fails | Not excluded and passes |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for report in sector_reports:
        for row in report["rows"]:
            lines.append("| %s | %.0f° | %d | %d | %d | %d |" % (
                report["sector_id"],
                row["threshold"],
                len(row["manual_fail"]),
                len(row["manual_pass"]),
                len(row["other_fail"]),
                len(row["other_pass"]),
            ))
    lines.append("")
    for report in sector_reports:
        lines.append("### %s" % report["sector_id"])
        lines.append("")
        lines.append("Manual list entries: %d. Fit-quality omissions relative to the nominal acceptance bins: %d. Comparisons the budget still keeps: %d." % (len(report["listed"]), report["quality_count"], report["kept_count"]))
        lines.append("")
        if(len(report["outside"]) > 0):
            lines.append("Manual entries outside the retained population:")
            lines.append("")
            lines.append(wrap_bins(report["outside"], {}))
            lines.append("")
        if(len(report["missing_listed"]) > 0):
            lines.append("Manual entries with no stored histogram:")
            lines.append("")
            lines.append(wrap_bins(report["missing_listed"], {}))
            lines.append("")
        if(len(report["invalid_listed"]) > 0):
            lines.append("Manual entries whose histogram is invalid and therefore not in the four counts:")
            lines.append("")
            lines.append(wrap_bins(report["invalid_listed"], {}))
            lines.append("")
        for row in report["rows"]:
            assessed_manual = len(row["manual_fail"]) + len(row["manual_pass"])
            captures = (assessed_manual > 0) and (len(row["manual_pass"]) == 0)
            lines.append("#### %.0f°" % row["threshold"])
            lines.append("")
            if(assessed_manual == 0):
                lines.append("No assessable manual exclusion at this threshold.")
            elif(captures):
                lines.append("The rule fails every assessable manual exclusion (%d)." % assessed_manual)
            else:
                lines.append("The rule does not fail every assessable manual exclusion: %d of %d pass." % (len(row["manual_pass"]), assessed_manual))
            lines.append("")
            if((len(row["kept"]) > 0) and (len(row["kept_unassessed"]) == 0) and (len(row["kept_fail"]) == len(row["kept"]))):
                lines.append("Flag: this threshold would reject every currently usable comparison for %s (%d)." % (report["sector_id"], len(row["kept"])))
                lines.append("")
            elif(len(row["kept_unassessed"]) > 0):
                lines.append("Kept comparisons not assessed, so the rule does not score them: %d of %d." % (len(row["kept_unassessed"]), len(row["kept"])))
                lines.append("")
            lines.append("Manually excluded but passes:")
            lines.append("")
            lines.append(wrap_bins(mark_quality(row["manual_pass"], row["quality"]), {}))
            lines.append("")
            lines.append("Not manually excluded but fails:")
            lines.append("")
            lines.append(wrap_bins(mark_quality(row["other_fail"], row["quality"]), {}))
            lines.append("")
    lines.append("## Monotonicity")
    lines.append("")
    failed_inputs = []
    for item in ordered:
        if(not monotonic(item["summary"]["failures"])):
            failed_inputs.append(input_label(item))
    if(len(failed_inputs) == 0):
        lines.append("For every nominal input and every variation, the failure count does not increase as the allowed missing coverage increases from 90° to 180°.")
    else:
        lines.append("Monotonicity failed for:")
        lines.append("")
        for name in failed_inputs:
            lines.append("- %s" % name)
    lines.append("")
    with open(path, "w") as handle:
        handle.write("\n".join(lines))
    return failed_inputs


def main():
    args = parse_args()
    command = " ".join([sys.executable] + sys.argv)
    population = retained_bins()
    if(len(population) != 452):
        raise SystemExit("retained bins are %d, expected 452" % len(population))
    jobs = load_json(args.jobs)
    shares_payload = load_json(args.shares)
    shares = shares_payload.get("table_shares_percent", {})
    exclusions_payload = load_json(args.exclusions)
    exclusions = exclusions_payload.get("exclusions", {})
    nominals, variations = build_inputs(jobs)
    grouped = order_variations(variations, shares)
    nominal_fit = ""
    for item in nominals:
        if((item["kind"] == "Bayesian") and (item["weight"] == "spline") and (item["stage"] == "acceptance")):
            nominal_fit = item["fit_json"]
    nominal_cells = {}
    if(nominal_fit not in ["", None]):
        nominal_cells = load_json(nominal_fit).get(FIT_KEY, {})
        if(not isinstance(nominal_cells, dict)):
            nominal_cells = {}
    scanned = nominals + variations
    for item in scanned:
        print("scan %s" % input_label(item))
        item["records"] = scan_file(item["root"], item["kind"], item["smear"], population)
        item["summary"] = summarize_records(item["records"], population)
        if(not monotonic(item["summary"]["failures"])):
            print("monotonicity failed %s %s" % (input_label(item), item["summary"]["failures"]))
    sector_items = [item for item in variations if(item["sector_id"] not in ["", None])]
    sector_items.sort(key=lambda item: item["sector_id"])
    sector_reports = []
    for item in sector_items:
        sector_reports.append(sector_rows(item, item["records"], exclusions, nominal_cells))
    failed_inputs = write_report(args.output, command, args, nominals, grouped, shares, sector_reports, population)
    print("report %s" % args.output)
    if(len(failed_inputs) > 0):
        raise SystemExit("failure counts increased as the allowed coverage increased")


if(__name__ == "__main__"):
    main()
