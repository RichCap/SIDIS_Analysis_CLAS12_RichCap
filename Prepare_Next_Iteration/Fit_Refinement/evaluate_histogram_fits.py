#!/usr/bin/env python3
"""Catalog φ_h histogram-fit quality from a completed hybrid ROOT file."""

import argparse
import csv
import json
import os
import re
import sys

import ROOT
ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)


FAMILIES = [
    ("3D", "Bayesian", "MultiDim_z_pT_Bin_Y_bin_phi_t"),
    ("3D", "RC_Bayesian", "MultiDim_z_pT_Bin_Y_bin_phi_t"),
    ("3D", "BC_RC_Bayesian", "MultiDim_z_pT_Bin_Y_bin_phi_t"),
    ("5D", "Bayesian", "MultiDim_Q2_y_z_pT_phi_h"),
    ("5D", "RC_Bayesian", "MultiDim_Q2_y_z_pT_phi_h"),
    ("5D", "BC_RC_Bayesian", "MultiDim_Q2_y_z_pT_phi_h"),
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--json", default=None)
    p.add_argument("--out-dir", default="Prepare_Next_Iteration/Fit_Refinement/catalogs")
    p.add_argument("--plots-dir", default=None)
    p.add_argument("--max-plots", type=int, default=0, help="0 = plot every non-empty bin")
    return p.parse_args()


def chi_from_file(tfile, method, q2y, zpt, var):
    name = f"TVectorD_(Chi_Squared)_({method})_(SMEAR=Smear)_(Q2_y_Bin_{q2y})_(z_pT_Bin_{zpt})_({var})"
    obj = tfile.Get(name)
    if(not obj):
        obj = tfile.Get(f"(Chi_Squared)_({method})_(SMEAR=Smear)_(Q2_y_Bin_{q2y})_(z_pT_Bin_{zpt})_({var})")
    if(not obj):
        return None, None
    try:
        return float(obj[0]), float(obj[1])
    except Exception:
        return None, None


def par_from_file(tfile, par, method, q2y, zpt, var):
    name = f"TVectorD_(Fit_Par_{par})_({method})_(SMEAR=Smear)_(Q2_y_Bin_{q2y})_(z_pT_Bin_{zpt})_({var})"
    obj = tfile.Get(name)
    if(not obj):
        obj = tfile.Get(f"(Fit_Par_{par})_({method})_(SMEAR=Smear)_(Q2_y_Bin_{q2y})_(z_pT_Bin_{zpt})_({var})")
    if(not obj):
        return None, None
    try:
        return float(obj[0]), float(obj[1])
    except Exception:
        return None, None


def residual_stats(hist, func):
    if((hist is None) or (func is None) or (not hasattr(func, "Eval"))):
        return None, None, 0
    pulls = []
    n_used = 0
    x_lo, x_hi = func.GetXmin(), func.GetXmax()
    for ibin in range(1, hist.GetNbinsX() + 1):
        x = hist.GetXaxis().GetBinCenter(ibin)
        if((x < x_lo) or (x > x_hi)):
            continue
        y = hist.GetBinContent(ibin)
        e = hist.GetBinError(ibin)
        if(e <= 0):
            continue
        n_used += 1
        pulls.append((y - func.Eval(x)) / e)
    if(not pulls):
        return None, None, n_used
    abs_pulls = [abs(p) for p in pulls]
    return max(abs_pulls), (sum(abs_pulls) / len(abs_pulls)), n_used


def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    json_obj = {}
    if((args.json is not None) and os.path.isfile(args.json)):
        with open(args.json, "r") as jf:
            json_obj = json.load(jf)
    tfile = ROOT.TFile.Open(args.root, "READ")
    if((not tfile) or tfile.IsZombie()):
        print(f"ERROR: cannot open {args.root}", file=sys.stderr)
        sys.exit(1)
    keys = [k.GetName() for k in tfile.GetListOfKeys()]
    summaries = {}
    for dim, method, var in FAMILIES:
        rows = []
        prefix = f"(MultiDim_{dim}_Histo)_({method})_(SMEAR=Smear)_"
        histo_names = [n for n in keys if(n.startswith(prefix) and f"_({var})" in n and "z_pT_Bin_All" not in n and "Q2_y_Bin_All" not in n)]
        plot_count = 0
        for hname in sorted(histo_names):
            mm = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", hname)
            if(mm is None):
                continue
            q2y, zpt = mm.group(1), mm.group(2)
            hist = tfile.Get(hname)
            func = tfile.Get(hname.replace(f"(MultiDim_{dim}_Histo)", "(Fit_Function)"))
            chi2, ndf = chi_from_file(tfile, method, q2y, zpt, var)
            A, Ae = par_from_file(tfile, "A", method, q2y, zpt, var)
            B, Be = par_from_file(tfile, "B", method, q2y, zpt, var)
            C, Ce = par_from_file(tfile, "C", method, q2y, zpt, var)
            fit_set = f"Fit_Pars_from_{dim}_{method}"
            if((A is None) and (fit_set in json_obj)):
                entry = json_obj[fit_set].get(f"(Q2_y_Bin_{q2y})-(z_pT_Bin_{zpt})", {})
                A, Ae = entry.get("Fit_Par_A"), entry.get("Fit_Par_A_ERR")
                B, Be = entry.get("Fit_Par_B"), entry.get("Fit_Par_B_ERR")
                C, Ce = entry.get("Fit_Par_C"), entry.get("Fit_Par_C_ERR")
                chi2 = entry.get("Chi2", chi2)
                ndf = entry.get("NDF", ndf)
            red = None
            if((chi2 is not None) and (ndf not in [None, 0])):
                red = float(chi2) / float(ndf)
            max_pull, mean_abs_pull, n_used = residual_stats(hist, func)
            empty = (A in [None, 0, 0.0]) and (Ae in [None, 0, 0.0])
            zero_err = (not empty) and (Be in [0, 0.0]) and (Ce in [0, 0.0])
            rows.append({
                "q2y": int(q2y),
                "zpt": int(zpt),
                "A": A, "A_err": Ae, "B": B, "B_err": Be, "C": C, "C_err": Ce,
                "chi2": chi2, "ndf": ndf, "redchi2": red,
                "max_abs_pull": max_pull, "mean_abs_pull": mean_abs_pull,
                "n_resid": n_used, "empty": empty, "zero_err": zero_err,
                "histo": hname,
            })
            if((args.plots_dir is not None) and (hist is not None) and (not empty)):
                if((args.max_plots <= 0) or (plot_count < args.max_plots)):
                    os.makedirs(os.path.join(args.plots_dir, f"{dim}_{method}"), exist_ok=True)
                    cnv = ROOT.TCanvas("c", "c", 800, 600)
                    hist.Draw("E1")
                    if(func):
                        func.Draw("same")
                    out_png = os.path.join(args.plots_dir, f"{dim}_{method}", f"Q2y{q2y}_zpt{zpt}.png")
                    cnv.SaveAs(out_png)
                    plot_count += 1
        reds = [r["redchi2"] for r in rows if(r["redchi2"] is not None)]
        reds.sort()
        p95 = reds[int(0.95 * (len(reds) - 1))] if(reds) else None
        summaries[f"{dim}_{method}"] = {
            "n_bins": len(rows),
            "n_empty": sum(1 for r in rows if(r["empty"])),
            "n_zero_err": sum(1 for r in rows if(r["zero_err"])),
            "n_missing_fit": sum(1 for r in rows if(r["chi2"] is None)),
            "redchi2_median": reds[len(reds)//2] if(reds) else None,
            "redchi2_p95": p95,
            "n_redchi2_gt3": sum(1 for r in rows if((r["redchi2"] is not None) and (r["redchi2"] > 3))),
        }
        csv_path = os.path.join(args.out_dir, f"{dim}_{method}.csv")
        if(rows):
            with open(csv_path, "w", newline="") as cf:
                writer = csv.DictWriter(cf, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        print(f"{dim}_{method}: {summaries[f'{dim}_{method}']}")
    out_json = os.path.join(args.out_dir, "histogram_fit_summary.json")
    with open(out_json, "w") as jf:
        json.dump(summaries, jf, indent=2)
    tfile.Close()
    print(f"Wrote {out_json}")


if(__name__ == "__main__"):
    main()
