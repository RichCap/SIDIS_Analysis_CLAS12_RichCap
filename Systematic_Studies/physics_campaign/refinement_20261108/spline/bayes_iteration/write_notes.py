# Record the BayesMinus1 and BayesPlus1 refinement. Does not refit.
import json
import math
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError
ROOT.gStyle.SetOptStat(0)

BASE = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign"
NOMINAL_PATH = os.path.join(BASE, "fits/spline/nominal/nominal/fit.json")
PARENT = os.path.join(BASE, "refinement_20261108/spline/bayes_iteration")


def load_json(path):
    with open(path, "r") as handle:
        return json.load(handle)


def bin_ids(name):
    q2y = int(name.split("Q2_y_Bin_")[1].split(")")[0])
    zpt = int(name.split("z_pT_Bin_")[1].split(")")[0])
    return (q2y, zpt)


def pack(cell):
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


def near(left, right):
    return abs(float(left) - float(right)) <= 1.0e-4


def curve_spike(histo, amplitude, cosine_b, cosine_c, filled_low, filled_high):
    chi2 = 0.0
    worst = None
    for ibin in range(1, histo.GetNbinsX() + 1):
        center = float(histo.GetXaxis().GetBinCenter(ibin))
        if((center < filled_low - 1.0e-6) or (center > filled_high + 1.0e-6)):
            continue
        error = float(histo.GetBinError(ibin))
        if(not (error > 0.0)):
            continue
        rad = center * math.pi / 180.0
        model = float(amplitude) * (1.0 + float(cosine_b) * math.cos(rad) + float(cosine_c) * math.cos(2.0 * rad))
        pull = (float(histo.GetBinContent(ibin)) - model) / error
        chi2 += pull * pull
        if((worst is None) or (abs(pull) > abs(worst[0]))):
            worst = (pull, center)
    if((worst is None) or (not (chi2 > 0.0))):
        return None
    fraction = (worst[0] * worst[0]) / chi2
    if((abs(worst[0]) >= 5.0) and (fraction >= 0.25)):
        return {"pull": worst[0], "phi": worst[1], "fraction": fraction}
    return None


def fmt(value):
    return "%.3f" % float(value)


def fmt_par(value):
    return "%.6f" % float(value)


def write_family(family, show):
    here = os.path.join(PARENT, family)
    source_root = os.path.join(BASE, "fits/spline/bayes_iteration", family, "fit_copy.root")
    before = load_json(os.path.join(here, "fit_before.json"))["Fit_Pars_from_3D_Bayesian"]
    pass1 = load_json(os.path.join(here, "fit_pass1.json"))["Fit_Pars_from_3D_Bayesian"]
    after = load_json(os.path.join(here, "fit.json"))["Fit_Pars_from_3D_Bayesian"]
    diagnosis = load_json(os.path.join(here, "diagnosis_before.json"))
    targets = load_json(os.path.join(here, "pass2_targets.json"))
    nominal = load_json(NOMINAL_PATH)["Fit_Pars_from_3D_Bayesian"]
    by_diag = {}
    histo_for_bin = {}
    for row in diagnosis["rows"]:
        by_diag[row["bin"]] = row
        histo_for_bin[row["bin"]] = row["name"]
    copied = ROOT.TFile.Open(os.path.join(here, "fit_copy.root"), "READ")
    source = ROOT.TFile.Open(source_root, "READ")
    content_changes = []
    bins = []
    mismatches = []
    problems_all = []
    spikes = []
    for bin_name in sorted(after, key=bin_ids):
        histo_name = histo_for_bin[bin_name]
        histo = copied.Get(histo_name)
        source_histo = source.Get(histo_name)
        fit_obj = copied.Get(histo_name.replace("(MultiDim_3D_Histo)", "(Fit_Function)"))
        nbins = int(histo.GetNbinsX())
        changed_bins = 0
        for ibin in range(1, nbins + 1):
            if(abs(float(histo.GetBinContent(ibin)) - float(source_histo.GetBinContent(ibin))) > 1.0e-6):
                changed_bins += 1
            if(abs(float(histo.GetBinError(ibin)) - float(source_histo.GetBinError(ibin))) > 1.0e-6):
                changed_bins += 1
        if(changed_bins > 0):
            content_changes.append(bin_name)
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
                if((center < filled_low - 1.0e-6) or (center > filled_high + 1.0e-6)):
                    continue
                bins_in_tf1 += 1
                if(float(histo.GetBinError(ibin)) > 0.0):
                    positive_error += 1
                else:
                    zero_error += 1
        matches = False
        if((filled_low is not None) and (phi_low is not None)):
            matches = near(filled_low, phi_low) and near(filled_high, phi_high)
        if(not matches):
            mismatches.append(bin_name)
        cell = after[bin_name]
        old = before[bin_name]
        problems = []
        for par in ["A", "B", "C"]:
            value = cell.get("Fit_Par_%s" % par)
            error = cell.get("Fit_Par_%s_ERR" % par)
            if((value is None) or (error is None) or (not math.isfinite(float(value))) or (not math.isfinite(float(error)))):
                problems.append("%s_nonfinite" % par)
            elif(float(error) < 1.0e-8):
                problems.append("%s_collapsed_error" % par)
        if(float(cell["Fit_Par_A"]) <= 0.0):
            problems.append("A_nonpositive")
        if(abs(float(cell["Fit_Par_B"])) >= 1.0):
            problems.append("B_abs_ge_1")
        if(abs(float(cell["Fit_Par_C"])) >= 1.0):
            problems.append("C_abs_ge_1")
        if((not math.isfinite(float(cell["Chi2"]))) or (float(cell["Chi2"]) == 0.0)):
            problems.append("chi2_bad")
        if(not matches):
            problems.append("range_mismatch")
        spike = None
        if(filled_low is not None):
            spike = curve_spike(histo, cell["Fit_Par_A"], cell["Fit_Par_B"], cell["Fit_Par_C"], filled_low, filled_high)
        if(spike is not None):
            spikes.append({"bin": bin_name, "pull": spike["pull"], "phi": spike["phi"], "fraction": spike["fraction"], "Chi2": cell["Chi2"], "NDF": cell["NDF"]})
        record = {
            "bin": bin_name,
            "status": "completed",
            "problems": problems,
            "before": pack(old),
            "after": pack(cell),
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
            problems_all.append({"bin": bin_name, "problems": problems})
    # Overlay uses the open file. Draw before closing.
    os.makedirs(os.path.join(here, "overlays"), exist_ok=True)
    by_bin = {}
    for record in bins:
        by_bin[record["bin"]] = record
    canvas = ROOT.TCanvas("%s_final" % family, family, 1800, 1500)
    canvas.Divide(3, 3)
    keepers = []
    for index, bin_name in enumerate(show):
        canvas.cd(index + 1)
        record = by_bin[bin_name]
        histo_name = histo_for_bin[bin_name]
        histo = copied.Get(histo_name)
        fit_obj = copied.Get(histo_name.replace("(MultiDim_3D_Histo)", "(Fit_Function)"))
        histo.SetMarkerStyle(20)
        histo.SetMarkerSize(0.55)
        histo.SetLineColor(ROOT.kBlack)
        histo.SetTitle("%s  #chi^{2} %.1f #rightarrow %.1f" % (bin_name, record["before"]["Chi2"], record["after"]["Chi2"]))
        histo.Draw("E")
        fit_obj.SetLineColor(ROOT.kRed)
        fit_obj.SetLineWidth(2)
        fit_obj.Draw("SAME")
        old_fn = ROOT.TF1("old_%s_%d" % (family, index), "[0]*(1+[1]*cos(x*3.1415926/180)+[2]*cos(2*x*3.1415926/180))", record["range"]["phi_low"], record["range"]["phi_high"])
        old_fn.SetParameters(record["before"]["A"], record["before"]["B"], record["before"]["C"])
        old_fn.SetLineColor(ROOT.kBlue)
        old_fn.SetLineStyle(2)
        old_fn.SetLineWidth(2)
        old_fn.Draw("SAME")
        keepers.append((histo, fit_obj, old_fn))
    overlay_name = "overlays/%s_final.png" % family.lower()
    canvas.SaveAs(os.path.join(here, overlay_name))
    copied.Close()
    source.Close()

    improved = []
    worse = []
    same = 0
    pass1_better = 0
    pass1_worse = []
    for record in bins:
        dchi = float(record["after"]["Chi2"]) - float(record["before"]["Chi2"])
        if(dchi < -0.05):
            improved.append((dchi, record))
        elif(dchi > 0.05):
            worse.append((dchi, record))
        else:
            same += 1
        p1 = pass1[record["bin"]]
        dpass = float(p1["Chi2"]) - float(record["before"]["Chi2"])
        if(dpass < -0.05):
            pass1_better += 1
        elif(dpass > 0.05):
            pass1_worse.append((dpass, record["bin"], record["before"]["Chi2"], p1["Chi2"], p1["Fit_Par_B"], p1["Fit_Par_C"]))
    improved.sort(key=lambda item: item[0])
    worse.sort(reverse=True)
    pass1_worse.sort(reverse=True)
    shifts = []
    for record in bins:
        nom = nominal.get(record["bin"])
        free = by_diag[record["bin"]]["free"]
        if((nom is None) or (free is None)):
            continue
        db = float(record["after"]["B"]) - float(nom["Fit_Par_B"])
        b_err = float(record["after"]["B_ERR"])
        shifts.append((abs(db), db, record, free, nom, b_err))
    shifts.sort(reverse=True)
    reduced = []
    for record in bins:
        ndf = float(record["after"]["NDF"])
        if(ndf <= 0.0):
            continue
        free = by_diag[record["bin"]]["free"]
        gap = None if(free is None) else (float(record["after"]["Chi2"]) - float(free["Chi2"]))
        reduced.append((float(record["after"]["Chi2"]) / ndf, record, gap))
    reduced.sort(reverse=True)
    stability = []
    for record in bins:
        for problem in record["problems"]:
            if("collapsed" in problem):
                stability.append("%s %s" % (record["bin"], problem))
    q2y = [int(item) for item in targets["q2y"]]
    pass2_count = 0
    for record in bins:
        if(bin_ids(record["bin"])[0] in q2y):
            pass2_count += 1
    one = by_bin["(Q2_y_Bin_1)-(z_pT_Bin_8)"]
    nom18 = nominal["(Q2_y_Bin_1)-(z_pT_Bin_8)"]
    free18 = by_diag["(Q2_y_Bin_1)-(z_pT_Bin_8)"]["free"]
    db_before = float(one["before"]["B"]) - float(nom18["Fit_Par_B"])
    db_after = float(one["after"]["B"]) - float(nom18["Fit_Par_B"])
    drop_bits = []
    for dchi, record in improved[:12]:
        drop_bits.append("%s %s to %s" % (record["bin"], fmt(record["before"]["Chi2"]), fmt(record["after"]["Chi2"])))
    left_bits = []
    for abs_db, db, record, free, nom, b_err in shifts[:8]:
        if(abs(float(record["after"]["B"]) - float(free["B"])) > 0.01):
            continue
        ratio = None if(not b_err) else (db / b_err)
        left_bits.append("%s B %s versus nominal %s (%.2f stat)" % (record["bin"], fmt_par(record["after"]["B"]), fmt_par(nom["Fit_Par_B"]), 0.0 if(ratio is None) else ratio))
    unresolved_bits = []
    for red, record, gap in reduced[:8]:
        unresolved_bits.append("%s %.3f (chi2 %s, NDF %s)" % (record["bin"], red, fmt(record["after"]["Chi2"]), fmt(record["after"]["NDF"])))
    spike_bits = []
    for item in spikes:
        if(float(item["Chi2"]) / float(item["NDF"]) < 4.0):
            continue
        spike_bits.append("%s pull %.1f at %.0f deg (%.0f%% of chi2)" % (item["bin"], item["pull"], item["phi"], 100.0 * item["fraction"]))
    pass1_worst = pass1_worse[0]
    q2y_text = ", ".join(str(item) for item in q2y)
    skipped = [str(item) for item in range(1, 18) if(item not in q2y)]
    skipped_text = "none" if(len(skipped) == 0) else ", ".join(skipped)
    scope = (
        "Spline Bayesian iterations %s, 3D Bayesian only, on a copy of fits/spline/bayes_iteration/%s/fit_copy.root. "
        "Q2-y 1-17, 452 histograms. The file has rdf, mdf, gdf, Background, and Bayesian histograms and no RC_Bayesian, "
        "BC_RC_Bayesian, Bin, or 5D histograms. Those families were not created. No publication. The source ROOT file, "
        "budgets, sector exclusions, histogram weights, and the shared Phi_h guides were not edited. This copy does not "
        "replace the source, so the source stays in the budget. The destination did not already contain refinement_note.json "
        "and fit.json, so this is not a resume."
    ) % (family, family)
    start_mode = (
        "manual. start=auto: the 3D spline B windows selected by these 452 histograms have median width 0.0153 and 428 are "
        "narrower than 0.05, and the C windows have median width 0.0070 with 445 of 452 narrower than 0.05, so they can pin a fit. "
        "The run-local guide started as Phi_h_Fit_Parameters_Initialize.py. --use_spline_init was not passed."
    )
    changed = (
        "Pass 1 refit all 452 histograms with the manual baseline and the corrected filled-window range. It improved %d and made %d worse. "
        "The worst was %s, whose chi-squared rose from %s to %s because the manual window missed this histogram's cosine. "
        "(Q2_y_Bin_1)-(z_pT_Bin_8) moved only from the stored second-pass edge B=%s to B=%s, still short of this histogram's cosine B=%s, C=%s. "
        "Pass 2 put %d starts on each histogram's own unconstrained cosine, opened only the limits that excluded that cosine, and turned off the "
        "second-pass half-width when it was narrower than the parameter error. It refit Q2-y %s (%d histograms). Q2-y not in pass 2: %s. "
        "JSON still has 452 bins. %d histograms have a lower chi-squared than the stored fit and %d are higher. Meaningful drops: %s. "
        "(Q2_y_Bin_1)-(z_pT_Bin_8) went from B=%s, statistical error %s, C=%s, error %s, chi-squared %s, NDF %s, to B=%s, error %s, C=%s, error %s, "
        "chi-squared %s, NDF %s, status completed, phi %.0f-%.0f, %d histogram bins inside the TF1 range and %d with positive error. "
        "The stored B=-0.045 was the second-pass edge of a first-pass limit at -0.03 in the old variation guide, not this histogram's cosine. "
        "Nominal B=%s is close because the histogram cosine is close; the fit was not pulled to the nominal. The nominal-minus-variation B shift "
        "is now %+.6f instead of %+.6f. The pass-1 excursions were not kept. Stored TF1 ranges already matched the filled windows, and the refit "
        "kept that window: %d range mismatches. Empty bins inside a filled window stay in the range. No fit was widened to 0-360 to match a drawing."
    ) % (
        pass1_better,
        len(pass1_worse),
        pass1_worst[1],
        fmt(pass1_worst[2]),
        fmt(pass1_worst[3]),
        fmt_par(one["before"]["B"]),
        fmt_par(pass1[one["bin"]]["Fit_Par_B"]),
        fmt_par(free18["B"]),
        fmt_par(free18["C"]),
        len(targets["targets"]),
        q2y_text,
        pass2_count,
        skipped_text,
        len(improved),
        len(worse),
        "; ".join(drop_bits),
        fmt_par(one["before"]["B"]),
        fmt_par(one["before"]["B_ERR"]),
        fmt_par(one["before"]["C"]),
        fmt_par(one["before"]["C_ERR"]),
        fmt(one["before"]["Chi2"]),
        fmt(one["before"]["NDF"]),
        fmt_par(one["after"]["B"]),
        fmt_par(one["after"]["B_ERR"]),
        fmt_par(one["after"]["C"]),
        fmt_par(one["after"]["C_ERR"]),
        fmt(one["after"]["Chi2"]),
        fmt(one["after"]["NDF"]),
        one["range"]["phi_low"],
        one["range"]["phi_high"],
        one["range"]["bins_in_tf1"],
        one["range"]["positive_error_in_range"],
        fmt_par(nom18["Fit_Par_B"]),
        db_after,
        db_before,
        len(mismatches),
    )
    left = (
        "No 5D family is in this file, so nothing was left from a 3D-versus-5D disagreement. Large nominal-minus-variation shifts that already "
        "match this histogram were not moved onto the nominal: %s. Excluded sector pairs were not put back into this comparison. No comparison was "
        "filled with zero. The source was not removed from the budget, and fit-parameter errors were not added to the systematic uncertainty."
    ) % ("; ".join(left_bits) if(len(left_bits) > 0) else "none above the recorded threshold")
    unresolved = (
        "The remaining high chi-squared is the histogram shape. The retained A(1+B cos phi+C cos 2phi) already matches an unconstrained cosine, "
        "so another guide change would not help. %s. (Q2_y_Bin_1)-(z_pT_Bin_8) is not unresolved as a guide miss: the retained curve matches the free cosine, "
        "and the remaining chi-squared is scatter inside 60-300. Isolated spikes, where one phi bin is at least 5 pulls and at least a quarter of the chi-squared: %s. "
        "Collapsed errors that remain are the stored second-pass edge around a near-zero moment, not a new shrink: %s. No empty histograms."
    ) % (
        "; ".join(unresolved_bits),
        "; ".join(spike_bits) if(len(spike_bits) > 0) else "none in the high-chi-squared bins",
        "; ".join(stability) if(len(stability) > 0) else "none",
    )
    why = (
        "Pass 2 is kept because %d histograms are better than the stored fit and %d are worse, including the bins the manual baseline missed or made worse. "
        "(Q2_y_Bin_1)-(z_pT_Bin_8) follows this histogram's cosine, chi-squared %s to %s, rather than the pinned B=-0.045 or a forced match to nominal B=%s. "
        "The large shifts that were already the cosine were left where they are. Fit-parameter errors were not added to the systematic uncertainty."
    ) % (len(improved), len(worse), fmt(one["before"]["Chi2"]), fmt(one["after"]["Chi2"]), fmt_par(nom18["Fit_Par_B"]))
    note = {
        "task": "bayes-iterations",
        "family": family,
        "scope": scope,
        "start_mode": start_mode,
        "error_source": "histogram",
        "changed": changed,
        "left_bins": left,
        "unresolved": unresolved,
        "why_retained": why,
        "fitted_bins": len(bins),
        "unselected_bins_present": len(after) == len(before),
        "range_mismatches": len(mismatches),
        "range_mismatch_bins": mismatches,
        "pass1_histograms": 452,
        "pass1_better": pass1_better,
        "pass1_worse": len(pass1_worse),
        "pass2_histograms": pass2_count,
        "pass2_q2y": q2y,
        "pass2_targets": len(targets["targets"]),
        "improved_bin_count": len(improved),
        "worse_bin_count": len(worse),
        "same_bin_count": same,
        "overlay": overlay_name,
        "stability_problems": stability,
        "spikes": spikes,
        "histogram_contents_unchanged": len(content_changes) == 0,
        "content_changes": content_changes,
        "families_seen": diagnosis["summary"]["family_counts"],
        "resumed": False,
        "bins": bins,
    }
    with open(os.path.join(here, "bin_record.json"), "w") as handle:
        json.dump({"bins": bins, "mismatches": mismatches, "problems": problems_all, "n_improved": len(improved)}, handle)
    with open(os.path.join(here, "refinement_note.json"), "w") as handle:
        json.dump(note, handle, indent=2)
        handle.write("\n")
    print(family, "bins", len(bins), "mismatches", len(mismatches), "content_changes", len(content_changes))
    print("  improved", len(improved), "worse", len(worse), "same", same, "pass2", pass2_count, "q2y", q2y)
    print("  stability", stability)
    print("  spikes", spike_bits)
    print("  left", left_bits)
    print("  overlay", os.path.join(here, overlay_name))
    print("  bin18", one["after"]["B"], one["after"]["Chi2"], "db", db_after)


if(__name__ == "__main__"):
    requested = sys.argv[1:]
    if(len(requested) == 0):
        requested = ["BayesMinus1", "BayesPlus1"]
    shows = {
        "BayesMinus1": [
            "(Q2_y_Bin_1)-(z_pT_Bin_8)",
            "(Q2_y_Bin_13)-(z_pT_Bin_10)",
            "(Q2_y_Bin_7)-(z_pT_Bin_11)",
            "(Q2_y_Bin_3)-(z_pT_Bin_7)",
            "(Q2_y_Bin_1)-(z_pT_Bin_17)",
            "(Q2_y_Bin_6)-(z_pT_Bin_2)",
            "(Q2_y_Bin_1)-(z_pT_Bin_4)",
            "(Q2_y_Bin_1)-(z_pT_Bin_14)",
            "(Q2_y_Bin_1)-(z_pT_Bin_7)",
        ],
        "BayesPlus1": [
            "(Q2_y_Bin_1)-(z_pT_Bin_8)",
            "(Q2_y_Bin_10)-(z_pT_Bin_8)",
            "(Q2_y_Bin_16)-(z_pT_Bin_12)",
            "(Q2_y_Bin_7)-(z_pT_Bin_10)",
            "(Q2_y_Bin_2)-(z_pT_Bin_29)",
            "(Q2_y_Bin_1)-(z_pT_Bin_17)",
            "(Q2_y_Bin_5)-(z_pT_Bin_31)",
            "(Q2_y_Bin_13)-(z_pT_Bin_10)",
            "(Q2_y_Bin_1)-(z_pT_Bin_32)",
        ],
    }
    for family in requested:
        write_family(family, shows[family])
