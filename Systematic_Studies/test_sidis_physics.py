# Lightweight checks for the SIDIS physics-results workflow. No fits and no farm jobs.

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys


def expect(condition, message):
    if(not condition):
        raise SystemExit(message)


def test_nominal_and_weights():
    manifest = phys.build_manifest()
    spline = manifest["nominals"]["spline"]
    unweighted = manifest["nominals"]["unweighted"]
    expect(os.path.basename(spline["path"]) == phys.SPLINE_NOMINAL_NAME, "spline nominal file")
    expect(spline["weight_tag"] == "Spline", "spline nominal tag")
    expect("AccSpline" not in os.path.basename(spline["path"]), "spline nominal name")
    expect(unweighted["weight_tag"] == "", "unweighted nominal tag")
    for row in manifest["variations"]:
        expect(row["weight_tag"] != "AccSpline" or row["source"] == "acceptance_reweighting", "AccSpline role")
        if(row["source"] == "acceptance_reweighting" and row["campaign"] == "spline"):
            expect(os.path.basename(row["path"]) == phys.ACCSPLINE_VARIATION_NAME, "AccSpline variation")
            expect(row["nominal_id"] == "nominals.spline", "AccSpline nominal id")
        if(row["source"] == "acceptance_reweighting" and row["campaign"] == "unweighted"):
            expect(row["weight_tag"] == "Acc", "Acc tag")
            expect(row["path_status"] == "absent_on_disk", "Acc absent")
            expect(row["path"] is None, "Acc path")
    blocked = manifest["method_branches_blocked"]
    branches = sorted([row["branch"] for row in blocked])
    expect(branches == sorted(phys.BLOCKED_METHOD_BRANCHES), "blocked branches %s" % branches)
    for row in blocked:
        expect(row["eligible"] is False, "blocked eligible")
        expect(row["study_state"] == "blocked", "blocked study")
        expect(row["path_status"] == "verified", "blocked AccSpline file is on disk")
        expect(row["spline_path"] is None, "blocked spline substitute")
    jobs = phys.fit_jobs(manifest, "spline")
    for job in jobs:
        expect(job["weight_tag"] != "AccSpline" or job["source"] == "acceptance_reweighting", "fit job AccSpline")
        expect(phys.weight_pair_allowed(job["source"] if(job["kind"] == "variation") else "nominal", job["nominal_tag"], job["weight_tag"]), "pair")
    expect(phys.weight_pair_allowed("acceptance_reweighting", "", "Acc"), "acc pair")
    expect(phys.weight_pair_allowed("acceptance_reweighting", "Spline", "AccSpline"), "accspline pair")
    expect(not phys.weight_pair_allowed("dcfid_el", "Spline", "AccSpline"), "cut cross weight")
    expect(not phys.weight_pair_allowed("nominal", "Spline", "AccSpline"), "nominal cross weight")
    removed = json.loads(json.dumps(manifest))
    for row in removed["variations"]:
        if(row["campaign"] == "spline" and row["source"] == "dcfid_el"):
            row["path"] = None
            row["path_status"] = "absent_on_disk"
    for job in phys.fit_jobs(removed, "spline"):
        expect(job["source"] != "dcfid_el", "missing spline was not replaced")
    print("nominal and weight checks ok")
    return manifest


def test_shards_and_commands(manifest):
    jobs = phys.fit_jobs(manifest, "unweighted")
    shards = phys.shard_jobs(jobs, 2)
    expect(len(shards) == 2, "shard count")
    expect(sum(len(shard) for shard in shards) == len(jobs), "shard coverage")
    bayes = [job for job in jobs if(job["method"] == "Bayesian")][0]
    bbb = [job for job in phys.fit_jobs(manifest, "spline") if(job["method"] == "Bin")]
    expect(len(bbb) == 1, "one spline bin-by-bin job")
    copy_root = "/tmp/sidis_fit_copy.root"
    bayes["dimension"] = "3D"
    five = dict(bayes)
    five["dimension"] = "5D"
    five["source"] = "dimension"
    five["kind"] = "variation"
    five_cmd = phys.plan_fit_command(five, copy_root, "/tmp/five.json", None)
    expect("--unfolding_5D" in five_cmd and "--unfolding_3D" not in five_cmd, "5d command")
    bayes_cmd = phys.plan_fit_command(bayes, copy_root, "/tmp/bayes.json", None)
    expect("--unfolding_3D" in bayes_cmd and "--unfolding_5D" not in bayes_cmd, "3d command")
    bin_cmd = phys.plan_fit_command(bbb[0], copy_root, "/tmp/bin.json", "/tmp/init.py")
    expect("--unfolding_3D" in bayes_cmd and "--fit_corrections" in bayes_cmd and "Bayesian" in bayes_cmd, "bayes command")
    expect("--unfolding_3D" in bin_cmd and "--unfolding_1D" not in bin_cmd and "(Bin)" in bin_cmd, "bin command")
    expect(phys.expected_fit_key(bbb[0]) == "Fit_Pars_from_3D_Bin", "bin json key")
    expect(phys.fit_config_fingerprint(bbb[0]) == "3D|Bin|MultiDim_3D_Histo", "bin fingerprint")
    expect("--Apply_RC" not in bayes_cmd and "--Apply_BC" not in bin_cmd, "no correction flags")
    expect(bayes_cmd[bayes_cmd.index("--root") + 1] == copy_root, "copy root")
    try:
        phys.plan_fit_command(bayes, bayes["input_path"], "/tmp/x.json", None)
        raise SystemExit("input path was accepted as the fit output")
    except ValueError:
        pass
    print("command checks ok")


def test_rms_and_dominance():
    bin_name = "(Q2_y_Bin_1)-(z_pT_Bin_2)"
    one = phys.variation_bin_record("particle", "loose", bin_name, {
        "A": {"nominal": 0.10, "variation": 0.13, "stat_nominal": 0.02},
        "B": {"nominal": 0.0, "variation": 0.0, "stat_nominal": 0.0},
        "C": {"nominal": 1.0, "variation": 1.0, "stat_nominal": None},
    })
    two = phys.variation_bin_record("particle", "tight", bin_name, {
        "A": {"nominal": 0.10, "variation": 0.04, "stat_nominal": 0.02},
        "B": {"nominal": 0.0, "variation": 0.0, "stat_nominal": 0.0},
        "C": {"nominal": 1.0, "variation": 1.0, "stat_nominal": None},
    })
    sector = phys.variation_bin_record("electron_sector", "eS1o", bin_name, {
        "A": {"nominal": 0.10, "variation": 0.50, "stat_nominal": 0.02},
        "B": {"nominal": 0.0, "variation": 0.0, "stat_nominal": 0.0},
        "C": {"nominal": 1.0, "variation": 1.0, "stat_nominal": None},
    })
    groups = {
        "particle": {bin_name: [one, two]},
        "electron_sector": {bin_name: [sector]},
    }
    result = phys.aggregate_campaign(groups, {"particle": "independent", "electron_sector": "not_combined"}, 1.0e-9)
    expect_rms = math.sqrt((0.03 ** 2 + (-0.06) ** 2) / 2.0)
    got = result["sources"]["particle"][bin_name]["A"]["up"]
    expect(abs(got - expect_rms) < 1.0e-12, "rms %s" % got)
    total = result["totals"][bin_name]["A"]["up"]
    expect(abs(total - expect_rms) < 1.0e-12, "sector entered the total")
    flags = [row for row in result["diagnostics"] if(row["parameter"] == "A" and row.get("source") == "particle")]
    expect(flags[0]["flag"] == "systematic_larger", "R_source flag")
    expect(abs(flags[0]["R_source"] - (expect_rms / 0.02)) < 1.0e-12, "R_source")
    zero = [row for row in result["diagnostics"] if(row["parameter"] == "B" and ("source" not in row))][0]
    expect(zero["flag"] == "fit_uncertainty_zero" and zero["R_total"] is None, "zero fit error")
    missing = [row for row in result["diagnostics"] if(row["parameter"] == "C" and ("source" not in row))][0]
    expect(missing["flag"] == "fit_uncertainty_missing", "missing fit error")
    print("rms and dominance ok")


def test_campaigns_stay_separate():
    bin_name = "(Q2_y_Bin_1)-(z_pT_Bin_1)"
    def one_campaign(delta):
        record = phys.variation_bin_record("acceptance_reweighting", "alt", bin_name, {
            "A": {"nominal": 1.0, "variation": 1.0 + delta, "stat_nominal": 0.1},
            "B": {"nominal": 0.0, "variation": 0.0, "stat_nominal": 0.1},
            "C": {"nominal": 0.0, "variation": 0.0, "stat_nominal": 0.1},
        })
        return phys.aggregate_campaign(
            {"acceptance_reweighting": {bin_name: [record]}},
            {"acceptance_reweighting": "independent"},
            1.0e-9,
        )
    left = one_campaign(0.2)
    right = one_campaign(0.5)
    expect(abs(left["totals"][bin_name]["A"]["up"] - 0.2) < 1.0e-12, "left budget")
    expect(abs(right["totals"][bin_name]["A"]["up"] - 0.5) < 1.0e-12, "right budget")
    expect(abs(left["totals"][bin_name]["A"]["up"] - right["totals"][bin_name]["A"]["up"]) > 0.1, "budgets differ")
    print("separate campaigns ok")


def test_normalization_and_registry():
    cells = {
        "(Q2_y_Bin_1)-(z_pT_Bin_1)": {
            "Fit_Par_A": 10.0, "Fit_Par_A_ERR": 1.0, "Fit_Par_A_SYS": 2.0,
            "Fit_Par_B": 0.2, "Fit_Par_B_ERR": 0.02, "Fit_Par_B_SYS": 0.04,
            "Fit_Par_C": -0.1, "Fit_Par_C_ERR": 0.01, "Fit_Par_C_SYS": 0.03,
        },
    }
    original = json.dumps(cells)
    stat_copy = phys.normalize_campaign_copy(cells, "statistical", {"(Q2_y_Bin_1)-(z_pT_Bin_1)": 4.0})
    sys_copy = phys.normalize_campaign_copy(cells, "systematic", {"(Q2_y_Bin_1)-(z_pT_Bin_1)": 4.0})
    merged = phys.merge_normalized(stat_copy, sys_copy)
    cell = merged["cells"]["(Q2_y_Bin_1)-(z_pT_Bin_1)"]
    expect(cell["Fit_Par_A"] == 2.5, "A0")
    expect(cell["Fit_Par_A_ERR"] == 0.25, "stat")
    expect(cell["Fit_Par_A_SYS"] == 0.5, "sys")
    expect(cell["Fit_Par_B"] == 0.2 and cell["Fit_Par_B_ERR"] == 0.02 and cell["Fit_Par_B_SYS"] == 0.04, "B unscaled")
    expect(cell["Fit_Par_C"] == -0.1, "C unscaled")
    expect(json.dumps(cells) == original, "source cells changed")
    expect(merged["unassigned_factor_uncertainty"] is True, "factor uncertainty assigned")
    folder = tempfile.mkdtemp(prefix="sidis_registry_")
    try:
        registry = phys.PhysicsRegistry(folder)
        wanted = {"stage": "fit", "producer": "test", "campaign": "spline", "source": "nominal", "input_size": "3", "input_mtime": "10", "config_fingerprint": "abc"}
        record = dict(wanted)
        record["status"] = "completed"
        record["validation"] = "ok"
        record["output"] = os.path.join(folder, "out.json")
        registry.append(record)
        expect(registry.find_reusable(wanted, False)["output"] == record["output"], "reuse")
        changed = dict(wanted)
        changed["input_mtime"] = "11"
        expect(registry.find_reusable(changed, False) is None, "stale mtime")
        expect(registry.find_reusable(changed, True) is None, "force")
        blocked = {"stage": "radiative", "status": "blocked", "validation": "ok", "study_state": "pending", "systematic": None}
        registry.append(blocked)
        expect(registry.find_completed({"stage": "fit", "campaign": "spline"}) is not None, "blocked sibling removed a fit")
    finally:
        shutil.rmtree(folder)
    print("normalization and registry ok")


def test_init_mosaic_radiative_bc_kt2():
    cells = {"(Q2_y_Bin_5)-(z_pT_Bin_16)": {"Fit_Par_B": 0.11, "Fit_Par_C": -0.07}}
    limits = {("5", "16"): {"B_limits": [-0.8, 0.8], "C_limits": [-0.5, 0.5]}}
    folder = tempfile.mkdtemp(prefix="sidis_init_")
    try:
        path = phys.write_init_module(cells, limits, os.path.join(folder, "init.py"))
        text = open(path["path"]).read()
        expect("0.11" in text and "B_limits" in text and "[-0.8, 0.8]" in text, "init module")
        broken = {"(Q2_y_Bin_1)-(z_pT_Bin_1)": {"Fit_Par_A": 1.0}}
        skipped = phys.write_init_module(broken, {}, os.path.join(folder, "skip.py"))
        expect(skipped["bins"] == 0 and len(skipped["skipped"]) == 1, "skipped bin")
    finally:
        shutil.rmtree(folder)
    artifact = {"normalization_status": "applied", "path": "/tmp/nominal.json"}
    cmd = phys.mosaic_command(artifact, False, "/tmp/spline", "spline")
    expect("--apply_A_corr" not in cmd and "-cs" not in cmd, "mosaic scale")
    expect("--sys_err_suffix" in cmd and "_SYS" in cmd and "_ERR" in cmd, "separate errors")
    try:
        phys.mosaic_command({"normalization_status": "unnormalized", "path": "/tmp/x.json"}, False, "", "spline")
        raise SystemExit("unnormalized mosaic was accepted")
    except ValueError:
        pass
    radiative = phys.radiative_report()
    expect(radiative["study_state"] == "pending" and radiative["systematic"] is None, "radiative value")
    expect(radiative["cross_section"]["path_status"] == "absent_on_disk", "cross section")
    expect(radiative["event_ratio_root"]["path_status"] == "needs_configuration", "event ratio")
    bc = phys.bin_centering_report({"num_sub_bins_q2": 3, "num_sub_bins_y": 3, "num_sub_bins_z": 3, "num_sub_bins_pt": 3, "num_sub_bins_phi": 5}, None, None)
    expect(bc["event_counts_match"] and bc["method"]["kind"] == "estimated_transfer", "bc label")
    expect(bc["method"]["systematic"] is None and bc["method"]["transfer_prescription"] == "user_decision", "bc transfer")
    expect(bc["iteration"]["combine"] == "not_combined", "iteration combine")
    points = [{"x": 0.0, "y": 0.0, "err": 0.1}, {"x": 1.0, "y": 1.0, "err": 0.1}, {"x": 2.0, "y": 3.0, "err": 0.1}]
    other = [{"x": 0.0, "y": 0.0, "err": 0.1}, {"x": 1.0, "y": 1.0, "err": 10.0}, {"x": 2.0, "y": 3.0, "err": 0.1}]
    same_y = [point["y"] for point in points] == [point["y"] for point in other]
    expect(same_y, "A0 central values")
    expect(phys.weighted_line_fit(points)["slope"] != phys.weighted_line_fit(other)["slope"], "slope changed with errors")
    print("init mosaic radiative bc kt2 ok")


def test_root_family_and_parser():
    py = "/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
    script = os.path.join(phys.ANALYSIS_ROOT, ".grok", "skills", "extract-sidis-kt2", "scripts", "extract_sidis_kt2.py")
    env = os.environ.copy()
    root_build = os.path.join(phys.ANALYSIS_ROOT, "New_RooUnfold", "RooUnfold", "build-arm64")
    env["PYTHONPATH"] = root_build + (os.pathsep + env["PYTHONPATH"] if(env.get("PYTHONPATH")) else "")
    env["LD_LIBRARY_PATH"] = root_build + (os.pathsep + env["LD_LIBRARY_PATH"] if(env.get("LD_LIBRARY_PATH")) else "")
    env["DYLD_LIBRARY_PATH"] = root_build + (os.pathsep + env["DYLD_LIBRARY_PATH"] if(env.get("DYLD_LIBRARY_PATH")) else "")
    help_run = subprocess.run([py, script, "--help"], capture_output=True, text=True, env=env)
    expect(help_run.returncode == 0, help_run.stderr)
    expect("systematic" in help_run.stdout and "uncertainty_source" in help_run.stdout, "parser default text")
    expect("default is systematic" in help_run.stdout, "systematic default")
    probe = subprocess.run([py, "-c", (
        "import ROOT\n"
        "ROOT.gROOT.SetBatch(True)\n"
        "path = %r\n"
        "handle = ROOT.TFile.Open(path, 'READ')\n"
        "keys = [key.GetName() for key in handle.GetListOfKeys()]\n"
        "bayes = sum(1 for name in keys if 'Bayesian' in name and 'RC_Bayesian' not in name and 'BC_' not in name)\n"
        "rc = sum(1 for name in keys if 'RC_Bayesian' in name or 'BC_RC' in name)\n"
        "fits = sum(1 for name in keys if 'Fit_Par' in name)\n"
        "print(bayes, rc, fits)\n"
        "handle.Close()\n"
    ) % os.path.join(phys.UNFOLDED_DIR, phys.SPLINE_NOMINAL_NAME)], capture_output=True, text=True, env=env)
    expect(probe.returncode == 0, probe.stderr)
    bayes, rc, fits = [int(token) for token in probe.stdout.split()]
    expect(bayes > 0 and rc == 0 and fits == 0, "family counts %s" % probe.stdout.strip())
    print("root family and parser ok")


def main():
    manifest = test_nominal_and_weights()
    test_shards_and_commands(manifest)
    test_rms_and_dominance()
    test_campaigns_stay_separate()
    test_normalization_and_registry()
    test_init_mosaic_radiative_bc_kt2()
    test_root_family_and_parser()
    print("sidis physics tests ok")


if(__name__ == "__main__"):
    main()
