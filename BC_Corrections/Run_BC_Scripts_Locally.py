#!/usr/bin/env python3
import os
import argparse
import subprocess
import glob
import shlex
import sys

# ====================================================================================================
# Your standard import pattern (no fallback)
# ====================================================================================================
script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir


def main():
    parser = argparse.ArgumentParser(description="Run a command on each file in a directory or glob pattern", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-d", "--directory",
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb*EvGen*",
                        type=str,
                        help="Directory path OR glob pattern of files to process")

    parser.add_argument("-check", "--check",
                        action="store_true",
                        help="Stop if a command exits non-zero")

    parser.add_argument("-c", "--command",
                        default="lt",
                        type=str,
                        help="Command to run.")

    parser.add_argument("-e", '--email',
                        action="store_true",
                        help="Passes an email argument to the last command.")

    args = parser.parse_args()

    timer = RuntimeTimer()
    timer.start()

    target = args.directory
    command_template = args.command

    # Build file list from either directory or glob
    if(os.path.isdir(target)):
        files = [os.path.join(target, name) for name in os.listdir(target) if(os.path.isfile(os.path.join(target, name)))]
    else: # treat as glob
        files = [p for p in glob.glob(target) if(os.path.isfile(p))]

    if(not files):
        print(f"Error: no files found for '{target}'")
        return

    base_cmd = shlex.split(command_template)

    for num, filepath in enumerate(files):
        command = base_cmd + [filepath]
        # print("Running:", " ".join(command))
        if((num+1) == len(files)):
            # print("\n\nLAST ONE\n\n")
            StartTimePrint = str(timer.start_find(return_Q=True)).replace("Ran", "Started running")
            ElaspTimePrint = "\n".join(timer.time_elapsed(return_Q=True))
            Email_output = f"""This was the last file to be run with the command: 
{args.command} "files..."


{StartTimePrint}
{ElaspTimePrint}

Ran in tmuxPython
"""
            if(args.email):
                cmd = (shlex.split(command) if isinstance(command, str) else list(command))
                cmd += ["-e", "-em", Email_output]
                subprocess.run(cmd, check=args.check)
            print(f"\n{color.BBLUE}{Email_output}{color.END}\n")
        else:
            subprocess.run(command, check=args.check)
            print(f"""\n\n{color.BGREEN}{color_bg.YELLOW}
\t                   \t   
\tRan {color.END_B}{color.UNDERLINE}{color_bg.YELLOW}{num:>3.0f}{color.END}{color_bg.YELLOW}{color.BGREEN} of {color.END_B}{color.UNDERLINE}{color_bg.YELLOW}{len(files)}{color.END}{color_bg.YELLOW}{color.BGREEN} Files.\t   
\t                   \t   
{color.END}""")
            timer.time_elapsed()

    print("\n\nCommands are Complete\n")

    timer.stop()

if(__name__ == "__main__"):
    main()
