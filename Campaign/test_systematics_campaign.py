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


def dry_run_leaves_manifest_bytes():
    # -n prints the plan and must not rewrite an existing manifest.
    code = runner.main(["-n", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-mlw", "41"])
    if(code != 0):
        raise SystemExit("dry-run exit %s" % code)
    manifest = runner.last_manifest
    if(manifest is None):
        raise SystemExit("dry-run did not build a manifest")
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
    camp = runner.campaign_directory("work_b", "systematics_self_test")
    runner.write_manifest(camp, manifest)
    path = runner.manifest_path(camp)
    before = open(path, "rb").read()
    sentinel = os.path.join(camp, "do_not_delete_batch.root")
    open(sentinel, "wb").write(b"keep")
    resumed = runner.main(["-n", "-rs", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-ht", "NotTheOriginalTag"])
    if(resumed != 0):
        raise SystemExit("resume dry-run exit %s" % resumed)
    if(open(path, "rb").read() != before):
        raise SystemExit("resume dry-run changed the manifest bytes")
    if(open(sentinel, "rb").read() != b"keep"):
        raise SystemExit("resume dry-run changed a batch file")
    again = runner.last_manifest
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
    manifest = runner.last_manifest
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
        "dcv_loose_el", "ecband_loose_el", "dcv_tight_el",
    ]
    by_id = {}
    total = 0
    for item in payload["configs"]:
        by_id[item["id"]] = item
        if(str(item.get("batches", "")).strip() != ""):
            total += len(expand_batch_spec(item["batches"]))
    if((len(payload["configs"]) != 33) or (total != 159)):
        raise SystemExit("20261029 inventory is %s configs and %s tasks" % (len(payload["configs"]), total))
    for config_id, (spec, deferred) in expected.items():
        item = by_id[config_id]
        if((item["batches"] != spec) or (bool(item.get("defer_merge", False)) != deferred)):
            raise SystemExit("20261029 entry changed for %s" % config_id)
    for config_id in empty_ids:
        if(str(by_id[config_id].get("batches", "x")).strip() != ""):
            raise SystemExit("%s was given histogram batches" % config_id)
    for banned in ["nominal"]:
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
    if("recovery tasks 159" not in printed):
        raise SystemExit("dry-run task count")
    if("nominal" in printed.split("PHASE1")[0]):
        pass
    camp = runner.campaign_directory("work_b", "systematics_3d_both_recovery_20261029")
    manifest = runner.last_manifest
    if((len(manifest["phase1"]) != 33) or (manifest.get("recovery_task_count") != 159)):
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
    if((empty_seen != 24) or (sorted(deferred_ids) != ["ecband_tight_el", "ecthr_tight_el"])):
        raise SystemExit("empty or deferred set changed")
    pip = [row for row in manifest["phase1"] if(row["id"] == "pipS6o")][0]
    if(("-rlb" not in pip["command"]) or ("-dfm" in pip["command"]) or (len(expand_batch_spec(pip["batch_ids"])) != 11)):
        raise SystemExit("pipS6o was not routed through selective replace")
    if(printed.count("hadd deferred") != 2):
        raise SystemExit("deferred hadd lines %s" % printed.count("hadd deferred"))
    if(printed.count("skip histograms; verify merged response; then Phase 2") != 24):
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


def complete_campaign_20261029():
    import io
    from contextlib import redirect_stdout
    from Campaign.systematics_campaign import (
        expand_batch_spec, load_recovery_batches, response_names_ready, systematic_batch_paths, worker_cap,
    )
    json_path = os.path.join(_BOOT, "Campaign", "recovery_batches_complete_20261029.json")
    old_path = os.path.join(_BOOT, "Campaign", "recovery_batches_20261029.json")
    payload = load_recovery_batches(json_path)
    old = load_recovery_batches(old_path)
    if(len(payload["configs"]) != 33):
        raise SystemExit("complete inventory config count")
    total = 0
    by_id = {}
    for item in payload["configs"]:
        by_id[item["id"]] = item
        if(str(item.get("batches", "")).strip() != ""):
            total += len(expand_batch_spec(item["batches"]))
    if(total != 130):
        raise SystemExit("complete histogram tasks %s" % total)
    if(str(by_id["dvz_loose_pip"].get("batches", "x")).strip() != ""):
        raise SystemExit("dvz_loose_pip still lists batches")
    if(not by_id["dvz_loose_pip"].get("external_merge")):
        raise SystemExit("dvz_loose_pip is not an external merge")
    for config_id in ["ecband_tight_el", "ecthr_tight_el"]:
        if((not by_id[config_id].get("defer_merge")) or (not by_id[config_id].get("auto_merge"))):
            raise SystemExit("%s is not an automatic merge" % config_id)
    if(by_id["pipS6o"].get("auto_merge")):
        raise SystemExit("pipS6o was switched to automatic merge")
    old_dvz = [item for item in old["configs"] if(item["id"] == "dvz_loose_pip")][0]
    if(str(old_dvz.get("batches", "")).strip() == ""):
        raise SystemExit("the October 29 recovery file lost dvz batches")
    names = []
    for q2y in range(1, 18):
        for tag in ["", "_(Spline)"]:
            names.append("(Histo-Group='Response_Matrix_Normal'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS_dcv_tight_el'), [Q2-y-Bin=%d, z]%s" % (q2y, tag))
            names.append("Response_Matrix_Normal_1D (Data-Type='gdf'), (Data-Cut='no_cut') [Q2-y-Bin=%d, z]%s" % (q2y, tag))
    if(not response_names_ready(names, "cut_Complete_SIDIS_dcv_tight_el")):
        raise SystemExit("object check rejected a complete name set")
    names_missing = list(names)
    names_missing.pop()
    if(response_names_ready(names_missing, "cut_Complete_SIDIS_dcv_tight_el")):
        raise SystemExit("object check accepted a missing spline generated histogram")
    paths = systematic_batch_paths("ecband_tight_el", "cut_Complete_SIDIS_ecband_tight_el", "10_27_2026")
    if((len(paths) != 171) or ("Batch001.root" not in paths[0]) or ("10_27_2026" not in paths[0]) or ("Sys3D_ecband_tight_el" not in paths[0])):
        raise SystemExit("EC batch path was not the existing volatile file")
    if(worker_cap(43, 43) != 43):
        raise SystemExit("complete cap 43 was rejected")
    try:
        worker_cap(44, 43)
        raise SystemExit("cap 44 was accepted")
    except ValueError:
        pass
    refused = runner.main(["-n", "-c", "systematics_3d_complete_cap", "-droot", "work_b", "-wm", "both", "-rb", json_path, "-incn", "-mlw", "44"])
    if(refused == 0):
        raise SystemExit("include_nominal accepted cap 44")
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_complete_20261029", "-droot", "work_b", "-wm", "both",
            "-rb", json_path, "-incn", "-mlw", "43",
        ])
    if(code != 0):
        raise SystemExit("complete dry-run exit %s" % code)
    printed = stdout.getvalue()
    if("recovery tasks 130" not in printed):
        raise SystemExit("complete dry-run task count")
    camp = runner.campaign_directory("work_b", "systematics_3d_complete_20261029")
    manifest = runner.last_manifest
    if((len(manifest["phase1"]) != 34) or (manifest.get("recovery_task_count") != 130)):
        raise SystemExit("complete manifest counts")
    nominal = [row for row in manifest["phase1"] if(row.get("nominal_complete"))]
    if(len(nominal) != 1):
        raise SystemExit("nominal complete row")
    command = " ".join(nominal[0]["command"])
    for token in ["-m slurm", "-sa", "-spf", "acc020_3D_BC_RC_rawA", "-hdate 10_29_2026", "-o3m 4500M", "Sys3D_nominal_complete_20261029"]:
        if(token not in command):
            raise SystemExit("nominal command missing %s" % token)
    for banned in ["-rnh", "-rlb", "-bids", "-dfm", "-cwc"]:
        if(banned in nominal[0]["command"]):
            raise SystemExit("nominal command contains %s" % banned)
    dvz = [row for row in manifest["phase1"] if(row["id"] == "dvz_loose_pip")][0]
    if((dvz["command"] != []) or (not dvz.get("external_merge"))):
        raise SystemExit("dvz_loose_pip was not left to the external merge")
    auto = []
    for row in manifest["phase1"]:
        if(row.get("auto_merge")):
            auto.append(row["id"])
            if("-dfm" not in row["command"]):
                raise SystemExit("%s submit does not defer the pipeline hadd" % row["id"])
            if("-rlb" not in row["command"]):
                raise SystemExit("%s does not replace only listed batches" % row["id"])
    if(sorted(auto) != ["ecband_tight_el", "ecthr_tight_el"]):
        raise SystemExit("automatic merge set %s" % auto)
    if(printed.count("hadd after all 171 batch files validate") != 2):
        raise SystemExit("automatic hadd lines")
    if("wait for external merge; then Phase 2" not in printed):
        raise SystemExit("dvz wait line missing")
    nominal_rows = [row for row in manifest["phase2"] if(row["config_id"] == "nominal_complete_20261029")]
    if(len(nominal_rows) != 11):
        raise SystemExit("nominal Phase 2 count %s" % len(nominal_rows))
    keys = [row["key"] for row in nominal_rows]
    for required in [
        "nominal_complete_20261029__inherited__AccSpline",
        "nominal_complete_20261029__BayesMinus1__AccSpline",
        "nominal_complete_20261029__BayesPlus1__AccSpline",
        "nominal_complete_20261029__Acc015__AccSpline",
        "nominal_complete_20261029__Acc025__AccSpline",
        "nominal_complete_20261029__Phi12__AccSpline",
        "nominal_complete_20261029__NoRho0__AccSpline",
        "nominal_complete_20261029__AcceptanceWeightVariation__Spline",
        "nominal_complete_20261029__inherited__Unweighted",
        "nominal_complete_20261029__BinByBin__Spline",
        "nominal_complete_20261029__BinByBin__Unweighted",
    ]:
        if(required not in keys):
            raise SystemExit("missing nominal Phase 2 %s" % required)
    if("nominal_complete_20261029__inherited__Spline" in keys):
        raise SystemExit("spline Bayesian was scheduled twice")
    bin_row = [row for row in nominal_rows if(row["key"].endswith("BinByBin__Unweighted"))][0]
    if(bin_row["lineage"] != [row["lineage"] for row in nominal_rows if(row["key"].endswith("BinByBin__Spline"))][0]):
        raise SystemExit("bin-by-bin weights do not share a lineage")
    if("-bbo" not in printed):
        raise SystemExit("bin-by-bin command was not printed")
    if(printed.count("PHASE2 ecband_tight_el__inherited__Spline deferred") != 0):
        raise SystemExit("EC Phase 2 stayed deferred")
    for walk_root, _dirs, files in os.walk(camp):
        for name in files:
            if(name.endswith(".sh")):
                raise SystemExit("dry-run wrote sbatch %s" % name)


def phase2_spline_nosmear_dry_run():
    import io
    from contextlib import redirect_stdout
    from Campaign.systematics_campaign import part_is_ready, part_notes_ready, written_output_path
    json_path = os.path.join(_BOOT, "Campaign", "recovery_batches_phase2_spline_nosmear.json")
    finished = [
        "chi2_strict_pip", "dcfid_loose_el", "dcfid_loose_pip", "dcfid_tight_el", "dcfid_tight_pip",
        "dcfidref_loose_el", "dcfidref_tight_el", "dcv_loose_el", "dcv_tight_el", "dvz_loose_pip",
        "ecband_loose_el", "ecband_tight_el", "ecthr_loose_el", "ecthr_tight_el",
        "eS1o", "eS2o", "eS3o", "eS4o", "eS5o", "eS6o",
        "no_pip_testdc", "no_sector_pcal", "no_valerii_knockout", "pcalvol_loose", "pcalvol_tight",
        "pipS1o", "pipS2o", "pipS3o", "pipS4o", "pipS5o",
    ]
    logical = "/parts/Sys3D_pcalvol_tight_inherited_Spline_q2y01.root"
    if(written_output_path(logical, "Spline") != "/parts/Sys3D_pcalvol_tight_inherited_Spline_q2y01_WSpline.root"):
        raise SystemExit("spline part path was not renamed")
    if(written_output_path(logical, "") != logical):
        raise SystemExit("unweighted part path changed")
    names = ["(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_1)_(z_pT_Bin_All)"]
    config_lines = ["error_mode=covariance"]
    inputs = ["SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Sys3D_pcalvol_tight_Bank_cut_Complete_SIDIS_pcalvol_tight_Response_Matrices_Final_Thesis_Files_All.root"]
    part = written_output_path(logical, "Spline")
    if(not part_notes_ready(names, config_lines, inputs, 1, "Spline", inputs[0], part, False)):
        raise SystemExit("a valid spline note set was rejected")
    if(part_notes_ready(names, config_lines, inputs, 1, "Spline", inputs[0], logical, False)):
        raise SystemExit("a spline file without the _WSpline suffix was accepted")
    if(part_notes_ready(names, ["error_mode=toys"], inputs, 1, "Spline", inputs[0], part, False)):
        raise SystemExit("a non-covariance part was accepted")
    smear_names = ["(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_1)_(z_pT_Bin_All)"]
    if(part_notes_ready(smear_names, config_lines, inputs, 1, "", inputs[0], logical, True)):
        raise SystemExit("a smeared histogram was accepted for noSmear")
    diag = "/tmp/sidis_phase2_diag/Sys3D_pcalvol_tight_inherited_Spline_q2y01_WSpline.root"
    if(os.path.isfile(diag)):
        if(not part_is_ready(diag, 1, "Spline", inputs[0], False)):
            raise SystemExit("the local spline bin did not pass the open check")
        if(part_is_ready(diag, 2, "Spline", inputs[0], False)):
            raise SystemExit("bin 2 was accepted from a bin 1 file")
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_phase2_recover_20261030", "-droot", "work_b", "-wm", "both",
            "-rb", json_path, "-suo", "-mlw", "43",
        ])
    if(code != 0):
        raise SystemExit("phase2 recovery dry-run exit %s" % code)
    printed = stdout.getvalue()
    camp = runner.campaign_directory("work_b", "systematics_3d_phase2_recover_20261030")
    manifest = runner.last_manifest
    ids = [row["id"] for row in manifest["phase1"]]
    if((len(ids) != 31) or ("dvz_tight_pip" in ids) or ("pipS6o" in ids) or ("noSmear" not in ids)):
        raise SystemExit("recovery inventory is not the 30 spline configs plus noSmear")
    for config_id in finished:
        rows = [row for row in manifest["phase2"] if(row["config_id"] == config_id)]
        if([row["weight_label"] for row in rows] != ["Spline"]):
            raise SystemExit("%s was not spline-only under -wm both" % config_id)
        if("systematics_3d_complete_20261029/unfolded" not in rows[0]["final"]):
            raise SystemExit("%s final is not in the shared unfolded directory" % config_id)
    nosmear = [row for row in manifest["phase2"] if(row["config_id"] == "noSmear")]
    if(sorted(row["weight_label"] for row in nosmear) != ["Spline", "Unweighted"]):
        raise SystemExit("noSmear was not scheduled for both weights")
    if(printed.count("--no_smear") < 2):
        raise SystemExit("noSmear commands did not pass --no_smear")
    if("PHASE2 pcalvol_tight__inherited__Unweighted" in printed):
        raise SystemExit("a finished Unweighted configuration was scheduled again")
    for walk_root, _dirs, files in os.walk(camp):
        for name in files:
            if(name.endswith(".sh")):
                raise SystemExit("dry-run wrote sbatch %s" % name)


def array_script_paths():
    import argparse
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import run_sidis_DataFrame_pipeline as pipeline
    from jlab_work_paths import REL_SPLINE_DEFAULT, apply_input_if_default
    rel_hpp = "Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_noSpline.hpp"
    rel_spline_hpp = "Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_withSpline.hpp"
    holder = argparse.Namespace(spline_weight_file=REL_SPLINE_DEFAULT, hpp_weight_file=rel_hpp, hpp_weight_file_spline=rel_spline_hpp)
    apply_input_if_default(holder, "spline_weight_file", ["-swf", "--spline_weight_file"], "work_b", argv=["-swf", REL_SPLINE_DEFAULT])
    apply_input_if_default(holder, "hpp_weight_file", ["-hppf", "--hpp_weight_file"], "work_b", argv=["-hppf", rel_hpp])
    apply_input_if_default(holder, "hpp_weight_file_spline", ["-hpp_swf", "--hpp_weight_file_spline"], "work_b", argv=["-hpp_swf", rel_spline_hpp])
    for product, only_3d in [["Only_3D", True], ["Only_5D", False]]:
        args = argparse.Namespace(
            run_subdir_name="%s_demo_10_30_2026" % product,
            slurm_cpus="1",
            slurm_mem="4500M" if(only_3d) else "14GB",
            slurm_time="24:00:00" if(only_3d) else "12:00:00",
            replace_listed_batches=False,
            data_root="work_b",
            cut_name="cut_Complete_SIDIS",
            unsmeared=False,
            z_axis_2D="4D_Bin",
            no_make_root=False,
            no_make_2D=True,
            no_make_2D_rho=True,
            no_unfold_5D=only_3d,
            make_2D_only=False,
            unfold_5D_only=(not only_3d),
            old_3D_unfold=False,
            no_fast=False,
            valerii_bins=False,
            use_hpp=True,
            spline_weights=True,
            spline_weight_file=holder.spline_weight_file,
            json_weights=False,
            hpp_weight_file=holder.hpp_weight_file,
            hpp_weight_file_spline=holder.hpp_weight_file_spline,
            run_rho_weight=True,
            matching_criteria="Bank",
            name="%s_demo" % product,
            name_in=["*Final_Thesis_Files*.root"],
            root="SIDIS_epip_Response_Matrices_from_RDataFrames.root",
            email_message_job="",
            extra=[],
        )
        text = pipeline.slurm_array_script_text(args, "/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/demo", 171, None)
        if("cd /lustre24/" not in text):
            raise SystemExit("%s array script does not cd to lustre" % product)
        parts = text.split()
        for flag in ["--spline_file", "--hpp_input_file", "--hpp_input_file_spline"]:
            value = parts[parts.index(flag) + 1]
            if(not value.startswith("/")):
                raise SystemExit("%s %s stayed relative: %s" % (product, flag, value))
        if(not parts[parts.index("--spline_file") + 1].endswith("acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt")):
            raise SystemExit("%s spline file name changed" % product)
        if(" --spline_file Prepare_Next_Iteration/" in text):
            raise SystemExit("%s script kept a bare spline path" % product)


def nominal_and_5d_dry_run():
    import io
    from contextlib import redirect_stdout
    from Campaign.systematics_campaign import NOMINAL_SYSREGEN_HPP
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_nominal_only_20261030", "-droot", "work_b", "-wm", "both",
            "-nmo", "-suo", "-mlw", "11",
        ])
    if(code != 0):
        raise SystemExit("nominal-only dry-run exit %s\n%s" % (code, stdout.getvalue()))
    printed = stdout.getvalue()
    camp = runner.campaign_directory("work_b", "systematics_3d_nominal_only_20261030")
    manifest = runner.last_manifest
    if(len(manifest["phase1"]) != 1) or (manifest["phase1"][0]["id"] != "nominal_only_20261030"):
        raise SystemExit("nominal-only dry-run did not select one phase1 configuration")
    if(len(manifest["phase2"]) != 11):
        raise SystemExit("nominal-only phase2 count %s" % len(manifest["phase2"]))
    if(printed.count("PHASE2 ") != 11):
        raise SystemExit("nominal-only printed %s phase2 rows" % printed.count("PHASE2 "))
    command = runner.command_text(manifest["phase1"][0]["command"])
    for token in ["-sa", "-m hybrid", "-j3D 1", "-j5D 0", "-cwc 11", NOMINAL_SYSREGEN_HPP]:
        if(token not in command):
            raise SystemExit("nominal-only command missing %s" % token)
    for banned in ["-rnh", "-hso", "-hsp ", " -spf Prepare_Next_Iteration/", " -m slurm ", " -rlb ", " -dfm ", " -bids ", " -y "]:
        if(banned in " %s " % command):
            raise SystemExit("nominal-only command contains %s" % banned)
    if(manifest["phase1"][0].get("auto_merge")) or (manifest["phase1"][0].get("batch_ids") not in [None, ""]):
        raise SystemExit("nominal hybrid added a second merge")
    if("/Prepare_Next_Iteration/acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt" not in command):
        raise SystemExit("nominal-only command spline path is not absolute")
    for row in manifest["phase2"]:
        if("systematics_3d_complete_20261029/unfolded" not in row["final"]):
            raise SystemExit("nominal phase2 final left the shared directory: %s" % row["final"])
        if(row["status"] != "waiting_phase1"):
            raise SystemExit("nominal phase2 was not waiting on phase1: %s" % row["status"])
    labels = [row["key"] for row in manifest["phase2"]]
    for needed in ["AcceptanceWeightVariation", "BinByBin", "Unweighted", "inherited__AccSpline"]:
        if(not any(needed in key for key in labels)):
            raise SystemExit("nominal phase2 missing %s" % needed)
    five_out = io.StringIO()
    with redirect_stdout(five_out):
        five_code = runner.main(["-n", "-c", "nominal_5d_spline_20261030", "-droot", "work_b", "-5ds"])
    if(five_code != 0):
        raise SystemExit("5D dry-run exit %s\n%s" % (five_code, five_out.getvalue()))
    five_text = five_out.getvalue()
    five_camp = runner.campaign_directory("work_b", "nominal_5d_spline_20261030")
    five_manifest = runner.last_manifest
    if(len(five_manifest["phase1"]) != 1) or (len(five_manifest["phase2"]) != 1):
        raise SystemExit("5D dry-run schedule is not one and one")
    five_command = runner.command_text(five_manifest["phase1"][0]["command"])
    for token in ["-m slurm", "-j5D 1", "-j3D 0", "-sa", "-dfm", "-rlb", "generated_acceptance_weights_Final_Thesis_withSpline.hpp"]:
        if(token not in five_command):
            raise SystemExit("5D command missing %s" % token)
    if(NOMINAL_SYSREGEN_HPP in five_command) or (" -spf Prepare_Next_Iteration/" in five_command):
        raise SystemExit("5D command kept a relative spline path or the 3D sysregen HPP")
    if(five_text.count("PHASE2 ") != 1) or ("-wt Spline" not in five_text) or ("starts after phase1 success" not in five_text):
        raise SystemExit("5D dry-run did not show one gated Spline unfold")
    for banned in ["-bi", "-ac ", "-ph ", "-err ", "AccSpline", "Unweighted"]:
        if(banned in five_text.split("PHASE2 ", 1)[1]):
            raise SystemExit("5D unfold overrides a launcher default or adds another weight: %s" % banned)
    if(five_manifest["phase2"][0]["status"] != "waiting_phase1"):
        raise SystemExit("5D phase2 was not waiting on phase1")
    if("systematics_3d_complete_20261029" in five_manifest["phase2"][0]["final"]):
        raise SystemExit("5D final was written into the 3D shared directory")
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import Submit_Full_Histogram_Creation_Pipeline as submit_full
    from jlab_work_paths import data_root_path, REL_SPLINE_DEFAULT
    product = [item for item in submit_full.PRODUCTS if(item["key"] == "Only_5D")][0]
    spline = os.path.join(data_root_path("work_b"), REL_SPLINE_DEFAULT)
    pure = os.path.join(data_root_path("work_b"), "Histo_Files_ROOT", "DataFrames", "HPP_Files_Output", "generated_acceptance_weights_Final_Thesis_noSpline.hpp")
    comb = os.path.join(data_root_path("work_b"), "Histo_Files_ROOT", "DataFrames", "HPP_Files_Output", "generated_acceptance_weights_Final_Thesis_withSpline.hpp")
    child = submit_full.build_pipeline_cmd(bag(
        name="Only_5D_nominal_spline_20261030",
        cut_name="cut_Complete_SIDIS",
        spline_file=spline,
        spline_weight_file=spline,
        hpp_weight_file=pure,
        hpp_weight_file_spline=comb,
        batch_ids="1",
        replace_listed_batches=True,
        defer_merge=True,
        slurm_time=None,
        slurm_mem=None,
        campaign_worker_name="nominal_5d_spline_20261030",
    ), "cut_Complete_SIDIS", product, pure, comb, mode="slurm", jobs=1)
    for token in ["--unfold_5D_only", "--no_make_2D", "--no_make_2D_rho", "--defer_merge", spline, comb]:
        if(token not in child):
            raise SystemExit("5D one-batch pipeline command missing %s" % token)
    if(child[child.index("--batch_ids") + 1] != "1"):
        raise SystemExit("5D one-batch proof did not select batch 1")


def pips6o_batch111_dry_run():
    import io
    import tempfile
    from contextlib import redirect_stdout
    from Campaign.systematics_campaign import pips6o_batch111_path, remove_named_batch_file
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = runner.main([
            "-n", "-c", "systematics_3d_pips6o_batch111_20261030", "-droot", "work_b", "-wm", "both",
            "-p6b", "-suo", "-mlw", "2",
        ])
    if(code != 0):
        raise SystemExit("pipS6o dry-run exit %s\n%s" % (code, stdout.getvalue()))
    camp = runner.campaign_directory("work_b", "systematics_3d_pips6o_batch111_20261030")
    manifest = runner.last_manifest
    if([row["id"] for row in manifest["phase1"]] != ["pipS6o"]):
        raise SystemExit("pipS6o dry-run selected another configuration")
    if("dvz_tight_pip" in stdout.getvalue()):
        raise SystemExit("pipS6o dry-run mentioned dvz_tight_pip")
    command = runner.command_text(manifest["phase1"][0]["command"])
    for token in ["-m sequential", "-bids 111", "-hdate 10_27_2026", "-n Sys3D_pipS6o", "-cn cut_Complete_SIDIS_pipS6o", "-sa"]:
        if(token not in command):
            raise SystemExit("pipS6o command missing %s" % token)
    for banned in [" -rlb ", " -st ", " -m slurm ", " -dfm ", " -y "]:
        if(banned in " %s " % command):
            raise SystemExit("pipS6o command contains %s" % banned)
    replaced = manifest["phase1"][0].get("replace_one_batch")
    if(replaced != pips6o_batch111_path()):
        raise SystemExit("pipS6o replace path drifted from the batch helper")
    labels = sorted(row["weight_label"] for row in manifest["phase2"])
    if(labels != ["Spline", "Unweighted"]):
        raise SystemExit("pipS6o Phase 2 pair changed")
    folder = tempfile.mkdtemp()
    keep = os.path.join(folder, "Batch110.root")
    gone = os.path.join(folder, "Batch111.root")
    open(keep, "w").close()
    open(gone, "w").close()
    if(not remove_named_batch_file(gone)) or os.path.isfile(gone) or (not os.path.isfile(keep)):
        raise SystemExit("the one-file removal touched another batch")


def command_has(command, token):
    return token in runner.command_text(command)


def nominal_plan(extra):
    import io
    from contextlib import redirect_stdout
    stdout = io.StringIO()
    argv = ["-n", "-c", "systematics_plc_nominal_check", "-droot", "work_b", "-wm", "both", "-nmo", "-suo"] + extra
    with redirect_stdout(stdout):
        code = runner.main(argv)
    if(code != 0):
        raise SystemExit("nominal concurrency dry-run exit %s\n%s" % (code, stdout.getvalue()))
    manifest = runner.last_manifest
    if((len(manifest["phase2"]) != 11) or (manifest["phase1"][0].get("auto_merge"))):
        raise SystemExit("nominal concurrency changed Phase 2 or the hybrid merge")
    return manifest["phase1"][0]["command"], stdout.getvalue()


def run_mocked_pool(jobs, n_batches, batch_ids, completed):
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import run_sidis_DataFrame_pipeline as pipeline
    state = {"inflight": 0, "peak": 0, "started": []}
    hadd_n = []
    saved = {}

    def patch(name, fn):
        saved[name] = getattr(pipeline, name)
        setattr(pipeline, name, fn)

    def load_batches(data_root, execution_root=None):
        return list(range(n_batches)), [], [], "mock"

    def start(args, batch_index, batch_output_dir, log_dir, block_for_slot=False):
        selected = pipeline.parse_batch_id_spec(getattr(args, "batch_ids", None), args.num_batches)
        if((selected is not None) and (int(batch_index) not in selected)):
            return None
        if(int(batch_index) in completed):
            return None
        state["inflight"] += 1
        if(state["inflight"] > state["peak"]):
            state["peak"] = state["inflight"]
        state["started"].append(int(batch_index))
        return {"batch_index": int(batch_index)}

    def finish(job_item, results, args):
        state["inflight"] -= 1
        results.append(0)
        return True

    def hadd(args, batch_output_dir, num_batches):
        hadd_n.append(int(num_batches))

    patch("resolved_batch_output_dir", lambda args, slurm=False: "/tmp/sidis_mock_batches")
    patch("ensure_directory", lambda path: path)
    patch("load_file_batches", load_batches)
    patch("Update_Email", lambda *args, **kwargs: None)
    patch("stop_if_outside_batches_missing", lambda args, output_dir, num_batches: None)
    patch("start_job", start)
    patch("finish_job", finish)
    patch("wait_for_remaining_slurm_tasks", lambda args: None)
    patch("hadd_response_batches", hadd)
    patch("estimate_peak_memory_children", lambda: "0")
    patch("Construct_Email", lambda *args, **kwargs: None)
    args = type("Pool", (), {})()
    args.jobs = int(jobs)
    args.mode = "parallel"
    args.batch_ids = batch_ids
    args.data_root = "work_b"
    args.log_dir = "/tmp"
    args.continue_on_failure = False
    args.campaign_resource_mode = None
    try:
        pipeline.run_local_batches(args)
    finally:
        for name, fn in saved.items():
            setattr(pipeline, name, fn)
    return state["peak"], state["started"], hadd_n


def nominal_local_concurrency():
    import tempfile
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import Submit_Full_Histogram_Creation_Pipeline as submit_full
    import run_sidis_DataFrame_pipeline as pipeline
    from Campaign.systematics_campaign import classify_saved_batches, nominal_resume_command
    default_cmd, _printed = nominal_plan(["-mlw", "30"])
    if((not command_has(default_cmd, "-j3D 1")) or (not command_has(default_cmd, "-cwc 30"))):
        raise SystemExit("omitted -plc did not stay at one local worker: %s" % runner.command_text(default_cmd))
    wide_cmd, _printed = nominal_plan(["-mlw", "30", "-plc", "30"])
    text = runner.command_text(wide_cmd)
    for token in ["-m hybrid", "-j3D 30", "-cwc 30", "-j 1"]:
        if(token not in text):
            raise SystemExit("nominal 30-worker command missing %s" % token)
    for banned in [" -rlb ", " -dfm ", " -bids ", " -y "]:
        if(banned in " %s " % text):
            raise SystemExit("nominal 30-worker command contains %s" % banned)
    capped_cmd, _printed = nominal_plan(["-mlw", "11", "-plc", "30"])
    capped = runner.command_text(capped_cmd)
    if(("-j3D 11" not in capped) or ("-cwc 11" not in capped) or ("-j3D 30" in capped)):
        raise SystemExit("the campaign cap did not limit -j3D: %s" % capped)
    refused = runner.main(["-n", "-c", "systematics_plc_reject_flag", "-droot", "work_b", "-plc", "30"])
    if(refused == 0):
        raise SystemExit("-plc was accepted without nominal_only")
    refused = runner.main(["-n", "-c", "systematics_plc_reject_zero", "-droot", "work_b", "-wm", "both", "-nmo", "-suo", "-plc", "0"])
    if(refused == 0):
        raise SystemExit("-plc 0 was accepted")
    old_argv = list(sys.argv)
    sys.argv = [wide_cmd[1]] + [str(token) for token in wide_cmd[2:]]
    try:
        parsed = submit_full.parse_args()
    finally:
        sys.argv = old_argv
    product = [item for item in submit_full.PRODUCTS if(item["key"] == "Only_3D")][0]
    jobs = submit_full.product_job_count(parsed, product)
    if(jobs != 30):
        raise SystemExit("Only_3D scheduler jobs were %s" % jobs)
    child = submit_full.build_pipeline_cmd(parsed, "cut_Complete_SIDIS", product, wide_cmd[wide_cmd.index("-hpf") + 1], wide_cmd[wide_cmd.index("-hps") + 1], mode="parallel", jobs=jobs)
    if(child[child.index("--jobs") + 1] != "30"):
        raise SystemExit("parallel --jobs did not receive -j3D")
    if(child[child.index("--campaign_worker_cap") + 1] != "30"):
        raise SystemExit("parallel worker cap was not -cwc")
    slurm = submit_full.build_pipeline_cmd(parsed, "cut_Complete_SIDIS", product, "/hpp/a.hpp", "/hpp/b.hpp", mode="slurm", jobs=jobs)
    if(("--jobs" in slurm) or ("--batch_ids" in slurm)):
        raise SystemExit("the SLURM leg was limited by the local worker count")
    peak, started, hadd_n = run_mocked_pool(jobs, 40, None, set())
    if((peak != 30) or (len(started) != 40) or (hadd_n != [40])):
        raise SystemExit("30 workers did not run together: peak %s started %s hadd %s" % (peak, len(started), hadd_n))
    sys.argv = [capped_cmd[1]] + [str(token) for token in capped_cmd[2:]]
    try:
        capped_parsed = submit_full.parse_args()
    finally:
        sys.argv = old_argv
    capped_jobs = submit_full.product_job_count(capped_parsed, product)
    peak, _started, _hadd_n = run_mocked_pool(capped_jobs, 40, None, set())
    if((capped_jobs != 11) or (peak != 11)):
        raise SystemExit("the global cap did not limit the scheduler: jobs %s peak %s" % (capped_jobs, peak))
    peak, _started, _hadd_n = run_mocked_pool(1, 40, None, set())
    if(peak != 1):
        raise SystemExit("the default scheduler started %s workers" % peak)
    peak, started, hadd_n = run_mocked_pool(30, 8, "1-6", set([2]))
    if((peak != 5) or (started != [1, 3, 4, 5, 6]) or (hadd_n != [8])):
        raise SystemExit("completed or unlisted batches were started: %s hadd %s" % (started, hadd_n))
    folder = tempfile.mkdtemp()
    paths = [os.path.join(folder, "Batch%03d.root" % index) for index in range(1, 172)]
    open(paths[0], "wb").write(b"ok")
    open(paths[2], "wb").write(b"bad")

    def valid_name(path):
        return os.path.basename(path) == "Batch001.root"

    spec = classify_saved_batches(paths, valid_name)
    if(spec != "2-171"):
        raise SystemExit("a valid batch was included in the resume list: %s" % spec)
    if(classify_saved_batches([os.path.join(folder, "missing", "Batch001.root")], valid_name) is not None):
        raise SystemExit("a missing batch directory was classified")
    base = ["python", "submit.py", "-m", "hybrid", "-j3D", "30"]
    resumed = nominal_resume_command(base, spec)
    if(resumed[resumed.index("-bids") + 1] != "2-171"):
        raise SystemExit("resume did not pass the incomplete batch list")
    if("-bids" in nominal_resume_command(base, None)):
        raise SystemExit("an absent directory added -bids")
    if(nominal_resume_command(base, "") is not None):
        raise SystemExit("a complete batch set was submitted again")
    selected = pipeline.parse_batch_id_spec(spec, 171)
    array = pipeline.slurm_array_spec(selected, 171)
    if((1 in selected) or (array.split(",")[0] != "2") or ("1" in array.split(","))):
        raise SystemExit("the new SLURM array includes a valid batch")
    holder = type("Job", (), {})()
    holder.name = "Only_3D_demo"
    holder.name_in = ["*Final_Thesis_Files*.root"]
    holder.root = "SIDIS_epip_Response_Matrices_from_RDataFrames.root"
    holder.batch_ids = "2,3"
    holder.num_batches = 3
    holder.slurm_array_jobid = None
    holder.mode = "parallel"
    holder.campaign_worker_cap = None
    holder.campaign_worker_name = None
    holder.campaign_resource_mode = None
    holder.verbose = False
    work = tempfile.mkdtemp()
    valid_path = pipeline.expected_batch_root_path(holder, work, 2)
    invalid_path = pipeline.expected_batch_root_path(holder, work, 3)
    unlisted_path = pipeline.expected_batch_root_path(holder, work, 1)
    open(valid_path, "wb").write(b"ok")
    open(invalid_path, "wb").write(b"bad")
    open(unlisted_path, "wb").write(b"bad")
    original_valid = pipeline.batch_root_is_valid
    original_build = pipeline.build_main_command

    def fake_valid(path, piece):
        return path == valid_path

    class StopLaunch(Exception):
        pass

    def stop_launch(*args, **kwargs):
        raise StopLaunch()

    pipeline.batch_root_is_valid = fake_valid
    pipeline.build_main_command = stop_launch
    try:
        if(pipeline.start_job(holder, 1, work, work, False) is not None):
            raise SystemExit("an unlisted batch was opened")
        if(os.path.getsize(unlisted_path) == 0):
            raise SystemExit("an unlisted batch file was removed")
        if(pipeline.start_job(holder, 2, work, work, False) is not None):
            raise SystemExit("a valid listed batch was started")
        if(not os.path.isfile(valid_path)):
            raise SystemExit("a valid batch file was removed")
        launched = False
        try:
            pipeline.start_job(holder, 3, work, work, False)
        except StopLaunch:
            launched = True
        if(not launched):
            raise SystemExit("an invalid batch was not rewritten")
        if(os.path.isfile(invalid_path)):
            raise SystemExit("an invalid batch file was kept")
    finally:
        pipeline.batch_root_is_valid = original_valid
        pipeline.build_main_command = original_build
    calls = []
    original_run = pipeline.subprocess.run
    original_update = pipeline.Update_Email
    original_merge = pipeline.merge_ch4_count_files

    def fake_run(cmd, check=False):
        calls.append(list(cmd))
        class Result(object):
            returncode = 0
        return Result()

    pipeline.subprocess.run = fake_run
    pipeline.batch_root_is_valid = lambda path, piece: True
    pipeline.Update_Email = lambda *args, **kwargs: None
    pipeline.merge_ch4_count_files = lambda *args, **kwargs: None
    try:
        hadd_args = type("Hadd", (), {})()
        hadd_args.name = "Only_3D_demo"
        hadd_args.name_in = ["*Final_Thesis_Files*.root"]
        hadd_args.root = "SIDIS_epip_Response_Matrices_from_RDataFrames.root"
        hadd_args.work_dir = work
        hadd_args.batch_ids = "4,9"
        hadd_args.unfold_5D_only = False
        hadd_args.extra = []
        hadd_args.no_make_2D = True
        hadd_args.no_unfold_5D = True
        hadd_args.z_axis_2D = ""
        hadd_args.email = False
        hadd_args.email_message = ""
        hadd_args.verbose = False
        hadd_args.campaign_worker_name = ""

        class Clock(object):
            def time_elapsed(self, return_Q=True):
                return ["0s"]

        hadd_args.timer = Clock()
        pipeline.hadd_response_batches(hadd_args, work, 171)
    finally:
        pipeline.subprocess.run = original_run
        pipeline.batch_root_is_valid = original_valid
        pipeline.Update_Email = original_update
        pipeline.merge_ch4_count_files = original_merge
    if((len(calls) != 1) or (len(calls[0]) != 174)):
        raise SystemExit("hadd did not keep all 171 batches: %s" % (len(calls[0]) if(calls) else 0))
    names = [os.path.basename(path) for path in calls[0][3:]]
    if((not names[0].endswith("Batch001.root")) or (not names[1].endswith("Batch002.root")) or (not names[-1].endswith("Batch171.root"))):
        raise SystemExit("hadd dropped a batch outside the resume list")
    manifest = {
        "nominal_only": True,
        "phase1": [
            {"id": "nominal_only_20261030", "status": "running", "pid": 99999999, "nominal_only": True, "response": os.path.join(work, "missing_all.root"), "cut": "cut_Complete_SIDIS", "reason": "old"},
            {"id": "pipS6o", "status": "running", "pid": 99999999, "nominal_only": False, "response": os.path.join(work, "missing_pip.root"), "cut": "cut_Complete_SIDIS_pipS6o", "reason": ""},
        ],
        "phase2": [
            {"key": "nominal_only_20261030__inherited__AccSpline", "status": "waiting_phase1", "final": os.path.join(work, "missing_final.root"), "reason": ""},
        ],
    }
    runner.reconcile_existing(manifest)
    nominal = manifest["phase1"][0]
    if((nominal["status"] != "planned") or (nominal["pid"] is not None) or ("stopped before" not in nominal["reason"])):
        raise SystemExit("a dead nominal coordinator was not returned to planned")
    if(manifest["phase1"][1]["status"] != "failed"):
        raise SystemExit("a non-nominal dead Phase 1 row was not failed")
    if(manifest["phase2"][0]["status"] != "waiting_phase1"):
        raise SystemExit("nominal Phase 2 was failed after the coordinator stopped")
    nominal["status"] = "running"
    nominal["pid"] = os.getpid()
    runner.reconcile_existing(manifest)
    if((nominal["status"] != "running") or (manifest["phase2"][0]["status"] != "waiting_phase1")):
        raise SystemExit("a live nominal coordinator was reset")
    row = {"id": "nominal_only_20261030", "nominal_only": True, "command": ["python", "submit.py", "-m", "hybrid", "-j3D", "30"], "response": os.path.join(work, "missing_all.root")}
    live = {"resume_saved_batches": True, "data_root": "work_b", "nominal_only": True}
    launched = []

    class Proc(object):
        pid = 4321

    original_popen = runner.subprocess.Popen
    original_spec = runner.nominal_saved_batch_spec

    def fake_popen(cmd):
        launched.append(list(cmd))
        return Proc()

    def fake_spec(data_root):
        return "2-171"

    runner.subprocess.Popen = fake_popen
    runner.nominal_saved_batch_spec = fake_spec
    try:
        runner.start_phase1(live, row, False, work)
    finally:
        runner.subprocess.Popen = original_popen
        runner.nominal_saved_batch_spec = original_spec
    if((launched[0][launched[0].index("-bids") + 1] != "2-171") or ("-j3D" not in launched[0])):
        raise SystemExit("resume did not submit only the incomplete batches")
    bytes_campaign = "systematics_plc_resume_bytes"
    plan_argv = ["-n", "-c", bytes_campaign, "-droot", "work_b", "-wm", "both", "-nmo", "-suo", "-mlw", "30", "-plc", "30"]
    if(runner.main(plan_argv) != 0):
        raise SystemExit("concurrency manifest plan failed")
    saved_manifest = runner.last_manifest
    camp = runner.campaign_directory("work_b", bytes_campaign)
    runner.write_manifest(camp, saved_manifest)
    manifest_path = runner.manifest_path(camp)
    before = open(manifest_path, "rb").read()
    called = {"n": 0}

    def boom(data_root):
        called["n"] += 1
        raise SystemExit("dry-run classified the batch directory")

    runner.nominal_saved_batch_spec = boom
    try:
        code = runner.main(["-n", "-rs"] + plan_argv[1:])
    finally:
        runner.nominal_saved_batch_spec = original_spec
    if((code != 0) or (called["n"] != 0) or (open(manifest_path, "rb").read() != before)):
        raise SystemExit("nominal -n -rs changed the manifest or scanned batches")
    if("-j3D 30" not in runner.command_text(runner.last_manifest["phase1"][0]["command"])):
        raise SystemExit("resume dry-run dropped the local concurrency")
    if(len(runner.last_manifest["phase2"]) != 11):
        raise SystemExit("resume dry-run changed the 11 Phase 2 branches")


def main():
    self_test()
    ledger_self_test()
    squeue_compact_is_pending()
    hpp_matches_submit_full()
    dry_run_leaves_manifest_bytes()
    recovery_static_checks()
    followup_recovery_20261029()
    complete_campaign_20261029()
    phase2_spline_nosmear_dry_run()
    array_script_paths()
    nominal_and_5d_dry_run()
    pips6o_batch111_dry_run()
    nominal_local_concurrency()
    print("systematics campaign self-test ok")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
