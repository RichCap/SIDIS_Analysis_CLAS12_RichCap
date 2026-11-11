# Read-only review of the copied no_valerii_knockout 3D Bayesian histograms.
# Does not unfold, does not edit shared guides, and does not write the ROOT file.
import importlib.util
import json
import math
import os
import sys

import numpy as np

DEST = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(DEST, "fit_copy.root")
BEFORE_JSON = os.path.join(DEST, "fit_before.json")
NOMINAL_JSON = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/fits/spline/nominal/nominal/fit.json"
MANUAL_PATH = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
SPLINE_PATH = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
FAMILY = "Bayesian"
JSON_KEY = "Fit_Pars_from_3D_Bayesian"


def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def load_json(path):
    with open(path, "r") as handle:
        return json.load(handle)


def bin_numbers(bin_name):
    # (Q2_y_Bin_1)-(z_pT_Bin_8) -> ("1", "8")
    q2y = bin_name.split("Q2_y_Bin_")[1].split(")")[0]
    zpt = bin_name.split("z_pT_Bin_")[1].split(")")[0]
    return q2y, zpt


def window_width(limits):
    if(not limits):
        return None
    return float(max(limits) - min(limits))


def excludes(value, limits):
    if((value is None) or (not limits)):
        return False
    return (float(value) < min(limits) - 1.0e-9) or (float(value) > max(limits) + 1.0e-9)


def free_cosine(centers, contents, errors):
    rows = []
    ys = []
    ws = []
    for phi, content, error in zip(centers, contents, errors):
        if(not (error > 0.0)):
            continue
        rad = float(phi) * math.pi / 180.0
        rows.append([1.0, math.cos(rad), math.cos(2.0 * rad)])
        ys.append(float(content))
        ws.append(1.0 / (float(error) * float(error)))
    if(len(ys) < 4):
        return None
    design = np.asarray(rows, dtype=float)
    yvec = np.asarray(ys, dtype=float)
    weight = np.asarray(ws, dtype=float)
    xtw = design.T * weight
    normal = xtw @ design
    try:
        beta = np.linalg.solve(normal, xtw @ yvec)
        cov = np.linalg.inv(normal)
    except np.linalg.LinAlgError:
        return None
    amplitude = float(beta[0])
    if(not (abs(amplitude) > 0.0)):
        return None
    cosine_b = float(beta[1] / amplitude)
    cosine_c = float(beta[2] / amplitude)
    # B = P/A and C = Q/A. Propagate the linear covariance.
    grad_b = np.array([-beta[1] / (amplitude * amplitude), 1.0 / amplitude, 0.0])
    grad_c = np.array([-beta[2] / (amplitude * amplitude), 0.0, 1.0 / amplitude])
    b_var = float(grad_b @ cov @ grad_b)
    c_var = float(grad_c @ cov @ grad_c)
    a_var = float(cov[0, 0])
    residual = yvec - design @ beta
    chi2 = float(np.sum(weight * residual * residual))
    ndf = int(len(ys) - 3)
    return {
        "A": amplitude,
        "A_ERR": float(math.sqrt(a_var)) if(a_var > 0.0) else 0.0,
        "B": cosine_b,
        "B_ERR": float(math.sqrt(b_var)) if(b_var > 0.0) else 0.0,
        "C": cosine_c,
        "C_ERR": float(math.sqrt(c_var)) if(c_var > 0.0) else 0.0,
        "Chi2": chi2,
        "NDF": ndf,
        "n_used": int(len(ys)),
    }


def curve_chi2(centers, contents, errors, amplitude, cosine_b, cosine_c):
    chi2 = 0.0
    used = 0
    worst_pull = 0.0
    worst_phi = None
    worst_share = 0.0
    pulls = []
    for phi, content, error in zip(centers, contents, errors):
        if(not (error > 0.0)):
            continue
        rad = float(phi) * math.pi / 180.0
        model = amplitude * (1.0 + cosine_b * math.cos(rad) + cosine_c * math.cos(2.0 * rad))
        pull = (float(content) - model) / float(error)
        chi2 += pull * pull
        used += 1
        pulls.append((abs(pull), float(phi), pull))
    if((used == 0) or (not (chi2 > 0.0))):
        return chi2, used, None
    pulls.sort(reverse=True)
    worst_pull_abs, worst_phi, worst_signed = pulls[0]
    worst_share = (worst_pull_abs * worst_pull_abs) / chi2
    spike = None
    if((worst_pull_abs >= 5.0) and (worst_share >= 0.25)):
        spike = {
            "pull": worst_signed,
            "phi": worst_phi,
            "fraction": worst_share,
        }
    return chi2, used, spike


def select_guide(guide, q2y, zpt):
    if(guide is None):
        return None
    for key in ((q2y, zpt, "3D"), (q2y, zpt)):
        if(key in guide):
            return guide[key]
    return None


def histo_family(name):
    parts = str(name).split(")_(")
    if(len(parts) < 2):
        return ""
    return parts[1]


def main():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.TH1.AddDirectory(False)
    before = load_json(BEFORE_JSON)[JSON_KEY]
    nominal = load_json(NOMINAL_JSON)[JSON_KEY]
    manual = load_module(MANUAL_PATH, "manual_phi_init_review").special_fit_parameters_set
    spline = load_module(SPLINE_PATH, "spline_phi_init_review").special_fit_parameters_set
    tfile = ROOT.TFile.Open(ROOT_PATH, "READ")
    if((tfile is None) or tfile.IsZombie()):
        print("Could not open", ROOT_PATH)
        sys.exit(1)
    families = {}
    histos = {}
    functions = {}
    for key in tfile.GetListOfKeys():
        name = key.GetName()
        if(name in ["TVectorT<double>", "TVectorD"]):
            continue
        if(name.startswith("TVector") or name.startswith("TList")):
            continue
        family = histo_family(name)
        if("MultiDim_3D_Histo" in name):
            families[family] = families.get(family, 0) + 1
        if(("MultiDim_5D_Histo" in name) or ("MultiDim_5D" in name)):
            families["5D_object"] = families.get("5D_object", 0) + 1
        if("(Bin)" in name):
            families["Bin_token"] = families.get("Bin_token", 0) + 1
        if(("MultiDim_3D_Histo" in name) and (family == FAMILY) and ("Bin_All" not in name) and ("_(Normalized)" not in name) and ("_AsymErr" not in name) and ("MultiDim_z_pT_Bin_Y_bin_phi_t" in name)):
            histos[name] = key.ReadObj()
        if(("Fit_Function" in name) and (family == FAMILY) and ("Bin_All" not in name) and ("MultiDim_z_pT_Bin_Y_bin_phi_t" in name)):
            functions[name] = key.ReadObj()
    rows = []
    b_widths = []
    c_widths = []
    for name in sorted(histos):
        histo = histos[name]
        bin_name = "(" + name.split(")_(")[3] + ")-(" + name.split(")_(")[4] + ")"
        q2y, zpt = bin_numbers(bin_name)
        fit_name = name.replace("MultiDim_3D_Histo", "Fit_Function")
        function = functions.get(fit_name)
        nbins = int(histo.GetNbinsX())
        centers = []
        contents = []
        errors = []
        filled_low = None
        filled_high = None
        nonempty = 0
        for ibin in range(1, nbins + 1):
            content = float(histo.GetBinContent(ibin))
            error = float(histo.GetBinError(ibin))
            center = float(histo.GetXaxis().GetBinCenter(ibin))
            low = float(histo.GetXaxis().GetBinLowEdge(ibin))
            high = float(histo.GetXaxis().GetBinUpEdge(ibin))
            centers.append(center)
            contents.append(content)
            errors.append(error)
            if(content != 0.0):
                nonempty += 1
                if(filled_low is None):
                    filled_low = low
                filled_high = high
        phi_low = None
        phi_high = None
        if(function is not None):
            phi_low = float(function.GetXmin())
            phi_high = float(function.GetXmax())
        in_centers = []
        in_contents = []
        in_errors = []
        bins_in_tf1 = 0
        positive_error = 0
        zero_error = 0
        for center, content, error, ibin in zip(centers, contents, errors, range(1, nbins + 1)):
            low = float(histo.GetXaxis().GetBinLowEdge(ibin))
            high = float(histo.GetXaxis().GetBinUpEdge(ibin))
            inside = False
            if((phi_low is not None) and (phi_high is not None)):
                inside = (low >= phi_low - 0.01) and (high <= phi_high + 0.01)
            if(inside):
                bins_in_tf1 += 1
                in_centers.append(center)
                in_contents.append(content)
                in_errors.append(error)
                if(error > 0.0):
                    positive_error += 1
                else:
                    zero_error += 1
        stored = before.get(bin_name, {})
        nom = nominal.get(bin_name, {})
        cosine = free_cosine(in_centers, in_contents, in_errors)
        spline_key = select_guide(spline, q2y, zpt)
        manual_key = select_guide(manual, q2y, zpt)
        spline_b = window_width(None if(spline_key is None) else spline_key.get("B_limits"))
        spline_c = window_width(None if(spline_key is None) else spline_key.get("C_limits"))
        if(spline_b is not None):
            b_widths.append(spline_b)
        if(spline_c is not None):
            c_widths.append(spline_c)
        stored_chi2 = None
        spike = None
        if(stored):
            stored_chi2, used_count, spike = curve_chi2(in_centers, in_contents, in_errors, stored.get("Fit_Par_A"), stored.get("Fit_Par_B"), stored.get("Fit_Par_C"))
        problems = []
        if(not stored):
            problems.append("missing_json")
        if(function is None):
            problems.append("missing_tf1")
        if(nonempty == 0):
            problems.append("empty_histogram")
        if((phi_low is None) or (abs(phi_low - filled_low) > 0.1) or (abs(phi_high - filled_high) > 0.1)):
            problems.append("range_mismatch")
        for par_name in ["A", "B", "C"]:
            err = stored.get("Fit_Par_%s_ERR" % par_name)
            val = stored.get("Fit_Par_%s" % par_name)
            if((err is None) or (val is None) or (not math.isfinite(float(err))) or (not math.isfinite(float(val)))):
                problems.append("nonfinite_%s" % par_name)
            elif(float(err) == 0.0):
                problems.append("zero_error_%s" % par_name)
            elif(float(err) < 1.0e-6):
                problems.append("collapsed_%s" % par_name)
        if(stored.get("Fit_Par_B") is not None):
            if(abs(float(stored["Fit_Par_B"])) >= 0.999):
                problems.append("boundary_B")
        if(stored.get("Fit_Par_C") is not None):
            if(abs(float(stored["Fit_Par_C"])) >= 0.999):
                problems.append("boundary_C")
        chi2 = stored.get("Chi2")
        ndf = stored.get("NDF")
        if((chi2 is None) or (ndf is None) or (float(ndf) <= 0.0) or (not math.isfinite(float(chi2)))):
            problems.append("bad_chi2")
        off_cosine = False
        if((cosine is not None) and (stored.get("Fit_Par_B") is not None)):
            db = abs(float(stored["Fit_Par_B"]) - cosine["B"])
            dc = abs(float(stored["Fit_Par_C"]) - cosine["C"])
            b_scale = max(float(stored.get("Fit_Par_B_ERR") or 0.0), cosine["B_ERR"], 1.0e-4)
            c_scale = max(float(stored.get("Fit_Par_C_ERR") or 0.0), cosine["C_ERR"], 1.0e-4)
            chi_gap = float(stored.get("Chi2") or 0.0) - cosine["Chi2"]
            if((chi_gap > 0.5) and ((db > max(0.5 * b_scale, 0.01)) or (dc > max(0.5 * c_scale, 0.01)))):
                off_cosine = True
                problems.append("off_cosine")
        if(spike is not None):
            problems.append("isolated_spike")
        manual_excludes_b = False
        manual_excludes_c = False
        if((cosine is not None) and (manual_key is not None)):
            manual_excludes_b = excludes(cosine["B"], manual_key.get("B_limits"))
            manual_excludes_c = excludes(cosine["C"], manual_key.get("C_limits"))
        dB = None
        dC = None
        dB_stat = None
        dC_stat = None
        if((stored.get("Fit_Par_B") is not None) and (nom.get("Fit_Par_B") is not None)):
            dB = float(stored["Fit_Par_B"]) - float(nom["Fit_Par_B"])
            dC = float(stored["Fit_Par_C"]) - float(nom["Fit_Par_C"])
            if(float(stored.get("Fit_Par_B_ERR") or 0.0) > 0.0):
                dB_stat = dB / float(stored["Fit_Par_B_ERR"])
            if(float(stored.get("Fit_Par_C_ERR") or 0.0) > 0.0):
                dC_stat = dC / float(stored["Fit_Par_C_ERR"])
        reduced = None
        if((ndf is not None) and (float(ndf) > 0.0) and (chi2 is not None)):
            reduced = float(chi2) / float(ndf)
        row = {
            "bin": bin_name,
            "q2y": q2y,
            "zpt": zpt,
            "histo": name,
            "stored": {
                "A": stored.get("Fit_Par_A"),
                "A_ERR": stored.get("Fit_Par_A_ERR"),
                "B": stored.get("Fit_Par_B"),
                "B_ERR": stored.get("Fit_Par_B_ERR"),
                "C": stored.get("Fit_Par_C"),
                "C_ERR": stored.get("Fit_Par_C_ERR"),
                "Chi2": chi2,
                "NDF": ndf,
                "recomputed_chi2": stored_chi2,
            },
            "nominal": {
                "A": nom.get("Fit_Par_A"),
                "B": nom.get("Fit_Par_B"),
                "B_ERR": nom.get("Fit_Par_B_ERR"),
                "C": nom.get("Fit_Par_C"),
                "C_ERR": nom.get("Fit_Par_C_ERR"),
                "Chi2": nom.get("Chi2"),
                "NDF": nom.get("NDF"),
            },
            "cosine": cosine,
            "range": {
                "filled_low": filled_low,
                "filled_high": filled_high,
                "phi_low": phi_low,
                "phi_high": phi_high,
                "nonempty": nonempty,
                "bins_in_tf1": bins_in_tf1,
                "positive_error_in_range": positive_error,
                "zero_error_in_range": zero_error,
                "matches_filled_window": ("range_mismatch" not in problems) and (nonempty > 0),
                "nbins": nbins,
            },
            "points": {
                "phi": in_centers,
                "y": in_contents,
                "err": in_errors,
            },
            "spline_B_width": spline_b,
            "spline_C_width": spline_c,
            "manual_limits_exclude_cosine_B": manual_excludes_b,
            "manual_limits_exclude_cosine_C": manual_excludes_c,
            "dB_nominal": dB,
            "dC_nominal": dC,
            "dB_over_stat": dB_stat,
            "dC_over_stat": dC_stat,
            "reduced_chi2": reduced,
            "spike": spike,
            "off_cosine": off_cosine,
            "problems": problems,
        }
        rows.append(row)
    tfile.Close()
    b_widths_sorted = sorted(b_widths)
    c_widths_sorted = sorted(c_widths)
    summary = {
        "families": families,
        "n_histograms": len(rows),
        "n_json": len(before),
        "range_mismatches": sum(1 for row in rows if("range_mismatch" in row["problems"])),
        "empty": sum(1 for row in rows if("empty_histogram" in row["problems"])),
        "off_cosine": [row["bin"] for row in rows if(row["off_cosine"])],
        "collapsed": [row["bin"] for row in rows if(any(item.startswith("collapsed_") or item.startswith("zero_error_") for item in row["problems"]))],
        "spikes": [row["bin"] for row in rows if(row["spike"] is not None)],
        "spline_B_n": len(b_widths),
        "spline_C_n": len(c_widths),
        "spline_B_median": b_widths_sorted[len(b_widths_sorted) // 2] if(b_widths_sorted) else None,
        "spline_C_median": c_widths_sorted[len(c_widths_sorted) // 2] if(c_widths_sorted) else None,
        "spline_B_narrow": sum(1 for width in b_widths if(width < 0.05)),
        "spline_C_narrow": sum(1 for width in c_widths if(width < 0.05)),
        "manual_excludes_B": sum(1 for row in rows if(row["manual_limits_exclude_cosine_B"])),
        "manual_excludes_C": sum(1 for row in rows if(row["manual_limits_exclude_cosine_C"])),
        "high_chi2": [
            {"bin": row["bin"], "reduced": row["reduced_chi2"], "chi2": row["stored"]["Chi2"], "ndf": row["stored"]["NDF"], "off_cosine": row["off_cosine"]}
            for row in sorted(rows, key=lambda item: -(item["reduced_chi2"] or 0.0))[:20]
        ],
    }
    ranked_shift = sorted(rows, key=lambda item: -max(abs(item["dB_nominal"] or 0.0), abs(item["dC_nominal"] or 0.0)))
    summary["largest_shifts"] = [
        {
            "bin": row["bin"],
            "dB": row["dB_nominal"],
            "dC": row["dC_nominal"],
            "dB_over_stat": row["dB_over_stat"],
            "dC_over_stat": row["dC_over_stat"],
            "B": row["stored"]["B"],
            "C": row["stored"]["C"],
            "off_cosine": row["off_cosine"],
            "problems": row["problems"],
        }
        for row in ranked_shift[:15]
    ]
    out_path = os.path.join(DEST, "diagnosis_before.json")
    with open(out_path, "w") as handle:
        json.dump({"summary": summary, "rows": rows}, handle, indent=2)
    print("dimensions 3D")
    print("families", families)
    print("rewrite Bayesian only")
    print("histograms", len(rows), "json", len(before), "range_mismatches", summary["range_mismatches"], "empty", summary["empty"])
    print("spline B median", summary["spline_B_median"], "narrow", summary["spline_B_narrow"], "of", summary["spline_B_n"])
    print("spline C median", summary["spline_C_median"], "narrow", summary["spline_C_narrow"], "of", summary["spline_C_n"])
    print("off_cosine", len(summary["off_cosine"]))
    print("collapsed", summary["collapsed"])
    print("spikes", summary["spikes"])
    print("manual excludes B/C", summary["manual_excludes_B"], summary["manual_excludes_C"])
    print("high chi2")
    for item in summary["high_chi2"][:12]:
        print(" ", item)
    print("largest shifts")
    for item in summary["largest_shifts"][:12]:
        print(" ", item["bin"], "dB", item["dB"], "dC", item["dC"], "dB/stat", item["dB_over_stat"], "off", item["off_cosine"], item["problems"])
    bin18 = [row for row in rows if(row["bin"] == "(Q2_y_Bin_1)-(z_pT_Bin_8)")][0]
    print("bin 1,8 stored", bin18["stored"])
    print("bin 1,8 cosine", bin18["cosine"])
    print("bin 1,8 range", bin18["range"])
    print("bin 1,8 problems", bin18["problems"])
    print("wrote", out_path)


if(__name__ == "__main__"):
    main()
