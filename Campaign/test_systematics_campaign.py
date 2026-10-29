#!/usr/bin/env python3
# Static checks for the systematic campaign. No SLURM submission and no ROOT production.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.systematics_campaign import hpp_pair, self_test
from Campaign.systematics_worker_ledger import ledger_self_test
from Campaign import run_sidis_systematics_campaign as runner


def squeue_compact_is_pending():
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import run_sidis_DataFrame_pipeline as pipeline
    state = pipeline._parse_squeue_task_state("12345", 1, "12345_[1-17] PD")
    if(state != "PD"):
        raise SystemExit("compact pending array was not PD, got %s" % state)
    running = pipeline._parse_squeue_task_state("12345", 4, "12345_4 R")
    if(running == "PD"):
        raise SystemExit("a running task was treated as pending")


def hpp_matches_submit_full():
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import Submit_Full_Histogram_Creation_Pipeline as submit_full
    pure, comb = hpp_pair("work_b", "Final_Thesis")
    other_pure, other_comb = submit_full.hpp_paths_from_tag("Final_Thesis", "work_b")
    if((pure != other_pure) or (comb != other_comb)):
        raise SystemExit("HPP paths diverged from Submit_Full")


def dry_run_writes_manifest():
    code = runner.main(["-n", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-mlw", "41"])
    if(code != 0):
        raise SystemExit("dry-run exit %s" % code)
    camp = runner.campaign_directory("work_b", "systematics_self_test")
    manifest = runner.read_manifest(camp)
    if(manifest is None):
        raise SystemExit("dry-run did not write a manifest")
    if(len(manifest["phase1"]) != 34):
        raise SystemExit("dry-run phase1 count")
    if(len(manifest["phase2"]) != 74):
        raise SystemExit("dry-run both-mode phase2 count")
    nominal = [row for row in manifest["phase1"] if(row["id"] == "nominal")][0]
    other = [row for row in manifest["phase1"] if(row["id"] == "chi2_strict_pip")][0]
    if("cut_Complete_SIDIS_chi2_strict_pip" not in " ".join(other["command"])):
        raise SystemExit("dry-run dropped the strict chi2 cut")
    if("-mac" not in other["command"]):
        raise SystemExit("dry-run dropped Bank matching")
    if(nominal["hpp_nospline"] in [None, ""]):
        raise SystemExit("manifest is missing the noSpline path")
    resumed = runner.main(["-n", "-rs", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-ht", "NotTheOriginalTag"])
    if(resumed != 0):
        raise SystemExit("resume dry-run exit %s" % resumed)
    again = runner.read_manifest(camp)
    again_nom = [row for row in again["phase1"] if(row["id"] == "nominal")][0]
    if(again_nom["hpp_nospline"] != nominal["hpp_nospline"]):
        raise SystemExit("resume dry-run replaced the recorded HPP path")
    refused = runner.main(["-n", "-c", "systematics_cap_reject", "-droot", "work_b", "-mlw", "42"])
    if(refused == 0):
        raise SystemExit("cap 42 was accepted")


def bag(**overrides):
    class Bag(object):
        pass
    args = Bag()
    args.mode = "slurm"
    args.data_root = "work_b"
    args.cut_name = "cut_Complete_SIDIS_pipS6o"
    args.unsmeared = False
    args.z_axis_2D = "4D_Bin"
    args.no_make_root = False
    args.no_make_2D = True
    args.no_make_2D_rho = True
    args.no_unfold_5D = True
    args.make_2D_only = False
    args.unfold_5D_only = False
    args.old_3D_unfold = False
    args.no_fast = False
    args.valerii_bins = False
    args.use_hpp = True
    args.spline_weights = True
    args.spline_weight_file = "spline.txt"
    args.spline_file = "spline.txt"
    args.json_weights = False
    args.json_file = None
    args.hpp_weight_file = "/hpp/noSpline.hpp"
    args.hpp_weight_file_spline = "/hpp/withSpline.hpp"
    args.run_rho_weight = True
    args.no_run_rho_weight = False
    args.matching_criteria = "Bank"
    args.name = "Sys3D_pipS6o"
    args.name_in = ["*Final_Thesis_Files*.root"]
    args.root = "SIDIS_epip_Response_Matrices_from_RDataFrames.root"
    args.email_message_job = ""
    args.user_email_message = ""
    args.email = "none"
    args.extra = None
    args.slurm_array_jobid = None
    args.histogram_local_cap = None
    args.campaign_worker_cap = None
    args.campaign_worker_name = "systematics_3d_both_recovery_20261028"
    args.run_subdir_name = "Only_3D_Sys3D_pipS6o_Bank_cut_Complete_SIDIS_pipS6o_Response_Matrices_Final_Thesis_Files_10_27_2026"
    args.slurm_cpus = "1"
    args.slurm_mem = "4500M"
    args.slurm_time = "24:00:00"
    args.batch_ids = "5,9-10,105,108-109,113,127-128,167-168"
    args.replace_listed_batches = True
    args.only3d_slurm_mem = None
    args.submission_config = "pipS6o"
    args.num_batches = 171
    args.work_dir = "/tmp/hadd_work"
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


def recovery_static_checks():
    import json
    from Campaign.systematics_campaign import (
        append_submission_history, expand_batch_spec, load_recovery_batches, recovery_configs,
        recovery_failure_text, submission_history_path, submission_ids_for_config,
    )
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import run_sidis_DataFrame_pipeline as pipeline
    import Submit_Full_Histogram_Creation_Pipeline as submit_full
    json_path = os.path.join(_BOOT, "Campaign", "recovery_batches_systematics_3d_both_rnh_20261027.json")
    payload = load_recovery_batches(json_path)
    chosen = recovery_configs(payload)
    if(len(chosen) != 33):
        raise SystemExit("recovery config count %s" % len(chosen))
    by_id = {}
    total = 0
    for item in chosen:
        spec = expand_batch_spec(item["batches"])
        other = pipeline.parse_batch_id_spec(item["batches"], 171)
        if(spec != other):
            raise SystemExit("batch parser diverged for %s" % item["config"]["id"])
        by_id[item["config"]["id"]] = spec
        total += len(spec)
        if(item["config"]["nominal"]):
            raise SystemExit("nominal was included")
    if(total != 1580):
        raise SystemExit("recovery task count %s" % total)
    if((156 in by_id["pipS3o"]) or (157 in by_id["pipS3o"]) or (158 in by_id["pipS3o"])):
        raise SystemExit("pipS3o 156-158 were not dropped")
    if(108 in by_id["no_valerii_knockout"]):
        raise SystemExit("13660242_108 is still listed")
    if(112 in by_id["pipS6o"]):
        raise SystemExit("13660241_112 is still listed")
    if(111 in by_id["pipS6o"]):
        raise SystemExit("13660241_111 is still listed")
    if(105 not in by_id["pipS5o"]):
        raise SystemExit("pipS5o batch 105 was dropped")
    for item in payload["configs"]:
        indices = expand_batch_spec(item["batches"])
        if((item["original_job"] == "13660240") and (any(index in [156, 157, 158] for index in indices))):
            raise SystemExit("original job 13660240 still has 156-158")
        if((item["original_job"] == "13660242") and (108 in indices)):
            raise SystemExit("original job 13660242 still has 108")
        if((item["original_job"] == "13660241") and ((112 in indices) or (111 in indices))):
            raise SystemExit("original job 13660241 still has 111 or 112")

    script_args = bag()
    selected = pipeline.parse_batch_id_spec(script_args.batch_ids, 171)
    script = pipeline.slurm_array_script_text(script_args, "/volatile/example", 171, selected)
    if(("--time=24:00:00" not in script) or ("--mem-per-cpu=4500M" not in script)):
        raise SystemExit("recovery sbatch resources")
    if(script.count("rm -f ") != 1):
        raise SystemExit("array script rm count")
    if("Batch${BATCH_PAD}" not in script):
        raise SystemExit("rm is not limited to the array task")
    if("_Batch112.root" in script):
        raise SystemExit("array script names batch 112")
    array_line = [line for line in script.splitlines() if(line.startswith("#SBATCH --array="))][0]
    array_indices = pipeline.parse_batch_id_spec(array_line.split("=", 1)[1], 171)
    if((112 in array_indices) or (111 in array_indices) or (113 not in array_indices)):
        raise SystemExit("array index spec")
    plain = pipeline.slurm_array_script_text(bag(replace_listed_batches=False), "/volatile/example", 171, selected)
    if("rm -f" in plain):
        raise SystemExit("ordinary array script removes a batch file")
    kept = pipeline.stop_if_outside_batches_missing(bag(batch_ids="113,127"), "/definitely/missing", 171)
    if(kept != [113, 127]):
        raise SystemExit("replace_listed_batches still ran the outside-batch gate")

    product = [item for item in submit_full.PRODUCTS if(item["key"] == "Only_3D")][0]
    normal = bag(only3d_slurm_mem=None, slurm_mem="9GB", replace_listed_batches=False, batch_ids=None)
    normal_cmd = submit_full.build_pipeline_cmd(normal, "cut_Complete_SIDIS_pipS6o", product, "/hpp/a.hpp", "/hpp/b.hpp", mode="slurm", jobs=1)
    if(normal_cmd[normal_cmd.index("--slurm_mem") + 1] != "4GB"):
        raise SystemExit("Only_3D without -o3m is not 4GB")
    raised = bag(only3d_slurm_mem="4500M", replace_listed_batches=True)
    raised_cmd = submit_full.build_pipeline_cmd(raised, "cut_Complete_SIDIS_pipS6o", product, "/hpp/a.hpp", "/hpp/b.hpp", mode="slurm", jobs=1)
    if(raised_cmd[raised_cmd.index("--slurm_mem") + 1] != "4500M"):
        raise SystemExit("Only_3D -o3m was not forwarded")
    if("--replace_listed_batches" not in raised_cmd):
        raise SystemExit("replace flag was not forwarded")

    history_dir = "/tmp/SIDIS_systematics_campaign/work_b/submission_history_self_test"
    os.makedirs(history_dir, exist_ok=True)
    history_path = submission_history_path(history_dir)
    if(os.path.isfile(history_path)):
        os.remove(history_path)
    append_submission_history(history_dir, {
        "campaign": "systematics_3d_both_recovery_20261028",
        "configuration": "pipS6o",
        "phase": "phase1",
        "job_name": "RMatrix_pipS6o",
        "slurm_id": "200",
        "index_spec": script_args.batch_ids,
        "memory": "4500M",
        "wall": "24:00:00",
        "cpus": "1",
    })
    append_submission_history(history_dir, {
        "campaign": "systematics_3d_both_recovery_20261028",
        "configuration": "pipS6o",
        "phase": "phase2",
        "job_name": "Sys3D_pipS6o_inherited_Spline",
        "slurm_id": "201",
        "index_spec": "1-17",
        "memory": "15000",
        "wall": "1:40:00",
        "cpus": "1",
    })
    lines = open(history_path).read().splitlines()
    if(len(lines) != 2):
        raise SystemExit("jsonl line count %s" % len(lines))
    first = json.loads(lines[0])
    second = json.loads(lines[1])
    if((first["phase"] != "phase1") or (second["phase"] != "phase2")):
        raise SystemExit("jsonl phases")
    append_submission_history(history_dir, {
        "campaign": "systematics_3d_both_recovery_20261028",
        "configuration": "pipS6o",
        "phase": "phase1",
        "job_name": "RMatrix_pipS6o",
        "slurm_id": "202",
        "index_spec": script_args.batch_ids,
        "memory": "4500M",
        "wall": "24:00:00",
        "cpus": "1",
    })
    again = open(history_path).read().splitlines()
    if((len(again) != 3) or (json.loads(again[0]) != first) or (json.loads(again[1]) != second)):
        raise SystemExit("jsonl rewrote an earlier line")
    ids = submission_ids_for_config(history_dir, "pipS6o")
    body = recovery_failure_text("systematics_3d_both_recovery_20261028", "pipS6o", script_args.batch_ids, ids, "histogram pipeline exited 1")
    for token in ["systematics_3d_both_recovery_20261028", "pipS6o", "200", "201", "202", script_args.batch_ids]:
        if(token not in body):
            raise SystemExit("failure mail missing %s" % token)

    from jlab_work_paths import data_root_path
    root = data_root_path("work_b")
    if(os.path.isdir(root)):
        original = os.path.join(root, "SIDIS_Campaign", "systematics", "systematics_3d_both_rnh_20261027")
    else:
        original = "/tmp/SIDIS_systematics_campaign/work_b/systematics_3d_both_rnh_20261027"
    original_manifest = os.path.join(original, "manifest.json")
    if(original.startswith("/tmp/")):
        os.makedirs(original, exist_ok=True)
        marker = os.path.join(original, "marker.txt")
        if(not os.path.isfile(marker)):
            handle = open(marker, "w")
            handle.write("keep\n")
            handle.close()
        marker_text = open(marker).read()
        marker_time = os.path.getmtime(marker)
    else:
        marker = None
        marker_text = None
        marker_time = None
    if(os.path.isfile(original_manifest)):
        original_text = open(original_manifest).read()
    else:
        original_text = None
    import io
    from contextlib import redirect_stdout
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_both_recovery_20261028", "-droot", "work_b", "-wm", "both",
            "-rb", json_path,
        ])
    if(code != 0):
        raise SystemExit("recovery dry-run exit %s" % code)
    printed = stdout.getvalue()
    if("hadd after listed batches" not in printed):
        raise SystemExit("dry-run does not continue to the existing hadd")
    if("PHASE2" not in printed):
        raise SystemExit("dry-run does not continue to Phase 2")
    if(marker is not None):
        if((open(marker).read() != marker_text) or (os.path.getmtime(marker) != marker_time)):
            raise SystemExit("dry-run changed the original campaign marker")
    if(original_text is None):
        if(os.path.isfile(original_manifest)):
            raise SystemExit("dry-run wrote the original campaign manifest")
    elif(open(original_manifest).read() != original_text):
        raise SystemExit("dry-run changed the original campaign manifest")
    camp = runner.campaign_directory("work_b", "systematics_3d_both_recovery_20261028")
    if(os.path.abspath(camp) == os.path.abspath(original)):
        raise SystemExit("recovery dry-run used the original campaign directory")
    for walk_root, _dirs, files in os.walk(camp):
        for name in files:
            if(name.endswith(".sh")):
                raise SystemExit("dry-run wrote sbatch %s" % os.path.join(walk_root, name))
    if(os.path.isfile(os.path.join(camp, "submission_history.jsonl"))):
        raise SystemExit("dry-run wrote submission history")
    manifest = runner.read_manifest(camp)
    if((len(manifest["phase1"]) != 33) or (manifest.get("recovery_task_count") != 1580)):
        raise SystemExit("dry-run manifest counts")
    if(any(row["nominal"] for row in manifest["phase1"])):
        raise SystemExit("dry-run included nominal")
    if(len(manifest["phase2"]) != 66):
        raise SystemExit("dry-run phase2 count %s" % len(manifest["phase2"]))
    for row in manifest["phase1"]:
        command = row["command"]
        text = " ".join(command)
        if(("-m" not in command) or (command[command.index("-m") + 1] != "slurm")):
            raise SystemExit("recovery command is not slurm")
        if("-rlb" not in command):
            raise SystemExit("recovery command missing -rlb")
        if("--skip_slurm_hadd" in command):
            raise SystemExit("recovery command skips hadd")
        if(("-hso" in command) or ("sysregen" in text) or ("-rnh" in command)):
            raise SystemExit("recovery command regenerates HPP")
        cut = command[command.index("-cn") + 1]
        if(cut == "cut_Complete_SIDIS"):
            raise SystemExit("nominal cut was scheduled")
        listed = expand_batch_spec(command[command.index("-bids") + 1])
        if(listed != by_id[row["id"]]):
            raise SystemExit("batch_ids were not taken from the JSON for %s" % row["id"])
        if((command[command.index("-st") + 1] != "24:00:00") or (command[command.index("-o3m") + 1] != "4500M")):
            raise SystemExit("recovery resources")
        if(command[command.index("-hdate") + 1] != "10_27_2026"):
            raise SystemExit("hybrid date")
        if((not row["hpp_nospline"].endswith("generated_acceptance_weights_Final_Thesis_noSpline.hpp")) or (not row["hpp_spline"].endswith("generated_acceptance_weights_Final_Thesis_withSpline.hpp"))):
            raise SystemExit("HPP path was not the recorded Final_Thesis pair")
    weights = {}
    for row in manifest["phase2"]:
        if(row["branch"] != "inherited"):
            raise SystemExit("recovery scheduled a nominal-only branch")
        weights.setdefault(row["config_id"], []).append(row["weight_tag"])
    for config_id, tags in weights.items():
        if(tags != ["Spline", ""]):
            raise SystemExit("both-mode order for %s" % config_id)
    refused = runner.main([
        "-n", "-c", "systematics_recovery_reject_rnh", "-droot", "work_b", "-wm", "both",
        "-rb", json_path, "-rnh",
    ])
    if(refused == 0):
        raise SystemExit("recovery accepted nominal HPP regeneration")


def followup_recovery_20261029():
    import io
    from contextlib import redirect_stdout
    from Campaign.systematics_campaign import expand_batch_spec, load_recovery_batches, sbatch_script
    json_path = os.path.join(_BOOT, "Campaign", "recovery_batches_20261029.json")
    payload = load_recovery_batches(json_path)
    expected = {
        "dcv_tight_el": ("3-5,10-11,105,108-109,111-113", False),
        "dvz_loose_pip": ("2-5,7-13,94-96,99-101,104-115", False),
        "dvz_tight_pip": ("13,98,105,108-109,111-115,117-163", False),
        "pipS2o": ("3-5,9-10", False),
        "eS6o": ("165,167-168", False),
        "no_sector_pcal": ("126,128", False),
        "pipS6o": ("5,9-10,105,108-109,113,127-128,167-168", False),
        "ecband_tight_el": ("127-149", True),
        "pcalvol_loose": ("141-168", False),
        "ecthr_tight_el": ("4", True),
    }
    empty_ids = [
        "pcalvol_tight", "dcfidref_loose_el", "ecthr_loose_el", "eS2o", "dcfidref_tight_el",
        "eS3o", "pipS5o", "eS4o", "pipS4o", "eS5o", "no_pip_testdc", "noSmear", "pipS3o",
        "eS1o", "dcfid_tight_el", "chi2_strict_pip", "dcfid_loose_pip", "dcfid_tight_pip",
        "dcfid_loose_el", "pipS1o", "no_valerii_knockout",
    ]
    by_id = {}
    total = 0
    for item in payload["configs"]:
        by_id[item["id"]] = item
        if(str(item.get("batches", "")).strip() != ""):
            total += len(expand_batch_spec(item["batches"]))
    if((len(payload["configs"]) != 31) or (total != 170)):
        raise SystemExit("20261029 inventory is %s configs and %s tasks" % (len(payload["configs"]), total))
    for config_id, (spec, deferred) in expected.items():
        item = by_id[config_id]
        if((item["batches"] != spec) or (bool(item.get("defer_merge", False)) != deferred)):
            raise SystemExit("20261029 entry changed for %s" % config_id)
    for config_id in empty_ids:
        if(str(by_id[config_id].get("batches", "x")).strip() != ""):
            raise SystemExit("%s was given histogram batches" % config_id)
    for banned in ["nominal", "ecband_loose_el", "dcv_loose_el"]:
        if(banned in by_id):
            raise SystemExit("%s is in the 20261029 inventory" % banned)
    if(113 in expand_batch_spec(by_id["eS6o"]["batches"])):
        raise SystemExit("eS6o task 113 was listed")
    script = sbatch_script("SysUnfold", "/logs", "python3", "run_Simple_Unfold.py", "work_b", "/in.root", "/parts", "stem", "inherited", "AccSpline")
    if("/farm_out/richcap/%x-%A_%a-%j-%N.out" not in script):
        raise SystemExit("Phase 2 stdout is not /farm_out/richcap")
    if(("/w/ceph24/" in script) or ("slurm_logs" in script)):
        raise SystemExit("Phase 2 logs still use the work filesystem")
    kept = []
    for name in ["systematics_3d_both_rnh_20261027", "systematics_3d_both_recovery_20261028"]:
        path = os.path.join(_BOOT, "SIDIS_Campaign", "systematics", name, "manifest.json")
        if(os.path.isfile(path)):
            kept.append((path, os.path.getmtime(path), open(path).read()))
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_both_recovery_20261029", "-droot", "work_b", "-wm", "both",
            "-rb", json_path,
        ])
    if(code != 0):
        raise SystemExit("20261029 dry-run exit %s" % code)
    printed = stdout.getvalue()
    if("recovery tasks 170" not in printed):
        raise SystemExit("dry-run task count")
    if("nominal" in printed.split("PHASE1")[0]):
        pass
    camp = runner.campaign_directory("work_b", "systematics_3d_both_recovery_20261029")
    manifest = runner.read_manifest(camp)
    if((len(manifest["phase1"]) != 31) or (manifest.get("recovery_task_count") != 170)):
        raise SystemExit("20261029 manifest counts")
    deferred_ids = []
    empty_seen = 0
    for row in manifest["phase1"]:
        if(row["id"] == "nominal"):
            raise SystemExit("nominal was scheduled")
        if(row.get("batch_ids") in [None, ""]):
            empty_seen += 1
            if(("-bids" in row["command"]) or ("-rlb" in row["command"])):
                raise SystemExit("empty batch list still submits histograms")
        elif(row.get("defer_merge")):
            deferred_ids.append(row["id"])
            if("-dfm" not in row["command"]):
                raise SystemExit("deferred merge was not forwarded")
            if(113 in expand_batch_spec(row["batch_ids"])):
                raise SystemExit("active task 113 was resubmitted for %s" % row["id"])
        else:
            if("-dfm" in row["command"]):
                raise SystemExit("immediate merge was deferred")
    if((empty_seen != 21) or (sorted(deferred_ids) != ["ecband_tight_el", "ecthr_tight_el"])):
        raise SystemExit("empty or deferred set changed")
    pip = [row for row in manifest["phase1"] if(row["id"] == "pipS6o")][0]
    if(("-rlb" not in pip["command"]) or ("-dfm" in pip["command"]) or (len(expand_batch_spec(pip["batch_ids"])) != 11)):
        raise SystemExit("pipS6o was not routed through selective replace")
    if(printed.count("hadd deferred") != 2):
        raise SystemExit("deferred hadd lines %s" % printed.count("hadd deferred"))
    if(printed.count("skip histograms; verify merged response; then Phase 2") != 21):
        raise SystemExit("phase2-only lines")
    if("PHASE2 ecband_tight_el__inherited__Spline deferred" not in printed):
        raise SystemExit("deferred Phase 2 was printed as an unfold command")
    if("PHASE2 pipS3o__inherited__Spline lineage" not in printed):
        raise SystemExit("finished Phase 1 did not continue to Phase 2")
    if("PHASE2 pcalvol_loose__inherited__Spline lineage" not in printed):
        raise SystemExit("pcalvol_loose did not continue to Phase 2")
    for path, stamp, text in kept:
        if((os.path.getmtime(path) != stamp) or (open(path).read() != text)):
            raise SystemExit("dry-run changed %s" % path)
    for walk_root, _dirs, files in os.walk(camp):
        for name in files:
            if(name.endswith(".sh")):
                raise SystemExit("dry-run wrote sbatch %s" % name)


def main():
    self_test()
    ledger_self_test()
    squeue_compact_is_pending()
    hpp_matches_submit_full()
    dry_run_writes_manifest()
    recovery_static_checks()
    followup_recovery_20261029()
    print("systematics campaign self-test ok")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
