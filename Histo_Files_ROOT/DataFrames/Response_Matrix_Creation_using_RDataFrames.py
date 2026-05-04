#!/usr/bin/env python3
import sys
import argparse
import ROOT, re
# import traceback
# import os
from pathlib import Path
import ROOT, re

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/'
sys.path.append(script_dir)
from File_Batches import rdf_batch, mdf_batch, gdf_batch
sys.path.remove(script_dir)
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues          import *
sys.path.remove(script_dir)
del script_dir

# import math
# import array
# import copy

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Makes Response Matricies for Unfolding (based on using_RDataFrames_python.py)", formatter_class=RawDefaultsHelpFormatter)
    
    parser.add_argument('-v',  '--verbose',
                        action='store_true', 
                        help='Prints more info while running.\n')
    parser.add_argument('-cnR', '-cRdf', '--cut_name_rdf',
                        type=str,
                        default="cut_Complete_SIDIS",
                        choices=['cut_Complete_SIDIS', 'cut_Complete_SIDIS_MM_loose', 'cut_Complete_SIDIS_MM_tight', 'cut_Complete_SIDIS_chi2_strict_pip', 'cut_Complete_SIDIS_dcfid_loose_el', 'cut_Complete_SIDIS_dcfid_loose_pip', 'cut_Complete_SIDIS_dcfid_pass1_el', 'cut_Complete_SIDIS_dcfid_pass1_pip', 'cut_Complete_SIDIS_dcfid_tight_el', 'cut_Complete_SIDIS_dcfid_tight_pip', 'cut_Complete_SIDIS_dcfidref_loose_el', 'cut_Complete_SIDIS_dcfidref_tight_el', 'cut_Complete_SIDIS_dcv_loose_el', 'cut_Complete_SIDIS_dcv_pass1_el', 'cut_Complete_SIDIS_dcv_tight_el', 'cut_Complete_SIDIS_dvz_loose_pip', 'cut_Complete_SIDIS_dvz_pass1_pip', 'cut_Complete_SIDIS_dvz_tight_pip', 'cut_Complete_SIDIS_eS1o', 'cut_Complete_SIDIS_eS2o', 'cut_Complete_SIDIS_eS3o', 'cut_Complete_SIDIS_eS4o', 'cut_Complete_SIDIS_eS5o', 'cut_Complete_SIDIS_eS6o', 'cut_Complete_SIDIS_ecband_loose_el', 'cut_Complete_SIDIS_ecband_tight_el', 'cut_Complete_SIDIS_ecoi_pass1_el', 'cut_Complete_SIDIS_ecthr_loose_el', 'cut_Complete_SIDIS_ecthr_tight_el', 'cut_Complete_SIDIS_ectri_pass1_el', 'cut_Complete_SIDIS_noSmear', 'cut_Complete_SIDIS_no_pip_testdc', 'cut_Complete_SIDIS_no_sector_pcal', 'cut_Complete_SIDIS_no_valerii_knockout', 'cut_Complete_SIDIS_pcalvol_loose', 'cut_Complete_SIDIS_pcalvol_tight', 'cut_Complete_SIDIS_pid_full_pass1', 'cut_Complete_SIDIS_pipS1o', 'cut_Complete_SIDIS_pipS2o', 'cut_Complete_SIDIS_pipS3o', 'cut_Complete_SIDIS_pipS4o', 'cut_Complete_SIDIS_pipS5o', 'cut_Complete_SIDIS_pipS6o'],
                        help="Baseline Cut name for the 'rdf' files.\n")
    parser.add_argument('-cnM', '-cMdf', '--cut_name_mdf',
                        type=str,
                        default="cut_Complete_SIDIS",
                        choices=['cut_Complete_SIDIS', 'cut_Complete_SIDIS_MM_loose', 'cut_Complete_SIDIS_MM_tight', 'cut_Complete_SIDIS_chi2_strict_pip', 'cut_Complete_SIDIS_dcfid_loose_el', 'cut_Complete_SIDIS_dcfid_loose_pip', 'cut_Complete_SIDIS_dcfid_pass1_el', 'cut_Complete_SIDIS_dcfid_pass1_pip', 'cut_Complete_SIDIS_dcfid_tight_el', 'cut_Complete_SIDIS_dcfid_tight_pip', 'cut_Complete_SIDIS_dcfidref_loose_el', 'cut_Complete_SIDIS_dcfidref_tight_el', 'cut_Complete_SIDIS_dcv_loose_el', 'cut_Complete_SIDIS_dcv_pass1_el', 'cut_Complete_SIDIS_dcv_tight_el', 'cut_Complete_SIDIS_dvz_loose_pip', 'cut_Complete_SIDIS_dvz_pass1_pip', 'cut_Complete_SIDIS_dvz_tight_pip', 'cut_Complete_SIDIS_eS1o', 'cut_Complete_SIDIS_eS2o', 'cut_Complete_SIDIS_eS3o', 'cut_Complete_SIDIS_eS4o', 'cut_Complete_SIDIS_eS5o', 'cut_Complete_SIDIS_eS6o', 'cut_Complete_SIDIS_ecband_loose_el', 'cut_Complete_SIDIS_ecband_tight_el', 'cut_Complete_SIDIS_ecoi_pass1_el', 'cut_Complete_SIDIS_ecthr_loose_el', 'cut_Complete_SIDIS_ecthr_tight_el', 'cut_Complete_SIDIS_ectri_pass1_el', 'cut_Complete_SIDIS_noSmear', 'cut_Complete_SIDIS_no_pip_testdc', 'cut_Complete_SIDIS_no_sector_pcal', 'cut_Complete_SIDIS_no_valerii_knockout', 'cut_Complete_SIDIS_pcalvol_loose', 'cut_Complete_SIDIS_pcalvol_tight', 'cut_Complete_SIDIS_pid_full_pass1', 'cut_Complete_SIDIS_pipS1o', 'cut_Complete_SIDIS_pipS2o', 'cut_Complete_SIDIS_pipS3o', 'cut_Complete_SIDIS_pipS4o', 'cut_Complete_SIDIS_pipS5o', 'cut_Complete_SIDIS_pipS6o'],
                        help="Baseline Cut name for the 'mdf' files.\n")
    parser.add_argument('-cnG', '-cGdf', '--cut_name_gdf',
                        type=str,
                        default="no_cut",
                        choices=['no_cut'],
                        help="Baseline Cut name for the 'gdf' files. Only has the 'no_cut' option currently—all other cuts to the generated files must be added separately.\n")
    parser.add_argument('-c',  '--cut',
                        type=str,
                        help=f"Adds additional cuts based on user input.\n{color.Error}Warning: applies to all datasets.{color.END}\n")
    parser.add_argument('-n', '--name',
                        type=str,
                        default=None,
                        help='Extra save name that can be added to the saved files.\n')
    parser.add_argument('-t', '--title',
                        type=str,
                        help='Extra title text that can be added to the default titles.\n')
    parser.add_argument('-bID', '--batch_id',
                        type=int,
                        default=1,
                        # choices=range(0, 109),
                        help="Uses pre-defined groups of data and (clasdis) MC files (Maximum Group Number: See File_Batches.py — 0 runs all batches together).\n")
    parser.add_argument('-numF', '-nf', '--number_of_files',
                        type=int,
                        default=-1,
                        help="Number of files allowed to run together if '--batch_id' is set to 0 (-1 corresponds to all files). Applies equally to each dataframe.\n")
    parser.add_argument('-evnL', '--event_limit',
                        type=int,
                        help=f"Event limit for all datasets (will set df.Range(...) based on this value, so only use if you don't want/need the full event statistics from the files).\n{color.Error}Use for testing only.{color.END}\n")
    parser.add_argument('-EvGen', '--Use_EvGen',
                        action='store_true', 
                        help="Includes EvGen files when running (files not yet processed as of 2/12/2026).\n")
    parser.add_argument('-2D', '--make_2D',
                        action='store_true',
                        help='Makes 2D Q2 vs y, Q2 vs xB, z vs pT, momentum vs lab angles (2 per particle), and MM vs W plots in different kinematic bins (uses the 4D bins as the z-axis variable).\n')
    parser.add_argument('-2Dr', '--make_2D_rho',
                        action='store_true',
                        help=f"Adds the rho0 kinematic plots to the list of 2D histograms to be made with '--make_2D'.\n{color.Error}Requires '--make_2D' to be run and only can be made for the MC datasets.{color.END}\n")
    parser.add_argument('-2Do', '--make_2D_only',
                        action='store_true',
                        help="Only makes the 2D histograms given by '--make_2D'.\n")
    parser.add_argument('-u5D', '--unfold_5D',
                        action='store_true',
                        help='Makes the response matrices for the full 5D unfolding (will run in addition to the 3D unfolding done by default).\n')
    parser.add_argument('-u5Do', '--unfold_5D_only',
                        action='store_true',
                        help='Only makes the response matrices for the full 5D unfolding (will skip the 3D response matrices).\n')
    parser.add_argument('-mr', '-MR', '--make_root',
                        action='store_true',
                        help="Makes a ROOT output file like 'makeROOT_epip_SIDIS_histos_new.py' (but meant for fewer histograms per run — will update old files if the path given by `--root` already exists).\n")
    parser.add_argument('-vb', '--valerii_bins',
                        action='store_true',
                        help="Runs code using Valerii's kinematic bins instead of mine (available only with the `--make_root` option as of 2/11/2025).\n")
    parser.add_argument('-hpp', '--use_hpp',
                        action='store_true',
                        help="Applies the acceptance weights. Allows the JSON weights (injected modulations) to be applied without also needing the Acceptance weights.\n")
    parser.add_argument('-aohpp', '--angles_only_hpp',
                        action='store_true',
                        help="Changes the acceptance weights being applied (with the '--make_root' option) so that only the azimuthal and polar angle weights are applied (no momentum weights).\n")
    parser.add_argument('-r', '--root',
                        type=str,
                        default="SIDIS_epip_Response_Matrices_from_RDataFrames.root", 
                        help="Name of the ROOT file to be outputted by the '--make_root' option (will still append the string from '--name' just before the '.root' of this argument's value).\n")
    parser.add_argument('-jsw', '--json_weights',
                        action='store_true',
                        help='Use the json weights (for physics injections) given by the `--json_file` argument.\n')
    parser.add_argument('-jsf', '--json_file',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json", 
                        help='JSON file path for using `json_weights`.\n')
    parser.add_argument('-sw', '--spline_weights',
                        action='store_true',
                        help="Use the new spline-based event-by-event weights (alternative to '--json_weights').\n")
    parser.add_argument('-spf', '--spline_file',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/Final_ZerothOrder_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt",
                        help="Path to the spline weight file when '--spline_weights' is used.\n")
    parser.add_argument('-hpp_in', '--hpp_input_file',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights.hpp", 
                        help="hpp file path that is used to apply the acceptance weights used/created by the '--make_2D_weight', '--make_2D_weight_check, and '--make_2D_weight_binned_check' options in 'using_RDataFrames_python.py'.\n")
    parser.add_argument('-f', '--fast',
                        action='store_true',
                        help="Tries to run the code faster by skipping some printed outputs that take more time to run.\n")
    parser.add_argument('-bc', '-BC', '--run_BC_comparison',
                        action='store_true',
                        help="Creates Images showing the differences to the phi_h distributions based on the BC_Factors from the JSON file given by '--json_file_BC'.\n")
    parser.add_argument('-jsbc', '--json_file_BC',
                        type=str,
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/BC_Corrections/Sub_Bin_Contents_for_BC_Correction.json", 
                        help="JSON file path for running '--run_BC_comparison'. The default file is for 0th order BC with EvGen corrections.\nThe equivalent clasdis corrections are stored here:  '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/BC_Corrections/Sub_Bin_Contents_for_clasdis_BC_Correction.json'\n")
    parser.add_argument('-df', '--dataframe_BC',
                        type=str,
                        default="gdf",
                        choices=['rdf', 'mdf', 'mdf_smeared', 'mdf_gen', "gdf"],
                        help="Selects which RDataFrame is used to create the images for the '--run_BC_comparison' option.\nThe different 'mdf' choices control smearing/'matched generated' plotting for the variables.\nEvGen plots are not available yet as of 2/12/2026.\n")
    parser.add_argument('-sf', '--File_Save_Format',
                        type=str,
                        default=".png",
                        choices=['.png', '.pdf'],
                        help="Save Format of Images created in the '--run_BC_comparison' option.\n")
    parser.add_argument('-e', '--email',
                        action='store_true',
                        help="Sends an email when the script is done running.\n")
    parser.add_argument('-em', '--email_message',
                        type=str,
                        default="", 
                        help="Adds an extra user-defined message to emails sent with the `--email` option.\n")
    parser.add_argument('-dr', '-ns', '-test', '--dry_run',
                        action='store_true', 
                        help='Runs a test of the histogram creation without saving them.\n')
    
    return parser.parse_args()

import subprocess
def ansi_to_plain(text):
    ansi_plain_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "", '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", '\033[0m': ""}
    sorted_codes = sorted(ansi_plain_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_plain_map[code])
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_plain(body)
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
            sys.stdout.flush()

def Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Images"):
    Name_of_Script = "Response_Matrix_Creation_using_RDataFrames.py"
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name)  in ["email", "email_message", "timer", "json_file_BC", "dataframe_BC", "File_Save_Format", "root"]):
            continue
        if((str(name) in ["number_of_files"]) and      (args.batch_id >= 0)):
            continue
        if((str(name) in ["json_file"])       and (not  args.json_weights)):
            args_list = f"""{args_list}
       Did not use JSON file(s)"""
            continue
        if((str(name) in ["hpp_input_file"])  and (not (args.use_hpp or args.angles_only_hpp))):
            args_list = f"""{args_list}
       Did not use HPP file(s)"""
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    custom_head = f'''
Input(s):
    --json_file_BC     --> {args.json_file_BC}
Output(s):
    --dataframe_BC     --> {args.dataframe_BC}
    --File_Save_Format --> {args.File_Save_Format} ''' if(args.run_BC_comparison) else f'''
Output:
    --root --> {color.BOLD}{args.root}{color.END}'''
    email_body = f"""
The '{Name_of_Script}' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

{args.email_message}

{custom_head}

Arguments:
{args_list}

{end_time}
{total_time}
{rate_line}
    """

    if(args.email):
        send_email(subject=f"Finished Running the '{Name_of_Script}' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: '{Name_of_Script}' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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


def Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""):
    # Defined for the 'Y_bin' binning option
    if(str(Variable_Type) not in ["smear", "smeared", "GEN", "Gen", "gen", "", "norm", "normal", "default"]):
        print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type='{Variable_Type}').\nFix input to use anything other than the default calculations of the 4D kinematic bin.")
        Variable_Type   = ""
        
    Q2_y_Bin_event_name = f"""Q2_Y_Bin{      "_smeared" if(str(Variable_Type) in ["smear", "smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen"]) else ""}"""
    z_pT_Bin_event_name = f"""z_pT_Bin_Y_bin{"_smeared" if(str(Variable_Type) in ["smear", "smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen"]) else ""}"""
    
    Q2_y_z_pT_4D_Bin_Def = f"""
    int Q2_y_Bin_event_val = {Q2_y_Bin_event_name};
    int z_pT_Bin_event_val = {z_pT_Bin_event_name};
    int Q2_y_z_pT_4D_Bin_event_val = 0;
    if(Q2_y_Bin_event_val >  1){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val >  2){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  3){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val >  4){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  5){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  6){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val >  7){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  8){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val >  9){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val > 10){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val > 11){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 12){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 13){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val > 14){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val > 15){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 16){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    
    Q2_y_z_pT_4D_Bin_event_val += z_pT_Bin_event_val;
    
    if(Q2_y_Bin_event_val < 1 || z_pT_Bin_event_val < 1){{ Q2_y_z_pT_4D_Bin_event_val = 0; }}
    
    return Q2_y_z_pT_4D_Bin_event_val;
    """
    # Total number of bins: 546 — Includes the migration bins in the grid, but not the zero bin
    return Q2_y_z_pT_4D_Bin_Def


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
def pair_key_after_marker(path_str, marker="Final_Analysis_Iterations_I0"):
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

if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    print(f"{color.BBLUE}\nCode is ready to run.{color.END}")
    args.timer.start()

    args.make_2D_only =  args.make_2D_only and (not args.unfold_5D_only)
    args.unfold_5D    =  args.unfold_5D     or      args.unfold_5D_only
    args.make_2D      = (args.make_2D       or      args.make_2D_only) and (not args.unfold_5D_only)

    ROOT.TH1.AddDirectory(0)
    ROOT.gStyle.SetTitleOffset(1.3,'y')
    ROOT.gStyle.SetGridColor(17)
    ROOT.gStyle.SetPadGridX(1)
    ROOT.gStyle.SetPadGridY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(1)
    
    if(".root" not in args.root):
        print(f"\n'--root' was set to {args.root}\n")
        raise ValueError("Invalid '--root' argument (the string must end with '.root')")
    if(args.spline_weights and (not args.spline_file)):
        raise ValueError("--spline_weights was used but no --spline_file was provided!")
    
    if((args.name is not None) and (str(args.name) not in str(args.root))):
        args.root = f'{str(args.root).split(".root")[0]}_{args.name}.root'

    if(all(f"_Batch{args.batch_id:03d}" not in str(check) for check in [args.root, args.name]) and (args.batch_id > 0)):
        args.root = f'{str(args.root).split(".root")[0]}_Batch{args.batch_id:03d}.root'
    
    Update_Email(args, update_message=f"\n\n{color_bg.YELLOW}\n\n\t{color.BGREEN}Running with batch files {color.CYAN}{color_bg.YELLOW}{color.UNDERLINE}{args.batch_id}{color.END}{color_bg.YELLOW}\t\n{color.END}", verbose_override=True)
    
    if(not args.Use_EvGen):
        print(f"\n{color.RED}Will NOT use EvGen Files{color.END}\n")
    else:
        print(f"\n{color.ERROR}WARNING: EvGen Files not available yet (as of 2/11/2026)...{color.END}\n")
        args.Use_EvGen = False
        sys.exit(1)
        # print(f"\n{color.BGREEN}WILL be using EvGen Files{color.END}\n")
    
    # JSON_WEIGHT_FILE = args.json_file
    
    # Load the self-contained, generated header for acceptance weights (helpers + accw_* functions)
    print(f"{color.BBLUE}Loading {color.END_B}{args.hpp_input_file}{color.BBLUE} for acceptance weights (if applicable){color.END}\n")
    ROOT.gInterpreter.Declare(f'#include "{args.hpp_input_file}"')
    
    if(not args.use_hpp):
        Update_Email(args, update_message=f"{color.Error}Not using Acceptance Weights{color.END}", verbose_override=True)
    elif(args.angles_only_hpp):
        Update_Email(args, update_message=f"{color.Error}Only using the angle Acceptance Weights (not weighing the lab momemtum for acceptance){color.END}", verbose_override=True)
    else:
        Update_Email(args, update_message=f"{color.BBLUE}Using the Full Acceptance Weights{color.END}", verbose_override=True)

    all_root_files = {}
    print(f"\n\n{color.BOLD}Will Run With:{color.END}\n")
    if(args.batch_id > 0):
        all_root_files = build_all_root_files(mdf_batch[args.batch_id], gdf_batch[args.batch_id], pair_key_after_marker, rdf_list=rdf_batch[args.batch_id], mc_key="_clasdis", all_root_files=all_root_files)
    else:
        mdf_all = combine_batches(mdf_batch, args.number_of_files)
        gdf_all = combine_batches(gdf_batch, args.number_of_files)
        rdf_all = combine_batches(rdf_batch, args.number_of_files)
        all_root_files = build_all_root_files(mdf_all, gdf_all, pair_key_after_marker, rdf_list=rdf_all, mc_key="_clasdis", all_root_files=all_root_files)

    lundrho_MC = False
    for ii in all_root_files:
        print(f"\n\t{color.BLUE}{ii}:{color.END}")
        for jj in all_root_files[ii]:
            print(f"\t\t{jj}")
            if(("lundrho" in str(jj)) and ("rdf" not in str(ii))):
                lundrho_MC = True
        print(f"\n\t{color.CYAN}Total Number of files = {color.BBLUE}{len(all_root_files[ii])}{color.END}")
    if(args.unfold_5D and lundrho_MC):
        Update_Email(args, update_message=f"{color.Error}WARNING: Cannot run the 5D response matrices with the lundrho files (as of 5/2/2026)\n\t{color.END}Turning off this option now...", verbose_override=True)
        args.unfold_5D = False
    args.num_rdf_files = len(all_root_files["rdf"])
    args.num_MC_files  = len(all_root_files["mdf_clasdis"])
    
    Update_Email(args, update_message=f"\n{color.BOLD}LOADING DATAFRAMES{color.END}", verbose_override=True)
    
    rdf           = ROOT.RDataFrame("h22", all_root_files["rdf"])
    mdf_clasdis   = ROOT.RDataFrame("h22", all_root_files["mdf_clasdis"])
    gdf_clasdis   = ROOT.RDataFrame("h22", all_root_files["gdf_clasdis"])
    if(args.Use_EvGen):
        mdf_EvGen = ROOT.RDataFrame("h22", all_root_files["mdf"])
        gdf_EvGen = ROOT.RDataFrame("h22", all_root_files["gdf"])
    if(args.event_limit):
        rdf           = rdf.Range(args.event_limit)
        mdf_clasdis   = mdf_clasdis.Range(args.event_limit)
        gdf_clasdis   = gdf_clasdis.Range(args.event_limit)
        if(args.Use_EvGen):
            mdf_EvGen = mdf_EvGen.Range(args.event_limit)
            gdf_EvGen = gdf_EvGen.Range(args.event_limit)
    
    print(f"\n{color.BBLUE}rdf{color.END}:")
    if(args.verbose or (not True)):
        for ii in range(0, len(rdf.GetColumnNames()), 1):
            print(f"\t{str((rdf.GetColumnNames())[ii]).ljust(38)} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    if(not args.fast):
        Update_Email(args, update_message=f"\tTotal entries in {color.BBLUE}rdf{color.END} files: \n{rdf.Count().GetValue():>20.0f}", verbose_override=True)
    else:
        print("Fast Load...")
    
    print(f"\n{color.Error}mdf_clasdis{color.END}:")
    if(args.verbose or (not True)):
        for ii in range(0, len(mdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((mdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_clasdis.GetColumnType(mdf_clasdis.GetColumnNames()[ii])})")
    if(not args.fast):
        Update_Email(args, update_message=f"\tTotal entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}", verbose_override=True)
    else:
        print("Fast Load...")
    
    print(f"\n{color.BGREEN}gdf_clasdis{color.END}:")
    if(args.verbose or (not True)):
        for ii in range(0, len(gdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((gdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_clasdis.GetColumnType(gdf_clasdis.GetColumnNames()[ii])})")
    if(not args.fast):
        Update_Email(args, update_message=f"\tTotal entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}", verbose_override=True)
    else:
        print("Fast Load...")
    
    if(args.Use_EvGen):
        print(f"\n{color.BOLD}{color.PINK}mdf_EvGen{color.END}:")
        if(args.verbose or (not True)):
            for ii in range(0, len(mdf_EvGen.GetColumnNames()), 1):
                print(f"\t{str((mdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_EvGen.GetColumnType(mdf_EvGen.GetColumnNames()[ii])})")
        if(not args.fast):
            Update_Email(args, update_message=f"\tTotal entries in {color.BOLD}{color.PINK}mdf_EvGen{color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}", verbose_override=True)
        else:
            print("Fast Load...")
        print(f"\n{color.BCYAN}gdf_EvGen{color.END}:")
        if(args.verbose or (not True)):
            for ii in range(0, len(gdf_EvGen.GetColumnNames()), 1):
                print(f"\t{str((gdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_EvGen.GetColumnType(gdf_EvGen.GetColumnNames()[ii])})")
        if(not args.fast):
            Update_Email(args, update_message=f"\tTotal entries in {color.BCYAN}gdf_EvGen{color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}", verbose_override=True)
        else:
            print("Fast Load...")
        
    Update_Email(args, update_message=f"\n{color.BOLD}DATAFRAMES LOADED\nAPPLYING (BASE) CUTS{color.END}\n", verbose_override=True)
    rdf           =         rdf.Filter(args.cut_name_rdf)
    mdf_clasdis   = mdf_clasdis.Filter(args.cut_name_mdf)
    if(args.Use_EvGen):
        mdf_EvGen =   mdf_EvGen.Filter(args.cut_name_mdf)
    if(args.cut_name_gdf not in ["no_cut"]):
        if(args.Use_EvGen):
            gdf_EvGen =   gdf_EvGen.Filter(args.cut_name_gdf)
        gdf_clasdis   = gdf_clasdis.Filter(args.cut_name_gdf)
    else:
        Update_Email(args, update_message=f"\n{color.RED}No cuts are applied to the generated events.{color.END}\n", verbose_override=False)

    if(args.cut):
        Update_Email(args, update_message=f"{color.Error}Applying User Cut: {color.END_B}{args.cut}{color.END}", verbose_override=True)
        rdf           =         rdf.Filter(args.cut)
        if(args.Use_EvGen):
            mdf_EvGen =   mdf_EvGen.Filter(args.cut)
            gdf_EvGen =   gdf_EvGen.Filter(args.cut)
        mdf_clasdis   = mdf_clasdis.Filter(args.cut)
        gdf_clasdis   = gdf_clasdis.Filter(args.cut)

    if(not args.fast):
        Update_Email(args, update_message=f"\t(New) Total entries in {color.BBLUE}rdf        {color.END} files: \n{rdf.Count().GetValue():>20.0f}", verbose_override=True)
        Update_Email(args, update_message=f"\t(New) Total entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}", verbose_override=True)
        Update_Email(args, update_message=f"\t(New) Total entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}", verbose_override=True)
        if(args.Use_EvGen):
            Update_Email(args, update_message=f"\t(New) Total entries in {color.BPINK}mdf_EvGen  {color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}", verbose_override=True)
            Update_Email(args, update_message=f"\t(New) Total entries in {color.BCYAN}gdf_EvGen  {color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}", verbose_override=True)
    else:
        Update_Email(args, update_message=f"\n{color.BGREEN}Done with Cuts {color.END_B}(Ran with 'fast' setting to skip the statistics change){color.END}\n", verbose_override=True)

    if(args.make_root):
        Update_Email(args, update_message=f"\n{color.BOLD}Making ROOT Output File{color.END}", verbose_override=True)
        from helper_functions_for_using_RDataFrames_python import *
        check_frame = True
        if(check_frame):
            if(not rdf.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
                print(f"\t{color.Error}WARNING:         'rdf' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
                rdf = rdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
            if(not rdf.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
                print(f"\t{color.Error}WARNING:         'rdf' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
                rdf = rdf.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
            if(not rdf.HasColumn("Q2_y_z_pT_4D_Bins")):
                print(f"\t{color.Error}WARNING:         'rdf' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
                rdf = rdf.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))
                
            if(not mdf_clasdis.HasColumn("PID_pip")):
                # print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'PID_pip' — artifically defining as 211){color.END}")
                mdf_clasdis = mdf_clasdis.Define("PID_pip", "211")
            if(not mdf_clasdis.HasColumn("PID_el")):
                # print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'PID_el'  — artifically defining as 11){color.END}")
                mdf_clasdis = mdf_clasdis.Define("PID_el", "11")
            if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
            if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
            if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))

            if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_gen")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_gen'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="3D"))
            if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h_gen")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h_gen'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="5D"))
            if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins_gen")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins_gen'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins_gen", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type="gen"))

            if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_smeared'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="3D"))
            if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h_smeared")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h_smeared'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="5D"))
            if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins_smeared")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins_smeared'){color.END}")
                mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins_smeared", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type="smear"))

            if(not gdf_clasdis.HasColumn("PID_pip")):
                # print(f"\t{color.RED}WARNING: 'gdf_clasdis' is missing 'PID_pip' — artifically defining as 211){color.END}")
                gdf_clasdis = gdf_clasdis.Define("PID_pip", "211")
            if(not gdf_clasdis.HasColumn("PID_el")):
                # print(f"\t{color.RED}WARNING: 'gdf_clasdis' is missing 'PID_el'  — artifically defining as 11){color.END}")
                gdf_clasdis = gdf_clasdis.Define("PID_el", "11")
            if(not gdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
                print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
                gdf_clasdis = gdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
            if(not gdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
                print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
                gdf_clasdis = gdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
            if(not gdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins")):
                print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
                gdf_clasdis = gdf_clasdis.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))

            if(args.Use_EvGen):
                if(not mdf_EvGen.HasColumn("PID_pip")):
                    print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'PID_pip' — artifically defining as 211){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("PID_pip", "211")
                if(not mdf_EvGen.HasColumn("PID_el")):
                    print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'PID_el'  — artifically defining as 11){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("PID_el", "11")
                if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
                if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))

                if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_gen")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_gen'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="3D"))
                if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h_gen")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h_gen'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="5D"))

                if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_smeared'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="3D"))
                if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h_smeared")):
                    # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h_smeared'){color.END}")
                    mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="5D"))

                
                if(not gdf_EvGen.HasColumn("PID_pip")):
                    # print(f"\t{color.RED}WARNING:   'gdf_EvGen' is missing 'PID_pip' — artifically defining as 211){color.END}")
                    gdf_EvGen = gdf_EvGen.Define("PID_pip", "211")
                if(not gdf_EvGen.HasColumn("PID_el")):
                    # print(f"\t{color.RED}WARNING:   'gdf_EvGen' is missing 'PID_el'  — artifically defining as 11){color.END}")
                    gdf_EvGen = gdf_EvGen.Define("PID_el", "11")
                if(not gdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
                    # print(f"\t{color.Error}WARNING:   'gdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
                    gdf_EvGen = gdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
                if(not gdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
                    # print(f"\t{color.Error}WARNING:   'gdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
                    gdf_EvGen = gdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))

        if(args.valerii_bins):
            script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
            sys.path.append(script_dir)
            from Valerii_Kinematic_Binning_Code import *
            sys.path.remove(script_dir)
            del script_dir
            ROOT.gInterpreter.Declare(Run_this_str_with_gInterpreter_for_Valeriis_Bins)
            if(not rdf.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING:         'rdf' is missing Valerii's Kinematic bins{color.END}")
                rdf         = add_valerii_bins(rdf_in=rdf,         var_type="")
            if(not mdf_clasdis.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing Valerii's Kinematic bins{color.END}")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="_smeared")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="_gen")
            if(not gdf_clasdis.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing Valerii's Kinematic bins{color.END}")
                gdf_clasdis = add_valerii_bins(rdf_in=gdf_clasdis, var_type="")
            if(args.Use_EvGen):
                if(not mdf_EvGen.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                    print(f"\t{color.Error}WARNING: 'mdf_EvGen' is missing Valerii's Kinematic bins{color.END}")
                    mdf_EvGen = add_valerii_bins(rdf_in=mdf_EvGen, var_type="")
                    mdf_EvGen = add_valerii_bins(rdf_in=mdf_EvGen, var_type="_smeared")
                    mdf_EvGen = add_valerii_bins(rdf_in=mdf_EvGen, var_type="_gen")
                if(not gdf_EvGen.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                    print(f"\t{color.Error}WARNING: 'gdf_EvGen' is missing Valerii's Kinematic bins{color.END}")
                    gdf_EvGen = add_valerii_bins(rdf_in=gdf_EvGen, var_type="")

        # === NEW SPLINE WEIGHTING BLOCK (added as alternative) ===
        if(args.spline_weights):
            if(not args.spline_file):
                Crash_Report(args, crash_message="--spline_weights was used but no --spline_file was provided!", continue_run=False)
            Update_Email(args, update_message=f"\n{color.BBLUE}Using new spline-based event-by-event weights from {args.spline_file}{color.END}\n", verbose_override=True)
            with open(args.spline_file) as f:
                spline_cpp_code = f.read()
            ROOT.gInterpreter.Declare(spline_cpp_code)
            # Define Event_Weight using the new spline function (is based entirely on individual event kinematics)
            gdf_clasdis         = gdf_clasdis.Define("Event_Weight", "ComputeSplineWeight(Q2, xB, y, z, pT, phi_t)")
            mdf_clasdis         = mdf_clasdis.Define("Event_Weight", "ComputeSplineWeight(Q2_gen, xB_gen, y_gen, z_gen, pT_gen, phi_t_gen)")
            mdf_clasdis         = mdf_clasdis.Define("W_pre",        "ComputeSplineWeight(Q2_gen, xB_gen, y_gen, z_gen, pT_gen, phi_t_gen)")
            if(args.use_hpp or args.angles_only_hpp):
                if(args.angles_only_hpp):
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared))")
                else:
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
            else:
                mdf_clasdis     = mdf_clasdis.Define("W_acc",                      "1.0")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
            if(args.Use_EvGen):
                mdf_EvGen = mdf_EvGen.Define("Event_Weight", "weight*ComputeSplineWeight(Q2, xB, y, z, pT, phi_t)")
                gdf_EvGen = gdf_EvGen.Define("Event_Weight", "weight*ComputeSplineWeight(Q2_gen, xB_gen, y_gen, z_gen, pT_gen, phi_t_gen)")
        elif(args.json_weights):
            # With the Modulation weights option, apply the modulations to both gdf and mdf before adding the acceptance weights to mdf
            Update_Email(args, update_message=f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n", verbose_override=True)
            with open(args.json_file) as f:
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
                    // safely retrieve parameters (default = 0 or 1)
                    double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 1.0;
                    double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                    double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                    // calculate weight
                    double phi_rad = phi_h * TMath::DegToRad();
                    double weight  = Par_A * (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                    return weight;
                }}
                """)
            if(args.valerii_bins):
                gdf_clasdis = gdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_xB_Bin_Valerii,     z_pT_Bin_Valerii,     phi_t)")
                mdf_clasdis = mdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_xB_Bin_Valerii_gen, z_pT_Bin_Valerii_gen, phi_t_gen)")
                mdf_clasdis = mdf_clasdis.Define("W_pre",        "ComputeWeight(Q2_xB_Bin_Valerii_gen, z_pT_Bin_Valerii_gen, phi_t_gen)")
            else:
                gdf_clasdis = gdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin,     z_pT_Bin_Y_bin,     phi_t)")
                mdf_clasdis = mdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
                mdf_clasdis = mdf_clasdis.Define("W_pre",        "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            if(args.use_hpp or args.angles_only_hpp):
                if(args.angles_only_hpp):
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared))")
                else:
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
            else:
                mdf_clasdis     = mdf_clasdis.Define("W_acc",                      "1.0")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
            if(args.Use_EvGen):
                if(args.valerii_bins):
                    mdf_EvGen   = mdf_EvGen.Define("Event_Weight", "weight*ComputeWeight(Q2_xB_Bin_Valerii_gen, z_pT_Bin_Valerii_gen, phi_t_gen)")
                    gdf_EvGen   = gdf_EvGen.Define("Event_Weight", "weight*ComputeWeight(Q2_xB_Bin_Valerii,     z_pT_Bin_Valerii,     phi_t)")
                else:
                    mdf_EvGen   = mdf_EvGen.Define("Event_Weight", "weight*ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
                    gdf_EvGen   = gdf_EvGen.Define("Event_Weight", "weight*ComputeWeight(Q2_Y_Bin,     z_pT_Bin_Y_bin,     phi_t)")
        else:
            gdf_clasdis   = gdf_clasdis.Define("Event_Weight",  "1.0")
            mdf_clasdis   = mdf_clasdis.Define("Event_Weight",  "1.0")
            mdf_clasdis   = mdf_clasdis.Define("W_pre",         "1.0")
            if(args.Use_EvGen):
                mdf_EvGen = mdf_EvGen.Define("Event_Weight", "weight")
                gdf_EvGen = gdf_EvGen.Define("Event_Weight", "weight")
            if(args.use_hpp or args.angles_only_hpp):
                if(args.angles_only_hpp):
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared))")
                else:
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
            else:
                mdf_clasdis     = mdf_clasdis.Define("W_acc",                      "1.0")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
        Histograms_All = {}
        if(args.use_hpp):
            # mdf_clasdis   = weight_norm_by_bins(df_in=mdf_clasdis, Histo_Data_In="mdf", verbose=args.verbose, Do_not_use_Smeared=False, Valerii_binning=args.valerii_bins) # See helper_functions_for_using_RDataFrames_python.py
            mdf_clasdis, args, Additional_Histos = weight_norm_by_bins_wHisto(df_in=mdf_clasdis, Histo_Data_In="mdf", args=args, Do_not_use_Smeared=False, Valerii_binning=args.valerii_bins) # See helper_functions_for_using_RDataFrames_python.py
            if(isinstance(Additional_Histos, str)):
                Crash_Report(args, crash_message=f"{Additional_Histos}\n{color.END_B}Will Continue Running Anyway...{color.END}", continue_run=True)
            elif(isinstance(Additional_Histos, dict)):
                if((len(Additional_Histos) > 0)):
                    Update_Email(args, update_message=f"'weight_norm_by_bins_wHisto()' is done running. Appending {len(Additional_Histos)} new histograms to 'Histograms_All'", verbose_override=True)
                    Histograms_All.update(Additional_Histos)
                else:
                    Update_Email(args, update_message=f"{color.Error}'weight_norm_by_bins_wHisto()' returned an empty histogram dict.{color.END}", verbose_override=True)
            else:
                Crash_Report(args, crash_message=f"{color.Error}'Additional_Histos' is neither a string OR dict... (Is a '{type(Additional_Histos)}')\n{color.END_B}Will Continue Running Anyway...{color.END}", continue_run=True)
        print(f"{color.BLUE}Will be saving to: {color.BGREEN}{args.root}{color.END}")
        sys.stdout.flush()
        Res_Binning_2D_z_pT_In     = ["z_pT_Bin_Y_bin_smeared",           -0.5,     37.5,    38]
        z_pT_phi_h_Binning         = ['MultiDim_z_pT_Bin_Y_bin_phi_t',    -1.5,    913.5,   915]
        phi_h_5D_Binning           = ['MultiDim_Q2_y_z_pT_phi_h',         -0.5,  11815.5, 11816]
        Sliced_5D_Increment        = 422 # Gives 28 slices to form the full response matrix
        if(args.valerii_bins):
            Res_Binning_2D_z_pT_In = ["z_pT_Bin_Valerii_smeared",         -0.5,     60.5,    61]
            z_pT_phi_h_Binning     = ['z_pT_phi_t_3D_Bin_Valerii',        -1.5,    960.5,   962]
            phi_h_5D_Binning       = ['Q2_xB_z_pT_phi_t_5D_Bin_Valerii',  -0.5,  11815.5, 11816]
            Sliced_5D_Increment    = 562 # Gives 41 slices to form the full response matrix
        Q2_y_or_xB_bin_range = range(-1, 18) if(not args.valerii_bins) else range(-1, 17)
        Bin_str = "Q2-y Bin" if(not args.valerii_bins) else "Valerii's Q2-xB Bin"
        if(not (args.make_2D_only or args.unfold_5D_only)):
            for Q2_y_Bins in Q2_y_or_xB_bin_range:
                if(Q2_y_Bins == 0):
                    continue
                Update_Email(args, update_message=f"{color.BLUE}Creating Histograms for {color.BGREEN}rdf{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}", verbose_override=True)
                Histograms_All = make_rm_single(sdf=rdf,           Histo_Group="Response_Matrix_Normal",     Histo_Data="rdf", Histo_Cut=f"{args.cut_name_rdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=False,                                                           Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
                Update_Email(args, update_message=f"{color.BLUE}Creating Histograms for {color.BGREEN}mdf_clasdis{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}", verbose_override=True)
                Histograms_All = make_rm_single(sdf=mdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,                                                            Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title, custom_tag=None if(not lundrho_MC) else "lundrho")
                Histograms_All = make_rm_single(sdf=mdf_clasdis,   Histo_Group="Background_Response_Matrix", Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,                                                            Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title, custom_tag=None if(not lundrho_MC) else "lundrho")
                Update_Email(args, update_message=f"{color.BLUE}Creating Histograms for {color.BGREEN}gdf_clasdis{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}", verbose_override=True)
                Histograms_All = make_rm_single(sdf=gdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut=f"{args.cut_name_gdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=args.json_weights,                                               Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title, custom_tag=None if(not lundrho_MC) else "lundrho")
                if(args.Use_EvGen):
                    Update_Email(args, update_message=f"{color.BLUE}Creating Histograms for {color.BGREEN}mdf_EvGen{color.END_B} (Q2-y Bin {Q2_y_Bins}){color.END}", verbose_override=True)
                    Histograms_All = make_rm_single(sdf=mdf_EvGen, Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,                                                        Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
                    Update_Email(args, update_message=f"{color.BLUE}Creating Histograms for {color.BGREEN}gdf_EvGen{color.END_B} (Q2-y Bin {Q2_y_Bins}){color.END}", verbose_override=True)
                    Histograms_All = make_rm_single(sdf=gdf_EvGen, Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut=f"{args.cut_name_gdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,                                                        Histograms_All=Histograms_All, file_location="output_file", output_type="output_file", Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            Update_Email(args, update_name="'make_rm_single()'", verbose_override=True)
        else:
            Update_Email(args, update_message=f"{color.Error}Skipped the 3D Response Matricies{color.END}", verbose_override=True)
        if(args.unfold_5D and (not args.make_2D_only)):
            print(f"\n{color.BGREEN}Making the 5D Response Matrices...{color.END}")
            args.timer.time_elapsed()
            sys.stdout.flush()
            Histograms_All = make_rm5d_single(sdf=rdf,             Histo_Group="Response_Matrix_Normal",     Histo_Data="rdf", Histo_Cut=f"{args.cut_name_rdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=False,              Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
            Update_Email(args, update_name=f"'make_rm5d_single({color.BGREEN}rdf{color.END})'",              verbose_override=True)
            Histograms_All = make_rm5d_single(sdf=mdf_clasdis,     Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=True,               Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
            Histograms_All = make_rm5d_single(sdf=mdf_clasdis,     Histo_Group="Background_Response_Matrix", Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=True,               Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
            Update_Email(args, update_name=f"'make_rm5d_single({color.BGREEN}mdf_clasdis{color.END})'",      verbose_override=True)
            Histograms_All = make_rm5d_single(sdf=gdf_clasdis,     Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut=f"{args.cut_name_gdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=args.json_weights,  Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
            Update_Email(args, update_name=f"'make_rm5d_single({color.BGREEN}gdf_clasdis{color.END})'",      verbose_override=True)
            if(args.Use_EvGen):
                Histograms_All = make_rm5d_single(sdf=mdf_EvGen,   Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=True,               Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
                Histograms_All = make_rm5d_single(sdf=mdf_EvGen,   Histo_Group="Background_Response_Matrix", Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="smear", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=True,               Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
                Update_Email(args, update_name=f"'make_rm5d_single({color.BGREEN}mdf_EvGen{color.END})'",    verbose_override=True)
                Histograms_All = make_rm5d_single(sdf=gdf_EvGen,   Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut=f"{args.cut_name_gdf}{'' if(not args.cut) else '_extra'}",     Histo_Smear="",      Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Q2_y_z_pT_phi_h_5D_Binning=phi_h_5D_Binning,          Use_Weight=True,  Sliced_5D_Increment=Sliced_5D_Increment, Histograms_All=Histograms_All, custom_title=args.title)
                Update_Email(args, update_name=f"'make_rm5d_single({color.BGREEN}gdf_EvGen{color.END})'",    verbose_override=True)
        else:
            Update_Email(args, update_message=f"{color.Error}Skipped the 5D Response Matricies{color.END}", verbose_override=True)
        if(args.make_2D):
            print(f"\n{color.BGREEN}Making the 2D Kinematic Plots...{color.END}")
            args.timer.time_elapsed()
            sys.stdout.flush()
            el_Binning       = ['el',        0,        8,   400]
            elth_Binning     = ['elth',      0,       40,   400]
            elPhi_Binning    = ['elPhi',     0,      360,   720]
            pip_Binning      = ['pip',       0,        6,   300]
            pipth_Binning    = ['pipth',     0,       40,   400]
            pipPhi_Binning   = ['pipPhi',    0,      360,   720]
            Q2_Binning       = ['Q2',        0,       12,   140]
            xB_Binning       = ['xB',        0,      1.0,   100]
            y_Binning        = ['y',      0.05,     1.05,   100]
            z_Binning        = ['z',         0,      1.0,   100]
            pT_Binning       = ['pT',        0,     1.05,   105]
            MM_Binning       = ['MM',      0.5,      4.5,    80]
            W_Binning        = ['W',      0.99,     4.99,    80]
            List_of_2D_Plots = [[Q2_Binning,            xB_Binning]]
            List_of_2D_Plots.append([Q2_Binning,         y_Binning])
            List_of_2D_Plots.append([z_Binning,         pT_Binning])
            List_of_2D_Plots.append([MM_Binning,         W_Binning])
            List_of_2D_Plots.append([el_Binning,      elth_Binning])
            List_of_2D_Plots.append([el_Binning,     elPhi_Binning])
            List_of_2D_Plots.append([elth_Binning,   elPhi_Binning])
            List_of_2D_Plots.append([pip_Binning,    pipth_Binning])
            List_of_2D_Plots.append([pip_Binning,   pipPhi_Binning])
            List_of_2D_Plots.append([pipth_Binning, pipPhi_Binning])

            if((args.make_2D_rho) and all((mdf_clasdis.HasColumn(needed_for_rho) and gdf_clasdis.HasColumn(needed_for_rho)) for needed_for_rho in ["rho0", "rho0th", "rho0Phi", "Par_PID_pip"])):
                # === NEW RHO KINEMATICS (MC ONLY) ===
                rho_Binning    = ['rho0',    0,        8,   400]
                rhoth_Binning  = ['rho0th',  0,       40,   400]
                rhoPhi_Binning = ['rho0Phi', 0,      360,   720]
                List_of_2D_Plots.append([rho_Binning,    rhoth_Binning])
                List_of_2D_Plots.append([rho_Binning,   rhoPhi_Binning])
                List_of_2D_Plots.append([rhoth_Binning, rhoPhi_Binning])
                # === END NEW RHO BLOCK ===

            for data, df, cut in [["rdf", rdf, args.cut_name_rdf], ["mdf", mdf_clasdis, args.cut_name_mdf], ["gdf", gdf_clasdis, args.cut_name_gdf]]:
                use_weight = (('mdf' in data) or (('gdf' in data) and ((args.json_weights) or (args.spline_weights)))) and ('rdf' not in data)
                for Vars in List_of_2D_Plots:
                    if(("rho0" in str(Vars)) and (data not in ["mdf", "gdf"])):
                        continue # Skip the rho0 plots using data
                    Use_Smear = (data not in ["rdf", "gdf"]) and ("rho0" not in str(Vars))
                    # print(f"{data} ==> {Use_Smear}")
                    Histograms_All = make_TH2D_histos(sdf=df if("rho0" not in str(Vars)) else df.Filter("Par_PID_pip == 113"), Histo_Data=data, Histo_Cut=f"{cut}{'' if(not args.cut) else '_extra'}", Histo_Smear="smear" if(Use_Smear) else "", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Vars_Input=Vars, Use_Weight=use_weight, Histograms_All=Histograms_All, Histo_Group="Normal_2D", custom_title=args.title, custom_tag=None if((not lundrho_MC) or ("rdf" in str(data))) else "lundrho")
                Update_Email(args, update_name=f"'make_TH2D_histos({color.BGREEN}{'clasdis_' if('rdf' not in data) else ''}{data}{color.END})'", verbose_override=True)
            if(args.Use_EvGen):
                for Vars in List_of_2D_Plots:
                    if("rho0" in str(Vars)):
                        continue # EvGen files do not use rho0 at all
                    Histograms_All = make_TH2D_histos(sdf=mdf_EvGen, Histo_Data="mdf", Histo_Cut=f"{args.cut_name_mdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Vars_Input=Vars, Use_Weight=True, Histograms_All=Histograms_All, Histo_Group="Normal_2D", custom_title=args.title)
                    Histograms_All = make_TH2D_histos(sdf=gdf_EvGen, Histo_Data="gdf", Histo_Cut=f"{args.cut_name_gdf}{'' if(not args.cut) else '_extra'}", Histo_Smear="", Binning="Y_bin" if(not args.valerii_bins) else "Valerii", Vars_Input=Vars, Use_Weight=True, Histograms_All=Histograms_All, Histo_Group="Normal_2D", custom_title=args.title)
                Update_Email(args, update_name=f"'make_TH2D_histos({color.BGREEN}EvGen, All{color.END})'", verbose_override=True)
        else:
            Update_Email(args, update_message=f"{color.Error}Skipped the 2D Kinematic Plots{color.END}", verbose_override=True)
        print(f"\n{color.BCYAN}Done Collecting Histograms. Ready to Save.{color.END}\n")
        args.timer.time_elapsed()
        sys.stdout.flush()
        num_histos_saved = Evaluate_And_Write_Histograms(hist_ptrs=Histograms_All, out_path=args.root, test=args.dry_run, timer=args.timer)  # See helper_functions_for_using_RDataFrames_python.py
        print(f"{color.BBLUE}Done Saving (Saved {color.END_B}{num_histos_saved}{color.BBLUE} Histograms){color.END}\n")
        Update_Email(args, update_name="'Evaluate_And_Write_Histograms()'", verbose_override=True)
        args.num_histos_saved = num_histos_saved
    else:
        print(f"\n{color.Error}Skipping ROOT Output File{color.END}")

    if(args.run_BC_comparison):
        print(f"\n{color.BOLD}Making BC Comparison Images{color.END}")
        from helper_functions_for_BC_Corrections import *
        sys.stdout.flush()
        PhiT_Var     = "phi_t"          if("smear" not in str(args.dataframe_BC)) else "phi_t_smeared"          if("gen" not in str(args.dataframe_BC)) else "phi_t_gen"
        Q2y_Bin_Var  = "Q2_Y_Bin"       if("smear" not in str(args.dataframe_BC)) else "Q2_Y_Bin_smeared"       if("gen" not in str(args.dataframe_BC)) else "Q2_Y_Bin_gen"
        z_pT_Bin_Var = "z_pT_Bin_Y_bin" if("smear" not in str(args.dataframe_BC)) else "z_pT_Bin_Y_bin_smeared" if("gen" not in str(args.dataframe_BC)) else "z_pT_Bin_Y_bin_gen"
        rdf_in       = rdf if("rdf" in str(args.dataframe_BC)) else mdf_clasdis if("mdf" in str(args.dataframe_BC)) else gdf_clasdis
        List_of_Canvases = BC_Corrections_Compare_in_z_pT_Images_Together(rdf_in, args, Q2_Y_Bin_Range=range(1,18), PhiT_Var=PhiT_Var, Q2y_Bin_Var=Q2y_Bin_Var, z_pT_Bin_Var=z_pT_Bin_Var, Normalize_Q=False, Plot_Orientation="z_pT")
        print(f"\n{color.BBLUE}Done Creating ({color.END_B}{len(List_of_Canvases)}{color.BBLUE}) Images{color.END}\n")
    else:
        print(f"\n{color.Error}Skipping ROOT Output File{color.END}")
        
    Construct_Email(args)

    print("\nEnd of Script\n\n")
