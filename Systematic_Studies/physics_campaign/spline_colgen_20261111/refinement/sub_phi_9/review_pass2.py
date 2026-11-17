import json
import math
import os
import importlib.util
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/sub_phi_9"
fit_path = os.path.join(dest, "fit_pass2.json")
root_path = os.path.join(dest, "histograms.root")
init_path = os.path.join(dest, "refine_init.py")
overlay_dir = os.path.join(dest, "overlays_pass2")
os.makedirs(overlay_dir, exist_ok=True)

spec = importlib.util.spec_from_file_location("refine_init", init_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
guide = mod.special_fit_parameters_set

def settings_for(q2y, zpt):
    candidates = [(q2y, zpt, "3D", "BC"), (q2y, zpt, "BC"), (q2y, zpt)]
    for key in candidates:
        if(key in guide):
            return key, guide[key]
    return None, None

def histo_name(q2y, zpt):
    return "(MultiDim_3D_Histo)_(BC_RC_Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)

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
        row = {
            "ratio": chi2 / float(ndf),
            "chi2": chi2,
            "ndf": ndf,
            "A": func.GetParameter(0),
            "B": func.GetParameter(1),
            "C": func.GetParameter(2),
            "Berr": func.GetParError(1),
            "Cerr": func.GetParError(2),
        }
        if((best is None) or (row["ratio"] < best["ratio"])):
            best = row
    return best

def parse_bin(key):
    left, right = key.split(")-(")
    q2y = left.split("_Bin_")[-1]
    zpt = right.split("_Bin_")[-1].rstrip(")")
    return q2y, zpt

def on_limit(value, limits):
    if((value is None) or (not limits)):
        return False
    numeric = [item for item in limits if(isinstance(item, (int, float)))]
    if(len(numeric) < 2):
        return False
    lo = min(numeric)
    hi = max(numeric)
    if((abs(value - lo) < 1.0e-3) or (abs(value - hi) < 1.0e-3)):
        return True
    return False

with open(fit_path) as handle:
    payload = json.load(handle)
cells = payload["Fit_Pars_from_3D_BC_RC_Bayesian"]
infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")

rows = []
misses = []
ratios = []
for key in cells:
    cell = cells[key]
    chi2 = cell.get("Chi2")
    ndf = cell.get("NDF")
    par_b = cell.get("Fit_Par_B")
    par_c = cell.get("Fit_Par_C")
    err_b = cell.get("Fit_Par_B_ERR")
    err_c = cell.get("Fit_Par_C_ERR")
    par_a = cell.get("Fit_Par_A")
    if((ndf is None) or (ndf == 0) or (chi2 is None) or (not math.isfinite(chi2))):
        continue
    stored_ratio = chi2 / float(ndf)
    ratios.append(stored_ratio)
    q2y, zpt = parse_bin(key)
    guide_key, settings = settings_for(q2y, zpt)
    b_hit = False
    c_hit = False
    if(settings):
        b_hit = on_limit(par_b, settings.get("B_limits"))
        c_hit = on_limit(par_c, settings.get("C_limits"))
    suspect = False
    if(stored_ratio >= 2.5):
        suspect = True
    if((err_b is not None) and (abs(err_b) < 1.0e-6)):
        suspect = True
    if((err_c is not None) and (abs(err_c) < 1.0e-6)):
        suspect = True
    if((par_b is not None) and (abs(par_b) >= 0.9)):
        suspect = True
    if((par_c is not None) and (abs(par_c) >= 0.9)):
        suspect = True
    if(b_hit or c_hit):
        suspect = True
    if(not suspect):
        continue
    name = histo_name(q2y, zpt)
    histo = infile.Get(name)
    if((not histo) or (histo.Integral() == 0)):
        continue
    fitted = free_fit(histo)
    if(fitted is None):
        continue
    rel = 0.0
    if(fitted["ratio"] > 0):
        rel = (stored_ratio - fitted["ratio"]) / fitted["ratio"]
    outside = False
    if(settings):
        b_limits = settings.get("B_limits")
        c_limits = settings.get("C_limits")
        b_numeric = [item for item in (b_limits or []) if(isinstance(item, (int, float)))]
        c_numeric = [item for item in (c_limits or []) if(isinstance(item, (int, float)))]
        if((len(b_numeric) >= 2) and ((fitted["B"] < min(b_numeric) - 0.01) or (fitted["B"] > max(b_numeric) + 0.01))):
            outside = True
        if((len(c_numeric) >= 2) and ((fitted["C"] < min(c_numeric) - 0.01) or (fitted["C"] > max(c_numeric) + 0.01))):
            outside = True
    delta_b = abs((par_b or 0.0) - fitted["B"])
    delta_c = abs((par_c or 0.0) - fitted["C"])
    improved = (stored_ratio - fitted["ratio"] > 0.25) and (rel > 0.12) and (abs(fitted["B"]) < 0.94) and (abs(fitted["C"]) < 0.94) and ((outside) or (b_hit) or (c_hit) or (delta_b > 0.03) or (delta_c > 0.03))
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
        "b_hit": b_hit,
        "c_hit": c_hit,
        "outside": outside,
        "improved": improved,
        "guide_key": None if(guide_key is None) else list(guide_key),
    }
    rows.append(record)
    draw = improved or (stored_ratio >= 4.0)
    if(draw):
        lo, hi = filled_range(histo)
        canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
        histo.SetTitle("Q2y %s zpt %s stored %.2f free %.2f" % (q2y, zpt, stored_ratio, fitted["ratio"]))
        histo.SetStats(0)
        histo.Draw("E")
        stored_func = ROOT.TF1("stored_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
        stored_func.SetParameters(par_a, par_b, par_c)
        stored_func.SetLineColor(ROOT.kRed)
        stored_func.SetLineWidth(2)
        stored_func.Draw("SAME")
        free_func = ROOT.TF1("freedraw_%s_%s" % (q2y, zpt), "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))", lo, hi)
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
misses.sort(key=lambda item: item["stored_ratio"] - item["free_ratio"], reverse=True)
summary = {
    "n_cells": len(cells),
    "n_ratios": len(ratios),
    "median_chi2_ndf": median,
    "n_suspect_tested": len(rows),
    "n_improved": len(misses),
    "misses": misses,
    "high_tail": sorted(rows, key=lambda item: item["stored_ratio"], reverse=True)[:15],
}
out_path = os.path.join(dest, "review_pass2.json")
with open(out_path, "w") as handle:
    json.dump(summary, handle, indent=2)
print("n_cells", len(cells))
print("median", median)
print("tested", len(rows))
print("improved", len(misses))
for item in misses:
    print("MISS", item["q2y"], item["zpt"], "stored", round(item["stored_ratio"], 3), "free", round(item["free_ratio"], 3), "B", round(item["B"], 4), "->", round(item["freeB"], 4), "C", round(item["C"], 4), "->", round(item["freeC"], 4), "bhit", item["b_hit"], "chit", item["c_hit"], "out", item["outside"], "key", item["guide_key"])
print("TAIL")
for item in summary["high_tail"]:
    print("TAIL", item["q2y"], item["zpt"], round(item["stored_ratio"], 3), round(item["free_ratio"], 3), "imp", item["improved"], "C", round(item["C"], 4), round(item["freeC"], 4))
