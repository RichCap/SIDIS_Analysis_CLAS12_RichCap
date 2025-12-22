#!/usr/bin/env python3

import argparse
import glob
import os
import shutil
import socket
import subprocess
import sys
import time
import re
from datetime import datetime

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

timer = RuntimeTimer()

SLURM_ARRAY_CHECK_DISABLED = False

EMAIL_TO                  = "richard.capobianco@uconn.edu"
DEFAULT_PATHS_DIR         = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy"
PLACEHOLDER_GROOVY_SCRIPT = "placeholder/path/to/groovy/scripts.not_defined"

DEFAULT_SLURM_TIME        = "20:00:00"
DEFAULT_SLURM_MEM_PER_CPU = "3GB"
DEFAULT_SLURM_PARTITION   = "production"
DEFAULT_SLURM_ACCOUNT     = "clas12"

# Output directories (per your provided locations)
OUTPUT_DIR_DATA           = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/"
OUTPUT_DIR_GEN_MC         = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"
OUTPUT_DIR_REC_MC         = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/"


def date_tag_m_d_yyyy():
    dt = datetime.now()
    return f"{dt.month}_{dt.day}_{dt.year}"


def normalize_source(src_in):
    if((src_in is None) or (str(src_in).strip() == "")):
        return "clasdis"
    ss = str(src_in).strip().lower()
    if(ss == "rdf"):
        ss = "data"
    if(ss not in ["clasdis", "evgen", "data"]):
        print(f"{color.RED}WARNING: Unrecognized --source value '{src_in}'. Defaulting to 'clasdis'.{color.END}")
        ss = "clasdis"
    return ss


def normalize_mc_type(mc_in):
    if((mc_in is None) or (str(mc_in).strip() == "")):
        return "mdf"
    mm = str(mc_in).strip().lower()
    if(mm in ["rec", "mdf"]):
        return "mdf"
    if(mm in ["gen", "gdf"]):
        return "gdf"
    print(f"{color.RED}WARNING: Unrecognized --mc-type value '{mc_in}'. Defaulting to 'mdf'.{color.END}")
    return "mdf"


def normalize_event_type(evt_in):
    if((evt_in is None) or (str(evt_in).strip() == "")):
        return "epipX"
    ee = str(evt_in).strip()
    eel = ee.lower()
    if(eel in ["sidis", "epipx"]):
        return "epipX"
    if(eel in ["exclusive", "epipn"]):
        return "epipN"
    if(eel in ["proton", "eppipx"]):
        return "eppipX"
    if(eel in ["dp", "epippimx"]):
        return "epippimX"
    print(f"{color.RED}WARNING: Unrecognized --event-type value '{evt_in}'. Defaulting to 'epipX'.{color.END}")
    return "epipX"


def default_paths_txt_for_source(source_norm):
    paths_map = {
        "clasdis": os.path.join(DEFAULT_PATHS_DIR, "Paths_to_MC_clasdis_files_all.txt"),
        "evgen":   os.path.join(DEFAULT_PATHS_DIR, "Paths_to_MC_EvGen_files_all.txt"),
        "data":    os.path.join(DEFAULT_PATHS_DIR, "Paths_to_REAL_Data_files_all.txt"),
    }
    return paths_map.get(source_norm, paths_map["clasdis"])


def build_default_job_id(source_norm, mc_type_norm, event_type_norm, mode):
    if(source_norm == "data"):
        file_type = "Data"
    else:
        file_type = "MC_Rec" if(mc_type_norm == "mdf") else "MC_Gen"
    src_tag = source_norm
    evt_tag = "epipX" if(source_norm == "evgen") else event_type_norm
    job_id  = f"{file_type}_{evt_tag}_{src_tag}_{date_tag_m_d_yyyy()}"
    if(mode == "sequential"):
        job_id = f"{job_id}_Seq"
    return job_id


def resolve_output_dir_from_presets(source_norm, mc_type_norm):
    if(source_norm == "data"):
        return OUTPUT_DIR_DATA
    # clasdis/evgen -> decide by MC type
    if(mc_type_norm == "gdf"):
        return OUTPUT_DIR_GEN_MC
    return OUTPUT_DIR_REC_MC


def is_placeholder_path(path_in):
    if(path_in is None):
        return True
    pp = str(path_in).strip()
    if(pp == ""):
        return True
    if(pp == PLACEHOLDER_GROOVY_SCRIPT):
        return True
    if(pp.startswith("placeholder/")):
        return True
    return False


def read_globs_from_txt(txt_path):
    if((txt_path is None) or (str(txt_path).strip() == "")):
        return None
    txt_path = os.path.expanduser(os.path.expandvars(str(txt_path).strip()))
    if(not os.path.isfile(txt_path)):
        return None
    globs_list = []
    with open(txt_path, "r") as txt_in:
        for raw_line in txt_in:
            line = raw_line.strip()
            if((line == "") or (line.startswith("#"))):
                continue
            globs_list.append(line)
    if(len(globs_list) == 0):
        return None
    return globs_list


def expand_globs_to_files(globs_list):
    expanded  = []
    unmatched = []
    if((globs_list is None) or (len(globs_list) == 0)):
        return expanded, unmatched
    for gg in globs_list:
        matches = sorted(glob.glob(gg))
        if(len(matches) > 0):
            expanded.extend(matches)
        else:
            unmatched.append(gg)
    return expanded, unmatched


def dedupe_keep_order(paths_list):
    if((paths_list is None) or (len(paths_list) == 0)):
        return []
    seen  = set()
    out   = []
    for pth in paths_list:
        if(pth in seen):
            continue
        seen.add(pth)
        out.append(pth)
    return out


def resolve_groovy_script_from_presets(source_norm, mc_type_norm, event_type_norm):
    # IMPORTANT: You will replace these placeholders with real Groovy scripts later.
    # Explicitly kept generic so they are easy to search for and so undefined options are obvious.
    presets = {
        "clasdis": {
            "mdf": {"epipX":    "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matched_TTree_epip_Batch_New.groovy",
                    "epipN":    PLACEHOLDER_GROOVY_SCRIPT,
                    "eppipX":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matched_TTree_epip_Proton_Batch_New.groovy",
                    "epippimX": "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matched_TTree_epip_Pim_Batch_New.groovy"},
            "gdf": {"epipX":    "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy",
                    "epipN":    PLACEHOLDER_GROOVY_SCRIPT,
                    "eppipX":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Proton_Batch_Pass2_UpToDate.groovy",
                    "epippimX": "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Pim_Batch_Pass2_UpToDate.groovy"},
        },
        "evgen": {
            "mdf":              "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matched_EvGen_epip_Batch.groovy",
            "gdf":              "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_EvGen.groovy",
        },
        "data": {
            "epipX":            "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_TTree_epip_Batch_Pass2.groovy",
            "epipN":            PLACEHOLDER_GROOVY_SCRIPT,
            "eppipX":           "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_TTree_epip_Proton_Batch_Pass2_New.groovy",
            "epippimX":         "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_TTree_epip_Pim_Batch_Pass2.groovy",
        },
    }

    if(source_norm == "evgen"):
        return presets["evgen"].get(mc_type_norm, PLACEHOLDER_GROOVY_SCRIPT)

    if(source_norm == "data"):
        return presets["data"].get(event_type_norm, PLACEHOLDER_GROOVY_SCRIPT)

    # clasdis
    if(source_norm not in presets):
        return PLACEHOLDER_GROOVY_SCRIPT
    if(mc_type_norm not in presets[source_norm]):
        return PLACEHOLDER_GROOVY_SCRIPT
    return presets[source_norm][mc_type_norm].get(event_type_norm, PLACEHOLDER_GROOVY_SCRIPT)


def ansi_strip(text):
    if(text is None):
        return ""
    tt = str(text)
    tt = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', tt)
    return tt


def send_email(subject, body, recipient, dry_run=False):
    if(dry_run):
        print(f"\n--- DRY RUN: email would be sent ---\nTo: {recipient}\nSubject: {subject}\n{body}\n--- END DRY RUN ---\n")
        return 0
    try:
        clean_body = ansi_strip(body)
        proc = subprocess.run(["mail", "-s", str(subject), str(recipient)], input=clean_body.encode(), check=False)
        return int(proc.returncode) if(hasattr(proc, "returncode")) else 0
    except FileNotFoundError:
        print(f"{color.Error}WARNING: 'mail' command not found; cannot send email.{color.END}")
        return 1
    except Exception as exc:
        print(f"{color.Error}WARNING: Exception while running mail: {exc}{color.END}")
        return 1


def parse_unique_batches_string(unique_str, max_batch):
    if(unique_str is None):
        return None
    s = str(unique_str).strip()
    if(s == ""):
        return None
    s = s.replace(" ", "")
    if("%" in s):
        s = s.split("%", 1)[0].strip()
        if(s == ""):
            return None
    selected = set()
    bad_tokens = []
    for token in s.split(","):
        if((token is None) or (token == "")):
            continue
        step_val = 1
        if(":" in token):
            left, step_str = token.split(":", 1)
            token = left
            try:
                step_val = int(step_str)
                if(step_val <= 0):
                    step_val = 1
            except Exception:
                step_val = 1
        if("-" in token):
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
            if(a > b):
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
    in_range  = sorted([v for v in selected if((v >= 1) and (v <= max_batch))])
    out_range = sorted([v for v in selected if((v < 1) or (v > max_batch))])
    if(len(out_range) > 0):
        print(f"{color.Error}[WARNING]{color.END} Some --unique_batches values are outside [1, {max_batch}] and will be ignored: {out_range}")
    if(len(in_range) == 0):
        return []
    return in_range


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
    except Exception as exc:
        print(f"{color.Error}[WARNING]{color.END} Exception while running squeue for array job {array_jobid}: {exc}")
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
        if((job_id == target_id)):
            return state
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
        msg = proc.stderr.strip()
        if(msg == ""):
            msg = "(no additional message from squeue)"
        print(f"{color.Error}[WARNING]{color.END} squeue for array job {array_jobid} returned code {proc.returncode}: {msg}")
        SLURM_ARRAY_CHECK_DISABLED = True
        return False
    output = proc.stdout.strip()
    if(output == ""):
        return False
    return True


def build_slurm_array_script_text(script_path, manifest_path, job_name, email_address, slurm_time, slurm_mem_per_cpu, slurm_partition, slurm_account, array_spec, work_dir):
    safe_script_path   = str(script_path).replace('"', '\\"')
    safe_manifest_path = str(manifest_path).replace('"', '\\"')
    safe_email_address = str(email_address).replace('"', '\\"')
    safe_work_dir      = str(work_dir).replace('"', '\\"')

    lines = []
    lines.append("#!/bin/bash")
    lines.append("#SBATCH --ntasks=1")
    lines.append(f"#SBATCH --job-name={job_name}")
    lines.append("#SBATCH --mail-type=ALL")
    lines.append(f"#SBATCH --mail-user={safe_email_address}")
    lines.append("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out")
    lines.append("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err")
    lines.append("#SBATCH --partition=production")
    lines.append("#SBATCH --account=clas12")
    lines.append(f"#SBATCH --mem-per-cpu={slurm_mem_per_cpu}")
    lines.append(f"#SBATCH --time={slurm_time}")
    lines.append(f"#SBATCH --array={array_spec}")
    lines.append("")
    lines.append('TASK_ID="${SLURM_ARRAY_TASK_ID}"')
    lines.append(f'MANIFEST="{safe_manifest_path}"')
    lines.append(f'GROOVY_SCRIPT="{safe_script_path}"')
    lines.append(f'WORK_DIR="{safe_work_dir}"')
    lines.append("")
    lines.append('cd "${WORK_DIR}" || { echo "ERROR: Failed to cd into WORK_DIR=${WORK_DIR}"; exit 1; }')
    lines.append("")
    lines.append('mapfile -t PATTERNS < <(grep -v \'^[[:space:]]*#\' "${MANIFEST}" | sed \'/^[[:space:]]*$/d\')')
    lines.append('if [[ ${#PATTERNS[@]} -eq 0 ]]; then echo "ERROR: No usable entries in manifest: ${MANIFEST}"; exit 1; fi')
    lines.append("")
    lines.append('# Expand patterns into file list (sorted per-pattern for stability)')
    lines.append('FILES=()')
    lines.append('for pat in "${PATTERNS[@]}"; do')
    lines.append('  while IFS= read -r fp; do FILES+=("$fp"); done < <(compgen -G "$pat" | sort)')
    lines.append('done')
    lines.append("")
    lines.append('# Dedupe while keeping order')
    lines.append('declare -A SEEN')
    lines.append('DEDUPED=()')
    lines.append('for fp in "${FILES[@]}"; do')
    lines.append('  if [[ -z "${SEEN[$fp]+x}" ]]; then SEEN["$fp"]=1; DEDUPED+=("$fp"); fi')
    lines.append('done')
    lines.append("")
    lines.append('NFILES=${#DEDUPED[@]}')
    lines.append('if [[ $NFILES -eq 0 ]]; then echo "ERROR: Expansion produced zero files from manifest: ${MANIFEST}"; exit 1; fi')
    lines.append("")
    lines.append('# TASK_ID is 0-based here (matches your default array spec 0-(N-1))')
    lines.append('if [[ ${TASK_ID} -lt 0 || ${TASK_ID} -ge ${NFILES} ]]; then')
    lines.append('  echo "ERROR: TASK_ID=${TASK_ID} out of range for NFILES=${NFILES}"; exit 1;')
    lines.append('fi')
    lines.append('INPUT_FILE="${DEDUPED[$TASK_ID]}"')
    lines.append("")
    lines.append('echo "Running TASK_ID=${TASK_ID} on host $(hostname) at $(date)"')
    lines.append('echo "Work dir: ${WORK_DIR}"')
    lines.append('echo "Input file: ${INPUT_FILE}"')
    lines.append("")
    lines.append('srun "${GROOVY_SCRIPT}" "${INPUT_FILE}"')
    lines.append('echo "Finished TASK_ID=${TASK_ID} at $(date)"')
    lines.append("")
    return "\n".join(lines)



def write_manifest_file(manifest_path, files_list):
    with open(manifest_path, "w") as out:
        for fp in files_list:
            out.write(f"{fp}\n")


def estimate_peak_memory_children():
    peak_mem_str = "Unknown"
    try:
        import resource
        usage   = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak_kb = usage.ru_maxrss
        if((peak_kb is not None) and (peak_kb > 0)):
            peak_mb = float(peak_kb) / 1024.0
            if(peak_mb < 1024.0):
                peak_mem_str = f"{peak_mb:.2f} MB"
            else:
                peak_gb      = peak_mb / 1024.0
                peak_mem_str = f"{peak_gb:.2f} GB"
        else:
            peak_mem_str = "Unavailable"
    except Exception:
        peak_mem_str = "Unavailable"
    return peak_mem_str


def main():
    local_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="Run a Groovy conversion script over many input files in sequential or SLURM array mode, with optional email summary (sequential only).", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-m",    "-mode",    "--mode",              dest="mode",       choices=["sequential", "slurm"], default="sequential",              help="Run mode: sequential (local) or slurm (submit array job).")
    parser.add_argument("-src",  "-source",  "--source",            dest="source",                                      default="clasdis",                 help="Input source preset: clasdis, evgen, data, rdf (rdf is alias for data).")
    parser.add_argument("-mc",   "-mct",     "--mc-type",           dest="mc_type",                                     default="mdf",                     help="MC type preset for clasdis/evgen: rec/mdf (default) or gen/gdf. Ignored for data/rdf.")
    parser.add_argument("-evt",  "-event",   "--event-type",        dest="event_type",                                  default="epipX",                   help="Event type preset for clasdis and data/rdf: SIDIS/epipX (default), exclusive/epipN, proton/eppipX, DP/epippimX. Ignored for evgen (forced epipX).")

    parser.add_argument("-ptxt", "-paths",   "--paths-txt",         dest="paths_txt",                                   default=None,                      help=f"Override the default TXT file list. If omitted, uses a built-in default based on --source in: {DEFAULT_PATHS_DIR}/")
    parser.add_argument("-sp",   "-script",  "--script-path",       dest="script_path",                                 default=None,                      help="Override the Groovy script path directly. If omitted, uses a preset-based selection (currently placeholder until you fill it).")
    parser.add_argument("-id",   "-jID",     "--job-id",            dest="job_id",                                      default=None,                      help="Job identifier (default is derived from presets + date; adds _Seq in sequential mode).")

    parser.add_argument("-e",    "-mail",    "--email",             dest="email",                                       action="store_true",               help=f"Send completion email to: {EMAIL_TO} (sequential mode only).")
    parser.add_argument("-em",   "-message", "--email_message",     dest="email_message",     type=str,                 default=None,                      help="Extra message to send in email if selected (sequential mode only).")
    parser.add_argument("-f",    "-file",    "--file",              dest="files",             action="append",          default=None,                      help="Add an explicit input file (bypasses TXT expansion for that entry). Can be repeated.")
    parser.add_argument("-ub",   "-uniq",    "--unique-batches",    dest="unique_batches",    type=str,                 default=None,                      help="Run only a unique set of file-indices (SLURM-style list like '1-5,7,10-12' or '1-10:2'). Applies to sequential (filter) and slurm (array spec).")
    parser.add_argument("-saj",  "-aj",      "--slurm-array-jobid", dest="slurm_array_jobid", type=str,                 default=None,                      help="In sequential mode, coordinate with an existing SLURM array job (cancel pending tasks; skip active/completed tasks).")

    parser.add_argument("-st",   "-time",    "--slurm-time",        dest="slurm_time",                                  default=DEFAULT_SLURM_TIME,        help="SLURM time limit for each job in slurm mode (HH:MM:SS).")
    parser.add_argument("-cpu",  "-mem",     "--slurm-mem-per-cpu", dest="slurm_mem_per_cpu",                           default=DEFAULT_SLURM_MEM_PER_CPU, help="SLURM memory per CPU in slurm mode (e.g. '3GB', '4000M').")

    parser.add_argument("-dr",   "-test",    "--dry-run",           dest="dry_run",                                     action="store_true",               help="Do not execute local run-groovy or submit SLURM jobs; still expands file lists and prints planned actions (SLURM mode still requires approval).")

    args = parser.parse_args()

    timer.start()

    start_time = timer.start_find(return_Q=True)

    source_norm     = normalize_source(args.source)
    mc_type_norm    = normalize_mc_type(args.mc_type)
    event_type_norm = normalize_event_type(args.event_type)

    if((source_norm == "evgen") and (event_type_norm != "epipX")):
        print(f"{color.BBLUE}[INFO]{color.END} --source evgen forces event type to epipX; ignoring requested --event-type '{args.event_type}'.")
        event_type_norm = "epipX"

    if((args.paths_txt is None) or (str(args.paths_txt).strip() == "")):
        used_paths_txt = default_paths_txt_for_source(source_norm)
        used_paths_txt_reason = "default-by-source"
    else:
        used_paths_txt = os.path.expanduser(os.path.expandvars(str(args.paths_txt).strip()))
        used_paths_txt_reason = "user-override"

    globs_list = read_globs_from_txt(used_paths_txt)

    if(globs_list is None):
        print(f"{color.Error}WARNING: paths TXT file not found / empty: {color.END}{used_paths_txt}\nCannot continue.\n")
        sys.exit(1)

    expanded_files, unmatched_globs = expand_globs_to_files(globs_list)

    if((len(unmatched_globs) > 0)):
        ex1 = unmatched_globs[0]
        print(f"{color.RED}WARNING: Some TXT entries expanded to zero files: {color.END}{len(unmatched_globs)} (example: {ex1})")

    if(args.files is not None):
        for fp in args.files:
            expanded_files.append(fp)

    expanded_files = dedupe_keep_order(expanded_files)

    nfiles = len(expanded_files)
    if((nfiles <= 0)):
        print(f"{color.Error}ERROR: No input files were found after TXT expansion (and --file inputs).{color.END}")
        sys.exit(1)

    requested_batches = parse_unique_batches_string(args.unique_batches, nfiles)
    if((args.unique_batches is not None) and (requested_batches is not None)):
        print(f"{color.BBLUE}[INFO]{color.END} --unique-batches provided: '{args.unique_batches}'")
        print(f"{color.BBLUE}[INFO]{color.END} Will operate on these file indices (after range filtering): {requested_batches}")

    if((args.job_id is None) or (str(args.job_id).strip() == "")):
        job_id_final = build_default_job_id(source_norm, mc_type_norm, event_type_norm, args.mode)
    else:
        job_id_final = str(args.job_id).strip()

    if((args.script_path is None) or (str(args.script_path).strip() == "")):
        script_path_final = resolve_groovy_script_from_presets(source_norm, mc_type_norm, event_type_norm)
        script_path_reason = "preset"
    else:
        script_path_final = os.path.expanduser(os.path.expandvars(str(args.script_path).strip()))
        script_path_reason = "user-override"

    if(is_placeholder_path(script_path_final)):
        if(args.dry_run):
            print(f"{color.RED}WARNING: Groovy script path is a placeholder and must be updated or overridden with --script-path: {color.END}{script_path_final}")
        else:
            print(f"{color.Error}ERROR: Groovy script path is a placeholder and must be updated or overridden with --script-path: {color.END}{script_path_final}")
        sys.exit(1)

    work_dir_final = resolve_output_dir_from_presets(source_norm, mc_type_norm)

    array_spec_default = f"0-{nfiles-1}"
    if((args.unique_batches is None) or (str(args.unique_batches).strip() == "")):
        array_spec = array_spec_default, "default"
        array_spec_str = array_spec_default
        array_spec_reason = "default-by-filecount"
    else:
        array_spec_str = str(args.unique_batches).replace(" ", "")
        array_spec_reason = "user-override"

    if(args.dry_run):
        txt_note = f"{used_paths_txt}"
        print("")
        print(f"{color.BBLUE}[INFO]{color.END} DRY RUN SUMMARY: mode={args.mode}, source={source_norm}, mc-type={mc_type_norm}, event-type={event_type_norm}, job_id={job_id_final}")
        print(f"{color.BBLUE}[INFO]{color.END} Paths TXT ({used_paths_txt_reason}): {txt_note}")
        print(f"{color.BBLUE}[INFO]{color.END} Work directory (preset): {work_dir_final}")
        print(f"{color.BBLUE}[INFO]{color.END} TXT entries used (non-comment, non-empty): {len(globs_list) if(globs_list is not None) else 0}")
        print(f"{color.BBLUE}[INFO]{color.END} Expanded files (after dedupe, plus --file): {nfiles}")
        print(f"{color.BBLUE}[INFO]{color.END} Default SLURM array spec (if not overridden): {array_spec_default}")
        print(f"{color.BBLUE}[INFO]{color.END} Active array spec ({array_spec_reason}): {array_spec_str}")
        if((nfiles > 0)):
            show_n = 5 if((nfiles >= 5)) else nfiles
            examples = ""
            for ii in range(show_n):
                examples = f"{examples}[{ii+1:05d}] {expanded_files[ii]}\n"
            print(f"{color.BBLUE}[INFO]{color.END} First {show_n} expanded file(s):\n{examples}")

    overall_success = False
    processed_lines = []
    results         = []
    slurm_jobid     = None

    if(args.mode == "sequential"):
        if((args.slurm_array_jobid is not None)):
            print(f"{color.BBLUE}[INFO]{color.END} Sequential mode will coordinate with SLURM array job: {args.slurm_array_jobid}")

        if((requested_batches is None)):
            batch_iterable = list(range(1, nfiles + 1))
        else:
            batch_iterable = requested_batches

        for batch_idx in batch_iterable:
            file_path = expanded_files[batch_idx - 1]
            run_this  = True

            if((args.slurm_array_jobid is not None)):
                state = query_slurm_array_task_state(args.slurm_array_jobid, batch_idx)
                if((state == "IGNORE")):
                    pass
                elif((state is None)):
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} not found in squeue output; assuming completed and skipping index {batch_idx}.")
                    run_this = False
                elif((state == "PD")):
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} is pending; attempting to cancel so sequential mode can run index {batch_idx}.")
                    cancelled = cancel_slurm_array_task(args.slurm_array_jobid, batch_idx)
                    if(not cancelled):
                        print(f"{color.BYELLOW}[INFO]{color.END} Could not safely cancel {args.slurm_array_jobid}_{batch_idx}; skipping index {batch_idx} to avoid double-processing.")
                        run_this = False
                else:
                    print(f"{color.BBLUE}[INFO]{color.END} SLURM array task {args.slurm_array_jobid}_{batch_idx} is in state '{state}'; skipping index {batch_idx} to avoid double-processing.")
                    run_this = False

            if(not run_this):
                continue

            print(f"{color.BBLUE}Processing file index {batch_idx}/{nfiles}: {color.END_B}{file_path}{color.END}")
            print(f"{color.BBLUE}[INFO]{color.END} Working directory: {work_dir_final}")

            cmd = ["run-groovy", script_path_final, file_path]
            if(args.dry_run):
                rc = 0
            else:
                try:
                    completed = subprocess.run(cmd, check=False, cwd=work_dir_final)
                    rc        = completed.returncode
                except Exception as exc:
                    rc = 999
                    print(f"{color.Error}ERROR: failed to run command: {cmd}\nReason: {exc}{color.END}")

            done_stamp = "\n".join(timer.time_elapsed(return_Q=True))
            done_stamp = f'({done_stamp.replace("\n", " ")})'
            done_stamp = done_stamp.replace(" Current", "Current")
            done_stamp = done_stamp.replace(". )", ".)")
            processed_lines.append(f"[{batch_idx:05d}] {file_path} {done_stamp} [rc={rc}]")
            results.append({"index": batch_idx, "file": file_path, "rc": rc, "done": done_stamp})

        failed = [rr for rr in results if(rr["rc"] != 0)]
        overall_success = (len(failed) == 0)

        peak_mem_str = estimate_peak_memory_children()

        if((args.slurm_array_jobid is not None)):
            active = slurm_array_has_active_tasks(args.slurm_array_jobid)
            if(active):
                print(f"{color.BBLUE}[INFO]{color.END} SLURM array job {args.slurm_array_jobid} still has active tasks (sequential mode ran only the non-active/cancelled subset).")
            else:
                print(f"{color.BBLUE}[INFO]{color.END} No active tasks remain in SLURM array job {args.slurm_array_jobid} (or coordination was disabled).")

        start_time_str = timer.start_find(return_Q=True).replace("Ran", "Started running")
        end_time_str, total_time_str, rate_line = timer.stop(return_Q=True)

        failures_block = "None"
        if(len(failed) > 0):
            failures_block = ""
            for rr in failed:
                failures_block = f"{failures_block}  [{rr['index']:05d}] rc={rr['rc']} file={rr['file']}\n"
            failures_block = failures_block.rstrip("\n")

        processed_block = ""
        for line in processed_lines:
            processed_block = f"{processed_block}{line}\n"
        processed_block = processed_block.rstrip("\n")

        subject_status = "SUCCESS" if(overall_success) else "FAILURE"
        subject        = f"[GroovyRunner] {subject_status} (mode=sequential, N={nfiles}, job_id={job_id_final})"

        paths_txt_shown = used_paths_txt
        summary_block = f"""Script: {os.path.basename(__file__)}
Mode: sequential
Host: {socket.gethostname()}
Job ID: {job_id_final}
Source preset: {source_norm}
MC type preset: {mc_type_norm}
Event type preset: {event_type_norm}
Groovy script ({script_path_reason}): {script_path_final}
Paths TXT ({used_paths_txt_reason}): {paths_txt_shown}
Work directory (preset): {work_dir_final}
Total expanded files: {nfiles}
Unique batches: {args.unique_batches}
Coordinating SLURM array jobid: {args.slurm_array_jobid}
Dry run: {args.dry_run}
Overall success: {overall_success}
Approx. peak memory usage (children): {peak_mem_str}
Failed items:
{failures_block}
"""

        email_body = f"""{start_time_str}

{summary_block}

Files processed:
{processed_block}

{end_time_str}
{total_time_str}
{rate_line}
"""
        if(args.email_message is not None):
            email_body = f"""
User Given Message:
{args.email_message}

{email_body}

"""
        print(email_body)

        if(args.email):
            send_email(subject=subject, body=email_body, recipient=EMAIL_TO, dry_run=args.dry_run)
        else:
            if(args.dry_run):
                print("\n--- DRY RUN: email sending disabled (no email would be sent) ---\n")
            else:
                print("Email sending disabled (no email sent).")

    elif(args.mode == "slurm"):
        if(args.email):
            print(f"{color.BBLUE}[INFO]{color.END} Note: -e/--email is ignored in slurm mode (SLURM mail settings handle FAIL notifications).")

        job_name      = job_id_final
        manifest_path = used_paths_txt
        sbatch_path   = os.path.join(local_dir, f"{job_name}.sh")

        if((args.unique_batches is None) or (str(args.unique_batches).strip() == "")):
            array_spec_str = f"0-{nfiles-1}"
        else:
            array_spec_str = str(args.unique_batches).replace(" ", "")

        slurm_script_text = build_slurm_array_script_text(script_path=script_path_final, manifest_path=manifest_path, job_name=job_name, email_address=EMAIL_TO, slurm_time=args.slurm_time, slurm_mem_per_cpu=args.slurm_mem_per_cpu, slurm_partition=DEFAULT_SLURM_PARTITION, slurm_account=DEFAULT_SLURM_ACCOUNT, array_spec=array_spec_str, work_dir=work_dir_final)

        print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM sbatch script:\n")
        print(slurm_script_text)
        print(f"\n{color.BBLUE}[INFO]{color.END} Proposed manifest file path:\n{manifest_path}\n")
        print(f"{color.BBLUE}[INFO]{color.END} Proposed sbatch script path:\n{sbatch_path}\n")
        print(f"{color.BBLUE}[INFO]{color.END} Expanded file count (manifest lines): {nfiles} (array spec: {array_spec_str})")
        print(f"{color.BBLUE}[INFO]{color.END} Work directory (preset): {work_dir_final}")

        try:
            response = input("Approve this SLURM sbatch script (and allow it to be written + submitted)? [y/N]: ").strip().lower()
        except EOFError:
            response = "n"

        if((response != "y") and (response != "yes")):
            print(f"{color.Error}[ERROR]{color.END} SLURM script not approved. Exiting without writing or submission.")
            sys.exit(1)

        if(args.dry_run):
            print("\n--- DRY RUN: approved SLURM script would now be written and submitted, but dry-run prevents writing/submission. ---\n")
            overall_success = True
        else:
            # IMPORTANT: Do NOT overwrite the shared "Paths_to_*.txt" file. The sbatch script expands it at runtime.
            with open(sbatch_path, "w") as out:
                out.write(slurm_script_text)
            os.chmod(sbatch_path, 0o755)

            array_cmd = ["sbatch", "--parsable", sbatch_path]
            cmd_str   = ""
            for cc in array_cmd:
                cmd_str = f"{cmd_str}{cc} "
            cmd_str = cmd_str.strip()

            print(f"{color.BBLUE}[INFO]{color.END} Submitting SLURM array job with command: {cmd_str}")

            try:
                proc = subprocess.run(array_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as exc:
                print(f"{color.Error}[ERROR]{color.END} Exception while submitting SLURM job: {exc}")
                sys.exit(1)

            if(proc.returncode != 0):
                msg = proc.stderr.strip()
                if((msg == "")):
                    msg = "(no additional message from sbatch)"
                print(f"{color.Error}[ERROR]{color.END} sbatch failed with code {proc.returncode}: {msg}")
                sys.exit(1)

            slurm_jobid_raw = proc.stdout.strip()
            slurm_jobid     = slurm_jobid_raw.split(";")[0].strip()
            print(f"{color.BBLUE}[INFO]{color.END} Submitted SLURM array job id: {slurm_jobid}")
            overall_success = True

        start_time_str = timer.start_find(return_Q=True).replace("Ran", "Started running")
        end_time_str, total_time_str, rate_line = timer.stop(return_Q=True)

        paths_txt_shown = used_paths_txt
        slurm_summary = f"""Script: {os.path.basename(__file__)}
Mode: slurm
Host: {socket.gethostname()}
Job ID: {job_id_final}
Source preset: {source_norm}
MC type preset: {mc_type_norm}
Event type preset: {event_type_norm}
Groovy script ({script_path_reason}): {script_path_final}
Paths TXT ({used_paths_txt_reason}): {paths_txt_shown}
Work directory (preset): {work_dir_final}
Total expanded files: {nfiles}
Unique batches: {args.unique_batches}
SLURM time: {args.slurm_time}
SLURM mem-per-cpu: {args.slurm_mem_per_cpu}
Manifest path: {manifest_path}
SBATCH script path: {sbatch_path}
Submitted SLURM jobid: {slurm_jobid}
Dry run: {args.dry_run}
Overall success: {overall_success}
"""

        print(f"""{start_time_str}

{slurm_summary}

{end_time_str}
{total_time_str}
{rate_line}
""")

    print(start_time)
    timer.stop()
    print("Done")
    sys.exit(0 if(overall_success) else 1)


if(__name__ == "__main__"):
    main()
