#!/usr/bin/env python

import sys


print("Starting...\n")

from datetime import datetime
# datetime_object_full = datetime.now() # Getting Current Date

# from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT
# import math


import faulthandler
faulthandler.enable(all_threads=True)
print("faulthandler enabled:", faulthandler.is_enabled())


from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

# Turns off the canvases when running in the command line --> (1) is off, (0) is on
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

try:
    import RooUnfold
except ImportError:
    print(f"{color.Error}ERROR: \n{color.END_R}{traceback.format_exc()}{color.END}\n")
    # print("Somehow the python module was not found, let's try loading the library by hand...")
    # try:
    #     ROOT.gSystem.Load("libRooUnfold.so")
    # except:
    #     print("".join([color.Error, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))


# if Common_Int_Bins = True, then the code will only run the z-pT bins that have been designated to share the same ranges of z-pT (given by Common_Ranges_for_Integrating_z_pT_Bins)
                # if = False, then the code will run normally and include all z-pT bins for the given Q2-y bin
Common_Int_Bins  = not True

Saving_Q         = True
Sim_Test         = False
Mod_Test         = False
Tag_ProQ         = False
Cut_ProQ         = False
Closure_Test     = False
Fit_Test         = True
Create_txt_File  = True
Create_stat_File = not True
Cor_Compare      = False
Smearing_Options = "both"

Apply_RC = True
if(Apply_RC):
    print(f"\n{color.BYELLOW}Running with RC Corrections (from EvGen){color.END}\n")

Use_TTree        = True # Uses pre-existing unfolded plots stored in a TTree to create the images (skips the rest of the unfolding process)
if(Use_TTree):
    TTree_Name   = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap.root"
    TTree_Name   = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut.root"
    # TTree_Name   = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_No_Acceptance_Cut.root"
    TTree_Name   = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_No_Acceptance_Cut_AND_Errors_done_with_kCovToy.root"
    TTree_Name   = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut_AND_Errors_done_with_kCovToy.root"

    

if(len(sys.argv) > 1):
    arg_option_1 = str(sys.argv[1])
    if(arg_option_1 in ["test", "Test", "time", "Time"]):
        print("\nNOT SAVING\n")
        Saving_Q = False
    else:
        print("".join(["\nOption Selected: ", str(arg_option_1), " (Still Saving...)" if("no_save" not in str(arg_option_1)) else " (NOT SAVING)"]))
        Saving_Q         = True  if("no_save" not in str(arg_option_1)) else False
        Sim_Test         = True  if(("sim"        in str(arg_option_1)) or ("simulation"    in str(arg_option_1))) else False
        Mod_Test         = True  if(("mod"        in str(arg_option_1)) or ("modulation"    in str(arg_option_1))) else False
        Closure_Test     = True  if(("close"      in str(arg_option_1)) or ("closure"       in str(arg_option_1))  or ("Closure" in str(arg_option_1)) or ("Closure" in str(arg_option_1))) else False
        Fit_Test         = True  if("no_fit"  not in str(arg_option_1)) else False
        Create_txt_File  = False if("no_txt"      in str(arg_option_1)) else True if("txt"  in str(arg_option_1)) else Create_txt_File
        Create_stat_File = False if("no_stat"     in str(arg_option_1)) else True if("stat" in str(arg_option_1)) else (Create_stat_File and Create_txt_File)
        Cor_Compare      = True  if(any(compare   in str(arg_option_1) for compare in ["cor_compare", "Cor_Compare", "CC"])) else False
        Cut_ProQ         = True  if(any(taggedP   in str(arg_option_1) for taggedP in ["Cutpro",      "MMproC",      "CP"])) else False
        Tag_ProQ         = True  if(any(taggedP   in str(arg_option_1) for taggedP in ["proton",      "tagged",      "TP"])  or Cut_ProQ) else False
        if(Closure_Test):
            Sim_Test = True
            Mod_Test = False
        arg_option_1     = arg_option_1.replace("_simulation", "")
        arg_option_1     = arg_option_1.replace("_sim",        "")
        arg_option_1     = arg_option_1.replace("simulation",  "")
        arg_option_1     = arg_option_1.replace("sim",         "")
        arg_option_1     = arg_option_1.replace("_modulation", "")
        arg_option_1     = arg_option_1.replace("_mod",        "")
        arg_option_1     = arg_option_1.replace("modulation",  "")
        arg_option_1     = arg_option_1.replace("mod",         "")
        arg_option_1     = arg_option_1.replace("_closure",    "")
        arg_option_1     = arg_option_1.replace("_close",      "")
        arg_option_1     = arg_option_1.replace("closure",     "")
        arg_option_1     = arg_option_1.replace("close",       "")
        arg_option_1     = arg_option_1.replace("_Closure",    "")
        arg_option_1     = arg_option_1.replace("_Close",      "")
        arg_option_1     = arg_option_1.replace("Closure",     "")
        arg_option_1     = arg_option_1.replace("Close",       "")
        arg_option_1     = arg_option_1.replace("_no_fit",     "")
        arg_option_1     = arg_option_1.replace("no_fit",      "")
        arg_option_1     = arg_option_1.replace("_no_txt",     "")
        arg_option_1     = arg_option_1.replace("no_txt",      "")
        arg_option_1     = arg_option_1.replace("_txt",        "")
        arg_option_1     = arg_option_1.replace("txt",         "")
        arg_option_1     = arg_option_1.replace("_no_stat",    "")
        arg_option_1     = arg_option_1.replace("no_stat",     "")
        arg_option_1     = arg_option_1.replace("_stat",       "")
        arg_option_1     = arg_option_1.replace("stat",        "")
        for compare in ["cor_compare", "Cor_Compare", "CC"]:
            arg_option_1 = arg_option_1.replace(f"_{compare}", "")
            arg_option_1 = arg_option_1.replace(f"{compare}",  "")
        for taggedP in ["proton", "tagged", "TP", "Cutpro", "MMproC", "CP"]:
            arg_option_1 = arg_option_1.replace(f"_{taggedP}", "")
            arg_option_1 = arg_option_1.replace(f"{taggedP}",  "")
        Smearing_Options = str((arg_option_1).replace("_no_save", "")).replace("no_save", "") if(str(arg_option_1) not in ["save", ""]) else "both"
        if(Smearing_Options == ""):
            Smearing_Options = "both"
        if(("no_smear" in [str(Smearing_Options)]) or ("no_smear" in str(arg_option_1))):
            Smearing_Options = "no_smear"
        if(Smearing_Options in ["_smear", "Smear", "_Smear"]):
            Smearing_Options = "smear"
else:
    Saving_Q = True
    
Standard_Histogram_Title_Addition = ""
if(Closure_Test):
    print(f"\n{color.BLUE}Running Closure Test (Unfolding the Modulated MC using the unweighted response matrices){color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Modulated Simulation"
elif(Sim_Test):
    print(f"\n{color.BLUE}Running Simulated Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
if(Mod_Test):
    print(f"\n{color.BLUE}Using {color.BOLD}Modulated{color.END_b} Monte Carlo Files (to create the response matrices){color.END}\n")
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = "".join([str(Standard_Histogram_Title_Addition), " - Using Modulated Response Matrix"])
    else:
        Standard_Histogram_Title_Addition = "Closure Test - Using Modulated Response Matrix"

if(Tag_ProQ):
    Proton_Type = "Tagged Proton" if(not Cut_ProQ) else "Cut with Proton Missing Mass"
    Standard_Histogram_Title_Addition = "".join([Proton_Type, f" - {Standard_Histogram_Title_Addition}" if(Standard_Histogram_Title_Addition not in [""]) else ""])
    print(f"\n{color.BBLUE}Running with the '{color.UNDERLINE}{Proton_Type}{color.END}{color.BBLUE}' Files{color.END}\n")
    del Proton_Type
        
# if((Closure_Test or Sim_Test) and (str(Smearing_Options) not in ["no_smear"])):
if(Closure_Test and (str(Smearing_Options) not in ["no_smear"])):
    print(f"\n{color.BOLD}Unfolding Simulated data for Closure Tests should (probably) not use any additional smearing (forcing choice change)\n{color.END}")
    Smearing_Options = "no_smear"
        
if(Cor_Compare):
    Fit_Test         = False
    Create_txt_File  = False
    Create_stat_File = False
    Smearing_Options = "no_smear"
    # if(Standard_Histogram_Title_Addition not in [""]):
    #     Standard_Histogram_Title_Addition = "".join([str(Standard_Histogram_Title_Addition), " - Kinematic Correction Comparisons"])
    # else:
    #     Standard_Histogram_Title_Addition = "Kinematic Correction Comparisons"

# if(TTree_Name == "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut.root"):
#     if(Standard_Histogram_Title_Addition not in [""]):
#         Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{Used Lower Acceptance Cut}}"
#     else:
#         Standard_Histogram_Title_Addition =  "Used Lower Acceptance Cut"
        
if(TTree_Name == "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_No_Acceptance_Cut.root"):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{Did not use Acceptance Cuts}}"
    else:
        Standard_Histogram_Title_Addition =  "Did not use Acceptance Cuts"
        
if(not Fit_Test):
    print(f"\n\n{color.BBLUE}{color_bg.RED}\n\n    Not Fitting Plots    \n{color.END}\n\n")
    
if(Create_txt_File):
    print(f"{color.BBLUE}\nWill create a txt output file{color.END}")
    if(not Create_stat_File):
        print(f"{color.RED}Will {color.BOLD}NOT{color.END_R} create a (stats) txt output file{color.END}")
    print("")
else:
    print(f"{color.RED}\nWill {color.BOLD}NOT{color.END_R} create a txt output file\n{color.END}")
    

if(Use_TTree and (Sim_Test or Mod_Test)):
    if(Sim_Test):
        TTree_Name = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Synthetic_Data_with_kCovToy.root"
    elif(Mod_Test):
        TTree_Name = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Modulated_Response_with_kCovToy.root"

# if(str(Smearing_Options) not in ["both"]):
print(color.BBLUE, "\nSmear option selected is:", "No Smear" if(str(Smearing_Options) in ["", "no_smear"]) else str(Smearing_Options.replace("_s", "S")).replace("s", "S"), color.END, "\n")

File_Save_Format = ".png"
# File_Save_Format = ".root"
# File_Save_Format = ".pdf"


if((File_Save_Format != ".png") and Saving_Q):
    print(f"\n{color.BGREEN}Save Option was not set to output .png files. Save format is: {color.END_B}{color.UNDERLINE}{File_Save_Format}{color.END}\n")

    
# # How to run code in the commandline:
# # # Step 1) Run these commands before running this code:
#         source /group/clas12/packages/setup.csh
#         source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# # # Step 2) Run this code with the following command (optional inputs are in []): 
#         python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py [saving/smearing options] [list of Q2-xB bins to run]

# # # Possible input options for the above command:
# # # # "saving/smearing" options (include as one word without spaces - use '_' when combining options):
#     1) save                     -->   default option of code - will save all histograms (without options 4 or 5 below, this option will unfold with the smeared monte carlo AND the unsmeared monte carlo)
#     2) test, Test, time, Time   -->   simple options to run full code but without saving any images (do not combine with other options - all of these do the same thing)
#     3) no_save                  -->   same as the above option(s) but can can be added to the end of other options to prevent saving (include as the last part of the option with '_no_save')
#     4) smear                    -->   will unfold with smeared monte carlo files only
#     5) no_smear                 -->   will unfold with normal (unsmeared) monte carlo files only
#     6) sim, simulation          -->   will test the unfolding methods by using the reconstructed monte carlo instead of the experimental data (test should result in the reproduction of the generated distributions)
# # # # "list of Q2-xB bins to run" options (notes):
#     (*) Can select bins numbered 0-8 (0 is for 'All Bins' histograms) - Order does not matter
#         * Separate each bin choice with a space and just use interger numbers
#     (*) Must specify an input for "saving/smearing" (see above) to use these options
#         * Takes from the 2nd arguement and on only (will never take from the 1st arguement after 'RooUnfold_SIDIS_richcap.py')
#     (*) Default option is to run all bins in sequential order
    
    
# # Test code with the command:
# # # python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py test [list of Q2-xB bins to run]


# # 'Binning_Method' is defined in 'MyCommonAnalysisFunction_richcap'
# # Binning_Method = "_y_bin" 

    
Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
if(any(binning in Binning_Method for binning in ["y_bin", "Y_bin"])):
    # Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']

appended_0 = False
if(len(sys.argv) > 2):
    Q2_xB_Bin_List = []
    for ii_bin in range(2, len(sys.argv), 1):
        Q2_xB_Bin_List.append(sys.argv[ii_bin])
    if(Q2_xB_Bin_List == []):
        print("Error")
        Q2_xB_Bin_List = ['1']
    if('0' not in Q2_xB_Bin_List):
        Q2_xB_Bin_List.append('0')
        appended_0 = True
        print(f"\n{color.RED}Running Bin 'All' for Q2-y Bins by default (will skip at end){color.END}\n")
    else:
        appended_0 = False
    print(str(("".join(["\nRunning for Q2-xB/Q2-y Bins: ", str(Q2_xB_Bin_List)]).replace("[", "")).replace("]", "")))
    


if(Common_Int_Bins):
    print(f"\n\n{color.BGREEN}Will ONLY be running the z-pT Bins that have been selected as per the 'Commom Integration Region' given by 'Common_Ranges_for_Integrating_z_pT_Bins'{color.END}\n\n")

print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis\n{color.END}")

timer = RuntimeTimer()
timer.start()

Date_Day = timer.start_find(return_no_time=True)
# # # Getting Current Date
# # datetime_object_full = datetime.now()

# startMin_full = datetime_object_full.minute
# startHr_full  = datetime_object_full.hour
# startDay_full = datetime_object_full.day

# if(datetime_object_full.minute < 10):
#     timeMin_full = f"0{datetime_object_full.minute}"
# else:
#     timeMin_full = str(datetime_object_full.minute)

    
# Date_Day = "".join(["\nStarted running on ", color.BOLD, str(datetime_object_full.month), "-", str(startDay_full), "-", str(datetime_object_full.year), color.END, " at "])
# # Printing Current Time
# Date_Time = Date_Day
# if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
#     Date_Time = "".join([Date_Day, color.BOLD, str((datetime_object_full.hour)-12), ":", timeMin_full, " p.m.", color.END])
# if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
#     Date_Time = "".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " a.m.", color.END])
# if(datetime_object_full.hour == 12):
#     Date_Time = "".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " p.m.", color.END])
# if(datetime_object_full.hour == 0 or  datetime_object_full.hour == 24):
#     Date_Time = "".join([Date_Day, color.BOLD, "12:", str(timeMin_full), " a.m.", color.END])
# print(Date_Time, "\n")

        
# print("\n\n")

# Variable for imposing a minimum acceptance value cut to the unfolded distributions
# Min_Allowed_Acceptance_Cut = 0.0175
Min_Allowed_Acceptance_Cut = 0.005

Min_Allowed_Acceptance_Cut = 0.0005 # Tested with TTree_Name = Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut.root (on 9/22/2025)
# Min_Allowed_Acceptance_Cut = 0.008 # Updated for tests on 9/14/2025

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
    if(Closure_Test):
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
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
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
                print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Same bin used in fits", color.END]))
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

    #         # Above is the 1st Version of the calculation
    #         # Below is the additional versions of the calculation which use different points to solve for parameters B and C using the same value of A
    #         Phi_low_bin = Histo.FindBin(52.5)
    #         Phi_mid_bin = Histo.FindBin(157.5)
    #         Phi_max_bin = Histo.FindBin(262.5)
    #         Phi_low = (3.1415926/180)*Histo.GetBinCenter(Phi_low_bin)
    #         Phi_mid = (3.1415926/180)*Histo.GetBinCenter(Phi_mid_bin)
    #         Phi_max = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
    #         n2 = Histo.GetBinContent(Phi_max_bin)
    #         a2 = ROOT.cos(Phi_max)                # Cos_phi_max
    #         b2 = ROOT.cos(2*Phi_max)              # Cos_2_phi_max
    #         n0 = Histo.GetBinContent(Phi_low_bin)
    #         n1 = Histo.GetBinContent(Phi_mid_bin)
    #         a0 = ROOT.cos(Phi_low)                # Cos_phi_low
    #         a1 = ROOT.cos(Phi_mid)                # Cos_phi_mid
    #         b0 = ROOT.cos(2*Phi_low)              # Cos_2_phi_low
    #         b1 = ROOT.cos(2*Phi_mid)              # Cos_2_phi_mid
    #         numerator_B   = b0*(n1    -    n2) + b1*(n2    - n0)    + b2*(n0    - n1)
    #         denominator_B = a0*(b2*n1 - b1*n2) + b0*(a1*n2 - a2*n0) + n0*(a2*b1 - a1*b2)
    #         numerator_C   = a0*(n1    -    n2) + a1*(n2    - n0)    + a2*(n0    - n1)
    #         denominator_C = a0*(b1*n2 - b2*n1) + b0*(a2*n1 - a1*n2) + n0*(a1*b2 - a2*b1)
    #         if(denominator_B != 0):
    #             B = numerator_B/denominator_B
    #         else:
    #             print(color.RED, "\nError B - V2 - Divide by 0\n", color.END)
    #             B = (1/a2)*((n2/A) - (numerator_C/denominator_C)*b2 - 1)
    #         if(denominator_C != 0):
    #             C = numerator_C/denominator_C
    #         else:
    #             print(color.RED, "\nError C - V2 - Divide by 0\n", color.END)
    #             C = (1/b2)*((n2/A) - B*a2 - 1)
    #         # Above is the 2nd Version of the calculation (for new parameter B)
    #         # Below is the additional versions of the calculation which use different points to solve for parameter C using the same value of A and B
    #         Phi_low_bin = Histo.FindBin(157.5)
    #         Phi_mid_bin = Histo.FindBin(202.5)        
    #         Phi_max_bin = Histo.FindBin(262.5)
    #         Phi_low = (3.1415926/180)*Histo.GetBinCenter(Phi_low_bin)
    #         Phi_mid = (3.1415926/180)*Histo.GetBinCenter(Phi_mid_bin)
    #         Phi_max = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
    #         n2 = Histo.GetBinContent(Phi_max_bin)
    #         a2 = ROOT.cos(Phi_max)                # Cos_phi_max
    #         b2 = ROOT.cos(2*Phi_max)              # Cos_2_phi_max
    #         n0 = Histo.GetBinContent(Phi_low_bin)
    #         n1 = Histo.GetBinContent(Phi_mid_bin)
    #         a0 = ROOT.cos(Phi_low)                # Cos_phi_low
    #         a1 = ROOT.cos(Phi_mid)                # Cos_phi_mid
    #         b0 = ROOT.cos(2*Phi_low)              # Cos_2_phi_low
    #         b1 = ROOT.cos(2*Phi_mid)              # Cos_2_phi_mid
    #         numerator_C   = a0*(n1    -    n2) + a1*(n2    - n0)    + a2*(n0    - n1)
    #         denominator_C = a0*(b1*n2 - b2*n1) + b0*(a2*n1 - a1*n2) + n0*(a1*b2 - a2*b1)
    #         if(denominator_C != 0):
    #             C = numerator_C/denominator_C
    #         else:
    #             print(color.RED, "\nError C - V3 - Divide by 0\n", color.END)
    #             C = (1/b2)*((n2/A) - B*a2 - 1)

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
    if(Closure_Test):
        B_opt, C_opt = -0.500, 0.025
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    # elif(Sim_Test):
    #     B_opt, C_opt = 0, 0
    #     Histo_max_bin     = Histo.GetMaximumBin()
    #     Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
    #     Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
    #     A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
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
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)

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










def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default", MC_BGS_1D="None"):#, Test_Bayes_Iterations=False):
    
##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Original)   #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    if(Method in ["SVD"]):
        print("".join([color.BOLD_C, "Starting ", color.UNDERLINE, color.BLUE, "SVD", color.END_B, color.CYAN, " Unfolding Procedure...", color.END]))
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
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
                        
        Covariance_Matrix = ROOT.TH2D("".join(["statcov_", str(Name_Main)]), "".join(["Covariance Matrix for: ", str(Name_Main)]), nBins_CVM, MinBinCVM, MaxBinCVM, nBins_CVM, MinBinCVM, MaxBinCVM)
        
        #######################################################################################
        ##==========##==========##   Filling the Covariance Matrix   ##==========##==========##
        #######################################################################################
        for CVM_Bin in range(0, nBins_CVM, 1):
            Covariance_Matrix.SetBinContent(CVM_Bin, CVM_Bin, ExREAL_1D.GetBinError(CVM_Bin)*ExREAL_1D.GetBinError(CVM_Bin))
        ######################################################################################
        ##==========##==========##   Filled the Covariance Matrix   ##==========##==========##
        ######################################################################################
             
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        Reg_Par = 13
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        
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

                for ii in range(1, Unfolded_Histo.GetNbinsX() + 1, 1):
                    Unfolded_Histo.SetBinError(ii, ROOT.sqrt(Regularized_CV_Matrix.GetBinContent(ii, ii)))
                
                Unfolded_Histo.SetTitle(((str(Unfolded_Histo.GetTitle()).replace("Experimental", "SVD Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(Unfolded_Histo.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))
                
                List_Of_Outputs = [Unfolded_Histo, Unfold_Obj, Unfolded_Determinate, Unfolded_Covariance_Matrix, Regularized_CV_Matrix]    
                
                print(f"{color.BCYAN}Finished {color.BLUE}SVD{color.END_B}{color.CYAN} Unfolding Procedure.\n{color.END}")
                return List_Of_Outputs

            except:
                print("".join([color.Error, "\nFAILED TO UNFOLD A HISTOGRAM (SVD)...", color.END]))
                print("".join([color.Error, "ERROR:\n", color.END_R, str(traceback.format_exc()), color.END]))
                
        else:
            print("unequal bins...")
            print("".join(["nBins_CVM               = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX()   = ", str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX()   = ", str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
####################################################################################################################
#####=========================#####==============================================#####=========================#####
#####=====#####=====#####=====#####     End of Method: "SVD" (Original)          #####=====#####=====#####=====#####
#####=========================#####==============================================#####=========================#####
####################################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################
    elif((Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]) or (Response_2D in ["N/A", "None", "Error"])):
        print("".join([color.BCYAN, "Starting ", color.UNDERLINE, color.PURPLE, "Bin-by-Bin", color.END_B, color.CYAN, " Unfolding Procedure...", color.END]))
        if(Response_2D in ["N/A", "None", "Error"]):
            print(f"{color.Error}WARNING: NOT Using Response Matrix for unfolding{color.END}")
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(Name_Print).replace("(Data-Type='mdf'), ", "")]))
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            if(MC_BGS_1D not in ["None"]):
                # Add the background back into the acceptance calculation
                Bin_Acceptance.Add(MC_BGS_1D)
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Acceptance.SetTitle(str(Bin_Acceptance.GetTitle()).replace("Reconstructed (MC) Distribution of", "Bin-by-Bin Acceptance for"))
            # print("\n\n\n\n\n\n\n\n\n\nstr(Bin_Acceptance.GetTitle()) =", str(Bin_Acceptance.GetTitle()), "\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            # Bin_Acceptance.GetYaxis().SetTitle("#frac{Number of REC Events}{Number of GEN Events}")
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Corrected")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Unfolded.Sumw2()
            
            # cut_criteria = (0.01*Bin_Acceptance.GetBinContent(Bin_Acceptance.GetMaximumBin()))
            # cut_criteria = 0.02
            # cut_criteria = 0
            cut_criteria = Min_Allowed_Acceptance_Cut

            if(any(Sector_Cut in str(Name_Print) for Sector_Cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"])):
                print(f"{color.RED}NOTE: Reducing Acceptance Cut criteria by 50% for Sector Cut plots{color.END}")
                cut_criteria = 0.5*Min_Allowed_Acceptance_Cut
            
            for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
                if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
                    if(Bin_Acceptance.GetBinContent(ii) != 0):
                        print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...\n\t(cut_criteria = ", str(cut_criteria), ")\n\t(Bin_Content  = ", str(Bin_Acceptance.GetBinContent(ii)), ")", color.END]))
                    # Bin_Unfolded.SetBinError(ii,   Bin_Unfolded.GetBinContent(ii) + Bin_Unfolded.GetBinError(ii))
                    Bin_Unfolded.SetBinError(ii,   0)
                    Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BCYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END_B, color.CYAN, " Unfolding Procedure.", color.END]))
            if(Response_2D in ["N/A", "None", "Error"]):
                return [Bin_Unfolded, Bin_Acceptance]
        except:
            print("".join([color.Error, "\nFAILED TO CORRECT A HISTOGRAM (Bin-by-Bin)...", color.END]))
            print("".join([color.Error, "ERROR:\n", color.END_R, str(traceback.format_exc()), color.END]))
            return "ERROR"
############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####     End of Method:  "Bin-by-Bin"     #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    if((("RooUnfold" in str(Method)) or (str(Method) in ["Default"]) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])) and (Response_2D not in ["N/A", "None", "Error"])):
        print("".join([color.BCYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END_B, color.CYAN, " Unfolding Procedure...", color.END]))        
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
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
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle())])
            Response_2D_Input       = ROOT.TH2D("".join([str(Response_2D.GetName()), "_Flipped"]), str(Response_2D_Input_Title), Response_2D.GetNbinsY(), MinBinCVM, MaxBinCVM, Response_2D.GetNbinsX(), MinBinCVM, MaxBinCVM)
            # Use the following code if the input Response Matrix plots the generated events on the x-axis
            # # The RooUnfold library takes Response Matrices which plot the true/generated events on the y-axis and the measured/reconstructed events on the x-axis
            ##==============##============================================##==============##
            ##==============##=====##     Flipping Response_2D     ##=====##==============##
            ##=========##   Generated Bins       ##=====##
            for gen_bin in range(0, nBins_CVM + 1, 1):
                ##=====##   Reconstructed Bins   ##=====##
                for rec_bin in range(0, nBins_CVM + 1, 1):
                    Res_Value = Response_2D.GetBinContent(gen_bin,    rec_bin)
                    Res_Error = Response_2D.GetBinError(gen_bin,      rec_bin)
                    Response_2D_Input.SetBinContent(rec_bin, gen_bin, Res_Value)
                    Response_2D_Input.SetBinError(rec_bin,   gen_bin, Res_Error)
            ##==============##=====##     Flipped Response_2D      ##=====##==============##
            ##==============##============================================##==============##
            # Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle())])
            Response_2D_Input       = Response_2D
        del Response_2D

        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                # Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, "".join([str(Response_2D_Input.GetName()).replace("_Flipped", ""), "_RooUnfoldResponse_Object"]), Response_2D_Input_Title)
                
                if(MC_BGS_1D != "None"):
                    # Background Subtraction Method 1: Fill the Response_RooUnfold object explicitly with the content of a background histogram with the Fake() function
                    for rec_bin in range(0, nBins_CVM + 1, 1):
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
                    print("".join(["\t", color.CYAN, "Using ", color.BGREEN, str(Unfold_Title), color.END_C, " Unfolding Procedure...", color.END]))

                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################
                    Reg_Par = 13
                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################

                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)

                elif(("bbb" in str(Method)) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print("".join(["\t", color.CYAN, "Using ", color.BGREEN, str(Unfold_Title), color.END_C, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)

                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print("".join(["\t", color.CYAN, "Using ", color.BGREEN, str(Unfold_Title), color.END_C, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)

                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print("".join(["\t", color.RED, "Method '",                 color.BOLD,   str(Method),       color.END_R, "' is unknown/undefined...", color.END]))
                        print("".join(["\t", color.RED, "Defaulting to using the ", color.BGREEN, str(Unfold_Title), color.END_R, " method to unfold...",      color.END]))
                    else:
                        print("".join(["\t", color.CYAN, "Using ",                  color.BGREEN, str(Unfold_Title), color.END_C, " method to unfold...",      color.END]))
                        
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
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)


##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                Unfolded_Histo = Unfolding_Histo.Hunfold()
    
                for bin_rec in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                    if(MC_REC_1D.GetBinContent(bin_rec) == 0):
                        Unfolded_Histo.SetBinError(bin_rec,          Unfolded_Histo.GetBinContent(bin_rec)        + Unfolded_Histo.GetBinError(bin_rec))
                        # Unfolded_Histo.SetBinError(bin_rec,          0)
                        # Unfolded_Histo.SetBinContent(bin_rec,        0)
                        
                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    Bin_Acceptance = MC_REC_1D.Clone()
                    Bin_Acceptance.Sumw2()
                    Bin_Acceptance.Divide(MC_GEN_1D)
                for bin_acceptance in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
                    if((all(cut not in str(Name_Main_Print) for cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"]) and (Bin_Acceptance.GetBinContent(bin_acceptance) < Min_Allowed_Acceptance_Cut)) or (Bin_Acceptance.GetBinContent(bin_acceptance) < 0.5*Min_Allowed_Acceptance_Cut)):
                        # Condition above applied normal Acceptance Cuts only when the Sector Cuts are NOT present but will always apply the cuts if the acceptance is less than 50% of the normal set value
                        # Unfolded_Histo.SetBinError(bin_acceptance,   Unfolded_Histo.GetBinContent(bin_acceptance) + Unfolded_Histo.GetBinError(bin_acceptance))
                        Unfolded_Histo.SetBinError(bin_acceptance,   0)
                        Unfolded_Histo.SetBinContent(bin_acceptance, 0)
                        
                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print("".join([color.BCYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END_B, color.CYAN, " Unfolding Procedure.\n", color.END]))
                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    return [Unfolded_Histo, Response_RooUnfold]
                else:
                    return [Unfolded_Histo, Bin_Acceptance]

                        
            except:
                print("".join([color.Error, "\nFAILED TO UNFOLD A HISTOGRAM (RooUnfold)...", color.END]))
                print("".join([color.Error, "ERROR:\n", color.END, str(traceback.format_exc())]))
                
        else:
            print("".join([color.RED, "Unequal Bins...", color.END]))
            print("".join(["nBins_CVM = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX() = ",   str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX() = ",   str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
    

    else:
        print("".join(["Procedure for Method '", str(Method), "' has not yet been defined..."]))
        return "ERROR"
    
    print("".join([color.Error, "\nERROR: DID NOT RETURN A HISTOGRAM YET...\n", color.END]))
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
                    histo_group = "".join(["Q2_y_Bin_", str(histo_group)]) 
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
    
    return Name_Output

######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default", Special="Normal", Use_Higher_Terms=extra_function_terms, Overwrite_Fit_Test=False, Text_NDC=None):
    if((Fitting in ["flat", "Flat", "pol0", "POL0"])):
        try:
            fit_range_lower = 0.0
            fit_range_upper = 360.0
            n_bins          = Histo_To_Fit.GetNbinsX()
            for bin_lower in range(1, (n_bins // 2) + 1):
                if(Histo_To_Fit.GetBinContent(bin_lower) != 0):
                    fit_range_lower = Histo_To_Fit.GetXaxis().GetBinLowEdge(bin_lower)
                    break
            for bin_upper in range(n_bins, (n_bins // 2), -1):
                if(Histo_To_Fit.GetBinContent(bin_upper) != 0):
                    fit_range_upper = Histo_To_Fit.GetXaxis().GetBinUpEdge(bin_upper)
                    break

            # Build a constant function (pol0). This is the pseudo-average line.
            Flat_Function = ROOT.TF1(f"Flat_Function_of_{Histo_To_Fit.GetName()}_{str(Method).replace(' ', '_')}", "pol0", float(fit_range_lower), float(fit_range_upper))
            Flat_Function.SetRange(float(fit_range_lower), float(fit_range_upper))

            Flat_Function.SetLineColor(ROOT.kRed)
            Flat_Function.SetLineStyle(7)
            Flat_Function.SetLineWidth(2)

            # Perform the fit quietly, draw result on the same pad
            # "QRB": Q=quiet, R=respect range, B=use bounding for errors
            Histo_To_Fit.Fit(Flat_Function, "QRB")

            A_Flat        = Flat_Function.GetParameter(0)
            A_Flat_Error  = Flat_Function.GetParError(0)
            try:
                Fit_Chisquared = Flat_Function.GetChisquare()
                Fit_ndf        = Flat_Function.GetNDF()
            except:
                Fit_Chisquared = "Fit_Chisquared"
                Fit_ndf        = "Fit_ndf"

            if(Text_NDC is None): # Default: bottom-center
                Text_NDC = [0.33, 0.10, 0.67, 0.24]

            # Build a brief, readable summary
            # Example:  <flat>  A = 1234 ± 12   χ²/ndf = 45.3/48
            try:
                chi2_text = f"{Fit_Chisquared:.3g}/{Fit_ndf}" if(isinstance(Fit_Chisquared, (int, float)) and isinstance(Fit_ndf, (int, float))) else f"{Fit_Chisquared}/{Fit_ndf}"
            except:
                chi2_text = f"{Fit_Chisquared}/{Fit_ndf}"

            pave = ROOT.TPaveText(float(Text_NDC[0]), float(Text_NDC[1]),
                                  float(Text_NDC[2]), float(Text_NDC[3]), "NDC")
            pave.SetName(f"PaveText_Flat_{Histo_To_Fit.GetName()}_{str(Method).replace(' ', '_')}")
            pave.SetFillStyle(0)
            pave.SetBorderSize(0)
            pave.SetTextAlign(12)         # left-aligned, vertically centered
            pave.SetTextFont(42)
            # pave.SetTextSize(0.032)
            pave.SetTextSize(0.064)
            pave.SetTextColor(ROOT.kBlack)
            pave.AddText(f"A = {A_Flat:.6f} +/- {A_Flat_Error:.3f}")
            pave.AddText(f"chi2/ndf = {chi2_text}")
            pave.Draw()

            # Return format identical to your default path
            # For the flat fit, B and C are identically zero.
            # Out_Put = [Histo_To_Fit, Flat_Function, [Fit_Chisquared, Fit_ndf], [A_Flat, A_Flat_Error], [0.0, 0.0], [0.0, 0.0]]
            Out_Put = [Histo_To_Fit, pave, [Fit_Chisquared, Fit_ndf], [A_Flat, A_Flat_Error], [0.0, 0.0], [0.0, 0.0]]
            return Out_Put
        except:
            print(f"{color.Error}ERROR IN FLAT FIT:\n{color.END}{str(traceback.format_exc())}\n")
            # Out_Put = [Histo_To_Fit, "Flat_Function", ["Fit_Chisquared", "Fit_ndf"], ["A_Flat", "A_Flat_Error"], ["B_Flat", "B_Flat_Error"], ["C_Flat", "C_Flat_Error"]]
            Out_Put = [Histo_To_Fit, "pave", ["Fit_Chisquared", "Fit_ndf"], ["A_Flat", "A_Flat_Error"], ["B_Flat", "B_Flat_Error"], ["C_Flat", "C_Flat_Error"]]
            return Out_Put

    elif((Method in ["RC"]) and (Fit_Test or Overwrite_Fit_Test)):
        try:
            Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
            Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit.GetName()}_{Method}", fit_function, 0, 360)
            RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=Q2_y_Bin_Special, z_pT_bin=z_pT_Bin_Special, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
            Fitting_Function.SetParameter(0, RC_Par_A)
            Fitting_Function.SetParLimits(0, RC_Par_A - 2*abs(RC_Err_A), RC_Par_A + 2*abs(RC_Err_A))
            Fitting_Function.SetParameter(1, RC_Par_B)
            Fitting_Function.SetParLimits(1, RC_Par_B - 2*abs(RC_Err_B), RC_Par_B + 2*abs(RC_Err_B))
            Fitting_Function.SetParameter(2, RC_Par_C)
            Fitting_Function.SetParLimits(2, RC_Par_C - 2*abs(RC_Err_C), RC_Par_C + 2*abs(RC_Err_C))
            Fitting_Function.SetParName(0, "A")
            Fitting_Function.SetParName(1, "B")
            Fitting_Function.SetParName(2, "C")
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
    elif((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true", "RC_Bin", "RC_Bayesian"]) and (Fitting in ["default", "Default"]) and (Fit_Test or Overwrite_Fit_Test)):
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
            if(Method in ["RC_Bin"]):
                Fitting_Function.SetLineColor(ROOT.kOrange + 4)
            if(Method in ["RC_Bayesian"]):
                Fitting_Function.SetLineColor(ROOT.kViolet - 8)
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

                if(((Special not in ["Normal"]) and isinstance(Special, list)) and (not Closure_Test)):
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
                                if(("RC_" in Method) and ((Q2_y_Bin_Special, z_pT_Bin_Special, "RC") in special_fit_parameters_set)):
                                    print(f"\n{color.BCYAN}Using RC Initial Fit Configs for Bin ({Q2_y_Bin_Special}-{z_pT_Bin_Special}){color.END}\n")
                                    bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "RC")]
                                else:
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
            print(f"\n{color.BLUE}Running MultiD_Slice(...){color.END}\n")
        else:
            print(f"\n\n{color.Error}Wrong Smearing option for MultiD_Slice(...){color.END}\n\n")
            return "Error"
    elif(Smear in [""]):
        print(f"\n{color.BLUE}Running MultiD_Slice(...){color.END}\n")
    else:
        print(f"\n\n{color.Error}Wrong Smearing option for MultiD_Slice(...){color.END}\n\n")
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
    if(str(Method) not in ["rdf", "gdf"]):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
        else:
            print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
            return "Error"
    elif(Smear in [""]):
        print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
    elif((not Sim_Test) or (str(Method) in ["gdf"])):
        print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
        return "Error"
    else:
        print(f"\n{color.BLUE}Running Multi3D_Slice(...) {color.RED}(with Method = '{Method}' and Smear = '{Smear}' — Sim_Test = '{Sim_Test}'){color.END}\n")
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName = {color.END}{Name}\nMulti3D_Slice() should be used on the histograms with the 'MultiDim_z_pT_Bin_Y_bin_phi_t' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_z_pT_Bin_Y_bin_phi_t"]):
            print(f"{color.RED}ERROR in Multi3D_Slice(): Not set up for other variables (yet)\n{color.END}Variable = {Variable}\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = f"{Variable}_smeared"
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
        print(f"{color.Error}Multi3D_Slice(...) ERROR:{color.END}\n{traceback.format_exc()}\n")
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
            print(f"\n{color.BLUE}Running Multi5D_Slice(...){color.END}\n")
        else:
            print(f"\n\n{color.Error}Wrong Smearing option for Multi5D_Slice(...){color.END}\n\n")
            return "Error"
    elif(Smear in [""]):
        print(f"\n{color.BLUE}Running Multi5D_Slice(...){color.END}\n")
    elif((not Sim_Test) or (str(Method) in ["gdf"])):
        print(f"\n\n{color.Error}Wrong Smearing option for Multi5D_Slice(...){color.END}\n\n")
        return "Error"
    else:
        print(f"\n{color.BLUE}Running Multi5D_Slice(...) {color.RED}(with Method = '{Method}' and Smear = '{Smear}' — Sim_Test = '{Sim_Test}'){color.END}\n")
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName = {color.END}{Name}\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_Q2_y_z_pT_phi_h"]):
            print(f"{color.RED}ERROR in Multi5D_Slice(): Not set up for other variables (yet)\n{color.END}Variable = {Variable}\n\n")
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
        print(f"{color.Error}Multi5D_Slice(...) ERROR:{color.END}\n{traceback.format_exc()}\n")
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
            print(f"\n\n\n{color.Error}ERROR IN New_Version_of_File_Creation()...\nThis function is meant to just handle the 'Response_Matrix' Histograms (for Unfolding)\nFlawed Input was: {Out_Print_Main}{color.END}\n\n")
            return Histogram_List_All
        if(type(Histogram_List_All) is not dict):
            print(f"\n\n\n{color.Error}ERROR IN New_Version_of_File_Creation()...\nThis function requires that 'Histogram_List_All' be set as a dict to properly handle the outputs\nFlawed Input was:\nHistogram_List_All = {Histogram_List_All}{color.END}\n\n")
            return Histogram_List_All
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################

        Variable_Input = Histogram_Name_Def(Out_Print_Main, Variable="FindAll")
        print(f"Variable_Input = {Variable_Input}")
        Allow_Fitting  = ("phi_t" in str(Variable_Input)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input))

        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        try:
            Bin_Method_Histograms        = Unfold_Function(Response_2D,  ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D)
            Bin_Unfolded, Bin_Acceptance = Bin_Method_Histograms
        except:
            print(f"{color.Error}ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n{color.END_R}{traceback.format_exc()}{color.END}")

        if(("sec" not in Variable_Input) or (Response_2D not in ["N/A", "None", "Error"])):
            try:
                if("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input)):
                    # Temporary restriction on 5D unfolding as method is being tested for computational requirements (copy this line to see other restriction)
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D))[0]
                else:
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes", MC_BGS_1D=MC_BGS_1D))[0]
            except:
                print(f"{color.Error}ERROR IN RooUnfold Bayesian METHOD:\n{color.END_R}{traceback.format_exc()}{color.END}")
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
        if(not Sim_Test):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "rdf")).replace("Smear", "''")]               = ExREAL_1D.Clone(str(Histo_Name_General.replace("METHOD",   "rdf")).replace("Smear", "''"))
        else:
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "rdf"))]                                      = ExREAL_1D.Clone(str(Histo_Name_General.replace("METHOD",   "rdf")))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf"))]                                      = MC_REC_1D.Clone(str(Histo_Name_General.replace("METHOD",   "mdf")))
        if(hasattr(Response_2D, 'Clone') and callable(getattr(Response_2D, 'Clone'))):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "mdf")).replace("1D", "Response_Matrix")]     = Response_2D.Clone(str(Histo_Name_General.replace("METHOD", "mdf")).replace("1D",    "Response_Matrix"))
        else:
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "mdf")).replace("1D", "Response_Matrix")]     = Response_2D
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
            if(Fit_Test and Allow_Fitting):
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function")] = Unfolded_TDF_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Chi_Squared")]  = Chi_Squared_TDF.Clone(str(Histo_Name_General.replace("METHOD",           "tdf")).replace("1D", "Chi_Squared"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_A")]    = TDF_Fit_Par_A.Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_A"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_B")]    = TDF_Fit_Par_B.Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_B"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_C")]    = TDF_Fit_Par_C.Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_C"))
                
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
                            print("".join([color.Error, "ERROR IN ADDING TO Histogram_List_All (while looping within an item in histos_list):\n", color.END_R, str(traceback.format_exc()), color.END]))
                            print("histos_list =", histos_list)
                            # print("histos_list_loop =", histos_list_loop)
                except:
                    print("".join([color.Error,         "ERROR IN ADDING TO Histogram_List_All (while looping through items in histos_list):\n",  color.END_R, str(traceback.format_exc()), color.END]))
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










######################################################################################################################################################
##==========##==========## (New) Simple Function for Drawing 2D Histograms  ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################

def Draw_2D_Histograms_Simple_New(Histogram_List_All_Input, Canvas_Input=[], Default_Histo_Name_Input="", Q2_Y_Bin_Input="All", Z_PT_Bin_Input="All", String_Output=""):
    
    Name_Uses_MultiDim = any(multi in str(Default_Histo_Name_Input) for multi in ["(Multi-Dim Histo)", "(MultiDim_Q2_y_z_pT_phi_h)", "(MultiDim_5D_Histo)", "(MultiDim_3D_Histo)"])
    
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(1D)",                "(Normal_2D)")
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(Multi-Dim Histo)",   "(Normal_2D)")
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(MultiDim_5D_Histo)", "(Normal_2D)")
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(MultiDim_3D_Histo)", "(Normal_2D)")
    
    Variable = "(MultiDim_Q2_y_z_pT_phi_h)" if("(MultiDim_Q2_y_z_pT_phi_h)" in Default_Histo_Name_Input) else "(MultiDim_z_pT_Bin_Y_bin_phi_t)" if("(MultiDim_z_pT_Bin_Y_bin_phi_t)" in Default_Histo_Name_Input) else "(phi_t)" if("(phi_t)" in Default_Histo_Name_Input) else "(Q2)" if("(Q2)" in Default_Histo_Name_Input) else "(xB)" if("(xB)" in Default_Histo_Name_Input) else "(z)" if("(z)" in Default_Histo_Name_Input) else "(pT)" if("(pT)" in Default_Histo_Name_Input) else "(y)" if("(y)" in Default_Histo_Name_Input) else "(MM)"
    
    Q2_y__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    z_pT__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    Q2_xB_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    Q2_y_Histo_rdf_Initial   = Histogram_List_All_Input[str(Q2_y__Histo_rdf_Initial_Name)]
    z_pT_Histo_rdf_Initial   = Histogram_List_All_Input[str(z_pT__Histo_rdf_Initial_Name)]
    Q2_xB_Histo_rdf_Initial  = Histogram_List_All_Input[str(Q2_xB_Histo_rdf_Initial_Name)]
    
    Q2_y__Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear", "Smear")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    z_pT__Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear", "Smear")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    Q2_xB_Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear", "Smear")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    Q2_y_Histo_mdf_Initial   = Histogram_List_All_Input[str(Q2_y__Histo_mdf_Initial_Name)]
    z_pT_Histo_mdf_Initial   = Histogram_List_All_Input[str(z_pT__Histo_mdf_Initial_Name)]
    Q2_xB_Histo_mdf_Initial  = Histogram_List_All_Input[str(Q2_xB_Histo_mdf_Initial_Name)]
    
    elth__Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),    "(el)_(elth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    elPhi_Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),   "(el)_(elPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    elth_Histo_rdf_Initial   = Histogram_List_All_Input[str(elth__Histo_rdf_Initial_Name)]
    elPhi_Histo_rdf_Initial  = Histogram_List_All_Input[str(elPhi_Histo_rdf_Initial_Name)]
    
    pipth__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),  "(pip)_(pipth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    pipPhi_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable), "(pip)_(pipPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    pipth_Histo_rdf_Initial  = Histogram_List_All_Input[str(pipth__Histo_rdf_Initial_Name)]
    pipPhi_Histo_rdf_Initial = Histogram_List_All_Input[str(pipPhi_Histo_rdf_Initial_Name)]
    
    elth__Histo_mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),        "(el)_(elth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    elPhi_Histo_mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),       "(el)_(elPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    elth_Histo_mdf_Initial   = Histogram_List_All_Input[str(elth__Histo_mdf_Initial_Name)]
    elPhi_Histo_mdf_Initial  = Histogram_List_All_Input[str(elPhi_Histo_mdf_Initial_Name)]
        
    pipth__Histo_mdf_Initial_Name = str(str(Default_Histo_Name_Input.replace(str(Variable),      "(pip)_(pipth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    pipPhi_Histo_mdf_Initial_Name = str(str(Default_Histo_Name_Input.replace(str(Variable),     "(pip)_(pipPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    pipth_Histo_mdf_Initial  = Histogram_List_All_Input[str(pipth__Histo_mdf_Initial_Name)]
    pipPhi_Histo_mdf_Initial = Histogram_List_All_Input[str(pipPhi_Histo_mdf_Initial_Name)]
    
    Bin_Title     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin_Input) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin_Input), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ["All", "0"]) else "All"]), "}}}"])
    Bin_Title     = Bin_Title.replace("Common_Int", "Integrated (Over Common Range)")
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])
    
    Drawing_Histo_Set = {}
    for Drawing_Histo_Found_and_Name in [[Q2_y_Histo_rdf_Initial,   Q2_y__Histo_rdf_Initial_Name], [z_pT_Histo_rdf_Initial,   z_pT__Histo_rdf_Initial_Name], [Q2_xB_Histo_rdf_Initial,  Q2_xB_Histo_rdf_Initial_Name], [Q2_y_Histo_mdf_Initial,   Q2_y__Histo_mdf_Initial_Name], [z_pT_Histo_mdf_Initial,   z_pT__Histo_mdf_Initial_Name], [Q2_xB_Histo_mdf_Initial,  Q2_xB_Histo_mdf_Initial_Name], [elth_Histo_rdf_Initial,   elth__Histo_rdf_Initial_Name], [elPhi_Histo_rdf_Initial,  elPhi_Histo_rdf_Initial_Name], [pipth_Histo_rdf_Initial,  pipth__Histo_rdf_Initial_Name], [pipPhi_Histo_rdf_Initial, pipPhi_Histo_rdf_Initial_Name], [elth_Histo_mdf_Initial,   elth__Histo_mdf_Initial_Name], [elPhi_Histo_mdf_Initial,  elPhi_Histo_mdf_Initial_Name], [pipth_Histo_mdf_Initial,  pipth__Histo_mdf_Initial_Name], [pipPhi_Histo_mdf_Initial, pipPhi_Histo_mdf_Initial_Name]]:
        Drawing_Histo_Found, Drawing_Histo_Name = Drawing_Histo_Found_and_Name
        #########################################################
        ##===============##     3D Slices     ##===============##
        if("3D" in str(type(Drawing_Histo_Found))):
            # bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input    if(str(Z_PT_Bin_Input) not in ["All", "0"]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0"]) else Drawing_Histo_Found.GetNbinsX())
            bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input    if(str(Z_PT_Bin_Input) not in ["All", "0"]) else 1), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0"]) else Drawing_Histo_Found.GetNbinsX())
            if(str(Z_PT_Bin_Input) not in ["All", "0"]):
                Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            New_Name = str(Drawing_Histo_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input)     in ["All", "0"]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found.Project3D('yz e')
            Drawing_Histo_Set[New_Name].SetName(New_Name)
            Drawing_Histo_Title = (str(Drawing_Histo_Set[New_Name].GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: " if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: ", str(Q2_Y_Bin_Input)]), str(Bin_Title))
            Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
            if("mdf" in str(Drawing_Histo_Found.GetName())):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
            Drawing_Histo_Set[New_Name].SetTitle(Drawing_Histo_Title)
        else:
            New_Name = str(Drawing_Histo_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input)     in ["All", "0"]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found
            if((str(Bin_Title) not in str(Drawing_Histo_Set[New_Name].GetTitle())) and (str(Standard_Histogram_Title_Addition) not in [""]) and (str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[New_Name].GetTitle()))):
                Drawing_Histo_Set[New_Name].SetTitle("".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"]))
            if(("MultiDim_Q2_y_z_pT_phi_h" not in New_Name) or ("MultiDim_z_pT_Bin_Y_bin_phi_t" not in New_Name)):
                print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
        ##===============##     3D Slices     ##===============##
        #########################################################

    try:
        Canvas_Input_0, Canvas_Input_1, Canvas_Input_2, Canvas_Input_3, Canvas_Input_4 = Canvas_Input
    except:
        try:
            Canvas_Input_0, Canvas_Input_1, Canvas_Input_2, Canvas_Input_3             = Canvas_Input
        except:
            print(color.Error, "\n\nMajor Error in getting 'Canvas_Input' for the Draw_2D_Histograms_Simple_New() function.\n\n", color.END)
    
    
    Q2_y__Histo_rdf_2D  = str(Q2_y__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    z_pT__Histo_rdf_2D  = str(z_pT__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    Q2_xB_Histo_rdf_2D  = str(Q2_xB_Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    Q2_y__Histo_mdf_2D  = str(Q2_y__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    z_pT__Histo_mdf_2D  = str(z_pT__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    Q2_xB_Histo_mdf_2D  = str(Q2_xB_Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    ##################################################################
    ##===============##     Drawing Histograms     ##===============##
    Draw_Canvas(canvas=Canvas_Input_1, cd_num=1, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].Draw("colz")
    Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].SetTitle((Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].GetTitle()).replace("Q^{2}-x_{B} Bin: All" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: All", str(Bin_Title)))
    Q2_y_borders = {}
    if("y_bin" in Binning_Method):
        line_num = 0
        for b_lines in Q2_y_Border_Lines(-1):
            try:
                Q2_y_borders[(line_num)] = ROOT.TLine()
            except:
                print(color.RED, "Error in Q2_y_borders[(line_num)]", color.END)
            Q2_y_borders[(line_num)].SetLineColor(1)
            Q2_y_borders[(line_num)].SetLineWidth(2)
            Q2_y_borders[(line_num)].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
            line_num += 1
    else:
        for Q2_Y_Bin_ii in range(1, 18, 1):
            Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.DrawClone("same")
    
    Draw_Canvas(canvas=Canvas_Input_1, cd_num=2, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].Draw("colz")
    if(str(Q2_Y_Bin_Input) not in ["All", "0"]):
        if("y_bin" in Binning_Method):
            z_pT_borders = {}
            Max_z  = max(z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2])
            Min_z  = min(z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2])
            Max_pT = max(z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2])
            Min_pT = min(z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2])
            for zline in z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2]:
                for pTline in z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2]:
                    z_pT_borders[zline] = ROOT.TLine()
                    z_pT_borders[zline].SetLineColor(1)
                    z_pT_borders[zline].SetLineWidth(2)
                    z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                    z_pT_borders[pTline] = ROOT.TLine()
                    z_pT_borders[pTline].SetLineColor(1)
                    z_pT_borders[pTline].SetLineWidth(2)
                    z_pT_borders[pTline].DrawLine(pTline, Min_z, pTline, Max_z)
        else:
            Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].GetXaxis().SetRangeUser(0, 1.2)
            Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin_Input, Set_Max_Y=1.2, Set_Max_X=1.2)
            
    if(any(binning in str(Binning_Method) for binning in ["y", "Y"])):
        Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].GetYaxis().SetRangeUser(0, 1.2)
        MM_z_pT_borders = {}
        # Create a TLegend
        MM_z_pT_legend = ROOT.TLegend(0.5, 0.1, 0.9, 0.2)  # (x1, y1, x2, y2)
        MM_z_pT_legend.SetNColumns(2)
        MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin=Q2_Y_Bin_Input, Plot_Orientation="z_pT")
        for MM_lines in MM_z_pT_borders:
            MM_z_pT_borders[MM_lines].DrawClone("same")
        MM_z_pT_legend.DrawClone("same")
    
    
    Draw_Canvas(canvas=Canvas_Input_2, cd_num=1, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].Draw("colz")
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].SetTitle((Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].GetTitle()).replace("Q^{2}-x_{B} Bin: All" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: All", str(Bin_Title)))
    # Q2_xB_borders, line_num = {}, 0
    # for b_lines in Q2_xB_Border_Lines(-1):
    #     Q2_xB_borders[line_num] = ROOT.TLine()
    #     Q2_xB_borders[line_num].SetLineColor(1)    
    #     Q2_xB_borders[line_num].SetLineWidth(2)
    #     Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
    #     line_num += 1
    Q2_xB_borders = {}
    for Q2_Y_Bin_ii in range(1, 18, 1):
        Q2_xB_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, Use_xB=True)
        for line in Q2_xB_borders[Q2_Y_Bin_ii]:
            line.DrawClone("same")
    # if((str(Q2_Y_Bin_Input) not in ["All", "0"]) and (("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method)))):
    #     ##=====================================================##
    #     ##==========##     Selecting Q2-xB Bin     ##==========##
    #     ##=====================================================##
    #     line_num_2 = 0
    #     for b_lines_2 in Q2_xB_Border_Lines(Q2_Y_Bin_Input):
    #         Q2_xB_borders[line_num_2] = ROOT.TLine()
    #         Q2_xB_borders[line_num_2].SetLineColor(2)
    #         Q2_xB_borders[line_num_2].SetLineWidth(3)
    #         Q2_xB_borders[line_num_2].DrawLine(b_lines_2[0][0], b_lines_2[0][1], b_lines_2[1][0], b_lines_2[1][1])
    #         line_num_2 += + 1
    #     ##=====================================================##
    #     ##==========##     Selecting Q2-xB Bin     ##==========##
    #     ##=====================================================##
        
    
    # Setting the Q2, y, and z ranges (other variables keep their default ranges)
    # # Q2 Ranges:
    Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].GetYaxis().SetRangeUser(1.5,  12)
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].GetYaxis().SetRangeUser(1.5,  12)
    Drawing_Histo_Set[str(Q2_y__Histo_mdf_2D)].GetYaxis().SetRangeUser(1.5,  12)
    Drawing_Histo_Set[str(Q2_xB_Histo_mdf_2D)].GetYaxis().SetRangeUser(1.5,  12)
    # # y Range:
    Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].GetXaxis().SetRangeUser(0.2, 0.8)
    Drawing_Histo_Set[str(Q2_y__Histo_mdf_2D)].GetXaxis().SetRangeUser(0.2, 0.8)
    # # z Range:
    Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].GetYaxis().SetRangeUser(0.1, 0.9)
    Drawing_Histo_Set[str(z_pT__Histo_mdf_2D)].GetYaxis().SetRangeUser(0.1, 0.9)
    # # pT Range:
    Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].GetXaxis().SetRangeUser(0,   1.2)
    Drawing_Histo_Set[str(z_pT__Histo_mdf_2D)].GetXaxis().SetRangeUser(0,   1.2)
    
    
    elth___Histo_rdf_2D = str(elth__Histo_rdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    elPhi__Histo_rdf_2D = str(elPhi_Histo_rdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipth__Histo_rdf_2D = str(pipth__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipPhi_Histo_rdf_2D = str(pipPhi_Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    elth___Histo_mdf_2D = str(elth__Histo_mdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    elPhi__Histo_mdf_2D = str(elPhi_Histo_mdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipth__Histo_mdf_2D = str(pipth__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipPhi_Histo_mdf_2D = str(pipPhi_Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    
    # Setting the range for P_el
    Drawing_Histo_Set[str(elth___Histo_rdf_2D)].GetYaxis().SetRangeUser(2.08, 8)
    Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)].GetYaxis().SetRangeUser(2.08, 8)
    Drawing_Histo_Set[str(elth___Histo_mdf_2D)].GetYaxis().SetRangeUser(2.08, 8)
    Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)].GetYaxis().SetRangeUser(2.08, 8)
    
    # Setting the range for Theta_el
    Drawing_Histo_Set[str(elth___Histo_rdf_2D)].GetXaxis().SetRangeUser(3, 37)
    Drawing_Histo_Set[str(elth___Histo_mdf_2D)].GetXaxis().SetRangeUser(3, 37)
    
    # Setting the range for P_pip
    Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].GetYaxis().SetRangeUser(1, 5.25)
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_2D)].GetYaxis().SetRangeUser(1, 5.25)
    Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].GetYaxis().SetRangeUser(1, 5.25)
    Drawing_Histo_Set[str(pipPhi_Histo_mdf_2D)].GetYaxis().SetRangeUser(1, 5.25)
    
    # Setting the range for Theta_pip
    Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].GetXaxis().SetRangeUser(3, 37)
    Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].GetXaxis().SetRangeUser(3, 37)

    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth___Histo_rdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=4,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=5,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth___Histo_mdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=6,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=7,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=8,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipPhi_Histo_mdf_2D)].Draw("colz")
    
    
    ########################################################
    ###==========###  Making 1D Histograms  ###==========###
    ########################################################
    
    el_____Histo_rdf_1D = str(str(elth___Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elth)",    "(el)")
    elth___Histo_rdf_1D = str(str(elth___Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elth)",    "(elth)")
    elPhi__Histo_rdf_1D = str(str(elPhi__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elPhi)",   "(elPhi)")
    pip____Histo_rdf_1D = str(str(pipth__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipth)",  "(pip)")
    pipth__Histo_rdf_1D = str(str(pipth__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipth)",  "(pipth)")
    pipPhi_Histo_rdf_1D = str(str(pipPhi_Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipPhi)", "(pipPhi)")
    
    el_____Histo_mdf_1D = str(str(elth___Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elth)",    "(el)")
    elth___Histo_mdf_1D = str(str(elth___Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elth)",    "(elth)")
    elPhi__Histo_mdf_1D = str(str(elPhi__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(el)_(elPhi)",   "(elPhi)")
    pip____Histo_mdf_1D = str(str(pipth__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipth)",  "(pip)")
    pipth__Histo_mdf_1D = str(str(pipth__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipth)",  "(pipth)")
    pipPhi_Histo_mdf_1D = str(str(pipPhi_Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(pip)_(pipPhi)", "(pipPhi)")
    
    Q2_____Histo_rdf_1D = str(str(Q2_y__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(y)",  "(Q2)")
    y______Histo_rdf_1D = str(str(Q2_y__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(y)",  "(y)")
    z______Histo_rdf_1D = str(str(z_pT__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(z)_(pT)",  "(z)")
    pT_____Histo_rdf_1D = str(str(z_pT__Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(z)_(pT)",  "(pT)")
    xB_____Histo_rdf_1D = str(str(Q2_xB_Histo_rdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(xB)", "(xB)")
    
    Q2_____Histo_mdf_1D = str(str(Q2_y__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(y)",  "(Q2)")
    y______Histo_mdf_1D = str(str(Q2_y__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(y)",  "(y)")
    z______Histo_mdf_1D = str(str(z_pT__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(z)_(pT)",  "(z)")
    pT_____Histo_mdf_1D = str(str(z_pT__Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(z)_(pT)",  "(pT)")
    xB_____Histo_mdf_1D = str(str(Q2_xB_Histo_mdf_2D).replace("Normal_2D", "Normal_1D")).replace("(Q2)_(xB)", "(xB)")
    
    Drawing_Histo_Set[str(el_____Histo_rdf_1D)] = Drawing_Histo_Set[str(elth___Histo_rdf_2D)].ProjectionY(str(el_____Histo_rdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(elth___Histo_rdf_1D)] = Drawing_Histo_Set[str(elth___Histo_rdf_2D)].ProjectionX(str(elth___Histo_rdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(elPhi__Histo_rdf_1D)] = Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)].ProjectionX(str(elPhi__Histo_rdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pip____Histo_rdf_1D)] = Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].ProjectionY(str(pip____Histo_rdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pipth__Histo_rdf_1D)] = Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].ProjectionX(str(pipth__Histo_rdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_1D)] = Drawing_Histo_Set[str(pipPhi_Histo_rdf_2D)].ProjectionX(str(pipPhi_Histo_rdf_1D), 0, -1, "e")
    
    Drawing_Histo_Set[str(el_____Histo_mdf_1D)] = Drawing_Histo_Set[str(elth___Histo_mdf_2D)].ProjectionY(str(el_____Histo_mdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(elth___Histo_mdf_1D)] = Drawing_Histo_Set[str(elth___Histo_mdf_2D)].ProjectionX(str(elth___Histo_mdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(elPhi__Histo_mdf_1D)] = Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)].ProjectionX(str(elPhi__Histo_mdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pip____Histo_mdf_1D)] = Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].ProjectionY(str(pip____Histo_mdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pipth__Histo_mdf_1D)] = Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].ProjectionX(str(pipth__Histo_mdf_1D), 0, -1, "e")
    Drawing_Histo_Set[str(pipPhi_Histo_mdf_1D)] = Drawing_Histo_Set[str(pipPhi_Histo_mdf_2D)].ProjectionX(str(pipPhi_Histo_mdf_1D), 0, -1, "e")
    
    Drawing_Histo_Set[str(Q2_____Histo_rdf_1D)] = Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].ProjectionY(str(Q2_____Histo_rdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(y______Histo_rdf_1D)] = Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)].ProjectionX(str(y______Histo_rdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(z______Histo_rdf_1D)] = Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].ProjectionY(str(z______Histo_rdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(pT_____Histo_rdf_1D)] = Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)].ProjectionX(str(pT_____Histo_rdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(xB_____Histo_rdf_1D)] = Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].ProjectionX(str(xB_____Histo_rdf_1D),  0, -1, "e")
    
    Drawing_Histo_Set[str(Q2_____Histo_mdf_1D)] = Drawing_Histo_Set[str(Q2_y__Histo_mdf_2D)].ProjectionY(str(Q2_____Histo_mdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(y______Histo_mdf_1D)] = Drawing_Histo_Set[str(Q2_y__Histo_mdf_2D)].ProjectionX(str(y______Histo_mdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(z______Histo_mdf_1D)] = Drawing_Histo_Set[str(z_pT__Histo_mdf_2D)].ProjectionY(str(z______Histo_mdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(pT_____Histo_mdf_1D)] = Drawing_Histo_Set[str(z_pT__Histo_mdf_2D)].ProjectionX(str(pT_____Histo_mdf_1D),  0, -1, "e")
    Drawing_Histo_Set[str(xB_____Histo_mdf_1D)] = Drawing_Histo_Set[str(Q2_xB_Histo_mdf_2D)].ProjectionX(str(xB_____Histo_mdf_1D),  0, -1, "e")
    
    Drawing_Histo_Set[str(el_____Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{p_{El}}}}{",           str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(elth___Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#theta_{El}}}}{",      str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(elPhi__Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#phi_{El}}}}{",        str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pip____Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{p_{#pi^{+}}}}}{",      str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pipth__Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#theta_{#pi^{+}}}}}{", str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#phi_{#pi^{+}}}}}{",   str(Bin_Title), "}"]))

    Drawing_Histo_Set[str(Q2_____Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{Q^{2}}}}{",            str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(y______Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{y}}}{",                str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(z______Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{z}}}{",                str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pT_____Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{P_{T}}}}{",            str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(xB_____Histo_rdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{x_{B}}}}{",            str(Bin_Title), "}"]))
    
    for Histo_rdf_1D_Name in [el_____Histo_rdf_1D, elth___Histo_rdf_1D, elPhi__Histo_rdf_1D, pip____Histo_rdf_1D, pipth__Histo_rdf_1D, pipPhi_Histo_rdf_1D, Q2_____Histo_rdf_1D, y______Histo_rdf_1D, z______Histo_rdf_1D, pT_____Histo_rdf_1D, xB_____Histo_rdf_1D]:
        Drawing_Histo_Set[str(Histo_rdf_1D_Name)].SetLineColor(root_color.Blue)
        Drawing_Histo_Set[str(Histo_rdf_1D_Name)].SetMarkerColor(root_color.Blue)
        Drawing_Histo_Set[str(Histo_rdf_1D_Name)].SetLineWidth(2)
    
    Drawing_Histo_Set[str(el_____Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{p_{El}}}}{",           str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(elth___Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#theta_{El}}}}{",      str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(elPhi__Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#phi_{El}}}}{",        str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pip____Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{p_{#pi^{+}}}}}{",      str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pipth__Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#theta_{#pi^{+}}}}}{", str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pipPhi_Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{#phi_{#pi^{+}}}}}{",   str(Bin_Title), "}"]))
    
    Drawing_Histo_Set[str(Q2_____Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{Q^{2}}}}{",            str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(y______Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{y}}}{",                str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(z______Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{z}}}{",                str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(pT_____Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{P_{T}}}}{",            str(Bin_Title), "}"]))
    Drawing_Histo_Set[str(xB_____Histo_mdf_1D)].SetTitle("".join(["#splitline{#scale[1.5]{#color[", str(root_color.Blue), "]{Data} to #color[", str(root_color.Red), "]{MC REC} Comparison of: ", root_color.Bold, "{x_{B}}}}{",            str(Bin_Title), "}"]))
    
    for Histo_mdf_1D_Name in [el_____Histo_mdf_1D, elth___Histo_mdf_1D, elPhi__Histo_mdf_1D, pip____Histo_mdf_1D, pipth__Histo_mdf_1D, pipPhi_Histo_mdf_1D, Q2_____Histo_mdf_1D, y______Histo_mdf_1D, z______Histo_mdf_1D, pT_____Histo_mdf_1D, xB_____Histo_mdf_1D]:
        Drawing_Histo_Set[str(Histo_mdf_1D_Name)].SetLineColor(root_color.Red)
        Drawing_Histo_Set[str(Histo_mdf_1D_Name)].SetMarkerColor(root_color.Red)
        Drawing_Histo_Set[str(Histo_mdf_1D_Name)].SetLineWidth(2)
        
    
    Canvas_Input_4_Row_1 = Canvas_Input_4.cd(1)
    Canvas_Input_4_Row_1.Divide(5, 1, 0, 0)
    Canvas_Input_4_Row_2 = Canvas_Input_4.cd(2)
    Canvas_Input_4_Row_2.Divide(3, 1, 0, 0)
    Canvas_Input_4_Row_3 = Canvas_Input_4.cd(3)
    Canvas_Input_4_Row_3.Divide(3, 1, 0, 0)
    
    # for Name_1D in [Q2_____Histo_rdf_1D, Q2_____Histo_mdf_1D, y______Histo_rdf_1D, y______Histo_mdf_1D, z______Histo_rdf_1D, z______Histo_mdf_1D, pT_____Histo_rdf_1D, pT_____Histo_mdf_1D, xB_____Histo_rdf_1D, xB_____Histo_mdf_1D, el_____Histo_rdf_1D, el_____Histo_mdf_1D, elth___Histo_rdf_1D, elth___Histo_mdf_1D, pip____Histo_rdf_1D, pip____Histo_mdf_1D, pipth__Histo_rdf_1D, pipth__Histo_mdf_1D]:
    #     # Rebinning all comparisons except the lab phi angles
    #     if(Drawing_Histo_Set[Name_1D].GetNbinsX()%2 == 1):
    #         print(f"{color.Error}Drawing_Histo_Set[{Name_1D}] has an odd number of bins...{color.END}")
    #     Drawing_Histo_Set[Name_1D].Rebin(2)
    
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Q2_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(Q2_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    Q2_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(Q2_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    Q2_____Histo_max_1D_Normalized = max([0, 1.4*Q2_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*Q2_____Histo_mdf_1D_Normalized.GetMaximum()])
    Q2_____Histo_min_1D_Normalized = min([0, 1.4*Q2_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*Q2_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    Q2_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(Q2_____Histo_min_1D_Normalized, Q2_____Histo_max_1D_Normalized)
    Q2_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(Q2_____Histo_min_1D_Normalized, Q2_____Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    y______Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(y______Histo_rdf_1D)].DrawNormalized("H P E0 same")
    y______Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(y______Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    y______Histo_max_1D_Normalized = max([0, 1.4*y______Histo_rdf_1D_Normalized.GetMaximum(), 1.4*y______Histo_mdf_1D_Normalized.GetMaximum()])
    y______Histo_min_1D_Normalized = min([0, 1.4*y______Histo_rdf_1D_Normalized.GetMinimum(), 1.4*y______Histo_mdf_1D_Normalized.GetMinimum()])
    
    y______Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(y______Histo_min_1D_Normalized, y______Histo_max_1D_Normalized)
    y______Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(y______Histo_min_1D_Normalized, y______Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    z______Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(z______Histo_rdf_1D)].DrawNormalized("H P E0 same")
    z______Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(z______Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    z______Histo_max_1D_Normalized = max([0, 1.4*z______Histo_rdf_1D_Normalized.GetMaximum(), 1.4*z______Histo_mdf_1D_Normalized.GetMaximum()])
    z______Histo_min_1D_Normalized = min([0, 1.4*z______Histo_rdf_1D_Normalized.GetMinimum(), 1.4*z______Histo_mdf_1D_Normalized.GetMinimum()])
    
    z______Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(z______Histo_min_1D_Normalized, z______Histo_max_1D_Normalized)
    z______Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(z______Histo_min_1D_Normalized, z______Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=4,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pT_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pT_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pT_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pT_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pT_____Histo_max_1D_Normalized = max([0, 1.4*pT_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pT_____Histo_mdf_1D_Normalized.GetMaximum()])
    pT_____Histo_min_1D_Normalized = min([0, 1.4*pT_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pT_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    pT_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pT_____Histo_min_1D_Normalized, pT_____Histo_max_1D_Normalized)
    pT_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pT_____Histo_min_1D_Normalized, pT_____Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=5,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    xB_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(xB_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    xB_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(xB_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    xB_____Histo_max_1D_Normalized = max([0, 1.4*xB_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*xB_____Histo_mdf_1D_Normalized.GetMaximum()])
    xB_____Histo_min_1D_Normalized = min([0, 1.4*xB_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*xB_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    xB_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(xB_____Histo_min_1D_Normalized, xB_____Histo_max_1D_Normalized)
    xB_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(xB_____Histo_min_1D_Normalized, xB_____Histo_max_1D_Normalized)
    
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    el_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(el_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    el_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(el_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    el_____Histo_max_1D_Normalized = max([0, 1.4*el_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*el_____Histo_mdf_1D_Normalized.GetMaximum()])
    el_____Histo_min_1D_Normalized = min([0, 1.4*el_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*el_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    el_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(el_____Histo_min_1D_Normalized, el_____Histo_max_1D_Normalized)
    el_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(el_____Histo_min_1D_Normalized, el_____Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    elth___Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(elth___Histo_rdf_1D)].DrawNormalized("H P E0 same")
    elth___Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(elth___Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    elth___Histo_max_1D_Normalized = max([0, 1.4*elth___Histo_rdf_1D_Normalized.GetMaximum(), 1.4*elth___Histo_mdf_1D_Normalized.GetMaximum()])
    elth___Histo_min_1D_Normalized = min([0, 1.4*elth___Histo_rdf_1D_Normalized.GetMinimum(), 1.4*elth___Histo_mdf_1D_Normalized.GetMinimum()])
    
    elth___Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(elth___Histo_min_1D_Normalized, elth___Histo_max_1D_Normalized)
    elth___Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(elth___Histo_min_1D_Normalized, elth___Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    elPhi__Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(elPhi__Histo_rdf_1D)].DrawNormalized("H P E0 same")
    elPhi__Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(elPhi__Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    elPhi__Histo_max_1D_Normalized = max([0, 1.4*elPhi__Histo_rdf_1D_Normalized.GetMaximum(), 1.4*elPhi__Histo_mdf_1D_Normalized.GetMaximum()])
    elPhi__Histo_min_1D_Normalized = min([0, 1.4*elPhi__Histo_rdf_1D_Normalized.GetMinimum(), 1.4*elPhi__Histo_mdf_1D_Normalized.GetMinimum()])
    
    elPhi__Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(elPhi__Histo_min_1D_Normalized, elPhi__Histo_max_1D_Normalized)
    elPhi__Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(elPhi__Histo_min_1D_Normalized, elPhi__Histo_max_1D_Normalized)
    
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pip____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pip____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pip____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pip____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pip____Histo_max_1D_Normalized = max([0, 1.4*pip____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pip____Histo_mdf_1D_Normalized.GetMaximum()])
    pip____Histo_min_1D_Normalized = min([0, 1.4*pip____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pip____Histo_mdf_1D_Normalized.GetMinimum()])
    
    pip____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pip____Histo_min_1D_Normalized, pip____Histo_max_1D_Normalized)
    pip____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pip____Histo_min_1D_Normalized, pip____Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pipth__Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pipth__Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pipth__Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pipth__Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pipth__Histo_max_1D_Normalized = max([0, 1.4*pipth__Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pipth__Histo_mdf_1D_Normalized.GetMaximum()])
    pipth__Histo_min_1D_Normalized = min([0, 1.4*pipth__Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pipth__Histo_mdf_1D_Normalized.GetMinimum()])
    
    pipth__Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pipth__Histo_min_1D_Normalized, pipth__Histo_max_1D_Normalized)
    pipth__Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pipth__Histo_min_1D_Normalized, pipth__Histo_max_1D_Normalized)
    
    Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pipPhi_Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pipPhi_Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pipPhi_Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pipPhi_Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pipPhi_Histo_max_1D_Normalized = max([0, 1.4*pipPhi_Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pipPhi_Histo_mdf_1D_Normalized.GetMaximum()])
    pipPhi_Histo_min_1D_Normalized = min([0, 1.4*pipPhi_Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pipPhi_Histo_mdf_1D_Normalized.GetMinimum()])
    
    pipPhi_Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pipPhi_Histo_min_1D_Normalized, pipPhi_Histo_max_1D_Normalized)
    pipPhi_Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pipPhi_Histo_min_1D_Normalized, pipPhi_Histo_max_1D_Normalized)
    
    ##===============##     Drawing Histograms     ##===============##
    ##################################################################
    
    Canvas_Input_0.Modified()
    Canvas_Input_0.Update()
    
    palette_move(canvas=Canvas_Input_1, histo=Drawing_Histo_Set[str(Q2_y__Histo_rdf_2D)],  x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_1, histo=Drawing_Histo_Set[str(z_pT__Histo_rdf_2D)],  x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_2, histo=Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)],  x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elth___Histo_rdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipth__Histo_rdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipPhi_Histo_rdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elth___Histo_mdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipth__Histo_mdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipPhi_Histo_mdf_2D)], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    
    Canvas_Input_0.Modified()
    Canvas_Input_0.Update()
    
    if(not Name_Uses_MultiDim):
        try:
            Large_Bin_Canvas_Compare = Canvas_Create(Name=str(Canvas_Input_0.GetName()).replace("CANVAS", "CANVAS_COMPARE"), Num_Columns=1, Num_Rows=3, Size_X=2600, Size_Y=3000, cd_Space=0)

            Large_Bin_Canvas_Compare_CD              = Large_Bin_Canvas_Compare.cd(1)
            Large_Bin_Canvas_Compare_Side_by_Side_CD = Large_Bin_Canvas_Compare.cd(2)
            Large_Bin_Canvas_Compare_2D_Histo_Row_CD = Large_Bin_Canvas_Compare.cd(3)
            Large_Bin_Canvas_Compare_2D_Histo_Row_CD.Divide(1, 2)
            Large_Bin_Canvas_Compare_Main_Histos__CD = Large_Bin_Canvas_Compare_2D_Histo_Row_CD.cd(1)
            Large_Bin_Canvas_Compare_Acceptance___CD = Large_Bin_Canvas_Compare_2D_Histo_Row_CD.cd(2)

            # # Large_Bin_Canvas_Compare_CD.SetPad(0.0, 0.5, 1.0, 1.0)
            Large_Bin_Canvas_Compare_CD.SetPad(             0.0, 0.55, 1.0, 1.00)
            Large_Bin_Canvas_Compare_Side_by_Side_CD.SetPad(0.0, 0.31, 1.0, 0.55)
            Large_Bin_Canvas_Compare_2D_Histo_Row_CD.SetPad(0.0, 0.00, 1.0, 0.30)
            Large_Bin_Canvas_Compare_Main_Histos__CD.SetPad(0.0, 0.52, 1.0, 0.96)
            Large_Bin_Canvas_Compare_Acceptance___CD.SetPad(0.0, 0.01, 1.0, 0.45)

            Large_Bin_Canvas_Compare_Side_by_Side_CD.cd()
            Large_Bin_Canvas_Compare_Side_by_Side = Canvas_Input_4.DrawClone()
            Large_Bin_Canvas_Compare_Side_by_Side.SetPad(0.0, 0.0, 1.0, 1.0)
            Large_Bin_Canvas_Compare_Side_by_Side.Modified()
            Large_Bin_Canvas_Compare_Side_by_Side.Update()

            Large_Bin_Canvas_Compare_Main_Histos__CD.cd()
            Large_Bin_Canvas_Compare_Main_Histos  = Canvas_Input_1.DrawClone()
            Large_Bin_Canvas_Compare_Main_Histos.SetPad(0.0, 0.0, 1.0, 1.0)
            Large_Bin_Canvas_Compare_Main_Histos.Modified()
            Large_Bin_Canvas_Compare_Main_Histos.Update()

            Large_Bin_Canvas_Compare_Acceptance___CD.cd()
            Large_Bin_Canvas_Compare_Acceptance  = Canvas_Input_2.DrawClone()
            Large_Bin_Canvas_Compare_Acceptance.SetPad(0.0, 0.0, 1.0, 1.0)
            Large_Bin_Canvas_Compare_Acceptance.Modified()
            Large_Bin_Canvas_Compare_Acceptance.Update()

            Large_Bin_Canvas_Compare_CD.Divide(1, 3)
            Large_Bin_Canvas_Compare_CD_Upper_Kin = Large_Bin_Canvas_Compare_CD.cd(1)
            Large_Bin_Canvas_Compare_CD_Lower_Ele = Large_Bin_Canvas_Compare_CD.cd(2)
            Large_Bin_Canvas_Compare_CD_Lower_Pip = Large_Bin_Canvas_Compare_CD.cd(3)
            Large_Bin_Canvas_Compare_CD_Upper_Kin.Divide(5, 1)
            Large_Bin_Canvas_Compare_CD_Lower_Ele.Divide(3, 1)
            Large_Bin_Canvas_Compare_CD_Lower_Pip.Divide(3, 1)

            Q2_____Histo_RATIO__Normalized = Q2_____Histo_rdf_1D_Normalized.Clone("".join([str(Q2_____Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            Q2_____Histo_RATIO__Normalized.Divide(Q2_____Histo_mdf_1D_Normalized)
            Q2_____Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{Q^{2}}}}{",            str(Bin_Title), "}"]))
            # Q2_____Histo_RATIO__Normalized.Sumw2()
            # Q2_____Histo_RATIO__Normalized.Rebin()

            y______Histo_RATIO__Normalized = y______Histo_rdf_1D_Normalized.Clone("".join([str(y______Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            y______Histo_RATIO__Normalized.Divide(y______Histo_mdf_1D_Normalized)
            y______Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{y}}}{",                str(Bin_Title), "}"]))
            # y______Histo_RATIO__Normalized.Sumw2()
            # y______Histo_RATIO__Normalized.Rebin()

            z______Histo_RATIO__Normalized = z______Histo_rdf_1D_Normalized.Clone("".join([str(z______Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            z______Histo_RATIO__Normalized.Divide(z______Histo_mdf_1D_Normalized)
            z______Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{z}}}{",                str(Bin_Title), "}"]))
            # z______Histo_RATIO__Normalized.Sumw2()
            # z______Histo_RATIO__Normalized.Rebin()

            pT_____Histo_RATIO__Normalized = pT_____Histo_rdf_1D_Normalized.Clone("".join([str(pT_____Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            if(pT_____Histo_RATIO__Normalized.GetNbinsX() != pT_____Histo_mdf_1D_Normalized.GetNbinsX()):
                print(f"{color.RED}pT Data/MC Ratio does not have the same number of bins ((pT_____Histo_RATIO__Normalized.GetNbinsX() = {pT_____Histo_RATIO__Normalized.GetNbinsX()}) != (pT_____Histo_mdf_1D_Normalized.GetNbinsX() = {pT_____Histo_mdf_1D_Normalized.GetNbinsX()})){color.END}")
                pT_____Histo_mdf_1D_Normalized.GetXaxis().SetRangeUser(0, 1.2)
                if(pT_____Histo_RATIO__Normalized.GetNbinsX() != pT_____Histo_mdf_1D_Normalized.GetNbinsX()):
                    print(f"{color.Error}pT Data/MC Ratio STILL does not have the same number of bins ((pT_____Histo_RATIO__Normalized.GetNbinsX() = {pT_____Histo_RATIO__Normalized.GetNbinsX()}) != (pT_____Histo_mdf_1D_Normalized.GetNbinsX() = {pT_____Histo_mdf_1D_Normalized.GetNbinsX()})){color.END}")
            pT_____Histo_RATIO__Normalized.Divide(pT_____Histo_mdf_1D_Normalized)
            pT_____Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{P_{T}}}}{",            str(Bin_Title), "}"]))
            # pT_____Histo_RATIO__Normalized.Sumw2()
            # pT_____Histo_RATIO__Normalized.Rebin()

            xB_____Histo_RATIO__Normalized = xB_____Histo_rdf_1D_Normalized.Clone("".join([str(xB_____Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            xB_____Histo_RATIO__Normalized.Divide(xB_____Histo_mdf_1D_Normalized)
            xB_____Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{x_{B}}}}{",            str(Bin_Title), "}"]))
            # xB_____Histo_RATIO__Normalized.Sumw2()
            # xB_____Histo_RATIO__Normalized.Rebin()

            el_____Histo_RATIO__Normalized = el_____Histo_rdf_1D_Normalized.Clone("".join([str(el_____Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            el_____Histo_RATIO__Normalized.Divide(el_____Histo_mdf_1D_Normalized)
            el_____Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{p_{El}}}}{",           str(Bin_Title), "}"]))
            # el_____Histo_RATIO__Normalized.Sumw2()
            # el_____Histo_RATIO__Normalized.Rebin()

            elth___Histo_RATIO__Normalized = elth___Histo_rdf_1D_Normalized.Clone("".join([str(elth___Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            elth___Histo_RATIO__Normalized.Divide(elth___Histo_mdf_1D_Normalized)
            elth___Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{#theta_{El}}}}{",      str(Bin_Title), "}"]))
            # elth___Histo_RATIO__Normalized.Sumw2()
            # elth___Histo_RATIO__Normalized.Rebin()

            elPhi__Histo_RATIO__Normalized = elPhi__Histo_rdf_1D_Normalized.Clone("".join([str(elPhi__Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            elPhi__Histo_RATIO__Normalized.Divide(elPhi__Histo_mdf_1D_Normalized)
            elPhi__Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{#phi_{El}}}}{",        str(Bin_Title), "}"]))
            # elPhi__Histo_RATIO__Normalized.Sumw2()
            # elPhi__Histo_RATIO__Normalized.Rebin()

            pip____Histo_RATIO__Normalized = pip____Histo_rdf_1D_Normalized.Clone("".join([str(pip____Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            pip____Histo_RATIO__Normalized.Divide(pip____Histo_mdf_1D_Normalized)
            pip____Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{p_{#pi^{+}}}}}{",      str(Bin_Title), "}"]))
            # pip____Histo_RATIO__Normalized.Sumw2()
            # pip____Histo_RATIO__Normalized.Rebin()

            pipth__Histo_RATIO__Normalized = pipth__Histo_rdf_1D_Normalized.Clone("".join([str(pipth__Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            pipth__Histo_RATIO__Normalized.Divide(pipth__Histo_mdf_1D_Normalized)
            pipth__Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{#theta_{#pi^{+}}}}}{", str(Bin_Title), "}"]))
            # pipth__Histo_RATIO__Normalized.Sumw2()
            # pipth__Histo_RATIO__Normalized.Rebin()

            pipPhi_Histo_RATIO__Normalized = pipPhi_Histo_rdf_1D_Normalized.Clone("".join([str(pipPhi_Histo_rdf_1D_Normalized.GetName()), "_RATIO"]))
            pipPhi_Histo_RATIO__Normalized.Divide(pipPhi_Histo_mdf_1D_Normalized)
            pipPhi_Histo_RATIO__Normalized.SetTitle("".join(["#splitline{#scale[1.35]{Ratio of #frac{#color[", str(root_color.Blue), "]{Data}}{#color[", str(root_color.Red), "]{MC REC}} for ", root_color.Bold, "{#phi_{#pi^{+}}}}}{",   str(Bin_Title), "}"]))
            # pipPhi_Histo_RATIO__Normalized.Sumw2()
            # pipPhi_Histo_RATIO__Normalized.Rebin()


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Upper_Kin, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            Q2_____Histo_RATIO__Normalized.Draw("H P E0 same")
            Q2_____Histo_RATIO__Normalized_Max = max([1.8, 1.4*Q2_____Histo_RATIO__Normalized.GetBinContent(Q2_____Histo_RATIO__Normalized.GetMaximumBin())])
            Q2_____Histo_RATIO__Normalized_Min = min([0,   1.4*Q2_____Histo_RATIO__Normalized.GetBinContent(Q2_____Histo_RATIO__Normalized.GetMinimumBin())])
            Q2_____Histo_RATIO__Normalized.GetYaxis().SetRangeUser(Q2_____Histo_RATIO__Normalized_Min, Q2_____Histo_RATIO__Normalized_Max)
            Q2_____Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            Q2_____Histo_RATIO__Normalized_Line = ROOT.TLine()
            Q2_____Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            Q2_____Histo_RATIO__Normalized_Line.SetLineWidth(1)
            Q2_____Histo_RATIO__Normalized_Line.DrawLine(Q2_____Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, Q2_____Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Upper_Kin, cd_num=2, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            y______Histo_RATIO__Normalized.Draw("H P E0 same")
            y______Histo_RATIO__Normalized_Max = max([1.8, 1.4*y______Histo_RATIO__Normalized.GetBinContent(y______Histo_RATIO__Normalized.GetMaximumBin())])
            y______Histo_RATIO__Normalized_Min = min([0,   1.4*y______Histo_RATIO__Normalized.GetBinContent(y______Histo_RATIO__Normalized.GetMinimumBin())])
            y______Histo_RATIO__Normalized.GetYaxis().SetRangeUser(y______Histo_RATIO__Normalized_Min, y______Histo_RATIO__Normalized_Max)
            y______Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            y______Histo_RATIO__Normalized_Line = ROOT.TLine()
            y______Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            y______Histo_RATIO__Normalized_Line.SetLineWidth(2)
            y______Histo_RATIO__Normalized_Line.DrawLine(y______Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, y______Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Upper_Kin, cd_num=3, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            z______Histo_RATIO__Normalized.Draw("H P E0 same")
            z______Histo_RATIO__Normalized_Max = max([1.8, 1.4*z______Histo_RATIO__Normalized.GetBinContent(z______Histo_RATIO__Normalized.GetMaximumBin())])
            z______Histo_RATIO__Normalized_Min = min([0,   1.4*z______Histo_RATIO__Normalized.GetBinContent(z______Histo_RATIO__Normalized.GetMinimumBin())])
            z______Histo_RATIO__Normalized.GetYaxis().SetRangeUser(z______Histo_RATIO__Normalized_Min, z______Histo_RATIO__Normalized_Max)
            z______Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            z______Histo_RATIO__Normalized_Line = ROOT.TLine()
            z______Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            z______Histo_RATIO__Normalized_Line.SetLineWidth(2)
            z______Histo_RATIO__Normalized_Line.DrawLine(z______Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, z______Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Upper_Kin, cd_num=4, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            pT_____Histo_RATIO__Normalized.Draw("H P E0 same")
            pT_____Histo_RATIO__Normalized_Max = max([1.8, 1.4*pT_____Histo_RATIO__Normalized.GetBinContent(pT_____Histo_RATIO__Normalized.GetMaximumBin())])
            pT_____Histo_RATIO__Normalized_Min = min([0,   1.4*pT_____Histo_RATIO__Normalized.GetBinContent(pT_____Histo_RATIO__Normalized.GetMinimumBin())])
            pT_____Histo_RATIO__Normalized.GetYaxis().SetRangeUser(pT_____Histo_RATIO__Normalized_Min, pT_____Histo_RATIO__Normalized_Max)
            pT_____Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            pT_____Histo_RATIO__Normalized_Line = ROOT.TLine()
            pT_____Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            pT_____Histo_RATIO__Normalized_Line.SetLineWidth(2)
            pT_____Histo_RATIO__Normalized_Line.DrawLine(pT_____Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, pT_____Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Upper_Kin, cd_num=5, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            xB_____Histo_RATIO__Normalized.Draw("H P E0 same")
            xB_____Histo_RATIO__Normalized_Max = max([1.8, 1.4*xB_____Histo_RATIO__Normalized.GetBinContent(xB_____Histo_RATIO__Normalized.GetMaximumBin())])
            xB_____Histo_RATIO__Normalized_Min = min([0,   1.4*xB_____Histo_RATIO__Normalized.GetBinContent(xB_____Histo_RATIO__Normalized.GetMinimumBin())])
            xB_____Histo_RATIO__Normalized.GetYaxis().SetRangeUser(xB_____Histo_RATIO__Normalized_Min, xB_____Histo_RATIO__Normalized_Max)
            xB_____Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            xB_____Histo_RATIO__Normalized_Line = ROOT.TLine()
            xB_____Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            xB_____Histo_RATIO__Normalized_Line.SetLineWidth(2)
            xB_____Histo_RATIO__Normalized_Line.DrawLine(xB_____Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, xB_____Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Ele, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            el_____Histo_RATIO__Normalized.Draw("H P E0 same")
            el_____Histo_RATIO__Normalized_Max = max([1.8, 1.4*el_____Histo_RATIO__Normalized.GetBinContent(el_____Histo_RATIO__Normalized.GetMaximumBin())])
            el_____Histo_RATIO__Normalized_Min = min([0,   1.4*el_____Histo_RATIO__Normalized.GetBinContent(el_____Histo_RATIO__Normalized.GetMinimumBin())])
            el_____Histo_RATIO__Normalized.GetYaxis().SetRangeUser(el_____Histo_RATIO__Normalized_Min, el_____Histo_RATIO__Normalized_Max)
            el_____Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            el_____Histo_RATIO__Normalized_Line = ROOT.TLine()
            el_____Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            el_____Histo_RATIO__Normalized_Line.SetLineWidth(2)
            el_____Histo_RATIO__Normalized_Line.DrawLine(el_____Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, el_____Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Ele, cd_num=2, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            elth___Histo_RATIO__Normalized.Draw("H P E0 same")
            elth___Histo_RATIO__Normalized_Max = max([1.8, 1.4*elth___Histo_RATIO__Normalized.GetBinContent(elth___Histo_RATIO__Normalized.GetMaximumBin())])
            elth___Histo_RATIO__Normalized_Min = min([0,   1.4*elth___Histo_RATIO__Normalized.GetBinContent(elth___Histo_RATIO__Normalized.GetMinimumBin())])
            elth___Histo_RATIO__Normalized.GetYaxis().SetRangeUser(elth___Histo_RATIO__Normalized_Min, elth___Histo_RATIO__Normalized_Max)
            elth___Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            elth___Histo_RATIO__Normalized_Line = ROOT.TLine()
            elth___Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            elth___Histo_RATIO__Normalized_Line.SetLineWidth(2)
            elth___Histo_RATIO__Normalized_Line.DrawLine(elth___Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, elth___Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Ele, cd_num=3, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            elPhi__Histo_RATIO__Normalized.Draw("H P E0 same")
            elPhi__Histo_RATIO__Normalized_Max = max([1.8, 1.4*elPhi__Histo_RATIO__Normalized.GetBinContent(elPhi__Histo_RATIO__Normalized.GetMaximumBin())])
            elPhi__Histo_RATIO__Normalized_Min = min([0,   1.4*elPhi__Histo_RATIO__Normalized.GetBinContent(elPhi__Histo_RATIO__Normalized.GetMinimumBin())])
            elPhi__Histo_RATIO__Normalized.GetYaxis().SetRangeUser(elPhi__Histo_RATIO__Normalized_Min, elPhi__Histo_RATIO__Normalized_Max)
            elPhi__Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            elPhi__Histo_RATIO__Normalized_Line = ROOT.TLine()
            elPhi__Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            elPhi__Histo_RATIO__Normalized_Line.SetLineWidth(2)
            elPhi__Histo_RATIO__Normalized_Line.DrawLine(elPhi__Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, elPhi__Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Pip, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            pip____Histo_RATIO__Normalized.Draw("H P E0 same")
            pip____Histo_RATIO__Normalized_Max = max([1.8, 1.4*pip____Histo_RATIO__Normalized.GetBinContent(pip____Histo_RATIO__Normalized.GetMaximumBin())])
            pip____Histo_RATIO__Normalized_Min = min([0,   1.4*pip____Histo_RATIO__Normalized.GetBinContent(pip____Histo_RATIO__Normalized.GetMinimumBin())])
            pip____Histo_RATIO__Normalized.GetYaxis().SetRangeUser(pip____Histo_RATIO__Normalized_Min, pip____Histo_RATIO__Normalized_Max)
            pip____Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            pip____Histo_RATIO__Normalized_Line = ROOT.TLine()
            pip____Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            pip____Histo_RATIO__Normalized_Line.SetLineWidth(2)
            pip____Histo_RATIO__Normalized_Line.DrawLine(pip____Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, pip____Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Pip, cd_num=2, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            pipth__Histo_RATIO__Normalized.Draw("H P E0 same")
            pipth__Histo_RATIO__Normalized_Max = max([1.8, 1.4*pipth__Histo_RATIO__Normalized.GetBinContent(pipth__Histo_RATIO__Normalized.GetMaximumBin())])
            pipth__Histo_RATIO__Normalized_Min = min([0,   1.4*pipth__Histo_RATIO__Normalized.GetBinContent(pipth__Histo_RATIO__Normalized.GetMinimumBin())])
            pipth__Histo_RATIO__Normalized.GetYaxis().SetRangeUser(pipth__Histo_RATIO__Normalized_Min, pipth__Histo_RATIO__Normalized_Max)
            pipth__Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            pipth__Histo_RATIO__Normalized_Line = ROOT.TLine()
            pipth__Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            pipth__Histo_RATIO__Normalized_Line.SetLineWidth(2)
            pipth__Histo_RATIO__Normalized_Line.DrawLine(pipth__Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, pipth__Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Draw_Canvas(canvas=Large_Bin_Canvas_Compare_CD_Lower_Pip, cd_num=3, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            pipPhi_Histo_RATIO__Normalized.Draw("H P E0 same")
            pipPhi_Histo_RATIO__Normalized_Max = max([1.8, 1.4*pipPhi_Histo_RATIO__Normalized.GetBinContent(pipPhi_Histo_RATIO__Normalized.GetMaximumBin())])
            pipPhi_Histo_RATIO__Normalized_Min = min([0,   1.4*pipPhi_Histo_RATIO__Normalized.GetBinContent(pipPhi_Histo_RATIO__Normalized.GetMinimumBin())])
            pipPhi_Histo_RATIO__Normalized.GetYaxis().SetRangeUser(pipPhi_Histo_RATIO__Normalized_Min, pipPhi_Histo_RATIO__Normalized_Max)
            pipPhi_Histo_RATIO__Normalized.SetLineColor(root_color.Purple)

            pipPhi_Histo_RATIO__Normalized_Line = ROOT.TLine()
            pipPhi_Histo_RATIO__Normalized_Line.SetLineColor(root_color.DGrey)    
            pipPhi_Histo_RATIO__Normalized_Line.SetLineWidth(2)
            pipPhi_Histo_RATIO__Normalized_Line.DrawLine(pipPhi_Histo_RATIO__Normalized.GetXaxis().GetXmin(), 1, pipPhi_Histo_RATIO__Normalized.GetXaxis().GetXmax(), 1)


            Large_Bin_Canvas_Compare.Modified()
            Large_Bin_Canvas_Compare.Update()

            Run_Bin_Comparison = not True
            if(Create_txt_File and Run_Bin_Comparison and (String_Output not in [""])):
                for Histo_Compare_and_Name in [[Q2_____Histo_RATIO__Normalized, str(Q2_____Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [y______Histo_RATIO__Normalized, str(y______Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [z______Histo_RATIO__Normalized, str(z______Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [pT_____Histo_RATIO__Normalized, str(pT_____Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [xB_____Histo_RATIO__Normalized, str(xB_____Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [el_____Histo_RATIO__Normalized, str(el_____Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [elth___Histo_RATIO__Normalized, str(elth___Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [elPhi__Histo_RATIO__Normalized, str(elPhi__Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [pip____Histo_RATIO__Normalized, str(pip____Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [pipth__Histo_RATIO__Normalized, str(pipth__Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")], [pipPhi_Histo_RATIO__Normalized, str(pipPhi_Histo_mdf_1D.replace("rdf", "RATIO")).replace("mdf", "RATIO")]]:
                    Histo_Compare, Histo_Name = Histo_Compare_and_Name
                    String_Output = "".join([str(String_Output), color.BOLD, """\n\n
    ======================================================================================================================================================
    ======================================================================================================================================================
    ======================================================================================================================================================
    ======================================================================================================================================================
    For Histogram: """, color.UNDERLINE, str(Histo_Name.replace("(Normal_1D)_(RATIO)_", "")).replace("All_1D", "All"), color.END, "\n"])
                    Great_Score, Good_Score, Okay_Score, Poor_Score, Bad_Score, No_Score = 0, 0, 0, 0, 0, 0
                    for bin_ii in range(0, Histo_Compare.GetNbinsX(), 1):
                        Bin_Center, Bin_Content, Bin_Error = round(Histo_Compare.GetBinCenter(bin_ii), 5), round(Histo_Compare.GetBinContent(bin_ii), 5), round(Histo_Compare.GetBinError(bin_ii), 5)
                        string_line = "".join(["\tBin ", str(bin_ii), ":\n\t\tCenter: ", str(Bin_Center), "\n\t\tRatio of Data/MC REC: ", str(Bin_Content), " (Error = ±", str(Bin_Error), ")\n"])
                        # Highlighting bins of interest
                        if(Bin_Content == 0):                                                           # Empty Bin (no comparison)
                            No_Score   += 1
                        elif(((Bin_Content + Bin_Error) > 1)   and ((Bin_Content - Bin_Error) < 1)):    # Good Matches (within error of 1:1)
                            if((Bin_Content < 1.05) and (Bin_Content > 0.95)):                          # Great Match
                                string_line  = "".join([color.BGREEN, str(string_line), color.END])
                                Great_Score += 1
                            else:                                                                       # Could just have large error but still good
                                string_line = "".join([color.GREEN,   str(string_line), color.END])
                                Good_Score += 1
                        elif((Bin_Content < 1.05)              and (Bin_Content  > 0.95)):              # Good Match (but not necessarily perfect)
                            string_line = "".join([color.GREEN,       str(string_line), color.END])
                            Good_Score += 1
                        elif((Bin_Content < 1.1)               and (Bin_Content  > 0.9)):               # Okay Match (closer to good than to bad)
                            string_line = "".join([color.BOLD,        str(string_line), color.END])
                            Okay_Score += 1
                        elif(((Bin_Content + Bin_Error) > 1.2)  or ((Bin_Content - Bin_Error) < 0.8)):  # Poor match
                            string_line = "".join([color.PURPLE,      str(string_line), color.END])
                            Poor_Score += 1
                        elif(((Bin_Content + Bin_Error) > 1.45) or ((Bin_Content - Bin_Error) < 0.55)): # Bad match
                            string_line = "".join([color.RED,         str(string_line), color.END])
                            Bad_Score  += 1

                        String_Output = "".join([str(String_Output), str(string_line)])

                    Total_Score         = (2*Great_Score) + (Good_Score) + (0.5*Okay_Score) - (Poor_Score) - (2*Bad_Score)
                    Average_Bin_Content = round(Histo_Compare.Integral() / Histo_Compare.GetNbinsX(), 4)
                    String_Output = "".join([str(String_Output), color.BOLD, "Review of Histogram", color.END, """
    Total Num of Bins:   """, str(bin_ii + 1), """
    Average Bin Content: """, color.Error if((Average_Bin_Content > 1.4) or (Average_Bin_Content < 0.6)) else color.GREEN if((Average_Bin_Content < 1.15) and (Average_Bin_Content > 0.85)) else "", str(Average_Bin_Content), color.END, """
    Total Score:         """, color.Error if(Total_Score < 0) else color.GREEN if(Total_Score > 0) else "", str(Total_Score), color.END, """
    """, color.BGREEN, "\tNum of Great  (+2) Score: ", str(Great_Score), color.END, """
    """, color.GREEN,  "\tNum of Good   (+1) Score: ", str(Good_Score),  color.END, """
    """, color.BOLD,   "\tNum of Okay (+0.5) Score: ", str(Okay_Score),  color.END, """
    """,               "\tNum of Empty  (+0) Score: ", str(No_Score),               """
    """, color.PURPLE, "\tNum of Poor   (-1) Score: ", str(Poor_Score),  color.END, """
    """, color.RED,    "\tNum of Bad    (-2) Score: ", str(Bad_Score),   color.END])
            else:
                String_Output = ""
            # Save_Name = "".join([str(Canvas_Input_0.GetName()).replace("CANVAS", "COMPARE"), ".png"])
            # Save_Name = Save_Name.replace("SMEAR=''",    "")
            # if("SMEAR=Smear" in str(Save_Name)):
            #     Save_Name = str(Save_Name.replace("SMEAR=Smear", "")).replace(").png", "_Smeared.png")
            # Save_Name = str(Save_Name.replace("(", "")).replace(")", "")
            # Save_Name = str(Save_Name.replace("__", "_"))

            Save_Name     = "".join(["Kinematic_Comparison_Q2_y_Bin_", str(Q2_Y_Bin_Input) if(str(Q2_Y_Bin_Input) not in ["0"]) else "All", "_z_pT_Bin_", str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ["0"]) else "All", "".join(["_Smeared", str(File_Save_Format)]) if("Smear" in Default_Histo_Name_Input) else str(File_Save_Format)])    
            if(Name_Uses_MultiDim):
                Save_Name = f"Multi_Unfold_{Save_Name}"
            if(Sim_Test):
                Save_Name = f"Sim_Test_{Save_Name}"
            if(Mod_Test):
                Save_Name = f"Mod_Test_{Save_Name}"
            if(not any(binning in Binning_Method for binning in ["y", "Y"])):
                print(f"\n\n{color.Error}Using Old Binning Scheme (i.e., Binning_Method = {Binning_Method}){color.END}\n\n")
                Save_Name = Save_Name.replace("_Q2_y_Bin_", "_Q2_xB_Bin_")
            Save_Name = Save_Name.replace("__", "_")
            if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
                Save_Name = Save_Name.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
            elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
                Save_Name = Save_Name.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
            if(Saving_Q):
                if("root" in str(File_Save_Format)):
                    Large_Bin_Canvas_Compare.SetName(Save_Name.replace(".root", ""))
                Large_Bin_Canvas_Compare.SaveAs(Save_Name)
            print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))

            # Returning 'String_For_Output_txt'/'String_Input' as 'String_Output'
            return String_Output

        except:
            print(f"\n\n{color.Error}ERROR IN 'Large_Bin_Canvas_Compare'...\nTraceback:\n{color.END_B}{traceback.format_exc()}{color.END}\n")
            return String_Output
    else:
        print("\nDo not run kinematic comparisons for Multidimensional unfolding histograms...\n")
        return String_Output

######################################################################################################################################################
##==========##==========## (New) Simple Function for Drawing 2D Histograms  ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################





########################################################################################################################################################
##==========##==========## Function for Larger Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################

def Large_Individual_Bin_Images(Histogram_List_All, Default_Histo_Name, Q2_Y_Bin="All", Z_PT_Bin="All", Multi_Dim_Option="Off", String_Input=""):
    if("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]) not in Default_Histo_Name):
        Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_All)", "".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]))
        
    if(Multi_Dim_Option in ["Only"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        Default_Histo_Name = Default_Histo_Name.replace("Multi_Dim_Q2_Y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t")
        if(((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) in ["All", "0"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if(Multi_Dim_Option in ["Q2_y"])                                       else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        Default_Histo_Name = Default_Histo_Name.replace("Multi_Dim_Q2_Y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
    if(Multi_Dim_Option in ["5D"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
        Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_5D_Histo)")
    if(Multi_Dim_Option in ["3D"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
        Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_3D_Histo)")
    elif((Multi_Dim_Option not in ["Off"]) and (str(Z_PT_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")

    if(Cut_ProQ):
        Default_Histo_Name = Default_Histo_Name.replace("(Data_Type)_(SMEAR=", "(Data_Type)_(Proton)_(SMEAR=")
        
    Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
    
    Large_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS"), Num_Columns=1, Num_Rows=4, Size_X=2600, Size_Y=3200, cd_Space=0)
    Large_Bin_Canvas_Row_1 = Large_Bin_Canvas.cd(1)
    Large_Bin_Canvas_Row_2 = Large_Bin_Canvas.cd(2)
    Large_Bin_Canvas_Row_3 = Large_Bin_Canvas.cd(3)
    Large_Bin_Canvas_Row_4 = Large_Bin_Canvas.cd(4)
    Large_Bin_Canvas_Row_1.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_2.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_3.Divide(4, 2, 0, 0)
    Large_Bin_Canvas_Row_4.Divide(1, 3, 0, 0)

    if("(1D)" in str(Default_Histo_Name)):
        ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''"))]
    else:
        ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''" if(not Sim_Test) else "Smear"))]
    MC_REC_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "mdf")))]
    MC_GEN_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "gdf")).replace("Smear", "''"))]
    if(Sim_Test and ("(1D)" in str(Default_Histo_Name))):
        ExTRUE_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")))]
    elif(Sim_Test):
        ExTRUE_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''"))]
    else:
        ExTRUE_1D = "N/A"
    
    Default_Response_Matrix_Name = str(str(str(str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")).replace("Multi-Dim Histo", "Response_Matrix")).replace("MultiDim_5D_Histo", "Response_Matrix")).replace("MultiDim_3D_Histo", "Response_Matrix")
    if(Multi_Dim_Option not in ["Off"]):
        Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]),     "(z_pT_Bin_All)")
        if((("(MultiDim_Q2_y_z_pT_phi_h)" in Default_Response_Matrix_Name) or ("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Response_Matrix_Name) or ("(Multi_Dim_Q2_Y_Bin_phi_t)" in Default_Response_Matrix_Name)) and (str(Q2_Y_Bin) not in ["All", "0"])):
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(Q2_y_Bin_", str(Q2_Y_Bin), ")"]), "(Q2_y_Bin_All)")
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(Q2_Y_Bin_", str(Q2_Y_Bin), ")"]), "(Q2_Y_Bin_All)")

    Response_2D       = Histogram_List_All[Default_Response_Matrix_Name]
    
    UNFOLD_Bin        = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Bin")))]
    UNFOLD_Acceptance = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Acceptance")))]
    UNFOLD_Bay        = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Bayesian")))]

    for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
        Response_2D.SetTitle(      str(Response_2D.GetTitle()).replace(      range_strings, ""))
        UNFOLD_Bin.SetTitle(       str(UNFOLD_Bin.GetTitle()).replace(       range_strings, ""))
        UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace(range_strings, ""))
        UNFOLD_Bay.SetTitle(       str(UNFOLD_Bay.GetTitle()).replace(       range_strings, ""))
    
    Bin_Title     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All"]), "}}}"])
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    try:
        ExREAL_1D.GetXaxis().SetRange(1,         ExREAL_1D.GetXaxis().GetNbins()         + 1)
        MC_REC_1D.GetXaxis().SetRange(1,         MC_REC_1D.GetXaxis().GetNbins()         + 1)
        MC_GEN_1D.GetXaxis().SetRange(1,         MC_GEN_1D.GetXaxis().GetNbins()         + 1)
        if(ExTRUE_1D not in ["N/A"]):
            ExTRUE_1D.GetXaxis().SetRange(1,     ExTRUE_1D.GetXaxis().GetNbins()         + 1)
        Response_2D.GetXaxis().SetRange(1,       Response_2D.GetXaxis().GetNbins()       + 2)
        Response_2D.GetYaxis().SetRange(1,       Response_2D.GetYaxis().GetNbins()       + 2)
        
        UNFOLD_Bin.GetXaxis().SetRange(1,        UNFOLD_Bin.GetXaxis().GetNbins()        + 1)
        UNFOLD_Acceptance.GetXaxis().SetRange(1, UNFOLD_Acceptance.GetXaxis().GetNbins() + 1)
        UNFOLD_Bay.GetXaxis().SetRange(1,        UNFOLD_Bay.GetXaxis().GetNbins()        + 1)
    except:
        print(f"\n{color.Error}ERROR IN Axis Ranges...\nERROR:{color.END_R}\n{traceback.format_exc()}{color.END}")
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####        Legend Setup         #####==========##### ################################################################
    ##################################################################### ################################################################
    if(("phi_t" not in str(Default_Histo_Name)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(Default_Histo_Name))):
        Legends_Unfolded = ROOT.TLegend(0.5,  0.5,  0.95, 0.75)
    else:
        Legends_Unfolded = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)

    Legends_Unfolded.SetNColumns(2)
    Legends_Unfolded.SetBorderSize(0)
    Legends_Unfolded.SetFillColor(0)
    Legends_Unfolded.SetFillStyle(0)

    Legends_REC = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
    Legends_REC.SetNColumns(1)
    Legends_REC.SetBorderSize(0)
    Legends_REC.SetFillColor(0)
    Legends_REC.SetFillStyle(0)
    ##################################################################### ################################################################
    #####==========#####        Legend Setup         #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####   Experimental Histogram    #####==========##### ################################################################
    ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Experimental", "Reconstucted"))
    ExREAL_1D.GetYaxis().SetTitle("Normalized")
    ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", ""))
    ExREAL_1D.SetLineColor(root_color.Blue)
    ExREAL_1D.SetLineWidth(2)
    ExREAL_1D.SetLineStyle(1)
    ExREAL_1D.SetMarkerColor(root_color.Blue)
    ExREAL_1D.SetMarkerSize(1)
    ExREAL_1D.SetMarkerStyle(21)
    #####==========#####      MC REC Histogram       #####==========##### ################################################################
    MC_REC_1D.GetYaxis().SetTitle("Normalized")
    MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("(REC)", ""))
    MC_REC_1D.SetLineColor(root_color.Red)
    MC_REC_1D.SetLineWidth(2)
    MC_REC_1D.SetLineStyle(1)
    MC_REC_1D.SetMarkerColor(root_color.Red)
    MC_REC_1D.SetMarkerSize(1)
    MC_REC_1D.SetMarkerStyle(22)
    #####==========#####      MC GEN Histogram       #####==========##### ################################################################
    MC_GEN_1D.SetLineColor(root_color.Green)
    MC_GEN_1D.SetLineWidth(3  if("Multi" not in str(Default_Histo_Name)) else 1)
    MC_GEN_1D.SetLineStyle(1)
    MC_GEN_1D.SetMarkerColor(root_color.Green)
    MC_GEN_1D.SetMarkerSize(1 if("Multi" not in str(Default_Histo_Name)) else 0.5)
    MC_GEN_1D.SetMarkerStyle(20)
    MC_GEN_1D.GetYaxis().SetTitle("Normalized")
    #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################
    # UNFOLD_Bin.GetYaxis().SetTitle("Normalized")
    UNFOLD_Bin.SetLineColor(root_color.Brown)
    UNFOLD_Bin.SetLineWidth(2 if("Multi" not in str(Default_Histo_Name)) else 1)
    UNFOLD_Bin.SetLineStyle(1)
    UNFOLD_Bin.SetMarkerColor(root_color.Brown)
    UNFOLD_Bin.SetMarkerSize(1.5)
    UNFOLD_Bin.SetMarkerStyle(21)
    #####==========#####    Acceptance Histogram     #####==========##### ################################################################
    UNFOLD_Acceptance.SetLineColor(root_color.Red)
    UNFOLD_Acceptance.SetLineWidth(2)
    UNFOLD_Acceptance.SetMarkerColor(root_color.Red)
    #####==========#####   Unfold Bayes Histogram    #####==========##### ################################################################
    # UNFOLD_Bay.GetYaxis().SetTitle("Normalized")
    UNFOLD_Bay.SetLineColor(root_color.Teal)
    UNFOLD_Bay.SetLineWidth(2  if("Multi" not in str(Default_Histo_Name)) else 1)
    UNFOLD_Bay.SetLineStyle(1)
    UNFOLD_Bay.SetMarkerColor(root_color.Teal)
    UNFOLD_Bay.SetMarkerSize(1 if("Multi" not in str(Default_Histo_Name)) else 0.5)
    UNFOLD_Bay.SetMarkerStyle(21)
    #####==========#####      MC TRUE Histogram      #####==========##### ################################################################
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D.SetLineColor(root_color.Cyan)
        ExTRUE_1D.SetLineWidth(3  if("Multi" not in str(Default_Histo_Name)) else 1)
        ExTRUE_1D.SetLineStyle(1)
        ExTRUE_1D.SetMarkerColor(root_color.Cyan)
        ExTRUE_1D.SetMarkerSize(1 if("Multi" not in str(Default_Histo_Name)) else 0.5)
        ExTRUE_1D.SetMarkerStyle(20)
    ##################################################################### ################################################################
    #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
    ##################################################################### ################################################################
    
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    
    
    ######################################################################################
    ###==============###==============================================###==============###
    ###==============###   Openning Canvas Pads to Draw Histograms    ###==============###
    ###==============###==============================================###==============###
    ######################################################################################

    
    ########################################################################## ################################################################
    ##==========##==========##     Row 1 - CD 3     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ################################################################
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=3, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)

    Main_Histos_Title ="".join(["#splitline{#scale[1.5]{Pre-", "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolded" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolded (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of "])
    if(("phi_t" in str(Default_Histo_Name)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Default_Histo_Name))):
        ExREAL_1D.GetXaxis().SetRangeUser(0, 360)
        MC_REC_1D.GetXaxis().SetRangeUser(0, 360)
        MC_GEN_1D.GetXaxis().SetRangeUser(0, 360)
        ExREAL_1D.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_REC_1D.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_GEN_1D.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
    elif(("phi_t" not in str(Default_Histo_Name)) and ("MM" in str(Default_Histo_Name))):
        ExREAL_1D.GetXaxis().SetRangeUser(1, 3.5)
        MC_REC_1D.GetXaxis().SetRangeUser(1, 3.5)
        MC_GEN_1D.GetXaxis().SetRangeUser(1, 3.5)
        ExREAL_1D.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_REC_1D.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_GEN_1D.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
    ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(ExREAL_1D_Norm, "#scale[2]{Experimental}", "lpE")
    MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(MC_REC_1D_Norm, "#scale[2]{MC REC}", "lpE")
    MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(MC_GEN_1D_Norm, "#scale[2]{MC GEN}", "lpE")
    
    # Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
    Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()) if(ExREAL_1D_Norm and ExREAL_1D_Norm.GetEntries() > 0) else 0, MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()) if(MC_REC_1D_Norm and MC_REC_1D_Norm.GetEntries() > 0) else 0, MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin()) if(MC_GEN_1D_Norm and MC_GEN_1D_Norm.GetEntries() > 0) else 0])
    
    ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    
    configure_stat_box(hist=ExREAL_1D_Norm, show_entries=False, canvas=Large_Bin_Canvas_Row_1)
    configure_stat_box(hist=MC_REC_1D_Norm, show_entries=False, canvas=Large_Bin_Canvas_Row_1)
    configure_stat_box(hist=MC_GEN_1D_Norm, show_entries=False, canvas=Large_Bin_Canvas_Row_1)
    statbox_move(Histogram=ExREAL_1D_Norm, Canvas=Large_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_REC_1D_Norm, Canvas=Large_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=Large_Bin_Canvas_Row_1, Print_Method="off")
    # ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    
    Legends_REC.Draw("same")
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 1 - CD 4     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ################################################################
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=4, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
    Main_Histos_Title = "".join(["#splitline{#scale[1.5]{", "Unfolded" if(str(Multi_Dim_Option) in ["Off"]) else "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "".join(["#splitline{3D Unfolded}{", "Q^{2}-y-#phi_{h} Unfolding" if("(Multi_Dim_Q2_y_Bin_phi_t)" in str(Default_Histo_Name)) else "".join(["z-P_{T}-#phi_{h} Unfolding", " (Old)" if("(MultiDim_z_pT_Bin_Y_bin_phi_t)" not in str(Default_Histo_Name)) else ""]), "}"]), " Distributions of "])
    if(("phi_t" in str(Default_Histo_Name)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Default_Histo_Name))):
        UNFOLD_Bin.GetXaxis().SetRangeUser(0, 360)
        UNFOLD_Bay.GetXaxis().SetRangeUser(0, 360)
        if(ExTRUE_1D not in ["N/A"]):
            ExTRUE_1D.GetXaxis().SetRangeUser(0, 360)
            # ExTRUE_1D.SetTitle("".join(["#splitline{#scale[1.5]{Unfolded Distributions of #phi_{h}}}{#scale[1.15]{",  str(Bin_Title), "}}"]))
            ExTRUE_1D.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bin.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bay.SetTitle("".join([Main_Histos_Title, "#phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
    elif(("phi_t" not in str(Default_Histo_Name)) and ("MM" in str(Default_Histo_Name))):
        UNFOLD_Bin.GetXaxis().SetRangeUser(1, 3.5)
        UNFOLD_Bay.GetXaxis().SetRangeUser(1, 3.5)
        if(ExTRUE_1D not in ["N/A"]):
            ExTRUE_1D.GetXaxis().SetRangeUser(1, 3.5)
            ExTRUE_1D.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bin.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bay.SetTitle("".join([Main_Histos_Title, "Missing Mass}}{#scale[1.15]{", str(Bin_Title), "}}"]))
    else:
        UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
        for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
            UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace(range_strings, ""))
            UNFOLD_Bay.SetTitle(str(UNFOLD_Bay.GetTitle()).replace(range_strings, ""))
        
    UNFOLD_Bin.GetYaxis().SetTitle("Count")
    UNFOLD_Bin.Draw("H P E0 same")
    statbox_move(Histogram=UNFOLD_Bin, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bin.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bin.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bin.SetBinContent(ii,  0)
    #         UNFOLD_Bin.SetBinError(ii,    0)
    Legends_Unfolded.AddEntry(UNFOLD_Bin, "#scale[2]{Bin-by-Bin}", "lpE")


    UNFOLD_Bay.Draw("H P E0 same")
    statbox_move(Histogram=UNFOLD_Bay, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bay.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bay.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bay.SetBinContent(ii, 0)
    #         UNFOLD_Bay.SetBinError(ii,   0)
    Legends_Unfolded.AddEntry(UNFOLD_Bay, "#scale[2]{Bayesian}", "lpE")
    
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D.Draw("H P E0 same")
        statbox_move(Histogram=ExTRUE_1D, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
        # for ii in range(0, ExTRUE_1D.GetNbinsX() + 1, 1):
        #     if(ExTRUE_1D.GetBinError(ii) > 0.01):
        #         print("".join([color.RED, "\n(MC TRUE Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
        #         ExTRUE_1D.SetBinContent(ii, 0)
        #         ExTRUE_1D.SetBinError(ii,   0)
        Legends_Unfolded.AddEntry(ExTRUE_1D, "#scale[2]{MC TRUE}", "lpE")
    
    Max_Unfolded     = max([UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin()), UNFOLD_Bay.GetBinContent(UNFOLD_Bay.GetMaximumBin())])
    if(ExTRUE_1D not in ["N/A"]):
        Max_Unfolded = max([UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin()), UNFOLD_Bay.GetBinContent(UNFOLD_Bay.GetMaximumBin()), ExTRUE_1D.GetBinContent(ExTRUE_1D.GetMaximumBin())])
    
    UNFOLD_Bin.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    UNFOLD_Bay.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D.GetYaxis().SetRangeUser(0,  1.2*Max_Unfolded)
    Legends_Unfolded.Draw("same")
    ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 2     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=2, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
    ROOT.gPad.SetLogz(1)
    Response_2D.Draw("colz")
    if(Multi_Dim_Option in ["Off"]):
        Response_2D.GetXaxis().SetRangeUser(0, 360)
        Response_2D.GetYaxis().SetRangeUser(0, 360)
        
    if("y" in Binning_Method):
        Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("z_pT_Bin_y_bin_phi_t",                             "z-P_{T}-#phi_{h} Bins"))
        Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t",       "z-P_{T}-#phi_{h} Bins"))
        Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t",       "z-P_{T}-#phi_{h} Bins"))
    else:
        Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("z_pT_Bin_Y_bin_phi_t",                       "(New) z-P_{T}-#phi_{h} Bins"))
        Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h} Bins"))
        Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h} Bins"))
    
    if((Standard_Histogram_Title_Addition not in [""]) and (Standard_Histogram_Title_Addition not in str(Response_2D.GetTitle()))):
        Response_2D.SetTitle("".join(["#splitline{", str(Response_2D.GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
    
    Large_Bin_Canvas.Modified()
    Large_Bin_Canvas.Update()
    palette_move(canvas=Large_Bin_Canvas, histo=Response_2D, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 3     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##                                          ##=====##=====## ################################################################
    try:
        Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=3, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
        MC_BG__1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Background")))]
        MC_BG__1D.SetLineColor(root_color.Black)
        MC_BG__1D.SetLineWidth(2)
        MC_BG__1D.SetLineStyle(1)
        MC_BG__1D.SetMarkerColor(root_color.Black)
        MC_BG__1D.SetMarkerSize(1)
        MC_BG__1D.SetMarkerStyle(22)
        MC_BG__1D.GetXaxis().SetRangeUser(0, 360)
        MC_BG__1D.GetYaxis().SetRangeUser(0, 1.5*(MC_BG__1D.GetBinContent(MC_BG__1D.GetMaximumBin()) + MC_BG__1D.GetBinError(MC_BG__1D.GetMaximumBin())))
        MC_BG__1D.SetTitle("".join(["#splitline{#scale[1.5]{", "5D " if(str(Multi_Dim_Option) in ["5D"]) else "3D " if(str(Multi_Dim_Option) in ["3D"]) else "3D (Old) " if(str(Multi_Dim_Option) not in ["Off"]) else "", "MC Background Distributions of #phi_{h}}}{#scale[1.15]{",  str(Bin_Title), "}}"]))
        # configure_stat_box(hist=MC_BG__1D, show_entries=True, canvas=Large_Bin_Canvas)
        MC_BG__1D.Draw("H P E0 same")
        Large_Bin_Canvas.Modified()
        Large_Bin_Canvas.Update()
        # configure_stat_box(hist=MC_BG__1D, show_entries=False, canvas=Large_Bin_Canvas)
    except:
        print(f"{color.Error}Error in Large_Individual_Bin_Images():\n{color.END_B}Missing Background Plots\nTraceback:\n{color.END_R}{str(traceback.format_exc())}{color.END}")
    ##=====##=====##                                          ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 4     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=4, left_add=0.2, right_add=0.075, up_add=0.1, down_add=0.1)
    for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
        UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace(range_strings, ""))
    if((Standard_Histogram_Title_Addition not in [""]) and (Standard_Histogram_Title_Addition not in str(UNFOLD_Acceptance.GetTitle()))):
        UNFOLD_Acceptance.SetTitle("".join(["#splitline{", str(UNFOLD_Acceptance.GetTitle()), "}{",  str(Standard_Histogram_Title_Addition), "}"]))
    if("Reconstructed (MC) Distribution of" in str(UNFOLD_Acceptance.GetTitle())):
        UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace("Reconstructed (MC) Distribution of", "Bin-by-Bin Acceptance for"))
    UNFOLD_Acceptance.GetXaxis().SetRangeUser(0, 360)
    UNFOLD_Acceptance.GetYaxis().SetTitle("Acceptance")
    UNFOLD_Acceptance.Draw("same E1 H")
    Acceptance_Cut_Line.Draw()
    Large_Bin_Canvas.Modified()
    Large_Bin_Canvas.Update()
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ########################################################################## ###################################################################################################################################################################################################################################################################################################
    ##=====##=====##      Drawing the Extra 2D Histos         ##=====##=====## ###################################################################################################################################################################################################################################################################################################
    String_Input = Draw_2D_Histograms_Simple_New(Histogram_List_All_Input=Histogram_List_All, Canvas_Input=[Large_Bin_Canvas, Large_Bin_Canvas_Row_1, Large_Bin_Canvas_Row_2, Large_Bin_Canvas_Row_3, Large_Bin_Canvas_Row_4], Default_Histo_Name_Input=str(str(str(str(Default_Histo_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")).replace("(Multi_Dim_Q2_y_Bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_y_bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_Y_bin_phi_t)", "(phi_t)")).replace("(MultiDim_Q2_y_z_pT_phi_h)", "(phi_t)"), Q2_Y_Bin_Input=Q2_Y_Bin, Z_PT_Bin_Input=Z_PT_Bin, String_Output=String_Input)
    ##=====##=====##      Drawing the Extra 2D Histos         ##=====##=====## ###################################################################################################################################################################################################################################################################################################
    ########################################################################## ###################################################################################################################################################################################################################################################################################################
    ########################################################################## ################################################################
    
    #########################################################################################################################
    ##==================================#################################################==================================##
    ##==========##==========##==========##    Done Drawing Histograms to Canvas Pads   ##==========##==========##==========##
    ##==================================#################################################==================================##
    #########################################################################################################################
    
    
    
    ##################################################################### ################################################################
    #####==========#####        Saving Canvas        #####==========##### ################################################################
    ##################################################################### ################################################################
    if(("phi_t)" in Default_Histo_Name) or ("phi_h)" in Default_Histo_Name)):
        Save_Name = "".join(["Response_Matrix_Normal_Q2_y_Bin_", str(Q2_Y_Bin), "_z_pT_Bin_", str(Z_PT_Bin), "".join(["_Smeared", str(File_Save_Format)]) if("Smear" in Default_Histo_Name) else str(File_Save_Format)])
    else:
        Save_Name = str("".join([str(Default_Histo_Name), str(File_Save_Format)]).replace("(", "")).replace(")", "")
        Save_Name = Save_Name.replace("_Data_Type_SMEAR=''",        "")
        if("_Data_Type_SMEAR=Smear" in str(Save_Name)):
            Save_Name = Save_Name.replace("_Data_Type_SMEAR=Smear", "")
            Save_Name = Save_Name.replace(str(File_Save_Format), "".join(["_Smeared", str(File_Save_Format)]))
            Save_Name = Save_Name.replace("".join(["_Smeared_Smeared", str(File_Save_Format)]), "".join(["_Smeared", str(File_Save_Format)]))
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim",  "Multi_Dim_Histo"))
    if(any(binning in Binning_Method for binning in ["y", "Y"])):
        Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
    if(Multi_Dim_Option not in ["Off", "5D", "3D"]):
        Save_Name =    f"Multi_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Multi_Dim_Option     in ["5D"]):
        Save_Name = f"Multi_5D_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Multi_Dim_Option     in ["3D"]):
        Save_Name = f"Multi_3D_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Sim_Test):
        Save_Name = f"Sim_Test_{Save_Name}"
    if(Mod_Test):
        Save_Name = f"Mod_Test_{Save_Name}"
    Save_Name = Save_Name.replace("Multi_5D_Unfold_5D_Response_Matrix_Normal", "Multi_5D_Unfold_Response_Matrix_Normal")
    Save_Name = Save_Name.replace("Multi_3D_Unfold_3D_Response_Matrix_Normal", "Multi_3D_Unfold_Response_Matrix_Normal")
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                            "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]),       str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                        "_")
    if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
    elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            Large_Bin_Canvas.SetName(Save_Name.replace(".root", ""))
        Large_Bin_Canvas.SaveAs(Save_Name)
        del Large_Bin_Canvas
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################
    #####==========#####        Saving Canvas        #####==========##### ################################################################
    ##################################################################### ################################################################
    
    # Returning 'String_For_Output_txt' as 'String_Input'
    return String_Input

    
    
########################################################################################################################################################
##==========##==========## Function for Larger Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################





####################################################################################################################################################################
##==========##==========## Function for Smaller (Unfolded) Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
####################################################################################################################################################################

def Unfolded_Individual_Bin_Images(Histogram_List_All, Default_Histo_Name, Q2_Y_Bin="All", Z_PT_Bin="All", Multi_Dim_Option="Off"):
    if("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]) not in Default_Histo_Name):
        Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_All)", "".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]))
        
    # if(Multi_Dim_Option in ["Only"]):
    #     Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
    #     Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
    if(Multi_Dim_Option in ["Only"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) not in ["All", "0"])):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        Default_Histo_Name = str(Default_Histo_Name.replace("Multi_Dim_Q2_Y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t"))
        Default_Histo_Name = str(Default_Histo_Name.replace("Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t"))
    if(Multi_Dim_Option in ["5D"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
        Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_5D_Histo)")
    if(Multi_Dim_Option in ["3D"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
        Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_3D_Histo)")
            
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if(Multi_Dim_Option in ["Q2_y"])                                       else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")

    if(("(1D)" in Default_Histo_Name) and (("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Histo_Name) or ("(Multi_Dim_Q2_Y_Bin_phi_t)" in Default_Histo_Name)) and (str(Q2_Y_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        
    Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_0)",          "(z_pT_Bin_All)")

    if(Cut_ProQ):
        Default_Histo_Name = Default_Histo_Name.replace("(Data_Type)_(SMEAR=", "(Data_Type)_(Proton)_(SMEAR=")
    
    if(Fit_Test):
        fit_function_title         = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if(Multi_Dim_Option in ["Off"]):
            if(not extra_function_terms):
                fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
            else:
                fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
        elif(Multi_Dim_Option     in ["5D"]):
            fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))}{5D Unfolding}"])
        elif(Multi_Dim_Option     in ["3D"]):
            fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))}{3D Unfolding}"])
        elif(Multi_Dim_Option not in ["Fitted", "Only"]):
            fit_function_title = "".join(["Plotted with #splitline{#color[", str(root_color.Pink), "]{Multidimensional Unfolding}}{",                       "Q^{2}-y-#phi_{h} Unfolding" if(str(Z_PT_Bin) in ["All", "0"]) else "z-P_{T}-#phi_{h} Unfolding", "}"])
        else:
            if(not extra_function_terms):
                fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))}{",                    "Q^{2}-y-#phi_{h} Unfolding" if((Multi_Dim_Option in ["Q2_y"]) or ((str(Z_PT_Bin) in ["All", "0"]) and (Multi_Dim_Option not in ["z_pT"]))) else "z-P_{T}-#phi_{h} Unfolding", "}"])
            else:
                fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))}{", "Q^{2}-y-#phi_{h} Unfolding" if((Multi_Dim_Option in ["Q2_y"]) or ((str(Z_PT_Bin) in ["All", "0"]) and (Multi_Dim_Option not in ["z_pT"]))) else "z-P_{T}-#phi_{h} Unfolding", "}"])
        # else:
        #     if(not extra_function_terms):
        #         fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))}{",                    "Q^{2}-y-#phi_{h} Unfolding" if(str(Z_PT_Bin) in ["All", "0"]) else "z-P_{T}-#phi_{h} Unfolding", "}"])
        #     else:
        #         fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))}{", "Q^{2}-y-#phi_{h} Unfolding" if(str(Z_PT_Bin) in ["All", "0"]) else "z-P_{T}-#phi_{h} Unfolding", "}"])
    else:
        fit_function_title = ""
    Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All", "}"]), "}}"])
    Bin_Title = Bin_Title.replace("Common_Int", "Integrated (Over Common Range)")
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])
    Sector_Title, Sector__Save = "", ""
    if(any(sec in Default_Histo_Name for sec in ["pipsec_", "esec_"])):
        Sector_Title = "#pi^{+} Sector !" if("pipsec_" in str(Default_Histo_Name)) else "Electron Sector !"
        Sector__Save = "pipsec_!"         if("pipsec_" in str(Default_Histo_Name)) else "esec_!"
        for sec in range(1, 7):
            if(f"sec_{sec}" in str(Default_Histo_Name)):
                Sector_Title = Sector_Title.replace("!", str(sec))
                Sector__Save = Sector__Save.replace("!", str(sec))
                break
        # if("pipsec_" not in str(Default_Histo_Name)):
        #     print(f"\nDefault_Histo_Name = {Default_Histo_Name}\n")
    if(Sector_Title not in [""]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{{Sector_Title}}}"
    
    Small_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS_Unfolded"), Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1100, cd_Space=0)
    Small_Bin_Canvas_Row_1 = Small_Bin_Canvas.cd(1)
    Small_Bin_Canvas_Row_2 = Small_Bin_Canvas.cd(2)
    # Small_Bin_Canvas_Row_1.Divide(2 if(Multi_Dim_Option in ["Off"]) else 1, 1, 0)
    Small_Bin_Canvas_Row_1.Divide(2, 1, 0)
    Small_Bin_Canvas_Row_2.Divide(2, 1, 0)

    if("z_pT_Bin_Integrated" not in Default_Histo_Name):
        ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''" if((not Sim_Test) or ("(1D)" in str(Default_Histo_Name))) else "Smear"))]
        MC_REC_1D = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "mdf"))]
        MC_GEN_1D = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "gdf")).replace("Smear", "''")]
    else:
        ExREAL_1D_name = str(str(Default_Histo_Name.replace("Data_Type",               "rdf")).replace("Smear", "''" if((not Sim_Test) or ("(1D)" in str(Default_Histo_Name))) else "Smear"))
        MC_REC_1D_name = str(Default_Histo_Name.replace("Data_Type",                   "mdf"))
        MC_GEN_1D_name = str(Default_Histo_Name.replace("Data_Type",                   "gdf")).replace("Smear", "''")
        for names in [ExREAL_1D_name, MC_REC_1D_name, MC_GEN_1D_name]:
            if(names not in Histogram_List_All):
                if(names == ExREAL_1D_name):
                    ExREAL_1D_name = ExREAL_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
                if(names == MC_REC_1D_name):
                    MC_REC_1D_name = MC_REC_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
                if(names == MC_GEN_1D_name):
                    MC_GEN_1D_name = MC_GEN_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
        ExREAL_1D = Histogram_List_All[ExREAL_1D_name]
        MC_REC_1D = Histogram_List_All[MC_REC_1D_name]
        MC_GEN_1D = Histogram_List_All[MC_GEN_1D_name]
        del ExREAL_1D_name
        del MC_REC_1D_name
        del MC_GEN_1D_name
    
    if(Sim_Test):
        # ExREAL_1D = MC_REC_1D
        if("(1D)" in str(Default_Histo_Name)):
            ExTRUE_1D = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "tdf"))]
        else:
            ExTRUE_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''"))]
    else:
        # ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''"))]
        ExTRUE_1D = "N/A"

    # print(f"Default_Histo_Name            = {Default_Histo_Name}")
    UNFOLD_Bin = Histogram_List_All[str(Default_Histo_Name.replace('Data_Type',      'Bin'))].Clone(f"{Histogram_List_All[str(Default_Histo_Name.replace('Data_Type',      'Bin'))].GetName()}__Bin_{Sector__Save}")
    # print(f"Default_Histo_Name (Bin)      = {Default_Histo_Name.replace('Data_Type', 'Bin')}")
    UNFOLD_Bay = Histogram_List_All[str(Default_Histo_Name.replace('Data_Type',      'Bayesian'))].Clone(f"{Histogram_List_All[str(Default_Histo_Name.replace('Data_Type', 'Bayesian'))].GetName()}__Bay_{Sector__Save}")
    # print(f"Default_Histo_Name (Bayesian) = {Default_Histo_Name.replace('Data_Type', 'Bayesian')}")
    if(UNFOLD_Bin.GetName() == UNFOLD_Bay.GetName()):
        UNFOLD_Bin.SetName(f"{UNFOLD_Bin.GetName()}_Bin")
        UNFOLD_Bay.SetName(f"{UNFOLD_Bay.GetName()}_Bay")
        print(f"UNFOLD_Bin.GetName() = {UNFOLD_Bin.GetName()}")
        print(f"UNFOLD_Bay.GetName() = {UNFOLD_Bay.GetName()}")
    # print("")
    
    # if(Multi_Dim_Option in ["Off"]):
    #     UNFOLD_SVD = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "SVD"))]
    
    # if((Multi_Dim_Option in ["Fitted", "Only"]) and ((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) in ["All", "0"]))):
    #     Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("1D", "Multi-Dim Histo"))
    #     UNFOLD_Bin_Multi_Dim         = Histogram_List_All[str(str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "Bin"))).replace("(phi_t)",              "".join(["(Multi_Dim_", "Q2_y_Bin_" if(str(Z_PT_Bin) in ["All", "0"]) else "z_pT_Bin_y_bin_", "phi_t)"]))]
    #     UNFOLD_Bay_Multi_Dim         = Histogram_List_All[str(str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "Bayesian"))).replace("(phi_t)",         "".join(["(Multi_Dim_", "Q2_y_Bin_" if(str(Z_PT_Bin) in ["All", "0"]) else "z_pT_Bin_y_bin_", "phi_t)"]))]
    # if((Multi_Dim_Option in ["Fitted", "Only"]) and ((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) in ["All", "0"]))):
    #     UNFOLD_Bin                   = UNFOLD_Bin_Multi_Dim
    #     UNFOLD_Bay                   = UNFOLD_Bay_Multi_Dim
    #     ExREAL_1D                    = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''")).replace("(phi_t)", "".join(["(Multi_Dim_", "Q2_y_Bin_" if(str(Z_PT_Bin) in ["All", "0"]) else "z_pT_Bin_y_bin_", "phi_t)"]))]
    #     MC_REC_1D                    = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "mdf"))).replace("(phi_t)",                        "".join(["(Multi_Dim_", "Q2_y_Bin_" if(str(Z_PT_Bin) in ["All", "0"]) else "z_pT_Bin_y_bin_", "phi_t)"]))]
    #     MC_GEN_1D                    = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "gdf")).replace("Smear", "''")).replace("(phi_t)", "".join(["(Multi_Dim_", "Q2_y_Bin_" if(str(Z_PT_Bin) in ["All", "0"]) else "z_pT_Bin_y_bin_", "phi_t)"]))]
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    try:
        ExREAL_1D.GetXaxis().SetRange(1,      ExREAL_1D.GetXaxis().GetNbins()  + 1)
        MC_REC_1D.GetXaxis().SetRange(1,      MC_REC_1D.GetXaxis().GetNbins()  + 1)
        MC_GEN_1D.GetXaxis().SetRange(1,      MC_GEN_1D.GetXaxis().GetNbins()  + 1)
        if(ExTRUE_1D not in ["N/A"]):
            ExTRUE_1D.GetXaxis().SetRange(1,  ExTRUE_1D.GetXaxis().GetNbins()  + 1)
        UNFOLD_Bin.GetXaxis().SetRange(1,     UNFOLD_Bin.GetXaxis().GetNbins() + 1)
        UNFOLD_Bay.GetXaxis().SetRange(1,     UNFOLD_Bay.GetXaxis().GetNbins() + 1)
        # if(Multi_Dim_Option in ["Off"]):
        #     UNFOLD_SVD.GetXaxis().SetRange(1, UNFOLD_SVD.GetXaxis().GetNbins() + 1)
        
        if(("phi_t" in str(Default_Histo_Name)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Default_Histo_Name))):
            ExREAL_1D.GetXaxis().SetRangeUser(0,  360)
            MC_REC_1D.GetXaxis().SetRangeUser(0,  360)
            MC_GEN_1D.GetXaxis().SetRangeUser(0,  360)
            UNFOLD_Bin.GetXaxis().SetRangeUser(0, 360)
            UNFOLD_Bay.GetXaxis().SetRangeUser(0, 360)
            # if(Multi_Dim_Option in ["Off"]):
            #     UNFOLD_SVD.GetXaxis().SetRangeUser(0, 360)
            if(ExTRUE_1D not in ["N/A"]):
                ExTRUE_1D.GetXaxis().SetRangeUser(0,  360)
            # if(Multi_Dim_Option not in ["Off", "Fitted", "Only"]):
            #     UNFOLD_Bin_Multi_Dim.GetXaxis().SetRangeUser(0, 360)
            #     UNFOLD_Bay_Multi_Dim.GetXaxis().SetRangeUser(0, 360)
    except:
        print("".join([color.Error, "\nERROR IN Axis Ranges...", color.END]))
        print("".join([color.Error,   "ERROR:\n",                color.END_R, str(traceback.format_exc()), color.END]))
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####        Legend Setup         #####==========##### ################################################################
    ##################################################################### ################################################################
    Legends_REC = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
    Legends_REC.SetNColumns(1)
    Legends_REC.SetBorderSize(0)
    Legends_REC.SetFillColor(0)
    Legends_REC.SetFillStyle(0)
    ##################################################################### ################################################################
    #####==========#####        Legend Setup         #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
    ##################################################################### ################################################################
    DRAW_NORMALIZE = True
    DRAW_NORMALIZE = False    
    ##################################################################### ################################################################
    #####==========#####   Experimental Histogram    #####==========##### ################################################################
    
    ExREAL_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolded" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolded (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
    ExREAL_1D.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
    ExREAL_1D.SetLineColor(root_color.Blue)
    ExREAL_1D.SetLineWidth(2)
    ExREAL_1D.SetLineStyle(1)
    ExREAL_1D.SetMarkerColor(root_color.Blue)
    ExREAL_1D.SetMarkerSize(1)
    ExREAL_1D.SetMarkerStyle(21)
    if(DRAW_NORMALIZE):
        ExREAL_1D.GetYaxis().SetTitle("Normalized")
    else:
        ExREAL_1D.GetYaxis().SetTitle("")
    #####==========#####      MC REC Histogram       #####==========##### ################################################################
    MC_REC_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolded" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolded (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
    MC_REC_1D.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
    MC_REC_1D.SetLineColor(root_color.Red)
    MC_REC_1D.SetLineWidth(2)
    MC_REC_1D.SetLineStyle(1)
    MC_REC_1D.SetMarkerColor(root_color.Red)
    MC_REC_1D.SetMarkerSize(1)
    MC_REC_1D.SetMarkerStyle(22)
    if(DRAW_NORMALIZE):
        MC_REC_1D.GetYaxis().SetTitle("Normalized")
    else:
        MC_REC_1D.GetYaxis().SetTitle("")
    #####==========#####      MC GEN Histogram       #####==========##### ################################################################ ################################################################
    MC_GEN_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolded" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolded (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
    MC_GEN_1D.SetLineColor(root_color.Green)
    MC_GEN_1D.SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
    MC_GEN_1D.SetLineStyle(1)
    MC_GEN_1D.SetMarkerColor(root_color.Green)
    MC_GEN_1D.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
    MC_GEN_1D.SetMarkerStyle(20)
    if(DRAW_NORMALIZE):
        MC_GEN_1D.GetYaxis().SetTitle("Normalized")
    else:
        MC_GEN_1D.GetYaxis().SetTitle("")
    #####==========#####      MC TRUE Histogram      #####==========##### ################################################################ ################################################################
    if(ExTRUE_1D not in ["N/A"]):
        # ExTRUE_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "5D Unfolded" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolded" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolded (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
        ExTRUE_1D.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Cyan), "]{True} Distribution of #phi_{h}}}{",             root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
        ExTRUE_1D.SetLineColor(root_color.Cyan)
        ExTRUE_1D.SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
        ExTRUE_1D.SetLineStyle(1)
        ExTRUE_1D.SetMarkerColor(root_color.Cyan)
        ExTRUE_1D.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
        ExTRUE_1D.SetMarkerStyle(20)
        if(DRAW_NORMALIZE):
            ExTRUE_1D.GetYaxis().SetTitle("Normalized")
        else:
            ExTRUE_1D.GetYaxis().SetTitle("")
    #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################ ################################################################ ################################################################
    UNFOLD_Bin.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Brown), "]{Bin-By-Bin} Distribution of #phi_{h}}}{",         root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
    UNFOLD_Bin.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
    UNFOLD_Bin.SetLineColor(root_color.Brown)
    UNFOLD_Bin.SetLineWidth(2)
    UNFOLD_Bin.SetLineStyle(1)
    UNFOLD_Bin.SetMarkerColor(root_color.Brown)
    UNFOLD_Bin.SetMarkerSize(1.5)
    UNFOLD_Bin.SetMarkerStyle(21)
    if(DRAW_NORMALIZE):
        UNFOLD_Bin.GetYaxis().SetTitle("Normalized")
    else:
        UNFOLD_Bin.GetYaxis().SetTitle("")
    # if(Multi_Dim_Option not in ["Off", "Fitted", "Only"]):
    #     UNFOLD_Bin_Multi_Dim.SetMarkerColor(root_color.Pink)
    #     UNFOLD_Bin_Multi_Dim.SetLineWidth(2)
    #     UNFOLD_Bin_Multi_Dim.SetLineStyle(1)
    #     UNFOLD_Bin_Multi_Dim.SetLineColor(root_color.Pink)
    #     UNFOLD_Bin_Multi_Dim.SetMarkerSize(1)
    #     UNFOLD_Bin_Multi_Dim.SetMarkerStyle(21)
    #####==========#####   Unfold Bayes Histogram    #####==========##### ################################################################ ################################################################ ################################################################
    UNFOLD_Bay.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Teal),  "]{RooUnfold Bayesian} Distribution of #phi_{h}}}{", root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
    UNFOLD_Bay.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
    UNFOLD_Bay.SetLineColor(root_color.Teal)
    UNFOLD_Bay.SetLineWidth(2)
    UNFOLD_Bay.SetLineStyle(1)
    UNFOLD_Bay.SetMarkerColor(root_color.Teal)
    UNFOLD_Bay.SetMarkerSize(1)
    UNFOLD_Bay.SetMarkerStyle(21)
    if(DRAW_NORMALIZE):
        UNFOLD_Bay.GetYaxis().SetTitle("Normalized")
    else:
        UNFOLD_Bay.GetYaxis().SetTitle("")
    # if(Multi_Dim_Option not in ["Off", "Fitted", "Only"]):
    #     UNFOLD_Bay_Multi_Dim.SetMarkerColor(root_color.Pink)
    #     UNFOLD_Bay_Multi_Dim.SetLineWidth(2)
    #     UNFOLD_Bay_Multi_Dim.SetLineStyle(1)
    #     UNFOLD_Bay_Multi_Dim.SetLineColor(root_color.Pink)
    #     UNFOLD_Bay_Multi_Dim.SetMarkerSize(1)
    #     UNFOLD_Bay_Multi_Dim.SetMarkerStyle(21)
    #####==========#####    Unfold SVD Histogram     #####==========##### ################################################################ ################################################################ ################################################################
    # if(Multi_Dim_Option in ["Off"]):
    #     UNFOLD_SVD.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Pink),  "]{SVD Unfolded} Distribution of #phi_{h}}}{",       root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
    #     UNFOLD_SVD.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
    #     UNFOLD_SVD.SetMarkerColor(root_color.Pink)
    #     UNFOLD_SVD.SetLineWidth(2)
    #     UNFOLD_SVD.SetLineStyle(1)
    #     UNFOLD_SVD.SetLineColor(root_color.Pink)
    #     UNFOLD_SVD.SetMarkerSize(1)
    #     UNFOLD_SVD.SetMarkerStyle(21)
    #     if(DRAW_NORMALIZE):
    #         UNFOLD_SVD.GetYaxis().SetTitle("Normalized")
    #     else:
    #         UNFOLD_SVD.GetYaxis().SetTitle("")
    ##################################################################### ################################################################ ################################################################ ################################################################
    #####==========#####  Setting Histogram Colors   #####==========##### ################################################################ ################################################################
    ##################################################################### ################################################################
    
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    
    
    ######################################################################################
    ###==============###==============================================###==============###
    ###==============###   Openning Canvas Pads to Draw Histograms    ###==============###
    ###==============###==============================================###==============###
    ######################################################################################
    
    
    ########################################################################## ###################################################################
    ##==========##==========##     Row 1 - CD 1     ##==========##==========## ###################################################################
    ########################################################################## ###################################################################
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ###################################################################
    # Draw_Canvas(canvas=Small_Bin_Canvas_Row_1, cd_num=1, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
    Draw_Canvas(Small_Bin_Canvas_Row_1, 1, 0.15)
    # ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H PL E0 same")
    # MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H PL E0 same")
    # MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H PL E0 same")
    ExREAL_1D_Norm     = ExREAL_1D.DrawNormalized("H P E0 same")
    MC_REC_1D_Norm     = MC_REC_1D.DrawNormalized("H P E0 same")
    MC_GEN_1D_Norm     = MC_GEN_1D.DrawNormalized("H P E0 same")
    configure_stat_box(hist=ExREAL_1D_Norm, show_entries=False, canvas=Small_Bin_Canvas_Row_1)
    configure_stat_box(hist=MC_REC_1D_Norm, show_entries=False, canvas=Small_Bin_Canvas_Row_1)
    configure_stat_box(hist=MC_GEN_1D_Norm, show_entries=False, canvas=Small_Bin_Canvas_Row_1)
    statbox_move(Histogram=ExREAL_1D_Norm, Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_REC_1D_Norm, Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=ExREAL_1D,      Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_REC_1D,      Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    statbox_move(Histogram=MC_GEN_1D,      Canvas=Small_Bin_Canvas_Row_1, Print_Method="off")
    ExREAL_1D_Norm.SetStats(0)
    MC_REC_1D_Norm.SetStats(0)
    MC_GEN_1D_Norm.SetStats(0)
    # if(Fit_Test):
    #     try:
    #         statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=Small_Bin_Canvas_Row_1.cd(1), Print_Method="off")
    #     except:
    #         print("\nMC_GEN_1D IS NOT FITTED\n")
    # if(ExTRUE_1D not in ["N/A"]):
    #     try:
    #         statbox_move(Histogram=ExTRUE_1D_Norm, Canvas=Small_Bin_Canvas_Row_1.cd(1), Print_Method="off")
    #     except:
    #         print("\nExTRUE_1D IS NOT FITTED\n")
        
    Max_Pre_Unfolded     = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
    # if(ExTRUE_1D not in ["N/A"]):
    #     Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin()), ExTRUE_1D_Norm.GetBinContent(ExTRUE_1D_Norm.GetMaximumBin())])
        
    ExREAL_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    MC_REC_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    # if(ExTRUE_1D not in ["N/A"]):
    #     ExTRUE_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
        
    Legends_REC.AddEntry(ExREAL_1D_Norm,     "#scale[2]{Experimental}", "lpE")
    Legends_REC.AddEntry(MC_REC_1D_Norm,     "#scale[2]{MC REC}",       "lpE")
    Legends_REC.AddEntry(MC_GEN_1D_Norm,     "#scale[2]{MC GEN}",       "lpE")
    # if(ExTRUE_1D not in ["N/A"]):
    #     Legends_REC.AddEntry(ExTRUE_1D_Norm, "#scale[2]{MC TRUE}",       "lpE")
    Legends_REC.Draw("same")
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ###################################################################
    ########################################################################## ###################################################################
    ##==========##==========##     Row 2 - CD 1     ##==========##==========## ###################################################################
    ########################################################################## ###################################################################
    ##=====##=====##     Drawing the Bayesian Histograms      ##=====##=====## ###################################################################
    Draw_Canvas(Small_Bin_Canvas_Row_2, 1, 0.15)
    if(DRAW_NORMALIZE):
        # UNFOLD_Bay_Norm = UNFOLD_Bay.DrawNormalized("H PL E0 same")
        UNFOLD_Bay_Norm = UNFOLD_Bay.DrawNormalized("H P E0 same")
        UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bay_Norm.GetBinContent(UNFOLD_Bay_Norm.GetMaximumBin())))
        
        for ii in range(0, UNFOLD_Bay_Norm.GetNbinsX() + 1, 1):
            if(UNFOLD_Bay_Norm.GetBinError(ii) > 0.01):
                print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                UNFOLD_Bay_Norm.SetBinContent(ii, 0)
                UNFOLD_Bay_Norm.SetBinError(ii,   0)
        if(Fit_Test):
            # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
            UNFOLD_Bay_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bay_Norm, Method="bayes", Special=[Q2_Y_Bin, Z_PT_Bin])
            # UNFOLD_Bay_Fitted[1].Draw("H PL E0 same")
            UNFOLD_Bay_Fitted[1].Draw("H P E0 same")
            statbox_move(Histogram=UNFOLD_Bay_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            # else:
            #     UNFOLD_Bay_Multi_Dim.DrawNormalized("H PL E0 same")
            #     maximum = max([UNFOLD_Bay_Norm.GetMaximum, UNFOLD_Bay_Multi_Dim.GetMaximum])
            #     UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0,      1.2*maximum)
            #     UNFOLD_Bay_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
            
    else:
        # UNFOLD_Bay.Draw("H PL E0 same")
        UNFOLD_Bay.Draw("H P E0 same")
        configure_stat_box(hist=UNFOLD_Bay, show_entries=True, canvas=Small_Bin_Canvas)
        UNFOLD_Bay.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bay.GetBinContent(UNFOLD_Bay.GetMaximumBin())))
        statbox_move(Histogram=UNFOLD_Bay, Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
        #     UNFOLD_Bay_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bay)
        #     UNFOLD_Bay_Fitted[1].Draw("same")
        #     statbox_move(Histogram=UNFOLD_Bay_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # else:
        #     UNFOLD_Bay_Multi_Dim.Draw("H PL E0 same")
        #     maximum = max([UNFOLD_Bay.GetMaximum, UNFOLD_Bay_Multi_Dim.GetMaximum])
        #     UNFOLD_Bay.GetYaxis().SetRangeUser(0,           1.2*maximum)
        #     UNFOLD_Bay_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
    ##=====##=====##     Drawing the Bayesian Histograms      ##=====##=====## ###################################################################
    ########################################################################## ###################################################################
    ##==========##==========##     Row 1 - CD 2     ##==========##==========## ###################################################################
    ########################################################################## ###################################################################
    ##=====##=====##    Drawing the 'True' Histogram          ##=====##=====## ###################################################################
    if(ExTRUE_1D not in ["N/A"]):
        Draw_Canvas(Small_Bin_Canvas_Row_1, 2, 0.15)
        if(DRAW_NORMALIZE):
            ExTRUE_1D_Norm = ExTRUE_1D.DrawNormalized("H P E0 same")
            ExTRUE_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*(ExTRUE_1D_Norm.GetBinContent(ExTRUE_1D_Norm.GetMaximumBin())))
            for ii in range(0, ExTRUE_1D_Norm.GetNbinsX() + 1, 1):
                if(ExTRUE_1D_Norm.GetBinError(ii) > 0.01):
                    print("".join([color.RED, "\n(tdf) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                    ExTRUE_1D_Norm.SetBinContent(ii, 0)
                    ExTRUE_1D_Norm.SetBinError(ii,   0)
            if(Fit_Test):
                UNFOLD_SVD_Fitted = Fitting_Phi_Function(Histo_To_Fit=ExTRUE_1D_Norm, Method="tdf", Special=[Q2_Y_Bin, Z_PT_Bin])
                UNFOLD_SVD_Fitted[1].Draw("H P E0 same")
                statbox_move(Histogram=UNFOLD_SVD_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        else:
            ExTRUE_1D.Draw("H P E0 same")
            configure_stat_box(hist=ExTRUE_1D, show_entries=True, canvas=Small_Bin_Canvas)
            ExTRUE_1D.GetYaxis().SetRangeUser(0, 1.2*(ExTRUE_1D.GetBinContent(ExTRUE_1D.GetMaximumBin())))
            statbox_move(Histogram=ExTRUE_1D, Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            # ExTRUE_1D_Fitted = Fitting_Phi_Function(Histo_To_Fit=ExTRUE_1D)
            # ExTRUE_1D_Fitted[1].Draw("same")
            # statbox_move(Histogram=ExTRUE_1D_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
    ##=====##=====##    Drawing the SVD Unfold Histograms     ##=====##=====## ###################################################################
    ########################################################################## ###################################################################
    ##==========##==========##     Row 2 - CD 2     ##==========##==========## ###################################################################
    ########################################################################## ###################################################################
    ##=====##=====##    Drawing the Bin-by-Bin Histograms     ##=====##=====## ###################################################################
    Draw_Canvas(Small_Bin_Canvas_Row_2, 2, 0.15)
    if(DRAW_NORMALIZE):
        # UNFOLD_Bin_Norm = UNFOLD_Bin.DrawNormalized("H PL E0 same")
        UNFOLD_Bin_Norm = UNFOLD_Bin.DrawNormalized("H P E0 same")
        UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bin_Norm.GetBinContent(UNFOLD_Bin_Norm.GetMaximumBin())))
        for ii in range(0, UNFOLD_Bin_Norm.GetNbinsX() + 1, 1):
            if(UNFOLD_Bin_Norm.GetBinError(ii) > 0.01):
                print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                UNFOLD_Bin_Norm.SetBinContent(ii,  0)
                UNFOLD_Bin_Norm.SetBinError(ii,    0)
        if(Fit_Test):
            # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
            UNFOLD_Bin_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bin_Norm, Method="bbb", Special=[Q2_Y_Bin, Z_PT_Bin])
            # UNFOLD_Bin_Fitted[1].Draw("H PL E0 same")
            UNFOLD_Bin_Fitted[1].Draw("H P E0 same")
            configure_stat_box(hist=UNFOLD_Bin_Fitted[1], show_entries=True, canvas=Small_Bin_Canvas)
            statbox_move(Histogram=UNFOLD_Bin_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            # else:
            #     UNFOLD_Bin_Multi_Dim.DrawNormalized("H PL E0 same")
            #     maximum = max([UNFOLD_Bin_Norm.GetMaximum, UNFOLD_Bin_Multi_Dim.GetMaximum])
            #     UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0,      1.2*maximum)
            #     UNFOLD_Bin_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
    else:
        # UNFOLD_Bin.Draw("H PL E0 same")
        UNFOLD_Bin.Draw("H P E0 same")
        UNFOLD_Bin.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin())))
        configure_stat_box(hist=UNFOLD_Bin, show_entries=True, canvas=Small_Bin_Canvas)
        statbox_move(Histogram=UNFOLD_Bin, Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
        #     UNFOLD_Bin_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bin)
        #     UNFOLD_Bin_Fitted[1].Draw("same")
        #     statbox_move(Histogram=UNFOLD_Bin_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # else:
        #     UNFOLD_Bin_Multi_Dim.Draw("H PL E0 same")
        #     maximum = max([UNFOLD_Bin.GetMaximum, UNFOLD_Bin_Multi_Dim.GetMaximum])
        #     UNFOLD_Bin.GetYaxis().SetRangeUser(0,           1.2*maximum)
        #     UNFOLD_Bin_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
    ##=====##=====##    Drawing the Bin-by-Bin Histograms     ##=====##=====## ###################################################################
    ########################################################################## ###################################################################


    #########################################################################################################################
    ##==================================#################################################==================================##
    ##==========##==========##==========##    Done Drawing Histograms to Canvas Pads   ##==========##==========##==========##
    ##==================================#################################################==================================##
    #########################################################################################################################
    
    
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    if(("phi_t)" in Default_Histo_Name) or ("phi_h)" in Default_Histo_Name)):
        Save_Name = "".join(["Response_Matrix_Normal_Q2_xB_Bin_", str(Q2_Y_Bin) if(str(Q2_Y_Bin) not in ["0"]) else "All", "_z_pT_Bin_", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All", "".join(["_Unfolded_Histos_Smeared", str(File_Save_Format)]) if("Smear" in Default_Histo_Name) else "".join(["_Unfolded_Histos", str(File_Save_Format)])])    
    else:
        Save_Name = str("".join([str(Default_Histo_Name), "_Unfolded_Histos", str(File_Save_Format)]).replace("(", "")).replace(")", "")
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
    if(any(binning in Binning_Method for binning in ["y", "Y"])):
        Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
    if(Multi_Dim_Option not in ["Off", "5D", "3D"]):
        Save_Name =    f"Multi_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Multi_Dim_Option     in ["5D"]):
        Save_Name = f"Multi_5D_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Multi_Dim_Option     in ["3D"]):
        Save_Name = f"Multi_3D_Unfold_{Multi_Dim_Option}_{Save_Name}"
    if(Sim_Test):
        Save_Name = f"Sim_Test_{Save_Name}"
    if(Mod_Test):
        Save_Name = f"Mod_Test_{Save_Name}"
    if(Sector__Save not in [""]):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_{Sector__Save}{File_Save_Format}")
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                            "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("Multi_5D_Unfold_5D_MultiDim_5D",            "Multi_5D_Unfold")
    Save_Name = Save_Name.replace("Multi_5D_Unfold_5D_Response_Matrix_Normal", "Multi_5D_Unfold_Response_Matrix_Normal")
    Save_Name = Save_Name.replace("Multi_3D_Unfold_3D_MultiDim_3D",            "Multi_3D_Unfold")
    Save_Name = Save_Name.replace("Multi_3D_Unfold_3D_Response_Matrix_Normal", "Multi_3D_Unfold_Response_Matrix_Normal")
    Save_Name = Save_Name.replace(f"_{File_Save_Format}",                      str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                        "_")
    if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
    elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            Small_Bin_Canvas.SetName(Save_Name.replace(".root", ""))
        Small_Bin_Canvas.SaveAs(Save_Name)
        # del Small_Bin_Canvas
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################

    
####################################################################################################################################################################
##==========##==========## Function for Smaller (Unfolded) Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
####################################################################################################################################################################





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
        if(not (Sim_Test and (((Multi_Dim_Option in ["3D", "5D"]) and (str(Method) in ["rdf"])) or (((Multi_Dim_Option in ["1D", "Off"]) and (str(Method) in ["tdf"])))))):
            Default_Histo_Name_Integrated = str(Default_Histo_Name_Integrated.replace("Smear",  "''"))# if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear"))
        
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
    if(((str(Method) not in ["rdf", "gdf", "tdf"]) or (Sim_Test and (str(Method) not in ["gdf", "tdf"]))) and ("Smear" in str(Default_Histo_Name_Integrated))):
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





##################################################################################################################################################################
##==========##==========## Function for Creating the Images for All z-pT Bins Together  ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################

def z_pT_Images_Together(Histogram_List_All, Default_Histo_Name, VARIABLE="(phi_t)", Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z", Cut_Option="Cut", Stats_Text_Output=False):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    All_z_pT_Canvas = Canvas_Create(Name=Default_Histo_Name.replace("1D", "".join(["".join(["CANVAS_", str(Plot_Orientation)]) if(Multi_Dim_Option in ["Off"]) else "".join(["CANVAS_", str(Plot_Orientation), "_", str(Multi_Dim_Option)]), "_UnCut" if(Cut_Option not in ["Cut", "Proton"]) else "_ProtonCut" if(Cut_Option not in ["Cut"]) else ""])), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
    # # Use above for normal size, use below for 2x size (made with PDFs)
    # All_z_pT_Canvas = Canvas_Create(Name=Default_Histo_Name.replace("1D", "".join(["".join(["CANVAS_", str(Plot_Orientation)]) if(Multi_Dim_Option in ["Off"]) else "".join(["CANVAS_", str(Plot_Orientation), "_", str(Multi_Dim_Option)]), "_UnCut" if(Cut_Option not in ["Cut", "Proton"]) else "_ProtonCut" if(Cut_Option not in ["Cut"]) else ""])), Num_Columns=2, Num_Rows=1, Size_X=3900*2, Size_Y=2175*2, cd_Space=0.01)
    All_z_pT_Canvas.SetFillColor(root_color.LGrey)
    # All_z_pT_Canvas.Draw()

    All_z_pT_Canvas_cd_1       = All_z_pT_Canvas.cd(1)
    All_z_pT_Canvas_cd_1.SetFillColor(root_color.LGrey)
    All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
    All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)

    All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
    All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
    All_z_pT_Canvas_cd_1_Upper.Divide(1, 2, 0, 0)

    All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
    All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
    All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
    All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)

    All_z_pT_Canvas_cd_2               = All_z_pT_Canvas.cd(2)
    All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
    All_z_pT_Canvas_cd_2.SetFillColor(root_color.LGrey)
    if("Y_bin" not in Binning_Method):
        number_of_rows, number_of_cols     = z_pT_Border_Lines(Q2_Y_Bin)[0][1]-1, z_pT_Border_Lines(Q2_Y_Bin)[1][1]-1
        if(Plot_Orientation in ["z_pT"]):
            number_of_rows, number_of_cols = z_pT_Border_Lines(Q2_Y_Bin)[1][1]-1, z_pT_Border_Lines(Q2_Y_Bin)[0][1]-1
            All_z_pT_Canvas_cd_2.Divide(number_of_rows, number_of_cols, 0.0001, 0.0001)
        else:
            All_z_pT_Canvas_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)
            for ii in range(1, number_of_cols + 1, 1):
                All_z_pT_Canvas_cd_2_cols = All_z_pT_Canvas_cd_2.cd(ii)
                All_z_pT_Canvas_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)
    else:
        if(Plot_Orientation in ["z_pT"]):
            number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
            All_z_pT_Canvas_cd_2.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
        else:
            number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
            All_z_pT_Canvas_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)
            for ii in range(1, number_of_cols + 1, 1):
                All_z_pT_Canvas_cd_2_cols = All_z_pT_Canvas_cd_2.cd(ii)
                All_z_pT_Canvas_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
    
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ####  Upper Left - i.e., 2D Histograms  ############################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    # Q2_y_Histo_rdf_Initial = Histogram_List_All[str(str(str(Default_Histo_Name.replace("(phi_t)", "(Q2)_(y)")).replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear")).replace("Data_Type", ("rdf" if(not Sim_Test) else "mdf") if(str(Method) not in ["mdf", "gdf", "tdf"]) else str(Method))).replace("(1D)", "(Normal_2D)")]
    # z_pT_Histo_rdf_Initial = Histogram_List_All[str(str(str(Default_Histo_Name.replace("(phi_t)", "(z)_(pT)")).replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear")).replace("Data_Type", ("rdf" if(not Sim_Test) else "mdf") if(str(Method) not in ["mdf", "gdf", "tdf"]) else str(Method))).replace("(1D)", "(Normal_2D)")]
    Q2_y_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name.replace(VARIABLE, "(Q2)_(y)")).replace("Smear", "''" if(((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) and (str(Method) not in ["mdf", "pdf", "bbb", "Unfold", "Background", "Relative_Background", "RC_Bayesian", "RC_Bin", "RC"])) else "Smear")).replace("Data_Type", "bbb" if(("Unfold" in str(Method)) or ("RC" in str(Method))) else "rdf" if(str(Method) not in ["mdf", "gdf", "tdf", "Background", "Relative_Background"]) else "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method))).replace("(1D)", "(Normal_2D)")
    z_pT_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name.replace(VARIABLE, "(z)_(pT)")).replace("Smear", "''" if(((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) and (str(Method) not in ["mdf", "pdf", "bbb", "Unfold", "Background", "Relative_Background", "RC_Bayesian", "RC_Bin", "RC"])) else "Smear")).replace("Data_Type", "bbb" if(("Unfold" in str(Method)) or ("RC" in str(Method))) else "rdf" if(str(Method) not in ["mdf", "gdf", "tdf", "Background", "Relative_Background"]) else "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method))).replace("(1D)", "(Normal_2D)")
    if((str(Method) not in ["gdf", "tdf"]) and (Cut_Option in ["UnCut"])):
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(no_cut)_(SMEAR"]))
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(no_cut)_(SMEAR"]))
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(no_cut)_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(no_cut)_(SMEAR")
    elif((str(Method) not in ["gdf", "tdf"]) and (Cut_Option in ["Proton"])):
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(Proton)_(SMEAR"]))
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(Proton)_(SMEAR"]))
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(bbb)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(bbb)_({Cut_Option})_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(bbb)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(bbb)_({Cut_Option})_(SMEAR")
    elif((str(Method) not in ["gdf", "tdf"]) and (Cut_Option not in ["Cut", ""])):
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), f")_({Cut_Option})_(SMEAR"]))
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", "mdf" if(str(Method) in ["Background", "Relative_Background"]) else str(Method), f")_({Cut_Option})_(SMEAR"]))
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(rdf)_({Cut_Option})_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(rdf)_({Cut_Option})_(SMEAR")
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                                                                                                                                                                                "(Normal_2D)_(rdf)_(Proton)_(SMEAR")
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(bbb)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(bbb)_({Cut_Option})_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(bbb)_(SMEAR",                                                                                                                                                                                f"(Normal_2D)_(bbb)_({Cut_Option})_(SMEAR")
    if("Background" in str(Method)):
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace("(Normal_2D)", f"(Normal_{Method}_2D)")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace("(Normal_2D)", f"(Normal_{Method}_2D)")

    if(str(Q2_y_Histo_rdf_Initial_Name.replace(f"Q2_y_Bin_{Q2_Y_Bin}", "Q2_y_Bin_All")) in Histogram_List_All):
        Q2_y_Histo_rdf_Initial_Name = Q2_y_Histo_rdf_Initial_Name.replace(f"Q2_y_Bin_{Q2_Y_Bin}", "Q2_y_Bin_All")
    # print(f"Q2_y_Histo_rdf_Initial_Name = {Q2_y_Histo_rdf_Initial_Name}")
    #Find Comment
    Q2_y_Histo_rdf_Initial = Histogram_List_All[Q2_y_Histo_rdf_Initial_Name]
    z_pT_Histo_rdf_Initial = Histogram_List_All[z_pT_Histo_rdf_Initial_Name]
    Drawing_Histo_Set = {}
    ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    if("3D" in str(type(Q2_y_Histo_rdf_Initial))):
        # bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(0), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Q2_y_Histo_rdf_Initial.GetNbinsX())
        bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(1), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Q2_y_Histo_rdf_Initial.GetNbinsX())
        Q2_y_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
        Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial.Project3D('yz e')
        Drawing_Histo_Set[Q2_y_Name].SetName(Q2_y_Name)
        Drawing_Histo_Title = (str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
        Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
        if("mdf" in str(Q2_y_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
        if("gdf" in str(Q2_y_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Generated")
        if("tdf" in str(Q2_y_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Generated",    "True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Gen",          "True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("GEN",          "True")
        if("Unfold" in str(Method)):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "Acceptance Corrected")
        Drawing_Histo_Set[Q2_y_Name].SetTitle(Drawing_Histo_Title)
    else:
        Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial
        print("Using Q2_y_Histo_rdf_Initial =", str(Q2_y_Histo_rdf_Initial))
        
    if("3D" in str(type(z_pT_Histo_rdf_Initial))):
        # Find Comment
        # bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(0), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(z_pT_Histo_rdf_Initial.GetNbinsX())
        bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(1), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(z_pT_Histo_rdf_Initial.GetNbinsX())
        z_pT_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
        z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial.Project3D('yz e'                        if(Plot_Orientation in ["z_pT"]) else 'zy e')
        Drawing_Histo_Set[z_pT_Name].SetName(z_pT_Name)
        Drawing_Histo_Title = (str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("yz projection" if(Plot_Orientation in ["z_pT"]) else "zy projection", "")).replace("".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
        Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
        if("mdf" in str(z_pT_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
        if("gdf" in str(z_pT_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Generated")
        if("tdf" in str(z_pT_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Generated",    "True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Gen",          "True")
            Drawing_Histo_Title = Drawing_Histo_Title.replace("GEN",          "True")
        if("Unfold" in str(Method)):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "Acceptance Corrected")
        Drawing_Histo_Set[z_pT_Name].SetTitle(Drawing_Histo_Title)
    else:
        z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial
        print("Using z_pT_Histo_rdf_Initial =", str(z_pT_Histo_rdf_Initial))
        
    if((str(Standard_Histogram_Title_Addition) not in [""]) and ((str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[z_pT_Name].GetTitle())) or ((str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[Q2_y_Name].GetTitle()))))):
        Drawing_Histo_Set[Q2_y_Name].SetTitle("".join(["#splitline{", str(Drawing_Histo_Set[Q2_y_Name].GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
        Drawing_Histo_Set[z_pT_Name].SetTitle("".join(["#splitline{", str(Drawing_Histo_Set[z_pT_Name].GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
    if(str(Method) in ["tdf"]):
        Drawing_Histo_Set[Q2_y_Name].SetTitle(str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("Experimental", "MC True"))
        Drawing_Histo_Set[Q2_y_Name].SetTitle(str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("Generated",    "True"))
        Drawing_Histo_Set[Q2_y_Name].SetTitle(str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("Gen",          "True"))
        Drawing_Histo_Set[Q2_y_Name].SetTitle(str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("GEN",          "True"))
        Drawing_Histo_Set[z_pT_Name].SetTitle(str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("Experimental", "MC True"))
        Drawing_Histo_Set[z_pT_Name].SetTitle(str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("Generated",    "True"))
        Drawing_Histo_Set[z_pT_Name].SetTitle(str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("Gen",          "True"))
        Drawing_Histo_Set[z_pT_Name].SetTitle(str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("GEN",          "True"))
    ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
        
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 1, 0.15)
    Drawing_Histo_Set[Q2_y_Name].Draw("colz")
    Drawing_Histo_Set[Q2_y_Name].SetStats(1)
    ROOT.gStyle.SetOptStat("i")
    stats = Drawing_Histo_Set[Q2_y_Name].GetListOfFunctions().FindObject("stats")
    if(stats):
        stats.SetX1NDC(0.80)  # New X start position
        stats.SetX2NDC(0.90)  # New X end position
        stats.SetY1NDC(0.85) # New Y start position
        stats.SetY2NDC(0.95) # New Y end position
    else:
        print(f"{color.Error}Error in (Q2-y) stat_box of Drawing_Histo_Set[{Q2_y_Name}]...{color.END}\n\tstats = {stats}")
    # statbox_move(Histogram=Drawing_Histo_Set[Q2_y_Name], Canvas=All_z_pT_Canvas_cd_1_Upper, Default_Stat_Obj="", Y1_add=0.85, Y2_add=0.95, X1_add=0.9, X2_add=0.8, Print_Method="norm")
    # configure_stat_box(hist=Drawing_Histo_Set[Q2_y_Name], show_entries=False, canvas=All_z_pT_Canvas_cd_1_Upper)
    # statbox_move(Histogram=Drawing_Histo_Set[Q2_y_Name],  Canvas=All_z_pT_Canvas_cd_1_Upper, Default_Stat_Obj="", Print_Method="off")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(1), histo=Drawing_Histo_Set[Q2_y_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    # Drawing_Histo_Set[Q2_y_Name].SetStats(0)
    Q2_y_borders = {}
    if("y_bin" in Binning_Method):
        # Q2_y_borders, Q2_y_borders_New = {}, {}
        line_num, line_num_New = 0, 0
        for b_lines in Q2_y_Border_Lines(-1):
            try:
                Q2_y_borders[(line_num)] = ROOT.TLine()
            except:
                print(color.RED, "Error in Q2_y_borders[(line_num)]", color.END)
            Q2_y_borders[(line_num)].SetLineColor(1)
            Q2_y_borders[(line_num)].SetLineWidth(2)
            Q2_y_borders[(line_num)].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
            line_num += 1
    else:
        for Q2_Y_Bin_ii in range(1, 18, 1):
            Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.Draw("same")
        if(Q2_Y_Bin in range(1,18)):
            for line_Bin in Q2_y_borders[Q2_Y_Bin]:
                line_Bin.SetLineColor(ROOT.kRed)
                line_Bin.SetLineWidth(6)
                line_Bin.Draw("same")
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 2, 0.15)
    Drawing_Histo_Set[z_pT_Name].Draw("colz")
    Drawing_Histo_Set[z_pT_Name].SetStats(1)
    ROOT.gStyle.SetOptStat("i")
    stats = Drawing_Histo_Set[z_pT_Name].GetListOfFunctions().FindObject("stats")
    if(stats):
        stats.SetX1NDC(0.80)  # New X start position
        stats.SetX2NDC(0.90)  # New X end position
        stats.SetY1NDC(0.85) # New Y start position
        stats.SetY2NDC(0.95) # New Y end position
    else:
        print(f"{color.Error}Error in (z-pT) stat_box of Drawing_Histo_Set[{z_pT_Name}]...{color.END}\n\tstats = {stats}")
    # statbox_move(Histogram=Drawing_Histo_Set[z_pT_Name], Canvas=All_z_pT_Canvas_cd_1_Upper, Default_Stat_Obj="", Y1_add=0.85, Y2_add=0.95, X1_add=0.9, X2_add=0.8, Print_Method="norm")
    # configure_stat_box(hist=Drawing_Histo_Set[z_pT_Name], show_entries=False, canvas=All_z_pT_Canvas_cd_1_Upper)
    # statbox_move(Histogram=Drawing_Histo_Set[z_pT_Name],  Canvas=All_z_pT_Canvas_cd_1_Upper, Default_Stat_Obj="", Print_Method="off")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(2), histo=Drawing_Histo_Set[z_pT_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    # ROOT.gStyle.SetOptStat(1111)
    if(Plot_Orientation in ["pT_z"]):
        if(str(Q2_Y_Bin) not in ["0", "All"]):
            if("y_bin" in Binning_Method):
                z_pT_borders = {}
                Max_z  = max(z_pT_Border_Lines(Q2_Y_Bin)[0][2])
                Min_z  = min(z_pT_Border_Lines(Q2_Y_Bin)[0][2])
                Max_pT = max(z_pT_Border_Lines(Q2_Y_Bin)[1][2])
                Min_pT = min(z_pT_Border_Lines(Q2_Y_Bin)[1][2])
                for zline in z_pT_Border_Lines(Q2_Y_Bin)[0][2]:
                    for pTline in z_pT_Border_Lines(Q2_Y_Bin)[1][2]:
                        z_pT_borders[zline] = ROOT.TLine()
                        z_pT_borders[zline].SetLineColor(1)
                        z_pT_borders[zline].SetLineWidth(4)
                        z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT)
                        z_pT_borders[pTline] = ROOT.TLine()
                        z_pT_borders[pTline].SetLineColor(1)
                        z_pT_borders[pTline].SetLineWidth(4)
                        z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline)
            else:
                Drawing_Histo_Set[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
                Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2, Plot_Orientation_Input=Plot_Orientation)
        if(any(binning in Binning_Method for binning in ["y", "Y"])):
            Drawing_Histo_Set[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
            MM_z_pT_borders = {}
            # Create a TLegend
            MM_z_pT_legend = ROOT.TLegend(0.8, 0.1, 0.95, 0.4)  # (x1, y1, x2, y2)
            MM_z_pT_legend.SetNColumns(1)
            # Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            for MM_lines in MM_z_pT_borders:
                MM_z_pT_borders[MM_lines].Draw("same")
            MM_z_pT_legend.Draw("same")
            
    else:
        if(str(Q2_Y_Bin) not in ["All", "0"]):
            if("y_bin" in Binning_Method):
                z_pT_borders = {}
                Max_z  = max(z_pT_Border_Lines(Q2_Y_Bin)[0][2])
                Min_z  = min(z_pT_Border_Lines(Q2_Y_Bin)[0][2])
                Max_pT = max(z_pT_Border_Lines(Q2_Y_Bin)[1][2])
                Min_pT = min(z_pT_Border_Lines(Q2_Y_Bin)[1][2])
                for zline in z_pT_Border_Lines(Q2_Y_Bin)[0][2]:
                    for pTline in z_pT_Border_Lines(Q2_Y_Bin)[1][2]:
                        z_pT_borders[zline] = ROOT.TLine()
                        z_pT_borders[zline].SetLineColor(1)
                        z_pT_borders[zline].SetLineWidth(2)
                        z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                        z_pT_borders[pTline] = ROOT.TLine()
                        z_pT_borders[pTline].SetLineColor(1)
                        z_pT_borders[pTline].SetLineWidth(2)
                        z_pT_borders[pTline].DrawLine(pTline, Min_z, pTline, Max_z)
            else:
                Drawing_Histo_Set[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
                Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2)
                
        if(any(binning in Binning_Method for binning in ["y", "Y"])):
            Drawing_Histo_Set[z_pT_Name].GetYaxis().SetRangeUser(0, 1.2)
            MM_z_pT_borders = {}
            # Create a TLegend
            MM_z_pT_legend = ROOT.TLegend(0.5, 0.1, 0.9, 0.2)  # (x1, y1, x2, y2)
            MM_z_pT_legend.SetNColumns(2)
            # Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            for MM_lines in MM_z_pT_borders:
                MM_z_pT_borders[MM_lines].Draw("same")
            MM_z_pT_legend.Draw("same")
            
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    ####  Upper Left - i.e., 2D Histograms  ############################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    Bin_Title_All_z_pT_Bins     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All"]), "}}}"])
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title_All_z_pT_Bins = "".join(["#splitline{", str(Bin_Title_All_z_pT_Bins), "}{", str(Standard_Histogram_Title_Addition), "}"])
    if("sec" in str(VARIABLE)):
        Variable_Title = "#phi_{h}"
        for particle_sec in ["esec_smeared", "pipsec_smeared", "esec", "pipsec"]:
            for sec in [1, 2, 3, 4, 5, 6]:
                if(f"{particle_sec}_{sec}" in VARIABLE):
                    Bin_Title_All_z_pT_Bins = Bin_Title_All_z_pT_Bins.replace("".join(["{", str(Standard_Histogram_Title_Addition), "}"]), "".join(["{", "#pi^{+} Pion" if(particle_sec in ["pipsec"]) else "Electron", " Sector ", str(sec), " #topbar ", str(Standard_Histogram_Title_Addition), "}"]))
                    Particle_Sector = f"{particle_sec}_{sec}"
                    break
    else:
        Particle_Sector = "N/A"
        if("MM" in str(VARIABLE.replace("(", "")).replace(")", "")):
            Variable_Title = "Missing Mass"
        else:
            Variable_Title = "".join(["P_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(el)", "(pip)"]) else "".join(["#theta_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(elth)", "(pipth)"]) else "".join(["#phi_{", str(VARIABLE.replace("(", "")).replace(")", ""), "}"]) if(VARIABLE in ["(elPhi)", "(pipPhi)"]) else "#phi_{h}"
            if("#phi_{h}" not in Variable_Title):
                for var_error_title in ["{elth}", "{elPhi}", "{pipth}", "{pipPhi}"]:
                    Variable_Title = Variable_Title.replace(var_error_title, "{El}" if("el" in var_error_title) else "{#pi^{+}}")
        
    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower, 1, 0.15)
    # if(str(Multi_Dim_Option) not in ["Off", "5D"]):
    #     Default_Response_Matrix_Name =   str(str(str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")).replace("Multi-Dim Histo", "Response_Matrix")).replace("MultiDim_5D_Histo", "Response_Matrix")
    #     # Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")
    #     if((("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Response_Matrix_Name) or ("(MultiDim_Q2_y_z_pT_phi_h)" in Default_Response_Matrix_Name)) and (str(Q2_Y_Bin) not in ["All", "0"])):
    #         Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(Q2_y_Bin_", str(Q2_Y_Bin), ")"]), "(Q2_y_Bin_All)")
    #     if("y" in Binning_Method):
    #         Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
    #     else:
    #         Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
    #     # print("\n\n\n\n\n\n\nDefault_Response_Matrix_Name =", Default_Response_Matrix_Name, "\n\n\n\n\n\n\n\n")
    #     Histogram_List_All[Default_Response_Matrix_Name].SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
    #     Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
    #     Histogram_List_All[Default_Response_Matrix_Name].GetYaxis().SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetYaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
    #     Histogram_List_All[Default_Response_Matrix_Name].Draw("col")
    # elif("Response" in str(Method)):
    if("Response" in str(Method)):
        try:
            for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].SetTitle(str(Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].GetTitle()).replace(range_strings, ""))
            Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "mdf")).replace("1D", "Response_Matrix")].Draw("col")
        except Exception as e:
            print("".join([color.Error, "ERROR IN Response Matrix:\n", color.END_R, str(traceback.format_exc()), color.END]))
    elif("Data"   in str(Method)):
        try:
            if(Multi_Dim_Option in ["Off"]):
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                # MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                # MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")].DrawNormalized("H P E0 same")
                # ExREAL_1D_Norm     = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf") ].DrawNormalized("H P E0 same")
                ExREAL_1D_Norm     = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type",                                     "rdf") ].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm     = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",                                                                 "mdf"))].DrawNormalized("H P E0 same")
                if(any(Accepted_Vars in str(VARIABLE) for Accepted_Vars in ["phi_t", "MM"])):
                    MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type",                                     "gdf") ].DrawNormalized("H P E0 same")
            elif(Multi_Dim_Option in ["5D"]):
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(MultiDim_5D_Histo)")).replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf") ].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type",                                                           "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type",                               "gdf") ].DrawNormalized("H P E0 same")                
            elif(Multi_Dim_Option in ["3D"]):
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(MultiDim_3D_Histo)")).replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf") ].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type",                                                           "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type",                               "gdf") ].DrawNormalized("H P E0 same")                
            else:
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
                # Currently built so that the integrated z-pT bin for multidimensional unfolding uses the combined Q2-y-phi variable (whereas the unfolding done for the individual z-pT bins will unfold the z-pT-phi variable instead)
                    # This note is to explain that the Multi-Dim version of this image will show 2 different types of multidimensional unfolding
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                # MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                # MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")].DrawNormalized("H P E0 same")
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf") ].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type",                                                           "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type",                               "gdf") ].DrawNormalized("H P E0 same")
            
            # ExREAL_1D_Norm.SetTitle(str(ExREAL_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            # MC_REC_1D_Norm.SetTitle(str(MC_REC_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            # MC_GEN_1D_Norm.SetTitle(str(MC_GEN_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            
            # if(("phi_t" in str(VARIABLE)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(VARIABLE))):
            Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
            #     # print(f"{color.BLUE}Max_Pre_Unfolded = {Max_Pre_Unfolded}{color.END}")
            # else:
            #     # print(f"{color.BOLD}ExREAL_1D_Norm = {type(ExREAL_1D_Norm)}\nMC_REC_1D_Norm = {type(MC_REC_1D_Norm)}{color.END}")
            #     Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), 0])
            #     # print(f"{color.RED}Max_Pre_Unfolded = {Max_Pre_Unfolded}{color.END}")
            
            ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
            MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
            MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)

            if("Missing" not in Variable_Title):
                ExREAL_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                MC_REC_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                MC_GEN_1D_Norm.GetXaxis().SetRangeUser(0, 360)
            else:
                ExREAL_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                MC_REC_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                MC_GEN_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                
            Norm_Data_Title = "".join(["#splitline{#scale[1.5]{Pre-", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolding (Old)" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"])

            ExREAL_1D_Norm.SetTitle(Norm_Data_Title)
            ExREAL_1D_Norm.GetYaxis().SetTitle("Normalized")
            ExREAL_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            ExREAL_1D_Norm.SetLineColor(root_color.Blue)
            ExREAL_1D_Norm.SetLineWidth(2)
            ExREAL_1D_Norm.SetLineStyle(1)
            ExREAL_1D_Norm.SetMarkerColor(root_color.Blue)
            ExREAL_1D_Norm.SetMarkerSize(1)
            ExREAL_1D_Norm.SetMarkerStyle(21)
            #####==========#####      MC REC Histogram       #####==========##### ################################################################
            MC_REC_1D_Norm.SetTitle(Norm_Data_Title)
            MC_REC_1D_Norm.GetYaxis().SetTitle("Normalized")
            MC_REC_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            MC_REC_1D_Norm.SetLineColor(root_color.Red)
            MC_REC_1D_Norm.SetLineWidth(2)
            MC_REC_1D_Norm.SetLineStyle(1)
            MC_REC_1D_Norm.SetMarkerColor(root_color.Red)
            MC_REC_1D_Norm.SetMarkerSize(1)
            MC_REC_1D_Norm.SetMarkerStyle(22)
            #####==========#####      MC GEN Histogram       #####==========##### ################################################################
            # if(("phi_t" in str(VARIABLE)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(VARIABLE))):
            MC_GEN_1D_Norm.SetTitle(Norm_Data_Title)
            MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")
            MC_GEN_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            MC_GEN_1D_Norm.SetLineColor(root_color.Green)
            MC_GEN_1D_Norm.SetLineWidth(3)
            MC_GEN_1D_Norm.SetLineStyle(1)
            MC_GEN_1D_Norm.SetMarkerColor(root_color.Green)
            MC_GEN_1D_Norm.SetMarkerSize(1)
            MC_GEN_1D_Norm.SetMarkerStyle(20)

            ExREAL_1D_Norm.SetStats(0)
            MC_REC_1D_Norm.SetStats(0)
            MC_GEN_1D_Norm.SetStats(0)
            
            # if(Fit_Test):
            #     try:
            #         statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
            #     except:
            #         print("\nMC_GEN_1D IS NOT FITTED\n")
            
        except Exception as e:
            print("".join([color.Error, "ERROR IN 1D (Input) Histograms:\n",        color.END_R, str(traceback.format_exc()), color.END]))
            
    elif("Kinematic_Comparison" in str(Method)):
        try:
            ExREAL_1D_Norm_All = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")]
            MC_REC_1D_Norm_All = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf"))]

            if(ExREAL_1D_Norm_All.Integral() != 0):
                scale_factor_ExREAL = 1.0 / ExREAL_1D_Norm_All.Integral()
            else:
                scale_factor_ExREAL = 1.0
            ExREAL_1D_Norm_All.Scale(scale_factor_ExREAL)
            if(MC_REC_1D_Norm_All.Integral() != 0):
                scale_factor_MC_REC = 1.0 / MC_REC_1D_Norm_All.Integral()
            else:
                scale_factor_MC_REC = 1.0
            MC_REC_1D_Norm_All.Scale(scale_factor_MC_REC)

            for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                ExREAL_1D_Norm_All.SetTitle(str(ExREAL_1D_Norm_All.GetTitle()).replace(range_strings, "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolding (Old)" if(Multi_Dim_Option in ["Only"]) else ""))
                MC_REC_1D_Norm_All.SetTitle(str(MC_REC_1D_Norm_All.GetTitle()).replace(range_strings, "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "3D Unfolding (Old)" if(Multi_Dim_Option in ["Only"]) else ""))
            
            Kinematic_Comparison_1D_All = ExREAL_1D_Norm_All.Clone(str(Default_Histo_Name.replace("Data_Type", "Kinematic_Comparison_1D")))
            Kinematic_Comparison_1D_All.Divide(MC_REC_1D_Norm_All)

            Kinematic_Comparison_1D_All.SetTitle("".join(["#splitline{#scale[1.5]{", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D " if(str(Multi_Dim_Option) not in ["Off"]) else "", "Comparison of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))

            Kinematic_Comparison_1D_All.GetYaxis().SetRangeUser(0, 1.2*Kinematic_Comparison_1D_All.GetMaximumBin())
            if("Missing" not in Variable_Title):
                Kinematic_Comparison_1D_All.GetXaxis().SetRangeUser(0, 360)
            else:
                Kinematic_Comparison_1D_All.GetXaxis().SetRangeUser(1, 3.5)

            Kinematic_Comparison_1D_All.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            Kinematic_Comparison_1D_All.SetLineColor(root_color.Black)
            Kinematic_Comparison_1D_All.SetLineWidth(2)
            Kinematic_Comparison_1D_All.SetLineStyle(1)
            Kinematic_Comparison_1D_All.SetMarkerColor(root_color.Black)
            Kinematic_Comparison_1D_All.SetMarkerSize(1)
            Kinematic_Comparison_1D_All.SetMarkerStyle(21)

            # Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "Kinematic_Comparison_1D_All"))] = Kinematic_Comparison_1D_All
            # Kinematic_Comparison_1D_All.Draw("H P E0 same")
            # Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "Kinematic_Comparison_1D_All"))].Draw("H P E0 same")

        except Exception as e:
            print(f"{color.Error}ERROR IN (z-pT Bin All) 1D (Input) Histograms:{color.END_B}\n{traceback.format_exc()}\n{color.END}Exception = {e}")
    elif("Unfold" in str(Method)):
        try:
            Max_Unfolded, Min_Unfolded = 1, 0
            if(Multi_Dim_Option in ["Off"]):
                BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "Bayesian")]
                BAY_Histo_Unfold.Draw("H P E0 same")
                BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "Bin")]
                BIN_Histo_Unfold.Draw("H P E0 same")
                # SVD_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "SVD")]
                # SVD_Histo_Unfold.Draw("H P E0 same")
                MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                # MC_GEN_1D_Unfold.Draw("H P E0 same")
                if(tdf not in ["N/A"]):
                    # ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                    ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "tdf"))]
                    ExTRUE_1D_Unfold.Draw("H P E0 same")
                    # Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                    # Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                else:
                    # Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                    # Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
            else:
                if(Multi_Dim_Option   in ["5D"]):
                    Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(MultiDim_5D_Histo)")).replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
                elif(Multi_Dim_Option in ["3D"]):
                    Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(MultiDim_3D_Histo)")).replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
                else:
                    Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)",   "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
                BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim).replace("Data_Type", "Bayesian")]
                BAY_Histo_Unfold.Draw("H P E0 same")
                BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim).replace("Data_Type", "Bin")]
                BIN_Histo_Unfold.Draw("H P E0 same")
                MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                # MC_GEN_1D_Unfold.Draw("H P E0 same")
                if(tdf not in ["N/A"]):
                    ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                    ExTRUE_1D_Unfold.Draw("H P E0 same")
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                else:
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
            
            BAY_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
            BIN_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
            MC_GEN_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
            if("Missing" not in Variable_Title):
                BAY_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                BIN_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(0,            360)
            else:
                BAY_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                BIN_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(0,            360)
            if(tdf not in ["N/A"]):
                ExTRUE_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                if("Missing" not in Variable_Title):
                    ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(0,        360)
                else:
                    ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(1,        3.5)
                #####==========#####    MC TRUE Histogram    #####==========##### ################################################################
                ExTRUE_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
                ExTRUE_1D_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                ExTRUE_1D_Unfold.SetLineColor(root_color.Cyan)
                ExTRUE_1D_Unfold.SetLineWidth(3)
                ExTRUE_1D_Unfold.SetLineStyle(1)
                ExTRUE_1D_Unfold.SetMarkerColor(root_color.Cyan)
                ExTRUE_1D_Unfold.SetMarkerSize(1)
                ExTRUE_1D_Unfold.SetMarkerStyle(20)
            # if(Multi_Dim_Option in ["Off"]):
            #     SVD_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
            #     SVD_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
            #     #####==========#####      SVD Histogram      #####==========##### ################################################################
            #     SVD_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            #     SVD_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            #     SVD_Histo_Unfold.SetLineColor(root_color.Pink)
            #     SVD_Histo_Unfold.SetLineWidth(2)
            #     SVD_Histo_Unfold.SetLineStyle(1)
            #     SVD_Histo_Unfold.SetMarkerColor(root_color.Pink)
            #     SVD_Histo_Unfold.SetMarkerSize(1)
            #     SVD_Histo_Unfold.SetMarkerStyle(20)
            
            #####==========#####     BAYESIAN Histogram      #####==========##### ################################################################
            BAY_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding",     " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            BAY_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            BAY_Histo_Unfold.SetLineColor(root_color.Teal)
            BAY_Histo_Unfold.SetLineWidth(2)
            BAY_Histo_Unfold.SetLineStyle(1)
            BAY_Histo_Unfold.SetMarkerColor(root_color.Teal)
            BAY_Histo_Unfold.SetMarkerSize(1)
            BAY_Histo_Unfold.SetMarkerStyle(21)
            #####==========#####    Bin-by-Bin Histogram     #####==========##### ################################################################
            BIN_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding",     " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            BIN_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            BIN_Histo_Unfold.SetLineColor(root_color.Brown)
            BIN_Histo_Unfold.SetLineWidth(2)
            BIN_Histo_Unfold.SetLineStyle(1)
            BIN_Histo_Unfold.SetMarkerColor(root_color.Brown)
            BIN_Histo_Unfold.SetMarkerSize(1)
            BIN_Histo_Unfold.SetMarkerStyle(22)
            #####==========#####      MC GEN Histogram       #####==========##### ################################################################
            MC_GEN_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding",     " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            MC_GEN_1D_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            MC_GEN_1D_Unfold.SetLineColor(root_color.Green)
            MC_GEN_1D_Unfold.SetLineWidth(3)
            MC_GEN_1D_Unfold.SetLineStyle(1)
            MC_GEN_1D_Unfold.SetMarkerColor(root_color.Green)
            MC_GEN_1D_Unfold.SetMarkerSize(1)
            MC_GEN_1D_Unfold.SetMarkerStyle(20)
            
            if(Fit_Test):
                try:
                    statbox_move(Histogram=BAY_Histo_Unfold,     Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                except:
                    print("\nBAY_Histo_Unfold IS NOT FITTED\n")
                try:
                    statbox_move(Histogram=BIN_Histo_Unfold,     Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                except:
                    print("\nBIN_Histo_Unfold IS NOT FITTED\n")
                try:
                    statbox_move(Histogram=MC_GEN_1D_Unfold,     Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                except:
                    print("\nMC_GEN_1D_Unfold IS NOT FITTED\n")
                if(tdf not in ["N/A"]):
                    try:
                        statbox_move(Histogram=ExTRUE_1D_Unfold, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                    except:
                        print("\nExTRUE_1D_Unfold IS NOT FITTED\n")
                # if(Multi_Dim_Option in ["Off"]):
                #     try:
                #         statbox_move(Histogram=SVD_Histo_Unfold, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                #     except:
                #         print("\nSVD_Histo_Unfold IS NOT FITTED\n")
            
        except Exception as e:
            print("".join([color.Error, "ERROR IN 1D (Input) Histograms:\n", color.END_B, str(traceback.format_exc()), color.END]))

    elif("Background" in str(Method)):
        Default_Histo_Name_Any     = str(Default_Histo_Name)
        if(Multi_Dim_Option   not in ["Off"]):
            if(Multi_Dim_Option   in ["5D"]):
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(MultiDim_5D_Histo)")).replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
            elif(Multi_Dim_Option in ["3D"]):
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(MultiDim_3D_Histo)")).replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
            else:
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)",   "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if(str(Method) in ["rdf", "gdf", "tdf"]):
            Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("Smear", "''"))
        ##################################################################### ################################################################
        #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
        ##################################################################### ################################################################
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(root_color.Black)
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(root_color.Black)
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1)
        Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(22)
        ##################################################################### ################################################################
        #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
        ##################################################################### ################################################################
        
        try:
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H P E0 same")
            
            configure_stat_box(hist=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))], show_entries=True, canvas=All_z_pT_Canvas_cd_1_Lower.cd(1))
            statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type",  Method))], Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
            
            if("Missing" not in Variable_Title):
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
            else:
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(1, 3.5)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())))

        except Exception as e:
            print("".join([color.Error, "ERROR IN METHOD = '", str(Method), "':\n", color.END_R, str(traceback.format_exc()), color.END]))

    elif("RC" not in str(Method)):
        Default_Histo_Name_Any     = str(Default_Histo_Name).replace("z_pT_Bin_All", "z_pT_Bin_Integrated" if((str(Method) not in ["Acceptance", "Acceptance_ratio"]) and ("pipsec" not in str(Default_Histo_Name))) else "z_pT_Bin_All")
        if(Multi_Dim_Option   not in ["Off"]):
            if(Multi_Dim_Option   in ["5D"]):
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(MultiDim_5D_Histo)")).replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
            elif(Multi_Dim_Option in ["3D"]):
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(MultiDim_3D_Histo)")).replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
            else:
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)",   "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("Multi_Dim_Q2_Y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t"))
                Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t"))
        if(str(Method) in ["rdf", "gdf", "tdf"]):
            Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("Smear", "''"))
        ##################################################################### ################################################################
        #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
        ##################################################################### ################################################################
        #####==========#####   Experimental Histogram    #####==========##### ################################################################
        if(str(Method) in ["rdf"]):
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineColor(root_color.Blue)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineWidth(2)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineStyle(1)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerColor(root_color.Blue)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerSize(1)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerStyle(21)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineColor(root_color.Blue)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerColor(root_color.Blue)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''" if(not Sim_Test) else "Smear")].SetMarkerStyle(21)
        #####==========#####      MC REC Histogram       #####==========##### ################################################################
        if(str(Method) in ["mdf"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(root_color.Red)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(root_color.Red)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(22)
        #####==========#####      MC GEN Histogram       #####==========##### ################################################################
        if(str(Method) in ["gdf"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineColor(root_color.Green)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineWidth(3)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerColor(root_color.Green)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerStyle(20)
        #####==========#####      MC True Histogram      #####==========##### ################################################################
        if(str(Method) in ["tdf"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineColor(root_color.Cyan)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineWidth(3)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerColor(root_color.Cyan)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerStyle(20)
        #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################
        if(str(Method) in ["Bin", "bbb", "bin", "Bin-by-Bin", "Bin-By-Bin", "Bin-by-bin", "bin-by-bin"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(root_color.Brown)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(root_color.Brown)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1.5)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(21)
        #####==========#####   Unfold Bayes Histogram    #####==========##### ################################################################
        if(str(Method) in ["Bayesian", "Bayes"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(root_color.Teal)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(root_color.Teal)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(21)
        #####==========#####   RC Unfold Bin Histogram     #####==========##### ################################################################
        if(str(Method) in ["RC_Bin"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(ROOT.kOrange + 4)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(ROOT.kOrange + 4)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1.5)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(21)
        #####==========#####  RC Unfold Bayes Histogram    #####==========##### ################################################################
        if(str(Method) in ["RC_Bayesian"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(ROOT.kViolet - 8)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(ROOT.kViolet - 8)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(21)
        #####==========#####    Unfold SVD Histogram     #####==========##### ################################################################
        if(str(Method) in ["SVD"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(root_color.Pink)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(root_color.Pink)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerStyle(21)
        ##################################################################### ################################################################
        #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
        ##################################################################### ################################################################
        
        try:
            Histo_Bin_Max = Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())
            Run_Acceptance_EvGen = False
            if(Method in ["Acceptance", "Acceptance_ratio", "Relative_Background"]):
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetStats(0)
                if(Use_TTree and (Method not in ["Acceptance_ratio", "Relative_Background"])):
                    Acceptance_EvGen_Name = f'{str(Default_Histo_Name_Any.replace("Data_Type", Method))}_EvGen'
                    Acceptance_EvGen_Name = Acceptance_EvGen_Name.replace("Smear", "''")
                    Run_Acceptance_EvGen  = Acceptance_EvGen_Name in Histogram_List_All
                    if(Run_Acceptance_EvGen):
                        print(f"\n{color.BBLUE}Comparing clasdis and EvGen Acceptance{color.END}\n")
                        Histogram_List_All[Acceptance_EvGen_Name].SetStats(0)
                        Histogram_List_All[Acceptance_EvGen_Name].SetLineColor(ROOT.kYellow + 3)
                        Histogram_List_All[Acceptance_EvGen_Name].SetLineStyle(7)
                        Histogram_List_All[Acceptance_EvGen_Name].SetLineWidth(3)
                        Histo_Bin_Max = max([Histo_Bin_Max, Histogram_List_All[Acceptance_EvGen_Name].GetBinContent(Histogram_List_All[Acceptance_EvGen_Name].GetMaximumBin())])
                    else:
                        print(f"\n{color.Error}Can't compare clasdis and EvGen Acceptance because {color.END_B}{color.UNDERLINE}{Acceptance_EvGen_Name}{color.END_B}{color.RED} is not in 'Histogram_List_All'{color.END}\n")
            
            for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetTitle()).replace(range_strings, ""))
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H P E0 same")
                
            show_entries_condition = Method not in ["Acceptance"]
            configure_stat_box(hist=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))], show_entries=show_entries_condition, canvas=All_z_pT_Canvas_cd_1_Lower.cd(1))

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))

            if("Missing" not in Variable_Title):
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
            else:
                Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(1, 3.5)

            
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*Histo_Bin_Max)
            # if(Method not in ["Acceptance"]):
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())))
            # else:
            #     Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 0.2)

            if(Run_Acceptance_EvGen):
                Histogram_List_All[Acceptance_EvGen_Name].Draw("H P E0 same")
            if(Method in ["Acceptance"]):
                Acceptance_Cut_Line.Draw()
                All_z_pT_Canvas_cd_1_Lower.Modified()
                All_z_pT_Canvas_cd_1_Lower.Update()
                
            if(Fit_Test):
                try:
                    statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))], Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                except:
                    print("\nTHE SELECTED HISTOGRAM WAS NOT FITTED\n")

        except Exception as e:
            print(f"{color.Error}ERROR IN METHOD = '{Method}':\n{color.END_R}{str(traceback.format_exc())}{color.END}")

    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ####  Filling Canvas (Left) End ################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - i.e., Individual z-pT Bins  #####################################################################################################################################################################################################################################################################################################################################################
    if("Y_bin" not in Binning_Method):
        z_pT_Bin_Range = 42 if(str(Q2_Y_Bin) in ["2"]) else 36 if(str(Q2_Y_Bin) in ["4", "5", "9", "10"]) else 35 if(str(Q2_Y_Bin) in ["1", "3"]) else 30 if(str(Q2_Y_Bin) in ["6", "7", "8", "11"]) else 25 if(str(Q2_Y_Bin) in ["13", "14"]) else 20 if(str(Q2_Y_Bin) in ["12", "15", "16", "17"]) else 1
    else:
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
        # # i.e.,      = [Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2][1] - 1 where (Migration_Bin_1 - 1) is the last non-migration bin (without removing from the main grid)
    for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
        
        # if("Y_bin" not in Binning_Method):
        #     if(((Q2_Y_Bin in [1]) and (z_pT_Bin in [28, 34, 35])) or ((Q2_Y_Bin in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or (Q2_Y_Bin in [3] and z_pT_Bin in [28, 35]) or (Q2_Y_Bin in [4] and z_pT_Bin in [6, 36]) or (Q2_Y_Bin in [5] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [6] and z_pT_Bin in [30]) or (Q2_Y_Bin in [7] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [9] and z_pT_Bin in [36]) or (Q2_Y_Bin in [10] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [11] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [13, 14] and z_pT_Bin in [25]) or (Q2_Y_Bin in [15, 16, 17] and z_pT_Bin in [20])):
        #         continue
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
            continue
        
        Bin_Title_z_pT_Bin              = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(str(z_pT_Bin) not in ["0", "-1", "-2"]) else "All" if(str(z_pT_Bin) in ["0"]) else f"Integrated{'' if(str(z_pT_Bin) in ['-1']) else ' (Over Common Range)'}"]), "}}}"])
        Default_Histo_Name_z_pT_Bin     = str(Default_Histo_Name.replace("z_pT_Bin_All",     "".join(["z_pT_Bin_", str(z_pT_Bin)])))
        if((Multi_Dim_Option   not in ["Off"]) and ("Response" not in str(Method))):
            if(Multi_Dim_Option    in ["5D"]):
                Default_Histo_Name_z_pT_Bin     = str(Default_Histo_Name_z_pT_Bin.replace(VARIABLE,       "(MultiDim_Q2_y_z_pT_phi_h)")).replace("(1D)", "(MultiDim_5D_Histo)")
            elif(Multi_Dim_Option  in ["3D"]):
                Default_Histo_Name_z_pT_Bin     = str(Default_Histo_Name_z_pT_Bin.replace(VARIABLE,  "(MultiDim_z_pT_Bin_Y_bin_phi_t)")).replace("(1D)", "(MultiDim_3D_Histo)")
            else:
                if("y" in Binning_Method):
                    Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace(VARIABLE, "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
                else:
                    Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace(VARIABLE, "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
        if(str(Method) in ["rdf", "gdf", "tdf"]):
            Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear"))
        
        
        cd_number_of_z_pT_all_together = z_pT_Bin
        # if("Y_bin" in Binning_Method):
        #     cd_number_of_z_pT_all_together = FindCanvas_cd_Kinematic_Bins(Bin_Name="", Q2_y_Bin_Input=Q2_Y_Bin, z_pT_Bin_Input=z_pT_Bin)
        # else:
        #     cd_number_of_z_pT_all_together = z_pT_Bin
        
            
        if(Plot_Orientation in ["z_pT"]):
            All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(cd_number_of_z_pT_all_together)
            All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
        else:
            cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
            if(0 == (cd_number_of_z_pT_all_together%number_of_cols)):
                cd_row += -1
            cd_col = cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
            
            All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
            All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)

            All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)

        Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)

        if("Data"       in str(Method)):
            try:
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                # MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                # MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")].DrawNormalized("H P E0 same")
                if(("(1D)" in str(Default_Histo_Name_z_pT_Bin)) or (not Sim_Test)):
                    ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",      "''")).replace("Data_Type", "rdf")].DrawNormalized("H P E0 same")
                else:
                    ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf"))].DrawNormalized("H P E0 same")
                    
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf"))].DrawNormalized("H P E0 same")
                
                # ExREAL_1D_Norm.SetTitle(str(ExREAL_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                # MC_REC_1D_Norm.SetTitle(str(MC_REC_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                
                # if(("phi_t" in str(VARIABLE)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(VARIABLE))):
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H P E0 same")
                # MC_GEN_1D_Norm.SetTitle(str(MC_GEN_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
                # else:
                    # Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin())])
                
                ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
                MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
                MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)

                if("Missing" not in Variable_Title):
                    ExREAL_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                    MC_REC_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                    MC_GEN_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                else:
                    ExREAL_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                    MC_REC_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                    MC_GEN_1D_Norm.GetXaxis().SetRangeUser(1, 3.5)
                    
                Norm_Data_Title = "".join(["#splitline{#scale[1.5]{Pre-",  "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"])
                
                ExREAL_1D_Norm.SetTitle(Norm_Data_Title)
                ExREAL_1D_Norm.GetYaxis().SetTitle("Normalized")
                ExREAL_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                ExREAL_1D_Norm.SetLineColor(root_color.Blue)
                ExREAL_1D_Norm.SetLineWidth(2)
                ExREAL_1D_Norm.SetLineStyle(1)
                ExREAL_1D_Norm.SetMarkerColor(root_color.Blue)
                ExREAL_1D_Norm.SetMarkerSize(1)
                ExREAL_1D_Norm.SetMarkerStyle(21)
                #####==========#####      MC REC Histogram       #####==========##### ################################################################
                MC_REC_1D_Norm.SetTitle(Norm_Data_Title)
                MC_REC_1D_Norm.GetYaxis().SetTitle("Normalized")
                MC_REC_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                MC_REC_1D_Norm.SetLineColor(root_color.Red)
                MC_REC_1D_Norm.SetLineWidth(2)
                MC_REC_1D_Norm.SetLineStyle(1)
                MC_REC_1D_Norm.SetMarkerColor(root_color.Red)
                MC_REC_1D_Norm.SetMarkerSize(1)
                MC_REC_1D_Norm.SetMarkerStyle(22)
                #####==========#####      MC GEN Histogram       #####==========##### ################################################################
                # if(("phi_t" in str(VARIABLE)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(VARIABLE))):
                MC_GEN_1D_Norm.SetTitle(Norm_Data_Title)
                MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")
                MC_GEN_1D_Norm.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                MC_GEN_1D_Norm.SetLineColor(root_color.Green)
                MC_GEN_1D_Norm.SetLineWidth(3)
                MC_GEN_1D_Norm.SetLineStyle(1)
                MC_GEN_1D_Norm.SetMarkerColor(root_color.Green)
                MC_GEN_1D_Norm.SetMarkerSize(1)
                MC_GEN_1D_Norm.SetMarkerStyle(20)
                MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")
                    # if(Fit_Test):
                    #     try:
                    #         statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    #     except:
                    #         print(color.RED, "\nMC_GEN_1D IS NOT FITTED\n", color.END)
            
                ExREAL_1D_Norm.SetStats(0)
                MC_REC_1D_Norm.SetStats(0)
                MC_GEN_1D_Norm.SetStats(0)
                
            except Exception as e:
                print("".join([color.Error, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") 1D (Input) Histograms:\n", color.END_B, str(traceback.format_exc()), color.END]))
                
        elif("Kinematic_Comparison" in str(Method)):
            try:
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")]
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf"))]
                
                if(ExREAL_1D_Norm.Integral() != 0):
                    scale_factor_ExREAL = 1.0 / ExREAL_1D_Norm.Integral()
                else:
                    scale_factor_ExREAL = 1.0
                if(MC_REC_1D_Norm.Integral() != 0):
                    scale_factor_MC_REC = 1.0 / MC_REC_1D_Norm.Integral()
                else:
                    scale_factor_MC_REC = 1.0

                for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                    ExREAL_1D_Norm.SetTitle(str(ExREAL_1D_Norm.GetTitle()).replace(range_strings, "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                    MC_REC_1D_Norm.SetTitle(str(MC_REC_1D_Norm.GetTitle()).replace(range_strings, "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"]) else "3D Unfolding" if(Multi_Dim_Option in ["3D"]) else "(Old) 3D Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                
                Kinematic_Comparison_1D = ExREAL_1D_Norm.Clone(str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "Kinematic_Comparison_1D")))
                Kinematic_Comparison_1D.Divide(MC_REC_1D_Norm)
                
                Kinematic_Comparison_1D.SetTitle("".join(["#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", "Kinematic Comparison of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                
                Kinematic_Comparison_1D.GetYaxis().SetRangeUser(0, 1.2*Kinematic_Comparison_1D.GetMaximumBin())
                if("phi_t" in str(VARIABLE)):
                    Kinematic_Comparison_1D.GetXaxis().SetRangeUser(0, 360)
                else:
                    Kinematic_Comparison_1D.GetXaxis().SetRangeUser(1, 3.5)
                
                Kinematic_Comparison_1D.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                Kinematic_Comparison_1D.SetLineColor(root_color.Black)
                Kinematic_Comparison_1D.SetLineWidth(2)
                Kinematic_Comparison_1D.SetLineStyle(1)
                Kinematic_Comparison_1D.SetMarkerColor(root_color.Black)
                Kinematic_Comparison_1D.SetMarkerSize(1)
                Kinematic_Comparison_1D.SetMarkerStyle(21)
                
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "Kinematic_Comparison_1D"))] = Kinematic_Comparison_1D
                # Kinematic_Comparison_1D.Draw("H P E0 same")
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "Kinematic_Comparison_1D"))].Draw("H P E0 same")
                
            except Exception as e:
                print("".join([color.Error, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") 1D (Input) Histograms:\n", color.END_B, str(traceback.format_exc()), color.END]))
                
        elif("Unfold" in str(Method)):
            try:
                Max_Unfolded, Min_Unfolded = 1, 0
                if(Multi_Dim_Option in ["Off"]):
                    BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "Bayesian")]
                    BAY_Histo_Unfold.Draw("H P E0 same")
                    BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "Bin")]
                    BIN_Histo_Unfold.Draw("H P E0 same")
                    # SVD_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "SVD")]
                    # SVD_Histo_Unfold.Draw("H P E0 same")
                    MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                    # MC_GEN_1D_Unfold.Draw("H P E0 same")
                    if(tdf not in ["N/A"]):
                        # ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                        ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "tdf")]
                        ExTRUE_1D_Unfold.Draw("H P E0 same")
                        # Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                        # Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                    else:
                        # Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                        # Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
                else:
                    if(str(Multi_Dim_Option)   in ["5D"]):
                        Default_Histo_Name_Multi_Dim = str(Default_Histo_Name_z_pT_Bin.replace("(1D)", "(MultiDim_5D_Histo)")).replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
                    elif(str(Multi_Dim_Option) in ["3D"]):
                        Default_Histo_Name_Multi_Dim = str(Default_Histo_Name_z_pT_Bin.replace("(1D)", "(MultiDim_3D_Histo)")).replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
                    else:
                        Default_Histo_Name_Multi_Dim = str(Default_Histo_Name_z_pT_Bin.replace("(1D)",   "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
                    BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim).replace("Data_Type", "Bayesian")]
                    BAY_Histo_Unfold.Draw("H P E0 same")
                    BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim).replace("Data_Type", "Bin")]
                    BIN_Histo_Unfold.Draw("H P E0 same")
                    MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                    # MC_GEN_1D_Unfold.Draw("H P E0 same")
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                        ExTRUE_1D_Unfold.Draw("H P E0 same")
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                    else:
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])

                BAY_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
                BIN_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
                MC_GEN_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded,     1.3*Max_Unfolded)
                if("Missing" not in Variable_Title):
                    BAY_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                    BIN_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                    MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(0,            360)
                else:
                    BAY_Histo_Unfold.GetXaxis().SetRangeUser(1,            3.5)
                    BIN_Histo_Unfold.GetXaxis().SetRangeUser(1,            3.5)
                    MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(1,            3.5)
                if(tdf not in ["N/A"]):
                    ExTRUE_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                    if("Missing" not in Variable_Title):
                        ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(0,        360)
                    else:
                        ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(1,        3.5)
                    #####==========#####    MC TRUE Histogram    #####==========##### ################################################################
                    ExTRUE_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{",      "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"])        else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                    ExTRUE_1D_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), ""             if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                    ExTRUE_1D_Unfold.SetLineColor(root_color.Cyan)
                    ExTRUE_1D_Unfold.SetLineWidth(3)
                    ExTRUE_1D_Unfold.SetLineStyle(1)
                    ExTRUE_1D_Unfold.SetMarkerColor(root_color.Cyan)
                    ExTRUE_1D_Unfold.SetMarkerSize(1)
                    ExTRUE_1D_Unfold.SetMarkerStyle(20)
                # if(Multi_Dim_Option in ["Off"]):
                #     SVD_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                #     SVD_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                #     #####==========#####      SVD Histogram      #####==========##### ################################################################
                #     SVD_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ", str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                #     SVD_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                #     SVD_Histo_Unfold.SetLineColor(root_color.Pink)
                #     SVD_Histo_Unfold.SetLineWidth(2)
                #     SVD_Histo_Unfold.SetLineStyle(1)
                #     SVD_Histo_Unfold.SetMarkerColor(root_color.Pink)
                #     SVD_Histo_Unfold.SetMarkerSize(1)
                #     SVD_Histo_Unfold.SetMarkerStyle(20)

                #####==========#####     BAYESIAN Histogram      #####==========##### ################################################################
                BAY_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{",      "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"])        else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ",     str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                BAY_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), ""             if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                BAY_Histo_Unfold.SetLineColor(root_color.Teal)
                BAY_Histo_Unfold.SetLineWidth(2)
                BAY_Histo_Unfold.SetLineStyle(1)
                BAY_Histo_Unfold.SetMarkerColor(root_color.Teal)
                BAY_Histo_Unfold.SetMarkerSize(1)
                BAY_Histo_Unfold.SetMarkerStyle(21)
                #####==========#####    Bin-by-Bin Histogram     #####==========##### ################################################################
                BIN_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{",      "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"])        else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ",     str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                BIN_Histo_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), ""             if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                BIN_Histo_Unfold.SetLineColor(root_color.Brown)
                BIN_Histo_Unfold.SetLineWidth(2)
                BIN_Histo_Unfold.SetLineStyle(1)
                BIN_Histo_Unfold.SetMarkerColor(root_color.Brown)
                BIN_Histo_Unfold.SetMarkerSize(1)
                BIN_Histo_Unfold.SetMarkerStyle(22)
                #####==========#####      MC GEN Histogram       #####==========##### ################################################################
                MC_GEN_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{",      "5D Unfolding" if(str(Multi_Dim_Option) in ["5D"])        else "3D Unfolding" if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3D Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of ",     str(Variable_Title), "}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                MC_GEN_1D_Unfold.GetXaxis().SetTitle("".join([str(Variable_Title), ""             if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                MC_GEN_1D_Unfold.SetLineColor(root_color.Green)
                MC_GEN_1D_Unfold.SetLineWidth(3)
                MC_GEN_1D_Unfold.SetLineStyle(1)
                MC_GEN_1D_Unfold.SetMarkerColor(root_color.Green)
                MC_GEN_1D_Unfold.SetMarkerSize(1)
                MC_GEN_1D_Unfold.SetMarkerStyle(20)

                if(Fit_Test):
                    try:
                        statbox_move(Histogram=BAY_Histo_Unfold,     Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    except:
                        print(color.RED, "\nBAY_Histo_Unfold IS NOT FITTED\n", color.END)
                    try:
                        statbox_move(Histogram=BIN_Histo_Unfold,     Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    except:
                        print(color.RED, "\nBIN_Histo_Unfold IS NOT FITTED\n", color.END)
                    try:
                        statbox_move(Histogram=MC_GEN_1D_Unfold,     Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    except:
                        print(color.RED, "\nMC_GEN_1D_Unfold IS NOT FITTED\n", color.END)
                    if(tdf not in ["N/A"]):
                        try:
                            statbox_move(Histogram=ExTRUE_1D_Unfold, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                        except:
                            print(color.RED, "\nExTRUE_1D_Unfold IS NOT FITTED\n", color.END)
                    # if(Multi_Dim_Option in ["Off"]):
                    #     try:
                    #         statbox_move(Histogram=SVD_Histo_Unfold, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    #     except:
                    #         print(color.RED, "\nSVD_Histo_Unfold IS NOT FITTED\n", color.END)

            except Exception as e:
                print("".join([color.Error, "ERROR IN 1D (Input) Histograms:\n", color.END_B, str(traceback.format_exc()), color.END]))
            
        elif("Response" in str(Method)):
            try:
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].Draw("col")
            except Exception as e:
                print("".join([color.Error, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") Response Matrix:\n", color.END_B, str(traceback.format_exc()), color.END]))
        else:
            
            ##################################################################### ################################################################
            #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
            ##################################################################### ################################################################
            #####==========#####   Experimental Histogram    #####==========##### ################################################################
            if(str(Method) in ["rdf"]):
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetLineColor(root_color.Blue)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetLineWidth(2)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetLineStyle(1)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetMarkerColor(root_color.Blue)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetMarkerSize(1)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "rdf" if(not Sim_Test) else "mdf"))].SetMarkerStyle(21)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Blue)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Blue)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
                if(("phi_t" not in str(VARIABLE)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(VARIABLE))):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", " Distributions of ", str(Variable_Title), " #color[", str(root_color.Blue),  "]{(Experimental)}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}}{#font[22]{", str(Standard_Histogram_Title_Addition), "}}"]))
                # str_Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))
                # Histogram_List_All_title_test   = Histogram_List_All[str_Default_Histo_Name_z_pT_Bin].GetTitle()
                # print(f"Histogram_List_All[{str_Default_Histo_Name_z_pT_Bin}].GetTitle() =\n{Histogram_List_All_title_test}")
            #####==========#####      MC REC Histogram             #####==========##### ################################################################
            if(str(Method) in ["mdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Red)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Red)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(22)
                if(("phi_t" not in str(VARIABLE)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(VARIABLE))):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", " Distributions of ", str(Variable_Title), " #color[", str(root_color.Red),   "]{(MC REC)}}}{#scale[1.15]{",       str(Bin_Title_z_pT_Bin), "}}}{#font[22]{", str(Standard_Histogram_Title_Addition), "}}"]))
            #####==========#####      MC GEN Histogram             #####==========##### ################################################################
            if(str(Method) in ["gdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Green)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(3)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Green)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(20)
                if(("phi_t" not in str(VARIABLE)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(VARIABLE))):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", " Distributions of ", str(Variable_Title), " #color[", str(root_color.Green), "]{(MC GEN)}}}{#scale[1.15]{",       str(Bin_Title_z_pT_Bin), "}}}{#font[22]{", str(Standard_Histogram_Title_Addition), "}}"]))
            #####==========#####      MC Background Histogram       #####==========##### ################################################################
            if(str(Method) in ["Background", "Relative_Background"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Black)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(3)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Black)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(20)
                if(("phi_t" not in str(VARIABLE)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(VARIABLE))):
                    if(str(Method) in ["Background"]):
                        Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", " Distributions of ", str(Variable_Title), " ", str(root_color.Bold), "{(MC Background)}}}{#scale[1.15]{",      str(Bin_Title_z_pT_Bin), "}}}{#font[22]{", str(Standard_Histogram_Title_Addition), "}}"]))
                    else:
                        Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{", "5-Dimensional " if(str(Multi_Dim_Option) in ["5D"]) else "3-Dimensional " if(str(Multi_Dim_Option) in ["3D"]) else "(Old) 3-Dimensional " if(str(Multi_Dim_Option) not in ["Off"]) else "", " Distributions of ", str(Variable_Title), " ", str(root_color.Bold), "{(Relative MC Background)}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}}{#font[22]{", str(Standard_Histogram_Title_Addition), "}}"]))
            #####==========#####      MC True Histogram            #####==========##### ################################################################
            if(str(Method) in ["tdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Cyan)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(3)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Cyan)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(20)
            #####==========#####    Unfold Bin Histogram           #####==========##### ################################################################
            if(str(Method) in ["Bin", "bbb", "bin", "Bin-by-Bin", "Bin-By-Bin", "Bin-by-bin", "bin-by-bin"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Brown)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Brown)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1.5)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####   Unfold Bayes Histogram          #####==========##### ################################################################
            if(str(Method) in ["Bayesian", "Bayes"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Teal)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Teal)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####   RC Unfold Bin Histogram     #####==========##### ################################################################
            if(str(Method) in ["RC_Bin"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(ROOT.kOrange + 4)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(ROOT.kOrange + 4)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1.5)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####  RC Unfold Bayes Histogram    #####==========##### ################################################################
            if(str(Method) in ["RC_Bayesian"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(ROOT.kViolet - 8)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(ROOT.kViolet - 8)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####    Unfold SVD Histogram           #####==========##### ################################################################
            if(str(Method) in ["SVD"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Pink)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Pink)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            ##################################################################### ################################################################
            #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
            ##################################################################### ################################################################

            if("Missing" in Variable_Title):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetStats(0)
            
            try:
                if(Method in ["RC"]):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0.25, 1.7)
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].Draw("AP")
                    continue

                Histo_Bin_Max = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetMaximumBin())
                
                Run_Acceptance_EvGen = False
                if(Method in ["Acceptance", "Acceptance_ratio", "Relative_Background"]):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetStats(0)
                    if(Use_TTree and (Method not in ["Acceptance_ratio", "Relative_Background"])):
                        Acceptance_EvGen_Name = f'{str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))}_EvGen'
                        Acceptance_EvGen_Name = Acceptance_EvGen_Name.replace("Smear", "''")
                        Run_Acceptance_EvGen  = Acceptance_EvGen_Name in Histogram_List_All
                        if(Run_Acceptance_EvGen):
                            # print(f"\n{color.BBLUE}Comparing clasdis and EvGen Acceptance{color.END}\n")
                            Histogram_List_All[Acceptance_EvGen_Name].SetStats(0)
                            Histogram_List_All[Acceptance_EvGen_Name].SetLineColor(ROOT.kYellow + 3)
                            Histogram_List_All[Acceptance_EvGen_Name].SetLineStyle(7)
                            Histogram_List_All[Acceptance_EvGen_Name].SetLineWidth(3)
                            Histo_Bin_Max = max([Histo_Bin_Max, Histogram_List_All[Acceptance_EvGen_Name].GetBinContent(Histogram_List_All[Acceptance_EvGen_Name].GetMaximumBin())])
                        else:
                            print(f"\n{color.Error}Can't compare clasdis and EvGen Acceptance because {color.END_B}{color.UNDERLINE}{Acceptance_EvGen_Name}{color.END_B}{color.RED} is not in 'Histogram_List_All'{color.END}\n")
                
                for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetTitle()).replace(range_strings, ""))
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type",     Method))].Draw("H P E0 same")
                if("Missing" not in Variable_Title):
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
                else:
                    Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetXaxis().SetRangeUser(1, 3.5)

                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*Histo_Bin_Max)
                # if(Method not in ["Acceptance"]):
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetMaximumBin())))
                # else:
                #     Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 0.6)
                if(Run_Acceptance_EvGen):
                    Histogram_List_All[Acceptance_EvGen_Name].Draw("H P E0 same")
                if(Method in ["Acceptance", "Acceptance_ratio"]):
                    if(Method in ["Acceptance"]):
                        Acceptance_Cut_Line.Draw()
                    else:
                        Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))], Flat_Function_pave, [Fit_flat_Chisquared, Fit_flat_ndf], [A_Flat, A_Flat_Error], [B_Flat, B_Flat_Error], [C_Flat, C_Flat_Error] = Fitting_Phi_Function(Histo_To_Fit=Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))], Method=Method, Fitting="flat", Text_NDC=None) # Use default `Text_NDC`
                        Histogram_List_All[str(Flat_Function_pave.GetName())] = Flat_Function_pave
                        Histogram_List_All[str(Flat_Function_pave.GetName())].Draw("same")
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Modified()
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Update()
                elif(Fit_Test and (("phi_t" not in str(VARIABLE)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(VARIABLE)))):
                    if(Method not in ["rdf", "mdf"]):
                        try:
                            statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))], Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                        except:
                            print(f"{color.RED}\nTHE SELECTED HISTOGRAM WAS NOT FITTED\n{color.END}")
                            
                        # Below Sets Fill Color of Pads in the images which show the z-pT bins together (Used to help search for poor fits)
                        if(not True):
                            try:
                                if((get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))]) is not None) and (get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))]) > (9050 if(not Closure_Test) else 10))):
                                    print("Poor fit for:\n", str(Default_Histo_Name_z_pT_Bin.replace("Data_Type",         Method)), "\n\tchi^2 =", str(get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))])))
                                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Red)
                            except:
                                print(color.Error, "\n\n\nERROR WITH get_chisquare(...)\n\n\n", color.END)
                                print("Traceback:\n", str(traceback.format_exc()))

                            if(Closure_Test):
                                try:
                                    Fit_Par_B_Test, Fit_Par_B_Error_Test, Fit_Par_C_Test, Fit_Par_C_Error_Test = get_fit_parameters_B_and_C(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))])
                                    Ideal_Closure_B, Ideal_Closure_C = -0.5, 0.025
                                    if(None not in [Fit_Par_B_Test, Fit_Par_B_Error_Test, Fit_Par_C_Test, Fit_Par_C_Error_Test]):
                                        if((((Fit_Par_B_Test + Fit_Par_B_Error_Test) < Ideal_Closure_B) or ((Fit_Par_B_Test - Fit_Par_B_Error_Test) > Ideal_Closure_B)) and (((Fit_Par_C_Test + Fit_Par_C_Error_Test) < Ideal_Closure_C) or ((Fit_Par_C_Test - Fit_Par_C_Error_Test) > Ideal_Closure_C))):
                                            print("Incorrect fit parameter values for:\n", str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method)))
                                            if(All_z_pT_Canvas_cd_2_z_pT_Bin.GetFillColor() == root_color.Red):
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Black)
                                            else:
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Yellow)
                                        elif(((Fit_Par_B_Test + Fit_Par_B_Error_Test) < Ideal_Closure_B) or ((Fit_Par_B_Test - Fit_Par_B_Error_Test) > Ideal_Closure_B)):
                                            print("Incorrect B fit parameter values for:\n", str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method)))
                                            if(All_z_pT_Canvas_cd_2_z_pT_Bin.GetFillColor() == root_color.Red):
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Blue)
                                            else:
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Cyan)
                                        elif(((Fit_Par_C_Test + Fit_Par_C_Error_Test) < Ideal_Closure_C) or ((Fit_Par_C_Test - Fit_Par_C_Error_Test) > Ideal_Closure_C)):
                                            print("Incorrect C fit parameter values for:\n", str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method)))
                                            if(All_z_pT_Canvas_cd_2_z_pT_Bin.GetFillColor() == root_color.Red):
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Teal)
                                            else:
                                                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.Green)
                                except:
                                    print(f"{color.Error}\n\n\nERROR WITH get_fit_parameters_B_and_C(...)\n\n\n{color.END}")
                                    print(f"Traceback:\n{str(traceback.format_exc())}")
                        
            except Exception as e:
                print("".join([color.Error, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") METHOD = '", str(Method), "':\n", color.END_R, str(traceback.format_exc()), color.END]))

    ####  Filling Canvas (Right) - i.e., Individual z-pT Bins (End)  ###############################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    
    
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    Save_Name = "".join(["Unfolded_Histos_Q2_y_Bin_", str(Q2_Y_Bin), "_", str(Method), "_Smeared" if("Smear" in str(Default_Histo_Name)) else "", str(File_Save_Format)])
    if(extra_function_terms):
        Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
    if(Plot_Orientation in ["pT_z"]):
        Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Flipped", str(File_Save_Format)]))
    if(Multi_Dim_Option     in ["5D"]):
        Save_Name = "".join(["Multi_5D_",  str(Save_Name)])
    if(Multi_Dim_Option     in ["3D"]):
        Save_Name = "".join(["Multi_3D_",  str(Save_Name)])
    if(Multi_Dim_Option not in ["Off", "5D", "3D"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = f"Sim_Test_{Save_Name}"
    if(Mod_Test):
        Save_Name = f"Mod_Test_{Save_Name}"
        
    Save_Name = Save_Name.replace("Multi_5D_Unfold_5D_Response_Matrix_Normal", "Multi_5D_Unfold_Response_Matrix_Normal")
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                            "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                      "z_pT_phi_h")
    Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]),       str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                        "_")
    if(("phi_h" not in str(VARIABLE)) and ("phi_t" not in str(VARIABLE))):
        Save_Name = Save_Name.replace(str(File_Save_Format),                   "".join(["_", str(VARIABLE.replace("(", "")).replace(")", ""), str(File_Save_Format)]))
    if(Cut_Option   in ["UnCut"]):
        Save_Name = Save_Name.replace(str(File_Save_Format),                   "".join(["_UnCut",     str(File_Save_Format)]))
    if(Cut_Option   in ["Proton"]):
        Save_Name = Save_Name.replace(str(File_Save_Format),                   "".join(["_ProtonCut", str(File_Save_Format)]))
    if(Particle_Sector not in ["N/A", "None", "Error"]):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_{Particle_Sector}{File_Save_Format}")
    if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
    elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            All_z_pT_Canvas.SetName(Save_Name.replace(".root", ""))
        All_z_pT_Canvas.SaveAs(Save_Name)
        del All_z_pT_Canvas
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    
    
    
##################################################################################################################################################################
##==========##==========## Function for Creating the Images for All z-pT Bins Together  ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################

# def InspectHist(histo, label=""):
#     """
#     Print key properties of a TH1/TH2 before drawing:
#      - GetName()
#      - GetTitle()
#      - List of TF1 fit names (if any)
#     """
#     print(f"{color.BOLD}\n––– Inspecting {label} –––{color.END}")
#     print(f"  Name : {histo.GetName()}")
#     print(f"  Title: {histo.GetTitle()}")
#     # ROOT stores fit functions in the histogram’s internal list
#     funcs = histo.GetListOfFunctions()
#     if(funcs and funcs.GetSize()):
#         print(f"  Fits :")
#         for i in range(funcs.GetSize()):
#             f = funcs.At(i)
#             print(f"    [{i:>2}] {f.GetName()}  (Class {f.ClassName()})")
#     else:
#         print(f"{color.RED}  Fits : none{color.END}")
#     print(f"{color.BOLD}––––––––––––––––––––––––––––\n{color.END}")

####################################################################################################################################################################
##==========##==========##   Function for Individual Sector Dependent Unfolding Images    ##==========##==========##==========##==========##==========##==========##
####################################################################################################################################################################

def Unfolded_Sector_Dependent_Images(Histogram_List_All, Default_Histo_Name, Q2_Y_Bin="All", Z_PT_Bin="All", Multi_Dim_Option="Off", Sector_Ranges=["All"], Unfolding_Methods=["Bin", "Bayesian"], Show_text=True, Cut_or_Hist="Hist"):
    if((any(sec in Default_Histo_Name for sec in ["pipsec_", "esec_"])) or (Cut_or_Hist in ["Cut"])):
        Sector_Type = "pip" if("pipsec_" in Default_Histo_Name) else "e"

        if(Cut_or_Hist in ["Hist"]):
            Q2_y_Histo_rdf_Initial_Name = Default_Histo_Name.replace(f"({Sector_Type}sec_SECTOR)_(phi_t)",  "(Q2)_(y)")
            z_pT_Histo_rdf_Initial_Name = Default_Histo_Name.replace(f"({Sector_Type}sec_SECTOR)_(phi_t)",  "(z)_(pT)")
            Q2xB_Histo_rdf_Initial_Name = Default_Histo_Name.replace(f"({Sector_Type}sec_SECTOR)_(phi_t)", "(Q2)_(xB)")
        else:
            Q2_y_Histo_rdf_Initial_Name = Default_Histo_Name.replace("(phi_t)",                                   "(Q2)_(y)")
            z_pT_Histo_rdf_Initial_Name = Default_Histo_Name.replace("(phi_t)",                                   "(z)_(pT)")
            Q2xB_Histo_rdf_Initial_Name = Default_Histo_Name.replace("(phi_t)",                                  "(Q2)_(xB)")
            Q2_y_Histo_rdf_Initial_Name = Q2_y_Histo_rdf_Initial_Name.replace("(MultiDim_z_pT_Bin_Y_bin_phi_t)",  "(Q2)_(y)")
            z_pT_Histo_rdf_Initial_Name = z_pT_Histo_rdf_Initial_Name.replace("(MultiDim_z_pT_Bin_Y_bin_phi_t)",  "(z)_(pT)")
            Q2xB_Histo_rdf_Initial_Name = Q2xB_Histo_rdf_Initial_Name.replace("(MultiDim_z_pT_Bin_Y_bin_phi_t)", "(Q2)_(xB)")
            Q2_y_Histo_rdf_Initial_Name = Q2_y_Histo_rdf_Initial_Name.replace(f"_{Sector_Type}S_SECTORo",          "")
            z_pT_Histo_rdf_Initial_Name = z_pT_Histo_rdf_Initial_Name.replace(f"_{Sector_Type}S_SECTORo",          "")
            Q2xB_Histo_rdf_Initial_Name = Q2xB_Histo_rdf_Initial_Name.replace(f"_{Sector_Type}S_SECTORo",          "")
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name.replace("Smear", "''")).replace("Data_Type", "rdf")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name.replace("Smear", "''")).replace("Data_Type", "rdf")
        Q2xB_Histo_rdf_Initial_Name = str(Q2xB_Histo_rdf_Initial_Name.replace("Smear", "''")).replace("Data_Type", "rdf")
        for ii in ["(1D)", f"({Multi_Dim_Option})"]:
            Q2_y_Histo_rdf_Initial_Name = Q2_y_Histo_rdf_Initial_Name.replace(ii, "(Normal_2D)")
            z_pT_Histo_rdf_Initial_Name = z_pT_Histo_rdf_Initial_Name.replace(ii, "(Normal_2D)")
            Q2xB_Histo_rdf_Initial_Name = Q2xB_Histo_rdf_Initial_Name.replace(ii, "(Normal_2D)")

        if(f"(z_pT_Bin_{Z_PT_Bin})" not in Default_Histo_Name):
            Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_All)", f"(z_pT_Bin_{Z_PT_Bin})")

        # print(f"Default_Histo_Name = {Default_Histo_Name}")
            
        if(Multi_Dim_Option in ["Only"]):
            Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
            if((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) not in ["All", "0"])):
                Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            Default_Histo_Name = Default_Histo_Name.replace("Multi_Dim_Q2_Y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t")
            Default_Histo_Name = Default_Histo_Name.replace("Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t")
        if(Multi_Dim_Option in ["5D"]):
            Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_Q2_y_z_pT_phi_h)")
            Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_5D_Histo)")
        if(Multi_Dim_Option in ["3D"]):
            Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(MultiDim_z_pT_Bin_Y_bin_phi_t)")
            Default_Histo_Name = Default_Histo_Name.replace("(1D)",    "(MultiDim_3D_Histo)")
                
        if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
            Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", ("(Multi_Dim_Q2_y_Bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_Q2_Y_Bin_phi_t)") if(Multi_Dim_Option in ["Q2_y"])                                       else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
            if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
                Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        if(("(1D)" in Default_Histo_Name) and (("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Histo_Name) or ("(Multi_Dim_Q2_Y_Bin_phi_t)" in Default_Histo_Name)) and (str(Q2_Y_Bin) not in ["All", "0"])):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
        Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
        
        if(Cut_ProQ):
            Default_Histo_Name = Default_Histo_Name.replace("(Data_Type)_(SMEAR=", "(Data_Type)_(Proton)_(SMEAR=")
        if(Fit_Test):
            fit_function_title         = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
            if(Multi_Dim_Option in ["Off"]):
                if(not extra_function_terms):
                    fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
                else:
                    fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
            elif(Multi_Dim_Option     in ["5D", "3D"]):
                fit_function_title = f"#splitline{{Fitted Multidimensionally with: A (1 + B Cos(#phi_{{h}}) + C Cos(2#phi_{{h}}))}}{{{Multi_Dim_Option} Unfolding}}"
            elif(Multi_Dim_Option not in ["Fitted", "Only"]):
                fit_function_title = "".join(["Plotted with #splitline{#color[", str(root_color.Pink), "]{Multidimensional Unfolding}}{",                       "Q^{2}-y-#phi_{h} Unfolding" if(str(Z_PT_Bin) in ["All", "0"]) else "z-P_{T}-#phi_{h} Unfolding", "}"])
            else:
                if(not extra_function_terms):
                    fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))}{",                    "Q^{2}-y-#phi_{h} Unfolding" if((Multi_Dim_Option in ["Q2_y"]) or ((str(Z_PT_Bin) in ["All", "0"]) and (Multi_Dim_Option not in ["z_pT"]))) else "z-P_{T}-#phi_{h} Unfolding", "}"])
                else:
                    fit_function_title = "".join(["#splitline{Fitted Multidimensionally with: A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))}{", "Q^{2}-y-#phi_{h} Unfolding" if((Multi_Dim_Option in ["Q2_y"]) or ((str(Z_PT_Bin) in ["All", "0"]) and (Multi_Dim_Option not in ["z_pT"]))) else "z-P_{T}-#phi_{h} Unfolding", "}"])
        else:
            fit_function_title = ""
        Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["-2", "-1", "0", "Common_Int"]) else "All" if(str(Z_PT_Bin) in ["0"]) else "Integrated" if(str(Z_PT_Bin) in ["-1"]) else "Integrated (Over Common Range)", "}"]), "}}"])
        if(Standard_Histogram_Title_Addition not in [""]):
            Bin_Title = f"#splitline{{{Bin_Title}}}{{{Standard_Histogram_Title_Addition}}}"
            
        # Sector_Bin_Canvas = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", f"CANVAS_{Sector_Type}_Sector_Unfolding"), Num_Columns=4 if(Fit_Test) else 2, Num_Rows=1, Size_X=7800 if(Fit_Test) else 2500, Size_Y=4350 if(Fit_Test) else 2000, cd_Space=0)
        Sector_Bin_Canvas, Pad_Col0, Pad_Col1, Pad_Col2 = {}, {}, {}, {}
        for cor_num, cor in enumerate(Unfolding_Methods):
            Sector_Bin_Canvas[cor] = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", f"CANVAS_{Sector_Type}_Sector_{cor}_Unfolding"), Num_Columns=3 if(Fit_Test and (cor not in ["Acceptance"])) else 2, Num_Rows=1, Size_X=4*1008, Size_Y=4*576, cd_Space=0)
            ################################################################################################################################################################################################################################################################################################################################################################################################################
            ##===============##     2D Histos     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            Pad_Col0[cor] = Sector_Bin_Canvas[cor].cd(1)              ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            Pad_Col0[cor].SetPad(0.00, 1.1*Pad_Col0[cor].GetY1(), 0.2 if(Fit_Test) else 0.40, 0.9*Pad_Col0[cor].GetY2())
            Pad_Col0[cor].Divide(1, 3, 0)
            if(cor_num == 0):
                Q2_y_Histo_rdf_Initial = Histogram_List_All[Q2_y_Histo_rdf_Initial_Name]
                z_pT_Histo_rdf_Initial = Histogram_List_All[z_pT_Histo_rdf_Initial_Name]
                Q2xB_Histo_rdf_Initial = Histogram_List_All[Q2xB_Histo_rdf_Initial_Name]
                Drawing_Histo_Set = {}
            ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
                if("3D" in str(type(Q2_y_Histo_rdf_Initial))):
                    if(str(Z_PT_Bin) in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(1), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Q2_y_Histo_rdf_Initial.GetNbinsX())
                    else:
                        bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin)
                    Q2_y_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
                    Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial.Project3D('yz e')
                    Drawing_Histo_Set[Q2_y_Name].SetName(Q2_y_Name)
                    Drawing_Histo_Title = (str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("yz projection", "")).replace(f"Q^{{2}}-y Bin: {Q2_Y_Bin}", "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
                    Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
                    if(str(Z_PT_Bin) not in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        Drawing_Histo_Title = Drawing_Histo_Title.replace("z-P_{T} Bin: All", f"z-P_{{T}} Bin: {Z_PT_Bin}")
                    Drawing_Histo_Set[Q2_y_Name].SetTitle(Drawing_Histo_Title)
                else:
                    Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial
                    print("Using Q2_y_Histo_rdf_Initial =", str(Q2_y_Histo_rdf_Initial))
                if("3D" in str(type(Q2xB_Histo_rdf_Initial))):
                    if(str(Z_PT_Bin) in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        bin_Histo_2D_0, bin_Histo_2D_1 = Q2xB_Histo_rdf_Initial.GetXaxis().FindBin(1), Q2xB_Histo_rdf_Initial.GetXaxis().FindBin(Q2xB_Histo_rdf_Initial.GetNbinsX())
                    else:
                        bin_Histo_2D_0, bin_Histo_2D_1 = Q2xB_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin), Q2xB_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin)
                    Q2xB_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
                    Q2xB_Name = str(Q2xB_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[Q2xB_Name] = Q2xB_Histo_rdf_Initial.Project3D('yz e')
                    Drawing_Histo_Set[Q2xB_Name].SetName(Q2xB_Name)
                    Drawing_Histo_Title = (str(Drawing_Histo_Set[Q2xB_Name].GetTitle()).replace("yz projection", "")).replace(f"Q^{{2}}-y Bin: {Q2_Y_Bin}", "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
                    Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
                    if(str(Z_PT_Bin) not in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        Drawing_Histo_Title = Drawing_Histo_Title.replace("z-P_{T} Bin: All", f"z-P_{{T}} Bin: {Z_PT_Bin}")
                    Drawing_Histo_Set[Q2xB_Name].SetTitle(Drawing_Histo_Title)
                else:
                    Q2xB_Name = str(Q2xB_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[Q2xB_Name] = Q2xB_Histo_rdf_Initial
                    print("Using Q2xB_Histo_rdf_Initial =", str(Q2xB_Histo_rdf_Initial))
                if("3D" in str(type(z_pT_Histo_rdf_Initial))):
                    if(str(Z_PT_Bin) in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(1), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(z_pT_Histo_rdf_Initial.GetNbinsX())
                    else:
                        bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(Z_PT_Bin)
                    z_pT_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
                    z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial.Project3D('yz e')
                    Drawing_Histo_Set[z_pT_Name].SetName(z_pT_Name)
                    Drawing_Histo_Title = (str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("yz projection", "")).replace(f"Q^{{2}}-y Bin: {Q2_Y_Bin}", "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
                    Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
                    if(str(Z_PT_Bin) not in ["All", "Integrated", "Common_Int", "0", "-1", "-2"]):
                        Drawing_Histo_Title = Drawing_Histo_Title.replace("z-P_{T} Bin: All", f"z-P_{{T}} Bin: {Z_PT_Bin}")
                    Drawing_Histo_Set[z_pT_Name].SetTitle(Drawing_Histo_Title)
                else:
                    z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
                    Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial
                    print("Using z_pT_Histo_rdf_Initial =", str(z_pT_Histo_rdf_Initial))
                if((str(Standard_Histogram_Title_Addition) not in [""]) and ((str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[Q2xB_Name].GetTitle())) or (str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[z_pT_Name].GetTitle())) or ((str(Standard_Histogram_Title_Addition) not in str(Drawing_Histo_Set[Q2_y_Name].GetTitle()))))):
                    Drawing_Histo_Set[Q2_y_Name].SetTitle("".join(["#splitline{", str(Drawing_Histo_Set[Q2_y_Name].GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
                    Drawing_Histo_Set[Q2xB_Name].SetTitle("".join(["#splitline{", str(Drawing_Histo_Set[Q2xB_Name].GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
                    Drawing_Histo_Set[z_pT_Name].SetTitle("".join(["#splitline{", str(Drawing_Histo_Set[z_pT_Name].GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
            ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            # 1. Q² vs y plot
            Draw_Canvas(canvas=Pad_Col0[cor], cd_num=1, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
            Drawing_Histo_Set[Q2_y_Name].GetYaxis().SetRangeUser(1, 9)
            Drawing_Histo_Set[Q2_y_Name].SetStats(ROOT.kFALSE)
            Drawing_Histo_Set[Q2_y_Name].Draw("colz")
            for Q2_Y_Bin_ii in range(1, 18):
                color_ii = ROOT.kRed if(str(Q2_Y_Bin) in [str(Q2_Y_Bin_ii), "0", "All"]) else ROOT.kBlack
                Drawing_Histo_Set[f"Q2_Y_Bin_{Q2_Y_Bin_ii}"] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
                for line in Drawing_Histo_Set[f"Q2_Y_Bin_{Q2_Y_Bin_ii}"]:
                    line.SetLineColor(color_ii)
                    line.SetLineWidth(4 if(color_ii == ROOT.kRed) else 2)
                    line.DrawClone("same")
            draw_annotations(annotations)
            # 2. z vs pT plot
            Draw_Canvas(canvas=Pad_Col0[cor], cd_num=2, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
            Drawing_Histo_Set[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
            Drawing_Histo_Set[z_pT_Name].GetYaxis().SetRangeUser(0.1, 1)
            Drawing_Histo_Set[z_pT_Name].SetStats(ROOT.kFALSE)
            Drawing_Histo_Set[z_pT_Name].Draw("colz")
            if(Q2_Y_Bin not in ["All", "0", 0]):
                Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1, Set_Max_X=1.2, Select_z_pT_bin=Z_PT_Bin)
            draw_annotations(annotations)
            # 3. Q² vs xB plot
            Draw_Canvas(canvas=Pad_Col0[cor], cd_num=3, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
            Drawing_Histo_Set[Q2xB_Name].GetXaxis().SetRangeUser(0.1, 0.75)
            Drawing_Histo_Set[Q2xB_Name].GetYaxis().SetRangeUser(1, 9)
            Drawing_Histo_Set[Q2xB_Name].SetStats(ROOT.kFALSE)
            Drawing_Histo_Set[Q2xB_Name].Draw("colz")
            for Q2_Y_Bin_ii in range(1, 18):
                color_ii = ROOT.kRed if(str(Q2_Y_Bin) in [str(Q2_Y_Bin_ii), "0", "All"]) else ROOT.kBlack
                Drawing_Histo_Set[f"Q2_xB_borders_Q2_Y_Bin_{Q2_Y_Bin_ii}"] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, Use_xB=True)
                for line in Drawing_Histo_Set[f"Q2_xB_borders_Q2_Y_Bin_{Q2_Y_Bin_ii}"]:
                    line.SetLineColor(color_ii)
                    line.SetLineWidth(4 if(color_ii == ROOT.kRed) else 2)
                    line.DrawClone("same")
            draw_annotations(annotations)                             ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            ##===============##     2D Histos     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
            ################################################################################################################################################################################################################################################################################################################################################################################################################
            
            # Access and subdivide the first column into N rows × 3 columns (based on Sector_Ranges)
            Pad_Col1[cor] = Sector_Bin_Canvas[cor].cd(2)
            Pad_Col1[cor].SetPad(0.2 if(Fit_Test) else 0.40, Pad_Col1[cor].GetY1(), 0.55 if(Fit_Test) else 1.00, Pad_Col1[cor].GetY2())
            Pad_Col1[cor].Divide(1, len(Sector_Ranges), 0)
            Pad_Col1_rows = {}
            for cd_num, sec in enumerate(Sector_Ranges):
                Pad_Col1_rows[str(sec)] = Pad_Col1[cor].cd(cd_num+1)
                if(Sim_Test):
                    Pad_Col1_rows[str(sec)].Divide(3, 1, 0)
                else:
                    Pad_Col1_rows[str(sec)].Divide(2, 1, 0)
    
            if(Fit_Test and (cor not in ["Acceptance"])):
                # Access and subdivide the second column into 2 rows
                Pad_Col2[cor] = Sector_Bin_Canvas[cor].cd(3)
                Pad_Col2[cor].SetPad(0.55,  1.1*Pad_Col2[cor].GetY1(), 1.00, 0.9*Pad_Col2[cor].GetY2())
                Pad_Col2[cor].Divide(1, 2, 0)
    
            Sector_Title_Base = "#pi^{+} Sector !" if(Sector_Type in ["pip"]) else "Electron Sector !"
            graph, line = {}, {}
            if(cor_num == 0):
                Default_Histo_Name_In = Default_Histo_Name
                ExREAL_1D, MC_REC_1D, MC_GEN_1D, ExTRUE_1D, UNFOLD_1D = {}, {}, {}, {}, {}
            ##################################################################### ################################################################
            #####==========#####        Legend Setup         #####==========##### ################################################################
            Run_With_Legends = not True
            if(Run_With_Legends):
                Legends_REC = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                Legends_REC.SetNColumns(1)
                Legends_REC.SetBorderSize(0)
                Legends_REC.SetFillColor(0)
                Legends_REC.SetFillStyle(0)
            #####==========#####        Legend Setup         #####==========##### ################################################################
            ##################################################################### ################################################################
            for Sectors in Sector_Ranges:
                Sectors = str(Sectors)
                if(Sectors in ["All", "0"]):
                    Sector_Title = "All Sectors"
                    Default_Histo_Name = Default_Histo_Name_In.replace(f"({Sector_Type}sec_SECTOR)_", "")
                    Default_Histo_Name = Default_Histo_Name.replace(f"_{Sector_Type}S_SECTORo",       "")
                else:
                    Sector_Title = Sector_Title_Base.replace("!", str(Sectors))
                    Default_Histo_Name = Default_Histo_Name_In.replace(f"({Sector_Type}sec_SECTOR)_", f"({Sector_Type}sec_{Sectors})_")
                    Default_Histo_Name = Default_Histo_Name.replace(f"_{Sector_Type}S_SECTORo)_",     f"_{Sector_Type}S{Sectors}o)_")
                # print(f"Default_Histo_Name = {Default_Histo_Name}")
                if(cor_num == 0):
                    ExREAL_1D_name = str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''" if(not Sim_Test) else "Smear"))
                    MC_REC_1D_name = str(Default_Histo_Name.replace("Data_Type",     "mdf"))
                    MC_GEN_1D_name = str(Default_Histo_Name.replace("Data_Type",     "gdf")).replace("Smear", "''")
                    if("z_pT_Bin_Integrated" in Default_Histo_Name):
                        for names in [ExREAL_1D_name, MC_REC_1D_name, MC_GEN_1D_name]:
                            if(names not in Histogram_List_All):
                                if(names == ExREAL_1D_name):
                                    ExREAL_1D_name = ExREAL_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
                                if(names == MC_REC_1D_name):
                                    MC_REC_1D_name = MC_REC_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
                                if(names == MC_GEN_1D_name):
                                    MC_GEN_1D_name = MC_GEN_1D_name.replace("(z_pT_Bin_Integrated)", "(z_pT_Bin_All)")
                    ExREAL_1D[Sectors] = Histogram_List_All[ExREAL_1D_name].Clone(f"{ExREAL_1D_name}_Sector_{Sectors}")
                    MC_REC_1D[Sectors] = Histogram_List_All[MC_REC_1D_name].Clone(f"{MC_REC_1D_name}_Sector_{Sectors}")
                    MC_GEN_1D[Sectors] = Histogram_List_All[MC_GEN_1D_name].Clone(f"{MC_GEN_1D_name}_Sector_{Sectors}")
                    # InspectHist(histo=ExREAL_1D[Sectors], label=f"ExREAL_1D[{Sectors}] should -> ({ExREAL_1D_name}_Sector_{Sectors})")
                    # InspectHist(histo=MC_REC_1D[Sectors], label=f"MC_REC_1D[{Sectors}] should -> ({MC_REC_1D_name}_Sector_{Sectors})")
                    # InspectHist(histo=MC_GEN_1D[Sectors], label=f"MC_GEN_1D[{Sectors}] should -> ({MC_GEN_1D_name}_Sector_{Sectors})")
                    del ExREAL_1D_name
                    del MC_REC_1D_name
                    del MC_GEN_1D_name
                    
                    if(Sim_Test):
                        ExTRUE_1D[Sectors] = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''"))].Clone("".join([str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''")), f'_Sector_{Sectors}']))
                    else:
                        ExTRUE_1D[Sectors] = "N/A"
                        
                UNFOLD_1D[f"{cor}_{Sectors}"] = Histogram_List_All[str(Default_Histo_Name.replace('Data_Type', str(cor)))].Clone(f"{Histogram_List_All[str(Default_Histo_Name.replace('Data_Type', str(cor)))].GetName()}__{cor}_{Sectors}")
                # print(f"UNFOLD_1D['{cor}_{Sectors}'].GetName() = {UNFOLD_1D[f'{cor}_{Sectors}'].GetName()}")
                
                ##################################################################### ################################################################
                #####==========#####     Setting Axis Range      #####==========##### ################################################################
                ##################################################################### ################################################################
                if(("phi_t" not in str(Default_Histo_Name)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(Default_Histo_Name))):
                    if(cor_num == 0):
                        ExREAL_1D[Sectors].GetXaxis().SetRange(1,        ExREAL_1D[Sectors].GetXaxis().GetNbins()            + 1)
                        MC_REC_1D[Sectors].GetXaxis().SetRange(1,        MC_REC_1D[Sectors].GetXaxis().GetNbins()            + 1)
                        MC_GEN_1D[Sectors].GetXaxis().SetRange(1,        MC_GEN_1D[Sectors].GetXaxis().GetNbins()            + 1)
                        if(ExTRUE_1D[Sectors] not in ["N/A"]):
                            ExTRUE_1D[Sectors].GetXaxis().SetRange(1,    ExTRUE_1D[Sectors].GetXaxis().GetNbins()            + 1)
                    UNFOLD_1D[f"{cor}_{Sectors}"].GetXaxis().SetRange(1, UNFOLD_1D[f"{cor}_{Sectors}"].GetXaxis().GetNbins() + 1)
                else:
                    if(cor_num == 0):
                        ExREAL_1D[Sectors].GetXaxis().SetRange(0,        360)
                        MC_REC_1D[Sectors].GetXaxis().SetRange(0,        360)
                        MC_GEN_1D[Sectors].GetXaxis().SetRange(0,        360)
                        if(ExTRUE_1D[Sectors] not in ["N/A"]):
                            ExTRUE_1D[Sectors].GetXaxis().SetRange(0,    360)
                    UNFOLD_1D[f"{cor}_{Sectors}"].GetXaxis().SetRange(0, 360)
                ##################################################################### ################################################################
                #####==========#####     Setting Axis Range      #####==========##### ################################################################
                #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
                ##################################################################### ################################################################
                Default_Uncorrected_Titles = "#splitline{#scale[1.35]{Pre-"
                if(str(Multi_Dim_Option) in ["5D", "3D"]):
                    Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles}{Multi_Dim_Option} Unfolded"
                elif(str(Multi_Dim_Option) not in ["Off"]):
                    Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles}3D Unfolded (Old)"
                else:
                    Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles}Unfolded"
                Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles} Distributions #phi_{{h}}}}}}{{{Bin_Title}}}"
                Default___Corrected_Titles = f"#splitline{{#splitline{{{root_color.Bold}{{Fitted #color[ROOT_COLOR]{{CORRECTION_NAME}} Distribution of #phi_{{h}}}}}}{{{root_color.Bold}{{{fit_function_title}}}}}}}{{{Bin_Title}}}"
                if(Sector_Title not in [""]):
                    Default_Uncorrected_Titles = f"#splitline{{#scale[1.5]{{{Sector_Title}}}}}{{{Default_Uncorrected_Titles}}}"
                    Default___Corrected_Titles = f"#splitline{{#scale[1.5]{{{Sector_Title}}}}}{{{Default___Corrected_Titles}}}"
                Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles}; #phi_{{h}}"
                Default___Corrected_Titles = f"{Default___Corrected_Titles}; #phi_{{h}}"
                if('Smear' in str(Default_Histo_Name)):
                    Default_Uncorrected_Titles = f"{Default_Uncorrected_Titles} (Smeared)"
                    Default___Corrected_Titles = f"{Default___Corrected_Titles} (Smeared)"
                if(cor_num == 0):
                ##################################################################### ################################################################
                #####==========#####   Experimental Histogram    #####==========##### ################################################################
                    ExREAL_1D[Sectors].SetTitle(Default_Uncorrected_Titles)
                    ExREAL_1D[Sectors].SetLineColor(root_color.Blue)
                    ExREAL_1D[Sectors].SetLineWidth(2)
                    ExREAL_1D[Sectors].SetLineStyle(1)
                    ExREAL_1D[Sectors].SetMarkerColor(root_color.Blue)
                    ExREAL_1D[Sectors].SetMarkerSize(1)
                    ExREAL_1D[Sectors].SetMarkerStyle(21)
                #####==========#####      MC REC Histogram       #####==========##### ################################################################
                    MC_REC_1D[Sectors].SetTitle(Default_Uncorrected_Titles)
                    MC_REC_1D[Sectors].SetLineColor(root_color.Red)
                    MC_REC_1D[Sectors].SetLineWidth(2)
                    MC_REC_1D[Sectors].SetLineStyle(1)
                    MC_REC_1D[Sectors].SetMarkerColor(root_color.Red)
                    MC_REC_1D[Sectors].SetMarkerSize(1)
                    MC_REC_1D[Sectors].SetMarkerStyle(22)
                #####==========#####      MC GEN Histogram       #####==========##### ################################################################ ################################################################
                    MC_GEN_1D[Sectors].SetTitle(Default_Uncorrected_Titles)
                    MC_GEN_1D[Sectors].SetLineColor(root_color.Green)
                    MC_GEN_1D[Sectors].SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
                    MC_GEN_1D[Sectors].SetLineStyle(1)
                    MC_GEN_1D[Sectors].SetMarkerColor(root_color.Green)
                    MC_GEN_1D[Sectors].SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
                    MC_GEN_1D[Sectors].SetMarkerStyle(20)
                #####==========#####      MC TRUE Histogram      #####==========##### ################################################################ ################################################################
                    if(ExTRUE_1D[Sectors] not in ["N/A"]):
                        ExTRUE_1D[Sectors].SetTitle(str(Default___Corrected_Titles.replace("ROOT_COLOR", str(root_color.Cyan))).replace("CORRECTION_NAME", "True"))
                        ExTRUE_1D[Sectors].SetLineColor(root_color.Cyan)
                        ExTRUE_1D[Sectors].SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
                        ExTRUE_1D[Sectors].SetLineStyle(1)
                        ExTRUE_1D[Sectors].SetMarkerColor(root_color.Cyan)
                        ExTRUE_1D[Sectors].SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
                        ExTRUE_1D[Sectors].SetMarkerStyle(20)
                #####==========#####    Unfolded  Histograms     #####==========##### ################################################################ ################################################################
                if(cor   in ["Bin"]):
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetTitle(str(Default___Corrected_Titles.replace("ROOT_COLOR", str(root_color.Brown))).replace("CORRECTION_NAME", f"Multidimensional ({Multi_Dim_Option}) Bin-By-Bin"         if(str(Multi_Dim_Option) in ["5D", "3D"]) else "Bin-By-Bin"))
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetLineColor(root_color.Brown)
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetMarkerColor(root_color.Brown)
                elif(cor in ["Bayesian"]):
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetTitle(str(Default___Corrected_Titles.replace("ROOT_COLOR",  str(root_color.Teal))).replace("CORRECTION_NAME", f"Multidimensional ({Multi_Dim_Option}) RooUnfold Bayesian" if(str(Multi_Dim_Option) in ["5D", "3D"]) else "RooUnfold Bayesian"))
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetLineColor(root_color.Teal)
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetMarkerColor(root_color.Teal)
                elif(cor in ["Acceptance"]):
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetTitle(str(Default___Corrected_Titles.replace("ROOT_COLOR",  str(root_color.Black))).replace("CORRECTION_NAME", f"Multidimensional ({Multi_Dim_Option}) Acceptance"        if(str(Multi_Dim_Option) in ["5D", "3D"]) else "Acceptance"))
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetLineColor(root_color.Black)
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetMarkerColor(root_color.Black)
                else:
                    UNFOLD_1D[f"{cor}_{Sectors}"].SetTitle(str(Default___Corrected_Titles.replace("ROOT_COLOR",  str(root_color.Pink))).replace("CORRECTION_NAME", f"Unrecognized Correction Input: {cor}"))
                UNFOLD_1D[f"{cor}_{Sectors}"].SetLineWidth(2)
                UNFOLD_1D[f"{cor}_{Sectors}"].SetLineStyle(1)
                UNFOLD_1D[f"{cor}_{Sectors}"].SetMarkerSize(1)
                UNFOLD_1D[f"{cor}_{Sectors}"].SetMarkerStyle(21)
                ##################################################################### ################################################################ ################################################################
                #####==========#####  Setting Histogram Colors   #####==========##### ################################################################ ################################################################
                ##################################################################### ################################################################
                
                ######################################################################################
                ###==============###   Openning Canvas Pads to Draw Histograms    ###==============###
                ######################################################################################
                Y_axis_range = 1.5 #Findcomment
                ########################################################################## ###################################################################
                ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ###################################################################
                Draw_Canvas(Pad_Col1_rows[Sectors], 1, 0.15)
                ExREAL_1D[f"Normalized_{Sectors}"] = ExREAL_1D[Sectors].DrawNormalized("H P E0")
                MC_REC_1D[f"Normalized_{Sectors}"] = MC_REC_1D[Sectors].DrawNormalized("H P E0 same")
                MC_GEN_1D[f"Normalized_{Sectors}"] = MC_GEN_1D[Sectors].DrawNormalized("H P E0 same")
                configure_stat_box(hist=ExREAL_1D[f"Normalized_{Sectors}"], show_entries=False, canvas=Pad_Col1_rows[Sectors])
                configure_stat_box(hist=MC_REC_1D[f"Normalized_{Sectors}"], show_entries=False, canvas=Pad_Col1_rows[Sectors])
                configure_stat_box(hist=MC_GEN_1D[f"Normalized_{Sectors}"], show_entries=False, canvas=Pad_Col1_rows[Sectors])
                statbox_move(Histogram=ExREAL_1D[f"Normalized_{Sectors}"],  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                statbox_move(Histogram=MC_REC_1D[f"Normalized_{Sectors}"],  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                statbox_move(Histogram=MC_GEN_1D[f"Normalized_{Sectors}"],  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                statbox_move(Histogram=ExREAL_1D[Sectors],                  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                statbox_move(Histogram=MC_REC_1D[Sectors],                  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                statbox_move(Histogram=MC_GEN_1D[Sectors],                  Canvas=Pad_Col1_rows[Sectors], Print_Method="off")
                ExREAL_1D[f"Normalized_{Sectors}"].SetStats(0)
                MC_REC_1D[f"Normalized_{Sectors}"].SetStats(0)
                MC_GEN_1D[f"Normalized_{Sectors}"].SetStats(0)
                Max_Pre_Unfolded = max([ExREAL_1D[f"Normalized_{Sectors}"].GetBinContent(ExREAL_1D[f"Normalized_{Sectors}"].GetMaximumBin()), MC_REC_1D[f"Normalized_{Sectors}"].GetBinContent(MC_REC_1D[f"Normalized_{Sectors}"].GetMaximumBin()), MC_GEN_1D[f"Normalized_{Sectors}"].GetBinContent(MC_GEN_1D[f"Normalized_{Sectors}"].GetMaximumBin())])
                ExREAL_1D[f"Normalized_{Sectors}"].GetYaxis().SetRangeUser(0, Y_axis_range*Max_Pre_Unfolded)
                MC_REC_1D[f"Normalized_{Sectors}"].GetYaxis().SetRangeUser(0, Y_axis_range*Max_Pre_Unfolded)
                MC_GEN_1D[f"Normalized_{Sectors}"].GetYaxis().SetRangeUser(0, Y_axis_range*Max_Pre_Unfolded)
                if(Run_With_Legends):
                    if(str(Sectors) == str(Sector_Ranges[0])):
                        Legends_REC.AddEntry(ExREAL_1D[f"Normalized_{Sectors}"], "#scale[2]{Experimental}", "lpE")
                        Legends_REC.AddEntry(MC_REC_1D[f"Normalized_{Sectors}"], "#scale[2]{MC REC}",       "lpE")
                        Legends_REC.AddEntry(MC_GEN_1D[f"Normalized_{Sectors}"], "#scale[2]{MC GEN}",       "lpE")
                        Legends_REC.Draw("same")
                draw_annotations(annotations)
                ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ###################################################################
                ########################################################################## ###################################################################
                ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ###################################################################
                Draw_Canvas(Pad_Col1_rows[Sectors], 2, 0.15)
                UNFOLD_1D[f"{cor}_{Sectors}"].Draw("H P E0")
                UNFOLD_1D[f"{cor}_{Sectors}"].GetYaxis().SetRangeUser(0, Y_axis_range*(UNFOLD_1D[f"{cor}_{Sectors}"].GetBinContent(UNFOLD_1D[f"{cor}_{Sectors}"].GetMaximumBin())))
                if(cor in ["Acceptance"]):
                    Acceptance_Cut_Line.Draw("same")
                configure_stat_box(hist=UNFOLD_1D[f"{cor}_{Sectors}"], show_entries=True, canvas=Pad_Col1_rows[Sectors])
                statbox_move(Histogram=UNFOLD_1D[f"{cor}_{Sectors}"],  Canvas=Pad_Col1_rows[Sectors], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                draw_annotations(annotations)
                ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ###################################################################
                ########################################################################## ###################################################################
                ##=====##=====##    Drawing the 'True' Histogram          ##=====##=====## ###################################################################
                if(ExTRUE_1D[Sectors] not in ["N/A"]):
                    Draw_Canvas(Pad_Col1_rows[Sectors], 3, 0.15)
                    ExTRUE_1D[Sectors].Draw("H P E0")
                    ExTRUE_1D[Sectors].GetYaxis().SetRangeUser(0, Y_axis_range*(ExTRUE_1D[Sectors].GetBinContent(ExTRUE_1D[Sectors].GetMaximumBin())))
                    configure_stat_box(hist=ExTRUE_1D[Sectors],   show_entries=True, canvas=Pad_Col1_rows[Sectors])
                    statbox_move(Histogram=ExTRUE_1D[Sectors],    Canvas=Pad_Col1_rows[Sectors], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    draw_annotations(annotations)
                ##=====##=====##    Drawing the 'True' Histogram          ##=====##=====## ###################################################################
                ########################################################################## ###################################################################
            
                #########################################################################################################################
                ##==========##==========##==========##    Done Drawing Histograms to Sector Pads   ##==========##==========##==========##
            #############################################################################################################################
            ##==========##==========##==========##           Drawing Moments vs Sector Plots       ##==========##==========##==========##
            #############################################################################################################################
            if(Fit_Test and (cor not in ["Acceptance"])):
                Cor_Type = str(Default_Histo_Name_In.replace('Data_Type', str(cor)))
                Unfolding_Type = "Bin-by-Bin" if(cor in ["Bin"]) else "Bayesian"
                for Parameter_Type in ["B", "C"]:
                    Cor_Type_Par = Cor_Type.replace("(1D)", f"(Fit_Par_{Parameter_Type})")
                    if(Multi_Dim_Option in ["5D", "3D"]):
                        Cor_Type_Par = Cor_Type_Par.replace(f"(MultiDim_{Multi_Dim_Option}_Histo)", f"(Fit_Par_{Parameter_Type})")
                    key = f"(Bin:{Q2_Y_Bin}-{Z_PT_Bin})_(Unfold_with_{Unfolding_Type})_(Par_{Parameter_Type})_({Sector_Type})"
                    Parameter_Type_Title = "Cos(#phi_{h})" if(Parameter_Type in ["B"]) else "Cos(2#phi_{h})"
                    y_values, y_errors = [], []
                    for sec in ["All", "1", "2", "3", "4", "5", "6"]:
                        if(sec in ["All"]):
                            Cor_Type_Sec = Cor_Type_Par.replace(f"({Sector_Type}sec_SECTOR)_", "")
                            Cor_Type_Sec = Cor_Type_Sec.replace(f"_{Sector_Type}S_SECTORo",    "")
                        else:
                            Cor_Type_Sec = Cor_Type_Par.replace(f"({Sector_Type}sec_SECTOR)_", f"({Sector_Type}sec_{sec})_")
                            Cor_Type_Sec = Cor_Type_Sec.replace(f"_{Sector_Type}S_SECTORo)_",  f"_{Sector_Type}S{sec}o)_")
                        if((Cor_Type_Sec not in Histogram_List_All) or ((sec == "All") and all(sec_check not in Sector_Ranges for sec_check in ["All", "0", 0])) or ((sec != "All") and all(str(sec_check) != sec for sec_check in Sector_Ranges))):
                            print(f"{color.Error}Sector_Ranges did not include Sector {sec} (Setting measurement to 0){color.END}")
                            y_values.append(0)
                            y_errors.append(0)
                            if(Cor_Type_Sec not in Histogram_List_All):
                                print(f"{color.Error}'{Cor_Type_Sec}' is missing from Histogram_List_All{color.END}\nAvalaible:")
                                for test in Histogram_List_All:
                                    if(f"(Fit_Par_{Parameter_Type})" in str(test)):
                                        print(test)
                                print("")
                        else:
                            y_values.append(Histogram_List_All[Cor_Type_Sec][0])
                            y_errors.append(Histogram_List_All[Cor_Type_Sec][1])
                    x_values = range(7) # Assumes the 6 foward sectors + 'All Sectors'

                    if(Show_text):
                        # --- stats calculations ---
                        M_all         = y_values[0]
                        sigma_all     = y_errors[0]
                        sector_vals   = y_values[1:]
                        sector_errs   = y_errors[1:]
                        M_mean        = sum(sector_vals) / len(sector_vals)
                        sigma_sector  = ROOT.sqrt(sum((v - M_mean)**2 for v in sector_vals)/ (len(sector_vals) - 1))
                        sigma_mean    = ROOT.sqrt(sum(e*e for e in sector_errs)) / len(sector_errs)
                        # compute per‐sector percent differences
                        if(M_all != 0):
                            percent_errors = [abs(v - M_all) / abs(M_all) * 100 for v in sector_vals]
                        else:
                            percent_errors = [100 for v in sector_vals]
                        avg_pct_error  = sum(percent_errors) / len(percent_errors)
                        # --- end stats ---
                    
                    # Create TGraphErrors
                    n_points = len(x_values)
                    graph[key] = ROOT.TGraphErrors(n_points)
                    for i in range(n_points):
                        graph[key].SetPoint(i, x_values[i], y_values[i])
                        graph[key].SetPointError(i,      0, y_errors[i])
                    if("p" in Sector_Type):
                        graph[key].SetTitle(
                            f"#splitline{{#splitline{{Plot of {Parameter_Type_Title} vs #pi^{{+}} Sectors}}"
                            f"{{Q^{{2}}-y-z-P_{{T}} Bin: {Q2_Y_Bin}-{str(Z_PT_Bin).replace('Common_Int', 'Integrated (Over Common Range)')}}}}}{{Correction Method: #color[{root_color.Brown if(cor in ['Bin']) else root_color.Teal}]{{{f'{Multi_Dim_Option} ' if(Multi_Dim_Option in ['5D', '3D']) else ''}{Unfolding_Type}}}}};"
                            f" Pion Sector; {Parameter_Type_Title}")
                    else:
                        graph[key].SetTitle(
                            f"#splitline{{#splitline{{Plot of {Parameter_Type_Title} vs Electron Sectors}}"
                            f"{{Q^{{2}}-y-z-P_{{T}} Bin: {Q2_Y_Bin}-{str(Z_PT_Bin).replace('Common_Int', 'Integrated (Over Common Range)')}}}}}{{Correction Method: #color[{root_color.Brown if(cor in ['Bin']) else root_color.Teal}]{{{f'{Multi_Dim_Option} ' if(Multi_Dim_Option in ['5D', '3D']) else ''}{Unfolding_Type}}}}};"
                            f" Electron Sector; {Parameter_Type_Title}")
                    graph[key].SetMarkerStyle(21)
                    graph[key].SetMarkerColor(root_color.Brown if(cor in ['Bin']) else root_color.Teal)
                    graph[key].SetLineColor(root_color.Brown   if(cor in ['Bin']) else root_color.Teal)
                    
                    Pad_Col2[cor].cd(1 if(Parameter_Type in ["B"]) else 2)

                    if(Show_text):
                        pad1 = ROOT.TPad(f"pad1_{key}", f"pad1_{key}", 0.00, 0.00, 0.50, 1.00)
                        pad2 = ROOT.TPad(f"pad2_{key}", f"pad2_{key}", 0.50, 0.00, 1.00, 1.00)
                        pad1.SetRightMargin(0.01)
                        pad2.SetLeftMargin(0.15)
                        pad1.Draw()
                        pad2.Draw()
                        # —— Right pad: the stats box ——
                        pad2.cd()
                        stats = ROOT.TLatex()
                        stats.SetTextFont(42)
                        stats.SetNDC()
                        start_h     = 0.9
                        line_height = 0.06
                        # 1) Header for individual sectors
                        stats.SetTextSize(0.05)
                        stats.DrawLatex(0.10, start_h, f"Individual Sector Measurements of {Parameter_Type_Title}:")
                        # 2) All‐point first, largest text
                        stats.SetTextSize(0.045)
                        stats.DrawLatex(0.10, start_h-line_height,   f"All Sectors:        {M_all:8.5f} #pm {sigma_all:8.5f}")
                        # 3) List each sector
                        for j, (val, err, pct) in enumerate(zip(sector_vals, sector_errs, percent_errors)):
                            y = ((start_h-line_height) - 0.75*(line_height*(2*j+1))) if(j > 0) else ((start_h-line_height) - 0.8*(line_height*(j+1)))
                            stats.SetTextSize(0.035)
                            stats.DrawLatex(0.10, y,                    f"         Sector {j+1}:          {val:8.5f}   #pm {err:8.5f}")
                            stats.SetTextSize(0.03)
                            stats.DrawLatex(0.10, y - 0.75*line_height, f"                                       % Diff from All: {pct:6.2f}%")
                        # 4) Mean and Std Dev at bottom, slightly larger text
                        mean_y = (start_h-line_height) - 0.8*(line_height*(2*len(sector_vals)+1))
                        mErr_y = mean_y - (0.75*line_height)
                        std_y  = mErr_y - (0.75*line_height)
                        stats.SetTextSize(0.04)
                        stats.DrawLatex(0.10, mean_y, f"Mean of Sectors:   {M_mean:8.5f}  #pm {sigma_mean:8.5f}")
                        stats.SetTextSize(0.03)
                        stats.DrawLatex(0.10, mErr_y, f"                                       % Diff from All: {avg_pct_error:6.2f}%")
                        stats.SetTextSize(0.035)
                        stats.DrawLatex(0.10, std_y,  f"Std Dev of Sectors:  {sigma_sector:8.5f}")
                    # —— Left pad: the graph ——
                        pad1.cd()
                    graph[key].Draw("APL")
                    graph[key].GetXaxis().SetLimits(-0.5, n_points-0.5)
                    # graph[key].GetYaxis().SetRangeUser(-0.15, 0.1)
                    graph[key].GetYaxis().SetRangeUser(-0.25, 0.1)
                    line[key] = ROOT.TLine(-0.5, 0, n_points-0.5, 0)
                    line[key].SetLineColor(ROOT.kBlack)
                    line[key].Draw()
                    draw_annotations(annotations)

                    for i, sector in enumerate(["All", "1", "2", "3", "4", "5", "6"]):
                        graph[key].GetXaxis().ChangeLabel(i+1, -1, -1, -1, -1, -1, sector)
            
                    Pad_Col2[cor].Update()
                    Sector_Bin_Canvas[cor].Update()
            #########################################################################################################################
            ##==========##==========##==========##    Done Drawing Histograms to Canvas Pads   ##==========##==========##==========##
            #########################################################################################################################
                
            ##################################################################### ################################################################ ################################################################ ################################################################ #####################
            #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
            ##################################################################### ################################################################ ################################################################ ################################################################ #####################
            if(("phi_t)" in Default_Histo_Name) or ("phi_h)" in Default_Histo_Name)):
                bin_label = f"Q2_xB_Bin_{Q2_Y_Bin if(str(Q2_Y_Bin) not in ['0']) else 'All'}_z_pT_Bin_{Z_PT_Bin if(str(Z_PT_Bin) not in ['0']) else 'All'}"
                suffix = f"_{cor}_Unfolded_Histos_Smeared" if("Smear" in Default_Histo_Name) else f"_{cor}_Unfolded_Histos"
                Save_Name = f"{Sector_Type}Sector_Dependence_{bin_label}{suffix}{File_Save_Format}"
            else:
                Save_Name = f"{Default_Histo_Name}_Sector_Dependence_{cor}_Unfolded_Histos{File_Save_Format}".replace("(", "").replace(")", "")
            # Optional renaming/formatting adjustments
            replacements = {
                " ":                                         "_",
                "Multi_Dim_Histo_Multi_Dim":                 "Multi_Dim_Histo",
                "_Q2_xB_Bin_":                               "_Q2_y_Bin_" if(any(b in Binning_Method for b in ["y", "Y"])) else "_Q2_xB_Bin_",
                "Q2_y_Bin_phi_h":                            "Q2_y_phi_h",
                "z_pT_Bin_y_bin_phi_h":                      "z_pT_phi_h",
                "z_pT_Bin_Y_bin_phi_h":                      "z_pT_phi_h",
                "Multi_5D_Unfold_5D_MultiDim_5D":            "Multi_5D_Unfold",
                "Multi_5D_Unfold_5D_Response_Matrix_Normal": "Multi_5D_Unfold_Response_Matrix_Normal",
                "Multi_3D_Unfold_3D_MultiDim_3D":            "Multi_3D_Unfold",
                "Multi_3D_Unfold_3D_Response_Matrix_Normal": "Multi_3D_Unfold_Response_Matrix_Normal",
                f"_{File_Save_Format}":                      File_Save_Format,
                "__":                                        "_"}
            
            if(Multi_Dim_Option not in ["Off", "5D", "3D"]):
                Save_Name = f"Multi_Unfold_{Multi_Dim_Option}_{Save_Name}"
            elif(Multi_Dim_Option in ["5D", "3D"]):
                Save_Name = f"Multi_{Multi_Dim_Option}_Unfold_{Save_Name}"
            if(Sim_Test):
                Save_Name = f"Sim_Test_{Save_Name}"
            if(Mod_Test):
                Save_Name = f"Mod_Test_{Save_Name}"
            if(Cut_ProQ and f"_ProtonCut{File_Save_Format}" not in Save_Name):
                Save_Name = Save_Name.replace(File_Save_Format, f"_ProtonCut{File_Save_Format}")
            elif(Tag_ProQ and all(tag not in Save_Name for tag in [f"_TagProton{File_Save_Format}", f"_ProtonCut{File_Save_Format}"])):
                Save_Name = Save_Name.replace(File_Save_Format, f"_TagProton{File_Save_Format}")
            for old, new in replacements.items():
                Save_Name = Save_Name.replace(old, new)
            if(Saving_Q):
                if("root" in str(File_Save_Format)):
                    Sector_Bin_Canvas[cor].SetName(Save_Name.replace(".root", ""))
                Sector_Bin_Canvas[cor].SaveAs(Save_Name)
            print(f"{'Saved' if(Saving_Q) else 'Would be Saving'}: {color.BBLUE}{Save_Name}{color.END}")
            ##################################################################### ################################################################ ################################################################ ################################################################ #####################
            #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
            ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    else:
        print(f"{color.Error}Did not pass 'Sector Info' properly to Default_Histo_Name = {Default_Histo_Name} (requires 'pipsec_' or 'esec_'){color.END}")
    
####################################################################################################################################################################
##==========##==========##   Function for Individual Sector Dependent Unfolding Images    ##==========##==========##==========##==========##==========##==========##
####################################################################################################################################################################



##################################################################################################################################################################
##==========##==========## Function for Creating Images for Individual Plots with 2D Kinematics Bins Shown      ##==========##==========##==========##==========##
##################################################################################################################################################################

def Draw_Histogram_With_Kinematic_Bins(Histogram_List_All_Input, Default_Histo_Name_Input="", Data_Type="rdf", Smear="''", Variable1="", Variable2="", Q2_Y_Bin_Input="All", Z_PT_Bin_Input="All"):

    # ---------------------------------------------------------------------
    # 1) Determine User Inputs/Set Default Conditions (and Bin_Title)
    # ---------------------------------------------------------------------
    # Draw_3_only = False
    Variable1 = Variable1.replace("_smeared", "")
    Variable2 = Variable2.replace("_smeared", "")
    if((not Sim_Test) and ((Smear not in ["''"]) and (Data_Type not in ["mdf", "Bin", "Acceptance", "Bayesian", "bbb"]))):
        Smear = "''" # Smearing is only allowed for Data_Type = mdf unless the Sim_Test option is set to 'True'

    Bin_Title     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin_Input) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin_Input), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ["All", "0"]) else "All"]), "}}}"])
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])

    if(Data_Type in ["rdf"]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{CLAS12 RG-A Experimental Data}}"  if(not Sim_Test)    else f"#splitline{{{Bin_Title}}}{{Experimental Data}}"
    if(Data_Type in ["mdf"]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{Monte Carlo Reconstructed}}"      if(Smear in ["''"]) else f"#splitline{{{Bin_Title}}}{{(Smeared) Monte Carlo Reconstructed}}"
    if(Data_Type in ["gdf"]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{Monte Carlo Generated}}"
    if(Data_Type in ["Bin", "Bayesian", "bbb"]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{Acceptance Corrected Data}}"
    if(Data_Type in ["Acceptance"]):
        Bin_Title = f"#splitline{{{Bin_Title}}}{{Plot of {Data_Type}}}"
    if("Response_Matrix" in Default_Histo_Name_Input):
        Using_Response_Matrix = True
        Bin_Title = f"#splitline{{{Bin_Title}}}{{Plot of Response Matrix}}"
    else:
        Using_Response_Matrix = False
        
    # if(Variable1 in [""]):
    #     # No 4th Plot selected (drawing just the 3 main plots instead)
    #     Draw_3_only = True
    # elif(Variable1 not in Accepted_Variables):
    #     print(f"{color.Error}Variable1 = {color.UNDERLINE}{Variable1}{color.END}{color.Error} is not within the accepted list of variables defined for 'Draw_Histogram_With_Kinematic_Bins'{color.END}")
    #     return None
    # elif((Variable2 not in Accepted_Variables) and (Variable2 not in [""])):
    #     print(f"{color.Error}Variable2 = {color.UNDERLINE}{Variable2}{color.END}{color.Error} is not within the accepted list of variables defined for 'Draw_Histogram_With_Kinematic_Bins'{color.END}")
    #     print(f"{color.Error}Defaulting to a 1D plot of just Variable1 = {color.UNDERLINE}{Variable1}{color.END}")
    #     Variable2 = ""
    # User_Histo_Dimensions = 2 if(Variable2 not in [""]) else 1 if(not Draw_3_only) else 0
    # Variable_Full         = f"({Variable1})_({Variable2})" if(User_Histo_Dimensions == 2) else f"({Variable1})" if(User_Histo_Dimensions == 1) else "(VARIABLE_NOT_GIVEN)"
    # del Draw_3_only # Do not need this bool anymore (can use User_Histo_Dimensions instead)

    User_Histo_Dimensions = 2 if(Variable2 not in [""]) else 1 if(Variable1 not in [""]) else 0
    # User_Histo_Dimensions = 0 ==> 3‑panel mode
    Variable_Full         = f"({Variable1})_({Variable2})" if(User_Histo_Dimensions == 2) else f"({Variable1})" if(User_Histo_Dimensions == 1) else "(VARIABLE_NOT_GIVEN)"

    # ---------------------------------------------------------------------
    # 2) Find Relevant Histograms
    # ---------------------------------------------------------------------
    Input_Histo_Initial_Name = str(str(str(Default_Histo_Name_Input.replace("(VARIABLE)", Variable_Full)).replace("SMEAR_OPTION", Smear)).replace("Data_Type", Data_Type))

    Name_Uses_MultiDim    = any(multi in str(Default_Histo_Name_Input) for multi in ["(Multi-Dim Histo)", "(MultiDim_Q2_y_z_pT_phi_h)", "(MultiDim_5D_Histo)", "(MultiDim_3D_Histo)"])
    for dim_replace in ["(1D)", "(Multi-Dim Histo)", "(MultiDim_5D_Histo)", "(MultiDim_3D_Histo)", "(Response_Matrix)"]:
        Default_Histo_Name_Input     = Default_Histo_Name_Input.replace(dim_replace, "(Normal_2D)")
        if(User_Histo_Dimensions    == 2):
            Input_Histo_Initial_Name = Input_Histo_Initial_Name.replace(dim_replace, "(Normal_2D)") # If User Input is 2D, then the options listed for 'dim_replace' need to be replaced by (Normal_2D)
                                                                                                    # If the user input is NOT 2D, then replacing them here should be unnecessary (i.e., it is assumed that the request was intentional)
    # if("Integrate" in str(Z_PT_Bin_Input)):
    #     Default_Histo_Name_Input = Default_Histo_Name_Input.replace("Data_Type)_(SMEAR=", "Data_Type)_(Integrate)_(SMEAR=")
    #     print(f"Default_Histo_Name_Input = {Default_Histo_Name_Input}")
    Q2_y__Histo_Initial_Name = str(str(str(Default_Histo_Name_Input.replace("(VARIABLE)",    "(Q2)_(y)")).replace("SMEAR_OPTION", Smear)).replace("Data_Type", Data_Type))
    z_pT__Histo_Initial_Name = str(str(str(Default_Histo_Name_Input.replace("(VARIABLE)",    "(z)_(pT)")).replace("SMEAR_OPTION", Smear)).replace("Data_Type", Data_Type))
    Q2_xB_Histo_Initial_Name = str(str(str(Default_Histo_Name_Input.replace("(VARIABLE)",   "(Q2)_(xB)")).replace("SMEAR_OPTION", Smear)).replace("Data_Type", Data_Type))
    # if(Data_Type in ["Bin", "Acceptance", "Bayesian"]):
    if(Data_Type in ["Bin", "Bayesian"]):
        Q2_y__Histo_Initial_Name = Q2_y__Histo_Initial_Name.replace(Data_Type, "bbb") # Other Correction Methods do not apply to 2D histograms
        z_pT__Histo_Initial_Name = z_pT__Histo_Initial_Name.replace(Data_Type, "bbb") # Other Correction Methods do not apply to 2D histograms
        Q2_xB_Histo_Initial_Name = Q2_xB_Histo_Initial_Name.replace(Data_Type, "bbb") # Other Correction Methods do not apply to 2D histograms
    if(Data_Type in ["Acceptance"]):
        Q2_y__Histo_Initial_Name = Q2_y__Histo_Initial_Name.replace(Data_Type, "mdf") # Acceptance method does not apply to 2D histograms (using uncorrected MC instead)
        z_pT__Histo_Initial_Name = z_pT__Histo_Initial_Name.replace(Data_Type, "mdf") # Acceptance method does not apply to 2D histograms (using uncorrected MC instead)
        Q2_xB_Histo_Initial_Name = Q2_xB_Histo_Initial_Name.replace(Data_Type, "mdf") # Acceptance method does not apply to 2D histograms (using uncorrected MC instead)

    count_missing = 0
    Show_All_Q2 = False
    for check_histos in [Q2_y__Histo_Initial_Name, z_pT__Histo_Initial_Name, Q2_xB_Histo_Initial_Name, Input_Histo_Initial_Name]:
        if("VARIABLE_NOT_GIVEN" not in check_histos):
            if(check_histos         in [Q2_y__Histo_Initial_Name, Q2_xB_Histo_Initial_Name]):
                check_histos_All = check_histos.replace(f"Q2_y_Bin_{Q2_Y_Bin_Input}", "Q2_y_Bin_All")
                if(check_histos_All in Histogram_List_All_Input):
                    Show_All_Q2  = True
                else:
                    Show_All_Q2  = False
            if(check_histos     not in Histogram_List_All_Input):
                count_missing += 1
                print(f"{color.Error}Missing Histogram: {color.END_B}{color.UNDERLINE}{check_histos}{color.END}")
    if(count_missing > 0):
        print(f"{color.Error}Missing a total of {count_missing} histograms...\nCannot finish running Draw_Histogram_With_Kinematic_Bins(){color.END}")
        return None
    del count_missing # Variable no longer needed

    if(Show_All_Q2):
        Q2_y__Histo_Initial_Name = Q2_y__Histo_Initial_Name.replace(f"Q2_y_Bin_{Q2_Y_Bin_Input}", "Q2_y_Bin_All")
        Q2_xB_Histo_Initial_Name = Q2_xB_Histo_Initial_Name.replace(f"Q2_y_Bin_{Q2_Y_Bin_Input}", "Q2_y_Bin_All")
    Q2_y_Histo_Initial                = Histogram_List_All_Input[str(Q2_y__Histo_Initial_Name)]
    z_pT_Histo_Initial                = Histogram_List_All_Input[str(z_pT__Histo_Initial_Name)]
    Q2_xB_Histo_Initial               = Histogram_List_All_Input[str(Q2_xB_Histo_Initial_Name)]
    Drawing_Histo_Name_and_Found_List = [[Q2_y__Histo_Initial_Name, Q2_y_Histo_Initial], [z_pT__Histo_Initial_Name, z_pT_Histo_Initial], [Q2_xB_Histo_Initial_Name, Q2_xB_Histo_Initial]]
    if(User_Histo_Dimensions not in [0]):
        if(Data_Type not in ["Acceptance"]):
            Input_Histo_Initial = Histogram_List_All_Input[str(Input_Histo_Initial_Name)]
        else:
            Input_Histo_Initial = Histogram_List_All_Input[str(Input_Histo_Initial_Name).replace("z_pT_Bin_All", f"z_pT_Bin_{Z_PT_Bin_Input}")]
        Drawing_Histo_Name_and_Found_List.append([Input_Histo_Initial_Name, Input_Histo_Initial])

    

    # ---------------------------------------------------------------------
    # 3) Slice 3D Histograms and Get Individual Titles
    # ---------------------------------------------------------------------
    Drawing_Histo_Set = {}
    for Drawing_Histo_Name_and_Found in Drawing_Histo_Name_and_Found_List:
        Drawing_Histo_Name, Drawing_Histo_Found = Drawing_Histo_Name_and_Found
        #########################################################
        ##===============##    Set  Titles    ##===============##
        Drawing_Histo_Title = "Default Title"
        if(Drawing_Histo_Name   in [Q2_y__Histo_Initial_Name]):
            Drawing_Histo_Title = "Q^{2} vs y ; y ; Q^{2}"
        elif(Drawing_Histo_Name in [z_pT__Histo_Initial_Name]):
            Drawing_Histo_Title = "z vs P_{T} ; P_{T} ; z"
        elif(Drawing_Histo_Name in [Q2_xB_Histo_Initial_Name]):
            Drawing_Histo_Title = "Q^{2} vs x_{B} ; x_{B} ; Q^{2}"
        elif(User_Histo_Dimensions == 2):
            Drawing_Histo_Title = f"{variable_Title_name(str(Variable1))} vs {variable_Title_name(str(Variable2))} ; {variable_Title_name(str(Variable2))} ; {variable_Title_name(str(Variable1))}"
        else:
            Drawing_Histo_Title = f"{variable_Title_name(str(Variable1))} ; {variable_Title_name(str(Variable1))}"
        if(Smear not in ["''"]):
            Drawing_Histo_Title = Drawing_Histo_Title.replace(" ;", " (Smeared);")
            Drawing_Histo_Title = f"{Drawing_Histo_Title} (Smeared)"
        ##===============##    Set  Titles    ##===============##
        #########################################################
        ##===============##     3D Slices     ##===============##
        if("3D" in str(type(Drawing_Histo_Found))):
            # Find Comment
            # if(Drawing_Histo_Name    in [Q2_y__Histo_Initial_Name, z_pT__Histo_Initial_Name, Q2_xB_Histo_Initial_Name]):
            if(Drawing_Histo_Name    in [Q2_y__Histo_Initial_Name, Q2_xB_Histo_Initial_Name]):
                # if((not Show_All_Q2) or  Drawing_Histo_Name   in  [z_pT__Histo_Initial_Name]):
                bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(1), Drawing_Histo_Found.GetXaxis().FindBin(Drawing_Histo_Found.GetNbinsX())
                Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            else:
                bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0", "Integrated", "-1", "Common_Int", "-2"]) else 1), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0", "Integrated", "-1", "Common_Int", "-2"]) else Drawing_Histo_Found.GetNbinsX())
                if(str(Z_PT_Bin_Input) not in ["All", "0"]):
                    Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            New_Name = str(Drawing_Histo_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D"  if(str(Z_PT_Bin_Input)     in ["All", "0"]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found.Project3D('yz e')
            Drawing_Histo_Set[New_Name].SetName(New_Name)
        else:
            New_Name = str(Drawing_Histo_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D"  if(str(Z_PT_Bin_Input)     in ["All", "0"]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found
            # if(("MultiDim_Q2_y_z_pT_phi_h" not in New_Name) or ("MultiDim_z_pT_Bin_Y_bin_phi_t" not in New_Name)):
            #     print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
        Drawing_Histo_Set[New_Name].SetTitle(Drawing_Histo_Title)
        ##===============##     3D Slices     ##===============##
        #########################################################

    # ---------------------------------------------------------------------
    # 4) Build the TCanvas (and define Save_Name)
    # ---------------------------------------------------------------------
    Save_Name = f"Kinematics_of_{Data_Type}_VARIABLE_for_Q2_y_Bin_{str(Q2_Y_Bin_Input) if(str(Q2_Y_Bin_Input) not in ['0']) else 'All'}_z_pT_Bin_{str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ['0']) else 'All'}"
    if(User_Histo_Dimensions != 0):
        Save_Name = str(str(Save_Name.replace("VARIABLE", str(Variable_Full))).replace("(", "")).replace(")", "")
    else:
        Save_Name = Save_Name.replace("_VARIABLE_", "_")
    if(Smear not in ["''"]):
        Save_Name = f"{Save_Name}_Smeared{File_Save_Format}"
    else:
        Save_Name = f"{Save_Name}{File_Save_Format}"
    if(Name_Uses_MultiDim):
        Save_Name = "".join(["Multi_Unfold_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = f"Sim_Test_{Save_Name}"
    if(Mod_Test):
        Save_Name = f"Mod_Test_{Save_Name}"
    if(not any(binning in Binning_Method for binning in ["y", "Y"])):
        print(f"{color.Error}\n\nUsing Old Binning Scheme (i.e., Binning_Method = {str(Binning_Method)}){color.END}\n\n")
        Save_Name = Save_Name.replace("_Q2_y_Bin_", "_Q2_xB_Bin_")
    if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
    elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name))):
        Save_Name = Save_Name.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
    Save_Name = Save_Name.replace(" ",  "_")
    Save_Name = Save_Name.replace("__", "_")

    extra_top = 800 # Extra space for the top margin
    if(User_Histo_Dimensions != 0):
        Canvas = ROOT.TCanvas(Save_Name, Save_Name, 1600, extra_top + 1200)
        Canvas.SetTopMargin(extra_top / float(1200 + extra_top))
        Canvas.Divide(2, 2, 0, 0)
    else: # Just need 3 TPads (1 row, 3 columns)
        Canvas = ROOT.TCanvas(Save_Name, Save_Name, 1600, extra_top + 800)
        Canvas.SetTopMargin(extra_top / float(800  + extra_top))
        Canvas.Divide(3, 1, 0, 0)

    # ---------------------------------------------------------------------
    # 5) Drawing Histograms (Loop through Drawing_Histo_Set)
    # ---------------------------------------------------------------------
    drawn_1, drawn_2, drawn_3, drawn_4 = False, False, False, False
    for Drawing_Histo in Drawing_Histo_Set:
        # -----------------------------------------------------------------
        # 5.1) Drawing Histogram Q2 vs y
        # -----------------------------------------------------------------
        if(("(Q2)_(y)" in Drawing_Histo) and (not drawn_1)):
            drawn_1 = True
            Draw_Canvas(canvas=Canvas, cd_num=1, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
            Drawing_Histo_Set[Drawing_Histo].SetStats(False)
            Drawing_Histo_Set[Drawing_Histo].GetYaxis().SetRangeUser(0, 11)
            Drawing_Histo_Set[Drawing_Histo].Draw("colz")
            palette_move(canvas=Canvas, histo=Drawing_Histo_Set[Drawing_Histo], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
            Q2_y_borders = {}
            if("y_bin" in Binning_Method):
                line_num = 0
                for b_lines in Q2_y_Border_Lines(-1):
                    try:
                        Q2_y_borders[(line_num)] = ROOT.TLine()
                    except:
                        print(f"{color.RED}Error in Q2_y_borders[({line_num})]{color.END}")
                    Q2_y_borders[(line_num)].SetLineColor(1)
                    Q2_y_borders[(line_num)].SetLineWidth(2)
                    Q2_y_borders[(line_num)].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
                    line_num += 1
            else:
                for Q2_Y_Bin_ii in range(1, 18, 1):
                    Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
                    for line in Q2_y_borders[Q2_Y_Bin_ii]:
                        line.DrawClone("same")
                if(Q2_Y_Bin_Input not in ['All']):
                   if(int(Q2_Y_Bin_Input) in range(1, 18)):
                        for line_bin in Q2_y_borders[int(Q2_Y_Bin_Input)]:
                            line_bin.SetLineColor(ROOT.kRed)
                            line_bin.SetLineWidth(6)
                            line_bin.DrawClone("same")
        # -----------------------------------------------------------------
        # 5.2) Drawing Histogram z vs pT
        # -----------------------------------------------------------------
        elif(("(z)_(pT)" in Drawing_Histo) and (not drawn_2)):
            drawn_2 = True
            Draw_Canvas(canvas=Canvas, cd_num=2, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
            Drawing_Histo_Set[Drawing_Histo].SetStats(False)
            Drawing_Histo_Set[Drawing_Histo].Draw("colz")
            palette_move(canvas=Canvas, histo=Drawing_Histo_Set[Drawing_Histo], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
            if(str(Q2_Y_Bin_Input) not in ["All", "0"]):
                if("y_bin" in Binning_Method):
                    z_pT_borders = {}
                    Max_z  = max(z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2])
                    Min_z  = min(z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2])
                    Max_pT = max(z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2])
                    Min_pT = min(z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2])
                    for zline in z_pT_Border_Lines(Q2_Y_Bin_Input)[0][2]:
                        for pTline in z_pT_Border_Lines(Q2_Y_Bin_Input)[1][2]:
                            z_pT_borders[zline] = ROOT.TLine()
                            z_pT_borders[zline].SetLineColor(1)
                            z_pT_borders[zline].SetLineWidth(2)
                            z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                            z_pT_borders[pTline] = ROOT.TLine()
                            z_pT_borders[pTline].SetLineColor(1)
                            z_pT_borders[pTline].SetLineWidth(2)
                            z_pT_borders[pTline].DrawLine(pTline, Min_z, pTline, Max_z)
                else:
                    Drawing_Histo_Set[Drawing_Histo].GetXaxis().SetRangeUser(0, 1.2)
                    Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin_Input, Set_Max_Y=1.2, Set_Max_X=1.2, Select_z_pT_bin=Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0", "Integrated", "-1", "Common_Int", "-2"]) else None)
            # -------------------------------------------------------------
            # 5.2.1) Drawing Missing Mass Cuts on z vs pT plot
            # -------------------------------------------------------------
            if(any(binning in str(Binning_Method) for binning in ["y", "Y"])):
                Drawing_Histo_Set[Drawing_Histo].GetXaxis().SetRangeUser(0, 1.2)
                MM_z_pT_borders = {}
                # Create a TLegend
                MM_z_pT_legend = ROOT.TLegend(0.5, 0.1, 0.9, 0.2)  # (x1, y1, x2, y2)
                MM_z_pT_legend.SetNColumns(2)
                MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin=Q2_Y_Bin_Input, Plot_Orientation="z_pT")
                for MM_lines in MM_z_pT_borders:
                    MM_z_pT_borders[MM_lines].DrawClone("same")
                MM_z_pT_legend.DrawClone("same")
        # -----------------------------------------------------------------
        # 5.3) Drawing Histogram Q2 vs xB
        # -----------------------------------------------------------------
        elif(("(Q2)_(xB)" in Drawing_Histo) and (not drawn_3)):
            drawn_3 = True
            Draw_Canvas(canvas=Canvas, cd_num=3, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
            Create_Stat_Box = True and (User_Histo_Dimensions == 0)
            # ---- stat box create (if not drawing TPad 4) ----------------
            if(Create_Stat_Box):
                # ROOT.gStyle.SetOptStat(1110)  # Entries / Mean / RMS
                Drawing_Histo_Set[Drawing_Histo].SetStats(True)  # show box
                ROOT.gStyle.SetOptStat(1110)
            else:
                Drawing_Histo_Set[Drawing_Histo].SetStats(False)
            Drawing_Histo_Set[Drawing_Histo].GetYaxis().SetRangeUser(0, 11)
            Drawing_Histo_Set[Drawing_Histo].Draw("colz")
            palette_move(canvas=Canvas, histo=Drawing_Histo_Set[Drawing_Histo], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
            Q2_xB_borders = {}
            for Q2_Y_Bin_ii in range(1, 18, 1):
                Q2_xB_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, Use_xB=True)
                for line in Q2_xB_borders[Q2_Y_Bin_ii]:
                    line.DrawClone("same")
            if(Q2_Y_Bin_Input not in ['All']):
                if(int(Q2_Y_Bin_Input) in range(1, 18)):
                    for line_bin in Q2_xB_borders[int(Q2_Y_Bin_Input)]:
                        line_bin.SetLineWidth(6)
                        line_bin.SetLineColor(ROOT.kRed)
                        line_bin.DrawClone("same")
            # ---- stat box (if not drawing TPad 4) -----------------------
            if(Create_Stat_Box):
                Canvas.Modified()
                Canvas.Update()
                stat = Drawing_Histo_Set[Drawing_Histo].GetListOfFunctions().FindObject("stats")
                if(stat):
                    stat.SetX1NDC(0.7)
                    stat.SetY1NDC(0.85)
                    stat.SetX2NDC(0.9)
                    stat.SetY2NDC(0.7)
                    stat.SetBorderSize(1)
                    stat.SetFillColor(0)
                    stat.SetTextColor(ROOT.kBlack)
        # -----------------------------------------------------------------
        # 5.4) Drawing User Input Histogram
        # -----------------------------------------------------------------
        elif((Variable_Full in Drawing_Histo) and (not drawn_4)):
            drawn_4 = True
            Draw_Canvas(canvas=Canvas, cd_num=4, left_add=0.15, right_add=0.075, up_add=0.1, down_add=0.1)
            if(Data_Type in ["Bin", "Acceptance", "Bayesian", "bbb"]):
                Correction_Method = "Bin-by-Bin Correction" if(Data_Type in ["Bin", "bbb"]) else "Bayesian Unfolding Correction" if(Data_Type in ["Bayesian"]) else "Bin-by-Bin Acceptance"
                Drawing_Histo_Set[Drawing_Histo].SetTitle(f"#splitline{{{Drawing_Histo_Set[Drawing_Histo].GetTitle()}}}{{{Correction_Method}}}")
            Create_Stat_Box = True
            # ---- stat box create (only pad 4) ---------------------------
            if(Create_Stat_Box):
                # ROOT.gStyle.SetOptStat(1110)  # Entries / Mean / RMS
                Drawing_Histo_Set[Drawing_Histo].SetStats(True)  # show box
                # Drawing_Histo_Set[Drawing_Histo].SetOptStat(1110)
                ROOT.gStyle.SetOptStat(1110)
            else:
                Drawing_Histo_Set[Drawing_Histo].SetStats(False)
            if((User_Histo_Dimensions == 2) or Using_Response_Matrix):
                Drawing_Histo_Set[Drawing_Histo].Draw("colz")
                palette_move(canvas=Canvas, histo=Drawing_Histo_Set[Drawing_Histo], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
            else: 
                if(("phi" in Variable_Full) and ("MultiDim" not in Variable_Full)):
                    Drawing_Histo_Set[Drawing_Histo].GetXaxis().SetRangeUser(0, 360)
                # if(Data_Type not in ["Acceptance"]):
                Drawing_Histo_Set[Drawing_Histo].GetYaxis().SetRangeUser(0, 1.5*Drawing_Histo_Set[Drawing_Histo].GetMaximum())
                # else:
                #     Drawing_Histo_Set[Drawing_Histo].GetYaxis().SetRangeUser(0, 1)
                Drawing_Histo_Set[Drawing_Histo].Draw("H P E0 same")
            # ---- stat box (only pad 4) ----------------------------------
            if(Create_Stat_Box):
                Canvas.Modified()
                Canvas.Update()
                stat = Drawing_Histo_Set[Drawing_Histo].GetListOfFunctions().FindObject("stats")
                if(stat):
                    stat.SetX1NDC(0.7)
                    stat.SetY1NDC(0.85)
                    stat.SetX2NDC(0.9)
                    stat.SetY2NDC(0.7)
                    stat.SetBorderSize(1)
                    stat.SetFillColor(0)
                    stat.SetTextColor(ROOT.kBlack)

    # ---------------------------------------------------------------------
    # 6) Global title textbox
    # ---------------------------------------------------------------------
    Canvas.cd()
    title_latex = ROOT.TLatex()
    title_latex.SetNDC(True)
    title_latex.SetTextAlign(22)
    title_latex.SetTextSize(0.03)
    title_latex.DrawLatex(0.5, 0.94, Bin_Title)
    Canvas.Modified()
    Canvas.Update()

    # ---------------------------------------------------------------------
    # 7. Save/Return Canvas
    # ---------------------------------------------------------------------
    if(Saving_Q):
        Canvas.SaveAs(Save_Name)
        print(f"Saved: {color.BBLUE}{str(Save_Name)}{color.END}")
    else:
        print(f"Would be Saving: {color.BBLUE}{str(Save_Name)}{color.END}")
    return Canvas

##################################################################################################################################################################
##==========##==========## Function for Creating Images for Individual Plots with 2D Kinematics Bins Shown      ##==========##==========##==========##==========##
##################################################################################################################################################################






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
    if((str(Datatype) == 'mdf') or ((str(Datatype) in ['rdf']) and Sim_Test)):
        file = "".join(["Matching_REC_MC/SIDIS_epip_MC_Matched_", str(FileName), ".root"])
    if(str(Datatype) == 'gdf'):
        file = "".join(["GEN_MC/SIDIS_epip_MC_GEN_",              str(FileName), ".root"])
        
    loading = "".join([location, file])
    
    return loading



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
# # Common_Name = "Unfolding_Tests_V13_All"
# # Common_Name = "Analysis_Note_Update_V4_All"
# # Common_Name = "Multi_Dimension_Unfold_V1_All"
# # # Common_Name = "Multi_Dimension_Unfold_V2_All"
# # Common_Name = "Multi_Dimension_Unfold_V3_All"
# # Common_Name = "Analysis_Note_Update_VF_APS_All"

# # Common_Name = "New_Binning_Schemes_V8_All"

# Common_Name = "Gen_Cuts_V6_All"
# # Common_Name = "Gen_Cuts_V7_All"
# Common_Name = "Gen_Cuts_V8_All"

# # # Common_Name = "New_Bin_Tests_V5_All"

# # Common_Name = "CrossCheck_V2_All"
# # # Common_Name = "Pass_2_CrossCheck_V2_All"

# Common_Name = "New_Q2_Y_Bins_V2_All"


# Common_Name = "Pass_2_New_Q2_Y_Bins_V4_All"
Common_Name = "Pass_2_New_Q2_Y_Bins_V5_All"

# Common_Name = "MultiDim_Bin_Test_V1_All"
# Common_Name = "Pass_2_Correction_Effects_V1_5197"

Common_Name = "Pass_2_5D_Unfold_Test_V4_All"
Common_Name = "5D_Unfold_Test_V4_All"

Common_Name = "Pass_2_5D_Unfold_Test_V7_All"
Common_Name = "5D_Unfold_Test_V7_All"


Common_Name = "Pass_2_5D_Unfold_Test_V7_All"
Common_Name = "Pass_2_New_Sector_Cut_Test_V3_All"

Common_Name = "Pass_2_New_Sector_Cut_Test_V10_All"

Common_Name = "Pass_2_New_Sector_Cut_Test_V12_All"

Common_Name = "Pass_2_New_Fiducial_Cut_Test_V5_All"


Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC0_V7_All"
Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC5_V7_All"

Common_Name = "Pass_2_New_Fiducial_Cut_Test_V9_All"
# Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC7_V9_All"

Common_Name = "Pass_2_New_Fiducial_Cut_Test_V11_All"
Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_11_V11_All"
# Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC0_V11_All"

Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_14_V12_All"
# Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_11_V12_All"
Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC0_V12_All"

# Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_14_V13_All"

Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_14_V14_All"

# Common_Name = "Pass_2_New_Fiducial_Cut_Test_FC_14_V15_All"

# Common_Name = "Pass_2_New_Integrated_Bins_Test_FC_14_V1_All"

Common_Name = "Pass_2_Plots_for_Maria_FC_14_V1_All"
Common_Name = "Pass_2_Plots_for_Maria_FC_14_V2_All" # Same as V1 above but with sector plots and no MM plots
Common_Name = "Pass_2_Plots_for_Maria_FC_14_V3_All" # Same as V2 above but with additional MC files (run rdf with V2)

# if(not (Tag_ProQ or Cut_ProQ)):
Common_Name = "Pass_2_Sector_Integrated_Tests_FC_14_V2_All"

Common_Name = "Pass_2_Sector_Tests_FC_14_V1_EvGen_All"


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

if(not Use_TTree):
    print(f"\n{color.Error}Ignore the following information - Will be using the existing TTree file instead of the RDataFrames{color.END}\n")
    
##################################
##   Real (Experimental) Data   ##
##################################
if(True):
    print("".join([color.BOLD, "\nNot using the common file name for the Real (Experimental) Data...\n", color.END]))
if(False):
    REAL_File_Name = Common_Name
else:
    # REAL_File_Name = "Unfolding_Tests_V11_All"
    # REAL_File_Name = "Pass_2_Correction_Effects_V1_5197"
    # REAL_File_Name = "Pass_2_5D_Unfold_Test_V3_All" if(Pass_Version in ["Pass 2"]) else "5D_Unfold_Test_V3_All"
    # REAL_File_Name = "Pass_2_5D_Unfold_Test_V7_All" if(Pass_Version in ["Pass 2"]) else "5D_Unfold_Test_V7_All"
    # REAL_File_Name = "Pass_2_New_Sector_Cut_Test_V1_All"
    # REAL_File_Name = "Pass_2_Plots_for_Maria_FC_14_V1_All"
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
if(True):
    print("".join([color.BOLD, "\nNot using the common file name for the Reconstructed Monte Carlo Data...\n", color.END]))
if(False):
    MC_REC_File_Name = Common_Name
else:
    # MC_REC_File_Name = "Unfolding_Tests_V13_Failed_All"
    # MC_REC_File_Name = "Analysis_Note_Update_V6_All"
    # MC_REC_File_Name = "Gen_Cuts_V2_Fixed_All"
    # MC_REC_File_Name = "CrossCheck_V3_All"
    # # MC_REC_File_Name = "Pass_2_CrossCheck_V3_All"
    # MC_REC_File_Name = "Pass_2_New_Q2_Y_Bins_V3_Smeared_V2_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_New_Q2_Y_Bins_V4_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_New_Q2_Y_Bins_V5_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_New_Q2_Y_Bins_V5_All"       if(Smearing_Options in ["no_smear"]) else "Pass_2_New_Q2_Y_Bins_V5_All"
    # MC_REC_File_Name = "Pass_2_Correction_Effects_V1_30"
    # MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V1_All"      if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V1_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V5_All"      if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V5_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V7_All"      if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V7_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_Background_Tests_V4_All"
    # MC_REC_File_Name = "Unsmeared_Pass_2_New_Sector_Cut_Test_V1_All" if(Smearing_Options in ["no_smear"]) else "Pass_2_New_Sector_Cut_Test_V1_All"
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
if(True):
    print("".join([color.BOLD, "\nNot using the common file name for the Generated Monte Carlo Data...\n", color.END]))
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


if(Mod_Test and ("Gen_Cuts_V7_All" in str(Common_Name))):
    MC_REC_File_Name = "Gen_Cuts_V7_Modulated_All"
    MC_GEN_File_Name = "Gen_Cuts_V7_Modulated_All"
elif(Mod_Test):
    if("_Modulated" not in str(MC_REC_File_Name)):
        MC_REC_File_Name = str(MC_REC_File_Name).replace("_All", "_Modulated_All")
    if("_Modulated" not in str(MC_GEN_File_Name)):
        MC_GEN_File_Name = str(MC_GEN_File_Name).replace("_All", "_Modulated_All")

        
# 'TRUE_File_Name' refers to a file which is used in the closure tests where the simulated data is unfolded - corresponds to the distribution that should ideally be returned if the unfolding procedure is working correctly
TRUE_File_Name = ""
if(Sim_Test):
    REAL_File_Name = MC_REC_File_Name
    TRUE_File_Name = MC_GEN_File_Name
    
if(Closure_Test):
    if("_Modulated" not in str(MC_REC_File_Name)):
        REAL_File_Name = str(MC_REC_File_Name).replace("_All", "_Modulated_All")
    else:
        REAL_File_Name = MC_REC_File_Name
    if("_Modulated" not in str(MC_GEN_File_Name)):
        TRUE_File_Name = str(MC_GEN_File_Name).replace("_All", "_Modulated_All")
    else:
        TRUE_File_Name = MC_GEN_File_Name


################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################










###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################
try:
    rdf = ROOT.TFile(str(FileLocation(str(REAL_File_Name), "rdf")), "READ")
    print("".join(["The total number of histograms available for the", color.BLUE,  " Real (Experimental) Data" if(not Sim_Test) else " Test Experimental (Simulated) Data", " " if(Sim_Test) else "       ", color.END, " in '", color.BOLD, REAL_File_Name,   color.END, "' is ", color.BOLD, str(len(rdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
    print("".join(["The total number of histograms available for the", color.RED,   " Reconstructed Monte Carlo Data", " " if(not Sim_Test) else "     ",                                                     color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
    print("".join(["The total number of histograms available for the", color.GREEN, " Generated Monte Carlo Data", "     " if(not Sim_Test) else "         ",                                                 color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
    
if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])):
    print("\nWill be using a file as the 'True' distribution (i.e., what 'rdf' should look like after unfolding)")
    try:
        tdf = ROOT.TFile(str(FileLocation(str(TRUE_File_Name), "gdf")), "READ")
        print("".join(["The total number of histograms available for the", color.CYAN, " 'True' Monte Carlo Data   ", "     " if(not Sim_Test) else "         ",                                              color.END, " in '", color.BOLD, TRUE_File_Name,   color.END, "' is ", color.BOLD, str(len(tdf.GetListOfKeys())), color.END]))
    except:
        print("".join([color.Error, "\nERROR IN GETTING THE 'tdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
else:
    tdf = "N/A"
###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################

# else:
#     print(f"\n{color.BOLD}Will be loading existing TTree file{color.END}\n")

if(Create_txt_File):
    # String_For_Output_txt = "".join([color.BOLD, """
    # ######################################################################################################################################################
    # ##==========##    COMPARISON OF DATA TO MONTE CARLO FOR RELEVANT KINEMATIC VARIABLES    ##==========##==========##==========##==========##==========##
    # ######################################################################################################################################################
    # """, color.END, str(str(Date_Time).replace("Started running", "Ran")).replace("\n", ""), """
    # """, str(str(("".join(["Ran for Q2-y Bin(s): ", str(Q2_xB_Bin_List)]).replace("[",  "")).replace("]", "")).replace("'0'", "'All'")), """

    # Files Used:
    # """, "".join(["\tFile name for ", color.BLUE,  "Real (Experimental) Data"            if(not Sim_Test) else " Test Experimental (Simulated) Data", " " if(Sim_Test) else "       ", color.END, " in '", color.BOLD, REAL_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(REAL_File_Name),   "rdf")))]), """
    # """, "".join(["\tFile name for ", color.RED,   "Reconstructed Monte Carlo Data", " " if(not Sim_Test) else "     ",                                                                color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_REC_File_Name), "mdf")))]), """
    # """, "".join(["\tFile name for ", color.GREEN, "Generated Monte Carlo Data", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_GEN_File_Name), "gdf")))]), """
    # """, "".join(["\tFile name for ", color.CYAN,  "'True' Monte Carlo Data   ", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, TRUE_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(TRUE_File_Name),   "gdf"))),   "\n"]) if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])) else "", """
    # ##=========================================================##
    # ##==========##   Starting to Run Comparisons   ##==========##
    # ##=========================================================##"""])
    if(not Use_TTree):
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
        String_For_Output_txt = f"""{color.BOLD}
    ######################################################################################################################################################
    ##==========##    COMPARISON OF DATA TO MONTE CARLO FOR RELEVANT KINEMATIC VARIABLES    ##==========##==========##==========##==========##==========##
    ######################################################################################################################################################
    {color.END}{timer.start_find(return_Q=True)}
    {str(str(("".join(["Ran for Q2-y Bin(s): ", str(Q2_xB_Bin_List)]).replace("[",  "")).replace("]", "")).replace("'0'", "'All'"))}

    File Used:
    {color.BOLD}{TTree_Name}{color.END}\t(Is the reference TTree file used in place of the individual RDataFrames)
    ##=========================================================##
    ##==========##   Starting to Run Comparisons   ##==========##
    ##=========================================================##"""
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
# Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods, Parameter_List_Unfold, Parameter_List_Bin = {}, {}, {}, {}, {}, {}, {}, {}, [], []
Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods = {}, {}, {}, {}, {}, {}, {}, {}
Parameter_List_Unfold_Methods["SVD"], Parameter_List_Unfold_Methods["Bin"], Parameter_List_Unfold_Methods["Bayes"] = [], [], []
List_of_All_Histos_For_Unfolding = {}
count, count_failed = 0, 0

Relative_Background_Run_Q = False
if(Use_TTree):
    print(f"\n{color.Error}Using Existing TTree {color.END_B}(File is: {color.UNDERLINE}{TTree_Name}{color.END_B}){color.Error} instead of Creating New Unfolded Histograms{color.END}\n")
    TTree_Input = ROOT.TFile.Open(TTree_Name, "READ")
    List_of_All_Histos_For_Unfolding = {}
    for key in TTree_Input.GetListOfKeys():
        key_name = key.GetName()
        if(not Relative_Background_Run_Q):
            Relative_Background_Run_Q = "Relative_Background" in str(key_name)
        if("TList_of_" in key_name):
            List_of_All_Histos_For_Unfolding[key_name] = [float(str(item.GetString())) for item in TTree_Input.Get(key_name)]
        else:
            List_of_All_Histos_For_Unfolding[key_name] = TTree_Input.Get(key_name)
    TTree_Input.Close()
    print(f"{color.BBLUE}Recovered: {color.BGREEN}{len(List_of_All_Histos_For_Unfolding)}{color.END_B}{color.BLUE} items{color.END}\n")
    timer.time_elapsed()
else:
    for ii in mdf.GetListOfKeys():
        if(Cor_Compare):
            print(f"{color.Error}\nCorrection Comparison Plot Option selected does NOT include Unfolding/Acceptance Corrections{color.END_R} (as of 4-18-2024){color.END}\n")
            break
        out_print_main = str(ii.GetName()).replace("mdf", "DataFrame_Type")

        # if(all(fixed_cuts not in out_print_main for fixed_cuts in ["cut_Complete_SIDIS_I", "cut_Complete_SIDIS_Proton_I"])):
        #     continue
        # print("test")
    
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
                    print("".join([color.Error, "ERROR IN MDF...\n", color.END_R, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
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
                out_print_main_rdf = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
                out_print_main_gdf = out_print_main.replace("DataFrame_Type", "gdf")
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
                out_print_main_rdf = out_print_main_rdf.replace("smear", "")
                out_print_main_gdf = out_print_main_gdf.replace("smear", "")
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                ################################################################################
                ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
                out_print_main_rdf    = out_print_main_rdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                out_print_main_gdf    = out_print_main_gdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                out_print_main_mdf_1D = out_print_main_mdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
                ################################################################################
                
                if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                    print("".join([color.Error, "ERROR IN MDF...\n", color.END_R, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf_1D), color.END, "\n"]))
                    for ii in mdf.GetListOfKeys():
                        if(("5D_Response_Matrix_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))
                if(Sim_Test):
                    out_print_main_rdf = out_print_main_mdf_1D
                    out_print_main_tdf = out_print_main_gdf
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print("".join([color.Error, "ERROR IN TDF...\n", color.END_R, "Dataframe is missing: ", color.BCYAN,  str(out_print_main_tdf), color.END, "\n"]))
                            continue
                    else:
                        print("".join([color.Error,     "ERROR IN TDF...\n", color.END_R, "Missing Dataframe...",   color.END, "\n"]))
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN RDF...\n", color.END_R, "Dataframe is missing: ", color.BBLUE,  str(out_print_main_rdf), color.END, "\n"]))
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN GDF...\n", color.END_R, "Dataframe is missing: ", color.BGREEN, str(out_print_main_gdf), color.END, "\n"]))
                    continue
    
                count += 1
                print("".join([color.BGREEN, "\n(5D) Unfolding: ", str(out_print_main), "\n", color.END]))
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
                if((out_print_main_bdf_1D in mdf.GetListOfKeys()) and ("Background") in str(out_print_main_bdf_1D)):
                    MC_BGS_1D = mdf.Get(out_print_main_bdf_1D)
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
                out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
                out_print_main_rdf = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
                out_print_main_gdf = out_print_main.replace("DataFrame_Type", "gdf")
                
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
                out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                out_print_main_gdf = out_print_main_gdf.replace("_smeared", "")
                out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
                out_print_main_gdf = out_print_main_gdf.replace("smear",    "")
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                ################################################################################
                
                if(out_print_main_mdf not in mdf.GetListOfKeys()):
                    print("".join([color.Error, "ERROR IN MDF...\n", color.END_R, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
                    for ii in mdf.GetListOfKeys():
                        if(("Normal_2D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))
                if(Sim_Test):
                    out_print_main_rdf = out_print_main_mdf
                    out_print_main_tdf = out_print_main_gdf
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print("".join([color.Error, "ERROR IN TDF...\n", color.END_R, "Dataframe is missing: ", color.BCYAN,  str(out_print_main_tdf), color.END, "\n"]))
                            continue
                    else:
                        print("".join([color.Error,     "ERROR IN TDF...\n", color.END_R, "Missing Dataframe...",   color.END, "\n"]))
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN RDF...\n", color.END_R, "Dataframe is missing: ", color.BBLUE,  str(out_print_main_rdf), color.END, "\n"]))
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN GDF...\n", color.END_R, "Dataframe is missing: ", color.BGREEN, str(out_print_main_gdf), color.END, "\n"]))
                    continue
    
                count += 1
                print("".join([color.BGREEN, "\n(Sector) Unfolding: ", str(out_print_main), "\n", color.END]))
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
                if((out_print_main_bdf in mdf.GetListOfKeys()) and ("Background") in str(out_print_main_bdf)):
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
            Conditions_For_Unfolding.append("MultiDim_"     in str(out_print_main)) # For running only (New 3D) Multidimensional Unfolding Plots
    
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
                
                out_print_main_rdf = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
                out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
                out_print_main_gdf = out_print_main.replace("DataFrame_Type", "gdf")
    
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
                out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                out_print_main_rdf = out_print_main_rdf.replace("smear_",   "")
                out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
                out_print_main_gdf = out_print_main_gdf.replace("_smeared", "")
                out_print_main_gdf = out_print_main_gdf.replace("smear_",   "")
                out_print_main_gdf = out_print_main_gdf.replace("smear",    "")
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
                    print("".join([color.Error, "ERROR IN MDF...\n", color.END_R, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
                    continue
    
                out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
                if(("".join([", (Var-D2='z_pT_Bin", str(Binning_Method)]) not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
                    out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "".join(["]), (Var-D2='z_pT_Bin", str(Binning_Method), "" if("smear" not in str(out_print_main_mdf_1D)) else "_smeared", "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
                if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                    print("".join([color.Error, "ERROR IN MDF...\n", color.END_R, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf_1D), color.END, "\n"]))
                    for ii in mdf.GetListOfKeys():
                        if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))
    
                if(Sim_Test):
                    out_print_main_rdf = out_print_main_mdf_1D
                    out_print_main_tdf = out_print_main_gdf
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print("".join([color.Error, "ERROR IN TDF...\n", color.END_R, "Dataframe is missing: ", color.BCYAN,  str(out_print_main_tdf), color.END, "\n"]))
                            continue
                    else:
                        print("".join([color.Error,     "ERROR IN TDF...\n", color.END_R, "Missing Dataframe...",   color.END, "\n"]))
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN RDF...\n", color.END_R, "Dataframe is missing: ", color.BBLUE,  str(out_print_main_rdf), color.END, "\n"]))
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print("".join([color.Error,         "ERROR IN GDF...\n", color.END_R, "Dataframe is missing: ", color.BGREEN, str(out_print_main_gdf), color.END, "\n"]))
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
                    print("".join([color.Error, "\nERROR - Q2_xB_Bin_Unfold = ", str(Q2_xB_Bin_Unfold), color.END]))
                    print(f"Error is with\n out_print_main = {out_print_main}")
    
                if((str(Q2_xB_Bin_Unfold) not in Q2_xB_Bin_List) and ("Multi_Dim_Q2_y_Bin_phi_t" not in str(out_print_main))):
                    # print("Skipping unselected Q2-xB Bin...")
                    print("".join(["Bin ", str(Q2_xB_Bin_Unfold), " is not in Q2_xB_Bin_List = ", str(Q2_xB_Bin_List)]))
                    continue
    
                count += 1
                print("".join(["\nUnfolding: ", str(out_print_main)]))
                ExREAL_1D_initial     = rdf.Get(out_print_main_rdf)
                MC_REC_1D_initial     = mdf.Get(out_print_main_mdf_1D)
                MC_GEN_1D_initial     = gdf.Get(out_print_main_gdf)
                Response_2D_initial   = mdf.Get(out_print_main_mdf)
                if(tdf not in ["N/A"]):
                    ExTRUE_1D_initial = tdf.Get(out_print_main_tdf)
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
                if((out_print_main_bdf_1D in mdf.GetListOfKeys()) and ("Background") in str(out_print_main_bdf_1D)):
                    MC_BGS_1D_initial = mdf.Get(out_print_main_bdf_1D)
                    # print(f"{color.BLUE}\n\nout_print_main_bdf_1D = {out_print_main_bdf_1D}{color.END}")
                    # print(f"{color.BOLD}\nMC_BGS_1D_initial  -> {MC_BGS_1D_initial.GetName()}{color.END}")
                    # print(f"{color.BOLD}MC_REC_1D_initial  -> {MC_REC_1D_initial.GetName()}{color.END}\n")
                else:
                    MC_BGS_1D_initial = "None"
                    print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
                    raise TypeError("Missing Background Histogram")
                if(Sim_Test and (str(MC_BGS_1D_initial) not in ["None"])):
                    # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                    ExREAL_1D_initial.Add(MC_BGS_1D_initial)
                    
                # Use_Gen_MM_Cut = True
                Use_Gen_MM_Cut = False
    
                if(("Gen_MM_Cut" in str(out_print_main_rdf)) or ("Gen_MM_Cut" in str(out_print_main_mdf_1D)) or ("Gen_MM_Cut" in str(out_print_main_gdf))  or ("Gen_MM_Cut" in str(out_print_main_mdf))):
                    if((not Use_Gen_MM_Cut) and (Common_Name not in ["Gen_Cuts_V7_All"])):
                        print(color.Error, "\nERROR: NOT TRYING TO RUN Gen_MM_Cut\n", color.END)
                        continue
                    print(color.BBLUE, "INCLUDES Gen_MM_Cut", color.END)
                    # print("out_print_main_rdf    =", out_print_main_rdf)
                    # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                    # print("out_print_main_gdf    =", out_print_main_gdf)
                    # print("out_print_main_mdf    =", out_print_main_mdf)
    
                    # if(Use_Gen_MM_Cut):
                    if(abs(Response_2D_initial.GetZaxis().GetXmin()) == abs(Response_2D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        Response_2D_initial = Response_2D_initial.Project3D("yx e")
                        Response_2D_initial.SetTitle(str(Response_2D_initial.GetTitle()).replace(" yx projection", ""))
                    else:
                        print(color.Error, "\n\nERROR WITH Gen_MM_Cut Response Matrix", color.END, "\nResponse_2D_initial = ", Response_2D_initial)
                        raise TypeError("ERROR WITH Gen_MM_Cut Response Matrix")
    
                    if("3D" in str(type(MC_REC_1D_initial))):
                        if(abs(MC_REC_1D_initial.GetZaxis().GetXmin()) == abs(MC_REC_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            MC_REC_1D_initial = MC_REC_1D_initial.Project3D("yx e")
                            MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" yx projection", ""))
                        else:
                            print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC REC HISTO", color.END, "\nMC_REC_1D_initial = ", MC_REC_1D_initial)
                            raise TypeError("ERROR WITH Gen_MM_Cut MC REC HISTO")
                    else:
                        if(abs(MC_REC_1D_initial.GetYaxis().GetXmin()) == abs(MC_REC_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                            MC_REC_1D_initial = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()), 0, -1, "e")
                            MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" x projection", ""))
                        else:
                            print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC REC HISTO", color.END, "\nMC_REC_1D_initial = ", MC_REC_1D_initial)
                            raise TypeError("ERROR WITH Gen_MM_Cut MC REC HISTO")
    
                    if("3D" in str(type(MC_GEN_1D_initial))):
                        if(abs(MC_GEN_1D_initial.GetZaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                            MC_GEN_1D_initial = MC_GEN_1D_initial.Project3D("yx e")
                            MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" yx projection", ""))
                        else:
                            print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC GEN HISTO", color.END, "\nMC_GEN_1D_initial = ", MC_GEN_1D_initial)
                            raise TypeError("ERROR WITH Gen_MM_Cut MC GEN HISTO")
                    else:
                        if(abs(MC_GEN_1D_initial.GetYaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                            MC_GEN_1D_initial = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()), 0, -1, "e")
                            MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" x projection", ""))
                        else:
                            print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC GEN HISTO", color.END, "\nMC_GEN_1D_initial = ", MC_GEN_1D_initial)
                            raise TypeError("ERROR WITH Gen_MM_Cut MC GEN HISTO")
    
                    if(tdf not in ["N/A"]):
                        if("3D" in str(type(ExTRUE_1D_initial))):
                            if(abs(ExTRUE_1D_initial.GetZaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                                ExTRUE_1D_initial = ExTRUE_1D_initial.Project3D("yx e")
                                ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" yx projection", ""))
                            else:
                                print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC TRUE HISTO", color.END, "\nExTRUE_1D_initial = ", ExTRUE_1D_initial)
                                raise TypeError("ERROR WITH Gen_MM_Cut MC TRUE HISTO")
                        else:
                            if(abs(ExTRUE_1D_initial.GetYaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                                ExTRUE_1D_initial = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()), 0, -1, "e")
                                ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" x projection", ""))
                            else:
                                print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC TRUE HISTO", color.END, "\nExTRUE_1D_initial = ", ExTRUE_1D_initial)
                                raise TypeError("ERROR WITH Gen_MM_Cut MC TRUE HISTO")
    
                    if(MC_BGS_1D_initial != "None"):
                        if("3D" in str(type(MC_BGS_1D_initial))):
                            if(abs(MC_BGS_1D_initial.GetZaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                                MC_BGS_1D_initial = MC_BGS_1D_initial.Project3D("yx e")
                                MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" yx projection", ""))
                            else:
                                print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC BGS HISTO", color.END, "\nMC_BGS_1D_initial = ", MC_BGS_1D_initial)
                                raise TypeError("ERROR WITH Gen_MM_Cut MC BGS HISTO")
                        else:
                            if(abs(MC_BGS_1D_initial.GetYaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                                MC_BGS_1D_initial = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()), 0, -1, "e")
                                MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" x projection", ""))
                            else:
                                print(color.Error, "\n\nERROR WITH Gen_MM_Cut MC BGS HISTO", color.END, "\nMC_BGS_1D_initial = ", MC_BGS_1D_initial)
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
                    if(tdf not in ["N/A"]):
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
                            print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (Response_2D):\n", color.END_R, str(traceback.format_exc()), color.END]))
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
                            print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_REC_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
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
                                print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_BGS_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
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
                            print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_GEN_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
                    else:
                        # print("\nMC_GEN_1D already is a 1D Histogram...")
                        MC_GEN_1D = MC_GEN_1D_initial
    
                    if(tdf not in ["N/A"]):
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
                                print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (ExTRUE_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
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
                        print("\nADDING CUTS FOR:", out_print_main, "\n")
    
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
                                print("".join([color.RED, "ERROR IN SETTING BIT CONTENTS", color.END]))
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
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace("Cut: No Cuts", "")).replace("Cut:  No Cuts", ""))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
    
    
                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    ExREAL_1D.GetXaxis().SetTitle(str((str(ExREAL_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    MC_REC_1D.GetXaxis().SetTitle(str((str(MC_REC_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("_{t}",                 "_{h}")))
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
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
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
    
    
                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
    
    
                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))
    
    
                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
    
    
                    if("Var-D1='Q2" in out_print_main):
                        ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        if(tdf not in ["N/A"]):
                            ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                        Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                        Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV^{2}]"]))
    
    
                    if("Var-D1='pT" in out_print_main):
                        ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        if(tdf not in ["N/A"]):
                            ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV]"]))
                        Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV]"]))
                        Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV]"]))
    
    
                    for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                        ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace(range_strings,     ""))
                        MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace(range_strings,     ""))
                        MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace(range_strings,     ""))
                        if(tdf not in ["N/A"]):
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
    # print(f"Num Failed: {count_failed}")
    del count
    
    
    
    
    BIN_SEARCH = []
    for BIN in Q2_xB_Bin_List:
        BIN_SEARCH.append("".join(["Q2_y_Bin_", str(BIN) if(str(BIN) not in ['0', 0]) else "All", ")"]))
        
    for ii in rdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            # print("out_print_main =", out_print_main)
            # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
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
                # List_of_All_Histos_For_Unfolding[out_print_str.replace("mdf", "rdf")] = rdf.Get(out_print_main)
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
                            # sum_of_weights = List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")].Integral()
                            # if(sum_of_weights <= 0):
                            #     low_edge   = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinLowEdge(ii)
                            #     high_edge  = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinUpEdge(ii)
                            #     print(f"{color.Error}Projection of Y-bin {z_pT_bin_value} resulted in 'Sum of weights is null'. Check this bin's range ({low_edge} to {high_edge}) and content ({sum_of_weights}).{color.END}")
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                
    for ii in mdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if(("Normal_2D" in out_print_main) or ("Normal_Background_2D" in out_print_main)):
            # print("out_print_main =", out_print_main)
            # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
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
                            # print(f"out_print_str_1D_Binned = {out_print_str_1D_Binned}")
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            # sum_of_weights = List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")].Integral()
                            # if(sum_of_weights <= 0):
                            #     low_edge   = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinLowEdge(ii)
                            #     high_edge  = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinUpEdge(ii)
                            #     print(f"{color.Error}Projection of Y-bin {z_pT_bin_value} resulted in 'Sum of weights is null'. Check this bin's range ({low_edge} to {high_edge}) and content ({sum_of_weights}).{color.END}")
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                
    if(Cor_Compare):
        print(f"{color.Error}\nCorrection Comparison Plot Option selected does NOT include the Generated MC Plots{color.END_R} (as of 4-18-2024){color.END}\n")
    else:
        for ii in gdf.GetListOfKeys():
            out_print_main = str(ii.GetName())
            if("Normal_2D" in out_print_main):
                # print("out_print_main =", out_print_main)
                # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
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
                                # sum_of_weights = List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")].Integral()
                                # if(sum_of_weights <= 0):
                                #     low_edge   = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinLowEdge(ii)
                                #     high_edge  = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinUpEdge(ii)
                                #     print(f"{color.Error}Projection of Y-bin {z_pT_bin_value} resulted in 'Sum of weights is null'. Check this bin's range ({low_edge} to {high_edge}) and content ({sum_of_weights}).{color.END}")
                                if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                    List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                    List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
    
                
                
    if(tdf not in ["N/A"]):
        for ii in tdf.GetListOfKeys():
            out_print_main = str(ii.GetName())
            if("Normal_2D" in out_print_main):
                # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
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
                                # sum_of_weights = List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")].Integral()
                                # if(sum_of_weights <= 0):
                                #     low_edge   = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinLowEdge(ii)
                                #     high_edge  = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetYaxis().GetBinUpEdge(ii)
                                #     print(f"{color.Error}Projection of Y-bin {z_pT_bin_value} resulted in 'Sum of weights is null'. Check this bin's range ({low_edge} to {high_edge}) and content ({sum_of_weights}).{color.END}")
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
    #             if("Normal_2D" in out_print_main):
                    mdf_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
                    mdf_print_str     = mdf_print_str.replace("_(cut_Complete_SIDIS)",           "")
                    mdf_print_str     = mdf_print_str.replace("cut_Complete_SIDIS_",             "")
                    mdf_print_str     = mdf_print_str.replace("(gdf)_(no_cut)",                  "(gdf)")
                    mdf_print_str     = mdf_print_str.replace("_smeared",                        "")
                    mdf_print_str     = mdf_print_str.replace("'smear'",                         "Smear")
                    rdf_print_str     = str(mdf_print_str.replace("mdf", "rdf")).replace("Smear", "''")
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
                
                
    # Creating set of relative background plots
    temp_list_of_background_histos = {}
    for Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
        Conditions_List = [False]
        if("_(Background" in str(Histos_For_Unfolding_ii)):
            Conditions_List = [str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf") in List_of_All_Histos_For_Unfolding]
            # Conditions_List.append("1D" in str(type(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii])))
            # Conditions_List.append("1D" in str(type(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf")])))
        if("Normal_Background_2D" in str(Histos_For_Unfolding_ii)):
            Conditions_List = [str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D") in List_of_All_Histos_For_Unfolding]
        if(False not in Conditions_List):
            Relative_Background_Run_Q = True
            hist_temp = List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].Clone()
            hist_temp.SetName(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetName()).replace("'Background", "'Relative_Background"))
            hist_temp.SetTitle(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetTitle()).replace("BACKGROUND", "Relative Background"))
            if("_(Background" in str(Histos_For_Unfolding_ii)):
                hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf")])
            else:
                hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D")])
            if("1D"    in str(type(hist_temp))):
                hist_temp.GetYaxis().SetTitle("#frac{Background}{MC Reconstructed}")
            elif("2D" in str(type(hist_temp))):
                hist_temp.GetZaxis().SetTitle("#frac{Background}{MC Reconstructed}")
            if("_(Background" in str(Histos_For_Unfolding_ii)):
                temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("_(Background",         "_(Relative_Background")]         = hist_temp
            else:
                temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_Relative_Background_2D")] = hist_temp
    for adding_hist in temp_list_of_background_histos:
        if(adding_hist not in List_of_All_Histos_For_Unfolding):
            List_of_All_Histos_For_Unfolding[adding_hist] = temp_list_of_background_histos[adding_hist]
        else:
            print(f"{color.Error}ERROR:{color.END_R} adding_hist = {adding_hist}{color.Error} is already in 'List_of_All_Histos_For_Unfolding'{color.END}")
    del temp_list_of_background_histos
    
final_count = 0

if(not Relative_Background_Run_Q):
    # Creating set of relative background plots
    temp_list_of_background_histos = {}
    for Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
        Conditions_List = [False]
        if("_(Background" in str(Histos_For_Unfolding_ii)):
            Conditions_List = [str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf") in List_of_All_Histos_For_Unfolding]
            # Conditions_List.append("1D" in str(type(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii])))
            # Conditions_List.append("1D" in str(type(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf")])))
        if("Normal_Background_2D" in str(Histos_For_Unfolding_ii)):
            Conditions_List = [str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D") in List_of_All_Histos_For_Unfolding]
        if(False not in Conditions_List):
            hist_temp = List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].Clone()
            hist_temp.SetName(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetName()).replace("'Background", "'Relative_Background"))
            hist_temp.SetTitle(str(List_of_All_Histos_For_Unfolding[Histos_For_Unfolding_ii].GetTitle()).replace("BACKGROUND", "Relative Background"))
            if("_(Background" in str(Histos_For_Unfolding_ii)):
                hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("_(Background", "_(mdf")])
            else:
                hist_temp.Divide(List_of_All_Histos_For_Unfolding[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_2D")])
            if("1D"    in str(type(hist_temp))):
                hist_temp.GetYaxis().SetTitle("#frac{Background}{MC Reconstructed}")
            elif("2D" in str(type(hist_temp))):
                hist_temp.GetZaxis().SetTitle("#frac{Background}{MC Reconstructed}")
            if("_(Background" in str(Histos_For_Unfolding_ii)):
                temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("_(Background",         "_(Relative_Background")]         = hist_temp
            else:
                temp_list_of_background_histos[str(Histos_For_Unfolding_ii).replace("Normal_Background_2D", "Normal_Relative_Background_2D")] = hist_temp
    for adding_hist in temp_list_of_background_histos:
        if(adding_hist not in List_of_All_Histos_For_Unfolding):
            List_of_All_Histos_For_Unfolding[adding_hist] = temp_list_of_background_histos[adding_hist]
        else:
            print(f"{color.Error}ERROR:{color.END_R} adding_hist = {adding_hist}{color.Error} is already in 'List_of_All_Histos_For_Unfolding'{color.END}")
    del temp_list_of_background_histos


if((Fit_Test and Use_TTree) or Apply_RC):
    fits_included = False
    if(Fit_Test):
        for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
            if("(Fit_Par" in str(List_of_All_Histos_For_Unfolding_ii)):
                # print(f"\n{List_of_All_Histos_For_Unfolding_ii}")
                fits_included = True
                break
    print(f"{color.BLUE}Normal Unfolding Fits Already Included? -> {color.BGREEN if(fits_included) else color.Error}{fits_included}{color.END}")
    
    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code'
    sys.path.append(script_dir)
    from Find_RC_Fit_Params import Find_RC_Fit_Params, Apply_RC_Factor_Corrections, Get_RC_Fit_Plot
    sys.path.remove(script_dir)
    del script_dir
    print(f"\n{color.BOLD}Loaded `{color.GREEN}Find_RC_Fit_Params{color.END_B}` and `{color.GREEN}Apply_RC_Factor_Corrections{color.END_B}` for applying RC Corrections...{color.END}\n")
    # print(Find_RC_Fit_Params(Q2_y_bin=1, z_pT_bin=1, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=not True))
    Histogram_Fit_List_All = {}
    fit_count = 0
    for ii, List_of_All_Histos_For_Unfolding_ii in enumerate(List_of_All_Histos_For_Unfolding):
        if(any(Fit_objects in str(List_of_All_Histos_For_Unfolding_ii) for Fit_objects in ["Fit_Function", "Chi_Squared", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C"])):
            continue
        if("Bin_All)"  in str(List_of_All_Histos_For_Unfolding_ii)):
            continue
        if("_EvGen"    in str(List_of_All_Histos_For_Unfolding_ii)):
            continue
        if(("Acceptance" in str(List_of_All_Histos_For_Unfolding_ii)) and ("_EvGen" not in str(List_of_All_Histos_For_Unfolding_ii))):
            Histo_clasdis        = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
            Histo_Name_EvGen     = f"{Histo_clasdis.GetName()}_EvGen"
            Histo_Name_EvGen     = Histo_Name_EvGen.replace("Smear", "''")
            if(Histo_Name_EvGen not in List_of_All_Histos_For_Unfolding):
                if(Histo_Name_EvGen.replace("V1", "V2") in List_of_All_Histos_For_Unfolding):
                    Histo_Name_EvGen = Histo_Name_EvGen.replace("V1", "V2")
                    print(f"{color.Error}Warning:{color.END} Needed to switch to 'V2' to use '{Histo_Name_EvGen}'\n")
                else:
                    print(f"{color.Error}Could not find EvGen Acceptance ({Histo_Name_EvGen}){color.END}")
                    continue
            match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_EvGen))
            if(match):
                Q2_Y_Bin_Fitting = int(match.group(1))
                Z_PT_Bin_Fitting = int(match.group(2))
            else:
                print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                continue
            if(str(Q2_Y_Bin_Fitting) not in Q2_xB_Bin_List):
                continue
            Histo_Name_ratio     = str(Histo_clasdis.GetName()).replace("(Acceptance)", "(Acceptance_ratio)")
            Hist_AcceptanceRatio = List_of_All_Histos_For_Unfolding[Histo_Name_EvGen].Clone(Histo_Name_ratio)
            Hist_AcceptanceRatio.Divide(Histo_clasdis)
            Hist_AcceptanceRatio.SetTitle(Hist_AcceptanceRatio.GetTitle().replace("Bin-by-Bin Acceptance", "Ratio of #frac{EvGen}{clasdis} Acceptances"))
            Hist_AcceptanceRatio.GetYaxis().SetTitle("#frac{EvGen}{clasdis} Acceptance Ratio")
            Hist_AcceptanceRatio.SetLineColor(ROOT.kAzure + 3)
            Hist_AcceptanceRatio.SetLineWidth(2)
            Hist_AcceptanceRatio.SetLineStyle(1)
            Histogram_Fit_List_All[Histo_Name_ratio] = Hist_AcceptanceRatio
            fit_count += 1
        if(("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) or ("(Bin)" in str(List_of_All_Histos_For_Unfolding_ii))):
            Histo_Original       = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
            Histo_Name_General   = Histo_Original.GetName()
            match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_General))
            if(match):
                Q2_Y_Bin_Fitting = int(match.group(1))
                Z_PT_Bin_Fitting = int(match.group(2))
            else:
                print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                continue
            if(str(Q2_Y_Bin_Fitting) not in Q2_xB_Bin_List):
                # print(f"\n{color.RED}Not Using Histograms from Q2-y Bin {color.UNDERLINE}{Q2_Y_Bin_Fitting}{color.END}")
                continue
            Dimensions_Original = "1D" if("1D" in Histo_Name_General) else "MultiDim_3D_Histo" if("MultiDim_3D_Histo" in Histo_Name_General) else "MultiDim_5D_Histo" if("MultiDim_5D_Histo" in Histo_Name_General) else "Error"
            if(Dimensions_Original == "Error"):
                print(f"\n{color.Error}Error: Could not find unfolding dimensions for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                continue
            print(f"\nFitting for: {color.BOLD}{List_of_All_Histos_For_Unfolding_ii}{color.END} (Histo Num {ii:>5.0f})")
            Histo_Name_Rad_Cor          = str(Histo_Name_General.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
            RC_RooUnfolded_TTree_Histos = Histo_Original.Clone(Histo_Name_Rad_Cor)
            if(TTree_Name in ["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_No_Acceptance_Cut.root"]):
                RC_RooUnfolded_TTree_Histos.Rebin(2)
            if((not fits_included) and Fit_Test):
                RooUnfolded_TTree_Histos, Unfolded_TTree_Fit_Function, Chi_Squared_TTree, TTree_Fit_Par_A, TTree_Fit_Par_B, TTree_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Histo_Original, Method="Bayesian" if("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) else "Bin", Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting])
                Histogram_Fit_List_All[str(Histo_Name_General)]                                                = RooUnfolded_TTree_Histos.Clone(str(Histo_Name_General))
                Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Function")]   = Unfolded_TTree_Fit_Function.Clone(str(Histo_Name_General).replace(Dimensions_Original, "Fit_Function"))
                Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Chi_Squared")]    = Chi_Squared_TTree
                Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_A")]      = TTree_Fit_Par_A
                Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_B")]      = TTree_Fit_Par_B
                Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_C")]      = TTree_Fit_Par_C
                fit_count += 1

            RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=Q2_Y_Bin_Fitting, z_pT_bin=Z_PT_Bin_Fitting, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
            RC_RooUnfolded_TTree_Histos = Apply_RC_Factor_Corrections(hist=RC_RooUnfolded_TTree_Histos, Par_A=RC_Par_A, Par_B=RC_Par_B, Par_C=RC_Par_C, use_param_errors=True, Par_A_err=RC_Err_A, Par_B_err=RC_Err_B, Par_C_err=RC_Err_C, param_cov=None)
            RC_RooUnfolded_TTree_Histos, RC_Unfolded_TTree_Fit_Function, RC_Chi_Squared_TTree, RC_TTree_Fit_Par_A, RC_TTree_Fit_Par_B, RC_TTree_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RC_RooUnfolded_TTree_Histos, Method="RC_Bayesian" if("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) else "RC_Bin", Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting], Overwrite_Fit_Test=True)
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor)]                                                = RC_RooUnfolded_TTree_Histos.Clone(str(Histo_Name_Rad_Cor))
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Function")]   = RC_Unfolded_TTree_Fit_Function.Clone(str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Function"))
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Chi_Squared")]    = RC_Chi_Squared_TTree
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_A")]      = RC_TTree_Fit_Par_A
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_B")]      = RC_TTree_Fit_Par_B
            Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_C")]      = RC_TTree_Fit_Par_C
            fit_count += 1
            
            if(("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) and ("1D" in Histo_Name_General)):
                print(f"\n{color.BBLUE}Grabbing the RC vs phi_h plot for {color.END_B}Bin {Q2_Y_Bin_Fitting}-{Z_PT_Bin_Fitting}{color.BLUE}...{color.END}\n")
                RC_Factor_Plot = Get_RC_Fit_Plot(Q2_y_bin=Q2_Y_Bin_Fitting, z_pT_bin=Z_PT_Bin_Fitting, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", quiet=True, plot_choice="RC_factor")
                RC_Factor_Plot, RC_Factor_Plot_Fit_Function, RC_Factor_Chi_Squared_Plot, RC_Factor_Fit_Par_A, RC_Factor_Fit_Par_B, RC_Factor_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RC_Factor_Plot, Method="RC", Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting], Overwrite_Fit_Test=True)
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC"))]                                                = RC_Factor_Plot.Clone(str(Histo_Name_General).replace("Bayesian", "RC"))
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Function")]   = RC_Factor_Plot_Fit_Function.Clone(str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Function"))
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Chi_Squared")]    = RC_Factor_Chi_Squared_Plot
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_A")]      = RC_Factor_Fit_Par_A
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_B")]      = RC_Factor_Fit_Par_B
                Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_C")]      = RC_Factor_Fit_Par_C
                fit_count += 1
            
    print(f"\n{color.BBLUE}Fit/Added {color.END_B}{fit_count}{color.BBLUE} Histograms{color.END_b}\nAdding to Main List...{color.END}")

    for name_ii in Histogram_Fit_List_All:
        List_of_All_Histos_For_Unfolding[name_ii] = Histogram_Fit_List_All[name_ii]
        
    print(f"\n{color.BGREEN}Length of Main List of Histograms (After adding Fits): {color.END_B}{len(List_of_All_Histos_For_Unfolding)}{color.END}\n")

    timer.time_elapsed()


#Search comment find
print("\n\nCounting Total Number of collected histograms...")
for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
    final_count += 1
    # if(("Fit_Par" in str(List_of_All_Histos_For_Unfolding_ii)) and not any(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["(RC", "(Bin)", "(phi_t)"])):
    #     print(f"\n{List_of_All_Histos_For_Unfolding_ii} --> {type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
    # if("RC" in str(List_of_All_Histos_For_Unfolding_ii)):
    #     print(f"\n{List_of_All_Histos_For_Unfolding_ii}")
    # print("\n", str(List_of_All_Histos_For_Unfolding_ii))
    # if(any(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["(Q2)_(y)", "(Q2)_(xB)", "(z)_(pT)"])):
    #     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
    # if(all(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["(1D)_(", ")_(SMEAR=", "z_pT_Bin_Integrate"])):
    #     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
    # if(all(search not in str(List_of_All_Histos_For_Unfolding_ii) for search in ["elPhi", "elth", "pipPhi", "pipth", "(el)", "(pip)", "Background", "Acceptance", "Response_Matrix"])):
    #     # if(any(sec in str(List_of_All_Histos_For_Unfolding_ii) for sec in ["esec", "pipsec"])):
    #     if(any(sec in str(List_of_All_Histos_For_Unfolding_ii) for sec in ["_eS1o"])):
    #         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Multi_Dim_z_pT_Bin_Y_bin_phi_t" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if(("Background" in str(List_of_All_Histos_For_Unfolding_ii)) and ("MultiDim_Q2_y_z_pT_phi_h" not in str(List_of_All_Histos_For_Unfolding_ii))):
# #         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#         print(color.BLUE, "\n", str(List_of_All_Histos_For_Unfolding_ii), color.END)
#         print(f"\t{List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]}")

    # if(all(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["Acceptance", "(1D)", "(z_pT_Bin_1)"])):
    #     print(f"\n{List_of_All_Histos_For_Unfolding_ii}")

    # if("Acceptance" in str(List_of_All_Histos_For_Unfolding_ii)):
    #     print(f"\n{List_of_All_Histos_For_Unfolding_ii}")
    # if(any(search in str(List_of_All_Histos_For_Unfolding_ii) for search in ["Acceptance", "Response_Matrix"]) and ("Background" not in str(List_of_All_Histos_For_Unfolding_ii))):
    #     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("MultiDim_Q2_y_z_pT_phi_h" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print(color.BOLD, "\n", str(List_of_All_Histos_For_Unfolding_ii), color.END)
#     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("phi_h" in List_of_All_Histos_For_Unfolding_ii and isinstance(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii], ROOT.TH1D)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("(1D)" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("elPhi" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Background" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("MultiDim_3D_Histo" in str(List_of_All_Histos_For_Unfolding_ii)):
#         if("MultiDim_z_pT_Bin_Y_bin_phi_t" in str(List_of_All_Histos_For_Unfolding_ii)):
#             print(color.BLUE, "\n", str(List_of_All_Histos_For_Unfolding_ii), color.END)
#             print(f"\t{List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]}")
#     if("Multi_Dim" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
    # if("(MultiDim_3D_Histo)_(rdf)_(" in str(List_of_All_Histos_For_Unfolding_ii)):
    #     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
    # if("sec" in str(List_of_All_Histos_For_Unfolding_ii)):
    #     if("(1D)_(Bin)_" in str(List_of_All_Histos_For_Unfolding_ii)):
    #         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if(("tdf" not in str(List_of_All_Histos_For_Unfolding_ii)) and ("Fit" not in str(List_of_All_Histos_For_Unfolding_ii))):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if(("1D)_(mdf" in str(List_of_All_Histos_For_Unfolding_ii)) or ("1D)_(Background" in str(List_of_All_Histos_For_Unfolding_ii)) or ("1D)_(Relative_Background" in str(List_of_All_Histos_For_Unfolding_ii))):
#         print(color.BLUE, "\n", str(List_of_All_Histos_For_Unfolding_ii), color.END)
#         print(f"\t{type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
#     if((")_(mdf" in str(List_of_All_Histos_For_Unfolding_ii)) or (")_(Background" in str(List_of_All_Histos_For_Unfolding_ii)) or (")_(Relative_Background" in str(List_of_All_Histos_For_Unfolding_ii))):
#         print(color.BLUE, "\n", str(List_of_All_Histos_For_Unfolding_ii), color.END)
#         print(f"\t{type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
#     if("Proton" in  str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
# print("\n\n\nList_of_All_Histos_For_Unfolding =\n", List_of_All_Histos_For_Unfolding)
print(f"\nFinal Count = {final_count}")
# del final_count


if((Fit_Test and Saving_Q) and (all(str(bin_in) in Q2_xB_Bin_List for bin_in in range(1, 17)) or False) and True):
    import json
    print(f"\n{color.BBLUE}Will be saving the Modulations now (for iterative modulations){color.END}\n")
    Cor_Type  = "Bayesian"
    # Var_Type  = "phi_t"                         # --> 1D Unfolding
    Var_Type  = "MultiDim_z_pT_Bin_Y_bin_phi_t" # --> 3D Unfolding
    JSON_Name = f"Fit_Pars_from_{'3D' if(Var_Type == 'MultiDim_z_pT_Bin_Y_bin_phi_t') else '1D'}_{Cor_Type}.json"
    if("_with_kCovToy" in TTree_Name):
        JSON_Name = JSON_Name.replace(f"{Cor_Type}.json", f"{Cor_Type}_with_Toys.json")
    if(Sim_Test):
        JSON_Name = f"Sim_Test_{JSON_Name}"
    if(Mod_Test):
        JSON_Name = f"Mod_Test_{JSON_Name}"
    Fit_Pars_JSON = {}
    for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
        if(all(search in str(List_of_All_Histos_For_Unfolding_ii) for search in [f"({Cor_Type})", f"({Var_Type})", "Fit_Par"])):
            par, method, smear_line, q2_y_bin, z_pt_bin, var = List_of_All_Histos_For_Unfolding_ii.split(")_(")
            par = par.replace("(Fit_Par_", "")
            var = var.replace(")", "")
            if("A" in par):
                continue
            if("=Smear" not in smear_line):
                print(f"{color.RED}Missing Smearing{color.END}")
                continue
            if(Cor_Type not in method):
                print(f"{color.RED}Wrong Correction Method{color.END}")
                continue
            if(Var_Type not in var):
                print(f"{color.RED}Wrong variable for unfolding{color.END}")
                continue
            q2_y_bin = q2_y_bin.replace("Q2_y_Bin_", "")
            z_pt_bin = z_pt_bin.replace("z_pT_Bin_", "")
            val, err = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
            Fit_Pars_JSON[f"{par}_{q2_y_bin}_{z_pt_bin}"] = val
    #         print(f"\n{List_of_All_Histos_For_Unfolding_ii} --> {val} (±{err})")
    # print(f"\n{color.BOLD}Looking at 'Fit_Pars_JSON' (len = {len(Fit_Pars_JSON)}){color.END}\n")
    # for ii in Fit_Pars_JSON:
    #     print(f"Fit_Pars_JSON[{ii}] = {Fit_Pars_JSON[ii]}")
    print(f"\n{color.BGREEN}Saving {color.END_B}{JSON_Name}{color.BGREEN}...{color.END}\n")
    with open(JSON_Name, "w") as f:
        json.dump(Fit_Pars_JSON, f, indent=4)
    print(f"\n{color.BCYAN}Done Saving JSON File.{color.END}\n")
    timer.time_elapsed()
    
# stop

Smearing_final_list = ["''", "Smear"]
if(Smearing_Options not in ["no_smear", "both"]):
    Smearing_final_list = ["Smear"]
elif(Smearing_Options in ["no_smear"]):
    Smearing_final_list = ["''"]
elif(Smearing_Options in ["both"]):
    Smearing_final_list = ["''", "Smear"]
    

#Search comment find

# Method_Type_List = ["Data", "Response", "Bin", "RooUnfold_bayes", "RooUnfold_svd", "rdf", "mdf", "gdf"]
# Method_Type_List = ["Data", "Kinematic_Comparison", "Response", "Bin", "Bayesian", "SVD", "Unfold", "rdf", "mdf", "gdf", "Acceptance"]
# Method_Type_List = ["Data", "Kinematic_Comparison", "Response", "Bin", "Bayesian", "Unfold", "rdf", "mdf", "gdf", "Acceptance"]
# Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "Unfold", "rdf", "mdf", "gdf", "Acceptance"]
# Method_Type_List = ["Data", "Response", "Bin",             "Unfold", "rdf", "mdf", "gdf", "Acceptance"]
# Method_Type_List = ["Data", "Response", "Bin",                       "rdf", "mdf", "gdf", "Acceptance"]
# Method_Type_List = ["mdf", "Background", "Relative_Background"]
Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "Unfold", "rdf", "mdf", "gdf", "Acceptance", "Background", "Relative_Background"]
# Method_Type_List = ["Bin"]
# Method_Type_List = ["Data", "rdf", "mdf"]
# Method_Type_List = ["rdf"]

Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "Unfold", "rdf", "mdf", "gdf", "Acceptance", "Background"]

    
if("''" not in Smearing_final_list):
    for method in Method_Type_List:
        if(method in ["rdf", "gdf"]):
            if((method in ["gdf"]) or (not Sim_Test)):
                Method_Type_List.remove(method)
    
    
# Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD", "Unfold"]
# Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD"]
# Method_Type_List = ["Unfold"]
# Method_Type_List = ["Data", "Unfold"]
# Method_Type_List = ["Data"]
# Method_Type_List = ["Bin"]
# Method_Type_List = ["Data", "Bayesian", "Bin", "Acceptance"]
# Method_Type_List = ["Bayesian", "Bin", "Acceptance"]
# Method_Type_List = ["Bayesian"]
# Method_Type_List = ["Background", "mdf"]
# Method_Type_List = ["Data", "rdf", "mdf"]
# Method_Type_List = ["Data", "Bin", "Bayesian", "Unfold", "rdf", "mdf", "gdf"]
# Method_Type_List = ["Data", "Bayesian", "Unfold"]

# Method_Type_List = ["Data", "Bin", "Bayesian", "rdf", "mdf", "gdf"]
# Method_Type_List = ["Data", "Bin", "Bayesian", "Unfold", "mdf"]
# Method_Type_List = ["Data", "Bin", "Bayesian", "Unfold", "mdf", "Acceptance"]
Method_Type_List = ["Data", "Bin", "Bayesian", "Unfold"]
Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "Unfold"]

if((tdf not in ["N/A"]) or Sim_Test):
    Method_Type_List.append("tdf")

if(Apply_RC):
    # Method_Type_List = []
    Method_Type_List.append("RC")
    # Method_Type_List.remove("Bin")
    # Method_Type_List.append("RC_Bin")
    Method_Type_List.append("RC_Bayesian")
# Method_Type_List = []
# Method_Type_List.append("Bayesian")
# Method_Type_List.append("RC_Bayesian")
# Method_Type_List.append("Acceptance")
# if(Use_TTree):
#     Method_Type_List.append("Acceptance_ratio")


# Method_Type_List = ["mdf", "Background", "Relative_Background"]
# Method_Type_List = ["RC"]


# Method_Type_List = ["Data", "Bin", "rdf", "mdf", "gdf", "Acceptance"]

# All phi_t related plots (including multidimensional plots) are controlled by variable = 'phi_t'
Variable_List = ["phi_t", "MM"]
# Variable_List = ["MM"]
Variable_List = ["phi_t"]
# Variable_List = ["el", "elth", "elPhi", "pip", "pipth", "pipPhi"]
# Variable_List = ["phi_t", "el", "elth", "elPhi", "pip", "pipth", "pipPhi"]

# Variable_List = ["pipsec_1)_(phi_t"]

if(run_Sec_Unfold):
    # Variable_List = []
    for sec in Sector_List:
        # Variable_List.append(f"pipsec_{sec})_(phi_t")
        Variable_List.append(f"esec_{sec})_(phi_t")


# Cut_Options_List = ["Cut", "UnCut"]
# Cut_Options_List = ["Cut", "Proton"]
Cut_Options_List = ["Cut"]
# Cut_Options_List = ["Integrate"]
# Cut_Options_List = ["Cut", "Integrate"]

if(Cut_ProQ):
    # Cut_Options_List = ["Proton"]
    Cut_Options_List = ["Proton_Integrate"]
# 'Cut'              --> Normal Cuts (Default)
# 'Proton'           --> Normal Cuts + Proton Missing Mass Cuts
# 'Proton_Integrate' --> Normal Cuts + Proton Missing Mass Cuts + Only the bins compatible with z-pT bin integration

if(run_SecCut_Unfold):
    for sec in Sector_List:
        if(Cut_ProQ):
            Cut_Options_List.append(f"Proton_Integrate_eS{sec}o")
        else:
            Cut_Options_List.append(f"Integrate_eS{sec}o")

Orientation_Option_List = ["pT_z", "z_pT"]
# Orientation_Option_List = ["pT_z"] # Flipped
Orientation_Option_List = ["z_pT"]


# Variable_List_Final = ["phi_t", "Multi_Dim_z_pT_Bin_y_bin_phi_t" if("y" in Binning_Method) else "Multi_Dim_z_pT_Bin_Y_bin_phi_t"]
# Variable_List_Final = ["phi_t"]
# Variable_List_Final = []
# Variable_List_Final = ["Multi_Dim_z_pT_Bin_y_bin_phi_t" if("y" in Binning_Method) else "Multi_Dim_z_pT_Bin_Y_bin_phi_t"]
Variable_List_Final = ["phi_t", "Multi_Dim_z_pT_Bin_Y_bin_phi_t", "MultiDim_z_pT_Bin_Y_bin_phi_t", "MultiDim_Q2_y_z_pT_phi_h"]
# Variable_List_Final = ["Multi_Dim_z_pT_Bin_Y_bin_phi_t", "MultiDim_Q2_y_z_pT_phi_h"]
# Variable_List_Final = ["MultiDim_z_pT_Bin_Y_bin_phi_t"]

Variable_List_Final = ["phi_t", "MultiDim_z_pT_Bin_Y_bin_phi_t", "MultiDim_Q2_y_z_pT_phi_h"]

Variable_List_Final = ["MultiDim_z_pT_Bin_Y_bin_phi_t"]
# Variable_List_Final = ["phi_t"]
# Variable_List_Final = ["phi_t", "MM"]

Variable_List_Final = ["phi_t", "MultiDim_z_pT_Bin_Y_bin_phi_t"]

if(run_Sec_Unfold):
    # Variable_List_Final = []
    for sec in Sector_List:
        # Variable_List_Final.append(f"pipsec_{sec})_(phi_t")
        Variable_List_Final.append(f"esec_{sec})_(phi_t")
# Variable_List_Final = ["pipsec_1)_(phi_t"]

if(Cor_Compare):
    Method_Type_List    = ["rdf", "mdf"]
    Method_Type_List    = ["rdf"]
    Variable_List       = ["Complete_Correction_Factor_Ele"]
    Variable_List_Final = []

Run_Individual_Bin_Images_Option = True
Print_Run_Individual_Bin_Option  = True

if((not Fit_Test) and Run_Individual_Bin_Images_Option):
    print(f"\n\n{color.ERROR}WARNING FOR (POTENTIAL) SEGMENTATION FAULT:\n\t{color.END_R}An error was observed when running individual bin images without fitting. I don't know why this error exists now, but the code will now default to setting `Run_Individual_Bin_Images_Option = False` unless you run again with `Fit_Test = True`.{color.END}\n\n")
    Run_Individual_Bin_Images_Option = False

# Multi_Dimensional_List = ["Off", "Only", "Q2_y", "z_pT"]
# Multi_Dimensional_List = ["Off", "Only"]
# Multi_Dimensional_List = ["Off"]
Multi_Dimensional_List = ["Only"]
# Multi_Dimensional_List = ["5D"]
Multi_Dimensional_List = ["Off", "Only", "5D"]
Multi_Dimensional_List = ["Off", "Only", "3D", "5D"]
# Multi_Dimensional_List = ["Off",         "5D"]
# Multi_Dimensional_List = ["Only", "3D"]
# Multi_Dimensional_List = ["3D"]
Multi_Dimensional_List = ["Off", "3D", "5D"]

Multi_Dimensional_List = ["Off"]
Multi_Dimensional_List = ["Off", "3D"]
# # if(not (Tag_ProQ or Cut_ProQ)):
# Multi_Dimensional_List = ["3D"]

if((not run_5D_Unfold) and ("5D"       in Multi_Dimensional_List)):
    Multi_Dimensional_List.remove("5D")
if(("phi_t"                            in Variable_List_Final) and ("Off"  not in Multi_Dimensional_List)):
    Variable_List_Final.remove("phi_t")
if((not run_Sec_Unfold) or ("Off"  not in Multi_Dimensional_List)):
    removing_list = []
    for ii in Variable_List_Final:
        if("sec" in ii):
            removing_list.append(ii)
    if(len(removing_list) != len([])):
        for ii in removing_list:
            Variable_List_Final.remove(ii)
    del removing_list
if(("Multi_Dim_z_pT_Bin_Y_bin_phi_t" in Variable_List_Final) and ("Only" not in Multi_Dimensional_List)):
    Variable_List_Final.remove("Multi_Dim_z_pT_Bin_Y_bin_phi_t")
if(("MultiDim_Q2_y_z_pT_phi_h"       in Variable_List_Final) and ("5D"   not in Multi_Dimensional_List)):
    Variable_List_Final.remove("MultiDim_Q2_y_z_pT_phi_h")
if(("MultiDim_z_pT_Bin_Y_bin_phi_t"  in Variable_List_Final) and ("3D"   not in Multi_Dimensional_List)):
    Variable_List_Final.remove("MultiDim_z_pT_Bin_Y_bin_phi_t")


print(f"\n{color.BOLD}About to run 'Integrate_z_pT_Bins(...)' to get the Integrated z-pT bin plots...{color.END}")
for variable in Variable_List:
    # if((variable not in ["phi_t", "MM"]) or ("sec" in variable)):
    #     continue
    for BIN in Q2_xB_Bin_List:
        BIN_NUM        = int(BIN) if(str(BIN) not in ["0"]) else "All"
        for smear in Smearing_final_list:
            for Cut in Cut_Options_List:
                # if(Cut in ["Proton", "Proton_Integrate"]):
                if(Cut not in ["", "Cut"]):
                    HISTO_NAME = f"(1D)_(Data_Type)_({Cut})_(SMEAR={str(smear)})_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_({str(variable)})"
                else:
                    HISTO_NAME = "".join(["(1D)_(Data_Type)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_All)_(", str(variable), ")"])
                for Multi_Dim in Multi_Dimensional_List:
                    # if((Multi_Dim not in ["Off"]) and ((variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi"]) or ("sec" in variable))):
                    if((Multi_Dim not in ["Off"]) and ((variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi"]))):
                        continue
                    if((BIN_NUM not in ["All"]) and (Multi_Dim in ["Off", "Only", "3D", "5D"])):
                        for method in Method_Type_List:
                            if((method in ["RooUnfold_svd", "SVD", "Response", "Relative_Background", "RC"]) and (Multi_Dim not in ["Off"])):
                                if((method == "RC") and ("Off" not in Multi_Dimensional_List)):
                                    Multi_Dim = "Off"
                                else:
                                    continue
                            if((method in ["Bayesian", "Unfold"])                                      and (Multi_Dim     in ["5D"])):
                                # Temporary restriction on 5D unfolding as method is being tested for computational requirements (copy this line to see other restriction)
                                continue
                            if((method in ["gdf", "tdf"]) and (("Smear" in str(smear)) or (Cut in ["Proton"]))):
                                continue
                            # if((method in ["gdf", "rdf", "Response", "Kinematic_Comparison", "Unfold", "Acceptance"]) or (variable not in ["phi_t", "MM"]) or ("sec" in variable)):
                            # if((method in ["gdf", "rdf", "Response", "Kinematic_Comparison", "Unfold", "Acceptance"])):
                            if((method in ["gdf", "rdf", "Response", "Kinematic_Comparison", "Unfold", "RC", "RC_Bin", "RC_Bayesian", "Acceptance_ratio"])):
                                continue
                            if(method in ["Data"]):
                                if(Sim_Test):
                                    List_of_All_Histos_For_Unfolding = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME,                                        VARIABLE=f"({variable})", Method="rdf",  Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                    List_of_All_Histos_For_Unfolding = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME,                                        VARIABLE=f"({variable})", Method="tdf",  Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                    final_count += 1
                                else:
                                    List_of_All_Histos_For_Unfolding = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME.replace(f"SMEAR={smear}", f"SMEAR=''"), VARIABLE=f"({variable})", Method="rdf",  Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                List_of_All_Histos_For_Unfolding     = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME.replace(f"SMEAR={smear}", f"SMEAR=''"), VARIABLE=f"({variable})", Method="gdf",  Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                final_count += 2
                                if("mdf" not in Method_Type_List):
                                    List_of_All_Histos_For_Unfolding = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME,                                        VARIABLE=f"({variable})", Method="mdf",  Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                    final_count += 1
                            else:
                                List_of_All_Histos_For_Unfolding     = Integrate_z_pT_Bins(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME,                                        VARIABLE=f"({variable})", Method=method, Q2_Y_Bin=BIN_NUM, Multi_Dim_Option=Multi_Dim)
                                final_count += 1

print(f"\n(Extra) Final Count = {final_count}\n")
del final_count

to_be_saved_count = 0


# Individual (Manual) Run(s) of specific histograms
if(not True): # Run from list
    print(f"{color.BOLD}Running Individual (Manual) Images using 'Draw_Histogram_With_Kinematic_Bins'...{color.END}")
    for method in Method_Type_List:
        if(method not in ["rdf", "mdf", "gdf", "Bin", "Bayesian", "Acceptance", "bbb", "RC_Bin", "RC_Bayesian"]):
            continue
        for BIN in Q2_xB_Bin_List:
            BIN_NUM        = int(BIN) if(str(BIN) not in ["0"]) else "All"
            HISTO_NAME     = f"(1D)_(Data_Type)_(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[1]
            for Cut in Cut_Options_List:
                if(Cut in ["Proton"]):
                    if(method in ["gdf", "tdf"]):
                        continue
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(SMEAR", "Data_Type)_(Proton)_(SMEAR"))
                elif(Cut in ["Proton_Integrate"]):
                    if(method in ["gdf", "tdf"]):
                        continue
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(SMEAR", "Data_Type)_(Proton_Integrate)_(SMEAR"))
                elif(Cut in ["Integrate"]):
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(SMEAR", "Data_Type)_(Integrate)_(SMEAR"))
                else:
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(Proton)_(SMEAR",           "Data_Type)_(SMEAR"))
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(Integrate)_(SMEAR",        "Data_Type)_(SMEAR"))
                    HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(Proton_Integrate)_(SMEAR", "Data_Type)_(SMEAR"))
                for smear in Smearing_final_list:
                    for variable in Variable_List:
                        for z_PT_BIN_NUM in z_pT_Bin_Range:
                            canvas_manual_from_list = Draw_Histogram_With_Kinematic_Bins(Histogram_List_All_Input=List_of_All_Histos_For_Unfolding, Default_Histo_Name_Input=HISTO_NAME, Data_Type=method, Smear=smear, Variable1=variable, Variable2="", Q2_Y_Bin_Input=BIN_NUM, Z_PT_Bin_Input=z_PT_BIN_NUM)
                            to_be_saved_count += 1
    print(f"\nCurrent Count to be saved = {to_be_saved_count}\n")

if(not True): # Run selected plot manually
    # Can control Q2_xB_Bin_List and Smearing_final_list from commandline
    print(f"{color.BOLD}Running Individual (Manual) Images using 'Draw_Histogram_With_Kinematic_Bins'...{color.END}")
    for BIN in Q2_xB_Bin_List:
        if(str(BIN) in ['0', 'All']):
            continue
        for smear in Smearing_final_list:
            # smear = "''" # Manual Override
            BIN_NUM   = int(BIN) if(str(BIN) not in ["0"]) else "All"
            # method    = "Bayesian"
            # method    = "rdf"
            # variable1 = "MM"
            # variable2 = ""
            # # variable2 = "esec"
            
            # z_PT_BIN_NUM = "Integrated"
            # z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[1]
            
            # if((str(z_PT_BIN_NUM) not in ["All", "Integrated", "0"]) and (int(z_PT_BIN_NUM) not in z_pT_Bin_Range)):
            #     print(f"{color.Error}z-pT bin = {z_PT_BIN_NUM} is a poor choice for Q2-y bin = {BIN_NUM}...{color.END}")
            #     break
                
            # HISTO_NAME    = f"(1D)_(Data_Type)_(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
            # canvas_manual = Draw_Histogram_With_Kinematic_Bins(Histogram_List_All_Input=List_of_All_Histos_For_Unfolding, Default_Histo_Name_Input=HISTO_NAME, Data_Type=method, Smear=smear, Variable1=variable1, Variable2=variable2, Q2_Y_Bin_Input=BIN_NUM, Z_PT_Bin_Input=z_PT_BIN_NUM)

            variable1 = "MultiDim_z_pT_Bin_Y_bin_phi_t" # if(not (Tag_ProQ or Cut_ProQ)) else "phi_t"
            variable1 = "phi_t"
            variable2 = ""
            z_pT_Bin_Range = range(-2, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[1] + 1, 1)
            # for Cut_Select in ["(Integrate)_", "(Integrate_eS1o)_", "(Integrate_eS2o)_", "(Integrate_eS3o)_", "(Integrate_eS4o)_", "(Integrate_eS5o)_", "(Integrate_eS6o)_"]:
            for Cut_Select in ["(Integrate)_"]:
                # method     = "Acceptance"
                method     = "mdf"
                if(not (Tag_ProQ or Cut_ProQ)):
                    HISTO_NAME = f"(MultiDim_3D_Histo)_(Data_Type)_{Cut_Select}(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
                else:
                    if(Cut_ProQ):
                        Cut_Select = Cut_Select.replace("(Integrate", "(Proton_Integrate")
                    # HISTO_NAME =                f"(1D)_(Data_Type)_{Cut_Select}(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
                    HISTO_NAME = f"(MultiDim_3D_Histo)_(Data_Type)_{Cut_Select}(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
                if("MultiDim" not in variable1):
                    HISTO_NAME = HISTO_NAME.replace("(MultiDim_3D_Histo)", "(1D)")
                if("_eS" in Cut_Select):
                    continue
                for z_PT_BIN_NUM in z_pT_Bin_Range:
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_PT_BIN_NUM, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                        continue
                    if(z_PT_BIN_NUM < 1):
                        z_PT_BIN_NUM = "All" if(z_PT_BIN_NUM == 0) else "Integrated" if(z_PT_BIN_NUM == -1) else "Common_Int" if(z_PT_BIN_NUM == -2) else z_PT_BIN_NUM
                    canvas_manual = Draw_Histogram_With_Kinematic_Bins(Histogram_List_All_Input=List_of_All_Histos_For_Unfolding, Default_Histo_Name_Input=HISTO_NAME, Data_Type=method, Smear=smear, Variable1=variable1, Variable2=variable2, Q2_Y_Bin_Input=BIN_NUM, Z_PT_Bin_Input=z_PT_BIN_NUM)
                    to_be_saved_count += 1
                # z_PT_BIN_NUM  = "All"
                # method        = "mdf"            
                # HISTO_NAME    = f"(Response_Matrix)_(Data_Type)_{Cut_Select}(SMEAR=SMEAR_OPTION)_(Q2_y_Bin_{str(BIN_NUM)})_(z_pT_Bin_All)_(VARIABLE)"
                # canvas_manual = Draw_Histogram_With_Kinematic_Bins(Histogram_List_All_Input=List_of_All_Histos_For_Unfolding, Default_Histo_Name_Input=HISTO_NAME, Data_Type=method, Smear=smear, Variable1=variable1, Variable2=variable2, Q2_Y_Bin_Input=BIN_NUM, Z_PT_Bin_Input=z_PT_BIN_NUM)
                # to_be_saved_count += 1
    print(f"\nCurrent Count to be saved = {to_be_saved_count}\n")




if(run_Sec_Unfold and True):
    print(f"{color.BOLD}Running Sector (Histo) Unfolded Images using 'Unfolded_Sector_Dependent_Images'...{color.END}")
    Variable_List = []
    for smear in Smearing_final_list:
        for Cut_Option in Cut_Options_List:
            for Q2_y_BIN in Q2_xB_Bin_List:
                Q2_y_BIN_NUM = int(Q2_y_BIN) if(str(Q2_y_BIN) not in ["0"]) else "All"
                # HISTO_NAME = f"(1D)_(Data_Type)_(SMEAR={smear})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_All)_(pipsec_SECTOR)_(phi_t)"
                HISTO_NAME = f"(1D)_(Data_Type)_(SMEAR={smear})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_All)_(esec_SECTOR)_(phi_t)"
                if(Cut_ProQ):
                    HISTO_NAME = f"(1D)_(Data_Type)_(Proton_Integrate)_(SMEAR={smear})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_All)_(esec_SECTOR)_(phi_t)"
                if(Cut_Option not in ["", "Cut"]):
                    HISTO_NAME = HISTO_NAME.replace("(Data_Type)_(SMEAR", f"(Data_Type)_({Cut_Option})_(SMEAR")
                z__pT__Range = range(-2, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_BIN_NUM)[1] + 1, 1)
                # z__pT__Range = [-1, 1]
                for z_pT_Bin in z__pT__Range:
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                        continue
                    if(z_pT_Bin in [0]):
                        print(f"{color.RED}Manual skip of z_pT_Bin = {z_pT_Bin} for Unfolded_Sector_Dependent_Images(...){color.END}")
                        continue
                    # print(f"""\n{color.BOLD}
                    # Inputs:
                    # HISTO_NAME    = {HISTO_NAME}
                    # Q2_Y_Bin      = {Q2_y_BIN_NUM}
                    # Z_PT_Bin      = {z_pT_Bin if(z_pT_Bin not in [-1, 0]) else "All" if(z_pT_Bin not in [0]) else "Integrated"}
                    # Sector_Ranges = {["All"]+Sector_List}
                    # {color.END}""")
                    try:
                        Unfolded_Sector_Dependent_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME,
                                                         Q2_Y_Bin=Q2_y_BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int",
                                                         Multi_Dim_Option="Off", Sector_Ranges=["All"]+Sector_List)
                        to_be_saved_count += 1
                    except:
                        print(f"""{color.Error}
                        Error in Unfolded_Sector_Dependent_Images(...) with Inputs:{color.END_B}
                        HISTO_NAME           = {HISTO_NAME}
                        (Q2_Y_Bin, Z_PT_Bin) = ({Q2_y_BIN_NUM}, {z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}){color.END}""")
                        print(f"""                        Traceback:\n{traceback.format_exc()}\n""")

if(run_SecCut_Unfold and True):
    print(f"{color.BOLD}Running Sector (Cut) Unfolded Images using 'Unfolded_Sector_Dependent_Images'...{color.END}")
    Variable_List = []
    for smear in Smearing_final_list:
        for variable in Variable_List_Final:
            for Q2_y_BIN in Q2_xB_Bin_List:
                Q2_y_BIN_NUM = int(Q2_y_BIN) if(str(Q2_y_BIN) not in ["0"]) else "All"
                if(Q2_y_BIN_NUM in ["0", "All"]):
                    continue
                HISTO_NAME = f"(1D)_(Data_Type)_(Integrate_eS_SECTORo)_(SMEAR={smear})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_All)_({variable})"
                if(Cut_ProQ):
                    HISTO_NAME = f"(1D)_(Data_Type)_(Proton_Integrate_eS_SECTORo)_(SMEAR={smear})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_All)_({variable})"
                # z__pT__Range = [-1, 0]
                # z__pT__Range = [0]
                z__pT__Range = range(-2, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_BIN_NUM)[1] + 1, 1)
                for z_pT_Bin in z__pT__Range:
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                        continue
                    if(z_pT_Bin in [0]):
                        print(f"{color.RED}Manual skip of z_pT_Bin = {z_pT_Bin} for Unfolded_Sector_Dependent_Images(...){color.END}")
                        continue
                    # print(f"""\n{color.BOLD}
                    # Inputs:
                    # HISTO_NAME    = {HISTO_NAME}
                    # Q2_Y_Bin      = {Q2_y_BIN_NUM}
                    # Z_PT_Bin      = {z_pT_Bin if(z_pT_Bin not in [-1, 0]) else "All" if(z_pT_Bin not in [0]) else "Integrated"}
                    # Sector_Ranges = {["All"]+Sector_List}
                    # {color.END}""")
                    try:
                        # Unfolded_Sector_Dependent_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME, 
                        #                                  Q2_Y_Bin=Q2_y_BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [-1, 0]) else "All" if(z_pT_Bin not in [0]) else "Integrated",
                        #                                  Multi_Dim_Option="3D" if(variable in ["MultiDim_z_pT_Bin_Y_bin_phi_t"]) else "Off",
                        #                                  Sector_Ranges=["All"]+Sector_List,
                        #                                  Cut_or_Hist="Cut")
                        Unfolded_Sector_Dependent_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME, 
                                                         Q2_Y_Bin=Q2_y_BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int",
                                                         Multi_Dim_Option="3D" if(variable in ["MultiDim_z_pT_Bin_Y_bin_phi_t"]) else "Off",
                                                         Sector_Ranges=["All"]+Sector_List,
                                                         Unfolding_Methods=["Bin", "Bayesian", "Acceptance"], Show_text=True,
                                                         Cut_or_Hist="Cut")
                        to_be_saved_count += 1
                    except:
                        print(f"""{color.Error}
                        Error in Unfolded_Sector_Dependent_Images(...) with Inputs:{color.END_B}
                        HISTO_NAME           = {HISTO_NAME}
                        (Q2_Y_Bin, Z_PT_Bin) = ({Q2_y_BIN_NUM}, {z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}){color.END}""")
                        print(f"""                        Traceback:\n{traceback.format_exc()}\n""")


Pars_Canvas, Histo_Pars_VS_Z, Histo_Pars_VS_PT, Pars_Legends = {}, {}, {}, {}
for variable in Variable_List:
    for BIN in Q2_xB_Bin_List:
        if(appended_0 and (str(BIN) in ["0"])):
            print(f"\n{color.BOLD}Skipping appended '0' Q2-y Bin{color.END}\n")
            continue
        BIN_NUM        = int(BIN) if(str(BIN) not in ["0"]) else "All"
        z_pT_Bin_Range = 42       if(str(BIN_NUM) in ["2"]) else  36 if(str(BIN_NUM) in ["4", "5", "9", "10"]) else 35 if(str(BIN_NUM) in ["1", "3"]) else 30 if(str(BIN_NUM) in ["6", "7", "8", "11"]) else 25 if(str(BIN_NUM) in ["13", "14"]) else 20 if(str(BIN_NUM) in ["12", "15", "16", "17"]) else 0
        if("Y_bin" in Binning_Method):
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[1]
        # z_pT_Bin_Range = 0
        # print(f"{color.Error}Setting z_pT_Bin_Range = 0 (just doing 'Integrated' and 'All' z-pT bins - must reset later){color.END}")
        for smear in Smearing_final_list:
            HISTO_NAME = f"(1D)_(Data_Type)_(SMEAR={smear})_(Q2_y_Bin_{BIN_NUM})_(z_pT_Bin_All)_({variable})"
            for Multi_Dim in Multi_Dimensional_List:
                if((Multi_Dim not in ["Off"]) and ((variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi"]) or ("sec" in variable))):
                    continue
                if((BIN_NUM not in ["All"]) and (Multi_Dim in ["Off", "Only", "3D", "5D"]) and ((str(variable) in ["phi_t", "el", "pip", "elth", "pipth", "elPhi", "pipPhi", "MM"]) or ("sec" in variable))):
                # if((BIN_NUM not in ["All"]) and (Multi_Dim in ["Off", "Only", "3D", "5D"]) and ((str(variable) in ["phi_t", "el", "pip", "elth", "pipth", "elPhi", "pipPhi", "MM"]) and  ("sec" not in variable))):
                    for method in Method_Type_List:
                        # if(True):
                        #     print(f"{color.Error}Skipping z_pT_Images_Together...{color.END}")
                        #     continue #Temporary skip
                        if((method in ["RooUnfold_svd", "SVD", "Response", "Relative_Background", "RC"]) and (Multi_Dim not in ["Off"])):
                            if((method == "RC") and ("Off" not in Multi_Dimensional_List)):
                                Multi_Dim = "Off"
                            else:
                                continue
                        if((method in ["Bayesian", "Unfold"])                                            and (Multi_Dim     in ["5D"])):
                            # Temporary restriction on 5D unfolding as method is being tested for computational requirements (copy this line to see other restriction)
                            continue
                        # if((method in ["rdf"]) and Sim_Test):
                        #     continue
                        if((method in ["gdf", "tdf"]) and ("Smear" in str(smear))):
                            continue
                        if((method not in ["Data", "rdf", "mdf", "gdf", "Kinematic_Comparison"])         and (variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi", "MM"])):
                            continue
                        if((method     in ["Response", "Bayesian", "Unfold", "RC"])                      and ("sec" in variable)):
                            continue
                        for Cut in Cut_Options_List:
                            if((Cut in ["UnCut"]) and (method not in ["rdf", "mdf", "Data"])):
                                # There is (currently) no point in running any other method with both the cut and uncut versions of this plot (this option only affects the 2D histograms and not the unfolded histograms - gdf and tdf are also already uncut by default)
                                continue
                            if(Cut in ["Proton"]):
                                if(method in ["gdf", "tdf"]):
                                    continue
                                HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(SMEAR", "Data_Type)_(Proton)_(SMEAR"))
                            elif(Cut in ["Proton_Integrate"]):
                                if(method in ["gdf", "tdf"]):
                                    continue
                                HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(SMEAR", "Data_Type)_(Proton_Integrate)_(SMEAR"))
                            else:
                                HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(Proton)_(SMEAR",           "Data_Type)_(SMEAR"))
                                HISTO_NAME = str(HISTO_NAME.replace("Data_Type)_(Proton_Integrate)_(SMEAR", "Data_Type)_(SMEAR"))
                            for Orientation in Orientation_Option_List:
                                if((Orientation not in ["z_pT"]) and ((variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi"]) or (method in ["Kinematic_Comparison"]))):
                                    # No need to have the flipped plots for the particle kinematic plots or for the kinematic comparisons
                                    continue
                                try:
                                    z_pT_Images_Together(Histogram_List_All=List_of_All_Histos_For_Unfolding,     Default_Histo_Name=HISTO_NAME, VARIABLE=f"({variable})", Method=method,    Q2_Y_Bin=BIN_NUM,                                     Multi_Dim_Option=Multi_Dim, Plot_Orientation=Orientation, Cut_Option=Cut)
                                    to_be_saved_count += 1
                                except Exception as e:
                                    print("".join([color.Error, "ERROR IN z_pT_Images_Together():\n",   color.END_R, str(traceback.format_exc()), color.END]))
                                
                # if((variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi", "MM"]) or ("sec" in variable)):
                #     continue
                if(variable in ["el", "pip", "elth", "pipth", "elPhi", "pipPhi", "MM"]):
                    continue
                # continue # This is to skip everything that isn't the z_pT_Images_Together() images
                for z_pT_Bin in range(-2, z_pT_Bin_Range + 1, 1):
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                        continue
                    # if("Y_bin" not in Binning_Method):
                    #     if(((BIN_NUM in [1]) and (z_pT_Bin in [28, 34, 35])) or ((BIN_NUM in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or ((BIN_NUM in [3]) and (z_pT_Bin in [28, 35])) or ((BIN_NUM in [4]) and (z_pT_Bin in [6, 36])) or ((BIN_NUM in [5]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [6]) and (z_pT_Bin in [30])) or ((BIN_NUM in [7]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [9]) and (z_pT_Bin in [36])) or ((BIN_NUM in [10]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [11]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [13, 14]) and (z_pT_Bin in [25])) or ((BIN_NUM in [15, 16, 17]) and (z_pT_Bin in [20]))):
                    #         continue
                    # if((Multi_Dim not in ["Off"])  and ((BIN_NUM in ["All"]) or (z_pT_Bin in [0]))):
                    #     continue
                    # if((Multi_Dim in ["Only"]) and ((BIN_NUM     in ["All"]) or (z_pT_Bin in [0]))):
                    #     continue
                    if((Multi_Dim in ["Only", "z_pT", "3D"]) and (BIN_NUM  in ["All"])):
                        continue
                    if((Multi_Dim in ["Q2_y"])               and ((BIN_NUM in ["All"]) or (z_pT_Bin not in [0]))):
                        continue
                        

                    # print("")
                    # print("BIN_NUM    =", BIN_NUM)
                    # print("HISTO_NAME =", HISTO_NAME)
                    # print("Multi_Dim  =", Multi_Dim)
                    # print("z_pT_Bin   =", z_pT_Bin)

                    if(Run_Individual_Bin_Images_Option):
                        # if(z_pT_Bin not in [0, "Integrated"]):
                        # if(z_pT_Bin not in [0]):
                        if((z_pT_Bin not in [0]) and ("sec" not in variable)):
                            print(f"""\nRunning {color.PINK}Large_Individual_Bin_Images(Histogram_List_All=..., Default_Histo_Name={HISTO_NAME}, Q2_Y_Bin={BIN_NUM}, Z_PT_Bin={z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}, Multi_Dim_Option={Multi_Dim}, String_Input=...){color.END}""")
                            try:
                                String_For_Output_txt  = Large_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int", Multi_Dim_Option=Multi_Dim, String_Input=String_For_Output_txt)
                                if(str(Multi_Dim) in ["Off"]):
                                    to_be_saved_count += 2
                                else:
                                    to_be_saved_count += 1
                            except Exception as e:
                                print(f"{color.Error}ERROR IN Large_Individual_Bin_Images():{color.END_R}\n{traceback.format_exc()}{color.END}")
                            # print(f"""Finished {color.CYAN}Large_Individual_Bin_Images(Histogram_List_All=..., Default_Histo_Name={HISTO_NAME}, Q2_Y_Bin={BIN_NUM}, Z_PT_Bin={z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}, Multi_Dim_Option={Multi_Dim}, String_Input=...){color.END}
                            # """)
                        # if(str(variable) in ["phi_t"]):
                        if("phi_t" in str(variable)):
                            print(f"""\nRunning {color.PINK}Unfolded_Individual_Bin_Images(Histogram_List_All=..., Default_Histo_Name={HISTO_NAME}, Q2_Y_Bin={BIN_NUM}, Z_PT_Bin={z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}, Multi_Dim_Option={Multi_Dim}){color.END}""")
                            try:
                                Unfolded_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding,                       Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int", Multi_Dim_Option=Multi_Dim)
                                to_be_saved_count += 1
                            except Exception as e:
                                print(f"{color.Error}ERROR IN Unfolded_Individual_Bin_Images():{color.END_R}\n{traceback.format_exc()}{color.END}")
                            # print(f"""Finished {color.CYAN}Unfolded_Individual_Bin_Images(Histogram_List_All=..., Default_Histo_Name={HISTO_NAME}, Q2_Y_Bin={BIN_NUM}, Z_PT_Bin={z_pT_Bin if(z_pT_Bin not in [-2, -1, 0]) else "All" if(z_pT_Bin in [0]) else "Integrated" if(z_pT_Bin in [-1]) else "Common_Int"}, Multi_Dim_Option={Multi_Dim}){color.END}
                            # """)
                        else:
                            continue
                    elif(Print_Run_Individual_Bin_Option):
                        print(f"\n\n\n\n{color.BOLD}NOT MAKING INDIVIDUAL BIN IMAGES AT THIS TIME{color.END}\n\tMust set Run_Individual_Bin_Images_Option = True\n\n\n\n")
                        Print_Run_Individual_Bin_Option = False

            # continue

            if((str(BIN_NUM) not in ["All", "0"]) and (Fit_Test)):
                # for Variable       in ["phi_t",     "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_y_bin_phi_t"]:
                for Variable       in Variable_List_Final:
                    if("phi_t" not in Variable):
                        print(f"\n{color.RED}Not Running Moment fit plots for variable: {Variable}{color.END}\n")
                        continue
                    # for Parameter  in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
                    for Parameter  in ["Fit_Par_B", "Fit_Par_C"]:
                    # for Parameter  in ["Fit_Par_A"]:
                        for Method in Method_Type_List:
                            if(str(Method) in ["rdf", "mdf", "Response", "Data", "Unfold", "Acceptance", "Acceptance_ratio", "Kinematic_Comparison", "Background", "Relative_Background", "gdf", "tdf", "RC"]):
                                continue
                            if((("Multi" in str(Variable)) and (str(Method) in ["SVD"])) or (("Smear" in str(smear)) and ("gdf" in str(Method)))):
                                continue
                            for Cut in Cut_Options_List:
                                if(Cut in ["Proton"]):
                                    if(Method in ["gdf", "tdf"]):
                                        continue
                                    PAR_HISTO_MASTER_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_Z"])
                                    PAR_HISTO_MASTER_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_PT"])
                                else:
                                    PAR_HISTO_MASTER_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_Z"])
                                    PAR_HISTO_MASTER_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_PT"])
                                LAST_Z_BIN,  LAST_PT_BIN  = "NA", "NA"
                                Z_BIN_COLOR, PT_BIN_COLOR = 1, 1

                                Moment_Title     = "Cos(#phi_{h})" if("Fit_Par_B" in str(Parameter)) else "Cos(2#phi_{h})" if("Fit_Par_C" in str(Parameter)) else "Multiplicity" if("Fit_Par_A" in str(Parameter)) else "".join(["Parameter ", str(Parameter).replace("Fit_Par_", "")])
                                MASTER_TITLE     = "".join(["#splitline{#scale[1.15]{", "3-Dimensional (Old) " if("Multi_Dim" in str(Variable)) else "3-Dimensional " if("MultiDim_z_pT" in str(Variable)) else "5-Dimensional " if("Multi" in str(Variable)) else "", "Plot of ", str(Moment_Title), "}}{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(BIN_NUM), "} ", root_color.Bold, "{#topbar #color[", str(root_color.Blue), "]{Method: ", "Bin-by-Bin" if(Method in ["Bin"]) else "MC Generated" if(Method in ["gdf"]) else "".join([str(Method).replace("RC_", "Radiative Corrections and "), " Unfolding"]), "}}}"])
                                if((Pass_Version not in [""]) and (Pass_Version not in str(MASTER_TITLE))):
                                    MASTER_TITLE = "".join(["#splitline{", str(MASTER_TITLE), "}{", root_color.Bold, "{#scale[1.05]{", str(Pass_Version), "}}}"])
                                if((Cut in ["Proton"]) and ("Cut with Proton Missing Mass" not in str(MASTER_TITLE))):
                                    MASTER_TITLE = "".join(["#splitline{", str(MASTER_TITLE), "}{Cut with Proton Missing Mass}"])
                                if("sec" in Variable):
                                    Sector = Variable.replace(")_(phi_t", "")
                                    Sector = str(Sector.replace("pipsec_", "")).replace("esec_", "")
                                    MASTER_TITLE = MASTER_TITLE.replace("".join(["{", str(Pass_Version), "}"]), "".join(["{", "#pi^{+} Pion" if("pipsec" in Variable) else "Electron", " Sector ", str(Sector), " #topbar ", str(Pass_Version), "}"]))
                                    del Sector

                                if(str(PAR_HISTO_MASTER_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                    Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z]   = ROOT.TMultiGraph(PAR_HISTO_MASTER_NAME_VS_Z,  "".join(["#splitline{", str(MASTER_TITLE), "}{#scale[1.05]{Showing all P_{T} bins vs z}};", "(Smeared) " if(str(smear) in ["Smear"]) else "", "z; ",           str(Moment_Title)]))
                                if(str(PAR_HISTO_MASTER_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                    Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT] = ROOT.TMultiGraph(PAR_HISTO_MASTER_NAME_VS_PT, "".join(["#splitline{", str(MASTER_TITLE), "}{#scale[1.05]{Showing all z bins vs P_{T}}};", "(Smeared) " if(str(smear) in ["Smear"]) else "", "P_{T} [GeV]; ", str(Moment_Title)]))

                                if(str(PAR_HISTO_MASTER_NAME_VS_Z)  not in Pars_Legends):
                                    Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z]      = ROOT.TLegend(0.55, 0.1, 0.9, 0.425)
                                if(str(PAR_HISTO_MASTER_NAME_VS_PT) not in Pars_Legends):
                                    Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT]     = ROOT.TLegend(0.55, 0.1, 0.9, 0.425)

                                for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
                                    if(skip_condition_z_pT_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=Common_Int_Bins)):
                                        continue
                                    if(Cut in ["Proton"]):
                                        PAR_FIND_NAME = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                    # elif(Cut not in ["Cut", "UnCut", ""]):
                                    #     PAR_FIND_NAME = "".join(["(", str(Parameter), ")_(", str(Method), ")_(", str(Cut), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                    else:
                                        PAR_FIND_NAME = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])


                                    Z_BIN_VALUE   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][0][1], 3)
                                    PT_BIN_VALUE  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][1][1], 3)
                                    # Z_BIN_VALUE   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][1], 3)
                                    # PT_BIN_VALUE  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][1], 3)
                                    Z_BIN         = str(Z_BIN_VALUE)
                                    PT_BIN        = str(PT_BIN_VALUE)

                                    Z_BIN_VALUE_Title   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][1], 3)
                                    PT_BIN_VALUE_Title  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][1], 3)
                                    Z_BIN         = str(Z_BIN_VALUE_Title)
                                    PT_BIN        = str(PT_BIN_VALUE_Title)

                                    Z_BIN_WIDTH   = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][0][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][0][0])/2, 3)
                                    PT_BIN_WIDTH  = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][1][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb" if(Cut in ["Cut", "UnCut", ""]) else f"bbb)_({Cut}")[1][1][0])/2, 3)
                                    # Z_BIN_WIDTH   = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][0])/2, 3)
                                    # PT_BIN_WIDTH  = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][0])/2, 3)

                                    # PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                                    # PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                                    # PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])

                                    if(Cut in ["Proton"]):
                                        PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                                        PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                                        PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(Proton)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])
                                    else:
                                        PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                                        PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                                        PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])

                                    if("y_bin" in Binning_Method):
                                        if(("0.27" in str(PT_BIN)) and (("Bay" in str(Method)) or ("Bin" in str(Method)))):
                                            # print("\nSKIPPING PT_BIN = 0.27\n")
                                            continue

                                    if(Fit_Test):
                                        try:
                                            PARAMETER_TO_ADD, PAR_ERROR_TO_ADD = List_of_All_Histos_For_Unfolding[str(PAR_FIND_NAME)]
                                        except:
                                            print("".join([color.Error, "ERROR IN GETTING THE FIT PARAMETERS FOR: ", color.END, str(PAR_FIND_NAME), "\n", color.RED, str(traceback.format_exc()), color.END]))
                                            continue
                                    else:
                                        PARAMETER_TO_ADD, PAR_ERROR_TO_ADD = 1, 1
                                        continue

                                    if((PT_BIN != LAST_PT_BIN) and (Z_BIN == LAST_Z_BIN)):
                                        LAST_PT_BIN       = PT_BIN
                                        PT_BIN_COLOR     += 1
                                        if(PT_BIN_COLOR in [3, 5, 7]):
                                            PT_BIN_COLOR += 1
                                        if(PT_BIN_COLOR in [9]):
                                            PT_BIN_COLOR  = 28
                                        if(PT_BIN_COLOR in [29]):
                                            PT_BIN_COLOR  = 30
                                        if(PT_BIN_COLOR in [31]):
                                            PT_BIN_COLOR  = 42
                                        if(PT_BIN_COLOR in [43]):
                                            PT_BIN_COLOR  = 46
                                        if(PT_BIN_COLOR in [47]):
                                            PT_BIN_COLOR  = 12
                                    if((Z_BIN  != LAST_Z_BIN)):
                                        LAST_Z_BIN        = Z_BIN
                                        LAST_PT_BIN       = PT_BIN
                                        Z_BIN_COLOR      += 1
                                        if(Z_BIN_COLOR in [3, 5, 7]):
                                            Z_BIN_COLOR  += 1
                                        if(Z_BIN_COLOR in [9]):
                                            Z_BIN_COLOR   = 28
                                        if(Z_BIN_COLOR in [29]):
                                            Z_BIN_COLOR   = 30
                                        if(Z_BIN_COLOR in [31]):
                                            Z_BIN_COLOR   = 42
                                        if(Z_BIN_COLOR in [43]):
                                            Z_BIN_COLOR   = 46
                                        if(Z_BIN_COLOR in [47]):
                                            Z_BIN_COLOR   = 12
                                        PT_BIN_COLOR      = 2

                                    if("y_bin" in Binning_Method):
                                        Borders_z_pT   = z_pT_Border_Lines(BIN_NUM)
                                        z_length       = Borders_z_pT[0][1] - 1
                                        pT_length      = Borders_z_pT[1][1] - 1
                                    # else:
                                    #     z_length, pT_length = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=BIN_NUM)
                                    if(str(z_pT_Bin) not in ["All", "0"]):
                                        if("y_bin" in Binning_Method):
                                            # This finds the dimensions of a particular z-pT bin for a given Q2-y bin
                                            z_bin      = ((z_pT_Bin - 1) // pT_length) + 1
                                            z_bin      = (z_length + 1) - z_bin
                                            pT_bin     = ((z_pT_Bin - 1) %  pT_length) + 1
                                            z_bin_max  = Borders_z_pT[0][2][z_bin]
                                            z_bin_min  = Borders_z_pT[0][2][z_bin  - 1]
                                            pT_bin_max = Borders_z_pT[1][2][pT_bin]
                                            pT_bin_min = Borders_z_pT[1][2][pT_bin - 1]
                                        else:
                                            z_bin_max, z_bin_min, pT_bin_max, pT_bin_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT_Bin, Q2_y_Bin_Num=BIN_NUM)
                                        if(str(PAR_HISTO_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z]   = ROOT.TGraphErrors()
                                            # Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z with #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}}}; z; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z for #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin with ", str(round(pT_bin_min, 3)), " < P_{T} < ", str(round(pT_bin_max, 3)), "}}}; #scale[1.25]{z}; ",           str(Moment_Title)]))
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineColor(PT_BIN_COLOR)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerColor(PT_BIN_COLOR)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerStyle(33)
                                            # Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(3)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(2)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineWidth(2)

                                            # # TEMPORARY PASS 2 EXCLUSION
                                            #     # REMOVE THE if() STATEMENT ONLY
                                            # if(not (str(round(pT_bin_min, 3)) in ["0.05"])):
                                            Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z].Add(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z])
                                            # Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}"]), "lep")
                                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin: ", str(round(pT_bin_min, 3)), " < P_{T} < ", str(round(pT_bin_max, 3)), "}"]), "lep")

                                        if(str(PAR_HISTO_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT] = ROOT.TGraphErrors()
                                            # Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} with #color[", str(Z_BIN_COLOR), "]{z Bin Centered at ",     str(Z_BIN),   "}}}; P_{T} [GeV]; Parameter ", str(Parameter).replace("Fit_Par_", "")]))
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} for #color[", str(Z_BIN_COLOR),  "]{z Bin with ",     str(round(z_bin_min, 3)),  " < z < ",     str(round(z_bin_max, 3)),  "}}}; #scale[1.25]{P_{T} [GeV]}; ", str(Moment_Title)]))
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineColor(Z_BIN_COLOR)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerColor(Z_BIN_COLOR)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerStyle(33)
                                            # Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(3)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(2)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineWidth(2)

                                            Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT].Add(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT])
                                            # Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin Centered at ",     str(Z_BIN),  "}"]), "lep")
                                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin: ",     str(round(z_bin_min, 3)),  " < z < ",     str(round(z_bin_max, 3)),  "}"]), "lep")

                                    else:
                                        print(color.Error, "\n\nERROR: Using center of bin in title/legends...\n\n", color.END)
                                        if(str(PAR_HISTO_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z]   = ROOT.TGraphErrors()
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z with #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}}}; z; ",           str(Moment_Title)]))
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineColor(PT_BIN_COLOR)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerColor(PT_BIN_COLOR)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerStyle(33)
                                            # Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(3)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(2)
                                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineWidth(2)

                                            Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z].Add(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z])
                                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}"]), "lep")
                                        if(str(PAR_HISTO_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT] = ROOT.TGraphErrors()
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} with #color[", str(Z_BIN_COLOR), "]{z Bin Centered at ",     str(Z_BIN),   "}}}; P_{T} [GeV]; ", str(Moment_Title)]))
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineColor(Z_BIN_COLOR)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerColor(Z_BIN_COLOR)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerStyle(33)
                                            # Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(3)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(2)
                                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineWidth(2)

                                            Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT].Add(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT])
                                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin Centered at ",     str(Z_BIN),  "}"]), "lep")

                                    if(not Point_Already_Present(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z], Z_BIN_VALUE, tol=1e-8)):
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPoint(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN(),              Z_BIN_VALUE,  PARAMETER_TO_ADD)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPointError(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN()     - 1, Z_BIN_WIDTH,  PAR_ERROR_TO_ADD)

                                    # if(("0.135" in str(PT_BIN)) or ("0.27" in str(PT_BIN)) or ("0.365" in str(PT_BIN))):
                                    #     print("".join([color.BOLD, color_bg.YELLOW, "\n\n\nFor z_pT_Bin = ", str(z_pT_Bin), ":\t\n\tZ_BIN        = ", str(Z_BIN), "\t\n\tZ_BIN_VALUE  = ", str(Z_BIN_VALUE), "\t\nand\t\t\n\tPT_BIN       = ", str(PT_BIN), "\t\n\tPT_BIN_VALUE = ", str(PT_BIN_VALUE), "\n\n", color.END, "\n\n"]))

                                    if(not Point_Already_Present(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], PT_BIN_VALUE, tol=1e-8)):
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPoint(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN(),          PT_BIN_VALUE, PARAMETER_TO_ADD)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPointError(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN() - 1, PT_BIN_WIDTH, PAR_ERROR_TO_ADD)
#Find Comment

                                
def Flip_TLegend(legend_In):
    entries = []
    # Loop over legend entries and store them
    for entry in legend_In.GetListOfPrimitives():
        entries.append((entry.GetLabel(), entry.GetObject()))
    # Create a new TLegend
    new_legend = ROOT.TLegend(0.55, 0.1, 0.9, 0.425)
    # Add entries in reverse order to the new legend
    for label, obj in reversed(entries):
        new_legend.AddEntry(obj, label, "lep")
    return new_legend

    
for ii in Histo_Pars_VS_Z:
    if(type(Histo_Pars_VS_Z[ii]) is type(ROOT.TMultiGraph())):
        Pars_Canvas[ii] = ROOT.TCanvas(str(ii), str(ii), 1200, 1100)
        # Pars_Canvas[ii].Draw()
        Histo_Pars_VS_Z[ii].SetTitle(str(Histo_Pars_VS_Z[ii].GetTitle()).replace("Showing all P_{T} bins vs z", ""))
        Histo_Pars_VS_Z[ii].Draw("APL same")
        ROOT.gPad.Modified()
        if("Par_B" in str(ii)):
            # Histo_Pars_VS_Z[ii].SetMinimum(-0.9)
            Histo_Pars_VS_Z[ii].SetMinimum(-1.0)
            Histo_Pars_VS_Z[ii].SetMaximum( 0.2)
        elif("Par_C" in str(ii)):
            # Histo_Pars_VS_Z[ii].SetMinimum(-0.35)
            Histo_Pars_VS_Z[ii].SetMinimum(-0.45)
            Histo_Pars_VS_Z[ii].SetMaximum( 0.25)
        # if((("Bayesian" in str(ii)) or ("(Bin)" in str(ii))) and ("Multi_Dim" in str(ii))):
        #     if("Par_B" in str(ii)):
        #         # Histo_Pars_VS_Z[ii].SetMinimum(-0.65 if("Q2_y_Bin_17" not in str(ii)) else -0.4 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMinimum()) if(Histo_Pars_VS_Z[ii].GetMinimum() < 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMinimum()))
        #         # Histo_Pars_VS_Z[ii].SetMaximum( 0.1  if("Q2_y_Bin_17" not in str(ii)) else  0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMaximum()) if(Histo_Pars_VS_Z[ii].GetMaximum() > 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMaximum()))
        #         Histo_Pars_VS_Z[ii].SetMinimum(-0.85)
        #         Histo_Pars_VS_Z[ii].SetMaximum( 0.15)
        #         # print(color.GREEN, "\nAdjusting (B):\n", str(ii), "\n", color.END)
        #     elif("Par_C" in str(ii)):
        #         # Histo_Pars_VS_Z[ii].SetMinimum(-0.16 if("Q2_y_Bin_17" not in str(ii)) else -0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMinimum()) if(Histo_Pars_VS_Z[ii].GetMinimum() < 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMinimum()))
        #         # Histo_Pars_VS_Z[ii].SetMaximum( 0.16 if("Q2_y_Bin_17" not in str(ii)) else  0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMaximum()) if(Histo_Pars_VS_Z[ii].GetMaximum() > 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMaximum()))
        #         Histo_Pars_VS_Z[ii].SetMinimum(-0.2)
        #         Histo_Pars_VS_Z[ii].SetMaximum( 0.2)
        #         # print(color.GREEN, "\nAdjusting (C):\n", str(ii), "\n", color.END)
        #     # else:
        #     #     print(color.RED, "NOT adjusting:\n", str(ii), color.END)
        Pars_Legends[f"{ii}_Flipped"] = Flip_TLegend(Pars_Legends[ii])
        Pars_Legends[f"{ii}_Flipped"].Draw()
        # Pars_Legends[ii].Draw()
        Pars_Canvas[ii].Update()


if(True):
    for jj in Histo_Pars_VS_PT:
        if(type(Histo_Pars_VS_PT[jj]) is type(ROOT.TMultiGraph())):
            Pars_Canvas[jj] = ROOT.TCanvas(str(jj), str(jj), 1200, 1100)
            # Pars_Canvas[jj].Draw()
            Histo_Pars_VS_PT[jj].Draw("APL same")
            ROOT.gPad.Modified()
            if("Par_B" in str(jj)):
                Histo_Pars_VS_PT[jj].SetMinimum(-1.0)
                Histo_Pars_VS_PT[jj].SetMaximum( 0.2)
            elif("Par_C" in str(jj)):
                Histo_Pars_VS_PT[jj].SetMinimum(-0.45)
                Histo_Pars_VS_PT[jj].SetMaximum( 0.25)
            Pars_Legends[jj].Draw()
            Pars_Canvas[jj].Update()

for CanvasPar_Name in Pars_Canvas:
    # if("Par_A" not in str(CanvasPar_Name)):
    Save_Name_Pars = str(CanvasPar_Name).replace(".", "_")
    Save_Name_Pars = str(Save_Name_Pars).replace("(", "")
    Save_Name_Pars = str(Save_Name_Pars).replace(")", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("SMEAR=", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("''", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("__", "_")

    Save_Name_Pars = "".join([str(Save_Name_Pars), File_Save_Format])
    if(Cut_ProQ   and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name_Pars))):
        Save_Name_Pars = Save_Name_Pars.replace(str(File_Save_Format), f"_ProtonCut{File_Save_Format}")
    elif(Tag_ProQ and (f"_TagProton{File_Save_Format}" not in str(Save_Name_Pars)) and (f"_ProtonCut{File_Save_Format}" not in str(Save_Name_Pars))):
        Save_Name_Pars = Save_Name_Pars.replace(str(File_Save_Format), f"_TagProton{File_Save_Format}")
    if(Sim_Test):
        Save_Name_Pars = f"Sim_Test_{Save_Name_Pars}"
    if(Mod_Test):
        Save_Name_Pars = f"Mod_Test_{Save_Name_Pars}"
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            Pars_Canvas[CanvasPar_Name].SetName(Save_Name_Pars.replace(".root", ""))
        Pars_Canvas[CanvasPar_Name].SaveAs(Save_Name_Pars)
    print(f"{'Saved: ' if(Saving_Q) else 'Would be Saving: '}{color.BBLUE}{Save_Name_Pars}{color.END}")
    to_be_saved_count += 1


    
print(f"{color.BGREEN}\nImages to be saved = {to_be_saved_count}\n{color.END}")

if(appended_0 and ("0" in Q2_xB_Bin_List)):
    print(f"\n{color.BOLD}Removing '0' from Q2-y Bin list{color.END}\n")
    Q2_xB_Bin_List.remove("0")

if(Create_txt_File):
    # print("\n\nString_For_Output_txt =", str(String_For_Output_txt), "\n")
    Q2_y_Select_bin = str(str(str(Q2_xB_Bin_List).replace("[",  "")).replace("]", "")).replace("'0'", "'All'")
    Q2_y_Select_bin = str(Q2_y_Select_bin.replace("'", "")).replace(",", "_")
    Q2_y_Select_bin = str(Q2_y_Select_bin.replace(" ", "_")).replace("__", "_")
    # File_Time = str(str(Date_Time).replace("Started running on ", "")).replace("\n", "")
    File_Time = str(str(Date_Day.replace(" at ", "")).replace("Started running on ", "")).replace("\n", "")
    File_Time = str(File_Time.replace(color.BOLD, "")).replace(color.END, "")
    File_Time = str((str((File_Time.replace(" ", "_")).replace("-", "_")).replace(":", "_")).replace(".", "")).replace("__", "_")
    # Output_txt_Name = "".join([str(Common_Name).replace("_All", ""), "_Q2_y_Bins_", str(Q2_y_Select_bin), "_from_", str(File_Time), ".txt"])
    Output_txt_Name         = "".join([str(Common_Name).replace("_All", ""), "_", str(File_Time), "_Q2_y_Bins_", str(Q2_y_Select_bin), ".txt"])
    
    if(Cut_ProQ   and ("_ProtonCut.txt" not in str(Output_txt_Name))):
        Output_txt_Name = Output_txt_Name.replace(".txt", "_ProtonCut.txt")
    elif(Tag_ProQ and ("_TagProton.txt" not in str(Output_txt_Name)) and ("_ProtonCut.txt" not in str(Output_txt_Name))):
        Output_txt_Name = Output_txt_Name.replace(".txt", "_TagProton.txt")
    
    if(Smearing_Options     in ["no_smear"]):
        Output_txt_Name     = Output_txt_Name.replace(".txt", "_Unsmeared.txt")
    elif(Smearing_Options   in ["smear"]):
        Output_txt_Name     = Output_txt_Name.replace(".txt", "_Smeared.txt")
    if(Closure_Test):
        Output_txt_Name = f"Closure_{Output_txt_Name}"
    else:
        if(Sim_Test):
            Output_txt_Name = f"Sim_Test_{Output_txt_Name}"
        if(Mod_Test):
            Output_txt_Name = f"Mod_Test_{Output_txt_Name}"
        
    Output_txt_Name = str(Output_txt_Name.replace(" ", "_")).replace("__", "_")
    # print(Output_txt_Name)

    # if(os.path.exists(Output_txt_Name)):
    #     print(color.RED, "Output_txt_Name =", Output_txt_Name, "already is defined...", color.END)
    #     for version in range(1, 10, 1):
    #         Output_txt_Name_New = Output_txt_Name.replace(".txt", "".join(["_V", str(version), ".txt"]))
    #         if(not os.path.exists(Output_txt_Name_New)):
    #             print("New file.txt name =", Output_txt_Name_New)
    #             Output_txt_Name = Output_txt_Name_New
    #             break
    # if(not os.path.exists(Output_txt_Name)):
    #     if(Saving_Q):
    #         with open(Output_txt_Name, "w") as file:
    #             file.write(String_For_Output_txt)
    #     print("".join(["\n", "Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Output_txt_Name), color.END, "\n"]))
    # else:
    #     print(color.Error, "Still failed to get a new name for the .txt file...", color.END)

    if(Fit_Test):
        Output_txt_Par_Name  = f"Parameters_{Output_txt_Name}"
        Text_Par_Outputs     = "Note to Reader: Print the text in this file as a string in Python for the best formatting...\n"
        if(Pass_Version not in [""]):
            Text_Par_Outputs = f"This information is from {color.BOLD}{Pass_Version}{color.END}\n{Text_Par_Outputs}"
        for BIN in Q2_xB_Bin_List:
            if(appended_0 and (str(BIN) in ["0"])):
                print(f"\n{color.BOLD}Skipping appended '0' Q2-y Bin{color.END}\n")
                continue
            BIN_NUM          = int(BIN) if(str(BIN) not in ["0"]) else "All"
            z_pT_Bin_Range   = 42       if(str(BIN_NUM) in ["2"]) else  36 if(str(BIN_NUM) in ["4", "5", "9", "10"]) else 35 if(str(BIN_NUM) in ["1", "3"]) else 30 if(str(BIN_NUM) in ["6", "7", "8", "11"]) else 25 if(str(BIN_NUM) in ["13", "14"]) else 20 if(str(BIN_NUM) in ["12", "15", "16", "17"]) else 0
            if("Y_bin" in Binning_Method):
                z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[0]
            for z_pT_Bin in range(-2, z_pT_Bin_Range + 1, 1):
            # for z_pT_Bin in range(0 if(Cut_ProQ or Tag_ProQ) else -1, z_pT_Bin_Range + 1, 1):
            # for z_pT_Bin in range(-1, 1, 1):
                if(z_pT_Bin in [-2]):
                    z_pT_Bin = "Common_Int"
                if(z_pT_Bin in [-1]):
                    z_pT_Bin = "Integrated"
                if(z_pT_Bin in [0]):
                    z_pT_Bin = "All"
                if((z_pT_Bin not in [-2, -1, 0, "-2", "-1", "0", "All", "Integrated", "Common_Int"]) and (skip_condition_z_pT_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method))):
                    continue
                for smear in Smearing_final_list:
                    if(smear not in ["''"]):
                        Text_Par_Outputs = f"{Text_Par_Outputs}\n======================================================================\nFor {color.UNDERLINE}{color.BOLD}SMEARED Q2-y Bin {BIN_NUM} - z-PT Bin {z_pT_Bin}{color.END}: "
                    else:
                        Text_Par_Outputs = f"{Text_Par_Outputs}\n======================================================================\nFor {color.UNDERLINE}{color.BOLD}Q2-y Bin {BIN_NUM} - z-PT Bin {z_pT_Bin}{color.END}: "
                    for Variable   in Variable_List_Final:
                        if(run_SecCut_Unfold):
                            for Cut_Option in Cut_Options_List:
                                Sector_txt_Out   = f" (esec {m.group(1)})" if (m := re.search(r"_eS(\d)o", Cut_Option)) else ""
                                Text_Par_Outputs = f"{Text_Par_Outputs}{color.BOLD}\n\t (*) {'3D' if(('Multi_Dim' in Variable) or ('MultiDim_z_pT' in Variable)) else '5D' if('MultiDim' in Variable) else '1D'}{Sector_txt_Out} Histograms:{color.END}"
                                for Method in Method_Type_List:
                                    if(str(Method)    in ["rdf", "mdf", "Response", "Data", "Unfold", "Acceptance", "Acceptance_ratio", "Kinematic_Comparison", "Background", "Relative_Background", "RC"]):
                                        continue
                                    if(((("Multi_Dim" in str(Variable)) or ("MultiDim" in str(Variable))) and (str(Method) in ["SVD"])) or (("Smear" in str(smear)) and ("gdf" in str(Method)))):
                                        continue
                                    if(("RC" in str(Method)) and (z_pT_Bin in [-2, -1, 0, "-2", "-1", "0", "All", "Integrated", "Common_Int"])):
                                        continue # RC only applies to full Q2-y-z-pT bins
                                    Text_Par_Outputs = f'{Text_Par_Outputs}{color.BOLD}\n\t - {"".join(["Bayesian" if("Bayesian" in str(Method)) else "Bin-by-Bin Correction", " Unfolding with RC"]) if("RC" in str(Method)) else f"{Method} Unfolding" if(Method not in ["gdf", "bbb", "Bin", "bay"]) else "Bayesian Unfolding" if(Method not in ["gdf", "bbb", "Bin"]) else "Bin-by-Bin Correction" if(Method not in ["gdf"]) else "Generated Plot"} Fits:{color.END}'
                                    
                                    PAR_A_NAME = f"(Fit_Par_A)_({  Method})_({Cut_Option})_(SMEAR={smear})_(Q2_y_Bin_{BIN_NUM})_(z_pT_Bin_{z_pT_Bin})_({Variable})"
                                    PAR_B_NAME = f"(Fit_Par_B)_({  Method})_({Cut_Option})_(SMEAR={smear})_(Q2_y_Bin_{BIN_NUM})_(z_pT_Bin_{z_pT_Bin})_({Variable})"
                                    PAR_C_NAME = f"(Fit_Par_C)_({  Method})_({Cut_Option})_(SMEAR={smear})_(Q2_y_Bin_{BIN_NUM})_(z_pT_Bin_{z_pT_Bin})_({Variable})"
                                    CHI_2_NAME = f"(Chi_Squared)_({Method})_({Cut_Option})_(SMEAR={smear})_(Q2_y_Bin_{BIN_NUM})_(z_pT_Bin_{z_pT_Bin})_({Variable})"
                                    PARAMETER_A, PARAMETER_B, PARAMETER_C = "ERROR", "ERROR", "ERROR"
                                    ERROR_PAR_A, ERROR_PAR_B, ERROR_PAR_C = "ERROR", "ERROR", "ERROR"
                                    Chi_2_Value, NDF_Value                = "ERROR", "ERROR"
                                    try:
                                        PARAMETER_A, ERROR_PAR_A = List_of_All_Histos_For_Unfolding[str(PAR_A_NAME)]
                                    except:
                                        print(f"{color.Error}ERROR IN GETTING THE FIT PARAMETER A FOR: {color.END}\n\tPAR_A_NAME = {PAR_A_NAME}")
                                        # print(f"{color.BOLD}{traceback.format_exc()}{color.END}")
                                        # continue
                                    try:
                                        PARAMETER_B, ERROR_PAR_B = List_of_All_Histos_For_Unfolding[str(PAR_B_NAME)]
                                    except:
                                        print(f"{color.Error}ERROR IN GETTING THE FIT PARAMETER B FOR: {color.END}\n\tPAR_B_NAME = {PAR_B_NAME}")
                                        # print(f"{color.BOLD}{traceback.format_exc()}{color.END}")
                                        # continue
                                    try:
                                        PARAMETER_C, ERROR_PAR_C = List_of_All_Histos_For_Unfolding[str(PAR_C_NAME)]
                                    except:
                                        print(f"{color.Error}ERROR IN GETTING THE FIT PARAMETER C FOR: {color.END}\n\tPAR_C_NAME = {PAR_C_NAME}")
                                        # print(f"{color.BOLD}{traceback.format_exc()}{color.END}")
                                        # continue
                                    try:
                                        Chi_2_Value, NDF_Value = List_of_All_Histos_For_Unfolding[str(CHI_2_NAME)]
                                    except:
                                        print(f"{color.Error}ERROR IN GETTING THE FIT Chi^2 FOR: {color.END}\n\tCHI_2_NAME = {CHI_2_NAME}")
                                        # print(f"{color.BOLD}{traceback.format_exc()}{color.END}")
                                        # continue
                                    Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par A    = {PARAMETER_A} ± {ERROR_PAR_A}"
                                    Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par B    = {PARAMETER_B} ± {ERROR_PAR_B}"
                                    Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par C    = {PARAMETER_C} ± {ERROR_PAR_C}"
                                    if((str not in [type(Chi_2_Value), type(NDF_Value)]) and (NDF_Value not in [0])):
                                        Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t chi2/NDF = {Chi_2_Value/NDF_Value}"
                                    else:
                                        Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t chi2/NDF = ERROR"
                                    Text_Par_Outputs = Text_Par_Outputs.replace("\t", "    ")
                        else:
                            if(any((("Multi" in ii) or ("sec" in ii)) for ii in Variable_List_Final)):
                                Sector_txt_Out = "" if("sec" not in Variable) else str(Variable.replace(")_(phi_t", "")).replace("_", " ")
                            else:
                                Sector_txt_Out = ""
                            Text_Par_Outputs   = "".join([str(Text_Par_Outputs), color.BOLD, "\n\t (*) ", "3D" if(("Multi_Dim" in Variable) or ("MultiDim_z_pT" in Variable)) else "5D" if("MultiDim" in Variable) else "1D" if(Sector_txt_Out in [""]) else f"1D ({Sector_txt_Out})", " Histograms:", color.END])
                            for Method in Method_Type_List:
                                if(str(Method)    in ["rdf", "mdf", "Response", "Data", "Unfold", "Acceptance", "Acceptance_ratio", "Kinematic_Comparison", "Background", "Relative_Background", "RC"]):
                                    continue
                                if(("RC" in str(Method)) and (z_pT_Bin in [-2, -1, 0, "-2", "-1", "0", "All", "Integrated", "Common_Int"])):
                                    continue # RC only applies to full Q2-y-z-pT bins
                                if(((("Multi_Dim" in str(Variable)) or ("MultiDim" in str(Variable))) and (str(Method) in ["SVD"])) or (("Smear" in str(smear)) and ("gdf" in str(Method)))):
                                    continue
                                Text_Par_Outputs = "".join([str(Text_Par_Outputs), color.BOLD, "\n\t - ", "".join(["Bayesian" if("Bayesian" in str(Method)) else "Bin-by-Bin Correction", " Unfolding with RC"]) if("RC" in str(Method)) else f"{Method} Unfolding" if(Method not in ["gdf", "bbb", "Bin", "bay"]) else "Bayesian Unfolding" if(Method not in ["gdf", "bbb", "Bin"]) else "Bin-by-Bin Correction" if(Method not in ["gdf"]) else "Generated Plot", " Fits:", color.END])
                                PAR_A_NAME = "".join(["(Fit_Par_A)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ) else ")_(Integrate" if("Integrate" in Cut_Options_List) else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                PAR_B_NAME = "".join(["(Fit_Par_B)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ) else ")_(Integrate" if("Integrate" in Cut_Options_List) else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                PAR_C_NAME = "".join(["(Fit_Par_C)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ) else ")_(Integrate" if("Integrate" in Cut_Options_List) else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                CHI_2_NAME = "".join(["(Chi_Squared)_(", str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ) else ")_(Integrate" if("Integrate" in Cut_Options_List) else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                # #####################################
                                # PAR_A_NAME = "".join(["(Fit_Par_A)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ)                                                         else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                # PAR_B_NAME = "".join(["(Fit_Par_B)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ)                                                         else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                # PAR_C_NAME = "".join(["(Fit_Par_C)_(",   str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ)                                                         else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                # CHI_2_NAME = "".join(["(Chi_Squared)_(", str(Method), ")_(Proton_Integrate" if("Proton_Integrate" in Cut_Options_List) else ")_(Proton" if(Cut_ProQ)                                                         else "", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                                PARAMETER_A, PARAMETER_B, PARAMETER_C = "ERROR", "ERROR", "ERROR"
                                ERROR_PAR_A, ERROR_PAR_B, ERROR_PAR_C = "ERROR", "ERROR", "ERROR"
                                Chi_2_Value, NDF_Value = "ERROR", "ERROR"
                                try:
                                    PARAMETER_A, ERROR_PAR_A = List_of_All_Histos_For_Unfolding[str(PAR_A_NAME)]
                                except:
                                    print("".join([color.Error, "ERROR IN GETTING THE FIT PARAMETER A FOR: ", color.END, "\n\tPAR_A_NAME = ", str(PAR_A_NAME)]))
                                    # print("".join([color.BOLD, str(traceback.format_exc()), color.END]))
                                    # continue
                                try:
                                    PARAMETER_B, ERROR_PAR_B = List_of_All_Histos_For_Unfolding[str(PAR_B_NAME)]
                                except:
                                    print("".join([color.Error, "ERROR IN GETTING THE FIT PARAMETER B FOR: ", color.END, "\n\tPAR_B_NAME = ", str(PAR_B_NAME)]))
                                    # print("".join([color.BOLD, str(traceback.format_exc()), color.END]))
                                    # continue
                                try:
                                    PARAMETER_C, ERROR_PAR_C = List_of_All_Histos_For_Unfolding[str(PAR_C_NAME)]
                                except:
                                    print("".join([color.Error, "ERROR IN GETTING THE FIT PARAMETER C FOR: ", color.END, "\n\tPAR_C_NAME = ", str(PAR_C_NAME)]))
                                    # print("".join([color.BOLD, str(traceback.format_exc()), color.END]))
                                    # continue
                                try:
                                    Chi_2_Value, NDF_Value = List_of_All_Histos_For_Unfolding[str(CHI_2_NAME)]
                                except:
                                    print("".join([color.Error, "ERROR IN GETTING THE FIT Chi^2 FOR: ", color.END, "\n\tCHI_2_NAME = ", str(CHI_2_NAME)]))
                                    # print("".join([color.BOLD, str(traceback.format_exc()), color.END]))
                                #     # continue
                                Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par A    = {PARAMETER_A} ± {ERROR_PAR_A}"
                                Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par B    = {PARAMETER_B} ± {ERROR_PAR_B}"
                                Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t Par C    = {PARAMETER_C} ± {ERROR_PAR_C}"
                                if((str not in [type(Chi_2_Value), type(NDF_Value)]) and (NDF_Value not in [0])):
                                    Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t chi2/NDF = {Chi_2_Value/NDF_Value}"
                                else:
                                    Text_Par_Outputs = f"{Text_Par_Outputs}\n\t\t\t chi2/NDF = ERROR"
                                Text_Par_Outputs = Text_Par_Outputs.replace("\t", "    ")
        # print(f"Text_Par_Outputs = {Text_Par_Outputs}")
        if(os.path.exists(Output_txt_Par_Name)):
            print(color.RED, "Output_txt_Par_Name =", Output_txt_Par_Name, "already is defined...", color.END)
            for version in range(1, 10, 1):
                Output_txt_Par_Name_New = Output_txt_Par_Name.replace(".txt", "".join(["_V", str(version), ".txt"]))
                if(not os.path.exists(Output_txt_Par_Name_New)):
                    print("New file.txt name =", Output_txt_Par_Name_New)
                    Output_txt_Par_Name = Output_txt_Par_Name_New
                    break
        if(not os.path.exists(Output_txt_Par_Name)):
            if(Saving_Q):
                with open(Output_txt_Par_Name, "w") as file:
                    file.write(Text_Par_Outputs)
            print("".join(["\n", "Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Output_txt_Par_Name), color.END, "\n"]))
        else:
            print(f"{color.Error}Still failed to get a new name for the .txt file...{color.END}")



    def Extract_phi_h_Histograms_Info(hist_dict=List_of_All_Histos_For_Unfolding, save_to_file=Saving_Q, filename=f"Statistics_{Output_txt_Name}"):
        # Extract information from a dictionary of ROOT objects, focusing on the TH1D phi_h histograms
        # Parameters:
        #     - hist_dict: dictionary with string keys and ROOT TH1D histogram objects as values.
        #     - save_to_file: boolean flag to save the extracted information to a text file.
        #     - filename: name of the file to save the extracted information.
        # info_str = ""  # Initialize the string to store information.
        info_str = "Note to Reader: Print the text in this file as a string in Python for the best formatting...\n"
        if(Pass_Version not in [""]):
            info_str = f"This information is from {color.BOLD}{Pass_Version}{color.END}\n{info_str}"
        for hist_name, hist in hist_dict.items():
            # Check if the object name contains 'phi_t' and is indeed a TH1D histogram
            if((("phi_t" in hist_name) or ("phi_h" in hist_name)) and (isinstance(hist, ROOT.TH1D)) and (not (("(1D)" in hist_name) and ("Multi" in hist_name)))):
                if(any(Method   in hist_name for Method in ["(Bin)", "(bbb)"])):
                    Method_Name = "Bin-by-Bin Correction"
                elif(any(Method in hist_name for Method in ["(rdf)"])):
                    Method_Name = "Experimental Data"
                elif(any(Method in hist_name for Method in ["(bayes)", "(bay)", "(Bayesian)"])):
                    Method_Name = "Bayesian Unfolding"
                elif(any(Method in hist_name for Method in ["(RC_Bayesian)"])):
                    Method_Name = "Bayesian Unfolding with RC"
                elif(any(Method in hist_name for Method in ["(RC_Bin)"])):
                    Method_Name = "Bin-by-Bin Correction with RC"
                elif(any(Method in hist_name for Method in ["(SVD)"])):
                    Method_Name = "SVD Unfolding"
                elif(any(Method in hist_name for Method in ["(mdf)", "(gdf)", "(tdf)", "(gen)"])):
                    Method_Name  = "".join(["Monte Carlo (", "Generated" if("(gdf)" in hist_name) else "Reconstructed" if("(mdf)" in hist_name) else "True" if("(tdf)" in hist_name) else "Matched Generated" if("(gen)" in hist_name) else "Error", ")"])
                elif(any(Method in hist_name for Method in ["(Acceptance)"])):
                    Method_Name  = "Acceptance"
                else:
                    Method_Name  = f"{color.Error}Error{color.END}"

                # Smear_Name       = "Smearing" if((not any(Method in hist_name for Method in ["rdf", "gdf", "tdf", "gen"])) and ("Smear" in hist_name)) else "Not smeared"
                # Smear_Name       = "Not Smeared" if("SMEAR=''" in hist_name) else "Smeared"
                for Method in ["Bin", "bbb", "rdf", "bayes", "bay", "Bayesian", "SVD", "mdf", "gdf", "tdf", "gen", "Acceptance", "RC_Bin", "RC_Bayesian"]:
                    hist_name = hist_name.replace(f"_({Method})_", f"_({Method_Name})_")
                hist_name     = hist_name.replace("_(SMEAR='')_", "_(Not Smeared)_")
                hist_name     = hist_name.replace("_(SMEAR=Smear)_", "_(Smeared)_")
                total_stats   = sum(hist.GetBinContent(bin) for bin in range(1, hist.GetNbinsX() + 1)) # hist.GetEntries()
                # info_str += f"\n========================================================================================================================\n{color.BOLD}Histogram Name: \n\t{color.END}{hist_name}\nhist.GetName() = {hist.GetName()}\n"
                info_str += f"\n========================================================================================================================\n{color.BOLD}Histogram Name: \n\t{color.END}{color.BLUE}{hist_name}{color.END}\n"
                info_str += f"\n\t{color.UNDERLINE}Total Statistics{color.END}: {total_stats}\n\n"
                # info_str += f"{color.BOLD}{color.UNDERLINE}Bin #\t\tRange\t\t\tContent\t\t\tError\t\t{color.END}\n"
                info_str += f"{color.BOLD}{color.UNDERLINE}"
                info_str += "\t{:<8}|\t{:<20}|\t{:<20}|\t{:<20}|\t".format("Bin #", "Bin Range (˚)", "Content", "Error")
                info_str += f"{color.END}\n"
                for bin in range(1, hist.GetNbinsX() + 1):  # Loop over each bin
                    # center  = round(hist.GetBinCenter(bin),  2)
                    bin_lower_edge = hist.GetBinLowEdge(bin)
                    bin_upper_edge = bin_lower_edge + hist.GetBinWidth(bin)
                    bin_range = f"{round(bin_lower_edge, 2)}-{round(bin_upper_edge, 2)}"
                    # bin_range = f"{int(bin_lower_edge)}-{int(bin_upper_edge)}"
                    content   = round(hist.GetBinContent(bin), 6)
                    error     = round(hist.GetBinError(bin),   6)
                    try:
                        info_str += "\t{:<8}|\t{:<20}|\t{:<20.5f}|\t{:<20.5f}|\t\n".format(bin, bin_range, content, error)
                    except:
                        info_str += f"{bin}\t{bin_range}\t{content}\t{error}\n"
                    # info_str += f"{bin}\t\t{bin_range}\t\t\t{content}\t\t\t{error}\n"
                info_str += f"{color.UNDERLINE}\t                                                                                   \t{color.END}\n\n========================================================================================================================"  # Add a newline for separation between histograms
        info_str         += "\n========================================================================================================================\n\n"
        if(save_to_file):
            with open(filename, "w") as file:
                file.write(info_str)
        print("".join(["\n", "Saved: " if(save_to_file) else "Would be Saving: ", color.BBLUE, str(filename), color.END, "\n"]))
        # print(f"Content of {filename} -> \n{info_str}")

    try:
        if(Create_txt_File and Create_stat_File):
            Extract_phi_h_Histograms_Info(hist_dict=List_of_All_Histos_For_Unfolding, save_to_file=Saving_Q, filename=f"Statistics_{Output_txt_Name}")
        else:
            print(f"{color.RED}\nNOT RUNNING Extract_phi_h_Histograms_Info()...\n{color.END}")
    except:
        print(f"{color.Error}Failed...{color.END}\nTraceback:\n{traceback.format_exc()}")


    # info_str += "{:<8}{:<15}{:<15}{:<15}{:<15}\n".format("Bin #", "Bin Center", "Content", "Error", "Bin Edges")

    # for bin in range(1, hist.GetNbinsX() + 1):
    #     content = hist.GetBinContent(bin)
    #     error = hist.GetBinError(bin)
    #     bin_low_edge = hist.GetBinLowEdge(bin)
    #     bin_upper_edge = bin_low_edge + hist.GetBinWidth(bin)
    #     # Assuming you want to print the bin center as well, which is (low_edge + upper_edge) / 2
    #     bin_center = (bin_low_edge + bin_upper_edge) / 2
    #     info_str += "{:<8}{:<15.5f}{:<15.5f}{:<15.5f}{:<15.5f}-{:<15.5f}\n".format(
    #         bin, bin_center, content, error, bin_low_edge, bin_upper_edge
    #     )
else:
    print(f"{color.RED}\nNot Creating .txt File(s)\n{color.END}")

    


# # Getting Current Date
# datetime_object_end = datetime.now()
# endMin_full, endHr_full, endDay_full = datetime_object_end.minute, datetime_object_end.hour, datetime_object_end.day
# if(datetime_object_end.minute < 10):
#     timeMin_end = ''.join(['0', str(datetime_object_end.minute)])
# else:
#     timeMin_end = str(datetime_object_end.minute)
# # Printing Current Time
# if(datetime_object_end.hour > 12 and datetime_object_end.hour < 24):
#     print("".join(["The time that this code finished is ", str((datetime_object_end.hour) - 12), ":", str(timeMin_end), " p.m."]))
# if(datetime_object_end.hour < 12 and datetime_object_end.hour > 0):
#     print("".join(["The time that this code finished is ", str(datetime_object_end.hour),        ":", str(timeMin_end), " a.m."]))
# if(datetime_object_end.hour == 12):
#     print("".join(["The time that this code finished is ", str(datetime_object_end.hour),        ":", str(timeMin_end), " p.m."]))
# if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
#     print("".join(["The time that this code finished is 12:", str(timeMin_end), " a.m."]))

    

print(f"Saved {to_be_saved_count} Images...")

timer.stop(count_label="Images", count_value=to_be_saved_count)

# Num_of_Days, Num_of_Hrs, Num_of_Mins = 0, 0, 0

# if(startDay_full > endDay_full):
#     Num_of_Days  = endDay_full + (30 - startDay_full)
# else:
#     Num_of_Days  = endDay_full - startDay_full
# if(startHr_full  > endHr_full):
#     Num_of_Hrs   = endHr_full  + (24 - startHr_full)
# else:
#     Num_of_Hrs   = endHr_full  - startHr_full
# if(startMin_full > endMin_full):
#     Num_of_Mins  = endMin_full + (60 - startMin_full)
# else:
#     Num_of_Mins  = endMin_full - startMin_full
# if(Num_of_Hrs > 0  and startMin_full >= endMin_full):
#     Num_of_Hrs  += -1
# if(Num_of_Days > 0 and startHr_full  >= endHr_full):
#     Num_of_Days += -1


# print("\nThe total time the code took to run the given files is:")
# print("".join([str(Num_of_Days), " Day(s), ", str(Num_of_Hrs), " Hour(s), and ", str(Num_of_Mins), " Minute(s)."]))


# if((((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins) != 0):
#     rate_of_histos = to_be_saved_count/(((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins)
#     print(f"Rate of Histos/Minute = {rate_of_histos} Histos/Min")
    

print(f"""\n\n{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

