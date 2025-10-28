#!/usr/bin/env python3

import sys
import ROOT
import math

# Turns off the canvases when running in the command line
ROOT.gROOT.SetBatch(1)

import traceback
import os
# import re

from MyCommonAnalysisFunction_richcap    import *
from Convert_MultiDim_Kinematic_Bins     import *
from Fit_Related_Functions_For_RooUnfold import *


timer = RuntimeTimer()
timer.start()


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
def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    subprocess.run(["mail", "-s", subject, recipient], input=body.encode(), check=False)

import argparse

def parse_args():
    p = argparse.ArgumentParser(description="Multi5D_Bayes_RooUnfold_SIDIS_dedicated_script.py analysis script:\n\tMeant for JUST doing the 5D (Bayesian) Unfolding Procedure before saving outputs to a ROOT file.",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save', action='store_true', dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root', type=str, default="Unfolded_5D_Histos_From_Multi5D_Bayes_RooUnfold_SIDIS_dedicated_script.root",
                   help="Name of ROOT output file to be saved.")
    # # smearing selection
    # grp_smear = p.add_mutually_exclusive_group()
    # grp_smear.add_argument('-smear',    '--smear',    action='store_true',
    #                        help="Unfold with smeared Monte Carlo only")
    # grp_smear.add_argument('-no-smear', '--no-smear', action='store_true',
    p.add_argument('-no-smear', '--no-smear', action='store_true',
                   help="Unfold with unsmeared Monte Carlo only (Defaults to just using Smearing only).")

    # simulation / modulation / closure
    p.add_argument('-sim', '--simulation', action='store_true', dest='sim',
                   help="Use reconstructed MC instead of experimental data.")
    p.add_argument('-mod', '--modulation', action='store_true', dest='mod',
                   help="Use modulated MC files to create response matrices.")
    # p.add_argument('-close', '--closure',  action='store_true', dest='closure',
    #                help="Run Closure Test (unfold modulated MC with unweighted matrices).")

    # # fitting / output control
    # p.add_argument('-nf', '--no-fit', action='store_true', dest='no_fit',
    #                help="Disable fitting of plots.")
    # p.add_argument('-txt', '--txt',   action='store_true', dest='txt',
    #                help="Create a txt output file.")
    # p.add_argument('-stat', '--stat', action='store_true', dest='stat',
    #                help="Create a (stats) txt output file.")

    # # kinematic comparison & proton modes
    # p.add_argument('-tp', '--tag-proton',  action='store_true', dest='tag_proton',
    #                help="Use 'Tagged Proton' files.")
    # p.add_argument('-cp', '--cut-proton',  action='store_true', dest='cut_proton',
    #                help="Use 'Cut with Proton Missing Mass' files.")

    # p.add_argument('-cib', '-CIB', '--Common_Int_Bins', action='store_true',
    #                help="If given then the code will only run the z-pT bins that have been designated to share the same ranges of z-pT (given by Common_Ranges_for_Integrating_z_pT_Bins). Otherwise, the code will run normally and include all z-pT bins for the given Q2-y bin.")

    p.add_argument('-bi', '-bayes-it', '--bayes_iterations', type=int, default=4,
                   help="Number of Bayesian Iterations performed while Unfolding (Must use to change the number of iterations).")
    
    p.add_argument('-title', '--title', type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-evgen', '--EvGen', action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut', type=float, default=0.005,
                   help="Cut made on acceptance (as the minimum acceptance before a bin is removed from unfolding).")

    # # positional Q2-y bin arguments
    # p.add_argument('bins', nargs='*', metavar='BIN',
    #                help="List of Q2-y bin indices to run. '0' means all bins.")
    p.add_argument('-b', '--bins', nargs="+", type=str, default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
                   help="List of Q2-y bin indices to run.")

    p.add_argument('-v', '--verbose', action='store_true',
                   help="Prints each Histogram name to be saved.")

    return p.parse_args()

args = parse_args()


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

       
Saving_Q         = not args.test
Fit_Test         = False
Sim_Test         = args.sim
Mod_Test         = args.mod
Smearing_Options = "no_smear" if(args.no_smear) else "smear"


if(Saving_Q):
    print(f"\n{color.BBLUE}Will be saving results to {color.END_B}{args.root}{color.END}\n")
else:
    print(f"\n{color.RED}Will {color.Error}NOT{color.END_R} be saving results (running as a test)\n{color.END_b}Would have saved to {color.END_B}{args.root}{color.END}\n")


Standard_Histogram_Title_Addition = ""
if(Sim_Test):
    print(f"{color.BLUE}\nRunning Simulated Test\n{color.END}")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
if(Mod_Test):
    print(f"{color.BLUE}\nUsing {color.BOLD}Modulated {color.END_b} Monte Carlo Files (to create the response matrices)\n {color.END}")
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"{Standard_Histogram_Title_Addition} - Using Modulated Response Matrix"
    else:
        Standard_Histogram_Title_Addition = "Closure Test - Using Modulated Response Matrix"

if(args.title):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{{args.title}}}"
    else:
        Standard_Histogram_Title_Addition = args.title
    print(f"\nAdding the following extra title to the histograms:\n\t{Standard_Histogram_Title_Addition}\n")
    
# if(not Fit_Test):
#     print(f"\n\n{color.BBLUE}{color_bg.RED}\n\n    Not Fitting Plots    \n{color.END}\n\n")

print(color.BBLUE, "\nSmear option selected is:", "No Smear" if(str(Smearing_Options) in ["", "no_smear"]) else str(Smearing_Options.replace("_s", "S")).replace("s", "S"), color.END, "\n")

File_Save_Format = ".png"
# File_Save_Format = ".root"
# File_Save_Format = ".pdf"

if((File_Save_Format != ".png") and Saving_Q):
    print(f"\n{color.BGREEN}Save Option was not set to output .png files. Save format is: {color.ERROR}{File_Save_Format}{color.END}\n")


# # 'Binning_Method' is defined in 'MyCommonAnalysisFunction_richcap'

Q2_y_Bin_List = args.bins # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']

if(Q2_y_Bin_List != ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']):
    print(f"\n{color.BOLD}Running with the following Q2-y Bins:\t{color.GREEN}{Q2_y_Bin_List}{color.END}\n")

print(f"\n{color.BOLD}Starting RG-A SIDIS Analysis{color.END}\n\n")




########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loading Data Files     ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################



def FileLocation(FileName, Datatype):
    # location = "Histo_Files_ROOT/"
    location = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/"

    if(str(Datatype) == 'rdf'):
        file = "".join(["REAL_Data/SIDIS_epip_Data_REC_",         str(FileName), ".root"])
    if(str(Datatype) == 'mdf'):
        file = "".join(["Matching_REC_MC/SIDIS_epip_MC_Matched_", str(FileName), ".root"])
    if(str(Datatype) == 'gdf'):
        file = "".join(["GEN_MC/SIDIS_epip_MC_GEN_",              str(FileName), ".root"])
        
    loading = "".join([location, file])
    
    return loading



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
Common_Name = "Pass_2_5D_Unfold_Test_V6_All"
Common_Name = "Pass_2_5D_Unfold_Test_V7_All"
Common_Name = "5D_Unfold_Test_V7_All"

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


# Use unique file(s) for one of datatypes? (If so, set the following if(...) conditions to 'False')

##################################
##   Real (Experimental) Data   ##
##################################
if(True):
#     print(f"\n{color.BOLD}Not using the common file name for the Real (Experimental) Data...{color.END}\n")
# if(False):
    REAL_File_Name = Common_Name
else:
    REAL_File_Name = "Unfolding_Tests_V11_All"
    REAL_File_Name = "Pass_2_Correction_Effects_V1_5197"
    REAL_File_Name = "Pass_2_5D_Unfold_Test_V3_All" if("Pass 2" in Pass_Version) else "5D_Unfold_Test_V3_All"
    REAL_File_Name = "Pass_2_5D_Unfold_Test_V7_All" if("Pass 2" in Pass_Version) else "5D_Unfold_Test_V7_All"
    
##################################
##   Real (Experimental) Data   ##
##################################

########################################
##   Reconstructed Monte Carlo Data   ##
########################################
if(args.mod):
    MC_REC_File_Name = "Pass_2_Acceptance_Tests_FC_14_V1_DataWeight_All"
else:
    if(True):
        print(f"\n{color.BOLD}Not using the common file name for the Reconstructed Monte Carlo Data...{color.END}\n")
    if(False):
        MC_REC_File_Name = Common_Name
    else:
        MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V5_All" if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V5_All"
        MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V7_All" if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V7_All"
        MC_REC_File_Name = f"Unsmeared_{Common_Name}" if(Smearing_Options in ["no_smear"]) else Common_Name
        if(Pass_Version not in ["Pass 2"]):
            MC_REC_File_Name = MC_REC_File_Name.replace("Pass_2_", "")
########################################
##   Reconstructed Monte Carlo Data   ##
########################################

####################################
##   Generated Monte Carlo Data   ##
####################################
if(args.mod):
    MC_GEN_File_Name = "Pass_2_Acceptance_Tests_V1_DataWeight_All"
else:
    if(True):
        print(f"\n{color.BOLD}Not using the common file name for the Generated Monte Carlo Data...{color.END}\n")
    if(False):
        MC_GEN_File_Name = Common_Name
    else:
        MC_GEN_File_Name = "Unfolding_Tests_V11_All"
        MC_GEN_File_Name = "Gen_Cuts_V2_Fixed_All"
        MC_GEN_File_Name = "Pass_2_5D_Unfold_Test_V4_All" if("Pass 2" in Pass_Version) else "5D_Unfold_Test_V4_All"
        MC_GEN_File_Name = "Pass_2_5D_Unfold_Test_V7_All" if("Pass 2" in Pass_Version) else "5D_Unfold_Test_V7_All"
        for ii in range(0, 10, 1):
            if(Common_Name   not in [str(Common_Name).replace(f"_FC{ii}_",   "_")]):
                MC_GEN_File_Name   = str(Common_Name).replace(f"_FC{ii}_",   "_")
                break
            elif(Common_Name not in [str(Common_Name).replace(f"_FC_1{ii}_", "_")]):
                MC_GEN_File_Name   = str(Common_Name).replace(f"_FC_1{ii}_", "_")
                break
            else:
                MC_GEN_File_Name = Common_Name
####################################
##   Generated Monte Carlo Data   ##
####################################



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################










###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################
try:
    rdf = ROOT.TFile(str(FileLocation(str(REAL_File_Name), "rdf")), "READ")
    print("".join(["The total number of histograms available for the", color.BLUE,  " Real (Experimental) Data       ", color.END, " in '", color.BOLD, REAL_File_Name,   color.END, "' is ", color.BOLD, str(len(rdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
    print("".join(["The total number of histograms available for the", color.RED,   " Reconstructed Monte Carlo Data ", color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
    print("".join(["The total number of histograms available for the", color.GREEN, " Generated Monte Carlo Data     ", color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################

print(f"\n\n{color.BOLD}Done Loading RDataFrame files...{color.END}\n")



########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loaded Data Files      ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################



to_be_saved_count = 0

start_time = timer.start_find(return_Q=True)
start_time = start_time.replace("Ran", "Started running")
end_time, total_time, rate_line = timer.stop(count_label="Histograms", count_value=to_be_saved_count, return_Q=True)

email_body = f"""
The 'Assign_Uncertainties_to_unfolding.py' script has finished running.
{start_time}

Ran with the following options:
Common_Name      = {Common_Name}
REAL_File_Name   = {REAL_File_Name}
MC_REC_File_Name = {MC_REC_File_Name}
MC_GEN_File_Name = {MC_GEN_File_Name}

Arguments:
--test                         --> {args.test}
--root (Output File Name)      --> {args.root}
--no-smear                     --> {args.no_smear}
--simulation (synthetic data?) --> {args.sim}
--modulation (added to MC?)    --> {args.mod}
--bayes_iterations             --> {args.bayes_iterations}
--title  (added title)         --> {args.title}
--EvGen                        --> {args.EvGen}
--Min_Allowed_Acceptance_Cut   --> {args.Min_Allowed_Acceptance_Cut}
--bins   (Q2-y Bins)           --> {args.bins}
--verbose                      --> {args.verbose}

{end_time}
{total_time}
{rate_line}
"""
# send_email(subject="Finished Running 5D Unfolding Code", body=email_body, recipient="richard.capobianco@uconn.edu")
print(email_body)

timer.stop(count_label="Histos", count_value=to_be_saved_count)


print(f"""{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

