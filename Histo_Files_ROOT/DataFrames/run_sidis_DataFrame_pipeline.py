#!/usr/bin/env python3
import os
import sys
import glob
import argparse
import subprocess
import re
from datetime import datetime
import time

script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

Script_Name = "run_sidis_DataFrame_pipeline.py"

# ===================================================================
# DEFAULT PATHS
# ===================================================================
DATAFRAMES_BASE = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames"
RDF_DIR_DEFAULT = os.path.join(DATAFRAMES_BASE, "REAL_Data")
MDF_DIR_DEFAULT = os.path.join(DATAFRAMES_BASE, "Matching_REC_MC")
GDF_DIR_DEFAULT = os.path.join(DATAFRAMES_BASE, "GEN_MC")
BATCH_FILE_DEFAULT = os.path.join(DATAFRAMES_BASE, "File_Batches.py")

MAIN_SCRIPT = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py"

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Production orchestrator for SIDIS response-matrix pipeline.\nReplaces old helpers with clean CLI, dynamic batching, and unified SLURM/local modes.", formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-m", "--mode",
                        default="parallel",
                        choices=["sequential", "parallel", "slurm", "make_batches"],
                        help="Execution mode.\n")

    parser.add_argument('-cn', '--cut_name',
                        default="cut_Complete_SIDIS",
                        choices=['cut_Complete_SIDIS', 'cut_Complete_SIDIS_MM_loose', 'cut_Complete_SIDIS_MM_tight', 'cut_Complete_SIDIS_chi2_strict_pip', 'cut_Complete_SIDIS_dcfid_loose_el', 'cut_Complete_SIDIS_dcfid_loose_pip', 'cut_Complete_SIDIS_dcfid_pass1_el', 'cut_Complete_SIDIS_dcfid_pass1_pip', 'cut_Complete_SIDIS_dcfid_tight_el', 'cut_Complete_SIDIS_dcfid_tight_pip', 'cut_Complete_SIDIS_dcfidref_loose_el', 'cut_Complete_SIDIS_dcfidref_tight_el', 'cut_Complete_SIDIS_dcv_loose_el', 'cut_Complete_SIDIS_dcv_pass1_el', 'cut_Complete_SIDIS_dcv_tight_el', 'cut_Complete_SIDIS_dvz_loose_pip', 'cut_Complete_SIDIS_dvz_pass1_pip', 'cut_Complete_SIDIS_dvz_tight_pip', 'cut_Complete_SIDIS_eS1o', 'cut_Complete_SIDIS_eS2o', 'cut_Complete_SIDIS_eS3o', 'cut_Complete_SIDIS_eS4o', 'cut_Complete_SIDIS_eS5o', 'cut_Complete_SIDIS_eS6o', 'cut_Complete_SIDIS_ecband_loose_el', 'cut_Complete_SIDIS_ecband_tight_el', 'cut_Complete_SIDIS_ecoi_pass1_el', 'cut_Complete_SIDIS_ecthr_loose_el', 'cut_Complete_SIDIS_ecthr_tight_el', 'cut_Complete_SIDIS_ectri_pass1_el', 'cut_Complete_SIDIS_noSmear', 'cut_Complete_SIDIS_no_pip_testdc', 'cut_Complete_SIDIS_no_sector_pcal', 'cut_Complete_SIDIS_no_valerii_knockout', 'cut_Complete_SIDIS_pcalvol_loose', 'cut_Complete_SIDIS_pcalvol_tight', 'cut_Complete_SIDIS_pid_full_pass1', 'cut_Complete_SIDIS_pipS1o', 'cut_Complete_SIDIS_pipS2o', 'cut_Complete_SIDIS_pipS3o', 'cut_Complete_SIDIS_pipS4o', 'cut_Complete_SIDIS_pipS5o', 'cut_Complete_SIDIS_pipS6o'],
                        help="Cut name applied to both RDF and MDF (GDF always uses 'no_cut').\n")

    # Analysis options — ON by default → only negation flags
    parser.add_argument('-nmr', '--no_make_root',
                        action='store_true',
                        help="Disable ROOT output (enabled by default).\n")
    parser.add_argument('-nm2', '--no_make_2D',
                        action='store_true',
                        help="Disable 2D kinematic plots (enabled by default).\n")
    parser.add_argument('-nm2r', '--no_make_2D_rho',
                        action='store_true',
                        help="Disable rho0 2D plots (enabled by default).\n")
    parser.add_argument('-nu5', '--no_unfold_5D',
                        action='store_true',
                        help="Disable 5D response matrices (enabled by default).\n")
    parser.add_argument('-nf', '--no_fast',
                        action='store_true',
                        help="Disable fast mode (enabled by default).\n")

    # Other toggles
    parser.add_argument('-vb', '--valerii_bins',
                        action='store_true',
                        help="Use Valerii binning.\n")
    parser.add_argument('-hpp', '--use_hpp',
                        action='store_true',
                        help="Apply HPP acceptance weights.\n")
    parser.add_argument('-sw', '--spline_weights',
                        action='store_true',
                        help="Use spline-based event weights.\n")
    parser.add_argument('-swf', '--spline_weight_file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/Final_ZerothOrder_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt",
                        help="Spline weight file path.\n")
    parser.add_argument('-hppf', '--hpp_weight_file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights.hpp",
                        help="HPP acceptance weight file path.\n")


    parser.add_argument('-nin', '--name_in',
                        default="*Final_Analysis_Iterations_I0*.root",
                        help="Common string name of the RDataFrames that are to be used to form the file batches.\n")
    parser.add_argument('-n', '--name',
                        default="",
                        help="Base name suffix for merged output and batch files.\n")
    parser.add_argument('-r', '--root',
                        default="SIDIS_epip_Response_Matrices_from_RDataFrames.root",
                        # help="Base ROOT output name.\n")
                        help=argparse.SUPPRESS)

    # Batching controls
    parser.add_argument('-nb', '--num_batches',
                        type=int,
                        default=150,
                        help="Number of normal batches to create. Last batch will be reserved for lundrho-MC files.\n")

    # Directories
    parser.add_argument('-wd', '--work_dir',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames",
                        help="Final work directory for merged output.\n")
    parser.add_argument('-sd', '--scratch_dir',
                        # default="/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work",
                        default="/scratch/richcap/Response_Matrix_Outputs",
                        help="Scratch/volatile directory for temporary batch outputs (parallel/sequential).\n")
    parser.add_argument('-ld', '--log_dir',
                        default="/scratch/richcap/Response_Matrix_Outputs",
                        help="Log directory (empty = /scratch/<user>/response_matrix_logs).\n")

    # Parallel/sequential controls
    parser.add_argument('-j', '--jobs',
                        type=int,
                        default=6,
                        help="Max simultaneous jobs in parallel mode.\n")
    parser.add_argument('-cf', '--continue_on_failure',
                        action='store_true',
                        help="Continue on batch failure (sequential/parallel).\n")

    # SLURM controls + coordination
    parser.add_argument('-st', '--slurm_time',
                        default="12:00:00",
                        help="SLURM time limit per array task.\n")
    parser.add_argument('-sm', '--slurm_mem',
                        default="4GB",
                        help="SLURM mem-per-cpu.\n")
    parser.add_argument('-saj', '--slurm_array_jobid',
                        type=str,
                        default=None,
                        help="Optional SLURM array job ID for coordination with local modes.\n")

    # make_batches mode directories
    parser.add_argument('-rdfd', '--rdf_dir',
                        default=RDF_DIR_DEFAULT,
                        help="RDF input directory (make_batches only).\n")
    parser.add_argument('-mdfd', '--mdf_dir',
                        default=MDF_DIR_DEFAULT,
                        help="MDF input directory (make_batches only).\n")
    parser.add_argument('-gdfd', '--gdf_dir',
                        default=GDF_DIR_DEFAULT,
                        help="GDF input directory (make_batches only).\n")
    parser.add_argument('-bf', '--batch_file',
                        default=BATCH_FILE_DEFAULT,
                        help="Output File_Batches.py path (make_batches only).\n")

    # Helpers
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Verbose output.\n")
    parser.add_argument('-dr', '--dry_run',
                        action='store_true',
                        help="Dry run (print commands only).\n")
    parser.add_argument('-e', '--email',
                        action='store_true',
                        help="Send completion email.\n")
    parser.add_argument('-em', '--email_message',
                        default="",
                        help="Extra message for email.\n")
    parser.add_argument('-emj', '--email_message_job',
                        default="",
                        help="Extra message for email (will be given to the jobs executed by this script).\n")

    # Passthrough
    parser.add_argument('-x', '--extra',
                        nargs=argparse.REMAINDER,
                        default=[],
                        help="Everything after --extra is passed verbatim to Response_Matrix_Creation_using_RDataFrames.py.\n")

    return parser.parse_args()

# ===================================================================
# EMAIL FUNCTIONS — PRESERVED VERBATIM
# ===================================================================
def ansi_to_plain(text):
    ansi_plain_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "", '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", '\033[0m': ""}
    sorted_codes = sorted(ansi_plain_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_plain_map[code])
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    plain_body = ansi_to_plain(body)
    subprocess.run(["mail", "-s", subject, recipient], input=plain_body.encode(), check=False)

def Update_Email(args, update_message="", verbose_override=False, no_time=True):
    update_email = ""
    if(no_time):
        update_email = update_message
    else:
        update_email = f"""{update_message}
{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}"""
    if(update_email not in [""]):
        args.email_message = f"{args.email_message}\n{update_email}"
        if((args.verbose or verbose_override) and (verbose_override is not None)):
            print(update_email)

def Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Files"):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "root", "email_message_job"]):
            continue
        if(any(((surpress == str(name)) and (not getattr(args, surpress, False))) for surpress in ["no_make_root", "no_make_2D", "no_make_2D_rho", "no_unfold_5D", "no_fast", "dry_run"])):
            continue
        if((getattr(args, "mode", None) == "make_batches") and (str(name) not in ["name_in", "rdf_per_batch", "mc_per_batch", "rdf_dir", "mdf_dir", "gdf_dir", "batch_file", "num_batches", "mode"])):
            continue
        if((getattr(args, "mode", None) != "slurm")        and ("slurm" in str(name))):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The '{Script_Name}' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

{args.email_message}

Arguments:
{args_list}

{end_time}
{total_time}
{rate_line}
    """

    if(args.email):
        send_email(subject=f"Finished Running the '{Script_Name}' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: '{Script_Name}' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
    print(f"\n\n\n\n{color.BOLD}{color_bg.YELLOW}EMAIL MESSAGE TO SEND:{color.END}\n\n{email_body}\n")
    if(Warning):
        print(f"\n\n{color.BOLD}CONTNUE RUNNING...{color.END}\n\n")
    elif(not Crashed):
        print(f"""{color.BGREEN}{color_bg.YELLOW}
    \t                                   \t
    \tThis code has now finished running.\t
    \t                                   \t   {color.END}

    """)
    else:
        print(f"""{color.BYELLOW}{color_bg.RED}
    \t                                   \t
    \t       This code has CRASHED!      \t
    \t                                   \t   {color.END}

    """)

def Crash_Report(args, crash_message="The Code has CRASHED!", continue_run=False):
    if(continue_run):
        crash_message = f"\n{color.BYELLOW}ERROR WARNING!{color.END}\n{crash_message}\n\nCONTINUED RUNNING...\n"
    else:
        crash_message = f"\n{color.Error}CRASH WARNING!{color.END}\n{crash_message}\n"
    print(crash_message, file=sys.stderr)
    args.email_message = f"{args.email_message}\n{crash_message}\n"
    Construct_Email(args, Crashed=(not continue_run), Warning=continue_run)
    if(not continue_run):
        sys.exit(1)
    else:
        print(f"\n\n{color.ERROR}WILL CONTINUE RUNNING THROUGH THE ERROR{color.END}\n\n")

# ===================================================================
# SLURM COORDINATION (from your original script)
# ===================================================================
SLURM_ARRAY_CHECK_DISABLED = False

def query_slurm_array_task_state(array_jobid, batch_index):
    global SLURM_ARRAY_CHECK_DISABLED
    if(SLURM_ARRAY_CHECK_DISABLED):
        return "IGNORE"
    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid), "-o", "%.18i %.2t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception:
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    if(proc.returncode != 0):
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    target_id = f"{array_jobid}_{batch_index}"
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        if parts[0] == target_id:
            return parts[1]
    return None

def cancel_slurm_array_task(array_jobid, batch_index):
    job_str = f"{array_jobid}_{batch_index}"
    try:
        subprocess.run(["scancel", job_str], check=False)
        print(f"{color.BBLUE}[INFO]{color.END} Cancelled SLURM array task {job_str}")
    except Exception:
        pass

def slurm_array_has_active_tasks(array_jobid):
    global SLURM_ARRAY_CHECK_DISABLED
    if(array_jobid is None or SLURM_ARRAY_CHECK_DISABLED):
        return False
    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(array_jobid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return proc.stdout.strip() != ""
    except Exception:
        SLURM_ARRAY_CHECK_DISABLED = True
        return False

# ===================================================================
# HELPER FUNCTIONS
# ===================================================================
def ensure_directory(path):
    os.makedirs(path, exist_ok=True)
    return path

def collect_files(dir_path, pattern="*.root"):
    if(all(backup not in pattern for backup in ["*", "."])):
        pattern = f"*{pattern}*"
    if("*.root" not in pattern):
        pattern = f"{pattern}.root" if("*" in pattern) else f"{pattern}*.root"
    if(not os.path.isdir(dir_path)):
        print(f"{color.Error}Directory not found: {dir_path}{color.END}")
        return []
    files = glob.glob(os.path.join(dir_path, pattern), recursive=True)
    return sorted([os.path.abspath(f) for f in files])

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

def split_evenly(files, n_batches):
    if(not files or n_batches <= 0):
        return [[]]
    batch_size = len(files) // n_batches
    remainder = len(files) % n_batches
    batches = []
    start = 0
    for i in range(n_batches):
        current = batch_size + (1 if i < remainder else 0)
        batches.append(files[start:start + current])
        start += current
    return batches

def make_batches_mode(args):
    rdf_files = collect_files(args.rdf_dir, args.name_in)
    mdf_files = collect_files(args.mdf_dir, args.name_in)
    gdf_files = collect_files(args.gdf_dir, args.name_in)
    if(not rdf_files):
        Crash_Report(args, crash_message=f"{color.Error}No RDF files found - cannot generate batches.{color.END}")
    # Determine number of normal batches
    num_normal_batches = max(1, args.num_batches if(getattr(args, "num_batches", len(rdf_files)) < len(rdf_files)) else len(rdf_files))
    # Separate LUND files (lowercase "lund" anywhere in filename) from both MDF and GDF
    lund_mdf   = [f for f in mdf_files if("lund" in os.path.basename(f).lower())]
    lund_gdf   = [f for f in gdf_files if("lund" in os.path.basename(f).lower())]
    normal_mdf = [f for f in mdf_files if(f not in lund_mdf)]
    normal_gdf = [f for f in gdf_files if(f not in lund_gdf)]
    # Split normal files evenly across the first (N-1) batches
    num_normal = max(1, num_normal_batches - 1)
    rdf_chunks = split_evenly(rdf_files,  num_normal_batches)
    mdf_chunks = split_evenly(normal_mdf, num_normal)
    gdf_chunks = split_evenly(normal_gdf, num_normal)
    # LUND batch goes at the end (batch N)
    lund_batch_num = num_normal_batches
    lund_mdf_batch = {lund_batch_num: [os.path.abspath(f) for f in lund_mdf]}
    lund_gdf_batch = {lund_batch_num: [os.path.abspath(f) for f in lund_gdf]}
    def to_absolute(flist):
        return [os.path.abspath(f) for f in flist]
    rdf_batch = {i+1: to_absolute(chunk) for i, chunk in enumerate(rdf_chunks) if(chunk)}
    mdf_batch = {i+1: to_absolute(chunk) for i, chunk in enumerate(mdf_chunks) if(chunk)}
    gdf_batch = {i+1: to_absolute(chunk) for i, chunk in enumerate(gdf_chunks) if(chunk)}
    # Merge LUND batch
    mdf_batch.update(lund_mdf_batch)
    gdf_batch.update(lund_gdf_batch)
    with open(args.batch_file, "w") as f:
        f.write("# Auto-generated by run_sidis_DataFrame_pipeline.py on {}\n".format(datetime.now().strftime("%m-%d-%Y %H:%M:%S")))
        f.write("rdf_batch = {}\n".format(rdf_batch))
        f.write("mdf_batch = {}\n".format(mdf_batch))
        f.write("gdf_batch = {}\n".format(gdf_batch))
        f.write(f"# {num_normal_batches} total batches ({num_normal} normal + 1 LUND-only) - RDF:{len(rdf_files)} MDF:{len(normal_mdf)} GDF:{len(normal_gdf)} LUND_MDF:{len(lund_mdf)} LUND_GDF:{len(lund_gdf)}\n")
    # Update args for reporting
    args.rdf_per_batch =  len(rdf_files) // num_normal_batches if(num_normal_batches > 0) else 0
    args.mc_per_batch  = len(normal_mdf) // num_normal         if(num_normal > 0) else 0
    args.num_batches   = num_normal_batches
    Update_Email(args, update_message=f"""
{color.BGREEN}Successfully generated {color.END_B}{args.batch_file}{color.BGREEN} with {color.END_B}{num_normal_batches}{color.BGREEN} batches.{color.END}
   Normal batches : {num_normal}
   RDF files      : {len(rdf_files)} ({args.rdf_per_batch} per normal batch)
   Normal MDF/GDF : {len(normal_mdf)} ({args.mc_per_batch} per normal batch)
   LUND MDF/GDF   : {len(lund_mdf)}""", verbose_override=True, no_time=True)
    Construct_Email(args)

def build_main_command(args, batch_id, output_dir):
    # cmd = [sys.executable, MAIN_SCRIPT, "--batch_id", str(batch_id)]
    cmd = [MAIN_SCRIPT, "--batch_id", str(batch_id)]
    cmd.extend(["-cnR", args.cut_name, "-cnM", args.cut_name])

    if(not getattr(args, 'no_make_root',   False)):
        cmd.append("--make_root")
    if(not getattr(args, 'no_make_2D',     False)):
        cmd.append("--make_2D")
    if(not getattr(args, 'no_make_2D_rho', False)):
        cmd.append("--make_2D_rho")
    if(not getattr(args, 'no_unfold_5D',   False)):
        cmd.append("--unfold_5D")
    if(not getattr(args, 'no_fast',        False)):
        cmd.append("--fast")
    if(args.valerii_bins):
        cmd.append("--valerii_bins")
    if(args.use_hpp):
        cmd.append("--use_hpp")
    if(args.spline_weights):
        cmd.append("--spline_weights")
        cmd.extend(["--spline_file", args.spline_weight_file])
    if(args.hpp_weight_file and args.use_hpp):
        cmd.extend(["--hpp_input_file", args.hpp_weight_file])

    name_for_batch = f"{args.name}_{args.name_in}_Batch{batch_id:03d}" if(args.name) else f"{args.name_in}_Batch{batch_id:03d}"
    name_for_batch = name_for_batch.replace("*",     "")
    name_for_batch = name_for_batch.replace(".root", "")
    cmd.extend(["-n", name_for_batch])
    cmd.extend(["-r", os.path.join(output_dir, args.root)])

    if(args.email_message_job):
        cmd.extend(["-em", args.email_message_job])

    if(args.extra):
        cmd.extend(args.extra)

    return cmd


def should_skip_batch_due_to_slurm(args, batch_index):
    if(args.slurm_array_jobid is None):
        return False
    try:
        proc = subprocess.run(["squeue", "-h", "-r", "-j", str(args.slurm_array_jobid), "-o", "%.18i %.2t"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception:
        return False
    if(proc.returncode != 0):
        return False
    target_id = f"{args.slurm_array_jobid}_{batch_index}"
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if(len(parts) < 2):
            continue
        if(parts[0] == target_id):
            state = parts[1]
            if(state == "PD"):
                print(f"{color.BBLUE}[INFO]{color.END} Cancelling pending SLURM task {target_id}")
                cancel_slurm_array_task(args.slurm_array_jobid, batch_index)
                return False
            else:
                print(f"{color.BBLUE}[INFO]{color.END} Batch {batch_index} is {state} in SLURM - skipping")
                return True
    print(f"{color.BBLUE}[INFO]{color.END} Batch {batch_index} already completed by SLURM - skipping")
    return True

def start_job(args, batch_index, batch_output_dir, log_dir):
    if(should_skip_batch_due_to_slurm(args, batch_index)):
        return None
    cmd = build_main_command(args, batch_index, batch_output_dir)
    name_for_log = f"{args.name}_{args.name_in}_batch_{batch_index:03d}" if(args.name) else f"{args.name_in}_batch_{batch_index:03d}"
    name_for_log = str(name_for_log.replace("*", "")).replace(".root", "")
    log_path = os.path.join(log_dir, f"{name_for_log}.log")
    err_path = os.path.join(log_dir, f"{name_for_log}.err")
    Update_Email(args, update_message=f"{color.BCYAN}START{color.END}: Batch {batch_index:>3} of {args.num_batches}", verbose_override=True, no_time=False)
    if(args.verbose):
        print(f"        CMD: {' '.join(cmd)}")
        print(f"        LOG: {log_path}")
        print(f"        ERR: {err_path}")
    log_handle = open(log_path, "w")
    err_handle = open(err_path, "w")
    log_handle.write(f"# {' '.join(cmd)}\n")
    log_handle.flush()
    if(args.mode == "parallel"):
        process = subprocess.Popen(cmd, stdout=log_handle, stderr=err_handle, cwd=batch_output_dir)
    else:
        process = subprocess.run(  cmd, stdout=log_handle, stderr=err_handle, cwd=batch_output_dir)
    return {"process": process, "log_handle": log_handle, "err_handle": err_handle, "batch_index": batch_index}

def finish_job(job_item, results, args):
    ret = job_item["process"].poll()
    if(ret is None):
        return False
    try:
        job_item["log_handle"].close()
    except Exception:
        pass
    try:
        job_item["err_handle"].close()
    except Exception:
        pass
    if(ret == 0):
        Update_Email(args, update_message=f"{color.BGREEN}DONE {color.END}: Batch {job_item['batch_index']:>3} of {args.num_batches}", verbose_override=True, no_time=False)
    elif(not args.continue_on_failure):
        Crash_Report(args,  crash_message=f"{color.Error}FAIL {color.END}: Batch {job_item['batch_index']:>3} of {args.num_batches} (rc={ret})", continue_run=False)
    else:
        Update_Email(args, update_message=f"{color.Error}FAIL {color.END}: Batch {job_item['batch_index']:>3} of {args.num_batches} (rc={ret})", verbose_override=True, no_time=False)
    results.append(ret)
    return True

def run_local_batches(args):
    if(args.mode == "parallel"):
        # base_output = ensure_directory(os.path.join(args.scratch_dir, "Response_Matrices_Batches"))
        base_output = ensure_directory(args.scratch_dir)
    else:
        base_output = ensure_directory(args.work_dir)
    batch_output_dir = ensure_directory(os.path.join(base_output, args.run_subdir_name))
    log_dir = ensure_directory(args.log_dir if(args.log_dir) else f"/scratch/{os.getlogin()}/response_matrix_logs")
    sys.path.append(DATAFRAMES_BASE)
    from File_Batches import rdf_batch#, mdf_batch, gdf_batch
    sys.path.remove(DATAFRAMES_BASE)
    # num_batches = max(len(rdf_batch), len(mdf_batch), len(gdf_batch))
    num_batches = len(rdf_batch)
    args.num_batches = num_batches
    Update_Email(args, update_message=f"{color.BBLUE}Starting {args.mode} run with {color.END_B}{num_batches}{color.BBLUE} batches → output dir: {color.BCYAN}{batch_output_dir}{color.END}\n", verbose_override=True, no_time=True)
    results = []
    if(args.mode == "parallel"):
        running_jobs = []
        next_index   = 0
        max_jobs     = args.jobs if(args.jobs > 0) else 1
        while((next_index < num_batches) or (len(running_jobs) > 0)):
            while((next_index < num_batches) and (len(running_jobs) < max_jobs)):
                job = start_job(args, next_index + 1, batch_output_dir, log_dir)
                if(job is not None):
                    running_jobs.append(job)
                next_index += 1
            finished_index = None
            for i, job_item in enumerate(running_jobs):
                if(finish_job(job_item, results, args)):
                    finished_index = i
                    break
            if(finished_index is not None):
                running_jobs.pop(finished_index)
            else:
                time.sleep(1.0)
    else:  # sequential mode
        for b in range(1, num_batches + 1):
            job = start_job(args, b, batch_output_dir, log_dir)
            if(job is None):
                continue
            ret = job["process"].returncode
            results.append(ret)
            if(ret == 0):
                Update_Email(args, update_message=f"{color.BGREEN}DONE {color.END}: Batch {b:>3} of {args.num_batches}", verbose_override=True, no_time=False)
            else:
                Update_Email(args, update_message=f"{color.Error}FAIL {color.END}: Batch {b:>3} of {args.num_batches} (rc={ret})", verbose_override=True, no_time=False)
                if(not args.continue_on_failure):
                    Crash_Report(args, crash_message=f"{color.Error}Full Stop on Batch {b}.{color.END}", continue_run=False)
    failed = [i+1 for i, rc in enumerate(results) if(rc != 0)]
    if(failed):
        Crash_Report(args, crash_message=f"{color.Error}Failed batches: {failed}{color.END}", continue_run=args.continue_on_failure)

    if(not failed):
        name_for_merge = f"{args.name}_{args.name_in}_All" if(args.name) else f"{args.name_in}_All"
        name_for_merge = name_for_merge.replace("*",     "")
        name_for_merge = name_for_merge.replace(".root", "")
        merged_file    = os.path.join(args.work_dir, f"SIDIS_epip_Response_Matrices_from_RDataFrames_{name_for_merge}.root")
        batch_pattern  = os.path.join(batch_output_dir, "*Batch*.root")
        batch_files    = glob.glob(batch_pattern)
        if(batch_files):
            Update_Email(args, update_message=f"{color.BBLUE}Running hadd on {len(batch_files)} batch files...{color.END}", verbose_override=True, no_time=False)
            hadd_cmd = ["hadd", "-f", merged_file] + batch_files
            subprocess.run(hadd_cmd, check=True)
            Update_Email(args, update_message=f"{color.BGREEN}Merged file created: {merged_file}{color.END}", verbose_override=True, no_time=False)
    # === NEW: Track peak memory used by all child jobs ===
    peak_mem_str = estimate_peak_memory_children()
    Update_Email(args, update_message=f"{color.BBLUE}Peak memory used by child jobs: {peak_mem_str}{color.END}", verbose_override=True, no_time=True)
    Construct_Email(args)

def run_slurm_mode(args):
    sys.path.append(DATAFRAMES_BASE)
    from File_Batches import rdf_batch
    sys.path.remove(DATAFRAMES_BASE)
    num_batches = len(rdf_batch)

    batch_output_dir = ensure_directory(args.work_dir)

    name_base = args.run_subdir_name
    array_script = f"slurm_array_{name_base}.sh"
    hadd_script = f"slurm_hadd_{name_base}.sh"

    # Build array script
    with open(array_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --ntasks=1\n")
        f.write(f"#SBATCH --job-name=RMatrix_{name_base}\n")
        f.write("#SBATCH --mail-type=ALL\n")
        f.write("#SBATCH --mail-user=richard.capobianco@uconn.edu\n")
        f.write("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out\n")
        f.write("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err\n")
        f.write("#SBATCH --partition=production\n")
        f.write("#SBATCH --account=clas12\n")
        f.write(f"#SBATCH --mem-per-cpu={args.slurm_mem}\n")
        f.write(f"#SBATCH --time={args.slurm_time}\n")
        f.write(f"#SBATCH --array=1-{num_batches}\n\n")
        f.write(f'BATCH_ID=${{SLURM_ARRAY_TASK_ID}}\n')
        f.write(f'cd {batch_output_dir}\n')
        cmd_parts = build_main_command(args, "${BATCH_ID}", batch_output_dir)
        f.write(" ".join(cmd_parts) + "\n")

    # Build hadd script
    merged_file = os.path.join(args.work_dir, f"SIDIS_epip_Response_Matrices_from_RDataFrames_{name_base}.root")
    with open(hadd_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --ntasks=1\n")
        f.write(f"#SBATCH --job-name=RMatrix_hadd_{name_base}\n")
        f.write("#SBATCH --mail-type=ALL\n")
        f.write("#SBATCH --mail-user=richard.capobianco@uconn.edu\n")
        f.write("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out\n")
        f.write("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err\n")
        f.write("#SBATCH --partition=production\n")
        f.write("#SBATCH --account=clas12\n")
        f.write("#SBATCH --mem-per-cpu=2GB\n")
        f.write("#SBATCH --time=04:00:00\n\n")
        f.write(f'hadd -f {merged_file} {batch_output_dir}/*Batch*.root\n')

    os.chmod(array_script, 0o755)
    os.chmod(hadd_script, 0o755)

    # Print scripts for review
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM array script:\n")
    with open(array_script) as f:
        print(f.read())
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM hadd script:\n")
    with open(hadd_script) as f:
        print(f.read())

    try:
        response = input("\nApprove and submit these SLURM scripts? [y/N]: ").strip().lower()
    except EOFError:
        response = "n"

    if(response not in ["y", "yes"]):
        print(f"{color.Error}[ERROR]{color.END} SLURM scripts not approved. Exiting.")
        sys.exit(0)

    proc = subprocess.run(["sbatch", "--parsable", array_script], capture_output=True, text=True)
    array_id = proc.stdout.strip()
    Update_Email(args, update_message=f"{color.BGREEN}Submitted SLURM array job {array_id}{color.END}", verbose_override=True, no_time=True)

    hadd_proc = subprocess.run(["sbatch", "--parsable", f"--dependency=afterok:{array_id}", hadd_script], capture_output=True, text=True)
    Update_Email(args, update_message=f"{color.BGREEN}Submitted dependent hadd job {hadd_proc.stdout.strip()}{color.END}", verbose_override=True, no_time=True)

    Construct_Email(args)

def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    args.run_subdir_name = f"{args.name}_{args.name_in}_{datetime.now().strftime('%m_%d_%Y')}" if(args.name) else f"{args.name_in}_{datetime.now().strftime('%m_%d_%Y')}"
    args.run_subdir_name = args.run_subdir_name.replace("*",     "")
    args.run_subdir_name = args.run_subdir_name.replace(".root", "")
    if(  (args.email_message_job in [""]) and (args.email_message     not in [""])):
        args.email_message_job = args.email_message
    elif((args.email_message     in [""]) and (args.email_message_job not in [""])):
        args.email_message     = args.email_message_job

    if(args.mode == "make_batches"):
        make_batches_mode(args)
    elif(args.mode in ["sequential", "parallel"]):
        run_local_batches(args)
    elif(args.mode == "slurm"):
        args.email = False
        run_slurm_mode(args)
    else:
        args.email = False
        Crash_Report(args, crash_message="Unknown mode.")

if(__name__ == "__main__"):
    main()
    