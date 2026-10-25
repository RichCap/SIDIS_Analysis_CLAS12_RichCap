#!/usr/bin/env python3
# Draw the four RooUnfold diagnostics and the normalized closure scores.
# Reads the saved tables, not the unfolding output, so the axis choices can be redone.

import argparse
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)


def parse_args():
    parser = argparse.ArgumentParser(description="plot_3d_closure_study.py:\n\tPlot closure diagnostics and normalized scores.")
    parser.add_argument("-o", "--out_dir", default="Unfold_Iteration_Study_3D/Closure_Opt_3pct_4pct_5pct",
                        help="Study directory containing the score tables.\n")
    parser.add_argument("-l", "--label", default="initial",
                        help="Score-table label, matching scores_<label>.tsv.\n")
    parser.add_argument("-d", "--diagnostics", default="",
                        help="Diagnostics TSV. Default is diagnostics_long.tsv in --out_dir.\n")
    return parser.parse_args()


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


def series_from(rows, key):
    out = {}
    for row in rows:
        value = as_float(row.get(key, ""))
        if(value is None):
            continue
        out[int(row["k"])] = value
    return out


def data_range(hist, values):
    ordered = sorted(values)
    y_lo = ordered[0]
    y_hi = ordered[-1]
    # A late blow-up should not hide the iterations where the curve actually settles.
    if(len(ordered) >= 8):
        body = ordered[int(0.80 * (len(ordered) - 1))]
        body_span = body - y_lo
        if(body_span <= 0.0):
            body_span = abs(body) * 0.01 if(body != 0.0) else 1.0
        if((y_hi - y_lo) > 4.0 * body_span):
            y_hi = body
    span = y_hi - y_lo
    if(span <= 0.0):
        span = abs(y_lo) * 0.01 if(y_lo != 0.0) else 1.0
    pad = 0.12 * span
    hist.SetMinimum(y_lo - pad)
    hist.SetMaximum(y_hi + pad)


def draw_series(canvas, ipad, by_k, title, ytitle, mark_k, name):
    import ROOT
    canvas.cd(ipad)
    if(not by_k):
        return None
    ks = sorted(by_k)
    hist = ROOT.TH1D(name, title + ";Bayesian iteration;" + ytitle, max(ks) - min(ks) + 1, min(ks) - 0.5, max(ks) + 0.5)
    hist.SetDirectory(0)
    for k, value in by_k.items():
        hist.SetBinContent(hist.FindBin(float(k)), value)
    hist.SetLineWidth(2)
    hist.SetStats(0)
    data_range(hist, list(by_k.values()))
    hist.Draw("hist")
    if(mark_k is not None):
        line = ROOT.TLine(float(mark_k), hist.GetMinimum(), float(mark_k), hist.GetMaximum())
        line.SetLineColor(ROOT.kRed)
        line.SetLineStyle(2)
        line.Draw()
        hist._line = line
    return hist


def draw_band_lines(hist):
    import ROOT
    lines = []
    for level, color in ((0.10, ROOT.kGray + 2), (0.20, ROOT.kGray + 1)):
        if((level < hist.GetMinimum()) or (level > hist.GetMaximum())):
            continue
        line = ROOT.TLine(hist.GetXaxis().GetXmin(), level, hist.GetXaxis().GetXmax(), level)
        line.SetLineStyle(3)
        line.SetLineColor(color)
        line.Draw()
        lines.append(line)
    hist._bands = lines


def main():
    args = parse_args()
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diag_path = args.diagnostics or os.path.join(args.out_dir, "diagnostics_long.tsv")
    score_path = os.path.join(args.out_dir, f"scores_{args.label}.tsv")
    rec_path = os.path.join(args.out_dir, f"recommendations_{args.label}.tsv")
    if(not os.path.isfile(score_path)):
        print(f"Missing {score_path}", file=sys.stderr)
        return 1
    scores = read_tsv(score_path)
    recs = read_tsv(rec_path) if(os.path.isfile(rec_path)) else []
    mark = {}
    for row in recs:
        if(row.get("k_recommended", "") == ""):
            continue
        mark[(row["cut"], int(row["q2y"]))] = int(row["k_recommended"])
    grouped = {}
    for row in scores:
        key = (row["sample"], row["cut"], int(row["q2y"]))
        grouped.setdefault(key, []).append(row)
    plot_root = os.path.join(args.out_dir, "plots_" + args.label)
    os.makedirs(plot_root, exist_ok=True)
    written = 0
    for key in sorted(grouped):
        sample, cut, q2y = key
        rows = grouped[key]
        folder = os.path.join(plot_root, f"{sample}_cut{cut}")
        os.makedirs(folder, exist_ok=True)
        mark_k = mark.get((cut, q2y))
        tag = f"{sample}_{cut}_{q2y}"
        canvas = ROOT.TCanvas("c_" + tag, "c", 1200, 900)
        canvas.Divide(2, 2)
        keep = []
        keep.append(draw_series(canvas, 1, series_from(rows, "chi2"), f"Q^{{2}}-y {q2y}  {sample}  cut {cut}: #chi^{{2}}", "#chi^{2}", mark_k, "chi_" + tag))
        keep.append(draw_series(canvas, 2, series_from(rows, "mean_abs"), f"Q^{{2}}-y {q2y}: |mean residual|", "|mean residual|", mark_k, "mean_" + tag))
        keep.append(draw_series(canvas, 3, series_from(rows, "rms_aligned"), f"Q^{{2}}-y {q2y}: residual-mean error", "residual-mean error", mark_k, "rms_" + tag))
        keep.append(draw_series(canvas, 4, series_from(rows, "mean_error"), f"Q^{{2}}-y {q2y}: mean bin error", "mean bin error", mark_k, "err_" + tag))
        png = os.path.join(folder, f"diagnostics_Q2y_{q2y}.png")
        pdf = os.path.join(folder, f"diagnostics_Q2y_{q2y}.pdf")
        canvas.SaveAs(png)
        canvas.SaveAs(pdf)
        canvas2 = ROOT.TCanvas("b_" + tag, "b", 1200, 900)
        canvas2.Divide(2, 2)
        keep.append(draw_series(canvas2, 1, series_from(rows, "b_chi2"), f"Q^{{2}}-y {q2y}: b(#chi^{{2}})", "b", mark_k, "bchi_" + tag))
        keep.append(draw_series(canvas2, 2, series_from(rows, "b_mean"), f"Q^{{2}}-y {q2y}: b(|mean residual|)", "b", mark_k, "bmean_" + tag))
        keep.append(draw_series(canvas2, 3, series_from(rows, "b_rms"), f"Q^{{2}}-y {q2y}: b(residual-mean error)", "b", mark_k, "brms_" + tag))
        keep.append(draw_series(canvas2, 4, series_from(rows, "B"), f"Q^{{2}}-y {q2y}: combined closure B", "B", mark_k, "bsum_" + tag))
        png2 = os.path.join(folder, f"scores_Q2y_{q2y}.png")
        pdf2 = os.path.join(folder, f"scores_Q2y_{q2y}.pdf")
        for ipad, hist in ((1, keep[-4]), (2, keep[-3]), (3, keep[-2]), (4, keep[-1])):
            if(hist is None):
                continue
            canvas2.cd(ipad)
            draw_band_lines(hist)
        canvas2.SaveAs(png2)
        canvas2.SaveAs(pdf2)
        written += 1
        del canvas
        del canvas2
    print(f"Wrote {written} region plots under {plot_root}")
    if(not os.path.isfile(diag_path)):
        print(f"Diagnostics table not required for plotting: {diag_path}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
