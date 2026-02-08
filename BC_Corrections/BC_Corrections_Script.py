#!/usr/bin/env python3
import sys
import argparse

import ROOT, numpy, re
import traceback
import os

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
sys.path.remove(script_dir)
del script_dir

def parse_args():
    parser = argparse.ArgumentParser(description="Creates BC Corrections from MC GEN Bins.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-t', '--test',
                        action='store_true', 
                        help='Run as test.')
    
    parser.add_argument('-clasdis', '--use_clasdis',
                        action='store_true', 
                        help='Run with clasdis instead of EvGen (assumes that the EvGen weight should be used by default unless this argument is used).')
    
    parser.add_argument('-nb', '--num_sub_bins',
                        default=5,
                        type=int,
                        help="Number of sub-bins used per Q2-y-z-pT bin. Must be a positive, odd number.")
    
    parser.add_argument('-q2y', '-Q2y', '--Q2_y_Bin',
                        default=-1,
                        type=int,
                        choices=[x for x in range(-1, 18) if(x != 0)],
                        help="Selected Q2-y Bin to run. Use '-1' to run all bins.")
    
    parser.add_argument('-zpt', '-zpT', '--z_pT_Bin',
                        default=-1,
                        type=int,
                        help="Selected z-pT Bin (for any given Q2-y Bin) to run. Use '-1' to run all bins. Does not automatically reject incompatible combinations of the '--Q2_y_Bin' and '--z_pT_Bin' options.")
    
    parser.add_argument('-phit', '-phih', '-phi_t', '-phi_h', '--phih_Bin',
                        default=-1,
                        type=int,
                        choices=[x for x in range(-1, 16) if(x != 0)],
                        help="Selected phi_t Bin to run (each bin is given in increments of 15 degrees). Use '-1' to run all bins.")
    
    parser.add_argument('-f', '--file',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb-EvGen-LUND_EvGen_richcap_GEMC-9729_4.hipo.root",
                        type=str, 
                        help="Path to MC GEN ROOT file used to create the BC corrections. Use EvGen files so that a difference in the modulations is actually observable in the 4D sub-bins.")
    
    parser.add_argument('-cdf', '--check_dataframe',
                        action='store_true', 
                        help='Prints full contents of the RDataFrame to see available branches.')
    
    parser.add_argument('-v', '--verbose',
                        action='store_true', 
                        help='Print more information while running.')

    parser.add_argument('-jsw', '--json_weights',
                        action='store_true',
                        help='Use the json weights (for physics injections) given by the `--json_file` argument.')
    
    parser.add_argument('-jsf_in', '--json_file_in',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json",
                        type=str,
                        help='JSON file path for using `json_weights`.')

    parser.add_argument('-jf', '--json_file_out',
                        default="Sub_Bin_Contents_for_BC_Correction.json",
                        type=str,
                        help='Output JSON file where the bin contents will be saved.')

    parser.add_argument('-hi', '-histo', '--histogram',
                        action='store_true',
                        help='Use ROOT histograms to get the weighted bin contents per sub-bin (instead of the per-bin sum of weight counts).')

    parser.add_argument('-rf', '--root_file_out',
                        default="ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root",
                        type=str,
                        help="Output ROOT file where the sub-bin histograms will be saved if the '--histogram' option is selected.")

    parser.add_argument('-ufn', '--use_file_name',
                        action='store_true',
                        help="If the '--file' argument does not include a '*' in its path, this argument will assume that a single file is being used and that it should be added to the output JSON or ROOT file's names (the default option of just using the '--json_file_out' and '--root_file_out' will be applied if multiple files are given)")
    
    parser.add_argument('-ht', '--histo_title',
                        default="",
                        type=str,
                        help="Optional histogram title addition (use with the '--histogram' option).")

    parser.add_argument('-e', '--email',
                        action='store_true', 
                        help='Send Email message when the script finishes running.')
    
    parser.add_argument('-em', '--email_message',
                        default="",
                        type=str,
                        help="Optional Email message that can be added to the default notification from '--email'.")

    parser.add_argument('-rR', '-read_root', '-bc', '--get_BC_factors',
                        action='store_true', 
                        help="Reads the ROOT files from '--root_file_out' to get the BC factors for each bin (will write the results to the '--json_file_out' JSON file if not running in '--test' mode).")
    
    
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


def Construct_Email(args, timer):
    start_time = timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    end_time, total_time, rate_line = timer.stop(return_Q=True)
    email_body = f"""
The 'BC_Corrections_Script.py' script has finished running.
{start_time}

{args.email_message}

Ran with the following arguments:
--test                          --> {args.test}
--use_clasdis                   --> {args.use_clasdis}
--num_sub_bins                  --> {args.num_sub_bins}{f'''
--root_file_out       (Input)   --> {args.root_file_out}''' if(args.get_BC_factors) else f'''
--file                (Input)   --> {args.file}
--check_dataframe               --> {args.check_dataframe}'''}
--verbose                       --> {args.verbose}
--json_weights                  --> {args.json_weights}
--json_file_in      {'          ' if(args.json_weights) else '(Not Used)'}  --> {args.json_file_in}
--histogram                     --> {args.histogram}
--get_BC_factors                --> {args.get_BC_factors}
--use_file_name                 --> {args.use_file_name}
--Q2_y_Bin                      --> {args.Q2_y_Bin}
--z_pT_Bin                      --> {args.z_pT_Bin}{f'''
--phih_Bin                      --> {args.phih_Bin}
--json_file_out      (Output)   --> {args.json_file_out}''' if((not args.histogram) or args.get_BC_factors) else f'''
--root_file_out      (Output)   --> {args.root_file_out}
--histo_title                   --> "{args.histo_title}"'''}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'BC_Corrections_Script.py' Code", body=email_body, recipient="richard.capobianco@uconn.edu")
    print(email_body)
    
    print(f"""{color.BGREEN}{color_bg.YELLOW}
    \t                                   \t   
    \tThis code has now finished running.\t   
    \t                                   \t   {color.END}
    
    """)


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
    #
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
            # Stale lock handling (best-effort cleanup)
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
    return True



# =========================
# Binning Dictionary
# =========================
from Binning_Dictionaries import Full_Bin_Definition_Array, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D

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
        gdf = gdf.Define("Q2_Y_Bin", Q2_y_Bin_Def)
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
        gdf = gdf.Define("z_pT_Bin_Y_bin",                str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="2D")))
        # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="3D")))
        # gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",      str(z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin", Var_return="5D")))
    
    print(f"\n{color.BGREEN}Creating New Sub-bins... {color.END_B}({color.ERROR}{args.num_sub_bins}{color.END_B} per variable){color.END}\n")
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
    delta_phi_Sbin = float(15.0/float(args.num_sub_bins))
    gdf = gdf.Define("phi_t_SUB_BINs", f" int((phi_t - 15*(phi_t_bin - 1))/{delta_phi_Sbin}) + 1 ")

    gdf = gdf.Define("Full_SUB_BIN_idx", f"""
    if( (Q2_y_SUB_BINs < 0) || (z_pT_SUB_BINs < 0) || (phi_t_SUB_BINs < 0) ){{ return -1; }}
    int q2y_idx = (Q2_y_SUB_BINs - 1)*{args.num_sub_bins}*{args.num_sub_bins};
    int zpT_idx = (q2y_idx + (z_pT_SUB_BINs - 1))*{args.num_sub_bins};
    return zpT_idx + phi_t_SUB_BINs;
    """)
    
    Default_Weights = "1.0" if(args.use_clasdis) else "weight"
    if(args.use_clasdis):
        print(f"\n{color.BBLUE}Using clasdis File(s){color.END}\n")
    if("Event_Weight" in gdf.GetColumnNames()):
        print(f"\n{color.Error}WARNING: 'Event_Weight' is already defined in the RDataFrame...{color.END}\n")
    elif(args.json_weights):
        # With the Modulation weights option, apply the modulations to both gdf and mdf before adding the acceptance weights to mdf
        print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file: {color.BPINK}{str(args.json_file_in).split('/')[-1]}{color.END}\n")
        Fit_Pars = load_json_file(args.json_file_in)
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
            // std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
            // safely retrieve parameters (default = 0)
            // double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 0.0;
            double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
            double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
            // calculate weight
            double phi_rad = phi_h * TMath::DegToRad();
            double weight  = (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
            return weight;
        }}""")
        gdf = gdf.Define("Event_Weight", f"{Default_Weights}*ComputeWeight(Q2_Y_Bin, z_pT_Bin_Y_bin, phi_t)")
    else:
        gdf = gdf.Define("Event_Weight", Default_Weights)
    gdf = gdf.Filter("MM > 1.5") # Apply Missing Mass Cut to exclude the 'exclusive' phase space from my bins
    gdf = gdf.Filter("(Q2_y_SUB_BINs  != -1) && (z_pT_SUB_BINs  != -1) && (phi_t_SUB_BINs != -1)") # Remove all events outside my nominal binning scheme
    return gdf

    

def Evaluate_Weights(List_of_BCBins_In, SumOfWeights_L_In, Full_Run__List_In, args, timer):
    if(not args.test):
        print(f"{color.BCYAN}Triggering Event Evaluation on {color.END_B}{len(Full_Run__List_In)}{color.BCYAN} Sub-Bins...{color.END}\n")
        # One trigger for everything
        ROOT.RDF.RunGraphs(Full_Run__List_In)
        for (nom_name, sub_name), ptr in SumOfWeights_L_In.items():
            List_of_BCBins_In[nom_name][sub_name] = float(ptr.GetValue())
        print(f"{color.BGREEN}Evaluations are Complete{color.END}")
        print(f"{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
        # for     ii in List_of_BCBins_In:
        #     for jj in List_of_BCBins_In[ii]:
        #         print(f"List_of_BCBins_In['{ii}']['{jj}'] = {List_of_BCBins_In[ii][jj]}")
        print(f"{color.BBLUE}Saving To JSON File: {color.BPINK}{args.json_file_out}{color.END}")
        save_dict_to_json(data_to_save=List_of_BCBins_In, json_file=args.json_file_out)
        timer.time_elapsed()
    elif(args.verbose):
        print(f"\n{color.RED}Running as a test (no event evaluations)...{color.END}\n")
        timer.time_elapsed()
    else:
        print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}\n")
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
                        for phi_Sbin in range(1, int(args.num_sub_bins+1)):
                            gdf_phi_SBin = gdf_zpT_SBin.Filter(f"phi_t_SUB_BINs == {phi_Sbin}")
                            sub_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-{zpT_Sbin})-({phih_bin}-{phi_Sbin})"
                            sumw = gdf_phi_SBin.Sum("Event_Weight") # Book the action; do NOT GetValue() yet
                            SumOfWeights_L[(Nominal_bin_name, sub_bin_name)] = sumw
                            Full_Run__List.append(sumw)
                            if(args.verbose):
                                print(f"\t\t{color.BOLD}Collected Sub-{sub_bin_name}{color.END}")
                                print(f"\t\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
                print(f"\t{color.BBLUE}Collected all sub-bins in {Nominal_bin_name}{color.END}")
                Total_Num_SBin += len(Full_Run__List)
                List_of_BCBins, SumOfWeights_L, Full_Run__List = Evaluate_Weights(List_of_BCBins, SumOfWeights_L, Full_Run__List, args, timer)
    print(f"\n{color.BGREEN}Done Collecting all the bin event counts {color.END_B}(Total Number of Sub-bins Collected = {Total_Num_SBin}){color.END}")
    return List_of_BCBins, Total_Num_SBin



def Make_SubBin_TH2_SumW(gdf, args, Q2_y_Bin, z_pT_Bin):
    # Build ONE TH2D for a single (Q2_y_Bin, z_pT_Bin)
    #   X axis: Full_SUB_BIN_idx
    #   Y axis: phi_t_bin (1..24)
    #   Weight: Event_Weight
    Nsub = int(args.num_sub_bins**5)
    hist_name   = f"Histogram Bin ({Q2_y_Bin}-{z_pT_Bin})-(Num SubBins={args.num_sub_bins})"
    hist_titl   = f"#splitline{{{root_color.Bold}{{Generated #phi_{{h}} vs Sub-Bin Indexes from {'EvGen' if(not args.use_clasdis) else 'clasdis'}}}}}{{Made with {args.num_sub_bins} Sub-Bins per Kinematic Variable}}"
    hist_titl   = f"#splitline{{{hist_titl}}}{{Made for Q^{{2}}-y-z-P_{{T}} Bin: ({Q2_y_Bin}-{z_pT_Bin})}}"
    hist_titl   = f"#splitline{{{hist_titl}}}{{Number of Sub-Bins Per Variable = {args.num_sub_bins}}}"
    if(args.json_weights):
      hist_titl = f"#splitline{{{hist_titl}}}{{Used Injected Modulation Weights}}"
    if(args.histo_title not in ["", None]):
      hist_titl = f"#splitline{{{hist_titl}}}{{{args.histo_title}}}"
    hist_titl   = f"{hist_titl}; Sub-Bin Indexes; #phi_{{h}} Bins"
    hmodel      = (hist_name, hist_titl, int(Nsub+2), -0.5, Nsub+1.5, 24, 0.5, 24.5)
    hist_ptr    = gdf.Histo2D(hmodel, "Full_SUB_BIN_idx", "phi_t_bin", "Event_Weight")
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
            List_of_Histos[Nominal_bin_name] = Make_SubBin_TH2_SumW(gdf_z_pT_Bin, args, Q2_y_Bin, z_pT_Bin)
    print(f"\n{color.BBLUE}Done Creating All Sub-bin Histograms {color.END_B}(Total = {len(List_of_Histos)}){color.END}")
    print(f"{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
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
    print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    ROOT.RDF.RunGraphs(ptr_list)
    print(f"{color.BLUE}Time After 'RunGraphs':{color.END}\n\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
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
    #   "Histogram Bin (Q2y-zpt)-(Num SubBins=N)"
    # Returns: (Q2_y_Bin, z_pT_Bin, num_sub_bins) or (None, None, None) if no match.
    match = re.search(r"Histogram Bin \((\d+)-(\d+)\)-\(Num SubBins=(\d+)\)", str(hist_name))
    if(not match):
        return None, None, None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))

def mean_and_weighted_mean(contents, errors):
    if(len(contents) != len(errors)):
        raise ValueError("contents and errors must have the same length")
    len_content = len(contents)
    if(len_content == 0):
        return None
    # --- unweighted mean ---
    sum_c, sum_e2 = 0.0, 0.0
    for c,e in zip(contents, errors):
        sum_c  += c
        sum_e2 += (e*e)
    mean     = (sum_c / len_content)
    mean_err = (ROOT.TMath.Sqrt(sum_e2) / len_content)
    # --- weighted mean (inverse-variance) ---
    num, den = 0.0, 0.0
    for c,e in zip(contents, errors):
        if(e <= 0.0): 
            continue
        w    = (1.0 / (e*e))
        num += (c * w)
        den += w
    if(den > 0.0):
        wmean     = (num / den)
        wmean_err = ROOT.TMath.Sqrt(1.0 / den)
    else:
        wmean     = float("nan")
        wmean_err = float("nan")
    return {"ave": mean, "ave_err": mean_err, "weighted_ave": wmean, "weighted_ave_err": wmean_err}


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
    Nsub = int(num_sub_bins**5)
    full_center_idx = int((Nsub)/2)+1
    
    # Output: one value per nominal bin
    out = {"meta": { "root_file": str(root_path), "num_sub_bins": int(num_sub_bins), "Nsub_per_nominal_bin": int(Nsub), "center_subbin": int(full_center_idx),
                     "definition": {"bc_factor": "avg_subbin_content / center_subbin_content", "avg": "mean over all sub-bins in the nominal bin (optionally includes zeros)"}
                   },
           "results":       {},
           "full_contents": {}
          }

    print(f"\n{color.BBLUE}Opening ROOT file: {color.BPINK}{root_path}{color.END}")
    if(verbose):
        print(f"\tnum_sub_bins={num_sub_bins}  => Nsub={Nsub}")
        print(f"\tcenter Full_SUB_BIN_idx={full_center_idx}")
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
        Q2_y_Bin, z_pT_Bin, nsub_in_name = parse_histogram_name(hist_name)
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
            out["results"][nom_key].update(mean_and_weighted_mean(nonBinContentsList, nonBin_Errors_List))
            BC_norm, BC_norm_err = BC_ratio_and_error(out["results"][nom_key]["ave"],          out["results"][nom_key]["ave_err"],          out["results"][nom_key]["Center Sub-Bin"]["Content"], out["results"][nom_key]["Center Sub-Bin"]["Error"])
            BC_Wave, BC_Wave_err = BC_ratio_and_error(out["results"][nom_key]["weighted_ave"], out["results"][nom_key]["weighted_ave_err"], out["results"][nom_key]["Center Sub-Bin"]["Content"], out["results"][nom_key]["Center Sub-Bin"]["Error"])
            out["results"][nom_key].update({"BC_Factor": BC_norm, "BC_Factor_Err": BC_norm_err, "BC_Factor_Wave": BC_Wave, "BC_Factor_Wave_Err": BC_Wave_err})
            Count_of_Nominal_Bins += 1
        if(verbose):
            print(f"{color.BBLUE}Processed histogram for (Q2-y={Q2_y_Bin}, z-pT={z_pT_Bin}){color.END_B} -> 24 nominal phi bins{color.END}")
        print(f"{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")

    fin.Close()
    print(f"\n{color.BGREEN}Done Accessing the ROOT File{color.END_B} (Total Num of Nominal Bins Processed = {Count_of_Nominal_Bins}){color.END}")
    if(not args.test):
        print(f"{color.BBLUE}Saving To JSON File: {color.BPINK}{args.json_file_out}{color.END}")
        save_dict_to_json(data_to_save=out, json_file=args.json_file_out)
        timer.time_elapsed()
    elif(args.verbose):
        print(f"\n{color.RED}Running as a test (no JSON file save)...{color.END}\n")
        timer.time_elapsed()
    else:
        print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}\n")
    return out, Count_of_Nominal_Bins





if(__name__ == "__main__"):
    
    args = parse_args()
    
    if((args.num_sub_bins <= 0) or (args.num_sub_bins%2 == 0)):
        print(f"\n{color.Error}ERROR: Number of sub-bins must a positive, odd number for this script to work properly{color.END}\n")
        sys.exit(0)
    
    print(f"\n{color.BBLUE}Ready to Run BC Correction Script...{color.END}\n")
        
    timer = RuntimeTimer()
    timer.start()
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
        List_of_BCBins, Total_Num_SBin = Compute_BC_Factors_From_SubBin_Histograms(args, include_zero_bins=True, write_full_diagnostics=False)
    else:
        if(args.use_file_name and ("*" not in str(args.file))):
            name_insert = str(args.file).split("/")[-1]
            name_insert = str(name_insert.split("new6.")[-1]).replace(".hipo.root", "")
            args.json_file_out = str(args.json_file_out).replace(".json", f"_{name_insert}.json")
            args.root_file_out = str(args.root_file_out).replace(".root", f"_{name_insert}.root")
            if(args.verbose):
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
    args.email_message = f"""{args.email_message}
    
The Total Number of {'Histograms Created' if(args.histogram) else 'Sub-bins Collected'} = {Total_Num_SBin}
"""
    Construct_Email(args, timer)
    
