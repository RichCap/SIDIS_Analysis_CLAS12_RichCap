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
DEFAULT_MAIN_SCRIPT = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/using_RDataFrames_python.py"

# Default email (can be overridden with --email)
DEFAULT_EMAIL = "richard.capobianco@uconn.edu"

# Base ROOT file prefix from using_RDataFrames_python.py:
#   SIDIS_epip_All_File_Types_from_RDataFrames_{args.name}.root
ROOT_BASE_PREFIX = "SIDIS_epip_All_File_Types_from_RDataFrames_"

# Default SLURM settings (used only in --mode slurm)
DEFAULT_SLURM_PARTITION   = "production"
DEFAULT_SLURM_TIME        = "08:00:00"      # HH:MM:SS
DEFAULT_SLURM_ACCOUNT     = "clas12"
DEFAULT_SLURM_MEM_PER_CPU = "2GB"

# Args that are always passed to using_RDataFrames_python.py
# (As requested: "-NoEvGen -f -MR")
ALWAYS_MAIN_ARGS = ["-NoEvGen", "-f", "-MR", "-e", "--event_limit", "1"]
ALWAYS_MAIN_ARGS = ["-NoEvGen", "-f", "-MR", "--event_limit", "1"]
# ALWAYS_MAIN_ARGS = ["-NoEvGen", "-f", "--event_limit", "1"]
ALWAYS_MAIN_ARGS = ["-NoEvGen", "-f", "-MR", "-e"]

JSON_DEFAULT_PATH = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json"

# Preset configurations: base name, title, base email message, etc.
PRESETS = {
    "zeroth": {
        "name_base":        "ZerothOrder",
        "title":            "Zeroth Order Acceptance Weights",
        "email_base":       "Zeroth Order Acceptance Weight batched run. No Injected Physics.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp",
        "use_json_weights": False,
        "json_file":        JSON_DEFAULT_PATH,
        "do_not_use_hpp":   False,
        "angles_only_hpp":  False,
    },
    "ao-zeroth": {
        "name_base":        "AngleOnlyZerothOrder",
        "title":            "Zeroth Order Acceptance Weights (Angles Only)",
        "email_base":       "Zeroth Order Acceptance Weight batched run. Only used the acceptance weights for the lab angles. No Momemntum weights OR Injected Physics.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp",
        "use_json_weights": False,
        "json_file":        JSON_DEFAULT_PATH,
        "do_not_use_hpp":   False,
        "angles_only_hpp":  True,
    },
    "first": {
        "name_base":        "FirstOrder",
        "title":            "First Order Modulation Weights",
        "email_base":       "First Order Injected Physics Modulation Weight batched run. No Acceptance Weights.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "do_not_use_hpp":   True,   # disable acceptance weights
        "angles_only_hpp":  False,  # No variation of physics weights only will use 'angles_only_hpp'
    },
    "first-acc": {
        "name_base":        "FirstOrderAcc",
        "title":            "#splitline{First Order Acceptance Weights}{Made with injected physics}",
        "email_base":       "First Acceptance Order Weight batched run. Uses both the Injected Physics Modulations AND Acceptance Weights.",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "do_not_use_hpp":   False,
        "angles_only_hpp":  False,
    },
    "ao-first-acc": {
        "name_base":        "AngleOnlyFirstOrderAcc",
        "title":            "#splitline{First Order Acceptance Weights (Angles Only)}{Made with injected physics}",
        "email_base":       "First Acceptance Order Weight batched run. Uses both the Injected Physics Modulations AND Acceptance Weights, but the acceptance weights only used the lab angles (not momentum).",
        "hpp_file":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp",
        "use_json_weights": True,
        "json_file":        JSON_DEFAULT_PATH,
        "do_not_use_hpp":   False,
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

def build_name_base_for_merged(preset_cfg, name_tag):
    # e.g., "ZerothOrder" or "ZerothOrder_MyTag"
    parts = [preset_cfg["name_base"]]
    if((name_tag is not None) and (name_tag != "")):
        parts.append(name_tag)
    return "_".join(parts)


def build_name_for_batch(name_base_for_merged, batch_index):
    # e.g., "ZerothOrder_MyTag_Batch01" (max groups 57 -> 2 digits is enough)
    return f"{name_base_for_merged}_Batch{batch_index:02d}"


def build_batch_root_filename(name_for_batch, output_dir):
    filename = f"{ROOT_BASE_PREFIX}{name_for_batch}.root"
    return os.path.join(output_dir, filename)


def build_merged_root_filename(name_base_for_merged, output_dir):
    filename = f"{ROOT_BASE_PREFIX}{name_base_for_merged}.root"
    return os.path.join(output_dir, filename)


def build_email_message(preset_cfg, email_extra):
    msg = preset_cfg["email_base"]
    if((email_extra is not None) and (email_extra.strip() != "")):
        msg = f"{msg}\n{email_extra}"
    return msg


def apply_common_preset_args_to_cmd(cmd_base, preset_cfg):
    # hpp file always provided
    cmd_base.extend(["-hpp", preset_cfg["hpp_file"]])

    # JSON weights / file
    if(preset_cfg.get("use_json_weights", False)):
        cmd_base.append("--json_weights")
        cmd_base.extend(["--json_file", preset_cfg.get("json_file", JSON_DEFAULT_PATH)])

    # disable acceptance weights completely
    if(preset_cfg.get("do_not_use_hpp", False)):
        cmd_base.append("--do_not_use_hpp")

    # angles-only acceptance weights
    if(preset_cfg.get("angles_only_hpp", False)):
        cmd_base.append("--angles_only_hpp")


def run_single_batch_sequential(main_script, batch_index, output_dir, preset_cfg, name_base_for_merged, email_msg):
    name_for_batch   = build_name_for_batch(name_base_for_merged, batch_index)
    batch_root_file  = build_batch_root_filename(name_for_batch, output_dir)

    cmd_base = [sys.executable, main_script, "-bID", str(batch_index)]
    cmd_base.extend(ALWAYS_MAIN_ARGS)
    cmd_base.extend(["-n", name_for_batch])
    cmd_base.extend(["-t", preset_cfg["title"]])
    cmd_base.extend(["-em", email_msg])
    apply_common_preset_args_to_cmd(cmd_base, preset_cfg)

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
        "batch_id":      batch_index,
        "returncode":    returncode,
        "root_file":     batch_root_file,
        "name_for_batch": name_for_batch,
    }


def run_batches_parallel(main_script, nbatches, output_dir, max_parallel, preset_cfg, name_base_for_merged, email_msg):
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

            print(f"\n{color.BBLUE}[INFO]{color.END} Starting batch {batch_index} in parallel (name={name_for_batch})...")
            print("       Command:", " ".join(cmd_base))
            try:
                proc = subprocess.Popen(cmd_base)
            except Exception as e:
                print(f"{color.Error}[ERROR]{color.END} Failed to start batch {batch_index}: {e}")
                results.append({
                    "batch_id":      batch_index,
                    "returncode":    1,
                    "root_file":     batch_root_file,
                    "name_for_batch": name_for_batch,
                })
                continue

            running.append({
                "batch_id":      batch_index,
                "process":       proc,
                "root_file":     batch_root_file,
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
                "batch_id":      batch_id,
                "returncode":    ret,
                "root_file":     root_file,
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
# SLURM helpers (bash sbatch, with preview + approval)
# =========================

def build_slurm_array_script_text(main_script, preset_cfg, name_base_for_merged, email_msg, nbatches, partition, time_str, account, slurm_mem_per_cpu, email_address, job_name):
    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append(f"#SBATCH --mail-user={email_address}")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append(f"#SBATCH --partition={partition}")
    lines.append(f"#SBATCH --account={account}")
    lines.append(f"#SBATCH --mem-per-cpu={slurm_mem_per_cpu}")
    lines.append(f"#SBATCH --time={time_str}")
    lines.append(f"#SBATCH --array=1-{nbatches}")
    lines.append("")
    lines.append("")
    lines.append('BATCH_ID=${SLURM_ARRAY_TASK_ID}')
    # lines.append('echo "Running batch ${BATCH_ID} on host $(hostname) at $(date)"')
    lines.append(f'NAME_BASE="{name_base_for_merged}"')

    safe_email_msg = email_msg.replace('"', '\\"')
    lines.append(f'EMAIL_MSG="{safe_email_msg}"')

    lines.append('NAME_FOR_BATCH="${NAME_BASE}_Batch${BATCH_ID}"')
    lines.append("")

    # cmd_parts = [sys.executable, main_script, "-bID", "${BATCH_ID}"]
    cmd_parts = ["srun", "python3", main_script, "-bID", "${BATCH_ID}"]
    if("-e" in ALWAYS_MAIN_ARGS):
        ALWAYS_MAIN_ARGS.remove("-e") # Do not send emails within sbatch jobs
    cmd_parts.extend(ALWAYS_MAIN_ARGS)
    cmd_parts.extend(["-n", '"${NAME_FOR_BATCH}"'])
    cmd_parts.extend(["-t", f"\"{preset_cfg['title']}\""])
    cmd_parts.extend(["-em", '"${EMAIL_MSG}"'])
    apply_common_preset_args_to_cmd(cmd_parts, preset_cfg)

    cmd_str = " ".join(cmd_parts)

    lines.append("")
    # lines.append(f'echo "Command: {cmd_str}"')
    lines.append(cmd_str)
    # lines.append('exit_code=$?')
    # lines.append('echo "Batch ${BATCH_ID} finished with exit code ${exit_code} at $(date)"')
    # lines.append("exit ${exit_code}")

    return "\n".join(lines)


def build_slurm_hadd_script_text(batch_files, merged_file, partition, time_str, account, slurm_mem_per_cpu, email_address, job_name):
    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append(f"#SBATCH --mail-user={email_address}")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append(f"#SBATCH --partition={partition}")
    lines.append(f"#SBATCH --account={account}")
    # lines.append(f"#SBATCH --mem-per-cpu={slurm_mem_per_cpu}")
    lines.append("#SBATCH --mem-per-cpu=5000")
    lines.append(f"#SBATCH --time={time_str}")
    lines.append("")
    lines.append("")
    # lines.append('echo "Starting hadd job on host $(hostname) at $(date)"')

    cmd_parts = ["$ROOTSYS/bin/hadd", "-f", merged_file] + batch_files
    cmd_str   = " ".join(cmd_parts)

    # lines.append(f'echo "Command: {cmd_str}"')
    lines.append(cmd_str)
    # lines.append('exit_code=$?')
    # lines.append('echo "hadd finished with exit code ${exit_code} at $(date)"')
    # lines.append("exit ${exit_code}")

    return "\n".join(lines)


def submit_slurm_jobs(nbatches, main_script, output_dir, partition, time_str, account, preset_cfg, name_base_for_merged, email_msg, email_address, slurm_mem_per_cpu):
    script_dir_local = os.path.dirname(os.path.abspath(__file__))

    batch_files = []
    for i in range(1, nbatches + 1):
        name_for_batch = build_name_for_batch(name_base_for_merged, i)
        batch_files.append(build_batch_root_filename(name_for_batch, output_dir))

    merged_file = build_merged_root_filename(name_base_for_merged, output_dir)

    date_str       = time.strftime("%m_%d_%Y")
    job_base       = preset_cfg["name_base"]
    array_job_name = f"{job_base}_{date_str}_running_batch_jobs"
    hadd_job_name  = f"{job_base}_{date_str}_hadd_batches"

    array_script_text = build_slurm_array_script_text(main_script, preset_cfg, name_base_for_merged, email_msg, nbatches, partition, time_str, account, slurm_mem_per_cpu, email_address, array_job_name)

    hadd_script_text = build_slurm_hadd_script_text(batch_files, merged_file, partition, time_str, account, slurm_mem_per_cpu, email_address, hadd_job_name)

    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM array script:\n")
    print(array_script_text)
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM hadd script:\n")
    print(hadd_script_text)

    try:
        response = input("\nApprove and submit these SLURM scripts? [y/N]: ").strip().lower()
    except EOFError:
        response = "n"

    if((response != "y") and (response != "yes")):
        print(f"{color.Error}[ERROR]{color.END} SLURM scripts not approved. Exiting without submission.")
        return None, None, merged_file, batch_files

    array_script_path = os.path.join(script_dir_local, "slurm_array_job.sh")
    hadd_script_path  = os.path.join(script_dir_local, "slurm_hadd_job.sh")

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

    parser.add_argument("-nb", "--nbatches", type=int, default=57, help="Number of batches (integer between 1 and 57).")
    parser.add_argument("-m", "--mode", choices=["sequential", "parallel", "slurm"], default="sequential", help="Run mode: sequential (default), parallel, or slurm.")
    parser.add_argument("-nt", "--name-tag", default=None, help="Optional name tag appended into the --name used for files (affects both batch and merged ROOT names).")
    parser.add_argument("--delete-batch-files", action="store_true", help="Delete per-batch ROOT files after successful hadd.")
    parser.add_argument("--max-parallel", type=int, default=2, help="Maximum number of parallel jobs in parallel mode.")
    parser.add_argument("-e", "--email", default=None, help="Email address for notifications (overrides DEFAULT_EMAIL).")
    parser.add_argument("--main-script", default=DEFAULT_MAIN_SCRIPT, help="Path to using_RDataFrames_python.py (or equivalent).")
    parser.add_argument("--output-dir", default=os.path.dirname(os.path.abspath(__file__)), help="Directory where batch and merged ROOT files live.")
    parser.add_argument("--slurm-partition", default=DEFAULT_SLURM_PARTITION, help="SLURM partition to use in slurm mode.")
    parser.add_argument("-st", "--slurm-time", default=DEFAULT_SLURM_TIME, help="SLURM time limit for each job in slurm mode (HH:MM:SS).")
    parser.add_argument("--slurm-account", default=DEFAULT_SLURM_ACCOUNT, help="SLURM account in slurm mode (if required by your cluster).")
    parser.add_argument("-cpu", "--slurm-mem-per-cpu", default=DEFAULT_SLURM_MEM_PER_CPU, help="SLURM memory per CPU in slurm mode (e.g. '2GB', '4000M').")
    parser.add_argument("-p", "--preset", choices=["zeroth", "ao-zeroth", "first", "first-acc", "ao-first-acc"], default="zeroth", help="Preset configuration.")
    parser.add_argument("-ee", "--email-extra", type=str, default="", help="Extra message appended to the -em email message passed to using_RDataFrames_python.py.")

    args = parser.parse_args()

    if((args.nbatches <= 0) or (args.nbatches > 57)):
        print(f"{color.Error}[ERROR]{color.END} --nbatches must be between 1 and 57 (Maximum Group Number: 57).")
        sys.exit(1)

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

    preset_cfg          = PRESETS[args.preset]
    name_base_for_merged = build_name_base_for_merged(preset_cfg, args.name_tag)
    email_msg           = build_email_message(preset_cfg, args.email_extra)

    overall_success = False
    hadd_success    = False
    delete_success  = False
    batch_failures  = []

    merged_file = build_merged_root_filename(name_base_for_merged, output_dir)

    if(args.mode == "sequential"):
        print(f"{color.BBLUE}[INFO]{color.END} Running in sequential local mode (no SLURM).")

        results = []
        for batch_idx in range(1, args.nbatches + 1):
            res = run_single_batch_sequential(main_script, batch_idx, output_dir, preset_cfg, name_base_for_merged, email_msg)
            results.append(res)

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

    elif(args.mode == "parallel"):
        print(f"{color.BBLUE}[INFO]{color.END} Running in parallel local mode (no SLURM).")
        if(args.max_parallel <= 0):
            print(f"{color.Error}[ERROR]{color.END} --max-parallel must be > 0 in parallel mode.")
            sys.exit(1)

        results = run_batches_parallel(main_script, args.nbatches, output_dir, args.max_parallel, preset_cfg, name_base_for_merged, email_msg)

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

        array_jobid, hadd_jobid, merged_file, batch_files = submit_slurm_jobs(
            args.nbatches, main_script, output_dir,
            args.slurm_partition, args.slurm_time, args.slurm_account,
            preset_cfg, name_base_for_merged, email_msg,
            email_address, args.slurm_mem_per_cpu
        )

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
    summary_lines.append("Script: run_make_ROOT_files_with_batching.py")
    summary_lines.append(f"Mode: {args.mode}")
    summary_lines.append(f"Preset: {args.preset}")
    summary_lines.append(f"Main script: {main_script}")
    summary_lines.append(f"Output directory: {output_dir}")
    summary_lines.append(f"Name base for merged file: {name_base_for_merged}")
    summary_lines.append(f"Merged ROOT file: {merged_file}")
    summary_lines.append(f"Number of batches: {args.nbatches}")
    summary_lines.append(f"Overall success: {overall_success}")
    summary_lines.append(f"hadd success: {hadd_success}")
    summary_lines.append(f"Delete batch files flag: {args.delete_batch_files}")
    summary_lines.append(f"Delete batch files success: {delete_success}")
    summary_lines.append(f"Approx. peak memory usage (children): {peak_mem_str}")

    if(len(batch_failures) > 0):
        summary_lines.append(f"Failed batches: {batch_failures}")

    summary_block = "\n".join(summary_lines)

    email_body = f"""
The 'run_make_ROOT_files_with_batching.py' script has finished running.

{start_time_str}

{summary_block}

{end_time_str}
{total_time_str}
{rate_line}
"""

    subject_status = "SUCCESS" if(overall_success) else "FAILURE"
    subject        = f"[run_make_ROOT_files_with_batching] {subject_status} ({args.mode}, N={args.nbatches}, preset={args.preset})"

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
