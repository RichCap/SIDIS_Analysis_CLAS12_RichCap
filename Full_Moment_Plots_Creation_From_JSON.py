#!/usr/bin/env python3

import os
import sys
import re
import json
import argparse
import pickle
import numpy as np
import ROOT
# import traceback
# # traceback.format_exc()

ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)

# Grid styling (requested: avoid blank white background)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)
# ────── Readability fixes for y-axis + title
# ROOT.gStyle.SetLabelSize(0.18,  "y")      # bigger, easier to read
# ROOT.gStyle.SetLabelSize(0.038, "y")      # bigger, easier to read
ROOT.gStyle.SetLabelFont(62, "y")         # Helvetica bold → looks "thicker"
ROOT.gStyle.SetTitleX(0.58)
ROOT.gStyle.SetTitleFont(62)              # bold title too
# ROOT.gStyle.SetLabelSize(0.15,  "x")      # optional but nice for x-axis
# ROOT.gStyle.SetLabelSize(0.035, "x")      # optional but nice for x-axis


universal_directory = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/' if(os.path.exists('/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis')) else '/Users/richardcapobianco/Desktop/Work_Offline.nosync/'
# ------------------------------------------------------------
# User-provided plotting/binning utilities (incorporated directly)
# ------------------------------------------------------------
import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis' if(os.path.exists('/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis')) else '/Users/richardcapobianco/Desktop/Work_Offline.nosync/General_Helper_Scripts'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, RuntimeTimer, Get_Num_of_z_pT_Rows_and_Columns, skip_condition_z_pT_bins
from Binning_Dictionaries             import Full_Bin_Definition_Array
from Cross_Section_Normalization      import Cross_Section_Normalization
sys.path.remove(script_dir)
del script_dir

color_mapper  = {"1": ROOT.kRed, "2": ROOT.kBlue, "3": ROOT.kMagenta, "4": ROOT.kGreen, "5": ROOT.kOrange+3, "6": ROOT.kAzure+10, "7": ROOT.kOrange}
marker_mapper = {"1": ROOT.kFullDotLarge, "2": ROOT.kFullSquare, "3": ROOT.kFullTriangleUp, "4": ROOT.kFullTriangleDown, "5": ROOT.kFullDiamond, "6": ROOT.kFullCrossX, "7": ROOT.kFullThreeTriangles}

def Construct_JSON_Info(Q2_y_Bin, z_pT_Bin, return_info={}):
    key = f"(Q2_y_Bin_{Q2_y_Bin})-(z_pT_Bin_{z_pT_Bin})"
    if(all(str(bins) not in ["0", "-1", "All"] for bins in [Q2_y_Bin, z_pT_Bin])):
        _, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=int(Q2_y_Bin))
        pT_group  = ((int(z_pT_Bin)-1)%number_of_cols) + 1
        z__group  = int((int(z_pT_Bin) - 1)/number_of_cols) + 1
        pT_color  = color_mapper[str(pT_group)]
        z__color  = color_mapper[str(z__group)]
        pT_marker = marker_mapper[str(pT_group)]
        z__marker = marker_mapper[str(z__group)]
        Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f"Q2-y={Q2_y_Bin}, Q2-y"]
        z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[f"Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}"]
        Q2val = (Q2_max + Q2_min)/2
        y_val = (y_max  +  y_min)/2
        z_val = (z_max  +  z_min)/2
        pTval = (pT_max + pT_min)/2
        Q2range = [Q2val, Q2_min, Q2_max]
        y_range = [y_val,  y_min,  y_max]
        z_range = [z_val,  z_min,  z_max]
        pTrange = [pTval, pT_min, pT_max]
        return_info[key] = {"pT_group": pT_group, "z__group": z__group, "pT_color": pT_color, "z__color": z__color, "pT_marker": pT_marker, "z__marker": z__marker, "Q2range": Q2range, "y_range": y_range, "z_range": z_range, "pTrange": pTrange}
    else:
        return return_info

# ------------------------------------------------------------
# Argparse
# ------------------------------------------------------------
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def parse_args():
    p = argparse.ArgumentParser(description="Make slide-optimized mosaic plots from the fit-parameter JSON output.", formatter_class=RawDefaultsHelpFormatter)

    p.add_argument("-err", "--err_suffix",
                   default="_ERR",
                   help="Error key suffix (e.g. Fit_Par_B + _ERR -> Fit_Par_B_ERR).\n")

    p.add_argument("-q", "--q2y_count",
                   type=int,
                   default=17,
                   # help="Number of Q2-y bins in the mosaic layout.\n")
                   help=argparse.SUPPRESS)
    p.add_argument("-R", "--layout_rows",
                   default="4,4,4,3,2",
                   # help="Comma-separated pads per row from bottom->top (ragged, right-aligned).\n"
                   help=argparse.SUPPRESS)

    p.add_argument("-X", "--global_x_range",
                   nargs=2,
                   type=float,
                   default=None,
                   # help="Override global X range: XMIN XMAX.\n")
                   help=argparse.SUPPRESS)
    
    p.add_argument("-m", "--y_range_mode",
                   choices=["global", "auto"],
                   default="global",
                   help="Y range policy: 'global' shared across pads (default), or 'auto' per-pad tight range.\n")
    
    p.add_argument("-Y", "--global_y_range",
                   nargs=2,
                   type=float,
                   default=None,
                   help="Override global Y range: YMIN YMAX (applies when y_range_mode='global').\n")

    p.add_argument("-g", "--grid",
                   action="store_true",
                   help="Enable pad grid.\n")

    p.add_argument("-l", "--label_mode",
                   choices=["outer", "all"],
                   default="outer",
                   # help="Tick label policy: 'outer' shows labels only on outer pads, 'all' shows labels on every pad.\n")
                   help=argparse.SUPPRESS)

    # Centered per-pad labels + slightly smaller default (requested)
    p.add_argument("-K", "--pad_label_size",
                   type=float,
                   default=0.070,
                   # help="Per-pad label TLatex size (NDC).\n")
                   help=argparse.SUPPRESS)
    p.add_argument("-a", "--pad_label_x",
                   type=float,
                   default=0.50,
                   # help="Per-pad label X position (NDC).\n")
                   help=argparse.SUPPRESS)
    p.add_argument("-A", "--pad_label_y",
                   type=float,
                   default=0.965,
                   # help="Per-pad label Y position (NDC).\n")
                   help=argparse.SUPPRESS)

    p.add_argument("-M", "--title_mode",
                   choices=["none", "auto", "text_only"],
                   default="auto",
                   # help="Global title policy: none, auto-built title, or text_only.\n")
                   help=argparse.SUPPRESS)
    p.add_argument("-fs", "--fit_set_label",
                   default="",
                   help="Optional friendly label for the fit_set (used in title). If blank, uses fit_set-derived default.\n")

    # Slightly smaller default title size (after increased canvas size)
    p.add_argument("-s", "--title_size",
                   type=float,
                   default=0.028,
                   # help="Global title TLatex size (NDC).\n")
                   help=argparse.SUPPRESS)

    p.add_argument("-p", "--title_x",
                   type=float,
                   default=0.01,
                   # help="Global title X position (NDC).\n")
                   help=argparse.SUPPRESS)
    p.add_argument("-P", "--title_y",
                   type=float,
                   default=0.99,
                   # help="Global title Y position (NDC).\n")
                   help=argparse.SUPPRESS)


    p.add_argument("-W", "--canvas_width",
                   type=int,
                   # default=2800,
                   default=2800,
                   help="Canvas width in pixels.\n")
    p.add_argument("-H", "--canvas_height",
                   type=int,
                   # default=3400,
                   default=3200,
                   help="Canvas height in pixels.\n")
    
    p.add_argument("-b", "--frame_line_width",
                   type=int,
                   default=3,
                   help="Bold frame/border thickness for each pad.\n")

    p.add_argument("-T", "--title_text",
                   default="",
                   help="Optional extra title text to include in the global title.\n")

    p.add_argument("-leg", "--draw_legends",
                   action="store_true",
                   help="Draw per-pad text-only legends for the variable not used on the x-axis.\n")
    p.add_argument("-tsl", "--toggle_source_legend",
                   action="store_true",
                   help="Toggle the canvas-level source/style legend. In comparison-overlay mode it is on by default (flag turns it off). In other modes it is off by default (flag turns it on, e.g. data vs spline). Does not affect per-pad bin legends.\n")

    p.add_argument("-t", "--test",
                   action="store_true",
                   help="Parse JSON, build point maps, and print summaries; do not write output files.\n")
    p.add_argument("-v", "--verbose",
                   action="store_true",
                   help="Verbose logging.\n")

    p.add_argument("-n", "--name",
                   default="Mosaic_Image",
                   help="Filename prefix for outputs written to the current directory.\n")
    p.add_argument("-F", "--formats",
                   choices=["png", "pdf"],
                   default="png",
                   help="Output format (png or pdf). Re-run the script if you want the other format too.\n")
    
    p.add_argument("-js", "-json", "--json_file",
                   nargs="+",
                   default=["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Appended_in_Parallel_Fixed_RC_Factor_Normalization_Full.json"],
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Final_File_Before_the_Collaboration_Meeting.json",
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_New_File_with_BC.json",
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_NEW_FULL_Normalization_AND_FULL_Fits.json",
                   help="Input JSON file(s) produced by your fit workflow. Multiple files are used with --comparison_mode (pairing rules apply).\n")

    p.add_argument("-L", "--list_fit_sets",
                   action="store_true",
                   help="List available fit-set keys in the JSON and exit.\n")
    p.add_argument("-f", "--fit_set",
                   nargs="+",
                   # default="Fit_Pars_from_3D_Bayesian",
                   default=["Fit_Pars_from_3D_BC_RC_Bayesian"],
                   help="Top-level JSON key(s) to use. Multiple keys are used with --comparison_mode.\n")

    p.add_argument("-cm", "--comparison_mode",
                   action="store_true",
                   help="Enable multi-fit_set / multi-JSON comparison workflow (plot overlay, pairwise differences, and/or tables).\n")
    p.add_argument("-om", "--output_mode",
                   choices=["plot", "table", "both"],
                   default="plot",
                   help="Comparison output: 'plot' (images only, default), 'table' (txt tables only), or 'both'. Ignored unless --comparison_mode is set.\n")
    p.add_argument("-ct", "--comparison_types",
                   nargs="+",
                   choices=["overlay", "delta", "diff", "percent_dif"],
                   default=["overlay"],
                   help="Comparison types with --comparison_mode: overlay (all series together); delta = |v1-v2|; diff = v1-v2; percent_dif = 100*(v1-v2)/v2. Errors: independent propagation — delta/diff use sqrt(e1^2+e2^2); percent_dif uses 100*sqrt((e1/v2)^2+(v1*e2/v2^2)^2).\n")
    p.add_argument("-lad", "--log_abs_diff",
                   action="store_true",
                   help="Use logarithmic Y-axis for absolute-difference (delta) comparison plots only. Default remains linear. Not applied to signed diff, percent_dif, or overlay.\n")

    p.add_argument("-y", "--y_pars",
                   nargs="+",
                   default=["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"],
                   help="Fit parameters to plot (each produces a separate mosaic canvas).\n")
    
    p.add_argument("-x", "--x_mode",
                   choices=["z", "pt", "pT", "Q2", "q2", "y", "xB", "xb"],
                   default="z",
                   help=f"Choose X axis: 'z' plots vs z center, 'pt'/'pT' plots vs pT center, etc.\n{color.RED}'Q2'/'q2', 'y', and 'xB'/'xb' all only work with the '--Spline_Only' images (as of 4/17/2026).{color.END}\n")

    p.add_argument("-k", "--pad_label_mode",
                   choices=["none", "bin", "bin_Q2", "bin_Q2y", "Q2y_only"],
                   default="Q2y_only",
                   help="Per-pad label: none, bin only, bin+Q2 range, bin+Q2+y ranges, or just the Q2+y ranges.\n")

    p.add_argument("-sb", "--single_bin",
                   action="store_true",
                   help="Draw a single Q2-y bin as a standalone plot (does not modify mosaic generation).\n")
    p.add_argument("-qb", "--single_q2y_bin",
                   type=int,
                   default=1,
                   help="Q2-y bin number to draw when --single_bin is enabled.\n")
    p.add_argument("-SW", "--single_canvas_width",
                   type=int,
                   default=1200,
                   help="Single-bin canvas width in pixels.\n")
    p.add_argument("-SH", "--single_canvas_height",
                   type=int,
                   default=1100,
                   help="Single-bin canvas height in pixels.\n")
    p.add_argument("-wm", "--draw_preliminary_watermark",
                   action="store_true",
                   help="Draw a faint diagonal 'PRELIMINARY' watermark on single-bin outputs.\n")

    p.add_argument("-cs", "-cs_A", "--apply_A_corr",
                   action="store_true",
                   help=f"Apply Cross Section Normalization to the 'Fit_Par_A' measurements.\n{color.Error}WARNING: Do not run with the '_(Normalized)' Fit Sets{color.END}.\n")
    p.add_argument("-nabc", "--no_apply_beam_corrections",
                   action="store_true",
                   help="Disable Klimenko tracking-efficiency and beam-blocker charge corrections inside Cross_Section_Normalization (default: corrections ON).\n")

    p.add_argument("-log", "--draw_with_log_A",
                   action="store_true",
                   help="Draw Fit_Par_A plots with a logarithmic y-axis (other parameters always use linear scale).\n")

    p.add_argument("-sp", "--spline_prefix",
                   type=str,
                   default=None,
                   help="Prefix used to load spline overlays: {spline_prefix}_{fit_set}_{y_par}.pkl.\n")
    
    p.add_argument("-dm", "--dimension_mode",
                   choices=["4D", "5D", "4D_xB"],
                   default="4D",
                   help="Spline dimensionality used when loading overlays:\n  4D     = Q², y, z, pT\n  5D     = Q², y, z, pT, xB\n  4D_xB  = xB, y, z, pT (Q² replaced)\n")

    p.add_argument("-ssr", "--show_spline_range",
                   action="store_true",
                   help="With --spline_prefix: also draw transparent filled bands around each series showing either fit-parameter limits or phase-space spline min/max ranges.\n")
    p.add_argument("-ssrm", "--spline_range_mode",
                   choices=["fit_limits", "phase_space"],
                   default="fit_limits",
                   help="Source of the shaded spline-range bands when --show_spline_range is set:\n  fit_limits   = B_limits/C_limits from Phi_h_Fit_Parameters_from_Spline.py (B/C only; A skipped)\n  phase_space  = min/max of the spline over a Q2×y×(z|pT) grid within each bin (A/B/C)\n")
    p.add_argument("-ssrn", "--spline_range_scan_n",
                   type=int,
                   default=6,
                   help="For --spline_range_mode phase_space: number of sample points per free kinematic variable (default 6 → 6^3=216 evaluations per data point).\n")

    p.add_argument("-xe", "--x_error_bars",
                   action="store_true",
                   help="Replace connecting lines between points with x-error bars sized to a fraction of the x-bin width.\n")
    p.add_argument("-xf", "--x_error_fraction",
                   type=float,
                   default=(1.0/3.0),
                   help="Fraction of the x-variable bin width to use for the FULL x-error-bar length (ex = 0.5*fraction*bin_width).\n")
    
    p.add_argument("-so", "--Spline_Only",
                   action="store_true",
                   help="Create Plots of just the Spline Fit Functions.\n")
    p.add_argument("-fq2", "-fQ2", "--Fixed_Q2",
                   nargs="+",
                   default=[2.2],
                   help="Fixed Q2 kinematics for the '--Spline_Only' Image Option.\n")
    p.add_argument("-fy", "--Fixed_y",
                   nargs="+",
                   default=[0.7],
                   help="Fixed y kinematics for the '--Spline_Only' Image Option.\n")
    p.add_argument("-fz", "--Fixed_z",
                   nargs="+",
                   default=[0.555],
                   help="Fixed z kinematics for the '--Spline_Only' Image Option.\n")
    p.add_argument("-fpt", "-fpT", "--Fixed_pT",
                   nargs="+",
                   default=[0.135],
                   help="Fixed pT kinematics for the '--Spline_Only' Image Option.\n")
    p.add_argument("-fxb", "-fxB", "--Fixed_xB",
                   nargs="+",
                   default=None,
                   help=f"Fixed xB kinematics for the '--Spline_Only' Image Option.\n{color.RED}Note: Will replace either the 'Fixed_Q2' or 'Fixed_y'.{color.END}\n")
    
    return p.parse_args()

# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------
def use_log_y_for_par(args, y_par):
    return bool(getattr(args, "draw_with_log_A", False)) and (str(y_par) == "Fit_Par_A")

def ensure_positive_y_range_for_log(ymin, ymax):
    # ROOT log y-axes require ymin > 0. Adjust only when needed for log scale.
    ymin = float(ymin)
    ymax = float(ymax)
    if(ymin > 0.0):
        return ymin, ymax
    if(ymax > 0.0):
        return max(ymax * 1e-4, 1e-12), ymax
    # Both non-positive: give ROOT a tiny valid log window so drawing does not immediately fail
    return 1e-12, 1.0

def load_json(args, json_index=0):
    # --json_file may be a path string or a list (nargs="+"); json_index selects which list entry to load
    if(isinstance(args.json_file, (list, tuple))):
        if(len(args.json_file) == 0):
            raise SystemExit(f"{color.Error}ERROR: --json_file list is empty.{color.END}")
        if((json_index < 0) or (json_index >= len(args.json_file))):
            raise SystemExit(f"{color.Error}ERROR: json_index={json_index} out of range for --json_file (len={len(args.json_file)}).{color.END}")
        path = str(args.json_file[json_index])
    else:
        path = str(args.json_file)
    if(not os.path.isfile(path)):
        raise SystemExit(f"{color.Error}ERROR: JSON file not found:{color.END_R} {path}{color.END}")
    with open(path, "r") as handle:
        return json.load(handle)

def list_fit_sets(json_obj):
    keys = []
    for kk in json_obj.keys():
        keys.append(str(kk))
    keys.sort()
    return keys

def select_default_fit_set(json_obj):
    candidates = []
    for kk, vv in json_obj.items():
        if(str(kk) == "Meta_Data_of_Last_Run"):
            continue
        if(isinstance(vv, dict) and (len(vv) > 0)):
            candidates.append(str(kk))
    if(len(candidates) == 0):
        return ""
    normalized = [cc for cc in candidates if("(Normalized)" in cc)]
    if(len(normalized) > 0):
        normalized.sort()
        return normalized[0]
    candidates.sort()
    return candidates[0]

def sanitize_for_filename(text_in):
    txt = str(text_in)
    txt = re.sub(r"\s+", "_", txt)
    txt = re.sub(r"[^A-Za-z0-9_]+", "_", txt)
    txt = re.sub(r"_+", "_", txt)
    txt = txt.strip("_")
    return txt

def parse_inner_key(key_str):
    mm = re.fullmatch(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", str(key_str).strip())
    if(mm is None):
        raise ValueError(f"Key '{key_str}' does not match '(Q2_y_Bin_#)-(z_pT_Bin_#)'")
    return int(mm.group(1)), int(mm.group(2))

def parse_layout_rows(layout_rows_str):
    rows = []
    for tok in str(layout_rows_str).split(","):
        tt = tok.strip()
        if(tt != ""):
            rows.append(int(tt))
    if(len(rows) == 0):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} --layout_rows parsed to an empty list.{color.END}")
    if(any([(rr <= 0) for rr in rows])):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} --layout_rows contains non-positive values: {rows}{color.END}")
    return rows

def build_layout_map(args):
    layout_rows = parse_layout_rows(args.layout_rows)
    max_cols = max(layout_rows)
    nrows    = len(layout_rows)
    mapping  = {}
    bin_num  = 1
    for row in range(nrows):
        ncol = layout_rows[row]
        col_start = max_cols - ncol
        for ii in range(ncol):
            col = (max_cols - 1) - ii
            if(bin_num > args.q2y_count):
                break
            mapping[bin_num] = (row, col, col_start)
            bin_num += 1
        if(bin_num > args.q2y_count):
            break
    return mapping, max_cols, nrows

def pad_is_outer(row, col, col_start, max_cols, nrows):
    is_bottom            = (row == 0)
    is_top               = (row == (nrows - 1))
    is_leftmost_present  = (col == col_start)
    is_rightmost_present = (col == (max_cols - 1))
    return is_bottom, is_leftmost_present, is_rightmost_present, is_top

# ------------------------------------------------------------
# JSON -> binnings/styles (via Construct_JSON_Info) -> grouping
# ------------------------------------------------------------
def build_info_map(args, fit_dict):
    info_map = {}
    for key_str in fit_dict.keys():
        q2y_bin, zpt_bin = parse_inner_key(key_str)
        if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin, BINNING_METHOD="_Y_bin", Common_z_pT_Range_Q=False)):
            print(f"{color.Error}WARNING: MUST SKIP BIN {q2y_bin}-{zpt_bin}...{color.END}")
            continue
        Construct_JSON_Info(Q2_y_Bin=str(q2y_bin), z_pT_Bin=str(zpt_bin), return_info=info_map)
    if(args.verbose):
        print(f"{color.CYAN}[INFO] Built info_map entries: {len(info_map)}{color.END}")
    return info_map

def group_by_q2y(fit_dict):
    grouped = {}
    for key_str in fit_dict.keys():
        q2y_bin, zpt_bin = parse_inner_key(key_str)
        if(q2y_bin not in grouped):
            grouped[q2y_bin] = []
        if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin, BINNING_METHOD="_Y_bin", Common_z_pT_Range_Q=False)):
            print(f"{color.Error}WARNING: MUST SKIP BIN {q2y_bin}-{zpt_bin}...{color.END}")
            continue
        grouped[q2y_bin].append((zpt_bin, key_str))
    for q2y_bin in grouped.keys():
        grouped[q2y_bin].sort(key=lambda tt: tt[0])
    return grouped

def build_q2y_ranges(grouped, info_map):
    q2y_ranges = {}
    for q2y_bin in grouped.keys():
        first_key = ""
        for zpt_bin, key_str in grouped[q2y_bin]:
            if(key_str in info_map):
                first_key = key_str
                break
        if(first_key != ""):
            q2y_ranges[q2y_bin] = {"Q2range": info_map[first_key]["Q2range"], "y_range": info_map[first_key]["y_range"]}
    return q2y_ranges

def compute_global_x_range(args, grouped, info_map):
    xmin = None
    xmax = None
    for q2y_bin in grouped.keys():
        for zpt_bin, key_str in grouped[q2y_bin]:
            if(key_str not in info_map):
                continue
            xval = info_map[key_str]["z_range"][0] if(args.x_mode == "z") else info_map[key_str]["pTrange"][0]
            xval = float(xval)
            if((xmin is None) or (xval < xmin)):
                xmin = xval
            if((xmax is None) or (xval > xmax)):
                xmax = xval
    if((xmin is None) or (xmax is None)):
        return 0.0, 1.0
    if(xmin == xmax):
        return xmin - 1.0, xmax + 1.0
    pad = 0.06 * (xmax - xmin)
    return xmin - pad, xmax + pad

def compute_global_y_range(args, grouped, fit_dict, y_par, include_errors=True):
    # include_errors=False: axis from central values only (error bars still drawn from stored errs)
    ymin = None
    ymax = None
    err_key = f"{y_par}{args.err_suffix}"
    for q2y_bin in grouped.keys():
        for zpt_bin, key_str in grouped[q2y_bin]:
            if(key_str not in fit_dict):
                continue
            entry = fit_dict[key_str]
            if(y_par not in entry):
                continue
            if(include_errors and (err_key not in entry)):
                continue
            yv = float(entry[y_par])
            ye = float(entry[err_key]) if((include_errors) and (err_key in entry)) else 0.0
            if((getattr(args, "apply_A_corr", False)) and (y_par == "Fit_Par_A")):
                _, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y_bin, z_pT_Bin=zpt_bin, args_in=args)
                if((str(Bin_Width_Area_Scale) not in ["0", "None", None]) and (str(Luminosity) not in ["0", "None", None])):
                    yv = yv/(Bin_Width_Area_Scale*Luminosity)
                    ye = ye/(Bin_Width_Area_Scale*Luminosity)
            lo = yv - abs(ye) if(include_errors) else yv
            hi = yv + abs(ye) if(include_errors) else yv
            if((ymin is None) or (lo < ymin)):
                ymin = lo
            if((ymax is None) or (hi > ymax)):
                ymax = hi
    if((ymin is None) or (ymax is None)):
        print(f"\n{color.Error}WARNING (compute_global_y_range): ymin, ymax = {ymin}, {ymax}{color.END}\n")
        return 0.0, 1.0
    if(ymin == ymax):
        return ymin - 1.0, ymax + 1.0
    pad = 0.12 * (ymax - ymin)
    return ymin - pad, ymax + pad

def build_series_for_q2y(args, grouped, fit_dict, info_map, q2y_bin, y_par):
    series_map = {}
    err_key = f"{y_par}{args.err_suffix}"
    if(q2y_bin not in grouped):
        return series_map
    for zpt_bin, key_str in grouped[q2y_bin]:
        if((key_str not in fit_dict) or (key_str not in info_map)):
            continue
        entry = fit_dict[key_str]
        if((y_par not in entry) or (err_key not in entry)):
            continue
        inf  = info_map[key_str]
        xval = inf["z_range"][0] if(args.x_mode == "z") else inf["pTrange"][0]
        yval = float(entry[y_par])
        yerr = float(entry[err_key])
        if((getattr(args, "apply_A_corr", False)) and (y_par == "Fit_Par_A")):
            _, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y_bin, z_pT_Bin=zpt_bin, args_in=args)
            if((str(Bin_Width_Area_Scale) not in ["0", "None", None]) and (str(Luminosity) not in ["0", "None", None])):
                yval = yval/(Bin_Width_Area_Scale*Luminosity)
                yerr = yerr/(Bin_Width_Area_Scale*Luminosity)
        if(args.x_mode == "z"):
            series_id = str(inf["pT_group"])
            scolor    = inf["pT_color"]
            smarker   = inf["pT_marker"]
        else:
            series_id = str(inf["z__group"])
            scolor    = inf["z__color"]
            smarker   = inf["z__marker"]
        if(series_id not in series_map):
            series_map[series_id] = {"color": scolor, "marker": smarker, "points": []}
        series_map[series_id]["points"].append((float(xval), float(yval), float(yerr), key_str))
    for sid in series_map.keys():
        series_map[sid]["points"].sort(key=lambda tt: tt[0])
    return series_map

def Convert_xB_var(xB_in=None, Q2_in=None, y_in=None, Var_out="y"):
    Conversion_Factor = 0.0502731 # From xB = Q2/(2*M*E*y) -> Conversion_Factor = 1/(2*M*E)
    if(Var_out == "xB"):
        return (Conversion_Factor*(Q2_in/y_in))  if((None not in [Q2_in,  y_in]) and (y_in  != 0)) else xB_in
    if(Var_out == "y"):
        return (Conversion_Factor*(Q2_in/xB_in)) if((None not in [Q2_in, xB_in]) and (xB_in != 0)) else y_in
    if(Var_out == "Q2"):
        return ((xB_in*y_in)/Conversion_Factor)  if( None not in [xB_in,  y_in])                   else Q2_in
    return None

class ExpRBFWrapper:
    """Wrap an RBF fit on log(A) so evaluation returns Amplitude = exp(rbf(x))."""
    def __init__(self, rbf):
        self.rbf = rbf
    def __call__(self, x):
        return np.exp(np.asarray(self.rbf(x), dtype=float))

def load_spline_models(args, fit_set):
    spline_models = {}
    if(args.spline_prefix is None):
        return spline_models
    if(str(args.spline_prefix).strip() in ["", "None", "none"]):
        return spline_models
    for y_par in args.y_pars:
        # UPDATED: include dimension_mode in filename
        pkl_file = f"{args.spline_prefix}_{args.dimension_mode}_{fit_set}_{y_par}.pkl"
        if(not os.path.isfile(pkl_file)):
            if(not os.path.isfile(f"{universal_directory}Prepare_Next_Iteration/{pkl_file}")):
                print(f"{color.BYELLOW}[INFO] Missing spline file for {y_par}: {pkl_file}{color.END}")
                continue
            else:
                pkl_file = f"{universal_directory}Prepare_Next_Iteration/{pkl_file}"
        try:
            with open(pkl_file, "rb") as pklf:
                spline_obj = pickle.load(pklf)
        except Exception as ee:
            print(f"{color.Error}WARNING:{color.END_R} Failed to load spline file '{pkl_file}': {ee}{color.END}")
            continue
        log_space = False
        if(isinstance(spline_obj, dict)):
            cfg = spline_obj.get("config", {}) if(isinstance(spline_obj.get("config", {}), dict)) else {}
            log_space = bool(cfg.get("log_space", False))
            if("rbf" in spline_obj):
                spline_obj = spline_obj["rbf"]
            elif("spline" in spline_obj):
                spline_obj = spline_obj["spline"]
        if(spline_obj is None):
            continue
        if(log_space):
            spline_obj = ExpRBFWrapper(spline_obj)
        spline_models[y_par] = spline_obj
        if(args.verbose):
            print(f"{color.GREEN}[INFO] Loaded {args.dimension_mode} spline for {y_par}: {pkl_file}{color.END}")
    return spline_models

def build_spline_graph(args, spline_models, info_map, sid, series_map, y_par):
    if(y_par not in spline_models):
        return None
    if(sid not in series_map):
        return None
    pts = series_map[sid]["points"]
    if(len(pts) == 0):
        return None
    key0 = pts[0][3]
    if(key0 not in info_map):
        return None

    q2_center = float(info_map[key0]["Q2range"][0])
    y__center = float(info_map[key0]["y_range"][0])
    z__center = float(info_map[key0]["z_range"][0])
    pT_center = float(info_map[key0]["pTrange"][0])

    x_min = min([float(xx) for xx, yy, ey, key_str in pts])
    x_max = max([float(xx) for xx, yy, ey, key_str in pts])
    if(x_min == x_max):
        return None

    x_grid = np.linspace(float(x_min), float(x_max), 200)

    # UPDATED: build correct query points based on dimension_mode
    if(str(args.x_mode).lower() == "z"):
        if(args.dimension_mode == "4D"):
            query_points = np.column_stack([np.full(len(x_grid), q2_center), np.full(len(x_grid), y__center), x_grid, np.full(len(x_grid), pT_center)])
        elif(args.dimension_mode == "5D"):
            xB_center = Convert_xB_var(Q2_in=q2_center, y_in=y__center, Var_out="xB")
            query_points = np.column_stack([np.full(len(x_grid), q2_center), np.full(len(x_grid), y__center), x_grid, np.full(len(x_grid), pT_center), np.full(len(x_grid), xB_center)])
        elif(args.dimension_mode == "4D_xB"):
            xB_center = Convert_xB_var(Q2_in=q2_center, y_in=y__center, Var_out="xB")
            query_points = np.column_stack([np.full(len(x_grid), xB_center), np.full(len(x_grid), y__center), x_grid, np.full(len(x_grid), pT_center)])
    else:
        if(args.dimension_mode == "4D"):
            query_points = np.column_stack([np.full(len(x_grid), q2_center), np.full(len(x_grid), y__center), np.full(len(x_grid), z__center), x_grid])
        elif(args.dimension_mode == "5D"):
            xB_center = Convert_xB_var(Q2_in=q2_center, y_in=y__center, Var_out="xB")
            query_points = np.column_stack([np.full(len(x_grid), q2_center), np.full(len(x_grid), y__center), np.full(len(x_grid), z__center), x_grid, np.full(len(x_grid), xB_center)])
        elif(args.dimension_mode == "4D_xB"):
            xB_center = Convert_xB_var(Q2_in=q2_center, y_in=y__center, Var_out="xB")
            query_points = np.column_stack([np.full(len(x_grid), xB_center), np.full(len(x_grid), y__center), np.full(len(x_grid), z__center), x_grid])
    try:
        y_grid = spline_models[y_par](query_points)
    except Exception:
        try:
            y_grid = spline_models[y_par](np.asarray(query_points, dtype=float))
        except Exception:
            return None

    y_grid = np.asarray(y_grid).reshape(-1)
    if(len(y_grid) != len(x_grid)):
        return None

    gr_spline = ROOT.TGraph(len(x_grid))
    for ip, (xx, yy) in enumerate(zip(x_grid, y_grid)):
        gr_spline.SetPoint(ip, float(xx), float(yy))

    gr_spline.SetLineColorAlpha(int(series_map[sid]["color"]), 0.45)
    gr_spline.SetLineWidth(0)
    gr_spline.SetLineStyle(7)
    gr_spline.SetMarkerColorAlpha(int(series_map[sid]["color"]), 0.45)
    gr_spline.SetMarkerSize(1)
    gr_spline.SetMarkerStyle(29)
    return gr_spline

# ------------------------------------------------------------
# Spline-range shaded bands (--show_spline_range)
# ------------------------------------------------------------
def load_spline_fit_parameter_limits(path_hint=None):
    # Load special_fit_parameters_set from Phi_h_Fit_Parameters_from_Spline.py (cwd, then script dir).
    candidates = []
    if((path_hint is not None) and (str(path_hint).strip() not in ["", "None", "none"])):
        candidates.append(str(path_hint))
    candidates.append(os.path.join(os.getcwd(), "Phi_h_Fit_Parameters_from_Spline.py"))
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Phi_h_Fit_Parameters_from_Spline.py"))
    seen = set()
    for path in candidates:
        ap = os.path.abspath(path)
        if(ap in seen):
            continue
        seen.add(ap)
        if(not os.path.isfile(ap)):
            continue
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("Phi_h_Fit_Parameters_from_Spline_ssr", ap)
            if(spec is None or spec.loader is None):
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if(hasattr(mod, "special_fit_parameters_set")):
                return dict(mod.special_fit_parameters_set), ap
        except Exception as ee:
            print(f"{color.Error}WARNING:{color.END_R} Failed to load spline fit limits from '{ap}': {ee}{color.END}")
            continue
    return {}, None

def _build_spline_eval_point(args, Q2_val, y_val, z_val, Pt_val):
    # Match build_spline_graph / Create_Continuous_4D_Moments query packing for one kinematics point.
    if(args.dimension_mode == "4D"):
        return np.array([[float(Q2_val), float(y_val), float(z_val), float(Pt_val)]], dtype=float)
    elif(args.dimension_mode == "5D"):
        xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
        return np.array([[float(Q2_val), float(y_val), float(z_val), float(Pt_val), float(xB)]], dtype=float)
    elif(args.dimension_mode == "4D_xB"):
        xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
        return np.array([[float(xB), float(y_val), float(z_val), float(Pt_val)]], dtype=float)
    raise ValueError(f"Unsupported dimension_mode: {args.dimension_mode}")

def _evaluate_spline_safe(spline_obj, point):
    try:
        result = spline_obj(point)
    except Exception:
        result = spline_obj(np.asarray(point, dtype=float))
    return float(np.ravel(np.asarray(result, dtype=float))[0])

def build_spline_range_band_graph(xs, y_lo, y_hi, color, alpha=0.20):
    # Closed filled polygon: upper left→right, then lower right→left. Fill only (no lines/markers).
    n = len(xs)
    if((n == 0) or (len(y_lo) != n) or (len(y_hi) != n)):
        return None
    gr = ROOT.TGraph(2 * n)
    for ip in range(n):
        gr.SetPoint(ip, float(xs[ip]), float(y_hi[ip]))
    for ip in range(n):
        j = n - 1 - ip
        gr.SetPoint(n + ip, float(xs[j]), float(y_lo[j]))
    gr.SetFillColorAlpha(int(color), float(alpha))
    gr.SetFillStyle(1001)
    gr.SetLineWidth(0)
    gr.SetLineColorAlpha(int(color), 0.0)
    gr.SetMarkerSize(0)
    gr.SetMarkerStyle(1)
    return gr

def collect_spline_range_band_arrays(args, spline_models, info_map, sid, series_map, y_par):
    # Returns (xs, y_lo, y_hi) for one series, or None if bands do not apply / cannot be built.
    if(not getattr(args, "show_spline_range", False)):
        return None
    if(sid not in series_map):
        return None
    pts = series_map[sid]["points"]
    if(len(pts) == 0):
        return None
    mode = str(getattr(args, "spline_range_mode", "fit_limits")).strip().lower()
    y_par_s = str(y_par)

    # Mode fit_limits: B/C only, from Phi_h_Fit_Parameters_from_Spline.py
    if(mode == "fit_limits"):
        if(y_par_s == "Fit_Par_A"):
            return None
        limits = getattr(args, "spline_fit_limits", None)
        if((limits is None) or (len(limits) == 0)):
            return None
        lim_key = "B_limits" if(y_par_s == "Fit_Par_B") else ("C_limits" if(y_par_s == "Fit_Par_C") else None)
        if(lim_key is None):
            return None
        xs, y_lo, y_hi = [], [], []
        for xx, yy, ey, key_str in pts:
            try:
                q2y_bin, zpt_bin = parse_inner_key(key_str)
            except Exception:
                continue
            entry = limits.get((str(q2y_bin), str(zpt_bin)), None)
            if(entry is None):
                # Also try int-keyed tuples if the module stored mixed types
                entry = limits.get((q2y_bin, zpt_bin), None)
            if((entry is None) or (lim_key not in entry)):
                continue
            lim = entry[lim_key]
            if((lim is None) or (len(lim) < 2)):
                continue
            lo, hi = float(lim[0]), float(lim[1])
            if(lo > hi):
                lo, hi = hi, lo
            xs.append(float(xx))
            y_lo.append(lo)
            y_hi.append(hi)
        if(len(xs) == 0):
            return None
        return (xs, y_lo, y_hi)

    # Mode phase_space: min/max of spline over free kinematics inside the bin
    if(mode != "phase_space"):
        return None
    if(y_par not in spline_models):
        return None
    n_scan = int(getattr(args, "spline_range_scan_n", 6))
    if(n_scan < 2):
        n_scan = 2
    spline_obj = spline_models[y_par]
    x_is_z = (str(args.x_mode).lower() == "z")
    xs, y_lo, y_hi = [], [], []
    for xx, yy, ey, key_str in pts:
        try:
            q2y_bin, zpt_bin = parse_inner_key(key_str)
        except Exception:
            continue
        q2y_key = f"Q2-y={q2y_bin}, Q2-y"
        zpt_key = f"Q2-y={q2y_bin}, z-pT={zpt_bin}"
        if((q2y_key not in Full_Bin_Definition_Array) or (zpt_key not in Full_Bin_Definition_Array)):
            continue
        Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[q2y_key]
        z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[zpt_key]
        Q2_opts = np.linspace(float(Q2_min), float(Q2_max), n_scan)
        y_opts  = np.linspace(float(y_min),  float(y_max),  n_scan)
        if(x_is_z):
            z_fixed = float(xx)
            free3 = np.linspace(float(pT_min), float(pT_max), n_scan)
        else:
            pT_fixed = float(xx)
            free3 = np.linspace(float(z_min), float(z_max), n_scan)
        vmin, vmax = None, None
        for Q2_val in Q2_opts:
            for y_val in y_opts:
                for free_val in free3:
                    if(x_is_z):
                        z_val, Pt_val = z_fixed, float(free_val)
                    else:
                        z_val, Pt_val = float(free_val), pT_fixed
                    try:
                        point = _build_spline_eval_point(args, Q2_val, y_val, z_val, Pt_val)
                        val = _evaluate_spline_safe(spline_obj, point)
                    except Exception:
                        continue
                    if(not np.isfinite(val)):
                        continue
                    if((vmin is None) or (val < vmin)):
                        vmin = val
                    if((vmax is None) or (val > vmax)):
                        vmax = val
        if((vmin is None) or (vmax is None)):
            continue
        xs.append(float(xx))
        y_lo.append(float(vmin))
        y_hi.append(float(vmax))
    if(len(xs) == 0):
        return None
    return (xs, y_lo, y_hi)

def build_spline_range_band_for_series(args, spline_models, info_map, sid, series_map, y_par):
    arrays = collect_spline_range_band_arrays(args, spline_models, info_map, sid, series_map, y_par)
    if(arrays is None):
        return None
    xs, y_lo, y_hi = arrays
    color = series_map[sid]["color"]
    return build_spline_range_band_graph(xs, y_lo, y_hi, color, alpha=0.20)

def expand_y_range_for_spline_bands(args, grouped, fit_dict, info_map, y_par, y_range, spline_models, q2y_bins=None):
    # Expand (ymin, ymax) so shaded bands are not clipped off-pad.
    if(not getattr(args, "show_spline_range", False)):
        return y_range
    ymin, ymax = float(y_range[0]), float(y_range[1])
    bins_iter = list(q2y_bins) if(q2y_bins is not None) else list(grouped.keys())
    for q2y_bin in bins_iter:
        series_map = build_series_for_q2y(args, grouped, fit_dict, info_map, int(q2y_bin), y_par)
        for sid in series_map.keys():
            arrays = collect_spline_range_band_arrays(args, spline_models, info_map, sid, series_map, y_par)
            if(arrays is None):
                continue
            xs, y_lo, y_hi = arrays
            if(len(y_lo) > 0):
                ymin = min(ymin, float(np.min(y_lo)))
                ymax = max(ymax, float(np.max(y_hi)))
    if(ymin == ymax):
        return (ymin - 1.0, ymax + 1.0)
    pad = 0.08 * (ymax - ymin)
    return (ymin - pad, ymax + pad)

# ------------------------------------------------------------
# Title logic
# ------------------------------------------------------------
def Get_Default_Y_Title(y_par, fit_set):
    y_title_map = {"Fit_Par_A": "Amplitude", "Fit_Par_B": "Cos(#phi) Moment", "Fit_Par_C": "Cos(2#phi) Moment"}
    base = y_title_map.get(str(y_par), str(y_par))
    if(("(Normalized)" in str(fit_set)) and (str(y_par) in y_title_map)):
        base = f"{base} from the Cross Section Fits"
    return base

def parse_fit_set_features(fit_set):
    fs = str(fit_set)
    is_norm = ("(Normalized)" in fs)
    fs_clean = fs.replace("Fit_Pars_from_", "").replace("(Normalized)", "")
    mm_dim = re.search(r"(\d+)D", fs_clean)
    dim_tag = f"{mm_dim.group(1)}D" if(mm_dim is not None) else ""
    has_RC = (re.search(r"(^|_)RC(_|$)", fs_clean) is not None) or ("_RC_" in fs_clean) or ("RC_" in fs_clean) or ("_RC" in fs_clean)
    has_BC = (re.search(r"(^|_)BC(_|$)", fs_clean) is not None) or ("_BC_" in fs_clean) or ("BC_" in fs_clean) or ("_BC" in fs_clean)
    if("Bayesian" in fs_clean):
        method = "Bayesian Unfolding"
    elif("Bin" in fs_clean):
        method = "Bin-by-bin Acceptance Corrected"
    else:
        method = fs_clean.strip("_").replace("_", " ")
    return {"dim": dim_tag, "method": method, "has_BC": has_BC, "has_RC": has_RC, "is_norm": is_norm}

def Get_Default_FitSet_Title(fit_set):
    feat = parse_fit_set_features(fit_set)
    core = f"{feat['dim']} {feat['method']}".strip()
    if(feat["has_BC"] and feat["has_RC"]):
        core = f"{core} with BC Corrections and Radiative Corrections"
    elif(feat["has_BC"]):
        core = f"{core} with BC Corrections"
    elif(feat["has_RC"]):
        core = f"{core} with Radiative Corrections"
    if(feat["is_norm"]):
        core = f"{core} (Normalized)"
    return core

def comparison_y_axis_title(y_par, fit_set, ctype):
    base = Get_Default_Y_Title(y_par, fit_set).replace("from the Cross Section Fits", "").strip()
    if((ctype is None) or (str(ctype) == "overlay")):
        return base
    if(str(ctype) == "delta"):
        return f"|#Delta| {base}"
    if(str(ctype) == "diff"):
        return f"#Delta {base}"
    if(str(ctype) == "percent_dif"):
        return f"% Diff {base}"
    return base

def build_comparison_source_phrases(sources):
    # Human-readable source phrases: emphasize differences; factor shared method/corrections
    feats = [parse_fit_set_features(src["fit_set"]) for src in sources]
    shared_method = all((ff["method"] == feats[0]["method"]) for ff in feats)
    shared_BC = all((ff["has_BC"] == feats[0]["has_BC"]) for ff in feats)
    shared_RC = all((ff["has_RC"] == feats[0]["has_RC"]) for ff in feats)
    phrases = []
    for ff in feats:
        parts = []
        if(ff["dim"] != ""):
            parts.append(ff["dim"])
        if(not shared_method):
            parts.append(ff["method"])
        if((not shared_BC) and ff["has_BC"]):
            parts.append("BC")
        if((not shared_RC) and ff["has_RC"]):
            parts.append("RC")
        if(ff["is_norm"]):
            parts.append("Normalized")
        if(len(parts) == 0):
            parts.append(ff["method"] if(ff["method"] != "") else "Source")
        phrases.append(" ".join(parts))
    shared_bits = []
    if(shared_method and (feats[0]["method"] != "")):
        shared_bits.append(feats[0]["method"])
    if(shared_BC and feats[0]["has_BC"] and shared_RC and feats[0]["has_RC"]):
        shared_bits.append("with BC Corrections and Radiative Corrections")
    elif(shared_BC and feats[0]["has_BC"]):
        shared_bits.append("with BC Corrections")
    elif(shared_RC and feats[0]["has_RC"]):
        shared_bits.append("with Radiative Corrections")
    return phrases, " ".join(shared_bits).strip()

def build_comparison_canvas_title(args, sources, y_par, ctype):
    x_label = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    y_obs = Get_Default_Y_Title(y_par, sources[0]["fit_set"]).replace("from the Cross Section Fits", "").strip()
    if(str(ctype) == "overlay"):
        line1 = f"Comparison Overlay: {y_obs} vs {x_label}"
    elif(str(ctype) == "delta"):
        line1 = f"Absolute Difference of {y_obs} vs {x_label}"
    elif(str(ctype) == "diff"):
        line1 = f"Difference of {y_obs} vs {x_label}"
    elif(str(ctype) == "percent_dif"):
        line1 = f"Percent Difference of {y_obs} vs {x_label}"
    else:
        line1 = f"{comparison_type_title(ctype)}: {y_obs} vs {x_label}"
    if(str(args.title_text).strip() != ""):
        line1 = f"{args.title_text} {line1}"
    phrases, shared_line = build_comparison_source_phrases(sources)
    contrast = " vs ".join(phrases)
    if(shared_line != ""):
        line2 = f"#splitline{{{contrast}}}{{{shared_line}}}"
    else:
        line2 = contrast
    return f"#splitline{{{line1}}}{{{line2}}}"

# ------------------------------------------------------------
# Drawing
# ------------------------------------------------------------
def style_graph(gr, color_val, marker_val, line_width=2):
    gr.SetLineColor(int(color_val))
    gr.SetMarkerColor(int(color_val))
    gr.SetMarkerStyle(int(marker_val))
    gr.SetLineWidth(line_width)
    gr.SetMarkerSize(1.0)

def build_global_title(args, fit_set, y_par):
    if(args.title_mode == "none"):
        return ""
    if(args.title_mode == "text_only"):
        return str(args.title_text)

    if(str(args.fit_set_label).strip() != ""):
        fit_label = str(args.fit_set_label)
    else:
        fit_label = Get_Default_FitSet_Title(fit_set)

    x_label = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    y_label = Get_Default_Y_Title(y_par, fit_set)
    line1 = f"{y_label} vs {x_label}"
    line2 = f"{fit_label}"
    if(str(args.title_text).strip() != ""):
        line1 = f"{args.title_text} {line1}"
    return f"#splitline{{{line1}}}{{{line2}}}"

def draw_global_title(args, canvas, title_text):
    if(str(title_text).strip() == ""):
        return
    canvas.cd()
    tex = ROOT.TLatex()
    tex.SetNDC(True)
    tex.SetTextAlign(13)
    tex.SetTextFont(42)
    tex.SetTextSize(float(args.title_size))
    tex.DrawLatex(float(args.title_x), float(args.title_y), str(title_text))

def draw_pad_label(args, q2y_bin, q2y_ranges):
    if(args.pad_label_mode == "none"):
        return
    lab = ROOT.TLatex()
    lab.SetNDC(True)
    lab.SetTextAlign(23)
    lab.SetTextFont(42)
    lab.SetTextSize(float(args.pad_label_size))
    x0 = float(args.pad_label_x)
    y0 = float(args.pad_label_y)
    line_step = 1.10 * float(args.pad_label_size)
    Q2min = float(q2y_ranges[q2y_bin]["Q2range"][1])
    Q2max = float(q2y_ranges[q2y_bin]["Q2range"][2])
    ymin = float(q2y_ranges[q2y_bin]["y_range"][1])
    ymax = float(q2y_ranges[q2y_bin]["y_range"][2])
    if(args.pad_label_mode == "Q2y_only"):
        lab.DrawLatex(x0, y0, f"{Q2min:.2f} < Q^{{2}} < {Q2max:.2f}")
        lab.DrawLatex(x0, y0 - line_step, f"{ymin:.2f} < y < {ymax:.2f}")
        return
    lab.DrawLatex(x0, y0, f"Q^{{2}}-y Bin {q2y_bin}")
    if(args.pad_label_mode == "bin"):
        return
    if(q2y_bin not in q2y_ranges):
        return
    lab.DrawLatex(x0, y0 - line_step, f"{Q2min:.2f} < Q^{{2}} < {Q2max:.2f}")
    if(args.pad_label_mode == "bin_Q2"):
        return
    lab.DrawLatex(x0, y0 - 2.0*line_step, f"{ymin:.2f} < y < {ymax:.2f}")

def draw_mosaic(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, x_range, y_range, spline_models={}, y_axis_title_override=None, canvas_name_suffix="", title_space_override=None, force_log_y=False):
    mapping, max_cols, nrows = build_layout_map(args)
    cname = f"c_mosaic_{y_par}{canvas_name_suffix}"
    c1 = ROOT.TCanvas(cname, cname, int(args.canvas_width), int(args.canvas_height))
    c1.SetFillColor(0)
    c1.SetFillStyle(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)

    if(not hasattr(c1, "_keepalive")):
        c1._keepalive = []

    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])
    use_log_y = bool(force_log_y) or use_log_y_for_par(args, y_par)
    if(use_log_y):
        gymin, gymax = ensure_positive_y_range_for_log(gymin, gymax)

    if(title_space_override is not None):
        title_space = float(title_space_override)
    else:
        title_space = 0.090 if(args.title_mode != "none") else 0.00
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    if(y_axis_title_override is not None):
        y_axis_title = str(y_axis_title_override)
    else:
        y_axis_title = Get_Default_Y_Title(y_par, fit_set)
        y_axis_title = y_axis_title.replace("from the Cross Section Fits", "")

    # -------------------------------------------------------------------------
    #  Variable TPad widths per row so plot-area width is identical
    #  even when left_margin is larger on the "y-axis label" pad.
    #  This changes ONLY the TPad placement (x0/x1), not the plot logic.
    # -------------------------------------------------------------------------
    row_bins = {}
    for q2y_bin in mapping.keys():
        row, col, col_start = mapping[q2y_bin]
        if(row not in row_bins):
            row_bins[row] = []
        row_bins[row].append((col, q2y_bin, col_start))
    for row in row_bins.keys():
        row_bins[row].sort(key=lambda tt: tt[0])  # left->right

    x_edges = {}
    right_margin = 0.03 - 0.03
    left_small   = 0.03 - 0.03
    left_big     = 0.22

    for row in row_bins.keys():
        pads = row_bins[row]
        n_present = len(pads)

        big_flags = []
        for col, q2y_bin, col_start in pads:
            is_leftmost_present = (col == col_start)
            big_flags.append((args.label_mode == "all") or ((args.label_mode == "outer") and is_leftmost_present))

        n_big = sum([1 for bb in big_flags if(bb)])
        n_small = n_present - n_big

        if((args.label_mode == "all") or (n_big == 0)):
            width_each = 1.0 / float(max_cols)
            widths = [width_each for _ in range(n_present)]
        else:
            plot_frac_small = 1.0 - left_small - right_margin
            plot_frac_big   = 1.0 - left_big   - right_margin
            ratio = plot_frac_small / plot_frac_big
            width_small = 1.0 / (float(max_cols - 1) + float(ratio))
            width_big = width_small * ratio
            widths = [(width_big if(big_flags[i]) else width_small) for i in range(n_present)]

        target_total = sum(widths)
        x_start = 1.0 - target_total

        cursor = x_start
        for i, (col, q2y_bin, col_start) in enumerate(pads):
            x0 = cursor
            cursor = cursor + widths[i]
            x1 = cursor
            if(i == (n_present - 1)):
                x1 = 1.0
                cursor = x1
            x_edges[q2y_bin] = (float(x0), float(x1))

    for q2y_bin in range(1, int(args.q2y_count) + 1):
        if(q2y_bin not in mapping):
            continue
        row, col, col_start = mapping[q2y_bin]

        # Use compensated x0/x1 (instead of uniform col/max_cols)
        x0, x1 = x_edges[q2y_bin]

        y0 = (float(row) / float(nrows)) * (1.0 - title_space)
        y1 = (float(row + 1) / float(nrows)) * (1.0 - title_space)

        pad = ROOT.TPad(f"pad_q2y_{q2y_bin}_{y_par}", f"pad_q2y_{q2y_bin}_{y_par}", float(x0), float(y0), float(x1), float(y1))
        pad.SetFillColor(0)
        pad.SetFillStyle(0)
        pad.SetFrameFillStyle(0)
        pad.SetFrameLineWidth(int(args.frame_line_width))
        pad.SetTickx(1)
        pad.SetTicky(1)
        pad.SetGrid(1, 1)

        is_bottom, is_leftmost_present, is_rightmost_present, is_top = pad_is_outer(row, col, col_start, max_cols, nrows)

        # left_margin   = 0.22 if((args.label_mode == "outer") and (is_leftmost_present)) else (0.22 if(args.label_mode == "all") else (0.03 - 0.02))
        # bottom_margin = 0.20 if((args.label_mode == "outer") and (is_bottom)) else (0.20 if(args.label_mode == "all") else (0.03 - 0.02))
        # right_margin  = (0.03 - 0.02)
        # top_margin    = (0.05 - 0.02)
        left_margin   = 0.22 if((args.label_mode == "outer") and (is_leftmost_present)) else (0.22 if(args.label_mode == "all") else 0)
        bottom_margin = 0.20 if((args.label_mode == "outer") and (is_bottom)) else (0.20 if(args.label_mode == "all") else 0)
        right_margin  = 0
        top_margin    = 0

        pad.SetLeftMargin(float(left_margin))
        pad.SetBottomMargin(float(bottom_margin))
        pad.SetRightMargin(float(right_margin))
        pad.SetTopMargin(float(top_margin))
        if(use_log_y):
            pad.SetLogy(1)

        pad.Draw()
        pad.cd()

        frame = pad.DrawFrame(xmin, gymin, xmax, gymax)
        c1._keepalive.append(frame)

        frame.SetTitle("")
        frame.GetXaxis().SetTitle(x_axis_title if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_bottom))) else "")
        frame.GetYaxis().SetTitle(y_axis_title if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_leftmost_present))) else "")

        # frame.GetXaxis().SetTitleSize(0.060 if((args.label_mode == "all") or is_bottom) else 0.0)
        # frame.GetYaxis().SetTitleSize(0.060 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        # frame.GetXaxis().SetLabelSize(0.050 if((args.label_mode == "all") or is_bottom) else 0.0)
        # frame.GetYaxis().SetLabelSize(0.050 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        frame.GetXaxis().SetTitleSize(0.080 if((args.label_mode == "all") or is_bottom) else 0.0)
        frame.GetYaxis().SetTitleSize(0.080 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        frame.GetXaxis().SetLabelSize(0.070 if((args.label_mode == "all") or is_bottom) else 0.0)
        frame.GetYaxis().SetLabelSize(0.070 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_leftmost_present))):
            frame.GetYaxis().SetTitleOffset(0.85)

        frame.GetXaxis().SetNdivisions(505)
        frame.GetYaxis().SetNdivisions(505)

        series_map = build_series_for_q2y(args, grouped, fit_dict, info_map, q2y_bin, y_par)
        sid_list = sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)

        for sid in sid_list:
            # Shaded range band first (behind spline + data)
            if(getattr(args, "show_spline_range", False)):
                gr_band = build_spline_range_band_for_series(args, spline_models, info_map, sid, series_map, y_par)
                if(gr_band is not None):
                    gr_band.Draw("F SAME")
                    c1._keepalive.append(gr_band)

            gr_spline = build_spline_graph(args, spline_models, info_map, sid, series_map, y_par)
            if(gr_spline is not None):
                gr_spline.Draw("P L SAME")
                c1._keepalive.append(gr_spline)

            pts = series_map[sid]["points"]
            gr  = ROOT.TGraphErrors(len(pts))
            for ip, (xx, yy, ey, key_str) in enumerate(pts):
                gr.SetPoint(ip, float(xx), float(yy))
                xerr = 0.0
                if(args.x_error_bars):
                    if(str(args.x_mode).lower() == "z"):
                        xw = float(info_map[key_str]["z_range"][2]) - float(info_map[key_str]["z_range"][1])
                    else:
                        xw = float(info_map[key_str]["pTrange"][2]) - float(info_map[key_str]["pTrange"][1])
                    xerr = 0.5 * float(args.x_error_fraction) * float(xw)
                gr.SetPointError(ip, float(xerr), float(ey))
            style_graph(gr, series_map[sid]["color"], series_map[sid]["marker"], line_width=2 if("pdf" not in str(args.formats)) else 1)
            draw_opt = "P L SAME"
            if(args.x_error_bars):
                draw_opt = "P E1 SAME"
            gr.Draw(draw_opt)
            c1._keepalive.append(gr)

        if(args.draw_legends):
            legend_title = "P_{T} Bins" if(args.x_mode == "z") else "z Bins"
            legend_entries = []
            for sid in sid_list:
                pts = series_map[sid]["points"]
                if(len(pts) == 0):
                    continue
                key0 = pts[0][3]
                if(key0 not in info_map):
                    continue
                other_val = float(info_map[key0]["pTrange"][0]) if(args.x_mode == "z") else float(info_map[key0]["z_range"][0])
                legend_entries.append((other_val, int(series_map[sid]["color"])))
            legend_entries.sort(key=lambda tt: tt[0])

            if(len(legend_entries) > 0):
                leg_x1 = 0.98
                # leg_x0 = 0.82
                leg_x0 = 0.78
                # leg_y1 = 0.84
                leg_y1 = 0.89
                entry_h = 0.055
                nlines = int(2*len(legend_entries)) + 1
                leg_y0 = leg_y1 - entry_h * float(nlines)
                if(leg_y0 < 0.12):
                    leg_y0 = 0.12
                leg = ROOT.TLegend(float(leg_x0), float(leg_y0), float(leg_x1), float(leg_y1))
                # leg.SetBorderSize(0)
                leg.SetBorderSize(1)
                leg.SetFillStyle(1001)
                leg.SetFillColor(ROOT.kWhite)
                leg.SetTextFont(42)
                # leg.SetTextSize(0.045)
                leg.SetTextSize(0.055)
                leg.SetHeader(str(legend_title), "C")
                for val, colv in legend_entries:
                    ent = leg.AddEntry(0, f"{val:.3f}", "")
                    if(ent):
                        ent.SetTextColor(int(colv))
                leg.Draw("SAME")
                c1._keepalive.append(leg)

        draw_pad_label(args, q2y_bin, q2y_ranges)

        pad.Update()
        c1.cd()

    c1.Update()
    return c1

# ------------------------------------------------------------
# Single-bin output (standalone) helpers
# ------------------------------------------------------------
def FitSet_Has_RC(fit_set):
    fs = str(fit_set)
    fs = fs.replace("Fit_Pars_from_", "")
    fs_clean = fs.replace("(Normalized)", "")
    has_RC = (re.search(r"(^|_)RC(_|$)", fs_clean) is not None) or ("_RC_" in fs_clean) or ("RC_" in fs_clean) or ("_RC" in fs_clean)
    return has_RC

def FitSet_Has_BC(fit_set):
    fs = str(fit_set)
    fs = fs.replace("Fit_Pars_from_", "")
    fs_clean = fs.replace("(Normalized)", "")
    has_BC = (re.search(r"(^|_)BC(_|$)", fs_clean) is not None) or ("_BC_" in fs_clean) or ("BC_" in fs_clean) or ("_BC" in fs_clean)
    return has_BC

def Build_SingleBin_Subtitle(args, fit_set):
    has_rc = FitSet_Has_RC(fit_set)
    has_bc = FitSet_Has_BC(fit_set)
    if(has_bc and has_rc):
        subtitle = "With BC + RC Factors"
        if((str(args.title_text).strip() != "")):
            subtitle = f"{subtitle} #topbar {str(args.title_text).strip()}"
        return subtitle
    if(has_rc):
        subtitle = "With RC Factors"
        if((str(args.title_text).strip() != "")):
            subtitle = f"{subtitle} #topbar {str(args.title_text).strip()}"
        return subtitle
    if(has_bc):
        subtitle = "With BC Corrections"
        return subtitle
    return ""

def Draw_SingleBin_Title_Block(args, canvas, fit_set, y_par):
    y_label = Get_Default_Y_Title(y_par, fit_set)
    y_label = y_label.replace(" from the Cross Section Fits", "")
    line1 = f"CLAS12 Preliminary #topbar {y_label}"
    line2 = Build_SingleBin_Subtitle(args, fit_set)
    canvas.cd()
    tex = ROOT.TLatex()
    tex.SetNDC(True)
    # Title block sizes (subtitle ~5-10% larger vs previous version)
    size1 = 0.050
    size2 = 0.037
    y_top = 0.965
    # Main title: centered
    tex.SetTextAlign(13)
    tex.SetTextFont(62)
    tex.SetTextSize(size1)
    try:
        lm = float(canvas.GetLeftMargin())
    except Exception:
        lm = 0.14
    tex.DrawLatex(lm-0.04, y_top, str(line1))
    # Subtitle: indented (left-aligned) + more vertical separation from line1
    if((str(line2).strip() != "")):
        try:
            lm = float(canvas.GetLeftMargin())
        except Exception:
            lm = 0.14
        x_sub = lm #+ 0.18
        tex.SetTextAlign(13)
        tex.SetTextFont(42)
        tex.SetTextSize(size2)
        tex.DrawLatex(float(x_sub), float(y_top - 1.15*size1), str(line2))

def Draw_SingleBin_Preliminary_Watermark(args):
    if(not args.draw_preliminary_watermark):
        return
    wm = ROOT.TLatex()
    wm.SetNDC(True)
    wm.SetTextAlign(22)
    wm.SetTextFont(62)
    wm.SetTextSize(0.135)
    wm.SetTextAngle(-30)
    try:
        wm.SetTextColorAlpha(ROOT.kRed, 0.10)
    except Exception:
        wm.SetTextColor(ROOT.kRed)
    wm.DrawLatex(0.52, 0.50, "PRELIMINARY")

def Compute_SingleBin_AutoYRange(series_map):
    ymin = None
    ymax = None
    for sid in series_map.keys():
        for xx, yy, ey, key_str in series_map[sid]["points"]:
            lo = float(yy) - abs(float(ey))
            hi = float(yy) + abs(float(ey))
            if((ymin is None) or (lo < ymin)):
                ymin = lo
            if((ymax is None) or (hi > ymax)):
                ymax = hi
    if((ymin is None) or (ymax is None)):
        return (-1.0, 1.0)
    if(ymin == ymax):
        return (ymin - 1.0, ymax + 1.0)
    span = ymax - ymin
    ymin = ymin - 0.35 * span
    ymax = ymax + 0.10 * span
    return (ymin, ymax)

def Draw_SingleBin_Q2yText(q2y_bin, q2y_ranges):
    if(q2y_bin not in q2y_ranges):
        return
    Q2min = float(q2y_ranges[q2y_bin]["Q2range"][1])
    Q2max = float(q2y_ranges[q2y_bin]["Q2range"][2])
    yminv = float(q2y_ranges[q2y_bin]["y_range"][1])
    ymaxv = float(q2y_ranges[q2y_bin]["y_range"][2])

    lab = ROOT.TLatex()
    lab.SetNDC(True)
    lab.SetTextAlign(13)
    lab.SetTextFont(42)
    lab.SetTextSize(0.03)

    lm = ROOT.gPad.GetLeftMargin()
    tm = ROOT.gPad.GetTopMargin()

    x0 = float(lm) + 0.02
    y0 = 1.0 - float(tm) - 0.02
    step = 0.055

    lab.DrawLatex(x0, y0, f"{Q2min:.2f} < Q^{{2}} < {Q2max:.2f}")
    lab.DrawLatex(x0, y0 - step, f"{yminv:.2f} < y < {ymaxv:.2f}")

def Draw_SingleBin_Legend(args, series_map, info_map):
    # Legend entries show the full bin width of the variable NOT on the x-axis
    other_is_pT = (str(args.x_mode).lower() == "z")
    entries = []

    for sid in series_map.keys():
        pts = series_map[sid]["points"]
        if(len(pts) == 0):
            continue
        key0 = pts[0][3]
        if(key0 not in info_map):
            continue
        if(other_is_pT):
            cen = float(info_map[key0]["pTrange"][0])
            vmin = float(info_map[key0]["pTrange"][1])
            vmax = float(info_map[key0]["pTrange"][2])
            label = f"{vmin:.2f} < P_{{T}} < {vmax:.2f}"
        else:
            cen = float(info_map[key0]["z_range"][0])
            vmin = float(info_map[key0]["z_range"][1])
            vmax = float(info_map[key0]["z_range"][2])
            label = f"{vmin:.2f} < z < {vmax:.2f}"
        colv = int(series_map[sid]["color"])
        entries.append((cen, label, colv, sid))

    entries.sort(key=lambda tt: tt[0])

    if(len(entries) == 0):
        return None

    # Requirement: if > 6 entries, add a column (not a row)
    ncols = 3 if(len(entries) <= 6) else 4

    lm = ROOT.gPad.GetLeftMargin()
    rm = ROOT.gPad.GetRightMargin()
    bm = ROOT.gPad.GetBottomMargin()
    tm = ROOT.gPad.GetTopMargin()

    leg_x1 = float(lm)
    leg_x2 = 1.0 - float(rm)

    leg_y1 = 0.125
    if(leg_y1 <= float(bm)):
        leg_y1 = float(bm) + 0.01

    legend_height = 0.25
    leg_y2 = leg_y1 + legend_height

    top_limit = 1.0 - float(tm) - 0.02
    if(leg_y2 > top_limit):
        leg_y2 = top_limit

    leg = ROOT.TLegend(float(leg_x1), float(leg_y1), float(leg_x2), float(leg_y2))
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.025)
    leg.SetNColumns(int(ncols))
    try:
        leg.SetColumnSeparation(0.10)
    except Exception:
        pass
    try:
        leg.SetMargin(0.20)
    except Exception:
        pass

    return (leg, entries)

def draw_single_bin(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, q2y_bin, x_range, y_range, spline_models={}, y_axis_title_override=None, force_log_y=False):
    c1 = ROOT.TCanvas(f"c_single_{y_par}_{q2y_bin}", f"c_single_{y_par}_{q2y_bin}", int(args.single_canvas_width), int(args.single_canvas_height))
    c1.SetFillColor(0)
    c1.SetFillStyle(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)

    if(not hasattr(c1, "_keepalive")):
        c1._keepalive = []

    # Macro-style: single pad fills the canvas, with a reduced top margin for the title block.
    # Only allocate enough room for the subtitle if it actually exists.
    subtitle_tmp = Build_SingleBin_Subtitle(args, fit_set)
    # top_margin = 0.22 if((str(subtitle_tmp).strip() != "")) else 0.18
    top_margin = 0.16 if((str(subtitle_tmp).strip() != "")) else 0.16

    pad = ROOT.TPad(f"pad_single_{y_par}_{q2y_bin}", f"pad_single_{y_par}_{q2y_bin}", 0.0, 0.0, 1.0, 1.0)
    pad.SetFillColor(0)
    pad.SetFillStyle(0)
    pad.SetFrameFillStyle(0)
    pad.SetGrid(1, 1)
    # pad.SetTickx(1) # This adds exta tick marks on the oposite axis (i.e., on the top and bottom sides of the image)
    # pad.SetTicky(1) # This adds exta tick marks on the oposite axis (i.e., on the left and right sides of the image)
    pad.SetLeftMargin(0.14)
    pad.SetBottomMargin(0.12)
    pad.SetRightMargin(0.04)
    pad.SetTopMargin(top_margin)
    use_log_y = bool(force_log_y) or use_log_y_for_par(args, y_par)
    if(use_log_y):
        pad.SetLogy(1)
    pad.Draw()
    pad.cd()
    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])
    if(use_log_y):
        gymin, gymax = ensure_positive_y_range_for_log(gymin, gymax)
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    if(y_axis_title_override is not None):
        y_axis_title = str(y_axis_title_override)
    else:
        y_axis_title = Get_Default_Y_Title(y_par, fit_set)
        y_axis_title = y_axis_title.replace("from the Cross Section Fits", "")

    frame = pad.DrawFrame(xmin, gymin, xmax, gymax)
    c1._keepalive.append(frame)

    frame.SetTitle("")
    frame.GetXaxis().SetTitle(x_axis_title)
    frame.GetYaxis().SetTitle(y_axis_title)

    # Closer to your reference formatting
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetYaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.025)
    frame.GetYaxis().SetLabelSize(0.025)
    frame.GetYaxis().SetTitleOffset(0.85)
    # frame.GetXaxis().SetTitleSize(0.045)
    # frame.GetYaxis().SetTitleSize(0.045)
    # frame.GetXaxis().SetLabelSize(0.040)
    # frame.GetYaxis().SetLabelSize(0.040)
    # frame.GetXaxis().SetNdivisions(505)
    # frame.GetYaxis().SetNdivisions(505)

    series_map = build_series_for_q2y(args, grouped, fit_dict, info_map, int(q2y_bin), y_par)
    sid_list = sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)

    # Watermark (optional) UNDER the data
    Draw_SingleBin_Preliminary_Watermark(args)

    graphs_by_sid = {}

    for sid in sid_list:
        pts = series_map[sid]["points"]
        # if(int(series_map[sid]["color"]) != ROOT.kGreen):
        #     continue

        # Shaded range band first (behind spline + data)
        if(getattr(args, "show_spline_range", False)):
            gr_band = build_spline_range_band_for_series(args, spline_models, info_map, sid, series_map, y_par)
            if(gr_band is not None):
                gr_band.Draw("F SAME")
                c1._keepalive.append(gr_band)

        gr_spline = build_spline_graph(args, spline_models, info_map, sid, series_map, y_par)
        if(gr_spline is not None):
            gr_spline.Draw("P L SAME")
            c1._keepalive.append(gr_spline)

        gr  = ROOT.TGraphErrors(len(pts))
        for ip, (xx, yy, ey, key_str) in enumerate(pts):
            gr.SetPoint(ip, float(xx), float(yy))
            xerr = 0.0
            if(args.x_error_bars):
                if(str(args.x_mode).lower() == "z"):
                    xw = float(info_map[key_str]["z_range"][2]) - float(info_map[key_str]["z_range"][1])
                else:
                    xw = float(info_map[key_str]["pTrange"][2]) - float(info_map[key_str]["pTrange"][1])
                xerr = 0.5 * float(args.x_error_fraction) * float(xw)
            gr.SetPointError(ip, float(xerr), float(ey))
        style_graph(gr, series_map[sid]["color"], series_map[sid]["marker"], line_width=1 if("pdf" not in str(args.formats)) else 1)
        # gr.SetMarkerSize(0.5)
        # gr.SetLineWidth(1)

        draw_opt = "P E1 L SAME"
        if(args.x_error_bars):
            draw_opt = "P E1 SAME"
        gr.Draw(draw_opt)
        c1._keepalive.append(gr)
        graphs_by_sid[sid] = gr

    Draw_SingleBin_Q2yText(int(q2y_bin), q2y_ranges)

    leg_pack = Draw_SingleBin_Legend(args, series_map, info_map)
    if(leg_pack is not None):
        leg, entries = leg_pack
        for cen, label, colv, sid in entries:
            gr = graphs_by_sid.get(sid, None)
            if(gr is None):
                continue
            if(gr.GetLineColor() != ROOT.kGreen):
                continue
            leg_opt = "LP"
            if(args.x_error_bars):
                leg_opt = "PE"
            ent = leg.AddEntry(gr, str(label), leg_opt)
            if(ent):
                ent.SetTextColor(int(colv))
                try:
                    ent.SetTextSize(0.030)
                except Exception:
                    pass
        leg.Draw("SAME")
        c1._keepalive.append(leg)

    # Title/subtitle in the pad top margin
    Draw_SingleBin_Title_Block(args, pad, fit_set, y_par)

    pad.Modified()
    pad.Update()
    c1.cd()
    c1.Modified()
    c1.Update()
    return c1

def Validate_Output_Filename(filename):
    forbidden = [' ', '"', "'", '=']
    for ch in forbidden:
        if(ch in str(filename)):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} Forbidden character '{ch}' in output filename:{color.END} {filename}")
    return

def Get_Default_Y_FileTag(y_par, fit_set):
    y_tag_map = {"Fit_Par_A": "Amplitude", "Fit_Par_B": "CosPhiMoment", "Fit_Par_C": "Cos2PhiMoment"}
    base_tag  = y_tag_map.get(str(y_par), sanitize_for_filename(str(y_par)))
    if(("(Normalized)" in str(fit_set)) and (str(y_par) in y_tag_map)):
        base_tag = f"{base_tag}_XsecFits"
    return sanitize_for_filename(base_tag)

def Get_Default_FitSet_FileTag(fit_set):
    fs = str(fit_set)
    fs = fs.replace("Fit_Pars_from_", "")
    is_norm = "(Normalized)" in fs
    fs_clean = fs.replace("(Normalized)", "")

    mm_dim = re.search(r"(\d+)D", fs_clean)
    dim_tag = f"{mm_dim.group(1)}D" if(mm_dim is not None) else ""

    has_rc = (re.search(r"(^|_)RC(_|$)", fs_clean) is not None) or ("_RC_" in fs_clean) or ("RC_" in fs_clean) or ("_RC" in fs_clean)
    has_bc = (re.search(r"(^|_)BC(_|$)", fs_clean) is not None) or ("_BC_" in fs_clean) or ("BC_" in fs_clean) or ("_BC" in fs_clean)

    if("Bayesian" in fs_clean):
        method_tag = "BayesianUnfold"
    elif("Bin" in fs_clean):
        method_tag = "BinByBinAccCorr"
    else:
        method_tag = sanitize_for_filename(fs_clean)

    tag = f"{dim_tag}_{method_tag}" if(dim_tag != "") else f"{method_tag}"
    if(has_bc):
        tag = f"{tag}_BC"
    if(has_rc):
        tag = f"{tag}_RC"
    if(is_norm):
        tag = f"{tag}_Norm"

    return sanitize_for_filename(tag)

def Build_Output_Filename(args, fit_set, y_par):
    stem  = sanitize_for_filename(args.name)
    fs_tag = Get_Default_FitSet_FileTag(fit_set)
    x_tag = "pT" if(str(args.x_mode).lower() == "pt") else "z"
    y_tag  = Get_Default_Y_FileTag(y_par, fit_set)
    filename = f"{stem}_{fs_tag}_{x_tag}_{y_tag}.{args.formats}"
    Validate_Output_Filename(filename)
    return filename

def Build_SingleBin_Output_Filename(args, fit_set, y_par, q2y_bin):
    stem  = sanitize_for_filename(args.name)
    fs_tag = Get_Default_FitSet_FileTag(fit_set)
    x_tag = "pT" if(str(args.x_mode).lower() == "pt") else "z"
    y_tag  = Get_Default_Y_FileTag(y_par, fit_set)
    filename = f"{stem}_SingleBin_Q2yBin{int(q2y_bin)}_{fs_tag}_{x_tag}_{y_tag}.{args.formats}"
    Validate_Output_Filename(filename)
    return filename

def save_canvas(args, canvas, fit_set, y_par):
    filename = Build_Output_Filename(args, fit_set, y_par)
    canvas.SaveAs(filename)
    return filename

def save_single_canvas(args, canvas, fit_set, y_par, q2y_bin):
    filename = Build_SingleBin_Output_Filename(args, fit_set, y_par, q2y_bin)
    canvas.SaveAs(filename)
    return filename

 
def Spline_Plots_Only(args, spline_models, y_ranges=None):
    # Fixed kinematic grids (with float conversion as you added)
    Q2_grid = [float(val) for val in getattr(args, "Fixed_Q2", [2.2])]
    y__grid = [float(val) for val in getattr(args, "Fixed_y",  [0.7])]
    z__grid = [float(val) for val in getattr(args, "Fixed_z",  [0.555])]
    pT_grid = [float(val) for val in getattr(args, "Fixed_pT", [0.135])]

    x_min, x_max = 0.05, 1.0
    xB_is_Q2, xB_is__y = False, False # Probably should remove these later (xB should be being handled differently now than when these conditions were first introduced — probably outdated now)
                                      # Current Best Practices: Do not use 'Fixed_xB' — let it just be determined by Q2 and y when not plotting
    if(str(args.x_mode).lower() == "q2"):
        x_min, x_max = 2.0, 7.9
        if(getattr(args, "Fixed_xB", None) is not None):
            y__grid      = [float(val) for val in args.Fixed_xB]
            args.Fixed_y = [float(val) for val in args.Fixed_xB]
            xB_is__y     = True
    if(args.x_mode in ["y"]):
        x_min, x_max = 0.35, 0.75
        if(getattr(args, "Fixed_xB", None) is not None):
            Q2_grid       = [float(val) for val in args.Fixed_xB]
            args.Fixed_Q2 = [float(val) for val in args.Fixed_xB]
            xB_is_Q2      = True
    if(args.x_mode in ["xB", "xb"]):
        x_min, x_max = 0.134061, 0.722104
    x_grid = np.linspace(float(x_min), float(x_max), 200)
    Q2_varies_with_xB, y__varies_with_xB = False, False
    legend_title = "#scale[1.25]{Fixed Kinematics}"
    if((len(Q2_grid) == 1) and ((str(args.x_mode).lower() != "q2") or xB_is_Q2)):
        if(str(args.x_mode).lower() == "xb"):
            Q2_varies_with_xB = True
            legend_title = f"#splitline{{{legend_title}}}{{Q^{{2}} Varies with x_{{B}}}}"
        else:
            legend_title = f"#splitline{{{legend_title}}}{{{'Q^{2}' if(not xB_is_Q2) else 'x_{B}'} = {Q2_grid[0]}}}"
    if((len(y__grid) == 1) and ((str(args.x_mode).lower() != "y")  or xB_is__y)):
        if((str(args.x_mode).lower() == "xb") and (not Q2_varies_with_xB)):
            y__varies_with_xB = True
            legend_title = f"#splitline{{{legend_title}}}{{y Varies with x_{{B}}}}"
        else:
            legend_title = f"#splitline{{{legend_title}}}{{{'y'     if(not xB_is__y) else 'x_{B}'} = {y__grid[0]}}}"
    if((len(z__grid) == 1) and (str(args.x_mode).lower()  != "z")):
        legend_title = f"#splitline{{{legend_title}}}{{z = {z__grid[0]}}}"
    if((len(pT_grid) == 1) and (str(args.x_mode).lower()  != "pt")):
        legend_title = f"#splitline{{{legend_title}}}{{P_{{T}} = {pT_grid[0]}}}"
    if(Q2_varies_with_xB or y__varies_with_xB):
        print("\n\n")
        print(f"Q2_varies_with_xB = {Q2_varies_with_xB}")
        print(f"y__varies_with_xB = {y__varies_with_xB}")
        print(f"legend_title      = {legend_title}\n\n")
    # Build all query points
    Line_Num, query_points = 0, {}
    for             Q2_val in Q2_grid:
        for         y__val in y__grid:
            for     z__val in z__grid:
                for pT_val in pT_grid:
                    Line_Num += 1
                    Q2_stack = np.full(len(x_grid), Q2_val) if(str(args.x_mode).lower() != "q2") else x_grid
                    y__stack = np.full(len(x_grid), y__val) if(str(args.x_mode).lower() != "y")  else x_grid
                    z__stack = np.full(len(x_grid), z__val) if(str(args.x_mode).lower() != "z")  else x_grid
                    pT_stack = np.full(len(x_grid), pT_val) if(str(args.x_mode).lower() != "pt") else x_grid
                    if(args.dimension_mode == "5D"):
                        if(str(args.x_mode).lower() == "xb"):
                            xB_stack = x_grid
                            if(len(Q2_grid) < 2):   # Assumes that Q2 is set to default values → let it vary with xB
                                Q2_stack = np.array([Convert_xB_var(xB_in=xb, Q2_in=Q2_val, y_in=y__val, Var_out="Q2") for xb in xB_stack])
                                # Q2_varies_with_xB = True
                            elif(len(y__grid) < 2): # Assumes that y  is set to default values → let it vary with xB
                                y__stack = np.array([Convert_xB_var(xB_in=xb, Q2_in=Q2_val, y_in=y__val, Var_out="y")  for xb in xB_stack])
                                # y__varies_with_xB = True
                            else:
                                raise SystemExit(f"{color.Error}ERROR:{color.END} Cannot plot xB while fixing BOTH Q2 and y.\n")
                        elif(str(args.x_mode).lower() in ["y", "q2"]):
                            if(str(args.x_mode).lower() in ["q2"]): #   Q2 is varying → xB must vary with it (fixed y)
                                xB_stack = np.array([Convert_xB_var(Q2_in=qq, y_in=y__val, Var_out="xB") for qq in Q2_stack])
                            else:                                   #    y is varying → xB must vary with it (fixed Q2)
                                xB_stack = np.array([Convert_xB_var(Q2_in=Q2_val, y_in=yy, Var_out="xB") for yy in y__stack])
                        else:                                       # Varying z or pT → xB is fixed by Q2 and y
                            xB_stack = np.full(len(x_grid), Convert_xB_var(Q2_in=Q2_val, y_in=y__val, Var_out="xB"))
                        column_stack = np.column_stack([Q2_stack, y__stack, z__stack, pT_stack, xB_stack])
                    elif(args.dimension_mode == "4D_xB"):
                        if(str(args.x_mode).lower() == "xb"):
                            xB_stack = x_grid
                            if(len(Q2_grid) < 2):   # Assumes that Q2 is set to default values → let it vary with xB
                                Q2_stack = np.array([Convert_xB_var(xB_in=xb, Q2_in=Q2_val, y_in=y__val, Var_out="Q2") for xb in xB_stack])
                                # Q2_varies_with_xB = True
                            elif(len(y__grid) < 2): # Assumes that y  is set to default values → let it vary with xB
                                y__stack = np.array([Convert_xB_var(xB_in=xb, Q2_in=Q2_val, y_in=y__val, Var_out="y")  for xb in xB_stack])
                                # y__varies_with_xB = True
                            else:
                                raise SystemExit(f"{color.Error}ERROR:{color.END} Cannot plot xB while fixing BOTH Q2 and y.\n")
                        elif(str(args.x_mode).lower() in ["y", "q2"]):
                            if(str(args.x_mode).lower() in ["q2"]): #   Q2 is varying → xB must vary with it (fixed y)
                                xB_stack = np.array([Convert_xB_var(Q2_in=qq, y_in=y__val, Var_out="xB") for qq in Q2_stack])
                            else:                                   #    y is varying → xB must vary with it (fixed Q2)
                                xB_stack = np.array([Convert_xB_var(Q2_in=Q2_val, y_in=yy, Var_out="xB") for yy in y__stack])
                        else:                                       # Varying z or pT → xB is fixed by Q2 and y
                            xB_stack = np.full(len(x_grid), Convert_xB_var(Q2_in=Q2_val, y_in=y__val, Var_out="xB"))
                        column_stack = np.column_stack([xB_stack, y__stack, z__stack, pT_stack])
                    else:  # 4D — This version does not care about xB
                        column_stack = np.column_stack([Q2_stack, y__stack, z__stack, pT_stack])
                    query_points[f"Line_Num_{Line_Num}"] = {"column_stack": column_stack,
                                                            "Values": {"Q2": "Plotting" if(str(args.x_mode).lower() == "q2") else Q2_val                if(not Q2_varies_with_xB) else "Effected by Plotting",
                                                                       "y":  "Plotting" if(str(args.x_mode).lower() == "y")  else y__val                if(not y__varies_with_xB) else "Effected by Plotting",
                                                                       "z":      z__val if(str(args.x_mode).lower() != "z")  else "Plotting",
                                                                       "pT":     pT_val if(str(args.x_mode).lower() != "pt") else "Plotting",
                                                                       "xB": "Plotting" if(str(args.x_mode).lower() == "xb") else "See Q2" if(xB_is_Q2) else "See y" if(xB_is__y) else "Effected by Plotting" if(str(args.x_mode).lower() in ["y", "q2"]) else Convert_xB_var(Q2_in=Q2_val, y_in=y__val, Var_out="xB")
                                                                      }
                                                            }
    # Create canvases and draw
    y_grid, gr_spline, canvas_spline, legends, line_bins = {}, {}, {}, {}, {}
    for y_par in args.y_pars:
        if(y_par not in spline_models):
            print(f"{color.BYELLOW}[INFO] No spline loaded for {y_par}. Skipping.{color.END}")
            continue
        if(y_ranges is not None):
            y_min, y_max = y_ranges[y_par]
        else:
            if(str(y_par) == "Fit_Par_B"):
                # y_min, y_max = -0.8, 0.125
                y_min, y_max = -0.2, 0.125
            elif(str(y_par) == "Fit_Par_C"):
                y_min, y_max = -0.3, 0.25
            else:
                y_min, y_max = 0.0, 0.0
        use_log_y = use_log_y_for_par(args, y_par)
        if(use_log_y):
            y_min, y_max = ensure_positive_y_range_for_log(y_min, y_max)

        Titles_y = Get_Default_Y_Title(y_par, str(args.fit_set).strip())
        Titles = ""
        if("from the Cross Section Fits" not in Titles_y):
            Titles = f"#splitline{{#scale[1.75]{{CLAS12 Preliminary #topbar {Titles_y}}}}}{{{Build_SingleBin_Subtitle(args, str(args.fit_set).strip())}}}"
        else:
            Titles_y = Titles_y.replace(" from the Cross Section Fits", "")
            Titles = f"#splitline{{#splitline{{#scale[1.75]{{CLAS12 Preliminary #topbar {Titles_y}}}}}{{{Build_SingleBin_Subtitle(args, str(args.fit_set).strip())}}}}}{{Made From Normalized Cross Sections}}"
        Titles = f"{Titles}; {'Q^{2} [GeV^{2}]' if(str(args.x_mode).lower() == 'q2') else 'y' if(str(args.x_mode).lower() == 'y') else 'z' if(str(args.x_mode).lower() == 'z') else 'P_{T} [GeV]' if(str(args.x_mode).lower() == 'pt') else 'x_{B}' if(str(args.x_mode).lower() == 'xb') else 'ERROR'}; {Titles_y}"
        # Legend
        leg_x1 = 0.75
        leg_x0 = 0.0 # 0.25
        leg_y1 = 0.89
        entry_h = 0.055
        nlines = int(2 * len(query_points)) + 1
        leg_y0 = leg_y1 - entry_h * float(nlines)
        if(leg_y0 < 0.12):
            leg_y0 = 0.12
        legends[y_par] = ROOT.TLegend(float(leg_x0), float(leg_y0), float(leg_x1), float(leg_y1))
        legends[y_par].SetBorderSize(1)
        legends[y_par].SetFillStyle(1001)
        legends[y_par].SetTextFont(42)
        legends[y_par].SetTextSize(0.055)
        legends[y_par].SetHeader(str(legend_title), "C")

        y_grid[y_par], gr_spline[y_par] = {}, {}
        color_loop = -1
        for Line_Num, Line in enumerate(query_points):
            try:
                y_grid[y_par][Line] = spline_models[y_par](query_points[Line]["column_stack"])
            except Exception:
                try:
                    y_grid[y_par][Line] = spline_models[y_par](np.asarray(query_points[Line]["column_stack"], dtype=float))
                except Exception as ee:
                    raise SystemExit(f"{color.Error}ERROR:{color.END} Spline evaluation failed for {y_par} line {Line_Num}.\nException:\t{ee}\n")
            x_vals = x_grid # np.array(val for val in x_grid)
            # # Convert x-axis back to xB if needed
            # x_vals = query_points[Line]["column_stack"][:, 0] if(str(args.x_mode).lower() == "q2") else query_points[Line]["column_stack"][:, 1] if(str(args.x_mode).lower() == "y") else query_points[Line]["column_stack"][:, 2] if(str(args.x_mode).lower() == "z") else query_points[Line]["column_stack"][:, 3] if(args.dimension_mode == "4D") else query_points[Line]["column_stack"][:, 0] if(args.dimension_mode == "4D_xB") else query_points[Line]["column_stack"][:, 4]
            # if(args.x_mode in ["xB", "xb"]):
            #     x_vals = np.array([Convert_xB_var(xB_in=val, Q2_in=Q2_grid[0] if(len(Q2_grid) == 1) else None, y_in=y__grid[0] if(len(y__grid) == 1) else None, Var_out="xB") for val in x_vals])
            gr_spline[y_par][Line] = ROOT.TGraph(len(x_vals))
            for ip, (xx, yy) in enumerate(zip(x_vals, y_grid[y_par][Line])):
                gr_spline[y_par][Line].SetPoint(ip, float(xx), float(yy))
                if(str(y_par) not in ["Fit_Par_B", "Fit_Par_C"]):
                    y_min = min([y_min, yy, 0.8*yy, 1.2*yy])
                    y_min = 0
                    y_max = max([y_max, yy, 0.8*yy, 1.2*yy])
                elif(str(y_par) in ["Fit_Par_B"]):
                    y_min = -0.2
            # Color from your existing mapper
            color_index = Line_Num % len(color_mapper)
            color_gr = color_mapper[str(color_index + 1)] if(str(color_index + 1) in color_mapper) else ROOT.kRed
            if(color_index == 0):
                color_loop += 1
                gr_spline[y_par][Line].SetLineStyle(7)
            else:
                gr_spline[y_par][Line].SetLineStyle((11-color_index) if(color_index not in [0, 4]) else 2)
            color_gr += color_loop
            gr_spline[y_par][Line].SetLineColorAlpha(int(color_gr), 0.95)
            gr_spline[y_par][Line].SetLineWidth(2 if("pdf" not in str(args.formats)) else 1)
            gr_spline[y_par][Line].SetMarkerColorAlpha(int(color_gr), 0.95)
            if(str(color_loop) in marker_mapper):
                gr_spline[y_par][Line].SetMarkerSize(0.5)
                gr_spline[y_par][Line].SetMarkerStyle(marker_mapper[str(color_loop)])
            else:
                gr_spline[y_par][Line].SetMarkerSize(0)
                gr_spline[y_par][Line].SetMarkerStyle(8)
            # gr_spline[y_par][Line].SetMarkerStyle(29)
            gr_spline[y_par][Line].SetName(f"{y_par}_{Line}")
            gr_spline[y_par][Line].SetTitle(Titles)
            gr_spline[y_par][Line].GetXaxis().SetTitleSize(0.035)
            gr_spline[y_par][Line].GetYaxis().SetTitleSize(0.035)
            gr_spline[y_par][Line].GetXaxis().SetLabelSize(0.025)
            gr_spline[y_par][Line].GetYaxis().SetLabelSize(0.025)
            # Build legend entry
            Entry_Title = ""
            if("See"    in str(query_points[Line]["Values"]["xB"])):
                if("Q2" in str(query_points[Line]["Values"]["xB"])):
                    Entry_Title = f'x_{{B}} = {query_points[Line]["Values"]["Q2"]}' if("Plotting" not in str(query_points[Line]["Values"]["Q2"])) else ""
                if("y"  in str(query_points[Line]["Values"]["xB"])):
                    Entry_Title = f'x_{{B}} = {query_points[Line]["Values"]["y"]}'  if("Plotting" not in str(query_points[Line]["Values"]["y"]))  else ""
            else:
                for plot_var in query_points[Line]["Values"]:
                    if(getattr(args, f"Fixed_{plot_var}") is None):
                        continue
                    elif(len(getattr(args, f"Fixed_{plot_var}")) < 2):
                        continue
                    plot_var_title = plot_var if(plot_var in ["y", "z"]) else "Q^{2}" if(plot_var == "Q2") else "P_{T}" if(plot_var == "pT") else "x_{B}" if(plot_var in ["xB"]) else "Error"
                    if("Plotting" not in str(query_points[Line]["Values"][plot_var])):
                        Entry_Title = f'{plot_var_title} = {query_points[Line]["Values"][plot_var]}' if(Entry_Title == "") else f'#splitline{{{Entry_Title}}}{{{plot_var_title} = {query_points[Line]["Values"][plot_var]}}}'
            if(Entry_Title != ""):
                legends[y_par].AddEntry(gr_spline[y_par][Line], Entry_Title, "lp")
        # Create and save canvas
        Save_Name = f"{'' if(args.name in ['Mosaic_Image', '']) else f'{args.name}_'}Spline_Image_{args.spline_prefix}_{str(args.fit_set).strip()}_{y_par}_vs_{args.x_mode}"

        canvas_spline[Save_Name] = ROOT.TCanvas(Save_Name, Save_Name, int(args.single_canvas_width), int(args.single_canvas_height))
        canvas_spline[Save_Name].SetFillColor(0)
        # canvas_spline[Save_Name].SetMargin(0.0, 0.0, 0.0, 0.0)
        canvas_spline[Save_Name].Divide(2, 1)
        canvas_spline[Save_Name].cd(1)

        if(not hasattr(canvas_spline[Save_Name], "_keepalive")):
            canvas_spline[Save_Name]._keepalive = {}

        # Graph pad
        # pad_graph = ROOT.TPad(f"pad_graph_{Save_Name}", f"pad_graph_{Save_Name}", 0.0, 0.0, 0.73, 1.0)
        pad_graph = canvas_spline[Save_Name].cd(1) # ROOT.TPad(f"pad_graph_{Save_Name}", f"pad_graph_{Save_Name}", 0.0, 0.0, 1.0, 1.0)
        pad_graph.SetFillColor(0)
        pad_graph.SetPad(0.00, 0.00, 0.75, 1.00)
        # pad_graph.SetGrid(1, 1)
        pad_graph.SetLeftMargin(0.14)
        pad_graph.SetBottomMargin(0.13)
        pad_graph.SetRightMargin(0.03)
        pad_graph.SetTopMargin(0.12)
        if(use_log_y):
            pad_graph.SetLogy(1)
        pad_graph.Draw()
        pad_graph.cd()

        frame = pad_graph.DrawFrame(float(x_min), float(y_min), float(x_max), float(y_max))
        frame.SetTitle(Titles)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.035)
        frame.GetYaxis().SetLabelSize(0.035)
        canvas_spline[Save_Name]._keepalive["Frame"] = frame

        for Line in gr_spline[y_par]:
            pad_graph.Draw()
            pad_graph.cd()
            gr_spline[y_par][Line].GetYaxis().SetRangeUser(y_min, y_max)
            gr_spline[y_par][Line].Draw("P L SAME")
        if((str(args.x_mode).lower() in ["q2", "y", "xb"]) and (args.draw_legends)): # `draw_legends` is used here just to make these bin lines be optional — probably should change the argument later to not get confused since this image type always draws a TLegend and these lines have nothing to do with it
            Bin_centers = {"1": 2.2, "2": 2.65, "3": 3.3, "4": 4.5, "5": 6.6} if(str(args.x_mode).lower() == "q2") else {"1": 0.4, "2": 0.5, "3": 0.6, "4": 0.7} if(str(args.x_mode).lower() == "y") else {'1': 0.27650205, '2': 0.22120164, '3': 0.1843347, '4': 0.15800117, '5': 0.33305929, '6': 0.26644743, '7': 0.22203953, '8': 0.19031959, '9': 0.41475307, '10': 0.33180246, '11': 0.27650205, '12': 0.23700176, '13': 0.56557238, '14': 0.4524579, '15': 0.37704825, '16': 0.32318421, '17': 0.82950615, '18': 0.66360492, '19': 0.5530041, '20': 0.47400351}
            for ii in Bin_centers:
                if(f"{y_par}_bins_{ii}" not in line_bins):
                    line_bins[f"{y_par}_bins_{ii}"] = ROOT.TLine(Bin_centers[ii], y_min, Bin_centers[ii], y_max)
                    color_ii = (int(ii)%len(color_mapper)) + 1
                    # line_bins[f"{y_par}_bins_{ii}"].SetLineColorAlpha(color_mapper[str(color_ii)], 0.45)
                    line_bins[f"{y_par}_bins_{ii}"].SetLineColorAlpha(ROOT.kGray+2, 0.45)
                    line_bins[f"{y_par}_bins_{ii}"].SetLineWidth(2 if("pdf" not in str(args.formats)) else 1)
                pad_graph.cd()
                line_bins[f"{y_par}_bins_{ii}"].Draw("SAME")
            canvas_spline[Save_Name]._keepalive["Bin_Lines"] = line_bins

        Draw_SingleBin_Preliminary_Watermark(args)

        canvas_spline[Save_Name].cd(2)
        # Legend pad
        pad_legend = canvas_spline[Save_Name].cd(2) # ROOT.TPad(f"pad_legend_{Save_Name}", f"pad_legend_{Save_Name}", 0.73, 0.0, 1.0, 1.0)
        pad_legend.SetPad(0.75, 0.00, 1.00, 1.00)
        # pad_legend.SetFillColor(0)
        # pad_legend.SetLeftMargin(0.05)
        # pad_legend.SetRightMargin(0.05)
        # pad_legend.SetTopMargin(0.10)
        # pad_legend.SetBottomMargin(0.10)
        pad_legend.Draw()
        pad_legend.cd()
        legends[y_par].Draw("SAME")

        canvas_spline[Save_Name]._keepalive["TPad"] = {"Graph_Pad": pad_graph, "Legend_Pad": pad_legend}
        canvas_spline[Save_Name].cd()
        canvas_spline[Save_Name].Modified()
        canvas_spline[Save_Name].Update()

        if(not args.test):
            print(f"\n{color.BGREEN}Saving: {color.BPINK if('png' in args.formats) else color.END_B}{Save_Name}.{args.formats}{color.END}")
            canvas_spline[Save_Name].SaveAs(f"{Save_Name}.{args.formats}")
        else:
            print(f"\n{color.BBLUE}Would have Saved: {color.BPINK if('png' in args.formats) else color.END_B}{Save_Name}.{args.formats}{color.END}")

    args.timer.stop()
    return canvas_spline

# ------------------------------------------------------------
# Comparison-mode helpers (--comparison_mode)
# Error propagation (independent measurements):
#   overlay:     report each source e_i as stored
#   delta:       |v1-v2|,  err = sqrt(e1^2 + e2^2)
#   diff:        v1-v2,    err = sqrt(e1^2 + e2^2)
#   percent_dif: |100*(v1-v2)/v2|, err = 100*sqrt((e1/v2)^2 + (v1*e2/v2^2)^2)
# ------------------------------------------------------------
def normalize_fit_set_list(args):
    if(isinstance(args.fit_set, (list, tuple))):
        return [str(xx).strip() for xx in args.fit_set if(str(xx).strip() != "")]
    fs = str(args.fit_set).strip()
    return [fs] if(fs != "") else []

def normalize_json_file_list(args):
    if(isinstance(args.json_file, (list, tuple))):
        return [str(xx) for xx in args.json_file]
    return [str(args.json_file)]

def short_fit_set_label(fit_set):
    tag = Get_Default_FitSet_FileTag(fit_set)
    return tag if(tag != "") else sanitize_for_filename(str(fit_set).replace("Fit_Pars_from_", ""))

def build_comparison_sources(args):
    # Pair fit_set names with JSON files: equal counts → index pairing; else first-match scan in CLI order
    fit_sets = normalize_fit_set_list(args)
    json_files = normalize_json_file_list(args)
    if(len(fit_sets) == 0):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} --comparison_mode requires at least one --fit_set.{color.END}")
    if(len(json_files) == 0):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} --comparison_mode requires at least one --json_file.{color.END}")
    sources = []
    if(len(fit_sets) == len(json_files)):
        for ii in range(len(fit_sets)):
            json_obj = load_json(args, json_index=ii)
            fs = fit_sets[ii]
            if(fs not in json_obj):
                raise SystemExit(f"{color.Error}ERROR:{color.END_R} fit_set '{fs}' not found in JSON[{ii}] '{json_files[ii]}'.{color.END}")
            fit_dict = json_obj[fs]
            if((not isinstance(fit_dict, dict)) or (len(fit_dict) == 0)):
                raise SystemExit(f"{color.Error}ERROR:{color.END_R} fit_set '{fs}' empty in '{json_files[ii]}'.{color.END}")
            grouped = group_by_q2y(fit_dict)
            info_map = build_info_map(args, fit_dict)
            q2y_ranges = build_q2y_ranges(grouped, info_map)
            sources.append({"fit_set": fs, "json_path": json_files[ii], "json_index": ii, "fit_dict": fit_dict, "grouped": grouped, "info_map": info_map, "q2y_ranges": q2y_ranges, "label": short_fit_set_label(fs)})
    else:
        for fs in fit_sets:
            found = False
            for ii in range(len(json_files)):
                json_obj = load_json(args, json_index=ii)
                if(fs not in json_obj):
                    continue
                fit_dict = json_obj[fs]
                if((not isinstance(fit_dict, dict)) or (len(fit_dict) == 0)):
                    continue
                grouped = group_by_q2y(fit_dict)
                info_map = build_info_map(args, fit_dict)
                q2y_ranges = build_q2y_ranges(grouped, info_map)
                sources.append({"fit_set": fs, "json_path": json_files[ii], "json_index": ii, "fit_dict": fit_dict, "grouped": grouped, "info_map": info_map, "q2y_ranges": q2y_ranges, "label": short_fit_set_label(fs)})
                found = True
                break
            if(not found):
                raise SystemExit(f"{color.Error}ERROR:{color.END_R} fit_set '{fs}' not found in any provided --json_file.{color.END}")
    return sources

def get_entry_value_error(args, fit_dict, key_str, y_par, q2y_bin, zpt_bin):
    err_key = f"{y_par}{args.err_suffix}"
    if((key_str not in fit_dict) or (y_par not in fit_dict[key_str]) or (err_key not in fit_dict[key_str])):
        return None
    yval = float(fit_dict[key_str][y_par])
    yerr = float(fit_dict[key_str][err_key])
    if((getattr(args, "apply_A_corr", False)) and (str(y_par) == "Fit_Par_A")):
        _, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y_bin, z_pT_Bin=zpt_bin, args_in=args)
        if((str(Bin_Width_Area_Scale) not in ["0", "None", None]) and (str(Luminosity) not in ["0", "None", None])):
            yval = yval / (Bin_Width_Area_Scale * Luminosity)
            yerr = yerr / (Bin_Width_Area_Scale * Luminosity)
    return (yval, abs(yerr))

def compute_pair_comparison(ctype, v1, e1, v2, e2):
    # Returns (value, error) or None if undefined
    # delta: |v1-v2| with err sqrt(e1^2+e2^2); diff: v1-v2 same err;
    # percent_dif: |100*(v1-v2)/v2| (always ≥0) with quotient-propagation error
    e_comb = float(np.sqrt((e1 ** 2) + (e2 ** 2)))
    if(ctype == "delta"):
        return (abs(v1 - v2), e_comb)
    if(ctype == "diff"):
        return (v1 - v2, e_comb)
    if(ctype == "percent_dif"):
        if(abs(v2) < 1e-30):
            return None
        val = abs(100.0 * (v1 - v2) / v2)
        err = 100.0 * float(np.sqrt(((e1 / v2) ** 2) + (((v1 * e2) / (v2 ** 2)) ** 2)))
        return (val, err)
    return None

def comparison_type_title(ctype):
    if(ctype == "delta"):
        return "Absolute Difference"
    if(ctype == "diff"):
        return "Difference"
    if(ctype == "percent_dif"):
        return "Percent Difference"
    if(ctype == "overlay"):
        return "Overlay"
    return str(ctype)

def format_value_pm_error(val, err):
    return f"{val:.6g}±{err:.6g}"

def build_synthetic_fit_dict_for_pair(args, source_a, source_b, y_par, ctype):
    # Build a fit_dict of comparison values for bins present in both sources (reuses draw_mosaic layout)
    err_key = f"{y_par}{args.err_suffix}"
    out = {}
    for key_str in source_a["fit_dict"].keys():
        if(key_str not in source_b["fit_dict"]):
            continue
        try:
            q2y_bin, zpt_bin = parse_inner_key(key_str)
        except Exception:
            continue
        ve1 = get_entry_value_error(args, source_a["fit_dict"], key_str, y_par, q2y_bin, zpt_bin)
        ve2 = get_entry_value_error(args, source_b["fit_dict"], key_str, y_par, q2y_bin, zpt_bin)
        if((ve1 is None) or (ve2 is None)):
            continue
        cmp = compute_pair_comparison(ctype, ve1[0], ve1[1], ve2[0], ve2[1])
        if(cmp is None):
            continue
        out[key_str] = {y_par: float(cmp[0]), err_key: float(cmp[1])}
    return out

def comparison_log_requested(args):
    # Any explicit log-scale CLI flag enables optional log for eligible comparison images
    return bool(getattr(args, "draw_with_log_A", False) or getattr(args, "log_abs_diff", False))

def write_comparison_table(args, sources, y_par):
    # One txt table per y_par; columns use readable titles (no raw underscores); final Averages row
    err_key = f"{y_par}{args.err_suffix}"
    ctypes = list(getattr(args, "comparison_types", ["overlay"]))
    y_tag = Get_Default_Y_FileTag(y_par, sources[0]["fit_set"])
    labels = [src["label"] for src in sources]
    stem = sanitize_for_filename(args.name)
    filename = f"{stem}_Compare_Table_{y_tag}.txt"
    Validate_Output_Filename(filename)

    # Union of keys across sources
    all_keys = set()
    for src in sources:
        all_keys.update(src["fit_dict"].keys())
    key_list = sorted(list(all_keys), key=lambda kk: parse_inner_key(kk))

    headers = ["Q2-y Bin", "z-pT Bin"]
    for lab in labels:
        headers.append(str(lab))
    pair_specs = []
    for ctype in ctypes:
        if(ctype == "overlay"):
            continue
        for ia in range(len(sources)):
            for ib in range(ia + 1, len(sources)):
                title = f"{comparison_type_title(ctype)} ({labels[ia]} vs {labels[ib]})"
                headers.append(title)
                pair_specs.append((ctype, ia, ib, title))

    col_vals = [[] for _ in headers]  # collect numeric means for Averages row (value part only for ± columns)
    col_errs = [[] for _ in headers]

    lines = []
    lines.append("\t".join(headers))
    for key_str in key_list:
        try:
            q2y_bin, zpt_bin = parse_inner_key(key_str)
        except Exception:
            continue
        # Prefer first source that has this key for range labels
        q2y_lab = str(q2y_bin)
        zpt_lab = str(zpt_bin)
        for src in sources:
            if(key_str in src["info_map"]):
                inf = src["info_map"][key_str]
                q2 = inf["Q2range"]
                yy = inf["y_range"]
                zz = inf["z_range"]
                pt = inf["pTrange"]
                q2y_lab = f"{q2y_bin} (Q2 {q2[1]:.3g}-{q2[2]:.3g}, y {yy[1]:.3g}-{yy[2]:.3g})"
                zpt_lab = f"{zpt_bin} (z {zz[1]:.3g}-{zz[2]:.3g}, pT {pt[1]:.3g}-{pt[2]:.3g})"
                break
        row = [q2y_lab, zpt_lab]
        # source columns
        for isrc, src in enumerate(sources):
            ve = get_entry_value_error(args, src["fit_dict"], key_str, y_par, q2y_bin, zpt_bin)
            if(ve is None):
                row.append("---")
            else:
                row.append(format_value_pm_error(ve[0], ve[1]))
                col_vals[2 + isrc].append(ve[0])
                col_errs[2 + isrc].append(ve[1])
        # pair comparison columns
        for ip, (ctype, ia, ib, title) in enumerate(pair_specs):
            ve1 = get_entry_value_error(args, sources[ia]["fit_dict"], key_str, y_par, q2y_bin, zpt_bin)
            ve2 = get_entry_value_error(args, sources[ib]["fit_dict"], key_str, y_par, q2y_bin, zpt_bin)
            col_i = 2 + len(sources) + ip
            if((ve1 is None) or (ve2 is None)):
                row.append("---")
                continue
            cmp = compute_pair_comparison(ctype, ve1[0], ve1[1], ve2[0], ve2[1])
            if(cmp is None):
                row.append("---")
                continue
            row.append(format_value_pm_error(cmp[0], cmp[1]))
            col_vals[col_i].append(cmp[0])
            col_errs[col_i].append(cmp[1])
        lines.append("\t".join(row))

    # Averages row: mean of values; uncertainty = std of values (population), not mean of errs
    avg_row = ["Averages", ""]
    for ic in range(2, len(headers)):
        if(len(col_vals[ic]) == 0):
            avg_row.append("---")
            continue
        arr = np.asarray(col_vals[ic], dtype=float)
        mean_v = float(np.mean(arr))
        std_v = float(np.std(arr, ddof=0))
        avg_row.append(format_value_pm_error(mean_v, std_v))
    lines.append("\t".join(avg_row))

    header_note = [
        f"# Comparison table for {y_par} ({Get_Default_Y_Title(y_par, sources[0]['fit_set'])})",
        f"# Sources: " + "; ".join([f"{src['label']} <= {src['fit_set']} from {src['json_path']}" for src in sources]),
        f"# Comparison types: {', '.join(ctypes)}",
        "# Error propagation: overlay uses source errors; delta/diff use sqrt(e1^2+e2^2); percent_dif uses |100*(v1-v2)/v2| with 100*sqrt((e1/v2)^2+(v1*e2/v2^2)^2)",
        "# Averages row: column mean ± population std of the row values in that column",
        "",
    ]
    if(not args.test):
        with open(filename, "w") as outf:
            outf.write("\n".join(header_note))
            outf.write("\n".join(lines))
            outf.write("\n")
        print(f"{color.GREEN}[INFO] Wrote comparison table: {filename}{color.END}")
    else:
        print(f"{color.BYELLOW}[TEST] Would write comparison table: {filename}{color.END}")
    return filename

def comparison_source_line_style(src, source_index, sources):
    # Dim-based styles when dimensions differ: 5D solid (1), 3D dashed (2). Data always from src; style tied to same src.
    # Fallback: higher source_index → dashed variants. Markers vary by index only.
    markers = [20, 21, 22, 23, 24, 25, 26, 29, 33, 34]
    dims = [parse_fit_set_features(s["fit_set"])["dim"] for s in sources]
    unique_dims = [d for d in dict.fromkeys(dims) if(d != "")]
    feat = parse_fit_set_features(src["fit_set"])
    dim = feat["dim"]
    if((len(unique_dims) >= 2) and (dim != "")):
        if(dim == "5D"):
            lsty = 1
        elif(dim == "3D"):
            lsty = 2
        else:
            # Remaining dims: cycle 7,9,10 after solid/dashed reserved
            other = [d for d in unique_dims if(d not in ["5D", "3D"])]
            lsty = [7, 9, 10][other.index(dim) % 3] if(dim in other) else 7
    else:
        lsty = [1, 2, 7, 9, 10][source_index % 5]
    mark = markers[source_index % len(markers)]
    return (mark, int(lsty))

def comparison_source_draw_style(source_index, base_color, base_marker, src=None, sources=None):
    if((src is not None) and (sources is not None)):
        mark, lsty = comparison_source_line_style(src, source_index, sources)
        return (int(base_color), mark, lsty)
    line_styles = [1, 2, 7, 9, 10]
    markers = [20, 21, 22, 23, 24, 25, 26, 29, 33, 34]
    return (int(base_color), markers[source_index % len(markers)], line_styles[source_index % len(line_styles)])

def build_adaptive_source_legend_box(n_entries, phrases, x1=0.02, y1=0.56):
    # Content-based size; grow up/right from (x1,y1); capped so it stays left of bin 15 / above bin 12
    max_len = max([len(str(p)) for p in phrases]) if(len(phrases) > 0) else 4
    w = min(0.22, max(0.10, 0.06 + 0.008 * float(max_len)))
    h = min(0.18, max(0.06, 0.035 + 0.028 * float(n_entries + 1)))
    return (float(x1), float(y1), float(x1 + w), float(y1 + h))

def draw_mosaic_comparison_overlay(args, sources, y_par, x_range, y_range, y_axis_title_override=None):
    # Multi-source overlay on the same pads; no spline / range bands; original per-pad bin legends
    mapping, max_cols, nrows = build_layout_map(args)
    c1 = ROOT.TCanvas(f"c_cmp_overlay_{y_par}", f"c_cmp_overlay_{y_par}", int(args.canvas_width), int(args.canvas_height))
    c1.SetFillColor(0)
    c1.SetFillStyle(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)
    if(not hasattr(c1, "_keepalive")):
        c1._keepalive = []
    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])
    use_log_y = use_log_y_for_par(args, y_par)
    if(use_log_y):
        gymin, gymax = ensure_positive_y_range_for_log(gymin, gymax)
    # Extra headroom for multi-line comparison titles (#splitline nesting)
    title_space = 0.120 if(args.title_mode != "none") else 0.00
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    if(y_axis_title_override is not None):
        y_axis_title = str(y_axis_title_override)
    else:
        y_axis_title = comparison_y_axis_title(y_par, sources[0]["fit_set"], "overlay")
    ref_q2y = sources[0]["q2y_ranges"]
    # Prefer first source that has the bin for complementary-bin legend values
    primary = sources[0]

    row_bins = {}
    for q2y_bin in mapping.keys():
        row, col, col_start = mapping[q2y_bin]
        if(row not in row_bins):
            row_bins[row] = []
        row_bins[row].append((col, q2y_bin, col_start))
    for row in row_bins.keys():
        row_bins[row].sort(key=lambda tt: tt[0])
    x_edges = {}
    right_margin = 0.0
    left_small = 0.0
    left_big = 0.22
    for row in row_bins.keys():
        pads = row_bins[row]
        n_present = len(pads)
        big_flags = []
        for col, q2y_bin, col_start in pads:
            is_leftmost_present = (col == col_start)
            big_flags.append((args.label_mode == "all") or ((args.label_mode == "outer") and is_leftmost_present))
        n_big = sum([1 for bb in big_flags if(bb)])
        if((args.label_mode == "all") or (n_big == 0)):
            width_each = 1.0 / float(max_cols)
            widths = [width_each for _ in range(n_present)]
        else:
            plot_frac_small = 1.0 - left_small - right_margin
            plot_frac_big = 1.0 - left_big - right_margin
            ratio = plot_frac_small / plot_frac_big
            width_small = 1.0 / (float(max_cols - 1) + float(ratio))
            width_big = width_small * ratio
            widths = [(width_big if(big_flags[i]) else width_small) for i in range(n_present)]
        target_total = sum(widths)
        x_start = 1.0 - target_total
        cursor = x_start
        for i, (col, q2y_bin, col_start) in enumerate(pads):
            x0 = cursor
            cursor = cursor + widths[i]
            x1 = cursor
            if(i == (n_present - 1)):
                x1 = 1.0
                cursor = x1
            x_edges[q2y_bin] = (float(x0), float(x1))

    for q2y_bin in range(1, int(args.q2y_count) + 1):
        if(q2y_bin not in mapping):
            continue
        row, col, col_start = mapping[q2y_bin]
        x0, x1 = x_edges[q2y_bin]
        y0 = (float(row) / float(nrows)) * (1.0 - title_space)
        y1 = (float(row + 1) / float(nrows)) * (1.0 - title_space)
        pad = ROOT.TPad(f"pad_cmp_ov_{q2y_bin}_{y_par}", f"pad_cmp_ov_{q2y_bin}_{y_par}", float(x0), float(y0), float(x1), float(y1))
        pad.SetFillColor(0)
        pad.SetFillStyle(0)
        pad.SetFrameFillStyle(0)
        pad.SetFrameLineWidth(int(args.frame_line_width))
        pad.SetTickx(1)
        pad.SetTicky(1)
        pad.SetGrid(1, 1)
        is_bottom, is_leftmost_present, is_rightmost_present, is_top = pad_is_outer(row, col, col_start, max_cols, nrows)
        left_margin = 0.22 if((args.label_mode == "outer") and (is_leftmost_present)) else (0.22 if(args.label_mode == "all") else 0)
        bottom_margin = 0.20 if((args.label_mode == "outer") and (is_bottom)) else (0.20 if(args.label_mode == "all") else 0)
        pad.SetLeftMargin(float(left_margin))
        pad.SetBottomMargin(float(bottom_margin))
        pad.SetRightMargin(0)
        pad.SetTopMargin(0)
        if(use_log_y):
            pad.SetLogy(1)
        pad.Draw()
        pad.cd()
        frame = pad.DrawFrame(xmin, gymin, xmax, gymax)
        c1._keepalive.append(frame)
        frame.SetTitle("")
        frame.GetXaxis().SetTitle(x_axis_title if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_bottom))) else "")
        frame.GetYaxis().SetTitle(y_axis_title if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_leftmost_present))) else "")
        frame.GetXaxis().SetTitleSize(0.080 if((args.label_mode == "all") or is_bottom) else 0.0)
        frame.GetYaxis().SetTitleSize(0.080 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        frame.GetXaxis().SetLabelSize(0.070 if((args.label_mode == "all") or is_bottom) else 0.0)
        frame.GetYaxis().SetLabelSize(0.070 if((args.label_mode == "all") or is_leftmost_present) else 0.0)
        if((args.label_mode == "all") or ((args.label_mode == "outer") and (is_leftmost_present))):
            frame.GetYaxis().SetTitleOffset(0.85)
        frame.GetXaxis().SetNdivisions(505)
        frame.GetYaxis().SetNdivisions(505)

        # Draw all sources; keep per-pad legend from primary source only (original compact design)
        for isrc, src in enumerate(sources):
            series_map = build_series_for_q2y(args, src["grouped"], src["fit_dict"], src["info_map"], q2y_bin, y_par)
            sid_list = sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)
            for sid in sid_list:
                pts = series_map[sid]["points"]
                if(len(pts) == 0):
                    continue
                colr, mark, lsty = comparison_source_draw_style(isrc, series_map[sid]["color"], series_map[sid]["marker"], src=src, sources=sources)
                colr = int(series_map[sid]["color"])
                gr = ROOT.TGraphErrors(len(pts))
                for ip, (xx, yy, ey, key_str) in enumerate(pts):
                    gr.SetPoint(ip, float(xx), float(yy))
                    xerr = 0.0
                    if(args.x_error_bars):
                        if(str(args.x_mode).lower() == "z"):
                            xw = float(src["info_map"][key_str]["z_range"][2]) - float(src["info_map"][key_str]["z_range"][1])
                        else:
                            xw = float(src["info_map"][key_str]["pTrange"][2]) - float(src["info_map"][key_str]["pTrange"][1])
                        xerr = 0.5 * float(args.x_error_fraction) * float(xw)
                    gr.SetPointError(ip, float(xerr), float(ey))
                style_graph(gr, colr, mark, line_width=2 if("pdf" not in str(args.formats)) else 1)
                gr.SetLineStyle(int(lsty))
                draw_opt = "P L SAME"
                if(args.x_error_bars):
                    draw_opt = "P E1 SAME"
                gr.Draw(draw_opt)
                c1._keepalive.append(gr)

        if(args.draw_legends):
            series_map_leg = build_series_for_q2y(args, primary["grouped"], primary["fit_dict"], primary["info_map"], q2y_bin, y_par)
            sid_list_leg = sorted(list(series_map_leg.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)
            legend_title = "P_{T} Bins" if(args.x_mode == "z") else "z Bins"
            legend_entries = []
            for sid in sid_list_leg:
                pts = series_map_leg[sid]["points"]
                if(len(pts) == 0):
                    continue
                key0 = pts[0][3]
                if(key0 not in primary["info_map"]):
                    continue
                other_val = float(primary["info_map"][key0]["pTrange"][0]) if(args.x_mode == "z") else float(primary["info_map"][key0]["z_range"][0])
                legend_entries.append((other_val, int(series_map_leg[sid]["color"])))
            legend_entries.sort(key=lambda tt: tt[0])
            if(len(legend_entries) > 0):
                leg_x1 = 0.98
                leg_x0 = 0.78
                leg_y1 = 0.89
                entry_h = 0.055
                nlines = int(2 * len(legend_entries)) + 1
                leg_y0 = leg_y1 - entry_h * float(nlines)
                if(leg_y0 < 0.12):
                    leg_y0 = 0.12
                leg = ROOT.TLegend(float(leg_x0), float(leg_y0), float(leg_x1), float(leg_y1))
                leg.SetBorderSize(1)
                leg.SetFillStyle(1001)
                leg.SetFillColor(ROOT.kWhite)
                leg.SetTextFont(42)
                leg.SetTextSize(0.055)
                leg.SetHeader(str(legend_title), "C")
                for val, colv in legend_entries:
                    ent = leg.AddEntry(0, f"{val:.3f}", "")
                    if(ent):
                        ent.SetTextColor(int(colv))
                leg.Draw("SAME")
                c1._keepalive.append(leg)

        draw_pad_label(args, q2y_bin, ref_q2y)
        pad.Update()
        c1.cd()

    # Canvas-level source/style legend; default on for overlay unless --toggle_source_legend
    # Styles must match the same comparison_source_line_style used when drawing graphs
    show_src_leg = (not bool(getattr(args, "toggle_source_legend", False)))
    if(show_src_leg and (len(sources) >= 1)):
        phrases, _shared = build_comparison_source_phrases(sources)
        c1.cd()
        x1, y1, x2, y2 = build_adaptive_source_legend_box(len(sources), phrases, x1=0.02, y1=0.56)
        leg_src = ROOT.TLegend(float(x1), float(y1), float(x2), float(y2))
        leg_src.SetBorderSize(1)
        leg_src.SetFillStyle(1001)
        leg_src.SetFillColor(ROOT.kWhite)
        leg_src.SetTextFont(42)
        leg_src.SetTextSize(0.018)
        leg_src.SetHeader("Sources", "C")
        for isrc, src in enumerate(sources):
            phrase = phrases[isrc] if(isrc < len(phrases)) else src.get("label", f"Source {isrc}")
            mark, lsty = comparison_source_line_style(src, isrc, sources)
            dummy = ROOT.TGraph(1)
            dummy.SetLineColor(ROOT.kBlack)
            dummy.SetMarkerColor(ROOT.kBlack)
            dummy.SetLineStyle(int(lsty))
            dummy.SetLineWidth(2)
            dummy.SetMarkerStyle(int(mark))
            c1._keepalive.append(dummy)
            leg_src.AddEntry(dummy, str(phrase), "lp")
            if(args.verbose):
                print(f"{color.CYAN}[INFO] Source style: fit_set={src['fit_set']} phrase={phrase} lineStyle={lsty} marker={mark}{color.END}")
        leg_src.Draw()
        c1._keepalive.append(leg_src)

    c1.Update()
    return c1

def Build_Comparison_Output_Filename(args, y_par, kind_title, pair_labels=None, extra_tag=""):
    stem = sanitize_for_filename(args.name)
    x_tag = "pT" if(str(args.x_mode).lower() == "pt") else "z"
    y_tag = Get_Default_Y_FileTag(y_par, "Compare")
    kind_tag = sanitize_for_filename(kind_title)
    extra = f"_{sanitize_for_filename(extra_tag)}" if(str(extra_tag).strip() != "") else ""
    if(pair_labels is None):
        filename = f"{stem}_Compare_{kind_tag}{extra}_{x_tag}_{y_tag}.{args.formats}"
    else:
        pair_tag = sanitize_for_filename(f"{pair_labels[0]} vs {pair_labels[1]}")
        filename = f"{stem}_Compare_{kind_tag}_{pair_tag}{extra}_{x_tag}_{y_tag}.{args.formats}"
    Validate_Output_Filename(filename)
    return filename

def run_comparison_plots(args, sources):
    # Overlay and/or pairwise difference mosaics (and optional single-bin)
    ctypes = list(getattr(args, "comparison_types", ["overlay"]))
    ref = sources[0]
    if(args.global_x_range is not None):
        xmin, xmax = float(args.global_x_range[0]), float(args.global_x_range[1])
    else:
        xmin, xmax = compute_global_x_range(args, ref["grouped"], ref["info_map"])
    if(args.draw_legends):
        xspan = xmax - xmin
        xmax = xmax + (0.30 * xspan if(xspan > 0.0) else 1.0)

    do_single = bool(args.single_bin)
    q2y_bin = int(args.single_q2y_bin) if(do_single) else None

    if("overlay" in ctypes):
        for y_par in args.y_pars:
            if(args.y_range_mode == "global"):
                if(args.global_y_range is not None):
                    y_range = (float(args.global_y_range[0]), float(args.global_y_range[1]))
                else:
                    ymin, ymax = None, None
                    for src in sources:
                        lo, hi = compute_global_y_range(args, src["grouped"], src["fit_dict"], y_par)
                        ymin = lo if(ymin is None) else min(ymin, lo)
                        ymax = hi if(ymax is None) else max(ymax, hi)
                    y_range = (ymin, ymax) if((ymin is not None) and (ymax is not None)) else (0.0, 1.0)
            else:
                y_range = (0.0, 1.0)
            if(do_single):
                if(str(y_par) == "Fit_Par_B"):
                    y_range = (-0.8, 0.125)
                elif(str(y_par) == "Fit_Par_C"):
                    y_range = (-0.3, 0.25)
            yat = comparison_y_axis_title(y_par, sources[0]["fit_set"], "overlay")
            if(args.test):
                print(f"{color.BYELLOW}[TEST] Would draw comparison overlay for {y_par}{color.END}")
                continue
            if(do_single):
                canv = draw_single_bin_comparison_overlay(args, sources, y_par, q2y_bin, (xmin, xmax), y_range)
            else:
                canv = draw_mosaic_comparison_overlay(args, sources, y_par, (xmin, xmax), y_range, y_axis_title_override=yat)
            title_text = build_comparison_canvas_title(args, sources, y_par, "overlay")
            draw_global_title(args, canv, title_text)
            canv.Update()
            out_name = Build_Comparison_Output_Filename(args, y_par, "Overlay")
            if(do_single):
                out_name = out_name.replace(f".{args.formats}", f"_SingleBin_Q2yBin{int(q2y_bin)}.{args.formats}")
                Validate_Output_Filename(out_name)
            canv.SaveAs(out_name)
            print(f"{color.GREEN}[INFO] Wrote: {out_name}{color.END}")

    for ctype in ctypes:
        if(ctype == "overlay"):
            continue
        for ia in range(len(sources)):
            for ib in range(ia + 1, len(sources)):
                pair_sources = [sources[ia], sources[ib]]
                for y_par in args.y_pars:
                    fit_dict_cmp = build_synthetic_fit_dict_for_pair(args, sources[ia], sources[ib], y_par, ctype)
                    if(len(fit_dict_cmp) == 0):
                        print(f"{color.BYELLOW}[INFO] No overlapping bins for {ctype} {sources[ia]['label']} vs {sources[ib]['label']} ({y_par}){color.END}")
                        continue
                    saved_cs = bool(getattr(args, "apply_A_corr", False))
                    saved_log_A = bool(getattr(args, "draw_with_log_A", False))
                    args.apply_A_corr = False
                    # signed diff can be ≤0 → never log; percent_dif is |%| and may log if triggered below
                    if(str(ctype) == "diff"):
                        args.draw_with_log_A = False
                    # For diff/percent_dif: keep full error bars on points, but set axis from values only
                    range_no_err = (str(ctype) in ["diff", "percent_dif"])
                    grouped = group_by_q2y(fit_dict_cmp)
                    info_map = build_info_map(args, fit_dict_cmp)
                    q2y_ranges = build_q2y_ranges(grouped, info_map)
                    if(args.y_range_mode == "global"):
                        if(args.global_y_range is not None):
                            y_range = (float(args.global_y_range[0]), float(args.global_y_range[1]))
                        else:
                            y_range = compute_global_y_range(args, grouped, fit_dict_cmp, y_par, include_errors=(not range_no_err))
                    else:
                        y_range = (0.0, 1.0)
                    kind = comparison_type_title(ctype)
                    pair_phrases, _sh = build_comparison_source_phrases(pair_sources)
                    pair_labs = (pair_phrases[0], pair_phrases[1]) if(len(pair_phrases) >= 2) else (sources[ia]["label"], sources[ib]["label"])
                    yat = comparison_y_axis_title(y_par, sources[ia]["fit_set"], ctype)
                    # Log Y: delta with --log_abs_diff; percent_dif if log flag(s) set and any |%| > 10
                    force_log = bool((str(ctype) == "delta") and getattr(args, "log_abs_diff", False))
                    if((str(ctype) == "percent_dif") and comparison_log_requested(args)):
                        vals = [abs(float(ent[y_par])) for ent in fit_dict_cmp.values() if((y_par in ent) and np.isfinite(float(ent[y_par])))]
                        if((len(vals) > 0) and (max(vals) > 10.0)):
                            force_log = True
                            args.draw_with_log_A = False  # force_log_y alone drives axis for this image
                    if(force_log):
                        # Drop non-positive comparison values for valid log axes
                        fit_dict_pos = {}
                        for kk, ent in fit_dict_cmp.items():
                            if((y_par in ent) and (float(ent[y_par]) > 0.0) and np.isfinite(float(ent[y_par]))):
                                fit_dict_pos[kk] = ent
                        fit_dict_cmp = fit_dict_pos
                        if(len(fit_dict_cmp) == 0):
                            print(f"{color.BYELLOW}[INFO] No positive comparison points for log axis ({ctype}, {y_par}){color.END}")
                            args.apply_A_corr = saved_cs
                            args.draw_with_log_A = saved_log_A
                            continue
                        grouped = group_by_q2y(fit_dict_cmp)
                        info_map = build_info_map(args, fit_dict_cmp)
                        q2y_ranges = build_q2y_ranges(grouped, info_map)
                        y_range = compute_global_y_range(args, grouped, fit_dict_cmp, y_par, include_errors=(not range_no_err))
                        # percent_dif log: anchor lower bound at 0 (ROOT then uses a tiny positive floor)
                        if(str(ctype) == "percent_dif"):
                            y_range = (0.0, float(y_range[1]))
                        y_range = ensure_positive_y_range_for_log(y_range[0], y_range[1])
                    if(args.test):
                        print(f"{color.BYELLOW}[TEST] Would draw {kind} for {pair_labs} {y_par}{color.END}")
                        args.apply_A_corr = saved_cs
                        args.draw_with_log_A = saved_log_A
                        continue
                    c_suffix = f"_{sanitize_for_filename(ctype)}_{ia}_{ib}{'_log' if(force_log) else ''}"
                    if(do_single):
                        if(q2y_bin not in grouped):
                            args.apply_A_corr = saved_cs
                            args.draw_with_log_A = saved_log_A
                            continue
                        if((not force_log) and (str(y_par) == "Fit_Par_B")):
                            y_range = (-0.8, 0.125)
                        elif((not force_log) and (str(y_par) == "Fit_Par_C")):
                            y_range = (-0.3, 0.25)
                        elif(not force_log):
                            y_range = Compute_SingleBin_AutoYRange(build_series_for_q2y(args, grouped, fit_dict_cmp, info_map, int(q2y_bin), y_par))
                        canv = draw_single_bin(args, grouped, fit_dict_cmp, info_map, q2y_ranges, sources[ia]["fit_set"], y_par, q2y_bin, (xmin, xmax), y_range, spline_models={}, y_axis_title_override=yat, force_log_y=force_log)
                    else:
                        canv = draw_mosaic(args, grouped, fit_dict_cmp, info_map, q2y_ranges, sources[ia]["fit_set"], y_par, (xmin, xmax), y_range, spline_models={}, y_axis_title_override=yat, canvas_name_suffix=c_suffix, title_space_override=0.120, force_log_y=force_log)
                    title_text = build_comparison_canvas_title(args, pair_sources, y_par, ctype)
                    draw_global_title(args, canv, title_text)
                    canv.Update()
                    out_name = Build_Comparison_Output_Filename(args, y_par, kind, pair_labs, extra_tag=("logY" if(force_log) else ""))
                    if(do_single):
                        out_name = out_name.replace(f".{args.formats}", f"_SingleBin_Q2yBin{int(q2y_bin)}.{args.formats}")
                        Validate_Output_Filename(out_name)
                    canv.SaveAs(out_name)
                    print(f"{color.GREEN}[INFO] Wrote: {out_name}{color.END}")
                    # Keep canvas alive until process end to avoid ROOT double-delete on reuse
                    if(not hasattr(args, "_cmp_canvas_keepalive")):
                        args._cmp_canvas_keepalive = []
                    args._cmp_canvas_keepalive.append(canv)
                    args.apply_A_corr = saved_cs
                    args.draw_with_log_A = saved_log_A

def draw_single_bin_comparison_overlay(args, sources, y_par, q2y_bin, x_range, y_range):
    c1 = ROOT.TCanvas(f"c_cmp_ov_single_{y_par}_{q2y_bin}", f"c_cmp_ov_single_{y_par}_{q2y_bin}", int(args.single_canvas_width), int(args.single_canvas_height))
    c1.SetFillColor(0)
    c1.SetFillStyle(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)
    if(not hasattr(c1, "_keepalive")):
        c1._keepalive = []
    top_margin = 0.16
    pad = ROOT.TPad(f"pad_cmp_ov_single_{y_par}_{q2y_bin}", f"pad_cmp_ov_single_{y_par}_{q2y_bin}", 0.0, 0.0, 1.0, 1.0)
    pad.SetFillColor(0)
    pad.SetFillStyle(0)
    pad.SetFrameFillStyle(0)
    pad.SetGrid(1, 1)
    pad.SetLeftMargin(0.14)
    pad.SetBottomMargin(0.12)
    pad.SetRightMargin(0.04)
    pad.SetTopMargin(top_margin)
    use_log_y = use_log_y_for_par(args, y_par)
    if(use_log_y):
        pad.SetLogy(1)
    pad.Draw()
    pad.cd()
    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])
    if(use_log_y):
        gymin, gymax = ensure_positive_y_range_for_log(gymin, gymax)
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
    y_axis_title = Get_Default_Y_Title(y_par, sources[0]["fit_set"]).replace("from the Cross Section Fits", "")
    frame = pad.DrawFrame(xmin, gymin, xmax, gymax)
    c1._keepalive.append(frame)
    frame.SetTitle("")
    frame.GetXaxis().SetTitle(x_axis_title)
    frame.GetYaxis().SetTitle(y_axis_title)
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetYaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.025)
    frame.GetYaxis().SetLabelSize(0.025)
    Draw_SingleBin_Preliminary_Watermark(args)
    for isrc, src in enumerate(sources):
        series_map = build_series_for_q2y(args, src["grouped"], src["fit_dict"], src["info_map"], int(q2y_bin), y_par)
        for sid in sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss):
            pts = series_map[sid]["points"]
            if(len(pts) == 0):
                continue
            colr, mark, lsty = comparison_source_draw_style(isrc, series_map[sid]["color"], series_map[sid]["marker"], src=src, sources=sources)
            colr = int(series_map[sid]["color"])
            gr = ROOT.TGraphErrors(len(pts))
            for ip, (xx, yy, ey, key_str) in enumerate(pts):
                gr.SetPoint(ip, float(xx), float(yy))
                xerr = 0.0
                if(args.x_error_bars):
                    if(str(args.x_mode).lower() == "z"):
                        xw = float(src["info_map"][key_str]["z_range"][2]) - float(src["info_map"][key_str]["z_range"][1])
                    else:
                        xw = float(src["info_map"][key_str]["pTrange"][2]) - float(src["info_map"][key_str]["pTrange"][1])
                    xerr = 0.5 * float(args.x_error_fraction) * float(xw)
                gr.SetPointError(ip, float(xerr), float(ey))
            style_graph(gr, colr, mark, line_width=1)
            gr.SetLineStyle(int(lsty))
            draw_opt = "P E1 L SAME"
            if(args.x_error_bars):
                draw_opt = "P E1 SAME"
            gr.Draw(draw_opt)
            c1._keepalive.append(gr)
    Draw_SingleBin_Q2yText(int(q2y_bin), sources[0]["q2y_ranges"])
    Draw_SingleBin_Title_Block(args, pad, sources[0]["fit_set"], y_par)
    pad.Modified()
    pad.Update()
    c1.cd()
    c1.Modified()
    c1.Update()
    return c1

def run_comparison_mode(args):
    sources = build_comparison_sources(args)
    if(args.verbose):
        for src in sources:
            print(f"{color.CYAN}[INFO] Comparison source: {src['label']} | fit_set={src['fit_set']} | json={src['json_path']} | n={len(src['fit_dict'])}{color.END}")
    om = str(getattr(args, "output_mode", "plot")).strip().lower()
    if(om in ["table", "both"]):
        for y_par in args.y_pars:
            write_comparison_table(args, sources, y_par)
    if(om in ["plot", "both"]):
        # Disable spline overlays for comparison plots
        saved_sp = args.spline_prefix
        saved_ssr = bool(getattr(args, "show_spline_range", False))
        args.spline_prefix = None
        args.show_spline_range = False
        run_comparison_plots(args, sources)
        args.spline_prefix = saved_sp
        args.show_spline_range = saved_ssr
    print(f"\n{color.BBLUE}Finished comparison mode for 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
    args.timer.stop()

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    args = parse_args()
    print(f"\n{color.BBLUE}Beginning to run 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
    args.timer = RuntimeTimer()
    args.timer.start()
    args.x_mode = str(args.x_mode).lower()
    if("pdf" in args.formats):
        args.frame_line_width = max([1, args.frame_line_width - 2])

    # Multi json/fit_set without -cm would silently use source[0] only
    _jsons = normalize_json_file_list(args)
    _fsets = normalize_fit_set_list(args)
    if((not getattr(args, "comparison_mode", False)) and ((len(_jsons) > 1) or (len(_fsets) > 1))):
        print(f"{color.BYELLOW}[WARN] Multiple --json_file/--fit_set without --comparison_mode; enabling comparison_mode.{color.END}")
        args.comparison_mode = True
    if(getattr(args, "comparison_mode", False)):
        print(f"{color.CYAN}[INFO] comparison | files={_jsons} | fit_sets={_fsets} | output_mode={getattr(args, 'output_mode', 'plot')} | types={list(getattr(args, 'comparison_types', ['overlay']))}{color.END}")
    else:
        print(f"{color.CYAN}[INFO] single | file={_jsons[0] if(len(_jsons) > 0) else '?'} | fit_set={_fsets[0] if(len(_fsets) > 0) else '(auto)'}{color.END}")

    # --show_spline_range: avoid overwriting normal outputs
    if((getattr(args, "show_spline_range", False)) and ("with_spline_ranges" not in str(getattr(args, "name", "")).lower())):
        args.name = f"With_Spline_Ranges_{getattr(args, 'name', '')}"

    if(getattr(args, "show_spline_range", False)):
        if((args.spline_prefix is None) or (str(args.spline_prefix).strip() in ["", "None", "none"])):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} --show_spline_range requires --spline_prefix.{color.END}")
        args.spline_fit_limits = {}
        if(str(getattr(args, "spline_range_mode", "fit_limits")).strip().lower() == "fit_limits"):
            limits_dict, limits_path = load_spline_fit_parameter_limits()
            args.spline_fit_limits = limits_dict
            if((limits_path is None) or (len(limits_dict) == 0)):
                print(f"{color.Error}WARNING:{color.END_R} --spline_range_mode fit_limits could not load Phi_h_Fit_Parameters_from_Spline.py; B/C range bands will be skipped.{color.END}")
            elif(args.verbose):
                print(f"{color.GREEN}[INFO] Loaded spline fit limits from: {limits_path} ({len(limits_dict)} keys){color.END}")
        if(args.verbose):
            print(f"{color.CYAN}[INFO] show_spline_range mode={args.spline_range_mode} scan_n={args.spline_range_scan_n} name='{args.name}'{color.END}")

    # Comparison workflow (fully gated)
    if(getattr(args, "comparison_mode", False)):
        if(args.list_fit_sets):
            for ii in range(len(normalize_json_file_list(args))):
                print(f"Fit sets in JSON[{ii}] ({normalize_json_file_list(args)[ii]}):")
                for kk in list_fit_sets(load_json(args, json_index=ii)):
                    print(f"  {kk}")
            return
        run_comparison_mode(args)
        return

    json_obj = load_json(args, json_index=0)
    if(args.list_fit_sets):
        print("Fit sets in JSON:")
        for kk in list_fit_sets(json_obj):
            print(f"  {kk}")
        return

    fit_sets = normalize_fit_set_list(args)
    fit_set = fit_sets[0] if(len(fit_sets) > 0) else ""
    if(fit_set == ""):
        fit_set = select_default_fit_set(json_obj)
        if(fit_set == ""):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} No non-empty fit_set found in JSON (excluding Meta_Data_of_Last_Run). Use --fit_set.{color.END}")
        if(args.verbose):
            print(f"{color.BYELLOW}[INFO] Auto-selected fit_set = '{fit_set}'{color.END}")

    if(fit_set not in json_obj):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} Requested --fit_set '{fit_set}' not found in JSON.{color.END}")

    fit_dict = json_obj[fit_set]
    if((not isinstance(fit_dict, dict)) or (len(fit_dict) == 0)):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} Fit set '{fit_set}' is empty or not a dict.{color.END}")

    grouped       = group_by_q2y(fit_dict)
    info_map      = build_info_map(args, fit_dict)
    q2y_ranges    = build_q2y_ranges(grouped, info_map)

    spline_models = load_spline_models(args, fit_set)
    if(args.Spline_Only):
        y_range = {}
        for y_par in ['Fit_Par_B', 'Fit_Par_C']:
            if(args.y_range_mode == "global"):
                if(args.global_y_range is not None):
                    gymin, gymax = float(args.global_y_range[0]), float(args.global_y_range[1])
                else:
                    gymin, gymax = compute_global_y_range(args, grouped, fit_dict, y_par)
                y_range[y_par] = (gymin, gymax)
            else:
                y_range[y_par] = (0.0, 1.0)
            # y_range[y_par] = (0.0, 0.0)
        y_range["Fit_Par_A"] = (0.0, 0.0)
        if(args.spline_prefix is None):
            raise SystemExit(f"\n{color.Error}ERROR:{color.END_R} Did not select a spline function file.\n\tMust set a value for {color.END_B}'--spline_prefix'{color.END}\n")
        else:
            return Spline_Plots_Only(args, spline_models, y_ranges=y_range)
    elif(args.x_mode in ["Q2", "q2", "y", "xB", "xb"]):
        raise SystemExit(f"\n{color.Error}ERROR:{color.END_R} The variable {color.END_B}'{args.x_mode}'{color.END_R} only works for the '--Spline_Only' images (as of 4/17/2026){color.END}\n")

    if(args.verbose):
        print(f"{color.CYAN}[INFO] Using fit_set: {fit_set}{color.END}")
        print(f"{color.CYAN}[INFO] Q2-y bins present: {sorted(list(grouped.keys()))}{color.END}")
        print(f"{color.CYAN}[INFO] Total fit entries: {len(fit_dict)}{color.END}")

    if(args.global_x_range is not None):
        xmin, xmax = float(args.global_x_range[0]), float(args.global_x_range[1])
    else:
        xmin, xmax = compute_global_x_range(args, grouped, info_map)

    if(args.single_bin):
        if(args.single_q2y_bin is None):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} --single_bin requires --single_q2y_bin to be set.{color.END}")
        q2y_bin = int(args.single_q2y_bin)
        if(q2y_bin not in grouped):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} Requested Q2-y bin {q2y_bin} is not present in this fit_set.{color.END}")

        if(args.verbose):
            print(f"{color.CYAN}[INFO] Single-bin mode enabled: Q2-y bin = {q2y_bin}{color.END}")
            print(f"{color.CYAN}[INFO] Global X range: [{xmin}, {xmax}]{color.END}")

        for y_par in args.y_pars:
            if((str(y_par) == "Fit_Par_B")):
                y_range = (-0.8, 0.125)
            elif((str(y_par) == "Fit_Par_C")):
                y_range = (-0.3, 0.25)
            else:
                series_map_tmp = build_series_for_q2y(args, grouped, fit_dict, info_map, int(q2y_bin), y_par)
                y_range = Compute_SingleBin_AutoYRange(series_map_tmp)
            y_range = expand_y_range_for_spline_bands(args, grouped, fit_dict, info_map, y_par, y_range, spline_models, q2y_bins=[q2y_bin])

            if(args.test):
                fake_name = Build_SingleBin_Output_Filename(args, fit_set, y_par, q2y_bin)
                print(f"{color.BYELLOW}[TEST] Would draw SINGLE BIN: fit_set='{fit_set}' x_mode='{args.x_mode}' y_par='{y_par}' q2y_bin='{q2y_bin}' -> {color.BCYAN}{fake_name}{color.END}")
                continue

            canv = draw_single_bin(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, q2y_bin, (xmin, xmax), y_range, spline_models=spline_models)
            canv.Update()
            out_name = save_single_canvas(args, canv, fit_set, y_par, q2y_bin)

            if(args.verbose):
                print(f"{color.GREEN}[INFO] Wrote: {out_name}{color.END}")

        print(f"\n{color.BBLUE}Finished running 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
        args.timer.stop()
        return

    if(args.draw_legends):
        xspan = xmax - xmin
        if(xspan > 0.0):
            xmax = xmax + 0.30 * xspan
        else:
            xmax = xmax + 1.0

    if(args.verbose):
        print(f"{color.CYAN}[INFO] Global X range: [{xmin}, {xmax}]{color.END}")

    for y_par in args.y_pars:
        if(args.y_range_mode == "global"):
            if(args.global_y_range is not None):
                gymin, gymax = float(args.global_y_range[0]), float(args.global_y_range[1])
            else:
                gymin, gymax = compute_global_y_range(args, grouped, fit_dict, y_par)
            y_range = (gymin, gymax)
        else:
            y_range = (0.0, 1.0)
        y_range = expand_y_range_for_spline_bands(args, grouped, fit_dict, info_map, y_par, y_range, spline_models)

        if(args.test):
            fake_name = Build_Output_Filename(args, fit_set, y_par)
            print(f"{color.BYELLOW}[TEST] Would draw: fit_set='{fit_set}' x_mode='{args.x_mode}' y_par='{y_par}' -> {color.BCYAN}{fake_name}{color.END}")
            continue

        canv = draw_mosaic(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, (xmin, xmax), y_range, spline_models=spline_models)
        title_text = build_global_title(args, fit_set, y_par)
        draw_global_title(args, canv, title_text)
        # Optional canvas-level data vs spline legend (off by default; enabled by --toggle_source_legend)
        if((bool(getattr(args, "toggle_source_legend", False))) and (y_par in spline_models)):
            canv.cd()
            x1, y1, x2, y2 = build_adaptive_source_legend_box(2, ["Data", "Spline fit"], x1=0.02, y1=0.56)
            leg_src = ROOT.TLegend(float(x1), float(y1), float(x2), float(y2))
            leg_src.SetBorderSize(1)
            leg_src.SetFillStyle(1001)
            leg_src.SetFillColor(ROOT.kWhite)
            leg_src.SetTextFont(42)
            leg_src.SetTextSize(0.018)
            leg_src.SetHeader("Sources", "C")
            g_data = ROOT.TGraph(1)
            g_data.SetLineColor(ROOT.kBlack)
            g_data.SetMarkerColor(ROOT.kBlack)
            g_data.SetLineStyle(1)
            g_data.SetMarkerStyle(20)
            g_sp = ROOT.TGraph(1)
            g_sp.SetLineColor(ROOT.kBlack)
            g_sp.SetMarkerColor(ROOT.kBlack)
            g_sp.SetLineStyle(7)
            g_sp.SetMarkerStyle(29)
            if(not hasattr(canv, "_keepalive")):
                canv._keepalive = []
            canv._keepalive.append(g_data)
            canv._keepalive.append(g_sp)
            leg_src.AddEntry(g_data, "Data", "lp")
            leg_src.AddEntry(g_sp, "Spline fit", "lp")
            leg_src.Draw()
            canv._keepalive.append(leg_src)
        canv.Update()
        out_name = save_canvas(args, canv, fit_set, y_par)

        if(args.verbose):
            print(f"{color.GREEN}[INFO] Wrote: {out_name}{color.END}")

    print(f"\n{color.BBLUE}Finished running 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
    args.timer.stop()

if(__name__ == "__main__"):
    main()

