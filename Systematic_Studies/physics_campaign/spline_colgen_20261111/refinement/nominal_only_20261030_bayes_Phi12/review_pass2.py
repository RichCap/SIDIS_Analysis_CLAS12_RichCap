import json
import os
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

dest = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/spline_colgen_20261111/refinement/nominal_only_20261030_bayes_Phi12"
overlay_dir = os.path.join(dest, "overlays_pass2")
os.makedirs(overlay_dir, exist_ok=True)
with open(os.path.join(dest, "fit_pass1.json")) as handle:
    pass1 = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(dest, "fit_pass2.json")) as handle:
    pass2 = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
keep = [("9","14"),("1","14"),("10","18"),("15","15"),("3","29"),("5","31"),("9","1"),("9","7"),("16","12"),("11","20"),("12","24"),("15","24"),("15","6")]
root_path = os.path.join(dest, "histograms.root")
infile = ROOT.TFile.Open(root_path, "READ")
if((not infile) or infile.IsZombie()):
    raise SystemExit("open failed")
formula = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
rows = []
for q2y, zpt in keep:
    key = "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt)
    name = "(MultiDim_3D_Histo)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (q2y, zpt)
    histo = infile.Get(name)
    old = pass1[key]
    new = pass2[key]
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
    canvas = ROOT.TCanvas("c_%s_%s" % (q2y, zpt), "c", 700, 500)
    histo.SetTitle("pass2 Q2y %s zpt %s" % (q2y, zpt))
    histo.SetStats(0)
    histo.Draw("E")
    old_func = ROOT.TF1("old_%s_%s" % (q2y, zpt), formula, lo, hi)
    old_func.SetParameters(old["Fit_Par_A"], old["Fit_Par_B"], old["Fit_Par_C"])
    old_func.SetLineColor(ROOT.kRed)
    old_func.SetLineWidth(2)
    old_func.Draw("SAME")
    new_func = ROOT.TF1("new_%s_%s" % (q2y, zpt), formula, lo, hi)
    new_func.SetParameters(new["Fit_Par_A"], new["Fit_Par_B"], new["Fit_Par_C"])
    new_func.SetLineColor(ROOT.kBlue)
    new_func.SetLineWidth(2)
    new_func.Draw("SAME")
    canvas.SaveAs(os.path.join(overlay_dir, "Q2_y_Bin_%s_z_pT_Bin_%s.png" % (q2y, zpt)))
    canvas.Close()
    rows.append({
        "q2y": q2y,
        "zpt": zpt,
        "pass1_ratio": old["Chi2"] / float(old["NDF"]),
        "pass2_ratio": new["Chi2"] / float(new["NDF"]),
        "B": new["Fit_Par_B"],
        "C": new["Fit_Par_C"],
    })
infile.Close()
ratios = []
for key, cell in pass2.items():
    ratios.append(cell["Chi2"] / float(cell["NDF"]))
ratios.sort()
summary = {
    "n_cells": len(pass2),
    "median_chi2_ndf": ratios[len(ratios) // 2],
    "kept": rows,
}
with open(os.path.join(dest, "review_pass2.json"), "w") as handle:
    json.dump(summary, handle, indent=2)
print("median", summary["median_chi2_ndf"])
print("n", summary["n_cells"])
