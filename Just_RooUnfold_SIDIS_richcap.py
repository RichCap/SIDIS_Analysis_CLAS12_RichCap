#!/usr/bin/env python3

import sys

# from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT
# import math

from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

timer = RuntimeTimer()
timer.start()

# Turns off the canvases when running in the command line
ROOT.gROOT.SetBatch(1)

import traceback
# import shutil
import os

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)

# Set up global style
ROOT.gStyle.SetStatX(0.80)  # Set the right edge of the stat box (NDC)
ROOT.gStyle.SetStatY(0.45)  # Set the top edge of the stat box (NDC)
ROOT.gStyle.SetStatW(0.3)  # Set the width of the stat box (NDC)
ROOT.gStyle.SetStatH(0.2)  # Set the height of the stat box (NDC)

def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()

import subprocess
# def send_email(subject, body, recipient):
#     # Send an email via the system mail command.
#     subprocess.run(["mail", "-s", subject, recipient], input=body.encode(), check=False)

def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    # Map ANSI codes to HTML spans
    ansi_html_map = { # Styles
                    '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
                      # Colors
                    '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
                      # Reset (closes span)
                    '\033[0m': "",
                    }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    count = 0
    while("  " in str(text)):
        count += 1
        text = text.replace("  ", " ")
        if(count == 150):
            break
    text = text.replace(" --> ", ":\n\t")
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)

import argparse

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def parse_args():
    p = argparse.ArgumentParser(description="Just_RooUnfold_SIDIS_richcap.py analysis script:\n\tMeant for JUST doing the Unfolding Procedure before saving outputs to a ROOT file.",
                                formatter_class=RawDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save', action='store_true', dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root', type=str, default="Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap.root",
                   help="Name of ROOT output file to be saved (must specify the FULL file name).")

    # smearing selection
    grp_smear = p.add_mutually_exclusive_group()
    grp_smear.add_argument('-smear',    '--smear',    action='store_true',
                           help="Unfold with smeared Monte Carlo only.")
    grp_smear.add_argument('-no-smear', '--no-smear', action='store_true',
                           help="Unfold with unsmeared Monte Carlo only.")

    # simulation / modulation / closure
    p.add_argument('-wa', '--weighed_acceptace', action='store_true', dest='weighed_acceptace',
                   help="Use to control the MC weights. If used, all closure tests will assume that the generated MC distributions should be unweighed (i.e., only acceptance weights are applied).\nUse with the '--single_file' option only. WARNING: This option does not make sure the reconstructed MC is weighed only for acceptance (weight injections are controlled by the input file).")
    p.add_argument('-sim', '--simulation', action='store_true', dest='sim',
                   help="Use reconstructed MC instead of experimental data.")
    p.add_argument('-mod', '--modulation', action='store_true', dest='mod',
                   help="Use modulated MC files to create response matrices.")
    p.add_argument('-close', '--closure',  action='store_true', dest='closure',
                   help="Run Closure Test (unfold modulated MC with itself).")
                   # help="Run Closure Test (unfold modulated MC with unweighted matrices).")

    # fitting / output control
    p.add_argument('-fit', '--fit', action='store_true', dest='fit',
                   help="Enable fitting of plots. (Defaults to no fits)")
    p.add_argument('-txt', '--txt',   action='store_true', dest='txt',
                   help="Create a txt output file.")
    p.add_argument('-stat', '--stat', action='store_true', dest='stat',
                   help="Create a (stats) txt output file.")

    # kinematic comparison & proton modes
    p.add_argument('-cc', '--cor-compare', action='store_true', dest='cor_compare',
                   help="Do kinematic correction comparisons (disables fitting & text files).")
    p.add_argument('-tp', '--tag-proton',  action='store_true', dest='tag_proton',
                   help="Use 'Tagged Proton' files.")
    p.add_argument('-cp', '--cut-proton',  action='store_true', dest='cut_proton',
                   help="Use 'Cut with Proton Missing Mass' files.")

    p.add_argument('-cib', '-CIB', '--Common_Int_Bins', action='store_true',
                   help="If given then the code will only run the z-pT bins that have been designated to share the same ranges of z-pT (given by Common_Ranges_for_Integrating_z_pT_Bins).\nOtherwise, the code will run normally and include all z-pT bins for the given Q2-y bin.")

    p.add_argument('-bi', '-bayes-it', '--bayes_iterations', type=int,
                   help="Number of Bayesian Iterations performed while Unfolding (defaults to pre-set values in the code, but this argument allows them to be overwritten automatically).")

    p.add_argument('-nt', '-ntoys', '--Num_Toys', type=int, default=500,
                   help="Number of Toys used to estimate the unfolding errors (used with Unfolding_Histo.SetNToys(...)).")
                   
    p.add_argument('-title', '--title', type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-evgen', '--EvGen', action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut', type=float, default=0.0005,
                   help="Cut made on acceptance (as the minimum acceptance before a bin is removed from unfolding - Old Default: 0.005).")

    p.add_argument('-e', '--email', action='store_true',
                   help="Sends an email to user when done running.")
    
    p.add_argument('-em', '--email_message', type=str, default=None,
                   help="Extra email message to be added when given (use with `--email`).")

    p.add_argument('-sf', '--single_file', action='store_true',
                   help="Runs with a single input file where the histograms are all taken from the same file instead of 3 separate ones.")
    p.add_argument('-sfin', '--single_file_input', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/SIDIS_epip_All_File_Types_from_RDataFrames_ZeroOrder.root",
                   help="Input file to be used with the '--single_file' option. Is set to 'None' if the '--single_file' option is not selected.\n")
    # p.add_argument('-ZO', '--zero_order',  action='store_true', 
    #                help="USE '-wa' INSTEAD — Can use with '--single_file' when using the zeroth order acceptance weights. When you want to use the weighted MC for corrections, the zeroth order generated distributions do not have any weights, so the script will always fail to find them. This argument allows for the unweighted 'gdf' histograms to be used in these cases (do not use this option for other types of weighted MCs).")

    # positional Q2-xB bin arguments
    p.add_argument('bins', nargs='*', metavar='BIN',
                   help="List of Q2-y (or Q2-xB) bin indices to run. '0' means all bins.")

    return p.parse_args()

args = parse_args()

if(not args.single_file):
    args.single_file_input = None

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

# Use it like this:
silence_root_import()
# print("\nImported RooUnfold...\n")

# try:
#     import RooUnfold
# except ImportError:
#     print(f"{color.Error}ERROR: \n{color.END_R}{traceback.format_exc()}{color.END}\n")
#     # print("Somehow the python module was not found, let's try loading the library by hand...")
#     # try:
#     #     ROOT.gSystem.Load("libRooUnfold.so")
#     # except:
#     #     print("".join([color.Error, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))


# ——— determine all your flags exactly as before ———
Saving_Q       = not args.test
Closure_Test   = args.closure
# closure implies sim and no mod
Sim_Test       = ((args.closure) or (args.sim))
Mod_Test       = ((not args.closure) and args.mod)
Fit_Test       = args.fit

# txt/stat file logic (preserve original defaults)
Create_txt_File  = args.txt
Create_stat_File = args.stat

Common_Int_Bins  = args.Common_Int_Bins

# smear logic
Smearing_Options = "no_smear" if(args.no_smear) else "smear" if(args.smear) else "both"

# # combine with closure/sim override
# if((Closure_Test or Sim_Test) and (Smearing_Options != "no_smear")):
#     Smearing_Options = "no_smear"

# correlation comparison overrides everything
Cor_Compare = args.cor_compare
if(Cor_Compare):
    Fit_Test         = False
    Create_txt_File  = False
    Create_stat_File = False
    Smearing_Options = "no_smear"

# proton tagging
Cut_ProQ        = args.cut_proton
Tag_ProQ        = args.tag_proton or Cut_ProQ

    
Standard_Histogram_Title_Addition = ""
if(Closure_Test):
    print(f"\n{color.BLUE}Running Closure Test (Unfolding the Modulated MC using the unweighted response matrices){color.END}\n")
    # Standard_Histogram_Title_Addition = "Closure Test - Unfolding Modulated Simulation"
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Modulated Simulation with itself"
elif(Sim_Test):
    print(f"\n{color.BLUE}Running Simulated Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
if(Mod_Test):
    print(f"\n{color.BLUE}Using {color.BOLD}Modulated {color.END_b} Monte Carlo Files (to create the response matrices){color.END}\n")
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"{Standard_Histogram_Title_Addition} - Using Modulated Response Matrix"
    else:
        Standard_Histogram_Title_Addition = "Closure Test - Using Modulated Response Matrix"

if(args.weighed_acceptace):
    Standard_Histogram_Title_Addition = Standard_Histogram_Title_Addition.replace("Modulated", "Weighted")

if(Tag_ProQ):
    Proton_Type = "Tagged Proton" if(not Cut_ProQ) else "Cut with Proton Missing Mass"
    Standard_Histogram_Title_Addition = "".join([Proton_Type, f" - {Standard_Histogram_Title_Addition}" if(Standard_Histogram_Title_Addition not in [""]) else ""])
    print(f"\n{color.BBLUE}Running with the '{color.UNDERLINE}{Proton_Type}{color.END}{color.BBLUE}' Files{color.END}\n")
    del Proton_Type
        
# if((Closure_Test or Sim_Test) and (str(Smearing_Options) not in ["no_smear"])):
#     print(f"\n{color.BOLD}Unfolding Simulated data for Closure Tests should (probably) not use any additional smearing (forcing choice change)\n{color.END}")
#     Smearing_Options = "no_smear"
        
if(Cor_Compare):
    Fit_Test         = False
    Create_txt_File  = False
    Create_stat_File = False
    Smearing_Options = "no_smear"
    # if(Standard_Histogram_Title_Addition not in [""]):
    #     Standard_Histogram_Title_Addition = "".join([str(Standard_Histogram_Title_Addition), " - Kinematic Correction Comparisons"])
    # else:
    #     Standard_Histogram_Title_Addition = "Kinematic Correction Comparisons"


if(args.title):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{{args.title}}}"
    else:
        Standard_Histogram_Title_Addition = args.title
    print(f"\nAdding the following extra title to the histograms:\n\t{Standard_Histogram_Title_Addition}\n")
    
if(Fit_Test):
    print(f"\n\n{color.BGREEN}{color_bg.YELLOW}\n\n    Will be Fitting Plots    \n{color.END}\n\n")
    
if(Create_txt_File):
    print(f"{color.BBLUE}\nWill create a txt output file{color.END}")
    if(not Create_stat_File):
        print(f"{color.RED}Will {color.BOLD}NOT{color.END_R} create a (stats) txt output file{color.END}")
    print("")
else:
    print(f"\n{color.RED}Will {color.BOLD}NOT{color.END_R} create a txt output file{color.END}\n")
    
    
# if(str(Smearing_Options) not in ["both"]):
print(color.BBLUE, "\nSmear option selected is:", "No Smear" if(str(Smearing_Options) in ["", "no_smear"]) else str(Smearing_Options.replace("_s", "S")).replace("s", "S"), color.END, "\n")

# File_Save_Format = ".png"
# # File_Save_Format = ".root"
# # File_Save_Format = ".pdf"


# if((File_Save_Format != ".png") and Saving_Q):
#     print(f"{color.BGREEN}\nSave Option was not set to output .png files. Save format is:{color.END_B}{color.UNDERLINE}{File_Save_Format}{color.END}\n")



# # 'Binning_Method' is defined in 'MyCommonAnalysisFunction_richcap'
# # Binning_Method = "_y_bin" 

Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
if(any(binning in Binning_Method for binning in ["y_bin", "Y_bin"])):
    Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']


if(args.bins):
    Q2_xB_Bin_List = args.bins
if(Q2_xB_Bin_List == []):
    print(f"{color.Error}ERROR: 'Q2_xB_Bin_List' is empty. (Defaulting to running with Bin 1){color.END}")
    Q2_xB_Bin_List = ['1']
if('0' not in Q2_xB_Bin_List):
    Q2_xB_Bin_List.append('0')
    appended_0 = True
    print(f"\n{color.RED}Running Bin 'All' for Q2-y Bins by default (will skip at end){color.END}\n")
else:
    appended_0 = False
print(f"\nRunning for Q2-xB/Q2-y Bins: {str(Q2_xB_Bin_List).replace('[', '')}".replace(']', ''))
    
# if(len(sys.argv) > 2):
#     Q2_xB_Bin_List = []
#     for ii_bin in range(2, len(sys.argv), 1):
#         Q2_xB_Bin_List.append(sys.argv[ii_bin])
#     if(Q2_xB_Bin_List == []):
#         print("Error")
#         Q2_xB_Bin_List = ['1']
#     if('0' not in Q2_xB_Bin_List):
#         Q2_xB_Bin_List.append('0')
#         appended_0 = True
#         print(f"\n{color.RED}Running Bin 'All' for Q2-y Bins by default (will skip at end){color.END}\n")
#     else:
#         appended_0 = False
#     # print(str(("".join(["\nRunning for Q2-xB/Q2-y Bins: ", str(Q2_xB_Bin_List)]).replace("[", "")).replace("]", "")))
#     print(f"\nRunning for Q2-xB/Q2-y Bins: {str(Q2_xB_Bin_List).replace('[', '')}".replace(']', ''))
    


if(Common_Int_Bins):
    print(f"\n\n{color.BGREEN}Will ONLY be running the z-pT Bins that have been selected as per the 'Commom Integration Region' given by 'Common_Ranges_for_Integrating_z_pT_Bins'{color.END}\n\n")

print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis\n{color.END}")

# Getting Current Date/Time
timer.time_elapsed()

# # Variable for imposing a minimum acceptance value cut to the unfolded distributions
# Min_Allowed_Acceptance_Cut = 0.0175
# Min_Allowed_Acceptance_Cut = 0.005

# Min_Allowed_Acceptance_Cut = 0.0025 # Updated for tests on 9/21/2025 --> Wanted to see if Acceptance cut could be lowered
# Min_Allowed_Acceptance_Cut = 0.0005 # Updated for tests on 9/21/2025 --> Wanted to see if Acceptance cut could be lowered

Min_Allowed_Acceptance_Cut = args.Min_Allowed_Acceptance_Cut # As of 9/21/2025 - Made an agument with the default being 0.005

# Min_Allowed_Acceptance_Cut = 0.0045 # Updated for tests on 5/2/2025

# 'Acceptance_Cut_Line' will be used to show where the minimum acceptance cut is placed when drawing the Acceptance Plots
Acceptance_Cut_Line = ROOT.TLine(0, Min_Allowed_Acceptance_Cut, 360, Min_Allowed_Acceptance_Cut)
Acceptance_Cut_Line.SetLineColor(ROOT.kRed)
Acceptance_Cut_Line.SetLineWidth(1)
Acceptance_Cut_Line.SetLineStyle(1) # Solid line (default)


############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################

def Full_Calc_Fit(Histo, version="norm"):
    
    # Helping the closure tests with known values of B and C
    if(Closure_Test and False): # On 10/30/2025 -> Changed closure test to use default data fitting
        B, C = -0.500, 0.025
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A    = (Histo_max_bin_num)/((1 + B*ROOT.cos(Histo_max_bin_phi) + C*ROOT.cos(2*Histo_max_bin_phi)))
    # elif(Sim_Test):
    #     B, C = 0, 0
    #     Histo_max_bin     = Histo.GetMaximumBin()
    #     Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
    #     Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
    #     A    = (Histo_max_bin_num)/((1 + B*ROOT.cos(Histo_max_bin_phi) + C*ROOT.cos(2*Histo_max_bin_phi)))
    # # As of 10/23/2025, the Sim_Test includes modulations taken from data
    else:
        Histo_180_bin = Histo.FindBin(155)
        Histo_240_bin = Histo.FindBin(300)
        Histo_max_bin = Histo.GetMaximumBin()
        if(Histo_max_bin == Histo_180_bin or Histo_max_bin == Histo_240_bin):
            # print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Same bin used in fits", color.END]))
            Histo_max_bin = Histo.FindBin(100)
        Histo_180_bin_y = Histo.GetBinContent(Histo_180_bin)
        Histo_240_bin_y = Histo.GetBinContent(Histo_240_bin)
        Histo_max_bin_y = Histo.GetBinContent(Histo_max_bin)
        Histo_180_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_180_bin)
        Histo_240_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_240_bin)
        Histo_max_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_180_bin_Cos_phi   = ROOT.cos(Histo_180_bin_x)
        Histo_240_bin_Cos_phi   = ROOT.cos(Histo_240_bin_x)
        Histo_max_bin_Cos_phi   = ROOT.cos(Histo_max_bin_x)
        Histo_180_bin_Cos_2_phi = ROOT.cos(2*Histo_180_bin_x)
        Histo_240_bin_Cos_2_phi = ROOT.cos(2*Histo_240_bin_x)
        Histo_max_bin_Cos_2_phi = ROOT.cos(2*Histo_max_bin_x)
        numerator   = (Histo_180_bin_y*Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_Cos_phi*Histo_240_bin_y*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_y*Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_2_phi*Histo_240_bin_y*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi*Histo_max_bin_y) - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi*Histo_max_bin_y)
        denominator = (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi)                 - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi)                 - (Histo_180_bin_Cos_phi*Histo_max_bin_Cos_2_phi)                 + (Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi)                 + (Histo_180_bin_Cos_2_phi*Histo_max_bin_Cos_phi)                 - (Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi)
        try:
            A = numerator/denominator
            # A = 0.025
            B = -0.2*A
            C = -0.1*A
            # C = ((Histo_240_bin_x - A) + (Histo_180_bin_x - A)*(Histo_240_bin_Cos_phi/Histo_180_bin_Cos_phi))/((Histo_240_bin_Cos_2_phi + (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi)/Histo_180_bin_Cos_phi))
            # B = (Histo_max_bin - A - C*Histo_max_bin_Cos_2_phi)/(Histo_max_bin_Cos_phi)
        except:
            print(f"{color.Error}Full_Calc_Fit(...) ERROR:\n{color.END}{traceback.format_exc()}\n")
            A, B, C = "Error", "Error", "Error"

        try:
    #         Phi_low_bin = Histo.FindBin(52.5)
    #         Phi_mid_bin = Histo.FindBin(157.5)
    #         Phi_max_bin = Histo.FindBin(262.5)

            Phi_low_bin = Histo.FindBin(157.5)
            Phi_mid_bin = Histo.FindBin(202.5)

            Phi_low_bin = Histo.FindBin(155)
            Phi_mid_bin = Histo.FindBin(300)

            # Phi_max_bin = Histo.FindBin(262.5)
            Phi_max_bin = Histo.GetMaximumBin()

            if(Phi_max_bin in [Phi_low_bin, Phi_mid_bin, Phi_low_bin - 1, Phi_mid_bin - 1, Phi_low_bin - 2, Phi_mid_bin - 2, Phi_low_bin + 1, Phi_mid_bin + 1, Phi_low_bin + 2, Phi_mid_bin + 2]):
                print(f"{color.RED}(Minor) Error in 'Full_Calc_Fit': Same bin used in fits{color.END}")
                # Phi_max_bin = Histo.FindBin(187.5)
                Phi_max_bin = Histo.FindBin(262.5)

            Phi_low = (3.1415926/180)*Histo.GetBinCenter(Phi_low_bin)
            Phi_mid = (3.1415926/180)*Histo.GetBinCenter(Phi_mid_bin)
            Phi_max = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)

            n2 = Histo.GetBinContent(Phi_max_bin)
            a2 = ROOT.cos(Phi_max)                # Cos_phi_max
            b2 = ROOT.cos(2*Phi_max)              # Cos_2_phi_max

            if(0 not in [ROOT.cos(Phi_max), ROOT.cos(2*Phi_max)]):
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max
            elif(Phi_max_bin != Histo.FindBin(187.5)):
                print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Phi_max gives divide by 0 error", color.END]))
                Phi_max_bin = Histo.FindBin(187.5)
                Phi_max     = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max

            if(0 in [ROOT.cos(Phi_max), ROOT.cos(2*Phi_max)]):
                print(color.Error, "POTENTIAL RISK OF DIVIDE BY 0 ERROR FOR Phi_max_bin =", Phi_max_bin, color.END)
                Phi_max_bin = Histo.FindBin(100 if(Phi_max_bin != Histo.FindBin(100)) else 247.5)
                Phi_max     = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max

            n0 = Histo.GetBinContent(Phi_low_bin)
            n1 = Histo.GetBinContent(Phi_mid_bin)

            a0 = ROOT.cos(Phi_low)                # Cos_phi_low
            a1 = ROOT.cos(Phi_mid)                # Cos_phi_mid

            b0 = ROOT.cos(2*Phi_low)              # Cos_2_phi_low
            b1 = ROOT.cos(2*Phi_mid)              # Cos_2_phi_mid

            numerator_A   = a0*(b2*n1 - b1*n2) + b0*(a1*n2 - a2*n1) - n0*(a1*b2 - a2*b1)
            denominator_A = a0*(b2    - b1)    + b0*(a1    - a2)    -     a1*b2 + a2*b1

            numerator_B   = b0*(n1    -    n2) + b1*(n2    - n0)    + b2*(n0    - n1)
            denominator_B = a0*(b2*n1 - b1*n2) + b0*(a1*n2 - a2*n0) + n0*(a2*b1 - a1*b2)

            numerator_C   = a0*(n1    -    n2) + a1*(n2    - n0)    + a2*(n0    - n1)
            denominator_C = a0*(b1*n2 - b2*n1) + b0*(a2*n1 - a1*n2) + n0*(a1*b2 - a2*b1)

            if(denominator_A != 0):
                A = numerator_A/denominator_A
            else:
                print(color.RED, "\nError A - Divide by 0\n", color.END)
                A = n2/(1 + (numerator_B/denominator_B)*a2 + (numerator_C/denominator_C)*b2)

            if(denominator_B != 0):
                B = numerator_B/denominator_B
            else:
                print(color.RED, "\nError B - Divide by 0\n", color.END)
                print("a2 =", a2)
                print("A  =", A)
                print("denominator_C =", denominator_C)
                B = (1/a2)*((n2/A) - (numerator_C/denominator_C)*b2 - 1)

            if(denominator_C != 0):
                C = numerator_C/denominator_C
            else:
                print(color.RED, "\nError C - Divide by 0\n", color.END)
                C = (1/b2)*((n2/A) - B*a2 - 1)

        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)

            A, B, C = "Error", "Error", "Error"
        
        
        
    if(version != "norm"):
        
        Phi_1_bin = Histo.FindBin(52.5)
        Phi_2_bin = Histo.FindBin(105)
        Phi_3_bin = Histo.FindBin(157.5)
        Phi_4_bin = Histo.FindBin(210)
        Phi_5_bin = Histo.FindBin(262.5)
        
        Phi_1 = (3.1415926/180)*Histo.GetBinCenter(Phi_1_bin)
        Phi_2 = (3.1415926/180)*Histo.GetBinCenter(Phi_2_bin)
        Phi_3 = (3.1415926/180)*Histo.GetBinCenter(Phi_3_bin)
        Phi_4 = (3.1415926/180)*Histo.GetBinCenter(Phi_4_bin)
        Phi_5 = (3.1415926/180)*Histo.GetBinCenter(Phi_5_bin)
        
        n1 = Histo.GetBinContent(Phi_1_bin)
        n2 = Histo.GetBinContent(Phi_2_bin)
        n3 = Histo.GetBinContent(Phi_3_bin)
        n4 = Histo.GetBinContent(Phi_4_bin)
        n5 = Histo.GetBinContent(Phi_5_bin)
        
        a1 = ROOT.cos(Phi_1)    # Cos(phi)
        b1 = ROOT.cos(2*Phi_1)  # Cos(2*phi)
        c1 = ROOT.cos(3*Phi_1)  # Cos(3*phi)
        d1 = ROOT.cos(4*Phi_1)  # Cos(4*phi)
        
        a2 = ROOT.cos(Phi_2)
        b2 = ROOT.cos(2*Phi_2)
        c2 = ROOT.cos(3*Phi_2)
        d2 = ROOT.cos(4*Phi_2)

        a3 = ROOT.cos(Phi_3)
        b3 = ROOT.cos(2*Phi_3)
        c3 = ROOT.cos(3*Phi_3)
        d3 = ROOT.cos(4*Phi_3)

        a4 = ROOT.cos(Phi_4)
        b4 = ROOT.cos(2*Phi_4)
        c4 = ROOT.cos(3*Phi_4)
        d4 = ROOT.cos(4*Phi_4)

        a5 = ROOT.cos(Phi_5)
        b5 = ROOT.cos(2*Phi_5)
        c5 = ROOT.cos(3*Phi_5)
        d5 = ROOT.cos(4*Phi_5)
        
        A =  (n2*b1*c3*d4    - n2*b1*c3*d5    - n2*b1*d3*c4    + n2*b1*d3*c5    + n2*b1*c4*d5    - n2*b1*d4*c5    - n2*c1*b3*d4    + n2*c1*b3*d5    + n2*c1*d3*b4    - n2*c1*d3*b5    - n2*c1*b4*d5    + n2*c1*d4*b5    + n2*d1*b3*c4    - n2*d1*b3*c5    - n2*d1*c3*b4    + n2*d1*c3*b5    + n2*d1*b4*c5    - n2*d1*c4*b5    - n2*b3*c4*d5    + n2*b3*d4*c5    + n2*c3*b4*d5    - n2*c3*d4*b5    - n2*d3*b4*c5    + n2*d3*c4*b5    + n4*b1*c2*d3    - n4*b1*c2*d5    - n4*b1*d2*c3    + n4*b1*d2*c5    + n4*b1*c3*d5    - n4*b1*d3*c5    - n4*c1*b2*d3    + n4*c1*b2*d5    + n4*c1*d2*b3    - n4*c1*d2*b5    - n4*c1*b3*d5    + n4*c1*d3*b5    + n4*d1*b2*c3    - n4*d1*b2*c5    - n4*d1*c2*b3    + n4*d1*c2*b5    + n4*d1*b3*c5    - n4*d1*c3*b5    - n4*b2*c3*d5    + n4*b2*d3*c5    + n4*c2*b3*d5    - n4*c2*d3*b5    - n4*d2*b3*c5    + n4*d2*c3*b5    - b1*c2*d3*n5    - b1*c2*d4*n3    + b1*c2*d4*n5    + b1*c2*d5*n3    + b1*d2*c3*n5    + b1*d2*c4*n3    - b1*d2*c4*n5    - b1*d2*c5*n3    - b1*c3*d4*n5    + b1*d3*c4*n5    - b1*c4*d5*n3    + b1*d4*c5*n3    + c1*b2*d3*n5    + c1*b2*d4*n3    - c1*b2*d4*n5    - c1*b2*d5*n3    - c1*d2*b3*n5    - c1*d2*b4*n3    + c1*d2*b4*n5    + c1*d2*b5*n3    + c1*b3*d4*n5    - c1*d3*b4*n5    + c1*b4*d5*n3    - c1*d4*b5*n3    - d1*b2*c3*n5    - d1*b2*c4*n3    + d1*b2*c4*n5    + d1*b2*c5*n3    + d1*c2*b3*n5    + d1*c2*b4*n3    - d1*c2*b4*n5    - d1*c2*b5*n3    - d1*b3*c4*n5    + d1*c3*b4*n5    - d1*b4*c5*n3    + d1*c4*b5*n3    - b2*c3*d4*n1 + b2*c3*d4*n5 + b2*c3*d5*n1 + b2*d3*c4*n1 - b2*d3*c4*n5 - b2*d3*c5*n1 - b2*c4*d5*n1 + b2*c4*d5*n3 + b2*d4*c5*n1 - b2*d4*c5*n3 + c2*b3*d4*n1 - c2*b3*d4*n5 - c2*b3*d5*n1 - c2*d3*b4*n1 + c2*d3*b4*n5 + c2*d3*b5*n1 + c2*b4*d5*n1 - c2*b4*d5*n3 - c2*d4*b5*n1 + c2*d4*b5*n3 - d2*b3*c4*n1 + d2*b3*c4*n5 + d2*b3*c5*n1 + d2*c3*b4*n1 - d2*c3*b4*n5 - d2*c3*b5*n1 - d2*b4*c5*n1 + d2*b4*c5*n3 + d2*c4*b5*n1 - d2*c4*b5*n3 + b3*c4*d5*n1 - b3*d4*c5*n1 - c3*b4*d5*n1 + c3*d4*b5*n1 + d3*b4*c5*n1 - d3*c4*b5*n1)/(n2*a1*b3*c4*d5 - n2*a1*b3*d4*c5 - n2*a1*c3*b4*d5 + n2*a1*c3*d4*b5 + n2*a1*d3*b4*c5 - n2*a1*d3*c4*b5 - n2*b1*a3*c4*d5 + n2*b1*a3*d4*c5 + n2*b1*c3*a4*d5 - n2*b1*c3*d4*a5 - n2*b1*d3*a4*c5 + n2*b1*d3*c4*a5 + n2*c1*a3*b4*d5 - n2*c1*a3*d4*b5 - n2*c1*b3*a4*d5 + n2*c1*b3*d4*a5 + n2*c1*d3*a4*b5 - n2*c1*d3*b4*a5 - n2*d1*a3*b4*c5 + n2*d1*a3*c4*b5 + n2*d1*b3*a4*c5 - n2*d1*b3*c4*a5 - n2*d1*c3*a4*b5 + n2*d1*c3*b4*a5 + n4*a1*b2*c3*d5 - n4*a1*b2*d3*c5 - n4*a1*c2*b3*d5 + n4*a1*c2*d3*b5 + n4*a1*d2*b3*c5 - n4*a1*d2*c3*b5 - n4*b1*a2*c3*d5 + n4*b1*a2*d3*c5 + n4*b1*c2*a3*d5 - n4*b1*c2*d3*a5 - n4*b1*d2*a3*c5 + n4*b1*d2*c3*a5 + n4*c1*a2*b3*d5 - n4*c1*a2*d3*b5 - n4*c1*b2*a3*d5 + n4*c1*b2*d3*a5 + n4*c1*d2*a3*b5 - n4*c1*d2*b3*a5 - n4*d1*a2*b3*c5 + n4*d1*a2*c3*b5 + n4*d1*b2*a3*c5 - n4*d1*b2*c3*a5 - n4*d1*c2*a3*b5 + n4*d1*c2*b3*a5 - a1*b2*c3*d4*n5 + a1*b2*d3*c4*n5 - a1*b2*c4*d5*n3 + a1*b2*d4*c5*n3 + a1*c2*b3*d4*n5 - a1*c2*d3*b4*n5 + a1*c2*b4*d5*n3 - a1*c2*d4*b5*n3 - a1*d2*b3*c4*n5 + a1*d2*c3*b4*n5 - a1*d2*b4*c5*n3 + a1*d2*c4*b5*n3 + b1*a2*c3*d4*n5 - b1*a2*d3*c4*n5 + b1*a2*c4*d5*n3 - b1*a2*d4*c5*n3 - b1*c2*a3*d4*n5 + b1*c2*d3*a4*n5 - b1*c2*a4*d5*n3 + b1*c2*d4*a5*n3 + b1*d2*a3*c4*n5 - b1*d2*c3*a4*n5 + b1*d2*a4*c5*n3 - b1*d2*c4*a5*n3 - c1*a2*b3*d4*n5 + c1*a2*d3*b4*n5 - c1*a2*b4*d5*n3 + c1*a2*d4*b5*n3 + c1*b2*a3*d4*n5 - c1*b2*d3*a4*n5 + c1*b2*a4*d5*n3 - c1*b2*d4*a5*n3 - c1*d2*a3*b4*n5 + c1*d2*b3*a4*n5 - c1*d2*a4*b5*n3 + c1*d2*b4*a5*n3 + d1*a2*b3*c4*n5 - d1*a2*c3*b4*n5 + d1*a2*b4*c5*n3 - d1*a2*c4*b5*n3 - d1*b2*a3*c4*n5 + d1*b2*c3*a4*n5 - d1*b2*a4*c5*n3 + d1*b2*c4*a5*n3 + d1*c2*a3*b4*n5 - d1*c2*b3*a4*n5 + d1*c2*a4*b5*n3 - d1*c2*b4*a5*n3 - a2*b3*c4*d5*n1 + a2*b3*d4*c5*n1 + a2*c3*b4*d5*n1 - a2*c3*d4*b5*n1 - a2*d3*b4*c5*n1 + a2*d3*c4*b5*n1 + b2*a3*c4*d5*n1 - b2*a3*d4*c5*n1 - b2*c3*a4*d5*n1 + b2*c3*d4*a5*n1 + b2*d3*a4*c5*n1 - b2*d3*c4*a5*n1 - c2*a3*b4*d5*n1 + c2*a3*d4*b5*n1 + c2*b3*a4*d5*n1 - c2*b3*d4*a5*n1 - c2*d3*a4*b5*n1 + c2*d3*b4*a5*n1 + d2*a3*b4*c5*n1 - d2*a3*c4*b5*n1 - d2*b3*a4*c5*n1 + d2*b3*c4*a5*n1 + d2*c3*a4*b5*n1 - d2*c3*b4*a5*n1)
        B = (-n2*a1*c3*d4    + n2*a1*c3*d5    + n2*a1*d3*c4    - n2*a1*d3*c5    - n2*a1*c4*d5    + n2*a1*d4*c5    + n2*c1*a3*d4    - n2*c1*a3*d5    - n2*c1*d3*a4    + n2*c1*d3*a5    + n2*c1*a4*d5    - n2*c1*d4*a5    - n2*d1*a3*c4    + n2*d1*a3*c5    + n2*d1*c3*a4    - n2*d1*c3*a5    - n2*d1*a4*c5    + n2*d1*c4*a5    + n2*a3*c4*d5    - n2*a3*d4*c5    - n2*c3*a4*d5    + n2*c3*d4*a5    + n2*d3*a4*c5    - n2*d3*c4*a5    - n4*a1*c2*d3    + n4*a1*c2*d5    + n4*a1*d2*c3    - n4*a1*d2*c5    - n4*a1*c3*d5    + n4*a1*d3*c5    + n4*c1*a2*d3    - n4*c1*a2*d5    - n4*c1*d2*a3    + n4*c1*d2*a5    + n4*c1*a3*d5    - n4*c1*d3*a5    - n4*d1*a2*c3    + n4*d1*a2*c5    + n4*d1*c2*a3    - n4*d1*c2*a5    - n4*d1*a3*c5    + n4*d1*c3*a5    + n4*a2*c3*d5    - n4*a2*d3*c5    - n4*c2*a3*d5    + n4*c2*d3*a5    + n4*d2*a3*c5    - n4*d2*c3*a5    + a1*c2*d3*n5    + a1*c2*d4*n3    - a1*c2*d4*n5    - a1*c2*d5*n3    - a1*d2*c3*n5    - a1*d2*c4*n3    + a1*d2*c4*n5    + a1*d2*c5*n3    + a1*c3*d4*n5    - a1*d3*c4*n5    + a1*c4*d5*n3    - a1*d4*c5*n3    - c1*a2*d3*n5    - c1*a2*d4*n3    + c1*a2*d4*n5    + c1*a2*d5*n3    + c1*d2*a3*n5    + c1*d2*a4*n3    - c1*d2*a4*n5    - c1*d2*a5*n3    - c1*a3*d4*n5    + c1*d3*a4*n5    - c1*a4*d5*n3    + c1*d4*a5*n3    + d1*a2*c3*n5    + d1*a2*c4*n3    - d1*a2*c4*n5    - d1*a2*c5*n3    - d1*c2*a3*n5    - d1*c2*a4*n3    + d1*c2*a4*n5    + d1*c2*a5*n3    + d1*a3*c4*n5    - d1*c3*a4*n5    + d1*a4*c5*n3    - d1*c4*a5*n3    + a2*c3*d4*n1 - a2*c3*d4*n5 - a2*c3*d5*n1 - a2*d3*c4*n1 + a2*d3*c4*n5 + a2*d3*c5*n1 + a2*c4*d5*n1 - a2*c4*d5*n3 - a2*d4*c5*n1 + a2*d4*c5*n3 - c2*a3*d4*n1 + c2*a3*d4*n5 + c2*a3*d5*n1 + c2*d3*a4*n1 - c2*d3*a4*n5 - c2*d3*a5*n1 - c2*a4*d5*n1 + c2*a4*d5*n3 + c2*d4*a5*n1 - c2*d4*a5*n3 + d2*a3*c4*n1 - d2*a3*c4*n5 - d2*a3*c5*n1 - d2*c3*a4*n1 + d2*c3*a4*n5 + d2*c3*a5*n1 + d2*a4*c5*n1 - d2*a4*c5*n3 - d2*c4*a5*n1 + d2*c4*a5*n3 - a3*c4*d5*n1 + a3*d4*c5*n1 + c3*a4*d5*n1 - c3*d4*a5*n1 - d3*a4*c5*n1 + d3*c4*a5*n1)/(n2*a1*b3*c4*d5 - n2*a1*b3*d4*c5 - n2*a1*c3*b4*d5 + n2*a1*c3*d4*b5 + n2*a1*d3*b4*c5 - n2*a1*d3*c4*b5 - n2*b1*a3*c4*d5 + n2*b1*a3*d4*c5 + n2*b1*c3*a4*d5 - n2*b1*c3*d4*a5 - n2*b1*d3*a4*c5 + n2*b1*d3*c4*a5 + n2*c1*a3*b4*d5 - n2*c1*a3*d4*b5 - n2*c1*b3*a4*d5 + n2*c1*b3*d4*a5 + n2*c1*d3*a4*b5 - n2*c1*d3*b4*a5 - n2*d1*a3*b4*c5 + n2*d1*a3*c4*b5 + n2*d1*b3*a4*c5 - n2*d1*b3*c4*a5 - n2*d1*c3*a4*b5 + n2*d1*c3*b4*a5 + n4*a1*b2*c3*d5 - n4*a1*b2*d3*c5 - n4*a1*c2*b3*d5 + n4*a1*c2*d3*b5 + n4*a1*d2*b3*c5 - n4*a1*d2*c3*b5 - n4*b1*a2*c3*d5 + n4*b1*a2*d3*c5 + n4*b1*c2*a3*d5 - n4*b1*c2*d3*a5 - n4*b1*d2*a3*c5 + n4*b1*d2*c3*a5 + n4*c1*a2*b3*d5 - n4*c1*a2*d3*b5 - n4*c1*b2*a3*d5 + n4*c1*b2*d3*a5 + n4*c1*d2*a3*b5 - n4*c1*d2*b3*a5 - n4*d1*a2*b3*c5 + n4*d1*a2*c3*b5 + n4*d1*b2*a3*c5 - n4*d1*b2*c3*a5 - n4*d1*c2*a3*b5 + n4*d1*c2*b3*a5 - a1*b2*c3*d4*n5 + a1*b2*d3*c4*n5 - a1*b2*c4*d5*n3 + a1*b2*d4*c5*n3 + a1*c2*b3*d4*n5 - a1*c2*d3*b4*n5 + a1*c2*b4*d5*n3 - a1*c2*d4*b5*n3 - a1*d2*b3*c4*n5 + a1*d2*c3*b4*n5 - a1*d2*b4*c5*n3 + a1*d2*c4*b5*n3 + b1*a2*c3*d4*n5 - b1*a2*d3*c4*n5 + b1*a2*c4*d5*n3 - b1*a2*d4*c5*n3 - b1*c2*a3*d4*n5 + b1*c2*d3*a4*n5 - b1*c2*a4*d5*n3 + b1*c2*d4*a5*n3 + b1*d2*a3*c4*n5 - b1*d2*c3*a4*n5 + b1*d2*a4*c5*n3 - b1*d2*c4*a5*n3 - c1*a2*b3*d4*n5 + c1*a2*d3*b4*n5 - c1*a2*b4*d5*n3 + c1*a2*d4*b5*n3 + c1*b2*a3*d4*n5 - c1*b2*d3*a4*n5 + c1*b2*a4*d5*n3 - c1*b2*d4*a5*n3 - c1*d2*a3*b4*n5 + c1*d2*b3*a4*n5 - c1*d2*a4*b5*n3 + c1*d2*b4*a5*n3 + d1*a2*b3*c4*n5 - d1*a2*c3*b4*n5 + d1*a2*b4*c5*n3 - d1*a2*c4*b5*n3 - d1*b2*a3*c4*n5 + d1*b2*c3*a4*n5 - d1*b2*a4*c5*n3 + d1*b2*c4*a5*n3 + d1*c2*a3*b4*n5 - d1*c2*b3*a4*n5 + d1*c2*a4*b5*n3 - d1*c2*b4*a5*n3 - a2*b3*c4*d5*n1 + a2*b3*d4*c5*n1 + a2*c3*b4*d5*n1 - a2*c3*d4*b5*n1 - a2*d3*b4*c5*n1 + a2*d3*c4*b5*n1 + b2*a3*c4*d5*n1 - b2*a3*d4*c5*n1 - b2*c3*a4*d5*n1 + b2*c3*d4*a5*n1 + b2*d3*a4*c5*n1 - b2*d3*c4*a5*n1 - c2*a3*b4*d5*n1 + c2*a3*d4*b5*n1 + c2*b3*a4*d5*n1 - c2*b3*d4*a5*n1 - c2*d3*a4*b5*n1 + c2*d3*b4*a5*n1 + d2*a3*b4*c5*n1 - d2*a3*c4*b5*n1 - d2*b3*a4*c5*n1 + d2*b3*c4*a5*n1 + d2*c3*a4*b5*n1 - d2*c3*b4*a5*n1)
        C =  (n2*a1*b3*d4    - n2*a1*b3*d5    - n2*a1*d3*b4    + n2*a1*d3*b5    + n2*a1*b4*d5    - n2*a1*d4*b5    - n2*b1*a3*d4    + n2*b1*a3*d5    + n2*b1*d3*a4    - n2*b1*d3*a5    - n2*b1*a4*d5    + n2*b1*d4*a5    + n2*d1*a3*b4    - n2*d1*a3*b5    - n2*d1*b3*a4    + n2*d1*b3*a5    + n2*d1*a4*b5    - n2*d1*b4*a5    - n2*a3*b4*d5    + n2*a3*d4*b5    + n2*b3*a4*d5    - n2*b3*d4*a5    - n2*d3*a4*b5    + n2*d3*b4*a5    + n4*a1*b2*d3    - n4*a1*b2*d5    - n4*a1*d2*b3    + n4*a1*d2*b5    + n4*a1*b3*d5    - n4*a1*d3*b5    - n4*b1*a2*d3    + n4*b1*a2*d5    + n4*b1*d2*a3    - n4*b1*d2*a5    - n4*b1*a3*d5    + n4*b1*d3*a5    + n4*d1*a2*b3    - n4*d1*a2*b5    - n4*d1*b2*a3    + n4*d1*b2*a5    + n4*d1*a3*b5    - n4*d1*b3*a5    - n4*a2*b3*d5    + n4*a2*d3*b5    + n4*b2*a3*d5    - n4*b2*d3*a5    - n4*d2*a3*b5    + n4*d2*b3*a5    - a1*b2*d3*n5    - a1*b2*d4*n3    + a1*b2*d4*n5    + a1*b2*d5*n3    + a1*d2*b3*n5    + a1*d2*b4*n3    - a1*d2*b4*n5    - a1*d2*b5*n3    - a1*b3*d4*n5    + a1*d3*b4*n5    - a1*b4*d5*n3    + a1*d4*b5*n3    + b1*a2*d3*n5    + b1*a2*d4*n3    - b1*a2*d4*n5    - b1*a2*d5*n3    - b1*d2*a3*n5    - b1*d2*a4*n3    + b1*d2*a4*n5    + b1*d2*a5*n3    + b1*a3*d4*n5    - b1*d3*a4*n5    + b1*a4*d5*n3    - b1*d4*a5*n3    - d1*a2*b3*n5    - d1*a2*b4*n3    + d1*a2*b4*n5    + d1*a2*b5*n3    + d1*b2*a3*n5    + d1*b2*a4*n3    - d1*b2*a4*n5    - d1*b2*a5*n3    - d1*a3*b4*n5    + d1*b3*a4*n5    - d1*a4*b5*n3    + d1*b4*a5*n3    - a2*b3*d4*n1 + a2*b3*d4*n5 + a2*b3*d5*n1 + a2*d3*b4*n1 - a2*d3*b4*n5 - a2*d3*b5*n1 - a2*b4*d5*n1 + a2*b4*d5*n3 + a2*d4*b5*n1 - a2*d4*b5*n3 + b2*a3*d4*n1 - b2*a3*d4*n5 - b2*a3*d5*n1 - b2*d3*a4*n1 + b2*d3*a4*n5 + b2*d3*a5*n1 + b2*a4*d5*n1 - b2*a4*d5*n3 - b2*d4*a5*n1 + b2*d4*a5*n3 - d2*a3*b4*n1 + d2*a3*b4*n5 + d2*a3*b5*n1 + d2*b3*a4*n1 - d2*b3*a4*n5 - d2*b3*a5*n1 - d2*a4*b5*n1 + d2*a4*b5*n3 + d2*b4*a5*n1 - d2*b4*a5*n3 + a3*b4*d5*n1 - a3*d4*b5*n1 - b3*a4*d5*n1 + b3*d4*a5*n1 + d3*a4*b5*n1 - d3*b4*a5*n1)/(n2*a1*b3*c4*d5 - n2*a1*b3*d4*c5 - n2*a1*c3*b4*d5 + n2*a1*c3*d4*b5 + n2*a1*d3*b4*c5 - n2*a1*d3*c4*b5 - n2*b1*a3*c4*d5 + n2*b1*a3*d4*c5 + n2*b1*c3*a4*d5 - n2*b1*c3*d4*a5 - n2*b1*d3*a4*c5 + n2*b1*d3*c4*a5 + n2*c1*a3*b4*d5 - n2*c1*a3*d4*b5 - n2*c1*b3*a4*d5 + n2*c1*b3*d4*a5 + n2*c1*d3*a4*b5 - n2*c1*d3*b4*a5 - n2*d1*a3*b4*c5 + n2*d1*a3*c4*b5 + n2*d1*b3*a4*c5 - n2*d1*b3*c4*a5 - n2*d1*c3*a4*b5 + n2*d1*c3*b4*a5 + n4*a1*b2*c3*d5 - n4*a1*b2*d3*c5 - n4*a1*c2*b3*d5 + n4*a1*c2*d3*b5 + n4*a1*d2*b3*c5 - n4*a1*d2*c3*b5 - n4*b1*a2*c3*d5 + n4*b1*a2*d3*c5 + n4*b1*c2*a3*d5 - n4*b1*c2*d3*a5 - n4*b1*d2*a3*c5 + n4*b1*d2*c3*a5 + n4*c1*a2*b3*d5 - n4*c1*a2*d3*b5 - n4*c1*b2*a3*d5 + n4*c1*b2*d3*a5 + n4*c1*d2*a3*b5 - n4*c1*d2*b3*a5 - n4*d1*a2*b3*c5 + n4*d1*a2*c3*b5 + n4*d1*b2*a3*c5 - n4*d1*b2*c3*a5 - n4*d1*c2*a3*b5 + n4*d1*c2*b3*a5 - a1*b2*c3*d4*n5 + a1*b2*d3*c4*n5 - a1*b2*c4*d5*n3 + a1*b2*d4*c5*n3 + a1*c2*b3*d4*n5 - a1*c2*d3*b4*n5 + a1*c2*b4*d5*n3 - a1*c2*d4*b5*n3 - a1*d2*b3*c4*n5 + a1*d2*c3*b4*n5 - a1*d2*b4*c5*n3 + a1*d2*c4*b5*n3 + b1*a2*c3*d4*n5 - b1*a2*d3*c4*n5 + b1*a2*c4*d5*n3 - b1*a2*d4*c5*n3 - b1*c2*a3*d4*n5 + b1*c2*d3*a4*n5 - b1*c2*a4*d5*n3 + b1*c2*d4*a5*n3 + b1*d2*a3*c4*n5 - b1*d2*c3*a4*n5 + b1*d2*a4*c5*n3 - b1*d2*c4*a5*n3 - c1*a2*b3*d4*n5 + c1*a2*d3*b4*n5 - c1*a2*b4*d5*n3 + c1*a2*d4*b5*n3 + c1*b2*a3*d4*n5 - c1*b2*d3*a4*n5 + c1*b2*a4*d5*n3 - c1*b2*d4*a5*n3 - c1*d2*a3*b4*n5 + c1*d2*b3*a4*n5 - c1*d2*a4*b5*n3 + c1*d2*b4*a5*n3 + d1*a2*b3*c4*n5 - d1*a2*c3*b4*n5 + d1*a2*b4*c5*n3 - d1*a2*c4*b5*n3 - d1*b2*a3*c4*n5 + d1*b2*c3*a4*n5 - d1*b2*a4*c5*n3 + d1*b2*c4*a5*n3 + d1*c2*a3*b4*n5 - d1*c2*b3*a4*n5 + d1*c2*a4*b5*n3 - d1*c2*b4*a5*n3 - a2*b3*c4*d5*n1 + a2*b3*d4*c5*n1 + a2*c3*b4*d5*n1 - a2*c3*d4*b5*n1 - a2*d3*b4*c5*n1 + a2*d3*c4*b5*n1 + b2*a3*c4*d5*n1 - b2*a3*d4*c5*n1 - b2*c3*a4*d5*n1 + b2*c3*d4*a5*n1 + b2*d3*a4*c5*n1 - b2*d3*c4*a5*n1 - c2*a3*b4*d5*n1 + c2*a3*d4*b5*n1 + c2*b3*a4*d5*n1 - c2*b3*d4*a5*n1 - c2*d3*a4*b5*n1 + c2*d3*b4*a5*n1 + d2*a3*b4*c5*n1 - d2*a3*c4*b5*n1 - d2*b3*a4*c5*n1 + d2*b3*c4*a5*n1 + d2*c3*a4*b5*n1 - d2*c3*b4*a5*n1)
        D = (-n2*a1*b3*c4    + n2*a1*b3*c5    + n2*a1*c3*b4    - n2*a1*c3*b5    - n2*a1*b4*c5    + n2*a1*c4*b5    + n2*b1*a3*c4    - n2*b1*a3*c5    - n2*b1*c3*a4    + n2*b1*c3*a5    + n2*b1*a4*c5    - n2*b1*c4*a5    - n2*c1*a3*b4    + n2*c1*a3*b5    + n2*c1*b3*a4    - n2*c1*b3*a5    - n2*c1*a4*b5    + n2*c1*b4*a5    + n2*a3*b4*c5    - n2*a3*c4*b5    - n2*b3*a4*c5    + n2*b3*c4*a5    + n2*c3*a4*b5    - n2*c3*b4*a5    - n4*a1*b2*c3    + n4*a1*b2*c5    + n4*a1*c2*b3    - n4*a1*c2*b5    - n4*a1*b3*c5    + n4*a1*c3*b5    + n4*b1*a2*c3    - n4*b1*a2*c5    - n4*b1*c2*a3    + n4*b1*c2*a5    + n4*b1*a3*c5    - n4*b1*c3*a5    - n4*c1*a2*b3    + n4*c1*a2*b5    + n4*c1*b2*a3    - n4*c1*b2*a5    - n4*c1*a3*b5    + n4*c1*b3*a5    + n4*a2*b3*c5    - n4*a2*c3*b5    - n4*b2*a3*c5    + n4*b2*c3*a5    + n4*c2*a3*b5    - n4*c2*b3*a5    + a1*b2*c3*n5    + a1*b2*c4*n3    - a1*b2*c4*n5    - a1*b2*c5*n3    - a1*c2*b3*n5    - a1*c2*b4*n3    + a1*c2*b4*n5    + a1*c2*b5*n3    + a1*b3*c4*n5    - a1*c3*b4*n5    + a1*b4*c5*n3    - a1*c4*b5*n3    - b1*a2*c3*n5    - b1*a2*c4*n3    + b1*a2*c4*n5    + b1*a2*c5*n3    + b1*c2*a3*n5    + b1*c2*a4*n3    - b1*c2*a4*n5    - b1*c2*a5*n3    - b1*a3*c4*n5    + b1*c3*a4*n5    - b1*a4*c5*n3    + b1*c4*a5*n3    + c1*a2*b3*n5    + c1*a2*b4*n3    - c1*a2*b4*n5    - c1*a2*b5*n3    - c1*b2*a3*n5    - c1*b2*a4*n3    + c1*b2*a4*n5    + c1*b2*a5*n3    + c1*a3*b4*n5    - c1*b3*a4*n5    + c1*a4*b5*n3    - c1*b4*a5*n3    + a2*b3*c4*n1 - a2*b3*c4*n5 - a2*b3*c5*n1 - a2*c3*b4*n1 + a2*c3*b4*n5 + a2*c3*b5*n1 + a2*b4*c5*n1 - a2*b4*c5*n3 - a2*c4*b5*n1 + a2*c4*b5*n3 - b2*a3*c4*n1 + b2*a3*c4*n5 + b2*a3*c5*n1 + b2*c3*a4*n1 - b2*c3*a4*n5 - b2*c3*a5*n1 - b2*a4*c5*n1 + b2*a4*c5*n3 + b2*c4*a5*n1 - b2*c4*a5*n3 + c2*a3*b4*n1 - c2*a3*b4*n5 - c2*a3*b5*n1 - c2*b3*a4*n1 + c2*b3*a4*n5 + c2*b3*a5*n1 + c2*a4*b5*n1 - c2*a4*b5*n3 - c2*b4*a5*n1 + c2*b4*a5*n3 - a3*b4*c5*n1 + a3*c4*b5*n1 + b3*a4*c5*n1 - b3*c4*a5*n1 - c3*a4*b5*n1 + c3*b4*a5*n1)/(n2*a1*b3*c4*d5 - n2*a1*b3*d4*c5 - n2*a1*c3*b4*d5 + n2*a1*c3*d4*b5 + n2*a1*d3*b4*c5 - n2*a1*d3*c4*b5 - n2*b1*a3*c4*d5 + n2*b1*a3*d4*c5 + n2*b1*c3*a4*d5 - n2*b1*c3*d4*a5 - n2*b1*d3*a4*c5 + n2*b1*d3*c4*a5 + n2*c1*a3*b4*d5 - n2*c1*a3*d4*b5 - n2*c1*b3*a4*d5 + n2*c1*b3*d4*a5 + n2*c1*d3*a4*b5 - n2*c1*d3*b4*a5 - n2*d1*a3*b4*c5 + n2*d1*a3*c4*b5 + n2*d1*b3*a4*c5 - n2*d1*b3*c4*a5 - n2*d1*c3*a4*b5 + n2*d1*c3*b4*a5 + n4*a1*b2*c3*d5 - n4*a1*b2*d3*c5 - n4*a1*c2*b3*d5 + n4*a1*c2*d3*b5 + n4*a1*d2*b3*c5 - n4*a1*d2*c3*b5 - n4*b1*a2*c3*d5 + n4*b1*a2*d3*c5 + n4*b1*c2*a3*d5 - n4*b1*c2*d3*a5 - n4*b1*d2*a3*c5 + n4*b1*d2*c3*a5 + n4*c1*a2*b3*d5 - n4*c1*a2*d3*b5 - n4*c1*b2*a3*d5 + n4*c1*b2*d3*a5 + n4*c1*d2*a3*b5 - n4*c1*d2*b3*a5 - n4*d1*a2*b3*c5 + n4*d1*a2*c3*b5 + n4*d1*b2*a3*c5 - n4*d1*b2*c3*a5 - n4*d1*c2*a3*b5 + n4*d1*c2*b3*a5 - a1*b2*c3*d4*n5 + a1*b2*d3*c4*n5 - a1*b2*c4*d5*n3 + a1*b2*d4*c5*n3 + a1*c2*b3*d4*n5 - a1*c2*d3*b4*n5 + a1*c2*b4*d5*n3 - a1*c2*d4*b5*n3 - a1*d2*b3*c4*n5 + a1*d2*c3*b4*n5 - a1*d2*b4*c5*n3 + a1*d2*c4*b5*n3 + b1*a2*c3*d4*n5 - b1*a2*d3*c4*n5 + b1*a2*c4*d5*n3 - b1*a2*d4*c5*n3 - b1*c2*a3*d4*n5 + b1*c2*d3*a4*n5 - b1*c2*a4*d5*n3 + b1*c2*d4*a5*n3 + b1*d2*a3*c4*n5 - b1*d2*c3*a4*n5 + b1*d2*a4*c5*n3 - b1*d2*c4*a5*n3 - c1*a2*b3*d4*n5 + c1*a2*d3*b4*n5 - c1*a2*b4*d5*n3 + c1*a2*d4*b5*n3 + c1*b2*a3*d4*n5 - c1*b2*d3*a4*n5 + c1*b2*a4*d5*n3 - c1*b2*d4*a5*n3 - c1*d2*a3*b4*n5 + c1*d2*b3*a4*n5 - c1*d2*a4*b5*n3 + c1*d2*b4*a5*n3 + d1*a2*b3*c4*n5 - d1*a2*c3*b4*n5 + d1*a2*b4*c5*n3 - d1*a2*c4*b5*n3 - d1*b2*a3*c4*n5 + d1*b2*c3*a4*n5 - d1*b2*a4*c5*n3 + d1*b2*c4*a5*n3 + d1*c2*a3*b4*n5 - d1*c2*b3*a4*n5 + d1*c2*a4*b5*n3 - d1*c2*b4*a5*n3 - a2*b3*c4*d5*n1 + a2*b3*d4*c5*n1 + a2*c3*b4*d5*n1 - a2*c3*d4*b5*n1 - a2*d3*b4*c5*n1 + a2*d3*c4*b5*n1 + b2*a3*c4*d5*n1 - b2*a3*d4*c5*n1 - b2*c3*a4*d5*n1 + b2*c3*d4*a5*n1 + b2*d3*a4*c5*n1 - b2*d3*c4*a5*n1 - c2*a3*b4*d5*n1 + c2*a3*d4*b5*n1 + c2*b3*a4*d5*n1 - c2*b3*d4*a5*n1 - c2*d3*a4*b5*n1 + c2*d3*b4*a5*n1 + d2*a3*b4*c5*n1 - d2*a3*c4*b5*n1 - d2*b3*a4*c5*n1 + d2*b3*c4*a5*n1 + d2*c3*a4*b5*n1 - d2*c3*b4*a5*n1)
        F = (-n2*a1*b3*c4*d5 + n2*a1*b3*d4*c5 + n2*a1*c3*b4*d5 - n2*a1*c3*d4*b5 - n2*a1*d3*b4*c5 + n2*a1*d3*c4*b5 + n2*b1*a3*c4*d5 - n2*b1*a3*d4*c5 - n2*b1*c3*a4*d5 + n2*b1*c3*d4*a5 + n2*b1*d3*a4*c5 - n2*b1*d3*c4*a5 - n2*c1*a3*b4*d5 + n2*c1*a3*d4*b5 + n2*c1*b3*a4*d5 - n2*c1*b3*d4*a5 - n2*c1*d3*a4*b5 + n2*c1*d3*b4*a5 + n2*d1*a3*b4*c5 - n2*d1*a3*c4*b5 - n2*d1*b3*a4*c5 + n2*d1*b3*c4*a5 + n2*d1*c3*a4*b5 - n2*d1*c3*b4*a5 - n4*a1*b2*c3*d5 + n4*a1*b2*d3*c5 + n4*a1*c2*b3*d5 - n4*a1*c2*d3*b5 - n4*a1*d2*b3*c5 + n4*a1*d2*c3*b5 + n4*b1*a2*c3*d5 - n4*b1*a2*d3*c5 - n4*b1*c2*a3*d5 + n4*b1*c2*d3*a5 + n4*b1*d2*a3*c5 - n4*b1*d2*c3*a5 - n4*c1*a2*b3*d5 + n4*c1*a2*d3*b5 + n4*c1*b2*a3*d5 - n4*c1*b2*d3*a5 - n4*c1*d2*a3*b5 + n4*c1*d2*b3*a5 + n4*d1*a2*b3*c5 - n4*d1*a2*c3*b5 - n4*d1*b2*a3*c5 + n4*d1*b2*c3*a5 + n4*d1*c2*a3*b5 - n4*d1*c2*b3*a5 + a1*b2*c3*d4*n5 - a1*b2*d3*c4*n5 + a1*b2*c4*d5*n3 - a1*b2*d4*c5*n3 - a1*c2*b3*d4*n5 + a1*c2*d3*b4*n5 - a1*c2*b4*d5*n3 + a1*c2*d4*b5*n3 + a1*d2*b3*c4*n5 - a1*d2*c3*b4*n5 + a1*d2*b4*c5*n3 - a1*d2*c4*b5*n3 - b1*a2*c3*d4*n5 + b1*a2*d3*c4*n5 - b1*a2*c4*d5*n3 + b1*a2*d4*c5*n3 + b1*c2*a3*d4*n5 - b1*c2*d3*a4*n5 + b1*c2*a4*d5*n3 - b1*c2*d4*a5*n3 - b1*d2*a3*c4*n5 + b1*d2*c3*a4*n5 - b1*d2*a4*c5*n3 + b1*d2*c4*a5*n3 + c1*a2*b3*d4*n5 - c1*a2*d3*b4*n5 + c1*a2*b4*d5*n3 - c1*a2*d4*b5*n3 - c1*b2*a3*d4*n5 + c1*b2*d3*a4*n5 - c1*b2*a4*d5*n3 + c1*b2*d4*a5*n3 + c1*d2*a3*b4*n5 - c1*d2*b3*a4*n5 + c1*d2*a4*b5*n3 - c1*d2*b4*a5*n3 - d1*a2*b3*c4*n5 + d1*a2*c3*b4*n5 - d1*a2*b4*c5*n3 + d1*a2*c4*b5*n3 + d1*b2*a3*c4*n5 - d1*b2*c3*a4*n5 + d1*b2*a4*c5*n3 - d1*b2*c4*a5*n3 - d1*c2*a3*b4*n5 + d1*c2*b3*a4*n5 - d1*c2*a4*b5*n3 + d1*c2*b4*a5*n3 + a2*b3*c4*d5*n1 - a2*b3*d4*c5*n1 - a2*c3*b4*d5*n1 + a2*c3*d4*b5*n1 + a2*d3*b4*c5*n1 - a2*d3*c4*b5*n1 - b2*a3*c4*d5*n1 + b2*a3*d4*c5*n1 + b2*c3*a4*d5*n1 - b2*c3*d4*a5*n1 - b2*d3*a4*c5*n1 + b2*d3*c4*a5*n1 + c2*a3*b4*d5*n1 - c2*a3*d4*b5*n1 - c2*b3*a4*d5*n1 + c2*b3*d4*a5*n1 + c2*d3*a4*b5*n1 - c2*d3*b4*a5*n1 - d2*a3*b4*c5*n1 + d2*a3*c4*b5*n1 + d2*b3*a4*c5*n1 - d2*b3*c4*a5*n1 - d2*c3*a4*b5*n1 + d2*c3*b4*a5*n1)/(a1*b2*c3*d4 - a1*b2*c3*d5 - a1*b2*d3*c4 + a1*b2*d3*c5 + a1*b2*c4*d5 - a1*b2*d4*c5 - a1*c2*b3*d4 + a1*c2*b3*d5 + a1*c2*d3*b4 - a1*c2*d3*b5 - a1*c2*b4*d5 + a1*c2*d4*b5 + a1*d2*b3*c4 - a1*d2*b3*c5 - a1*d2*c3*b4 + a1*d2*c3*b5 + a1*d2*b4*c5 - a1*d2*c4*b5 - a1*b3*c4*d5 + a1*b3*d4*c5 + a1*c3*b4*d5 - a1*c3*d4*b5 - a1*d3*b4*c5 + a1*d3*c4*b5 - b1*a2*c3*d4 + b1*a2*c3*d5 + b1*a2*d3*c4 - b1*a2*d3*c5 - b1*a2*c4*d5 + b1*a2*d4*c5 + b1*c2*a3*d4 - b1*c2*a3*d5 - b1*c2*d3*a4 + b1*c2*d3*a5 + b1*c2*a4*d5 - b1*c2*d4*a5 - b1*d2*a3*c4 + b1*d2*a3*c5 + b1*d2*c3*a4 - b1*d2*c3*a5 - b1*d2*a4*c5 + b1*d2*c4*a5 + b1*a3*c4*d5 - b1*a3*d4*c5 - b1*c3*a4*d5 + b1*c3*d4*a5 + b1*d3*a4*c5 - b1*d3*c4*a5 + c1*a2*b3*d4 - c1*a2*b3*d5 - c1*a2*d3*b4 + c1*a2*d3*b5 + c1*a2*b4*d5 - c1*a2*d4*b5 - c1*b2*a3*d4 + c1*b2*a3*d5 + c1*b2*d3*a4 - c1*b2*d3*a5 - c1*b2*a4*d5 + c1*b2*d4*a5 + c1*d2*a3*b4 - c1*d2*a3*b5 - c1*d2*b3*a4 + c1*d2*b3*a5 + c1*d2*a4*b5 - c1*d2*b4*a5 - c1*a3*b4*d5 + c1*a3*d4*b5 + c1*b3*a4*d5 - c1*b3*d4*a5 - c1*d3*a4*b5 + c1*d3*b4*a5 - d1*a2*b3*c4 + d1*a2*b3*c5 + d1*a2*c3*b4 - d1*a2*c3*b5 - d1*a2*b4*c5 + d1*a2*c4*b5 + d1*b2*a3*c4 - d1*b2*a3*c5 - d1*b2*c3*a4 + d1*b2*c3*a5 + d1*b2*a4*c5 - d1*b2*c4*a5 - d1*c2*a3*b4 + d1*c2*a3*b5 + d1*c2*b3*a4 - d1*c2*b3*a5 - d1*c2*a4*b5 + d1*c2*b4*a5 + d1*a3*b4*c5 - d1*a3*c4*b5 - d1*b3*a4*c5 + d1*b3*c4*a5 + d1*c3*a4*b5 - d1*c3*b4*a5 + a2*b3*c4*d5 - a2*b3*d4*c5 - a2*c3*b4*d5 + a2*c3*d4*b5 + a2*d3*b4*c5 - a2*d3*c4*b5 - b2*a3*c4*d5 + b2*a3*d4*c5 + b2*c3*a4*d5 - b2*c3*d4*a5 - b2*d3*a4*c5 + b2*d3*c4*a5 + c2*a3*b4*d5 - c2*a3*d4*b5 - c2*b3*a4*d5 + c2*b3*d4*a5 + c2*d3*a4*b5 - c2*d3*b4*a5 - d2*a3*b4*c5 + d2*a3*c4*b5 + d2*b3*a4*c5 - d2*b3*c4*a5 - d2*c3*a4*b5 + d2*c3*b4*a5)
        
        print(A)
        print(B)
        print(C)
        print(D)
        print(F)
        
    else:
        return [A, B, C]

############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################


















###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################

# from scipy.optimize import curve_fit

# def func_fit(x, A, B, C):
#     return (A*(1 + B*(ROOT.cos(x)) + C*(ROOT.cos(2*x))))

from functools import partial

def func_fit(params, x, y):
    A, B, C = params
    y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi))) for xi in x]
    return sum((y_pred[i] - y[i])**2 for i in range(len(x)))

def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
    N = len(x0)
    simplex = [x0]
    for i in range(N):
        point = list(x0)
        point[i] = x0[i] + 1.0
        simplex.append(point)
    
    for _ in range(max_iter):
        simplex.sort(key=lambda point: func(point, *args))
        if abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol:
            break
        centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
        reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
        if func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args):
            simplex[-1] = reflected
            continue
        if func(reflected, *args) < func(simplex[0], *args):
            expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
            if func(expanded, *args) < func(reflected, *args):
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected
            continue
        contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
        if func(contracted, *args) < func(simplex[-1], *args):
            simplex[-1] = contracted
            continue
        for i in range(1, N+1):
            simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]
    
    return simplex[0]

def Full_Calc_Fit(Histo):
    # Helping the closure tests with known values of B and C
    if(Closure_Test and False):
        B_opt, C_opt = -0.500, 0.025
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    elif(Sim_Test and False):
        B_opt, C_opt = 0, 0
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    else:
        x_data, y_data = [], []
        try:
            # print("Histo.GetNbinsX() =", Histo.GetNbinsX())
            for ii in range(0, Histo.GetNbinsX(), 1):
    #             x_data.append((3.1415926/180)*(Histo.GetBinCenter(ii)))
                x_data.append(Histo.GetBinCenter(ii))
                y_data.append(Histo.GetBinContent(ii))

    #         # Perform curve fitting
    #         popt, pcov = curve_fit(func_fit, x_data, y_data)
    #         # Extract the optimized parameters
    #         A_opt, B_opt, C_opt = popt

            # Perform optimization using the Nelder-Mead method
            initial_guess = [1e6, 1, 1]  # Initial guess for A, B, C
            optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)

            # Extract the optimized parameters
            A_opt, B_opt, C_opt = optim_params

        except:
            print(f"{color.Error}Full_Calc_Fit(...) ERROR:{color.END}\n{traceback.format_exc()}\n\n{color.Error}ERROR is with 'Histo' = {Histo}\n{color.END}")
            A_opt, B_opt, C_opt = "Error", "Error", "Error"
        
    return [A_opt, B_opt, C_opt]



extra_function_terms = False
# extra_function_terms = True

if(extra_function_terms):
    # def func_fit(params, x, y):
    #     A, B, C, D, E = params
    #     y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi)) + D*(ROOT.cos(3*xi)) + E*(ROOT.cos(4*xi))) for xi in x]
    #     return sum((y_pred[i] - y[i])**2 for i in range(len(x)))
    def func_fit(params, x, y):
        A, B, C, D = params
        y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi)) + D*(ROOT.cos(3*xi))) for xi in x]
        return sum((y_pred[i] - y[i])**2 for i in range(len(x)))

    def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
        N = len(x0)
        simplex = [x0]
        for i in range(N):
            point = list(x0)
            point[i] = x0[i] + 1.0
            simplex.append(point)

        for _ in range(max_iter):
            simplex.sort(key=lambda point: func(point, *args))
            if abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol:
                break
            centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
            reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
            if func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args):
                simplex[-1] = reflected
                continue
            if func(reflected, *args) < func(simplex[0], *args):
                expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
                if func(expanded, *args) < func(reflected, *args):
                    simplex[-1] = expanded
                else:
                    simplex[-1] = reflected
                continue
            contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
            if func(contracted, *args) < func(simplex[-1], *args):
                simplex[-1] = contracted
                continue
            for i in range(1, N+1):
                simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]

        return simplex[0]

    
    def Full_Calc_Fit(Histo):
        x_data, y_data = [], []
        try:
            # print("Histo.GetNbinsX() =", Histo.GetNbinsX())
            for ii in range(0, Histo.GetNbinsX(), 1):
                x_data.append(Histo.GetBinCenter(ii))
                y_data.append(Histo.GetBinContent(ii))
            # Perform optimization using the Nelder-Mead method
            initial_guess = [1e6, 1, 1, 1]  # Initial guess for A, B, C, D
            optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)
            # Extract the optimized parameters
            A_opt, B_opt, C_opt, D_opt = optim_params
        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)
            A_opt, B_opt, C_opt, D_opt = "Error", "Error", "Error", "Error"
        return [A_opt, B_opt, C_opt, D_opt]

###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################




















##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##










def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default", MC_BGS_1D="None"):
    
##############################################################################################################
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Original)   #####=====#####=====#####=====#####
##############################################################################################################
    if(Method in ["SVD"]):
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.BLUE}SVD{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        # print(f'\t{color.BOLD}Unfolding Histogram:{color.END}\n\t{str(Name_Main_Print).replace("(Data-Type=\'mdf\'), ", "")}')
        clean_name = str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")
        print(f"\t{color.BOLD}Unfolding Histogram:{color.END}\n\t{clean_name}")
        del clean_name
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        ExREAL_1D.GetXaxis().SetRange(0,     nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0,   nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0,   nBins_CVM)     # Response Matrix (Y axis --> REC)
        
        Covariance_Matrix = ROOT.TH2D(f"statcov_{Name_Main}", f"Covariance Matrix for: {Name_Main}", nBins_CVM, MinBinCVM, MaxBinCVM, nBins_CVM, MinBinCVM, MaxBinCVM)
        
        #######################################################################################
        ##==========##==========##   Filling the Covariance Matrix   ##==========##==========##
        #######################################################################################
        for CVM_Bin in range(0, nBins_CVM):
            Covariance_Matrix.SetBinContent(CVM_Bin, CVM_Bin, ExREAL_1D.GetBinError(CVM_Bin)*ExREAL_1D.GetBinError(CVM_Bin))
        ######################################################################################
        ##==========##==========##   Filled the Covariance Matrix   ##==========##==========##
        ######################################################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        Reg_Par = 13
        ##=====##  Unfolding Regularization Parameter  ##=====##
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D.GetNbinsX() == Response_2D.GetNbinsY()):
            try:
                Unfold_Obj = ROOT.TSVDUnfold(ExREAL_1D, Covariance_Matrix, MC_REC_1D, MC_GEN_1D, Response_2D)
                Unfold_Obj.SetNormalize(False)

                Unfolded_Histo = Unfold_Obj.Unfold(Reg_Par)

                Unfolded_Histo.SetLineColor(root_color.Pink)
                Unfolded_Histo.SetMarkerColor(root_color.Pink)
                Unfolded_Histo.SetMarkerSize(3)
                Unfolded_Histo.SetLineWidth(2)
                
                Unfolded_Determinate = Unfold_Obj.GetD()
                # Unfolded_Single_Value = Unfold_Obj[Unfolding_Canvas_Name].GetSV()

                unfolding_toys = 100

                Unfolded_Covariance_Matrix = Unfold_Obj.GetUnfoldCovMatrix(Covariance_Matrix, unfolding_toys)

                Error_Matrix = Unfold_Obj.GetAdetCovMatrix(100)

                Unfolded_Covariance_Matrix.Add(Error_Matrix)

                Regularized_CV_Matrix = Unfold_Obj.GetXtau()

                Regularized_CV_Matrix.Add(Error_Matrix)

                # Inverse_CV_Matrix = Unfold_Obj.GetXinv()

                for ii in range(1, Unfolded_Histo.GetNbinsX() + 1):
                    Unfolded_Histo.SetBinError(ii, ROOT.sqrt(Regularized_CV_Matrix.GetBinContent(ii, ii)))
                
                Unfolded_Histo.SetTitle(((str(Unfolded_Histo.GetTitle()).replace("Experimental", "SVD Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(Unfolded_Histo.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))
                
                List_Of_Outputs = [Unfolded_Histo, Unfold_Obj, Unfolded_Determinate, Unfolded_Covariance_Matrix, Regularized_CV_Matrix]    
                
                print(f"{color.BCYAN}Finished {color.BLUE}SVD{color.END_B}{color.CYAN} Unfolding Procedure.\n{color.END}")
                return List_Of_Outputs

            except:
                print(f"\n{color.Error}FAILED TO UNFOLD A HISTOGRAM (SVD)...\nERROR:\n{color.END}{traceback.format_exc()}")
                
                
        else:
            print(f"{color.RED}Unequal Bins...{color.END}")
            print(f"nBins_CVM = {nBins_CVM}")
            print(f"MC_REC_1D.GetNbinsX() = {MC_REC_1D.GetNbinsX()}")
            print(f"MC_GEN_1D.GetNbinsX() = {MC_GEN_1D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsX() = {Response_2D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsY() = {Response_2D.GetNbinsY()}")
            return "ERROR"
####################################################################################################################
#####=====#####=====#####=====#####     End of Method: "SVD" (Original)          #####=====#####=====#####=====#####
####################################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
############################################################################################################
    elif((Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]) or (Response_2D in ["N/A", "None", "Error"])):
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.PURPLE}Bin-by-Bin{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        if(Response_2D in ["N/A", "None", "Error"]):
            print(f"{color.Error}WARNING: NOT Using Response Matrix for unfolding{color.END}")
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        clean_name = str(Name_Print).replace("(Data-Type='mdf'), ", "")
        print(f"\t{color.BOLD}Acceptance Correction of Histogram:{color.END}\n\t{clean_name}")
        del clean_name
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            if(MC_BGS_1D not in ["None"]):
                # Add the background back into the acceptance calculation
                Bin_Acceptance.Add(MC_BGS_1D)
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Acceptance.SetTitle(str(Bin_Acceptance.GetTitle()).replace("Reconstructed (MC) Distribution of", "Bin-by-Bin Acceptance for"))
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Corrected")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Unfolded.Sumw2()
            
            cut_criteria = Min_Allowed_Acceptance_Cut

            if(any(Sector_Cut in str(Name_Print) for Sector_Cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"])):
                print(f"{color.RED}NOTE: Reducing Acceptance Cut criteria by 50% for Sector Cut plots{color.END}")
                cut_criteria = 0.5*Min_Allowed_Acceptance_Cut
            
            for ii in range(0, Bin_Acceptance.GetNbinsX() + 1):
                if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
                    if(Bin_Acceptance.GetBinContent(ii) != 0):
                        print(f"{color.RED}\nBin {ii} had a very low acceptance...\n\t(cut_criteria = {cut_criteria})\n\t(Bin_Content  = {Bin_Acceptance.GetBinContent(ii)}){color.END}")
                    # Bin_Unfolded.SetBinError(ii,   Bin_Unfolded.GetBinContent(ii) + Bin_Unfolded.GetBinError(ii))
                    Bin_Unfolded.SetBinError(ii,   0)
                    Bin_Unfolded.SetBinContent(ii, 0)
            
            print(f"{color.BCYAN}Finished {color.PURPLE}Bin-by-Bin{color.END_B}{color.CYAN} Unfolding Procedure.{color.END}")
            if(Response_2D in ["N/A", "None", "Error"]):
                return [Bin_Unfolded, Bin_Acceptance]
        except:
            print(f"\n{color.Error}FAILED TO CORRECT A HISTOGRAM (Bin-by-Bin)...\nERROR:\n{color.END}{traceback.format_exc()}")
            
            return "ERROR"
############################################################################################################
#####=====#####=====#####=====#####     End of Method:  "Bin-by-Bin"     #####=====#####=====#####=====#####
############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

##############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====#####
##############################################################################################################
    if((("RooUnfold" in str(Method)) or (str(Method) in ["Default"]) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])) and (Response_2D not in ["N/A", "None", "Error"])):
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.GREEN}RooUnfold{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        clean_name = str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")
        print(f"\t{color.BOLD}Unfolding Histogram:{color.END}\n\t{clean_name}")
        del clean_name
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width
        
        ExREAL_1D.GetXaxis().SetRange(0,     nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0,   nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0,   nBins_CVM)     # Response Matrix (Y axis --> REC)
        if(MC_BGS_1D != "None"):
            MC_BGS_1D.GetXaxis().SetRange(0, nBins_CVM)     # MC Background Subtracted Distribution
            
        if(("MultiDim_Q2_y_z_pT_phi_h" not in str(Name_Main)) or ("5D_Unfold_Test_V1_All" in str(MC_REC_File_Name))):
            Response_2D_Input_Title = f"{Response_2D.GetTitle()};{Response_2D.GetYaxis().GetTitle()};{Response_2D.GetXaxis().GetTitle()}"
            Response_2D_Input       = ROOT.TH2D(f"{Response_2D.GetName()}_Flipped", str(Response_2D_Input_Title), Response_2D.GetNbinsY(), MinBinCVM, MaxBinCVM, Response_2D.GetNbinsX(), MinBinCVM, MaxBinCVM)
            # Use the following code if the input Response Matrix plots the generated events on the x-axis
            # # The RooUnfold library takes Response Matrices which plot the true/generated events on the y-axis and the measured/reconstructed events on the x-axis
            ##==============##============================================##==============##
            ##==============##=====##     Flipping Response_2D     ##=====##==============##
            ##=========##   Generated Bins       ##=====##
            for gen_bin in range(0, nBins_CVM + 1):
                ##=====##   Reconstructed Bins   ##=====##
                for rec_bin in range(0, nBins_CVM + 1):
                    Res_Value = Response_2D.GetBinContent(gen_bin,    rec_bin)
                    Res_Error = Response_2D.GetBinError(gen_bin,      rec_bin)
                    Response_2D_Input.SetBinContent(rec_bin, gen_bin, Res_Value)
                    Response_2D_Input.SetBinError(rec_bin,   gen_bin, Res_Error)
            ##==============##=====##     Flipped Response_2D      ##=====##==============##
            ##==============##============================================##==============##
            # Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = f"{Response_2D.GetTitle()};{Response_2D.GetXaxis().GetTitle()};{Response_2D.GetYaxis().GetTitle()}"
            Response_2D_Input       = Response_2D
        del Response_2D

        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                # Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, f"{str(Response_2D_Input.GetName()).replace('_Flipped', '')}_RooUnfoldResponse_Object", Response_2D_Input_Title)
                if(MC_BGS_1D != "None"):
                    # Background Subtraction Method 1: Fill the Response_RooUnfold object explicitly with the content of a background histogram with the Fake() function
                    for rec_bin in range(0, nBins_CVM + 1):
                        rec_val = MC_BGS_1D.GetBinCenter(rec_bin)
                        rec_con = MC_BGS_1D.GetBinContent(rec_bin)
                        Response_RooUnfold.Fake(rec_val, w=rec_con)
                    # Background Subtraction Method 2:
                        # Should be possible to add MC_BGS_1D to MC_REC_1D to combine those plots where MC_REC_1D != the projection of Response_2D_Input since MC_REC_1D would (in this case) still contain events which would be identifified as background in MC_BGS_1D
                        # This is likely the better approach computationally, though some testing needs to be done to get the execution working correctly
##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if("svd" in str(Method)):
                    Unfold_Title = "RooUnfold (SVD)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    ##=====##  SVD Regularization Parameter  ##=====##
                    Reg_Par = 13
                    ##=====##  SVD Regularization Parameter  ##=====##
                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)
                elif(("bbb" in str(Method)) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)
                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)
                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print(f"\t{color.RED}Method '{color.BOLD}{Method}{color.END_R}' is unknown/undefined...{color.END}")
                        print(f"\t{color.RED}Defaulting to using the {color.BGREEN}{Unfold_Title}{color.END_R} method to unfold...{color.END}")
                    else:
                        print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} method to unfold...{color.END}")

                        
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = (10 if(not Closure_Test) else 10) if(("Multi_Dim" not in str(Name_Main)) or (("Multi_Dim_z_pT_Bin" in str(Name_Main)) or ("MultiDim_z_pT" in str(Name_Main)))) else 4
                    if(Pass_Version not in ["", "Pass 1"]):
                        bayes_iterations += 3
                    if("MultiDim_Q2_y_z_pT_phi_h" in str(Name_Main)):
                        # 5D Unfolding
                        bayes_iterations = 4
                        print(f"{color.BOLD}Performing 5D Unfolding with {color.UNDERLINE}{bayes_iterations}{color.END_B} iteration(s)...{color.END}")
                    if(args.bayes_iterations):
                        if(args.bayes_iterations != bayes_iterations):
                            bayes_iterations = args.bayes_iterations
                            print(f"{color.BOLD}Performing Unfolding with {color.UNDERLINE}{bayes_iterations}{color.END_B} iteration(s)...{color.END}")
                    else:
                        args.bayes_iterations = bayes_iterations
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)
                    Unfolding_Histo.SetNToys(args.Num_Toys)

##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                if(any(method in str(Method) for method in ["bbb", "svd", "inv"]) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])):
                    Unfolded_Histo = Unfolding_Histo.Hunfold()
                else:
                    Unfolded_Histo = Unfolding_Histo.Hunfold(ROOT.RooUnfold.kCovToys)
                    
                for bin_rec in range(0, MC_REC_1D.GetNbinsX() + 1):
                    if(MC_REC_1D.GetBinContent(bin_rec) == 0):
                        Unfolded_Histo.SetBinError(bin_rec,          Unfolded_Histo.GetBinContent(bin_rec)        + Unfolded_Histo.GetBinError(bin_rec))
                        # Unfolded_Histo.SetBinError(bin_rec,          0)
                        # Unfolded_Histo.SetBinContent(bin_rec,        0)
                        
                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    Bin_Acceptance = MC_REC_1D.Clone()
                    Bin_Acceptance.Sumw2()
                    Bin_Acceptance.Divide(MC_GEN_1D)
                for bin_acceptance in range(0, Bin_Acceptance.GetNbinsX() + 1):
                    if((all(cut not in str(Name_Main_Print) for cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"]) and (Bin_Acceptance.GetBinContent(bin_acceptance) < Min_Allowed_Acceptance_Cut)) or (Bin_Acceptance.GetBinContent(bin_acceptance) < 0.5*Min_Allowed_Acceptance_Cut)):
                        # Condition above applied normal Acceptance Cuts only when the Sector Cuts are NOT present but will always apply the cuts if the acceptance is less than 50% of the normal set value
                        # Unfolded_Histo.SetBinError(bin_acceptance,   Unfolded_Histo.GetBinContent(bin_acceptance) + Unfolded_Histo.GetBinError(bin_acceptance))
                        Unfolded_Histo.SetBinError(bin_acceptance,   0)
                        Unfolded_Histo.SetBinContent(bin_acceptance, 0)
                        
                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print(f"{color.BCYAN}Finished {color.GREEN}{Unfold_Title}{color.END_B}{color.CYAN} Unfolding Procedure.\n{color.END}")
                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    return [Unfolded_Histo, Response_RooUnfold]
                else:
                    return [Unfolded_Histo, Bin_Acceptance]
                    
            except:
                print(f"\n{color.Error}FAILED TO UNFOLD A HISTOGRAM (RooUnfold)...\nERROR:\n{color.END}{traceback.format_exc()}")
                
        else:
            print(f"{color.RED}Unequal Bins...{color.END}")
            print(f"nBins_CVM = {nBins_CVM}")
            print(f"MC_REC_1D.GetNbinsX() = {MC_REC_1D.GetNbinsX()}")
            print(f"MC_GEN_1D.GetNbinsX() = {MC_GEN_1D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsX() = {Response_2D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsY() = {Response_2D.GetNbinsY()}")
            return "ERROR"
    
    else:
        print(f"Procedure for Method '{Method}' has not yet been defined...")
        return "ERROR"
    
    print(f"\n{color.Error}ERROR: DID NOT RETURN A HISTOGRAM YET...{color.END}\n")
    return "ERROR"





    
    
    
    
    
    
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##










######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################

import re
def Histogram_Name_Def(out_print, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="All", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"):
    # if(Data_Type in ["Background"]):
    #     Data_Type = "mdf"
    Pattern_List = []
    Pattern_Histo_General = r"\(Histo-Group='([^']+)'"
    Pattern_Data_Type     = r"\(Data-Type='([^']+)'"
    Pattern_Cut_Type      = r"\(Data-Cut='([^']+)'"
    Pattern_Smear_Type    = r"\(Smear-Type='([^']+)'"
    Pattern_Q2_y_Bin      = r"\[Q2-y-Bin=([^,]+),"
    Pattern_Var_1         = r"\(Var-D1='([^']+)'"
    Pattern_Var_2         = r"\(Var-D2='([^']+)'"
    # Pattern_Var_3         = r"\(Var-D3='([^']+)'"
    
    if(Histo_General  == "Find"):
        Pattern_List.append(Pattern_Histo_General)
    else:
        Pattern_List.append(Histo_General)
    if(Data_Type      == "Find"):
        Pattern_List.append(Pattern_Data_Type)
    else:
        Pattern_List.append(Data_Type)
    if(Cut_Type       == "Find"):
        Pattern_List.append(Pattern_Cut_Type)
    elif(Cut_Type not in ["Skip", "skip"]):
        Pattern_List.append(Cut_Type)
    if(Smear_Type     == "Find"):
        Pattern_List.append(Pattern_Smear_Type)
    else:
        Pattern_List.append(Smear_Type)
        

    if(Bin_Extra      == "Default"):
        Pattern_List.append(str("".join(["Q2_y_Bin_", str(Q2_y_Bin) if(Q2_y_Bin != 0) else "All"])) if(Q2_y_Bin not in ["Find"]) else Pattern_Q2_y_Bin)
        Pattern_List.append("".join(["z_pT_Bin_", str(z_pT_Bin) if(z_pT_Bin != 0) else "All"]))
    elif(Bin_Extra not in ["Skip", "skip"]):
        Pattern_List.append("".join(["Kinematic_Bin_", str(Bin_Extra) if(Bin_Extra != 0) else "All"]))
        
    if(Variable       == "Default"):
        Pattern_List.append(Pattern_Var_1)
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    elif(Variable     in ["Find", "FindAll", "FindOnly"]):
        Pattern_List = [Pattern_Var_1]
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    else:
        Pattern_List.append(Variable)
        
    if(Q2_y_Bin in ["FindOnly"]):
        Pattern_List = [Pattern_Q2_y_Bin]
        
    Name_Output = ""
    
    for pattern in Pattern_List:
        if(pattern in [r"\(Histo-Group='([^']+)'", r"\(Data-Type='([^']+)'", r"\(Data-Cut='([^']+)'", r"\(Smear-Type='([^']+)'", r"\[Q2-y-Bin=([^,]+),", r"\(Var-D1='([^']+)'", r"\(Var-D2='([^']+)'"]):
            match = re.search(pattern, out_print.replace("''", "' '"))
            if(match):
                histo_group = match.group(1)
                if((histo_group == " ")):
                    histo_group = "''"
                if(pattern == Pattern_Smear_Type):
                    histo_group = "".join(["SMEAR=", "".join(["'", str(histo_group), "'"]) if(histo_group != "''") else str(histo_group)]) 
                if(pattern == Pattern_Q2_y_Bin):
                    histo_group = f"Q2_y_Bin_{histo_group}"
        else:
            histo_group = pattern
            if(pattern == Smear_Type):
                histo_group = "".join(["SMEAR=", pattern if(pattern != "") else "''"])
        Name_Output = "".join([Name_Output, "_(" if(str(Name_Output) != "") else "(", str(histo_group), ")"])
        # if(("rdf" in str(Name_Output)) or ("gdf" in str(Name_Output))):
        #     Name_Output = Name_Output.replace("Smear", "''")
        
    if((Variable in ["Find", "FindAll", "FindOnly"]) and (")_(" not in str(Name_Output))):
        Name_Output = Name_Output.replace("(", "")
        Name_Output = Name_Output.replace(")", "")
    
    Name_Output = str(Name_Output.replace("cut_Complete_SIDIS_Proton",    "Proton"))
    Name_Output = str(Name_Output.replace("cut_Complete_SIDIS_Integrate", "Integrate"))
    if(args.single_file and (Closure_Test or Mod_Test or Sim_Test) and (")_(" in str(Name_Output)) and all(extra not in str(Name_Output) for extra in ["Mod_Test", "Closure_Test", "Sim_Test"])):
        Name_Output = f"{Name_Output}_({'Mod_Test' if(Mod_Test) else 'Closure_Test' if(Closure_Test) else 'Sim_Test'})"
    
    return Name_Output

######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default", Special="Normal", Use_Higher_Terms=extra_function_terms):
    if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true"]) and (Fitting in ["default", "Default"]) and Fit_Test):
        if(not Use_Higher_Terms):
            A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
        else:
            A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"

        # Fitting_Function = ROOT.TF1("".join(["Fitting_Function", str(Method).replace(" ", "_")]), str(fit_function), 0, 360)
        Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit.GetName()}_{str(Method).replace(' ', '_')}", str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")

        fit_range_lower = 0
        fit_range_upper = 360
        # Number of bins in the histogram
        n_bins = Histo_To_Fit.GetNbinsX()
        
        # Find the lower fit range (first non-empty bin)
        for bin_lower in range(1, n_bins // 2 + 1):  # Search from the start to the center
            if(Histo_To_Fit.GetBinContent(bin_lower) != 0):
                fit_range_lower = Histo_To_Fit.GetXaxis().GetBinLowEdge(bin_lower)
                break  # Stop the loop once the first non-empty bin is found

        # Find the upper fit range (last non-empty bin)
        for bin_upper in range(n_bins, n_bins // 2, -1):  # Search from the end towards the center
            if(Histo_To_Fit.GetBinContent(bin_upper) != 0):
                fit_range_upper = Histo_To_Fit.GetXaxis().GetBinUpEdge(bin_upper)
                break  # Stop the loop once the last non-empty bin is found
        
        
        Fitting_Function.SetRange(fit_range_lower, fit_range_upper)
        
        Fitting_Function.SetLineColor(2)
        if(Special in ["Normal"]):
            if(Method in ["rdf", "Experimental"]):
                Fitting_Function.SetLineColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Fitting_Function.SetLineColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Fitting_Function.SetLineColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Fitting_Function.SetLineColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Fitting_Function.SetLineColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian", "bay"]):
                Fitting_Function.SetLineColor(root_color.Teal)
            if(Method in ["SVD"]):
                Fitting_Function.SetLineColor(root_color.Pink)
        
        Allow_Multiple_Fits   = True
        Allow_Multiple_Fits_C = True

        try:
            if("Error" not in [A_Unfold, B_Unfold, C_Unfold]):
                # This is the constant scaling factor - A (should basically always be positive)
                Fitting_Function.SetParameter(0,      abs(A_Unfold))
                Fitting_Function.SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))

                if(Use_Higher_Terms):
                    try:
                        Fitting_Function.SetParameter(3, D_Unfold)
                        Fitting_Function.SetParLimits(3, D_Unfold - 5.5*abs(D_Unfold), D_Unfold + 5.5*abs(D_Unfold))
                    except:
                        print(f"{color.Error}Fitting_Function ERROR:\n{color.END}{str(traceback.format_exc())}\n")

                # if(((Special not in ["Normal"]) and isinstance(Special, list)) and (not Closure_Test)):
                if((Special not in ["Normal"]) and isinstance(Special, list)):
                    try:
                        Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
                        # print(f"Fitting_Phi_Function Special: Q2_y_Bin_Special, z_pT_Bin_Special = {Q2_y_Bin_Special}, {z_pT_Bin_Special}")
                        if(len(Special) > 2):
                            Sector_Special = str(Special[2])
                        else:
                            Sector_Special = "N/A"
                        if(str(z_pT_Bin_Special) in ["All", "0"]):
                            print(f"\n\n{color.BBLUE}z_pT_Bin_Special = {z_pT_Bin_Special}{color.END}\n\n\n")
                        if(str(z_pT_Bin_Special) in ["Integrated", "All", "-1", "0"]):
                            if(Sector_Special not in ["N/A"]):
                                if((Q2_y_Bin_Special, z_pT_Bin_Special, "Sectors", "Trusted") in special_fit_parameters_set):
                                    bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "Sectors", "Trusted")]
                                    print(f"\n{color.Error}Using Sector Fit Ranges\n{color.END}")
                                    fit_range_lower = bin_ranges.get("fit_range_lower")
                                    fit_range_upper = bin_ranges.get("fit_range_upper")
                                elif((Q2_y_Bin_Special, "All", "Sectors", "Trusted") in special_fit_parameters_set):
                                    bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, "All", "Sectors", "Trusted")]
                                    print(f"\n{color.Error}Using Sector Fit Ranges\n{color.END}")
                                    fit_range_lower = bin_ranges.get("fit_range_lower")
                                    fit_range_upper = bin_ranges.get("fit_range_upper")
                            elif((Q2_y_Bin_Special, z_pT_Bin_Special, "Trusted") in special_fit_parameters_set):
                                bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "Trusted")]
                                fit_range_lower = bin_ranges.get("fit_range_lower")
                                fit_range_upper = bin_ranges.get("fit_range_upper")
                            elif((Q2_y_Bin_Special, "All", "Trusted") in special_fit_parameters_set):
                                bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, "All", "Trusted")]
                                fit_range_lower = bin_ranges.get("fit_range_lower")
                                fit_range_upper = bin_ranges.get("fit_range_upper")
                            else:
                                fit_range_lower =  45 if(str(Q2_y_Bin_Special) in ["1", "5"]) else  30 if(str(Q2_y_Bin_Special) in ["2", "3", "6", "9", "10", "13", "16"]) else  15
                                fit_range_upper = 315 if(str(Q2_y_Bin_Special) in ["1", "5"]) else 330 if(str(Q2_y_Bin_Special) in ["2", "3", "6", "9", "10", "13", "16"]) else 345
                            Fitting_Function.SetRange(fit_range_lower, fit_range_upper)
                        if((z_pT_Bin_Special in ["Integrated", "-1"]) and not ((Q2_y_Bin_Special, z_pT_Bin_Special) in special_fit_parameters_set)):
                            if((Q2_y_Bin_Special, "All") in special_fit_parameters_set):
                                bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, "All")]
                                if(bin_settings.get("B_initial") is not None):
                                    Fitting_Function.SetParameter(1, bin_settings["B_initial"])
                                    if(bin_settings.get("B_limits")):
                                        Fitting_Function.SetParLimits(1, *sorted(bin_settings["B_limits"]))
                                if(bin_settings.get("C_initial") is not None):
                                    Fitting_Function.SetParameter(2, bin_settings["C_initial"])
                                    if(bin_settings.get("C_limits")):
                                        Fitting_Function.SetParLimits(2, *sorted(bin_settings["C_limits"]))
                                Allow_Multiple_Fits   = bin_settings.get("Allow_Multiple_Fits",   True)
                                Allow_Multiple_Fits_C = bin_settings.get("Allow_Multiple_Fits_C", True)
                            else:
                                Par_initial_B = -0.05 if(str(Q2_y_Bin_Special) in ["12"]) else -0.1   if(str(Q2_y_Bin_Special) in ["8", "15"]) else -0.12 if(str(Q2_y_Bin_Special) in ["4", "11", "17"]) else -0.14  if(str(Q2_y_Bin_Special) in ["7", "16"]) else -0.155 if(str(Q2_y_Bin_Special) in ["3",  "6", "13", "14"]) else -0.1625 if(str(Q2_y_Bin_Special) in ["12"]) else -0.174
                                Par_initial_C = -0.05 if(str(Q2_y_Bin_Special) in ["8"])  else -0.075 if(str(Q2_y_Bin_Special) in ["12"])      else -0.04 if(str(Q2_y_Bin_Special) in ["4", "15"])       else -0.029 if(str(Q2_y_Bin_Special) in ["11"])      else -0.021 if(str(Q2_y_Bin_Special) in ["7", "14", "16", "17"]) else -0.01   if(str(Q2_y_Bin_Special) in ["10"]) else -0.006 if(str(Q2_y_Bin_Special) in ["3", "6", "13"]) else 0.0045 if(str(Q2_y_Bin_Special) in ["2"]) else 0.0067 if(str(Q2_y_Bin_Special) in ["9"]) else 0.009
                                Par__range__B = [0.5*Par_initial_B, 1.5*Par_initial_B]
                                Par__range__C = [0.5*Par_initial_C, 1.5*Par_initial_C]
                                # Cos(phi) Moment - B
                                Fitting_Function.SetParameter(1, Par_initial_B)
                                Fitting_Function.SetParLimits(1, min(Par__range__B), max(Par__range__B))
                                # Cos(2*phi) Moment - C
                                Fitting_Function.SetParameter(2, Par_initial_C)
                                Fitting_Function.SetParLimits(2, min(Par__range__C), max(Par__range__C))
                        elif((Q2_y_Bin_Special, z_pT_Bin_Special) in special_fit_parameters_set):
                                bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special)]
                                if(bin_settings.get("B_initial") is not None):
                                    Fitting_Function.SetParameter(1, bin_settings["B_initial"])
                                    if(bin_settings.get("B_limits")):
                                        Fitting_Function.SetParLimits(1, *sorted(bin_settings["B_limits"]))
                                if(bin_settings.get("C_initial") is not None):
                                    Fitting_Function.SetParameter(2, bin_settings["C_initial"])
                                    if(bin_settings.get("C_limits")):
                                        Fitting_Function.SetParLimits(2, *sorted(bin_settings["C_limits"]))
                                Allow_Multiple_Fits   = bin_settings.get("Allow_Multiple_Fits",   True)
                                Allow_Multiple_Fits_C = bin_settings.get("Allow_Multiple_Fits_C", True)                        
                    except:
                        print(f"{color.Error}\nERROR in Fitting_Phi_Function() for 'Special' arguement...{color.END_B}\nTraceback:\n{str(traceback.format_exc())}{color.END}\n")
                else:
                    print(f"\n\n\n{color.RED}Fitting_Phi_Function Not Special{color.END}\n\n\n")
                Histo_To_Fit.Fit(Fitting_Function, "QRB")
            else:
                # print(f"{color.RED}Error in A_Unfold, B_Unfold, C_Unfold = {A_Unfold}, {B_Unfold}, {C_Unfold}{color.END}")
                Histo_To_Fit.Fit(Fitting_Function, "QR")

            A_Unfold = Fitting_Function.GetParameter(0)
            B_Unfold = Fitting_Function.GetParameter(1)
            C_Unfold = Fitting_Function.GetParameter(2)
            
            # Re-fitting with the new parameters
            # The constant scaling factor - A
            Fitting_Function.SetParameter(0,     abs(A_Unfold))
            Fitting_Function.SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
            
            if(Allow_Multiple_Fits): # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
            else:                    # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - Fitting_Function.GetParError(1), B_Unfold + Fitting_Function.GetParError(1))
                
            if(Allow_Multiple_Fits_C): # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))
            else:                      # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - Fitting_Function.GetParError(2), C_Unfold + Fitting_Function.GetParError(2))

            if(Use_Higher_Terms):
                D_Unfold = Fitting_Function.GetParameter(3)
                # Cos(3*phi) Moment - D
                Fitting_Function.SetParameter(3, D_Unfold)
                Fitting_Function.SetParLimits(3, D_Unfold - 0.5*abs(D_Unfold), D_Unfold + 0.5*abs(D_Unfold))

            # Re-Fitting the plots
            Histo_To_Fit.Fit(Fitting_Function, "QRB")

            A_Unfold       = Fitting_Function.GetParameter(0)
            B_Unfold       = Fitting_Function.GetParameter(1)
            C_Unfold       = Fitting_Function.GetParameter(2)

            A_Unfold_Error = Fitting_Function.GetParError(0)
            B_Unfold_Error = Fitting_Function.GetParError(1)
            C_Unfold_Error = Fitting_Function.GetParError(2)
            
            try:
                Fit_Chisquared = Fitting_Function.GetChisquare()
                Fit_ndf        = Fitting_Function.GetNDF()
            except:
                Fit_Chisquared = "Fit_Chisquared"
                Fit_ndf        = "Fit_ndf"

            Out_Put = [Histo_To_Fit,  Fitting_Function,   [Fit_Chisquared,    Fit_ndf],  [A_Unfold,    A_Unfold_Error],  [B_Unfold,    B_Unfold_Error],  [C_Unfold,    C_Unfold_Error]]
        except:
            print(f"{color.Error}ERROR IN FITTING:\n{color.END}{str(traceback.format_exc())}\n")
            Out_Put = [Histo_To_Fit, "Fitting_Function",  ["Fit_Chisquared", "Fit_ndf"], ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        return Out_Put
    else:
        print(f"\n\n\n{color.Error}ERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...\n\n\n{color.END}")
        return "ERROR"
    
################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##           Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def MultiD_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="Multi_Dim_Q2_y_Bin_phi_t", Smear="", Out_Option="Save", Fitting_Input="default", Q2_y_Bin_Select="All"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}
    if(str(Method) not in ["rdf", "gdf"]):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
        else:
            print(color.Error, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
    else:
        print(color.Error, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
        return "Error"
    try:
        Output_Histos = {}
        #############################################################################################
        #####==========#####     Catching Input Errors     #####==========###########################
        #############################################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("Combined_" not in str(Name) and "Multi_Dim" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName ={color.END} {Name}\nMultiD_Slice() should be used on 1D histograms with the 'Combined_' or 'Multi_Dim_' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t"]):
            print(f"{color.RED}ERROR in MultiD_Slice(): Not set up for other variables (yet){color.END}\nVariable ={Variable}\n\n")
            return "Error"

        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        #############################################################################################
        #####==========#####     Catching Input Errors     #####==========###########################
        #############################################################################################
        #####==========#####    Setting Histogram Title     #####==========##########################
        #############################################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["gdf", "gen", "MC GEN", "tdf", "true"]):
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not Sim_Test) else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        if(Title == "Default"):
            Title = str(Histo.GetTitle())
        elif(Title in ["norm", "standard"]):
            Title = "".join(["#splitline{", str(root_color.Bold), "{(Old) 3-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{Multi_Dim_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((Pass_Version not in [""]) and (Pass_Version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(Pass_Version), "}}"])
        #############################################################################################
        #####==========#####    Setting Histogram Title     #####==========##########################
        #############################################################################################
        
        #############################################################################################
        #####==========#####   Setting Variable Binning    #####==========###########################
        #############################################################################################
        ###=======================================================================================###
                               # ['min', 'max', 'num_bins', 'size']
        Q2_y_Binning           = [-0.5,  18.5,  19,          1]
        z_pT_Binning           = [-0.5,  37.5,  38,          1]
        if("Y_bin" not in str(Binning_Method)):
            z_pT_Binning       = [-0.5,  42.5,  43,          1]
        phi_h_Binning          = [0,     360,   24,         15]
        ###=======================================================================================###
        ###========###  Setting Q2-y Binning   ###================================================###
        NewDim_Bin_Min,     NewDim_Bin_Max, NewDim_Bin_Num, NewDim_Bin_Size = Q2_y_Binning
        Multi_Dim_Var       = "Q2_y"
        ###========###  Setting z-pT Binning   ###================================================###
        if("z_pT_Bin" in Variable):
            NewDim_Bin_Min, NewDim_Bin_Max, NewDim_Bin_Num, NewDim_Bin_Size = z_pT_Binning
            Multi_Dim_Var   = "z_pT"
        ###========###   Setting 4D Binning    ###================================================###
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            Q2_y_z_pT_4D_Binning = [-0.5, 506.5, 507, 1]
            NewDim_Bin_Min, NewDim_Bin_Max, NewDim_Bin_Num, NewDim_Bin_Size = Q2_y_z_pT_4D_Binning
            Multi_Dim_Var   = "Q2_y_z_pT"
        ###=======================================================================================###
        ###=======================================================================================###
        #############################################################################################
        #####==========#####   Setting Variable Binning    #####==========###########################
        #############################################################################################
        ###==============###========================================###==============################
        ###==============###   Creation of the Sliced Histograms    ###==============################
        ###==============###========================================###==============################
        #############################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="Multi-Dim Histo", Data_Type=str(Method), Cut_Type="Skip" if(all(cut_checks not in str(Name) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=str(Smear), Q2_y_Bin="Multi_Dim_Q2_y_Bin_Info", z_pT_Bin="Multi_Dim_z_pT_Bin_Info", Bin_Extra="Multi_Dim_Bin_Info" if(Multi_Dim_Var not in ["Q2_y", "z_pT"]) else "Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                Name = str(Name.replace("mdf", "tdf")).replace("gdf", "tdf")
        if(str(Multi_Dim_Var) in ["z_pT"]):
            Name = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All"))
        bin_ii = 1
        for NewDim_Bin in range(0, NewDim_Bin_Num - 1, 1):            
            if(str(Multi_Dim_Var) in ["Q2_xB", "Q2_y"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(NewDim_Bin))).replace("Multi_Dim_z_pT_Bin_Info", "All")
            elif(str(Multi_Dim_Var) in ["z_pT"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All")).replace("Multi_Dim_z_pT_Bin_Info", str(NewDim_Bin))
                z_pT_Bin_Range     = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Select)[1]
                if("Y_bin" not in Binning_Method):
                    z_pT_Bin_Range = 42 if(str(Q2_y_Bin_Select) in ["2"]) else 36 if(str(Q2_y_Bin_Select) in ["4", "5", "9", "10"]) else 35 if(str(Q2_y_Bin_Select) in ["1", "3"]) else 30 if(str(Q2_y_Bin_Select) in ["6", "7", "8", "11"]) else 25 if(str(Q2_y_Bin_Select) in ["13", "14"]) else 20 if(str(Q2_y_Bin_Select) in ["12", "15", "16", "17"]) else 1
                if(NewDim_Bin > z_pT_Bin_Range):
                    break
            else:
                Name_Out = str(Name.replace("Multi_Dim_Bin_Info",      str(NewDim_Bin)))
            if(str(Multi_Dim_Var) not in ["z_pT"]):
                Title_Out = str(Title.replace("Range: -1.5 #rightarrow 481.5 - Size: 1.0 per bin", "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))
                Title_Out = str(Title_Out.replace("Multi_Dim_Var_Info",                            "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))
            else:
                Title_Out = str(Title.replace("Range: -1.5 #rightarrow 481.5 - Size: 1.0 per bin", "".join(["#scale[1.1]{Q^{2}-y Bin ", str(Q2_y_Bin_Select), ": z-P_{T} Bin ", str(NewDim_Bin), "}"])))
                Title_Out = str(Title_Out.replace("Multi_Dim_Var_Info",                            "".join(["#scale[1.1]{Q^{2}-y Bin ", str(Q2_y_Bin_Select), ": z-P_{T} Bin ", str(NewDim_Bin), "}"])))
            if("(z_pT_Bin_0)" in str(Name_Out)):
                Name_Out = str(Name_Out).replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
                Name_All = Name_Out
            ######################################################################
            #####==========#####   Filling Sliced Histogram   #####==========#####
            ######################################################################
            Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
            ii_bin_num = 1
            for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                if(Histo_Cut is not False):
                    ii_bin_num += 1
                    bin_jj = Histo.FindBin(bin_ii)
                    Multi_Dim_cut_num = Histo_Cut.GetBinContent(bin_jj)
                    Multi_Dim_cut_err = Histo_Cut.GetBinError(bin_jj)
                    if((Multi_Dim_cut_num == 0) or (Multi_Dim_cut_num <= Multi_Dim_cut_err)):
                        Multi_Dim_phi_num = 0
                        Multi_Dim_phi_err = 0 # Histo.GetBinContent(bin_jj) + Histo.GetBinError(bin_jj)
                    else:
                        Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                        Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                    Output_Histos[Name_Out].Fill(                                                               phi_bin + 0.5*phi_h_Binning[3],   Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(                        phi_bin + 0.5*phi_h_Binning[3]),  Multi_Dim_phi_err)
                    if(NewDim_Bin not in [0]):
                        Multi_Dim_All_Err = Output_Histos[Name_All].GetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]))
                        Output_Histos[Name_All].Fill(                                                           phi_bin + 0.5*phi_h_Binning[3],   Multi_Dim_phi_num)
                        Output_Histos[Name_All].SetBinError(Output_Histos[Name_All].FindBin(                    phi_bin + 0.5*phi_h_Binning[3]), (Multi_Dim_All_Err**2 + Multi_Dim_phi_err**2)**0.5)
                    bin_ii += 1
                else:
                    ii_bin_num += 1
                    bin_jj = Histo.FindBin(bin_ii)
                    Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                    Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                    Output_Histos[Name_Out].Fill(                                                               phi_bin + 0.5*phi_h_Binning[3],   Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(                        phi_bin + 0.5*phi_h_Binning[3]),  Multi_Dim_phi_err)
                    if(NewDim_Bin not in [0]):
                        Multi_Dim_All_Err = Output_Histos[Name_All].GetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]))
                        Output_Histos[Name_All].Fill(                                                           phi_bin + 0.5*phi_h_Binning[3],   Multi_Dim_phi_num)
                        Output_Histos[Name_All].SetBinError(Output_Histos[Name_All].FindBin(                    phi_bin + 0.5*phi_h_Binning[3]), (Multi_Dim_All_Err**2 + Multi_Dim_phi_err**2)**0.5)
                    bin_ii += 1
            ######################################################################
            #####==========#####   Filling Sliced Histogram   #####==========#####
            ######################################################################
            #####==========#####   Drawing Histogram/Canvas   #####==========#####
            ######################################################################
            if(Method in ["rdf", "Experimental"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Blue)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Red)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Green)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Cyan)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Teal)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Teal)
            if(Method in ["Background"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Black)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Black)
            ######################################################################
            #####==========#####   Drawing Histogram/Canvas   #####==========#####
            ######################################################################
            Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            if(Fitting_Input in ["default", "Default"] and Fit_Test):
                Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("Multi-Dim Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[Q2_y_Bin_Select, NewDim_Bin] if(str(Multi_Dim_Var) in ["z_pT"]) else "Normal")
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
        #############################################################################################
        ###==============###========================================###==============################
        ###==============###   Creation of the Sliced Histograms    ###==============################
        ###==============###========================================###==============################
        #############################################################################################
        #####==========#####      Returning Outputs       #####==========############################
        #############################################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        #############################################################################################
        #####==========#####      Returning Outputs       #####==========############################
        #############################################################################################
    except:
        print(f"{color.Error}MultiD_Slice(...) ERROR:\n{color.END}{str(traceback.format_exc())}\n")
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##           Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##        3D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################

def Multi3D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_z_pT_Bin_Y_bin_phi_t", Smear="", Q2_y_Bin_Select="All", Out_Option="Save", Fitting_Input="default"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    if((str(Method) not in ["rdf", "gdf"]) or ((str(Method) not in ["gdf"]) and Sim_Test)):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
        else:
            print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
            return "Error"
    elif(Smear in [""]):
        print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
    else:
        print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
        return "Error"
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in str(Name)):
                print(color.RED, "ERROR: WRONG TYPE OF HISTOGRAM\nName =", color.END, Name, "\nMulti3D_Slice() should be used on the histograms with the 'MultiDim_z_pT_Bin_Y_bin_phi_t' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_z_pT_Bin_Y_bin_phi_t"]):
            print(color.RED, "ERROR in Multi3D_Slice(): Not set up for other variables (yet)", color.END, "\nVariable =", Variable, "\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue),  "]{(Experimental)}"       if(not Sim_Test)      else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{3-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_3D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((Pass_Version not in [""]) and (Pass_Version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(Pass_Version), "}}"])
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_3D_Histo", Data_Type=str(Method), Cut_Type="Skip" if(all(cut_checks not in str(Name) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=str(Smear), Q2_y_Bin=Q2_y_Bin_Select, z_pT_Bin="MultiDim_3D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                Name = str(Name.replace("mdf", "tdf")).replace("gdf", "tdf")
        if(str(Q2_y_Bin_Select) not in ["0", "All"]):
            if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT=1", End_Bins_Name="3D_Bins")):
                raise TypeError(f"Convert_All_Kinematic_Bins(Start_Bins_Name='Q2-y={Q2_y_Bin_Select}, z-pT=1', End_Bins_Name='3D_Bins') == ERROR")
            else:
                z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Select)[1]
                for z_pT in range(0, z_pT_Range+1):
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_Select, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin", Common_z_pT_Range_Q=Common_Int_Bins)):
                        continue
                    Name_Out  = str(Name.replace("MultiDim_3D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
                    Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                    Bin_Title = Bin_Title.replace("Common_Int", "Integrated (Over Common Range)")
                    Title_Out = str(Title.replace("MultiDim_3D_Var_Info", Bin_Title))
                    if(z_pT not in [0]):
                        if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT}", End_Bins_Name="3D_Bins")):
                            break
                        else:
                            Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT}",       End_Bins_Name="3D_Bins")
                            End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT+1}",     End_Bins_Name="3D_Bins")
                            if(End___phi_h_bin in ["ERROR"]):
                                End___phi_h_bin = Start_phi_h_bin + phi_h_Binning[2]
                            if(((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]) or skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_Select, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin", Common_z_pT_Range_Q=Common_Int_Bins)):
                                continue
                    else:
                        Name_All                = Name_Out
                        Output_Histos[Name_All] = ROOT.TH1D(Name_All, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                        continue
                    Output_Histos[Name_Out]     = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                    #######################################################################
                    #####==========#####   Filling Sliced Histogram    #####==========#####
                    #######################################################################
                    ii_bin_num = Start_phi_h_bin
                    phi_Content, phi___Error = {}, {}
                    for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                        phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                        phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
                    while(ii_bin_num < End___phi_h_bin):
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            if(Histo_Cut is not False):
                                bin_ii = Histo.FindBin(ii_bin_num + 1)
                                MultiDim_cut_num = Histo_Cut.GetBinContent(bin_ii)
                                MultiDim_cut_err = Histo_Cut.GetBinError(bin_ii)
                                if((MultiDim_cut_num == 0) or (MultiDim_cut_num <= MultiDim_cut_err)):
                                    phi_Content[phi_bin + 0.5*phi_h_Binning[3]] += 0
                                    phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0 # Histo.GetBinContent(bin_ii) + Histo.GetBinError(bin_ii)
                                else:
                                    phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                    phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                            else:
                                bin_ii = Histo.FindBin(ii_bin_num + 1)
                                phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                            ii_bin_num += 1
                    for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                        Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],             phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                        Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                        Current_All_Error = Output_Histos[Name_All].GetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]))
                        Output_Histos[Name_All].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],             phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                        Output_Histos[Name_All].SetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(Current_All_Error**2 + phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                    #######################################################################
                    #####==========#####   Filling Sliced Histogram    #####==========#####
                    #######################################################################
                    for name in [Name_All, Name_Out]:
                        if((name in [Name_All]) and (z_pT not in [z_pT_Range-3, z_pT_Range-2, z_pT_Range-1, z_pT_Range, z_pT_Range+1])):
                            continue # Do not have to set the integrated z-pT bin plot more than once at the end of the z_pT loop
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        Output_Histos[name].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[name].GetBinContent(Output_Histos[name].GetMaximumBin()))
                        if(Method in ["rdf", "Experimental"]):
                            Output_Histos[name].SetLineColor(root_color.Blue)
                            Output_Histos[name].SetMarkerColor(root_color.Blue)
                        if(Method in ["mdf", "MC REC"]):
                            Output_Histos[name].SetLineColor(root_color.Red)
                            Output_Histos[name].SetMarkerColor(root_color.Red)
                        if(Method in ["gdf", "gen", "MC GEN"]):
                            Output_Histos[name].SetLineColor(root_color.Green)
                            Output_Histos[name].SetMarkerColor(root_color.Green)
                        if(Method in ["tdf", "true"]):
                            Output_Histos[name].SetLineColor(root_color.Cyan)
                            Output_Histos[name].SetMarkerColor(root_color.Cyan)
                        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                            Output_Histos[name].SetLineColor(root_color.Brown)
                            Output_Histos[name].SetMarkerColor(root_color.Brown)
                        if(Method in ["bayes", "bayesian", "Bayesian"]):
                            Output_Histos[name].SetLineColor(root_color.Teal)
                            Output_Histos[name].SetMarkerColor(root_color.Teal)
                        if(Method in ["Background"]):
                            Output_Histos[name].SetLineColor(root_color.Black)
                            Output_Histos[name].SetMarkerColor(root_color.Black)
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
                        if(Fitting_Input in ["default", "Default"] and Fit_Test):
                            Output_Histos[name], Unfolded_Fit_Function[name.replace("MultiDim_3D_Histo", "Fit_Function")], Fit_Chisquared[name.replace("MultiDim_3D_Histo", "Chi_Squared")], Fit_Par_A[name.replace("MultiDim_3D_Histo", "Fit_Par_A")], Fit_Par_B[name.replace("MultiDim_3D_Histo", "Fit_Par_B")], Fit_Par_C[name.replace("MultiDim_3D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[name], Method=Method, Fitting="default", Special=[int(Q2_y_Bin_Select), int(z_pT)])
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################

        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    except:
        print("".join([color.Error, "Multi3D_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##        3D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Multi5D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="", Out_Option="Save", Fitting_Input="default"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    if(str(Method) not in ["rdf", "gdf"]):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(color.BLUE, "\nRunning Multi5D_Slice(...)\n", color.END)
        else:
            print(color.Error, "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE,      "\nRunning Multi5D_Slice(...)\n", color.END)
    else:
        print(color.Error,     "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
        return "Error"
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name)):
                print(color.RED, "ERROR: WRONG TYPE OF HISTOGRAM\nName =", color.END, Name, "\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_Q2_y_z_pT_phi_h"]):
            print(color.RED, "ERROR in Multi5D_Slice(): Not set up for other variables (yet)", color.END, "\nVariable =", Variable, "\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue),  "]{(Experimental)}"       if(not Sim_Test)      else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{5-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_5D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((Pass_Version not in [""]) and (Pass_Version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(Pass_Version), "}}"])
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip" if(all(cut_checks not in str(Name) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a MultiDim_5D Histo for 'True' distribution\n", color.END, "\nName =", str(Name), "\n"]))
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a MultiDim_5D Histo for '", str(Method), "' distribution\n", color.END, "\nName =", str(Name), "\n"]))
        for Q2_y in Q2_xB_Bin_List:
            if(Q2_y not in ["0", "All"]):
                if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                    break
                else:
                    z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
                    for z_pT in range(0, z_pT_Range+1):
                        Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y) if(str(Q2_y) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                        Title_Out = str(Title.replace("MultiDim_5D_Var_Info", Bin_Title))
                        if(z_pT not in [0]):
                            if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                                break
                            else:
                                Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}",       End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT+1}",     End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if(End___phi_h_bin in ["ERROR"]):
                                    End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if(((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]) or skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin")):
                                    continue
                        else:
                            Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1",                End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                            End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1",         End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                        Name_Out = str(Name.replace("MultiDim_5D_Q2_y_Bin_Info",     str(Q2_y) if(str(Q2_y) not in ["0", "All"]) else "All"))
                        Name_Out = str(Name_Out.replace("MultiDim_5D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
                        Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                        # print(f"Making Output_Histos[{Name_Out}]...\n\tlen(Output_Histos[Name_Out]) = ", str(len(Output_Histos[Name_Out])))
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        ii_bin_num,  ii_LastNum  = Start_phi_h_bin, Start_phi_h_bin
                        phi_Content, phi___Error = {}, {}
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
                        while(ii_bin_num < End___phi_h_bin):
                            OverFlow_Con = False
                            if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
                                # Conditions for combining all z-pT bins
                                Q2_y_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="Q2-y") if(ii_bin_num != 0) else 1
                                Q2_y_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="Q2-y")
                                z_pT_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="z-pT") if(ii_bin_num != 0) else 1
                                z_pT_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="z-pT")
                                if((z_pT_bin_0 != z_pT_bin_1) and (Q2_y_bin_0 == Q2_y_bin_1)):
                                    if(ii_LastNum + 1 == ii_bin_num):
                                        OverFlow_Con = True
                                    ii_LastNum = ii_bin_num
                                elif(Q2_y_bin_0 != Q2_y_bin_1):
                                    ii_LastNum = Start_phi_h_bin
                                elif(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_bin_1, Z_PT_BIN=z_pT_bin_1, BINNING_METHOD="Y_bin")):
                                    OverFlow_Con = True
                                    ii_LastNum = ii_bin_num
                            if(OverFlow_Con):
                                ii_bin_num += 1
                                continue
                            else:
                                for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                                    if(Histo_Cut is not False):
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        MultiDim_cut_num = Histo_Cut.GetBinContent(bin_ii)
                                        MultiDim_cut_err = Histo_Cut.GetBinError(bin_ii)
                                        if((MultiDim_cut_num == 0) or (MultiDim_cut_num <= MultiDim_cut_err)):
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] += 0
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0 # Histo.GetBinContent(bin_ii) + Histo.GetBinError(bin_ii)
                                        else:
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                                    else:
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                        phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],            phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                            Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
                        if(Method in ["rdf", "Experimental"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Blue)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Blue)
                        if(Method in ["mdf", "MC REC"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Red)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Red)
                        if(Method in ["gdf", "gen", "MC GEN"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Green)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Green)
                        if(Method in ["tdf", "true"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Cyan)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Cyan)
                        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
                        if(Method in ["bayes", "bayesian", "Bayesian"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Teal)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Teal)
                        if(Method in ["Background"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Black)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Black)
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
                        if(Fitting_Input in ["default", "Default"] and Fit_Test):
                            Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("MultiDim_5D_Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("MultiDim_5D_Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[int(Q2_y), int(z_pT)])
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
            # else:
            #     # Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{All Binned Events}}}"])
            #     # Title_Out = str(Title.replace("MultiDim_5D_Var_Info", Bin_Title))
            #     print(f"{color.Error}\n\n\nError while running Multi5D_Slice(...):\n\tDo NOT run for Q2-y Bin = 'All'{color.END_R}\n\t(Plot is currently considered not important enough to warrent the effort to create){color.END}\n\n\n")
            #     return "Error"
            
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    except:
        print("".join([color.Error, "Multi5D_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Rebuild_Matrix_5D(List_of_Sliced_Histos, Standard_Name, Increment=4, Title="Default"):
    Num__Bins, Min_Range, Max_Range = Find_Bins_From_Histo_Name(Standard_Name)
    Slicing_Name = f"{Standard_Name}_Slice_SLICE-NUM_(Increment='{Increment}')"
    # print(f"Slicing_Name = {Slicing_Name}")
    print("\nRunning Rebuild_Matrix_5D(...)")
    Num_Slices   = int(Num__Bins/Increment)
    for test in ["1", str(Num_Slices)]:
        if(Slicing_Name.replace("SLICE-NUM", str(test)) not in List_of_Sliced_Histos):
            missing_name = Slicing_Name.replace("SLICE-NUM", str(test))
            print(f"{color.Error}ERROR IN Rebuild_Matrix_5D(...): {color.END_R}'Slicing_Name' is missing from 'List_of_Sliced_Histos'{color.END_B}\n\tSlicing_Name = {missing_name}\n\tList_of_Sliced_Histos = {List_of_Sliced_Histos}")
            return "ERROR"
    Histo_Title = Title if(Title not in ["Default"]) else "".join([str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetXaxis().GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetYaxis().GetTitle())])
    Rebuilt_5D_Matrix = ROOT.TH2D(str(Standard_Name), str(Histo_Title), Num__Bins, Min_Range, Max_Range, Num__Bins, Min_Range, Max_Range)
    X_Bin_5D = 0
    for slice_num in range(1, Num_Slices + 1):
        Histo_Add     = List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", str(slice_num))]
        X_Bin_5D     += -1
        for     x_bin in range(0, Histo_Add.GetNbinsX() + 1):
            X_Bin_5D +=  1
            for y_bin in range(0, Histo_Add.GetNbinsY() + 1):                
                bin_content = Histo_Add.GetBinContent(x_bin, y_bin)
                bin_error   = Histo_Add.GetBinError(x_bin,   y_bin)
                for ii in range(1, int(bin_content)+1):
                    Rebuilt_5D_Matrix.Fill(X_Bin_5D-1, y_bin-1)
    print("Finished running Rebuild_Matrix_5D(...)\n")
    return Rebuilt_5D_Matrix

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def New_Version_of_File_Creation(Histogram_List_All, Out_Print_Main, Response_2D="", ExREAL_1D="", MC_REC_1D="", MC_GEN_1D="", ExTRUE_1D="N/A", Smear_Input="", Q2_Y_Bin="All", Z_PT_Bin="All", MC_BGS_1D="None"):
    try:
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################
        if("Response" not in str(Out_Print_Main) and (Response_2D not in ["N/A", "None", "Error"])):
            print(color.Error, "\n\n\nERROR IN New_Version_of_File_Creation()...\nThis function is meant to just handle the 'Response_Matrix' Histograms (for Unfolding)\nFlawed Input was:", str(Out_Print_Main), color.END, "\n\n")
            return Histogram_List_All
        if(type(Histogram_List_All) is not dict):
            print(color.Error, "\n\n\nERROR IN New_Version_of_File_Creation()...\nThis function requires that 'Histogram_List_All' be set as a dict to properly handle the outputs\nFlawed Input was:\nHistogram_List_All =", str(Histogram_List_All), color.END, "\n\n")
            return Histogram_List_All
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################

        Variable_Input = Histogram_Name_Def(Out_Print_Main, Variable="FindAll")
        print("Variable_Input =", Variable_Input)
        Allow_Fitting  = ("phi_t" in str(Variable_Input)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input))

        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        try:
            Bin_Method_Histograms        = Unfold_Function(Response_2D,  ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D)
            Bin_Unfolded, Bin_Acceptance = Bin_Method_Histograms
        except:
            print("".join([color.Error, "ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n", color.END_R, str(traceback.format_exc()), color.END]))

        if(("sec" not in Variable_Input) or (Response_2D not in ["N/A", "None", "Error"])):
            try:
                if("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input)):
                    # Temporary restriction on 5D unfolding as method is being tested for computational requirements (copy this line to see other restriction)
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D))[0]
                else:
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes", MC_BGS_1D=MC_BGS_1D))[0]
            except:
                print("".join([color.Error, "ERROR IN RooUnfold Bayesian METHOD:\n",           color.END_R, str(traceback.format_exc()), color.END]))
        else:
            print(f"\n{color.Error}Not running bayesian unfolding method...{color.END}\n")
            RooUnfolded_Bayes_Histos = Bin_Method_Histograms[0]

        # if("Multi_Dim" not in str(Variable_Input)):
        #     try:
        #         RooUnfolded_SVD_Histos   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd",   MC_BGS_1D=MC_BGS_1D))[0]
        #     except:
        #         print("".join([color.Error, "ERROR IN RooUnfold SVD METHOD:\n",                    color.END_R, str(traceback.format_exc()), color.END]))

        # try:
        #     RooUnfolded_BinByBin_Histos  = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bbb", MC_BGS_1D=MC_BGS_1D))[0]
        # except:
        #     print("".join([color.Error, "ERROR IN RooUnfold Bin-by-Bin METHOD:\n",             color.END_R, str(traceback.format_exc()), color.END]))
        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################

        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========##### (3D) Multi_Dim Histos (Old) #####==========#####
        if(("Multi_Dim" in str(Variable_Input))   and (Z_PT_Bin in ["All", "Integrated", "Common_Int", -2, -1, 0])):
            # Only the Multi_Dim z-pT Plots should be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All" or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###        
                # Multi_Dim_ExREAL_1D                                                                                                  = MultiD_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf" if(not Sim_Test) else "mdf", Variable=Variable_Input, Smear=Smear_Input if(Sim_Test) else "", Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_ExREAL_1D                                                                                                  = MultiD_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf",           Variable=Variable_Input, Smear=Smear_Input if(Sim_Test) else "", Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_MC_REC_1D                                                                                                  = MultiD_Slice(Histo=MC_REC_1D,                             Title="norm", Name=Out_Print_Main, Method="mdf",           Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(Fit_Test and Allow_Fitting):
                    Multi_Dim_MC_GEN_1D,     Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = MultiD_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                else:
                    Multi_Dim_MC_GEN_1D                                                                                              = MultiD_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(MC_BGS_1D not in ["None"]):
                    Multi_Dim_MC_BGS_1D                                                                                              = MultiD_Slice(Histo=MC_BGS_1D,                             Title="norm", Name=Out_Print_Main, Method="Background",    Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(ExTRUE_1D not in ["N/A"]):
                    if(Fit_Test and Allow_Fitting):
                        Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = MultiD_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                    else:
                        Multi_Dim_ExTRUE_1D                                                                                          = MultiD_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
                # Multi_Dim_Bin_Histo,         Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = MultiD_Slice(Histo=Bin_Unfolded,                          Title="norm", Name=Out_Print_Main, Method="Bin-by-bin", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                Multi_Dim_Bin_Acceptance                                                                                             = MultiD_Slice(Histo=Bin_Acceptance,                        Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(Fit_Test and Allow_Fitting):
                    Multi_Dim_Bin_Histo,     Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = MultiD_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                    Multi_Dim_Bay_Histo,     Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = MultiD_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                else:
                    Multi_Dim_Bin_Histo                                                                                              = MultiD_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                    Multi_Dim_Bay_Histo                                                                                              = MultiD_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
        #####==========##### (3D) MultiDim Histos (New)  #####==========#####
        elif(("MultiDim_z_pT_Bin" in str(Variable_Input)) and (Z_PT_Bin in ["All", "Integrated", "Common_Int", -2, -1, 0])):
            # The MultiDim_z_pT_Bin z-pT Plots should only be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All", "Integrated", -1 or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###        
                Multi_Dim_ExREAL_1D                                                                                                  = Multi3D_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf",           Variable=Variable_Input, Smear=Smear_Input if(Sim_Test) else "", Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_MC_REC_1D                                                                                                  = Multi3D_Slice(Histo=MC_REC_1D,                             Title="norm", Name=Out_Print_Main, Method="mdf",           Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(Fit_Test and Allow_Fitting):
                    Multi_Dim_MC_GEN_1D,     Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Multi3D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                else:
                    Multi_Dim_MC_GEN_1D                                                                                              = Multi3D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(MC_BGS_1D not in ["None"]):
                    Multi_Dim_MC_BGS_1D                                                                                              = Multi3D_Slice(Histo=MC_BGS_1D,                             Title="norm", Name=Out_Print_Main, Method="Background",    Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(ExTRUE_1D not in ["N/A"]):
                    if(Fit_Test and Allow_Fitting):
                        Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Multi3D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                    else:
                        Multi_Dim_ExTRUE_1D                                                                                          = Multi3D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
                Multi_Dim_Bin_Acceptance                                                                                             = Multi3D_Slice(Histo=Bin_Acceptance,                        Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                if(Fit_Test and Allow_Fitting):
                    Multi_Dim_Bin_Histo,     Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Multi3D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                    Multi_Dim_Bay_Histo,     Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Multi3D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                else:
                    Multi_Dim_Bin_Histo                                                                                              = Multi3D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                    Multi_Dim_Bay_Histo                                                                                              = Multi3D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
        #####==========#####   (5D) MultiDim Histos      #####==========#####
        elif(("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input)) and (Z_PT_Bin in ["All", "Integrated", "Common_Int", -2, -1, 0]) and (Q2_Y_Bin in ["All", 0])):
            # The 5D MultiDim Histograms should only be able to run if Q2_Y_Bin and Z_PT_Bin are equal to "All", "Integrated", -1 or 0 (all kinematic binning is done through these slices)
            ###=============================================###
            ###========###   Before Unfolding    ###========###
            ###=============================================###
            Multi_Dim_ExREAL_1D                                                                                                  = Multi5D_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf",        Variable=Variable_Input, Smear=Smear_Input if(Sim_Test) else "", Out_Option="Histos",   Fitting_Input="Off")[0]
            Multi_Dim_MC_REC_1D                                                                                                  = Multi5D_Slice(Histo=MC_REC_1D,                             Title="norm", Name=Out_Print_Main, Method="mdf",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off")[0]
            if(Fit_Test and Allow_Fitting):
                Multi_Dim_MC_GEN_1D,     Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Multi5D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",        Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default")
            else:
                Multi_Dim_MC_GEN_1D                                                                                              = Multi5D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",        Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off")[0]
            if(MC_BGS_1D not in ["None"]):
                Multi_Dim_MC_BGS_1D                                                                                              = Multi5D_Slice(Histo=MC_BGS_1D,                             Title="norm", Name=Out_Print_Main, Method="Background", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off")[0]
            if(ExTRUE_1D not in ["N/A"]):
                if(Fit_Test and Allow_Fitting):
                    Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Multi5D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",        Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default")
                else:
                    Multi_Dim_ExTRUE_1D                                                                                          = Multi5D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",        Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off")[0]
            ###=============================================###
            ###========###   Before Unfolding    ###========###
            ###=============================================###
            ###========###   After Unfolding     ###========###
            ###=============================================###
            Multi_Dim_Bin_Acceptance                                                                                             = Multi5D_Slice(Histo=Bin_Acceptance,                        Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off")[0]
            if(Fit_Test and Allow_Fitting):
                Multi_Dim_Bin_Histo,     Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Multi5D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default")
                Multi_Dim_Bay_Histo,     Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Multi5D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default")
            else:
                Multi_Dim_Bin_Histo                                                                                              = Multi5D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off")[0]
                Multi_Dim_Bay_Histo                                                                                              = Multi5D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off")[0]
            ###=============================================###
            ###========###   After Unfolding     ###========###
            ###=============================================###
        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========#####      Fitting 1D Histo       #####==========#####
        elif("phi" in Variable_Input):
            if(Fit_Test and Allow_Fitting):
                MC_GEN_1D,                   Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=MC_GEN_1D,                Method="gdf",   Special=[Q2_Y_Bin, Z_PT_Bin])
                Bin_Unfolded,                Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Bin_Unfolded,             Method="bbb",   Special=[Q2_Y_Bin, Z_PT_Bin])
                RooUnfolded_Bayes_Histos,    Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_Bayes_Histos, Method="bayes", Special=[Q2_Y_Bin, Z_PT_Bin])
                # if("Multi_Dim" not in str(Variable_Input)):
                #     RooUnfolded_SVD_Histos,  Unfolded_SVD_Fit_Function, Chi_Squared_SVD, SVD_Fit_Par_A, SVD_Fit_Par_B, SVD_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_SVD_Histos,   Method="SVD",   Special=[Q2_Y_Bin, Z_PT_Bin])
                if(ExTRUE_1D not in ["N/A"]):
                    ExTRUE_1D,               Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=ExTRUE_1D,                Method="tdf",   Special=[Q2_Y_Bin, Z_PT_Bin])
        #####==========#####      Fitting 1D Histo       #####==========#####


        ##################################################################################
        ###==============###==========================================###==============###
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ###==============###==========================================###==============###
        ##################################################################################
        Histo_Name_General = Histogram_Name_Def(out_print=Out_Print_Main, Histo_General="1D", Data_Type="METHOD", Cut_Type="Skip" if(all(cut_checks not in str(Out_Print_Main) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=Smear_Input, Q2_y_Bin=Q2_Y_Bin, z_pT_Bin=Z_PT_Bin, Bin_Extra="Default", Variable=Variable_Input)
        if("cut_Complete_SIDIS_Proton" in str(Histo_Name_General)):
            print(f"\n\n\n{color.Error}'cut_Complete_SIDIS_Proton' is still in 'Histo_Name_General' ({Histo_Name_General}){color.END}\n\n")
            Histo_Name_General = str(Histo_Name_General.replace("cut_Complete_SIDIS_Proton", "Proton"))
        if("sec'-[" in Out_Print_Main):
            Histo_Name_General = Histo_Name_General.replace("((", "(")
            for sec in [1, 2, 3, 4, 5, 6]:
                if(f"sec'-[{sec}]" in Out_Print_Main):
                    Histo_Name_General = Histo_Name_General.replace("sec)_(phi_t))", f"sec_{sec})_(phi_t)")
                    break
        if("sec_smeared'-[" in Out_Print_Main):
            Histo_Name_General = Histo_Name_General.replace("((", "(")
            for sec in [1, 2, 3, 4, 5, 6]:
                if(f"sec_smeared'-[{sec}]" in Out_Print_Main):
                    # print(f"\nBefore: Histo_Name_General = {Histo_Name_General}")
                    Histo_Name_General = Histo_Name_General.replace("sec_smeared)_(phi_t_smeared))", f"sec_{sec})_(phi_t)")
                    # print(f"After:  Histo_Name_General = {Histo_Name_General}\n")
                    break
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "rdf")).replace("Smear", "''")]               = ExREAL_1D.Clone(str(Histo_Name_General.replace("METHOD",   "rdf")).replace("Smear", "''"))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf"))]                                      = MC_REC_1D.Clone(str(Histo_Name_General.replace("METHOD",   "mdf")))
        if(hasattr(Response_2D, 'Clone') and callable(getattr(Response_2D, 'Clone'))):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")] = Response_2D.Clone(str(Histo_Name_General.replace("METHOD", "mdf")).replace("1D",    "Response_Matrix"))
        else:
            Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")] = Response_2D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "gdf")).replace("Smear", "''")]               = MC_GEN_1D.Clone(str(Histo_Name_General.replace("METHOD",   "gdf")).replace("Smear", "''"))
        if(MC_BGS_1D not in ["None"]):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Background"))]                               = MC_BGS_1D.Clone(str(Histo_Name_General.replace("METHOD",   "Background")))
            # print(f"""Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Background"))] -> {str(Histo_Name_General.replace("METHOD", "Background"))}""")
            # print(f"""     MC_BGS_1D                                                              -> {str(MC_BGS_1D.GetName())}""")
            # print(f"""     MC_REC_1D                                                              -> {str(MC_REC_1D.GetName())}""")

        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin"))]                                      = Bin_Unfolded.Clone(str(Histo_Name_General.replace("METHOD",             "Bin")))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Acceptance"))]                               = Bin_Acceptance.Clone(str(Histo_Name_General.replace("METHOD",           "Acceptance")))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian"))]                                 = RooUnfolded_Bayes_Histos.Clone(str(Histo_Name_General.replace("METHOD", "Bayesian")))
        # if("Multi_Dim" not in str(Variable_Input)):
        #     Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD"))]                                   = RooUnfolded_SVD_Histos
        #     if(Fit_Test and Allow_Fitting):
        #         Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Function")] = Unfolded_SVD_Fit_Function
        #         Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Chi_Squared")]  = Chi_Squared_SVD
        #         Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_A")]    = SVD_Fit_Par_A
        #         Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_B")]    = SVD_Fit_Par_B
        #         Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_C")]    = SVD_Fit_Par_C
        if(ExTRUE_1D not in ["N/A"]):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf"))]                                   = ExTRUE_1D.Clone(str(Histo_Name_General.replace("METHOD", "tdf")))
            if((Fit_Test and Allow_Fitting) and (not (("Multi" in str(Variable_Input)) and (Z_PT_Bin in ["All", 0])))):
                # print(f"\nHisto_Name_General = {Histo_Name_General}\nUnfolded_TDF_Fit_Function = {Unfolded_TDF_Fit_Function}\n")
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function")] = Unfolded_TDF_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Chi_Squared")]  = Chi_Squared_TDF # .Clone(str(Histo_Name_General.replace("METHOD",           "tdf")).replace("1D", "Chi_Squared"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_A")]    = TDF_Fit_Par_A # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_A"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_B")]    = TDF_Fit_Par_B # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_B"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_C")]    = TDF_Fit_Par_C # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_C"))
                
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Multi-Dim Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        # if(("Multi_Dim" in str(Variable_Input))   and (Z_PT_Bin in ["All", 0])):
        if(("Multi" in str(Variable_Input)) and (Z_PT_Bin in ["All", 0])):
            # Only the Multi_Dim z-pT Plots should be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All" or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                if(ExTRUE_1D not in ["N/A"]):
                    if(Fit_Test and Allow_Fitting):
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C, Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C, Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C, Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C]
                    else:
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D,                                                                                          Multi_Dim_Bin_Histo,                                                                                          Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo,                                                                                          Multi_Dim_ExTRUE_1D]
                else:
                    if(Fit_Test and Allow_Fitting):
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C, Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C, Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C]
                    else:
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D,                                                                                          Multi_Dim_Bin_Histo,                                                                                          Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo]
                if(MC_BGS_1D not in ["None"]):
                    histos_list_loop.append(Multi_Dim_MC_BGS_1D)

                try:
                    for histos_list in histos_list_loop:
                        try:
                            for name in histos_list:
                                Histogram_List_All[name] = histos_list[name]
                        except:
                            print(f"{color.Error}ERROR IN ADDING TO Histogram_List_All (while looping within an item in histos_list):\n{color.END_R}{traceback.format_exc()}{color.END}")
                            print("histos_list =", histos_list)
                            # print("histos_list_loop =", histos_list_loop)
                except:
                    print(f"{color.Error}ERROR IN ADDING TO Histogram_List_All (while looping through items in histos_list):\n{color.END_R}{traceback.format_exc()}{color.END}")
        ###==========###         Multi_Dim Histos          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        elif("phi" in Variable_Input):
            if(Fit_Test and Allow_Fitting):
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")).replace("Smear", "''")] = Unfolded_GEN_Fit_Function.Clone(str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")).replace("Smear", "''"))
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Chi_Squared")).replace("Smear",  "''")] = Chi_Squared_GEN
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_A")).replace("Smear",    "''")] = GEN_Fit_Par_A
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_B")).replace("Smear",    "''")] = GEN_Fit_Par_B
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_C")).replace("Smear",    "''")] = GEN_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Function")]                         = Unfolded_Bin_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Chi_Squared")]                          = Chi_Squared_Bin
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_A")]                            = Bin_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_B")]                            = Bin_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_C")]                            = Bin_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Function")]                         = Unfolded_Bay_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Chi_Squared")]                          = Chi_Squared_Bay
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_A")]                            = Bay_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_B")]                            = Bay_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_C")]                            = Bay_Fit_Par_C
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ##################################################################################
        ###==============###==========================================###==============###
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ###==============###==========================================###==============###
        ##################################################################################
        
        return Histogram_List_All
        
    except:
        print(f"{color.Error}ERROR IN New_Version_of_File_Creation(...):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
        return Histogram_List_All
    
################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################





##################################################################################################################################################################
##==========##==========## Function for Creating the Integrated z-pT Bin Histograms     ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################
# # Run the following code whenever changes are made to the z-pT bins in order to get the correct (new) values for 'Area_of_z_pT_Bins'
# Area_of_z_pT_Bins = {}
# for Q2_y_Bin     in range(1, 18):
#     Area_of_z_pT_Bins[f"{Q2_y_Bin}"] = 0
#     for z_pT_Bin in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin)[0]):
#         if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
#             continue
#         else:
#             z_Max, z_Min, pTMax, pTMin = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT_Bin, Q2_y_Bin_Num=Q2_y_Bin)
#             Area_of_z_pT_Bins[f"{Q2_y_Bin}"]           +=       abs((z_Max - z_Min)*(pTMax - pTMin))
#             Area_of_z_pT_Bins[f"{Q2_y_Bin}_{z_pT_Bin}"] = round(abs((z_Max - z_Min)*(pTMax - pTMin)), 6)
#     Area_of_z_pT_Bins[f"{Q2_y_Bin}"] = round(Area_of_z_pT_Bins[f"{Q2_y_Bin}"], 6)
# print(f"Area_of_z_pT_Bins = {Area_of_z_pT_Bins}")




Area_of_z_pT_Bins = {'1': 0.4741, '1_1': 0.0527, '1_2': 0.031, '1_3': 0.031, '1_4': 0.031, '1_5': 0.0341, '1_6': 0.0372, '1_7': 0.0744, '1_8': 0.0187, '1_9': 0.011, '1_10': 0.011, '1_11': 0.011, '1_12': 0.0121, '1_13': 0.0132, '1_14': 0.0264, '1_15': 0.0102, '1_16': 0.006, '1_17': 0.006, '1_18': 0.006, '1_19': 0.0066, '1_20': 0.0072, '1_22': 0.0068, '1_23': 0.004, '1_24': 0.004, '1_25': 0.004, '1_26': 0.0044, '1_29': 0.0051, '1_30': 0.003, '1_31': 0.003, '1_32': 0.003, '2': 0.4564, '2_1': 0.05, '2_2': 0.025, '2_3': 0.025, '2_4': 0.0225, '2_5': 0.0325, '2_6': 0.065, '2_7': 0.024, '2_8': 0.012, '2_9': 0.012, '2_10': 0.0108, '2_11': 0.0156, '2_12': 0.0312, '2_13': 0.014, '2_14': 0.007, '2_15': 0.007, '2_16': 0.0063, '2_17': 0.0091, '2_18': 0.0182, '2_19': 0.01, '2_20': 0.005, '2_21': 0.005, '2_22': 0.0045, '2_23': 0.0065, '2_25': 0.006, '2_26': 0.003, '2_27': 0.003, '2_28': 0.0027, '2_29': 0.0039, '2_31': 0.008, '2_32': 0.004, '2_33': 0.004, '2_34': 0.0036, '3': 0.3661, '3_1': 0.0285, '3_2': 0.019, '3_3': 0.0171, '3_4': 0.019, '3_5': 0.019, '3_6': 0.0323, '3_7': 0.0225, '3_8': 0.015, '3_9': 0.0135, '3_10': 0.015, '3_11': 0.015, '3_12': 0.0255, '3_13': 0.012, '3_14': 0.008, '3_15': 0.0072, '3_16': 0.008, '3_17': 0.008, '3_18': 0.0136, '3_19': 0.0075, '3_20': 0.005, '3_21': 0.0045, '3_22': 0.005, '3_23': 0.005, '3_24': 0.0085, '3_25': 0.009, '3_26': 0.006, '3_27': 0.0054, '3_28': 0.006, '3_29': 0.006, '4': 0.3024, '4_1': 0.018, '4_2': 0.0108, '4_3': 0.0108, '4_4': 0.012, '4_5': 0.0156, '4_7': 0.0135, '4_8': 0.0081, '4_9': 0.0081, '4_10': 0.009, '4_11': 0.0117, '4_12': 0.0216, '4_13': 0.0105, '4_14': 0.0063, '4_15': 0.0063, '4_16': 0.007, '4_17': 0.0091, '4_18': 0.0168, '4_19': 0.0075, '4_20': 0.0045, '4_21': 0.0045, '4_22': 0.005, '4_23': 0.0065, '4_24': 0.012, '4_25': 0.0075, '4_26': 0.0045, '4_27': 0.0045, '4_28': 0.005, '4_29': 0.0065, '4_31': 0.0105, '4_32': 0.0063, '4_33': 0.0063, '4_34': 0.007, '4_35': 0.0091, '5': 0.469, '5_1': 0.0391, '5_2': 0.023, '5_3': 0.0207, '5_4': 0.023, '5_5': 0.0322, '5_6': 0.0759, '5_7': 0.0187, '5_8': 0.011, '5_9': 0.0099, '5_10': 0.011, '5_11': 0.0154, '5_12': 0.0363, '5_13': 0.0136, '5_14': 0.008, '5_15': 0.0072, '5_16': 0.008, '5_17': 0.0112, '5_18': 0.0264, '5_19': 0.0102, '5_20': 0.006, '5_21': 0.0054, '5_22': 0.006, '5_23': 0.0084, '5_25': 0.0068, '5_26': 0.004, '5_27': 0.0036, '5_28': 0.004, '5_29': 0.0056, '5_31': 0.0068, '5_32': 0.004, '5_33': 0.0036, '5_34': 0.004, '6': 0.4465, '6_1': 0.0459, '6_2': 0.027, '6_3': 0.0243, '6_4': 0.027, '6_5': 0.0378, '6_6': 0.0945, '6_7': 0.017, '6_8': 0.01, '6_9': 0.009, '6_10': 0.01, '6_11': 0.014, '6_12': 0.035, '6_13': 0.0119, '6_14': 0.007, '6_15': 0.0063, '6_16': 0.007, '6_17': 0.0098, '6_19': 0.0085, '6_20': 0.005, '6_21': 0.0045, '6_22': 0.005, '6_23': 0.007, '6_25': 0.0085, '6_26': 0.005, '6_27': 0.0045, '6_28': 0.005, '7': 0.3646, '7_1': 0.0285, '7_2': 0.0171, '7_3': 0.0171, '7_4': 0.019, '7_5': 0.0228, '7_7': 0.0195, '7_8': 0.0117, '7_9': 0.0117, '7_10': 0.013, '7_11': 0.0156, '7_12': 0.0299, '7_13': 0.012, '7_14': 0.0072, '7_15': 0.0072, '7_16': 0.008, '7_17': 0.0096, '7_18': 0.0184, '7_19': 0.009, '7_20': 0.0054, '7_21': 0.0054, '7_22': 0.006, '7_23': 0.0072, '7_24': 0.0138, '7_25': 0.006, '7_26': 0.0036, '7_27': 0.0036, '7_28': 0.004, '7_29': 0.0048, '7_31': 0.0075, '7_32': 0.0045, '7_33': 0.0045, '7_34': 0.005, '7_35': 0.006, '8': 0.2281, '8_1': 0.021, '8_2': 0.0126, '8_3': 0.0112, '8_4': 0.0126, '8_5': 0.0196, '8_6': 0.0105, '8_7': 0.0063, '8_8': 0.0056, '8_9': 0.0063, '8_10': 0.0098, '8_11': 0.0075, '8_12': 0.0045, '8_13': 0.004, '8_14': 0.0045, '8_15': 0.007, '8_16': 0.0075, '8_17': 0.0045, '8_18': 0.004, '8_19': 0.0045, '8_20': 0.007, '8_21': 0.0045, '8_22': 0.0027, '8_23': 0.0024, '8_24': 0.0027, '8_25': 0.0042, '8_26': 0.0045, '8_27': 0.0027, '8_28': 0.0024, '8_29': 0.0027, '8_30': 0.0042, '8_31': 0.009, '8_32': 0.0054, '8_33': 0.0048, '8_34': 0.0054, '9': 0.439, '9_1': 0.0476, '9_2': 0.0224, '9_3': 0.0224, '9_4': 0.0224, '9_5': 0.0336, '9_6': 0.0448, '9_7': 0.0588, '9_8': 0.0204, '9_9': 0.0096, '9_10': 0.0096, '9_11': 0.0096, '9_12': 0.0144, '9_13': 0.0192, '9_14': 0.0252, '9_15': 0.0102, '9_16': 0.0048, '9_17': 0.0048, '9_18': 0.0048, '9_19': 0.0072, '9_20': 0.0096, '9_22': 0.0068, '9_23': 0.0032, '9_24': 0.0032, '9_25': 0.0032, '9_26': 0.0048, '9_29': 0.0068, '9_30': 0.0032, '9_31': 0.0032, '9_32': 0.0032, '10': 0.4111, '10_1': 0.0352, '10_2': 0.022, '10_3': 0.0198, '10_4': 0.022, '10_5': 0.0308, '10_6': 0.0572, '10_7': 0.016, '10_8': 0.01, '10_9': 0.009, '10_10': 0.01, '10_11': 0.014, '10_12': 0.026, '10_13': 0.0128, '10_14': 0.008, '10_15': 0.0072, '10_16': 0.008, '10_17': 0.0112, '10_18': 0.0208, '10_19': 0.0096, '10_20': 0.006, '10_21': 0.0054, '10_22': 0.006, '10_23': 0.0084, '10_25': 0.0048, '10_26': 0.003, '10_27': 0.0027, '10_28': 0.003, '10_29': 0.0042, '10_31': 0.0064, '10_32': 0.004, '10_33': 0.0036, '10_34': 0.004, '11': 0.3184, '11_1': 0.0315, '11_2': 0.021, '11_3': 0.021, '11_4': 0.0273, '11_5': 0.0336, '11_6': 0.0195, '11_7': 0.013, '11_8': 0.013, '11_9': 0.0169, '11_10': 0.0208, '11_11': 0.0105, '11_12': 0.007, '11_13': 0.007, '11_14': 0.0091, '11_15': 0.0112, '11_16': 0.0075, '11_17': 0.005, '11_18': 0.005, '11_19': 0.0065, '11_20': 0.008, '11_21': 0.0075, '11_22': 0.005, '11_23': 0.005, '11_24': 0.0065, '12': 0.199, '12_1': 0.0285, '12_2': 0.0152, '12_3': 0.0152, '12_4': 0.0171, '12_6': 0.012, '12_7': 0.0064, '12_8': 0.0064, '12_9': 0.0072, '12_10': 0.012, '12_11': 0.009, '12_12': 0.0048, '12_13': 0.0048, '12_14': 0.0054, '12_15': 0.009, '12_16': 0.006, '12_17': 0.0032, '12_18': 0.0032, '12_19': 0.0036, '12_20': 0.006, '12_21': 0.009, '12_22': 0.0048, '12_23': 0.0048, '12_24': 0.0054, '13': 0.4288, '13_1': 0.0442, '13_2': 0.0312, '13_3': 0.026, '13_4': 0.0364, '13_5': 0.0832, '13_6': 0.0187, '13_7': 0.0132, '13_8': 0.011, '13_9': 0.0154, '13_10': 0.0352, '13_11': 0.0102, '13_12': 0.0072, '13_13': 0.006, '13_14': 0.0084, '13_15': 0.0192, '13_16': 0.0085, '13_17': 0.006, '13_18': 0.005, '13_19': 0.007, '13_21': 0.0068, '13_22': 0.0048, '13_23': 0.004, '13_24': 0.0056, '13_26': 0.0068, '13_27': 0.0048, '13_28': 0.004, '14': 0.4026, '14_1': 0.0336, '14_2': 0.021, '14_3': 0.0189, '14_4': 0.021, '14_5': 0.0294, '14_6': 0.0546, '14_7': 0.0176, '14_8': 0.011, '14_9': 0.0099, '14_10': 0.011, '14_11': 0.0154, '14_12': 0.0286, '14_13': 0.0112, '14_14': 0.007, '14_15': 0.0063, '14_16': 0.007, '14_17': 0.0098, '14_18': 0.0182, '14_19': 0.008, '14_20': 0.005, '14_21': 0.0045, '14_22': 0.005, '14_23': 0.007, '14_25': 0.0064, '14_26': 0.004, '14_27': 0.0036, '14_28': 0.004, '14_29': 0.0056, '14_31': 0.0064, '14_32': 0.004, '14_33': 0.0036, '14_34': 0.004, '15': 0.2975, '15_1': 0.0408, '15_2': 0.024, '15_3': 0.024, '15_4': 0.0312, '15_6': 0.0153, '15_7': 0.009, '15_8': 0.009, '15_9': 0.0117, '15_10': 0.0225, '15_11': 0.0136, '15_12': 0.008, '15_13': 0.008, '15_14': 0.0104, '15_15': 0.02, '15_16': 0.0085, '15_17': 0.005, '15_18': 0.005, '15_19': 0.0065, '15_21': 0.0085, '15_22': 0.005, '15_23': 0.005, '15_24': 0.0065, '16': 0.3823, '16_1': 0.0425, '16_2': 0.025, '16_3': 0.025, '16_4': 0.025, '16_5': 0.035, '16_6': 0.06, '16_7': 0.0187, '16_8': 0.011, '16_9': 0.011, '16_10': 0.011, '16_11': 0.0154, '16_12': 0.0264, '16_13': 0.0119, '16_14': 0.007, '16_15': 0.007, '16_16': 0.007, '16_17': 0.0098, '16_19': 0.0068, '16_20': 0.004, '16_21': 0.004, '16_22': 0.004, '16_25': 0.0068, '16_26': 0.004, '16_27': 0.004, '17': 0.313, '17_1': 0.0336, '17_2': 0.0216, '17_3': 0.0216, '17_4': 0.0192, '17_5': 0.024, '17_6': 0.0432, '17_7': 0.014, '17_8': 0.009, '17_9': 0.009, '17_10': 0.008, '17_11': 0.01, '17_12': 0.018, '17_13': 0.0084, '17_14': 0.0054, '17_15': 0.0054, '17_16': 0.0048, '17_17': 0.006, '17_18': 0.0108, '17_19': 0.007, '17_20': 0.0045, '17_21': 0.0045, '17_22': 0.004, '17_23': 0.005, '17_25': 0.0056, '17_26': 0.0036, '17_27': 0.0036, '17_28': 0.0032}

def Integrate_z_pT_Bins(Histogram_List_All, Default_Histo_Name, VARIABLE="(phi_t)", Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off"):
    Default_Histo_Name_Integrated = str(str(Default_Histo_Name.replace("Data_Type", Method)).replace("z_pT_Bin_All", "z_pT_Bin_Integrated"))    
    if((Multi_Dim_Option   not in ["Off"]) and ("Response" not in str(Method))):
        if(Multi_Dim_Option    in ["5D"]):
            Default_Histo_Name_Integrated     = str(Default_Histo_Name_Integrated.replace(VARIABLE,       "(MultiDim_Q2_y_z_pT_phi_h)")).replace("(1D)", "(MultiDim_5D_Histo)")
        elif(Multi_Dim_Option  in ["3D"]):
            Default_Histo_Name_Integrated     = str(Default_Histo_Name_Integrated.replace(VARIABLE,  "(MultiDim_z_pT_Bin_Y_bin_phi_t)")).replace("(1D)", "(MultiDim_3D_Histo)")
        else:
            if("y" in Binning_Method):
                Default_Histo_Name_Integrated = str(Default_Histo_Name_Integrated.replace(VARIABLE, "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
            else:
                Default_Histo_Name_Integrated = str(Default_Histo_Name_Integrated.replace(VARIABLE, "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
    if(str(Method) in ["rdf", "gdf", "tdf"]):
        Default_Histo_Name_Integrated         = str(Default_Histo_Name_Integrated.replace("Smear",  "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear"))
        
    Allow_Fitting = ("phi" in VARIABLE) and (Fit_Test) and (Method not in ["rdf", "mdf", "Background", "Relative_Background", "Acceptance"])
        
    if(Allow_Fitting):
        for entry_type in ["1D", "MultiDim_5D_Histo", "MultiDim_3D_Histo", "Multi-Dim Histo"]:
            Integrated_Histo_Fit_Function = str(Default_Histo_Name_Integrated.replace(str(entry_type), "Fit_Function"))
            Integrated_Histo__Chi_Squared = str(Default_Histo_Name_Integrated.replace(str(entry_type), "Chi_Squared"))
            Integrated_Histo____Fit_Par_A = str(Default_Histo_Name_Integrated.replace(str(entry_type), "Fit_Par_A"))
            Integrated_Histo____Fit_Par_B = str(Default_Histo_Name_Integrated.replace(str(entry_type), "Fit_Par_B"))
            Integrated_Histo____Fit_Par_C = str(Default_Histo_Name_Integrated.replace(str(entry_type), "Fit_Par_C"))
            if("Fit_Function" in str(Integrated_Histo_Fit_Function)):
                break
        if("Fit_Function" not in str(Integrated_Histo_Fit_Function)):
            raise TypeError(f"Integrated_Histo_Fit_Function = {Integrated_Histo_Fit_Function} is missing the proper naming convensions (i.e., it should have 'Fit_Function' in its name)")
            
    if("sec" in str(VARIABLE)):
        Variable_Title = "#phi_{h}"
        Particle_Sector = "#pi^{+} Sector !" if("pipsec" in str(VARIABLE)) else "Electron Sector !"
        for sec in range(1, 7):
            if(f"sec_{sec}" in str(VARIABLE)):
                Particle_Sector = Particle_Sector.replace("!", str(sec))
                break
        Variable_Title = f"({Particle_Sector}) {Variable_Title}"
    else:
        Particle_Sector = "N/A"
        if("MM" in VARIABLE):
            Variable_Title = "Missing Mass"
        else:
            Variable_Title = "".join(["P_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(el)", "(pip)"]) else "".join(["#theta_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(elth)", "(pipth)"]) else "".join(["#phi_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(elPhi)", "(pipPhi)"]) else "#phi_{h}"
            if("#phi_{h}" not in Variable_Title):
                for var_error_title in ["{elth}", "{elPhi}", "{pipth}", "{pipPhi}"]:
                    Variable_Title = Variable_Title.replace(var_error_title, "{El}" if("el" in var_error_title) else "{#pi^{+}}")
    if((str(Method) not in ["rdf", "gdf", "tdf"]) and ("Smear" in str(Default_Histo_Name_Integrated))):
        Variable_Title = f"{Variable_Title} (Smeared)"
            
    z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
    for Bin_Type in ["Integrated", "Common_Int"]:
        if(Common_Int_Bins and (Bin_Type not in ["Common_Int"])):
            print(f"{color.RED}Not Running Full z-pT Intergration (i.e., select region only){color.END}")
            continue
        Default_Histo_Name_Integrated     = str(str(Default_Histo_Name_Integrated.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
        if(Allow_Fitting):
            Integrated_Histo_Fit_Function = str(str(Integrated_Histo_Fit_Function.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
            Integrated_Histo__Chi_Squared = str(str(Integrated_Histo__Chi_Squared.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
            Integrated_Histo____Fit_Par_A = str(str(Integrated_Histo____Fit_Par_A.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
            Integrated_Histo____Fit_Par_B = str(str(Integrated_Histo____Fit_Par_B.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
            Integrated_Histo____Fit_Par_C = str(str(Integrated_Histo____Fit_Par_C.replace("z_pT_Bin_All", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Integrated", f"z_pT_Bin_{Bin_Type}")).replace("z_pT_Bin_Common_Int", f"z_pT_Bin_{Bin_Type}")
        
        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=((Bin_Type in ["Common_Int"]) or Common_Int_Bins))):
                continue
            Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_Integrated.replace(f"z_pT_Bin_{Bin_Type}", f"z_pT_Bin_{z_pT_Bin}"))
            
            try:
                if("1D" in str(type(Histogram_List_All[Default_Histo_Name_Integrated]))):
                    # Histogram_List_All[str(Default_Histo_Name_Integrated)] Already Exists...
                    hist_clone = Histogram_List_All[Default_Histo_Name_z_pT_Bin].Clone()
                    # hist_clone.Scale(Area_of_z_pT_Bins[f"{Q2_Y_Bin}_{z_pT_Bin}"]/Area_of_z_pT_Bins[f"{Q2_Y_Bin}"])
                    Histogram_List_All[Default_Histo_Name_Integrated].Add(hist_clone)
                    hist_clone = None  # Explicitly drop the reference, allowing Python to clean up
                else:
                    raise TypeError(f"{Default_Histo_Name_Integrated} is NOT a 1D histogram")
            except KeyError:
                # print(f"{color.BOLD}Making Histogram_List_All[{color.UNDERLINE}{Default_Histo_Name_Integrated}{color.END_B}] from the initial z-pT Bin (Bin {z_pT_Bin})...{color.END}")
                print(f"{color.BOLD}Making Histogram_List_All[{color.UNDERLINE}{Default_Histo_Name_Integrated}{color.END_B}]...{color.END}")
                Histogram_List_All[Default_Histo_Name_Integrated] = Histogram_List_All[Default_Histo_Name_z_pT_Bin].Clone(Default_Histo_Name_Integrated)
                if(Bin_Type in ["Common_Int"]):
                    Bin_Title_Integrated_z_pT_Bins = str(Histogram_List_All[Default_Histo_Name_Integrated].GetTitle()).replace("z-P_{T} Bin: 1}", "z-P_{T} Bin: Integrated (Over Common Range)}")
                else:
                    Bin_Title_Integrated_z_pT_Bins = str(Histogram_List_All[Default_Histo_Name_Integrated].GetTitle()).replace("z-P_{T} Bin: 1}", "z-P_{T} Bin: Integrated}")
                Bin_Title_Integrated_z_pT_Bins 
                Histogram_List_All[Default_Histo_Name_Integrated].SetTitle(f"{Bin_Title_Integrated_z_pT_Bins};{Variable_Title}")
                # print(f"Final Title   = {Histogram_List_All[Default_Histo_Name_Integrated].GetTitle()}")
                # Histogram_List_All[Default_Histo_Name_Integrated].Scale(Area_of_z_pT_Bins[f"{Q2_Y_Bin}_{z_pT_Bin}"]/Area_of_z_pT_Bins[f"{Q2_Y_Bin}"])
                ##################################################################### ################################################################
                #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetLineWidth(2)
                # Histogram_List_All[str(Default_Histo_Name_Integrated)].SetMarkerSize(1 if(str(Method) not in ["Bin", "bbb", "bin", "Bin-by-Bin", "Bin-By-Bin", "Bin-by-bin", "bin-by-bin"]) else 1.5)
                # Histogram_List_All[str(Default_Histo_Name_Integrated)].SetLineWidth(3  if(str(Method)     in ["gdf", "Background", "Relative_Background", "tdf"]) else 2)
                Set_Color       = root_color.Blue if(str(Method) in ["rdf", "Acceptance"]) else root_color.Red if(str(Method) in ["mdf"])                                             else root_color.Green if(str(Method) in ["gdf"]) else root_color.Black if(str(Method) in ["Background", "Relative_Background"]) else root_color.Cyan  if(str(Method) in ["tdf"]) else root_color.Brown if(str(Method) in ["Bin", "bbb", "bin", "Bin-by-Bin", "Bin-By-Bin", "Bin-by-bin", "bin-by-bin"]) else root_color.Teal  if(str(Method) in ["Bayesian", "Bayes"]) else root_color.Pink  if(str(Method) in ["SVD"]) else "ERROR"
                Set_MarkerStyle = 21              if(str(Method) in ["mdf"])               else 20             if(str(Method) in ["gdf", "tdf", "Background", "Relative_Background"]) else 21
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetLineColor(Set_Color)
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetMarkerColor(Set_Color)
                Histogram_List_All[str(Default_Histo_Name_Integrated)].SetMarkerStyle(Set_MarkerStyle)
                #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
                ##################################################################### ################################################################
            except Exception as e:
                # Re-raise any other unexpected exceptions
                print(f"Unexpected error occurred: {e}")
                raise
        try:
            if(Allow_Fitting):
                Histogram_List_All[str(Default_Histo_Name_Integrated)], Histogram_List_All[str(Integrated_Histo_Fit_Function)], Histogram_List_All[str(Integrated_Histo__Chi_Squared)], Histogram_List_All[str(Integrated_Histo____Fit_Par_A)], Histogram_List_All[str(Integrated_Histo____Fit_Par_B)], Histogram_List_All[str(Integrated_Histo____Fit_Par_C)] = Fitting_Phi_Function(Histo_To_Fit=Histogram_List_All[str(Default_Histo_Name_Integrated)], Method=Method, Special=[int(Q2_Y_Bin), "Integrated", Particle_Sector])
                # print(f"""{color.BOLD}Made:
                # Histogram_List_All[{Default_Histo_Name_Integrated}], 
                # Histogram_List_All[{Integrated_Histo_Fit_Function}], 
                # Histogram_List_All[{Integrated_Histo__Chi_Squared}], 
                # Histogram_List_All[{Integrated_Histo____Fit_Par_A}], 
                # Histogram_List_All[{Integrated_Histo____Fit_Par_B}], 
                # Histogram_List_All[{Integrated_Histo____Fit_Par_C}]{color.END}\n\n""")
        except Exception as e:
            print(f"{color.Error}ERROR IN 'Integrated z-pT Bins' METHOD = '{str(Method)}':\n{color.END_R}{str(traceback.format_exc())}{color.END}")
    
    return Histogram_List_All
    
##################################################################################################################################################################
##==========##==========## Function for Creating the Integrated z-pT Bin Histograms     ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################












########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loading Data Files     ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################



def FileLocation(FileName, Datatype):
    if(args.single_file):
        return args.single_file_input
    # location = "Histo_Files_ROOT/"
    location = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/"
    if(str(Datatype) == 'rdf'):
        file = "".join(["REAL_Data/SIDIS_epip_Data_REC_",         str(FileName), ".root"])
    if((str(Datatype) == 'mdf') or ((str(Datatype) in ['rdf']) and Sim_Test)):
        file = "".join(["Matching_REC_MC/SIDIS_epip_MC_Matched_", str(FileName), ".root"])
    if(str(Datatype) == 'gdf'):
        file = "".join(["GEN_MC/SIDIS_epip_MC_GEN_",              str(FileName), ".root"])
    loading = f"{location}{file}"
    return loading



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################


Common_Name = "Pass_2_Plots_for_Maria_FC_14_V1_All"
Common_Name = "Pass_2_Plots_for_Maria_FC_14_V2_All" # Same as V1 above but with sector plots and no MM plots
Common_Name = "Pass_2_Plots_for_Maria_FC_14_V3_All" # Same as V2 above but with additional MC files (run rdf with V2)

# if(not (Tag_ProQ or Cut_ProQ)):
Common_Name = "Pass_2_Sector_Integrated_Tests_FC_14_V2_All"


Common_Name =  "Pass_2_Sector_Tests_FC_14_V1_All"
# Common_Name = "Pass_2_Sector_Tests_FC_14_V1_EvGen_All"

Common_Name = "Pass_2_Acceptance_Tests_FC_14_V1_All"
if(args.EvGen):
    Common_Name = "Pass_2_Acceptance_Tests_FC_14_V1_EvGen_All"
    Common_Name = "Pass_2_Acceptance_Tests_FC_14_V2_EvGen_All"

Pass_Version = "Pass 2" if("Pass_2" in Common_Name) else "Pass 1"
if(Pass_Version not in [""]):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"{Pass_Version} - {Standard_Histogram_Title_Addition}"
    else:
        Standard_Histogram_Title_Addition = Pass_Version


if(Tag_ProQ):
    Common_Name = f"Tagged_Proton_{Common_Name}"

print(f"{color.BBLUE}\nRunning with {Pass_Version} files\n\n{color.END}")
        
        
# Use unique file(s) for one of datatypes? (If so, set the following if(...) conditions to 'False')

##################################
##   Real (Experimental) Data   ##
##################################
if(True):
#     print(f"\n{color.BOLD}Not using the common file name for the Real (Experimental) Data...{color.END}\n")
# if(False):
    REAL_File_Name = Common_Name
else:
    # REAL_File_Name = "Unfolding_Tests_V11_All"
    # REAL_File_Name = "Pass_2_Plots_for_Maria_FC_14_V2_All"
    # if(Pass_Version not in ["Pass 2"]):
    #     REAL_File_Name = REAL_File_Name.replace("Pass_2_", "")
    REAL_File_Name =  Common_Name
    REAL_File_Name =  "Pass_2_Sector_Tests_FC_14_V1_All"
    if(Common_Name == "Pass_2_Sector_Integrated_Tests_FC_14_V2_All"):
        REAL_File_Name = REAL_File_Name.replace("V2_All", "V1_All")
##################################
##   Real (Experimental) Data   ##
##################################

########################################
##   Reconstructed Monte Carlo Data   ##
########################################
if(args.mod or args.closure):
    MC_REC_File_Name = "Pass_2_Acceptance_Tests_FC_14_V1_DataWeight_All"
else:
    if(True):
        print(f"\n{color.BOLD}Not using the common file name for the Reconstructed Monte Carlo Data...{color.END}\n")
    if(False):
        MC_REC_File_Name = Common_Name
    else:
        # MC_REC_File_Name = "Unfolding_Tests_V13_Failed_All"
        # MC_REC_File_Name = "Analysis_Note_Update_V6_All"
        # MC_REC_File_Name = "Unsmeared_Pass_2_New_Sector_Cut_Test_V3_All" if(Smearing_Options in ["no_smear"]) else "Pass_2_New_Sector_Cut_Test_V3_All"
        MC_REC_File_Name = f"Unsmeared_{Common_Name}" if(Smearing_Options in ["no_smear"]) else Common_Name
        if(Pass_Version not in ["Pass 2"]):
            MC_REC_File_Name = MC_REC_File_Name.replace("Pass_2_", "")
########################################
##   Reconstructed Monte Carlo Data   ##
########################################

####################################
##   Generated Monte Carlo Data   ##
####################################
if(args.mod or args.closure):
    MC_GEN_File_Name = "Pass_2_Acceptance_Tests_V1_DataWeight_All"
else:
    if(True):
        print(f"\n{color.BOLD}Not using the common file name for the Generated Monte Carlo Data...{color.END}\n")
    if(False):
        MC_GEN_File_Name = Common_Name
    else:
    #     MC_GEN_File_Name = "Unfolding_Tests_V11_All"
    #     MC_GEN_File_Name = "Gen_Cuts_V2_Fixed_All"
    #     MC_GEN_File_Name = "Pass_2_New_Sector_Cut_Test_V9_All"
        for ii in range(0, 10, 1):
            if(Common_Name   not in [str(Common_Name).replace(f"_FC{ii}_",   "_")]):
                MC_GEN_File_Name   = str(Common_Name).replace(f"_FC{ii}_",   "_")
                break
            elif(Common_Name not in [str(Common_Name).replace(f"_FC_1{ii}_", "_")]):
                MC_GEN_File_Name   = str(Common_Name).replace(f"_FC_1{ii}_", "_")
                break
            else:
                MC_GEN_File_Name = Common_Name
        if(("Pass_2_New_Fiducial_Cut_Test_V13_All" in MC_GEN_File_Name) and (not Tag_ProQ)):
            MC_GEN_File_Name = "Pass_2_New_Fiducial_Cut_Test_V12_All"
        if(("Pass_2_New_Fiducial_Cut_Test_V15_All" in MC_GEN_File_Name) and (Tag_ProQ)):
            MC_GEN_File_Name = MC_GEN_File_Name.replace("Test_V15", "Test_V14")
        # MC_GEN_File_Name = "Pass_2_Plots_for_Maria_V1_Incomplete_All"
        if(Common_Name == "Pass_2_Sector_Integrated_Tests_FC_14_V2_All"):
            MC_GEN_File_Name = MC_GEN_File_Name.replace("V2_All", "V1_All")
    
####################################
##   Generated Monte Carlo Data   ##
####################################


if("Background_Tests" in str(MC_REC_File_Name)):
    Background_Type = "Unmatched Electron" if("V1" in str(MC_REC_File_Name)) else "Unmatched Pion" if("V2" in str(MC_REC_File_Name)) else "Wrong Electron" if("V3" in str(MC_REC_File_Name)) else "Wrong Pion" if("V4" in str(MC_REC_File_Name)) else "UNDEFINED BACKGROUND"
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = "".join(["#splitline{", str(Standard_Histogram_Title_Addition), "}{Background: ", str(Background_Type), "}"])
    else:
        Standard_Histogram_Title_Addition = f"Background: {Background_Type}"
    del Background_Type


# if(Mod_Test and ("Gen_Cuts_V7_All" in str(Common_Name))):
#     MC_REC_File_Name = "Gen_Cuts_V7_Modulated_All"
#     MC_GEN_File_Name = "Gen_Cuts_V7_Modulated_All"
# elif(Mod_Test):
#     if("_Modulated" not in str(MC_REC_File_Name)):
#         MC_REC_File_Name = str(MC_REC_File_Name).replace("_All", "_Modulated_All")
#     if("_Modulated" not in str(MC_GEN_File_Name)):
#         MC_GEN_File_Name = str(MC_GEN_File_Name).replace("_All", "_Modulated_All")

        
# 'TRUE_File_Name' refers to a file which is used in the closure tests where the simulated data is unfolded - corresponds to the distribution that should ideally be returned if the unfolding procedure is working correctly
TRUE_File_Name = ""
if(Sim_Test or args.closure):
    # REAL_File_Name = MC_REC_File_Name
    # TRUE_File_Name = MC_GEN_File_Name
    REAL_File_Name = "Pass_2_Acceptance_Tests_FC_14_V1_DataWeight_All"
    TRUE_File_Name = "Pass_2_Acceptance_Tests_V1_DataWeight_All"
    
# if(Closure_Test):
#     if("_Modulated" not in str(MC_REC_File_Name)):
#         REAL_File_Name = str(MC_REC_File_Name).replace("_All", "_Modulated_All")
#     else:
#         REAL_File_Name = MC_REC_File_Name
#     if("_Modulated" not in str(MC_GEN_File_Name)):
#         TRUE_File_Name = str(MC_GEN_File_Name).replace("_All", "_Modulated_All")
#     else:
#         TRUE_File_Name = MC_GEN_File_Name


################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################




if(args.single_file):
    MC_REC_File_Name = args.single_file_input
    MC_GEN_File_Name = args.single_file_input
    REAL_File_Name   = args.single_file_input
    TRUE_File_Name   = args.single_file_input




###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################
try:
    rdf = ROOT.TFile(str(FileLocation(str(REAL_File_Name), "rdf")), "READ")
    print(f"The total number of histograms available for the{color.BLUE}{' Real (Experimental) Data' if(not (Sim_Test or args.closure)) else ' Test Experimental (Simulated) Data'}{' ' if(Sim_Test) else '       '}{color.END} in '{color.BOLD}{REAL_File_Name}{  color.END}' is {color.BOLD}{len(rdf.GetListOfKeys())}{color.END}")
except:
    print(f"\n{color.Error}ERROR IN GETTING THE 'rdf' DATAFRAME...\n{color.END}Traceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
try:
    mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
    print(f"The total number of histograms available for the{color.RED} Reconstructed Monte Carlo Data{' ' if(not (Sim_Test or args.closure)) else '     '}{                                                         color.END} in '{color.BOLD}{MC_REC_File_Name}{color.END}' is {color.BOLD}{len(mdf.GetListOfKeys())}{color.END}")

except:
    print(f"\n{color.Error}ERROR IN GETTING THE 'mdf' DATAFRAME...\n{color.END}Traceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
try:
    gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
    print(f"The total number of histograms available for the{color.GREEN} Generated Monte Carlo Data{'     ' if(not (Sim_Test or args.closure)) else '         '}{                                                   color.END} in '{color.BOLD}{MC_GEN_File_Name}{color.END}' is {color.BOLD}{len(gdf.GetListOfKeys())}{color.END}")
except:
    print(f"\n{color.Error}ERROR IN GETTING THE 'gdf' DATAFRAME...\n{color.END}Traceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])):
    print("\nWill be using a file as the 'True' distribution (i.e., what 'rdf' should look like after unfolding)")
    try:
        tdf = ROOT.TFile(str(FileLocation(str(TRUE_File_Name), "gdf")), "READ")
        print(f"The total number of histograms available for the{color.CYAN} 'True' Monte Carlo Data   {'     ' if(not (Sim_Test or args.closure)) else '         '}{                                                 color.END} in '{color.BOLD}{TRUE_File_Name}{color.END}' is {color.BOLD}{len(tdf.GetListOfKeys())}{color.END}")
        
    except:
        print(f"\n{color.Error}ERROR IN GETTING THE 'tdf' DATAFRAME...\n{color.END}Traceback:\n{color.END_R}{traceback.format_exc()}{color.END}")

else:
    tdf = "N/A"
###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################

if(Create_txt_File):
    String_For_Output_txt = "".join([color.BOLD, """
    ######################################################################################################################################################
    ##==========##    COMPARISON OF DATA TO MONTE CARLO FOR RELEVANT KINEMATIC VARIABLES    ##==========##==========##==========##==========##==========##
    ######################################################################################################################################################
    """, color.END, timer.start_find(return_Q=True), """
    """, str(str(("".join(["Ran for Q2-y Bin(s): ", str(Q2_xB_Bin_List)]).replace("[",  "")).replace("]", "")).replace("'0'", "'All'")), """

    Files Used:
    """, "".join(["\tFile name for ", color.BLUE,  "Real (Experimental) Data"            if(not Sim_Test) else " Test Experimental (Simulated) Data", " " if(Sim_Test) else "       ", color.END, " in '", color.BOLD, REAL_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(REAL_File_Name),   "rdf")))]), """
    """, "".join(["\tFile name for ", color.RED,   "Reconstructed Monte Carlo Data", " " if(not Sim_Test) else "     ",                                                                color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_REC_File_Name), "mdf")))]), """
    """, "".join(["\tFile name for ", color.GREEN, "Generated Monte Carlo Data", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_GEN_File_Name), "gdf")))]), """
    """, "".join(["\tFile name for ", color.CYAN,  "'True' Monte Carlo Data   ", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, TRUE_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(TRUE_File_Name),   "gdf"))),   "\n"]) if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])) else "", """
    ##=========================================================##
    ##==========##   Starting to Run Comparisons   ##==========##
    ##=========================================================##"""])

else:
    String_For_Output_txt = ""
# Set String_For_Output_txt = "" to stop the comparison from printing the text-based results

print(f"\n\n{color.BOLD}Done Loading RDataFrame files...\n{color.END}")


########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loaded Data Files      ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################










##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##








run_5D_Unfold  = not True
if(run_5D_Unfold):
    Num_5D_Increments_Used_to_Slice = 422
    
run_Sec_Unfold = not True and (Smearing_Options in ["no_smear"])
run_Sec_Unfold = not True
run_SecCut_Unfold = not True

# if(Tag_ProQ or Cut_ProQ):
#     run_Sec_Unfold = True
#     run_SecCut_Unfold = False

if(run_Sec_Unfold or run_SecCut_Unfold):
    Sector_List = [1, 2, 3, 4, 5, 6]
    # Sector_List = [1, 1, 1, 1, 1, 1]


print(f"{color.BBLUE}\n\nStarting Unfolding Procedures...\n{color.END}")


Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods = {}, {}, {}, {}, {}, {}, {}, {}
Parameter_List_Unfold_Methods["SVD"], Parameter_List_Unfold_Methods["Bin"], Parameter_List_Unfold_Methods["Bayes"] = [], [], []
List_of_All_Histos_For_Unfolding = {}
count, count_failed = 0, 0

# for Simulation in ["clasdis", "EvGen"]:
#     if(Simulation == "EvGen"):
#         if(not args.EvGen):
#             continue
#         else:
#             print(f"\n\n===================================================================================================================================================================================================\n{color.BGREEN}NOW RUNNING WITH {color.END_B}{color.CYAN}{color.UNDERLINE}EvGen{color.END}\n\n")
#             MC_EvGen_REC_File_Name = MC_REC_File_Name.replace("_All", "_EvGen_All") if("EvGen" not in MC_REC_File_Name) else MC_REC_File_Name
#             Smearing_Options = "no_smear" # EvGen does not use smearing (as of 9/8/2025)
#             if("Unsmeared" not in MC_EvGen_REC_File_Name):
#                 MC_EvGen_REC_File_Name = MC_EvGen_REC_File_Name.replace("Matched_Pass_2", "Matched_Unsmeared_Pass_2")
#             MC_EvGen_GEN_File_Name = MC_GEN_File_Name.replace("_All", "_EvGen_All") if("EvGen" not in MC_GEN_File_Name) else MC_GEN_File_Name
#             if(Sim_Test):
#                 REAL_File_Name = MC_EvGen_REC_File_Name
#                 TRUE_File_Name = MC_EvGen_GEN_File_Name
#             if(Closure_Test):
#                 if("_Modulated" not in str(MC_EvGen_REC_File_Name)):
#                     REAL_File_Name = str(MC_EvGen_REC_File_Name).replace("_All", "_Modulated_All")
#                 else:
#                     REAL_File_Name = MC_EvGen_REC_File_Name
#                 if("_Modulated" not in str(MC_EvGen_GEN_File_Name)):
#                     TRUE_File_Name = str(MC_EvGen_GEN_File_Name).replace("_All", "_Modulated_All")
#                 else:
#                     TRUE_File_Name = MC_EvGen_GEN_File_Name
#             if(Sim_Test or Closure_Test):
#                 try:
#                     rdf = ROOT.TFile(str(FileLocation(str(REAL_File_Name), "rdf")), "READ")
#                     print(f"The total number of histograms available for the {color.BLUE}Test Experimental (Simulated) Data {color.END} in '{color.BOLD}{REAL_File_Name}{color.END}' is {color.BOLD}{len(rdf.GetListOfKeys())}{color.END}")
#                 except:
#                     print(f"{color.Error}\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
#                 print("\nWill be using a file as the 'True' distribution (i.e., what 'rdf' should look like after unfolding)")
#                 try:
#                     tdf = ROOT.TFile(str(FileLocation(str(TRUE_File_Name), "gdf")), "READ")
#                     print(f"The total number of histograms available for the{color.CYAN} 'True' Monte Carlo Data   {'     ' if(not Sim_Test) else '         '}{color.END} in '{color.BOLD}{TRUE_File_Name}{color.END}' is {color.BOLD}{len(tdf.GetListOfKeys())}{color.END}")
#                 except:
#                     print(f"{color.Error}\nERROR IN GETTING THE 'tdf' DATAFRAME...\nTraceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
#             try:
#                 mdf = ROOT.TFile(str(FileLocation(str(MC_EvGen_REC_File_Name), "mdf")), "READ")
#                 print(f"The total number of histograms available for the{color.RED} Reconstructed Monte Carlo Data{' ' if not Sim_Test else '     '}{color.END} in '{color.BOLD}{MC_EvGen_REC_File_Name}{color.END}' is {color.BOLD}{len(mdf.GetListOfKeys())}{color.END}")
#             except:
#                 print(f"{color.Error}\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
#             try:
#                 gdf = ROOT.TFile(str(FileLocation(str(MC_EvGen_GEN_File_Name), "gdf")), "READ")
#                 print(f"The total number of histograms available for the{color.GREEN} Generated Monte Carlo Data{'     ' if not Sim_Test else '         '}{color.END} in '{color.BOLD}{MC_EvGen_GEN_File_Name}{color.END}' is {color.BOLD}{len(gdf.GetListOfKeys())}{color.END}")
#             except:
#                 print(f"{color.Error}\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
#             print(f"\n{color.BOLD}Done loading EvGen Files{color.END}\n")

for ii in mdf.GetListOfKeys():
    if(Cor_Compare):
        print(f"{color.Error}\nCorrection Comparison Plot Option selected does NOT include Unfolding/Acceptance Corrections{color.END_R} (as of 4-18-2024){color.END}\n")
        break
    out_print_main = str(ii.GetName()).replace("mdf", "DataFrame_Type")

    # if(all(fixed_cuts not in out_print_main for fixed_cuts in ["cut_Complete_SIDIS_I", "cut_Complete_SIDIS_Proton_I"])):
    #     continue

    # if("Q2_y_z_pT_4D_Bins" not in out_print_main):
    #     continue
    # else:
    #     print(f"out_print_main:\n\t{out_print_main}\n")
    if("Q2_y_z_pT_4D_Bins" in out_print_main):
        continue
    else:
        print(f"out_print_main:\n\t{out_print_main}\n")

    if(("_(Weighed)" in out_print_main) and not (Mod_Test or Closure_Test)):
        print(f"\n{color.BOLD}Skipping '{out_print_main}' because it is weighed{color.END}\n")
        continue
    elif(("_(Weighed)" not in out_print_main) and Mod_Test):
        print(f"\n{color.BOLD}Skipping '{out_print_main}' because it is unweighed{color.END}\n")
        continue

    
    # count += 1
    # if("pipsec" in out_print_main):
    #     print(f"out_print_main ({count}):\n{out_print_main}\n")
    # continue
    
    ##========================================================##
    ##=====##    Conditions for Histogram Selection    ##=====##
    ##========================================================##
    
    Conditions_For_Unfolding = ["DataFrame_Type" in str(out_print_main)]
    # The histograms for 'out_print_main' will be skipped if any item in the list 'Conditions_For_Unfolding' is 'False'
    
    if("5D_Response" in str(out_print_main) and run_5D_Unfold):
        # Found a Response matrix for 5D unfolding (handles differently to other plots selected below)
        if(f"_Slice_1_(Increment='{Num_5D_Increments_Used_to_Slice}')" not in str(out_print_main)):
            # The full 5D Response matrix is split into multiple slices that are rebuilt into a single 2D histogram in this script
            # For the common key name, only the first slice is needed (not counted as failure)
            continue
        elif((f"_Slice_1_" in str(out_print_main)) and (f"_Slice_1_(Increment='{Num_5D_Increments_Used_to_Slice}')" not in str(out_print_main))):
            count_failed += 1
            print(f"{color.RED}Potential Reason for Failure: Incorrect number of increments in:\n\tout_print_main = {color.Error}{out_print_main}{color.END}")
            print(f"Number Failed: {count_failed}")
            continue
        ## Correct Histogram Type:
        Conditions_For_Unfolding.append(run_5D_Unfold) # Defined above (will not run 5D unfolding plots unless run_5D_Unfold = True)
        Conditions_For_Unfolding.append("5D_Response_Matrix"        in str(out_print_main))
        Conditions_For_Unfolding.append("5D_Response_Matrix_1D" not in str(out_print_main))
        Conditions_For_Unfolding.append("Background"            not in str(out_print_main))
        ## Correct Cuts:
        Conditions_For_Unfolding.append("no_cut"                not in str(out_print_main))
        Conditions_For_Unfolding.append("cut_Complete_EDIS"     not in str(out_print_main))
        # Do not include the electron sector cuts here
        Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS" not in str(out_print_main))
        # Conditions_For_Unfolding.append("cut_Complete_SIDIS"        in str(out_print_main))
        Conditions_For_Unfolding.append("no_cut_eS"             not in str(out_print_main))
        ## Correct Variable(s):
        Conditions_For_Unfolding.append("MultiDim_Q2_y_z_pT_phi_h"  in str(out_print_main))
        ## Correct Smearing:
        if((Smearing_Options not in ["no_smear", "both"])):
            Conditions_For_Unfolding.append("(Smear-Type='')"   not in str(out_print_main))
        if((Smearing_Options not in ["smear",    "both"])):
            Conditions_For_Unfolding.append("(Smear-Type='')"       in str(out_print_main))
        if(False in Conditions_For_Unfolding):
            count_failed += 1
            # print(f"Conditions_For_Unfolding = {Conditions_For_Unfolding}")
            # print(f"{color.RED}{out_print_main}{color.END}")
            # print(f"Number Failed: {count_failed}")
            continue
        else:
            out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
            if(out_print_main_mdf not in mdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                continue
            Base_Name             = out_print_main_mdf.replace("_Slice_1_", "_Slice_NUMBER_")
            Slice_Num, Histo_List = 1, {}
            while(Slice_Num < 800):
                histo_sliced = mdf.Get(Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_"))
                if(histo_sliced):  # Check if the histogram exists
                    Histo_List[Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_")] = histo_sliced
                    Slice_Num += 1
                else:
                    break  # Exit the loop if the histogram does not exist
            out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
            if(not Closure_Test):
                out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
            out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
            if(args.weighed_acceptace):
                out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
            ################################################################################
            ##======##     Removing Sliced Increments from non-TH2D Plot Names    ##======##
            out_print_main_rdf = out_print_main_rdf.replace(f"_Slice_1_(Increment='{Num_5D_Increments_Used_to_Slice}')", "")
            out_print_main_gdf = out_print_main_gdf.replace(f"_Slice_1_(Increment='{Num_5D_Increments_Used_to_Slice}')", "")
            out_print_main_mdf = out_print_main_mdf.replace(f"_Slice_1_(Increment='{Num_5D_Increments_Used_to_Slice}')", "")
            ##======##     Removing Sliced Increments from non-TH2D Plot Names    ##======##
            ################################################################################
            ##=============##    Removing Cuts from the Generated files    ##=============##
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
            for sector_cut_remove in range(1, 7):
                out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
            del sector_cut_remove
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
            ##=============##    Removing Cuts from the Generated files    ##=============##
            ################################################################################
            ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
            if(not Sim_Test):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                out_print_main_rdf = out_print_main_rdf.replace("smear", "")
            out_print_main_gdf     = out_print_main_gdf.replace("smear", "")
            ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
            ################################################################################
            ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
            out_print_main_rdf    = out_print_main_rdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
            out_print_main_gdf    = out_print_main_gdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
            out_print_main_mdf_1D = out_print_main_mdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
            ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
            ################################################################################
            
            if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf_1D}{color.END}\n")
                for ii in mdf.GetListOfKeys():
                    if(("5D_Response_Matrix_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                        print(str(ii.GetName()))
            if(Sim_Test):
                out_print_main_rdf = out_print_main_mdf_1D
                out_print_main_tdf = out_print_main_gdf
                if(not Closure_Test):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                    out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                if(tdf not in ["N/A"]):
                    if(out_print_main_tdf not in tdf.GetListOfKeys()):
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                        continue
                else:
                    print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
            if(out_print_main_rdf not in rdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                continue
            if(out_print_main_gdf not in gdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                continue
            
            count += 1
            print(f"\n{color.BGREEN}\n(5D) Unfolding: {out_print_main}){color.END}\n")
            ExREAL_1D   = rdf.Get(out_print_main_rdf)
            MC_REC_1D   = mdf.Get(out_print_main_mdf_1D)
            MC_GEN_1D   = gdf.Get(out_print_main_gdf)
            Response_2D = Rebuild_Matrix_5D(List_of_Sliced_Histos=Histo_List, Standard_Name=out_print_main_mdf, Increment=Num_5D_Increments_Used_to_Slice)
            del Histo_List
            if(tdf not in ["N/A"]):
                ExTRUE_1D = tdf.Get(out_print_main_tdf)
            else:
                ExTRUE_1D = "N/A"
            if("mdf" in str(ExREAL_1D.GetName())):
                print("\n    ExREAL_1D_initial.GetName() =", ExREAL_1D.GetName())
                ExREAL_1D.SetName(str(ExREAL_1D_initial.GetName()).replace("mdf", "rdf"))
                print("New ExREAL_1D_initial.GetName() =",   ExREAL_1D.GetName())
            
            # Getting MC Background Histogram (bgs - stands for BackGroundSubtraction)
            out_print_main_bdf_1D = out_print_main_mdf_1D.replace("'5D_Response_Matrix_1D'", "'Background_5D_Response_Matrix_1D'")
            if(((out_print_main_bdf_1D in mdf.GetListOfKeys()) or (out_print_main_bdf_1D in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf_1D))):
                MC_BGS_1D = mdf.Get(out_print_main_bdf_1D) if(not Sim_Test) else rdf.Get(out_print_main_bdf_1D)
                MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))
            else:
                MC_BGS_1D = "None"
                print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
                raise TypeError("Missing (5D) Background Histogram")
            if(Sim_Test and (str(MC_BGS_1D) not in ["None"])):
                # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                ExREAL_1D.Add(MC_BGS_1D)
            List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin="All", Z_PT_Bin="All", MC_BGS_1D=MC_BGS_1D)
            continue
    elif(any(sector_particle in out_print_main for sector_particle in ["esec", "pipsec"]) and run_Sec_Unfold):
        if("Var-D2='phi_t" not in out_print_main):
            # Only running with the 1D Unfolding options at this time
            continue
        ## Correct Q2-y Bin:
        for Q2_y_bin in Q2_xB_Bin_List:
            Q2_xB_Bin_Unfold = Q2_y_bin if(str(Q2_y_bin) not in ["All", "0", 0]) else "All"
            if(f"Q2-y-Bin={Q2_xB_Bin_Unfold}, " in str(out_print_main)):
                Conditions_For_Unfolding = [True]
                break
            else:
                Conditions_For_Unfolding = [False]
        ## Correct Histogram Type:
        Conditions_For_Unfolding.append(run_Sec_Unfold) # Defined above (will not run sector unfolding plots unless run_Sec_Unfold = True)
        Conditions_For_Unfolding.append("Normal_2D"                 in str(out_print_main))
        Conditions_For_Unfolding.append("Background"            not in str(out_print_main))
        ## Correct Cuts:
        Conditions_For_Unfolding.append("no_cut"                not in str(out_print_main))
        Conditions_For_Unfolding.append("cut_Complete_EDIS"     not in str(out_print_main))
        # Do not include the electron sector cuts here
        Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS" not in str(out_print_main))
        # Conditions_For_Unfolding.append("cut_Complete_SIDIS"        in str(out_print_main))
        Conditions_For_Unfolding.append("no_cut_eS"             not in str(out_print_main))
        # Proton Cuts (Can control from the command line arguments: add 'CP' options for 'Cut on Proton' - other inputs will prevent the Proton Missing Mass cuts from being run as of 8/26/2024)
        if(Cut_ProQ):
            Conditions_For_Unfolding.append(any(proCuts in str(out_print_main) for proCuts in ["_Proton'), ", "_Proton_Integrate'), "])) # Require Proton MM Cuts
        else:
            Conditions_For_Unfolding.append("_Proton'), "          not in str(out_print_main)) # Remove  Proton MM Cuts
            Conditions_For_Unfolding.append("_Proton_Integrate')"  not in str(out_print_main)) # Remove  Proton MM Cuts (with integrated bins)
        ## Correct Variable(s):
        Particle_Sector = "N/A"
        Conditions_For_Unfolding.append("Var-D1='esec"             in str(out_print_main)) # Electron Sector Only
        if("Var-D1='esec"   in str(out_print_main)):
            Particle_Sector = "Electron Sector"
        # Conditions_For_Unfolding.append("Var-D1='pipsec"           in str(out_print_main)) # Pi+ Pion Sector Only
        if("Var-D1='pipsec" in str(out_print_main)):
            Particle_Sector = "#pi^{+} Pion Sector"
        ## Correct Smearing:
        Smear_Found = "(Smear-Type='')" not in str(out_print_main)
        if((Smearing_Options not in ["no_smear", "both"])):
            Conditions_For_Unfolding.append("(Smear-Type='')"   not in str(out_print_main))
        if((Smearing_Options not in ["smear",    "both"])):
            Conditions_For_Unfolding.append("(Smear-Type='')"       in str(out_print_main))
        if(False in Conditions_For_Unfolding):
            count_failed += 1
            # print(f"Conditions_For_Unfolding = {Conditions_For_Unfolding}")
            # print(f"{color.RED}{out_print_main}{color.END}")
            # print(f"Number Failed: {count_failed}\n\n")
            continue
        else:
            out_print_main_mdf     = out_print_main.replace("DataFrame_Type", "mdf")
            out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
            if(not Closure_Test):
                out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
            out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
            if(args.weighed_acceptace):
                out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
            ################################################################################
            ##=============##          Finding MC Backgound Plots          ##=============##
            out_print_main_bdf = out_print_main_mdf.replace("Normal_2D", "Normal_Background_2D")
            ##=============##          Finding MC Backgound Plots          ##=============##
            ################################################################################
            ##=============##    Removing Cuts from the Generated files    ##=============##
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
            for sector_cut_remove in range(1, 7):
                out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
            del sector_cut_remove
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
            out_print_main_gdf     = out_print_main_gdf.replace("_Proton",                                    "")
            ##=============##    Removing Cuts from the Generated files    ##=============##
            ################################################################################
            ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
            if(not Sim_Test):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
            out_print_main_gdf     = out_print_main_gdf.replace("_smeared", "")
            out_print_main_gdf     = out_print_main_gdf.replace("smear",    "")
            ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
            ################################################################################
            
            if(out_print_main_mdf not in mdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                for ii in mdf.GetListOfKeys():
                    if(("Normal_2D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                        print(str(ii.GetName()))
            if(Sim_Test):
                out_print_main_rdf     = out_print_main_mdf
                out_print_main_tdf     = out_print_main_gdf
                if(not Closure_Test):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                    out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                if(tdf not in ["N/A"]):
                    if(out_print_main_tdf not in tdf.GetListOfKeys()):
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                        continue
                else:
                    print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
            if(out_print_main_rdf not in rdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                continue
            if(out_print_main_gdf not in gdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                continue

            count += 1
            print(f"\n{color.BGREEN}(Sector) Unfolding: {out_print_main}{color.END}\n")
            ExREAL_3D     = rdf.Get(out_print_main_rdf)
            MC_REC_3D     = mdf.Get(out_print_main_mdf)
            MC_GEN_3D     = gdf.Get(out_print_main_gdf)
            if(Sim_Test):
                ExTRUE_3D = tdf.Get(out_print_main_tdf)
            else:
                ExTRUE_3D = "N/A"
            if("mdf" in str(ExREAL_3D.GetName())):
                print("\n    ExREAL_3D.GetName() =", ExREAL_3D.GetName())
                ExREAL_3D.SetName(str(ExREAL_3D_initial.GetName()).replace("mdf", "rdf"))
                print("New ExREAL_3D.GetName() =",   ExREAL_3D.GetName())
            # Getting MC Background Histogram (BGS - stands for BackGroundSubtraction)
            if(((out_print_main_bdf in mdf.GetListOfKeys()) or (out_print_main_bdf in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf))):
                MC_BGS_3D = mdf.Get(out_print_main_bdf) if(not Sim_Test) else rdf.Get(out_print_main_bdf)
                MC_BGS_3D = mdf.Get(out_print_main_bdf)
                MC_BGS_3D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_3D.GetTitle()), "};", str(MC_REC_3D.GetXaxis().GetTitle()), ";", str(MC_REC_3D.GetYaxis().GetTitle())]))
            else:
                MC_BGS_3D = "None"
                print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf}{color.END_R}){color.END}")
                raise TypeError("Missing (Sector) Background Histogram")
            if(Sim_Test and (str(MC_BGS_3D) not in ["None"])):
                # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                ExREAL_3D.Add(MC_BGS_3D)
                
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_xB_Bin_Unfold)[1]
            for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
                if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_xB_Bin_Unfold, Z_PT_BIN=z_pT_Bin_Unfold, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                    continue
                for Sector in Sector_List:
                    if(Smear_Found):
                        out_print_main_____1D_Sector     = str(out_print_main.replace("z-PT-Bin=All",     "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        out_print_main_rdf_1D_Sector     = str(out_print_main_rdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        out_print_main_mdf_1D_Sector     = str(out_print_main_mdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        out_print_main_gdf_1D_Sector     = str(out_print_main_gdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        if(Sim_Test):
                            out_print_main_tdf_1D_Sector = str(out_print_main_tdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        out_print_main_bdf_1D_Sector     = str(out_print_main_bdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                    else:
                        out_print_main_____1D_Sector     = str(out_print_main.replace("z-PT-Bin=All",     "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                        out_print_main_rdf_1D_Sector     = str(out_print_main_rdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                        out_print_main_mdf_1D_Sector     = str(out_print_main_mdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                        out_print_main_gdf_1D_Sector     = str(out_print_main_gdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                        if(Sim_Test):
                            out_print_main_tdf_1D_Sector = str(out_print_main_tdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                        out_print_main_bdf_1D_Sector     = str(out_print_main_bdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")                    
                    
                    New_Bin_Title = "".join(["".join(["}{#splitline{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold), "".join([" #topbar z-P_{T} Bin: ", str(z_pT_Bin_Unfold)]) if(z_pT_Bin_Unfold not in [0]) else "", f" #topbar {Particle_Sector} {Sector}"]) if(str(Q2_xB_Bin_Unfold) not in ["All", "0", 0]) else "".join(["}{#splitline{", Particle_Sector, " ", str(Sector)]),  "}{Pass Version: #color[", str(root_color.Blue), "]{", str(Standard_Histogram_Title_Addition), "}}"])
                    
                    ExREAL_1D = ExREAL_3D.Clone(out_print_main_rdf_1D_Sector)
                    ExREAL_1D_Title = str(ExREAL_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                    ExREAL_1D_Title = ExREAL_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                    MC_REC_1D = MC_REC_3D.Clone(out_print_main_mdf_1D_Sector)
                    MC_REC_1D_Title = str(MC_REC_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                    MC_REC_1D_Title = MC_REC_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                    MC_GEN_1D = MC_GEN_3D.Clone(out_print_main_gdf_1D_Sector)
                    MC_GEN_1D_Title = str(MC_GEN_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                    MC_GEN_1D_Title = MC_GEN_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                    if(Sim_Test):
                        ExTRUE_1D = ExTRUE_3D.Clone(out_print_main_tdf_1D_Sector)
                        ExTRUE_1D_Title = str(ExTRUE_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                        ExTRUE_1D_Title = ExTRUE_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                    if(MC_BGS_3D not in ["None"]):
                        MC_BGS_1D = MC_BGS_3D.Clone(out_print_main_bdf_1D_Sector)
                        MC_BGS_1D_Title = str(MC_BGS_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                        MC_BGS_1D_Title = MC_BGS_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                        
                    # Setting z-pT Bins
                    ExREAL_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                    MC_REC_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                    MC_GEN_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                    if(Sim_Test):
                        ExTRUE_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                    if(MC_BGS_3D not in ["None"]):
                        MC_BGS_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                    # Setting Particle Sector
                    ExREAL_1D.GetYaxis().SetRangeUser(Sector,     Sector)
                    MC_REC_1D.GetYaxis().SetRangeUser(Sector,     Sector)
                    # MC_GEN_1D.GetYaxis().SetRangeUser(Sector,     Sector)
                    MC_GEN_1D.GetYaxis().SetRangeUser(0, 7) # Generated Sector is not useful
                    if(Sim_Test):
                        ExTRUE_1D.GetYaxis().SetRangeUser(Sector, Sector)
                    if(MC_BGS_3D not in ["None"]):
                        MC_BGS_1D.GetYaxis().SetRangeUser(Sector, Sector)
                        
                    ExREAL_1D = ExREAL_1D.Project3D("z")
                    ExREAL_1D.SetTitle(ExREAL_1D_Title)
                    MC_REC_1D = MC_REC_1D.Project3D("z")
                    MC_REC_1D.SetTitle(MC_REC_1D_Title)
                    MC_GEN_1D = MC_GEN_1D.Project3D("z")
                    MC_GEN_1D.SetTitle(MC_GEN_1D_Title)
                    if(Sim_Test):
                        ExTRUE_1D = ExTRUE_1D.Project3D("z")
                        ExTRUE_1D.SetTitle(ExTRUE_1D_Title)
                    else:
                        ExTRUE_1D = "N/A"
                    if(MC_BGS_3D not in ["None"]):
                        MC_BGS_1D = MC_BGS_1D.Project3D("z")
                        MC_BGS_1D.SetTitle(MC_BGS_1D_Title)
                
                    List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main_____1D_Sector, Response_2D="N/A", ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold, MC_BGS_1D=MC_BGS_1D)
        continue
    else:
        # continue
        ## Correct Histogram Type:
        # Conditions_For_Unfolding.append('''"Response_Matrix_Normal" in str(out_print_main)''')
        Conditions_For_Unfolding.append("Response_Matrix_Normal"    in str(out_print_main))

        # Conditions_For_Unfolding.append('''"Response_Matrix_Normal_1D" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Response_Matrix_Normal_1D"    not in str(out_print_main))
        
        Conditions_For_Unfolding.append("5D_Response" not in str(out_print_main))

        ## Correct Cuts:
        # Conditions_For_Unfolding.append('''"no_cut"                not in str(out_print_main)''')
        Conditions_For_Unfolding.append("no_cut"                   not in str(out_print_main))

        # Conditions_For_Unfolding.append('''"cut_Complete_EDIS"     not in str(out_print_main)''')
        Conditions_For_Unfolding.append("cut_Complete_EDIS"        not in str(out_print_main))

        # Do not include the electron sector cuts here
        # Conditions_For_Unfolding.append('''"cut_Complete_SIDIS_eS" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS"    not in str(out_print_main))
        # Conditions_For_Unfolding.append('''"no_cut_eS"             not in str(out_print_main)''')
        Conditions_For_Unfolding.append("no_cut_eS"                not in str(out_print_main))
        
        # Proton Cuts (Can control from the command line arguments: add 'CP' options for 'Cut on Proton' - other inputs will prevent the Proton Missing Mass cuts from being run as of 8/26/2024)
        if(Cut_ProQ):
            Conditions_For_Unfolding.append(any(proCuts in str(out_print_main) for proCuts in ["_Proton'), ", "_Proton_Integrate'), "] + [f"_Proton_eS{sec}o'), " for sec in range(1, 7)] + [f"_Proton_Integrate_eS{sec}o'), " for sec in range(1, 7)]))
            # Conditions_For_Unfolding.append("_Proton'), "              in str(out_print_main)) # Require Proton MM Cuts
        else:
            Conditions_For_Unfolding.append("_Proton'), "          not in str(out_print_main)) # Remove  Proton MM Cuts
            Conditions_For_Unfolding.append("_Proton_Integrate')"  not in str(out_print_main)) # Remove  Proton MM Cuts (with integrated bins)
            for sec in range(1, 7):
                Conditions_For_Unfolding.append(f"_Proton_eS{sec}o'), "          not in str(out_print_main)) # Remove Proton MM Cuts (Sector Cuts)
                Conditions_For_Unfolding.append(f"_Proton_Integrate_eS{sec}o')"  not in str(out_print_main)) # Remove Proton MM Cuts (with integrated bins - Sector Cuts)

        # # Require Integrated Bin Cuts
        # Conditions_For_Unfolding.append("Integrate')"     in str(out_print_main))
        # # Remove Integrated Bin Cuts
        # Conditions_For_Unfolding.append("Integrate')" not in str(out_print_main))

        # Remove inverted proton cut
        Conditions_For_Unfolding.append("RevPro"      not in str(out_print_main))

        ## Correct Variable(s):
        # # Conditions_For_Unfolding.append('''"phi_t" in str(out_print_main)''')
        # Conditions_For_Unfolding.append("phi_t"    in str(out_print_main))
        # # Conditions_For_Unfolding.append("'phi_t"      not in str(out_print_main))
        Conditions_For_Unfolding.append("Multi_Dim_" not in str(out_print_main)) # For removing all (Old 3D) Multidimensional Unfolding Plots
        # Conditions_For_Unfolding.append("Multi_Dim_"     in str(out_print_main)) # For running only (Old 3D) Multidimensional Unfolding Plots
        
        # Conditions_For_Unfolding.append("MultiDim_" not in str(out_print_main)) # For removing all (New 3D) Multidimensional Unfolding Plots
        # Conditions_For_Unfolding.append("MultiDim_"     in str(out_print_main)) # For running only (New 3D) Multidimensional Unfolding Plots

        # if(not (Tag_ProQ or Cut_ProQ)):
        #     # Conditions_For_Unfolding.append("Multi" not in str(out_print_main)) # For removing all (3D) Multidimensional Unfolding Plots (Old and New)
        #     Conditions_For_Unfolding.append("Multi"     in str(out_print_main)) # For running only (3D) Multidimensional Unfolding Plots (Old and New)
        # else:
        #     Conditions_For_Unfolding.append("Multi" not in str(out_print_main))
        
        # Conditions_For_Unfolding.append("Var-D1='MM"     in str(out_print_main))
        # if(Closure_Test):
        #     Conditions_For_Unfolding.append("'Multi_Dim_z_pT_Bin_y_bin_phi_t"      in str(out_print_main))

        if("y" in Binning_Method):
            # Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
            Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)
        else:
            # Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_Y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
            Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_Y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)

        # Conditions_For_Unfolding.append('''"Multi_Dim_Q2_phi_t"               not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_Q2_phi_t"                  not in str(out_print_main))

        # Conditions_For_Unfolding.append('''"Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t"    not in str(out_print_main))

        # Not Tested Yet...
        # Conditions_For_Unfolding.append('''"Multi_Dim_elth_phi_t"  not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_elth_phi_t"     not in str(out_print_main))

        # Conditions_For_Unfolding.append('''"Multi_Dim_pipth_phi_t" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_pipth_phi_t"    not in str(out_print_main))

        # Conditions_For_Unfolding.append('''"Multi_Dim_elPhi_phi_t" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_elPhi_phi_t"    not in str(out_print_main))

        # Conditions_For_Unfolding.append('''"Multi_Dim_pipPhi_phi_t not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Multi_Dim_pipPhi_phi_t"   not in str(out_print_main))
        # Conditions_For_Unfolding.append(("Multi_Dim_elth_phi_t" in str(out_print_main)) or ("Multi_Dim_pipth_phi_t" in str(out_print_main)) or ("Multi_Dim_elPhi_phi_t" in str(out_print_main)) or ("Multi_Dim_pipPhi_phi_t" in str(out_print_main)))


        ## Correct Binning:
        # Conditions_For_Unfolding.append("Q2-xB-Bin=1" in str(out_print_main))
        # Conditions_For_Unfolding.append("Q2-xB-Bin=All" not in str(out_print_main))

        # Smearing Options:
        # if((Smearing_Options not in ["no_smear", "both"]) or  (Sim_Test)):
        if((Smearing_Options not in ["no_smear", "both"])):
            # Conditions_For_Unfolding.append('''"(Smear-Type='')" not in str(out_print_main)''')
            Conditions_For_Unfolding.append("(Smear-Type='')"    not in str(out_print_main))
        # if((Smearing_Options not in ["smear",    "both"]) and (not Sim_Test)):
        if((Smearing_Options not in ["smear",    "both"])):
            # Conditions_For_Unfolding.append('''"(Smear-Type='')"     in str(out_print_main)''')
            Conditions_For_Unfolding.append("(Smear-Type='')"        in str(out_print_main))


        # if(False not in Conditions_For_Unfolding):
        #     print("\nout_print_main =\n  ", out_print_main, "\n")
        #     print("Conditions_For_Unfolding:")
        #     for ii in Conditions_For_Unfolding:
        #         if(type(ii) is str):
        #             print("".join([str(ii), ":"]))
        #         else:
        #             print("".join(["\t", color.GREEN if(ii) else color.Error, str(ii), color.END]))
        #     stop

        ##========================================================##
        ##=====##    Conditions for Histogram Selection    ##=====##
        ##========================================================##

        if(False in Conditions_For_Unfolding):
            # Conditions for unfolding were not met by 'out_print_main'
            count_failed += 1
            # print("Conditions_For_Unfolding =", Conditions_For_Unfolding)
            # print("".join([color.RED, str(out_print_main), color.END]))
            # print("".join(["Number Failed: ", str(count_failed)]))
            continue
        else:
            del Conditions_For_Unfolding # Do not need the list of conditions for the rest of this loop
            
            out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
            if(not Closure_Test):
                out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
            out_print_main_mdf     = out_print_main.replace("DataFrame_Type", "mdf")
            out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
            if(args.weighed_acceptace):
                out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
            ################################################################################
            ##=============##    Removing Cuts from the Generated files    ##=============##
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
            for sector_cut_remove in range(1, 7):
                out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
                out_print_main_gdf = out_print_main_gdf.replace(f"Integrate_eS{sector_cut_remove}o",       "Integrate")
            del sector_cut_remove
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS_Proton",                  "no_cut")
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
            out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
            ##=============##    Removing Cuts from the Generated files    ##=============##
            ################################################################################


            #############################################################################
            ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
            if(not Sim_Test):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                out_print_main_rdf = out_print_main_rdf.replace("smear_",   "")
                out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
            out_print_main_gdf     = out_print_main_gdf.replace("_smeared", "")
            out_print_main_gdf     = out_print_main_gdf.replace("smear_",   "")
            out_print_main_gdf     = out_print_main_gdf.replace("smear",    "")
            ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
            #############################################################################


            ############################################################################
            ##=============##    Removing Gen_MM_Cut from RDF files    ##=============##
            out_print_main_rdf = out_print_main_rdf.replace(", (Gen_MM_Cut)", "")
            ##=============##    Removing Gen_MM_Cut from RDF files    ##=============##
            ############################################################################

            #############################################################################
            ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
            out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
            out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
            out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix'",        "'Response_Matrix_1D'")
            out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix'",        "'Response_Matrix_1D'")
            ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
            #############################################################################


            ##########################################################################################
            ##======##    Fixing potential LACK of z-pT bins in Multi-Dim Response Matix    ##======##
            # if(Common_Name in ["New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All"]):
            if(Common_Name in ["New_Binning_Schemes_V8_All"]):
                if(("Var-D2='z_pT_Bin" not in str(out_print_main_rdf)) and ("Var-D1='Multi_Dim" in str(out_print_main_rdf))):
                    out_print_main_rdf = out_print_main_rdf.replace("))", "".join(["), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
                if(("Var-D2='z_pT_Bin" not in str(out_print_main_gdf)) and ("Var-D1='Multi_Dim" in str(out_print_main_gdf))):
                    out_print_main_gdf = out_print_main_gdf.replace("))", "".join(["), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
            ##======##    Fixing potential LACK of z-pT bins in Multi-Dim Response Matix    ##======##
            ##########################################################################################
            # ##########################################################################################
            # ##======## Fixing potential LACK of (New) z-pT bins in Multi-Dim Response Matix ##======##
            # if(Common_Name in ["Gen_Cuts_V6_All"]):
            #     if(("Var-D2='z_pT_Bin" not in str(out_print_main_rdf)) and ("Var-D1='Multi_Dim" in str(out_print_main_rdf))):
            #         out_print_main_rdf = out_print_main_rdf.replace("))", "), (Var-D2='z_pT_Bin_y_bin'-[NumBins=43, MinBin=-0.5, MaxBin=42.5]))")
            #     if(("Var-D2='z_pT_Bin" not in str(out_print_main_gdf)) and ("Var-D1='Multi_Dim" in str(out_print_main_gdf))):
            #         out_print_main_gdf = out_print_main_gdf.replace("))", "), (Var-D2='z_pT_Bin_y_bin'-[NumBins=43, MinBin=-0.5, MaxBin=42.5]))")
            # ##======## Fixing potential LACK of (New) z-pT bins in Multi-Dim Response Matix ##======##
            # ##########################################################################################

            if(out_print_main_mdf not in mdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                continue

            out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
            if(("".join([", (Var-D2='z_pT_Bin", str(Binning_Method)]) not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
                out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "".join(["]), (Var-D2='z_pT_Bin", str(Binning_Method), "" if("smear" not in str(out_print_main_mdf_1D)) else "_smeared", "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
            if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf_1D}{color.END}\n")
                for ii in mdf.GetListOfKeys():
                    if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                        print(str(ii.GetName()))

            out_print_main_tdf = None
            if(Sim_Test):
                out_print_main_rdf     = out_print_main_mdf_1D
                out_print_main_tdf     = out_print_main_gdf
                if(not Closure_Test):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                    out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                if(tdf not in ["N/A"]):
                    if(out_print_main_tdf not in tdf.GetListOfKeys()):
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                        continue
                else:
                    print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
            if(out_print_main_rdf not in rdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                continue
            if(out_print_main_gdf not in gdf.GetListOfKeys()):
                print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                continue



            # Q2_xB_Bin_Unfold = 0 if("Q2-xB-Bin=All" in str(out_print_main)) else 1 if("Q2-xB-Bin=1" in str(out_print_main)) else 2 if("Q2-xB-Bin=2" in str(out_print_main)) else 3 if("Q2-xB-Bin=3" in str(out_print_main)) else 4 if("Q2-xB-Bin=4" in str(out_print_main)) else 5 if("Q2-xB-Bin=5" in str(out_print_main)) else 6 if("Q2-xB-Bin=6" in str(out_print_main)) else 7 if("Q2-xB-Bin=7" in str(out_print_main)) else 8 if("Q2-xB-Bin=8" in str(out_print_main)) else 9 if("Q2-xB-Bin=9" in str(out_print_main)) else 10 if("Q2-xB-Bin=10" in str(out_print_main)) else 11 if("Q2-xB-Bin=11" in str(out_print_main)) else 12 if("Q2-xB-Bin=12" in str(out_print_main)) else "Undefined..."
            # Q2_xB_Bin_Unfold = 0 if("Q2-xB-Bin=All" in str(out_print_main) or "Q2-y-Bin=All," in str(out_print_main)) else 1 if("Q2-xB-Bin=1," in str(out_print_main) or "Q2-y-Bin=1," in str(out_print_main)) else 2 if("Q2-xB-Bin=2," in str(out_print_main) or "Q2-y-Bin=2," in str(out_print_main)) else 3 if("Q2-xB-Bin=3," in str(out_print_main) or "Q2-y-Bin=3," in str(out_print_main)) else 4 if("Q2-xB-Bin=4," in str(out_print_main) or "Q2-y-Bin=4," in str(out_print_main)) else 5 if("Q2-xB-Bin=5," in str(out_print_main) or "Q2-y-Bin=5," in str(out_print_main)) else 6 if("Q2-xB-Bin=6," in str(out_print_main) or "Q2-y-Bin=6," in str(out_print_main)) else 7 if("Q2-xB-Bin=7," in str(out_print_main) or "Q2-y-Bin=7," in str(out_print_main)) else 8 if("Q2-xB-Bin=8," in str(out_print_main) or "Q2-y-Bin=8," in str(out_print_main)) else 9 if("Q2-xB-Bin=9," in str(out_print_main) or "Q2-y-Bin=9," in str(out_print_main)) else 10 if("Q2-xB-Bin=10," in str(out_print_main) or "Q2-y-Bin=10," in str(out_print_main)) else 11 if("Q2-xB-Bin=11," in str(out_print_main) or "Q2-y-Bin=11," in str(out_print_main)) else 12 if("Q2-xB-Bin=12," in str(out_print_main) or "Q2-y-Bin=12," in str(out_print_main)) else 13 if("Q2-xB-Bin=13," in str(out_print_main) or "Q2-y-Bin=13," in str(out_print_main)) else 14 if("Q2-xB-Bin=14," in str(out_print_main) or "Q2-y-Bin=14," in str(out_print_main)) else 15 if("Q2-xB-Bin=15," in str(out_print_main) or "Q2-y-Bin=15," in str(out_print_main)) else 16 if("Q2-xB-Bin=16," in str(out_print_main) or "Q2-y-Bin=16," in str(out_print_main)) else 17 if("Q2-xB-Bin=17," in str(out_print_main) or "Q2-y-Bin=17," in str(out_print_main)) else 18 if("Q2-xB-Bin=18," in str(out_print_main) or "Q2-y-Bin=18," in str(out_print_main)) else "Undefined..."
            if("Q2-xB-Bin=All" in str(out_print_main) or "Q2-y-Bin=All," in str(out_print_main)):
                Q2_xB_Bin_Unfold = 0
            elif(any(str(f"{BinType}=-3,") in str(out_print_main) for BinType in ["Q2-xB-Bin", "Q2-y-Bin"])):
                Q2_xB_Bin_Unfold = -3
            else:
                for Q2_xB_Bin_Unfold_ii in range(1, 40, 1):
                    if(any(f"{BinType}={Q2_xB_Bin_Unfold_ii}," in str(out_print_main) for BinType in ["Q2-xB-Bin", "Q2-y-Bin"])):
                        Q2_xB_Bin_Unfold = Q2_xB_Bin_Unfold_ii
                        break
                    else:
                        Q2_xB_Bin_Unfold = "Undefined..."

            # print("\n\nQ2_xB_Bin_Unfold =", Q2_xB_Bin_Unfold)
            # print("out_print_main =", out_print_main, "\n\n")

            if(type(Q2_xB_Bin_Unfold) is str):
                print(f"\n{color.Error}ERROR - Q2_xB_Bin_Unfold = {Q2_xB_Bin_Unfold}\n{color.END}Error is with\n out_print_main = {out_print_main}")

            if((str(Q2_xB_Bin_Unfold) not in Q2_xB_Bin_List) and ("Multi_Dim_Q2_y_Bin_phi_t" not in str(out_print_main))):
                # print("Skipping unselected Q2-xB Bin...")
                print(f"Bin {Q2_xB_Bin_Unfold} is not in Q2_xB_Bin_List = {Q2_xB_Bin_List}")
                continue

            count += 1
            print(f"\nUnfolding: {out_print_main}")
            ExREAL_1D_initial     = rdf.Get(out_print_main_rdf)
            MC_REC_1D_initial     = mdf.Get(out_print_main_mdf_1D)
            MC_GEN_1D_initial     = gdf.Get(out_print_main_gdf)
            Response_2D_initial   = mdf.Get(out_print_main_mdf)
            if((tdf not in ["N/A"]) and out_print_main_tdf):
                ExTRUE_1D_initial = tdf.Get(out_print_main_tdf)
            else:
                ExTRUE_1D_initial = None
            if("mdf" in str(ExREAL_1D_initial.GetName())):
                print("\n    ExREAL_1D_initial.GetName() =", ExREAL_1D_initial.GetName())
                ExREAL_1D_initial.SetName(str(ExREAL_1D_initial.GetName()).replace("mdf", "rdf"))
                print("New ExREAL_1D_initial.GetName() =",   ExREAL_1D_initial.GetName())


            ExREAL_1D_initial.SetTitle(str(ExREAL_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
            MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
            MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
            Response_2D_initial.SetTitle(str(Response_2D_initial.GetTitle()).replace("with Proton Cuts", ""))

            # Getting MC Background Histogram (bgs - stands for BackGroundSubtraction)
            out_print_main_bdf_1D = out_print_main_mdf_1D.replace("'Response_Matrix_1D'",        "'Background_Response_Matrix_1D'")
            out_print_main_bdf_1D = out_print_main_bdf_1D.replace("'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'")
            # out_print_main_bdf_1D = out_print_main_bdf_1D.replace("'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_Normal_1D'")
            if(((out_print_main_bdf_1D in mdf.GetListOfKeys()) or (out_print_main_bdf_1D in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf_1D))):
                MC_BGS_1D_initial = mdf.Get(out_print_main_bdf_1D) if(not Sim_Test) else rdf.Get(out_print_main_bdf_1D)
                # print(f"{color.BLUE}\n\nout_print_main_bdf_1D = {out_print_main_bdf_1D}{color.END}")
                # print(f"{color.BOLD}\nMC_BGS_1D_initial  -> {MC_BGS_1D_initial.GetName()}{color.END}")
                # print(f"{color.BOLD}MC_REC_1D_initial  -> {MC_REC_1D_initial.GetName()}{color.END}\n")
            else:
                MC_BGS_1D_initial = "None"
                print(f"\n{color.Error}ERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
                raise TypeError("Missing Background Histogram")
            if(Sim_Test and (str(MC_BGS_1D_initial) not in ["None"])):
                # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                ExREAL_1D_initial.Add(MC_BGS_1D_initial)
                
            # Use_Gen_MM_Cut = True
            Use_Gen_MM_Cut = False

            if(("Gen_MM_Cut" in str(out_print_main_rdf)) or ("Gen_MM_Cut" in str(out_print_main_mdf_1D)) or ("Gen_MM_Cut" in str(out_print_main_gdf))  or ("Gen_MM_Cut" in str(out_print_main_mdf))):
                if((not Use_Gen_MM_Cut) and (Common_Name not in ["Gen_Cuts_V7_All"])):
                    print(f"\n{color.Error}ERROR: NOT TRYING TO RUN Gen_MM_Cut{color.END}\n")
                    continue
                print(f"{color.BBLUE}INCLUDES Gen_MM_Cut{color.END}")
                # print("out_print_main_rdf    =", out_print_main_rdf)
                # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                # print("out_print_main_gdf    =", out_print_main_gdf)
                # print("out_print_main_mdf    =", out_print_main_mdf)

                # if(Use_Gen_MM_Cut):
                if(abs(Response_2D_initial.GetZaxis().GetXmin()) == abs(Response_2D_initial.GetZaxis().GetXmax()) == 1.5):                    
                    Response_2D_initial = Response_2D_initial.Project3D("yx e")
                    Response_2D_initial.SetTitle(str(Response_2D_initial.GetTitle()).replace(" yx projection", ""))
                else:
                    print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut Response Matrix\n{color.END}Response_2D_initial = {Response_2D_initial}")
                    raise TypeError("ERROR WITH Gen_MM_Cut Response Matrix")

                if("3D" in str(type(MC_REC_1D_initial))):
                    if(abs(MC_REC_1D_initial.GetZaxis().GetXmin()) == abs(MC_REC_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        MC_REC_1D_initial = MC_REC_1D_initial.Project3D("yx e")
                        MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" yx projection", ""))
                    else:
                        print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC REC HISTO\n{color.END}MC_REC_1D_initial = {MC_REC_1D_initial}")
                        raise TypeError("ERROR WITH Gen_MM_Cut MC REC HISTO")
                else:
                    if(abs(MC_REC_1D_initial.GetYaxis().GetXmin()) == abs(MC_REC_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                        MC_REC_1D_initial = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()), 0, -1, "e")
                        MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" x projection", ""))
                    else:
                        print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC REC HISTO\n{color.END}MC_REC_1D_initial = {MC_REC_1D_initial}")
                        raise TypeError("ERROR WITH Gen_MM_Cut MC REC HISTO")

                if("3D" in str(type(MC_GEN_1D_initial))):
                    if(abs(MC_GEN_1D_initial.GetZaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        MC_GEN_1D_initial = MC_GEN_1D_initial.Project3D("yx e")
                        MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" yx projection", ""))
                    else:
                        print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC GEN HISTO\n{color.END}MC_GEN_1D_initial = {MC_GEN_1D_initial}")
                        raise TypeError("ERROR WITH Gen_MM_Cut MC GEN HISTO")
                else:
                    if(abs(MC_GEN_1D_initial.GetYaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                        MC_GEN_1D_initial = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()), 0, -1, "e")
                        MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" x projection", ""))
                    else:
                        print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC GEN HISTO\n{color.END}MC_GEN_1D_initial = {MC_GEN_1D_initial}")
                        raise TypeError("ERROR WITH Gen_MM_Cut MC GEN HISTO")

                if((tdf not in ["N/A"]) and ExTRUE_1D_initial):
                    if("3D" in str(type(ExTRUE_1D_initial))):
                        if(abs(ExTRUE_1D_initial.GetZaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            ExTRUE_1D_initial = ExTRUE_1D_initial.Project3D("yx e")
                            ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" yx projection", ""))
                        else:
                            print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC TRUE HISTO\n{color.END}ExTRUE_1D_initial = {ExTRUE_1D_initial}")
                            raise TypeError("ERROR WITH Gen_MM_Cut MC TRUE HISTO")
                    else:
                        if(abs(ExTRUE_1D_initial.GetYaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                            ExTRUE_1D_initial = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()), 0, -1, "e")
                            ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" x projection", ""))
                        else:
                            print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC TRUE HISTO\n{color.END}ExTRUE_1D_initial = {ExTRUE_1D_initial}")
                            raise TypeError("ERROR WITH Gen_MM_Cut MC TRUE HISTO")

                if(MC_BGS_1D_initial != "None"):
                    if("3D" in str(type(MC_BGS_1D_initial))):
                        if(abs(MC_BGS_1D_initial.GetZaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            MC_BGS_1D_initial = MC_BGS_1D_initial.Project3D("yx e")
                            MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" yx projection", ""))
                        else:
                            print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC BGS HISTO\n{color.END}MC_BGS_1D_initial = {MC_BGS_1D_initial}")
                            raise TypeError("ERROR WITH Gen_MM_Cut MC BGS HISTO")
                    else:
                        if(abs(MC_BGS_1D_initial.GetYaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                            MC_BGS_1D_initial = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()), 0, -1, "e")
                            MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" x projection", ""))
                        else:
                            print(f"\n\n{color.Error}ERROR WITH Gen_MM_Cut MC BGS HISTO\n{color.END}MC_BGS_1D_initial = {MC_BGS_1D_initial}")
                            raise TypeError("ERROR WITH Gen_MM_Cut MC BGS HISTO")

            elif(Common_Name in ["Gen_Cuts_V7_All"]):
                if("3D" in str(type(ExREAL_1D_initial))):
                    # print(color.BBLUE, "\n\n\n\nExREAL_1D_initial.GetZaxis().GetTitle() =", ExREAL_1D_initial.GetZaxis().GetTitle(), color.END)
                    # print("out_print_main_rdf    =", out_print_main_rdf)
                    # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                    # print("out_print_main_gdf    =", out_print_main_gdf)
                    # print("out_print_main_mdf    =", out_print_main_mdf)
                    if(abs(ExREAL_1D_initial.GetZaxis().GetXmin()) == abs(ExREAL_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        ExREAL_1D_initial = ExREAL_1D_initial.Project3D("yx e")
                        ExREAL_1D_initial.SetTitle(str(ExREAL_1D_initial.GetTitle()).replace(" yx projection", ""))
                if("3D" in str(type(MC_REC_1D_initial))):
                    # print(color.Error, "\n\n\n\nMC_REC_1D_initial.GetZaxis().GetTitle() =", MC_REC_1D_initial.GetZaxis().GetTitle(), color.END)
                    # print("out_print_main_rdf    =", out_print_main_rdf)
                    # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                    # print("out_print_main_gdf    =", out_print_main_gdf)
                    # print("out_print_main_mdf    =", out_print_main_mdf)
                    if(abs(MC_REC_1D_initial.GetZaxis().GetXmin()) == abs(MC_REC_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        MC_REC_1D_initial = MC_REC_1D_initial.Project3D("yx e")
                        MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" yx projection", ""))
                    # print("MC_REC_1D_initial.GetTitle() =", MC_REC_1D_initial.GetTitle())
                if("3D" in str(type(MC_GEN_1D_initial))):
                    # print(color.BGREEN, "\n\n\n\nMC_GEN_1D_initial.GetZaxis().GetTitle() =", MC_GEN_1D_initial.GetZaxis().GetTitle(), color.END)
                    # print("out_print_main_rdf    =", out_print_main_rdf)
                    # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                    # print("out_print_main_gdf    =", out_print_main_gdf)
                    # print("out_print_main_mdf    =", out_print_main_mdf)
                    if(abs(MC_GEN_1D_initial.GetZaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        MC_GEN_1D_initial = MC_GEN_1D_initial.Project3D("yx e")
                        MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" yx projection", ""))
                    # print("MC_GEN_1D_initial.GetTitle() =", MC_GEN_1D_initial.GetTitle())
                if((tdf not in ["N/A"]) and ExTRUE_1D_initial):
                    if("3D" in str(type(ExTRUE_1D_initial))):
                        if(abs(ExTRUE_1D_initial.GetZaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            ExTRUE_1D_initial = ExTRUE_1D_initial.Project3D("yx e")
                            ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" yx projection", ""))

                if(MC_BGS_1D_initial != "None"):
                    if("3D" in str(type(MC_BGS_1D_initial))):
                        if(abs(MC_BGS_1D_initial.GetZaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            MC_BGS_1D_initial = MC_BGS_1D_initial.Project3D("yx e")
                            MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" yx projection", ""))

            # print("\n\n")
            # print("".join(["ExREAL_1D_initial[", str(ExREAL_1D_initial.GetName()), "]: \n\t\t", str(type(ExREAL_1D_initial)), "\n"]))
            # print("".join(["MC_REC_1D_initial[", str(out_print_main_mdf_1D), "]: \n\t\t", str(type(MC_REC_1D_initial)), "\n"]))
            # print("".join(["MC_GEN_1D_initial[", str(MC_GEN_1D_initial.GetName()), "]: \n\t\t", str(type(MC_GEN_1D_initial)), "\n"]))
            # print("".join(["Response_2D_initial[", str(Response_2D_initial.GetName()), "]: \n\t\t", str(type(Response_2D_initial)), "\n"]))



    ###############################################################################################
    ###############################################################################################
    ###==========##==========###     z-pT Binning Dimensions Slice     ###==========##==========###


            z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All"     in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3] or ("Binning-Type='3'" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [4]) else 36 if(Q2_xB_Bin_Unfold in [5]) else 25 if(Q2_xB_Bin_Unfold in [6, 7]) else 20 if(Q2_xB_Bin_Unfold in [8]) else 1

            if(any(binning in Binning_Method for binning in ["y"])):
                z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin_Unfold in [4])           else 36 if(Q2_xB_Bin_Unfold in [5, 8, 9, 11, 12]) else 30 if(Q2_xB_Bin_Unfold in [6, 10])       else 25 if(Q2_xB_Bin_Unfold in [13])     else 1
                z_pT_Bin_Range = 0
                z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin_Unfold in [4])           else 36 if(Q2_xB_Bin_Unfold in [5, 8, 9])         else 30 if(Q2_xB_Bin_Unfold in [6, 10, 11])   else 25 if(Q2_xB_Bin_Unfold in [13, 14]) else 20 if(Q2_xB_Bin_Unfold in [12, 15, 16, 17]) else 1

                z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [2])          else 36 if(Q2_xB_Bin_Unfold in [4, 5, 9, 10]) else 35 if(Q2_xB_Bin_Unfold in [1, 3])            else 30 if(Q2_xB_Bin_Unfold in [6, 7, 8, 11]) else 25 if(Q2_xB_Bin_Unfold in [13, 14]) else 20 if(Q2_xB_Bin_Unfold in [12, 15, 16, 17]) else 1

            if("Y_bin" in Binning_Method):
                z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_xB_Bin_Unfold)[1]

            for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
                if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                    if(((Q2_xB_Bin_Unfold in [1, 2]) and (z_pT_Bin_Unfold in [49])) or (Q2_xB_Bin_Unfold == 3 and z_pT_Bin_Unfold in [49, 48, 42]) or (Q2_xB_Bin_Unfold in [1, 4] and z_pT_Bin_Unfold in [42]) or (Q2_xB_Bin_Unfold == 5 and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold == 7 and z_pT_Bin_Unfold in [25])):
                        continue
                elif(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_xB_Bin_Unfold, Z_PT_BIN=z_pT_Bin_Unfold, BINNING_METHOD=Binning_Method)):
                    continue
                # elif("Y_bin" not in Binning_Method):
                #     # if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [42, 48, 49])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [42, 49])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [7, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [6, 7, 14, 28, 35, 41, 42]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [7, 35, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [8] and z_pT_Bin_Unfold in [5, 6, 36]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [24, 29, 30]) or (Q2_xB_Bin_Unfold in [11, 12] and z_pT_Bin_Unfold in [30, 35, 36])  or (Q2_xB_Bin_Unfold in [13] and z_pT_Bin_Unfold in [5, 20, 24, 25])):
                #     #     # print("Testing z_pT_Bin_Unfold...")
                #     #     continue
                #     #
                #     # if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [42, 48, 49])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [42, 49])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [42, 48, 49]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [7, 28, 35, 41, 42]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [7, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [8] and z_pT_Bin_Unfold in [6, 36]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [11] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [14] and z_pT_Bin_Unfold in [25]) or (Q2_xB_Bin_Unfold in [15, 16, 17] and z_pT_Bin_Unfold in [20])):
                #     #     continue
                #     if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [28, 34, 35])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [28, 35, 41, 42])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [28, 35]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [6, 36]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [24, 30]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [11] and z_pT_Bin_Unfold in [24, 30]) or (Q2_xB_Bin_Unfold in [13, 14] and z_pT_Bin_Unfold in [25]) or (Q2_xB_Bin_Unfold in [15, 16, 17] and z_pT_Bin_Unfold in [20])):
                #         continue

                # # For Selecting specific z-pT Bins
                # if(z_pT_Bin_Unfold not in [0, 10]):
                #     continue

        #########################################################
        ##===============##     3D Slices     ##===============##

                if("3D" in str(type(Response_2D_initial))):
                    try:
                        # bin_Response_2D_0, bin_Response_2D_1 = Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else Response_2D_initial.GetNbinsZ())
                        bin_Response_2D_0, bin_Response_2D_1 = Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else Response_2D_initial.GetNbinsZ())
                        if(z_pT_Bin_Unfold != 0):
                            Response_2D_initial.GetZaxis().SetRange(bin_Response_2D_0, bin_Response_2D_1)
                        Response_2D           = Response_2D_initial.Project3D('yx e')
                        Response_2D.SetName(str(Response_2D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])))
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        else:
                            Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        if((Pass_Version not in [""]) and (Pass_Version not in Response_2D_Title_New)):
                            Response_2D_Title_New = "".join(["#splitline{", str(Response_2D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                        Response_2D.SetTitle(Response_2D_Title_New)
                        # print(str(Response_2D.GetTitle()))
                    except:
                        print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (Response_2D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                else:
                    Response_2D = Response_2D_initial

        ##===============##     3D Slices     ##===============##
        #########################################################


        #########################################################
        ##===============##     2D Slices     ##===============##
                if("2D" in str(type(ExREAL_1D_initial))):
                    try:
                        # bin_ExREAL_1D_0, bin_ExREAL_1D_1 = ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExREAL_1D_initial.GetNbinsY())
                        bin_ExREAL_1D_0, bin_ExREAL_1D_1 = ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExREAL_1D_initial.GetNbinsY())
                        ExREAL_1D                        = ExREAL_1D_initial.ProjectionX(str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExREAL_1D_0, bin_ExREAL_1D_1, "e")
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        else:
                            ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        if((Pass_Version not in [""]) and (Pass_Version not in ExREAL_1D_Title_New)):
                            ExREAL_1D_Title_New          = "".join(["#splitline{", str(ExREAL_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                        ExREAL_1D.SetTitle(ExREAL_1D_Title_New)
                    except:
                        print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (ExREAL_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
                else:
                    # print("\nExREAL_1D already is a 1D Histogram...")
                    ExREAL_1D = ExREAL_1D_initial

                if("2D" in str(type(MC_REC_1D_initial))):
                    try:
                        # bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                        bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                        MC_REC_1D                        = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_REC_1D_0, bin_MC_REC_1D_1, "e")
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        else:
                            MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        if((Pass_Version not in [""]) and (Pass_Version not in MC_REC_1D_Title_New)):
                            MC_REC_1D_Title_New          = "".join(["#splitline{", str(MC_REC_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                        MC_REC_1D.SetTitle(MC_REC_1D_Title_New)
                    except:
                        print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (ExREAL_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                else:
                    # print("\nMC_REC_1D already is a 1D Histogram...")
                    MC_REC_1D = MC_REC_1D_initial


                if(MC_BGS_1D_initial != "None"):
                    if("2D" in str(type(MC_BGS_1D_initial))):
                        try:
                            # bin_MC_BGS_1D_0, bin_MC_BGS_1D_1 = MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_BGS_1D_initial.GetNbinsY())
                            bin_MC_BGS_1D_0, bin_MC_BGS_1D_1 = MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_BGS_1D_initial.GetNbinsY())
                            MC_BGS_1D                        = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_BGS_1D_0, bin_MC_BGS_1D_1, "e")
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                            else:
                                MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                            if((Pass_Version not in [""]) and (Pass_Version not in MC_BGS_1D_Title_New)):
                                MC_BGS_1D_Title_New          = "".join(["#splitline{", str(MC_BGS_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                            MC_BGS_1D.SetTitle(MC_BGS_1D_Title_New)
                        except:
                            print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (MC_BGS_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                    else:
                        # print("\nMC_BGS_1D already is a 1D Histogram...")
                        MC_BGS_1D = MC_BGS_1D_initial
                else:
                    MC_BGS_1D = MC_BGS_1D_initial


                if("2D" in str(type(MC_GEN_1D_initial))):
                    try:
                        # bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                        bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                        MC_GEN_1D                        = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_GEN_1D_0, bin_MC_GEN_1D_1, "e")
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        else:
                            MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        if((Pass_Version not in [""]) and (Pass_Version not in MC_GEN_1D_Title_New)):
                            MC_GEN_1D_Title_New          = "".join(["#splitline{", str(MC_GEN_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                        MC_GEN_1D.SetTitle(MC_GEN_1D_Title_New)
                    except:
                        print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (MC_GEN_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                else:
                    # print("\nMC_GEN_1D already is a 1D Histogram...")
                    MC_GEN_1D = MC_GEN_1D_initial

                if((tdf not in ["N/A"]) and ExTRUE_1D_initial):
                    if("2D" in str(type(ExTRUE_1D_initial))):
                        try:
                            # bin_ExTRUE_1D_0, bin_ExTRUE_1D_1 = ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExTRUE_1D_initial.GetNbinsY())
                            bin_ExTRUE_1D_0, bin_ExTRUE_1D_1 = ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExTRUE_1D_initial.GetNbinsY())
                            ExTRUE_1D                        = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExTRUE_1D_0, bin_ExTRUE_1D_1, "e")
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            else:
                                ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            if((Pass_Version not in [""]) and (Pass_Version not in ExTRUE_1D_Title_New)):
                                ExTRUE_1D_Title_New          = "".join(["#splitline{", str(ExTRUE_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                            ExTRUE_1D_Title_New        = str(str(ExTRUE_1D_Title_New.replace("Generated",                  "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                            ExTRUE_1D_Title_X_Axis_New = str(str(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Generated", "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                            ExTRUE_1D.SetTitle(ExTRUE_1D_Title_New)
                            ExTRUE_1D.GetXaxis().SetTitle(ExTRUE_1D_Title_X_Axis_New)
                        except:
                            print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (ExTRUE_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                    else:
                        # print("\nExTRUE_1D already is a 1D Histogram...")
                        ExTRUE_1D = ExTRUE_1D_initial
                        ExTRUE_1D_Title_New            = str(str(str(ExTRUE_1D.GetTitle()).replace("Generated",            "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                        if((Pass_Version not in [""]) and (Pass_Version not in ExTRUE_1D_Title_New)):
                            ExTRUE_1D_Title_New        = "".join(["#splitline{", str(ExTRUE_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(Pass_Version), "}}}"])
                        ExTRUE_1D_Title_X_Axis_New     = str(str(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Generated", "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                        ExTRUE_1D.SetTitle(ExTRUE_1D_Title_New)
                        ExTRUE_1D.GetXaxis().SetTitle(ExTRUE_1D_Title_X_Axis_New)
                else:
                    ExTRUE_1D = "N/A"
        ##===============##     2D Slices     ##===============##
        #########################################################


    ###==========##==========###     z-pT Binning Dimensions Slice     ###==========##==========###
    ###############################################################################################
    ###############################################################################################


                if((z_pT_Bin_Unfold   != 0)                            and (("Combined_"                 in out_print_main) or ("Multi_Dim_Q2"       in out_print_main))):
                    continue
                if(((Q2_xB_Bin_Unfold == 0) or (z_pT_Bin_Unfold != 0)) and ("Multi_Dim_z_pT_Bin"         in out_print_main)):
                    continue
                if(((Q2_xB_Bin_Unfold == 0) or (z_pT_Bin_Unfold != 0)) and ("MultiDim_z_pT_Bin"          in out_print_main)):
                    continue
                if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("Combined_"                 in out_print_main) or ("Multi_Dim_Q2_phi_t" in out_print_main))):
                    continue
                if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("MultiDim_Q2_y_z_pT_phi_h"  in out_print_main))):
                    continue
                # if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'Multi_Dim" not in out_print_main)):
                # if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'MM" not in out_print_main) and ("'W" not in out_print_main)):
                if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'W" not in out_print_main) and ("'Multi_Dim" not in out_print_main) and ("'MultiDim_Q2_y_z_pT_phi_h" not in out_print_main) and ("'MultiDim_z_pT_Bin_Y_bin_phi_t" not in out_print_main)):
                    print(f"\nADDING CUTS FOR: {out_print_main}\n")

                    if("'MM" not in out_print_main):
                        if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("Combined_phi_t" not in out_print_main) and ("Multi_Dim" not in out_print_main))):
                            # Do not plot other variables that are not phi_t
                            continue

                        # Extra Y-Bins in 2D Histogram:
                        for ybin in range(0, Response_2D.GetYaxis().GetNbins() + 2, 1):
                            Response_2D.SetBinContent(0, ybin, 0)
                            if("'pT'" not in out_print_main and "'pT_smeared'" not in out_print_main):
                                Response_2D.SetBinContent(1, ybin, 0)

                        try:
                            # Extra Bins in 1D Histogram:
                            ExREAL_1D.SetBinContent(0, 0)
                            MC_REC_1D.SetBinContent(0, 0)
                            MC_GEN_1D.SetBinContent(0, 0)
                            ExREAL_1D.SetBinContent(ExREAL_1D.GetNbinsX() + 1, 0)
                            MC_REC_1D.SetBinContent(MC_REC_1D.GetNbinsX() + 1, 0)
                            MC_GEN_1D.SetBinContent(MC_GEN_1D.GetNbinsX() + 1, 0)
                            if(MC_BGS_1D != "None"):
                                MC_BGS_1D.SetBinContent(MC_BGS_1D.GetNbinsX() + 1, 0)
                            if(tdf not in ["N/A"]):
                                ExTRUE_1D.SetBinContent(ExTRUE_1D.GetNbinsX() + 1, 0)
                            if("'pT'" not in out_print_main and "'pT_smeared'" not in out_print_main):
                                ExREAL_1D.SetBinContent(1, 0)
                                MC_REC_1D.SetBinContent(1, 0)
                                MC_GEN_1D.SetBinContent(1, 0)
                                if(MC_BGS_1D != "None"):
                                    MC_BGS_1D.SetBinContent(1, 0)
                                if(tdf not in ["N/A"]):
                                    ExTRUE_1D.SetBinContent(1, 0)
                        except:
                            print(f"{color.RED}ERROR IN SETTING BIT CONTENTS{color.END}")
                            print(type(MC_REC_1D))

                    # else:
                    #     # Missing Mass Cut on Response Matrix (Gen)
                    #     for xbin in range(0, Response_2D.GetXaxis().GetNbins() + 2, 1):
                    #         if(Response_2D.GetXaxis().GetBinCenter(xbin) > 1.5):
                    #             print("Done with MM Cuts...")
                    #             break
                    #         for ybin in range(0, Response_2D.GetYaxis().GetNbins() + 2, 1):
                    #             Response_2D.SetBinContent(xbin, ybin, 0)
                    #     # for ybin in range(0, Response_2D.GetYaxis().GetNbins() + 2, 1):
                    #     #     Response_2D.SetBinContent(Response_2D.GetXaxis().FindBin(3.5) + 1, ybin, 0)
                    #     # Cut on gdf histogram
                    #     for xbin in range(0, MC_GEN_1D.GetNbinsX() + 1, 1):
                    #         if(MC_GEN_1D.GetBinCenter(xbin) > 1.5):
                    #             print("Done with MM Cuts...")
                    #             break
                    #         else:
                    #             MC_GEN_1D.SetBinContent(xbin, 0)
                    #     # MC_GEN_1D.SetBinContent(MC_GEN_1D.FindBin(3.5) + 1, 0)
                    #     # Cut on mdf histogram
                    #     for xbin in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                    #         if(MC_REC_1D.GetBinCenter(xbin) > 1.5):
                    #             print("Done with MM Cuts...")
                    #             break
                    #         else:
                    #             MC_REC_1D.SetBinContent(xbin, 0)
                    #     # MC_REC_1D.SetBinContent(MC_REC_1D.FindBin(3.5) + 1, 0)
                    #     # Cut on rdf histogram
                    #     for xbin in range(0, ExREAL_1D.GetNbinsX() + 1, 1):
                    #         if(ExREAL_1D.GetBinCenter(xbin) > 1.5):
                    #             print("Done with MM Cuts...")
                    #             break
                    #         else:
                    #             ExREAL_1D.SetBinContent(xbin, 0)
                    #     # ExREAL_1D.SetBinContent(ExREAL_1D.FindBin(3.5) + 1, 0)


                # if(Sim_Test):
                #     print(color.BOLD, "\n\nFor 'Sim_Test' of 'out_print_main' =", color.BLUE,  str(out_print_main),        color.END)
                #     print(color.BOLD, "\t'out_print_main_rdf'    =",              color.GREEN, str(out_print_main_rdf),    color.END)
                #     print(color.BOLD, "\t'out_print_main_mdf_1D' =",              color.GREEN, str(out_print_main_mdf_1D), color.END)
                #     print(color.BOLD, "\t'out_print_main_tdf'    =",              color.CYAN,  str(out_print_main_tdf),    color.END)
                #     for xbin in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                #         MC_REC_1D_Content = MC_REC_1D.GetBinContent(xbin)
                #         ExREAL_1D_Content = ExREAL_1D.GetBinContent(xbin)
                #         if(0 not in [MC_REC_1D_Content, ExREAL_1D_Content, MC_REC_1D_Content - ExREAL_1D_Content]):
                #             print("\t\tDifference (smear - unsmear) in Bin", xbin, " =", str(round(((MC_REC_1D_Content - ExREAL_1D_Content)/ExREAL_1D_Content)*100, 4)), "% of Unsmeared")
                #         else:
                #             print("\t\tDifference (smear - unsmear) in Bin", xbin, " =", str(round(MC_REC_1D_Content - ExREAL_1D_Content, 4)))
                #     print("\n\n")

                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("Cut: No Cuts",     "")).replace("Cut:  No Cuts", ""))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace("Cut: No Cuts", "")).replace("Cut:  No Cuts", ""))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))


                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                ExREAL_1D.GetXaxis().SetTitle(str((str(ExREAL_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                MC_REC_1D.GetXaxis().SetTitle(str((str(MC_REC_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("_{t}",                 "_{h}")))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace("_{t}",                                   "_{h}")))
                    ExTRUE_1D.GetXaxis().SetTitle((str(ExTRUE_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("_{t}", "_{h}")))
                Response_2D.GetXaxis().SetTitle(str((str(Response_2D.GetXaxis().GetTitle()).replace("_{t}",         "_{h}")).replace(") (", " - ")))
                Response_2D.GetYaxis().SetTitle(str((str(Response_2D.GetYaxis().GetTitle()).replace("_{t}",         "_{h}")).replace(") (", " - ")))


                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2",                           "#phi_{h}+Q^{2}-x_{B} Bin"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2",     "#phi_{h}+Q^{2}-x_{B} Bin"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2",                           "#phi_{h}+Q^{2}-x_{B} Bin"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2",     "#phi_{h}+Q^{2}-x_{B} Bin"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2",                           "#phi_{h}+Q^{2}-x_{B} Bin"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2",     "#phi_{h}+Q^{2}-x_{B} Bin"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2",                       "#phi_{h}+Q^{2}-x_{B} Bin"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("phi_t_Q2_xB_Bin_2",                       "#phi_{h}+Q^{2}-x_{B} Bin"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin"))


                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3",                           "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3",     "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3",                           "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3",     "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3",                           "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3",     "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3",                       "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("phi_t_Q2_xB_Bin_3",                       "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)"))


                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_y_Bin",                              "#phi_{h}+Q^{2}-y Bin"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",        "#phi_{h}+Q^{2}-y Bin"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_y_Bin",                              "#phi_{h}+Q^{2}-y Bin"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",        "#phi_{h}+Q^{2}-y Bin"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_y_Bin",                              "#phi_{h}+Q^{2}-y Bin"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",        "#phi_{h}+Q^{2}-y Bin"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("phi_t_Q2_y_Bin",                          "#phi_{h}+Q^{2}-y Bin"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",    "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("phi_t_Q2_y_Bin",                          "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",    "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_y_Bin",    "#phi_{h}+Q^{2}-y Bin"))

                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Q2_y_Bin_phi_t",                              "#phi_{h}+Q^{2}-y Bin"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",        "#phi_{h}+Q^{2}-y Bin"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("Q2_y_Bin_phi_t",                              "#phi_{h}+Q^{2}-y Bin"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",        "#phi_{h}+Q^{2}-y Bin"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("Q2_y_Bin_phi_t",                              "#phi_{h}+Q^{2}-y Bin"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",        "#phi_{h}+Q^{2}-y Bin"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("Q2_y_Bin_phi_t",                          "#phi_{h}+Q^{2}-y Bin"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",    "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Q2_y_Bin_phi_t",                          "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",    "#phi_{h}+Q^{2}-y Bin"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("Q2_y_Bin_phi_t",    "#phi_{h}+Q^{2}-y Bin"))


                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Q2_phi_t",                                    "#phi_{h}+Q^{2}"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("Q2_phi_t",              "#phi_{h}+Q^{2}"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("Q2_phi_t",                                    "#phi_{h}+Q^{2}"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("Q2_phi_t",              "#phi_{h}+Q^{2}"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("Q2_phi_t",                                    "#phi_{h}+Q^{2}"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("Q2_phi_t",              "#phi_{h}+Q^{2}"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("Q2_phi_t",                                "#phi_{h}+Q^{2}"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",          "#phi_{h}+Q^{2}"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Q2_phi_t",                                "#phi_{h}+Q^{2}"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("Q2_phi_t",          "#phi_{h}+Q^{2}"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("Q2_phi_t",          "#phi_{h}+Q^{2}"))


                ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("phi_t_Q2",                                    "#phi_{h}+Q^{2}"))
                ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",              "#phi_{h}+Q^{2}"))
                MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("phi_t_Q2",                                    "#phi_{h}+Q^{2}"))
                MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",              "#phi_{h}+Q^{2}"))
                MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2",                                    "#phi_{h}+Q^{2}"))
                MC_GEN_1D.GetXaxis().SetTitle(str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",              "#phi_{h}+Q^{2}"))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("Q2_phi_t",                                "#phi_{h}+Q^{2}"))
                    ExTRUE_1D.GetXaxis().SetTitle(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",          "#phi_{h}+Q^{2}"))
                Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("phi_t_Q2",                                "#phi_{h}+Q^{2}"))
                Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2",          "#phi_{h}+Q^{2}"))
                Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2",          "#phi_{h}+Q^{2}"))


                Q2_Bin_Range         = "Range: 1.4805 #rightarrow 11.8705 - Size: 0.5195 per bin"
                Q2_Bin_Replace_Range = "Range: 1.48 #rightarrow 11.87 GeV^{2} - Size: 0.52 GeV^{2}/bin"
                # xB_Bin_Range         = "Range: 0.082643 #rightarrow 0.82643 - Size: 0.0368 per bin"
                # xB_Bin_Replace_Range = "Range: 0.083 #rightarrow 0.83 - Size: 0.0368/bin"
                xB_Bin_Range         = "Range: 0.08977 #rightarrow 0.82643 - Size: 0.0368 per bin"
                xB_Bin_Replace_Range = "Range: 0.0898 #rightarrow 0.826 - Size: 0.0368/bin"
                z_Bin_Range          = "Range: 0.11944 #rightarrow 0.73056 - Size: 0.0306 per bin"
                z_Bin_Replace_Range  = "Range: 0.12 #rightarrow 0.73 - Size: 0.0306/bin"
                pT_Bin_Range         = "Range: 0 #rightarrow 1.05 - Size: 0.0525 per bin"
                pT_Bin_Replace_Range = "Range: 0 #rightarrow 1.05 GeV - Size: 0.0525 GeV/bin"


                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))


                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))


                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))


                ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                if("N/A" not in [tdf, ExTRUE_1D]):
                    ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
                Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))


                if("Var-D1='Q2" in out_print_main):
                    ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                    MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                    MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                    Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                    Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV^{2}]"]))


                if("Var-D1='pT" in out_print_main):
                    ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                    MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                    MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV]"]))
                    Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV]"]))
                    Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV]"]))


                for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                    ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace(range_strings,     ""))
                    MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace(range_strings,     ""))
                    MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace(range_strings,     ""))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace(range_strings, ""))
                    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace(range_strings, ""))
                if(MC_BGS_1D != "None"):
                    MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))
                    # print(f"{color.BOLD}MC_BGS_1D  -> {MC_BGS_1D.GetName()}{color.END}")
                    # print(f"{color.BOLD}MC_REC_1D  -> {MC_REC_1D.GetName()}{color.END}")


                # continue
                List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold, MC_BGS_1D=MC_BGS_1D)
                continue




##===============##     Unfolding Histogram Procedure     ##===============##
#############################################################################




print(f"Total: {count}")
# print("".join(["Num Failed: ", str(count_failed)]))
del count




BIN_SEARCH = []
for BIN in Q2_xB_Bin_List:
    BIN_SEARCH.append("".join(["Q2_y_Bin_", str(BIN) if(str(BIN) not in ['0', 0]) else "All", ")"]))
    
for ii in rdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
        out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
        out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
        out_print_str     = out_print_str.replace("_smeared",              "")
        out_print_str     = out_print_str.replace("'smear'",               "Smear")
        SEARCH = []
        for BIN in BIN_SEARCH:
            SEARCH.append(str(BIN) in str(out_print_str))
            if(str(BIN) in str(out_print_str)):
                break
        out_print_str     = out_print_str.replace("mdf",                   "rdf")
        if(True in SEARCH):
            List_of_All_Histos_For_Unfolding[out_print_str] = rdf.Get(str(out_print_main))
            if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                for particle in ["el", "pip"]:
                    if(f"({particle})_({particle}th)"    in str(out_print_str)):
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                    elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                    else:
                        continue
                    num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                    out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                    out_print_str_1D_Binned         = out_print_str_1D.replace(f"({particle})_",    "")
                    List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                    if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                        out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                    else:
                        out_print_str_1D_Binned_Mom = "N/A"
                    for ii in range(4, num_z_pT_bins + 1):
                        z_pT_bin_value = ii - 4
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                        List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
            
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if(("Normal_2D" in out_print_main) or ("Normal_Background_2D" in out_print_main)):
        out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
        out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
        out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
        out_print_str     = out_print_str.replace("_smeared",              "")
        out_print_str     = out_print_str.replace("'smear'",               "Smear")
        SEARCH = []
        for BIN in BIN_SEARCH:
            SEARCH.append(str(BIN) in str(out_print_str))
            if(str(BIN) in str(out_print_str)):
                break
        if(True in SEARCH):
            List_of_All_Histos_For_Unfolding[out_print_str] = mdf.Get(out_print_main)
            if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                if("Normal_Background_2D" in out_print_main):
                    continue
                for particle in ["el", "pip"]:
                    if(f"({particle})_({particle}th)"    in str(out_print_str)):
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                    elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                        List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                    else:
                        continue
                    num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                    out_print_str_1D = str(out_print_str.replace("(Normal_2D)",               "(1D)"))
                    out_print_str_1D = str(out_print_str_1D.replace("(Normal_Background_2D)", "(Background_1D)"))
                    out_print_str_1D_Binned = out_print_str_1D.replace(f"({particle})_",    "")
                    List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                    if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                        out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                    for ii in range(4, num_z_pT_bins + 1):
                        z_pT_bin_value = ii - 4
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                        List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
            
if(Cor_Compare):
    print(f"{color.Error}\nCorrection Comparison Plot Option selected does NOT include the Generated MC Plots{color.END_R} (as of 4-18-2024){color.END}\n")
else:
    for ii in gdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
            out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
            out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
            out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
            out_print_str     = out_print_str.replace("_smeared",              "")
            out_print_str     = out_print_str.replace("'smear'",               "Smear")
            SEARCH = []
            for BIN in BIN_SEARCH:
                SEARCH.append(str(BIN) in str(out_print_str))
                if(str(BIN) in str(out_print_str)):
                    break
            if(True in SEARCH):
                List_of_All_Histos_For_Unfolding[out_print_str] = gdf.Get(out_print_main)
                if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                    for particle in ["el", "pip"]:
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        else:
                            continue
                        num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                        out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                        out_print_str_1D_Binned         = out_print_str_1D.replace(f"({particle})_",    "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                        if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                            out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                        for ii in range(4, num_z_pT_bins + 1):
                            z_pT_bin_value = ii - 4
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)

            
            
if(tdf not in ["N/A"]):
    for ii in tdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
            out_print_str = out_print_str.replace("_(cut_Complete_SIDIS)", "")
            out_print_str = out_print_str.replace("cut_Complete_SIDIS_",   "")
            out_print_str = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
            out_print_str = out_print_str.replace("_smeared",              "")
            out_print_str = out_print_str.replace("'smear'",               "Smear")
            SEARCH = []
            for BIN in BIN_SEARCH:
                SEARCH.append(str(BIN) in str(out_print_str))
                if(str(BIN) in str(out_print_str)):
                    break
            if(True in SEARCH):
                List_of_All_Histos_For_Unfolding[out_print_str.replace("gdf", "tdf")] = tdf.Get(out_print_main)
                if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                    for particle in ["el", "pip"]:
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        else:
                            continue
                        num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                        out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                        out_print_str_1D_Binned         = out_print_str_1D.replace(f"({particle})_",    "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                        if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                            out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                        for ii in range(4, num_z_pT_bins + 1):
                            z_pT_bin_value = ii - 4
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
            

# Bin-by-Bin Acceptance Corrections for 2D Histograms
if(Cor_Compare):
    print(f"{color.Error}\nCorrection Comparison Plot Option selected does NOT include Unfolding/Acceptance Corrections{color.END_R} (as of 4-18-2024){color.END}\n")
else:
    for ii in mdf.GetListOfKeys():
        try:
            out_print_main = str(ii.GetName())
            if(("Normal_2D" in out_print_main) and (not any(f"{cut}_eS" in out_print_main for cut in ["cut_Complete_SIDIS", "no_cut", "cut_Complete_SIDIS_Proton", "no_cut_Integrate", "cut_Complete_SIDIS_Integrate", "cut_Complete_SIDIS_Proton_Integrate"]))):
                mdf_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
                mdf_print_str     = mdf_print_str.replace("_(cut_Complete_SIDIS)",           "")
                mdf_print_str     = mdf_print_str.replace("cut_Complete_SIDIS_",             "")
                mdf_print_str     = mdf_print_str.replace("(gdf)_(no_cut)",                  "(gdf)")
                mdf_print_str     = mdf_print_str.replace("_smeared",                        "")
                mdf_print_str     = mdf_print_str.replace("'smear'",                         "Smear")
                if(not Sim_Test):
                    rdf_print_str = str(mdf_print_str.replace("mdf", "rdf")).replace("Smear", "''")
                else:
                    rdf_print_str = str(mdf_print_str.replace("mdf", "rdf"))
                gdf_print_str     = str(mdf_print_str.replace("mdf", "gdf")).replace("Smear", "''")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(no_cut)",                  "(gdf)")
                for sector_cut_remove in range(1, 7):
                    gdf_print_str = gdf_print_str.replace(f"(gdf)_(eS{sector_cut_remove}o)", "(gdf)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Proton)",                  "(gdf)")
                # gdf_print_str     = gdf_print_str.replace(f"(gdf)_(no_cut_Integrate)",       "(gdf)_(Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Integrate)",               "(gdf)_(no_cut_Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Proton_Integrate)",        "(gdf)_(no_cut_Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(RevPro)",                  "(gdf)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(RevPro_Integrate)",        "(gdf)_(no_cut_Integrate)")
                # print(f"gdf_print_str = {gdf_print_str}")
                SEARCH = []
                for BIN in BIN_SEARCH:
                    SEARCH.append(str(BIN) in str(mdf_print_str))
                    if(str(BIN) in str(mdf_print_str)):
                        break
                if(True in SEARCH):
                    Histo_MDF = List_of_All_Histos_For_Unfolding[mdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[mdf_print_str].GetName()), "_Clone"]))
                    Histo_RDF = List_of_All_Histos_For_Unfolding[rdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[rdf_print_str].GetName()), "_Clone"]))
                    Histo_GDF = List_of_All_Histos_For_Unfolding[gdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[gdf_print_str].GetName()), "_Clone"]))

                    Histo_BBB        = Histo_RDF.Clone(str(mdf_print_str).replace("mdf", "bbb"))
                    Histo_Acceptance = Histo_MDF.Clone(str(mdf_print_str).replace("mdf", "Acceptance"))
                    Histo_Acceptance.Sumw2()

                    if((Histo_MDF.GetNbinsX() != Histo_GDF.GetNbinsX()) or (Histo_MDF.GetNbinsY() != Histo_GDF.GetNbinsY()) or (Histo_MDF.GetNbinsZ() != Histo_GDF.GetNbinsZ())):
                        print(color.RED, "Histograms have different binning!", color.END)
                        print("\nHisto_MDF =",             str(mdf_print_str))
                        print("\tHisto_MDF (type) =",      str(type(Histo_MDF)))
                        print("\tHisto_MDF (Title - X) =", str(Histo_MDF.GetXaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - X) =",   str(Histo_MDF.GetNbinsX()))
                        print("\tHisto_MDF (Title - Y) =", str(Histo_MDF.GetYaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - Y) =",   str(Histo_MDF.GetNbinsY()))
                        print("\tHisto_MDF (Title - Z) =", str(Histo_MDF.GetZaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - Z) =",   str(Histo_MDF.GetNbinsZ()))

                        print("\nHisto_RDF =",             str(rdf_print_str))
                        print("\tHisto_RDF (type) =",      str(type(Histo_RDF)))
                        print("\tHisto_RDF (Title - X) =", str(Histo_RDF.GetXaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - X) =",   str(Histo_RDF.GetNbinsX()))
                        print("\tHisto_RDF (Title - Y) =", str(Histo_RDF.GetYaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - Y) =",   str(Histo_RDF.GetNbinsY()))
                        print("\tHisto_RDF (Title - Z) =", str(Histo_RDF.GetZaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - Z) =",   str(Histo_RDF.GetNbinsZ()))

                        print("\nHisto_GDF =",             str(gdf_print_str))
                        print("\tHisto_GDF (type) =",      str(type(Histo_GDF)))
                        print("\tHisto_GDF (Title - X) =", str(Histo_GDF.GetXaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - X) =",   str(Histo_GDF.GetNbinsX()))
                        print("\tHisto_GDF (Title - Y) =", str(Histo_GDF.GetYaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - Y) =",   str(Histo_GDF.GetNbinsY()))
                        print("\tHisto_GDF (Title - Z) =", str(Histo_GDF.GetZaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - Z) =",   str(Histo_GDF.GetNbinsZ()))

                    Histo_Acceptance.Divide(Histo_GDF)
                    Histo_BBB.Divide(Histo_Acceptance)
                    Histo_BBB.SetName(str(mdf_print_str).replace("mdf", "bbb"))
                    List_of_All_Histos_For_Unfolding[mdf_print_str.replace("mdf", "bbb")] = Histo_BBB
        except:
            print(f"{color.Error}ERROR! See:{color.END_B}\n\tBin-by-Bin Acceptance Corrections for 2D Histograms{color.END}")
            print(f"Traceback:\n{traceback.format_exc()}")
            
            
# # Creating set of relative background plots
# temp_list_of_background_histos = {}
# for Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
#     Conditions_List = [not False]
#     if("_(Background" in str(Histos_For_Unfolding_ii)):
#         Conditions_List = [str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf") in List_of_All_Histos_For_Unfolding]
#     if("Normal_Background_2D" in str(Histos_For_Unfolding_ii)):
#         Conditions_List = [str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D") in List_of_All_Histos_For_Unfolding]
#     if(False not in Conditions_List):
#         hist_temp = List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].Clone()
#         hist_temp.SetName(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetName()).replace("'Background", "'Relative_Background"))
#         hist_temp.SetTitle(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetTitle()).replace("BACKGROUND", "Relative Background"))
#         if("_(Background" in str(Histos_For_Unfolding_ii)):
#             hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf")])
#         else:
#             hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D")])
#         if("1D"    in str(type(hist_temp))):
#             hist_temp.GetYaxis().SetTitle("#frac{Background}{MC Reconstructed}")
#         elif("2D" in str(type(hist_temp))):
#             hist_temp.GetZaxis().SetTitle("#frac{Background}{MC Reconstructed}")
#         if("_(Background" in str(Histos_For_Unfolding_ii)):
#             temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("_(Background",         "_(Relative_Background")]         = hist_temp
#         else:
#             temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_Relative_Background_2D")] = hist_temp
# for adding_hist in temp_list_of_background_histos:
#     if(adding_hist not in List_of_All_Histos_For_Unfolding):
#         List_of_All_Histos_For_Unfolding[adding_hist] = temp_list_of_background_histos[adding_hist]
#     else:
#         print(f"{color.Error}ERROR:{color.END_R} adding_hist = {adding_hist}{color.Error} is already in 'List_of_All_Histos_For_Unfolding'{color.END}")
# del temp_list_of_background_histos

final_count = 0
#Search comment find
print("\n\nCounting Total Number of collected histograms...")
if(Saving_Q):
    print(f"{color.BBLUE}Saving to: {color.BGREEN}{args.root}{color.END}")
    output_file = ROOT.TFile(args.root, "UPDATE")
    File_Name_Lists = [str(Common_Name), str(REAL_File_Name), str(MC_REC_File_Name), str(MC_GEN_File_Name)]
    File_Name_Tlist = ROOT.TList() # Convert to a ROOT TList of TObjString
    File_Name_Tlist.SetName("Latest_List_of_File_Names")  # Name in the ROOT file
    for s in File_Name_Lists:
        File_Name_Tlist.Add(ROOT.TObjString(s))
    safe_write(File_Name_Tlist, output_file)
    # File_Name_Tlist.Write()
else:
    print(f"{color.PINK}Would be saving to: {color.BCYAN}{args.root}{color.END}")
    output_file = None
    
for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
    final_count += 1
    if(not Saving_Q):
        # if(any(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["(Q2)_(y)", "(Q2)_(xB)", "(z)_(pT)"])):
        #     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
        print(f"\n{List_of_All_Histos_For_Unfolding_ii} --> {type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
        # if(type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]) is list):
        #     print(f"\n{List_of_All_Histos_For_Unfolding_ii} --> {type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
        #     # print(f"len  -> {len(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
        #     # print(f"list -> {List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]}")
        #     # for ii in List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]:
        #     #     print(f"{ii} -> {type(ii)}")
        #     # print("")
    else:
        if(type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]) is list):
            Temp_Tlist = ROOT.TList()
            Temp_Tlist.SetName(f"TList_of_{List_of_All_Histos_For_Unfolding_ii}" if(not args.EvGen) else f"TList_of_{List_of_All_Histos_For_Unfolding_ii}_EvGen")  # Name in the ROOT file
            for s in List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]:
                Temp_Tlist.Add(ROOT.TObjString(str(s) if(not args.EvGen) else f"{str(s)}_EvGen"))
            safe_write(Temp_Tlist, output_file)
        else:
            List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii].SetName(List_of_All_Histos_For_Unfolding_ii if(not args.EvGen) else f"{List_of_All_Histos_For_Unfolding_ii}_EvGen")
            safe_write(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii], output_file)
if(Saving_Q):
    print(f"{color.BBLUE}Done Saving...{color.END}\n")
    output_file.Close()

print(f"\nFinal Count = {final_count}")
# del final_count

    
# timer.stop(count_label="Histos", count_value=final_count)

start_time = timer.start_find(return_Q=True)
start_time = start_time.replace("Ran", "Started running")
end_time, total_time, rate_line = timer.stop(count_label="Histograms", count_value=final_count, return_Q=True)

email_body = f"""
The 'Just_RooUnfold_SIDIS_richcap.py' script has finished running.
{start_time}

Ran with the following options:

Output File:
\t{args.root}
    
Arguments:
--test                                              --> {args.test}
--bayes_iterations                                  --> {args.bayes_iterations}
--Num_Toys                                          --> {args.Num_Toys}
--Min_Allowed_Acceptance_Cut                        --> {args.Min_Allowed_Acceptance_Cut}
--bins   (Q2-y Bins)                                --> {Q2_xB_Bin_List}
--title    (added title)                            --> {args.title}
--EvGen                                             --> {args.EvGen}
--smear                                             --> {args.smear}
--no-smear                                          --> {args.no_smear}
--simulation (unfolding synthetic data)             --> {args.sim}
--modulation (data unfolded with modulated MC)      --> {args.mod}
--closure  (modulated MC unfolded with itself)      --> {args.closure}
--weighed_acceptace (use acceptance weights only)   --> {args.weighed_acceptace}
--fit                                               --> {args.fit}
--txt                                               --> {args.txt}
--stat                                              --> {args.stat}
--cor-compare                                       --> {args.cor_compare}
--tag-proton                                        --> {args.tag_proton}
--cut-proton                                        --> {args.cut_proton}
--Common_Int_Bins                                   --> {args.Common_Int_Bins}
--single_file                                       --> {args.single_file}
--single_file_input                                 --> {args.single_file_input}

"""
if(args.email_message):
    email_body = f"""{email_body}
Extra Message:
\t{args.email_message}

"""
else:
    email_body = f"""{email_body}

"""

email_body = f"""{email_body}
{end_time}
{total_time}
{rate_line}
"""

if(args.email):
    send_email(subject="Finished Running the 'Just_RooUnfold_SIDIS_richcap.py' Code", body=email_body, recipient="richard.capobianco@uconn.edu")

print(email_body)


print(f"""{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

