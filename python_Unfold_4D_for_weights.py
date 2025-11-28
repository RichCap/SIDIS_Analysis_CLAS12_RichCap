#!/usr/bin/env python3

import ROOT, numpy, re
import traceback
import sys
import os
import argparse
import math
import array
import copy
import subprocess

# ----------------------------------------------------------------------
# Imports from your analysis environment
# ----------------------------------------------------------------------
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *  # color, etc.
from ExtraAnalysisCodeValues import *
sys.path.remove(script_dir)
del script_dir

EMAIL_RECIPIENT = "richard.capobianco@uconn.edu"

# ----------------------------------------------------------------------
# ANSI → HTML + email helper
# ----------------------------------------------------------------------
def ansi_to_html(text):
    ansi_html_map = {
        '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
        '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "",
        '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
        '\033[0m': "",
    }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text


def send_email(subject, body):
    if(EMAIL_RECIPIENT is None):
        return
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, EMAIL_RECIPIENT], input=html_body.encode(), check=False)


def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")
    obj.Write()


# ----------------------------------------------------------------------
# pT ranges per Q2_y_Bin (as provided)
# ----------------------------------------------------------------------
pT_Ranges_per_Q2_y_Bin = {
    1:  [[0.05, 0.22], [0.22, 0.32], [0.32, 0.42], [0.42, 0.52], [0.52, 0.63], [0.63, 0.75], [0.75, 0.99]],
    2:  [[0.05, 0.25], [0.25, 0.35], [0.35, 0.45], [0.45, 0.54], [0.54, 0.67], [0.67, 0.93]],
    3:  [[0.05, 0.20], [0.20, 0.30], [0.30, 0.39], [0.39, 0.49], [0.49, 0.59], [0.59, 0.76]],
    4:  [[0.05, 0.20], [0.20, 0.29], [0.29, 0.38], [0.38, 0.48], [0.48, 0.61], [0.61, 0.85]],
    5:  [[0.05, 0.22], [0.22, 0.32], [0.32, 0.41], [0.41, 0.51], [0.51, 0.65], [0.65, 0.98]],
    6:  [[0.05, 0.22], [0.22, 0.32], [0.32, 0.41], [0.41, 0.51], [0.51, 0.65], [0.65, 1.00]],
    7:  [[0.05, 0.20], [0.20, 0.29], [0.29, 0.38], [0.38, 0.48], [0.48, 0.60], [0.60, 0.83]],
    8:  [[0.05, 0.20], [0.20, 0.29], [0.29, 0.37], [0.37, 0.46], [0.46, 0.60]],
    9:  [[0.05, 0.22], [0.22, 0.30], [0.30, 0.38], [0.38, 0.46], [0.46, 0.58], [0.58, 0.74], [0.74, 0.95]],
    10: [[0.05, 0.21], [0.21, 0.31], [0.31, 0.40], [0.40, 0.50], [0.50, 0.64], [0.64, 0.90]],
    11: [[0.05, 0.20], [0.20, 0.30], [0.30, 0.40], [0.40, 0.53], [0.53, 0.69]],
    12: [[0.05, 0.20], [0.20, 0.28], [0.28, 0.36], [0.36, 0.45], [0.45, 0.60]],
    13: [[0.05, 0.22], [0.22, 0.34], [0.34, 0.44], [0.44, 0.58], [0.58, 0.90]],
    14: [[0.05, 0.21], [0.21, 0.31], [0.31, 0.40], [0.40, 0.50], [0.50, 0.64], [0.64, 0.90]],
    15: [[0.05, 0.22], [0.22, 0.32], [0.32, 0.42], [0.42, 0.55], [0.55, 0.80]],
    16: [[0.05, 0.22], [0.22, 0.32], [0.32, 0.42], [0.42, 0.52], [0.52, 0.66], [0.66, 0.90]],
    17: [[0.05, 0.19], [0.19, 0.28], [0.28, 0.37], [0.37, 0.45], [0.45, 0.55], [0.55, 0.73]],
}

Z_MIN = 0.16
Z_MAX = 0.77

Q2_Centers = [2.20, 2.65, 3.30, 4.50, 6.60]
y_Centers  = [0.40, 0.50, 0.60, 0.70]

# We will re-use this everywhere:
PARAM_NAMES = ["a0", "a1", "a2",
               "b0", "b1", "b2",
               "c0", "c1", "c2"]


# ----------------------------------------------------------------------
# 4D → (Q2_y_Bin, z_pT_Bin) decoder
# ----------------------------------------------------------------------
def decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins):
    if(Q2_y_z_pT_4D_Bins <= 0):
        return 0, 0

    max_Q2_y_Bin = 17

    for Q2_y_Bin in range(max_Q2_y_Bin, 0, -1):
        offset = 0

        if(Q2_y_Bin >  1):
            offset += 35
        if(Q2_y_Bin >  2):
            offset += 36
        if(Q2_y_Bin >  3):
            offset += 30
        if(Q2_y_Bin >  4):
            offset += 36
        if(Q2_y_Bin >  5):
            offset += 36
        if(Q2_y_Bin >  6):
            offset += 30
        if(Q2_y_Bin >  7):
            offset += 36
        if(Q2_y_Bin >  8):
            offset += 35
        if(Q2_y_Bin >  9):
            offset += 35
        if(Q2_y_Bin > 10):
            offset += 36
        if(Q2_y_Bin > 11):
            offset += 25
        if(Q2_y_Bin > 12):
            offset += 25
        if(Q2_y_Bin > 13):
            offset += 30
        if(Q2_y_Bin > 14):
            offset += 36
        if(Q2_y_Bin > 15):
            offset += 25
        if(Q2_y_Bin > 16):
            offset += 30

        if(Q2_y_z_pT_4D_Bins > offset):
            z_pT_Bin = Q2_y_z_pT_4D_Bins - offset
            return Q2_y_Bin, z_pT_Bin

    return 0, 0


# ----------------------------------------------------------------------
# Decode 2D bin indices into kinematic values
# ----------------------------------------------------------------------
def decode_kinematics_from_bins(Q2_y_Bin_Find_In, z_pT_Bin_Find_In):
    Q2_y_bins, z_pT_bins = Find_Q2_y_z_pT_Bin_Stats(Q2_y_Bin_Find=Q2_y_Bin_Find_In, z_pT_Bin_Find=z_pT_Bin_Find_In, List_Of_Histos_For_Stats_Search="Use_Center", Smearing_Q="''", DataType="bbb", Binning_Method_Input=Binning_Method)
    Q2_bins, y_bins = Q2_y_bins
    z_bins, pT_bins = z_pT_bins
    Q2_val, y_val, z_val, pT_val = Q2_bins[1], y_bins[1], z_bins[1], pT_bins[1]
    return Q2_val, y_val, z_val, pT_val


# ----------------------------------------------------------------------
# Build or fetch the ratio histogram: h_ratio = h_num / h_den
# ----------------------------------------------------------------------
def build_ratio_histogram(root_file, num_name, den_name, ratio_name, force_ratio):
    if((root_file is None) or root_file.IsZombie()):
        raise RuntimeError("Input ROOT file is not open or is a zombie.")

    num_hist = root_file.Get(num_name)
    den_hist = root_file.Get(den_name)

    if(num_hist is None):
        raise RuntimeError(f"Numerator histogram '{num_name}' not found in file.")
    if(den_hist is None):
        raise RuntimeError(f"Denominator histogram '{den_name}' not found in file.")

    ratio_hist = num_hist.Clone(ratio_name)
    ratio_hist.SetDirectory(0)
    ratio_hist.Divide(num_hist, den_hist)
    ratio_hist.SetTitle(f"{ratio_name}")

    root_file.cd()
    safe_write(ratio_hist, root_file)

    print(f"{color.BGREEN}Created ratio histogram '{ratio_name}' and wrote it to file.{color.END}")
    return ratio_hist


# ----------------------------------------------------------------------
# Convert TH1D ratio histogram → RDataFrame with 7 columns
# ----------------------------------------------------------------------
def build_dataframe_from_hist(ratio_hist):
    if(ratio_hist is None):
        raise RuntimeError("build_dataframe_from_hist: ratio_hist is None.")

    n_bins = ratio_hist.GetNbinsX()

    Q2_y_Bin_list = []
    Q2_val_list   = []
    y_val_list    = []
    z_val_list    = []
    pT_val_list   = []
    content_list  = []
    error_list    = []

    for ibin in range(1, n_bins + 1):
        Q2_y_z_pT_4D_Bins = int(ratio_hist.GetBinCenter(ibin))

        Q2_y_Bin, z_pT_Bin = decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins)
        if((Q2_y_Bin <= 0) or (z_pT_Bin <= 0)):
            continue

        bin_content = ratio_hist.GetBinContent(ibin)
        bin_error   = ratio_hist.GetBinError(ibin)

        Q2_val, y_val, z_val, pT_val = decode_kinematics_from_bins(Q2_y_Bin, z_pT_Bin)

        Q2_y_Bin_list.append(Q2_y_Bin)
        Q2_val_list.append(Q2_val)
        y_val_list.append(y_val)
        z_val_list.append(z_val)
        pT_val_list.append(pT_val)
        content_list.append(bin_content)
        error_list.append(bin_error)

    if(len(Q2_y_Bin_list) == 0):
        print(f"{color.YELLOW}Warning: No valid bins were converted into dataframe entries.{color.END}")

    n_entries = len(Q2_y_Bin_list)

    memfile = ROOT.TMemFile("tmp_unfold_4D_mem", "RECREATE")
    tree    = ROOT.TTree("h22_tmp", "h22_tmp")

    b_Q2_y_Bin = array.array("i", [0])
    b_Q2_val   = array.array("d", [0.0])
    b_y_val    = array.array("d", [0.0])
    b_z_val    = array.array("d", [0.0])
    b_pT_val   = array.array("d", [0.0])
    b_content  = array.array("d", [0.0])
    b_error    = array.array("d", [0.0])

    tree.Branch("Q2_y_Bin",    b_Q2_y_Bin, "Q2_y_Bin/I")
    tree.Branch("Q2_val",      b_Q2_val,   "Q2_val/D")
    tree.Branch("y_val",       b_y_val,    "y_val/D")
    tree.Branch("z_val",       b_z_val,    "z_val/D")
    tree.Branch("pT_val",      b_pT_val,   "pT_val/D")
    tree.Branch("bin_content", b_content,  "bin_content/D")
    tree.Branch("bin_error",   b_error,    "bin_error/D")

    for index in range(n_entries):
        b_Q2_y_Bin[0] = Q2_y_Bin_list[index]
        b_Q2_val[0]   = Q2_val_list[index]
        b_y_val[0]    = y_val_list[index]
        b_z_val[0]    = z_val_list[index]
        b_pT_val[0]   = pT_val_list[index]
        b_content[0]  = content_list[index]
        b_error[0]    = error_list[index]
        tree.Fill()

    memfile.Write()

    rdf = ROOT.RDataFrame(tree)
    rdf._unfold_memfile = memfile
    rdf._unfold_tree    = tree

    return rdf


# ----------------------------------------------------------------------
# Z-fit layer: bin_content vs z at fixed (Q2_y_Bin, pT range)
# Quadratic: bin_content(z) = p0 + p1*z + p2*z^2
# ----------------------------------------------------------------------
def perform_z_fits(rdf, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    print(f"{color.BCYAN}Starting z-fits using RDataFrame (quadratic in z).{color.END}")

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BCYAN}z-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    results = []

    for Q2_y_Bin_key in sorted(pT_Ranges_per_Q2_y_Bin.keys()):
        pT_ranges = pT_Ranges_per_Q2_y_Bin[Q2_y_Bin_key]

        for pT_range in pT_ranges:
            pT_min = pT_range[0]
            pT_max = pT_range[1]

            cut_expr = f"(Q2_y_Bin == {Q2_y_Bin_key}) && (pT_val >= {pT_min}) && (pT_val < {pT_max}) && (z_val >= {Z_MIN}) && (z_val <= {Z_MAX}) && (bin_content > 0.0)"
            df_slice = rdf.Filter(cut_expr, f"Q2_y_Bin={Q2_y_Bin_key}, pT in [{pT_min},{pT_max}), bin_content>0")

            np_dict  = df_slice.AsNumpy(["z_val", "bin_content", "bin_error"])
            z_vals   = numpy.array(np_dict["z_val"],        dtype="float64")
            y_vals   = numpy.array(np_dict["bin_content"],  dtype="float64")
            err_vals = numpy.array(np_dict["bin_error"],    dtype="float64")

            n_points = len(z_vals)
            if(n_points == 0):
                print(f"{color.YELLOW}Skipping Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min}, {pT_max}) due to zero valid points after bin_content>0 cut.{color.END}")
                continue

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(z_vals[idx]), float(y_vals[idx]))
                graph.SetPointError(idx, 0.0, float(err_vals[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            fit_func = ROOT.TF1("f_z_tmp", "[0] + [1]*x + [2]*x*x", Z_MIN, Z_MAX)

            intercept_guess = float(numpy.mean(y_vals))
            fit_func.SetParameter(0, intercept_guess)
            fit_func.SetParameter(1, 0.0)
            fit_func.SetParameter(2, 0.0)
            
            if(n_points < 3):
                print(f"{color.RED}Waring: {color.YELLOW}Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min}, {pT_max}) has insufficient points for quadratic fit (n={n_points}) — using linear instead.{color.END}")
                fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            intercept     = fit_func.GetParameter(0)
            intercept_err = fit_func.GetParError(0)
            slope         = fit_func.GetParameter(1)
            slope_err     = fit_func.GetParError(1)
            quad          = fit_func.GetParameter(2)
            quad_err      = fit_func.GetParError(2)
            chi2          = fit_func.GetChisquare()
            ndf           = fit_func.GetNDF()
            pT_center     = 0.5 * (pT_min + pT_max)

            print(f"{color.BBLUE}Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min:.3f}, {pT_max:.3f}) "
                  f"n={n_points}, intercept={intercept:.4g} ± {intercept_err:.4g}, "
                  f"slope={slope:.4g} ± {slope_err:.4g}, quad={quad:.4g} ± {quad_err:.4g}, "
                  f"chi2/ndf={chi2}/{ndf}{color.END}")

            if(save_plots):
                pT_center_code = int(round(1000.0 * pT_center))
                cname = f"c_zFit_Q2_y_Bin_{Q2_y_Bin_key}_pT_{pT_center_code:03d}"

                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"z-fit (quadratic): Q^{{2}}-y Bin = {Q2_y_Bin_key} #topbar P_{{T}} = [{pT_min:.2f},{pT_max:.2f})"
                graph.SetTitle(f"{title_str};z;Ratio of #frac{{Unfolded Data}}{{Generated MC}}")
                graph.Draw("AP")

                fit_func.SetLineColor(ROOT.kRed)
                fit_func.SetLineWidth(2)
                fit_func.Draw("same")

                latex = ROOT.TLatex()
                latex.SetNDC(True)
                latex.SetTextSize(0.04)
                latex.DrawLatex(0.15, 0.88, f"intercept = {intercept:.4g} #pm {intercept_err:.4g}")
                latex.DrawLatex(0.15, 0.83, f"slope     = {slope:.4g} #pm {slope_err:.4g}")
                latex.DrawLatex(0.15, 0.78, f"quad      = {quad:.4g} #pm {quad_err:.4g}")
                latex.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

                if((image_suffix is not None) and (len(str(image_suffix)) > 0)):
                    base_name = f"{cname}_{image_suffix}"
                else:
                    base_name = cname

                out_name = os.path.join(plot_dir, f"{base_name}{file_ext}")
                canvas.SaveAs(out_name)
                del canvas

            results.append({
                "Q2_y_Bin":      Q2_y_Bin_key,
                "pT_min":        pT_min,
                "pT_max":        pT_max,
                "pT_center":     pT_center,
                "n_points":      n_points,
                "intercept":     intercept,
                "intercept_err": intercept_err,
                "slope":         slope,
                "slope_err":     slope_err,
                "quad":          quad,
                "quad_err":      quad_err,
                "chi2":          chi2,
                "ndf":           ndf,
            })

    print(f"{color.BGREEN}z-fits complete. Total successful fits: {len(results)}.{color.END}")
    return results


# ----------------------------------------------------------------------
# pT-fits: intercept(pT), slope(pT), quad(pT) → 9 parameters per Q2_y_Bin
# pT-fit layer: fit intercept(pT), slope(pT), quad(pT) with quadratics
#   intercept(pT) ≈ b0 + b1*pT + b2*pT^2
#   slope(pT)     ≈ a0 + a1*pT + a2*pT^2
#   quad(pT)      ≈ c0 + c1*pT + c2*pT^2
#
# Final 2D function per Q2_y_Bin:
#   F(z,pT) = (b0 + b1*pT + b2*pT^2)
#           + (a0 + a1*pT + a2*pT^2) * z
#           + (c0 + c1*pT + c2*pT^2) * z^2
# ----------------------------------------------------------------------
def perform_pT_fits(z_fit_results, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    print(f"{color.BPURPLE}Starting pT-fits of z-fit parameters (quadratic in pT).{color.END}")

    if(len(z_fit_results) == 0):
        print(f"{color.YELLOW}No z-fit results provided; skipping pT fits.{color.END}")
        return {}

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BPURPLE}pT-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    results_by_q2 = {}
    for row in z_fit_results:
        key = int(row["Q2_y_Bin"])
        if(key not in results_by_q2):
            results_by_q2[key] = []
        results_by_q2[key].append(row)

    pt_fit_summary = {}

    for Q2_y_Bin_key in sorted(results_by_q2.keys()):
        rows = results_by_q2[Q2_y_Bin_key]
        n = len(rows)
        Linear = False
        if(n < 3):
            print(f"{color.RED}Waring: {color.YELLOW}Q2_y_Bin={Q2_y_Bin_key} only has {n} z-fit points, need ≥3 for quadratic — using linear instead.{color.END}")
            Linear = True
            
        pT_centers     = numpy.array([r["pT_center"]     for r in rows], dtype="float64")
        intercepts     = numpy.array([r["intercept"]     for r in rows], dtype="float64")
        intercept_errs = numpy.array([r["intercept_err"] for r in rows], dtype="float64")
        slopes         = numpy.array([r["slope"]         for r in rows], dtype="float64")
        slope_errs     = numpy.array([r["slope_err"]     for r in rows], dtype="float64")
        quads          = numpy.array([r["quad"]          for r in rows], dtype="float64")
        quad_errs      = numpy.array([r["quad_err"]      for r in rows], dtype="float64")

        pT_min_fit = float(min(pT_centers))
        pT_max_fit = float(max(pT_centers))

        # --- slope(pT) ---
        g_slope = ROOT.TGraphErrors(n)
        for idx in range(n):
            g_slope.SetPoint(idx, float(pT_centers[idx]), float(slopes[idx]))
            g_slope.SetPointError(idx, 0.0, float(slope_errs[idx]))
        g_slope.SetMarkerStyle(21)
        g_slope.SetMarkerSize(1.0)
        g_slope.SetLineWidth(2)

        f_slope = ROOT.TF1(f"f_slope_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", pT_min_fit, pT_max_fit)
        f_slope.SetParameter(0, float(numpy.mean(slopes)))
        f_slope.SetParameter(1, 0.0)
        f_slope.SetParameter(2, 0.0)
        if(Linear):
            f_slope.FixParameter(2, 0.0)
        g_slope.Fit(f_slope, "QSRNB")

        a0     = f_slope.GetParameter(0)
        a0_err = f_slope.GetParError(0)
        a1     = f_slope.GetParameter(1)
        a1_err = f_slope.GetParError(1)
        a2     = f_slope.GetParameter(2)
        a2_err = f_slope.GetParError(2)
        chi2_s = f_slope.GetChisquare()
        ndf_s  = f_slope.GetNDF()

        # --- intercept(pT) ---
        g_int = ROOT.TGraphErrors(n)
        for idx in range(n):
            g_int.SetPoint(idx, float(pT_centers[idx]), float(intercepts[idx]))
            g_int.SetPointError(idx, 0.0, float(intercept_errs[idx]))
        g_int.SetMarkerStyle(22)
        g_int.SetMarkerSize(1.0)
        g_int.SetLineWidth(2)

        f_int = ROOT.TF1(f"f_int_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", pT_min_fit, pT_max_fit)
        f_int.SetParameter(0, float(numpy.mean(intercepts)))
        f_int.SetParameter(1, 0.0)
        f_int.SetParameter(2, 0.0)
        if(Linear):
            f_int.FixParameter(2, 0.0)
        g_int.Fit(f_int, "QSRNB")

        b0     = f_int.GetParameter(0)
        b0_err = f_int.GetParError(0)
        b1     = f_int.GetParameter(1)
        b1_err = f_int.GetParError(1)
        b2     = f_int.GetParameter(2)
        b2_err = f_int.GetParError(2)
        chi2_i = f_int.GetChisquare()
        ndf_i  = f_int.GetNDF()

        # --- quad(pT) ---
        g_quad = ROOT.TGraphErrors(n)
        for idx in range(n):
            g_quad.SetPoint(idx, float(pT_centers[idx]), float(quads[idx]))
            g_quad.SetPointError(idx, 0.0, float(quad_errs[idx]))
        g_quad.SetMarkerStyle(23)
        g_quad.SetMarkerSize(1.0)
        g_quad.SetLineWidth(2)

        f_quad = ROOT.TF1(f"f_quad_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", pT_min_fit, pT_max_fit)
        f_quad.SetParameter(0, float(numpy.mean(quads)))
        f_quad.SetParameter(1, 0.0)
        f_quad.SetParameter(2, 0.0)
        if(Linear):
            f_quad.FixParameter(2, 0.0)
        g_quad.Fit(f_quad, "QSRNB")

        c0     = f_quad.GetParameter(0)
        c0_err = f_quad.GetParError(0)
        c1     = f_quad.GetParameter(1)
        c1_err = f_quad.GetParError(1)
        c2     = f_quad.GetParameter(2)
        c2_err = f_quad.GetParError(2)
        chi2_q = f_quad.GetChisquare()
        ndf_q  = f_quad.GetNDF()

        print(f"{color.BPURPLE}Q2_y_Bin={Q2_y_Bin_key}:")
        print(f"  slope(pT)     = a0 + a1*pT + a2*pT^2 with "
              f"a0={a0:.4g}±{a0_err:.4g}, a1={a1:.4g}±{a1_err:.4g}, a2={a2:.4g}±{a2_err:.4g}, chi2/ndf={chi2_s}/{ndf_s}")
        print(f"  intercept(pT) = b0 + b1*pT + b2*pT^2 with "
              f"b0={b0:.4g}±{b0_err:.4g}, b1={b1:.4g}±{b1_err:.4g}, b2={b2:.4g}±{b2_err:.4g}, chi2/ndf={chi2_i}/{ndf_i}")
        print(f"  quad(pT)      = c0 + c1*pT + c2*pT^2 with "
              f"c0={c0:.4g}±{c0_err:.4g}, c1={c1:.4g}±{c1_err:.4g}, c2={c2:.4g}±{c2_err:.4g}, chi2/ndf={chi2_q}/{ndf_q}{color.END}")

        if(save_plots):
            # Slope vs pT plot
            cname_slope = f"c_pTFit_slope_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_s = ROOT.TCanvas(cname_slope, cname_slope, 800, 600)
            title_s  = f"Slope vs P_{{T}} (quadratic): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
            g_slope.SetTitle(f"{title_s};P_{{T}} (GeV);Slope of z-fit")
            g_slope.Draw("AP")
            f_slope.SetLineColor(ROOT.kRed)
            f_slope.SetLineWidth(2)
            f_slope.Draw("same")

            latex_s = ROOT.TLatex()
            latex_s.SetNDC(True)
            latex_s.SetTextSize(0.04)
            latex_s.DrawLatex(0.15, 0.88, f"a0 = {a0:.4g} #pm {a0_err:.4g}")
            latex_s.DrawLatex(0.15, 0.83, f"a1 = {a1:.4g} #pm {a1_err:.4g}")
            latex_s.DrawLatex(0.15, 0.78, f"a2 = {a2:.4g} #pm {a2_err:.4g}")
            latex_s.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2_s:.1f} / {ndf_s}")

            base_s = f"{cname_slope}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname_slope
            out_s = os.path.join(plot_dir, f"{base_s}{file_ext}")
            canvas_s.SaveAs(out_s)
            del canvas_s

            # Intercept vs pT plot
            cname_i = f"c_pTFit_intercept_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_i = ROOT.TCanvas(cname_i, cname_i, 800, 600)
            title_i  = f"Intercept vs P_{{T}} (quadratic): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
            g_int.SetTitle(f"{title_i};P_{{T}} (GeV);Intercept of z-fit")
            g_int.Draw("AP")
            f_int.SetLineColor(ROOT.kRed)
            f_int.SetLineWidth(2)
            f_int.Draw("same")

            latex_i = ROOT.TLatex()
            latex_i.SetNDC(True)
            latex_i.SetTextSize(0.04)
            latex_i.DrawLatex(0.15, 0.88, f"b0 = {b0:.4g} #pm {b0_err:.4g}")
            latex_i.DrawLatex(0.15, 0.83, f"b1 = {b1:.4g} #pm {b1_err:.4g}")
            latex_i.DrawLatex(0.15, 0.78, f"b2 = {b2:.4g} #pm {b2_err:.4g}")
            latex_i.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2_i:.1f} / {ndf_i}")

            base_i = f"{cname_i}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname_i
            out_i = os.path.join(plot_dir, f"{base_i}{file_ext}")
            canvas_i.SaveAs(out_i)
            del canvas_i

            # Quad vs pT plot
            cname_q = f"c_pTFit_quad_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_q = ROOT.TCanvas(cname_q, cname_q, 800, 600)
            title_q  = f"Quad coeff vs P_{{T}} (quadratic): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
            g_quad.SetTitle(f"{title_q};P_{{T}} (GeV);Quad term of z-fit")
            g_quad.Draw("AP")
            f_quad.SetLineColor(ROOT.kRed)
            f_quad.SetLineWidth(2)
            f_quad.Draw("same")

            latex_q = ROOT.TLatex()
            latex_q.SetNDC(True)
            latex_q.SetTextSize(0.04)
            latex_q.DrawLatex(0.15, 0.88, f"c0 = {c0:.4g} #pm {c0_err:.4g}")
            latex_q.DrawLatex(0.15, 0.83, f"c1 = {c1:.4g} #pm {c1_err:.4g}")
            latex_q.DrawLatex(0.15, 0.78, f"c2 = {c2:.4g} #pm {c2_err:.4g}")
            latex_q.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2_q:.1f} / {ndf_q}")

            base_q = f"{cname_q}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname_q
            out_q = os.path.join(plot_dir, f"{base_q}{file_ext}")
            canvas_q.SaveAs(out_q)
            del canvas_q

        pt_fit_summary[Q2_y_Bin_key] = {
            "a0": a0, "a0_err": a0_err,
            "a1": a1, "a1_err": a1_err,
            "a2": a2, "a2_err": a2_err,
            "b0": b0, "b0_err": b0_err,
            "b1": b1, "b1_err": b1_err,
            "b2": b2, "b2_err": b2_err,
            "c0": c0, "c0_err": c0_err,
            "c1": c1, "c1_err": c1_err,
            "c2": c2, "c2_err": c2_err,
            "chi2_slope": chi2_s,
            "ndf_slope":  ndf_s,
            "chi2_int":   chi2_i,
            "ndf_int":    ndf_i,
            "chi2_quad":  chi2_q,
            "ndf_quad":   ndf_q,
        }

    print(f"{color.BGREEN}pT-fits complete. Total Q2_y_Bins with 9-parameter (z,pT) description: {len(pt_fit_summary)}.{color.END}")
    return pt_fit_summary


# ----------------------------------------------------------------------
# Attach pT-fit parameters as columns in the RDataFrame (by Q2_y_Bin)
# ----------------------------------------------------------------------
def attach_pT_params_to_rdf(rdf, pt_fit_summary, out_file, tree_name="h22"):

    # Take the existing RDataFrame with columns:
    #   Q2_y_Bin, Q2_val, y_val, z_val, pT_val, bin_content, bin_error and add 18 new columns:
    #   a0,a0_err,...,c2,c2_err
    # where each parameter is constant for all rows with the same Q2_y_Bin.
    # The result is written back out as a new ROOT file 'out_file', tree 'tree_name'.

    if((pt_fit_summary is None) or (len(pt_fit_summary) == 0)):
        print(f"{color.YELLOW}attach_pT_params_to_rdf: No pt_fit_summary provided; skipping augmentation.{color.END}")
        rdf.Snapshot(tree_name, out_file)
        return

    max_bin = 17

    cpp_lines = []
    cpp_lines.append("#include <cmath>")
    cpp_lines.append("struct PTParamTables {")
    cpp_lines.append("  static const int NMAX = 18;")
    for pname in PARAM_NAMES:
        cpp_lines.append(f"  static double {pname}[NMAX];")
        cpp_lines.append(f"  static double {pname}_err[NMAX];")
    cpp_lines.append("};")

    for pname in PARAM_NAMES:
        cpp_lines.append(f"double PTParamTables::{pname}[PTParamTables::NMAX] = {{0.0}};")
        cpp_lines.append(f"double PTParamTables::{pname}_err[PTParamTables::NMAX] = {{0.0}};")

    cpp_lines.append("void InitPTParamTables(){")
    for Q2_y_Bin_key in range(1, max_bin + 1):
        if(Q2_y_Bin_key not in pt_fit_summary):
            continue
        pars = pt_fit_summary[Q2_y_Bin_key]
        for pname in PARAM_NAMES:
            val = float(pars[pname])
            err = float(pars[f"{pname}_err"])
            cpp_lines.append(f"  PTParamTables::{pname}[{Q2_y_Bin_key}] = {val};")
            cpp_lines.append(f"  PTParamTables::{pname}_err[{Q2_y_Bin_key}] = {err};")
    cpp_lines.append("}")

    for pname in PARAM_NAMES:
        cpp_lines.append(
            f"double Get_{pname}(int bin){{ "
            f"if(bin < 0 || bin >= PTParamTables::NMAX) return 0.0; "
            f"return PTParamTables::{pname}[bin]; }}"
        )
        cpp_lines.append(
            f"double Get_{pname}_err(int bin){{ "
            f"if(bin < 0 || bin >= PTParamTables::NMAX) return 0.0; "
            f"return PTParamTables::{pname}_err[bin]; }}"
        )

    cpp_code = "\n".join(cpp_lines)
    ROOT.gInterpreter.Declare(cpp_code)
    ROOT.InitPTParamTables()

    rdf_def = rdf
    print(f"list(rdf_def.GetColumnNames()) = {list(rdf_def.GetColumnNames())}")
    for pname in PARAM_NAMES:
        if((pname in list(rdf_def.GetColumnNames())) or (f"{pname}_err" in list(rdf_def.GetColumnNames()))):
            rdf_def = rdf_def.Redefine(pname, f"Get_{pname}(Q2_y_Bin)").Redefine(f"{pname}_err", f"Get_{pname}_err(Q2_y_Bin)")
        else:
            rdf_def = rdf_def.Define(pname,   f"Get_{pname}(Q2_y_Bin)").Define(f"{pname}_err",   f"Get_{pname}_err(Q2_y_Bin)")
    rdf_def.Snapshot(tree_name, out_file)
    print(f"{color.BCYAN}attach_pT_params_to_rdf: wrote augmented tree '{tree_name}' to '{out_file}' with parameter columns added.{color.END}")


# ----------------------------------------------------------------------
# Q²-fits using only Q2_val, y_val, and parameter columns in the RDataFrame
# ----------------------------------------------------------------------
def perform_Q2_fits(rdf, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    # Fit each parameter (a0..c2) as a function of Q2 at fixed y, using only
    # the RDataFrame columns:
    #    Q2_val, y_val, a0..c2, a0_err..c2_err.
    # No use of Q2_y_Bin or pT_fit_results here: we just fix y and fit param(Q2).

    print(f"{color.BCYAN}Starting Q^{{2}}-fits of (z,pT) parameters at fixed y (from RDataFrame columns).{color.END}")

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BCYAN}Q^2-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    Q2_fit_summary = {}

    for y_center in y_Centers:
        # Narrow window around y_center; all y_val should be exact centers anyway.
        y_min = y_center - 1e-3
        y_max = y_center + 1e-3

        cut_expr = f"(y_val > {y_min}) && (y_val < {y_max})"
        df_y = rdf.Filter(cut_expr, f"Select rows with y≈{y_center:.2f}")

        needed_cols = ["Q2_val"] + PARAM_NAMES + [f"{p}_err" for p in PARAM_NAMES]
        np_dict = df_y.AsNumpy(needed_cols)

        if(("Q2_val" not in np_dict) or (len(np_dict["Q2_val"]) == 0)):
            print(f"{color.YELLOW}perform_Q2_fits: No entries found at y={y_center:.2f}; skipping this y bin.{color.END}")
            continue

        Q2_vals_all = numpy.array(np_dict["Q2_val"], dtype="float64")

        for pname in PARAM_NAMES:
            par_vals_all = numpy.array(np_dict[pname],       dtype="float64")
            par_errs_all = numpy.array(np_dict[f"{pname}_err"], dtype="float64")

            # Collapse many events per (Q2,y) down to one value per Q2:
            points_by_Q2 = {}
            for idx in range(len(Q2_vals_all)):
                q2  = float(Q2_vals_all[idx])
                val = float(par_vals_all[idx])
                err = float(par_errs_all[idx])

                if(q2 not in points_by_Q2):
                    points_by_Q2[q2] = [val, err]
                else:
                    # Sanity check: if we ever see mismatched values for same Q2,y, warn.
                    old_val, old_err = points_by_Q2[q2]
                    if((abs(old_val - val) > 1e-8) or (abs(old_err - err) > 1e-8)):
                        print(
                            f"{color.YELLOW}Warning: multiple values for param {pname} at "
                            f"Q2={q2:.3f}, y={y_center:.2f} differ slightly; using first.{color.END}"
                        )

            if(len(points_by_Q2) == 0):
                print(f"{color.YELLOW}perform_Q2_fits: No unique Q2 points for param={pname}, y={y_center:.2f}.{color.END}")
                continue

            Q2_unique = sorted(points_by_Q2.keys())
            n_points  = len(Q2_unique)

            x_vals = numpy.array(Q2_unique, dtype="float64")
            y_vals = numpy.array([points_by_Q2[q2][0] for q2 in Q2_unique], dtype="float64")
            y_errs = numpy.array([points_by_Q2[q2][1] for q2 in Q2_unique], dtype="float64")

            Linear = False
            if(n_points < 3):
                print(
                    f"{color.RED}Waring: {color.YELLOW}Param={pname}, y={y_center:.2f} only has {n_points} Q^2 points, "
                    f"need ≥3 for quadratic — using linear instead.{color.END}"
                )
                Linear = True

            x_min = float(min(x_vals))
            x_max = float(max(x_vals))

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(x_vals[idx]), float(y_vals[idx]))
                graph.SetPointError(idx, 0.0, float(y_errs[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            y_code = int(round(100.0 * y_center))  # e.g. 40, 50, 60, 70
            fname  = f"f_Q2_{pname}_y_{y_code:03d}"

            fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x", x_min, x_max)
            fit_func.SetParameter(0, float(numpy.mean(y_vals)))
            fit_func.SetParameter(1, 0.0)
            fit_func.SetParameter(2, 0.0)

            if(Linear):
                fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            q0     = fit_func.GetParameter(0)
            q0_err = fit_func.GetParError(0)
            q1     = fit_func.GetParameter(1)
            q1_err = fit_func.GetParError(1)
            q2     = fit_func.GetParameter(2)
            q2_err = fit_func.GetParError(2)
            chi2   = fit_func.GetChisquare()
            ndf    = fit_func.GetNDF()

            print(
                f"{color.BCYAN}Q^2-fit: param={pname}, y={y_center:.2f}: n={n_points}, "
                f"q0={q0:.4g}±{q0_err:.4g}, q1={q1:.4g}±{q1_err:.4g}, "
                f"q2={q2:.4g}±{q2_err:.4g}, chi2/ndf={chi2}/{ndf}{color.END}"
            )

            if(save_plots):
                cname = f"c_Q2Fit_{pname}_y_{y_code:03d}"
                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"{pname} vs Q^{{2}} (quadratic): y = {y_center:.2f}"
                graph.SetTitle(f"{title_str};Q^{{2}} (GeV^{{2}});{pname} parameter")
                graph.Draw("AP")

                fit_func.SetLineColor(ROOT.kRed)
                fit_func.SetLineWidth(2)
                fit_func.Draw("same")

                latex = ROOT.TLatex()
                latex.SetNDC(True)
                latex.SetTextSize(0.04)
                latex.DrawLatex(0.15, 0.88, f"q0 = {q0:.4g} #pm {q0_err:.4g}")
                latex.DrawLatex(0.15, 0.83, f"q1 = {q1:.4g} #pm {q1_err:.4g}")
                latex.DrawLatex(0.15, 0.78, f"q2 = {q2:.4g} #pm {q2_err:.4g}")
                latex.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

                base_name = f"{cname}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname
                out_name  = os.path.join(plot_dir, f"{base_name}{file_ext}")
                canvas.SaveAs(out_name)
                del canvas

            if(pname not in Q2_fit_summary):
                Q2_fit_summary[pname] = {}
            Q2_fit_summary[pname][y_center] = {
                "q0":       q0,
                "q0_err":   q0_err,
                "q1":       q1,
                "q1_err":   q1_err,
                "q2":       q2,
                "q2_err":   q2_err,
                "chi2":     chi2,
                "ndf":      ndf,
                "n_points": n_points,
                "Linear":   Linear,
            }

    total_combos = sum(len(v) for v in Q2_fit_summary.values())
    print(f"{color.BGREEN}Q^2-fits complete. Total (param,y) combinations fitted: {total_combos}.{color.END}")
    return Q2_fit_summary


# ----------------------------------------------------------------------
# NEW: y-fits of the Q² coefficients q0,q1,q2 vs y
# ----------------------------------------------------------------------
def perform_y_fits(Q2_fit_results, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    # Take the output of perform_Q2_fits:
    #   Q2_fit_results[pname][y_center] = {q0,q0_err,q1,q1_err,q2,q2_err,...}
    # For each pname in PARAM_NAMES and each coefficient (q0,q1,q2),
    # build qk(y) using the available y_center values and fit:
    #   qk(y) ≈ r0 + r1*y + r2*y^2
    # with a quadratic in y (or linear if <3 points).
    # That gives 27 y-fits total (9 pname × 3 coefficients).

    print(f"{color.BPINK}Starting y-fits of Q^{{2}} coefficients (q0,q1,q2) vs y.{color.END}")

    if((Q2_fit_results is None) or (len(Q2_fit_results) == 0)):
        print(f"{color.YELLOW}perform_y_fits: No Q2_fit_results provided; skipping y-fits.{color.END}")
        return {}

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BPINK}y-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    coeff_names = ["q0", "q1", "q2"]
    Y_fit_summary = {}

    for pname in PARAM_NAMES:
        if(pname not in Q2_fit_results):
            print(f"{color.YELLOW}perform_y_fits: pname={pname} not present in Q2_fit_results; skipping.{color.END}")
            continue

        # Dictionary: y_center → dict with q0,q1,q2,...
        y_dict = Q2_fit_results[pname]
        if(len(y_dict) == 0):
            print(f"{color.YELLOW}perform_y_fits: pname={pname} has no y entries; skipping.{color.END}")
            continue

        # Sort y values so plots are monotonic in x
        y_values_sorted = sorted(y_dict.keys())
        n_y = len(y_values_sorted)

        for coeff in coeff_names:
            y_points  = []
            val_points = []
            err_points = []

            for y_center in y_values_sorted:
                entry = y_dict[y_center]
                if((coeff not in entry) or (f"{coeff}_err" not in entry)):
                    print(f"{color.YELLOW}perform_y_fits: Missing {coeff} or {coeff}_err for param={pname}, y={y_center:.2f}; skipping that point.{color.END}")
                    continue

                y_points.append(float(y_center))
                val_points.append(float(entry[coeff]))
                err_points.append(float(entry[f"{coeff}_err"]))

            n_points = len(y_points)
            if(n_points == 0):
                print(f"{color.YELLOW}perform_y_fits: No valid points for (param={pname}, coeff={coeff}); skipping this y-fit.{color.END}")
                continue

            Linear = False
            if(n_points < 3):
                print(f"{color.RED}Waring: {color.YELLOW}y-fit for param={pname}, coeff={coeff} only has {n_points} points, need ≥3 for quadratic — using linear instead.{color.END}")
                Linear = True

            y_min = float(min(y_points))
            y_max = float(max(y_points))

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, y_points[idx], val_points[idx])
                graph.SetPointError(idx, 0.0, err_points[idx])

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            fname = f"f_y_{pname}_{coeff}"
            fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x", y_min, y_max)
            fit_func.SetParameter(0, float(numpy.mean(val_points)))
            fit_func.SetParameter(1, 0.0)
            fit_func.SetParameter(2, 0.0)

            if(Linear):
                fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            r0     = fit_func.GetParameter(0)
            r0_err = fit_func.GetParError(0)
            r1     = fit_func.GetParameter(1)
            r1_err = fit_func.GetParError(1)
            r2     = fit_func.GetParameter(2)
            r2_err = fit_func.GetParError(2)
            chi2   = fit_func.GetChisquare()
            ndf    = fit_func.GetNDF()

            print(
                f"{color.BPINK}y-fit: param={pname}, coeff={coeff}: n={n_points}, "
                f"r0={r0:.4g}±{r0_err:.4g}, r1={r1:.4g}±{r1_err:.4g}, "
                f"r2={r2:.4g}±{r2_err:.4g}, chi2/ndf={chi2}/{ndf}{color.END}"
            )

            if(save_plots):
                cname = f"c_YFit_{pname}_{coeff}"
                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"{coeff} of {pname} vs y (quadratic)"
                graph.SetTitle(f"{title_str};y;{coeff} coefficient of {pname}")
                graph.Draw("AP")

                fit_func.SetLineColor(ROOT.kRed)
                fit_func.SetLineWidth(2)
                fit_func.Draw("same")

                latex = ROOT.TLatex()
                latex.SetNDC(True)
                latex.SetTextSize(0.04)
                latex.DrawLatex(0.15, 0.88, f"r0 = {r0:.4g} #pm {r0_err:.4g}")
                latex.DrawLatex(0.15, 0.83, f"r1 = {r1:.4g} #pm {r1_err:.4g}")
                latex.DrawLatex(0.15, 0.78, f"r2 = {r2:.4g} #pm {r2_err:.4g}")
                latex.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

                if((image_suffix is not None) and (len(str(image_suffix)) > 0)):
                    base_name = f"{cname}_{image_suffix}"
                else:
                    base_name = cname

                out_name = os.path.join(plot_dir, f"{base_name}{file_ext}")
                canvas.SaveAs(out_name)
                del canvas

            if(pname not in Y_fit_summary):
                Y_fit_summary[pname] = {}
            if(coeff not in Y_fit_summary[pname]):
                Y_fit_summary[pname][coeff] = {}

            Y_fit_summary[pname][coeff] = {
                "r0":       r0,
                "r0_err":   r0_err,
                "r1":       r1,
                "r1_err":   r1_err,
                "r2":       r2,
                "r2_err":   r2_err,
                "chi2":     chi2,
                "ndf":      ndf,
                "n_points": n_points,
                "Linear":   Linear,
            }

    total_y_fits = sum(len(coeff_dict) for coeff_dict in Y_fit_summary.values())
    print(f"{color.BGREEN}y-fits complete. Total (param,coeff) combinations fitted: {total_y_fits}.{color.END}")
    return Y_fit_summary


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Build ratio histograms, build an RDataFrame, do quadratic z- and pT-fits, then fit parameters vs Q^2 and y.",
        formatter_class=RawDefaultsHelpFormatter
    )

    parser.add_argument("-r", "-inR", "--input_root",
                        default="Unfold_4D_Bins_Test_with_SF_FirstOrder_Almost_All.root",
                        help="Input ROOT file containing the TH1D histograms.\n")
    parser.add_argument("-nh", "--num_hist",
                        default="(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the numerator TH1D histogram in the input file.\n")
    parser.add_argument("-dh", "--den_hist",
                        default="(1D)_(gdf)_(SMEAR='')_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the denominator TH1D histogram in the input file.\n")
    parser.add_argument("-rh", "--ratio_hist", default=None,
                        help="Name to use (or look for) for the ratio TH1D histogram in the input file.")
    parser.add_argument("-rf", "--rdf_file",
                        default="Kinematic_4D_Unfolding.root",
                        help="Output ROOT file to store the RDataFrame with bin-by-bin values.")

    parser.add_argument("-fr", "--force_ratio", action="store_true",
                        help="Force recreation of the ratio histogram even if it already exists.")
    parser.add_argument("-frdf", "--force_rdf", action="store_true",
                        help="Force recreation of the RDataFrame file even if it already exists.")

    parser.add_argument("-noZ", "--no_z_fits", action="store_true",
                        help="Do NOT run bin_content vs z fits.")
    parser.add_argument("-noPT", "--no_pT_fits", action="store_true",
                        help="Do NOT run pT fits of z-fit parameters.")
    parser.add_argument("-noQ2", "--no_Q2_fits", action="store_true",
                        help="Do NOT run fits of parameters vs Q^2.")
    parser.add_argument("-noY", "--no_y_fits", action="store_true",
                        help="Do NOT run fits of Q^2 coefficients vs y.")
    parser.add_argument("-np", "--no_plots", action="store_true",
                        help="Do NOT save any fit plots (z, pT, Q^2, or y).")

    parser.add_argument("-zdir", "--z_plot_dir",
                        default="ZFit_Plots",
                        help="Output directory for all fit plots (z, pT, Q^2, y).")
    parser.add_argument("-n", "-tag", "--image_suffix", default=None, type=str,
                        help="Optional string appended to fit image filenames.")
    parser.add_argument("-fmt", "--image_format",
                        default="png", choices=["png", "pdf"],
                        help="Image file format for fit plots.")

    parser.add_argument("-e", "--email", action="store_true",
                        help="Send an email when the script finishes.")
    parser.add_argument("-ee", "--email_message", default=None, type=str,
                        help="Additional message to include in email.")

    args = parser.parse_args()
    return args


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    args = parse_arguments()

    if(args.ratio_hist is None):
        ratio_name = args.num_hist
        for options in ["(Bin)", "(Bayesian)", "(gdf)"]:
            ratio_name = ratio_name.replace(options, "(ratio)")
            if("(ratio)" in ratio_name):
                break
        if("(ratio)" not in ratio_name):
            print(f"{color.Error}Error in updating ratio_name = {color.END_B}'{ratio_name}'\n\t{color.Error}Appending {color.END_B}'_(ratio)'{color.Error} to the end of the name...{color.END}")
            ratio_name = f"{ratio_name}_(ratio)"
    else:
        ratio_name = args.ratio_hist

    do_z_fits  = (not args.no_z_fits)
    do_pT_fits = (not args.no_pT_fits)
    do_Q2_fits = (not args.no_Q2_fits)
    do_y_fits  = (not args.no_y_fits)
    save_plots = (not args.no_plots)
    file_ext   = "." + str(args.image_format).lower()

    if(save_plots):
        ROOT.gROOT.SetBatch(True)

    try:
        need_build_rdf = (not os.path.exists(args.rdf_file)) or args.force_rdf

        if(need_build_rdf):
            if(not os.path.exists(args.input_root)):
                raise RuntimeError(f"Input ROOT file '{args.input_root}' does not exist.")

            root_file = ROOT.TFile.Open(args.input_root, "UPDATE")
            if((root_file is None) or root_file.IsZombie()):
                raise RuntimeError(f"Failed to open input ROOT file '{args.input_root}' in UPDATE mode.")

            ratio_hist = build_ratio_histogram(root_file, args.num_hist, args.den_hist, ratio_name, args.force_ratio)

            root_file.Write("", ROOT.TObject.kOverwrite)
            root_file.Close()
            root_file = None

            rdf_build = build_dataframe_from_hist(ratio_hist)
            print(f"{color.BBLUE}Writing RDataFrame to file '{args.rdf_file}' as tree 'h22'.{color.END}")
            rdf_build.Snapshot("h22", args.rdf_file)
        else:
            msg = f"{color.BBLUE}RDataFrame file '{args.rdf_file}' already exists and --force_rdf was not set. Skipping RDataFrame rebuild.{color.END}"
            print(msg if(args.email_message is None) else f"{msg}\n\nUser message:\n{args.email_message}\n")

        if(not os.path.exists(args.rdf_file)):
            raise RuntimeError(f"RDataFrame file '{args.rdf_file}' does not exist even after attempted build.")

        z_fit_results   = None
        pT_fit_results  = None
        Q2_fit_results  = None
        Y_fit_results   = None

        if(do_z_fits):
            rdf_for_fits = ROOT.RDataFrame("h22", args.rdf_file)
            z_fit_results = perform_z_fits(rdf_for_fits, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)
            print(f"{color.BCYAN}Stored {len(z_fit_results)} z-fit result rows in memory (Python list).{color.END}")

        if(do_z_fits and do_pT_fits and (z_fit_results is not None) and (len(z_fit_results) > 0)):
            pT_fit_results = perform_pT_fits(z_fit_results, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)
            print(f"{color.BCYAN}Stored {len(pT_fit_results)} pT-fit (z,pT) descriptions in memory (by Q2_y_Bin).{color.END}")

            # Augment the RDataFrame with the pT-fit parameters as columns
            rdf_orig = ROOT.RDataFrame("h22", args.rdf_file)
            attach_pT_params_to_rdf(rdf_orig, pT_fit_results, args.rdf_file, tree_name="h22")

            if(do_Q2_fits):
                rdf_for_Q2 = ROOT.RDataFrame("h22", args.rdf_file)
                Q2_fit_results = perform_Q2_fits(rdf_for_Q2, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)

                if(do_y_fits and (Q2_fit_results is not None) and (len(Q2_fit_results) > 0)):
                    Y_fit_results = perform_y_fits(Q2_fit_results, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)

        email_body = f"{color.BGREEN}python_Unfold_4D_for_weights.py script completed successfully.{color.END}"
        email_body += f"\n\nInput ROOT file: {args.input_root}\n"
        email_body += f"Numerator hist:  {args.num_hist}\n"
        email_body += f"Denominator hist:{args.den_hist}\n"
        email_body += f"Ratio hist:      {ratio_name}\n"
        email_body += f"RDF file:        {args.rdf_file}\n"
        if(do_z_fits and (z_fit_results is not None)):
            email_body += f"z-fits in memory: {len(z_fit_results)} results (quadratic in z).\n"
        if(do_z_fits and do_pT_fits and (pT_fit_results is not None)):
            email_body += f"pT-fit functions (quadratic) per Q2_y_Bin: {len(pT_fit_results)}\n"
        if(do_z_fits and do_pT_fits and do_Q2_fits and (Q2_fit_results is not None)):
            total_Q2_combos = sum(len(v) for v in Q2_fit_results.values())
            email_body += f"Q^2-fit functions (quadratic) for (param,y) combinations: {total_Q2_combos}\n"
        if(do_z_fits and do_pT_fits and do_Q2_fits and do_y_fits and (Y_fit_results is not None)):
            total_Y_combos = sum(len(v) for v in Y_fit_results.values())
            email_body += f"y-fit functions (quadratic) for (param,coeff) combinations: {total_Y_combos}\n"
        if(save_plots):
            email_body += f"Fit image directory: {args.z_plot_dir}\n"
            email_body += f"Fit image format: {args.image_format}\n"
            if(args.image_suffix is not None):
                email_body += f"Image filename suffix: {args.image_suffix}\n"
        if(args.email_message is not None):
            email_body += f"\nUser message:\n{args.email_message}\n"
        print(email_body)
        if(args.email):
            send_email("python_Unfold_4D_for_weights.py Script Done", email_body)

    except Exception as e:
        email_body = f"\n{color.Error}ERROR in python_Unfold_4D_for_weights.py script:\n{color.END}{e}\n\n{traceback.format_exc()}\n"
        if(args.email_message is not None):
            email_body += f"\nUser message:\n{args.email_message}\n"
        print(email_body)
        if(args.email):
            send_email("python_Unfold_4D_for_weights.py Script Error", email_body)
        sys.exit(1)


if(__name__ == "__main__"):
    main()
    print("\nDone\n\n")
