#!/usr/bin/env python3

import os
import sys
import re
import json
import math
import argparse
import ROOT

ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)

# ------------------------------------------------------------
# User-provided plotting/binning utilities (incorporated directly)
# ------------------------------------------------------------
import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, Get_Num_of_z_pT_Rows_and_Columns
from Binning_Dictionaries import Full_Bin_Definition_Array
sys.path.remove(script_dir)
del script_dir
color_mapper  = {"1": ROOT.kRed, "2": ROOT.kBlue, "3": ROOT.kMagenta, "4": ROOT.kGreen, "5": ROOT.kOrange+3, "6": ROOT.kAzure, "7": ROOT.kOrange}
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

    p.add_argument("json_file", help="Input JSON file produced by your fit workflow.")

    p.add_argument("-L", "--list_fit_sets", action="store_true", help="List available fit-set keys in the JSON and exit.")
    p.add_argument("-f", "--fit_set", default="", help="Top-level JSON key to use (e.g. 'Fit_Pars_from_3D_Bayesian_(Normalized)'). If blank, auto-selects a non-empty fit-set (prefers '(Normalized)' if present).")

    p.add_argument("-x", "--x_mode", choices=["z", "pt"], required=True, help="Choose X axis: 'z' plots vs z center, 'pt' plots vs pT center.")
    p.add_argument("-y", "--y_pars", nargs="+", default=["Fit_Par_B", "Fit_Par_C"], help="Fit parameters to plot (each produces a separate mosaic canvas).")
    p.add_argument("-e", "--err_suffix", default="_ERR", help="Error key suffix (e.g. Fit_Par_B + _ERR -> Fit_Par_B_ERR).")

    p.add_argument("-q", "--q2y_count", type=int, default=17, help="Number of Q2-y bins in the mosaic layout.")
    p.add_argument("-R", "--layout_rows", default="4,4,4,3,2", help="Comma-separated pads per row from bottom->top (ragged, right-aligned).")

    p.add_argument("-o", "--out_dir", default=".", help="Output directory.")
    p.add_argument("-O", "--out_stem", default="mosaic", help="Output file stem.")
    p.add_argument("-F", "--formats", default="png", help="Comma-separated output formats (e.g. 'png,pdf').")
    p.add_argument("-w", "--overwrite", action="store_true", help="Overwrite existing output files.")

    p.add_argument("-W", "--canvas_width", type=int, default=1600, help="Canvas width in pixels.")
    p.add_argument("-H", "--canvas_height", type=int, default=2000, help="Canvas height in pixels.")

    p.add_argument("-X", "--global_x_range", nargs=2, type=float, default=None, help="Override global X range: XMIN XMAX.")
    p.add_argument("-m", "--y_range_mode", choices=["global", "auto"], default="global", help="Y range policy: 'global' shared across pads (default), or 'auto' per-pad tight range.")
    p.add_argument("-Y", "--global_y_range", nargs=2, type=float, default=None, help="Override global Y range: YMIN YMAX (applies when y_range_mode='global').")

    p.add_argument("-b", "--frame_line_width", type=int, default=3, help="Bold frame/border thickness for each pad.")
    p.add_argument("-g", "--grid", action="store_true", help="Enable pad grid.")

    p.add_argument("-l", "--label_mode", choices=["outer", "all"], default="outer", help="Tick label policy: 'outer' shows labels only on outer pads, 'all' shows labels on every pad.")
    p.add_argument("-k", "--pad_label_mode", choices=["none", "bin", "bin_Q2", "bin_Q2y"], default="bin_Q2", help="Per-pad label: none, bin only, bin+Q2 range, or bin+Q2+y ranges.")
    p.add_argument("-K", "--pad_label_size", type=float, default=0.08, help="Per-pad label TLatex size (NDC).")
    p.add_argument("-a", "--pad_label_x", type=float, default=0.03, help="Per-pad label X position (NDC).")
    p.add_argument("-A", "--pad_label_y", type=float, default=0.95, help="Per-pad label Y position (NDC).")

    p.add_argument("-T", "--title_text", default="", help="Optional user-provided extra title text to include in the global title.")
    p.add_argument("-M", "--title_mode", choices=["none", "auto", "text_only"], default="auto", help="Global title policy: none, auto-built title, or text_only.")
    p.add_argument("-n", "--fit_set_label", default="", help="Optional friendly label for the fit_set (used in title). If blank, uses fit_set string.")
    p.add_argument("-s", "--title_size", type=float, default=0.035, help="Global title TLatex size (NDC).")
    p.add_argument("-p", "--title_x", type=float, default=0.01, help="Global title X position (NDC).")
    p.add_argument("-P", "--title_y", type=float, default=0.99, help="Global title Y position (NDC).")

    p.add_argument("-t", "--test", action="store_true", help="Parse JSON, build point maps, and print summaries; do not write output files.")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")

    return p.parse_args()

# ------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------
def load_json(json_path):
    if(not os.path.isfile(json_path)):
        raise SystemExit(f"{color.Error}ERROR: JSON file not found:{color.END_R} {json_path}{color.END}")
    with open(json_path, "r") as jf:
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

def build_layout_map(q2y_count, layout_rows):
    max_cols = max(layout_rows)
    nrows    = len(layout_rows)
    mapping  = {}
    bin_num  = 1
    for row in range(nrows):
        ncol = layout_rows[row]
        col_start = max_cols - ncol
        for ii in range(ncol):
            col = (max_cols - 1) - ii
            if(bin_num > q2y_count):
                break
            mapping[bin_num] = (row, col, col_start)
            bin_num += 1
        if(bin_num > q2y_count):
            break
    return mapping, max_cols, nrows

def pad_is_outer(row, col, col_start, max_cols, nrows):
    is_bottom            = (row == 0)
    is_top               = (row == (nrows - 1))
    is_leftmost_present  = (col == col_start)
    is_rightmost_present = (col == (max_cols - 1))
    return is_bottom, is_leftmost_present, is_rightmost_present, is_top

def ensure_outdir(out_dir):
    if((out_dir is not None) and (str(out_dir).strip() != "") and (not os.path.isdir(out_dir))):
        os.makedirs(out_dir, exist_ok=True)

# ------------------------------------------------------------
# JSON -> binnings/styles (via Construct_JSON_Info) -> grouping
# ------------------------------------------------------------
def build_info_map(fit_dict, verbose=False):
    info_map = {}
    for key_str in fit_dict.keys():
        q2y_bin, zpt_bin = parse_inner_key(key_str)
        Construct_JSON_Info(Q2_y_Bin=str(q2y_bin), z_pT_Bin=str(zpt_bin), return_info=info_map)
    if(verbose):
        print(color.CYAN, f"[INFO] Built info_map entries: {len(info_map)}", color.END)
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

def compute_global_x_range(grouped, info_map, x_mode):
    xmin = None
    xmax = None
    for q2y_bin in grouped.keys():
        for zpt_bin, key_str in grouped[q2y_bin]:
            if(key_str not in info_map):
                continue
            xval = info_map[key_str]["z_range"][0] if(x_mode == "z") else info_map[key_str]["pTrange"][0]
            xval = float(xval)
            if((xmin is None) or (xval < xmin)):
                xmin = xval
            if((xmax is None) or (xval > xmax)):
                xmax = xval
    if((xmin is None) or (xmax is None)):
        return 0.0, 1.0
    if(xmin == xmax):
        return xmin - 1.0, xmax + 1.0
    return xmin, xmax

def compute_global_y_range(grouped, fit_dict, y_par, err_suffix):
    ymin = None
    ymax = None
    err_key = f"{y_par}{err_suffix}"
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
    pad = 0.10 * (ymax - ymin)
    return ymin - pad, ymax + pad

def build_series_for_q2y(q2y_bin, grouped, fit_dict, info_map, x_mode, y_par, err_suffix):
    series_map = {}
    err_key = f"{y_par}{err_suffix}"
    if(q2y_bin not in grouped):
        return series_map
    for zpt_bin, key_str in grouped[q2y_bin]:
        if((key_str not in fit_dict) or (key_str not in info_map)):
            continue
        entry = fit_dict[key_str]
        if((y_par not in entry) or (err_key not in entry)):
            continue
        inf  = info_map[key_str]
        xval = inf["z_range"][0] if(x_mode == "z") else inf["pTrange"][0]
        yval = entry[y_par]
        yerr = entry[err_key]
        if(x_mode == "z"):
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
# Drawing
# ------------------------------------------------------------
def style_graph(gr, color_val, marker_val):
    gr.SetLineColor(int(color_val))
    gr.SetMarkerColor(int(color_val))
    gr.SetMarkerStyle(int(marker_val))
    gr.SetLineWidth(2)
    gr.SetMarkerSize(1.0)

def build_global_title(args, fit_set, y_par):
    if(args.title_mode == "none"):
        return ""
    if(args.title_mode == "text_only"):
        return str(args.title_text)
    fit_label = args.fit_set_label if(str(args.fit_set_label).strip() != "") else str(fit_set)
    parts = []
    if(str(args.title_text).strip() != ""):
        parts.append(str(args.title_text))
    parts.append(str(fit_label))
    parts.append(f"x={args.x_mode}")
    parts.append(f"y={y_par}")
    return "  |  ".join(parts)

def draw_global_title(canvas, title_text, title_x, title_y, title_size):
    if(str(title_text).strip() == ""):
        return
    canvas.cd()
    tex = ROOT.TLatex()
    tex.SetNDC(True)
    tex.SetTextAlign(13)
    tex.SetTextSize(float(title_size))
    tex.DrawLatex(float(title_x), float(title_y), str(title_text))

def draw_pad_label(args, q2y_bin, q2y_ranges):
    if(args.pad_label_mode == "none"):
        return
    lab = ROOT.TLatex()
    lab.SetNDC(True)
    lab.SetTextAlign(13)
    lab.SetTextSize(float(args.pad_label_size))
    x0 = float(args.pad_label_x)
    y0 = float(args.pad_label_y)
    line_step = 1.15 * float(args.pad_label_size)

    lab.DrawLatex(x0, y0, f"Q2-y Bin {q2y_bin}")
    if(args.pad_label_mode == "bin"):
        return

    if(q2y_bin not in q2y_ranges):
        return

    Q2min = float(q2y_ranges[q2y_bin]["Q2range"][1])
    Q2max = float(q2y_ranges[q2y_bin]["Q2range"][2])
    lab.DrawLatex(x0, y0 - line_step, f"Q^{{2}}: [{Q2min:.3g}, {Q2max:.3g}]")
    if(args.pad_label_mode == "bin_Q2"):
        return

    ymin = float(q2y_ranges[q2y_bin]["y_range"][1])
    ymax = float(q2y_ranges[q2y_bin]["y_range"][2])
    lab.DrawLatex(x0, y0 - 2.0*line_step, f"y: [{ymin:.3g}, {ymax:.3g}]")

def draw_mosaic(grouped, fit_dict, info_map, q2y_ranges, args, y_par, x_range, y_range):
    rows = parse_layout_rows(args.layout_rows)
    mapping, max_cols, nrows = build_layout_map(args.q2y_count, rows)

    c1 = ROOT.TCanvas(f"c_mosaic_{y_par}", f"c_mosaic_{y_par}", int(args.canvas_width), int(args.canvas_height))
    c1.SetFillColor(0)
    c1.SetMargin(0.0, 0.0, 0.0, 0.0)

    xmin, xmax = float(x_range[0]), float(x_range[1])
    gymin, gymax = float(y_range[0]), float(y_range[1])

    for q2y_bin in range(1, int(args.q2y_count) + 1):
        if(q2y_bin not in mapping):
            continue

        row, col, col_start = mapping[q2y_bin]
        x0 = float(col) / float(max_cols)
        x1 = float(col + 1) / float(max_cols)
        y0 = float(row) / float(nrows)
        y1 = float(row + 1) / float(nrows)

        pad = ROOT.TPad(f"pad_q2y_{q2y_bin}_{y_par}", f"pad_q2y_{q2y_bin}_{y_par}", x0, y0, x1, y1)
        pad.SetFillColor(0)
        pad.SetFrameLineWidth(int(args.frame_line_width))
        pad.SetTickx(1)
        pad.SetTicky(1)
        if(args.grid):
            pad.SetGrid(1, 1)

        is_bottom, is_leftmost_present, is_rightmost_present, is_top = pad_is_outer(row, col, col_start, max_cols, nrows)

        left_margin   = 0.14 if((args.label_mode == "outer") and (is_leftmost_present)) else (0.14 if(args.label_mode == "all") else 0.0)
        bottom_margin = 0.14 if((args.label_mode == "outer") and (is_bottom)) else (0.14 if(args.label_mode == "all") else 0.0)
        right_margin  = 0.02 if((args.label_mode == "outer") and (is_rightmost_present)) else (0.02 if(args.label_mode == "all") else 0.0)
        top_margin    = 0.02 if((args.label_mode == "outer") and (is_top)) else (0.02 if(args.label_mode == "all") else 0.0)

        pad.SetLeftMargin(float(left_margin))
        pad.SetBottomMargin(float(bottom_margin))
        pad.SetRightMargin(float(right_margin))
        pad.SetTopMargin(float(top_margin))

        pad.Draw()
        pad.cd()

        series_map = build_series_for_q2y(q2y_bin, grouped, fit_dict, info_map, args.x_mode, y_par, args.err_suffix)
        mg = ROOT.TMultiGraph()

        sid_list = sorted(list(series_map.keys()), key=lambda ss: int(ss) if(re.fullmatch(r"\d+", ss)) else ss)
        for sid in sid_list:
            pts = series_map[sid]["points"]
            gr  = ROOT.TGraphErrors(len(pts))
            for ip, (xx, yy, ey, key_str) in enumerate(pts):
                gr.SetPoint(ip, float(xx), float(yy))
                gr.SetPointError(ip, 0.0, float(ey))
            style_graph(gr, series_map[sid]["color"], series_map[sid]["marker"])
            mg.Add(gr, "P")

        mg.Draw("A")
        mg.GetXaxis().SetLimits(float(xmin), float(xmax))

        if(args.y_range_mode == "global"):
            mg.GetYaxis().SetRangeUser(float(gymin), float(gymax))
        else:
            ymin = None
            ymax = None
            for sid in series_map.keys():
                for xx, yy, ey, key_str in series_map[sid]["points"]:
                    lo = yy - abs(ey)
                    hi = yy + abs(ey)
                    if((ymin is None) or (lo < ymin)):
                        ymin = lo
                    if((ymax is None) or (hi > ymax)):
                        ymax = hi
            if((ymin is None) or (ymax is None)):
                ymin, ymax = gymin, gymax
            if(ymin == ymax):
                ymin, ymax = ymin - 1.0, ymax + 1.0
            pad_y = 0.10 * (ymax - ymin)
            mg.GetYaxis().SetRangeUser(float(ymin - pad_y), float(ymax + pad_y))

        mg.GetXaxis().SetTitle("")
        mg.GetYaxis().SetTitle("")
        mg.GetXaxis().SetTitleSize(0.0)
        mg.GetYaxis().SetTitleSize(0.0)

        if(args.label_mode == "outer"):
            mg.GetXaxis().SetLabelSize(0.06 if(is_bottom) else 0.0)
            mg.GetYaxis().SetLabelSize(0.06 if(is_leftmost_present) else 0.0)
        else:
            mg.GetXaxis().SetLabelSize(0.06)
            mg.GetYaxis().SetLabelSize(0.06)

        draw_pad_label(args, q2y_bin, q2y_ranges)

        pad.Update()
        c1.cd()

    c1.Update()
    return c1

def save_canvas(canvas, out_paths, overwrite):
    for out_path in out_paths:
        if((not overwrite) and os.path.exists(out_path)):
            raise SystemExit(f"{color.Error}ERROR:{color.END_R} Output exists (use --overwrite): {out_path}{color.END}")
        canvas.SaveAs(out_path)

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    args = parse_args()
    json_obj = load_json(args.json_file)

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
            print(color.YELLOW, f"[INFO] Auto-selected fit_set = '{fit_set}'", color.END)

    if(fit_set not in json_obj):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} Requested --fit_set '{fit_set}' not found in JSON.{color.END}")

    fit_dict = json_obj[fit_set]
    if((not isinstance(fit_dict, dict)) or (len(fit_dict) == 0)):
        raise SystemExit(f"{color.Error}ERROR:{color.END_R} Fit set '{fit_set}' is empty or not a dict.{color.END}")

    grouped   = group_by_q2y(fit_dict)
    info_map  = build_info_map(fit_dict, verbose=args.verbose)
    q2y_ranges = build_q2y_ranges(grouped, info_map)

    if(args.verbose):
        print(color.CYAN, f"[INFO] Using fit_set: {fit_set}", color.END)
        print(color.CYAN, f"[INFO] Q2-y bins present: {sorted(list(grouped.keys()))}", color.END)
        print(color.CYAN, f"[INFO] Total fit entries: {len(fit_dict)}", color.END)

    ensure_outdir(args.out_dir)

    if(args.global_x_range is not None):
        xmin, xmax = float(args.global_x_range[0]), float(args.global_x_range[1])
    else:
        xmin, xmax = compute_global_x_range(grouped, info_map, args.x_mode)

    if(args.verbose):
        print(color.CYAN, f"[INFO] Global X range: [{xmin}, {xmax}]", color.END)

    fmts = [ff.strip() for ff in str(args.formats).split(",") if(ff.strip() != "")]

    for y_par in args.y_pars:
        if(args.y_range_mode == "global"):
            if(args.global_y_range is not None):
                gymin, gymax = float(args.global_y_range[0]), float(args.global_y_range[1])
            else:
                gymin, gymax = compute_global_y_range(grouped, fit_dict, y_par, args.err_suffix)
            y_range = (gymin, gymax)
        else:
            y_range = (0.0, 1.0)

        if(args.test):
            print(color.YELLOW, f"[TEST] Would draw: fit_set='{fit_set}' x_mode='{args.x_mode}' y_par='{y_par}' entries={len(fit_dict)} x_range=[{xmin},{xmax}] y_mode='{args.y_range_mode}'", color.END)
            continue

        canv = draw_mosaic(grouped, fit_dict, info_map, q2y_ranges, args, y_par, (xmin, xmax), y_range)

        title_text = build_global_title(args, fit_set, y_par)
        draw_global_title(canv, title_text, args.title_x, args.title_y, args.title_size)
        canv.Update()

        fit_set_tag = sanitize_for_filename(fit_set)
        stem = f"{args.out_stem}_{fit_set_tag}_{args.x_mode}_{y_par}"
        out_paths = [os.path.join(args.out_dir, f"{stem}.{ff}") for ff in fmts]
        save_canvas(canv, out_paths, args.overwrite)

        if(args.verbose):
            for op in out_paths:
                print(color.GREEN, f"[INFO] Wrote: {op}", color.END)

if __name__ == "__main__":
    main()