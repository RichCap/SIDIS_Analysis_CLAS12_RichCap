#!/usr/bin/env python3
# 10/28/2026: one square PDF of the finished 5D iteration curves.
# Reads iteration_study_errors.root. Does not unfold.

import os
import sys

_HERE = os.path.abspath(os.path.dirname(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, ".."))
sys.path.insert(0, _REPO)

import score_data_iteration_stability as stability

SCAN = os.path.join(_HERE, "iteration_study_errors.root")
OUT  = os.path.join(_HERE, "Iteration_Tests_5D_Diagnostics_for_Experimental_Data_020_AccCut_lundvpk.pdf")
# key, main title, y-axis title
PANELS = (
    ("chi2", "#chi^{2}", "#chi^{2}"),
    ("mean_abs", "Absolute Mean Residual", "|#mu|"),
    ("rms_aligned", "Residual-Mean Error", "#sigma_{#mu}"),
    ("mean_error", "Mean Bin Error", "Mean Bin Error"),
)


def load_rows():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    tfile = ROOT.TFile.Open(SCAN, "READ")
    if((tfile is None) or tfile.IsZombie()):
        raise SystemExit("could not open %s" % SCAN)
    chi2_h = tfile.Get("Iteration_Study_Chi2")
    mean_h = tfile.Get("Iteration_Study_MeanResiduals")
    err_h  = tfile.Get("Iteration_Study_RMSError")
    rows = []
    for index in range(1, chi2_h.GetNbinsX() + 1):
        k_val = int(round(chi2_h.GetXaxis().GetBinCenter(index)))
        signed = float(mean_h.GetBinContent(index))
        rows.append({
            "k": k_val,
            "chi2": float(chi2_h.GetBinContent(index)),
            "mean_residual": signed,
            "mean_abs": abs(signed),
            "rms_aligned": float(mean_h.GetBinError(index)),
            "mean_error": float(err_h.GetBinContent(index)),
        })
    tfile.Close()
    rows.sort(key=lambda item: item["k"])
    return rows


def y_limits(values):
    y_lo = min(values)
    y_hi = max(values)
    pad = 0.08 * (y_hi - y_lo)
    return y_lo - pad, y_hi + pad


def panel_title(main_name, y_title):
    sub = "Based on Unfolding Tests with 2% Acceptance Cuts"
    return "#font[22]{#splitline{#scale[1.15]{%s}}{#splitline{#scale[0.9]{vs Bayesian Iterations}}{#scale[0.8]{%s}}}};# of Iterations; " % (main_name, sub)


def main():
    import ROOT
    rows = load_rows()
    scored, good = stability.score_curve(rows, stability.STEP_MAX, stability.RUN_LEN, stability.STABLE_REL)
    rec = stability.recommend(scored, good, None)
    if((rec["status"] != "ok") or (rec["k_selected"] != 5)):
        raise SystemExit("scorer returned %s" % rec)
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaperSize(16.5, 16.5)
    canvas = ROOT.TCanvas("five", "five", 1200, 1200)
    frames = (
        (0.01, 0.51, 0.50, 0.99),
        (0.50, 0.51, 0.99, 0.99),
        (0.01, 0.01, 0.50, 0.49),
        (0.50, 0.01, 0.99, 0.49),
    )
    keep = []
    k_line = float(rec["k_selected"])
    for index, (box, (key, main_name, y_title)) in enumerate(zip(frames, PANELS)):
        pad = ROOT.TPad("pad%d" % index, "pad", box[0], box[1], box[2], box[3])
        pad.SetLeftMargin(0.18)
        pad.SetRightMargin(0.04)
        pad.SetBottomMargin(0.14)
        pad.SetTopMargin(0.22)
        pad.SetGrid(1, 1)
        canvas.cd()
        pad.Draw()
        pad.cd()
        graph = ROOT.TGraph(len(rows))
        values = []
        for i, row in enumerate(rows):
            graph.SetPoint(i, float(row["k"]), float(row[key]))
            values.append(float(row[key]))
        y_lo, y_hi = y_limits(values)
        graph.SetTitle(panel_title(main_name, y_title))
        graph.SetLineColor(ROOT.kBlue + 2)
        graph.SetLineWidth(2)
        graph.GetXaxis().SetLimits(0.5, 10.5)
        graph.GetXaxis().SetTitleSize(0.055)
        graph.GetYaxis().SetTitleSize(0.055)
        graph.GetXaxis().SetLabelSize(0.045)
        graph.GetYaxis().SetLabelSize(0.045)
        graph.GetXaxis().SetTitleOffset(0.95)
        graph.GetXaxis().SetTitleFont(22)
        graph.GetYaxis().SetTitleFont(22)
        graph.GetXaxis().SetLabelFont(22)
        graph.GetYaxis().SetLabelFont(22)
        graph.SetMinimum(y_lo)
        graph.SetMaximum(y_hi)
        graph.Draw("AL")
        label = ROOT.TLatex()
        label.SetNDC(True)
        label.SetTextFont(22)
        label.SetTextSize(0.055)
        label.SetTextAngle(90)
        label.SetTextAlign(22)
        label.DrawLatex(0.06, 0.50, y_title)
        line = ROOT.TLine(k_line, y_lo, k_line, y_hi)
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(2)
        line.Draw("same")
        keep.append((pad, graph, label, line))
    canvas.SaveAs(OUT)
    canvas.Close()
    print("Wrote %s" % OUT)
    print("k_selected %s window %s-%s" % (rec["k_selected"], rec["k_lo"], rec["k_hi"]))
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
