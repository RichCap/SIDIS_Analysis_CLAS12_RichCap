#!/usr/bin/env python3
# Consolidated thesis phi_h figures. One 4x5 Q2-y canvas per family.
# Pad map copied from phi_h_1D_Compare_in_z_pT_Images_Together in
# Histo_Files_ROOT/DataFrames/Get_rho_Normalization_values.py.

import argparse
import csv
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

from MyCommonAnalysisFunction_richcap import Canvas_Create, Draw_Canvas, Get_Num_of_z_pT_Rows_and_Columns, MM_z_pT_Draw, Q2_Y_Border_Lines, skip_condition_z_pT_bins
from Binning_Dictionaries import Full_Bin_Definition_Array

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
    parser.add_argument("-mm", "--missing_mass_study", action="store_true", help="Draw the missing-mass cut study. Default off, and the phi_h families are not drawn.")
    parser.add_argument("-mmc", "--missing_mass_consolidated", action="store_true", help="Draw the two thesis missing-mass mosaics. Default off.")
    parser.add_argument("-mmroot", "--missing_mass_root", default="", help="1D ROOT file for the missing-mass study.")
    parser.add_argument("-mmo", "--missing_mass_output", default="", help="Output directory for the missing-mass study.")
    parser.add_argument("-mmcsv", "--missing_mass_csv", default="", help="Classification CSV for the consolidated mosaics.")
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


def phi_canvas_decision(drawn, na_count, dry_run):
    studies = os.path.join(ANALYSIS, "Systematic_Studies")
    if(studies not in sys.path):
        sys.path.insert(0, studies)
    import sidis_physics_lib as phys
    return phys.phi_canvas_decision(drawn, na_count, dry_run)


def room_for_labels(pad, top=0.18):
    pad.SetLeftMargin(0.20)
    pad.SetRightMargin(0.02)
    pad.SetBottomMargin(0.11)
    pad.SetTopMargin(top)


def mark_na_pad(pad, q2y, zpt, reason, alive):
    # Text only. No histogram is created, so a missing bin is not stored as zero.
    pad.cd()
    ROOT.gStyle.SetOptTitle(0)
    room_for_labels(pad)
    label = ROOT.TPaveText(0.08, 0.22, 0.92, 0.78, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.SetTextFont(42)
    label.SetTextAlign(22)
    label.SetTextSize(0.11)
    label.AddText("N/A")
    label.AddText("%s-%s" % (q2y, zpt))
    label.AddText(reason)
    label.Draw()
    alive.append(label)
    draw_bin_label(pad, q2y, zpt, alive)
    pad.Modified()


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
    drawn = 0
    na_count = 0
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
                mark_na_pad(pad, q2y, zpt, "empty", alive)
                na_count += 1
                continue
            fit_func = None
            if(fit_block is not None):
                pars = fit_block.get("(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt))
                if(not isinstance(pars, dict)):
                    missing.append("missing fit %s-%s" % (q2y, zpt))
                    mark_na_pad(pad, q2y, zpt, "missing fit", alive)
                    na_count += 1
                    continue
                fit_func = make_fit("fit_%s_%s_%s" % (family, q2y, zpt), pars)
            draw_stack(pad, hists, [item[1] for item in spec], [item[2] for item in spec], spec, fit_func, alive, q2y, zpt)
            drawn += 1
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
    decision = phi_canvas_decision(drawn, na_count, args.dry_run)
    destination = info["pdf"]
    if(decision["save"]):
        save_one_page(canvas, destination)
    if(len(missing) > 0):
        info["reason"] = "; ".join(missing[:8])
    info["thesis_ready"] = decision["thesis_ready"]
    info["pdf_written"] = decision["save"]
    info["na_count"] = na_count
    info["drawn"] = drawn
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
    pad_count = 0
    na_count = 0
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
                drawn_objects = plotter(bc_args, main_pad=pad, save_plot=False, q2_y_bin_override=q2y, z_pT_bin_override=zpt, json_data=payload, draw_legend=False)
            except Exception as exc:
                missing.append("bc draw %s-%s %s" % (q2y, zpt, exc))
                mark_na_pad(pad, q2y, zpt, "missing", alive)
                na_count += 1
                continue
            if(not isinstance(drawn_objects, dict)):
                missing.append("bc draw returned no pad objects %s-%s" % (q2y, zpt))
                mark_na_pad(pad, q2y, zpt, "missing", alive)
                na_count += 1
                continue
            alive.append(drawn_objects)
            if(info["family"] == "bc_subbin"):
                hists = [drawn_objects["h_ave"], drawn_objects["h_center"]]
            else:
                hists = [drawn_objects["h_bc"]]
            show_existing_hists(pad, hists, q2y, zpt, alive)
            pad_count += 1
            if(legend_entries is None):
                if(info["family"] == "bc_subbin"):
                    legend_entries = [("Average sub-bin", drawn_objects["h_ave"], "points"), ("Center sub-bin", drawn_objects["h_center"], "points")]
                else:
                    legend_entries = [("BC factor", drawn_objects["h_bc"], "points")]
    if(legend_entries):
        draw_global_legend(host, legend_entries, alive)
    decision = phi_canvas_decision(pad_count, na_count, args.dry_run)
    if(decision["save"]):
        save_one_page(canvas, info["pdf"])
    if(len(missing) > 0):
        info["reason"] = "; ".join(missing[:8])
    info["thesis_ready"] = decision["thesis_ready"]
    info["pdf_written"] = decision["save"]
    info["na_count"] = na_count
    info["drawn"] = pad_count
    info["counts"] = counts
    return info


MM_THRESHOLD = 1.8
MM_REVIEW    = "/Users/richardcapobianco/Desktop/MM_Cut_Impact_Study_Review"
MM_ROOT_DEFAULT = os.path.join(ANALYSIS, "Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_1D_SIDIS_Workflow_V2_Bank_Kinematics_Final_Thesis_Files_All.root")
MM_INTEGRAL_DEFINITION = "N_below is the underflow plus every bin whose upper edge is <= 1.8 GeV. The bin that starts at 1.8 GeV is not below. A bin that straddled 1.8 GeV would be N_straddle and would not be split. N_above is the remaining in-range bins plus overflow. N_total = N_below + N_straddle + N_above. Contents are unweighted."
MM_PROJ_I = 0
MM_KEY = {
    "rdf_mm_none":     "((Histo-Group='Only_1D'), (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS_MM_None'), (Smear-Type='no_smear'), (Binning-Type='Y_bin'), (Var='MM'))",
    "rdf_nominal":     "((Histo-Group='Only_1D'), (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='no_smear'), (Binning-Type='Y_bin'), (Var='MM'))",
    "mdf_mm_none":     "((Histo-Group='Only_1D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS_MM_None'), (Smear-Type='no_smear'), (Binning-Type='Y_bin'), (Var='MM'))",
    "mdf_nominal":     "((Histo-Group='Only_1D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='no_smear'), (Binning-Type='Y_bin'), (Var='MM'))",
    "mdf_matched_gen": "((Histo-Group='Only_1D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='matched_gen'), (Binning-Type='Y_bin'), (Var='MM_gen'))",
}
MM_SOURCE_ORDER = ["rdf_mm_none", "mdf_mm_none", "mdf_matched_gen"]
MM_COLOR = {"rdf_mm_none": ROOT.kBlue + 1, "mdf_mm_none": ROOT.kRed + 1, "mdf_matched_gen": ROOT.kGreen + 2}
MM_EXPECTED_INTEGRAL = {
    "rdf_mm_none": 38315028.0,
    "rdf_nominal": 30204509.0,
    "mdf_mm_none": 330091216.0,
    "mdf_nominal": 275392373.0,
    "mdf_matched_gen": 275392373.0,
}


def mm_num_text(value):
    if(value in ["", None]):
        return ""
    if(abs(float(value) - round(float(value))) < 1e-6):
        return str(int(round(float(value))))
    return format(float(value), ".12g")


def mm_percent_label(value):
    if(value in ["", None]):
        return "N/A"
    return "%.2f%%" % float(value)


def mm_piece_counts(hist):
    axis  = hist.GetXaxis()
    nbins = hist.GetNbinsX()
    n_under    = hist.GetBinContent(0)
    n_over     = hist.GetBinContent(nbins + 1)
    n_below    = n_under
    n_above    = n_over
    n_straddle = 0.0
    thr_bin    = axis.FindBin(MM_THRESHOLD)
    on_edge    = abs(axis.GetBinLowEdge(thr_bin) - MM_THRESHOLD) < 1e-8
    for ibin in range(1, nbins + 1):
        low     = axis.GetBinLowEdge(ibin)
        up      = axis.GetBinUpEdge(ibin)
        content = hist.GetBinContent(ibin)
        if(up <= MM_THRESHOLD + 1e-8):
            n_below += content
        elif(low >= MM_THRESHOLD - 1e-8):
            n_above += content
        else:
            n_straddle += content
    n_total = n_below + n_above + n_straddle
    return n_below, n_above, n_straddle, n_under, n_over, n_total, on_edge


def project_mm_cell(hist3, q2y, zpt, tag):
    global MM_PROJ_I
    MM_PROJ_I += 1
    ybin = hist3.GetYaxis().FindBin(float(q2y))
    zbin = hist3.GetZaxis().FindBin(float(zpt))
    if((abs(hist3.GetYaxis().GetBinCenter(ybin) - float(q2y)) > 1e-6) or (abs(hist3.GetZaxis().GetBinCenter(zbin) - float(zpt)) > 1e-6)):
        raise RuntimeError("bin-center mismatch for %s Q2-y %s z-pT %s" % (tag, q2y, zpt))
    proj = hist3.ProjectionX("mm_%s_%s_%s_%s" % (tag, q2y, zpt, MM_PROJ_I), ybin, ybin, zbin, zbin)
    proj.SetDirectory(0)
    return proj


def mm_full_integral(hist3):
    return hist3.Integral(0, hist3.GetNbinsX() + 1, 0, hist3.GetNbinsY() + 1, 0, hist3.GetNbinsZ() + 1)


def compare_mm_subset(none_hist, cut_hist):
    nbins = none_hist.GetNbinsX()
    n_below, n_above, n_straddle, n_under, n_over, n_total, on_edge = mm_piece_counts(cut_hist)
    n_none = none_hist.Integral(0, nbins + 1)
    n_cut  = cut_hist.Integral(0, nbins + 1)
    violations = 0
    excess     = 0.0
    if(cut_hist.GetNbinsX() != nbins):
        violations = -1
    else:
        for ibin in range(0, nbins + 2):
            cut_content  = cut_hist.GetBinContent(ibin)
            none_content = none_hist.GetBinContent(ibin)
            if(cut_content > none_content):
                violations += 1
                excess     += cut_content - none_content
    status = "pass" if(violations == 0) else "fail"
    rejected = ""
    percent  = ""
    if((violations == 0) and (n_none > 0)):
        rejected = n_none - n_cut
        percent  = 100.0 * rejected / n_none
    elif(n_none <= 0):
        status = "undetermined"
    return {
        "subset_status": status,
        "n_violating_bins": violations,
        "excess_counts": excess,
        "n_mm_none": n_none,
        "n_nominal": n_cut,
        "n_nominal_below": n_below,
        "n_rejected": rejected,
        "percent_rejected": percent,
        "nominal_on_edge": on_edge,
    }


def blank_subset():
    return {
        "subset_status": "not_applicable",
        "n_violating_bins": "",
        "excess_counts": "",
        "n_mm_none": "",
        "n_nominal": "",
        "n_nominal_below": "",
        "n_rejected": "",
        "percent_rejected": "",
    }


def mm_record(q2y, zpt, source, status, hist_key, counts=None, subset=None):
    if(source == "rdf_mm_none"):
        cut_name = "cut_Complete_SIDIS_MM_None"
        meaning  = "experimental_unsmeared_below_threshold_fraction"
    elif(source == "mdf_mm_none"):
        cut_name = "cut_Complete_SIDIS_MM_None"
        meaning  = "reconstructed_mc_unsmeared_below_threshold_fraction"
    elif(source == "mdf_matched_gen"):
        cut_name = "cut_Complete_SIDIS"
        meaning  = "matched_generated_below_threshold_fraction"
    else:
        cut_name = ""
        meaning  = ""
    if(subset is None):
        subset = blank_subset()
    n_below = n_above = n_straddle = n_under = n_over = n_total = ""
    on_edge = ""
    percent = ""
    if(counts is not None):
        n_below, n_above, n_straddle, n_under, n_over, n_total, on_edge = counts
        if(n_total > 0):
            percent = 100.0 * n_below / n_total
            status  = "ok"
        else:
            status  = "empty"
            percent = ""
    row = {
        "q2y_bin": q2y,
        "zpt_bin": zpt,
        "bin_role": "retained",
        "source": source,
        "cut_definition": cut_name,
        "interpretation": meaning,
        "n_below": n_below,
        "n_above": n_above,
        "n_straddle": n_straddle,
        "n_underflow": n_under,
        "n_overflow": n_over,
        "n_total": n_total,
        "percent_below": percent,
        "percent_below_label": mm_percent_label(percent) if(status == "ok") else "N/A",
        "sample_status": status,
        "histo_key": hist_key,
        "threshold_gev": MM_THRESHOLD,
        "threshold_on_edge": on_edge,
        "integral_definition": MM_INTEGRAL_DEFINITION,
    }
    row.update(subset)
    row["percent_rejected_label"] = mm_percent_label(row["percent_rejected"]) if(row["percent_rejected"] not in ["", None]) else ""
    return row


def mm_below_class(mdf_row):
    if(mdf_row is None):
        return "Undetermined"
    if(mdf_row["sample_status"] != "ok"):
        return "Undetermined"
    if(float(mdf_row["n_below"]) > 0):
        return "Observed below-threshold events"
    return "No observed below-threshold events"


def eval_curve_z(formula, pt_value):
    expression = str(formula).replace("sqrt", "ROOT.sqrt").replace("x", "(%s)" % format(pt_value, ".8f"))
    try:
        value = eval(expression)
    except Exception:
        return None
    try:
        value = float(value)
    except Exception:
        return None
    if(value != value):
        return None
    return value


def curve_formulas_for_q2y(q2y):
    formulas = []
    for pick in ["Minimum", "Maximum"]:
        pair = MM_z_pT_Draw(z_val="pT", MM_val=MM_THRESHOLD, Q2_y_Bin=q2y, pT_Input="pT", Q2_y_value_pick=pick)
        formulas.extend(pair)
    return formulas


def curve_enters_rectangle(formulas, z_max, z_min, pt_max, pt_min):
    # Sampled diagnostic of the helper's two quadratic branches. Not a safety class.
    pt_value = float(pt_min)
    entered  = False
    while(pt_value <= float(pt_max) + 1e-9):
        for formula in formulas:
            value = eval_curve_z(formula, pt_value)
            if((value is not None) and (value >= float(z_min)) and (value <= float(z_max))):
                entered = True
        if(entered):
            break
        pt_value += 0.002
    return "curve_enters" if(entered) else "curve_outside"


def write_mm_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    handle = open(path, "w", newline="")
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        out = {}
        for field in fieldnames:
            value = row.get(field, "")
            if(isinstance(value, float)):
                out[field] = format(value, ".12g")
            else:
                out[field] = value
        writer.writerow(out)
    handle.close()


def style_mm_hist(hist, line_color):
    hist.SetDirectory(0)
    hist.SetLineColor(line_color)
    hist.SetLineWidth(2)
    hist.SetFillStyle(0)
    hist.SetMarkerSize(0)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("M_{X} [GeV]")
    hist.GetYaxis().SetTitle("")
    hist.GetXaxis().SetTitleSize(0.07)
    hist.GetXaxis().SetLabelSize(0.055)
    hist.GetYaxis().SetLabelSize(0.055)
    hist.GetXaxis().SetNdivisions(505)
    hist.SetStats(0)


def draw_mm_titles(pad, lines, alive, text_size):
    label = ROOT.TPaveText(0.02, 1.0 - pad.GetTopMargin(), 0.98, 0.995, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.SetTextFont(42)
    label.SetTextAlign(22)
    label.SetTextSize(text_size)
    for line in lines:
        label.AddText(line)
    label.Draw()
    alive.append(label)


def mm_title_lines(row, compact):
    lines = ["Q^{2}-y %s, z-P_{T} %s" % (row["q2y_bin"], row["zpt_bin"])]
    if(row["sample_status"] != "ok"):
        lines.append("N/A")
        return lines
    if(row["source"] == "mdf_matched_gen"):
        lines.append("matched-gen below 1.8: %s" % row["percent_below_label"])
    else:
        lines.append("unsmeared below 1.8: %s" % row["percent_below_label"])
    if(not compact):
        lines.append("N_{below}=%s, N=%s" % (mm_num_text(row["n_below"]), mm_num_text(row["n_total"])))
        if(row["source"] != "mdf_matched_gen"):
            if(row["percent_rejected"] in ["", None]):
                lines.append("nominal removal: not established")
            else:
                lines.append("nominal removal: %s" % row["percent_rejected_label"])
    return lines


def draw_mm_pad(pad, row, hist, alive, compact):
    pad.cd()
    pad.SetFillColor(ROOT.kWhite)
    pad.SetFillStyle(1001)
    pad.SetTopMargin(0.34 if(not compact) else 0.22)
    pad.SetBottomMargin(0.16 if(not compact) else 0.14)
    pad.SetLeftMargin(0.16)
    pad.SetRightMargin(0.04)
    ROOT.gStyle.SetOptStat(0)
    if((row is None) or (row["sample_status"] != "ok") or (hist is None)):
        mark = ROOT.TPaveText(0.08, 0.25, 0.92, 0.75, "NDC")
        mark.SetFillStyle(0)
        mark.SetBorderSize(0)
        mark.SetTextAlign(22)
        mark.SetTextSize(0.12 if(not compact) else 0.16)
        if((row is not None) and (row["bin_role"] == "skipped")):
            mark.AddText("Skipped")
        else:
            mark.AddText("N/A")
            if(row is not None):
                mark.AddText("%s-%s" % (row["q2y_bin"], row["zpt_bin"]))
        mark.Draw()
        alive.append(mark)
        return
    shown = hist.Clone("%s_draw_%s" % (hist.GetName(), id(pad)))
    shown.SetDirectory(0)
    style_mm_hist(shown, MM_COLOR[row["source"]])
    ymax = shown.GetMaximum()
    if(ymax <= 0):
        ymax = 1.0
    shown.GetYaxis().SetRangeUser(0.0, ymax * 1.25)
    shown.Draw("HIST")
    alive.append(shown)
    cut_line = ROOT.TLine(MM_THRESHOLD, 0.0, MM_THRESHOLD, ymax * 1.25)
    cut_line.SetLineColor(ROOT.kRed)
    cut_line.SetLineStyle(2)
    cut_line.SetLineWidth(2)
    cut_line.Draw("same")
    alive.append(cut_line)
    if(float(row["n_below"]) > 0):
        outline = ROOT.TPave(0.01, 0.01, 0.99, 0.99, 1, "NDC")
        outline.SetFillStyle(0)
        outline.SetLineColor(ROOT.kRed)
        outline.SetLineWidth(2)
        outline.Draw()
        alive.append(outline)
    draw_mm_titles(pad, mm_title_lines(row, compact), alive, 0.055 if(not compact) else 0.09)
    pad.Modified()


def draw_mm_q2y_canvas(path, q2y, rows, cols, row_by_zpt, hist_by_zpt):
    alive  = []
    canvas = ROOT.TCanvas("mm_q2y_%s" % q2y, "", 2400, 3200)
    canvas.SetFillColor(ROOT.kWhite)
    host = ROOT.TPad("mm_host_%s" % q2y, "", 0.035, 0.025, 0.985, 0.985)
    host.SetFillColor(ROOT.kWhite)
    host.Draw()
    host.Divide(cols, rows, 0.004, 0.004)
    alive.append(canvas)
    alive.append(host)
    for zpt in range(1, rows * cols + 1):
        draw_mm_pad(host.cd(zpt), row_by_zpt.get(zpt), hist_by_zpt.get(zpt), alive, False)
    canvas.SaveAs(path)
    canvas.Clear()
    alive.clear()


def draw_mm_overview(path, q2y_bins, rows_of, row_maps, hist_maps):
    alive = []
    canvas, host = make_host(os.path.basename(path), "", alive)
    for q2y in q2y_bins:
        kept, rows, cols = rows_of[q2y]
        cell = host.cd(Q2Y_PAD[q2y])
        left, grid = open_q2y_cell(cell, q2y, cols, rows, alive, False)
        for zpt in range(1, rows * cols + 1):
            draw_mm_pad(grid.cd(zpt), row_maps[q2y].get(zpt), hist_maps[q2y].get(zpt), alive, True)
    canvas.SaveAs(path)
    canvas.Clear()
    alive.clear()


def draw_overlay_pad(pad, q2y, zpt, data_hist, mc_hist, data_row, mc_row, alive, compact):
    pad.cd()
    pad.SetFillColor(ROOT.kWhite)
    pad.SetTopMargin(0.32 if(not compact) else 0.24)
    pad.SetBottomMargin(0.16 if(not compact) else 0.14)
    pad.SetLeftMargin(0.16)
    pad.SetRightMargin(0.04)
    if((data_row is None) or (mc_row is None) or (data_row["sample_status"] != "ok") or (mc_row["sample_status"] != "ok")):
        mark = ROOT.TPaveText(0.08, 0.3, 0.92, 0.7, "NDC")
        mark.SetFillStyle(0)
        mark.SetBorderSize(0)
        mark.SetTextAlign(22)
        mark.SetTextSize(0.1)
        if((data_row is not None) and (data_row.get("bin_role") == "skipped")):
            mark.AddText("Skipped")
        else:
            mark.AddText("N/A")
        mark.Draw()
        alive.append(mark)
        return
    drawn = []
    ymax  = 0.0
    for hist, color in [(data_hist, ROOT.kBlue + 1), (mc_hist, ROOT.kRed + 1)]:
        clone = hist.Clone("%s_norm_%s" % (hist.GetName(), id(pad)))
        clone.SetDirectory(0)
        total = clone.Integral(0, clone.GetNbinsX() + 1)
        if(total > 0):
            clone.Scale(1.0 / total)
        style_mm_hist(clone, color)
        ymax = max(ymax, clone.GetMaximum())
        drawn.append(clone)
        alive.append(clone)
    if(ymax <= 0):
        ymax = 1.0
    first = True
    for clone in drawn:
        clone.GetYaxis().SetRangeUser(0.0, ymax * 1.35)
        clone.Draw("HIST" if(first) else "HIST SAME")
        first = False
    cut_line = ROOT.TLine(MM_THRESHOLD, 0.0, MM_THRESHOLD, ymax * 1.35)
    cut_line.SetLineColor(ROOT.kBlack)
    cut_line.SetLineStyle(2)
    cut_line.SetLineWidth(2)
    cut_line.Draw("same")
    alive.append(cut_line)
    lines = ["Q^{2}-y %s, z-P_{T} %s" % (q2y, zpt), "data below %s" % data_row["percent_below_label"], "MC below %s" % mc_row["percent_below_label"]]
    draw_mm_titles(pad, lines, alive, 0.055 if(not compact) else 0.08)
    pad.Modified()


def draw_overlay_q2y(path, q2y, rows, cols, data_rows, mc_rows, data_hists, mc_hists):
    alive  = []
    canvas = ROOT.TCanvas("mm_overlay_%s" % q2y, "", 2400, 3200)
    canvas.SetFillColor(ROOT.kWhite)
    host = ROOT.TPad("mm_overlay_host_%s" % q2y, "", 0.035, 0.025, 0.985, 0.985)
    host.SetFillColor(ROOT.kWhite)
    host.Draw()
    host.Divide(cols, rows, 0.004, 0.004)
    alive.append(canvas)
    alive.append(host)
    for zpt in range(1, rows * cols + 1):
        draw_overlay_pad(host.cd(zpt), q2y, zpt, data_hists.get(zpt), mc_hists.get(zpt), data_rows.get(zpt), mc_rows.get(zpt), alive, False)
    canvas.SaveAs(path)
    canvas.Clear()
    alive.clear()


def draw_overlay_overview(path, q2y_bins, rows_of, data_rows, mc_rows, data_hists, mc_hists):
    alive = []
    canvas, host = make_host("mm_overlay_overview", "", alive)
    for q2y in q2y_bins:
        kept, rows, cols = rows_of[q2y]
        cell = host.cd(Q2Y_PAD[q2y])
        left, grid = open_q2y_cell(cell, q2y, cols, rows, alive, False)
        for zpt in range(1, rows * cols + 1):
            draw_overlay_pad(grid.cd(zpt), q2y, zpt, data_hists[q2y].get(zpt), mc_hists[q2y].get(zpt), data_rows[q2y].get(zpt), mc_rows[q2y].get(zpt), alive, True)
    canvas.SaveAs(path)
    canvas.Clear()
    alive.clear()


def shape_distance(data_hist, mc_hist):
    nbins = data_hist.GetNbinsX()
    data_total = data_hist.Integral(0, nbins + 1)
    mc_total   = mc_hist.Integral(0, nbins + 1)
    if((data_total <= 0) or (mc_total <= 0)):
        return "", "", "", ""
    tv_full  = 0.0
    tv_below = 0.0
    data_below = 0.0
    mc_below   = 0.0
    below_bins = []
    axis = data_hist.GetXaxis()
    for ibin in range(0, nbins + 2):
        pdata = data_hist.GetBinContent(ibin) / data_total
        pmc   = mc_hist.GetBinContent(ibin) / mc_total
        tv_full += abs(pdata - pmc)
        low = -1.0 if(ibin == 0) else axis.GetBinLowEdge(ibin)
        up  = axis.GetBinLowEdge(1) if(ibin == 0) else (1e9 if(ibin == nbins + 1) else axis.GetBinUpEdge(ibin))
        is_below = (ibin == 0) or ((ibin <= nbins) and (up <= MM_THRESHOLD + 1e-8))
        if(is_below):
            tv_below   += abs(pdata - pmc)
            data_below += data_hist.GetBinContent(ibin)
            mc_below   += mc_hist.GetBinContent(ibin)
            below_bins.append(ibin)
    tv_full  = 0.5 * tv_full
    tv_below = 0.5 * tv_below
    tv_shape = ""
    if((data_below > 0) and (mc_below > 0)):
        shape = 0.0
        for ibin in below_bins:
            shape += abs((data_hist.GetBinContent(ibin) / data_below) - (mc_hist.GetBinContent(ibin) / mc_below))
        tv_shape = 0.5 * shape
    return tv_full, tv_below, tv_shape, abs((data_below / data_total) - (mc_below / mc_total)) * 100.0


def run_missing_mass_study(args):
    ROOT.gStyle.SetLineScalePS(1)
    ROOT.gStyle.SetOptStat(0)
    output = args.missing_mass_output if(args.missing_mass_output not in ["", None]) else os.path.join(MM_REVIEW, "phase1_1d")
    pdf_dir = os.path.join(output, "pdf")
    csv_dir = os.path.join(output, "csv")
    log_dir = os.path.join(MM_REVIEW, "logs")
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "phase1_missing_mass.log")
    log_lines = []
    def log(message):
        print(message)
        log_lines.append(message)
    root_path = args.missing_mass_root if(args.missing_mass_root not in ["", None]) else MM_ROOT_DEFAULT
    log("missing-mass root %s" % root_path)
    log(MM_INTEGRAL_DEFINITION)
    log("Data MM_None differs from the nominal cut by the unsmeared sqrt(MM2) > 1.8 requirement.")
    log("Reconstructed-MC MM_None and the nominal cut share smeared kinematic cuts and differ by sqrt(smeared MM2) > 0 versus > 1.8.")
    log("The reconstructed-MC axis and bin indices are unsmeared. f_below is not the nominal rejected fraction.")
    log("f_rejected is (N_MM_None - N_nominal) / N_MM_None after every missing-mass bin satisfies N_nominal <= N_MM_None.")
    handle = open_root(root_path)
    loaded = {}
    for tag, key in MM_KEY.items():
        hist = take(handle, key)
        if(hist is None):
            raise RuntimeError("missing histogram %s" % key)
        integral = mm_full_integral(hist)
        log("integral %s %s expected %s" % (tag, mm_num_text(integral), mm_num_text(MM_EXPECTED_INTEGRAL[tag])))
        if(abs(integral - MM_EXPECTED_INTEGRAL[tag]) > 0.1):
            raise RuntimeError("integral mismatch for %s" % tag)
        loaded[tag] = hist
    q2y_bins = q2y_list(args.q2y_bins)
    rows_of = {}
    retained_count = 0
    skipped_count  = 0
    for q2y in q2y_bins:
        kept, rows, cols = retained_bins(q2y)
        rows_of[q2y] = (kept, rows, cols)
        if(len(kept) != RETAINED[q2y]):
            raise RuntimeError("retained count Q2-y %s is %s, expected %s" % (q2y, len(kept), RETAINED[q2y]))
        retained_count += len(kept)
        skipped_count  += rows * cols - len(kept)
    if((q2y_bins == list(range(1, 18))) and (retained_count != 452)):
        raise RuntimeError("retained total %s is not 452" % retained_count)
    log("retained %s skipped grid cells %s" % (retained_count, skipped_count))
    detail_rows = []
    hist_maps   = {source: {} for source in MM_SOURCE_ORDER}
    row_maps    = {source: {} for source in MM_SOURCE_ORDER}
    for q2y in q2y_bins:
        kept, rows, cols = rows_of[q2y]
        log("counting Q2-y %s" % q2y)
        hist_maps_q = {source: {} for source in MM_SOURCE_ORDER}
        row_maps_q  = {source: {} for source in MM_SOURCE_ORDER}
        for zpt in range(1, rows * cols + 1):
            if(zpt not in kept):
                detail_rows.append({
                    "q2y_bin": q2y, "zpt_bin": zpt, "bin_role": "skipped", "source": "",
                    "cut_definition": "", "interpretation": "", "n_below": "", "n_above": "",
                    "n_straddle": "", "n_underflow": "", "n_overflow": "", "n_total": "",
                    "percent_below": "", "percent_below_label": "", "sample_status": "skipped",
                    "histo_key": "", "threshold_gev": MM_THRESHOLD, "threshold_on_edge": "",
                    "integral_definition": MM_INTEGRAL_DEFINITION, "subset_status": "not_applicable",
                    "n_violating_bins": "", "excess_counts": "", "n_mm_none": "", "n_nominal": "",
                    "n_nominal_below": "", "n_rejected": "", "percent_rejected": "", "percent_rejected_label": "",
                })
                row_maps_q_skip = {
                    "q2y_bin": q2y, "zpt_bin": zpt, "bin_role": "skipped", "source": "",
                    "sample_status": "skipped", "n_below": "", "percent_below_label": "",
                    "percent_rejected": "", "percent_rejected_label": "",
                }
                for source in MM_SOURCE_ORDER:
                    row_maps_q[source][zpt] = row_maps_q_skip
                continue
            for source in MM_SOURCE_ORDER:
                proj   = project_mm_cell(loaded[source], q2y, zpt, source)
                counts = mm_piece_counts(proj)
                subset = blank_subset()
                if(source in ["rdf_mm_none", "mdf_mm_none"]):
                    nominal_tag = "rdf_nominal" if(source == "rdf_mm_none") else "mdf_nominal"
                    nominal     = project_mm_cell(loaded[nominal_tag], q2y, zpt, nominal_tag)
                    subset      = compare_mm_subset(proj, nominal)
                row = mm_record(q2y, zpt, source, "missing", MM_KEY[source], counts, subset)
                if((row["percent_below"] not in ["", None]) and (abs(float(row["percent_below_label"].replace("%", "")) - float("%.2f" % row["percent_below"])) > 0.001)):
                    raise RuntimeError("label mismatch %s %s %s" % (source, q2y, zpt))
                detail_rows.append(row)
                row_maps_q[source][zpt]  = row
                hist_maps_q[source][zpt] = proj
        for source in MM_SOURCE_ORDER:
            row_maps[source][q2y]  = row_maps_q[source]
            hist_maps[source][q2y] = hist_maps_q[source]
        spot = row_maps_q["rdf_mm_none"].get(1)
        if((q2y == 1) and (spot is not None)):
            log("spot Q2-y 1 z-pT 1 data total %s below %s" % (mm_num_text(spot["n_total"]), mm_num_text(spot["n_below"])))
            if((abs(float(spot["n_total"]) - 42583.0) > 0.1) or (abs(float(spot["n_below"])) > 0.1)):
                raise RuntimeError("spot check failed for data bin 1, 1")
    detail_fields = [
        "q2y_bin", "zpt_bin", "bin_role", "source", "cut_definition", "interpretation",
        "n_below", "n_above", "n_straddle", "n_underflow", "n_overflow", "n_total",
        "percent_below", "percent_below_label", "sample_status", "histo_key",
        "threshold_gev", "threshold_on_edge", "integral_definition", "subset_status",
        "n_violating_bins", "excess_counts", "n_mm_none", "n_nominal", "n_nominal_below",
        "n_rejected", "percent_rejected", "percent_rejected_label",
    ]
    write_mm_csv(os.path.join(csv_dir, "mm_cut_bin_counts.csv"), detail_rows, detail_fields)
    log("wrote bin counts")
    border_rows = []
    max_border_diff = 0.0
    for q2y in range(1, 18):
        helper = [float(value) for value in Q2_Y_Border_Lines(q2y)]
        live   = [float(value) for value in Full_Bin_Definition_Array["Q2-y=%d, Q2-y" % q2y]]
        diffs  = [abs(helper[i] - live[i]) for i in range(4)]
        max_border_diff = max(max_border_diff, max(diffs))
        border_rows.append({
            "q2y_bin": q2y,
            "helper_q2_max": helper[0], "helper_q2_min": helper[1], "helper_y_max": helper[2], "helper_y_min": helper[3],
            "live_q2_max": live[0], "live_q2_min": live[1], "live_y_max": live[2], "live_y_min": live[3],
            "max_abs_diff": max(diffs),
        })
    write_mm_csv(os.path.join(csv_dir, "q2y_border_comparison.csv"), border_rows, list(border_rows[0].keys()))
    log("maximum Q2-y border difference %s" % format(max_border_diff, ".12g"))
    class_rows = []
    shape_rows = []
    for q2y in q2y_bins:
        kept, rows, cols = rows_of[q2y]
        log("geometry and shapes Q2-y %s" % q2y)
        formulas = curve_formulas_for_q2y(q2y)
        for zpt in range(1, rows * cols + 1):
            mdf_row = row_maps["mdf_mm_none"][q2y].get(zpt)
            rdf_row = row_maps["rdf_mm_none"][q2y].get(zpt)
            gen_row = row_maps["mdf_matched_gen"][q2y].get(zpt)
            corners = Full_Bin_Definition_Array.get("Q2-y=%d, z-pT=%d" % (q2y, zpt))
            if(zpt not in kept):
                geometry = "skipped"
                label    = "Skipped"
            elif(corners is None):
                geometry = "no_corners"
                label    = mm_below_class(mdf_row)
            else:
                z_max, z_min, pt_max, pt_min = corners
                geometry = curve_enters_rectangle(formulas, z_max, z_min, pt_max, pt_min)
                label    = mm_below_class(mdf_row)
            class_rows.append({
                "q2y_bin": q2y,
                "zpt_bin": zpt,
                "bin_role": "skipped" if(zpt not in kept) else "retained",
                "below_threshold_class": label,
                "geometric_curve": geometry,
                "mdf_percent_below": "" if(mdf_row is None) else mdf_row.get("percent_below", ""),
                "mdf_percent_rejected": "" if(mdf_row is None) else mdf_row.get("percent_rejected", ""),
                "mdf_subset_status": "" if(mdf_row is None) else mdf_row.get("subset_status", ""),
                "mdf_n_below": "" if(mdf_row is None) else mdf_row.get("n_below", ""),
                "mdf_n_total": "" if(mdf_row is None) else mdf_row.get("n_total", ""),
                "mdf_n_rejected": "" if(mdf_row is None) else mdf_row.get("n_rejected", ""),
                "mdf_n_nominal_below": "" if(mdf_row is None) else mdf_row.get("n_nominal_below", ""),
                "rdf_percent_below": "" if(rdf_row is None) else rdf_row.get("percent_below", ""),
                "rdf_percent_rejected": "" if(rdf_row is None) else rdf_row.get("percent_rejected", ""),
                "rdf_subset_status": "" if(rdf_row is None) else rdf_row.get("subset_status", ""),
                "rdf_n_below": "" if(rdf_row is None) else rdf_row.get("n_below", ""),
                "rdf_n_total": "" if(rdf_row is None) else rdf_row.get("n_total", ""),
                "gen_percent_below": "" if(gen_row is None) else gen_row.get("percent_below", ""),
                "gen_n_below": "" if(gen_row is None) else gen_row.get("n_below", ""),
                "gen_n_total": "" if(gen_row is None) else gen_row.get("n_total", ""),
            })
            if(zpt not in kept):
                continue
            data_hist = hist_maps["rdf_mm_none"][q2y].get(zpt)
            mc_hist   = hist_maps["mdf_mm_none"][q2y].get(zpt)
            tv_full, tv_below, tv_shape, abs_diff = ("", "", "", "")
            shape_status = "missing"
            if((data_hist is not None) and (mc_hist is not None) and (rdf_row["sample_status"] == "ok") and (mdf_row["sample_status"] == "ok")):
                tv_full, tv_below, tv_shape, abs_diff = shape_distance(data_hist, mc_hist)
                shape_status = "ok"
            shape_rows.append({
                "q2y_bin": q2y, "zpt_bin": zpt, "shape_status": shape_status,
                "rdf_percent_below": rdf_row.get("percent_below", ""),
                "mdf_percent_below": mdf_row.get("percent_below", ""),
                "abs_diff_percent_below": abs_diff,
                "tv_full": tv_full,
                "tv_below_contribution": tv_below,
                "tv_below_shape": tv_shape,
            })
    write_mm_csv(os.path.join(csv_dir, "mm_bin_classification.csv"), class_rows, list(class_rows[0].keys()))
    write_mm_csv(os.path.join(csv_dir, "mm_shape_comparison.csv"), shape_rows, list(shape_rows[0].keys()))
    log("wrote classification and shape tables")
    for source in MM_SOURCE_ORDER:
        for q2y in q2y_bins:
            kept, rows, cols = rows_of[q2y]
            path = os.path.join(pdf_dir, "MM_%s_Q2y_%02d.pdf" % (source, q2y))
            log("drawing %s" % path)
            draw_mm_q2y_canvas(path, q2y, rows, cols, row_maps[source][q2y], hist_maps[source][q2y])
        overview = os.path.join(pdf_dir, "MM_%s_overview.pdf" % source)
        log("drawing %s" % overview)
        draw_mm_overview(overview, q2y_bins, rows_of, row_maps[source], hist_maps[source])
    for q2y in q2y_bins:
        kept, rows, cols = rows_of[q2y]
        path = os.path.join(pdf_dir, "MM_overlay_norm_Q2y_%02d.pdf" % q2y)
        log("drawing %s" % path)
        draw_overlay_q2y(path, q2y, rows, cols, row_maps["rdf_mm_none"][q2y], row_maps["mdf_mm_none"][q2y], hist_maps["rdf_mm_none"][q2y], hist_maps["mdf_mm_none"][q2y])
    overlay_overview = os.path.join(pdf_dir, "MM_overlay_norm_overview.pdf")
    log("drawing %s" % overlay_overview)
    draw_overlay_overview(overlay_overview, q2y_bins, rows_of, row_maps["rdf_mm_none"], row_maps["mdf_mm_none"], hist_maps["rdf_mm_none"], hist_maps["mdf_mm_none"])
    counts = {}
    for row in class_rows:
        if(row["bin_role"] != "retained"):
            continue
        label = row["below_threshold_class"]
        counts[label] = counts.get(label, 0) + 1
    subset_pass = 0
    subset_fail = 0
    for row in detail_rows:
        if(row.get("source") != "mdf_mm_none"):
            continue
        if(row.get("subset_status") == "pass"):
            subset_pass += 1
        elif(row.get("subset_status") == "fail"):
            subset_fail += 1
    log("retained class counts %s" % counts)
    log("mdf subset pass %s fail %s" % (subset_pass, subset_fail))
    log_handle = open(log_path, "w")
    log_handle.write("\n".join(log_lines) + "\n")
    log_handle.close()
    log("log %s" % log_path)


def load_mm_rejection(csv_path):
    rows = list(csv.DictReader(open(csv_path)))
    kept = {}
    for row in rows:
        if(row["bin_role"] != "retained"):
            continue
        key = (int(row["q2y_bin"]), int(row["zpt_bin"]))
        kept[key] = row
    return kept


def mm_weighted_removal(rows, prefix):
    rejected = 0.0
    total    = 0.0
    for row in rows:
        count = float(row["%s_n_total" % prefix])
        total += count
        rejected += float(row["%s_percent_rejected" % prefix]) / 100.0 * count
    if(total <= 0):
        return 0.0
    return 100.0 * rejected / total


def prepare_mm_spectrum(hist, line_color, title):
    shown = hist.Clone("%s_show" % hist.GetName())
    shown.SetDirectory(0)
    shown.SetLineColor(line_color)
    shown.SetLineWidth(1)
    shown.SetFillStyle(0)
    shown.SetMarkerSize(0)
    shown.SetStats(0)
    shown.SetTitle(title)
    shown.GetXaxis().SetTitle("M_{X} [GeV]")
    shown.GetYaxis().SetTitle("Counts")
    shown.GetYaxis().SetTitleOffset(1.05)
    shown.GetXaxis().SetTitleOffset(1.0)
    ymax = shown.GetMaximum()
    if(ymax <= 0.0):
        ymax = 1.0
    shown.GetYaxis().SetRangeUser(0.0, 1.2 * ymax)
    return shown, 1.2 * ymax


def draw_mm_cut_marker(ymax):
    cut_line = ROOT.TLine(MM_THRESHOLD, 0.0, MM_THRESHOLD, ymax)
    cut_line.SetLineColor(ROOT.kBlack)
    cut_line.SetLineStyle(2)
    cut_line.SetLineWidth(2)
    cut_line.Draw("same")
    return cut_line


def draw_mm_removal_box(pad, heading, percent):
    pad.cd()
    pad.SetFillColor(ROOT.kWhite)
    box = ROOT.TPaveText(0.05, 0.05, 0.95, 0.95, "NDC")
    box.SetFillColor(0)
    box.SetBorderSize(1)
    box.SetFillStyle(1001)
    box.SetTextAlign(22)
    box.SetTextFont(62)
    box.SetTextSize(0.025)
    box.SetMargin(0.02)
    box.AddText("#scale[2.2]{%s}" % heading)
    box.AddText("#scale[3.0]{#splitline{Events removed by M_{X} cut:}{%.3f%%}}" % float(percent))
    box.AddText("#scale[1.8]{#splitline{Event-weighted average}{over retained bins}}")
    box.Draw()
    return box


def draw_mm_sample_legend(pad, sample_entry, line_color):
    pad.cd()
    pad.SetFillColor(ROOT.kWhite)
    legend = ROOT.TLegend(0.05, 0.08, 0.95, 0.92, "", "NDC")
    legend.SetNColumns(1)
    legend.SetBorderSize(1)
    legend.SetFillStyle(1001)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    legend.SetTextSize(0.075)
    proxy = ROOT.TH1D("mm_leg_%s" % id(pad), "", 1, 0.0, 1.0)
    proxy.SetDirectory(0)
    proxy.SetLineColor(line_color)
    proxy.SetLineWidth(4)
    legend.AddEntry(proxy, "#scale[0.85]{%s}" % sample_entry, "l")
    marker = ROOT.TH1D("mm_thr_%s" % id(pad), "", 1, 0.0, 1.0)
    marker.SetDirectory(0)
    marker.SetLineColor(ROOT.kBlack)
    marker.SetLineStyle(2)
    marker.SetLineWidth(3)
    legend.AddEntry(marker, "#scale[0.85]{#splitline{M_{X} = 1.8 GeV}{threshold}}", "l")
    legend.Draw()
    return [legend, proxy, marker]


def configure_mm_summary_strip(side_pad):
    # Same left-strip division as phi_h_1D_Compare_in_z_pT_Images_Together.
    side_pad.SetFillColor(ROOT.kWhite)
    side_pad.SetPad(0.005, 0.015, 0.27, 0.985)
    side_pad.Divide(1, 2, 0, 0)
    upper = side_pad.cd(1)
    upper.SetPad(0.0, 0.425, 1.0, 1.0)
    upper.Divide(1, 2, 0.001, 0.001)
    lower = side_pad.cd(2)
    lower.SetPad(0.0, 0.0, 1.0, 0.42)
    lower.Divide(1, 1, 0, 0)
    lower.cd(1).SetPad(0.035, 0.025, 0.95, 0.975)
    return upper, lower


def draw_thesis_mm_mosaics(args):
    # Consolidated missing-mass figures in the Figure 5.5 pad geometry.
    # The per-bin spectrum, the 1.8 GeV marker, and the integrated spectra are drawn.
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadGridX(0)
    ROOT.gStyle.SetPadGridY(0)
    old_line_scale = ROOT.gStyle.GetLineScalePS()
    csv_path  = args.missing_mass_csv if(args.missing_mass_csv not in ["", None]) else os.path.join(MM_REVIEW, "phase1_1d/csv/mm_bin_classification.csv")
    root_path = args.missing_mass_root if(args.missing_mass_root not in ["", None]) else MM_ROOT_DEFAULT
    rejection = load_mm_rejection(csv_path)
    handle = open_root(root_path)
    loaded = {}
    for tag in ["rdf_mm_none", "mdf_mm_none"]:
        hist = take(handle, MM_KEY[tag])
        if(hist is None):
            raise RuntimeError("missing %s" % tag)
        loaded[tag] = hist
    outputs = [
        ("rdf", "rdf_mm_none", ROOT.kBlue, os.path.join(THESIS, "Experiment/Data_Collection_Images/Kinematic_Binning/MM_Data/MM_rdf_all_Q2y.pdf"), "#splitline{Experimental data}{Before the M_{X} cut}"),
        ("mdf", "mdf_mm_none", ROOT.kRed, os.path.join(THESIS, "Monte_Carlo/Data_MC_Images/MM_Reconstructed/MM_mdf_all_Q2y.pdf"), "#splitline{Reconstructed clasdis}{Before the M_{X} cut}"),
    ]
    if(args.missing_mass_output not in ["", None]):
        outputs = [
            ("rdf", "rdf_mm_none", ROOT.kBlue, os.path.join(args.missing_mass_output, "MM_rdf_all_Q2y.pdf"), "#splitline{Experimental data}{Before the M_{X} cut}"),
            ("mdf", "mdf_mm_none", ROOT.kRed, os.path.join(args.missing_mass_output, "MM_mdf_all_Q2y.pdf"), "#splitline{Reconstructed clasdis}{Before the M_{X} cut}"),
        ]
    for prefix, hist_tag, line_color, destination, sample_entry in outputs:
        alive = []
        canvas = Canvas_Create("mm_thesis_%s" % prefix, 2, 1, int(1800 * 8), int(1500 * 10), 0.01)
        canvas.SetFillColor(ROOT.kWhite)
        alive.append(canvas)
        left = canvas.cd(1)
        left_upper, left_lower = configure_mm_summary_strip(left)
        right = canvas.cd(2)
        right.SetPad(0.28, 0.015, 0.995, 0.9975)
        right.SetFillColor(ROOT.kWhite)
        right.Divide(4, 5, 0.0001, 0.0001)
        all_rows = []
        summed = None
        drawn_total = 0
        for q2y in range(1, 18):
            kept, rows, cols = retained_bins(q2y)
            q2y_rows = [rejection[(q2y, zpt)] for zpt in kept]
            all_rows.extend(q2y_rows)
            panel = right.cd(Q2Y_PAD[q2y])
            panel.SetFillColor(ROOT.kWhite)
            panel.Divide(2, 1, 0.01, 0.01)
            side_upper, side_lower = configure_mm_summary_strip(panel.cd(1))
            grid = panel.cd(2)
            grid.SetPad(0.28, 0.015, 0.995, 0.9975)
            grid.SetFillColor(ROOT.kWhite)
            grid.Divide(cols, rows, 0.0001, 0.0001)
            q2y_sum = None
            drawn_count = 0
            for zpt in range(1, rows * cols + 1):
                pad = grid.cd(zpt)
                pad.SetFillColor(ROOT.kWhite)
                pad.SetFrameFillColor(ROOT.kWhite)
                if(zpt not in kept):
                    continue
                proj = project_mm_cell(loaded[hist_tag], q2y, zpt, hist_tag)
                percent = float(rejection[(q2y, zpt)]["%s_percent_rejected" % prefix])
                title = "#splitline{z-P_{T} bin %d}{#scale[4]{#splitline{Events removed by M_{X} cut:}{%.3f%%}}}" % (zpt, percent)
                shown, ymax = prepare_mm_spectrum(proj, line_color, title)
                pad.Divide(1, 1, 0, 0)
                Draw_Canvas(pad, 1, 0.15)
                inner = pad.cd(1)
                inner.SetFillColor(ROOT.kWhite)
                inner.SetFrameFillColor(ROOT.kWhite)
                shown.Draw("hist")
                alive.append(shown)
                alive.append(draw_mm_cut_marker(ymax))
                alive.append(proj)
                drawn_count += 1
                if(q2y_sum is None):
                    q2y_sum = proj.Clone("q2ysum_%s_%s" % (prefix, q2y))
                    q2y_sum.SetDirectory(0)
                else:
                    q2y_sum.Add(proj)
            if(drawn_count != len(kept)):
                raise RuntimeError("Q2-y %s drew %s histograms, expected %s" % (q2y, drawn_count, len(kept)))
            drawn_total += drawn_count
            average = mm_weighted_removal(q2y_rows, prefix)
            integrated, iymax = prepare_mm_spectrum(q2y_sum, line_color, "#splitline{M_{X} Distribution}{Q^{2}-y Bin %d}" % q2y)
            integrated.GetYaxis().SetTitleSize(0.055)
            integrated.GetYaxis().SetLabelSize(0.045)
            integrated.GetYaxis().SetTitleOffset(1.35)
            integrated.GetXaxis().SetTitleSize(0.055)
            integrated.GetXaxis().SetLabelSize(0.045)
            integ_pad = side_upper.cd(1)
            integ_pad.cd()
            integ_pad.SetLeftMargin(0.22)
            integ_pad.SetRightMargin(0.05)
            integ_pad.SetTopMargin(0.18)
            integ_pad.SetBottomMargin(0.16)
            integrated.Draw("hist")
            alive.append(integrated)
            alive.append(draw_mm_cut_marker(iymax))
            alive.append(draw_mm_removal_box(side_upper.cd(2), "Q^{2}-y Bin %d" % q2y, average))
            alive.extend(draw_mm_sample_legend(side_lower.cd(1), sample_entry, line_color))
            alive.append(q2y_sum)
            if(summed is None):
                summed = q2y_sum.Clone("allsum_%s" % prefix)
                summed.SetDirectory(0)
            else:
                summed.Add(q2y_sum)
            print("  q2y %s average %.6f histograms %s" % (q2y, average, drawn_count))
        if(drawn_total != 452):
            raise RuntimeError("drew %s histograms, expected 452" % drawn_total)
        overall = mm_weighted_removal(all_rows, prefix)
        full_hist, fymax = prepare_mm_spectrum(summed, line_color, "#splitline{M_{X} Distribution}{Q^{2}-y Bin All}")
        full_hist.GetYaxis().SetTitleSize(0.055)
        full_hist.GetYaxis().SetLabelSize(0.045)
        full_hist.GetYaxis().SetTitleOffset(1.35)
        full_hist.GetXaxis().SetTitleSize(0.055)
        full_hist.GetXaxis().SetLabelSize(0.045)
        full_pad = left_upper.cd(1)
        full_pad.cd()
        full_pad.SetLeftMargin(0.22)
        full_pad.SetRightMargin(0.05)
        full_pad.SetTopMargin(0.18)
        full_pad.SetBottomMargin(0.16)
        full_hist.Draw("hist")
        alive.append(full_hist)
        alive.append(draw_mm_cut_marker(fymax))
        alive.append(summed)
        alive.append(draw_mm_removal_box(left_upper.cd(2), "Q^{2}-y Bin All", overall))
        alive.extend(draw_mm_sample_legend(left_lower.cd(1), sample_entry, line_color))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        canvas.SetCanvasSize(145000, 152000)
        ROOT.gStyle.SetLineScalePS(0.75)
        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(destination)
        print("mosaic %s average %.6f histograms %s -> %s" % (prefix, overall, drawn_total, destination))
        canvas.Clear()
        alive.clear()
    ROOT.gStyle.SetLineScalePS(old_line_scale)
    ROOT.gStyle.SetPadGridX(1)
    ROOT.gStyle.SetPadGridY(1)


def selected_families(args):
    if(len(args.family) > 0):
        return list(args.family)
    return list(FAMILIES)


def main():
    args = parse_args()
    if(args.missing_mass_consolidated):
        draw_thesis_mm_mosaics(args)
        for handle in OPEN_FILES.values():
            handle.Close()
        return
    if(args.missing_mass_study):
        run_missing_mass_study(args)
        for handle in OPEN_FILES.values():
            handle.Close()
        return
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
        pdf_out = info["pdf"] if(info.get("pdf_written")) else ""
        print("STATUS family=%s thesis_ready=%s pdf=%s na=%s drawn=%s reason=%s" % (family, "yes" if(info["thesis_ready"]) else "no", pdf_out, info.get("na_count", 0), info.get("drawn", 0), info["reason"]))
    for handle in OPEN_FILES.values():
        handle.Close()


if(__name__ == "__main__"):
    main()
