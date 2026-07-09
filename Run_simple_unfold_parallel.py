#!/usr/bin/env python3

import argparse
import glob
import os
import shlex
import subprocess
import sys
import time
import traceback
from datetime import datetime

Name_of_Script = "Run_simple_unfold_parallel.py"

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import RuntimeTimer, color
sys.path.remove(script_dir)
del script_dir

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"""Usage: ./{Name_of_Script} [options]

Purpose:
  This script launches multiple parallel jobs of the Simple_RooUnfold_SelfContained.py script,
  each processing a different Q2-y bin (1 to 17 by default). It handles safe parallel execution
  with file locking (assumed in the Python script), captures per-job logs, and measures runtime
  and peak memory usage using /usr/bin/time.

What it does:
  - Launches jobs in background for parallelism.
  - Redirects stdout/stderr to per-bin log files.
  - Records timing/memory stats in separate .time files.
  - Optionally limits concurrent jobs to avoid overload.
  - Waits for all jobs to complete and prints a summary of runtimes/peak memory.

How to use:
  1. Pass options on the command line: script path, njobs, args_command (flags for Python script),
     log_dir, max_concurrent (0 = no limit).
  2. Run: ./{Name_of_Script}
  3. Outputs go to log_dir: Unfold_Log_of_Q2_y_Bin_#.out and Unfold_Time_of_Q2_y_Bin_#.time
  4. For help: ./{Name_of_Script} -h

Customization:
  - Change --args_command for different Python flags.
  - Set --max_concurrent > 0 to queue jobs (e.g., 8 for 8 at a time).

Script: {Name_of_Script}""",
        formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument('-rm', '--run_mode',
                        default='3D',
                        choices=['3D', '5D'],
                        help="Run mode: 3D = parallel Q2-y bins via Simple_RooUnfold_SelfContained.py; 5D = single Dedicated_5D_Unfold.py job.\n")

    parser.add_argument('-s', '--script',
                        type=str,
                        default='./Simple_RooUnfold_SelfContained.py',
                        help="Path to the Simple_RooUnfold_SelfContained.py script.\n")

    parser.add_argument('-n', '--njobs',
                        type=int,
                        default=17,
                        help="Number of Q2-y bins to process (jobs 1 through njobs).\n")

    parser.add_argument('-ld', '--log_dir',
                        type=str,
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Logs_for_Simple_Unfolding',
                        help="Directory for per-job .out and .time log files.\n")

    parser.add_argument('-lp', '--log_prefix',
                        type=str,
                        # default='Unfold_Without_rho0_Log_of_Q2_y_Bin_',
                        default="Unfold_rho0_Log_of_Q2_y_Bin_",
                        # default="Unfold_Log_of_Q2_y_Bin_",
                        # default="ZerothOrderAcc_Unfold_Log_of_Q2_y_Bin_",
                        help="Prefix for per-bin stdout/stderr log files.\n")

    parser.add_argument('-tp', '--time_prefix',
                        type=str,
                        # default="Unfold_Time_of_Q2_y_Bin_",
                        # default="ZerothOrderAcc_Unfold_Time_of_Q2_y_Bin_",
                        # default="Unfold_rho0_Time_of_Q2_y_Bin_",
                        default="Unfold_rho0_Log_of_Q2_y_Bin_",
                        # default='Unfold_Without_rho0_Time_of_Q2_y_Bin_',
                        help="Prefix for per-bin /usr/bin/time statistics files.\n")

    # Arguments for the Python script (easily changeable here)
    # default='-bi 1 -nt 1 -smear -u3D -e -em "Test of parallel running"'
    # default='-r "FULL_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root" -smear -u3D -e -em "Running default Unfolding as background parallel jobs. Ran in tmuxUnfold (in case there were any local issues)"'
    # default='-r ZerothOrderAcc_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root -smear -u3D -e -sfin /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_ZerothOrderAcc_All_Batches.root -mod -wa'
    # default='-r ZerothOrderAcc_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root -smear -u3D -sfin /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_ZerothOrderAcc_All_Batches.root'
    # default='--root "Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_rho0_Normalized_Response_Matrices_Final_Analysis_Iterations_I0_All.root" --single_file_input /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_rho0_Normalized_Response_Matrices_Final_Analysis_Iterations_I0_All.root --unfolding_3D --Apply_RC --fit --smear --save_json'
    # default='--root "Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root" --single_file_input /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root --unfolding_3D --Apply_RC --fit --smear --save_json'
    # default='--root "Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V3_Response_Matrices_Final_Analysis_Iterations_I0_All.root" --single_file_input /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V3_Response_Matrices_Final_Analysis_Iterations_I0_All.root --unfolding_3D --Apply_RC --fit --smear --save_json'
    # default='--root "Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root" --single_file_input /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root --unfolding_3D --Apply_RC --fit --smear --save_json'
    parser.add_argument('-ac', '--args_command',
                        default='--unfolding_3D --Apply_RC --fit --smear --save_json',
                        help="Command-line arguments passed to the unfolding script (excluding -em, -ti, and bin number).\n")
    
    parser.add_argument('-bkgs', '--background_source',
                        default='lundvpk',
                        choices=["lundvpk","lundrho","None"],
                        help="Command-line `--background_source` argument (3D: appended to args_command; 5D: passed directly to Dedicated_5D_Unfold.py).\n")

    parser.add_argument('-r', '--root',
                        # default='Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_rho0_Normalized_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V3_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='Unfolded_Parallel_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        default='Unfolded_Parallel_SIDIS_epip_from_Only_3D_wFitIntegration_V4_rho0_Subtraction.root',
                        # default='Unfolded_Parallel_SIDIS_epip_from_Only_3D_wFitIntegration_V4_WITHOUT_rho0_Subtraction.root',
                        help="Command-line `--root` argument for passing the output file name.\n")
    
    parser.add_argument('-sfi', '--single_file_input',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_rho0_Normalized_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V3_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/Copy_for_no_rhoSub_SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root',
                        help="Command-line `--single_file_input` argument for passing the input file name.\n")

    parser.add_argument('-em', '--email_message',
                        # default='Running Unfolding with 0th Order Acceptance Weights as background parallel jobs. Ran in tmuxTTree.',
                        # default='Finished running Unfolding with the Baseline Response Matricies, but from the file that also has the 0th Order Acceptance Weights available. Reran to use the most recent set of successful batched files. Was running as background parallel jobs in tmuxTTree.',
                        # default="Ran in parallel using the histograms in the ROOT files from the newest Final_Analysis_Iterations files. Ran with Harut's exclusive 'lundvpk' rho0 events subtracted directly from data as background (without the unfolding background/fake histograms). Saving the fits to the new JSON file formats. Ran in tmuxSIDIS_1.",
                        # default='Ran in parallel using the histograms in the ROOT files from the newest Final_Analysis_Iterations files. Ran WITHOUT any rho0 subtraction (for comparison to the results with the subtraction). Saving the fits to the new JSON file formats. Ran in tmuxSIDIS_1.',
                        default=f"Run was coordinated through the `{Name_of_Script}` script.",
                        help="Email message body prefix passed to each job via -em and used in the final notification.\n")
    
    parser.add_argument('-eac', '--extra_args_command',
                        type=str,
                        default='',
                        help="Extra arguments added to the run (3D: appended to args_command; 5D: passed directly to Dedicated_5D_Unfold.py).\n")

    parser.add_argument('-ti', '--title',
                        # default='Applied the 0th Order Acceptance Weights',
                        # default='Used the Pass 2 PID Refinements',
                        # default='rho0 Normalized Subtraction Run (V3)',
                        default='rho0 Normalized Subtraction Run',
                        # default='Without rho0 Subtraction',
                        help="Title string passed to each job via -ti.\n")

    # Optional: limit concurrent jobs if machine is overloaded (0 = unlimited)
    parser.add_argument('-mc', '--max_concurrent',
                        type=int,
                        default=0,
                        help="Maximum simultaneously running jobs (0 = run all njobs at once; e.g. 8 = limit to 8 at a time).\n")

    parser.add_argument('-ms', '--mail_subject',
                        default='Finished running all parallel Simple_RooUnfold_SelfContained.py tasks',
                        help="Subject line for the completion email.\n")

    parser.add_argument('-ne', '--no_email',
                        action='store_true',
                        help="Skip sending the final completion email.\n")

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Print extra information about constructed commands and job statuses.\n")

    return parser.parse_args(), parser


def apply_run_mode_defaults(parsed_args, parser):
    if(parsed_args.run_mode == '5D'):
        if(parsed_args.script == parser.get_default('script')):
            parsed_args.script = './Dedicated_5D_Unfold.py'
        if(parsed_args.njobs == parser.get_default('njobs')):
            parsed_args.njobs = 1
        if(parsed_args.mail_subject == parser.get_default('mail_subject')):
            parsed_args.mail_subject = 'Finished running Dedicated_5D_Unfold.py (5D_Bins All)'


def effective_prefixes_for_run_mode(run_mode, log_prefix, time_prefix):
    if(run_mode == '5D'):
        return (log_prefix.replace('Q2_y_Bin_', '5D_Bins_'), time_prefix.replace('Q2_y_Bin_', '5D_Bins_'), 'All')
    return (log_prefix, time_prefix, None)


def build_script_command(run_mode, script, args_command, email_message, title, job_label, background_source, extra_args_command):
    if(run_mode == '5D'):
        script_cmd = [script, '--background_source', background_source, '-em', email_message, '-e']
        if(extra_args_command.strip()):
            script_cmd += shlex.split(extra_args_command)
        return script_cmd
    return [script] + shlex.split(args_command) + ['-em', email_message, '-ti', title, str(job_label)]


def build_display_command(run_mode, script, args_command, email_message, title, job_label, background_source, extra_args_command):
    return shlex.join(build_script_command(run_mode, script, args_command, email_message, title, job_label, background_source, extra_args_command))


def build_run_command(run_mode, script, args_command, email_message, title, job_label, timefile, background_source, extra_args_command):
    return ['/usr/bin/time', '-v', '-o', timefile] + build_script_command(run_mode, script, args_command, email_message, title, job_label, background_source, extra_args_command)


def wait_for_any_job(running_jobs, verbose):
    while(True):
        for job_index, (job_label, proc, out_fh) in enumerate(running_jobs):
            returncode = proc.poll()
            if(returncode is not None):
                out_fh.close()
                finished_job = running_jobs.pop(job_index)
                if(verbose):
                    status = f'{color.BGREEN}succeeded{color.END}' if(returncode == 0) else f'{color.Error}failed (exit code {returncode}){color.END}'
                    print(f"Job {finished_job[0]} {status}")
                return finished_job
        time.sleep(0.1)


def wait_for_all_jobs(running_jobs, verbose):
    finished_jobs = []
    while(running_jobs):
        finished_jobs.append(wait_for_any_job(running_jobs, verbose))
    return finished_jobs


def print_time_summary(log_dir, time_prefix):
    time_glob = os.path.join(log_dir, f'{time_prefix}*.time')
    time_files = sorted(glob.glob(time_glob))
    summary_lines = []
    for timefile in time_files:
        try:
            with open(timefile, 'r') as time_fh:
                for line in time_fh:
                    if(('Elapsed' in line or 'Maximum resident' in line) and ('Average' not in line)):
                        summary_lines.append(f'{timefile}:{line.rstrip()}')
        except OSError as exc:
            print(f"{color.Error}Warning: could not read time file {timefile}: {exc}{color.END}")
    summary_lines.sort(key=lambda summary_line: summary_line.split(':', 1)[1] if (':' in summary_line) else summary_line)
    for summary_line in summary_lines:
        print(summary_line)


def send_completion_email(email_message, log_dir, log_prefix, mail_subject, email_address):
    mail_body = f'{email_message} See the log files in {log_dir}/{log_prefix}* for details.'
    try:
        subprocess.run(['mail', '-s', mail_subject, email_address], input=mail_body, text=True, check=True)
    except Exception:
        print(f'\n{color.Error}Warning: failed to send completion email.{color.END}')
        print(f'  Recipient: {email_address}')
        print(f'  Subject:   {mail_subject}')
        print(f'  Body:      {mail_body}')
        traceback.print_exc()


def main():
    parsed_args, parser = parse_args()
    parsed_args.timer = RuntimeTimer()
    parsed_args.timer.start()
    apply_run_mode_defaults(parsed_args, parser)

    run_mode           = parsed_args.run_mode
    args_command       = parsed_args.args_command
    background_source  = parsed_args.background_source
    extra_args_command = parsed_args.extra_args_command

    if(run_mode == '3D'):
        if("--root"              not in str(args_command)):
            args_command = f'{args_command} --root "{parsed_args.root}"'
        if("--single_file_input" not in str(args_command)):
            args_command = f'{args_command} --single_file_input "{parsed_args.single_file_input}"'
        if("--background_source" not in str(args_command)):
            args_command = f'{args_command} --background_source "{background_source}"'
        if(extra_args_command not in [""]):
            args_command = f'{args_command} {extra_args_command}'

    script          = parsed_args.script
    njobs           = parsed_args.njobs
    log_dir         = parsed_args.log_dir
    email_message   = parsed_args.email_message
    title           = parsed_args.title
    max_concurrent  = parsed_args.max_concurrent

    log_prefix, time_prefix, fixed_bin_label = effective_prefixes_for_run_mode(run_mode, parsed_args.log_prefix, parsed_args.time_prefix)

    if(run_mode == '5D'):
        job_labels = [fixed_bin_label]
    else:
        job_labels = list(range(1, njobs + 1))

    os.makedirs(log_dir, exist_ok=True)

    print(f'{color.BOLD}===================================================================={color.END}')

    if(run_mode == '5D'):
        print(' Starting Dedicated_5D_Unfold.py run (5D mode)')
        print('   Jobs       : All (5D_Bins)')
        extra_part = f' {extra_args_command}' if (extra_args_command.strip()) else ''
        print(f'   Command    : {script} --background_source {background_source} -em <message> -e{extra_part}')
    else:
        print(' Starting parallel RooUnfold test run (3D mode)')
        print(f'   Jobs       : 1 to {njobs}')
        print(f'   Command    : {script} {args_command} <bin>')
    print(f'   Start time : {datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")}')
    print(f'{color.BOLD}===================================================================={color.END}')


    running_jobs  = []
    launched_jobs = []

    for job_label in job_labels:
        outfile  = os.path.join(log_dir, f'{log_prefix}{job_label}.out')
        timefile = os.path.join(log_dir, f'{time_prefix}{job_label}.time')

        if(run_mode == '5D'):
            print(f'{color.BOLD}Launching 5D_Bins All job → {outfile} + {timefile}{color.END}')
        else:
            print(f'{color.BOLD}Launching job {job_label} → {outfile} + {timefile}{color.END}')

        display_cmd = build_display_command(run_mode, script, args_command, email_message, title, job_label, background_source, extra_args_command)
        run_cmd     = build_run_command(run_mode, script, args_command, email_message, title, job_label, timefile, background_source, extra_args_command)

        with open(outfile, 'w') as log_fh:
            log_fh.write(f'Full command: {display_cmd}\n')

        if(parsed_args.verbose):
            print(f'  Display command: {display_cmd}')
            print(f'  Run command:     {shlex.join(run_cmd)}')

        out_fh = open(outfile, 'a')
        proc   = subprocess.Popen(run_cmd, stdout=out_fh, stderr=subprocess.STDOUT)
        running_jobs.append((job_label, proc, out_fh))
        launched_jobs.append((job_label, proc, out_fh))

        if(max_concurrent > 0 and len(running_jobs) >= max_concurrent):
            wait_for_any_job(running_jobs, parsed_args.verbose)

    print('')
    print(f'All {len(job_labels)} jobs launched. Waiting for completion...')
    print('')
    print(f'Start time  : {datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")}')
    print('')

    wait_for_all_jobs(running_jobs, parsed_args.verbose)

    failed_jobs = []
    for job_label, proc, out_fh in launched_jobs:
        returncode = proc.returncode
        if(returncode == 0):
            print(f'{color.BGREEN}Job {job_label}: succeeded{color.END}')
            parsed_args.timer.time_elapsed()
        else:
            print(f'{color.Error}Job {job_label}: failed (exit code {returncode}){color.END}')
            parsed_args.timer.time_elapsed()
            failed_jobs.append(job_label)

    print('')
    print(f'{color.BOLD}===================================================================={color.END}')
    print(' All jobs finished')
    print(f' End time   : {datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")}')
    print('')
    print(f' Log files:   {log_dir}/{log_prefix}*.out')
    print(f' Time stats:  {log_dir}/{time_prefix}*.time  (includes runtime + peak RSS memory)')
    print('')
    print(' Quick summary of runtimes and peak memory:')
    print('------------------------------------------')
    print_time_summary(log_dir, time_prefix)
    print(f'{color.BOLD}===================================================================={color.END}')

    if(not parsed_args.no_email):
        send_completion_email(email_message, log_dir, log_prefix, parsed_args.mail_subject, "richard.capobianco@uconn.edu")

    if(failed_jobs):
        parsed_args.timer.stop()
        print(f'\n{color.Error}Exiting with failure: jobs {failed_jobs} did not complete successfully.{color.END}\n')
        sys.exit(1)
    sys.exit(0)


if(__name__ == '__main__'):
    main()
    