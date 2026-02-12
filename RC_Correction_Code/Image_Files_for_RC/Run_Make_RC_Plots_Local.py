#!/usr/bin/env python3

import argparse
import datetime
import subprocess
import sys

script_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis"
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir


def build_name_and_title(mmod):
    if(mmod == 2):
        return "Measured_Mods", "Injected Modulations from Unfolded Data"
    elif(mmod == 1):
        return "No_Mods", "No Modulations"
    else:
        return "EvGen", "Default Modulations from EvGen"


def send_mail(subject, body):
    to_addr = "richard.capobianco@uconn.edu"
    try:
        subprocess.run(["mail", "-s", subject, to_addr], input=body, text=True, check=True)
        print(f"Sent email to {to_addr}")
    except Exception as err:
        print(f"ERROR: failed to send email via 'mail': {err}")


def main():
    parser = argparse.ArgumentParser(description="Run Make_RC_Factor_Plots_with_Kinematic_Bins.py command grid and optionally email when done.")
    parser.add_argument("-e", "--email", dest="send_email", action="store_true", help="Send completion email")
    parser.add_argument("-em", "--email_message", type=str, default="", help="Add additional message to the completion email")
    parser.add_argument("-t", "-dr", "-test", "--dry-run", dest="dry_run", action="store_true", help="Print commands that would be run, but do not execute them.")
    args = parser.parse_args()
    
    timer = RuntimeTimer()
    timer.start()

    script_path = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/./Make_RC_Factor_Plots_with_Kinematic_Bins.py"

    fixed_args = [script_path, "-q", "-v", "pT", "-m", "z", "-u-z-pT"]

    mmods = [2, 0, 1]
    plots = ["sf_cos_sel", "sf_cos2_sel"]
    q2y_bins = range(1, 18)

    total_commands = 0
    failures = []

    for mmod in mmods:
        name_str, title_str = build_name_and_title(mmod)
        for plot in plots:
            for Q2_y_Bin in q2y_bins:
                cmd = []
                cmd.extend(fixed_args)
                cmd.extend(["-p", plot])
                cmd.extend(["-mm", str(mmod)])
                cmd.extend(["-n", name_str])
                cmd.extend(["-t", title_str])
                cmd.extend(["-q2y", str(Q2_y_Bin)])

                total_commands += 1
                print("Running:", " ".join([str(x) for x in cmd]))
                sys.stdout.flush()

                if(args.dry_run):
                    continue

                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as err:
                    failures.append({"returncode": err.returncode, "cmd": cmd})
                    print(f"ERROR: command failed (returncode={err.returncode})")
                    sys.stdout.flush()
                except FileNotFoundError as err:
                    failures.append({"returncode": 127, "cmd": cmd, "error": str(err)})
                    print(f"ERROR: executable not found: {err}")
                    sys.stdout.flush()
                timer.time_elapsed()

    StartTimePrint = str(timer.start_find(return_Q=True)).replace("Ran", "Started running")
    ElaspTimePrint = "\n".join(timer.time_elapsed(return_Q=True))
    ok_count = total_commands - len(failures)
    summary_lines = []
    summary_lines.append("")
    summary_lines.append(args.email_message)
    summary_lines.append("")
    summary_lines.append(StartTimePrint)
    summary_lines.append(ElaspTimePrint)
    summary_lines.append("")
    summary_lines.append(f"Total commands: {total_commands}")
    summary_lines.append(f"Succeeded:      {ok_count}")
    summary_lines.append(f"Failed:         {len(failures)}")

    if(len(failures) > 0):
        summary_lines.append("")
        summary_lines.append("Failures (up to first 50 shown):")
        for idx, item in enumerate(failures[:50]):
            cmd_str = " ".join([str(x) for x in item["cmd"]])
            rc = item.get("returncode", "unknown")
            summary_lines.append(f"{idx+1:02d}) returncode={rc} :: {cmd_str}")
            if("error" in item):
                summary_lines.append(f"    error={item['error']}")

    summary = "\n".join(summary_lines)
    print("\n" + summary)

    if(args.send_email):
        subject = f"RC-factor command sweep finished ({ok_count}/{total_commands} ok)"
        send_mail(subject, summary)

    if(len(failures) > 0):
        sys.exit(1)

    sys.exit(0)


if(__name__ == "__main__"):
    main()
