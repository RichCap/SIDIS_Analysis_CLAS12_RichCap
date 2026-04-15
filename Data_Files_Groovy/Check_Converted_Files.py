#!/usr/bin/env python3
import sys
import argparse

import ROOT, numpy, re
import traceback
import os
from pathlib import Path
import glob

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
# from ExtraAnalysisCodeValues import *
sys.path.remove(script_dir)
del script_dir


# DEFAULT_cache_dir = '/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/'
DEFAULT_cache_dir = '/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/Q2_1.5GeV/'
# DEFAULT_cache_dir = '/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/'
# DEFAULT_cache_dir = '/cache/clas12/rg-a/production/montecarlo/EvGen_DIS/pass2/fa18_inb/'
# DEFAULT_mss_dir = DEFAULT_cache_dir.replace("cache", "mss/")

DEFAULT_GROUPS = {"rdf":
                        {"cache_dir": "/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/"},
                  "mdf":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/"},
                  "mdf_1.5":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/Q2_1.5GeV/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/"},
                  "mdf_EvGen":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/EvGen_DIS/pass2/fa18_inb/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/"},
                  "mdf_rho0":
                        {"cache_dir": "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/rho0_rga_fall2018/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/"},
                  "gdf":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                  "gdf_1.5":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/Q2_1.5GeV/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                  "gdf_EvGen":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/EvGen_DIS/pass2/fa18_inb/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                  "gdf_rho0":
                        {"cache_dir": "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/rho0_rga_fall2018/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                }

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Checks the number of HIPO Files that still need to be converted from HIPO to ROOT.", formatter_class=RawDefaultsHelpFormatter)
    
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Run with more print messages.\n')

    parser.add_argument('-g', '--group',
                        nargs='+',
                        default=['rdf'],
                        choices=["rdf", "mdf", "gdf", "mdf_1.5", "gdf_1.5", "mdf_EvGen", "gdf_EvGen", "mdf_rho0", "gdf_rho0"],
                        help=f"Choice of directories for checking files.\n{color.BOLD}See '--group_lists' for list of directories.{color.END}\n")
    parser.add_argument('-gl', '--group_lists',
                        action='store_true',
                        help="Check the contents of 'DEFAULT_GROUPS' instead of running to help select '--group'.\n")
    
    parser.add_argument('-cv', '--check_versions',
                        nargs='+',
                        default=['*qa'],
                        help="List of channel patterns to check. Examples: '*qa', '*wPim*', '*wProton*', or '*'.\n")

    parser.add_argument('-cc', '--check_cache',
                        action='store_true',
                        help="Check to see if all the available files are on the cache/how many are missing.\n")

    # New run mode support
    parser.add_argument('-rm', '--run_mode',
                        default='local',
                        choices=['local', 'slurm', 'parallel'],
                        help="Run mode: 'local' (default), 'slurm' (array jobs), or 'parallel' (concurrent local jobs).\n")
    parser.add_argument('-pj', '--parallel_jobs',
                        type=int,
                        default=4,
                        help="Number of concurrent jobs when '--run_mode parallel' is used.\n")

    parser.add_argument('-t', '--test',
                        action='store_true',
                        help="Run test commands (prevents code from running/writing other script to just test this script's commands — will also skip sending emails).\n")

    parser.add_argument('-dr', '--dry_run',
                        action='store_true',
                        help="Run test commands (only impacts the arguments given to the 'run_groovy_scripts_with_emails.py' script).\n")
    
    parser.add_argument('-np', '--no_prompt',
                        action='store_true',
                        help='Run with default settings instead of requesting user permissions/inputs before completing the commands.\n')

    parser.add_argument('-e', '--email',
                        action='store_true',
                        help='Send Email message when the script finishes running.\n')
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the default notification from '--email'.\n")
    parser.add_argument('-emj', '--email_message_jobs',
                        default="",
                        type=str,
                        help="Optional Email message is provided to the jobs submitted by this script.\nIs treated separately from the standard '--email_message' argument to avoid issues with this script's email constructor.\n")
    
    parser.add_argument('-n', '-fvm', '--file_version_main',
                        default=".new8.",
                        type=str,
                        help="File version name used to name the output ROOT files being checked/created.\n")

    parser.add_argument('-fc', '--fast_check',
                        action='store_true',
                        help="Use fast size check instead of rootls (faster, less accurate for corruption).\n")

    parser.add_argument('-scid', '--scancel_ids',
                        type=str,
                        default=None,
                        help="Comma-separated SLURM job IDs (e.g. '64692480,64692481') to replace hard-coded values.\n")

    parser.add_argument('-ntf', '--new_text_files',
                        action='store_true',
                        help="Runs the Save_Path_Files function to save new txt files to point the scripts to which files need to be processed.\n")


    parser.add_argument('-pld', '--parallel_log_dir',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/parallel_logs/",
                        help="Directory for per-job log files when '--mode' parallel is used.\n")

    return parser.parse_args()

def silence_root_import():
    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
    sys.path.append(script_dir)
    sys.stdout.flush()
    sys.stderr.flush()
    old_stdout = os.dup(1)
    old_stderr = os.dup(2)
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        os.close(devnull)
        import RooUnfold
    finally:
        os.dup2(old_stdout, 1)
        os.dup2(old_stderr, 2)
        os.close(old_stdout)
        os.close(old_stderr)
    sys.path.remove(script_dir)
    del script_dir

# import math
# import array
# import copy
# import json
# import time
import subprocess

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

def Update_Email(args, update_name="", update_message="", verbose_override=False, no_time=not False):
    update_email = ""
    if(no_time):
        if(update_name not in [""]):
            update_email = update_name
        if(update_message not in [""]):
            update_email = update_message if(update_email not in [""]) else f"{update_email}\n{update_message}"
    else:
        if(update_message not in [""]):
            update_email = f"""{update_message}
{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}"""
        elif(update_name not in [""]):
            update_email = f"""
{color.BCYAN}{update_name}{color.END_B} is done running...{color.END}
{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}

"""
    if(update_email not in [""]):
        args.email_message = f"{args.email_message}\n{update_email}"
        if(args.verbose or verbose_override):
            print(update_email)

def Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Files"):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    Script_Name = "Check_Converted_Files.py"
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list, dir_lists = "", ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "group_lists"]):
            continue
        if((str(name) in ["parallel_log_dir", "parallel_jobs"]) and (args.run_mode not in "parallel")):
            continue
        if((str(name) in ["new_dir",  "cache_dir",  "mss_dir"]) and (len(args.group) > 1)):
            if(dir_lists == ""):
                dir_lists = "Directories Per Group:"
                for single_group in args.group:
                    dir_lists = f"""{dir_lists}
    Group '{single_group}':
        new_dir: {args.new_dir[single_group]}
        cache_dir: {args.cache_dir[single_group]}
        mss_dir: {args.mss_dir[single_group]}"""
            dir_lists = f"{dir_lists}\n\n"
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The '{Script_Name}' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

{args.email_message}

{dir_lists}
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

def human_readable_size(size_bytes):
    # Convert bytes to human-readable format (KB, MB, GB, etc.)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if(size_bytes < 1024):
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def tmux_has_session(session_name):
    result = subprocess.run(["tmux", "has-session", "-t", session_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def prompt_tmux_session(default_name="hadd_sidis", test_mode=False):
    while(True):
        session = input(f"\nEnter tmux session name to use [default: {default_name}]: ").strip() or default_name
        if(tmux_has_session(session)):
            print(f"{color.BGREEN}Using existing session: {session}{color.END}")
            return session, False
        create = input(f"Session '{session}' does not exist. Create it? (y/N): ").strip().lower()
        if(create in ['y', 'yes']):
            if(not test_mode):
                subprocess.run(["tmux", "new-session", "-d", "-s", session], check=False)
                print(f"{color.BCYAN}Created new tmux session: {session}{color.END}")
            else:
                print(f"{color.BCYAN}WOULD have created new tmux session: {session}\n{color.END}The session was not made since you are running in 'test' mode.\n")
            return session, not test_mode
        print("Please choose a different name or type 'y' to create.")

def tmux_send(session_name, command_str):
    # Send a single command to a tmux session and press Enter. 
    result = subprocess.run(["tmux", "send-keys", "-t", session_name, command_str, "C-m"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if(result.returncode != 0):
        print(f"{color.Error}Warning: Failed to send command to tmux session '{session_name}': {result.stderr.strip()}{color.END}")
    return result.returncode == 0

def is_incomplete_root_file(filename, args):
    # Fast check for truncated / crashed-while-writing ROOT files.
    # Returns True if the file is incomplete/corrupted from a crash.
    # Does NOT load any trees or call GetEntries().
    try:
        # "READ" mode only reads the file header + footer (very fast)
        root_file = ROOT.TFile.Open(filename, "READ")
        if((not root_file) or root_file.IsZombie()):
            return args, True                     # classic incomplete file
        if(root_file.TestBit(ROOT.TFile.kRecovered)):
            return args, True                     # ROOT tried to recover a truncated file
        tree_now = root_file.Get("h22")
        if((tree_now is None) or (not tree_now.InheritsFrom("TTree"))):
            root_file.Close()
            return args, True
        if(getattr(args, "event_count_full", False) or args.verbose):
            entries_now = int(tree_now.GetEntriesFast())
            if(entries_now == 0):
                Update_Email(args, update_message=f"\n{color.Error}Empty ROOT File Warning for: {color.END_R}{filename}{color.END}", verbose_override=True)
            elif(args.verbose):
                print(f"\tNumber of events added in current ROOT file: {color.BOLD}{entries_now}{color.END}")
            if(getattr(args, "event_count_full", False)):
                args.current_event_count_total = entries_now if(getattr(args, "current_event_count_total", None) is None) else (args.current_event_count_total + entries_now)
        root_file.Close()
        return args, False
    except Exception:
        return args, True   # any PyROOT error = treat as bad

def command_to_use_run_groovy_scripts_with_emails(file_paths, args, src_type="clasdis", mc_type="rec", evt_type="epipX", slurmCancel=None, tmux_name=""):
    commands = ""
    command = "cd_Groovy; ./run_groovy_scripts_with_emails.py"
    array = f" -ptxt '{file_paths}'"
    if(args.dry_run):
        array += " -dr"
    if(args.run_mode == "slurm"):
        slurm_time = "20:00:00"
        slurm_cpu  = "3500M" if mc_type == "rec" else "3GB"
        slurm = f' -m slurm -st "{slurm_time}" -cpu "{slurm_cpu}"'
        arguments = f'-src "{src_type}" -mc "{mc_type}" -evt "{evt_type}"{array}{slurm}'
        email = f' -em "Ran with the Command: \'{arguments.replace(chr(34), chr(39))}\'.{f" Extra Message: {args.email_message_jobs}." if(args.email_message_jobs) else ""}" '
        commands = f"{command}{email}{arguments}; SQueue_format; "
    elif(args.run_mode == "parallel"):
        parallel = f' -m parallel -pj {args.parallel_jobs} --parallel_log_dir "{args.parallel_log_dir}"'
        arguments = f'-src "{src_type}" -mc "{mc_type}" -evt "{evt_type}"{array}{parallel}'
        if(slurmCancel):
            arguments += f" -saj {slurmCancel}"
        email = f' -e -em "Ran with the Command: \'{arguments.replace(chr(34), chr(39))}\' (parallel mode).{f" Extra Message: {args.email_message_jobs}." if(args.email_message_jobs) else ""}" '
        commands = f"{command} {arguments}{email}; Done_at\n\n"
    else:  # local / sequential
        arguments = f'-src "{src_type}" -mc "{mc_type}" -evt "{evt_type}"{array}'
        if(slurmCancel):
            arguments += f" -saj {slurmCancel}"
        email = f' -e -em "Ran with the Command: \'{arguments.replace(chr(34), chr(39))}\'.{f" Ran in {tmux_name}." if tmux_name else ""}{f" Extra Message: {args.email_message_jobs}." if(args.email_message_jobs) else ""}" '
        commands = f"{command} {arguments}{email}; Done_at\n\n"

    return f"{color.BGREEN}{commands}lt; Done_at{color.END}"

def Check_Files_To_Run_Missing_Only(args):
    args.new_dir   = {} if(not hasattr(args, "new_dir"))   else args.new_dir
    args.cache_dir = {} if(not hasattr(args, "cache_dir")) else args.cache_dir
    args.mss_dir   = {} if(not hasattr(args, "mss_dir"))   else args.mss_dir
    mss_files, cache_files, missing_in_cache = {}, {}, {}
    for single_group in args.group:
        args.new_dir[single_group]     = DEFAULT_GROUPS[single_group]["new_dir"]
        args.cache_dir[single_group]   = DEFAULT_GROUPS[single_group]["cache_dir"]
        args.mss_dir[single_group]     = str(args.cache_dir[single_group]).replace("cache", "mss/")
        mss_files[single_group]        = set(os.listdir(args.mss_dir[single_group]))
        cache_files[single_group]      = set(os.listdir(args.cache_dir[single_group]))
        missing_in_cache[single_group] = mss_files[single_group] - cache_files[single_group]
        if(args.check_cache):
            missing_message = f"\n{color.BOLD}No files are missing in the cache directory for group '{single_group}'.{color.END}\n"
            if(missing_in_cache[single_group]):
                missing_message = f"Missing {len(missing_in_cache[single_group])} Files in the cache directory for group '{single_group}'.\nThe Missing Files are:\n"
                for num, file in enumerate(sorted(missing_in_cache)):
                    missing_message = f"{missing_message}\t{num+1:>4.0f}) {file}\n"
            Update_Email(args, update_message=missing_message, verbose_override=True)
    return args, mss_files, cache_files, missing_in_cache

def Check_For_Proccessed_Files(args, cache_files):
    full_list_to_rerun, full_need_rerun_count = [], 0
    group_map = {
        "rdf":       ("data",    "rec"),
        "mdf":       ("clasdis", "rec"),
        "mdf_1.5":   ("clasdis", "rec"),
        "mdf_EvGen": ("evgen",   "rec"),
        "mdf_rho0":  ("rho0",    "rec"),
        "gdf":       ("clasdis", "gen"),
        "gdf_1.5":   ("clasdis", "gen"),
        "gdf_EvGen": ("evgen",   "gen"),
        "gdf_rho0":  ("rho0",    "gen")
    }

    per_group_results = {}   # will hold data per group

    for single_group in args.group:
        source, Type = group_map.get(single_group, ("Error", "Error"))
        if("Error" in [source, Type]):
            Crash_Report(args, crash_message=f"\n{color.Error}Error in 'group_map':{color.END_B} {single_group} was not defined in the map...{color.END}", continue_run=False)

        print(f"""{color.BBLUE}
================================================================================================================================================
Source\t     = {source}{color.END}""")

        if(args.file_version_main in ["", None]):
            args.file_version_main = ".new7." if("GEN_MC" not in args.new_dir[single_group]) else ".new6." 

        text_of_path_file = """# Full (Normal) Path:
# /lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*""" if(source == "data") else """# Full (Normal) Path:
# /cache/clas12/rg-a/production/montecarlo/EvGen_DIS/pass2/fa18_inb/inb-EvGen-LUND_EvGen_richcap_GEMC-*""" if(source == "evgen") else """# Full (Normal) Path:
# /cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/clasdis_rga_fa18_inb_*
# /cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/Q2_1.5GeV/nb-clasdis-Q2_1.5-9*""" if(source != "rho0") else """# Full (Normal) Path:
# /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/rho0_rga_fall2018/lundrho*"""

        for version_num, check_version in enumerate(args.check_versions):
            print(f"\n\t\t{color.BYELLOW}Running with check_version = {check_version}{color.END}\n")

            cache_dir = args.cache_dir[single_group]
            new_dir   = args.new_dir[single_group]

            Update_Email(args, update_message=f"\t\t\t{color.PINK}For cache_dir = {color.BLUE}{cache_dir}{color.END}", verbose_override=True, no_time=True)

            list_to_rerun, may_need_to_rerun, may_need_rerun_count, need_rerun_count = [], [], 0, 0

            for num, file in enumerate(sorted(cache_files[single_group])):
                if(file in ["Q2_1.5GeV", "GEMC_5.12_Q2_1.5GeV_potential_bad_neutral_pid", "GEMC_5.12_potential_bad_neutral_pid"]):
                    continue
                # Derive file_num from the cache file name
                if("nSidis_00" not in file):
                    parts = file.split("-")
                    if(len(parts) < 2):
                        print(f"{color.Error}{num+1:>4.0f}) - {file}: Could not parse file_num (missing '-'){color.END}")
                        continue
                else:
                    parts = file.split("nSidis_00")
                    if(len(parts) < 2):
                        print(f"{color.Error}{num+1:>4.0f}) - {file}: Could not parse file_num (missing 'nSidis_00'){color.END}")
                        continue
                last_part = parts[-1]
                file_num_parts = last_part.split(".hipo")
                if(len(file_num_parts) < 2):
                    print(f"{color.Error}{num+1:>4.0f}) - {file}: Could not parse file_num (missing '.hipo'){color.END}")
                    continue
                file_num = file_num_parts[0]

                pattern = f"{new_dir}{check_version}{args.file_version_main}*{file_num}*.root" if("clasdis_pass2" not in cache_dir) else f"{new_dir}{check_version}{args.file_version_main}*clasdis*{file_num}*.root"
                processed_files = glob.glob(pattern)

                if(processed_files):
                    for proc_file in sorted(processed_files):
                        try:
                            if(args.fast_check):
                                size_bytes = os.path.getsize(proc_file)
                                size_str = human_readable_size(size_bytes)
                                if(all(unit not in size_str for unit in ["9.01 KB", "MB", "GB"])):
                                    may_need_rerun_count += 1
                                    full_need_rerun_count += 1
                                    list_to_rerun.append(f"{cache_dir}{file}")
                                    full_list_to_rerun.append(f"{cache_dir}{file}")
                                    may_need_to_rerun.append(os.path.basename(proc_file))
                                    if(args.verbose):
                                        Update_Email(args, update_message=f"({num+1:>4.0f})\t  → {os.path.basename(proc_file)}  |  Size: {size_str}", no_time=True)
                            else:
                                args, root_check = is_incomplete_root_file(proc_file, args)
                                if(root_check):
                                    may_need_rerun_count += 1
                                    full_need_rerun_count += 1
                                    list_to_rerun.append(f"{cache_dir}{file}")
                                    full_list_to_rerun.append(f"{cache_dir}{file}")
                                    may_need_to_rerun.append(os.path.basename(proc_file))
                                    if(args.verbose):
                                        size_str = human_readable_size(os.path.getsize(proc_file))
                                        Update_Email(args, update_message=f"({num+1:>4.0f})\t  → {os.path.basename(proc_file)}  |  Size: {size_str}", no_time=True)
                                elif(args.verbose and ((num+1)%100 == 0)):
                                    print(f"\tChecked up to file {num+1}...")
                        except Exception as e:
                            Update_Email(args, update_message=f"\t  → {os.path.basename(proc_file)}  |  Error: {e}", verbose_override=True, no_time=True)
                else:
                    if(args.verbose):
                        Update_Email(args, update_message=f"{num+1:>4.0f}) - {file}: No processed version found", verbose_override=True, no_time=True)
                    list_to_rerun.append(f"{cache_dir}{file}")
                    need_rerun_count += 1
                    full_need_rerun_count += 1

            # Store per-group results
            per_group_results[f"{single_group}_{check_version}"] = {
                "list_to_rerun": list_to_rerun,
                "text_of_path_file": f'{text_of_path_file}\n{"\n".join(list_to_rerun)}\n\n',
                "check_version": check_version,
                "source": source,
                "Type": Type,
                "new_dir": new_dir,
                "cache_dir": cache_dir
            }

            tot_rerun = may_need_rerun_count + need_rerun_count
            rerun_str_output = f"""
\t\t\t\t{color.RED}(May) Need Rerun Count  = {may_need_rerun_count}{color.END}
\t\t\t\t{color.RED}Will Need to Run Count  = {need_rerun_count}{color.END}
\t\t\t\t{color.RED}Total to Run (Group)    = {tot_rerun}{color.END}
\t\t\t\t{color.BOLD}Total Avaliable (Group) = {len(cache_files[single_group])}{color.END}
\t\t\t\t{color.RED}Total to Run (Full)     = {color.UNDERLINE}{full_need_rerun_count}{color.END}

"""
            Update_Email(args, update_message=rerun_str_output, verbose_override=True)

    return args, full_list_to_rerun, full_need_rerun_count, per_group_results

def Save_Path_Files(args, per_group_results):
    save_count = 0
    args.files_Saved = []
    Path_to_where_files_will_be_saved = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/"

    for key, data in per_group_results.items():
        text_of_path_file = data["text_of_path_file"]
        check_version     = data["check_version"]
        Path_file = "Paths_to_REAL_Data_files_all.txt" if("nSidis" in data["cache_dir"]) else "Paths_to_MC_EvGen_files_all.txt" if("EvGen" in data["cache_dir"]) else "Paths_to_MC_rho0_files_all.txt" if("rho0" in data["cache_dir"]) else "Paths_to_MC_clasdis_files_all.txt"
        if(check_version != "*"):
            if("GEN_MC" in data["new_dir"]):
                Path_file = f"GEN_{Path_file}"
            if("Q2_1.5GeV" in data["cache_dir"]):
                Path_file = f"Q2_Cut_{Path_file}"
            if(check_version not in ["*", "*qa"]):
                Path_file = str(f"TEMP_{Path_file}".replace("all.txt", f"{check_version}.txt")).replace("*", "")
            else:
                Path_file = str(f"TEMP_{Path_file}".replace("all.txt",  "SIDIS.txt"))
                # Path_file = str(Path_file.replace("all.txt",  "SIDIS.txt"))

        ptxt_file = f'{Path_to_where_files_will_be_saved}{Path_file}'
        path_list = text_of_path_file

        print(f"\n\t{color.BCYAN}Saving: {color.BGREEN}{ptxt_file}{color.END}" if(not args.test) else f"\n\t{color.BLUE}WOULD have Saved: {color.END_B}{ptxt_file}{color.END}")
        if(ptxt_file not in args.files_Saved):
            args.files_Saved.append(ptxt_file)
        else:
            Update_Email(args, update_message=f"\n{color.ERROR}ERROR: File{color.END_B} '{ptxt_file}' {color.ERROR}was already saved{color.END}!\n", verbose_override=True)
        if(args.test):
            save_count += 1
            continue
        try:
            with open(ptxt_file, "w", encoding="utf-8") as out_file:
                out_file.write(path_list)
            save_count += 1
            print(f"\t{color.BCYAN}Saved!{color.END}")
        except Exception:
            Crash_Report(args, crash_message=f"{color.ERROR}Error in Saving{color.END}{color.Error} '{ptxt_file}':\n{color.END_R}{str(traceback.format_exc())}{color.END}", continue_run=False)
    if(args.test):
        Update_Email(args, update_message=f"\n{color.BCYAN}Would have saved a total of {color.END_B}{save_count}{color.BCYAN} files...\n{color.END}", verbose_override=True)
    else:
        Update_Email(args, update_message=f"\n{color.BCYAN}Done Saving... {color.END}(Total Saved = {save_count})\n", verbose_override=True)
    return args

def prompt_for_scancel_id(group_key, tmux_name):
    # Per-command scancel prompt — tailored to this exact group + tmux screen.
    print(f"\n{color.BBLUE}Command for group: {group_key} → tmux session: {tmux_name}{color.END}")
    user_input = input(f"{color.BOLD}Enter scancel job ID for this command (or press Enter to skip): {color.END}").strip()
    return user_input if(user_input) else None

def Create_Run_Commands(args, per_group_results, full_command_str, tmux_running):
    full_command_str = "" if(full_command_str is None) else full_command_str

    # === NEW: Collect all commands first (no dispatch yet) ===
    dispatch_plan = []   # list of (group_key, tmux_session, command_str, text_of_path_file)

    for single_group_and_check_version, data in per_group_results.items():
        list_to_rerun      = data["list_to_rerun"]
        text_of_path_file  = data["text_of_path_file"]
        check_version      = data["check_version"]
        source             = data["source"]
        Type               = data["Type"]
        new_dir            = data["new_dir"]
        cache_dir          = data["cache_dir"]

        if(len(list_to_rerun) == 0):
            Update_Email(args, update_message=f"\n{color.Error}No files to rerun for {single_group_and_check_version}{color.END}", verbose_override=True, no_time=False)
            continue

        # === Path file name logic (unchanged) ===
        Path_file = "Paths_to_REAL_Data_files_all.txt" if("nSidis" in cache_dir) else "Paths_to_MC_EvGen_files_all.txt" if("EvGen" in cache_dir) else "Paths_to_MC_rho0_files_all.txt" if("rho0" in cache_dir) else "Paths_to_MC_clasdis_files_all.txt"

        if(check_version != "*"):
            if("GEN_MC" in new_dir):
                Path_file = f"GEN_{Path_file}"
            if("Q2_1.5GeV" in cache_dir):
                Path_file = f"Q2_Cut_{Path_file}"
            if(check_version not in ["*", "*qa"]):
                Path_file = str(f"TEMP_{Path_file}".replace("all.txt", f"{check_version}.txt")).replace("*", "")
            else:
                Path_file = str(f"TEMP_{Path_file}".replace("all.txt", "SIDIS.txt"))

        event_type = "epipX" if(check_version == "*qa") else "eppipX" if(check_version == "*wProton*") else "epippimX"

        # if((check_version not in ["*"]) and ("# Rerunning for" not in text_of_path_file)):
        #     text_of_path_file = f"{text_of_path_file}\n# Rerunning for {event_type} events only\n"
        # for ii in list_to_rerun:
        #     text_of_path_file = f"{text_of_path_file}{ii}\n"

        # === SLURM / tmux handling (Combination_List) ===
        Combination_List = {
            "0" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "hadd_sidis",      "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "1" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "hadd_sidis1",     "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "2" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "hadd_sidis2",     "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "3" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "hadd_sidis3",     "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "4" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "EIC_Environment", "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "5" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "EvGen",           "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "6" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "run_EvGen_lund",  "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "7" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "Local_OSG_run",   "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "8" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "Run_python",      "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "9" : {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "RADGEN",          "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "10": {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "hadd_TTree",      "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "11": {"scancel": None, "source": None, "type": None, "channel": None, "tmux": "Unfolding",       "command": "",   "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": False, "AllowUse": True},
            "12": {"scancel": None, "source": None, "type": None, "channel": None, "tmux": None,              "command": None, "NumReRun": None, "ptxt_file": None, "path_list": None, "EndofList": True,  "AllowUse": True}
        }

        # Populate any CLI-provided scancel_ids (legacy support)
        if(args.scancel_ids):
            ids = [x.strip() for x in args.scancel_ids.split(",")]
            idx = 0
            for k in sorted(Combination_List.keys()):
                if((not Combination_List[k]["EndofList"]) and (Combination_List[k]["AllowUse"])):
                    if(idx < len(ids)):
                        Combination_List[k]["scancel"] = ids[idx]
                        idx += 1

        while(not Combination_List[f"{tmux_running}"]["AllowUse"]):
            tmux_running += 1
            if(Combination_List[f"{tmux_running}"]["EndofList"]):
                print(f"{color.ERROR}ERROR: END OF LIST{color.END}")
                tmux_running = 0
        this_tmux_name  = Combination_List[f"{tmux_running}"]["tmux"]
        slurmCancel_num = Combination_List[f"{tmux_running}"]["scancel"]

        # === Per-command interactive tmux session selection ===
        if(not args.no_prompt):
            print(f"\n{color.BBLUE}Command for group: {single_group_and_check_version}{color.END}")
            this_tmux_name, was_created = prompt_tmux_session(default_name=this_tmux_name, test_mode=args.test)
            print(f"{color.BBLUE}Base tmux session chosen: {this_tmux_name}{color.END}")
        else:
            # tmux_name = "hadd_sidis"
            was_created = False

        # === Per-command interactive scancel prompt ===
        if((not args.no_prompt) and (not args.scancel_ids)):
            print("")
            scancel_for_this = prompt_for_scancel_id(single_group_and_check_version, this_tmux_name)
            if(scancel_for_this):
                slurmCancel_num = scancel_for_this   # override for this command only

        command_str = command_to_use_run_groovy_scripts_with_emails(Path_file, args, src_type=source.lower(), mc_type=Type, evt_type=event_type, slurmCancel=slurmCancel_num, tmux_name=this_tmux_name)
        full_command_str += f"{command_str}; "
        full_command_str = full_command_str.replace("Done_atlt; Done_at", "Done_at; lt")

        # Store for final display
        dispatch_plan.append((single_group_and_check_version, this_tmux_name, command_str, text_of_path_file))

        tmux_running += 1
        if((len(args.check_versions) == 1) and (not args.new_text_files)):
            print(f"\n\n\t{color.BCYAN}Suggested path file content for {single_group_and_check_version}:{color.END}\n")
            print(f"{text_of_path_file}\n")

    # === Final full command summary (first listing) ===
    print(f"\n\n\n{color.BOLD}=== FULL COMMAND PLAN FOR 'run_groovy_scripts_with_emails.py' ==={color.END}")
    for group, tmux_sess, cmd, _ in dispatch_plan:
        print(f"{color.BBLUE}Group: {group} → tmux: {tmux_sess}{color.END}")
        print(f"   {cmd}\n")

    print(f"{color.BOLD}echo 'Done'{color.END}\n")

    if(args.test):
        Update_Email(args, update_message=f"{color.BGREEN}Done with dry run commands.{color.END}", verbose_override=True, no_time=False)
        return full_command_str, tmux_running

    # === Final user approval (second listing + cancel opportunity) ===
    if(not args.no_prompt):
        print(f"{color.BOLD}=== FINAL REVIEW BEFORE DISPATCH ==={color.END}")
        for group, tmux_sess, cmd, _ in dispatch_plan:
            print(f"{color.BBLUE}{group} → {tmux_sess}{color.END}")
            print(f"   {cmd}")
        approve = input(f"\n{color.BOLD}Dispatch ALL these commands to their respective tmux sessions now? (y/N): {color.END}").strip().lower()
        if(approve not in ['y', 'yes']):
            # Update_Email(args, update_message=f"{color.BYELLOW}Dispatch cancelled by user.{color.END}", verbose_override=True, no_time=not False)
            Crash_Report(args, crash_message=f"{color.Error}Dispatch cancelled by user.{color.END}", continue_run=False)
            return full_command_str, tmux_running

    # === Direct tmux dispatch ===
    print(f"{color.BCYAN}Dispatching to respective tmux sessions...{color.END}")
    for _, tmux_name, cmd, _ in dispatch_plan:
        cmd = ansi_to_plain(cmd)
        for line in cmd.splitlines():
            line = line.strip()
            if(not (line and line.startswith("#"))):
                for subcmd in line.split(';'):
                    subcmd = subcmd.strip()
                    if(subcmd):
                        tmux_send(tmux_name, subcmd)

    Update_Email(args, update_message=f"{color.BGREEN}All commands successfully dispatched to their tmux sessions.{color.END}", verbose_override=True, no_time=not False)
    return full_command_str, tmux_running

def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()

    silence_root_import()

    if(args.group_lists):
        print(f"\n{color.BGREEN}Contents of 'DEFAULT_GROUPS':{color.END}\n\t('new_dir' is where the converted ROOT files will go)\n")
        for ii in DEFAULT_GROUPS:
            print(f"\t{color.BBLUE}For Group {color.UNDERLINE}{ii}{color.END}{color.BBLUE}:{color.END}")
            for jj in DEFAULT_GROUPS[ii]:
                print(f"\t\t{color.BOLD}{jj:<10s} -> {color.END}{DEFAULT_GROUPS[ii][jj]}")
        print("\n\nDONE\n")
        args.timer.stop()
        sys.exit(0)
    
    if(args.test):
        args.email = False # Never send emails during a test run
        print(f"""{color.Error}{color_bg.YELLOW}
    \t                                   \t
    \t         Running as a TEST         \t
    \t                                   \t   {color.END}

    """)
    args, _, cache_files, _ = Check_Files_To_Run_Missing_Only(args)
    full_command_str = ""
    tmux_running = 0
    args, full_list_to_rerun, full_need_rerun_count, per_group_results = Check_For_Proccessed_Files(args, cache_files)
    if(args.new_text_files):
        args = Save_Path_Files(args, per_group_results)
    else:
        full_command_str, tmux_running = Create_Run_Commands(args, per_group_results, full_command_str, tmux_running)
    Construct_Email(args, final_count=full_need_rerun_count, Count_Type="Files to rerun")

if(__name__ == "__main__"):
    main()
    