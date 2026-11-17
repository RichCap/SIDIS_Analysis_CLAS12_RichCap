# Compare the stored Bayesian phi fits with a wide |B|,|C|<0.95 refit.
import json
import math
import os
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

ref_dir = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/pcalvol_loose_bayes_inherited"
root_path = os.path.join(ref_dir, "histograms.root")
fit_path = os.path.join(ref_dir, "fit_pass1.json")
overlay_dir = os.path.join(ref_dir, "overlays")
pi_text = "3.1415926"
formula = "[0]*(1 + [1]*cos(x*(" + pi_text + "/180)) + [2]*cos(2*x*(" + pi_text + "/180)))"

with open(fit_path) as handle:
    payload = json.load(handle)
cells = payload["Fit_Pars_from_3D_Bayesian"]
infile = ROOT.TFile.Open(root_path, "READ")
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
    best = None
    for start_b, start_c in ((0.0, 0.0), (stored_b, stored_c)):
        func = ROOT.TF1("free_%s_%s" % (q2y, zpt), formula, fit_range_lower, fit_range_upper)
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
    b_wall = abs(abs(free_b) - 0.95) < 0.002
    c_wall = abs(abs(free_c) - 0.95) < 0.002
    finite = True
    for value in (best["A"], free_b, free_c, best["Aerr"], best["Berr"], best["Cerr"], best["chi2"], best["ndf"]):
        if((value != value) or (abs(value) == float("inf"))):
            finite = False
    rel = float("nan")
    if((stored_ratio == stored_ratio) and (best["ratio"] == best["ratio"]) and (best["ratio"] > 0)):
        rel = (stored_ratio - best["ratio"]) / best["ratio"]
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
        "B": stored_b,
        "Berr": stored_berr,
        "C": stored_c,
        "Cerr": stored_cerr,
        "freeA": best["A"],
        "freeB": free_b,
        "freeBerr": best["Berr"],
        "freeC": free_c,
        "freeCerr": best["Cerr"],
        "b_wall": b_wall,
        "c_wall": c_wall,
        "finite": finite,
        "zero_bins": zero_bins,
        "filled": filled,
        "range": [fit_range_lower, fit_range_upper],
        "func": best["func"],
        "histo": histo,
        "name": name,
    }
    if((not finite) or (stored_a <= 0) or (abs(stored_b) >= 1) or (abs(stored_c) >= 1) or (stored_berr <= 0) or (stored_cerr <= 0) or (stored_chi2 <= 0) or (stored_ndf <= 0)):
        bad.append(key)
    rows.append(row)

ratios = sorted([row["stored_ratio"] for row in rows if(row["stored_ratio"] == row["stored_ratio"])])
median = ratios[len(ratios) // 2] if(len(ratios) > 0) else float("nan")
misses = []
for row in rows:
    if((row["rel"] != row["rel"]) or (not row["finite"])):
        continue
    if((row["b_wall"]) or (row["c_wall"])):
        continue
    moved = (abs(row["freeB"] - row["B"]) > 0.02) or (abs(row["freeC"] - row["C"]) > 0.02)
    improved = (row["stored_ratio"] > row["free_ratio"] + 0.45) and (row["stored_ratio"] > 1.2 * row["free_ratio"])
    if(moved and improved):
        misses.append(row)
misses.sort(key=lambda row: row["rel"], reverse=True)
high = sorted(rows, key=lambda row: row["stored_ratio"] if(row["stored_ratio"] == row["stored_ratio"]) else -1, reverse=True)
draw_ids = []
for row in misses[:16]:
    draw_ids.append((row["q2y"], row["zpt"]))
for row in high[:8]:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        draw_ids.append(ident)
drawn = []
for row in rows:
    ident = (row["q2y"], row["zpt"])
    if(ident not in draw_ids):
        row["func"].IsA().Destructor(row["func"])
        continue
    canvas = ROOT.TCanvas("c_%s_%s" % ident, "c", 900, 650)
    row["histo"].SetTitle("Q2_y %s z_pT %s  stored %.2f  free %.2f" % (ident[0], ident[1], row["stored_ratio"], row["free_ratio"]))
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
    "median_stored_ratio": median,
    "n_misses": len(misses),
    "misses": [slim(row) for row in misses],
    "high_stored": [slim(row) for row in high[:12]],
    "drawn": drawn,
}
with open(os.path.join(ref_dir, "review_pass1.json"), "w") as handle:
    json.dump(report, handle, indent=2)
print("n_cells", len(cells))
print("n_fit", len(rows))
print("missing", len(missing))
print("empty", len(empty))
print("bad", len(bad))
print("median", median)
print("n_misses", len(misses))
for row in misses[:25]:
    print("MISS", row["q2y"], row["zpt"], "stored", round(row["stored_ratio"], 3), "free", round(row["free_ratio"], 3), "rel", round(row["rel"], 3), "B", round(row["B"], 4), "->", round(row["freeB"], 4), "C", round(row["C"], 4), "->", round(row["freeC"], 4), "filled", row["filled"])
print("HIGH")
for row in high[:12]:
    print("HIGH", row["q2y"], row["zpt"], "stored", round(row["stored_ratio"], 3), "free", round(row["free_ratio"], 3), "B", round(row["B"], 4), "freeB", round(row["freeB"], 4), "C", round(row["C"], 4), "freeC", round(row["freeC"], 4))
infile.Close()
