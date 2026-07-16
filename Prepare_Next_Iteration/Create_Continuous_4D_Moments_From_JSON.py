#!/usr/bin/env python3

import os
import sys
import re
import json
import argparse
import numpy as np
from scipy.interpolate import RBFInterpolator
import pickle
import subprocess

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis' if(os.path.exists('/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis')) else '/Users/richardcapobianco/Desktop/Work_Offline.nosync/General_Helper_Scripts'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
from Binning_Dictionaries             import Full_Bin_Definition_Array
from Cross_Section_Normalization      import Cross_Section_Normalization
sys.path.remove(script_dir)

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    p = argparse.ArgumentParser(description="Create_Continuous_4D_Moments_From_JSON.py: Build tunable continuous spline functions (4D / 5D / 4D_xB) from the same JSON files used in 'Full_Moment_Plots_Creation_From_JSON.py'.", formatter_class=RawDefaultsHelpFormatter)

    p.add_argument("-v", "--verbose",
                   action="store_true",
                   help="Verbose logging.\n")
    
    p.add_argument('-e', '--email',
                        action='store_true',
                        help='Send Email message when the script finishes running for record keeping.\n')
    p.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the notification from '--email'.\n")

    p.add_argument("-js", "-json", "--json_file",
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Appended_in_Parallel_Fixed_RC_Factor_Normalization_Full.json" if(os.path.exists('/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis')) else 'Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Updated_with_Old_RC_for_Unfolded_Parallel_SIDIS_epip_from_Only_3D_wFitIntegration_V4_rho0_Subtraction.json',
                   help="Input JSON file produced by your fit workflow.\n")
    
    p.add_argument("-L", "--list_fit_sets",
                   action="store_true",
                   help="List available fit-set keys in the JSON and exit.\n")
    p.add_argument("-f", "--fit_set",
                   default="Fit_Pars_from_3D_BC_RC_Bayesian",
                   help="Top-level JSON key to use.\n")
    
    p.add_argument("-cs", "-cs_A", "--apply_A_corr",
                   action="store_true",
                   help=f"Apply Cross Section Normalization to the 'Fit_Par_A' measurements.\n{color.Error}WARNING: Do not run with the '_(Normalized)' Fit Sets{color.END}.\n")
    
    p.add_argument("-err", "--err_suffix",
                   default="_ERR",
                   # help="Error key suffix (Fit_Par_B + _ERR -> Fit_Par_B_ERR).\n")
                   help=argparse.SUPPRESS)
    
    p.add_argument("-o", "--output_prefix",
                   default="Continuous_Moments",
                   help="Prefix for output files.\n")

    p.add_argument("-gi", "--generate_init",
                   action="store_true",
                   help="Print a ready-to-use initial parameter dictionary using the B and C splines.\n")
    p.add_argument("-si", "--save_init",
                   type=str,
                   default=None,
                   help=f"Text file name to be used with '--generate_init'.\n{color.BOLD}Will save the output of '--generate_init' to a txt file of this argument's name {color.UNDERLINE}ONLY{color.END_B} if it is passed.{color.END}\n")
    p.add_argument("-rp", "--range_pct",
                   type=float,
                   default=30.0,
                   help="Percentage range for limits around spline value (used only with --use_range_pct).\n")
    p.add_argument("-std", "--std_multiple",
                   type=float,
                   default=1.0,
                   help="Multiplier on the population std of the 81-point spline evaluations for B/C limits (default mode).\n")
    p.add_argument("-urp", "--use_range_pct",
                   action="store_true",
                   help="Use legacy range-percentage limits (--range_pct + fixed offsets) instead of the default 81-point std method.\n")

    # === NEW DIMENSION MODE ===
    p.add_argument("-dm", "--dimension_mode",
                   choices=["4D", "5D", "4D_xB"],
                   default="4D",
                   help="Spline dimensionality:\n  4D     = Q², y, z, pT (original)\n  5D     = Q², y, z, pT, xB\n  4D_xB  = xB, y, z, pT (xB replaces Q²)\n")

    # === TUNING KNOBS ===
    p.add_argument("-s", "--smoothing_factor",
                   type=float,
                   default=1.0,
                   help="Multiplier on median uncertainty for smoothing (0 = exact interpolation, 1 = default, >1 = smoother).\n")
    p.add_argument("-sA", "--smoothing_factor_A",
                   type=float,
                   default=None,
                   help="Exact Smoothing Factor applied to the Fit Parameter A (Amplitude). Use if you want to override the default 'smoothing_factor' for this parameter's fits.\n")
    p.add_argument("-sB", "--smoothing_factor_B",
                   type=float,
                   default=None,
                   help="Exact Smoothing Factor applied to the Fit Parameter B (CosPhi Moments). Use if you want to override the default 'smoothing_factor' for this parameter's fits.\n")
    p.add_argument("-sC", "--smoothing_factor_C",
                   type=float,
                   default=None,
                   help="Exact Smoothing Factor applied to the Fit Parameter C (Cos2Phi Moments). Use if you want to override the default 'smoothing_factor' for this parameter's fits.\n")
    
    p.add_argument("-k", "--kernel",
                   choices=["thin_plate_spline", "cubic", "multiquadric", "inverse", "gaussian", "linear"],
                   default="thin_plate_spline",
                   help="Kernel type for the RBF spline.\n")
    p.add_argument("-kA", "--kernel_A",
                   choices=["thin_plate_spline", "cubic", "multiquadric", "inverse", "gaussian", "linear"],
                   default=None,
                   help="Kernel type for the RBF spline for the Fit Parameter A (use if a unique kernal is preferred for this parameter).\n")
    
    p.add_argument("-eps", "--epsilon",
                   type=float,
                   default=None,
                   help="Epsilon parameter (scale) for the kernel. Leave blank for auto-tuning.\n")

    p.add_argument("-logA", "--log_A",
                   action="store_true",
                   help="Fit Fit_Par_A in log-space (RBF on log(A), evaluate with exp). Helps Amplitude multi-decade dynamic range and reduces between-point oscillations. B/C are unchanged.\n")
    
    p.add_argument("-t", "--test",
                   action="store_true",
                   help="Only parse JSON and print summary; do not build or save anything.\n")

    p.add_argument("-gc", "--generate_spline_code",
                   action="store_true",
                   help="Generate a single C++ text file containing ComputeSplineWeight() for direct use in RDataFrame.\nThe output file name is auto-generated based on the same controls as the '.npz' files but with 'Compute_SplineWeight.txt' as the suffix instead of the fit parameters.\n")
    
    p.add_argument("-gcO", "--generate_spline_code_only",
                   action="store_true",
                   help="Only runs the '--generate_spline_code' code and skips all the other parts of the script.\n")

    return p.parse_args()


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

def Update_Email(args, update_name="", update_message="", verbose_override=False, no_time=True):
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
    Script_Name = "Create_Continuous_4D_Moments_From_JSON.py"
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list, dir_lists = "", ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer"]):
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


def load_json(args):
    if(not os.path.isfile(args.json_file)):
        Crash_Report(args, crash_message=f"{color.Error}ERROR: JSON file not found:{color.END_R} {args.json_file}{color.END}", continue_run=False)
    with open(args.json_file, "r") as jf:
        return json.load(jf)

def list_fit_sets(json_obj):
    keys = [str(kk) for kk in json_obj.keys()]
    keys.sort()
    return keys

def select_default_fit_set(json_obj):
    candidates = []
    for kk, vv in json_obj.items():
        if(str(kk) == "Meta_Data_of_Last_Run"):
            continue
        if((isinstance(vv, dict)) and (len(vv) > 0)):
            candidates.append(str(kk))
    if(not candidates):
        return ""
    normalized = [cc for cc in candidates if("(Normalized)" in cc)]
    if(normalized):
        normalized.sort()
        return normalized[0]
    candidates.sort()
    return candidates[0]

def sanitize_for_filename(text_in):
    txt = str(text_in)
    txt = re.sub(r"\s+", "_", txt)
    txt = re.sub(r"[^A-Za-z0-9_]+", "_", txt)
    txt = re.sub(r"_+", "_", txt)
    txt = txt.strip("_")
    return txt

def parse_inner_key(key_str):
    mm = re.fullmatch(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", str(key_str).strip())
    if(mm is None):
        raise ValueError(f"Key '{key_str}' does not match '(Q2_y_Bin_#)-(z_pT_Bin_#)'")
    return int(mm.group(1)), int(mm.group(2))

def Construct_JSON_Info(Q2_y_Bin, z_pT_Bin, return_info=None):
    if(return_info is None):
        return_info = {}
    key = f"(Q2_y_Bin_{Q2_y_Bin})-(z_pT_Bin_{z_pT_Bin})"
    if(all(str(bins) not in ["0", "-1", "All"] for bins in [Q2_y_Bin, z_pT_Bin])):
        Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array.get(f"Q2-y={Q2_y_Bin}, Q2-y", (0,0,0,0))
        z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array.get(f"Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}", (0,0,0,0))
        Q2val = (Q2_max + Q2_min) / 2
        y_val =  (y_max + y_min)  / 2
        z_val =  (z_max + z_min)  / 2
        pTval = (pT_max + pT_min) / 2
        return_info[key] = {"Q2range": [Q2val, Q2_min, Q2_max],
                            "y_range": [y_val,  y_min,  y_max],
                            "z_range": [z_val,  z_min,  z_max],
                            "pTrange": [pTval, pT_min, pT_max]
                            }
    return return_info

def build_info_map(fit_dict):
    info_map = {}
    for key_str in fit_dict.keys():
        q2y_bin, zpt_bin = parse_inner_key(key_str)
        Construct_JSON_Info(str(q2y_bin), str(zpt_bin), return_info=info_map)
    return info_map

def Convert_xB_var(xB_in=None, Q2_in=None, y_in=None, Var_out="y"):
    Conversion_Factor = 0.0502731 # From xB = Q2/(2*M*E*y) -> Conversion_Factor = 1/(2*M*E)
    if(Var_out == "xB"):
        return (Conversion_Factor*(Q2_in/y_in))  if((None not in [Q2_in,  y_in]) and (y_in  != 0)) else xB_in
    if(Var_out == "y"):
        return (Conversion_Factor*(Q2_in/xB_in)) if((None not in [Q2_in, xB_in]) and (xB_in != 0)) else y_in
    if(Var_out == "Q2"):
        return ((xB_in*y_in)/Conversion_Factor)  if( None not in [xB_in,  y_in])                   else Q2_in
    return None

# ------------------------------------------------------------
# Build data points for any dimension mode
# ------------------------------------------------------------
def build_data(fit_dict, info_map, y_par, args):
    points = []
    values = []
    stds   = []
    for key_str, entry in fit_dict.items():
        if((y_par not in entry) or (f"{y_par}{args.err_suffix}" not in entry)):
            continue
        if(key_str not in info_map):
            continue
        inf = info_map[key_str]
        Q2_val = inf["Q2range"][0]
        y_val  = inf["y_range"][0]
        z_val  = inf["z_range"][0]
        Pt_val = inf["pTrange"][0]
        val = float(entry[y_par])
        err = float(entry[f"{y_par}{args.err_suffix}"])

        # === Apply normalization correction to A only ===
        if((getattr(args, "apply_A_corr", False)) and (y_par == "Fit_Par_A")):
            q2y_bin, zpt_bin = parse_inner_key(key_str)
            _, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y_bin, z_pT_Bin=zpt_bin, args_in=args)
            if((str(Bin_Width_Area_Scale) not in ["0", "None", None]) and (str(Luminosity) not in ["0", "None", None])):
                val = val/(Bin_Width_Area_Scale*Luminosity)
                err = err/(Bin_Width_Area_Scale*Luminosity)

        # === Build the point for the spline ===
        if(args.dimension_mode == "4D"):
            points.append([Q2_val, y_val, z_val, Pt_val])
        elif(args.dimension_mode == "5D"):
            xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
            points.append([Q2_val, y_val, z_val, Pt_val, xB])
        elif(args.dimension_mode == "4D_xB"):
            xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
            points.append([xB, y_val, z_val, Pt_val])

        values.append(val)
        stds.append(err)
    return (np.array(points, dtype=float), np.array(values, dtype=float),  np.array(stds, dtype=float))

# ------------------------------------------------------------
# Generate New Initial Dictionary for Moment Fits
# ------------------------------------------------------------
def load_spline_models(args):
    spline_models = {}
    if(args.output_prefix is None):
        return spline_models
    if(str(args.output_prefix).strip() in ["", "None", "none"]):
        return spline_models
    for y_par in ["Fit_Par_B", "Fit_Par_C"]:
        # UPDATED: include dimension_mode in filename
        pkl_file = f"{args.output_prefix}_{args.dimension_mode}_{args.fit_set}_{y_par}.pkl"
        if(not os.path.isfile(pkl_file)):
            print(f"{color.BYELLOW}[INFO] Missing spline file for {y_par}: {pkl_file}{color.END}")
            continue
        try:
            with open(pkl_file, "rb") as pklf:
                spline_obj = pickle.load(pklf)
        except Exception as ee:
            print(f"{color.Error}WARNING:{color.END_R} Failed to load spline file '{pkl_file}': {ee}{color.END}")
            continue
        log_space = False
        if(isinstance(spline_obj, dict)):
            cfg = spline_obj.get("config", {}) if(isinstance(spline_obj.get("config", {}), dict)) else {}
            log_space = bool(cfg.get("log_space", False))
            if("rbf" in spline_obj):
                spline_obj = spline_obj["rbf"]
            elif("spline" in spline_obj):
                spline_obj = spline_obj["spline"]
        if(spline_obj is None):
            continue
        if(log_space):
            spline_obj = ExpRBFWrapper(spline_obj)
        spline_models[y_par] = spline_obj
        if(args.verbose):
            print(f"{color.GREEN}[INFO] Loaded {args.dimension_mode} spline for {y_par}: {pkl_file}{color.END}")
    return spline_models

# Hardcoded Trusted / Sectors blocks from Phi_h_Fit_Parameters_Initialize.py (do not edit the template file)
TRUSTED_AND_SECTORS_BLOCK = '''    ("1", "All", "Trusted"): {
        # "fit_range_lower": 45,
        # "fit_range_upper": 315
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("2", "All", "Trusted"): {
        # "fit_range_lower": 30,
        "fit_range_lower": 45,
        "fit_range_upper": 330
    },
    ("3", "All", "Trusted"): {
        # "fit_range_lower": 30,
        "fit_range_lower": 15,
        "fit_range_upper": 330
    },
    ("4", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("5", "All", "Trusted"): {
        # "fit_range_lower": 45,
        # "fit_range_upper": 315
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("6", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("7", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("8", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("9", "All", "Trusted"): {
        # "fit_range_lower": 30,
        "fit_range_lower": 45,
        "fit_range_upper": 330
    },
    ("10", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("11", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("12", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("13", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("14", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("15", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("16", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("17", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },

    ("1", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("2", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 315
    },
    ("3", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("4", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("5", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("6", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("7", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("8", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("9", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 315
    },
    ("10", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("11", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("12", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("13", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("14", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("15", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("16", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("17", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
'''

def _iter_all_zpT_bins():
    # Yield (q2y_bin_str, zpt_bin_str) for every valid z-pT bin in Full_Bin_Definition_Array
    bin_list = []
    for key_str in Full_Bin_Definition_Array.keys():
        mm = re.fullmatch(r"Q2-y=(\d+), z-pT=(\d+)", str(key_str).strip())
        if(mm is None):
            continue
        bin_list.append((mm.group(1), mm.group(2)))
    bin_list.sort(key=lambda pair: (int(pair[0]), int(pair[1])))
    return bin_list

def _build_eval_point(Q2_val, y_val, z_val, Pt_val, args):
    # Build a single spline evaluation point for the current dimension_mode
    if(args.dimension_mode == "4D"):
        point = np.column_stack([[Q2_val], [y_val], [z_val], [Pt_val]])
    elif(args.dimension_mode == "5D"):
        xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
        point = np.column_stack([[Q2_val], [y_val], [z_val], [Pt_val], [xB]])
    elif(args.dimension_mode == "4D_xB"):
        xB = Convert_xB_var(Q2_in=Q2_val, y_in=y_val, Var_out="xB")
        point = np.column_stack([[xB], [y_val], [z_val], [Pt_val]])
    else:
        raise ValueError(f"Unsupported dimension_mode: {args.dimension_mode}")
    return point

def _evaluate_spline_safe(spline_obj, point):
    # Evaluate one spline at one point; RBF often returns a length-1 array
    try:
        result = spline_obj(point)
    except Exception:
        result = spline_obj(np.asarray(point, dtype=float))
    return float(np.ravel(np.asarray(result, dtype=float))[0])

def generate_initial_dict(info_map, args):
    print(f"\n{color.BOLD}=== Generating Initial Parameter Dictionary (Phi_h_Fit_Parameters_from_Spline.py) ==={color.END}\n")
    use_legacy_range = getattr(args, "use_range_pct", False)
    std_multiple = float(getattr(args, "std_multiple", 1.0))
    range_pct = getattr(args, "range_pct", 30.0) / 100.0

    # Require both B and C splines before writing anything
    spline_models = load_spline_models(args)
    if(("Fit_Par_B" not in spline_models) or ("Fit_Par_C" not in spline_models)):
        print(f"{color.Error}ERROR:{color.END} Missing required B and/or C spline models for generation.")
        print(f"{color.Error}  Loaded keys: {list(spline_models.keys())}{color.END}")
        print(f"{color.Error}  Expected pkl files like: {args.output_prefix}_{args.dimension_mode}_{args.fit_set}_Fit_Par_B.pkl / Fit_Par_C.pkl{color.END}")
        print(f"{color.Error}  Aborting — Phi_h_Fit_Parameters_from_Spline.py was NOT written.{color.END}")
        return

    b_spline = spline_models["Fit_Par_B"]
    c_spline = spline_models["Fit_Par_C"]
    bin_pairs = _iter_all_zpT_bins()
    if(not bin_pairs):
        print(f"{color.Error}ERROR:{color.END} No valid Q2-y / z-pT bins found in Full_Bin_Definition_Array.")
        print(f"{color.Error}  Aborting — Phi_h_Fit_Parameters_from_Spline.py was NOT written.{color.END}")
        return

    dict_lines = []
    n_ok = 0
    n_skip = 0
    critical_failure = False

    for q2y_bin, zpt_bin in bin_pairs:
        q2y_key = f"Q2-y={q2y_bin}, Q2-y"
        zpt_key = f"Q2-y={q2y_bin}, z-pT={zpt_bin}"
        if((q2y_key not in Full_Bin_Definition_Array) or (zpt_key not in Full_Bin_Definition_Array)):
            print(f"{color.Error}ERROR:{color.END} Missing bin definition for ({q2y_bin}, {zpt_bin})")
            n_skip += 1
            critical_failure = True
            break

        Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[q2y_key]
        z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[zpt_key]
        if(all(abs(float(vv)) < 1e-15 for vv in [Q2_max, Q2_min, y_max, y_min, z_max, z_min, pT_max, pT_min])):
            print(f"{color.Error}ERROR:{color.END} Degenerate (zero) bin ranges for ({q2y_bin}, {zpt_bin})")
            n_skip += 1
            critical_failure = True
            break

        Q2_avg = 0.5 * (float(Q2_min) + float(Q2_max))
        y_avg  = 0.5 * (float(y_min)  + float(y_max))
        z_avg  = 0.5 * (float(z_min)  + float(z_max))
        pT_avg = 0.5 * (float(pT_min) + float(pT_max))

        try:
            if(use_legacy_range):
                # Legacy: single center-point evaluation + range_pct / fixed offsets
                point = _build_eval_point(Q2_avg, y_avg, z_avg, pT_avg, args)
                B_val = _evaluate_spline_safe(b_spline, point)
                C_val = _evaluate_spline_safe(c_spline, point)
                if(not (np.isfinite(B_val) and np.isfinite(C_val))):
                    print(f"{color.Error}ERROR:{color.END} Non-finite spline value for bin ({q2y_bin}, {zpt_bin}): B={B_val}, C={C_val}")
                    n_skip += 1
                    critical_failure = True
                    break
                B_min = min([B_val * (1 - range_pct), B_val - 0.15])
                B_max = max([B_val * (1 + range_pct), B_val + 0.15])
                C_min = min([C_val * (1 - range_pct), C_val - 0.075])
                C_max = max([C_val * (1 + range_pct), C_val + 0.075])
                B_init, C_init = B_val, C_val
            else:
                # Default: 81-point Cartesian product of {min, avg, max} for Q2, y, z, pT
                Q2_opts = [float(Q2_min), Q2_avg, float(Q2_max)]
                y_opts  = [float(y_min),  y_avg,  float(y_max)]
                z_opts  = [float(z_min),  z_avg,  float(z_max)]
                pT_opts = [float(pT_min), pT_avg, float(pT_max)]
                B_vals = []
                C_vals = []
                for Q2_val in Q2_opts:
                    for y_val in y_opts:
                        for z_val in z_opts:
                            for Pt_val in pT_opts:
                                point = _build_eval_point(Q2_val, y_val, z_val, Pt_val, args)
                                B_vals.append(_evaluate_spline_safe(b_spline, point))
                                C_vals.append(_evaluate_spline_safe(c_spline, point))
                if(len(B_vals) != 81):
                    print(f"{color.Error}ERROR:{color.END} Expected 81 evaluation points for bin ({q2y_bin}, {zpt_bin}), got {len(B_vals)}")
                    n_skip += 1
                    critical_failure = True
                    break
                B_arr = np.asarray(B_vals, dtype=float)
                C_arr = np.asarray(C_vals, dtype=float)
                if(not (np.all(np.isfinite(B_arr)) and np.all(np.isfinite(C_arr)))):
                    print(f"{color.Error}ERROR:{color.END} Non-finite spline values among 81-point sample for bin ({q2y_bin}, {zpt_bin})")
                    n_skip += 1
                    critical_failure = True
                    break
                B_init = float(np.mean(B_arr))
                C_init = float(np.mean(C_arr))
                B_std  = float(np.std(B_arr, ddof=0))
                C_std  = float(np.std(C_arr, ddof=0))
                B_min  = B_init - (std_multiple * B_std)
                B_max  = B_init + (std_multiple * B_std)
                C_min  = C_init - (std_multiple * C_std)
                C_max  = C_init + (std_multiple * C_std)
        except Exception as ee:
            print(f"{color.Error}ERROR:{color.END} Spline evaluation failed for bin ({q2y_bin}, {zpt_bin}): {ee}")
            n_skip += 1
            critical_failure = True
            break

        entry = f'''    ("{q2y_bin}", "{zpt_bin}"): {{
        "B_initial": {B_init:.5f},
        "B_limits":  [{B_min:.4f}, {B_max:.4f}],
        "C_initial": {C_init:.5f},
        "C_limits":  [{C_min:.4f}, {C_max:.4f}],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    }},'''
        if(args.verbose):
            print(entry)
        dict_lines.append(entry)
        n_ok += 1

    if(critical_failure or (n_ok == 0)):
        print(f"{color.Error}ERROR:{color.END} Generation incomplete (ok={n_ok}, skipped/failed={n_skip}).")
        print(f"{color.Error}  Aborting — Phi_h_Fit_Parameters_from_Spline.py was NOT written.{color.END}")
        return

    # Build complete module content in memory, then write once
    if(use_legacy_range):
        range_mode_note = f"# Limit mode: legacy range_pct = {getattr(args, 'range_pct', 30.0)}% (+ fixed 0.15 / 0.075 offsets)"
    else:
        range_mode_note = f"# Limit mode: 81-point mean ± (std_multiple={std_multiple} × population std)"

    if(hasattr(args, "timer") and (args.timer is not None)):
        run_time_note = f"# {ansi_to_plain(args.timer.start_find(return_Q=True))}"
    else:
        run_time_note = "# Run time: unknown (args.timer not defined)"
    header_lines = [
        run_time_note,
        "# These are the per-bin fit parameters predicted by the spline fit functions (to be used to help guide the later histogram fits)",
        f"# The Kernel used for these fits was: {args.kernel}",
        f"# The Smoothing Parameter used for the  Cos(Phi) Moments was: {args.smoothing_factor_B}",
        f"# The Smoothing Parameter used for the Cos(2Phi) Moments was: {args.smoothing_factor_C}",
        f"# Parameters were fit for these corrections: '{args.fit_set}'",
        f"# The original fits were saved here: '{args.json_file}'",
        f"# The output files containing the spline fits should be named: '{args.output_prefix}_{args.dimension_mode}_{args.fit_set}_Fit_Par_*.{{npz,pkl}}'",
        f"# Dimension mode: {args.dimension_mode}",
        range_mode_note,
        f"# Auto-generated by Create_Continuous_4D_Moments_From_JSON.py — do not edit Phi_h_Fit_Parameters_Initialize.py",
        "",
    ]
    module_body = "\n".join(header_lines)
    module_body += "special_fit_parameters_set = {\n"
    module_body += TRUSTED_AND_SECTORS_BLOCK
    module_body += "\n"
    module_body += "\n".join(dict_lines)
    module_body += "\n}\n"

    out_name = "Phi_h_Fit_Parameters_from_Spline.py"
    with open(out_name, "w") as f:
        f.write(module_body)
    print(f"\n{color.GREEN}Wrote complete importable module: {out_name}{color.END}")
    print(f"{color.GREEN}  Entries: {n_ok} spline bin pairs + Trusted/Sectors blocks{color.END}")

    # Optional: also save the legacy Fit_Parameter_Initials txt if --save_init is set
    if(getattr(args, "save_init", None) is not None):
        filename = args.save_init
        if(not filename.endswith(".txt")):
            filename += ".txt"
        with open(filename, "w") as f:
            f.write("\n".join(header_lines))
            f.write("Fit_Parameter_Initials = {\n")
            f.write("\n".join(dict_lines))
            f.write("\n}\n")
        print(f"{color.GREEN}Optional dictionary also saved to: {filename}{color.END}")

    print(f"\n{color.GREEN}Ready to import as special_fit_parameters_set from {out_name}{color.END}")


# ------------------------------------------------------------
# Generate C++ code for RDataFrame
# ------------------------------------------------------------
class ExpRBFWrapper:
    # Wrap an RBF fit on log(A) so evaluation returns Amplitude = exp(rbf(x)).
    def __init__(self, rbf):
        self.rbf = rbf
    def __call__(self, x):
        return np.exp(np.asarray(self.rbf(x), dtype=float))


def generate_spline_code(args):
    args.Compute_SplineWeight_File = f"{args.output_prefix}_{args.dimension_mode}_{args.fit_set}_Compute_SplineWeight.txt"
    print(f"\n{color.BOLD}=== Generating complete C++ Spline Evaluator ({args.Compute_SplineWeight_File}) ==={color.END}\n")
    files = {}
    for y_par in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
        npz_file = f"{args.output_prefix}_{args.dimension_mode}_{args.fit_set}_{y_par}.npz"
        if(not os.path.isfile(npz_file)):
            Crash_Report(args, crash_message=f"\n{color.Error}ERROR: Missing {npz_file}{color.END}\n", continue_run=True)
            return
        files[y_par] = npz_file
    # Load the three .npz files
    data = {}
    for y_par, fname in files.items():
        d = np.load(fname, allow_pickle=True)
        data[y_par] = {
            "points": d["points"].tolist(),
            "values": d["values"].tolist(),
            "kernel": str(d["kernel"]),
            "smoothing": float(d["effective_smoothing"]),
            "epsilon": float(d.get("epsilon", 1.0)),
            "dimension_mode": str(d["dimension_mode"]),
            "log_space": bool(d["log_space"]) if("log_space" in d.files) else False,
        }
    # Start building the C++ code
    cpp_code = f"""// Auto-generated by Create_Continuous_4D_Moments_From_JSON.py
// Dimension mode: {args.dimension_mode}
// Fit set: {args.fit_set}
// Generated on {__import__('datetime').datetime.now().strftime('%m-%d-%Y %H:%M:%S')}
#include <vector>
#include <cmath>
#include <string>
double rbf_kernel(double r, std::string kernel, double epsilon) {{
    if (kernel == "thin_plate_spline") return r*r * std::log(r + 1e-12);
    if (kernel == "linear") return r;
    if (kernel == "multiquadric") return std::sqrt(1.0 + epsilon*epsilon*r*r);
    if (kernel == "gaussian") return std::exp(-epsilon*epsilon*r*r);
    if (kernel == "cubic") return r*r*r;
    return r; // fallback
}}
"""
    # Add data + evaluator for each parameter
    for y_par in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
        d = data[y_par]
        n = len(d["points"])
        dim = len(d["points"][0])
        cpp_code += f"\n// --- {y_par} data ---\n"
        cpp_code += f"const int n_{y_par.lower()} = {n};\n"
        cpp_code += f"const double centers_{y_par.lower()}[{n}][{dim}] = {{\n"
        for p in d["points"]:
            cpp_code += "    {" + ", ".join(f"{x:.8e}" for x in p) + "},\n"
        cpp_code += "};\n"
        cpp_code += f"const double values_{y_par.lower()}[{n}] = {{{', '.join(f'{v:.8e}' for v in d['values'])}}};\n"
        cpp_code += f"const std::string kernel_{y_par.lower()} = \"{d['kernel']}\";\n"
        cpp_code += f"const double epsilon_{y_par.lower()} = {d['epsilon']:.8e};\n"
        cpp_code += f"const std::string dim_mode_{y_par.lower()} = \"{d['dimension_mode']}\";\n\n"
        log_space = bool(d.get("log_space", False))
        cpp_code += f"const bool log_space_{y_par.lower()} = {'true' if(log_space) else 'false'};\n"
        # Dimension-aware evaluator
        ret_expr = f"std::exp(sum)" if(log_space) else "sum"
        cpp_code += f"""
double ComputeSpline{y_par[-1]}(double Q2, double xB, double y, double z, double pT) {{
    double sum = 0.0;
    double r;
    double pt[5];
    if (dim_mode_{y_par.lower()} == "4D") {{ pt[0] = Q2; pt[1] = y; pt[2] = z; pt[3] = pT; pt[4] = 0.0; }}
    else if (dim_mode_{y_par.lower()} == "4D_xB") {{ pt[0] = xB; pt[1] = y; pt[2] = z; pt[3] = pT; pt[4] = 0.0; }}
    else {{ pt[0] = Q2; pt[1] = xB; pt[2] = y; pt[3] = z; pt[4] = pT; }} // 5D
    for(int i = 0; i < n_{y_par.lower()}; ++i) {{
        r = 0.0;
        for(int j = 0; j < {dim}; ++j) {{
            double diff = pt[j] - centers_{y_par.lower()}[i][j];
            r += diff * diff;
        }}
        r = std::sqrt(r);
        sum += values_{y_par.lower()}[i] * rbf_kernel(r, kernel_{y_par.lower()}, epsilon_{y_par.lower()});
    }}
    return {ret_expr};
}}
"""
    # Main weight function
    cpp_code += """
double ComputeSplineWeight(double Q2, double xB, double y, double z, double pT, double phi_h) {
    double phi_rad = phi_h * TMath::DegToRad();
    double A = ComputeSplineA(Q2, xB, y, z, pT);
    double B = ComputeSplineB(Q2, xB, y, z, pT);
    double C = ComputeSplineC(Q2, xB, y, z, pT);
    return A * (1.0 + B * std::cos(phi_rad) + C * std::cos(2.0 * phi_rad));
}
"""
    with open(args.Compute_SplineWeight_File, "w") as f:
        f.write(cpp_code)
    Update_Email(args, update_message=f"\n{color.BGREEN}Successfully generated complete C++ file: {color.BCYAN}{args.Compute_SplineWeight_File}{color.END}\n", verbose_override=True, no_time=True)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    print(f"\n{color.BBLUE}=== Building tunable spline functions ({args.dimension_mode} mode) ==={color.END}\n")
    json_obj = load_json(args)
    if(args.list_fit_sets):
        print("Fit sets in JSON:")
        for kk in list_fit_sets(json_obj):
            print(f"  {kk}")
        return
    fit_set = str(args.fit_set).strip()
    if(not fit_set):
        fit_set = select_default_fit_set(json_obj)
        if(not fit_set):
            Crash_Report(args, crash_message=f"{color.Error}ERROR: No valid fit_set found.{color.END}", continue_run=False)
        if((args.verbose) or (args.email)):
            Update_Email(args, update_message=f"{color.BYELLOW}[INFO] Auto-selected fit_set = '{fit_set}'{color.END}", verbose_override=False, no_time=True)
    if(fit_set not in json_obj):
        Crash_Report(args, crash_message=f"{color.Error}ERROR: fit_set '{fit_set}' not found in JSON.{color.END}", continue_run=False)
    fit_dict = json_obj[fit_set]
    info_map = build_info_map(fit_dict)
    if((args.verbose) or (args.email)):
        Update_Email(args, update_message=f"{color.CYAN}[INFO] Using fit_set: {fit_set}\n[INFO] Total measurement points: {len(fit_dict)}\n[INFO] Dimension mode: {args.dimension_mode}{color.END}", verbose_override=False, no_time=True)
    y_pars = ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]
    if(not args.generate_spline_code_only):
        for y_par in y_pars:
            # points, values, stds = build_data(fit_dict, info_map, y_par, args.err_suffix, args.dimension_mode)
            points, values, stds = build_data(fit_dict, info_map, y_par, args)
            if(len(points) == 0):
                Update_Email(args, update_message=f"{color.Error}[WARNING] No valid data points found for {y_par}{color.END}", verbose_override=True, no_time=True)
                continue
            # # === PER-POINT UNCERTAINTY WEIGHTING ===
            # alpha = stds ** 2
            # smoothing = args.smoothing_factor * np.mean(alpha)
            smoothing = args.smoothing_factor
            if("Fit_Par_A" in y_par):
                # smoothing = max([smoothing*20, 0.005]) # Done to test unique smoothing parameters for the Amplitude measurements
                # # smoothing = 0
                # # args.smoothing_factor   = smoothing
                if(getattr(args, "smoothing_factor_A", None) is not None):
                    smoothing = args.smoothing_factor_A
                else:
                    args.smoothing_factor_A = smoothing
            elif("Fit_Par_B" in y_par):
                # smoothing = min([smoothing*20, 0.00005])
                # args.smoothing_factor_B = smoothing
                if(getattr(args, "smoothing_factor_B", None) is not None):
                    smoothing = args.smoothing_factor_B
                else:
                    args.smoothing_factor_B = smoothing
            elif("Fit_Par_C" in y_par):
                # smoothing = min([smoothing*20, 0.00005])
                # args.smoothing_factor_C = smoothing
                if(getattr(args, "smoothing_factor_C", None) is not None):
                    smoothing = args.smoothing_factor_C
                else:
                    args.smoothing_factor_C = smoothing
            if(args.test):
                print(f"{color.CYAN}{y_par}: {len(points)} points | median err = {np.median(stds):.5f} | effective smoothing = {smoothing:.2e}{color.END}")
                continue
            kernel_par = args.kernel if(("Fit_Par_A" not in y_par) or (getattr(args, "kernel_A", None) is None)) else args.kernel_A
            use_log_A = bool(getattr(args, "log_A", False)) and ("Fit_Par_A" in y_par)
            fit_values = values
            if(use_log_A):
                if(np.any(values <= 0)):
                    n_bad = int(np.sum(values <= 0))
                    Update_Email(args, update_message=f"{color.Error}[WARNING] {n_bad} non-positive Fit_Par_A values; clipping to 1e-30 before log_A fit{color.END}", verbose_override=True, no_time=True)
                fit_values = np.log(np.clip(values, 1e-30, None))
            rbf = RBFInterpolator(points, fit_values, kernel=kernel_par, smoothing=smoothing, epsilon=args.epsilon)
            config = {"kernel": kernel_par,
                    "smoothing_factor": args.smoothing_factor,
                    "effective_smoothing": smoothing,
                    "epsilon": args.epsilon,
                    "fit_set": fit_set,
                    "y_par": y_par,
                    "n_points": len(points),
                    "per_point_weighting": True,
                    "dimension_mode": args.dimension_mode,
                    "log_space": use_log_A,
                    }
            mode_str = args.dimension_mode
            pkl_file = f"{args.output_prefix}_{mode_str}_{fit_set}_{y_par}.pkl"
            with open(pkl_file, "wb") as f:
                # Store the raw RBF (trained on fit_values). If log_space, loaders must exp() on evaluate.
                # Keep original linear-space "values" for diagnostics.
                pickle.dump({"rbf": rbf, "config": config, "points": points, "values": values, "fit_values": fit_values}, f)
            npz_file = f"{args.output_prefix}_{mode_str}_{fit_set}_{y_par}.npz"
            # C++ export uses the values the RBF was trained on (log(A) when --log_A)
            np.savez(npz_file, **config, points=points, values=fit_values)
            log_tag = " [log_A]" if(use_log_A) else ""
            Update_Email(args, update_message=f"{color.GREEN}SAVED {y_par}{log_tag} → {pkl_file} (Python) + {npz_file} (C++){color.END}", verbose_override=True, no_time=True)
        if(getattr(args, "generate_init", False)):
            generate_initial_dict(info_map, args)
        Update_Email(args, update_message=f"\n{color.BBLUE}All spline functions built ({args.dimension_mode} mode) with per-point uncertainty weighting.{color.END}\n", verbose_override=True, no_time=not getattr(args, "generate_spline_code", False))
    if(getattr(args, "generate_spline_code", False)):
        generate_spline_code(args)
    Construct_Email(args, Crashed=False, Warning=False)

if(__name__ == "__main__"):
    main()
    