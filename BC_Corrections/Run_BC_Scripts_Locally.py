#!/usr/bin/env python3
import os
import argparse
import subprocess
import glob
import shlex
import sys
import time

# ====================================================================================================
# Your standard import pattern (no fallback)
# ====================================================================================================
script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

def parse_args():
    parser = argparse.ArgumentParser(description="Run a command on each file in a directory or glob pattern", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-d", "--directory",
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb*EvGen*",
                        type=str,
                        help="Directory path OR glob pattern of files to process.")

    parser.add_argument("-check", "--check",
                        action="store_true",
                        help="Stop if a command exits non-zero.")

    parser.add_argument("-c", "--command",
                        default="lt",
                        type=str,
                        help="Command to run. The default command is just 'lt'—must at least set to 'BC_Corrections_Script.py' to run the actual code.")

    parser.add_argument("-e", '--email',
                        action="store_true",
                        help="Passes an email argument to the last command.")

    parser.add_argument("-gdf", '--clasdis',
                        action="store_true",
                        help="Runs clasdis default files instead of EvGen files (overwrites the '--directory' argument automatically).")

    parser.add_argument("-p", "--parallel",
                        action="store_true",
                        help="Enable parallel execution mode (default is sequential).")

    parser.add_argument("-j", "--max_jobs",
                        default=4,
                        type=int,
                        help="Maximum number of simultaneous jobs when running in parallel mode.")

    parser.add_argument("-rcl", "--run_context_line",
                        default="Ran in tmuxPython",
                        type=str,
                        help="Custom line to include at the end of the Email_output string (replaces the hardcoded 'Ran in tmux...' line).")

    return parser.parse_args()


def main():

    args = parse_args()
    timer = RuntimeTimer()
    timer.start()

    target = args.directory if(not args.clasdis) else "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.*clasdis*"
    if(args.clasdis and ("BC_Corrections_Script.py" in str(args.command)) and not any(clas_com in str(args.command) for clas_com in ["-clasdis", "--use_clasdis"])):
        args.command = f"{args.command} --use_clasdis"
    if(("BC_Corrections_Script.py" in str(args.command)) and not any(file_com in str(args.command) for file_com in ["-f ", "--file "])):
        args.command = f"{args.command} --file "
        
    # Build file list from either directory or glob
    if(os.path.isdir(target)):
        files = [os.path.join(target, name) for name in os.listdir(target) if(os.path.isfile(os.path.join(target, name)))]
    else: # treat as glob
        files = [p for p in glob.glob(target) if(os.path.isfile(p))]

    if(not files):
        print(f"Error: no files found for '{target}'")
        return

    base_cmd = shlex.split(args.command)

    if(args.parallel):

        max_jobs = int(args.max_jobs)
        if(max_jobs < 1):
            max_jobs = 1

        # log_dir_base = "Parallel_Logs"
        # log_dir_run  = os.path.join(log_dir_base, f"Run_{os.getpid()}")
        log_dir_run = "/lustre24/expphy/volatile/clas12/richcap/BC_Log_and_Old_Files/"
        os.makedirs(log_dir_run, exist_ok=True)

        # In the original sequential logic, the final file is treated specially (and only run with --email).
        # To preserve that behavior, parallel mode runs all but the final file in parallel, then handles the final file as before.
        files_to_run = files[:-1]

        parallel_email_text = f"""
{color.BBLUE}Parallel mode enabled{color.END}
    Max Concurrent jobs    = {max_jobs}
    Log Output Directory   = {log_dir_run}
    Number of Files to Run = {len(files)}
"""
        print(parallel_email_text)
        args.run_context_line = f"{args.run_context_line}\n{parallel_email_text}"
        
        running = []  # list of dicts: {"proc":..., "fh":..., "log":..., "filepath":..., "num":...}
        num_started = 0
        num_done    = 0
        num_fail    = 0

        def start_job(job_num, filepath):
            command = base_cmd + [filepath]
            base    = os.path.basename(filepath).replace(" ", "_")
            log_p   = os.path.join(log_dir_run, f"job_{job_num:05d}_{base}.log")
            fh      = open(log_p, "w")
            fh.write(f"# {' '.join(shlex.quote(x) for x in command)}\n")
            fh.flush()
            proc    = subprocess.Popen(command, stdout=fh, stderr=fh)
            running.append({"proc": proc, "fh": fh, "log": log_p, "filepath": filepath, "num": job_num})
            print(f"{color.BCYAN}START{color.END}: {job_num+1:>3.0f} of {len(files)}  ->  {base}")
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
            else:
                num_fail += 1
                print(f"{color.Error}FAIL {color.END}: {item['num']+1:>3.0f} of {len(files)}  ->  {base} (rc={rc})")
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

        for num, filepath in enumerate(files_to_run):

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
                    return

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
                return

        if(len(files) > 0):
            filepath = files[-1]
            command  = base_cmd + [filepath]
            # print("Running:", " ".join(command))
            # print("\n\nLAST ONE\n\n")
            StartTimePrint = str(timer.start_find(return_Q=True)).replace("Ran", "Started running")
            ElaspTimePrint = "\n".join(timer.time_elapsed(return_Q=True))
            Email_output = f"""This was the last file to be run with the command: 
{args.command} "files"

{StartTimePrint}
{ElaspTimePrint}

{args.run_context_line}
"""
            if(args.email):
                cmd = (shlex.split(command) if isinstance(command, str) else list(command))
                cmd += ["-e", "-em", Email_output]
                subprocess.run(cmd, check=args.check)
            print(f"\n{color.BBLUE}{Email_output}{color.END}\n")

        print("\n\nCommands are Complete\n")

        timer.stop()
        return

    for num, filepath in enumerate(files):
        command = base_cmd + [filepath]
        # print("Running:", " ".join(command))
        if((num+1) == len(files)):
            # print("\n\nLAST ONE\n\n")
            StartTimePrint = str(timer.start_find(return_Q=True)).replace("Ran", "Started running")
            ElaspTimePrint = "\n".join(timer.time_elapsed(return_Q=True))
            Email_output = f"""This was the last file to be run with the command: 
{args.command} "files"

{StartTimePrint}
{ElaspTimePrint}

{args.run_context_line}
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
    