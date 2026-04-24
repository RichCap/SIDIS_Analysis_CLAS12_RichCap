#!/usr/bin/env python3
import sys
import argparse

# import ROOT, numpy
import re
import traceback
# import os
from pathlib import Path
import glob
import json
import subprocess

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer #, silence_root_import
sys.path.remove(script_dir)
del script_dir


Name_of_Script = "Compile_json_logs.py"
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"{Name_of_Script}: Compile multiple JSON log files from the rdf run mode of groovy scripts into a single combined JSON file.", formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Run with more print messages.\n')
    parser.add_argument('-t', '--test',
                        action='store_true',
                        help="Run a test that prevents the code from saving outputs and prevents emails from being sent.\n")
    
    parser.add_argument('-ra', '--report_after',
                        type=int,
                        default=100,
                        help=f"Number of files that must be processed before a verbose runtime report is printed (for the current values of the 'Final_Totals' index).\n{color.Error}MUST USE WITH '--verbose'.{color.END}\n")
    

    parser.add_argument('-i', '--input_files',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Charge_Summary_Data_sidis_epip_richcap.inb.qa.new8.nSidis*.json',
                        help='Wildcard path (glob pattern) to the JSON files to compile. The script will automatically expand this into a list of files.\n')

    parser.add_argument('-o', '--output_file',
                        default='Charge_Summary_Data_sidis_epip_richcap.inb.qa.new8.nSidis_All_Files.json',
                        help='The path to the output combined JSON file.\n')
    
    parser.add_argument('-e', '--email',
                        action='store_true',
                        help='Send Email message when the script finishes running.\n')
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the default notification from '--email'.\n")

    return parser.parse_args()


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

def Update_Email(args, update_name="", update_message="", verbose_override=False, no_time=False):
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
    Script_Name = Name_of_Script
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list, dir_lists = "", ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer"]):
            continue
        if((str(name) in ["report_after"]) and (not args.verbose)):
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


def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    args.email = (args.email and (not args.test))
    
    # Collect the list of files to process
    files_to_process = sorted([Path(f) for f in glob.glob(args.input_files)])

    if(not files_to_process):
        print(f"{color.Error}Error: {color.END_R}No files found matching the input pattern.{color.END} See --help for usage.")
        sys.exit(1)

    # Combine all JSON data
    complete_new_Json, combined_data, list_of_runtime = {}, {}, []
    combined_data["Date_Compiled"] = ansi_to_plain(args.timer.start_find(return_Q=True))
    for total_index in ["Total_Number_of_Files", "Total_accumulated_charge", "Total_events", "Total_events_after_PID_Cuts", "Total_Pass_1_PID_Cut_events", "Total_Multiple_Pions_Per_event"]:
        combined_data[total_index] = 0

    for file_path in files_to_process:
        if(not file_path.is_file()):
            Update_Email(args, update_message=f"{color.BYELLOW}Warning: {file_path} is not a file.{color.Error} Skipping.{color.END}", verbose_override=True)
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if(isinstance(data, dict)):
                complete_new_Json[f"File: {file_path.name}"] = data
                combined_data["Total_Number_of_Files"]          += 1
                combined_data["Total_accumulated_charge"]       += data["accumulated_charge"]
                combined_data["Total_events"]                   += data["total_events"]
                combined_data["Total_events_after_PID_Cuts"]    += data["events_after_PID_Cuts"]
                combined_data["Total_Pass_1_PID_Cut_events"]    += data["Pass_1_PID_Cut_events"]
                combined_data["Total_Multiple_Pions_Per_event"] += data["Multiple_Pions_Per_event"]
                list_of_runtime.append(data["RunTime_in_secs"])
                if((args.verbose or args.test) and (combined_data["Total_Number_of_Files"]%args.report_after == 0)):
                    for print_report in combined_data:
                        if(print_report == "Date_Compiled"):
                            continue
                        print(f"{color.BOLD}CURRENT {color.BBLUE}'{print_report}'{color.END_B}:{color.END} {combined_data[print_report]}")
                    current_Average_Runtime = sum(list_of_runtime)/len(list_of_runtime) if(len(list_of_runtime) != 0 ) else f"{color.ERROR}ERROR{color.END}"
                    hours___Average_Runtime = f" ({current_Average_Runtime/3600:3.4f} hours)" if("ERROR" not in str(current_Average_Runtime)) else ""
                    print(f"{color.BOLD}CURRENT {color.BBLUE}'Average_Runtime'{color.END_B}:{color.END} {current_Average_Runtime} seconds{hours___Average_Runtime}\n\n")
            else:
                Update_Email(args, update_message=f"{color.BYELLOW}Warning: {file_path} JSON is not a dict.{color.Error} Skipping.{color.END}", verbose_override=True)
        except Exception as e:
            Crash_Report(args, crash_message=f"{color.Error}Warning:{color.END_R} Failed to read {color.END_B}{file_path}. {color.UNDERLINE}Will Continue Running Anyway...{color.END}\n{color.BOLD}Exception:{color.END_R} {e}\n{color.END_B}Traceback:{color.END}\n{str(traceback.format_exc())}\n", continue_run=True)

    current_Average_Runtime = sum(list_of_runtime)/len(list_of_runtime) if(len(list_of_runtime) != 0 ) else f"{color.ERROR}ERROR{color.END}"
    hours___Average_Runtime = f" ({current_Average_Runtime/3600:3.4f} hours)" if("ERROR" not in str(current_Average_Runtime)) else ""
    combined_data["Average_Runtime"] = f"{current_Average_Runtime:3.4f} seconds{hours___Average_Runtime}"
    for print_report in combined_data:
        if(print_report == "Date_Compiled"):
            continue
        Update_Email(args, update_message=f"{color.BOLD}FINAL {color.BBLUE}{f'{print_report}':<32s}{color.END_B}:{color.END} {combined_data[print_report]}", no_time=True)
    complete_new_Json["Final_Totals"] = combined_data

    if(not args.test):
        # Write the output
        try:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(complete_new_Json, f, indent=2)
            Update_Email(args, update_message=f"{color.BGREEN}Success:{color.END_G} Compiled {len(files_to_process)} file(s) into {color.BBLUE}{args.output_file}{color.END}", no_time=True)
            print("\n\n\n\n\n")
            Construct_Email(args, final_count=len(complete_new_Json), Count_Type="Records")
        except Exception as e:
            Crash_Report(args, crash_message=f"{color.Error}Error:{color.END_R} Could not write to {color.END_B}{args.output_file}:{color.END} {e}", continue_run=False)
    else:
        Update_Email(args, update_message=f"{color.GREEN}Success: WOULD have compiled {len(files_to_process)} file(s) into {color.BLUE}{args.output_file}\n{color.Error}RAN AS TEST >>> DID NOT SAVE{color.END}", no_time=True)
        print("\n\n\n\n\n")
        Construct_Email(args)


if(__name__ == "__main__"):
    main()

