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

# Single email recipient (you can hardcode your real address here)
EMAIL_RECIPIENT = "richard.capobianco@uconn.edu"


# ----------------------------------------------------------------------
# ANSI → HTML + email helper
# ----------------------------------------------------------------------
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {  # Styles
                      '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
                      # Colors
                      '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
                      # Reset
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

    # Reuse logic disabled for now due to previous segfaults.
    # Can revisit later if needed.

    num_hist = root_file.Get(num_name)
    den_hist = root_file.Get(den_name)

    if(num_hist is None):
        raise RuntimeError(f"Numerator histogram '{num_name}' not found in file.")
    if(den_hist is None):
        raise RuntimeError(f"Denominator histogram '{den_name}' not found in file.")

    ratio_hist = num_hist.Clone(ratio_name)
    ratio_hist.SetDirectory(0)
    # ratio_hist.Sumw2()  # Keep original errors

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
# ----------------------------------------------------------------------
def perform_z_fits(rdf, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    print(f"{color.BCYAN}Starting z-fits using RDataFrame.{color.END}")

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

            cut_expr = f"(Q2_y_Bin == {Q2_y_Bin_key}) && (pT_val >= {pT_min}) && (pT_val < {pT_max}) && (z_val >= {Z_MIN}) && (z_val <= {Z_MAX})"
            df_slice = rdf.Filter(cut_expr, f"Q2_y_Bin={Q2_y_Bin_key}, pT in [{pT_min},{pT_max})")

            np_dict  = df_slice.AsNumpy(["z_val", "bin_content", "bin_error"])
            z_vals   = numpy.array(np_dict["z_val"],        dtype="float64")
            y_vals   = numpy.array(np_dict["bin_content"],  dtype="float64")
            err_vals = numpy.array(np_dict["bin_error"],    dtype="float64")

            n_points = len(z_vals)
            if(n_points < 2):
                print(f"{color.YELLOW}Skipping Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min}, {pT_max}) due to insufficient points (n={n_points}).{color.END}")
                continue

            graph = ROOT.TGraphErrors(n_points)
            for idx in range(n_points):
                graph.SetPoint(idx, float(z_vals[idx]), float(y_vals[idx]))
                graph.SetPointError(idx, 0.0, float(err_vals[idx]))

            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.0)
            graph.SetLineWidth(2)

            fit_func = ROOT.TF1("f_z_tmp", "[0] + [1]*x", Z_MIN, Z_MAX)

            intercept_guess = float(numpy.mean(y_vals))
            fit_func.SetParameter(0, intercept_guess)
            fit_func.SetParameter(1, 0.0)

            fit_result = graph.Fit(fit_func, "QSRN")

            slope         = fit_func.GetParameter(1)
            slope_err     = fit_func.GetParError(1)
            intercept     = fit_func.GetParameter(0)
            intercept_err = fit_func.GetParError(0)
            chi2          = fit_func.GetChisquare()
            ndf           = fit_func.GetNDF()
            pT_center     = 0.5 * (pT_min + pT_max)

            print(f"{color.BBLUE}Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min:.3f}, {pT_max:.3f}) "
                  f"n={n_points}, slope={slope:.4g} ± {slope_err:.4g}, "
                  f"intercept={intercept:.4g} ± {intercept_err:.4g}, "
                  f"chi2/ndf={chi2}/{ndf}{color.END}")

            if(save_plots):
                pT_center_code = int(round(1000.0 * pT_center))
                cname = f"c_zFit_Q2_y_Bin_{Q2_y_Bin_key}_pT_{pT_center_code:03d}"

                canvas = ROOT.TCanvas(cname, cname, 800, 600)

                title_str = f"z-fit: Q2_y_Bin={Q2_y_Bin_key}, pT=[{pT_min:.2f},{pT_max:.2f})"
                graph.SetTitle(f"{title_str};z;Ratio of #frac{{Unfolded Data}}{{Generated MC}}")
                graph.Draw("AP")

                fit_func.SetLineColor(ROOT.kRed)
                fit_func.SetLineWidth(2)
                fit_func.Draw("same")

                latex = ROOT.TLatex()
                latex.SetNDC(True)
                latex.SetTextSize(0.04)
                latex.DrawLatex(0.15, 0.88, f"slope = {slope:.4g} #pm {slope_err:.4g}")
                latex.DrawLatex(0.15, 0.83, f"intercept = {intercept:.4g} #pm {intercept_err:.4g}")
                latex.DrawLatex(0.15, 0.78, f"#chi^{{2}}/ndf = {chi2:.1f} / {ndf}")

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
                "slope":         slope,
                "slope_err":     slope_err,
                "intercept":     intercept,
                "intercept_err": intercept_err,
                "chi2":          chi2,
                "ndf":           ndf,
            })

    print(f"{color.BGREEN}z-fits complete. Total successful fits: {len(results)}.{color.END}")
    return results


# ----------------------------------------------------------------------
# pT-fit layer: slope(pT) and intercept(pT) for each Q2_y_Bin
# ----------------------------------------------------------------------
def perform_pT_fits(z_fit_results, save_plots=True, plot_dir="ZFit_Plots", image_suffix=None, file_ext=".png"):
    print(f"{color.BPURPLE}Starting pT-fits of z-fit parameters.{color.END}")

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
        if(n < 2):
            print(f"{color.YELLOW}Skipping pT-fit for Q2_y_Bin={Q2_y_Bin_key} (only {n} z-fit points).{color.END}")
            continue

        pT_centers     = numpy.array([r["pT_center"]     for r in rows], dtype="float64")
        slopes         = numpy.array([r["slope"]         for r in rows], dtype="float64")
        slope_errs     = numpy.array([r["slope_err"]     for r in rows], dtype="float64")
        intercepts     = numpy.array([r["intercept"]     for r in rows], dtype="float64")
        intercept_errs = numpy.array([r["intercept_err"] for r in rows], dtype="float64")

        # Slope vs pT
        g_slope = ROOT.TGraphErrors(n)
        for idx in range(n):
            g_slope.SetPoint(idx, float(pT_centers[idx]), float(slopes[idx]))
            g_slope.SetPointError(idx, 0.0, float(slope_errs[idx]))
        g_slope.SetMarkerStyle(21)
        g_slope.SetMarkerSize(1.0)
        g_slope.SetLineWidth(2)

        # Intercept vs pT
        g_int = ROOT.TGraphErrors(n)
        for idx in range(n):
            g_int.SetPoint(idx, float(pT_centers[idx]), float(intercepts[idx]))
            g_int.SetPointError(idx, 0.0, float(intercept_errs[idx]))
        g_int.SetMarkerStyle(22)
        g_int.SetMarkerSize(1.0)
        g_int.SetLineWidth(2)

        pT_min_fit = float(min(pT_centers))
        pT_max_fit = float(max(pT_centers))

        f_slope = ROOT.TF1(f"f_slope_Q2yBin_{Q2_y_Bin_key}", "[0] + [1]*x", pT_min_fit, pT_max_fit)
        f_int   = ROOT.TF1(f"f_int_Q2yBin_{Q2_y_Bin_key}",   "[0] + [1]*x", pT_min_fit, pT_max_fit)

        f_slope.SetParameter(0, float(numpy.mean(slopes)))
        f_slope.SetParameter(1, 0.0)
        f_int.SetParameter(0, float(numpy.mean(intercepts)))
        f_int.SetParameter(1, 0.0)

        g_slope.Fit(f_slope, "QSRN")
        g_int.Fit(f_int, "QSRN")

        a0      = f_slope.GetParameter(0)
        a0_err  = f_slope.GetParError(0)
        a1      = f_slope.GetParameter(1)
        a1_err  = f_slope.GetParError(1)
        chi2_s  = f_slope.GetChisquare()
        ndf_s   = f_slope.GetNDF()

        b0      = f_int.GetParameter(0)
        b0_err  = f_int.GetParError(0)
        b1      = f_int.GetParameter(1)
        b1_err  = f_int.GetParError(1)
        chi2_i  = f_int.GetChisquare()
        ndf_i   = f_int.GetNDF()

        print(f"{color.BPURPLE}Q2_y_Bin={Q2_y_Bin_key}: slope(pT) = a0 + a1*pT with "
              f"a0={a0:.4g}±{a0_err:.4g}, a1={a1:.4g}±{a1_err:.4g}, chi2/ndf={chi2_s}/{ndf_s}; "
              f"intercept(pT) = b0 + b1*pT with b0={b0:.4g}±{b0_err:.4g}, b1={b1:.4g}±{b1_err:.4g}, "
              f"chi2/ndf={chi2_i}/{ndf_i}{color.END}")

        if(save_plots):
            # Slope vs pT plot
            cname_slope = f"c_pTFit_slope_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_s = ROOT.TCanvas(cname_slope, cname_slope, 800, 600)
            title_s  = f"Slope vs p_{{T}}: Q2_y_Bin={Q2_y_Bin_key}"
            g_slope.SetTitle(f"{title_s};p_{{T}} (GeV);Slope of z-fit")
            g_slope.Draw("AP")
            f_slope.SetLineColor(ROOT.kRed)
            f_slope.SetLineWidth(2)
            f_slope.Draw("same")

            latex_s = ROOT.TLatex()
            latex_s.SetNDC(True)
            latex_s.SetTextSize(0.04)
            latex_s.DrawLatex(0.15, 0.88, f"a0 = {a0:.4g} #pm {a0_err:.4g}")
            latex_s.DrawLatex(0.15, 0.83, f"a1 = {a1:.4g} #pm {a1_err:.4g}")
            latex_s.DrawLatex(0.15, 0.78, f"#chi^{{2}}/ndf = {chi2_s:.1f} / {ndf_s}")

            if((image_suffix is not None) and (len(str(image_suffix)) > 0)):
                base_s = f"{cname_slope}_{image_suffix}"
            else:
                base_s = cname_slope
            out_s = os.path.join(plot_dir, f"{base_s}{file_ext}")
            canvas_s.SaveAs(out_s)
            del canvas_s

            # Intercept vs pT plot
            cname_i = f"c_pTFit_intercept_Q2_y_Bin_{Q2_y_Bin_key}"
            canvas_i = ROOT.TCanvas(cname_i, cname_i, 800, 600)
            title_i  = f"Intercept vs p_{{T}}: Q2_y_Bin={Q2_y_Bin_key}"
            g_int.SetTitle(f"{title_i};p_{{T}} (GeV);Intercept of z-fit")
            g_int.Draw("AP")
            f_int.SetLineColor(ROOT.kRed)
            f_int.SetLineWidth(2)
            f_int.Draw("same")

            latex_i = ROOT.TLatex()
            latex_i.SetNDC(True)
            latex_i.SetTextSize(0.04)
            latex_i.DrawLatex(0.15, 0.88, f"b0 = {b0:.4g} #pm {b0_err:.4g}")
            latex_i.DrawLatex(0.15, 0.83, f"b1 = {b1:.4g} #pm {b1_err:.4g}")
            latex_i.DrawLatex(0.15, 0.78, f"#chi^{{2}}/ndf = {chi2_i:.1f} / {ndf_i}")

            if((image_suffix is not None) and (len(str(image_suffix)) > 0)):
                base_i = f"{cname_i}_{image_suffix}"
            else:
                base_i = cname_i
            out_i = os.path.join(plot_dir, f"{base_i}{file_ext}")
            canvas_i.SaveAs(out_i)
            del canvas_i

        # Store the 4-parameter (z,pT) description for this Q2_y_Bin:
        #   slope(pT)     = a0 + a1 * pT
        #   intercept(pT) = b0 + b1 * pT
        #   F(z,pT)       = (a0 + a1*pT)*z + (b0 + b1*pT)
        pt_fit_summary[Q2_y_Bin_key] = {
            "a0": a0, "a0_err": a0_err,
            "a1": a1, "a1_err": a1_err,
            "b0": b0, "b0_err": b0_err,
            "b1": b1, "b1_err": b1_err,
            "chi2_slope": chi2_s,
            "ndf_slope":  ndf_s,
            "chi2_int":   chi2_i,
            "ndf_int":    ndf_i,
        }

    print(f"{color.BGREEN}pT-fits complete. Total Q2_y_Bins with 4-parameter (z,pT) functions: {len(pt_fit_summary)}.{color.END}")
    return pt_fit_summary


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Build ratio histograms and export their 4D-bin contents into an RDataFrame ROOT file, then perform z- and pT-fits.",
                                     formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-r", "-inR", "--input_root", default="Unfold_4D_Bins_Test_with_SF_FirstOrder_Almost_All.root",
                        help="Input ROOT file containing the TH1D histograms.\n")
    parser.add_argument("-nh", "--num_hist", default="(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the numerator TH1D histogram in the input file.\n")
    parser.add_argument("-dh", "--den_hist", default="(1D)_(gdf)_(SMEAR='')_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the denominator TH1D histogram in the input file.\n")
    parser.add_argument("-rh", "--ratio_hist", default=None,
                        help="Name to use (or look for) for the ratio TH1D histogram in the input file. Overwrites the default naming.")
    parser.add_argument("-rf", "--rdf_file", default="Kinematic_4D_Unfolding.root",
                        help="Output ROOT file to store the RDataFrame with bin-by-bin values.\n If this file already exists and `--force_rdf` is not set, the RDataFrame will not be rebuilt.")

    parser.add_argument("-fr", "--force_ratio", action="store_true",
                        help="Force recreation of the ratio histogram even if it already exists in the input file.")
    parser.add_argument("-frdf", "--force_rdf", action="store_true",
                        help="Force recreation of the RDataFrame file even if it already exists.")

    # Fit/plot control: defaults are to DO everything; flags disable.
    parser.add_argument("-noZ", "--no_z_fits", action="store_true",
                        help="Do NOT run bin_content vs z fits for each Q2_y_Bin and pT range.")
    parser.add_argument("-noPT", "--no_pT_fits", action="store_true",
                        help="Do NOT run fits of z-fit parameters vs pT.")
    parser.add_argument("-np", "--no_plots", action="store_true",
                        help="Do NOT save any fit plots (neither z nor pT).")

    parser.add_argument("-zdir", "--z_plot_dir", default="ZFit_Plots",
                        help="Output directory for all fit plots (z and pT).")

    parser.add_argument("-tag", "--image_suffix", default=None, type=str,
                        help="Optional string appended to fit image filenames (before the file extension).")
    parser.add_argument("-fmt", "--image_format", default="png", choices=["png", "pdf"],
                        help="Image file format for saved fit plots (png or pdf).")

    parser.add_argument("-e", "--email", action="store_true",
                        help="Optional email sent at the end of the script.")
    parser.add_argument("-ee", "--email_message", default=None, type=str,
                        help="Additional message to be attached to the email.")

    args = parser.parse_args()
    return args


# ----------------------------------------------------------------------
# Main control flow
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

        z_fit_results  = None
        pT_fit_results = None

        if(do_z_fits):
            rdf_for_fits = ROOT.RDataFrame("h22", args.rdf_file)
            z_fit_results = perform_z_fits(rdf_for_fits, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)
            print(f"{color.BCYAN}Stored {len(z_fit_results)} z-fit result rows in memory (Python list).{color.END}")

            if((not args.no_pT_fits) and (len(z_fit_results) > 0)):
                pT_fit_results = perform_pT_fits(z_fit_results, save_plots=save_plots, plot_dir=args.z_plot_dir, image_suffix=args.image_suffix, file_ext=file_ext)
                print(f"{color.BCYAN}Stored {len(pT_fit_results)} pT-fit (z,pT) functions in memory (by Q2_y_Bin).{color.END}")

        email_body = f"{color.BGREEN}python_Unfold_4D_for_weights.py script completed successfully.{color.END}"
        email_body += f"\n\nInput ROOT file: {args.input_root}\n"
        email_body += f"Numerator hist:  {args.num_hist}\n"
        email_body += f"Denominator hist:{args.den_hist}\n"
        email_body += f"Ratio hist:      {ratio_name}\n"
        email_body += f"RDF file:        {args.rdf_file}\n"
        if(do_z_fits and (z_fit_results is not None)):
            email_body += f"z-fits in memory: {len(z_fit_results)} results\n"
        if(do_z_fits and do_pT_fits and (pT_fit_results is not None)):
            email_body += f"pT-fit functions: {len(pT_fit_results)} Q2_y_Bins\n"
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
