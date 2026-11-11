# Record ranges, stability, and an overlay. Does not refit.
import json
import math
import os

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError
ROOT.gStyle.SetOptStat(0)

here = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(here, "fit_copy.root")
with open(os.path.join(here, "fit_before.json"), "r") as handle:
    before = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "fit.json"), "r") as handle:
    after = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "diagnosis_before.json"), "r") as handle:
    diagnosis = json.load(handle)
nominal_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/fits/spline/nominal/nominal/fit.json"
with open(nominal_path, "r") as handle:
    nominal = json.load(handle)["Fit_Pars_from_3D_Bayesian"]

by_name = {}
for row in diagnosis["rows"]:
    by_name[row["name"]] = row

infile = ROOT.TFile.Open(root_path, "READ")
names = {}
for key in infile.GetListOfKeys():
    names[str(key.GetName())] = str(key.GetClassName())

bins = []
mismatches = []
problems_all = []
shifts = []
reduced = []
for name in sorted(names):
    if("(MultiDim_3D_Histo)_(Bayesian)_" not in name):
        continue
    if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in name):
        continue
    if("Bin_All" in name) or ("_(Normalized)" in name) or ("_AsymErr" in name):
        continue
    histo = infile.Get(name)
    parts = name.split(")_(")
    q2y = parts[3].replace("Q2_y_Bin_", "")
    zpt = parts[4].replace("z_pT_Bin_", "")
    bin_name = "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt)
    fit_obj = infile.Get(name.replace("(MultiDim_3D_Histo)", "(Fit_Function)"))
    nbins = int(histo.GetNbinsX())
    first = None
    last = None
    nonempty = 0
    for ibin in range(1, nbins + 1):
        if(histo.GetBinContent(ibin) != 0.0):
            nonempty += 1
            if(first is None):
                first = ibin
            last = ibin
    filled_low = float(histo.GetXaxis().GetBinLowEdge(first)) if(first is not None) else None
    filled_high = float(histo.GetXaxis().GetBinUpEdge(last)) if(last is not None) else None
    phi_low = float(fit_obj.GetXmin()) if(fit_obj) else None
    phi_high = float(fit_obj.GetXmax()) if(fit_obj) else None
    bins_in_tf1 = 0
    positive_error = 0
    zero_error = 0
    if(first is not None):
        for ibin in range(1, nbins + 1):
            center = float(histo.GetXaxis().GetBinCenter(ibin))
            if(center < filled_low - 1.0e-6) or (center > filled_high + 1.0e-6):
                continue
            bins_in_tf1 += 1
            if(float(histo.GetBinError(ibin)) > 0.0):
                positive_error += 1
            else:
                zero_error += 1
    matches = False
    if(filled_low is not None) and (phi_low is not None):
        matches = (abs(filled_low - phi_low) <= 1.0e-4) and (abs(filled_high - phi_high) <= 1.0e-4)
    if(not matches):
        mismatches.append(bin_name)
    cell = after[bin_name]
    old = before[bin_name]
    nom = nominal.get(bin_name, {})
    problems = []
    for par in ["A", "B", "C"]:
        value = cell.get("Fit_Par_%s" % par)
        error = cell.get("Fit_Par_%s_ERR" % par)
        if(value is None) or (error is None) or (not math.isfinite(float(value))) or (not math.isfinite(float(error))):
            problems.append("%s_nonfinite" % par)
        elif(float(error) == 0.0) or (float(error) < 1.0e-8):
            problems.append("%s_collapsed_error" % par)
    if(float(cell["Fit_Par_A"]) <= 0.0):
        problems.append("A_nonpositive")
    if(abs(float(cell["Fit_Par_B"])) >= 1.0):
        problems.append("B_abs_ge_1")
    if(abs(float(cell["Fit_Par_C"])) >= 1.0):
        problems.append("C_abs_ge_1")
    if(not math.isfinite(float(cell["Chi2"]))) or (float(cell["Chi2"]) == 0.0):
        problems.append("chi2_bad")
    if(not matches):
        problems.append("range_mismatch")
    status = "completed" if(len(problems) == 0) else "completed"
    record = {
        "bin": bin_name,
        "status": status,
        "problems": problems,
        "before": {
            "A": old["Fit_Par_A"],
            "A_ERR": old["Fit_Par_A_ERR"],
            "B": old["Fit_Par_B"],
            "B_ERR": old["Fit_Par_B_ERR"],
            "C": old["Fit_Par_C"],
            "C_ERR": old["Fit_Par_C_ERR"],
            "Chi2": old["Chi2"],
            "NDF": old["NDF"],
        },
        "after": {
            "A": cell["Fit_Par_A"],
            "A_ERR": cell["Fit_Par_A_ERR"],
            "B": cell["Fit_Par_B"],
            "B_ERR": cell["Fit_Par_B_ERR"],
            "C": cell["Fit_Par_C"],
            "C_ERR": cell["Fit_Par_C_ERR"],
            "Chi2": cell["Chi2"],
            "NDF": cell["NDF"],
        },
        "range": {
            "filled_low": filled_low,
            "filled_high": filled_high,
            "phi_low": phi_low,
            "phi_high": phi_high,
            "nonempty": nonempty,
            "bins_in_tf1": bins_in_tf1,
            "positive_error_in_range": positive_error,
            "zero_error_in_range": zero_error,
            "matches_filled_window": matches,
            "nbins": nbins,
        },
    }
    bins.append(record)
    if(len(problems) > 0):
        problems_all.append({"bin": bin_name, "problems": problems, "after": record["after"]})
    if(nom):
        db = float(cell["Fit_Par_B"]) - float(nom["Fit_Par_B"])
        dc = float(cell["Fit_Par_C"]) - float(nom["Fit_Par_C"])
        b_err = float(cell["Fit_Par_B_ERR"])
        shifts.append((abs(db), bin_name, db, dc, b_err, cell, nom, old))
    ndf = float(cell["NDF"])
    if(ndf > 0.0):
        reduced.append((float(cell["Chi2"]) / ndf, bin_name, cell, old))

infile.Close()
shifts.sort(reverse=True)
reduced.sort(reverse=True)
improved = []
for record in bins:
    dchi = float(record["after"]["Chi2"]) - float(record["before"]["Chi2"])
    if(dchi < -0.05):
        improved.append((dchi, record["bin"], record["before"]["Chi2"], record["after"]["Chi2"], record["before"]["B"], record["after"]["B"]))
improved.sort()
print("bins", len(bins), "mismatches", len(mismatches), "problem_bins", len(problems_all))
print("improved", len(improved))
for item in improved:
    print("  improved", item[1], round(item[2], 3), "to", round(item[3], 3), "B", round(item[4], 5), "to", round(item[5], 5))
print("problems")
for item in problems_all:
    print(" ", item["bin"], item["problems"], "B", item["after"]["B"], "Berr", item["after"]["B_ERR"], "C", item["after"]["C"], "Cerr", item["after"]["C_ERR"])
print("top shifts vs nominal")
for item in shifts[:12]:
    print(" ", item[1], "dB", round(item[2], 5), "dB/stat", round(item[2] / item[4], 3) if(item[4]) else None, "dC", round(item[3], 5), "B", round(item[5]["Fit_Par_B"], 5), "nomB", round(item[6]["Fit_Par_B"], 5), "oldB", round(item[7]["Fit_Par_B"], 5))
print("top reduced")
for item in reduced[:12]:
    print(" ", round(item[0], 3), item[1], "chi2", round(item[2]["Chi2"], 3), "ndf", item[2]["NDF"], "old", round(item[3]["Chi2"], 3))

with open(os.path.join(here, "bin_record.json"), "w") as handle:
    json.dump({
        "bins": bins,
        "mismatches": mismatches,
        "problems": problems_all,
        "n_improved": len(improved),
    }, handle)

# Overlay of the bins that decided the pass. Stored curve is drawn from fit_before, not refit.
show = [
    "(Q2_y_Bin_1)-(z_pT_Bin_8)",
    "(Q2_y_Bin_13)-(z_pT_Bin_4)",
    "(Q2_y_Bin_13)-(z_pT_Bin_10)",
    "(Q2_y_Bin_1)-(z_pT_Bin_4)",
    "(Q2_y_Bin_1)-(z_pT_Bin_17)",
    "(Q2_y_Bin_7)-(z_pT_Bin_11)",
    "(Q2_y_Bin_15)-(z_pT_Bin_24)",
    "(Q2_y_Bin_1)-(z_pT_Bin_32)",
    "(Q2_y_Bin_3)-(z_pT_Bin_29)",
]
by_bin = {}
for record in bins:
    by_bin[record["bin"]] = record
infile = ROOT.TFile.Open(root_path, "READ")
canvas = ROOT.TCanvas("nosmear_final", "nosmear_final", 1800, 1500)
canvas.Divide(3, 3)
keepers = []
for index, bin_name in enumerate(show):
    canvas.cd(index + 1)
    record = by_bin[bin_name]
    histo_name = None
    for row in diagnosis["rows"]:
        if(row["bin"] == bin_name):
            histo_name = row["name"]
            break
    histo = infile.Get(histo_name)
    fit_obj = infile.Get(histo_name.replace("(MultiDim_3D_Histo)", "(Fit_Function)"))
    histo.SetMarkerStyle(20)
    histo.SetMarkerSize(0.55)
    histo.SetLineColor(ROOT.kBlack)
    histo.SetTitle("%s  #chi^{2} %.1f #rightarrow %.1f" % (bin_name, record["before"]["Chi2"], record["after"]["Chi2"]))
    histo.Draw("E")
    fit_obj.SetLineColor(ROOT.kRed)
    fit_obj.SetLineWidth(2)
    fit_obj.Draw("SAME")
    old_fn = ROOT.TF1("old_%d" % index, "[0]*(1+[1]*cos(x*3.1415926/180)+[2]*cos(2*x*3.1415926/180))", record["range"]["phi_low"], record["range"]["phi_high"])
    old_fn.SetParameters(record["before"]["A"], record["before"]["B"], record["before"]["C"])
    old_fn.SetLineColor(ROOT.kBlue)
    old_fn.SetLineStyle(2)
    old_fn.SetLineWidth(2)
    old_fn.Draw("SAME")
    keepers.append((histo, fit_obj, old_fn))
canvas.SaveAs(os.path.join(here, "overlays", "nosmear_final.png"))
infile.Close()
print("overlay", os.path.join(here, "overlays", "nosmear_final.png"))
