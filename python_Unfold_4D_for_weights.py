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


# Parameters from pT-fits
PARAM_NAMES = ["a0", "a1", "a2",
               "b0", "b1", "b2",
               "c0", "c1", "c2"]

# Map Q^2 power index → letter (for names like Aaa2)
Q2_INDEX_LETTER = {
    3: "d",   # Q2^3
    2: "a",   # Q2^2
    1: "b",   # Q2^1
    0: "c",   # Q2^0
}

# Map original parameters (a0..c2) to (pT-letter, z-digit)
PARAM_Z_PTZ_MAP = {
    "c2": ("a", "2"),
    "c1": ("b", "2"),
    "c0": ("c", "2"),
    "a2": ("a", "1"),
    "a1": ("b", "1"),
    "a0": ("c", "1"),
    "b2": ("a", "0"),
    "b1": ("b", "0"),
    "b0": ("c", "0"),
}


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
    Q2_y_bins, z_pT_bins = Find_Q2_y_z_pT_Bin_Stats(
        Q2_y_Bin_Find       = Q2_y_Bin_Find_In,
        z_pT_Bin_Find       = z_pT_Bin_Find_In,
        List_Of_Histos_For_Stats_Search = "Use_Center",
        Smearing_Q          = "''",
        DataType            = "bbb",
        Binning_Method_Input= Binning_Method
    )
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
# Convert TH1D ratio histogram → RDataFrame with 8 columns
# (adds Q2_y_z_pT_4D_Bins for later 4D-bin tests)
# ----------------------------------------------------------------------
def build_dataframe_from_hist(ratio_hist):
    if(ratio_hist is None):
        raise RuntimeError("build_dataframe_from_hist: ratio_hist is None.")

    n_bins = ratio_hist.GetNbinsX()

    Q2_y_z_pT_4D_Bins_list = []
    Q2_y_Bin_list          = []
    Q2_val_list            = []
    y_val_list             = []
    z_val_list             = []
    pT_val_list            = []
    content_list           = []
    error_list             = []

    for ibin in range(1, n_bins + 1):
        Q2_y_z_pT_4D_Bins = int(ratio_hist.GetBinCenter(ibin))

        Q2_y_Bin, z_pT_Bin = decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins)
        if((Q2_y_Bin <= 0) or (z_pT_Bin <= 0)):
            continue

        bin_content = ratio_hist.GetBinContent(ibin)
        bin_error   = ratio_hist.GetBinError(ibin)

        Q2_val, y_val, z_val, pT_val = decode_kinematics_from_bins(Q2_y_Bin, z_pT_Bin)

        Q2_y_z_pT_4D_Bins_list.append(Q2_y_z_pT_4D_Bins)
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

    b_Q2_y_z_pT_4D_Bins = array.array("i", [0])
    b_Q2_y_Bin          = array.array("i", [0])
    b_Q2_val            = array.array("d", [0.0])
    b_y_val             = array.array("d", [0.0])
    b_z_val             = array.array("d", [0.0])
    b_pT_val            = array.array("d", [0.0])
    b_content           = array.array("d", [0.0])
    b_error             = array.array("d", [0.0])

    tree.Branch("Q2_y_z_pT_4D_Bins", b_Q2_y_z_pT_4D_Bins, "Q2_y_z_pT_4D_Bins/I")
    tree.Branch("Q2_y_Bin",          b_Q2_y_Bin,          "Q2_y_Bin/I")
    tree.Branch("Q2_val",            b_Q2_val,            "Q2_val/D")
    tree.Branch("y_val",             b_y_val,             "y_val/D")
    tree.Branch("z_val",             b_z_val,             "z_val/D")
    tree.Branch("pT_val",            b_pT_val,            "pT_val/D")
    tree.Branch("bin_content",       b_content,           "bin_content/D")
    tree.Branch("bin_error",         b_error,             "bin_error/D")

    for index in range(n_entries):
        b_Q2_y_z_pT_4D_Bins[0] = Q2_y_z_pT_4D_Bins_list[index]
        b_Q2_y_Bin[0]          = Q2_y_Bin_list[index]
        b_Q2_val[0]            = Q2_val_list[index]
        b_y_val[0]             = y_val_list[index]
        b_z_val[0]             = z_val_list[index]
        b_pT_val[0]            = pT_val_list[index]
        b_content[0]           = content_list[index]
        b_error[0]             = error_list[index]
        tree.Fill()

    memfile.Write()

    rdf = ROOT.RDataFrame(tree)
    rdf._unfold_memfile = memfile
    rdf._unfold_tree    = tree

    return rdf


# ----------------------------------------------------------------------
# Helper: check if RDF tree already has the needed 4D columns
# ----------------------------------------------------------------------
def rdf_tree_has_4D_columns(rdf_file, tree_name="h22"):
    if(not os.path.exists(rdf_file)):
        return False

    tfile = ROOT.TFile.Open(rdf_file, "READ")
    if((tfile is None) or tfile.IsZombie()):
        return False

    tree = tfile.Get(tree_name)
    if(tree is None):
        tfile.Close()
        return False

    branches = tree.GetListOfBranches()
    needed   = [
        "Q2_y_z_pT_4D_Bins",
        "Q2_y_Bin",
        "Q2_val",
        "y_val",
        "z_val",
        "pT_val",
        "bin_content",
        "bin_error"
    ]

    for name in needed:
        if(branches.FindObject(name) is None):
            tfile.Close()
            return False

    tfile.Close()
    return True


# ----------------------------------------------------------------------
# Z-fit layer: bin_content vs z at fixed (Q2_y_Bin, pT range)
# Polynomial in z (default quadratic, optional cubic)
# ----------------------------------------------------------------------
def perform_z_fits(rdf, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png", allow_cubic=False):
    print(f"{color.BCYAN}Starting z-fits using RDataFrame (polynomial in z, up to cubic).{color.END}")

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

            if((allow_cubic) and (n_points >= 4)):
                poly_order = 3
            elif(n_points >= 3):
                poly_order = 2
            else:
                poly_order = 1
                print(f"{color.RED}Warning: {color.YELLOW}Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min}, {pT_max}) has insufficient points for quadratic fit in z (n={n_points}) — using linear instead.{color.END}")

            Linear = (poly_order == 1)

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(z_vals[idx]), float(y_vals[idx]))
                graph.SetPointError(idx, 0.0, float(err_vals[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            z_min_fit = min([0.9*Z_MIN, Z_MIN])
            z_max_fit = max([1.1*Z_MAX, Z_MAX])

            intercept_guess = float(numpy.mean(y_vals))

            if(allow_cubic):
                fit_func = ROOT.TF1("f_z_tmp", "[0] + [1]*x + [2]*x*x + [3]*x*x*x", z_min_fit, z_max_fit)
                fit_func.SetParameter(0, intercept_guess)
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                fit_func.SetParameter(3, 0.0)
                if(poly_order < 3):
                    fit_func.FixParameter(3, 0.0)
                if(Linear):
                    fit_func.FixParameter(2, 0.0)
            else:
                fit_func = ROOT.TF1("f_z_tmp", "[0] + [1]*x + [2]*x*x", z_min_fit, z_max_fit)
                fit_func.SetParameter(0, intercept_guess)
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                if(Linear):
                    fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            intercept     = fit_func.GetParameter(0)
            intercept_err = fit_func.GetParError(0)
            slope         = fit_func.GetParameter(1)
            slope_err     = fit_func.GetParError(1)
            quad          = fit_func.GetParameter(2)
            quad_err      = fit_func.GetParError(2) if(not Linear) else 1e-4

            cubic     = 0.0
            cubic_err = 0.0
            if(allow_cubic):
                cubic     = fit_func.GetParameter(3)
                cubic_err = fit_func.GetParError(3) if(poly_order > 2) else 1e-4

            chi2      = fit_func.GetChisquare()
            ndf       = fit_func.GetNDF()
            pT_center = 0.5 * (pT_min + pT_max)

            poly_label = "linear"
            if(poly_order == 2):
                poly_label = "quadratic"
            elif(poly_order == 3):
                poly_label = "cubic"

            msg  = f"{color.BBLUE}z-fit ({poly_label}) Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min:.3f}, {pT_max:.3f}) "
            msg += f"n={n_points}, intercept={intercept:.4g} ± {intercept_err:.4g}, "
            msg += f"slope={slope:.4g} ± {slope_err:.4g}, quad={quad:.4g} ± {quad_err:.4g}"
            if(allow_cubic):
                msg += f", cubic={cubic:.4g} ± {cubic_err:.4g}"
            msg += f", chi2/ndf={chi2}/{ndf}{color.END}"
            print(msg)

            if(save_plots):
                pT_center_code = int(round(1000.0 * pT_center))
                cname = f"c_zFit_Q2_y_Bin_{Q2_y_Bin_key}_pT_{pT_center_code:03d}"

                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"z-fit ({poly_label}): Q^{{2}}-y Bin = {Q2_y_Bin_key} #topbar P_{{T}} = [{pT_min:.2f},{pT_max:.2f})"
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
                if(allow_cubic):
                    latex.DrawLatex(0.15, 0.73, f"cubic     = {cubic:.4g} #pm {cubic_err:.4g}")
                    latex.DrawLatex(0.15, 0.68, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")
                else:
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
                "cubic":         cubic,
                "cubic_err":     cubic_err,
                "chi2":          chi2,
                "ndf":           ndf,
                "poly_order":    poly_order,
                "Linear":        Linear,
            })

    print(f"{color.BGREEN}z-fits complete. Total successful fits: {len(results)}.{color.END}")
    return results


# ----------------------------------------------------------------------
# pT-fits: intercept(pT), slope(pT), quad(pT) → 9 parameters per Q2_y_Bin
# Polynomial in pT (default quadratic, optional cubic)
# ----------------------------------------------------------------------
def perform_pT_fits(z_fit_results, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png", allow_cubic=False):
    print(f"{color.BPURPLE}Starting pT-fits of z-fit parameters (polynomial in pT, up to cubic).{color.END}")

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
        n    = len(rows)

        if(n < 2):
            print(f"{color.YELLOW}perform_pT_fits: Q2_y_Bin={Q2_y_Bin_key} only has {n} pT points; skipping pT fits for this bin.{color.END}")
            continue

        if((allow_cubic) and (n >= 4)):
            poly_order = 3
        elif(n >= 3):
            poly_order = 2
        else:
            poly_order = 1
            print(f"{color.RED}Warning: {color.YELLOW}Q2_y_Bin={Q2_y_Bin_key} only has {n} z-fit points, need ≥3 for quadratic — using linear instead.{color.END}")

        Linear = (poly_order == 1)

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

        if(allow_cubic):
            f_slope = ROOT.TF1(f"f_slope_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x + [3]*x*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
            f_slope.SetParameter(0, float(numpy.mean(slopes)))
            f_slope.SetParameter(1, 0.0)
            f_slope.SetParameter(2, 0.0)
            f_slope.SetParameter(3, 0.0)
            if(poly_order < 3):
                f_slope.FixParameter(3, 0.0)
            if(Linear):
                f_slope.FixParameter(2, 0.0)
        else:
            f_slope = ROOT.TF1(f"f_slope_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
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
        a2_err = f_slope.GetParError(2) if(not Linear) else 1e-4
        a3     = 0.0
        a3_err = 0.0
        if(allow_cubic):
            a3     = f_slope.GetParameter(3)
            a3_err = f_slope.GetParError(3) if(poly_order > 2) else 1e-4
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

        if(allow_cubic):
            f_int = ROOT.TF1(f"f_int_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x + [3]*x*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
            f_int.SetParameter(0, float(numpy.mean(intercepts)))
            f_int.SetParameter(1, 0.0)
            f_int.SetParameter(2, 0.0)
            f_int.SetParameter(3, 0.0)
            if(poly_order < 3):
                f_int.FixParameter(3, 0.0)
            if(Linear):
                f_int.FixParameter(2, 0.0)
        else:
            f_int = ROOT.TF1(f"f_int_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
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
        b2_err = f_int.GetParError(2) if(not Linear) else 1e-4
        b3     = 0.0
        b3_err = 0.0
        if(allow_cubic):
            b3     = f_int.GetParameter(3)
            b3_err = f_int.GetParError(3) if(poly_order > 2) else 1e-4
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

        if(allow_cubic):
            f_quad = ROOT.TF1(f"f_quad_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x + [3]*x*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
            f_quad.SetParameter(0, float(numpy.mean(quads)))
            f_quad.SetParameter(1, 0.0)
            f_quad.SetParameter(2, 0.0)
            f_quad.SetParameter(3, 0.0)
            if(poly_order < 3):
                f_quad.FixParameter(3, 0.0)
            if(Linear):
                f_quad.FixParameter(2, 0.0)
        else:
            f_quad = ROOT.TF1(f"f_quad_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x + [2]*x*x", min([0.9*pT_min_fit, pT_min_fit]), max([1.1*pT_max_fit, pT_max_fit]))
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
        c2_err = f_quad.GetParError(2) if(not Linear) else 1e-4
        c3     = 0.0
        c3_err = 0.0
        if(allow_cubic):
            c3     = f_quad.GetParameter(3)
            c3_err = f_quad.GetParError(3) if(poly_order > 2) else 1e-4
        chi2_q = f_quad.GetChisquare()
        ndf_q  = f_quad.GetNDF()

        poly_label = "linear"
        if(poly_order == 2):
            poly_label = "quadratic"
        elif(poly_order == 3):
            poly_label = "cubic"

        print(f"{color.BPURPLE}Q2_y_Bin={Q2_y_Bin_key} (pT-fit {poly_label}):")
        line_s = f"  slope(pT)     = a0 + a1*pT + a2*pT^2"
        if(allow_cubic):
            line_s += " + a3*pT^3"
        line_s += f" with a0={a0:.4g}±{a0_err:.4g}, a1={a1:.4g}±{a1_err:.4g}, a2={a2:.4g}±{a2_err:.4g}"
        if(allow_cubic):
            line_s += f", a3={a3:.4g}±{a3_err:.4g}"
        line_s += f", chi2/ndf={chi2_s}/{ndf_s}"
        print(line_s)

        line_i = f"  intercept(pT) = b0 + b1*pT + b2*pT^2"
        if(allow_cubic):
            line_i += " + b3*pT^3"
        line_i += f" with b0={b0:.4g}±{b0_err:.4g}, b1={b1:.4g}±{b1_err:.4g}, b2={b2:.4g}±{b2_err:.4g}"
        if(allow_cubic):
            line_i += f", b3={b3:.4g}±{b3_err:.4g}"
        line_i += f", chi2/ndf={chi2_i}/{ndf_i}"
        print(line_i)

        line_q = f"  quad(pT)      = c0 + c1*pT + c2*pT^2"
        if(allow_cubic):
            line_q += " + c3*pT^3"
        line_q += (f" with c0={c0:.4g}±{c0_err:.4g}, c1={c1:.4g}±{c1_err:.4g}, "
                   f"c2={c2:.4g}±{c2_err:.4g}")
        if(allow_cubic):
            line_q += f", c3={c3:.4g}±{c3_err:.4g}"
        line_q += f", chi2/ndf={chi2_q}/{ndf_q}{color.END}"
        print(line_q)

        if(save_plots):
            # Slope vs pT plot
            cname_slope = f"c_pTFit_slope_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_s = ROOT.TCanvas(cname_slope, cname_slope, 800, 600)
            title_s  = f"Slope vs P_{{T}} ({poly_label}): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
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
            if(allow_cubic):
                latex_s.DrawLatex(0.15, 0.73, f"a3 = {a3:.4g} #pm {a3_err:.4g}")
                latex_s.DrawLatex(0.15, 0.68, f"#chi^{{2}}/ndf = {chi2_s:.1f} / {ndf_s}")
            else:
                latex_s.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2_s:.1f} / {ndf_s}")

            base_s = f"{cname_slope}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname_slope
            out_s = os.path.join(plot_dir, f"{base_s}{file_ext}")
            canvas_s.SaveAs(out_s)
            del canvas_s

            # Intercept vs pT plot
            cname_i = f"c_pTFit_intercept_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_i = ROOT.TCanvas(cname_i, cname_i, 800, 600)
            title_i  = f"Intercept vs P_{{T}} ({poly_label}): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
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
            if(allow_cubic):
                latex_i.DrawLatex(0.15, 0.73, f"b3 = {b3:.4g} #pm {b3_err:.4g}")
                latex_i.DrawLatex(0.15, 0.68, f"#chi^{{2}}/ndf = {chi2_i:.1f} / {ndf_i}")
            else:
                latex_i.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2_i:.1f} / {ndf_i}")

            base_i = f"{cname_i}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname_i
            out_i = os.path.join(plot_dir, f"{base_i}{file_ext}")
            canvas_i.SaveAs(out_i)
            del canvas_i

            # Quad vs pT plot
            cname_q = f"c_pTFit_quad_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_q = ROOT.TCanvas(cname_q, cname_q, 800, 600)
            title_q  = f"Quad coeff vs P_{{T}} ({poly_label}): Q^{{2}}-y Bin = {Q2_y_Bin_key}"
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
            if(allow_cubic):
                latex_q.DrawLatex(0.15, 0.73, f"c3 = {c3:.4g} #pm {c3_err:.4g}")
                latex_q.DrawLatex(0.15, 0.68, f"#chi^{{2}}/ndf = {chi2_q:.1f} / {ndf_q}")
            else:
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
            "poly_order": poly_order,
        }

        if(allow_cubic):
            pt_fit_summary[Q2_y_Bin_key]["a3"]     = a3
            pt_fit_summary[Q2_y_Bin_key]["a3_err"] = a3_err
            pt_fit_summary[Q2_y_Bin_key]["b3"]     = b3
            pt_fit_summary[Q2_y_Bin_key]["b3_err"] = b3_err
            pt_fit_summary[Q2_y_Bin_key]["c3"]     = c3
            pt_fit_summary[Q2_y_Bin_key]["c3_err"] = c3_err

    print(f"{color.BGREEN}pT-fits complete. Total Q2_y_Bins with 9-parameter (z,pT) description: {len(pt_fit_summary)}.{color.END}")
    return pt_fit_summary


# ----------------------------------------------------------------------
# Attach pT-fit parameters as columns in the RDataFrame (by Q2_y_Bin)
# ----------------------------------------------------------------------
def attach_pT_params_to_rdf(rdf, pt_fit_summary, out_file, tree_name="h22"):

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
def perform_Q2_fits(rdf, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png", allow_cubic=False):

    print(f"{color.BCYAN}Starting Q^{{2}}-fits of (z,pT) parameters at fixed y (from RDataFrame columns).{color.END}")

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BCYAN}Q^2-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    Q2_fit_summary = {}

    for y_center in y_Centers:
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
            par_vals_all = numpy.array(np_dict[pname],          dtype="float64")
            par_errs_all = numpy.array(np_dict[f"{pname}_err"], dtype="float64")

            points_by_Q2 = {}
            for idx in range(len(Q2_vals_all)):
                q2  = float(Q2_vals_all[idx])
                val = float(par_vals_all[idx])
                err = float(par_errs_all[idx])

                if(q2 not in points_by_Q2):
                    points_by_Q2[q2] = [val, err]
                else:
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

            # Decide polynomial order
            if((allow_cubic) and (n_points >= 4)):
                poly_order = 3
            elif(n_points >= 3):
                poly_order = 2
            elif(n_points >= 2):
                poly_order = 1
                print(f"\n{color.RED}Warning: {color.YELLOW}Param={pname}, y={y_center:.2f} only has {n_points} Q^2 points, need ≥3 for quadratic — using linear instead.{color.END}\n")
            else:
                print(f"{color.YELLOW}perform_Q2_fits: Param={pname}, y={y_center:.2f} has only {n_points} Q^2 point(s); skipping this fit.{color.END}")
                continue

            y_code = int(round(100.0 * y_center))
            fname  = f"f_Q2_{pname}_y_{y_code:03d}"

            Linear = (poly_order < 2)

            x_min = float(min(x_vals))
            x_max = float(max(x_vals))

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(x_vals[idx]), float(y_vals[idx]))
                graph.SetPointError(idx, 0.0, float(y_errs[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            # Fit function: cubic allowed, otherwise quadratic/linear
            if(allow_cubic):
                fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x + [3]*x*x*x", min([0.9*x_min, x_min]), max([1.1*x_max, x_max]))
                fit_func.SetParameter(0, float(numpy.mean(y_vals)))
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                fit_func.SetParameter(3, 0.0)
                if(poly_order < 3):
                    fit_func.FixParameter(3, 0.0)
                if(Linear):
                    fit_func.FixParameter(2, 0.0)
            else:
                fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x", min([0.9*x_min, x_min]), max([1.1*x_max, x_max]))
                fit_func.SetParameter(0, float(numpy.mean(y_vals)))
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                if(poly_order == 1):
                    fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            q0     = fit_func.GetParameter(0)
            q0_err = fit_func.GetParError(0)
            q1     = fit_func.GetParameter(1)
            q1_err = fit_func.GetParError(1)
            q2     = fit_func.GetParameter(2)
            q2_err = fit_func.GetParError(2) if(not Linear) else 1e-4
            q3     = 0.0
            q3_err = 0.0
            if(allow_cubic):
                q3     = fit_func.GetParameter(3)
                q3_err = fit_func.GetParError(3) if(poly_order > 2) else 1e-4
            chi2   = fit_func.GetChisquare()
            ndf    = fit_func.GetNDF()

            poly_label = "linear"
            if(poly_order == 2):
                poly_label = "quadratic"
            elif(poly_order == 3):
                poly_label = "cubic"

            msg  = f"{color.BCYAN}Q^2-fit ({poly_label}): param={pname}, y={y_center:.2f}: n={n_points}, "
            msg += f"q0={q0:.4g}±{q0_err:.4g}, q1={q1:.4g}±{q1_err:.4g}, q2={q2:.4g}±{q2_err:.4g}"
            if(allow_cubic):
                msg += f", q3={q3:.4g}±{q3_err:.4g}"
            msg += f", chi2/ndf={chi2}/{ndf}{color.END}"
            print(msg)

            if(save_plots):
                cname = f"c_Q2Fit_{pname}_y_{y_code:03d}"
                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"{pname} vs Q^{{2}} ({poly_label}): y = {y_center:.2f}"
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
                if(allow_cubic):
                    latex.DrawLatex(0.15, 0.73, f"q3 = {q3:.4g} #pm {q3_err:.4g}")
                    latex.DrawLatex(0.15, 0.68, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")
                else:
                    latex.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

                base_name = f"{cname}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname
                out_name  = os.path.join(plot_dir, f"{base_name}{file_ext}")
                canvas.SaveAs(out_name)
                del canvas

            if(pname not in Q2_fit_summary):
                Q2_fit_summary[pname] = {}

            entry = {
                "q0":         q0,
                "q0_err":     q0_err,
                "q1":         q1,
                "q1_err":     q1_err,
                "q2":         q2,
                "q2_err":     q2_err,
                "chi2":       chi2,
                "ndf":        ndf,
                "n_points":   n_points,
                "poly_order": poly_order,
                "Linear":     (poly_order == 1),
            }
            if(allow_cubic):
                entry["q3"]     = q3
                entry["q3_err"] = q3_err

            Q2_fit_summary[pname][y_center] = entry

    total_combos = sum(len(v) for v in Q2_fit_summary.values())
    print(f"{color.BGREEN}Q^2-fits complete. Total (param,y) combinations fitted: {total_combos}.{color.END}")
    return Q2_fit_summary


# ----------------------------------------------------------------------
# y-fits of the Q² coefficients q0,q1,q2 vs y
# Produces A,B,C for each (param, Q2-power)
# Polynomial in y (default quadratic, optional cubic fit)
# ----------------------------------------------------------------------
def perform_y_fits(Q2_fit_results, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png", allow_cubic=False):
    print(f"{color.BPINK}Starting y-fits of Q^{{2}} coefficients q_{{i}} vs y.{color.END}")

    if((Q2_fit_results is None) or (len(Q2_fit_results) == 0)):
        print(f"{color.YELLOW}perform_y_fits: No Q2_fit_results provided; skipping y-fits.{color.END}")
        return {}

    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)
        print(f"{color.BPINK}y-fit plots will be saved in directory '{plot_dir}' with extension '{file_ext}'.{color.END}")

    y_fit_results = {}

    for pname in PARAM_NAMES:
        if(pname not in Q2_fit_results):
            print(f"{color.YELLOW}perform_y_fits: pname={pname} not present in Q2_fit_results; skipping.{color.END}")
            continue

        by_y = Q2_fit_results[pname]
        if(len(by_y) == 0):
            print(f"{color.YELLOW}perform_y_fits: pname={pname} has no y entries; skipping.{color.END}")
            continue

        y_list = sorted(by_y.keys())

        for q_index in [0, 1, 2, 3]:
            q_key     = f"q{q_index}"
            q_err_key = f"{q_key}_err"

            y_vals   = []
            val_vals = []
            err_vals = []

            for y_center in y_list:
                entry = by_y[y_center]
                if((q_key not in entry) or (q_err_key not in entry)):
                    # This is expected if we didn't do cubic, or this q_index wasn't fitted
                    continue
                y_vals.append(float(y_center))
                val_vals.append(float(entry[q_key]))
                err_vals.append(float(entry[q_err_key]))

            n_points = len(y_vals)
            if(n_points == 0):
                print(f"{color.YELLOW}perform_y_fits: No valid y points for (param={pname}, q_index={q_index}); skipping this y-fit.{color.END}")
                continue

            arr_y   = numpy.array(y_vals,   dtype="float64")
            arr_v   = numpy.array(val_vals, dtype="float64")
            arr_err = numpy.array(err_vals, dtype="float64")

            if((allow_cubic) and (n_points >= 4)):
                poly_order = 3
            elif(n_points >= 3):
                poly_order = 2
            elif(n_points >= 2):
                poly_order = 1
                print(f"\n{color.RED}Warning: {color.YELLOW}y-fit for param={pname}, q_index={q_index} only has {n_points} points, need >3 for quadratic — using linear instead.{color.END}\n")
            else:
                print(f"{color.YELLOW}perform_y_fits: y-fit for param={pname}, q_index={q_index} only has {n_points} point(s); skipping.{color.END}")
                continue

            Linear = (poly_order == 1)

            y_min = float(min(arr_y))
            y_max = float(max(arr_y))

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(arr_y[idx]), float(arr_v[idx]))
                graph.SetPointError(idx, 0.0, float(arr_err[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            fname = f"f_y_{pname}_q{q_index}"

            if(allow_cubic):
                fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x + [3]*x*x*x", min([0.9*y_min, y_min]), max([1.1*y_max, y_max]))
                fit_func.SetParameter(0, float(numpy.mean(arr_v)))
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                fit_func.SetParameter(3, 0.0)
                if(poly_order < 3):
                    fit_func.FixParameter(3, 0.0)
                if(Linear):
                    fit_func.FixParameter(2, 0.0)
            else:
                fit_func = ROOT.TF1(fname, "[0] + [1]*x + [2]*x*x", min([0.9*y_min, y_min]), max([1.1*y_max, y_max]))
                fit_func.SetParameter(0, float(numpy.mean(arr_v)))
                fit_func.SetParameter(1, 0.0)
                fit_func.SetParameter(2, 0.0)
                if(Linear):
                    fit_func.FixParameter(2, 0.0)

            fit_result = graph.Fit(fit_func, "QSRNB")

            C_val = fit_func.GetParameter(0)
            C_err = fit_func.GetParError(0)
            B_val = fit_func.GetParameter(1)
            B_err = fit_func.GetParError(1)
            A_val = fit_func.GetParameter(2)
            A_err = fit_func.GetParError(2) if(not Linear) else 1e-4

            D_val = 0.0
            D_err = 0.0
            if(allow_cubic):
                D_val = fit_func.GetParameter(3)
                D_err = fit_func.GetParError(3) if(poly_order > 2) else 1e-4

            chi2  = fit_func.GetChisquare()
            ndf   = fit_func.GetNDF()

            poly_label = "linear"
            if(poly_order == 2):
                poly_label = "quadratic"
            elif(poly_order == 3):
                poly_label = "cubic"

            print(
                f"{color.BPINK}y-fit ({poly_label}): param={pname}, q_index={q_index}: n={n_points}, "
                f"A={A_val:.4g}±{A_err:.4g}, B={B_val:.4g}±{B_err:.4g}, "
                f"C={C_val:.4g}±{C_err:.4g}, chi2/ndf={chi2}/{ndf}{color.END}"
            )

            if(save_plots):
                if(q_index in Q2_INDEX_LETTER):
                    q_letter = Q2_INDEX_LETTER[q_index]
                else:
                    q_letter = "?"
                cname = f"c_yFit_{pname}_q{q_index}"
                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"{pname}, q{q_index} vs y ({poly_label}): Q^{{2}}-coefficient ({q_letter})"
                graph.SetTitle(f"{title_str};y;{pname}, q{q_index} coefficient")
                graph.Draw("AP")

                fit_func.SetLineColor(ROOT.kRed)
                fit_func.SetLineWidth(2)
                fit_func.Draw("same")

                latex = ROOT.TLatex()
                latex.SetNDC(True)
                latex.SetTextSize(0.04)
                latex.DrawLatex(0.15, 0.88, f"A = {A_val:.4g} #pm {A_err:.4g}")
                latex.DrawLatex(0.15, 0.83, f"B = {B_val:.4g} #pm {B_err:.4g}")
                latex.DrawLatex(0.15, 0.78, f"C = {C_val:.4g} #pm {C_err:.4g}")
                latex.DrawLatex(0.15, 0.73, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

                base_name = f"{cname}_{image_suffix}" if((image_suffix is not None) and (len(str(image_suffix)) > 0)) else cname
                out_name  = os.path.join(plot_dir, f"{base_name}{file_ext}")
                canvas.SaveAs(out_name)
                del canvas

            if(pname not in y_fit_results):
                y_fit_results[pname] = {}
            y_fit_results[pname][q_index] = {
                "A":        A_val,
                "A_err":    A_err,
                "B":        B_val,
                "B_err":    B_err,
                "C":        C_val,
                "C_err":    C_err,
                "chi2":     chi2,
                "ndf":      ndf,
                "n_points": n_points,
                "Linear":   Linear,
                "poly_order": poly_order,
            }

            if(allow_cubic):
                y_fit_results[pname][q_index]["D"]     = D_val
                y_fit_results[pname][q_index]["D_err"] = D_err

    total_y_fits = sum(len(v) for v in y_fit_results.values())
    print(f"{color.BGREEN}y-fits complete. Total (param,q_index) combinations fitted: {total_y_fits}.{color.END}")
    return y_fit_results


# ----------------------------------------------------------------------
# Build the final A.. / B.. / C.. coefficient maps from y_fits
# (still useful for symbolic printout)
# ----------------------------------------------------------------------
def build_final_coefficients(y_fit_results):
    coeff_map     = {}
    coeff_err_map = {}
    meta_map      = {}

    for pname, (pT_letter, z_digit) in PARAM_Z_PTZ_MAP.items():
        if(pname not in y_fit_results):
            print(f"{color.YELLOW}build_final_coefficients: No y-fit results for param '{pname}'. Coefficients set to 0.{color.END}")
            param_y_fits = {}
        else:
            param_y_fits = y_fit_results[pname]

        for q_index in sorted(Q2_INDEX_LETTER.keys(), reverse=True):
            q_letter = Q2_INDEX_LETTER[q_index]
            entry    = param_y_fits.get(q_index, None)

            if(entry is None):
                A_val = 0.0
                B_val = 0.0
                C_val = 0.0
                A_err = 0.0
                B_err = 0.0
                C_err = 0.0
                print(
                    f"{color.YELLOW}build_final_coefficients: Missing y-fit for param='{pname}', q_index={q_index}; "
                    f"setting A,B,C to 0.{color.END}"
                )
            else:
                A_val = entry["A"]
                A_err = entry["A_err"]
                B_val = entry["B"]
                B_err = entry["B_err"]
                C_val = entry["C"]
                C_err = entry["C_err"]

            nameA = f"A{q_letter}{pT_letter}{z_digit}"
            nameB = f"B{q_letter}{pT_letter}{z_digit}"
            nameC = f"C{q_letter}{pT_letter}{z_digit}"

            coeff_map[nameA]     = A_val
            coeff_err_map[nameA] = A_err
            meta_map[nameA]      = {
                "param":     pname,
                "Q2_power":  q_index,
                "y_power":   2,
                "pT_letter": pT_letter,
                "z_power":   int(z_digit),
            }

            coeff_map[nameB]     = B_val
            coeff_err_map[nameB] = B_err
            meta_map[nameB]      = {
                "param":     pname,
                "Q2_power":  q_index,
                "y_power":   1,
                "pT_letter": pT_letter,
                "z_power":   int(z_digit),
            }

            coeff_map[nameC]     = C_val
            coeff_err_map[nameC] = C_err
            meta_map[nameC]      = {
                "param":     pname,
                "Q2_power":  q_index,
                "y_power":   0,
                "pT_letter": pT_letter,
                "z_power":   int(z_digit),
            }

    print(f"{color.BGREEN}build_final_coefficients: constructed {len(coeff_map)} final coefficients (A/B/C with aa2-style names).{color.END}")
    return coeff_map, coeff_err_map, meta_map


# ----------------------------------------------------------------------
# Print the final 4D function F(y,Q2,pT,z) and coefficient table
# ----------------------------------------------------------------------
def print_final_4D_function(y_fit_results):
    coeff_map, coeff_err_map, meta_map = build_final_coefficients(y_fit_results)

    Z_GROUPS = {
        "2": ["c2", "c1", "c0"],
        "1": ["a2", "a1", "a0"],
        "0": ["b2", "b1", "b0"],
    }

    def y_poly_str(q_letter, pT_letter, z_digit):
        return f"(A{q_letter}{pT_letter}{z_digit}*y_val*y_val + B{q_letter}{pT_letter}{z_digit}*y_val + C{q_letter}{pT_letter}{z_digit})"

    z_terms = []

    for z_digit in ["2", "1", "0"]:
        pT_terms = []

        for pname in Z_GROUPS[z_digit]:
            pT_letter, _z = PARAM_Z_PTZ_MAP[pname]

            q2_terms = []
            for q_index in sorted(Q2_INDEX_LETTER.keys(), reverse=True):
                q_letter = Q2_INDEX_LETTER[q_index]
                y_poly   = y_poly_str(q_letter, pT_letter, z_digit)
                if(q_index == 3):
                    q2_terms.append(f"{y_poly}*Q2_val*Q2_val*Q2_val")
                elif(q_index == 2):
                    q2_terms.append(f"{y_poly}*Q2_val*Q2_val")
                elif(q_index == 1):
                    q2_terms.append(f"{y_poly}*Q2_val")
                else:
                    q2_terms.append(f"{y_poly}")

            Q2_block = "(" + " + ".join(q2_terms) + ")"

            if(pname.endswith("2")):
                pT_factor = "*pT_val*pT_val"
            elif(pname.endswith("1")):
                pT_factor = "*pT_val"
            else:
                pT_factor = ""

            pT_terms.append(f"{Q2_block}{pT_factor}")

        pT_block = "(" + " + ".join(pT_terms) + ")"

        if(z_digit == "2"):
            z_terms.append(f"{pT_block}*z_val*z_val")
        elif(z_digit == "1"):
            z_terms.append(f"{pT_block}*z_val")
        else:
            z_terms.append(f"{pT_block}")

    print(f"\n{color.BCYAN}Symbolic final 4D function in terms of fitted coefficients:{color.END}")
    print("F(y_val, Q2_val, pT_val, z_val) =")
    email_output = "Symbolic final 4D function in terms of fitted coefficients:\n"
    email_output += "F(y_val, Q2_val, pT_val, z_val) =\n"

    for idx, term in enumerate(z_terms):
        prefix = "  " if(idx == 0) else "  + "
        print(prefix + term)
        email_output = f"{email_output}{prefix + term}\n"

    print(f"\n{color.BCYAN}Final 4D-coefficient values (name = value ± error):{color.END}")
    email_output += "\nFinal 4D-coefficient values (name = value ± error):\n"
    for name in sorted(coeff_map.keys()):
        val  = coeff_map[name]
        err  = coeff_err_map[name]
        meta = meta_map[name]
        line = (
            f"  {name:4s} = {val:.6g} ± {err:.6g}   "
            f"(from param '{meta['param']}', Q2^{meta['Q2_power']}, "
            f"pT index '{meta['pT_letter']}', z^{meta['z_power']})"
        )
        print(line)
        email_output = f"{email_output}{line}\n"

    return coeff_map, coeff_err_map, meta_map, email_output


# ----------------------------------------------------------------------
# Declare C++ implementation of the final F(y,Q2,pT,z) using A/B/C
# ----------------------------------------------------------------------
def declare_final_F_function(y_fit_results):
    # Map param name → index in arrays
    param_index_map = {}
    for idx, pname in enumerate(PARAM_NAMES):
        param_index_map[pname] = idx

    cpp_lines = []
    cpp_lines.append("#include <cmath>")
    cpp_lines.append("struct Final4DParams {")
    cpp_lines.append("  static const int NPAR = 9;")
    cpp_lines.append("  static const int NQ   = 4;  // allow Q2^0..Q2^3")
    cpp_lines.append("  static double A[NPAR][NQ];")
    cpp_lines.append("  static double B[NPAR][NQ];")
    cpp_lines.append("  static double C[NPAR][NQ];")
    cpp_lines.append("};")
    cpp_lines.append("double Final4DParams::A[Final4DParams::NPAR][Final4DParams::NQ] = {{0.0}};")
    cpp_lines.append("double Final4DParams::B[Final4DParams::NPAR][Final4DParams::NQ] = {{0.0}};")
    cpp_lines.append("double Final4DParams::C[Final4DParams::NPAR][Final4DParams::NQ] = {{0.0}};")

    cpp_lines.append("void InitFinal4DParams(){")
    for pname in PARAM_NAMES:
        p_index = param_index_map[pname]
        if(pname not in y_fit_results):
            continue
        param_y_fits = y_fit_results[pname]
        for q_index in [0, 1, 2, 3]:
            entry = param_y_fits.get(q_index, None)
            if(entry is None):
                A_val = 0.0
                B_val = 0.0
                C_val = 0.0
            else:
                A_val = float(entry["A"])
                B_val = float(entry["B"])
                C_val = float(entry["C"])
            cpp_lines.append(f"  Final4DParams::A[{p_index}][{q_index}] = {A_val};")
            cpp_lines.append(f"  Final4DParams::B[{p_index}][{q_index}] = {B_val};")
            cpp_lines.append(f"  Final4DParams::C[{p_index}][{q_index}] = {C_val};")
    cpp_lines.append("}")

    cpp_lines.append(
        "double EvalFinalParam(int pIndex, double y, double Q2){\n"
        "  if(pIndex < 0 || pIndex >= Final4DParams::NPAR) return 0.0;\n"
        "  double result = 0.0;\n"
        "  for(int q = 0; q < Final4DParams::NQ; ++q){\n"
        "    double A = Final4DParams::A[pIndex][q];\n"
        "    double B = Final4DParams::B[pIndex][q];\n"
        "    double C = Final4DParams::C[pIndex][q];\n"
        "    double y_poly = A*y*y + B*y + C;\n"
        "    double Q2_pow = 1.0;\n"
        "    if(q == 1)      Q2_pow = Q2;\n"
        "    else if(q == 2) Q2_pow = Q2*Q2;\n"
        "    else if(q == 3) Q2_pow = Q2*Q2*Q2;\n"
        "    result += y_poly * Q2_pow;\n"
        "  }\n"
        "  return result;\n"
        "}\n"
    )

    # Param indices: a0..c2 (must match PARAM_NAMES order)
    cpp_lines.append(
        "double F_4D_eval(double y_val, double Q2_val, double pT_val, double z_val){\n"
        "  // PARAM_NAMES = [a0,a1,a2,b0,b1,b2,c0,c1,c2]\n"
        "  double a0 = EvalFinalParam(0, y_val, Q2_val);\n"
        "  double a1 = EvalFinalParam(1, y_val, Q2_val);\n"
        "  double a2 = EvalFinalParam(2, y_val, Q2_val);\n"
        "  double b0 = EvalFinalParam(3, y_val, Q2_val);\n"
        "  double b1 = EvalFinalParam(4, y_val, Q2_val);\n"
        "  double b2 = EvalFinalParam(5, y_val, Q2_val);\n"
        "  double c0 = EvalFinalParam(6, y_val, Q2_val);\n"
        "  double c1 = EvalFinalParam(7, y_val, Q2_val);\n"
        "  double c2 = EvalFinalParam(8, y_val, Q2_val);\n"
        "  double pT2 = pT_val * pT_val;\n"
        "  double z2  = z_val  * z_val;\n"
        "  double slope     = a0 + a1*pT_val + a2*pT2;\n"
        "  double intercept = b0 + b1*pT_val + b2*pT2;\n"
        "  double quad      = c0 + c1*pT_val + c2*pT2;\n"
        "  double output = intercept + slope*z_val + quad*z2;\n"
        "  if(output < 0){output = 0;}\n"
        "  return output;\n"
        "}\n"
    )

    cpp_code = "\n".join(cpp_lines)
    ROOT.gInterpreter.Declare(cpp_code)
    ROOT.InitFinal4DParams()
    print(f"{color.BCYAN}declare_final_F_function: C++ F_4D_eval(y,Q2,pT,z) declared and initialized with final A/B/C parameters.{color.END}")


# ----------------------------------------------------------------------
# Test: compare original bin_content vs F_4D_eval prediction per 4D bin
# ----------------------------------------------------------------------
def test_final_F_vs_original(rdf_file, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    print(f"{color.BYELLOW}Running final 4D test: comparing bin_content to F_4D_eval(y,Q2,pT,z) per 4D bin index.{color.END}")

    rdf      = ROOT.RDataFrame("h22", rdf_file)
    colnames = list(rdf.GetColumnNames())
    if("Q2_y_z_pT_4D_Bins" not in colnames):
        msg = f"{color.RED}test_final_F_vs_original: Column 'Q2_y_z_pT_4D_Bins' not found in tree 'h22'. Will look in 'h22_tmp'...{color.END}"
        print(msg)
        rdf      = ROOT.RDataFrame("h22_tmp", rdf_file)
        colnames = list(rdf.GetColumnNames())
        if("Q2_y_z_pT_4D_Bins" not in colnames):
            msg = f"{msg}\n{color.RED}Also looked for Column 'Q2_y_z_pT_4D_Bins' in tree 'h22_tmp'. Cannot build 4D-bin histograms.{color.END}"
            print(msg)
            return msg

    # Define F_4D prediction per event
    rdf_with_F = rdf.Define("F_fit_val", "F_4D_eval(y_val, Q2_val, pT_val, z_val)")

    # Determine bin range from data
    max_bin = int(rdf.Max("Q2_y_z_pT_4D_Bins").GetValue())
    min_bin = int(rdf.Min("Q2_y_z_pT_4D_Bins").GetValue())
    n_bins  = max_bin - min_bin + 1
    x_min   = float(min_bin) - 0.5
    x_max   = float(max_bin) + 0.5

    # Histos: original (bin_content), fitted (F_fit_val), and their ratio
    h_orig_rptr = rdf_with_F.Histo1D(("h_4D_binContent", "Weight to go from MC GEN to Unfolded Data #scale[0.75]{(per 4D bin)}; 4D Bin Index; Weight per Bin (at center)", n_bins, x_min, x_max), "Q2_y_z_pT_4D_Bins", "bin_content")
    h_fit_rptr  = rdf_with_F.Histo1D(("h_4D_Ffit",       "Weight to go from MC GEN to Unfolded Data #scale[0.75]{(per 4D bin)}; 4D Bin Index; Weight per Bin (at center)", n_bins, x_min, x_max), "Q2_y_z_pT_4D_Bins", "F_fit_val")

    h_orig = h_orig_rptr.GetValue()
    h_fit  = h_fit_rptr.GetValue()

    h_ratio = h_fit.Clone("h_4D_ratio_F_over_binContent")
    h_ratio.SetTitle("#frac{Continuous Function}{Per Bin Ratio} Weight per 4D bin; 4D Bin Index; #frac{Continuous Function}{Per Bin Ratio}")
    h_ratio.Divide(h_orig)

    # helper to compute average bin content (regular bins only)
    def avg_bin_content(h):
        nbins = h.GetNbinsX()
        if(nbins <= 0):
            return 0.0
        sum_content = 0.0
        for ibin in range(1, nbins + 1):
            sum_content += h.GetBinContent(ibin)
        return sum_content / float(nbins)

    avg_orig  = avg_bin_content(h_orig)
    avg_fit   = avg_bin_content(h_fit)
    avg_ratio = avg_bin_content(h_ratio)

    # Write histograms into RDF file
    tfile = ROOT.TFile.Open(rdf_file, "UPDATE")
    if((tfile is None) or tfile.IsZombie()):
        print(f"{color.RED}test_final_F_vs_original: FAILED to reopen RDF file '{rdf_file}' in UPDATE mode; histos not written.{color.END}")
    else:
        safe_write(h_orig,  tfile)
        safe_write(h_fit,   tfile)
        safe_write(h_ratio, tfile)
        tfile.Close()
        print(f"{color.BGREEN}test_final_F_vs_original: Wrote h_4D_binContent, h_4D_Ffit, h_4D_ratio_F_over_binContent to '{rdf_file}'.{color.END}")

    email_summary  = "Final 4D fit vs original bin_content test:\n"
    email_summary += f"  4D bin index range: [{min_bin}, {max_bin}] (n_bins = {n_bins})\n"
    email_summary += f"  Integral(h_4D_binContent) = {h_orig.Integral():.6g}\n"
    email_summary += f"  Integral(h_4D_Ffit)       = {h_fit.Integral():.6g}\n"
    email_summary += f"  Avg bin content(h_4D_binContent) = {avg_orig:.6g}\n"
    email_summary += f"  Avg bin content(h_4D_Ffit)       = {avg_fit:.6g}\n"
    email_summary += f"  Avg bin content(h_4D_ratio)      = {avg_ratio:.6g}\n"

    # Optional plots
    if(save_plots):
        if(not os.path.exists(plot_dir)):
            os.makedirs(plot_dir, exist_ok=True)

        old_optstat = ROOT.gStyle.GetOptStat()
        ROOT.gStyle.SetOptStat("e")

        # Overlay of original vs fitted (2 pads, text on the right)
        c1_name = "c_4D_binContent_vs_Ffit"

        canvas1 = ROOT.TCanvas(c1_name, c1_name, 1400, 700)
        canvas1.Divide(2, 1)

        canvas1.cd(1)
        h_orig.SetLineColor(ROOT.kBlue)
        h_fit.SetLineColor(ROOT.kRed)
        h_orig.SetLineWidth(2)
        h_fit.SetLineWidth(2)
        h_fit.Draw("HIST")
        h_orig.Draw("HIST SAME")

        legend = ROOT.TLegend(0.15, 0.80, 0.45, 0.90)
        legend.AddEntry(h_orig, "Per Bin Ratio Weight", "l")
        legend.AddEntry(h_fit,  "Continous Function (Predicted) Weight", "l")
        legend.Draw()

        canvas1.cd(2)
        ROOT.gPad.SetLeftMargin(0.10)
        ROOT.gPad.SetRightMargin(0.10)
        ROOT.gPad.SetTopMargin(0.10)
        ROOT.gPad.SetBottomMargin(0.10)

        latex = ROOT.TLatex()
        latex.SetNDC(True)
        latex.SetTextSize(0.03)
        latex.SetTextAlign(13)

        x0 = 0.05
        y0 = 0.95
        dy = 0.045

        bin_lines = [
            r"Conversion Key for Q^{2}-y Bins to the 4D Bins shown:",
            r"#scale[0.85]{Q^{2}-y Bin  1: 4D Bins   1 to  35}",
            r"#scale[0.85]{Q^{2}-y Bin  2: 4D Bins  36 to  71}",
            r"#scale[0.85]{Q^{2}-y Bin  3: 4D Bins  72 to 101}",
            r"#scale[0.85]{Q^{2}-y Bin  4: 4D Bins 102 to 137}",
            r"#scale[0.85]{Q^{2}-y Bin  5: 4D Bins 138 to 173}",
            r"#scale[0.85]{Q^{2}-y Bin  6: 4D Bins 174 to 203}",
            r"#scale[0.85]{Q^{2}-y Bin  7: 4D Bins 204 to 239}",
            r"#scale[0.85]{Q^{2}-y Bin  8: 4D Bins 240 to 274}",
            r"#scale[0.85]{Q^{2}-y Bin  9: 4D Bins 275 to 309}",
            r"#scale[0.85]{Q^{2}-y Bin 10: 4D Bins 310 to 345}",
            r"#scale[0.85]{Q^{2}-y Bin 11: 4D Bins 346 to 370}",
            r"#scale[0.85]{Q^{2}-y Bin 12: 4D Bins 371 to 395}",
            r"#scale[0.85]{Q^{2}-y Bin 13: 4D Bins 396 to 425}",
            r"#scale[0.85]{Q^{2}-y Bin 14: 4D Bins 426 to 461}",
            r"#scale[0.85]{Q^{2}-y Bin 15: 4D Bins 462 to 486}",
            r"#scale[0.85]{Q^{2}-y Bin 16: 4D Bins 487 to 516}",
            r"#scale[0.85]{Q^{2}-y Bin 17: 4D Bins 517+}",
            f"Average Bin Content #color[{ROOT.kBlue}]{{(Per Bin)}}  = {avg_orig:.4g}",
            f"Average Bin Content #color[{ROOT.kRed}]{{(Function)}} = {avg_fit:.4g}",
        ]

        y = y0
        for line in bin_lines:
            latex.DrawLatex(x0, y, line)
            y -= dy

        base1 = c1_name if((image_suffix is None) or (len(str(image_suffix)) == 0)) else f"{c1_name}_{image_suffix}"
        out1  = os.path.join(plot_dir, f"{base1}{file_ext}")
        canvas1.SaveAs(out1)
        del canvas1

        c2_name = "c_4D_ratio_F_over_binContent"
        canvas2 = ROOT.TCanvas(c2_name, c2_name, 900, 700)
        h_ratio.SetLineColor(ROOT.kBlack)
        h_ratio.SetLineWidth(2)
        h_ratio.Draw("HIST")

        avg_text_2 = ROOT.TLatex()
        avg_text_2.SetNDC(True)
        avg_text_2.SetTextSize(0.03)
        avg_text_2.SetTextAlign(13)
        avg_text_2.DrawLatex(0.15, 0.85, f"Average Bin Content (ratio) = {avg_ratio:.4g}")

        base2 = c2_name if((image_suffix is None) or (len(str(image_suffix)) == 0)) else f"{c2_name}_{image_suffix}"
        out2  = os.path.join(plot_dir, f"{base2}{file_ext}")
        canvas2.SaveAs(out2)
        del canvas2

        ROOT.gStyle.SetOptStat(old_optstat)

        email_summary += f"  4D comparison canvases written to: {plot_dir} (base names '{c1_name}', '{c2_name}', format '{file_ext}')\n"

    print(email_summary)
    return email_summary


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Build ratio histograms, build an RDataFrame, do z- and pT-fits, then fit parameters vs Q^2 and y.",
                                     formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument("-r", "-inR", "--input_root", default="Unfold_4D_Bins_Test_with_SF_FirstOrder_Almost_All.root",
                        help="Input ROOT file containing the TH1D histograms.\n")
    parser.add_argument("-nh", "--num_hist", default="(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the numerator TH1D histogram in the input file.\n")
    parser.add_argument("-dh", "--den_hist", default="(1D)_(gdf)_(SMEAR='')_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the denominator TH1D histogram in the input file.\n")
    parser.add_argument("-rh", "--ratio_hist", default=None,
                        help="Name to use (or look for) for the ratio TH1D histogram in the input file.")
    parser.add_argument("-rf", "--rdf_file", default="Kinematic_4D_Unfolding.root",
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

    parser.add_argument("-z3", "--z_cubic", action="store_true",
                        help="Allow cubic polynomials in the z-fits (degree 3) when there are ≥4 distinct z points. Otherwise fall back to quadratic/linear.")
    parser.add_argument("-pT3", "--pT_cubic", action="store_true",
                        help="Allow cubic polynomials in the pT-fits (degree 3) when there are ≥4 distinct pT points. Otherwise fall back to quadratic/linear.")
    parser.add_argument("-Q23", "-pol3", "--Q2_cubic", action="store_true",
                        help="Allow cubic polynomials in the Q^2-fits (degree 3) when there are ≥4 distinct Q^2 points. Otherwise fall back to quadratic/linear.")
    parser.add_argument("-y3", "--y_cubic", action="store_true",
                        help="Allow cubic polynomials in the y-fits (degree 3) when there are ≥4 distinct y points. Otherwise fall back to quadratic/linear.")

    parser.add_argument("-np", "--no_plots", action="store_true",
                        help="Do NOT save any fit plots (z, pT, Q^2, or y).")

    parser.add_argument("-zdir", "--z_plot_dir", default="ZFit_Plots",
                        help="Output directory for all fit plots (z, pT, Q^2, y).")
    parser.add_argument("-n", "-tag", "--image_suffix", default=None, type=str,
                        help="Optional string appended to fit image filenames.")
    parser.add_argument("-fmt", "--image_format", default="png", choices=["png", "pdf"],
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

    email_output_4D    = None
    email_output_FTest = None

    if(save_plots):
        ROOT.gROOT.SetBatch(True)

    try:
        # Decide whether we actually need to build / rebuild the RDF file
        need_build_rdf = False
        if((not os.path.exists(args.rdf_file)) or args.force_rdf):
            need_build_rdf = True
        else:
            if(not rdf_tree_has_4D_columns(args.rdf_file, "h22")):
                print(f"{color.YELLOW}Existing RDF file '{args.rdf_file}' is missing required 4D columns; rebuilding it now.{color.END}")
                need_build_rdf = True

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
            msg = f"{color.BBLUE}RDataFrame file '{args.rdf_file}' already exists with required 4D columns and --force_rdf was not set. Skipping RDataFrame rebuild.{color.END}"
            print(msg if(args.email_message is None) else f"{msg}\n\nUser message:\n{args.email_message}\n")

        if(not os.path.exists(args.rdf_file)):
            raise RuntimeError(f"RDataFrame file '{args.rdf_file}' does not exist even after attempted build.")

        z_fit_results   = None
        pT_fit_results  = None
        Q2_fit_results  = None
        Y_fit_results   = None

        if(do_z_fits):
            rdf_for_fits = ROOT.RDataFrame("h22", args.rdf_file)
            z_fit_results = perform_z_fits(rdf_for_fits, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext, allow_cubic=args.z_cubic)
            print(f"{color.BCYAN}Stored {len(z_fit_results)} z-fit result rows in memory (Python list).{color.END}")

        if(do_z_fits and do_pT_fits and (z_fit_results is not None) and (len(z_fit_results) > 0)):
            pT_fit_results = perform_pT_fits(z_fit_results, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext, allow_cubic=args.pT_cubic)
            print(f"{color.BCYAN}Stored {len(pT_fit_results)} pT-fit (z,pT) descriptions in memory (by Q2_y_Bin).{color.END}")

            rdf_orig = ROOT.RDataFrame("h22", args.rdf_file)
            attach_pT_params_to_rdf(rdf_orig, pT_fit_results, args.rdf_file, tree_name="h22")

            if(do_Q2_fits):
                rdf_for_Q2 = ROOT.RDataFrame("h22", args.rdf_file)
                Q2_fit_results = perform_Q2_fits(rdf_for_Q2, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext, allow_cubic=args.Q2_cubic)

                if(do_y_fits and (Q2_fit_results is not None) and (len(Q2_fit_results) > 0)):
                    Y_fit_results = perform_y_fits(Q2_fit_results, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext, allow_cubic=args.y_cubic)
                    if((Y_fit_results is not None) and (len(Y_fit_results) > 0)):
                        _, _, _, email_output_4D = print_final_4D_function(Y_fit_results)

                        # Declare F_4D_eval in C++ and run final 4D-bin test
                        declare_final_F_function(Y_fit_results)
                        email_output_FTest = test_final_F_vs_original(args.rdf_file, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)

        email_body = f"{color.BGREEN}python_Unfold_4D_for_weights.py script completed successfully.{color.END}"
        email_body += f"\n\nInput ROOT file: {args.input_root}\n"
        email_body += f"Numerator hist:  {args.num_hist}\n"
        email_body += f"Denominator hist:{args.den_hist}\n"
        email_body += f"Ratio hist:      {ratio_name}\n"
        email_body += f"RDF file:        {args.rdf_file}\n"
        if(do_z_fits and (z_fit_results is not None)):
            email_body += f"z-fits in memory: {len(z_fit_results)} results (polynomial in z, up to cubic).\n"
        if(do_z_fits and do_pT_fits and (pT_fit_results is not None)):
            email_body += f"pT-fit functions (polynomial in pT, up to cubic) per Q2_y_Bin: {len(pT_fit_results)}\n"
        if(do_z_fits and do_pT_fits and do_Q2_fits and (Q2_fit_results is not None)):
            total_Q2_combos = sum(len(v) for v in Q2_fit_results.values())
            email_body += f"Q^2-fit functions (polynomial, up to cubic) for (param,y) combinations: {total_Q2_combos}\n"
        if(do_z_fits and do_pT_fits and do_Q2_fits and do_y_fits and (Y_fit_results is not None)):
            total_Y_combos = sum(len(v) for v in Y_fit_results.values())
            email_body += f"y-fit functions (polynomial in y, up to cubic) for (param,q_index) combinations: {total_Y_combos}\n"
        if(save_plots):
            email_body += f"Fit image directory: {args.z_plot_dir}\n"
            email_body += f"Fit image format: {args.image_format}\n"
            if(args.image_suffix is not None):
                email_body += f"Image filename suffix: {args.image_suffix}\n"

        # Note which cubic options were enabled
        cubic_flags = []
        if(args.z_cubic):
            cubic_flags.append("z")
        if(args.pT_cubic):
            cubic_flags.append("pT")
        if(args.Q2_cubic):
            cubic_flags.append("Q^2")
        if(args.y_cubic):
            cubic_flags.append("y")
        if(len(cubic_flags) > 0):
            email_body += f"Cubic fits enabled for: {', '.join(cubic_flags)}\n"

        if(args.email_message is not None):
            email_body += f"\nUser message:\n{args.email_message}\n"

        if(email_output_4D is not None):
            email_body = f"{email_body}\n{email_output_4D}"
        if(email_output_FTest is not None):
            email_body = f"{email_body}\n{email_output_FTest}"

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
