#!/usr/bin/env python3

import ROOT
import argparse
import sys
import subprocess
import re

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from Binning_Dictionaries import Full_Bin_Definition_Array, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D #, Bin_Converter_5D # Binning Dictionaries
sys.path.remove(script_dir)
del script_dir

from array import array
import traceback
import fcntl

ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetGridColor(920)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)


# =========================
# Argument Parsing
# =========================
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Create ROOT-first outputs (TGraphs) from EvGen cross_section and optionally draws/saves them as images.", formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-p", "--plot",
                        type=str, default="RC",
                        choices=["RC", "rc", "rc_ave", "BORN", "born", "totalcs", "nrad", "sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"],
                        help="The calculated value to be plotted.\n")
    parser.add_argument("-V", "-var", "--variable",
                        type=str, default="phi_h",
                        choices=["Q2", "y", "z", "pT", "phi_h", "phi_s", "k0_cut"],
                        help="Variable to plot against.\n")

    parser.add_argument("-q2y", "--Q2_y_bin",
                        type=int, default=1,
                        help="Bin key for Q2_y Bin (required for z/pT plotting).\n")
    parser.add_argument("-zpt", "--z_pT_bin",
                        type=int, default=1,
                        help="Bin key for z_pT Bin.\n")
    parser.add_argument("-4d", "--Q2_y_z_pT_bin",
                        type=int,
                        help="4D bin key converted via Bin_Converter_4D_to_2D.\n")

    parser.add_argument("-g-Q2", "--Q2_group",
                        type=int,
                        help="Group of Q2-y Bins used for plotting vs Q2.\n")
    parser.add_argument("-g-y", "--y_group",
                        type=int,
                        help="Group of Q2-y Bins used for plotting vs y.\n")
    parser.add_argument("-g-pT", "--pT_group", 
                        type=int,
                        help="Group of z-pT Bins used for plotting vs pT (depends on Q2_y_Bin).\n")
    parser.add_argument("-g-z", "--z_group", 
                        type=int,
                        help="Group of z-pT Bins used for plotting vs z (depends on Q2_y_Bin).\n")

    parser.add_argument("--phi_h",
                        type=float, default=0.0,
                        help="Fixed value for phi_h parameter. (Use Radians)\n")
    parser.add_argument("--phi_s",
                        type=float, default=0.0,
                        help="Fixed value for phi_s parameter. (Use Radians)\n")
    parser.add_argument("--k0_cut",
                        type=float, default=0.01,
                        help="Fixed value for k0_cut parameter.\n")

    parser.add_argument("-n", "--name",
                        type=str,
                        help="Extra name tag appended to outputs (ROOT filename and image filename).\n")
    parser.add_argument("-t", "--title",
                        type=str,
                        help="Extra text added to plot title.\n")

    parser.add_argument("-v", "--verbose",
                        action='store_true',
                        help="Verbose print statements.\n")
    parser.add_argument("-md", "--meta_data",
                        action='store_true',
                        help="Saves the meta data to the ROOT files.\n")

    parser.add_argument("-nf", "--no_file",
                        action='store_true',
                        help="Skip ROOT output writing (useful if only images output files are desired).\n")
    parser.add_argument("-si", "--save_image",
                        action='store_true',
                        help="Create image files (PNG/PDF) and also write Canvas/TLatex to ROOT.\n")
    parser.add_argument("-ur", "--use_radian",
                        action='store_true',
                        help="Plot angles in radians instead of degrees (inputs always remain in radians, but the plots will default to degrees unless told otherwise).\n")

    parser.add_argument("-oft", "--output_file_type",
                        default=".png", choices=[".png", ".pdf"],
                        help="Image file format (only used with '--save_image').\n")
    
    parser.add_argument("-f", "--fit",
                        action='store_true',
                        help="Fit phi_h plots with A*(1 + B*cos(phi_h) + C*cos(2*phi_h)).\n")
    parser.add_argument("-s", "--scan",
                        action='store_true',
                        help="Scan within kinematic bins and average (phi_h only).\n")
    parser.add_argument("-sn", "--scan_num",
                        type=int, default=10,
                        help="Number of bins to scan through when '--scan' is used.\n")

    parser.add_argument("-r", "--root",
                        type=str, default="RC_Factor_Plots.root", 
                        help="Base name (or path) for output ROOT file (without .root). Will append the string from '--name' if it is set.\n")

    parser.add_argument("-uj", "--use_json",
                        action='store_true',
                        help="If fitting, save fit parameters to JSON.\n")
    parser.add_argument("-json", "--json_file",
                        type=str, default="Fit_Parameters_from_Make_RC_Factor_Plots.json",
                        help="JSON file name for fit parameters (used with '--use_json').\n")

    parser.add_argument("-mm", "--modulation_mode",
                        type=int, default=0,
                        choices=[0, 1, 2],
                        help="EvGen structure-function mode selector (passed to 'cross_section').\n")

    parser.add_argument('-e', '--email',
                   action='store_true',
                   help="Sends an email to user when done running.\n")
    parser.add_argument('-em', '--email_message',
                   type=str,
                   default="",
                   help="Extra email message to be added when given (use with `--email`).\n")

    return parser.parse_args()

# =========================
# Email Writers
# =========================

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

def Construct_Email(args, Crashed=False, Warning=False, final_count=None, Count_Type="Images"):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label=Count_Type, count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer"]):
            continue
        if((str(name) in ["scan_num"]) and (not args.scan)):
            continue
        if((str(name) in ["root", "root_file"]) and (args.no_file)):
            continue
        if((str(name) in ["output_file_type", "Save_Name"]) and (not args.save_image)):
            continue
        if((str(name) in ["json_file"]) and (not args.use_json)):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'Make_RC_Factor_Plots.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

{args.email_message}

Arguments:
{args_list}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'Make_RC_Factor_Plots.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'Make_RC_Factor_Plots.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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

def Other_Save_Message(args):
    start_time = str(args.timer.start_find(return_Q=True)).replace("Ran", "Started running")
    end_time, total_time, _ = args.timer.stop(return_Q=True)
    Save_Info_List = [f"start_time: {start_time}", f"end_time: {end_time}", f"total_time: {total_time}"]
    for name, value in vars(args).items():
        if(str(name) in ["timer"]):
            continue
        Save_Info_List.append(f"{name}: {str(value)}")
    return Save_Info_List

# =========================
# Plot Helpers
# =========================

def variable_Title_name_new(variable_in):
    if(variable_in in ["k0_cut"]):
        return "E^{Cutoff}_{#gamma}"
    else:
        output = variable_Title_name(variable_in)
        output = output.replace(" (lepton energy loss fraction)", "")
        return output

def fit_phi_h_graph(graph, DegOrRad=True, Color_Line=ROOT.kRed):
    # Fit g(x) to A*(1 + B*cos(x) + C*cos(2x)) over the *points’* x-range (not the axis range).
    npts = graph.GetN()
    if(npts <= 0):
        return None, None, None, None, None, None

    # Get xmin/xmax from the actual points
    x_vals = []
    if(hasattr(graph, "GetPointX")):
        for ii in range(npts):
            x_vals.append(float(graph.GetPointX(ii)))
    else:
        x_tmp = ROOT.Double(0)
        y_tmp = ROOT.Double(0)
        for ii in range(npts):
            graph.GetPoint(ii, x_tmp, y_tmp)
            x_vals.append(float(x_tmp))

    xmin = min(x_vals)
    xmax = max(x_vals)
    ymin = min(graph.GetY())
    ymax = max(graph.GetY())

    if(DegOrRad): # Using Degrees
        f = ROOT.TF1(f"phi_h_fit_of_graph_{graph.GetName()}", "[0]*(1 + [1]*cos(x * TMath::DegToRad()) + [2]*cos(2 * x * TMath::DegToRad()))", xmin, xmax)
    else:         # Using Radians
        f = ROOT.TF1(f"phi_h_fit_of_graph_{graph.GetName()}", "[0]*(1 + [1]*cos(x) + [2]*cos(2*x))", xmin, xmax)

    f.SetParameter(0, (ymin + ymax)/2)
    f.SetParLimits(0, min([0.8*ymin, 1.2*ymin]), max([0.8*ymax, 1.2*ymax]))
    f.SetParameter(1,  0)
    f.SetParLimits(1, -1, 1)
    f.SetParameter(2,  0)
    f.SetParLimits(2, -1, 1)

    f.SetLineColorAlpha(Color_Line, 0.85)
    f.SetLineStyle(2)

    graph.Fit(f, "QR")   # QR = quiet, recursive
    A, Aerr = f.GetParameter(0), f.GetParError(0)
    B, Berr = f.GetParameter(1), f.GetParError(1)
    C, Cerr = f.GetParameter(2), f.GetParError(2)

    return A, Aerr, B, Berr, C, Cerr

# =========================
# JSON Code for Saving Fit Parameters
# =========================
import json
import os
import time

def save_fit_to_json(param_label, param_value, param_error=None, Q2Y_Bin=1, z_pT_Bin=1, json_file="Fit_Parameters_for_RC.json", lock_timeout_sec=120, stale_lock_sec=3600, indent=2, sort_keys=True, verbose=False):
    param_label = str(param_label).strip()
    if(param_label == ""):
        raise ValueError("save_fit_to_json(...): param_label is empty")
    q2y_bin = int(Q2Y_Bin)
    zpt_bin = int(z_pT_Bin)
    key_val = f"{param_label}_{q2y_bin}_{zpt_bin}"
    key_err = f"{param_label}_ERR_{q2y_bin}_{zpt_bin}"
    json_path = os.path.abspath(json_file)
    json_dir  = os.path.dirname(json_path)
    if((json_dir != "") and (not os.path.exists(json_dir))):
        os.makedirs(json_dir, exist_ok=True)
    lock_dir = f"{json_path}.lockdir"
    start_t  = time.time()
    # Acquire lock (mkdir is atomic)
    while(True):
        try:
            os.mkdir(lock_dir)
            owner_path = os.path.join(lock_dir, "owner.txt")
            with open(owner_path, "w") as ofile:
                ofile.write(f"pid={os.getpid()}\n")
                ofile.write(f"epoch={time.time():.6f}\n")
            break
        except FileExistsError:
            try:
                lock_age = time.time() - os.path.getmtime(lock_dir)
                if(lock_age > float(stale_lock_sec)):
                    owner_path = os.path.join(lock_dir, "owner.txt")
                    if(os.path.exists(owner_path)):
                        try:
                            os.remove(owner_path)
                        except Exception:
                            pass
                    try:
                        os.rmdir(lock_dir)
                        continue
                    except Exception:
                        pass
            except Exception:
                pass
            if((time.time() - start_t) > float(lock_timeout_sec)):
                raise RuntimeError(f"save_fit_to_json(...): timed out waiting for lock: {lock_dir}")
            time.sleep(0.10)
    try:
        data = {}
        if(os.path.exists(json_path)):
            try:
                with open(json_path, "r") as jfile:
                    raw = jfile.read().strip()
                if(raw != ""):
                    data = json.loads(raw)
                    if(not isinstance(data, dict)):
                        raise ValueError("JSON root is not an object/dict")
            except json.JSONDecodeError:
                backup = f"{json_path}.corrupt.{int(time.time())}"
                try:
                    os.replace(json_path, backup)
                except Exception:
                    pass
                data = {}
        data[key_val] = float(param_value) if(param_value is not None) else None
        if(param_error is not None):
            data[key_err] = float(param_error)
        tmp_path = f"{json_path}.tmp.{os.getpid()}"
        with open(tmp_path, "w") as tfile:
            json.dump(data, tfile, indent=indent, sort_keys=sort_keys)
            tfile.write("\n")
        os.replace(tmp_path, json_path)
        if(verbose):
            print(f"Updated JSON: {json_path}")
            print(f"  {key_val} = {data[key_val]}")
            if(param_error is not None):
                print(f"  {key_err} = {data[key_err]}")
    finally:
        try:
            owner_path = os.path.join(lock_dir, "owner.txt")
            if(os.path.exists(owner_path)):
                os.remove(owner_path)
        except Exception:
            pass
        try:
            os.rmdir(lock_dir)
        except Exception:
            pass
    return key_val, key_err

def _err0(err):
    return 0.0 if(err is None) else float(err)

# =========================
# ROOT Write Helper
# =========================

def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()

def build_root_filename(args):
    if(args.root is None):
        return None
    root_name = str(args.root).strip()
    if(root_name == ""):
        return None
    if(root_name.endswith(".root")):
        if(args.name):
            root_name = root_name.replace(".root", f"_{args.name}.root")
    else:
        if(args.name):
            root_name = f"{root_name}_{args.name}.root"
        else:
            root_name = f"{root_name}.root"
    return root_name

def get_plot_key_name(plot_choice):
    pc = str(plot_choice).lower()

    if(pc in ["rc"]):
        return "RC_Factor"
    if(pc in ["rc_ave"]):
        return "RC_Factor_Ave"
    if(pc in ["born"]):
        return "Born_CS"
    if(pc in ["totalcs"]):
        return "Total_CS"
    if(pc in ["nrad"]):
        return "NonRadiated_CS"

    if(pc in ["sf_cos_sel"]):
        return "FUU_cosphi"
    if(pc in ["sf_cos2_sel"]):
        return "FUU_cos2phi"
    if(pc in ["sf_cos_pro"]):
        return "FUU_cosphi_Prokudin"
    if(pc in ["sf_cos2_pro"]):
        return "FUU_cos2phi_Prokudin"

    if(pc in ["fit_b"]):
        return "B_from_SF"
    if(pc in ["fit_c"]):
        return "C_from_SF"

    return f"{plot_choice}"

def build_root_key(args, plot_choice):
    key_main = get_plot_key_name(plot_choice)
    smear    = "Scan" if(args.scan) else "''"
    key = f"({key_main})_(EvGen)_(SMEAR={smear})"
    if(args.Q2_y_bin is not None):
        key += f"_(Q2_y_bin_{args.Q2_y_bin})"
    if(args.z_pT_bin is not None):
        key += f"_(z_pT_bin_{args.z_pT_bin})"
    key += f"_({args.variable})"
    return key

# =========================
# New: Lock-protected multi-object ROOT saving
# =========================

def Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding):
    print("\n\nCounting Total Number of/Saving collected histograms...")
    fit_list_tags = ["Chi_Squared", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]
    def write_vec(tfile, name, py_list):
        if(py_list is None):
            Update_Email(args, update_message=f"{color.Error}WARNING:{color.END} Fit list '{name}' is None (skipping)", verbose_override=True)
            return
        if(not isinstance(py_list, (list, tuple))):
            Update_Email(args, update_message=f"{color.Error}WARNING:{color.END} Fit list '{name}' is type={type(py_list)} (expected list/tuple; skipping)", verbose_override=True)
            return
        if(len(py_list) == 0):
            Update_Email(args, update_message=f"{color.Error}WARNING:{color.END} Fit list '{name}' is empty (skipping)", verbose_override=True)
            return
        vec = ROOT.TVectorD(len(py_list))
        for ii, val in enumerate(py_list):
            vec[ii] = float(val)
        keyname = f"TVectorD_{name}"
        existing = tfile.GetListOfKeys().FindObject(keyname)
        if(existing):
            if(getattr(args, "verbose", False)):
                print(f"{color.BBLUE}Deleting:{color.END} '{keyname};*' (already exists)")
            tfile.Delete(f"{keyname};*")
        tfile.WriteObject(vec, keyname)
    root_file = build_root_filename(args)
    if(getattr(args, "no_file", False)):
        print(f"{color.PINK}Would be saving to: {color.BCYAN}{root_file}{color.END}")
        for key in List_of_All_Histos_For_Unfolding:
            print(f"\n{key} --> {type(List_of_All_Histos_For_Unfolding[key])}")
        print(f"\nFinal Count = {len(List_of_All_Histos_For_Unfolding)}")
        return List_of_All_Histos_For_Unfolding
    elif(root_file is None):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END} No ROOT file specified (args.root is None/empty).", continue_run=False)
    print(f"{color.BBLUE}Saving to: {color.BGREEN}{root_file}{color.END}")
    lock_file_path = root_file + ".lock"
    with open(lock_file_path, "w+") as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        output_file = ROOT.TFile(root_file, "UPDATE")
        # Optional metadata write
        if(args.meta_data):
            try:
                Save_Info_List = Other_Save_Message(args)
                File_Name_Tlist = ROOT.TList()
                File_Name_Tlist.SetName("Latest_Run_Info")
                for s in Save_Info_List:
                    File_Name_Tlist.Add(ROOT.TObjString(s))
                safe_write(File_Name_Tlist, output_file)
            except:
                Crash_Report(args, crash_message=f"{color.Error}Metadata write FAILED in 'Save_Histos_To_ROOT'. Will still finish running.\n{color.END_R}ERROR MESSAGE:{color.END}\n\n{traceback.format_exc()}", continue_run=True)
        elif(args.verbose):
            print("Not saving the meta data to the output ROOT file...\n")
        for key in List_of_All_Histos_For_Unfolding:
            try:
                obj = List_of_All_Histos_For_Unfolding[key]
                if((any(tag in key for tag in fit_list_tags)) and isinstance(obj, (list, tuple))):
                    write_vec(output_file, key, obj)
                elif(type(obj) is list):
                    Temp_Tlist = ROOT.TList()
                    Temp_Tlist.SetName(f"TList_of_{key}")
                    for s in obj:
                        Temp_Tlist.Add(ROOT.TObjString(str(s)))
                    safe_write(Temp_Tlist, output_file)
                else:
                    if(type(obj) is not ROOT.TObjString):
                        try:
                            obj.SetName(key)
                        except Exception:
                            pass
                    safe_write(obj, output_file)
            except:
                Crash_Report(args, crash_message=f"The Save Code would have CRASHED! Was trying to save: '{key}'. (Was allowed to finish running anyway...)\nERROR MESSAGE:\n\n{traceback.format_exc()}", continue_run=True)
        output_file.Close()
    print(f"\nFinal Count = {len(List_of_All_Histos_For_Unfolding)}")
    return List_of_All_Histos_For_Unfolding

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
        z_pT_Ranges = Full_Bin_Definition_Array.get(f'Q2-y={Q2_y_num}, z-pT={z_pT_num}', None)
        if(z_pT_Ranges):
            z_max, z_min, pT_max, pT_min = z_pT_Ranges
            return_value = (0.5 * (pT_max + pT_min)) if(var in ["pT"]) else (0.5 * (z_max + z_min)) if(var in ["z"]) else [(0.5 * (pT_max + pT_min)), (0.5 * (z_max + z_min))]
            return round(return_value, 5) if(not isinstance(return_value, list)) else return_value
    return [None, None] if(var in ["Q2_y", "z_pT"]) else None

def get_bins_in_row_or_column(cols, rows, target, axis):
    if(axis not in ('pT', 'z')):
        raise ValueError("Axis must be either 'pT' (for rows) or 'z' (for columns)")
    if(axis in ['pT', 'row']):
        if((target < 1) or (target > rows)):
            print(f"{color.Error}'target' = {target} while 'rows' = {rows} so ((target < 1) or (target > rows)){color.END}")
            raise ValueError("pT (row) index out of range.")
        start = (target - 1) * cols + 1
        return list(range(start, start + cols))
    else:
        if((target < 1) or (target > cols)):
            raise ValueError("z (column) index out of range.")
        z_return = [target + (r * cols) for r in range(rows)]
        z_return.sort(reverse=True)
        return z_return

def Q2_y_z_pT_Bin_rows_function(var, row_num, Q2_y_Bin=None, Output_Q="Centers"):
    bin_num_list = None
    if(var in ["Q2", "y"]):
        bin_num_list = Q2_y_Bin_rows_Array[f"{var}-row-{row_num}"]
    elif((var in ["pT", "z"]) and Q2_y_Bin):
        col_total, rows_total = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_y_Bin, Integration_Bins_Q=False)
        bin_num_list = get_bins_in_row_or_column(rows_total, col_total, row_num, var)
        print(f"Bin List of {var} in group {row_num}: {color.BOLD}{bin_num_list}{color.END} (Q2_y_Bin = {Q2_y_Bin})")
    if(Output_Q in ["Centers"]):
        bin_center_list = []
        for center_bin in bin_num_list:
            if(var in ["Q2", "y"]):
                if(get_bin_centers(var, center_bin, z_pT_num=None)):
                    bin_center_list.append(get_bin_centers(var, center_bin, z_pT_num=None))
            elif((var in ["pT", "z"]) and Q2_y_Bin):
                if(get_bin_centers(var, Q2_y_Bin, z_pT_num=center_bin)):
                    bin_center_list.append(get_bin_centers(var, Q2_y_Bin, z_pT_num=center_bin))
        return bin_center_list
    else:
        return bin_num_list
    return None

# =========================
# Calculation Function
# =========================

def parse_nradiate_output(NRadiate_text_output):
    # raw_line_by_key = {}   # key -> full original line string
    value_by_key = {}
    unc_by_key   = {}

    NRadiate_lines = NRadiate_text_output.splitlines()
    for line in NRadiate_lines:
        if(not line.strip()):
            continue

        line = line.replace(")  (S", ")_(S")
        line = line.replace(") (S",  ")_(S")
        line = line.replace(")  (P", ")_(P")
        line = line.replace(") (P",  ")_(P")
        line = line.replace("SF (S", "SF_(S")
        line = line.replace("SF (P", "SF_(P")

        key = line.split(None, 1)[0]
        # raw_line_by_key[key] = line

        tokens = line.replace("±", " ± ").split()
        nums = []
        for tok in tokens:
            if(tok in ("=", "±")):
                continue
            try:
                nums.append(float(tok))
            except ValueError:
                pass

        if("±" in tokens):
            if(len(nums) >= 2):
                value_by_key[key] = nums[-2]
                unc_by_key[key]   = nums[-1]
            elif(len(nums) == 1):
                value_by_key[key] = nums[-1]
                unc_by_key[key]   = None
            else:
                value_by_key[key] = None
                unc_by_key[key]   = None
        else:
            value_by_key[key] = (nums[-1] if(nums) else None)
            unc_by_key[key]   = None

    # Back-fill RC uncertainty if the RC line lacks a native "±"
    if(("RC" in value_by_key) and (unc_by_key.get("RC") is None)):
        tot   = value_by_key.get("σ_tot", None)
        born  = value_by_key.get("σ_B",   None)
        dtot  = _err0(unc_by_key.get("σ_tot", None))
        dborn = _err0(unc_by_key.get("σ_B",   None))
        if((tot is not None) and (born is not None) and (abs(float(tot)) > 0.0) and (abs(float(born)) > 0.0)):
            rc_val = float(tot) / float(born)
            rc_err = abs(rc_val) * ROOT.TMath.Sqrt((dtot/float(tot))*(dtot/float(tot)) + (dborn/float(born))*(dborn/float(born)))
            unc_by_key["RC"] = rc_err

    return value_by_key, unc_by_key

def Calc_RC_Factor(args, Q2_CS, y_CS, z_CS, pT_CS, phi_h_CS, phi_s_CS, k0_cut_CS, x_CS=None, Beam_E=10.6):
    function = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/sidis/build/example/cross_section"

    phi_h_degrees = float(phi_h_CS)*ROOT.TMath.RadToDeg()
    phi_h_degrees = round((phi_h_degrees+360) if(phi_h_degrees < 0) else phi_h_degrees, 5)
    pT2_CS = str(float(pT_CS)*float(pT_CS))

    if(not x_CS):
        x_CS = str(float(Q2_CS)/(2 * 0.938 * float(Beam_E) *float(y_CS)))

    if(args.verbose):
        print(f"""{color.BOLD}Current Inputs:
    Q2   = {color.BLUE}{float(Q2_CS):>7.4f}{color.END_B} GeV^2
    xB   = {color.BLUE}{float(x_CS):>7.4f}{color.END_B}
    y    = {color.BLUE}{float(y_CS):>7.4f}{color.END_B}
    z    = {color.BLUE}{float(z_CS):>7.4f}{color.END_B}
    pT   = {color.BLUE}{float(pT_CS):>7.4f}{color.END_B} GeV
    pT^2 = {color.BLUE}{float(pT2_CS):>7.4f}{color.END_B} GeV^2
    φh   = {color.BLUE}{float(phi_h_CS):>7.4f}{color.END_B} rad (i.e., {phi_h_degrees:>7.4f} degrees)
    φS   = {color.BLUE}{float(phi_s_CS):>7.4f}{color.END_B} rad
    k0   = {color.BLUE}{float(k0_cut_CS):>7.4f}{color.END}
""")

    NRadiate = subprocess.run([function, str(args.modulation_mode), str(Beam_E), "U", "U", str(x_CS), str(y_CS), str(z_CS), str(pT2_CS), str(phi_h_CS), str(phi_s_CS), str(k0_cut_CS)], capture_output=True, text=True)
    NRadiate_output = NRadiate.stdout

    if(NRadiate.returncode != 0):
        print(f"{color.Error}Error (NRadiate): {color.END_B}{NRadiate.stderr}{color.END}")
        return None, None
    else:
        if(args.verbose):
            print(f"Full Output:\n{NRadiate_output}\n\n")
        value_by_key, unc_by_key = parse_nradiate_output(NRadiate_text_output=NRadiate_output)
        return value_by_key, unc_by_key

# =========================
# RC Bin Scan Functions
# =========================

def phi_h_RADIAN_Scan_Bin(phi_h_Bin_Start):
    list_phi = [phi_h_Bin_Start, phi_h_Bin_Start + 7.5*ROOT.TMath.DegToRad(), phi_h_Bin_Start + 14.9*ROOT.TMath.DegToRad()]
    if(all(abs(ii) < 180*ROOT.TMath.DegToRad() for ii in list_phi)):
        return list_phi
    else:
        list_phi_2 = []
        for ii in list_phi:
            if(abs(ii) < 180*ROOT.TMath.DegToRad()):
                list_phi_2.append(ii)
            else:
                list_phi_2.append(ii - 180*ROOT.TMath.DegToRad())
        return list_phi_2

def Scan_RC_in_Bins(args, Q2_y_Bin, z_pT_Bin, phi_h_Bin, phi_s_Set, k0_cut_Set, Num_of_SubBins=10):
    Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y_Bin}, Q2-y']
    z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}']

    Q2_increment = (Q2_max - Q2_min)/Num_of_SubBins
    y_increment  = (y_max - y_min)/Num_of_SubBins
    z_increment  = (z_max - z_min)/Num_of_SubBins
    pT_increment = (pT_max - pT_min)/Num_of_SubBins

    phi_h_scan_list = phi_h_RADIAN_Scan_Bin(phi_h_Bin)
    y_min_true  = y_min
    z_min_true  = z_min
    pT_min_true = pT_min

    Q2_loop_num, y_loop_num, z_loop_num, pT_loop_num = 0, 0, 0, 0
    CS__nRad_List, Born__CS_List, Total_CS_List, RC_Fact__List = [], [], [], []
    CS__nRad_Lerr, Born__CS_Lerr, Total_CS_Lerr, RC_Fact__Lerr = [], [], [], []
    # CS_AMM___List, CS_radf__List, CS_rad___List                = [], [], []
    # CS_AMM___Lerr, CS_radf__Lerr, CS_rad___Lerr                = [], [], []
    
    while(round(Q2_min, 4) <= round(Q2_max, 4)):
        Q2_loop_num += 1
        print(f"\tCurrent Q2 increment = {Q2_min:>7.4f} ({color.BBLUE}{Q2_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
        y_min, y_loop_num = y_min_true, 0
        while(round(y_min, 4) <= round(y_max, 4)):
            y_loop_num += 1
            if(args.verbose):
                print(f"\t\tCurrent y increment = {y_min:>7.4f} ({color.BBLUE}{y_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
            z_min, z_loop_num = z_min_true, 0
            while(round(z_min, 4) <= round(z_max, 4)):
                z_loop_num += 1
                if(args.verbose):
                    print(f"\t\t\tCurrent z increment = {z_min:>7.4f} ({color.BBLUE}{z_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                pT_min, pT_loop_num = pT_min_true, 0
                while(round(pT_min, 4) <= round(pT_max, 4)):
                    pT_loop_num += 1
                    if(args.verbose):
                        print(f"\t\t\t\tCurrent pT increment = {pT_min:>7.4f} ({color.BBLUE}{pT_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                    for phi_h_loop_num, phi_h in enumerate(phi_h_scan_list):
                        if(args.verbose):
                            print(f"\t\t\t\t\tCurrent phi_h increment = {phi_h*ROOT.TMath.RadToDeg():>7.4f} degrees ({color.BBLUE}{phi_h_loop_num+1}{color.END_B} of {color.BGREEN}{len(phi_h_scan_list)}{color.END})")
                        value_by_key, unc_by_key = Calc_RC_Factor(args, str(Q2_min), str(y_min), str(z_min), str(pT_min), str(phi_h), str(phi_s_Set), str(k0_cut_Set))
                        if((value_by_key is None) or (unc_by_key is None)):
                            print(f"{color.Error}Scan step failed (Calc_RC_Factor returned None). Skipping this scan point.{color.END}")
                            continue
                        # CS_nRad_NRadiate = value_by_key.get("σ_nrad")
                        BornCS__NRadiate = value_by_key.get("σ_B")
                        TotalCS_NRadiate = value_by_key.get("σ_tot")
                        RC_Fact_NRadiate = value_by_key.get("RC")
                        # CS_AMM__NRadiate = value_by_key.get("σ_AMM")
                        # CS_radf_NRadiate = value_by_key.get("σ_rad_f")
                        # CS_rad__Radiated = value_by_key.get("σ_rad")

                        # if(None in [BornCS__NRadiate, TotalCS_NRadiate, RC_Fact_NRadiate, CS_AMM__NRadiate, CS_radf_NRadiate, CS_rad__Radiated]):
                        if(None in [BornCS__NRadiate, TotalCS_NRadiate, RC_Fact_NRadiate]):
                            print(f"{color.Error}Scan step returned incomplete values. Skipping this scan point.{color.END}")
                            continue

                        Born__CS_List.append(float(BornCS__NRadiate))
                        Total_CS_List.append(float(TotalCS_NRadiate))
                        RC_Fact__List.append(float(RC_Fact_NRadiate))
                        # CS__nRad_List.append(float(CS_nRad_NRadiate))
                        # CS_AMM___List.append(float(CS_AMM__NRadiate))
                        # CS_radf__List.append(float(CS_radf_NRadiate))
                        # CS_rad___List.append(float(CS_rad__Radiated))
                        # CS__nRad_Lerr.append(float(unc_by_key.get("σ_nrad"))  if(unc_by_key.get("σ_nrad")  is not None) else 0.0)
                        # CS_AMM___Lerr.append(float(unc_by_key.get("σ_AMM"))   if(unc_by_key.get("σ_AMM")   is not None) else 0.0)
                        # CS_radf__Lerr.append(float(unc_by_key.get("σ_rad_f")) if(unc_by_key.get("σ_rad_f") is not None) else 0.0)
                        # CS_rad___Lerr.append(float(unc_by_key.get("σ_rad"))   if(unc_by_key.get("σ_rad")   is not None) else 0.0)

                        Born__CS_Lerr.append(float(unc_by_key.get("σ_B"))   if(unc_by_key.get("σ_B")   is not None) else 0.0)
                        Total_CS_Lerr.append(float(unc_by_key.get("σ_tot")) if(unc_by_key.get("σ_tot") is not None) else 0.0)
                        RC_Fact__Lerr.append(float(unc_by_key.get("RC"))    if(unc_by_key.get("RC")    is not None) else 0.0)

                    pT_min += pT_increment
                    if(hasattr(args, "timer")):
                        print(f"\t\t\t\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
                z_min += z_increment
                if(hasattr(args, "timer")):
                    print(f"\t\t\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
            y_min += y_increment
            if(hasattr(args, "timer")):
                print(f"\t\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
        Q2_min += Q2_increment
        if(hasattr(args, "timer")):
            print(f"\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    if(hasattr(args, "timer")):
        args.timer.time_elapsed()
        sys.stdout.flush()
        
    def AveAndErr(_List, _Lerr):
        _Ave = sum(_List)/len(_List)
        _arr = array('d', _List)
        _Scatt = ROOT.TMath.RMS(len(_arr), _arr) / ROOT.TMath.Sqrt(len(_arr))
        if((len(_Lerr) != 0) and (len(_Lerr) == len(_List))):
            _Meas = ROOT.TMath.Sqrt(sum(u**2 for u in _Lerr)) / (len(_Lerr))
        else:
            _Meas = 0.0
        _Err = ROOT.TMath.Sqrt((_Meas**2) + (_Scatt**2))
        return _Ave, _Err

    if(len(Born__CS_List) == 0):
        return [None, None, None, None, None, None, None, None]

    Born__CS_Ave, Born__CS_Err = AveAndErr(Born__CS_List, Born__CS_Lerr)
    Total_CS_Ave, Total_CS_Err = AveAndErr(Total_CS_List, Total_CS_Lerr)
    RC_Fact__Ave, RC_Fact__Err = AveAndErr(RC_Fact__List, RC_Fact__Lerr)

    True_RC_for_Bin     = Total_CS_Ave/Born__CS_Ave
    True_RC_for_Bin_Err = True_RC_for_Bin * ROOT.TMath.Sqrt((Total_CS_Err / Total_CS_Ave)**2 + (Born__CS_Err  / Born__CS_Ave)**2)

    return [Born__CS_Ave, Born__CS_Err, Total_CS_Ave, Total_CS_Err, True_RC_for_Bin, True_RC_for_Bin_Err, RC_Fact__Ave, RC_Fact__Err]

# =========================
# Plot Generation
# =========================

def default_ranges(args):
    find_range = None
    if(args.variable == "Q2"):
        find_range = [round(2 + 1.18*ii, 5) for ii in range(6)]
        if(args.Q2_group):
            find_range = Q2_y_z_pT_Bin_rows_function("Q2", args.Q2_group, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")
    elif(args.variable == "y"):
        find_range = [round(0.35 + 0.04*ii, 5) for ii in range(11)]
        if(args.y_group):
            find_range = Q2_y_z_pT_Bin_rows_function("y", args.y_group, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")
    elif(args.variable == "z"):
        find_range = [round(0.1 + 0.1*ii, 5) for ii in range(8)]
        if(args.z_group):
            find_range = Q2_y_z_pT_Bin_rows_function("z", args.z_group, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")
            print(f"{color.GREEN}Range for z group {args.z_group} = {color.END_B}{find_range}{color.END}")
    elif(args.variable == "pT"):
        find_range = [round(0.1 + 0.1*ii, 5) for ii in range(8)]
        if(args.pT_group):
            find_range = Q2_y_z_pT_Bin_rows_function("pT", args.pT_group, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")
            print(f"{color.GREEN}Range for pT group {args.pT_group} = {color.END_B}{find_range}{color.END}")
    elif(args.variable == "k0_cut"):
        find_range = [round(0.001 + 0.005*ii, 5) if(ii < 20) else round((0.1*(ii-19)), 5) for ii in range(29)]
    elif((not args.use_radian) and (args.variable in ["phi_h", "phi_s"])):
        # find_range = [((ii * 15) if(ii*15 <= 180) else ((ii*15) - 360))*ROOT.TMath.DegToRad() for ii in range(24)]
        # find_range.append(-1*ROOT.TMath.DegToRad())
        find_range = [(((ii * 15)+7.5) if(((ii * 15)+7.5) <= 180) else ((ii*15) - (360-7.5)))*ROOT.TMath.DegToRad() for ii in range(24)]
    elif(args.variable in ["phi_h", "phi_s"]):
        # find_range = [((ii * 15)-180)*ROOT.TMath.DegToRad() for ii in range(25)]
        find_range = [((ii * 15)-(180 - 7.5))*ROOT.TMath.DegToRad() for ii in range(24)]
    elif(find_range is None):
        Crash_Report(args, crash_message=f"\n{color.Error}WARNING: Unknown variable to plot.{color.END}\n", continue_run=False)
    if(None in find_range):
        find_range.remove(None)
    return find_range

def make_plot(args):
    print(f"\n\n{color.BOLD}Starting 'make_plot' function...{color.END}\n\n")

    plot_choice = args.plot.lower()

    if((plot_choice == "rc_ave") and (not args.scan)):
        args.email = False # Do not send an email for such a quick failure
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR: '--plot rc_ave' is only supported with '--scan'.{color.END}\n", continue_run=False)

    if(args.scan and (args.variable not in ["phi_h"])):
        args.email = False # Do not send an email for such a quick failure
        Crash_Report(args, crash_message=f"\n{color.Error}WARNING: '--scan' assumes '--variable phi_h' (killing run).{color.END}\n", continue_run=False)

    if(args.scan and ("sf_cos" in str(plot_choice))):
        args.email = False # Do not send an email for such a quick failure
        Crash_Report(args, crash_message=f"\n{color.Error}WARNING: '--scan' is not set up for structure-function plots (killing run).{color.END}\n", continue_run=False)

    if(args.Q2_y_z_pT_bin):
        print(f"\n{color.BBLUE}Setting (Q2-y, z-pT) with 4D Bin Number: {color.END_B}{args.Q2_y_z_pT_bin}{color.END}")
        args.Q2_y_bin, args.z_pT_bin = Bin_Converter_4D_to_2D[f"Q2_y_z_pT_bin_{args.Q2_y_z_pT_bin}"]
        print(f"\n{color.BGREEN}Running with (Q2-y, z-pT) bin = {color.END_B}{color.UNDERLINE}({args.Q2_y_bin}, {args.z_pT_bin}){color.END}")

    if(args.z_pT_bin):
        if(f"Q2-y={args.Q2_y_bin}, z-pT={args.z_pT_bin}" not in Full_Bin_Definition_Array):
            args.email = False # Do not send an email for such a quick failure
            Full_Error = f"\n{color.Error}WARNING: Bin ('Q2-y={args.Q2_y_bin}, z-pT={args.z_pT_bin}') is not defined. MUST SKIP.{color.END}"
            if(args.Q2_y_z_pT_bin):
                Full_Error = f"{Full_Error}\n{color.BOLD}Corresponded to 4D bin {color.UNDERLINE}{args.Q2_y_z_pT_bin}{color.END}"
            Crash_Report(args, crash_message=Full_Error, continue_run=False)

    root_key       = build_root_key(args, plot_choice)
    args.root_file = build_root_filename(args)

    args.Save_Name = None
    if(args.save_image):
        args.Save_Name = f"{get_plot_key_name(plot_choice)}_vs_{args.variable}{args.output_file_type}"
        if(args.Q2_y_bin is not None):
            args.Save_Name = args.Save_Name.replace(args.output_file_type, f"_Q2_y_Bin_{args.Q2_y_bin}{args.output_file_type}")
        if(args.z_pT_bin is not None):
            args.Save_Name = args.Save_Name.replace(args.output_file_type, f"_z_pT_Bin_{args.z_pT_bin}{args.output_file_type}")
        if(args.name):
            args.Save_Name = args.Save_Name.replace(args.output_file_type, f"_{args.name}{args.output_file_type}")
        if(args.scan):
            args.Save_Name = f"Scanned_Bins_{args.Save_Name}"

    print(f"{color.CYAN}ROOT Key: {color.END_B}{root_key}{color.END}")
    if(args.root_file is not None):
        if(not args.no_file):
            print(f"{color.CYAN}ROOT File: {color.END_B}{args.root_file}{color.END}\n")
        else:
            print(f"{color.RED}Would have saved ROOT File: {color.END_B}{args.root_file}{color.END}\n")
    if(args.save_image and (args.Save_Name is not None)):
        print(f"{color.CYAN}Image File: {color.END_B}{args.Save_Name}{color.END}\n")
    else:
        print("")

    plot_var_title = variable_Title_name_new(args.variable)
    otherVar_Title = "RC Factor" if(plot_choice in ["rc", "rc_ave"]) else "#sigma_{Total}" if(plot_choice in ["totalcs"]) else "#sigma_{Born}" if(plot_choice == "born") else "#sigma_{non-rad}" if(plot_choice == "nrad") else "ERROR"

    if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro"]):
        otherVar_Title = f"{'' if('_pro' not in plot_choice) else '(EvGen-Default) '}F_{{UU}}^{{{'cos(#phi)' if('cos_' in plot_choice) else 'cos(2#phi)'}}}"

    if(plot_choice in ["fit_b", "fit_c"]):
        otherVar_Title = f"Pre-Determined Fit Parameter {'cos(#phi)' if('fit_b' in plot_choice) else 'cos(2#phi)'}"

    Q2, y  = get_bin_centers("Q2_y", args.Q2_y_bin) if(args.Q2_y_bin is not None) else [2.2, 0.7]
    pT, z  = get_bin_centers("z_pT", args.Q2_y_bin, args.z_pT_bin) if((args.z_pT_bin is not None) and (args.Q2_y_bin is not None)) else [0.555, 0.135]
    phi_h  = args.phi_h
    phi_s  = args.phi_s
    k0_cut = args.k0_cut
    Q2, y = round(Q2, 5), round(y, 5)
    pT, z = round(pT, 5), round(z, 5)
    x_range = default_ranges(args)
    x_vals, y_vals, x_errs, y_errs = [], [], [], []
    kwargs = {"Q2_CS":     str(Q2),
              "y_CS":      str(y),
              "z_CS":      str(z),
              "pT_CS":     str(pT),
              "phi_h_CS":  str(phi_h),
              "phi_s_CS":  str(phi_s),
              "k0_cut_CS": str(k0_cut)
    }

    for num, x in enumerate(x_range):
        converted = "" if(("phi" not in str(args.variable)) or args.use_radian) else f" rads = {x*ROOT.TMath.RadToDeg():.1f} degs"
        print(f"{color.BOLD}Running ({args.variable}) Point {color.BBLUE}{num+1:>3}{color.END_B} of {color.BGREEN}{len(x_range)}{color.END_B}... {color.END}({args.variable} = {x:.5f}{converted})")
        print(f"\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
        sys.stdout.flush()
        kwargs[f"{args.variable}_CS"] = str(x)
        if(args.scan):
            output = Scan_RC_in_Bins(args, Q2_y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, phi_h_Bin=x, phi_s_Set=phi_s, k0_cut_Set=k0_cut, Num_of_SubBins=args.scan_num)
            if((output is None) or (None in output)):
                Update_Email(args, update_message=f"{color.Error}WARNING: Scan returned 'None' values for {args.variable} = '{x}'; skipping point.{color.END}", verbose_override=True)
                continue
            if(plot_choice == "born"):
                rc_value, rc_error = output[0], output[1]
            elif(plot_choice == "totalcs"):
                rc_value, rc_error = output[2], output[3]
            elif(plot_choice == "rc"):
                rc_value, rc_error = output[4], output[5]
            elif(plot_choice == "rc_ave"):
                rc_value, rc_error = output[6], output[7]
            else:
                Crash_Report(args, crash_message=f"{color.Error}Unknown plot option in scan mode: {args.plot}{color.END}", continue_run=False)
            rc_value, rc_error = float(rc_value), float(rc_error)
            if(not args.use_radian):
                phi_deg  = ROOT.TMath.RadToDeg()*x
                phi_deg += 7.5
                if(phi_deg < 0):
                    phi_deg += 360
                x_vals.append(phi_deg)
                x_errs.append(7.5)
            else:
                phi_rad = x + 7.5*ROOT.TMath.DegToRad()
                if(phi_rad > 180*ROOT.TMath.DegToRad()):
                    phi_rad += -360*ROOT.TMath.DegToRad()
                x_vals.append(phi_rad)
                x_errs.append(7.5*ROOT.TMath.DegToRad())
            y_vals.append(rc_value)
            y_errs.append(rc_error)
        else:
            value_by_key, unc_by_key = Calc_RC_Factor(args, **kwargs)
            if((value_by_key is None) or (unc_by_key is None)):
                Update_Email(args, update_message=f"{color.Error}WARNING: Calc_RC_Factor returned 'None' for {args.variable} = '{x}'; skipping point.{color.END}", verbose_override=True)
                continue
            if(plot_choice == "rc"):
                rc_value = float(value_by_key["RC"])
                rc_error = _err0(unc_by_key.get("RC"))
            elif(plot_choice == "totalcs"):
                rc_value = float(value_by_key["σ_tot"])
                rc_error = _err0(unc_by_key.get("σ_tot"))
            elif(plot_choice == "born"):
                rc_value = float(value_by_key["σ_B"])
                rc_error = _err0(unc_by_key.get("σ_B"))
            elif(plot_choice == "nrad"):
                rc_value = float(value_by_key["σ_nrad"])
                rc_error = _err0(unc_by_key.get("σ_nrad"))
            elif(plot_choice == "sf_cos_sel"):
                rc_value = float(value_by_key["F_UU^cos(phi_h)_(Selected)"])
                rc_error = _err0(unc_by_key.get("F_UU^cos(phi_h)_(Selected)"))
            elif(plot_choice == "sf_cos2_sel"):
                rc_value = float(value_by_key["F_UU^cos(2phi_h)_(Selected)"])
                rc_error = _err0(unc_by_key.get("F_UU^cos(2phi_h)_(Selected)"))
            elif(plot_choice == "sf_cos_pro"):
                rc_value = float(value_by_key["F_UU^cos(phi_h)_(Prokudin)"])
                rc_error = _err0(unc_by_key.get("F_UU^cos(phi_h)_(Prokudin)"))
            elif(plot_choice == "sf_cos2_pro"):
                rc_value = float(value_by_key["F_UU^cos(2phi_h)_(Prokudin)"])
                rc_error = _err0(unc_by_key.get("F_UU^cos(2phi_h)_(Prokudin)"))
            elif(plot_choice == "fit_b"):
                rc_value = float(value_by_key["B_from_SF_(Selected)"])
                rc_error = _err0(unc_by_key.get("B_from_SF_(Selected)"))
            elif(plot_choice == "fit_c"):
                rc_value = float(value_by_key["C_from_SF_(Selected)"])
                rc_error = _err0(unc_by_key.get("C_from_SF_(Selected)"))
            elif(plot_choice == "rc_ave"):
                print()
                Crash_Report(args, crash_message=f"{color.Error}ERROR: '--plot rc_ave' requires '--scan'.{color.END}", continue_run=False)
            else:
                Crash_Report(args, crash_message=f"{color.Error}Unknown plot option: {args.plot}{color.END}", continue_run=False)
            if((not args.use_radian) and (args.variable in ["phi_h", "phi_s"])):
                phi_deg = ROOT.TMath.RadToDeg()*x
                if(phi_deg < 0):
                    phi_deg += 360
                x_vals.append(phi_deg)
            else:
                x_vals.append(x)
            y_vals.append(rc_value)
            x_errs.append(0.0)
            y_errs.append(rc_error)
            if((args.variable in ["phi_h"]) and (plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"])):
                Update_Email(args, update_message=f"\t{color.RED}Notice: SF and cosine moments don't have phi_h dependencies...{color.END}", verbose_override=True)
                for num_ii, x_ii in enumerate(x_range):
                    if(num_ii <= num):
                        continue
                    if((not args.use_radian) and (args.variable in ["phi_h", "phi_s"])):
                        phi_deg = ROOT.TMath.RadToDeg()*x_ii
                        if(phi_deg < 0):
                            phi_deg += 360
                        x_vals.append(phi_deg)
                    else:
                        x_vals.append(x_ii)
                    y_vals.append(rc_value)
                    x_errs.append(0.0)
                    y_errs.append(rc_error)
                break

    if(len(x_vals) == 0):
        Crash_Report(args, crash_message=f"{color.Error}ERROR: No points were successfully calculated; nothing to save.{color.END}", continue_run=False)

    Plot_Title_Full = f"{otherVar_Title} vs {plot_var_title}"
    if(args.scan):
        Plot_Title_Full = f"(Averaged over Kinematic Bins) {Plot_Title_Full}"
    if(args.title):
        Plot_Title_Full = f"#splitline{{{Plot_Title_Full}}}{{{args.title}}}"
    Plot_Title_Full = f"{Plot_Title_Full}; {plot_var_title}; {otherVar_Title}"

    graph = ROOT.TGraphErrors(len(x_vals), array('d', x_vals), array('d', y_vals), array('d', x_errs), array('d', y_errs))
    graph.SetTitle(Plot_Title_Full)
    graph.SetName(root_key)

    # Optional y-range tweaks for non-phi-dependent series (kept consistent with earlier behavior)
    if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"]):
        ymin, ymax = float("inf"), float("-inf")
        if(plot_choice in ["fit_b", "fit_c"]):
            ymin =  -1 if(plot_choice in ["fit_b"]) else -0.45
            ymax = 0.2 if(plot_choice in ["fit_b"]) else  0.25
        for yv in y_vals:
            ymin = min([ymin, 0.8*yv if(yv > 0) else 1.2*yv])
            ymax = max([ymax, 1.2*yv if(yv > 0) else 0.8*yv])
        graph.GetYaxis().SetRangeUser(ymin, ymax)

    # Fit + JSON (must be independent of image creation)
    Par_A, Par_Aerr, Par_B, Par_Berr, Par_C, Par_Cerr = None, None, None, None, None, None
    if((args.variable in ["phi_h"]) and (args.fit)):
        Par_A, Par_Aerr, Par_B, Par_Berr, Par_C, Par_Cerr = fit_phi_h_graph(graph, DegOrRad=(not args.use_radian))

        if(args.verbose):
            if((Par_B is not None) and (Par_Berr is not None)):
                Update_Email(args, update_message=f"\t{get_plot_key_name(plot_choice)} Cos(phi_h)   = {Par_B:<10.3e} ± {Par_Berr:1.3e}" if(abs(Par_B) < 0.01) else f"\t{get_plot_key_name(plot_choice)} Cos(phi_h)   = {Par_B:<10.5f} ± {Par_Berr:1.3e}", verbose_override=True)
            if((Par_C is not None) and (Par_Cerr is not None)):
                Update_Email(args, update_message=f"\t{get_plot_key_name(plot_choice)} Cos(2*phi_h) = {Par_C:<10.3e} ± {Par_Cerr:1.3e}" if(abs(Par_C) < 0.01) else f"\t{get_plot_key_name(plot_choice)} Cos(2*phi_h) = {Par_C:<10.5f} ± {Par_Cerr:1.3e}", verbose_override=True)

        if(args.use_json and (None not in [args.Q2_y_bin, args.z_pT_bin])):
            json_out = args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json")
            save_fit_to_json(f"{plot_choice}_A", Par_A, param_error=Par_Aerr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=json_out, verbose=args.verbose)
            save_fit_to_json(f"{plot_choice}_B", Par_B, param_error=Par_Berr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=json_out, verbose=args.verbose)
            save_fit_to_json(f"{plot_choice}_C", Par_C, param_error=Par_Cerr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=json_out, verbose=args.verbose)
            print(f'\n{color.BGREEN}Updated and Saved: {color.BBLUE}{json_out}{color.END}\n')
        elif(args.use_json):
            print(f"\n{color.Error}WARNING: Could not save JSON (Must select a Q2-y/z-pT bin).{color.END}\n")

    canvas = None
    latex  = None

    if(args.save_image and (args.Save_Name is not None)):
        canvas = ROOT.TCanvas("c1", "RC Factor Plot", 1200, 600)
        canvas.Divide(2, 1)

        pad1 = canvas.cd(1)
        pad1.SetGrid()
        pad1.SetLeftMargin(0.15)
        pad1.SetRightMargin(0.05)

        graph.SetLineColor(ROOT.kBlue)
        graph.SetMarkerColor(ROOT.kBlue)
        graph.SetMarkerStyle(20)
        graph.SetLineWidth(2)
        graph.Draw("ALP")

        canvas.cd(2)
        ROOT.gPad.SetBottomMargin(0.15)
        ROOT.gPad.SetLeftMargin(0.15)
        latex = ROOT.TLatex()
        latex.SetTextSize(0.045)
        latex.DrawLatexNDC(0.1, 0.9, "Fixed Kinematic Inputs:")
        placement = 0.83

        # Show only values that are actually fixed (i.e., not the x-axis variable)
        if(args.variable not in ["Q2"]):
            latex.DrawLatexNDC(0.1, placement, f"Q^{{2}} = {Q2:.4f} GeV^{{2}}")
            placement += -0.05
        if(args.variable not in ["Q2", "y"]):
            xB_val = (Q2/(2 * 0.938 * 10.6 * y)) if((y is not None) and (y != 0.0)) else 0.0
            latex.DrawLatexNDC(0.1, placement, f"x_{{B}} = {xB_val:.4f}")
            placement += -0.05
        if(args.variable not in ["y"]):
            latex.DrawLatexNDC(0.1, placement, f"y  = {y:.4f}")
            placement += -0.05
        if(args.variable not in ["z"]):
            latex.DrawLatexNDC(0.1, placement, f"z  = {z:.4f}")
            placement += -0.05
        if(args.variable not in ["pT"]):
            latex.DrawLatexNDC(0.1, placement, f"P_{{T}} = {pT:.4f} GeV")
            placement += -0.05

        if(args.variable not in ["phi_h"]):
            if(not args.use_radian):
                phi_h_degrees = phi_h*ROOT.TMath.RadToDeg()
                phi_h_degrees = phi_h_degrees + 360 if(phi_h_degrees < 0) else phi_h_degrees
                latex.DrawLatexNDC(0.1, placement, f"#phi_{{h}} = {phi_h_degrees:.4f} Degrees")
            else:
                latex.DrawLatexNDC(0.1, placement, f"#phi_{{h}} = {phi_h:.4f} Radians")
            placement += -0.05

        if(args.variable not in ["k0_cut"]):
            placement += -0.01
            latex.DrawLatexNDC(0.1, placement, f"E^{{Cutoff}}_{{#gamma}} = {k0_cut:.4f} GeV"); placement += -0.05

        if(args.Q2_y_bin is not None):
            placement += -0.02
            latex.DrawLatexNDC(0.1, placement, f"Q^{{2}}-y Bin {args.Q2_y_bin}")
            placement += -0.05
        if(args.z_pT_bin is not None):
            latex.DrawLatexNDC(0.1, placement, f"z-P_{{T}} Bin {args.z_pT_bin}")
            placement += -0.05

        if((args.variable in ["phi_h"]) and (args.fit) and (Par_B is not None) and (Par_C is not None)):
            # if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"]):
            placement += -0.02
            latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} From Fit: ")
            placement += -0.05
            latex.DrawLatexNDC(0.1, placement, f"{Par_A:<10.3e} #pm {Par_Aerr:1.3e}" if(abs(Par_A) < 0.01) else f"{Par_A:<10.5f} #pm {Par_Aerr:1.3e}")
            # else:
            placement += -0.07
            latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} Cos(#phi_{{h}})  From Fit: ")
            placement += -0.06
            latex.DrawLatexNDC(0.1, placement, f"{Par_B:<10.3e} #pm {Par_Berr:1.3e}" if(abs(Par_B) < 0.01) else f"{Par_B:<10.5f} #pm {Par_Berr:1.3e}")
            placement += -0.07
            latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} Cos(2#phi_{{h}}) From Fit: ")
            placement += -0.06
            latex.DrawLatexNDC(0.1, placement, f"{Par_C:<10.3e} #pm {Par_Cerr:1.3e}" if(abs(Par_C) < 0.01) else f"{Par_C:<10.5f} #pm {Par_Cerr:1.3e}")

        print(f"\n{color.BBLUE}Saving Image: {color.PINK}{args.Save_Name}{color.END}")
        canvas.SaveAs(args.Save_Name)
        print(f"{color.BGREEN}Image Saved.{color.END}")

    # =========================
    # ROOT output (now using Save_Histos_To_ROOT)
    # =========================
    if((not args.no_file) and (args.root_file is not None)):
        Objects_To_Save = {}
        Objects_To_Save[root_key] = graph

        if(args.save_image and (canvas is not None) and (latex is not None)):
            Objects_To_Save[f"{root_key}_Canvas"] = canvas
            Objects_To_Save[f"{root_key}_TLatex"] = latex

        Save_Histos_To_ROOT(args, Objects_To_Save)

    Construct_Email(args)

# =========================
# Main
# =========================

if(__name__ == "__main__"):
    args = parse_args()

    args.timer = RuntimeTimer()
    args.timer.start()

    if(args.use_json and (not args.fit)):
        print(f"{color.RED}Warning: To use '--use_json', '--fit' must be True (enabling fit).{color.END}")
        args.fit = True

    make_plot(args)
    