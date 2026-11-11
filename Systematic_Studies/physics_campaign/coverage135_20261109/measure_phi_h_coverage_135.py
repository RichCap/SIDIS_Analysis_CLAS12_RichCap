#!/usr/bin/env python3
# Measure missing phi_h coverage at the 135 degree criterion.
# Reads stored histograms. Does not refit or edit the budget.

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
SCAN_DIR = os.path.join(CAMP, "phi_h_coverage_20261109")
if(SCAN_DIR not in sys.path):
    sys.path.insert(0, SCAN_DIR)

import scan_phi_h_coverage as scan

THRESHOLD = 135.0


def parse_args():
    parser = argparse.ArgumentParser(description="Measure missing phi_h coverage at 135 degrees.")
    parser.add_argument("-j", "--jobs", default=os.path.join(CAMP, "review_comparisons_v3", "jobs.json"))
    parser.add_argument("-o", "--output", default=os.path.join(HERE, "coverage_records.json"))
    return parser.parse_args()


def missing_from_bins(widths, contents):
    missing = 0.0
    empty = 0
    nonfinite = 0
    negative = 0
    for width, content in zip(widths, contents):
        if(not math.isfinite(content)):
            nonfinite += 1
            continue
        if(content < 0.0):
            negative += 1
            continue
        if(content == 0.0):
            missing += float(width)
            empty += 1
    status = "invalid" if(nonfinite > 0) else "assessed"
    return {
        "missing_deg": missing,
        "empty_bins": empty,
        "nonfinite_bins": nonfinite,
        "negative_bins": negative,
        "status": status,
    }


def coverage_fails(record):
    if(record.get("status") != "assessed"):
        return True
    return float(record["missing_deg"]) > THRESHOLD


def expect(condition, message):
    if(not condition):
        raise SystemExit("coverage rule test failed: %s" % message)


def run_tests():
    widths_15 = [15.0] * 24
    nine = [0.0] * 9 + [1.0] * 15
    ten = [0.0] * 10 + [1.0] * 14
    nine_row = missing_from_bins(widths_15, nine)
    ten_row = missing_from_bins(widths_15, ten)
    expect(nine_row["missing_deg"] == 135.0, "nine empty 15 degree bins sum to 135")
    expect((not coverage_fails(nine_row)), "exactly 135 degrees missing passes")
    expect(ten_row["missing_deg"] == 150.0, "ten empty 15 degree bins sum to 150")
    expect(coverage_fails(ten_row), "ten empty 15 degree bins fail")

    widths_12 = [30.0] * 12
    four_row = missing_from_bins(widths_12, [0.0] * 4 + [1.0] * 8)
    five_row = missing_from_bins(widths_12, [0.0] * 5 + [1.0] * 7)
    expect(four_row["missing_deg"] == 120.0, "four empty 30 degree bins sum to 120")
    expect((not coverage_fails(four_row)), "120 degrees missing on the 12-bin axis passes")
    expect(five_row["empty_bins"] == 5, "five empty 30 degree bins")
    expect(coverage_fails(five_row), "150 degrees missing on the 12-bin axis fails")
    expect(five_row["empty_bins"] < 10, "the 12-bin failure is not an empty-bin count of ten")

    edge = missing_from_bins([20.0, 140.0, 160.0, 40.0], [0.0, 2.0, 2.0, 0.0])
    expect(edge["missing_deg"] == 60.0, "both edge gaps are summed")
    internal = missing_from_bins([90.0, 45.0, 90.0, 135.0], [3.0, 0.0, 3.0, 3.0])
    expect(internal["missing_deg"] == 45.0, "an internal gap is summed")
    mixed = missing_from_bins([100.0, 35.0, 50.0, 175.0], [0.0, 0.0, 4.0, 4.0])
    expect((mixed["missing_deg"] == 135.0) and (not coverage_fails(mixed)), "mixed widths at exactly 135 pass")

    negative = missing_from_bins([15.0, 15.0, 15.0], [-0.2, 0.0, 1.0])
    expect(negative["negative_bins"] == 1, "a negative nonzero bin is counted")
    expect(negative["missing_deg"] == 15.0, "a negative nonzero bin is not empty")
    expect(negative["empty_bins"] == 1, "only the exact zero is empty")

    invalid = missing_from_bins([180.0, 180.0], [float("nan"), 1.0])
    expect(invalid["status"] == "invalid", "a non-finite content is invalid")
    expect(coverage_fails(invalid), "an invalid histogram cannot pass")
    expect(coverage_fails({"status": "missing"}), "a missing histogram cannot pass")
    print("coverage rule tests passed")


def compact(record):
    if(record.get("status") == "missing"):
        return {"status": "missing", "q2y": record.get("q2y"), "zpt": record.get("zpt")}
    return {
        "status": record["status"],
        "q2y": record["q2y"],
        "zpt": record["zpt"],
        "missing_deg": record["missing_deg"],
        "empty_bins": record["empty_bins"],
        "nonfinite_bins": record["nonfinite_bins"],
        "negative_bins": record["negative_bins"],
        "nbins": record["nbins"],
        "axis_low": record["axis_low"],
        "axis_high": record["axis_high"],
        "name": record.get("name", ""),
    }


def main():
    args = parse_args()
    run_tests()
    jobs = scan.load_json(args.jobs)
    population = scan.retained_bins()
    if(len(population) != 452):
        raise SystemExit("retained population is %d, expected 452" % len(population))
    nominals, variations = scan.build_inputs(jobs)
    rows = []
    for item in nominals + variations:
        print("scanning %s %s" % (item["role"], item["variation_name"]))
        records = scan.scan_file(item["root"], item["kind"], item["smear"], population)
        packed = {}
        for key, record in records.items():
            packed[key] = compact(record)
        rows.append({
            "role": item["role"],
            "source_id": item["source_id"],
            "source_title": item["source_title"],
            "variation_name": item["variation_name"],
            "kind": item["kind"],
            "smear": item["smear"],
            "root": item["root"],
            "fit_json": item["fit_json"],
            "weight": item["weight"],
            "stage": item["stage"],
            "sector_id": item["sector_id"],
            "variation_index": item["variation_index"],
            "records": packed,
        })
    by_ident = {}
    for row in rows:
        by_ident[(row["root"], row["kind"], str(row["smear"]))] = row
    failures = 0
    sector_failures = 0
    sector_total = 0
    job_rows = []
    for job in jobs:
        ident = (job["variation_root"], job["variation_kind"], str(job["variation_smear"]))
        row = by_ident[ident]
        job_fail = 0
        for record in row["records"].values():
            if(coverage_fails(record)):
                job_fail += 1
        failures += job_fail
        if(job["source_id"] == "sector"):
            sector_failures += job_fail
            sector_total += len(population)
        job_rows.append({
            "source_id": job["source_id"],
            "variation_name": job["variation_name"],
            "variation_index": job["variation_index"],
            "fit_json": job["variation_json"],
            "failures": job_fail,
        })
    nominal_summary = []
    for row in rows:
        if(row["role"] != "nominal"):
            continue
        failed = [key for key, record in row["records"].items() if(coverage_fails(record))]
        nominal_summary.append({
            "label": "%s %s" % (row["weight"], row["stage"]),
            "kind": row["kind"],
            "weight": row["weight"],
            "stage": row["stage"],
            "root": row["root"],
            "fit_json": row["fit_json"],
            "failures": len(failed),
            "failed_bins": failed,
        })
    reference = {
        "variation_failures": failures,
        "variation_distributions": len(jobs) * len(population),
        "sector_failures": sector_failures,
        "sector_distributions": sector_total,
        "reference_variation_failures": 2522,
        "reference_variation_distributions": 27572,
        "reference_sector_failures": 2498,
        "reference_sector_distributions": 5424,
    }
    reference["variation_match"] = (
        (reference["variation_failures"] == 2522) and (reference["variation_distributions"] == 27572)
    )
    reference["sector_match"] = (
        (reference["sector_failures"] == 2498) and (reference["sector_distributions"] == 5424)
    )
    payload = {
        "threshold_deg": THRESHOLD,
        "pass_rule": "missing coverage <= 135 degrees; exactly 135 passes; missing or invalid cannot pass",
        "population": len(population),
        "jobs_path": os.path.abspath(args.jobs),
        "nominals": nominal_summary,
        "reference": reference,
        "job_failure_counts": job_rows,
        "inputs": rows,
    }
    with open(args.output, "w") as handle:
        json.dump(payload, handle)
        handle.write("\n")
    print("wrote %s" % args.output)
    print("variation failures %d / %d match %s" % (
        failures, len(jobs) * len(population), reference["variation_match"]))
    print("sector failures %d / %d match %s" % (
        sector_failures, sector_total, reference["sector_match"]))
    for item in nominal_summary:
        print("nominal %s failures %d" % (item["label"], item["failures"]))


if(__name__ == "__main__"):
    main()
