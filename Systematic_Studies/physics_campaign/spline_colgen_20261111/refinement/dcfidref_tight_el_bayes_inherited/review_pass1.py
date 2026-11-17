import json
import math
import os
import importlib.util
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

base = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/dcfidref_tight_el_bayes_inherited"
root_path = os.path.join(base, "histograms.root")
fit_path = os.path.join(base, "fit_pass1.json")
init_path = os.path.join(base, "refine_init.py")
out_path = os.path.join(base, "review_pass1.json")
overlay_dir = os.path.join(base, "overlays")
os.makedirs(overlay_dir, exist_ok=True)

spec = importlib.util.spec_from_file_location("refine_init", init_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
guide = module.special_fit_parameters_set

with open(fit_path) as handle:
    fit_json = json.load(handle)
cells = fit_json["Fit_Pars_from_3D_Bayesian"]

infile = ROOT.TFile.Open(root_path, "READ")
if((infile is None) or (infile.IsZombie())):
    raise SystemExit("root open failed")

family_counts = {"Bayesian": 0, "RC_Bayesian": 0, "BC_RC_Bayesian": 0, "Bin": 0, "5D": 0, "other_phi": 0}
for key in infile.GetListOfKeys():
    name = str(key.GetName())
    if("MultiDim_5D_Histo" in name):
        family_counts["5D"] += 1
    if("MultiDim_3D_Histo" not in name):
        continue
    if("phi" not in name):
        continue
    if(")_(Bayesian)_(" in name):
        family_counts["Bayesian"] += 1
    elif(")_(RC_Bayesian)_(" in name):
        family_counts["RC_Bayesian"] += 1
    elif(")_(BC_RC_Bayesian)_(" in name):
        family_counts["BC_RC_Bayesian"] += 1
    elif(")_(Bin)_(" in name):
        family_counts["Bin"] += 1
    else:
        family_counts["other_phi"] += 1

def guide_for(q2y, zpt):
    for key in ((q2y, zpt, "3D"), (q2y, zpt)):
        if(key in guide):
            return guide[key]
    return None

def on_edge(value, limits):
    if(not limits):
        return False
    lo, hi = sorted(float(x) for x in limits)
    span = max(hi - lo, 1e-6)
    tol = max(0.002, 0.02 * span)
    return (abs(value - lo) <= tol) or (abs(value - hi) <= tol)

def finite_number(value):
    return (value is not None) and math.isfinite(float(value))

def free_fit(histo, xmin, xmax, start_b, start_c):
    formula = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
    func = ROOT.TF1("free_fit", formula, float(xmin), float(xmax))
    peak = 0.0
    for bin_index in range(1, histo.GetNbinsX() + 1):
        peak = max(peak, float(histo.GetBinContent(bin_index)))
    start_a = max(peak, 1.0)
    best = None
    best_func = None
    starts = [(start_b, start_c), (0.0, 0.0), (start_b, 0.0), (0.0, start_c)]
    for b0, c0 in starts:
        func.SetParameter(0, start_a)
        func.SetParLimits(0, 0.0, max(start_a * 8.0, 1.0))
        func.SetParameter(1, float(b0))
        func.SetParLimits(1, -0.95, 0.95)
        func.SetParameter(2, float(c0))
        func.SetParLimits(2, -0.95, 0.95)
        histo.Fit(func, "QRB0")
        chi2 = float(func.GetChisquare())
        ndf = float(func.GetNDF())
        pars = [float(func.GetParameter(i)) for i in range(3)]
        errs = [float(func.GetParError(i)) for i in range(3)]
        if(not all(finite_number(v) for v in pars + errs + [chi2, ndf])):
            continue
        if(ndf <= 0):
            continue
        ratio = chi2 / ndf
        if((best is None) or (ratio < best["ratio"])):
            best = {"A": pars[0], "B": pars[1], "C": pars[2], "Aerr": errs[0], "Berr": errs[1], "Cerr": errs[2], "chi2": chi2, "ndf": ndf, "ratio": ratio}
            best_func = func.Clone("free_keep")
    return best, best_func

rows = []
ratios = []
bad_finite = []
for bin_key, cell in cells.items():
    q2y = bin_key.split(")-(z_pT_Bin_")[0].replace("(Q2_y_Bin_", "")
    zpt = bin_key.split(")-(z_pT_Bin_")[1].replace(")", "")
    histo_name = "(MultiDim_3D_Histo)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)
    fit_name = histo_name.replace("MultiDim_3D_Histo", "Fit_Function")
    histo = infile.Get(histo_name)
    stored_func = infile.Get(fit_name)
    if(histo is None):
        rows.append({"q2y": q2y, "zpt": zpt, "missing_histo": True})
        continue
    chi2 = float(cell["Chi2"])
    ndf = float(cell["NDF"])
    b_val = float(cell["Fit_Par_B"])
    c_val = float(cell["Fit_Par_C"])
    b_err = float(cell["Fit_Par_B_ERR"])
    c_err = float(cell["Fit_Par_C_ERR"])
    a_val = float(cell["Fit_Par_A"])
    a_err = float(cell["Fit_Par_A_ERR"])
    ratio = chi2 / ndf if(ndf) else float("nan")
    ratios.append(ratio)
    if(not all(finite_number(v) for v in [chi2, ndf, b_val, c_val, b_err, c_err, a_val, a_err])):
        bad_finite.append((q2y, zpt))
    settings = guide_for(q2y, zpt)
    b_limits = None if(settings is None) else settings.get("B_limits")
    c_limits = None if(settings is None) else settings.get("C_limits")
    xmin = float(stored_func.GetXmin()) if(stored_func is not None) else 0.0
    xmax = float(stored_func.GetXmax()) if(stored_func is not None) else 360.0
    filled = 0
    zeros = 0
    integral = float(histo.Integral())
    for bin_index in range(1, histo.GetNbinsX() + 1):
        center = float(histo.GetBinCenter(bin_index))
        if((center < xmin) or (center > xmax)):
            continue
        if(float(histo.GetBinContent(bin_index)) == 0.0):
            zeros += 1
        else:
            filled += 1
    clone = histo.Clone("review_%s_%s" % (q2y, zpt))
    clone.SetDirectory(0)
    free, free_func = free_fit(clone, xmin, xmax, b_val, c_val)
    row = {
        "q2y": q2y,
        "zpt": zpt,
        "ratio": ratio,
        "chi2": chi2,
        "ndf": ndf,
        "A": a_val,
        "Aerr": a_err,
        "B": b_val,
        "Berr": b_err,
        "C": c_val,
        "Cerr": c_err,
        "b_limits": b_limits,
        "c_limits": c_limits,
        "b_edge": on_edge(b_val, b_limits),
        "c_edge": on_edge(c_val, c_limits),
        "filled": filled,
        "zeros": zeros,
        "integral": integral,
        "xmin": xmin,
        "xmax": xmax,
        "histo": clone,
        "free_func": free_func,
        "histo_name": histo_name,
    }
    if(free is None):
        row["free_failed"] = True
    else:
        row["free_ratio"] = free["ratio"]
        row["freeB"] = free["B"]
        row["freeC"] = free["C"]
        row["freeBerr"] = free["Berr"]
        row["freeCerr"] = free["Cerr"]
        row["freeA"] = free["A"]
        row["dB"] = free["B"] - b_val
        row["dC"] = free["C"] - c_val
        row["rel"] = ratio / free["ratio"] if(free["ratio"] > 0) else None
    rows.append(row)

def is_miss(row):
    if(row.get("free_failed") or ("free_ratio" not in row)):
        return False
    if((not math.isfinite(row["ratio"])) or (not math.isfinite(row["free_ratio"]))):
        return False
    if((abs(row["freeB"]) >= 0.9) or (abs(row["freeC"]) >= 0.9)):
        return False
    if((abs(abs(row["freeB"]) - 0.95) < 0.015) or (abs(abs(row["freeC"]) - 0.95) < 0.015)):
        return False
    moved = (abs(row["dB"]) > 0.03) or (abs(row["dC"]) > 0.03)
    better = (row["ratio"] > (row["free_ratio"] + 0.35)) and (row["rel"] is not None) and (row["rel"] >= 1.25)
    if((not moved) or (not better)):
        return False
    narrow = False
    if(row["b_limits"]):
        lo, hi = sorted(row["b_limits"])
        narrow = narrow or ((hi - lo) < 0.08) or (row["freeB"] < lo) or (row["freeB"] > hi) or row["b_edge"]
    if(row["c_limits"]):
        lo, hi = sorted(row["c_limits"])
        narrow = narrow or ((hi - lo) < 0.08) or (row["freeC"] < lo) or (row["freeC"] > hi) or row["c_edge"]
    collapsed = ((row["Berr"] < 0.002) and (abs(row["dB"]) > 0.03)) or ((row["Cerr"] < 0.002) and (abs(row["dC"]) > 0.03))
    strong = (row["rel"] >= 1.8) or ((row["ratio"] - row["free_ratio"]) >= 1.0)
    return narrow or collapsed or strong

misses = [row for row in rows if(is_miss(row))]
misses.sort(key=lambda row: row["ratio"] - row["free_ratio"], reverse=True)
clean_ratios = sorted(r for r in ratios if(math.isfinite(r)))
median = clean_ratios[len(clean_ratios) // 2] if(clean_ratios) else None
worst = sorted([row for row in rows if(("ratio" in row) and math.isfinite(row["ratio"]))], key=lambda row: row["ratio"], reverse=True)[:12]
draw_ids = []
for row in misses[:24]:
    draw_ids.append((row["q2y"], row["zpt"]))
for row in worst:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        draw_ids.append(ident)
drawn = []
for row in rows:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        continue
    canvas = ROOT.TCanvas("c_%s_%s" % ident, "c", 900, 650)
    title_ratio = row["ratio"]
    title_free = row.get("free_ratio", float("nan"))
    row["histo"].SetTitle("Q2_y %s z_pT %s  stored %.2f  free %.2f" % (ident[0], ident[1], title_ratio, title_free))
    row["histo"].SetMarkerStyle(20)
    row["histo"].Draw("E")
    stored = infile.Get(row["histo_name"].replace("(MultiDim_3D_Histo)", "(Fit_Function)"))
    if(stored):
        stored.SetLineColor(ROOT.kRed)
        stored.SetLineWidth(2)
        stored.Draw("same")
    if(row.get("free_func") is not None):
        row["free_func"].SetLineColor(ROOT.kBlue)
        row["free_func"].SetLineWidth(2)
        row["free_func"].Draw("same")
    out_png = os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % ident)
    canvas.SaveAs(out_png)
    drawn.append(out_png)
    canvas.IsA().Destructor(canvas)

def slim(row):
    keep = ("q2y", "zpt", "ratio", "free_ratio", "chi2", "ndf", "A", "Aerr", "B", "Berr", "C", "Cerr", "b_limits", "c_limits", "b_edge", "c_edge", "filled", "zeros", "integral", "xmin", "xmax", "freeB", "freeC", "freeBerr", "freeCerr", "freeA", "dB", "dC", "rel", "free_failed", "missing_histo")
    return {key: row[key] for key in keep if(key in row)}

summary = {
    "n_cells": len(cells),
    "n_rows": len(rows),
    "median_ratio": median,
    "family_counts": family_counts,
    "n_misses": len(misses),
    "bad_finite": bad_finite,
    "n_empty": sum(1 for row in rows if(row.get("integral", 1) == 0)),
    "misses": [slim(row) for row in misses],
    "worst": [slim(row) for row in worst],
    "drawn": drawn,
}
with open(out_path, "w") as handle:
    json.dump(summary, handle, indent=2)
infile.Close()
print("cells", len(cells), "median", median, "misses", len(misses), "empty", summary["n_empty"], "bad", len(bad_finite))
print("families", family_counts)
print("drawn", len(drawn))
for row in misses:
    print("MISS q%s z%s stored %.3f free %.3f dB %.3f dC %.3f edge %s %s B %.4f C %.4f freeB %.4f freeC %.4f Berr %.4f Cerr %.4f limitsB %s limitsC %s" % (row["q2y"], row["zpt"], row["ratio"], row["free_ratio"], row["dB"], row["dC"], row["b_edge"], row["c_edge"], row["B"], row["C"], row["freeB"], row["freeC"], row["Berr"], row["Cerr"], row["b_limits"], row["c_limits"]))
