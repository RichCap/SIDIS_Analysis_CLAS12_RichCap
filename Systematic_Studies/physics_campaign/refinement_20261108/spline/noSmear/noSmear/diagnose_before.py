# Read-only diagnosis of the copied spline noSmear 3D Bayesian histograms.
# Does not edit the shared Phi_h guides or the source fit.
import importlib.util
import json
import math
import os

import numpy as np
import ROOT

ROOT.gErrorIgnoreLevel = ROOT.kError

here = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(here, "fit_copy.root")
before_path = os.path.join(here, "fit_before.json")
nominal_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/fits/spline/nominal/nominal/fit.json"
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
out_path = os.path.join(here, "diagnosis_before.json")


def load_set(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_fit_parameters_set


def select_settings(table, q2y, zpt):
    for key in [(q2y, zpt, "3D"), (q2y, zpt)]:
        if(key in table):
            return key, table[key]
    return None, None


def span(limits):
    if(not limits):
        return None
    return abs(float(limits[1]) - float(limits[0]))


def sorted_limits(limits):
    if(not limits):
        return None
    lo = float(limits[0])
    hi = float(limits[1])
    if(lo > hi):
        return [hi, lo]
    return [lo, hi]


def near(left, right):
    return abs(float(left) - float(right)) <= 1.0e-4


def wls_cosine(centers, values, errors):
    phi = np.deg2rad(np.asarray(centers, dtype=float))
    y = np.asarray(values, dtype=float)
    err = np.asarray(errors, dtype=float)
    design = np.column_stack([np.ones_like(phi), np.cos(phi), np.cos(2.0 * phi)])
    weight = 1.0 / np.square(err)
    weighted = design.T * weight
    normal = weighted @ design
    target = weighted @ y
    try:
        beta = np.linalg.solve(normal, target)
        cov = np.linalg.inv(normal)
    except np.linalg.LinAlgError:
        return None
    amplitude = float(beta[0])
    if(not math.isfinite(amplitude)) or (abs(amplitude) < 1.0e-12):
        return None
    b_value = float(beta[1] / amplitude)
    c_value = float(beta[2] / amplitude)
    # d(B)/d(A, AB) with B = AB/A
    # var(B) = (AB/A^2)^2 varA + (1/A)^2 varAB - 2 (AB/A^3) cov
    var_a = float(cov[0, 0])
    var_ab = float(cov[1, 1])
    var_ac = float(cov[2, 2])
    cov_a_ab = float(cov[0, 1])
    cov_a_ac = float(cov[0, 2])
    b_var = (b_value * b_value) * var_a / (amplitude * amplitude) + var_ab / (amplitude * amplitude) - 2.0 * b_value * cov_a_ab / (amplitude * amplitude)
    c_var = (c_value * c_value) * var_a / (amplitude * amplitude) + var_ac / (amplitude * amplitude) - 2.0 * c_value * cov_a_ac / (amplitude * amplitude)
    pred = amplitude * (1.0 + b_value * np.cos(phi) + c_value * np.cos(2.0 * phi))
    chi2 = float(np.sum(np.square((y - pred) / err)))
    ndf = int(len(y) - 3)
    return {
        "A": amplitude,
        "B": b_value,
        "C": c_value,
        "B_ERR": math.sqrt(b_var) if(b_var > 0.0) else None,
        "C_ERR": math.sqrt(c_var) if(c_var > 0.0) else None,
        "Chi2": chi2,
        "NDF": ndf,
    }


def chi2_of(amplitude, b_value, c_value, centers, values, errors):
    phi = np.deg2rad(np.asarray(centers, dtype=float))
    y = np.asarray(values, dtype=float)
    err = np.asarray(errors, dtype=float)
    pred = float(amplitude) * (1.0 + float(b_value) * np.cos(phi) + float(c_value) * np.cos(2.0 * phi))
    return float(np.sum(np.square((y - pred) / err)))


def pinned(value, limits):
    bounds = sorted_limits(limits)
    if(bounds is None):
        return False, None
    if(near(value, bounds[0]) or near(value, bounds[1])):
        return True, "first_pass_limit"
    outer_lo = bounds[0] - 0.5 * abs(bounds[0])
    outer_hi = bounds[1] + 0.5 * abs(bounds[1])
    if(near(value, outer_lo) or near(value, outer_hi)):
        return True, "second_pass_edge"
    return False, None


manual = load_set(manual_path, "manual_phi_init")
spline = load_set(spline_path, "spline_phi_init")
with open(before_path, "r") as handle:
    before = json.load(handle)
with open(nominal_path, "r") as handle:
    nominal = json.load(handle)
stored = before["Fit_Pars_from_3D_Bayesian"]
nominal_cells = nominal["Fit_Pars_from_3D_Bayesian"]

infile = ROOT.TFile.Open(root_path, "READ")
if(not infile) or (infile.IsZombie()):
    raise SystemExit("could not open the copied ROOT file")

names = {}
for key in infile.GetListOfKeys():
    names[str(key.GetName())] = str(key.GetClassName())

family_counts = {}
for name in names:
    if("MultiDim_3D_Histo" not in name) and ("MultiDim_5D_Histo" not in name):
        continue
    if("Bin_All" in name) or ("_(Normalized)" in name) or ("_AsymErr" in name):
        continue
    parts = name.split(")_(")
    if(len(parts) < 2):
        continue
    token = parts[1]
    dim = "5D" if("MultiDim_5D_Histo" in name) else "3D"
    label = dim + ":" + token
    family_counts[label] = family_counts.get(label, 0) + 1

rows = []
b_widths = []
c_widths = []
narrow_b = 0
narrow_c = 0
selected = 0
for name in sorted(names):
    if("(MultiDim_3D_Histo)_(Bayesian)_" not in name):
        continue
    if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in name):
        continue
    if("Bin_All" in name) or ("_(Normalized)" in name) or ("_AsymErr" in name):
        continue
    histo = infile.Get(name)
    if(not histo):
        continue
    parts = name.split(")_(")
    q2y = parts[3].replace("Q2_y_Bin_", "")
    zpt = parts[4].replace("z_pT_Bin_", "")
    bin_name = "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt)
    nbins = int(histo.GetNbinsX())
    contents = []
    first = None
    last = None
    for ibin in range(1, nbins + 1):
        content = float(histo.GetBinContent(ibin))
        error = float(histo.GetBinError(ibin))
        low = float(histo.GetXaxis().GetBinLowEdge(ibin))
        high = float(histo.GetXaxis().GetBinUpEdge(ibin))
        center = float(histo.GetXaxis().GetBinCenter(ibin))
        contents.append({"i": ibin, "content": content, "error": error, "low": low, "high": high, "center": center})
        if(content != 0.0):
            if(first is None):
                first = ibin
            last = ibin
    fit_name = name.replace("(MultiDim_3D_Histo)", "(Fit_Function)")
    fit_obj = infile.Get(fit_name)
    phi_low = None
    phi_high = None
    if(fit_obj):
        phi_low = float(fit_obj.GetXmin())
        phi_high = float(fit_obj.GetXmax())
    filled_low = None
    filled_high = None
    if(first is not None):
        filled_low = contents[first - 1]["low"]
        filled_high = contents[last - 1]["high"]
    centers = []
    values = []
    errors = []
    zero_error_in_range = 0
    positive_error_in_range = 0
    nonempty = 0
    bins_in_tf1 = 0
    if(first is not None):
        for item in contents:
            inside = (item["center"] >= filled_low - 1.0e-6) and (item["center"] <= filled_high + 1.0e-6)
            if(item["content"] != 0.0):
                nonempty += 1
            if(not inside):
                continue
            bins_in_tf1 += 1
            if(item["error"] > 0.0):
                positive_error_in_range += 1
                centers.append(item["center"])
                values.append(item["content"])
                errors.append(item["error"])
            else:
                zero_error_in_range += 1
    free = None
    if(len(centers) >= 4):
        free = wls_cosine(centers, values, errors)
    cell = stored.get(bin_name, {})
    nom = nominal_cells.get(bin_name, {})
    stored_chi2_on_window = None
    if(cell) and (len(centers) >= 1):
        stored_chi2_on_window = chi2_of(cell.get("Fit_Par_A"), cell.get("Fit_Par_B"), cell.get("Fit_Par_C"), centers, values, errors)
    spline_key, spline_set = select_settings(spline, q2y, zpt)
    manual_key, manual_set = select_settings(manual, q2y, zpt)
    b_width = span(spline_set.get("B_limits")) if(spline_set) else None
    c_width = span(spline_set.get("C_limits")) if(spline_set) else None
    if(spline_set):
        selected += 1
        if(b_width is not None):
            b_widths.append(b_width)
            if(b_width < 0.05):
                narrow_b += 1
        if(c_width is not None):
            c_widths.append(c_width)
            if(c_width < 0.05):
                narrow_c += 1
    b_pin, b_pin_kind = pinned(cell.get("Fit_Par_B", 0.0), None if(manual_set is None) else manual_set.get("B_limits"))
    c_pin, c_pin_kind = pinned(cell.get("Fit_Par_C", 0.0), None if(manual_set is None) else manual_set.get("C_limits"))
    # The stored guide is not the manual file. Also test the copied refine_init limits by the known second-pass edge.
    free_gap = None
    if(free is not None) and (cell):
        free_gap = float(free["Chi2"] - float(cell.get("Chi2", free["Chi2"])))
    matches_window = None
    if(filled_low is not None) and (phi_low is not None):
        matches_window = near(filled_low, phi_low) and near(filled_high, phi_high)
    row = {
        "bin": bin_name,
        "q2y": q2y,
        "zpt": zpt,
        "name": name,
        "stored": {
            "A": cell.get("Fit_Par_A"),
            "A_ERR": cell.get("Fit_Par_A_ERR"),
            "B": cell.get("Fit_Par_B"),
            "B_ERR": cell.get("Fit_Par_B_ERR"),
            "C": cell.get("Fit_Par_C"),
            "C_ERR": cell.get("Fit_Par_C_ERR"),
            "Chi2": cell.get("Chi2"),
            "NDF": cell.get("NDF"),
        },
        "nominal": {
            "B": nom.get("Fit_Par_B"),
            "B_ERR": nom.get("Fit_Par_B_ERR"),
            "C": nom.get("Fit_Par_C"),
            "C_ERR": nom.get("Fit_Par_C_ERR"),
            "Chi2": nom.get("Chi2"),
            "NDF": nom.get("NDF"),
        },
        "free": free,
        "stored_chi2_on_filled_window": stored_chi2_on_window,
        "range": {
            "filled_low": filled_low,
            "filled_high": filled_high,
            "phi_low": phi_low,
            "phi_high": phi_high,
            "nonempty": nonempty,
            "bins_in_tf1": bins_in_tf1,
            "positive_error_in_range": positive_error_in_range,
            "zero_error_in_range": zero_error_in_range,
            "matches_filled_window": matches_window,
            "nbins": nbins,
        },
        "manual_key": None if(manual_key is None) else list(manual_key),
        "manual_B_limits": None if(manual_set is None) else manual_set.get("B_limits"),
        "manual_C_limits": None if(manual_set is None) else manual_set.get("C_limits"),
        "spline_key": None if(spline_key is None) else list(spline_key),
        "spline_B_width": b_width,
        "spline_C_width": c_width,
        "b_pin_vs_manual": b_pin,
        "b_pin_kind": b_pin_kind,
        "c_pin_vs_manual": c_pin,
        "c_pin_kind": c_pin_kind,
        "free_minus_stored_chi2": None if(free is None) or (cell.get("Chi2") is None) else (float(free["Chi2"]) - float(cell["Chi2"])),
    }
    if(cell) and (nom):
        row["dB_nominal"] = None if(nom.get("Fit_Par_B") is None) else (float(cell["Fit_Par_B"]) - float(nom["Fit_Par_B"]))
        row["dC_nominal"] = None if(nom.get("Fit_Par_C") is None) else (float(cell["Fit_Par_C"]) - float(nom["Fit_Par_C"]))
        b_err = cell.get("Fit_Par_B_ERR")
        c_err = cell.get("Fit_Par_C_ERR")
        row["dB_over_stat"] = None if(not b_err) else (row["dB_nominal"] / float(b_err))
        row["dC_over_stat"] = None if(not c_err) else (row["dC_nominal"] / float(c_err))
    rows.append(row)

infile.Close()

def median(values):
    if(len(values) == 0):
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if(len(ordered) % 2):
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])

misses = []
for row in rows:
    gap = row["free_minus_stored_chi2"]
    if(gap is None):
        continue
    # free chi2 minus stored: negative means the cosine beats the stored fit
    if(gap < -0.5):
        misses.append(row)

misses.sort(key=lambda item: item["free_minus_stored_chi2"])
shifts = [row for row in rows if(row.get("dB_nominal") is not None)]
shifts.sort(key=lambda item: abs(item["dB_nominal"]), reverse=True)
range_bad = [row["bin"] for row in rows if(row["range"]["matches_filled_window"] is False)]
reduced = []
for row in rows:
    ndf = row["stored"].get("NDF")
    chi2 = row["stored"].get("Chi2")
    if(ndf) and (chi2 is not None) and (float(ndf) > 0.0):
        reduced.append((float(chi2) / float(ndf), row["bin"], chi2, ndf))
reduced.sort(reverse=True)

summary = {
    "histograms": len(rows),
    "json_bins": len(stored),
    "nominal_bins": len(nominal_cells),
    "family_counts": family_counts,
    "range_mismatches": len(range_bad),
    "range_mismatch_bins": range_bad[:30],
    "spline_selected": selected,
    "spline_B_median_width": median(b_widths),
    "spline_C_median_width": median(c_widths),
    "spline_B_narrower_than_0p05": narrow_b,
    "spline_C_narrower_than_0p05": narrow_c,
    "spline_B_widths": len(b_widths),
    "cosine_better_than_stored_by_0p5": len(misses),
    "worst_reduced": [
        {"reduced": item[0], "bin": item[1], "Chi2": item[2], "NDF": item[3]}
        for item in reduced[:20]
    ],
    "largest_abs_dB": [
        {
            "bin": row["bin"],
            "dB": row.get("dB_nominal"),
            "dB_over_stat": row.get("dB_over_stat"),
            "dC": row.get("dC_nominal"),
            "stored_B": row["stored"]["B"],
            "nominal_B": row["nominal"]["B"],
            "free_B": None if(row["free"] is None) else row["free"]["B"],
            "stored_Chi2": row["stored"]["Chi2"],
            "free_Chi2": None if(row["free"] is None) else row["free"]["Chi2"],
            "b_pin_kind": row["b_pin_kind"],
        }
        for row in shifts[:15]
    ],
    "cosine_misses": [
        {
            "bin": row["bin"],
            "gap": row["free_minus_stored_chi2"],
            "stored_B": row["stored"]["B"],
            "stored_C": row["stored"]["C"],
            "stored_B_ERR": row["stored"]["B_ERR"],
            "stored_C_ERR": row["stored"]["C_ERR"],
            "stored_Chi2": row["stored"]["Chi2"],
            "stored_NDF": row["stored"]["NDF"],
            "free_B": row["free"]["B"],
            "free_C": row["free"]["C"],
            "free_Chi2": row["free"]["Chi2"],
            "free_B_ERR": row["free"]["B_ERR"],
            "free_C_ERR": row["free"]["C_ERR"],
            "manual_B_limits": row["manual_B_limits"],
            "manual_C_limits": row["manual_C_limits"],
            "b_pin_kind": row["b_pin_kind"],
            "c_pin_kind": row["c_pin_kind"],
            "phi": [row["range"]["filled_low"], row["range"]["filled_high"]],
            "bins_in_tf1": row["range"]["bins_in_tf1"],
        }
        for row in misses[:40]
    ],
}

target = None
for row in rows:
    if(row["bin"] == "(Q2_y_Bin_1)-(z_pT_Bin_8)"):
        target = row
        break
summary["bin_1_8"] = target

with open(out_path, "w") as handle:
    json.dump({"summary": summary, "rows": rows}, handle, indent=2)

print("histograms", len(rows), "json", len(stored))
print("families", json.dumps(family_counts, sort_keys=True))
print("range_mismatches", len(range_bad))
print("spline B median", summary["spline_B_median_width"], "narrow", narrow_b, "of", len(b_widths))
print("spline C median", summary["spline_C_median_width"], "narrow", narrow_c, "of", len(c_widths))
print("cosine misses", len(misses))
print("top reduced", summary["worst_reduced"][:8])
print("top dB", summary["largest_abs_dB"][:8])
print("top misses", summary["cosine_misses"][:12])
if(target):
    print("bin18 stored", target["stored"])
    print("bin18 free", target["free"])
    print("bin18 nominal dB", target.get("dB_nominal"), "pin", target["b_pin_kind"], target["c_pin_kind"])
    print("bin18 range", target["range"])
    print("bin18 manual limits", target["manual_B_limits"], target["manual_C_limits"])
