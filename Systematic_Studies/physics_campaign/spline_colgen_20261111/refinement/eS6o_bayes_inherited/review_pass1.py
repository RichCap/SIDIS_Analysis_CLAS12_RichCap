# Compare stored Bayesian phi fits with a wide refit and draw the misses.
import json
import os
import importlib.util
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

base = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/eS6o_bayes_inherited"
root_path = os.path.join(base, "histograms.root")
fit_path = os.path.join(base, "fit_pass1.json")
init_path = os.path.join(base, "refine_init.py")
overlay_dir = os.path.join(base, "overlays")
os.makedirs(overlay_dir, exist_ok=True)
pi_text = "3.1415926"
formula = "[0]*(1 + [1]*cos(x*(" + pi_text + "/180)) + [2]*cos(2*x*(" + pi_text + "/180)))"

spec = importlib.util.spec_from_file_location("refine_init", init_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
guide = module.special_fit_parameters_set

with open(fit_path) as handle:
    payload = json.load(handle)
cells = payload["Fit_Pars_from_3D_Bayesian"]
infile = ROOT.TFile.Open(root_path, "READ")
if((infile is None) or (infile.IsZombie())):
    raise SystemExit("root open failed")

family_counts = {"Bayesian": 0, "RC_Bayesian": 0, "BC_RC_Bayesian": 0, "Bin": 0, "5D": 0, "other_phi": 0, "empty_bayes": 0}
empty_names = []
for key in infile.GetListOfKeys():
    name = str(key.GetName())
    if("MultiDim_5D_Histo" in name):
        family_counts["5D"] += 1
    if("MultiDim_3D_Histo" not in name):
        continue
    if("phi" not in name):
        continue
    if("Bin_All" in name):
        continue
    if("_(Normalized)" in name):
        continue
    if("_AsymErr" in name):
        continue
    if(")_(Bayesian)_(" in name):
        family_counts["Bayesian"] += 1
        histo = infile.Get(name)
        if((histo) and (float(histo.Integral()) <= 0)):
            family_counts["empty_bayes"] += 1
            empty_names.append(name)
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

rows = []
missing = []
empty = []
bad = []
for key in sorted(cells):
    q2y = key.split(")-(z_pT_Bin_")[0].replace("(Q2_y_Bin_", "")
    zpt = key.split(")-(z_pT_Bin_")[1].replace(")", "")
    name = "(MultiDim_3D_Histo)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)
    histo = infile.Get(name)
    cell = cells[key]
    if((not histo) or (str(histo) in ["None"])):
        missing.append(key)
        continue
    integral = float(histo.Integral())
    if(integral <= 0):
        empty.append(key)
        continue
    n_bins = int(histo.GetNbinsX())
    fit_range_lower = 0.0
    fit_range_upper = 360.0
    filled = 0
    zero_bins = 0
    a_sum = 0.0
    for bin_index in range(1, n_bins + 1):
        content = float(histo.GetBinContent(bin_index))
        if(content != 0):
            filled += 1
            a_sum += content
            if(filled == 1):
                fit_range_lower = float(histo.GetXaxis().GetBinLowEdge(bin_index))
        else:
            zero_bins += 1
    for bin_index in range(n_bins, 0, -1):
        if(float(histo.GetBinContent(bin_index)) != 0):
            fit_range_upper = float(histo.GetXaxis().GetBinUpEdge(bin_index))
            break
    a0 = a_sum / float(filled) if(filled > 0) else 1.0
    stored_chi2 = float(cell["Chi2"])
    stored_ndf = float(cell["NDF"])
    stored_ratio = stored_chi2 / stored_ndf if(stored_ndf > 0) else float("nan")
    stored_b = float(cell["Fit_Par_B"])
    stored_c = float(cell["Fit_Par_C"])
    stored_berr = float(cell["Fit_Par_B_ERR"])
    stored_cerr = float(cell["Fit_Par_C_ERR"])
    stored_a = float(cell["Fit_Par_A"])
    stored_aerr = float(cell["Fit_Par_A_ERR"])
    settings = guide_for(q2y, zpt)
    b_limits = None if(settings is None) else settings.get("B_limits")
    c_limits = None if(settings is None) else settings.get("C_limits")
    best = None
    for start_b, start_c in ((0.0, 0.0), (stored_b, stored_c), (stored_b, 0.0), (0.0, stored_c)):
        func = ROOT.TF1("free_%s_%s_%d" % (q2y, zpt, int(1000 * start_b + 50 * start_c)), formula, fit_range_lower, fit_range_upper)
        func.SetParameter(0, max(abs(a0), 1e-6))
        func.SetParLimits(0, 0.0, max(abs(a0) * 20.0, 1.0))
        func.SetParameter(1, start_b)
        func.SetParLimits(1, -0.95, 0.95)
        func.SetParameter(2, start_c)
        func.SetParLimits(2, -0.95, 0.95)
        histo.Fit(func, "QRN0")
        chi2 = float(func.GetChisquare())
        ndf = float(func.GetNDF())
        ratio = chi2 / ndf if(ndf > 0) else float("nan")
        candidate = {
            "func": func,
            "chi2": chi2,
            "ndf": ndf,
            "ratio": ratio,
            "A": float(func.GetParameter(0)),
            "B": float(func.GetParameter(1)),
            "C": float(func.GetParameter(2)),
            "Aerr": float(func.GetParError(0)),
            "Berr": float(func.GetParError(1)),
            "Cerr": float(func.GetParError(2)),
        }
        if((best is None) or ((ratio == ratio) and (best["ratio"] != best["ratio"])) or ((ratio == ratio) and (ratio < best["ratio"]))):
            if(best is not None):
                best["func"].IsA().Destructor(best["func"])
            best = candidate
        else:
            func.IsA().Destructor(func)
    free_b = best["B"]
    free_c = best["C"]
    b_wall = abs(abs(free_b) - 0.95) < 0.015
    c_wall = abs(abs(free_c) - 0.95) < 0.015
    finite = True
    for value in (best["A"], free_b, free_c, best["Aerr"], best["Berr"], best["Cerr"], best["chi2"], best["ndf"], stored_a, stored_b, stored_c, stored_aerr, stored_berr, stored_cerr, stored_chi2, stored_ndf):
        if((value != value) or (abs(value) == float("inf"))):
            finite = False
    rel = float("nan")
    if((stored_ratio == stored_ratio) and (best["ratio"] == best["ratio"]) and (best["ratio"] > 0)):
        rel = stored_ratio / best["ratio"]
    row = {
        "q2y": q2y,
        "zpt": zpt,
        "stored_ratio": stored_ratio,
        "free_ratio": best["ratio"],
        "rel": rel,
        "stored_chi2": stored_chi2,
        "free_chi2": best["chi2"],
        "ndf": stored_ndf,
        "free_ndf": best["ndf"],
        "A": stored_a,
        "Aerr": stored_aerr,
        "B": stored_b,
        "Berr": stored_berr,
        "C": stored_c,
        "Cerr": stored_cerr,
        "freeA": best["A"],
        "freeB": free_b,
        "freeBerr": best["Berr"],
        "freeC": free_c,
        "freeCerr": best["Cerr"],
        "b_limits": b_limits,
        "c_limits": c_limits,
        "b_edge": on_edge(stored_b, b_limits),
        "c_edge": on_edge(stored_c, c_limits),
        "b_wall": b_wall,
        "c_wall": c_wall,
        "finite": finite,
        "zero_bins": zero_bins,
        "filled": filled,
        "range": [fit_range_lower, fit_range_upper],
        "dB": free_b - stored_b,
        "dC": free_c - stored_c,
        "func": best["func"],
        "histo": histo,
        "name": name,
    }
    if((not finite) or (stored_a <= 0) or (abs(stored_b) >= 1) or (abs(stored_c) >= 1) or (stored_berr <= 0) or (stored_cerr <= 0) or (stored_chi2 <= 0) or (stored_ndf <= 0)):
        bad.append(key)
    rows.append(row)

def is_miss(row):
    if((not row["finite"]) or (row["b_wall"]) or (row["c_wall"])):
        return False
    if((abs(row["freeB"]) >= 0.9) or (abs(row["freeC"]) >= 0.9)):
        return False
    failed_store = (row["ndf"] <= 0) or (abs(row["B"]) >= 1) or (abs(row["C"]) >= 1) or (row["Berr"] <= 0) or (row["Cerr"] <= 0)
    if(failed_store and (row["free_ndf"] > 0) and (row["free_ratio"] == row["free_ratio"])):
        return True
    if((row["stored_ratio"] != row["stored_ratio"]) or (row["free_ratio"] != row["free_ratio"])):
        return False
    moved = (abs(row["dB"]) > 0.03) or (abs(row["dC"]) > 0.03)
    better = (row["stored_ratio"] > (row["free_ratio"] + 0.35)) and (row["rel"] == row["rel"]) and (row["rel"] >= 1.25)
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
    strong = (row["rel"] >= 1.8) or ((row["stored_ratio"] - row["free_ratio"]) >= 1.0)
    return narrow or collapsed or strong

misses = [row for row in rows if(is_miss(row))]
misses.sort(key=lambda row: (row["stored_ratio"] - row["free_ratio"]) if((row["stored_ratio"] == row["stored_ratio"]) and (row["free_ratio"] == row["free_ratio"])) else 999.0, reverse=True)
ratios = sorted(row["stored_ratio"] for row in rows if(row["stored_ratio"] == row["stored_ratio"]))
median = ratios[len(ratios) // 2] if(ratios) else None
high = sorted(rows, key=lambda row: row["stored_ratio"] if(row["stored_ratio"] == row["stored_ratio"]) else -1, reverse=True)
draw_ids = []
for row in misses[:24]:
    draw_ids.append((row["q2y"], row["zpt"]))
for row in high[:10]:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        draw_ids.append(ident)
for row in rows:
    if((row["filled"] <= 4) or (abs(row["B"]) >= 1) or (abs(row["C"]) >= 1)):
        ident = (row["q2y"], row["zpt"])
        if((ident not in draw_ids) and (len(draw_ids) < 36)):
            draw_ids.append(ident)
drawn = []
for row in rows:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        row["func"].IsA().Destructor(row["func"])
        continue
    canvas = ROOT.TCanvas("c_%s_%s" % ident, "c", 900, 650)
    stored_title = row["stored_ratio"] if(row["stored_ratio"] == row["stored_ratio"]) else -1.0
    free_title = row["free_ratio"] if(row["free_ratio"] == row["free_ratio"]) else -1.0
    row["histo"].SetTitle("Q2_y %s z_pT %s  stored %.2f  free %.2f" % (ident[0], ident[1], stored_title, free_title))
    row["histo"].SetMarkerStyle(20)
    row["histo"].Draw("E")
    stored_name = row["name"].replace("(MultiDim_3D_Histo)", "(Fit_Function)")
    stored = infile.Get(stored_name)
    if(stored):
        stored.SetLineColor(ROOT.kRed)
        stored.SetLineWidth(2)
        stored.Draw("same")
    row["func"].SetLineColor(ROOT.kBlue)
    row["func"].SetLineWidth(2)
    row["func"].Draw("same")
    out_png = os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % ident)
    canvas.SaveAs(out_png)
    drawn.append(out_png)
    canvas.IsA().Destructor(canvas)
    row["func"].IsA().Destructor(row["func"])

def slim(row):
    out = {}
    for key_name in row:
        if(key_name not in ["func", "histo", "name"]):
            out[key_name] = row[key_name]
    return out

report = {
    "n_cells": len(cells),
    "n_fit": len(rows),
    "missing": missing,
    "empty": empty,
    "bad": bad,
    "empty_names": empty_names,
    "family_counts": family_counts,
    "median_stored_ratio": median,
    "n_misses": len(misses),
    "misses": [slim(row) for row in misses],
    "high_stored": [slim(row) for row in high[:20]],
    "drawn": drawn,
}
with open(os.path.join(base, "review_pass1.json"), "w") as handle:
    json.dump(report, handle, indent=2)
print("n_cells", len(cells))
print("n_fit", len(rows))
print("missing", len(missing))
print("empty", len(empty))
print("bad", len(bad))
print("families", family_counts)
print("median", median)
print("n_misses", len(misses))
for row in misses:
    stored_print = row["stored_ratio"] if(row["stored_ratio"] == row["stored_ratio"]) else float("nan")
    free_print = row["free_ratio"] if(row["free_ratio"] == row["free_ratio"]) else float("nan")
    print("MISS", row["q2y"], row["zpt"], "stored", round(stored_print, 3), "free", round(free_print, 3), "ndf", row["ndf"], "free_ndf", row["free_ndf"], "B", round(row["B"], 4), "->", round(row["freeB"], 4), "C", round(row["C"], 4), "->", round(row["freeC"], 4), "edge", row["b_edge"], row["c_edge"], "Berr", round(row["Berr"], 4), "Cerr", round(row["Cerr"], 4), "filled", row["filled"], "limits", row["b_limits"], row["c_limits"])
print("HIGH")
for row in high[:15]:
    print("HIGH", row["q2y"], row["zpt"], "stored", round(row["stored_ratio"], 3), "free", round(row["free_ratio"], 3), "B", round(row["B"], 4), "freeB", round(row["freeB"], 4), "C", round(row["C"], 4), "freeC", round(row["freeC"], 4), "dB", round(row["dB"], 4), "dC", round(row["dC"], 4), "filled", row["filled"], "edge", row["b_edge"], row["c_edge"])
print("BAD")
for key_name in bad:
    print(key_name)
print("SPARSE")
for row in rows:
    if(row["filled"] <= 4):
        print("SPARSE", row["q2y"], row["zpt"], "filled", row["filled"], "stored", row["stored_ratio"], "free", row["free_ratio"], "B", row["B"], "C", row["C"], "ndf", row["ndf"])
infile.Close()
