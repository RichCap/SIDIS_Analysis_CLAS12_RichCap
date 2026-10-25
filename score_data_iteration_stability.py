#!/usr/bin/env python3
# Data-first iteration stability from the four RooUnfold diagnostics.
# Chi-squared, mean residual, and residual-mean error are stability curves only.
# Mean bin error is the cost. None of them is a truth-closure score.

import argparse
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

import score_3d_iteration_closure as closure

STEP_MAX = 0.03
RUN_LEN = 3
STABLE_REL = 1.0e-4

SCORE_COLUMNS = [
    "cut", "q2y", "k",
    "chi2", "mean_residual", "mean_abs", "rms_aligned", "mean_error",
    "d_chi2", "d_mean", "d_rms",
    "status_chi2", "status_mean", "status_rms",
    "step_stable", "in_supported_run",
    "C_E",
]
REC_COLUMNS = [
    "cut", "q2y", "status", "k_selected", "k_supported", "k_lo", "k_hi", "n_supported",
    "C_E", "mean_error",
    "n_phi", "n_kept", "kept_fraction", "n_interior_gap",
]


def parse_args():
    parser = argparse.ArgumentParser(description="score_data_iteration_stability.py:\n\tSelect a data-supported iteration from diagnostic stabilization.")
    parser.add_argument("-o", "--out_dir", default="Unfold_Iteration_Study_3D/DataFirst_4Way_Closure_3pct_4pct_5pct",
                        help="Directory for the written tables.\n")
    parser.add_argument("-l", "--label", default="initial",
                        help="Table label. Writes scores_data_<label>.tsv and recommendations_data_<label>.tsv.\n")
    parser.add_argument("-e", "--extra_root", action="append", default=[],
                        help="Additional data file as cut:path, for example 0.03:other/data_acc030.root.\n")
    parser.add_argument("-c", "--coverage", default="",
                        help="Phi coverage table. Default is phi_coverage.txt in --out_dir.\n")
    parser.add_argument("-sm", "--step_max", type=float, default=STEP_MAX,
                        help="A step is stable when the normalized change is at or below this value.\n")
    parser.add_argument("-rl", "--run_len", type=int, default=RUN_LEN,
                        help="Minimum number of consecutive stable steps.\n")
    parser.add_argument("-sr", "--stable_rel", type=float, default=STABLE_REL,
                        help="A curve whose full range is below this fraction of |M(k=1)| is already stable.\n")
    parser.add_argument("-t", "--self_test", action="store_true",
                        help="Run the selector on a built-in curve and exit.\n")
    return parser.parse_args()


def discover(out_dir, extras):
    found = []
    for cut, stem in ((0.04, "040"), (0.05, "050")):
        path = os.path.join(out_dir, "data_acc" + stem + ".root")
        if(os.path.isfile(path)):
            found.append((cut, path))
    for item in extras:
        cut_text, path = item.split(":", 1)
        found.append((float(cut_text), path))
    return found


def metric_status(by_k, stable_rel):
    start = by_k[min(by_k)]
    span = max(by_k.values()) - min(by_k.values())
    scale = max(abs(start), 1.0)
    if(span <= stable_rel * scale):
        return {k: {"d": 0.0, "status": "stable"} for k in by_k}
    out = {}
    keys = sorted(by_k)
    for k in keys:
        if((k + 1) not in by_k):
            out[k] = {"d": None, "status": "edge"}
            continue
        step = abs(by_k[k + 1] - by_k[k]) / span
        out[k] = {"d": step, "status": "active"}
    return out


def supported_from_steps(step_ok, run_len):
    # step_ok[k] means the step from k to k+1 is stable.
    # A run of run_len steps covers the iterations from the first step through one past the last.
    keys = sorted(step_ok)
    chosen = set()
    run = []
    for k in keys:
        if(step_ok[k]):
            if((not run) or (k == run[-1] + 1)):
                run.append(k)
            else:
                run = [k]
        else:
            run = []
        if(len(run) >= run_len):
            for item in run:
                chosen.add(item)
            chosen.add(run[-1] + 1)
    return chosen


def score_curve(rows, step_max, run_len, stable_rel):
    by = {int(row["k"]): row for row in rows}
    chi = {k: row["chi2"] for k, row in by.items()}
    mean = {k: row["mean_abs"] for k, row in by.items()}
    rms = {k: row["rms_aligned"] for k, row in by.items()}
    err = {k: row["mean_error"] for k, row in by.items()}
    st_chi = metric_status(chi, stable_rel)
    st_mean = metric_status(mean, stable_rel)
    st_rms = metric_status(rms, stable_rel)
    err_min = min(err.values())
    step_ok = {}
    for k in sorted(by):
        pieces = [st_chi[k], st_mean[k], st_rms[k]]
        if(any(piece["status"] == "edge" for piece in pieces)):
            continue
        ok = True
        for piece in pieces:
            if(piece["status"] == "stable"):
                continue
            if(piece["d"] > step_max):
                ok = False
        step_ok[k] = ok
    good = supported_from_steps(step_ok, run_len)
    scored = []
    for k in sorted(by):
        row = dict(by[k])
        row["d_chi2"] = st_chi[k]["d"]
        row["d_mean"] = st_mean[k]["d"]
        row["d_rms"] = st_rms[k]["d"]
        row["status_chi2"] = st_chi[k]["status"]
        row["status_mean"] = st_mean[k]["status"]
        row["status_rms"] = st_rms[k]["status"]
        row["step_stable"] = 1 if(step_ok.get(k, False)) else 0
        row["in_supported_run"] = 1 if(k in good) else 0
        row["C_E"] = (err[k] / err_min) - 1.0
        scored.append(row)
    return scored, good


def recommend(scored, good, coverage_row):
    if(not good):
        rec = {
            "status": "unresolved",
            "k_selected": "",
            "k_supported": "",
            "k_lo": "",
            "k_hi": "",
            "n_supported": 0,
            "C_E": "",
            "mean_error": "",
        }
    else:
        ordered = sorted(good)
        # Smallest k. Error normally grows with k, so this is also the lowest cost.
        pick = ordered[0]
        by = {row["k"]: row for row in scored}
        contiguous = (ordered[-1] - ordered[0] + 1) == len(ordered)
        rec = {
            "status": "ok" if(contiguous) else "gapped",
            "k_selected": pick,
            "k_supported": ",".join(str(k) for k in ordered),
            "k_lo": ordered[0],
            "k_hi": ordered[-1],
            "n_supported": len(ordered),
            "C_E": by[pick]["C_E"],
            "mean_error": by[pick]["mean_error"],
        }
    if(coverage_row):
        rec.update(coverage_row)
    else:
        rec.update({"n_phi": "", "n_kept": "", "kept_fraction": "", "n_interior_gap": ""})
    return rec


def build(diag_rows, step_max, run_len, stable_rel, coverage):
    grouped = {}
    for row in diag_rows:
        grouped.setdefault((row["cut"], int(row["q2y"])), []).append(row)
    score_rows = []
    rec_rows = []
    for key in sorted(grouped):
        cut, q2y = key
        scored, good = score_curve(grouped[key], step_max, run_len, stable_rel)
        score_rows.extend(scored)
        rec = recommend(scored, good, coverage.get((cut, q2y)))
        rec["cut"] = cut
        rec["q2y"] = q2y
        rec_rows.append(rec)
    return score_rows, rec_rows


def self_test():
    # Drops hard for three steps, then the remaining steps are 1% of the full span.
    rows = []
    values = [100.0, 70.0, 40.0, 20.0, 19.0, 18.2, 17.6, 17.1, 16.7, 16.4]
    for k, chi2 in enumerate(values, start=1):
        rows.append({
            "cut": "0.030",
            "q2y": 1,
            "k": k,
            "chi2": chi2,
            "mean_residual": -1000.0,
            "mean_abs": 1000.0,
            "rms_aligned": 10.0,
            "mean_error": 1.0 + 0.1 * (k - 1),
        })
    _scores, recs = build(rows, STEP_MAX, RUN_LEN, STABLE_REL, {})
    # Full span is 83.6. Steps after k=4 are under 0.03 of that span.
    # Three consecutive small steps begin at k=4 (19-18.2, 18.2-17.6, 17.6-17.1).
    if(recs[0]["k_selected"] != 4):
        raise SystemExit(f"self_test expected k=4, got {recs[0]}")
    print("self_test ok")
    return 0


def main():
    args = parse_args()
    if(args.self_test):
        return self_test()
    found = discover(args.out_dir, args.extra_root)
    if(not found):
        print("No data iteration files found", file=sys.stderr)
        return 1
    diag_rows = []
    for cut, path in found:
        print(f"Reading cut {cut:.3f} {path}")
        try:
            rows = closure.load_root_rows(path, "data", cut)
        except RuntimeError as err:
            print(f"Skipping incomplete file: {err}")
            continue
        for row in rows:
            row["cut"] = f"{cut:.3f}"
        diag_rows.extend(rows)
    if(not diag_rows):
        print("No complete data iteration files yet", file=sys.stderr)
        return 1
    diag_path = os.path.join(args.out_dir, "data_diagnostics_long.tsv")
    closure.write_tsv(diag_path, closure.DIAG_COLUMNS, diag_rows)
    coverage_path = args.coverage or os.path.join(args.out_dir, "phi_coverage.txt")
    coverage = closure.load_coverage(coverage_path) if(os.path.isfile(coverage_path)) else {}
    score_rows, rec_rows = build(diag_rows, args.step_max, args.run_len, args.stable_rel, coverage)
    score_path = os.path.join(args.out_dir, f"scores_data_{args.label}.tsv")
    rec_path = os.path.join(args.out_dir, f"recommendations_data_{args.label}.tsv")
    closure.write_tsv(score_path, SCORE_COLUMNS, score_rows)
    closure.write_tsv(rec_path, REC_COLUMNS, rec_rows)
    n_ok = sum(1 for row in rec_rows if(row["status"] == "ok"))
    n_bad = sum(1 for row in rec_rows if(row["status"] != "ok"))
    print(f"Wrote {score_path}")
    print(f"Wrote {rec_path}")
    print(f"regions ok={n_ok} other={n_bad}")
    for row in rec_rows:
        print(f"  {row['cut']} q{row['q2y']} {row['status']} k={row['k_selected']} {row['k_lo']}-{row['k_hi']}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
