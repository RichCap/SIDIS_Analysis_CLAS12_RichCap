#!/usr/bin/env python3

import argparse
import glob
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
sys.path.remove(script_dir)
del script_dir


def now_str():
    # Similar readability to `date` default output
    return datetime.now().ctime()


def build_default_patterns():
    return [
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9767*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9772*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9777*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9778*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9788*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9793*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9809*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9776*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9779*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9789*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9795*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9884*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9930*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9972*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9885*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9886*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9964*",
        "/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9973*",
    ]


def expand_patterns(patterns, preserve_unmatched=True):
    # Mimic bash globbing order reasonably:
    # - process patterns in user-provided order
    # - sort matches lexicographically (bash typically does)
    files = []
    for pattern in patterns:
        matches = sorted(glob.glob(pattern))
        if(len(matches) > 0):
            files.extend(matches)
        else:
            if(preserve_unmatched):
                files.append(pattern)
    return files


def send_mail_via_cli(mail_cmd, email_to, subject, message, dry_run=False):
    if(dry_run):
        print("\n--- DRY RUN: email would be sent ---")
        print(f"To: {email_to}")
        print(f"Subject: {subject}")
        print(message)
        print("--- END DRY RUN ---\n")
        return 0

    mail_path = shutil.which(mail_cmd)
    if(mail_path is None):
        print(f"ERROR: '{mail_cmd}' not found in PATH. Cannot send email.", file=sys.stderr)
        return 1

    try:
        proc = subprocess.Popen([mail_cmd, "-s", subject, email_to], stdin=subprocess.PIPE, text=True)
        proc.communicate(message)
        return proc.returncode
    except Exception as exc:
        print(f"ERROR: failed to send email via '{mail_cmd}': {exc}", file=sys.stderr)
        return 1


def main():
    default_script_path = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy"

    parser = argparse.ArgumentParser(description="Run a Groovy conversion script over many input files and send a completion email.")

    parser.add_argument("-id", "-jID", "--job-id", dest="job_id", default="MC_Gen_epip_clasdis_12_9_2025",
                        help="Job identifier used in the email subject/body.")
    parser.add_argument("-s", "-path", "-sp", "--script-path", dest="script_path", default=default_script_path,
                        help="Path to the Groovy script to run.")
    parser.add_argument("-e", "--email", dest="email", default="richard.capobianco@uconn.edu",
                        help="Completion email recipient.")
    parser.add_argument("--pattern", dest="patterns", action="append", default=None,
                        help="Add an input glob pattern. If not provided, built-in defaults are used. Can be repeated.")
    parser.add_argument("--file", dest="files", action="append", default=None,
                        help="Add an explicit input file (bypasses globbing for that entry). Can be repeated.")
    parser.add_argument("-t", "-test", "-dr", "--dry-run", dest="dry_run", action="store_true",
                        help="Do not execute run-groovy or send email; just print what would happen.")

    args = parser.parse_args()

    start_time = f"Started Running at: {now_str()}"

    if(args.patterns is None):
        patterns = build_default_patterns()
    else:
        patterns = args.patterns

    expanded_files = expand_patterns(patterns, preserve_unmatched=True)

    if(args.files is not None):
        expanded_files.extend(args.files)

    processed_lines = []
    results         = []  # list of dicts with file, rc, done

    # Run the Groovy script on each file
    for file_path in expanded_files:
        print(f"Processing file: {file_path}")
        print(f"(Done at: {now_str()})")

        cmd = ["run-groovy", args.script_path, file_path]

        if(args.dry_run):
            rc = 0
        else:
            try:
                completed = subprocess.run(cmd, check=False)
                rc        = completed.returncode
            except Exception as exc:
                rc = 999
                print(f"ERROR: failed to run command: {cmd}\nReason: {exc}", file=sys.stderr)

        done_stamp = now_str()
        processed_lines.append(f"{file_path} (Done at: {done_stamp}) [rc={rc}]")
        results.append({"file": file_path, "rc": rc, "done": done_stamp})

    host_name = socket.gethostname()
    end_time  = now_str()

    # Summarize failures (does not change execution behavior; only reporting)
    failed = [r for r in results if(r["rc"] != 0)]
    if(len(failed) > 0):
        failure_block = "\nFailures (nonzero return codes):\n" + "\n".join([f'  {r["file"]} [rc={r["rc"]}]' for r in failed]) + "\n"
    else:
        failure_block = "\nFailures (nonzero return codes):\n  None\n"

    subject = f"Local Job Finished: {args.job_id}"

    message = (
        f"The local job ({args.job_id}) processing MC (clasdis) SIDIS files has completed on {host_name} at:\n"
        f"{end_time}\n\n"
        f"Ran with: {args.script_path}\n\n"
        f"{start_time}\n\n"
        f"Files processed:\n"
        f"{os.linesep.join(processed_lines)}\n"
        f"{failure_block}"
    )

    # Send the email
    mail_rc = send_mail_via_cli(mail_cmd="mail", email_to=args.email, subject=subject, message=message, dry_run=args.dry_run)

    if(mail_rc != 0):
        print(f"WARNING: mail command returned nonzero exit code: {mail_rc}", file=sys.stderr)

    print(start_time)
    print("Done")


if(__name__ == "__main__"):
    main()
