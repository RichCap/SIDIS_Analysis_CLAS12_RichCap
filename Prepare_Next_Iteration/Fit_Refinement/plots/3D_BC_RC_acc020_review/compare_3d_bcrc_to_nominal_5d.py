#!/usr/bin/env python3
# Compare the new 3D BC+RC reweighting file with the July 2026 nominal 5D file.
# Training targets come from the npz files. Weights are the C++ evaluators actually consumed downstream.
# Photon flux matches Cross_Section_Normalization.virtual_photon_flux_y (same constants and formula).

import csv
import json
import math
import os
import re
import sys

import numpy as np

REPO = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
sys.path.append(REPO)
from Binning_Dictionaries import Full_Bin_Definition_Array
sys.path.remove(REPO)

REVIEW = os.path.join(REPO, "Prepare_Next_Iteration", "Fit_Refinement", "plots", "3D_BC_RC_acc020_review")
OUT_DIR = os.path.join(REVIEW, "comparison")
PNG_DIR = os.path.join(REVIEW, "phi_h_png")
PDF_DIR = os.path.join(REVIEW, "phi_h_pdf")
JSON_3D = os.path.join(REPO, "Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Unfolded_Simple_3D_Final_Thesis_Bank_rho0_new_acc020_Zeroth_Order_Full.json")
ROOT_FILE = os.path.join(REPO, "Unfolded_Simple_3D_Final_Thesis_Bank_rho0_new_acc020_Zeroth_Order_Full.root")
FILE_3D = os.path.join(REPO, "Prepare_Next_Iteration", "acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt")
FILE_5D = os.path.join(REPO, "Prepare_Next_Iteration", "rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt")
NPZ_3D = os.path.join(REPO, "Prepare_Next_Iteration", "acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Fit_Par_%s.npz")
NPZ_5D = os.path.join(REPO, "Prepare_Next_Iteration", "rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Fit_Par_%s.npz")
BEFORE_932 = os.path.join(REPO, "Prepare_Next_Iteration", "Fit_Refinement", "plots", "acc020_3D_bcrc_review", "Q2y09_zpt32.png")
CONVERSION_FACTOR = 0.0502731
PROTON_MASS = 0.938272
BEAM_ENERGY = 10.6
FINE_STRUCTURE = 1.0 / 137.035999
REL_FLOOR = 0.05


def virtual_photon_polarization(q2, y_value):
    e2 = BEAM_ENERGY * BEAM_ENERGY
    numer = 1.0 - y_value - (q2 / (4.0 * e2))
    denom = 1.0 - y_value + ((y_value * y_value) / 2.0) + (q2 / (4.0 * e2))
    return numer / denom


def virtual_photon_flux_y(q2, y_value):
    epsilon = virtual_photon_polarization(q2, y_value)
    flux = (FINE_STRUCTURE / (4.0 * math.pi)) * ((2.0 * PROTON_MASS * BEAM_ENERGY * y_value - q2) / (PROTON_MASS * BEAM_ENERGY * q2)) * (1.0 / (1.0 - epsilon))
    return flux


def percentile(values, fraction):
    return float(np.percentile(np.asarray(values, dtype=float), fraction))


def median_abs(values):
    return float(np.median(np.abs(np.asarray(values, dtype=float))))


def array_block(text, name):
    match = re.search(r"const (?:double|int) " + name + r"\[[^\]]*\](?:\[[^\]]*\])?\s*=\s*\{(.*?)\};", text, re.S)
    if(match is None):
        raise RuntimeError("Missing " + name)
    nums = re.findall(r"[-+]?(?:\d+\.\d*|\d+)(?:[eE][-+]?\d+)?", match.group(1))
    return [float(item) for item in nums]


def int_const(text, name):
    match = re.search(r"const int " + name + r"\s*=\s*(\d+);", text)
    return int(match.group(1))


def string_const(text, name):
    match = re.search(r"const std::string " + name + r"\s*=\s*\"([^\"]+)\";", text)
    return match.group(1)


def bool_const(text, name):
    match = re.search(r"const bool " + name + r"\s*=\s*(true|false);", text)
    return match.group(1) == "true"


def load_piece(text, tag):
    count = int_const(text, "n_fit_par_" + tag)
    ndim = int_const(text, "ndim_fit_par_" + tag)
    npoly = int_const(text, "n_poly_fit_par_" + tag)
    centers = array_block(text, "centers_fit_par_" + tag)
    coeffs = array_block(text, "coeffs_fit_par_" + tag)
    shift = array_block(text, "shift_fit_par_" + tag)
    scale = array_block(text, "scale_fit_par_" + tag)
    powers = array_block(text, "powers_fit_par_" + tag)
    kernel = string_const(text, "kernel_fit_par_" + tag)
    epsilon = float(re.search(r"const double epsilon_fit_par_" + tag + r"\s*=\s*([0-9eE.+\-]+);", text).group(1))
    log_space = bool_const(text, "log_space_fit_par_" + tag)
    centers = [centers[i * ndim:(i + 1) * ndim] for i in range(count)]
    powers = [powers[i * ndim:(i + 1) * ndim] for i in range(npoly)]
    return {
        "n": count,
        "ndim": ndim,
        "npoly": npoly,
        "centers": centers,
        "coeffs": coeffs,
        "shift": shift,
        "scale": scale,
        "powers": powers,
        "kernel": kernel,
        "epsilon": epsilon,
        "log_space": log_space,
    }


def kernel_value(radius, kernel):
    if(kernel == "thin_plate_spline"):
        if(radius == 0.0):
            return 0.0
        return radius * radius * math.log(radius)
    if(kernel == "gaussian"):
        return math.exp(-radius * radius)
    raise RuntimeError("Unexpected kernel " + kernel)


def evaluate_piece(piece, point):
    eps = piece["epsilon"]
    ndim = piece["ndim"]
    total = 0.0
    count = piece["n"]
    for i in range(count):
        radius2 = 0.0
        center = piece["centers"][i]
        for j in range(ndim):
            diff = eps * point[j] - eps * center[j]
            radius2 += diff * diff
        total += piece["coeffs"][i] * kernel_value(math.sqrt(radius2), piece["kernel"])
    xhat = []
    for j in range(ndim):
        xhat.append((point[j] - piece["shift"][j]) / piece["scale"][j])
    for m in range(piece["npoly"]):
        mono = 1.0
        power = piece["powers"][m]
        for j in range(ndim):
            powv = int(power[j])
            if(powv != 0):
                mono *= xhat[j] ** powv
        total += piece["coeffs"][count + m] * mono
    if(piece["log_space"]):
        return math.exp(total)
    return total


def load_spline(path):
    text = open(path).read()
    return {"A": load_piece(text, "a"), "B": load_piece(text, "b"), "C": load_piece(text, "c"), "text": text}


def moments_at(spline, point):
    return (
        evaluate_piece(spline["A"], point),
        evaluate_piece(spline["B"], point),
        evaluate_piece(spline["C"], point),
    )


def point_key(point):
    return (round(point[0], 5), round(point[1], 5), round(point[2], 5), round(point[3], 5))


def bin_center(q2y_bin, zpt_bin):
    q2_max, q2_min, y_max, y_min = Full_Bin_Definition_Array["Q2-y=%s, Q2-y" % q2y_bin]
    z_max, z_min, pt_max, pt_min = Full_Bin_Definition_Array["Q2-y=%s, z-pT=%s" % (q2y_bin, zpt_bin)]
    q2_mid = (float(q2_max) + float(q2_min)) / 2.0
    y_mid = (float(y_max) + float(y_min)) / 2.0
    z_mid = (float(z_max) + float(z_min)) / 2.0
    pt_mid = (float(pt_max) + float(pt_min)) / 2.0
    xB_mid = CONVERSION_FACTOR * (q2_mid / y_mid)
    return q2_mid, y_mid, z_mid, pt_mid, xB_mid


def entry_failed(entry, require_chi2=True):
    if(not isinstance(entry, dict)):
        return True
    for name in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
        try:
            value = float(entry[name])
            error = float(entry[name + "_ERR"])
        except Exception:
            return True
        if(not math.isfinite(value)) or (not math.isfinite(error)) or (error == 0.0):
            return True
        if((name == "Fit_Par_A") and (value <= 0.0)):
            return True
        if((name != "Fit_Par_A") and (abs(value) >= 1.0)):
            return True
    if(not require_chi2):
        return False
    try:
        chi2 = float(entry["Chi2"])
        ndf = float(entry["NDF"])
    except Exception:
        return True
    if((not math.isfinite(chi2)) or (chi2 == 0.0) or (not math.isfinite(ndf)) or (ndf <= 0.0)):
        return True
    return False


def load_fit_table(json_path, fit_set, require_chi2=True):
    with open(json_path) as handle:
        payload = json.load(handle)
    table = {}
    failed = []
    fit_dict = payload.get(fit_set, {})
    for key_str, entry in fit_dict.items():
        match = re.fullmatch(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", str(key_str).strip())
        if(match is None):
            continue
        q2y_bin = int(match.group(1))
        zpt_bin = int(match.group(2))
        if(entry_failed(entry, require_chi2=require_chi2)):
            failed.append((q2y_bin, zpt_bin))
            continue
        q2_mid, y_mid, z_mid, pt_mid, xB_mid = bin_center(q2y_bin, zpt_bin)
        table[point_key([xB_mid, y_mid, z_mid, pt_mid])] = {
            "q2y": q2y_bin,
            "zpt": zpt_bin,
            "Q2": q2_mid,
            "y": y_mid,
            "z": z_mid,
            "pT": pt_mid,
            "xB": xB_mid,
            "A": float(entry["Fit_Par_A"]),
            "B": float(entry["Fit_Par_B"]),
            "C": float(entry["Fit_Par_C"]),
            "Aerr": float(entry["Fit_Par_A_ERR"]),
            "Berr": float(entry["Fit_Par_B_ERR"]),
            "Cerr": float(entry["Fit_Par_C_ERR"]),
            "Chi2": float(entry["Chi2"]) if("Chi2" in entry) else None,
            "NDF": float(entry["NDF"]) if("NDF" in entry) else None,
            "red": (float(entry["Chi2"]) / float(entry["NDF"])) if(("Chi2" in entry) and ("NDF" in entry) and (float(entry["NDF"]) > 0.0)) else None,
        }
    return table, failed, sorted(payload.keys())


def npz_map(pattern):
    stored = {}
    meta = {}
    for par_name in ["A", "B", "C"]:
        record = np.load(pattern % par_name, allow_pickle=True)
        points = np.asarray(record["points"], dtype=float)
        values = np.asarray(record["values"], dtype=float)
        log_space = bool(record["log_space"]) if("log_space" in record.files) else False
        meta[par_name] = {
            "n": int(points.shape[0]),
            "kernel": str(record["kernel"]),
            "log_space": log_space,
            "dimension_mode": str(record["dimension_mode"]),
            "smoothing": float(record["smoothing_factor"]) if("smoothing_factor" in record.files) else None,
        }
        for row, value in zip(points, values):
            key = point_key(row)
            stored.setdefault(key, {})
            stored[key][par_name] = float(math.exp(value) if log_space else value)
            stored[key]["point"] = [float(item) for item in row]
    return stored, meta


def summarize_abs(values):
    arr = np.asarray(values, dtype=float)
    abs_arr = np.abs(arr)
    return {
        "n": int(arr.size),
        "median": float(np.median(arr)),
        "median_abs": float(np.median(abs_arr)),
        "p84_abs": percentile(abs_arr, 84),
        "p95_abs": percentile(abs_arr, 95),
        "max_abs": float(np.max(abs_arr)),
        "rms": float(np.sqrt(np.mean(arr * arr))),
    }


def modulation(b_value, c_value, phi_deg):
    phi_rad = math.radians(phi_deg)
    return 1.0 + b_value * math.cos(phi_rad) + c_value * math.cos(2.0 * phi_rad)


def render_phi_pages():
    import fitz
    os.makedirs(PNG_DIR, exist_ok=True)
    existing = [name for name in os.listdir(PNG_DIR) if(name.endswith(".png"))]
    manifest_path = os.path.join(OUT_DIR, "phi_pages.json")
    if((len(existing) >= 452) and os.path.isfile(manifest_path)):
        with open(manifest_path) as handle:
            cached = json.load(handle)
        if(len(cached) >= 452):
            print("reusing phi page pngs", len(cached))
            return cached
    pages = []
    seen = {}
    name_re = re.compile(r"\(Q2_y_Bin_(\d+)\)_\(z_pT_Bin_(\d+)\)")
    for q2y_bin in range(1, 18):
        pdf_path = os.path.join(PDF_DIR, "Q2y%02d_BC_RC_phi_h.pdf" % q2y_bin)
        if(not os.path.isfile(pdf_path)):
            continue
        document = fitz.open(pdf_path)
        for page_index in range(document.page_count):
            text = document[page_index].get_text()
            match = name_re.search(text)
            if(match is None):
                continue
            q2y_found = int(match.group(1))
            zpt_found = int(match.group(2))
            png_name = "Q2y%02d_zpt%02d.png" % (q2y_found, zpt_found)
            png_path = os.path.join(PNG_DIR, png_name)
            pixmap = document[page_index].get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
            pixmap.save(png_path)
            record = {
                "png": png_path,
                "q2y": q2y_found,
                "zpt": zpt_found,
                "pdf": pdf_path,
                "page": page_index + 1,
            }
            seen[(q2y_found, zpt_found)] = record
        document.close()
    for key in sorted(seen):
        pages.append(seen[key])
    return pages


def save_canvas(canvas, stem):
    canvas.SaveAs(os.path.join(OUT_DIR, stem + ".png"))
    canvas.SaveAs(os.path.join(OUT_DIR, stem + ".pdf"))


def fill_hist(name, title, values, nbins, x_min, x_max, color):
    import ROOT
    hist = ROOT.TH1D(name, title, nbins, x_min, x_max)
    hist.SetDirectory(0)
    for value in values:
        hist.Fill(value)
    hist.SetLineColor(color)
    hist.SetFillColor(color)
    hist.SetFillStyle(1001)
    hist.SetLineWidth(2)
    return hist


def style_hist(hist, x_title, y_title):
    hist.GetXaxis().SetTitle(x_title)
    hist.GetYaxis().SetTitle(y_title)
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetLabelSize(0.04)
    hist.GetYaxis().SetLabelSize(0.04)
    hist.SetStats(0)


def graph_from_pairs(x_values, y_values, color, marker):
    import ROOT
    graph = ROOT.TGraph(len(x_values))
    for index, (x_value, y_value) in enumerate(zip(x_values, y_values)):
        graph.SetPoint(index, x_value, y_value)
    graph.SetMarkerStyle(marker)
    graph.SetMarkerSize(0.7)
    graph.SetMarkerColor(color)
    return graph


def write_plots(rows):
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    os.makedirs(OUT_DIR, exist_ok=True)
    dB = [row["dB"] for row in rows]
    dC = [row["dC"] for row in rows]
    hist_b = fill_hist("dB", "B_{3D}-B_{5D}", dB, 40, -0.12, 0.12, ROOT.kBlue + 2)
    hist_c = fill_hist("dC", "C_{3D}-C_{5D}", dC, 40, -0.10, 0.10, ROOT.kGreen + 2)
    style_hist(hist_b, "B_{3D} - B_{5D}", "Matched bins")
    style_hist(hist_c, "C_{3D} - C_{5D}", "Matched bins")
    canvas = ROOT.TCanvas("c_dBC", "dBC", 1100, 480)
    canvas.Divide(2, 1)
    canvas.cd(1)
    hist_b.Draw("hist")
    canvas.cd(2)
    hist_c.Draw("hist")
    canvas.Update()
    save_canvas(canvas, "delta_BC_hist")

    graph_b = graph_from_pairs([row["B5"] for row in rows], [row["B3"] for row in rows], ROOT.kBlue + 2, 20)
    graph_c = graph_from_pairs([row["C5"] for row in rows], [row["C3"] for row in rows], ROOT.kGreen + 2, 20)
    line_b = ROOT.TLine(-0.25, -0.25, 0.15, 0.15)
    line_c = ROOT.TLine(-0.12, -0.12, 0.12, 0.12)
    line_b.SetLineColor(ROOT.kRed + 1)
    line_c.SetLineColor(ROOT.kRed + 1)
    canvas = ROOT.TCanvas("c_sc", "scatter", 1100, 500)
    canvas.Divide(2, 1)
    canvas.cd(1)
    graph_b.SetTitle("Evaluated B;B nominal 5D;B new 3D BC+RC")
    graph_b.Draw("AP")
    line_b.Draw("same")
    canvas.cd(2)
    graph_c.SetTitle("Evaluated C;C nominal 5D;C new 3D BC+RC")
    graph_c.Draw("AP")
    line_c.Draw("same")
    canvas.Update()
    save_canvas(canvas, "BC_scatter")

    graph_y = graph_from_pairs([row["y"] for row in rows], dB, ROOT.kBlue + 2, 20)
    graph_pt = graph_from_pairs([row["pT"] for row in rows], dC, ROOT.kGreen + 2, 20)
    canvas = ROOT.TCanvas("c_kin", "kin", 1100, 480)
    canvas.Divide(2, 1)
    canvas.cd(1)
    graph_y.SetTitle("B difference vs y;y;B_{3D}-B_{5D}")
    graph_y.Draw("AP")
    canvas.cd(2)
    graph_pt.SetTitle("C difference vs p_{T};p_{T} (GeV);C_{3D}-C_{5D}")
    graph_pt.Draw("AP")
    canvas.Update()
    save_canvas(canvas, "delta_vs_kinematics")

    q2y_ids = list(range(1, 18))
    hist_med_b = ROOT.TH1D("medB", "Median |#DeltaB| and |#DeltaC| by Q^{2}-y bin", 17, 0.5, 17.5)
    hist_med_c = ROOT.TH1D("medC", "Median |#DeltaC|", 17, 0.5, 17.5)
    hist_med_b.SetDirectory(0)
    hist_med_c.SetDirectory(0)
    for q2y_bin in q2y_ids:
        subset = [row for row in rows if(row["q2y"] == q2y_bin)]
        hist_med_b.GetXaxis().SetBinLabel(q2y_bin, str(q2y_bin))
        if(len(subset) == 0):
            continue
        hist_med_b.SetBinContent(q2y_bin, float(np.median([abs(row["dB"]) for row in subset])))
        hist_med_c.SetBinContent(q2y_bin, float(np.median([abs(row["dC"]) for row in subset])))
    hist_med_b.SetFillColor(ROOT.kBlue + 2)
    hist_med_c.SetFillColor(ROOT.kGreen + 2)
    hist_med_b.SetBarWidth(0.4)
    hist_med_c.SetBarWidth(0.4)
    hist_med_c.SetBarOffset(0.4)
    style_hist(hist_med_b, "Q^{2}-y bin", "Median absolute difference")
    hist_med_b.SetMaximum(max(hist_med_b.GetMaximum(), hist_med_c.GetMaximum()) * 1.25)
    legend = ROOT.TLegend(0.62, 0.75, 0.88, 0.88)
    legend.AddEntry(hist_med_b, "median |#DeltaB|", "f")
    legend.AddEntry(hist_med_c, "median |#DeltaC|", "f")
    canvas = ROOT.TCanvas("c_q2y", "q2y", 1100, 460)
    hist_med_b.Draw("bar")
    hist_med_c.Draw("bar same")
    legend.Draw()
    canvas.Update()
    save_canvas(canvas, "median_abs_by_q2y")

    hist_a = fill_hist("aflux", "(A_{3D}/A_{5D})#times#Gamma_{#gamma}", [row["A3_over_A5_times_flux"] for row in rows], 40, 0.80, 2.20, ROOT.kBlue + 2)
    hist_shape = fill_hist("shape", "max |#Delta modulation|", [row["max_abs_dmod"] for row in rows], 40, 0.0, 0.12, ROOT.kGreen + 2)
    style_hist(hist_a, "(A_{3D}/A_{5D}) #times #Gamma_{#gamma}", "Matched bins")
    style_hist(hist_shape, "max_{#phi} |#Delta(1+B cos #phi + C cos 2#phi)|", "Matched bins")
    canvas = ROOT.TCanvas("c_conv", "conv", 1100, 480)
    canvas.Divide(2, 1)
    canvas.cd(1)
    hist_a.Draw("hist")
    canvas.cd(2)
    hist_shape.Draw("hist")
    canvas.Update()
    save_canvas(canvas, "A_convention_and_shape")

    hist_raw = fill_hist("raww", "log10 weight ratio", [math.log10(row["weight_ratio_phi0"]) for row in rows], 40, 2.4, 4.3, ROOT.kRed + 1)
    hist_aligned = fill_hist("align", "aligned relative weight", [100.0 * row["aligned_rel_phi0"] for row in rows], 40, -20.0, 110.0, ROOT.kBlue + 2)
    style_hist(hist_raw, "log_{10}(W_{3D}/W_{5D}) at #phi_{h}=0", "Matched bins")
    style_hist(hist_aligned, "flux-aligned (W_{3D}/W_{5D} - 1) at #phi_{h}=0 (%)", "Matched bins")
    canvas = ROOT.TCanvas("c_w", "weights", 1100, 480)
    canvas.Divide(2, 1)
    canvas.cd(1)
    hist_raw.Draw("hist")
    canvas.cd(2)
    hist_aligned.Draw("hist")
    canvas.Update()
    save_canvas(canvas, "weight_ratios")
    return {
        "delta_hist": os.path.join(OUT_DIR, "delta_BC_hist.png"),
        "scatter": os.path.join(OUT_DIR, "BC_scatter.png"),
        "kinematics": os.path.join(OUT_DIR, "delta_vs_kinematics.png"),
        "by_q2y": os.path.join(OUT_DIR, "median_abs_by_q2y.png"),
        "convention": os.path.join(OUT_DIR, "A_convention_and_shape.png"),
        "weights": os.path.join(OUT_DIR, "weight_ratios.png"),
    }


def row_brief(row, kind):
    return {
        "q2y": row["q2y"],
        "zpt": row["zpt"],
        "xB": round(row["xB"], 4),
        "y": round(row["y"], 4),
        "z": round(row["z"], 4),
        "pT": round(row["pT"], 4),
        "Q2": round(row["Q2"], 3),
        "value3": round(row[kind + "3"], 4),
        "value5": round(row[kind + "5"], 4),
        "delta": round(row["d" + kind], 4),
        "err3": round(row[kind + "err3"], 4),
        "err5": None if(row[kind + "err5"] is None) else round(row[kind + "err5"], 4),
        "abs_over_err3": None if(row[kind + "err3"] == 0.0) else round(abs(row["d" + kind]) / row[kind + "err3"], 2),
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    spline_3d = load_spline(FILE_3D)
    spline_5d = load_spline(FILE_5D)
    stored_3d, meta_3d = npz_map(NPZ_3D)
    stored_5d, meta_5d = npz_map(NPZ_5D)
    table_3d, failed_3d, json_keys = load_fit_table(JSON_3D, "Fit_Pars_from_3D_BC_RC_Bayesian")

    # Attach 5D parameter errors from the JSON whose B values reproduce the nominal npz targets.
    five_d_candidates = []
    for dirpath, dirnames, filenames in os.walk(REPO):
        if("Fit_Refinement" in dirpath):
            continue
        for filename in filenames:
            if(filename.endswith(".json") and ("Fit_Pars" in filename)):
                five_d_candidates.append(os.path.join(dirpath, filename))
    best_match = {"path": None, "n_match": -1, "table": {}}
    for candidate in five_d_candidates:
        try:
            with open(candidate) as handle:
                payload = json.load(handle)
        except Exception:
            continue
        if("Fit_Pars_from_5D_BC_RC_Bayesian" not in payload):
            continue
        table_5d, failed_5d, _keys = load_fit_table(candidate, "Fit_Pars_from_5D_BC_RC_Bayesian", require_chi2=False)
        n_match = 0
        for key, entry in table_5d.items():
            if(key not in stored_5d):
                continue
            if(abs(entry["B"] - stored_5d[key]["B"]) < 1.0e-6):
                n_match += 1
        print("5D JSON candidate", n_match, candidate)
        if(n_match > best_match["n_match"]):
            best_match = {"path": candidate, "n_match": n_match, "table": table_5d, "failed": failed_5d}

    rows = []
    eval_vs_train_b = []
    for key, fit in table_3d.items():
        if(key not in stored_5d):
            continue
        point = [fit["xB"], fit["y"], fit["z"], fit["pT"]]
        a3, b3, c3 = moments_at(spline_3d, point)
        a5, b5, c5 = moments_at(spline_5d, point)
        train_a3 = stored_3d[key]["A"]
        train_b3 = stored_3d[key]["B"]
        train_c3 = stored_3d[key]["C"]
        train_a5 = stored_5d[key]["A"]
        train_b5 = stored_5d[key]["B"]
        train_c5 = stored_5d[key]["C"]
        eval_vs_train_b.append(b3 - train_b3)
        flux = virtual_photon_flux_y(fit["Q2"], fit["y"])
        fit5 = best_match["table"].get(key)
        berr5 = None if(fit5 is None) else fit5["Berr"]
        cerr5 = None if(fit5 is None) else fit5["Cerr"]
        phi_grid = list(range(0, 360, 15))
        dmod = []
        raw_ratios = []
        aligned_rels = []
        for phi_deg in phi_grid:
            mod3 = modulation(b3, c3, phi_deg)
            mod5 = modulation(b5, c5, phi_deg)
            dmod.append(mod3 - mod5)
            weight3 = a3 * mod3
            weight5 = a5 * mod5
            raw_ratios.append(weight3 / weight5)
            aligned = (a3 * flux * mod3) / weight5
            aligned_rels.append(aligned - 1.0)
        row = {
            "q2y": fit["q2y"],
            "zpt": fit["zpt"],
            "Q2": fit["Q2"],
            "y": fit["y"],
            "z": fit["z"],
            "pT": fit["pT"],
            "xB": fit["xB"],
            "A3": a3,
            "A5": a5,
            "B3": b3,
            "B5": b5,
            "C3": c3,
            "C5": c5,
            "dB": b3 - b5,
            "dC": c3 - c5,
            "train_dB": train_b3 - train_b5,
            "train_dC": train_c3 - train_c5,
            "train_B3": train_b3,
            "train_B5": train_b5,
            "train_C3": train_c3,
            "train_C5": train_c5,
            "train_A3": train_a3,
            "train_A5": train_a5,
            "train_A_flux_product": (train_a3 / train_a5) * flux,
            "Berr3": fit["Berr"],
            "Cerr3": fit["Cerr"],
            "Berr5": berr5,
            "Cerr5": cerr5,
            "red": fit["red"],
            "flux": flux,
            "A3_over_A5": a3 / a5,
            "A3_over_A5_times_flux": (a3 / a5) * flux,
            "max_abs_dmod": max(abs(item) for item in dmod),
            "weight_ratio_phi0": raw_ratios[0],
            "aligned_rel_phi0": aligned_rels[0],
            "max_abs_aligned_rel": max(abs(item) for item in aligned_rels),
        }
        rows.append(row)

    unmatched_3d = []
    for key, fit in table_3d.items():
        if(key not in stored_5d):
            unmatched_3d.append({"q2y": fit["q2y"], "zpt": fit["zpt"], "y": round(fit["y"], 3), "z": round(fit["z"], 3), "pT": round(fit["pT"], 3)})
    unmatched_5d = []
    for key, stored in stored_5d.items():
        if(key not in table_3d):
            point = stored["point"]
            unmatched_5d.append({"xB": round(point[0], 4), "y": round(point[1], 4), "z": round(point[2], 4), "pT": round(point[3], 4)})

    reds = [fit["red"] for fit in table_3d.values()]
    poor = sorted(table_3d.values(), key=lambda item: item["red"], reverse=True)
    poor_rows = []
    for fit in poor:
        if(fit["red"] < 2.5):
            break
        poor_rows.append({
            "q2y": fit["q2y"],
            "zpt": fit["zpt"],
            "red": round(fit["red"], 3),
            "Chi2": round(fit["Chi2"], 2),
            "NDF": int(fit["NDF"]),
            "B": round(fit["B"], 4),
            "C": round(fit["C"], 4),
        })
    bin_932 = None
    for fit in table_3d.values():
        if((fit["q2y"] == 9) and (fit["zpt"] == 32)):
            bin_932 = {
                "red": round(fit["red"], 3),
                "Chi2": round(fit["Chi2"], 3),
                "NDF": int(fit["NDF"]),
                "B": round(fit["B"], 4),
                "C": round(fit["C"], 4),
                "A": fit["A"],
            }

    rel_b = [row["dB"] / row["B5"] for row in rows if(abs(row["B5"]) > REL_FLOOR)]
    rel_c = [row["dC"] / row["C5"] for row in rows if(abs(row["C5"]) > REL_FLOOR)]
    over_err_b = []
    for row in rows:
        if((row["Berr5"] is None) or (row["Berr3"] <= 0.0)):
            continue
        scale = math.sqrt(row["Berr3"] ** 2 + row["Berr5"] ** 2)
        over_err_b.append(abs(row["dB"]) / scale)
    largest_b = sorted(rows, key=lambda item: abs(item["dB"]), reverse=True)[:8]
    largest_c = sorted(rows, key=lambda item: abs(item["dC"]), reverse=True)[:8]
    largest_shape = sorted(rows, key=lambda item: item["max_abs_dmod"], reverse=True)[:8]

    by_q2y = []
    for q2y_bin in range(1, 18):
        subset = [row for row in rows if(row["q2y"] == q2y_bin)]
        if(len(subset) == 0):
            continue
        by_q2y.append({
            "q2y": q2y_bin,
            "n": len(subset),
            "median_abs_dB": round(float(np.median([abs(row["dB"]) for row in subset])), 4),
            "median_abs_dC": round(float(np.median([abs(row["dC"]) for row in subset])), 4),
            "max_abs_dB": round(float(np.max([abs(row["dB"]) for row in subset])), 4),
        })

    convention_check = None
    norm_example = None
    try:
        sys.path.append(REPO)
        from Cross_Section_Normalization import Cross_Section_Normalization
        sys.path.remove(REPO)
        class quiet_args:
            verbose = False
        ratio_5d_no_flux = []
        ratio_5d_with_flux = []
        for key, fit in best_match["table"].items():
            if(key not in stored_5d):
                continue
            _histo, area, luminosity, flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=fit["q2y"], z_pT_Bin=fit["zpt"], args_in=quiet_args, verbose_in=False, apply_beam_corrections=True)
            raw_a = fit["A"]
            ratio_5d_no_flux.append(stored_5d[key]["A"] * area * luminosity / raw_a)
            ratio_5d_with_flux.append(stored_5d[key]["A"] * area * luminosity * flux / raw_a)
        ratio_3d_with_flux = []
        ratio_3d_no_flux = []
        for key, fit in table_3d.items():
            if(key not in stored_3d):
                continue
            _histo, area, luminosity, flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=fit["q2y"], z_pT_Bin=fit["zpt"], args_in=quiet_args, verbose_in=False, apply_beam_corrections=True)
            raw_a = fit["A"]
            ratio_3d_no_flux.append(stored_3d[key]["A"] * area * luminosity / raw_a)
            ratio_3d_with_flux.append(stored_3d[key]["A"] * area * luminosity * flux / raw_a)
        convention_check = {
            "five_d_stored_over_area_lumi": summarize_abs(ratio_5d_no_flux),
            "five_d_stored_over_area_lumi_flux": summarize_abs(ratio_5d_with_flux),
            "three_d_stored_over_area_lumi": summarize_abs(ratio_3d_no_flux),
            "three_d_stored_over_area_lumi_flux": summarize_abs(ratio_3d_with_flux),
        }
        _histo, area_on, lumi_on, flux_on = Cross_Section_Normalization(Histo=None, Q2_y_Bin=9, z_pT_Bin=32, args_in=quiet_args, verbose_in=False, apply_beam_corrections=True)
        _histo, area_off, lumi_off, flux_off = Cross_Section_Normalization(Histo=None, Q2_y_Bin=9, z_pT_Bin=32, args_in=quiet_args, verbose_in=False, apply_beam_corrections=False)
        norm_example = {
            "q2y": 9,
            "zpt": 32,
            "bin_area": area_on,
            "luminosity_beam_on": lumi_on,
            "luminosity_beam_off": lumi_off,
            "photon_flux": flux_on,
            "beam_lumi_ratio": lumi_on / lumi_off,
            "flux_matches_formula": abs(flux_on - flux_off) < 1.0e-9,
        }
    except Exception as exc:
        norm_example = {"error": str(exc)}

    root_counts = None
    try:
        import ROOT
        root_file = ROOT.TFile.Open(ROOT_FILE, "READ")
        names = [key.GetName() for key in root_file.GetListOfKeys()]
        root_file.Close()
        def count_names(token, family):
            return sum((token in name) and (family in name) and ("Bin_All" not in name) and ("Normalized" not in name) and ("AsymErr" not in name) for name in names)
        root_counts = {
            "n_keys": len(names),
            "phi_Bayesian": count_names("(MultiDim_3D_Histo)", "_(Bayesian)_"),
            "phi_RC": count_names("(MultiDim_3D_Histo)", "_(RC_Bayesian)_"),
            "phi_BC_RC": count_names("(MultiDim_3D_Histo)", "_(BC_RC_Bayesian)_"),
            "fit_Bayesian": count_names("(Fit_Function)", "_(Bayesian)_"),
            "fit_RC": count_names("(Fit_Function)", "_(RC_Bayesian)_"),
            "fit_BC_RC": count_names("(Fit_Function)", "_(BC_RC_Bayesian)_"),
        }
    except Exception as exc:
        root_counts = {"error": str(exc)}

    plots = write_plots(rows)
    phi_pages = render_phi_pages()

    csv_path = os.path.join(OUT_DIR, "matched_bins.csv")
    fieldnames = ["q2y", "zpt", "Q2", "xB", "y", "z", "pT", "A3", "A5", "flux", "A3_over_A5_times_flux", "B3", "B5", "dB", "Berr3", "Berr5", "C3", "C5", "dC", "Cerr3", "Cerr5", "max_abs_dmod", "weight_ratio_phi0", "aligned_rel_phi0", "red"]
    with open(csv_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row[name] for name in fieldnames})

    summary = {
        "n_json_3d": len(table_3d),
        "n_failed_3d": len(failed_3d),
        "failed_3d": failed_3d,
        "json_keys": json_keys,
        "red_median": float(np.median(reds)),
        "red_p95": percentile(reds, 95),
        "n_red_gt3": int(sum(item > 3.0 for item in reds)),
        "n_red_gt5": int(sum(item > 5.0 for item in reds)),
        "poor": poor_rows,
        "bin_932": bin_932,
        "meta_3d": meta_3d,
        "meta_5d": meta_5d,
        "n_eval_3d": spline_3d["A"]["n"],
        "n_eval_5d": spline_5d["A"]["n"],
        "kernel_A_3d": spline_3d["A"]["kernel"],
        "kernel_B_3d": spline_3d["B"]["kernel"],
        "log_A_both": spline_3d["A"]["log_space"] and spline_5d["A"]["log_space"],
        "n_matched": len(rows),
        "n_unmatched_3d": len(unmatched_3d),
        "n_unmatched_5d": len(unmatched_5d),
        "unmatched_3d": unmatched_3d,
        "B": summarize_abs([row["dB"] for row in rows]),
        "C": summarize_abs([row["dC"] for row in rows]),
        "train_B": summarize_abs([row["train_dB"] for row in rows]),
        "train_C": summarize_abs([row["train_dC"] for row in rows]),
        "train_A_flux_product": summarize_abs([row["train_A_flux_product"] for row in rows]),
        "frac_abs_train_dB_gt_0p05": float(np.mean([abs(row["train_dB"]) > 0.05 for row in rows])),
        "frac_abs_train_dB_gt_0p10": float(np.mean([abs(row["train_dB"]) > 0.10 for row in rows])),
        "frac_abs_train_dC_gt_0p05": float(np.mean([abs(row["train_dC"]) > 0.05 for row in rows])),
        "frac_abs_train_dC_gt_0p10": float(np.mean([abs(row["train_dC"]) > 0.10 for row in rows])),
        "largest_train_B": [{
            "q2y": row["q2y"], "zpt": row["zpt"], "y": round(row["y"], 3), "z": round(row["z"], 3), "pT": round(row["pT"], 3),
            "B3": round(row["train_B3"], 4), "B5": round(row["train_B5"], 4), "dB": round(row["train_dB"], 4),
            "Berr3": round(row["Berr3"], 4), "Berr5": None if(row["Berr5"] is None) else round(row["Berr5"], 4),
        } for row in sorted(rows, key=lambda item: abs(item["train_dB"]), reverse=True)[:8]],
        "largest_train_C": [{
            "q2y": row["q2y"], "zpt": row["zpt"], "y": round(row["y"], 3), "z": round(row["z"], 3), "pT": round(row["pT"], 3),
            "C3": round(row["train_C3"], 4), "C5": round(row["train_C5"], 4), "dC": round(row["train_dC"], 4),
            "Cerr3": round(row["Cerr3"], 4), "Cerr5": None if(row["Cerr5"] is None) else round(row["Cerr5"], 4),
        } for row in sorted(rows, key=lambda item: abs(item["train_dC"]), reverse=True)[:8]],
        "frac_abs_dB_gt_0p05": float(np.mean([abs(row["dB"]) > 0.05 for row in rows])),
        "frac_abs_dB_gt_0p10": float(np.mean([abs(row["dB"]) > 0.10 for row in rows])),
        "frac_abs_dC_gt_0p05": float(np.mean([abs(row["dC"]) > 0.05 for row in rows])),
        "frac_abs_dC_gt_0p10": float(np.mean([abs(row["dC"]) > 0.10 for row in rows])),
        "n_rel_B": len(rel_b),
        "median_rel_B": None if(len(rel_b) == 0) else float(np.median(rel_b)),
        "median_abs_rel_B": None if(len(rel_b) == 0) else float(np.median(np.abs(rel_b))),
        "n_rel_C": len(rel_c),
        "median_abs_rel_C": None if(len(rel_c) == 0) else float(np.median(np.abs(rel_c))),
        "median_abs_dB_over_combined_err": None if(len(over_err_b) == 0) else float(np.median(over_err_b)),
        "p95_abs_dB_over_combined_err": None if(len(over_err_b) == 0) else percentile(over_err_b, 95),
        "A_flux_product": summarize_abs([row["A3_over_A5_times_flux"] for row in rows]),
        "A_ratio": summarize_abs([row["A3_over_A5"] for row in rows]),
        "flux": summarize_abs([row["flux"] for row in rows]),
        "inv_flux_median": float(np.median([1.0 / row["flux"] for row in rows])),
        "shape": summarize_abs([row["max_abs_dmod"] for row in rows]),
        "aligned_rel_phi0": summarize_abs([row["aligned_rel_phi0"] for row in rows]),
        "aligned_rel_maxphi": summarize_abs([row["max_abs_aligned_rel"] for row in rows]),
        "raw_weight_ratio_phi0": summarize_abs([row["weight_ratio_phi0"] for row in rows]),
        "eval_minus_train_B_rms": float(np.sqrt(np.mean(np.square(eval_vs_train_b)))),
        "largest_B": [row_brief(row, "B") for row in largest_b],
        "largest_C": [row_brief(row, "C") for row in largest_c],
        "largest_shape": [{
            "q2y": row["q2y"], "zpt": row["zpt"], "y": round(row["y"], 3), "z": round(row["z"], 3), "pT": round(row["pT"], 3),
            "max_abs_dmod": round(row["max_abs_dmod"], 4), "dB": round(row["dB"], 4), "dC": round(row["dC"], 4),
        } for row in largest_shape],
        "by_q2y": by_q2y,
        "five_d_error_source": best_match["path"],
        "five_d_error_matches": best_match["n_match"],
        "norm_example": norm_example,
        "convention_check": convention_check,
        "root_counts": root_counts,
        "plots": plots,
        "n_phi_pages": len(phi_pages),
        "before_932": BEFORE_932 if(os.path.isfile(BEFORE_932)) else None,
        "csv": csv_path,
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as handle:
        json.dump(summary, handle, indent=2)
    with open(os.path.join(OUT_DIR, "phi_pages.json"), "w") as handle:
        json.dump(phi_pages, handle)
    print("matched", len(rows), "phi_pages", len(phi_pages))
    print("red median", summary["red_median"], "p95", summary["red_p95"], "gt3", summary["n_red_gt3"])
    print("bin 9,32", bin_932)
    print("B eval", summary["B"])
    print("C eval", summary["C"])
    print("B train", summary["train_B"])
    print("C train", summary["train_C"])
    print("train A flux", summary["train_A_flux_product"])
    print("A flux product", summary["A_flux_product"])
    print("raw weight ratio", summary["raw_weight_ratio_phi0"])
    print("aligned rel", summary["aligned_rel_phi0"])
    print("shape", summary["shape"])
    print("5D error source", best_match["n_match"], best_match["path"])
    print("norm", norm_example)
    print("convention", convention_check)
    print("root", root_counts)
    print("poor", poor_rows[:8])
    print("largest B", summary["largest_B"][:5])
    print("unmatched 3D", len(unmatched_3d), "5D stored-only", len(unmatched_5d))


if(__name__ == "__main__"):
    main()
