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


def corrected_name(name):
    return name.replace("_(Bayesian)_", "_(BC_RC_Bayesian)_", 1)


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
    handle = open(os.path.join(THIS_DIR, "sidis_physics_manifest.json"))
    manifest = json.load(handle)
    handle.close()
    bc = json.load(open(phys.BC_EVENT_JSON))
    results = bc["results"]
    budgets = json.load(open(os.path.join(THIS_DIR, "physics_campaign", "budgets.json")))
    for campaign in ["unweighted", "spline"]:
        nominal = manifest["nominals"][campaign]["path"]
        out_root = os.path.join(THIS_DIR, "physics_campaign", "corrected", campaign, "corrected.root")
        report = correct_campaign(campaign, nominal, phys.RC_FACTOR_ROOT, results, out_root)
        phys.write_json(os.path.join(os.path.dirname(out_root), "correction_report.json"), report)
        print(campaign, "histograms", report["written"], "problems", len(report["problems"]))
        if(report["written"] == 0):
            raise SystemExit("no corrected histograms for %s" % campaign)
        json_out = os.path.join(os.path.dirname(out_root), "fit.json")
        code = fit_corrected(out_root, json_out)
        print(campaign, "fit rc", code)
        if(code != 0):
            raise SystemExit("corrected fit failed for %s" % campaign)


if(__name__ == "__main__"):
    main()
