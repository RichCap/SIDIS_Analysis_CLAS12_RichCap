#!/usr/bin/env python

import sys

       
Saving_Q = True
Sim_Test = False
Smearing_Options = "both"
if(len(sys.argv) > 1):
    arg_option_1 = str(sys.argv[1])
    if(arg_option_1 in ["test", "Test", "time", "Time"]):
        print("\nNOT SAVING\n")
        Saving_Q = False
    else:
        print("".join(["\nOption Selected: ", str(arg_option_1), " (Still Saving...)" if("no_save" not in str(arg_option_1)) else " (NOT SAVING)"]))
        Saving_Q = True if("no_save" not in str(arg_option_1)) else False
        Sim_Test = True if("sim" in str(arg_option_1) or "simulation" in str(arg_option_1)) else False
        arg_option_1     = arg_option_1.replace("_simulation", "")
        arg_option_1     = arg_option_1.replace("_sim", "")
        arg_option_1     = arg_option_1.replace("simulation", "")
        arg_option_1     = arg_option_1.replace("sim", "")
        Smearing_Options = str((arg_option_1).replace("_no_save", "")).replace("no_save", "") if(str(arg_option_1) not in ["save", ""]) else "both"
        if(Smearing_Options == ""):
            Smearing_Options = "both"
else:
    Saving_Q = True
    
if(Sim_Test):
    print("\033[94m\nRunning Simulated Test\n\033[0m")
    print("Smearing_Options =", Smearing_Options)
#     print("\033[1m\033[91m\nWARNING: Sim_Test is not set up to run yet...\n\033[0m")



File_Save_Format = ".png"
# File_Save_Format = ".root"
# File_Save_Format = ".pdf"



Binning_Method = "_2"
Binning_Method = "_y_bin"

Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
if("y_bin" in Binning_Method):
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

from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT
import math

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



class color:
    CYAN      = '\033[96m'
    PURPLE    = '\033[95m'
    BLUE      = '\033[94m'
    YELLOW    = '\033[93m'
    GREEN     = '\033[92m'
    RED       = '\033[91m'
    DARKCYAN  = '\033[36m'
    BOLD      = '\033[1m'
    LIGHT     = '\033[2m'
    ITALIC    = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK     = '\033[5m'
    DELTA     = '\u0394' # symbol
    END       = '\033[0m'
    
    
class color_bg:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'
    END     = '\033[0m'
    
    
class root_color:
    # Colors
    White   = 0
    Black   = 1
    Red     = 2
    Green   = 3
    Blue    = 4
    Yellow  = 5
    Pink    = 6
    Cyan    = 7
    DGreen  = 8 # Dark Green
    Purple  = 9
    DGrey   = 13
    Grey    = 15
    LGrey   = 17
    Brown   = 28
    Gold    = 41
    Rust    = 46
    
    # Fonts
    Bold    = '#font[22]'
    Italic  = '#font[12]'
    
    # Symbols
    Delta   = '#Delta'
    Phi     = '#phi'
    π       = '#pi'
    Degrees = '#circ'
    
    Line    = '#splitline'

    

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
if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
    print("".join([Date_Day, color.BOLD, str((datetime_object_full.hour)-12), ":", timeMin_full, " p.m.", color.END]))
if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
    print("".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " a.m.", color.END]))
if(datetime_object_full.hour == 12):
    print("".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " p.m.", color.END]))
if(datetime_object_full.hour == 0 or  datetime_object_full.hour == 24):
    print("".join([Date_Day, color.BOLD, "12:", str(timeMin_full), " a.m.", color.END]))
print("")




try:
    import RooUnfold
    # print("".join([color.GREEN, color.BOLD, "Perfect Success", color.END]))
except ImportError:
    print("".join([color.RED, color.BOLD, "ERROR: \n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n"]))
    # print("Somehow the python module was not found, let's try loading the library by hand...")
    # try:
    #     ROOT.gSystem.Load("libRooUnfold.so")
    #     print("".join([color.GREEN, "Success", color.END]))
    # except:
    #     print("".join([color.RED, color.BOLD, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    
# for ii in sys.modules:
#     if(str(ii) in ["ROOT", "RooUnfold"]):
#         # print(ii)
#         print(sys.modules[ii])
        
        
        
print("\n\n")









#################################################################################################################################################################
##==========##==========##     Kinematic Binning Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
#################################################################################################################################################################
def Q2_xB_Border_Lines(Q2_xB_Bin_Select):
    # Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

    # Notation used: points are given by [xB, Q2] in sets of 2 points so they can be used to create the appropriate TLines 
    # All (original) points are given in Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl
    # Modifications made to Stefan's binning:
        # Size of some bins were reduced so that each bin did not have a minimum border value of Q2 < 2 (due to new cut)
        # One less Q2-xB bin (combined what was left of bin 1 with bin 3
            # The odd numbered bins are relabeled so that (example) the Q2-xB bin 5 defined by Stefan is now my Q2-xB bin 3 (the points above describe the only significant changes between Stefan's binning schemes and my own)
    Draw_Lines = []
    # Each appended list is defined in the following way:
        # Draw_Lines.append([[xB_Point_1, Q2_Point_1], [xB_Point_2, Q2_Point_2]])
    
    # To draw all bins, the input of this 'Q2_xB_Border_Lines' function should be Q2_xB_Bin_Select = -1
    # Any other value will draw just one single bin corresponding to the value of 'Q2_xB_Bin_Select'
        
    # For Q2_xB Bin 1
    if(Q2_xB_Bin_Select == 1 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.126602, 2], [0.15,     2.28]])
        Draw_Lines.append([[0.15,  2.28], [0.24,     3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.24,     2.75]])
        Draw_Lines.append([[0.24,  2.75], [0.15,     2]])
        # Draw_Lines.append([[0.15, 1.98],[0.15,     1.95]])
        Draw_Lines.append([[0.15,     2], [0.126602, 2]])
        
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.15,    2], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.24, 2]])
        Draw_Lines.append([[0.24,    2], [0.15, 2]])
        # Draw_Lines.append([[0.15, 1.95], [0.15, 1.98]])
        # Draw_Lines.append([[0.15, 1.98], [0.24, 2.75]])
        # Draw_Lines.append([[0.24, 2.75], [0.24, 1.95]])
        # Draw_Lines.append([[0.24, 1.95], [0.15, 1.95]])

    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.24,  2.75], [0.24, 3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.34, 5.12]])
        Draw_Lines.append([[0.34,  5.12], [0.34, 3.63]])
        Draw_Lines.append([[0.34,  3.63], [0.24, 2.75]])
        
    # For Q2_xB Bin 4
    if(Q2_xB_Bin_Select == 4 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.24, 2], [0.24, 2.75]])
        # Draw_Lines.append([[0.24, 1.95], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.34, 3.63]])
        # Draw_Lines.append([[0.34, 3.63], [0.34, 1.95]])
        # Draw_Lines.append([[0.34, 1.95], [0.24, 1.95]])
        Draw_Lines.append([[0.34, 3.63], [0.34, 2]])
        Draw_Lines.append([[0.34, 2], [0.24, 2]])

    # For Q2_xB Bin 5
    if(Q2_xB_Bin_Select == 5 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.34, 3.63], [0.34, 5.12]])
        Draw_Lines.append([[0.34, 5.12], [0.45, 6.76]])
        Draw_Lines.append([[0.45, 6.76], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.34, 3.63]])

    # For Q2_xB Bin 6
    if(Q2_xB_Bin_Select == 6 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.34, 2], [0.34, 3.63]])
        Draw_Lines.append([[0.34, 3.63], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.45, 2.52]])
        Draw_Lines.append([[0.45, 2.52], [0.387826, 2]])
        Draw_Lines.append([[0.387826, 2], [0.34, 2]])
        # Draw_Lines.append([[0.45, 2.52], [0.381848, 1.95]])
        # Draw_Lines.append([[0.381848, 1.95], [0.34, 1.95]])
        
    # For Q2_xB Bin 7
    if(Q2_xB_Bin_Select == 7 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.45, 4.7], [0.45, 6.76]])
        Draw_Lines.append([[0.45, 6.76], [0.677, 10.185]])
        Draw_Lines.append([[0.677, 10.185], [0.7896, 11.351]])
        Draw_Lines.append([[0.7896, 11.351], [0.75, 9.52]])
        Draw_Lines.append([[0.75, 9.52], [0.708, 7.42]])
        Draw_Lines.append([[0.708, 7.42], [0.45, 4.7]])

    # For Q2_xB Bin 8
    if(Q2_xB_Bin_Select == 8 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.45, 2.52], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.708, 7.42]])
        Draw_Lines.append([[0.708, 7.42], [0.64, 5.4]])
        Draw_Lines.append([[0.64, 5.4], [0.57, 4.05]])
        Draw_Lines.append([[0.57, 4.05], [0.50, 3.05]])
        Draw_Lines.append([[0.50, 3.05],[0.45, 2.52]])

    return Draw_Lines


##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def z_pT_Border_Lines(Q2_xB_Bin_Select):
    # Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

    # For Q2_xB Bin 1
    if(Q2_xB_Bin_Select == 1):
        z_Borders  = [0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70]
        Num_z_Borders = 8
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        Num_pT_Borders = 8
        
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2):
        z_Borders  = [0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70]
        Num_z_Borders = 8
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        Num_pT_Borders = 8
        
    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3):
        z_Borders  = [0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70]
        Num_z_Borders = 8
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        Num_pT_Borders = 8

    # For Q2_xB Bin 4
    if(Q2_xB_Bin_Select == 4):
        z_Borders  = [0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70]
        Num_z_Borders = 7
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        Num_pT_Borders = 8

    # For Q2_xB Bin 5
    if(Q2_xB_Bin_Select == 5):
        z_Borders  = [0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70]
        Num_z_Borders = 7
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
        Num_pT_Borders = 7

    # For Q2_xB Bin 6
    if(Q2_xB_Bin_Select == 6):
        z_Borders  = [0.22, 0.32, 0.40, 0.47, 0.56, 0.70]
        Num_z_Borders = 6
        pT_Borders = [0.05, 0.22, 0.32, 0.42, 0.54, 0.80]
        Num_pT_Borders = 6
        
    # For Q2_xB Bin 7
    if(Q2_xB_Bin_Select == 7):
        z_Borders  = [0.15, 0.23, 0.30, 0.39, 0.50, 0.70]
        Num_z_Borders = 6
        pT_Borders = [0.05, 0.23, 0.34, 0.435, 0.55, 0.80]
        Num_pT_Borders = 6

    # For Q2_xB Bin 8
    if(Q2_xB_Bin_Select == 8):
        z_Borders  = [0.22, 0.30, 0.36, 0.425, 0.50, 0.70]
        Num_z_Borders = 6
        pT_Borders = [0.05, 0.23, 0.34, 0.45, 0.70]
        Num_pT_Borders = 5
        
        
        
    if("y_bin" in str(Binning_Method)):
        # Defining Borders for z and pT Bins (based on 'Q2_y_Bin')
#         # For Q2_y Bin 1
#         if(Q2_xB_Bin_Select == 1):
#             z_Borders      = [0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.73]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 2
#         if(Q2_xB_Bin_Select == 2):
#             z_Borders      = [0.18, 0.24, 0.30, 0.36, 0.43, 0.52, 0.62, 0.74]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 3
#         if(Q2_xB_Bin_Select == 3):
#             z_Borders      = [0.20, 0.24, 0.29, 0.36, 0.45, 0.55, 0.65, 0.78]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 4
#         if(Q2_xB_Bin_Select == 4):
#             z_Borders      = [0.26, 0.315, 0.365, 0.43, 0.515, 0.615, 0.715]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.96]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 5
#         if(Q2_xB_Bin_Select == 5):
#             z_Borders      = [0.15, 0.205, 0.26, 0.32, 0.41, 0.52, 0.73]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 6
#         if(Q2_xB_Bin_Select == 6):
#             z_Borders      = [0.18,  0.245, 0.305, 0.40, 0.515, 0.73]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 7
#         if(Q2_xB_Bin_Select == 7):
#             z_Borders      = [0.20, 0.245, 0.295, 0.36, 0.45, 0.55, 0.65, 0.78]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 8
#         if(Q2_xB_Bin_Select in [8]):
#             z_Borders      = [0.26, 0.315, 0.365, 0.43, 0.515, 0.615, 0.715]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 9/10
#         if(Q2_xB_Bin_Select in [9, 10, 11, 12]):
#             z_Borders      = [0.15, 0.21, 0.26, 0.32, 0.40, 0.50, 0.70] if(Q2_xB_Bin_Select in [9, 11, 12]) else [0.21, 0.26, 0.32, 0.40, 0.50, 0.70]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 0.95]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 13/14
#         if(Q2_xB_Bin_Select in [13, 14]):
#             z_Borders      = [0.15, 0.23, 0.30, 0.39, 0.50, 0.70]
#             Num_z_Borders  = len(z_Borders)
#             pT_Borders     = [0.05, 0.23, 0.34, 0.435, 0.55, 0.80]
#             Num_pT_Borders = len(pT_Borders)
#         # For Q2_y Bin 0 and -1
#         if(Q2_xB_Bin_Select < 1):
#             z_Borders      = [0.15, 0.70]
#             Num_z_Borders  = 1
#             pT_Borders     = [0.05, 1.0]
#             Num_pT_Borders = 1
#         if(Q2_xB_Bin_Select == 0):
#             print("ERROR")
            
        # For Q2_y Bin 1
        if(Q2_xB_Bin_Select == 1):
            z_Borders      = [0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.73]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 2
        if(Q2_xB_Bin_Select == 2):
            z_Borders      = [0.18, 0.24, 0.30, 0.36, 0.43, 0.52, 0.62, 0.74]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 3
        if(Q2_xB_Bin_Select == 3):
            z_Borders      = [0.20, 0.24, 0.29, 0.36, 0.45, 0.55, 0.65, 0.78]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 4
        if(Q2_xB_Bin_Select == 4):
            z_Borders      = [0.26, 0.315, 0.365, 0.43, 0.515, 0.615, 0.715]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.96]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 5
        if(Q2_xB_Bin_Select == 5):
            z_Borders      = [0.15, 0.205, 0.26, 0.32, 0.41, 0.52, 0.73]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 6
        if(Q2_xB_Bin_Select == 6):
            z_Borders      = [0.18,  0.245, 0.305, 0.40, 0.515, 0.73]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 7
        if(Q2_xB_Bin_Select == 7):
            z_Borders      = [0.20, 0.245, 0.295, 0.36, 0.45, 0.55, 0.65, 0.78]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 8
        if(Q2_xB_Bin_Select in [8]):
            z_Borders      = [0.26, 0.315, 0.365, 0.43, 0.515, 0.615, 0.715]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.200, 0.300, 0.40, 0.500, 0.600, 0.750]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 9/10/11
        if(Q2_xB_Bin_Select in [9, 10, 11]):
            z_Borders      = [0.15, 0.21, 0.26, 0.32, 0.40, 0.50, 0.70] if(Q2_xB_Bin_Select in [9, 12]) else [0.21, 0.26, 0.32, 0.40, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 0.95]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 12
        if(Q2_xB_Bin_Select in [12]):
            z_Borders      = [0.26, 0.32, 0.40, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 13
        if(Q2_xB_Bin_Select in [13]):
            z_Borders      = [0.15, 0.23, 0.30, 0.390, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.23, 0.34, 0.435, 0.55, 0.80]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 14
        if(Q2_xB_Bin_Select in [14]):
            z_Borders      = [0.19, 0.235, 0.305, 0.390, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.230, 0.340, 0.435, 0.55, 0.80]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 15
        if(Q2_xB_Bin_Select in [15]):
            z_Borders      = [0.22, 0.29, 0.38, 0.500, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.23, 0.34, 0.435, 0.55, 0.80]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 16
        if(Q2_xB_Bin_Select in [16]):
            z_Borders      = [0.15, 0.23, 0.30, 0.39, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.25, 0.400, 0.55, 0.80]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 17
        if(Q2_xB_Bin_Select in [17]):
            z_Borders      = [0.19, 0.245, 0.32, 0.40, 0.50, 0.70]
            Num_z_Borders  = len(z_Borders)
            pT_Borders     = [0.05, 0.23, 0.37, 0.540, 0.80]
            Num_pT_Borders = len(pT_Borders)

        # For Q2_y Bin 0 and -1
        if(Q2_xB_Bin_Select < 1):
            z_Borders      = [0.15, 0.70]
            Num_z_Borders  = 1
            pT_Borders     = [0.05, 1.0]
            Num_pT_Borders = 1

        if(Q2_xB_Bin_Select == 0):
            print("ERROR")


                    # Info about z bins              # Info about pT bins         # Total number of z-pT bins
    output = [['z', Num_z_Borders, z_Borders],['pT', Num_pT_Borders, pT_Borders], (Num_z_Borders-1)*(Num_pT_Borders-1)]
    
    return output



# For my new 2D binning (only 17 Q2-y bins)
def z_pT_Border_Lines(Q2_y_Bin_Select):
    # Defining Borders for z and pT Bins (based on 'Q2_y_Bin')

    # For Q2-y Bin 1
    if(Q2_y_Bin_Select == 1):
        z_Borders  = [0.15, 0.20, 0.24, 0.29, 0.40, 0.73]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]

    # For Q2-y Bin 2
    if(Q2_y_Bin_Select == 2):
        z_Borders  = [0.18, 0.23, 0.26, 0.31, 0.38, 0.50, 0.74]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        
    # For Q2-y Bin 3
    if(Q2_y_Bin_Select == 3):
        z_Borders  = [0.22, 0.28, 0.35, 0.45, 0.60, 0.78]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]

    # For Q2-y Bin 4
    if(Q2_y_Bin_Select == 4):
        z_Borders  = [0.26, 0.32, 0.37, 0.43, 0.50, 0.60, 0.71]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80]

    # For Q2-y Bin 5
    if(Q2_y_Bin_Select == 5):
        z_Borders  = [0.15, 0.19, 0.24, 0.29, 0.38, 0.50, 0.73]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]

    # For Q2-y Bin 6
    if(Q2_y_Bin_Select == 6):
        z_Borders  = [0.18, 0.23, 0.30, 0.39, 0.50, 0.78]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
        
    # For Q2-y Bin 7
    if(Q2_y_Bin_Select == 7):
        z_Borders  = [0.21, 0.26, 0.30, 0.44, 0.55, 0.78]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.65, 1.0]
        
    # For Q2-y Bin 8
    if(Q2_y_Bin_Select in [8]):
        z_Borders  = [0.26, 0.32, 0.36, 0.40, 0.45, 0.53, 0.72]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.52, 0.75]
        
    # For Q2-y Bin 9
    if(Q2_y_Bin_Select in [9]):
        z_Borders  = [0.15, 0.20, 0.24, 0.30, 0.38, 0.48, 0.72]
        pT_Borders = [0.05, 0.22, 0.30, 0.38, 0.46, 0.60, 0.95]
        
    # For Q2-y Bin 10
    if(Q2_y_Bin_Select in [10]):
        z_Borders  = [0.18, 0.23, 0.26, 0.32, 0.40, 0.50, 0.72]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.00]
        
    # For Q2-y Bin 11
    if(Q2_y_Bin_Select in [11]):
        z_Borders  = [0.21, 0.26, 0.32, 0.40, 0.50, 0.70]
        pT_Borders = [0.05, 0.20, 0.31, 0.40, 0.50, 0.64, 0.95]
        
    # For Q2-y Bin 12
    if(Q2_y_Bin_Select in [12]):
        z_Borders  = [0.26, 0.32, 0.40, 0.50, 0.70]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.67]
        
    # For Q2-y Bin 13
    if(Q2_y_Bin_Select in [13]):
        z_Borders  = [0.15, 0.20, 0.24, 0.30, 0.40, 0.72]
        pT_Borders = [0.05, 0.23, 0.34, 0.43, 0.55, 0.90]

    # For Q2-y Bin 14
    if(Q2_y_Bin_Select in [14]):
        z_Borders  = [0.18, 0.23, 0.27, 0.33, 0.44, 0.74]
        pT_Borders = [0.05, 0.23, 0.34, 0.44, 0.55, 0.90]
        
    # For Q2-y Bin 15
    if(Q2_y_Bin_Select in [15]):
        z_Borders  = [0.21, 0.28, 0.35, 0.47, 0.72]
        pT_Borders = [0.05, 0.23, 0.34, 0.45, 0.58, 0.90]
        
    # For Q2-y Bin 16
    if(Q2_y_Bin_Select in [16]):
        z_Borders  = [0.15, 0.20, 0.25, 0.32, 0.41, 0.71]
        pT_Borders = [0.05, 0.24, 0.36, 0.55, 0.80]
    
    # For Q2-y Bin 17
    if(Q2_y_Bin_Select in [17]):
        z_Borders  = [0.18, 0.23, 0.30, 0.38, 0.48, 0.72]
        pT_Borders = [0.05, 0.23, 0.36, 0.51, 0.85]
        
        
    Num_z_Borders  = len(z_Borders)
    Num_pT_Borders = len(pT_Borders)
        
        
    # For Q2-y Bin 0 and -1
    if(Q2_y_Bin_Select < 1):
        z_Borders      = [0.15, 0.70]
        Num_z_Borders  = 1
        pT_Borders     = [0.05, 1.0]
        Num_pT_Borders = 1
        
    if(Q2_y_Bin_Select == 0):
        print("ERROR")

                    # Info about z bins              # Info about pT bins         # Total number of z-pT bins
    output = [['z', Num_z_Borders, z_Borders], ['pT', Num_pT_Borders, pT_Borders], (Num_z_Borders-1)*(Num_pT_Borders-1)]
    
    return output

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Q2_y_Border_Lines(Q2_y_Bin_Select):
    # Defining Borders for Q2 and y Bins (based on 'Q2_y_Bin_Select')
    # Notation used: points are given by [y, Q2] in sets of 2 points so they can be used to create the appropriate TLines 
    Draw_Lines = []
    
#     ##=====####################=====##
#     ##=====##   Q2 Group 1   ##=====##
#     ##=====####################=====##
#     # For Q2_y Bin 1
#     if(Q2_y_Bin_Select == 1 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.65, 2],      [0.65, 2.7268]])
#         Draw_Lines.append([[0.65, 2.7268], [0.75, 2.7268]])
#         Draw_Lines.append([[0.75, 2.7268], [0.75, 2]])
#         Draw_Lines.append([[0.75, 2],      [0.65, 2]])
#     # For Q2_y Bin 2
#     if(Q2_y_Bin_Select == 2 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.55, 2],      [0.55, 2.7268]])
#         Draw_Lines.append([[0.55, 2.7268], [0.65, 2.7268]])
#         Draw_Lines.append([[0.65, 2.7268], [0.65, 2]])
#         Draw_Lines.append([[0.65, 2],      [0.55, 2]])
#     # For Q2_y Bin 3
#     if(Q2_y_Bin_Select == 3 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.45, 2],      [0.45, 2.7268]])
#         Draw_Lines.append([[0.45, 2.7268], [0.55, 2.7268]])
#         Draw_Lines.append([[0.55, 2.7268], [0.55, 2]])
#         Draw_Lines.append([[0.55, 2],      [0.45, 2]])
#     # For Q2_y Bin 4
#     if(Q2_y_Bin_Select == 4 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.3,  2],      [0.3,  2.7268]])
#         Draw_Lines.append([[0.3,  2.7268], [0.45, 2.7268]])
#         Draw_Lines.append([[0.45, 2.7268], [0.45, 2]])
#         Draw_Lines.append([[0.45, 2],      [0.3,  2]])
#     ##=====####################=====##
#     ##=====##   Q2 Group 2   ##=====##
#     ##=====####################=====##
#     # For Q2_y Bin 5
#     if(Q2_y_Bin_Select == 5 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.65, 2.7268], [0.65, 3.558]])
#         Draw_Lines.append([[0.65, 3.558],  [0.75, 3.558]])
#         Draw_Lines.append([[0.75, 3.558],  [0.75, 2.7268]])
#         Draw_Lines.append([[0.75, 2.7268], [0.65, 2.7268]])
#     # For Q2_y Bin 6
#     if(Q2_y_Bin_Select == 6 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.55, 2.7268], [0.55, 3.558]])
#         Draw_Lines.append([[0.55, 3.558],  [0.65, 3.558]])
#         Draw_Lines.append([[0.65, 3.558],  [0.65, 2.7268]])
#         Draw_Lines.append([[0.65, 2.7268], [0.55, 2.7268]])
#     # For Q2_y Bin 7
#     if(Q2_y_Bin_Select == 7 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.45, 2.7268], [0.45, 3.558]])
#         Draw_Lines.append([[0.45, 3.558],  [0.55, 3.558]])
#         Draw_Lines.append([[0.55, 3.558],  [0.55, 2.7268]])
#         Draw_Lines.append([[0.55, 2.7268], [0.45, 2.7268]])
#     # For Q2_y Bin 8
#     if(Q2_y_Bin_Select == 8 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.35, 2.7268], [0.35, 4.3892]])
#         Draw_Lines.append([[0.35, 4.3892], [0.45, 4.3892]])
#         Draw_Lines.append([[0.45, 4.3892], [0.45, 2.7268]])
#         Draw_Lines.append([[0.45, 2.7268], [0.35, 2.7268]])
#     ##=====####################=====##
#     ##=====##   Q2 Group 3   ##=====##
#     ##=====####################=====##
#     # For Q2_y Bin 9
#     if(Q2_y_Bin_Select == 9 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.55, 3.558],  [0.55, 4.3892]])
#         Draw_Lines.append([[0.55, 4.3892], [0.75, 4.3892]])
#         Draw_Lines.append([[0.75, 4.3892], [0.75, 3.558]])
#         Draw_Lines.append([[0.75, 3.558],  [0.55, 3.558]])
#     # For Q2_y Bin 10
#     if(Q2_y_Bin_Select == 10 or Q2_y_Bin_Select < 1):
#         # Draw_Lines.append([[0.45, 3.558], [0.45, 6.636]])
#         # Draw_Lines.append([[0.45, 6.636], [0.55, 6.636]])
#         # Draw_Lines.append([[0.55, 6.636], [0.55, 3.558]])
#         # Draw_Lines.append([[0.55, 3.558], [0.45, 3.558]])
#         Draw_Lines.append([[0.45, 3.558], [0.45, 5.636]])
#         Draw_Lines.append([[0.45, 5.636], [0.55, 5.636]])
#         Draw_Lines.append([[0.55, 5.636], [0.55, 3.558]])
#         Draw_Lines.append([[0.55, 3.558], [0.45, 3.558]])
#     ##=====####################=====##
#     ##=====##   Q2 Group 4   ##=====##
#     ##=====####################=====##
#     # For Q2_y Bin 11
#     if(Q2_y_Bin_Select == 11 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.55, 4.3892], [0.55, 5.636]])
#         Draw_Lines.append([[0.55, 5.636],  [0.75, 5.636]])
#         Draw_Lines.append([[0.75, 5.636],  [0.75, 4.3892]])
#         Draw_Lines.append([[0.75, 4.3892], [0.55, 4.3892]])
#     # For Q2_y Bin 12
#     if(Q2_y_Bin_Select == 12 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.55, 5.636],  [0.55, 8.1296]])
#         Draw_Lines.append([[0.55, 8.1296], [0.75, 8.1296]])
#         Draw_Lines.append([[0.75, 8.1296], [0.75, 5.636]])
#         Draw_Lines.append([[0.75, 5.636],  [0.55, 5.636]])
#     # For Q2_y Bin 13
#     if(Q2_y_Bin_Select == 13 or Q2_y_Bin_Select < 1):
#         Draw_Lines.append([[0.6,  8.1296], [0.6,  9.473]])
#         Draw_Lines.append([[0.6,  9.473],  [0.75, 9.473]])
#         Draw_Lines.append([[0.75, 9.473],  [0.75, 8.1296]])
#         Draw_Lines.append([[0.75, 8.1296], [0.6,  8.1296]])
        
    ##=====####################=====##
    ##=====##   Q2 Group 1   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2, 2.423
    # For Q2_y Bin 1
    if(Q2_y_Bin_Select == 1 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 2
    if(Q2_y_Bin_Select == 2 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 3
    if(Q2_y_Bin_Select == 3 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 4
    if(Q2_y_Bin_Select == 4 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.3,  Q2_min], [0.3,  Q2_max]])
        Draw_Lines.append([[0.3,  Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.3,  Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 2   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2.423, 2.987
    # For Q2_y Bin 5
    if(Q2_y_Bin_Select == 5 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 6
    if(Q2_y_Bin_Select == 6 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 7
    if(Q2_y_Bin_Select == 7 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 8
    if(Q2_y_Bin_Select == 8 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.3,  Q2_min], [0.3,  Q2_max]])
        Draw_Lines.append([[0.3,  Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.3,  Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 3   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2.987, 3.974
    # For Q2_y Bin 9
    if(Q2_y_Bin_Select == 9 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 10
    if(Q2_y_Bin_Select == 10 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 11
    if(Q2_y_Bin_Select == 11 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 12
    if(Q2_y_Bin_Select == 12 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.35, Q2_min], [0.35, Q2_max]])
        Draw_Lines.append([[0.35, Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.35, Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 4   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 3.974, 5.384
    # For Q2_y Bin 13
    if(Q2_y_Bin_Select == 13 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 14
    if(Q2_y_Bin_Select == 14 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 15
    if(Q2_y_Bin_Select == 15 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, 5.948]])
        Draw_Lines.append([[0.45, 5.948],  [0.55, 5.948]])
        Draw_Lines.append([[0.55, 5.948],  [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 5   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 5.384, 7.922
    # For Q2_y Bin 16
    if(Q2_y_Bin_Select == 16 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, 9.896]])
        Draw_Lines.append([[0.65, 9.896],  [0.75, 9.896]])
        Draw_Lines.append([[0.75, 9.896],  [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 17
    if(Q2_y_Bin_Select == 17 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])


    return Draw_Lines


##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Find_z_pT_Bin_Center(Q2_xB_Bin_Select, z_pT_Bin, variable_return="Default"):
    z_Value,     pT_Value    = "Error", "Error"
    z_Value_Max, z_Value_Min = "Error", "Error"
    
    # For Q2_xB Bin 1
    if(Q2_xB_Bin_Select == 1):
        if(z_pT_Bin in range(1,  8,  1)):
            z_Value_Max, z_Value_Min = 0.7,   0.55
        if(z_pT_Bin in range(8,  15, 1)):
            z_Value_Max, z_Value_Min = 0.55,  0.445
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.445, 0.36
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.36,  0.29
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.29,  0.24
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.24,  0.2
        if(z_pT_Bin in range(43, 50, 1)):
            z_Value_Max, z_Value_Min = 0.2,   0.15
            
######################################################################################
            
        if(z_pT_Bin in range(1, 44, 7)):
            pT_Value_Max, pT_Value_Min = 0.2,  0.05
        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3,  0.2
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4,  0.3
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5,  0.4
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6,  0.5
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0,  0.75
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2):
        if(z_pT_Bin in range(1,  8,  1)):
            z_Value_Max, z_Value_Min = 0.7,  0.6
        if(z_pT_Bin in range(8,  15, 1)):
            z_Value_Max, z_Value_Min = 0.6,  0.5
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.5,  0.41
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.41, 0.34
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.34, 0.29
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.29, 0.25
        if(z_pT_Bin in range(43, 50, 1)):
            z_Value_Max, z_Value_Min = 0.25, 0.18
            
######################################################################################
            
        if(z_pT_Bin in range(1, 44, 7)):
            pT_Value_Max, pT_Value_Min = 0.2,  0.05
        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3,  0.2
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4,  0.3
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5,  0.4
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6,  0.5
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0,  0.75
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3):
        if(z_pT_Bin in range(1,  8,  1)):
            z_Value_Max, z_Value_Min = 0.7,   0.55
        if(z_pT_Bin in range(8,  15, 1)):
            z_Value_Max, z_Value_Min = 0.55,  0.445
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.445, 0.36
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.36,  0.29
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.29,  0.24
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.24,  0.2
        if(z_pT_Bin in range(43, 50, 1)):
            z_Value_Max, z_Value_Min = 0.2,   0.15
            
######################################################################################
            
        if(z_pT_Bin in range(1, 44, 7)):
            pT_Value_Max, pT_Value_Min = 0.2,  0.05
        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3,  0.2
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4,  0.3
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5,  0.4
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6,  0.5
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0,  0.75
            
######################################################################################
######################################################################################

    # For Q2_xB Bin 4
    if(Q2_xB_Bin_Select == 4):            
        if(z_pT_Bin in range(1,  8,  1)):
            z_Value_Max, z_Value_Min = 0.7,   0.6
        if(z_pT_Bin in range(8,  15, 1)):
            z_Value_Max, z_Value_Min = 0.6,   0.5
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.5,   0.41
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.41,  0.345
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.345, 0.29
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.29,  0.2
            
######################################################################################
            
        if(z_pT_Bin in range(1, 37, 7)):
            pT_Value_Max, pT_Value_Min = 0.2,  0.05
        if(z_pT_Bin in range(2, 38, 7)):
            pT_Value_Max, pT_Value_Min = 0.3,  0.2
        if(z_pT_Bin in range(3, 39, 7)):
            pT_Value_Max, pT_Value_Min = 0.4,  0.3
        if(z_pT_Bin in range(4, 40, 7)):
            pT_Value_Max, pT_Value_Min = 0.5,  0.4
        if(z_pT_Bin in range(5, 41, 7)):
            pT_Value_Max, pT_Value_Min = 0.6,  0.5
        if(z_pT_Bin in range(6, 42, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
        if(z_pT_Bin in range(7, 43, 7)):
            pT_Value_Max, pT_Value_Min = 1.0,  0.75
            
######################################################################################
######################################################################################
            
    # For Q2_xB Bin 5
    if(Q2_xB_Bin_Select == 5):
        if(z_pT_Bin in range(1,  7,  1)):
            z_Value_Max, z_Value_Min = 0.7,   0.5
        if(z_pT_Bin in range(7,  13, 1)):
            z_Value_Max, z_Value_Min = 0.5,   0.4
        if(z_pT_Bin in range(13, 19, 1)):
            z_Value_Max, z_Value_Min = 0.4,   0.32
        if(z_pT_Bin in range(19, 25, 1)):
            z_Value_Max, z_Value_Min = 0.32,  0.26
        if(z_pT_Bin in range(25, 31, 1)):
            z_Value_Max, z_Value_Min = 0.26,  0.215
        if(z_pT_Bin in range(31, 37, 1)):
            z_Value_Max, z_Value_Min = 0.215, 0.15
            
######################################################################################
            
        if(z_pT_Bin in range(1, 32, 6)):
            pT_Value_Max, pT_Value_Min = 0.22, 0.05
        if(z_pT_Bin in range(2, 33, 6)):
            pT_Value_Max, pT_Value_Min = 0.32, 0.22
        if(z_pT_Bin in range(3, 34, 6)):
            pT_Value_Max, pT_Value_Min = 0.41, 0.32
        if(z_pT_Bin in range(4, 35, 6)):
            pT_Value_Max, pT_Value_Min = 0.51, 0.41
        if(z_pT_Bin in range(5, 36, 6)):
            pT_Value_Max, pT_Value_Min = 0.65, 0.51
        if(z_pT_Bin in range(6, 37, 6)):
            pT_Value_Max, pT_Value_Min = 1.0,  0.65
            
######################################################################################
######################################################################################

    # For Q2_xB Bin 6
    if(Q2_xB_Bin_Select == 6):
        if(z_pT_Bin in range(1,  6,  1)):
            z_Value_Max, z_Value_Min = 0.7,  0.56
        if(z_pT_Bin in range(6,  11, 1)):
            z_Value_Max, z_Value_Min = 0.56, 0.47
        if(z_pT_Bin in range(11, 16, 1)):
            z_Value_Max, z_Value_Min = 0.47, 0.4
        if(z_pT_Bin in range(16, 21, 1)):
            z_Value_Max, z_Value_Min = 0.4,  0.32
        if(z_pT_Bin in range(21, 26, 1)):
            z_Value_Max, z_Value_Min = 0.32, 0.22
            
######################################################################################
            
        if(z_pT_Bin in range(1, 22, 5)):
            pT_Value_Max, pT_Value_Min = 0.22, 0.05
        if(z_pT_Bin in range(2, 23, 5)):
            pT_Value_Max, pT_Value_Min = 0.32, 0.22
        if(z_pT_Bin in range(3, 24, 5)):
            pT_Value_Max, pT_Value_Min = 0.42, 0.32
        if(z_pT_Bin in range(4, 25, 5)):
            pT_Value_Max, pT_Value_Min = 0.54, 0.42
        if(z_pT_Bin in range(5, 26, 5)):
            pT_Value_Max, pT_Value_Min = 0.8,  0.54
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 7
    if(Q2_xB_Bin_Select == 7):
        if(z_pT_Bin in range(1,  6,  1)):
            z_Value_Max, z_Value_Min = 0.7,  0.5
        if(z_pT_Bin in range(6,  11, 1)):
            z_Value_Max, z_Value_Min = 0.5,  0.39
        if(z_pT_Bin in range(11, 16, 1)):
            z_Value_Max, z_Value_Min = 0.39, 0.3
        if(z_pT_Bin in range(16, 21, 1)):
            z_Value_Max, z_Value_Min = 0.3,  0.23
        if(z_pT_Bin in range(21, 26, 1)):
            z_Value_Max, z_Value_Min = 0.23, 0.15
            
######################################################################################

        if(z_pT_Bin in range(1, 22, 5)):
            pT_Value_Max, pT_Value_Min = 0.23,  0.05
        if(z_pT_Bin in range(2, 23, 5)):
            pT_Value_Max, pT_Value_Min = 0.34,  0.23
        if(z_pT_Bin in range(3, 24, 5)):
            pT_Value_Max, pT_Value_Min = 0.435, 0.34
        if(z_pT_Bin in range(4, 25, 5)):
            pT_Value_Max, pT_Value_Min = 0.55,  0.435
        if(z_pT_Bin in range(5, 26, 5)):
            pT_Value_Max, pT_Value_Min = 0.8,   0.55
            
######################################################################################
######################################################################################
            
    # For Q2_xB Bin 8
    if(Q2_xB_Bin_Select == 8):
        if(z_pT_Bin in range(1,  5,  1)):
            z_Value_Max, z_Value_Min = 0.7,   0.5
        if(z_pT_Bin in range(5,  9,  1)):
            z_Value_Max, z_Value_Min = 0.5,   0.425
        if(z_pT_Bin in range(9,  13, 1)):
            z_Value_Max, z_Value_Min = 0.425, 0.36
        if(z_pT_Bin in range(13, 17, 1)):
            z_Value_Max, z_Value_Min = 0.36,  0.3
        if(z_pT_Bin in range(17, 21, 1)):
            z_Value_Max, z_Value_Min = 0.3,   0.22
            
######################################################################################

        if(z_pT_Bin in range(1, 18, 4)):
            pT_Value_Max, pT_Value_Min = 0.23, 0.05
        if(z_pT_Bin in range(2, 19, 4)):
            pT_Value_Max, pT_Value_Min = 0.34, 0.23
        if(z_pT_Bin in range(3, 20, 4)):
            pT_Value_Max, pT_Value_Min = 0.45, 0.34
        if(z_pT_Bin in range(4, 21, 4)):
            pT_Value_Max, pT_Value_Min = 0.7,  0.45
            
            
    z_Value  = (z_Value_Max  + z_Value_Min)/2
    pT_Value = (pT_Value_Max + pT_Value_Min)/2
            
            
    if(variable_return == "Default"):
        return [z_Value, pT_Value]
    if("z"  in variable_return and "title" not in variable_return and "Title" not in variable_return and "str" not in variable_return):
        return z_Value
    
    if("pT" in variable_return and "title" not in variable_return and "Title" not in variable_return and "str" not in variable_return):
        return pT_Value
    
    if("z"  in variable_return and ("title" in variable_return or "Title" in variable_return or "str" in variable_return)):
        return str("".join([str(z_Value_Min),  " - ", str(z_Value_Max)]))
    
    if("pT" in variable_return and ("title" in variable_return or "Title" in variable_return or "str" in variable_return)):
        return str("".join([str(pT_Value_Min), " - ", str(pT_Value_Max)]))
    
    if(variable_return in ["title", "Title", "str"]):
        return [str("".join([str(z_Value_Min), " - ", str(z_Value_Max)])), str("".join([str(pT_Value_Min), " - ", str(pT_Value_Max)]))]


#################################################################################################################################################################
##==========##==========##     Kinematic Binning Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
#################################################################################################################################################################


















#####################################################################################################################################################################
##==========##==========##     Function for Finding Kinematic Binning Info     ##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################
def Find_Q2_y_z_pT_Bin_Stats(Q2_y_Bin_Find, z_pT_Bin_Find="All"):
    
    ####################======================================####################
    #####==========#####   Finding the Q2-y Bin Information   #####==========#####
    ####################======================================####################
    Borders_Q2_y = Q2_y_Border_Lines(Q2_y_Bin_Find)
    Q2_bin_max   = Borders_Q2_y[0][1][1]
    Q2_bin_min   = Borders_Q2_y[0][0][1]
    y_bin_max    = Borders_Q2_y[1][1][0]
    y_bin_min    = Borders_Q2_y[1][0][0]
    Q2_Center    = (Q2_bin_max + Q2_bin_min)/2
    y_Center     = (y_bin_max  + y_bin_min)/2
    ####################======================================####################
    #####==========#####    Found the Q2-y Bin Information    #####==========#####
    ####################======================================####################
    
    ####################======================================####################
    #####==========#####   Finding the z-pT Bin Information   #####==========#####
    ####################======================================####################
    Borders_z_pT   = z_pT_Border_Lines(Q2_y_Bin_Find)
    z_length       = Borders_z_pT[0][1] - 1
    pT_length      = Borders_z_pT[1][1] - 1
    if(str(z_pT_Bin_Find) not in ["All", "0"]):
        # This finds the dimensions of a particular z-pT bin for a given Q2-y bin
        z_bin      = ((z_pT_Bin_Find - 1) // pT_length) + 1
        z_bin      = (z_length + 1) - z_bin
        pT_bin     = ((z_pT_Bin_Find - 1) %  pT_length) + 1
        z_bin_max  = Borders_z_pT[0][2][z_bin]
        z_bin_min  = Borders_z_pT[0][2][z_bin  - 1]
        pT_bin_max = Borders_z_pT[1][2][pT_bin]
        pT_bin_min = Borders_z_pT[1][2][pT_bin - 1]
    else:
        # This gives the overall dimensions of the combined z-pT binning scheme for a given Q2-y bin (i.e., if all z-pT binned events are to be included)
        z_bin_max  = Borders_z_pT[0][2][len(Borders_z_pT[0][2]) - 1]
        z_bin_min  = Borders_z_pT[0][2][0]
        pT_bin_max = Borders_z_pT[1][2][len(Borders_z_pT[1][2]) - 1]
        pT_bin_min = Borders_z_pT[1][2][0]
    z_Center       = (z_bin_max  + z_bin_min)/2
    pT_Center      = (pT_bin_max + pT_bin_min)/2
    ####################======================================####################
    #####==========#####    Found the z-pT Bin Information    #####==========#####
    ####################======================================####################
    
    # Return order goes as [[Q2_bin_info, y_bin_info], [z_bin_info, pT_bin_info]]
        # Order of bin_info goes as: bin_info = [min_bin, center_bin, max_bin]
    return [[[Q2_bin_min, Q2_Center, Q2_bin_max], [y_bin_min, y_Center, y_bin_max]], [[z_bin_min, z_Center, z_bin_max], [pT_bin_min, pT_Center, pT_bin_max]]]


#####################################################################################################################################################################
##==========##==========##     Function for Finding Kinematic Binning Info     ##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################


















############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################

def Full_Calc_Fit(Histo, version="norm"):
    
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

    # def Full_Calc_Fit(Histo):
    #     x_data, y_data = [], []
    #     try:
    #         # print("Histo.GetNbinsX() =", Histo.GetNbinsX())
    #         for ii in range(0, Histo.GetNbinsX(), 1):
    #             x_data.append(Histo.GetBinCenter(ii))
    #             y_data.append(Histo.GetBinContent(ii))
    #         # Perform optimization using the Nelder-Mead method
    #         initial_guess = [1e6, 1, 1, 1, 1]  # Initial guess for A, B, C, D, E
    #         optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)
    #         # Extract the optimized parameters
    #         A_opt, B_opt, C_opt, D_opt, E_opt = optim_params
    #         # print("A_opt =", A_opt)
    #         # print("B_opt =", B_opt)
    #         # print("C_opt =", C_opt)
    #         # print("D_opt =", D_opt)
    #         # print("E_opt =", E_opt)
    #     except:
    #         print("".join([color.RED, color.BOLD, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
    #         print(color.RED, color.BOLD, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)
    #         A_opt, B_opt, C_opt, D_opt, E_opt = "Error", "Error", "Error", "Error", "Error"
    #     return [A_opt, B_opt, C_opt, D_opt, E_opt]
    
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
##==========##==========##     Canvas Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################
def Canvas_Create(Name, Num_Columns=1, Num_Rows=1, Size_X=600, Size_Y=800, cd_Space=0):
    canvas_test = ROOT.TCanvas(str(Name), str(Name), Size_X, Size_Y)
    canvas_test.Divide(Num_Columns, Num_Rows, cd_Space, cd_Space)
    canvas_test.SetGrid()
    ROOT.gStyle.SetAxisColor(16, 'xy')
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(1)
    return canvas_test


##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Draw_Canvas(canvas, cd_num, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1):
    canvas.cd(cd_num)
    try:
        canvas.cd(cd_num).SetLeftMargin(left_add)
        canvas.cd(cd_num).SetRightMargin(right_add)
        canvas.cd(cd_num).SetTopMargin(up_add)
        canvas.cd(cd_num).SetBottomMargin(down_add)
    # except:
    #     print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
    except Exception as e:
        print("".join([color.RED, color.BOLD, "Draw_Canvas(...) ERROR: ", color.LIGHT, str(e), color.END]))
        print("".join(["canvas: ", str(canvas.GetName()), "\ncd_num: ", str(cd_num)]))


def palette_move(canvas, histo, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1):
    canvas.Modified()
    canvas.Update()
    palette_test = 0
    while(palette_test < 4 and palette_test != -1):
        try:
            palette_histo = histo.GetListOfFunctions().FindObject("palette")

            palette_histo.SetX1NDC(x_left)
            palette_histo.SetX2NDC(x_right)
            palette_histo.SetY1NDC(y_down)
            palette_histo.SetY2NDC(y_up)

            canvas.Modified()
            canvas.Update()
            palette_test = -1
        except:
            palette_test += 1
    if(palette_test > 0):
            print("\nFailed to move palette...")
            
            
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def statbox_move(Histogram, Canvas, Default_Stat_Obj="", Y1_add=0.05, Y2_add=0.25, X1_add=0.05, X2_add=0.35, Print_Method="norm"):
    finding, search = 0, 0
    while(finding == 0 and search < 5):
        if(Default_Stat_Obj == ""):
            Default_Stat_Obj = Histogram.GetListOfFunctions().FindObject("stats")

        if("TPaveStats" not in str(type(Default_Stat_Obj))):
            try:
                Default_Stat_Obj = Histogram.GetListOfFunctions().FindObject("stats")# Default_Stat_Obj.FindObject("stats")
            except Exception as e:
                print("".join([color.RED, "statbox_move(...) ERROR:", str(e), "\nTRACEBACK:\n", color.END, str(traceback.format_exc())]))
        try:
            if(Print_Method == "norm"):
                Default_Stat_Obj.SetY1NDC(Y1_add)
                Default_Stat_Obj.SetY2NDC(Y2_add)
                Default_Stat_Obj.SetX1NDC(X1_add)
                Default_Stat_Obj.SetX2NDC(X2_add)
            if(Print_Method in ["off", "Off"]):
                Default_Stat_Obj.SetY1NDC(0)
                Default_Stat_Obj.SetY2NDC(0)
                Default_Stat_Obj.SetX1NDC(0)
                Default_Stat_Obj.SetX2NDC(0)
            Default_Stat_Obj.Draw("same")
            Canvas.Modified()
            Canvas.Update()
            finding += 1
        except:
            Canvas.Modified()
            Canvas.Update()
            finding = 0
            search += 1
    if(search > 4):
        print("Failed search")

        
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def print_rounded_str(number, rounding=0):
    try:
        if(rounding != 0 and abs(number) >= 0.001):
            output = round(number, rounding)
            output = "".join(["{:.", str(rounding), "}"]).format(number)
            # print("round")
        elif(rounding != 0):
            output = "".join(["{:.", str(rounding-1), "e}"]).format(number)
            # print("science")
        else:
            # print("other")
            output = number
        return output
    except Exception as e:
        print("".join([color.BOLD, color.RED, "print_rounded_str(...) ERROR: number = ", str(output), " is not accepted", " --> failed to round input..." if(rounding != 0) else "", "\nERROR Output Is: \n", str(e), color.END]))
        print("".join([color.RED, "TRACEBACK:\n", color.END, str(traceback.format_exc())]))
        return number
    
    
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Error_Propagation(Type_of_Prop, Error1, Error2=0, Number1=0, Number2=0, Result=False):
    Error = False
    try:
        if("ave" in Type_of_Prop or "Ave" in Type_of_Prop or "average" in Type_of_Prop or "Average" in Type_of_Prop):
            # Average of given numbers
            if(type(Error1) is list):
                for x in Error1:
                    Error += (x - np.average(Error1))**2
                Error /= (len(Error1) - 1)
                Error *= 1/2
            else:
                ave = (Error1 + Error2)/2
                Error = ((Error1 - ave)**2 + (Error2 - ave)**2)**0.5
                
        if("add" in Type_of_Prop or "Add" in Type_of_Prop or "subtract" in Type_of_Prop or "Subtract" in Type_of_Prop or "sub" in Type_of_Prop or "Sub" in Type_of_Prop):
            # Addition or Subtraction
            Error = ((Error1)**2 + (Error2)**2)**0.5
            
        if("mult" in Type_of_Prop or "Mult" in Type_of_Prop or "multiply" in Type_of_Prop or "Multiply" in Type_of_Prop):
            # Multiplication
            if(not Result):
                Error = (Number1*Number2)*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            else:
                Error = Result*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            
        if("div" in Type_of_Prop or "Div" in Type_of_Prop or "divide" in Type_of_Prop or "Divide" in Type_of_Prop):
            # Division
            if(not Result):
                Error = (Number1/Number2)*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            else:
                Error = Result*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
        
        if(not Error):
            print("ERROR: error not calculated... (See option selection for 'Type_of_Prop')")
        else:
            return Error
    except Exception as e:
        print("".join([color.RED, "Error taking Error Propagation with inputs:\n", color.END, "Type_of_Prop = ", str(Type_of_Prop), ", Error1 = ", str(Error1), ", Error2 = ", str(Error2), ", Number1 = ", str(Number1), ", Number2 = ", str(Number2), "".join([", Result = ", str(Result)]) if(not Result) else ""]))
        print("Error is: \n\t" + str(e))
        print("".join([color.RED, "TRACEBACK:\n", color.END, str(traceback.format_exc())]))
        
        
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Get_Max_Y_Histo_1D(Histo_List, Norm_Q="Default"):
    try:
        if(type(Histo_List) is not list):
            Histo_List = [Histo_List]
        Max_Y = 0
        for Histo in Histo_List:
            if(type(Histo) is not bool and type(Histo) is not str):
                # print("".join([color.BOLD, color.BLUE, "\n'", str(Histo.GetName()), "' Maximum = ", str(Histo.GetBinContent(Histo.GetMaximumBin())), " Total = ", str(Histo.Integral()), color.END]))
                if(Histo.Integral() != 0 and Histo.GetBinContent(Histo.GetMaximumBin()) != 0):
                    Test_Y = (Histo.GetBinContent(Histo.GetMaximumBin())) if((Norm_Q not in ["Normalized", "Norm"]) or (Norm_Q == "Default")) else ((Histo.GetBinContent(Histo.GetMaximumBin()))/(Histo.Integral()))
                else:
                    Test_Y = 0
                    print("".join([color.BOLD, color.RED, "\n EMPTY HISTOGRAM: '", str(Histo.GetName()), "'\n\tMaximum = ", str(Histo.GetBinContent(Histo.GetMaximumBin())), "\n\tTotal = ", str(Histo.Integral()), color.END]))
                    print(Histo_List)
                    print(Histo)
                    for Histo2 in Histo_List:
                        print("".join(["".join([color.BOLD, color.BLUE]) if(Histo2 == Histo) else "\n", str(Histo2), color.END if(Histo2 == Histo) else "\n"]))
                if(Test_Y > Max_Y):
                    Max_Y = Test_Y   
        return Max_Y
    except:
        print("".join([color.BOLD, color.RED, "\nERROR IN GETTING THE MAX Y OF THE 1D HISTOGRAMS...", color.END]))
        print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc())]))
        print(Histo_List)
        return "ERROR"
    
    
######################################################################################################################################################
##==========##==========##     Canvas Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################








#####################################################################################################################################################
##==========##==========##     Missing Mass Lines for z-pT Histograms      ##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################


def MM_z_pT_Draw(z_val=0.1, MM_val=1.5, Q2_y_Bin=1):
    Q2_val = 4.00
    y_val  = 0.55
    if(str(Q2_y_Bin) in ["1",  "2",  "3",  "4"]):
        Q2_val = 2.2115
    if(str(Q2_y_Bin) in ["5",  "6",  "7",  "8"]):
        Q2_val = 2.7050
    if(str(Q2_y_Bin) in ["9",  "10", "11", "12"]):
        Q2_val = 3.4805
    if(str(Q2_y_Bin) in ["13", "14"]):
        Q2_val = 4.6790
    if(str(Q2_y_Bin) in ["15"]):
        Q2_val = 4.9610
    if(str(Q2_y_Bin) in ["16"]):
        Q2_val = 7.6400
    if(str(Q2_y_Bin) in ["17"]):
        Q2_val = 6.6530
        
    if(str(Q2_y_Bin) in ["1", "5", "9",  "13", "16"]):
        y_val  = 0.7
    if(str(Q2_y_Bin) in ["2", "6", "10", "14", "17"]):
        y_val  = 0.6
    if(str(Q2_y_Bin) in ["3", "7", "11", "15"]):
        y_val  = 0.5
    if(str(Q2_y_Bin) in ["4", "8"]):
        y_val  = 0.4
    if(str(Q2_y_Bin) in ["12"]):
        y_val  = 0.375
    
    Ebeam = 10.6041
    mpro  = 0.938272
    mpip  = 0.13957
    
    pT_val = ((mpro*mpro + mpip*mpip - Q2_val - MM_val*MM_val)/(2*y_val*Ebeam)) + mpro*(z_val + 1)
    
    return pT_val


#####################################################################################################################################################
##==========##==========##     Missing Mass Lines for z-pT Histograms      ##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################




















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
            if("y_bin" not in str(Binning_Method)):
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
#             NumBins_List.append(20)
            NumBins_List.append(80)
            
    # Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
    Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin) if(Q2_xB_Bin not in [0, '0', 'all', 'All']) else "All", ", z-PT-Bin=All]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
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
            Drawing_Histo_Set = Drawing_Histo_Found.Project3D('yz')
            Drawing_Histo_Set.SetName(str(Drawing_Histo_Found.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin in ["All", 0]) else str(z_pT_Bin)])))
            Drawing_Histo_Title = (str(Drawing_Histo_Set.GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin not in ["All", 0]) else "All", "}}}"]))
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
        Drawing_Histo_Set.SetTitle((Drawing_Histo_Set.GetTitle()).replace("Q^{2}-x_{B} Bin: All" if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin not in ["All", 0]) else "All", "}"])))
        # print("".join([color.BLUE, "Q2-xB plots:", color.END, "\n", str(Drawing_Histo_Set.GetTitle()), "\n", str(Find_Name), "\n\n"]))
        Q2_xB_borders, line_num = {}, 0
        for b_lines in Q2_xB_Border_Lines(-1):
            Q2_xB_borders[line_num] = ROOT.TLine()
            Q2_xB_borders[line_num].SetLineColor(1)    
            Q2_xB_borders[line_num].SetLineWidth(2)
            Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
            line_num += 1
        if((Q2_xB_Bin not in ["All", 0]) and ("y_bin" not in str(Binning_Method))):
            
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
        Drawing_Histo_Set.SetTitle((Drawing_Histo_Set.GetTitle()).replace("Q^{2}-x_{B} Bin: All" if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin not in ["All", 0]) else "All", "}"])))
        try:
            Q2_y_borders, Q2_y_borders_New = {}, {}
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
                
            # if((Q2_xB_Bin != -1) and ("y_bin" in str(Binning_Method))):
            #     for b_lines_New in Q2_y_Border_Lines(Q2_xB_Bin):
            #         try:
            #             Q2_y_borders_New[(line_num_New)] = ROOT.TLine()
            #         except:
            #             print(color.RED, "Error in Q2_y_borders_New[(line_num_New)]", color.END)
            #         Q2_y_borders_New[(line_num_New)].SetLineColor(2)
            #         Q2_y_borders_New[(line_num_New)].SetLineWidth(3)
            #         Q2_y_borders_New[(line_num_New)].DrawLine(b_lines_New[0][0], b_lines_New[0][1], b_lines_New[1][0], b_lines_New[1][1])
            #         line_num_New += 1
                
            # # print(Q2_y_Border_Lines(13))
            # Q2_y_borders_New["Cancel_1"] = ROOT.TLine()
            # Q2_y_borders_New["Cancel_1"].SetLineColor(2)
            # Q2_y_borders_New["Cancel_1"].SetLineWidth(2)
            # Q2_y_borders_New["Cancel_1"].DrawLine(Q2_y_Border_Lines(13)[0][0][0], Q2_y_Border_Lines(13)[0][0][1], Q2_y_Border_Lines(13)[1][1][0], Q2_y_Border_Lines(13)[1][1][1])
            # Q2_y_borders_New["Cancel_2"] = ROOT.TLine()
            # Q2_y_borders_New["Cancel_2"].SetLineColor(2)
            # Q2_y_borders_New["Cancel_2"].SetLineWidth(2)
            # Q2_y_borders_New["Cancel_2"].DrawLine(Q2_y_Border_Lines(13)[1][0][0], Q2_y_Border_Lines(13)[1][0][1], Q2_y_Border_Lines(13)[2][1][0], Q2_y_Border_Lines(13)[2][1][1])
 
        except:
            print("".join([color.RED, color.BOLD, "Q2-y line fail...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            
            
            
    if((Q2_xB_Bin not in ["All", 0]) and ("Var-D1='z" in str(Find_Name)) and ("Var-D2='pT" in str(Find_Name))):
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
                
        if("y" in str(Binning_Method) and False):
            MM_z_pT_borders = {}
            for MM in [0.94, 1.5, 2.5]:
                # print("".join(["MM_z_pT_Draw(z_val=0.1, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_xB_Bin), ") ="]), MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_xB_Bin))
                # print("".join(["MM_z_pT_Draw(z_val=0.8, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_xB_Bin), ") ="]), MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_xB_Bin))
                MM_z_pT_borders[MM] = ROOT.TLine()
                MM_z_pT_borders[MM].SetLineColor(6 if(MM == 0.94) else 8 if(MM == 1.5) else 46)
                MM_z_pT_borders[MM].SetLineWidth(2)
                MM_z_pT_borders[MM].DrawLine(MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_xB_Bin), 0.1, MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_xB_Bin), 0.8)
                

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










def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default"):
    
#############################################################################################################
#####=========================#####=======================================#####=========================#####
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Default)   #####=====#####=====#####=====#####
#####=========================#####=======================================#####=========================#####
#############################################################################################################
    if(Method in ["SVD", "Default"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
#         print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
                        
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
###############################################################################################################
#####=========================#####=========================================#####=========================#####
#####=====#####=====#####=====#####     End of Method:  "SVD" (Default)     #####=====#####=====#####=====#####
#####=========================#####=========================================#####=========================#####
###############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################
    elif(Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        # print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(MC_REC_1D.GetName()).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""), ""]))
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(Name_Print).replace("(Data-Type='mdf'), ", "")]))
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            # Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance Correction factor for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Acceptance.GetYaxis().SetTitle("#frac{Number of REC Events}{Number of GEN Events}")
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            
            cut_criteria = (0.01*Bin_Acceptance.GetBinContent(Bin_Acceptance.GetMaximumBin()))
            
            # for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
            #     if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
            #         print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...", color.END]))
            #         Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BOLD, color.CYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.", color.END]))
            return [Bin_Unfolded, Bin_Acceptance]
        except:
            print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (Bin-by-Bin)...", color.END]))
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
    elif("RooUnfold" in str(Method)):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))        
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        # print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")]))
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        # print("".join([color.RED, color.BOLD, "\t\tnBins_CVM = ", str(nBins_CVM), "\n\t\tMinBinCVM = ", str(MinBinCVM), "\n\t\tMaxBinCVM = ", str(MaxBinCVM), color.END]))
        
        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D.GetNbinsX() == Response_2D.GetNbinsY()):
            try:
                Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                
##==============##=======================================================##==============##
##==============##=====##     Constructing Response_RooUnfold     ##=====##==============##
##==============##=======================================================##==============##

                ##======================================##
                ##=====##     Generated Bins     ##=====##
                ##======================================##
                for gen_bin in range(0, nBins_CVM + 1, 1):
                    sum_of_gen = 0
                    gen_val    = Response_2D.GetXaxis().GetBinCenter(gen_bin)
                    ##======================================##
                    ##=====##   Reconstructed Bins   ##=====##
                    ##======================================##
                    for rec_bin in range(0, nBins_CVM + 1, 1):
                        rec_val = Response_2D.GetYaxis().GetBinCenter(rec_bin)
                        Res_Val = Response_2D.GetBinContent(gen_bin,  rec_bin)
                        sum_of_gen += Res_Val
                        
                        Response_RooUnfold.Fill(rec_val, gen_val, w=Res_Val)
                    ##======================================##
                    ##=====##   Reconstructed Bins   ##=====##
                    ##======================================##
                    gen_val_TRUE = MC_GEN_1D.GetBinContent(gen_bin)
                    if((gen_val_TRUE >= sum_of_gen) and (gen_val == MC_GEN_1D.GetBinCenter(gen_bin))):
                        gen_val_MISSED = gen_val_TRUE - sum_of_gen
                        Response_RooUnfold.Miss(gen_val, w=gen_val_MISSED)
                    else:
                        print("".join([color.RED, """
===================================================================================================================================================================================""", color.BOLD, """
MAJOR ERROR: sum_of_gen (""", str(sum_of_gen), """) is greater than gen_val_TRUE (""", str(gen_val_TRUE), """) for gen_bin = """, str(gen_bin), """ (i.e., there are more matched generated events than there should be generated events total)
             Error in this aspect of the code (need to check procedure/rewrite code)""", color.END, color.RED, """
===================================================================================================================================================================================
""", color.END]))
                ##======================================##
                ##=====##     Generated Bins     ##=====##
                ##======================================##
                
##==============##========================================================##==============##
##==============##=====##    Constructed the Response_RooUnfold    ##=====##==============##
##==============##========================================================##==============##


##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if(str(Method) in ["RooUnfold", "RooUnfold_bayes"]):
                    Unfold_Title = "RooUnfold (Bayesian)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " method to unfold...", color.END]))

                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = 10 if(("Multi_Dim" not in str(Name_Main)) or ("Multi_Dim_z_pT_Bin" in str(Name_Main))) else 4
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)

                elif("svd" in str(Method)):
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
                    print("".join(["\t", color.RED, "Method '", color.BOLD, str(Method), color.END, color.RED, "' is unknown/undefined...", color.END]))
                    print("".join(["\t", color.RED, "Defaulting to using the ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.RED, " method to unfold...", color.END]))

                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = 10
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)


##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                Unfolded_Histo = Unfolding_Histo.Hunfold()
                # Unfolding_Histo.PrintTable(cout, hTrue);

                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print("".join([color.BOLD, color.CYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return [Unfolded_Histo, Response_RooUnfold]

                        
            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (RooUnfold)...", color.END]))
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


















#####################################################################################################################################################################
##==========##==========##     Multidimensional Slice Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################

def MultiD_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="Combined_phi_t_Q2", Smear="", Out_Option="Save", Fitting="default"):
    Unfolded_Fit_Function = {}
    if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
        # print(color.BOLD, color.BLUE, "\nRunning MultiD_Slice(...) with the following info:", color.END, color.BOLD, "\n\tHisto =", str(Histo), "\n\n\tTitle =", str(Title), "\n\n\tName =", str(Name), "\n\n\tMethod =", str(Method), "\n\n\tVariable =", str(Variable), "\n\n\tSmear =", str(Smear), "\n\n\tOut_Option =", str(Out_Option), "\n\n\tFitting =", str(Fitting), "\n\n", color.END)
        print(color.BOLD, color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
    else:
        print(color.RED, color.BOLD, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
        return "Error"
    
    try:
        Output_Histos, Output_Canvas = {}, {}

        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("Combined_" not in str(Name) and "Multi_Dim" not in str(Name)):
                print("ERROR: WRONG TYPE OF HISTOGRAM")
                print("Name =", Name)
                print("MultiD_Slice() should be used on 1D histograms with the 'Combined_' or 'Multi_Dim_' bin variable\n\n")
                return "Error"
            if(("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_y_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_phi_t_smeared'" not in str(Name)) and (("'Combined_phi_t_Q2" not in str(Name).replace("_smeared", "") and "'Combined_phi_t_Q2_smeared'" not in str(Name)))):
                print("ERROR in MultiD_Slice(): Not set up for other variables (yet)")
                print("Name =", Name, "\n\n")
                return "Error"

        # if(Variable not in ["Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method), "_smeared"])]):
        if(Variable not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t_smeared"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method), "_smeared"]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method), "_smeared"])]):
            print("ERROR in MultiD_Slice(): Not set up for other variables (yet)")
            print("Variable =", Variable, "\n\n")
            return "Error"

        if(("mear" in str(Smear))     and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable, "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared" in str(Variable))):
            Smear = "Smear"

        Name = Name.replace("(Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), ", "".join(["(Multi-Dim Histo='", str(Method), "'), (Multi_Dim_Var_Info), "]))
        Name = Name.replace("".join(["(Binning-Type='y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), "]), "")
        Name = Name.replace("Binning-Type='y_bin'-", "")
        Name = Name.replace("".join(["(Binning-Type='", str(Binning_Method).replace("_", ""), "'-[Q2-xB-Bin=All, z-PT-Bin=All]), "]), "")
        Name = Name.replace("".join(["Binning-Type='",  str(Binning_Method).replace("_", ""), "'-"]), "")
        Name = Name.replace("".join([", (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")
        Name = Name.replace("".join([", (Var-D2='z_pT_Bin", str(Binning_Method), "_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")
        
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not Sim_Test) else "]{(MC REC - Test)}"])
            # if(not Sim_Test):
            Variable = Variable.replace("_smeared", "")
            Smear = ""
            
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
            # if((Sim_Test) and ("_smeared" not in str(Variable)) and (Smear in [""])):
            #     Variable = "".join([str(Variable), "_smeared"])
            #     Smear = "Smear"
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable = Variable.replace("_smeared", "")
            Smear = ""
            
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[30]{(Bayesian Unfolded)}"])


        if(Title == "Default"):
            Title = str(Histo.GetTitle())
        elif(Title in ["norm", "standard"]):
            Title = "".join(["#splitline{", str(root_color.Bold), "{Multi-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{Multi_Dim_Var_Info}"])
            
            
        if(not extra_function_terms):
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
            fit_function       = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
        else:
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
            fit_function       = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"
            
            # fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}) + E Cos(4#phi_{h}))"
            # fit_function       = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)) + [E]*cos(4*x*(3.1415926/180)))"

        
        if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting in ["default", "Default"])):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
            

                               # ['min',  'max',   'num_bins', 'size']
        Q2_Binning             = [1.4805, 11.8705, 20,         0.5195]
        Q2_xB_Binning          = [0,      8,       8,          1]
        # Q2_y_Binning         = [0,      18,      18,         1]
        Q2_y_Binning           = [-0.5,   18.5,    19,         1]
        
        Q2_y_z_pT_4D_Binning   = [-0.5,   566.5,   567,        1]
        Q2_y_z_pT_4D_Binning   = [-0.5,   512.5,   513,        1]
        Q2_y_z_pT_4D_Binning   = [-0.5,   506.5,   507,        1]

        phi_h_Binning          = [0,      360,     24,         15]
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            phi_h_Binning      = [0,      360,     12,         30]
            phi_h_Binning      = [0,      360,     10,         36]

        # Combined_phi_h_Q2_Bins = 480

        NewDim_Bin_Min  = Q2_xB_Binning[0]
        NewDim_Bin_Max  = Q2_xB_Binning[1]
        NewDim_Bin_Num  = Q2_xB_Binning[2]
        NewDim_Bin_Size = Q2_xB_Binning[3]
        Num_Columns_Canvas, Num_Rows_Canvas = 4, 2
        Multi_Dim_Var  = "Q2_xB"
        
        
        NewDim_Bin_Min  = Q2_y_Binning[0]
        NewDim_Bin_Max  = Q2_y_Binning[1]
        NewDim_Bin_Num  = Q2_y_Binning[2]
        NewDim_Bin_Size = Q2_y_Binning[3]
        Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
        Multi_Dim_Var  = "Q2_y"
        if(Variable in ["Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared"]):
            NewDim_Bin_Min  = Q2_Binning[0]
            NewDim_Bin_Max  = Q2_Binning[1]
            NewDim_Bin_Num  = Q2_Binning[2]
            NewDim_Bin_Size = Q2_Binning[3]
            Multi_Dim_Var   = "Q2"
            Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
            
        Canvas_Size_X = 2400
        Canvas_Size_Y = 1200 if(Num_Rows_Canvas < 3) else 2400
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            NewDim_Bin_Min  = Q2_y_z_pT_4D_Binning[0]
            NewDim_Bin_Max  = Q2_y_z_pT_4D_Binning[1]
            NewDim_Bin_Num  = Q2_y_z_pT_4D_Binning[2]
            NewDim_Bin_Size = Q2_y_z_pT_4D_Binning[3]
            Num_Columns_Canvas, Num_Rows_Canvas = 24, 24
            Multi_Dim_Var   = "Q2_y_z_pT"
            Canvas_Size_X   = 4800
            Canvas_Size_Y   = 4800
            
        Output_Canvas = Canvas_Create(Name.replace("Multi_Dim_Var_Info", str(Method)), Num_Columns=Num_Columns_Canvas, Num_Rows=Num_Rows_Canvas, Size_X=Canvas_Size_X, Size_Y=Canvas_Size_Y, cd_Space=0)
        
        bin_ii = 0 if(Common_Name not in ["New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"]) else 1
        # for NewDim_Bin in range(0, NewDim_Bin_Num + 1, 1):
        for NewDim_Bin in range(0, NewDim_Bin_Num - 1, 1):
            # if(NewDim_Bin != 0 and (Common_Name not in ["Multi_Dimension_Unfold_V3_All", "New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All"])):
            #     bin_ii  += -1
            if(NewDim_Bin != 0 and (Common_Name not in ["Multi_Dimension_Unfold_V3_All", "New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"])):
                bin_ii  += -1
            
            Name_Out = str(Name.replace("Multi_Dim_Var_Info", "".join([str(Multi_Dim_Var), "_Bin_", str(NewDim_Bin)])))
            
            Title_Out = str(Title.replace("Range: -1.5 #rightarrow 481.5 - Size: 1.0 per bin", "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))
            Title_Out = str(Title_Out.replace("Multi_Dim_Var_Info",                            "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))

            Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
            
            # print("".join(["\nFilling for: ", "Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]"])]))
            
            # print("\n(Start) NewDim_Bin =", NewDim_Bin, "\nbin_ii =", bin_ii, "\n")
            # print("".join([str(Multi_Dim_Var), "_Bin_", str(NewDim_Bin)]))
            ii_bin_num = 1
            for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                # print("(", ii_bin_num, ") bin_ii =", bin_ii)
                ii_bin_num += 1
                bin_jj = Histo.FindBin(bin_ii)
                Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                
                # print(color.GREEN, "Multi_Dim_phi_num =", Multi_Dim_phi_num, color.END)
                # print(color.BLUE,  "Multi_Dim_phi_err =", Multi_Dim_phi_err, color.END)
                
                # print("".join(["phi bin = ", str(phi_bin), "\nbin_ii  = ", str(bin_ii), "\nbin_jj  = ", str(bin_jj), "\nMulti_Dim_phi_num = ", str(Multi_Dim_phi_num), "\n"]))
                Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],  Multi_Dim_phi_num)
                # print(color.BOLD,  "Normal Error =", Output_Histos[Name_Out].GetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3])), color.END)
                Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), Multi_Dim_phi_err)
                bin_ii += 1
                
            # print(Histo.GetNbinsX())
                
                
            # Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
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
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian"]):
                Output_Histos[Name_Out].SetLineColor(30)
                Output_Histos[Name_Out].SetMarkerColor(30)

                
            Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
                
            Output_Canvas.Modified()
            Output_Canvas.Update()
            
            if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting in ["default", "Default"])):
                # if(Method in ["bayes", "bayesian", "Bayesian"]):
                if(not extra_function_terms):
                    A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Output_Histos[Name_Out])
                else:
                    # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(Output_Histos[Name_Out])
                    A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Output_Histos[Name_Out])
                print(color.BOLD, color.GREEN, "\nNewDim_Bin =", NewDim_Bin, color.END)
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])] = ROOT.TF1("".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)]), str(fit_function), 0, 360)
                if(not extra_function_terms):
                    print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]), color.END)
                    # print(color.BOLD, color.PURPLE, "\n\n", fit_function, "\n\n", color.END)
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(0, "Parameter A")
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(1, "Parameter B")
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(2, "Parameter C")
                
                else:
                    # print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold), str(E_Unfold)]), color.END)
                    print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold)]), color.END)

                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(0, "Parameter A")
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(1, "Parameter B")
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(2, "Parameter C")
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(3, "Parameter D")
                    # Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParName(4, "Parameter E")

                
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetRange(0, 360)
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetLineColor(2)

                if("Error" not in [A_Unfold, B_Unfold, C_Unfold] or False):
                    # This is the constant scaling factor - A (should basically always be positive)
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(0,      abs(A_Unfold))
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(0, 0.95*abs(A_Unfold), 1.05*abs(A_Unfold))
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                    # Cos(phi) Moment - B
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(1, B_Unfold)
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(1, B_Unfold - 0.05*abs(B_Unfold), B_Unfold + 0.05*abs(B_Unfold))
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                    # Cos(2*phi) Moment - C
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(2, C_Unfold)
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(2, C_Unfold - 0.05*abs(C_Unfold), C_Unfold + 0.05*abs(C_Unfold))
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))
        
                    if(extra_function_terms):
                        try:
                            Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(3, D_Unfold)
                            Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(3, D_Unfold - 5.5*abs(D_Unfold), D_Unfold + 5.5*abs(D_Unfold))
                            
                            # Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(4, E_Unfold)
                            # Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(4, E_Unfold - 5.5*abs(E_Unfold), E_Unfold + 5.5*abs(E_Unfold))
                        except:
                            print("".join([color.RED, color.BOLD, "Unfolded_Fit_Function[...] ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        
#                 else:
#                     print(color.RED, color.BOLD, "\nFIXING PARAMETERS FOR TESTING\n", color.END)
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])] = ROOT.TF1("".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_")]), "[A]", 0, 360)
# #                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetRange(0, 360)
#                     # This is the constant scaling factor - A
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(0, 0.50*abs(Output_Histos[Name_Out].GetMaximum)
#                     Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(0, 0.45*abs(Output_Histos[Name_Out].GetMaximum, 0.55*abs(Output_Histos[Name_Out].GetMaximum)

                    # Fitting the plots now
                    Output_Histos[Name_Out].Fit(Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])], "RB")
                else:
                    # Fitting the plots now
                    Output_Histos[Name_Out].Fit(Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])], "R")
                
            
                A_Unfold = Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].GetParameter(0)
                B_Unfold = Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].GetParameter(1)
                C_Unfold = Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].GetParameter(2)
                # Re-fitting with the new parameters
                # The constant scaling factor - A
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(0,     abs(A_Unfold))
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
                # Cos(phi) Moment - B
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(1,         B_Unfold)
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(1,         B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
                # Cos(2*phi) Moment - C
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(2,         C_Unfold)
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(2,         C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))
                
                if(extra_function_terms):
                    D_Unfold = Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].GetParameter(3)
                    # E_Unfold = Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].GetParameter(4)
                    # Cos(3*phi) Moment - D
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(3, D_Unfold)
                    Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(3, D_Unfold - 0.5*abs(D_Unfold), D_Unfold + 0.5*abs(D_Unfold))
                    # # Cos(4*phi) Moment - E
                    # Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParameter(4, E_Unfold)
                    # Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].SetParLimits(4, E_Unfold - 0.5*abs(E_Unfold), E_Unfold + 0.5*abs(E_Unfold))
            
                # Re-Fitting the plots
                Output_Histos[Name_Out].Fit(Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])], "RB")
                
                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
#                 Output_Histos[Name_Out].Draw("same HIST text E0")
                Output_Histos[Name_Out].Draw("same HIST E0")
                Unfolded_Fit_Function["".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_"), "_", str(NewDim_Bin)])].Draw("same")
                
                statbox_move(Histogram=Output_Histos[Name_Out], Canvas=Output_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                
            
            Output_Canvas.Modified()
            Output_Canvas.Update()
            
        Save_Name = "".join(["Multi_Dim_Histo_", str(Variable).replace("_smeared", ""), "_", str(Method) if(Method not in ["N/A"]) else "", "_Smeared" if("mear" in Smear) else "", str(File_Save_Format)]).replace(" ", "_")
        Save_Name = str((Save_Name.replace("-", "_")).replace("phi_t_", "phi_h_")).replace("__", "_")
        
        Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
        
        Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
        
        if(((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting in ["default", "Default"])) and (extra_function_terms and "phi_h" in str(Save_Name))):
            Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
        
        if("y" in Binning_Method):
            Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
        if(Sim_Test):
            Save_Name = "".join(["Sim_Test_", Save_Name])
            
        Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
        Save_Name = Save_Name.replace("_.png",                ".png")
        Save_Name = Save_Name.replace("__",                   "_")
            
        if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas"])):
            Output_Canvas.SaveAs(Save_Name)
        print("".join(["Saved: " if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas"])) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
        
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if(Out_Option in ["all", "All", "Canvas", "canvas"]):
                Output_List.append(Output_Canvas)
            return Output_List
        
    
    except:
        print("".join([color.RED, color.BOLD, "MultiD_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

#####################################################################################################################################################################
##==========##==========##     Multidimensional Slice Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################










#####################################################################################################################################################################
##==========##==========##  Multidimensional (Old) Slice Function  ##==========##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################

def MultiD_Canvas_Combine(Histo_rdf="none", Histo_mdf="none", Histo_gdf="none", Histo_bin="none", Histo_bay="none", Name_Combine="none", Variable_Combine="Combined_phi_t_Q2", Smear_Combine=""):
    # print(color.BOLD, "\nRunning MultiD_Canvas_Combine(...) with the following info:", color.END, "\nHisto_rdf =", str(Histo_rdf), "\nHisto_mdf =", str(Histo_mdf), "\nHisto_gdf =", str(Histo_gdf), "\nHisto_bin =", str(Histo_bin), "\nHisto_bay =", str(Histo_bay), "\nName_Combine =", str(Name_Combine), "\nSmear_Combine =", str(Smear_Combine), "\n\n")
    try:
        Histo_rdf_list, Histo_mdf_list, Histo_gdf_list, Histo_bin_list, Histo_bay_list = {}, {}, {}, {}, {}
        Legends_ExREC, Legends_TrueH = {}, {}

        if(str(Histo_rdf) not in ["none"]):
            Histo_rdf_list = MultiD_Slice(Histo=Histo_rdf, Title="norm", Name=Name_Combine, Method="rdf",        Variable=Variable_Combine, Smear="",            Out_Option="Histo", Fitting="Off")[0]
        if(str(Histo_mdf) not in ["none"]):
            Histo_mdf_list = MultiD_Slice(Histo=Histo_mdf, Title="norm", Name=Name_Combine, Method="mdf",        Variable=Variable_Combine, Smear=Smear_Combine, Out_Option="Histo", Fitting="Off")[0]
        if(str(Histo_gdf) not in ["none"]):
            Histo_gdf_list = MultiD_Slice(Histo=Histo_gdf, Title="norm", Name=Name_Combine, Method="gdf",        Variable=Variable_Combine, Smear="",            Out_Option="Histo", Fitting="Off")[0]
        if(str(Histo_bin) not in ["none"]):
            Histo_bin_list = MultiD_Slice(Histo=Histo_bin, Title="norm", Name=Name_Combine, Method="Bin-by-Bin", Variable=Variable_Combine, Smear=Smear_Combine, Out_Option="Histo", Fitting="Off")[0]
        if(str(Histo_bay) not in ["none"]):
            Histo_bay_list = MultiD_Slice(Histo=Histo_bay, Title="norm", Name=Name_Combine, Method="Bayesian",   Variable=Variable_Combine, Smear=Smear_Combine, Out_Option="Histo", Fitting="Off")[0]


        # Name_Combine = Name_Combine.replace("(Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), ", "".join(["(Multi-Dim Histo=Multi_Dim_Var_Info), "]))
        # Name_Combine = Name_Combine.replace("(Binning-Type='2'-[Q2-xB-Bin=All, z-PT-Bin=All]), ", "")
        # Name_Combine = Name_Combine.replace("Binning-Type='2'-", "")
        # Name_Combine = Name_Combine.replace(", (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")
        # Name_Combine = Name_Combine.replace(", (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")

        Name_Combine = Name_Combine.replace("(Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), ", "(Multi-Dim Histo=Multi_Dim_Var_Info), ")
        Name_Combine = Name_Combine.replace("".join(["(Binning-Type='y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), "]), "")
        Name_Combine = Name_Combine.replace("Binning-Type='y_bin'-", "")
        Name_Combine = Name_Combine.replace("".join(["(Binning-Type='", str(Binning_Method).replace("_", ""), "'-[Q2-xB-Bin=All, z-PT-Bin=All]), "]), "")
        Name_Combine = Name_Combine.replace("".join(["Binning-Type='", str(Binning_Method).replace("_", ""), "'-"]), "")
        Name_Combine = Name_Combine.replace("".join([", (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")
        Name_Combine = Name_Combine.replace("".join([", (Var-D2='z_pT_Bin", str(Binning_Method), "_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")

        
                               # ['min',  'max',   'num_bins', 'size']
        Q2_Binning             = [1.4805, 11.8705, 20,         0.5195]
        Q2_xB_Binning          = [0,      8,       8,          1]
        Q2_y_Binning           = [-0.5,   18.5,    19,         1]
 
        phi_h_Binning          = [0,      360,     24,         15]
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            phi_h_Binning      = [0,      360,     12,         30]
            phi_h_Binning      = [0,      360,     10,         36]

        # Combined_phi_h_Q2_Bins = 480

        NewDim_Bin_Max = 8
        Num_Columns_Canvas, Num_Rows_Canvas = 4, 2
        Multi_Dim_Var  = "Q2_xB"
        Multi_Dim_Var  = "Q2_y"
        if(Variable_Combine in ["Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared"]):
            NewDim_Bin_Min  = Q2_Binning[0]
            NewDim_Bin_Max  = Q2_Binning[1]
            NewDim_Bin_Num  = Q2_Binning[2]
            NewDim_Bin_Size = Q2_Binning[3]
            Multi_Dim_Var   = "Q2"
            Num_Columns_Canvas, Num_Rows_Canvas = 4, 5

        if("none" not in [str(Histo_rdf), str(Histo_mdf)]):
            try:
                Output_Canvas_ExREC = Canvas_Create("".join([str(Name_Combine), "_ExREC"]), Num_Columns=Num_Columns_Canvas, Num_Rows=Num_Rows_Canvas, Size_X=2400, Size_Y=1200 if(Num_Rows_Canvas < 3) else 2400, cd_Space=0)
                for cd_ii in range(1, len(Histo_rdf_list), 1):
                    name_rdf = str(Name_Combine.replace("Multi_Dim_Var_Info", "".join(["'rdf'), (", str(Multi_Dim_Var), "_Bin_", str(cd_ii)])))
                    Legends_ExREC[cd_ii] = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                    Legends_ExREC[cd_ii].SetNColumns(1)
                    Legends_ExREC[cd_ii].SetBorderSize(0)
                    Legends_ExREC[cd_ii].SetFillColor(0)
                    Legends_ExREC[cd_ii].SetFillStyle(0)
                    Draw_Canvas(canvas=Output_Canvas_ExREC, cd_num=cd_ii, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    Histo_rdf_list[name_rdf].SetTitle(str(Histo_rdf_list[name_rdf].GetTitle()).replace("".join(["#color[", str(root_color.Blue), "]{ (Experimental)}" if(not Sim_Test) else "]{ (MC REC - Test)}"]), "".join([root_color.Bold, "{ (Reconstructed)}"])))
                    Histo_rdf_list[name_rdf].DrawNormalized("same HIST E0")
                    Legends_ExREC[cd_ii].AddEntry(Histo_rdf_list[name_rdf], "#scale[2]{Experimental}" if(not Sim_Test) else "#scale[2]{MC REC - Test}", "lpE")
                for cd_ii in range(1, len(Histo_mdf_list), 1):
                    name_mdf = str(Name_Combine.replace("Multi_Dim_Var_Info", "".join(["'mdf'), (", str(Multi_Dim_Var), "_Bin_", str(cd_ii)])))
                    Draw_Canvas(canvas=Output_Canvas_ExREC, cd_num=cd_ii, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    Histo_mdf_list[name_mdf].DrawNormalized("same HIST E0")
                    Legends_ExREC[cd_ii].AddEntry(Histo_mdf_list[name_mdf], "#scale[2]{MC REC}", "lpE")
                    Legends_ExREC[cd_ii].Draw("same")
                Save_Name = "".join(["Multi_Dim_Histo_ExREC_", str(Variable_Combine), str(File_Save_Format)]).replace(" ", "_")
                Save_Name = str((Save_Name.replace("-", "_")).replace("phi_t_", "phi_h_")).replace("__", "_")
                Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
                
                Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
                
                # if(extra_function_terms and "phi_h" in str(Save_Name)):
                if(extra_function_terms):
                    Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
                
                if("y" in Binning_Method):
                    Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
                if(Sim_Test):
                    Save_Name = "".join(["Sim_Test_", Save_Name])
                    
                Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
                Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
                Save_Name = Save_Name.replace("_.png",                ".png")
                Save_Name = Save_Name.replace("__",                   "_")
                    
                if(Saving_Q):
                    Output_Canvas_ExREC.SaveAs(Save_Name)
                print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
                    
            except:
                print("".join([color.RED, color.BOLD, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), "\n", color.END]))
                for rdf_ii in Histo_rdf_list:
                    print("".join(["rdf_ii = ", str(rdf_ii)]))
                print("")
                for mdf_ii in Histo_mdf_list:
                    print("".join(["mdf_ii = ", str(mdf_ii)]))
                print("")
                for gdf_ii in Histo_gdf_list:
                    print("".join(["gdf_ii = ", str(gdf_ii)]))
                print("")
                for bay_ii in Histo_bay_list:
                    print("".join(["bay_ii = ", str(bay_ii)]))
                print("")
                for bin_ii in Histo_bin_list:
                    print("".join(["bin_ii = ", str(bin_ii)]))
                return "Error"

        if("none" not in [str(Histo_gdf), str(Histo_bin), str(Histo_bay)]):
            try:
                Output_Canvas_TrueH = Canvas_Create("".join([str(Name_Combine), "_TrueH"]), Num_Columns=Num_Columns_Canvas, Num_Rows=Num_Rows_Canvas, Size_X=2400, Size_Y=1200 if(Num_Rows_Canvas < 3) else 2400, cd_Space=0)
                for cd_ii in range(1, len(Histo_bay_list), 1):
                    name_bay = str(Name_Combine.replace("Multi_Dim_Var_Info", "".join(["'Bayesian'), (", str(Multi_Dim_Var), "_Bin_", str(cd_ii)])))
                    Legends_TrueH[cd_ii] = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                    Legends_TrueH[cd_ii].SetNColumns(1)
                    Legends_TrueH[cd_ii].SetBorderSize(0)
                    Legends_TrueH[cd_ii].SetFillColor(0)
                    Legends_TrueH[cd_ii].SetFillStyle(0)
                    Draw_Canvas(canvas=Output_Canvas_TrueH, cd_num=cd_ii, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    Histo_bay_list[name_bay].SetTitle(str(Histo_bay_list[name_bay].GetTitle()).replace("#color[30]{ (Bayesian Unfolded)}", "".join([root_color.Bold, "{ (Unfolded/True)}"])))
                    Histo_bay_list[name_bay].DrawNormalized("same HIST E0")
                    Legends_TrueH[cd_ii].AddEntry(Histo_bay_list[name_bay], "#scale[2]{Bayesian Unfold}", "lpE")
                for cd_ii in range(1, len(Histo_bin_list), 1):
                    name_bin = str(Name_Combine.replace("Multi_Dim_Var_Info", "".join(["'Bin-by-Bin'), (", str(Multi_Dim_Var), "_Bin_", str(cd_ii)])))
                    Draw_Canvas(canvas=Output_Canvas_TrueH, cd_num=cd_ii, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    Histo_bin_list[name_bin].DrawNormalized("same HIST E0")
                    Legends_TrueH[cd_ii].AddEntry(Histo_bin_list[name_bin], "#scale[2]{Bin-by-Bin}", "lpE")
                for cd_ii in range(1, len(Histo_gdf_list), 1):
                    name_gdf = str(Name_Combine.replace("Multi_Dim_Var_Info", "".join(["'gdf'), (", str(Multi_Dim_Var), "_Bin_", str(cd_ii)])))
                    Draw_Canvas(canvas=Output_Canvas_TrueH, cd_num=cd_ii, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    Histo_gdf_list[name_gdf].DrawNormalized("same HIST E0")
                    Legends_TrueH[cd_ii].AddEntry(Histo_gdf_list[name_gdf], "#scale[2]{MC GEN}", "lpE")
                    Legends_TrueH[cd_ii].Draw("same")


                    
                Save_Name = "".join(["Multi_Dim_Histo_TrueH_", str(Variable_Combine).replace("_smeared", ""), "" if("mear" not in Smear_Combine) else "_smeared", str(File_Save_Format)]).replace(" ", "_")
                Save_Name = str((Save_Name.replace("-", "_")).replace("phi_t_", "phi_h_")).replace("__", "_")
                Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
                
                Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
                
                # if(extra_function_terms and "phi_h" in str(Save_Name)):
                if(extra_function_terms):
                    Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
                
                if("y" in Binning_Method):
                    Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
                if(Sim_Test):
                    Save_Name = "".join(["Sim_Test_", Save_Name])
                    
                Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
                Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
                Save_Name = Save_Name.replace("_.png",                ".png")
                Save_Name = Save_Name.replace("__",                   "_")
                    
                if(Saving_Q):
                    Output_Canvas_TrueH.SaveAs(Save_Name)
                print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
            except:
                print("".join([color.RED, color.BOLD, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), "\n", color.END]))
                for rdf_ii in Histo_rdf_list:
                    print("".join(["rdf_ii = ", str(rdf_ii)]))
                print("")
                for mdf_ii in Histo_mdf_list:
                    print("".join(["mdf_ii = ", str(mdf_ii)]))
                print("")
                for gdf_ii in Histo_gdf_list:
                    print("".join(["gdf_ii = ", str(gdf_ii)]))
                print("")
                for bay_ii in Histo_bay_list:
                    print("".join(["bay_ii = ", str(bay_ii)]))
                print("")
                for bin_ii in Histo_bin_list:
                    print("".join(["bin_ii = ", str(bin_ii)]))
                return "Error"
            
            
    except:
        print("".join([color.RED, color.BOLD, "MultiD_Canvas_Combine(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

#####################################################################################################################################################################
##==========##==========##  Multidimensional (Old) Slice Function  ##==========##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################







































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
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default"):
    if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian", "FIT"]) and (Fitting in ["default", "Default"])):
        if(not extra_function_terms):
            A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
            
        else:
            # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(Histo_To_Fit)
            # fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)) + [E]*cos(4*x*(3.1415926/180)))"
            A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"
            

        Fitting_Function = ROOT.TF1("".join(["Fitting_Function", str(Method).replace(" ", "_")]), str(fit_function), 0, 360)
        Fitting_Function.SetParName(0, "Parameter A")
        Fitting_Function.SetParName(1, "Parameter B")
        Fitting_Function.SetParName(2, "Parameter C")
        if(not extra_function_terms):
            print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]), color.END)
        else:
            # print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold), str(E_Unfold)]), color.END)
            print(color.BOLD, color.BLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold =", color.END, color.BOLD, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold)]), color.END)
            Fitting_Function.SetParName(3, "Parameter D")
            # Fitting_Function.SetParName(4, "Parameter E")

        Fitting_Function.SetRange(0, 360)
        Fitting_Function.SetLineColor(2)
        
        try:
            if("Error" not in [A_Unfold, B_Unfold, C_Unfold] or False):
                # This is the constant scaling factor - A (should basically always be positive)
                Fitting_Function.SetParameter(0,      abs(A_Unfold))
            #     Fitting_Function.SetParLimits(0, 0.95*abs(A_Unfold), 1.05*abs(A_Unfold))
                Fitting_Function.SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
            #     Fitting_Function.SetParLimits(1, B_Unfold - 0.05*abs(B_Unfold), B_Unfold + 0.05*abs(B_Unfold))
                Fitting_Function.SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
            #     Fitting_Function.SetParLimits(2, C_Unfold - 0.05*abs(C_Unfold), C_Unfold + 0.05*abs(C_Unfold))
                Fitting_Function.SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))

                if(extra_function_terms):
                    try:
                        Fitting_Function.SetParameter(3, D_Unfold)
                        Fitting_Function.SetParLimits(3, D_Unfold - 5.5*abs(D_Unfold), D_Unfold + 5.5*abs(D_Unfold))

                        # Fitting_Function.SetParameter(4, E_Unfold)
                        # Fitting_Function.SetParLimits(4, E_Unfold - 5.5*abs(E_Unfold), E_Unfold + 5.5*abs(E_Unfold))
                    except:
                        print("".join([color.RED, color.BOLD, "Fitting_Function ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            # else:
            #     print(color.RED, color.BOLD, "\nFIXING PARAMETERS FOR TESTING\n", color.END)
            #     Fitting_Function= ROOT.TF1("".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_")]), "[A]", 0, 360)
            #     # Fitting_Function.SetRange(0, 360)
            #     # This is the constant scaling factor - A
            #     Fitting_Function.SetParameter(0, 0.50*abs(Histo_To_Fit.GetMaximum))
            #     Fitting_Function.SetParLimits(0, 0.45*abs(Histo_To_Fit.GetMaximum), 0.55*abs(Histo_To_Fit.GetMaximum))

                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "RB")
            else:
                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "R")

            A_Unfold = Fitting_Function.GetParameter(0)
            B_Unfold = Fitting_Function.GetParameter(1)
            C_Unfold = Fitting_Function.GetParameter(2)
            # Re-fitting with the new parameters
            # The constant scaling factor - A
            Fitting_Function.SetParameter(0,     abs(A_Unfold))
            Fitting_Function.SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
            # Cos(phi) Moment - B
            Fitting_Function.SetParameter(1, B_Unfold)
            Fitting_Function.SetParLimits(1, B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
            # Cos(2*phi) Moment - C
            Fitting_Function.SetParameter(2, C_Unfold)
            Fitting_Function.SetParLimits(2, C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))

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
            Histo_To_Fit.Fit(Fitting_Function, "RB")

            A_Unfold       = Fitting_Function.GetParameter(0)
            B_Unfold       = Fitting_Function.GetParameter(1)
            C_Unfold       = Fitting_Function.GetParameter(2)

            A_Unfold_Error = Fitting_Function.GetParError(0)
            B_Unfold_Error = Fitting_Function.GetParError(1)
            C_Unfold_Error = Fitting_Function.GetParError(2)

            Out_Put = [Histo_To_Fit, Fitting_Function, [A_Unfold, A_Unfold_Error], [B_Unfold, B_Unfold_Error], [C_Unfold, C_Unfold_Error]]
        except:
            print("".join([color.RED, color.BOLD, "ERROR IN FITTING:\n", color.END, str(traceback.format_exc()), "\n"]))
            Out_Put = [Histo_To_Fit, "Fitting_Function", ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        
        return Out_Put
    else:
        print("\n\n\nERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...\n\n\n")
        return "ERROR"
    
################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     (New) Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def MultiD_Slice_New(Histo, Title="Default", Name="none", Method="N/A", Variable="Multi_Dim_Q2_y_Bin_phi_t", Smear="", Out_Option="Save", Fitting_Input="default", Q2_y_Bin_Select="All"):
    Unfolded_Fit_Function, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}
    if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
        print(color.BLUE, "\nRunning MultiD_Slice_New(...)\n", color.END)
    else:
        print(color.RED, color.BOLD, "\n\nWrong Smearing option for MultiD_Slice_New(...)\n\n", color.END)
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
                print("ERROR: WRONG TYPE OF HISTOGRAM\nName =", Name)
                print("MultiD_Slice_New() should be used on 1D histograms with the 'Combined_' or 'Multi_Dim_' bin variable\n\n")
                return "Error"
            # if(("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_y_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_phi_t_smeared'" not in str(Name)) and (("'Combined_phi_t_Q2" not in str(Name).replace("_smeared", "") and "'Combined_phi_t_Q2_smeared'" not in str(Name)))):
            #     print("ERROR in MultiD_Slice_New(): Not set up for other variables (yet)")
            #     print("Name =", Name, "\n\n")
            #     return "Error"

        if(Variable not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t_smeared"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t_smeared"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method), "_smeared"]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method), "_smeared"])]):
            print("ERROR in MultiD_Slice_New(): Not set up for other variables (yet)")
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
            Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not Sim_Test) else "]{(MC REC - Test)}"])
            # if(not Sim_Test):
            Variable = Variable.replace("_smeared", "")
            Smear = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
            # if((Sim_Test) and ("_smeared" not in str(Variable)) and (Smear in [""])):
            #     Variable = "".join([str(Variable), "_smeared"])
            #     Smear = "Smear"
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable = Variable.replace("_smeared", "")
            Smear = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[30]{(Bayesian Unfolded)}"])
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

        
        if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"])):
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
        
        # Q2_y_z_pT_4D_Binning   = [-0.5,   566.5,   567,        1]
        # Q2_y_z_pT_4D_Binning   = [-0.5,   512.5,   513,        1]
        Q2_y_z_pT_4D_Binning   = [-0.5,   506.5,   507,        1]

        
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
            
        if(str(Multi_Dim_Var) in ["z_pT"]):
            Name = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(Q2_y_Bin_Select not in [0, "0"]) else "All"))
            
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

                
            #######################################################################
            #####==========#####   Filling Sliced Histogram    #####==========#####
            #######################################################################
            Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
            
            ii_bin_num = 1
            for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
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
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian"]):
                Output_Histos[Name_Out].SetLineColor(30)
                Output_Histos[Name_Out].SetMarkerColor(30)
            #######################################################################
            #####==========#####   Drawing Histogram/Canvas    #####==========#####
            #######################################################################
            
            
            Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
            
            Output_Canvas.Modified()
            Output_Canvas.Update()
            
            
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            if(Fitting_Input in ["default", "Default"]):
                # Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting=Fitting_Input)
                Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out])

                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                # Histo_To_Fit.Draw("same HIST text E0")
                Output_Histos[Name_Out].Draw("same HIST E0")
                Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")].Draw("same")

                statbox_move(Histogram=Output_Histos[Name_Out], Canvas=Output_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
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
        
        if("y" in Binning_Method):
            Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
        if(Sim_Test):
            Save_Name = "".join(["Sim_Test_", Save_Name])
            
            
        Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
        Save_Name = Save_Name.replace("_.png",                ".png")
        Save_Name = Save_Name.replace("__",                   "_")
        # if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas", "complete", "Complete"])):
        if(Saving_Q and ("Acceptance" not in Method)):
            Output_Canvas.SaveAs(Save_Name)
        print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method)) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
        # print("".join(["Saved: " if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas"])) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
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
            if(Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"]):
                Output_List.append(Unfolded_Fit_Function)
            if(Out_Option in ["all", "All", "Pars", "pars"]):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["all", "All", "Canvas", "canvas"]):
                Output_List.append(Output_Canvas)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    
    except:
        print("".join([color.RED, color.BOLD, "MultiD_Slice_New(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##     (New) Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def New_Version_of_File_Creation(Histogram_List_All, Out_Print_Main, Response_2D="", ExREAL_1D="", MC_REC_1D="", MC_GEN_1D="", Smear_Input="", Q2_Y_Bin="All", Z_PT_Bin="All"):
    try:
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################
        if("Response" not in str(Out_Print_Main)):
            print("\nERROR IN New_Version_of_File_Creation()...\nThis function is meant to just handle the 'Response_Matrix' Histograms (for Unfolding)\nFlawed Input was:", str(Out_Print_Main))
            return "Error"
        if(type(Histogram_List_All) is not dict):
            print("\nERROR IN New_Version_of_File_Creation()...\nThis function requires that 'Histogram_List_All' be set as a dict to properly handle the outputs\nFlawed Input was:\nHistogram_List_All =", str(Histogram_List_All))
            return "Error"
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################

        Variable_Input = Histogram_Name_Def(Out_Print_Main, Variable="FindAll")
        # print("Variable_Input =", Variable_Input)

        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        try:
            Bin_Method_Histograms        = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin")
            Bin_Unfolded, Bin_Acceptance = Bin_Method_Histograms
        except:
            print("".join([color.BOLD,     color.RED, "ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

        try:
            RooUnfolded_Bayes_Histos     = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes"))[0]
        except:
            print("".join([color.BOLD,     color.RED, "ERROR IN RooUnfold Bayesian METHOD:\n",               color.END, color.RED, str(traceback.format_exc()), color.END]))

        if("Multi_Dim" not in str(Variable_Input)):
            try:
                RooUnfolded_SVD_Histos   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd"))[0]
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
                Multi_Dim_ExREAL_1D                                                                          = MultiD_Slice_New(Histo=ExREAL_1D,                Title="norm", Name=Out_Print_Main, Method="rdf",        Variable=Variable_Input, Smear=Smear_Input if(Sim_Test) else "", Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_MC_REC_1D                                                                          = MultiD_Slice_New(Histo=MC_REC_1D,                Title="norm", Name=Out_Print_Main, Method="mdf",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function,  GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = MultiD_Slice_New(Histo=MC_GEN_1D,                Title="norm", Name=Out_Print_Main, Method="gdf",        Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
                # Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function,  Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = MultiD_Slice_New(Histo=Bin_Unfolded,             Title="norm", Name=Out_Print_Main, Method="Bin-by-bin", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function,  Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = MultiD_Slice_New(Histo=Bin_Unfolded,             Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                Multi_Dim_Bin_Acceptance                                                                     = MultiD_Slice_New(Histo=Bin_Acceptance,           Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin)[0]
                Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function,  Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = MultiD_Slice_New(Histo=RooUnfolded_Bayes_Histos, Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin)
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========#####      Fitting 1D Histo       #####==========#####
        elif("phi" in Variable_Input):
            MC_GEN_1D,                  Unfolded_GEN_Fit_Function, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=MC_GEN_1D)
            Bin_Unfolded,               Unfolded_Bin_Fit_Function, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Bin_Unfolded)
            RooUnfolded_Bayes_Histos,   Unfolded_Bay_Fit_Function, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_Bayes_Histos)
            if("Multi_Dim" not in str(Variable_Input)):
                RooUnfolded_SVD_Histos, Unfolded_SVD_Fit_Function, SVD_Fit_Par_A, SVD_Fit_Par_B, SVD_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_SVD_Histos)
        #####==========#####      Fitting 1D Histo       #####==========#####


        ##################################################################################
        ###==============###==========================================###==============###
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ###==============###==========================================###==============###
        ##################################################################################
        Histo_Name_General = Histogram_Name_Def(out_print=Out_Print_Main, Histo_General="1D", Data_Type="METHOD", Cut_Type="Skip", Smear_Type=Smear_Input, Q2_y_Bin=Q2_Y_Bin, z_pT_Bin=Z_PT_Bin, Bin_Extra="Default", Variable=Variable_Input)
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "rdf"))]                                  = ExREAL_1D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf"))]                                  = MC_REC_1D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")] = Response_2D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "gdf"))]                                  = MC_GEN_1D

        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin"))]                                  = Bin_Unfolded
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Acceptance"))]                           = Bin_Acceptance
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian"))]                             = RooUnfolded_Bayes_Histos
        if("Multi_Dim" not in str(Variable_Input)):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD"))]                                  = RooUnfolded_SVD_Histos
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Function")]    = Unfolded_SVD_Fit_Function
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_A")]       = SVD_Fit_Par_A
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_B")]       = SVD_Fit_Par_B
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "SVD")).replace("1D", "Fit_Par_C")]       = SVD_Fit_Par_C
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Multi_Dim Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        if(("Multi_Dim" in str(Variable_Input))   and (Z_PT_Bin in ["All", 0])):
            # Only the Multi_Dim z-pT Plots should be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All" or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                try:
                    for histos_list in [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C, Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C, Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C]:
                        try:
                            for name in histos_list:
                                Histogram_List_All[name] = histos_list[name]
                        except:
                            print("".join([color.BOLD, color.RED, "ERROR IN ADDING TO Histogram_List_All (while looping within an item in histos_list):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            print("histos_list =", histos_list)
                except:
                    print("".join([color.BOLD,         color.RED, "ERROR IN ADDING TO Histogram_List_All (while looping through items in histos_list):\n",  color.END, color.RED, str(traceback.format_exc()), color.END]))
        ###==========###         Multi_Dim Histos          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        elif("phi" in Variable_Input):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")] = Unfolded_GEN_Fit_Function
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_A")]    = GEN_Fit_Par_A
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_B")]    = GEN_Fit_Par_B
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_C")]    = GEN_Fit_Par_C

            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bin")).replace("1D",      "Fit_Function")] = Unfolded_Bin_Fit_Function
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bin")).replace("1D",      "Fit_Par_A")]    = Bin_Fit_Par_A
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bin")).replace("1D",      "Fit_Par_B")]    = Bin_Fit_Par_B
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bin")).replace("1D",      "Fit_Par_C")]    = Bin_Fit_Par_C

            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bayesian")).replace("1D", "Fit_Function")] = Unfolded_Bay_Fit_Function
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bayesian")).replace("1D", "Fit_Par_A")]    = Bay_Fit_Par_A
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bayesian")).replace("1D", "Fit_Par_B")]    = Bay_Fit_Par_B
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Bayesian")).replace("1D", "Fit_Par_C")]    = Bay_Fit_Par_C
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
    
################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################










######################################################################################################################################################
##==========##==========## (New) Simple Function for Drawing 2D Histograms  ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################

def Draw_2D_Histograms_Simple_New(Histogram_List_All_Input, Canvas_Input=[], Default_Histo_Name_Input="", Q2_Y_Bin_Input="All", Z_PT_Bin_Input="All"):
    
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(1D)",              "(Normal_2D)")
    Default_Histo_Name_Input = Default_Histo_Name_Input.replace("(Multi-Dim Histo)", "(Normal_2D)")
    
    Variable = "(phi_t)" if("(phi_t)" in Default_Histo_Name_Input) else "(Q2)" if("(Q2)" in Default_Histo_Name_Input) else "(xB)" if("(xB)" in Default_Histo_Name_Input) else "(z)" if("(z)" in Default_Histo_Name_Input) else "(pT)" if("(pT)" in Default_Histo_Name_Input) else "(y)" if("(y)" in Default_Histo_Name_Input) else "(MM)"
    
    Q2_y_Histo_rdf_Initial   = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(Q2)_(y)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    z_pT_Histo_rdf_Initial   = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),       "(z)_(pT)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    Q2_xB_Histo_rdf_Initial  = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),      "(Q2)_(xB)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    
    elth_Histo_rdf_Initial   = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),    "(el)_(elth)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    elPhi_Histo_rdf_Initial  = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),   "(el)_(elPhi)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    
    pipth_Histo_rdf_Initial  = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable),  "(pip)_(pipth)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    pipPhi_Histo_rdf_Initial = Histogram_List_All_Input[str(str(str(Default_Histo_Name_Input.replace(str(Variable), "(pip)_(pipPhi)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    
    # Q2_y_Histo_mdf_Initial   = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),           "(Q2)_(y)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    # Q2_xB_Histo_mdf_Initial  = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),          "(Q2)_(xB)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    # z_pT_Histo_mdf_Initial   = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),           "(z)_(pT)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    
    elth_Histo_mdf_Initial   = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),        "(el)_(elth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    elPhi_Histo_mdf_Initial  = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),       "(el)_(elPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    
    pipth_Histo_mdf_Initial  = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),      "(pip)_(pipth)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    pipPhi_Histo_mdf_Initial = Histogram_List_All_Input[str(str(Default_Histo_Name_Input.replace(str(Variable),     "(pip)_(pipPhi)")).replace("Data_Type", "mdf")).replace("(1D)", "(Normal_2D)")]
    
    Drawing_Histo_Set = {}
    for Drawing_Histo_Found in [Q2_y_Histo_rdf_Initial, Q2_xB_Histo_rdf_Initial, z_pT_Histo_rdf_Initial, elth_Histo_rdf_Initial, elPhi_Histo_rdf_Initial, pipth_Histo_rdf_Initial, pipPhi_Histo_rdf_Initial, elth_Histo_mdf_Initial, elPhi_Histo_mdf_Initial, pipth_Histo_mdf_Initial, pipPhi_Histo_mdf_Initial]:
        #########################################################
        ##===============##     3D Slices     ##===============##
        if("3D" in str(type(Drawing_Histo_Found))):
            bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(Z_PT_Bin_Input not in ["All", 0]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(Z_PT_Bin_Input if(Z_PT_Bin_Input not in ["All", 0]) else Drawing_Histo_Found.GetNbinsX())
            if(Z_PT_Bin_Input not in ["All", 0]):
                Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            New_Name = str(Drawing_Histo_Found.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found.Project3D('yz')
            Drawing_Histo_Set[New_Name].SetName(New_Name)
            Drawing_Histo_Title = (str(Drawing_Histo_Set[New_Name].GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: ", str(Q2_Y_Bin_Input)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_Y_Bin_Input), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin_Input) if(Z_PT_Bin_Input not in ["All", 0]) else "All", "}}}"]))
            Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
            if("mdf" in str(Drawing_Histo_Found.GetName())):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
            Drawing_Histo_Set[New_Name].SetTitle(Drawing_Histo_Title)
        else:
            New_Name = str(Drawing_Histo_Found.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))
            Drawing_Histo_Set[New_Name] = Drawing_Histo_Found
            print("Using Drawing_Histo_Found =", str(Drawing_Histo_Found))
        ##===============##     3D Slices     ##===============##
        #########################################################

        
    Canvas_Input_0, Canvas_Input_1, Canvas_Input_2, Canvas_Input_3 = Canvas_Input
    
    
    ##################################################################
    ##===============##     Drawing Histograms     ##===============##
    Draw_Canvas(canvas=Canvas_Input_1, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(Q2_y_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D"  if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    Drawing_Histo_Set[str(Q2_y_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D"  if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].SetTitle((Drawing_Histo_Set[str(Q2_y_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D"  if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetTitle()).replace("Q^{2}-x_{B} Bin: All" if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_Y_Bin_Input) if(Q2_Y_Bin_Input not in ["All", 0]) else "All", "}"])))
    Q2_y_borders, Q2_y_borders_New = {}, {}
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
    
    Draw_Canvas(canvas=Canvas_Input_1, cd_num=2, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(z_pT_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D"  if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    if(Q2_Y_Bin_Input not in ["All", 0]):
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
        if("y" in str(Binning_Method) and False):
            MM_z_pT_borders = {}
            for MM in [0.94, 1.5, 2.5]:
                # print("".join(["MM_z_pT_Draw(z_val=0.1, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_Y_Bin_Input), ") ="]), MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_Y_Bin_Input))
                # print("".join(["MM_z_pT_Draw(z_val=0.8, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_Y_Bin_Input), ") ="]), MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_Y_Bin_Input))
                MM_z_pT_borders[MM] = ROOT.TLine()
                MM_z_pT_borders[MM].SetLineColor(6 if(MM == 0.94) else 8 if(MM == 1.5) else 46)
                MM_z_pT_borders[MM].SetLineWidth(2)
                MM_z_pT_borders[MM].DrawLine(MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_Y_Bin_Input), 0.1, MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_Y_Bin_Input), 0.8)
    
    
    Draw_Canvas(canvas=Canvas_Input_2, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    Drawing_Histo_Set[str(Q2_xB_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].SetTitle((Drawing_Histo_Set[str(Q2_xB_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetTitle()).replace("Q^{2}-x_{B} Bin: All" if("y_bin" not in str(Binning_Method)) else "Q^{2}-y Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_Y_Bin_Input) if(Q2_Y_Bin_Input not in ["All", 0]) else "All", "}"])))
    Q2_xB_borders, line_num = {}, 0
    for b_lines in Q2_xB_Border_Lines(-1):
        Q2_xB_borders[line_num] = ROOT.TLine()
        Q2_xB_borders[line_num].SetLineColor(1)    
        Q2_xB_borders[line_num].SetLineWidth(2)
        Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
        line_num += 1
    if((Q2_Y_Bin_Input not in ["All", 0]) and ("y_bin" not in str(Binning_Method))):
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
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=1, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=2, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=3, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=4, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipPhi_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=5, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elth_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=6, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(elPhi_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=7, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipth_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    
    Draw_Canvas(canvas=Canvas_Input_3, cd_num=8, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set[str(pipPhi_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].Draw("colz")
    ##===============##     Drawing Histograms     ##===============##
    ##################################################################
    
    Canvas_Input_0.Modified()
    Canvas_Input_0.Update()
    
    palette_move(canvas=Canvas_Input_1, histo=Drawing_Histo_Set[str(Q2_y_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_1, histo=Drawing_Histo_Set[str(z_pT_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_2, histo=Drawing_Histo_Set[str(Q2_xB_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elth_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elPhi_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipth_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipPhi_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elth_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",   "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(elPhi_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipth_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    palette_move(canvas=Canvas_Input_3, histo=Drawing_Histo_Set[str(pipPhi_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    
    Canvas_Input_0.Modified()
    Canvas_Input_0.Update()
    

    Drawing_Histo_Set[str(elth_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetYaxis().SetRangeUser(2, 8)
    Drawing_Histo_Set[str(elPhi_Histo_rdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetYaxis().SetRangeUser(2, 8)
    Drawing_Histo_Set[str(elth_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All",  "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetYaxis().SetRangeUser(2, 8)
    Drawing_Histo_Set[str(elPhi_Histo_mdf_Initial.GetName()).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", "All_1D" if(Z_PT_Bin_Input in ["All", 0]) else str(Z_PT_Bin_Input)]))].GetYaxis().SetRangeUser(2, 8)
    

######################################################################################################################################################
##==========##==========## (New) Simple Function for Drawing 2D Histograms  ##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################





########################################################################################################################################################
##==========##==========## Function for Larger Individual z-pT binned Images  ##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################

def Large_Individual_Bin_Images(Histogram_List_All, Default_Histo_Name, Q2_Y_Bin="All", Z_PT_Bin="All", Multi_Dim_Option="Off"):
    if("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]) not in Default_Histo_Name):
        Default_Histo_Name = Default_Histo_Name.replace("(z_pT_Bin_All)", "".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]))
        
    if(Multi_Dim_Option in ["Only"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
        if(((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) in ["All", "0"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if(Multi_Dim_Option in ["Q2_y"]) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
            
    if((Multi_Dim_Option not in ["Off"]) and (str(Z_PT_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
    
    Large_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS"), Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=2400, cd_Space=0)
    Large_Bin_Canvas_Row_1 = Large_Bin_Canvas.cd(1)
    Large_Bin_Canvas_Row_2 = Large_Bin_Canvas.cd(2)
    Large_Bin_Canvas_Row_3 = Large_Bin_Canvas.cd(3)
    Large_Bin_Canvas_Row_1.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_2.Divide(4, 1, 0, 0)
    Large_Bin_Canvas_Row_3.Divide(4, 2, 0, 0)
    
    ExREAL_1D         = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "rdf")).replace("Smear", "''"))]
    MC_REC_1D         = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "mdf")))]
    MC_GEN_1D         = Histogram_List_All[str(str(Default_Histo_Name.replace("Data_Type", "gdf")).replace("Smear", "''"))]
    
    Default_Response_Matrix_Name = str(str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D",    "Response_Matrix")).replace("Multi-Dim Histo", "Response_Matrix")
    if(Multi_Dim_Option not in ["Off"]):
        Default_Response_Matrix_Name = Default_Response_Matrix_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")
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
    
    Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All"]), "}}}"])
    
    ##################################################################### ################################################################
    #####==========#####     Setting Axis Range      #####==========##### ################################################################
    ##################################################################### ################################################################
    try:
        ExREAL_1D.GetXaxis().SetRange(1,         ExREAL_1D.GetXaxis().GetNbins()         + 1)
        MC_REC_1D.GetXaxis().SetRange(1,         MC_REC_1D.GetXaxis().GetNbins()         + 1)
        MC_GEN_1D.GetXaxis().SetRange(1,         MC_GEN_1D.GetXaxis().GetNbins()         + 1)
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
    UNFOLD_Bin.GetYaxis().SetTitle("Normalized")
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
    UNFOLD_Bay.GetYaxis().SetTitle("Normalized")
    UNFOLD_Bay.SetLineColor(30)
    UNFOLD_Bay.SetLineWidth(2  if("Multi_Dim" not in str(Default_Histo_Name)) else 1)
    UNFOLD_Bay.SetLineStyle(1)
    UNFOLD_Bay.SetMarkerColor(30)
    UNFOLD_Bay.SetMarkerSize(1 if("Multi_Dim" not in str(Default_Histo_Name)) else 0.5)
    UNFOLD_Bay.SetMarkerStyle(21)
    #####==========#####    Unfold SVD Histogram     #####==========##### ################################################################
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD.GetYaxis().SetTitle("Normalized")
        UNFOLD_SVD.SetMarkerColor(root_color.Pink)
        UNFOLD_SVD.SetLineWidth(2)
        UNFOLD_SVD.SetLineStyle(1)
        UNFOLD_SVD.SetLineColor(root_color.Pink)
        UNFOLD_SVD.SetMarkerSize(1)
        UNFOLD_SVD.SetMarkerStyle(21)
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
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=3, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
    if("phi_t" in str(Default_Histo_Name)):
        ExREAL_1D.GetXaxis().SetRangeUser(0, 360)
        MC_REC_1D.GetXaxis().SetRangeUser(0, 360)
        MC_GEN_1D.GetXaxis().SetRangeUser(0, 360)
        
        # ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        ExREAL_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_REC_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        MC_GEN_1D.SetTitle("".join(["#splitline{#scale[1.5]{Pre-", "Multi-Dimensional Unfolded" if(str(Multi_Dim_Option) not in ["Off"]) else "Unfolded", " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
    ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H PL E0 same")
    Legends_REC.AddEntry(ExREAL_1D_Norm, "#scale[2]{Experimental}", "lpE")
    MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H PL E0 same")
    Legends_REC.AddEntry(MC_REC_1D_Norm, "#scale[2]{MC REC}", "lpE")
    MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H PL E0 same")
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
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_1, cd_num=4, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
    if("phi_t" in str(Default_Histo_Name)):
        UNFOLD_Bin.GetXaxis().SetRangeUser(0, 360)
        UNFOLD_Bay.GetXaxis().SetRangeUser(0, 360)
        
        if(Multi_Dim_Option in ["Off"]):
            UNFOLD_SVD.GetXaxis().SetRangeUser(0, 360)
            UNFOLD_SVD.SetTitle("".join(["#splitline{#scale[1.5]{Unfolded Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
        UNFOLD_Bin.SetTitle("".join(["#splitline{#scale[1.5]{", "Unfolded" if(str(Multi_Dim_Option) in ["Off"]) else "".join(["#splitline{Multi-Dimensional Unfolded}{", "Q^{2}-y-#phi_{h} Unfolding" if("(Multi_Dim_Q2_y_Bin_phi_t)" in str(Default_Histo_Name)) else "z-P_{T}-#phi_{h} Unfolding", "}"]), " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        UNFOLD_Bay.SetTitle("".join(["#splitline{#scale[1.5]{", "Unfolded" if(str(Multi_Dim_Option) in ["Off"]) else "".join(["#splitline{Multi-Dimensional Unfolded}{", "Q^{2}-y-#phi_{h} Unfolding" if("(Multi_Dim_Q2_y_Bin_phi_t)" in str(Default_Histo_Name)) else "z-P_{T}-#phi_{h} Unfolding", "}"]), " Distributions of #phi_{h}}}{#scale[1.15]{", str(Bin_Title), "}}"]))
        
    else:
        UNFOLD_SVD.SetTitle(str(UNFOLD_SVD.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        UNFOLD_SVD.SetTitle(str(UNFOLD_SVD.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
        UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        UNFOLD_Bin.SetTitle(str(UNFOLD_Bin.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
        UNFOLD_Bay.SetTitle(str(UNFOLD_Bay.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
        
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD_Norm =  UNFOLD_SVD.DrawNormalized("H PL E0 same")
        statbox_move(Histogram=UNFOLD_SVD_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
        for ii in range(0, UNFOLD_SVD.GetNbinsX() + 1, 1):
            if(UNFOLD_SVD_Norm.GetBinError(ii) > 0.01):
                print("".join([color.RED, "\n(SVD Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                UNFOLD_SVD_Norm.SetBinContent(ii, 0)
                UNFOLD_SVD_Norm.SetBinError(ii,   0)
        Legends_Unfolded.AddEntry(UNFOLD_SVD_Norm, "#scale[2]{SVD Unfolded}", "lpE")

    UNFOLD_Bin_Norm =  UNFOLD_Bin.DrawNormalized("H PL E0 same")
    statbox_move(Histogram=UNFOLD_Bin_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    for ii in range(0, UNFOLD_Bin_Norm.GetNbinsX() + 1, 1):
        if(UNFOLD_Bin_Norm.GetBinError(ii) > 0.01):
            print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
            UNFOLD_Bin_Norm.SetBinContent(ii,  0)
            UNFOLD_Bin_Norm.SetBinError(ii,    0)
    Legends_Unfolded.AddEntry(UNFOLD_Bin_Norm, "#scale[2]{Bin-by-Bin}", "lpE")

    UNFOLD_Bay_Norm =  UNFOLD_Bay.DrawNormalized("H PL E0 same")
    statbox_move(Histogram=UNFOLD_Bay_Norm, Canvas=Large_Bin_Canvas_Row_1.cd(4), Print_Method="off")
    for ii in range(0, UNFOLD_Bay_Norm.GetNbinsX() + 1, 1):
        if(UNFOLD_Bay_Norm.GetBinError(ii) > 0.01):
            print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
            UNFOLD_Bay_Norm.SetBinContent(ii, 0)
            UNFOLD_Bay_Norm.SetBinError(ii,   0)
    Legends_Unfolded.AddEntry(UNFOLD_Bay_Norm, "#scale[2]{Bayesian}", "lpE")
    
    
    # if(Multi_Dim_Option in ["Off"]):
    #     Max_Unfolded = max([UNFOLD_SVD_Norm.GetMaximum, UNFOLD_Bin_Norm.GetMaximum, UNFOLD_Bay_Norm.GetMaximum])
    # else:
    Max_Unfolded = max([UNFOLD_Bin_Norm.GetBinContent(UNFOLD_Bin_Norm.GetMaximumBin()), UNFOLD_Bay_Norm.GetBinContent(UNFOLD_Bay_Norm.GetMaximumBin())])
    
    # UNFOLD_SVD_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0, 0.11)
    if(Multi_Dim_Option in ["Off"]):
        UNFOLD_SVD_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Unfolded)
    UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0,     1.2*Max_Unfolded)
    
    Legends_Unfolded.Draw("same")
    ##=====##=====##     Drawing the Unfolded Histograms      ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 3     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=3, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
    ROOT.gPad.SetLogz(1)
    Response_2D.Draw("colz")
    if(Multi_Dim_Option in ["Off"]):
        Response_2D.GetXaxis().SetRangeUser(0, 360)
        Response_2D.GetYaxis().SetRangeUser(0, 360)
        
    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("z_pT_Bin_y_bin_phi_t",                       "z-P_{T}-#phi_{h} Bins"))
    Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h} Bins"))
    Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("z_pT_Bin_y_bin_phi_t", "z-P_{T}-#phi_{h} Bins"))
    
    Large_Bin_Canvas.Modified()
    Large_Bin_Canvas.Update()
    palette_move(canvas=Large_Bin_Canvas, histo=Response_2D, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    ##=====##=====##       Drawing the Response Matrix        ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ##==========##==========##     Row 2 - CD 4     ##==========##==========## ################################################################
    ########################################################################## ################################################################
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    Draw_Canvas(canvas=Large_Bin_Canvas_Row_2, cd_num=4, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
    UNFOLD_Acceptance.SetTitle(str(UNFOLD_Acceptance.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
    UNFOLD_Acceptance.GetXaxis().SetRangeUser(0, 360)
    UNFOLD_Acceptance.Draw("same E1 H")
    ##=====##=====##      Drawing the Bin Acceptance          ##=====##=====## ################################################################
    ########################################################################## ################################################################
    ########################################################################## ###################################################################################################################################################################################################################################################################################################
    ##=====##=====##      Drawing the Extra 2D Histos         ##=====##=====## ###################################################################################################################################################################################################################################################################################################
    Draw_2D_Histograms_Simple_New(Histogram_List_All_Input=Histogram_List_All, Canvas_Input=[Large_Bin_Canvas, Large_Bin_Canvas_Row_1, Large_Bin_Canvas_Row_2, Large_Bin_Canvas_Row_3], Default_Histo_Name_Input=str(str(Default_Histo_Name.replace("".join(["(z_pT_Bin_", str(Z_PT_Bin), ")"]), "(z_pT_Bin_All)")).replace("(Multi_Dim_Q2_y_Bin_phi_t)", "(phi_t)")).replace("(Multi_Dim_z_pT_Bin_y_bin_phi_t)", "(phi_t)"), Q2_Y_Bin_Input=Q2_Y_Bin, Z_PT_Bin_Input=Z_PT_Bin)
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
        Save_Name = "".join(["Response_Matrix_Normal_Q2_y_Bin_", str(Q2_Y_Bin), "_z_pT_Bin_", str(Z_PT_Bin), "_Smeared.png" if("Smear" in Default_Histo_Name) else ".png"])    
    else:
        Save_Name = str("".join([str(Default_Histo_Name), ".png"]).replace("(", "")).replace(")", "")
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
    if("y" in Binning_Method):
        Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
    if(Multi_Dim_Option not in ["Off"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = "".join(["Sim_Test_", Save_Name])
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
    Save_Name = Save_Name.replace("_.png",                ".png")
    Save_Name = Save_Name.replace("__",                   "_")
    if(Saving_Q):
        Large_Bin_Canvas.SaveAs(Save_Name)
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################
    #####==========#####        Saving Canvas        #####==========##### ################################################################
    ##################################################################### ################################################################

    
    
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
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if((str(Q2_Y_Bin) in ["All", "0"]) or (str(Z_PT_Bin) in ["All", "0"])) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
        if((str(Q2_Y_Bin) not in ["All", "0"]) and (str(Z_PT_Bin) not in ["All", "0"])):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
            
    if(Multi_Dim_Option in ["Q2_y", "z_pT"]):
        Default_Histo_Name = Default_Histo_Name.replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)" if(Multi_Dim_Option in ["Q2_y"]) else "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")
        if((str(Z_PT_Bin) not in ["All", "0"]) or ((str(Q2_Y_Bin) not in ["All", "0"]) and (Multi_Dim_Option in ["Q2_y"]))):
            Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")

    if(("(1D)" in Default_Histo_Name) and ("(Multi_Dim_Q2_y_Bin_phi_t)" in Default_Histo_Name) and (str(Q2_Y_Bin) not in ["All", "0"])):
        Default_Histo_Name = Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")
        
    fit_function_title     = "Fit Function = A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
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
        
    Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All", "}"]), "}}"])
    
    Small_Bin_Canvas       = Canvas_Create(Name=Default_Histo_Name.replace("Data_Type", "CANVAS_Unfolded"), Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1100, cd_Space=0)
    Small_Bin_Canvas_Row_1 = Small_Bin_Canvas.cd(1)
    Small_Bin_Canvas_Row_2 = Small_Bin_Canvas.cd(2)
    # Small_Bin_Canvas_Row_1.Divide(2 if(Multi_Dim_Option in ["Off"]) else 1, 1, 0)
    Small_Bin_Canvas_Row_1.Divide(2, 1, 0)
    Small_Bin_Canvas_Row_2.Divide(2, 1, 0)
    
    ExREAL_1D  = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "rdf")).replace("Smear", "''")]
    MC_REC_1D  = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "mdf"))]
    MC_GEN_1D  = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type",     "gdf")).replace("Smear", "''")]
    
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
        ExREAL_1D.GetXaxis().SetRange(1,  ExREAL_1D.GetXaxis().GetNbins()  + 1)
        MC_REC_1D.GetXaxis().SetRange(1,  MC_REC_1D.GetXaxis().GetNbins()  + 1)
        MC_GEN_1D.GetXaxis().SetRange(1,  MC_GEN_1D.GetXaxis().GetNbins()  + 1)
        
        UNFOLD_Bin.GetXaxis().SetRange(1, UNFOLD_Bin.GetXaxis().GetNbins() + 1)
        UNFOLD_Bay.GetXaxis().SetRange(1, UNFOLD_Bay.GetXaxis().GetNbins() + 1)
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
    #####==========#####    Unfold Bin Histogram     #####==========##### ################################################################ ################################################################ ################################################################
    UNFOLD_Bin.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Brown), "]{Bin-By-Bin} Distribution of #phi_{h}}}{",         root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
    UNFOLD_Bin.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
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
    UNFOLD_Bay.SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(30),               "]{RooUnfold Bayesian} Distribution of #phi_{h}}}{", root_color.Bold, "{", str(fit_function_title), "}}}{", str(Bin_Title), "}"]))
    UNFOLD_Bay.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
    UNFOLD_Bay.SetLineColor(30)
    UNFOLD_Bay.SetLineWidth(2)
    UNFOLD_Bay.SetLineStyle(1)
    UNFOLD_Bay.SetMarkerColor(30)
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
        UNFOLD_SVD.GetXaxis().SetTitle("".join(["#phi_{h}" if("Smear" in str(Default_Histo_Name)) else "#phi_{h} (Smeared)"]))
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
    ExREAL_1D_Norm = ExREAL_1D.DrawNormalized("H PL E0 same")
    MC_REC_1D_Norm = MC_REC_1D.DrawNormalized("H PL E0 same")
    MC_GEN_1D_Norm = MC_GEN_1D.DrawNormalized("H PL E0 same")
    try:
        statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=Small_Bin_Canvas_Row_1.cd(1), Print_Method="off")
    except:
        print("\nMC_GEN_1D IS NOT FITTED\n")
        
    Max_Pre_Unfolded = max([ExREAL_1D_Norm.GetBinContent(ExREAL_1D_Norm.GetMaximumBin()), MC_REC_1D_Norm.GetBinContent(MC_REC_1D_Norm.GetMaximumBin()), MC_GEN_1D_Norm.GetBinContent(MC_GEN_1D_Norm.GetMaximumBin())])
    
    # ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    # MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 0.11)
    ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_REC_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    MC_GEN_1D_Norm.GetYaxis().SetRangeUser(0, 1.2*Max_Pre_Unfolded)
    
    Legends_REC.AddEntry(ExREAL_1D_Norm, "#scale[2]{Experimental}", "lpE")
    Legends_REC.AddEntry(MC_REC_1D_Norm, "#scale[2]{MC REC}",       "lpE")
    Legends_REC.AddEntry(MC_GEN_1D_Norm, "#scale[2]{MC GEN}",       "lpE")
    Legends_REC.Draw("same")
    ##=====##=====##   Drawing the Pre-Unfolded Histograms    ##=====##=====## ###################################################################
    ########################################################################## ###################################################################
    ##==========##==========##     Row 2 - CD 1     ##==========##==========## ###################################################################
    ########################################################################## ###################################################################
    ##=====##=====##     Drawing the Bayesian Histograms      ##=====##=====## ###################################################################
    Draw_Canvas(Small_Bin_Canvas_Row_2, 1, 0.15)
    if(DRAW_NORMALIZE):
        UNFOLD_Bay_Norm = UNFOLD_Bay.DrawNormalized("H PL E0 same")
        UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bay_Norm.GetBinContent(UNFOLD_Bay_Norm.GetMaximumBin())))
        
        for ii in range(0, UNFOLD_Bay_Norm.GetNbinsX() + 1, 1):
            if(UNFOLD_Bay_Norm.GetBinError(ii) > 0.01):
                print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                UNFOLD_Bay_Norm.SetBinContent(ii, 0)
                UNFOLD_Bay_Norm.SetBinError(ii,   0)
        # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
        UNFOLD_Bay_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bay_Norm)
        UNFOLD_Bay_Fitted[1].Draw("H PL E0 same")
        statbox_move(Histogram=UNFOLD_Bay_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # else:
        #     UNFOLD_Bay_Multi_Dim.DrawNormalized("H PL E0 same")
        #     maximum = max([UNFOLD_Bay_Norm.GetMaximum, UNFOLD_Bay_Multi_Dim.GetMaximum])
        #     UNFOLD_Bay_Norm.GetYaxis().SetRangeUser(0,      1.2*maximum)
        #     UNFOLD_Bay_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
            
    else:
        UNFOLD_Bay.Draw("H PL E0 same")
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
            UNFOLD_SVD_Norm = UNFOLD_SVD.DrawNormalized("H PL E0 same")
            UNFOLD_SVD_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_SVD_Norm.GetBinContent(UNFOLD_SVD_Norm.GetMaximumBin())))
            for ii in range(0, UNFOLD_SVD_Norm.GetNbinsX() + 1, 1):
                if(UNFOLD_SVD_Norm.GetBinError(ii) > 0.01):
                    print("".join([color.RED, "\n(SVD Unfolded) Bin ",        str(ii), " has a large error (after normalizing)...", color.END]))
                    UNFOLD_SVD_Norm.SetBinContent(ii, 0)
                    UNFOLD_SVD_Norm.SetBinError(ii,   0)
            UNFOLD_SVD_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_SVD_Norm)
            UNFOLD_SVD_Fitted[1].Draw("H PL E0 same")
            statbox_move(Histogram=UNFOLD_SVD_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        else:
            UNFOLD_SVD.Draw("H PL E0 same")
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
        UNFOLD_Bin_Norm = UNFOLD_Bin.DrawNormalized("H PL E0 same")
        UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bin_Norm.GetBinContent(UNFOLD_Bin_Norm.GetMaximumBin())))
        for ii in range(0, UNFOLD_Bin_Norm.GetNbinsX() + 1, 1):
            if(UNFOLD_Bin_Norm.GetBinError(ii) > 0.01):
                print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                UNFOLD_Bin_Norm.SetBinContent(ii,  0)
                UNFOLD_Bin_Norm.SetBinError(ii,    0)
        # if(Multi_Dim_Option in ["Off", "Fitted", "Only"]):
        UNFOLD_Bin_Fitted = Fitting_Phi_Function(Histo_To_Fit=UNFOLD_Bin_Norm)
        UNFOLD_Bin_Fitted[1].Draw("H PL E0 same")
        statbox_move(Histogram=UNFOLD_Bin_Fitted[0], Canvas=Small_Bin_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
        # else:
        #     UNFOLD_Bin_Multi_Dim.DrawNormalized("H PL E0 same")
        #     maximum = max([UNFOLD_Bin_Norm.GetMaximum, UNFOLD_Bin_Multi_Dim.GetMaximum])
        #     UNFOLD_Bin_Norm.GetYaxis().SetRangeUser(0,      1.2*maximum)
        #     UNFOLD_Bin_Multi_Dim.GetYaxis().SetRangeUser(0, 1.2*maximum)
    else:
        UNFOLD_Bin.Draw("H PL E0 same")
        UNFOLD_Bin.GetYaxis().SetRangeUser(0, 1.2*(UNFOLD_Bin.GetBinContent(UNFOLD_Bin.GetMaximumBin())))
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
        Save_Name = "".join(["Response_Matrix_Normal_Q2_xB_Bin_", str(Q2_Y_Bin) if(str(Q2_Y_Bin) not in ["0"]) else "All", "_z_pT_Bin_", str(Z_PT_Bin) if(str(Z_PT_Bin) not in ["0"]) else "All", "_Unfolded_Histos_Smeared.png" if("Smear" in Default_Histo_Name) else "_Unfolded_Histos.png"])    
    else:
        Save_Name = str("".join([str(Default_Histo_Name), "_Unfolded_Histos.png"]).replace("(", "")).replace(")", "")
    Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
    if("y" in Binning_Method):
        Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
    if(Multi_Dim_Option not in ["Off"]):
        Save_Name = "".join(["Multi_Unfold_", str(Multi_Dim_Option), "_", str(Save_Name)])
    if(Sim_Test):
        Save_Name = "".join(["Sim_Test_",  str(Save_Name)])
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
    Save_Name = Save_Name.replace("_.png",                ".png")
    Save_Name = Save_Name.replace("__",                   "_")
    if(Saving_Q):
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

def z_pT_Images_Together(Histogram_List_All, Default_Histo_Name, Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z"):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    All_z_pT_Canvas = Canvas_Create(Name=Default_Histo_Name.replace("1D", "".join(["CANVAS_", str(Plot_Orientation)]) if(Multi_Dim_Option in ["Off"]) else "".join(["CANVAS_", str(Plot_Orientation), "_", str(Multi_Dim_Option)])), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
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
    number_of_rows, number_of_cols     = z_pT_Border_Lines(Q2_Y_Bin)[0][1]-1, z_pT_Border_Lines(Q2_Y_Bin)[1][1]-1
    if(Plot_Orientation in ["z_pT"]):
        number_of_rows, number_of_cols = z_pT_Border_Lines(Q2_Y_Bin)[1][1]-1, z_pT_Border_Lines(Q2_Y_Bin)[0][1]-1
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
    Q2_y_Histo_rdf_Initial = Histogram_List_All[str(str(str(Default_Histo_Name.replace("(phi_t)", "(Q2)_(y)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    z_pT_Histo_rdf_Initial = Histogram_List_All[str(str(str(Default_Histo_Name.replace("(phi_t)", "(z)_(pT)")).replace("Smear", "''")).replace("Data_Type", "rdf")).replace("(1D)", "(Normal_2D)")]
    Drawing_Histo_Set = {}
    ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    if("3D" in str(type(Q2_y_Histo_rdf_Initial))):
        bin_Histo_2D_0, bin_Histo_2D_1 = Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(0), Q2_y_Histo_rdf_Initial.GetXaxis().FindBin(Q2_y_Histo_rdf_Initial.GetNbinsX())
        Q2_y_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
        Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial.Project3D('yz')
        Drawing_Histo_Set[Q2_y_Name].SetName(Q2_y_Name)
        Drawing_Histo_Title = (str(Drawing_Histo_Set[Q2_y_Name].GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
        Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
        if("mdf" in str(Q2_y_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
        Drawing_Histo_Set[Q2_y_Name].SetTitle(Drawing_Histo_Title)
    else:
        Q2_y_Name = str(Q2_y_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[Q2_y_Name] = Q2_y_Histo_rdf_Initial
        print("Using Q2_y_Histo_rdf_Initial =", str(Q2_y_Histo_rdf_Initial))
        
    if("3D" in str(type(z_pT_Histo_rdf_Initial))):
        bin_Histo_2D_0, bin_Histo_2D_1 = z_pT_Histo_rdf_Initial.GetXaxis().FindBin(0), z_pT_Histo_rdf_Initial.GetXaxis().FindBin(z_pT_Histo_rdf_Initial.GetNbinsX())
        z_pT_Histo_rdf_Initial.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
        z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial.Project3D('yz'                        if(Plot_Orientation in ["z_pT"]) else 'zy')
        Drawing_Histo_Set[z_pT_Name].SetName(z_pT_Name)
        Drawing_Histo_Title = (str(Drawing_Histo_Set[z_pT_Name].GetTitle()).replace("yz projection" if(Plot_Orientation in ["z_pT"]) else "zy projection", "")).replace("".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All}}}"]))
        Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
        if("mdf" in str(z_pT_Histo_rdf_Initial.GetName())):
            Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
        Drawing_Histo_Set[z_pT_Name].SetTitle(Drawing_Histo_Title)
    else:
        z_pT_Name = str(z_pT_Histo_rdf_Initial.GetName())
        Drawing_Histo_Set[z_pT_Name] = z_pT_Histo_rdf_Initial
        print("Using z_pT_Histo_rdf_Initial =", str(z_pT_Histo_rdf_Initial))
    ##===============##     3D Slices     ##===============## ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ######################################################### ############ ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
        
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 1, 0.15)
    Drawing_Histo_Set[Q2_y_Name].Draw("colz")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(1), histo=Drawing_Histo_Set[Q2_y_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    Q2_y_borders, Q2_y_borders_New = {}, {}
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
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 2, 0.15)
    Drawing_Histo_Set[z_pT_Name].Draw("colz")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(2), histo=Drawing_Histo_Set[z_pT_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    if(Plot_Orientation in ["pT_z"]):
        if(str(Q2_Y_Bin) not in ["0", "All"]):
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
        if("y" in str(Binning_Method) and False):
            MM_z_pT_borders = {}
            for MM in [0.94, 1.5, 2.5]:
                # print("".join(["MM_z_pT_Draw(z_val=0.1, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_Y_Bin), ") ="]), MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_Y_Bin))
                # print("".join(["MM_z_pT_Draw(z_val=0.8, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_Y_Bin), ") ="]), MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_Y_Bin))
                MM_z_pT_borders[MM] = ROOT.TLine()
                MM_z_pT_borders[MM].SetLineColor(6 if(MM == 0.94) else 8 if(MM == 1.5) else 46)
                MM_z_pT_borders[MM].SetLineWidth(2)
                MM_z_pT_borders[MM].DrawLine(0.1, MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_Y_Bin), 0.8, MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_Y_Bin))
    else:
        if(str(Q2_Y_Bin) not in ["All", "0"]):
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
            if("y" in str(Binning_Method) and False):
                MM_z_pT_borders = {}
                for MM in [0.94, 1.5, 2.5]:
                    MM_z_pT_borders[MM] = ROOT.TLine()
                    MM_z_pT_borders[MM].SetLineColor(6 if(MM == 0.94) else 8 if(MM == 1.5) else 46)
                    MM_z_pT_borders[MM].SetLineWidth(2)
                    MM_z_pT_borders[MM].DrawLine(MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_Y_Bin), 0.1, MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_Y_Bin), 0.8)
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    ####  Upper Left - i.e., 2D Histograms  ############################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    Bin_Title_All_z_pT_Bins = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: All"]), "}}}"])
    
    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower, 1, 0.15)        
    if("Response" in str(Method)):
        try:
            Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].SetTitle(str(Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].Draw("col")
        except Exception as e:
            print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n",              color.END, color.RED, str(traceback.format_exc()), color.END]))
    elif("Data"   in str(Method)):
        try:
            if(Multi_Dim_Option in ["Off"]):
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
            else:
                Default_Histo_Name_Multi_Dim = str(Default_Histo_Name.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
                # Currently built so that the integrated z-pT bin for multidimensional unfolding uses the combined Q2-y-phi variable (whereas the unfolding done for the individual z-pT bins will unfold the z-pT-phi variable instead)
                    # This note is to explain that the Multi-Dim version of this image will show 2 different types of multidimensional unfolding
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_Multi_Dim.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
            
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
            

            try:
                statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
            except:
                print("\nMC_GEN_1D IS NOT FITTED\n")
            
        except Exception as e:
            print("".join([color.BOLD, color.RED, "ERROR IN 1D (Input) Histograms:\n",        color.END, color.RED, str(traceback.format_exc()), color.END]))
    else:
        

        Default_Histo_Name_Any     = str(Default_Histo_Name)
        if(Multi_Dim_Option not in ["Off"]):
            Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("(1D)", "(Multi-Dim Histo)")).replace("(phi_t)", "(Multi_Dim_Q2_y_Bin_phi_t)")
        if(str(Method) in ["rdf", "gdf"]):
            Default_Histo_Name_Any = str(Default_Histo_Name_Any.replace("Smear", "''"))
        ##################################################################### ################################################################
        #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
        ##################################################################### ################################################################
        #####==========#####   Experimental Histogram    #####==========##### ################################################################
        if(str(Method) in ["rdf"]):
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineColor(root_color.Blue)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerColor(root_color.Blue)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerSize(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method)).replace("Smear", "''")].SetMarkerStyle(21)
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
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineColor(30)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineWidth(2)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetLineStyle(1)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetMarkerColor(30)
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
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].Draw("H PL E0 same")

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetTitle("#phi_{h}" if("Smear" not in str(Default_Histo_Name)) else "#phi_{h} (Smeared)")

            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
            Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_Any.replace("Data_Type", Method))].GetMaximumBin())))
            
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
    z_pT_Bin_Range = 42 if(str(Q2_Y_Bin) in ["2"]) else 36 if(str(Q2_Y_Bin) in ["4", "5", "9", "10"]) else 35 if(str(Q2_Y_Bin) in ["1", "3"]) else 30 if(str(Q2_Y_Bin) in ["6", "7", "8", "11"]) else 25 if(str(Q2_Y_Bin) in ["13", "14"]) else 20 if(str(Q2_Y_Bin) in ["12", "15", "16", "17"]) else 1
    for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
        
        if(((Q2_Y_Bin in [1]) and (z_pT_Bin in [28, 34, 35])) or ((Q2_Y_Bin in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or (Q2_Y_Bin in [3] and z_pT_Bin in [28, 35]) or (Q2_Y_Bin in [4] and z_pT_Bin in [6, 36]) or (Q2_Y_Bin in [5] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [6] and z_pT_Bin in [30]) or (Q2_Y_Bin in [7] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [9] and z_pT_Bin in [36]) or (Q2_Y_Bin in [10] and z_pT_Bin in [30, 36]) or (Q2_Y_Bin in [11] and z_pT_Bin in [24, 30]) or (Q2_Y_Bin in [13, 14] and z_pT_Bin in [25]) or (Q2_Y_Bin in [15, 16, 17] and z_pT_Bin in [20])):
            continue
        
        
        Bin_Title_z_pT_Bin              = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(str(z_pT_Bin) not in ["0"]) else "All"]), "}}}"])
        Default_Histo_Name_z_pT_Bin     = str(Default_Histo_Name.replace("z_pT_Bin_All",     "".join(["z_pT_Bin_", str(z_pT_Bin)])))
        if((Multi_Dim_Option not in ["Off"]) and ("Response" not in str(Method))):
            Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("(phi_t)", "(Multi_Dim_z_pT_Bin_y_bin_phi_t)")).replace("(1D)", "(Multi-Dim Histo)")
        if(str(Method) in ["rdf", "gdf"]):
            Default_Histo_Name_z_pT_Bin = str(Default_Histo_Name_z_pT_Bin.replace("Smear", "''"))
            
        if(Plot_Orientation in ["z_pT"]):
            All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(z_pT_Bin)
            All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
        else:
            cd_row = int(z_pT_Bin/number_of_cols) + 1
            if(0 == (z_pT_Bin%number_of_cols)):
                cd_row += -1
            cd_col = z_pT_Bin - ((cd_row - 1)*number_of_cols)
            
            All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
            All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)

            All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)

        Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)

        if("Data"       in str(Method)):
            try:
                ExREAL_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "rdf")].DrawNormalized("H PL E0 same")
                MC_REC_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf"))].DrawNormalized("H PL E0 same")
                MC_GEN_1D_Norm = Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Smear",     "''")).replace("Data_Type", "gdf")].DrawNormalized("H PL E0 same")
                
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

                try:
                    statbox_move(Histogram=MC_GEN_1D_Norm, Canvas=All_z_pT_Canvas_cd_1_Lower.cd(1), Print_Method="off")
                except:
                    print("\nMC_GEN_1D IS NOT FITTED\n")
                
            except Exception as e:
                print("".join([color.BOLD, color.RED, "ERROR IN (z-pT Bin", str(z_pT_Bin), ") 1D (Input) Histograms:\n",        color.END, color.RED, str(traceback.format_exc()), color.END]))
        elif("Response" in str(Method)):
            try:
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", "mdf")).replace("1D", "Response_Matrix")].Draw("col")
            except Exception as e:
                print("".join([color.BOLD, color.RED, "ERROR IN (z-pT Bin", str(z_pT_Bin), ") Response Matrix:\n",              color.END, color.RED, str(traceback.format_exc()), color.END]))
        else:
            
            ##################################################################### ################################################################
            #####==========#####  Setting Histogram Colors   #####==========##### ################################################################
            ##################################################################### ################################################################
            #####==========#####   Experimental Histogram    #####==========##### ################################################################
            if(str(Method) in ["rdf"]):
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
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineColor(30)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineWidth(2)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetLineStyle(1)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetMarkerColor(30)
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
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].SetTitle(str(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].Draw("H PL E0 same")
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetXaxis().SetRangeUser(0, 360)
                Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetYaxis().SetRangeUser(0, 1.2*(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetBinContent(Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))].GetMaximumBin())))
                
                if(Method not in ["rdf", "mdf"]):
                    try:
                        statbox_move(Histogram=Histogram_List_All[str(Default_Histo_Name_z_pT_Bin.replace("Data_Type", Method))], Canvas=All_z_pT_Canvas_cd_2_z_pT_Bin.cd(1), Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    except:
                        print("\nTHE SELECTED HISTOGRAM WAS NOT FITTED\n")
                        
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
        
    Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
    Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
    Save_Name = Save_Name.replace("_.png",                ".png")
    Save_Name = Save_Name.replace("__",                   "_")
    if(Saving_Q):
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
Common_Name = "Unfolding_Tests_V13_All"
Common_Name = "Analysis_Note_Update_V4_All"
Common_Name = "Multi_Dimension_Unfold_V1_All"
# Common_Name = "Multi_Dimension_Unfold_V2_All"
Common_Name = "Multi_Dimension_Unfold_V3_All"
Common_Name = "Analysis_Note_Update_VF_APS_All"

Common_Name = "New_Binning_Schemes_V8_All"

Common_Name = "Gen_Cuts_V1_All"
Common_Name = "Gen_Cuts_V6_All"
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
###############################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################


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
    Conditions_For_Unfolding.append("Response_Matrix_Normal"        in str(out_print_main))
    Conditions_For_Unfolding.append("Response_Matrix_Normal_1D" not in str(out_print_main))
    
    ## Correct Cuts:
    Conditions_For_Unfolding.append("no_cut"                    not in str(out_print_main))
    Conditions_For_Unfolding.append("cut_Complete_EDIS"         not in str(out_print_main))
    

    ## Correct Variable(s):
    # Conditions_For_Unfolding.append("phi_t" in str(out_print_main))
    # Conditions_For_Unfolding.append("'phi_t" not in str(out_print_main))
    # Conditions_For_Unfolding.append("'Combined_Q2_xB_Bin_2_" not in str(out_print_main))
#     Conditions_For_Unfolding.append("'Combined_" in str(out_print_main))
    Conditions_For_Unfolding.append("phi_t"          in str(out_print_main))
#     Conditions_For_Unfolding.append("Multi_Dim_" not in str(out_print_main))
#     Conditions_For_Unfolding.append("Multi_Dim_"     in str(out_print_main))
#     Conditions_For_Unfolding.append("MM"     in str(out_print_main))
    Conditions_For_Unfolding.append("Multi_Dim_Q2_phi_t"               not in str(out_print_main))
    Conditions_For_Unfolding.append("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(out_print_main))

    
    ## Correct Binning:
    # Conditions_For_Unfolding.append("Q2-xB-Bin=1" in str(out_print_main))
    # Conditions_For_Unfolding.append("Q2-xB-Bin=All" not in str(out_print_main))
    
    # Smearing Options:
    # if((Smearing_Options not in ["no_smear", "both"]) or  (Sim_Test)):
    if((Smearing_Options not in ["no_smear", "both"])):
        Conditions_For_Unfolding.append("(Smear-Type='')" not in str(out_print_main))
    # if((Smearing_Options not in ["smear",    "both"]) and (not Sim_Test)):
    if((Smearing_Options not in ["smear",    "both"])):
        Conditions_For_Unfolding.append("(Smear-Type='')"     in str(out_print_main))
    
    ##========================================================##
    ##=====##    Conditions for Histogram Selection    ##=====##
    ##========================================================##
    
    if(False in Conditions_For_Unfolding):
        # Conditions for unfolding were not met by 'out_print_main'
        # print("Conditions_For_Unfolding =", Conditions_For_Unfolding)
        count_failed += 1
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
        # if(not Sim_Test):
        out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
        out_print_main_rdf = out_print_main_rdf.replace("smear_",   "")
        out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
        out_print_main_gdf = out_print_main_gdf.replace("_smeared", "")
        out_print_main_gdf = out_print_main_gdf.replace("smear_",   "")
        out_print_main_gdf = out_print_main_gdf.replace("smear",    "")
        ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
        #############################################################################


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
            print("".join([color.BOLD, color.RED, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
            continue

        out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
        if(("".join([", (Var-D2='z_pT_Bin", str(Binning_Method)]) not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
            out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "".join(["]), (Var-D2='z_pT_Bin", str(Binning_Method), "" if("smear" not in str(out_print_main_mdf_1D)) else "_smeared", "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
        if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf_1D), color.END, "\n"]))
            for ii in mdf.GetListOfKeys():
                if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                    print(str(ii.GetName()))
            
        if(out_print_main_rdf not in rdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN RDF...\n", color.END, color.RED, "Dataframe is missing: \n ", color.BOLD, color.BLUE, str(out_print_main_rdf), color.END, "\n"]))
            # for ii in rdf.GetListOfKeys():
            #     print("\n", ii.GetName())
            continue

        if(out_print_main_gdf not in gdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN GDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.GREEN, str(out_print_main_gdf), color.END, "\n"]))
            continue


        
        # Q2_xB_Bin_Unfold = 0 if("Q2-xB-Bin=All" in str(out_print_main)) else 1 if("Q2-xB-Bin=1" in str(out_print_main)) else 2 if("Q2-xB-Bin=2" in str(out_print_main)) else 3 if("Q2-xB-Bin=3" in str(out_print_main)) else 4 if("Q2-xB-Bin=4" in str(out_print_main)) else 5 if("Q2-xB-Bin=5" in str(out_print_main)) else 6 if("Q2-xB-Bin=6" in str(out_print_main)) else 7 if("Q2-xB-Bin=7" in str(out_print_main)) else 8 if("Q2-xB-Bin=8" in str(out_print_main)) else 9 if("Q2-xB-Bin=9" in str(out_print_main)) else 10 if("Q2-xB-Bin=10" in str(out_print_main)) else 11 if("Q2-xB-Bin=11" in str(out_print_main)) else 12 if("Q2-xB-Bin=12" in str(out_print_main)) else "Undefined..."
        Q2_xB_Bin_Unfold = 0 if("Q2-xB-Bin=All" in str(out_print_main) or "Q2-y-Bin=All," in str(out_print_main)) else 1 if("Q2-xB-Bin=1," in str(out_print_main) or "Q2-y-Bin=1," in str(out_print_main)) else 2 if("Q2-xB-Bin=2," in str(out_print_main) or "Q2-y-Bin=2," in str(out_print_main)) else 3 if("Q2-xB-Bin=3," in str(out_print_main) or "Q2-y-Bin=3," in str(out_print_main)) else 4 if("Q2-xB-Bin=4," in str(out_print_main) or "Q2-y-Bin=4," in str(out_print_main)) else 5 if("Q2-xB-Bin=5," in str(out_print_main) or "Q2-y-Bin=5," in str(out_print_main)) else 6 if("Q2-xB-Bin=6," in str(out_print_main) or "Q2-y-Bin=6," in str(out_print_main)) else 7 if("Q2-xB-Bin=7," in str(out_print_main) or "Q2-y-Bin=7," in str(out_print_main)) else 8 if("Q2-xB-Bin=8," in str(out_print_main) or "Q2-y-Bin=8," in str(out_print_main)) else 9 if("Q2-xB-Bin=9," in str(out_print_main) or "Q2-y-Bin=9," in str(out_print_main)) else 10 if("Q2-xB-Bin=10," in str(out_print_main) or "Q2-y-Bin=10," in str(out_print_main)) else 11 if("Q2-xB-Bin=11," in str(out_print_main) or "Q2-y-Bin=11," in str(out_print_main)) else 12 if("Q2-xB-Bin=12," in str(out_print_main) or "Q2-y-Bin=12," in str(out_print_main)) else 13 if("Q2-xB-Bin=13," in str(out_print_main) or "Q2-y-Bin=13," in str(out_print_main)) else 14 if("Q2-xB-Bin=14," in str(out_print_main) or "Q2-y-Bin=14," in str(out_print_main)) else 15 if("Q2-xB-Bin=15," in str(out_print_main) or "Q2-y-Bin=15," in str(out_print_main)) else 16 if("Q2-xB-Bin=16," in str(out_print_main) or "Q2-y-Bin=16," in str(out_print_main)) else 17 if("Q2-xB-Bin=17," in str(out_print_main) or "Q2-y-Bin=17," in str(out_print_main)) else 18 if("Q2-xB-Bin=18," in str(out_print_main) or "Q2-y-Bin=18," in str(out_print_main)) else "Undefined..."

        # print("\n\nQ2_xB_Bin_Unfold =", Q2_xB_Bin_Unfold)
        # print("out_print_main =", out_print_main, "\n\n")
        
        if(type(Q2_xB_Bin_Unfold) is str):
            print("".join([color.RED, color.BOLD, "\nERROR - Q2_xB_Bin_Unfold = ", str(Q2_xB_Bin_Unfold), color.END]))

        if((str(Q2_xB_Bin_Unfold) not in Q2_xB_Bin_List) and ("Multi_Dim_Q2_y_Bin_phi_t" not in str(out_print_main))):
            # print("Skipping unselected Q2-xB Bin...")
            print("".join(["Bin ", str(Q2_xB_Bin_Unfold), " is not in Q2_xB_Bin_List = ", str(Q2_xB_Bin_List)]))
            continue
        
        count += 1
        print("".join(["\nUnfolding: ", str(out_print_main)]))
        ExREAL_1D_initial   = rdf.Get(out_print_main_rdf)
        MC_REC_1D_initial   = mdf.Get(out_print_main_mdf_1D)
        MC_GEN_1D_initial   = gdf.Get(out_print_main_gdf)
        Response_2D_initial = mdf.Get(out_print_main_mdf)
        
        # print("\n\n")
        # print("".join(["ExREAL_1D_initial[", str(ExREAL_1D_initial.GetName()), "]: \n\t\t", str(type(ExREAL_1D_initial)), "\n"]))
        # print("".join(["MC_REC_1D_initial[", str(out_print_main_mdf_1D), "]: \n\t\t", str(type(MC_REC_1D_initial)), "\n"]))
        # print("".join(["MC_GEN_1D_initial[", str(MC_GEN_1D_initial.GetName()), "]: \n\t\t", str(type(MC_GEN_1D_initial)), "\n"]))
        # print("".join(["Response_2D_initial[", str(Response_2D_initial.GetName()), "]: \n\t\t", str(type(Response_2D_initial)), "\n"]))



###############################################################################################
###############################################################################################
###==========##==========###     z-pT Binning Dimensions Slice     ###==========##==========###


        z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3] or ("Binning-Type='3'" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [4]) else 36 if(Q2_xB_Bin_Unfold in [5]) else 25 if(Q2_xB_Bin_Unfold in [6, 7]) else 20 if(Q2_xB_Bin_Unfold in [8]) else 1
        
        if("y_bin" in Binning_Method):
            z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin_Unfold in [4])           else 36 if(Q2_xB_Bin_Unfold in [5, 8, 9, 11, 12]) else 30 if(Q2_xB_Bin_Unfold in [6, 10])       else 25 if(Q2_xB_Bin_Unfold in [13])     else 1
            z_pT_Bin_Range = 0
            z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin_Unfold in [4])           else 36 if(Q2_xB_Bin_Unfold in [5, 8, 9])         else 30 if(Q2_xB_Bin_Unfold in [6, 10, 11])   else 25 if(Q2_xB_Bin_Unfold in [13, 14]) else 20 if(Q2_xB_Bin_Unfold in [12, 15, 16, 17]) else 1
            
            z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [2])          else 36 if(Q2_xB_Bin_Unfold in [4, 5, 9, 10]) else 35 if(Q2_xB_Bin_Unfold in [1, 3])            else 30 if(Q2_xB_Bin_Unfold in [6, 7, 8, 11]) else 25 if(Q2_xB_Bin_Unfold in [13, 14]) else 20 if(Q2_xB_Bin_Unfold in [12, 15, 16, 17]) else 1
        

        for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
            if("y_bin" not in Binning_Method):
                if(((Q2_xB_Bin_Unfold in [1, 2]) and (z_pT_Bin_Unfold in [49])) or (Q2_xB_Bin_Unfold == 3 and z_pT_Bin_Unfold in [49, 48, 42]) or (Q2_xB_Bin_Unfold in [1, 4] and z_pT_Bin_Unfold in [42]) or (Q2_xB_Bin_Unfold == 5 and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold == 7 and z_pT_Bin_Unfold in [25])):
                    continue
            else:
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
                    Response_2D           = Response_2D_initial.Project3D('yx')
                    Response_2D.SetName(str(Response_2D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])))
                    if("y_bin" not in Binning_Method):
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
                    ExREAL_1D                        = ExREAL_1D_initial.ProjectionX(str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExREAL_1D_0, bin_ExREAL_1D_1)
                    if("y_bin" not in Binning_Method):
                        ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    ExREAL_1D.SetTitle(ExREAL_1D_Title_New)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (ExREAL_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                print("\nExREAL_1D already is a 1D Histogram...")
                ExREAL_1D = ExREAL_1D_initial

            if("2D" in str(type(MC_REC_1D_initial))):
                try:
                    bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                    MC_REC_1D                        = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_REC_1D_0, bin_MC_REC_1D_1)
                    if("y_bin" not in Binning_Method):
                        MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_REC_1D.SetTitle(MC_REC_1D_Title_New)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (MC_REC_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                print("\nMC_REC_1D already is a 1D Histogram...")
                MC_REC_1D = MC_REC_1D_initial

            if("2D" in str(type(MC_GEN_1D_initial))):
                try:
                    bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                    MC_GEN_1D                        = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_GEN_1D_0, bin_MC_GEN_1D_1)
                    if("y_bin" not in Binning_Method):
                        MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    else:
                        MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_GEN_1D.SetTitle(MC_GEN_1D_Title_New)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (MC_GEN_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                print("\nMC_GEN_1D already is a 1D Histogram...")
                MC_GEN_1D = MC_GEN_1D_initial

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
                        if("'pT'" not in out_print_main and "'pT_smeared'" not in out_print_main):
                            ExREAL_1D.SetBinContent(1, 0)
                            MC_REC_1D.SetBinContent(1, 0)
                            MC_GEN_1D.SetBinContent(1, 0)
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
                    
                    
            if(Sim_Test):
                print(color.BOLD, "\n\nFor 'Sim_Test' of 'out_print_main' =", color.BLUE,  str(out_print_main),        color.END)
                print(color.BOLD, "\t'out_print_main_rdf'    =",              color.GREEN, str(out_print_main_rdf),    color.END)
                print(color.BOLD, "\t'out_print_main_mdf_1D' =",              color.GREEN, str(out_print_main_mdf_1D), color.END)
                for xbin in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                    MC_REC_1D_Content = MC_REC_1D.GetBinContent(xbin)
                    ExREAL_1D_Content = ExREAL_1D.GetBinContent(xbin)
                    if(0 not in [MC_REC_1D_Content, ExREAL_1D_Content, MC_REC_1D_Content - ExREAL_1D_Content]):
                        print("\t\tDifference (smear - unsmear) in Bin", xbin, " =", str(round(((MC_REC_1D_Content - ExREAL_1D_Content)/ExREAL_1D_Content)*100, 4)), "% of Unsmeared")
                    else:
                        print("\t\tDifference (smear - unsmear) in Bin", xbin, " =", str(round(MC_REC_1D_Content - ExREAL_1D_Content, 4)))
                print("\n\n")
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("Cut: No Cuts", "")).replace("Cut:  No Cuts", ""))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))


            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("_{t}", "_{h}")))
            ExREAL_1D.GetXaxis().SetTitle(str((str(ExREAL_1D.GetXaxis().GetTitle()).replace("_{t}", "_{h}")).replace(") (", " - ")))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("_{t}", "_{h}")))
            MC_REC_1D.GetXaxis().SetTitle(str((str(MC_REC_1D.GetXaxis().GetTitle()).replace("_{t}", "_{h}")).replace(") (", " - ")))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("_{t}", "_{h}")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("_{t}", "_{h}")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("_{t}", "_{h}")))
            Response_2D.GetXaxis().SetTitle(str((str(Response_2D.GetXaxis().GetTitle()).replace("_{t}", "_{h}")).replace(") (", " - ")))
            Response_2D.GetYaxis().SetTitle(str((str(Response_2D.GetYaxis().GetTitle()).replace("_{t}", "_{h}")).replace(") (", " - ")))

            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2",  "#phi_{h}+Q^{2}-x_{B} Bin}"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2",  "#phi_{h}+Q^{2}-x_{B} Bin}"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_2", "#phi_{h}+Q^{2}-x_{B} Bin"))
            

            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3",  "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3",  "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_xB_Bin_3", "#phi_{h}+Q^{2}-x_{B} Bin (New)"))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",  "#phi_{h}+Q^{2}-y Bin}"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin",  "#phi_{h}+Q^{2}-y Bin}"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2_y_Bin", "#phi_{h}+Q^{2}-y Bin"))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",  "#phi_{h}+Q^{2}-y Bin}"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t",  "#phi_{h}+Q^{2}-y Bin}"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("Q2_y_Bin_phi_t", "#phi_{h}+Q^{2}-y Bin"))
            
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("Q2_phi_t",  "#phi_{h}+Q^{2}"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("Q2_phi_t",  "#phi_{h}+Q^{2}"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("Q2_phi_t", "#phi_{h}+Q^{2}"))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}")))
            ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",  "#phi_{h}+Q^{2}"))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}")))
            MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("phi_t_Q2",  "#phi_{h}+Q^{2}"))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}")))
            MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}")))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}")))
            Response_2D.GetXaxis().SetTitle(str(Response_2D.GetXaxis().GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}"))
            Response_2D.GetYaxis().SetTitle(str(Response_2D.GetYaxis().GetTitle()).replace("phi_t_Q2", "#phi_{h}+Q^{2}"))
            
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
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
            
            if("Var-D1='Q2" in out_print_main):
                ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV^{2}]"]))
                
            if("Var-D1='pT" in out_print_main):
                ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV]"]))
                Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV]"]))

                
                
                
                
                
            ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin",     ""))
            Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                
#             continue
                
                
        
        
                
            List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold)
            
                
                
                
            continue
                
                
        
        
        
        
        
        
        
        
        
        
                
                
                
                
            # if(("'Combined_phi_t_Q2_xB"  in str(out_print_main)) or ("'Multi_Dim_Q2_xB_Bin" in str(out_print_main))):
            if("'Combined_phi_t_Q2_xB"  in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear="", Out_Option="Save")
            # elif(("'Combined_phi_t_Q2_y" in str(out_print_main)) or ("'Multi_Dim_Q2_y_Bin_phi_t"  in str(out_print_main))):
            elif("'Combined_phi_t_Q2_y" in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]),       Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]),       Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]),       Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]),       Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]),       Smear="", Out_Option="Save")
            # elif(("'Combined_phi_t_Q2"   in str(out_print_main)) or ("'Multi_Dim_Q2_phi_t"    in str(out_print_main))):
            elif("'Combined_phi_t_Q2"   in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Combined_phi_t_Q2",                                             Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Combined_phi_t_Q2",                                             Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Combined_phi_t_Q2",                                             Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Combined_phi_t_Q2",                                             Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="Combined_phi_t_Q2",                                             Smear="", Out_Option="Save")
                
            if("'Multi_Dim_Q2_xB_Bin"                in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear="", Out_Option="Save")
            elif("'Multi_Dim_Q2_y_Bin_phi_t"         in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear="", Out_Option="Save")
            elif("'Multi_Dim_Q2_phi_t"               in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_phi_t",                                            Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_phi_t",                                            Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_phi_t",                                            Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_phi_t",                                            Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="Multi_Dim_Q2_phi_t",                                            Smear="", Out_Option="Save")
            elif("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(out_print_main)):
                # MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear="" if(not Sim_Test) else "" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                # MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear=""                          if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=ExREAL_1D, Title="norm", Name=out_print_main, Method="rdf", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear="", Out_Option="Save")
                MultiD_Slice(Histo=MC_REC_1D, Title="norm", Name=out_print_main, Method="mdf", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear=""  if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                MultiD_Slice(Histo=MC_GEN_1D, Title="norm", Name=out_print_main, Method="gdf", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear="", Out_Option="Save")

                
            try:
                out_print_main_binned = out_print_main.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)]))
                # if("'Combined_" not in str(out_print_main)):
                #     try:
                #         Unfolding_Histograms  = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default")
                #         Unfolding_Histogram_1 = Unfolding_Histograms[0]
                #     except:
                #         print("".join([color.BOLD, color.RED, "ERROR IN SVD UNFOLDING ('Unfolding_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                # else:
                #     Unfolding_Histogram_1 = False
                Unfolding_Histogram_1 = False
                # else:
                #     Unfolding_Histogram_1 = MC_GEN_1D.Add(MC_GEN_1D, -1)
                try:
                    Bin_Method_Histograms = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin")
                    Bin_Unfolded[out_print_main_binned], Bin_Acceptance[out_print_main_binned] = Bin_Method_Histograms
                    # if(("'Combined_phi_t_Q2_xB"   in str(out_print_main)) or ("'Multi_Dim_Q2_xB_Bin"       in str(out_print_main))):
                    if("'Combined_phi_t_Q2_xB"   in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    # elif(("'Combined_phi_t_Q2_xB" in str(out_print_main)) or ("'Multi_Dim_Q2_y_Bin_phi_t"  in str(out_print_main))):
                    elif("'Combined_phi_t_Q2_xB" in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="".join(["Combined_phi_t_Q2_y_Bin",  str(Binning_Method)]),      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    # elif(("'Combined_phi_t_Q2"    in str(out_print_main)) or ("'Multi_Dim_Q2_phi_t"        in str(out_print_main))):
                    elif("'Combined_phi_t_Q2"    in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="Combined_phi_t_Q2",                                             Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                        
                    if("'Multi_Dim_Q2_xB_Bin"                in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_y_Bin_phi_t"         in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_phi_t"               in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="Multi_Dim_Q2_phi_t",                                            Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(out_print_main)):
                        MultiD_Slice(Histo=Bin_Unfolded[out_print_main_binned], Title="norm", Name=out_print_main, Method="Bin-by-bin", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")

                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                    
                try: 
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])]   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes"))[0]
                    # if(("'Combined_phi_t_Q2_xB"  in str(out_print_main)) or ("'Multi_Dim_Q2_xB_Bin" in str(out_print_main))):
                    if("'Combined_phi_t_Q2_xB"  in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    # elif(("'Combined_phi_t_Q2_y" in str(out_print_main)) or ("'Multi_Dim_Q2_y_Bin_phi_t"  in str(out_print_main))):
                    elif("'Combined_phi_t_Q2_y" in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="".join(["Combined_phi_t_Q2_y_Bin",  str(Binning_Method)]),      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    # elif(("'Combined_phi_t_Q2"   in str(out_print_main)) or ("'Multi_Dim_Q2_phi_t"    in str(out_print_main))):
                    elif("'Combined_phi_t_Q2"   in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="Combined_phi_t_Q2",                                             Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                        
                    if("'Multi_Dim_Q2_xB_Bin"                in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_y_Bin_phi_t"         in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="Multi_Dim_Q2_y_Bin_phi_t",                                      Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_phi_t"               in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="Multi_Dim_Q2_phi_t",                                            Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                    elif("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(out_print_main)):
                        MultiD_Slice(Histo=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Title="norm", Name=out_print_main, Method="Bayesian", Variable="Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t",                              Smear="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Out_Option="Save")
                        
                        
                        
                    if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim_" not in str(out_print_main))):
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd"))[0]
                    else:
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = False
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]     = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd"))[0]
                    # if("'Combined_" not in str(out_print_main)):
                    #     RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd"))[0]
                    # else:
                    #     RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])]
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])]   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bbb"))[0]
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold UNFOLDING METHOD(s):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                # if(("'Combined_phi_t_Q2_xB" in str(out_print_main)) or ("'Multi_Dim_Q2_xB_Bin" in str(out_print_main))):
                if("'Combined_phi_t_Q2_xB" in str(out_print_main)):
                    MultiD_Canvas_Combine(Histo_rdf=ExREAL_1D, Histo_mdf=MC_REC_1D, Histo_gdf=MC_GEN_1D, Histo_bin=Bin_Unfolded[out_print_main_binned], Histo_bay=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Name_Combine=out_print_main, Variable_Combine="".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]),      Smear_Combine="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear")
                # elif(("'Combined_phi_t_Q2"  in str(out_print_main)) or ("'Multi_Dim_Q2_phi_t"  in str(out_print_main))):
                elif("'Combined_phi_t_Q2"  in str(out_print_main)):
                    MultiD_Canvas_Combine(Histo_rdf=ExREAL_1D, Histo_mdf=MC_REC_1D, Histo_gdf=MC_GEN_1D, Histo_bin=Bin_Unfolded[out_print_main_binned], Histo_bay=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Name_Combine=out_print_main, Variable_Combine="Combined_phi_t_Q2",                                             Smear_Combine="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear")
                    
#                 if("'Multi_Dim_Q2_xB_Bin"   in str(out_print_main)):
#                     MultiD_Canvas_Combine(Histo_rdf=ExREAL_1D, Histo_mdf=MC_REC_1D, Histo_gdf=MC_GEN_1D, Histo_bin=Bin_Unfolded[out_print_main_binned], Histo_bay=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Name_Combine=out_print_main, Variable_Combine="".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), Smear_Combine="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear")
#                 elif("'Multi_Dim_Q2_phi_t"  in str(out_print_main)):
#                     MultiD_Canvas_Combine(Histo_rdf=ExREAL_1D, Histo_mdf=MC_REC_1D, Histo_gdf=MC_GEN_1D, Histo_bin=Bin_Unfolded[out_print_main_binned], Histo_bay=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], Name_Combine=out_print_main, Variable_Combine="Multi_Dim_Q2_phi_t",                                            Smear_Combine="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear")
                
                Plot_Version = "Web"
                # Plot_Version = "Note"
                
                # if("phi_t" not in out_print_main):
                #     Plot_Version = "Note"
                    
                if(Plot_Version == "Web"):
                    # Unfolded_Canvas[out_print_main_binned] = Canvas_Create(Name=out_print_main_binned, Num_Columns=1, Num_Rows=3, Size_X=1200, Size_Y=1200, cd_Space=0)
                    Unfolded_Canvas[out_print_main_binned] = Canvas_Create(Name=out_print_main_binned, Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=2400, cd_Space=0)
                    Unfolded_Canvas_main_Row_1 = Unfolded_Canvas[out_print_main_binned].cd(1)
                    Unfolded_Canvas_main_Row_2 = Unfolded_Canvas[out_print_main_binned].cd(2)
                    Unfolded_Canvas_main_Row_3 = Unfolded_Canvas[out_print_main_binned].cd(3)
                    Unfolded_Canvas_main_Row_1.Divide(4, 1, 0, 0)
                    Unfolded_Canvas_main_Row_2.Divide(4, 1, 0, 0)
                    Unfolded_Canvas_main_Row_3.Divide(4, 2, 0, 0)
                    # Unfolded_Canvas[out_print_main_binned].Draw()
                elif(Plot_Version == "Note"):
                    Unfolded_Canvas[out_print_main_binned] = Canvas_Create(Name=out_print_main_binned, Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1200, cd_Space=0)
                    Unfolded_Canvas_main_Row_1 = Unfolded_Canvas[out_print_main_binned].cd(1)
                    Unfolded_Canvas_main_Row_2 = Unfolded_Canvas[out_print_main_binned].cd(2)
                    Unfolded_Canvas_main_Row_1.Divide(2, 1, 0, 0)
                    Unfolded_Canvas_main_Row_2.Divide(2, 1, 0, 0)
                    # Unfolded_Canvas[out_print_main_binned].Draw()


##########################################################################################################################################################
    #################################################
    ##=====##=====##   Axis Ranges   ##=====##=====##
                try:
                    Unfolded_Max = 1.25*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # if(Plot_Version == "Web"):
                    #     Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # elif(Plot_Version == "Note"):
                    #     Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])]], Norm_Q="Norm")
                    # Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN Y-AXIS MAXIMUM (Unfolded)...", color.END]))
                    Unfolded_Max = 1
                    print("".join([color.BOLD, color.RED, "ERROR:\n",                                color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    Data_REC_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[ExREAL_1D, MC_REC_1D], Norm_Q="Norm")
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN Y-AXIS MAXIMUM (Reconstructed)...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n",                                     color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    Response_2D.GetXaxis().SetRange(1, Response_2D.GetXaxis().GetNbins() + 2)
                    Response_2D.GetYaxis().SetRange(1, Response_2D.GetYaxis().GetNbins() + 2)
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN 2D Matrix Ranges...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n",                                     color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    RooUnfolded_Histos["".join([str(out_print_main_binned),   "_bayes"])].GetXaxis().SetRange(1, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].GetXaxis().GetNbins() + 1)
                    if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))):
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].GetXaxis().SetRange(1, RooUnfolded_Histos["".join([str(out_print_main_binned),   "_svd"])].GetXaxis().GetNbins() + 1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].GetXaxis().SetRange(1,   RooUnfolded_Histos["".join([str(out_print_main_binned),   "_bbb"])].GetXaxis().GetNbins() + 1)
                    Bin_Unfolded[out_print_main_binned].GetXaxis().SetRange(1, Bin_Unfolded[out_print_main_binned].GetXaxis().GetNbins() + 1)
                    MC_GEN_1D.GetXaxis().SetRange(1, MC_GEN_1D.GetXaxis().GetNbins() + 1)
                    ExREAL_1D.GetXaxis().SetRange(1, ExREAL_1D.GetXaxis().GetNbins() + 1)
                    MC_REC_1D.GetXaxis().SetRange(1, MC_REC_1D.GetXaxis().GetNbins() + 1)
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN 1D X-Axis Ranges...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n",                       color.END, color.RED, str(traceback.format_exc()), color.END]))
    ##=====##=====##   Axis Ranges   ##=====##=====##
    #################################################
    ##=====##=====##  Legends Setup  ##=====##=====##
                if((("phi_t" not in out_print_main_binned) and ("'phi_t_smeared'" not in out_print_main_binned)) and (("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main)))):
                    Legends[(out_print_main_binned, "Unfolded")] = ROOT.TLegend(0.5,  0.5,  0.95, 0.75)
                elif(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))):
                    Legends[(out_print_main_binned, "Unfolded")] = ROOT.TLegend(0.25, 0.15, 0.85, 0.55)
                else:
                    Legends[(out_print_main_binned, "Unfolded")] = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                    
                Legends[(out_print_main_binned, "Unfolded")].SetNColumns(2 if("'Combined_" not in str(out_print_main)) else 1)
                Legends[(out_print_main_binned, "Unfolded")].SetBorderSize(0)
                Legends[(out_print_main_binned, "Unfolded")].SetFillColor(0)
                Legends[(out_print_main_binned, "Unfolded")].SetFillStyle(0)

                # if("phi_t" not in out_print_main_binned and "'phi_t_smeared'" not in out_print_main_binned):
                #     Legends[(out_print_main_binned, "REC")] = ROOT.TLegend(0.5, 0.5, 0.95, 0.75)
                # else:
                #     Legends[(out_print_main_binned, "REC")] = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                Legends[(out_print_main_binned, "REC")] = ROOT.TLegend(0.35, 0.25, 0.75, 0.5)
                Legends[(out_print_main_binned, "REC")].SetNColumns(1)
                Legends[(out_print_main_binned, "REC")].SetBorderSize(0)
                Legends[(out_print_main_binned, "REC")].SetFillColor(0)
                Legends[(out_print_main_binned, "REC")].SetFillStyle(0)
    ##=====##=====##  Legends Setup  ##=====##=====##
    #################################################


##########################################################################################################################################################
##########################################################################################################################################################
    ##=====##=====##   Unfolded Histogram   ##=====##=====##
                try:
                    if(Unfolding_Histogram_1 is not False):
                        Unfolding_Histogram_1.GetYaxis().SetTitle("Normalized")
                        # Unfolding_Histogram_1.SetTitle(str(Unfolding_Histogram_1.GetTitle()).replace("SVD ", ""))
                        Unfolding_Histogram_1.SetMarkerColor(root_color.Pink)
                        Unfolding_Histogram_1.SetLineWidth(3)
                        Unfolding_Histogram_1.SetLineStyle(1)
                        Unfolding_Histogram_1.SetLineColor(root_color.Pink)
                        Unfolding_Histogram_1.SetMarkerSize(1)
                        Unfolding_Histogram_1.SetMarkerStyle(20)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN DRAWING SVD UNFOLDING ('Unfolding_Histogram_1'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                                        
                try:
                    Bin_Unfolded[out_print_main_binned].GetYaxis().SetTitle("Normalized")
                    Bin_Unfolded[out_print_main_binned].SetLineColor(root_color.Brown)
                    Bin_Unfolded[out_print_main_binned].SetLineWidth(2  if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))) else 1)
                    Bin_Unfolded[out_print_main_binned].SetLineStyle(1)
                    Bin_Unfolded[out_print_main_binned].SetMarkerColor(root_color.Brown)
                    # Bin_Unfolded[out_print_main_binned].SetMarkerSize(1 if("'Combined_" not in str(out_print_main)) else 0.5)
                    Bin_Unfolded[out_print_main_binned].SetMarkerSize(1.5)
                    Bin_Unfolded[out_print_main_binned].SetMarkerStyle(21)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN DRAWING BIN UNFOLDING ('Bin_Unfolded[out_print_main]'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                    
                try:
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].GetYaxis().SetTitle("Normalized")
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].GetYaxis().SetTitle("Normalized")

                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineColor(30)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineColor(41)
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineWidth(2 if("'Combined_" not in str(out_print_main)) else 1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineWidth(2)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineStyle(1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineStyle(1)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerColor(30)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerColor(41)
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerSize(1 if("'Combined_" not in str(out_print_main)) else 0.5)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerSize(1)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerStyle(21)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerStyle(21)
                    
                    if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))):
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].GetYaxis().SetTitle("Normalized")
                        # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineColor(46)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineColor(root_color.Pink)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineWidth(2)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineStyle(1)
                        # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerColor(46)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerColor(root_color.Pink)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerSize(1)
                        # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerSize(0.75)
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerStyle(21)

                    

                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN DRAWING RooUnfolded HISTOS:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                    

                    
##########################################################################################################################################################
##########################################################################################################################################################

##########################################################################################################################################################
##########################################################################################################################################################
    ##=====##=====##   Experimental Histogram   ##=====##=====##
                try:
                    ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace("Experimental", "Reconstucted"))
                    ExREAL_1D.GetYaxis().SetTitle("Normalized")
                    ExREAL_1D.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", ""))
                    ExREAL_1D.SetLineColor(root_color.Blue)
                    ExREAL_1D.SetLineWidth(2)
                    ExREAL_1D.SetLineStyle(1)
                    ExREAL_1D.SetMarkerColor(root_color.Blue)
                    ExREAL_1D.SetMarkerSize(1)
                    ExREAL_1D.SetMarkerStyle(21)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN HISTOGRAM(S) ('ExREAL_1D'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
##########################################################################################################################################################
##########################################################################################################################################################

##########################################################################################################################################################
##########################################################################################################################################################
    ##=====##=====##   MC REC Histogram   ##=====##=====##
                try:
                    MC_REC_1D.GetYaxis().SetTitle("Normalized")
                    MC_REC_1D.GetXaxis().SetTitle(str(MC_REC_1D.GetXaxis().GetTitle()).replace("(REC)", ""))
                    MC_REC_1D.SetLineColor(root_color.Red)
                    MC_REC_1D.SetLineWidth(2)
                    MC_REC_1D.SetLineStyle(1)
                    MC_REC_1D.SetMarkerColor(root_color.Red)
                    MC_REC_1D.SetMarkerSize(1)
                    MC_REC_1D.SetMarkerStyle(22)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN HISTOGRAM(S) ('MC_REC_1D'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
##########################################################################################################################################################
##########################################################################################################################################################

##########################################################################################################################################################
##########################################################################################################################################################
    ##=====##=====##   MC GEN Histogram   ##=====##=====##
                try:
                    MC_GEN_1D.SetLineColor(root_color.Green)
                    MC_GEN_1D.SetLineWidth(3  if(("'Combined_"  not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))) else 1)
                    MC_GEN_1D.SetLineStyle(1)
                    MC_GEN_1D.SetMarkerColor(root_color.Green)
                    MC_GEN_1D.SetMarkerSize(1 if(("'Combined_" not in str(out_print_main))  and ("'Multi_Dim" not in str(out_print_main))) else 0.5)
                    MC_GEN_1D.SetMarkerStyle(20)
                    MC_GEN_1D.GetYaxis().SetTitle("Normalized")
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN HISTOGRAM(S) ('MC_GEN_1D'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
##########################################################################################################################################################
##########################################################################################################################################################

##########################################################################################################################################################
##########################################################################################################################################################
    ##=====##=====##   Drawing the Bin-by-Bin Acceptance Histogram (cd: 2-1)   ##=====##=====##
                try:
                    Bin_Acceptance[out_print_main_binned].SetLineColor(root_color.Red)
                    Bin_Acceptance[out_print_main_binned].SetLineWidth(2)
                    Bin_Acceptance[out_print_main_binned].SetMarkerColor(root_color.Red)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN BIN UNFOLDING ('Bin_Acceptance[out_print_main]'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
##########################################################################################################################################################
##########################################################################################################################################################





#########################################################################################################################
##==================================#################################################==================================##
##==========##==========##==========##   Openning Canvas Pads to Draw Histograms   ##==========##==========##==========##
##==================================#################################################==================================##
#########################################################################################################################

    ##################################################################
    ##==========##==========##     CD 1     ##==========##==========##
    ##################################################################
    ##=====##=====##   Drawing the Response Matrix    ##=====##=====##
                try:
                    Response_2D.SetTitle(str(Response_2D.GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                    if(Plot_Version == "Web"):
                        # Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=2, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=3, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        ROOT.gPad.SetLogz(1)
                        Response_2D.Draw("colz")
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=1, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        ROOT.gPad.SetLogz(1)
                        Response_2D.Draw("col")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = Response_2D.Clone()
                    Unfolded_Canvas[out_print_main_binned].Modified()
                    Unfolded_Canvas[out_print_main_binned].Update()
                    if(Plot_Version == "Web"):
                        palette_move(canvas=Unfolded_Canvas[out_print_main_binned], histo=Response_2D, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Response Matrix):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
    ##################################################################
    ##==========##==========##     CD 4     ##==========##==========##
    ##################################################################
    ##=====##=====## Drawing the Unfolding Histograms ##=====##=====##
                try:
                    if((Plot_Version == "Web") and (("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))) and (Unfolding_Histogram_1 is not False)):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=4, left_add=0.1, right_add=0.075, up_add=0.1, down_add=0.1)
                        Unfolding_Histogram_1.SetTitle(str(Unfolding_Histogram_1.GetTitle()).replace("SVD Unfolded Distribution", "Unfolded Distributions"))
                        Unfolding_Histogram_1_Norm = (Unfolding_Histogram_1.DrawNormalized("PL E0 same"))
                        for ii in range(0, Unfolding_Histogram_1_Norm.GetNbinsX() + 1, 1):
                            if(Unfolding_Histogram_1_Norm.GetBinError(ii) > 0.01):
                                print("".join([color.RED, "\n(SVD Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                                Unfolding_Histogram_1_Norm.SetBinContent(ii, 0)
                                Unfolding_Histogram_1_Norm.SetBinError(ii,   0)
                        Unfolding_Histogram_1_Norm.GetYaxis().SetRangeUser(0, Unfolded_Max)
                        Legends[(out_print_main_binned, "Unfolded")].AddEntry(Unfolding_Histogram_1, "#scale[2]{SVD Unfolded}", "lpE")
                    elif(Plot_Version == "Web"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=4, left_add=0.1, right_add=0.075, up_add=0.1, down_add=0.1)
                        Bin_Unfolded[out_print_main_binned].SetTitle(str(Bin_Unfolded[out_print_main_binned].GetTitle()).replace("Bin-By-Bin Unfolded Distribution", "Unfolded Distributions"))
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=2, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        if("'phi_t" in out_print_main or "'phi_t_smeared'" in out_print_main):
                            Bin_Unfolded[out_print_main_binned].GetXaxis().SetRangeUser(0, 360)
                        Bin_Unfolded[out_print_main_binned].SetTitle(str(Bin_Unfolded[out_print_main_binned].GetTitle()).replace("Bin-By-Bin Unfolded Distribution", "Unfolded Distributions"))
                        Bin_Unfolded[out_print_main_binned].SetTitle(str(Bin_Unfolded[out_print_main_binned].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                        # print(Bin_Unfolded[out_print_main_binned].GetTitle())
                    
                    # Bin_Unfolded[(out_print_main_binned, "Norm")] = (Bin_Unfolded[out_print_main_binned].DrawNormalized("H PL E0 same"))
                    Bin_Unfolded[(out_print_main_binned, "Norm")] = (Bin_Unfolded[out_print_main_binned].DrawNormalized("PL E0 same"))
                    for ii in range(0, Bin_Unfolded[(out_print_main_binned, "Norm")].GetNbinsX() + 1, 1):
                        if(Bin_Unfolded[(out_print_main_binned, "Norm")].GetBinError(ii) > 0.01):
                            print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                            Bin_Unfolded[(out_print_main_binned, "Norm")].SetBinContent(ii, 0)
                            Bin_Unfolded[(out_print_main_binned, "Norm")].SetBinError(ii,   0)
                    Bin_Unfolded[(out_print_main_binned, "Norm")].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    Bin_Unfolded[(out_print_main_binned, "Norm")].SetTitle(str(Bin_Unfolded[(out_print_main_binned, "Norm")].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                    Legends[(out_print_main_binned,  "Unfolded")].AddEntry(Bin_Unfolded[out_print_main_binned], "".join(["#scale[", "2" if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))) else "1", "]{Bin-by-Bin}"]), "lpE")
                    
                    if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))):
                        # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].DrawNormalized("H PL E0 same"))
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].DrawNormalized("PL E0 same"))
                        for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].GetNbinsX() + 1, 1):
                            if(RooUnfolded_Histos["".join([str(out_print_main_binned),  "_svd_Norm"])].GetBinError(ii) > 0.01):
                                print("".join([color.RED, "\n(RooUnfold (SVD) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                                RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].SetBinContent(ii, 0)
                                RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].SetBinError(ii,   0)
                        Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])], "#scale[2]{SVD (RooUnfold)}", "lpE")
                    
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])] = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].DrawNormalized("H PL E0 same"))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])] = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].DrawNormalized("PL E0 same"))
                    for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetNbinsX() + 1, 1):
                        if(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetBinError(ii) > 0.01):
                            print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii),  " has a large error (after normalizing)...", color.END]))
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].SetBinContent(ii, 0)
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].SetBinError(ii,   0)
                    Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])], "".join(["#scale[", "2" if(("'Combined_" not in str(out_print_main)) and ("'Multi_Dim" not in str(out_print_main))) else "1", "]{Bayesian}"]), "lpE")
                    
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].DrawNormalized("PL E0 same"))
                    # for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].GetNbinsX() + 1, 1):
                    #     if(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].GetBinError(ii) > 0.01):
                    #         print("".join([color.RED, "\n(RooUnfold (Bin-by-Bin) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                    #         RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].SetBinContent(ii, 0)
                    #         RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].SetBinError(ii,   0)
                    # Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])], "#scale[2]{Bin-by-Bin (RooUnfold)}", "lpE")

#                     Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("H PL E0 same")
#                     if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
#                         Save_Response_Matrix["".join(["Multi Variable " if("Combined" in out_print_main) else "", "MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("PL E0 same")
#                     else:
#                         MC_GEN_1D.DrawNormalized("PL E0 same")
#                     Legends[(out_print_main_binned, "Unfolded")].AddEntry(MC_GEN_1D, "".join(["#scale[", "2" if("'Combined_" not in str(out_print_main)) else "1", "]{MC GEN}"]), "lpE")

                    Legends[(out_print_main_binned, "Unfolded")].Draw("same")
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Unfolding Histograms):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    ##################################################################
    ##==========##==========##     CD 2     ##==========##==========##
    ##################################################################
    ##=====##=====##    Drawing the Bin Acceptance    ##=====##=====##
                try:
                    if(Plot_Version == "Web"):
                        # Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=3, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=4, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=1, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
                    Bin_Acceptance[out_print_main_binned].SetTitle(str(Bin_Acceptance[out_print_main_binned].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                    Bin_Acceptance[out_print_main_binned].Draw("same E1 H")
                    # Bin_Acceptance[out_print_main_binned].DrawNormalized("Hist E1 same")
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Bin Acceptance):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    ##################################################################
    ##==========##==========##     CD 3     ##==========##==========##
    ##################################################################
    ##=====##=====##   Drawing the Measured Histos    ##=====##=====##
                try:
                    if(Plot_Version == "Web"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=3, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=2, left_add=0.075, right_add=0.075, up_add=0.1, down_add=0.1)

                    if("'phi_t'" in out_print_main or "'phi_t_smeared''" in out_print_main):
                        ExREAL_1D.GetXaxis().SetRangeUser(0, 360)
                        if(Plot_Version == "Web"):
                            Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = (ExREAL_1D.DrawNormalized("H PL E0 same"))
                        else:
                            Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = (ExREAL_1D.DrawNormalized("PL E0 same"))
                      # Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = ExREAL_1D_Norm.Clone()
                        Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])].SetTitle(str(Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])].GetTitle()).replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", ""))
                        Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])].GetYaxis().SetRangeUser(0, Data_REC_Max)
                    else:
                        if(Plot_Version == "Web"):
                            ExREAL_1D_Norm = (ExREAL_1D.DrawNormalized("H PL E0 same"))
                        else:
                            ExREAL_1D_Norm = (ExREAL_1D.DrawNormalized("PL E0 same"))
                        ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, Data_REC_Max)
                    Legends[(out_print_main_binned, "REC")].AddEntry(ExREAL_1D, "#scale[2]{Experimental}" if(Plot_Version == "Web") else "#scale[1]{Experimental}", "lpE")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        if(Plot_Version == "Web"):
                            Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = MC_REC_1D.DrawNormalized("H PL E0 same")
                        else:
                            Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = MC_REC_1D.DrawNormalized("PL E0 same")
                    else:
                        if(Plot_Version == "Web"):
                            MC_REC_1D.DrawNormalized("H PL E0 same")
                        else:
                            MC_REC_1D.DrawNormalized("PL E0 same")
                    # MC_REC_1D_Norm = (MC_REC_1D.DrawNormalized("PL E1 same"))
                    Legends[(out_print_main_binned, "REC")].AddEntry(MC_REC_1D, "#scale[2]{MC REC}" if(Plot_Version == "Web") else "#scale[1]{MC REC}", "lpE")
                    
                    
                    MC_GEN_1D.GetXaxis().SetRangeUser(0, 360)
                    Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("H PL E0 same")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        Save_Response_Matrix["".join(["Multi Variable " if(("Combined" in out_print_main) or ("Multi_Dim" in out_print_main)) else "", "MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("PL E0 same")
                    else:
                        MC_GEN_1D.DrawNormalized("PL E0 same")
                    Legends[(out_print_main_binned, "REC")].AddEntry(MC_GEN_1D, "#scale[2]{MC GEN}" if(Plot_Version == "Web") else "#scale[1]{MC GEN}", "lpE")
                    
                    Legends[(out_print_main_binned, "REC")].Draw("same")
                    
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Experimental/Reconstructed):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                    
                    
                    
    ##################################################################
    ##==========##==========##   CD Extra   ##==========##==========##
    ##################################################################
    ##=====##=====##   Drawing the Extra 2D Histos    ##=====##=====##
                try:
                    if(Plot_Version == "Web"):
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_2, CD_Num=1, Var_D1="Q2_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "Q2",  Var_D2="xB_smeared"     if(Sim_Test and "smear" in str(out_print_main_mdf)) else "xB",     Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=2, Var_D1="z_smeared"   if(Sim_Test and "smear" in str(out_print_main_mdf)) else "z",   Var_D2="pT_smeared"     if(Sim_Test and "smear" in str(out_print_main_mdf)) else "pT",     Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=1, Var_D1="Q2_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "Q2",  Var_D2="y_smeared"      if(Sim_Test and "smear" in str(out_print_main_mdf)) else "y",      Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         # Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=1, Var_D1="Q2_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "Q2",  Var_D2="xB_smeared"     if(Sim_Test and "smear" in str(out_print_main_mdf)) else "xB",     Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         # Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_2, CD_Num=1, Var_D1="Q2_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "Q2",  Var_D2="y_smeared"      if(Sim_Test and "smear" in str(out_print_main_mdf)) else "y",      Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")

#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=1, Var_D1="el_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "el",  Var_D2="elth_smeared"   if(Sim_Test and "smear" in str(out_print_main_mdf)) else "elth",   Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=2, Var_D1="el_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "el",  Var_D2="elPhi_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "elPhi",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=3, Var_D1="pip_smeared" if(Sim_Test and "smear" in str(out_print_main_mdf)) else "pip", Var_D2="pipth_smeared"  if(Sim_Test and "smear" in str(out_print_main_mdf)) else "pipth",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=4, Var_D1="pip_smeared" if(Sim_Test and "smear" in str(out_print_main_mdf)) else "pip", Var_D2="pipPhi_smeared" if(Sim_Test and "smear" in str(out_print_main_mdf)) else "pipPhi", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("smear" not in str(out_print_main_mdf)) else "smear")

#                         Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=5, Var_D1="el_smeared"  if("smear" in str(out_print_main_mdf)) else "el",               Var_D2="elth_smeared"   if("smear" in str(out_print_main_mdf))              else "elth",   Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q=""                          if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=6, Var_D1="el_smeared"  if("smear" in str(out_print_main_mdf)) else "el",               Var_D2="elPhi_smeared"  if("smear" in str(out_print_main_mdf))              else "elPhi",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q=""                          if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=7, Var_D1="pip_smeared" if("smear" in str(out_print_main_mdf)) else "pip",              Var_D2="pipth_smeared"  if("smear" in str(out_print_main_mdf))              else "pipth",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q=""                          if("smear" not in str(out_print_main_mdf)) else "smear")
#                         Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=8, Var_D1="pip_smeared" if("smear" in str(out_print_main_mdf)) else "pip",              Var_D2="pipPhi_smeared" if("smear" in str(out_print_main_mdf))              else "pipPhi", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q=""                          if("smear" not in str(out_print_main_mdf)) else "smear")

                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_2, CD_Num=1, Var_D1="Q2",                                                            Var_D2="xB",                                                                  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=2, Var_D1="z",                                                             Var_D2="pT",                                                                  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=1, Var_D1="Q2",                                                            Var_D2="y",                                                                   Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")

                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=1, Var_D1="el",                                                            Var_D2="elth",                                                                Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=2, Var_D1="el",                                                            Var_D2="elPhi",                                                               Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=3, Var_D1="pip",                                                           Var_D2="pipth",                                                               Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=4, Var_D1="pip",                                                           Var_D2="pipPhi",                                                              Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")

                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=5, Var_D1="el_smeared"  if("smear" in str(out_print_main_mdf)) else "el",  Var_D2="elth_smeared"   if("smear" in str(out_print_main_mdf)) else "elth",   Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=6, Var_D1="el_smeared"  if("smear" in str(out_print_main_mdf)) else "el",  Var_D2="elPhi_smeared"  if("smear" in str(out_print_main_mdf)) else "elPhi",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=7, Var_D1="pip_smeared" if("smear" in str(out_print_main_mdf)) else "pip", Var_D2="pipth_smeared"  if("smear" in str(out_print_main_mdf)) else "pipth",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=8, Var_D1="pip_smeared" if("smear" in str(out_print_main_mdf)) else "pip", Var_D2="pipPhi_smeared" if("smear" in str(out_print_main_mdf)) else "pipPhi", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf",                             Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                    
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (2D Histograms):\n", color.END, str(traceback.format_exc())]))
                    
                    
                    


#########################################################################################################################
##==================================#################################################==================================##
##==========##==========##==========##   Openning Canvas Pads to Draw Histograms   ##==========##==========##==========##
##==================================#################################################==================================##
#########################################################################################################################

                Unfolded_Canvas[out_print_main_binned].Modified()
                Unfolded_Canvas[out_print_main_binned].Update()

                if(("phi_t" in out_print_main_binned) and (("Combined_" not in out_print_main) and ("Multi_Dim" not in out_print_main))):
                    # fit_function_title = "A + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h})"
                    # fit_function = "[A] + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180))"
                    if(not extra_function_terms):
                        # fit_function_title = "A + B Cos(#phi_{h}) + C Cos(2#phi_{h})"
                        # fit_function = "[A] + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180))"

                        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
                        fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
                        
                    else:
                        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
                        fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"
                        
                        # fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}) + E Cos(4#phi_{h}))"
                        # fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)) + [E]*cos(4*x*(3.1415926/180)))"

                    # Q2_xB_Bin_Title = "" if("Q2-xB-Bin=All" in str(out_print_main)) else "".join(["Q^{2}-x_{B} Bin: ", "1" if("Q2-xB-Bin=1" in str(out_print_main)) else "2" if("Q2-xB-Bin=2" in str(out_print_main)) else "3" if("Q2-xB-Bin=3" in str(out_print_main)) else "4" if("Q2-xB-Bin=4" in str(out_print_main)) else "5" if("Q2-xB-Bin=5" in str(out_print_main)) else "6" if("Q2-xB-Bin=6" in str(out_print_main)) else "7" if("Q2-xB-Bin=7" in str(out_print_main)) else "8" if("Q2-xB-Bin=8" in str(out_print_main)) else "9" if("Q2-xB-Bin=9" in str(out_print_main)) else "Error"])
                    Q2_xB_Bin_Title = "" if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: " if("y_bin" not in str(Binning_Method)) else "]{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"])
                ##################################################################
                ##==========##         Matrix Unfolded Fits         ##==========##
                ##################################################################
                    
                    # Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])] = Canvas_Create(Name="".join([str(out_print_main_binned), "extra"]), Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1600, cd_Space=0)
                    # Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])] = Canvas_Create(Name="".join([str(out_print_main_binned), "extra"]), Num_Columns=1, Num_Rows=2, Size_X=1800, Size_Y=1650, cd_Space=0)
                    Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])] = Canvas_Create(Name="".join([str(out_print_main_binned), "extra"]), Num_Columns=1, Num_Rows=2, Size_X=1200, Size_Y=1100, cd_Space=0)
                    # Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])].Draw()
                    
                    Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])] = Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])].cd(1)
                    Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])] = Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])].cd(2)
                    
                    # Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])].Divide(3, 1, 0)
                    Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])].Divide(2, 1, 0)
                    Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])].Divide(2, 1, 0)
                    # Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])].Divide(1, 1, 0)
                    
                    
                    
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 1, 0.15)
                    ExREAL_1D_Single = ExREAL_1D.Clone()
                    ExREAL_1D_Single_Title = str(ExREAL_1D_Single.GetTitle()).replace("Reconstucted Distribution", "Pre-Unfolded Distributions")
                    ExREAL_1D_Single_Title = ExREAL_1D_Single_Title.replace("#splitline{#splitline{#splitline{", "#splitline{")
                    ExREAL_1D_Single_Title = ExREAL_1D_Single_Title.replace("}}{#scale[1.15]{}}}", "}}")
                    ExREAL_1D_Single_Title = ExREAL_1D_Single_Title.replace("#scale[1.35]{Range: 0 #rightarrow 360 - Size: 15.0 per bin}}}{}", "".join(["#scale[1.15]{", str(Q2_xB_Bin_Title), "}}"]))
                    ExREAL_1D_Single_Title = ExREAL_1D_Single_Title.replace("Range: 0 #rightarrow 360 - Size: 15.0 per bin", str(Q2_xB_Bin_Title))
                    
                    if(("phi_" in str(out_print_main_binned)) and ("Multi_Dim" not in str(out_print_main_binned))):
                        ExREAL_1D_Single_Title = "".join(["#splitline{#scale[1.35]{Pre-Unfolded Distributions of #phi_{h}}}{#scale[1.35]{", str(Q2_xB_Bin_Title), "}}"])
                    
                    
                    ExREAL_1D_Single.SetTitle(ExREAL_1D_Single_Title)
                    # print(str(ExREAL_1D_Single.GetTitle()))
                    
                    ExREAL_1D_Single.DrawNormalized("H PL E0 same")
                    MC_REC_1D.DrawNormalized("H PL E0 same")
                    MC_GEN_1D.DrawNormalized("H PL E0 same")
                    # MC_GEN_1D.DrawNormalized("PL E0 same")
                    Legends[(out_print_main_binned, "REC")].Draw("same")
                    
                    ###################################################################
                    ##==========##         Bayesian Unfolded Fit         ##==========##
                    ###################################################################
#                     Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 1, 0.15)
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 2, 0.15)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].Clone()
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(30),"]{RooUnfold Bayesian} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetYaxis().SetTitle("")
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetXaxis().SetTitle(str(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetXaxis().GetTitle()).replace("(REC)", ""))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                    # A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])])
                    if(not extra_function_terms):
                        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])])
                    else:
                        # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])])
                        A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])])
                    # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
                    # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
                    # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
                    # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
                    # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
                    # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].Fit(Unfolded_Fit_Function, "RQ")

                    A_Unfold,   B_Unfold,   C_Unfold   = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    A_Unfold_E, B_Unfold_E, C_Unfold_E = Unfolded_Fit_Function.GetParError(0),  Unfolded_Fit_Function.GetParError(1),  Unfolded_Fit_Function.GetParError(2)
                    Parameter_List_Unfold_Methods["Bayes"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, A_Unfold_E, B_Unfold, B_Unfold_E, C_Unfold, C_Unfold_E, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

                    # statbox_move_new(Histogram=Unfolding_Histogram_1_Norm, Canvas=Unfolded_Canvas["".join([str(out_print_main), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    statbox_move(Histogram=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    # Unfolded_C_clone.ShowPeaks()
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
                    ###################################################################
                    ##==========##         Bayesian Unfolded Fit         ##==========##
                    ###################################################################
                    
                    
                    
                    ####################################################################
                    ##==========##      (RooUnfold) SVD Unfolded Fit      ##==========##
                    ####################################################################
#                     Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 2, 0.15)
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])], 1, 0.15)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].Clone()
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(46),"]{RooUnfold SVD} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Pink),"]{RooUnfold SVD} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetYaxis().SetTitle("")
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetXaxis().SetTitle(str(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].GetXaxis().GetTitle()).replace("(REC)", ""))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
#                     A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])])
                    if(not extra_function_terms):
                        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])])
                    else:
                        # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])])
                        A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])])
                    # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
                    # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
                    # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
                    # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
                    # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
                    # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].Fit(Unfolded_Fit_Function, "RQ")

                    # A_Unfold,   B_Unfold,   C_Unfold   = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    # A_Unfold_E, B_Unfold_E, C_Unfold_E = Unfolded_Fit_Function.GetParError(0),  Unfolded_Fit_Function.GetParError(1),  Unfolded_Fit_Function.GetParError(2)
                    # Parameter_List_Unfold_Methods["SVD_RooUnfold"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, A_Unfold_E, B_Unfold, B_Unfold_E, C_Unfold, C_Unfold_E, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

                    # statbox_move_new(Histogram=Unfolding_Histogram_1_Norm, Canvas=Unfolded_Canvas["".join([str(out_print_main), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    statbox_move(Histogram=RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    # Unfolded_C_clone.ShowPeaks()
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
                    ####################################################################
                    ##==========##      (RooUnfold) SVD Unfolded Fit      ##==========##
                    ####################################################################
                    
                    
                    
#                     #####################################################################
#                     ##==========##   (RooUnfold) Bin-by-Bin Unfolded Fit   ##==========##
#                     #####################################################################
#                     Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 3, 0.15)
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].Clone()
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(41),"]{RooUnfold Bin-by-Bin} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].GetYaxis().SetTitle("")
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].GetXaxis().SetTitle(str(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].GetXaxis().GetTitle()).replace("(REC)", ""))
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].Draw("PL E1 same")
#                     Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
#                     A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])])
#                     # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
#                     # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
#                     # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
#                     # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
#                     # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
#                     # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
#                     # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
#                     # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
#                     # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].Fit(Unfolded_Fit_Function, "RQ")
#
#                     # A_Unfold,   B_Unfold,   C_Unfold   = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
#                     # A_Unfold_E, B_Unfold_E, C_Unfold_E = Unfolded_Fit_Function.GetParError(0),  Unfolded_Fit_Function.GetParError(1),  Unfolded_Fit_Function.GetParError(2)
#                     # Parameter_List_Unfold_Methods["bbb"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, A_Unfold_E, B_Unfold, B_Unfold_E, C_Unfold, C_Unfold_E, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])
#
#                     # statbox_move_new(Histogram=Unfolding_Histogram_1_Norm, Canvas=Unfolded_Canvas["".join([str(out_print_main), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
#                     statbox_move(Histogram=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
#                     # Unfolded_C_clone.ShowPeaks()
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
#                     #####################################################################
#                     ##==========##   (RooUnfold) Bin-by-Bin Unfolded Fit   ##==========##
#                     #####################################################################
                    
                    
                    
                    # ###################################################################
                    # ##==========##      (Original) SVD Unfolded Fit      ##==========##
                    # ###################################################################
                    # try:
                    #     Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])], 1, 0.15)
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])] = Unfolding_Histogram_1_Norm.Clone()
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Pink),"]{SVD Unfolded} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetTitle("")
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetTitle(str(Unfolding_Histogram_1_Norm.GetXaxis().GetTitle()).replace("(REC)", ""))
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].Draw("PL E1 same")
                    #     Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                    #     A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])])
                    #     # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
                    #     # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
                    #     # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
                    #     # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
                    #     # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
                    #     # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
                    #     # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
                    #     # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
                    #     # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].Fit(Unfolded_Fit_Function, "RQ")

                    #     A_Unfold,   B_Unfold,   C_Unfold   = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    #     A_Unfold_E, B_Unfold_E, C_Unfold_E = Unfolded_Fit_Function.GetParError(0),  Unfolded_Fit_Function.GetParError(1),  Unfolded_Fit_Function.GetParError(2)
                    #     Parameter_List_Unfold_Methods["SVD"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, A_Unfold_E, B_Unfold, B_Unfold_E, C_Unfold, C_Unfold_E, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

                    #     statbox_move(Histogram=Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)#, Print_Method="norm"):
                    #     # Unfolded_C_clone.ShowPeaks()
                    #     Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetRangeUser(0, 360)
                    # except:
                    #     print("".join([color.RED, "Error in SVD (TSVDUnfold):\n", str(traceback.format_exc()), color.END]))
                    # ###################################################################
                    # ##==========##      (Original) SVD Unfolded Fit      ##==========##
                    # ###################################################################
                    


                    
                    ###################################################################
                    ##==========##       (Original) Bin-by-Bin Fit       ##==========##
                    ###################################################################
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])], 2, 0.15)
                    # Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])], 1, 0.15)
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])] = Bin_Unfolded[(out_print_main_binned, "Norm")].Clone()
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Brown),"]{Bin-By-Bin} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetTitle("")
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetTitle(str(Bin_Unfolded[(out_print_main_binned, "Norm")].GetXaxis().GetTitle()).replace("(REC)", ""))
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetRangeUser(0, 360)
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
#                     A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Bin_Unfolded["".join([str(out_print_main_binned), "extra"])])
                    if(not extra_function_terms):
                        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Bin_Unfolded["".join([str(out_print_main_binned), "extra"])])
                    else:
                        # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(Bin_Unfolded["".join([str(out_print_main_binned), "extra"])])
                        A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Bin_Unfolded["".join([str(out_print_main_binned), "extra"])])
                    # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
                    # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
                    # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
                    # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
                    # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
                    # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
                    # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].Fit(Unfolded_Fit_Function, "RQ")

                    A_Unfold,   B_Unfold,   C_Unfold   = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    A_Unfold_E, B_Unfold_E, C_Unfold_E = Unfolded_Fit_Function.GetParError(0),  Unfolded_Fit_Function.GetParError(1),  Unfolded_Fit_Function.GetParError(2)
                    Parameter_List_Unfold_Methods["Bin"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, A_Unfold_E, B_Unfold, B_Unfold_E, C_Unfold, C_Unfold_E, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])
                        

                    statbox_move(Histogram=Bin_Unfolded["".join([str(out_print_main_binned), "extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)#, Print_Method="norm"):
                    # Unfolded_C_clone.ShowPeaks()
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetRangeUser(0, 360)
                    ###################################################################
                    ##==========##       (Original) Bin-by-Bin Fit       ##==========##
                    ###################################################################
                    
                    
                    # for name in Parameter_List_Unfold_Methods:
                    #     print("".join([str(name), ":\n", str(Parameter_List_Unfold_Methods[name]), "\n================================================================\n"]))

            except:
                print("".join([color.BOLD, color.RED, "ERROR IN UNFOLDING:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))



##===============##     Unfolding Histogram Procedure     ##===============##
#############################################################################





print("".join(["Total: ", str(count)]))




































BIN_SEARCH = []
for BIN in Q2_xB_Bin_List:
    BIN_SEARCH.append("".join(["Q2_y_Bin_", str(BIN) if(str(BIN) not in ['0', 0]) else "All", ")"]))

         
# Draw_2D_Histograms_Simple
for ii in rdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        # print("out_print_main =", out_print_main)
        out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str = out_print_str.replace("_smeared", "")
        out_print_str = out_print_str.replace("'smear'",  "Smear")
        SEARCH = []
        for BIN in BIN_SEARCH:
            SEARCH.append(str(BIN) in str(out_print_str))
            if(str(BIN) in str(out_print_str)):
                break
        if(True in SEARCH):
            List_of_All_Histos_For_Unfolding[out_print_str] = rdf.Get(out_print_main)

            
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName())
    if("Normal_2D" in out_print_main):
        # print("out_print_main =", out_print_main)
        out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str = out_print_str.replace("_smeared", "")
        out_print_str = out_print_str.replace("'smear'",  "Smear")
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
        out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Skip", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"))
        out_print_str = out_print_str.replace("_smeared", "")
        out_print_str = out_print_str.replace("'smear'",  "Smear")
        SEARCH = []
        for BIN in BIN_SEARCH:
            SEARCH.append(str(BIN) in str(out_print_str))
            if(str(BIN) in str(out_print_str)):
                break
        if(True in SEARCH):
            List_of_All_Histos_For_Unfolding[out_print_str] = gdf.Get(out_print_main)

            
final_count = 0
print("\n\n")
for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
    if("Par" in str(List_of_All_Histos_For_Unfolding_ii)):
        print("\n", str(List_of_All_Histos_For_Unfolding_ii))
# print("\n\n\nList_of_All_Histos_For_Unfolding =\n", List_of_All_Histos_For_Unfolding)
    final_count += 1
print("\n\n")

print("final_count =", final_count)

count_of_images = 0



Smearing_final_list = ["''", "Smear"]
if(Smearing_Options not in ["no_smear", "both"]):
    Smearing_final_list = ["Smear"]
elif(Smearing_Options in ["no_smear"]):
    Smearing_final_list = ["''"]
elif(Smearing_Options in ["both"]):
    Smearing_final_list = ["''", "Smear"]
    
    
# Method_Type_List = ["Data", "Response", "Bin", "RooUnfold_bayes", "RooUnfold_svd", "rdf", "mdf", "gdf"]
Method_Type_List = ["Data", "Response", "Bin", "Bayesian", "SVD", "rdf", "mdf", "gdf"]

Pars_Canvas, Histo_Pars_VS_Z, Histo_Pars_VS_PT, Pars_Legends = {}, {}, {}, {}
for BIN in Q2_xB_Bin_List:
    BIN_NUM = int(BIN) if(str(BIN) not in ["0"]) else "All"
    z_pT_Bin_Range = 42 if(str(BIN_NUM) in ["2"]) else 36 if(str(BIN_NUM) in ["4", "5", "9", "10"]) else 35 if(str(BIN_NUM) in ["1", "3"]) else 30 if(str(BIN_NUM) in ["6", "7", "8", "11"]) else 25 if(str(BIN_NUM) in ["13", "14"]) else 20 if(str(BIN_NUM) in ["12", "15", "16", "17"]) else 0
    for smear in Smearing_final_list:
        HISTO_NAME = "".join(["(1D)_(Data_Type)_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_All)_(phi_t)"])
        
        # for Multi_Dim in ["Off", "Only", "Q2_y", "z_pT"]:
        for Multi_Dim in ["Off", "Only"]:
            if((BIN_NUM not in ["All"]) and (Multi_Dim in ["Off", "Only"])):
                for method in Method_Type_List:
                    if((method in ["RooUnfold_svd", "SVD", "Response"]) and (Multi_Dim not in ["Off"])):
                        continue
                    for Orientation in ["pT_z", "z_pT"]:
                        try:
                            z_pT_Images_Together(Histogram_List_All=List_of_All_Histos_For_Unfolding,   Default_Histo_Name=HISTO_NAME, Method=method,    Q2_Y_Bin=BIN_NUM,                                     Multi_Dim_Option=Multi_Dim, Plot_Orientation=Orientation)
                        except Exception as e:
                            print("".join([color.BOLD, color.RED, "ERROR IN z_pT_Images_Together():\n",   color.END, color.RED, str(traceback.format_exc()), color.END]))
            for z_pT_Bin in range(0, z_pT_Bin_Range + 1, 1):
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
                    
                print("")
                print("BIN_NUM    =", BIN_NUM)
                print("HISTO_NAME =", HISTO_NAME)
                print("Multi_Dim  =", Multi_Dim)
                print("z_pT_Bin   =", z_pT_Bin)
                
                try:
                    Large_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding,    Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [0]) else "All", Multi_Dim_Option=Multi_Dim)
                except Exception as e:
                    print("".join([color.BOLD, color.RED, "ERROR IN Large_Individual_Bin_Images():\n",    color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    Unfolded_Individual_Bin_Images(Histogram_List_All=List_of_All_Histos_For_Unfolding, Default_Histo_Name=HISTO_NAME, Q2_Y_Bin=BIN_NUM, Z_PT_Bin=z_pT_Bin if(z_pT_Bin not in [0]) else "All", Multi_Dim_Option=Multi_Dim)
                except Exception as e:
                    print("".join([color.BOLD, color.RED, "ERROR IN Unfolded_Individual_Bin_Images():\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                
        
        if(str(BIN_NUM) not in ["All", "0"]):
            # for Variable       in ["phi_t",     "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_z_pT_Bin_y_bin_phi_t"]:
            for Variable       in ["phi_t",     "Multi_Dim_z_pT_Bin_y_bin_phi_t"]:
                for Parameter  in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
                    for Method in ["Bin",       "Bayesian",  "SVD",        "gdf"]:
                        if(("Multi_Dim" in str(Variable)) and (str(Method) in ["SVD"])):
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
                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z]      = ROOT.TLegend(0.7, 0.1, 0.9, 0.3)
                        if(str(PAR_HISTO_MASTER_NAME_VS_PT) not in Pars_Legends):
                            Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT]     = ROOT.TLegend(0.7, 0.1, 0.9, 0.3)

                        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
                            if(((BIN_NUM in [1]) and (z_pT_Bin in [28, 34, 35])) or ((BIN_NUM in [2]) and (z_pT_Bin in [28, 35, 41, 42])) or ((BIN_NUM in [3]) and (z_pT_Bin in [28, 35])) or ((BIN_NUM in [4]) and (z_pT_Bin in [6, 36])) or ((BIN_NUM in [5]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [6]) and (z_pT_Bin in [30])) or ((BIN_NUM in [7]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [9]) and (z_pT_Bin in [36])) or ((BIN_NUM in [10]) and (z_pT_Bin in [30, 36])) or ((BIN_NUM in [11]) and (z_pT_Bin in [24, 30])) or ((BIN_NUM in [13, 14]) and (z_pT_Bin in [25])) or ((BIN_NUM in [15, 16, 17]) and (z_pT_Bin in [20]))):
                                continue
                            PAR_FIND_NAME = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_", str(z_pT_Bin), ")_(", str(Variable), ")"])

                            Z_BIN_VALUE   = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][1], 3)
                            PT_BIN_VALUE  = round(Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][1], 3)
                            Z_BIN         = str(Z_BIN_VALUE)
                            PT_BIN        = str(PT_BIN_VALUE)

                            Z_BIN_WIDTH   = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][0][0])/2, 3)
                            PT_BIN_WIDTH  = round((Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][2] - Find_Q2_y_z_pT_Bin_Stats(BIN_NUM, z_pT_Bin)[1][1][0])/2, 3)

                            PAR_FIND_NAME        = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_pT_Bin_",      str(z_pT_Bin), ")_(", str(Variable), ")"])
                            PAR_HISTO_NAME_VS_Z  = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(z_Bin_Center_",  str(PT_BIN),   ")_(", str(Variable), ")_VS_Z"])
                            PAR_HISTO_NAME_VS_PT = "".join(["(", str(Parameter), ")_(", str(Method), ")_(SMEAR=", str(smear), ")_(Q2_y_Bin_", str(BIN_NUM), ")_(pT_Bin_Center_", str(Z_BIN),    ")_(", str(Variable), ")_VS_PT"])

                            try:
                                PARAMETER_TO_ADD, PAR_ERROR_TO_ADD = List_of_All_Histos_For_Unfolding[str(PAR_FIND_NAME)]
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN GETTING THE FIT PARAMETERS FOR: ", color.END, str(PAR_FIND_NAME), "\n", color.RED, str(traceback.format_exc()), color.END]))
                                continue
                                
                            if((PT_BIN != LAST_PT_BIN) and (Z_BIN == LAST_Z_BIN)):
                                LAST_PT_BIN       = PT_BIN
                                PT_BIN_COLOR     += 1
                                if(PT_BIN_COLOR in [5, 8]):
                                    PT_BIN_COLOR += 1
                                if(PT_BIN_COLOR in [9]):
                                    PT_BIN_COLOR  = 28
                                if(PT_BIN_COLOR in [29]):
                                    PT_BIN_COLOR  = 30
                            if((Z_BIN  != LAST_Z_BIN)):
                                LAST_Z_BIN        = Z_BIN
                                LAST_PT_BIN       = PT_BIN
                                Z_BIN_COLOR      += 1
                                if(Z_BIN_COLOR in [5, 8]):
                                    Z_BIN_COLOR  += 1
                                if(Z_BIN_COLOR in [9]):
                                    Z_BIN_COLOR   = 28
                                if(Z_BIN_COLOR in [29]):
                                    Z_BIN_COLOR   = 30
                                PT_BIN_COLOR      = 2
                                
                            if(str(PAR_HISTO_NAME_VS_Z)  not in Histo_Pars_VS_Z):
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z]   = ROOT.TGraphErrors()
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs z with #color[",       str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}}}; z; Parameter ",           str(Parameter).replace("Fit_Par_", "")]))
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineColor(PT_BIN_COLOR)
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerColor(PT_BIN_COLOR)
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerStyle(33)
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetMarkerSize(2)
                                Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetLineWidth(1)
                                
                                Histo_Pars_VS_Z[PAR_HISTO_MASTER_NAME_VS_Z].Add(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z])
                                Pars_Legends[PAR_HISTO_MASTER_NAME_VS_Z].AddEntry(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z],    "".join(["#color[", str(PT_BIN_COLOR), "]{P_{T} Bin Centered at ", str(PT_BIN), "}"]), "lep")
                                
                            if(str(PAR_HISTO_NAME_VS_PT) not in Histo_Pars_VS_PT):
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT] = ROOT.TGraphErrors()
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetTitle("".join(["#splitline{", str(MASTER_TITLE), "}{#scale[0.75]{Plotting vs P_{T} with #color[", str(Z_BIN_COLOR), "]{z Bin Centered at ",     str(Z_BIN),   "}}}; P_{T} [GeV]; Parameter ", str(Parameter).replace("Fit_Par_", "")]))
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineColor(Z_BIN_COLOR)
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerColor(Z_BIN_COLOR)
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerStyle(33)
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetMarkerSize(2)
                                Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetLineWidth(1)
                                
                                Histo_Pars_VS_PT[PAR_HISTO_MASTER_NAME_VS_PT].Add(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT])
                                Pars_Legends[PAR_HISTO_MASTER_NAME_VS_PT].AddEntry(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT], "".join(["#color[", str(Z_BIN_COLOR),  "]{z Bin Centered at ",     str(Z_BIN),  "}"]), "lep")
                                
                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPoint(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN(),              Z_BIN_VALUE,  PARAMETER_TO_ADD)
                            Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].SetPointError(Histo_Pars_VS_Z[PAR_HISTO_NAME_VS_Z].GetN()     - 1, Z_BIN_WIDTH,  PAR_ERROR_TO_ADD)
                            
                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPoint(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN(),          PT_BIN_VALUE, PARAMETER_TO_ADD)
                            Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].SetPointError(Histo_Pars_VS_PT[PAR_HISTO_NAME_VS_PT].GetN() - 1, PT_BIN_WIDTH, PAR_ERROR_TO_ADD)


for ii in Histo_Pars_VS_Z:
    Pars_Canvas[ii] = ROOT.TCanvas(str(ii), str(ii), 1200, 1100)
    # Pars_Canvas[ii].Draw()
    Histo_Pars_VS_Z[ii].Draw("APL same")
    if(type(Histo_Pars_VS_Z[ii]) is type(ROOT.TMultiGraph())):
        Pars_Legends[ii].Draw()
        
for jj in Histo_Pars_VS_PT:
    Pars_Canvas[jj] = ROOT.TCanvas(str(jj), str(jj), 1200, 1100)
    # Pars_Canvas[jj].Draw()
    Histo_Pars_VS_PT[jj].Draw("APL same")
    if(type(Histo_Pars_VS_PT[jj]) is type(ROOT.TMultiGraph())):
        Pars_Legends[jj].Draw()

for CanvasPar_Name in Pars_Canvas:
    Save_Name_Pars = str(CanvasPar_Name).replace(".", "_")
    Save_Name_Pars = str(Save_Name_Pars).replace("(", "")
    Save_Name_Pars = str(Save_Name_Pars).replace(")", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("SMEAR=", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("''", "")
    Save_Name_Pars = str(Save_Name_Pars).replace("__", "_")
    
    Save_Name_Pars = "".join([str(Save_Name_Pars), File_Save_Format])
    if(Saving_Q):
        Pars_Canvas[CanvasPar_Name].SaveAs(Save_Name_Pars)
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name_Pars), color.END]))











































# if(False):

#     print("".join([color.BOLD, color.GREEN, "\n\n\nDone Creating Unfolded Histograms (Now saving...)\n", color.END]))


#     for Canvas_name in Unfolded_Canvas:
#         if("cd_upper" not in str(Canvas_name) and "cd_lower" not in str(Canvas_name)):
#             Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), str(File_Save_Format)])
#             if("smear" in str(Canvas_name)):
#                 Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), "_Smeared", str(File_Save_Format)])

#             Save_Name = Save_Name.replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]), "")
#             Save_Name = Save_Name.replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]), "")
#             Save_Name = Save_Name.replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))"]), "")
#             Save_Name = Save_Name.replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "_smeared'-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))"]), "")
#             Save_Name = Save_Name.replace("Smear-Type=''", "")
#             Save_Name = Save_Name.replace("Smear-Type='smear'", "")
#             Save_Name = str(str(Save_Name.replace("(", "")).replace(")", "").replace(", ", "_")).replace("'", "")
#             Save_Name = str(Save_Name.replace("_Data-Type=DataFrame_Type", "")).replace("extra", "_Unfolded_Histos")
#             Save_Name = str(Save_Name.replace("__", "_"))
#             Save_Name = str(Save_Name.replace("Histo-Group=", ""))
#             Save_Name = str(Save_Name.replace("Data-", ""))
#             Save_Name = str(Save_Name.replace("z-PT-Bin=", "_z_pT_Bin_"))
#             Save_Name = str(Save_Name.replace("Q2-xB-Bin=", "Q2_xB_Bin_"))
#             Save_Name = str(Save_Name.replace("".join(["Binning-Type=", str(Binning_Method).replace("_", ""), "-["]) , "_")).replace("]", "")
#             Save_Name = str(Save_Name.replace("Q2-y-Bin=", "Q2_y_Bin_"))
#             Save_Name = str(Save_Name.replace("".join(["Binning-Type=y_bin-["]) , "_")).replace("]", "")
#             Save_Name = str(Save_Name.replace("_Cut=cut_Complete_SIDIS", ""))
#             Save_Name = Save_Name.replace("__", "_")

#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0_MaxBin=1.05_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0_MaxBin=1.05_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0_MaxBin=1.05", "")

#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0.11944_MaxBin=0.73056_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0.11944_MaxBin=0.73056_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.11944_MaxBin=0.73056", "")

#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0.08977_MaxBin=0.82643_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=0.08977_MaxBin=0.82643_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.08977_MaxBin=0.82643", "")

#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=1.4805_MaxBin=11.8705_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=20_MinBin=1.4805_MaxBin=11.8705_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5"]), "")
#             Save_Name = Save_Name.replace("-[NumBins=20_MinBin=1.4805_MaxBin=11.8705", "")

#             Save_Name = Save_Name.replace("Q2_xB_Bin_All_z_pT_Bin_All_1D_Var-D1=", "All_Events_")

#             Save_Name = Save_Name.replace("".join(["_smeared-[NumBins=483_MinBin=-1.5_MaxBin=481.5_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=483_MinBin=-1.5_MaxBin=481.5_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")

#             Save_Name = Save_Name.replace("".join(["_smeared-[NumBins=195_MinBin=-1.5_MaxBin=193.5_Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#             Save_Name = Save_Name.replace("".join(["-[NumBins=195_MinBin=-1.5_MaxBin=193.5_Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")

#             Save_Name = Save_Name.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#             Save_Name = Save_Name.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#             Save_Name = Save_Name.replace("_smeared-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#             Save_Name = Save_Name.replace("-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#             Save_Name = Save_Name.replace("_smeared-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#             Save_Name = Save_Name.replace("-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#             Save_Name = Save_Name.replace("_smeared-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")
#             Save_Name = Save_Name.replace("-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")

#             Save_Name = Save_Name.replace("Q2_y_Bin_All_z_pT_Bin_All_1D_", "")
#             Save_Name = Save_Name.replace("Q2_y_Bin_All_z_pT_Bin_All_1D",  "")

#             if((str(Save_Name).find("-[NumBins")) != -1):
#                 Save_Name = str(Save_Name).replace(str(Save_Name).replace(str(Save_Name)[:(str(Save_Name).find("-[NumBins"))], ""), "".join(["_Unfolded_Histos" if("_Unfolded_Histos" in Save_Name) else "", str(File_Save_Format)]))

#             Save_Name = Save_Name.replace("Var-D1=", "")
#             Save_Name = Save_Name.replace("__", "_")

#             Save_Name = str(Save_Name.replace("phi_t", "phi_h"))

#             Save_Name = Save_Name.replace("_phi_hSmeared", "_phi_h_Smeared")
#             Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))

#             if(("smear" in str(Canvas_name)) and ("_Smeared" not in str(Save_Name))):
#                 Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Smeared", str(File_Save_Format)]))

#             # if(extra_function_terms and "phi_h" in str(Save_Name)):
#             if(extra_function_terms):
#                 Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))

#             if("y" in Binning_Method):
#                 Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
#             if(Sim_Test):
#                 Save_Name = "".join(["Sim_Test_", Save_Name])
                
                
#             Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
#             Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
#             Save_Name = Save_Name.replace("_.png",                ".png")
#             Save_Name = Save_Name.replace("__",                   "_")
#             if(Saving_Q):
#                 Unfolded_Canvas[Canvas_name].SaveAs(Save_Name)
#             count_of_images += 1
#             print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))

#     if(Saving_Q):
#         print("".join([color.BOLD, color.GREEN, "\n\nDONE SAVING INDIVIDUAL PLOTS\n", color.END]))
#     else:
#         print("".join([color.BOLD, color.RED, "\nNOT SAVING INDIVIDUAL PLOTS\n", color.END]))



#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##

#     Smearing_final_list = ["", "smear"]
#     if(Smearing_Options not in ["no_smear", "both"]):
#         Smearing_final_list = ["smear"]
#     elif(Smearing_Options in ["no_smear"]):
#         Smearing_final_list = [""]
#     elif(Smearing_Options in ["both"]):
#         Smearing_final_list = ["", "smear"]


#     # Smearing_final_list = ["smear"]
    
#     if("y_bin" not in Binning_Method):
#         print("".join([color.BOLD, color.GREEN, "\n\nDone with main Unfolded Histograms (Now getting parameter plots...)\n", color.END]))
#         Canvas_Parameters_List, Histo_Par_A_z, Histo_Par_B_z, Histo_Par_C_z, Histo_Par_A_pT, Histo_Par_B_pT, Histo_Par_C_pT, Par_Legends = {}, {}, {}, {}, {}, {}, {}, {}
#         # for Method in ["Bayes", "SVD", "Bin"]:
#         for Method in ["Bayes", "Bin"]:
#             for smearing_par in Smearing_final_list:
#                 z_value_Start, pT_value_Start = 1, 0
#                 try:
#                     for bin_ii in Parameter_List_Unfold_Methods[Method]:
#                         Q2_xB_Bin, z_pT_Bin, Par_A, Par_A_Error, Par_B, Par_B_Error, Par_C, Par_C_Error, Smearing_Title = bin_ii
#                         if((0 in [Q2_xB_Bin, z_pT_Bin]) or ("mear" in smearing_par and "mear" not in Smearing_Title) or ("mear" not in smearing_par and "mear" in Smearing_Title)):
#                             continue
#                         z_value,       pT_value       = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Default")
#                         z_value_title, pT_value_title = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Title")

#                         if("Error" in [z_value, pT_value]):
#                             print("".join([color.BOLD, color.RED, "ERROR IN Q2-xB Bin ",  str(Q2_xB_Bin), " --- z-pT Bin ",  str(z_pT_Bin), color.END]))
#                             print("".join(["z_value = ", str(z_value), "\tpT_value = ", str(pT_value)]))

#                         Histo_Name_z  = "".join([str(pT_value_title), "_Unfold_", str(Method), "_Q2_xB_Bin_", str(Q2_xB_Bin), "".join(["_", str(Smearing_Title)]) if("" != Smearing_Title) else ""])
#                         Histo_Name_pT = "".join([str(z_value_title),  "_Unfold_", str(Method), "_Q2_xB_Bin_", str(Q2_xB_Bin), "".join(["_", str(Smearing_Title)]) if("" != Smearing_Title) else ""])
#                         Unfolding_Title_Name = "bin-by-bin" if(Method in ["Bin", "bin", "bbb"]) else "Bayesian" if(Method in ["Bayes", "bayes", "bayesian"]) else str(Method)


#                         Title_Q2_xB_Bin = "".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)])
#                         Title_Line_1    = "".join(["(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{PARAMETER}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}"])

#                         Title_z_Line_3  = "".join([root_color.Bold, "{P_{T} Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), " [GeV]"])
#                         Title_pT_Line_3 = "".join([root_color.Bold, "{z Bin:} ",     str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title"))])

#                         Title_z_All     = "".join(["#splitline{#splitline{", str(Title_Line_1), "}{", str(Title_Q2_xB_Bin), "}}{", str(Title_z_Line_3),  "}; z; PARAMETER"])
#                         Title_pT_All    = "".join(["#splitline{#splitline{", str(Title_Line_1), "}{", str(Title_Q2_xB_Bin), "}}{", str(Title_pT_Line_3), "}; P_{T} [GeV]; PARAMETER"])

#                         # try:
#                         #     Histo_Par_A_z[Histo_Name_z]
#                         # except:
#                         #     Histo_Par_A_z[Histo_Name_z] = ROOT.TGraph()
#                         #     Histo_Par_A_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_A"]))
#                         #     Histo_Par_A_z[Histo_Name_z].SetTitle(str(Title_z_All).replace("PARAMETER", "Parameter A"))
#                         try:
#                             Histo_Par_B_z[Histo_Name_z]
#                         except:
#                             # Histo_Par_B_z[Histo_Name_z] = ROOT.TGraph()
#                             Histo_Par_B_z[Histo_Name_z] = ROOT.TGraphErrors()
#                             Histo_Par_B_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_B"]))
#                             Histo_Par_B_z[Histo_Name_z].SetTitle(str(Title_z_All).replace("PARAMETER", "Parameter B"))
#                             # Histo_Par_B_z[Histo_Name_z].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter B}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{P_{T} Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), " [GeV]}; z; Parameter B"]))
#                         try:
#                             Histo_Par_C_z[Histo_Name_z]
#                         except:
#                             # Histo_Par_C_z[Histo_Name_z] = ROOT.TGraph()
#                             Histo_Par_C_z[Histo_Name_z] = ROOT.TGraphErrors()
#                             Histo_Par_C_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_C"]))
#                             Histo_Par_C_z[Histo_Name_z].SetTitle(str(Title_z_All).replace("PARAMETER", "Parameter C"))
#                             # Histo_Par_C_z[Histo_Name_z].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter C}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{P_{T} Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), " [GeV]}; z; Parameter C"]))

#                         # try:
#                         #     Histo_Par_A_pT[Histo_Name_pT]
#                         # except:
#                         #     Histo_Par_A_pT[Histo_Name_pT] = ROOT.TGraph()
#                         #     Histo_Par_A_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT),  "_Par_A"]))
#                         #     Histo_Par_A_pT[Histo_Name_pT].SetTitle(str(Title_pT_All).replace("PARAMETER", "Parameter A"))
#                         try:
#                             Histo_Par_B_pT[Histo_Name_pT]
#                         except:
#                             # Histo_Par_B_pT[Histo_Name_pT] = ROOT.TGraph()
#                             Histo_Par_B_pT[Histo_Name_pT] = ROOT.TGraphErrors()
#                             Histo_Par_B_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT), "_Par_B"]))
#                             Histo_Par_B_pT[Histo_Name_pT].SetTitle(str(Title_pT_All).replace("PARAMETER", "Parameter B"))
#                             # Histo_Par_B_pT[Histo_Name_pT].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter B}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{z Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title")), "}; P_{T} [GeV]; Parameter B"]))
#                         try:
#                             Histo_Par_C_pT[Histo_Name_pT]
#                         except:
#                             # Histo_Par_C_pT[Histo_Name_pT] = ROOT.TGraph()
#                             Histo_Par_C_pT[Histo_Name_pT] = ROOT.TGraphErrors()
#                             Histo_Par_C_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT), "_Par_C"]))
#                             Histo_Par_C_pT[Histo_Name_pT].SetTitle(str(Title_pT_All).replace("PARAMETER", "Parameter C"))
#                             # Histo_Par_C_pT[Histo_Name_pT].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter C}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{z Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title")), "}; P_{T} [GeV]; Parameter C"]))


#                         # print("\n============================================================================")
#                         # print("".join(["Histo_Par_B_z[Histo_Name_z].GetN()   = ", str(Histo_Par_B_z[Histo_Name_z].GetN())]))
#                         # print("".join(["Histo_Par_B_pT[Histo_Name_pT].GetN() = ", str(Histo_Par_B_pT[Histo_Name_pT].GetN())]))
#                         # print("".join(["Q2_xB_Bin = ", str(Q2_xB_Bin)]))
#                         # print("".join(["z_pT_Bin  = ", str(z_pT_Bin)]))
#                         # print("".join(["z_value   = ", str(round(z_value,  3))]))
#                         # print("".join(["pT_value  = ", str(round(pT_value, 3))]))
#                         # # print("".join(["Par_B     = ", str(Par_B)]))
#                         # # print("".join(["Par_C     = ", str(Par_C)]))
#                         # print("============================================================================\n")

#                         # if((z_value_Start  > z_value)  and (z_value  != z_value_Start)):
#                         #     z_value_Start  = z_value
#                         # Histo_Par_A_z[Histo_Name_z].SetPoint(Histo_Par_A_z[Histo_Name_z].GetN(), z_value, Par_A)
#                         Histo_Par_B_z[Histo_Name_z].SetPoint(Histo_Par_B_z[Histo_Name_z].GetN(), z_value, Par_B)
#                         Histo_Par_B_z[Histo_Name_z].SetPointError(Histo_Par_B_z[Histo_Name_z].GetN() - 1, 0, Par_B_Error)
#                         Histo_Par_C_z[Histo_Name_z].SetPoint(Histo_Par_C_z[Histo_Name_z].GetN(), z_value, Par_C)
#                         Histo_Par_C_z[Histo_Name_z].SetPointError(Histo_Par_C_z[Histo_Name_z].GetN() - 1, 0, Par_C_Error)

#                         # if((pT_value_Start < pT_value) and (pT_value != pT_value_Start)):
#                         #     pT_value_Start = pT_value
#                         # Histo_Par_A_pT[Histo_Name_pT].SetPoint(Histo_Par_A_pT[Histo_Name_pT].GetN(), pT_value, Par_A)
#                         Histo_Par_B_pT[Histo_Name_pT].SetPoint(Histo_Par_B_pT[Histo_Name_pT].GetN(), pT_value, Par_B)
#                         Histo_Par_B_pT[Histo_Name_pT].SetPointError(Histo_Par_B_pT[Histo_Name_pT].GetN() - 1, 0, Par_B_Error)
#                         Histo_Par_C_pT[Histo_Name_pT].SetPoint(Histo_Par_C_pT[Histo_Name_pT].GetN(), pT_value, Par_C)
#                         Histo_Par_C_pT[Histo_Name_pT].SetPointError(Histo_Par_C_pT[Histo_Name_pT].GetN() - 1, 0, Par_C_Error)


#                     #################################################################################################################################################################################################################################################################################################################################################
#                     #################################################################################################################################################################################################################################################################################################################################################
#                     #################################################################################################################################################################################################################################################################################################################################################
#                     #################################################################################################################################################################################################################################################################################################################################################
#                     #################################################################################################################################################################################################################################################################################################################################################

#                     for Q2_xB_Bin_Name_ii in Q2_xB_Bin_List:
#                         if(Q2_xB_Bin_Name_ii in ['0']):
#                             continue
#                         Q2_xB_Bin_Name     = "".join(["Q2_xB_Bin_" if("y_bin" not in str(Binning_Method)) else "Q2_y_Bin_", str(Q2_xB_Bin_Name_ii)])
#                         Q2_xB_Bin          = int(Q2_xB_Bin_Name_ii)
#                         # Q2_xB_Bin          = 1 if("Q2_xB_Bin_1" in str(Q2_xB_Bin_Name)) else 2 if("Q2_xB_Bin_2" in str(Q2_xB_Bin_Name)) else 3 if("Q2_xB_Bin_3" in str(Q2_xB_Bin_Name)) else 4 if("Q2_xB_Bin_4" in str(Q2_xB_Bin_Name)) else 5 if("Q2_xB_Bin_5" in str(Q2_xB_Bin_Name)) else 6 if("Q2_xB_Bin_6" in str(Q2_xB_Bin_Name)) else 7 if("Q2_xB_Bin_7" in str(Q2_xB_Bin_Name)) else 8 if("Q2_xB_Bin_8" in str(Q2_xB_Bin_Name)) else 9 if("Q2_xB_Bin_9" in str(Q2_xB_Bin_Name)) else "ERROR"
#                         z_pT_Bin_Range     = 49 if(Q2_xB_Bin_Name_ii in ['1', '2', '3']) else 42 if(Q2_xB_Bin_Name_ii in ['4']) else 36 if(Q2_xB_Bin_Name_ii in ['5']) else 25 if(Q2_xB_Bin_Name_ii in ['6', '7']) else 20 if(Q2_xB_Bin_Name_ii in ['8']) else 1
#                         if("y_bin" in str(Binning_Method)):
#                             z_pT_Bin_Range = 49 if(Q2_xB_Bin_Name_ii in ['1', '2', '3', '7']) else 42 if(Q2_xB_Bin_Name_ii in ['4']) else 36 if(Q2_xB_Bin_Name_ii in ['5', '8', '9']) else 30 if(Q2_xB_Bin_Name_ii in ['6', '10', '11']) else 25 if(Q2_xB_Bin_Name_ii in ['13', '14']) else 20 if(Q2_xB_Bin_Name_ii in ['12', '15', '16', '17']) else 1

#                         canvas_name_z      = "".join(["z_Pars_",  str(Method), "_", str(Q2_xB_Bin_Name), "_Smeared" if("mear" in smearing_par) else ""])
#                         canvas_name_PT     = "".join(["PT_Pars_", str(Method), "_", str(Q2_xB_Bin_Name), "_Smeared" if("mear" in smearing_par) else ""])

#                         Histo_Name_z_list  = []
#                         Histo_Name_pT_list = []

#                         root_color_ii_z, root_color_ii_pT = 1, 1
#                         for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):                
#                             z_value,       pT_value       = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Default")
#                             z_value_title, pT_value_title = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Title")

#                             Histo_Name_z  = "".join([str(pT_value_title), "_Unfold_", str(Method), "_Q2_xB_Bin_" if("y_bin" not in str(Binning_Method)) else "_Q2_y_Bin_", str(Q2_xB_Bin), "_Smeared" if("mear" in smearing_par) else ""])
#                             Histo_Name_pT = "".join([str(z_value_title),  "_Unfold_", str(Method), "_Q2_xB_Bin_" if("y_bin" not in str(Binning_Method)) else "_Q2_y_Bin_", str(Q2_xB_Bin), "_Smeared" if("mear" in smearing_par) else ""])

#                             try:
#                                 Canvas_Parameters_List[canvas_name_z].GetName()

#                                 if(Histo_Name_z not in Histo_Name_z_list):

#                                     # print("".join(["Histo_Name_z_list = ", str(Histo_Name_z_list)]))
#                                     # print("".join(["Histo_Name_z      = ", str(Histo_Name_z)]))

#                                     Histo_Name_z_list.append(Histo_Name_z)

#                                     root_color_ii_z += 1
#                                     if(root_color_ii_z in [5, 10, 19]):
#                                         root_color_ii_z += 1

#                                     Histo_Par_B_z[Histo_Name_z].SetMarkerSize(2)
#                                     Histo_Par_B_z[Histo_Name_z].SetMarkerColor(root_color_ii_z)
#                                     Histo_Par_B_z[Histo_Name_z].SetLineColor(root_color_ii_z)
#                                     Histo_Par_B_z[Histo_Name_z].SetLineWidth(1)
#                                     Canvas_Parameters_List[TMulti_Graph_B_name_z].Add(Histo_Par_B_z[Histo_Name_z])
#                                     Par_Legends[TMulti_Graph_B_name_z].AddEntry(Histo_Par_B_z[Histo_Name_z], "".join(["#color[", str(root_color_ii_z), "]{", str(pT_value_title),"}"]), "lpE")
#                                     Histo_Par_C_z[Histo_Name_z].SetMarkerSize(2)
#                                     Histo_Par_C_z[Histo_Name_z].SetMarkerColor(root_color_ii_z)
#                                     Histo_Par_C_z[Histo_Name_z].SetLineColor(root_color_ii_z)
#                                     Histo_Par_C_z[Histo_Name_z].SetLineWidth(1)
#                                     Canvas_Parameters_List[TMulti_Graph_C_name_z].Add(Histo_Par_C_z[Histo_Name_z])
#                                     Par_Legends[TMulti_Graph_C_name_z].AddEntry(Histo_Par_C_z[Histo_Name_z], "".join(["#color[", str(root_color_ii_z), "]{", str(pT_value_title),"}"]), "lpE")

#                             except:
#                                 Canvas_Parameters_List[canvas_name_z]          = Canvas_Create(Name=canvas_name_z,  Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)
#                                 TMulti_Graph_B_name_z, TMulti_Graph_B_name_PT  = "".join([str(canvas_name_z), "_TMultiGraph_B"]), "".join([str(canvas_name_PT), "_TMultiGraph_B"])
#                                 TMulti_Graph_C_name_z, TMulti_Graph_C_name_PT  = "".join([str(canvas_name_z), "_TMultiGraph_C"]), "".join([str(canvas_name_PT), "_TMultiGraph_C"])

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z]  = ROOT.TMultiGraph(TMulti_Graph_B_name_z,  "".join([str(str(Histo_Par_B_z[Histo_Name_z].GetTitle()).replace(str(z_value_title), "All Bins")).replace(" [GeV]", ""),   ";", str(Histo_Par_B_z[Histo_Name_z].GetXaxis().GetTitle()),   ";", str(Histo_Par_B_z[Histo_Name_z].GetYaxis().GetTitle())]))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z]  = ROOT.TMultiGraph(TMulti_Graph_C_name_z,  "".join([str(str(Histo_Par_C_z[Histo_Name_z].GetTitle()).replace(str(z_value_title), "All Bins")).replace(" [GeV]", ""),   ";", str(Histo_Par_C_z[Histo_Name_z].GetXaxis().GetTitle()),   ";", str(Histo_Par_C_z[Histo_Name_z].GetYaxis().GetTitle())]))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_z].GetTitle()).replace("0.55 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_z].GetTitle()).replace("0.55 - 0.7", "All Bins"))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_z].GetTitle()).replace("0.56 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_z].GetTitle()).replace("0.56 - 0.7", "All Bins"))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_z].GetTitle()).replace("0.6 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_z].GetTitle()).replace("0.6 - 0.7", "All Bins"))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_z].GetTitle()).replace("0.5 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_z].GetTitle()).replace("0.5 - 0.7", "All Bins"))

#                                 # print(str(Canvas_Parameters_List[TMulti_Graph_B_name_z].GetTitle()))

#                                 Par_Legends[TMulti_Graph_B_name_z] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#                                 Par_Legends[TMulti_Graph_B_name_z].SetNColumns(1)
#                                 Par_Legends[TMulti_Graph_B_name_z].SetBorderSize(0)
#                                 Par_Legends[TMulti_Graph_B_name_z].SetFillColor(0)
#                                 Par_Legends[TMulti_Graph_B_name_z].SetFillStyle(0)

#                                 Par_Legends[TMulti_Graph_C_name_z] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#                                 Par_Legends[TMulti_Graph_C_name_z].SetNColumns(1)
#                                 Par_Legends[TMulti_Graph_C_name_z].SetBorderSize(0)
#                                 Par_Legends[TMulti_Graph_C_name_z].SetFillColor(0)
#                                 Par_Legends[TMulti_Graph_C_name_z].SetFillStyle(0)

#                                 root_color_ii_z   = 1
#                                 Histo_Name_z_list.append(Histo_Name_z)

#                                 Histo_Par_B_z[Histo_Name_z].SetMarkerSize(2)
#                                 Histo_Par_B_z[Histo_Name_z].SetMarkerColor(root_color_ii_z)
#                                 Histo_Par_B_z[Histo_Name_z].SetLineColor(root_color_ii_z)
#                                 Histo_Par_B_z[Histo_Name_z].SetLineWidth(1)
#                                 Canvas_Parameters_List[TMulti_Graph_B_name_z].Add(Histo_Par_B_z[Histo_Name_z])
#                                 Par_Legends[TMulti_Graph_B_name_z].AddEntry(Histo_Par_B_z[Histo_Name_z], "".join(["#color[", str(root_color_ii_z), "]{", str(pT_value_title),"}"]), "lpE")
#                                 Histo_Par_C_z[Histo_Name_z].SetMarkerSize(2)
#                                 Histo_Par_C_z[Histo_Name_z].SetMarkerColor(root_color_ii_z)
#                                 Histo_Par_C_z[Histo_Name_z].SetLineColor(root_color_ii_z)
#                                 Histo_Par_C_z[Histo_Name_z].SetLineWidth(1)
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_z].Add(Histo_Par_C_z[Histo_Name_z])
#                                 Par_Legends[TMulti_Graph_C_name_z].AddEntry(Histo_Par_C_z[Histo_Name_z], "".join(["#color[", str(root_color_ii_z), "]{", str(pT_value_title),"}"]), "lpE")


#                             try:
#                                 Canvas_Parameters_List[canvas_name_PT].GetName()

#                                 if(Histo_Name_pT not in Histo_Name_pT_list):
#                                     Histo_Name_pT_list.append(Histo_Name_pT)

#                                     root_color_ii_pT += 1
#                                     if(root_color_ii_pT in [5, 10, 19]):
#                                         root_color_ii_pT += 1

#                                     Histo_Par_B_pT[Histo_Name_pT].SetMarkerSize(2)
#                                     Histo_Par_B_pT[Histo_Name_pT].SetMarkerColor(root_color_ii_pT)
#                                     Histo_Par_B_pT[Histo_Name_pT].SetLineColor(root_color_ii_pT)
#                                     Histo_Par_B_pT[Histo_Name_pT].SetLineWidth(1)
#                                     Canvas_Parameters_List[TMulti_Graph_B_name_PT].Add(Histo_Par_B_pT[Histo_Name_pT])
#                                     Par_Legends[TMulti_Graph_B_name_PT].AddEntry(Histo_Par_B_pT[Histo_Name_pT], "".join(["#color[", str(root_color_ii_pT), "]{", str(z_value_title),"}"]), "lpE")
#                                     Histo_Par_C_pT[Histo_Name_pT].SetMarkerSize(2)
#                                     Histo_Par_C_pT[Histo_Name_pT].SetMarkerColor(root_color_ii_pT)
#                                     Histo_Par_C_pT[Histo_Name_pT].SetLineColor(root_color_ii_pT)
#                                     Histo_Par_C_pT[Histo_Name_pT].SetLineWidth(1)
#                                     Canvas_Parameters_List[TMulti_Graph_C_name_PT].Add(Histo_Par_C_pT[Histo_Name_pT])
#                                     Par_Legends[TMulti_Graph_C_name_PT].AddEntry(Histo_Par_C_pT[Histo_Name_pT], "".join(["#color[", str(root_color_ii_pT), "]{", str(z_value_title),"}"]), "lpE")

#                             except:
#                                 Canvas_Parameters_List[canvas_name_PT]         = Canvas_Create(Name=canvas_name_PT, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)

#                                 TMulti_Graph_B_name_z, TMulti_Graph_B_name_PT  = "".join([str(canvas_name_z), "_TMultiGraph_B"]), "".join([str(canvas_name_PT), "_TMultiGraph_B"])
#                                 TMulti_Graph_C_name_z, TMulti_Graph_C_name_PT  = "".join([str(canvas_name_z), "_TMultiGraph_C"]), "".join([str(canvas_name_PT), "_TMultiGraph_C"])

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_PT] = ROOT.TMultiGraph(TMulti_Graph_B_name_PT, "".join([str(str(Histo_Par_B_pT[Histo_Name_pT].GetTitle()).replace(str(pT_value_title), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_B_pT[Histo_Name_pT].GetXaxis().GetTitle()), ";", str(Histo_Par_B_pT[Histo_Name_pT].GetYaxis().GetTitle())]))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_PT] = ROOT.TMultiGraph(TMulti_Graph_C_name_PT, "".join([str(str(Histo_Par_C_pT[Histo_Name_pT].GetTitle()).replace(str(pT_value_title), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_C_pT[Histo_Name_pT].GetXaxis().GetTitle()), ";", str(Histo_Par_C_pT[Histo_Name_pT].GetYaxis().GetTitle())]))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_PT].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_PT].GetTitle()).replace("0.05 - 0.2", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_PT].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_PT].GetTitle()).replace("0.05 - 0.2", "All Bins"))

#                                 Canvas_Parameters_List[TMulti_Graph_B_name_PT].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_B_name_PT].GetTitle()).replace("0.05 - 0.22", "All Bins"))
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_PT].SetTitle(str(Canvas_Parameters_List[TMulti_Graph_C_name_PT].GetTitle()).replace("0.05 - 0.22", "All Bins"))

#                                 Par_Legends[TMulti_Graph_B_name_PT] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#                                 Par_Legends[TMulti_Graph_B_name_PT].SetNColumns(1)
#                                 Par_Legends[TMulti_Graph_B_name_PT].SetBorderSize(0)
#                                 Par_Legends[TMulti_Graph_B_name_PT].SetFillColor(0)
#                                 Par_Legends[TMulti_Graph_B_name_PT].SetFillStyle(0)

#                                 Par_Legends[TMulti_Graph_C_name_PT] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#                                 Par_Legends[TMulti_Graph_C_name_PT].SetNColumns(1)
#                                 Par_Legends[TMulti_Graph_C_name_PT].SetBorderSize(0)
#                                 Par_Legends[TMulti_Graph_C_name_PT].SetFillColor(0)
#                                 Par_Legends[TMulti_Graph_C_name_PT].SetFillStyle(0)

#                                 root_color_ii_pT   = 1
#                                 Histo_Name_pT_list.append(Histo_Name_pT)

#                                 Histo_Par_B_pT[Histo_Name_pT].SetMarkerSize(2)
#                                 Histo_Par_B_pT[Histo_Name_pT].SetMarkerColor(root_color_ii_pT)
#                                 Histo_Par_B_pT[Histo_Name_pT].SetLineColor(root_color_ii_pT)
#                                 Histo_Par_B_pT[Histo_Name_pT].SetLineWidth(1)
#                                 Canvas_Parameters_List[TMulti_Graph_B_name_PT].Add(Histo_Par_B_pT[Histo_Name_pT])
#                                 Par_Legends[TMulti_Graph_B_name_PT].AddEntry(Histo_Par_B_pT[Histo_Name_pT], "".join(["#color[", str(root_color_ii_pT), "]{", str(z_value_title),"}"]), "lpE")
#                                 Histo_Par_C_pT[Histo_Name_pT].SetMarkerSize(2)
#                                 Histo_Par_C_pT[Histo_Name_pT].SetMarkerColor(root_color_ii_pT)
#                                 Histo_Par_C_pT[Histo_Name_pT].SetLineColor(root_color_ii_pT)
#                                 Histo_Par_C_pT[Histo_Name_pT].SetLineWidth(1)
#                                 Canvas_Parameters_List[TMulti_Graph_C_name_PT].Add(Histo_Par_C_pT[Histo_Name_pT])
#                                 Par_Legends[TMulti_Graph_C_name_PT].AddEntry(Histo_Par_C_pT[Histo_Name_pT], "".join(["#color[", str(root_color_ii_pT), "]{", str(z_value_title),"}"]), "lpE")




#                     for canvas_loop in Canvas_Parameters_List:
#                         if("_TMultiGraph" not in canvas_loop):
#                             print(canvas_loop)
#                             if("PT_Pars" in canvas_loop):
#                                 # Canvas_Parameters_List[canvas_loop].Draw()
#                                 Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=1, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].SetTitle(str(Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].GetTitle()).replace("0.5 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].Draw("APL* same")
#                                 Par_Legends[TMulti_Graph_B_name_PT].Draw("same")
#                                 Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=2, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].SetTitle(str(Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].GetTitle()).replace("0.5 - 0.7", "All Bins"))
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].Draw("APL* same")
#                                 Par_Legends[TMulti_Graph_C_name_PT].Draw("same")
#                             else:
#                                 # Canvas_Parameters_List[canvas_loop].Draw()
#                                 Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=1, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].SetTitle(str(Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].GetTitle()).replace("0.05 - 0.23", "All Bins"))
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].Draw("APL* same")
#                                 Par_Legends[TMulti_Graph_B_name_z].Draw("same")
#                                 Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=2, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].SetTitle(str(Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].GetTitle()).replace("0.05 - 0.23", "All Bins"))
#                                 Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].Draw("APL* same")
#                                 Par_Legends[TMulti_Graph_C_name_z].Draw("same")

#                 except:
#                     print("".join([color.BOLD, color.RED, "\nError in getting parameter plots with method: ", color.BLUE, str(Method), color.RED, "\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#         #             for name in Histo_Par_B_z:
#         #                 if(("".join(["Unfold_", str(Method)]) not in str(name)) or ("mear" in smearing_par and "mear" not in str(name)) or ("mear" not in smearing_par and "mear" in str(name))):
#         #                     continue
#         #                 Q2_xB_Bin_Name = "Q2_xB_Bin_1" if("Q2_xB_Bin_1" in str(name)) else "Q2_xB_Bin_2" if("Q2_xB_Bin_2" in str(name)) else "Q2_xB_Bin_3" if("Q2_xB_Bin_3" in str(name)) else "Q2_xB_Bin_4" if("Q2_xB_Bin_4" in str(name)) else "Q2_xB_Bin_5" if("Q2_xB_Bin_5" in str(name)) else "Q2_xB_Bin_6" if("Q2_xB_Bin_6" in str(name)) else "Q2_xB_Bin_7" if("Q2_xB_Bin_7" in str(name)) else "Q2_xB_Bin_8" if("Q2_xB_Bin_8" in str(name)) else "Q2_xB_Bin_9" if("Q2_xB_Bin_9" in str(name)) else "ERROR"
#         #                 canvas_name    = "".join(["PT_Pars_", str(Method), "_", str(Q2_xB_Bin_Name), "" if("Smeared" not in str(name) and "mear" not in smearing_par) else "_Smeared"])
#         #                 Bin_Range_str  = str(name.replace("".join(["_Unfold_", str(Method), "_", str(Q2_xB_Bin_Name)]), ""))
#         #                 Bin_Range_str  = str(Bin_Range_str).replace("_Smeared", "")
#         #                 try:
#         #                     Canvas_Parameters_List[canvas_name].GetName()
#         #                     root_color_ii += 1
#         #                     if(root_color_ii in [5, 10, 19]):
#         #                         root_color_ii += 1
#         #                 except:
#         #                     Canvas_Parameters_List[canvas_name] = Canvas_Create(Name=canvas_name, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)
#         #                     # Canvas_Parameters_List[canvas_name].Draw()
#         #                     TMulti_Graph_B_name = "".join([str(canvas_name), "_TMultiGraph_B"])
#         #                     TMulti_Graph_C_name = "".join([str(canvas_name), "_TMultiGraph_C"])
#         #                     Canvas_Parameters_List[TMulti_Graph_B_name] = ROOT.TMultiGraph(TMulti_Graph_B_name, "".join([str(str(Histo_Par_B_z[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_B_z[name].GetXaxis().GetTitle()), ";", str(Histo_Par_B_z[name].GetYaxis().GetTitle())]))
#         #                     Canvas_Parameters_List[TMulti_Graph_C_name] = ROOT.TMultiGraph(TMulti_Graph_C_name, "".join([str(str(Histo_Par_C_z[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_C_z[name].GetXaxis().GetTitle()), ";", str(Histo_Par_C_z[name].GetYaxis().GetTitle())]))
#         #                     Par_Legends[TMulti_Graph_B_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#         #                     Par_Legends[TMulti_Graph_B_name].SetNColumns(1)
#         #                     Par_Legends[TMulti_Graph_B_name].SetBorderSize(0)
#         #                     Par_Legends[TMulti_Graph_B_name].SetFillColor(0)
#         #                     Par_Legends[TMulti_Graph_B_name].SetFillStyle(0)

#         #                     Par_Legends[TMulti_Graph_C_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#         #                     Par_Legends[TMulti_Graph_C_name].SetNColumns(1)
#         #                     Par_Legends[TMulti_Graph_C_name].SetBorderSize(0)
#         #                     Par_Legends[TMulti_Graph_C_name].SetFillColor(0)
#         #                     Par_Legends[TMulti_Graph_C_name].SetFillStyle(0)

#         #                     root_color_ii = 1

#         #                 Histo_Par_B_z[name].SetMarkerSize(2)
#         #                 Histo_Par_B_z[name].SetMarkerColor(root_color_ii)
#         #                 Histo_Par_B_z[name].SetLineColor(root_color_ii)
#         #                 Histo_Par_B_z[name].SetLineWidth(1)
#         #                 Canvas_Parameters_List[TMulti_Graph_B_name].Add(Histo_Par_B_z[name])
#         #                 Par_Legends[TMulti_Graph_B_name].AddEntry(Histo_Par_B_z[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")
#         #                 Histo_Par_C_z[name].SetMarkerSize(2)
#         #                 Histo_Par_C_z[name].SetMarkerColor(root_color_ii)
#         #                 Histo_Par_C_z[name].SetLineColor(root_color_ii)
#         #                 Histo_Par_C_z[name].SetLineWidth(1)
#         #                 Canvas_Parameters_List[TMulti_Graph_C_name].Add(Histo_Par_C_z[name])
#         #                 Par_Legends[TMulti_Graph_C_name].AddEntry(Histo_Par_C_z[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")

#         #             root_color_ii = 1
#         #             for name in Histo_Par_B_pT:
#         #                 if(("".join(["Unfold_", str(Method)]) not in str(name)) or ("mear" in smearing_par and "mear" not in str(name)) or ("mear" not in smearing_par and "mear" in str(name))):
#         #                     continue
#         #                 Q2_xB_Bin_Name = "Q2_xB_Bin_1" if("Q2_xB_Bin_1" in str(name)) else "Q2_xB_Bin_2" if("Q2_xB_Bin_2" in str(name)) else "Q2_xB_Bin_3" if("Q2_xB_Bin_3" in str(name)) else "Q2_xB_Bin_4" if("Q2_xB_Bin_4" in str(name)) else "Q2_xB_Bin_5" if("Q2_xB_Bin_5" in str(name)) else "Q2_xB_Bin_6" if("Q2_xB_Bin_6" in str(name)) else "Q2_xB_Bin_7" if("Q2_xB_Bin_7" in str(name)) else "Q2_xB_Bin_8" if("Q2_xB_Bin_8" in str(name)) else "Q2_xB_Bin_9" if("Q2_xB_Bin_9" in str(name)) else "ERROR"
#         #                 canvas_name    = "".join(["z_Pars_", str(Method), "_", str(Q2_xB_Bin_Name), "" if("Smeared" not in str(name) and "mear" not in smearing_par) else "_Smeared"])
#         #                 Bin_Range_str  = str(name.replace("".join(["_Unfold_", str(Method), "_", str(Q2_xB_Bin_Name)]), ""))
#         #                 Bin_Range_str  = str(Bin_Range_str).replace("_Smeared", "")
#         #                 try:
#         #                     Canvas_Parameters_List[canvas_name].GetName()
#         #                     root_color_ii += 1
#         #                     if(root_color_ii in [5, 10, 19]):
#         #                         root_color_ii += 1
#         #                 except:
#         #                     Canvas_Parameters_List[canvas_name] = Canvas_Create(Name=canvas_name, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)
#         #                     # Canvas_Parameters_List[canvas_name].Draw()
#         #                     TMulti_Graph_B_name = "".join([str(canvas_name), "_TMultiGraph_B"])
#         #                     TMulti_Graph_C_name = "".join([str(canvas_name), "_TMultiGraph_C"])
#         #                     Canvas_Parameters_List[TMulti_Graph_B_name] = ROOT.TMultiGraph(TMulti_Graph_B_name, "".join([str(str(Histo_Par_B_pT[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_B_pT[name].GetXaxis().GetTitle()), ";", str(Histo_Par_B_pT[name].GetYaxis().GetTitle())]))
#         #                     Canvas_Parameters_List[TMulti_Graph_C_name] = ROOT.TMultiGraph(TMulti_Graph_C_name, "".join([str(str(Histo_Par_C_pT[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_C_pT[name].GetXaxis().GetTitle()), ";", str(Histo_Par_C_pT[name].GetYaxis().GetTitle())]))
#         #                     Par_Legends[TMulti_Graph_B_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#         #                     Par_Legends[TMulti_Graph_B_name].SetNColumns(1)
#         #                     Par_Legends[TMulti_Graph_B_name].SetBorderSize(0)
#         #                     Par_Legends[TMulti_Graph_B_name].SetFillColor(0)
#         #                     Par_Legends[TMulti_Graph_B_name].SetFillStyle(0)

#         #                     Par_Legends[TMulti_Graph_C_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
#         #                     Par_Legends[TMulti_Graph_C_name].SetNColumns(1)
#         #                     Par_Legends[TMulti_Graph_C_name].SetBorderSize(0)
#         #                     Par_Legends[TMulti_Graph_C_name].SetFillColor(0)
#         #                     Par_Legends[TMulti_Graph_C_name].SetFillStyle(0)

#         #                     root_color_ii = 1

#         #                 Histo_Par_B_pT[name].SetMarkerSize(2)
#         #                 Histo_Par_B_pT[name].SetMarkerColor(root_color_ii)
#         #                 Histo_Par_B_pT[name].SetLineColor(root_color_ii)
#         #                 Histo_Par_B_pT[name].SetLineWidth(1)
#         #                 Canvas_Parameters_List[TMulti_Graph_B_name].Add(Histo_Par_B_pT[name])
#         #                 Par_Legends[TMulti_Graph_B_name].AddEntry(Histo_Par_B_pT[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")
#         #                 Histo_Par_C_pT[name].SetMarkerSize(2)
#         #                 Histo_Par_C_pT[name].SetMarkerColor(root_color_ii)
#         #                 Histo_Par_C_pT[name].SetLineColor(root_color_ii)
#         #                 Histo_Par_C_pT[name].SetLineWidth(1)
#         #                 Canvas_Parameters_List[TMulti_Graph_C_name].Add(Histo_Par_C_pT[name])
#         #                 Par_Legends[TMulti_Graph_C_name].AddEntry(Histo_Par_C_pT[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")


#         #             for canvas_loop in Canvas_Parameters_List:
#         #                 if("_TMultiGraph" not in canvas_loop):
#         #                     # Canvas_Parameters_List[canvas_loop].Draw()
#         #                     Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=1, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#         #                     Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].Draw("APL* same")
#         #                     Par_Legends[TMulti_Graph_B_name].Draw("same")
#         #                     Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=2, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
#         #                     Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].Draw("APL* same")
#         #                     Par_Legends[TMulti_Graph_C_name].Draw("same")

#         #         except:
#         #             print("".join([color.BOLD, color.RED, "\nError in getting parameter plots with method: ", color.BLUE, str(Method), color.RED, "\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))



#         print("".join([color.BOLD, color.GREEN, "\n\nDone with getting parameter plots (Now Saving...)\n", color.END]))    
#         for ii in Canvas_Parameters_List:
#             if("TMultiGraph" not in str(ii) and File_Save_Format == ".png"):
#                 Saving_Name_Pars = "".join([str(ii), str(File_Save_Format)])

#                 Saving_Name_Pars = Saving_Name_Pars.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("_smeared-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("_smeared-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("_smeared-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")

#                 Saving_Name_Pars = str(Saving_Name_Pars.replace("phi_t", "phi_h"))
#                 Saving_Name_Pars = str(Saving_Name_Pars.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))

#                 # if(extra_function_terms and "phi_h" in str(Save_Name)):
#                 if(extra_function_terms):
#                     Saving_Name_Pars = str(Saving_Name_Pars).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))

#                 if("y" in Binning_Method):
#                     Saving_Name_Pars = Saving_Name_Pars.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
#                 if(Sim_Test):
#                     Saving_Name_Pars = "".join(["Sim_Test_", Saving_Name_Pars])

#                 Saving_Name_Pars = Saving_Name_Pars.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("_.png",                ".png")
#                 Saving_Name_Pars = Saving_Name_Pars.replace("__",                   "_")
                
#                 # print(Saving_Name_Pars)
#                 if(Saving_Q):
#                     Canvas_Parameters_List[ii].SaveAs(Saving_Name_Pars)
#                 else:
#                     Canvas_Parameters_List[ii].Draw()
#                 count_of_images += 1
#                 print("".join(["Saved: " if(Saving_Q) else "".join([color.RED, "Would be Saving: ", color.END]), color.BOLD, color.BLUE, str(Saving_Name_Pars), color.END]))
#     else:
#         print(color.RED, "\n\nNot Making Parameter Plots for y-binning yet (in developement)...\n\n", color.END)


#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##
#     ##=======================================================================================================================================================================================================##















#     if(count != 0 and Q2_xB_Bin_List != ['0']):
#     # if(count != 0):

#         print("".join([color.BOLD, color.BLUE, "\n\nStarting Combined Images...\n", color.END]))
#         Unfolded_Canvas_Test, Main_Unfolding_Images, Main_Final_Unfolding_Images = {}, {}, {}
#         for Q2_xB in Q2_xB_Bin_List:
#             Q2_xB_Bin = int(Q2_xB)
#             z_pT_Bin_Range = 0 if(Q2_xB_Bin in [0]) else 49 if(Q2_xB_Bin in [1, 2, 3]) else 42 if(Q2_xB_Bin in [4]) else 36 if(Q2_xB_Bin in [5]) else 25 if(Q2_xB_Bin in [6, 7]) else 20 if(Q2_xB_Bin in [8]) else 1
#             if("y_bin" in Binning_Method):
#                 # z_pT_Bin_Range = 0 if(Q2_xB_Bin in [0]) else 49 if(Q2_xB_Bin in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin in [4]) else 36 if(Q2_xB_Bin in [5, 8, 9, 11, 12]) else 30 if(Q2_xB_Bin in [6, 10]) else 25 if(Q2_xB_Bin in [13]) else 1
#                 z_pT_Bin_Range = 0 if(Q2_xB_Bin in [0]) else 49 if(Q2_xB_Bin in [1, 2, 3, 7]) else 42 if(Q2_xB_Bin in [4]) else 36 if(Q2_xB_Bin in [5, 8, 9]) else 30 if(Q2_xB_Bin in [6, 10, 11]) else 25 if(Q2_xB_Bin in [13, 14]) else 20 if(Q2_xB_Bin in [12, 15, 16, 17]) else 1


#             if(str(Q2_xB_Bin) not in Q2_xB_Bin_List):
#                 print("Skipping unselected Q2-xB Bin...")
#                 print("".join(["Bin ", str(Q2_xB_Bin), " is not in Q2_xB_Bin_List = " if("y_bin" in str(Binning_Method)) else " is not in Q2_y_Bin_List = ", str(Q2_xB_Bin_List)]))
#                 continue

#             # for DF_Current in [rdf, mdf, gdf]:
#             for DF_Current in [rdf]:
#                 for ii in DF_Current.GetListOfKeys():
#                     out_print = str(ii.GetName())
#                     Conditions_For_Histograms = []
#                     Conditions_For_Histograms.append("Normal_2D" in str(out_print))
#                     Conditions_For_Histograms.append(("cut_Complete_SIDIS" in str(out_print)) or  ("no_cut"       in str(out_print)   and (("gdf"         in str(out_print)) or  ("gen"         in str(out_print)))))
#                     Conditions_For_Histograms.append(("Var-D1='Q2'"        in str(out_print)  and ("Var-D2='xB'"  in str(out_print))) or  (("Var-D1='z'"  in str(out_print)) and ("Var-D2='pT'" in str(out_print))))
#                     Conditions_For_Histograms.append(((("Q2-xB-Bin=All"    in str(out_print)) or  ("Q2-y-Bin=All" in str(out_print))) and (("Var-D1='Q2'" in str(out_print)) and ("Var-D2='xB'" in str(out_print)))) or ((("".join(["Q2-xB-Bin=", str(Q2_xB_Bin), ","]) in str(out_print)) or ("".join(["Q2-y-Bin=", str(Q2_xB_Bin), ","]) in str(out_print))) and ("Var-D1='z" in str(out_print) and ("Var-D2='pT" in str(out_print)))))
#                     # Conditions_For_Histograms.append(("".join(["Q2-xB-Bin=", str(Q2_xB_Bin)]) in str(out_print)) and ("Var-D1='z" in str(out_print) and ("Var-D2='pT" in str(out_print))))
#                     # print(Conditions_For_Histograms)
#                     if(False not in Conditions_For_Histograms):
#                         Main_Unfolding_Images[out_print] = DF_Current.Get(out_print)
#                         z_pT_Bin = 0
#                         if(z_pT_Bin != 0 and (("Var-D1='Q2'" in str(out_print)) and ("Var-D2='xB'" in str(out_print)))):
#                             print("Testing Q2-xB bins...")
#                             break
#                         if("smear" in str(out_print)):
#                             print("smeared:")
#                             print(out_print)
#                         out_print_binned = out_print.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)]))
#                         out_print_binned = out_print.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D"]))

#                         try:
#                             if("3D" in str(type(Main_Unfolding_Images[out_print]))):
#                                 if(("Response_Matrix" in str(out_print)) and True):
#                                     bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetZaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetZaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsZ())
#                                     if(z_pT_Bin != 0):
#                                         Main_Unfolding_Images[out_print].GetZaxis().SetRange(bin_2D_0, bin_2D_1)
#                                     Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('yx')
#                                     Main_Final_Unfolding_Images[out_print_binned].SetName(str(Main_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])))
#                                     New_2D_Title = (str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
#                                     New_2D_Title = str(str(New_2D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
#                                     Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_2D_Title)
#                                 elif(("Normal_2D" in str(out_print)) and True):
#                                     bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsX())
#                                     if(z_pT_Bin != 0):
#                                         Main_Unfolding_Images[out_print].GetXaxis().SetRange(bin_2D_0, bin_2D_1)
#                                     if("Var-D1='z'" not in out_print_binned):
#                                         Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('yz')
#                                     else:
#                                         Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('zy')
#                                     Main_Final_Unfolding_Images[out_print_binned].SetName(str(Main_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])))
#                                     New_2D_Title = (str(str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("xy projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
#                                     New_2D_Title = str(str(New_2D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
#                                     if("z vs. P_{T}" in New_2D_Title):
#                                         New_2D_Title = New_2D_Title.replace("z vs. P_{T}", "P_{T} vs. z")
#                                     Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_2D_Title)
#                                 else:
#                                     bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsY())
#                                     if(z_pT_Bin != 0):
#                                         Main_Unfolding_Images[out_print].GetYaxis().SetRange(bin_2D_0, bin_2D_1)
#                                     New_2D_Title = (str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
#                                     Main_Unfolding_Images[out_print].SetTitle(New_2D_Title)
#                             elif("2D" in str(type(Main_Unfolding_Images[out_print]))):
#                                 if(("Response_Matrix" in str(out_print)) and True):
#                                     bin_1D_0, bin_1D_1 = Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsY())
#                                     Main_Final_Unfolding_Images[out_print_binned] = Main_Final_Unfolding_Images[out_print].ProjectionX(str(Main_Final_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])), bin_1D_0, bin_1D_1)
#                                     New_1D_Title = str(Main_Final_Unfolding_Images[out_print_binned].GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
#                                     New_1D_Title = str(str(New_1D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
#                                     Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_1D_Title)
#                         except:
#                             print("".join(["Failed...\n", color.RED, color.BOLD, "ERROR in 2D Plot Creation: \n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                     # elif(Conditions_For_Histograms[0] and Conditions_For_Histograms[1]):
#                     #     print(color.RED, "Failed:\n", out_print, color.END, "\n")
#             print("".join([color.BOLD, "\n\tDone Making the 2D Plots for this bin...", color.END]))
#             # print(Main_Final_Unfolding_Images)


#             # Histos_Type_List = ["Data", "Response", "SVD", "Bin", "RooUnfold_bayes", "RooUnfold_svd", "RooUnfold_bbb"]
#             # Histos_Type_List = ["Data", "Response", "SVD", "Bin", "RooUnfold_bayes", "RooUnfold_svd"]
#             Histos_Type_List = ["Data", "Response", "Bin", "RooUnfold_bayes", "RooUnfold_svd"]
#             # Histos_Type_List = ["Data", "Response", "Bin", "RooUnfold_bayes"]

#             for Smear in Smearing_final_list:
#     #             for Variable_Type in ["", "Combined"]:
#     #             for Variable_Type in ["Combined"]:
#                 for Variable_Type in [""]:
#                     if(File_Save_Format != ".png"):
#                         continue
#                     if((Q2_xB_Bin != 0) and (Variable_Type in ["Combined"])):
#                         print("".join([color.RED, "\t'Combined' histogram variables only run with Q2_xB_Bin = 0 (at this time)", color.END]))
#                         continue
#                     for Histos_Type in Histos_Type_List:
#                         if((Histos_Type in ["SVD", "RooUnfold_svd"]) and (Variable_Type in ["Combined"])):
#                             print("".join([color.RED, "\tSkipping unfolding method SVD (does not work with 'Combined' histogram variables)", color.END]))
#                             continue
#                         else:
#                             print("".join([color.BLUE, "".join(["\n\tVariable_Type = ", str(Variable_Type), "\n"]) if("Combined" in Variable_Type) else "", "\tHisto_Type    = ", str(Histos_Type), color.END]))
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ####  Canvas (Main) Creation  ####################################################################################################################################################################################################################################################################################################################################################################################
#                             # Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)])] = Canvas_Create(Name="".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)]), Num_Columns=2, Num_Rows=1, Size_X=3999, Size_Y=2250, cd_Space=0.01)
#                             Unfolded_Canvas_Test["".join(["Multi_Variable_" if("Combined" in Variable_Type) else "", "Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])] = Canvas_Create(Name="".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])]), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
#                             Unfolded_Canvas_Test["".join(["Multi_Variable_" if("Combined" in Variable_Type) else "", "Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].SetFillColor(root_color.LGrey)
#                             # Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)])].Draw()

#                             Unfolded_Canvas_Test_cd_1 = Unfolded_Canvas_Test["".join(["Multi_Variable_" if("Combined" in Variable_Type) else "", "Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].cd(1)
#                             Unfolded_Canvas_Test_cd_1.SetFillColor(root_color.LGrey)
#                             Unfolded_Canvas_Test_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
#                             Unfolded_Canvas_Test_cd_1.Divide(1, 2, 0, 0)

#                             Unfolded_Canvas_Test_cd_1_Upper = Unfolded_Canvas_Test_cd_1.cd(1)
#                             Unfolded_Canvas_Test_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
#                             Unfolded_Canvas_Test_cd_1_Upper.Divide(1, 2, 0, 0)

#                             Unfolded_Canvas_Test_cd_1_Lower = Unfolded_Canvas_Test_cd_1.cd(2)
#                             Unfolded_Canvas_Test_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
#                             Unfolded_Canvas_Test_cd_1_Lower.Divide(1, 1, 0, 0)
#                             Unfolded_Canvas_Test_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)



#                             Unfolded_Canvas_Test_cd_2 = Unfolded_Canvas_Test["".join(["Multi_Variable_" if("Combined" in Variable_Type) else "", "Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].cd(2)
#                             Unfolded_Canvas_Test_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
#                             Unfolded_Canvas_Test_cd_2.SetFillColor(root_color.LGrey)
#                             number_of_rows, number_of_cols = z_pT_Border_Lines(Q2_xB_Bin)[0][1]-1, z_pT_Border_Lines(Q2_xB_Bin)[1][1]-1

#                             # Unfolded_Canvas_Test_cd_2.Divide(1, number_of_rows, 0.0001, 0.0001)
#                             Unfolded_Canvas_Test_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)

#                             # for ii in range(1, number_of_rows + 1, 1):
#                             for ii in range(1, number_of_cols + 1, 1):
#                                 Unfolded_Canvas_Test_cd_2_cols = Unfolded_Canvas_Test_cd_2.cd(ii)
#                                 # Unfolded_Canvas_Test_cd_2_cols.Divide(number_of_cols, 1, 0.0001, 0.0001)
#                                 Unfolded_Canvas_Test_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)


#                         ####  Canvas (Main) Creation End #################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################



#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ####  Filling Canvas (Left)  #####################################################################################################################################################################################################################################################################################################################################################################################


#                             ##############################################################################################################################################################################################################################################################################################################################################################################################################
#                             ####  Upper Left  ############################################################################################################################################################################################################################################################################################################################################################################################

#                             if("y_bin" not in Binning_Method):
#                                 # Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_Test_cd_1_Upper, CD_Num=1, Var_D1="Q2_smeared" if(Sim_Test and "mear" in str(Smear)) else "Q2", Var_D2="xB_smeared" if(Sim_Test and "mear" in str(Smear)) else "xB", Q2_xB_Bin=Q2_xB_Bin, z_pT_Bin="All", Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("mear" not in str(Smear)) else "smear")
#                                 Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_Test_cd_1_Upper, CD_Num=1, Var_D1="Q2", Var_D2="xB", Q2_xB_Bin=Q2_xB_Bin, z_pT_Bin="All", Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
#                             else:
#                                 # Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_Test_cd_1_Upper, CD_Num=1, Var_D1="Q2_smeared" if(Sim_Test and "mear" in str(Smear)) else "Q2", Var_D2="y_smeared"  if(Sim_Test and "mear" in str(Smear)) else "y",  Q2_xB_Bin=Q2_xB_Bin, z_pT_Bin="All", Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("mear" not in str(Smear)) else "smear")
#                                 Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_Test_cd_1_Upper, CD_Num=1, Var_D1="Q2", Var_D2="y",  Q2_xB_Bin=Q2_xB_Bin, z_pT_Bin="All", Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
#                             # Draw_2D_Histograms_Simple(DataFrame=rdf,     Canvas_Input=Unfolded_Canvas_Test_cd_1_Upper, CD_Num=2, Var_D1="z_smeared"  if(Sim_Test and "mear" in str(Smear)) else "z",  Var_D2="pT_smeared" if(Sim_Test and "mear" in str(Smear)) else "pT", Q2_xB_Bin=Q2_xB_Bin, z_pT_Bin="All", Data_Type="rdf" if(not Sim_Test) else "mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if(not Sim_Test) else "" if("mear" not in str(Smear)) else "smear")
#                             Draw_Canvas(Unfolded_Canvas_Test_cd_1_Upper, 2, 0.15)
#                             for ii in Main_Final_Unfolding_Images:
#                                 if(("Var-D1='z" in str(ii)) and ("Var-D2='pT" in str(ii))):
#                                     Main_Final_Unfolding_Images[ii].Draw("colz")
#                                     palette_move(canvas=Unfolded_Canvas_Test_cd_1_Upper.cd(2), histo=Main_Final_Unfolding_Images[ii], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
#                                     if(Q2_xB_Bin != 0):
#                                         # print(color.BOLD, "\nFor z-pT Histogram with 1D unfolding images (together), Q2_xB_Bin =", Q2_xB_Bin, color.END)
#                                         # print(color.BOLD,   "Main_Final_Unfolding_Images[ii].GetName() =", Main_Final_Unfolding_Images[ii].GetName(), "\n", color.END)
#                                         z_pT_borders = {}
#                                         Max_z  = max(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
#                                         Min_z  = min(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
#                                         Max_pT = max(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
#                                         Min_pT = min(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
#                                         for zline in z_pT_Border_Lines(Q2_xB_Bin)[0][2]:
#                                             for pTline in z_pT_Border_Lines(Q2_xB_Bin)[1][2]:
#                                                 z_pT_borders[zline] = ROOT.TLine()
#                                                 z_pT_borders[zline].SetLineColor(1)
#                                                 z_pT_borders[zline].SetLineWidth(4)
#                                                 z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT)
#                                                 z_pT_borders[pTline] = ROOT.TLine()
#                                                 z_pT_borders[pTline].SetLineColor(1)
#                                                 z_pT_borders[pTline].SetLineWidth(4)
#                                                 z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline)

#                                     if("y" in str(Binning_Method) and False):
#                                         MM_z_pT_borders = {}
#                                         for MM in [0.94, 1.5, 2.5]:
#                                             # print("".join(["MM_z_pT_Draw(z_val=0.1, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_xB_Bin), ") ="]), MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_xB_Bin))
#                                             # print("".join(["MM_z_pT_Draw(z_val=0.8, MM_val=", str(MM), ", Q2_y_Bin=", str(Q2_xB_Bin), ") ="]), MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_xB_Bin))
#                                             MM_z_pT_borders[MM] = ROOT.TLine()
#                                             MM_z_pT_borders[MM].SetLineColor(6 if(MM == 0.94) else 8 if(MM == 1.5) else 46)
#                                             MM_z_pT_borders[MM].SetLineWidth(2)
#                                             MM_z_pT_borders[MM].DrawLine(0.1, MM_z_pT_Draw(z_val=0.1, MM_val=MM, Q2_y_Bin=Q2_xB_Bin), 0.8, MM_z_pT_Draw(z_val=0.8, MM_val=MM, Q2_y_Bin=Q2_xB_Bin))

#     #                         cd_test = 1
#     #                         for ii in Main_Final_Unfolding_Images:
#     #                             # if(cd_test > 2 or ("Q2-xB-Bin=All" not in str(ii) and "".join(["Q2-xB-Bin=", str(Q2_xB_Bin) if(Q2_xB_Bin not in [0, "0"]) else "All"]) not in str(ii)) or (("Var-D1='z'" in str(ii)) and ("Var-D2='pT'" in str(ii)) and cd_test != 2) or (("Var-D1='z'" not in str(ii)) and ("Var-D2='pT'" not in str(ii)) and cd_test != 1)):
#     #                             #     continue
#     #
#     #
#     #                             if(str(ii) == "".join(["((Histo-Group='Normal_2D'), (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=''), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", "All, z-PT-Bin=All_1D]), (Var-D1='Q2'-[NumBins=100, MinBin=1.48, MaxBin=11.87]), (Var-D2='xB'-[NumBins=100, MinBin=0.09, MaxBin=0.826]))"]) if(not Sim_Test) else "".join(["((Histo-Group='Normal_2D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=''), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", "All, z-PT-Bin=All_1D]), (Var-D1='Q2'-[NumBins=100, MinBin=1.48, MaxBin=11.87]), (Var-D2='xB'-[NumBins=100, MinBin=0.09, MaxBin=0.826]))"])):
#     #                                 cd_test = 1
#     #                             else:
#     #                                 cd_test += 1
#     #                                 # print(ii)
#     #                                 # if(cd_test > 2):
#     #                                 #     print(cd_test)
#     #                                 #     break
#     #
#     #
#     #
#     #                             Draw_Canvas(Unfolded_Canvas_Test_cd_1_Upper, cd_test, 0.15)
#     #                             # Unfolded_Canvas_Test_cd_1_Upper.cd(cd_test)
#     #                             Main_Final_Unfolding_Images[ii].Draw("colz")
#     #
#     #                             Unfolded_Canvas_Test_cd_1_Upper.Modified()
#     #                             Unfolded_Canvas_Test_cd_1_Upper.Update()
#     #
#     #                             palette_move(canvas=Unfolded_Canvas_Test_cd_1_Upper, histo=Main_Final_Unfolding_Images[ii], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
#     #
#     #                             if(("Var-D1='Q2'" in str(ii)) and ("Var-D2='xB'" in str(ii))):
#     #                                 Main_Final_Unfolding_Images[ii].SetTitle((Main_Final_Unfolding_Images[ii].GetTitle()).replace("Q^{2}-x_{B} Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All", "}"])))
#     #                                 # print("".join([color.BLUE, "Q2-xB plots:", color.END]))
#     #                                 # print(Main_Final_Unfolding_Images[ii].GetTitle())
#     #                                 # print(ii)
#     #                                 # print("\n\n")
#     #                                 Q2_xB_borders = {}
#     #                                 line_num      = 0
#     #                                 for b_lines in Q2_xB_Border_Lines(-1):
#     #                                     Q2_xB_borders[line_num] = ROOT.TLine()
#     #                                     Q2_xB_borders[line_num].SetLineColor(1)    
#     #                                     Q2_xB_borders[line_num].SetLineWidth(5)
#     #                                     Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
#     #                                     line_num += 1
#     #                                 if(Q2_xB_Bin != 0):
#     #                                     ##=====================================================##
#     #                                     ##==========##     Selecting Q2-xB Bin     ##==========##
#     #                                     ##=====================================================##
#     #                                     line_num_2 = 0
#     #                                     for b_lines_2 in Q2_xB_Border_Lines(Q2_xB_Bin):
#     #                                         Q2_xB_borders[line_num_2] = ROOT.TLine()
#     #                                         Q2_xB_borders[line_num_2].SetLineColor(2)
#     #                                         Q2_xB_borders[line_num_2].SetLineWidth(10)
#     #                                         Q2_xB_borders[line_num_2].DrawLine(b_lines_2[0][0], b_lines_2[0][1], b_lines_2[1][0], b_lines_2[1][1])
#     #                                         line_num_2 += + 1
#     #                                     ##=====================================================##
#     #                                     ##==========##     Selecting Q2-xB Bin     ##==========##
#     #                                     ##=====================================================##
#     #
#     #
#     #                             if((Q2_xB_Bin != 0) and ("Var-D1='z'" in str(ii)) and ("Var-D2='pT'" in str(ii))):
#     #                                 z_pT_borders = {}
#     #                                 Max_z  = max(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
#     #                                 Min_z  = min(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
#     #                                 Max_pT = max(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
#     #                                 Min_pT = min(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
#     #                                 for zline in z_pT_Border_Lines(Q2_xB_Bin)[0][2]:
#     #                                     for pTline in z_pT_Border_Lines(Q2_xB_Bin)[1][2]:
#     #                                         z_pT_borders[zline] = ROOT.TLine()
#     #                                         z_pT_borders[zline].SetLineColor(1)
#     #                                         z_pT_borders[zline].SetLineWidth(4)
#     #                                         z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT) # z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
#     #                                         z_pT_borders[pTline] = ROOT.TLine()
#     #                                         z_pT_borders[pTline].SetLineColor(1)
#     #                                         z_pT_borders[pTline].SetLineWidth(4)
#     #                                         z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline) # z_pT_borders[pTline].DrawLine(pTline, Max_z, pTline, Min_z)
#     #
#     #                             # cd_test += 1
#                             ####  Upper Left  ############################################################################################################################################################################################################################################################################################################################################################################################
#                             ##############################################################################################################################################################################################################################################################################################################################################################################################################

#                             ##############################################################################################################################################################################################################################################################################################################################################################################################################
#                             ####  Lower Left  ############################################################################################################################################################################################################################################################################################################################################################################################

#                             Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)

#                             if("Data" in Histos_Type):
#                                 try:
#                                     # Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)
#                                     Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0"])].DrawClone("same")
#                                     Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0", "_Smeared" if("smear" in str(Smear)) else ""])].DrawClone("same")
#                                     Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0"])].DrawClone("same")
#                                 except Exception as e:
#                                     print("".join([color.BOLD, color.RED, "ERROR IN 1D Histograms:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#                                     # print("".join([color.RED, color.BOLD, "ERROR IN 1D Histograms (line 2714): ", color.END, color.RED, str(e), color.END]))
#                                     for ii_error in Save_Response_Matrix:
#                                         print(ii_error)


#                             if("Response" in Histos_Type):
#                                 try:
#                                     Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0", "_Smeared" if("smear" in str(Smear)) else ""])].Draw("col")
#                                 except Exception as e:
#                                     print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#                                     # print("".join([color.RED, color.BOLD, "ERROR IN Response Matrix (line 2722): ", color.END, color.RED, str(e), color.END]))


#                             if("SVD" in Histos_Type):
#                                 try:
#                                     Unfolding_Histogram_1_Norm_Clone[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin",                                                str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                 except Exception as e:
#                                     try:
#                                         Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                     except:
#                                         print("".join([color.BOLD, color.RED, "ERROR IN SVD Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#                                     # print("".join([color.RED, color.BOLD, "ERROR IN SVD Method Histogram (line 2730): ", color.END, color.RED, str(e), color.END]))

#                             if("Bin" in Histos_Type):
#                                 try:
#                                     if("Combined" not in Variable_Type):
#                                         Bin_Unfolded[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin",                                                                                               str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                     else:
#                                         if("Combined_phi_t_Q2_xB"   in Variable_Type):
#                                             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Combined_phi_t_Q2_xB_Bin",  str(Binning_Method),     "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=195, MinBin=-1.5, MaxBin=193.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         elif("Combined_phi_t_Q2"    in Variable_Type):
#                                             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Combined_phi_t_Q2",                                  "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         if("Multi_Dim_Q2_xB_Bin"    in Variable_Type):
#                                             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t", "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=195, MinBin=-1.5, MaxBin=193.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         elif("Multi_Dim_Q2_y_Bin_phi_t" in Variable_Type):
#                                             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Multi_Dim_Q2_y_Bin_phi_t",                           "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         elif(("Multi_Dim_Q2_phi_t"  in Variable_Type) or ("Combined" == Variable_Type)):
#                                             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Multi_Dim_Q2_phi_t",                                 "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                 except Exception as e:
#                                     try:
#                                         Bin_Unfolded[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t",                                              "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin",        str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                     except:
#                                         print("".join([color.BOLD, color.RED, "ERROR IN Bin-by-bin Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#                                     # print("".join([color.RED, color.BOLD, "ERROR IN Bin-by-bin Method Histogram (line 2737): ", color.END, color.RED, str(e), color.END]))


#                             if("RooUnfold_bayes" in Histos_Type):
#                                 try:
#                                     if("Combined" not in Variable_Type):
#                                         RooUnfolded_Histos[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method),                                                "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                     else:
#                                         if("Combined_phi_t_Q2_xB"   in Variable_Type):
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Combined_phi_t_Q2_xB_Bin", str(Binning_Method),                                                                                     "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=195, MinBin=-1.5, MaxBin=193.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                         elif("Combined_phi_t_Q2"    in Variable_Type):
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Combined_phi_t_Q2",                                                                                                                 "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                         elif("Multi_Dim_Q2_y_Bin_phi_t" in Variable_Type):
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Multi_Dim_Q2_y_Bin_phi_t",                                                                                                          "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                         elif(("Multi_Dim_Q2_phi_t"  in Variable_Type) or ("Combined" == Variable_Type)):
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='Multi_Dim_Q2_phi_t",                                                                                                                "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")

#                                 except Exception as e:
#                                     try:
#                                         RooUnfolded_Histos[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                     except:
#                                         print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bayesian) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                             if("RooUnfold_svd" in Histos_Type):
#                                 try:
#                                     RooUnfolded_Histos[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin",                                                str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
#                                 except Exception as e:
#                                     try:
#                                         RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
#                                     except:
#                                         print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (SVD) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                             if("RooUnfold_bbb" in Histos_Type):
#                                 try:
#                                     RooUnfolded_Histos[    "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin",                                                str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
#                                 except Exception as e:
#                                     try:
#                                         RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
#                                     except:
#                                         print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bin-by-Bin) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))


#                             ####  Lower Left  ############################################################################################################################################################################################################################################################################################################################################################################################
#                             ##############################################################################################################################################################################################################################################################################################################################################################################################################


#                         ####  Filling Canvas (Left) End ##################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################



#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ####  Filling Canvas (Right)  ####################################################################################################################################################################################################################################################################################################################################################################################

#                             for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):

#                                 cd_row = int(z_pT_Bin/number_of_cols) + 1
#                                 if(0 == (z_pT_Bin%number_of_cols)):
#                                     cd_row += -1

#                                 cd_col = z_pT_Bin - ((cd_row - 1)*number_of_cols)

#                                 # Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row = Unfolded_Canvas_Test_cd_2.cd(cd_row)
#                                 # Unfolded_Canvas_Test_cd_2_z_pT_Bin     = Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row.cd(cd_col)
#                                 Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row = Unfolded_Canvas_Test_cd_2.cd((number_of_cols - cd_col) + 1)
#                                 Unfolded_Canvas_Test_cd_2_z_pT_Bin     = Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)

#                                 Unfolded_Canvas_Test_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
#                                 Unfolded_Canvas_Test_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
#                                 Draw_Canvas(Unfolded_Canvas_Test_cd_2_z_pT_Bin, 1, 0.15)

#                                 if("y_bin" in Binning_Method):
#                                     # if(((Q2_xB_Bin in [1]) and (z_pT_Bin in [42, 48, 49])) or ((Q2_xB_Bin in [2]) and (z_pT_Bin in [42, 49])) or (Q2_xB_Bin in [3] and z_pT_Bin in [7, 42, 48, 49]) or (Q2_xB_Bin in [4] and z_pT_Bin in [6, 7, 14, 28, 35, 41, 42]) or (Q2_xB_Bin in [5] and z_pT_Bin in [36]) or (Q2_xB_Bin in [6] and z_pT_Bin in [30]) or (Q2_xB_Bin in [7] and z_pT_Bin in [7, 35, 42, 48, 49]) or (Q2_xB_Bin in [8] and z_pT_Bin in [5, 6, 36]) or (Q2_xB_Bin in [9] and z_pT_Bin in [30, 36]) or (Q2_xB_Bin in [10] and z_pT_Bin in [24, 29, 30]) or (Q2_xB_Bin in [11, 12] and z_pT_Bin in [30, 35, 36])  or (Q2_xB_Bin in [13] and z_pT_Bin in [5, 20, 24, 25])):
#                                     #     continue
#                                     if(((Q2_xB_Bin in [1]) and (z_pT_Bin in [42, 48, 49])) or ((Q2_xB_Bin in [2]) and (z_pT_Bin in [42, 49])) or (Q2_xB_Bin in [3] and z_pT_Bin in [42, 48, 49]) or (Q2_xB_Bin in [4] and z_pT_Bin in [7, 28, 35, 41, 42]) or (Q2_xB_Bin in [5] and z_pT_Bin in [36]) or (Q2_xB_Bin in [6] and z_pT_Bin in [30]) or (Q2_xB_Bin in [7] and z_pT_Bin in [7, 42, 48, 49]) or (Q2_xB_Bin in [8] and z_pT_Bin in [6, 36]) or (Q2_xB_Bin in [9] and z_pT_Bin in [36]) or (Q2_xB_Bin in [10] and z_pT_Bin in [30]) or (Q2_xB_Bin in [11] and z_pT_Bin in [30]) or (Q2_xB_Bin in [14] and z_pT_Bin in [25]) or (Q2_xB_Bin in [15, 16, 17] and z_pT_Bin in [20])):
#                                         continue

#                                 try:
#                                     if("Data" in Histos_Type):
#                                         try:
#                                             # Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)
#                                             Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin)])].Draw("same")
#                                             Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin), "_Smeared" if("smear" in str(Smear)) else ""])].Draw("same")
#                                             Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin)])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN 1D (Data) Histograms:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                                     if("Response" in Histos_Type):
#                                         try:
#                                             Save_Response_Matrix["".join(["Multi Variable " if("Combined" in Variable_Type) else "", "Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin), "_Smeared" if("smear" in str(Smear)) else ""])].Draw("col")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                                     if("SVD" in Histos_Type):
#                                         try:
#                                             Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN SVD Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                                     if("Bin" in Histos_Type):
#                                         try:
#                                             if("Combined" not in Variable_Type):
#                                                 Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method),                                                                   "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                             else:
#                                                 # Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='Combined_phi_t_Q2", "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                                 Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='Multi_Dim_Q2_phi_t", "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN Bin-by-bin Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                                     if("RooUnfold_bayes" in Histos_Type):
#                                         try:
#                                             if("Combined" not in Variable_Type):
#                                                 RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method),                                                                   "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                             else:
#                                                 # RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='Combined_phi_t_Q2", "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                                 RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='Multi_Dim_Q2_phi_t", "'" if(Smear != "smear") else "_smeared'" , "'-[NumBins=483, MinBin=-1.5, MaxBin=481.5]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bayesian) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

#                                     if("RooUnfold_svd" in Histos_Type):
#                                         try:
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (SVD) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
#                                             for ii in RooUnfolded_Histos:
#                                                 if(("".join(["Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin)]) in str(ii)) and ("_svd_Norm_extra" in str(ii))):
#                                                     print("".join(["RooUnfolded_Histos: ", str(ii)]))

#                                     if("RooUnfold_bbb" in Histos_Type):
#                                         try:
#                                             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='", str(Binning_Method).replace("_", "") if("y_bin" not in str(Binning_Method)) else "y_bin", "'-[Q2-xB-Bin=" if("y_bin" not in str(Binning_Method)) else "'-[Q2-y-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
#                                         except Exception as e:
#                                             print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bin-by-Bin) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))


#                                 except:
#                                     print("".join(["Failed on ", str(z_pT_Bin)]))
#                                     print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc()), "\n================================================================================================================================================================================================\n\n"]))
#                                     # continue
#                                     # break

#                         ####  Filling Canvas (Right) End #################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################
#                         ##################################################################################################################################################################################################################################################################################################################################################################################################################



#         print("".join([color.BOLD, color.GREEN, "\nDone Combining Unfolded Histograms into one image per bin (Now saving...)\n", color.END]))
#         for Canvas_name in Unfolded_Canvas_Test:
#             print("".join(["\n", str(Canvas_name), ": ", str(Unfolded_Canvas_Test[Canvas_name])]))
#             if("cd_upper" not in str(Canvas_name) and "cd_lower" not in str(Canvas_name)):
#                 Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), str(File_Save_Format)])
#                 Save_Name = Save_Name.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "_smeared-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#                 Save_Name = Save_Name.replace("".join(["Var-D2=z_pT_Bin", str(Binning_Method), "-[NumBins=52_MinBin=-1.5_MaxBin=50.5"]), "")
#                 Save_Name = Save_Name.replace("_smeared-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#                 Save_Name = Save_Name.replace("-[NumBins=483_MinBin=-1.5_MaxBin=481.5_", "")
#                 Save_Name = Save_Name.replace("_smeared-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#                 Save_Name = Save_Name.replace("-[NumBins=528_MinBin=-1.5_MaxBin=526.5_", "")
#                 Save_Name = Save_Name.replace("_smeared-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")
#                 Save_Name = Save_Name.replace("-[NumBins=228_MinBin=-1.5_MaxBin=226.5_", "")
#                 Save_Name = Save_Name.replace("Var-D1=", "")
#                 Save_Name = Save_Name.replace("__", "_")

#                 Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
#                 Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))

#                 # if(extra_function_terms and "phi_h" in str(Save_Name)):
#                 if(extra_function_terms):
#                     Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))

#                 if("y" in Binning_Method):
#                     Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
#                 if(Sim_Test):
#                     Save_Name = "".join(["Sim_Test_", Save_Name])

#                 if("y" in Binning_Method):
#                     Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
                    
#                 Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",       "Q2_y_phi_h")
#                 Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h", "z_pT_phi_h")
#                 Save_Name = Save_Name.replace("_.png",                ".png")
#                 Save_Name = Save_Name.replace("__",                   "_")

#                 if(Saving_Q):
#                     Unfolded_Canvas_Test[Canvas_name].SaveAs(Save_Name)
#                 count_of_images += 1
#                 print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
#             else:
#                 print("".join([color.RED, "Canvas_name = ", str(Canvas_name), color.END, "\n"]))

#         if(Saving_Q):
#             print("".join([color.BOLD, color.GREEN, "\nDONE SAVING\n", color.END, color.BOLD, color.BLUE, "Starting final folder creation/image sorting...", color.END]))
#         else:
#             print("".join([color.BOLD, color.RED, "\nNOT SAVING", color.END]))



#     else:
#         print("".join([color.RED, color.BOLD, "\n\nMAJOR ERROR: No histograms were made...\n\n", color.END]) if(count != 0) else "")


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

print("".join(["Saved ", str(count_of_images), " Images..."]))

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
    rate_of_histos = count_of_images/(((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins)
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
