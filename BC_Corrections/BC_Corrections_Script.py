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
                        default=3,
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
    
    # parser.add_argument('-sf', '-ff', '--save_format',
    #                     default=".png",
    #                     type=str,
    #                     choices=[".png", ".pdf"],
    #                     help="Selects the image file format of the images that would be saved by this script when running.")
    
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
        print(f"{color.ERROR}WARNING{color.END}{color.Error}:{color.END_B} ROOT file is missing the kinematic variables.{color.END}\n")
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
    gdf = gdf.Define("z_pT_SUB_BINs", f"""{New_z_pT_and_MultiDim_Binning_Code}
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
    
    Default_Weights = "1.0" if(args.use_clasdis) else "weight"
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
    phih_Bin_Range = range(1, 16) if(args.phih_Bin == -1) else [args.phih_Bin]
    Total_Num_SBin = 0
    for                     Q2_y_Bin in Q2_y_Bin_Range:
        gdf_Q2_y_Bin         = gdf.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")
        for                 z_pT_Bin in z_pT_Bin_Range:
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                if(z_pT_Bin < 35):
                    print(f"{color.Error}Skip Bin {Q2_y_Bin}-{z_pT_Bin}{color.END}")
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
    return List_of_BCBins





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
    
    gdf = Load_RDataFrame(args)
    
    if(args.check_dataframe):
        print(f"\n{color.BOLD}Print all (currently) defined content of the RDataFrame:{color.END}")
        for num, ii in enumerate(gdf.GetColumnNames()):
            print(f"{num:>3.0f}) {str(ii).ljust(38)} (type -> {gdf.GetColumnType(ii)})")
        print(f"\tTotal length= {len(gdf.GetColumnNames())}\n\n")
    

    List_of_BCBins = {}
    List_of_BCBins = Get_Bin_Contents_for_BC(args)

    timer.stop(return_Q=not True)
    
