#!/usr/bin/env python3
# Compare the raw-A spline, after the usual cross-section factors, with the spline that was fit to already-normalized A.

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
OUT_DIR = os.path.join(REVIEW, "rawA_comparison")
JSON_3D = os.path.join(REPO, "Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Unfolded_Simple_3D_Final_Thesis_Bank_rho0_new_acc020_Zeroth_Order_Full.json")
FILE_RAW = os.path.join(REPO, "Prepare_Next_Iteration", "acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt")
FILE_NORM = os.path.join(REPO, "Prepare_Next_Iteration", "acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt")
CONVERSION_FACTOR = 0.0502731
REL_FLOOR_FRACTION = 0.02


def array_block(text, name):
    match = re.search(r"const (?:double|int) " + name + r"\[[^\]]*\](?:\[[^\]]*\])?\s*=\s*\{(.*?)\};", text, re.S)
    if(match is None):
        raise RuntimeError("Missing " + name)
    return [float(item) for item in re.findall(r"[-+]?(?:\d+\.\d*|\d+)(?:[eE][-+]?\d+)?", match.group(1))]


def int_const(text, name):
    return int(re.search(r"const int " + name + r"\s*=\s*(\d+);", text).group(1))


def load_piece(text, tag):
    count = int_const(text, "n_fit_par_" + tag)
    ndim = int_const(text, "ndim_fit_par_" + tag)
    npoly = int_const(text, "n_poly_fit_par_" + tag)
    centers = array_block(text, "centers_fit_par_" + tag)
    coeffs = array_block(text, "coeffs_fit_par_" + tag)
    shift = array_block(text, "shift_fit_par_" + tag)
    scale = array_block(text, "scale_fit_par_" + tag)
    powers = array_block(text, "powers_fit_par_" + tag)
    kernel = re.search(r"const std::string kernel_fit_par_" + tag + r"\s*=\s*\"([^\"]+)\";", text).group(1)
    epsilon = float(re.search(r"const double epsilon_fit_par_" + tag + r"\s*=\s*([0-9eE.+\-]+);", text).group(1))
    log_space = re.search(r"const bool log_space_fit_par_" + tag + r"\s*=\s*(true|false);", text).group(1) == "true"
    return {
        "n": count,
        "ndim": ndim,
        "npoly": npoly,
        "centers": [centers[i * ndim:(i + 1) * ndim] for i in range(count)],
        "coeffs": coeffs,
        "shift": shift,
        "scale": scale,
        "powers": [powers[i * ndim:(i + 1) * ndim] for i in range(npoly)],
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
    raise RuntimeError(kernel)


def evaluate_piece(piece, point):
    eps = piece["epsilon"]
    ndim = piece["ndim"]
    total = 0.0
    count = piece["n"]
    for index in range(count):
        radius2 = 0.0
        center = piece["centers"][index]
        for axis in range(ndim):
            diff = eps * point[axis] - eps * center[axis]
            radius2 += diff * diff
        total += piece["coeffs"][index] * kernel_value(math.sqrt(radius2), piece["kernel"])
    xhat = [(point[axis] - piece["shift"][axis]) / piece["scale"][axis] for axis in range(ndim)]
    for poly_index in range(piece["npoly"]):
        mono = 1.0
        power = piece["powers"][poly_index]
        for axis in range(ndim):
            powv = int(power[axis])
            if(powv != 0):
                mono *= xhat[axis] ** powv
        total += piece["coeffs"][count + poly_index] * mono
    if(piece["log_space"]):
        return math.exp(total)
    return total


def bin_center(q2y_bin, zpt_bin):
    q2_max, q2_min, y_max, y_min = Full_Bin_Definition_Array["Q2-y=%s, Q2-y" % q2y_bin]
    z_max, z_min, pt_max, pt_min = Full_Bin_Definition_Array["Q2-y=%s, z-pT=%s" % (q2y_bin, zpt_bin)]
    q2_mid = (float(q2_max) + float(q2_min)) / 2.0
    y_mid = (float(y_max) + float(y_min)) / 2.0
    z_mid = (float(z_max) + float(z_min)) / 2.0
    pt_mid = (float(pt_max) + float(pt_min)) / 2.0
    xB_mid = CONVERSION_FACTOR * (q2_mid / y_mid)
    return q2_mid, y_mid, z_mid, pt_mid, xB_mid


def summarize(values):
    arr = np.asarray(values, dtype=float)
    abs_arr = np.abs(arr)
    return {
        "n": int(arr.size),
        "median": float(np.median(arr)),
        "p16": float(np.percentile(arr, 16)),
        "p84": float(np.percentile(arr, 84)),
        "p95_abs": float(np.percentile(abs_arr, 95)),
        "max_abs": float(np.max(abs_arr)),
        "median_abs": float(np.median(abs_arr)),
    }


def save_canvas(canvas, stem):
    canvas.SaveAs(os.path.join(OUT_DIR, stem + ".png"))
    canvas.SaveAs(os.path.join(OUT_DIR, stem + ".pdf"))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    raw_text = open(FILE_RAW).read()
    norm_text = open(FILE_NORM).read()
    raw_A = load_piece(raw_text, "a")
    norm_A = load_piece(norm_text, "a")
    if((not raw_A["log_space"]) or (not norm_A["log_space"])):
        raise RuntimeError("Both A evaluators are expected in log space")
    sys.path.append(REPO)
    from Cross_Section_Normalization import Cross_Section_Normalization
    sys.path.remove(REPO)
    class quiet_args:
        verbose = False
    with open(JSON_3D) as handle:
        payload = json.load(handle)
    fit_dict = payload["Fit_Pars_from_3D_BC_RC_Bayesian"]
    rows = []
    for key_str, entry in fit_dict.items():
        match = re.fullmatch(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", str(key_str).strip())
        if(match is None):
            continue
        q2y_bin = int(match.group(1))
        zpt_bin = int(match.group(2))
        q2_mid, y_mid, z_mid, pt_mid, xB_mid = bin_center(q2y_bin, zpt_bin)
        point = [xB_mid, y_mid, z_mid, pt_mid]
        a_raw = evaluate_piece(raw_A, point)
        a_norm = evaluate_piece(norm_A, point)
        _histo, area, luminosity, flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y_bin, z_pT_Bin=zpt_bin, args_in=quiet_args, verbose_in=False, apply_beam_corrections=True)
        scale = float(area) * float(luminosity) * float(flux)
        a_aligned = a_raw / scale
        rows.append({
            "q2y": q2y_bin,
            "zpt": zpt_bin,
            "Q2": q2_mid,
            "y": y_mid,
            "z": z_mid,
            "pT": pt_mid,
            "A_raw": a_raw,
            "A_norm": a_norm,
            "A_aligned": a_aligned,
            "scale": scale,
            "delta": a_aligned - a_norm,
            "json_A": float(entry["Fit_Par_A"]),
        })
    median_abs_norm = float(np.median([abs(row["A_norm"]) for row in rows]))
    rel_floor = REL_FLOOR_FRACTION * median_abs_norm
    rel_rows = []
    for row in rows:
        if(abs(row["A_norm"]) > rel_floor):
            row["rel"] = row["delta"] / row["A_norm"]
            rel_rows.append(row)
        else:
            row["rel"] = None
    by_q2y = []
    for q2y_bin in range(1, 18):
        subset = [row for row in rel_rows if(row["q2y"] == q2y_bin)]
        if(len(subset) == 0):
            continue
        by_q2y.append({
            "q2y": q2y_bin,
            "n": len(subset),
            "median_abs_rel": float(np.median([abs(row["rel"]) for row in subset])),
            "max_abs_rel": float(np.max([abs(row["rel"]) for row in subset])),
        })
    largest = sorted(rel_rows, key=lambda item: abs(item["rel"]), reverse=True)[:8]
    summary = {
        "n": len(rows),
        "n_rel": len(rel_rows),
        "rel_floor": rel_floor,
        "median_abs_A_norm": median_abs_norm,
        "delta": summarize([row["delta"] for row in rows]),
        "rel": summarize([row["rel"] for row in rel_rows]),
        "by_q2y": by_q2y,
        "largest_rel": [{
            "q2y": row["q2y"], "zpt": row["zpt"], "y": round(row["y"], 3), "z": round(row["z"], 3), "pT": round(row["pT"], 3),
            "rel": row["rel"], "A_aligned": row["A_aligned"], "A_norm": row["A_norm"],
        } for row in largest],
        "raw_over_json_median": float(np.median([row["A_raw"] / row["json_A"] for row in rows])),
        "log_space_both": True,
        "kernels": {"raw": raw_A["kernel"], "norm": norm_A["kernel"]},
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as handle:
        json.dump(summary, handle, indent=2)
    with open(os.path.join(OUT_DIR, "matched_A.csv"), "w", newline="") as handle:
        fields = ["q2y", "zpt", "Q2", "y", "z", "pT", "A_raw", "scale", "A_aligned", "A_norm", "delta", "rel", "json_A"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row[name] for name in fields})

    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    rel_percent = [100.0 * row["rel"] for row in rel_rows]
    hist = ROOT.TH1D("relA", "(A_{raw}/scale - A_{norm})/A_{norm}", 40, -90.0, 90.0)
    hist.SetDirectory(0)
    for value in rel_percent:
        hist.Fill(value)
    hist.SetLineColor(ROOT.kBlue + 2)
    hist.SetFillColor(ROOT.kBlue + 2)
    hist.GetXaxis().SetTitle("100 #times (A_{aligned} - A_{normalized}) / A_{normalized} (%)")
    hist.GetYaxis().SetTitle("Bins")
    hist.SetStats(0)
    canvas = ROOT.TCanvas("c_rel", "rel", 900, 520)
    hist.Draw("hist")
    canvas.Update()
    save_canvas(canvas, "relative_difference")

    graph = ROOT.TGraph(len(rows))
    for index, row in enumerate(rows):
        graph.SetPoint(index, row["A_norm"], row["A_aligned"])
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.7)
    graph.SetMarkerColor(ROOT.kBlue + 2)
    graph.SetTitle("Common normalized scale;A from normalized spline;A from raw spline / (area #times L #times #Gamma_{#gamma})")
    xmin = min(row["A_norm"] for row in rows)
    xmax = max(row["A_norm"] for row in rows)
    line = ROOT.TLine(xmin, xmin, xmax, xmax)
    line.SetLineColor(ROOT.kRed + 1)
    canvas = ROOT.TCanvas("c_sc", "scatter", 800, 700)
    graph.Draw("AP")
    line.Draw("same")
    canvas.Update()
    save_canvas(canvas, "aligned_vs_normalized")

    hist_q = ROOT.TH1D("q2y", "Median |relative difference| by Q^{2}-y", 17, 0.5, 17.5)
    hist_q.SetDirectory(0)
    for item in by_q2y:
        hist_q.SetBinContent(item["q2y"], 100.0 * item["median_abs_rel"])
        hist_q.GetXaxis().SetBinLabel(item["q2y"], str(item["q2y"]))
    hist_q.SetFillColor(ROOT.kBlue + 2)
    hist_q.GetXaxis().SetTitle("Q^{2}-y bin")
    hist_q.GetYaxis().SetTitle("Median |relative difference| (%)")
    hist_q.SetStats(0)
    canvas = ROOT.TCanvas("c_q", "q2y", 1000, 480)
    hist_q.Draw("bar")
    canvas.Update()
    save_canvas(canvas, "median_abs_rel_by_q2y")
    print("n", summary["n"], "rel", summary["rel"])
    print("delta", summary["delta"])
    print("floor", rel_floor, "largest", summary["largest_rel"][:3])
    print("raw/json", summary["raw_over_json_median"])


if(__name__ == "__main__"):
    main()
