#!/usr/bin/env python3
import os
import sys
import glob
import shlex
# import shutil
# import socket
import getpass
import argparse
import subprocess
import time
from datetime import datetime

# script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis' if(os.path.exists('/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis')) else ('/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap' if(os.path.exists('/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap')) else os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# sys.path.append(script_dir)
# from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
# sys.path.remove(script_dir)
# del script_dir
_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
from jlab_work_paths import (
    VOLATILE_BASE, add_data_root_argument, apply_output_if_default, bootstrap_from_file,
    dataframe_output_dir, flag_was_passed, print_path_summary, volatile_dataframe_dir,
)
EXEC_ROOT = bootstrap_from_file(__file__)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer

# MAIN_SCRIPT_DEFAULT = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/dataframe_makeROOT_epip_SIDIS.py"
MAIN_SCRIPT_DEFAULT = os.path.join(EXEC_ROOT, "dataframe_makeROOT_epip_SIDIS.py")

# ===================================================================
# PRESET VARIANTS
# ===================================================================
PRESET_VARIANTS = {
    "matching_mc_pass2": {
        "data_type":     "mdf",
        "sidis":         True,
        "job_base":      "mdf_DF_9_2_2026_R1_Final_Thesis_Files",
        "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.*.new10*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new9*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.*rho*.new9*",
        # "job_base":      "mdf_DF_4_26_2026_R1_Final_Analysis_Iterations_I0",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.*.new8*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.*rho*.new8*lundvpk*",
        # # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new8.nb-clasdis-Q2_1.5-9972_*.hipo.root",
    },
    "gen_mc_pass2": {
        "data_type":     "gdf",
        "sidis":         True,
        "job_base":      "gdf_DF_9_2_2026_R1_Final_Thesis_Files",
        "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.*.new10*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new9*",
        # "job_base":      "gdf_DF_4_27_2026_R1_Final_Analysis_Iterations_I0",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.*.new8*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.*rho*.new8*lundvpk*",
        # # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new8.nb-clasdis-Q2_1.5-9972_*.hipo.root",
    },
    "real_data_pass2": {
        "data_type":     "rdf",
        "sidis":         True,
        "job_base":      "rdf_DF_9_2_2026_R1_Final_Thesis_Files",
        "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new10.nSidis_005*",
        # "input_pattern": "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new8.nSidis_00540*.hipo.root",
    },
}

# ===================================================================
# NEW: Group-specific clean output directories
# ===================================================================
# OUTPUT_DIRS = {
#     "rdf": {
#         "work":     "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/REAL_Data",
#         "volatile": "/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/REAL_Data",
#     },
#     "mdf": {
#         "work":     "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Matching_REC_MC",
#         "volatile": "/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Matching_REC_MC",
#     },
#     "gdf": {
#         "work":     "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/GEN_MC",
#         "volatile": "/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/GEN_MC",
#     },
# }
OUTPUT_DIRS = None  # Persistent "work" trees are filled from --data_root at runtime.

# Log subdirectories (always under scratch, grouped by the same names)
LOG_SUBDIRS = {
    "rdf": "REAL_Data",
    "mdf": "Matching_REC_MC",
    "gdf": "GEN_MC",
}

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def parse_args():
    parser = argparse.ArgumentParser(description="run_dataframe_makeROOT_helper.py: Centralized helper for running dataframe_makeROOT_epip_SIDIS.py across many files", formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Verbose printing.\n")
    

    parser.add_argument("-main", "--main_script",
                        type=str,
                        default=MAIN_SCRIPT_DEFAULT,
                        # help="Path to dataframe_makeROOT_epip_SIDIS.py.\n")
                        help=argparse.SUPPRESS)

    parser.add_argument("-i", "--input_pattern",
                        type=str,
                        help="Override the preset file glob / brace pattern.\n")
    parser.add_argument("-il", "--input_list",
                        type=str,
                        default="",
                        help="Text file with one source ROOT path per line (same format as the hybrid *_filelist.txt). Replaces the variant glob. Blank lines and # comments are ignored. --variant still selects data_type, job_base, and output directory.\n")
    parser.add_argument("-o", "--output_location",
                        choices=["work", "volatile"],
                        default="work",
                        help="Where DataFrame ROOT files are written (persistent vs temporary; not which copy of this helper is run).\n  work     : write under --data_root. --data_root work → /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/<rdf|mdf|gdf> ; --data_root work_b → /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/<rdf|mdf|gdf>\n  volatile : write under /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/<rdf|mdf|gdf> (unchanged; --data_root work_b does not send files here)\nUse --data_root work_b with -o work to put persistent DataFrames on the ceph tree. Groovy input globs stay on hallb SIDIS/.\n")

    add_data_root_argument(parser)

    parser.add_argument("-w", "-work", "--work_dir",
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames",
                        help="Override the persistent DataFrames parent directory. Ignored unless given explicitly; otherwise -o work uses --data_root.\n")
    parser.add_argument("-vol", "-volatile", "--volatile_dir",
                        type=str,
                        # default="/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work",
                        default=VOLATILE_BASE,
                        help="Override the volatile output parent directory (used only with -o volatile).\n")
    parser.add_argument("-sld", "-scratch", "--scratch_log_dir",
                        type=str,
                        default="",
                        help="Base directory for logs. If empty, uses /scratch/<username>/dataframe_makeROOT_logs.\n")

    parser.add_argument("-jb", "-job", "--job_base",
                        type=str,
                        default="",
                        help="Override the preset job base name.\n")
    parser.add_argument("-rn", "-run", "--run_name",
                        type=str,
                        default="",
                        help="Optional explicit run subdirectory name.\n")

    parser.add_argument("-plo", "--primary_log_in_output",
                        action="store_true",
                        help="Place the primary job log in the main output directory instead of scratch.\n")

    parser.add_argument("-pji", "--primary_job_index",
                        type=int,
                        default=0,
                        help="Zero-based job index treated as the primary job for log placement.\n")

    parser.add_argument("-check", "--check",
                        action="store_true",
                        help="Stop early if a job exits non-zero.\n")

    parser.add_argument("-t", "-dry", "--dry_run",
                        action="store_true",
                        help="Print commands and planned paths without running them.\n")

    parser.add_argument("-e", "--email",
                        action="store_true",
                        help="Send completion email notification.\n")
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the notification from '--email'.\n")

    parser.add_argument("-dtype", "--data_type",
                        choices=["rdf", "mdf", "gdf", "pdf"],
                        default="",
                        help="Override the preset data_type.\n")
    
    # The following arguments just pass specific commands to the dataframe_makeROOT_epip_SIDIS.py if you don't want to use the default ones set up in the script — the only really relevant one is probably the '--smear_FX' argument, since all the other ones basically control things that either should not be changed or can be more effiecently controlled in later histogram creation scripts
    parser.add_argument("-sidis", "--sidis",
                        action="store_true",
                        help="Pass the '--sidis' flag to the main script.\n")
    parser.add_argument("-mom", "--mom_cor",
                        action="store_true",
                        help="Pass the '--mom-cor' flag to the main script.\n")
    parser.add_argument("-no-mom", "--no_mom_cor",
                        action="store_true",
                        help="Pass the '--no-mom-cor' flag to the main script.\n")
    parser.add_argument("-TP", "--tag_proton",
                        action="store_true",
                        help="Pass the '--tag-proton' flag to the main script.\n")
    parser.add_argument("-nsmear", "--no_smear",
                        action="store_true",
                        help="Pass the '--no-smear' flag to the main script.\n")
    parser.add_argument("-uw", "--use_weight",
                        choices=["None", "mod", "close", "closure", "weighed", "use_weight", "Q4"],
                        default="",
                        help="Optional value for the main script's '--use-weight'.\n")
    parser.add_argument("-SF", "--smear_factor",
                        type=float,
                        default=None,
                        help="Optional value for '--smear-factor'.\n")

    parser.add_argument("-SFFX", "--smear_FX",
                        action="store_true",
                        help="Pass '--smear-FX' to the main script.\n")

    parser.add_argument("-pver", "--pass_version",
                        choices=[1, 2],
                        type=int,
                        default=None,
                        help="Optional value for '--pass-version'.\n")
    parser.add_argument("-old-pass", "--old_pass",
                        action="store_true",
                        help="Pass '--old_pass' to the main script.\n")
    parser.add_argument("-sfid", "--skip_fiducial",
                        choices=[f"FC{i}" for i in range(0, 10)] + [f"FC_{i}" for i in range(10, 15)] + ["None"],
                        default="",
                        help="Optional value for '--skip-fiducial'.\n")


    # The following arguments just pass specific commands to the dataframe_makeROOT_epip_SIDIS.py, but these may be slightly more useful than the above ones...
    parser.add_argument("-evt", "--events",
                        type=int,
                        default=None,
                        help="Optional value for '--events'.\n")
    parser.add_argument("-cuts", "--cuts",
                        type=str,
                        default="",
                        help="Optional cut string for '--cuts'.\n")
    parser.add_argument("-cc", "--count_cuts",
                        action="store_true",
                        help="Pass '--count-cuts' to the main script.\n")
    parser.add_argument("-out", "--output_type",
                        choices=["histo", "data", "tree", "test", "time"],
                        default="",
                        help="Optional value for '--output-type'.\n")

    parser.add_argument("-sn", "--save_name",
                        type=str,
                        default="",
                        help="Optional value for '--save_name'.\n")

    parser.add_argument("-cn", "--common_name",
                        type=str,
                        default="Final_Thesis_Files_",
                        help="Optional value for '--Common_Name'.\n")

    parser.add_argument("-mac", "--matching_criteria",
                        choices=["", "P12T6", "P8T6", "P10T8", "Bank"],
                        default="",
                        help="Optional value for '--matching_criteria'.\n")

    parser.add_argument("-eg", "--exclude_groups",
                        nargs="+",
                        default=[],
                        help="Optional values for '--exclude-groups'.\n")



    
    parser.add_argument("-V", "--variant",
                        choices=list(PRESET_VARIANTS.keys()),
                        default="matching_mc_pass2",
                        help=f"{color.BOLD}Preset workflow variant replacing the original Bash wrappers.{color.END}\n")

    parser.add_argument("-m", "--mode",
                        choices=["sequential", "parallel", "slurm", "hybrid"],
                        default="parallel",
                        help="Job execution mode. hybrid: submit the same file-job list to SLURM then process remaining jobs locally in parallel.\n")
    parser.add_argument("-st", "--slurm_time",
                        default="01:00:00",
                        help="SLURM time limit per array task.\n")
    parser.add_argument("-sm", "--slurm_mem",
                        default="4GB",
                        help="SLURM mem-per-cpu.\n")
    parser.add_argument("-saj", "--slurm_array_jobid",
                        type=str,
                        default=None,
                        help="Optional SLURM array job ID for hybrid local coordination.\n")
    parser.add_argument("-y", "--yes",
                        action="store_true",
                        help="Noninteractive approval for SLURM script submission (skip [y/N] prompt).\n")

    parser.add_argument("-j", "--max_jobs",
                        type=int,
                        default=10,
                        help="Maximum simultaneous jobs in parallel mode.\n")

    parser.add_argument("-test", "--test",
                        action="store_true",
                        help="Pass '--test' to the main script.\n")
    
    parser.add_argument("-hs", "--help_script",
                        action="store_true",
                        help="Shows the --help message of the main script then exits.\n")

    parser.add_argument("-extra", "--extra_main_args",
                        nargs=argparse.REMAINDER,
                        default=[],
                        help="Extra arguments appended verbatim to the main script command.\n")

    return parser.parse_args()

import re
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
    Script_Name = "run_dataframe_makeROOT_helper.py"
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "help_script"]):
            continue
        if((str(name) in ["extra_main_args"]) and (len(getattr(args, "extra_main_args", [])) < 1)):
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
    options, current = [], []
    depth  = 0
    for char in body:
        if((char == ",") and (depth == 0)):
            options.append("".join(current))
            current = []
            continue
        depth += 1 if(char == "{") else -1 if(char == "}") else 0
        current.append(char)
    options.append("".join(current))
    expanded_patterns = []
    for option in options:
        expanded_patterns.extend(expand_brace_patterns(f"{prefix}{option}{suffix}"))
    return expanded_patterns

def build_file_list(target_pattern):
    if(os.path.isdir(target_pattern)):
        files = []
        for name in os.listdir(target_pattern):
            filepath = os.path.join(target_pattern, name)
            if(os.path.isfile(filepath)):
                files.append(filepath)
        return sorted(files)
    expanded_targets = expand_brace_patterns(target_pattern)
    files = []
    seen  = set()
    for expanded_target in expanded_targets:
        for filepath in glob.glob(expanded_target):
            if(os.path.isfile(filepath) and (filepath not in seen)):
                files.append(filepath)
                seen.add(filepath)
    return sorted(files)

def build_file_list_from_input_list(list_path):
    files, seen = [], set()
    with open(list_path, "r") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if((line == "") or line.startswith("#")):
                continue
            if(line not in seen):
                seen.add(line)
                files.append(line)
    return files

def default_scratch_log_dir():
    username = getpass.getuser()
    scratch_base = f"/scratch/{username}"
    return os.path.join(scratch_base, "dataframe_makeROOT_logs")

def choose_variant_settings(args):
    variant_settings = dict(PRESET_VARIANTS[args.variant])
    # Argument Overides of PRESET_VARIANTS
    if(args.data_type):
        variant_settings["data_type"] = args.data_type
    if(args.input_pattern):
        variant_settings["input_pattern"] = args.input_pattern
    if(args.job_base):
        variant_settings["job_base"] = args.job_base
    if(args.sidis):
        variant_settings["sidis"] = True
    return variant_settings

# ===================================================================
# UPDATED: Clean group-specific directories
# ===================================================================
def resolve_output_dir(args, variant_settings):
    # Returns the exact output folder for the chosen data_type + output_location.
    data_type = variant_settings["data_type"]
    # if data_type in OUTPUT_DIRS and args.output_location in OUTPUT_DIRS[data_type]:
    #     return OUTPUT_DIRS[data_type][args.output_location]
    # return args.work_dir if(args.output_location == "work") else args.volatile_dir
    subdir = LOG_SUBDIRS.get(data_type, data_type)
    if(args.output_location == "volatile"):
        if(flag_was_passed(["-vol", "-volatile", "--volatile_dir"])):
            if(os.path.basename(args.volatile_dir) == subdir):
                return args.volatile_dir
            return os.path.join(args.volatile_dir, subdir)
        return volatile_dataframe_dir(data_type)
    if(flag_was_passed(["-w", "-work", "--work_dir"])):
        if(os.path.basename(args.work_dir) == subdir):
            return args.work_dir
        return os.path.join(args.work_dir, subdir)
    return dataframe_output_dir(args.data_root, data_type)

def resolve_log_dir(args, variant_settings):
    # Logs ALWAYS go to scratch (never volatile) and are grouped by the same subfolder name.
    data_type = variant_settings["data_type"]
    log_base_dir = args.scratch_log_dir if(args.scratch_log_dir) else default_scratch_log_dir()
    subdir = LOG_SUBDIRS.get(data_type, data_type)
    return os.path.join(log_base_dir, subdir)

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)
    return path

def sanitize_name(text):
    cleaned = str(text).replace(" ", "_")
    cleaned = cleaned.replace("/", "_")
    return cleaned

def build_main_command(args, variant_settings, input_file):
    command = [args.main_script, variant_settings["data_type"]]
    if(variant_settings.get("sidis", False)):
        command.append("--sidis")
    if(args.mom_cor):
        command.append("--mom-cor")
    if(args.no_mom_cor):
        command.append("--no-mom-cor")
    if(args.tag_proton):
        command.append("--tag-proton")
    if(args.no_smear):
        command.append("--no-smear")
    if(args.smear_FX):
        command.append("--smear-FX")
    if(args.old_pass):
        command.append("--old_pass")
    if(args.count_cuts):
        command.append("--count-cuts")
    if(args.test):
        command.append("--test")
    if(args.output_type):
        command.extend(["--output-type", args.output_type])
    if(args.use_weight):
        command.extend(["--use-weight", args.use_weight])
    if(args.smear_factor is not None):
        command.extend(["--smear-factor", str(args.smear_factor)])
    if(args.pass_version is not None):
        command.extend(["--pass-version", str(args.pass_version)])
    if(args.skip_fiducial):
        command.extend(["--skip-fiducial", args.skip_fiducial])
    if(args.events is not None):
        command.extend(["--events", str(args.events)])
    if(args.cuts):
        command.extend(["--cuts", args.cuts])
    if(args.save_name):
        command.extend(["--save_name", args.save_name])
    if(args.common_name):
        command.extend(["--Common_Name", args.common_name])
    if(args.matching_criteria):
        command.extend(["--matching_criteria", args.matching_criteria])
    if(len(args.exclude_groups) > 0):
        command.append("--exclude-groups")
        command.extend(args.exclude_groups)

    command.extend(["--file", input_file])
    if(len(args.extra_main_args) > 0):
        extra_arguments = list(args.extra_main_args)
        if((len(extra_arguments) > 0) and (extra_arguments[0] == "--")):
            extra_arguments = extra_arguments[1:]
        command.extend(extra_arguments)
    return command

def format_command(command):
    return " ".join(shlex.quote(part) for part in command)

def build_log_paths(log_dir, output_dir, job_base, file_index, input_file, primary_in_output, primary_job_index):
    base_name = sanitize_name(os.path.basename(input_file))
    log_name  = f"{job_base}_{file_index:05d}_{base_name}.log"
    err_name  = f"{job_base}_{file_index:05d}_{base_name}.err"
    primary_dir = output_dir if(primary_in_output and (file_index == primary_job_index)) else log_dir
    log_path    = os.path.join(primary_dir, log_name)
    err_path    = os.path.join(primary_dir, err_name)
    return log_path, err_path


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


def build_email_summary(args, variant_settings, files, results, output_dir, log_dir, Peak_Mem=None):
    total_jobs  = len(results)
    done_jobs   = sum(1 for result in results if(result["returncode"] == 0))
    fail_jobs   = sum(1 for result in results if(result["returncode"] != 0))
    lines = ["Run Report Message:"]
    lines.append(f"Data Type:       {variant_settings['data_type']}")
    lines.append(f"Files Requested: {len(files)}")
    lines.append(f"Files Run:       {total_jobs}")
    lines.append(f"Files Succeeded: {done_jobs}")
    lines.append(f"Files Failed:    {fail_jobs}")
    lines.append(f"Output Dir:      {output_dir}")
    lines.append(f"Log Dir:         {log_dir}")
    if(Peak_Mem is not None):
        lines.append(f"Peak Mem Used:   {Peak_Mem}")
    Update_Email(args, update_message="\n".join(lines), verbose_override=None, no_time=True) # `verbose_override=None` forces the function to suppress the print message even if `verbose` is `True`
    Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Files")

def print_run_header(args, variant_settings, files, output_dir, log_dir):
    print(f"""{color.BBLUE}
========================================
Running dataframe helper
========================================
{color.END}""")
    print_path_summary(EXEC_ROOT, args.data_root)
    print(f"{color.BOLD}Output Location:{color.END}   {args.output_location}")
    print(f"{color.BOLD}Variant:{color.END}           {args.variant}")
    print(f"{color.BOLD}Mode:{color.END}              {args.mode}")
    print(f"{color.BOLD}Data Type:{color.END}         {variant_settings['data_type']}")
    print(f"{color.BOLD}Job Base:{color.END}          {variant_settings['job_base']}")
    print(f"{color.BOLD}Input Pattern:{color.END}     {variant_settings['input_pattern']}")
    print(f"{color.BOLD}Files Found:{color.END}       {len(files)}")
    print(f"{color.BOLD}Output Dir:{color.END}        {output_dir}")
    print(f"{color.BOLD}Log Dir:{color.END}           {log_dir}")
    print(f"{color.BOLD}Main Script:{color.END}       {args.main_script}")
    print(f"{color.BOLD}Matching Criteria:{color.END} {args.matching_criteria if(args.matching_criteria) else '<default>'}")
    print("")



SLURM_ARRAY_CHECK_DISABLED = False
_SQUEUE_SNAPSHOT_LOGGED = set()
_SQUEUE_COMPACT_STATES = set(["PD", "R", "CG", "CF", "CD", "CA", "F", "TO", "PR", "S", "ST", "NF", "SE", "OOM", "DL", "SO", "RF", "RQ", "RS", "RV", "RD", "RH"])

def slurm_array_expr_contains(expr, task_index):
    # SLURM compact index expression: "1-171", "1-10,20,30-40", optional ":step" and "%N" concurrency.
    task_index = int(task_index)
    expr = str(expr).split("%", 1)[0]
    for part in expr.split(","):
        part = part.strip()
        if(part == ""):
            continue
        if(":" in part):
            range_part, step_s = part.split(":", 1)
            step = int(step_s)
        else:
            range_part, step = part, 1
        if("-" in range_part):
            lo_s, hi_s = range_part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if((lo <= task_index <= hi) and (((task_index - lo) % step) == 0)):
                return True
        elif(int(range_part) == task_index):
            return True
    return False

def squeue_job_id_covers_task(job_id, array_jobid, task_index):
    job_id = str(job_id).strip()
    array_jobid = str(array_jobid).strip()
    task_index = int(task_index)
    if(job_id == array_jobid):
        return True
    if(job_id == f"{array_jobid}_{task_index}"):
        return True
    prefix = f"{array_jobid}_["
    if(job_id.startswith(prefix) and job_id.endswith("]")):
        return slurm_array_expr_contains(job_id[len(prefix):-1], task_index)
    return False

def _run_squeue(array_jobid, fmt=None, retries=4, delay=1.0):
    cmd = ["squeue", "-h", "-r", "-j", str(array_jobid)]
    if(fmt not in [None, ""]):
        cmd.extend(["-o", str(fmt)])
    last = None
    for attempt in range(int(retries)):
        try:
            last = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception:
            return None
        if(last.returncode != 0):
            return last
        if((last.stdout or "").strip() != ""):
            return last
        if(attempt < (int(retries) - 1)):
            time.sleep(delay)
    return last

def _log_squeue_snapshot(array_jobid, raw):
    key = str(array_jobid)
    if(key in _SQUEUE_SNAPSHOT_LOGGED):
        return
    _SQUEUE_SNAPSHOT_LOGGED.add(key)
    text = (raw or "").strip() or "<empty>"
    print(f"{color.BBLUE}[INFO]{color.END} squeue snapshot for array {array_jobid}:\n{text}")

def _squeue_line_fields(line):
    parts = str(line).split()
    if(len(parts) < 2):
        return None
    if((len(parts) >= 3) and (parts[2] in _SQUEUE_COMPACT_STATES)):
        return parts[0], parts[1], parts[2]
    if(parts[1] in _SQUEUE_COMPACT_STATES):
        return parts[0], None, parts[1]
    if((len(parts) >= 5) and (parts[4] in _SQUEUE_COMPACT_STATES)):
        return parts[0], None, parts[4]
    return None

def _task_field_covers(task_field, task_index):
    if(task_field in [None, ""]):
        return False
    tf = str(task_field).strip()
    if(tf == str(int(task_index))):
        return True
    if(tf.startswith("[") and tf.endswith("]")):
        return slurm_array_expr_contains(tf[1:-1], task_index)
    return slurm_array_expr_contains(tf, task_index)

def _parse_squeue_task_state(array_jobid, task_index, *outputs):
    task_index = int(task_index)
    array_jobid = str(array_jobid).strip()
    individual_non_pd = None
    pending_whole_array = False
    for raw in outputs:
        if(raw in [None, ""]):
            continue
        for line in str(raw).strip().splitlines():
            fields = _squeue_line_fields(line)
            if(fields is None):
                continue
            job_id, task_field, state = fields
            tf_covers = _task_field_covers(task_field, task_index)
            id_covers = squeue_job_id_covers_task(job_id, array_jobid, task_index)
            if((job_id == array_jobid) and (task_field not in [None, ""]) and (not tf_covers)):
                id_covers = False
            covers = id_covers or tf_covers
            exact = (job_id == f"{array_jobid}_{task_index}") or (str(task_field).strip() == str(task_index))
            if((job_id == array_jobid) and (task_field in [None, ""]) and (state == "PD")):
                pending_whole_array = True
            if(not covers):
                continue
            if(exact and (state != "PD")):
                return state
            if(state != "PD"):
                individual_non_pd = state
            else:
                return "PD"
    if(individual_non_pd not in [None, ""]):
        return individual_non_pd
    if(pending_whole_array):
        return "PD"
    return None

def query_slurm_array_task_state(array_jobid, batch_index):
    global SLURM_ARRAY_CHECK_DISABLED
    if(SLURM_ARRAY_CHECK_DISABLED):
        return "IGNORE"
    default_proc = _run_squeue(array_jobid, fmt=None)
    if(default_proc is None):
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    if(default_proc.returncode != 0):
        SLURM_ARRAY_CHECK_DISABLED = True
        return "IGNORE"
    _log_squeue_snapshot(array_jobid, default_proc.stdout)
    fmt_proc = _run_squeue(array_jobid, fmt="%F %K %t", retries=1, delay=0.0)
    fmt_out = ""
    if((fmt_proc is not None) and (fmt_proc.returncode == 0)):
        fmt_out = fmt_proc.stdout or ""
    return _parse_squeue_task_state(array_jobid, batch_index, fmt_out, default_proc.stdout)

def cancel_slurm_array_task(array_jobid, task_index):
    job_str = f"{array_jobid}_{task_index}"
    try:
        subprocess.run(["scancel", job_str], check=False)
        print(f"{color.BBLUE}[INFO]{color.END} Cancelled SLURM array task {job_str}")
    except Exception:
        pass

def slurm_array_has_active_tasks(array_jobid):
    if(array_jobid in [None, ""]):
        return False
    proc = _run_squeue(array_jobid, fmt=None, retries=1, delay=0.0)
    if((proc is None) or (proc.returncode != 0)):
        return False
    return (proc.stdout or "").strip() != ""

def should_skip_file_due_to_slurm(args, task_index):
    # task_index is 1-based to match SLURM_ARRAY_TASK_ID.
    if(getattr(args, "slurm_array_jobid", None) in [None, ""]):
        return False
    state = query_slurm_array_task_state(args.slurm_array_jobid, task_index)
    if(state == "IGNORE"):
        return False
    target_id = f"{args.slurm_array_jobid}_{task_index}"
    if(state is None):
        print(f"{color.BBLUE}[INFO]{color.END} File job {task_index} already completed by SLURM - skipping")
        return True
    if(state == "PD"):
        print(f"{color.BBLUE}[INFO]{color.END} Cancelling pending SLURM task {target_id}")
        cancel_slurm_array_task(args.slurm_array_jobid, task_index)
        return False
    print(f"{color.BBLUE}[INFO]{color.END} File job {task_index} is {state} in SLURM - skipping")
    return True

def wait_for_remaining_slurm_tasks(args):
    if(getattr(args, "slurm_array_jobid", None) in [None, ""]):
        return
    while(slurm_array_has_active_tasks(args.slurm_array_jobid)):
        print(f"{color.BBLUE}[INFO]{color.END} Waiting for remaining SLURM array tasks of {args.slurm_array_jobid}...")
        time.sleep(30.0)

def write_hybrid_filelist(output_dir, job_base, files):
    list_path = os.path.join(output_dir, f"{job_base}_filelist.txt")
    with open(list_path, "w") as fh:
        for input_file in files:
            fh.write(f"{input_file}\n")
    return list_path

def run_slurm_mode(args, variant_settings, files, output_dir, log_dir, auto_yes=False):
    job_base = variant_settings["job_base"]
    nfiles = len(files)
    list_path = write_hybrid_filelist(output_dir, job_base, files)
    array_script = os.path.join(output_dir, f"slurm_array_{job_base}.sh")
    example_cmd = build_main_command(args, variant_settings, files[0])
    cmd_template = build_main_command(args, variant_settings, "${INPUT_FILE}")
    cmd_line = " ".join(shlex.quote(part) if(part != "${INPUT_FILE}") else '"${INPUT_FILE}"' for part in cmd_template)
    with open(array_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --ntasks=1\n")
        f.write(f"#SBATCH --job-name={job_base}\n")
        f.write("#SBATCH --mail-type=ALL\n")
        f.write("#SBATCH --mail-user=richard.capobianco@uconn.edu\n")
        f.write("#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out\n")
        f.write("#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err\n")
        f.write("#SBATCH --partition=production\n")
        f.write("#SBATCH --account=clas12\n")
        f.write(f"#SBATCH --mem-per-cpu={args.slurm_mem}\n")
        f.write(f"#SBATCH --time={args.slurm_time}\n")
        f.write(f"#SBATCH --array=1-{nfiles}\n\n")
        f.write(f'FILELIST="{list_path}"\n')
        f.write('INPUT_FILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${FILELIST}")\n')
        f.write(f'cd {shlex.quote(output_dir)}\n')
        f.write(f"{cmd_line}\n")
    os.chmod(array_script, 0o755)
    print(f"\n{color.BBLUE}[INFO]{color.END} Proposed SLURM array script:\n")
    with open(array_script) as f:
        print(f.read())
    print(f"{color.BBLUE}[INFO]{color.END} Example local-equivalent command:\n  {format_command(example_cmd)}\n")
    if(auto_yes or getattr(args, "yes", False)):
        response = "y"
        print(f"\n{color.BBLUE}[INFO]{color.END} --yes set: auto-approving SLURM submission.")
    else:
        try:
            response = input("\nApprove and submit this SLURM script? [y/N]: ").strip().lower()
        except EOFError:
            response = "n"
    if(response not in ["y", "yes"]):
        print(f"{color.Error}[ERROR]{color.END} SLURM script not approved. Exiting.")
        sys.exit(0)
    proc = subprocess.run(["sbatch", "--parsable", array_script], capture_output=True, text=True)
    array_id = (proc.stdout or "").strip()
    if(proc.returncode != 0 or array_id in [None, ""]):
        err = (proc.stderr or proc.stdout or "").strip()
        Crash_Report(args, crash_message=f"sbatch failed (rc={proc.returncode}): {err}", continue_run=False)
    Update_Email(args, update_message=f"{color.BGREEN}Submitted SLURM array job {array_id} for {nfiles} file jobs{color.END}", verbose_override=True, no_time=True)
    return array_id

def run_sequential(args, variant_settings, files, output_dir, log_dir):
    results  = []
    job_base = variant_settings["job_base"]
    for file_index, input_file in enumerate(files):
        command = build_main_command(args, variant_settings, input_file)
        log_path, err_path = build_log_paths(log_dir, output_dir, job_base, file_index, input_file, args.primary_log_in_output, args.primary_job_index)
        Update_Email(args, update_message=f"{color.BCYAN}START{color.END}: {file_index + 1:>3} of {len(files)}  ->  {os.path.basename(input_file)}", verbose_override=True, no_time=False)
        if(args.verbose):
            print(f"        CMD: {format_command(command)}")
            print(f"        LOG: {log_path}")
            print(f"        ERR: {err_path}")
        result = {"index":      file_index,
                  "input_file": input_file,
                  "command":    command,
                  "log_path":   log_path,
                  "err_path":   err_path,
                  "returncode": 0,
                }
        if(args.dry_run):
            results.append(result)
            continue
        with(open(log_path, "w")) as log_handle, open(err_path, "w") as err_handle:
            log_handle.write(f"# {format_command(command)}\n")
            log_handle.flush()
            completed = subprocess.run(command, stdout=log_handle, stderr=err_handle, cwd=output_dir, check=False)
            result["returncode"] = completed.returncode
        if(result["returncode"] == 0):
            Update_Email(args, update_message=f"{color.BGREEN}DONE {color.END}: {file_index + 1:>3} of {len(files)}", verbose_override=True, no_time=False)
            print()
        elif(args.check):
            results.append(result)
            Crash_Report(args, crash_message=f"{color.Error}FAIL {color.END}: {file_index + 1:>3} of {len(files)}  (rc={result['returncode']})\nUsed the '--check' argument to force a crash here.", continue_run=True)
            break
        else:
            Update_Email(args, update_message=f"{color.Error}FAIL {color.END}: {file_index + 1:>3} of {len(files)}  (rc={result['returncode']})", verbose_override=True, no_time=False)
        results.append(result)
    return results

def run_parallel(args, variant_settings, files, output_dir, log_dir):
    results      = []
    running_jobs = []
    job_base     = variant_settings["job_base"]
    max_jobs     = args.max_jobs if(args.max_jobs > 0) else 1
    next_index   = 0

    def start_job(file_index, input_file):
        if(should_skip_file_due_to_slurm(args, file_index + 1)):
            Update_Email(args, update_message=f"{color.BBLUE}SKIP {color.END}: {file_index + 1:>3} of {len(files)}  (SLURM owns this file job)", verbose_override=True, no_time=False)
            return
        command = build_main_command(args, variant_settings, input_file)
        log_path, err_path = build_log_paths(log_dir, output_dir, job_base, file_index, input_file, args.primary_log_in_output, args.primary_job_index)
        Update_Email(args, update_message=f"{color.BCYAN}START{color.END}: {file_index + 1:>3} of {len(files)}  ->  {os.path.basename(input_file)}", verbose_override=True, no_time=False)
        if(args.verbose):
            print(f"        CMD: {format_command(command)}")
            print(f"        LOG: {log_path}")
            print(f"        ERR: {err_path}")
        result = {"index":      file_index,
                  "input_file": input_file,
                  "command":    command,
                  "log_path":   log_path,
                  "err_path":   err_path,
                  "returncode": 0,
                }
        if(args.dry_run):
            results.append(result)
            return
        log_handle = open(log_path, "w")
        err_handle = open(err_path, "w")
        log_handle.write(f"# {format_command(command)}\n")
        log_handle.flush()
        process = subprocess.Popen(command, stdout=log_handle, stderr=err_handle, cwd=output_dir)
        running_jobs.append({"process":    process,
                             "log_handle": log_handle,
                             "err_handle": err_handle,
                             "result":     result,
                            })

    def finish_job(job_item):
        process = job_item["process"]
        return_code = process.poll()
        if(return_code is None):
            return False
        job_item["result"]["returncode"] = return_code
        try:
            job_item["log_handle"].close()
        except Exception:
            pass
        try:
            job_item["err_handle"].close()
        except Exception:
            pass
        if(return_code == 0):
            Update_Email(args, update_message=f"{color.BGREEN}DONE {color.END}: {job_item['result']['index'] + 1:>3} of {len(files)}", verbose_override=True, no_time=False)
        else:
            Update_Email(args, update_message=f"{color.Error}FAIL {color.END}: {job_item['result']['index'] + 1:>3} of {len(files)}  (rc={return_code})", verbose_override=True, no_time=False)
        results.append(job_item["result"])
        return True
    
    if(args.dry_run):
        for file_index, input_file in enumerate(files):
            start_job(file_index, input_file)
        return sorted(results, key=lambda item: item["index"])
    
    while((next_index < len(files)) or (len(running_jobs) > 0)):
        while((next_index < len(files)) and (len(running_jobs) < max_jobs)):
            start_job(next_index, files[next_index])
            next_index += 1
        finished_index = None
        for running_index, job_item in enumerate(running_jobs):
            if(finish_job(job_item)):
                finished_index = running_index
                break
        if(finished_index is not None):
            finished_job = running_jobs.pop(finished_index)
            if((finished_job["result"]["returncode"] != 0) and args.check):
                for job_item in running_jobs:
                    try:
                        if(job_item["process"].poll() is None):
                            job_item["process"].terminate()
                    except Exception:
                        pass
                time.sleep(0.5)
                for job_item in running_jobs:
                    try:
                        if(job_item["process"].poll() is None):
                            job_item["process"].kill()
                    except Exception:
                        pass
                    try:
                        job_item["log_handle"].close()
                    except Exception:
                        pass
                    try:
                        job_item["err_handle"].close()
                    except Exception:
                        pass
                break
        else:
            time.sleep(0.50)
    wait_for_remaining_slurm_tasks(args)
    return sorted(results, key=lambda item: item["index"])


def main():
    args = parse_args()
    if(not flag_was_passed(["-main", "--main_script"])):
        args.main_script = MAIN_SCRIPT_DEFAULT
    apply_output_if_default(args, "work_dir", ["-w", "-work", "--work_dir"], args.data_root)
    if(args.help_script):
        print(f"\n\n{color.BBLUE}PRINTING THE '--help' MESSAGE FROM THE MAIN SCRIPT...{color.END}\n")
        # subprocess.run(["python3", MAIN_SCRIPT_DEFAULT, "-h"], check=False)
        subprocess.run(["python3", args.main_script, "-h"], check=False)
        sys.exit(0)
    args.timer = RuntimeTimer()
    args.timer.start()
    variant_settings = choose_variant_settings(args)
    if(args.input_list not in ["", None]):
        if(not os.path.isfile(args.input_list)):
            print(f"{color.Error}Input list not found:{color.END} {args.input_list}")
            return
        files = build_file_list_from_input_list(args.input_list)
        variant_settings["input_pattern"] = args.input_list
        if(len(files) == 0):
            print(f"{color.Error}No files found for:{color.END} {args.input_list}")
            return
    else:
        files = build_file_list(variant_settings["input_pattern"])
        if(len(files) == 0):
            print(f"{color.Error}No files found for:{color.END} {variant_settings['input_pattern']}")
            return
    output_dir = ensure_directory(resolve_output_dir(args, variant_settings))
    log_dir    = ensure_directory(resolve_log_dir(args, variant_settings))
    print_run_header(args, variant_settings, files, output_dir, log_dir)
    if(args.primary_job_index < 0):
        args.primary_job_index = 0
    if(args.primary_job_index >= len(files)):
        args.primary_job_index = 0
    if(args.mode == "hybrid"):
        array_id = run_slurm_mode(args, variant_settings, files, output_dir, log_dir, auto_yes=True)
        args.slurm_array_jobid = array_id
        results = run_parallel(args, variant_settings, files, output_dir, log_dir)
    elif(args.mode == "slurm"):
        run_slurm_mode(args, variant_settings, files, output_dir, log_dir, auto_yes=False)
        Construct_Email(args)
        return
    elif(args.mode == "parallel"):
        results = run_parallel(args, variant_settings, files, output_dir, log_dir)
    else:
        results = run_sequential(args, variant_settings, files, output_dir, log_dir)
    print(f"{color.BOLD}Run complete.{color.END}")
    # === NEW: Track peak memory used by all child jobs ===
    peak_mem_str = estimate_peak_memory_children()
    build_email_summary(args, variant_settings, files, results, output_dir, log_dir, Peak_Mem=peak_mem_str)


if(__name__ == "__main__"):
    main()

