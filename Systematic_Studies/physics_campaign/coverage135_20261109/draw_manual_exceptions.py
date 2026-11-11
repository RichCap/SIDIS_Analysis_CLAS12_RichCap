#!/usr/bin/env python3
# Draw the sector comparisons that pass 135 degrees and stay manually excluded.
# The default draws the historical three-panel figure. --electron_only draws eS4o alone.

import argparse
import json
import math
import os
import sys

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
REF = os.path.join(CAMP, "refinement_20261108")
SCAN_DIR = os.path.join(CAMP, "phi_h_coverage_20261109")
if(SCAN_DIR not in sys.path):
    sys.path.insert(0, SCAN_DIR)
import scan_phi_h_coverage as scan

PANELS = [
    {
        "title": "Electron in only sector 4",
        "subtitle": "Q^{2}-y bin 15, z-P_{T} bin 22",
        "q2y": 15,
        "zpt": 22,
        "variation": os.path.join(REF, "spline/electron_sector/eS4o"),
    },
    {
        "title": "#pi^{+} in only sector 4",
        "subtitle": "Q^{2}-y bin 15, z-P_{T} bin 21",
        "q2y": 15,
        "zpt": 21,
        "variation": os.path.join(REF, "spline/pion_sector/pipS4o"),
    },
    {
        "title": "#pi^{+} in only sector 5",
        "subtitle": "Q^{2}-y bin 9, z-P_{T} bin 9",
        "q2y": 9,
        "zpt": 9,
        "variation": os.path.join(REF, "spline/pion_sector/pipS5o"),
    },
]
NOMINAL_DIR = os.path.join(REF, "spline/nominal/acceptance")
KEY = "Fit_Pars_from_3D_Bayesian"


def bin_key(q2y, zpt):
    return "(Q2_y_Bin_%d)-(z_pT_Bin_%d)" % (q2y, zpt)


def load_cell(folder, q2y, zpt):
    payload = json.load(open(os.path.join(folder, "fit.json")))
    return payload[KEY][bin_key(q2y, zpt)]


def fetch(path, q2y, zpt):
    handle = ROOT.TFile.Open(path, "READ")
    if((handle is None) or handle.IsZombie()):
        raise SystemExit("unreadable %s" % path)
    hist, name = scan.fetch_histogram(handle, "Bayesian", q2y, zpt, "Smear")
    if(hist is None):
        handle.Close()
        raise SystemExit("missing histogram in %s" % path)
    clone = hist.Clone(name + "_clone")
    clone.SetDirectory(0)
    handle.Close()
    return clone, name


def empty_runs(hist):
    nbins = int(hist.GetNbinsX())
    empty = []
    for ibin in range(1, nbins + 1):
        content = float(hist.GetBinContent(ibin))
        if((math.isfinite(content)) and (content == 0.0)):
            empty.append(ibin)
    runs = []
    if(len(empty) == 0):
        return runs, False
    start = empty[0]
    previous = empty[0]
    for ibin in empty[1:]:
        if(ibin == previous + 1):
            previous = ibin
            continue
        runs.append((start, previous))
        start = ibin
        previous = ibin
    runs.append((start, previous))
    periodic = (empty[0] == 1) and (empty[-1] == nbins)
    return runs, periodic


def fit_window(hist):
    nbins = int(hist.GetNbinsX())
    first = None
    last = None
    for ibin in range(1, nbins + 1):
        content = float(hist.GetBinContent(ibin))
        if((not math.isfinite(content)) or (content == 0.0)):
            continue
        if(first is None):
            first = ibin
        last = ibin
    low = float(hist.GetXaxis().GetBinLowEdge(first))
    high = float(hist.GetXaxis().GetBinUpEdge(last))
    return low, high


def curve(name, cell, low, high):
    function = ROOT.TF1(name, "[0]*(1+[1]*cos(x*TMath::Pi()/180)+[2]*cos(2*x*TMath::Pi()/180))", low, high)
    function.SetParameter(0, float(cell["Fit_Par_A"]))
    function.SetParameter(1, float(cell["Fit_Par_B"]))
    function.SetParameter(2, float(cell["Fit_Par_C"]))
    function.SetLineWidth(2)
    return function


def parse_args():
    parser = argparse.ArgumentParser(description="Draw manual sector-exclusion comparisons from stored histograms.")
    parser.add_argument("-eo", "--electron_only", action="store_true", help="Draw only the electron sector 4 comparison at Q2-y 15, z-PT 22.")
    return parser.parse_args()


def main(electron_only=False):
    nominal_root = os.path.join(NOMINAL_DIR, "fit_copy.root")
    panels = [PANELS[0]] if(electron_only) else list(PANELS)
    if(electron_only):
        canvas = ROOT.TCanvas("manual_exceptions", "manual_exceptions", 1100, 800)
    else:
        canvas = ROOT.TCanvas("manual_exceptions", "manual_exceptions", 2100, 900)
        canvas.Divide(3, 1, 0.004, 0.004)
    kept = []
    report = []
    for index, panel in enumerate(panels, start=1):
        q2y = panel["q2y"]
        zpt = panel["zpt"]
        nominal_hist, nominal_name = fetch(nominal_root, q2y, zpt)
        variation_hist, variation_name = fetch(os.path.join(panel["variation"], "fit_copy.root"), q2y, zpt)
        nominal_cell = load_cell(NOMINAL_DIR, q2y, zpt)
        variation_cell = load_cell(panel["variation"], q2y, zpt)
        runs, periodic = empty_runs(variation_hist)
        low, high = fit_window(variation_hist)
        nominal_low, nominal_high = fit_window(nominal_hist)
        missing = 0.0
        for ibin in range(1, variation_hist.GetNbinsX() + 1):
            content = float(variation_hist.GetBinContent(ibin))
            if((math.isfinite(content)) and (content == 0.0)):
                missing += float(variation_hist.GetXaxis().GetBinWidth(ibin))
        center = 0.5 * (low + high)
        function = curve("var_%d" % index, variation_cell, low, high)
        nominal_function = curve("nom_%d" % index, nominal_cell, nominal_low, nominal_high)
        edge_low = function.Eval(low + 0.5)
        edge_high = function.Eval(high - 0.5)
        middle = function.Eval(center)
        report.append({
            "label": panel["title"],
            "nominal_histogram": nominal_name,
            "variation_histogram": variation_name,
            "missing_deg": missing,
            "empty_runs": [
                [float(variation_hist.GetXaxis().GetBinLowEdge(start)), float(variation_hist.GetXaxis().GetBinUpEdge(stop))]
                for start, stop in runs
            ],
            "periodic_edge_gap": periodic,
            "fit_low": low,
            "fit_high": high,
            "nominal_fit_low": nominal_low,
            "nominal_fit_high": nominal_high,
            "chi2": variation_cell["Chi2"],
            "ndf": variation_cell["NDF"],
            "nominal_chi2": nominal_cell["Chi2"],
            "nominal_ndf": nominal_cell["NDF"],
            "variation": {letter: [variation_cell["Fit_Par_%s" % letter], variation_cell["Fit_Par_%s_ERR" % letter]] for letter in ("A", "B", "C")},
            "nominal": {letter: [nominal_cell["Fit_Par_%s" % letter], nominal_cell["Fit_Par_%s_ERR" % letter]] for letter in ("A", "B", "C")},
            "curve_low": edge_low,
            "curve_middle": middle,
            "curve_high": edge_high,
        })
        if(electron_only):
            pad = canvas.cd()
            pad.SetLeftMargin(0.12)
            pad.SetRightMargin(0.04)
            pad.SetBottomMargin(0.12)
            pad.SetTopMargin(0.16)
        else:
            pad = canvas.cd(index)
            pad.SetLeftMargin(0.20)
            pad.SetRightMargin(0.04)
            pad.SetBottomMargin(0.15)
            pad.SetTopMargin(0.24)
        ymax = 0.0
        for hist in (nominal_hist, variation_hist):
            for ibin in range(1, hist.GetNbinsX() + 1):
                value = float(hist.GetBinContent(ibin)) + float(hist.GetBinError(ibin))
                if(value > ymax):
                    ymax = value
        nominal_hist.SetTitle("")
        nominal_hist.SetLineColor(ROOT.kBlue + 1)
        nominal_hist.SetLineWidth(2)
        nominal_hist.SetFillStyle(0)
        nominal_hist.SetMarkerStyle(1)
        variation_hist.SetLineColor(ROOT.kRed + 1)
        variation_hist.SetLineWidth(2)
        variation_hist.SetFillStyle(0)
        variation_hist.SetMarkerStyle(1)
        nominal_hist.GetXaxis().SetTitle("#phi_{h} (deg)")
        nominal_hist.GetYaxis().SetTitle("Yield")
        title_size = 0.045 if(electron_only) else 0.055
        label_size = 0.040 if(electron_only) else 0.048
        nominal_hist.GetXaxis().SetTitleSize(title_size)
        nominal_hist.GetYaxis().SetTitleSize(title_size)
        nominal_hist.GetXaxis().SetLabelSize(label_size)
        nominal_hist.GetYaxis().SetLabelSize(label_size)
        nominal_hist.GetYaxis().SetTitleOffset(1.35 if(electron_only) else 1.85)
        nominal_hist.SetMinimum(0.0)
        nominal_hist.SetMaximum(1.55 * ymax)
        nominal_hist.Draw("HIST E0")
        variation_hist.Draw("HIST E0 SAME")
        nominal_function.SetLineColor(ROOT.kBlue + 1)
        function.SetLineColor(ROOT.kRed + 1)
        nominal_function.Draw("SAME")
        function.Draw("SAME")
        if(electron_only):
            legend = ROOT.TLegend(0.62, 0.72, 0.94, 0.86)
            legend.SetTextSize(0.038)
        else:
            legend = ROOT.TLegend(0.46, 0.58, 0.94, 0.74)
            legend.SetTextSize(0.042)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.AddEntry(nominal_hist, "Nominal", "le")
        legend.AddEntry(variation_hist, "Variation", "le")
        legend.Draw()
        title = ROOT.TLatex()
        title.SetNDC()
        title.SetTextSize(0.040 if(electron_only) else 0.046)
        title.DrawLatex(0.14 if(electron_only) else 0.22, 0.955 if(electron_only) else 0.905, panel["title"])
        subtitle = ROOT.TLatex()
        subtitle.SetNDC()
        subtitle.SetTextSize(0.034 if(electron_only) else 0.040)
        subtitle.DrawLatex(0.14 if(electron_only) else 0.22, 0.905 if(electron_only) else 0.845, panel["subtitle"])
        kept.append((nominal_hist, variation_hist, nominal_function, function, legend, title, subtitle))
    canvas.Update()
    stem = "sector_manual_exceptions_electron" if(electron_only) else "sector_manual_exceptions"
    out_path = os.path.join(HERE, stem + ".pdf")
    canvas.SaveAs(out_path)
    thesis_dir = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis/Results/Systematic_Images"
    os.makedirs(thesis_dir, exist_ok=True)
    thesis_path = os.path.join(thesis_dir, "Sector_Coverage_Exceptions.pdf")
    canvas.SaveAs(thesis_path)
    report_path = os.path.join(HERE, stem + ".json")
    with open(report_path, "w") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print("wrote %s" % out_path)
    print("wrote %s" % thesis_path)
    for row in report:
        print(row["label"], "missing", row["missing_deg"], "fit", row["fit_low"], row["fit_high"])


if(__name__ == "__main__"):
    main(parse_args().electron_only)
