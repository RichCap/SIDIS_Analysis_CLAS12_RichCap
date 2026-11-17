import json
import math
import os
import importlib.util
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/eS1o_bayes_inherited"
fit_path = os.path.join(dest, "fit_pass1.json")
root_path = os.path.join(dest, "histograms.root")
init_path = os.path.join(dest, "refine_init.py")
overlay_dir = os.path.join(dest, "overlays")
os.makedirs(overlay_dir, exist_ok=True)

spec = importlib.util.spec_from_file_location("refine_init", init_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
guide = mod.special_fit_parameters_set

with open(fit_path) as handle:
    payload = json.load(handle)
cells = payload["Fit_Pars_from_3D_Bayesian"]

def histo_name(q2y, zpt):
    return "(MultiDim_3D_Histo)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)

def filled_range(histo):
    lo = None
    hi = None
    n_bins = histo.GetNbinsX()
    for ibin in range(1, n_bins + 1):
        if(histo.GetBinContent(ibin) != 0):
            lo = histo.GetXaxis().GetBinLowEdge(ibin)
            break
    for ibin in range(n_bins, 0, -1):
        if(histo.GetBinContent(ibin) != 0):
            hi = histo.GetXaxis().GetBinUpEdge(ibin)
            break
    if((lo is None) or (hi is None) or (hi <= lo)):
        return 0.0, 360.0
    return lo, hi

def n_filled(histo):
    filled = 0
    total = 0.0
    n_bins = histo.GetNbinsX()
    for ibin in range(1, n_bins + 1):
        content = histo.GetBinContent(ibin)
        if(content != 0):
            filled += 1
            total += content
    return filled, total

def free_fit(histo):
    formula = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
    lo, hi = filled_range(histo)
    filled, total = n_filled(histo)
    if(filled < 4):
        return None
    mean_a = total / float(filled)
    if(mean_a <= 0):
        mean_a = abs(total) / float(filled)
    if(mean_a <= 0):
        mean_a = 1.0
    best = None
    starts = [(0.0, 0.0), (-0.2, 0.05), (-0.2, -0.05), (0.15, 0.08), (-0.35, 0.02), (0.05, -0.08), (-0.45, 0.12), (0.25, -0.12)]
    for start_b, start_c in starts:
        func = ROOT.TF1("free_phi", formula, 0, 360)
        func.SetRange(lo, hi)
        func.SetParameter(0, mean_a)
        func.SetParLimits(0, 0.05 * mean_a, 8.0 * mean_a)
        func.SetParameter(1, start_b)
        func.SetParLimits(1, -0.95, 0.95)
        func.SetParameter(2, start_c)
        func.SetParLimits(2, -0.95, 0.95)
        histo.Fit(func, "QRB0")
        chi2 = func.GetChisquare()
        ndf = func.GetNDF()
        if((ndf is None) or (ndf <= 0) or (not math.isfinite(chi2)) or (chi2 <= 0)):
            continue
        ratio = chi2 / float(ndf)
        row = {
            "ratio": ratio,
            "chi2": chi2,
            "ndf": ndf,
            "A": func.GetParameter(0),
            "B": func.GetParameter(1),
            "C": func.GetParameter(2),
            "Berr": func.GetParError(1),
            "Cerr": func.GetParError(2),
            "Aerr": func.GetParError(0),
        }
        if((best is None) or (row["ratio"] < best["ratio"])):
            best = row
    return best

def on_limit(value, limits):
    if((value is None) or (not limits)):
        return False
    lo = min(limits)
    hi = max(limits)
    if((abs(value - lo) < 1e-3) or (abs(value - hi) < 1e-3)):
        return True
    return False

infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")

family_counts = {"Bayesian": 0, "RC_Bayesian": 0, "BC_RC_Bayesian": 0, "Bin": 0, "5D": 0}
for key in infile.GetListOfKeys():
    name = key.GetName()
    if("MultiDim_5D_Histo" in name):
        family_counts["5D"] += 1
    if(")_(Bin)_" in name):
        family_counts["Bin"] += 1
    if(")_(RC_Bayesian)_" in name):
        family_counts["RC_Bayesian"] += 1
    if(")_(BC_RC_Bayesian)_" in name):
        family_counts["BC_RC_Bayesian"] += 1
    if(")_(Bayesian)_" in name):
        family_counts["Bayesian"] += 1

rows = []
misses = []
ratios = []
n_cells = 0
for key, cell in cells.items():
    n_cells += 1
    left, right = key.split(")-(")
    q2y = left.split("_Bin_")[-1]
    zpt = right.split("_Bin_")[-1].rstrip(")")
    chi2 = cell.get("Chi2")
    ndf = cell.get("NDF")
    par_b = cell.get("Fit_Par_B")
    par_c = cell.get("Fit_Par_C")
    err_b = cell.get("Fit_Par_B_ERR")
    err_c = cell.get("Fit_Par_C_ERR")
    par_a = cell.get("Fit_Par_A")
    stored_ratio = None
    if((ndf is not None) and (ndf != 0) and (chi2 is not None) and math.isfinite(chi2) and math.isfinite(ndf)):
        stored_ratio = chi2 / float(ndf)
        ratios.append(stored_ratio)
    settings = guide.get((q2y, zpt), {})
    b_hit = on_limit(par_b, settings.get("B_limits"))
    c_hit = on_limit(par_c, settings.get("C_limits"))
    suspect = False
    if((stored_ratio is not None) and (stored_ratio >= 2.2)):
        suspect = True
    if((err_b is not None) and (abs(err_b) < 1e-4)):
        suspect = True
    if((err_c is not None) and (abs(err_c) < 1e-4)):
        suspect = True
    if((par_b is not None) and (abs(par_b) >= 0.85)):
        suspect = True
    if((par_c is not None) and (abs(par_c) >= 0.85)):
        suspect = True
    if((ndf is None) or (ndf == 0) or (chi2 is None) or (chi2 == 0)):
        suspect = True
    if(b_hit or c_hit):
        suspect = True
    if(not suspect):
        continue
    name = histo_name(q2y, zpt)
    histo = infile.Get(name)
    if((not histo) or (histo.Integral() == 0)):
        continue
    filled, total = n_filled(histo)
    fitted = free_fit(histo)
    if(fitted is None):
        rows.append({
            "q2y": q2y,
            "zpt": zpt,
            "stored_ratio": stored_ratio,
            "free_ratio": None,
            "filled": filled,
            "B": par_b,
            "C": par_c,
            "improved": False,
            "reason": "no_free_fit",
        })
        continue
    rel = 0.0
    delta = 0.0
    if(stored_ratio is not None):
        delta = stored_ratio - fitted["ratio"]
        if(fitted["ratio"] > 0):
            rel = delta / fitted["ratio"]
    shape_ok = (abs(fitted["B"]) < 0.94) and (abs(fitted["C"]) < 0.94) and math.isfinite(fitted["Berr"]) and math.isfinite(fitted["Cerr"]) and (fitted["Berr"] > 1e-6) and (fitted["Cerr"] > 1e-6)
    stored_bad = False
    if((par_b is not None) and (abs(par_b) >= 1)):
        stored_bad = True
    if((par_c is not None) and (abs(par_c) >= 1)):
        stored_bad = True
    if((ndf is None) or (ndf == 0) or (chi2 is None) or (chi2 == 0)):
        stored_bad = True
    if((err_b is not None) and (abs(err_b) < 1e-6)):
        stored_bad = True
    if((err_c is not None) and (abs(err_c) < 1e-6)):
        stored_bad = True
    improved = shape_ok and (((stored_ratio is not None) and (delta > 0.30) and (rel > 0.15)) or stored_bad)
    # A near-zero stored moment that the free fit also calls consistent with zero is not a shape miss.
    if(stored_bad and (stored_ratio is not None) and (delta <= 0.15) and (abs(fitted["B"]) < 0.05) and (abs(par_b) < 0.05) and (abs(fitted["C"] - (par_c or 0)) < 0.05)):
        improved = False
    record = {
        "q2y": q2y,
        "zpt": zpt,
        "stored_ratio": stored_ratio,
        "free_ratio": fitted["ratio"],
        "rel": rel,
        "delta": delta,
        "B": par_b,
        "Berr": err_b,
        "C": par_c,
        "Cerr": err_c,
        "A": par_a,
        "freeB": fitted["B"],
        "freeBerr": fitted["Berr"],
        "freeC": fitted["C"],
        "freeCerr": fitted["Cerr"],
        "freeA": fitted["A"],
        "b_hit": b_hit,
        "c_hit": c_hit,
        "filled": filled,
        "improved": improved,
        "stored_bad": stored_bad,
    }
    rows.append(record)
    if(not improved):
        continue
    misses.append(record)
    canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
    histo.SetTitle("Q2y %s zPT %s  stored %.2f  free %.2f" % (q2y, zpt, stored_ratio if stored_ratio is not None else -1, fitted["ratio"]))
    histo.SetStats(0)
    histo.Draw("E")
    lo, hi = filled_range(histo)
    stored_func = ROOT.TF1("stored_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
    stored_b = par_b if par_b is not None else 0.0
    stored_c = par_c if par_c is not None else 0.0
    stored_a = par_a if((par_a is not None) and math.isfinite(par_a) and (abs(par_a) < 1e7)) else fitted["A"]
    stored_func.SetParameters(stored_a, stored_b, stored_c)
    stored_func.SetLineColor(ROOT.kRed)
    stored_func.SetLineWidth(2)
    stored_func.Draw("SAME")
    free_func = ROOT.TF1("free_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
    free_func.SetParameters(fitted["A"], fitted["B"], fitted["C"])
    free_func.SetLineColor(ROOT.kBlue)
    free_func.SetLineWidth(2)
    free_func.Draw("SAME")
    canvas.SaveAs(os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % (q2y, zpt)))
    canvas.Close()

infile.Close()
ratios.sort()
median = ratios[len(ratios) // 2] if(ratios) else None
misses.sort(key=lambda item: item["delta"], reverse=True)
summary = {
    "n_cells": n_cells,
    "n_ratios": len(ratios),
    "median_chi2_ndf": median,
    "family_counts": family_counts,
    "n_suspect_tested": len(rows),
    "n_improved": len(misses),
    "misses": misses,
    "tested": rows,
}
out_path = os.path.join(dest, "review_pass1.json")
with open(out_path, "w") as handle:
    json.dump(summary, handle, indent=2)
print("families", family_counts)
print("n_cells", n_cells)
print("median", median)
print("tested", len(rows))
print("improved", len(misses))
for item in misses:
    stored_text = "NA" if(item["stored_ratio"] is None) else round(item["stored_ratio"], 3)
    print("MISS", item["q2y"], item["zpt"], "stored", stored_text, "free", round(item["free_ratio"], 3), "B", None if item["B"] is None else round(item["B"], 4), "->", round(item["freeB"], 4), "C", None if item["C"] is None else round(item["C"], 4), "->", round(item["freeC"], 4), "filled", item["filled"], "bhit", item["b_hit"], "chit", item["c_hit"], "bad", item["stored_bad"])
print("NOT_IMPROVED")
for item in rows:
    if(item.get("improved")):
        continue
    stored_text = item.get("stored_ratio")
    free_text = item.get("free_ratio")
    print("KEEP", item["q2y"], item["zpt"], "stored", None if stored_text is None else round(stored_text, 3), "free", None if free_text is None else round(free_text, 3), "reason", item.get("reason"), "B", item.get("B"), "C", item.get("C"))
