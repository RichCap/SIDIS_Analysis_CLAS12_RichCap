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

    parser.add_argument("-ft", "--fit_type",
                        default='lin',
                        choices=['lin', 'quad'],
                        help="Selects the (initial) fit function type: 'lin' (linear) or 'quad' (quadratic).")
    
    parser.add_argument('-f', '--file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json",
                        type=str, 
                        help="Path to JSON file that contains the list of parameters that are to be fit.")
    
    parser.add_argument('-sf', '-ff', '--save_format',
                        default=".png",
                        type=str,
                        choices=[".png", ".pdf"],
                        help="Selects the image file format of the images that would be saved by this script when running.")

    parser.add_argument('-title', '-at', '--title',
                        type=str,
                        help="Optional string to add to plot titles.")
    parser.add_argument('-n', '-sn', '--save_name',
                        type=str,
                        help="Optional string to add to the file names when saving.")

    parser.add_argument('-v', '--verbose',
                        action='store_true', 
                        help='Print more information while running.')

    parser.add_argument('-o', '--fit_out',
                        default="Kinematic_FitEquations_Of_Modulations.json",
                        type=str,
                        help="Optional output JSON file to save fitted equations/coefficients for reuse in later scripts.")

    parser.add_argument("-ftpT", '-pt_fit_type', '--pT_fit_type',
                        default='quad',
                        choices=['lin', 'quad'],
                        help="Fit type used when fitting the z-fit coefficients as functions of pT.")

    
    return parser.parse_args()



script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
sys.path.remove(script_dir)
del script_dir

def silence_root_import():
    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
    sys.path.append(script_dir)
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

def get_bin_centers(var, Q2_y_num, z_pT_num=None, Get_Range_str=False):
    if(var in ["Q2_y", "Q2", "y"]):
        Q2_y_Ranges = Full_Bin_Definition_Array.get(f'Q2-y={Q2_y_num}, Q2-y', None)
        if(Q2_y_Ranges):
            Q2_max, Q2_min, y_max, y_min = Q2_y_Ranges
            if(Get_Range_str):
                return_value = f"{Q2_min} < Q2 < {Q2_max}" if(var in ["Q2"]) else f"{y_min} < y < {y_max}" if(var in ["y"]) else f"#splitline{{{Q2_min} < Q^{{2}} < {Q2_max}}}{{{y_min} < y < {y_max}}}"
                return return_value
            else:
                return_value = (0.5 * (Q2_max + Q2_min)) if(var in ["Q2"]) else (0.5 * (y_max + y_min)) if(var in ["y"]) else [(0.5 * (Q2_max + Q2_min)), (0.5 * (y_max + y_min))]
                return round(return_value, 5) if(not isinstance(return_value, list)) else return_value
    elif(var in ["z_pT", "z", "pT"]):
        # print(f"Getting: f'Q2-y={Q2_y_num}, z-pT={z_pT_num}'")
        z_pT_Ranges = Full_Bin_Definition_Array.get(f'Q2-y={Q2_y_num}, z-pT={z_pT_num}', None)
        # print(f"z_pT_Ranges = {z_pT_Ranges}")
        if(z_pT_Ranges):
            z_max, z_min, pT_max, pT_min = z_pT_Ranges
            if(Get_Range_str):
                return_value = f"{z_min} < z < {z_max}" if(var in ["z"]) else f"{pT_min} < pT < {pT_max}" if(var in ["pT"]) else f"#splitline{{{z_min} < z < {z_max}}}{{{pT_min} < P_{{T}} < {pT_max}}}"
                return return_value
            else:
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



# =========================
# Saving Fit Helpers
# =========================

def tf1_to_dict(fit_fn, x_min=None, x_max=None, fit_type=None):
    if(fit_fn is None):
        return None

    npar = int(fit_fn.GetNpar())

    par_vals = []
    par_errs = []
    for ii in range(npar):
        par_vals.append(float(fit_fn.GetParameter(ii)))
        par_errs.append(float(fit_fn.GetParError(ii)))

    out = {}
    out["fit_type"]   = str(fit_type) if(fit_type is not None) else None
    out["formula"]    = str(fit_fn.GetTitle()) if(fit_fn.GetTitle() is not None) else None
    out["npar"]       = int(npar)
    out["par"]        = par_vals
    out["par_err"]    = par_errs
    out["chi2"]       = float(fit_fn.GetChisquare())
    out["ndf"]        = int(fit_fn.GetNDF())
    out["x_min"]      = float(x_min) if(x_min is not None) else None
    out["x_max"]      = float(x_max) if(x_max is not None) else None

    # Convenience equation strings for downstream scripts
    # (These are redundant with par[] but handy.)
    if(npar == 2):
        out["equation"] = "p0 + p1*x"
        out["par_name"] = ["p0", "p1"]
    elif(npar == 3):
        out["equation"] = "p0 + p1*x + p2*x^2"
        out["par_name"] = ["p0", "p1", "p2"]
    else:
        out["equation"] = None
        out["par_name"] = [f"p{ii}" for ii in range(npar)]

    return out


def safe_write_json(path_out, payload):
    if((path_out is None) or (payload is None)):
        raise ValueError("safe_write_json: was passed a None argument.")
    with open(path_out, "w", encoding="utf-8") as out_f:
        json.dump(payload, out_f, indent=2, sort_keys=True)

# =========================
# Plotting Helpers
# =========================

def make_tgraph_errors(x_vals, y_vals, y_errs, graph_name="", graph_title=""):
    if((x_vals is None) or (y_vals is None) or (y_errs is None)):
        return None

    npts = len(x_vals)
    if((npts < 1) or (len(y_vals) != npts) or (len(y_errs) != npts)):
        return None

    x_arr  = array.array('d', [float(xx) for xx in x_vals])
    y_arr  = array.array('d', [float(yy) for yy in y_vals])
    ex_arr = array.array('d', [0.0 for _ in range(npts)])
    ey_arr = array.array('d', [float(ee) for ee in y_errs])

    graph = ROOT.TGraphErrors(npts, x_arr, y_arr, ex_arr, ey_arr)
    if(graph_name):
        graph.SetName(graph_name)
    if(graph_title):
        graph.SetTitle(graph_title)

    return graph


group_color_map = {
    "1": ROOT.kRed,
    "2": ROOT.kBlue,
    "3": ROOT.kMagenta,
    "4": ROOT.kGreen,
    "5": 28,
    "6": 29,
    "7": 41,
}
def style_graph(graph, Parameter="B", Group_Num=1):
    if(graph is None):
        return
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    graph.SetLineWidth(2)

    graph.SetMarkerColor(group_color_map[str(Group_Num)])
    graph.SetLineColor(group_color_map[str(Group_Num)])
    
    if(Parameter in ["B"]):
        graph.GetYaxis().SetRangeUser(-1,    0.2)
    else:
        graph.GetYaxis().SetRangeUser(-0.45, 0.25)
        


def fit_graph(graph, fit_type, fit_name, x_min, x_max):
    if(graph is None):
        return None, None

    if(fit_type == "lin"):
        fit_formula = "[0] + [1]*x"
    elif(fit_type == "quad"):
        fit_formula = "[0] + [1]*x + [2]*x*x"
    else:
        raise ValueError(f"Unknown fit_type='{fit_type}' (expected 'lin' or 'quad').")

    if((x_min is None) or (x_max is None)):
        return None, None

    fit_fn = ROOT.TF1(fit_name, fit_formula, float(x_min), float(x_max))
    fit_fn.SetLineWidth(2)
    fit_fn.SetLineColorAlpha(graph.GetLineColor(), 0.75)
    fit_fn.SetLineStyle(3)

    # Quiet + return fit result + enforce range
    fit_result = graph.Fit(fit_fn, "QSR")

    return fit_fn, fit_result


def save_canvas(canvas, save_name, save_format):
    if((canvas is None) or (save_name is None) or (save_format is None)):
        raise ValueError("save_canvas: was passed a None argument.")
    save_out = str(save_name)
    if(not save_out.endswith(save_format)):
        save_out += save_format
    print(f"\n{color.BBLUE}Saving Image As: {color.BPINK}{save_out}{color.END}")
    canvas.SaveAs(save_out)


def add_fit_statbox(graph, canvas, Group_Num=1, x1=0.55, y1=0.1, x2=0.9, y2=0.32):
    # Ensure fit stats are enabled (statbox for hist stats is separate from fit stats)
    ROOT.gStyle.SetOptFit(1110)
    if((graph is None) or (canvas is None)):
        return None
    canvas.cd()
    ROOT.gPad.Update()
    stats = graph.GetListOfFunctions().FindObject("stats")
    if(stats is None):
        # Sometimes one extra update is needed for TGraph
        canvas.Update()
        ROOT.gPad.Update()
        stats = graph.GetListOfFunctions().FindObject("stats")
    if(stats is None):
        return None
    # Position in NDC coordinates
    stats.SetX1NDC(x1)
    stats.SetY1NDC(y1)
    stats.SetX2NDC(x2)
    stats.SetY2NDC(y2)
    # Make it readable / consistent
    stats.SetFillStyle(0)
    stats.SetBorderSize(1)
    stats.SetTextFont(42)
    stats.SetTextSize(0.030)
    # # Match the group color (optional but useful)
    # stats.SetTextColor(group_color_map[str(Group_Num)])
    canvas.Modified()
    canvas.Update()
    return stats


def make_and_save_parameter_plot(fit_par, Q2_y_bin, z_group, bin_range, x_vals, y_vals, y_errs, args, keep_canvases=None, keep_graphs=None, keep_fits=None):
    # Make one plot per (fit_par, Q2_y_bin, z_group)
    if((x_vals is None) or (len(x_vals) < 1)):
        return None, None, None, None

    par_fitT   = f"{'Cos(#phi_{h})' if('B' in fit_par) else 'Cos(2#phi_{h})'} Moments"
    fit_type   = args.fit_type if(len(x_vals) > 2) else "lin"
    for bb in bin_range:
        bins_str   = get_bin_centers(var="pT", Q2_y_num=Q2_y_bin, z_pT_num=bb, Get_Range_str=True)
        if(bins_str is not None):
            bins_str = bins_str.replace("pT", "P_{T}")
            bins_str = f"#color[{group_color_map[str(z_group)]}]{{{bins_str}}}"
            break
        else:
            bins_str = f"#color[{ROOT.kRed}]{{ERROR}}"
    plot_ttl     = f"#splitline{{{par_fitT} vs z}}{{#scale[0.5]{{Q^{{2}}-y Bin: {Q2_y_bin} #topbar {bins_str}}}}}"
    ind_bins_str = ",".join([str(bb) for bb in bin_range]) if(bin_range is not None) else ""
    plot_ttl     = f"#splitline{{{plot_ttl}}}{{#scale[0.35]{{Full List of z-P_{{T}} bins = [{ind_bins_str}]}}}}"
    # plot_ttl   = f"#splitline{{{fit_par} vs z}}{{#scale[0.5]{{Q^{{2}}-y Bin={Q2_y_bin}, z-group={z_group}, z-P_{{T}} bins=[{bins_str}]}}}}"
    if(args.title is not None):
        plot_ttl = f"#splitline{{{plot_ttl}}}{{{args.title}}}"
    g_title    = f"{plot_ttl}; z; {par_fitT}"
    graph_name = f"gr_{fit_par}_Q2y{Q2_y_bin}_zG{z_group}"

    graph = make_tgraph_errors(x_vals, y_vals, y_errs, graph_name=graph_name, graph_title=g_title)
    if(graph is None):
        return None, None, None, None

    style_graph(graph, fit_par, z_group)

    canv_name = f"can_{fit_par}_Q2y{Q2_y_bin}_zG{z_group}"
    canvas    = ROOT.TCanvas(canv_name, canv_name, 900, 700)
    canvas.cd()

    graph.Draw("APL")

    fit_fn     = None
    fit_result = None
    if(len(x_vals) >= 2):
        x_min = min(x_vals)
        x_max = max(x_vals)
        if(x_min == x_max):
            x_min -= 1e-6
            x_max += 1e-6

        fit_name = f"f_{fit_par}_Q2y{Q2_y_bin}_zG{z_group}_{fit_type}"
        fit_fn, fit_result = fit_graph(graph, fit_type, fit_name, x_min, x_max)
        if(fit_fn is not None):
            fit_fn.Draw("same")

    canvas.Update()
    add_fit_statbox(graph, canvas, Group_Num=z_group)

    if(keep_canvases is not None):
        keep_canvases.append(canvas)
    if(keep_graphs is not None):
        keep_graphs.append(graph)
    if((keep_fits is not None) and (fit_fn is not None)):
        keep_fits.append(fit_fn)

    if(not args.test):
        save_name = f"Fit_Par_{fit_par}_Q2_y_{Q2_y_bin}_zG_{z_group}_{fit_type}"
        if(args.save_name is not None):
            save_name = f"{save_name}_{args.save_name}"
        save_canvas(canvas, save_name, args.save_format)

    return canvas, graph, fit_fn, fit_result




if(__name__ == "__main__"):
    args = parse_args()
    timer = RuntimeTimer()
    timer.start()
    silence_root_import()
    List_of_Fit_Parameters = load_json_file(args.file)
    print(f"{color.BBLUE}Loaded Parameters from: {color.BPINK}{str(args.file).split('/')[-1]}{color.END}")
    # if(args.verbose):
    #     print(f"\n{color.BOLD}The contents of this file are as follows:{color.END}")
    #     for ii in List_of_Fit_Parameters:
    #         print(f"\t{color.BOLD}{ii}: {color.END}{List_of_Fit_Parameters[ii]}")
    #     print(f"\nTotal Number of Entries = {len(List_of_Fit_Parameters)}")

    # Keep ROOT objects alive
    keep_canvases = []
    keep_graphs   = []
    keep_fits     = []

    Param_list    = ["B", "C"]   if(args.fit_parameter  is None) else [args.fit_parameter]
    Q2_y_range    = range(1, 18) if(args.Q2_y_Bin in [None, -1]) else [args.Q2_y_Bin]
    z_group_range = range(1, 8)  if(args.z_group  in [None, -1]) else [args.z_group]
    for fit_par         in Param_list:
        for Q2_y_bin    in Q2_y_range:
            print(f"Q2_y_bin = {Q2_y_bin}")
            for z_group in z_group_range:
                try:
                    bin_range = Q2_y_z_pT_Bin_rows_function("z", z_group, Q2_y_Bin=Q2_y_bin, Output_Q="Bins")
                    # x_range   = Q2_y_z_pT_Bin_rows_function("z", z_group, Q2_y_Bin=Q2_y_bin, Output_Q="Centers")
                    print(f"\tz_group = {z_group}")
                except ValueError as e:
                    msg = str(e).lower()
                    if("out of range" in msg):
                        # print(f"\t\tSkipping invalid z_group={z_group} for Q2_y_bin={Q2_y_bin} ({e})")
                        break
                    raise
                print(f"\t\tbin_range = {bin_range}")
                # print(f"\t\tx_range   = {x_range}")

                x_vals, y_vals, y_errs = [], [], []

                for bin_num in bin_range:
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_bin, Z_PT_BIN=bin_num, BINNING_METHOD="Y_bin")):
                        continue
                    Moment_To_Plot = List_of_Fit_Parameters.get(f"{fit_par}_{Q2_y_bin}_{bin_num}",    None)
                    if(Moment_To_Plot is None):
                        print(f"\t\t{color.Error}Missing Parameter '{fit_par}' for Bin ({Q2_y_bin}-{bin_num}){color.END}\n")
                        continue
                    Err__of_Moment = List_of_Fit_Parameters.get(f"{fit_par}_ERR_{Q2_y_bin}_{bin_num}", 0.0)
                    print(f"\t\t{color.BOLD}{color.UNDERLINE}Par {fit_par}{color.END_B} of Bin {f'({Q2_y_bin}-{bin_num})':>7s}:{color.END} {Moment_To_Plot:>8.5f} ± {Err__of_Moment:1.3e}")

                    x_vals.append(float(get_bin_centers(var="z", Q2_y_num=Q2_y_bin, z_pT_num=bin_num)))
                    y_vals.append(float(Moment_To_Plot))
                    y_errs.append(float(Err__of_Moment))

                make_and_save_parameter_plot(fit_par, Q2_y_bin, z_group,
                                             bin_range, x_vals, y_vals, y_errs,
                                             args, keep_canvases=keep_canvases, keep_graphs=keep_graphs, keep_fits=keep_fits)

    print(f"\n{color.BGREEN}Done Running {color.END_B}'Creation_of_Parameter_Fits.py'{color.END}\n")
    timer.stop()


