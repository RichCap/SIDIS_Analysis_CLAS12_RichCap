#!/usr/bin/env python3
"""Safe one-canvas-per-file 5D φ_h overlays. Does not reuse TCanvas names."""
import argparse, os, re, sys
import ROOT
ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--method", default="Bayesian", choices=["Bayesian", "RC_Bayesian", "BC_RC_Bayesian"])
    p.add_argument("--q2y", type=int, default=0, help="0 = all Q2-y")
    p.add_argument("--max-plots", type=int, default=0)
    args = p.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    tfile = ROOT.TFile.Open(args.root, "READ")
    if (not tfile) or tfile.IsZombie():
        print("ERROR opening", args.root, file=sys.stderr)
        sys.exit(1)
    var = "MultiDim_Q2_y_z_pT_phi_h"
    prefix = f"(MultiDim_5D_Histo)_({args.method})_(SMEAR=Smear)_"
    names = []
    for key in tfile.GetListOfKeys():
        n = key.GetName()
        if not n.startswith(prefix):
            continue
        if f"_({var})" not in n:
            continue
        if "z_pT_Bin_All" in n or "Q2_y_Bin_All" in n:
            continue
        if "_(Normalized)" in n:
            continue
        mm = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", n)
        if mm is None:
            continue
        q2y, zpt = int(mm.group(1)), int(mm.group(2))
        if args.q2y and q2y != args.q2y:
            continue
        names.append((q2y, zpt, n))
    names.sort()
    nplot = 0
    for q2y, zpt, hname in names:
        if args.max_plots and nplot >= args.max_plots:
            break
        hist = tfile.Get(hname)
        fname = hname.replace("(MultiDim_5D_Histo)", "(Fit_Function)")
        func = tfile.Get(fname)
        if hist is None:
            continue
        cname = f"c_5D_{args.method}_{q2y}_{zpt}"
        cnv = ROOT.TCanvas(cname, cname, 700, 500)
        hist.SetTitle(f"5D {args.method}  Q2-y {q2y}  z-pT {zpt}")
        hist.Draw("E1")
        if func is not None:
            func.SetLineColor(ROOT.kRed)
            func.Draw("same")
        out = os.path.join(args.out_dir, f"Q2y{q2y:02d}_zpt{zpt:02d}.png")
        cnv.SaveAs(out)
        cnv.Close()
        del cnv
        nplot += 1
    tfile.Close()
    print(f"wrote {nplot} overlays to {args.out_dir}")


if __name__ == "__main__":
    main()
