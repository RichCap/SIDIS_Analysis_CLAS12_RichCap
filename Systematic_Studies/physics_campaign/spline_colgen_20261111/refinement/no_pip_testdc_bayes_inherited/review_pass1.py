import json
import math
import os
import importlib.util
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/no_pip_testdc_bayes_inherited"
fit_path = os.path.join(dest, "fit_pass1.json")
root_path = os.path.join(dest, "histograms.root")
init_path = os.path.join(dest, "refine_init.py")
overlay_dir = os.path.join(dest, "overlays")
os.makedirs(overlay_dir, exist_ok=True)

spec = importlib.util.spec_from_file_location("refine_init", init_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
guide = mod.special_fit_parameters_set

def histo_name(q2y, zpt):
    return "(MultiDim_3D_Histo)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)

def filled_range(histo):
    n_bins = histo.GetNbinsX()
    lo = None
    hi = None
    filled = 0
    total = 0.0
    for ibin in range(1, n_bins + 1):
        content = histo.GetBinContent(ibin)
        if(content != 0):
            filled += 1
            total += content
            if(lo is None):
                lo = histo.GetXaxis().GetBinLowEdge(ibin)
            hi = histo.GetXaxis().GetBinUpEdge(ibin)
    return lo, hi, filled, total

def free_fit(histo):
    formula = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
    lo, hi, filled, total = filled_range(histo)
    if((lo is None) or (filled < 4)):
        return None
    mean_a = total / float(filled)
    if(mean_a <= 0):
        mean_a = abs(total) / float(filled)
    if(mean_a <= 0):
        mean_a = 1.0
    starts = [(0.0, 0.0), (-0.2, 0.05), (-0.2, -0.05), (0.15, 0.08), (-0.35, 0.02), (0.05, -0.08), (-0.45, 0.1), (0.25, -0.1)]
    best = None
    for start_b, start_c in starts:
        func = ROOT.TF1("free_phi", formula, lo, hi)
        func.SetParameter(0, mean_a)
        func.SetParLimits(0, 0.05 * mean_a, 8.0 * mean_a)
        func.SetParameter(1, start_b)
        func.SetParLimits(1, -0.95, 0.95)
        func.SetParameter(2, start_c)
        func.SetParLimits(2, -0.95, 0.95)
        histo.Fit(func, "QRB0")
        chi2 = func.GetChisquare()
        ndf = func.GetNDF()
        if((ndf is None) or (ndf <= 0) or (not math.isfinite(chi2))):
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
            "lo": lo,
            "hi": hi,
        }
        if((best is None) or (row["ratio"] < best["ratio"])):
            best = row
    return best

def parse_bin(key):
    left, right = key.split(")-(")
    q2y = left.split("_Bin_")[-1]
    zpt = right.split("_Bin_")[-1].rstrip(")")
    return q2y, zpt

def active_limits(q2y, zpt):
    key_bin = (str(q2y), str(zpt))
    key_dim = (str(q2y), str(zpt), "3D")
    if(key_dim in guide):
        return guide[key_dim]
    if(key_bin in guide):
        return guide[key_bin]
    return None

with open(fit_path) as handle:
    payload = json.load(handle)
cells = payload["Fit_Pars_from_3D_Bayesian"]

infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")

family_counts = {"Bayesian": 0, "RC_Bayesian": 0, "BC_RC_Bayesian": 0, "Bin": 0, "5D": 0, "Fit_Function": 0}
for key in infile.GetListOfKeys():
    name = str(key.GetName())
    if("MultiDim_5D_Histo" in name):
        family_counts["5D"] += 1
    if("Fit_Function" in name):
        family_counts["Fit_Function"] += 1
    if("MultiDim_3D_Histo" not in name):
        continue
    if("_(Bin)_" in name):
        family_counts["Bin"] += 1
    if("_(BC_RC_Bayesian)_" in name):
        family_counts["BC_RC_Bayesian"] += 1
    elif("_(RC_Bayesian)_" in name):
        family_counts["RC_Bayesian"] += 1
    elif("_(Bayesian)_" in name):
        family_counts["Bayesian"] += 1

rows = []
misses = []
ratios = []
bad_finite = []
q2y_counts = {}
collapsed = []
n_cells = 0
for key in cells:
    cell = cells[key]
    n_cells += 1
    chi2 = cell.get("Chi2")
    ndf = cell.get("NDF")
    par_b = cell.get("Fit_Par_B")
    par_c = cell.get("Fit_Par_C")
    err_b = cell.get("Fit_Par_B_ERR")
    err_c = cell.get("Fit_Par_C_ERR")
    par_a = cell.get("Fit_Par_A")
    q2y, zpt = parse_bin(key)
    q2y_counts[q2y] = q2y_counts.get(q2y, 0) + 1
    finite_ok = True
    for value in [chi2, ndf, par_a, par_b, par_c, err_b, err_c]:
        if((value is None) or (not math.isfinite(value))):
            finite_ok = False
    if(not finite_ok):
        bad_finite.append(key)
        continue
    if((ndf == 0) or (chi2 == 0) or (par_a <= 0)):
        bad_finite.append(key)
        continue
    stored_ratio = chi2 / float(ndf)
    ratios.append(stored_ratio)
    name = histo_name(q2y, zpt)
    histo = infile.Get(name)
    if((not histo) or (histo.Integral() == 0)):
        continue
    settings = active_limits(q2y, zpt)
    b_hit = False
    c_hit = False
    if(settings):
        b_limits = settings.get("B_limits")
        c_limits = settings.get("C_limits")
        if(b_limits):
            lo_b = min(b_limits)
            hi_b = max(b_limits)
            if((abs(par_b - lo_b) < 1e-3) or (abs(par_b - hi_b) < 1e-3)):
                b_hit = True
        if(c_limits):
            lo_c = min(c_limits)
            hi_c = max(c_limits)
            if((abs(par_c - lo_c) < 1e-3) or (abs(par_c - hi_c) < 1e-3)):
                c_hit = True
    suspect = False
    if(stored_ratio >= 2.0):
        suspect = True
    if(abs(err_b) < 1e-5):
        suspect = True
    if(abs(err_c) < 1e-5):
        suspect = True
    if(abs(par_b) >= 0.9):
        suspect = True
    if(abs(par_c) >= 0.9):
        suspect = True
    if(b_hit or c_hit):
        suspect = True
    if(not suspect):
        continue
    fitted = free_fit(histo)
    if(fitted is None):
        continue
    rel = 0.0
    if(fitted["ratio"] > 0):
        rel = (stored_ratio - fitted["ratio"]) / fitted["ratio"]
    delta = stored_ratio - fitted["ratio"]
    shape_move = (abs(par_b - fitted["B"]) > 0.03) or (abs(par_c - fitted["C"]) > 0.02)
    improved = (delta > 0.25) and (rel > 0.12) and shape_move and (abs(fitted["B"]) < 0.94) and (abs(fitted["C"]) < 0.94) and (fitted["Berr"] > 0) and (fitted["Cerr"] > 0)
    record = {
        "q2y": q2y,
        "zpt": zpt,
        "stored_ratio": stored_ratio,
        "free_ratio": fitted["ratio"],
        "delta": delta,
        "rel": rel,
        "A": par_a,
        "B": par_b,
        "Berr": err_b,
        "C": par_c,
        "Cerr": err_c,
        "freeA": fitted["A"],
        "freeB": fitted["B"],
        "freeBerr": fitted["Berr"],
        "freeC": fitted["C"],
        "freeCerr": fitted["Cerr"],
        "b_hit": b_hit,
        "c_hit": c_hit,
        "improved": improved,
        "lo": fitted["lo"],
        "hi": fitted["hi"],
    }
    rows.append(record)
    if(abs(err_b) < 1e-5):
        collapsed.append("%s %s B" % (q2y, zpt))
    if(abs(err_c) < 1e-5):
        collapsed.append("%s %s C" % (q2y, zpt))
    draw = improved or (stored_ratio >= 4.5)
    if(draw):
        canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
        histo.SetStats(0)
        histo.Draw("E")
        stored_func = ROOT.TF1("stored_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", fitted["lo"], fitted["hi"])
        stored_func.SetParameters(par_a, par_b, par_c)
        stored_func.SetLineColor(ROOT.kRed)
        stored_func.SetLineWidth(2)
        stored_func.Draw("SAME")
        free_func = ROOT.TF1("free_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", fitted["lo"], fitted["hi"])
        free_func.SetParameters(fitted["A"], fitted["B"], fitted["C"])
        free_func.SetLineColor(ROOT.kBlue)
        free_func.SetLineWidth(2)
        free_func.Draw("SAME")
        canvas.SaveAs(os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % (q2y, zpt)))
        canvas.Close()
    if(improved):
        misses.append(record)

infile.Close()
ratios.sort()
median = ratios[len(ratios) // 2] if(ratios) else None
misses.sort(key=lambda item: item["delta"], reverse=True)
summary = {
    "n_cells": n_cells,
    "n_ratios": len(ratios),
    "median_chi2_ndf": median,
    "q2y_counts": q2y_counts,
    "family_counts": family_counts,
    "n_bad_finite": len(bad_finite),
    "bad_finite": bad_finite,
    "n_suspect_tested": len(rows),
    "n_improved": len(misses),
    "misses": misses,
    "high_tail": sorted(rows, key=lambda item: item["stored_ratio"], reverse=True)[:25],
    "collapsed": collapsed,
}
out_path = os.path.join(dest, "review_pass1.json")
with open(out_path, "w") as handle:
    json.dump(summary, handle, indent=2)
print("families", family_counts)
print("n_cells", n_cells)
print("median", median)
print("q2y", dict(sorted(q2y_counts.items(), key=lambda item: int(item[0]))))
print("bad", len(bad_finite))
print("tested", len(rows))
print("improved", len(misses))
print("collapsed", collapsed)
for item in misses:
    print("MISS", item["q2y"], item["zpt"], "stored", round(item["stored_ratio"], 3), "free", round(item["free_ratio"], 3), "B", round(item["B"], 4), "->", round(item["freeB"], 4), "C", round(item["C"], 4), "->", round(item["freeC"], 4), "bhit", item["b_hit"], "chit", item["c_hit"])
print("TAIL")
for item in summary["high_tail"]:
    print("TAIL", item["q2y"], item["zpt"], round(item["stored_ratio"], 3), round(item["free_ratio"], 3), "improved", item["improved"], "B", round(item["B"], 4), round(item["freeB"], 4), "C", round(item["C"], 4), round(item["freeC"], 4))
