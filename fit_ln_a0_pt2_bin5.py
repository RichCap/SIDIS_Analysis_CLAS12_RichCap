#!/usr/bin/env python3
# Optional Q2-y Bin 5 ln(A0) versus P_T^2 fits. Not used by the normal plotters.
# Reads stored data fits. Does not refit phi_h and does not write the source JSON.

import array
import math
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.TH1.AddDirectory(0)

analysis_dir = os.path.abspath(os.path.dirname(__file__))
if(analysis_dir not in sys.path):
    sys.path.insert(0, analysis_dir)
from MyCommonAnalysisFunction_richcap import Get_Num_of_z_pT_Rows_and_Columns, skip_condition_z_pT_bins
from Binning_Dictionaries import Full_Bin_Definition_Array
from Cross_Section_Normalization import Bin_Area_by_Widths_Calc, Cross_Section_Normalization, representative_q2_y, virtual_photon_flux_y
import json

out_dir = "/Users/richardcapobianco/Desktop/Q2yBin5_ParameterA_Slices/LnA0_vs_pT2"
data_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/Run_Large_Files_For_Iterative_Corrections/Comparison_With_Unfolding/Hybrid_3D_rho0_acc025_bayes_ref4.json"
Q2Y_BIN = 5
POOR_CHI2_NDF = 2.0

class NormArgs:
    verbose = False
    pT2 = True
    no_apply_beam_corrections = False

def load_data():
    handle = open(data_path)
    payload = json.load(handle)
    handle.close()
    return payload["Fit_Pars_from_3D_BC_RC_Bayesian"]

def bin_info(zpt_bin):
    z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array["Q2-y=%d, z-pT=%d" % (Q2Y_BIN, zpt_bin)]
    z_mid = 0.5 * (float(z_min) + float(z_max))
    pT_mid = 0.5 * (float(pT_min) + float(pT_max))
    return {"zpt": zpt_bin, "z": z_mid, "pT": pT_mid, "pT2": pT_mid * pT_mid}

def normalized_a0(data_fit, zpt_bin):
    info = bin_info(zpt_bin)
    entry = data_fit["(Q2_y_Bin_%d)-(z_pT_Bin_%d)" % (Q2Y_BIN, zpt_bin)]
    _, bin_area, luminosity, photon_flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=Q2Y_BIN, z_pT_Bin=zpt_bin, args_in=NormArgs())
    area_again, _ = Bin_Area_by_Widths_Calc(args=NormArgs(), Q2_y_Bin=Q2Y_BIN, z_pT_Bin=zpt_bin, phi_t_bin=15)
    q2_rep, y_rep = representative_q2_y(Q2Y_BIN)
    flux_again = virtual_photon_flux_y(q2_rep, y_rep)
    if(abs(float(bin_area) - float(area_again)) > 1e-6 * abs(float(bin_area))):
        raise SystemExit("bin-area mismatch for z-pT bin %d" % zpt_bin)
    if(abs(float(photon_flux) - float(flux_again)) > 1e-8 * abs(float(photon_flux))):
        raise SystemExit("photon-flux mismatch for z-pT bin %d" % zpt_bin)
    scale = float(bin_area) * float(luminosity) * float(photon_flux)
    if(scale == 0.0):
        raise SystemExit("zero normalization scale for z-pT bin %d" % zpt_bin)
    info["A"] = float(entry["Fit_Par_A"]) / scale
    info["Ae"] = float(entry["Fit_Par_A_ERR"]) / scale
    info["scale"] = scale
    info["raw_A"] = float(entry["Fit_Par_A"])
    return info

def z_rows():
    rows, columns = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2Y_BIN)
    grouped = {}
    for zpt_bin in range(1, (rows * columns) + 1):
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2Y_BIN, Z_PT_BIN=zpt_bin, BINNING_METHOD="Y_bin")):
            continue
        if(("Q2-y=%d, z-pT=%d" % (Q2Y_BIN, zpt_bin)) not in Full_Bin_Definition_Array):
            continue
        z_group = int((zpt_bin - 1) / columns) + 1
        grouped.setdefault(z_group, []).append(zpt_bin)
    return grouped

def fit_line(points):
    count = len(points)
    if(count < 2):
        return None
    xs = array.array("d", [point["pT2"] for point in points])
    ys = array.array("d", [math.log(point["A"]) for point in points])
    xe = array.array("d", [0.0 for point in points])
    ye = array.array("d", [point["Ae"] / point["A"] for point in points])
    graph = ROOT.TGraphErrors(count, xs, ys, xe, ye)
    x_lo = min(xs)
    x_hi = max(xs)
    if(x_lo == x_hi):
        x_lo = x_lo - 0.01
        x_hi = x_hi + 0.01
    line = ROOT.TF1("ln_a0_line", "[0]+[1]*x", x_lo, x_hi)
    line.SetParameters(ys[0], 0.0)
    result = graph.Fit(line, "SQ")
    if((result is None) or (not result.IsValid()) or (int(result.Status()) != 0)):
        return {"ok": False, "graph": graph, "line": line}
    ndf = int(line.GetNDF())
    chi2 = float(line.GetChisquare())
    if(ndf > 0):
        chi2_ndf = chi2 / float(ndf)
        chi2_text = "%.6g" % chi2_ndf
    else:
        chi2_ndf = None
        chi2_text = "undefined"
    slope = float(line.GetParameter(1))
    intercept = float(line.GetParameter(0))
    slope_err = float(line.GetParError(1))
    intercept_err = float(line.GetParError(0))
    covariance = float(result.CovMatrix(0, 1))
    poor = (chi2_ndf is not None) and (chi2_ndf > POOR_CHI2_NDF)
    return {
        "ok": True, "graph": graph, "line": line, "a": slope, "ae": slope_err,
        "b": intercept, "be": intercept_err, "inv_kt2": -slope, "inv_kt2_e": slope_err,
        "ln_c0": intercept, "ln_c0_e": intercept_err, "chi2": chi2, "ndf": ndf,
        "chi2_ndf": chi2_ndf, "chi2_text": chi2_text, "cov_ab": covariance, "poor": poor,
    }

def draw_row(z_value, fit):
    canvas = ROOT.TCanvas("row", "row", 900, 700)
    fit["graph"].SetTitle("ln A_{0} versus P_{T}^{2} at z = %.4g" % z_value)
    fit["graph"].GetXaxis().SetTitle("P_{T}^{2} (GeV^{2})")
    fit["graph"].GetYaxis().SetTitle("ln A_{0}")
    fit["graph"].SetMarkerStyle(20)
    fit["graph"].Draw("AP")
    fit["line"].SetLineColor(ROOT.kRed)
    fit["line"].Draw("same")
    canvas.SaveAs(os.path.join(out_dir, "LnA0_vs_pT2_z%.4g.pdf" % z_value))
    canvas.Close()

def draw_summary(rows, key, err_key, y_title, file_name):
    count = len(rows)
    if(count == 0):
        return
    xs = array.array("d", [row["z"] for row in rows])
    ys = array.array("d", [row[key] for row in rows])
    xe = array.array("d", [0.0 for row in rows])
    ye = array.array("d", [row[err_key] for row in rows])
    graph = ROOT.TGraphErrors(count, xs, ys, xe, ye)
    canvas = ROOT.TCanvas("sum", "sum", 900, 700)
    graph.SetTitle(y_title + " versus z")
    graph.GetXaxis().SetTitle("z")
    graph.GetYaxis().SetTitle(y_title)
    graph.SetMarkerStyle(20)
    graph.Draw("AP")
    canvas.SaveAs(os.path.join(out_dir, file_name))
    canvas.Close()

def main():
    os.makedirs(out_dir, exist_ok=True)
    data_fit = load_data()
    grouped = z_rows()
    table_path = os.path.join(out_dir, "LnA0_pT2_fits.txt")
    handle = open(table_path, "w")
    handle.write("z_row\tz\tn_fit\texcluded_zpt\ta\ta_err\tb\tb_err\tinv_kT2\tinv_kT2_err\tln_C0\tln_C0_err\tchi2\tndf\tchi2_ndf\tcov_ab\tflag\n")
    fitted = []
    for z_group in sorted(grouped):
        cells = []
        excluded = []
        for zpt_bin in grouped[z_group]:
            point = normalized_a0(data_fit, zpt_bin)
            if(point["A"] <= 0.0):
                excluded.append(str(zpt_bin))
                continue
            cells.append(point)
        cells = sorted(cells, key=lambda point: point["pT2"])
        z_value = cells[0]["z"] if(len(cells) > 0) else bin_info(grouped[z_group][0])["z"]
        result = fit_line(cells)
        excluded_text = ",".join(excluded) if(len(excluded) > 0) else "-"
        if((result is None) or (not result["ok"])):
            handle.write("%d\t%.6g\t%d\t%s\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\tundefined\t-\tunsuccessful\n" % (z_group, z_value, len(cells), excluded_text))
            print("z row %d at z=%.4g: unsuccessful, %d positive points, excluded %s" % (z_group, z_value, len(cells), excluded_text))
            continue
        flag = "poor" if(result["poor"]) else "ok"
        handle.write("%d\t%.6g\t%d\t%s\t%.8g\t%.8g\t%.8g\t%.8g\t%.8g\t%.8g\t%.8g\t%.8g\t%.8g\t%d\t%s\t%.8g\t%s\n" % (
            z_group, z_value, len(cells), excluded_text, result["a"], result["ae"], result["b"], result["be"],
            result["inv_kt2"], result["inv_kt2_e"], result["ln_c0"], result["ln_c0_e"], result["chi2"], result["ndf"],
            result["chi2_text"], result["cov_ab"], flag,
        ))
        draw_row(z_value, result)
        fitted.append({"z": z_value, "inv_kt2": result["inv_kt2"], "inv_kt2_e": result["inv_kt2_e"], "ln_c0": result["ln_c0"], "ln_c0_e": result["ln_c0_e"]})
        print("z row %d at z=%.4g: a=%.6g b=%.6g inv_kT2=%.6g flag=%s excluded=%s" % (z_group, z_value, result["a"], result["b"], result["inv_kt2"], flag, excluded_text))
    handle.close()
    draw_summary(fitted, "inv_kt2", "inv_kt2_e", "1/#LT k_{T}^{2}(z) #GT", "Inverse_kT2_vs_z.pdf")
    draw_summary(fitted, "ln_c0", "ln_c0_e", "ln C_{0}(z)", "ln_C0_vs_z.pdf")
    print("wrote %s" % out_dir)

if(__name__ == "__main__"):
    main()
