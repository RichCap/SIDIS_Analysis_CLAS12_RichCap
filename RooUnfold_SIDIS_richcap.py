#!/usr/bin/env python

import sys

print("Starting...\n")

from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT
import math

from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

# # Turns off the canvases when running in the command line
# ROOT.gROOT.SetBatch(1)

import traceback
from datetime import datetime

import shutil
import os

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)

       
Saving_Q     = True
Sim_Test     = False
Mod_Test     = False
Closure_Test = False
Fit_Test     = True
Smearing_Options = "both"
if(len(sys.argv) > 1):
    arg_option_1 = str(sys.argv[1])
    if(arg_option_1 in ["test", "Test", "time", "Time"]):
        print("\nNOT SAVING\n")
        Saving_Q = False
    else:
        print("".join(["\nOption Selected: ", str(arg_option_1), " (Still Saving...)" if("no_save" not in str(arg_option_1)) else " (NOT SAVING)"]))
        Saving_Q     = True if("no_save" not in str(arg_option_1)) else False
        Sim_Test     = True if(("sim"        in str(arg_option_1)) or ("simulation" in str(arg_option_1))) else False
        Mod_Test     = True if(("mod"        in str(arg_option_1)) or ("modulation" in str(arg_option_1))) else False
        Closure_Test = True if(("close"      in str(arg_option_1)) or ("closure"    in str(arg_option_1))  or ("Closure" in str(arg_option_1)) or ("Closure" in str(arg_option_1))) else False
        Fit_Test     = True if("no_fit"  not in str(arg_option_1)) else False
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
    print("".join([color.BLUE, "\nRunning Closure Test (Unfolding the Modulated MC using the unweighted response matrices)\n", color.END]))
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Modulated Simulation"
elif(Sim_Test):
    print("".join([color.BLUE, "\nRunning Simulated Test\n", color.END]))
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
if(Mod_Test):
    print("".join([color.BLUE, "\nUsing ", color.BOLD, "Modulated", color.END, color.BLUE, " Monte Carlo Files (to create the response matrices)\n", color.END]))
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = "".join([str(Standard_Histogram_Title_Addition), " - Using Modulated Response Matrix"])
    else:
        Standard_Histogram_Title_Addition = "Closure Test - Using Modulated Response Matrix"
if(not Fit_Test):
    print("\n")
    print("".join([color.BLUE, color.BOLD, color_bg.RED, """\n\n    Not Fitting Plots    \n""", color.END, "\n\n"]))
    
    
# if(str(Smearing_Options) not in ["both"]):
print(color.BLUE, color.BOLD, "\nSmear option selected is:", "No Smear" if(str(Smearing_Options) in ["", "no_smear"]) else str(Smearing_Options.replace("_s", "S")).replace("s", "S"), color.END, "\n")

File_Save_Format = ".png"
# File_Save_Format = ".root"
# File_Save_Format = ".pdf"


if((File_Save_Format != ".png") and Saving_Q):
    print(color.GREEN, color.BOLD, "\nSave Option was not set to output .png files. Save format is:", "".join([color.END, color.BOLD, color.UNDERLINE, str(File_Save_Format), color.END, "\n"]))

    
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

if(len(sys.argv) > 2):
    Q2_xB_Bin_List = []
    for ii_bin in range(2, len(sys.argv), 1):
        Q2_xB_Bin_List.append(sys.argv[ii_bin])
    if(Q2_xB_Bin_List == []):
        print("Error")
        Q2_xB_Bin_List = ['1']
    print(str(("".join(["\nRunning for Q2-xB/Q2-y Bins: ", str(Q2_xB_Bin_List)]).replace("[", "")).replace("]", "")))
    
    

print("".join([color.BOLD, "\nStarting RG-A SIDIS Analysis\n", color.END]))


# Getting Current Date
datetime_object_full = datetime.now()

startMin_full = datetime_object_full.minute
startHr_full  = datetime_object_full.hour
startDay_full = datetime_object_full.day

if(datetime_object_full.minute < 10):
    timeMin_full = "".join(["0", str(datetime_object_full.minute)])
else:
    timeMin_full = str(datetime_object_full.minute)

    
Date_Day = "".join(["\nStarted running on ", color.BOLD, str(datetime_object_full.month), "-", str(startDay_full), "-", str(datetime_object_full.year), color.END, " at "])
# Printing Current Time
Date_Time = Date_Day
if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
    Date_Time = "".join([Date_Day, color.BOLD, str((datetime_object_full.hour)-12), ":", timeMin_full, " p.m.", color.END])
if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
    Date_Time = "".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " a.m.", color.END])
if(datetime_object_full.hour == 12):
    Date_Time = "".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " p.m.", color.END])
if(datetime_object_full.hour == 0 or  datetime_object_full.hour == 24):
    Date_Time = "".join([Date_Day, color.BOLD, "12:", str(timeMin_full), " a.m.", color.END])
print(Date_Time, "\n")




try:
    import RooUnfold
except ImportError:
    print("".join([color.RED, color.BOLD, "ERROR: \n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n"]))
    # print("Somehow the python module was not found, let's try loading the library by hand...")
    # try:
    #     ROOT.gSystem.Load("libRooUnfold.so")
    # except:
    #     print("".join([color.RED, color.BOLD, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
        
        
print("\n\n")



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
    elif(Sim_Test):
        B, C = 0, 0
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A    = (Histo_max_bin_num)/((1 + B*ROOT.cos(Histo_max_bin_phi) + C*ROOT.cos(2*Histo_max_bin_phi)))
        
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
            print("".join([color.RED, color.BOLD, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
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
                print(color.RED, color.BOLD, "POTENTIAL RISK OF DIVIDE BY 0 ERROR FOR Phi_max_bin =", Phi_max_bin, color.END)
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
            print("".join([color.RED, color.BOLD, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            print(color.RED, color.BOLD, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)

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
    elif(Sim_Test):
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
            print("".join([color.RED, color.BOLD, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            print(color.RED, color.BOLD, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)

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
            print("".join([color.RED, color.BOLD, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
            print(color.RED, color.BOLD, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)
            A_opt, B_opt, C_opt, D_opt = "Error", "Error", "Error", "Error"
        return [A_opt, B_opt, C_opt, D_opt]

###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################






######################################################################################################################################################
##==========##==========##    Simple Function for Drawing 2D Histograms     ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################

def Draw_2D_Histograms_Simple(DataFrame, Canvas_Input, CD_Num=1, Var_D1="Q2", Var_D2="xB", Q2_xB_Bin="All", z_pT_Bin="All", Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q=""):
    NumBins_List, MinBin_List, MaxBin_List = [], [], []
    if((str(Smear_Q) not in [""]) and (str(Data_Type) not in ["rdf", "gdf", "gen"])):
        Var_D1 = "".join([str(Var_D1), "_smeared" if("_smeared" not in str(Var_D1)) else ""])
        Var_D2 = "".join([str(Var_D2), "_smeared" if("_smeared" not in str(Var_D2)) else ""])
    for variable in [Var_D1, Var_D2]:
        if(variable in ["el", "el_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(8)
            # NumBins_List.append(200)
            NumBins_List.append(100)
        if(variable in ["pip", "pip_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(6)
            # NumBins_List.append(200)
            NumBins_List.append(100)
        if(variable in ["elth",  "pipth",  "elth_smeared",  "pipth_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(40)
            # NumBins_List.append(200)
            NumBins_List.append(100)
        if(variable in ["elPhi", "pipPhi", "elPhi_smeared", "pipPhi_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(360)
            # NumBins_List.append(200)
            NumBins_List.append(100)
            
        if(variable in ["Q2", "Q2_smeared"]):
            if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))):
                MinBin_List.append(1.48)
                MaxBin_List.append(11.87)
                NumBins_List.append(100)
            else:
                MinBin_List.append(1.154)
                MaxBin_List.append(12.434)
                NumBins_List.append(80)
        if(variable in ["xB", "xB_smeared"]):
            MinBin_List.append(0.09)
            MaxBin_List.append(0.826)
            # NumBins_List.append(100)
            NumBins_List.append(50)
        if(variable in ["z",  "z_smeared"]):
            MinBin_List.append(0.017)
            MaxBin_List.append(0.935)
            # NumBins_List.append(100)
            NumBins_List.append(50)
        if(variable in ["pT", "pT_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(1.26)
            # NumBins_List.append(120)
            NumBins_List.append(60)
            
        if(variable in ["y", "y_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(1)
            # NumBins_List.append(20)
            NumBins_List.append(80)
            
    # Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
    Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='", "Y_bin" if("Y_bin" in str(Binning_Method)) else str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "'-[Q2-y-Bin=", str(Q2_xB_Bin) if(Q2_xB_Bin not in [0, '0', 'all', 'All']) else "All", ", z-PT-Bin=All]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
    # print("\n\nFind_Name =", Find_Name, "\n\n")
    
    Drawing_Histo_Found = DataFrame.Get(Find_Name)
    
    # print(Drawing_Histo_Found)
    
    #########################################################
    ##===============##     3D Slices     ##===============##
    if("3D" in str(type(Drawing_Histo_Found))):
        try:
            bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin not in ["All", 0]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin not in ["All", 0]) else Drawing_Histo_Found.GetNbinsX())
            if(z_pT_Bin not in ["All", 0]):
                Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            Drawing_Histo_Set = Drawing_Histo_Found.Project3D('yz e')
            Drawing_Histo_Set.SetName(str(Drawing_Histo_Found.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin in ["All", 0]) else str(z_pT_Bin)])))
            Drawing_Histo_Title = (str(Drawing_Histo_Set.GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: " if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin not in ["All", 0]) else "All", "}}}"]))
            Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
            if(Data_Type == "mdf"):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
            if(Data_Type == "gdf"):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Generated")
            Drawing_Histo_Set.SetTitle(Drawing_Histo_Title)
            # print(str(Drawing_Histo_Set.GetTitle()))
        except:
            print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (2D Histograms):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            Drawing_Histo_Set = Drawing_Histo_Found
            print("ERROR: Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
    else:
        Drawing_Histo_Set = Drawing_Histo_Found
        print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
    ##===============##     3D Slices     ##===============##
    #########################################################
    # Draw_Canvas(Canvas_Input, CD_Num, 0.15)
    Draw_Canvas(canvas=Canvas_Input, cd_num=CD_Num, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set.Draw("colz")
    
    Canvas_Input.Modified()
    Canvas_Input.Update()
    
    palette_move(canvas=Canvas_Input, histo=Drawing_Histo_Set, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    
    Canvas_Input.Modified()
    Canvas_Input.Update()
    
    if("el" in str(Var_D1)):
        Drawing_Histo_Set.GetYaxis().SetRangeUser(2, 8)
    
    if("Var-D1='Q2" in str(Find_Name) and "Var-D2='xB" in str(Find_Name)):
        Drawing_Histo_Set.SetTitle((Drawing_Histo_Set.GetTitle()).replace("Q^{2}-x_{B} Bin: All" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin not in ["All", 0]) else "All", "}"])))
        # print("".join([color.BLUE, "Q2-xB plots:", color.END, "\n", str(Drawing_Histo_Set.GetTitle()), "\n", str(Find_Name), "\n\n"]))
        Q2_xB_borders, line_num = {}, 0
        for b_lines in Q2_xB_Border_Lines(-1):
            Q2_xB_borders[line_num] = ROOT.TLine()
            Q2_xB_borders[line_num].SetLineColor(1)    
            Q2_xB_borders[line_num].SetLineWidth(2)
            Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
            line_num += 1
        if((Q2_xB_Bin not in ["All", 0]) and (("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method)))):
            ##=====================================================##
            ##==========##     Selecting Q2-xB Bin     ##==========##
            ##=====================================================##
            line_num_2 = 0
            for b_lines_2 in Q2_xB_Border_Lines(Q2_xB_Bin):
                Q2_xB_borders[line_num_2] = ROOT.TLine()
                Q2_xB_borders[line_num_2].SetLineColor(2)
                Q2_xB_borders[line_num_2].SetLineWidth(3)
                Q2_xB_borders[line_num_2].DrawLine(b_lines_2[0][0], b_lines_2[0][1], b_lines_2[1][0], b_lines_2[1][1])
                line_num_2 += + 1
            ##=====================================================##
            ##==========##     Selecting Q2-xB Bin     ##==========##
            ##=====================================================##
            
            
    if("Var-D1='Q2" in str(Find_Name) and "Var-D2='y" in str(Find_Name)):
        Drawing_Histo_Set.SetTitle((Drawing_Histo_Set.GetTitle()).replace("Q^{2}-x_{B} Bin: All" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin not in ["All", 0]) else "All", "}"])))
        try:
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
                for Q2_Y_Bin_ii in range(1, 40, 1):
                    Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
                    for line in Q2_y_borders[Q2_Y_Bin_ii]:
                        line.Draw("same")
 
        except:
            print("".join([color.RED, color.BOLD, "Q2-y line fail...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            
            
            
    if((Q2_xB_Bin not in ["All", 0]) and ("Var-D1='z" in str(Find_Name)) and ("Var-D2='pT" in str(Find_Name))):
        if("y_bin" in Binning_Method):
            z_pT_borders = {}
            Max_z  = max(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
            Min_z  = min(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
            Max_pT = max(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
            Min_pT = min(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
            for zline in z_pT_Border_Lines(Q2_xB_Bin)[0][2]:
                for pTline in z_pT_Border_Lines(Q2_xB_Bin)[1][2]:
                    z_pT_borders[zline] = ROOT.TLine()
                    z_pT_borders[zline].SetLineColor(1)
                    z_pT_borders[zline].SetLineWidth(2)
                    # z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT)
                    z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                    z_pT_borders[pTline] = ROOT.TLine()
                    z_pT_borders[pTline].SetLineColor(1)
                    z_pT_borders[pTline].SetLineWidth(2)
                    # z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline)
                    z_pT_borders[pTline].DrawLine(pTline, Min_z, pTline, Max_z)
        else:
            Drawing_Histo_Set.GetXaxis().SetRangeUser(0, 1.2)
            Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_xB_Bin, Set_Max_Y=1.2, Set_Max_X=1.2)
                
    if(("Var-D1='z" in str(Find_Name)) and ("Var-D2='pT" in str(Find_Name))):
        if(("y_bin" in str(Binning_Method)) or ("Y_bin" in str(Binning_Method))):
            Drawing_Histo_Set.GetYaxis().SetRangeUser(0, 1.2)
            MM_z_pT_borders = {}
            # Create a TLegend
            MM_z_pT_legend = ROOT.TLegend(0.5, 0.1, 0.9, 0.2)  # (x1, y1, x2, y2)
            MM_z_pT_legend.SetNColumns(2)
            # for MM in [0.94, 1.5, 2.5]:
            # for MM in [1.22474, 0.77545, 0.93956, 1.232]:
            # for MM in [0.93956, 1.232, 1.5, 2.0]:
            # Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation="z_pT")
            MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin=Q2_xB_Bin, Plot_Orientation="z_pT")
            for MM_lines in MM_z_pT_borders:
                MM_z_pT_borders[MM_lines].Draw("same")
            MM_z_pT_legend.Draw("same")

######################################################################################################################################################
##==========##==========##    Simple Function for Drawing 2D Histograms     ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################
























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
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Original)   #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    if(Method in ["SVD"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
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
                
                print("".join([color.BOLD, color.CYAN, "Finished ", color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return List_Of_Outputs

            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (SVD)...", color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                
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
    elif(Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(Name_Print).replace("(Data-Type='mdf'), ", "")]))
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
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
            Bin_Unfolded.Sumw2()
            
            cut_criteria = (0.01*Bin_Acceptance.GetBinContent(Bin_Acceptance.GetMaximumBin()))
            cut_criteria = 0.02
            
            for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
                if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
                    if(Bin_Acceptance.GetBinContent(ii) != 0):
                        print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...\n\t(cut_criteria = ", str(cut_criteria), ")\n\t(Bin_Content  = ", str(Bin_Acceptance.GetBinContent(ii)), ")", color.END]))
                    # Bin_Unfolded.SetBinError(ii,   Bin_Unfolded.GetBinContent(ii) + Bin_Unfolded.GetBinError(ii))
                    Bin_Unfolded.SetBinError(ii,   0)
                    Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BOLD, color.CYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.", color.END]))
            return [Bin_Unfolded, Bin_Acceptance]
        except:
            print("".join([color.BOLD, color.RED, "\nFAILED TO CORRECT A HISTOGRAM (Bin-by-Bin)...", color.END]))
            print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
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
    elif(("RooUnfold" in str(Method)) or (str(Method) in ["Default"])):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))        
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
        
        if(True):
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
            Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle())])
            Response_2D_Input       = Response_2D

        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                # Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, "".join([str(Response_2D.GetName()), "_RooUnfoldResponse_Object"]), Response_2D_Input_Title)
                
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
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################
                    Reg_Par = 13
                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################

                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)

                elif("bbb" in str(Method)):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)

                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)

                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print("".join(["\t", color.RED, "Method '",                 color.BOLD,              str(Method),       color.END, color.RED,  "' is unknown/undefined...", color.END]))
                        print("".join(["\t", color.RED, "Defaulting to using the ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.RED,  " method to unfold...",      color.END]))
                    else:
                        print("".join(["\t", color.CYAN, "Using ",                  color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " method to unfold...",      color.END]))
                        
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = (10 if(not Closure_Test) else 10) if(("Multi_Dim" not in str(Name_Main)) or ("Multi_Dim_z_pT_Bin" in str(Name_Main))) else 4
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
                        # Unfolded_Histo.SetBinError(bin_rec,          Unfolded_Histo.GetBinContent(bin_rec)        + Unfolded_Histo.GetBinError(bin_rec))
                        Unfolded_Histo.SetBinError(bin_rec,          0)
                        Unfolded_Histo.SetBinContent(bin_rec,        0)
                        
                Bin_Acceptance = MC_REC_1D.Clone()
                Bin_Acceptance.Sumw2()
                Bin_Acceptance.Divide(MC_GEN_1D)
                for bin_acceptance in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
                    if(Bin_Acceptance.GetBinContent(bin_acceptance) < 0.02):
                        # Unfolded_Histo.SetBinError(bin_acceptance,   Unfolded_Histo.GetBinContent(bin_acceptance) + Unfolded_Histo.GetBinError(bin_acceptance))
                        Unfolded_Histo.SetBinError(bin_acceptance,   0)
                        Unfolded_Histo.SetBinContent(bin_acceptance, 0)
                        
                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print("".join([color.BOLD, color.CYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return [Unfolded_Histo, Response_RooUnfold]

                        
            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (RooUnfold)...",    color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc()), color.END]))
                
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
    
    print("".join([color.RED, color.BOLD, "\nERROR: DID NOT RETURN A HISTOGRAM YET...\n", color.END]))
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
    
    return Name_Output

######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default", Special="Normal"):
    if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true"]) and (Fitting in ["default", "Default"]) and Fit_Test):
        # if(Method in ["bayes", "bayesian", "Bayesian"]):
        #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSpecial =", str(Special), "\nMethod =", str(Method), "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if(not extra_function_terms):
            A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
        else:
            # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(Histo_To_Fit)
            # fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)) + [E]*cos(4*x*(3.1415926/180)))"
            A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"
            
        Fitting_Function = ROOT.TF1("".join(["Fitting_Function", str(Method).replace(" ", "_")]), str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")
        
        # if(not extra_function_terms):
        #     print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]), color.END)
        # else:
        if(extra_function_terms):
            # print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold), str(E_Unfold)]), color.END)
            print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold)]), color.END)
            Fitting_Function.SetParName(3, "Parameter D")
            # Fitting_Function.SetParName(4, "Parameter E")
            
            
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
            if("Error" not in [A_Unfold, B_Unfold, C_Unfold] or False):
                # This is the constant scaling factor - A (should basically always be positive)
                Fitting_Function.SetParameter(0,      abs(A_Unfold))
                # Fitting_Function.SetParLimits(0, 0.95*abs(A_Unfold), 1.05*abs(A_Unfold))
                Fitting_Function.SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                # Fitting_Function.SetParLimits(1, B_Unfold - 0.05*abs(B_Unfold), B_Unfold + 0.05*abs(B_Unfold))
                Fitting_Function.SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                # Fitting_Function.SetParLimits(2, C_Unfold - 0.05*abs(C_Unfold), C_Unfold + 0.05*abs(C_Unfold))
                Fitting_Function.SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))

                if(extra_function_terms):
                    try:
                        Fitting_Function.SetParameter(3, D_Unfold)
                        Fitting_Function.SetParLimits(3, D_Unfold - 5.5*abs(D_Unfold), D_Unfold + 5.5*abs(D_Unfold))

                        # Fitting_Function.SetParameter(4, E_Unfold)
                        # Fitting_Function.SetParLimits(4, E_Unfold - 5.5*abs(E_Unfold), E_Unfold + 5.5*abs(E_Unfold))
                    except:
                        print("".join([color.RED, color.BOLD, "Fitting_Function ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
                        
                if((str(Special) not in ["Normal"]) and (str(type(Special)) not in [str(type("Normal"))]) and (not Closure_Test)):
                    try:
                        Q2_y_Bin_Special, z_pT_Bin_Special = Special
                        if(Method in ["bayes", "bayesian", "Bayesian", "bay", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                        # if(Method in ["bayes", "bayesian", "Bayesian"]):
                            if(str(Q2_y_Bin_Special) in ["5"]):
                                # print("\n\n\n\nAPPLYING SPECIAL PARAMETERS FOR:\nQ2_y_Bin_Special =", str(Q2_y_Bin_Special), "\nz_pT_Bin_Special =", str(z_pT_Bin_Special), "\n\n\n")
                                if(str(z_pT_Bin_Special) in ["26", "32"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.08)
                                    Fitting_Function.SetParLimits(1, -0.10, -0.065)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["8"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.07)
                                    Fitting_Function.SetParLimits(1, -0.08, -0.06)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["14"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.085)
                                    Fitting_Function.SetParLimits(1, -0.125, -0.05)
                                    
                                if(str(z_pT_Bin_Special) in ["9"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.10)
                                    Fitting_Function.SetParLimits(1, -0.145, -0.065)
                                    Allow_Multiple_Fits = False
                                    
                                   
                                # Just Cos(2*phi) Moments - C
                                if(str(z_pT_Bin_Special) in ["1", "7", "13", "19", "25", "31"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.025)
                                    # Fitting_Function.SetParLimits(2, -0.06, 0)
                                    Fitting_Function.SetParLimits(2, -0.06, -0.01)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["2", "8", "14", "20", "26", "32"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.02 if(str(z_pT_Bin_Special) not in ["2"]) else 0.01)
                                    if(str(z_pT_Bin_Special) in ["2", "8"]):
                                        Fitting_Function.SetParLimits(2, -0.01, 0.05)                                        
                                    else:
                                        Fitting_Function.SetParLimits(2, -0.04, 0.02)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["3", "9", "15", "21", "27", "33"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.01)
                                    # Fitting_Function.SetParLimits(2, -0.03, 0.03)
                                    Fitting_Function.SetParLimits(2, -0.03, 0.01)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["4"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0)
                                    # Fitting_Function.SetParLimits(2, -0.01, 0.025)
                                    Fitting_Function.SetParLimits(2, -0.01, 0.01)
                                    Allow_Multiple_Fits_C = False
                                    
                                    
                                if(str(z_pT_Bin_Special) in ["2"]):
                                    # Cos(phi) Moment - B
                                    # Fitting_Function.SetParameter(1, -0.1062)
                                    # # Fitting_Function.SetParLimits(1, -0.1062   - 0.005,    -0.1062 + 0.005)
                                    # Fitting_Function.SetParLimits(1, -0.125, -0.05)
                                    Fitting_Function.SetParameter(1, -0.1)
                                    Fitting_Function.SetParLimits(1, -0.105, -0.08)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.01945)
                                    Fitting_Function.SetParLimits(2, 0.01945   - 0.06,     0.01945 + 0.06)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["3"]):
                                    # # Cos(phi) Moment - B
                                    # Fitting_Function.SetParameter(1, -0.2175)
                                    # # Fitting_Function.SetParLimits(1, -0.2175   - 0.05,     -0.2175 + 0.05)
                                    # Fitting_Function.SetParLimits(1, -0.2175   - 0.025,     -0.2175 + 0.025)
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.1375)
                                    Fitting_Function.SetParLimits(1, -0.1, -0.16)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.001952)
                                    Fitting_Function.SetParLimits(2, 0.001952  - 0.003,   0.001952 + 0.003)
                                if(str(z_pT_Bin_Special) in ["4"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.195)
                                    Fitting_Function.SetParLimits(1, -0.18, -0.22)
                                if(str(z_pT_Bin_Special) in ["5"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.24)
                                    Fitting_Function.SetParLimits(1, -0.2, -0.3)
                                if(str(z_pT_Bin_Special) in ["6", "12", "18"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.35)
                                    Fitting_Function.SetParLimits(1, -0.35     - 0.5,        -0.35 + 0.5)
                                if(str(z_pT_Bin_Special) in ["13"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.027)
                                    Fitting_Function.SetParLimits(1, -0.09, 0)
                                if(str(z_pT_Bin_Special) in ["20"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.04262)
                                    # Fitting_Function.SetParLimits(1, -0.04262  - 0.02,    -0.04262 + 0.02)
                                    Fitting_Function.SetParLimits(1, -0.04262  - 0.005,    -0.04262 + 0.01)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.001472)
                                    Fitting_Function.SetParLimits(2, -0.001472 - 0.003,  -0.001472 + 0.003)
                                    
                                    # Fitting_Function.SetRange(30, 330)
                                    
                                if(str(z_pT_Bin_Special) in ["29"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.19)
                                    Fitting_Function.SetParLimits(1, -0.19     - 0.5,        -0.19 + 0.5)
                                if(str(z_pT_Bin_Special) in ["35"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.25)
                                    Fitting_Function.SetParLimits(1, -0.30, -0.175)
                                    Allow_Multiple_Fits = False
                                    
                                    
                            if(str(Q2_y_Bin_Special) in ["1"]):
                                if(str(z_pT_Bin_Special) in ["14", "21"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.3)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.275)
                            if(str(Q2_y_Bin_Special) in ["2"]):
                                if(str(z_pT_Bin_Special) in ["7", "14", "21"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.3)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.275)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.1)
                                    Fitting_Function.SetParLimits(2, 0.06, 0.2)
                            if(str(Q2_y_Bin_Special) in ["10"]):
                                if(str(z_pT_Bin_Special) in ["6", "12", "18", "24"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.275)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.2)
                            if(str(Q2_y_Bin_Special) in ["14"]):
                                if(str(z_pT_Bin_Special) in ["2"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.1)
                                    Fitting_Function.SetParLimits(1, -0.12, -0.02)
                                if(str(z_pT_Bin_Special) in ["20"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.25)
                                    Fitting_Function.SetParLimits(1, -0.3, -0.2)
                                
                                    
                    except:
                        print(color.Error, "\nERROR in Fitting_Phi_Function() for 'Special' arguement...", color.END)
                        print(color.BOLD,  "Traceback:\n", str(traceback.format_exc()), color.END, "\n")

            # else:
            #     print(color.RED, color.BOLD, "\nFIXING PARAMETERS FOR TESTING\n", color.END)
            #     Fitting_Function= ROOT.TF1("".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_")]), "[A]", 0, 360)
            #     # Fitting_Function.SetRange(0, 360)
            #     # This is the constant scaling factor - A
            #     Fitting_Function.SetParameter(0, 0.50*abs(Histo_To_Fit.GetMaximum))
            #     Fitting_Function.SetParLimits(0, 0.45*abs(Histo_To_Fit.GetMaximum), 0.55*abs(Histo_To_Fit.GetMaximum))
            
                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "QRB")
            else:
                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "QR")

            A_Unfold = Fitting_Function.GetParameter(0)
            B_Unfold = Fitting_Function.GetParameter(1)
            C_Unfold = Fitting_Function.GetParameter(2)
            

            # Re-fitting with the new parameters
            # The constant scaling factor - A
            Fitting_Function.SetParameter(0,     abs(A_Unfold))
            Fitting_Function.SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
            
            # Allow_Multiple_Fits = True
            if(Allow_Multiple_Fits):
                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
            else:
                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - Fitting_Function.GetParError(1), B_Unfold + Fitting_Function.GetParError(1))
                
            # Allow_Multiple_Fits_C = True
            if(Allow_Multiple_Fits_C):
                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))
            else:
                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - Fitting_Function.GetParError(2), C_Unfold + Fitting_Function.GetParError(2))

            if(extra_function_terms):
                D_Unfold = Fitting_Function.GetParameter(3)
                # E_Unfold = Fitting_Function.GetParameter(4)
                # Cos(3*phi) Moment - D
                Fitting_Function.SetParameter(3, D_Unfold)
                Fitting_Function.SetParLimits(3, D_Unfold - 0.5*abs(D_Unfold), D_Unfold + 0.5*abs(D_Unfold))
                # # Cos(4*phi) Moment - E
                # Fitting_Function.SetParameter(4, E_Unfold)
                # Fitting_Function.SetParLimits(4, E_Unfold - 0.5*abs(E_Unfold), E_Unfold + 0.5*abs(E_Unfold))

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
            print("".join([color.Error, "ERROR IN FITTING:\n", color.END, str(traceback.format_exc()), "\n"]))
            Out_Put = [Histo_To_Fit, "Fitting_Function",  ["Fit_Chisquared", "Fit_ndf"], ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        
        return Out_Put
    else:
        print("\n\n\nERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...\n\n\n")
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
            print(color.RED, color.BOLD, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
    else:
        print(color.RED, color.BOLD, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
        return "Error"
    
    try:
        Output_Histos, Output_Canvas = {}, {}

        
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("Combined_" not in str(Name) and "Multi_Dim" not in str(Name)):
                print(color.RED, "ERROR: WRONG TYPE OF HISTOGRAM\nName =", color.END, Name)
                print("MultiD_Slice() should be used on 1D histograms with the 'Combined_' or 'Multi_Dim_' bin variable\n\n")
                return "Error"
            # if(("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_y_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_phi_t_smeared'" not in str(Name)) and (("'Combined_phi_t_Q2" not in str(Name).replace("_smeared", "") and "'Combined_phi_t_Q2_smeared'" not in str(Name)))):
            #     print("ERROR in MultiD_Slice(): Not set up for other variables (yet)")
            #     print("Name =", Name, "\n\n")
            #     return "Error"

        # if(Variable not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t_smeared"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t_smeared"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method), "_smeared"]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method), "_smeared"])]):
        if(str(Variable).replace("_smeared", "") not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Combined_phi_t_Q2", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "Multi_Dim_elth_phi_t", "Multi_Dim_pipth_phi_t", "Multi_Dim_elPhi_phi_t", "Multi_Dim_pipPhi_phi_t"]):
            print(color.RED, "ERROR in MultiD_Slice(): Not set up for other variables (yet)", color.END)
            print("Variable =", Variable, "\n\n")
            return "Error"

        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
            
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not Sim_Test) else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
            # if((Sim_Test) and ("_smeared" not in str(Variable)) and (Smear in [""])):
            #     Variable = "".join([str(Variable), "_smeared"])
            #     Smear = "Smear"
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
        if(Method in ["Acceptance"]):
            Method_Title = "".join(["(", str(root_color.Bold),  "{Acceptance})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###


        if(Title == "Default"):
            Title = str(Histo.GetTitle())
        elif(Title in ["norm", "standard"]):
            Title = "".join(["#splitline{", str(root_color.Bold), "{Multi-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{Multi_Dim_Var_Info}"])
            
            
        if(not extra_function_terms):
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        else:
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
            
            # fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}) + E Cos(4#phi_{h}))"

        
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
            
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
            

        #######################################################################
        #####==========#####   Setting Variable Binning    #####==========#####
        #######################################################################
                               # ['min',  'max',   'num_bins', 'size']
        Q2_Binning             = [1.4805, 11.8705, 20,         0.5195]
        Q2_xB_Binning          = [0,      8,       8,          1]
        # Q2_y_Binning         = [0,      18,      18,         1]
        Q2_y_Binning           = [-0.5,   18.5,    19,         1]
        
        z_pT_Binning           = [-0.5,   42.5,    43,         1]
        
        if("Y_bin" in str(Binning_Method)):
            z_pT_Binning       = [-1.5,   50.5,    52,         1]
        
        # Q2_y_z_pT_4D_Binning   = [-0.5,   566.5,   567,        1]
        # Q2_y_z_pT_4D_Binning   = [-0.5,   512.5,   513,        1]
        Q2_y_z_pT_4D_Binning   = [-0.5,   506.5,   507,        1]
        
        particle_Th__Binning   = [5,  35, 30,  1]
        particle_Phi_Binning   = [0, 360, 24, 15]
        
        ###==============================================###
        ###========###  Setting Phi Binning   ###========###
        ###==============================================###
        phi_h_Binning          = [0,      360,     24,         15]
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            # phi_h_Binning      = [0,      360,     12,         30]
            phi_h_Binning      = [0,      360,     10,         36]
        ###==============================================###
        ###========###  Setting Phi Binning   ###========###
        ###==============================================###

        # NewDim_Bin_Min  = Q2_xB_Binning[0]
        # NewDim_Bin_Max  = Q2_xB_Binning[1]
        # NewDim_Bin_Num  = Q2_xB_Binning[2]
        # NewDim_Bin_Size = Q2_xB_Binning[3]
        # Num_Columns_Canvas, Num_Rows_Canvas = 4, 2
        # Multi_Dim_Var  = "Q2_xB"
        
        ###===============================================###
        ###========###  Setting Q2-y Binning   ###========###
        ###===============================================###
        NewDim_Bin_Min  = Q2_y_Binning[0]
        NewDim_Bin_Max  = Q2_y_Binning[1]
        NewDim_Bin_Num  = Q2_y_Binning[2]
        NewDim_Bin_Size = Q2_y_Binning[3]
        Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
        Multi_Dim_Var  = "Q2_y"
        ###===============================================###
        ###========###  Setting Q2-y Binning   ###========###
        ###===============================================###
        
        ###===============================================###
        ###========###  Setting z-pT Binning   ###========###
        ###===============================================###
        if("z_pT_Bin" in Variable):
            NewDim_Bin_Min  = z_pT_Binning[0]
            NewDim_Bin_Max  = z_pT_Binning[1]
            NewDim_Bin_Num  = z_pT_Binning[2]
            NewDim_Bin_Size = z_pT_Binning[3]
            Num_Columns_Canvas, Num_Rows_Canvas = 6, 7
            Multi_Dim_Var  = "z_pT"
        ###===============================================###
        ###========###  Setting z-pT Binning   ###========###
        ###===============================================###
        
        ###===============================================###
        ###========###   Setting Q2 Binning    ###========###
        ###===============================================###
        if(Variable in ["Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared"]):
            NewDim_Bin_Min  = Q2_Binning[0]
            NewDim_Bin_Max  = Q2_Binning[1]
            NewDim_Bin_Num  = Q2_Binning[2]
            NewDim_Bin_Size = Q2_Binning[3]
            Multi_Dim_Var   = "Q2"
            Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
        ###===============================================###
        ###========###   Setting Q2 Binning    ###========###
        ###===============================================###
        
        
        ###===============================================###
        ###========###  Setting Theta Binning  ###========###
        ###===============================================###
        if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elth_phi_t", "Multi_Dim_pipth_phi_t"]):
            NewDim_Bin_Min  = particle_Th__Binning[0]
            NewDim_Bin_Max  = particle_Th__Binning[1]
            NewDim_Bin_Num  = particle_Th__Binning[2]
            NewDim_Bin_Size = particle_Th__Binning[3]
            Multi_Dim_Var   = "elth" if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elth_phi_t"]) else "pipth"
            Num_Columns_Canvas, Num_Rows_Canvas = 6, 6
        ###===============================================###
        ###========###  Setting Theta Binning  ###========###
        ###===============================================###
        
        
        ###===============================================###
        ###========###   Setting Phi Binning   ###========###
        ###===============================================###
        if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elPhi_phi_t", "Multi_Dim_pipPhi_phi_t"]):
            NewDim_Bin_Min  = particle_Phi_Binning[0]
            NewDim_Bin_Max  = particle_Phi_Binning[1]
            NewDim_Bin_Num  = particle_Phi_Binning[2]
            NewDim_Bin_Size = particle_Phi_Binning[3]
            Multi_Dim_Var   = "elPhi" if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elPhi_phi_t"]) else "pipPhi"
            Num_Columns_Canvas, Num_Rows_Canvas = 5, 5
        ###===============================================###
        ###========###   Setting Phi Binning   ###========###
        ###===============================================###
            
        Canvas_Size_X = 2400
        Canvas_Size_Y = 1200 if(Num_Rows_Canvas < 3) else 2400
        
        ###===============================================###
        ###========###   Setting 4D Binning    ###========###
        ###===============================================###
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            NewDim_Bin_Min  = Q2_y_z_pT_4D_Binning[0]
            NewDim_Bin_Max  = Q2_y_z_pT_4D_Binning[1]
            NewDim_Bin_Num  = Q2_y_z_pT_4D_Binning[2]
            NewDim_Bin_Size = Q2_y_z_pT_4D_Binning[3]
            Num_Columns_Canvas, Num_Rows_Canvas = 24, 24
            Multi_Dim_Var   = "Q2_y_z_pT"
            Canvas_Size_X   = 4800
            Canvas_Size_Y   = 4800
        ###===============================================###
        ###========###   Setting 4D Binning    ###========###
        ###===============================================###
        
        #######################################################################
        #####==========#####   Setting Variable Binning    #####==========#####
        #######################################################################
        
        
        
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="Multi-Dim Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="Multi_Dim_Q2_y_Bin_Info", z_pT_Bin="Multi_Dim_z_pT_Bin_Info", Bin_Extra="Multi_Dim_Bin_Info" if(Multi_Dim_Var not in ["Q2_xB", "Q2_y", "z_pT"]) else "Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BOLD, color.BLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END]))
                # print("Name =", Name)
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BOLD, color.BLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END]))
            #     print("Name =", Name, "\n")
            
        if(str(Multi_Dim_Var) in ["z_pT"]):
            Name = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All"))
            
        Output_Canvas = Canvas_Create(Name, Num_Columns=Num_Columns_Canvas, Num_Rows=Num_Rows_Canvas, Size_X=Canvas_Size_X, Size_Y=Canvas_Size_Y, cd_Space=0)
        
        bin_ii = 1 # 0 # if(Common_Name not in ["New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"]) else 1
        # for NewDim_Bin in range(0, NewDim_Bin_Num + 1, 1):
        for NewDim_Bin in range(0, NewDim_Bin_Num - 1, 1):
            # if(NewDim_Bin != 0 and (Common_Name not in ["Multi_Dimension_Unfold_V3_All", "New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"])):
            #     bin_ii  += -1
            
            if(str(Multi_Dim_Var) in ["Q2_xB", "Q2_y"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(NewDim_Bin)))
                Name_Out = str(Name_Out.replace("Multi_Dim_z_pT_Bin_Info", "All"))
            elif(str(Multi_Dim_Var) in ["z_pT"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(Q2_y_Bin_Select not in [0, "0"]) else "All"))
                Name_Out = str(Name_Out.replace("Multi_Dim_z_pT_Bin_Info", str(NewDim_Bin)))
                z_pT_Bin_Range = 42 if(str(Q2_y_Bin_Select) in ["2"]) else 36 if(str(Q2_y_Bin_Select) in ["4", "5", "9", "10"]) else 35 if(str(Q2_y_Bin_Select) in ["1", "3"]) else 30 if(str(Q2_y_Bin_Select) in ["6", "7", "8", "11"]) else 25 if(str(Q2_y_Bin_Select) in ["13", "14"]) else 20 if(str(Q2_y_Bin_Select) in ["12", "15", "16", "17"]) else 1
                if("Y_bin" in Binning_Method):
                    z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Select)[1] - 1
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
                
            #######################################################################
            #####==========#####   Filling Sliced Histogram    #####==========#####
            #######################################################################
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
                    Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],  Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), Multi_Dim_phi_err)
                    bin_ii += 1
                else:
                    ii_bin_num += 1
                    bin_jj = Histo.FindBin(bin_ii)
                    Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                    Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                    Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],  Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), Multi_Dim_phi_err)
                    bin_ii += 1
            #######################################################################
            #####==========#####   Filling Sliced Histogram    #####==========#####
            #######################################################################

            #######################################################################
            #####==========#####   Drawing Histogram/Canvas    #####==========#####
            #######################################################################
            Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
            # Output_Histos[Name_Out].Draw("same HIST text E0")
            Output_Histos[Name_Out].Draw("same HIST E0")
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
            #######################################################################
            #####==========#####   Drawing Histogram/Canvas    #####==========#####
            #######################################################################
            
            
            Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
            
            configure_stat_box(hist=Output_Histos[Name_Out], show_entries=True, canvas=Output_Canvas)
            # Output_Canvas.Modified()
            # Output_Canvas.Update()
            
            
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            if(Fitting_Input in ["default", "Default"] and Fit_Test):
                # Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("Multi-Dim Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting=Fitting_Input)
                Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("Multi-Dim Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[Q2_y_Bin_Select, NewDim_Bin] if(str(Multi_Dim_Var) in ["z_pT"]) else "Normal") # Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out])
                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                # Histo_To_Fit.Draw("same HIST text E0")
                Output_Histos[Name_Out].Draw("same HIST E0")
                Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")].Draw("same")

                statbox_move(Histogram=Output_Histos[Name_Out], Canvas=Output_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            elif(not Fit_Test):
                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                Output_Histos[Name_Out].Draw("same HIST E0")
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            
            
            Output_Canvas.Modified()
            Output_Canvas.Update()
            
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        
        
        ######################################################################
        #####==========#####        Saving Canvas         #####==========#####
        ######################################################################
        Save_Name = "".join(["Multi_Dim_Histo_", str(Variable).replace("_smeared", ""), "_Q2_y_Bin_", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All", "_", str(Method) if(Method not in ["N/A"]) else "", "_Smeared" if("mear" in Smear) else "", str(File_Save_Format)]).replace(" ", "_")
        Save_Name = str((Save_Name.replace("-", "_")).replace("phi_t_", "phi_h_")).replace("__", "_")
        
        Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
        
        Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
        
        if(((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"])) and (extra_function_terms and "phi_h" in str(Save_Name))):
            Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
        
        if(("y_bin" in str(Binning_Method)) or ("Y_bin" in str(Binning_Method))):
            Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
        if(Sim_Test):
            Save_Name = "".join(["Sim_Test_", Save_Name])
            
            
        Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                      "Q2_y_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                "z_pT_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                "z_pT_phi_h")
        Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]), str(File_Save_Format))
        Save_Name = Save_Name.replace("__",                                  "_")
        # if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas", "complete", "Complete"])):
        # if(Saving_Q and ("Acceptance" not in Method)):
        if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save"])):
            if("root" in str(File_Save_Format)):
                Output_Canvas.SetName(Save_Name.replace(".root", ""))
            Output_Canvas.SaveAs(Save_Name)
        # print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method)) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
        # print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save", "Canvas", "canvas"])) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
        print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save"])) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
        ######################################################################
        #####==========#####        Saving Canvas         #####==========#####
        ######################################################################
        
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
            if(Out_Option in ["all", "All", "Canvas", "canvas"]):
                Output_List.append(Output_Canvas)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    
    except:
        print("".join([color.Error, "MultiD_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##           Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def New_Version_of_File_Creation(Histogram_List_All, Out_Print_Main, Response_2D="", ExREAL_1D="", MC_REC_1D="", MC_GEN_1D="", ExTRUE_1D="N/A", Smear_Input="", Q2_Y_Bin="All", Z_PT_Bin="All", MC_BGS_1D="None"):
    try:
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################
        if("Response" not in str(Out_Print_Main)):
            print(color.Error, "\n\n\nERROR IN New_Version_of_File_Creation()...\nThis function is meant to just handle the 'Response_Matrix' Histograms (for Unfolding)\nFlawed Input was:", str(Out_Print_Main), color.END, "\n\n")
            return Histogram_List_All
        if(type(Histogram_List_All) is not dict):
            print(color.Error, "\n\n\nERROR IN New_Version_of_File_Creation()...\nThis function requires that 'Histogram_List_All' be set as a dict to properly handle the outputs\nFlawed Input was:\nHistogram_List_All =", str(Histogram_List_All), color.END, "\n\n")
            return Histogram_List_All
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################

        Variable_Input = Histogram_Name_Def(Out_Print_Main, Variable="FindAll")
        # print("Variable_Input =", Variable_Input)
        Allow_Fitting  = "phi_t" in str(Variable_Input)

        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        try:
            Bin_Method_Histograms        = Unfold_Function(Response_2D,  ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D)
            Bin_Unfolded, Bin_Acceptance = Bin_Method_Histograms
        except:
            print("".join([color.BOLD,     color.RED, "ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

        try:
            RooUnfolded_Bayes_Histos     = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes", MC_BGS_1D=MC_BGS_1D))[0]
        except:
            print("".join([color.BOLD,     color.RED, "ERROR IN RooUnfold Bayesian METHOD:\n",               color.END, color.RED, str(traceback.format_exc()), color.END]))

        if("Multi_Dim" not in str(Variable_Input)):
            try:
                RooUnfolded_SVD_Histos   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd",   MC_BGS_1D=MC_BGS_1D))[0]
            except:
                print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold SVD METHOD:\n",                    color.END, color.RED, str(traceback.format_exc()), color.END]))

        # try:
        #     RooUnfolded_BinByBin_Histos  = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bbb"))[0]
        # except:
        #     print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold Bin-by-Bin METHOD:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################


        #####==========#####      Multi_Dim Histos       #####==========#####
        if(("Multi_Dim" in str(Variable_Input))   and (Z_PT_Bin in ["All", 0])):
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
                if(ExTRUE_1D not in ["N/A"]):
                    if(Fit_Test and Allow_Fitting):
                        Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = MultiD_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                    else:
                        Multi_Dim_ExTRUE_1D                                                                                          = MultiD_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###
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
        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========#####      Fitting 1D Histo       #####==========#####
        elif("phi" in Variable_Input):
            if(Fit_Test and Allow_Fitting):
                MC_GEN_1D,                   Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=MC_GEN_1D,                Method="gdf",   Special=[Q2_Y_Bin, Z_PT_Bin])
                Bin_Unfolded,                Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Bin_Unfolded,             Method="bbb",   Special=[Q2_Y_Bin, Z_PT_Bin])
                RooUnfolded_Bayes_Histos,    Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_Bayes_Histos, Method="bayes", Special=[Q2_Y_Bin, Z_PT_Bin])
                if("Multi_Dim" not in str(Variable_Input)):
                    RooUnfolded_SVD_Histos,  Unfolded_SVD_Fit_Function, Chi_Squared_SVD, SVD_Fit_Par_A, SVD_Fit_Par_B, SVD_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_SVD_Histos,   Method="SVD",   Special=[Q2_Y_Bin, Z_PT_Bin])
                if(ExTRUE_1D not in ["N/A"]):
                    ExTRUE_1D,               Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=ExTRUE_1D,                Method="tdf",   Special=[Q2_Y_Bin, Z_PT_Bin])
        #####==========#####      Fitting 1D Histo       #####==========#####


        ##################################################################################
        ###==============###==========================================###==============###
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ###==============###==========================================###==============###
        ##################################################################################
        Histo_Name_General = Histogram_Name_Def(out_print=Out_Print_Main, Histo_General="1D", Data_Type="METHOD", Cut_Type="Skip", Smear_Type=Smear_Input, Q2_y_Bin=Q2_Y_Bin, z_pT_Bin=Z_PT_Bin, Bin_Extra="Default", Variable=Variable_Input)
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "rdf")).replace("Smear", "''")]            = ExREAL_1D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf"))]                                   = MC_REC_1D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")]  = Response_2D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "gdf")).replace("Smear", "''")]            = MC_GEN_1D

        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin"))]                                   = Bin_Unfolded
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Acceptance"))]                            = Bin_Acceptance
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian"))]                              = RooUnfolded_Bayes_Histos
        if("Multi_Dim" not in str(Variable_Input)):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD"))]                                   = RooUnfolded_SVD_Histos
            if(Fit_Test and Allow_Fitting):
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Function")] = Unfolded_SVD_Fit_Function
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Chi_Squared")]  = Chi_Squared_SVD
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_A")]    = SVD_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_B")]    = SVD_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_C")]    = SVD_Fit_Par_C
        if(ExTRUE_1D not in ["N/A"]):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf"))]                                   = ExTRUE_1D
            if(Fit_Test and Allow_Fitting):
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function")] = Unfolded_TDF_Fit_Function
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Chi_Squared")]  = Chi_Squared_TDF
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_A")]    = TDF_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_B")]    = TDF_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_C")]    = TDF_Fit_Par_C
                
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Multi_Dim Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        if(("Multi_Dim" in str(Variable_Input))   and (Z_PT_Bin in ["All", 0])):
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

                try:
                    for histos_list in histos_list_loop:
                        try:
                            for name in histos_list:
                                Histogram_List_All[name] = histos_list[name]
                        except:
                            print("".join([color.Error, "ERROR IN ADDING TO Histogram_List_All (while looping within an item in histos_list):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            print("histos_list =", histos_list)
                            # print("histos_list_loop =", histos_list_loop)
                except:
                    print("".join([color.BOLD,         color.RED, "ERROR IN ADDING TO Histogram_List_All (while looping through items in histos_list):\n",  color.END, color.RED, str(traceback.format_exc()), color.END]))
        ###==========###         Multi_Dim Histos          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        elif("phi" in Variable_Input):
            if(Fit_Test and Allow_Fitting):
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")).replace("Smear", "''")] = Unfolded_GEN_Fit_Function
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Chi_Squared")).replace("Smear", "''")]  = Chi_Squared_GEN
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_A")).replace("Smear", "''")]    = GEN_Fit_Par_A
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_B")).replace("Smear", "''")]    = GEN_Fit_Par_B
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_C")).replace("Smear", "''")]    = GEN_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Function")]                         = Unfolded_Bin_Fit_Function
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Chi_Squared")]                          = Chi_Squared_Bin
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_A")]                            = Bin_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_B")]                            = Bin_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_C")]                            = Bin_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Function")]                         = Unfolded_Bay_Fit_Function
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
        print("".join([color.BOLD, color.RED, "ERROR IN New_Version_of_File_Creation(...):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
        return Histogram_List_All
    
################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################










######################################################################################################################################################
##==========##==========## (New) Simple Function for Drawing 2D Histograms  ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################

def Draw_2D_Histograms_Simple_New(Histogram_List_All_Input, Canvas_Input=[], Default_Histo_Name_Input="", Q2_Y_Bin_Input="All", Z_PT_Bin_Input="All", String_Output=""):
    
    Name_Uses_MultiDim = ("(Multi-Dim Histo)" in str(Default_Histo_Name_Input))
    
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(1D)",              "(Normal_2D)")
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(Multi-Dim Histo)", "(Normal_2D)")
    
    Variable = "(phi_t)" if("(phi_t)" in Default_Histo_Name_Input) else "(Q2)" if("(Q2)" in Default_Histo_Name_Input) else "(xB)" if("(xB)" in Default_Histo_Name_Input) else "(z)" if("(z)" in Default_Histo_Name_Input) else "(pT)" if("(pT)" in Default_Histo_Name_Input) else "(y)" if("(y)" in Default_Histo_Name_Input) else "(MM)"
    
    # Q2_y__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    # z_pT__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    # Q2_xB_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    Q2_y__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    z_pT__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    Q2_xB_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear",  "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    Q2_y_Histo_rdf_Initial   = Histogram_List_All_Input[str(Q2_y__Histo_rdf_Initial_Name)]
    z_pT_Histo_rdf_Initial   = Histogram_List_All_Input[str(z_pT__Histo_rdf_Initial_Name)]
    Q2_xB_Histo_rdf_Initial  = Histogram_List_All_Input[str(Q2_xB_Histo_rdf_Initial_Name)]
    
    Q2_y__Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear", "''")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    z_pT__Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear", "''")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    Q2_xB_Histo_mdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear", "''")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    Q2_y_Histo_mdf_Initial   = Histogram_List_All_Input[str(Q2_y__Histo_mdf_Initial_Name)]
    z_pT_Histo_mdf_Initial   = Histogram_List_All_Input[str(z_pT__Histo_mdf_Initial_Name)]
    Q2_xB_Histo_mdf_Initial  = Histogram_List_All_Input[str(Q2_xB_Histo_mdf_Initial_Name)]
    
    # elth__Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),    "(el)_(elth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    # elPhi_Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),   "(el)_(elPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    elth__Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),    "(el)_(elth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    elPhi_Histo_rdf_Initial_Name  = str(str(str(Default_Histo_Name_Input.replace(str(Variable),   "(el)_(elPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    elth_Histo_rdf_Initial   = Histogram_List_All_Input[str(elth__Histo_rdf_Initial_Name)]
    elPhi_Histo_rdf_Initial  = Histogram_List_All_Input[str(elPhi_Histo_rdf_Initial_Name)]
    
    # pipth__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),  "(pip)_(pipth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    # pipPhi_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable), "(pip)_(pipPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")).replace("(1D)", "(Normal_2D)")
    pipth__Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable),  "(pip)_(pipth)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    pipPhi_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name_Input.replace(str(Variable), "(pip)_(pipPhi)")).replace("Smear", "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")
    pipth_Histo_rdf_Initial  = Histogram_List_All_Input[str(pipth__Histo_rdf_Initial_Name)]
    pipPhi_Histo_rdf_Initial = Histogram_List_All_Input[str(pipPhi_Histo_rdf_Initial_Name)]
    
    # Q2_y_Histo__mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),           "(Q2)_(y)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    # Q2_xB_Histo_mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),          "(Q2)_(xB)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    # z_pT_Histo__mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),           "(z)_(pT)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    # Q2_y_Histo_mdf_Initial   = Histogram_List_All_Input[str(Q2_y_Histo__mdf_Initial_Name)]
    # Q2_xB_Histo_mdf_Initial  = Histogram_List_All_Input[str(Q2_xB_Histo_mdf_Initial_Name)]
    # z_pT_Histo_mdf_Initial   = Histogram_List_All_Input[str(z_pT_Histo__mdf_Initial_Name)]
    
    elth__Histo_mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),        "(el)_(elth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    elPhi_Histo_mdf_Initial_Name  = str(str(Default_Histo_Name_Input.replace(str(Variable),       "(el)_(elPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    elth_Histo_mdf_Initial   = Histogram_List_All_Input[str(elth__Histo_mdf_Initial_Name)]
    elPhi_Histo_mdf_Initial  = Histogram_List_All_Input[str(elPhi_Histo_mdf_Initial_Name)]
        
    pipth__Histo_mdf_Initial_Name = str(str(Default_Histo_Name_Input.replace(str(Variable),      "(pip)_(pipth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    pipPhi_Histo_mdf_Initial_Name = str(str(Default_Histo_Name_Input.replace(str(Variable),     "(pip)_(pipPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")
    pipth_Histo_mdf_Initial  = Histogram_List_All_Input[str(pipth__Histo_mdf_Initial_Name)]
    pipPhi_Histo_mdf_Initial = Histogram_List_All_Input[str(pipPhi_Histo_mdf_Initial_Name)]
    
    Bin_Title     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin_Input) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin_Input), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ["All", "0"]) else "All"]), "}}}"])
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])
    
    
    
    
    Drawing_Histo_Set = {}
    # for Drawing_Histo_Found in [Q2_y_Histo_rdf_Initial, Q2_xB_Histo_rdf_Initial, z_pT_Histo_rdf_Initial, elth_Histo_rdf_Initial, elPhi_Histo_rdf_Initial, pipth_Histo_rdf_Initial, pipPhi_Histo_rdf_Initial, elth_Histo_mdf_Initial, elPhi_Histo_mdf_Initial, pipth_Histo_mdf_Initial, pipPhi_Histo_mdf_Initial]:
    # for Drawing_Histo_Found in [Q2_y_Histo_rdf_Initial, Q2_xB_Histo_rdf_Initial, z_pT_Histo_rdf_Initial, Q2_y_Histo_mdf_Initial, z_pT_Histo_mdf_Initial, Q2_xB_Histo_mdf_Initial, elth_Histo_rdf_Initial, elPhi_Histo_rdf_Initial, pipth_Histo_rdf_Initial, pipPhi_Histo_rdf_Initial, elth_Histo_mdf_Initial, elPhi_Histo_mdf_Initial, pipth_Histo_mdf_Initial, pipPhi_Histo_mdf_Initial]:
    for Drawing_Histo_Found_and_Name in [[Q2_y_Histo_rdf_Initial,   Q2_y__Histo_rdf_Initial_Name], [z_pT_Histo_rdf_Initial,   z_pT__Histo_rdf_Initial_Name], [Q2_xB_Histo_rdf_Initial,  Q2_xB_Histo_rdf_Initial_Name], [Q2_y_Histo_mdf_Initial,   Q2_y__Histo_mdf_Initial_Name], [z_pT_Histo_mdf_Initial,   z_pT__Histo_mdf_Initial_Name], [Q2_xB_Histo_mdf_Initial,  Q2_xB_Histo_mdf_Initial_Name], [elth_Histo_rdf_Initial,   elth__Histo_rdf_Initial_Name], [elPhi_Histo_rdf_Initial,  elPhi_Histo_rdf_Initial_Name], [pipth_Histo_rdf_Initial,  pipth__Histo_rdf_Initial_Name], [pipPhi_Histo_rdf_Initial, pipPhi_Histo_rdf_Initial_Name], [elth_Histo_mdf_Initial,   elth__Histo_mdf_Initial_Name], [elPhi_Histo_mdf_Initial,  elPhi_Histo_mdf_Initial_Name], [pipth_Histo_mdf_Initial,  pipth__Histo_mdf_Initial_Name], [pipPhi_Histo_mdf_Initial, pipPhi_Histo_mdf_Initial_Name]]:
        Drawing_Histo_Found, Drawing_Histo_Name = Drawing_Histo_Found_and_Name
        #########################################################
        ##===============##     3D Slices     ##===============##
        if("3D" in str(type(Drawing_Histo_Found))):
            bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input    if(str(Z_PT_Bin_Input) not in ["All", "0"]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(str(Z_PT_Bin_Input) not in ["All", "0"]) else Drawing_Histo_Found.GetNbinsX())
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
            print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
        ##===============##     3D Slices     ##===============##
        #########################################################
        # #########################################################
        # ##===============##     3D Slices     ##===============##
        # if("3D" in str(type(Drawing_Histo_Found))):
        #     bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(Z_PT_Bin_Input not in ["All", 0]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(Z_PT_Bin_Input not in ["All", 0]) else Drawing_Histo_Found.GetNbinsX())
        #     if(Z_PT_Bin_Input not in ["All", 0]):
        #         Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
        #     New_Name = str(Drawing_Histo_Found.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))
        #     Drawing_Histo_Set[New_Name] = Drawing_Histo_Found.Project3D('yz e')
        #     Drawing_Histo_Set[New_Name].SetName(New_Name)
        #     Drawing_Histo_Title = (str(Drawing_Histo_Set[New_Name].GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: ", str(Q2_Y_Bin_Input)]), str(Bin_Title))
        #     Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
        #     if("mdf" in str(Drawing_Histo_Found.GetName())):
        #         Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
        #     Drawing_Histo_Set[New_Name].SetTitle(Drawing_Histo_Title)
        # else:
        #     New_Name = str(Drawing_Histo_Found.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))
        #     Drawing_Histo_Set[New_Name] = Drawing_Histo_Found
        #     if((str(Bin_Title) not in str(Drawing_Histo_Set[New_Name].GetTitle())) and (Standard_Histogram_Title_Addition not in [""])):
        #         Drawing_Histo_Set[New_Name].SetTitle("".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"]))
        #     print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
        # ##===============##     3D Slices     ##===============##
        # #########################################################

    try:
        Canvas_Input_0, Canvas_Input_1, Canvas_Input_2, Canvas_Input_3, Canvas_Input_4 = Canvas_Input
    except:
        try:
            Canvas_Input_0, Canvas_Input_1, Canvas_Input_2, Canvas_Input_3             = Canvas_Input
        except:
            print(color.RED, color.BOLD, "\n\nMajor Error in getting 'Canvas_Input' for the Draw_2D_Histograms_Simple_New() function.\n\n", color.END)
    
    
    Q2_y__Histo_rdf_2D  = str(Q2_y__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    z_pT__Histo_rdf_2D  = str(z_pT__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    Q2_xB_Histo_rdf_2D  = str(Q2_xB_Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    Q2_y__Histo_mdf_2D  = str(Q2_y__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    z_pT__Histo_mdf_2D  = str(z_pT__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    Q2_xB_Histo_mdf_2D  = str(Q2_xB_Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    ##################################################################
    ##===============##     Drawing Histograms     ##===============##
    # Draw_Canvas(canvas=Canvas_Input_1, cd_num=1, left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
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
        for Q2_Y_Bin_ii in range(1, 40, 1):
            Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.Draw("same")
    
    # Draw_Canvas(canvas=Canvas_Input_1, cd_num=2, left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
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
                    # z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT)
                    z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                    z_pT_borders[pTline] = ROOT.TLine()
                    z_pT_borders[pTline].SetLineColor(1)
                    z_pT_borders[pTline].SetLineWidth(2)
                    # z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline)
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
        # Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation="z_pT")
        MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin=Q2_Y_Bin_Input, Plot_Orientation="z_pT")
        for MM_lines in MM_z_pT_borders:
            MM_z_pT_borders[MM_lines].Draw("same")
        MM_z_pT_legend.Draw("same")
    
    
    # Draw_Canvas(canvas=Canvas_Input_2, cd_num=1, left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_2, cd_num=1, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].Draw("colz")
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].SetTitle((Drawing_Histo_Set[str(Q2_xB_Histo_rdf_2D)].GetTitle()).replace("Q^{2}-x_{B} Bin: All" if(("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method))) else "Q^{2}-y Bin: All", str(Bin_Title)))
    Q2_xB_borders, line_num = {}, 0
    for b_lines in Q2_xB_Border_Lines(-1):
        Q2_xB_borders[line_num] = ROOT.TLine()
        Q2_xB_borders[line_num].SetLineColor(1)    
        Q2_xB_borders[line_num].SetLineWidth(2)
        Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
        line_num += 1
    if((str(Q2_Y_Bin_Input) not in ["All", "0"]) and (("y_bin" not in str(Binning_Method)) and ("Y_bin" not in str(Binning_Method)))):
        ##=====================================================##
        ##==========##     Selecting Q2-xB Bin     ##==========##
        ##=====================================================##
        line_num_2 = 0
        for b_lines_2 in Q2_xB_Border_Lines(Q2_Y_Bin_Input):
            Q2_xB_borders[line_num_2] = ROOT.TLine()
            Q2_xB_borders[line_num_2].SetLineColor(2)
            Q2_xB_borders[line_num_2].SetLineWidth(3)
            Q2_xB_borders[line_num_2].DrawLine(b_lines_2[0][0], b_lines_2[0][1], b_lines_2[1][0], b_lines_2[1][1])
            line_num_2 += + 1
        ##=====================================================##
        ##==========##     Selecting Q2-xB Bin     ##==========##
        ##=====================================================##
        
    
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
    
    
    elth___Histo_rdf_2D = str(elth__Histo_rdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    elPhi__Histo_rdf_2D = str(elPhi_Histo_rdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipth__Histo_rdf_2D = str(pipth__Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipPhi_Histo_rdf_2D = str(pipPhi_Histo_rdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    elth___Histo_mdf_2D = str(elth__Histo_mdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    elPhi__Histo_mdf_2D = str(elPhi_Histo_mdf_Initial_Name).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipth__Histo_mdf_2D = str(pipth__Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    pipPhi_Histo_mdf_2D = str(pipPhi_Histo_mdf_Initial_Name).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(str(Z_PT_Bin_Input) in ["All", "0"]) else str(Z_PT_Bin_Input)]))
    
    
    # Setting the range for P_el
    Drawing_Histo_Set[str(elth___Histo_rdf_2D)].GetYaxis().SetRangeUser(2.2, 8)
    Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)].GetYaxis().SetRangeUser(2.2, 8)
    Drawing_Histo_Set[str(elth___Histo_mdf_2D)].GetYaxis().SetRangeUser(2.2, 8)
    Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)].GetYaxis().SetRangeUser(2.2, 8)
    
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

    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=1,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth___Histo_rdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=2,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi__Histo_rdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=3,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth__Histo_rdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=4,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=4,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=5,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=5,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth___Histo_mdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=6,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=6,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi__Histo_mdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=7,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=7,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth__Histo_mdf_2D)].Draw("colz")
    
    # Draw_Canvas(canvas=Canvas_Input_3, cd_num=8,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
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
    
    # Kinematic_Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin_Input) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin_Input), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin_Input) if(str(Z_PT_Bin_Input) not in ["0"]) else "All"]), "}}}"])
    
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
    
    # for Histo_rdf_1D_Name in [el_____Histo_rdf_1D, elth___Histo_rdf_1D, elPhi__Histo_rdf_1D, pip____Histo_rdf_1D, pipth__Histo_rdf_1D, pipPhi_Histo_rdf_1D]:
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
    
    # for Histo_mdf_1D_Name in [el_____Histo_mdf_1D, elth___Histo_mdf_1D, elPhi__Histo_mdf_1D, pip____Histo_mdf_1D, pipth__Histo_mdf_1D, pipPhi_Histo_mdf_1D]:
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
    
    for Name_1D in [Q2_____Histo_rdf_1D, Q2_____Histo_mdf_1D, y______Histo_rdf_1D, y______Histo_mdf_1D, z______Histo_rdf_1D, z______Histo_mdf_1D, pT_____Histo_rdf_1D, pT_____Histo_mdf_1D, xB_____Histo_rdf_1D, xB_____Histo_mdf_1D, el_____Histo_rdf_1D, el_____Histo_mdf_1D, elth___Histo_rdf_1D, elth___Histo_mdf_1D, pip____Histo_rdf_1D, pip____Histo_mdf_1D, pipth__Histo_rdf_1D, pipth__Histo_mdf_1D]:
        # Rebinning all comparisons except the lab phi angles
        Drawing_Histo_Set[Name_1D].Rebin(2)
    
        
    # Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=1,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    Q2_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(Q2_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    Q2_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(Q2_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    Q2_____Histo_max_1D_Normalized = max([0, 1.4*Q2_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*Q2_____Histo_mdf_1D_Normalized.GetMaximum()])
    Q2_____Histo_min_1D_Normalized = min([0, 1.4*Q2_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*Q2_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    Q2_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(Q2_____Histo_min_1D_Normalized, Q2_____Histo_max_1D_Normalized)
    Q2_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(Q2_____Histo_min_1D_Normalized, Q2_____Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=2,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    y______Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(y______Histo_rdf_1D)].DrawNormalized("H P E0 same")
    y______Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(y______Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    y______Histo_max_1D_Normalized = max([0, 1.4*y______Histo_rdf_1D_Normalized.GetMaximum(), 1.4*y______Histo_mdf_1D_Normalized.GetMaximum()])
    y______Histo_min_1D_Normalized = min([0, 1.4*y______Histo_rdf_1D_Normalized.GetMinimum(), 1.4*y______Histo_mdf_1D_Normalized.GetMinimum()])
    
    y______Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(y______Histo_min_1D_Normalized, y______Histo_max_1D_Normalized)
    y______Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(y______Histo_min_1D_Normalized, y______Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=3,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    z______Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(z______Histo_rdf_1D)].DrawNormalized("H P E0 same")
    z______Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(z______Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    z______Histo_max_1D_Normalized = max([0, 1.4*z______Histo_rdf_1D_Normalized.GetMaximum(), 1.4*z______Histo_mdf_1D_Normalized.GetMaximum()])
    z______Histo_min_1D_Normalized = min([0, 1.4*z______Histo_rdf_1D_Normalized.GetMinimum(), 1.4*z______Histo_mdf_1D_Normalized.GetMinimum()])
    
    z______Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(z______Histo_min_1D_Normalized, z______Histo_max_1D_Normalized)
    z______Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(z______Histo_min_1D_Normalized, z______Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=4,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=4,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pT_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pT_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pT_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pT_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pT_____Histo_max_1D_Normalized = max([0, 1.4*pT_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pT_____Histo_mdf_1D_Normalized.GetMaximum()])
    pT_____Histo_min_1D_Normalized = min([0, 1.4*pT_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pT_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    pT_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pT_____Histo_min_1D_Normalized, pT_____Histo_max_1D_Normalized)
    pT_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pT_____Histo_min_1D_Normalized, pT_____Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=5,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_1, cd_num=5,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    xB_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(xB_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    xB_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(xB_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    xB_____Histo_max_1D_Normalized = max([0, 1.4*xB_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*xB_____Histo_mdf_1D_Normalized.GetMaximum()])
    xB_____Histo_min_1D_Normalized = min([0, 1.4*xB_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*xB_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    xB_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(xB_____Histo_min_1D_Normalized, xB_____Histo_max_1D_Normalized)
    xB_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(xB_____Histo_min_1D_Normalized, xB_____Histo_max_1D_Normalized)
    
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=1,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    el_____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(el_____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    el_____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(el_____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    el_____Histo_max_1D_Normalized = max([0, 1.4*el_____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*el_____Histo_mdf_1D_Normalized.GetMaximum()])
    el_____Histo_min_1D_Normalized = min([0, 1.4*el_____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*el_____Histo_mdf_1D_Normalized.GetMinimum()])
    
    el_____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(el_____Histo_min_1D_Normalized, el_____Histo_max_1D_Normalized)
    el_____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(el_____Histo_min_1D_Normalized, el_____Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=2,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    elth___Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(elth___Histo_rdf_1D)].DrawNormalized("H P E0 same")
    elth___Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(elth___Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    elth___Histo_max_1D_Normalized = max([0, 1.4*elth___Histo_rdf_1D_Normalized.GetMaximum(), 1.4*elth___Histo_mdf_1D_Normalized.GetMaximum()])
    elth___Histo_min_1D_Normalized = min([0, 1.4*elth___Histo_rdf_1D_Normalized.GetMinimum(), 1.4*elth___Histo_mdf_1D_Normalized.GetMinimum()])
    
    elth___Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(elth___Histo_min_1D_Normalized, elth___Histo_max_1D_Normalized)
    elth___Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(elth___Histo_min_1D_Normalized, elth___Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=3,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_2, cd_num=3,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    elPhi__Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(elPhi__Histo_rdf_1D)].DrawNormalized("H P E0 same")
    elPhi__Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(elPhi__Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    elPhi__Histo_max_1D_Normalized = max([0, 1.4*elPhi__Histo_rdf_1D_Normalized.GetMaximum(), 1.4*elPhi__Histo_mdf_1D_Normalized.GetMaximum()])
    elPhi__Histo_min_1D_Normalized = min([0, 1.4*elPhi__Histo_rdf_1D_Normalized.GetMinimum(), 1.4*elPhi__Histo_mdf_1D_Normalized.GetMinimum()])
    
    elPhi__Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(elPhi__Histo_min_1D_Normalized, elPhi__Histo_max_1D_Normalized)
    elPhi__Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(elPhi__Histo_min_1D_Normalized, elPhi__Histo_max_1D_Normalized)
    
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=1,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=1,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pip____Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pip____Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pip____Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pip____Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pip____Histo_max_1D_Normalized = max([0, 1.4*pip____Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pip____Histo_mdf_1D_Normalized.GetMaximum()])
    pip____Histo_min_1D_Normalized = min([0, 1.4*pip____Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pip____Histo_mdf_1D_Normalized.GetMinimum()])
    
    pip____Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pip____Histo_min_1D_Normalized, pip____Histo_max_1D_Normalized)
    pip____Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pip____Histo_min_1D_Normalized, pip____Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=2,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=2,  left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    pipth__Histo_rdf_1D_Normalized = Drawing_Histo_Set[str(pipth__Histo_rdf_1D)].DrawNormalized("H P E0 same")
    pipth__Histo_mdf_1D_Normalized = Drawing_Histo_Set[str(pipth__Histo_mdf_1D)].DrawNormalized("H P E0 same")
    
    pipth__Histo_max_1D_Normalized = max([0, 1.4*pipth__Histo_rdf_1D_Normalized.GetMaximum(), 1.4*pipth__Histo_mdf_1D_Normalized.GetMaximum()])
    pipth__Histo_min_1D_Normalized = min([0, 1.4*pipth__Histo_rdf_1D_Normalized.GetMinimum(), 1.4*pipth__Histo_mdf_1D_Normalized.GetMinimum()])
    
    pipth__Histo_rdf_1D_Normalized.GetYaxis().SetRangeUser(pipth__Histo_min_1D_Normalized, pipth__Histo_max_1D_Normalized)
    pipth__Histo_mdf_1D_Normalized.GetYaxis().SetRangeUser(pipth__Histo_min_1D_Normalized, pipth__Histo_max_1D_Normalized)
    
    # Draw_Canvas(canvas=Canvas_Input_4_Row_3, cd_num=3,  left_add=0.075, right_add=0.05,  up_add=0.1, down_add=0.1)
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
            Large_Bin_Canvas_Compare = Canvas_Create(Name=str(Canvas_Input_0.GetName()).replace("CANVAS", "CANVAS_COMPARE"), Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=3000, cd_Space=0)

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

            # Large_Bin_Canvas_Compare.cd(3)
            # Canvas_Input_1.DrawClone()
            # Canvas_Input_1.Modified()
            # Canvas_Input_1.Update()
            # Large_Bin_Canvas_Compare.cd(4)
            # Canvas_Input_2.DrawClone()
            # Canvas_Input_2.Modified()
            # Canvas_Input_2.Update()


            # Large_Bin_Canvas_Compare_Side_by_Side.Modified()
            # Large_Bin_Canvas_Compare_Side_by_Side.Update()

            # Large_Bin_Canvas_Compare.cd(2)
            # rect1 = ROOT.TBox(Large_Bin_Canvas_Compare_Side_by_Side_CD.GetX1(), Large_Bin_Canvas_Compare_Side_by_Side_CD.GetY1(), Large_Bin_Canvas_Compare_Side_by_Side_CD.GetX2(), Large_Bin_Canvas_Compare_Side_by_Side_CD.GetY2())
            # rect1.SetFillColor(0)
            # rect1.SetFillStyle(0)
            # rect1.Draw("same")

            # rect2 = ROOT.TBox(Large_Bin_Canvas_Compare_Side_by_Side.GetX1(), Large_Bin_Canvas_Compare_Side_by_Side.GetY1(), Large_Bin_Canvas_Compare_Side_by_Side.GetX2(), Large_Bin_Canvas_Compare_Side_by_Side.GetY2())
            # rect2.SetFillColor(3)
            # rect2.SetFillStyle(0)
            # rect2.Draw("same")

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

            Run_Bin_Comparison = True
            # Run_Bin_Comparison = False
            if(Run_Bin_Comparison and String_Output not in [""]):
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
                        if(Bin_Content == 0):
                            # Empty Bin (no comparison)
                            No_Score   += 1
                        elif(((Bin_Content + Bin_Error) > 1)   and ((Bin_Content - Bin_Error) < 1)):
                            # Good Matches (within error of 1:1)
                            if((Bin_Content < 1.05) and (Bin_Content > 0.95)):
                                # Great Match
                                string_line  = "".join([color.GREEN, color.BOLD, str(string_line), color.END])
                                Great_Score += 1
                            else:
                                # Could just have large error but still good
                                string_line = "".join([color.GREEN, str(string_line), color.END])
                                Good_Score += 1
                        elif((Bin_Content < 1.05)              and (Bin_Content  > 0.95)):
                            # Good Match (but not necessarily perfect)
                            string_line = "".join([color.GREEN,  str(string_line), color.END])
                            Good_Score += 1
                        elif((Bin_Content < 1.1)               and (Bin_Content  > 0.9)):
                            # Okay Match (closer to good than to bad)
                            string_line = "".join([color.BOLD,   str(string_line), color.END])
                            Okay_Score += 1
                        elif(((Bin_Content + Bin_Error) > 1.2)  or ((Bin_Content - Bin_Error) < 0.8)):
                            # Poor match
                            string_line = "".join([color.PURPLE, str(string_line), color.END])
                            Poor_Score += 1
                        elif(((Bin_Content + Bin_Error) > 1.45) or ((Bin_Content - Bin_Error) < 0.55)):
                            # Bad match
                            string_line = "".join([color.RED,    str(string_line), color.END])
                            Bad_Score  += 1

                        String_Output = "".join([str(String_Output), str(string_line)])

                    Total_Score         = (2*Great_Score) + (Good_Score) + (0.5*Okay_Score) - (Poor_Score) - (2*Bad_Score)
                    Average_Bin_Content = round(Histo_Compare.Integral() / Histo_Compare.GetNbinsX(), 4)
                    String_Output = "".join([str(String_Output), color.BOLD, "Review of Histogram", color.END, """
    Total Num of Bins:   """, str(bin_ii + 1), """
    Average Bin Content: """, color.BOLD, color.RED if((Average_Bin_Content > 1.4) or (Average_Bin_Content < 0.6)) else color.GREEN if((Average_Bin_Content < 1.15) and (Average_Bin_Content > 0.85)) else "", str(Average_Bin_Content), color.END, """
    Total Score:         """, color.BOLD, color.RED if(Total_Score < 0) else color.GREEN if(Total_Score > 0) else "", str(Total_Score), color.END, """
    """, color.GREEN, color.BOLD, "\tNum of Great  (+2) Score: ", str(Great_Score), color.END, """
    """, color.GREEN,             "\tNum of Good   (+1) Score: ", str(Good_Score),  color.END, """
    """,              color.BOLD, "\tNum of Okay (+0.5) Score: ", str(Okay_Score),  color.END, """
    """,                          "\tNum of Empty  (+0) Score: ", str(No_Score),               """
    """, color.PURPLE,            "\tNum of Poor   (-1) Score: ", str(Poor_Score),  color.END, """
    """, color.RED,               "\tNum of Bad    (-2) Score: ", str(Bad_Score),   color.END])
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
                Save_Name = "".join(["Multi_Unfold_", str(Save_Name)])
            if(Sim_Test):
                Save_Name = "".join(["Sim_Test_",     str(Save_Name)])
            if(not any(binning in Binning_Method for binning in ["y", "Y"])):
                print(color.Error, "\n\nUsing Old Binning Scheme (i.e., Binning_Method = ", str(Binning_Method), ")", color.END, "\n\n")
                Save_Name = Save_Name.replace("_Q2_y_Bin_", "_Q2_xB_Bin_")
            Save_Name = Save_Name.replace("__", "_")
            if(Saving_Q):
                if("root" in str(File_Save_Format)):
                    Large_Bin_Canvas_Compare.SetName(Save_Name.replace(".root", ""))
                Large_Bin_Canvas_Compare.SaveAs(Save_Name)
            print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))

            # Returning 'String_For_Output_txt'/'String_Input' as 'String_Output'
            return String_Output

        except:
            print(color.Error, "\n\nERROR IN 'Large_Bin_Canvas_Compare'...\nTraceback:\n", color.END, color.BOLD, str(traceback.format_exc()), color.END, "\n")
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
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if(((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) in ["All", "0"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if(Multi_Dim_Option in ["Q2_y"]) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
    if((Multi_Dim_Option not in ["Off"]) and (str(Z_PT_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        
    Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
    
    # Large_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS"), Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=2400, cd_Space=0)
    # Large_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS"), Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=3300, cd_Space=0)
    Large_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS"), Num_Columns=1, Num_Rows=4, Size_X=2400, Size_Y=3200, cd_Space=0)
    Large_Bin_Canvas_Row_1 = Large_Bin_Canvas.cd(1)
    Large_Bin_Canvas_Row_2 = Large_Bin_Canvas.cd(2)
    Large_Bin_Canvas_Row_3 = Large_Bin_Canvas.cd(3)
    Large_Bin_Canvas_Row_4 = Large_Bin_Canvas.cd(4)
    Large_Bin_Canvas_Row_1.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_2.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_3.Divide(4, 2, 0, 0)
    Large_Bin_Canvas_Row_4.Divide(1, 3, 0, 0)
    
    ExREAL_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''" if(not Sim_Test) else "Smear"))]
    MC_REC_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "mdf")))]
    MC_GEN_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "gdf")).replace("Smear", "''"))]
    if(Sim_Test):
        # ExREAL_1D = MC_REC_1D
        ExTRUE_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''"))]
    else:
        # ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''"))]
        ExTRUE_1D = "N/A"
    
    Default_Response_Matrix_Name = str(str(Default_Histo_Name.replace("Data_Type",     "mdf")).replace("1D",    "Response_Matrix")).replace("Multi-Dim Histo", "Response_Matrix")
    if(Multi_Dim_Option not in ["Off"]):
        Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]),     "(z_pT_Bin_All)")
        if(("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Response_Matrix_Name) and (str(Q2_Y_Bin) not in ["All", "0"])):
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(Q2_y_Bin_", str(Q2_Y_Bin), ")"]), "(Q2_y_Bin_All)")
        
    
    Response_2D       = Histogram_List_All[Default_Response_Matrix_Name]
    
    UNFOLD_Bin        = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Bin")))]
    UNFOLD_Acceptance = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Acceptance")))]
    UNFOLD_Bay        = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "Bayesian")))]
    
    Response_2D.SetTitle(      str(Response_2D.GetTitle()).replace(      "Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    UNFOLD_Bin.SetTitle(       str(UNFOLD_Bin.GetTitle()).replace(       "Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    UNFOLD_Bay.SetTitle(       str(UNFOLD_Bay.GetTitle()).replace(       "Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD    = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "SVD")))]
        UNFOLD_SVD.SetTitle(   str(UNFOLD_SVD.GetTitle()).replace(       "Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    
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
        if(Multi_Dim_Option in ["Off"]):
            UNFOLD_SVD.GetXaxis().SetRange(1,    UNFOLD_SVD.GetXaxis().GetNbins()        + 1)
    except:
        print("".join([color.BOLD, color.RED, "\nERROR IN Axis Ranges...", color.END]))
        print("".join([color.BOLD, color.RED,   "ERROR:\n",                color.END, color.RED, str(traceback.format_exc()), color.END]))
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    #####==========#####        Legend Setup         #####==========##### ################################################################
    ##################################################################### ################################################################
    # if(("phi_t"      not in str(Default_Histo_Name)) and ("Multi_Dim" not in str(Default_Histo_Name))):
    #     Legends_Unfolded = ROOT.TLegend(0.5,  0.5,  0.95, 0.75)
    # elif("Multi_Dim" not in str(Default_Histo_Name)):
    #     Legends_Unfolded = ROOT.TLegend(0.25, 0.15, 0.85, 0.55)
    if("phi_t" not in str(Default_Histo_Name)):
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
    MC_GEN_1D.SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
    MC_GEN_1D.SetLineStyle(1)
    MC_GEN_1D.SetMarkerColor(root_color.Green)
    MC_GEN_1D.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
    MC_GEN_1D.SetMarkerStyle(20)
    MC_GEN_1D.GetYaxis().SetTitle("Normalized")
    #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################
    # UNFOLD_Bin.GetYaxis().SetTitle("Normalized")
    UNFOLD_Bin.SetLineColor(root_color.Brown)
    UNFOLD_Bin.SetLineWidth(2 if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
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
    UNFOLD_Bay.SetLineWidth(2  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
    UNFOLD_Bay.SetLineStyle(1)
    UNFOLD_Bay.SetMarkerColor(root_color.Teal)
    UNFOLD_Bay.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
    UNFOLD_Bay.SetMarkerStyle(21)
    #####==========#####    Unfold SVD Histogram     #####==========##### ################################################################
    if(Multi_Dim_Option in ["Off"]):
        # UNFOLD_SVD.GetYaxis().SetTitle("Normalized")
        UNFOLD_SVD.SetMarkerColor(root_color.Pink)
        UNFOLD_SVD.SetLineWidth(2)
        UNFOLD_SVD.SetLineStyle(1)
        UNFOLD_SVD.SetLineColor(root_color.Pink)
        UNFOLD_SVD.SetMarkerSize(1)
        UNFOLD_SVD.SetMarkerStyle(21)
    #####==========#####      MC TRUE Histogram      #####==========##### ################################################################
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D.SetLineColor(root_color.Cyan)
        ExTRUE_1D.SetLineWidth(3  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
        ExTRUE_1D.SetLineStyle(1)
        ExTRUE_1D.SetMarkerColor(root_color.Cyan)
        ExTRUE_1D.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
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
    # Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=3, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=3, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    if("phi_t" in str(Default_Histo_Name)):
        ExREAL_1D.GetXaxis().SetRangeUser(0, 360)
        MC_REC_1D.GetXaxis().SetRangeUser(0, 360)
        MC_GEN_1D.GetXaxis().SetRangeUser(0, 360)
        
        # ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        ExREAL_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_REC_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_GEN_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
    # ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H PL E0 same")
    ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(ExREAL_1D_Norm, "#scale[2]{Experimental}", "lpE")
    # MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H PL E0 same")
    MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(MC_REC_1D_Norm, "#scale[2]{MC REC}", "lpE")
    # MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H PL E0 same")
    MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H P E0 same")
    Legends_REC.AddEntry(MC_GEN_1D_Norm, "#scale[2]{MC GEN}", "lpE")
    
    Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
    
    ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    
    # ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    
    Legends_REC.Draw("same")
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 1 - CD 4     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ################################################################
    # Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=4, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=4, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
    if("phi_t" in str(Default_Histo_Name)):
        UNFOLD_Bin.GetXaxis().SetRangeUser(0, 360)
        UNFOLD_Bay.GetXaxis().SetRangeUser(0, 360)
        
        if(Multi_Dim_Option in ["Off"]):
            UNFOLD_SVD.GetXaxis().SetRangeUser(0, 360)
            UNFOLD_SVD.SetTitle("".join(["#splitline{#scale[1.5]{Unfolded Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
            
        if(ExTRUE_1D not in ["N/A"]):
            ExTRUE_1D.GetXaxis().SetRangeUser(0, 360)
            ExTRUE_1D.SetTitle("".join(["#splitline{#scale[1.5]{Unfolded Distributions of #phi_{h}}}{#scale[1.15]{",  str(Bin_Title), "}}"]))
            
        UNFOLD_Bin.SetTitle("".join(["#splitline{#scale[1.5]{", "Unfolded" if(str(Multi_Dim_Option) in ["Off"]) else "".join(["#splitline{Multi-Dimensional Unfolded}{", "Q^{2}-y-#phi_{h} Unfolding" if("(Multi_Dim_Q2_y_Bin_phi_t)" in str(Default_Histo_Name)) else "z-P_{T}-#phi_{h} Unfolding", "}"]), " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bay.SetTitle("".join(["#splitline{#scale[1.5]{", "Unfolded" if(str(Multi_Dim_Option) in ["Off"]) else "".join(["#splitline{Multi-Dimensional Unfolded}{", "Q^{2}-y-#phi_{h} Unfolding" if("(Multi_Dim_Q2_y_Bin_phi_t)" in str(Default_Histo_Name)) else "z-P_{T}-#phi_{h} Unfolding", "}"]), " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
    else:
        UNFOLD_SVD.SetTitle(str(UNFOLD_SVD.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        UNFOLD_SVD.SetTitle(str(UNFOLD_SVD.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
        UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
        UNFOLD_Bay.SetTitle(str(UNFOLD_Bay.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        
    # if(Multi_Dim_Option in ["Off"]):
    #     # UNFOLD_SVD_Norm =  UNFOLD_SVD.DrawNormalized("H PL E0 same")
    #     UNFOLD_SVD_Norm =  UNFOLD_SVD.DrawNormalized("H P E0 same")
    #     # UNFOLD_SVD_Norm =  UNFOLD_SVD.Draw("H P E0 same")
    #     statbox_move(Histogram=UNFOLD_SVD_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    #     for ii in range(0, UNFOLD_SVD.GetNbinsX() + 1, 1):
    #         if(UNFOLD_SVD_Norm.GetBinError(ii) > 0.01):
    #             print("".join([color.RED, "\n(SVD Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
    #             UNFOLD_SVD_Norm.SetBinContent(ii, 0)
    #             UNFOLD_SVD_Norm.SetBinError(ii,   0)
    #     Legends_Unfolded.AddEntry(UNFOLD_SVD_Norm, "#scale[2]{SVD Unfolded}", "lpE")
    # # UNFOLD_Bin_Norm =  UNFOLD_Bin.DrawNormalized("H PL E0 same")
    # UNFOLD_Bin_Norm =  UNFOLD_Bin.DrawNormalized("H P E0 same")
    # # UNFOLD_Bin_Norm =  UNFOLD_Bin.Draw("H P E0 same")
    # statbox_move(Histogram=UNFOLD_Bin_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bin_Norm.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bin_Norm.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bin_Norm.SetBinContent(ii,  0)
    #         UNFOLD_Bin_Norm.SetBinError(ii,    0)
    # Legends_Unfolded.AddEntry(UNFOLD_Bin_Norm, "#scale[2]{Bin-by-Bin}", "lpE")
    # # UNFOLD_Bay_Norm =  UNFOLD_Bay.DrawNormalized("H PL E0 same")
    # UNFOLD_Bay_Norm =  UNFOLD_Bay.DrawNormalized("H P E0 same")
    # # UNFOLD_Bay_Norm =  UNFOLD_Bay.Draw("H P E0 same")
    # statbox_move(Histogram=UNFOLD_Bay_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bay_Norm.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bay_Norm.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bay_Norm.SetBinContent(ii, 0)
    #         UNFOLD_Bay_Norm.SetBinError(ii,   0)
    # Legends_Unfolded.AddEntry(UNFOLD_Bay_Norm, "#scale[2]{Bayesian}", "lpE")
    # if(ExTRUE_1D not in ["N/A"]):
    #     ExTRUE_1D_Norm =  ExTRUE_1D.DrawNormalized("H P E0 same")
    #     # ExTRUE_1D_Norm =  ExTRUE_1D.Draw("H P E0 same")
    #     statbox_move(Histogram=ExTRUE_1D_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    #     for ii in range(0, ExTRUE_1D_Norm.GetNbinsX() + 1, 1):
    #         if(ExTRUE_1D_Norm.GetBinError(ii) > 0.01):
    #             print("".join([color.RED, "\n(MC TRUE Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
    #             ExTRUE_1D_Norm.SetBinContent(ii, 0)
    #             ExTRUE_1D_Norm.SetBinError(ii,   0)
    #     Legends_Unfolded.AddEntry(ExTRUE_1D_Norm, "#scale[2]{MC TRUE}", "lpE")
    # # if(Multi_Dim_Option in ["Off"]):
    # #     Max_Unfolded = max([UNFOLD_SVD_Norm.GetMaximum, UNFOLD_Bin_Norm.GetMaximum, UNFOLD_Bay_Norm.GetMaximum])
    # # else:
    # Max_Unfolded = max([UNFOLD_Bin_Norm.GetBinContent(UNFOLD_Bin_Norm.GetMaximumBin()), UNFOLD_Bay_Norm.GetBinContent(UNFOLD_Bay_Norm.GetMaximumBin())])
    # if(ExTRUE_1D not in ["N/A"]):
    #     Max_Unfolded = max([UNFOLD_Bin_Norm.GetBinContent(UNFOLD_Bin_Norm.GetMaximumBin()), UNFOLD_Bay_Norm.GetBinContent(UNFOLD_Bay_Norm.GetMaximumBin()), ExTRUE_1D_Norm.GetBinContent(ExTRUE_1D_Norm.GetMaximumBin())])
    # if(Multi_Dim_Option in ["Off"]):
    #     UNFOLD_SVD_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Unfolded)
    # UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    # UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    # if(ExTRUE_1D not in ["N/A"]):
    #     ExTRUE_1D_Norm.GetYaxis().SetRangeUser(0,  1.2*Max_Unfolded)
    # Legends_Unfolded.Draw("same")
    
    
    
    if(Multi_Dim_Option in ["Off"]):
        # UNFOLD_SVD.DrawNormalized("H PL E0 same")
        UNFOLD_SVD.GetYaxis().SetTitle("Count")
        UNFOLD_SVD.Draw("H P E0 same")
        # configure_stat_box(hist=UNFOLD_SVD, show_entries=True, canvas=Large_Bin_Canvas_Row_1.cd(4))
        statbox_move(Histogram=UNFOLD_SVD, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
        # for ii in range(0, UNFOLD_SVD.GetNbinsX() + 1, 1):
        #     if(UNFOLD_SVD.GetBinError(ii) > 0.01):
        #         print("".join([color.RED, "\n(SVD Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
        #         UNFOLD_SVD.SetBinContent(ii, 0)
        #         UNFOLD_SVD.SetBinError(ii,   0)
        Legends_Unfolded.AddEntry(UNFOLD_SVD, "#scale[2]{SVD Unfolded}", "lpE")

    # UNFOLD_Bin.DrawNormalized("H PL E0 same")
    # UNFOLD_Bin.DrawNormalized("H P E0 same")
    UNFOLD_Bin.GetYaxis().SetTitle("Count")
    UNFOLD_Bin.Draw("H P E0 same")
    statbox_move(Histogram=UNFOLD_Bin, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bin.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bin.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bin.SetBinContent(ii,  0)
    #         UNFOLD_Bin.SetBinError(ii,    0)
    Legends_Unfolded.AddEntry(UNFOLD_Bin, "#scale[2]{Bin-by-Bin}", "lpE")

    # UNFOLD_Bay.DrawNormalized("H PL E0 same")
    # UNFOLD_Bay.DrawNormalized("H P E0 same")
    UNFOLD_Bay.Draw("H P E0 same")
    statbox_move(Histogram=UNFOLD_Bay, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    # for ii in range(0, UNFOLD_Bay.GetNbinsX() + 1, 1):
    #     if(UNFOLD_Bay.GetBinError(ii) > 0.01):
    #         print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
    #         UNFOLD_Bay.SetBinContent(ii, 0)
    #         UNFOLD_Bay.SetBinError(ii,   0)
    Legends_Unfolded.AddEntry(UNFOLD_Bay, "#scale[2]{Bayesian}", "lpE")
    
    if(ExTRUE_1D not in ["N/A"]):
        # ExTRUE_1D.DrawNormalized("H P E0 same")
        ExTRUE_1D.Draw("H P E0 same")
        statbox_move(Histogram=ExTRUE_1D, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
        # for ii in range(0, ExTRUE_1D.GetNbinsX() + 1, 1):
        #     if(ExTRUE_1D.GetBinError(ii) > 0.01):
        #         print("".join([color.RED, "\n(MC TRUE Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
        #         ExTRUE_1D.SetBinContent(ii, 0)
        #         ExTRUE_1D.SetBinError(ii,   0)
        Legends_Unfolded.AddEntry(ExTRUE_1D, "#scale[2]{MC TRUE}", "lpE")
    
    # if(Multi_Dim_Option in ["Off"]):
    #     Max_Unfolded = max([UNFOLD_SVD_Norm.GetMaximum, UNFOLD_Bin_Norm.GetMaximum, UNFOLD_Bay_Norm.GetMaximum])
    # else:
    Max_Unfolded     = max([UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin()), UNFOLD_Bay.GetBinContent(UNFOLD_Bay.GetMaximumBin())])
    if(ExTRUE_1D not in ["N/A"]):
        Max_Unfolded = max([UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin()), UNFOLD_Bay.GetBinContent(UNFOLD_Bay.GetMaximumBin()), ExTRUE_1D.GetBinContent(ExTRUE_1D.GetMaximumBin())])
    
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD.GetYaxis().SetRangeUser(0, 1.2*Max_Unfolded)
    UNFOLD_Bin.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    UNFOLD_Bay.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D.GetYaxis().SetRangeUser(0,  1.2*Max_Unfolded)
    Legends_Unfolded.Draw("same")
    ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 3     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    # Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=3, left_add=0.1,   right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=3, left_add=0.15,  right_add=0.075, up_add=0.1, down_add=0.1)
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
    
    # if((str(Bin_Title) not in str(Response_2D.GetTitle())) and (Multi_Dim_Option in ["Off"])):
    #     Response_2D.SetTitle("".join(["#splitline{", str(Response_2D.GetTitle()), "}{", str(Bin_Title), "}"]))
    if((Standard_Histogram_Title_Addition not in [""]) and (Standard_Histogram_Title_Addition not in str(Response_2D.GetTitle()))):
        Response_2D.SetTitle("".join(["#splitline{", str(Response_2D.GetTitle()), "}{", str(Standard_Histogram_Title_Addition), "}"]))
    
    Large_Bin_Canvas.Modified()
    Large_Bin_Canvas.Update()
    palette_move(canvas=Large_Bin_Canvas, histo=Response_2D, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 4     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    # Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=4, left_add=0.15,  right_add=0.05,  up_add=0.1, down_add=0.1)
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=4, left_add=0.2,   right_add=0.075, up_add=0.1, down_add=0.1)
    UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    # if(str(Bin_Title) not in str(UNFOLD_Acceptance.GetTitle())):
    #     UNFOLD_Acceptance.SetTitle("".join(["#splitline{", str(UNFOLD_Acceptance.GetTitle()), "}{",  str(Bin_Title), "}"]))
    if((Standard_Histogram_Title_Addition not in [""]) and (Standard_Histogram_Title_Addition not in str(UNFOLD_Acceptance.GetTitle()))):
        UNFOLD_Acceptance.SetTitle("".join(["#splitline{", str(UNFOLD_Acceptance.GetTitle()), "}{",  str(Standard_Histogram_Title_Addition), "}"]))
    if("Reconstructed (MC) Distribution of" in str(UNFOLD_Acceptance.GetTitle())):
        UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace("Reconstructed (MC) Distribution of", "Bin-by-Bin Acceptance for"))
    UNFOLD_Acceptance.GetXaxis().SetRangeUser(0, 360)
    UNFOLD_Acceptance.GetYaxis().SetTitle("Acceptance")
    UNFOLD_Acceptance.Draw("same E1 H")
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ########################################################################## ###################################################################################################################################################################################################################################################################################################
    ##=====##=====##      Drawing the Extra 2D Histos         ##=====##=====## ###################################################################################################################################################################################################################################################################################################
    # Draw_2D_Histograms_Simple_New(Histogram_List_All_Input=Histogram_List_All, Canvas_Input=[Large_Bin_Canvas, Large_Bin_Canvas_Row_1, Large_Bin_Canvas_Row_2, Large_Bin_Canvas_Row_3], Default_Histo_Name_Input=str(str(Default_Histo_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")).replace("(Multi_Dim_Q2_y_Bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_y_bin_phi_t)", "(phi_t)"), Q2_Y_Bin_Input=Q2_Y_Bin, Z_PT_Bin_Input=Z_PT_Bin)
    String_Input = Draw_2D_Histograms_Simple_New(Histogram_List_All_Input=Histogram_List_All, Canvas_Input=[Large_Bin_Canvas, Large_Bin_Canvas_Row_1, Large_Bin_Canvas_Row_2, Large_Bin_Canvas_Row_3, Large_Bin_Canvas_Row_4], Default_Histo_Name_Input=str(str(str(Default_Histo_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")).replace("(Multi_Dim_Q2_y_Bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_y_bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_Y_bin_phi_t)", "(phi_t)"), Q2_Y_Bin_Input=Q2_Y_Bin, Z_PT_Bin_Input=Z_PT_Bin, String_Output=String_Input)
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
    if("phi_t)" in Default_Histo_Name):
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
    if(Multi_Dim_Option not in ["Off"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = "".join(["Sim_Test_", Save_Name])
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                    "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",              "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",              "z_pT_phi_h")
    Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]), str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                "_")
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            Large_Bin_Canvas.SetName(Save_Name.replace(".root", ""))
        Large_Bin_Canvas.SaveAs(Save_Name)
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
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
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) not in ["All", "0"])):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if(Multi_Dim_Option in ["Q2_y"]) else                                       "(Multi_Dim_z_pT_Bin_y_bin_phi_t)" if("y" in Binning_Method) else "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")

    if(("(1D)" in Default_Histo_Name) and ("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Histo_Name) and (str(Q2_Y_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        
    Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
    
    if(Fit_Test):
        fit_function_title         = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if(Multi_Dim_Option in ["Off"]):
            if(not extra_function_terms):
                fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
            else:
                fit_function_title = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
        elif(Multi_Dim_Option not in ["Fitted", "Only"]):
            fit_function_title = "".join(["Plotted with #splitline{#color[", str(root_color.Pink), "]{Multidimensional Unfolding}}{",                       "Q^{2}-y-#phi_{h} Unfolding" if(str(Z_PT_Bin) in ["All", "0"]) else "z-P_{T}-#phi_{h} Unfolding", "}"])
            # Will need to update the line above later for 5D unfolding
            # Currently just switches between the 2 types of 3D Unfolding
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
    if(Standard_Histogram_Title_Addition not in [""]):
        Bin_Title = "".join(["#splitline{", str(Bin_Title), "}{", str(Standard_Histogram_Title_Addition), "}"])
    
    Small_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS_Unfolded"), Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1100, cd_Space=0)
    Small_Bin_Canvas_Row_1 = Small_Bin_Canvas.cd(1)
    Small_Bin_Canvas_Row_2 = Small_Bin_Canvas.cd(2)
    # Small_Bin_Canvas_Row_1.Divide(2 if(Multi_Dim_Option in ["Off"]) else 1, 1, 0)
    Small_Bin_Canvas_Row_1.Divide(2, 1, 0)
    Small_Bin_Canvas_Row_2.Divide(2, 1, 0)
    
    ExREAL_1D     = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''" if(not Sim_Test) else "Smear"))]
    MC_REC_1D     = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "mdf"))]
    MC_GEN_1D     = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "gdf")).replace("Smear", "''")]
    if(Sim_Test):
        # ExREAL_1D = MC_REC_1D
        ExTRUE_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "tdf")).replace("Smear", "''"))]
    else:
        # ExREAL_1D = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''"))]
        ExTRUE_1D = "N/A"
        
    UNFOLD_Bin = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "Bin"))]
    UNFOLD_Bay = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "Bayesian"))]
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "SVD"))]
    
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
        if(Multi_Dim_Option in ["Off"]):
            UNFOLD_SVD.GetXaxis().SetRange(1, UNFOLD_SVD.GetXaxis().GetNbins() + 1)
        
        if("phi_t" in str(Default_Histo_Name)):
            ExREAL_1D.GetXaxis().SetRangeUser(0,  360)
            MC_REC_1D.GetXaxis().SetRangeUser(0,  360)
            MC_GEN_1D.GetXaxis().SetRangeUser(0,  360)
            UNFOLD_Bin.GetXaxis().SetRangeUser(0, 360)
            UNFOLD_Bay.GetXaxis().SetRangeUser(0, 360)
            if(Multi_Dim_Option in ["Off"]):
                UNFOLD_SVD.GetXaxis().SetRangeUser(0, 360)
            if(ExTRUE_1D not in ["N/A"]):
                ExTRUE_1D.GetXaxis().SetRangeUser(0,  360)
            # if(Multi_Dim_Option not in ["Off", "Fitted", "Only"]):
            #     UNFOLD_Bin_Multi_Dim.GetXaxis().SetRangeUser(0, 360)
            #     UNFOLD_Bay_Multi_Dim.GetXaxis().SetRangeUser(0, 360)
    except:
        print("".join([color.BOLD, color.RED, "\nERROR IN Axis Ranges...", color.END]))
        print("".join([color.BOLD, color.RED,   "ERROR:\n",                color.END, color.RED, str(traceback.format_exc()), color.END]))
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
    
    ExREAL_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
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
    MC_REC_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
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
    MC_GEN_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
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
        ExTRUE_1D.SetTitle("".join(["#splitline{#scale[1.35]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions #phi_{h}}}{", str(Bin_Title), "}"]))
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
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Pink),  "]{SVD Unfolded} Distribution of #phi_{h}}}{",       root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
        UNFOLD_SVD.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
        UNFOLD_SVD.SetMarkerColor(root_color.Pink)
        UNFOLD_SVD.SetLineWidth(2)
        UNFOLD_SVD.SetLineStyle(1)
        UNFOLD_SVD.SetLineColor(root_color.Pink)
        UNFOLD_SVD.SetMarkerSize(1)
        UNFOLD_SVD.SetMarkerStyle(21)
        if(DRAW_NORMALIZE):
            UNFOLD_SVD.GetYaxis().SetTitle("Normalized")
        else:
            UNFOLD_SVD.GetYaxis().SetTitle("")
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
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D_Norm = ExTRUE_1D.DrawNormalized("H P E0 same")
    if(Fit_Test):
        try:
            statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=Small_Bin_Canvas_Row_1.cd(1), Print_Method="off")
        except:
            print("\nMC_GEN_1D IS NOT FITTED\n")
        if(ExTRUE_1D not in ["N/A"]):
            try:
                statbox_move(Histogram=ExTRUE_1D_Norm, Canvas=Small_Bin_Canvas_Row_1.cd(1), Print_Method="off")
            except:
                print("\nExTRUE_1D IS NOT FITTED\n")
        
    Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
    if(ExTRUE_1D not in ["N/A"]):
        Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin()), ExTRUE_1D_Norm.GetBinContent(ExTRUE_1D_Norm.GetMaximumBin())])
        
    ExREAL_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    MC_REC_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Pre_Unfolded)
    if(ExTRUE_1D not in ["N/A"]):
        ExTRUE_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
        
    Legends_REC.AddEntry(ExREAL_1D_Norm,     "#scale[2]{Experimental}", "lpE")
    Legends_REC.AddEntry(MC_REC_1D_Norm,     "#scale[2]{MC REC}",       "lpE")
    Legends_REC.AddEntry(MC_GEN_1D_Norm,     "#scale[2]{MC GEN}",       "lpE")
    if(ExTRUE_1D not in ["N/A"]):
        Legends_REC.AddEntry(ExTRUE_1D_Norm, "#scale[2]{MC TRUE}",       "lpE")
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
    ##=====##=====##    Drawing the SVD Unfold Histograms     ##=====##=====## ###################################################################
    if(Multi_Dim_Option in ["Off"]):
        Draw_Canvas(Small_Bin_Canvas_Row_1, 2, 0.15)
        if(DRAW_NORMALIZE):
            # UNFOLD_SVD_Norm = UNFOLD_SVD.DrawNormalized("H PL E0 same")
            UNFOLD_SVD_Norm = UNFOLD_SVD.DrawNormalized("H P E0 same")
            UNFOLD_SVD_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_SVD_Norm.GetBinContent(UNFOLD_SVD_Norm.GetMaximumBin())))
            for ii in range(0, UNFOLD_SVD_Norm.GetNbinsX() + 1, 1):
                if(UNFOLD_SVD_Norm.GetBinError(ii) > 0.01):
                    print("".join([color.RED, "\n(SVD Unfolded) Bin ",        str(ii), " has a large error (after normalizing)...", color.END]))
                    UNFOLD_SVD_Norm.SetBinContent(ii, 0)
                    UNFOLD_SVD_Norm.SetBinError(ii,   0)
            if(Fit_Test):
                UNFOLD_SVD_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_SVD_Norm, Method="SVD", Special=[Q2_Y_Bin, Z_PT_Bin])
                # UNFOLD_SVD_Fitted[1].Draw("H PL E0 same")
                UNFOLD_SVD_Fitted[1].Draw("H P E0 same")
                statbox_move(Histogram=UNFOLD_SVD_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        else:
            # UNFOLD_SVD.Draw("H PL E0 same")
            UNFOLD_SVD.Draw("H P E0 same")
            configure_stat_box(hist=UNFOLD_SVD, show_entries=True, canvas=Small_Bin_Canvas)
            UNFOLD_SVD.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_SVD.GetBinContent(UNFOLD_SVD.GetMaximumBin())))
            statbox_move(Histogram=UNFOLD_SVD, Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            # UNFOLD_SVD_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_SVD)
            # UNFOLD_SVD_Fitted[1].Draw("same")
            # statbox_move(Histogram=UNFOLD_SVD_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
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
    if("phi_t)" in Default_Histo_Name):
        Save_Name = "".join(["Response_Matrix_Normal_Q2_xB_Bin_", str(Q2_Y_Bin) if(str(Q2_Y_Bin) not in ["0"]) else "All", "_z_pT_Bin_", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All", "".join(["_Unfolded_Histos_Smeared", str(File_Save_Format)]) if("Smear" in Default_Histo_Name) else "".join(["_Unfolded_Histos", str(File_Save_Format)])])    
    else:
        Save_Name = str("".join([str(Default_Histo_Name), "_Unfolded_Histos", str(File_Save_Format)]).replace("(", "")).replace(")", "")
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
    if(any(binning in Binning_Method for binning in ["y", "Y"])):
        Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
    if(Multi_Dim_Option not in ["Off"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = "".join(["Sim_Test_",  str(Save_Name)])
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                      "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                "z_pT_phi_h")
    Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]), str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                  "_")
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            Small_Bin_Canvas.SetName(Save_Name.replace(".root", ""))
        Small_Bin_Canvas.SaveAs(Save_Name)
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################

    
####################################################################################################################################################################
##==========##==========## Function for Smaller (Unfolded) Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
####################################################################################################################################################################





##################################################################################################################################################################
##==========##==========## Function for Creating the Images for All z-pT Bins Together  ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################

def z_pT_Images_Together(Histogram_List_All, Default_Histo_Name, Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z", Cut_Option="Cut"):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    All_z_pT_Canvas = Canvas_Create(Name=Default_Histo_Name.replace("1D", "".join(["".join(["CANVAS_", str(Plot_Orientation)]) if(Multi_Dim_Option in ["Off"]) else "".join(["CANVAS_", str(Plot_Orientation), "_", str(Multi_Dim_Option)]), "_UnCut" if(Cut_Option not in ["Cut"]) else ""])), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
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
        number_of_rows, number_of_cols     = z_pT_Border_Lines_New(Q2_Y_Bin)[0][1]-1, z_pT_Border_Lines_New(Q2_Y_Bin)[1][1]-1
        if(Plot_Orientation in ["z_pT"]):
            number_of_rows, number_of_cols = z_pT_Border_Lines_New(Q2_Y_Bin)[1][1]-1, z_pT_Border_Lines_New(Q2_Y_Bin)[0][1]-1
            All_z_pT_Canvas_cd_2.Divide(number_of_rows, number_of_cols, 0.0001, 0.0001)
        else:
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
    Q2_y_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name.replace("(phi_t)", "(Q2)_(y)")).replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear")).replace("Data_Type", "bbb" if("Unfold" in str(Method)) else "rdf" if(str(Method) not in ["mdf", "gdf", "tdf"]) else str(Method))).replace("(1D)", "(Normal_2D)")
    z_pT_Histo_rdf_Initial_Name = str(str(str(Default_Histo_Name.replace("(phi_t)", "(z)_(pT)")).replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear")).replace("Data_Type", "bbb" if("Unfold" in str(Method)) else "rdf" if(str(Method) not in ["mdf", "gdf", "tdf"]) else str(Method))).replace("(1D)", "(Normal_2D)")
    if((str(Method) not in ["gdf", "tdf"]) and (Cut_Option not in ["Cut"])):
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", str(Method), ")_(no_cut)_(SMEAR"]))
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace("".join(["(Normal_2D)_(", str(Method), ")_(SMEAR"]), "".join(["(Normal_2D)_(", str(Method), ")_(no_cut)_(SMEAR"]))
        Q2_y_Histo_rdf_Initial_Name = str(Q2_y_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                          "(Normal_2D)_(rdf)_(no_cut)_(SMEAR")
        z_pT_Histo_rdf_Initial_Name = str(z_pT_Histo_rdf_Initial_Name).replace(         "(Normal_2D)_(rdf)_(SMEAR",                          "(Normal_2D)_(rdf)_(no_cut)_(SMEAR")
    Q2_y_Histo_rdf_Initial = Histogram_List_All[Q2_y_Histo_rdf_Initial_Name]
    z_pT_Histo_rdf_Initial = Histogram_List_All[z_pT_Histo_rdf_Initial_Name]
    Drawing_Histo_Set = {}
    ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    if("3D" in str(type(Q2_y_Histo_rdf_Initial))):
        bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(0), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Q2_y_Histo_rdf_Initial.GetNbinsX())
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
        bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(0), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(z_pT_Histo_rdf_Initial.GetNbinsX())
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
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(1), histo=Drawing_Histo_Set[Q2_y_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
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
        for Q2_Y_Bin_ii in range(1, 40, 1):
            Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.Draw("same")
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 2, 0.15)
    Drawing_Histo_Set[z_pT_Name].Draw("colz")
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
        
    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower, 1, 0.15)
    if(str(Multi_Dim_Option) not in ["Off"]):
        Default_Response_Matrix_Name =   str(str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")).replace("Multi-Dim Histo", "Response_Matrix")
        # Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")
        if(("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Response_Matrix_Name) and (str(Q2_Y_Bin) not in ["All", "0"])):
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(Q2_y_Bin_", str(Q2_Y_Bin), ")"]), "(Q2_y_Bin_All)")
        if("y" in Binning_Method):
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
        else:
            Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")
        # print("\n\n\n\n\n\n\nDefault_Response_Matrix_Name =", Default_Response_Matrix_Name, "\n\n\n\n\n\n\n\n")
        Histogram_List_All[Default_Response_Matrix_Name].SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
        Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
        Histogram_List_All[Default_Response_Matrix_Name].GetYaxis().SetTitle(str(str(Histogram_List_All[Default_Response_Matrix_Name].GetYaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h}")).replace("z_pT_Bin_Y_bin_phi_t", "(New) z-P_{T}-#phi_{h}"))
        Histogram_List_All[Default_Response_Matrix_Name].Draw("col")
    elif("Response" in str(Method)):
        try:
            Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].SetTitle(str(Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].Draw("col")
        except Exception as e:
            print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n",              color.END, color.RED, str(traceback.format_exc()), color.END]))
    elif("Data"   in str(Method)):
        try:
            if(Multi_Dim_Option in ["Off"]):
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                # MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                # MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")].DrawNormalized("H P E0 same")
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H P E0 same")
            else:
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
                # Currently built so that the integrated z-pT bin for multidimensional unfolding uses the combined Q2-y-phi variable (whereas the unfolding done for the individual z-pT bins will unfold the z-pT-phi variable instead)
                    # This note is to explain that the Multi-Dim version of this image will show 2 different types of multidimensional unfolding
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                # MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                # MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                # ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf" if(not Sim_Test) else "mdf")].DrawNormalized("H P E0 same")
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H P E0 same")
            
            # ExREAL_1D_Norm.SetTitle(str(ExREAL_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            # MC_REC_1D_Norm.SetTitle(str(MC_REC_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            # MC_GEN_1D_Norm.SetTitle(str(MC_GEN_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
            
            Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
            
            ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
            MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
            MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
            
            ExREAL_1D_Norm.GetXaxis().SetRangeUser(0, 360)
            MC_REC_1D_Norm.GetXaxis().SetRangeUser(0, 360)
            MC_GEN_1D_Norm.GetXaxis().SetRangeUser(0, 360)
            

            ExREAL_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            ExREAL_1D_Norm.GetYaxis().SetTitle("Normalized")
            ExREAL_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
            ExREAL_1D_Norm.SetLineColor(root_color.Blue)
            ExREAL_1D_Norm.SetLineWidth(2)
            ExREAL_1D_Norm.SetLineStyle(1)
            ExREAL_1D_Norm.SetMarkerColor(root_color.Blue)
            ExREAL_1D_Norm.SetMarkerSize(1)
            ExREAL_1D_Norm.SetMarkerStyle(21)
            #####==========#####      MC REC Histogram       #####==========##### ################################################################
            MC_REC_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            MC_REC_1D_Norm.GetYaxis().SetTitle("Normalized")
            MC_REC_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
            MC_REC_1D_Norm.SetLineColor(root_color.Red)
            MC_REC_1D_Norm.SetLineWidth(2)
            MC_REC_1D_Norm.SetLineStyle(1)
            MC_REC_1D_Norm.SetMarkerColor(root_color.Red)
            MC_REC_1D_Norm.SetMarkerSize(1)
            MC_REC_1D_Norm.SetMarkerStyle(22)
            #####==========#####      MC GEN Histogram       #####==========##### ################################################################
            MC_GEN_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")
            MC_GEN_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
            MC_GEN_1D_Norm.SetLineColor(root_color.Green)
            MC_GEN_1D_Norm.SetLineWidth(3)
            MC_GEN_1D_Norm.SetLineStyle(1)
            MC_GEN_1D_Norm.SetMarkerColor(root_color.Green)
            MC_GEN_1D_Norm.SetMarkerSize(1)
            MC_GEN_1D_Norm.SetMarkerStyle(20)
            
            if(Fit_Test):
                try:
                    statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                except:
                    print("\nMC_GEN_1D IS NOT FITTED\n")
            
        except Exception as e:
            print("".join([color.BOLD, color.RED, "ERROR IN 1D (Input) Histograms:\n",        color.END, color.RED, str(traceback.format_exc()), color.END]))
    elif("Unfold" in str(Method)):
        try:
            Max_Unfolded, Min_Unfolded = 1, 0
            if(Multi_Dim_Option in ["Off"]):
                BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "Bayesian")]
                BAY_Histo_Unfold.Draw("H P E0 same")
                BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "Bin")]
                BIN_Histo_Unfold.Draw("H P E0 same")
                SVD_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name).replace("Data_Type", "SVD")]
                SVD_Histo_Unfold.Draw("H P E0 same")
                MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                # MC_GEN_1D_Unfold.Draw("H P E0 same")
                if(tdf not in ["N/A"]):
                    ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                    ExTRUE_1D_Unfold.Draw("H P E0 same")
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                else:
                    Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                    Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
            else:
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
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
            BAY_Histo_Unfold.GetXaxis().SetRangeUser(0,                360)
            BIN_Histo_Unfold.GetXaxis().SetRangeUser(0,                360)
            MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(0,                360)
            if(tdf not in ["N/A"]):
                ExTRUE_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(0,            360)
                #####==========#####    MC TRUE Histogram    #####==========##### ################################################################
                ExTRUE_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
                ExTRUE_1D_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                ExTRUE_1D_Unfold.SetLineColor(root_color.Cyan)
                ExTRUE_1D_Unfold.SetLineWidth(3)
                ExTRUE_1D_Unfold.SetLineStyle(1)
                ExTRUE_1D_Unfold.SetMarkerColor(root_color.Cyan)
                ExTRUE_1D_Unfold.SetMarkerSize(1)
                ExTRUE_1D_Unfold.SetMarkerStyle(20)
            if(Multi_Dim_Option in ["Off"]):
                SVD_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                SVD_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                #####==========#####      SVD Histogram      #####==========##### ################################################################
                SVD_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
                SVD_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                SVD_Histo_Unfold.SetLineColor(root_color.Pink)
                SVD_Histo_Unfold.SetLineWidth(2)
                SVD_Histo_Unfold.SetLineStyle(1)
                SVD_Histo_Unfold.SetMarkerColor(root_color.Pink)
                SVD_Histo_Unfold.SetMarkerSize(1)
                SVD_Histo_Unfold.SetMarkerStyle(20)
            
            #####==========#####     BAYESIAN Histogram      #####==========##### ################################################################
            BAY_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            BAY_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
            BAY_Histo_Unfold.SetLineColor(root_color.Teal)
            BAY_Histo_Unfold.SetLineWidth(2)
            BAY_Histo_Unfold.SetLineStyle(1)
            BAY_Histo_Unfold.SetMarkerColor(root_color.Teal)
            BAY_Histo_Unfold.SetMarkerSize(1)
            BAY_Histo_Unfold.SetMarkerStyle(21)
            #####==========#####    Bin-by-Bin Histogram     #####==========##### ################################################################
            BIN_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            BIN_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
            BIN_Histo_Unfold.SetLineColor(root_color.Brown)
            BIN_Histo_Unfold.SetLineWidth(2)
            BIN_Histo_Unfold.SetLineStyle(1)
            BIN_Histo_Unfold.SetMarkerColor(root_color.Brown)
            BIN_Histo_Unfold.SetMarkerSize(1)
            BIN_Histo_Unfold.SetMarkerStyle(22)
            #####==========#####      MC GEN Histogram       #####==========##### ################################################################
            MC_GEN_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_All_z_pT_Bins), "}}"]))
            MC_GEN_1D_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
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
                # try:
                #     statbox_move(Histogram=MC_GEN_1D_Unfold,     Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                # except:
                #     print("\nMC_GEN_1D_Unfold IS NOT FITTED\n")
                if(tdf not in ["N/A"]):
                    try:
                        statbox_move(Histogram=ExTRUE_1D_Unfold, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                    except:
                        print("\nExTRUE_1D_Unfold IS NOT FITTED\n")
                if(Multi_Dim_Option in ["Off"]):
                    try:
                        statbox_move(Histogram=SVD_Histo_Unfold, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                    except:
                        print("\nSVD_Histo_Unfold IS NOT FITTED\n")
            
        except Exception as e:
            print("".join([color.Error, "ERROR IN 1D (Input) Histograms:\n", color.END, color.BOLD, str(traceback.format_exc()), color.END]))
    else:
        
        Default_Histo_Name_Any     = str(Default_Histo_Name)
        if(Multi_Dim_Option not in ["Off"]):
            Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
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
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            # # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H PL E0 same")
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].Draw("H P E0 same")

            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")

            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetXaxis().SetRangeUser(0, 360)
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())))
            
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            # Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H PL E0 same")
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H P E0 same")
            
            configure_stat_box(hist=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))], show_entries=True, canvas=All_z_pT_Canvas_cd_1_Lower.cd(1))

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())))
            
            if(Fit_Test):
                if(Method not in ["rdf", "mdf"]):
                    try:
                        statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))], Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    except:
                        print("\nTHE SELECTED HISTOGRAM WAS NOT FITTED\n")

        except Exception as e:
            print("".join([color.BOLD, color.RED, "ERROR IN METHOD = '", str(Method), "':\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ####  Filling Canvas (Left) End ################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - i.e., Individual z-pT Bins  #####################################################################################################################################################################################################################################################################################################################################################
    if("Y_bin" not in Binning_Method):
        z_pT_Bin_Range = 42 if(str(Q2_Y_Bin) in ["2"]) else 36 if(str(Q2_Y_Bin) in ["4", "5", "9", "10"]) else 35 if(str(Q2_Y_Bin) in ["1", "3"]) else 30 if(str(Q2_Y_Bin) in ["6", "7", "8", "11"]) else 25 if(str(Q2_Y_Bin) in ["13", "14"]) else 20 if(str(Q2_Y_Bin) in ["12", "15", "16", "17"]) else 1
    else:
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1] - 1
        # # i.e.,      = [Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2][1] - 1 where (Migration_Bin_1 - 1) is the last non-migration bin (without removing from the main grid)
    for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
        
        if("Y_bin" not in Binning_Method):
            if(((Q2_Y_Bin in [1]) and (z_pT_Bin in [28, 34, 35])) or ((Q2_Y_Bin in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or (Q2_Y_Bin in [3] and z_pT_Bin in [28, 35]) or (Q2_Y_Bin in [4] and z_pT_Bin in [6, 36]) or (Q2_Y_Bin in [5] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [6] and z_pT_Bin in [30]) or (Q2_Y_Bin in [7] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [9] and z_pT_Bin in [36]) or (Q2_Y_Bin in [10] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [11] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [13, 14] and z_pT_Bin in [25]) or (Q2_Y_Bin in [15, 16, 17] and z_pT_Bin in [20])):
                continue
        
        Bin_Title_z_pT_Bin              = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(str(z_pT_Bin) not in ["0"]) else "All"]), "}}}"])
        Default_Histo_Name_z_pT_Bin     = str(Default_Histo_Name.replace("z_pT_Bin_All",     "".join(["z_pT_Bin_", str(z_pT_Bin)])))
        if((Multi_Dim_Option not in ["Off"]) and ("Response" not in str(Method))):
            if("y" in Binning_Method):
                Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
            else:
                Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_Y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
        if(str(Method) in ["rdf", "gdf", "tdf"]):
            Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("Smear", "''" if((not Sim_Test) or (str(Method) in ["gdf", "tdf"])) else "Smear"))
        
        
        if("Y_bin" in Binning_Method):
            cd_number_of_z_pT_all_together = FindCanvas_cd_Kinematic_Bins(Bin_Name="", Q2_y_Bin_Input=Q2_Y_Bin, z_pT_Bin_Input=z_pT_Bin)
        else:
            cd_number_of_z_pT_all_together = z_pT_Bin
        
            
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
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''" if(not Sim_Test) else "Smear")).replace("Data_Type", "rdf")].DrawNormalized("H P E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf"))].DrawNormalized("H P E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H P E0 same")
                
                ExREAL_1D_Norm.SetTitle(str(ExREAL_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                MC_REC_1D_Norm.SetTitle(str(MC_REC_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))
                MC_GEN_1D_Norm.SetTitle(str(MC_GEN_1D_Norm.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Multi-Dimensional Unfolding" if(Multi_Dim_Option in ["Only"]) else ""))

                Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
                
                ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
                MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
                MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
                
                ExREAL_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                MC_REC_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                MC_GEN_1D_Norm.GetXaxis().SetRangeUser(0, 360)
                
                ExREAL_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                ExREAL_1D_Norm.GetYaxis().SetTitle("Normalized")
                ExREAL_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                ExREAL_1D_Norm.SetLineColor(root_color.Blue)
                ExREAL_1D_Norm.SetLineWidth(2)
                ExREAL_1D_Norm.SetLineStyle(1)
                ExREAL_1D_Norm.SetMarkerColor(root_color.Blue)
                ExREAL_1D_Norm.SetMarkerSize(1)
                ExREAL_1D_Norm.SetMarkerStyle(21)
                #####==========#####      MC REC Histogram       #####==========##### ################################################################
                MC_REC_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                MC_REC_1D_Norm.GetYaxis().SetTitle("Normalized")
                MC_REC_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                MC_REC_1D_Norm.SetLineColor(root_color.Red)
                MC_REC_1D_Norm.SetLineWidth(2)
                MC_REC_1D_Norm.SetLineStyle(1)
                MC_REC_1D_Norm.SetMarkerColor(root_color.Red)
                MC_REC_1D_Norm.SetMarkerSize(1)
                MC_REC_1D_Norm.SetMarkerStyle(22)
                #####==========#####      MC GEN Histogram       #####==========##### ################################################################
                MC_GEN_1D_Norm.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")
                MC_GEN_1D_Norm.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                MC_GEN_1D_Norm.SetLineColor(root_color.Green)
                MC_GEN_1D_Norm.SetLineWidth(3)
                MC_GEN_1D_Norm.SetLineStyle(1)
                MC_GEN_1D_Norm.SetMarkerColor(root_color.Green)
                MC_GEN_1D_Norm.SetMarkerSize(1)
                MC_GEN_1D_Norm.SetMarkerStyle(20)
                MC_GEN_1D_Norm.GetYaxis().SetTitle("Normalized")

                if(Fit_Test):
                    try:
                        statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    except:
                        print(color.RED, "\nMC_GEN_1D IS NOT FITTED\n", color.END)
                
            except Exception as e:
                print("".join([color.Error, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") 1D (Input) Histograms:\n", color.END, color.BOLD, str(traceback.format_exc()), color.END]))
                
        elif("Unfold" in str(Method)):
            try:
                Max_Unfolded, Min_Unfolded = 1, 0
                if(Multi_Dim_Option in ["Off"]):
                    BAY_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "Bayesian")]
                    BAY_Histo_Unfold.Draw("H P E0 same")
                    BIN_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "Bin")]
                    BIN_Histo_Unfold.Draw("H P E0 same")
                    SVD_Histo_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin).replace("Data_Type", "SVD")]
                    SVD_Histo_Unfold.Draw("H P E0 same")
                    MC_GEN_1D_Unfold     = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",      "''")).replace("Data_Type", "gdf")]
                    # MC_GEN_1D_Unfold.Draw("H P E0 same")
                    if(tdf not in ["N/A"]):
                        ExTRUE_1D_Unfold = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",      "''")).replace("Data_Type", "tdf")]
                        ExTRUE_1D_Unfold.Draw("H P E0 same")
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin()), ExTRUE_1D_Unfold.GetBinContent(ExTRUE_1D_Unfold.GetMinimumBin())])
                    else:
                        Max_Unfolded     = max([1, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMaximumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMaximumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMaximumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMaximumBin())])
                        Min_Unfolded     = min([0, BAY_Histo_Unfold.GetBinContent(BAY_Histo_Unfold.GetMinimumBin()), BIN_Histo_Unfold.GetBinContent(BIN_Histo_Unfold.GetMinimumBin()), SVD_Histo_Unfold.GetBinContent(SVD_Histo_Unfold.GetMinimumBin()), MC_GEN_1D_Unfold.GetBinContent(MC_GEN_1D_Unfold.GetMinimumBin())])
                else:
                    Default_Histo_Name_Multi_Dim = str(Default_Histo_Name_z_pT_Bin.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
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
                BAY_Histo_Unfold.GetXaxis().SetRangeUser(0,                360)
                BIN_Histo_Unfold.GetXaxis().SetRangeUser(0,                360)
                MC_GEN_1D_Unfold.GetXaxis().SetRangeUser(0,                360)
                if(tdf not in ["N/A"]):
                    ExTRUE_1D_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                    ExTRUE_1D_Unfold.GetXaxis().SetRangeUser(0,            360)
                    #####==========#####    MC TRUE Histogram    #####==========##### ################################################################
                    ExTRUE_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                    ExTRUE_1D_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                    ExTRUE_1D_Unfold.SetLineColor(root_color.Cyan)
                    ExTRUE_1D_Unfold.SetLineWidth(3)
                    ExTRUE_1D_Unfold.SetLineStyle(1)
                    ExTRUE_1D_Unfold.SetMarkerColor(root_color.Cyan)
                    ExTRUE_1D_Unfold.SetMarkerSize(1)
                    ExTRUE_1D_Unfold.SetMarkerStyle(20)
                if(Multi_Dim_Option in ["Off"]):
                    SVD_Histo_Unfold.GetYaxis().SetRangeUser(Min_Unfolded, 1.3*Max_Unfolded)
                    SVD_Histo_Unfold.GetXaxis().SetRangeUser(0,            360)
                    #####==========#####      SVD Histogram      #####==========##### ################################################################
                    SVD_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                    SVD_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                    SVD_Histo_Unfold.SetLineColor(root_color.Pink)
                    SVD_Histo_Unfold.SetLineWidth(2)
                    SVD_Histo_Unfold.SetLineStyle(1)
                    SVD_Histo_Unfold.SetMarkerColor(root_color.Pink)
                    SVD_Histo_Unfold.SetMarkerSize(1)
                    SVD_Histo_Unfold.SetMarkerStyle(20)

                #####==========#####     BAYESIAN Histogram      #####==========##### ################################################################
                BAY_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                BAY_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                BAY_Histo_Unfold.SetLineColor(root_color.Teal)
                BAY_Histo_Unfold.SetLineWidth(2)
                BAY_Histo_Unfold.SetLineStyle(1)
                BAY_Histo_Unfold.SetMarkerColor(root_color.Teal)
                BAY_Histo_Unfold.SetMarkerSize(1)
                BAY_Histo_Unfold.SetMarkerStyle(21)
                #####==========#####    Bin-by-Bin Histogram     #####==========##### ################################################################
                BIN_Histo_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                BIN_Histo_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
                BIN_Histo_Unfold.SetLineColor(root_color.Brown)
                BIN_Histo_Unfold.SetLineWidth(2)
                BIN_Histo_Unfold.SetLineStyle(1)
                BIN_Histo_Unfold.SetMarkerColor(root_color.Brown)
                BIN_Histo_Unfold.SetMarkerSize(1)
                BIN_Histo_Unfold.SetMarkerStyle(22)
                #####==========#####      MC GEN Histogram       #####==========##### ################################################################
                MC_GEN_1D_Unfold.SetTitle("".join(["#splitline{#scale[1.5]{", "Multi-Dimensional Unfolding" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolding", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}"]))
                MC_GEN_1D_Unfold.GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")
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
                    # try:
                    #     statbox_move(Histogram=MC_GEN_1D_Unfold,     Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                    # except:
                    #     print(color.RED, "\nMC_GEN_1D_Unfold IS NOT FITTED\n", color.END)
                    if(tdf not in ["N/A"]):
                        try:
                            statbox_move(Histogram=ExTRUE_1D_Unfold, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                        except:
                            print(color.RED, "\nExTRUE_1D_Unfold IS NOT FITTED\n", color.END)
                    if(Multi_Dim_Option in ["Off"]):
                        try:
                            statbox_move(Histogram=SVD_Histo_Unfold, Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Print_Method="off")
                        except:
                            print(color.RED, "\nSVD_Histo_Unfold IS NOT FITTED\n", color.END)

            except Exception as e:
                print("".join([color.Error, "ERROR IN 1D (Input) Histograms:\n", color.END, color.BOLD, str(traceback.format_exc()), color.END]))
            
        elif("Response" in str(Method)):
            try:
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].Draw("col")
            except Exception as e:
                print("".join([color.BOLD, color.RED, "ERROR IN (z-pT Bin ", str(z_pT_Bin), ") Response Matrix:\n",              color.END, color.BOLD, str(traceback.format_exc()), color.END]))
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
            #####==========#####      MC REC Histogram       #####==========##### ################################################################
            if(str(Method) in ["mdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Red)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Red)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(22)
            #####==========#####      MC GEN Histogram       #####==========##### ################################################################
            if(str(Method) in ["gdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Green)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(3)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Green)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(20)
            #####==========#####      MC True Histogram      #####==========##### ################################################################
            if(str(Method) in ["tdf"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Cyan)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(3)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Cyan)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(20)
            #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################
            if(str(Method) in ["Bin", "bbb", "bin", "Bin-by-Bin", "Bin-By-Bin", "Bin-by-bin", "bin-by-bin"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Brown)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Brown)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1.5)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####   Unfold Bayes Histogram    #####==========##### ################################################################
            if(str(Method) in ["Bayesian", "Bayes"]):
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(root_color.Teal)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(root_color.Teal)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerSize(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerStyle(21)
            #####==========#####    Unfold SVD Histogram     #####==========##### ################################################################
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
            
            
            try:
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                # # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].Draw("H PL E0 same")
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].Draw("H P E0 same")
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetXaxis().SetRangeUser(0, 360)
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf"))].GetMaximumBin())))
                
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                # Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].Draw("H PL E0 same")
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].Draw("H P E0 same")
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetMaximumBin())))
                
                if(Fit_Test):
                    if(Method not in ["rdf", "mdf"]):
                        try:
                            statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))], Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                        except:
                            print(color.RED, "\nTHE SELECTED HISTOGRAM WAS NOT FITTED\n", color.END)
                            
                        # Below Sets Fill Color of Pads in the images which show the z-pT bins together (Used to help search for poor fits)
                        if(not True):
                            try:
                                if((get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))]) is not None) and (get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))]) > (9050 if(not Closure_Test) else 10))):
                                    print("Poor fit for:\n", str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method)), "\n\tchi^2 =", str(get_chisquare(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))])))
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
                                    print(color.Error, "\n\n\nERROR WITH get_fit_parameters_B_and_C(...)\n\n\n", color.END)
                                    print("Traceback:\n", str(traceback.format_exc()))
                        
            except Exception as e:
                print("".join([color.BOLD, color.RED, "ERROR IN (z-pT Bin", str(z_pT_Bin), ") METHOD = '", str(Method), "':\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

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
    if(Multi_Dim_Option not in ["Off"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = "".join(["Sim_Test_",  str(Save_Name)])
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                      "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                "z_pT_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                "z_pT_phi_h")
    Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]), str(File_Save_Format))
    Save_Name = Save_Name.replace("__",                                  "_")
    if(Cut_Option not in ["Cut"]):
        Save_Name = Save_Name.replace(str(File_Save_Format),             "".join(["_UnCut", str(File_Save_Format)]))
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            All_z_pT_Canvas.SetName(Save_Name.replace(".root", ""))
        All_z_pT_Canvas.SaveAs(Save_Name)
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    
    
    
##################################################################################################################################################################
##==========##==========## Function for Creating the Images for All z-pT Bins Together  ##==========##==========##==========##==========##==========##==========##
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
# Common_Name = "Unfolding_Tests_V13_All"
# Common_Name = "Analysis_Note_Update_V4_All"
# Common_Name = "Multi_Dimension_Unfold_V1_All"
# # Common_Name = "Multi_Dimension_Unfold_V2_All"
# Common_Name = "Multi_Dimension_Unfold_V3_All"
# Common_Name = "Analysis_Note_Update_VF_APS_All"

# Common_Name = "New_Binning_Schemes_V8_All"

Common_Name = "Gen_Cuts_V6_All"
# Common_Name = "Gen_Cuts_V7_All"
Common_Name = "Gen_Cuts_V8_All"

# Common_Name = "New_Bin_Tests_V5_All"

# Common_Name = "CrossCheck_V2_All"

# Use unique file(s) for one of datatypes? (If so, set the following if(...) conditions to 'False')

##################################
##   Real (Experimental) Data   ##
##################################
if(True):
#     print("".join([color.BOLD, "\nNot using the common file name for the Real (Experimental) Data...\n", color.END]))
# if(False):
    REAL_File_Name = Common_Name
else:
    REAL_File_Name = "Unfolding_Tests_V11_All"
##################################
##   Real (Experimental) Data   ##
##################################

########################################
##   Reconstructed Monte Carlo Data   ##
########################################
if(True):
#     print("".join([color.BOLD, "\nNot using the common file name for the Reconstructed Monte Carlo Data...\n", color.END]))
# if(False):
    MC_REC_File_Name = Common_Name
else:
    MC_REC_File_Name = "Unfolding_Tests_V13_Failed_All"
    MC_REC_File_Name = "Analysis_Note_Update_V6_All"
    MC_REC_File_Name = "Gen_Cuts_V2_Fixed_All"
    MC_REC_File_Name = "CrossCheck_V3_All"
########################################
##   Reconstructed Monte Carlo Data   ##
########################################

####################################
##   Generated Monte Carlo Data   ##
####################################
if(True):
#     print("".join([color.BOLD, "\nNot using the common file name for the Generated Monte Carlo Data...\n", color.END]))
# if(False):
    MC_GEN_File_Name = Common_Name
else:
    MC_GEN_File_Name = "Unfolding_Tests_V11_All"
    MC_GEN_File_Name = "Gen_Cuts_V2_Fixed_All"
####################################
##   Generated Monte Carlo Data   ##
####################################



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
    print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
try:
    mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
    print("".join(["The total number of histograms available for the", color.RED,   " Reconstructed Monte Carlo Data", " " if(not Sim_Test) else "     ",                                                     color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
try:
    gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
    print("".join(["The total number of histograms available for the", color.GREEN, " Generated Monte Carlo Data", "     " if(not Sim_Test) else "         ",                                                 color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
    
if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])):
    print("\nWill be using a file as the 'True' distribution (i.e., what 'rdf' should look like after unfolding)")
    try:
        tdf = ROOT.TFile(str(FileLocation(str(TRUE_File_Name), "gdf")), "READ")
        print("".join(["The total number of histograms available for the", color.CYAN, " 'True' Monte Carlo Data   ", "     " if(not Sim_Test) else "         ",                                              color.END, " in '", color.BOLD, TRUE_File_Name,   color.END, "' is ", color.BOLD, str(len(tdf.GetListOfKeys())), color.END]))
    except:
        print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'tdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
else:
    tdf = "N/A"
###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################


String_For_Output_txt = "".join([color.BOLD, """
######################################################################################################################################################
##==========##    COMPARISON OF DATA TO MONTE CARLO FOR RELEVANT KINEMATIC VARIABLES    ##==========##==========##==========##==========##==========##
######################################################################################################################################################
""", color.END, str(str(Date_Time).replace("Started running", "Ran")).replace("\n", ""), """
""", str(str(("".join(["Ran for Q2-y Bin(s): ", str(Q2_xB_Bin_List)]).replace("[",  "")).replace("]", "")).replace("'0'", "'All'")), """

Files Used:
""", "".join(["\tFile name for ", color.BLUE,  "Real (Experimental) Data"            if(not Sim_Test) else " Test Experimental (Simulated) Data", " " if(Sim_Test) else "       ", color.END, " in '", color.BOLD, REAL_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(REAL_File_Name),   "rdf")))]), """
""", "".join(["\tFile name for ", color.RED,   "Reconstructed Monte Carlo Data", " " if(not Sim_Test) else "     ",                                                                color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_REC_File_Name), "mdf")))]), """
""", "".join(["\tFile name for ", color.GREEN, "Generated Monte Carlo Data", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is \n\t\t", str(str(FileLocation(str(MC_GEN_File_Name), "gdf")))]), """
""", "".join(["\tFile name for ", color.CYAN,  "'True' Monte Carlo Data   ", "     " if(not Sim_Test) else "         ",                                                            color.END, " in '", color.BOLD, TRUE_File_Name,   color.END, "' is \n\t\t", str(str(FileLocation(str(TRUE_File_Name),   "gdf"))),   "\n"]) if((Sim_Test) or (Closure_Test) or (TRUE_File_Name not in [""])) else "", """
##=========================================================##
##==========##   Starting to Run Comparisons   ##==========##
##=========================================================##"""])

# Set String_For_Output_txt = "" to stop the comparison from printing the text-based results

print("".join(["\n\n", color.BOLD, "Done Loading RDataFrame files...\n", color.END]))


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











print("".join([color.BOLD, color.BLUE, "\n\nStarting Unfolding Procedures...\n", color.END]))
# Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods, Parameter_List_Unfold, Parameter_List_Bin = {}, {}, {}, {}, {}, {}, {}, {}, [], []
Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods = {}, {}, {}, {}, {}, {}, {}, {}
Parameter_List_Unfold_Methods["SVD"], Parameter_List_Unfold_Methods["Bin"], Parameter_List_Unfold_Methods["Bayes"] = [], [], []
List_of_All_Histos_For_Unfolding = {}
count, count_failed = 0, 0
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName()).replace("mdf", "DataFrame_Type")
    
    # print("out_print_main =", out_print_main)
    
    ##========================================================##
    ##=====##    Conditions for Histogram Selection    ##=====##
    ##========================================================##
    
    Conditions_For_Unfolding = ["DataFrame_Type" in str(out_print_main)]
    # The histograms for 'out_print_main' will be skipped if any item in the list 'Conditions_For_Unfolding' is 'False'
    
    ## Correct Histogram Type:
    Conditions_For_Unfolding.append('''"Response_Matrix_Normal" in str(out_print_main)''')
    Conditions_For_Unfolding.append("Response_Matrix_Normal"    in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"Response_Matrix_Normal_1D" not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Response_Matrix_Normal_1D"    not in str(out_print_main))
    
    ## Correct Cuts:
    Conditions_For_Unfolding.append('''"no_cut"             not in str(out_print_main)''')
    Conditions_For_Unfolding.append("no_cut"                not in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"cut_Complete_EDIS"  not in str(out_print_main)''')
    Conditions_For_Unfolding.append("cut_Complete_EDIS"     not in str(out_print_main))
    
    ## Generated Missing Mass Cuts (not ready yet)
    if(Common_Name not in ["Gen_Cuts_V7_All"]):
        Conditions_For_Unfolding.append('''"Gen_MM_Cut"     not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Gen_MM_Cut"        not in str(out_print_main))
        Conditions_For_Unfolding.append('''"Gen_Cut_MM"     not in str(out_print_main)''')
        Conditions_For_Unfolding.append("Gen_Cut_MM"        not in str(out_print_main))
    

    ## Correct Variable(s):
    Conditions_For_Unfolding.append('''"phi_t" in str(out_print_main)''')
    Conditions_For_Unfolding.append("phi_t"    in str(out_print_main))
    # Conditions_For_Unfolding.append("'phi_t"      not in str(out_print_main))
    # Conditions_For_Unfolding.append("Multi_Dim_" not in str(out_print_main)) # For removing all Multidimensional Unfolding Plots
    # Conditions_For_Unfolding.append("Multi_Dim_"     in str(out_print_main)) # For running only Multidimensional Unfolding Plots
    # Conditions_For_Unfolding.append("Var-D1='MM"     in str(out_print_main))
    # if(Closure_Test):
    #     Conditions_For_Unfolding.append("'Multi_Dim_z_pT_Bin_y_bin_phi_t"      in str(out_print_main))
    
    if("y" in Binning_Method):
        Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
        Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)
    else:
        Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_Y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
        Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_Y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)
    
    Conditions_For_Unfolding.append('''"Multi_Dim_Q2_phi_t"               not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_Q2_phi_t"                  not in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t"    not in str(out_print_main))
    
    # Not Tested Yet...
    Conditions_For_Unfolding.append('''"Multi_Dim_elth_phi_t"  not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_elth_phi_t"     not in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"Multi_Dim_pipth_phi_t" not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_pipth_phi_t"    not in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"Multi_Dim_elPhi_phi_t" not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_elPhi_phi_t"    not in str(out_print_main))
    
    Conditions_For_Unfolding.append('''"Multi_Dim_pipPhi_phi_t not in str(out_print_main)''')
    Conditions_For_Unfolding.append("Multi_Dim_pipPhi_phi_t"   not in str(out_print_main))
    # Conditions_For_Unfolding.append(("Multi_Dim_elth_phi_t" in str(out_print_main)) or ("Multi_Dim_pipth_phi_t" in str(out_print_main)) or ("Multi_Dim_elPhi_phi_t" in str(out_print_main)) or ("Multi_Dim_pipPhi_phi_t" in str(out_print_main)))
    
    
    ## Correct Binning:
    # Conditions_For_Unfolding.append("Q2-xB-Bin=1" in str(out_print_main))
    # Conditions_For_Unfolding.append("Q2-xB-Bin=All" not in str(out_print_main))
    
    # Smearing Options:
    # if((Smearing_Options not in ["no_smear", "both"]) or  (Sim_Test)):
    if((Smearing_Options not in ["no_smear", "both"])):
        Conditions_For_Unfolding.append('''"(Smear-Type='')" not in str(out_print_main)''')
        Conditions_For_Unfolding.append("(Smear-Type='')"    not in str(out_print_main))
    # if((Smearing_Options not in ["smear",    "both"]) and (not Sim_Test)):
    if((Smearing_Options not in ["smear",    "both"])):
        Conditions_For_Unfolding.append('''"(Smear-Type='')"     in str(out_print_main)''')
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

        out_print_main_rdf = out_print_main.replace("DataFrame_Type", "rdf" if(not Sim_Test) else "mdf")
        out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
        out_print_main_gdf = out_print_main.replace("DataFrame_Type", "gdf")

        ################################################################################
        ##=============##    Removing Cuts from the Generated files    ##=============##
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_EDIS",  "no_cut")
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_SIDIS", "no_cut")
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete",       "no_cut")
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
            print("".join([color.Error, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
            continue

        out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
        if(("".join([", (Var-D2='z_pT_Bin", str(Binning_Method)]) not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
            out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "".join(["]), (Var-D2='z_pT_Bin", str(Binning_Method), "" if("smear" not in str(out_print_main_mdf_1D)) else "_smeared", "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
        if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf_1D), color.END, "\n"]))
            for ii in mdf.GetListOfKeys():
                if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                    print(str(ii.GetName()))
                    
        if(Sim_Test):
            out_print_main_rdf = out_print_main_mdf_1D
            out_print_main_tdf = out_print_main_gdf
            if(tdf not in ["N/A"]):
                if(out_print_main_tdf not in tdf.GetListOfKeys()):
                    print("".join([color.Error, "ERROR IN TDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.CYAN,  str(out_print_main_tdf), color.END, "\n"]))
                    continue
            else:
                print("".join([color.Error,     "ERROR IN TDF...\n", color.END, color.RED, "Missing Dataframe...",   color.END, "\n"]))
        if(out_print_main_rdf not in rdf.GetListOfKeys()):
            print("".join([color.Error,         "ERROR IN RDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.BLUE,  str(out_print_main_rdf), color.END, "\n"]))
            continue
        if(out_print_main_gdf not in gdf.GetListOfKeys()):
            print("".join([color.Error,         "ERROR IN GDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.GREEN, str(out_print_main_gdf), color.END, "\n"]))
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
        
        # Getting MC Background Histogram (bgs - stands for BackGroundSubtraction)
        out_print_main_bdf_1D = out_print_main_mdf_1D.replace("'Response_Matrix_1D'", "'Background_Response_Matrix_1D''")
        if(out_print_main_bdf_1D in mdf.GetListOfKeys()):
            MC_BGS_1D_initial = mdf.Get(out_print_main_bdf_1D)
        else:
            MC_BGS_1D_initial = "None"
        
        # Use_Gen_MM_Cut = True
        Use_Gen_MM_Cut = False
        
        if(("Gen_MM_Cut" in str(out_print_main_rdf)) or ("Gen_MM_Cut" in str(out_print_main_mdf_1D)) or ("Gen_MM_Cut" in str(out_print_main_gdf))  or ("Gen_MM_Cut" in str(out_print_main_mdf))):
            if((not Use_Gen_MM_Cut) and (Common_Name not in ["Gen_Cuts_V7_All"])):
                print(color.Error, "\nERROR: NOT TRYING TO RUN Gen_MM_Cut\n", color.END)
                continue
            print(color.BLUE, color.BOLD, "INCLUDES Gen_MM_Cut", color.END)
            # print("out_print_main_rdf    =", out_print_main_rdf)
            # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
            # print("out_print_main_gdf    =", out_print_main_gdf)
            # print("out_print_main_mdf    =", out_print_main_mdf)
            
            # if(Use_Gen_MM_Cut):
            if(abs(Response_2D_initial.GetZaxis().GetXmin()) == abs(Response_2D_initial.GetZaxis().GetXmax()) == 1.5):                    
                Response_2D_initial = Response_2D_initial.Project3D("yx e")
                Response_2D_initial.SetTitle(str(Response_2D_initial.GetTitle()).replace(" yx projection", ""))
            else:
                print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut Response Matrix", color.END, "\nResponse_2D_initial = ", Response_2D_initial)
                FAIL
                
            if("3D" in str(type(MC_REC_1D_initial))):
                if(abs(MC_REC_1D_initial.GetZaxis().GetXmin()) == abs(MC_REC_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                    MC_REC_1D_initial = MC_REC_1D_initial.Project3D("yx e")
                    MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" yx projection", ""))
                else:
                    print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC REC HISTO", color.END, "\nMC_REC_1D_initial = ", MC_REC_1D_initial)
                    FAIL
            else:
                if(abs(MC_REC_1D_initial.GetYaxis().GetXmin()) == abs(MC_REC_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                    MC_REC_1D_initial = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()), 0, -1, "e")
                    MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" x projection", ""))
                else:
                    print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC REC HISTO", color.END, "\nMC_REC_1D_initial = ", MC_REC_1D_initial)
                    FAIL
                    
            if("3D" in str(type(MC_GEN_1D_initial))):
                if(abs(MC_GEN_1D_initial.GetZaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                    MC_GEN_1D_initial = MC_GEN_1D_initial.Project3D("yx e")
                    MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" yx projection", ""))
                else:
                    print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC GEN HISTO", color.END, "\nMC_GEN_1D_initial = ", MC_GEN_1D_initial)
                    FAIL
            else:
                if(abs(MC_GEN_1D_initial.GetYaxis().GetXmin()) == abs(MC_GEN_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                    MC_GEN_1D_initial = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()), 0, -1, "e")
                    MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace(" x projection", ""))
                else:
                    print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC GEN HISTO", color.END, "\nMC_GEN_1D_initial = ", MC_GEN_1D_initial)
                    FAIL
                    
            if(tdf not in ["N/A"]):
                if("3D" in str(type(ExTRUE_1D_initial))):
                    if(abs(ExTRUE_1D_initial.GetZaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        ExTRUE_1D_initial = ExTRUE_1D_initial.Project3D("yx e")
                        ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" yx projection", ""))
                    else:
                        print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC TRUE HISTO", color.END, "\nExTRUE_1D_initial = ", ExTRUE_1D_initial)
                        FAIL
                else:
                    if(abs(ExTRUE_1D_initial.GetYaxis().GetXmin()) == abs(ExTRUE_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                        ExTRUE_1D_initial = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()), 0, -1, "e")
                        ExTRUE_1D_initial.SetTitle(str(ExTRUE_1D_initial.GetTitle()).replace(" x projection", ""))
                    else:
                        print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC TRUE HISTO", color.END, "\nExTRUE_1D_initial = ", ExTRUE_1D_initial)
                        FAIL
                        
            if(MC_BGS_1D_initial != "None"):
                if("3D" in str(type(MC_BGS_1D_initial))):
                    if(abs(MC_BGS_1D_initial.GetZaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                        MC_BGS_1D_initial = MC_BGS_1D_initial.Project3D("yx e")
                        MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" yx projection", ""))
                    else:
                        print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC BGS HISTO", color.END, "\nMC_BGS_1D_initial = ", MC_BGS_1D_initial)
                        FAIL
                else:
                    if(abs(MC_BGS_1D_initial.GetYaxis().GetXmin()) == abs(MC_BGS_1D_initial.GetYaxis().GetXmax()) == 1.5):                    
                        MC_BGS_1D_initial = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()), 0, -1, "e")
                        MC_BGS_1D_initial.SetTitle(str(MC_BGS_1D_initial.GetTitle()).replace(" x projection", ""))
                    else:
                        print(color.ERROR, "\n\nERROR WITH Gen_MM_Cut MC BGS HISTO", color.END, "\nMC_BGS_1D_initial = ", MC_BGS_1D_initial)
                        FAIL
                    
        elif(Common_Name in ["Gen_Cuts_V7_All"]):
            if("3D" in str(type(ExREAL_1D_initial))):
                # print(color.BLUE, color.BOLD, "\n\n\n\nExREAL_1D_initial.GetZaxis().GetTitle() =", ExREAL_1D_initial.GetZaxis().GetTitle(), color.END)
                # print("out_print_main_rdf    =", out_print_main_rdf)
                # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                # print("out_print_main_gdf    =", out_print_main_gdf)
                # print("out_print_main_mdf    =", out_print_main_mdf)
                if(abs(ExREAL_1D_initial.GetZaxis().GetXmin()) == abs(ExREAL_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                    ExREAL_1D_initial = ExREAL_1D_initial.Project3D("yx e")
                    ExREAL_1D_initial.SetTitle(str(ExREAL_1D_initial.GetTitle()).replace(" yx projection", ""))
            if("3D" in str(type(MC_REC_1D_initial))):
                # print(color.RED, color.BOLD, "\n\n\n\nMC_REC_1D_initial.GetZaxis().GetTitle() =", MC_REC_1D_initial.GetZaxis().GetTitle(), color.END)
                # print("out_print_main_rdf    =", out_print_main_rdf)
                # print("out_print_main_mdf_1D =", out_print_main_mdf_1D)
                # print("out_print_main_gdf    =", out_print_main_gdf)
                # print("out_print_main_mdf    =", out_print_main_mdf)
                if(abs(MC_REC_1D_initial.GetZaxis().GetXmin()) == abs(MC_REC_1D_initial.GetZaxis().GetXmax()) == 1.5):                    
                    MC_REC_1D_initial = MC_REC_1D_initial.Project3D("yx e")
                    MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace(" yx projection", ""))
                # print("MC_REC_1D_initial.GetTitle() =", MC_REC_1D_initial.GetTitle())
            if("3D" in str(type(MC_GEN_1D_initial))):
                # print(color.GREEN, color.BOLD, "\n\n\n\nMC_GEN_1D_initial.GetZaxis().GetTitle() =", MC_GEN_1D_initial.GetZaxis().GetTitle(), color.END)
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
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_xB_Bin_Unfold)[1] - 1
        
        for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                if(((Q2_xB_Bin_Unfold in [1, 2]) and (z_pT_Bin_Unfold in [49])) or (Q2_xB_Bin_Unfold == 3 and z_pT_Bin_Unfold in [49, 48, 42]) or (Q2_xB_Bin_Unfold in [1, 4] and z_pT_Bin_Unfold in [42]) or (Q2_xB_Bin_Unfold == 5 and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold == 7 and z_pT_Bin_Unfold in [25])):
                    continue
            elif("Y_bin" not in Binning_Method):
                # if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [42, 48, 49])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [42, 49])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [7, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [6, 7, 14, 28, 35, 41, 42]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [7, 35, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [8] and z_pT_Bin_Unfold in [5, 6, 36]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [24, 29, 30]) or (Q2_xB_Bin_Unfold in [11, 12] and z_pT_Bin_Unfold in [30, 35, 36])  or (Q2_xB_Bin_Unfold in [13] and z_pT_Bin_Unfold in [5, 20, 24, 25])):
                #     # print("Testing z_pT_Bin_Unfold...")
                #     continue
                #
                # if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [42, 48, 49])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [42, 49])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [42, 48, 49]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [7, 28, 35, 41, 42]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [7, 42, 48, 49]) or (Q2_xB_Bin_Unfold in [8] and z_pT_Bin_Unfold in [6, 36]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [11] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [14] and z_pT_Bin_Unfold in [25]) or (Q2_xB_Bin_Unfold in [15, 16, 17] and z_pT_Bin_Unfold in [20])):
                #     continue
                if(((Q2_xB_Bin_Unfold in [1]) and (z_pT_Bin_Unfold in [28, 34, 35])) or ((Q2_xB_Bin_Unfold in [2]) and (z_pT_Bin_Unfold in [28, 35, 41, 42])) or (Q2_xB_Bin_Unfold in [3] and z_pT_Bin_Unfold in [28, 35]) or (Q2_xB_Bin_Unfold in [4] and z_pT_Bin_Unfold in [6, 36]) or (Q2_xB_Bin_Unfold in [5] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [6] and z_pT_Bin_Unfold in [30]) or (Q2_xB_Bin_Unfold in [7] and z_pT_Bin_Unfold in [24, 30]) or (Q2_xB_Bin_Unfold in [9] and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold in [10] and z_pT_Bin_Unfold in [30, 36]) or (Q2_xB_Bin_Unfold in [11] and z_pT_Bin_Unfold in [24, 30]) or (Q2_xB_Bin_Unfold in [13, 14] and z_pT_Bin_Unfold in [25]) or (Q2_xB_Bin_Unfold in [15, 16, 17] and z_pT_Bin_Unfold in [20])):
                    continue
                
            # # For Selecting specific z-pT Bins
            # if(z_pT_Bin_Unfold not in [0, 10]):
            #     continue

    #########################################################
    ##===============##     3D Slices     ##===============##

            if("3D" in str(type(Response_2D_initial))):
                try:
                    bin_Response_2D_0, bin_Response_2D_1 = Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else Response_2D_initial.GetNbinsZ())
                    if(z_pT_Bin_Unfold != 0):
                        Response_2D_initial.GetZaxis().SetRange(bin_Response_2D_0, bin_Response_2D_1)
                    Response_2D           = Response_2D_initial.Project3D('yx e')
                    Response_2D.SetName(str(Response_2D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])))
                    if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                        Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))                        
                    Response_2D.SetTitle(Response_2D_Title_New)
                    # print(str(Response_2D.GetTitle()))
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (Response_2D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                Response_2D = Response_2D_initial

    ##===============##     3D Slices     ##===============##
    #########################################################


    #########################################################
    ##===============##     2D Slices     ##===============##
            if("2D" in str(type(ExREAL_1D_initial))):
                try:
                    bin_ExREAL_1D_0, bin_ExREAL_1D_1 = ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExREAL_1D_initial.GetNbinsY())
                    ExREAL_1D                        = ExREAL_1D_initial.ProjectionX(str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExREAL_1D_0, bin_ExREAL_1D_1, "e")
                    if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                        ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    ExREAL_1D.SetTitle(ExREAL_1D_Title_New)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (ExREAL_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                # print("\nExREAL_1D already is a 1D Histogram...")
                ExREAL_1D = ExREAL_1D_initial

            if("2D" in str(type(MC_REC_1D_initial))):
                try:
                    bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                    MC_REC_1D                        = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_REC_1D_0, bin_MC_REC_1D_1, "e")
                    if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                        MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_REC_1D.SetTitle(MC_REC_1D_Title_New)
                except:
                    print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_REC_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                # print("\nMC_REC_1D already is a 1D Histogram...")
                MC_REC_1D = MC_REC_1D_initial


            if(MC_BGS_1D_initial != "None"):
                if("2D" in str(type(MC_BGS_1D_initial))):
                    try:
                        bin_MC_BGS_1D_0, bin_MC_BGS_1D_1 = MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_BGS_1D_initial.GetNbinsY())
                        MC_BGS_1D                        = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_BGS_1D_0, bin_MC_BGS_1D_1, "e")
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                        else:
                            MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                        MC_BGS_1D.SetTitle(MC_BGS_1D_Title_New)
                    except:
                        print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_BGS_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                else:
                    # print("\nMC_BGS_1D already is a 1D Histogram...")
                    MC_BGS_1D = MC_BGS_1D_initial
            else:
                MC_BGS_1D = MC_BGS_1D_initial
                
                
            if("2D" in str(type(MC_GEN_1D_initial))):
                try:
                    bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                    MC_GEN_1D                        = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_GEN_1D_0, bin_MC_GEN_1D_1, "e")
                    if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                        MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_GEN_1D.SetTitle(MC_GEN_1D_Title_New)
                except:
                    print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (MC_GEN_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                # print("\nMC_GEN_1D already is a 1D Histogram...")
                MC_GEN_1D = MC_GEN_1D_initial
                
            if(tdf not in ["N/A"]):
                if("2D" in str(type(ExTRUE_1D_initial))):
                    try:
                        bin_ExTRUE_1D_0, bin_ExTRUE_1D_1 = ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExTRUE_1D_initial.GetNbinsY())
                        ExTRUE_1D                        = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExTRUE_1D_0, bin_ExTRUE_1D_1, "e")
                        if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                            ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        else:
                            ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                        ExTRUE_1D_Title_New        = str(str(ExTRUE_1D_Title_New.replace("Generated",                  "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                        ExTRUE_1D_Title_X_Axis_New = str(str(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Generated", "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                        ExTRUE_1D.SetTitle(ExTRUE_1D_Title_New)
                        ExTRUE_1D.GetXaxis().SetTitle(ExTRUE_1D_Title_X_Axis_New)
                    except:
                        print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (ExTRUE_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                else:
                    # print("\nExTRUE_1D already is a 1D Histogram...")
                    ExTRUE_1D = ExTRUE_1D_initial
                    ExTRUE_1D_Title_New            = str(str(str(ExTRUE_1D.GetTitle()).replace("Generated",            "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
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


            if((z_pT_Bin_Unfold   != 0)                            and (("Combined_"         in out_print_main) or ("Multi_Dim_Q2"       in out_print_main))):
                continue
            if(((Q2_xB_Bin_Unfold == 0) or (z_pT_Bin_Unfold != 0)) and ("Multi_Dim_z_pT_Bin" in out_print_main)):
                continue
            if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("Combined_"         in out_print_main) or ("Multi_Dim_Q2_phi_t" in out_print_main))):
                continue
            # if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'Multi_Dim" not in out_print_main)):
            # if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'MM" not in out_print_main) and ("'W" not in out_print_main)):
            if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'W" not in out_print_main) and ("'Multi_Dim" not in out_print_main)):
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

                

            ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            if(tdf not in ["N/A"]):
                ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            if(MC_BGS_1D != "None"):
                MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))
                
                
            # continue
            List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold, MC_BGS_1D=MC_BGS_1D)
            continue
                



##===============##     Unfolding Histogram Procedure     ##===============##
#############################################################################




print("".join(["Total: ",      str(count)]))
# print("".join(["Num Failed: ", str(count_failed)]))










def skip_condition_y_bins(Q2_Y_BIN, Z_PT_BIN, BINNING_METHOD="_y_bin"):
    if("Y_bin" not in BINNING_METHOD):
        skip_condition_y_bins_return = (Q2_Y_BIN in [1]) and (Z_PT_BIN in [28, 34, 35])
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [2])          and (Z_PT_BIN in [28, 35, 41, 42])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [3])          and (Z_PT_BIN in [28, 35])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [4])          and (Z_PT_BIN in [6,  36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [5])          and (Z_PT_BIN in [30, 36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [6])          and (Z_PT_BIN in [30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [7])          and (Z_PT_BIN in [24, 30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [9])          and (Z_PT_BIN in [36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [10])         and (Z_PT_BIN in [30, 36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [11])         and (Z_PT_BIN in [24, 30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [13, 14])     and (Z_PT_BIN in [25])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [15, 16, 17]) and (Z_PT_BIN in [20])))
        return skip_condition_y_bins_return
    else:
        return False






BIN_SEARCH = []
for BIN in Q2_xB_Bin_List:
    BIN_SEARCH.append("".join(["Q2_y_Bin_", str(BIN) if(str(BIN) not in ['0', 0]) else "All", ")"]))
    
# Draw_2D_Histograms_Simple
for ii in rdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        # print("out_print_main =", out_print_main)
        # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
        out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
        out_print_str     = out_print_str.replace("_smeared",              "")
        out_print_str     = out_print_str.replace("'smear'",               "Smear")
        SEARCH = []
        for BIN in BIN_SEARCH:
            SEARCH.append(str(BIN) in str(out_print_str))
            if(str(BIN) in str(out_print_str)):
                break
        if(True in SEARCH):
            List_of_All_Histos_For_Unfolding[out_print_str.replace("mdf", "rdf")] = rdf.Get(out_print_main)
            # List_of_All_Histos_For_Unfolding[str(out_print_str)] = rdf.Get(str(out_print_main))

            
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        # print("out_print_main =", out_print_main)
        # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
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
            
            
for ii in gdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        # print("out_print_main =", out_print_main)
        # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
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
            
            
            
if(tdf not in ["N/A"]):
    for ii in tdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            # out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
            out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
            out_print_str = out_print_str.replace("_(cut_Complete_SIDIS)", "")
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
            


# Bin-by-Bin Acceptance Corrections for 2D Histograms
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        mdf_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        mdf_print_str     = mdf_print_str.replace("_(cut_Complete_SIDIS)", "")
        mdf_print_str     = mdf_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
        mdf_print_str     = mdf_print_str.replace("_smeared",              "")
        mdf_print_str     = mdf_print_str.replace("'smear'",               "Smear")
        rdf_print_str     = str(mdf_print_str.replace("mdf", "rdf")).replace("Smear", "''")
        gdf_print_str     = str(mdf_print_str.replace("mdf", "gdf")).replace("Smear", "''")
        gdf_print_str     = gdf_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
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

final_count = 0
print("\n\nCounting Total Number of collected histograms...")
for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
    final_count += 1
#     print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Chi_Squared" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Normal_2D" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Multi_Dim" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("_(rdf)_(SMEAR=" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if("Acceptance" in str(List_of_All_Histos_For_Unfolding_ii)):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
#     if(("tdf" not in str(List_of_All_Histos_For_Unfolding_ii)) and ("Fit" not in str(List_of_All_Histos_For_Unfolding_ii))):
#         print("\n", str(List_of_All_Histos_For_Unfolding_ii))
# print("\n\n\nList_of_All_Histos_For_Unfolding =\n", List_of_All_Histos_For_Unfolding)
print("\nFinal Count =", final_count)






Smearing_final_list = ["''", "Smear"]
if(Smearing_Options not in ["no_smear", "both"]):
    Smearing_final_list = ["Smear"]
elif(Smearing_Options in ["no_smear"]):
    Smearing_final_list = ["''"]
elif(Smearing_Options in ["both"]):
    Smearing_final_list = ["''", "Smear"]
    
    
# Method_Type_List = ["Data", "Response", "Bin", "RooUnfold_bayes", "RooUnfold_svd", "rdf", "mdf", "gdf"]
Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD", "Unfold", "rdf", "mdf", "gdf", "Acceptance"]
if(tdf not in ["N/A"]):
    Method_Type_List.append("tdf")
    
    
# Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD", "Unfold"]
# Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD"]
# Method_Type_List = ["Unfold"]
# Method_Type_List = ["Data", "Unfold"]
# Method_Type_List = ["Data"]
# Method_Type_List = ["Bin"]
# Method_Type_List = ["Data", "Bayesian", "Bin", "Acceptance"]
# Method_Type_List = ["Bayesian", "Bin", "Acceptance"]

# Method_Type_List = ["Data", "Bin", "rdf", "mdf", "gdf", "Acceptance"]

# All phi_t related plots (including multidimensional plots) are controlled by variable = 'phi_t'
# Variable_List = ["phi_t", "MM"]
# Variable_List = ["MM"]
Variable_List = ["phi_t"]


# Cut_Options_List = ["Cut", "UnCut"]
Cut_Options_List = ["Cut"]


Orientation_Option_List = ["pT_z", "z_pT"]
Orientation_Option_List = ["pT_z"] # Flipped
Orientation_Option_List = ["z_pT"]


Variable_List_Final = ["phi_t", "Multi_Dim_z_pT_Bin_y_bin_phi_t" if("y" in Binning_Method) else "Multi_Dim_z_pT_Bin_Y_bin_phi_t"]
# Variable_List_Final = ["phi_t"]

Run_Individual_Bin_Images_Option = True
Print_Run_Individual_Bin_Option  = True

to_be_saved_count = 0
Pars_Canvas, Histo_Pars_VS_Z, Histo_Pars_VS_PT, Pars_Legends = {}, {}, {}, {}
for variable in Variable_List:
    for BIN in Q2_xB_Bin_List:
        BIN_NUM        = int(BIN) if(str(BIN) not in ["0"]) else "All"
        z_pT_Bin_Range = 42       if(str(BIN_NUM) in ["2"]) else  36 if(str(BIN_NUM) in ["4", "5", "9", "10"]) else 35 if(str(BIN_NUM) in ["1", "3"]) else 30 if(str(BIN_NUM) in ["6", "7", "8", "11"]) else 25 if(str(BIN_NUM) in ["13", "14"]) else 20 if(str(BIN_NUM) in ["12", "15", "16", "17"]) else 0
        if("Y_bin" in Binning_Method):
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=BIN_NUM)[1] - 1
        for smear in Smearing_final_list:
            HISTO_NAME = "".join(["(1D)_(Data_Type)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_All)_(", str(variable), ")"])

            # for Multi_Dim in ["Off", "Only", "Q2_y", "z_pT"]:
            for Multi_Dim in ["Off", "Only"]:
#             for Multi_Dim in ["Off"]:
                if((BIN_NUM not in ["All"]) and (Multi_Dim in ["Off", "Only"]) and (str(variable) in ["phi_t"])):
                    for method in Method_Type_List:
                        if((method in ["RooUnfold_svd", "SVD", "Response"]) and (Multi_Dim not in ["Off"])):
                            continue
                        # if((method in ["rdf"]) and Sim_Test):
                        #     continue
                        if((method in ["gdf", "tdf"]) and ("Smear" in str(smear))):
                            continue
                        for Cut in Cut_Options_List:
                            if((Cut in ["UnCut"]) and (method not in ["rdf", "mdf", "Data"])):
                                # There is (currently) no point in running any other method with both the cut and uncut versions of this plot (this option only affects the 2D histograms and not the unfolded histograms - gdf and tdf are also already uncut by default)
                                continue
                            for Orientation in Orientation_Option_List:
                                try:
                                    z_pT_Images_Together(Histogram_List_All=List_of_All_Histos_For_Unfolding,     Default_Histo_Name=HISTO_NAME, Method=method,    Q2_Y_Bin=BIN_NUM,                                     Multi_Dim_Option=Multi_Dim, Plot_Orientation=Orientation, Cut_Option=Cut)
                                    to_be_saved_count += 1
                                except Exception as e:
                                    print("".join([color.BOLD, color.RED, "ERROR IN z_pT_Images_Together():\n",   color.END, color.RED, str(traceback.format_exc()), color.END]))
                                
                # continue # This is to skip everything that isn't the z_pT_Images_Together() images
                for z_pT_Bin in range(0, z_pT_Bin_Range + 1, 1):
                    if("Y_bin" not in Binning_Method):
                        if(((BIN_NUM in [1]) and (z_pT_Bin in [28, 34, 35])) or ((BIN_NUM in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or ((BIN_NUM in [3]) and (z_pT_Bin in [28, 35])) or ((BIN_NUM in [4]) and (z_pT_Bin in [6, 36])) or ((BIN_NUM in [5]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [6]) and (z_pT_Bin in [30])) or ((BIN_NUM in [7]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [9]) and (z_pT_Bin in [36])) or ((BIN_NUM in [10]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [11]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [13, 14]) and (z_pT_Bin in [25])) or ((BIN_NUM in [15, 16, 17]) and (z_pT_Bin in [20]))):
                            continue
                    # if((Multi_Dim not in ["Off"])  and ((BIN_NUM in ["All"]) or (z_pT_Bin in [0]))):
                    #     continue
                    # if((Multi_Dim in ["Only"]) and ((BIN_NUM     in ["All"]) or (z_pT_Bin in [0]))):
                    #     continue
                    if((Multi_Dim in ["Only", "z_pT"]) and (BIN_NUM  in ["All"])):
                        continue
                    if((Multi_Dim in ["Q2_y"])         and ((BIN_NUM in ["All"]) or (z_pT_Bin not in [0]))):
                        continue
                        

                    # print("")
                    # print("BIN_NUM    =", BIN_NUM)
                    # print("HISTO_NAME =", HISTO_NAME)
                    # print("Multi_Dim  =", Multi_Dim)
                    # print("z_pT_Bin   =", z_pT_Bin)

                    if(Run_Individual_Bin_Images_Option):
                        try:
                            String_For_Output_txt  = Large_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding,      Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [0]) else "All", Multi_Dim_Option=Multi_Dim, String_Input=String_For_Output_txt)
                            if(str(Multi_Dim) in ["Off"]):
                                to_be_saved_count += 2
                            else:
                                to_be_saved_count += 1
                        except Exception as e:
                            print("".join([color.BOLD, color.RED, "ERROR IN Large_Individual_Bin_Images():\n",    color.END, color.RED, str(traceback.format_exc()), color.END]))
                        if(str(variable) in ["phi_t"]):
                            try:
                                Unfolded_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding,   Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [0]) else "All", Multi_Dim_Option=Multi_Dim)
                                to_be_saved_count += 1
                            except Exception as e:
                                print("".join([color.BOLD, color.RED, "ERROR IN Unfolded_Individual_Bin_Images():\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                        else:
                            continue
                    elif(Print_Run_Individual_Bin_Option):
                        print(color.BOLD, "\n\n\n\nNOT MAKEING INDIVIDUAL BIN IMAGES AT THIS TIME", color.END, "\n\tMust set Run_Individual_Bin_Images_Option = True\n\n\n\n")
                        Print_Run_Individual_Bin_Option = False


            if((str(BIN_NUM) not in ["All", "0"]) and (Fit_Test)):
                # for Variable       in ["phi_t",     "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_y_bin_phi_t"]:
                for Variable       in Variable_List_Final:
                    # for Parameter  in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
                    for Parameter  in ["Fit_Par_B", "Fit_Par_C"]:
                        for Method in Method_Type_List:
                            if(str(Method) in ["rdf", "mdf", "Response", "Data", "Unfold", "Acceptance"]):
                                continue
                            if((("Multi_Dim" in str(Variable)) and (str(Method) in ["SVD"])) or (("Smear" in str(smear)) and ("gdf" in str(Method)))):
                                continue
                            LAST_Z_BIN,  LAST_PT_BIN  = "NA", "NA"
                            Z_BIN_COLOR, PT_BIN_COLOR = 1, 1
                            PAR_HISTO_MASTER_NAME_VS_Z   = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_Z"])
                            PAR_HISTO_MASTER_NAME_VS_PT  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(", str(Variable), ")_VS_PT"])

                            MASTER_TITLE = "".join(["#splitline{#scale[1.15]{", "Multidimensional " if("Multi_Dim" in str(Variable)) else "", "Plot of Parameter ", str(Parameter).replace("Fit_Par_", ""), "}}{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(BIN_NUM), "} ", root_color.Bold, "{#topbar #color[", str(root_color.Blue), "]{Method: ", "Bin-by-Bin" if(Method in ["Bin"]) else "MC Generated" if(Method in ["gdf"]) else "".join([str(Method), " Unfolding"]), "}}}"])

                            if(str(PAR_HISTO_MASTER_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z]   = ROOT.TMultiGraph(PAR_HISTO_MASTER_NAME_VS_Z,  "".join(["#splitline{", str(MASTER_TITLE), "}{#scale[1.05]{Showing all P_{T} bins vs z}};", "(Smeared) " if(str(smear) in ["Smear"]) else "", "z; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                            if(str(PAR_HISTO_MASTER_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT] = ROOT.TMultiGraph(PAR_HISTO_MASTER_NAME_VS_PT, "".join(["#splitline{", str(MASTER_TITLE), "}{#scale[1.05]{Showing all z bins vs P_{T}}};", "(Smeared) " if(str(smear) in ["Smear"]) else "", "P_{T} [GeV]; Parameter ", str(Parameter).replace("Fit_Par_", "")]))

                            if(str(PAR_HISTO_MASTER_NAME_VS_Z)  not in Pars_Legends):
                                Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z]      = ROOT.TLegend(0.55, 0.1, 0.9, 0.425)
                            if(str(PAR_HISTO_MASTER_NAME_VS_PT) not in Pars_Legends):
                                Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT]     = ROOT.TLegend(0.55, 0.1, 0.9, 0.425)

                            for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
                                if(skip_condition_y_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method)):
                                    continue
                                PAR_FIND_NAME = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])

                                
                                Z_BIN_VALUE   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][0][1], 3)
                                PT_BIN_VALUE  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][1][1], 3)
                                # Z_BIN_VALUE   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][1], 3)
                                # PT_BIN_VALUE  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][1], 3)
                                Z_BIN         = str(Z_BIN_VALUE)
                                PT_BIN        = str(PT_BIN_VALUE)
                                
                                Z_BIN_VALUE_Title   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][1], 3)
                                PT_BIN_VALUE_Title  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][1], 3)
                                Z_BIN         = str(Z_BIN_VALUE_Title)
                                PT_BIN        = str(PT_BIN_VALUE_Title)

                                Z_BIN_WIDTH   = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][0][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][0][0])/2, 3)
                                PT_BIN_WIDTH  = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][1][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin_Find=z_pT_Bin, List_Of_Histos_For_Stats_Search=List_of_All_Histos_For_Unfolding, Smearing_Q=smear, DataType="bbb")[1][1][0])/2, 3)
                                # Z_BIN_WIDTH   = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][0])/2, 3)
                                # PT_BIN_WIDTH  = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][0])/2, 3)

                                # PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                                # PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                                # PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method) if((not Sim_Test) or (str(Method) not in ["rdf"])) else "mdf", ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])
                                
                                PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                                PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                                PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])
                                
                                
                                if(("0.27" in str(PT_BIN)) and (("Bay" in str(Method)) or ("Bin" in str(Method)))):
                                    # print("\nSKIPPING PT_BIN = 0.27\n")
                                    continue

                                if(Fit_Test):
                                    try:
                                        PARAMETER_TO_ADD, PAR_ERROR_TO_ADD = List_of_All_Histos_For_Unfolding[str(PAR_FIND_NAME)]
                                    except:
                                        print("".join([color.BOLD, color.RED, "ERROR IN GETTING THE FIT PARAMETERS FOR: ", color.END, str(PAR_FIND_NAME), "\n", color.RED, str(traceback.format_exc()), color.END]))
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
                                    
                                    
                                Borders_z_pT   = z_pT_Border_Lines(BIN_NUM)
                                z_length       = Borders_z_pT[0][1] - 1
                                pT_length      = Borders_z_pT[1][1] - 1
                                if(str(z_pT_Bin) not in ["All", "0"]):
                                    # This finds the dimensions of a particular z-pT bin for a given Q2-y bin
                                    z_bin      = ((z_pT_Bin - 1) // pT_length) + 1
                                    z_bin      = (z_length + 1) - z_bin
                                    pT_bin     = ((z_pT_Bin - 1) %  pT_length) + 1
                                    z_bin_max  = Borders_z_pT[0][2][z_bin]
                                    z_bin_min  = Borders_z_pT[0][2][z_bin  - 1]
                                    pT_bin_max = Borders_z_pT[1][2][pT_bin]
                                    pT_bin_min = Borders_z_pT[1][2][pT_bin - 1]
                                    if(str(PAR_HISTO_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z]   = ROOT.TGraphErrors()
                                        # Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z with #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}}}; z; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z for #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin with ", str(round(pT_bin_min, 3)), " < P_{T} < ", str(round(pT_bin_max, 3)), "}}}; #scale[1.25]{z}; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineColor(PT_BIN_COLOR)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerColor(PT_BIN_COLOR)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerStyle(33)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(3)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineWidth(2)
                                        
                                        Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z].Add(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z])
                                        # Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}"]), "lep")
                                        Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin: ", str(round(pT_bin_min, 3)), " < P_{T} < ", str(round(pT_bin_max, 3)), "}"]), "lep")
                                        
                                    if(str(PAR_HISTO_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT] = ROOT.TGraphErrors()
                                        # Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} with #color[", str(Z_BIN_COLOR), "]{z Bin Centered at ",     str(Z_BIN),   "}}}; P_{T} [GeV]; Parameter ", str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} for #color[", str(Z_BIN_COLOR),  "]{z Bin with ",     str(round(z_bin_min, 3)),  " < z < ",     str(round(z_bin_max, 3)),  "}}}; #scale[1.25]{P_{T} [GeV]}; Parameter ", str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineColor(Z_BIN_COLOR)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerColor(Z_BIN_COLOR)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerStyle(33)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(3)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineWidth(2)

                                        Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT].Add(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT])
                                        # Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin Centered at ",     str(Z_BIN),  "}"]), "lep")
                                        Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin: ",     str(round(z_bin_min, 3)),  " < z < ",     str(round(z_bin_max, 3)),  "}"]), "lep")
                                    
                                else:
                                    print(color.Error, "\n\nERROR: Using center of bin in title/legends...\n\n", color.END)
                                    if(str(PAR_HISTO_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z]   = ROOT.TGraphErrors()
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z with #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}}}; z; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineColor(PT_BIN_COLOR)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerColor(PT_BIN_COLOR)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerStyle(33)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(3)
                                        Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineWidth(2)
                                        
                                        Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z].Add(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z])
                                        Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}"]), "lep")
                                    if(str(PAR_HISTO_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT] = ROOT.TGraphErrors()
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} with #color[", str(Z_BIN_COLOR), "]{z Bin Centered at ",     str(Z_BIN),   "}}}; P_{T} [GeV]; Parameter ", str(Parameter).replace("Fit_Par_", "")]))
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineColor(Z_BIN_COLOR)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerColor(Z_BIN_COLOR)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerStyle(33)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(3)
                                        Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineWidth(2)

                                        Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT].Add(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT])
                                        Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin Centered at ",     str(Z_BIN),  "}"]), "lep")

                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPoint(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN(),              Z_BIN_VALUE,  PARAMETER_TO_ADD)
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPointError(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN()     - 1, Z_BIN_WIDTH,  PAR_ERROR_TO_ADD)
                                
                                # if(("0.135" in str(PT_BIN)) or ("0.27" in str(PT_BIN)) or ("0.365" in str(PT_BIN))):
                                #     print("".join([color.BOLD, color_bg.YELLOW, "\n\n\nFor z_pT_Bin = ", str(z_pT_Bin), ":\t\n\tZ_BIN        = ", str(Z_BIN), "\t\n\tZ_BIN_VALUE  = ", str(Z_BIN_VALUE), "\t\nand\t\t\n\tPT_BIN       = ", str(PT_BIN), "\t\n\tPT_BIN_VALUE = ", str(PT_BIN_VALUE), "\n\n", color.END, "\n\n"]))
                                
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPoint(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN(),          PT_BIN_VALUE, PARAMETER_TO_ADD)
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPointError(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN() - 1, PT_BIN_WIDTH, PAR_ERROR_TO_ADD)


for ii in Histo_Pars_VS_Z:
    if(type(Histo_Pars_VS_Z[ii]) is type(ROOT.TMultiGraph())):
        Pars_Canvas[ii] = ROOT.TCanvas(str(ii), str(ii), 1200, 1100)
        # Pars_Canvas[ii].Draw()
        Histo_Pars_VS_Z[ii].SetTitle(str(Histo_Pars_VS_Z[ii].GetTitle()).replace("Showing all P_{T} bins vs z", ""))
        Histo_Pars_VS_Z[ii].Draw("APL same")
        ROOT.gPad.Modified()
        if((("Bayesian" in str(ii)) or ("(Bin)" in str(ii))) and ("Multi_Dim" in str(ii))):
            if("Par_B" in str(ii)):
                # Histo_Pars_VS_Z[ii].SetMinimum(-0.65 if("Q2_y_Bin_17" not in str(ii)) else -0.4 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMinimum()) if(Histo_Pars_VS_Z[ii].GetMinimum() < 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMinimum()))
                # Histo_Pars_VS_Z[ii].SetMaximum( 0.1  if("Q2_y_Bin_17" not in str(ii)) else  0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMaximum()) if(Histo_Pars_VS_Z[ii].GetMaximum() > 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMaximum()))
                Histo_Pars_VS_Z[ii].SetMinimum(-0.85)
                Histo_Pars_VS_Z[ii].SetMaximum( 0.15)
                # print(color.GREEN, "\nAdjusting (B):\n", str(ii), "\n", color.END)
            elif("Par_C" in str(ii)):
                # Histo_Pars_VS_Z[ii].SetMinimum(-0.16 if("Q2_y_Bin_17" not in str(ii)) else -0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMinimum()) if(Histo_Pars_VS_Z[ii].GetMinimum() < 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMinimum()))
                # Histo_Pars_VS_Z[ii].SetMaximum( 0.16 if("Q2_y_Bin_17" not in str(ii)) else  0.1 if("Q2_y_Bin_5" not in str(ii)) else 1.8*(Histo_Pars_VS_Z[ii].GetMaximum()) if(Histo_Pars_VS_Z[ii].GetMaximum() > 0) else 0.2*(Histo_Pars_VS_Z[ii].GetMaximum()))
                Histo_Pars_VS_Z[ii].SetMinimum(-0.2)
                Histo_Pars_VS_Z[ii].SetMaximum( 0.2)
                # print(color.GREEN, "\nAdjusting (C):\n", str(ii), "\n", color.END)
            # else:
            #     print(color.RED, "NOT adjusting:\n", str(ii), color.END)
        Pars_Legends[ii].Draw()
        Pars_Canvas[ii].Update()


if(not True):
    for jj in Histo_Pars_VS_PT:
        if(type(Histo_Pars_VS_PT[jj]) is type(ROOT.TMultiGraph())):
            Pars_Canvas[jj] = ROOT.TCanvas(str(jj), str(jj), 1200, 1100)
            # Pars_Canvas[jj].Draw()
            Histo_Pars_VS_PT[jj].Draw("APL same")
            Pars_Legends[jj].Draw()

for CanvasPar_Name in Pars_Canvas:
    if("Par_A" not in str(CanvasPar_Name)):
        Save_Name_Pars = str(CanvasPar_Name).replace(".", "_")
        Save_Name_Pars = str(Save_Name_Pars).replace("(", "")
        Save_Name_Pars = str(Save_Name_Pars).replace(")", "")
        Save_Name_Pars = str(Save_Name_Pars).replace("SMEAR=", "")
        Save_Name_Pars = str(Save_Name_Pars).replace("''", "")
        Save_Name_Pars = str(Save_Name_Pars).replace("__", "_")

        Save_Name_Pars = "".join([str(Save_Name_Pars), File_Save_Format])
        if(Saving_Q):
            if("root" in str(File_Save_Format)):
                Pars_Canvas[CanvasPar_Name].SetName(Save_Name_Pars.replace(".root", ""))
            Pars_Canvas[CanvasPar_Name].SaveAs(Save_Name_Pars)
        print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name_Pars), color.END]))
        to_be_saved_count += 1


    
print(color.BOLD, color.GREEN, "\nImages to be saved =", to_be_saved_count, "\n", color.END)

# print("\n\nString_For_Output_txt =", str(String_For_Output_txt), "\n")
Q2_y_Select_bin = str(str(str(Q2_xB_Bin_List).replace("[",  "")).replace("]", "")).replace("'0'", "'All'")
Q2_y_Select_bin = str(Q2_y_Select_bin.replace("'", "")).replace(",", "_")
Q2_y_Select_bin = str(Q2_y_Select_bin.replace(" ", "_")).replace("__", "_")
# File_Time = str(str(Date_Time).replace("Started running on ", "")).replace("\n", "")
File_Time = str(str(Date_Day.replace(" at ", "")).replace("Started running on ", "")).replace("\n", "")
File_Time = str(File_Time.replace(color.BOLD, "")).replace(color.END, "")
File_Time = str((str((File_Time.replace(" ", "_")).replace("-", "_")).replace(":", "_")).replace(".", "")).replace("__", "_")
# Output_txt_Name = "".join([str(Common_Name).replace("_All", ""), "_Q2_y_Bins_", str(Q2_y_Select_bin), "_from_", str(File_Time), ".txt"])
Output_txt_Name     = "".join([str(Common_Name).replace("_All", ""), "_", str(File_Time), "_Q2_y_Bins_", str(Q2_y_Select_bin), ".txt"])
if(Closure_Test):
    Output_txt_Name     = "".join(["Closure_",  str(Output_txt_Name)])
else:
    if(Sim_Test):
        Output_txt_Name = "".join(["Sim_Test_", str(Output_txt_Name)])
    if(Mod_Test):
        Output_txt_Name = "".join(["Mod_Test_", str(Output_txt_Name)])
        
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
#     print("".join(["\n", "Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Output_txt_Name), color.END, "\n"]))
# else:
#     print(color.Error, "Still failed to get a new name for the .txt file...", color.END)

if(Fit_Test):
    Output_txt_Par_Name = f"Parameters_{Output_txt_Name}"
    Text_Par_Outputs    = "Note to Reader: Print the text in this file as a string in Python for the best formatting..."
    for BIN in Q2_xB_Bin_List:
        BIN_NUM        = int(BIN) if(str(BIN) not in ["0"]) else "All"
        z_pT_Bin_Range = 42       if(str(BIN_NUM) in ["2"]) else  36 if(str(BIN_NUM) in ["4", "5", "9", "10"]) else 35 if(str(BIN_NUM) in ["1", "3"]) else 30 if(str(BIN_NUM) in ["6", "7", "8", "11"]) else 25 if(str(BIN_NUM) in ["13", "14"]) else 20 if(str(BIN_NUM) in ["12", "15", "16", "17"]) else 0
        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_y_bins(Q2_Y_BIN=BIN_NUM, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method)):
                continue
            for smear in Smearing_final_list:
                if(smear not in ["''"]):
                    Text_Par_Outputs = f"{Text_Par_Outputs}\n======================================================================\nFor {color.UNDERLINE}{color.BOLD}SMEARED Q2-y Bin {BIN_NUM} - z-PT Bin {z_pT_Bin}{color.END}: "
                else:
                    Text_Par_Outputs = f"{Text_Par_Outputs}\n======================================================================\nFor {color.UNDERLINE}{color.BOLD}Q2-y Bin {BIN_NUM} - z-PT Bin {z_pT_Bin}{color.END}: "
                for Variable   in Variable_List_Final:
                    if(any("Multi_Dim" in ii for ii in Variable_List_Final)):
                        Text_Par_Outputs = "".join([str(Text_Par_Outputs), color.BOLD, "\n\t (*) ", "3D" if("Multi_Dim" in Variable) else "1D", " Histograms:", color.END])
                    for Method in Method_Type_List:
                        if(str(Method)   in ["rdf", "mdf", "Response", "Data", "Unfold", "Acceptance"]):
                            continue
                        if((("Multi_Dim" in str(Variable)) and (str(Method) in ["SVD"])) or (("Smear" in str(smear)) and ("gdf" in str(Method)))):
                            continue
                        Text_Par_Outputs = "".join([str(Text_Par_Outputs), color.BOLD, "\n\t - ", f"{Method} Unfolding" if(Method not in ["gdf", "bbb", "Bin", "bay"]) else "Bayesian Unfolding" if(Method not in ["gdf", "bbb", "Bin"]) else "Bin-by-Bin Correction" if(Method not in ["gdf"]) else "Generated Plot", " Fits:", color.END])
                        PAR_A_NAME = "".join(["(Fit_Par_A)_(",   str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                        PAR_B_NAME = "".join(["(Fit_Par_B)_(",   str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                        PAR_C_NAME = "".join(["(Fit_Par_C)_(",   str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
                        CHI_2_NAME = "".join(["(Chi_Squared)_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])
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
                        if(str not in [type(Chi_2_Value), type(NDF_Value)]):
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
        print("".join(["\n", "Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Output_txt_Par_Name), color.END, "\n"]))
    else:
        print(color.Error, "Still failed to get a new name for the .txt file...", color.END)
    

    
    


# Getting Current Date
datetime_object_end = datetime.now()
endMin_full, endHr_full, endDay_full = datetime_object_end.minute, datetime_object_end.hour, datetime_object_end.day
if(datetime_object_end.minute < 10):
    timeMin_end = ''.join(['0', str(datetime_object_end.minute)])
else:
    timeMin_end = str(datetime_object_end.minute)
# Printing Current Time
if(datetime_object_end.hour > 12 and datetime_object_end.hour < 24):
    print("".join(["The time that this code finished is ", str((datetime_object_end.hour) - 12), ":", str(timeMin_end), " p.m."]))
if(datetime_object_end.hour < 12 and datetime_object_end.hour > 0):
    print("".join(["The time that this code finished is ", str(datetime_object_end.hour),        ":", str(timeMin_end), " a.m."]))
if(datetime_object_end.hour == 12):
    print("".join(["The time that this code finished is ", str(datetime_object_end.hour),        ":", str(timeMin_end), " p.m."]))
if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
    print("".join(["The time that this code finished is 12:", str(timeMin_end), " a.m."]))

    

print("".join(["Saved ", str(to_be_saved_count), " Images..."]))

Num_of_Days, Num_of_Hrs, Num_of_Mins = 0, 0, 0

if(startDay_full > endDay_full):
    Num_of_Days  = endDay_full + (30 - startDay_full)
else:
    Num_of_Days  = endDay_full - startDay_full
if(startHr_full  > endHr_full):
    Num_of_Hrs   = endHr_full  + (24 - startHr_full)
else:
    Num_of_Hrs   = endHr_full  - startHr_full
if(startMin_full > endMin_full):
    Num_of_Mins  = endMin_full + (60 - startMin_full)
else:
    Num_of_Mins  = endMin_full - startMin_full
if(Num_of_Hrs > 0  and startMin_full >= endMin_full):
    Num_of_Hrs  += -1
if(Num_of_Days > 0 and startHr_full  >= endHr_full):
    Num_of_Days += -1


print("\nThe total time the code took to run the given files is:")
print("".join([str(Num_of_Days), " Day(s), ", str(Num_of_Hrs), " Hour(s), and ", str(Num_of_Mins), " Minute(s)."]))


if((((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins) != 0):
    rate_of_histos = to_be_saved_count/(((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins)
    print("".join(["Rate of Histos/Minute = ", str(rate_of_histos), " Histos/Min"]))


print("\n")
    

print("".join([color.BOLD, color.GREEN, color_bg.YELLOW, """
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
""", color.END]))



# # Update Notes:
# As of 3-9-2023 (Running with 'Common_Name = "Multi_Dimension_Unfold_V3_All"')
#     1) Running with the Q2-xB bin 0 cut for multidimensional unfolding
#     2) Running Parameter plots again
#     3) Added these notes