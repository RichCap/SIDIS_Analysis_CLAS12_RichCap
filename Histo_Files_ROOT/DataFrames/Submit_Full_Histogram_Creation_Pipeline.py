#!/usr/bin/env python3
# Full histogram-creation submitter: optional dual HPP generation, then notebook-style response-matrix product jobs via ./run_sidis_DataFrame_pipeline.py.
# Acceptance is always local. Hybrid mode submits SLURM then starts parallel with -saj.

import os
import sys
import re
import time
import argparse
import subprocess
import threading
from collections import deque
from datetime import datetime

script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

Script_Name = "Submit_Full_Histogram_Creation_Pipeline.py"

DATAFRAMES_DIR    = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames"
ACCEPTANCE_SCRIPT = "./Acceptance_Weights_Creations_using_RDataFrames.py"
PIPELINE_SCRIPT   = "./run_sidis_DataFrame_pipeline.py"
HPP_OUT_DIR       = os.path.join(DATAFRAMES_DIR, "HPP_Files_Output")
DEFAULT_CUT       = "cut_Complete_SIDIS"

ACCEPTED_CUTS = [
    "cut_Complete_SIDIS", "cut_Complete_SIDIS_MM_None", "cut_Complete_SIDIS_MM_loose", "cut_Complete_SIDIS_MM_tight",
    "cut_Complete_SIDIS_chi2_strict_pip", "cut_Complete_SIDIS_dcfid_loose_el", "cut_Complete_SIDIS_dcfid_loose_pip",
    "cut_Complete_SIDIS_dcfid_pass1_el", "cut_Complete_SIDIS_dcfid_pass1_pip", "cut_Complete_SIDIS_dcfid_tight_el",
    "cut_Complete_SIDIS_dcfid_tight_pip", "cut_Complete_SIDIS_dcfidref_loose_el", "cut_Complete_SIDIS_dcfidref_tight_el",
    "cut_Complete_SIDIS_dcv_loose_el", "cut_Complete_SIDIS_dcv_pass1_el", "cut_Complete_SIDIS_dcv_tight_el",
    "cut_Complete_SIDIS_dvz_loose_pip", "cut_Complete_SIDIS_dvz_pass1_pip", "cut_Complete_SIDIS_dvz_tight_pip",
    "cut_Complete_SIDIS_eS1o", "cut_Complete_SIDIS_eS2o", "cut_Complete_SIDIS_eS3o", "cut_Complete_SIDIS_eS4o",
    "cut_Complete_SIDIS_eS5o", "cut_Complete_SIDIS_eS6o", "cut_Complete_SIDIS_ecband_loose_el",
    "cut_Complete_SIDIS_ecband_tight_el", "cut_Complete_SIDIS_ecoi_pass1_el", "cut_Complete_SIDIS_ecthr_loose_el",
    "cut_Complete_SIDIS_ecthr_tight_el", "cut_Complete_SIDIS_ectri_pass1_el", "cut_Complete_SIDIS_noSmear",
    "cut_Complete_SIDIS_no_pip_testdc", "cut_Complete_SIDIS_no_sector_pcal", "cut_Complete_SIDIS_no_valerii_knockout",
    "cut_Complete_SIDIS_pcalvol_loose", "cut_Complete_SIDIS_pcalvol_tight", "cut_Complete_SIDIS_pid_full_pass1",
    "cut_Complete_SIDIS_pipS1o", "cut_Complete_SIDIS_pipS2o", "cut_Complete_SIDIS_pipS3o", "cut_Complete_SIDIS_pipS4o",
    "cut_Complete_SIDIS_pipS5o", "cut_Complete_SIDIS_pipS6o",
]

# Notebook-style products (Only_1D deferred — pure phi RM not production-CLI-ready)
PRODUCTS = [{
        "key": "2D_Presentation",
        "label": "2D Presentation Histograms",
        "name_fmt": "2D_Presentation_{shared}_Q2_Y_Bins",
        "pipeline_flags": ["--z_axis_2D", "Q2_Y_Bin", "--no_make_2D_rho"],
        "extra": ["--make_2D_rho_normalization_only", "--run_rho_weight"],
        }, {
        "key": "Only_3D",
        "label": "Only 3D Response Matrices",
        "name_fmt": "Only_3D_{shared}_Response_Matrices",
        "pipeline_flags": ["--no_make_2D_rho", "--no_make_2D", "--no_unfold_5D"],
        "extra": ["--run_rho_weight"],
        }, {
        "key": "Only_5D",
        "label": "Only 5D Response Matrices",
        "name_fmt": "Only_5D_{shared}_Response_Matrices",
        "pipeline_flags": ["--no_make_2D_rho", "--no_make_2D"],
        "extra": ["--run_rho_weight", "--unfold_5D_only"],
        },
]

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def parse_args():
    p = argparse.ArgumentParser(description="Submit full histogram-creation pipeline: optional dual HPP generation, then parallel response-matrix products.", formatter_class=RawDefaultsHelpFormatter)
    p.add_argument("-e", "--email",
                   type=str,
                   default="children",
                   choices=["children", "runner", "all"],
                   nargs="?",
                   const="children",
                   help="Email mode: children (default: child scripts email, runner only prints), runner (only this script emails), all (both).\n")
    p.add_argument("-em", "--email_message",
                   type=str,
                   default="",
                   help="Free-form user message for emails. Product labels are appended for child -emj automatically.\n")
    p.add_argument("-spf", "--spline_file",
                   type=str,
                   # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/Final_ZerothOrder_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt",
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt",
                   help="Spline weight file for combined HPP and response-matrix spline weights.\n")
    p.add_argument("-n", "--name",
                   type=str,
                   default="SIDIS_Workflow",
                   help="Shared_Name base tag for HPP/ROOT product names and log files.\n")
    p.add_argument("-sa", "--skip_acceptance",
                   action="store_true",
                   help="Skip HPP generation. With --HPP_Old_Name, resolve older HPP paths; otherwise children use script defaults.\n")
    p.add_argument("--HPP_Old_Name", "-hon", "-hppOld",
                   type=str,
                   default=None,
                   help="When skipping acceptance, build HPP filenames from this tag instead of --name.\n")
    p.add_argument("-rac", "--run_all_cuts",
                   action="store_true",
                   help="Loop accepted cuts (skips pass1/noSmear and --skip_cut). Forces acceptance OFF. Blocked with pure slurm (use hybrid).\n")
    p.add_argument("-skc", "--skip_cut",
                   nargs="+",
                   default=["cut_Complete_SIDIS"],
                   help="Extra cut names to skip under --run_all_cuts. Default includes cut_Complete_SIDIS. Pass a non-cut token (e.g. None) to skip nothing extra.\n")
    p.add_argument("-us", "--unsmeared",
                   action="store_true",
                   help="Unsmeared reconstructed-MC mode (required for noSmear cut).\n")
    p.add_argument("-nrrw", "--no_run_rho_weight",
                   action="store_true",
                   help="Do not pass --run_rho_weight to Acceptance or Response-pipeline children (default: rho weights ON for production).\n")
    p.add_argument("-rho0", "--rho0_source",
                   type=str,
                   default="lundvpk",
                   choices=["lundvpk", "lundrho"],
                   help="Exclusive-rho MC source for Acceptance when rho weights are ON (default lundvpk). Forwarded as --rho0_source.\n")
    p.add_argument("-cn", "--cut_name",
                   type=str,
                   default=DEFAULT_CUT,
                   help="Single-cut mode cut name (ignored when --run_all_cuts).\n")
    p.add_argument("-m", "--mode",
                   type=str,
                   default="parallel",
                   choices=["parallel", "sequential", "slurm", "hybrid"],
                   help="Response stage mode (default parallel). hybrid: submit SLURM with --yes, then local parallel with -saj (currently flawed; use only after slurm/parallel alignment is fixed). Acceptance is always local.\n")
    p.add_argument("-saj", "--slurm_array_jobid",
                   type=str,
                   default=None,
                   help="Manual SLURM array job ID for parallel/sequential coordination. Hybrid auto-fills per product.\n")
    p.add_argument("-j", "--jobs",
                   type=int,
                   default=5,
                   help="Pipeline --jobs per product (each product may run this many batch jobs).\n")
    p.add_argument("-v", "--verbose",
                   action="store_true",
                   help="Runner-only: also tee one designated child stream to the terminal (all children still go to the master .log).\n")
    p.add_argument("-old3D", "--old_3D_unfold",
                   action="store_true",
                   help="Forward --old_3D_unfold to the pipeline (legacy sparse 3D MultiDim / fixed 915-bin axes).\n")
    return p.parse_args()

# ===================================================================
# EMAIL HELPERS (runner log only — never mutate child message bodies into args.email_message)
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
        time_line = args.timer.time_elapsed(return_Q=True)[-1].replace("\n", " ")
        update_email = f"""{update_message}
{time_line}"""
    if(update_email not in [""]):
        args.email_message = f"{args.email_message}\n{update_email}"
        if((args.verbose or verbose_override) and (verbose_override is not None)):
            print(update_email)

def Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Tasks"):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "user_email_message", "master_log_path", "time_log_path", "master_log_fh", "time_log_fh"]):
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
    if(args.email in ["runner", "all"]):
        if(Crashed or (not Warning)):
            send_email(subject=f"Finished Running the '{Script_Name}' Code" if(not Crashed) else f"CRASH REPORT: '{Script_Name}' Code Failed", body=email_body, recipient="richard.capobianco@uconn.edu")
    print(f"\n\n\n\n{color.BOLD}{color_bg.YELLOW}EMAIL MESSAGE TO SEND:{color.END}\n\n{email_body}\n")
    if(Warning):
        print(f"\n\n{color.BOLD}CONTINUE RUNNING...{color.END}\n\n")
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

def log_print(args, message, also_email=True, no_time=True):
    print(message)
    if(also_email):
        Update_Email(args, update_message=message, verbose_override=None, no_time=no_time)
    if(getattr(args, "master_log_fh", None) is not None):
        try:
            args.master_log_fh.write(ansi_to_plain(message) + "\n")
            args.master_log_fh.flush()
        except Exception:
            pass

# ===================================================================
# HPP PATH RESOLUTION
# ===================================================================
def hpp_tag_for_cut(base_name, cut_name):
    if(cut_name in [None, "", DEFAULT_CUT]):
        return str(base_name)
    return f"{base_name}_{cut_name}"

def hpp_paths_from_tag(name_tag):
    pure = os.path.join(HPP_OUT_DIR, f"generated_acceptance_weights_{name_tag}_noSpline.hpp")
    comb = os.path.join(HPP_OUT_DIR, f"generated_acceptance_weights_{name_tag}_withSpline.hpp")
    return pure, comb

def resolve_hpp_for_cut(args, cut_name):
    # Returns (pure, comb) or (None, None) to let children use defaults.
    if(not args.skip_acceptance):
        tag = hpp_tag_for_cut(args.name, cut_name)
        return hpp_paths_from_tag(tag)
    if(args.HPP_Old_Name in [None, ""]):
        return None, None
    # Prefer old name + cut (when cut is not the default), then base old name.
    candidates = []
    if(cut_name not in [None, "", DEFAULT_CUT]):
        candidates.append(hpp_tag_for_cut(args.HPP_Old_Name, cut_name))
    candidates.append(str(args.HPP_Old_Name))
    for tag in candidates:
        pure, comb = hpp_paths_from_tag(tag)
        if(os.path.isfile(pure) and os.path.isfile(comb)):
            return pure, comb
    tried = ", ".join(candidates)
    raise RuntimeError(f"Acceptance skip with --HPP_Old_Name='{args.HPP_Old_Name}' but no matching HPP pair found for cut='{cut_name}'. Tried tags: {tried}")

def product_shared_name(args, cut_name):
    # Shared_Name is always args.name; non-default cuts append cut so multi-cut outputs do not collide.
    if(cut_name in [None, "", DEFAULT_CUT]):
        return str(args.name)
    return f"{args.name}_{cut_name}"

def product_output_name(product, shared):
    return product["name_fmt"].format(shared=shared)

def child_email_message(user_message, label):
    base = "" if(user_message in [None]) else str(user_message)
    if(label in base):
        return base
    if(base.strip() in [""]):
        return label
    return f"{base} {label}"

def email_children(args):
    return args.email in ["children", "all"]

# ===================================================================
# COMMAND BUILDERS
# ===================================================================
def build_acceptance_cmd(args, spline_on, hpp_out, cut_name):
    cmd = [ACCEPTANCE_SCRIPT]
    cmd.append("--make_2D_weight")
    cmd.extend(["--hpp_output_file", hpp_out])
    name_tag = hpp_tag_for_cut(args.name, cut_name)
    cmd.extend(["--name", name_tag])
    cmd.extend(["-cnR", cut_name, "-cnM", cut_name])
    if(not args.no_run_rho_weight):
        cmd.append("--run_rho_weight")
        cmd.extend(["--rho0_source", str(args.rho0_source)])
    if(spline_on):
        cmd.append("--spline_weights")
        cmd.extend(["--spline_file", args.spline_file])
    if(args.unsmeared):
        cmd.append("--unsmeared")
    if(email_children(args)):
        cmd.append("--email")
        label = f"HPP {'withSpline' if(spline_on) else 'noSpline'}"
        cmd.extend(["--email_message", child_email_message(args.user_email_message, label)])
    return cmd

def product_extra_flags(args, product):
    # Default production extras include --run_rho_weight; strip it when -nrrw is set.
    extra = list(product["extra"] or [])
    if(args.no_run_rho_weight):
        extra = [e for e in extra if(e != "--run_rho_weight")]
    return extra

def build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode=None, saj=None, auto_yes=False):
    # IMPORTANT: --extra is argparse.REMAINDER in the pipeline — put all pipeline-owned flags before it or they get swallowed and forwarded to Response_Matrix.
    cmd = [PIPELINE_SCRIPT]
    run_mode = args.mode if(mode is None) else mode
    if(run_mode == "hybrid"):
        run_mode = "parallel"
    cmd.extend(["-m", run_mode])
    cmd.extend(["-cn", cut_name])
    shared = product_shared_name(args, cut_name)
    name_tag = product_output_name(product, shared)
    cmd.extend(["-n", name_tag])
    cmd.append("--use_hpp")
    cmd.append("--spline_weights")
    cmd.extend(["--spline_weight_file", args.spline_file])
    if(pure_hpp not in [None, ""]):
        cmd.extend(["--hpp_weight_file", pure_hpp])
    if(comb_hpp not in [None, ""]):
        cmd.extend(["--hpp_weight_file_spline", comb_hpp])
    if(args.unsmeared):
        cmd.append("--unsmeared")
    if(not args.no_run_rho_weight):
        # Pipeline-level -rrw (also kept in product --extra for Response passthrough)
        cmd.append("--run_rho_weight")
    for flag in product["pipeline_flags"]:
        cmd.append(flag)
    if(getattr(args, "old_3D_unfold", False)):
        cmd.append("--old_3D_unfold")
    use_saj = saj if(saj is not None) else args.slurm_array_jobid
    if(use_saj not in [None, ""]):
        cmd.extend(["--slurm_array_jobid", str(use_saj)])
    if(run_mode in ["parallel"]):
        cmd.extend(["--jobs", str(args.jobs)])
    # Hybrid SLURM leg always passes --yes so sbatch is noninteractive. Pure slurm stays interactive.
    if((auto_yes) and (run_mode == "slurm")):
        cmd.append("--yes")
    if(email_children(args) and (run_mode != "slurm")):
        cmd.append("--email")
        cmd.extend(["-emj", child_email_message(args.user_email_message, product["label"])])
    # --extra LAST: only true Response_Matrix passthrough args
    extra = product_extra_flags(args, product)
    if(extra):
        cmd.append("--extra")
        cmd.extend(extra)
    return cmd

# ===================================================================
# PROCESS LAUNCH + LOGGING
# ===================================================================
def format_peak_memory():
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

def write_time_entry(args, task_label, cut_name, mode, rc, wall_s, extra=""):
    if(getattr(args, "time_log_fh", None) is None):
        return
    lines = [
        f"=== TASK: {task_label} | cut={cut_name} | mode={mode} | rc={rc} ===",
        f"wall_time: {wall_s:.2f} s",
        f"peak_memory: {format_peak_memory()}",
    ]
    if(extra not in [None, ""]):
        lines.append(str(extra))
    lines.append("")
    try:
        args.time_log_fh.write("\n".join(lines) + "\n")
        args.time_log_fh.flush()
    except Exception:
        pass

CHILD_TAIL_MAX_LINES = 80
CHILD_ERROR_HINTS = ("traceback", "valueerror", "runtimeerror", "error message", "crash warning", "crashed", "exception", "file not found", "syntaxerror")

def stream_child_output(proc, task_label, master_log_fh, tee_terminal, line_buffer=None):
    prefix = f"[{task_label}] "
    try:
        for line in iter(proc.stdout.readline, ""):
            if(line == ""):
                break
            text = f"{prefix}{line}"
            if(line_buffer is not None):
                try:
                    line_buffer.append(text.rstrip("\n"))
                except Exception:
                    pass
            if(master_log_fh is not None):
                try:
                    master_log_fh.write(ansi_to_plain(text))
                    master_log_fh.flush()
                except Exception:
                    pass
            if(tee_terminal):
                sys.stdout.write(text)
                sys.stdout.flush()
    except Exception as exc:
        err = f"{prefix}[stream error] {exc}\n"
        if(line_buffer is not None):
            try:
                line_buffer.append(err.rstrip("\n"))
            except Exception:
                pass
        if(master_log_fh is not None):
            try:
                master_log_fh.write(err)
                master_log_fh.flush()
            except Exception:
                pass

def format_child_failure_snippet(job, max_lines=CHILD_TAIL_MAX_LINES):
    # Prefer error-looking lines, then fall back to the last N buffered lines.
    buf = list(job.get("line_buffer") or [])
    if(not buf):
        return f"(no child output captured for {job.get('task_label', 'unknown')})"
    hint_lines = []
    for line in buf:
        plain = ansi_to_plain(line).lower()
        if(any(h in plain for h in CHILD_ERROR_HINTS)):
            hint_lines.append(line)
    # Include a small window of context after the first traceback-like line when present.
    if(hint_lines):
        try:
            first_idx = next(i for i, line in enumerate(buf) if(any(h in ansi_to_plain(line).lower() for h in ("traceback", "crash warning", "error message", "valueerror", "runtimeerror"))))
            window = buf[first_idx:min(len(buf), first_idx + max_lines)]
            body = "\n".join(window)
        except StopIteration:
            body = "\n".join(hint_lines[-max_lines:])
    else:
        body = "\n".join(buf[-max_lines:])
    return body

def launch_cmd(args, cmd, task_label, tee_terminal=False):
    cmd_str = " ".join(str(c) for c in cmd)
    log_print(args, f"{color.BBLUE}CMD [{task_label}]:{color.END} {cmd_str}")
    start = time.time()
    line_buffer = deque(maxlen=CHILD_TAIL_MAX_LINES)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=DATAFRAMES_DIR, text=True, bufsize=1)
    reader = threading.Thread(target=stream_child_output, args=(proc, task_label, args.master_log_fh, tee_terminal, line_buffer), daemon=True)
    reader.start()
    return {"proc": proc, "reader": reader, "task_label": task_label, "start": start, "cmd": cmd, "line_buffer": line_buffer}

def wait_launched(args, job, cut_name, mode):
    rc = job["proc"].wait()
    try:
        job["reader"].join(timeout=5.0)
    except Exception:
        pass
    wall = time.time() - job["start"]
    write_time_entry(args, job["task_label"], cut_name, mode, rc, wall)
    msg = f"{color.BBLUE}DONE [{job['task_label']}] cut={cut_name} rc={rc} wall={wall:.1f}s{color.END}"
    if(rc != 0):
        msg = f"{color.Error}FAIL [{job['task_label']}] cut={cut_name} rc={rc} wall={wall:.1f}s{color.END}"
        snippet = format_child_failure_snippet(job)
        msg = f"""{msg}
{color.BYELLOW}--- child output snippet ({job['task_label']}) ---{color.END}
{snippet}
{color.BYELLOW}--- end child output snippet ---{color.END}"""
    log_print(args, msg, no_time=False)
    return rc

def run_cmd_blocking(args, cmd, task_label, cut_name, mode, tee_terminal=False):
    job = launch_cmd(args, cmd, task_label, tee_terminal=tee_terminal)
    return wait_launched(args, job, cut_name, mode)

def submit_slurm_capture_array_id(args, cmd, task_label, cut_name):
    cmd_str = " ".join(str(c) for c in cmd)
    log_print(args, f"{color.BBLUE}SLURM SUBMIT [{task_label}]:{color.END} {cmd_str}")
    start = time.time()
    proc = subprocess.run(cmd, cwd=DATAFRAMES_DIR, capture_output=True, text=True)
    wall = time.time() - start
    out = (proc.stdout or "") + (proc.stderr or "")
    if(args.master_log_fh is not None):
        try:
            args.master_log_fh.write(f"[{task_label}-slurm]\n{ansi_to_plain(out)}\n")
            args.master_log_fh.flush()
        except Exception:
            pass
    if(args.verbose):
        print(out)
    write_time_entry(args, f"{task_label}-slurm-submit", cut_name, "slurm", proc.returncode, wall)
    if(proc.returncode != 0):
        raise RuntimeError(f"SLURM submission failed for {task_label} (rc={proc.returncode})")
    match = re.search(r"Submitted SLURM array job\s+(\S+)", out)
    if(match is None):
        # Fallback: last parsable job-id-like token from sbatch
        match = re.search(r"(?m)^(\d+)(?:;[\w.-]+)?\s*$", out)
    if(match is None):
        raise RuntimeError(f"Could not parse SLURM array job id from pipeline output for {task_label}")
    array_id = match.group(1).split(";")[0]
    log_print(args, f"{color.BGREEN}Captured SLURM array job id {array_id} for {task_label}{color.END}")
    return array_id

# ===================================================================
# STAGES
# ===================================================================
def select_cuts(args):
    if(args.run_all_cuts):
        skip_extra = set(args.skip_cut or [])
        cuts = []
        for c in ACCEPTED_CUTS:
            if("pass1" in c):
                continue
            if("noSmear" in c):
                continue
            if(c in skip_extra):
                continue
            cuts.append(c)
        return cuts
    return [args.cut_name]

def run_acceptance_stage(args, cuts):
    os.makedirs(HPP_OUT_DIR, exist_ok=True)
    hpp_map = {}
    jobs = []
    for cut_name in cuts:
        pure, comb = resolve_hpp_for_cut(args, cut_name)
        hpp_map[cut_name] = (pure, comb)
        cmd_pure = build_acceptance_cmd(args, spline_on=False, hpp_out=pure, cut_name=cut_name)
        cmd_comb = build_acceptance_cmd(args, spline_on=True,  hpp_out=comb, cut_name=cut_name)
        log_print(args, f"\n{color.BGREEN}Acceptance HPP pair for cut {color.END_B}{cut_name}{color.END}")
        tee0 = bool(args.verbose) and (len(jobs) == 0)
        jobs.append((cut_name, "noSpline", launch_cmd(args, cmd_pure, f"HPP-noSpline-{cut_name}", tee_terminal=tee0)))
        jobs.append((cut_name, "withSpline", launch_cmd(args, cmd_comb, f"HPP-withSpline-{cut_name}", tee_terminal=False)))
    failed = []
    for cut_name, label, job in jobs:
        rc = wait_launched(args, job, cut_name, "acceptance")
        if(rc != 0):
            failed.append(f"{cut_name}:{label}")
    if(failed):
        Crash_Report(args, crash_message=f"Acceptance stage failed for: {failed}", continue_run=False)
    return hpp_map

def run_cmd_interactive(args, cmd, task_label, cut_name, mode):
    # Inherit stdio so SLURM script review + [y/N] prompts work for pure slurm mode.
    cmd_str = " ".join(str(c) for c in cmd)
    log_print(args, f"{color.BBLUE}CMD [{task_label}]:{color.END} {cmd_str}")
    start = time.time()
    proc = subprocess.run(cmd, cwd=DATAFRAMES_DIR)
    wall = time.time() - start
    rc = proc.returncode
    write_time_entry(args, task_label, cut_name, mode, rc, wall)
    msg = f"{color.BBLUE}DONE [{task_label}] cut={cut_name} rc={rc} wall={wall:.1f}s{color.END}"
    if(rc != 0):
        msg = f"{color.Error}FAIL [{task_label}] cut={cut_name} rc={rc} wall={wall:.1f}s{color.END}"
    log_print(args, msg, no_time=False)
    return rc

def run_products_for_cut(args, cut_name, pure_hpp, comb_hpp):
    results = []
    mode = args.mode

    if(mode == "hybrid"):
        # Per product: noninteractive SLURM submit (--yes), capture array id, then parallel with -saj.
        # All three product parallel pipelines run concurrently after their array ids are known.
        array_ids = {}
        for product in PRODUCTS:
            task = product["key"]
            slurm_cmd = build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode="slurm", auto_yes=True)
            array_ids[task] = submit_slurm_capture_array_id(args, slurm_cmd, f"{task}-slurm", cut_name)

        launched = []
        for i, product in enumerate(PRODUCTS):
            task = product["key"]
            par_cmd = build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode="parallel", saj=array_ids[task])
            tee = bool(args.verbose) and (i == 0)
            launched.append((product, launch_cmd(args, par_cmd, f"{task}-parallel", tee_terminal=tee)))
        for product, job in launched:
            rc = wait_launched(args, job, cut_name, "hybrid-parallel")
            results.append((product["key"], rc))
        return results

    if(mode == "sequential"):
        for i, product in enumerate(PRODUCTS):
            cmd = build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode="sequential")
            tee = bool(args.verbose) and (i == 0)
            rc = run_cmd_blocking(args, cmd, product["key"], cut_name, "sequential", tee_terminal=tee)
            results.append((product["key"], rc))
        return results

    if(mode == "slurm"):
        # Interactive per-product approval (stdio inherited; no --yes).
        for product in PRODUCTS:
            cmd = build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode="slurm", auto_yes=False)
            rc = run_cmd_interactive(args, cmd, f"{product['key']}-slurm", cut_name, "slurm")
            results.append((product["key"], rc))
        return results

    # parallel: all products concurrently
    launched = []
    for i, product in enumerate(PRODUCTS):
        cmd = build_pipeline_cmd(args, cut_name, product, pure_hpp, comb_hpp, mode="parallel")
        tee = bool(args.verbose) and (i == 0)
        launched.append((product, launch_cmd(args, cmd, product["key"], tee_terminal=tee)))
    for product, job in launched:
        rc = wait_launched(args, job, cut_name, "parallel")
        results.append((product["key"], rc))
    return results

def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    # Preserve the user-provided email body separately from the runner log.
    args.user_email_message = args.email_message if(args.email_message not in [None]) else ""
    args.email_message = args.user_email_message

    safe_name = re.sub(r"[^\w.\-]+", "_", str(args.name))
    args.master_log_path = os.path.join(DATAFRAMES_DIR, f"{safe_name}_full_pipeline.log")
    args.time_log_path   = os.path.join(DATAFRAMES_DIR, f"{safe_name}_full_pipeline.time")
    args.master_log_fh = open(args.master_log_path, "a")
    args.time_log_fh   = open(args.time_log_path, "a")
    header = f"\n===== {Script_Name} start {datetime.now().isoformat(timespec='seconds')} name={args.name} mode={args.mode} email={args.email} =====\n"
    args.master_log_fh.write(header)
    args.master_log_fh.flush()
    args.time_log_fh.write(header)
    args.time_log_fh.flush()

    log_print(args, f"{color.BBLUE}\n{Script_Name} ready.{color.END}")
    log_print(args, f"  name={args.name}  mode={args.mode}  email={args.email}  skip_acceptance={args.skip_acceptance}  run_all_cuts={args.run_all_cuts}  unsmeared={args.unsmeared}  no_run_rho_weight={args.no_run_rho_weight}  rho0_source={args.rho0_source}")
    log_print(args, f"  master log: {args.master_log_path}")
    log_print(args, f"  time log:   {args.time_log_path}")
    if(args.no_run_rho_weight):
        log_print(args, f"{color.BYELLOW}--no_run_rho_weight: child commands will NOT receive --run_rho_weight{color.END}")
    else:
        log_print(args, f"{color.BBLUE}rho0_source for Acceptance: {color.END_B}{args.rho0_source}{color.END}")

    if((args.run_all_cuts) and (args.mode == "slurm")):
        Crash_Report(args, crash_message="--run_all_cuts is not allowed with pure --mode slurm (job-count limits). Use --mode hybrid to coordinate SLURM then parallel, or use parallel/sequential.", continue_run=False)

    if(args.run_all_cuts):
        args.skip_acceptance = True
        cuts = select_cuts(args)
        log_print(args, f"{color.BYELLOW}--run_all_cuts: acceptance forced OFF; {len(cuts)} cuts (skip_cut={args.skip_cut}){color.END}")
    else:
        cuts = select_cuts(args)
        if(("noSmear" in str(args.cut_name)) and (not args.unsmeared)):
            Crash_Report(args, crash_message="cut_Complete_SIDIS_noSmear requires --unsmeared", continue_run=False)
        if((args.unsmeared) and ("noSmear" not in str(args.cut_name))):
            log_print(args, f"{color.BYELLOW}NOTE: --unsmeared set without noSmear cut; unsmeared columns will still be used.{color.END}")

    # Early HPP resolution check when skipping (fail before any job submit if -hon missing files)
    if(args.skip_acceptance and (args.HPP_Old_Name not in [None, ""])):
        for cut_name in cuts:
            resolve_hpp_for_cut(args, cut_name)

    hpp_map = {}
    if((not args.skip_acceptance) and (not args.run_all_cuts)):
        log_print(args, f"\n{color.BGREEN}=== Stage 1: Acceptance HPP generation ==={color.END}")
        hpp_map = run_acceptance_stage(args, cuts)
    else:
        log_print(args, f"\n{color.BYELLOW}=== Stage 1: Acceptance SKIPPED (-sa / -rac / defaults) ==={color.END}")
        for cut_name in cuts:
            pure, comb = resolve_hpp_for_cut(args, cut_name)
            hpp_map[cut_name] = (pure, comb)
            if(pure not in [None, ""]):
                log_print(args, f"  HPP cut={cut_name}: pure={pure}")
                log_print(args, f"                 comb={comb}")
            else:
                log_print(args, f"  HPP cut={cut_name}: using child-script defaults")

    log_print(args, f"\n{color.BGREEN}=== Stage 2: Response-matrix products ({len(PRODUCTS)} products × {args.jobs} jobs when parallel) ==={color.END}")
    all_failed = []
    task_count = 0
    for cut_name in cuts:
        pure_hpp, comb_hpp = hpp_map.get(cut_name, (None, None))
        log_print(args, f"\n{color.BGREEN}Products for cut {color.END_B}{cut_name}{color.END}")
        results = run_products_for_cut(args, cut_name, pure_hpp, comb_hpp)
        for key, rc in results:
            task_count += 1
            if(rc != 0):
                all_failed.append(f"{cut_name}:{key}(rc={rc})")

    if(all_failed):
        Crash_Report(args, crash_message=f"Some product jobs failed: {all_failed}", continue_run=False)

    Update_Email(args, update_message=f"{color.BGREEN}All pipeline products finished successfully ({task_count} product runs).{color.END}", verbose_override=True, no_time=False)
    Construct_Email(args, final_count=task_count, Count_Type="Product runs")

    try:
        args.master_log_fh.close()
    except Exception:
        pass
    try:
        args.time_log_fh.close()
    except Exception:
        pass

if(__name__ == "__main__"):
    main()
