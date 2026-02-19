#!/usr/bin/env python3
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Makes Acceptance Weight to match MC REC to Data for Unfolding (based on using_RDataFrames_python.py)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-v',  '--verbose',
                        action='store_true', 
                        help='Prints more info while running.')
    parser.add_argument('-cnR', '-cRdf', '--cut_name_rdf',
                        type=str,
                        default="cut_Complete_SIDIS",
                        choices=['cut_Complete_SIDIS', 'cut_Complete_SIDIS_MM_loose', 'cut_Complete_SIDIS_MM_tight', 'cut_Complete_SIDIS_chi2_strict_pip', 'cut_Complete_SIDIS_dcfid_loose_el', 'cut_Complete_SIDIS_dcfid_loose_pip', 'cut_Complete_SIDIS_dcfid_pass1_el', 'cut_Complete_SIDIS_dcfid_pass1_pip', 'cut_Complete_SIDIS_dcfid_tight_el', 'cut_Complete_SIDIS_dcfid_tight_pip', 'cut_Complete_SIDIS_dcfidref_loose_el', 'cut_Complete_SIDIS_dcfidref_tight_el', 'cut_Complete_SIDIS_dcv_loose_el', 'cut_Complete_SIDIS_dcv_pass1_el', 'cut_Complete_SIDIS_dcv_tight_el', 'cut_Complete_SIDIS_dvz_loose_pip', 'cut_Complete_SIDIS_dvz_pass1_pip', 'cut_Complete_SIDIS_dvz_tight_pip', 'cut_Complete_SIDIS_eS1o', 'cut_Complete_SIDIS_eS2o', 'cut_Complete_SIDIS_eS3o', 'cut_Complete_SIDIS_eS4o', 'cut_Complete_SIDIS_eS5o', 'cut_Complete_SIDIS_eS6o', 'cut_Complete_SIDIS_ecband_loose_el', 'cut_Complete_SIDIS_ecband_tight_el', 'cut_Complete_SIDIS_ecoi_pass1_el', 'cut_Complete_SIDIS_ecthr_loose_el', 'cut_Complete_SIDIS_ecthr_tight_el', 'cut_Complete_SIDIS_ectri_pass1_el', 'cut_Complete_SIDIS_noSmear', 'cut_Complete_SIDIS_no_pip_testdc', 'cut_Complete_SIDIS_no_sector_pcal', 'cut_Complete_SIDIS_no_valerii_knockout', 'cut_Complete_SIDIS_pcalvol_loose', 'cut_Complete_SIDIS_pcalvol_tight', 'cut_Complete_SIDIS_pid_full_pass1', 'cut_Complete_SIDIS_pipS1o', 'cut_Complete_SIDIS_pipS2o', 'cut_Complete_SIDIS_pipS3o', 'cut_Complete_SIDIS_pipS4o', 'cut_Complete_SIDIS_pipS5o', 'cut_Complete_SIDIS_pipS6o'],
                        help="Baseline Cut name for the 'rdf' files.")
    parser.add_argument('-cnM', '-cMdf', '--cut_name_mdf',
                        type=str,
                        default="cut_Complete_SIDIS",
                        choices=['cut_Complete_SIDIS', 'cut_Complete_SIDIS_MM_loose', 'cut_Complete_SIDIS_MM_tight', 'cut_Complete_SIDIS_chi2_strict_pip', 'cut_Complete_SIDIS_dcfid_loose_el', 'cut_Complete_SIDIS_dcfid_loose_pip', 'cut_Complete_SIDIS_dcfid_pass1_el', 'cut_Complete_SIDIS_dcfid_pass1_pip', 'cut_Complete_SIDIS_dcfid_tight_el', 'cut_Complete_SIDIS_dcfid_tight_pip', 'cut_Complete_SIDIS_dcfidref_loose_el', 'cut_Complete_SIDIS_dcfidref_tight_el', 'cut_Complete_SIDIS_dcv_loose_el', 'cut_Complete_SIDIS_dcv_pass1_el', 'cut_Complete_SIDIS_dcv_tight_el', 'cut_Complete_SIDIS_dvz_loose_pip', 'cut_Complete_SIDIS_dvz_pass1_pip', 'cut_Complete_SIDIS_dvz_tight_pip', 'cut_Complete_SIDIS_eS1o', 'cut_Complete_SIDIS_eS2o', 'cut_Complete_SIDIS_eS3o', 'cut_Complete_SIDIS_eS4o', 'cut_Complete_SIDIS_eS5o', 'cut_Complete_SIDIS_eS6o', 'cut_Complete_SIDIS_ecband_loose_el', 'cut_Complete_SIDIS_ecband_tight_el', 'cut_Complete_SIDIS_ecoi_pass1_el', 'cut_Complete_SIDIS_ecthr_loose_el', 'cut_Complete_SIDIS_ecthr_tight_el', 'cut_Complete_SIDIS_ectri_pass1_el', 'cut_Complete_SIDIS_noSmear', 'cut_Complete_SIDIS_no_pip_testdc', 'cut_Complete_SIDIS_no_sector_pcal', 'cut_Complete_SIDIS_no_valerii_knockout', 'cut_Complete_SIDIS_pcalvol_loose', 'cut_Complete_SIDIS_pcalvol_tight', 'cut_Complete_SIDIS_pid_full_pass1', 'cut_Complete_SIDIS_pipS1o', 'cut_Complete_SIDIS_pipS2o', 'cut_Complete_SIDIS_pipS3o', 'cut_Complete_SIDIS_pipS4o', 'cut_Complete_SIDIS_pipS5o', 'cut_Complete_SIDIS_pipS6o'],
                        help="Baseline Cut name for the 'mdf' files.")
    parser.add_argument('-c',  '--cut',
                        type=str,
                        help='Adds additional cuts based on user input (Warning: applies to all datasets).')
    parser.add_argument('-n', '--name',
                        type=str,
                        default=None,
                        help='Extra save name that can be added to the saved files.')
    parser.add_argument('-t', '--title',
                        type=str,
                        help='Extra title text that can be added to the default titles.')
    parser.add_argument('-bID', '--batch_id',
                        type=int,
                        default=0,
                        choices=range(0, 109),
                        help="Uses pre-defined groups of data and (clasdis) MC files (Maximum Group Number: 108 — 0 runs all batches together).")
    parser.add_argument('-numF', '-nf', '--number_of_files',
                        type=int,
                        default=-1,
                        help="Number of files allowed to run together if '--batch_id' is set to 0 (-1 corresponds to all files). Applies equally to each dataframe.")
    parser.add_argument('-evnL', '--event_limit',
                        type=int,
                        help="Event limit for all datasets (will set df.Range(...) based on this value, so only use if you don't want/need the full event statistics from the files — i.e., use for testing only).")
    # parser.add_argument('-2D', '--make_2D',
    #                     action='store_true',
    #                     help='Just Makes 2D Q2 vs y, Q2 vs xB, and z vs pT plots in different kinematic bins (rdf only) - Not finished.')
    # parser.add_argument('-hpp', '--use_hpp',
    #                     action='store_true',
    #                     help="Applies the acceptance weights. Allows the JSON weights (injected modulations) to be applied without also needing the Acceptance weights.")
    parser.add_argument('-aohpp', '--angles_only_hpp',
                        action='store_true',
                        help="Changes the acceptance weights being applied (with the '--make_root' option) so that only the azimuthal and polar angle weights are applied (no momentum weights).")
    parser.add_argument('-jsw', '--json_weights',
                        action='store_true',
                        help='Use the json weights (for physics injections) given by the `--json_file` argument.')
    parser.add_argument('-jsf', '--json_file',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json", 
                        help='JSON file path for using `json_weights`.')
    # parser.add_argument('-hpp_in', '--hpp_input_file',
    #                     type=str,
    #                     default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights.hpp", 
    #                     help="hpp file path that is used to apply the acceptance weights used/created by the '--make_2D_weight', '--make_2D_weight_check, and '--make_2D_weight_binned_check' options in 'using_RDataFrames_python.py'.")
    parser.add_argument('-hpp_out', '--hpp_output_file',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/New_Pass_2_Cut_generated_acceptance_weights.hpp", 
                        help="hpp file path for outputting the generated acceptance weights header.")
    parser.add_argument('-f', '--fast',
                        action='store_true',
                        help="Tries to run the code faster by skipping some printed outputs that take more time to run.")
    parser.add_argument('-sf', '--File_Save_Format',
                        type=str,
                        default=".png",
                        choices=['.png', '.pdf'],
                        help="Save Format of Images created.")
    parser.add_argument('-e', '--email',
                        action='store_true',
                        help="Sends an email when the script is done running (if selected).")
    parser.add_argument('-em', '--email_message',
                        type=str,
                        default="", 
                        help="Adds an extra user-defined message to emails sent with the `--email` option.")
    parser.add_argument('-dr', '-ns', '-test', '--dry_run',
                        action='store_true', 
                        help='Runs a test of the histogram creation without saving them.')
    
    return parser.parse_args()

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/'
sys.path.append(script_dir)
from File_Batches import rdf_batch, mdf_batch
sys.path.remove(script_dir)
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir

import math
# import array
# import copy
import re
import traceback

from pathlib import Path
import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "", '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", '\033[0m': ""}
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)

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

def Construct_Email(args, Crashed=False, Warning=False, final_count=None):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label="Histograms", count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "root", "single_file_input"]):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'Acceptance_Weights_Creations_using_RDataFrames.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}


{args.email_message}

Arguments:{args_list}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'Acceptance_Weights_Creations_using_RDataFrames.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'Simple_RooUnfold_SelfContained.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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


def variable_Title_name_new(variable_in):
    if(variable_in in ["k0_cut"]):
        return "E^{Cutoff}_{#gamma}"
    else:
        output = variable_Title_name(variable_in)
        output = output.replace(" (lepton energy loss fraction)", "")
        return output


def validate_root_paths(label, paths, require_root_ext=True, require_root_magic=False):
    ok, bad = [], []
    for p in paths:
        pp = Path(p).expanduser()
        if(not pp.exists()):
            bad.append(f"[{label}] missing: {str(pp)}")
            continue
        if(not pp.is_file()):
            bad.append(f"[{label}] not a file: {str(pp)}")
            continue
        if((require_root_ext) and (pp.suffix.lower() != ".root")):
            bad.append(f"[{label}] not .root: {str(pp)}")
            continue
        if(require_root_magic):
            try:
                with pp.open("rb") as f:
                    head = f.read(4)
                if(head != b"root"):
                    bad.append(f"[{label}] bad ROOT signature (expected b'root'): {str(pp)}")
                    continue
            except Exception as e:
                bad.append(f"[{label}] could not read header: {str(pp)} ({e})")
                continue
        ok.append(str(pp))
    if(len(bad) > 0):
        if(len(ok) != 0):
            Crash_Report(args, crash_message=f"{color.ERROR}Missing Files{color.END_R}:\nFileNotFoundError:{color.END}\n{'\n'.join(bad)}\n\n{color.BOLD}Allowed to keep running...{color.END}", continue_run=True)
        else:
            Update_Email(args, update_message=f"{color.ERROR}Missing All Files!{color.END_R} There are no files left to actually run...{color.END}")
            raise FileNotFoundError("\n".join(bad))
    return ok

def filter_matching_pairs(list_a, list_b, key_fn, label_a="A", label_b="B", keep="error", require_nonempty_after_filter=True):
    if(not callable(key_fn)):
        raise TypeError("key_fn must be callable (e.g. a lambda or function that returns a pairing key from a path string)")
    map_a, map_b = {}, {}
    dup_a, dup_b = {}, {}
    for p in list_a:
        k = key_fn(p)
        if(k in map_a):
            dup_a.setdefault(k, [map_a[k]]).append(p)
            if(keep == "error"):
                raise RuntimeError(f"Duplicate pairing key found in {label_a}: {k}")
            if(keep == "last"):
                map_a[k] = p
        else:
            map_a[k] = p
    for p in list_b:
        k = key_fn(p)
        if(k in map_b):
            dup_b.setdefault(k, [map_b[k]]).append(p)
            if(keep == "error"):
                raise RuntimeError(f"Duplicate pairing key found in {label_b}: {k}")
            if(keep == "last"):
                map_b[k] = p
        else:
            map_b[k] = p
    common_keys = sorted(set(map_a.keys()) & set(map_b.keys()))
    filtered_a = [map_a[k] for k in common_keys]
    filtered_b = [map_b[k] for k in common_keys]
    common_key_set = set(common_keys)
    removed_a = [p for p in list_a if(key_fn(p) not in common_key_set)]
    removed_b = [p for p in list_b if(key_fn(p) not in common_key_set)]
    if((require_nonempty_after_filter) and (len(common_keys) == 0)):
        raise RuntimeError(f"No matching pairs found between {label_a} and {label_b}.")
    if(((len(removed_a) > 0) or (len(removed_b) > 0))):
        print(f"Removed unmatched files between {label_a} and {label_b}.")
        print(f"{label_a}: {len(list_a)} -> {len(filtered_a)}")
        print(f"{label_b}: {len(list_b)} -> {len(filtered_b)}")
        if(len(removed_a) > 0):
            print(f"Removed from {label_a}:")
            for p in removed_a:
                print(f"  {p}")
        if(len(removed_b) > 0):
            print(f"Removed from {label_b}:")
            for p in removed_b:
                print(f"  {p}")
    if((len(dup_a) > 0) or (len(dup_b) > 0)):
        print("Warning: duplicate pairing keys detected (kept one file per key).")
        if(len(dup_a) > 0):
            print(f"Duplicate keys in {label_a}:")
            for k in sorted(dup_a.keys()):
                print(f"  {k}:")
                for p in dup_a[k]:
                    print(f"    {p}")
        if(len(dup_b) > 0):
            print(f"Duplicate keys in {label_b}:")
            for k in sorted(dup_b.keys()):
                print(f"  {k}:")
                for p in dup_b[k]:
                    print(f"    {p}")
    return filtered_a, filtered_b

def build_all_root_files(mdf_list, gdf_list, pair_key_fn, rdf_list=None, mc_key="_clasdis", all_root_files=None, require_root_ext=True, require_root_magic=False, keep="error"):
    if(all_root_files is None):
        all_root_files = {}
    if(rdf_list is not None):
        rdf_ok = validate_root_paths("rdf", rdf_list, require_root_ext=require_root_ext, require_root_magic=require_root_magic)
        all_root_files["rdf"] = rdf_ok
    mdf_ok = validate_root_paths(f"mdf{mc_key}", mdf_list, require_root_ext=require_root_ext, require_root_magic=require_root_magic)
    gdf_ok = validate_root_paths(f"gdf{mc_key}", gdf_list, require_root_ext=require_root_ext, require_root_magic=require_root_magic)
    mdf_ok, gdf_ok = filter_matching_pairs(mdf_ok, gdf_ok, pair_key_fn, label_a=f"mdf{mc_key}", label_b=f"gdf{mc_key}", keep=keep, require_nonempty_after_filter=True)
    all_root_files[f"mdf{mc_key}"] = mdf_ok
    all_root_files[f"gdf{mc_key}"] = gdf_ok
    return all_root_files

# Pairing rule: "everything AFTER the 'marker' string should match between MDF and GDF"
def pair_key_after_marker(path_str, marker="Pass_2_PID_Tests_FC_14_V1"):
    name = Path(path_str).name
    idx = name.find(marker)
    if(idx < 0):
        raise ValueError(f"Marker not found in filename: marker={marker!r} file={name!r}")
    return name[(idx + len(marker)):]  # suffix AFTER marker; includes extension


def combine_batches(batch_list, number_of_files=-1):
    combined_list = []
    for     ii in batch_list:
        for jj in batch_list[ii]:
            combined_list.append(jj)
            if((len(combined_list) >= number_of_files) and (number_of_files > 0)):
                return combined_list
    return combined_list


def Collect_DataFrames(args):
    all_root_files = {}
    print(f"\n\n{color.BOLD}Will Run With:{color.END}\n")
    if(args.batch_id > 0):
        all_root_files = build_all_root_files(mdf_batch[args.batch_id], mdf_batch[args.batch_id], pair_key_after_marker, rdf_list=rdf_batch[args.batch_id], mc_key="_clasdis", all_root_files=all_root_files)
    else:
        mdf_all = combine_batches(mdf_batch, args.number_of_files)
        rdf_all = combine_batches(rdf_batch, args.number_of_files)
        all_root_files = build_all_root_files(mdf_all, mdf_all, pair_key_after_marker, rdf_list=rdf_all, mc_key="_clasdis", all_root_files=all_root_files)

    for ii in all_root_files:
        print(f"\n\t{color.BLUE}{ii}:{color.END}")
        for jj in all_root_files[ii]:
            print(f"\t\t{jj}")
        print(f"\n\t{color.CYAN}Total Number of files = {color.BBLUE}{len(all_root_files[ii])}{color.END}")
        
    args.num_rdf_files = len(all_root_files["rdf"])
    args.num_MC_files  = len(all_root_files["mdf_clasdis"])
    print(f"\n{color.BOLD}LOADING DATAFRAMES{color.END}")
    rdf           = ROOT.RDataFrame("h22", all_root_files["rdf"])
    mdf_clasdis   = ROOT.RDataFrame("h22", all_root_files["mdf_clasdis"])
    if(args.event_limit):
        rdf           = rdf.Range(args.event_limit)
        mdf_clasdis   = mdf_clasdis.Range(args.event_limit)
    print(f"\n{color.BBLUE}rdf{color.END}:")
    if(args.verbose):
        for ii in range(0, len(rdf.GetColumnNames()), 1):
            print(f"\t{str((rdf.GetColumnNames())[ii]).ljust(38)} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    if(not args.fast):
        print(f"\tTotal entries in {color.BBLUE}rdf{color.END} files: \n{rdf.Count().GetValue():>20.0f}")
        args.timer.time_elapsed()
    else:
        print("Fast Load...")
    
    print(f"\n{color.Error}mdf_clasdis{color.END}:")
    if(args.verbose):
        for ii in range(0, len(mdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((mdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_clasdis.GetColumnType(mdf_clasdis.GetColumnNames()[ii])})")
    if(not args.fast):
        print(f"\tTotal entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
        args.timer.time_elapsed()
    else:
        print("Fast Load...")    

    print(f"\n{color.BOLD}DATAFRAMES LOADED\n{color.END}")
    args.timer.time_elapsed()
    print(f"\n{color.BOLD}APPLYING (BASE) CUTS\n{color.END}")
    rdf           =         rdf.Filter(args.cut_name_rdf)
    mdf_clasdis   = mdf_clasdis.Filter(args.cut_name_mdf)

    if(args.cut):
        print(f"{color.Error}Applying User Cut: {color.END_B}{args.cut}{color.END}")
        rdf           =         rdf.Filter(args.cut)
        mdf_clasdis   = mdf_clasdis.Filter(args.cut)

    if(not args.fast):
        print(f"\t(New) Total entries in {color.BBLUE}rdf        {color.END} files: \n{rdf.Count().GetValue():>20.0f}")
        args.timer.time_elapsed()
        print(f"\t(New) Total entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
        args.timer.time_elapsed()
    else:
        print(f"\n{color.BGREEN}Done with Cuts {color.END_B}(Ran with 'fast' setting to skip the statistics change){color.END}\n")

    return args, rdf, mdf_clasdis


if(__name__ == "__main__"):
    args = parse_args()
    print(f"{color.BBLUE}\nCode is ready to run.{color.END}")
    args.timer = RuntimeTimer()
    args.timer.start()

    args.save_name = f"Data_to_MC_Acceptance_Weights{args.File_Save_Format}" if(not args.name) else f"Data_to_MC_Acceptance_Weights_{args.name}{args.File_Save_Format}"
    args.make_2D_weight = not args.dry_run

    ROOT.TH1.AddDirectory(0)
    ROOT.gStyle.SetTitleOffset(1.3,'y')
    ROOT.gStyle.SetGridColor(17)
    ROOT.gStyle.SetPadGridX(1)
    ROOT.gStyle.SetPadGridY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(1)
    
    # if(".root" not in args.root):
    #     print(f"\n'--root' was set to {args.root}\n")
    #     raise ValueError("Invalid '--root' argument (the string must end with '.root')")
    # if((args.name is not None) and (str(args.name) not in str(args.root))):
    #     args.root = f'{str(args.root).split(".root")[0]}_{args.name}.root'
    # if(all(f"_Batch{args.batch_id:03d}" not in str(check) for check in [args.root, args.name]) and (args.batch_id > 0)):
    #     args.root = f'{str(args.root).split(".root")[0]}_Batch{args.batch_id:03d}.root'
    
    print(f"\n\n{color_bg.YELLOW}\n\n\t{color.BGREEN}Running with batch files {color.CYAN}{color_bg.YELLOW}{color.UNDERLINE}{args.batch_id}{color.END}{color_bg.YELLOW}\t\n{color.END}")
    
    
    # # Load the self-contained, generated header for acceptance weights (helpers + accw_* functions)
    # print(f"{color.BBLUE}Loading {color.END_B}{args.hpp_input_file}{color.BBLUE} for acceptance weights (if applicable){color.END}\n")
    # ROOT.gInterpreter.Declare(f'#include "{args.hpp_input_file}"')
    
    # if(not args.use_hpp):
    #     print(f"{color.Error}Not using Acceptance Weights{color.END}")
    if(args.angles_only_hpp):
        print(f"{color.Error}Only using the angle Acceptance Weights (not weighing the lab momemtum for acceptance){color.END}")
    else:
        print(f"{color.BBLUE}Using the Full Acceptance Weights{color.END}")

    try:
        args, rdf, mdf_clasdis = Collect_DataFrames(args)
        Update_Email(args, update_name="RDataFrame Collection", verbose_override=True)
    except:
        Crash_Report(args, crash_message=f"While trying to load the RDataFrames, the code CRASHED!\nERROR MESSAGE:\n{traceback.format_exc()}", continue_run=False)


    if(args.make_2D_weight):
        try:
            print(f"\n{color.BOLD}CREATING ACCEPTANCE WEIGHTS HISTOGRAMS/CODE{color.END}\n")
            El_Binning       = ['el',      2.5,  8.0,  44]
            El_Th_Binning    = ['elth',    7.5, 35.5,  56]
            El_Phi_Binning   = ['elPhi',     0,  360, 144]
            Pip_Binning      = ['pip',     1.0,    5,  32]
            Pip_Th_Binning   = ['pipth',   4.5, 35.5,  62]
            Pip_Phi_Binning  = ['pipPhi',    0,  360, 144]
            
            List_of_Quantities_2D = [[El_Phi_Binning, Pip_Phi_Binning], [El_Th_Binning, Pip_Th_Binning], [El_Binning, Pip_Binning]]
            histos_data_match = {}
            canvas_data_match = ROOT.TCanvas("canvas_data_match", "My Canvas", int(912*1.55*25), int(547*1.55*25))
            canvas_data_match.Divide(len(List_of_Quantities_2D), 5)

            # -----------------------------
            # 1) One-time C++ helpers
            # -----------------------------
            One_Time_Cpp_Helpers = r"""
    #include <vector>
    #include <algorithm>
    #include <cmath>
    #include <string>
    inline int accw_findBin(const double value, const std::vector<double>& edges){
        if((value < edges.front()) or (value >= edges.back())){ return -1; }
        auto it = std::upper_bound(edges.begin(), edges.end(), value);
        int idx = int(it - edges.begin()) - 1;
        if((idx < 0) or (idx >= int(edges.size()) - 1)){ return -1; }
        return idx;
    }
    inline double accw_lookup2D(const double x, const double y, const std::vector<double>& ex, const std::vector<double>& ey, const std::vector<double>& grid){
        const int nx = int(ex.size()) - 1;
        const int ny = int(ey.size()) - 1;
        int ix = accw_findBin(x, ex);
        int iy = accw_findBin(y, ey);
        if((ix < 0) or (iy < 0)){ return 1.0; } // under/overflow policy
        const int idx = ix + nx*iy; // row-major
        double w = grid[idx];
        if(!(w >= 0.0) or (!std::isfinite(w))){ return 1.0; }
        return w;
    }
    """
            ROOT.gInterpreter.Declare(One_Time_Cpp_Helpers)

            # Accumulate generated wrappers to save for later use
            generated_wrappers_code = []
            generated_wrappers_code.append("// Auto-generated acceptance weight functions\n")

            def _cpp_list(vals):
                return "{" + ", ".join(f"{v:.16g}" for v in vals) + "}"

            JSON_WEIGHT_FILE = args.json_file
            if(args.json_weights):
                print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n")
                with open(JSON_WEIGHT_FILE) as f:
                    Fit_Pars = json.load(f)
                    # Build the C++ initialization string
                    cpp_map_str = "{"
                    for key, val in Fit_Pars.items():
                        cpp_map_str += f'{{"{key}", {val}}},'
                    cpp_map_str += "}"
                    
                    ROOT.gInterpreter.Declare(f"""
                    #include <map>
                    #include <string>
                    #include <cmath>
                    std::map<std::string, double> Fit_Pars = {cpp_map_str};
                    double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h) {{
                        // build the keys dynamically
                        std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                        std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                        std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                        // safely retrieve parameters (default = 1.0 or 0.0)
                        double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 1.0;
                        double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                        double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                        // calculate weight
                        double phi_rad = phi_h * TMath::DegToRad();
                        double weight  = Par_A*(1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                        return weight;
                    }}
                    """)
                wdf = mdf_clasdis.Define("ACC_Weight_Product", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            else:
                wdf = mdf_clasdis.Define("ACC_Weight_Product", "1.0")
            print(f"\n{color.BOLD}Starting 2D Histogram Loops{color.END}\n")
            args.timer.time_elapsed()

            data_histos = {}
            mc_nw_histos = {}
            for num, (x_vars, y_vars) in enumerate(List_of_Quantities_2D):
                var_x, Min_range_x, Max_range_x, Num_of_Bins_x = x_vars
                var_y, Min_range_y, Max_range_y, Num_of_Bins_y = y_vars
                rdf_name = f"{var_x}_vs_{var_y}_rdf"
                mclasdis_no_weight = f"{var_x}_vs_{var_y}_mdf_no_weight"
                Title = f"Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
                if args.title:
                    Title = f"#splitline{{Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
                data_histos[rdf_name] = rdf.Histo2D((rdf_name, Title.replace("SOURCE", f"#color[{ROOT.kBlue}]{{Experimental Data}}"), Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), var_x, var_y)
                mc_nw_histos[mclasdis_no_weight] = wdf.Histo2D((mclasdis_no_weight, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{Unweighted MC REC (clasdis)}}"), Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared")

            for num, (x_vars, y_vars) in enumerate(List_of_Quantities_2D):
                var_x, Min_range_x, Max_range_x, Num_of_Bins_x = x_vars
                var_y, Min_range_y, Max_range_y, Num_of_Bins_y = y_vars

                rdf_name        = f"{var_x}_vs_{var_y}_rdf"
                mclasdis        = f"{var_x}_vs_{var_y}_mdf"
                data_match_name = f"{var_x}_vs_{var_y}"

                print(f"\n{color.BOLD}Starting '{data_match_name}' Histograms{color.END}")
                
                Title = f"Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
                if(args.title):
                    Title = f"#splitline{{Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"

                # -----------------------------
                # 2) Build 2D histos
                # -----------------------------
                histos_data_match[rdf_name]                = data_histos[rdf_name]
                histos_data_match[mclasdis]                = wdf.Histo2D((mclasdis,                Title.replace("SOURCE", f"#color[{ROOT.kRed}]{{Smeared MC REC (clasdis)}}"),         Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared", "ACC_Weight_Product")
                histos_data_match[f"{mclasdis}_no_weight"] = mc_nw_histos[f"{var_x}_vs_{var_y}_mdf_no_weight"]

                histos_data_match[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
                histos_data_match[mclasdis].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")
                histos_data_match[f"{mclasdis}_no_weight"].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
                histos_data_match[f"{mclasdis}_no_weight"].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")

                rdf_name_norm_factor = histos_data_match[rdf_name].Integral()
                mclasdis_norm_factor = histos_data_match[mclasdis].Integral()
                mclasdis_NoWn_factor = histos_data_match[f"{mclasdis}_no_weight"].Integral()

                histos_data_match[f"norm_{rdf_name}"]           = histos_data_match[rdf_name].Clone(f"norm_{rdf_name}")
                histos_data_match[f"norm_{mclasdis}"]           = histos_data_match[mclasdis].Clone(f"norm_{mclasdis}")
                histos_data_match[f"norm_{mclasdis}_no_weight"] = histos_data_match[f"{mclasdis}_no_weight"].Clone(f"norm_{mclasdis}_no_weight")

                histos_data_match[f"norm_{rdf_name}"].Scale(          (1/rdf_name_norm_factor) if(rdf_name_norm_factor != 0) else 1)
                histos_data_match[f"norm_{mclasdis}"].Scale(          (1/mclasdis_norm_factor) if(mclasdis_norm_factor != 0) else 1)
                histos_data_match[f"norm_{mclasdis}_no_weight"].Scale((1/mclasdis_NoWn_factor) if(mclasdis_NoWn_factor != 0) else 1)

                histos_data_match[data_match_name] = histos_data_match[f"norm_{rdf_name}"].Clone(data_match_name)
                histos_data_match[data_match_name].Divide(histos_data_match[f"norm_{mclasdis}"])
                data_match_norm_factor = histos_data_match[data_match_name].Integral()
                histos_data_match[data_match_name].Scale((1/data_match_norm_factor) if(data_match_norm_factor != 0) else 1)
                
                title_base = f"#splitline{{Ratio of #frac{{Data}}{{MC-REC}} for {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)}}}{{{args.title}}}" if args.title else f"Ratio of #frac{{Data}}{{MC-REC}} for {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)}"
                histos_data_match[data_match_name].SetTitle(f"#splitline{{{title_base}}}{{Ratio is Normalized to 1}}")

                # -----------------------------
                # 3) Extract edges + row-major weights from the ratio
                # -----------------------------
                H_w = histos_data_match[data_match_name]

                nx = H_w.GetXaxis().GetNbins()
                ny = H_w.GetYaxis().GetNbins()

                edges_x = [H_w.GetXaxis().GetBinLowEdge(i) for i in range(1, nx+1)]
                edges_x.append(H_w.GetXaxis().GetBinUpEdge(nx))

                edges_y = [H_w.GetYaxis().GetBinLowEdge(j) for j in range(1, ny+1)]
                edges_y.append(H_w.GetYaxis().GetBinUpEdge(ny))

                weights = []
                for iy in range(1, ny+1):
                    for ix in range(1, nx+1):
                        val = H_w.GetBinContent(ix, iy)
                        if((val < 0.0) or (not math.isfinite(val))):
                            val = 1.0
                        weights.append(val)

                cpp_edges_x = _cpp_list(edges_x)
                cpp_edges_y = _cpp_list(edges_y)
                cpp_weights = _cpp_list(weights)

                # Pick a stable function name for this pair
                func_name = f"accw_{var_x}_vs_{var_y}"

                # -----------------------------
                # 4) Generate + declare the concrete C++ wrapper
                # -----------------------------
                wrapper_code = f"""
    double {func_name}(const double x, const double y){{
        static const std::vector<double> EX = {cpp_edges_x};
        static const std::vector<double> EY = {cpp_edges_y};
        static const std::vector<double> GRID = {cpp_weights};
        return accw_lookup2D(x, y, EX, EY, GRID);
    }}"""
                ROOT.gInterpreter.Declare(wrapper_code)
                generated_wrappers_code.append(wrapper_code)

                # -----------------------------
                # 5) Apply weight to MC (using smeared cols) to draw the next weighted MC histo
                # -----------------------------
                weight_col = f"W_{var_x}_vs_{var_y}"
                wdf = wdf.Define(weight_col, f"{func_name}({var_x}_smeared, {var_y}_smeared)").Redefine("ACC_Weight_Product", f"(ACC_Weight_Product) * ({weight_col})")

                # -----------------------------
                # 6) Draw panels (ratio / data / MC)
                # -----------------------------
                cd_num = num + 1
                canvas_data_match.cd(cd_num)
                # ROOT.gPad.SetLogz(1)
                histos_data_match[data_match_name].Draw("colz")
                canvas_data_match.cd(cd_num +   len(List_of_Quantities_2D))
                # ROOT.gPad.SetLogz(1)
                histos_data_match[f"norm_{rdf_name}"].Draw("colz")
                canvas_data_match.cd(cd_num + 2*len(List_of_Quantities_2D))
                # ROOT.gPad.SetLogz(1)
                histos_data_match[f"norm_{mclasdis}_no_weight"].Draw("colz")
                canvas_data_match.cd(cd_num + 3*len(List_of_Quantities_2D))
                # ROOT.gPad.SetLogz(1)
                histos_data_match[f"norm_{mclasdis}"].Draw("colz")
                histos_data_match[f"norm_{mclasdis}"].SetTitle(f"#splitline{{{histos_data_match[f'norm_{mclasdis}'].GetTitle()}}}{{{root_color.Bold}{{#splitline{{Before Applying the Weights in this column}}{{Applied the weights from the columns to the left}}}}}}")
                print(f"{color.BOLD}Finished '{data_match_name}' Histograms{color.END}")
                args.timer.time_elapsed()
                
                
            print(f"\n{color.BOLD}Done Creating the Histograms for getting the new event weights{color.END}\n")
            args.timer.time_elapsed()

            # all_wrappers = "\n".join(generated_wrappers_code)
            # ROOT.gInterpreter.Declare(all_wrappers)

            for num, (x_vars, y_vars) in enumerate(List_of_Quantities_2D):
                var_x, Min_range_x, Max_range_x, Num_of_Bins_x = x_vars
                var_y, Min_range_y, Max_range_y, Num_of_Bins_y = y_vars
                mclasdis  = f"{var_x}_vs_{var_y}_mdf_Final"
                Title     = f"Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
                if(args.title):
                    Title = f"#splitline{{Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
                histos_data_match[mclasdis] = wdf.Histo2D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed}]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared", "ACC_Weight_Product")
                histos_data_match[mclasdis].GetValue()
                histos_data_match[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
                histos_data_match[mclasdis].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")
                mclasdis_norm_factor = histos_data_match[mclasdis].Integral()
                histos_data_match[f"norm_{mclasdis}"] = histos_data_match[mclasdis].Clone(f"norm_{mclasdis}")
                histos_data_match[f"norm_{mclasdis}"].Scale((1/mclasdis_norm_factor) if(mclasdis_norm_factor != 0) else 1)
                canvas_data_match.cd((num + 1) + 4*len(List_of_Quantities_2D))
                # ROOT.gPad.SetLogz(1)
                histos_data_match[f"norm_{mclasdis}"].Draw("colz")
                histos_data_match[f"norm_{mclasdis}"].SetTitle(f"#splitline{{{histos_data_match[f'norm_{mclasdis}'].GetTitle()}}}{{{root_color.Bold}{{After Applying ALL Weights in this image}}}}")
            # -----------------------------
            # 7) Save the canvas (ratio / data / weighted-MC)
            # -----------------------------
            canvas_data_match.SaveAs(args.save_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{args.save_name}{color.END}")

            # -----------------------------
            # 8) Emit a reusable header with all functions
            # -----------------------------
            header_body = "".join(generated_wrappers_code)
            header_path = args.hpp_output_file
            if(args.name):
                header_path = header_path.replace(".hpp", f"_{args.name}.hpp") if(args.name not in str(header_path)) else header_path

            with open(header_path, "w") as hf:
                hf.write("// This file was auto-generated by your acceptance-weight script.\n")
                hf.write("// It contains concrete lookup functions accw_<x>_vs_<y>(x, y).\n\n")
                hf.write("#pragma once\n\n")
                hf.write("// Embedded helper definitions (self-contained)\n")
                hf.write(One_Time_Cpp_Helpers)
                hf.write("\n\n")
                hf.write(header_body)

            print(f"{color.BOLD}Wrote weight functions to: {color.BBLUE}{header_path}{color.END}")
            print(f"\n{color.BOLD}===== BEGINNING OF GENERATED ACCEPTANCE-WEIGHT CODE ====={color.END}\n")
            print(header_body)
            print(f"\n{color.BOLD}=====    END OF GENERATED ACCEPTANCE-WEIGHT CODE    ====={color.END}\n")
            args.timer.time_elapsed()
            print(f"\n{color.BOLD}DONE CREATING ACCEPTANCE WEIGHTS HISTOGRAMS/CODE{color.END}\n")
        except:
            Crash_Report(args, crash_message=f"While trying to create the Acceptance Weights, the code CRASHED!\nERROR MESSAGE:\n{traceback.format_exc()}", continue_run=False)
    else:
        print(f"\n{color.Error}Skipping Acceptance Weight Histograms{color.END}")
        
    Construct_Email(args)