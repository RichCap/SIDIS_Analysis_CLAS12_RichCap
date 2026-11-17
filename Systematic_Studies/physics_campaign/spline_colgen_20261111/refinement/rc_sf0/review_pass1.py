# Review stored RC_Bayesian phi_h fits against a wide cosine on the filled range.
import json
import math
import os
import importlib.util
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/rc_sf0"
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
cells = payload["Fit_Pars_from_3D_RC_Bayesian"]

def histo_name(q2y, zpt):
    return "(MultiDim_3D_Histo)_(RC_Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)

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

def free_fit(histo):
    formula = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
    lo, hi = filled_range(histo)
    best = None
    starts = [(0.0, 0.0), (-0.2, 0.05), (-0.2, -0.05), (0.15, 0.08), (-0.35, 0.02), (0.05, -0.08)]
    filled = 0
    total = 0.0
    n_bins = histo.GetNbinsX()
    for ibin in range(1, n_bins + 1):
        content = histo.GetBinContent(ibin)
        if(content != 0):
            filled += 1
            total += content
    if(filled < 4):
        return None
    mean_a = total / float(filled)
    if(mean_a <= 0):
        mean_a = abs(total) / float(filled)
    if(mean_a <= 0):
        mean_a = 1.0
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
            "nbins": n_bins,
            "filled": filled,
        }
        if((best is None) or (row["ratio"] < best["ratio"])):
            best = row
    return best

def parse_bin(key):
    left, right = key.split(")-(")
    q2y = left.split("_Bin_")[-1]
    zpt = right.split("_Bin_")[-1].rstrip(")")
    return q2y, zpt

def guide_for(q2y, zpt):
    for key in ((q2y, zpt, "3D", "RC"), (q2y, zpt, "RC"), (q2y, zpt)):
        if(key in guide):
            return guide[key]
    return None

def draw_overlay(histo, q2y, zpt, par_a, par_b, par_c, fitted, folder):
    canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
    histo.SetTitle("Q2y %s zpt %s" % (q2y, zpt))
    histo.SetStats(0)
    histo.Draw("E")
    lo, hi = filled_range(histo)
    stored_func = ROOT.TF1("stored_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
    stored_func.SetParameters(par_a, par_b, par_c)
    stored_func.SetLineColor(ROOT.kRed)
    stored_func.SetLineWidth(2)
    stored_func.Draw("SAME")
    free_func = ROOT.TF1("free_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
    free_func.SetParameters(fitted["A"], fitted["B"], fitted["C"])
    free_func.SetLineColor(ROOT.kBlue)
    free_func.SetLineWidth(2)
    free_func.Draw("SAME")
    canvas.SaveAs(os.path.join(folder, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % (q2y, zpt)))
    canvas.Close()

infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")

family_counts = {"Bayesian": 0, "RC_Bayesian": 0, "BC_RC_Bayesian": 0, "Bin": 0, "5D": 0}
phi_names = []
for key in infile.GetListOfKeys():
    name = key.GetName()
    if("MultiDim_5D_Histo" in name):
        family_counts["5D"] += 1
    if("MultiDim_3D_Histo" not in name):
        continue
    if("phi_t" not in name):
        continue
    if("Bin_All" in name):
        continue
    if("_(Normalized)" in name):
        continue
    if("_AsymErr" in name):
        continue
    if(")_(Bayesian)_" in name):
        family_counts["Bayesian"] += 1
    elif(")_(RC_Bayesian)_" in name):
        family_counts["RC_Bayesian"] += 1
        phi_names.append(name)
    elif(")_(BC_RC_Bayesian)_" in name):
        family_counts["BC_RC_Bayesian"] += 1
    elif(")_(Bin)_" in name):
        family_counts["Bin"] += 1

rows = []
misses = []
n_cells = 0
ratios = []
collapsed = []
missing_histo = []
empty_histo = []
nbins_seen = {}
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
    name = histo_name(q2y, zpt)
    histo = infile.Get(name)
    if(not histo):
        missing_histo.append([q2y, zpt])
        continue
    if(histo.Integral() == 0):
        empty_histo.append([q2y, zpt])
        continue
    nbins_seen[histo.GetNbinsX()] = nbins_seen.get(histo.GetNbinsX(), 0) + 1
    if((ndf is None) or (ndf == 0) or (chi2 is None) or (not math.isfinite(chi2))):
        continue
    stored_ratio = chi2 / float(ndf)
    ratios.append(stored_ratio)
    suspect = False
    if(stored_ratio >= 2.2):
        suspect = True
    if((err_b is not None) and (abs(err_b) < 1e-6)):
        suspect = True
    if((err_c is not None) and (abs(err_c) < 1e-6)):
        suspect = True
    if((par_b is not None) and (abs(par_b) >= 0.9)):
        suspect = True
    if((par_c is not None) and (abs(par_c) >= 0.9)):
        suspect = True
    settings = guide_for(q2y, zpt)
    b_hit = False
    c_hit = False
    if(settings):
        b_limits = settings.get("B_limits")
        c_limits = settings.get("C_limits")
        if((b_limits) and (par_b is not None)):
            lo_b = min(b_limits)
            hi_b = max(b_limits)
            if((abs(par_b - lo_b) < 1e-3) or (abs(par_b - hi_b) < 1e-3)):
                b_hit = True
                suspect = True
        if((c_limits) and (par_c is not None)):
            lo_c = min(c_limits)
            hi_c = max(c_limits)
            if((abs(par_c - lo_c) < 1e-3) or (abs(par_c - hi_c) < 1e-3)):
                c_hit = True
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
    shape_move = (abs(fitted["B"] - par_b) > max(0.03, 1.5 * abs(err_b or 0))) or (abs(fitted["C"] - par_c) > max(0.03, 1.5 * abs(err_c or 0)))
    improved = (delta > 0.25) and (rel > 0.12) and shape_move and (abs(fitted["B"]) < 0.94) and (abs(fitted["C"]) < 0.94)
    record = {
        "q2y": q2y,
        "zpt": zpt,
        "stored_ratio": stored_ratio,
        "free_ratio": fitted["ratio"],
        "rel": rel,
        "B": par_b,
        "Berr": err_b,
        "C": par_c,
        "Cerr": err_c,
        "freeB": fitted["B"],
        "freeBerr": fitted["Berr"],
        "freeC": fitted["C"],
        "freeCerr": fitted["Cerr"],
        "freeA": fitted["A"],
        "A": par_a,
        "b_hit": b_hit,
        "c_hit": c_hit,
        "improved": improved,
        "nbins": fitted["nbins"],
        "filled": fitted["filled"],
        "lo": fitted["lo"],
        "hi": fitted["hi"],
    }
    rows.append(record)
    if((err_b is not None) and (abs(err_b) < 1e-6)):
        collapsed.append({"q2y": q2y, "zpt": zpt, "which": "B"})
    if((err_c is not None) and (abs(err_c) < 1e-6)):
        collapsed.append({"q2y": q2y, "zpt": zpt, "which": "C"})
    if(improved):
        misses.append(record)
        draw_overlay(histo, q2y, zpt, par_a, par_b, par_c, fitted, overlay_dir)

fitted_names = set()
for key in cells:
    q2y, zpt = parse_bin(key)
    fitted_names.add(histo_name(q2y, zpt))
unfitted = [name for name in phi_names if(name not in fitted_names)]
infile.Close()
ratios.sort()
median = ratios[len(ratios) // 2] if(ratios) else None
misses.sort(key=lambda item: item["stored_ratio"] - item["free_ratio"], reverse=True)
summary = {
    "n_cells": n_cells,
    "n_ratios": len(ratios),
    "median_chi2_ndf": median,
    "p90": ratios[int(0.9 * (len(ratios) - 1))] if(ratios) else None,
    "max_ratio": ratios[-1] if(ratios) else None,
    "n_suspect_tested": len(rows),
    "n_improved": len(misses),
    "family_counts": family_counts,
    "nbins_seen": nbins_seen,
    "missing_histo": missing_histo,
    "empty_histo": empty_histo,
    "unfitted_phi": unfitted,
    "misses": misses,
    "high_tail": sorted(rows, key=lambda item: item["stored_ratio"], reverse=True)[:20],
    "collapsed": collapsed,
}
out_path = os.path.join(dest, "review_pass1.json")
with open(out_path, "w") as handle:
    json.dump(summary, handle, indent=2)
print("n_cells", n_cells)
print("median", median)
print("p90", summary["p90"])
print("max", summary["max_ratio"])
print("families", family_counts)
print("nbins", nbins_seen)
print("tested", len(rows))
print("improved", len(misses))
print("unfitted", len(unfitted))
print("missing", len(missing_histo))
print("empty", len(empty_histo))
for item in misses:
    print("MISS", item["q2y"], item["zpt"], "stored", round(item["stored_ratio"], 3), "free", round(item["free_ratio"], 3), "B", round(item["B"], 4), "->", round(item["freeB"], 4), "C", round(item["C"], 4), "->", round(item["freeC"], 4), "bhit", item["b_hit"], "chit", item["c_hit"], "filled", item["filled"])
print("TAIL")
for item in summary["high_tail"]:
    print("TAIL", item["q2y"], item["zpt"], round(item["stored_ratio"], 3), round(item["free_ratio"], 3), round(item["rel"], 3), "dB", round(item["freeB"] - item["B"], 4), "dC", round(item["freeC"] - item["C"], 4), "hit", item["b_hit"], item["c_hit"])
print("COLLAPSED", len(collapsed))
