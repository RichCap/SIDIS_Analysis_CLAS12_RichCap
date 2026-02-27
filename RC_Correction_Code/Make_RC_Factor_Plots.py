#!/usr/bin/env python3

import ROOT
import argparse
import sys

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from Binning_Dictionaries import Full_Bin_Definition_Array, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D # Binning Dictionaries
sys.path.remove(script_dir)
del script_dir

# import math
from array import array

# import numpy, re
# from collections import OrderedDict
# import traceback
# import itertools

ROOT.ROOT.EnableImplicitMT()
ROOT.gStyle.SetGridColor(920)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)


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

    # f.SetLineColor(Color_Line)
    f.SetLineColorAlpha(Color_Line, 0.85)
    f.SetLineStyle(2)

    graph.Fit(f, "QR")   # QR = quiet, recursive (same as used in other fit functions in my unfolding code)
    # graph.Fit(f, "Q0")   # Q0 = quiet, no graphic
    B = f.GetParameter(1)
    C = f.GetParameter(2)

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
    # Saves ONE parameter (A/B/C/etc) and optionally its error to a JSON file using keys:
    #   "<PARAM>_<Q2Y>_<ZPT>" and "<PARAM>_ERR_<Q2Y>_<ZPT>"
    #
    # Concurrency protection:
    #   - Uses an atomic lock directory "<json_file>.lockdir" so multiple scripts can update the same JSON safely.
    #   - Writes via temp file + os.replace() for atomic file replacement (avoids partial writes).
    #
    # Behavior:
    #   - If the JSON already exists, it is read and updated (keys are added/overwritten), never wiped.
    #   - If the JSON is empty, starts from {}.

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
            # Mark ownership (optional, but helpful for debugging/stale detection)
            owner_path = os.path.join(lock_dir, "owner.txt")
            with open(owner_path, "w") as ofile:
                ofile.write(f"pid={os.getpid()}\n")
                ofile.write(f"epoch={time.time():.6f}\n")
            break
        except FileExistsError:
            # Stale lock handling (e.g., a crashed process left the lock behind)
            try:
                lock_age = time.time() - os.path.getmtime(lock_dir)
                if(lock_age > float(stale_lock_sec)): # Best-effort cleanup
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
        # Read existing JSON (if any)
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
                # If the file is corrupted (should be rare with locking + atomic replace), keep a backup and start fresh rather than silently discarding it.
                backup = f"{json_path}.corrupt.{int(time.time())}"
                try:
                    os.replace(json_path, backup)
                except Exception:
                    pass
                data = {}
        # Update keys (overwrite or add)
        data[key_val] = float(param_value) if(param_value is not None) else None
        if(param_error is not None):
            data[key_err] = float(param_error)
        # Atomic write: temp + replace
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
        # Release lock (best effort)
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

# Treat missing uncertainties as 0.0 (independent-error propagation)
def _err0(err):
    return 0.0 if(err is None) else float(err)
#JSON
def calc_rc_new_from_json(json_file_1, json_file_2, Q2Y_Bin=1, z_pT_Bin=1, phi_h=0, cs_nrad_in=[None, None], cs_AMM_in=[None, None], cs_rad_f_in=[None, None], cs_rad_in=[None, None], cs_born_in=[None, None], verbose=False):
    # Computes a new RC factor (RC_new) and its uncertainty (RC_new_err) using fit parameters stored in JSON files
    # Inputs:
    #   json_file_1, json_file_2 : paths to JSON files
    #                             - json_file_1 -> File for the 0th Order Born-Level Modulations (from EvGen)
    #                             - json_file_2 -> File for the Latest Measured Modulations (from unfolding)
    #   Q2Y_Bin, z_pT_Bin        : integer bin identifiers
    #   phi_h                   : phi_h value being used (must be given in radians)
    #   cs_nrad_in..cs_born_in  : Cross section inputs to calculate the new RC factor—each should be given as a list like [cs, err] or [cs, None]
    # Returns:
    #   [RC_new, RC_new_err], [cs_born_new, cs_born_new_err], [cs_tot_new, cs_tot_new_err]

    # ----------------------------------------
    # Basic input normalization
    # ----------------------------------------
    q2y_bin = int(Q2Y_Bin)
    zpt_bin = int(z_pT_Bin)

    if(phi_h is None):
        raise ValueError("calc_rc_new_from_json(...): phi_h is None")
    else:
        phi_h = float(phi_h)

    # Parse the cross section inputs into (val, err) pairs
    cs_nrad,  cs_nrad_err  = cs_nrad_in
    cs_AMM,   cs_AMM_err   = cs_AMM_in
    cs_rad_f, cs_rad_f_err = cs_rad_f_in
    cs_rad,   cs_rad_err   = cs_rad_in
    cs_born,  cs_born_err  = cs_born_in

    # If any required cross section VALUE is missing, do not attempt calculation
    if(None in [cs_nrad, cs_AMM, cs_rad_f, cs_rad, cs_born]):
        raise ValueError("calc_rc_new_from_json(...): One or more required cross section values are None")

    # Normalize numeric types
    cs_nrad  = float(cs_nrad)
    cs_AMM   = float(cs_AMM)
    cs_rad_f = float(cs_rad_f)
    cs_rad   = float(cs_rad)
    cs_born  = float(cs_born)

    cs_nrad_err  = _err0(cs_nrad_err)
    cs_AMM_err   = _err0(cs_AMM_err)
    cs_rad_f_err = _err0(cs_rad_f_err)
    cs_rad_err   = _err0(cs_rad_err)
    cs_born_err  = _err0(cs_born_err)

    # ----------------------------------------
    # Helper to read JSON dict
    # ----------------------------------------
    def _read_json_dict(path):
        print(f"\tReading JSON File: {color.BPINK}{path}{color.END}")
        if(path is None):
            raise ValueError("calc_rc_new_from_json(...): JSON path is None")

        abspath = os.path.abspath(str(path))
        if(not os.path.exists(abspath)):
            raise FileNotFoundError(f"calc_rc_new_from_json(...): JSON file not found: {abspath}")

        with open(abspath, "r") as f:
            raw = f.read().strip()
        if(raw == ""):
            return {}

        data = json.loads(raw)
        if(not isinstance(data, dict)):
            raise ValueError(f"calc_rc_new_from_json(...): JSON root is not a dict: {abspath}")
        return data

    # ----------------------------------------
    # Fetch parameters from both JSON files
    # ----------------------------------------
    BornL_JSON = _read_json_dict(json_file_1)
    UnfoldJSON = _read_json_dict(json_file_2)

    # Expected key format:
    #   "A_<Q2Y>_<ZPT>", "A_ERR_<Q2Y>_<ZPT>" (and same for B, C)
    def _get_param(data, label):
        key_val = f"{label}_{q2y_bin}_{zpt_bin}"
        key_err = f"{label}_ERR_{q2y_bin}_{zpt_bin}"
        val     = data.get(key_val, None)
        err     = data.get(key_err, None)
        return val, _err0(err)

    # Pull B/C from each file (A is not needed)
    # A_born, A_born_err = _get_param(BornL_JSON, "A") # Not used in these calculations (only injecting the modulations B and C)
    # A_unfd, A_unfd_err = _get_param(UnfoldJSON, "A")
    B_born, B_born_err = _get_param(BornL_JSON, "born_B") # The born level json files add the extra 'born_' string to the keys to make sure they are never confused with the keys from the unfolded measurements
    C_born, C_born_err = _get_param(BornL_JSON, "born_C")
    B_unfd, B_unfd_err = _get_param(UnfoldJSON, "B")
    C_unfd, C_unfd_err = _get_param(UnfoldJSON, "C")

    if(None in [B_born, C_born, B_unfd, C_unfd]):
        print(f"{color.Error}ERROR in calc_rc_new_from_json(...): The selected bin does not have a complete set of measurements for both the born-level and unfolded modulations...\nCannot return new RC values.{color.END}")
        return None, None, None

    # Normalize numeric types (JSON may store as int/float/str)
    B_born = float(B_born)
    C_born = float(C_born)
    B_unfd = float(B_unfd)
    C_unfd = float(C_unfd)

    cos1 = ROOT.TMath.Cos(phi_h)
    cos2 = ROOT.TMath.Cos(2*phi_h)

    Mods_Born = (1.0 + B_born*cos1 + C_born*cos2)
    Mods_Unfd = (1.0 + B_unfd*cos1 + C_unfd*cos2)

    # Mods uncertainties: M = 1 + B*cos(phi) + C*cos(2phi)
    Mods_Born_err = ROOT.TMath.Sqrt((cos1*B_born_err)*(cos1*B_born_err) + (cos2*C_born_err)*(cos2*C_born_err))
    Mods_Unfd_err = ROOT.TMath.Sqrt((cos1*B_unfd_err)*(cos1*B_unfd_err) + (cos2*C_unfd_err)*(cos2*C_unfd_err))

    # IRCM = Mods_Unfd / Mods_Born
    IRCM = Mods_Unfd/Mods_Born if(abs(Mods_Born) > 1e-30) else None
    IRCM_err = None
    if(IRCM is not None):
        IRCM_err = ROOT.TMath.Sqrt((Mods_Unfd_err/Mods_Born)*(Mods_Unfd_err/Mods_Born) + (Mods_Unfd*Mods_Born_err/(Mods_Born*Mods_Born))*(Mods_Unfd*Mods_Born_err/(Mods_Born*Mods_Born)))
    else:
        raise ValueError("calc_rc_new_from_json(...): IRCM is None")

    born_nrad       = cs_nrad - cs_AMM - cs_rad_f # this is not the true born-level cross section (cs_born), but is proportional to it (i.e., born_nrad = C*cs_born where C are some other terms given in the cross section equation—see eq. 54 in the EvGen paper)
    born_nrad_err   = ROOT.TMath.Sqrt(cs_nrad_err*cs_nrad_err + cs_AMM_err*cs_AMM_err + cs_rad_f_err*cs_rad_f_err)
    cs_tot_new      = ((born_nrad*IRCM) + cs_AMM + cs_rad_f) + cs_rad
    cs_tot_new_err  = ROOT.TMath.Sqrt((IRCM*born_nrad_err)*(IRCM*born_nrad_err) + (born_nrad*IRCM_err)*(born_nrad*IRCM_err) + cs_AMM_err*cs_AMM_err + cs_rad_f_err*cs_rad_f_err + cs_rad_err*cs_rad_err)
    cs_born_new     = cs_born*IRCM
    cs_born_new_err = ROOT.TMath.Sqrt((IRCM*cs_born_err)*(IRCM*cs_born_err) + (cs_born*IRCM_err)*(cs_born*IRCM_err))

    RC_new     = cs_born_new/cs_tot_new if(abs(cs_tot_new) > 1e-30) else None
    RC_new_err = None
    if(RC_new is not None):
        RC_new_err = ROOT.TMath.Sqrt((cs_born_new_err/cs_tot_new)*(cs_born_new_err/cs_tot_new) + (cs_born_new*cs_tot_new_err/(cs_tot_new*cs_tot_new))*(cs_born_new*cs_tot_new_err/(cs_tot_new*cs_tot_new)))
    else:
        raise ValueError("calc_rc_new_from_json(...): RC_new is None")

    return [RC_new, RC_new_err], [cs_born_new, cs_born_new_err], [cs_tot_new, cs_tot_new_err]


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

def Q2_y_z_pT_Bin_rows_function(var, row_num, Q2_y_Bin=None, Output_Q="Centers"):
    bin_num_list = None
    if(var    in ["Q2", "y"]):
        bin_num_list = Q2_y_Bin_rows_Array[f"{var}-row-{row_num}"]
    elif((var in ["pT", "z"]) and Q2_y_Bin):
        col_total, rows_total = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_y_Bin, Integration_Bins_Q=False)
        bin_num_list = get_bins_in_row_or_column(rows_total, col_total, row_num, var)
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
# Calculation Function
# =========================
def parse_nradiate_output(NRadiate_text_output):
    # Containers
    raw_line_by_key = {}   # key -> full original line string
    value_by_key = {}      # key -> float main value
    unc_by_key = {}        # key -> float uncertainty
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
        # Key is the first whitespace-separated token
        key = line.split(None, 1)[0]
        raw_line_by_key[key] = line
        # Tokenize with isolated ±
        tokens = line.replace("±", " ± ").split()
        # Collect all float-convertible tokens
        nums = []
        for tok in tokens:
            if(tok in ("=", "±")):
                continue
            try:
                nums.append(float(tok))
            except ValueError:
                pass
        # Assign value and uncertainty
        if("±" in tokens):
            # Expected format: ... = <value> ± <unc>
            if(len(nums) >= 2):
                value_by_key[key] = nums[-2]
                unc_by_key[key] = nums[-1]
            elif(len(nums) == 1):
                value_by_key[key] = nums[-1]
                unc_by_key[key] = None
            else:
                value_by_key[key] = None
                unc_by_key[key] = None
        else:
            value_by_key[key] = (nums[-1] if(nums) else None)
            unc_by_key[key] = None
    return value_by_key, unc_by_key

import subprocess
def Calc_RC_Factor(Q2_CS, y_CS, z_CS, pT_CS, phi_h_CS, phi_s_CS, k0_cut_CS, x_CS=None, Beam_E=10.6, tau_CS=0, phi_k_CS=0, R_CS=0, verbose=True, return_errors=False, Q2yBin=None, zpTBin=None):
    function = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/sidis/build/example/cross_section"
    Use_Rad = (tau_CS != 0) and (phi_k_CS != 0) and (R_CS != 0)
    phi_h_degrees = float(phi_h_CS)*ROOT.TMath.RadToDeg()
    phi_h_degrees = round((phi_h_degrees+360) if(phi_h_degrees < 0) else phi_h_degrees, 5)
    pT2_CS = str(float(pT_CS)*float(pT_CS))
    if(not x_CS):
        x_CS = str(float(Q2_CS)/(2 * 0.938 * float(Beam_E) *float(y_CS)))
    if(verbose):
        print(f"""{color.BOLD}Current Inputs:
    Q2   = {color.BLUE}{float(Q2_CS):>7.4f}{color.END_B} GeV^2
    xB   = {color.BLUE}{float(x_CS):>7.4f}{color.END_B}
    y    = {color.BLUE}{float(y_CS):>7.4f}{color.END_B}
    z    = {color.BLUE}{float(z_CS):>7.4f}{color.END_B}
    pT   = {color.BLUE}{float(pT_CS):>7.4f}{color.END_B} GeV
    pT^2 = {color.BLUE}{float(pT2_CS):>7.4f}{color.END_B} GeV^2
    φh   = {color.BLUE}{float(phi_h_CS):>7.4f}{color.END_B} rad (i.e., {phi_h_degrees:>7.4f} degrees)
    φS   = {color.BLUE}{float(phi_s_CS):>7.4f}{color.END_B} rad
    k0   = {color.BLUE}{float(k0_cut_CS):>7.4f}{color.END}{f'''
    𝞃    = {color.BLUE}{float(tau_CS):>7.4f}{color.END_B}
    φk   = {color.BLUE}{float(phi_k_CS):>7.4f}{color.END_B} rad
    R    = {color.BLUE}{float(R_CS):>7.3f}{color.END_B}''' if(Use_Rad) else ''}
""")

    if(Use_Rad):
        Radiated        = subprocess.run([function, str(args.modulation_mode), str(Beam_E), "U", "U", str(x_CS), str(y_CS), str(z_CS), str(pT2_CS), str(phi_h_CS), str(phi_s_CS), str(tau_CS), str(phi_k_CS), str(R_CS)], capture_output=True, text=True)
        Radiated_output = Radiated.stdout
        check_RAD       = Radiated.returncode != 0
    else:
        check_RAD   = False
    NRadiate        = subprocess.run([function,     str(args.modulation_mode), str(Beam_E), "U", "U", str(x_CS), str(y_CS), str(z_CS), str(pT2_CS), str(phi_h_CS), str(phi_s_CS), str(k0_cut_CS)],                        capture_output=True, text=True)
    NRadiate_output = NRadiate.stdout
    # Optionally, handle errors
    if(check_RAD or (NRadiate.returncode != 0)):
        print(f"{color.Error}Error (NRadiate): {color.END_B}{NRadiate.stderr}{color.END}")
        if(Use_Rad):
            print(f"\n{color.Error}Error (Radiated): {color.END_B}{Radiated.stderr}{color.END}")
        return [None, None, None, None, None, None, None]
    else:
        if(verbose):
            print(f"Full Output:\n{NRadiate_output}\n\n")
        if(Use_Rad): # This format is not really used by this code any more after 2/4/2026
            NRadiate_output_list = NRadiate_output.split("\n")
            if(Use_Rad):
                Radiated_output_list = Radiated_output.split("\n")
            BornCS__line_NRadiate = NRadiate_output_list[0]
            TotalCS_line_NRadiate = NRadiate_output_list[len(NRadiate_output_list) - 3]
            RC_Fact_line_NRadiate = NRadiate_output_list[len(NRadiate_output_list) - 2]
            
            CSnRad_nRadiated_line = NRadiate_output_list[len(NRadiate_output_list) - 5]
    
            BornCS__list_NRadiate = BornCS__line_NRadiate.split()
            TotalCS_list_NRadiate = TotalCS_line_NRadiate.split()
            RC_Fact_list_NRadiate = RC_Fact_line_NRadiate.split()
            CSnRad_nRadiated_list = CSnRad_nRadiated_line.split()
            BornCS__NRadiate = float(BornCS__list_NRadiate[len(BornCS__list_NRadiate) - 1])
            
            CSnRad_nRadiated = CSnRad_nRadiated_list[len(CSnRad_nRadiated_list) - 3]
            
            TotalCS_NRadiate = TotalCS_list_NRadiate[len(TotalCS_list_NRadiate) - 3]
            Total_Error_NRad = TotalCS_list_NRadiate[len(TotalCS_list_NRadiate) - 1]
            RC_Fact_NRadiate = RC_Fact_list_NRadiate[len(RC_Fact_list_NRadiate) - 1]
            if(Use_Rad):
                BornCS__line_Radiated = Radiated_output_list[0]
                TotalCS_line_Radiated = Radiated_output_list[len(Radiated_output_list) - 3]
                RC_Fact_line_Radiated = Radiated_output_list[len(Radiated_output_list) - 2]
                BornCS__list_Radiated = BornCS__line_Radiated.split()
                TotalCS_list_Radiated = TotalCS_line_Radiated.split()
                RC_Fact_list_Radiated = RC_Fact_line_Radiated.split()
                
                BornCS__Radiated = float(BornCS__list_Radiated[len(BornCS__list_Radiated) - 1])
                if(BornCS__Radiated != BornCS__NRadiate):
                    print(f"{color.Error}The Born Cross Sections Do Not Aggree...{color.END}")
                    print(f"{color.RED}BornCS__Radiated = {BornCS__Radiated}{color.END}")
                    print(f"{color.RED}BornCS__NRadiate = {BornCS__NRadiate}{color.END}\n")
    
                TotalCS_Radiated = TotalCS_list_Radiated[len(TotalCS_list_Radiated) - 1]
                RC_Fact_Radiated = RC_Fact_list_Radiated[len(RC_Fact_list_Radiated) - 1]
            else:
                BornCS__Radiated = CSnRad_nRadiated
                TotalCS_Radiated = TotalCS_NRadiate
                RC_Fact_Radiated = RC_Fact_NRadiate
            return [BornCS__Radiated, BornCS__NRadiate, TotalCS_Radiated, TotalCS_NRadiate, Total_Error_NRad, RC_Fact_Radiated, RC_Fact_NRadiate]
        else:
            # Updated on 2/4/2026
            value_by_key, unc_by_key = parse_nradiate_output(NRadiate_text_output=NRadiate_output)
            if((args.modulation_mode in [0]) and (args.inject_mods and (None not in [Q2yBin, zpTBin]))):
                RC_new_list, cs_born_new_list, cs_tot_new_list = calc_rc_new_from_json(json_file_1=args.json_born, json_file_2=args.json_mods, Q2Y_Bin=Q2yBin, z_pT_Bin=zpTBin, phi_h=phi_h_CS, cs_nrad_in=[value_by_key.get("σ_nrad"), unc_by_key.get("σ_nrad")], cs_AMM_in=[value_by_key.get("σ_AMM"), unc_by_key.get("σ_AMM")], cs_rad_f_in=[value_by_key.get("σ_rad_f"), unc_by_key.get("σ_rad_f")],  cs_rad_in=[value_by_key.get("σ_rad"), unc_by_key.get("σ_rad")], cs_born_in=[value_by_key.get("σ_B"), unc_by_key.get("σ_B")], verbose=verbose)
                if(RC_new_list      is not None):
                    value_by_key["RC"],    unc_by_key["RC"]    = RC_new_list
                if(cs_born_new_list is not None):
                    value_by_key["σ_B"],   unc_by_key["σ_B"]   = cs_born_new_list
                if(cs_tot_new_list  is not None):
                    value_by_key["σ_tot"], unc_by_key["σ_tot"] = cs_tot_new_list
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
        
def Scan_RC_in_Bins(Q2_y_Bin, z_pT_Bin, phi_h_Bin, phi_s_Set, k0_cut_Set, verbose=True, Num_of_SubBins=10):
    Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y_Bin}, Q2-y']
    z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}']        
    
    Q2_increment = (Q2_max - Q2_min)/Num_of_SubBins
    y_increment  =  (y_max -  y_min)/Num_of_SubBins
    z_increment  =  (z_max -  z_min)/Num_of_SubBins
    pT_increment = (pT_max - pT_min)/Num_of_SubBins

    phi_h_scan_list = phi_h_RADIAN_Scan_Bin(phi_h_Bin)
    y_min_true  = y_min
    z_min_true  = z_min
    pT_min_true = pT_min

    Q2_loop_num, y_loop_num, z_loop_num, pT_loop_num = 0, 0, 0, 0
    CS__nRad_List, Born__CS_List, Total_CS_List, RC_Fact__List = [], [], [], []
    CS__nRad_Lerr, Born__CS_Lerr, Total_CS_Lerr, RC_Fact__Lerr = [], [], [], []
    CS_AMM___List, CS_radf__List, CS_rad___List                = [], [], []
    CS_AMM___Lerr, CS_radf__Lerr, CS_rad___Lerr                = [], [], []
    while(round(Q2_min, 4)               <= round(Q2_max, 4)):
        # if(verbose):
        Q2_loop_num += 1
        print(f"\tCurrent Q2 increment = {Q2_min:>7.4f} ({color.BBLUE}{Q2_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
        y_min, y_loop_num = y_min_true, 0
        while(round(y_min, 4)            <=  round(y_max, 4)):
            y_loop_num += 1
            if(verbose):
                print(f"\t\tCurrent y increment = {y_min:>7.4f} ({color.BBLUE}{y_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
            z_min, z_loop_num = z_min_true, 0
            while(round(z_min, 4)        <=  round(z_max, 4)):
                z_loop_num += 1
                if(verbose):
                    print(f"\t\t\tCurrent z increment = {z_min:>7.4f} ({color.BBLUE}{z_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                pT_min, pT_loop_num = pT_min_true, 0
                while(round(pT_min, 4)   <= round(pT_max, 4)):
                    pT_loop_num += 1
                    if(verbose):
                        print(f"\t\t\t\tCurrent pT increment = {pT_min:>7.4f} ({color.BBLUE}{pT_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                    for phi_h_loop_num, phi_h in enumerate(phi_h_scan_list):
                        if(verbose):
                            print(f"\t\t\t\t\tCurrent phi_h increment = {phi_h*ROOT.TMath.RadToDeg():>7.4f} degrees ({color.BBLUE}{phi_h_loop_num+1}{color.END_B} of {color.BGREEN}{len(phi_h_scan_list)}{color.END})")
                        try:
                            value_by_key, unc_by_key = Calc_RC_Factor(str(Q2_min), str(y_min), str(z_min), str(pT_min), str(phi_h), str(phi_s_Set), str(k0_cut_Set), verbose=verbose)
                            CS_nRad_NRadiate = value_by_key.get("σ_nrad")
                            BornCS__NRadiate = value_by_key.get("σ_B")
                            TotalCS_NRadiate = value_by_key.get("σ_tot")
                            RC_Fact_NRadiate = value_by_key.get("RC")
                            CS_AMM__NRadiate = value_by_key.get("σ_AMM")
                            CS_radf_NRadiate = value_by_key.get("σ_rad_f")
                            CS_rad__Radiated = value_by_key.get("σ_rad")
                        except:
                            CS_nRad_NRadiate, BornCS__NRadiate, _, TotalCS_NRadiate, _, _, RC_Fact_NRadiate = Calc_RC_Factor(str(Q2_min), str(y_min), str(z_min), str(pT_min), str(phi_h), str(phi_s_Set), str(k0_cut_Set), verbose=verbose)
                            CS_AMM__NRadiate, CS_radf_NRadiate, CS_rad__Radiated = 0.0, 0.0, 0.0
                            value_by_key = {"σ_nrad": 0.0, "σ_B": 0.0, "σ_tot": 0.0, "RC": 0.0, "σ_AMM": 0.0, "σ_rad_f": 0.0, "σ_rad": 0.0}
                        if(None in [BornCS__NRadiate, TotalCS_NRadiate, RC_Fact_NRadiate, CS_AMM__NRadiate, CS_radf_NRadiate, CS_rad__Radiated]):
                            print("Scanning 'Calc_RC_Factor' returned 'None'...")
                            break
                        Born__CS_List.append(float(BornCS__NRadiate))
                        Total_CS_List.append(float(TotalCS_NRadiate))
                        RC_Fact__List.append(float(RC_Fact_NRadiate))
                        CS__nRad_List.append(float(CS_nRad_NRadiate))
                        CS_AMM___List.append(float(CS_AMM__NRadiate))
                        CS_radf__List.append(float(CS_radf_NRadiate))
                        CS_rad___List.append(float(CS_rad__Radiated))

                        Born__CS_Lerr.append(float(unc_by_key.get("σ_B"))     if(unc_by_key.get("σ_B")     is not None) else 0.0)
                        Total_CS_Lerr.append(float(unc_by_key.get("σ_tot"))   if(unc_by_key.get("σ_tot")   is not None) else 0.0)
                        RC_Fact__Lerr.append(float(unc_by_key.get("RC"))      if(unc_by_key.get("RC")      is not None) else 0.0)
                        CS__nRad_Lerr.append(float(unc_by_key.get("σ_nrad"))  if(unc_by_key.get("σ_nrad")  is not None) else 0.0)
                        CS_AMM___Lerr.append(float(unc_by_key.get("σ_AMM"))   if(unc_by_key.get("σ_AMM")   is not None) else 0.0)
                        CS_radf__Lerr.append(float(unc_by_key.get("σ_rad_f")) if(unc_by_key.get("σ_rad_f") is not None) else 0.0)
                        CS_rad___Lerr.append(float(unc_by_key.get("σ_rad"))   if(unc_by_key.get("σ_rad")   is not None) else 0.0)
                    pT_min += pT_increment
                    print(f"\t\t\t\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
                z_min += z_increment
                print(f"\t\t\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
                # break
            y_min += y_increment
            print(f"\t\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
            # break
        Q2_min += Q2_increment
        print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
        # break
    timer.time_elapsed()

    def AveAndErr(_List, _Lerr):
        _Ave      = sum(_List)/len(_List)  # Average
        # Scatter (RMS / sqrt(N))
        _arr      = array('d', _List)
        _Scatt    = ROOT.TMath.RMS(len(_arr), _arr) / ROOT.TMath.Sqrt(len(_arr))
        # Measurement ((sqrt(sum(u^2)))/N) if provided and same length; else 0
        if((len(_Lerr) != 0) and (len(_Lerr) == len(_List))):
            _Meas = ROOT.TMath.Sqrt(sum(u**2 for u in _Lerr)) / (len(_Lerr))
        else:
            _Meas = 0.0
        _Err      = ROOT.TMath.Sqrt((_Meas**2) + (_Scatt**2)) # Combined
        return _Ave, _Err

    Born__CS_Ave, Born__CS_Err = AveAndErr(Born__CS_List, Born__CS_Lerr)
    Total_CS_Ave, Total_CS_Err = AveAndErr(Total_CS_List, Total_CS_Lerr)

    nRad__CS_Ave, nRad__CS_Err = AveAndErr(CS__nRad_List, CS__nRad_Lerr)

    RC_Fact__Ave, RC_Fact__Err = AveAndErr(RC_Fact__List, RC_Fact__Lerr)

    AMM___CS_Ave, AMM___CS_Err = AveAndErr(CS_AMM___List, CS_AMM___Lerr)
    radf__CS_Ave, radf__CS_Err = AveAndErr(CS_radf__List, CS_radf__Lerr)
    rad___CS_Ave, rad___CS_Err = AveAndErr(CS_rad___List, CS_rad___Lerr)
    
    True_RC_for_Bin        = Total_CS_Ave/Born__CS_Ave
    True_RC_for_Bin_Err    = True_RC_for_Bin * ROOT.TMath.Sqrt((Total_CS_Err / Total_CS_Ave)**2 + (Born__CS_Err  / Born__CS_Ave)**2)
    if(args.inject_mods):
        RC_new_list, cs_born_new_list, cs_tot_new_list = calc_rc_new_from_json(json_file_1=args.json_born, json_file_2=args.json_mods, Q2Y_Bin=Q2_y_Bin, z_pT_Bin=z_pT_Bin, phi_h=phi_h_scan_list[1], cs_nrad_in=[nRad__CS_Ave, nRad__CS_Err], cs_AMM_in=[AMM___CS_Ave, AMM___CS_Err], cs_rad_f_in=[radf__CS_Ave, radf__CS_Err], cs_rad_in=[rad___CS_Ave, rad___CS_Err], cs_born_in=[Born__CS_Ave, Born__CS_Err], verbose=verbose)
        if(RC_new_list      is not None):
            True_RC_for_Bin, True_RC_for_Bin_Err = RC_Fact__Ave, RC_Fact__Err
            RC_Fact__Ave,    RC_Fact__Err = RC_new_list
        if(cs_born_new_list is not None):
            Born__CS_Ave,    Born__CS_Err = cs_born_new_list
        if(cs_tot_new_list  is not None):
            Total_CS_Ave,    Total_CS_Err = cs_tot_new_list
    return [Born__CS_Ave, Born__CS_Err, Total_CS_Ave, Total_CS_Err, True_RC_for_Bin, True_RC_for_Bin_Err, RC_Fact__Ave, RC_Fact__Err]

# =========================
# Plotting RC Cosine Fits
# =========================

def plot_RC_Cos_fits(entries, canvas_In, args_In, SAVE_NAME, Other_ROOT_Save_Items=[None]):
    # entries:      list of (slice_title, RC_cos_phi, RC_cos_2phi) tuples
    # canvas_In:    your TCanvas (pads 3 & 4 must be free)
    # args_In:      arguements from rest of code
    # SAVE_NAME:    file name for the image to be saved
    first_title = entries[0][0]
    var_name = first_title.split('=')[0].strip()
    print(f"{color.BBLUE}\nMaking RC Cosine vs {var_name} Plots{color.END}\n")
    xs, ys1, ys2  = [], [], []
    for slice_title, phi1, phi2 in entries:
        # slice_title is like "z = 0.4"
        _, _, val = slice_title.partition('=')
        x_val = float(val.strip())
        xs.append(x_val)
        ys1.append(phi1)
        ys2.append(phi2)
    n = len(xs)
    # make C arrays
    x  = array('d', xs)
    y1 = array('d', ys1)
    y2 = array('d', ys2)
    # --- DRAW ---
    pad3 = canvas_In.cd(3)
    pad3.SetGrid()
    pad3.SetLeftMargin(0.15)     # make room for the y‐axis title
    pad3.SetRightMargin(0.05)
    g1 = ROOT.TGraph(n, x, y1)
    g1.SetTitle(f"RC Cos(#phi) vs {var_name}; {var_name}; RC Cos(#phi)")
    g1.SetMarkerStyle(20)
    g1.Draw("ALP")

    pad4 = canvas_In.cd(4)
    pad4.SetGrid()
    pad4.SetLeftMargin(0.15)     # make room for the y‐axis title
    pad4.SetRightMargin(0.05)
    g2 = ROOT.TGraph(n, x, y2)
    g2.SetTitle(f"RC Cos(2#phi) vs {var_name}; {var_name}; RC Cos(2#phi)")
    g2.SetMarkerStyle(21)
    g2.Draw("ALP")

    canvas_In.Modified()
    canvas_In.Update()
    canvas_In.SaveAs(SAVE_NAME)
    if(args_In.root):
        if(".root" not in str(args_In.root)):
            print(f"{color.Error}WARNING: Include '.root' in '--root' argument (adding it by default now){color.END}\n")
            args_In.root = f"{args_In.root}.root"
        print(f"\n{color.BGREEN}CREATING/UPDATING ROOT FILE: {color.END_B}{args_In.root}\n{color.END}")
        Full_Graph_Names = f"{var_name}_{f'Q2_y_Bin_{args_In.Q2_y_bin}_' if(args_In.Q2_y_bin) else ''}in_{'pT' if('z' in str(var_name)) else 'z'}_slice_{args_In.pT_group if('z' in str(var_name)) else args_In.z_group}"
        g1.SetName(f"RC_Cos_phi_vs_{Full_Graph_Names}")
        g2.SetName(f"RC_Cos_2phi_vs_{Full_Graph_Names}")
        rootfile = ROOT.TFile(args_In.root, "UPDATE")
        rootfile.cd()
        g1.Write()
        g2.Write()
        canvas_In.SetName(SAVE_NAME)
        canvas_In.Write()
        if(Other_ROOT_Save_Items != [None]):
            Saving_MultiGraph, Saving_Legend, Saving_Latex = Other_ROOT_Save_Items
            Saving_MultiGraph.SetName(f"TMultiGraph_from_{SAVE_NAME}")
            Saving_Legend.SetName(f"TLegend_from_{SAVE_NAME}")
            Saving_Latex.SetName(f"TLatex_from_{SAVE_NAME}")
            Saving_MultiGraph.Write()
            Saving_Legend.Write()
            Saving_Latex.Write()
        rootfile.Close()
        print(f"{color.CYAN}Done making the ROOT file{color.END}")
    return canvas_In

# =========================
# TTree Plot Creation
# =========================

def create_TGraph_from_TTree(tree, yvar="RC_factor", Q2_y_Bin=1, z_pT_Bin=1, cut_string="Ave_Cen_Ind == -1", canvas_Q=False):
    graph      = ROOT.TGraphErrors()
    KinBin_cut = f"(Q2_y_Bin == {Q2_y_Bin}) && (z_pT_Bin == {z_pT_Bin})"
    KinBin_cut = f"{KinBin_cut} && ({cut_string})" if(cut_string) else KinBin_cut
    Plot_Title = f"Title;#phi_{{h}}; {yvar}"
    graph.SetTitle(Plot_Title)
    if(canvas_Q):
        canvas = ROOT.TCanvas("c1", "RC Factor Plot With Momement Fits", 1200, 1200)
        canvas.Divide(1, 2)
        canvas_cd_1 = canvas.cd(1)
        canvas_cd_1.Divide(2, 1)
        canvas_cd_1.cd(1)
        hist2D = (tree.Filter(KinBin_cut)).Histo2D(("hist2d", Plot_Title, 48, 0, 360, 150, 0.0, 1.5), "phi_h", yvar)
        hist2D.Draw("COLZ same")
        canvas_cd_2 = canvas.cd(2)
        canvas_cd_2.Divide(6, 4)
    hist = {}
    for phi_h_bin in range(1, 25):
        bin_cut = f"(phi_h > {15*(phi_h_bin-1)}) && (phi_h < {15*phi_h_bin})"
        full_cut = f"({bin_cut}) && ({KinBin_cut})"
        hist[f"phi_h_bin_{phi_h_bin}"] = (tree.Filter(full_cut)).Histo1D((f"hist_phi_h_bin_{phi_h_bin}", f"#phi_{{h}} Bin {phi_h_bin}", 150, 0.0, 1.5), yvar)
        if(canvas_Q):
            canvas_cd_2.cd(phi_h_bin)
            hist[f"phi_h_bin_{phi_h_bin}"].Draw("Hist same")
        if(hist[f"phi_h_bin_{phi_h_bin}"].GetEntries() < 2):
            continue
        mean = hist[f"phi_h_bin_{phi_h_bin}"].GetMean()
        err  = hist[f"phi_h_bin_{phi_h_bin}"].GetRMS()  # You could use GetMeanError() if preferred
        xval = 7.5 + (15*(phi_h_bin-1))
        xerr = 0 # 7.5
        graph.SetPoint(graph.GetN(), xval, mean)
        graph.SetPointError(graph.GetN()-1, xerr, err)
    graph.SetMarkerStyle(2)
    graph.SetMarkerSize(2)
    graph.SetLineWidth(2)
    graph.SetLineColor(ROOT.kBlue)
    graph.GetXaxis().SetRangeUser(0, 360)
    graph.GetYaxis().SetRangeUser(0, 1.5)
    if(canvas_Q):
        canvas.Modified()
        canvas.Update()
        canvas_cd_1.cd(2)
        graph.Draw("APL same")
        canvas.Draw()
        canvas.Modified()
        canvas.Update()
        return canvas, graph, hist, hist2D
    else:
        return graph

# =========================
# Argument Parsing
# =========================

def parse_args():
    parser = argparse.ArgumentParser(description="Create Plots from the 'cross_section.cpp' example EvGen code with RC Factor/Cross Section Values being plotted as functions of the kinematic variables used to calculate them.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--plot",                 type=str,   default="RC",    choices=["RC", "rc", "BORN", "born", "totalcs", "nrad", "sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"],
                        help="The name of the calculated value to be plotted. The 'sf_cos' and 'sf_cos2' options are for the F_UU structure functions for the cos(phi) and cos(2phi) terms (the '_sel' and '_pro' suffixes correspond to the 'Selected' and 'Prokudin' versions of these functions—used to compare the modified structure functions with EvGen's default values)")
    parser.add_argument("-v", "--variable",             type=str,   default="phi_h", choices=["Q2", "y", "z", "pT", "phi_h", "phi_s", "k0_cut"],
                        help="Variable to plot against.")
    parser.add_argument("-q2y", "--Q2_y_bin",           type=int, 
                        help="Bin key for Q2_y Bin (required for z/pT plotting)")
    parser.add_argument("-zpt", "--z_pT_bin",           type=int, 
                        help="Bin key for z_pT Bin")
    parser.add_argument("-4d", "--Q2_y_z_pT_bin",       type=int, 
                        help="Bin key for the 4D Q2_y_z_pT Bin (converts one number to the appropriate Q2_y+z_pT bin numbers using 'Bin_Converter_4D_to_2D' - use in place of BOTH the '--Q2_y_bin' and '--z_pT_bin' arguments)")
    parser.add_argument("-5d", "--Q2_y_z_pT_phi_h_bin", type=int, 
                        help="Bin key for the 5D Q2_y_z_pT_phi_h Bin (converts one number to the appropriate Q2_y+z_pT+phi_h bin numbers, replacing the '--Q2_y_bin' and '--z_pT_bin' arguments, and setting phi_h by bin number from 1 to 12 (phi_h bins have a width of 15 degrees and have a range from 0 to 180 degrees - symmetry is assumed so that the outputs of any phi_h bin are the same as the bin phi_h_bin+12)")
    parser.add_argument("-g-Q2", "--Q2_group",          type=int,   default=1,
                        help="Group of Q2-y Bins used for plotting vs Q2")
    parser.add_argument("-g-y",   "--y_group",          type=int,   default=1,
                        help="Group of Q2-y Bins used for plotting vs y")
    parser.add_argument("-g-pT", "--pT_group",          type=int,   # default=1,
                        help="Group of z-pT Bins used for plotting vs pT (Differs based on chosen Q2_y_Bin)")
    parser.add_argument("-g-z",   "--z_group",          type=int,   # default=1,
                        help="Group of z-pT Bins used for plotting vs z (Differs based on chosen Q2_y_Bin)")
    parser.add_argument("--phi_h",                      type=float, default=0.0,
                        help="Fixed value for phi_h parameter. (Use Radians)")
    parser.add_argument("--phi_s",                      type=float, default=0.0,
                        help="Fixed value for phi_s parameter. (Use Radians)")
    parser.add_argument("--k0_cut",                     type=float, default=0.01,
                        help="Fixed value for k0_cut parameter.")
    parser.add_argument("-m", "--multiline",                        default="None",  choices=["Q2", "y", "z", "pT", "phi_h", "phi_s", "k0_cut", "None"], 
                        help="Enable multiline (TMultiGraph) plotting versus the given variable ('None' option is the default 'off' input).")
    parser.add_argument("-u-z-pT", "--use_z_pT_groups",             action='store_true',
                        help="Use z-pT Bin groups when plotting with the 'multiline' option.")
    parser.add_argument("-n", "--name",                 type=str,
                        help="Add extra parts to the output file's name (format: f'{plot_choice}_vs_{plot_var}.png' -> f'{plot_choice}_vs_{plot_var}_{extra_name}.png')")
    parser.add_argument("-t", "--title",                type=str,
                        help="Add extra parts to the output plot's title.")
    parser.add_argument("-q", "--quiet",                            action='store_true',
                        help="Minimizes number of print statements shown while running.")
    parser.add_argument("-nf", "--no_file",                         action='store_true',
                        help="Skips the plot/file create (use to just see the numerical inputs/outputs).")
    parser.add_argument("-ud", "--use_degrees",                     action='store_true',
                        help="Report numbers in Degrees instead of Radians when plotting (does not effect the numbers being inputted into the calculations, so still use radians when inputting fixed values for the angles).")
    parser.add_argument("-pdf", "--pdf",                            action='store_true',
                        help="Use PDF format for images instead of PNG.")
    parser.add_argument("-f", "--fit",                              action='store_true',
                        help="Fits the phi_h plots with functions of the form: A*(1 + B*cos(phi_h) + C*cos(2*phi_h))")
    parser.add_argument("-s", "--scan",                             action='store_true',
                        help="Scans through kinematic bins to get the average RC factor for the bin instead of just taking it from a fixed center (requires use of kinematic bin ranges)")
    parser.add_argument("-sn", "--scan_num",            type=int,   default=10,
                        help="Number of bins to scan through whe the '--scan' argument is used.")
    parser.add_argument("-fm", "--fit_moments",                     action='store_true',
                        help="When using the '--fit' and '--multiline' options, this option will add the plots of fitted moments as functions of the multiline variable")
    parser.add_argument("-r", "--root",                 type=str,
                        help="When using the '--fit_moments' option, this option will also create/update a ROOT file (given by the user) which will contain the 'fit_moments' plots for later use/overlapping")
    parser.add_argument("-ttree", "--ttree",                        action='store_true',
                        help="Generate a TTree ROOT file instead of images. Runs for only a single 5D kinematic bin at a time. Requires the following arguments: '-5d'/'--Q2_y_z_pT_phi_h_bin' for kinematic bin (does not accept other bin arguments) AND '--root' for output file name")
    parser.add_argument("-uj", "--use_json",                        action='store_true',
                        help="Can be used with the '--fit' option to save the fit parameters to a JSON file for future use.")
    parser.add_argument("-json", "--json_file",         type=str,   default="Fit_Parameters_for_RC.json",
                        help="Name of JSON file to be saved to if the '--use_json' option is used. Will interact with the '--name' argument.")#JSON
    parser.add_argument("-inj", "--inject_mods",                    action='store_true',
                        help="Use this option to reweigh the Born-level cross section to inject the measured modulation taken from the unfolded data.")
    parser.add_argument("-jb", "--json_born",           type=str,   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code/Fit_Parameters_for_RC.json",
                        help="Name of JSON file to be used to give the initial Born-level modulations if the '--inject_mods' option is used.")
    parser.add_argument("-jm", "--json_mods",           type=str,   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json",
                        help="Name of JSON file to be used to give the measured modulations to be injected if the '--inject_mods' option is used.")
    parser.add_argument("-mm", "--modulation_mode",     type=int,   default=0,       choices=[0, 1, 2],
                        help="Modulation controls for using EvGen structure function groups ('0'->default EvGen structure functions, '1'->turns off modulations to be more like clasdis, and '2'->replaces the modulations in option '0' with the ones I measured).")
    
    return parser.parse_args()


def default_ranges(plot_var_In, args_In):
    # Choose plotting range
    find_range         = None
    if(plot_var_In     == "Q2"):
        find_range     = [round(2     + 1.18*ii,   5) for ii in range(6)]
        if(args_In.Q2_group):
            find_range = Q2_y_z_pT_Bin_rows_function("Q2", args_In.Q2_group, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
    elif(plot_var_In   == "y"):
        find_range     = [round(0.35  + 0.04*ii,   5) for ii in range(11)]
        if(args_In.y_group):
            find_range = Q2_y_z_pT_Bin_rows_function("y",   args_In.y_group, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
    elif(plot_var_In   == "z"):
        find_range     = [round(0.1   + 0.1*ii,    5) for ii in range(8)]
        if(args_In.z_group):
            find_range = Q2_y_z_pT_Bin_rows_function("z",   args_In.z_group, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
            # if(not args_In.quiet):
            print(f"{color.GREEN}Range for z group {args_In.z_group} = {color.END_B}{find_range}{color.END}")
        elif(args_In.use_z_pT_groups):
            find_range = Q2_y_z_pT_Bin_rows_function("z",   1, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
            # if(not args_In.quiet):
            print(f"{color.GREEN}Range for z  = {color.END_B}{find_range}{color.END}")
    elif(plot_var_In   == "pT"):
        find_range     = [round(0.1   + 0.1*ii,    5) for ii in range(8)]
        if(args_In.pT_group):
            find_range = Q2_y_z_pT_Bin_rows_function("pT", args_In.pT_group, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
            # if(not args_In.quiet):
            print(f"{color.GREEN}Range for pT group {args_In.pT_group} = {color.END_B}{find_range}{color.END}")
        elif(args_In.use_z_pT_groups):
            find_range = Q2_y_z_pT_Bin_rows_function("pT",  1, Q2_y_Bin=args_In.Q2_y_bin, Output_Q="Centers" if(not args_In.scan) else "Range")
            # if(not args_In.quiet):
            print(f"{color.GREEN}Range for pT = {color.END_B}{find_range}{color.END}")
    elif(plot_var_In   == "k0_cut"):
        find_range     = [round(0.001 + 0.005*ii, 5) if(ii < 20) else round((0.1*(ii-19)), 5) for ii in range(29)]
    elif((args_In.use_degrees) and (plot_var_In in ["phi_h", "phi_s"])):
        find_range     = [((ii * 15) if(ii*15 <= 180) else ((ii*15) - 360))*ROOT.TMath.DegToRad() for ii in range(24)]  # -π to π radians in 15° steps in an order designed to be converted to a range of 0 to 360 degrees
        find_range.append(-1*ROOT.TMath.DegToRad()) # adds a point at -1 degrees (converted to radians) to get a point for 359 degrees in the final plot (the shift method used sets the point for 360 to 0, so appending this point at 359 is the closest way to get this full distribution)
    elif(plot_var_In in ["phi_h", "phi_s"]):
        find_range     = [((ii * 15)-180)*ROOT.TMath.DegToRad() for ii in range(25)]  # -π to π radians in 15° steps
    elif(find_range    == None):
        print(f"{color.Error}Unknown variable to plot.{color.END}")
        sys.exit(1)
    if(None in find_range):
        find_range.remove(None)
    return find_range
    
# =========================
# Plot Generation
# =========================

def make_plot(args):
    print(f"\n\n{color.BOLD}Starting 'make_plot' function...{color.END}\n\n")
    if(args.variable in args.multiline):
        print(f"{color.Error}Input variable ({args.variable}) should not be in the 'multiline' variable(s) ({args.multiline}).\nChange your inputs and run again.{color.END}\n")
        sys.exit(1)
    # Define the variable to plot
    plot_var       = args.variable
    # Define the value to be plotted
    plot_choice    = args.plot.lower()

    if(args.scan and (plot_var not in ["phi_h"])):
        print(f"\n{color.Error}WARNING: '--scan' argument assumes that the variable given is 'phi_h' --> Will give error at this time, so killing run...{color.END}\n")
        return
    if(args.scan and ("sf_cos" in str(plot_choice))):
        print(f"\n{color.Error}WARNING: '--scan' has not been set up (yet) to run for the structure function plots.{color.END}\n")
        return
    if(args.Q2_y_z_pT_bin):
        print(f"\n{color.BBLUE}Setting the Q2-y and z-pT bins with the 4D Bin Number: {color.END_B}{args.Q2_y_z_pT_bin}{color.END}")
        args.Q2_y_bin, args.z_pT_bin = Bin_Converter_4D_to_2D[f"Q2_y_z_pT_bin_{args.Q2_y_z_pT_bin}"]
        print(f"\n{color.BGREEN}Running with (Q2-y, z-pT) bin = {color.END_B}{color.UNDERLINE}({args.Q2_y_bin}, {args.z_pT_bin}){color.END}")
    if(args.z_pT_bin):
        if(f"Q2-y={args.Q2_y_bin}, z-pT={args.z_pT_bin}" not in Full_Bin_Definition_Array):
            print(f"\n{color.Error}WARNING: Given Kinematic Bin ('Q2-y={args.Q2_y_bin}, z-pT={args.z_pT_bin}') is not defined in 'Full_Bin_Definition_Array'. MUST SKIP THIS SELECTION...{color.END}")
            if(args.Q2_y_z_pT_bin):
                print(f"{color.BOLD}The above bin corresponsed to the 4D Q2-y-z-pT bin number {color.UNDERLINE}{args.Q2_y_z_pT_bin}{color.END}")
            print("\n\nEnding Run...\n")
            return

    output_file_type = ".pdf" if(args.pdf) else ".png"
    Save_Name = "ERROR"
    if(plot_choice == "rc"):
        plot_print_str = "RC"
        Save_Name = f"RC_Factor_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "totalcs"):
        plot_print_str = "CS tot"
        Save_Name = f"Total_Cross_Section_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "born"):
        plot_print_str = "CS Born"
        Save_Name = f"Born_Cross_Section_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "nrad"):
        plot_print_str = "CS nonrad"
        Save_Name = f"Non_Radiated_Cross_Section_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "sf_cos_sel"):
        plot_print_str = "Selected SF Cos(phi)"
        Save_Name = f"Selected_SF_Cosphi_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "sf_cos2_sel"):
        plot_print_str = "Selected SF Cos(2phi)"
        Save_Name = f"Selected_SF_Cos2phi_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "sf_cos_pro"):
        plot_print_str = "Default SF Cos(phi)"
        Save_Name = f"Default_SF_Cosphi_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "sf_cos2_pro"):
        plot_print_str = "Default SF Cos(2phi)"
        Save_Name = f"Default_SF_Cos2phi_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "fit_b"):
        plot_print_str = "(Pre-determined) Cos(phi) Moment"
        Save_Name = f"Calc_Cosphi_vs_{plot_var}{output_file_type}"
    elif(plot_choice == "fit_c"):
        plot_print_str = "(Pre-determined) Cos(2phi) Moment"
        Save_Name = f"Calc_Cos2phi_vs_{plot_var}{output_file_type}"
    if(args.Q2_y_bin is not None):
        Save_Name = Save_Name.replace(output_file_type, f"_Q2_y_Bin_{args.Q2_y_bin}{output_file_type}")
    if(args.z_pT_bin is not None):
        Save_Name = Save_Name.replace(output_file_type, f"_z_pT_Bin_{args.z_pT_bin}{output_file_type}")
    if(args.name):
        Save_Name = Save_Name.replace(output_file_type, f"_{args.name}{output_file_type}")
    if(Save_Name in ["ERROR"]):
        print(f"{color.ERROR}Can't run due to error in Save_Name input{color.END}")
        return None
    if(args.scan):
        Save_Name = f"Scanned_Bins_{Save_Name}"
        print(f"\n{color.Error}Scanning Bins for Calculations (i.e., taking average cross sections from across the given kinematic bins to get the RC Factors).{color.END}")
    if(args.pdf):
        print(f"\n{color.Error}Using PDF Format for output images.{color.END}\n")
    print(f"{color.CYAN}Starting to make the plot(s) for file: {color.END_B}{Save_Name}{color.END}\n")

    # Defining the variable/value titles
    plot_var_title = variable_Title_name_new(plot_var)
    otherVar_Title = "RC Factor" if(plot_choice in ["rc"]) else "#sigma_{Total}" if(plot_choice in ["totalcs"]) else "#sigma_{Born}" if(plot_choice == "born") else "#sigma_{non-rad}" if(plot_choice == "nrad") else "ERROR"
    if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro"]):
        otherVar_Title = f"{'' if('_sel' in plot_choice) else '(EvGen-Default) '}F_{{UU}}^{{{'cos(#phi)' if('cos_' in plot_choice) else 'cos(2#phi)'}}}"
    if(plot_choice in ["fit_b", "fit_c"]):
        otherVar_Title = f"Pre-Determined Fit Parameter {'cos(#phi)' if('fit_b' in plot_choice) else 'cos(2#phi)'}"
    x_vals, y_vals, x_errs, y_errs, MultiLine_range = {}, {}, {}, {}, {}

    # Get fixed values for other variables
    Q2, y  = get_bin_centers("Q2_y", args.Q2_y_bin)                                                 if(args.Q2_y_bin is not None)  else [2.2,     0.7]
    pT, z  = get_bin_centers("z_pT", args.Q2_y_bin, args.z_pT_bin) if((args.z_pT_bin is not None) and (args.Q2_y_bin is not None)) else [0.555, 0.135]
    phi_h  = args.phi_h
    phi_s  = args.phi_s
    k0_cut = args.k0_cut

    if(("z"  not in args.multiline) and (str(plot_var) not in  ["z"]) and  (args.z_group)):
        z  = Q2_y_z_pT_Bin_rows_function("z",  1, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")[args.z_group - 1]  # 1 is used in the function instead of args.z_group because that row always has the full set of z bins, so there will not be an issue with '[args.z_group - 1]' grabbing and entry from the list that is a 'migration' (i.e., skipped/undefined) bin
        print(f"\n{color.BBLUE}Setting z  = {z} based on bin grouping{color.END}\n")
        Save_Name = Save_Name.replace(output_file_type, f"_z_Row_{args.z_group}{output_file_type}")
    if(("pT" not in args.multiline) and (str(plot_var) not in ["pT"]) and (args.pT_group)):
        pT = Q2_y_z_pT_Bin_rows_function("pT", 2, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")[args.pT_group - 1] # 2 is used in the function instead of args.pT_group because that row always has the full set of pT bins, so there will not be an issue with '[args.pT_group - 1]' grabbing and entry from the list that is a 'migration' (i.e., skipped/undefined) bin
        print(f"\n{color.BBLUE}Setting pT = {pT} based on bin grouping{color.END}\n")
        Save_Name = Save_Name.replace(output_file_type, f"_pT_Row_{args.pT_group}{output_file_type}")

    Q2, y  = round(Q2, 5), round(y, 5)
    pT, z  = round(pT, 5), round(z, 5)

    # Choose plotting range
    x_range = default_ranges(plot_var, args)
    if("None" not in args.multiline):
        if(isinstance(args.multiline, list)):
            for ii in args.multiline:
                MultiLine_range[ii] = default_ranges(ii, args)
        else:
            MultiLine_range[args.multiline] = default_ranges(args.multiline, args)
    else:
        MultiLine_range[args.multiline] = [None]

    for MultiLine_Var in MultiLine_range:
        if("None" not in args.multiline):
            print(f"Performing calculations of '{plot_choice} vs {plot_var}' in slices of {MultiLine_Var}")
            Save_Name_Full = Save_Name.replace(output_file_type, f"_slices_of_{MultiLine_Var}{output_file_type}")
            print(f"{color.Error}New Save Name: {color.END_B}{Save_Name_Full}{color.END}")
        else:
            Save_Name_Full = Save_Name
        if((plot_var in ["phi_h"]) and (args.fit) and ("Fit_" not in Save_Name_Full)):
            Save_Name_Full = f"Fit_{Save_Name_Full}"
        
        for numslice, MultiLine_Slice in enumerate(MultiLine_range[MultiLine_Var]):
                
            x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"] = []
            y_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"] = []
            x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"] = []
            y_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"] = []
            kwargs = {
              "Q2_CS":     str(Q2),
              "y_CS":      str(y),
              "z_CS":      str(z),
              "pT_CS":     str(pT),
              "phi_h_CS":  str(phi_h),
              "phi_s_CS":  str(phi_s),
              "k0_cut_CS": str(k0_cut),
              "verbose": not args.quiet
            }
            if((args.inject_mods) and (None not in [args.Q2_y_bin, args.z_pT_bin])):
                kwargs["Q2yBin"] = args.Q2_y_bin
                kwargs["zpTBin"] = args.z_pT_bin
            elif(args.inject_mods):
                print(f"\n{color.Error}WARNING: Cannot inject modulations unless a Q2-y and z-pT bin are specified in the arguments...{color.END}\n")

            if("None" not in args.multiline):
                print(f"\n{color.BOLD}Running {MultiLine_Var} Slice {color.PINK}{numslice+1:>3}{color.END_B} of {color.CYAN}{len(MultiLine_range[MultiLine_Var])}{color.END_B}... ({MultiLine_Var} = {MultiLine_Slice}){color.END}\n")
                kwargs[f"{MultiLine_Var}_CS"] = str(MultiLine_Slice) # Override the multiline variable

            if((args.use_z_pT_groups) and (MultiLine_Var in ["z", "pT"]) and (plot_var in ["z", "pT"])):
                x_range = Q2_y_z_pT_Bin_rows_function(plot_var, numslice+1, Q2_y_Bin=args.Q2_y_bin, Output_Q="Centers")
                if(None   in x_range):
                    x_range.remove(None)
                if("None" in x_range):
                    x_range.remove("None")
                print(f"{color.BLUE}New Range for {plot_var} group {numslice+1} = {color.END_B}{x_range}{color.END}")
                
            for num, x in enumerate(x_range):
                print(f"{color.BOLD}Running ({plot_var}) Point {color.BBLUE}{num+1:>3}{color.END_B} of {color.BGREEN}{len(x_range)}{color.END_B}... {color.END}({plot_var} = {x})")
                kwargs[f"{plot_var}_CS"] = str(x) # Override the plotted variable
                if(args.scan):
                    print(f"{color.Error}Running Scan{color.END}")
                    output = Scan_RC_in_Bins(Q2_y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin if(MultiLine_Var not in ["z", "pT"]) else MultiLine_Slice, phi_h_Bin=x, phi_s_Set=phi_s, k0_cut_Set=k0_cut, verbose=(not args.quiet), Num_of_SubBins=args.scan_num)
                    rc_value, rc_error = [output[0], output[1]] if(plot_choice == "born") else [output[2], output[3]] if(plot_choice == "totalcs") else [output[4], output[5]] if(plot_choice == "rc") else [output[6], output[7]] if(plot_choice == "rc_ave") else [None, None]
                    if(None in [rc_value, rc_error]):
                        print(f"{color.ERROR}Unknown plot option: {args.plot}{color.END}")
                        continue
                    rc_value, rc_error = float(rc_value), float(rc_error)
                    if(not args.quiet):
                        if(plot_choice == "rc"):
                            print(f"Average RC Factor Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "totalcs"):
                            print(f"Average Total CS Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "born"):
                            print(f"Average Born Output: {rc_value} ± {rc_error}\n")
                    if(args.use_degrees):
                        phi_deg  = ROOT.TMath.RadToDeg()*x
                        phi_deg += 7.5 # Assuming normal phi_h bin size of 15 degrees -> x is the start of the bin, so this addition shifts the x_val from the edge of the bin to its center
                        if(phi_deg < 0):
                            phi_deg += 360
                        x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(phi_deg)
                        x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(7.5)
                    else:
                        phi_rad = x + 7.5*ROOT.TMath.DegToRad()
                        if(phi_rad  > 180*ROOT.TMath.DegToRad()):
                            phi_rad += -360*ROOT.TMath.DegToRad()
                        x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(phi_rad)
                        x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(7.5*ROOT.TMath.DegToRad())
                    y_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_value)
                    y_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_error)
                else:
                    try:
                        value_by_key, unc_by_key = Calc_RC_Factor(**kwargs)
                        if(plot_choice == "rc"):
                            rc_value = float(value_by_key["RC"])
                            rc_error = _err0(unc_by_key["RC"])
                            if(not args.quiet):
                                print(f"RC Factor Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "totalcs"):
                            rc_value = float(value_by_key["σ_tot"])
                            rc_error = _err0(unc_by_key["σ_tot"])
                            if(not args.quiet):
                                print(f"Total CS Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "born"):
                            rc_value = float(value_by_key["σ_B"])
                            rc_error = _err0(unc_by_key["σ_B"])
                            if(not args.quiet):
                                print(f"Born Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "nrad"):
                            rc_value = float(value_by_key["σ_nrad"])
                            rc_error = _err0(unc_by_key["σ_nrad"])
                            if(not args.quiet):
                                print(f"CS nonRad Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "sf_cos_sel"):
                            rc_value = float(value_by_key["F_UU^cos(phi_h)_(Selected)"])
                            rc_error = _err0(unc_by_key["F_UU^cos(phi_h)_(Selected)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "sf_cos2_sel"):
                            rc_value = float(value_by_key["F_UU^cos(2phi_h)_(Selected)"])
                            rc_error = _err0(unc_by_key["F_UU^cos(2phi_h)_(Selected)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "sf_cos_pro"):
                            rc_value = float(value_by_key["F_UU^cos(phi_h)_(Prokudin)"])
                            rc_error = _err0(unc_by_key["F_UU^cos(phi_h)_(Prokudin)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "sf_cos2_pro"):
                            rc_value = float(value_by_key["F_UU^cos(2phi_h)_(Prokudin)"])
                            rc_error = _err0(unc_by_key["F_UU^cos(2phi_h)_(Prokudin)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "fit_b"):
                            rc_value = float(value_by_key["B_from_SF_(Selected)"])
                            rc_error = _err0(unc_by_key["B_from_SF_(Selected)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        elif(plot_choice == "fit_c"):
                            rc_value = float(value_by_key["C_from_SF_(Selected)"])
                            rc_error = _err0(unc_by_key["C_from_SF_(Selected)"])
                            if(not args.quiet):
                                print(f"{plot_print_str} Output: {rc_value} ± {rc_error}\n")
                        else:
                            print(f"{color.ERROR}Unknown plot option: {args.plot}{color.END}")
                            rc_value = None
                            continue
                    except:
                        output = Calc_RC_Factor(**kwargs)
                        if((output is None) or (None in output)):
                            continue
                        if(plot_choice == "rc"):
                            rc_value = float(output[6])
                            if(not args.quiet):
                                print(f"RC Factor Output: {rc_value}\n")
                        elif(plot_choice == "totalcs"):
                            rc_value = float(output[3])
                            if(not args.quiet):
                                print(f"Total CS Output: {rc_value}\n")
                        elif(plot_choice == "born"):
                            rc_value = float(output[1])
                            if(not args.quiet):
                                print(f"Born Output: {rc_value}\n")
                        elif(plot_choice == "nrad"):
                            rc_value = float(output[0])
                            if(not args.quiet):
                                print(f"CS nonRad Output: {rc_value}\n")
                        else:
                            print(f"{color.ERROR}Unknown plot option: {args.plot}{color.END}")
                            rc_value = None
                            continue
                        rc_error = 0.0
                    if((args.use_degrees) and (plot_var in ["phi_h", "phi_s"])):
                        phi_deg = ROOT.TMath.RadToDeg()*x
                        if(phi_deg < 0):
                            phi_deg += 360
                        x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(phi_deg)
                    else: 
                        x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(x)
                    y_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_value)
                    x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(0)
                    y_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_error)
                    if((plot_var in ["phi_h"]) and (plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"])):
                        print(f"\t{color.RED}Notice: SF and cosine moments don't have phi_h dependencies...{color.END}")
                        for num_ii, x_ii in enumerate(x_range):
                            if(num_ii <= num):
                                continue
                            print(f"{color.BOLD}Running ({plot_var}) Point {color.BBLUE}{num_ii+1:>3}{color.END_B} of {color.BGREEN}{len(x_range)}{color.END_B}... {color.END}({plot_var} = {x_ii})")
                            if((args.use_degrees) and (plot_var in ["phi_h", "phi_s"])):
                                phi_deg = ROOT.TMath.RadToDeg()*x_ii
                                if(phi_deg < 0):
                                    phi_deg += 360
                                x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(phi_deg)
                            else: 
                                x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(x_ii)
                            y_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_value)
                            x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(0)
                            y_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"].append(rc_error)
                        break

        if((not args.no_file) or (args.use_json)):
            Plot_Title_Full = f"{otherVar_Title} vs {plot_var_title}"
            if(args.scan):
                Plot_Title_Full = f"(Averaged over Kinematic Bins) {Plot_Title_Full}"
            if("None" not in args.multiline):
                Plot_Title_Full = f"#splitline{{{Plot_Title_Full}}}{{Plotting with Multiple Values of {variable_Title_name_new(MultiLine_Var)}}}"
            if(args.title):
                Plot_Title_Full = f"#splitline{{{Plot_Title_Full}}}{{{args.title}}}"
            if(args.pdf):
                print(f"\n{color.Error}WARNING: PDF Format Images currently do not include their main titles in the plots.{color.END}\n")
                Plot_Title_Full = ""
            Plot_Title_Full = f"{Plot_Title_Full}; {plot_var_title}; {otherVar_Title}"
            if((args.fit_moments) and (args.fit) and ("None" not in args.multiline)):
                canvas = ROOT.TCanvas("c1", "RC Factor Plot With Momement Fits", 1200, 1200)
                # split into four pads: pad 1 for the graph, pad 2 for annotations, pad 3 for Cos(phi) plots, and pad 4 for Cos(2phi) plots
                canvas.Divide(2, 2)
                Moment_Lists = []
            else:
                canvas = ROOT.TCanvas("c1", "RC Factor Plot", 1200, 600)
                # split into two horizontal pads: pad 1 for the graph, pad 2 for annotations
                canvas.Divide(2, 1)
                Moment_Lists = None
            # --- pad 1: your main graph ---
            pad1 = canvas.cd(1)
            pad1.SetGrid()
            pad1.SetLeftMargin(0.15)     # make room for the y‐axis title
            pad1.SetRightMargin(0.05)
            
            if("None" not in args.multiline):
                if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"]):
                    ymin, ymax = float("inf"), float("-inf")
                    if(plot_choice in ["fit_b", "fit_c"]):
                        ymin =  -1 if(plot_choice in ["fit_b"]) else -0.45
                        ymax = 0.2 if(plot_choice in ["fit_b"]) else  0.25
                    for vals in y_vals.values():
                        for yv in vals:
                            ymin = min(ymin, 0.8*yv if(yv > 0) else 1.2*yv)
                            ymax = max(ymax, 1.2*yv if(yv > 0) else 0.8*yv)
                else:
                    if(args.pdf):
                        ymin, ymax = float("inf"), float("-inf")
                    else:
                        ymin, ymax = 0.8, 1.4
                    for vals in y_vals.values():
                        for yv in vals:
                            ymin = min(ymin, yv)
                            ymax = max(ymax, yv)
                    ymin *= 0.9 if(args.pdf) else 0.8
                    ymax *= 1.1 if(args.pdf) else 1.2

                # 2) build a TMultiGraph and legend
                mg     = ROOT.TMultiGraph()
                legend = ROOT.TLegend(0.05, 0.05, 0.95, 0.35)
                legend.SetBorderSize(0)
                legend.SetEntrySeparation(0.15)
                base_colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
                pdf_colors  = [ROOT.kRed, ROOT.kBlue, ROOT.kMagenta, 8, 28, 30, 42, 46, 12]
                # a longer marker list so successive wraps give you new markers
                base_styles = [20, 21, 22, 23, 29, 30, 32, 33]
                # 3) loop over each slice
                for i, (slice_name, xs) in enumerate(x_vals.items()):
                    ys  = y_vals[slice_name]
                    exs = x_errs[slice_name]
                    eys = y_errs[slice_name]
                    arr_x  = array('d', xs)
                    arr_y  = array('d', ys)
                    arr_ex = array('d', exs)
                    arr_ey = array('d', eys)
                    g = ROOT.TGraphErrors(len(xs), arr_x, arr_y, arr_ex, arr_ey)
                    if(args.pdf or args.scan or (plot_var in ["phi_h"])):
                        if(i < len(pdf_colors)):
                            color_i   = pdf_colors[i % len(pdf_colors)]
                        else:
                            col0     = base_colors[(i-len(pdf_colors)) % len(base_colors)]
                            wraps    = (i-len(pdf_colors)) // len(base_colors)
                            color_i  = col0 - (wraps + 1)
                    else:
                        col0         = base_colors[i % len(base_colors)]
                        wraps        = i // len(base_colors)
                        color_i      = col0 - wraps
                    mstyle_i         = base_styles[i % len(base_styles)]
                    slice_title      = slice_name.replace(f"{MultiLine_Var}_Slice_", f"{variable_Title_name_new(MultiLine_Var)} = ")
                    g.SetLineColor(color_i)
                    g.SetMarkerColor(color_i)
                    g.SetMarkerStyle(mstyle_i)
                    g.SetLineWidth(2)
                    g.SetTitle(Plot_Title_Full)
                    g.SetName(f"Individual_Plot_{slice_name}")
                    if((plot_var in ["phi_h"]) and (args.fit)):
                        Par_A_mg, Par_Aerr_mg, Par_B_mg, Par_Berr_mg, Par_C_mg, Par_Cerr_mg = fit_phi_h_graph(g, DegOrRad=args.use_degrees, Color_Line=color_i)
                        if(not args.quiet):
                            print("")#JSON
                            print(f"\t{plot_print_str} Cos(phi_h)   = {Par_B_mg:<10.3e} ± {Par_Berr_mg:1.3e}" if(abs(Par_B_mg) < 0.01) else f"\t{plot_print_str} Cos(phi_h)   = {Par_B_mg:<10.5f} ± {Par_Berr_mg:1.3e}")
                            print(f"\t{plot_print_str} Cos(2*phi_h) = {Par_C_mg:<10.3e} ± {Par_Cerr_mg:1.3e}" if(abs(Par_C_mg) < 0.01) else f"\t{plot_print_str} Cos(2*phi_h) = {Par_C_mg:<10.5f} ± {Par_Cerr_mg:1.3e}")
                        mg.Add(g, "P")
                        if(args.use_json and (None not in [args.Q2_y_bin, args.z_pT_bin])):
                            save_fit_to_json(f"{plot_choice}_A", Par_A_mg, param_error=Par_Aerr_mg, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                            save_fit_to_json(f"{plot_choice}_B", Par_B_mg, param_error=Par_Berr_mg, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                            save_fit_to_json(f"{plot_choice}_C", Par_C_mg, param_error=Par_Cerr_mg, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                            print(f'\n{color.BGREEN}Updated and Saved: {color.BBLUE}{args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json")}{color.END}\n')
                            if(args.no_file):
                                print(f"\n{color.RED}Warning: Skipping rest of the image files creation...{color.END}")
                                continue
                        elif(args.use_json):
                            print(f"\n{color.Error}WARNING: Could not save the JSON file {color.END_R}(Must select a Q2-y/z-pT bin){color.END}\n")
                        if(args.fit_moments):
                            Moment_Lists.append((slice_title, Par_B_mg, Par_C_mg))
                    else:
                        Par_A_mg, Par_Aerr_mg, Par_B_mg, Par_Berr_mg, Par_C_mg, Par_Cerr_mg = None, None, None, None, None, None
                        mg.Add(g, "PL")
                    if(None not in [Par_B_mg, Par_C_mg]):
                        Par_B_mg_line = f"{Par_B_mg:<10.3e}" if(abs(Par_B_mg) < 0.01) else f"{Par_B_mg:>8.5f}  "
                        Par_C_mg_line = f"{Par_C_mg:<10.3e}" if(abs(Par_C_mg) < 0.01) else f"{Par_C_mg:>8.5f}  "
                        Par_B_mg_line = f"{Par_B_mg_line} #pm {Par_Berr_mg:1.3e}"
                        Par_C_mg_line = f"{Par_C_mg_line} #pm {Par_Cerr_mg:1.3e}"
                        slice_title = f"{slice_title} #topbar #scale[0.35]{{#splitline{{{otherVar_Title} Cos(#phi): {Par_B_mg_line}}}{{{otherVar_Title} Cos(2#phi): {Par_C_mg_line}}}}}"
                    legend.AddEntry(g, f"{slice_title}", "pl")

                # 4) draw the multigraph
                mg.SetTitle(Plot_Title_Full)
                mg.GetYaxis().SetRangeUser(ymin, ymax)
                mg.Draw("APL")
            else:
                graph = ROOT.TGraphErrors(len(x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"]), array('d', x_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"]), array('d', y_vals[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"]), array('d', x_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"]), array('d', y_errs[f"{MultiLine_Var}_Slice_{MultiLine_Slice}"]))
                graph.SetTitle(Plot_Title_Full)
                if(plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"]):
                    ymin, ymax = float("inf"), float("-inf")
                    if(plot_choice in ["fit_b", "fit_c"]):
                        ymin =  -1 if(plot_choice in ["fit_b"]) else -0.45
                        ymax = 0.2 if(plot_choice in ["fit_b"]) else  0.25
                    for vals in y_vals.values():
                        for yv in vals:
                            ymin = min(ymin, 0.8*yv if(yv > 0) else 1.2*yv)
                            ymax = max(ymax, 1.2*yv if(yv > 0) else 0.8*yv)
                    graph.GetYaxis().SetRangeUser(ymin, ymax)
                
                graph.SetLineColor(ROOT.kBlue)
                graph.SetMarkerColor(ROOT.kBlue)
                graph.SetMarkerStyle(20)      # solid circle
                graph.SetLineWidth(2)
                graph.Draw("ALP")

                if((plot_var in ["phi_h"]) and (args.fit)):
                    Par_A, Par_Aerr, Par_B, Par_Berr, Par_C, Par_Cerr = fit_phi_h_graph(graph, DegOrRad=args.use_degrees)
                    if(not args.quiet):#JSON
                        print(f"\t{plot_print_str} Cos(phi_h)   = {Par_B:<10.3e} ± {Par_Berr:1.3e}" if(abs(Par_B) < 0.01) else f"\t{plot_print_str} Cos(phi_h)   = {Par_B:<10.5f} ± {Par_Berr:1.3e}")
                        print(f"\t{plot_print_str} Cos(2*phi_h) = {Par_C:<10.3e} ± {Par_Cerr:1.3e}" if(abs(Par_C) < 0.01) else f"\t{plot_print_str} Cos(2*phi_h) = {Par_C:<10.5f} ± {Par_Cerr:1.3e}")
                    if(args.use_json and (None not in [args.Q2_y_bin, args.z_pT_bin])):
                        save_fit_to_json(f"{plot_choice}_A", Par_A, param_error=Par_Aerr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                        save_fit_to_json(f"{plot_choice}_B", Par_B, param_error=Par_Berr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                        save_fit_to_json(f"{plot_choice}_C", Par_C, param_error=Par_Cerr, Q2Y_Bin=args.Q2_y_bin, z_pT_Bin=args.z_pT_bin, json_file=args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json"), verbose=(not args.quiet))
                        print(f'\n{color.BGREEN}Updated and Saved: {color.BBLUE}{args.json_file if(args.name is None) else str(args.json_file).replace(".json", f"_{args.name}.json")}{color.END}\n')
                        if(args.no_file):
                            print(f"\n{color.RED}Warning: Skipping rest of the image files creation...{color.END}")
                            continue
                    elif(args.use_json):
                        print(f"\n{color.Error}WARNING: Could not save the JSON file {color.END_R}(Must select a Q2-y/z-pT bin){color.END}\n")
                else:
                    Par_A, Par_Aerr, Par_B, Par_Berr, Par_C, Par_Cerr = None, None, None, None, None, None

            if(args.no_file):
                print(f"\n{color.RED}Warning: Skipping rest of the image files creation...{color.END}")
                continue
            # --- pad 2: text annotations ---
            canvas.cd(2)
            ROOT.gPad.SetBottomMargin(0.15)
            ROOT.gPad.SetLeftMargin(0.15)
            latex = ROOT.TLatex()
            latex.SetTextSize(0.045)
            latex.DrawLatexNDC(0.1, 0.9, "Fixed Kinematic Inputs:")
            placement = 0.8
            if("Q2"    not in [MultiLine_Var, plot_var]):
                latex.DrawLatexNDC(0.1, placement, f"Q^{{2}} = {Q2:.4f} GeV^{{2}}")
                placement += -0.05
            if("xB"    not in [MultiLine_Var, plot_var]):
                latex.DrawLatexNDC(0.1, placement, f"x_{{B}} = {(Q2/(2 * 0.938 * 10.6 * y)):.4f}")
                placement += -0.05
            if("y"     not in [MultiLine_Var, plot_var]):
                latex.DrawLatexNDC(0.1, placement, f"y  = {y:.4f}")
                placement += -0.05
            if("z"     not in [MultiLine_Var, plot_var]):
                latex.DrawLatexNDC(0.1, placement, f"z  = {z:.4f}")
                placement += -0.05
            if("pT"    not in [MultiLine_Var, plot_var]):
                latex.DrawLatexNDC(0.1, placement, f"P_{{T}} = {pT:.4f} GeV")
                placement += -0.05
            if("phi_h" not in [MultiLine_Var, plot_var]):
                if(args.use_degrees):
                    phi_h_degrees = phi_h*ROOT.TMath.RadToDeg()
                    phi_h_degrees = phi_h_degrees + 360 if(phi_h_degrees < 0) else phi_h_degrees
                    latex.DrawLatexNDC(0.1, placement, f"#phi_{{h}} = {phi_h_degrees:.4f} Degrees")
                else:
                    latex.DrawLatexNDC(0.1, placement, f"#phi_{{h}} = {phi_h:.4f} Radians")
                placement += -0.05
            if("k0_cut" not in [MultiLine_Var, plot_var]):
                placement += -0.01
                latex.DrawLatexNDC(0.1, placement, f"E^{{Cutoff}}_{{#gamma}} = {k0_cut:.4f} GeV")
                placement += -0.05
            if(args.Q2_y_bin is not None):
                placement += -0.05
                latex.DrawLatexNDC(0.1, placement, f"Using Q^{{2}}-y Bin {args.Q2_y_bin}")
                placement += -0.05
            if(args.z_pT_bin is not None):
                latex.DrawLatexNDC(0.1, placement, f"Using z-P_{{T}} Bin {args.z_pT_bin}")
                placement += -0.05

            if("None" not in args.multiline):
                legend.Draw()
            elif((plot_var in ["phi_h"]) and (args.fit) and (plot_choice in ["sf_cos_sel", "sf_cos2_sel", "sf_cos_pro", "sf_cos2_pro", "fit_b", "fit_c"])):
                placement += -0.05
                latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} From Fit: ")
                placement += -0.1
                latex.DrawLatexNDC(0.1, placement, f"{Par_A:<10.3e} #pm {Par_Aerr:1.3e}" if(abs(Par_A) < 0.01) else f"{Par_A:<10.5f} #pm {Par_Aerr:1.3e}")
                placement += -0.05
            elif((plot_var in ["phi_h"]) and (args.fit)):
                placement += -0.05
                latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} Cos(#phi_{{h}})  From Fit: ")
                placement += -0.05
                latex.DrawLatexNDC(0.1, placement, f"{Par_B:<10.3e} #pm {Par_Berr:1.3e}" if(abs(Par_B) < 0.01) else f"{Par_B:<10.5f} #pm {Par_Berr:1.3e}")
                placement += -0.1
                latex.DrawLatexNDC(0.1, placement, f"{otherVar_Title} Cos(2#phi_{{h}}) From Fit: ")
                placement += -0.05
                latex.DrawLatexNDC(0.1, placement, f"{Par_C:<10.3e} #pm {Par_Cerr:1.3e}" if(abs(Par_C) < 0.01) else f"{Par_C:<10.5f} #pm {Par_Cerr:1.3e}")
                placement += -0.05
                
            print(f"\n{color.BBLUE}Saving File: {color.PINK}{Save_Name_Full}{color.END}")
            if(Save_Name not in ["ERROR"]):
                if((args.fit_moments) and Moment_Lists):
                    canvas = plot_RC_Cos_fits(entries=Moment_Lists, canvas_In=canvas, args_In=args, SAVE_NAME=Save_Name_Full, Other_ROOT_Save_Items=[mg, legend, latex])
                else:
                    if(args.root):
                        if(".root" not in str(args.root)):
                            print(f"{color.Error}WARNING: Include '.root' in '--root' argument (adding it by default now){color.END}\n")
                            args.root = f"{args.root}.root"
                        print(f"\n{color.BGREEN}CREATING/UPDATING ROOT FILE: {color.END_B}{args.root}\n{color.END}")
                        rootfile = ROOT.TFile(args.root, "UPDATE")
                        rootfile.cd()
                        canvas.SetName(Save_Name_Full)
                        canvas.Write()
                        latex.SetName(f"TLatex_from_{Save_Name_Full}")
                        latex.Write()
                        if("None" not in args.multiline):
                            mg.SetName(f"TMultiGraph_from_{Save_Name_Full}")
                            mg.Write()
                            legend.SetName(f"TLegend_from_{Save_Name_Full}")
                            legend.Write()
                        else:
                            graph.SetName(f"TGraph_from_{Save_Name_Full}")
                            graph.Write()
                        rootfile.Close()
                        print(f"{color.CYAN}Done making the ROOT file{color.END}")
                    canvas.SaveAs(Save_Name_Full)
                print(f"{color.BGREEN}File Saved.{color.END}")
            else:
                print(f"{color.Error}ERROR IN SAVING THE FILE!{color.END}")
        else:
            print(f"\n{color.RED}Chose not to create plot(s)/output file -> Done running{color.END}\n")

# =========================
# TTree Generation
# =========================

def generate_TTree_output(args):
    # Creates a ROOT file with a TTree for the events
    if(".root" not in str(args.root)):
        print(f"{color.Error}WARNING: Include '.root' in '--root' argument (adding it by default now){color.END}\n")
        args.root = f"{args.root}.root"
    filename = args.root
    if(args.name):
        filename = filename.replace(".root", f"_{args.name}.root")
    filename = filename.replace(".root", f"_5D_Bin_{args.Q2_y_z_pT_phi_h_bin}.root")

    if(f"Q2_y_z_pT_phi_h_bin_{args.Q2_y_z_pT_phi_h_bin}" not in Bin_Converter_5D):
        print(f"{color.Error}WARNING: Q2_y_z_pT_phi_h_bin_{args.Q2_y_z_pT_phi_h_bin} is not defined in 'Bin_Converter_5D' {color.END_R}(No known Q2-y/z-pT/phi_h bin for the given input){color.END}")
        return None

    root_file = ROOT.TFile(filename, "RECREATE")
    tree = ROOT.TTree("CrossSectionTree", "TTree holding cross section bin values")

    Num_of_SubBins = args.scan_num if(args.scan) else 0

    # Variables to fill
    Q2_y_Bin      = array('i', [0])
    z_pT_Bin      = array('i', [0])
    phi_h_Bin     = array('i', [0])
    Q2_center     = array('f', [0.])
    y_center      = array('f', [0.])
    xB_center     = array('f', [0.])
    z_center      = array('f', [0.])
    pT_center     = array('f', [0.])
    phi_h_center  = array('f', [0.])
    phi_s         = array('f', [0.])
    k0_cut        = array('f', [0.])
    RC_factor     = array('f', [0.])
    RC_factor_err = array('f', [0.])
    TCS           = array('f', [0.])
    TCS_err       = array('f', [0.])
    Born          = array('f', [0.])
    Born_err      = array('f', [0.])
    NSubBins      = array('i', [0])
    Ave_Cen_Ind   = array('i', [0]) # Flag for 'Averaged over bin'/'Center of bin'/'Individual bin' measurements (in that order, the flag numbers are 1, 0, and -1)
    RC_ave        = array('f', [0.]) # Used with '--scan' option to give the RC as an average of RC per scanned bin (instead of getting RC from the averaged cross section first)
    RC_ave_err    = array('f', [0.]) # (...) - Is error of above - if not a scanned bin/entry then RC_ave = RC_factor and RC_ave_err = RC_factor_err
    nrad_array    = array('f', [0.])
    nrad___err    = array('f', [0.])
    crad_array    = array('f', [0.])
    crad___err    = array('f', [0.])

    # Create branches
    tree.Branch("Q2_y_Bin",      Q2_y_Bin,      "Q2_y_Bin/I")
    tree.Branch("z_pT_Bin",      z_pT_Bin,      "z_pT_Bin/I")
    tree.Branch("phi_h_Bin",     phi_h_Bin,     "phi_h_Bin/I")
    tree.Branch("Q2",            Q2_center,     "Q2/F")
    tree.Branch("y",             y_center,      "y/F")
    tree.Branch("xB",            xB_center,     "xB/F")
    tree.Branch("z",             z_center,      "z/F")
    tree.Branch("pT",            pT_center,     "pT/F")
    tree.Branch("phi_h",         phi_h_center,  "phi_h/F")
    tree.Branch("phi_s",         phi_s,         "phi_s/F")
    tree.Branch("k0_cut",        k0_cut,        "k0_cut/F")
    tree.Branch("RC_factor",     RC_factor,     "RC_factor/F")
    tree.Branch("RC_factor_err", RC_factor_err, "RC_factor_err/F")
    tree.Branch("TCS",           TCS,           "TCS/F")
    tree.Branch("TCS_err",       TCS_err,       "TCS_err/F")
    tree.Branch("Born",          Born,          "Born/F")
    tree.Branch("Born_err",      Born_err,      "Born_err/F")
    tree.Branch("NSubBins",      NSubBins,      "NSubBins/I")
    tree.Branch("Ave_Cen_Ind",   Ave_Cen_Ind,   "Ave_Cen_Ind/I")
    tree.Branch("RC_ave",        RC_ave,        "RC_ave/F")
    tree.Branch("RC_ave_err",    RC_ave_err,    "RC_ave_err/F")
    tree.Branch("nrad",          nrad_array,    "nrad/F")
    tree.Branch("nrad_err",      nrad___err,    "nrad_err/F")
    tree.Branch("CS_rad",        crad_array,    "CS_rad/F")
    tree.Branch("CS_rad_err",    crad___err,    "CS_rad_err/F")
    

    Q2_y, z_pT, phi_h_bin = Bin_Converter_5D[f"Q2_y_z_pT_phi_h_bin_{args.Q2_y_z_pT_phi_h_bin}"]

    Q2, y = get_bin_centers("Q2_y", Q2_y, z_pT)
    pT, z = get_bin_centers("z_pT", Q2_y, z_pT)
    phi_h = 15*(phi_h_bin - 1) + 7.5
    phi_h_symmetry = phi_h + 180 # Assumes that RC is symmetric in phi_h between [0, 180] and [180, 360]
    xB_val  = round(Q2 / (2 * 0.938 * 10.6 * y), 5)
    phi_rad = phi_h*ROOT.TMath.DegToRad()
    if(args.inject_mods):
        value_by_key, unc_by_key = Calc_RC_Factor(Q2, y, z, pT, phi_rad, args.phi_s, args.k0_cut, verbose=not args.quiet, Q2yBin=Q2_y, zpTBin=z_pT)
    else:
        value_by_key, unc_by_key = Calc_RC_Factor(Q2, y, z, pT, phi_rad, args.phi_s, args.k0_cut, verbose=not args.quiet)
    
    Q2_y_Bin[0]     = Q2_y
    z_pT_Bin[0]     = z_pT
    phi_h_Bin[0]    = phi_h_bin
    Q2_center[0]    = Q2
    y_center[0]     = y
    xB_center[0]    = xB_val
    z_center[0]     = z
    pT_center[0]    = pT
    phi_h_center[0] = phi_h
    phi_s[0]        = args.phi_s
    k0_cut[0]       = args.k0_cut
    RC_factor[0]    = float(value_by_key["RC"])
    RC_factor_err[0]= _err0(unc_by_key["RC"])
    TCS[0]          = float(value_by_key["σ_tot"])
    TCS_err[0]      = _err0(unc_by_key["σ_tot"])
    Born[0]         = float(value_by_key["σ_B"])
    Born_err[0]     = _err0(unc_by_key["σ_B"])
    NSubBins[0]     = Num_of_SubBins
    Ave_Cen_Ind[0]  = 0
    RC_ave[0]       = float(value_by_key["RC"])
    RC_ave_err[0]   = _err0(unc_by_key["RC"])
    nrad_array[0]   = float(value_by_key["σ_nrad"])
    nrad___err[0]   = _err0(unc_by_key["σ_nrad"])
    crad_array[0]   = float(value_by_key["σ_rad"])
    crad___err[0]   = _err0(unc_by_key["σ_rad"])
    tree.Fill()
    # Symmetry fill
    phi_h_Bin[0]    = phi_h_bin + 12
    phi_h_center[0] = phi_h_symmetry
    tree.Fill()

    if(args.scan):
        print(f"\n{color.BGREEN}Running With Bin Scan (# Sub Bins = {Num_of_SubBins}){color.END}\n")
        Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y}, Q2-y']
        z_max, z_min, pT_max, pT_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y}, z-pT={z_pT}']        
        Q2_increment = (Q2_max - Q2_min)/Num_of_SubBins
        y_increment  =  (y_max -  y_min)/Num_of_SubBins
        z_increment  =  (z_max -  z_min)/Num_of_SubBins
        pT_increment = (pT_max - pT_min)/Num_of_SubBins
        y_min_true  = y_min
        z_min_true  = z_min
        pT_min_true = pT_min
        Q2_loop_num, y_loop_num, z_loop_num, pT_loop_num = 0, 0, 0, 0
        nrad__CS_List, Born__CS_List, Total_CS_List, RC_Fact__List = [], [], [], []
        nrad__CS_Lerr, Born__CS_Lerr, Total_CS_Lerr, RC_Fact__Lerr = [], [], [], []
        CS_AMM___List, CS_radf__List, CS_rad___List                = [], [], []
        CS_AMM___Lerr, CS_radf__Lerr, CS_rad___Lerr                = [], [], []
        while(round(Q2_min, 4)               <= round(Q2_max, 4)):
            Q2_loop_num += 1
            print(f"\tCurrent Q2 increment = {Q2_min:>7.4f} ({color.BBLUE}{Q2_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
            y_min = y_min_true
            y_loop_num = 0
            while(round(y_min, 4)            <=  round(y_max, 4)):
                y_loop_num += 1
                if(not args.quiet):
                    print(f"\t\tCurrent y increment = {y_min:>7.4f} ({color.BBLUE}{y_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                z_min = z_min_true
                z_loop_num = 0
                while(round(z_min, 4)        <=  round(z_max, 4)):
                    z_loop_num += 1
                    if(not args.quiet):
                        print(f"\t\t\tCurrent z increment = {z_min:>7.4f} ({color.BBLUE}{z_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                    pT_min = pT_min_true
                    pT_loop_num = 0
                    while(round(pT_min, 4)   <= round(pT_max, 4)):
                        pT_loop_num += 1
                        if(not args.quiet):
                            print(f"\t\t\t\tCurrent pT increment = {pT_min:>7.4f} ({color.BBLUE}{pT_loop_num}{color.END_B} of {color.BGREEN}{Num_of_SubBins+1}{color.END})")
                        try:
                            value_by_key, unc_by_key = Calc_RC_Factor(str(Q2_min), str(y_min), str(z_min), str(pT_min), str(phi_rad), str(args.phi_s), str(args.k0_cut), verbose=not args.quiet)
                            nrad_CS_NRadiate = value_by_key.get("σ_nrad")
                            BornCS__NRadiate = value_by_key.get("σ_B")
                            TotalCS_NRadiate = value_by_key.get("σ_tot")
                            RC_Fact_NRadiate = value_by_key.get("RC")
                            CS_AMM__NRadiate = value_by_key.get("σ_AMM")
                            CS_radf_NRadiate = value_by_key.get("σ_rad_f")
                            CS_rad__Radiated = value_by_key.get("σ_rad")
                        except:
                            nrad_CS_NRadiate, BornCS__NRadiate, _, TotalCS_NRadiate, _, _, RC_Fact_NRadiate = Calc_RC_Factor(str(Q2_min), str(y_min), str(z_min), str(pT_min), str(phi_rad), str(args.phi_s), str(args.k0_cut), verbose=not args.quiet)
                            CS_AMM__NRadiate, CS_radf_NRadiate, CS_rad__Radiated = 0.0, 0.0, 0.0
                            value_by_key = {"σ_nrad": 0.0, "σ_B": 0.0, "σ_tot": 0.0, "RC": 0.0, "σ_AMM": 0.0, "σ_rad_f": 0.0, "σ_rad": 0.0}
                        if(None not in [BornCS__NRadiate, TotalCS_NRadiate, RC_Fact_NRadiate, CS_AMM__NRadiate, CS_radf_NRadiate, CS_rad__Radiated]):
                            Born__CS_List.append(float(BornCS__NRadiate))
                            Total_CS_List.append(float(TotalCS_NRadiate))
                            RC_Fact__List.append(float(RC_Fact_NRadiate))
                            nrad__CS_List.append(float(nrad_CS_NRadiate))
                            CS_AMM___List.append(float(CS_AMM__NRadiate))
                            CS_radf__List.append(float(CS_radf_NRadiate))
                            CS_rad___List.append(float(CS_rad__Radiated))

                            Born__CS_Lerr.append(_err0(unc_by_key.get("σ_B")))
                            Total_CS_Lerr.append(_err0(unc_by_key.get("σ_tot")))
                            RC_Fact__Lerr.append(_err0(unc_by_key.get("RC")))
                            nrad__CS_Lerr.append(_err0(unc_by_key.get("σ_nrad")))
                            CS_AMM___Lerr.append(_err0(unc_by_key.get("σ_AMM")))
                            CS_radf__Lerr.append(_err0(unc_by_key.get("σ_rad_f")))
                            CS_rad___Lerr.append(_err0(unc_by_key.get("σ_rad")))

                            Q2_y_Bin[0]     = Q2_y
                            z_pT_Bin[0]     = z_pT
                            phi_h_Bin[0]    = phi_h_bin
                            Q2_center[0]    = Q2_min
                            y_center[0]     = y_min
                            xB_center[0]    = round(Q2_min / (2 * 0.938 * 10.6 * y_min), 5)
                            z_center[0]     = z_min
                            pT_center[0]    = pT_min
                            phi_h_center[0] = phi_h
                            phi_s[0]        = args.phi_s
                            k0_cut[0]       = args.k0_cut
                            RC_factor[0]    = float(RC_Fact_NRadiate)
                            RC_factor_err[0]= _err0(unc_by_key.get("RC"))
                            TCS[0]          = float(TotalCS_NRadiate)
                            TCS_err[0]      = _err0(unc_by_key.get("σ_tot"))
                            Born[0]         = float(BornCS__NRadiate)
                            Born_err[0]     = _err0(unc_by_key.get("σ_B"))
                            NSubBins[0]     = Num_of_SubBins
                            Ave_Cen_Ind[0]  = -1
                            RC_ave[0]       = float(RC_Fact_NRadiate)
                            RC_ave_err[0]   = _err0(unc_by_key.get("RC"))
                            nrad_array[0]   = float(nrad_CS_NRadiate)
                            nrad___err[0]   = _err0(unc_by_key["σ_nrad"])
                            crad_array[0]   = float(CS_rad__Radiated)
                            crad___err[0]   = _err0(unc_by_key["σ_rad"])
                            tree.Fill()
                            phi_h_Bin[0]    = phi_h_bin + 12
                            phi_h_center[0] = phi_h_symmetry
                            tree.Fill()
                        else:
                            print("Scanning 'Calc_RC_Factor' returned 'None'...")
                        pT_min += pT_increment
                    z_min += z_increment
                y_min += y_increment
            Q2_min += Q2_increment
            
        timer.time_elapsed()

        def AveAndErr(_List, _Lerr):
            _Ave      = sum(_List)/len(_List)  # Average
            # Scatter (RMS / sqrt(N))
            _arr      = array('d', _List)
            _Scatt    = ROOT.TMath.RMS(len(_arr), _arr) / ROOT.TMath.Sqrt(len(_arr))
        
            # Measurement ((sqrt(sum(u^2)))/N) if provided and same length; else 0
            if((len(_Lerr) != 0) and (len(_Lerr) == len(_List))):
                _Meas = ROOT.TMath.Sqrt(sum(u**2 for u in _Lerr)) / (len(_Lerr))
            else:
                _Meas = 0.0
            _Err      = ROOT.TMath.Sqrt((_Meas**2) + (_Scatt**2)) # Combined
            return _Ave, _Err
        
        Born__CS_Ave, Born__CS_Err = AveAndErr(Born__CS_List, Born__CS_Lerr)
        Total_CS_Ave, Total_CS_Err = AveAndErr(Total_CS_List, Total_CS_Lerr)

        nRad__CS_Ave, nRad__CS_Err = AveAndErr(CS__nRad_List, CS__nRad_Lerr)

        RC_Fact__Ave, RC_Fact__Err = AveAndErr(RC_Fact__List, RC_Fact__Lerr)

        AMM___CS_Ave, AMM___CS_Err = AveAndErr(CS_AMM___List, CS_AMM___Lerr)
        radf__CS_Ave, radf__CS_Err = AveAndErr(CS_radf__List, CS_radf__Lerr)
        rad___CS_Ave, rad___CS_Err = AveAndErr(CS_rad___List, CS_rad___Lerr)
        
        True_RC_for_Bin        = Total_CS_Ave/Born__CS_Ave
        True_RC_for_Bin_Err    = True_RC_for_Bin * ROOT.TMath.Sqrt((Total_CS_Err / Total_CS_Ave)**2 + (Born__CS_Err  / Born__CS_Ave)**2)

        if(args.inject_mods):
            RC_new_list, cs_born_new_list, cs_tot_new_list = calc_rc_new_from_json(json_file_1=args.json_born, json_file_2=args.json_mods, Q2Y_Bin=Q2_y, z_pT_Bin=z_pT, phi_h=phi_h*ROOT.TMath.DegToRad(), cs_nrad_in=[nRad__CS_Ave, nRad__CS_Err], cs_AMM_in=[AMM___CS_Ave, AMM___CS_Err], cs_rad_f_in=[radf__CS_Ave, radf__CS_Err], cs_rad_in=[rad___CS_Ave, rad___CS_Err], cs_born_in=[Born__CS_Ave, Born__CS_Err], verbose=verbose)
            if(RC_new_list      is not None):
                True_RC_for_Bin, True_RC_for_Bin_Err = RC_Fact__Ave, RC_Fact__Err
                RC_Fact__Ave,    RC_Fact__Err = RC_new_list
            if(cs_born_new_list is not None):
                Born__CS_Ave,    Born__CS_Err = cs_born_new_list
            if(cs_tot_new_list  is not None):
                Total_CS_Ave,    Total_CS_Err = cs_tot_new_list

        Q2_y_Bin[0]     = Q2_y
        z_pT_Bin[0]     = z_pT
        phi_h_Bin[0]    = phi_h_bin
        Q2_center[0]    = Q2
        y_center[0]     = y
        xB_center[0]    = xB_val
        z_center[0]     = z
        pT_center[0]    = pT
        phi_h_center[0] = phi_h
        phi_s[0]        = args.phi_s
        k0_cut[0]       = args.k0_cut
        RC_factor[0]    = True_RC_for_Bin
        RC_factor_err[0]= True_RC_for_Bin_Err
        TCS[0]          = Total_CS_Ave
        TCS_err[0]      = Total_CS_Err
        Born[0]         = Born__CS_Ave
        Born_err[0]     = Born__CS_Err
        NSubBins[0]     = Num_of_SubBins
        Ave_Cen_Ind[0]  = 1
        RC_ave[0]       = RC_Fact__Ave
        RC_ave_err[0]   = RC_Fact__Err
        nrad_array[0]   = nRad__CS_Ave
        nrad___err[0]   = nRad__CS_Err
        crad_array[0]   = rad___CS_Ave
        crad___err[0]   = rad___CS_Err
        tree.Fill()
        # Symmetry fill
        phi_h_Bin[0]    = phi_h_bin + 12
        phi_h_center[0] = phi_h_symmetry
        tree.Fill()
    
    # Save and close
    tree.Write()
    root_file.Close()
    print(f"{color.BBLUE}TTree successfully saved to {color.BGREEN}{filename}{color.END}")

# =========================
# Main
# =========================

if(__name__ == "__main__"):
    args = parse_args()
    if(args.use_json and (not args.fit)):
        print(f"{color.RED}Warning: To use the '--use_json' option, '--fit' must also be set to 'True' (changing this now).")
        args.fit = True
    timer = RuntimeTimer()
    timer.start()
    if(args.ttree):
        if((args.Q2_y_z_pT_phi_h_bin) and (args.root)):
            print(f"\n{color.BCYAN}Generating TTree ROOT File instead of Plots{color.END}\n")
            generate_TTree_output(args)
        else:
            print(f"\n{color.Error}WARNING: Must provide values for '-5d'/'--Q2_y_z_pT_phi_h_bin' and '--root' to be able to create the TTree ROOT Files{color.END}\n")
    else:
        make_plot(args)

    print("\nDone Running 'Make_RC_Factor_Plots.py'\n")
    timer.stop()
    