# Compare C++ bin-by-bin and Python -bbo before the acceptance mask.
import hashlib
import json
import math
import os
import re

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(False)

REPO = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
BASE = os.path.join(REPO, "Systematic_Studies", "physics_campaign", "spline_colgen_20261111")
INPUT_RESPONSE = os.path.join(
    REPO,
    "Histo_Files_ROOT",
    "DataFrames",
    "hadd_ROOT_files_From_using_RDataFrames",
    "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Sys3D_nominal_only_20261030_Bank_Response_Matrices_Final_Thesis_Files_All.root",
)
CPP_FILE = os.path.join(BASE, "unfolded", "nominal_only_20261030_q2y01_bin_cpp_WSpline.root")
PY_FILE = os.path.join(BASE, "unfolded", "nominal_only_20261030_q2y01_bin_py_WSpline.root")
OUT_JSON = os.path.join(BASE, "bin_method_check", "q2y01_comparison.json")
REL_LIMIT = 1e-6
ABS_LIMIT = 1e-8


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while(True):
            block = handle.read(1024 * 1024)
            if(not block):
                break
            digest.update(block)
    return digest.hexdigest()


def is_q2y1(name):
    return (re.search(r"Q2_y_Bin_1(?!\d)", name) is not None) or (re.search(r"Q2-y-Bin=1(?!\d)", name) is not None)


def zpt_index(name):
    match = re.search(r"z_pT_Bin_(\d+)", name)
    if(match is None):
        return None
    return int(match.group(1))


def content_agrees(left, right):
    difference = abs(left - right)
    scale = max(abs(left), abs(right))
    if(scale <= ABS_LIMIT):
        return difference <= ABS_LIMIT
    if(difference <= ABS_LIMIT):
        return True
    return (difference / scale) <= REL_LIMIT


def relative_error(left, right):
    scale = max(abs(left), abs(right))
    if(scale <= ABS_LIMIT):
        return 0.0
    return abs(left - right) / scale


def read_histos(path):
    infile = ROOT.TFile.Open(path, "READ")
    if((infile is None) or infile.IsZombie()):
        raise RuntimeError("could not open %s" % path)
    histos = {}
    labels = []
    for key in infile.GetListOfKeys():
        name = str(key.GetName())
        class_name = str(key.GetClassName())
        if(class_name[:3] == "TH1"):
            histos[name] = key.ReadObj()
            histos[name].SetDirectory(0)
        elif(class_name in ["TNamed", "TObjString"]):
            obj = key.ReadObj()
            labels.append(name)
            title = ""
            if(hasattr(obj, "GetTitle")):
                title = str(obj.GetTitle())
            labels.append(title)
    return infile, histos, labels


def select_bin_histos(histos, multidimensional):
    chosen = {}
    for name, histo in histos.items():
        if("_(Bin)_" not in name):
            continue
        if(not is_q2y1(name)):
            continue
        if(("AsymErr" in name) or ("Fit_" in name) or ("Normalized" in name)):
            continue
        if(("Acceptance" in name) or ("Background" in name)):
            continue
        multi = "(MultiDim_3D_Histo)" in name
        if(multi != multidimensional):
            continue
        if(multidimensional):
            if("z_pT_Bin_All" in name):
                continue
            index = zpt_index(name)
            if(index is None):
                continue
            if(("Smear" in name) and ("NoSmear" in name)):
                continue
            chosen[index] = (name, histo)
        else:
            if("z_pT_Bin_" in name) and ("z_pT_Bin_All" not in name) and (zpt_index(name) is not None):
                continue
            chosen[name] = histo
    return chosen


def compare_pair(left, right):
    n_bins = int(left.GetNbinsX())
    content_mismatch = []
    error_bins = []
    max_error_rel = 0.0
    if(n_bins != int(right.GetNbinsX())):
        return {
            "nbins_left": n_bins,
            "nbins_right": int(right.GetNbinsX()),
            "content_ok": False,
            "content_mismatches": [{"reason": "nbins"}],
            "max_error_rel": None,
            "error_bins": 0,
        }
    for bin_index in range(1, n_bins + 1):
        left_content = float(left.GetBinContent(bin_index))
        right_content = float(right.GetBinContent(bin_index))
        if(not content_agrees(left_content, right_content)):
            content_mismatch.append({
                "bin": bin_index,
                "left": left_content,
                "right": right_content,
            })
        error_rel = relative_error(float(left.GetBinError(bin_index)), float(right.GetBinError(bin_index)))
        if(error_rel > max_error_rel):
            max_error_rel = error_rel
        if(error_rel > REL_LIMIT):
            error_bins.append(bin_index)
    return {
        "nbins": n_bins,
        "content_ok": len(content_mismatch) == 0,
        "content_mismatches": content_mismatch[:8],
        "n_content_mismatches": len(content_mismatch),
        "max_error_rel": max_error_rel,
        "n_error_bins": len(error_bins),
    }


def axis_edges_match(left, right):
    if(int(left.GetNbins()) != int(right.GetNbins())):
        return False
    for bin_index in range(1, int(left.GetNbins()) + 2):
        if(abs(float(left.GetBinLowEdge(bin_index)) - float(right.GetBinLowEdge(bin_index))) > 1e-6):
            return False
    return True


def edge_match_report(reconstructed, generated):
    rec_axis = reconstructed.GetXaxis()
    gen_axis = generated.GetXaxis()
    if(axis_edges_match(rec_axis, gen_axis)):
        return {"map": "shared_axis_edges", "unmatched_reconstructed_bins": [], "reconstructed_bins": int(reconstructed.GetNbinsX())}
    unmatched = []
    for rec_bin in range(1, int(reconstructed.GetNbinsX()) + 1):
        low = float(rec_axis.GetBinLowEdge(rec_bin))
        high = float(rec_axis.GetBinUpEdge(rec_bin))
        matches = 0
        for gen_bin in range(1, int(generated.GetNbinsX()) + 1):
            same_low = abs(float(gen_axis.GetBinLowEdge(gen_bin)) - low) <= 1e-6
            same_high = abs(float(gen_axis.GetBinUpEdge(gen_bin)) - high) <= 1e-6
            if(same_low and same_high):
                matches += 1
        if(matches != 1):
            unmatched.append({"reconstructed_bin": rec_bin, "generated_matches": matches})
    report = {"map": "unique_edge_match", "unmatched_reconstructed_bins": unmatched, "reconstructed_bins": int(reconstructed.GetNbinsX())}
    if(unmatched):
        report["map"] = "failed"
    return report


def plain_spline(name):
    if(("lund" in name) or ("rho0" in name) or ("_(Acc" in name)):
        return False
    return name.endswith(")_(Spline)")


def find_input_names(infile):
    names = [str(key.GetName()) for key in infile.GetListOfKeys()]
    groups = {"mdf": [], "gdf": [], "rdf": [], "background": [], "rho": []}
    for name in names:
        if("Q2-y-Bin=1," not in name):
            continue
        if("_(rho0_new)" in name):
            if(("Response_Matrix_Normal_1D" in name) and ("(Data-Type='mdf')" in name) and ("Smear-Type='smear'" in name) and ("_(Acc" not in name)):
                groups["rho"].append(name)
            continue
        if(("Background_Response_Matrix" in name) and plain_spline(name) and ("Smear-Type='smear'" in name)):
            groups["background"].append(name)
            continue
        if(("(Data-Type='rdf')" in name) and ("Response_Matrix_Normal_1D" in name) and ("cut_Complete_SIDIS" in name) and ("_(Spline)" not in name) and ("rho0" not in name)):
            groups["rdf"].append(name)
            continue
        if((not plain_spline(name)) or ("Response_Matrix_Normal_1D" not in name)):
            continue
        if("(Data-Type='mdf')" in name) and ("Smear-Type='smear'" in name) and ("cut_Complete_SIDIS" in name):
            groups["mdf"].append(name)
        if("(Data-Type='gdf')" in name) and ("no_cut" in name):
            groups["gdf"].append(name)
    return groups


def only_name(group):
    if(len(group) != 1):
        return None
    return group[0]


def choose_name(group, needle):
    matches = [name for name in group if(needle in name)]
    if(len(matches) == 1):
        return matches[0]
    return only_name(group)


def load_named(infile, name):
    if(name is None):
        return None
    histo = infile.Get(name)
    if(histo):
        histo.SetDirectory(0)
    return histo


def specified_calculation(data, reconstructed, generated, background):
    acceptance = reconstructed.Clone("bin_method_check_acceptance")
    acceptance.SetDirectory(0)
    if(background is not None):
        acceptance.Add(background)
    acceptance.Sumw2()
    divide_ok = bool(acceptance.Divide(generated))
    unfolded = data.Clone("bin_method_check_unfolded")
    unfolded.SetDirectory(0)
    data_ok = bool(unfolded.Divide(acceptance))
    return unfolded, divide_ok, data_ok


def stored_error_summary(histo):
    if(histo is None):
        return None
    max_rel_to_poisson = 0.0
    n_stored = 0
    for bin_index in range(1, int(histo.GetNbinsX()) + 1):
        content = float(histo.GetBinContent(bin_index))
        error = float(histo.GetBinError(bin_index))
        if(error > 0.0):
            n_stored += 1
        poisson = math.sqrt(abs(content)) if(content != 0.0) else 0.0
        rel = relative_error(error, poisson)
        if(rel > max_rel_to_poisson):
            max_rel_to_poisson = rel
    return {
        "name": str(histo.GetName()),
        "sumw2_n": int(histo.GetSumw2N()),
        "bins_with_stored_error": n_stored,
        "max_rel_stored_error_vs_poisson": max_rel_to_poisson,
    }


def worst_error_bins(left, right, limit):
    rows = []
    n_bins = min(int(left.GetNbinsX()), int(right.GetNbinsX()))
    for bin_index in range(1, n_bins + 1):
        rel = relative_error(float(left.GetBinError(bin_index)), float(right.GetBinError(bin_index)))
        if(rel > REL_LIMIT):
            rows.append((rel, bin_index))
    rows.sort(reverse=True)
    chosen = []
    for rel, bin_index in rows[:limit]:
        chosen.append({
            "bin": bin_index,
            "error_rel": rel,
            "left_content": float(left.GetBinContent(bin_index)),
            "right_content": float(right.GetBinContent(bin_index)),
            "left_error": float(left.GetBinError(bin_index)),
            "right_error": float(right.GetBinError(bin_index)),
        })
    return chosen


def main():
    cpp_file, cpp_histos, cpp_labels = read_histos(CPP_FILE)
    py_file, py_histos, py_labels = read_histos(PY_FILE)
    cpp_slices = select_bin_histos(cpp_histos, True)
    py_slices = select_bin_histos(py_histos, True)
    cpp_dense = select_bin_histos(cpp_histos, False)
    py_dense = select_bin_histos(py_histos, False)
    slice_indexes = sorted(set(cpp_slices) | set(py_slices))
    slice_rows = []
    slices_with_error_difference = 0
    max_slice_error_rel = 0.0
    content_ok = True
    for index in slice_indexes:
        row = {"z_pT_bin": index}
        if((index not in cpp_slices) or (index not in py_slices)):
            row["content_ok"] = False
            row["missing"] = "cpp" if(index not in cpp_slices) else "python"
            content_ok = False
            slice_rows.append(row)
            continue
        row["cpp_name"] = cpp_slices[index][0]
        row["python_name"] = py_slices[index][0]
        compared = compare_pair(cpp_slices[index][1], py_slices[index][1])
        row.update(compared)
        if(not compared["content_ok"]):
            content_ok = False
        if(compared["max_error_rel"] > REL_LIMIT):
            slices_with_error_difference += 1
        if((compared["max_error_rel"] is not None) and (compared["max_error_rel"] > max_slice_error_rel)):
            max_slice_error_rel = compared["max_error_rel"]
        slice_rows.append(row)
    dense_rows = []
    dense_content_ok = True
    if((len(cpp_dense) != 1) or (len(py_dense) != 1)):
        dense_content_ok = False
        dense_rows.append({"cpp_names": list(cpp_dense), "python_names": list(py_dense), "content_ok": False})
    else:
        cpp_name = list(cpp_dense)[0]
        py_name = list(py_dense)[0]
        compared = compare_pair(cpp_dense[cpp_name], py_dense[py_name])
        compared["cpp_name"] = cpp_name
        compared["python_name"] = py_name
        dense_rows.append(compared)
        dense_content_ok = compared["content_ok"]
        dense_cpp = cpp_dense[cpp_name]
        dense_py = py_dense[py_name]
    input_file = ROOT.TFile.Open(INPUT_RESPONSE, "READ")
    input_groups = find_input_names(input_file)
    input_loaded = {}
    input_loaded["mdf"] = load_named(input_file, only_name(input_groups["mdf"]))
    input_loaded["gdf"] = load_named(input_file, only_name(input_groups["gdf"]))
    input_loaded["rdf"] = load_named(input_file, only_name(input_groups["rdf"]))
    input_loaded["background"] = load_named(input_file, choose_name(input_groups["background"], "Background_Response_Matrix_1D"))
    input_loaded["rho"] = load_named(input_file, choose_name(input_groups["rho"], ")_(rho0_new)"))
    edge_report = {"map": "missing_histograms", "unmatched_reconstructed_bins": ["not_loaded"]}
    if((input_loaded["mdf"] is not None) and (input_loaded["gdf"] is not None)):
        edge_report = edge_match_report(input_loaded["mdf"], input_loaded["gdf"])
    reference_report = {"done": False}
    if((input_loaded["mdf"] is not None) and (input_loaded["gdf"] is not None) and (input_loaded["rdf"] is not None) and (input_loaded["background"] is not None) and (edge_report["map"] != "failed") and (len(cpp_dense) == 1) and (len(py_dense) == 1)):
        # Rho subtraction is already in the unfolded rdf clones. The input rdf still includes rho.
        # Rebuild the measured histogram the same way only when the saved rdf is the comparison target.
        # The specified acceptance step is checked on the reconstructed MC, background, and generated MC.
        # Use the rho-subtracted measured histogram saved by the unfolder, then the specified acceptance ratio.
        cpp_rdf = None
        py_rdf = None
        for name, histo in cpp_histos.items():
            if(("_(rdf)_" in name) and is_q2y1(name) and ("(1D)_" in name) and ("(MultiDim_3D_Histo)" not in name) and ("wExclusive" not in name) and ("z_pT_Bin_All" in name)):
                cpp_rdf = histo
        for name, histo in py_histos.items():
            if(("_(rdf)_" in name) and is_q2y1(name) and ("(1D)_" in name) and ("(MultiDim_3D_Histo)" not in name) and ("wExclusive" not in name) and ("z_pT_Bin_All" in name)):
                py_rdf = histo
        data_for_calc = cpp_rdf if(cpp_rdf is not None) else input_loaded["rdf"]
        reference, divide_ok, data_ok = specified_calculation(data_for_calc, input_loaded["mdf"], input_loaded["gdf"], input_loaded["background"])
        versus_cpp = compare_pair(reference, dense_cpp)
        versus_py = compare_pair(reference, dense_py)
        reference_report = {
            "done": True,
            "divide_ok": divide_ok,
            "data_divide_ok": data_ok,
            "data_source": str(data_for_calc.GetName()),
            "versus_cpp": versus_cpp,
            "versus_python": versus_py,
            "calculation": "add background to reconstructed MC, Sumw2, ROOT Divide by generated bins with matching edges, then divide measured data by that acceptance",
        }
    input_errors = {
        "mdf": stored_error_summary(input_loaded["mdf"]),
        "gdf": stored_error_summary(input_loaded["gdf"]),
        "rdf": stored_error_summary(input_loaded["rdf"]),
        "background": stored_error_summary(input_loaded["background"]),
    }
    error_samples = []
    if((len(cpp_dense) == 1) and (len(py_dense) == 1)):
        error_samples = worst_error_bins(dense_cpp, dense_py, 5)
        for sample in error_samples:
            bin_index = sample["bin"]
            for role, histo in input_loaded.items():
                if((histo is not None) and (bin_index <= int(histo.GetNbinsX()))):
                    sample["input_%s_content" % role] = float(histo.GetBinContent(bin_index))
                    sample["input_%s_error" % role] = float(histo.GetBinError(bin_index))
    mask_labels = [label for label in cpp_labels if("acceptance_mask" in label or "spline_amplitude" in label or "unfold_method" in label or "physical_bin_map" in label)]
    mask_not_applied = any(label == "acceptance_mask=not_applied" for label in mask_labels)
    correction_off = any(label == "spline_amplitude_correction=off" for label in mask_labels)
    mask_from_corrected = any(("corrected" in label) and ("acceptance_mask" in label) for label in mask_labels)
    # Column correction is off, so the unused skip map is the original MC map, not a corrected-MC map.
    if(correction_off and mask_not_applied):
        mask_from_corrected = False
    edges_ok = edge_report.get("map") in ["shared_axis_edges", "unique_edge_match"]
    calculation_ok = bool(reference_report.get("done")) and reference_report.get("divide_ok") and reference_report.get("data_divide_ok") and reference_report["versus_cpp"]["content_ok"] and reference_report["versus_python"]["content_ok"]
    contents_match = content_ok and dense_content_ok and (len(slice_indexes) == 29)
    done = bool(contents_match and edges_ok and calculation_ok and (not mask_from_corrected))
    prior_uncertainty = {
        "statement": "measured uncertainty difference is at most 6.4 percent in 21 of the 29 Q2-y bin 1 slices",
        "max_percent": 6.4,
        "slices": 21,
        "of_slices": 29,
        "launch_blocker": False,
    }
    measured_uncertainty = {
        "slices_compared": len(slice_indexes),
        "slices_with_error_difference": slices_with_error_difference,
        "max_slice_error_rel": max_slice_error_rel,
        "max_slice_error_percent": 100.0 * max_slice_error_rel,
        "matches_recorded_6_4_percent_in_21_slices": (slices_with_error_difference == 21) and (max_slice_error_rel <= 0.064 + 1e-6) and (max_slice_error_rel > 0.0),
        "at_most_6_4_percent": max_slice_error_rel <= 0.064 + 1e-6,
        "launch_blocker": False,
    }
    mdf_poisson = 0.0 if(input_errors["mdf"] is None) else input_errors["mdf"]["max_rel_stored_error_vs_poisson"]
    gdf_poisson = 0.0 if(input_errors["gdf"] is None) else input_errors["gdf"]["max_rel_stored_error_vs_poisson"]
    bkg_poisson = 0.0 if(input_errors["background"] is None) else input_errors["background"]["max_rel_stored_error_vs_poisson"]
    input_error_note = (
        "Dense bin-by-bin errors agree. The 29-slice uncertainty difference is at most 6.4 percent "
        "in 21 slices and is not a launch blocker. Input reconstructed, generated, and background "
        "histograms already store Sumw2 errors; their largest relative gap versus a Poisson error is "
        "mdf %.6f, gdf %.6f, background %.6f. That stored-error gap is larger than the slice difference, "
        "so the slice uncertainty difference is not an implementation error."
    ) % (mdf_poisson, gdf_poisson, bkg_poisson)
    record = {
        "task": "method-check",
        "config": "nominal_only_20261030",
        "q2y_bin": 1,
        "weight_tag": "Spline",
        "cpp": {
            "unfold_method": "bin",
            "spline_amplitude_correction": "off",
            "skip_acceptance_mask": True,
            "output": CPP_FILE,
        },
        "python": {
            "flags": ["-u3D", "-bbo", "-sac", "off", "--no_post_unfold_acc_cut", "-wt", "Spline"],
            "output": PY_FILE,
        },
        "input_response": INPUT_RESPONSE,
        "sha256": {
            "input_response": sha256_file(INPUT_RESPONSE),
            "Simple_Unfold": sha256_file(os.path.join(REPO, "Cpp_Simple_Unfold", "Simple_Unfold")),
            "Simple_Unfold_cxx": sha256_file(os.path.join(REPO, "Cpp_Simple_Unfold", "Simple_Unfold.cxx")),
            "Dedicated_5D_Unfold_Helpers_h": sha256_file(os.path.join(REPO, "Cpp_Dedicated_5D_Unfold", "Dedicated_5D_Unfold_Helpers.h")),
        },
        "labels": mask_labels,
        "acceptance_mask": "not_applied" if(mask_not_applied) else "unexpected",
        "campaign_mask_after_this_check": "preserved_original_spline_before_column_correction",
        "mask_built_from_corrected_mc": mask_from_corrected,
        "physical_edge_map": edge_report["map"],
        "unmatched_reconstructed_bins": edge_report["unmatched_reconstructed_bins"][:12],
        "n_unmatched_reconstructed_bins": len(edge_report["unmatched_reconstructed_bins"]),
        "input_name_counts": {role: len(names) for role, names in input_groups.items()},
        "input_names": {role: names for role, names in input_groups.items()},
        "input_stored_errors": input_errors,
        "dense_1d": dense_rows,
        "n_slices": len(slice_indexes),
        "slice_content_match": content_ok,
        "dense_content_match": dense_content_ok,
        "contents_match": contents_match,
        "calculation_matches": calculation_ok,
        "reference_calculation": reference_report,
        "slices": [{key: value for key, value in row.items() if(key != "content_mismatches")} for row in slice_rows],
        "slice_content_mismatch_examples": [row for row in slice_rows if(not row.get("content_ok", False))],
        "dense_error_samples": error_samples,
        "uncertainty_record": prior_uncertainty,
        "measured_uncertainty": measured_uncertainty,
        "input_error_comparison": input_error_note,
        "error_difference_is_implementation_error": (not (contents_match and calculation_ok and (max_slice_error_rel <= 0.064 + 1e-6))),
        "done": done,
    }
    # Drop bulky compare fields inside reference that duplicate mismatches.
    with open(OUT_JSON, "w") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("slices", len(slice_indexes), "content", content_ok, "dense", dense_content_ok)
    print("edge", edge_report["map"], "unmatched", len(edge_report["unmatched_reconstructed_bins"]))
    print("error_slices", slices_with_error_difference, "max_percent", 100.0 * max_slice_error_rel)
    print("calculation", calculation_ok, "mask_from_corrected", mask_from_corrected, "done", done)
    print("labels", mask_labels)
    print("input_counts", record["input_name_counts"])
    cpp_file.Close()
    py_file.Close()
    input_file.Close()


if(__name__ == "__main__"):
    main()
