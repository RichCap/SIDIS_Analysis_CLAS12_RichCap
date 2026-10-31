#!/usr/bin/env python3
# One entry point for the 34+7 SIDIS 3D systematic campaign.
# --dry_run prints commands. It does not write the manifest, scan batches, or submit work.
import argparse
import os
import subprocess
import sys
import time

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.systematics_campaign import (
    COMPLETE_LINEAGE_COUNT, DEFAULT_CUT, EMAIL_TO, LOCAL_DELAY_S, NOMINAL_ONLY_ID, Q2Y_BINS, USED_CAMPAIGN_IDS, append_log, append_submission_history,
    bin_root, branch_settings, build_manifest, campaign_directory, command_text, file_nonempty, job_stem, load_recovery_batches,
    classify_saved_batches, dedicated_5d_command, manifest_path, nominal_batch_file_valid,
    nominal_complete_command, nominal_only_command, nominal_resume_command, only_5d_spline_command,
    pips6o_batch111_command, remove_named_batch_file,
    output_counts, phase1_command, phase2_history_record, read_manifest,
    final_is_ready, part_is_ready, recovery_failure_text, recovery_phase1_command, regen_command, response_matrix_ready,
    root_key_names, sbatch_script, submission_ids_for_config, systematic_batch_paths, unfold_bin_ok, unfold_command,
    unfold_final_ok, worker_cap, write_manifest, written_output_path,
)
from Campaign.systematics_worker_ledger import bind_worker, pid_alive, release, try_acquire

SUBMIT_SCRIPT = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Submit_Full_Histogram_Creation_Pipeline.py")
UNFOLD_SCRIPT = os.path.join(_BOOT, "run_Simple_Unfold.py")
DEDICATED_5D_SCRIPT = os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py")
BIN_SCRIPT = os.path.join(_BOOT, "Simple_RooUnfold_SelfContained.py")
DATAFRAMES_DIR = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
WAIT_POLL_S = 60
last_manifest = None


def unfold_program(branch):
    if(branch == "BinByBin"):
        return BIN_SCRIPT
    return UNFOLD_SCRIPT


def bin_method(branch):
    if(branch == "BinByBin"):
        return "Bin"
    return None


def response_ok(path):
    if(not file_nonempty(path)):
        return False
    try:
        names = root_key_names(path)
    except Exception:
        return False
    return (names is not None) and (len(names) > 0)


def send_mail(enabled, subject, body):
    if(not enabled):
        return
    try:
        subprocess.run(["mail", "-s", subject, EMAIL_TO], input=body.encode(), check=False)
    except Exception as exc:
        print("mail was not sent: %s" % exc)


def slurm_helpers():
    if(DATAFRAMES_DIR not in sys.path):
        sys.path.insert(0, DATAFRAMES_DIR)
    import run_sidis_DataFrame_pipeline as pipeline
    return pipeline.query_slurm_array_task_state, pipeline.cancel_slurm_array_task


def fill_commands(manifest, python):
    for row in manifest["phase1"]:
        config = {"id": row["id"], "cut": row["cut"], "unsmeared": row["unsmeared"], "nominal": row["nominal"], "nominal_complete": row.get("nominal_complete")}
        if(row.get("nominal_only")):
            row["command"] = nominal_only_command(
                python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"], row["hpp_nospline"], row["hpp_spline"],
                manifest["max_local_workers"], manifest.get("phase1_local_jobs", 1),
            )
            continue
        if(row.get("pips6o_batch111")):
            row["command"] = pips6o_batch111_command(
                python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"], row["hpp_nospline"], row["hpp_spline"],
            )
            continue
        if(row.get("only_5d")):
            row["command"] = only_5d_spline_command(
                python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"], row["hpp_nospline"], row["hpp_spline"],
            )
            continue
        if(row.get("nominal_complete")):
            row["command"] = nominal_complete_command(
                python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"], row["hpp_nospline"], row["hpp_spline"],
            )
            continue
        if(manifest.get("recovery")):
            if(row.get("batch_ids") in [None, ""]):
                row["command"] = []
            else:
                row["command"] = recovery_phase1_command(
                    python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"], config,
                    row["hpp_nospline"], row["hpp_spline"], row["batch_ids"], manifest["hybrid_date"],
                    manifest["slurm_time"], manifest["only3d_slurm_mem"], row.get("defer_merge", False),
                )
        else:
            row["command"] = phase1_command(
                python, SUBMIT_SCRIPT, manifest["data_root"], manifest["campaign"],
                manifest["max_local_workers"], config, row["hpp_nospline"], row["hpp_spline"],
            )


def print_plan(manifest, regen_cmd):
    single = manifest.get("recovery") or manifest.get("nominal_only") or manifest.get("only_5d") or manifest.get("pips6o_batch111")
    if(single):
        arrays = len(manifest["phase2"])
        tasks = 0
        for row in manifest["phase2"]:
            tasks += 1 if(row.get("local_5d")) else len(Q2Y_BINS)
        files = arrays
    else:
        arrays, tasks, files = output_counts(manifest["weight_mode"])
    print("dry-run only: no sbatch, no histogram process, no unfold process")
    print("campaign %s  weight_mode %s  local_workers %s" % (manifest["campaign"], manifest["weight_mode"], manifest["max_local_workers"]))
    print("phase1 configurations %s" % len(manifest["phase1"]))
    if(manifest.get("recovery")):
        print("recovery tasks %s" % manifest.get("recovery_task_count"))
    print("phase2 arrays %s  tasks %s  final files %s" % (arrays, tasks, files))
    if(regen_cmd is not None):
        print("HPP regen (nominal waits; others do not):")
        print(command_text(regen_cmd))
    for row in manifest["phase1"]:
        print("PHASE1 %s %s" % (row["id"], row["status"]))
        print("  hpp_nospline %s" % row["hpp_nospline"])
        print("  hpp_spline %s" % row["hpp_spline"])
        print("  response %s" % row["response"])
        if(row.get("nominal_only")):
            print("  hybrid SLURM plus local pending batches; then Phase 2")
            print("  %s" % command_text(row["command"]))
        elif(row.get("pips6o_batch111")):
            print("  local batch 111 only; then the existing merge and Phase 2")
            print("  replace %s" % row.get("replace_one_batch"))
            print("  %s" % command_text(row["command"]))
        elif(row.get("only_5d")):
            print("  hadd after all 171 batch files validate; then Phase 2")
            print("  %s" % command_text(row["command"]))
        elif(row.get("nominal_complete")):
            print("  full nominal histograms; then Phase 2")
            print("  %s" % command_text(row["command"]))
        elif(row.get("batch_ids") in [None, ""]):
            if(row.get("external_merge")):
                print("  wait for external merge; then Phase 2")
            else:
                print("  skip histograms; verify merged response; then Phase 2")
        elif(row.get("auto_merge")):
            print("  hadd after all 171 batch files validate")
            print("  %s" % command_text(row["command"]))
        elif(row.get("defer_merge")):
            print("  hadd deferred")
            print("  %s" % command_text(row["command"]))
        else:
            print("  hadd after listed batches")
            print("  %s" % command_text(row["command"]))
    camp = campaign_directory(manifest["data_root"], manifest["campaign"])
    logs = os.path.join(camp, "slurm_logs")
    for row in manifest["phase2"]:
        if(row.get("status") == "deferred"):
            print("PHASE2 %s deferred" % row["key"])
            continue
        if(row.get("local_5d")):
            sample = dedicated_5d_command(sys.executable, DEDICATED_5D_SCRIPT, manifest["data_root"], row["response"], row["launch_root"])
            print("PHASE2 %s lineage %s" % (row["key"], row["lineage"]))
            print("  starts after phase1 success")
            print("  final %s" % row["final"])
            print("  %s" % command_text(sample))
            continue
        settings = branch_settings(row["branch"], 1, row["weight_tag"])
        settings["unsmeared"] = bool(row.get("unsmeared"))
        sample = unfold_command(sys.executable, unfold_program(row["branch"]), manifest["data_root"], row["response"], row["bins"]["1"]["root"], 1, settings)
        print("PHASE2 %s lineage %s" % (row["key"], row["lineage"]))
        print("  final %s" % row["final"])
        print("  bin1 %s" % command_text(sample))
        script = sbatch_script(job_stem(row), logs, sys.executable, unfold_program(row["branch"]), manifest["data_root"], row["response"], os.path.dirname(row["bins"]["1"]["root"]), job_stem(row), row["branch"], row["weight_tag"], row.get("unsmeared"))
        print("  sbatch %s" % script.splitlines()[3])
    print("manifest %s" % manifest_path(camp))
    sys.stdout.flush()


def reconcile_existing(manifest):
    for row in manifest["phase1"]:
        if((row["status"] == "running") and (not pid_alive(row.get("pid")))):
            if(response_matrix_ready(row["response"], row["cut"])):
                row["status"] = "success"
                row["reason"] = ""
            elif(row.get("nominal_only")):
                # The coordinator stopped before _All.root was ready. Phase 2 stays waiting_phase1.
                row["status"] = "planned"
                row["pid"] = None
                row["reason"] = "coordinator stopped before the merged response was ready"
            else:
                row["status"] = "failed"
                row["reason"] = row.get("reason") or "phase1 process ended without a response file"
        elif((row["status"] == "success") and (not response_matrix_ready(row["response"], row["cut"]))):
            row["status"] = "failed"
            row["reason"] = "recorded success has no valid response file"
    for row in manifest["phase2"]:
        if((row["status"] == "success") and (not unfold_final_ok(row["final"]))):
            row["status"] = "failed"
            row["reason"] = "recorded success has no complete unfolded file"


def settle_saved_phase1(manifest, row, enabled_mail, camp):
    # Empty batch list: do not submit or merge histograms.
    ready = response_matrix_ready(row["response"], row["cut"])
    if(row.get("external_merge")):
        size = os.path.getsize(row["response"]) if(file_nonempty(row["response"])) else 0
        row["status"] = "waiting_merge"
        row["reason"] = "waiting for the external merge"
        row["confirm_ready"] = ready
        row["confirm_size"] = size
        row["next_check_at"] = time.time() + WAIT_POLL_S
        append_log(camp, "phase1", row["id"], "", "", "", "saved", "", "waiting", row["reason"], row["response"])
        return
    if(ready):
        row["status"] = "success"
        row["reason"] = ""
        append_log(camp, "phase1", row["id"], "", "", "", "saved", "", "success", "", row["response"])
        return
    row["status"] = "failed"
    if(file_nonempty(row["response"])):
        row["reason"] = "merged response failed the object check"
    else:
        row["reason"] = "merged response is missing"
    append_log(camp, "phase1", row["id"], "", "", "", "saved", "", "failed", row["reason"], row["response"])
    body = row["reason"] + "\n"
    if(manifest.get("recovery")):
        body = recovery_failure_text(manifest["campaign"], row["id"], row.get("batch_ids") or "", submission_ids_for_config(camp, row["id"]), row["reason"])
    send_mail(enabled_mail, "SIDIS systematics Phase 1 failed %s" % row["id"], body)


def phase1_needs_start(row):
    if(row["status"] in ["success", "waiting_merge", "waiting_batches", "merging", "deferred"]):
        return False
    if((row["status"] == "running") and pid_alive(row.get("pid"))):
        return False
    return True


def nominal_saved_batch_spec(data_root):
    # Read-only classification of the existing 10_30_2026 directory. Dry-run does not call this.
    paths = systematic_batch_paths(NOMINAL_ONLY_ID, DEFAULT_CUT, "10_30_2026", batch_name="Sys3D_%s" % NOMINAL_ONLY_ID)
    return classify_saved_batches(paths, nominal_batch_file_valid)


def nominal_merge_only_command(python, data_root):
    # No array. The child merges the 171 batch files that are already valid.
    code = "from Campaign.systematics_campaign import hadd_complete_nominal_batches; raise SystemExit(hadd_complete_nominal_batches(%r))" % data_root
    return [python, "-c", code]


def start_phase1(manifest, row, enabled_mail, camp):
    remove_named_batch_file(row.get("replace_one_batch"))
    command = list(row["command"])
    if(row.get("nominal_only") and manifest.get("resume_saved_batches")):
        spec = nominal_saved_batch_spec(manifest["data_root"])
        resumed = nominal_resume_command(command, spec)
        if(resumed is None):
            command = nominal_merge_only_command(sys.executable, manifest["data_root"])
        else:
            command = resumed
        row["command"] = command
    proc = subprocess.Popen(command)
    row["pid"] = proc.pid
    row["status"] = "running"
    row["reason"] = ""
    append_log(camp, "phase1", row["id"], "", "", "", "local", "", "started", "", row["response"])
    send_mail(enabled_mail, "SIDIS systematics started %s" % row["id"], "Phase 1 started for %s\n%s\n" % (row["id"], row["response"]))
    return proc


def submit_sbatch(script_path):
    proc = subprocess.run(["sbatch", "--parsable", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if(proc.returncode != 0):
        message = (proc.stderr or proc.stdout or "sbatch failed").strip()
        return "", message
    text = (proc.stdout or "").strip().split(";")[0].strip()
    return text, ""


def bin_written_path(row, q2y):
    return written_output_path(row["bins"][str(q2y)]["root"], row["weight_tag"])


def bin_output_ready(row, q2y):
    written = bin_written_path(row, q2y)
    if(row["branch"] == "BinByBin"):
        return unfold_bin_ok(row["bins"][str(q2y)]["root"], q2y, "Bin"), row["bins"][str(q2y)]["root"]
    ready = part_is_ready(written, q2y, row["weight_tag"], row["response"], row.get("unsmeared"))
    return ready, written


def missing_part_bins(row):
    missing = []
    for q2y in Q2Y_BINS:
        ready, written = bin_output_ready(row, q2y)
        row["bins"][str(q2y)]["written"] = written
        if(ready):
            row["bins"][str(q2y)]["status"] = "success"
            row["bins"][str(q2y)]["where"] = "reused"
        else:
            missing.append(int(q2y))
    return missing


def write_sbatch(camp, manifest, row, array_spec="1-17"):
    logs = os.path.join(camp, "slurm_logs")
    parts = os.path.dirname(row["bins"]["1"]["root"])
    os.makedirs(logs, exist_ok=True)
    os.makedirs(parts, exist_ok=True)
    path = os.path.join(camp, "sbatch", job_stem(row) + ".sh")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = sbatch_script(
        job_stem(row), logs, sys.executable, unfold_program(row["branch"]), manifest["data_root"],
        row["response"], parts, job_stem(row), row["branch"], row["weight_tag"], row.get("unsmeared"), array_spec,
    )
    handle = open(path, "w")
    handle.write(text)
    handle.close()
    os.chmod(path, 0o755)
    return path


def bin_needs_work(slot):
    return slot.get("status") not in ["success", "failed"]


def lineage_busy(running, lineage):
    return lineage in running


def first_pending_bin(row, query_state, now):
    if(row.get("array_id") in [None, ""]):
        return None
    if(row.get("submit_time") in [None, ""]):
        return None
    if((now - float(row["submit_time"])) < LOCAL_DELAY_S):
        return None
    for q2y in Q2Y_BINS:
        slot = row["bins"][str(q2y)]
        if(not bin_needs_work(slot)):
            continue
        ready, written = bin_output_ready(row, q2y)
        if(ready):
            slot["written"] = written
            slot["status"] = "success"
            slot["where"] = slot.get("where") or "slurm"
            continue
        if(row.get("array_id") == "reused"):
            continue
        state = query_state(row["array_id"], q2y)
        slot["slurm_state"] = "" if(state in [None]) else str(state)
        if(state == "PD"):
            return q2y
    return None


def choose_local(rows, running, query_state, now):
    by_lineage = {}
    for row in rows:
        if(row.get("local_5d")):
            continue
        if(row["status"] in ["success", "failed", "waiting_phase1", "deferred"]):
            continue
        by_lineage.setdefault(row["lineage"], []).append(row)
    for lineage, group in by_lineage.items():
        if(lineage_busy(running, lineage)):
            continue
        ordered = sorted(group, key=lambda item: item.get("local_order", 0))
        for row in ordered:
            if(row.get("submit_time") in [None, ""]):
                break
            if((now - float(row["submit_time"])) < LOCAL_DELAY_S):
                break
            q2y = first_pending_bin(row, query_state, now)
            if(q2y is not None):
                return row, q2y
    return None, None


def launch_local(manifest, camp, row, q2y, cap):
    ok, token = try_acquire(manifest["data_root"], manifest["campaign"], cap, "unfold", row["key"])
    if(not ok):
        return None
    return token


def confirm_external_merge(row, camp):
    path = row["response"]
    size = os.path.getsize(path) if(file_nonempty(path)) else 0
    ready = response_matrix_ready(path, row["cut"]) if(size > 0) else False
    previous_size = row.get("confirm_size")
    previous_ready = bool(row.get("confirm_ready"))
    row["confirm_size"] = size
    row["confirm_ready"] = ready
    # A size plateau while the object check fails stays pending. Two passing reads at the same size are required.
    if(ready and previous_ready and (previous_size == size) and (size > 0)):
        row["status"] = "success"
        row["reason"] = ""
        append_log(camp, "phase1", row["id"], "", "", "", "saved", "", "success", "", path)
        return True
    row["status"] = "waiting_merge"
    row["reason"] = "waiting for the external merge"
    return False


def batch_files_signature(row, hybrid_date):
    if(DATAFRAMES_DIR not in sys.path):
        sys.path.insert(0, DATAFRAMES_DIR)
    import run_sidis_DataFrame_pipeline as pipeline
    paths = systematic_batch_paths(row["id"], row["cut"], hybrid_date, batch_name=row.get("batch_name"), product_key=row.get("product_key") or "Only_3D")
    sizes = []
    for path in paths:
        if(not pipeline.batch_root_is_valid(path, "MultiDim")):
            return None, paths
        sizes.append(os.path.getsize(path))
    return sizes, paths


def confirm_batch_merge(row, camp, merge_procs, hybrid_date):
    path = row["response"]
    size = os.path.getsize(path) if(file_nonempty(path)) else 0
    if((size > 0) and response_matrix_ready(path, row["cut"])):
        if(bool(row.get("confirm_ready")) and (row.get("confirm_size") == size)):
            row["status"] = "success"
            row["reason"] = ""
            append_log(camp, "phase1", row["id"], "", "", "", "saved", "", "success", "", path)
            return True
        row["confirm_ready"] = True
        row["confirm_size"] = size
        row["reason"] = "confirming the merged response"
        return False
    row["confirm_ready"] = False
    sizes, paths = batch_files_signature(row, hybrid_date)
    previous = row.get("confirm_batch_sizes")
    row["confirm_batch_sizes"] = sizes
    if((sizes is None) or (previous != sizes)):
        row["reason"] = "waiting until all 171 batch files are valid"
        return False
    tmp = path + ".campaign_hadd_tmp.root"
    if(os.path.exists(tmp)):
        os.remove(tmp)
    parent = os.path.dirname(path)
    if(parent not in ["", None]):
        os.makedirs(parent, exist_ok=True)
    proc = subprocess.Popen(["hadd", "-f", tmp] + paths)
    merge_procs[row["id"]] = proc
    row["status"] = "merging"
    row["hadd_tmp"] = tmp
    row["reason"] = "merging 171 batch files"
    append_log(camp, "phase1", row["id"], "", "", "", "local", "", "merging", row["reason"], path)
    return False


def finish_merge_process(row, proc, camp):
    rc = proc.poll()
    if(rc is None):
        return False
    tmp = row.get("hadd_tmp") or (row["response"] + ".campaign_hadd_tmp.root")
    if(rc == 0):
        os.replace(tmp, row["response"])
        if(response_matrix_ready(row["response"], row["cut"])):
            row["status"] = "success"
            row["reason"] = ""
            append_log(camp, "phase1", row["id"], "", "", "", "local", "", "success", "", row["response"])
            return True
        row["status"] = "failed"
        row["reason"] = "merged response failed the object check"
    else:
        row["status"] = "failed"
        row["reason"] = "hadd failed"
        if(os.path.exists(tmp)):
            os.remove(tmp)
    append_log(camp, "phase1", row["id"], "", "", "", "local", "", "failed", row["reason"], row["response"])
    return True


def advance_waits(manifest, camp, merge_procs, now):
    finished = []
    for row in manifest["phase1"]:
        if(row["status"] == "merging"):
            proc = merge_procs.get(row["id"])
            if(proc is None):
                row["status"] = "failed"
                row["reason"] = "hadd process was lost"
                append_log(camp, "phase1", row["id"], "", "", "", "local", "", "failed", row["reason"], row["response"])
                continue
            if(finish_merge_process(row, proc, camp)):
                finished.append(row["id"])
            continue
        if(row["status"] not in ["waiting_merge", "waiting_batches"]):
            continue
        if(now < float(row.get("next_check_at") or 0)):
            continue
        row["next_check_at"] = now + WAIT_POLL_S
        if(row["status"] == "waiting_merge"):
            if(confirm_external_merge(row, camp)):
                send_mail(manifest.get("email"), "SIDIS systematics Phase 1 success %s" % row["id"], row["response"] + "\n")
        else:
            confirm_batch_merge(row, camp, merge_procs, manifest.get("hybrid_date") or "10_27_2026")
    for config_id in finished:
        if(config_id in merge_procs):
            del merge_procs[config_id]
        row = [item for item in manifest["phase1"] if(item["id"] == config_id)][0]
        if(row["status"] == "success"):
            send_mail(manifest.get("email"), "SIDIS systematics Phase 1 success %s" % row["id"], row["response"] + "\n")
        elif(row["status"] == "failed"):
            send_mail(manifest.get("email"), "SIDIS systematics Phase 1 failed %s" % row["id"], row["reason"] + "\n")


def run_live(args, manifest):
    camp = campaign_directory(args.data_root, args.campaign)
    os.makedirs(os.path.join(camp, "unfolded"), exist_ok=True)
    os.makedirs(os.path.join(camp, "final"), exist_ok=True)
    manifest["email"] = bool(args.email)
    reconcile_existing(manifest)
    if(args.resume and manifest.get("nominal_only")):
        manifest["resume_saved_batches"] = True
    fill_commands(manifest, sys.executable)
    write_manifest(camp, manifest)
    query_state, cancel_task = slurm_helpers()
    procs = {}
    regen_proc = None
    nominal = None
    for row in manifest["phase1"]:
        if(row["nominal"]):
            nominal = row
    regen_out = nominal["hpp_spline"] if((args.regenerate_nominal_spline_hpp) and (nominal is not None)) else ""
    if((regen_out not in [None, ""]) and phase1_needs_start(nominal) and (not file_nonempty(regen_out))):
        regen_cmd = regen_command(sys.executable, SUBMIT_SCRIPT, args.data_root, regen_out)
        append_log(camp, "hpp", "nominal", "", "AccSpline", "", "local", "", "started", "", regen_out)
        regen_proc = subprocess.Popen(regen_cmd)
    for row in manifest["phase1"]:
        if(row["nominal"] and (regen_proc is not None)):
            continue
        if(not phase1_needs_start(row)):
            continue
        if(manifest.get("recovery") and (row.get("batch_ids") in [None, ""]) and (not row.get("nominal_complete"))):
            settle_saved_phase1(manifest, row, args.email, camp)
            continue
        procs[row["id"]] = start_phase1(manifest, row, args.email, camp)
    write_manifest(camp, manifest)
    compiled = False
    compile_failed = False
    running_local = {}
    five_d_running = {}
    merge_procs = {}
    while(True):
        if(regen_proc is not None):
            regen_rc = regen_proc.poll()
            if(regen_rc is not None):
                if((regen_rc == 0) and file_nonempty(regen_out)):
                    append_log(camp, "hpp", "nominal", "", "AccSpline", "", "local", "", "success", "", regen_out)
                    if(phase1_needs_start(nominal)):
                        procs[nominal["id"]] = start_phase1(manifest, nominal, args.email, camp)
                else:
                    nominal["status"] = "failed"
                    nominal["reason"] = "nominal spline HPP regeneration failed"
                    append_log(camp, "hpp", "nominal", "", "AccSpline", "", "local", "", "failed", nominal["reason"], regen_out)
                    send_mail(args.email, "SIDIS systematics failed nominal", nominal["reason"] + "\n")
                regen_proc = None
                write_manifest(camp, manifest)
        finished = []
        for config_id, proc in procs.items():
            rc = proc.poll()
            if(rc is None):
                continue
            finished.append(config_id)
            row = [item for item in manifest["phase1"] if(item["id"] == config_id)][0]
            if(row.get("auto_merge") and (rc == 0)):
                row["status"] = "waiting_batches"
                row["reason"] = "waiting until all 171 batch files are valid"
                row["next_check_at"] = 0
                append_log(camp, "phase1", row["id"], "", "", "", "slurm", "", "waiting", row["reason"], row["response"])
            elif(row.get("defer_merge") and (rc == 0)):
                row["status"] = "deferred"
                row["reason"] = "histogram array submitted; merge deferred"
                append_log(camp, "phase1", row["id"], "", "", "", "slurm", "", "deferred", row["reason"], row["response"])
            elif((rc == 0) and response_matrix_ready(row["response"], row["cut"])):
                row["status"] = "success"
                row["reason"] = ""
                append_log(camp, "phase1", row["id"], "", "", "", "local", "", "success", "", row["response"])
                send_mail(args.email, "SIDIS systematics Phase 1 success %s" % row["id"], row["response"] + "\n")
            else:
                row["status"] = "failed"
                if(rc == 0):
                    row["reason"] = "merged response failed the object check"
                else:
                    row["reason"] = "histogram pipeline exited %s" % rc
                append_log(camp, "phase1", row["id"], "", "", "", "local", "", "failed", row["reason"], row["response"])
                if(manifest.get("recovery")):
                    body = recovery_failure_text(manifest["campaign"], row["id"], row.get("batch_ids") or "", submission_ids_for_config(camp, row["id"]), row["reason"])
                else:
                    body = row["reason"] + "\n"
                send_mail(args.email, "SIDIS systematics Phase 1 failed %s" % row["id"], body)
        for config_id in finished:
            del procs[config_id]
        finished_5d = []
        for five_key, five_proc in five_d_running.items():
            five_rc = five_proc.poll()
            if(five_rc is None):
                continue
            finished_5d.append(five_key)
            five_row = [item for item in manifest["phase2"] if(item["key"] == five_key)][0]
            if((five_rc == 0) and file_nonempty(five_row["final"])):
                five_row["status"] = "success"
                five_row["reason"] = ""
                append_log(camp, "phase2", five_row["config_id"], five_row["branch"], five_row["weight_label"], "", "local", "", "success", "", five_row["final"])
                send_mail(args.email, "SIDIS systematics Phase 2 success %s" % five_row["key"], five_row["final"] + "\n")
            else:
                five_row["status"] = "failed"
                five_row["reason"] = "5D unfold exited %s" % five_rc
                append_log(camp, "phase2", five_row["config_id"], five_row["branch"], five_row["weight_label"], "", "local", "", "failed", five_row["reason"], five_row["final"])
                send_mail(args.email, "SIDIS systematics Phase 2 failed %s" % five_row["key"], five_row["reason"] + "\n")
        for five_key in finished_5d:
            del five_d_running[five_key]
        needs_simple = any(not item.get("local_5d") for item in manifest["phase2"])
        if((not compiled) and needs_simple and any(row["status"] == "success" for row in manifest["phase1"])):
            compile_rc = subprocess.run([sys.executable, UNFOLD_SCRIPT, "--compile_only"]).returncode
            compiled = compile_rc == 0
            compile_failed = not compiled
            if(compile_failed):
                append_log(camp, "phase2", "", "", "", "", "local", "", "failed", "Simple_Unfold compile failed", "")
        for row in manifest["phase2"]:
            parent = [item for item in manifest["phase1"] if(item["id"] == row["config_id"])][0]
            if(row.get("local_5d")):
                if(parent["status"] != "success"):
                    continue
                if(row["status"] in ["success", "failed", "running"]):
                    continue
                if(row["key"] in five_d_running):
                    continue
                launch_dir = os.path.dirname(row["launch_root"])
                if(launch_dir not in ["", None]):
                    os.makedirs(launch_dir, exist_ok=True)
                command = dedicated_5d_command(sys.executable, DEDICATED_5D_SCRIPT, manifest["data_root"], row["response"], row["launch_root"])
                five_proc = subprocess.Popen(command)
                row["pid"] = five_proc.pid
                row["status"] = "running"
                row["reason"] = ""
                five_d_running[row["key"]] = five_proc
                append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "local", "", "started", "", row["final"])
                send_mail(args.email, "SIDIS systematics Phase 2 started %s" % row["key"], command_text(command) + "\n")
                continue
            if(parent["status"] != "success"):
                continue
            if(row["status"] in ["success", "failed", "deferred"]):
                continue
            if(compile_failed):
                row["status"] = "failed"
                row["reason"] = "Simple_Unfold compile failed"
                continue
            if(not compiled):
                continue
            if(row.get("array_id") not in [None, ""]):
                row["status"] = "submitted"
                continue
            if(final_is_ready(row["final"], row["response"], row.get("unsmeared"))):
                row["status"] = "success"
                row["reason"] = "existing final kept"
                append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "saved", "", "success", row["reason"], row["final"])
                continue
            missing = missing_part_bins(row)
            if(len(missing) == 0):
                row["array_id"] = "reused"
                row["submit_time"] = time.time()
                row["status"] = "submitted"
                append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "saved", "reused", "submitted", "all part files already valid", row["final"])
                continue
            script_path = write_sbatch(camp, manifest, row, ",".join([str(index) for index in missing]))
            array_id, message = submit_sbatch(script_path)
            if(array_id in [None, ""]):
                row["status"] = "failed"
                row["reason"] = message
                append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "slurm", "", "failed", message, "")
                continue
            row["array_id"] = array_id
            row["submit_time"] = time.time()
            row["status"] = "submitted"
            append_submission_history(camp, phase2_history_record(manifest, row, array_id))
            append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "slurm", array_id, "submitted", "", row["final"])
            send_mail(args.email, "SIDIS systematics Phase 2 started %s" % row["key"], "array %s\n%s\n" % (array_id, row["final"]))
        done_local = []
        for lineage, slot in running_local.items():
            rc = slot["proc"].poll()
            if(rc is None):
                continue
            done_local.append(lineage)
            release(manifest["data_root"], manifest["campaign"], slot["token"])
            q2y = slot["q2y"]
            bin_slot = slot["row"]["bins"][str(q2y)]
            if((rc == 0) and unfold_bin_ok(bin_slot["root"], q2y, bin_method(slot["row"]["branch"]))):
                bin_slot["status"] = "success"
                bin_slot["where"] = "local"
                append_log(camp, "phase2", slot["row"]["config_id"], slot["row"]["branch"], slot["row"]["weight_label"], q2y, "local", slot["row"].get("array_id"), "success", "", bin_slot["root"])
            else:
                bin_slot["status"] = "failed"
                bin_slot["where"] = "local"
                slot["row"]["status"] = "failed"
                slot["row"]["reason"] = "local unfold bin %s exited %s" % (q2y, rc)
                append_log(camp, "phase2", slot["row"]["config_id"], slot["row"]["branch"], slot["row"]["weight_label"], q2y, "local", slot["row"].get("array_id"), "failed", slot["row"]["reason"], bin_slot["root"])
        for lineage in done_local:
            del running_local[lineage]
        now = time.time()
        row, q2y = choose_local(manifest["phase2"], running_local, query_state, now)
        if((row is not None) and (q2y is not None)):
            state_now = query_state(row["array_id"], q2y)
            if(state_now == "PD"):
                token = launch_local(manifest, camp, row, q2y, args.max_local_workers)
                if(token not in [None, ""]):
                    state_again = query_state(row["array_id"], q2y)
                    if(state_again != "PD"):
                        release(manifest["data_root"], manifest["campaign"], token)
                    elif(not cancel_task(row["array_id"], q2y)):
                        release(manifest["data_root"], manifest["campaign"], token)
                        append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], q2y, "slurm", row["array_id"], "cancel_failed", "left on SLURM", "")
                    else:
                        settings = branch_settings(row["branch"], q2y, row["weight_tag"])
                        cmd = unfold_command(sys.executable, unfold_program(row["branch"]), args.data_root, row["response"], row["bins"][str(q2y)]["root"], q2y, settings)
                        log_handle = open(os.path.join(camp, "slurm_logs", "%s_q2y%02d.local.log" % (job_stem(row), q2y)), "w")
                        proc = subprocess.Popen(cmd, stdout=log_handle, stderr=subprocess.STDOUT)
                        bind_worker(manifest["data_root"], manifest["campaign"], token, proc.pid)
                        running_local[row["lineage"]] = {"proc": proc, "token": token, "row": row, "q2y": q2y}
                        append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], q2y, "local", row["array_id"], "started", "", row["bins"][str(q2y)]["root"])
        for row in manifest["phase2"]:
            if(row["status"] in ["success", "failed", "waiting_phase1", "deferred"]):
                continue
            if(row.get("array_id") in [None, ""]):
                continue
            pending = False
            failed_bin = False
            for q2y in Q2Y_BINS:
                slot = row["bins"][str(q2y)]
                if(slot["status"] == "failed"):
                    failed_bin = True
                    continue
                if(slot["status"] == "success"):
                    continue
                ready, written = bin_output_ready(row, q2y)
                if(ready):
                    slot["written"] = written
                    slot["status"] = "success"
                    slot["where"] = slot.get("where") or "slurm"
                    slot["missing_polls"] = 0
                    continue
                if(row.get("array_id") == "reused"):
                    pending = True
                    continue
                state = "" if(row.get("array_id") in [None, ""]) else query_state(row["array_id"], q2y)
                slot["slurm_state"] = "" if(state in [None]) else str(state)
                if(state in ["F", "CA", "TO", "NF", "OOM"]):
                    slot["status"] = "failed"
                    failed_bin = True
                    row["reason"] = "SLURM bin %s state %s" % (q2y, state)
                    continue
                waited = (row.get("submit_time") not in [None, ""]) and ((time.time() - float(row["submit_time"])) >= LOCAL_DELAY_S)
                if((state in [None, ""]) and waited):
                    slot["missing_polls"] = int(slot.get("missing_polls") or 0) + 1
                    if(slot["missing_polls"] >= 15):
                        slot["status"] = "failed"
                        failed_bin = True
                        row["reason"] = "Q2-y bin %s left the queue without an output file" % q2y
                        continue
                else:
                    slot["missing_polls"] = 0
                pending = True
            if(failed_bin):
                row["status"] = "failed"
                reason = row.get("reason") or "bin failed"
                if(manifest.get("recovery")):
                    parent = [item for item in manifest["phase1"] if(item["id"] == row["config_id"])][0]
                    body = recovery_failure_text(manifest["campaign"], row["config_id"], parent.get("batch_ids") or "", submission_ids_for_config(camp, row["config_id"]), reason)
                else:
                    body = reason
                send_mail(args.email, "SIDIS systematics Phase 2 failed %s" % row["key"], body)
            elif((not pending) and (row["lineage"] not in running_local)):
                if(final_is_ready(row["final"], row["response"], row.get("unsmeared"))):
                    row["status"] = "success"
                    row["reason"] = "existing final kept"
                    append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "saved", row.get("array_id"), "success", row["reason"], row["final"])
                    send_mail(args.email, "SIDIS systematics Phase 2 success %s" % row["key"], row["final"] + "\n")
                    continue
                if(merge_bins(row)):
                    if(unfold_final_ok(row["final"])):
                        row["status"] = "success"
                        append_log(camp, "phase2", row["config_id"], row["branch"], row["weight_label"], "", "local", row.get("array_id"), "success", "", row["final"])
                        send_mail(args.email, "SIDIS systematics Phase 2 success %s" % row["key"], row["final"] + "\n")
                    else:
                        row["status"] = "failed"
                        row["reason"] = "merged file failed validation"
                else:
                    row["status"] = "failed"
                    row["reason"] = "hadd failed"
        advance_waits(manifest, camp, merge_procs, time.time())
        write_manifest(camp, manifest)
        phase1_open = any(row["status"] in ["planned", "running", "waiting_merge", "waiting_batches", "merging"] for row in manifest["phase1"]) or (len(procs) > 0) or (regen_proc is not None) or (len(merge_procs) > 0)
        still = False
        for row in manifest["phase2"]:
            parent = [item for item in manifest["phase1"] if(item["id"] == row["config_id"])][0]
            if(row["status"] == "deferred"):
                continue
            if(parent["status"] in ["failed", "deferred"]):
                if((parent["status"] == "failed") and (row["status"] == "waiting_phase1")):
                    row["status"] = "failed"
                    row["reason"] = "phase1 failed"
                continue
            if(row["status"] not in ["success", "failed"]):
                still = True
        if((not phase1_open) and (not still) and (len(running_local) == 0)):
            break
        time.sleep(2)
    collect_finals(camp, manifest)
    write_manifest(camp, manifest)
    print("campaign log %s" % os.path.join(camp, "campaign.log"))
    print("final directory %s" % os.path.join(camp, "final"))


def phase1_parent_success(manifest, row):
    parent = [item for item in manifest["phase1"] if(item["id"] == row["config_id"])][0]
    return parent["status"] == "success"


def merge_bins(row):
    paths = []
    for q2y in Q2Y_BINS:
        slot = row["bins"][str(q2y)]
        paths.append(slot.get("written") or bin_written_path(row, q2y))
    final = row["final"]
    os.makedirs(os.path.dirname(final), exist_ok=True)
    tmp = final + ".hadd_tmp.root"
    if(os.path.exists(tmp)):
        os.remove(tmp)
    proc = subprocess.run(["hadd", "-f", tmp] + paths)
    if(proc.returncode != 0):
        return False
    os.replace(tmp, final)
    return True


def collect_finals(camp, manifest):
    final_dir = os.path.join(camp, "final")
    os.makedirs(final_dir, exist_ok=True)
    for row in manifest["phase2"]:
        if(row["status"] != "success"):
            continue
        if(not unfold_final_ok(row["final"])):
            continue
        dest = os.path.join(final_dir, os.path.basename(row["final"]))
        if(os.path.isfile(dest) and unfold_final_ok(dest)):
            row["collected"] = dest
            continue
        if(os.path.isfile(dest)):
            os.remove(dest)
        try:
            os.link(row["final"], dest)
        except OSError:
            import shutil
            shutil.copy2(row["final"], dest)
        row["collected"] = dest
        append_log(camp, "final", row["config_id"], row["branch"], row["weight_label"], "", "local", row.get("array_id"), "collected", "", dest)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run the two-phase SIDIS 3D systematic campaign. The default dry-run switch is off; pass --dry_run to print commands without submitting.")
    parser.add_argument("-c", "--campaign", default="systematics_3d")
    parser.add_argument("-droot", "--data_root", default="work_b")
    parser.add_argument("-wm", "--weight_mode", default="unweighted", choices=["unweighted", "weighted", "both"])
    parser.add_argument("-rnh", "--regenerate_nominal_spline_hpp", action="store_true")
    parser.add_argument("-mlw", "--max_local_workers", type=int, default=41)
    parser.add_argument("-n", "--dry_run", action="store_true")
    parser.add_argument("-rs", "--resume", action="store_true")
    parser.add_argument("-e", "--email", action="store_true")
    parser.add_argument("-ht", "--hpp_tag", default="Final_Thesis")
    parser.add_argument("-em", "--email_message", default="")
    parser.add_argument("-rb", "--recovery_batches", default=None)
    parser.add_argument("-incn", "--include_nominal", action="store_true")
    parser.add_argument("-suo", "--shared_unfold_output", action="store_true")
    parser.add_argument("-nmo", "--nominal_only", action="store_true")
    parser.add_argument("-plc", "--phase1_local_concurrency", type=int, default=None)
    parser.add_argument("-5ds", "--only_5d_spline", action="store_true")
    parser.add_argument("-p6b", "--pips6o_batch111", action="store_true")
    return parser.parse_args(argv)


def resolve_recovery_path(path):
    if(path in [None, ""]):
        return None
    if(os.path.isfile(path)):
        return path
    rooted = os.path.join(_BOOT, path)
    if(os.path.isfile(rooted)):
        return rooted
    raise ValueError("recovery batch file was not found: %s" % path)


def main(argv=None):
    global last_manifest
    last_manifest = None
    args = parse_args(sys.argv[1:] if(argv is None) else argv)
    if((args.campaign in USED_CAMPAIGN_IDS) and (not args.dry_run)):
        print("campaign id %s has already been used; choose a new id" % args.campaign, file=sys.stderr)
        return 1
    if(args.include_nominal and (args.recovery_batches in [None, ""])):
        print("include_nominal requires a recovery batch file", file=sys.stderr)
        return 1
    separate = [args.nominal_only, args.only_5d_spline, args.pips6o_batch111]
    if(len([item for item in separate if(item)]) > 1):
        print("nominal_only, only_5d_spline, and pips6o_batch111 are separate campaigns", file=sys.stderr)
        return 1
    if(args.nominal_only and ((args.recovery_batches not in [None, ""]) or args.include_nominal or args.regenerate_nominal_spline_hpp)):
        print("nominal_only does not take recovery batches, include_nominal, or HPP regeneration", file=sys.stderr)
        return 1
    if(args.nominal_only and (not args.shared_unfold_output)):
        print("nominal_only requires shared_unfold_output", file=sys.stderr)
        return 1
    if(args.only_5d_spline and ((args.recovery_batches not in [None, ""]) or args.include_nominal or args.regenerate_nominal_spline_hpp or args.shared_unfold_output)):
        print("only_5d_spline does not take recovery batches, include_nominal, HPP regeneration, or shared_unfold_output", file=sys.stderr)
        return 1
    if(args.pips6o_batch111 and ((args.recovery_batches not in [None, ""]) or args.include_nominal or args.regenerate_nominal_spline_hpp or (not args.shared_unfold_output) or (args.weight_mode != "both"))):
        print("pips6o_batch111 requires -wm both and -suo, and does not take recovery batches, include_nominal, or HPP regeneration", file=sys.stderr)
        return 1
    if(args.phase1_local_concurrency is not None):
        if(not args.nominal_only):
            print("phase1_local_concurrency requires nominal_only", file=sys.stderr)
            return 1
        if(int(args.phase1_local_concurrency) < 1):
            print("phase1 local concurrency must be at least 1", file=sys.stderr)
            return 1
    if((args.recovery_batches not in [None, ""]) and args.regenerate_nominal_spline_hpp):
        print("recovery does not regenerate the nominal spline HPP", file=sys.stderr)
        return 1
    try:
        ceiling = COMPLETE_LINEAGE_COUNT if(args.include_nominal or args.shared_unfold_output) else None
        args.max_local_workers = worker_cap(args.max_local_workers, ceiling)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    recovery = None
    if(args.recovery_batches not in [None, ""]):
        try:
            recovery = load_recovery_batches(resolve_recovery_path(args.recovery_batches))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    camp = campaign_directory(args.data_root, args.campaign)
    previous = read_manifest(camp) if(args.resume or os.path.isfile(manifest_path(camp))) else None
    if(args.resume and (previous is None)):
        print("no manifest to resume at %s" % manifest_path(camp), file=sys.stderr)
        return 1
    stamp = time.strftime("%Y%m%d_%H%M%S")
    try:
        manifest = build_manifest(
            args.data_root, args.campaign, args.weight_mode, args.max_local_workers,
            args.hpp_tag, args.regenerate_nominal_spline_hpp, stamp, previous=previous if(args.resume) else None,
            recovery=recovery, include_nominal=args.include_nominal, shared_unfold=args.shared_unfold_output,
            nominal_only=args.nominal_only, only_5d=args.only_5d_spline, pips6o_batch111=args.pips6o_batch111,
            phase1_local_jobs=args.phase1_local_concurrency,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    fill_commands(manifest, sys.executable)
    regen_cmd = None
    if(args.regenerate_nominal_spline_hpp):
        nominal = [row for row in manifest["phase1"] if(row["nominal"])][0]
        regen_cmd = regen_command(sys.executable, SUBMIT_SCRIPT, args.data_root, nominal["hpp_spline"])
    last_manifest = manifest
    if(args.dry_run):
        print_plan(manifest, regen_cmd)
        return 0
    write_manifest(camp, manifest)
    if(args.email_message not in [None, ""]):
        print(args.email_message)
    run_live(args, manifest)
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
