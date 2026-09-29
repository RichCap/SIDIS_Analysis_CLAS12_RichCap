#!/usr/bin/env python3
# Score 3D closure iteration scans from the four stored RooUnfold diagnostics.
# The RMS histogram is the residual-mean error shifted by one bin. The aligned
# series is TProfile::GetBinError of MeanResiduals at that iteration.

import argparse
import math
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

STABLE_REL = 1.0e-8
B_MAX = 0.10
COMPONENT_MAX = 0.20
# A closure metric with no improvement is recorded, but a drift smaller than this
# does not veto. The cap matches the 0.20 component tolerance. 9/26/2026
WORSEN_CAP = 0.20
RUN_LEN = 3
COST_TIE = 1.0e-9
RATIO_FLOOR = 1.0e-4
REQUIRED_SAMPLES = ("nominal", "acc", "accspline")

DIAG_COLUMNS = [
    "sample", "cut", "q2y", "k",
    "chi2", "mean_residual", "mean_abs", "rms_raw", "rms_aligned", "mean_error",
]
SCORE_COLUMNS = DIAG_COLUMNS + [
    "b_chi2", "b_mean", "b_rms",
    "status_chi2", "status_mean", "status_rms",
    "B", "C_E", "delta_B", "delta_C_E", "gain_cost_ratio",
    "pass_closure",
]
REC_COLUMNS = [
    "cut", "q2y", "status", "k_recommended", "k_supported",
    "k_lo", "k_hi", "n_supported", "C_E_joint",
    "B_nominal", "B_acc", "B_accspline",
    "b_chi2_nominal", "b_mean_nominal", "b_rms_nominal",
    "b_chi2_acc", "b_mean_acc", "b_rms_acc",
    "b_chi2_accspline", "b_mean_accspline", "b_rms_accspline",
    "C_E_nominal", "C_E_acc", "C_E_accspline",
    "n_phi", "n_kept", "kept_fraction", "n_interior_gap",
]


def parse_args():
    parser = argparse.ArgumentParser(description="score_3d_iteration_closure.py:\n\tNormalize the three closure diagnostics and pick a shared iteration.")
    parser.add_argument("-o", "--out_dir", default="Unfold_Iteration_Study_3D/Closure_Opt_3pct_4pct_5pct",
                        help="Directory with the closure ROOT files and written tables.\n")
    parser.add_argument("-d", "--diagnostics", default="",
                        help="Diagnostics TSV. Default is diagnostics_long.tsv in --out_dir.\n")
    parser.add_argument("-l", "--label", default="initial",
                        help="Score-table label. Writes scores_<label>.tsv and recommendations_<label>.tsv.\n")
    parser.add_argument("-x", "--extract_only", action="store_true",
                        help="Write the diagnostics table and stop.\n")
    parser.add_argument("-s", "--score_only", action="store_true",
                        help="Score an existing diagnostics table. Do not open ROOT files.\n")
    parser.add_argument("-c", "--coverage", default="",
                        help="phi coverage table from summarize_3d_phi_coverage.py.\n")
    parser.add_argument("-bm", "--b_max", type=float, default=B_MAX,
                        help="Combined closure score must be at or below this value.\n")
    parser.add_argument("-cm", "--component_max", type=float, default=COMPONENT_MAX,
                        help="Each active closure component must be at or below this value.\n")
    parser.add_argument("-rl", "--run_len", type=int, default=RUN_LEN,
                        help="Minimum consecutive passing iterations.\n")
    parser.add_argument("-sr", "--stable_rel", type=float, default=STABLE_REL,
                        help="Relative improvement below this is numerically negligible.\n")
    parser.add_argument("-wc", "--worsen_cap", type=float, default=WORSEN_CAP,
                        help="Relative worsening that vetoes a metric with no improvement. Use 0 for the initial veto-any-worsening rule.\n")
    parser.add_argument("-t", "--self_test", action="store_true",
                        help="Run the scorer on built-in curves and exit.\n")
    return parser.parse_args()


def fmt_num(value):
    if(value is None):
        return ""
    if(isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return ""
    if(isinstance(value, float)):
        return f"{value:.10g}"
    return str(value)


def write_tsv(path, columns, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in rows:
            handle.write("\t".join(fmt_num(row.get(column, "")) for column in columns) + "\n")


def read_tsv(path):
    rows = []
    with open(path) as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if(len(parts) != len(header)):
                continue
            row = {}
            for column, part in zip(header, parts):
                row[column] = part
            rows.append(row)
    return rows


def as_float(text):
    if(text in ("", None)):
        return None
    return float(text)


def bin_value(hist, k, want_error):
    for index in range(0, hist.GetNbinsX() + 2):
        if(abs(hist.GetBinLowEdge(index) - float(k)) > 1.0e-6):
            continue
        if(hist.InheritsFrom("TProfile")):
            try:
                if(hist.GetBinEntries(index) <= 0):
                    return None
            except Exception:
                return None
        if(want_error):
            return float(hist.GetBinError(index))
        return float(hist.GetBinContent(index))
    return None


def load_root_rows(path, sample, cut, allow_missing_chi2=False):
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    tfile = ROOT.TFile.Open(path, "READ")
    if((tfile is None) or tfile.IsZombie()):
        raise RuntimeError(f"Could not open {path}")
    rows = []
    for q2y in range(1, 18):
        tag = f"_Q2y_{q2y}_Smear"
        chi2_h = tfile.Get("Iteration_Study_Chi2" + tag)
        mean_h = tfile.Get("Iteration_Study_MeanResiduals" + tag)
        err_h = tfile.Get("Iteration_Study_RMSError" + tag)
        rms_h = tfile.Get("Iteration_Study_RMSResiduals" + tag)
        if((not chi2_h) or (not mean_h) or (not err_h) or (not rms_h)):
            raise RuntimeError(f"Missing iteration histograms for Q2y {q2y} in {path}")
        for k in range(1, 26):
            chi2 = bin_value(chi2_h, k, False)
            mean_signed = bin_value(mean_h, k, False)
            mean_error = bin_value(err_h, k, False)
            rms_raw = bin_value(rms_h, k, False)
            rms_aligned = bin_value(mean_h, k, True)
            # RooUnfold omits chi2 above 1e10, so a missing point is left out rather than invented.
            # 9/28/2026: a plot may keep the other three curves when every chi2 point was omitted.
            chi2_blocks = (chi2 is None) and (not allow_missing_chi2)
            if(chi2_blocks or (mean_signed is None) or (mean_error is None) or (rms_aligned is None)):
                if(k == 1):
                    raise RuntimeError(f"Missing k=1 for Q2y {q2y} in {path}")
                continue
            rows.append({
                "sample": sample,
                "cut": f"{cut:.3f}",
                "q2y": q2y,
                "k": k,
                "chi2": chi2,
                "mean_residual": mean_signed,
                "mean_abs": abs(mean_signed),
                "rms_raw": rms_raw,
                "rms_aligned": rms_aligned,
                "mean_error": mean_error,
            })
    tfile.Close()
    return rows


def discover_inputs(out_dir):
    found = []
    mapping = (
        ("nominal", "nom_acc"),
        ("acc", "acc_acc"),
        ("accspline", "accspline_acc"),
    )
    for sample, prefix in mapping:
        for cut, stem in ((0.03, "030"), (0.04, "040"), (0.05, "050")):
            path = os.path.join(out_dir, prefix + stem + ".root")
            if(os.path.isfile(path)):
                found.append((sample, cut, path))
    return found


def component_series(rows_for_curve, key, stable_rel, worsen_cap):
    # Return per-k status and b. A metric with no real improvement stays out of the average.
    # Its drift is still labeled. Only a drift above worsen_cap vetoes.
    by_k = {}
    for row in rows_for_curve:
        by_k[int(row["k"])] = float(row[key])
    start = by_k[1]
    best = min(by_k.values())
    scale = max(abs(start), 1.0)
    improve = start - best
    no_improvement = improve <= (stable_rel * scale)
    out = {}
    for k, value in by_k.items():
        rel_worse = (value - start) / scale
        if(no_improvement):
            if(rel_worse > worsen_cap):
                out[k] = {"status": "worsening", "b": None, "active": False}
            elif(rel_worse > stable_rel):
                out[k] = {"status": "flat_worse", "b": None, "active": False}
            else:
                out[k] = {"status": "stable", "b": None, "active": False}
        else:
            b_value = (value - best) / improve
            if((rel_worse > worsen_cap) or (b_value > 1.0 + 1.0e-8)):
                out[k] = {"status": "worsening", "b": b_value, "active": True}
            else:
                out[k] = {"status": "active", "b": b_value, "active": True}
    return out


def passes_at(b_score, parts, b_max, component_max):
    for part in parts:
        if(part["status"] == "worsening"):
            return False
    active = [part for part in parts if(part["active"])]
    if(not active):
        return True
    if(b_score > b_max):
        return False
    for part in active:
        if(part["b"] > component_max):
            return False
    return True


def converged_ks(pass_by_k, run_len):
    keys = sorted(pass_by_k)
    chosen = set()
    run = []
    for k in keys:
        if(pass_by_k[k]):
            if((not run) or (k == run[-1] + 1)):
                run.append(k)
            else:
                run = [k]
        else:
            run = []
        if(len(run) >= run_len):
            for item in run:
                chosen.add(item)
    return chosen


def score_one_curve(rows_for_curve, b_max, component_max, run_len, stable_rel, worsen_cap):
    chi = component_series(rows_for_curve, "chi2", stable_rel, worsen_cap)
    mean = component_series(rows_for_curve, "mean_abs", stable_rel, worsen_cap)
    rms = component_series(rows_for_curve, "rms_aligned", stable_rel, worsen_cap)
    errors = {int(row["k"]): float(row["mean_error"]) for row in rows_for_curve}
    error_min = min(errors.values())
    scored = []
    b_by_k = {}
    for row in sorted(rows_for_curve, key=lambda item: int(item["k"])):
        k = int(row["k"])
        parts = [chi[k], mean[k], rms[k]]
        # A defined b stays in the average, including a value above 1. Stable metrics have no b.
        active_for_mean = [part["b"] for part in parts if(part["active"] and (part["b"] is not None))]
        if(active_for_mean):
            b_score = sum(active_for_mean) / float(len(active_for_mean))
        elif(any(part["status"] == "worsening" for part in parts)):
            b_score = None
        else:
            b_score = 0.0
        b_by_k[k] = b_score
        c_cost = (errors[k] / error_min) - 1.0
        scored.append({
            "k": k,
            "b_chi2": chi[k]["b"],
            "b_mean": mean[k]["b"],
            "b_rms": rms[k]["b"],
            "status_chi2": chi[k]["status"],
            "status_mean": mean[k]["status"],
            "status_rms": rms[k]["status"],
            "B": b_score,
            "C_E": c_cost,
            "pass_closure": passes_at(0.0 if(b_score is None) else b_score, parts, b_max, component_max) and (b_score is not None or all(part["status"] == "stable" for part in parts)),
        })
    # passes_at with a missing B should fail. Recompute cleanly.
    for item in scored:
        k = item["k"]
        parts = [chi[k], mean[k], rms[k]]
        b_score = item["B"]
        if(b_score is None):
            item["pass_closure"] = False
        else:
            item["pass_closure"] = passes_at(b_score, parts, b_max, component_max)
    pass_by_k = {item["k"]: item["pass_closure"] for item in scored}
    good = converged_ks(pass_by_k, run_len)
    by_scored = {item["k"]: item for item in scored}
    for item in scored:
        k = item["k"]
        nxt = by_scored.get(k + 1)
        if((item["B"] is None) or (nxt is None) or (nxt["B"] is None)):
            item["delta_B"] = None
        else:
            item["delta_B"] = item["B"] - nxt["B"]
        if(nxt is None):
            item["delta_C_E"] = None
            item["gain_cost_ratio"] = None
        else:
            item["delta_C_E"] = nxt["C_E"] - item["C_E"]
            if((item["delta_B"] is None) or (item["delta_C_E"] is None) or (item["delta_C_E"] <= RATIO_FLOOR)):
                item["gain_cost_ratio"] = None
            else:
                item["gain_cost_ratio"] = item["delta_B"] / item["delta_C_E"]
        item["in_converged_run"] = k in good
    return scored, good


def group_rows(rows):
    grouped = {}
    for row in rows:
        key = (row["sample"], row["cut"], int(row["q2y"]))
        grouped.setdefault(key, []).append(row)
    return grouped


def numeric_rows(raw_rows):
    rows = []
    for raw in raw_rows:
        row = {
            "sample": raw["sample"],
            "cut": f"{float(raw['cut']):.3f}",
            "q2y": int(raw["q2y"]),
            "k": int(raw["k"]),
        }
        for column in ("chi2", "mean_residual", "mean_abs", "rms_raw", "rms_aligned", "mean_error"):
            row[column] = as_float(raw[column]) if(not isinstance(raw[column], float)) else raw[column]
        rows.append(row)
    return rows


def load_coverage(path):
    coverage = {}
    if(not path):
        return coverage
    with open(path) as handle:
        for line in handle:
            if(line.startswith("#") or line.startswith("cut")):
                continue
            parts = line.split()
            if(len(parts) < 9):
                continue
            cut = f"{float(parts[0]):.3f}"
            q2y = int(parts[1])
            coverage[(cut, q2y)] = {
                "n_phi": int(parts[2]),
                "n_kept": int(parts[3]),
                "kept_fraction": float(parts[8]),
                "n_interior_gap": int(parts[6]),
            }
    return coverage


def recommend(scored_by_sample, run_good, required, coverage_row):
    present = [sample for sample in required if(sample in run_good)]
    if(len(present) != len(required)):
        return {
            "status": "unresolved",
            "k_recommended": "",
            "k_supported": "",
            "k_lo": "",
            "k_hi": "",
            "n_supported": 0,
            "C_E_joint": "",
        }
    shared = None
    for sample in required:
        if(shared is None):
            shared = set(run_good[sample])
        else:
            shared = shared & run_good[sample]
    shared = sorted(shared)
    if(not shared):
        rec = {
            "status": "unresolved",
            "k_recommended": "",
            "k_supported": "",
            "k_lo": "",
            "k_hi": "",
            "n_supported": 0,
            "C_E_joint": "",
        }
    else:
        best_k = None
        best_cost = None
        for k in shared:
            costs = [scored_by_sample[sample][k]["C_E"] for sample in required]
            joint = max(costs)
            if((best_cost is None) or (joint < best_cost - COST_TIE) or ((abs(joint - best_cost) <= COST_TIE) and (k < best_k))):
                best_cost = joint
                best_k = k
        contiguous = (shared[-1] - shared[0] + 1) == len(shared)
        rec = {
            "status": "ok" if(contiguous) else "gapped",
            "k_recommended": best_k,
            "k_supported": ",".join(str(k) for k in shared),
            "k_lo": shared[0],
            "k_hi": shared[-1],
            "n_supported": len(shared),
            "C_E_joint": best_cost,
        }
    for sample in REQUIRED_SAMPLES:
        prefix = sample
        item = None
        if((rec["k_recommended"] != "") and (sample in scored_by_sample)):
            item = scored_by_sample[sample].get(rec["k_recommended"])
        rec["B_" + prefix] = "" if(item is None) else item["B"]
        rec["C_E_" + prefix] = "" if(item is None) else item["C_E"]
        rec["b_chi2_" + prefix] = "" if(item is None) else item["b_chi2"]
        rec["b_mean_" + prefix] = "" if(item is None) else item["b_mean"]
        rec["b_rms_" + prefix] = "" if(item is None) else item["b_rms"]
    if(coverage_row):
        rec.update(coverage_row)
    else:
        rec.update({"n_phi": "", "n_kept": "", "kept_fraction": "", "n_interior_gap": ""})
    return rec


def build_score_rows(diag_rows, b_max, component_max, run_len, stable_rel, coverage, worsen_cap):
    grouped = group_rows(diag_rows)
    score_rows = []
    goods = {}
    scored_maps = {}
    for key, curve in grouped.items():
        sample, cut, q2y = key
        scored, good = score_one_curve(curve, b_max, component_max, run_len, stable_rel, worsen_cap)
        by_k = {item["k"]: item for item in scored}
        scored_maps[(cut, q2y, sample)] = by_k
        goods[(cut, q2y, sample)] = good
        base = {int(row["k"]): row for row in curve}
        for item in scored:
            row = dict(base[item["k"]])
            row.update(item)
            row["pass_closure"] = 1 if(item["pass_closure"]) else 0
            row["in_converged_run"] = 1 if(item["in_converged_run"]) else 0
            score_rows.append(row)
    rec_rows = []
    cuts = sorted(set(cut for _sample, cut, _q2y in grouped))
    q2ys = sorted(set(q2y for _sample, _cut, q2y in grouped))
    for cut in cuts:
        for q2y in q2ys:
            run_good = {}
            scored_by_sample = {}
            for sample in REQUIRED_SAMPLES:
                if((cut, q2y, sample) in goods):
                    run_good[sample] = goods[(cut, q2y, sample)]
                    scored_by_sample[sample] = scored_maps[(cut, q2y, sample)]
            rec = recommend(scored_by_sample, run_good, REQUIRED_SAMPLES, coverage.get((cut, q2y)))
            rec["cut"] = cut
            rec["q2y"] = q2y
            rec_rows.append(rec)
    score_rows.sort(key=lambda row: (row["cut"], row["sample"], int(row["q2y"]), int(row["k"])))
    rec_rows.sort(key=lambda row: (row["cut"], int(row["q2y"])))
    return score_rows, rec_rows


def self_test():
    # Chi2 falls and is inside the band from k=4 onward. Mean and RMS are flat.
    # Error grows with k, so the pick is the first iteration of the shared run.
    def make_curve(sample, chi_values, error_values, mean_value=1000.0, rms_value=10.0):
        rows = []
        for k, chi2 in enumerate(chi_values, start=1):
            rows.append({
                "sample": sample,
                "cut": "0.030",
                "q2y": 1,
                "k": k,
                "chi2": chi2,
                "mean_residual": -mean_value,
                "mean_abs": mean_value,
                "rms_raw": rms_value,
                "rms_aligned": rms_value,
                "mean_error": error_values[k - 1],
            })
        return rows
    chi_fast = [100.0, 40.0, 20.0, 12.0, 10.5, 10.2, 10.1, 10.0, 10.0, 10.0]
    # b_chi2: best=10, start=100, b=(v-10)/90. k=4 -> 2/90=0.022, already <=0.10
    # Need three consecutive, so region starts at k=4.
    err = [1.0 + 0.1 * (k - 1) for k in range(1, 11)]
    rows = []
    rows.extend(make_curve("nominal", chi_fast, err))
    rows.extend(make_curve("acc", chi_fast, err))
    chi_slow = [100.0, 80.0, 60.0, 40.0, 25.0, 16.0, 12.0, 10.5, 10.1, 10.0]
    # b=(v-10)/90. k=6 -> 6/90=0.067, k=5 -> 15/90=0.167 so k=5 fails component 0.20.
    rows.extend(make_curve("accspline", chi_slow, err))
    _score_rows, rec_rows = build_score_rows(rows, B_MAX, COMPONENT_MAX, RUN_LEN, STABLE_REL, {}, WORSEN_CAP)
    rec = rec_rows[0]
    if(rec["k_recommended"] != 6):
        raise SystemExit(f"self_test expected k=6, got {rec}")
    # No shared run if one sample never enters the band.
    rows_bad = [row for row in rows if(row["sample"] != "accspline")]
    rows_bad.extend(make_curve("accspline", [100.0, 90.0, 80.0, 70.0, 60.0, 50.0, 40.0, 30.0, 25.0, 22.0], err))
    _score_rows, rec_bad = build_score_rows(rows_bad, B_MAX, COMPONENT_MAX, RUN_LEN, STABLE_REL, {}, WORSEN_CAP)
    if(rec_bad[0]["status"] != "unresolved"):
        raise SystemExit(f"self_test expected unresolved, got {rec_bad[0]}")
    # A drift above the cap vetoes. A 1% drift on a metric that never improves does not.
    rows_worse = make_curve("nominal", chi_fast, err, rms_value=10.0)
    for row in rows_worse:
        row["rms_aligned"] = 10.0 + 0.5 * (row["k"] - 1)
        row["sample"] = "nominal"
    scored, good = score_one_curve(rows_worse, B_MAX, COMPONENT_MAX, RUN_LEN, STABLE_REL, WORSEN_CAP)
    if(scored[5]["status_rms"] != "worsening"):
        raise SystemExit("self_test expected RMS worsening once the relative drift exceeds 0.20")
    if(good):
        raise SystemExit(f"self_test did not expect a converged run under a large RMS drift, got {sorted(good)}")
    rows_flat = make_curve("nominal", chi_fast, err, mean_value=1000.0)
    for row in rows_flat:
        row["mean_abs"] = 1000.0 * (1.0 + 0.01 * (row["k"] - 1) / 9.0)
    scored_flat, good_flat = score_one_curve(rows_flat, B_MAX, COMPONENT_MAX, RUN_LEN, STABLE_REL, WORSEN_CAP)
    if(4 not in good_flat):
        raise SystemExit(f"self_test expected a 1% residual drift to leave the chi2 run intact, got {sorted(good_flat)}")
    print("self_test ok")
    return 0


def main():
    args = parse_args()
    if(args.self_test):
        return self_test()
    out_dir = args.out_dir
    diag_path = args.diagnostics or os.path.join(out_dir, "diagnostics_long.tsv")
    if(not args.score_only):
        found = discover_inputs(out_dir)
        if(not found):
            print(f"No closure ROOT files in {out_dir}", file=sys.stderr)
            return 1
        diag_rows = []
        for sample, cut, path in found:
            print(f"Reading {sample} cut {cut:.3f} {path}")
            diag_rows.extend(load_root_rows(path, sample, cut))
        write_tsv(diag_path, DIAG_COLUMNS, diag_rows)
        print(f"Wrote {diag_path} ({len(diag_rows)} rows)")
        if(args.extract_only):
            return 0
    else:
        diag_rows = numeric_rows(read_tsv(diag_path))
    coverage_path = args.coverage or os.path.join(out_dir, "phi_coverage.txt")
    coverage = load_coverage(coverage_path) if(os.path.isfile(coverage_path)) else {}
    score_rows, rec_rows = build_score_rows(
        diag_rows, args.b_max, args.component_max, args.run_len, args.stable_rel, coverage, args.worsen_cap)
    score_path = os.path.join(out_dir, f"scores_{args.label}.tsv")
    rec_path = os.path.join(out_dir, f"recommendations_{args.label}.tsv")
    write_tsv(score_path, SCORE_COLUMNS + ["in_converged_run"], score_rows)
    write_tsv(rec_path, REC_COLUMNS, rec_rows)
    print(f"Wrote {score_path}")
    print(f"Wrote {rec_path}")
    n_ok = sum(1 for row in rec_rows if(row["status"] == "ok"))
    n_gap = sum(1 for row in rec_rows if(row["status"] == "gapped"))
    n_bad = sum(1 for row in rec_rows if(row["status"] == "unresolved"))
    print(f"regions ok={n_ok} gapped={n_gap} unresolved={n_bad}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
