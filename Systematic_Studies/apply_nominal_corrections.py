#!/usr/bin/env python3
# Apply event-ratio RC and JSON bin-centering to a nominal copy, then fit BC_RC_Bayesian.
# RC division matches Comparison_Between_GEN_and_Unfold.Apply_RC.
# BC division matches Apply_BC_Corrections: y_new = y / BC_Factor.

import json
import math
import os
import subprocess
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys

PY = "/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"


def rc_histogram_name(name):
    return name.replace("_(Bayesian)_", "_(RC_Bayesian)_", 1)


def bc_histogram_name(name):
    return name.replace("_(RC_Bayesian)_", "_(BC_RC_Bayesian)_", 1)


def corrected_name(name):
    return bc_histogram_name(rc_histogram_name(name))


def apply_bc(hist, q2y_bin, zpt_bin, results, problems):
    for ib in range(1, hist.GetNbinsX() + 1):
        key = phys.bc_factor_key(q2y_bin, zpt_bin, ib)
        entry = results.get(key)
        if(not isinstance(entry, dict)):
            problems.append({"key": key, "reason": "missing"})
            return False
        factor = entry.get("BC_Factor")
        error = entry.get("BC_Factor_Err", 0.0)
        try:
            factor = float(factor)
            error = float(error)
        except (TypeError, ValueError):
            problems.append({"key": key, "reason": "invalid"})
            return False
        if((factor != factor) or (factor == 0.0)):
            problems.append({"key": key, "reason": "invalid"})
            return False
        content = float(hist.GetBinContent(ib))
        stat = float(hist.GetBinError(ib))
        hist.SetBinContent(ib, content / factor)
        hist.SetBinError(ib, math.sqrt((stat / factor) ** 2 + (content * error / (factor * factor)) ** 2))
    return True


def write_rc_only(nominal_path, rc_path, out_root):
    # Acceptance Bayesian histograms divided by the nominal event-ratio factor. No BC factor is applied.
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    source = ROOT.TFile.Open(nominal_path, "READ")
    rc_file = ROOT.TFile.Open(rc_path, "READ")
    dest = ROOT.TFile.Open(out_root, "RECREATE")
    problems = []
    written = 0
    names = []
    for key in source.GetListOfKeys():
        name = key.GetName()
        if("(MultiDim_3D_Histo)_(Bayesian)_" not in name):
            continue
        if(("RC_Bayesian" in name) or ("BC_RC" in name) or ("Bin_All" in name) or ("z_pT_Bin_All" in name)):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        factor = rc_file.Get(phys.rc_factor_name(q2y, zpt))
        hist = key.ReadObj()
        if((factor is None) or (hist.GetNbinsX() != factor.GetNbinsX())):
            problems.append({"bin": [q2y, zpt], "reason": "missing_or_incompatible_rc"})
            continue
        corrected = hist.Clone(rc_histogram_name(name))
        corrected.Divide(factor)
        dest.cd()
        corrected.Write()
        names.append(corrected.GetName())
        written += 1
    dest.Close()
    rc_file.Close()
    source.Close()
    return {"written": written, "problems": problems, "names": names}


def assert_alternative_output(path):
    # Nominal RC and BC files live under corrected/. An alternative must not replace them.
    parts = os.path.abspath(path).split(os.sep)
    if("corrected" in parts):
        raise ValueError("refusing to write an alternative into a nominal corrected directory")
    if(os.path.exists(path)):
        raise ValueError("output already exists: %s" % path)


def cached_factor(cache_dir, mode, q2y, zpt, phi_bin, sf_index):
    path = os.path.join(cache_dir, phys.fixed_point_cache_name(mode, q2y, zpt, phi_bin, sf_index))
    if(not os.path.isfile(path)):
        return None, "missing"
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    if(payload.get("ok") is not True):
        return None, "not_ok"
    inner = payload.get("result")
    if(not isinstance(inner, dict)):
        return None, "missing_result"
    return phys.factor_from_fixed_point(inner)


def scale_hist_by_phi_factors(hist, factor_lookup, q2y, zpt, problems):
    # Cubature error stays out of the bin error. A missing factor drops the histogram.
    if(hist.GetNbinsX() != phys.PHI_BIN_COUNT):
        problems.append({"bin": [str(q2y), str(zpt)], "reason": "phi_count"})
        return False
    for phi_bin in range(1, phys.PHI_BIN_COUNT + 1):
        factor, reason = factor_lookup(phi_bin)
        if((factor is None) or (factor != factor) or (factor == 0.0)):
            problems.append({"bin": [str(q2y), str(zpt), phi_bin], "reason": reason})
            return False
        content = float(hist.GetBinContent(phi_bin))
        stat = float(hist.GetBinError(phi_bin))
        hist.SetBinContent(phi_bin, content / float(factor))
        hist.SetBinError(phi_bin, abs(stat / float(factor)))
    return True


def write_fixed_rc(nominal_path, cache_dir, sf_index, out_root):
    # Acceptance yields divided by sigma_tot/sigma_B. Not the event-ratio nominal.
    assert_alternative_output(out_root)
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    source = ROOT.TFile.Open(nominal_path, "READ")
    dest = ROOT.TFile.Open(out_root, "RECREATE")
    problems = []
    written = 0
    names = []
    for key in source.GetListOfKeys():
        name = key.GetName()
        if("(MultiDim_3D_Histo)_(Bayesian)_" not in name):
            continue
        if(("RC_Bayesian" in name) or ("BC_RC" in name) or ("Bin_All" in name) or ("z_pT_Bin_All" in name)):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        hist = key.ReadObj()
        corrected = hist.Clone(rc_histogram_name(name))

        def factor_lookup(phi_bin, q2y_bin=q2y, zpt_bin=zpt):
            return cached_factor(cache_dir, "RC", q2y_bin, zpt_bin, phi_bin, sf_index)

        if(not scale_hist_by_phi_factors(corrected, factor_lookup, q2y, zpt, problems)):
            continue
        dest.cd()
        corrected.Write()
        names.append(corrected.GetName())
        written += 1
    dest.Close()
    source.Close()
    return {"written": written, "problems": problems, "names": names, "sf_index": int(sf_index), "mode": "RC"}


def write_fixed_bc(rc_root, cache_dir, out_root):
    # Nominal RC yields divided by the raw-amplitude spline BC factor. Not the event BC.
    assert_alternative_output(out_root)
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    source = ROOT.TFile.Open(rc_root, "READ")
    dest = ROOT.TFile.Open(out_root, "RECREATE")
    problems = []
    written = 0
    names = []
    for key in source.GetListOfKeys():
        name = key.GetName()
        if("(MultiDim_3D_Histo)_(RC_Bayesian)_" not in name):
            continue
        if("BC_RC" in name):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        hist = key.ReadObj().Clone(bc_histogram_name(name))

        def factor_lookup(phi_bin, q2y_bin=q2y, zpt_bin=zpt):
            return cached_factor(cache_dir, "BC", q2y_bin, zpt_bin, phi_bin, None)

        if(not scale_hist_by_phi_factors(hist, factor_lookup, q2y, zpt, problems)):
            continue
        dest.cd()
        hist.Write()
        names.append(hist.GetName())
        written += 1
    dest.Close()
    source.Close()
    return {"written": written, "problems": problems, "names": names, "mode": "BC"}


def write_bc_on_rc(rc_root, bc_results, out_root):
    # Nominal BC factors applied once to the RC-corrected histograms.
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    source = ROOT.TFile.Open(rc_root, "READ")
    dest = ROOT.TFile.Open(out_root, "RECREATE")
    problems = []
    written = 0
    names = []
    for key in source.GetListOfKeys():
        name = key.GetName()
        if("(MultiDim_3D_Histo)_(RC_Bayesian)_" not in name):
            continue
        if("BC_RC" in name):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        hist = key.ReadObj().Clone(bc_histogram_name(name))
        if(not apply_bc(hist, q2y, zpt, bc_results, problems)):
            continue
        dest.cd()
        hist.Write()
        names.append(hist.GetName())
        written += 1
    dest.Close()
    source.Close()
    return {"written": written, "problems": problems, "names": names}


def correct_campaign(campaign, nominal_path, rc_path, bc_results, out_root):
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    source = ROOT.TFile.Open(nominal_path, "READ")
    rc_file = ROOT.TFile.Open(rc_path, "READ")
    dest = ROOT.TFile.Open(out_root, "RECREATE")
    problems = []
    written = 0
    for key in source.GetListOfKeys():
        name = key.GetName()
        if("(MultiDim_3D_Histo)_(Bayesian)_" not in name):
            continue
        if(("Q2_y_Bin_All" in name) or ("z_pT_Bin_All" in name)):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        factor_name = phys.rc_factor_name(q2y, zpt)
        factor = rc_file.Get(factor_name)
        hist = key.ReadObj()
        if((factor is None) or (hist.GetNbinsX() != factor.GetNbinsX())):
            problems.append({"bin": [q2y, zpt], "reason": "missing_or_incompatible_rc"})
            continue
        corrected = hist.Clone(corrected_name(name))
        corrected.Divide(factor)
        if(not apply_bc(corrected, q2y, zpt, bc_results, problems)):
            continue
        dest.cd()
        corrected.Write()
        written += 1
    dest.Close()
    rc_file.Close()
    source.Close()
    return {"campaign": campaign, "written": written, "problems": problems}


def fit_corrected(out_root, json_out):
    cmd = [
        PY, phys.FIT_SCRIPT,
        "--root", out_root,
        "--Use_TTree", "--fit", "--remake_fit", "--smear", "--save_json",
        "--json_name", json_out,
        "--fit_error_source", "histogram",
        "--unfolding_3D", "--fit_corrections", "BC_RC_Bayesian",
    ]
    env = os.environ.copy()
    root_build = os.path.join(phys.ANALYSIS_ROOT, "New_RooUnfold", "RooUnfold", "build-arm64")
    env["PYTHONPATH"] = root_build + (os.pathsep + env["PYTHONPATH"] if(env.get("PYTHONPATH")) else "")
    env["LD_LIBRARY_PATH"] = root_build + (os.pathsep + env["LD_LIBRARY_PATH"] if(env.get("LD_LIBRARY_PATH")) else "")
    env["DYLD_LIBRARY_PATH"] = root_build + (os.pathsep + env["DYLD_LIBRARY_PATH"] if(env.get("DYLD_LIBRARY_PATH")) else "")
    proc = subprocess.run(cmd, cwd=phys.ANALYSIS_ROOT, env=env)
    return proc.returncode


def main():
    # Writes one correction stage. Fitting is refine-phi-fits, not this script.
    import argparse
    parser = argparse.ArgumentParser(description="Write nominal RC or BC histograms. Does not fit.")
    parser.add_argument("-st", "--stage", required=True, choices=["rc", "bc", "fixed_rc", "fixed_bc", "subdivision_bc"])
    parser.add_argument("-c", "--campaign", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--cache_dir", default="")
    parser.add_argument("-s", "--sf", type=int, default=-1)
    parser.add_argument("--bc_json", default="")
    args = parser.parse_args()
    if(args.stage == "rc"):
        report = write_rc_only(args.input, phys.RC_FACTOR_ROOT, args.output)
    elif(args.stage == "bc"):
        bc = json.load(open(phys.BC_EVENT_JSON))
        report = write_bc_on_rc(args.input, bc["results"], args.output)
    elif(args.stage == "fixed_rc"):
        if(args.sf not in [0, 2]):
            raise SystemExit("fixed_rc requires --sf 0 or --sf 2")
        if(args.cache_dir == ""):
            raise SystemExit("fixed_rc requires --cache_dir")
        report = write_fixed_rc(args.input, args.cache_dir, args.sf, args.output)
    elif(args.stage == "fixed_bc"):
        if(args.cache_dir == ""):
            raise SystemExit("fixed_bc requires --cache_dir")
        report = write_fixed_bc(args.input, args.cache_dir, args.output)
    else:
        if(args.bc_json == ""):
            raise SystemExit("subdivision_bc requires --bc_json")
        assert_alternative_output(args.output)
        bc = json.load(open(args.bc_json))
        report = write_bc_on_rc(args.input, bc["results"], args.output)
        report["bc_json"] = args.bc_json
    report["campaign"] = args.campaign
    report["stage"] = args.stage
    phys.write_json(os.path.join(os.path.dirname(args.output), "correction_report.json"), report)
    print(args.campaign, args.stage, "histograms", report["written"], "problems", len(report["problems"]))


if(__name__ == "__main__"):
    main()
