#!/usr/bin/env python3

import os
import sys
import re
import json
import argparse
import ROOT

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

# ------------------------------------------------------------
# User-provided plotting/binning utilities (incorporated directly)
# ------------------------------------------------------------
import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, RuntimeTimer, Get_Num_of_z_pT_Rows_and_Columns
from Binning_Dictionaries import Full_Bin_Definition_Array
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
                   help="Number of Q2-y bins in the mosaic layout.\n")
    p.add_argument("-R", "--layout_rows",
                   default="4,4,4,3,2",
                   help="Comma-separated pads per row from bottom->top (ragged, right-aligned).\n")

    p.add_argument("-X", "--global_x_range",
                   nargs=2,
                   type=float,
                   default=None,
                   help="Override global X range: XMIN XMAX.\n")
    
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
                   help="Tick label policy: 'outer' shows labels only on outer pads, 'all' shows labels on every pad.\n")

    # Centered per-pad labels + slightly smaller default (requested)
    p.add_argument("-K", "--pad_label_size",
                   type=float,
                   default=0.070,
                   help="Per-pad label TLatex size (NDC).\n")
    p.add_argument("-a", "--pad_label_x",
                   type=float,
                   default=0.50,
                   help="Per-pad label X position (NDC).\n")
    p.add_argument("-A", "--pad_label_y",
                   type=float,
                   default=0.965,
                   help="Per-pad label Y position (NDC).\n")

    p.add_argument("-M", "--title_mode",
                   choices=["none", "auto", "text_only"],
                   default="auto",
                   help="Global title policy: none, auto-built title, or text_only.\n")
    p.add_argument("-fs", "--fit_set_label",
                   default="",
                   help="Optional friendly label for the fit_set (used in title). If blank, uses fit_set-derived default.\n")

    # Slightly smaller default title size (after increased canvas size)
    p.add_argument("-s", "--title_size",
                   type=float,
                   default=0.028,
                   help="Global title TLatex size (NDC).\n")

    p.add_argument("-p", "--title_x",
                   type=float,
                   default=0.01,
                   help="Global title X position (NDC).\n")
    p.add_argument("-P", "--title_y",
                   type=float,
                   default=0.99,
                   help="Global title Y position (NDC).\n")


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
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Appended_in_Parallel_Fixed_RC_Factor_Normalization_Full.json",
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Final_File_Before_the_Collaboration_Meeting.json",
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_New_File_with_BC.json",
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_NEW_FULL_Normalization_AND_FULL_Fits.json",
                   help="Input JSON file produced by your fit workflow.\n")

    p.add_argument("-L", "--list_fit_sets",
                   action="store_true",
                   help="List available fit-set keys in the JSON and exit.\n")
    p.add_argument("-f", "--fit_set",
                   default="Fit_Pars_from_3D_Bayesian",
                   help="Top-level JSON key to use.\n")

    p.add_argument("-y", "--y_pars",
                   nargs="+",
                   default=["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"],
                   help="Fit parameters to plot (each produces a separate mosaic canvas).\n")
    
    p.add_argument("-x", "--x_mode",
                   choices=["z", "pt", "pT"],
                   default="z",
                   help="Choose X axis: 'z' plots vs z center, 'pt'/'pT' plots vs pT center.\n")

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

    p.add_argument("-xe", "--x_error_bars",
                   action="store_true",
                   help="Replace connecting lines between points with x-error bars sized to a fraction of the x-bin width.\n")
    p.add_argument("-xf", "--x_error_fraction",
                   type=float,
                   default=(1.0/3.0),
                   help="Fraction of the x-variable bin width to use for the FULL x-error-bar length (ex = 0.5*fraction*bin_width).\n")

    return p.parse_args()

# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------
def load_json(args):
    if(not os.path.isfile(args.json_file)):
        raise SystemExit(f"{color.Error}ERROR: JSON file not found:{color.END_R} {args.json_file}{color.END}")
    with open(args.json_file, "r") as jf:
        return json.load(jf)

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

def compute_global_y_range(args, grouped, fit_dict, y_par):
    ymin = None
    ymax = None
    err_key = f"{y_par}{args.err_suffix}"
    for q2y_bin in grouped.keys():
        for zpt_bin, key_str in grouped[q2y_bin]:
            if(key_str not in fit_dict):
                continue
            entry = fit_dict[key_str]
            if((y_par not in entry) or (err_key not in entry)):
                continue
            yv = float(entry[y_par])
            ye = float(entry[err_key])
            lo = yv - abs(ye)
            hi = yv + abs(ye)
            if((ymin is None) or (lo < ymin)):
                ymin = lo
            if((ymax is None) or (hi > ymax)):
                ymax = hi
    if((ymin is None) or (ymax is None)):
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
        yval = entry[y_par]
        yerr = entry[err_key]
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

# ------------------------------------------------------------
# Title logic
# ------------------------------------------------------------
def Get_Default_Y_Title(y_par, fit_set):
    y_title_map = {"Fit_Par_A": "Amplitude", "Fit_Par_B": "Cos(#phi) Moment", "Fit_Par_C": "Cos(2#phi) Moment"}
    base = y_title_map.get(str(y_par), str(y_par))
    if(("(Normalized)" in str(fit_set)) and (str(y_par) in y_title_map)):
        base = f"{base} from the Cross Section Fits"
    return base

def Get_Default_FitSet_Title(fit_set):
    fs = str(fit_set)
    fs = fs.replace("Fit_Pars_from_", "")
    fs_clean = fs.replace("(Normalized)", "")
    mm_dim = re.search(r"(\d+)D", fs_clean)
    dim_tag = f"{mm_dim.group(1)}D" if(mm_dim is not None) else ""
    has_RC = (re.search(r"(^|_)RC(_|$)", fs_clean) is not None) or ("_RC_" in fs_clean) or ("RC_" in fs_clean) or ("_RC" in fs_clean)
    has_BC = (re.search(r"(^|_)BC(_|$)", fs_clean) is not None) or ("_BC_" in fs_clean) or ("BC_" in fs_clean) or ("_BC" in fs_clean)
    if("Bayesian" in fs_clean):
        method = "Bayesian Unfolding"
    elif("Bin" in fs_clean):
        method = "Bin-by-bin Acceptance Corrected"
    else:
        method = fs_clean.strip("_")
    core = f"{dim_tag} {method}".strip()
    if(has_BC and has_RC):
        core = f"{core} with BC Corrections and Radiative Corrections"
    elif(has_BC):
        core = f"{core} with BC Corrections"
    elif(has_RC):
        core = f"{core} with Radiative Corrections"
    return core

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

def draw_mosaic(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, x_range, y_range):
    mapping, max_cols, nrows = build_layout_map(args)
    c1 = ROOT.TCanvas(f"c_mosaic_{y_par}", f"c_mosaic_{y_par}", int(args.canvas_width), int(args.canvas_height))
    c1.SetFillColor(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)

    if(not hasattr(c1, "_keepalive")):
        c1._keepalive = []

    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])

    title_space = 0.090 if(args.title_mode != "none") else 0.00
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
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

        frame.GetXaxis().SetNdivisions(505)
        frame.GetYaxis().SetNdivisions(505)

        series_map = build_series_for_q2y(args, grouped, fit_dict, info_map, q2y_bin, y_par)
        sid_list = sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)

        for sid in sid_list:
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
                # leg.SetFillStyle(0)
                leg.SetFillStyle(1001)
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

def draw_single_bin(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, q2y_bin, x_range, y_range):
    c1 = ROOT.TCanvas(f"c_single_{y_par}_{q2y_bin}", f"c_single_{y_par}_{q2y_bin}", int(args.single_canvas_width), int(args.single_canvas_height))
    c1.SetFillColor(0)
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
    pad.SetGrid(1, 1)
    # pad.SetTickx(1) # This adds exta tick marks on the oposite axis (i.e., on the top and bottom sides of the image)
    # pad.SetTicky(1) # This adds exta tick marks on the oposite axis (i.e., on the left and right sides of the image)
    pad.SetLeftMargin(0.14)
    pad.SetBottomMargin(0.12)
    pad.SetRightMargin(0.04)
    pad.SetTopMargin(top_margin)
    pad.Draw()
    pad.cd()
    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])
    x_axis_title = "z" if(str(args.x_mode).lower() == "z") else "P_{T}"
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

        if(gr.GetLineColor() != ROOT.kGreen):
            continue
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

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    args = parse_args()
    print(f"\n{color.BBLUE}Beginning to run 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
    timer = RuntimeTimer()
    timer.start()
    args.timer = timer
    args.x_mode = str(args.x_mode).lower()
    if("pdf" in args.formats):
        args.frame_line_width = max([1, args.frame_line_width - 2])
    json_obj = load_json(args)
    if(args.list_fit_sets):
        print("Fit sets in JSON:")
        for kk in list_fit_sets(json_obj):
            print(f"  {kk}")
        return

    fit_set = str(args.fit_set).strip()
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

    grouped    = group_by_q2y(fit_dict)
    info_map   = build_info_map(args, fit_dict)
    q2y_ranges = build_q2y_ranges(grouped, info_map)

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

            if(args.test):
                fake_name = Build_SingleBin_Output_Filename(args, fit_set, y_par, q2y_bin)
                print(f"{color.BYELLOW}[TEST] Would draw SINGLE BIN: fit_set='{fit_set}' x_mode='{args.x_mode}' y_par='{y_par}' q2y_bin='{q2y_bin}' -> {color.BCYAN}{fake_name}{color.END}")
                continue

            canv = draw_single_bin(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, q2y_bin, (xmin, xmax), y_range)
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

        if(args.test):
            fake_name = Build_Output_Filename(args, fit_set, y_par)
            print(f"{color.BYELLOW}[TEST] Would draw: fit_set='{fit_set}' x_mode='{args.x_mode}' y_par='{y_par}' -> {color.BCYAN}{fake_name}{color.END}")
            continue

        canv = draw_mosaic(args, grouped, fit_dict, info_map, q2y_ranges, fit_set, y_par, (xmin, xmax), y_range)
        title_text = build_global_title(args, fit_set, y_par)
        draw_global_title(args, canv, title_text)
        canv.Update()
        out_name = save_canvas(args, canv, fit_set, y_par)

        if(args.verbose):
            print(f"{color.GREEN}[INFO] Wrote: {out_name}{color.END}")

    print(f"\n{color.BBLUE}Finished running 'Full_Moment_Plots_Creation_From_JSON.py'{color.END}\n")
    args.timer.stop()

if(__name__ == "__main__"):
    main()

