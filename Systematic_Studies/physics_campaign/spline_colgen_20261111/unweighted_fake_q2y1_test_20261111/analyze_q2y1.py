#!/usr/bin/env python3
import json
import math
import re
from array import array
from pathlib import Path

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

HERE = Path(__file__).resolve().parent
PLOTS = HERE / "plots"
FITS = HERE / "fits"
PLOTS.mkdir(exist_ok=True)
FITS.mkdir(exist_ok=True)

FILES = {
    "cpp_off": HERE / "cpp_bin_off_WSpline.root",
    "python_off": HERE / "python_bin_off_WSpline.root",
    "cpp_corrected": HERE / "cpp_bin_corrected_WSpline_ColGenRatio.root",
    "python_legacy_corrected": HERE / "python_bin_corrected_WSpline_DivUnw.root",
    "old_faulty_bin": Path("/private/tmp/old_faulty_bin.root"),
    "old_bayes": Path("/private/tmp/old_nominal_bayes.root"),
    "completed_nominal_bayes": Path("/Users/richardcapobianco/Documents/Codex/2026-11-11/execute-one-complete-local-3d-unfolding/outputs/q2y1_column_corrected_preserved_spline_mask_WSpline_ColGenRatio.root"),
    "new_bayes": HERE / "cpp_bayes_unweighted_fake_WSpline_ColGenRatio.root",
    "fixed_old_mask_bayes": HERE / "cpp_bayes_unweighted_fake_fixed_old_mask_WSpline_ColGenRatio.root",
}

ZPT_BINS = list(range(1, 21)) + list(range(22, 27)) + list(range(29, 33))


def open_files():
    result = {}
    for label, path in FILES.items():
        handle = ROOT.TFile.Open(str(path))
        if not handle or handle.IsZombie():
            raise RuntimeError(f"cannot open {label}: {path}")
        result[label] = handle
    return result


def dense_name(method):
    smear = "''" if method in ["rdf", "gdf"] else "Smear"
    return f"(1D)_({method})_(SMEAR={smear})_(Q2_y_Bin_1)_(z_pT_Bin_All)_(MultiDim_z_pT_Bin_Y_bin_phi_t)"


def slice_name(method, zpt):
    return f"(MultiDim_3D_Histo)_({method})_(SMEAR=Smear)_(Q2_y_Bin_1)_(z_pT_Bin_{zpt})_(MultiDim_z_pT_Bin_Y_bin_phi_t)"


def get_hist(handle, name):
    hist = handle.Get(name)
    if not hist:
        raise RuntimeError(f"missing histogram: {name} in {handle.GetName()}")
    return hist


def rel_delta(left, right):
    scale = max(abs(left), abs(right))
    return abs(left - right) / scale if scale else 0.0


def percentile(values, fraction):
    values = sorted(values)
    if not values:
        return 0.0
    position = fraction * (len(values) - 1)
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return values[low]
    return values[low] * (high - position) + values[high] * (position - low)


def compare_hist(left, right, include_flow=False):
    if left.GetNbinsX() != right.GetNbinsX():
        raise RuntimeError("histogram bin-count mismatch")
    first = 0 if include_flow else 1
    last = left.GetNbinsX() + 1 if include_flow else left.GetNbinsX()
    content_abs = []
    content_rel = []
    error_abs = []
    error_rel = []
    content_mismatch = 0
    error_mismatch = 0
    for index in range(first, last + 1):
        lc, rc = left.GetBinContent(index), right.GetBinContent(index)
        le, re_ = left.GetBinError(index), right.GetBinError(index)
        content_abs.append(abs(lc - rc))
        content_rel.append(rel_delta(lc, rc))
        error_abs.append(abs(le - re_))
        error_rel.append(rel_delta(le, re_))
        content_mismatch += lc != rc
        error_mismatch += le != re_
    return {
        "bins": last - first + 1,
        "content_mismatches_exact": content_mismatch,
        "error_mismatches_exact": error_mismatch,
        "content_max_abs": max(content_abs, default=0.0),
        "content_max_rel": max(content_rel, default=0.0),
        "content_median_rel": percentile(content_rel, 0.5),
        "content_rms_rel": math.sqrt(sum(value * value for value in content_rel) / len(content_rel)) if content_rel else 0.0,
        "error_max_abs": max(error_abs, default=0.0),
        "error_max_rel": max(error_rel, default=0.0),
        "error_median_rel": percentile(error_rel, 0.5),
        "error_rms_rel": math.sqrt(sum(value * value for value in error_rel) / len(error_rel)) if error_rel else 0.0,
    }


def compare_hist_selected(left, right, excluded):
    excluded = set(excluded)
    content_rel = []
    error_rel = []
    for index in range(1, left.GetNbinsX() + 1):
        if index in excluded:
            continue
        content_rel.append(rel_delta(left.GetBinContent(index), right.GetBinContent(index)))
        error_rel.append(rel_delta(left.GetBinError(index), right.GetBinError(index)))
    return {
        "bins": len(content_rel),
        "content_max_rel": max(content_rel, default=0.0),
        "content_median_rel": percentile(content_rel, 0.5),
        "content_rms_rel": math.sqrt(sum(value * value for value in content_rel) / len(content_rel)) if content_rel else 0.0,
        "error_max_rel": max(error_rel, default=0.0),
        "error_median_rel": percentile(error_rel, 0.5),
        "error_rms_rel": math.sqrt(sum(value * value for value in error_rel) / len(error_rel)) if error_rel else 0.0,
    }


def compare_slices(left_file, right_file, left_method, right_method):
    aggregate = {"bins": 0, "content_mismatches_exact": 0, "error_mismatches_exact": 0,
                 "content_max_abs": 0.0, "content_max_rel": 0.0,
                 "error_max_abs": 0.0, "error_max_rel": 0.0}
    per_slice = {}
    for zpt in ZPT_BINS:
        metrics = compare_hist(get_hist(left_file, slice_name(left_method, zpt)),
                               get_hist(right_file, slice_name(right_method, zpt)))
        per_slice[str(zpt)] = metrics
        aggregate["bins"] += metrics["bins"]
        for key in ["content_mismatches_exact", "error_mismatches_exact"]:
            aggregate[key] += metrics[key]
        for key in ["content_max_abs", "content_max_rel", "error_max_abs", "error_max_rel"]:
            aggregate[key] = max(aggregate[key], metrics[key])
    aggregate["slices"] = len(ZPT_BINS)
    aggregate["per_slice"] = per_slice
    return aggregate


def parse_mask(log_path):
    text = Path(log_path).read_text(errors="replace")
    matches = re.findall(r"skipped original indices:\s*([0-9,]+)", text)
    if not matches:
        raise RuntimeError(f"mask not found in {log_path}")
    return [int(value) for value in matches[-1].split(",")]


def aligned_generated(reconstructed, generated):
    aligned = reconstructed.Clone("python_reference_aligned_generated")
    aligned.Reset("ICES")
    aligned.Sumw2()
    for rec_bin in range(1, reconstructed.GetNbinsX() + 1):
        low = reconstructed.GetXaxis().GetBinLowEdge(rec_bin)
        high = reconstructed.GetXaxis().GetBinUpEdge(rec_bin)
        matches = []
        for gen_bin in range(1, generated.GetNbinsX() + 1):
            if abs(generated.GetXaxis().GetBinLowEdge(gen_bin) - low) <= 1e-6 and abs(generated.GetXaxis().GetBinUpEdge(gen_bin) - high) <= 1e-6:
                matches.append(gen_bin)
        if len(matches) != 1:
            raise RuntimeError(f"generated-edge match count {len(matches)} for reconstructed bin {rec_bin}")
        aligned.SetBinContent(rec_bin, generated.GetBinContent(matches[0]))
        aligned.SetBinError(rec_bin, generated.GetBinError(matches[0]))
    return aligned


def corrected_python_reference(source_file, skipped):
    data = get_hist(source_file, dense_name("rdf"))
    reconstructed = get_hist(source_file, dense_name("mdf"))
    generated = get_hist(source_file, dense_name("gdf"))
    background = get_hist(source_file, dense_name("Background"))
    aligned = aligned_generated(reconstructed, generated)
    acceptance = reconstructed.Clone("python_reference_acceptance")
    acceptance.SetDirectory(0)
    acceptance.Add(background)
    acceptance.Sumw2()
    acceptance.Divide(aligned)
    unfolded = data.Clone("python_reference_corrected_binbybin")
    unfolded.SetDirectory(0)
    unfolded.Divide(acceptance)
    for index in skipped:
        unfolded.SetBinContent(index, 0.0)
        unfolded.SetBinError(index, 0.0)
    return unfolded


def reference_slices(dense):
    output = {}
    for rank, zpt in enumerate(ZPT_BINS):
        hist = ROOT.TH1D(f"python_reference_slice_{zpt}", "", 24, 0.0, 360.0)
        hist.Sumw2()
        first_dense_bin = 3 + 24 * rank
        for phi_bin in range(1, 25):
            dense_bin = first_dense_bin + phi_bin - 1
            hist.SetBinContent(phi_bin, dense.GetBinContent(dense_bin))
            hist.SetBinError(phi_bin, dense.GetBinError(dense_bin))
        output[zpt] = hist
    return output


def fit_slice(hist, tag):
    function = ROOT.TF1(f"fit_{tag}", "[0]*(1+[1]*cos(x*TMath::Pi()/180.)+[2]*cos(2*x*TMath::Pi()/180.))", 0.0, 360.0)
    mean = hist.Integral() / max(hist.GetNbinsX(), 1)
    function.SetParameters(mean if mean > 0 else 1.0, 0.0, 0.0)
    result = hist.Fit(function, "QSN")
    return {
        "status": int(result),
        "A": function.GetParameter(0), "A_error": function.GetParError(0),
        "B": function.GetParameter(1), "B_error": function.GetParError(1),
        "C": function.GetParameter(2), "C_error": function.GetParError(2),
        "chi2": function.GetChisquare(), "ndf": function.GetNDF(),
    }


def fits_for_file(handle, method, label):
    return {str(zpt): fit_slice(get_hist(handle, slice_name(method, zpt)), f"{label}_{zpt}") for zpt in ZPT_BINS}


def fit_shift(left, right):
    output = {}
    for parameter in ["A", "B", "C"]:
        absolute = [abs(left[key][parameter] - right[key][parameter]) for key in left]
        relative = [rel_delta(left[key][parameter], right[key][parameter]) for key in left]
        output[parameter] = {
            "median_abs": percentile(absolute, 0.5), "max_abs": max(absolute, default=0.0),
            "median_rel": percentile(relative, 0.5), "max_rel": max(relative, default=0.0),
        }
    return output


def vector_graph(values, title, ytitle, color=ROOT.kBlue + 1):
    x = array("d", [float(index + 1) for index in range(len(values))])
    y = array("d", [float(value) for value in values])
    graph = ROOT.TGraph(len(values), x, y)
    graph.SetTitle(f"{title};dense reconstructed-bin index;{ytitle}")
    graph.SetLineColor(color)
    graph.SetMarkerColor(color)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.35)
    return graph


def relative_vector(left, right, errors=False):
    values = []
    for index in range(1, left.GetNbinsX() + 1):
        lv = left.GetBinError(index) if errors else left.GetBinContent(index)
        rv = right.GetBinError(index) if errors else right.GetBinContent(index)
        scale = max(abs(lv), abs(rv))
        values.append((lv - rv) / scale if scale else 0.0)
    return values


def save_plot(path, panels):
    canvas = ROOT.TCanvas(path.stem, path.stem, 1300, 400 * len(panels))
    canvas.Divide(1, len(panels))
    keep = []
    for index, (values, title, ytitle, color) in enumerate(panels, 1):
        canvas.cd(index)
        ROOT.gPad.SetGridy(True)
        graph = vector_graph(values, title, ytitle, color)
        graph.Draw("ALP")
        keep.append(graph)
    canvas.SaveAs(str(path))
    canvas.SaveAs(str(path.with_suffix(".png")))
    return keep


def main():
    files = open_files()
    old_mask = parse_mask(HERE.parent / "validation_24bin" / "nominal_q2y1.log")
    new_mask = parse_mask(HERE / "logs" / "cpp_bayes_unweighted_fake.log")
    fixed_mask = parse_mask(HERE / "logs" / "cpp_bayes_unweighted_fake_fixed_old_mask.log")

    cpp_off = get_hist(files["cpp_off"], dense_name("Bin"))
    python_off = get_hist(files["python_off"], dense_name("Bin"))
    cpp_corrected = get_hist(files["cpp_corrected"], dense_name("Bin"))
    python_legacy = get_hist(files["python_legacy_corrected"], dense_name("Bin"))
    reference = corrected_python_reference(files["cpp_corrected"], new_mask)

    corrected_reference_slices = reference_slices(reference)

    reference_file = ROOT.TFile.Open(str(HERE / "python_reference_corrected_binbybin.root"), "RECREATE")
    reference.Write("python_reference_corrected_binbybin")
    for zpt, hist in corrected_reference_slices.items():
        hist.Write(f"python_reference_corrected_binbybin_zpt{zpt}")
    reference_file.Close()

    old_bin = get_hist(files["old_faulty_bin"], dense_name("Bin"))
    completed_bayes = get_hist(files["completed_nominal_bayes"], dense_name("Bayesian"))
    old_bayes = get_hist(files["old_bayes"], dense_name("Bayesian"))
    new_bayes = get_hist(files["new_bayes"], dense_name("Bayesian"))
    fixed_bayes = get_hist(files["fixed_old_mask_bayes"], dense_name("Bayesian"))

    fit_sets = {
        "old_faulty_bin": fits_for_file(files["old_faulty_bin"], "Bin", "old_bin"),
        "repaired_bin": fits_for_file(files["cpp_corrected"], "Bin", "new_bin"),
        "completed_nominal_bayes": fits_for_file(files["completed_nominal_bayes"], "Bayesian", "completed_bayes"),
        "old_bayes": fits_for_file(files["old_bayes"], "Bayesian", "old_bayes"),
        "new_bayes": fits_for_file(files["new_bayes"], "Bayesian", "new_bayes"),
        "fixed_old_mask_bayes": fits_for_file(files["fixed_old_mask_bayes"], "Bayesian", "fixed_bayes"),
    }

    corrected_slice_metrics = {str(zpt): compare_hist(
        get_hist(files["cpp_corrected"], slice_name("Bin", zpt)), corrected_reference_slices[zpt])
        for zpt in ZPT_BINS}
    corrected_slice_summary = {
        "slices": len(corrected_slice_metrics),
        "bins": sum(value["bins"] for value in corrected_slice_metrics.values()),
        "content_mismatches_exact": sum(value["content_mismatches_exact"] for value in corrected_slice_metrics.values()),
        "error_mismatches_exact": sum(value["error_mismatches_exact"] for value in corrected_slice_metrics.values()),
        "content_max_abs": max(value["content_max_abs"] for value in corrected_slice_metrics.values()),
        "error_max_abs": max(value["error_max_abs"] for value in corrected_slice_metrics.values()),
    }

    report = {
        "inputs": {key: str(value) for key, value in FILES.items()},
        "q2y": 1,
        "zpt_bins": ZPT_BINS,
        "python_cpp_correction_off": {
            "dense": compare_hist(cpp_off, python_off),
            "slices": compare_slices(files["cpp_off"], files["python_off"], "Bin", "Bin"),
        },
        "corrected_case": {
            "cpp_vs_python_reference_dense": compare_hist(cpp_corrected, reference),
            "cpp_vs_python_reference_slices": corrected_slice_summary,
            "cpp_vs_legacy_python_divide_unweighted_dense": compare_hist(cpp_corrected, python_legacy),
            "interpretation": "The independent Python reference consumes the C++-saved column-corrected rec/gen histograms and repeats the exact bin-by-bin alignment/add/divide/mask arithmetic. The production Python DivUnw mode is a different legacy correction (histogram-wise division), so it is reported separately and is not treated as column-correction parity.",
        },
        "repaired_vs_faulty_binbybin": {
            "dense": compare_hist(cpp_corrected, old_bin),
            "integrals": {
                "faulty": old_bin.Integral(), "repaired": cpp_corrected.Integral(),
                "completed_nominal_bayes": completed_bayes.Integral(),
                "faulty_fraction_of_bayes": old_bin.Integral() / completed_bayes.Integral(),
                "repaired_fraction_of_bayes": cpp_corrected.Integral() / completed_bayes.Integral(),
            },
            "repaired_vs_completed_nominal_bayes": compare_hist(cpp_corrected, completed_bayes),
            "faulty_vs_completed_nominal_bayes": compare_hist(old_bin, completed_bayes),
            "fit_shift_repaired_vs_faulty": fit_shift(fit_sets["repaired_bin"], fit_sets["old_faulty_bin"]),
            "fit_shift_repaired_vs_completed_nominal_bayes": fit_shift(fit_sets["repaired_bin"], fit_sets["completed_nominal_bayes"]),
            "fit_shift_faulty_vs_completed_nominal_bayes": fit_shift(fit_sets["old_faulty_bin"], fit_sets["completed_nominal_bayes"]),
        },
        "bayesian_fake_background": {
            "mask": {
                "old_count": len(old_mask), "new_count": len(new_mask), "fixed_count": len(fixed_mask),
                "added_by_unweighted_fake": sorted(set(new_mask) - set(old_mask)),
                "removed_by_unweighted_fake": sorted(set(old_mask) - set(new_mask)),
                "fixed_equals_old": fixed_mask == old_mask,
                "old_indices": old_mask, "new_indices": new_mask,
            },
            "old_vs_new_dense": compare_hist(old_bayes, new_bayes),
            "old_vs_fixed_old_mask_dense": compare_hist(old_bayes, fixed_bayes),
            "fixed_old_mask_vs_new_dense": compare_hist(fixed_bayes, new_bayes),
            "fixed_old_mask_vs_new_excluding_membership_changes": compare_hist_selected(
                fixed_bayes, new_bayes, sorted(set(new_mask) ^ set(fixed_mask))),
            "fit_shift_old_vs_new": fit_shift(fit_sets["old_bayes"], fit_sets["new_bayes"]),
            "fit_shift_old_vs_fixed_old_mask": fit_shift(fit_sets["old_bayes"], fit_sets["fixed_old_mask_bayes"]),
        },
        "fits": fit_sets,
    }

    rho_name = "(1D)_(rdf_wExclusive_Background)_(SMEAR=Smear)_(Q2_y_Bin_1)_(z_pT_Bin_All)_(MultiDim_z_pT_Bin_Y_bin_phi_t)"
    old_rho = files["old_bayes"].Get(rho_name)
    new_rho = files["new_bayes"].Get(rho_name)
    report["rho0_subtraction_unchanged"] = compare_hist(old_rho, new_rho) if old_rho and new_rho else {"available": False}

    (HERE / "q2y1_comparison_report.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    (FITS / "q2y1_fit_parameters.json").write_text(json.dumps(fit_sets, indent=2, sort_keys=True))

    save_plot(PLOTS / "python_cpp_binbybin_parity_q2y1.pdf", [
        (relative_vector(cpp_off, python_off), "Correction off: C++ minus Python", "signed relative content difference", ROOT.kBlue + 1),
        (relative_vector(cpp_off, python_off, True), "Correction off: C++ minus Python", "signed relative error difference", ROOT.kGreen + 2),
        (relative_vector(cpp_corrected, reference), "Column-corrected: C++ minus Python reference", "signed relative content difference", ROOT.kMagenta + 1),
    ])
    save_plot(PLOTS / "binbybin_repaired_vs_faulty_and_bayes_q2y1.pdf", [
        (relative_vector(cpp_corrected, old_bin), "Repaired minus saved faulty bin-by-bin", "signed relative content difference", ROOT.kRed + 1),
        (relative_vector(cpp_corrected, completed_bayes), "Repaired bin-by-bin minus completed nominal Bayesian", "signed relative content difference", ROOT.kBlue + 1),
        (relative_vector(old_bin, completed_bayes), "Saved faulty bin-by-bin minus completed nominal Bayesian", "signed relative content difference", ROOT.kGray + 2),
    ])
    save_plot(PLOTS / "bayesian_unweighted_fake_mask_isolation_q2y1.pdf", [
        (relative_vector(old_bayes, fixed_bayes), "Old Bayesian minus new fake with fixed old mask", "signed relative content difference", ROOT.kGreen + 2),
        (relative_vector(fixed_bayes, new_bayes), "Fixed old mask minus new unweighted-fake mask", "signed relative content difference", ROOT.kOrange + 7),
        ([1.0 if index in set(new_mask) - set(old_mask) else 0.0 for index in range(1, old_bayes.GetNbinsX() + 1)], "Newly excluded bins", "mask membership change", ROOT.kRed + 1),
    ])

    print(json.dumps({
        "report": str(HERE / "q2y1_comparison_report.json"),
        "correction_off_dense": report["python_cpp_correction_off"]["dense"],
        "correction_off_slices": {key: report["python_cpp_correction_off"]["slices"][key] for key in ["bins", "slices", "content_mismatches_exact", "error_mismatches_exact"]},
        "corrected_reference": report["corrected_case"]["cpp_vs_python_reference_dense"],
        "mask": report["bayesian_fake_background"]["mask"],
    }, indent=2))


if __name__ == "__main__":
    main()
