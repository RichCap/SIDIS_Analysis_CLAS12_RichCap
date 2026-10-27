#!/usr/bin/env python3

# Standalone LUND VPK versus rho0_new exclusive rho0 comparison.
# Does not refit normalizations and does not change Get_rho_Normalization_values.py.

import argparse
import csv
import json
import os
import sys

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if(SCRIPT_DIR not in sys.path):
    sys.path.insert(0, SCRIPT_DIR)

from Get_rho_Normalization_values import Slice_4D_Histo_Bins_For_phi_h_Plots, calculate_weighted_percentage, presentation_project_xy, phi_h_1D_Compare_in_z_pT_Images_Together, Other_1D_Kinematic_Comparison_Images
from MyCommonAnalysisFunction_richcap import Get_Num_of_z_pT_Bins_w_Migrations, skip_condition_z_pT_bins

STAGE_NAME = "Full_SIDIS"
ROOT_VARIABLES = ["(phi_t)_(Q2_y_z_pT_4D_Bins)", "(Q2)_(y)", "(Q2)_(xB)", "(z)_(pT)"]
SAMPLE_ORDER = ["lundvpk", "rho0_new"]
SAMPLE_INFO = {
    "lundvpk": {"n_rho": 4.624974, "raw_phi": 99050.0, "legend": "LUND VPK", "root_name": "LUND VPK", "suffix": "Lundvpk_SIDIS"},
    "rho0_new": {"n_rho": 2.4020823572173544, "raw_phi": 261381.0, "legend": "#rho^{0} new", "root_name": "#rho^{0} new", "suffix": "Rho0New_SIDIS"},
}
HISTORICAL_BINS = [(5, 16, "historical_typical"), (7, 2, "historical_maximum"), (5, 29, "historical_minimum")]
KINEMATIC_SPECS = [
    {"key": "Q2", "pair": "(Q2)_(y)", "axis": 0, "label": "Q^{2}", "unit": "GeV^{2}", "file": "Q2"},
    {"key": "y",  "pair": "(Q2)_(y)", "axis": 1, "label": "y",      "unit": "",        "file": "y"},
    {"key": "z",  "pair": "(z)_(pT)", "axis": 0, "label": "z",      "unit": "",        "file": "z"},
    {"key": "pT", "pair": "(z)_(pT)", "axis": 1, "label": "P_{T}",  "unit": "GeV",     "file": "pT"},
    {"key": "xB", "pair": "(Q2)_(xB)", "axis": 1, "label": "x_{B}", "unit": "",        "file": "xB"},
]
COLOR_DATA = ROOT.kBlue + 1
COLOR_MC   = ROOT.kGreen + 2
COLOR_SUB  = ROOT.kCyan + 2
COLOR_VPK  = ROOT.kBlue + 1
COLOR_NEW  = ROOT.kRed + 1
COLOR_RATIO = ROOT.kBlack


class DrawArgs(object):
    def __init__(self, token, name, title, verbose=False):
        self.source_token = token
        self.file_format  = "pdf"
        self.name         = name
        self.title        = title
        self.verbose      = verbose
        self.no_save      = False


def parse_args():
    parser = argparse.ArgumentParser(description="Compare preweighted lundvpk and rho0_new exclusive rho0 backgrounds on the same reconstructed SIDIS data.")
    parser.add_argument("-f2", "--file2", default=os.path.join(SCRIPT_DIR, "hadd_ROOT_files_From_using_RDataFrames", "SIDIS_epip_Response_Matrices_from_RDataFrames_2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_All.root"), help="Presentation ROOT file with data and both reconstructed MC samples.\n")
    parser.add_argument("-o", "--output_dir", default=os.path.join(SCRIPT_DIR, "Lundvpk_vs_rho0_new_Exclusive_Rho0_Comparison"), help="New directory for figures, tables, and the report. Existing thesis figures are not written here.\n")
    parser.add_argument("-es", "--established_diagnostics", action="store_true", help="Also run the existing phi and kinematic drawers into figures/established. Those canvases are large.\n")
    parser.add_argument("-eo", "--established_only", action="store_true", help="Skip slide figures and rerun only the existing diagnostic drawers.\n")
    parser.add_argument("-V", "--verbose", action="store_true", help="Print the 4D bin lookup used by the existing slicer.\n")
    return parser.parse_args()


def axis_caption(label, unit):
    if(unit):
        return "%s (%s)" % (label, unit)
    return label


def style_hist(hist, line_color, y_title, x_title):
    hist.SetDirectory(0)
    hist.SetLineColor(line_color)
    hist.SetLineWidth(3)
    hist.SetFillStyle(0)
    hist.SetMarkerSize(0)
    hist.SetStats(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle(x_title)
    hist.GetYaxis().SetTitle(y_title)
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetXaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetLabelSize(0.045)
    hist.GetXaxis().SetTitleOffset(0.95)
    hist.GetYaxis().SetTitleOffset(1.05)
    hist.GetXaxis().SetNdivisions(505)
    return hist


def hold(canvas, *objects):
    if(not hasattr(canvas, "held_objects")):
        canvas.held_objects = []
    for obj in objects:
        canvas.held_objects.append(obj)


def content_bin_edges(hist):
    first_bin = None
    last_bin  = None
    for bin_index in range(1, hist.GetNbinsX() + 1):
        if(hist.GetBinContent(bin_index) > 0):
            if(first_bin is None):
                first_bin = bin_index
            last_bin = bin_index
    if(first_bin is None):
        return hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax()
    low  = hist.GetXaxis().GetBinLowEdge(first_bin)
    high = hist.GetXaxis().GetBinUpEdge(last_bin)
    span = high - low
    if(span <= 0):
        span = 1.0
    return low - 0.02 * span, high + 0.02 * span


def project_1d(hist2, axis, name):
    clone = hist2.Clone("%s_src" % name)
    clone.SetDirectory(0)
    if(axis == 0):
        projected = clone.ProjectionX(name)
    else:
        projected = clone.ProjectionY(name)
    projected.SetDirectory(0)
    return projected


def decide_scale(integral, n_rho, raw_expected, token):
    implied_raw = integral / n_rho
    preweighted = abs(implied_raw - raw_expected) < 0.5
    unweighted  = abs(integral - raw_expected) < 0.5
    if(preweighted and unweighted):
        raise SystemExit("normalization check is ambiguous for %s" % token)
    if(preweighted):
        print("  %s phi integral %.6f is already weighted: integral / %.12f = %.6f (expected raw %.1f). No additional scale." % (token, integral, n_rho, implied_raw, raw_expected))
        return 1.0, True, implied_raw
    if(unweighted):
        print("  %s phi integral %.6f matches the raw count. Applying the registered factor once." % (token, integral))
        return n_rho, False, integral
    raise SystemExit("phi integral %.6f for %s matches neither the preweighted sample nor the raw count %.1f" % (integral, token, raw_expected))


def histogram_names(variable, token):
    smeared   = variable.replace(")", "_smeared)")
    data_src  = "(Normal_2D)_(rdf)_(cut_Complete_SIDIS)_(SMEAR='')_(Q2_Y_Bin)_%s" % variable
    mc_src    = "(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_Y_Bin)_%s_(%s)" % (smeared, token)
    data_dest = "(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(exclusive_rho_individual)_%s_%s" % (variable, STAGE_NAME)
    mc_dest   = "(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_%s_(%s)_%s_(Scaled)" % (smeared, token, STAGE_NAME)
    return data_src, mc_src, data_dest, mc_dest


def load_comparisons(path):
    root_file = ROOT.TFile.Open(path, "READ")
    if((not root_file) or root_file.IsZombie()):
        raise SystemExit("could not open %s" % path)
    data_projections = {}
    sample_pack      = {}
    for variable in ROOT_VARIABLES:
        data_src, mc_src, data_dest, mc_dest = histogram_names(variable, "lundvpk")
        data_hist = root_file.Get(data_src)
        if(not data_hist):
            raise SystemExit("missing data histogram %s" % data_src)
        data_xy = presentation_project_xy(data_hist, "presentation_data_%s" % variable)
        data_xy.SetName(data_dest)
        data_projections[variable] = data_xy
    for token in SAMPLE_ORDER:
        info = SAMPLE_INFO[token]
        projections = {}
        removed     = {}
        phi_name = histogram_names("(phi_t)_(Q2_y_z_pT_4D_Bins)", token)[1]
        phi_hist = root_file.Get(phi_name)
        if(not phi_hist):
            raise SystemExit("missing %s" % phi_name)
        scale, preweighted, implied_raw = decide_scale(phi_hist.Integral(), info["n_rho"], info["raw_phi"], token)
        for variable in ROOT_VARIABLES:
            data_src, mc_src, data_dest, mc_dest = histogram_names(variable, token)
            mc_hist = root_file.Get(mc_src)
            if(not mc_hist):
                raise SystemExit("missing %s" % mc_src)
            mc_xy = presentation_project_xy(mc_hist, "presentation_mc_%s_%s" % (token, variable))
            if(scale != 1.0):
                mc_xy.Scale(scale)
            mc_xy.SetName(mc_dest)
            data_for_sample = data_projections[variable].Clone("%s_%s" % (data_projections[variable].GetName(), token))
            data_for_sample.SetDirectory(0)
            data_for_sample.SetName(data_dest)
            subtracted = data_for_sample.Clone("%s_(Removed_Background)" % data_dest)
            subtracted.SetDirectory(0)
            subtracted.Add(mc_xy, -1.0)
            projections[variable] = mc_xy
            removed[variable]     = subtracted
            projections["data_%s" % variable] = data_for_sample
        drawer_dict = {}
        for variable in ROOT_VARIABLES:
            data_dest = histogram_names(variable, token)[2]
            mc_dest   = histogram_names(variable, token)[3]
            drawer_dict[data_dest] = projections["data_%s" % variable]
            drawer_dict[mc_dest]   = projections[variable]
            drawer_dict[removed[variable].GetName()] = removed[variable]
        sample_pack[token] = {
            "scale": scale,
            "preweighted": preweighted,
            "implied_raw": implied_raw,
            "phi_integral": projections["(phi_t)_(Q2_y_z_pT_4D_Bins)"].Integral(),
            "projections": projections,
            "removed": removed,
            "drawer_dict": drawer_dict,
        }
    root_file.Close()
    return data_projections, sample_pack


def retained_bins():
    kept = []
    for q2y_bin in range(1, 18):
        z_max = int(Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2y_bin)[1])
        for zpt_bin in range(1, z_max + 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin)):
                continue
            kept.append((q2y_bin, zpt_bin))
    return kept


def slice_phi(draw_args, hist, q2y_bin, zpt_bin, tag):
    renamed = hist.Clone("%s_%s_%d_%d" % (hist.GetName(), tag, q2y_bin, zpt_bin))
    renamed.SetDirectory(0)
    sliced = Slice_4D_Histo_Bins_For_phi_h_Plots(draw_args, renamed, q2y_bin, zpt_bin, Use_All_Name=False)
    if(sliced is None):
        return None
    sliced.SetDirectory(0)
    return sliced


def bin_record(q2y_bin, zpt_bin, data_yield, mc_yield):
    if(data_yield <= 0):
        percent = None
    else:
        percent = 100.0 * mc_yield / data_yield
    return {"q2y": q2y_bin, "zpt": zpt_bin, "data_yield": data_yield, "mc_yield": mc_yield, "percent": percent}


def update_extreme(summary, record):
    if(record["percent"] is None):
        return
    if((summary["minimum"] is None) or (record["percent"] <= summary["minimum"]["percent"])):
        summary["minimum"] = record
    if((summary["maximum"] is None) or (record["percent"] >= summary["maximum"]["percent"])):
        summary["maximum"] = record


def summarize_bins(records):
    usable = [record for record in records if(record["percent"] is not None)]
    data_sum = 0.0
    mc_sum   = 0.0
    percent_sum = 0.0
    for record in usable:
        data_sum    += record["data_yield"]
        mc_sum      += record["mc_yield"]
        percent_sum += record["percent"]
    mean_percent = percent_sum / len(usable) if(len(usable) > 0) else 0.0
    integrated   = 100.0 * mc_sum / data_sum if(data_sum > 0) else 0.0
    closest = None
    for record in usable:
        distance = abs(record["percent"] - mean_percent)
        if((closest is None) or (distance <= closest[0])):
            closest = (distance, record)
    summary = {
        "n_bins": len(records),
        "n_positive_data": len(usable),
        "data_sum": data_sum,
        "mc_sum": mc_sum,
        "integrated_percent": integrated,
        "unweighted_mean_percent": mean_percent,
        "minimum": None,
        "maximum": None,
        "closest_to_mean": None if(closest is None) else closest[1],
    }
    for record in records:
        update_extreme(summary, record)
    return summary


def lookup_bin(records, q2y_bin, zpt_bin):
    for record in records:
        if((record["q2y"] == q2y_bin) and (record["zpt"] == zpt_bin)):
            return record
    return None


def collect_bin_table(draw_args, data_phi, sample_pack, bins):
    rows = []
    phi_sums = {"data": None}
    for token in SAMPLE_ORDER:
        phi_sums[token] = None
    missing = []
    for index, (q2y_bin, zpt_bin) in enumerate(bins):
        data_slice = slice_phi(draw_args, data_phi, q2y_bin, zpt_bin, "data")
        if(data_slice is None):
            missing.append((q2y_bin, zpt_bin))
            continue
        data_yield = data_slice.Integral()
        if(phi_sums["data"] is None):
            phi_sums["data"] = data_slice.Clone("phi_sum_data_retained")
            phi_sums["data"].SetDirectory(0)
            phi_sums["data"].Reset()
            phi_sums["data"].Add(data_slice)
        else:
            phi_sums["data"].Add(data_slice)
        row = {"q2y": q2y_bin, "zpt": zpt_bin, "data_yield": data_yield}
        for token in SAMPLE_ORDER:
            mc_slice = slice_phi(draw_args, sample_pack[token]["projections"]["(phi_t)_(Q2_y_z_pT_4D_Bins)"], q2y_bin, zpt_bin, token)
            if(mc_slice is None):
                missing.append((q2y_bin, zpt_bin, token))
                row["%s_yield" % token] = 0.0
                row["%s_percent" % token] = None
                continue
            mc_yield = mc_slice.Integral()
            check = calculate_weighted_percentage(data_slice, mc_slice)
            if(data_yield <= 0):
                percent = None
            else:
                percent = 100.0 * mc_yield / data_yield
                if(abs(percent - check) > 1.0e-6):
                    print("percentage mismatch in bin %d %d %s: %.8f vs %.8f" % (q2y_bin, zpt_bin, token, percent, check))
            row["%s_yield" % token] = mc_yield
            row["%s_percent" % token] = percent
            if(phi_sums[token] is None):
                phi_sums[token] = mc_slice.Clone("phi_sum_%s_retained" % token)
                phi_sums[token].SetDirectory(0)
            else:
                phi_sums[token].Add(mc_slice)
        if((row["lundvpk_percent"] is None) or (row["rho0_new_percent"] is None)):
            row["difference_percentage_points"] = None
        else:
            row["difference_percentage_points"] = row["rho0_new_percent"] - row["lundvpk_percent"]
        rows.append(row)
        if((index + 1) % 100 == 0):
            print("  sliced %d / %d retained bins" % (index + 1, len(bins)))
    per_sample = {}
    for token in SAMPLE_ORDER:
        records = []
        for row in rows:
            records.append(bin_record(row["q2y"], row["zpt"], row["data_yield"], row["%s_yield" % token]))
        per_sample[token] = {"records": records, "summary": summarize_bins(records)}
    if(len(missing) > 0):
        print("missing 4D slices: %s" % str(missing[:12]))
    return rows, per_sample, phi_sums, missing


def rows_from_histograms(variable_key, data_hist, mc_hists, scope):
    rows = []
    n_bins = data_hist.GetNbinsX()
    for bin_index in range(1, n_bins + 1):
        data_yield = data_hist.GetBinContent(bin_index)
        row = {
            "variable": variable_key,
            "scope": scope,
            "bin": bin_index,
            "bin_low": data_hist.GetXaxis().GetBinLowEdge(bin_index),
            "bin_high": data_hist.GetXaxis().GetBinUpEdge(bin_index),
            "bin_center": data_hist.GetXaxis().GetBinCenter(bin_index),
            "data_yield": data_yield,
        }
        for token in SAMPLE_ORDER:
            mc_yield = mc_hists[token].GetBinContent(bin_index)
            row["%s_yield" % token] = mc_yield
            if(data_yield > 0):
                row["%s_percent" % token] = 100.0 * mc_yield / data_yield
            else:
                row["%s_percent" % token] = None
        rows.append(row)
    return rows


def make_graph(hist_data, hist_mc, name):
    graph = ROOT.TGraph()
    graph.SetName(name)
    point = 0
    for bin_index in range(1, hist_data.GetNbinsX() + 1):
        data_yield = hist_data.GetBinContent(bin_index)
        if(data_yield <= 0):
            continue
        percent = 100.0 * hist_mc.GetBinContent(bin_index) / data_yield
        graph.SetPoint(point, hist_data.GetXaxis().GetBinCenter(bin_index), percent)
        point += 1
    return graph


def make_ratio_graph(hist_num, hist_den, name):
    graph = ROOT.TGraph()
    graph.SetName(name)
    point = 0
    for bin_index in range(1, hist_den.GetNbinsX() + 1):
        denominator = hist_den.GetBinContent(bin_index)
        if(denominator <= 0):
            continue
        graph.SetPoint(point, hist_den.GetXaxis().GetBinCenter(bin_index), hist_num.GetBinContent(bin_index) / denominator)
        point += 1
    return graph


def draw_legend_pad(pad, entries, lines):
    pad.cd()
    pad.SetFillColor(ROOT.kWhite)
    legend = ROOT.TLegend(0.08, 0.78, 0.96, 0.97)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.050)
    for hist, label in entries:
        legend.AddEntry(hist, label, "l")
    legend.Draw()
    texts = []
    y_pos = 0.70
    for line in lines:
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextFont(42)
        latex.SetTextSize(0.046)
        latex.DrawLatex(0.08, y_pos, line)
        texts.append(latex)
        y_pos -= 0.058
    return legend, texts


def save_canvas(canvas, path):
    canvas.SaveAs(path)
    print("saved %s" % path)
    canvas.Close()


def draw_data_overlay(path, title, x_title, data_hist, mc_hist, sub_hist, mc_label, note_lines):
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas(os.path.basename(path).replace(".", "_"), title, 1500, 1000)
    canvas.SetFillColor(ROOT.kWhite)
    pad_top = ROOT.TPad("top_%s" % canvas.GetName(), "", 0.0, 0.31, 0.76, 1.0)
    pad_bot = ROOT.TPad("bot_%s" % canvas.GetName(), "", 0.0, 0.0, 0.76, 0.31)
    pad_leg = ROOT.TPad("leg_%s" % canvas.GetName(), "", 0.76, 0.0, 1.0, 1.0)
    for pad in [pad_top, pad_bot, pad_leg]:
        pad.SetFillColor(ROOT.kWhite)
        pad.Draw()
    pad_top.cd()
    pad_top.SetLeftMargin(0.18)
    pad_top.SetRightMargin(0.03)
    pad_top.SetBottomMargin(0.02)
    pad_top.SetTopMargin(0.10)
    data_draw = style_hist(data_hist.Clone(data_hist.GetName() + "_draw"), COLOR_DATA, "Reconstructed yield", "")
    mc_draw   = style_hist(mc_hist.Clone(mc_hist.GetName() + "_draw"), COLOR_MC, "Reconstructed yield", "")
    sub_draw  = style_hist(sub_hist.Clone(sub_hist.GetName() + "_draw"), COLOR_SUB, "Reconstructed yield", "")
    data_draw.GetXaxis().SetLabelSize(0)
    x_low, x_high = content_bin_edges(data_draw)
    y_max = max(data_draw.GetMaximum(), mc_draw.GetMaximum(), sub_draw.GetMaximum())
    y_min = min(0.0, data_draw.GetMinimum(), mc_draw.GetMinimum(), sub_draw.GetMinimum())
    data_draw.GetXaxis().SetRangeUser(x_low, x_high)
    data_draw.GetYaxis().SetRangeUser(y_min, 1.18 * y_max if(y_max > 0) else 1.0)
    data_draw.SetTitle(title)
    data_draw.Draw("hist")
    mc_draw.Draw("hist same")
    sub_draw.Draw("hist same")
    pad_bot.cd()
    pad_bot.SetLeftMargin(0.18)
    pad_bot.SetRightMargin(0.03)
    pad_bot.SetTopMargin(0.04)
    pad_bot.SetBottomMargin(0.34)
    graph = make_graph(data_hist, mc_hist, data_hist.GetName() + "_contam")
    graph.SetLineColor(COLOR_MC)
    graph.SetLineWidth(3)
    graph.SetMarkerStyle(0)
    graph.SetTitle("")
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle("Contamination (%)")
    graph.GetXaxis().SetTitleSize(0.11)
    graph.GetYaxis().SetTitleSize(0.09)
    graph.GetXaxis().SetLabelSize(0.09)
    graph.GetYaxis().SetLabelSize(0.08)
    graph.GetXaxis().SetTitleOffset(1.20)
    graph.GetYaxis().SetTitleOffset(1.05)
    graph.GetXaxis().SetRangeUser(x_low, x_high)
    graph.GetYaxis().SetRangeUser(0.0, max(1.0, 1.25 * graph.GetYaxis().GetXmax() if(graph.GetN() > 0) else 1.0))
    if(graph.GetN() > 0):
        y_values = [graph.GetY()[point] for point in range(graph.GetN())]
        graph.GetYaxis().SetRangeUser(0.0, max(y_values) * 1.25)
    graph.Draw("AL")
    pad_leg.cd()
    legend, text = draw_legend_pad(pad_leg, [(data_draw, "Data before subtraction"), (mc_draw, mc_label), (sub_draw, "Data after subtraction")], note_lines)
    hold(canvas, pad_top, pad_bot, pad_leg, data_draw, mc_draw, sub_draw, graph, legend, text)
    save_canvas(canvas, path)


def draw_mc_overlay(path, title, x_title, y_title, hist_vpk, hist_new, ratio_name):
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas(os.path.basename(path).replace(".", "_"), title, 1500, 1000)
    canvas.SetFillColor(ROOT.kWhite)
    pad_top = ROOT.TPad("top_%s" % canvas.GetName(), "", 0.0, 0.31, 0.76, 1.0)
    pad_bot = ROOT.TPad("bot_%s" % canvas.GetName(), "", 0.0, 0.0, 0.76, 0.31)
    pad_leg = ROOT.TPad("leg_%s" % canvas.GetName(), "", 0.76, 0.0, 1.0, 1.0)
    for pad in [pad_top, pad_bot, pad_leg]:
        pad.SetFillColor(ROOT.kWhite)
        pad.Draw()
    pad_top.cd()
    pad_top.SetLeftMargin(0.18)
    pad_top.SetRightMargin(0.03)
    pad_top.SetBottomMargin(0.02)
    pad_top.SetTopMargin(0.10)
    draw_vpk = style_hist(hist_vpk.Clone(hist_vpk.GetName() + "_draw"), COLOR_VPK, y_title, "")
    draw_new = style_hist(hist_new.Clone(hist_new.GetName() + "_draw"), COLOR_NEW, y_title, "")
    draw_vpk.GetXaxis().SetLabelSize(0)
    x_low, x_high = content_bin_edges(draw_vpk)
    y_max = max(draw_vpk.GetMaximum(), draw_new.GetMaximum())
    draw_vpk.GetXaxis().SetRangeUser(x_low, x_high)
    draw_vpk.GetYaxis().SetRangeUser(0.0, 1.18 * y_max if(y_max > 0) else 1.0)
    draw_vpk.SetTitle(title)
    draw_vpk.Draw("hist")
    draw_new.Draw("hist same")
    pad_bot.cd()
    pad_bot.SetLeftMargin(0.18)
    pad_bot.SetRightMargin(0.03)
    pad_bot.SetTopMargin(0.04)
    pad_bot.SetBottomMargin(0.34)
    graph = make_ratio_graph(hist_new, hist_vpk, ratio_name)
    graph.SetLineColor(COLOR_RATIO)
    graph.SetLineWidth(3)
    graph.SetTitle("")
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle("#rho^{0} new / LUND VPK")
    graph.GetXaxis().SetTitleSize(0.11)
    graph.GetYaxis().SetTitleSize(0.08)
    graph.GetXaxis().SetLabelSize(0.09)
    graph.GetYaxis().SetLabelSize(0.08)
    graph.GetXaxis().SetTitleOffset(1.20)
    graph.GetYaxis().SetTitleOffset(1.05)
    graph.GetXaxis().SetRangeUser(x_low, x_high)
    if(graph.GetN() > 0):
        y_values = [graph.GetY()[point] for point in range(graph.GetN())]
        y_low = min(0.0, min(y_values) * 0.9)
        y_high = max(1.2, max(y_values) * 1.15)
        graph.GetYaxis().SetRangeUser(y_low, y_high)
    graph.Draw("AL")
    line = ROOT.TLine(x_low, 1.0, x_high, 1.0)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kGray + 2)
    line.Draw("same")
    pad_leg.cd()
    legend, text = draw_legend_pad(
        pad_leg,
        [(draw_vpk, "LUND VPK"), (draw_new, "#rho^{0} new")],
        ["No experimental data", "Ratio uses bins with", "nonzero LUND VPK yield"],
    )
    hold(canvas, pad_top, pad_bot, pad_leg, draw_vpk, draw_new, graph, line, legend, text)
    save_canvas(canvas, path)


def draw_phi_bin(path, title, curves, note_lines):
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas(os.path.basename(path).replace(".", "_"), title, 1400, 900)
    canvas.SetFillColor(ROOT.kWhite)
    pad_plot = ROOT.TPad("plot_%s" % canvas.GetName(), "", 0.0, 0.0, 0.74, 1.0)
    pad_leg  = ROOT.TPad("leg_%s" % canvas.GetName(), "", 0.74, 0.0, 1.0, 1.0)
    pad_plot.SetFillColor(ROOT.kWhite)
    pad_leg.SetFillColor(ROOT.kWhite)
    pad_plot.Draw()
    pad_leg.Draw()
    pad_plot.cd()
    pad_plot.SetLeftMargin(0.16)
    pad_plot.SetRightMargin(0.04)
    pad_plot.SetBottomMargin(0.14)
    pad_plot.SetTopMargin(0.12)
    drawn = []
    y_max = 0.0
    y_min = 0.0
    for hist, color, label in curves:
        styled = style_hist(hist.Clone(hist.GetName() + "_bin"), color, "Reconstructed yield", "#phi_{h} (deg)")
        y_max = max(y_max, styled.GetMaximum())
        y_min = min(y_min, styled.GetMinimum())
        drawn.append((styled, label))
    drawn[0][0].SetTitle(title)
    drawn[0][0].GetYaxis().SetRangeUser(min(0.0, 1.15 * y_min), 1.2 * y_max if(y_max > 0) else 1.0)
    drawn[0][0].Draw("hist")
    for styled, label in drawn[1:]:
        styled.Draw("hist same")
    legend, text = draw_legend_pad(pad_leg, drawn, note_lines)
    hold(canvas, pad_plot, pad_leg, legend, text)
    for styled, label in drawn:
        hold(canvas, styled)
    save_canvas(canvas, path)


def draw_both_contamination(path, title, x_title, data_hist, mc_vpk, mc_new):
    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas(os.path.basename(path).replace(".", "_"), title, 1500, 900)
    canvas.SetFillColor(ROOT.kWhite)
    pad_plot = ROOT.TPad("plot_%s" % canvas.GetName(), "", 0.0, 0.0, 0.76, 1.0)
    pad_leg  = ROOT.TPad("leg_%s" % canvas.GetName(), "", 0.76, 0.0, 1.0, 1.0)
    pad_plot.SetFillColor(ROOT.kWhite)
    pad_leg.SetFillColor(ROOT.kWhite)
    pad_plot.Draw()
    pad_leg.Draw()
    pad_plot.cd()
    pad_plot.SetLeftMargin(0.14)
    pad_plot.SetRightMargin(0.04)
    pad_plot.SetBottomMargin(0.14)
    pad_plot.SetTopMargin(0.12)
    graph_vpk = make_graph(data_hist, mc_vpk, data_hist.GetName() + "_both_vpk")
    graph_new = make_graph(data_hist, mc_new, data_hist.GetName() + "_both_new")
    graph_vpk.SetLineColor(COLOR_VPK)
    graph_new.SetLineColor(COLOR_NEW)
    graph_vpk.SetLineWidth(3)
    graph_new.SetLineWidth(3)
    graph_vpk.SetTitle(title)
    graph_vpk.GetXaxis().SetTitle(x_title)
    graph_vpk.GetYaxis().SetTitle("Contamination (%)")
    graph_vpk.GetXaxis().SetTitleSize(0.05)
    graph_vpk.GetYaxis().SetTitleSize(0.05)
    graph_vpk.GetXaxis().SetLabelSize(0.045)
    graph_vpk.GetYaxis().SetLabelSize(0.045)
    graph_vpk.GetYaxis().SetTitleOffset(1.25)
    x_low, x_high = content_bin_edges(data_hist)
    graph_vpk.GetXaxis().SetRangeUser(x_low, x_high)
    y_values = []
    for graph in [graph_vpk, graph_new]:
        for point in range(graph.GetN()):
            y_values.append(graph.GetY()[point])
    y_high = max(y_values) * 1.2 if(len(y_values) > 0) else 1.0
    graph_vpk.GetYaxis().SetRangeUser(0.0, y_high)
    graph_vpk.Draw("AL")
    graph_new.Draw("L same")
    legend, texts = draw_legend_pad(pad_leg, [(graph_vpk, "LUND VPK"), (graph_new, "#rho^{0} new")], ["100 #times MC / data", "Same reconstructed", "data in every bin"])
    hold(canvas, pad_plot, pad_leg, graph_vpk, graph_new, legend)
    for text in texts:
        hold(canvas, text)
    save_canvas(canvas, path)


def unit_clone(hist, name):
    clone = hist.Clone(name)
    clone.SetDirectory(0)
    integral = clone.Integral()
    if(integral > 0):
        clone.Scale(1.0 / integral)
    return clone


def write_csv(path, fieldnames, rows):
    handle = open(path, "w", newline="")
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    handle.close()


def fmt_num(value, digits=4):
    if(value is None):
        return ""
    return ("%." + str(digits) + "f") % value


def write_tables(output_dir, rows, per_sample, kinematic_rows, mc_rows, meta):
    table_dir = os.path.join(output_dir, "tables")
    os.makedirs(table_dir, exist_ok=True)
    per_bin_fields = ["q2y_bin", "z_pT_bin", "data_yield", "lundvpk_yield", "lundvpk_contamination_percent", "rho0_new_yield", "rho0_new_contamination_percent", "difference_percentage_points"]
    per_bin_out = []
    for row in rows:
        per_bin_out.append({
            "q2y_bin": row["q2y"],
            "z_pT_bin": row["zpt"],
            "data_yield": "%.6f" % row["data_yield"],
            "lundvpk_yield": "%.6f" % row["lundvpk_yield"],
            "lundvpk_contamination_percent": fmt_num(row["lundvpk_percent"], 6),
            "rho0_new_yield": "%.6f" % row["rho0_new_yield"],
            "rho0_new_contamination_percent": fmt_num(row["rho0_new_percent"], 6),
            "difference_percentage_points": fmt_num(row["difference_percentage_points"], 6),
        })
    write_csv(os.path.join(table_dir, "per_bin_contamination.csv"), per_bin_fields, per_bin_out)
    text_handle = open(os.path.join(table_dir, "per_bin_contamination.txt"), "w")
    text_handle.write("Retained Q2-y and z-PT bins. Contamination is 100 * weighted reconstructed rho0 MC / experimental data before subtraction.\n")
    text_handle.write("difference_percentage_points is rho0 new minus LUND VPK.\n")
    text_handle.write("The unweighted mean of these percentages is not the integrated yield ratio.\n\n")
    text_handle.write("%6s %6s %16s %16s %14s %16s %14s %14s\n" % ("Q2-y", "z-PT", "Data yield", "LUND VPK", "LUND VPK %", "rho0 new", "rho0 new %", "Difference pp"))
    for row in rows:
        text_handle.write("%6d %6d %16.3f %16.3f %14s %16.3f %14s %14s\n" % (
            row["q2y"], row["zpt"], row["data_yield"], row["lundvpk_yield"], fmt_num(row["lundvpk_percent"], 4),
            row["rho0_new_yield"], fmt_num(row["rho0_new_percent"], 4), fmt_num(row["difference_percentage_points"], 4),
        ))
    text_handle.close()
    kinematic_fields = ["variable", "scope", "bin", "bin_low", "bin_high", "bin_center", "data_yield", "lundvpk_yield", "lundvpk_contamination_percent", "rho0_new_yield", "rho0_new_contamination_percent"]
    kinematic_out = []
    for row in kinematic_rows:
        kinematic_out.append({
            "variable": row["variable"],
            "scope": row["scope"],
            "bin": row["bin"],
            "bin_low": "%.8f" % row["bin_low"],
            "bin_high": "%.8f" % row["bin_high"],
            "bin_center": "%.8f" % row["bin_center"],
            "data_yield": "%.6f" % row["data_yield"],
            "lundvpk_yield": "%.6f" % row["lundvpk_yield"],
            "lundvpk_contamination_percent": fmt_num(row["lundvpk_percent"], 6),
            "rho0_new_yield": "%.6f" % row["rho0_new_yield"],
            "rho0_new_contamination_percent": fmt_num(row["rho0_new_percent"], 6),
        })
    write_csv(os.path.join(table_dir, "kinematic_contamination.csv"), kinematic_fields, kinematic_out)
    mc_fields = ["variable", "scope", "bin", "bin_low", "bin_high", "bin_center", "lundvpk_yield", "rho0_new_yield", "lundvpk_unit_area", "rho0_new_unit_area", "yield_ratio_rho0_new_over_lundvpk", "unit_area_ratio_rho0_new_over_lundvpk"]
    write_csv(os.path.join(table_dir, "mc_comparison.csv"), mc_fields, mc_rows)
    summary_rows = []
    for token in SAMPLE_ORDER:
        summary = per_sample[token]["summary"]
        summary_rows.append({"quantity": "n_rho", "sample": token, "value": "%.12f" % SAMPLE_INFO[token]["n_rho"], "q2y_bin": "", "z_pT_bin": "", "data_yield": "", "mc_yield": ""})
        summary_rows.append({"quantity": "preweighted", "sample": token, "value": str(meta[token]["preweighted"]), "q2y_bin": "", "z_pT_bin": "", "data_yield": "", "mc_yield": ""})
        summary_rows.append({"quantity": "raw_count_from_integral", "sample": token, "value": "%.6f" % meta[token]["implied_raw"], "q2y_bin": "", "z_pT_bin": "", "data_yield": "", "mc_yield": ""})
        summary_rows.append({"quantity": "scale_applied_in_this_script", "sample": token, "value": "%.12f" % meta[token]["scale"], "q2y_bin": "", "z_pT_bin": "", "data_yield": "", "mc_yield": ""})
        summary_rows.append({"quantity": "integrated_contamination_percent", "sample": token, "value": "%.6f" % summary["integrated_percent"], "q2y_bin": "", "z_pT_bin": "", "data_yield": "%.6f" % summary["data_sum"], "mc_yield": "%.6f" % summary["mc_sum"]})
        summary_rows.append({"quantity": "unweighted_mean_percent", "sample": token, "value": "%.6f" % summary["unweighted_mean_percent"], "q2y_bin": "", "z_pT_bin": "", "data_yield": "", "mc_yield": ""})
        for label in ["minimum", "maximum", "closest_to_mean"]:
            record = summary[label]
            summary_rows.append({"quantity": label, "sample": token, "value": "%.6f" % record["percent"], "q2y_bin": record["q2y"], "z_pT_bin": record["zpt"], "data_yield": "%.6f" % record["data_yield"], "mc_yield": "%.6f" % record["mc_yield"]})
        for q2y_bin, zpt_bin, role in HISTORICAL_BINS:
            record = lookup_bin(per_sample[token]["records"], q2y_bin, zpt_bin)
            summary_rows.append({"quantity": role, "sample": token, "value": fmt_num(record["percent"], 6), "q2y_bin": q2y_bin, "z_pT_bin": zpt_bin, "data_yield": "%.6f" % record["data_yield"], "mc_yield": "%.6f" % record["mc_yield"]})
    write_csv(os.path.join(table_dir, "summary_comparison.csv"), ["quantity", "sample", "value", "q2y_bin", "z_pT_bin", "data_yield", "mc_yield"], summary_rows)
    readable = open(os.path.join(table_dir, "summary_comparison.txt"), "w")
    readable.write("Exclusive rho0 comparison on reconstructed cut_Complete_SIDIS yields.\n")
    readable.write("Integrated contamination = 100 * sum(MC) / sum(data) over retained bins.\n")
    readable.write("Unweighted mean = mean of the per-bin percentages. It is not the integrated ratio.\n")
    readable.write("Retained bins: %d\n\n" % per_sample["lundvpk"]["summary"]["n_bins"])
    readable.write("%28s %24s %24s\n" % ("Quantity", "LUND VPK", "rho0 new"))
    pairs = [
        ("Normalization factor", "%.6f" % SAMPLE_INFO["lundvpk"]["n_rho"], "%.12f" % SAMPLE_INFO["rho0_new"]["n_rho"]),
        ("Already weighted", str(meta["lundvpk"]["preweighted"]), str(meta["rho0_new"]["preweighted"])),
        ("Raw count check", "%.1f" % meta["lundvpk"]["implied_raw"], "%.1f" % meta["rho0_new"]["implied_raw"]),
        ("Scale applied here", "%.6f" % meta["lundvpk"]["scale"], "%.6f" % meta["rho0_new"]["scale"]),
        ("Integrated contamination %", "%.4f" % per_sample["lundvpk"]["summary"]["integrated_percent"], "%.4f" % per_sample["rho0_new"]["summary"]["integrated_percent"]),
        ("Unweighted mean %", "%.4f" % per_sample["lundvpk"]["summary"]["unweighted_mean_percent"], "%.4f" % per_sample["rho0_new"]["summary"]["unweighted_mean_percent"]),
    ]
    for label, left, right in pairs:
        readable.write("%28s %24s %24s\n" % (label, left, right))
    readable.write("\nSelected bins\n")
    for token in SAMPLE_ORDER:
        summary = per_sample[token]["summary"]
        readable.write("\n%s\n" % token)
        for label in ["closest_to_mean", "maximum", "minimum"]:
            record = summary[label]
            readable.write("  %16s  Q2-y %d  z-PT %d  contamination %8.4f%%  data %.3f  MC %.3f\n" % (label, record["q2y"], record["zpt"], record["percent"], record["data_yield"], record["mc_yield"]))
        for q2y_bin, zpt_bin, role in HISTORICAL_BINS:
            record = lookup_bin(per_sample[token]["records"], q2y_bin, zpt_bin)
            readable.write("  %16s  Q2-y %d  z-PT %d  contamination %8.4f%%  data %.3f  MC %.3f\n" % (role, q2y_bin, zpt_bin, record["percent"], record["data_yield"], record["mc_yield"]))
    readable.close()
    return os.path.join(table_dir, "summary.json")


def projection_note(data_hist, mc_hist):
    data_sum = data_hist.Integral()
    mc_sum   = mc_hist.Integral()
    if(data_sum <= 0):
        return "Integrated: undefined"
    return "Projection integral: %.2f%%" % (100.0 * mc_sum / data_sum)


def selected_bin_list(per_sample):
    chosen = {}
    for q2y_bin, zpt_bin, role in HISTORICAL_BINS:
        chosen.setdefault((q2y_bin, zpt_bin), []).append(role)
    for token in SAMPLE_ORDER:
        summary = per_sample[token]["summary"]
        for label in ["closest_to_mean", "maximum", "minimum"]:
            record = summary[label]
            key = (record["q2y"], record["zpt"])
            role = "%s_%s" % (token, label)
            chosen.setdefault(key, []).append(role)
    return chosen


def build_slide_figures(output_dir, sample_pack, phi_sums, per_sample, kinematic_hists):
    figure_dir = os.path.join(output_dir, "figures", "slides")
    os.makedirs(figure_dir, exist_ok=True)
    for spec in KINEMATIC_SPECS:
        x_title = axis_caption(spec["label"], spec["unit"])
        for token in SAMPLE_ORDER:
            data_hist = kinematic_hists[spec["key"]]["data"]
            mc_hist   = kinematic_hists[spec["key"]][token]
            subtracted = data_hist.Clone("%s_%s_sub" % (spec["key"], token))
            subtracted.SetDirectory(0)
            subtracted.Add(mc_hist, -1.0)
            note = [projection_note(data_hist, mc_hist), "Factor already in the MC", "No second scale"]
            draw_data_overlay(
                os.path.join(figure_dir, "data_%s_%s.pdf" % (token, spec["file"])),
                "%s versus data: %s" % (SAMPLE_INFO[token]["root_name"], spec["label"]),
                x_title,
                data_hist,
                mc_hist,
                subtracted,
                "Normalized exclusive #rho^{0}",
                note,
            )
        draw_mc_overlay(
            os.path.join(figure_dir, "mc_unit_%s.pdf" % spec["file"]),
            "Unit-area exclusive #rho^{0} shapes: %s" % spec["label"],
            x_title,
            "Unit area",
            kinematic_hists[spec["key"]]["lundvpk_unit"],
            kinematic_hists[spec["key"]]["rho0_new_unit"],
            "unit_ratio_%s" % spec["key"],
        )
        draw_mc_overlay(
            os.path.join(figure_dir, "mc_yield_%s.pdf" % spec["file"]),
            "Normalized exclusive #rho^{0} yields: %s" % spec["label"],
            x_title,
            "Weighted reconstructed yield",
            kinematic_hists[spec["key"]]["lundvpk"],
            kinematic_hists[spec["key"]]["rho0_new"],
            "yield_ratio_%s" % spec["key"],
        )
    for token in SAMPLE_ORDER:
        data_hist = phi_sums["data"]
        mc_hist   = phi_sums[token]
        subtracted = data_hist.Clone("phi_sub_%s" % token)
        subtracted.SetDirectory(0)
        subtracted.Add(mc_hist, -1.0)
        summary = per_sample[token]["summary"]
        note = [
            SAMPLE_INFO[token]["root_name"],
            "452-bin #phi_{h} sum",
            "Integrated: %.2f%%" % summary["integrated_percent"],
            "Unweighted mean: %.2f%%" % summary["unweighted_mean_percent"],
        ]
        draw_data_overlay(
            os.path.join(figure_dir, "data_%s_phi.pdf" % token),
            "%s versus data: #phi_{h}" % SAMPLE_INFO[token]["root_name"],
            "#phi_{h} (deg)",
            data_hist,
            mc_hist,
            subtracted,
            "Normalized exclusive #rho^{0}",
            note,
        )
    draw_both_contamination(os.path.join(figure_dir, "contam_both_phi.pdf"), "Contamination versus #phi_{h}", "#phi_{h} (deg)", phi_sums["data"], phi_sums["lundvpk"], phi_sums["rho0_new"])
    for spec in KINEMATIC_SPECS:
        draw_both_contamination(
            os.path.join(figure_dir, "contam_both_%s.pdf" % spec["file"]),
            "Contamination versus %s" % spec["label"],
            axis_caption(spec["label"], spec["unit"]),
            kinematic_hists[spec["key"]]["data"],
            kinematic_hists[spec["key"]]["lundvpk"],
            kinematic_hists[spec["key"]]["rho0_new"],
        )
    draw_mc_overlay(os.path.join(figure_dir, "mc_unit_phi.pdf"), "Unit-area exclusive #rho^{0} shapes: #phi_{h}", "#phi_{h} (deg)", "Unit area", unit_clone(phi_sums["lundvpk"], "phi_unit_lundvpk"), unit_clone(phi_sums["rho0_new"], "phi_unit_rho0_new"), "unit_ratio_phi")
    draw_mc_overlay(os.path.join(figure_dir, "mc_yield_phi.pdf"), "Normalized exclusive #rho^{0} yields: #phi_{h}", "#phi_{h} (deg)", "Weighted reconstructed yield", phi_sums["lundvpk"], phi_sums["rho0_new"], "yield_ratio_phi")
    draw_args = DrawArgs("lundvpk", "", "", False)
    chosen = selected_bin_list(per_sample)
    for (q2y_bin, zpt_bin), roles in chosen.items():
        slices = {}
        slices["data"] = slice_phi(draw_args, sample_pack["lundvpk"]["projections"]["data_(phi_t)_(Q2_y_z_pT_4D_Bins)"], q2y_bin, zpt_bin, "showdata")
        for token in SAMPLE_ORDER:
            slices[token] = slice_phi(draw_args, sample_pack[token]["projections"]["(phi_t)_(Q2_y_z_pT_4D_Bins)"], q2y_bin, zpt_bin, "show%s" % token)
        for token in SAMPLE_ORDER:
            record = lookup_bin(per_sample[token]["records"], q2y_bin, zpt_bin)
            subtracted = slices["data"].Clone("show_sub_%s_%d_%d" % (token, q2y_bin, zpt_bin))
            subtracted.SetDirectory(0)
            subtracted.Add(slices[token], -1.0)
            note = [
                "Q^{2}-y bin %d" % q2y_bin,
                "z-P_{T} bin %d" % zpt_bin,
                "Contamination: %.2f%%" % record["percent"],
                "Data yield: %.0f" % record["data_yield"],
                "MC yield: %.0f" % record["mc_yield"],
            ]
            draw_phi_bin(
                os.path.join(figure_dir, "phi_%s_Q2y%d_zPT%d.pdf" % (token, q2y_bin, zpt_bin)),
                "%s: Q^{2}-y %d, z-P_{T} %d" % (SAMPLE_INFO[token]["root_name"], q2y_bin, zpt_bin),
                [(slices["data"], COLOR_DATA, "Data before subtraction"), (slices[token], COLOR_MC, "Normalized exclusive #rho^{0}"), (subtracted, COLOR_SUB, "Data after subtraction")],
                note,
            )
        record_vpk = lookup_bin(per_sample["lundvpk"]["records"], q2y_bin, zpt_bin)
        record_new = lookup_bin(per_sample["rho0_new"]["records"], q2y_bin, zpt_bin)
        both_note = [
            "Q^{2}-y bin %d" % q2y_bin,
            "z-P_{T} bin %d" % zpt_bin,
            "LUND VPK: %.2f%%" % record_vpk["percent"],
            "#rho^{0} new: %.2f%%" % record_new["percent"],
            "Difference: %+.2f pp" % (record_new["percent"] - record_vpk["percent"]),
        ]
        draw_phi_bin(
            os.path.join(figure_dir, "phi_both_Q2y%d_zPT%d.pdf" % (q2y_bin, zpt_bin)),
            "Both exclusive #rho^{0} models: Q^{2}-y %d, z-P_{T} %d" % (q2y_bin, zpt_bin),
            [(slices["data"], COLOR_DATA, "Data before subtraction"), (slices["lundvpk"], COLOR_VPK, "LUND VPK"), (slices["rho0_new"], COLOR_NEW, "#rho^{0} new")],
            both_note,
        )
    return chosen


def mc_numeric_rows(variable_key, scope, hist_vpk, hist_new, unit_vpk, unit_new):
    rows = []
    for bin_index in range(1, hist_vpk.GetNbinsX() + 1):
        vpk_yield = hist_vpk.GetBinContent(bin_index)
        new_yield = hist_new.GetBinContent(bin_index)
        vpk_unit  = unit_vpk.GetBinContent(bin_index)
        new_unit  = unit_new.GetBinContent(bin_index)
        if(vpk_yield > 0):
            yield_ratio = new_yield / vpk_yield
        else:
            yield_ratio = ""
        if(vpk_unit > 0):
            unit_ratio = new_unit / vpk_unit
        else:
            unit_ratio = ""
        rows.append({
            "variable": variable_key,
            "scope": scope,
            "bin": bin_index,
            "bin_low": "%.8f" % hist_vpk.GetXaxis().GetBinLowEdge(bin_index),
            "bin_high": "%.8f" % hist_vpk.GetXaxis().GetBinUpEdge(bin_index),
            "bin_center": "%.8f" % hist_vpk.GetXaxis().GetBinCenter(bin_index),
            "lundvpk_yield": "%.8f" % vpk_yield,
            "rho0_new_yield": "%.8f" % new_yield,
            "lundvpk_unit_area": "%.8e" % vpk_unit,
            "rho0_new_unit_area": "%.8e" % new_unit,
            "yield_ratio_rho0_new_over_lundvpk": "" if(yield_ratio == "") else "%.8f" % yield_ratio,
            "unit_area_ratio_rho0_new_over_lundvpk": "" if(unit_ratio == "") else "%.8f" % unit_ratio,
        })
    return rows


def run_established(output_dir, sample_pack):
    for token in SAMPLE_ORDER:
        destination = os.path.join(output_dir, "figures", "established", token)
        os.makedirs(destination, exist_ok=True)
        previous = os.getcwd()
        os.chdir(destination)
        draw_args = DrawArgs(token, SAMPLE_INFO[token]["suffix"], SAMPLE_INFO[token]["root_name"], False)
        try:
            print("established diagnostics for %s in %s" % (token, destination))
            phi_h_1D_Compare_in_z_pT_Images_Together(sample_pack[token]["drawer_dict"], draw_args, Comparison_Type="In_Data", stage_name=STAGE_NAME, Draw_Type="data_scale")
            for pair in ["(Q2)_(y)", "(Q2)_(xB)", "(z)_(pT)"]:
                Other_1D_Kinematic_Comparison_Images(draw_args, sample_pack[token]["drawer_dict"], Vars_Input=pair, Comparison_Type="In_Data", stage_name=STAGE_NAME, Draw_Type="data_scale")
        finally:
            os.chdir(previous)


def json_record(record):
    if(record is None):
        return None
    return {"q2y": record["q2y"], "zpt": record["zpt"], "percent": record["percent"], "data_yield": record["data_yield"], "mc_yield": record["mc_yield"]}


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("loading %s" % args.file2)
    data_projections, sample_pack = load_comparisons(args.file2)
    if(args.established_only):
        run_established(args.output_dir, sample_pack)
        print("established diagnostics are in %s" % args.output_dir)
        return
    bins = retained_bins()
    print("retained bins from skip_condition_z_pT_bins: %d" % len(bins))
    quiet = DrawArgs("lundvpk", "", "", args.verbose)
    rows, per_sample, phi_sums, missing = collect_bin_table(quiet, data_projections["(phi_t)_(Q2_y_z_pT_4D_Bins)"], sample_pack, bins)
    kinematic_hists = {}
    kinematic_rows  = []
    mc_rows         = []
    for spec in KINEMATIC_SPECS:
        data_1d = project_1d(data_projections[spec["pair"]], spec["axis"], "data_%s" % spec["key"])
        kinematic_hists[spec["key"]] = {"data": data_1d}
        mc_for_rows = {}
        for token in SAMPLE_ORDER:
            mc_1d = project_1d(sample_pack[token]["projections"][spec["pair"]], spec["axis"], "%s_%s" % (token, spec["key"]))
            kinematic_hists[spec["key"]][token] = mc_1d
            mc_for_rows[token] = mc_1d
        kinematic_hists[spec["key"]]["lundvpk_unit"] = unit_clone(kinematic_hists[spec["key"]]["lundvpk"], "unit_lundvpk_%s" % spec["key"])
        kinematic_hists[spec["key"]]["rho0_new_unit"] = unit_clone(kinematic_hists[spec["key"]]["rho0_new"], "unit_rho0_new_%s" % spec["key"])
        kinematic_rows.extend(rows_from_histograms(spec["key"], data_1d, mc_for_rows, "established_Q2y_projection"))
        mc_rows.extend(mc_numeric_rows(spec["key"], "established_Q2y_projection", kinematic_hists[spec["key"]]["lundvpk"], kinematic_hists[spec["key"]]["rho0_new"], kinematic_hists[spec["key"]]["lundvpk_unit"], kinematic_hists[spec["key"]]["rho0_new_unit"]))
    phi_unit_vpk = unit_clone(phi_sums["lundvpk"], "phi_rows_unit_vpk")
    phi_unit_new = unit_clone(phi_sums["rho0_new"], "phi_rows_unit_new")
    kinematic_rows.extend(rows_from_histograms("phi_h", phi_sums["data"], {"lundvpk": phi_sums["lundvpk"], "rho0_new": phi_sums["rho0_new"]}, "retained_452_bins"))
    mc_rows.extend(mc_numeric_rows("phi_h", "retained_452_bins", phi_sums["lundvpk"], phi_sums["rho0_new"], phi_unit_vpk, phi_unit_new))
    meta = {}
    for token in SAMPLE_ORDER:
        meta[token] = {"preweighted": sample_pack[token]["preweighted"], "implied_raw": sample_pack[token]["implied_raw"], "scale": sample_pack[token]["scale"], "phi_integral": sample_pack[token]["phi_integral"]}
    json_path = write_tables(args.output_dir, rows, per_sample, kinematic_rows, mc_rows, meta)
    print("drawing slide figures")
    chosen = build_slide_figures(args.output_dir, sample_pack, phi_sums, per_sample, kinematic_hists)
    ranked = sorted([row for row in rows if(row["difference_percentage_points"] is not None)], key=lambda row: abs(row["difference_percentage_points"]), reverse=True)
    payload = {
        "root_file": args.file2,
        "n_retained": len(rows),
        "n_missing_slices": len(missing),
        "alpha_SIDIS_used": False,
        "samples": {},
        "largest_abs_differences": [],
        "selected_bins": {},
    }
    for token in SAMPLE_ORDER:
        summary = per_sample[token]["summary"]
        historical = {}
        for q2y_bin, zpt_bin, role in HISTORICAL_BINS:
            historical[role] = json_record(lookup_bin(per_sample[token]["records"], q2y_bin, zpt_bin))
        payload["samples"][token] = {
            "n_rho": SAMPLE_INFO[token]["n_rho"],
            "preweighted": sample_pack[token]["preweighted"],
            "scale_applied_here": sample_pack[token]["scale"],
            "implied_raw": sample_pack[token]["implied_raw"],
            "full_phi_integral": sample_pack[token]["phi_integral"],
            "full_phi_contamination_percent": 100.0 * sample_pack[token]["phi_integral"] / data_projections["(phi_t)_(Q2_y_z_pT_4D_Bins)"].Integral(),
            "integrated_percent": summary["integrated_percent"],
            "unweighted_mean_percent": summary["unweighted_mean_percent"],
            "data_sum": summary["data_sum"],
            "mc_sum": summary["mc_sum"],
            "minimum": json_record(summary["minimum"]),
            "maximum": json_record(summary["maximum"]),
            "closest_to_mean": json_record(summary["closest_to_mean"]),
            "historical": historical,
            "n_positive_data": summary["n_positive_data"],
        }
    for row in ranked[:15]:
        payload["largest_abs_differences"].append({
            "q2y": row["q2y"],
            "zpt": row["zpt"],
            "lundvpk_percent": row["lundvpk_percent"],
            "rho0_new_percent": row["rho0_new_percent"],
            "difference_percentage_points": row["difference_percentage_points"],
            "data_yield": row["data_yield"],
        })
    for (q2y_bin, zpt_bin), roles in chosen.items():
        payload["selected_bins"]["%d_%d" % (q2y_bin, zpt_bin)] = roles
    handle = open(json_path, "w")
    json.dump(payload, handle, indent=2)
    handle.write("\n")
    handle.close()
    print("wrote %s" % json_path)
    for token in SAMPLE_ORDER:
        summary = per_sample[token]["summary"]
        print("%s integrated %.4f%%  unweighted mean %.4f%%  min %.4f%% (%d,%d)  max %.4f%% (%d,%d)" % (
            token, summary["integrated_percent"], summary["unweighted_mean_percent"],
            summary["minimum"]["percent"], summary["minimum"]["q2y"], summary["minimum"]["zpt"],
            summary["maximum"]["percent"], summary["maximum"]["q2y"], summary["maximum"]["zpt"],
        ))
    if(args.established_diagnostics):
        run_established(args.output_dir, sample_pack)
    print("comparison outputs are in %s" % args.output_dir)


if(__name__ == "__main__"):
    main()
