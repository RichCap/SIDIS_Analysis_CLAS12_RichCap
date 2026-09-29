#!/usr/bin/env python3
# One page per acceptance cut and Q2-y region: fitted B versus z-pT for the four samples.

import glob
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)


def load_rows(fit_dir):
    rows = []
    for path in glob.glob(os.path.join(fit_dir, "*.tsv")):
        name = os.path.basename(path)
        if(("_k15." in name) or ("_k25." in name)):
            continue
        for line in open(path).read().splitlines()[1:]:
            p = line.split("\t")
            if(p[6] not in ("pass", "fail")):
                continue
            rows.append({
                "cut": p[0],
                "sample": p[1],
                "q2y": int(p[3]),
                "zpt": int(p[4]),
                "B": float(p[7]),
                "C": float(p[9]),
                "Bref": float(p[11]),
                "Cref": float(p[12]),
            })
    return rows


def main():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    out_dir = "Unfold_Iteration_Study_3D/DataFirst_4Way_Closure_3pct_4pct_5pct"
    rows = load_rows(os.path.join(out_dir, "fits"))
    plot_dir = os.path.join(out_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    samples = ["nominal", "Acc", "Spline", "AccSpline"]
    n_written = 0
    for cut in ("0.030", "0.040", "0.050"):
        for q2y in range(1, 18):
            canvas = ROOT.TCanvas(f"c_{cut}_{q2y}", "c", 1200, 900)
            canvas.Divide(2, 2)
            keep = []
            for ipad, sample in enumerate(samples, start=1):
                canvas.cd(ipad)
                sub = [r for r in rows if(r["cut"] == cut and r["q2y"] == q2y and r["sample"] == sample)]
                sub.sort(key=lambda item: item["zpt"])
                if(not sub):
                    continue
                n = len(sub)
                graph = ROOT.TGraph(n)
                ref = ROOT.TGraph(n)
                for i, row in enumerate(sub):
                    graph.SetPoint(i, row["zpt"], row["B"])
                    ref.SetPoint(i, row["zpt"], row["Bref"])
                graph.SetTitle(f"{sample}   Q^{{2}}-y {q2y}   cut {cut};z-p_{{T}} bin;fitted B")
                graph.SetMarkerStyle(20)
                graph.SetMarkerSize(0.8)
                ys = sorted([row["B"] for row in sub] + [row["Bref"] for row in sub])
                lo = ys[int(0.05 * (len(ys) - 1))]
                hi = ys[int(0.95 * (len(ys) - 1))]
                span = hi - lo
                if(span <= 0.0):
                    span = 0.02
                # A few slices with a failed moment should not hide the rest of the bin.
                if((ys[-1] - ys[0]) > 4.0 * span):
                    y_lo, y_hi = lo, hi
                else:
                    y_lo, y_hi = ys[0], ys[-1]
                pad = 0.15 * (y_hi - y_lo if(y_hi != y_lo) else 0.05)
                graph.SetMinimum(y_lo - pad)
                graph.SetMaximum(y_hi + pad)
                graph.Draw("AP")
                ref.SetLineColor(ROOT.kRed)
                ref.SetLineWidth(2)
                ref.Draw("L")
                keep.append((graph, ref))
            png = os.path.join(plot_dir, f"B_cut{cut}_Q2y{q2y}.png")
            canvas.SaveAs(png)
            n_written += 1
            del canvas
    print(f"Wrote {n_written} plots in {plot_dir}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
