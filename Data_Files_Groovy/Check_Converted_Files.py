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
                  "gdf":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                  "gdf_1.5":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/clasdis_pass2/fa18_inb/Q2_1.5GeV/",
                         "new_dir":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/"},
                  "gdf_EvGen":
                        {"cache_dir": "/cache/clas12/rg-a/production/montecarlo/EvGen_DIS/pass2/fa18_inb/",
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
                        type=str,
                        default='rdf',
                        choices=["rdf", "mdf", "gdf", "mdf_1.5", "gdf_1.5", "mdf_EvGen", "gdf_EvGen"],
                        help=f"Choice of directories for checking files.\n{color.BOLD}See '--group_lists' for list of directories.{color.END}\n")
    parser.add_argument('-gl', '--group_lists',
                        action='store_true',
                        help="Check the contents of 'DEFAULT_GROUPS' instead of running to help select '--group'.\n")
    
    parser.add_argument('-cc', '--check_cache',
                        action='store_true',
                        help="Check to see if all the available files are on the cache/how many are missing.\n")
    
    parser.add_argument('-rs', '--run_Slurm',
                        action='store_true',
                        help="Sets the commands to return the SLURM submission outputs.\n")
    
    parser.add_argument('-t', '-test', '--dry_run',
                        action='store_true',
                        help='Run test commands.\n')

    parser.add_argument('-e', '--email',
                        action='store_true',
                        help='Send Email message when the script finishes running.\n')
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the default notification from '--email'.\n")
    
    parser.add_argument('-n', '-sn', '--save_name',
                        default="",
                        type=str,
                        help="Optional prefix added to the output filename.\n")

    return parser.parse_args()

def silence_root_import():
    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
    sys.path.append(script_dir)
    # Flush Python’s buffers so dup2 doesn’t duplicate partial output
    sys.stdout.flush()
    sys.stderr.flush()
    # Save original file descriptors
    old_stdout = os.dup(1)
    old_stderr = os.dup(2)
    try:
        # Redirect stdout and stderr to /dev/null at the OS level
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        os.close(devnull)
        # Perform the noisy import
        import RooUnfold
    finally:
        # Restore the original file descriptors
        os.dup2(old_stdout, 1)
        os.dup2(old_stderr, 2)
        os.close(old_stdout)
        os.close(old_stderr)
    sys.path.remove(script_dir)
    del script_dir

# import math
# import array
# import copy
import json
import time

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

def Update_Email(args, update_name="", update_message="", verbose_override=False):
    update_email = ""
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
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "group_lists"]):
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

def human_readable_size(size_bytes):
    # Convert bytes to human-readable format (KB, MB, GB, etc.)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if(size_bytes < 1024):
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"



def command_to_use_run_groovy_scripts_with_emails(file_paths, args, src_type="clasdis", mc_type="rec", evt_type="epipX", slurmCancel=None):
    slurm_time  = {"rec": "20:00:00",   "gen": "20:00:00"}
    slurm_cpu   = {"rec":    "3500M",   "gen":      "3GB"}
    commands = ""
    command = "cd_Groovy; ./run_groovy_scripts_with_emails.py"
    command = "./run_groovy_scripts_with_emails.py"
    tmux = -1
    for         src in ["clasdis", "evgen", "data"]:
        for      mc in ["rec", "gen"]:
            for evt in ["epipX", "eppipX", "epippimX"]:
                if((src in ["evgen"]) and (evt not in ["epipX"])):
                    continue
                if((src in ["data"])  and (mc  not in ["rec"])):
                    continue
                tmux += 1
                if((src_type != src) or (mc_type != mc) or (evt_type != evt)):
                    continue
                tmux_name = "tmuxSIDIS" if(tmux == 0) else f"tmuxSIDIS_{tmux}" if(tmux < 4) else "tmuxTTree" if(tmux == 4) else "tmuxPython" if(tmux == 5) else "tmuxRADGEN" if(tmux == 6) else "tmuxEvGen" if(tmux == 7) else "tmuxEIC" if(tmux == 8) else "tmuxLUND" if(tmux == 9) else "tmuxOSGL" if(tmux == 10) else "tmuxRADGEN" if(tmux == 11) else "ERROR"
                # array = f' -ub "2-{num_files[src]}"'
                array = f" -ptxt '{file_paths}'"
                if(args.dry_run):
                    array = f"{array} -test"
                email, message = "-em ", ""
                if(args.run_Slurm):
                    slurm = f' -m "slurm" -st "{slurm_time[mc]}" -cpu "{slurm_cpu[mc]}"'
                    arguments = f'-src "{src}" -mc "{mc}" -evt "{evt}"{array}{slurm}'
                    message = f"""Ran with the Command: '{arguments.replace('"', "'")}'."""
                else:
                    arguments = f'-src "{src}" -mc "{mc}" -evt "{evt}"{array}'
                    if(slurmCancel is not None):
                        arguments = f'{arguments} -saj {slurmCancel}'
                    email = f"-e {email}"
                    message = f"""Ran with the Command: '{arguments.replace('"', "'")}'. Ran in {tmux_name}."""
                email = f"""{email} "{message}{f' Extra Message: {args.email_message}.' if(args.email_message not in ['']) else ''}" """
                if(args.run_Slurm):
                    commands = f"{commands}{command}{email}{arguments}; SQueue_format; "
                else:
                    commands = f"{commands}{command} {arguments}{email}; Done_at\n\n"
    return f"{color.BGREEN}{commands}lt; Done_at{color.END}"


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

    args.new_dir   = DEFAULT_GROUPS[args.group]["new_dir"]
    args.cache_dir = DEFAULT_GROUPS[args.group]["cache_dir"]
    args.mss_files = str(args.cache_dir).replace("cache", "mss/")
    # Get sets of files in each directory (non-recursive, only top-level files)
    mss_files   = set(os.listdir(args.mss_files))
    cache_files = set(os.listdir(args.cache_dir))
    # Find files present in mss_dir but missing in cache_dir
    missing_in_cache = mss_files - cache_files

    if(args.check_cache):
        missing_message = "No files are missing in the cache directory."
        if(missing_in_cache):
            missing_message = f"Missing {len(missing_in_cache)} Files in the cache directory.\nThe Missing Files are:\n"
            for num, file in enumerate(sorted(missing_in_cache)):
                missing_message = f"{missing_message}\t{num+1:>4.0f}) {file}\n"
        Update_Email(args, update_message=missing_message, verbose_override=True)

    full_command_str = ""

    Construct_Email(args)


if(__name__ == "__main__"):
    main()
    
