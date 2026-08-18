#!/usr/bin/env python3
"""Summarize 5D (and optional 3D) fit JSON without opening ROOT."""
import argparse, csv, json, math, os, re
from collections import defaultdict

def stats_and_rows(fit_dict):
    rows = []
    for key, e in fit_dict.items():
        if not isinstance(e, dict):
            continue
        mm = re.match(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", key)
        if mm is None:
            continue
        A, Ae = e.get("Fit_Par_A"), e.get("Fit_Par_A_ERR")
        B, Be = e.get("Fit_Par_B"), e.get("Fit_Par_B_ERR")
        C, Ce = e.get("Fit_Par_C"), e.get("Fit_Par_C_ERR")
        chi, ndf = e.get("Chi2"), e.get("NDF")
        red = None
        if chi is not None and ndf not in (None, 0):
            try:
                red = float(chi) / float(ndf)
                if (not math.isfinite(red)) or red > 1e6:
                    red = None
            except Exception:
                red = None
        nanA = A is None or (isinstance(A, float) and not math.isfinite(A))
        empty = (A == 0 and Ae == 0)
        rows.append({
            "q2y": int(mm.group(1)), "zpt": int(mm.group(2)), "bin": key,
            "A": A, "A_err": Ae, "B": B, "B_err": Be, "C": C, "C_err": Ce,
            "chi2": chi, "ndf": ndf, "redchi2": red,
            "nanA": nanA, "empty": empty,
        })
    reds = sorted(r["redchi2"] for r in rows if r["redchi2"] is not None)
    summary = {
        "n": len(rows),
        "nanA": sum(r["nanA"] for r in rows),
        "empty": sum(r["empty"] for r in rows),
        "red_med": reds[len(reds)//2] if reds else None,
        "red_p95": reds[int(0.95*(len(reds)-1))] if reds else None,
        "n_gt3": sum(r > 3 for r in reds),
        "n_gt5": sum(r > 5 for r in reds),
    }
    return rows, summary

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", required=True)
    p.add_argument("--out-dir", default="Prepare_Next_Iteration/Fit_Refinement/catalogs")
    p.add_argument("--tag", default="current")
    args = p.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    data = json.load(open(args.json))
    all_sum = {}
    for fs, v in data.items():
        if fs == "Meta_Data_of_Last_Run" or not isinstance(v, dict) or "(Normalized)" in fs:
            continue
        rows, summary = stats_and_rows(v)
        all_sum[fs] = summary
        csv_path = os.path.join(args.out_dir, f"{args.tag}_{fs}.csv")
        if rows:
            with open(csv_path, "w", newline="") as cf:
                w = csv.DictWriter(cf, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        by = defaultdict(lambda: [0, 0])
        for r in rows:
            by[r["q2y"]][1] += 1
            if r["redchi2"] is not None and r["redchi2"] > 5:
                by[r["q2y"]][0] += 1
        print(f"{fs}: {summary}")
        if fs.startswith("Fit_Pars_from_5D") and "(Normalized)" not in fs:
            print("  red>5 by Q2-y:", " ".join(f"{q}:{by[q][0]}/{by[q][1]}" for q in range(1, 18)))
    outj = os.path.join(args.out_dir, f"{args.tag}_summary.json")
    json.dump(all_sum, open(outj, "w"), indent=2)
    print("wrote", outj)

if __name__ == "__main__":
    main()
