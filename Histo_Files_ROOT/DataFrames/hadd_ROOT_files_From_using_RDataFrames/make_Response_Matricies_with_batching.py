#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import shutil
import time
import re

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

timer = RuntimeTimer()

# =========================
# Configuration section
# =========================

# Absolute path to your main analysis script.
DEFAULT_MAIN_SCRIPT = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py"

# Default email (can be overridden with --email)
DEFAULT_EMAIL = "richard.capobianco@uconn.edu"

# Base ROOT file prefix from Response_Matrix_Creation_using_RDataFrames.py:
ROOT_BASE_PREFIX = "SIDIS_epip_Response_Matrices_from_RDataFrames.root"

# Default SLURM settings (used only in --mode slurm)
# DEFAULT_SLURM_PARTITION   = "production"
DEFAULT_SLURM_TIME        = "20:00:00"      # HH:MM:SS
# DEFAULT_SLURM_ACCOUNT     = "clas12"
DEFAULT_SLURM_MEM_PER_CPU = "3GB"

# Args that are always passed to Response_Matrix_Creation_using_RDataFrames.py
# (As requested: "-f -MR")
# ALWAYS_MAIN_ARGS = ["-f", "-MR", "-e", "--event_limit", "1"]
# ALWAYS_MAIN_ARGS = ["-f", "-MR", "--event_limit", "1"]
# ALWAYS_MAIN_ARGS = ["-f", "--event_limit", "1", "-dr"]
ALWAYS_MAIN_ARGS = ["-f", "-MR", "-e"]

JSON_DEFAULT_PATH = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json"

# Preset configurations: base name, title, base email message, etc.
PRESETS = {
    "zeroth": {
        "name_base":        "ZerothOrder",
        "title":            "Zeroth Order (No Weights)",
        "email_base":       "Zeroth Order batched run. No Injected Physics/Weights.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp",
        "use_json_weights": False,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          False,
        "angles_only_hpp":  False,
    },
    "ac-zeroth": {
        "name_base":        "ZerothOrderAcc",
        "title":            "Zeroth Order Acceptance Weights",
        "email_base":       "Zeroth Order Acceptance Weight batched run. No Injected Physics.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp",
        "use_json_weights": False,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          True,
        "angles_only_hpp":  False,
    },
    "ao-zeroth": {
        "name_base":        "AngleOnlyZerothOrderAcc",
        "title":            "Zeroth Order Acceptance Weights (Angles Only)",
        "email_base":       "Zeroth Order Acceptance Weight batched run. Only used the acceptance weights for the lab angles. No Momemntum weights OR Injected Physics.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp",
        "use_json_weights": False,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          True,
        "angles_only_hpp":  True,
    },
    "first": {
        "name_base":        "FirstOrder",
        "title":            "First Order Modulation Weights",
        "email_base":       "First Order Injected Physics Modulation Weight batched run. No Acceptance Weights.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          False,   # disable acceptance weights
        "angles_only_hpp":  False,  # No variation of physics weights only will use 'angles_only_hpp'
    },
    "first-acc": {
        "name_base":        "FirstOrderAcc",
        "title":            "#splitline{First Order Acceptance Weights}{Made with injected physics}",
        "email_base":       "First Acceptance Order Weight batched run. Uses both the Injected Physics Modulations AND Acceptance Weights.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          True,
        "angles_only_hpp":  False,
    },
    "ao-first-acc": {
        "name_base":        "AngleOnlyFirstOrderAcc",
        "title":            "#splitline{First Order Acceptance Weights (Angles Only)}{Made with injected physics}",
        "email_base":       "First Acceptance Order Weight batched run. Uses both the Injected Physics Modulations AND Acceptance Weights, but the acceptance weights only used the lab angles (not momentum).",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "use_hpp":          True,
        "angles_only_hpp":  True,
    },
}



# =========================
# Email helpers
# =========================

def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {
        '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
        '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
        '\033[0m': "",
    }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text


def send_email(subject, body, recipient):
    html_body = ansi_to_html(body)
    try:
        subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)
    except FileNotFoundError:
        print(f"{color.Error}\n[WARNING] 'mail' command not found; cannot send email.\n{color.END}")
    except Exception as e:
        print(f"{color.Error}\n[WARNING] Exception while running mail: {e}\n{color.END}")


# =========================
# Helper functions
# =========================

def parse_unique_batches_string(unique_str, max_batch):
    # Parses SLURM-style array strings like:
    #   "1-5,7,10-12"
    # Also supports:
    #   "1-10:2" (step)
    #   "1-57%10" (concurrency; ignored here)
    #
    # Returns a sorted list of batch indices within [1, max_batch], or None if not provided.
    if((unique_str is None)):
        return None

    s = str(unique_str).strip()
    if((s == "")):
        return None

    s = s.replace(" ", "")

    # Ignore concurrency suffix like "%10"
    if(("%" in s)):
        s = s.split("%", 1)[0].strip()
        if((s == "")):
            return None

    selected = set()
    bad_tokens = []

    for token in s.split(","):
        if((token is None) or (token == "")):
            continue

        step_val = 1
        if((":" in token)):
            left, step_str = token.split(":", 1)
            token = left
            try:
                step_val = int(step_str)
                if((step_val <= 0)):
                    step_val = 1
            except Exception:
                step_val = 1

        if(("-" in token)):
            parts = token.split("-", 1)
            if(len(parts) != 2):
                bad_tokens.append(token)
                continue
            try:
                a = int(parts[0])
                b = int(parts[1])
            except Exception:
                bad_tokens.append(token)
                continue

            if((a > b)):
                a, b = b, a

            for v in range(a, b + 1, step_val):
                selected.add(v)
        else:
            try:
                selected.add(int(token))
            except Exception:
                bad_tokens.append(token)

    if(len(bad_tokens) > 0):
        print(f"{color.Error}[WARNING]{color.END} Could not parse some --unique_batches tokens: {bad_tokens}")

    # Filter to legal range
    in_range  = sorted([v for v in selected if((v >= 1) and (v <= max_batch))])
    out_range = sorted([v for v in selected if((v < 1) or (v > max_batch))])

    if(len(out_range) > 0):
        print(f"{color.Error}[WARNING]{color.END} Some --unique_batches values are outside [1, {max_batch}] and will be ignored: {out_range}")

    if(len(in_range) == 0):
        return []

    return in_range


def build_name_base_for_merged(preset_cfg, name_tag):
    # e.g., "ZerothOrder" or "ZerothOrder_MyTag"
    parts = [preset_cfg["name_base"]]
    if((name_tag is not None) and (name_tag != "")):
        parts.append(name_tag)
    return "_".join(parts)


def build_name_for_batch(name_base_for_merged, batch_index):
    # e.g., "ZerothOrder_MyTag_Batch001" (max groups 108 -> 3 digits is enough)
    name_base_for_merged = name_base_for_merged.replace(".root", "_")
    return f"{name_base_for_merged}_Batch{batch_index:03d}"


def build_batch_root_filename(name_for_batch, output_dir):
    filename = f"{ROOT_BASE_PREFIX}{name_for_batch}.root"
    filename = filename.replace("RDataFrames.root", "RDataFrames_")
    return os.path.join(output_dir, filename)


def build_merged_root_filename(name_base_for_merged, output_dir):
    filename = f"{ROOT_BASE_PREFIX}{name_base_for_merged}.root"
    filename = filename.replace("RDataFrames.root", "RDataFrames_")
    return os.path.join(output_dir, filename)


def build_email_message(preset_cfg, email_extra):
    msg = preset_cfg["email_base"]
    if((email_extra is not None) and (email_extra.strip() != "")):
        msg = f"{msg}\n{email_extra}"
    return msg


def apply_common_preset_args_to_cmd(cmd_base, preset_cfg):
    # hpp file always provided
    cmd_base.extend(["-hpp_in", preset_cfg["hpp_file"]])

    # JSON weights / file
    if(preset_cfg.get("use_json_weights", False)):
        cmd_base.append("--json_weights")
        cmd_base.extend(["--json_file", preset_cfg.get("json_file", JSON_DEFAULT_PATH)])

    # disable acceptance weights completely
    if(preset_cfg.get("use_hpp", False)):
        cmd_base.append("--use_hpp")

    # angles-only acceptance weights
    if(preset_cfg.get("angles_only_hpp", False)):
        cmd_base.append("--angles_only_hpp")
        

def run_single_batch_sequential(main_script, batch_index, output_dir, preset_cfg, name_base_for_merged, email_msg, valerii_bins=False):
    name_for_batch   = build_name_for_batch(name_base_for_merged, batch_index)
    batch_root_file  = build_batch_root_filename(name_for_batch, output_dir)

    cmd_base = [sys.executable, main_script, "-bID", str(batch_index)]
    cmd_base.extend(ALWAYS_MAIN_ARGS)
    cmd_base.extend(["-n", name_for_batch])
    cmd_base.extend(["-t", preset_cfg["title"]])
    cmd_base.extend(["-em", email_msg])
    apply_common_preset_args_to_cmd(cmd_base, preset_cfg)

    if(valerii_bins):
        cmd_base.append("--valerii_bins")

    print(f"\n{color.BBLUE}[INFO]{color.END} Running batch {batch_index} (name={name_for_batch})...")
    print("       Command:", " ".join(cmd_base))

    try:
        proc       = subprocess.run(cmd_base)
        returncode = proc.returncode
    except Exception as e:
        print(f"{color.Error}[ERROR]{color.END} Exception while running batch {batch_index}: {e}")
        returncode = 1

    if(returncode == 0):
        if(os.path.isfile(batch_root_file)):
            print(f"{color.BGREEN}[INFO]{color.END} Batch {batch_index} completed successfully.")
        else:
            print(f"{color.Error}[WARNING]{color.END} Batch {batch_index} exited with code 0 but ROOT file is missing: {batch_root_file}")
            returncode = 1
    else:
        print(f"{color.Error}[ERROR]{color.END} Batch {batch_index} failed with return code {returncode}.")

    return {
        "batch_id":       batch_index,
        "returncode":     returncode,
        "root_file":      batch_root_file,
        "name_for_batch": name_for_batch,
    }


def run_batches_parallel(main_script, nbatches, output_dir, max_parallel, preset_cfg, name_base_for_merged, email_msg, valerii_bins=False):
    results   = []
    running   = []
    next_id   = 1

    while(True):
        while((next_id <= nbatches) and (len(running) < max_parallel)):
            batch_index     = next_id
            next_id        += 1

            name_for_batch  = build_name_for_batch(name_base_for_merged, batch_index)
            batch_root_file = build_batch_root_filename(name_for_batch, output_dir)

            cmd_base = [sys.executable, main_script, "-bID", str(batch_index)]
            cmd_base.extend(ALWAYS_MAIN_ARGS)
            cmd_base.extend(["-n", name_for_batch])
            cmd_base.extend(["-t", preset_cfg["title"]])
            cmd_base.extend(["-em", email_msg])
            apply_common_preset_args_to_cmd(cmd_base, preset_cfg)

            if(valerii_bins):
                cmd_base.append("--valerii_bins")

            print(f"\n{color.BBLUE}[INFO]{color.END} Starting batch {batch_index} in parallel (name={name_for_batch})...")
            print("       Command:", " ".join(cmd_base))
            try:
                proc = subprocess.Popen(cmd_base)
            except Exception as e:
                print(f"{color.Error}[ERROR]{color.END} Failed to start batch {batch_index}: {e}")
                results.append({
                    "batch_id":       batch_index,
                    "returncode":     1,
                    "root_file":      batch_root_file,
                    "name_for_batch": name_for_batch,
                })
                continue

            running.append({
                "batch_id":       batch_index,
                "process":        proc,
                "root_file":      batch_root_file,
                "name_for_batch": name_for_batch,
            })

        if((len(running) == 0) and (next_id > nbatches)):
            break

        time.sleep(5)

        still_running = []
        for item in running:
            proc         = item["process"]
            ret          = proc.poll()
            batch_id     = item["batch_id"]
            root_file    = item["root_file"]
            name_for_bch = item["name_for_batch"]

            if(ret is None):
                still_running.append(item)
                continue

            if(ret == 0):
                if(os.path.isfile(root_file)):
                    print(f"{color.BGREEN}[INFO]{color.END} Batch {batch_id} completed successfully (parallel).")
                else:
                    print(f"{color.Error}[WARNING]{color.END} Batch {batch_id} exited with code 0 but ROOT file is missing: {root_file}")
                    ret = 1
            else:
                print(f"{color.Error}[ERROR]{color.END} Batch {batch_id} failed with return code {ret} (parallel).")

            results.append({
                "batch_id":       batch_id,
                "returncode":     ret,
                "root_file":      root_file,
                "name_for_batch": name_for_bch,
            })

        running = still_running

    return results


def run_hadd(batch_files, merged_file):
    # =====================
    # Check ROOTSYS
    # =====================
    if("ROOTSYS" not in os.environ):
        print(f"{color.Error}[ERROR]{color.END} ROOTSYS is not set. Cannot locate hadd.")
        return False

    hadd_path = os.path.join(os.environ["ROOTSYS"], "bin", "hadd")

    if(not os.path.isfile(hadd_path)):
        print(f"{color.Error}[ERROR]{color.END} hadd not found at: {hadd_path}")
        return False

    # =====================
    # Rename existing merged file if present
    # =====================
    if(os.path.isfile(merged_file)):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        dirname   = os.path.dirname(merged_file)
        basename  = os.path.basename(merged_file)
        newname   = f"{basename}_Outdated_on_{timestamp}_delete_later"
        newname   = f'{newname.replace(".root", "")}.root'
        newpath   = os.path.join(dirname, newname)

        try:
            os.rename(merged_file, newpath)
            print(f"{color.BBLUE}[INFO]{color.END} Existing merged file renamed to:\n       {newpath}")
        except Exception as e:
            print(f"{color.Error}[ERROR]{color.END} Could not rename existing merged file {merged_file}: {e}")
            return False

    # =====================
    # Build hadd command
    # =====================
    cmd = [hadd_path, "-f", merged_file] + batch_files

    print(f"\n{color.BBLUE}[INFO]{color.END} Running hadd to merge batch files:")
    print("       Command:", " ".join(cmd))

    # =====================
    # Run hadd
    # =====================
    try:
        proc = subprocess.run(cmd)
        if(proc.returncode != 0):
            print(f"{color.Error}[ERROR]{color.END} hadd failed with return code {proc.returncode}.")
            return False
    except Exception as e:
        print(f"{color.Error}[ERROR]{color.END} Exception while running hadd: {e}")
        return False

    # =====================
    # Verify output file
    # =====================
    if(os.path.isfile(merged_file)):
        print(f"{color.BGREEN}[INFO]{color.END} Successfully created merged ROOT file:\n       {merged_file}")
        return True

    print(f"{color.Error}[ERROR]{color.END} hadd reported success but merged file missing: {merged_file}")
    return False


def delete_batch_files(batch_files):
    print(f"\n{color.BBLUE}[INFO]{color.END} Deleting batch ROOT files...")
    for path in batch_files:
        try:
            os.remove(path)
            print(f"       Deleted: {path}")
        except FileNotFoundError:
            print(f"       Skipping missing file: {path}")
        except Exception as e:
            print(f"       {color.Error}[WARNING]{color.END} Could not delete {path}: {e}")


# =========================
# SLURM array status helpers (used by sequential mode)
# =========================

SLURM_ARRAY_CHECK_DISABLED = False


def query_slurm_array_task_state(array_jobid, batch_index):
    global SLURM_ARRAY_CHECK_DISABLED

    if(SLURM_ARRAY_CHECK_DISABLED):
        return "IGNORE"

    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid), "-o", "%.18i %.2t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} squeue not found; cannot coordinate with SLURM array job {array_jobid}.")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    except Exception as e:
        print(f"{color.Error}[WARNING]{color.END} Exception while running squeue for array job {array_jobid}: {e}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"

    if(proc.returncode != 0):
        msg = proc.stderr.strip()
        if(msg == ""):
            msg = "(no additional message from squeue)"
        print(f"{color.Error}[WARNING]{color.END} squeue for array job {array_jobid} returned code {proc.returncode}: {msg}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"

    target_id = f"{array_jobid}_{batch_index}"
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if(len(parts) < 2):
            continue
        job_id = parts[0]
        state  = parts[1]
        if(job_id == target_id):
            return state

    # Not found (not pending/running/etc. in this array) -> treat as completed or absent
    return None


def cancel_slurm_array_task(array_jobid, batch_index):
    job_str = f"{array_jobid}_{batch_index}"
    try:
        proc = subprocess.run(["scancel", job_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} scancel not found; cannot cancel SLURM array task {job_str}.")
        return False
    except Exception as e:
        print(f"{color.Error}[WARNING]{color.END} Exception while running scancel on {job_str}: {e}")
        return False

    if(proc.returncode != 0):
        msg = proc.stderr.strip()
        if(msg == ""):
            msg = "(no additional message from scancel)"
        print(f"{color.Error}[WARNING]{color.END} scancel {job_str} failed with code {proc.returncode}: {msg}")
        return False

    print(f"{color.BBLUE}[INFO]{color.END} Cancelled SLURM array task {job_str} (state was pending).")
    return True


def slurm_array_has_active_tasks(array_jobid):
    global SLURM_ARRAY_CHECK_DISABLED

    if(array_jobid is None):
        return False
    if(SLURM_ARRAY_CHECK_DISABLED):
        # Coordination has been disabled earlier; fall back to original behaviour
        return False

    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} squeue not found; cannot check active tasks for SLURM array job {array_jobid}.")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False
    except Exception as e:
        print(f"{color.Error}[WARNING]{color.END} Exception while checking active tasks for SLURM array job {array_jobid}: {e}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False

    if(proc.returncode != 0):
        msg = proc.stderr.strip()
        if(msg == ""):
            msg = "(no additional message from squeue)"
        print(f"{color.Error}[WARNING]{color.END} squeue for array job {array_jobid} (final check) returned code {proc.returncode}: {msg}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False

    output = proc.stdout.strip()
    if(output == ""):
        # No lines -> no active tasks in this array
        return False

    # At least one active task is still present
    return True


def cancel_slurm_job(jobid):
    try:
        proc = subprocess.run(["scancel", str(jobid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} scancel not found; cannot cancel SLURM job {jobid}.")
        return False
    except Exception as e:
        print(f"{color.Error}[WARNING]{color.END} Exception while running scancel on job {jobid}: {e}")
        return False

    if(proc.returncode != 0):
        msg = proc.stderr.strip()
        if(msg == ""):
            msg = "(no additional message from scancel)"
        print(f"{color.Error}[WARNING]{color.END} scancel {jobid} failed with code {proc.returncode}: {msg}")
        return False

    print(f"{color.BBLUE}[INFO]{color.END} Cancelled SLURM job {jobid} (hadd job).")
    return True


# =========================
# SLURM helpers (bash sbatch, with preview + approval)
# =========================

def build_slurm_array_script_text(main_script, preset_cfg, name_base_for_merged, email_msg, nbatches, time_str, slurm_mem_per_cpu, email_address, job_name, unique_array=None, valerii_bins=False):
    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append(f"#SBATCH --mail-user={email_address}")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append("#SBATCH --partition=production")
    lines.append("#SBATCH --account=clas12")
    lines.append(f"#SBATCH --mem-per-cpu={slurm_mem_per_cpu}")
    lines.append(f"#SBATCH --time={time_str}")
    if(unique_array is not None):
        lines.append(f"#SBATCH --array={unique_array}")
    else:
        lines.append(f"#SBATCH --array=1-{nbatches}")
    lines.append("")
    lines.append("")
    lines.append('BATCH_ID=${SLURM_ARRAY_TASK_ID}')
    # lines.append('echo "Running batch ${BATCH_ID} on host $(hostname) at $(date)"')
    lines.append(f'NAME_BASE="{name_base_for_merged}"')

    safe_email_msg = email_msg.replace('"', '\\"')
    lines.append(f'EMAIL_MSG="{safe_email_msg}"')
    lines.append("")

    # cmd_parts = [sys.executable, main_script, "-bID", "${BATCH_ID}"]
    cmd_parts = ["srun", "python3", main_script, "-bID", "${BATCH_ID}"]
    if("-e" in ALWAYS_MAIN_ARGS):
        ALWAYS_MAIN_ARGS.remove("-e") # Do not send emails within sbatch jobs
    cmd_parts.extend(ALWAYS_MAIN_ARGS)

    if(valerii_bins):
        cmd_parts.append("--valerii_bins")

    cmd_parts.extend(["-n", '"${NAME_BASE}"'])
    cmd_parts.extend(["-t", f"\"{preset_cfg['title']}\""])
    cmd_parts.extend(["-em", '"${EMAIL_MSG}"'])
    apply_common_preset_args_to_cmd(cmd_parts, preset_cfg)

    cmd_str = " ".join(cmd_parts)

    lines.append("")
    # lines.append(f'echo "Command: {cmd_str}"')
    lines.append(cmd_str)
    lines.append("")
    lines.append("")
    # lines.append('exit_code=$?')
    # lines.append('echo "Batch ${BATCH_ID} finished with exit code ${exit_code} at $(date)"')
    # lines.append("exit ${exit_code}")

    return "\n".join(lines)


def build_slurm_hadd_script_text(output_dir, name_base_for_merged, merged_file, time_str, slurm_mem_per_cpu, email_address, job_name):
    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append(f"#SBATCH --mail-user={email_address}")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append("#SBATCH --partition=production")
    lines.append("#SBATCH --account=clas12")
    lines.append("#SBATCH --mem-per-cpu=1GB")
    lines.append(f"#SBATCH --time=04:00:00")
    lines.append("")
    lines.append("")

    batch_pattern = os.path.join(output_dir, f"{ROOT_BASE_PREFIX}{name_base_for_merged}_Batch[0-9]*.root")
    batch_pattern = batch_pattern.replace("RDataFrames.root", "RDataFrames_")

    cmd_parts = ["$ROOTSYS/bin/hadd", "-f", merged_file, batch_pattern]
    cmd_str   = " ".join(cmd_parts)

    lines.append(cmd_str)
    lines.append("")
    lines.append("")

    return "\n".join(lines)


def submit_slurm_jobs(nbatches, main_script, output_dir, time_str, preset_cfg, name_base_for_merged, email_msg, email_address, slurm_mem_per_cpu, unique_array_batches=None, valerii_bins=False):
    script_dir_local = os.path.dirname(os.path.abspath(__file__))

    batch_files = []
    for i in range(1, nbatches + 1):
        name_for_batch = build_name_for_batch(name_base_for_merged, i)
        batch_files.append(build_batch_root_filename(name_for_batch, output_dir))

    merged_file = build_merged_root_filename(name_base_for_merged, output_dir)

    date_str       = time.strftime("%m_%d_%Y")
    job_base       = preset_cfg["name_base"]
    array_job_name = f"RMatrix_{job_base}_{date_str}_running_batch_jobs"
    hadd_job_name  = f"RMatrix_{job_base}_{date_str}_hadd_batches"

    if(valerii_bins):
        array_job_name = f"V_{array_job_name}"
        hadd_job_name  = f"V_{hadd_job_name}"

    array_script_text = build_slurm_array_script_text(main_script, preset_cfg, name_base_for_merged, email_msg, nbatches, time_str, slurm_mem_per_cpu, email_address, array_job_name, unique_array=unique_array_batches, valerii_bins=valerii_bins)

    hadd_script_text = build_slurm_hadd_script_text(output_dir, name_base_for_merged, merged_file, time_str, slurm_mem_per_cpu, email_address, hadd_job_name)

    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM array script:\n")
    print(array_script_text)
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM hadd script:\n")
    print(hadd_script_text)

    if(os.path.isfile(merged_file)):
        timestamp = time.strftime("%m-%d-%Y")
        dirname   = os.path.dirname(merged_file)
        basename  = os.path.basename(merged_file)
        newname   = f"{basename}_Outdated_on_{timestamp}_delete_later"
        newname   = f'{newname.replace(".root", "")}.root'
        newpath   = os.path.join(dirname, newname)
        print(f"\n{color.Error}[WARNING]{color.END_R} The to-be-merged file '{merged_file}' already exists.\n\t{color.END_B}If approved, will rename it to: {newpath}{color.END}\n\n")

    try:
        response = input("\nApprove and submit these SLURM scripts? [y/N]: ").strip().lower()
    except EOFError:
        response = "n"

    if((response != "y") and (response != "yes")):
        print(f"{color.Error}[ERROR]{color.END} SLURM scripts not approved. Exiting without submission.")
        return None, None, merged_file, batch_files

    array_script_path = os.path.join(script_dir_local, "Response_Matrix_slurm_array_job.sh")
    hadd_script_path  = os.path.join(script_dir_local, "Response_Matrix_slurm_hadd_job.sh")

    if(os.path.isfile(merged_file)):
        try:
            os.rename(merged_file, newpath)
            print(f"{color.BBLUE}[INFO]{color.END} Existing merged file renamed to:\n       {newpath}")
        except Exception as e:
            print(f"{color.Error}[ERROR] Could not rename existing merged file {merged_file}:{color.END} {e}")

    try:
        with open(array_script_path, "w") as f:
            f.write(array_script_text)
        os.chmod(array_script_path, 0o755)

        with open(hadd_script_path, "w") as f:
            f.write(hadd_script_text)
        os.chmod(hadd_script_path, 0o755)
    except Exception as e:
        print(f"{color.Error}[ERROR]{color.END} Could not write SLURM scripts: {e}")
        return None, None, merged_file, batch_files

    array_cmd = ["sbatch", "--parsable", array_script_path]

    print(f"\n{color.BBLUE}[INFO]{color.END} Submitting SLURM array job:")
    print("       Command:", " ".join(array_cmd))

    try:
        proc = subprocess.run(array_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"{color.Error}[ERROR]{color.END} Exception while submitting SLURM array job: {e}")
        return None, None, merged_file, batch_files

    if(proc.returncode != 0):
        print(f"{color.Error}[ERROR]{color.END} sbatch for array job failed with code {proc.returncode}")
        print(proc.stderr)
        return None, None, merged_file, batch_files

    array_jobid_raw = proc.stdout.strip()
    print(f"{color.BBLUE}[INFO]{color.END} Submitted array job with id: {array_jobid_raw}")
    array_jobid = array_jobid_raw.split(";")[0].strip()

    hadd_cmd = ["sbatch", "--parsable", f"--dependency=afterok:{array_jobid}", hadd_script_path]

    print(f"\n{color.BBLUE}[INFO]{color.END} Submitting SLURM hadd job (afterok dependency):")
    print("       Command:", " ".join(hadd_cmd))

    try:
        proc2 = subprocess.run(hadd_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"{color.Error}[ERROR]{color.END} Exception while submitting SLURM hadd job: {e}")
        return array_jobid, None, merged_file, batch_files

    if(proc2.returncode != 0):
        print(f"{color.Error}[ERROR]{color.END} sbatch for hadd job failed with code {proc2.returncode}")
        print(proc2.stderr)
        return array_jobid, None, merged_file, batch_files

    hadd_jobid_raw = proc2.stdout.strip()
    print(f"{color.BBLUE}[INFO]{color.END} Submitted hadd job with id: {hadd_jobid_raw}")
    hadd_jobid = hadd_jobid_raw.split(";")[0].strip()

    return array_jobid, hadd_jobid, merged_file, batch_files


def wait_for_slurm_job(jobid, poll_seconds=60):
    print(f"\n{color.BBLUE}[INFO]{color.END} Waiting for SLURM job {jobid} to finish...")
    while(True):
        try:
            proc = subprocess.run(["squeue", "-j", jobid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except FileNotFoundError:
            print(f"{color.Error}[WARNING]{color.END} squeue not found; cannot actively wait for job.")
            return

        if(proc.returncode != 0):
            print(f"{color.Error}[WARNING]{color.END} squeue returned non-zero code {proc.returncode}.")
            print(proc.stderr)
            return

        lines = proc.stdout.strip().splitlines()
        if(len(lines) <= 1):
            print(f"{color.BBLUE}[INFO]{color.END} SLURM job {jobid} no longer in queue.")
            break

        print(f"{color.BBLUE}[INFO]{color.END} Job {jobid} still running or pending... sleeping {poll_seconds} seconds.")
        time.sleep(poll_seconds)


# =========================
# Main
# =========================

def main():
    parser = argparse.ArgumentParser(
        description="Orchestrate batched ROOT production with using_RDataFrames_python.py and hadd.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-nb", "--nbatches",
                        type=int,
                        default=108,
                        choices=range(1, 109),
                        help="Number of batches (integer between 1 and 108).")
    parser.add_argument("-ub", "--unique_batches",
                        type=str,
                        default=None,
                        help="Unique set of batches to run (SLURM-style list like '1-5,7,10-12'). Works in slurm mode (as --array) and sequential mode (as a local filter).")
    parser.add_argument("-m", "--mode",
                        choices=["sequential", "parallel", "slurm"],
                        default="sequential",
                        help="Run mode: sequential (default), parallel, or slurm.")
    parser.add_argument("-nt", "--name-tag",
                        default=None,
                        help="Optional name tag appended into the --name used for files (affects both batch and merged ROOT names).")
    parser.add_argument("-dbf", "--delete-batch-files",
                        action="store_true",
                        help="Delete per-batch ROOT files after successful hadd. Ignored in the 'slurm' mode.")
    parser.add_argument("--max-parallel",
                        type=int,
                        default=2,
                        help="Maximum number of parallel jobs in parallel mode.")
    parser.add_argument("-e", "--email",
                        default=None,
                        help="Email address for notifications (overrides DEFAULT_EMAIL).")
    parser.add_argument("--main-script",
                        default=DEFAULT_MAIN_SCRIPT,
                        help="Path to Response_Matrix_Creation_using_RDataFrames.py (or equivalent).")
    parser.add_argument("--output-dir",
                        default=os.path.dirname(os.path.abspath(__file__)),
                        help="Directory where batch and merged ROOT files live.")
    parser.add_argument("-st", "--slurm-time",
                        default=DEFAULT_SLURM_TIME,
                        help="SLURM time limit for each job in slurm mode (HH:MM:SS).")
    parser.add_argument("-cpu", "--slurm-mem-per-cpu",
                        default=DEFAULT_SLURM_MEM_PER_CPU,
                        help="SLURM memory per CPU in slurm mode (e.g. '2GB', '4000M').")
    parser.add_argument("-p", "--preset",
                        choices=["zeroth", "ac-zeroth", "ao-zeroth", "first", "first-acc", "ao-first-acc"],
                        default="zeroth",
                        help="Preset configuration.")
    parser.add_argument("-ee", "-em", "--email-extra",
                        type=str,
                        default="",
                        help="Extra message appended to the -em email message passed to Response_Matrix_Creation_using_RDataFrames.py.")
    parser.add_argument("-saj", "--slurm-array-jobid",
                        type=str,
                        default=None,
                        help="Optional SLURM array job ID to coordinate with sequential mode (cancel pending tasks and skip running/completed ones).")
    parser.add_argument("-shj", "--slurm-hadd-jobid",
                        type=str,
                        default=None,
                        help="Optional SLURM hadd job ID to cancel if local hadd completes successfully.")
    parser.add_argument("-vb", "--valerii_bins",
                        action="store_true",
                        help="Pass --valerii_bins through to Response_Matrix_Creation_using_RDataFrames.py.")

    args = parser.parse_args()

    if((args.nbatches <= 0) or (args.nbatches > 108)):
        print(f"{color.Error}[ERROR]{color.END} --nbatches must be between 1 and 108 (Maximum Group Number: 108).")
        sys.exit(1)

    if((args.slurm_array_jobid is not None) and (args.mode != "sequential")):
        print(f"{color.BBLUE}[INFO]{color.END} --slurm-array-jobid provided but mode is '{args.mode}'. This option only affects sequential mode and will be ignored for other modes.")

    if((args.slurm_hadd_jobid is not None) and (args.mode != "sequential")):
        print(f"{color.BBLUE}[INFO]{color.END} --slurm-hadd-jobid provided but mode is '{args.mode}'. This option only affects sequential mode and will be ignored for other modes.")

    email_address = args.email if(args.email is not None) else DEFAULT_EMAIL

    output_dir = os.path.abspath(args.output_dir)
    if(not os.path.isdir(output_dir)):
        print(f"{color.BBLUE}[INFO]{color.END} Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    main_script = os.path.abspath(args.main_script)
    if(not os.path.isfile(main_script)):
        print(f"{color.Error}[ERROR]{color.END} Main script not found: {main_script}")
        sys.exit(1)

    if(args.preset not in PRESETS):
        print(f"{color.Error}[ERROR]{color.END} Unknown preset: {args.preset}")
        sys.exit(1)

    preset_cfg           = PRESETS[args.preset]
    name_base_for_merged = build_name_base_for_merged(preset_cfg, args.name_tag)
    email_msg            = build_email_message(preset_cfg, args.email_extra)

    overall_success = False
    hadd_success    = False
    delete_success  = False
    batch_failures  = []

    merged_file = build_merged_root_filename(name_base_for_merged, output_dir)

    if(args.mode == "sequential"):
        print(f"{color.BBLUE}[INFO]{color.END} Running in sequential local mode (no SLURM).")

        requested_batches = parse_unique_batches_string(args.unique_batches, args.nbatches)
        if((args.unique_batches is not None) and (requested_batches is not None)):
            print(f"{color.BBLUE}[INFO]{color.END} --unique_batches provided for sequential mode: '{args.unique_batches}'")
            print(f"{color.BBLUE}[INFO]{color.END} Will attempt to run these batch IDs (after range filtering): {requested_batches}")

        results             = []
        slurm_array_active  = False

        if((requested_batches is None)):
            batch_iterable = range(1, args.nbatches + 1)
        else:
            batch_iterable = requested_batches

        for batch_idx in batch_iterable:
            run_this_batch = True

            if(args.slurm_array_jobid is not None):
                state = query_slurm_array_task_state(args.slurm_array_jobid, batch_idx)

                if(state == "IGNORE"):
                    # Fall back to original sequential behaviour (no SLURM coordination)
                    pass
                elif(state is None):
                    # Not found in squeue output -> assume completed / not active, skip to avoid double-processing
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} not found in squeue output; assuming completed and skipping batch {batch_idx} in sequential mode.")
                    run_this_batch = False
                elif(state == "PD"):
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} is pending; attempting to cancel so sequential mode can run this batch.")
                    cancelled = cancel_slurm_array_task(args.slurm_array_jobid, batch_idx)
                    if(not cancelled):
                        print(f"{color.BBLUE}[INFO]{color.END} Could not safely cancel {args.slurm_array_jobid}_{batch_idx}; skipping batch {batch_idx} in sequential mode to avoid double-processing.")
                        run_this_batch = False
                else:
                    # Running or some other active state (e.g. CG, R, etc.)
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} is in state '{state}'; skipping batch {batch_idx} in sequential mode.")
                    run_this_batch = False

            if(not run_this_batch):
                continue

            res = run_single_batch_sequential(main_script, batch_idx, output_dir, preset_cfg, name_base_for_merged, email_msg, valerii_bins=args.valerii_bins)
            results.append(res)

        for res in results:
            if(res["returncode"] != 0):
                batch_failures.append(res["batch_id"])

        # Final check: are there any active SLURM array tasks still running/pending?
        if(args.slurm_array_jobid is not None):
            slurm_array_active = slurm_array_has_active_tasks(args.slurm_array_jobid)
            if(slurm_array_active):
                print(f"{color.BBLUE}[INFO]{color.END} SLURM array job {args.slurm_array_jobid} still has active tasks; local hadd will be skipped so the SLURM hadd job can perform the merge.")
            else:
                print(f"{color.BBLUE}[INFO]{color.END} No active tasks remain in SLURM array job {args.slurm_array_jobid}; local hadd is allowed to run if all sequential batches succeeded.")

        if(len(batch_failures) == 0):
            if(slurm_array_active):
                overall_success = True
                hadd_success    = f"Skipped locally (SLURM array {args.slurm_array_jobid} still active; SLURM hadd job will merge)."
            else:
                # For sequential reruns (including --unique_batches), attempt hadd over the full expected batch set.
                batch_files = []
                for i in range(1, args.nbatches + 1):
                    name_for_batch = build_name_for_batch(name_base_for_merged, i)
                    batch_files.append(build_batch_root_filename(name_for_batch, output_dir))

                missing_files = [bf for bf in batch_files if(not os.path.isfile(bf))]
                if(len(missing_files) > 0):
                    print(f"{color.Error}[ERROR]{color.END} Cannot run hadd: missing {len(missing_files)} expected batch ROOT files.")
                    print(f"{color.Error}[ERROR]{color.END} First missing file example(s):")
                    for mf in missing_files[:10]:
                        print(f"       {mf}")
                    hadd_success    = False
                    overall_success = False
                else:
                    hadd_success = run_hadd(batch_files, merged_file)

                    if(hadd_success and args.delete_batch_files):
                        delete_batch_files(batch_files)
                        delete_success = True

                    if(hadd_success and (args.slurm_hadd_jobid is not None)):
                        cancel_slurm_job(args.slurm_hadd_jobid)

                    overall_success = hadd_success
        else:
            print(f"{color.Error}[ERROR]{color.END} Some batches failed: {batch_failures}")
            overall_success = False

    elif(args.mode == "parallel"):
        print(f"{color.BBLUE}[INFO]{color.END} Running in parallel local mode (no SLURM).")
        if(args.max_parallel <= 0):
            print(f"{color.Error}[ERROR]{color.END} --max-parallel must be > 0 in parallel mode.")
            sys.exit(1)

        results = run_batches_parallel(main_script, args.nbatches, output_dir, args.max_parallel, preset_cfg, name_base_for_merged, email_msg, valerii_bins=args.valerii_bins)

        for res in results:
            if(res["returncode"] != 0):
                batch_failures.append(res["batch_id"])

        if(len(batch_failures) == 0):
            batch_files  = [res["root_file"] for res in results]
            hadd_success = run_hadd(batch_files, merged_file)
            if(hadd_success and args.delete_batch_files):
                delete_batch_files(batch_files)
                delete_success = True
            overall_success = hadd_success
        else:
            print(f"{color.Error}[ERROR]{color.END} Some batches failed: {batch_failures}")
            overall_success = False

    elif(args.mode == "slurm"):
        print(f"{color.BBLUE}[INFO]{color.END} Running in SLURM mode (submission only, no local waiting).")

        array_jobid, hadd_jobid, merged_file, batch_files = submit_slurm_jobs(args.nbatches, main_script, output_dir, args.slurm_time, preset_cfg, name_base_for_merged, email_msg, email_address, args.slurm_mem_per_cpu, unique_array_batches=args.unique_batches, valerii_bins=args.valerii_bins)

        if((array_jobid is None) or (hadd_jobid is None)):
            print(f"{color.Error}[ERROR]{color.END} Failed to submit SLURM jobs.")
            overall_success = False
            hadd_success    = "Not submitted"
        else:
            print(f"{color.BBLUE}[INFO]{color.END} SLURM array job id: {array_jobid}")
            print(f"{color.BBLUE}[INFO]{color.END} SLURM hadd job id:  {hadd_jobid}")
            print(f"{color.BBLUE}[INFO]{color.END} Merged ROOT file will be: {merged_file}")
            print(f"{color.BBLUE}[INFO]{color.END} Note: This script will not wait for jobs to finish; SLURM emails will report completion.")
            if(args.delete_batch_files):
                print(f"{color.BBLUE}[INFO]{color.END} Note: --delete-batch-files is ignored in slurm mode (cannot safely delete asynchronously).")

            overall_success = True
            hadd_success    = "Submitted via SLURM (not monitored in wrapper)"

    # =========================
    # Approximate peak memory (MB/GB) via resource.ru_maxrss
    # =========================
    peak_mem_str = "Unknown"
    try:
        import resource
        usage   = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak_kb = usage.ru_maxrss
        if(peak_kb > 0):
            peak_mb = peak_kb / 1024.0
            if(peak_mb < 1024.0):
                peak_mem_str = f"{peak_mb:.2f} MB"
            else:
                peak_gb      = peak_mb / 1024.0
                peak_mem_str = f"{peak_gb:.2f} GB"
    except Exception:
        peak_mem_str = "Unavailable (resource module not usable)"

    # =========================
    # Build summary + email
    # =========================

    start_time_str = timer.start_find(return_Q=True)
    start_time_str = start_time_str.replace("Ran", "Started running")
    end_time_str, total_time_str, rate_line = timer.stop(return_Q=True)

    summary_lines = []
    summary_lines.append("Script: make_Response_Matricies_with_batching.py")
    summary_lines.append(f"Mode: {args.mode}")
    summary_lines.append(f"Preset: {args.preset}")
    summary_lines.append(f"Main script: {main_script}")
    summary_lines.append(f"Output directory: {output_dir}")
    summary_lines.append(f"Name base for merged file: {name_base_for_merged}")
    summary_lines.append(f"Merged ROOT file: {merged_file}")
    summary_lines.append(f"Number of batches: {args.nbatches}")
    summary_lines.append(f"Unique batches: {args.unique_batches}")
    summary_lines.append(f"Valerii bins: {args.valerii_bins}")
    summary_lines.append(f"Overall success: {overall_success}")
    summary_lines.append(f"hadd success: {hadd_success}")
    summary_lines.append(f"Delete batch files flag: {args.delete_batch_files}")
    summary_lines.append(f"Delete batch files success: {delete_success}")
    summary_lines.append(f"Approx. peak memory usage (children): {peak_mem_str}")

    if(len(batch_failures) > 0):
        summary_lines.append(f"Failed batches: {batch_failures}")

    summary_block = "\n".join(summary_lines)

    email_body = f"""
The 'make_Response_Matricies_with_batching.py' script has finished running.

{start_time_str}

{summary_block}

{end_time_str}
{total_time_str}
{rate_line}
"""

    subject_status = "SUCCESS" if(overall_success) else "FAILURE"
    subject        = f"[make_Response_Matricies_with_batching] {subject_status} ({args.mode}, N={args.nbatches}, preset={args.preset})"

    print(email_body)

    # Only send email for non-SLURM modes; SLURM jobs send their own emails.
    if((args.mode != "slurm") and (email_address is not None) and (email_address != "")):
        send_email(subject=subject, body=email_body, recipient=email_address)

    if(overall_success):
        sys.exit(0)
    else:
        sys.exit(1)


if(__name__ == "__main__"):
    timer.start()
    main()
