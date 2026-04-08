#!/usr/bin/env python3
import sys
import argparse

import ROOT, numpy, re
import traceback
import os
from pathlib import Path

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
sys.path.remove(script_dir)
del script_dir

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Creates BC Corrections from MC GEN Bins.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        action='store_true',
                        help='Run as test.\n')
    parser.add_argument('-gdf', '-clasdis', '--use_clasdis',
                        action='store_true',
                        help='Run with clasdis instead of EvGen (assumes that the EvGen weight should be used by default unless this argument is used).\n')
    parser.add_argument('-nb', '--num_sub_bins',
                        default=5,
                        type=int,
                        help="Number of sub-bins used per Q2-y-z-pT bin. Must be a positive, odd number.\n")
    parser.add_argument('-nbphi', '--num_phi_sub_bins',
                        default=0,
                        type=int,
                        help=f"Addition number of sub-bins used per phi_h bin.\n{color.ERROR}Will add this number to '--num_sub_bins' to get a new total number of sub-bins used for phi_h specifically.{color.END}{color.YELLOW}\n(The default value of '0' means that the same number of bins are used for each variable)\n{color.END_e}The final total must still be a positive, odd number.{color.END}\n")
    parser.add_argument('-q2y', '-Q2y', '--Q2_y_Bin',
                        default=-1,
                        type=int,
                        choices=[x for x in range(-1, 18) if(x != 0)],
                        help="Selected Q2-y Bin to run. Use '-1' to run all bins.\n")
    parser.add_argument('-zpt', '-zpT', '--z_pT_Bin',
                        default=-1,
                        type=int,
                        help=f"Selected z-pT Bin (for any given Q2-y Bin) to run. Use '-1' to run all bins.\n{color.BOLD}Does not automatically reject incompatible combinations of the '--Q2_y_Bin' and '--z_pT_Bin' options.{color.END}\n")
    parser.add_argument('-phit', '-phih', '-phi_t', '-phi_h', '--phih_Bin',
                        default=-1,
                        type=int,
                        choices=[x for x in range(-1, 25) if(x != 0)],
                        help="Selected phi_t Bin to run (each bin is given in increments of 15 degrees). Use '-1' to run all bins.\n")
    parser.add_argument('-f', '--file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb-EvGen-LUND_EvGen_richcap_GEMC-9729_4.hipo.root",
                        type=str,
                        help=f"Path to MC GEN ROOT file used to create the BC corrections.\n{color.BOLD}Use EvGen files so that a difference in the modulations is actually observable in the 4D sub-bins.{color.END}\n")
    parser.add_argument('-cdf', '--check_dataframe',
                        action='store_true',
                        help='Prints full contents of the RDataFrame to see available branches.\n')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print more information while running.\n')
    parser.add_argument('-jsw', '--json_weights',
                        action='store_true',
                        help='Use the json weights (for physics injections) given by the `--json_file` argument.\n')
    parser.add_argument('-jsf_in', '--json_file_in',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_Final_File_Before_the_Collaboration_Meeting.json",
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_New_File_with_BC.json",
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_Simple_RooUnfold_SelfContained_using_SIDIS_Comparisons_Between_GEN_and_Unfold_NEW_FULL_Normalization_AND_FULL_Fits.json",
                        type=str,
                        help="JSON file path for using '--json_weights'.\n")
    parser.add_argument('-jf', '--json_file_out',
                        # default="Sub_Bin_Contents_for_BC_Correction.json",
                        default="Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json",
                        type=str,
                        help='Output JSON file where the bin contents will be saved.\n')
    parser.add_argument('-hi', '-histo', '--histogram',
                        action='store_true',
                        help='Use ROOT histograms to get the weighted bin contents per sub-bin (instead of the per-bin sum of weight counts).\n')
    parser.add_argument('-rf', '--root_file_out',
                        default="ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root",
                        type=str,
                        help="Output ROOT file where the sub-bin histograms will be saved if the '--histogram' option is selected.\n")
    parser.add_argument('-ufn', '--use_file_name',
                        action='store_true',
                        help="If the '--file' argument does not include a '*' in its path, this argument will assume that a single file is being used and that it should be added to the output JSON/ROOT file's names.\nThe default option of just using the '--json_file_out' and '--root_file_out' will be applied if multiple files are given.\n")
    parser.add_argument('-ht', '--histo_title',
                        default="",
                        type=str,
                        help="Optional histogram title addition (use with the '--histogram' option).\n")
    parser.add_argument('-nz', '--non_zero_bin_averages',
                        action='store_true',
                        help="Optional: calculate the average sub-bin contents and their standard deviations using only sub-bins with non-zero content.\n")
    parser.add_argument('-e', '--email',
                        action='store_true',
                        help='Send Email message when the script finishes running.\n')
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the default notification from '--email'.\n")
    parser.add_argument('-rR', '-read_root', '-bc', '--get_BC_factors',
                        action='store_true',
                        help=f"Reads the ROOT files from '--root_file_out' to get the BC factors for each bin.\n{color.BOLD}Will write the results to the '--json_file_out' JSON file if not running in '--test' mode.{color.END}\n")

    parser.add_argument('-mpi', '--make_plot_images',
                        action='store_true',
                        help="Optional: make a visualization plot (Center vs Average sub-bin contents vs nominal phi_h bin) from the existing JSON output.\n")
    parser.add_argument('-mpbc', '--make_plot_BC_factor',
                        action='store_true',
                        help="Optional: also make a BC Factor vs nominal phi_h bin plot from the existing JSON output.\nRequires the same single '--Q2_y_Bin' and '--z_pT_Bin' as '--make_plot_images' unless using '--make_plot_Q2_y_images'.\n")
    parser.add_argument('-mpq2y', '--make_plot_Q2_y_images',
                        action='store_true',
                        help="Optional: make combined z-pT image canvases for each selected Q2-y bin from the existing JSON output.\nWorks with '--make_plot_images' and/or '--make_plot_BC_factor'.\n")
    parser.add_argument('-n', '-sn', '--image_name',
                        default="",
                        type=str,
                        help="Optional prefix added to the output filename for the BC sub-bin comparison plot.\n")
    parser.add_argument('-ff', '--File_Format',
                        default="pdf",
                        type=str,
                        choices=["png", "pdf"],
                        help="Output format for the BC sub-bin comparison plot.\n")
    parser.add_argument('-bcz', '--BC_Zoom',
                        action='store_true',
                        help="When plotting the BC Factors with '--make_plot_BC_factor', this option will make it so the y-axis starts as 0.5 times the minimum point in the plot (instead of always at zero).\n")
    parser.add_argument('-sbs', '--show_bin_stats',
                        action='store_true',
                        help="Optional: show the total events (nominal bin sum over all phi_h) as a text label on Type 1 sub-bin comparison plots.\n")

    return parser.parse_args()

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

# import math
# import array
# import copy
import json
import time

import subprocess
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
        if(str(name) in ["email", "email_message", "timer", "root_file_out", "file", "json_file_out", "Save_Name"]):
            continue
        if((str(name) in ["check_dataframe"]) and (args.get_BC_factors)):
            continue
        if((str(name) in ["phih_Bin"]) and (args.histogram or (not args.get_BC_factors))):
            continue
        if((str(name) in ["histo_title"]) and ((not args.histogram) or args.get_BC_factors)):
            continue
        if((str(name) in ["json_file_in"]) and (not args.json_weights)):
            continue
        if((str(name) in ["image_name", "File_Format"]) and (not (args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images))):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'BC_Corrections_Script.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

{args.email_message}

Input(s):
{f'{args.root_file_out}\n{args.json_file_out}' if((args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images) and args.get_BC_factors) else args.json_file_out if(args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images) else args.root_file_out if(args.get_BC_factors) else args.file}
Output(s):
{f'{args.json_file_out}\n{getattr(args, "Save_Name", None)}' if((args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images) and args.get_BC_factors) else getattr(args, "Save_Name", None) if(args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images) else args.json_file_out if((not args.histogram) or args.get_BC_factors) else  args.root_file_out}


Arguments:
{args_list}

{end_time}
{total_time}
{rate_line}
    """

    if(args.email):
        send_email(subject="Finished Running the 'BC_Corrections_Script.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'BC_Corrections_Script.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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

def load_json_file(path):
    # Load a JSON file and return its contents.
    # Args: Path to the JSON file
    # Returns: Parsed JSON data (into a dict | list)
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

def save_dict_to_json(data_to_save, json_file="Sub_Bin_Contents_for_BC_Correction.json", lock_timeout_sec=120, stale_lock_sec=3600, verbose=False):
    # Concurrency protection:
    #   - Uses an atomic lock directory "<json_file>.lockdir" so multiple scripts can update the same JSON safely.
    #   - Writes via temp file + os.replace() for atomic file replacement (avoids partial writes).
    # Behavior:
    #   - Reads existing JSON (if any) and updates it with the keys from data_to_save (like dict.update()).
    #   - Never wipes the file unless the existing file is corrupted (then it is backed up and restarted as {}).
    if(not isinstance(data_to_save, dict)):
        raise TypeError("save_dict_to_json(...): data_to_save must be a dict")
    json_path = os.path.abspath(json_file)
    json_dir  = os.path.dirname(json_path)
    if((json_dir != "") and (not os.path.exists(json_dir))):
        os.makedirs(json_dir, exist_ok=True)
    lock_dir = f"{json_path}.lockdir"
    start_t  = time.time()
    while(True): # Acquire lock (mkdir is atomic)
        try:
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
            json.dump(data, tfile, indent=2, sort_keys=True)
            tfile.write("\n")
        os.replace(tmp_path, json_path)
        if(verbose):
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

def Flatten_Fit_Pars_For_CPP_Map(Fit_Pars_In, args, prefer_normalized=True):
    # Supports:
    #   (A) NEW format: Fit_Pars_from_3D_Bayesian{...} or Fit_Pars_from_3D_Bayesian_(Normalized){...}
    #   (B) OLD format: {"A_1_1": ..., "B_1_1": ..., "C_1_1": ..., ...}
    # Returns a flat dict: {"A_Q2y_zpt": float, "B_Q2y_zpt": float, "C_Q2y_zpt": float}
    if(not isinstance(Fit_Pars_In, dict)):
        Crash_Report(args, crash_message=f"{color.Error}The Code has CRASHED!\nFlatten_Fit_Pars_For_CPP_Map(...): Fit_Pars_In must be a dict{color.END}")
    # key_norm = "Fit_Pars_from_3D_RC_Bayesian_(Normalized)"
    key_norm = "Fit_Pars_from_3D_RC_Bayesian"
    key_raw  = "Fit_Pars_from_3D_Bayesian"
    Fit_Block = None
    if((prefer_normalized) and (key_norm in Fit_Pars_In) and isinstance(Fit_Pars_In[key_norm], dict)):
        Fit_Block = Fit_Pars_In[key_norm]
        if(args.verbose):
            print(f"{color.BBLUE}Using JSON group: {color.BPINK}{key_norm}{color.END}")
    elif((key_raw in Fit_Pars_In) and isinstance(Fit_Pars_In[key_raw], dict)):
        Fit_Block = Fit_Pars_In[key_raw]
        if(args.verbose):
            print(f"{color.BBLUE}Using JSON group: {color.BPINK}{key_raw}{color.END}")
    # --- NEW format detected ---
    if(Fit_Block is not None):
        Fit_Pars_Out = {}
        for bin_key, par_dict in Fit_Block.items():
            if(not isinstance(par_dict, dict)):
                continue
            match = re.search(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", str(bin_key))
            if(not match):
                continue
            Q2y = int(match.group(1))
            zpt = int(match.group(2))
            for tag, json_name in [("A", "Fit_Par_A"), ("B", "Fit_Par_B"), ("C", "Fit_Par_C")]:
                if(json_name in par_dict):
                    try:
                        val = float(par_dict[json_name])
                    except Exception:
                        continue
                    if(not numpy.isfinite(val)):
                        continue
                    Fit_Pars_Out[f"{tag}_{Q2y}_{zpt}"] = val
        return Fit_Pars_Out
    # --- OLD format fallback (already flat) ---
    # Expect keys like "A_9_1", "B_9_1", "C_9_1" -> float
    return Fit_Pars_In

# =========================
# Binning Dictionary
# =========================
from Binning_Dictionaries import Full_Bin_Definition_Array # , Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D

def Load_RDataFrame(args):
    print(f"\n{color.BBLUE}Running with File: {color.BPINK}{args.file.split('/')[-1]}{color.END}\n")
    gdf = ROOT.RDataFrame("h22", str(args.file))
    if(any(var not in gdf.GetColumnNames() for var in ["Q2", "y", "z", "pT", "phi_t"])):
        print(f"{color.RED}WARNING{color.END}: ROOT file is missing the kinematic variables.\n")
        ROOT.gInterpreter.Declare(Rotation_Matrix)
        gdf = gdf.Define("vals", """
auto beam    = ROOT::Math::PxPyPzMVector(0, 0, 10.6, 0);
auto targ    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
auto ele     = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
auto pip0    = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
auto epipX   = beam + targ - ele - pip0;
auto q       = beam - ele;
auto Q2      = -q.M2();
auto v       = beam.E() - ele.E();
auto xB      = Q2/(2*targ.M()*v);
auto W2      = targ.M2() + 2*targ.M()*v - Q2;
auto W       = sqrt(W2);
auto y       = (targ.Dot(q))/(targ.Dot(beam));
auto z       = ((pip0.E())/(q.E()));
auto gamma   = 2*targ.M()*(xB/sqrt(Q2));
auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));
std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};
return vals;""")
        gdf = gdf.Define('MM',  'vals[0]') # Missing Mass
        gdf = gdf.Define('MM2', 'vals[1]') # Missing Mass Squared
        gdf = gdf.Define('Q2',  'vals[2]') # lepton momentum transfer squared
        gdf = gdf.Define('xB',  'vals[3]') # fraction of the proton momentum that is carried by the struck quark
        gdf = gdf.Define('W',   'vals[6]') # center-of-mass energy
        gdf = gdf.Define('y',   'vals[7]') # energy fraction of the incoming lepton carried by the virtual photon
        gdf = gdf.Define('z',   'vals[8]') # energy fraction of the virtual photon carried by the outgoing hadron
        gdf = gdf.Define("vals2", """
auto beamM  = ROOT::Math::PxPyPzMVector(0, 0, 10.6, 0);
auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
auto eleM   = ROOT::Math::PxPyPzMVector(ex,     ey,   ez,       0);
auto pip0M  = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
auto lv_qMM = beamM - eleM;
TLorentzVector beam(0, 0, 10.6, beamM.E());
TLorentzVector targ(0, 0, 0, targM.E());
TLorentzVector ele(ex,      ey,   ez,  eleM.E());
TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
TLorentzVector lv_q = beam - ele;
///////////////     Angles for Rotation     ///////////////
double Theta_q = lv_q.Theta();
double Phi_el  = ele.Phi();
///////////////     Rotating to CM Frame     ///////////////
auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);
///////////////     Saving CM components     ///////////////
double pipx_1 = pip0_Clone.X();
double pipy_1 = pip0_Clone.Y();
double pipz_1 = pip0_Clone.Z();
double qx = lv_q_Clone.X();
double qy = lv_q_Clone.Y();
double qz = lv_q_Clone.Z();
double beamx = beam_Clone.X();
double beamy = beam_Clone.Y();
double beamz = beam_Clone.Z();
double elex = ele_Clone.X();
double eley = ele_Clone.Y();
double elez = ele_Clone.Z();
///////////////     Boosting Vectors     ///////////////
auto fCM   = lv_q_Clone + targ_Clone;
auto boost = -(fCM.BoostVector());
auto qlv_Boost(lv_q_Clone);
auto ele_Boost(ele_Clone);
auto pip_Boost(pip0_Clone);
auto beamBoost(beam_Clone);
auto targBoost(targ_Clone);
qlv_Boost.Boost(boost);
ele_Boost.Boost(boost);
pip_Boost.Boost(boost);
beamBoost.Boost(boost);
targBoost.Boost(boost);
TVector3 v0, v1;
v0 = qlv_Boost.Vect().Cross(ele_Boost.Vect());
v1 = qlv_Boost.Vect().Cross(pip_Boost.Vect());
Double_t c0, c1, c2, c3;
c0 = v0.Dot(pip_Boost.Vect());
c1 = v0.Dot(v1);
c2 = v0.Mag();
c3 = v1.Mag();
// Phi Trento (using Stefan's equation)
double phi_t_cross_product = (c0/TMath::Abs(c0)) * TMath::ACos(c1 /(c2*c3));
double Cos_theta_t = (pip0.Vect().Dot(lv_q.Vect()))/(pip0.Vect().Mag()*lv_q.Vect().Mag());
double theta_t = TMath::ACos(Cos_theta_t);
double pipTx = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
double pipTy = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
double pipTz = pip0.P()*TMath::Cos(theta_t);
TVector3 pipT(pipTx, pipTy, pipTz);
phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();
///////////////   x Feynmann   ///////////////
double xF = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);
// pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
double pT = sqrt(pipx_1*pipx_1 + pipy_1*pipy_1);
double phi_t = pip0_Clone.Phi()*TMath::RadToDeg();
if(phi_t < 0){phi_t += 360;}
std::vector<double> vals2 = {pT, phi_t, xF};
return vals2;""")
        gdf = gdf.Define('pT',    'vals2[0]')    # transverse momentum of the final state hadron
        gdf = gdf.Define('phi_t', 'vals2[1]')    # Most important angle (between lepton and hadron planes)
        gdf = gdf.Define('xF',    'vals2[2]')    # x Feynmann

        Q2_y_Bin_Def = ""
        for Q2_y in range(1, 18):
            Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y}, Q2-y']
            bin_condition= f"(Q2 < {Q2_max}) && (Q2 > {Q2_min}) && (y < {y_max}) && (y > {y_min})"
            Q2_y_Bin_Def = f"""{Q2_y_Bin_Def}
    if({bin_condition}){{ return {Q2_y}; }}"""
        Q2_y_Bin_Def = f"""{Q2_y_Bin_Def}
    return 0;"""
        gdf = gdf.Redefine("Q2_Y_Bin", Q2_y_Bin_Def) if(gdf.HasColumn("Q2_Y_Bin")) else gdf.Define("Q2_Y_Bin", Q2_y_Bin_Def)
        ##########################################################################################################################################################################################
        ##########################################################################################################################################################################################
        def z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="All"):
            if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
                print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function z_pT_Bin_Standard_Def_Function(Variable_Type='{Variable_Type}', Bin_Version='{Bin_Version}').\nFix input to use anything other than the default calculations of z and pT.")
                Variable_Type  = ""
            Q2_xB_Bin_event_name = "".join(["Q2_xB_Bin" if(Bin_Version not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q2_y_Bin" if(("y_" in Bin_Version) or (Bin_Version == "4")) else "Q2_Y_Bin", "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in ["", "4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
            z_pT_Bin_event_name  = "".join(["z_pT_Bin",                                                                                                                                                          "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in [""])                                               else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
            z_pT_Bin_Standard_Def = "".join([str(New_z_pT_and_MultiDim_Binning_Code), """
                double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
                double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", f""";
                int z_pT_Bin_event_val = 0;
                int Phih_Bin_event_val = 0;
                int MultiDim3D_Bin_val = 0;
                int MultiDim5D_Bin_val = 0;
                if({Q2_xB_Bin_event_name} != 0){{
                    z_pT_Bin_event_val = Find_z_pT_Bin({Q2_xB_Bin_event_name}, z_event_val, pT_event_val);
                    if(z_pT_Bin_event_val == 0){{ MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0; }}
                    else{{
                        if(Phi_h_Bin_Values[{Q2_xB_Bin_event_name}][z_pT_Bin_event_val][0] == 1){{ Phih_Bin_event_val = 1; }}
                        else{{Phih_Bin_event_val = Find_phi_h_Bin(""", str(Q2_xB_Bin_event_name), """, z_pT_Bin_event_val, """, "smeared_vals[11]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "phi_t", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """);}
                        MultiDim3D_Bin_val = Phi_h_Bin_Values[""",     str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][1] + Phih_Bin_event_val;
                        MultiDim5D_Bin_val = Phi_h_Bin_Values[""",     str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][2] + Phih_Bin_event_val;
                    }
                }
                else{ z_pT_Bin_event_val = 0; MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0; }
                """, f"""
                // Refinement of Migration/Overflow Bins
                if((({Q2_xB_Bin_event_name} == 1) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 2) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 3) && ((z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 4) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 5) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 6) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 7) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 8) && ((z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 9) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 10) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 11) && ((z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 12) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 13) && ((z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 14) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 15) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 16) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 23) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 17) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30)))){{
                    z_pT_Bin_event_val = 0; MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0;
                }}
                """, "return z_pT_Bin_event_val;" if(Var_return in ["z_pT", "2D"]) else "return MultiDim3D_Bin_val;" if(Var_return in ["3D"]) else "return MultiDim5D_Bin_val;" if(Var_return in ["5D"]) else """std::vector<int> z_pT_and_MultiDim_Bins = {z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val};
                return z_pT_and_MultiDim_Bins;"""])
            return z_pT_Bin_Standard_Def
        # gdf = gdf.Define("All_MultiDim_Y_bin",              str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="All")))
        # gdf = gdf.Define("z_pT_Bin_Y_bin",                  "All_MultiDim_Y_bin[0]")
        # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t",   "All_MultiDim_Y_bin[1]")
        # gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",        "All_MultiDim_Y_bin[2]")
        gdf = gdf.Redefine("z_pT_Bin_Y_bin", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="2D"))) if(gdf.HasColumn("z_pT_Bin_Y_bin")) else gdf.Define("z_pT_Bin_Y_bin", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="2D")))
        # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="3D")))
        # gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",      str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="5D")))

    if(any(var not in gdf.GetColumnNames() for var in ["Q2_Y_Bin", "z_pT_Bin_Y_bin"])):
        print(f"{color.RED}WARNING{color.END}: ROOT file is missing the binning variables.\n")
        Q2_y_Bin_Def = ""
        for Q2_y in range(1, 18):
            Q2_max, Q2_min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={Q2_y}, Q2-y']
            bin_condition= f"(Q2 < {Q2_max}) && (Q2 > {Q2_min}) && (y < {y_max}) && (y > {y_min})"
            Q2_y_Bin_Def = f"""{Q2_y_Bin_Def}
    if({bin_condition}){{ return {Q2_y}; }}"""
        Q2_y_Bin_Def = f"""{Q2_y_Bin_Def}
    return 0;"""
        gdf = gdf.Redefine("Q2_Y_Bin", Q2_y_Bin_Def) if(gdf.HasColumn("Q2_Y_Bin")) else gdf.Define("Q2_Y_Bin", Q2_y_Bin_Def)
        ##########################################################################################################################################################################################
        ##########################################################################################################################################################################################
        def z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="All"):
            if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
                print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function z_pT_Bin_Standard_Def_Function(Variable_Type='{Variable_Type}', Bin_Version='{Bin_Version}').\nFix input to use anything other than the default calculations of z and pT.")
                Variable_Type  = ""
            Q2_xB_Bin_event_name = "".join(["Q2_xB_Bin" if(Bin_Version not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q2_y_Bin" if(("y_" in Bin_Version) or (Bin_Version == "4")) else "Q2_Y_Bin", "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in ["", "4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
            z_pT_Bin_event_name  = "".join(["z_pT_Bin",                                                                                                                                                          "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in [""])                                               else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
            z_pT_Bin_Standard_Def = "".join([str(New_z_pT_and_MultiDim_Binning_Code), """
                double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
                double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", f""";
                int z_pT_Bin_event_val = 0;
                int Phih_Bin_event_val = 0;
                int MultiDim3D_Bin_val = 0;
                int MultiDim5D_Bin_val = 0;
                if({Q2_xB_Bin_event_name} != 0){{
                    z_pT_Bin_event_val = Find_z_pT_Bin({Q2_xB_Bin_event_name}, z_event_val, pT_event_val);
                    if(z_pT_Bin_event_val == 0){{ MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0; }}
                    else{{
                        if(Phi_h_Bin_Values[{Q2_xB_Bin_event_name}][z_pT_Bin_event_val][0] == 1){{ Phih_Bin_event_val = 1; }}
                        else{{Phih_Bin_event_val = Find_phi_h_Bin(""", str(Q2_xB_Bin_event_name), """, z_pT_Bin_event_val, """, "smeared_vals[11]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "phi_t", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """);}
                        MultiDim3D_Bin_val = Phi_h_Bin_Values[""",     str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][1] + Phih_Bin_event_val;
                        MultiDim5D_Bin_val = Phi_h_Bin_Values[""",     str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][2] + Phih_Bin_event_val;
                    }
                }
                else{ z_pT_Bin_event_val = 0; MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0; }
                """, f"""
                // Refinement of Migration/Overflow Bins
                if((({Q2_xB_Bin_event_name} == 1) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 2) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 3) && ((z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 4) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 5) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 6) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 7) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 8) && ((z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 9) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 10) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 11) && ((z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 12) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 13) && ((z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 14) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 15) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 16) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 23) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 17) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30)))){{
                    z_pT_Bin_event_val = 0; MultiDim3D_Bin_val = 0; MultiDim5D_Bin_val = 0;
                }}
                """, "return z_pT_Bin_event_val;" if(Var_return in ["z_pT", "2D"]) else "return MultiDim3D_Bin_val;" if(Var_return in ["3D"]) else "return MultiDim5D_Bin_val;" if(Var_return in ["5D"]) else """std::vector<int> z_pT_and_MultiDim_Bins = {z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val};
                return z_pT_and_MultiDim_Bins;"""])
            return z_pT_Bin_Standard_Def
        # gdf = gdf.Define("All_MultiDim_Y_bin",              str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="All")))
        # gdf = gdf.Define("z_pT_Bin_Y_bin",                  "All_MultiDim_Y_bin[0]")
        # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t",   "All_MultiDim_Y_bin[1]")
        # gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",        "All_MultiDim_Y_bin[2]")
        gdf = gdf.Redefine("z_pT_Bin_Y_bin", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="2D"))) if(gdf.HasColumn("z_pT_Bin_Y_bin")) else gdf.Define("z_pT_Bin_Y_bin", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="2D")))
        # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="3D")))
        # gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",      str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="5D")))

    print(f"\n{color.BGREEN}Creating New Sub-bins... {color.END_B}({color.ERROR}{args.num_sub_bins}{color.END_B} per variable){color.END}")
    if(args.num_phi_sub_bins > 0):
        print(f"\t{color.Error}Making with {color.END_B}{args.num_phi_sub_bins + args.num_sub_bins}{color.Error} phi_h sub-bins{color.END}\n")
    else:
        print("")
    Find_Q2_y_Bin_Ranges = """
if(Q2_Y_Bin < 1) { return -1; }
double q2min=0., q2max=0., ymin=0., ymax=0.;
// --- Q2 range from bin ---
if      (Q2_Y_Bin>= 1 && Q2_Y_Bin<= 4)  { q2min=2.0; q2max=2.4; }
else if (Q2_Y_Bin>= 5 && Q2_Y_Bin<= 8)  { q2min=2.4; q2max=2.9; }
else if (Q2_Y_Bin>= 9 && Q2_Y_Bin<=12)  { q2min=2.9; q2max=3.7; }
else if (Q2_Y_Bin>=13 && Q2_Y_Bin<=15)  { q2min=3.7; q2max=5.3; }
else if (Q2_Y_Bin>=16 && Q2_Y_Bin<=17)  { q2min=5.3; q2max=7.9; }
// --- y range from bin ---
if      (Q2_Y_Bin == 1 || Q2_Y_Bin == 5 || Q2_Y_Bin == 9  || Q2_Y_Bin ==13 || Q2_Y_Bin ==16) { ymin=0.65; ymax=0.75; }
else if (Q2_Y_Bin == 2 || Q2_Y_Bin == 6 || Q2_Y_Bin ==10  || Q2_Y_Bin ==14 || Q2_Y_Bin ==17) { ymin=0.55; ymax=0.65; }
else if (Q2_Y_Bin == 3 || Q2_Y_Bin == 7 || Q2_Y_Bin ==11  || Q2_Y_Bin ==15)                  { ymin=0.45; ymax=0.55; }
else if (Q2_Y_Bin == 4 || Q2_Y_Bin == 8 || Q2_Y_Bin ==12)                                    { ymin=0.35; ymax=0.45; }
"""
    gdf = gdf.Define("Q2_y_SUB_BINs", f"""{Find_Q2_y_Bin_Ranges}
    double delta_Q2 = ((q2max - q2min)/{args.num_sub_bins});
    double delta_y  = ((ymax  -  ymin)/{args.num_sub_bins});
    int Q2_y_subbin = 0;
    for(double Q2_subbin = q2max; Q2_subbin > q2min; Q2_subbin = Q2_subbin - delta_Q2){{
        if((Q2 <= Q2_subbin) && (Q2 >= (Q2_subbin-delta_Q2))){{
            for(int y_subbin = 0; y_subbin < {args.num_sub_bins}; y_subbin++){{
                Q2_y_subbin = Q2_y_subbin + 1;
                if((y >= ymin+(y_subbin*delta_y)) && (y <= ymin+((y_subbin+1)*delta_y))){{ return Q2_y_subbin; }}
            }}
        }}
        else {{ Q2_y_subbin = Q2_y_subbin + {args.num_sub_bins}; }}
    }}
    return -1; // Error (Should have returned already...)
    """)
    gdf = gdf.Define("z_pT_SUB_BINs", f"""
if((Q2_Y_Bin < 1) || (z_pT_Bin_Y_bin < 1)) {{ return -1; }}
{New_z_pT_and_MultiDim_Binning_Code}
    // From New_z_pT_and_MultiDim_Binning_Code:
       // z_pT_Bin_Borders[Q2_y_Bin][z_pT_Bin][Border_Num]
        // Border_Num = 0 -> z_max
        // Border_Num = 1 -> z_min
        // Border_Num = 2 -> pT_max
        // Border_Num = 3 -> pT_min
        // (Total of 17 Q2-y bins with defined z-pT borders)
    double z_max=0., z_min=0., pT_max=0., pT_min=0.;
    z_max  = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][0];
    z_min  = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][1];
    pT_max = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][2];
    pT_min = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][3];
    double delta_z  = ((z_max  -  z_min)/{args.num_sub_bins});
    double delta_pT = ((pT_max - pT_min)/{args.num_sub_bins});
    int z_pT_subbin = 0;
    for(double z_subbin = z_max; z_subbin > z_min; z_subbin = z_subbin - delta_z){{
        if((z <= z_subbin) && (z >= (z_subbin-delta_z))){{
            for(int pT_subbin = 0; pT_subbin < {args.num_sub_bins}; pT_subbin++){{
                z_pT_subbin = z_pT_subbin + 1;
                if((pT >= pT_min+(pT_subbin*delta_pT)) && (pT <= pT_min+((pT_subbin+1)*delta_pT))){{ return z_pT_subbin; }}
            }}
        }}
        else {{ z_pT_subbin = z_pT_subbin + {args.num_sub_bins}; }}
    }}
    return -1; // Error (Should have returned already...)
    """)
    gdf = gdf.Define("phi_t_bin", """
    if(phi_t < 360){ return int(phi_t/15) + 1; }
    else { return 1; } """)
    delta_phi_Sbin = float(15.0/float(args.num_sub_bins+args.num_phi_sub_bins))
    gdf = gdf.Define("phi_t_SUB_BINs", f" int((phi_t - 15*(phi_t_bin - 1))/{delta_phi_Sbin}) + 1 ")

    gdf = gdf.Define("Full_SUB_BIN_idx", f"""
    if( (Q2_y_SUB_BINs < 0) || (z_pT_SUB_BINs < 0) || (phi_t_SUB_BINs < 0) ){{ return -1; }}
    int q2y_idx = (Q2_y_SUB_BINs - 1)*{args.num_sub_bins}*{args.num_sub_bins};
    int zpT_idx = (q2y_idx + (z_pT_SUB_BINs - 1))*{args.num_sub_bins+args.num_phi_sub_bins};
    return zpT_idx + phi_t_SUB_BINs;
    """)

    # Default_Weights = "1.0"# if(args.use_clasdis) else "weight"
    Default_Weights = "1.0" if(args.use_clasdis) else "Weight" if(gdf.HasColumn("Weight")) else "weight" if(gdf.HasColumn("weight")) else "1.0"
    if(args.use_clasdis):
        print(f"\n{color.BBLUE}Using clasdis File(s){color.END}\n")
    elif(Default_Weights in ["1.0"]):
        Crash_Report(args, crash_message=f"\n{color.Error}WARNING: The default event weights for the proper EvGen events were missing...\n{color.END_R}Should not run the EvGen events with the proper event handling.{color.END}\n", continue_run=False)
    if("Event_Weight" in gdf.GetColumnNames()):
        print(f"\n{color.Error}WARNING: 'Event_Weight' is already defined in the RDataFrame...{color.END}\n")
    elif(args.json_weights):
        print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file: {color.BPINK}{str(args.json_file_in).split('/')[-1]}{color.END}\n")
        Fit_Pars_Raw  = load_json_file(args.json_file_in)
        Fit_Pars_Flat = Flatten_Fit_Pars_For_CPP_Map(Fit_Pars_Raw, args, prefer_normalized=True)
        # Build the C++ initialization string (flat map: "A_#_#", "B_#_#", "C_#_#")
        cpp_items = []
        for key, val in Fit_Pars_Flat.items():
            try:
                vv = float(val)
            except Exception:
                continue
            if(not numpy.isfinite(vv)):
                continue
            cpp_items.append(f'{{"{key}", {vv}}}')
        cpp_map_str = "{" + ",".join(cpp_items) + "}"
        ROOT.gInterpreter.Declare(f"""
        #include <map>
        #include <string>
        #include <cmath>
        #include "TMath.h"
        std::map<std::string, double> Fit_Pars = {cpp_map_str};
        double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h){{
            std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            double Par_A = (Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 1.0);
            double Par_B = (Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0);
            double Par_C = (Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0);
            double phi_rad = phi_h * TMath::DegToRad();
            return Par_A*(1.0 + Par_B*std::cos(phi_rad) + Par_C*std::cos(2.0*phi_rad));
        }}""")
        gdf = gdf.Define("Event_Weight", f"{Default_Weights}*ComputeWeight(Q2_Y_Bin, z_pT_Bin_Y_bin, phi_t)")
    else:
        gdf = gdf.Define("Event_Weight", Default_Weights)
    gdf = gdf.Filter("MM > 1.5") # Apply Missing Mass Cut to exclude the 'exclusive' phase space from my bins
    gdf = gdf.Filter("(Q2_y_SUB_BINs  != -1) && (z_pT_SUB_BINs  != -1) && (phi_t_SUB_BINs != -1)") # Remove all events outside my nominal binning scheme
    return gdf

def Evaluate_Weights(List_of_BCBins_In, SumOfWeights_L_In, Full_Run__List_In, args):
    if(not args.test):
        print(f"{color.BCYAN}Triggering Event Evaluation on {color.END_B}{len(Full_Run__List_In)}{color.BCYAN} Sub-Bins...{color.END}\n")
        # One trigger for everything
        ROOT.RDF.RunGraphs(Full_Run__List_In)
        for (nom_name, sub_name), ptr in SumOfWeights_L_In.items():
            List_of_BCBins_In[nom_name][sub_name] = float(ptr.GetValue())
        print(f"{color.BGREEN}Evaluations are Complete{color.END}")
        print(f"{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
        # for     ii in List_of_BCBins_In:
        #     for jj in List_of_BCBins_In[ii]:
        #         print(f"List_of_BCBins_In['{ii}']['{jj}'] = {List_of_BCBins_In[ii][jj]}")
        print(f"{color.BBLUE}Saving To JSON File: {color.BPINK}{args.json_file_out}{color.END}")
        save_dict_to_json(data_to_save=List_of_BCBins_In, json_file=args.json_file_out)
        args.timer.time_elapsed()
    elif(args.verbose):
        print(f"\n{color.RED}Running as a test (no event evaluations)...{color.END}\n")
        args.timer.time_elapsed()
    else:
        print(f"\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}\n")
    SumOfWeights_L_In.clear()
    Full_Run__List_In.clear()
    return List_of_BCBins_In, SumOfWeights_L_In, Full_Run__List_In

def Get_Bin_Contents_for_BC(args):
    print(f"\n{color.BGREEN}Looping through sub-bins...{color.END}\n")
    List_of_BCBins = {"keys": {"Nominal-Bins": "Bin (Q2_y_Bin-z_pT_Bin-phih_bin)", "Sub-Bins": "Bin (Q2_y_Bin-Q2y_Sbin)-(z_pT_Bin-zpT_Sbin)-(phih_bin-phi_Sbin)"}}
    SumOfWeights_L = {} # Initial List for `List_of_BCBins` that will pass all the sums to the final list after the dataframe evaluations
    Full_Run__List = [] # Used to store the sums in `SumOfWeights_L` in a way that is easily calculable at the end of the loops
    Q2_y_Bin_Range = range(1, 18) if(args.Q2_y_Bin == -1) else [args.Q2_y_Bin]
    z_pT_Bin_Range = range(1, 37) if(args.z_pT_Bin == -1) else [args.z_pT_Bin]
    phih_Bin_Range = range(1, 25) if(args.phih_Bin == -1) else [args.phih_Bin]
    Total_Num_SBin = 0
    for                     Q2_y_Bin in Q2_y_Bin_Range:
        gdf_Q2_y_Bin         = gdf.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")
        for                 z_pT_Bin in z_pT_Bin_Range:
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                if(args.verbose and (z_pT_Bin < 35)):
                    print(f"\t{color.Error}Skip Bin {Q2_y_Bin}-{z_pT_Bin}{color.END}")
                continue
            gdf_z_pT_Bin     = gdf_Q2_y_Bin.Filter(f"z_pT_Bin_Y_bin == {z_pT_Bin}")
            for             phih_bin in phih_Bin_Range:
                gdf_phih_Bin = gdf_z_pT_Bin.Filter(f"phi_t_bin == {phih_bin}")
                Nominal_bin_name = f"Bin ({Q2_y_Bin}-{z_pT_Bin}-{phih_bin})"
                List_of_BCBins[Nominal_bin_name] = {}
                for         Q2y_Sbin in range(1, int((args.num_sub_bins*args.num_sub_bins)+1)):
                    gdf_Q2y_SBin         = gdf_phih_Bin.Filter(f"Q2_y_SUB_BINs == {Q2y_Sbin}")
                    for     zpT_Sbin in range(1, int((args.num_sub_bins*args.num_sub_bins)+1)):
                        gdf_zpT_SBin     = gdf_Q2y_SBin.Filter(f"z_pT_SUB_BINs == {zpT_Sbin}")
                        for phi_Sbin in range(1, int((args.num_sub_bins+args.num_phi_sub_bins)+1)):
                            gdf_phi_SBin = gdf_zpT_SBin.Filter(f"phi_t_SUB_BINs == {phi_Sbin}")
                            sub_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-{zpT_Sbin})-({phih_bin}-{phi_Sbin})"
                            sumw = gdf_phi_SBin.Sum("Event_Weight") # Book the action; do NOT GetValue() yet
                            SumOfWeights_L[(Nominal_bin_name, sub_bin_name)] = sumw
                            Full_Run__List.append(sumw)
                            if(args.verbose):
                                print(f"\t\t{color.BOLD}Collected Sub-{sub_bin_name}{color.END}")
                                print(f"\t\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
                print(f"\t{color.BBLUE}Collected all sub-bins in {Nominal_bin_name}{color.END}")
                Total_Num_SBin += len(Full_Run__List)
                List_of_BCBins, SumOfWeights_L, Full_Run__List = Evaluate_Weights(List_of_BCBins, SumOfWeights_L, Full_Run__List, args)
    print(f"\n{color.BGREEN}Done Collecting all the bin event counts {color.END_B}(Total Number of Sub-bins Collected = {Total_Num_SBin}){color.END}")
    return List_of_BCBins, Total_Num_SBin

def Make_SubBin_TH2_SumW(gdf, args, Q2_y_Bin, z_pT_Bin):
    # Build ONE TH2D for a single (Q2_y_Bin, z_pT_Bin)
    #   X axis: Full_SUB_BIN_idx
    #   Y axis: phi_t_bin (1..24)
    #   Weight: Event_Weight
    Nsub = int((args.num_sub_bins**4)*(args.num_sub_bins+args.num_phi_sub_bins))
    hist_name     = f"Histogram Bin ({Q2_y_Bin}-{z_pT_Bin})-(Num SubBins={args.num_sub_bins})"
    hist_titl     = f"#splitline{{{root_color.Bold}{{Generated #phi_{{h}} vs Sub-Bin Indexes from {'EvGen' if(not args.use_clasdis) else 'clasdis'}}}}}{{Made with {args.num_sub_bins} Sub-Bins per Kinematic Variable}}"
    if(args.num_phi_sub_bins > 0):
        hist_name = f"{hist_name}-(Extra phi_h SubBins={args.num_phi_sub_bins})"
        hist_titl = f"#splitline{{{hist_titl}}}{{#scale[0.75]{{#phi_{{h}} Uniquely Used {args.num_sub_bins+args.num_phi_sub_bins} Sub-Bins instead}}}}"
    hist_titl     = f"#splitline{{{hist_titl}}}{{Made for Q^{{2}}-y-z-P_{{T}} Bin: ({Q2_y_Bin}-{z_pT_Bin})}}"
    # hist_titl     = f"#splitline{{{hist_titl}}}{{Number of Sub-Bins Per Variable = {args.num_sub_bins}}}"
    if(args.json_weights):
      hist_titl   = f"#splitline{{{hist_titl}}}{{Used Injected Modulation Weights}}"
    if(args.histo_title not in ["", None]):
      hist_titl   = f"#splitline{{{hist_titl}}}{{{args.histo_title}}}"
    hist_titl     = f"{hist_titl}; Sub-Bin Indexes; #phi_{{h}} Bins"
    hmodel        = (hist_name, hist_titl, int(Nsub+2), -0.5, Nsub+1.5, 24, 0.5, 24.5)
    hist_ptr      = gdf.Histo2D(hmodel, "Full_SUB_BIN_idx", "phi_t_bin", "Event_Weight")
    return hist_ptr

def Create_Histograms_for_BC(args):
    print(f"\n{color.BGREEN}Creating Sub-Bin Histograms...{color.END}\n")
    List_of_Histos = {}
    Q2_y_Bin_Range = range(1, 18) if(args.Q2_y_Bin == -1) else [args.Q2_y_Bin]
    z_pT_Bin_Range = range(1, 37) if(args.z_pT_Bin == -1) else [args.z_pT_Bin]
    for     Q2_y_Bin in Q2_y_Bin_Range:
        gdf_Q2_y_Bin         = gdf.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")
        for z_pT_Bin in z_pT_Bin_Range:
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                if(args.verbose and (z_pT_Bin < 35)):
                    print(f"\t{color.Error}Skip Bin {Q2_y_Bin}-{z_pT_Bin}{color.END}")
                continue
            gdf_z_pT_Bin     = gdf_Q2_y_Bin.Filter(f"z_pT_Bin_Y_bin == {z_pT_Bin}")
            Nominal_bin_name = f"Histogram Bin ({Q2_y_Bin}-{z_pT_Bin})-(Num SubBins={args.num_sub_bins})"
            if(args.num_phi_sub_bins > 0):
                Nominal_bin_name = f"{Nominal_bin_name}-(Extra phi_h SubBins={args.num_phi_sub_bins})"
            List_of_Histos[Nominal_bin_name] = Make_SubBin_TH2_SumW(gdf_z_pT_Bin, args, Q2_y_Bin, z_pT_Bin)
    print(f"\n{color.BBLUE}Done Creating All Sub-bin Histograms {color.END_B}(Total = {len(List_of_Histos)}){color.END}")
    print(f"{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    return List_of_Histos

def Evaluate_And_Write_Histograms(hist_ptrs, args):
    # Evaluate all booked histograms in ONE trigger, then write them all at once
    # hist_ptrs can be either:
    #   (A) dict: {"Histogram Bin (Q2y-zpt)": RResultPtr<TH2D>, ...}
    #   (B) list/tuple: [RResultPtr<TH2D>, ...]
    if(args.test):
        print(f"\n{color.BLUE}Would have saved the ROOT file as: {color.ERROR}{args.root_file_out}{color.END}")
        return len(hist_ptrs)
    if(isinstance(hist_ptrs, dict)):
        ptr_list = [hist_ptrs[key] for key in sorted(hist_ptrs.keys())]
    else:
        ptr_list = list(hist_ptrs)
    if((ptr_list is None) or (len(ptr_list) == 0)):
        raise ValueError("Evaluate_And_Write_Histograms(...): hist_ptrs is empty")
    out_path = str(args.root_file_out)
    out_dir  = os.path.dirname(os.path.abspath(out_path))
    if((out_dir != "") and (not os.path.exists(out_dir))):
        os.makedirs(out_dir, exist_ok=True)
    write_mode = "UPDATE" if(os.path.exists(out_path)) else "RECREATE"
    print(f"\n{color.BBLUE}{'Updating the' if(write_mode == 'UPDATE') else 'Creating a new'} ROOT file: {color.BPINK}{args.root_file_out}{color.END}")
    print(f"\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    ROOT.RDF.RunGraphs(ptr_list)
    print(f"{color.BLUE}Time After 'RunGraphs':{color.END}\n\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    fout = ROOT.TFile(out_path, write_mode)
    if((fout is None) or (fout.IsZombie())):
        raise RuntimeError(f"Evaluate_And_Write_Histograms(...): failed to open ROOT file: {out_path}")
    fout.cd()
    for ptr in ptr_list:
        hist = ptr.GetValue()
        # hist.Sumw2(True)
        hist.Write("", ROOT.TObject.kOverwrite)
    fout.Close()
    print(f"\n{color.BGREEN}ROOT FILE HAS BEEN SAVED{color.END}\n")
    return len(hist_ptrs)

def parse_histogram_name(hist_name):
    # Expected name pattern from Make_SubBin_TH2_SumW:
    #   "Histogram Bin (Q2y-zpt)-(Num SubBins=N)-(Extra phi_h SubBins=N)"
    # Returns: (Q2_y_Bin, z_pT_Bin, num_sub_bins, extra_phi) or (None, None, None, None) if no match.
    match = re.search(r"Histogram Bin \((\d+)-(\d+)\)-\(Num SubBins=(\d+)\)", str(hist_name))
    if(not match):
        return None, None, None, None
    Q2y = int(match.group(1))
    zpt = int(match.group(2))
    nsub = int(match.group(3))
    match_phi = re.search(r"\-\(Extra phi_h SubBins=(\d+)\)", str(hist_name))
    extra_phi = int(match_phi.group(1)) if(match_phi) else 0
    return Q2y, zpt, nsub, extra_phi

def mean_and_weighted_mean(contents, errors, include_zero_bins=True):
    if(len(contents) != len(errors)):
        raise ValueError("contents and errors must have the same length")
    len_content = len(contents)
    if(len_content == 0):
        return None

    filtered_contents = []
    filtered_errors   = []
    for content, error in zip(contents, errors):
        if(include_zero_bins or (content != 0.0)):
            filtered_contents.append(content)
            filtered_errors.append(error)

    if(len(filtered_contents) == 0):
        return {"ave": 0.0,
                "ave_err": 0.0,
                "weighted_ave": 0.0,
                "weighted_ave_err": 0.0,
                "stddev_of_bin_contents": 0.0,
                "ave_err_from_bin_errors": 0.0,
                "weighted_ave_err_from_bin_errors": 0.0,
                "num_bins_used_for_averages": 0,
                "num_bins_available_for_averages": len_content,
                "non_zero_bin_averages_used": (not include_zero_bins)}

    len_filtered_content = len(filtered_contents)

    # --- unweighted mean ---
    sum_c = 0.0
    for c in filtered_contents:
        sum_c += c
    mean = (sum_c / len_filtered_content)

    # --- standard deviation of the bin contents ---
    sum_sq_diff = 0.0
    for c in filtered_contents:
        sum_sq_diff += ((c - mean)*(c - mean))
    stddev_of_bin_contents = ROOT.TMath.Sqrt(sum_sq_diff / len_filtered_content) if(len_filtered_content > 0) else 0.0

    # --- standard error of the mean (NEW default uncertainty) ---
    standard_error_of_mean = (stddev_of_bin_contents / ROOT.TMath.Sqrt(len_filtered_content)) if(len_filtered_content > 0) else 0.0

    # --- old propagated mean error from sub-bin bin errors (renamed, no longer default) ---
    sum_e2 = 0.0
    for e in filtered_errors:
        sum_e2 += (e*e)
    mean_err_from_bin_errors = (ROOT.TMath.Sqrt(sum_e2) / len_filtered_content)

    # --- weighted mean (inverse-variance) ---
    num, den = 0.0, 0.0
    for c, e in zip(filtered_contents, filtered_errors):
        if(e <= 0.0):
            continue
        w    = (1.0 / (e*e))
        num += (c * w)
        den += w
    if(den > 0.0):
        wmean = (num / den)
        weighted_mean_err_from_bin_errors = ROOT.TMath.Sqrt(1.0 / den)
    else:
        wmean = float("nan")
        weighted_mean_err_from_bin_errors = float("nan")

    return {"ave": mean,
            "ave_err": standard_error_of_mean,
            "weighted_ave": wmean,
            "weighted_ave_err": standard_error_of_mean,
            "stddev_of_bin_contents": stddev_of_bin_contents,
            "ave_err_from_bin_errors": mean_err_from_bin_errors,
            "weighted_ave_err_from_bin_errors": weighted_mean_err_from_bin_errors,
            "num_bins_used_for_averages": len_filtered_content,
            "num_bins_available_for_averages": len_content,
            "non_zero_bin_averages_used": (not include_zero_bins)}

def BC_ratio_and_error(val_num, err_num, val_den, err_den):
    if(val_den == 0.0):
        return float("nan"), float("nan")
    if(val_num == 0.0):
        return 0.0, 0.0
    ratio = (val_num / val_den)
    rel_err2 = 0.0
    if(val_num != 0.0):
        rel_err2 += (err_num / val_num)**2
    if(val_den != 0.0):
        rel_err2 += (err_den / val_den)**2
    ratio_err = abs(ratio) * ROOT.TMath.Sqrt(rel_err2)
    return ratio, ratio_err

# ------------------------------------------------------------
# Core: read histograms and compute per-nominal-bin outputs
# ------------------------------------------------------------

def Compute_BC_Factors_From_SubBin_Histograms(args, include_zero_bins=True, write_full_diagnostics=False):
    # Self-contained function:
    #   - opens the ROOT file (default: args.root_file_out)
    #   - reads TH2 histograms
    #   - computes avg vs center per nominal (Q2y, zpt, phi_nom)
    #   - writes ONE number per nominal bin to JSON (plus optional diagnostics)
    root_path = args.root_file_out
    verbose   = args.verbose
    if((root_path is None) or (str(root_path).strip() == "")):
        raise ValueError("Compute_BC_Factors_From_SubBin_Histograms(...): empty root_path")
    if(not os.path.exists(root_path)):
        raise FileNotFoundError(f"ROOT file does not exist: {root_path}")

    num_sub_bins = int(args.num_sub_bins)
    Nsub = int((num_sub_bins**4)*(num_sub_bins+args.num_phi_sub_bins))
    full_center_idx = int((Nsub)/2)+1

    # Output: one value per nominal bin
    out = {"meta": { "root_file": str(root_path),
                     "num_sub_bins": int(num_sub_bins),
                     "extra_num_phi_sub_bins": int(args.num_phi_sub_bins),
                     "Nsub_per_nominal_bin": int(Nsub),
                     "center_subbin": int(full_center_idx),
                     "include_zero_bins_in_averages": bool(include_zero_bins),
                     "definition": {"bc_factor": "avg_subbin_content / center_subbin_content",
                                    "avg": "mean over all sub-bins in the nominal bin (optionally includes zeros)",
                                    "ave_err": "standard error of the mean from the selected sub-bin contents (new default uncertainty)",
                                    "weighted_ave_err": "standard error of the mean from the selected sub-bin contents (new default uncertainty also used for the weighted average entry)",
                                    "stddev_of_bin_contents": "population standard deviation of the selected sub-bin contents",
                                    "ave_err_from_bin_errors": "old propagated mean error from the selected sub-bin bin errors",
                                    "weighted_ave_err_from_bin_errors": "old inverse-variance weighted mean error from the selected sub-bin bin errors",
                                    "nominal_bin": "sum of all sub-bin contents, with nominal error from quadrature of the sub-bin bin errors when available"},
                     "email_message": args.email_message
                   },
           "results": {},
           "full_contents": {},
           "nominal_contents": {}
          }

    print(f"\n{color.BBLUE}Opening ROOT file: {color.BPINK}{root_path}{color.END}")
    if(verbose):
        print(f"\tnum_sub_bins={num_sub_bins}  => Nsub={Nsub}")
        print(f"\tcenter Full_SUB_BIN_idx={full_center_idx}")
        print(f"\tinclude_zero_bins_in_averages={include_zero_bins}")
    print("")

    fin = ROOT.TFile.Open(str(root_path), "READ")
    if((fin is None) or (fin.IsZombie())):
        raise RuntimeError(f"Failed to open ROOT file: {root_path}")

    # Collect all TH2 histograms by iterating keys
    keys = fin.GetListOfKeys()
    hist_names = []
    for key in keys:
        name = str(key.GetName())
        obj_class = str(key.GetClassName())
        if("TH2" in obj_class):
            hist_names.append(name)
    if(verbose):
        print(f"Found {len(hist_names)} TH2 histograms in file")

    Count_of_Nominal_Bins = 0
    for hist_name in sorted(hist_names): # Loop histograms
        h = fin.Get(hist_name)
        if(h is None):
            continue
        Q2_y_Bin, z_pT_Bin, nsub_in_name, extra_phi_in_name = parse_histogram_name(hist_name)
        if(None in [Q2_y_Bin, z_pT_Bin]):
            if(verbose):
                print(f"\t{color.RED}Skipping unrecognized histogram name: {color.ERROR}{hist_name}{color.END}")
            continue
        if((args.Q2_y_Bin not in [-1, None, Q2_y_Bin]) or (args.z_pT_Bin not in [-1, None, z_pT_Bin])):
            if(verbose):
                print(f"\t{color.RED}Skipping unselected histogram bin: {color.ERROR}{hist_name}{color.END}")
            continue
        if((nsub_in_name is not None) and (int(nsub_in_name) != int(num_sub_bins))):
            print(f"\n{color.Error}WARNING: num_sub_bins mismatch in {hist_name}: name has {nsub_in_name}, args has {num_sub_bins}{color.END}\n")
            raise ValueError("Compute_BC_Factors_From_SubBin_Histograms Warning: num_sub_bins mismatch in hist_name.")
        if((extra_phi_in_name is not None) and (int(extra_phi_in_name) != int(args.num_phi_sub_bins))):
            Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END} ROOT file histogram '{hist_name}' was made with Extra phi_h SubBins={extra_phi_in_name}, but you ran with --num_phi_sub_bins={args.num_phi_sub_bins}. This will break center-subbin logic.\n")
        xax = h.GetXaxis()
        yax = h.GetYaxis()
        for phi_nom in range(1, 24 + 1):
            phibin = yax.FindBin(phi_nom)
            if((phibin < 1) or (phibin > yax.GetNbins())):
                continue
            nom_key = f"Bin ({Q2_y_Bin}-{z_pT_Bin}-{phi_nom})"
            out["results"][nom_key] = {}
            if(args.phih_Bin not in [None, -1, phibin]):
                if(verbose):
                    print(f"\t{color.RED}Skipping unselected Nominal Bin: {color.ERROR}{nom_key}{color.END}")
                continue
            nonBinContentsList = []
            nonBin_Errors_List = []
            for sbinval in range(1, Nsub + 1):
                sbin = xax.FindBin(sbinval)
                if((sbin < 1) or (sbin > xax.GetNbins())):
                    continue
                content = h.GetBinContent(sbin, phibin)
                error   = h.GetBinError(sbin, phibin)
                if(write_full_diagnostics or (sbinval in [full_center_idx])):
                    sub_bin_key = f"Nominal {nom_key}-(SubBin={sbinval})"
                    out["full_contents"][sub_bin_key] = {"Content": content, "Error": error}
                    if(sbinval in [full_center_idx]):
                        out["results"][nom_key]["Center Sub-Bin"] = {"Content": content, "Error": error}
                nonBinContentsList.append(content)
                nonBin_Errors_List.append(error)

            try:
                nominal_content = 0.0
                nominal_err_sq  = 0.0
                for content_val, error_val in zip(nonBinContentsList, nonBin_Errors_List):
                    nominal_content += content_val
                    nominal_err_sq  += (error_val*error_val)
                nominal_info = {"Content": nominal_content, "Error": ROOT.TMath.Sqrt(nominal_err_sq)}
                out["results"][nom_key]["Nominal Bin"] = nominal_info
                out["nominal_contents"][nom_key] = nominal_info
            except Exception as Nominal_Bin_Exception:
                if(verbose):
                    print(f"{color.BYELLOW}WARNING:{color.END} Could not save nominal bin content/error for {nom_key}. Continuing without it.")
                    print(f"\t{Nominal_Bin_Exception}")

            mean_info = mean_and_weighted_mean(nonBinContentsList, nonBin_Errors_List, include_zero_bins=include_zero_bins)
            out["results"][nom_key].update(mean_info)
            BC_norm, BC_norm_err = BC_ratio_and_error(out["results"][nom_key]["ave"],          out["results"][nom_key]["ave_err"],          out["results"][nom_key]["Center Sub-Bin"]["Content"], out["results"][nom_key]["Center Sub-Bin"]["Error"])
            BC_Wave, BC_Wave_err = BC_ratio_and_error(out["results"][nom_key]["weighted_ave"], out["results"][nom_key]["weighted_ave_err"], out["results"][nom_key]["Center Sub-Bin"]["Content"], out["results"][nom_key]["Center Sub-Bin"]["Error"])
            out["results"][nom_key].update({"BC_Factor": BC_norm, "BC_Factor_Err": BC_norm_err, "BC_Factor_Wave": BC_Wave, "BC_Factor_Wave_Err": BC_Wave_err})
            Count_of_Nominal_Bins += 1
        if(verbose):
            print(f"{color.BBLUE}Processed histogram for (Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}){color.END_B} -> 24 nominal phi bins{color.END}")
        print(f"{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")

    fin.Close()
    print(f"\n{color.BGREEN}Done Accessing the ROOT File{color.END_B} (Total Num of Nominal Bins Processed = {Count_of_Nominal_Bins}){color.END}")
    if(not args.test):
        print(f"{color.BBLUE}Saving To JSON File: {color.BPINK}{args.json_file_out}{color.END}")
        save_dict_to_json(data_to_save=out, json_file=args.json_file_out)
        args.timer.time_elapsed()
    elif(args.verbose):
        print(f"\n{color.RED}Running as a test (no JSON file save)...{color.END}\n")
        args.timer.time_elapsed()
    else:
        print(f"\t{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}\n")
    return out, Count_of_Nominal_Bins

# ------------------------------------------------------------
# Optional plot: Center vs Average vs nominal phi_h bin
# ------------------------------------------------------------
def Plot_BC_Subbin_Inputs_From_JSON(args, main_pad=None, save_plot=True, q2_y_bin_override=None, z_pT_bin_override=None, json_data=None, draw_legend=True):
    q2_y_bin_to_use = args.Q2_y_Bin if(q2_y_bin_override in [None]) else q2_y_bin_override
    z_pT_bin_to_use = args.z_pT_Bin if(z_pT_bin_override in [None]) else z_pT_bin_override

    if((q2_y_bin_to_use in [-1, None]) or (z_pT_bin_to_use in [-1, None])):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} '--make_plot_images' requires a single '--Q2_y_Bin' and '--z_pT_Bin' (not -1). Skipping plot.{color.END}\n")
    json_path = str(args.json_file_out)
    if(json_data in [None]):
        if(not os.path.exists(json_path)):
            Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not exist.\n{color.END}File Input Was: {json_path}\n")
        json_data = load_json_file(json_path)
    if((not isinstance(json_data, dict)) or ("results" not in json_data) or (not isinstance(json_data["results"], dict))):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not have the expected schema with a top-level 'results' dict.\n{color.END}File Input Was: {json_path}\n")
    results = json_data["results"]
    # Build output histograms: 24 nominal phi bins (1..24)
    hname_center = f"h_center_Q2y{q2_y_bin_to_use}_zpt{z_pT_bin_to_use}"
    hname_ave    = f"h_ave_Q2y{q2_y_bin_to_use}_zpt{z_pT_bin_to_use}"
    title_base = f"#splitline{{BC Factor Sub-Bin Inputs}}{{#scale[0.75]{{For Q^{{2}}-y-z-P_{{T}} Bin: ({q2_y_bin_to_use}-{z_pT_bin_to_use})}}}}"
    h_center = ROOT.TH1D(hname_center, f"{title_base}; #phi_{{h}} Bin; Sub-Bin Contents", 24, 0.5, 24.5)
    h_ave    = ROOT.TH1D(hname_ave,    f"{title_base}; #phi_{{h}} Bin; Sub-Bin Contents", 24, 0.5, 24.5)
    # Fill from JSON
    max_y, min_y = 0.0, 0.0
    for phi_bin in range(1, 24 + 1):
        nom_key = f"Bin ({q2_y_bin_to_use}-{z_pT_bin_to_use}-{phi_bin})"
        entry = results.get(nom_key, {})
        # Defaults to 0 if missing
        c_val, c_err = 0.0, 0.0
        a_val, a_err = 0.0, 0.0
        if(isinstance(entry, dict)):
            csb = entry.get("Center Sub-Bin", {})
            if(isinstance(csb, dict)):
                try:
                    c_val = float(csb.get("Content", 0.0))
                except Exception:
                    c_val = 0.0
                try:
                    c_err = float(csb.get("Error", 0.0))
                except Exception:
                    c_err = 0.0
            try:
                a_val = float(entry.get("ave", 0.0))
            except Exception:
                a_val = 0.0
            try:
                a_err = float(entry.get("ave_err", 0.0))
            except Exception:
                a_err = 0.0
        h_center.SetBinContent(phi_bin, c_val)
        h_center.SetBinError(phi_bin,   c_err)
        h_ave.SetBinContent(phi_bin,    a_val)
        h_ave.SetBinError(phi_bin,      a_err)
        max_y = max([max_y, c_val + c_err, a_val + a_err])
        min_y = min([min_y, c_val - c_err, a_val - a_err])
    # Style (different colors, same pad)
    h_center.SetLineColor(ROOT.kSpring + 10)
    h_center.SetMarkerColor(ROOT.kSpring + 10)
    h_center.SetMarkerStyle(20)
    h_center.SetLineWidth(2)
    h_ave.SetLineColor(ROOT.kViolet + 1)
    h_ave.SetMarkerColor(ROOT.kViolet + 1)
    h_ave.SetMarkerStyle(21)
    h_ave.SetLineWidth(2)
    h_ave.GetYaxis().SetRangeUser(min([0.0, 0.8*min_y, 1.2*min_y]), max([0.0, 0.8*max_y, 1.2*max_y]))

    if(main_pad in [None]):
        Save_Name = f'{f"{args.image_name}_" if(args.image_name not in [""]) else ""}BC_Subbin_Comparisons_for_Q2_y_Bin_{q2_y_bin_to_use}_z_pT_Bin_{z_pT_bin_to_use}'
        c = ROOT.TCanvas(Save_Name, Save_Name, 1200, 800)
        pad = c.cd()
        # pad.SetBottomMargin(float(bottom_margin))
        pad.SetTopMargin(0.175)
        pad.SetLeftMargin(0.125)
        pad.SetRightMargin(0.025)
    else:
        Save_Name = None
        c = None
        pad = main_pad
        pad.cd()
        pad.SetTopMargin(0.175)
        pad.SetLeftMargin(0.125)
        pad.SetRightMargin(0.025)

    # Draw both on the same pad
    h_ave.Draw("E1")
    h_center.Draw("E1 SAME")

    leg = None
    if(draw_legend):
        # leg = ROOT.TLegend(0.62, 0.76, 0.88, 0.88)
        leg = ROOT.TLegend(0.38, 0.15, 0.64, 0.32)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.AddEntry(h_center, "#scale[2]{Center Sub-Bin Content}", "lep")
        leg.AddEntry(h_ave,    "#scale[2]{Average Sub-Bin Content}", "lep")
        leg.Draw()

    stat_box = None
    if(args.show_bin_stats):
        total_events = 0.0
        for phi_bin in range(1, 25):
            nom_key = f"Bin ({q2_y_bin_to_use}-{z_pT_bin_to_use}-{phi_bin})"
            entry = results.get(nom_key, {})
            if(isinstance(entry, dict)):
                nom = entry.get("Nominal Bin", {})
                if(isinstance(nom, dict)):
                    try:
                        total_events += float(nom.get("Content", 0.0))
                    except Exception:
                        pass
        stat_box = ROOT.TPaveText(0.38, 0.35, 0.64, 0.42, "NDC")
        stat_box.SetBorderSize(0)
        stat_box.SetFillStyle(0)
        stat_box.SetTextAlign(22)
        stat_box.SetTextFont(42)
        stat_box.SetTextSize(0.035)
        stat_box.AddText(f"Sum of Events in All Sub-Bins: {int(total_events):,}")
        stat_box.Draw()

    pad.Modified()
    pad.Update()

    if(save_plot and (Save_Name not in [None])):
        args.Save_Name = f'{Save_Name}.{args.File_Format}'
        if(not args.test):
            c.SaveAs(args.Save_Name)
            print(f"\n{color.BGREEN}Saved BC sub-bin comparison plot:{color.END} {color.BPINK}{args.Save_Name}{color.END}\n")
        else:
            print(f"\n{color.BBLUE}WOULD HAVE saved BC sub-bin comparison plot:{color.END} {color.BPINK}{args.Save_Name}{color.END}\n")
        return args

    return {"h_center": h_center,
            "h_ave": h_ave,
            "legend": leg,
            "pad": pad,
            "stat_box": stat_box}

def Plot_BC_Factor_From_JSON(args, main_pad=None, save_plot=True, q2_y_bin_override=None, z_pT_bin_override=None, json_data=None, draw_legend=True):
    q2_y_bin_to_use = args.Q2_y_Bin if(q2_y_bin_override in [None]) else q2_y_bin_override
    z_pT_bin_to_use = args.z_pT_Bin if(z_pT_bin_override in [None]) else z_pT_bin_override

    if((q2_y_bin_to_use in [-1, None]) or (z_pT_bin_to_use in [-1, None])):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} '--make_plot_BC_factor' requires a single '--Q2_y_Bin' and '--z_pT_Bin' (not -1). Skipping plot.{color.END}\n")
    json_path = str(args.json_file_out)
    if(json_data in [None]):
        if(not os.path.exists(json_path)):
            Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not exist.\n{color.END}File Input Was: {json_path}\n")
        json_data = load_json_file(json_path)
    if((not isinstance(json_data, dict)) or ("results" not in json_data) or (not isinstance(json_data["results"], dict))):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not have the expected schema with a top-level 'results' dict.\n{color.END}File Input Was: {json_path}\n")

    results = json_data["results"]

    hname_bc = f"h_bc_Q2y{q2_y_bin_to_use}_zpt{z_pT_bin_to_use}"
    title_base = f"#splitline{{BC Factor}}{{#scale[0.75]{{For Q^{{2}}-y-z-P_{{T}} Bin: ({q2_y_bin_to_use}-{z_pT_bin_to_use})}}}}"
    h_bc = ROOT.TH1D(hname_bc, f"{title_base}; #phi_{{h}} Bin; BC Factor", 24, 0.5, 24.5)

    max_y, min_y = 0.0, 0.0
    for phi_bin in range(1, 24 + 1):
        nom_key = f"Bin ({q2_y_bin_to_use}-{z_pT_bin_to_use}-{phi_bin})"
        entry = results.get(nom_key, {})

        bc_val, bc_err = 0.0, 0.0
        if(isinstance(entry, dict)):
            try:
                bc_val = float(entry.get("BC_Factor", 0.0))
            except Exception:
                bc_val = 0.0
            try:
                bc_err = float(entry.get("BC_Factor_Err", 0.0))
            except Exception:
                bc_err = 0.0

        if(not numpy.isfinite(bc_val)):
            bc_val = 0.0
        if((not numpy.isfinite(bc_err)) or (bc_err < 0.0)):
            bc_err = 0.0

        h_bc.SetBinContent(phi_bin, bc_val)
        h_bc.SetBinError(phi_bin,   bc_err)

        max_y = max([max_y, bc_val + bc_err])
        min_y = min([min_y, bc_val - bc_err])

    # Style (single histogram, same general look/feel)
    h_bc.SetLineColor(ROOT.kAzure + 1)
    h_bc.SetMarkerColor(ROOT.kAzure + 1)
    h_bc.SetMarkerStyle(20)
    h_bc.SetLineWidth(2)
    if(not args.BC_Zoom):
        h_bc.GetYaxis().SetRangeUser(min([0.0, 0.8*min_y, 1.2*min_y]), max([0.0, 0.8*max_y, 1.2*max_y]))
    else:
        h_bc.GetYaxis().SetRangeUser(max([0.0, 0.5*min_y if(abs(min_y) > 0) else 0.5*max_y]), max([0.0, 0.8*max_y, 1.2*max_y]))

    if(main_pad in [None]):
        Save_Name = f'{f"{args.image_name}_" if(args.image_name not in [""]) else ""}BC_Factor_for_Q2_y_Bin_{q2_y_bin_to_use}_z_pT_Bin_{z_pT_bin_to_use}'
        c = ROOT.TCanvas(Save_Name, Save_Name, 1200, 800)
        pad = c.cd()
        pad.SetTopMargin(0.175)
        pad.SetLeftMargin(0.125)
        pad.SetRightMargin(0.025)
    else:
        Save_Name = None
        c = None
        pad = main_pad
        pad.cd()
        pad.SetTopMargin(0.175)
        pad.SetLeftMargin(0.125)
        pad.SetRightMargin(0.025)

    h_bc.Draw("E1")

    leg = None
    if(draw_legend):
        leg = ROOT.TLegend(0.38, 0.15, 0.64, 0.32)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.AddEntry(h_bc, "#scale[2]{BC Factor}", "lep")
        leg.Draw()

    pad.Modified()
    pad.Update()

    if(save_plot and (Save_Name not in [None])):
        args.Save_Name_BC_Factor = f'{Save_Name}.{args.File_Format}'
        if(not args.test):
            c.SaveAs(args.Save_Name_BC_Factor)
            print(f"\n{color.BGREEN}Saved BC factor plot:{color.END} {color.BPINK}{args.Save_Name_BC_Factor}{color.END}\n")
        else:
            print(f"\n{color.BBLUE}WOULD HAVE saved BC factor plot:{color.END} {color.BPINK}{args.Save_Name_BC_Factor}{color.END}\n")
        return args

    return {"h_bc": h_bc,
            "legend": leg,
            "pad": pad}

def _get_pad_for_bc_z_pT_bin(main_pad, z_pT_Bin, number_of_rows, number_of_cols):
    pad_bin = main_pad.cd(z_pT_Bin)
    pad_bin.SetFillColor(ROOT.kGray)
    pad_bin.Divide(1, 1, 0, 0)
    inner_pad = pad_bin.cd(1)
    inner_pad.SetFillColor(0)
    return inner_pad

def Plot_BC_Q2_y_Images_Together_From_JSON(args):
    json_path = str(args.json_file_out)
    if(not os.path.exists(json_path)):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not exist.\n{color.END}File Input Was: {json_path}\n")
    json_data = load_json_file(json_path)
    if((not isinstance(json_data, dict)) or ("results" not in json_data) or (not isinstance(json_data["results"], dict))):
        Crash_Report(args, crash_message=f"\n{color.Error}ERROR:{color.END_R} JSON file does not have the expected schema with a top-level 'results' dict.\n{color.END}File Input Was: {json_path}\n")
    Q2_y_Bin_Range = range(1, 18) if(args.Q2_y_Bin == -1) else [args.Q2_y_Bin]
    Saved_Files = []
    Total_Num_Images = 0
    for Q2_Y_Bin in Q2_y_Bin_Range:
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
        if(args.make_plot_images):
            Save_Name = f'{f"{args.image_name}_" if(args.image_name not in [""]) else ""}BC_Subbin_Comparisons_Together_for_Q2_y_Bin_{Q2_Y_Bin}'
            canvas = ROOT.TCanvas(Save_Name, Save_Name, 3600, 3000)
            canvas.Divide(2, 1, 0.01, 0.01)
            canvas.SetFillColor(ROOT.kGray)
            canvas.plot_store = []

            left_pad = canvas.cd(1)
            left_pad.SetFillColor(ROOT.kGray)
            left_pad.SetPad(0.005, 0.015, 0.27, 0.985)
            left_pad.Divide(1, 2, 0, 0)

            title_pad = left_pad.cd(1)
            title_pad.SetPad(0, 0.45, 1, 1)
            title_pad.SetFillColor(ROOT.kGray)
            title_pad.cd()
            title_box = ROOT.TPaveText(0.05, 0.05, 0.95, 0.95, "NDC")
            title_box.SetBorderSize(0)
            title_box.SetFillStyle(0)
            title_box.SetTextAlign(22)
            title_box.SetTextFont(42)
            title_box.SetTextSize(0.08)
            title_box.AddText("BC Factor Sub-bin Inputs")
            title_box.AddText(f"Q^{{2}}-y Bin = {Q2_Y_Bin}")
            title_box.Draw()
            canvas.title_store = title_box

            legend_pad = left_pad.cd(2)
            legend_pad.SetPad(0, 0, 1, 0.44)
            legend_pad.SetFillColor(ROOT.kGray)

            right_pad = canvas.cd(2)
            right_pad.SetPad(0.28, 0.015, 0.995, 0.9975)
            right_pad.SetFillColor(ROOT.kGray)
            right_pad.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)

            first_plot_objects = None
            for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
                if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                    continue
                if((args.z_pT_Bin not in [-1, z_pT_Bin])):
                    continue
                pad_bin = _get_pad_for_bc_z_pT_bin(right_pad, z_pT_Bin, number_of_rows, number_of_cols)
                plot_objects = Plot_BC_Subbin_Inputs_From_JSON(args, main_pad=pad_bin, save_plot=False, q2_y_bin_override=Q2_Y_Bin, z_pT_bin_override=z_pT_Bin, json_data=json_data, draw_legend=False)
                canvas.plot_store.extend([plot_objects["h_center"], plot_objects["h_ave"], plot_objects["stat_box"]])
                if(first_plot_objects in [None]):
                    first_plot_objects = plot_objects

            legend_pad.cd()
            if(first_plot_objects not in [None]):
                legend = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
                legend.SetNColumns(1)
                legend.SetBorderSize(0)
                legend.SetFillStyle(0)
                legend.SetTextFont(42)
                legend.SetTextSize(0.08)
                legend.AddEntry(first_plot_objects["h_center"], "#scale[0.75]{Center Sub-Bin Content}",  "lep")
                legend.AddEntry(first_plot_objects["h_ave"],    "#scale[0.75]{Average Sub-Bin Content}", "lep")
                legend.Draw()
                canvas.legend_store = legend

            canvas.cd()
            canvas.Modified()
            canvas.Update()

            output_name = f'{Save_Name}.{args.File_Format}'
            if(not args.test):
                canvas.SaveAs(output_name)
                print(f"\n{color.BGREEN}Saved combined BC sub-bin comparison plot:{color.END} {color.BPINK}{output_name}{color.END}\n")
            else:
                print(f"\n{color.BBLUE}WOULD HAVE saved combined BC sub-bin comparison plot:{color.END} {color.BPINK}{output_name}{color.END}\n")
            Saved_Files.append(output_name)
            Total_Num_Images += 1

        if(args.make_plot_BC_factor):
            Save_Name_BC = f'{f"{args.image_name}_" if(args.image_name not in [""]) else ""}BC_Factor_Together_for_Q2_y_Bin_{Q2_Y_Bin}'
            canvas_bc = ROOT.TCanvas(Save_Name_BC, Save_Name_BC, 3600, 3000)
            canvas_bc.Divide(2, 1, 0.01, 0.01)
            canvas_bc.SetFillColor(ROOT.kGray)
            canvas_bc.plot_store = []

            left_pad_bc = canvas_bc.cd(1)
            left_pad_bc.SetFillColor(ROOT.kGray)
            left_pad_bc.SetPad(0.005, 0.015, 0.27, 0.985)
            left_pad_bc.Divide(1, 2, 0, 0)

            title_pad_bc = left_pad_bc.cd(1)
            title_pad_bc.SetPad(0, 0.45, 1, 1)
            title_pad_bc.SetFillColor(ROOT.kGray)
            title_pad_bc.cd()
            title_box_bc = ROOT.TPaveText(0.05, 0.05, 0.95, 0.95, "NDC")
            title_box_bc.SetBorderSize(0)
            title_box_bc.SetFillStyle(0)
            title_box_bc.SetTextAlign(22)
            title_box_bc.SetTextFont(42)
            title_box_bc.SetTextSize(0.08)
            title_box_bc.AddText("BC Factor")
            title_box_bc.AddText(f"Q^{{2}}-y Bin = {Q2_Y_Bin}")
            title_box_bc.Draw()
            canvas_bc.title_store = title_box_bc

            legend_pad_bc = left_pad_bc.cd(2)
            legend_pad_bc.SetPad(0, 0, 1, 0.44)
            legend_pad_bc.SetFillColor(ROOT.kGray)

            right_pad_bc = canvas_bc.cd(2)
            right_pad_bc.SetPad(0.28, 0.015, 0.995, 0.9975)
            right_pad_bc.SetFillColor(ROOT.kGray)
            right_pad_bc.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)

            first_bc_objects = None
            for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
                if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                    continue
                if((args.z_pT_Bin not in [-1, z_pT_Bin])):
                    continue
                pad_bin_bc = _get_pad_for_bc_z_pT_bin(right_pad_bc, z_pT_Bin, number_of_rows, number_of_cols)
                plot_objects_bc = Plot_BC_Factor_From_JSON(args, main_pad=pad_bin_bc, save_plot=False, q2_y_bin_override=Q2_Y_Bin, z_pT_bin_override=z_pT_Bin, json_data=json_data, draw_legend=False)
                canvas_bc.plot_store.append(plot_objects_bc["h_bc"])
                if(first_bc_objects in [None]):
                    first_bc_objects = plot_objects_bc

            legend_pad_bc.cd()
            if(first_bc_objects not in [None]):
                legend_bc = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
                legend_bc.SetNColumns(1)
                legend_bc.SetBorderSize(0)
                legend_bc.SetFillStyle(0)
                legend_bc.SetTextFont(42)
                legend_bc.SetTextSize(0.08)
                legend_bc.AddEntry(first_bc_objects["h_bc"], "#scale[0.85]{BC Factor}", "lep")
                legend_bc.Draw()
                canvas_bc.legend_store = legend_bc

            canvas_bc.cd()
            canvas_bc.Modified()
            canvas_bc.Update()

            output_name_bc = f'{Save_Name_BC}.{args.File_Format}'
            if(not args.test):
                canvas_bc.SaveAs(output_name_bc)
                print(f"\n{color.BGREEN}Saved combined BC factor plot:{color.END} {color.BPINK}{output_name_bc}{color.END}\n")
            else:
                print(f"\n{color.BBLUE}WOULD HAVE saved combined BC factor plot:{color.END} {color.BPINK}{output_name_bc}{color.END}\n")
            Saved_Files.append(output_name_bc)
            Total_Num_Images += 1

    args.Num_Made_Plots = Total_Num_Images
    args.Save_Name = "\n".join(Saved_Files)
    return args

if(__name__ == "__main__"):
    args = parse_args()
    if((args.num_sub_bins <= 0) or (args.num_sub_bins%2 == 0)):
        print(f"\n{color.Error}ERROR: Number of sub-bins must a positive, odd number for this script to work properly{color.END}\n")
        sys.exit(0)
    if((args.num_phi_sub_bins < 0) or ((args.num_sub_bins+args.num_phi_sub_bins)%2 == 0)):
        print(f"\n{color.Error}ERROR: Number of extra phi_h sub-bins cannot be negative and the total must still be a positive, odd number for this script to work properly{color.END}\n")
        sys.exit(0)

    print(f"\n{color.BBLUE}Ready to Run BC Correction Script...{color.END}\n")

    args.timer = RuntimeTimer()
    args.timer.start()
    silence_root_import()
    ROOT.TH1.AddDirectory(0)
    ROOT.gStyle.SetTitleOffset(1.3,'y')
    ROOT.gStyle.SetGridColor(17)
    ROOT.gStyle.SetPadGridX(1)
    ROOT.gStyle.SetPadGridY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(1)
    if(args.test):
        print(f"\t{color.Error}Running as a test of the script...{color.END}\n")
    List_of_BCBins, Total_Num_SBin = {}, 0
    if(args.get_BC_factors):
        List_of_BCBins, Total_Num_SBin = Compute_BC_Factors_From_SubBin_Histograms(args, include_zero_bins=(not args.non_zero_bin_averages), write_full_diagnostics=False)
    elif(not (args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images)):
        if(args.use_file_name and ("*" not in str(args.file))):
            name_insert = str(args.file).split("/")[-1]
            name_insert = str(name_insert.split("new6.")[-1]).replace(".hipo.root", "")
            name_insert = str(name_insert).replace(".root", "")
            args.json_file_out = str(args.json_file_out).replace(".json", f"_{name_insert}.json")
            args.root_file_out = str(args.root_file_out).replace(".root", f"_{name_insert}.root")
            # if(args.verbose):
            print(f"\n{color.BOLD}Updating Output File Names to insert: {color.RED}{name_insert}{color.END}")
        elif(args.use_file_name and args.verbose):
            print(f"\n{color.Error}Will Not Update Output File Names if multiple files are inputed at the same time.{color.END}")
        gdf = Load_RDataFrame(args)
        if(args.check_dataframe):
            print(f"\n{color.BOLD}Print all (currently) defined content of the RDataFrame:{color.END}")
            for num, ii in enumerate(gdf.GetColumnNames()):
                print(f"{num:>3.0f}) {str(ii).ljust(38)} (type -> {gdf.GetColumnType(ii)})")
            print(f"\tTotal length= {len(gdf.GetColumnNames())}\n\n")
            # mn  = gdf.Min("Full_SUB_BIN_idx").GetValue()
            # mx  = gdf.Max("Full_SUB_BIN_idx").GetValue()
            # print(f"Full_SUB_BIN_idx \n min: {mn}\nmax: {mx}")
            # mn  = gdf.Min("Q2_y_SUB_BINs").GetValue()
            # mx  = gdf.Max("Q2_y_SUB_BINs").GetValue()
            # print(f"Q2_y_SUB_BINs \n min: {mn}\nmax: {mx}")
            # mn  = gdf.Min("z_pT_SUB_BINs").GetValue()
            # mx  = gdf.Max("z_pT_SUB_BINs").GetValue()
            # print(f"z_pT_SUB_BINs \n min: {mn}\nmax: {mx}")
            # mn  = gdf.Min("phi_t_SUB_BINs").GetValue()
            # mx  = gdf.Max("phi_t_SUB_BINs").GetValue()
            # print(f"phi_t_SUB_BINs \n min: {mn}\nmax: {mx}")
        if(args.histogram):
            List_of_BCBins = Create_Histograms_for_BC(args)
            Total_Num_SBin = Evaluate_And_Write_Histograms(List_of_BCBins, args)
        else:
            List_of_BCBins, Total_Num_SBin = Get_Bin_Contents_for_BC(args)
    if(args.make_plot_Q2_y_images):
        args = Plot_BC_Q2_y_Images_Together_From_JSON(args)
        Total_Num_SBin += getattr(args, "Num_Made_Plots", 0)
    else:
        if(args.make_plot_images):
            args = Plot_BC_Subbin_Inputs_From_JSON(args)
            Total_Num_SBin += 1
        if(args.make_plot_BC_factor):
            args = Plot_BC_Factor_From_JSON(args)
            Total_Num_SBin += 1
            if(hasattr(args, "Save_Name_BC_Factor")):
                if(hasattr(args, "Save_Name")):
                    args.Save_Name = f"{args.Save_Name}\n{args.Save_Name_BC_Factor}"
                else:
                    args.Save_Name = str(args.Save_Name_BC_Factor)

    Construct_Email(args, final_count=Total_Num_SBin, Count_Type=f"{'Histograms' if(args.histogram) else 'Sub-bins'}{'/Image(s)' if(args.make_plot_images or args.make_plot_BC_factor or args.make_plot_Q2_y_images) else ''}")

