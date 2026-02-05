#!/usr/bin/env python3
import sys
import argparse

import ROOT, numpy, re
import traceback
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Creates Fits of Modulation Parameters as functions of the kinematic variables.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-t', '--test',
                        action='store_true', 
                        help='Run as test.')
    
    parser.add_argument('-q2y', '-Q2y', '--Q2_y_Bin',
                        default=-1,
                        type=int,
                        choices=[-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                        help="Selected Q2-y Bin to run. Use '-1' to run all bins.")
    
    # parser.add_argument('-zpt', '-zpT', '--z_pT_Bin',
    #                     default=-1,
    #                     type=int,
    #                     help="Selected z-pT Bin (for any given Q2-y Bin) to run. Use '-1' to run all bins. Does not automatically reject incompatible combinations of the '--Q2_y_Bin' and '--z_pT_Bin' options.")
    # parser.add_argument("-g-Q2", "--Q2_group",
    #                     # default=1,
    #                     type=int,
    #                     help="Group of Q2-y Bins used for plotting vs Q2 (Max group = 5)")
    # parser.add_argument("-g-y",   "--y_group",
    #                     # default=1,
    #                     type=int,
    #                     help="Group of Q2-y Bins used for plotting vs y (Max group = 4)")
    # parser.add_argument("-g-pT", "--pT_group",
    #                     # default=1,
    #                     type=int,
    #                     help="Group of z-pT Bins used for plotting vs pT (Differs based on chosen Q2_y_Bin — Max group = 7)")
    parser.add_argument("-g-z", "--z_group",
                        # default=1,
                        type=int,
                        help="Selects a single group of z-pT Bins used for plotting vs z (Differs based on chosen Q2_y_Bin — Max group = 7 — Runs all groups by default)")

    parser.add_argument("-fp", "-par", "--fit_parameter",
                        type=str,
                        choices=["B", "C"],
                        help="Selects which fit parameter to plot (defaults to both).")
    
    parser.add_argument('-f', '--file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json",
                        type=str, 
                        help="Path to JSON file that contains the list of parameters that are to be fit.")
    
    parser.add_argument('-sf', '-ff', '--save_format',
                        default=".png",
                        type=str,
                        choices=[".png", ".pdf"],
                        help="Selects the image file format of the images that would be saved by this script when running.")

    parser.add_argument('-v', '--verbose',
                        action='store_true', 
                        help='Print more information while running.')
    
    return parser.parse_args()



script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
def silence_root_import():
    # Flush Python’s buffers so dup2 doesn’t duplicate partial output
    sys.stdout.flush()
    sys.stderr.flush()
    # Save original file descriptors
    old_stdout = os.dup(1)
    old_stderr = os.dup(2)
    try:
        # Redirect stdout and stderr to /dev/null at the OS level
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        os.close(devnull)
        # Perform the noisy import
        import RooUnfold
    finally:
        # Restore the original file descriptors
        os.dup2(old_stdout, 1)
        os.dup2(old_stderr, 2)
        os.close(old_stdout)
        os.close(old_stderr)
silence_root_import()
sys.path.remove(script_dir)
del script_dir

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

import math
import array
import copy
import json
from pathlib import Path


import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",  # Styles
                     '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", # Colors
                     '\033[0m': "", # Reset (closes span)
                    }
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


def load_json_file(path):
    # Load a JSON file and return its contents.
    # Args:
    #     path (str | Path): Path to the JSON file.
    # Returns:
    #     dict | list: Parsed JSON data.
    # Raises:
    #     FileNotFoundError: If the path does not exist.
    #     ValueError: If the path is not a file.
    #     RuntimeError: If JSON is invalid.
    file_path = Path(path)
    if(not file_path.exists()):  # Check existence
        raise FileNotFoundError(f"Path does not exist: {file_path}")
    if(not file_path.is_file()): # Check that it is a file
        raise ValueError(f"Path is not a file: {file_path}")
    try:                         # Load JSON
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON format in {file_path}: {e}") from e




# =========================
# Binning Dictionary
# =========================

from Binning_Dictionaries import Full_Bin_Definition_Array, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D

# =========================
# Bin Conversion Helpers
# =========================

def get_bin_centers(var, Q2_y_num, z_pT_num=None):
    if(var in ["Q2_y", "Q2", "y"]):
        Q2_y_Ranges = Full_Bin_Definition_Array.get(f'Q2-y={Q2_y_num}, Q2-y', None)
        if(Q2_y_Ranges):
            Q2_max, Q2_min, y_max, y_min = Q2_y_Ranges
            return_value = (0.5 * (Q2_max + Q2_min)) if(var in ["Q2"]) else (0.5 * (y_max + y_min)) if(var in ["y"]) else [(0.5 * (Q2_max + Q2_min)), (0.5 * (y_max + y_min))]
            return round(return_value, 5) if(not isinstance(return_value, list)) else return_value
    elif(var in ["z_pT", "z", "pT"]):
        # print(f"Getting: f'Q2-y={Q2_y_num}, z-pT={z_pT_num}'")
        z_pT_Ranges = Full_Bin_Definition_Array.get(f'Q2-y={Q2_y_num}, z-pT={z_pT_num}', None)
        # print(f"z_pT_Ranges = {z_pT_Ranges}")
        if(z_pT_Ranges):
            z_max, z_min, pT_max, pT_min = z_pT_Ranges
            return_value = (0.5 * (pT_max + pT_min)) if(var in ["pT"]) else (0.5 * (z_max + z_min)) if(var in ["z"]) else [(0.5 * (pT_max + pT_min)), (0.5 * (z_max + z_min))]
            return round(return_value, 5) if(not isinstance(return_value, list)) else return_value
    return [None, None] if(var in ["Q2_y", "z_pT"]) else None


def get_bins_in_row_or_column(cols, rows, target, axis):
    # Returns a list of bin labels in a given row or column.
    # Parameters:
    #     rows (int): Number of rows in the grid.
    #     cols (int): Number of columns in the grid.
    #     target (int): Target row or column number (1-indexed).
    #     axis (str): Either 'pT' or 'z'.
    # Returns:
    #     List[int]: List of bin labels in the specified row or column.
    if(axis not in ('pT', 'z')):
        raise ValueError("Axis must be either 'pT' (for rows) or 'z' (for columns)")
    if(axis in ['pT', 'row']):
        if((target < 1) or (target > rows)):
            print(f"{color.Error}'target' = {target} while 'rows' = {rows} so ((target < 1) or (target > rows)){color.END}")
            raise ValueError("pT (row) index out of range.")
        start = (target - 1) * cols + 1
        return list(range(start, start + cols))
    else:  # axis == 'column'
        if((target < 1) or (target > cols)):
            raise ValueError("z (column) index out of range.")
        z_return = [target + (r * cols) for r in range(rows)]
        z_return.sort(reverse=True) # z values get smaller with increasing bin numbers in my scheme
        return z_return

def Q2_y_z_pT_Bin_rows_function(var, row_num, Q2_y_Bin=None, Output_Q="Centers", verbose=False):
    bin_num_list = None
    if(var    in ["Q2", "y"]):
        bin_num_list = Q2_y_Bin_rows_Array[f"{var}-row-{row_num}"]
    elif((var in ["pT", "z"]) and Q2_y_Bin):
        col_total, rows_total = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_y_Bin, Integration_Bins_Q=False)
        bin_num_list = get_bins_in_row_or_column(rows_total, col_total, row_num, var)
        if(verbose):
            print(f"Bin List of {var} in group {row_num}: {color.BOLD}{bin_num_list}{color.END} (Q2_y_Bin = {Q2_y_Bin})")
    if(Output_Q in ["Centers"]):
        bin_center_list = []
        for center_bin in bin_num_list:
            if(var    in ["Q2", "y"]):
                if(get_bin_centers(var, center_bin, z_pT_num=None)):
                    bin_center_list.append(get_bin_centers(var, center_bin, z_pT_num=None))
            elif((var in ["pT", "z"]) and Q2_y_Bin):
                if(get_bin_centers(var, Q2_y_Bin,   z_pT_num=center_bin)):
                    bin_center_list.append(get_bin_centers(var, Q2_y_Bin,   z_pT_num=center_bin))
        return bin_center_list
    else:
        return bin_num_list
    return None


if(__name__ == "__main__"):
    args = parse_args()
    timer = RuntimeTimer()
    timer.start()

    List_of_Fit_Parameters = load_json_file(args.file)
    print(f"{color.BBLUE}Loaded Parameters from: {color.BPINK}{str(args.file).split('/')[-1]}{color.END}")
    # if(args.verbose):
    #     print(f"\n{color.BOLD}The contents of this file are as follows:{color.END}")
    #     for ii in List_of_Fit_Parameters:
    #         print(f"\t{color.BOLD}{ii}: {color.END}{List_of_Fit_Parameters[ii]}")
    #     print(f"\nTotal Number of Entries = {len(List_of_Fit_Parameters)}")

    Param_list    = ["B", "C"]   if(args.fit_parameter  is None) else [args.fit_parameter]
    Q2_y_range    = range(1, 18) if(args.Q2_y_Bin in [None, -1]) else [args.Q2_y_Bin]
    z_group_range = range(1, 8)  if(args.z_group  in [None, -1]) else [args.z_group]
    for fit_par         in Param_list:
        for Q2_y_bin    in Q2_y_range:
            print(f"Q2_y_bin = {Q2_y_bin}")
            for z_group in z_group_range:
                try:
                    bin_range = Q2_y_z_pT_Bin_rows_function("z", z_group, Q2_y_Bin=Q2_y_bin, Output_Q="Bins")
                    x_range   = Q2_y_z_pT_Bin_rows_function("z", z_group, Q2_y_Bin=Q2_y_bin, Output_Q="Centers")
                    print(f"\tz_group = {z_group}")
                except ValueError as e:
                    msg = str(e).lower()
                    if("out of range" in msg):
                        # print(f"\t\tSkipping invalid z_group={z_group} for Q2_y_bin={Q2_y_bin} ({e})")
                        break
                    raise
                # print(f"\t\tbin_range = {bin_range}")
                # print(f"\t\tx_range   = {x_range}")
                for idx, bin_num in enumerate(bin_range):
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_bin, Z_PT_BIN=bin_num, BINNING_METHOD="Y_bin")):
                        continue
                    Moment_To_Plot = List_of_Fit_Parameters.get(f"{fit_par}_{Q2_y_bin}_{bin_num}",    None)
                    if(Moment_To_Plot is None):
                        print(f"\t\t{color.Error}Missing Parameter '{fit_par}' for Bin ({Q2_y_bin}-{bin_num}){color.END}\n")
                        continue
                    Err__of_Moment = List_of_Fit_Parameters.get(f"{fit_par}_ERR_{Q2_y_bin}_{bin_num}", 0.0)
                    print(f"\t\t{color.BOLD}{color.UNDERLINE}Par {fit_par}{color.END_B} of Bin {f'({Q2_y_bin}-{bin_num})':>7s}:{color.END} {Moment_To_Plot} ± {Err__of_Moment}")
                    
    
    # plot_var = "z"
    # numslice = 1
    # bin_range = Q2_y_z_pT_Bin_rows_function(plot_var, numslice+1, Q2_y_Bin=args.Q2_y_Bin, Output_Q="Bins")
    # x_range   = Q2_y_z_pT_Bin_rows_function(plot_var, numslice+1, Q2_y_Bin=args.Q2_y_Bin, Output_Q="Centers")
    # print(f"bin_range = {bin_range}")
    # print(f"x_range   = {x_range}")
    
    print("\nDone Running 'Creation_of_Parameter_Fits.py'\n")
    timer.stop()
    

