#!/usr/bin/env python3
# Redraw thesis figures 7.2-7.5 on the stepped Q2-y pad map.
# Cahn widths stay 0.25 and 0.20 GeV^2. The dashed curve is Bastami eq. (5.9a) only.

import ctypes
import json
import math
import os
import shutil
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)

ANALYSIS = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
THESIS   = os.path.join(ANALYSIS, "Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis")
EVGEN    = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/EvGen_sidis_fork"
if(ANALYSIS not in sys.path):
    sys.path.insert(0, ANALYSIS)

from Full_Moment_Plots_Creation_From_JSON import Construct_JSON_Info, color_mapper, marker_mapper
from MyCommonAnalysisFunction_richcap import skip_condition_z_pT_bins

import lhapdf

MSTW_PATH = os.path.join(EVGEN, "sidis/share/sidis/sf_set/prokudin/mstw2008lo.00.dat")
DSS_DIR   = os.path.join(EVGEN, "sidis/share/sidis/sf_set/stf")
JSON_PATH = os.path.join(ANALYSIS, "Systematic_Studies/physics_campaign/corrected/spline/normalized_bc.json")
FIT_KEY   = "Fit_Pars_from_3D_BC_RC_Bayesian"
IMAGE_DIR = os.path.join(THESIS, "Conclusions/Comparison_Images")
ARCHIVE   = os.path.join(IMAGE_DIR, "archive_wrap_20261103")

K2_UNP    = 0.25
P2_UNP    = 0.20
MBM2      = 0.34
MC2       = 1.50
M_NUCLEON = 0.938272
M_PION    = 0.13957018
E_BEAM    = 10.6
Q2_COLL   = 2.4
LAYOUT    = [4, 4, 4, 3, 2]

BM_ALPHA  = [0.73, 1.08, 0.79, 0.79, 0.79, 0.79]
BM_BETA   = 3.46
BM_A      = [0.35, -0.90, 0.24, 0.04, -0.40, -1.0]
BM_LAMBDA = [2.1, -1.111, 0.0, 0.0, 0.0, 0.0]
COLLINS_GAMMA = 1.06
COLLINS_DELTA = 0.07
COLLINS_FAV   = 0.49
COLLINS_DIS   = -1.0

# Prokudin flavor order: u, d, s, ubar, dbar, sbar.
MSTW_FLAVOUR = [(8, -2), (7, -1), (3,), (-2,), (-1,), (-3,)]
DSS_PID      = [2, 1, 3, -2, -1, -3]
CHARGE2      = [(2.0/3.0)**2, (1.0/3.0)**2, (1.0/3.0)**2, (2.0/3.0)**2, (1.0/3.0)**2, (1.0/3.0)**2]
COLLINS_N    = [COLLINS_FAV, COLLINS_DIS, 0.0, COLLINS_DIS, COLLINS_FAV, 0.0]


def load_mstw():
    source = "/tmp/mstw_bridge.cc"
    library = "/tmp/libmstw_bridge.dylib"
    include = os.path.join(EVGEN, "sidis/external/mstwpdf")
    code = os.path.join(include, "mstwpdf.cc")
    bridge = """#include "mstwpdf.h"
static mstw::c_mstwpdf* pdf_set = 0;
extern "C" void mstw_init(const char* path) { pdf_set = new mstw::c_mstwpdf(path, false, true); }
extern "C" double mstw_xf(int flavour, double x, double q) { return pdf_set->parton(flavour, x, q); }
"""
    with open(source, "w") as handle:
        handle.write(bridge)
    command = "c++ -std=c++17 -fPIC -shared -O2 -I%s %s %s -o %s" % (include, source, code, library)
    if(os.system(command) != 0):
        raise SystemExit("MSTW bridge did not compile")
    lib = ctypes.CDLL(library)
    lib.mstw_init.argtypes = [ctypes.c_char_p]
    lib.mstw_xf.argtypes   = [ctypes.c_int, ctypes.c_double, ctypes.c_double]
    lib.mstw_xf.restype    = ctypes.c_double
    lib.mstw_init(MSTW_PATH.encode())
    return lib


def x_shape(value_n, alpha, beta, x):
    return value_n * (x ** alpha) * ((1.0 - x) ** beta) * ((alpha + beta) ** (alpha + beta)) / ((alpha ** alpha) * (beta ** beta))


def gaussian(ph_t_sq, width):
    return math.exp(-ph_t_sq / width) / (math.pi * width)


def lepton_cos_phi(y):
    return 2.0 * (2.0 - y) * math.sqrt(1.0 - y) / (1.0 + (1.0 - y) ** 2)


def lepton_cos_2phi(y):
    return 2.0 * (1.0 - y) / (1.0 + (1.0 - y) ** 2)


def cahn_cos_phi(q2, y, z, pT):
    q_value = math.sqrt(q2)
    pT2_avg = P2_UNP + (z * z) * K2_UNP
    ratio   = -2.0 * (pT / q_value) * (z * K2_UNP) / pT2_avg
    return ratio * lepton_cos_phi(y)


def cahn_cos_2phi(q2, y, z, pT):
    pT2_avg = P2_UNP + (z * z) * K2_UNP
    ratio   = 2.0 * ((pT * pT) / q2) * ((z * z) * (K2_UNP ** 2)) / (pT2_avg ** 2)
    return ratio * lepton_cos_2phi(y)


def prepare_collinear(mstw, dss):
    k2_bm = K2_UNP * MBM2 / (K2_UNP + MBM2)
    p2_c  = P2_UNP * MC2 / (P2_UNP + MC2)
    q_col = math.sqrt(Q2_COLL)
    cache = {"k2_bm": k2_bm, "p2_c": p2_c, "q_col": q_col, "xf": {}, "zD": {}}
    return cache


def xf_at(mstw, cache, flavour, x):
    key = (flavour, round(x, 10))
    if(key in cache["xf"]):
        return cache["xf"][key]
    total = 0.0
    for parton_id in MSTW_FLAVOUR[flavour]:
        total += float(mstw.mstw_xf(int(parton_id), float(x), float(cache["q_col"])))
    cache["xf"][key] = total
    return total


def zD_at(dss, cache, flavour, z):
    key = (flavour, round(z, 10))
    if(key in cache["zD"]):
        return cache["zD"][key]
    value = float(dss.xfxQ(int(DSS_PID[flavour]), float(z), float(cache["q_col"])))
    cache["zD"][key] = value
    return value


def boer_mulders(mstw, dss, cache, x, y, z, pT, mass_scale=1.0):
    nucleon = M_NUCLEON * mass_scale
    pion    = M_PION * mass_scale
    m_bm    = math.sqrt(MBM2)
    m_c     = math.sqrt(MC2)
    k2_bm   = cache["k2_bm"]
    p2_c    = cache["p2_c"]
    width_bm  = (z * z) * k2_bm + p2_c
    width_unp = (z * z) * K2_UNP + P2_UNP
    numer = 0.0
    denom = 0.0
    for flavour in range(6):
        charge2 = CHARGE2[flavour]
        xf      = xf_at(mstw, cache, flavour, x)
        zD      = zD_at(dss, cache, flavour, z)
        # zD is z D1. The same factor sits in every Collins and unpolarized term.
        denom += charge2 * xf * zD
        if(BM_LAMBDA[flavour] == 0.0):
            continue
        if(COLLINS_N[flavour] == 0.0):
            continue
        shape_x = x_shape(BM_A[flavour], BM_ALPHA[flavour], BM_BETA, x)
        shape_z = x_shape(COLLINS_N[flavour], COLLINS_GAMMA, COLLINS_DELTA, z)
        xh1 = -math.sqrt(math.e / 2.0) / (nucleon * m_bm) * (k2_bm ** 2) / K2_UNP * BM_LAMBDA[flavour] * shape_x * xf
        h1  = math.sqrt(math.e / 2.0) / (z * pion * m_c) * (p2_c ** 2) / P2_UNP * shape_z * zD
        numer += charge2 * xh1 * h1
    g_ratio = gaussian(pT * pT, width_bm) / gaussian(pT * pT, width_unp)
    structure = 4.0 * nucleon * pion * (pT * pT) * ((z / width_bm) ** 2) * g_ratio * numer / denom
    return structure * lepton_cos_2phi(y)


def load_bins(json_path):
    with open(json_path) as handle:
        payload = json.load(handle)
    fit_dict = payload[FIT_KEY]
    info_map = {}
    rows = []
    for key_str in fit_dict.keys():
        q2y_bin = int(key_str.split("(Q2_y_Bin_")[1].split(")")[0])
        zpt_bin = int(key_str.split("(z_pT_Bin_")[1].split(")")[0])
        if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin, BINNING_METHOD="_Y_bin", Common_z_pT_Range_Q=False)):
            continue
        Construct_JSON_Info(Q2_y_Bin=str(q2y_bin), z_pT_Bin=str(zpt_bin), return_info=info_map)
        info = info_map[key_str]
        entry = fit_dict[key_str]
        q2 = float(info["Q2range"][0])
        y  = float(info["y_range"][0])
        z  = float(info["z_range"][0])
        pT = float(info["pTrange"][0])
        rows.append({
            "key": key_str,
            "q2y": q2y_bin,
            "zpt": zpt_bin,
            "q2": q2,
            "y": y,
            "z": z,
            "pT": pT,
            "x": q2 / (2.0 * M_NUCLEON * E_BEAM * y),
            "z_group": int(info["z__group"]),
            "pT_group": int(info["pT_group"]),
            "z_color": int(info["z__color"]),
            "pT_color": int(info["pT_color"]),
            "z_marker": int(info["z__marker"]),
            "pT_marker": int(info["pT_marker"]),
            "B": float(entry["Fit_Par_B"]),
            "B_sys": float(entry["Fit_Par_B_SYS"]),
            "C": float(entry["Fit_Par_C"]),
            "C_sys": float(entry["Fit_Par_C_SYS"]),
            "q2_min": float(info["Q2range"][1]),
            "q2_max": float(info["Q2range"][2]),
            "y_min": float(info["y_range"][1]),
            "y_max": float(info["y_range"][2]),
        })
    rows.sort(key=lambda row: (row["q2y"], row["zpt"]))
    return rows


def median(values):
    ordered = sorted(values)
    count = len(ordered)
    mid = count // 2
    if((count % 2) == 1):
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def rms(values):
    return math.sqrt(sum([value * value for value in values]) / float(len(values)))


def fill_theory(rows, mstw, dss):
    cache = prepare_collinear(mstw, dss)
    for row in rows:
        row["cahn_phi"]  = cahn_cos_phi(row["q2"], row["y"], row["z"], row["pT"])
        row["cahn_2phi"] = cahn_cos_2phi(row["q2"], row["y"], row["z"], row["pT"])
        row["bm"] = boer_mulders(mstw, dss, cache, row["x"], row["y"], row["z"], row["pT"], 1.0)
    doubled = None
    for row in rows:
        if((row["q2y"] == 1) and (row["zpt"] == 1)):
            doubled = boer_mulders(mstw, dss, cache, row["x"], row["y"], row["z"], row["pT"], 2.0)
            row["bm_double_mass"] = doubled
    return doubled


def require_close(name, value, target, tol):
    if(abs(value - target) > tol):
        raise SystemExit("%s = %.12g, target %.12g" % (name, value, target))
    print("%s = %.12g" % (name, value))


def check_rows(rows, check_measured=True):
    if(len(rows) != 452):
        raise SystemExit("expected 452 bins, found %d" % len(rows))
    bin11 = None
    for row in rows:
        if((row["q2y"] == 1) and (row["zpt"] == 1)):
            bin11 = row
    if(bin11 is None):
        raise SystemExit("bin (1,1) is missing")
    if(any([row["bm"] >= 0.0 for row in rows])):
        raise SystemExit("a Boer-Mulders value is not negative")
    require_close("x(1,1)", bin11["x"], 0.158001, 2.0e-6)
    require_close("Cahn phi (1,1)", bin11["cahn_phi"], -0.119125112809, 2.0e-9)
    require_close("Cahn 2phi (1,1)", bin11["cahn_2phi"], 0.002288160329, 2.0e-9)
    require_close("BM (1,1)", bin11["bm"], -0.002502403576, 2.0e-5)
    require_close("median Cahn phi", median([row["cahn_phi"] for row in rows]), -0.216961890660, 2.0e-6)
    require_close("median Cahn 2phi", median([row["cahn_2phi"] for row in rows]), 0.006687434678, 2.0e-6)
    require_close("median BM", median([row["bm"] for row in rows]), -0.006459882814, 2.0e-5)
    measured = [
        ("median B", median([row["B"] for row in rows]), -0.081220013228, 2.0e-9),
        ("median C", median([row["C"] for row in rows]), -0.004871686379, 2.0e-9),
        ("rms phi", rms([row["B"] - row["cahn_phi"] for row in rows]), 0.182614107478, 2.0e-6),
        ("rms 2phi", rms([row["C"] - row["cahn_2phi"] for row in rows]), 0.033427224584, 2.0e-6),
        ("rms BM", rms([row["C"] - row["bm"] for row in rows]), 0.036544986670, 2.0e-5),
    ]
    for name, value, target, tol in measured:
        if(check_measured):
            require_close(name, value, target, tol)
        else:
            print("%s = %.12g" % (name, value))
    relative = abs(bin11["bm_double_mass"] - bin11["bm"]) / abs(bin11["bm"])
    print("mass-cancellation relative change at (1,1) = %.3e" % relative)
    if(relative > 1.0e-8):
        raise SystemExit("nucleon and pion masses do not cancel")


def layout_map():
    mapping  = {}
    bin_num  = 1
    max_cols = max(LAYOUT)
    nrows    = len(LAYOUT)
    for row in range(nrows):
        ncol = LAYOUT[row]
        col_start = max_cols - ncol
        for ii in range(ncol):
            col = (max_cols - 1) - ii
            mapping[bin_num] = (row, col, col_start)
            bin_num += 1
    return mapping, max_cols, nrows


def pad_edges(mapping, max_cols):
    row_bins = {}
    for q2y_bin in mapping.keys():
        row, col, col_start = mapping[q2y_bin]
        if(row not in row_bins):
            row_bins[row] = []
        row_bins[row].append((col, q2y_bin, col_start))
    for row in row_bins.keys():
        row_bins[row].sort(key=lambda item: item[0])
    left_big   = 0.22
    left_small = 0.0
    right_margin = 0.0
    x_edges = {}
    for row in row_bins.keys():
        pads = row_bins[row]
        n_present = len(pads)
        big_flags = []
        for col, q2y_bin, col_start in pads:
            big_flags.append(col == col_start)
        n_big = sum([1 for flag in big_flags if(flag)])
        plot_frac_small = 1.0 - left_small - right_margin
        plot_frac_big   = 1.0 - left_big - right_margin
        ratio = plot_frac_small / plot_frac_big
        width_small = 1.0 / (float(max_cols - 1) + float(ratio))
        width_big   = width_small * ratio
        widths = [(width_big if(big_flags[i]) else width_small) for i in range(n_present)]
        cursor = 1.0 - sum(widths)
        for i, (col, q2y_bin, col_start) in enumerate(pads):
            x0 = cursor
            cursor = cursor + widths[i]
            x1 = cursor
            if(i == (n_present - 1)):
                x1 = 1.0
            x_edges[q2y_bin] = (float(x0), float(x1))
    return x_edges


def series_polylines(points):
    # points: (x, y, group). Break the line where a z or P_T row is skipped.
    ordered = sorted(points, key=lambda item: item[0])
    lines = []
    current = []
    previous_group = None
    for x_value, y_value, group in ordered:
        if((previous_group is not None) and (abs(group - previous_group) != 1)):
            if(len(current) >= 2):
                lines.append(current)
            current = []
        current.append((x_value, y_value))
        previous_group = group
    if(len(current) >= 2):
        lines.append(current)
    return lines


def draw_curve(canvas, points, color, line_style):
    graph = ROOT.TGraph(len(points))
    for index, (x_value, y_value) in enumerate(points):
        graph.SetPoint(index, float(x_value), float(y_value))
    graph.SetLineColor(int(color))
    graph.SetLineStyle(int(line_style))
    graph.SetLineWidth(2)
    graph.SetMarkerSize(0)
    graph.Draw("L SAME")
    canvas._keepalive.append(graph)


def draw_one(rows, x_mode, y_name, curves, out_path, y_title, legend_entries):
    mapping, max_cols, nrows = layout_map()
    x_edges = pad_edges(mapping, max_cols)
    grouped = {}
    x_values = []
    y_low  = None
    y_high = None
    for row in rows:
        if(row["q2y"] not in grouped):
            grouped[row["q2y"]] = []
        grouped[row["q2y"]].append(row)
        if(x_mode == "z"):
            x_values.append(row["z"])
        else:
            x_values.append(row["pT"])
        meas = row["B"] if(y_name == "B") else row["C"]
        sys  = row["B_sys"] if(y_name == "B") else row["C_sys"]
        candidates = [meas - abs(sys), meas + abs(sys)]
        for curve_name, line_style in curves:
            candidates.append(row[curve_name])
        for candidate in candidates:
            if((y_low is None) or (candidate < y_low)):
                y_low = candidate
            if((y_high is None) or (candidate > y_high)):
                y_high = candidate
    pad = 0.08 * (y_high - y_low)
    y_low  = y_low - pad
    y_high = y_high + pad
    print("%s vs %s y range %.4f %.4f" % (y_name, x_mode, y_low, y_high))
    x_span = max(x_values) - min(x_values)
    x_low  = min(x_values) - (0.04 * x_span)
    x_high = max(x_values) + (0.42 * x_span)

    canvas = ROOT.TCanvas("theory_stepped_%s_%s" % (y_name, x_mode), "theory_stepped", 2800, 3200)
    canvas.SetFillColor(0)
    canvas.SetMargin(0.0, 0.0, 0.0, 0.0)
    canvas._keepalive = []
    title_space = 0.090
    title = ROOT.TLatex()
    title.SetNDC(True)
    title.SetTextAlign(23)
    title.SetTextFont(62)
    title.SetTextSize(0.028)
    if(y_name == "B"):
        title_text = "#splitline{A_{UU}^{cos #phi} vs %s}{published-width Cahn}" % ("z" if(x_mode == "z") else "P_{T}")
    else:
        title_text = "#splitline{A_{UU}^{cos 2#phi} vs %s}{kinematic Cahn and Boer--Mulders term}" % ("z" if(x_mode == "z") else "P_{T}")
    title.DrawLatex(0.50, 0.985, title_text)
    canvas._keepalive.append(title)

    for q2y_bin in range(1, 18):
        row_index, col, col_start = mapping[q2y_bin]
        x0, x1 = x_edges[q2y_bin]
        y0 = (float(row_index) / float(nrows)) * (1.0 - title_space)
        y1 = (float(row_index + 1) / float(nrows)) * (1.0 - title_space)
        pad = ROOT.TPad("pad_%d_%s_%s" % (q2y_bin, y_name, x_mode), "", float(x0), float(y0), float(x1), float(y1))
        is_bottom = (row_index == 0)
        is_left   = (col == col_start)
        pad.SetFillColor(0)
        pad.SetFrameLineWidth(1)
        pad.SetTickx(1)
        pad.SetTicky(1)
        pad.SetGrid(1, 1)
        pad.SetLeftMargin(0.22 if(is_left) else 0.0)
        pad.SetBottomMargin(0.20 if(is_bottom) else 0.0)
        pad.SetRightMargin(0.0)
        pad.SetTopMargin(0.0)
        pad.Draw()
        pad.cd()
        frame = pad.DrawFrame(x_low, y_low, x_high, y_high)
        frame.SetTitle("")
        if(x_mode == "z"):
            x_title = "z"
        else:
            x_title = "P_{T}"
        frame.GetXaxis().SetTitle(x_title if(is_bottom) else "")
        frame.GetYaxis().SetTitle(y_title if(is_left) else "")
        frame.GetXaxis().SetTitleSize(0.080 if(is_bottom) else 0.0)
        frame.GetYaxis().SetTitleSize(0.080 if(is_left) else 0.0)
        frame.GetXaxis().SetLabelSize(0.070 if(is_bottom) else 0.0)
        frame.GetYaxis().SetLabelSize(0.070 if(is_left) else 0.0)
        if(is_left):
            frame.GetYaxis().SetTitleOffset(0.85)
        frame.GetXaxis().SetNdivisions(505)
        frame.GetYaxis().SetNdivisions(505)
        canvas._keepalive.append(frame)
        canvas._keepalive.append(pad)

        by_series = {}
        for row in grouped.get(q2y_bin, []):
            if(x_mode == "z"):
                series = row["pT_group"]
                color  = row["pT_color"]
                marker = row["pT_marker"]
                x_value = row["z"]
                group = row["z_group"]
                legend_value = row["pT"]
            else:
                series = row["z_group"]
                color  = row["z_color"]
                marker = row["z_marker"]
                x_value = row["pT"]
                group = row["pT_group"]
                legend_value = row["z"]
            if(series not in by_series):
                by_series[series] = {"color": color, "marker": marker, "legend": legend_value, "points": [], "curves": {}}
            meas = row["B"] if(y_name == "B") else row["C"]
            sys  = row["B_sys"] if(y_name == "B") else row["C_sys"]
            by_series[series]["points"].append((x_value, meas, sys))
            for curve_name, line_style in curves:
                if(curve_name not in by_series[series]["curves"]):
                    by_series[series]["curves"][curve_name] = []
                by_series[series]["curves"][curve_name].append((x_value, row[curve_name], group))

        for series in sorted(by_series.keys()):
            spec = by_series[series]
            for curve_name, line_style in curves:
                for line in series_polylines(spec["curves"][curve_name]):
                    draw_curve(canvas, line, spec["color"], line_style)
            graph = ROOT.TGraphErrors(len(spec["points"]))
            for index, (x_value, meas, sys) in enumerate(spec["points"]):
                graph.SetPoint(index, float(x_value), float(meas))
                graph.SetPointError(index, 0.0, float(abs(sys)))
            graph.SetMarkerColor(int(spec["color"]))
            graph.SetLineColor(int(spec["color"]))
            graph.SetMarkerStyle(int(spec["marker"]))
            graph.SetMarkerSize(1.35)
            graph.SetLineWidth(2)
            graph.Draw("P E1 SAME")
            canvas._keepalive.append(graph)

        legend_title = "P_{T} Bins" if(x_mode == "z") else "z Bins"
        entries = []
        for series in by_series.keys():
            entries.append((by_series[series]["legend"], by_series[series]["color"]))
        entries.sort(key=lambda item: item[0])
        if(len(entries) > 0):
            leg_y1 = 0.72
            leg_y0 = leg_y1 - (0.042 * float(len(entries) + 1))
            if(leg_y0 < 0.08):
                leg_y0 = 0.08
            leg = ROOT.TLegend(0.74, float(leg_y0), 0.98, float(leg_y1))
            leg.SetBorderSize(1)
            leg.SetFillStyle(1001)
            leg.SetFillColor(ROOT.kWhite)
            leg.SetTextFont(42)
            leg.SetTextSize(0.055)
            leg.SetHeader(legend_title, "C")
            for value, color in entries:
                entry = leg.AddEntry(0, "%.3f" % value, "")
                if(entry):
                    entry.SetTextColor(int(color))
            leg.Draw("SAME")
            canvas._keepalive.append(leg)

        sample = grouped[q2y_bin][0]
        label = ROOT.TLatex()
        label.SetNDC(True)
        label.SetTextAlign(23)
        label.SetTextFont(42)
        label.SetTextSize(0.070)
        label.DrawLatex(0.50, 0.965, "Q^{2}-y Bin %d" % q2y_bin)
        label.DrawLatex(0.50, 0.965 - 1.10 * 0.070, "%.2f < Q^{2} < %.2f" % (sample["q2_min"], sample["q2_max"]))
        label.DrawLatex(0.50, 0.965 - 2.20 * 0.070, "%.2f < y < %.2f" % (sample["y_min"], sample["y_max"]))
        canvas._keepalive.append(label)
        pad.Update()
        canvas.cd()

    canvas.cd()
    # Empty top-left of the stepped map, under the canvas title.
    page_leg = ROOT.TLegend(0.04, 0.905 - 0.026 * float(len(legend_entries)), 0.42, 0.900)
    page_leg.SetBorderSize(0)
    page_leg.SetFillStyle(0)
    page_leg.SetTextFont(42)
    page_leg.SetTextSize(0.016)
    proxies = []
    for label_text, marker_style, line_style in legend_entries:
        proxy = ROOT.TGraph(1)
        proxy.SetPoint(0, 0.0, 0.0)
        proxy.SetMarkerStyle(int(marker_style))
        proxy.SetMarkerColor(ROOT.kBlack)
        proxy.SetMarkerSize(1.4)
        proxy.SetLineColor(ROOT.kBlack)
        proxy.SetLineStyle(int(line_style))
        proxy.SetLineWidth(2)
        draw_opt = "P" if(line_style == 0) else "L"
        page_leg.AddEntry(proxy, label_text, draw_opt)
        proxies.append(proxy)
    page_leg.Draw()
    canvas._keepalive.append(page_leg)
    canvas._keepalive.extend(proxies)
    canvas.Update()
    canvas.SaveAs(out_path)
    print("wrote %s" % out_path)
    canvas.Close()


def archive_current():
    os.makedirs(ARCHIVE, exist_ok=True)
    names = [
        "Theory_CosPhi_vs_z.pdf",
        "Theory_CosPhi_vs_pT.pdf",
        "Theory_Cos2Phi_vs_z.pdf",
        "Theory_Cos2Phi_vs_pT.pdf",
    ]
    for name in names:
        source = os.path.join(IMAGE_DIR, name)
        destination = os.path.join(ARCHIVE, name)
        if(not os.path.exists(destination)):
            shutil.copy2(source, destination)
            print("archived %s" % destination)


def main(json_path, image_dir, do_archive, check_measured=True):
    lhapdf.pathsPrepend(DSS_DIR)
    dss  = lhapdf.mkPDF("dsspipLO", 0)
    mstw = load_mstw()
    rows = load_bins(json_path)
    fill_theory(rows, mstw, dss)
    check_rows(rows, check_measured)
    if(do_archive):
        archive_current()
    os.makedirs(image_dir, exist_ok=True)
    y_phi = "A_{UU}^{cos #phi}"
    y_2phi = "A_{UU}^{cos 2#phi}"
    legend_phi = [("measurement", 20, 0), ("Cahn, published widths", 1, 1)]
    legend_2phi = [("measurement", 20, 0), ("kinematic Cahn", 1, 1), ("Boer-Mulders term", 1, 7)]
    draw_one(rows, "z",  "B", [("cahn_phi", 1)], os.path.join(image_dir, "Theory_CosPhi_vs_z.pdf"), y_phi, legend_phi)
    draw_one(rows, "pT", "B", [("cahn_phi", 1)], os.path.join(image_dir, "Theory_CosPhi_vs_pT.pdf"), y_phi, legend_phi)
    draw_one(rows, "z",  "C", [("cahn_2phi", 1), ("bm", 7)], os.path.join(image_dir, "Theory_Cos2Phi_vs_z.pdf"), y_2phi, legend_2phi)
    draw_one(rows, "pT", "C", [("cahn_2phi", 1), ("bm", 7)], os.path.join(image_dir, "Theory_Cos2Phi_vs_pT.pdf"), y_2phi, legend_2phi)


if(__name__ == "__main__"):
    import argparse
    parser = argparse.ArgumentParser(description="Redraw the four theory comparison figures.")
    parser.add_argument("-j", "--json_file", default=JSON_PATH)
    parser.add_argument("-d", "--image_dir", default=IMAGE_DIR)
    parser.add_argument("-sm", "--skip_measured_regression", action="store_true", help="Keep the theory-curve checks and draw the current measured centrals. The older measured-median targets stay in force unless this is set.")
    args = parser.parse_args()
    main(args.json_file, args.image_dir, os.path.abspath(args.image_dir) == os.path.abspath(IMAGE_DIR), not args.skip_measured_regression)
