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
    parser.add_argument("-st", "--stage", required=True, choices=["rc", "bc"])
    parser.add_argument("-c", "--campaign", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    if(args.stage == "rc"):
        report = write_rc_only(args.input, phys.RC_FACTOR_ROOT, args.output)
    else:
        bc = json.load(open(phys.BC_EVENT_JSON))
        report = write_bc_on_rc(args.input, bc["results"], args.output)
    report["campaign"] = args.campaign
    report["stage"] = args.stage
    phys.write_json(os.path.join(os.path.dirname(args.output), "correction_report.json"), report)
    print(args.campaign, args.stage, "histograms", report["written"], "problems", len(report["problems"]))


if(__name__ == "__main__"):
    main()
