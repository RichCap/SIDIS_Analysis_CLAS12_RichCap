#!/usr/bin/env python3
# Consolidated thesis phi_h figures. One 4x5 Q2-y canvas per family.
# Pad map copied from phi_h_1D_Compare_in_z_pT_Images_Together in
# Histo_Files_ROOT/DataFrames/Get_rho_Normalization_values.py.

import argparse
import json
import math
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

ANALYSIS = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
THESIS   = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis"
if(ANALYSIS not in sys.path):
    sys.path.insert(0, ANALYSIS)

from MyCommonAnalysisFunction_richcap import Canvas_Create, Get_Num_of_z_pT_Rows_and_Columns, skip_condition_z_pT_bins

# Same placement as the exclusive-rho0 all-bins figure. Keys are Q2-y bin numbers.
Q2Y_PAD = {1: 20, 2: 19, 3: 18, 4: 17, 5: 16, 6: 15, 7: 14, 8: 13, 9: 12, 10: 11, 11: 10, 12: 9, 13: 8, 14: 7, 15: 6, 16: 4, 17: 3}
RETAINED = {1: 29, 2: 32, 3: 28, 4: 23, 5: 32, 6: 26, 7: 32, 8: 26, 9: 29, 10: 32, 11: 23, 12: 15, 13: 26, 14: 31, 15: 19, 16: 24, 17: 25}

DEFAULT_3D = os.path.join(ANALYSIS, "SIDIS_Campaign/systematics/systematics_3d_complete_20261029/unfolded/Sys3D_nominal_only_20261030_inherited_Unweighted.root")
DEFAULT_RC = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/Run_Large_Files_For_Iterative_Corrections/Comparison_With_Unfolding/build_EvGen_PerFile_Hists_Runtime_ifarm_rc/merged_outputs/RC_Factors_ifarm_rc.root"
DEFAULT_BC_ROOT = os.path.join(ANALYSIS, "BC_Corrections/Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026.root")
DEFAULT_BC_JSON = os.path.join(ANALYSIS, "BC_Corrections/Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026.json")
DEFAULT_2D = os.path.join(ANALYSIS, "Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_All.root")
FIT_AC = os.path.join(ANALYSIS, "Systematic_Studies/physics_campaign/fits/unweighted/nominal/nominal/fit.json")
FIT_BC = os.path.join(ANALYSIS, "Systematic_Studies/physics_campaign/corrected/unweighted/fit.json")
NORHO_DIR = os.path.join(ANALYSIS, "SIDIS_Campaign/systematics/systematics_3d_complete_20261029/unfolded")
NORHO_REJECTED = os.path.join(NORHO_DIR, "Sys3D_nominal_only_20261030_NoRho0_AccSpline.root")

FAMILIES = [
    "data_rec_gen",
    "unfolded_ac",
    "unfolded_rc",
    "unfolded_bc",
    "evgen_rad_born",
    "rc_factor",
    "bc_subbin",
    "bc_factor",
    "unfolded_ac_norho",
    "unfolded_rc_norho",
    "unfolded_bc_norho",
]
CORRECTED = {
    "unfolded_ac", "unfolded_rc", "unfolded_bc",
    "unfolded_ac_norho", "unfolded_rc_norho", "unfolded_bc_norho",
}
FIT_KEY = {
    "unfolded_ac":       "Fit_Pars_from_3D_Bayesian",
    "unfolded_ac_norho": "Fit_Pars_from_3D_Bayesian",
    "unfolded_rc":       "Fit_Pars_from_3D_RC_Bayesian",
    "unfolded_rc_norho": "Fit_Pars_from_3D_RC_Bayesian",
    "unfolded_bc":       "Fit_Pars_from_3D_BC_RC_Bayesian",
    "unfolded_bc_norho": "Fit_Pars_from_3D_BC_RC_Bayesian",
}
FIT_STAGE = {
    "unfolded_ac": "Bayesian",
    "unfolded_ac_norho": "Bayesian",
    "unfolded_rc": "RC_Bayesian",
    "unfolded_rc_norho": "RC_Bayesian",
    "unfolded_bc": "BC_RC_Bayesian",
    "unfolded_bc_norho": "BC_RC_Bayesian",
}

PDF_NAME = {
    "data_rec_gen":      "Monte_Carlo/Data_MC_Images/phi_h_Data_REC_GEN_All_Q2y.pdf",
    "unfolded_ac":       "Analysis_Procedures/Unfolding_Images/Unfolded_AC_All_Q2y.pdf",
    "unfolded_rc":       "Analysis_Procedures/Unfolding_Images/Unfolded_RC_All_Q2y.pdf",
    "unfolded_bc":       "Analysis_Procedures/Unfolding_Images/Unfolded_BC_All_Q2y.pdf",
    "evgen_rad_born":    "Analysis_Procedures/Unfolding_Images/EvGen_Rad_vs_Born_All_Q2y.pdf",
    "rc_factor":         "Analysis_Procedures/Unfolding_Images/RC_Factor_All_Q2y.pdf",
    "bc_subbin":         "Analysis_Procedures/Unfolding_Images/BC_Subbin_All_Q2y.pdf",
    "bc_factor":         "Analysis_Procedures/Unfolding_Images/BC_Factor_All_Q2y.pdf",
    "unfolded_ac_norho": "Analysis_Procedures/Unfolding_Images/Without_rho0/Unfolded_AC_NORHO_All_Q2y.pdf",
    "unfolded_rc_norho": "Analysis_Procedures/Unfolding_Images/Without_rho0/Unfolded_RC_NORHO_All_Q2y.pdf",
    "unfolded_bc_norho": "Analysis_Procedures/Unfolding_Images/Without_rho0/Unfolded_BC_NORHO_All_Q2y.pdf",
}

CLONE_I = 0
OPEN_FILES = {}


def parse_args():
    parser = argparse.ArgumentParser(description="Draw the eleven consolidated phi_h figures.")
    parser.add_argument("-a", "--all_families", action="store_true", help="Draw every family. This is the default when --family is omitted.")
    parser.add_argument("-f", "--family", action="append", default=[], choices=FAMILIES, help="Family to draw. Repeat for more than one.")
    parser.add_argument("-o", "--output_dir", default="", help="Directory for every PDF. Empty uses the thesis image directories.")
    parser.add_argument("-u3d", "--unfolded_3d", default=DEFAULT_3D)
    parser.add_argument("-u3d_norho", "--unfolded_3d_norho", default="")
    parser.add_argument("-rcf", "--rc_factors", default=DEFAULT_RC)
    parser.add_argument("-bcr", "--bc_root", default=DEFAULT_BC_ROOT)
    parser.add_argument("-bcj", "--bc_json", default=DEFAULT_BC_JSON)
    parser.add_argument("-fbk", "--fallback_2d", default=DEFAULT_2D)
    parser.add_argument("-fit", "--fit_source", default="")
    parser.add_argument("-root_data_rec_gen", "--root_data_rec_gen", default="")
    parser.add_argument("-root_evgen_rad_born", "--root_evgen_rad_born", default="")
    parser.add_argument("-root_rc_factor", "--root_rc_factor", default="")
    parser.add_argument("-root_unfolded_ac", "--root_unfolded_ac", default="")
    parser.add_argument("-root_unfolded_rc", "--root_unfolded_rc", default="")
    parser.add_argument("-root_unfolded_bc", "--root_unfolded_bc", default="")
    parser.add_argument("-root_unfolded_ac_norho", "--root_unfolded_ac_norho", default="")
    parser.add_argument("-root_unfolded_rc_norho", "--root_unfolded_rc_norho", default="")
    parser.add_argument("-root_unfolded_bc_norho", "--root_unfolded_bc_norho", default="")
    parser.add_argument("-root_bc_subbin", "--root_bc_subbin", default="")
    parser.add_argument("-json_bc_factor", "--json_bc_factor", default="")
    parser.add_argument("-json_bc_subbin", "--json_bc_subbin", default="")
    parser.add_argument("-fit_unfolded_ac", "--fit_unfolded_ac", default="")
    parser.add_argument("-fit_unfolded_rc", "--fit_unfolded_rc", default="")
    parser.add_argument("-fit_unfolded_bc", "--fit_unfolded_bc", default="")
    parser.add_argument("-fit_unfolded_ac_norho", "--fit_unfolded_ac_norho", default="")
    parser.add_argument("-fit_unfolded_rc_norho", "--fit_unfolded_rc_norho", default="")
    parser.add_argument("-fit_unfolded_bc_norho", "--fit_unfolded_bc_norho", default="")
    parser.add_argument("-q", "--q2y_bins", nargs="+", default=["1-17"])
    parser.add_argument("-s", "--summary_text", default="")
    parser.add_argument("-n", "--dry_run", action="store_true")
    return parser.parse_args()


def q2y_list(tokens):
    bins = []
    for token in tokens:
        if("-" in str(token)):
            left, right = str(token).split("-", 1)
            bins.extend(range(int(left), int(right) + 1))
        else:
            bins.append(int(token))
    return bins


def first_set(specific, shared):
    if(specific not in ["", None]):
        return specific
    return shared


def open_root(path):
    if(path in OPEN_FILES):
        return OPEN_FILES[path]
    handle = ROOT.TFile.Open(path, "READ")
    if((handle is None) or handle.IsZombie()):
        raise IOError("unreadable ROOT file: %s" % path)
    OPEN_FILES[path] = handle
    return handle


def take(handle, name):
    global CLONE_I
    obj = handle.Get(name)
    if(not obj):
        return None
    CLONE_I += 1
    clone = obj.Clone("%s_draw_%d" % (name.replace("/", "_"), CLONE_I))
    clone.SetDirectory(0)
    return clone


def phi_3d_name(kind, q2y, zpt):
    smear = "Smear" if(kind in ["mdf", "Bayesian", "Background"]) else "''"
    return "(MultiDim_3D_Histo)_(%s)_(SMEAR=%s)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (kind, smear, q2y, zpt)


def rc_name(prefix, q2y, zpt):
    tail = "_(Normalized_Weight)" if(prefix == "(RC_Factor)") else ""
    return "%s_(gdf)_(SMEAR='')_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(phi_t)%s" % (prefix, q2y, zpt, tail)


def shape_norm(hist):
    total = hist.Integral()
    if(total > 0):
        hist.Scale(1.0 / total)
    return hist


def style_hist(hist, color, marker, width=1):
    hist.SetLineColor(color)
    hist.SetMarkerColor(color)
    hist.SetMarkerStyle(marker)
    hist.SetMarkerSize(0.35)
    hist.SetLineWidth(width)
    hist.SetTitle("")
    hist.SetStats(0)
    hist.GetXaxis().SetLabelSize(0.09)
    hist.GetYaxis().SetLabelSize(0.09)
    hist.GetXaxis().SetTitleSize(0.0)
    hist.GetYaxis().SetTitleSize(0.0)
    hist.GetXaxis().SetNdivisions(404)
    hist.GetYaxis().SetNdivisions(404)
    return hist


def apply_bc(hist, q2y, zpt, results):
    for ib in range(1, hist.GetNbinsX() + 1):
        key = "Bin (%s-%s-%s)" % (q2y, zpt, ib)
        entry = results.get(key)
        if(not isinstance(entry, dict)):
            return False
        factor = entry.get("BC_Factor")
        error = entry.get("BC_Factor_Err", 0.0)
        try:
            factor = float(factor)
            error = float(error)
        except (TypeError, ValueError):
            return False
        if((factor != factor) or (factor == 0.0)):
            return False
        content = float(hist.GetBinContent(ib))
        stat = float(hist.GetBinError(ib))
        hist.SetBinContent(ib, content / factor)
        hist.SetBinError(ib, math.sqrt((stat / factor) ** 2 + (content * error / (factor * factor)) ** 2))
    return True


def divide_rc(hist, factor):
    if((factor is None) or (hist.GetNbinsX() != factor.GetNbinsX())):
        return False
    hist.Divide(factor)
    return True


def make_fit(name, pars):
    func = ROOT.TF1(name, "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", 0, 360)
    func.SetParName(0, "A")
    func.SetParName(1, "B")
    func.SetParName(2, "C")
    func.SetParameter(0, float(pars["Fit_Par_A"]))
    func.SetParameter(1, float(pars["Fit_Par_B"]))
    func.SetParameter(2, float(pars["Fit_Par_C"]))
    func.SetLineColor(ROOT.kRed)
    func.SetLineWidth(1)
    func.SetNpx(360)
    return func


def load_fit(path, family):
    if(path in ["", None]):
        return None, "no fit file"
    if(not os.path.isfile(path)):
        return None, "fit file missing: %s" % path
    payload = json.load(open(path))
    key = FIT_KEY[family]
    block = payload.get(key)
    if(not isinstance(block, dict) or (len(block) == 0)):
        return None, "fit file has no %s" % key
    meta = payload.get("Meta_Data_of_Last_Run", {})
    stage = str(meta.get("fit_corrections", ""))
    if((stage not in ["", FIT_STAGE[family]]) and (stage != FIT_STAGE[family])):
        return None, "fit_corrections=%s is not %s" % (stage, FIT_STAGE[family])
    if(meta.get("unfolding_3D") is False):
        return None, "fit is not a 3D unfold fit"
    if(str(meta.get("weight_tag", "")) in ["AccSpline", "Spline", "Acc", "AccJSON", "JSON"]):
        if("norho" not in family):
            return None, "fit weight_tag=%s does not match the unweighted nominal" % meta.get("weight_tag")
    return block, "ok"


def find_norho(explicit):
    if(explicit not in ["", None]):
        return explicit, "override"
    found = []
    if(os.path.isdir(NORHO_DIR)):
        for name in sorted(os.listdir(NORHO_DIR)):
            low = name.lower()
            if((not name.endswith(".root")) or ("norho" not in low and "no_rho" not in low and "nrho0" not in low)):
                continue
            if("unweighted" in low):
                found.append(os.path.join(NORHO_DIR, name))
    if(len(found) == 1):
        return found[0], "found unweighted without-rho unfold"
    note = "not found. %s is AccSpline and is not used as the unweighted without-rho unfold" % NORHO_REJECTED
    return "", note


def retained_bins(q2y):
    rows, cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=q2y)
    kept = []
    for zpt in range(1, int(rows) * int(cols) + 1):
        if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y, Z_PT_BIN=zpt)):
            continue
        kept.append(zpt)
    return kept, int(rows), int(cols)


def save_one_page(canvas, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    canvas.SaveAs(destination)


def pdf_path(args, family):
    relative = PDF_NAME[family]
    if(args.output_dir not in [""]):
        return os.path.join(args.output_dir, os.path.basename(relative))
    return os.path.join(THESIS, relative)


def family_root(args, family):
    specific = getattr(args, "root_%s" % family, "")
    if(family == "data_rec_gen"):
        return first_set(specific, args.unfolded_3d)
    if(family in ["evgen_rad_born", "rc_factor"]):
        return first_set(specific, args.rc_factors)
    if(family in ["bc_subbin", "bc_factor"]):
        return first_set(specific if(family == "bc_subbin") else "", args.bc_root)
    if(family.endswith("_norho")):
        shared, note = find_norho(args.unfolded_3d_norho)
        return first_set(specific, shared), note
    return first_set(specific, args.unfolded_3d)


def family_fit_path(args, family):
    specific = getattr(args, "fit_%s" % family, "")
    if(specific not in ["", None]):
        return specific
    if(args.fit_source not in ["", None]):
        return args.fit_source
    if(family in ["unfolded_ac"]):
        return FIT_AC
    if(family in ["unfolded_bc"]):
        return FIT_BC
    return ""


def family_json(args, family):
    if(family == "bc_factor"):
        return first_set(args.json_bc_factor, args.bc_json)
    if(family == "bc_subbin"):
        return first_set(args.json_bc_subbin, args.bc_json)
    return args.bc_json


def resolve_family(args, family):
    info = {"family": family, "pdf": pdf_path(args, family), "thesis_ready": False, "reason": ""}
    root_result = family_root(args, family)
    if(isinstance(root_result, tuple)):
        root_path, note = root_result
        info["norho_note"] = note
    else:
        root_path = root_result
    info["root"] = root_path
    info["json"] = family_json(args, family) if(family in ["bc_subbin", "bc_factor", "unfolded_bc", "unfolded_bc_norho", "unfolded_rc", "unfolded_rc_norho"]) else ""
    info["fit"] = family_fit_path(args, family) if(family in CORRECTED) else ""
    if(family.endswith("_norho") and (root_path in ["", None])):
        info["reason"] = info.get("norho_note", "without-rho unfold not found")
        return info
    if(not os.path.isfile(root_path)):
        info["reason"] = "ROOT input missing: %s" % root_path
        return info
    if(family in CORRECTED):
        block, note = load_fit(info["fit"], family)
        info["fit_note"] = note
        if(block is None):
            info["reason"] = note
            return info
        info["fit_block"] = block
        if((family in ["unfolded_ac", "unfolded_bc"]) and (args.unfolded_3d != DEFAULT_3D) and (getattr(args, "fit_%s" % family, "") in ["", None]) and (args.fit_source in ["", None])):
            info["reason"] = "default fit belongs to the default unweighted file; pass a fit override with this ROOT override"
            info["fit_block"] = None
            return info
    if(family in ["unfolded_rc", "unfolded_bc", "unfolded_rc_norho", "unfolded_bc_norho"]):
        if(not os.path.isfile(args.rc_factors)):
            info["reason"] = "RC file missing"
            return info
    if(family in ["unfolded_bc", "unfolded_bc_norho"]):
        if(not os.path.isfile(info["json"] if(info["json"]) else args.bc_json)):
            info["reason"] = "BC JSON missing"
            return info
    if(family in ["bc_subbin", "bc_factor"]):
        json_path = family_json(args, family)
        info["json"] = json_path
        if(not os.path.isfile(json_path)):
            info["reason"] = "BC JSON missing: %s" % json_path
            return info
    info["thesis_ready"] = True
    info["reason"] = "ok"
    return info


def room_for_labels(pad, top=0.18):
    pad.SetLeftMargin(0.20)
    pad.SetRightMargin(0.02)
    pad.SetBottomMargin(0.11)
    pad.SetTopMargin(top)


def draw_bin_label(pad, q2y, zpt, alive, text_size=0.065):
    pad.cd()
    label = ROOT.TPaveText(0.02, 1.0 - pad.GetTopMargin(), 0.98, 0.998, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.SetTextFont(42)
    label.SetTextAlign(22)
    label.SetTextSize(text_size)
    if(str(zpt) in ["All", "all"]):
        label.AddText("Q^{2}-y bin %s - z-P_{T} All" % q2y)
    else:
        label.AddText("Q^{2}-y bin %s - z-P_{T} bin %s" % (q2y, zpt))
    label.Draw()
    alive.append(label)


def draw_stack(pad, hists, colors, markers, legend_entries, fit_func, alive, q2y=None, zpt=None, top=0.18, label_size=0.065):
    pad.cd()
    ROOT.gStyle.SetOptTitle(0)
    room_for_labels(pad, top)
    ymax = 0.0
    styled = []
    for hist, color, marker in zip(hists, colors, markers):
        style_hist(hist, color, marker)
        ymax = max(ymax, hist.GetMaximum())
        styled.append(hist)
        alive.append(hist)
    if(ymax <= 0):
        ymax = 1.0
    first = True
    for hist, kind in zip(styled, legend_entries):
        hist.GetYaxis().SetRangeUser(0.0, ymax * 1.35)
        hist.GetYaxis().SetLabelOffset(0.004)
        hist.GetXaxis().SetLabelOffset(0.004)
        hist.SetTitle("")
        hist.Draw("HIST E0" if(first) else "HIST E0 SAME")
        first = False
    if(fit_func is not None):
        fit_func.Draw("SAME")
        alive.append(fit_func)
    if(q2y is not None):
        draw_bin_label(pad, q2y, zpt, alive, label_size)
    pad.Modified()


def draw_global_legend(host, entries, alive):
    host.cd()
    legend_pad = ROOT.TPad("global_legend_pad_%s" % id(host), "", 0.012, 0.802, 0.495, 0.988)
    legend_pad.SetFillColor(ROOT.kWhite)
    legend_pad.Draw()
    legend_pad.cd()
    legend = ROOT.TLegend(0.06, 0.10, 0.94, 0.90, "", "NDC")
    legend.SetNColumns(1)
    legend.SetBorderSize(1)
    legend.SetFillStyle(1001)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    legend.SetTextSize(0.10)
    legend.SetMargin(0.14)
    for label, obj, kind in entries:
        legend.AddEntry(obj, label, "lep" if(kind == "points") else "l")
    legend.Draw()
    alive.append(legend_pad)
    alive.append(legend)


def open_q2y_cell(cell, q2y, cols, rows, alive, with_integrated):
    if(with_integrated):
        cell.Divide(2, 1, 0.001, 0.001)
        left = cell.cd(1)
        left.SetPad(0.005, 0.02, 0.28, 0.98)
        right = cell.cd(2)
        right.SetPad(0.28, 0.02, 0.995, 0.98)
        right.Divide(cols, rows, 0.0001, 0.0001)
        alive.append(left)
        alive.append(right)
        return left, right
    cell.cd()
    header = ROOT.TPad("q2y_header_%s_%s" % (q2y, id(cell)), "", 0.01, 0.905, 0.99, 0.985)
    header.SetFillColor(ROOT.kWhite)
    header.Draw()
    header.cd()
    label = ROOT.TPaveText(0.02, 0.02, 0.98, 0.98, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.SetTextFont(42)
    label.SetTextAlign(22)
    label.SetTextSize(0.55)
    label.AddText("Q^{2}-y bin %s" % q2y)
    label.Draw()
    alive.append(header)
    alive.append(label)
    cell.cd()
    grid = ROOT.TPad("q2y_grid_%s_%s" % (q2y, id(cell)), "", 0.005, 0.012, 0.995, 0.895)
    grid.SetFillColor(ROOT.kWhite)
    grid.Draw()
    grid.Divide(cols, rows, 0.0001, 0.0001)
    alive.append(grid)
    return None, grid


def make_host(name, summary_text, alive):
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    if(summary_text not in ["", None]):
        canvas = Canvas_Create(name, 2, 1, int(1800 * 8), int(1500 * 10), 0.01)
        left = canvas.cd(1)
        left.SetPad(0.005, 0.015, 0.27, 0.985)
        box = ROOT.TPaveText(0.08, 0.08, 0.92, 0.92, "NDC")
        box.SetBorderSize(0)
        box.SetFillStyle(0)
        box.AddText(summary_text)
        left.cd()
        box.Draw()
        alive.append(box)
        host = canvas.cd(2)
        host.SetPad(0.28, 0.015, 0.995, 0.9975)
        host.Divide(4, 5, 0.0001, 0.0001)
    else:
        canvas = Canvas_Create(name, 4, 5, 7200, 9000, 0.0001)
        host = canvas
    canvas.SetGrid(0, 0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    alive.append(canvas)
    return canvas, host


def stored_all(info, q2y, rc_file):
    family = info["family"]
    if(family in ["unfolded_rc", "unfolded_bc", "unfolded_rc_norho", "unfolded_bc_norho"]):
        return None
    handle = open_root(info["root"])
    if(family == "data_rec_gen"):
        data = take(handle, phi_3d_name("rdf", q2y, "All"))
        rec  = take(handle, phi_3d_name("mdf", q2y, "All"))
        gen  = take(handle, phi_3d_name("gdf", q2y, "All"))
        if((data is None) or (rec is None) or (gen is None)):
            return None
        return [shape_norm(data), shape_norm(rec), shape_norm(gen)]
    if(family == "evgen_rad_born"):
        rad  = take(handle, rc_name("(EvGen_Rad)", q2y, "All"))
        born = take(handle, rc_name("(EvGenNRad)", q2y, "All"))
        if((rad is None) or (born is None)):
            return None
        return [rad, born]
    if(family == "rc_factor"):
        factor = take(handle, rc_name("(RC_Factor)", q2y, "All"))
        if(factor is None):
            return None
        return [factor]
    hist = take(handle, phi_3d_name("Bayesian", q2y, "All"))
    if(hist is None):
        return None
    return [hist]


def yield_for_bin(info, q2y, zpt, rc_file, bc_results):
    family = info["family"]
    handle = open_root(info["root"])
    if(family == "data_rec_gen"):
        data = take(handle, phi_3d_name("rdf", q2y, zpt))
        rec  = take(handle, phi_3d_name("mdf", q2y, zpt))
        gen  = take(handle, phi_3d_name("gdf", q2y, zpt))
        if((data is None) or (rec is None) or (gen is None)):
            return None
        return [shape_norm(data), shape_norm(rec), shape_norm(gen)]
    if(family == "evgen_rad_born"):
        rad  = take(handle, rc_name("(EvGen_Rad)", q2y, zpt))
        born = take(handle, rc_name("(EvGenNRad)", q2y, zpt))
        if((rad is None) or (born is None)):
            return None
        return [rad, born]
    if(family == "rc_factor"):
        factor = take(handle, rc_name("(RC_Factor)", q2y, zpt))
        if(factor is None):
            return None
        return [factor]
    base_kind = "Bayesian"
    hist = take(handle, phi_3d_name(base_kind, q2y, zpt))
    if(hist is None):
        return None
    if(family in ["unfolded_rc", "unfolded_bc", "unfolded_rc_norho", "unfolded_bc_norho"]):
        factor = take(rc_file, rc_name("(RC_Factor)", q2y, zpt))
        if(not divide_rc(hist, factor)):
            return None
    if(family in ["unfolded_bc", "unfolded_bc_norho"]):
        if(not apply_bc(hist, q2y, zpt, bc_results)):
            return None
    return [hist]


def legend_spec(family):
    if(family == "data_rec_gen"):
        return [("Experimental data", ROOT.kBlue, 20, "points"), ("Reconstructed clasdis", ROOT.kRed, 21, "points"), ("Generated clasdis", ROOT.kGreen + 2, 22, "points")]
    if(family == "evgen_rad_born"):
        return [("Radiated EvGen", ROOT.kRed, 20, "points"), ("Born EvGen", ROOT.kBlue, 21, "points")]
    if(family == "rc_factor"):
        return [("RC factor", ROOT.kBlack, 20, "points")]
    label = "Acceptance Corrected Only"
    if("unfolded_rc" in family):
        label = "AC + RC"
    if("unfolded_bc" in family):
        label = "AC + RC + BC"
    return [(label, ROOT.kGreen + 2, 20, "points")]


def draw_family(args, info, q2y_bins):
    alive = []
    family = info["family"]
    canvas, host = make_host(family, args.summary_text, alive)
    spec = legend_spec(family)
    legend_entries = None
    with_integrated = (family == "data_rec_gen")
    rc_file = open_root(args.rc_factors) if(family in ["unfolded_rc", "unfolded_bc", "unfolded_rc_norho", "unfolded_bc_norho"]) else None
    bc_results = None
    if(family in ["unfolded_bc", "unfolded_bc_norho"]):
        bc_results = json.load(open(args.bc_json))["results"]
    counts = {}
    missing = []
    fit_block = info.get("fit_block")
    for q2y in q2y_bins:
        kept, rows, cols = retained_bins(q2y)
        counts[q2y] = len(kept)
        if(counts[q2y] != RETAINED[q2y]):
            missing.append("retained %s=%s expected %s" % (q2y, counts[q2y], RETAINED[q2y]))
        cell = host.cd(Q2Y_PAD[q2y])
        left, grid = open_q2y_cell(cell, q2y, cols, rows, alive, with_integrated)
        summed = None
        all_hists = stored_all(info, q2y, rc_file) if(with_integrated) else None
        for zpt in kept:
            hists = yield_for_bin(info, q2y, zpt, rc_file, bc_results)
            pad = grid.cd(zpt)
            if(hists is None):
                missing.append("missing %s %s-%s" % (family, q2y, zpt))
                continue
            fit_func = None
            if(fit_block is not None):
                pars = fit_block.get("(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt))
                if(not isinstance(pars, dict)):
                    missing.append("missing fit %s-%s" % (q2y, zpt))
                else:
                    fit_func = make_fit("fit_%s_%s_%s" % (family, q2y, zpt), pars)
            draw_stack(pad, hists, [item[1] for item in spec], [item[2] for item in spec], spec, fit_func, alive, q2y, zpt)
            if(with_integrated):
                if(summed is None):
                    summed = hists[0].Clone("all_%s_%s" % (family, q2y))
                    summed.SetDirectory(0)
                else:
                    summed.Add(hists[0])
            if(legend_entries is None):
                legend_entries = []
                for item, obj in zip(spec, hists):
                    legend_entries.append((item[0], obj, item[3]))
                if(fit_func is not None):
                    legend_entries.append(("Fit", fit_func, "hist"))
        if(with_integrated):
            panel = all_hists if(all_hists) else ([summed] if(summed is not None) else [])
            if(panel):
                draw_stack(left, panel, [item[1] for item in spec[:len(panel)]], [item[2] for item in spec[:len(panel)]], spec[:len(panel)], None, alive, q2y, "All", 0.10, 0.055)
                panel[0].SetTitle("")
                panel[0].GetXaxis().SetTitle("#phi_{h}")
                panel[0].GetXaxis().SetTitleSize(0.08)
                panel[0].GetXaxis().SetLabelSize(0.07)
                panel[0].GetYaxis().SetLabelSize(0.07)
    if(legend_entries):
        draw_global_legend(host, legend_entries, alive)
    thesis_ready = (len(missing) == 0)
    destination = info["pdf"]
    if(thesis_ready and (not args.dry_run)):
        save_one_page(canvas, destination)
    elif(not thesis_ready):
        info["reason"] = "; ".join(missing[:8])
    info["thesis_ready"] = thesis_ready
    info["counts"] = counts
    canvas.Clear()
    alive.clear()
    return info


def show_existing_hists(pad, hists, q2y, zpt, alive):
    for hist in hists:
        hist.SetDirectory(0)
    primitives = pad.GetListOfPrimitives()
    if(primitives is not None):
        primitives.Clear("nodelete")
    pad.cd()
    ROOT.gStyle.SetOptTitle(0)
    room_for_labels(pad)
    first = True
    for hist in hists:
        hist.SetTitle("")
        hist.SetLineWidth(1)
        hist.GetYaxis().SetLabelSize(0.09)
        hist.GetXaxis().SetLabelSize(0.09)
        hist.GetYaxis().SetLabelOffset(0.004)
        hist.GetXaxis().SetLabelOffset(0.004)
        hist.Draw("HIST E0" if(first) else "HIST E0 SAME")
        first = False
    draw_bin_label(pad, q2y, zpt, alive)
    pad.Modified()


def draw_bc_family(args, info, q2y_bins):
    import importlib.util
    script_path = os.path.join(ANALYSIS, "BC_Corrections", "BC_Corrections_Script.py")
    spec = importlib.util.spec_from_file_location("bc_corrections_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    plotter = module.Plot_BC_Subbin_Inputs_From_JSON if(info["family"] == "bc_subbin") else module.Plot_BC_Factor_From_JSON
    payload = json.load(open(info["json"]))
    bc_args = argparse.Namespace(Q2_y_Bin=1, z_pT_Bin=1, json_file_out=info["json"], test=True, File_Format="pdf", image_name="", BC_Zoom=False, verbose=False, show_bin_stats=False)
    alive = []
    canvas, host = make_host(info["family"], args.summary_text, alive)
    missing = []
    counts = {}
    legend_entries = None
    for q2y in q2y_bins:
        kept, rows, cols = retained_bins(q2y)
        counts[q2y] = len(kept)
        if(counts[q2y] != RETAINED[q2y]):
            missing.append("retained %s=%s expected %s" % (q2y, counts[q2y], RETAINED[q2y]))
        cell = host.cd(Q2Y_PAD[q2y])
        left, grid = open_q2y_cell(cell, q2y, cols, rows, alive, False)
        for zpt in kept:
            pad = grid.cd(zpt)
            try:
                drawn = plotter(bc_args, main_pad=pad, save_plot=False, q2_y_bin_override=q2y, z_pT_bin_override=zpt, json_data=payload, draw_legend=False)
            except Exception as exc:
                missing.append("bc draw %s-%s %s" % (q2y, zpt, exc))
                continue
            if(not isinstance(drawn, dict)):
                missing.append("bc draw returned no pad objects %s-%s" % (q2y, zpt))
                continue
            alive.append(drawn)
            if(info["family"] == "bc_subbin"):
                hists = [drawn["h_ave"], drawn["h_center"]]
            else:
                hists = [drawn["h_bc"]]
            show_existing_hists(pad, hists, q2y, zpt, alive)
            if(legend_entries is None):
                if(info["family"] == "bc_subbin"):
                    legend_entries = [("Average sub-bin", drawn["h_ave"], "points"), ("Center sub-bin", drawn["h_center"], "points")]
                else:
                    legend_entries = [("BC factor", drawn["h_bc"], "points")]
    if(legend_entries):
        draw_global_legend(host, legend_entries, alive)
    thesis_ready = (len(missing) == 0)
    if(thesis_ready and (not args.dry_run)):
        save_one_page(canvas, info["pdf"])
    elif(not thesis_ready):
        info["reason"] = "; ".join(missing[:8])
    info["thesis_ready"] = thesis_ready
    info["counts"] = counts
    return info


def selected_families(args):
    if(len(args.family) > 0):
        return list(args.family)
    return list(FAMILIES)


def main():
    args = parse_args()
    q2y_bins = q2y_list(args.q2y_bins)
    print("unfolded_3d %s" % args.unfolded_3d)
    print("rc_factors %s" % args.rc_factors)
    print("bc_root %s" % args.bc_root)
    print("bc_json %s" % args.bc_json)
    print("fallback_2d %s" % args.fallback_2d)
    norho_path, norho_note = find_norho(args.unfolded_3d_norho)
    print("unfolded_3d_norho %s" % (norho_path if(norho_path) else "not found"))
    print("norho_note %s" % norho_note)
    print("fit_ac %s" % FIT_AC)
    print("fit_bc %s" % FIT_BC)
    print("fit_rc not found")
    for family in selected_families(args):
        info = resolve_family(args, family)
        print("PLAN family=%s thesis_ready=%s root=%s fit=%s pdf=%s reason=%s" % (family, "yes" if(info["thesis_ready"]) else "no", info.get("root", ""), info.get("fit", ""), info["pdf"], info["reason"]))
        if(args.dry_run):
            continue
        if(not info["thesis_ready"]):
            print("STATUS family=%s thesis_ready=no pdf= reason=%s" % (family, info["reason"]))
            continue
        if(family in ["bc_subbin", "bc_factor"]):
            info = draw_bc_family(args, info, q2y_bins)
        else:
            info = draw_family(args, info, q2y_bins)
        print("STATUS family=%s thesis_ready=%s pdf=%s reason=%s" % (family, "yes" if(info["thesis_ready"]) else "no", info["pdf"] if(info["thesis_ready"]) else "", info["reason"]))
    for handle in OPEN_FILES.values():
        handle.Close()


if(__name__ == "__main__"):
    main()
