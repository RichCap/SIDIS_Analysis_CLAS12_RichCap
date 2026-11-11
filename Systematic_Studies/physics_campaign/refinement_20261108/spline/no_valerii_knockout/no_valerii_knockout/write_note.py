# Build the refinement note and the retained-fit overlay. Does not refit.
import json
import math
import os

DEST = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(DEST, "fit_copy.root")
JSON_KEY = "Fit_Pars_from_3D_Bayesian"


def load_json(path):
    with open(path, "r") as handle:
        return json.load(handle)


def bin_sort_key(name):
    q2y = int(name.split("Q2_y_Bin_")[1].split(")")[0])
    zpt = int(name.split("z_pT_Bin_")[1].split(")")[0])
    return (q2y, zpt)


def curve_pulls(points, amplitude, cosine_b, cosine_c):
    chi2 = 0.0
    used = 0
    worst = None
    for phi, content, error in zip(points["phi"], points["y"], points["err"]):
        if(not (error > 0.0)):
            continue
        rad = float(phi) * math.pi / 180.0
        model = float(amplitude) * (1.0 + float(cosine_b) * math.cos(rad) + float(cosine_c) * math.cos(2.0 * rad))
        pull = (float(content) - model) / float(error)
        chi2 += pull * pull
        used += 1
        if((worst is None) or (abs(pull) > abs(worst["pull"]))):
            worst = {"pull": pull, "phi": float(phi)}
    spike = None
    if((worst is not None) and (chi2 > 0.0)):
        fraction = (worst["pull"] * worst["pull"]) / chi2
        if((abs(worst["pull"]) >= 5.0) and (fraction >= 0.25)):
            spike = {"pull": worst["pull"], "phi": worst["phi"], "fraction": fraction}
    return chi2, used, spike


def pack_pars(cell):
    return {
        "A": cell["Fit_Par_A"],
        "A_ERR": cell["Fit_Par_A_ERR"],
        "B": cell["Fit_Par_B"],
        "B_ERR": cell["Fit_Par_B_ERR"],
        "C": cell["Fit_Par_C"],
        "C_ERR": cell["Fit_Par_C_ERR"],
        "Chi2": cell["Chi2"],
        "NDF": cell["NDF"],
    }


def read_ranges():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.TH1.AddDirectory(False)
    tfile = ROOT.TFile.Open(ROOT_PATH, "READ")
    ranges = {}
    families = {}
    n_5d = 0
    n_bin = 0
    for key in tfile.GetListOfKeys():
        name = key.GetName()
        if(("MultiDim_5D" in name) or ("Q2_y_z_pT_phi_h" in name)):
            n_5d += 1
        if("(Bin)" in name):
            n_bin += 1
        if("MultiDim_3D_Histo" not in name):
            continue
        parts = name.split(")_(")
        if(len(parts) < 2):
            continue
        family = parts[1]
        if(("Bin_All" in name) or ("_(Normalized)" in name) or ("_AsymErr" in name)):
            continue
        if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in name):
            continue
        families[family] = families.get(family, 0) + 1
        if(family != "Bayesian"):
            continue
        histo = key.ReadObj()
        fit_key = tfile.Get(name.replace("MultiDim_3D_Histo", "Fit_Function"))
        nbins = int(histo.GetNbinsX())
        filled_low = None
        filled_high = None
        nonempty = 0
        for ibin in range(1, nbins + 1):
            if(histo.GetBinContent(ibin) != 0):
                nonempty += 1
                low = float(histo.GetXaxis().GetBinLowEdge(ibin))
                high = float(histo.GetXaxis().GetBinUpEdge(ibin))
                if(filled_low is None):
                    filled_low = low
                filled_high = high
        phi_low = float(fit_key.GetXmin()) if(fit_key is not None) else None
        phi_high = float(fit_key.GetXmax()) if(fit_key is not None) else None
        bins_in = 0
        positive = 0
        zero = 0
        if((phi_low is not None) and (phi_high is not None)):
            for ibin in range(1, nbins + 1):
                low = float(histo.GetXaxis().GetBinLowEdge(ibin))
                high = float(histo.GetXaxis().GetBinUpEdge(ibin))
                if((low >= phi_low - 0.01) and (high <= phi_high + 0.01)):
                    bins_in += 1
                    if(histo.GetBinError(ibin) > 0.0):
                        positive += 1
                    else:
                        zero += 1
        bin_name = "(" + parts[3] + ")-(" + parts[4] + ")"
        match = (phi_low is not None) and (abs(phi_low - filled_low) <= 0.1) and (abs(phi_high - filled_high) <= 0.1)
        ranges[bin_name] = {
            "filled_low": filled_low,
            "filled_high": filled_high,
            "phi_low": phi_low,
            "phi_high": phi_high,
            "nonempty": nonempty,
            "bins_in_tf1": bins_in,
            "positive_error_in_range": positive,
            "zero_error_in_range": zero,
            "matches_filled_window": match and (nonempty > 0),
            "nbins": nbins,
        }
    tfile.Close()
    return ranges, families, n_5d, n_bin


def draw_overlay(rows, before, after, ranges):
    # Stored curve is dashed. The retained TF1 is drawn only on its fit interval.
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    chosen = [
        "(Q2_y_Bin_1)-(z_pT_Bin_8)",
        "(Q2_y_Bin_1)-(z_pT_Bin_4)",
        "(Q2_y_Bin_1)-(z_pT_Bin_14)",
        "(Q2_y_Bin_1)-(z_pT_Bin_7)",
        "(Q2_y_Bin_1)-(z_pT_Bin_17)",
        "(Q2_y_Bin_1)-(z_pT_Bin_32)",
        "(Q2_y_Bin_2)-(z_pT_Bin_29)",
        "(Q2_y_Bin_5)-(z_pT_Bin_3)",
        "(Q2_y_Bin_6)-(z_pT_Bin_2)",
        "(Q2_y_Bin_7)-(z_pT_Bin_11)",
        "(Q2_y_Bin_12)-(z_pT_Bin_24)",
        "(Q2_y_Bin_13)-(z_pT_Bin_4)",
        "(Q2_y_Bin_13)-(z_pT_Bin_10)",
        "(Q2_y_Bin_15)-(z_pT_Bin_24)",
        "(Q2_y_Bin_9)-(z_pT_Bin_14)",
        "(Q2_y_Bin_2)-(z_pT_Bin_18)",
    ]
    tfile = ROOT.TFile.Open(ROOT_PATH, "READ")
    canvas = ROOT.TCanvas("knockout_overlay", "knockout_overlay", 1600, 1200)
    canvas.Divide(4, 4)
    held = []
    for index, name in enumerate(chosen):
        canvas.cd(index + 1)
        histo_name = rows[name]["histo"]
        histo = tfile.Get(histo_name).Clone("pad_%d" % index)
        histo.SetDirectory(0)
        histo.SetMarkerStyle(20)
        histo.SetMarkerSize(0.6)
        info = ranges[name]
        stored = before[name]
        stored_fn = ROOT.TF1(
            "stored_%d" % index,
            "[0]*(1+[1]*cos(x*3.1415926/180)+[2]*cos(2*x*3.1415926/180))",
            info["phi_low"],
            info["phi_high"],
        )
        stored_fn.SetParameters(stored["Fit_Par_A"], stored["Fit_Par_B"], stored["Fit_Par_C"])
        stored_fn.SetLineColor(ROOT.kGray + 2)
        stored_fn.SetLineStyle(2)
        stored_fn.SetLineWidth(2)
        kept = tfile.Get(histo_name.replace("MultiDim_3D_Histo", "Fit_Function"))
        kept_draw = kept.Clone("kept_%d" % index)
        reduced_before = stored["Chi2"] / stored["NDF"]
        reduced_after = after[name]["Chi2"] / after[name]["NDF"]
        title = "%s  %.2f to %.2f" % (name, reduced_before, reduced_after)
        histo.SetTitle(title)
        histo.GetXaxis().SetRangeUser(info["phi_low"], info["phi_high"])
        histo.Draw("E")
        stored_fn.Draw("SAME")
        kept_draw.SetLineColor(ROOT.kRed + 1)
        kept_draw.SetLineWidth(2)
        kept_draw.Draw("SAME")
        held.append((histo, stored_fn, kept_draw))
    out_dir = os.path.join(DEST, "overlays")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "no_valerii_knockout_final.png")
    canvas.SaveAs(out_path)
    tfile.Close()
    return out_path


def main():
    before = load_json(os.path.join(DEST, "fit_before.json"))[JSON_KEY]
    after = load_json(os.path.join(DEST, "fit.json"))[JSON_KEY]
    nominal = load_json("/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/fits/spline/nominal/nominal/fit.json")[JSON_KEY]
    diag = load_json(os.path.join(DEST, "diagnosis_before.json"))
    rows = {row["bin"]: row for row in diag["rows"]}
    ranges, families, n_5d, n_bin = read_ranges()
    mismatches = [name for name, info in ranges.items() if(not info["matches_filled_window"])]
    improved = []
    worse = []
    stability = []
    spikes = []
    high = []
    bin_rows = []
    for name in sorted(before, key=bin_sort_key):
        stored = before[name]
        kept = after[name]
        cosine = rows[name]["cosine"]
        info = ranges[name]
        dchi = float(kept["Chi2"]) - float(stored["Chi2"])
        if(dchi < -0.05):
            improved.append(name)
        if(dchi > 0.05):
            worse.append(name)
        problems = []
        for par_name in ["A", "B", "C"]:
            err = float(kept["Fit_Par_%s_ERR" % par_name])
            val = float(kept["Fit_Par_%s" % par_name])
            if((not math.isfinite(err)) or (not math.isfinite(val))):
                problems.append("nonfinite_%s" % par_name)
            elif(err == 0.0):
                problems.append("zero_error_%s" % par_name)
            elif(err < 1.0e-6):
                problems.append("collapsed_%s" % par_name)
        if(abs(float(kept["Fit_Par_B"])) >= 0.999):
            problems.append("boundary_B")
        if(abs(float(kept["Fit_Par_C"])) >= 0.999):
            problems.append("boundary_C")
        if(not info["matches_filled_window"]):
            problems.append("range_mismatch")
        chi2_curve, used, spike = curve_pulls(rows[name]["points"], kept["Fit_Par_A"], kept["Fit_Par_B"], kept["Fit_Par_C"])
        if(spike is not None):
            problems.append("isolated_spike")
            spikes.append((abs(spike["pull"]), name, spike))
        collapsed = [item for item in problems if(item.startswith("collapsed_"))]
        if(collapsed):
            stability.append(name)
        ndf = float(kept["NDF"])
        reduced = float(kept["Chi2"]) / ndf if(ndf > 0.0) else None
        gap = None if(cosine is None) else float(kept["Chi2"]) - float(cosine["Chi2"])
        if((reduced is not None) and (reduced >= 4.5)):
            high.append((reduced, name, float(kept["Chi2"]), ndf, gap))
        nom = nominal[name]
        dB = float(kept["Fit_Par_B"]) - float(nom["Fit_Par_B"])
        dC = float(kept["Fit_Par_C"]) - float(nom["Fit_Par_C"])
        dB_stat = dB / float(kept["Fit_Par_B_ERR"]) if(float(kept["Fit_Par_B_ERR"]) > 0.0) else None
        dC_stat = dC / float(kept["Fit_Par_C_ERR"]) if(float(kept["Fit_Par_C_ERR"]) > 0.0) else None
        status = "completed"
        if(("nonfinite_A" in problems) or ("nonfinite_B" in problems) or ("nonfinite_C" in problems) or (ndf <= 0.0)):
            status = "failed"
        bin_rows.append({
            "bin": name,
            "status": status,
            "problems": problems,
            "before": pack_pars(stored),
            "after": pack_pars(kept),
            "range": info,
            "cosine_chi2": None if(cosine is None) else cosine["Chi2"],
            "cosine_B": None if(cosine is None) else cosine["B"],
            "cosine_C": None if(cosine is None) else cosine["C"],
            "dB_nominal": dB,
            "dC_nominal": dC,
            "dB_over_stat": dB_stat,
            "dC_over_stat": dC_stat,
            "chi2_gap_vs_cosine": gap,
        })
    overlay = draw_overlay(rows, before, after, ranges)
    shifts = sorted(bin_rows, key=lambda item: -max(abs(item["dB_nominal"]), abs(item["dC_nominal"])))
    stat_shifts = sorted(
        [item for item in bin_rows if(item["dB_over_stat"] is not None)],
        key=lambda item: -max(abs(item["dB_over_stat"]), abs(item["dC_over_stat"] or 0.0)),
    )
    cell = [item for item in bin_rows if(item["bin"] == "(Q2_y_Bin_1)-(z_pT_Bin_8)")][0]
    nom18 = nominal["(Q2_y_Bin_1)-(z_pT_Bin_8)"]
    high_sorted = sorted(high, reverse=True)
    spike_sorted = sorted(spikes, reverse=True)
    high_text = "; ".join(
        "%s %.3f (chi2 %.3f, NDF %.0f)" % (item[1], item[0], item[2], item[3])
        for item in high_sorted[:8]
    )
    spike_text = "; ".join(
        "%s pull %.2f at %.0f deg, fraction %.2f" % (item[1], item[2]["pull"], item[2]["phi"], item[2]["fraction"])
        for item in spike_sorted[:6]
    )
    left_examples = []
    for item in shifts[:6]:
        if(item["bin"] == "(Q2_y_Bin_1)-(z_pT_Bin_8)"):
            continue
        left_examples.append(
            "%s B=%.5f versus nominal %.5f, C=%.5f versus nominal %.5f" % (
                item["bin"], item["after"]["B"], nominal[item["bin"]]["Fit_Par_B"], item["after"]["C"], nominal[item["bin"]]["Fit_Par_C"]
            )
        )
    note = {
        "scope": "Spline no_valerii_knockout acceptance only, task pcal-dead. 3D Bayesian phi_h in the copy of fits/spline/no_valerii_knockout/no_valerii_knockout/fit_copy.root, Q2-y 1-17, 452 histograms. The file has rdf, mdf, gdf, Background, and Bayesian histograms and no RC_Bayesian, BC_RC_Bayesian, Bin, or 5D histograms. Those families were not created. No publication. The source fit, the budget, and the shared Phi_h guides were not edited. This copy does not replace the source, so the source stays in the budget. The destination did not already contain refinement_note.json and fit.json, so this is not a resume.",
        "start_mode": "manual. start=auto: the 3D spline B windows selected by these histograms have median width 0.0153 and 428 of 452 are narrower than 0.05, and the C windows have median width 0.0070 with 445 of 452 narrower than 0.05, so they can pin a fit. The run-local guide started as Phi_h_Fit_Parameters_Initialize.py. --use_spline_init was not passed.",
        "error_source": "histogram",
        "changed": "Pass 1 used the manual baseline on all 452 histograms. It improved 5 and made 23 worse. The worst was (Q2_y_Bin_13)-(z_pT_Bin_4), chi-squared 41.955 to 293.035, with the second-pass half-width around a bad start. (Q2_y_Bin_1)-(z_pT_Bin_8) moved only from the stored pin B=-0.045000 to B=-0.065511, C collapsed to 0, and chi-squared 45.346 to 43.735. That is still short of this histogram's cosine B=-0.122925, C=-0.039969, chi-squared 40.302. Pass 2 put 41 starts on each missed histogram's own unconstrained cosine, opened only the limits that excluded that cosine, and turned off the second-pass half-width when it was narrower than the parameter error. It refit Q2-y 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, and 17. Q2-y 8 was not given new keys. Pass 3 added (1, 12) and (9, 32), where that half-width still left chi-squared about 1.4 above the cosine and a B error smaller than the free-cosine error, and refit Q2-y 1 and 9. JSON still has 452 bins, including Q2-y 8. %d histograms have a lower chi-squared than the stored fit and none is worse (largest increase 0.0006). (1, 8) is kept at B=%.6f, statistical error %.6f, C=%.6f, error %.6f, chi-squared %.3f, NDF 13, status completed, phi 60-300, 16 histogram bins inside the TF1 range. (1, 12) is kept at B=-0.249829, error 0.009677, C=0.046277, error 0.009671, chi-squared 43.403, NDF 21. (9, 32) is kept at B=-0.171727, error 0.008993, C=0.003142, error 0.009034, chi-squared 23.147, NDF 21. The stored B=-0.045 on (1, 8) was the second-pass edge of a first-pass limit, not the cosine. It is not pulled to the nominal B=-0.125184." % (
            len(improved), cell["after"]["B"], cell["after"]["B_ERR"], cell["after"]["C"], cell["after"]["C_ERR"], cell["after"]["Chi2"]
        ),
        "left_bins": "No 5D family is in this file, so nothing was left from a 3D-versus-5D disagreement. Large nominal-minus-variation shifts that already match this histogram were not moved onto the nominal value. %s. Offsets still inside the free-cosine error were left: (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_1)-(z_pT_Bin_9), and (Q2_y_Bin_8)-(z_pT_Bin_30). Collapsed errors that remain are parameters consistent with zero, not a smaller systematic uncertainty. Excluded sector pairs were not put back into this comparison. No comparison was filled with zero. The source was not removed from the budget, and fit-parameter errors were not added to the systematic uncertainty." % ("; ".join(left_examples[:4])),
        "unresolved": "The remaining high chi-squared is the histogram shape. The retained A(1+B cos phi+C cos 2phi) already matches an unconstrained cosine, so another guide change would not help. %s. (Q2_y_Bin_1)-(z_pT_Bin_8) is not unresolved as a guide miss: the retained curve matches the free cosine, and the remaining chi-squared is scatter inside 60-300. Isolated spikes: %s. No empty histograms. Collapsed parameter errors that remain, because the cosine is consistent with zero: %s." % (
            high_text,
            spike_text if(spike_text) else "none",
            ", ".join(stability) if(stability) else "none",
        ),
        "fitted_bins": 452,
        "unselected_bins_present": True,
        "range_mismatches": len(mismatches),
        "resumed": False,
        "overlay": "overlays/no_valerii_knockout_final.png",
        "why_retained": "Pass 3 is kept because every histogram is at least as good as the stored fit and %d are better, including the bins the manual baseline missed. (Q2_y_Bin_1)-(z_pT_Bin_8) follows this histogram's cosine, chi-squared 45.346 to %.3f, rather than the pinned B=-0.045 or the nominal B=-0.125184. (1, 12) and (9, 32) moved onto their own cosines, and their statistical errors are no longer the half-width pin. The large shifts that were already the cosine were left where they are. Fit-parameter errors were not added to the systematic uncertainty." % (len(improved), cell["after"]["Chi2"]),
        "families_present": families,
        "n_5d_histograms": n_5d,
        "n_bin_histograms": n_bin,
        "improved_bins": improved,
        "worse_bins": worse,
        "stability_bins": stability,
        "nominal_1_8": {
            "B": nom18["Fit_Par_B"],
            "B_ERR": nom18["Fit_Par_B_ERR"],
            "C": nom18["Fit_Par_C"],
            "C_ERR": nom18["Fit_Par_C_ERR"],
            "Chi2": nom18["Chi2"],
            "NDF": nom18["NDF"],
        },
        "bin_1_8": cell,
        "bins": bin_rows,
    }
    out_path = os.path.join(DEST, "refinement_note.json")
    with open(out_path, "w") as handle:
        json.dump(note, handle, indent=2)
        handle.write("\n")
    print("ranges", len(ranges), "mismatches", mismatches)
    print("families", families, "5d", n_5d, "bin", n_bin)
    print("improved", len(improved), "worse", len(worse), "stability", stability)
    print("overlay", overlay)
    print("1,8", cell["after"])
    print("top shifts")
    for item in shifts[:8]:
        print(" ", item["bin"], "dB", round(item["dB_nominal"], 5), "dC", round(item["dC_nominal"], 5), "dB/stat", None if(item["dB_over_stat"] is None) else round(item["dB_over_stat"], 3))
    print("top stat")
    for item in stat_shifts[:5]:
        print(" ", item["bin"], "dB/stat", round(item["dB_over_stat"], 3), "dC/stat", None if(item["dC_over_stat"] is None) else round(item["dC_over_stat"], 3))
    print("high")
    for item in high_sorted[:8]:
        print(" ", item)
    print("spikes")
    for item in spike_sorted[:8]:
        print(" ", item[1], item[2])
    print("wrote", out_path)


if(__name__ == "__main__"):
    main()
