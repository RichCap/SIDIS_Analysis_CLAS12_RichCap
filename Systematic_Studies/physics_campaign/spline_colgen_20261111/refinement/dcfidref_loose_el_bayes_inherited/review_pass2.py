import json
import math
import os
import importlib.util
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/dcfidref_loose_el_bayes_inherited"
fit_path = os.path.join(dest, "fit_pass2.json")
root_path = os.path.join(dest, "histograms.root")
init_path = os.path.join(dest, "refine_init.py")
overlay_dir = os.path.join(dest, "overlays_pass2")
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
        row = {"ratio": ratio, "A": func.GetParameter(0), "B": func.GetParameter(1), "C": func.GetParameter(2), "Berr": func.GetParError(1), "Cerr": func.GetParError(2)}
        if((best is None) or (row["ratio"] < best["ratio"])):
            best = row
    return best

def parse_bin(key):
    left, right = key.split(")-(")
    q2y = left.split("_Bin_")[-1]
    zpt = right.split("_Bin_")[-1].rstrip(")")
    return q2y, zpt

def draw_overlay(histo, q2y, zpt, par_a, par_b, par_c, fitted, stored_ratio):
    canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
    histo.SetTitle("Q2y %s zpt %s stored %.2f free %.2f" % (q2y, zpt, stored_ratio, fitted["ratio"]))
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
    canvas.SaveAs(os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % (q2y, zpt)))
    canvas.Close()

infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")

rows = []
misses = []
ratios = []
boundary = []
edited = {("3","16"),("10","11"),("14","5"),("1","19"),("13","10"),("15","15"),("7","11"),("3","29"),("3","24"),("9","7"),("10","8"),("5","31"),("7","10"),("11","3"),("16","12"),("1","22"),("11","20"),("5","7"),("15","24")}
for key in cells:
    cell = cells[key]
    chi2 = cell.get("Chi2")
    ndf = cell.get("NDF")
    par_b = cell.get("Fit_Par_B")
    par_c = cell.get("Fit_Par_C")
    err_b = cell.get("Fit_Par_B_ERR")
    err_c = cell.get("Fit_Par_C_ERR")
    par_a = cell.get("Fit_Par_A")
    q2y, zpt = parse_bin(key)
    if((ndf is None) or (ndf == 0) or (chi2 is None) or (not math.isfinite(chi2))):
        print("BAD", q2y, zpt)
        continue
    stored_ratio = chi2 / float(ndf)
    ratios.append(stored_ratio)
    settings = guide.get((q2y, zpt))
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
        if((c_limits) and (par_c is not None)):
            lo_c = min(c_limits)
            hi_c = max(c_limits)
            if((abs(par_c - lo_c) < 1e-3) or (abs(par_c - hi_c) < 1e-3)):
                c_hit = True
    if(b_hit or c_hit):
        boundary.append((q2y, zpt, b_hit, c_hit, par_b, par_c))
    suspect = stored_ratio >= 2.2
    if((err_b is not None) and (abs(err_b) < 1e-6)):
        suspect = True
    if((err_c is not None) and (abs(err_c) < 1e-6)):
        suspect = True
    if((par_b is not None) and (abs(abs(par_b) - 0.95) < 0.02)):
        suspect = True
    if(b_hit or c_hit):
        suspect = True
    draw_this = (q2y, zpt) in edited
    if((not suspect) and (not draw_this)):
        continue
    name = histo_name(q2y, zpt)
    histo = infile.Get(name)
    if((not histo) or (histo.Integral() == 0)):
        print("EMPTY", q2y, zpt)
        continue
    fitted = free_fit(histo)
    if(fitted is None):
        continue
    rel = 0.0
    if(fitted["ratio"] > 0):
        rel = (stored_ratio - fitted["ratio"]) / fitted["ratio"]
    improved = (stored_ratio - fitted["ratio"] > 0.30) and (rel > 0.15) and (abs(fitted["B"]) < 0.94) and (abs(fitted["C"]) < 0.94)
    record = {"q2y": q2y, "zpt": zpt, "stored_ratio": stored_ratio, "free_ratio": fitted["ratio"], "rel": rel, "improved": improved, "B": par_b, "C": par_c, "freeB": fitted["B"], "freeC": fitted["C"]}
    rows.append(record)
    if(improved):
        misses.append(record)
    if(draw_this or improved or (stored_ratio >= 4.5)):
        draw_overlay(histo, q2y, zpt, par_a, par_b, par_c, fitted, stored_ratio)

infile.Close()
ratios.sort()
median = ratios[len(ratios) // 2]
misses.sort(key=lambda item: item["stored_ratio"] - item["free_ratio"], reverse=True)
summary = {"n_ratios": len(ratios), "median_chi2_ndf": median, "n_improved": len(misses), "misses": misses, "boundary": boundary, "high_tail": sorted(rows, key=lambda item: item["stored_ratio"], reverse=True)[:12]}
with open(os.path.join(dest, "review_pass2.json"), "w") as handle:
    json.dump(summary, handle, indent=2)
print("median", median)
print("improved", len(misses))
print("boundary", len(boundary))
for item in misses:
    print("MISS", item["q2y"], item["zpt"], round(item["stored_ratio"], 3), round(item["free_ratio"], 3))
print("TAIL")
for item in summary["high_tail"]:
    print("TAIL", item["q2y"], item["zpt"], round(item["stored_ratio"], 3), round(item["free_ratio"], 3), round(item["rel"], 3), item["improved"])
