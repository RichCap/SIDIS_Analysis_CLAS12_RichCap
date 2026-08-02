#!/usr/bin/env python3
import os
import argparse
import subprocess
import glob
import shlex
import sys
import time
import re
from datetime import datetime

# ====================================================================================================
# Your standard import pattern (no fallback)
# ====================================================================================================
script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

SLURM_ARRAY_CHECK_DISABLED = False

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Run a command on each file in a directory or glob pattern (parallel, SLURM, or hybrid).", formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-d", "--directory",
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb*EvGen*",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/LUND_EvGen_Iterative_*{New,richcap}_No_Rad*V[0-9]*Part*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/LUND_EvGen_Iterative_*{New_V2,New_V3,Groups_Batch_[1-9],Groups_Batch_1[0-6]}_No_Rad*Part*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/LUND_EvGen_Iterative_*{richcap,New,New_V2,New_V3,Groups_Batch_[1-9],Groups_Batch_[1-2][0-9]}_No_Rad*Part*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/LUND_EvGen_Iterative_*{SBATCH_Group_Test_V1_Batch_1}_No_Rad*Part*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/LUND_EvGen_Iterative_*{richcap,New,New_V2,New_V3,Groups_Batch_[1-9],Groups_Batch_[1-2][0-9],SBATCH_Group_Test_V1_Batch_1}_No_Rad*Part*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_Group_Full_V1_Batch_*_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_{SBATCH_Group_Full_V2_Batch_[1-4],SBATCH_Large_Group_V1_Batch_[1-4]}_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_Large_Group_V[2-4]_Batch_[1-4]_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_Binned_Groups_Q2_Row_5_V1_Batch_[1-2]_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_{Refined_Binned_Groups_Q2_Row_[1-5],Binned_Groups_Q2_Row_[1-4]}_V1_Batch_[1-2]_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_Refined_Binned_Groups_Q2_Row_[1-5]_V[3-4]_Batch_1_No_Rad_Merged_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Binned_Groups_Q2_Row_*.root",
                        # default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Binned_Groups_Q2_Row_[1-5]_V2*.root",
                        default="/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_Q2_Row*No_Rad*.root",
                        type=str,
                        help="Directory path OR glob pattern of files to process. Supports explicit brace-branch patterns like '{New,richcap}'.\nDefault is the current No_Rad Old_MM_Cut production set only.\n")

    parser.add_argument("-check", "--check",
                        action="store_true",
                        help="Stop if a command exits non-zero.\n")

    parser.add_argument("-c", "--command",
                        default="lt",
                        type=str,
                        help="Command to run. The default command is just 'lt'—must at least set to 'BC_Corrections_Script.py' to run the actual code.\n")

    parser.add_argument("-e", '--email',
                        action="store_true",
                        help="Attach -e/-em to the final local completion BC_Corrections_Script.py job so its existing email is sent.\n")

    parser.add_argument("-gdf", '--clasdis',
                        action="store_true",
                        help="Runs clasdis default files instead of EvGen files (overwrites the '--directory' argument automatically).\n")

    parser.add_argument("-rm", "--run_mode",
                        default="parallel",
                        choices=["parallel", "slurm", "hybrid"],
                        help="Execution mode:\n  parallel — local concurrent jobs for indices 0..N-2, then final file N-1 locally\n  slurm    — one SLURM array task per file (array 0..N-1)\n  hybrid   — SLURM array for 0..N-2 competing with local workers, then final file N-1 locally\n")

    parser.add_argument("-j", "--max_jobs",
                        default=25,
                        type=int,
                        help="Maximum number of simultaneous local jobs (parallel/hybrid; applies to indices 0..N-2).\n")

    parser.add_argument("-rcl", "--run_context_line",
                        default="Ran in tmuxPython",
                        type=str,
                        help="Custom line to include at the end of the Email_output string (replaces the hardcoded 'Ran in tmux...' line).\n")

    parser.add_argument("-jn", "--job_name",
                        default="BC_Old_MM_Cut_No_Rad",
                        type=str,
                        help="Common SLURM array job-name stem (full name is <job_name>_<MM_DD_YYYY>).\n")

    parser.add_argument("-sm", "--slurm_mem",
                        default="3G",
                        type=str,
                        help="SLURM --mem-per-cpu (starting estimate; raise if MaxRSS/OOM requires it).\n")

    parser.add_argument("-st", "--slurm_time",
                        default="02:00:00",
                        type=str,
                        help="SLURM wall-time request. Must not exceed 24:00:00 (rejected, not silently shortened).\n")

    parser.add_argument("-y", "--yes",
                        action="store_true",
                        help="Noninteractive approval of SLURM submission (slurm/hybrid).\n")

    parser.add_argument("-ord", "--output_root_dir",
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/BC_Corrections/ROOT_Files_Output/Path_to_Volatile",
                        type=str,
                        help="Parent directory for run-specific ROOT outputs (a <run_tag> subdirectory is created).\n")

    parser.add_argument("-ld", "--log_dir",
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/BC_Corrections/BC_Log_and_Old_Files",
                        type=str,
                        help="Parent directory for run-specific logs, file lists, and SLURM scripts.\n")

    parser.add_argument("-rt", "--run_tag",
                        default="",
                        type=str,
                        help="Optional full override for the run-tag directory name used under --output_root_dir and --log_dir.\nDefault when empty: '<job_name>_<MM_DD_YYYY>' from --job_name and the submission date.\nIf set, this string fully replaces that default (job_name and date are NOT appended or combined).\nDoes not change the SLURM --job-name, which is always built as '<job_name>_<MM_DD_YYYY>' from --job_name.\n")

    parser.add_argument("-ps", "--poll_seconds",
                        default=30.0,
                        type=float,
                        help="Seconds between polls while waiting for remaining SLURM tasks (hybrid).\n")

    parser.add_argument("-ix", "--indices",
                        default="",
                        type=str,
                        help="Optional zero-based index filter for the mid-set, e.g. '0,3,10-12'. Empty means all mid-set indices.\n")

    return parser.parse_args()

def expand_brace_patterns(pattern):
    pattern = str(pattern)
    brace_start = pattern.find("{")
    if(brace_start == -1):
        return [pattern]

    depth = 0
    brace_end = -1
    for index, char in enumerate(pattern[brace_start:], start=brace_start):
        if(char == "{"):
            depth += 1
        elif(char == "}"):
            depth -= 1
            if(depth == 0):
                brace_end = index
                break

    if(brace_end == -1):
        return [pattern]

    prefix = pattern[:brace_start]
    suffix = pattern[brace_end + 1:]
    body   = pattern[brace_start + 1:brace_end]

    options = []
    current = []
    depth   = 0
    for char in body:
        if((char == ",") and (depth == 0)):
            options.append("".join(current))
            current = []
            continue
        if(char == "{"):
            depth += 1
        elif(char == "}"):
            depth -= 1
        current.append(char)
    options.append("".join(current))

    expanded_patterns = []
    for option in options:
        expanded_patterns.extend(expand_brace_patterns(f"{prefix}{option}{suffix}"))
    return expanded_patterns

def build_file_list(target):
    # Discover files from a directory or glob/brace pattern; return a deterministically sorted unique list.
    if(os.path.isdir(target)):
        files = []
        for name in os.listdir(target):
            filepath = os.path.join(target, name)
            if(not os.path.isfile(filepath)):
                continue
            # Directory discovery: keep ROOT inputs only (user globs remain fully user-controlled).
            if(not str(name).endswith(".root")):
                continue
            files.append(os.path.abspath(filepath))
        return sorted(files)

    expanded_targets = expand_brace_patterns(target)

    files = []
    seen  = set()
    for expanded_target in expanded_targets:
        for filepath in glob.glob(expanded_target):
            if(os.path.isfile(filepath)):
                abs_path = os.path.abspath(filepath)
                if(abs_path not in seen):
                    files.append(abs_path)
                    seen.add(abs_path)
    return sorted(files)

def parse_indices_spec(spec, n_files):
    # Parse '0,3,10-12' into a sorted unique list of indices in [0, n_files). Empty spec => all indices.
    if(spec is None or str(spec).strip() == ""):
        return list(range(n_files))
    out = set()
    for part in str(spec).split(","):
        part = part.strip()
        if(part == ""):
            continue
        if("-" in part):
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if(lo > hi):
                lo, hi = hi, lo
            for i in range(lo, hi + 1):
                if(0 <= i < n_files):
                    out.add(i)
        else:
            i = int(part)
            if(0 <= i < n_files):
                out.add(i)
    return sorted(out)

def submission_date_str():
    return datetime.now().strftime("%m_%d_%Y")

def make_run_tag(args):
    # Default run tag matches the SLURM job-name style: <job_name>_<MM_DD_YYYY> (no submission-time suffix).
    # Override with --run_tag if multiple runs on the same day need distinct directories.
    if(args.run_tag not in ["", None]):
        return str(args.run_tag)
    date_tag = submission_date_str()
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(args.job_name))
    return f"{safe_name}_{date_tag}"

def make_run_dirs(args, run_tag):
    root_run_dir = os.path.join(str(args.output_root_dir), run_tag)
    log_run_dir  = os.path.join(str(args.log_dir), run_tag)
    os.makedirs(root_run_dir, exist_ok=True)
    os.makedirs(log_run_dir, exist_ok=True)
    return root_run_dir, log_run_dir

def write_file_list(path, files):
    with open(path, "w") as fh:
        fh.write(f"# Generated by Run_BC_Scripts_Locally.py on {datetime.now().isoformat(timespec='seconds')}\n")
        fh.write(f"# N_files={len(files)}  (zero-based indices 0..{max(0, len(files)-1)})\n")
        for filepath in files:
            fh.write(f"{filepath}\n")

def name_insert_from_input(filepath):
    # Mirror BC_Corrections_Script.py --use_file_name basename insertion.
    name_insert = str(filepath).split("/")[-1]
    name_insert = str(name_insert.split("new6.")[-1]).replace(".hipo.root", "")
    name_insert = str(name_insert).replace(".root", "")
    return name_insert

def expected_output_path(filepath, root_run_dir, root_basename="Sub_Bin_Contents_for_BC_Correction.root"):
    name_insert = name_insert_from_input(filepath)
    if(str(root_basename).endswith(".root")):
        out_name = str(root_basename).replace(".root", f"_{name_insert}.root")
    else:
        out_name = f"{root_basename}_{name_insert}.root"
    return os.path.join(root_run_dir, out_name)

def prepare_base_command(args, root_run_dir):
    # Normalize the BC command string and return shlex-split base without the input file path.
    command = str(args.command)
    if(args.clasdis and ("BC_Corrections_Script.py" in command) and not any(clas_com in command for clas_com in ["-clasdis", "--use_clasdis"])):
        command = f"{command} --use_clasdis"
    if(("BC_Corrections_Script.py" in command) and not any(file_com in command for file_com in ["-f ", "--file ", "-f\t", "--file\t"])):
        command = f"{command.rstrip()} --file"
    # Inject --root_file_out into the run-specific directory when not already specified.
    if(("BC_Corrections_Script.py" in command) and ("--root_file_out" not in command) and (not re.search(r"(^|\s)(-rf|--root_file_out)(\s|=)", command))):
        root_out = os.path.join(root_run_dir, "Sub_Bin_Contents_for_BC_Correction.root")
        command = f"{command.rstrip()} --root_file_out {shlex.quote(root_out)}"
    args.command = command
    return shlex.split(command)

def build_bc_command(base_cmd, filepath, email_message=None):
    cmd = list(base_cmd) + [filepath]
    if(email_message is not None):
        cmd += ["-e", "-em", email_message]
    return cmd

def build_final_email_message(args, timer):
    StartTimePrint = str(timer.start_find(return_Q=True)).replace("Ran", "Started running")
    ElaspTimePrint = "\n".join(timer.time_elapsed(return_Q=True))
    return f"""This was the last file to be run with the command: 
{args.command} "files"

{StartTimePrint}
{ElaspTimePrint}

{args.run_context_line}
"""

def run_final_file(args, base_cmd, filepath, timer):
    # Always run the final file; attach child -e/-em only when email is enabled.
    Email_output = build_final_email_message(args, timer)
    if(args.email):
        cmd = build_bc_command(base_cmd, filepath, email_message=Email_output)
    else:
        cmd = build_bc_command(base_cmd, filepath, email_message=None)
    print(f"\n{color.BBLUE}FINAL FILE (index last): {color.END}{os.path.basename(filepath)}")
    print(f"  CMD: {' '.join(shlex.quote(x) for x in cmd)}")
    result = subprocess.run(cmd, check=False)
    print(f"\n{color.BBLUE}{Email_output}{color.END}\n")
    if((result.returncode != 0) and args.check):
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result.returncode

def parse_slurm_time_to_seconds_and_validate(time_str):
    # Parse SLURM-style time: MM, HH:MM:SS, DD-HH:MM:SS, or M:SS. Reject values above 24 hours.
    text = str(time_str).strip()
    seconds = None
    m = re.fullmatch(r"(\d+)-(\d+):(\d+):(\d+)", text)
    if(m):
        days, hours, mins, secs = [int(x) for x in m.groups()]
        seconds = (((days * 24 + hours) * 60) + mins) * 60 + secs
    if(seconds is None):
        m = re.fullmatch(r"(\d+):(\d+):(\d+)", text)
        if(m):
            hours, mins, secs = [int(x) for x in m.groups()]
            seconds = ((hours * 60) + mins) * 60 + secs
    if(seconds is None):
        m = re.fullmatch(r"(\d+):(\d+)", text)
        if(m):
            mins, secs = [int(x) for x in m.groups()]
            seconds = mins * 60 + secs
    if(seconds is None):
        m = re.fullmatch(r"(\d+)", text)
        if(m):
            seconds = int(m.group(1)) * 60
    if(seconds is None):
        raise ValueError(f"Could not parse --slurm_time '{time_str}'. Use HH:MM:SS (or DD-HH:MM:SS).")
    if(seconds > (24 * 3600)):
        raise ValueError(f"--slurm_time '{time_str}' exceeds the maximum allowed 24:00:00. Rejecting (not silently shortened).")
    return seconds

def build_slurm_job_name(args):
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(args.job_name))
    return f"{safe_name}_{submission_date_str()}"

def write_slurm_array_script(args, script_path, file_list_path, base_cmd, array_lo, array_hi, root_run_dir, log_run_dir):
    # Write a SLURM array script covering indices array_lo..array_hi inclusive (task id == file index).
    job_name = build_slurm_job_name(args)
    n_tasks  = array_hi - array_lo + 1
    if(n_tasks < 1):
        raise ValueError("SLURM array range is empty.")
    array_spec = f"{array_lo}-{array_hi}"
    cmd_prefix = " ".join([shlex.quote(x) for x in base_cmd])
    work_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/BC_Corrections"

    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append("#SBATCH --mail-user=richard.capobianco@uconn.edu")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append("#SBATCH --partition=production")
    lines.append("#SBATCH --account=clas12")
    lines.append(f"#SBATCH --mem-per-cpu={args.slurm_mem}")
    lines.append(f"#SBATCH --time={args.slurm_time}")
    lines.append(f"#SBATCH --array={array_spec}")
    lines.append("")
    lines.append(f'cd "{work_dir}"')
    lines.append(f'FILE_LIST="{file_list_path}"')
    lines.append('TASK_ID="${SLURM_ARRAY_TASK_ID}"')
    lines.append('FILE=$(awk -v id="${TASK_ID}" \'!/^#/ && NF {if (n++ == id) {print; exit}}\' "${FILE_LIST}")')
    lines.append('if [[ -z "${FILE}" ]]; then echo "ERROR: No file for SLURM_ARRAY_TASK_ID=${TASK_ID} in ${FILE_LIST}"; exit 1; fi')
    lines.append('echo "=============================================="')
    lines.append('echo "SLURM_ARRAY_TASK_ID=${TASK_ID}"')
    lines.append('echo "input=${FILE}"')
    lines.append(f'echo "command_prefix={cmd_prefix}"')
    lines.append(f'echo "ROOT_RUN_DIR={root_run_dir}"')
    lines.append(f'echo "LOG_RUN_DIR={log_run_dir}"')
    lines.append('echo "=============================================="')
    lines.append(f'{cmd_prefix} "${{FILE}}"')
    lines.append('exit $?')
    lines.append("")

    with open(script_path, "w") as fh:
        fh.write("\n".join(lines))
    os.chmod(script_path, 0o755)
    return job_name, array_spec

def preview_file(path, label="script"):
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed {label}: {path}\n")
    with open(path, "r") as fh:
        print(fh.read())

def approve_submission(args):
    if(args.yes):
        print(f"{color.BBLUE}[INFO]{color.END} --yes set: auto-approving SLURM submission.")
        return True
    try:
        response = input("\nApprove and submit this SLURM array script? [y/N]: ").strip().lower()
    except EOFError:
        response = "n"
    return response in ["y", "yes"]

def submit_sbatch(script_path):
    proc = subprocess.run(["sbatch", "--parsable", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if(proc.returncode != 0):
        msg = proc.stderr.strip() if(proc.stderr.strip() not in [""]) else proc.stdout.strip()
        raise RuntimeError(f"sbatch failed for {script_path}: {msg}")
    job_id = proc.stdout.strip().split(";")[0].strip()
    if(job_id in [""]):
        raise RuntimeError(f"sbatch returned an empty job id for {script_path}")
    return job_id

def query_slurm_array_task_state(array_jobid, batch_index):
    # Return SLURM state code (e.g. PD, R), None if absent, or 'IGNORE' if squeue is unusable.
    global SLURM_ARRAY_CHECK_DISABLED
    if(SLURM_ARRAY_CHECK_DISABLED):
        return "IGNORE"
    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid), "-o", "%i %t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} squeue not found; disabling SLURM local coordination.")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    except Exception as exc:
        print(f"{color.Error}[WARNING]{color.END} Exception while running squeue for array job {array_jobid}: {exc}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    if(proc.returncode != 0):
        msg = proc.stderr.strip() if(proc.stderr.strip() not in [""]) else "(no additional message from squeue)"
        print(f"{color.Error}[WARNING]{color.END} squeue for array job {array_jobid} returned code {proc.returncode}: {msg}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    target_id = f"{array_jobid}_{batch_index}"
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if(len(parts) < 2):
            continue
        if(parts[0] == target_id):
            return parts[1]
    return None

def cancel_slurm_array_task(array_jobid, batch_index):
    job_str = f"{array_jobid}_{batch_index}"
    try:
        proc = subprocess.run(["scancel", job_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} scancel not found; cannot cancel SLURM array task {job_str}.")
        return False
    except Exception as exc:
        print(f"{color.Error}[WARNING]{color.END} Exception while running scancel on {job_str}: {exc}")
        return False
    if(proc.returncode != 0):
        msg = proc.stderr.strip() if(proc.stderr.strip() not in [""]) else "(no additional message from scancel)"
        print(f"{color.Error}[WARNING]{color.END} scancel {job_str} failed with code {proc.returncode}: {msg}")
        return False
    print(f"{color.BBLUE}[INFO]{color.END} Cancelled SLURM array task {job_str} (state was pending).")
    return True

def slurm_array_has_active_tasks(array_jobid):
    global SLURM_ARRAY_CHECK_DISABLED
    if(array_jobid in [None, ""]):
        return False
    if(SLURM_ARRAY_CHECK_DISABLED):
        return False
    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"{color.Error}[WARNING]{color.END} squeue not found; cannot check active tasks for SLURM array job {array_jobid}.")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False
    except Exception as exc:
        print(f"{color.Error}[WARNING]{color.END} Exception while checking active tasks for SLURM array job {array_jobid}: {exc}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False
    if(proc.returncode != 0):
        msg = proc.stderr.strip() if(proc.stderr.strip() not in [""]) else "(no additional message from squeue)"
        print(f"{color.Error}[WARNING]{color.END} squeue for array job {array_jobid} returned code {proc.returncode}: {msg}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False
    return any(line.strip() not in [""] for line in proc.stdout.splitlines())

def wait_until_slurm_idle(array_jobid, poll_seconds=30.0):
    if(array_jobid in [None, ""]):
        return
    while(slurm_array_has_active_tasks(array_jobid)):
        print(f"{color.BBLUE}[INFO]{color.END} Waiting for remaining SLURM tasks of array job {array_jobid}...")
        time.sleep(max(1.0, float(poll_seconds)))
    print(f"{color.BGREEN}[INFO]{color.END} No active SLURM tasks remain for array job {array_jobid}.")

def should_start_local_hybrid_job(array_jobid, job_index):
    # Hybrid ownership (squeue-based): PD -> cancel then local; active/absent/IGNORE -> skip local.
    state = query_slurm_array_task_state(array_jobid, job_index)
    if(state == "IGNORE"):
        print(f"{color.BYELLOW}[INFO]{color.END} SLURM state checks unusable; skipping local start for index {job_index} to avoid double-processing.")
        return False
    if(state is None):
        print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {array_jobid}_{job_index} not in queue; skipping local start.")
        return False
    if(state == "PD"):
        print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {array_jobid}_{job_index} is pending; attempting cancel for local processing.")
        cancelled = cancel_slurm_array_task(array_jobid, job_index)
        if(not cancelled):
            print(f"{color.BYELLOW}[INFO]{color.END} Could not safely cancel {array_jobid}_{job_index}; skipping local start.")
            return False
        return True
    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {array_jobid}_{job_index} is in state '{state}'; skipping local start.")
    return False

def main():

    args = parse_args()
    timer = RuntimeTimer()
    timer.start()

    target = args.directory if(not args.clasdis) else "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.*clasdis*"

    # Build file list from either directory or glob/brace-expanded glob (shared by all modes).
    files = build_file_list(target)

    if(not files):
        print(f"Error: no files found for '{target}'")
        timer.stop()
        return 1

    run_tag = make_run_tag(args)
    args.run_tag = run_tag
    root_run_dir, log_run_dir = make_run_dirs(args, run_tag)
    file_list_path = os.path.join(log_run_dir, "input_files.txt")
    write_file_list(file_list_path, files)
    n_files = len(files)

    print(f"""
{color.BGREEN}Discovered {n_files} input file(s){color.END}
    Pattern / target : {target}
    Ordered list     : {file_list_path}
    Index range      : 0..{n_files-1}
    Pure SLURM array : 0-{n_files-1}
    Hybrid mid array : 0-{n_files-2 if(n_files >= 2) else 'N/A'} (final index local)
    Run tag          : {run_tag}
    ROOT outputs     : {root_run_dir}
    Logs             : {log_run_dir}
""")

    base_cmd = prepare_base_command(args, root_run_dir)

    if(args.run_mode == "parallel"):

        max_jobs = int(args.max_jobs)
        if(max_jobs < 1):
            max_jobs = 1

        # Per-file local logs live under the run-specific log directory.
        log_dir_run = log_run_dir
        os.makedirs(log_dir_run, exist_ok=True)

        # Final-job design: run indices 0..N-2 in the parallel queue, wait, then run index N-1 locally.
        # Email (-e/-em) is attached only to that final child job when --email is set.
        mid_indices = list(range(0, max(0, n_files - 1)))
        if(args.indices not in ["", None]):
            requested = set(parse_indices_spec(args.indices, n_files))
            mid_indices = [i for i in mid_indices if(i in requested)]

        parallel_email_text = f"""
{color.BBLUE}Parallel mode enabled{color.END}
    Max Concurrent jobs    = {max_jobs}
    Log Output Directory   = {log_dir_run}
    ROOT Output Directory  = {root_run_dir}
    Number of Files        = {n_files}
    Mid-set indices        = 0..{n_files-2 if(n_files >= 2) else 'N/A'} ({len(mid_indices)} jobs)
    Final index            = {n_files-1 if(n_files >= 1) else 'N/A'} (local completion job)
"""
        print(parallel_email_text)
        args.run_context_line = f"{args.run_context_line}\n{parallel_email_text}"
        
        running = []  # list of dicts: {"proc":..., "fh":..., "log":..., "filepath":..., "num":...}
        num_started = 0
        num_done    = 0
        num_fail    = 0
        failed_indices = []

        def start_job(job_num, filepath):
            command = base_cmd + [filepath]
            base    = os.path.basename(filepath).replace(" ", "_")
            log_p   = os.path.join(log_dir_run, f"job_{job_num:05d}_{base}.log")
            expected = expected_output_path(filepath, root_run_dir)
            fh      = open(log_p, "w")
            fh.write(f"# index={job_num} of 0..{n_files-1}\n")
            fh.write(f"# input={filepath}\n")
            fh.write(f"# expected_output={expected}\n")
            fh.write(f"# command={' '.join(shlex.quote(x) for x in command)}\n")
            fh.flush()
            proc    = subprocess.Popen(command, stdout=fh, stderr=fh)
            running.append({"proc": proc, "fh": fh, "log": log_p, "filepath": filepath, "num": job_num})
            # Original style (1-based progress count of N files):
            print(f"{color.BCYAN}START{color.END}: {job_num+1:>3.0f} of {len(files)}  ->  {base}")
            # Alternate zero-based index form: print(f"{color.BCYAN}START{color.END}: index {job_num:>3d} of 0..{n_files-1}  ->  {base}")
            return

        def finish_job(item, rc):
            nonlocal num_done
            nonlocal num_fail
            num_done += 1
            try:
                item["fh"].close()
            except Exception:
                pass
            base = os.path.basename(item["filepath"]).replace(" ", "_")
            if(rc == 0):
                print(f"{color.BGREEN}DONE {color.END}: {item['num']+1:>3.0f} of {len(files)}  ->  {base}")
                # Alternate: print(f"{color.BGREEN}DONE {color.END}: index {item['num']:>3d} of 0..{n_files-1}  ->  {base}")
            else:
                num_fail += 1
                failed_indices.append(item["num"])
                print(f"{color.Error}FAIL {color.END}: {item['num']+1:>3.0f} of {len(files)}  ->  {base} (rc={rc})")
                # Alternate: print(f"{color.Error}FAIL {color.END}: index {item['num']:>3d} of 0..{n_files-1}  ->  {base} (rc={rc})")
                print(f"\tlog: {item['log']}")
            return

        def terminate_all():
            for item in running:
                try:
                    if(item["proc"].poll() is None):
                        item["proc"].terminate()
                except Exception:
                    pass
            time.sleep(0.5)
            for item in running:
                try:
                    if(item["proc"].poll() is None):
                        item["proc"].kill()
                except Exception:
                    pass
                try:
                    item["fh"].close()
                except Exception:
                    pass
            return

        # Was: for num, filepath in enumerate(files_to_run):
        for num in mid_indices:
            filepath = files[num]

            while(len(running) >= max_jobs):
                finished_index = None
                finished_rc    = None
                for ii, item in enumerate(running):
                    rc = item["proc"].poll()
                    if(rc is not None):
                        finished_index = ii
                        finished_rc    = rc
                        break
                if(finished_index is None):
                    time.sleep(0.10)
                    continue

                finished_item = running.pop(finished_index)
                finish_job(finished_item, finished_rc)
                if((finished_rc != 0) and args.check):
                    terminate_all()
                    print(f"\n{color.Error}Stopping early due to --check (a parallel job failed).{color.END}\n")
                    timer.stop()
                    return 1

            start_job(num, filepath)
            num_started += 1

        while(len(running) > 0):
            finished_index = None
            finished_rc    = None
            for ii, item in enumerate(running):
                rc = item["proc"].poll()
                if(rc is not None):
                    finished_index = ii
                    finished_rc    = rc
                    break
            if(finished_index is None):
                time.sleep(0.10)
                continue

            finished_item = running.pop(finished_index)
            finish_job(finished_item, finished_rc)
            if((finished_rc != 0) and args.check):
                terminate_all()
                print(f"\n{color.Error}Stopping early due to --check (a parallel job failed).{color.END}\n")
                timer.stop()
                return 1

        # Final completion job: always run the last file; attach -e/-em only when --email is set.
        # Previous behavior only ran the final file inside `if(args.email):` — that skip is fixed here.
        if(n_files > 0):
            final_rc = run_final_file(args, base_cmd, files[-1], timer)
            if(final_rc != 0):
                num_fail += 1
                failed_indices.append(n_files - 1)

        print("\n\nCommands are Complete\n")
        if(failed_indices):
            print(f"{color.Error}Failed indices ({len(failed_indices)}): {failed_indices}{color.END}")
        timer.stop()
        return 1 if(num_fail > 0) else 0

    # Sequential mode removed (use --run_mode parallel|slurm|hybrid only).
    # Original sequential progress print formatting preserved for reference:
    # print(f"""\n\n{color.BGREEN}{color_bg.YELLOW}
    # \t                   \t   
    # \tRan {color.END_B}{color.UNDERLINE}{color_bg.YELLOW}{num:>3.0f}{color.END}{color_bg.YELLOW}{color.BGREEN} of {color.END_B}{color.UNDERLINE}{color_bg.YELLOW}{len(files)}{color.END}{color_bg.YELLOW}{color.BGREEN} Files.\t   
    # \t                   \t   
    # {color.END}""")

    elif(args.run_mode == "slurm"):
        try:
            parse_slurm_time_to_seconds_and_validate(args.slurm_time)
        except ValueError as exc:
            print(f"{color.Error}ERROR:{color.END} {exc}")
            timer.stop()
            return 1
        script_path = os.path.join(log_run_dir, f"slurm_array_{run_tag}.sh")
        job_name, array_spec = write_slurm_array_script(args, script_path, file_list_path, base_cmd, 0, n_files - 1, root_run_dir, log_run_dir)
        print(f"""
{color.BBLUE}SLURM mode{color.END}
    Files discovered       = {n_files}
    Array range            = {array_spec}
    Job name               = {job_name}
    mem-per-cpu            = {args.slurm_mem}
    time                   = {args.slurm_time}
    File list              = {file_list_path}
    Script                 = {script_path}
    ROOT Output Directory  = {root_run_dir}
    Log Directory          = {log_run_dir}
""")
        preview_file(script_path, label="SLURM array script")
        if(not approve_submission(args)):
            print(f"{color.Error}[ERROR]{color.END} SLURM script not approved. Exiting without submission.")
            timer.stop()
            return 0
        array_id = submit_sbatch(script_path)
        jobid_path = os.path.join(log_run_dir, "slurm_array_jobid.txt")
        with open(jobid_path, "w") as fh:
            fh.write(f"{array_id}\n")
        print(f"{color.BGREEN}Submitted SLURM array job {array_id}{color.END} (id saved to {jobid_path})")
        print(f"{color.BBLUE}[INFO]{color.END} Merge/JSON/plots remain manual after all array tasks succeed.")
        timer.stop()
        return 0

    elif(args.run_mode == "hybrid"):
        try:
            parse_slurm_time_to_seconds_and_validate(args.slurm_time)
        except ValueError as exc:
            print(f"{color.Error}ERROR:{color.END} {exc}")
            timer.stop()
            return 1

        max_jobs = int(args.max_jobs)
        if(max_jobs < 1):
            max_jobs = 1
        log_dir_run = log_run_dir
        os.makedirs(log_dir_run, exist_ok=True)

        if(n_files == 1):
            mid_indices = []
            array_lo, array_hi = None, None
        else:
            mid_indices = list(range(0, n_files - 1))
            array_lo, array_hi = 0, n_files - 2
        if(args.indices not in ["", None]):
            requested = set(parse_indices_spec(args.indices, n_files))
            mid_indices = [i for i in mid_indices if(i in requested)]

        hybrid_email_text = f"""
{color.BBLUE}Hybrid mode enabled{color.END}
    Max Concurrent local jobs = {max_jobs}
    Log Output Directory      = {log_dir_run}
    ROOT Output Directory     = {root_run_dir}
    Number of Files           = {n_files}
    SLURM competitive indices = 0..{n_files-2 if(n_files >= 2) else 'N/A'}
    Final index               = {n_files-1 if(n_files >= 1) else 'N/A'} (local completion job only)
"""
        print(hybrid_email_text)
        args.run_context_line = f"{args.run_context_line}\n{hybrid_email_text}"

        array_id = None
        num_fail = 0
        failed_indices = []
        skipped_indices = []

        if(array_lo is not None):
            script_path = os.path.join(log_run_dir, f"slurm_array_{run_tag}.sh")
            job_name, array_spec = write_slurm_array_script(args, script_path, file_list_path, base_cmd, array_lo, array_hi, root_run_dir, log_run_dir)
            print(f"  Hybrid SLURM array range = {array_spec}")
            print(f"  Job name                 = {job_name}")
            preview_file(script_path, label="hybrid SLURM array script")
            if(not approve_submission(args)):
                print(f"{color.Error}[ERROR]{color.END} SLURM script not approved. Exiting without hybrid run.")
                timer.stop()
                return 0
            array_id = submit_sbatch(script_path)
            jobid_path = os.path.join(log_run_dir, "slurm_array_jobid.txt")
            with open(jobid_path, "w") as fh:
                fh.write(f"{array_id}\n")
            print(f"{color.BGREEN}Submitted hybrid SLURM array job {array_id}{color.END}")

            running = []
            pending = list(mid_indices)

            def start_job(job_num, filepath):
                command = base_cmd + [filepath]
                base    = os.path.basename(filepath).replace(" ", "_")
                log_p   = os.path.join(log_dir_run, f"job_{job_num:05d}_{base}.log")
                expected = expected_output_path(filepath, root_run_dir)
                fh      = open(log_p, "w")
                fh.write(f"# index={job_num} of 0..{n_files-1}\n")
                fh.write(f"# input={filepath}\n")
                fh.write(f"# expected_output={expected}\n")
                fh.write(f"# command={' '.join(shlex.quote(x) for x in command)}\n")
                fh.flush()
                proc = subprocess.Popen(command, stdout=fh, stderr=fh)
                running.append({"proc": proc, "fh": fh, "log": log_p, "filepath": filepath, "num": job_num})
                print(f"{color.BCYAN}START{color.END}: {job_num+1:>3.0f} of {len(files)}  ->  {base}")

            def finish_job(item, rc):
                nonlocal num_fail
                try:
                    item["fh"].close()
                except Exception:
                    pass
                base = os.path.basename(item["filepath"]).replace(" ", "_")
                if(rc == 0):
                    print(f"{color.BGREEN}DONE {color.END}: {item['num']+1:>3.0f} of {len(files)}  ->  {base}")
                else:
                    num_fail += 1
                    failed_indices.append(item["num"])
                    print(f"{color.Error}FAIL {color.END}: {item['num']+1:>3.0f} of {len(files)}  ->  {base} (rc={rc})")
                    print(f"\tlog: {item['log']}")

            def terminate_all():
                for item in running:
                    try:
                        if(item["proc"].poll() is None):
                            item["proc"].terminate()
                    except Exception:
                        pass
                time.sleep(0.5)
                for item in running:
                    try:
                        if(item["proc"].poll() is None):
                            item["proc"].kill()
                    except Exception:
                        pass
                    try:
                        item["fh"].close()
                    except Exception:
                        pass

            while((len(pending) > 0) or (len(running) > 0)):
                while((len(pending) > 0) and (len(running) < max_jobs)):
                    job_num = pending.pop(0)
                    if(not should_start_local_hybrid_job(array_id, job_num)):
                        skipped_indices.append(job_num)
                        print(f"{color.BBLUE}SKIP {color.END}: {job_num+1:>3.0f} of {len(files)}  (owned by SLURM or uninspectable)")
                        continue
                    start_job(job_num, files[job_num])

                if(len(running) == 0):
                    if(len(pending) == 0):
                        break
                    continue

                finished_index = None
                finished_rc = None
                for ii, item in enumerate(running):
                    rc = item["proc"].poll()
                    if(rc is not None):
                        finished_index = ii
                        finished_rc = rc
                        break
                if(finished_index is None):
                    time.sleep(0.10)
                    continue
                finished_item = running.pop(finished_index)
                finish_job(finished_item, finished_rc)
                if((finished_rc != 0) and args.check):
                    terminate_all()
                    print(f"\n{color.Error}Stopping early due to --check (a hybrid local job failed).{color.END}\n")
                    timer.stop()
                    return 1

            wait_until_slurm_idle(array_id, poll_seconds=args.poll_seconds)

        if(n_files > 0):
            final_rc = run_final_file(args, base_cmd, files[-1], timer)
            if(final_rc != 0):
                num_fail += 1
                failed_indices.append(n_files - 1)

        print("\n\nCommands are Complete\n")
        if(failed_indices):
            print(f"{color.Error}Failed indices ({len(failed_indices)}): {failed_indices}{color.END}")
        if(skipped_indices):
            print(f"{color.BBLUE}Skipped indices ({len(skipped_indices)}): {skipped_indices}{color.END}")
        timer.stop()
        return 1 if(num_fail > 0) else 0

    else:
        print(f"{color.Error}ERROR:{color.END} Unknown --run_mode '{args.run_mode}'")
        timer.stop()
        return 1

if(__name__ == "__main__"):
    sys.exit(main() or 0)
    