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

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, color_bg, RuntimeTimer
from Binning_Dictionaries import Full_Bin_Definition_Array
sys.path.remove(script_dir)

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    p = argparse.ArgumentParser(description="Create_Continuous_4D_Moments_From_JSON.py: Build tunable 4D continuous spline functions from the same JSON files used in 'Full_Moment_Plots_Creation_From_JSON.py'.", formatter_class=RawDefaultsHelpFormatter)

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
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Appended_in_Parallel_Fixed_RC_Factor_Normalization_Full.json",
                   help="Input JSON file produced by your fit workflow.\n")
    
    p.add_argument("-L", "--list_fit_sets",
                   action="store_true",
                   help="List available fit-set keys in the JSON and exit.\n")
    p.add_argument("-f", "--fit_set",
                   default="Fit_Pars_from_3D_BC_RC_Bayesian",
                   help="Top-level JSON key to use.\n")
    
    p.add_argument("-err", "--err_suffix",
                   default="_ERR",
                   help="Error key suffix (Fit_Par_B + _ERR -> Fit_Par_B_ERR).\n")
    
    p.add_argument("-o", "--output_prefix",
                   default="Continuous_Moments",
                   help="Prefix for output files (e.g. Continuous_Moments_Fit_Pars_from_3D_Bayesian_Fit_Par_B.pkl).\n")

    # === TUNING KNOBS ===
    p.add_argument("-s", "--smoothing_factor",
                   type=float,
                   default=1.0,
                   help="Multiplier on median uncertainty for smoothing (0 = exact interpolation, 1 = default, >1 = smoother).\n")
    p.add_argument("-k", "--kernel",
                   choices=["thin_plate_spline", "cubic", "multiquadric", "inverse", "gaussian", "linear"],
                   default="thin_plate_spline",
                   help="Kernel type for the RBF spline (thin_plate_spline is the direct 4D cubic analogue).\n")
    p.add_argument("-eps", "--epsilon",
                   type=float,
                   default=None,
                   help="Epsilon parameter (scale) for the kernel. Leave blank for auto-tuning.\n")
    
    p.add_argument("-t", "--test",
                   action="store_true",
                   help="Only parse JSON and print summary; do not build or save anything.\n")

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


# ------------------------------------------------------------
# Build 4D data points (exact same extraction used in the mosaic plots)
# ------------------------------------------------------------
def build_4d_data(fit_dict, info_map, y_par, err_suffix):
    points = []
    values = []
    stds = []
    for key_str, entry in fit_dict.items():
        if((y_par not in entry) or (f"{y_par}{err_suffix}" not in entry)):
            continue
        if(key_str not in info_map):
            continue
        inf = info_map[key_str]
        Q2 = inf["Q2range"][0]
        y_val = inf["y_range"][0]
        z_val = inf["z_range"][0]
        Pt_val = inf["pTrange"][0]
        val = float(entry[y_par])
        err = float(entry[f"{y_par}{err_suffix}"])
        points.append([Q2, y_val, z_val, Pt_val])
        values.append(val)
        stds.append(err)
    return (np.array(points, dtype=float), np.array(values, dtype=float), np.array(stds, dtype=float))

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    print(f"\n{color.BBLUE}=== Building tunable 4D spline functions ==={color.END}\n")
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
        Update_Email(args, update_message=f"{color.CYAN}[INFO] Using fit_set: {fit_set}\n[INFO] Total measurement points: {len(fit_dict)}{color.END}", verbose_override=False, no_time=True)

    y_pars = ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]

    for y_par in y_pars:
        points, values, stds = build_4d_data(fit_dict, info_map, y_par, args.err_suffix)
        if(len(points) == 0):
            Update_Email(args, update_message=f"{color.Error}[WARNING] No valid data points found for {y_par}{color.END}", verbose_override=True, no_time=True)
            continue
        median_err = np.median(stds) if(len(stds) > 0) else 1.0
        smoothing = args.smoothing_factor * (median_err ** 2)
        if(args.test):
            print(f"{color.CYAN}{y_par}: {len(points)} points | median err = {median_err:.5f} | smoothing = {smoothing:.2e}{color.END}")
            continue
        # Build the spline with your chosen configuration
        rbf = RBFInterpolator(points, values, kernel=args.kernel, smoothing=smoothing, epsilon=args.epsilon)
        config = {"kernel": args.kernel,
                  "smoothing_factor": args.smoothing_factor,
                  "smoothing": smoothing,
                  "epsilon": args.epsilon,
                  "fit_set": fit_set,
                  "y_par": y_par,
                  "n_points": len(points)
                  }

        # 1. Python-friendly pickle (ready-to-use spline)
        pkl_file = f"{args.output_prefix}_{fit_set}_{y_par}.pkl"
        with(open(pkl_file, "wb") as f):
            pickle.dump({"rbf": rbf, "config": config, "points": points, "values": values}, f)

        # 2. C++-friendly npz (points + full config for later reconstruction)
        npz_file = f"{args.output_prefix}_{fit_set}_{y_par}.npz"
        np.savez(npz_file, **config, points=points, values=values)

        Update_Email(args, update_message=f"{color.GREEN}SAVED {y_par} → {pkl_file} (Python) + {npz_file} (C++){color.END}", verbose_override=True, no_time=True)

    Update_Email(args, update_message=f"\n{color.BBLUE}All 4D spline functions built and saved with full configuration.{color.END}\n", verbose_override=True, no_time=True)
    Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Files")

if(__name__ == "__main__"):
    main()
    