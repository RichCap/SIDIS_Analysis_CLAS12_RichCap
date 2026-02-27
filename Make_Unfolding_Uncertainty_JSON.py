#!/usr/bin/env python3

import sys
import ROOT
import math

ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)

import traceback
import os
import re
import json
import argparse
import subprocess
import time

from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *
from Cross_Section_Normalization      import Cross_Section_Normalization 

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    p = argparse.ArgumentParser(description=f"{color.BOLD}Make_Unfolding_Uncertainty_JSON.py:\n\t{color.END}JSON-only utility that reproduces the uncertainty JSON outputs from Assign_Uncertainties_to_unfolding.py, but using TWO separate ROOT files (Nominal vs Comparison) with matching histogram keys.",
                                formatter_class=RawDefaultsHelpFormatter)
    p.add_argument('-t', '--test', '--time', '--no_save',
                   action='store_true',
                   dest='test',
                   help="Run but do not write JSON output.\n")
    p.add_argument('-r', '-root', "--root_nominal",
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/FULL_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root",
                   dest='root_nominal',
                   help="Nominal ROOT input file (baseline).\n")
    p.add_argument('-r2', '-rc', '--root_compare',
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/ZerothOrderAcc_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root",
                   help="Comparison ROOT input file (variation).\n")
    p.add_argument("-u", "--unfold",         
                   type=str, 
                   default="Bayesian", 
                   help="Histogram label used in name, e.g. Bayesian, Bin, rdf, mdf.\n")
    p.add_argument("-d", "--dimensions",
                   type=str,
                   default="3D",
                   choices=["1D", "3D", "5D"],
                   help="Unfolding Dimension.")
    p.add_argument("-so", "--smearing_option",
                   type=str,
                   default="Smear",
                   choices=["Smear", "''"],
                   help="Select smearing (via the token used in the histogram names).\n")
    p.add_argument("-q2y", "-q2_y", "--Q2_y_Bins",
                   nargs="+",
                   type=str,
                   default=[str(i) for i in range(1, 18)],
                   help="List of Q2-y bins to run.\n")
    p.add_argument("-zpt", '-z_pt', '--z_pt',
                   nargs="+",
                   type=int,
                   help="List of z-pT bin indices to run. If omitted, runs the full bin range via Get_Num_of_z_pT_Bins_w_Migrations().\n")
    p.add_argument('-ns', '--normalize_shared',
                   action='store_true',
                   help="Normalize comparisons to the total events in their shared bins before getting the differences.\n")
    p.add_argument("-nt", "--normalization_threshold",
                   type=float,
                   default=0.0,
                   help="Bin content threshold for '--normalize_shared'. If either histogram has a bin with contents below this threshold, then that bin will be dropped from both histograms before normalizing.\n")
    p.add_argument('-ncs', '--normalize_cross_section',
                   action='store_true',
                   help="Normalize comparisons to the differential cross section using the functions from 'Cross_Section_Normalization.py'.\n")
    p.add_argument('-sn', '--save_name',
                   type=str,
                   default="",
                   help="Appended tag for the JSON output name.\n")
    p.add_argument('-jp', '--json_prefix',
                   type=str,
                   default="",
                   help="Prefix for JSON output naming (e.g. Mod_Test, Sim_Test, etc.). Can use to specify a full/relative file path.\n")
    p.add_argument('-o', '--json_out',
                   type=str,
                   default=None,
                   help="Optional explicit JSON output name. If omitted, uses the original naming convention (i.e., f'{args.json_prefix}_Unfolding_Bin_Differences_{args.save_name}.json').\nDoes not interact with '--save_name' or '--json_prefix' by itself (but will be save the file name constucted with them for the record outputs).\n")
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Verbose prints.\n")
    p.add_argument('-e', '--email',
                   action='store_true',
                   help="Send an email when finished (optional).\n")
    p.add_argument('-em', '--email_message',
                   type=str,
                   default="",
                   help="Extra message text included in the email.\n")
    return p.parse_args()

def ansi_to_plain(text):
    ansi_plain_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "", '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", '\033[0m': ""}
    sorted_codes = sorted(ansi_plain_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_plain_map[code])
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
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
        if(str(name) in ["email", "email_message", "timer", "root_nominal", "root_compare", "json_out"]):
            continue
        if(str(name) in ["normalization_threshold"] and (not args.normalize_shared)):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'Make_Unfolding_Uncertainty_JSON.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}
Input Files:
    Nominal   : {args.root_nominal}
    Comparison: {args.root_compare}
Output File:
    {args.json_out}
{args.email_message}
Arguments:
{args_list}

{end_time}
{total_time}
{rate_line}
    """
    if(args.email):
        send_email(subject="Finished Running the 'Make_Unfolding_Uncertainty_JSON.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'Make_Unfolding_Uncertainty_JSON.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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

def Normalize_To_Shared_Bins(args, histo1, histo2, include_under_over=False, name_suffix="_NormShared"):
    if((not histo1) or (not histo2)):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Normalize_To_Shared_Bins(): one or both histograms are 'None'.{color.END}", continue_run=False)
        # return histo1, histo2, [], None, None
    if((not histo1.InheritsFrom("TH1D")) or (not histo2.InheritsFrom("TH1D"))):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Normalize_To_Shared_Bins(): both inputs must be TH1D.{color.END}\n\nThe issue was with:\n\t{histo1.GetName()}\n\t{histo2.GetName()}", continue_run=False)
        # return histo1, histo2, [], None, None
    if(histo1.GetNbinsX() != histo2.GetNbinsX()):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Normalize_To_Shared_Bins(): different binning (NbinsX mismatch).{color.END}\n\nThe issue was with:\n\t{histo1.GetName()}\n\t{histo2.GetName()}", continue_run=False)
        # return histo1, histo2, [], None, None
    first_bin = 0 if(include_under_over) else 1
    last_bin  = histo1.GetNbinsX() + 1 if(include_under_over) else histo1.GetNbinsX()
    shared_bins = []
    for ib in range(first_bin, last_bin + 1):
        c1 = histo1.GetBinContent(ib)
        c2 = histo2.GetBinContent(ib)
        if((c1 > args.normalization_threshold) and (c2 > args.normalization_threshold)):
            shared_bins.append(ib)
    if(len(shared_bins) == 0):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): no shared bins found with threshold={args.normalization_threshold}.")
        return histo1, histo2, [], None, None
    sum1, sum2 = 0.0, 0.0
    for ib in shared_bins:
        sum1 += histo1.GetBinContent(ib)
        sum2 += histo2.GetBinContent(ib)
    if((sum1 <= 0.0) or (sum2 <= 0.0)):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Normalize_To_Shared_Bins(): non-positive shared integral (sum1={sum1}, sum2={sum2}).{color.END}\n\nThe issue was with:\n\t{histo1.GetName()}\n\t{histo2.GetName()}", continue_run=True)
        return histo1, histo2, shared_bins, None, None
    h1n = histo1.Clone(histo1.GetName() + name_suffix)
    h2n = histo2.Clone(histo2.GetName() + name_suffix)
    h1n.Scale(1.0 / sum1)
    h2n.Scale(1.0 / sum2)
    h1n.SetStats(0)
    h2n.SetStats(0)
    if(args.verbose):
        print(f"{color.BGREEN}Normalized to shared bins:{color.END} {len(shared_bins)} bins; thresholds > {args.normalization_threshold}")
    return h1n, h2n, shared_bins, sum1, sum2

def Apply_PreBin_Uncertainties(Histo_In, Q2_y_Bin=None, z_pT_Bin=None, Uncertainty_File_In=None, invert_errors=False):
    if(Uncertainty_File_In is None):
        return Histo_In
    if((not Histo_In) or (not Histo_In.InheritsFrom("TH1"))):
        print(f"{color.Error}Error:{color.END}\n\t{Histo_In} is an invalid histogram that was passed to Apply_PreBin_Uncertainties()")
        return Histo_In
    Histo_Name_General = Histo_In.GetName()
    if((Q2_y_Bin is None) or (z_pT_Bin is None)):
        match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_General))
        if(match):
            Q2_y_Bin = int(match.group(1))
            z_pT_Bin = int(match.group(2))
        else:
            print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
            return Histo_In
    with open(Uncertainty_File_In, "r") as jf:
        data = json.load(jf)
    key = f"{Q2_y_Bin}_{z_pT_Bin}"
    if(key not in data):
        print(f"{color.RED}Error:{color.END} Key '{key}' not found in {Uncertainty_File_In}")
        return Histo_In
    bin_data = data[key]
    n_bins_hist = Histo_In.GetNbinsX()
    n_bins_data = len(bin_data)
    if(n_bins_data != n_bins_hist):
        print(f"{color.Error}Error:{color.END} Bin count mismatch (JSON={n_bins_data}, Histo={n_bins_hist}). Aborting modification.")
        return Histo_In
    g_asym = ROOT.TGraphAsymmErrors(Histo_In)
    g_asym.SetName(f"{Histo_In.GetName()}_AsymErr")
    g_asym.SetLineColor(Histo_In.GetLineColor())
    g_asym.SetMarkerColor(Histo_In.GetMarkerColor())
    g_asym.SetLineWidth(Histo_In.GetLineWidth())
    for i, entry in enumerate(bin_data, start=1):
        uncertainty = float(entry.get("uncertainty", 0.0))
        current_err = float(Histo_In.GetBinError(i))
        sys_mag     = ROOT.sqrt(max([current_err**2, uncertainty**2 + current_err**2]))
        if(invert_errors):
            uncertainty = -uncertainty
        low_err, high_err = current_err, current_err
        if(uncertainty > 0.0):
            low_err  = current_err
            high_err = sys_mag
        elif(uncertainty < 0.0):
            low_err  = sys_mag
            high_err = current_err
        g_asym.SetPointEYlow(i  - 1, low_err)
        g_asym.SetPointEYhigh(i - 1, high_err)
    Histo_In.asym_errors = g_asym
    return Histo_In

def Compare_TH1D_Histograms_For_JSON(args, ROOT_In_1, HISTO_NAME_1, ROOT_In_2, HISTO_NAME_2, legend_labels=("Histogram 1", "Histogram 2"), Q2y_str="1", zPT_str="1", Unfolding_Diff_Data_In=None):
    if(Unfolding_Diff_Data_In is None):
        Unfolding_Diff_Data_In = {}
    histo1 = ROOT_In_1.Get(HISTO_NAME_1)
    histo2 = ROOT_In_2.Get(HISTO_NAME_2)
    if((not histo1) or (not histo2)):
        Update_Email(args, update_message=f"""{color.Error}MISSING:{color.END_R} Could not retrieve one or both histograms:{color.END}
    HISTO_NAME_1 = {HISTO_NAME_1}
    HISTO_NAME_2 = {HISTO_NAME_2}""")
        return False, Unfolding_Diff_Data_In
    if((not histo1.InheritsFrom("TH1D")) or (not histo2.InheritsFrom("TH1D"))):
        Update_Email(args, update_message=f"""{color.Error}MISSING:{color.END_R} Both histograms must be TH1D.{color.END}
Issue was with:
    HISTO_NAME_1 = {HISTO_NAME_1}
    HISTO_NAME_2 = {HISTO_NAME_2}""")
        return False, Unfolding_Diff_Data_In
    normalization_to_histo1, normalization_to_histo2 = 1.0, 1.0
    normalization_types = []
    if(args.normalize_shared):
        normalization_types.append("Shared_Bins")
        histo1, histo2, _, normalization_to_histo1, normalization_to_histo2 = Normalize_To_Shared_Bins(args, histo1, histo2, include_under_over=False, name_suffix="_NormShared")
        if((normalization_to_histo1 is None) or (normalization_to_histo2 is None)):
            normalization_to_histo1, normalization_to_histo2 = 1.0, 1.0
    if(args.normalize_cross_section):
        normalization_types.append("Differential_Cross_Section")
        histo1, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=histo1, Q2_y_Bin=Q2y_str, z_pT_Bin=zPT_str, phi_t_bin=15, Rename_Axis=True, args_in=args)
        normalization_to_histo1 = Bin_Width_Area_Scale*Luminosity
        histo2, Bin_Width_Area_Scale, Luminosity = Cross_Section_Normalization(Histo=histo2, Q2_y_Bin=Q2y_str, z_pT_Bin=zPT_str, phi_t_bin=15, Rename_Axis=True, args_in=args)
        normalization_to_histo2 = Bin_Width_Area_Scale*Luminosity
    histo_key = f"{Q2y_str}_{zPT_str}"
    if(histo_key not in Unfolding_Diff_Data_In):
        Unfolding_Diff_Data_In[histo_key] = []
    for bin_idx in range(1, histo1.GetNbinsX() + 1):
        val1    = histo1.GetBinContent(bin_idx)
        val2    = histo2.GetBinContent(bin_idx)
        err1    = histo1.GetBinError(bin_idx)
        err2    = histo2.GetBinError(bin_idx)
        diff    = abs(val1 - val2)
        err     = math.sqrt(max([err1**2 - err2**2, 0]))
        M_uncer = val2 - val1
        Unfolding_Diff_Data_In[histo_key].append({"phi_bin": bin_idx,
                                                  f"{legend_labels[0]} — Value": val1, f"{legend_labels[0]} — Error": err1,
                                                  f"{legend_labels[1]} — Value": val2, f"{legend_labels[1]} — Error": err2,
                                                  "diff": diff, "err": err, "uncertainty": M_uncer,
                                                  "scale_to_nominal": normalization_to_histo1,
                                                  "scale_to_variation": normalization_to_histo2,
                                                  "normalization_types": normalization_types if(normalization_types != []) else "None"})
    return True, Unfolding_Diff_Data_In

def build_histo_name(args, Q2_y_BIN_NUM, z_PT_BIN_NUM):
    if(args.dimensions in ["1D"]):
        return f"(1D)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(phi_t)"
    if(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
        return f"(MultiDim_3D_Histo)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(MultiDim_z_pT_Bin_Y_bin_phi_t)"
    if(args.dimensions in ["5D"]):
        return f"(MultiDim_5D_Histo)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(MultiDim_Q2_y_z_pT_phi_h)"
    Crash_Report(args, crash_message=f"{color.Error}Dimensions argument did not return a viable histogram name.{color.END}")

def Construct_Run_Info(args):
    Run_Info = {"Start_Time": args.timer.start_find(return_Q=True)}
    for name, value in vars(args).items():
        if(str(name) in ["timer"]):
            continue
        Run_Info[name] = value
    return Run_Info

def save_dict_to_json(data_to_save, args, lock_timeout_sec=120, stale_lock_sec=3600):
    # Concurrency protection:
    #   - Uses an atomic lock directory "<json_file>.lockdir" so multiple scripts can update the same JSON safely.
    #   - Writes via temp file + os.replace() for atomic file replacement (avoids partial writes).
    # Behavior:
    #   - Reads existing JSON (if any) and updates it with the keys from data_to_save (like dict.update()).
    #   - Never wipes the file unless the existing file is corrupted (then it is backed up and restarted as {}).
    if(not isinstance(data_to_save, dict)):
        raise TypeError("save_dict_to_json(...): data_to_save must be a dict")
    json_path = os.path.abspath(args.json_out)
    json_dir  = os.path.dirname(json_path)
    if((json_dir != "") and (not os.path.exists(json_dir))):
        os.makedirs(json_dir, exist_ok=True)
    lock_dir = f"{json_path}.lockdir"
    start_t  = time.time()
    while(True):
        try: # Acquire lock (mkdir is atomic)
            os.mkdir(lock_dir)
            owner_path = os.path.join(lock_dir, "owner.txt")
            with open(owner_path, "w") as ofile:
                ofile.write(f"pid={os.getpid()}\n")
                ofile.write(f"epoch={time.time():.6f}\n")
            break
        except FileExistsError: # Stale lock handling (best-effort cleanup)
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
                raise RuntimeError(f"save_dict_to_json(...): timed out waiting for lock: {lock_dir}")
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
                        raise ValueError("save_dict_to_json(...): existing JSON root is not an object/dict")
            except json.JSONDecodeError:
                backup = f"{json_path}.corrupt.{int(time.time())}"
                try:
                    os.replace(json_path, backup)
                except Exception:
                    pass
                data = {}
        data.update(data_to_save)
        tmp_path = f"{json_path}.tmp.{os.getpid()}"
        with open(tmp_path, "w") as tfile:
            json.dump(data, tfile, indent=4, sort_keys=True)
            tfile.write("\n")
        os.replace(tmp_path, json_path)
        if(args.verbose):
            print(f"Updated JSON: {json_path}")
            print(f"  Keys written/overwritten: {len(data_to_save)}")
    finally: # Release lock (best effort)
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
    return True

def main():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    if((args.unfold in ["tdf"]) and (args.dimensions in ["3D", "MultiDim_3D_Histo"])):
        args.smearing_option = "''"
    if(args.Q2_y_Bins != ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']):
        print(f"\n{color.BOLD}Running with the following Q2-y Bins:\t{color.GREEN}{args.Q2_y_Bins}{color.END}\n")
    if(args.json_out is None):
        args.json_out = f"{args.json_prefix if(str(args.json_prefix).endswith('/') or str(args.json_prefix).endswith('_') or (args.json_prefix in [''])) else f'{args.json_prefix}_'}Unfolding_Bin_Differences{f'_{args.save_name}' if(args.save_name not in ['']) else ''}.json"
    elif(not str(args.json_out).endswith(".json")):
        args.json_out = f"{args.json_out}.json"
    ROOT_Input = ROOT.TFile.Open(args.root_nominal, "READ")
    ROOT_Comp  = ROOT.TFile.Open(args.root_compare, "READ")
    if((not ROOT_Input) or ROOT_Input.IsZombie()):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Could not open nominal ROOT file:{color.END_B}\n\t{args.root_nominal}{color.END}")
    if((not ROOT_Comp) or ROOT_Comp.IsZombie()):
        Crash_Report(args, crash_message=f"{color.Error}ERROR:{color.END_R} Could not open comparison ROOT file:{color.END_B}\n\t{args.root_compare}{color.END}")
    Unfolding_Diff_Data = {"Run_Info": Construct_Run_Info(args)}
    comparisons_done    = 0
    for BIN in args.Q2_y_Bins:
        Q2_y_BIN_NUM = int(BIN) if(str(BIN) not in ["0"]) else "All"
        if(args.z_pt):
            z_pT_Bin_Range = args.z_pt
        else:
            z_pT_Bin_Range = range(0, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_BIN_NUM)[1] + 1)
        for z_PT_BIN in z_pT_Bin_Range:
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_BIN_NUM, Z_PT_BIN=z_PT_BIN) and (z_PT_BIN not in [0])):
                if(args.z_pt):
                    print(f"{color.Error}WARNING:{color.END_R} The selected (Q2-y)-(z-pT) Bin ({Q2_y_BIN_NUM}-{z_PT_BIN}) does not exist...{color.END}")
                continue
            z_PT_BIN_NUM = int(z_PT_BIN) if(str(z_PT_BIN) not in ["0"]) else "All"
            HISTO_NAME   = build_histo_name(args, Q2_y_BIN_NUM, z_PT_BIN_NUM)
            HISTO_NAME_2 = f"{HISTO_NAME}_(Mod_Test)"
            if(not ROOT_Comp.GetListOfKeys().Contains(HISTO_NAME_2)):
                Update_Email(args, update_message=f"{color.Error}The 'ROOT_Comp' file is missing the '_(Mod_Test)' part of the key in the Histogram Name: {color.END_B}{HISTO_NAME_2}\n{color.END}\nWill attempt to continue to run anyway by defaulting back to the non-'Mod_Test' key instead.", verbose_override=True)
                HISTO_NAME_2 = HISTO_NAME
            try:
                Saved_Q, Unfolding_Diff_Data = Compare_TH1D_Histograms_For_JSON(args, ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME, ROOT_In_2=ROOT_Comp, HISTO_NAME_2=HISTO_NAME_2, legend_labels=("Unfolded with Baseline MC", "Unfolded with Weighted/Modulated MC"), Q2y_str=Q2_y_BIN_NUM, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data)
            except:
                Crash_Report(args, crash_message=f"{color.Error}The 'Compare_TH1D_Histograms_For_JSON()' Function CRASHED!\n{color.END_R}ERROR:\n{str(traceback.format_exc())}{color.END}\nWill continue to run anyway.", continue_run=True)
                Saved_Q = False
            if(not Saved_Q):
                print(f"{color.Error}MISSING:{color.END} {HISTO_NAME}")
                continue
            comparisons_done += 1
            if(args.verbose):
                print(args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' '))
    if(not args.test):
        save_dict_to_json(Unfolding_Diff_Data, args)
        print(f"\n{color.BBLUE}Saved all bin-by-bin differences to: {color.END_B}{args.json_out}{color.END}\n")
    else:
        print(f"\n{color.BCYAN}Would have saved all bin-by-bin differences to: {color.END_B}{args.json_out}{color.END}\n")
    Construct_Email(args, final_count=comparisons_done, Count_Type="Comparisons")

if(__name__ == "__main__"):
    main()
