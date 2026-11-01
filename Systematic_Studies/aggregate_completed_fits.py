#!/usr/bin/env python3
# Aggregate completed fit JSON files. Deferred and failed studies are listed and not entered as zero.

import csv
import json
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys

OUTPUT = os.path.join(THIS_DIR, "physics_campaign")
MANIFEST = os.path.join(THIS_DIR, "sidis_physics_manifest.json")


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


def main():
    handle = open(MANIFEST)
    manifest = json.load(handle)
    handle.close()
    registry_path = os.path.join(OUTPUT, "registry", "artifacts.jsonl")
    completed = {}
    failed = []
    failed_keys = set()
    for line in open(registry_path):
        if(not line.strip()):
            continue
        record = json.loads(line)
        if(record.get("stage") != "fit"):
            continue
        key = (record.get("campaign"), record.get("source"), str(record.get("variation")))
        if(record.get("status") == "completed" and record.get("validation") == "ok"):
            completed[key] = record
            failed_keys.discard(key)
        else:
            failed.append(record)
            failed_keys.add(key)
    comparison_rows = []
    budgets = {}
    for campaign in ["unweighted", "spline"]:
        nominal_path = fit_json_for({"campaign": campaign, "source": "nominal", "variation": "nominal"})
        nominal_cells = fit_collection(nominal_path, "Bayesian", "3D")
        groups = {}
        combine = {}
        for job in phys.fit_jobs(manifest, campaign):
            if(job["kind"] != "variation"):
                continue
            key = (campaign, job["source"], str(job["variation"]))
            if(key not in completed):
                if(key not in failed_keys):
                    failed.append({"campaign": campaign, "source": job["source"], "variation": job["variation"], "status": "missing"})
                continue
            cells = fit_collection(fit_json_for(job), job["method"], job.get("dimension", "3D"))
            if(len(cells) == 0):
                failed.append({"campaign": campaign, "source": job["source"], "variation": job["variation"], "status": "empty_fit"})
                continue
            bin_rows, missing = phys.collect_bin_shifts(nominal_cells, cells)
            combine[job["source"]] = "not_combined"
            for row in manifest["variations"]:
                if(row["campaign"] == campaign and row["source"] == job["source"]):
                    combine[job["source"]] = row["combine"]
            if(job["source"] == "dimension"):
                combine[job["source"]] = "independent"
            by_bin = {}
            for item in bin_rows:
                observables = item["observables"]
                record = phys.variation_bin_record(job["source"], job["variation"], item["bin"], observables)
                by_bin.setdefault(item["bin"], []).append(record)
                q2y = item["bin"].split("Q2_y_Bin_")[1].split(")")[0]
                mismatch = (job["source"] == "dimension") and (int(q2y) in phys.ITERATION_MISMATCH_BINS)
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
        result = phys.aggregate_campaign(groups, combine, manifest["run"].get("tolerance", 1.0e-9))
        result["provisional"] = True
        result["excluded"] = [
            "acceptance_reweighting Acc absent",
            "six AccSpline-only method branches",
            "spline 5D absent" if(campaign == "spline") else "",
            "radiative systematic pending",
            "bin-centering systematic studies blocked",
            "sector fits failed and not_combined",
        ]
        budgets[campaign] = result
    columns = [
        "campaign", "source", "variation", "bin", "parameter", "nominal", "variation_value",
        "signed_difference", "absolute_difference", "stat_nominal", "weight_tag", "method",
        "dimension", "status", "iteration_mismatch",
    ]
    write_csv(os.path.join(OUTPUT, "comparisons.csv"), comparison_rows, columns)
    phys.write_json(os.path.join(OUTPUT, "budgets.json"), {"budgets": budgets, "failed": failed})
    print("comparisons", len(comparison_rows))
    print("failed_or_missing", len(failed))
    for campaign, result in budgets.items():
        totals = result["totals"]
        print(campaign, "bins", len(totals), "provisional", result["provisional"])


if(__name__ == "__main__"):
    main()
