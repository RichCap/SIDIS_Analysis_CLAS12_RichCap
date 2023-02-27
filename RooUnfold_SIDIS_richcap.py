#!/usr/bin/env python

import sys

       
Saving_Q = True
Smearing_Options = "both"
if(len(sys.argv) > 1):
    if(sys.argv[1] in ["test", "Test", "time", "Time"]):
        print("\nNOT SAVING\n")
        Saving_Q = False
    else:
        print("".join(["\nOption Selected: ", str(sys.argv[1]), " (Still Saving...)" if("no_save" not in str(sys.argv[1])) else " (NOT SAVING)"]))
        Saving_Q = True if("no_save" not in str(sys.argv[1])) else False
        Smearing_Options = str((sys.argv[1]).replace("_no_save", "")) if(str(sys.argv[1]) not in ["save"]) else "both"
else:
    Saving_Q = True
    
Q2_xB_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
if(len(sys.argv) > 2):
    Q2_xB_Bin_List = []
    for ii_bin in range(2, len(sys.argv), 1):
        Q2_xB_Bin_List.append(sys.argv[ii_bin])
    if(Q2_xB_Bin_List == []):
        print("Error")
        Q2_xB_Bin_List = ['1']
    print(str(("".join(["\nRunning for Q2-xB Bins: ", str(Q2_xB_Bin_List)]).replace("[", "")).replace("]", "")))
    
# # Test code with the command:
# # # python /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py test (Q2-xB bin)

from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT

import numpy
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
if(datetime_object_full.hour == 0 or datetime_object_full.hour == 24):
    print("".join([Date_Day, color.BOLD, "12:", str(timeMin_full), " a.m.", color.END]))
print("")




try:
    import RooUnfold
    print("".join([color.GREEN, color.BOLD, "Perfect Success", color.END]))
except ImportError:
    print("".join([color.RED, color.BOLD, "ERROR: \n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n"]))
    # print("Somehow the python module was not found, let's try loading the library by hand...")
    # try:
    #     ROOT.gSystem.Load("libRooUnfold.so")
    #     print("".join([color.GREEN, "Success", color.END]))
    # except:
    #     print("".join([color.RED, color.BOLD, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    
for ii in sys.modules:
    if(str(ii) in ["ROOT", "RooUnfold"]):
        # print(ii)
        print(sys.modules[ii])
        
        
        
print("\n\n")




File_Save_Format = ".png"

















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
        Draw_Lines.append([[0.126602, 2], [0.15, 2.28]])
        Draw_Lines.append([[0.15, 2.28], [0.24, 3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.15, 2]])
        # Draw_Lines.append([[0.15, 1.98], [0.15, 1.95]])
        Draw_Lines.append([[0.15, 2], [0.126602, 2]])
        
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.15, 2], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.24, 2]])
        Draw_Lines.append([[0.24, 2], [0.15, 2]])
        # Draw_Lines.append([[0.15, 1.95], [0.15, 1.98]])
        # Draw_Lines.append([[0.15, 1.98], [0.24, 2.75]])
        # Draw_Lines.append([[0.24, 2.75], [0.24, 1.95]])
        # Draw_Lines.append([[0.24, 1.95], [0.15, 1.95]])

    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.24, 2.75], [0.24, 3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.34, 5.12]])
        Draw_Lines.append([[0.34, 5.12], [0.34, 3.63]])
        Draw_Lines.append([[0.34, 3.63], [0.24, 2.75]])
        
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

                    # Info about z bins              # Info about pT bins         # Total number of z-pT bins
    output = [['z', Num_z_Borders, z_Borders],['pT', Num_pT_Borders, pT_Borders], (Num_z_Borders-1)*(Num_pT_Borders-1)]
    
    return output


##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Find_z_pT_Bin_Center(Q2_xB_Bin_Select, z_pT_Bin, variable_return="Default"):
    z_Value, pT_Value = "Error", "Error"
    z_Value_Max, z_Value_Min = "Error", "Error"
    
    # For Q2_xB Bin 1
    if(Q2_xB_Bin_Select == 1):
        if(z_pT_Bin in range(1, 8, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.55

        if(z_pT_Bin in range(8, 15, 1)):
            z_Value_Max, z_Value_Min = 0.55, 0.445

        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.445, 0.36

        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.36, 0.29

        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.29, 0.24

        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.24, 0.2

        if(z_pT_Bin in range(43, 50, 1)):
            z_Value_Max, z_Value_Min = 0.2, 0.15
            
######################################################################################
            
        if(z_pT_Bin in range(1, 44, 7)):
            pT_Value_Max, pT_Value_Min = 0.2, 0.05
            
        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3, 0.2
            
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4, 0.3
            
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5, 0.4
            
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
            
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0, 0.75
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2):
        if(z_pT_Bin in range(1, 8, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.6
            
        if(z_pT_Bin in range(8, 15, 1)):
            z_Value_Max, z_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.5, 0.41
            
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
            pT_Value_Max, pT_Value_Min = 0.2, 0.05

        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3, 0.2
            
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4, 0.3
            
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5, 0.4
            
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
            
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0, 0.75
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3):
        if(z_pT_Bin in range(1, 8, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.55
            
        if(z_pT_Bin in range(8, 15, 1)):
            z_Value_Max, z_Value_Min = 0.55, 0.445
            
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.445, 0.36
            
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.36, 0.29
            
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.29, 0.24
            
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.24, 0.2
            
        if(z_pT_Bin in range(43, 50, 1)):
            z_Value_Max, z_Value_Min = 0.2, 0.15
            
######################################################################################
            
        if(z_pT_Bin in range(1, 44, 7)):
            pT_Value_Max, pT_Value_Min = 0.2, 0.05
            
        if(z_pT_Bin in range(2, 45, 7)):
            pT_Value_Max, pT_Value_Min = 0.3, 0.2
            
        if(z_pT_Bin in range(3, 46, 7)):
            pT_Value_Max, pT_Value_Min = 0.4, 0.3
            
        if(z_pT_Bin in range(4, 47, 7)):
            pT_Value_Max, pT_Value_Min = 0.5, 0.4
            
        if(z_pT_Bin in range(5, 48, 7)):
            pT_Value_Max, pT_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(6, 49, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
            
        if(z_pT_Bin in range(7, 50, 7)):
            pT_Value_Max, pT_Value_Min = 1.0, 0.75
            
######################################################################################
######################################################################################

    # For Q2_xB Bin 4
    if(Q2_xB_Bin_Select == 4):            
        if(z_pT_Bin in range(1, 8, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.6
            
        if(z_pT_Bin in range(8, 15, 1)):
            z_Value_Max, z_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(15, 22, 1)):
            z_Value_Max, z_Value_Min = 0.5, 0.41
            
        if(z_pT_Bin in range(22, 29, 1)):
            z_Value_Max, z_Value_Min = 0.41, 0.345
            
        if(z_pT_Bin in range(29, 36, 1)):
            z_Value_Max, z_Value_Min = 0.345, 0.29
            
        if(z_pT_Bin in range(36, 43, 1)):
            z_Value_Max, z_Value_Min = 0.29, 0.2
            
######################################################################################
            
        if(z_pT_Bin in range(1, 37, 7)):
            pT_Value_Max, pT_Value_Min = 0.2, 0.05
            
        if(z_pT_Bin in range(2, 38, 7)):
            pT_Value_Max, pT_Value_Min = 0.3, 0.2
            
        if(z_pT_Bin in range(3, 39, 7)):
            pT_Value_Max, pT_Value_Min = 0.4, 0.3
            
        if(z_pT_Bin in range(4, 40, 7)):
            pT_Value_Max, pT_Value_Min = 0.5, 0.4
            
        if(z_pT_Bin in range(5, 41, 7)):
            pT_Value_Max, pT_Value_Min = 0.6, 0.5
            
        if(z_pT_Bin in range(6, 42, 7)):
            pT_Value_Max, pT_Value_Min = 0.75, 0.6
            
        if(z_pT_Bin in range(7, 43, 7)):
            pT_Value_Max, pT_Value_Min = 1.0, 0.75
            
######################################################################################
######################################################################################
            
    # For Q2_xB Bin 5
    if(Q2_xB_Bin_Select == 5):
        if(z_pT_Bin in range(1, 7, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.5
            
        if(z_pT_Bin in range(7, 13, 1)):
            z_Value_Max, z_Value_Min = 0.5, 0.4
            
        if(z_pT_Bin in range(13, 19, 1)):
            z_Value_Max, z_Value_Min = 0.4, 0.32
            
        if(z_pT_Bin in range(19, 25, 1)):
            z_Value_Max, z_Value_Min = 0.32, 0.26
            
        if(z_pT_Bin in range(25, 31, 1)):
            z_Value_Max, z_Value_Min = 0.26, 0.215
            
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
            pT_Value_Max, pT_Value_Min = 1.0, 0.65
            
######################################################################################
######################################################################################

    # For Q2_xB Bin 6
    if(Q2_xB_Bin_Select == 6):
        if(z_pT_Bin in range(1, 6, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.56
            
        if(z_pT_Bin in range(6, 11, 1)):
            z_Value_Max, z_Value_Min = 0.56, 0.47
            
        if(z_pT_Bin in range(11, 16, 1)):
            z_Value_Max, z_Value_Min = 0.47, 0.4
            
        if(z_pT_Bin in range(16, 21, 1)):
            z_Value_Max, z_Value_Min = 0.4, 0.32
            
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
            pT_Value_Max, pT_Value_Min = 0.8, 0.54
            
######################################################################################
######################################################################################
        
    # For Q2_xB Bin 7
    if(Q2_xB_Bin_Select == 7):
        if(z_pT_Bin in range(1, 6, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.5
            
        if(z_pT_Bin in range(6, 11, 1)):
            z_Value_Max, z_Value_Min = 0.5, 0.39
            
        if(z_pT_Bin in range(11, 16, 1)):
            z_Value_Max, z_Value_Min = 0.39, 0.3
            
        if(z_pT_Bin in range(16, 21, 1)):
            z_Value_Max, z_Value_Min = 0.3, 0.23
            
        if(z_pT_Bin in range(21, 26, 1)):
            z_Value_Max, z_Value_Min = 0.23, 0.15
            
######################################################################################

        if(z_pT_Bin in range(1, 22, 5)):
            pT_Value_Max, pT_Value_Min = 0.23, 0.05
            
        if(z_pT_Bin in range(2, 23, 5)):
            pT_Value_Max, pT_Value_Min = 0.34, 0.23
            
        if(z_pT_Bin in range(3, 24, 5)):
            pT_Value_Max, pT_Value_Min = 0.435, 0.34
            
        if(z_pT_Bin in range(4, 25, 5)):
            pT_Value_Max, pT_Value_Min = 0.55, 0.435
            
        if(z_pT_Bin in range(5, 26, 5)):
            pT_Value_Max, pT_Value_Min = 0.8, 0.55
            
######################################################################################
######################################################################################
            
    # For Q2_xB Bin 8
    if(Q2_xB_Bin_Select == 8):
        if(z_pT_Bin in range(1, 5, 1)):
            z_Value_Max, z_Value_Min = 0.7, 0.5
            
        if(z_pT_Bin in range(5, 9, 1)):
            z_Value_Max, z_Value_Min = 0.5, 0.425
            
        if(z_pT_Bin in range(9, 13, 1)):
            z_Value_Max, z_Value_Min = 0.425, 0.36
            
        if(z_pT_Bin in range(13, 17, 1)):
            z_Value_Max, z_Value_Min = 0.36, 0.3
            
        if(z_pT_Bin in range(17, 21, 1)):
            z_Value_Max, z_Value_Min = 0.3, 0.22
            
######################################################################################

        if(z_pT_Bin in range(1, 18, 4)):
            pT_Value_Max, pT_Value_Min = 0.23, 0.05
            
        if(z_pT_Bin in range(2, 19, 4)):
            pT_Value_Max, pT_Value_Min = 0.34, 0.23
            
        if(z_pT_Bin in range(3, 20, 4)):
            pT_Value_Max, pT_Value_Min = 0.45, 0.34
            
        if(z_pT_Bin in range(4, 21, 4)):
            pT_Value_Max, pT_Value_Min = 0.7, 0.45
            
            
    z_Value = (z_Value_Max - z_Value_Min)/2
    pT_Value = (pT_Value_Max - pT_Value_Min)/2
            
            
    if(variable_return == "Default"):
        return [z_Value, pT_Value]
    if("z" in variable_return and "title" not in variable_return and "Title" not in variable_return and "str" not in variable_return):
        return z_Value
    
    if("pT" in variable_return and "title" not in variable_return and "Title" not in variable_return and "str" not in variable_return):
        return pT_Value
    
    if("z" in variable_return and ("title" in variable_return or "Title" in variable_return or "str" in variable_return)):
        return str("".join([str(z_Value_Min), " - ", str(z_Value_Max)]))
    
    if("pT" in variable_return and ("title" in variable_return or "Title" in variable_return or "str" in variable_return)):
        return str("".join([str(pT_Value_Min), " - ", str(pT_Value_Max)]))
    
    if(variable_return in ["title", "Title", "str"]):
        return [str("".join([str(z_Value_Min), " - ", str(z_Value_Max)])), str("".join([str(pT_Value_Min), " - ", str(pT_Value_Max)]))]

    
#################################################################################################################################################################
##==========##==========##     Kinematic Binning Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
#################################################################################################################################################################


















############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################

def Full_Calc_Fit(Histo):
    
    Histo_180_bin = Histo.FindBin(155)
    Histo_240_bin = Histo.FindBin(300)
    Histo_max_bin = Histo.GetMaximumBin()
    
    if(Histo_max_bin == Histo_180_bin or Histo_max_bin == Histo_240_bin):
        print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Same bin used in fits"]))
        Histo_max_bin = Histo.FindBin(100)
    
    Histo_180_bin_y = Histo.GetBinContent(Histo_180_bin)
    Histo_240_bin_y = Histo.GetBinContent(Histo_240_bin)
    Histo_max_bin_y = Histo.GetBinContent(Histo_max_bin)
    
    Histo_180_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_180_bin)
    Histo_240_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_240_bin)
    Histo_max_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
    
    Histo_180_bin_Cos_phi = ROOT.cos(Histo_180_bin_x)
    Histo_240_bin_Cos_phi = ROOT.cos(Histo_240_bin_x)
    Histo_max_bin_Cos_phi = ROOT.cos(Histo_max_bin_x)
    
    Histo_180_bin_Cos_2_phi = ROOT.cos(2*Histo_180_bin_x)
    Histo_240_bin_Cos_2_phi = ROOT.cos(2*Histo_240_bin_x)
    Histo_max_bin_Cos_2_phi = ROOT.cos(2*Histo_max_bin_x)
    
    numerator = (Histo_180_bin_y*Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_Cos_phi*Histo_240_bin_y*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_y*Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_2_phi*Histo_240_bin_y*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi*Histo_max_bin_y) - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi*Histo_max_bin_y)
    denominator = (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi) - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi) - (Histo_180_bin_Cos_phi*Histo_max_bin_Cos_2_phi) + (Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi) + (Histo_180_bin_Cos_2_phi*Histo_max_bin_Cos_phi) - (Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi)

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
        
        
    return [A, B, C]

############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################




















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
            if(Print_Method == "off"):
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
            # print("".join([color.BOLD, color.BLUE, "\n'", str(Histo.GetName()), "' Maximum = ", str(Histo.GetMaximum()), " Total = ", str(Histo.Integral()), color.END]))
            if(Histo.Integral() != 0 and Histo.GetMaximum() != 0):
                Test_Y = (Histo.GetMaximum()) if((Norm_Q not in ["Normalized", "Norm"]) or (Norm_Q == "Default")) else ((Histo.GetMaximum())/(Histo.Integral()))
            else:
                Test_Y = 0
                print("".join([color.BOLD, color.RED, "\n EMPTY HISTOGRAM: '", str(Histo.GetName()), "'\n\tMaximum = ", str(Histo.GetMaximum()), "\n\tTotal = ", str(Histo.Integral()), color.END]))
            if(Test_Y > Max_Y):
                Max_Y = Test_Y   
        return Max_Y
    except:
        print("".join([color.BOLD, color.RED, "\nERROR IN GETTING THE MAX Y OF THE 1D HISTOGRAMS...", color.END]))
        print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc())]))
        return "ERROR"
    
    
######################################################################################################################################################
##==========##==========##     Canvas Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################




















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
            NumBins_List.append(200)
        if(variable in ["pip", "pip_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(6)
            NumBins_List.append(200)
        if(variable in ["elth", "pipth", "elth_smeared", "pipth_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(40)
            NumBins_List.append(200)
        if(variable in ["elPhi", "pipPhi", "elPhi_smeared", "pipPhi_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(360)
            NumBins_List.append(200)
            
        if(variable in ["Q2", "Q2_smeared"]):
            MinBin_List.append(1.48)
            MaxBin_List.append(11.87)
            NumBins_List.append(100)
        if(variable in ["xB", "xB_smeared"]):
            MinBin_List.append(0.09)
            MaxBin_List.append(0.826)
            NumBins_List.append(100)
        if(variable in ["z",  "z_smeared"]):
            MinBin_List.append(0.017)
            MaxBin_List.append(0.935)
            NumBins_List.append(100)
        if(variable in ["pT", "pT_smeared"]):
            MinBin_List.append(0)
            MaxBin_List.append(1.26)
            NumBins_List.append(120)
            
    # Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
    Find_Name = "".join(["((Histo-Group='Normal_2D'), (Data-Type='", str(Data_Type), "'), (Data-Cut='", str(Cut_Type), "'), (Smear-Type='", str(Smear_Q), "'), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All]), (Var-D1='", str(Var_D1), "'-[NumBins=", str(NumBins_List[0]), ", MinBin=", str(MinBin_List[0]), ", MaxBin=", str(MaxBin_List[0]), "]), (Var-D2='", str(Var_D2), "'-[NumBins=", str(NumBins_List[1]), ", MinBin=", str(MinBin_List[1]), ", MaxBin=", str(MaxBin_List[1]), "]))"])
    # print(Find_Name)
    
    Drawing_Histo_Found = DataFrame.Get(Find_Name)
    #########################################################
    ##===============##     3D Slices     ##===============##
    if("3D" in str(type(Drawing_Histo_Found))):
        try:
            bin_Histo_2D_0, bin_Histo_2D_1 = Drawing_Histo_Found.GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin not in ["All", 0]) else 0), Drawing_Histo_Found.GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin not in ["All", 0]) else Drawing_Histo_Found.GetNbinsX())
            if(z_pT_Bin not in ["All", 0]):
                Drawing_Histo_Found.GetXaxis().SetRange(bin_Histo_2D_0, bin_Histo_2D_1)
            Drawing_Histo_Set = Drawing_Histo_Found.Project3D('yz')
            Drawing_Histo_Set.SetName(str(Drawing_Histo_Found.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin in ["All", 0]) else str(z_pT_Bin)])))
            Drawing_Histo_Title = (str(Drawing_Histo_Set.GetTitle()).replace("yz projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin not in ["All", 0]) else "All", "}}}"]))
            Drawing_Histo_Title = str(Drawing_Histo_Title).replace("Cut: Complete Set of SIDIS Cuts", "")
            if(Data_Type == "mdf"):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Reconstructed")
            if(Data_Type == "gdf"):
                Drawing_Histo_Title = Drawing_Histo_Title.replace("Experimental", "MC Generated")
            Drawing_Histo_Set.SetTitle(Drawing_Histo_Title)
            # print(str(Drawing_Histo_Set.GetTitle()))
        except:
            print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (2D Histograms):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
    else:
        Drawing_Histo_Set = Drawing_Histo_Found
    ##===============##     3D Slices     ##===============##
    #########################################################
    # Draw_Canvas(Canvas_Input, CD_Num, 0.15)
    Draw_Canvas(canvas=Canvas_Input, cd_num=CD_Num, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
    Drawing_Histo_Set.Draw("colz")
    
    Canvas_Input.Modified()
    Canvas_Input.Update()
    
    palette_move(canvas=Canvas_Input, histo=Drawing_Histo_Set, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    
    if("Var-D1='Q2" in str(Find_Name) and "Var-D2='xB" in str(Find_Name)):
        Drawing_Histo_Set.SetTitle((Drawing_Histo_Set.GetTitle()).replace("Q^{2}-x_{B} Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin not in ["All", 0]) else "All", "}"])))
        # print("".join([color.BLUE, "Q2-xB plots:", color.END, "\n", str(Drawing_Histo_Set.GetTitle()), "\n", str(Find_Name), "\n\n"]))
        Q2_xB_borders, line_num = {}, 0
        for b_lines in Q2_xB_Border_Lines(-1):
            Q2_xB_borders[line_num] = ROOT.TLine()
            Q2_xB_borders[line_num].SetLineColor(1)    
            Q2_xB_borders[line_num].SetLineWidth(2)
            Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
            line_num += 1
        if(Q2_xB_Bin not in ["All", 0]):
            
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
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")]))
        
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
                Unfolded_Histo.SetMarkerSize(5)
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
            print("".join(["nBins_CVM = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX() = ", str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX() = ", str(MC_GEN_1D.GetNbinsX())]))
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
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(MC_REC_1D.GetName()).replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", ""), "\n"]))
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
            
            cut_criteria = (0.01*Bin_Acceptance.GetMaximum())
            
            # for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
            #     if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
            #         print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...", color.END]))
            #         Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BOLD, color.CYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
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
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")]))
        
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
                    gen_val = Response_2D.GetXaxis().GetBinCenter(gen_bin)
                    ##======================================##
                    ##=====##   Reconstructed Bins   ##=====##
                    ##======================================##
                    for rec_bin in range(0, nBins_CVM + 1, 1):
                        rec_val = Response_2D.GetYaxis().GetBinCenter(rec_bin)
                        Res_Val = Response_2D.GetBinContent(gen_bin, rec_bin)
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
================================================================================================================================================""", color.BOLD, """
MAJOR ERROR: sum_of_gen is greater than gen_val_TRUE (i.e., there are more matched generated events than there should be generated events total)
             Error in this aspect of the code (need to check procedure/rewrite code)""", color.END, color.RED, """
================================================================================================================================================
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
                    bayes_iterations = 10
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
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                
        else:
            print("".join([color.RED, "Unequal Bins...", color.END]))
            print("".join(["nBins_CVM = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX() = ", str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX() = ", str(MC_GEN_1D.GetNbinsX())]))
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
        file = "".join(["REAL_Data/SIDIS_epip_Data_REC_", str(FileName), ".root"])
    if(str(Datatype) == 'mdf'):
        file = "".join(["Matching_REC_MC/SIDIS_epip_MC_Matched_", str(FileName), ".root"])
    if(str(Datatype) == 'gdf'):
        file = "".join(["GEN_MC/SIDIS_epip_MC_GEN_", str(FileName), ".root"])
        
    loading = "".join([location, file])
    
    return loading



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
Common_Name = "Unfolding_Tests_V13_All"
Common_Name = "Analysis_Note_Update_V4_All"
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
    print("".join([color.BOLD, "\nNot using the common file name for the Reconstructed Monte Carlo Data...\n", color.END]))
if(False):
    MC_REC_File_Name = Common_Name
else:
    MC_REC_File_Name = "Unfolding_Tests_V13_Failed_All"
    MC_REC_File_Name = "Analysis_Note_Update_V6_All"
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
    print("".join(["The total number of histograms available for the", color.BLUE , " Real (Experimental) Data", color.END, " in '", color.BOLD, REAL_File_Name, color.END, "' is ", color.BOLD, str(len(rdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
try:
    mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
    print("".join(["The total number of histograms available for the", color.RED , " Reconstructed Monte Carlo Data", color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetListOfKeys())), color.END]))
except:
    print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
try:
    gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
    print("".join(["The total number of histograms available for the", color.GREEN , " Generated Monte Carlo Data", color.END, " in '", color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetListOfKeys())), color.END]))
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
count, count_failed = 0, 0
for ii in mdf.GetListOfKeys():
    out_print_main = str(ii.GetName()).replace("mdf", "DataFrame_Type")
    
    ##========================================================##
    ##=====##    Conditions for Histogram Selection    ##=====##
    ##========================================================##
    
    Conditions_For_Unfolding = ["DataFrame_Type" in str(out_print_main)]
    
    ## Correct Histogram Type:
    Conditions_For_Unfolding.append("Response_Matrix_Normal" in str(out_print_main))
    Conditions_For_Unfolding.append("Response_Matrix_Normal_1D" not in str(out_print_main))
    
    ## Correct Cuts:
    Conditions_For_Unfolding.append("no_cut" not in str(out_print_main))
    Conditions_For_Unfolding.append("cut_Complete_EDIS" not in str(out_print_main))

    ## Correct Variable(s):
    # Conditions_For_Unfolding.append("phi_t" in str(out_print_main))
    # Conditions_For_Unfolding.append("'phi_t" not in str(out_print_main))
    # Conditions_For_Unfolding.append("'Combined_Q2_xB_Bin_2_" not in str(out_print_main))
    Conditions_For_Unfolding.append("'Combined_" not in str(out_print_main))
    
    ## Correct Binning:
    # Conditions_For_Unfolding.append("Q2-xB-Bin=1" in str(out_print_main))
    # Conditions_For_Unfolding.append("Q2-xB-Bin=All" not in str(out_print_main))
    
    # Smearing Options:
    if(Smearing_Options not in ["no_smear", "both"]):
        Conditions_For_Unfolding.append("(Smear-Type='')" not in str(out_print_main))
    if(Smearing_Options not in ["smear", "both"]):
        Conditions_For_Unfolding.append("(Smear-Type='')" in str(out_print_main))
    
    ##========================================================##
    ##=====##    Conditions for Histogram Selection    ##=====##
    ##========================================================##
    
    if(False in Conditions_For_Unfolding):
        # Conditions for unfolding were not met by 'out_print_main'
        # print(Conditions_For_Unfolding)
        count_failed += 1
        # print("".join([color.RED, str(out_print_main), color.END]))
        # print("".join(["Number Failed: ", str(count_failed)]))
        continue
    else:

        out_print_main_rdf = out_print_main.replace("DataFrame_Type", "rdf")
        out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
        out_print_main_gdf = out_print_main.replace("DataFrame_Type", "gdf")

        ################################################################################
        ##=============##    Removing Cuts from the Generated files    ##=============##
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_EDIS", "no_cut")
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_SIDIS", "no_cut")
        out_print_main_gdf = out_print_main_gdf.replace("cut_Complete", "no_cut")
        ##=============##    Removing Cuts from the Generated files    ##=============##
        ################################################################################


        #############################################################################
        ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
        out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
        out_print_main_rdf = out_print_main_rdf.replace("smear_", "")
        out_print_main_rdf = out_print_main_rdf.replace("smear", "")
        out_print_main_gdf = out_print_main_gdf.replace("_smeared", "")
        out_print_main_gdf = out_print_main_gdf.replace("smear_", "")
        out_print_main_gdf = out_print_main_gdf.replace("smear", "")
        ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
        #############################################################################


        #############################################################################
        ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
        out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
        out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
        out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix'", "'Response_Matrix_1D'")
        out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix'", "'Response_Matrix_1D'")
        ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
        #############################################################################

        if(out_print_main_mdf not in mdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf), color.END, "\n"]))
            continue

        out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
        if((", (Var-D2='z_pT_Bin_2" not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
            out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "]), (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))" if("smear" not in str(out_print_main_mdf_1D)) else "]), (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))")
        if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN MDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, str(out_print_main_mdf_1D), color.END, "\n"]))
            for ii in mdf.GetListOfKeys():
                if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                    print(str(ii.GetName()))
            
        if(out_print_main_rdf not in rdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN RDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.BLUE, str(out_print_main_rdf), color.END, "\n"]))
            continue

        if(out_print_main_gdf not in gdf.GetListOfKeys()):
            print("".join([color.BOLD, color.RED, "ERROR IN GDF...\n", color.END, color.RED, "Dataframe is missing: ", color.BOLD, color.GREEN, str(out_print_main_gdf), color.END, "\n"]))
            continue


        
        
        count += 1
        # print("".join([color.BOLD, str(out_print_main_mdf_1D), color.END]))
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

        Q2_xB_Bin_Unfold = 0 if("Q2-xB-Bin=All" in str(out_print_main)) else 1 if("Q2-xB-Bin=1" in str(out_print_main)) else 2 if("Q2-xB-Bin=2" in str(out_print_main)) else 3 if("Q2-xB-Bin=3" in str(out_print_main)) else 4 if("Q2-xB-Bin=4" in str(out_print_main)) else 5 if("Q2-xB-Bin=5" in str(out_print_main)) else 6 if("Q2-xB-Bin=6" in str(out_print_main)) else 7 if("Q2-xB-Bin=7" in str(out_print_main)) else 8 if("Q2-xB-Bin=8" in str(out_print_main)) else 9 if("Q2-xB-Bin=9" in str(out_print_main)) else 10 if("Q2-xB-Bin=10" in str(out_print_main)) else "Undefined..."
        if(type(Q2_xB_Bin_Unfold) is str):
            print("".join([color.RED, color.BOLD, "\nERROR - Q2_xB_Bin_Unfold = ", str(Q2_xB_Bin_Unfold), color.END]))

        if(str(Q2_xB_Bin_Unfold) not in Q2_xB_Bin_List):
            # print("Skipping unselected Q2-xB Bin...")
            print("".join(["Bin ", str(Q2_xB_Bin_Unfold), " is not in Q2_xB_Bin_List = ", str(Q2_xB_Bin_List)]))
            continue
            
        test = Canvas_Create(Name="".join([str(out_print_main), str(Q2_xB_Bin_Unfold)]), Num_Columns=1, Num_Rows=1, Size_X=60, Size_Y=80, cd_Space=0)
        # test.Draw()

        z_pT_Bin_Range = 0 if("Q2-xB-Bin=All" in str(out_print_main)) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3]) else 42 if(Q2_xB_Bin_Unfold in [4]) else 36 if(Q2_xB_Bin_Unfold in [5]) else 25 if(Q2_xB_Bin_Unfold in [6, 7]) else 20 if(Q2_xB_Bin_Unfold in [8]) else 1
        
        # if(Q2_xB_Bin_Unfold != 1):
        #     continue
        # z_pT_Bin_Range = 1

        for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
            # Bin_Title = "" if(z_pT_Bin_Unfold == 0) else "".join(["z-P_{T} Bin: ", str(z_pT_Bin_Unfold)])

            if(((Q2_xB_Bin_Unfold in [1, 2]) and (z_pT_Bin_Unfold in [49])) or (Q2_xB_Bin_Unfold == 3 and z_pT_Bin_Unfold in [49, 48, 42]) or (Q2_xB_Bin_Unfold in [1, 4] and z_pT_Bin_Unfold in [42]) or (Q2_xB_Bin_Unfold == 5 and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold == 7 and z_pT_Bin_Unfold in [25])):
                # print("Testing z_pT_Bin_Unfold...")
                continue

    #########################################################
    ##===============##     3D Slices     ##===============##

            if("3D" in str(type(Response_2D_initial))):
                try:
                    bin_Response_2D_0, bin_Response_2D_1 = Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else Response_2D_initial.GetNbinsZ())
                    if(z_pT_Bin_Unfold != 0):
                        Response_2D_initial.GetZaxis().SetRange(bin_Response_2D_0, bin_Response_2D_1)
                    Response_2D = Response_2D_initial.Project3D('yx')
                    Response_2D.SetName(str(Response_2D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])))
                    Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
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
                    ExREAL_1D = ExREAL_1D_initial.ProjectionX(str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExREAL_1D_0, bin_ExREAL_1D_1)
                    ExREAL_1D_Title_New = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    ExREAL_1D.SetTitle(ExREAL_1D_Title_New)
                    # print("\n" + color.BOLD + str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])) + color.END)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (ExREAL_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                print("\nExREAL_1D already is a 1D Histogram...")
                ExREAL_1D = ExREAL_1D_initial

            if("2D" in str(type(MC_REC_1D_initial))):
                try:
                    bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                    MC_REC_1D = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_REC_1D_0, bin_MC_REC_1D_1)
                    MC_REC_1D_Title_New = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_REC_1D.SetTitle(MC_REC_1D_Title_New)
                    # print("\n" + color.BOLD + str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])) + color.END)
                except:
                    print("".join([color.RED, color.BOLD, "\nERROR IN z-pT BIN SLICING (MC_REC_1D):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            else:
                print("\nMC_REC_1D already is a 1D Histogram...")
                MC_REC_1D = MC_REC_1D_initial

            if("2D" in str(type(MC_GEN_1D_initial))):
                try:
                    bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 0), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                    MC_GEN_1D = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_GEN_1D_0, bin_MC_GEN_1D_1)
                    MC_GEN_1D_Title_New = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                    MC_GEN_1D.SetTitle(MC_GEN_1D_Title_New)
                    # print("\n" + color.BOLD + str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])) + color.END)
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



            if("phi_t" not in out_print_main and "phi_t_smeared'" not in out_print_main):
                if((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)):
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
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(z_Bin_Range), str(z_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(z_Bin_Range), str(z_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(z_Bin_Range), str(z_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(z_Bin_Range), str(z_Bin_Replace_Range))))
            
            ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
            MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
            MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
            Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
            
            if("Var-D1='Q2" in out_print_main):
                ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV^{2}]"]))
                
            if("Var-D1='pT" in out_print_main):
                ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()), " [GeV]"]))
                MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()), " [GeV]"]))
                MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()), " [GeV]"]))
                Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV]"]))
                Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV]"]))


            try:
                out_print_main_binned = out_print_main.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)]))
                if("'Combined_" not in str(out_print_main)):
                    try:
                        Unfolding_Histograms  = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default")
                        Unfolding_Histogram_1 = Unfolding_Histograms[0]
                    except:
                        print("".join([color.BOLD, color.RED, "ERROR IN SVD UNFOLDING ('Unfolding_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                else:
                    Unfolding_Histogram_1 = MC_GEN_1D.Add(MC_GEN_1D, -1)
                try:
                    Bin_Method_Histograms = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin")
                    Bin_Unfolded[out_print_main_binned], Bin_Acceptance[out_print_main_binned] = Bin_Method_Histograms
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                    
                try: 
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])]   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes"))[0]
                    if("'Combined_" not in str(out_print_main)):
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_svd"))[0]
                    else:
                        RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])]
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])]   = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bbb"))[0]
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold UNFOLDING METHOD(s):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                
                Plot_Version = "Web"
                Plot_Version = "Note"
                
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
                    Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # if(Plot_Version == "Web"):
                    #     Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # elif(Plot_Version == "Note"):
                    #     Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                    # Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Unfolding_Histogram_1, Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])]], Norm_Q="Norm")
                    # Unfolded_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[Bin_Unfolded[out_print_main_binned], MC_GEN_1D, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])], RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])]], Norm_Q="Norm")
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN Y-AXIS MAXIMUM (Unfolded)...", color.END]))
                    Unfolded_Max = 1
                    print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    Data_REC_Max = 1.2*Get_Max_Y_Histo_1D(Histo_List=[ExREAL_1D, MC_REC_1D], Norm_Q="Norm")
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN Y-AXIS MAXIMUM (Reconstructed)...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    Response_2D.GetXaxis().SetRange(1, Response_2D.GetXaxis().GetNbins() + 2)
                    Response_2D.GetYaxis().SetRange(1, Response_2D.GetYaxis().GetNbins() + 2)
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN 2D Matrix Ranges...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                try:
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].GetXaxis().SetRange(1, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].GetXaxis().GetNbins() + 1)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].GetXaxis().SetRange(1,   RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].GetXaxis().GetNbins() + 1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].GetXaxis().SetRange(1,   RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].GetXaxis().GetNbins() + 1)
                    Bin_Unfolded[out_print_main_binned].GetXaxis().SetRange(1, Bin_Unfolded[out_print_main_binned].GetXaxis().GetNbins() + 1)
                    MC_GEN_1D.GetXaxis().SetRange(1, MC_GEN_1D.GetXaxis().GetNbins() + 1)
                    ExREAL_1D.GetXaxis().SetRange(1, ExREAL_1D.GetXaxis().GetNbins() + 1)
                    MC_REC_1D.GetXaxis().SetRange(1, MC_REC_1D.GetXaxis().GetNbins() + 1)
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN 1D X-Axis Ranges...", color.END]))
                    print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
    ##=====##=====##   Axis Ranges   ##=====##=====##
    #################################################
    ##=====##=====##  Legends Setup  ##=====##=====##
                if("phi_t" not in out_print_main_binned and "'phi_t_smeared'" not in out_print_main_binned):
                    Legends[(out_print_main_binned, "Unfolded")] = ROOT.TLegend(0.5, 0.5, 0.95, 0.75)
                else:
                    Legends[(out_print_main_binned, "Unfolded")] = ROOT.TLegend(0.25, 0.15, 0.85, 0.55)
                Legends[(out_print_main_binned, "Unfolded")].SetNColumns(2)
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
                    Bin_Unfolded[out_print_main_binned].SetLineWidth(2)
                    Bin_Unfolded[out_print_main_binned].SetLineStyle(1)
                    Bin_Unfolded[out_print_main_binned].SetMarkerColor(root_color.Brown)
                    Bin_Unfolded[out_print_main_binned].SetMarkerSize(1)
                    Bin_Unfolded[out_print_main_binned].SetMarkerStyle(21)
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN DRAWING BIN UNFOLDING ('Bin_Unfolded[out_print_main]'):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                    
                try:
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].GetYaxis().SetTitle("Normalized")
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].GetYaxis().SetTitle("Normalized")
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].GetYaxis().SetTitle("Normalized")

                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineColor(30)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineColor(46)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineColor(41)
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineWidth(2)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineWidth(2)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineWidth(2)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetLineStyle(1)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetLineStyle(1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetLineStyle(1)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerColor(30)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerColor(46)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerColor(41)
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerSize(1)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerSize(1)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerSize(1)
                    
                    
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].SetMarkerStyle(21)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].SetMarkerStyle(21)
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].SetMarkerStyle(21)
                    

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
                    MC_GEN_1D.SetLineWidth(3)
                    MC_GEN_1D.SetLineStyle(1)
                    MC_GEN_1D.SetMarkerColor(root_color.Green)
                    MC_GEN_1D.SetMarkerSize(1)
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
                    if(Plot_Version == "Web"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=2, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        ROOT.gPad.SetLogz(1)
                        Response_2D.Draw("colz")
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=1, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        ROOT.gPad.SetLogz(1)
                        Response_2D.Draw("col")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        Save_Response_Matrix["".join(["Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = Response_2D.Clone()
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
                    if(Plot_Version == "Web"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_1, cd_num=4, left_add=0.1, right_add=0.075, up_add=0.1, down_add=0.1)
                        Unfolding_Histogram_1_Norm = (Unfolding_Histogram_1.DrawNormalized("PL E0 same"))
                        for ii in range(0, Unfolding_Histogram_1_Norm.GetNbinsX() + 1, 1):
                            if(Unfolding_Histogram_1_Norm.GetBinError(ii) > 0.01):
                                print("".join([color.RED, "\n(SVD Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                                Unfolding_Histogram_1_Norm.SetBinContent(ii, 0)
                                Unfolding_Histogram_1_Norm.SetBinError(ii, 0)
                        Unfolding_Histogram_1_Norm.GetYaxis().SetRangeUser(0, Unfolded_Max)
                        Legends[(out_print_main_binned, "Unfolded")].AddEntry(Unfolding_Histogram_1, "#scale[2]{SVD Unfolded}", "lpE")
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=2, left_add=0.1, right_add=0.05, up_add=0.1, down_add=0.1)
                        Bin_Unfolded[out_print_main_binned].SetTitle(str(Bin_Unfolded[out_print_main_binned].GetTitle()).replace("Bin-By-Bin Unfolded Distribution", "Unfolded Distributions"))
                    
                    # Bin_Unfolded[(out_print_main_binned, "Norm")] = (Bin_Unfolded[out_print_main_binned].DrawNormalized("H PL E0 same"))
                    Bin_Unfolded[(out_print_main_binned, "Norm")] = (Bin_Unfolded[out_print_main_binned].DrawNormalized("PL E0 same"))
                    for ii in range(0, Bin_Unfolded[(out_print_main_binned, "Norm")].GetNbinsX() + 1, 1):
                        if(Bin_Unfolded[(out_print_main_binned, "Norm")].GetBinError(ii) > 0.01):
                            print("".join([color.RED, "\n(Bin-by-Bin Unfolded) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                            Bin_Unfolded[(out_print_main_binned, "Norm")].SetBinContent(ii, 0)
                            Bin_Unfolded[(out_print_main_binned, "Norm")].SetBinError(ii, 0)
                    Legends[(out_print_main_binned, "Unfolded")].AddEntry(Bin_Unfolded[out_print_main_binned], "#scale[2]{Bin-by-Bin}", "lpE")
                    
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])] = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].DrawNormalized("H PL E0 same"))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])] = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes"])].DrawNormalized("PL E0 same"))
                    for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetNbinsX() + 1, 1):
                        if(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetBinError(ii) > 0.01):
                            print("".join([color.RED, "\n(RooUnfold (Bayesian) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].SetBinContent(ii, 0)
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].SetBinError(ii, 0)
                    Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])], "#scale[2]{Bayesian}", "lpE")
                    
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].DrawNormalized("H PL E0 same"))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd"])].DrawNormalized("PL E0 same"))
                    for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].GetNbinsX() + 1, 1):
                        if(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].GetBinError(ii) > 0.01):
                            print("".join([color.RED, "\n(RooUnfold (SVD) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].SetBinContent(ii, 0)
                            RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].SetBinError(ii, 0)
                    Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])], "#scale[2]{SVD (RooUnfold)}", "lpE")
                    
                    # RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])]   = (RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb"])].DrawNormalized("PL E0 same"))
                    # for ii in range(0, RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].GetNbinsX() + 1, 1):
                    #     if(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].GetBinError(ii) > 0.01):
                    #         print("".join([color.RED, "\n(RooUnfold (Bin-by-Bin) Bin ", str(ii), " has a large error (after normalizing)...", color.END]))
                    #         RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].SetBinContent(ii, 0)
                    #         RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])].SetBinError(ii, 0)
                    # Legends[(out_print_main_binned, "Unfolded")].AddEntry(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm"])], "#scale[2]{Bin-by-Bin (RooUnfold)}", "lpE")

                    # Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("H PL E0 same")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = MC_GEN_1D.DrawNormalized("PL E0 same")
                    else:
                        MC_GEN_1D.DrawNormalized("PL E0 same")
                    Legends[(out_print_main_binned, "Unfolded")].AddEntry(MC_GEN_1D, "#scale[2]{MC GEN}", "lpE")

                    Legends[(out_print_main_binned, "Unfolded")].Draw("same")
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Unfolding Histograms):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

    ##################################################################
    ##==========##==========##     CD 2     ##==========##==========##
    ##################################################################
    ##=====##=====##    Drawing the Bin Acceptance    ##=====##=====##
                try:
                    if(Plot_Version == "Web"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=3, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
                    elif(Plot_Version == "Note"):
                        Draw_Canvas(canvas=Unfolded_Canvas_main_Row_2, cd_num=1, left_add=0.15, right_add=0.05, up_add=0.1, down_add=0.1)
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

                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        if(Plot_Version == "Web"):
                            Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = (ExREAL_1D.DrawNormalized("H PL E0 same"))
                        else:
                            Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = (ExREAL_1D.DrawNormalized("PL E0 same"))
                        # Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])] = ExREAL_1D_Norm.Clone()
                        Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold)])].GetYaxis().SetRangeUser(0, Data_REC_Max)
                    else:
                        if(Plot_Version == "Web"):
                            ExREAL_1D_Norm = (ExREAL_1D.DrawNormalized("H PL E0 same"))
                        else:
                            ExREAL_1D_Norm = (ExREAL_1D.DrawNormalized("PL E0 same"))
                        ExREAL_1D_Norm.GetYaxis().SetRangeUser(0, Data_REC_Max)
                    Legends[(out_print_main_binned, "REC")].AddEntry(ExREAL_1D, "#scale[2]{Experimental}" if(Plot_Version == "Web") else "#scale[1]{Experimental}", "lpE")
                    if("phi_t" in out_print_main or "phi_t_smeared'" in out_print_main):
                        if(Plot_Version == "Web"):
                            Save_Response_Matrix["".join(["MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = MC_REC_1D.DrawNormalized("H PL E0 same")
                        else:
                            Save_Response_Matrix["".join(["MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin_Unfold), " z-pT Bin:", str(z_pT_Bin_Unfold), "_Smeared" if("_smeared" in str(out_print_main)) else ""])] = MC_REC_1D.DrawNormalized("PL E0 same")
                    else:
                        if(Plot_Version == "Web"):
                            MC_REC_1D.DrawNormalized("H PL E0 same")
                        else:
                            MC_REC_1D.DrawNormalized("PL E0 same")
                    # MC_REC_1D_Norm = (MC_REC_1D.DrawNormalized("PL E1 same"))
                    Legends[(out_print_main_binned, "REC")].AddEntry(MC_REC_1D, "#scale[2]{MC REC}" if(Plot_Version == "Web") else "#scale[1]{MC REC}", "lpE")
                    Legends[(out_print_main_binned, "REC")].Draw("same")
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (Experimental/Reconstructed):\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                    
                    
                    
    ##################################################################
    ##==========##==========##   CD Extra   ##==========##==========##
    ##################################################################
    ##=====##=====##   Drawing the Extra 2D Histos    ##=====##=====##
                try:
                    if(Plot_Version == "Web"):
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=1, Var_D1="Q2", Var_D2="xB", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_1, CD_Num=2, Var_D1="z",  Var_D2="pT", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")

                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=1, Var_D1="el", Var_D2="elth",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=2, Var_D1="el", Var_D2="elPhi", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=3, Var_D1="pip", Var_D2="pipth",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")
                        Draw_2D_Histograms_Simple(DataFrame=rdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=4, Var_D1="pip", Var_D2="pipPhi", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="rdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="")

                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=5, Var_D1="el" if("smear" not in str(out_print_main_mdf)) else "el_smeared", Var_D2="elth"  if("smear" not in str(out_print_main_mdf)) else "elth_smeared",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=6, Var_D1="el" if("smear" not in str(out_print_main_mdf)) else "el_smeared", Var_D2="elPhi" if("smear" not in str(out_print_main_mdf)) else "elPhi_smeared", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=7, Var_D1="pip" if("smear" not in str(out_print_main_mdf)) else "pip_smeared", Var_D2="pipth"  if("smear" not in str(out_print_main_mdf)) else "pipth_smeared",  Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                        Draw_2D_Histograms_Simple(DataFrame=mdf, Canvas_Input=Unfolded_Canvas_main_Row_3, CD_Num=8, Var_D1="pip" if("smear" not in str(out_print_main_mdf)) else "pip_smeared", Var_D2="pipPhi" if("smear" not in str(out_print_main_mdf)) else "pipPhi_smeared", Q2_xB_Bin=Q2_xB_Bin_Unfold, z_pT_Bin=z_pT_Bin_Unfold, Data_Type="mdf", Cut_Type="cut_Complete_SIDIS", Smear_Q="" if("smear" not in str(out_print_main_mdf)) else "smear")
                    
                except:
                    print("".join([color.BOLD, color.RED, "ERROR IN CANVAS (2D Histograms):\n", color.END, str(traceback.format_exc())]))
                    
                    
                    


#########################################################################################################################
##==================================#################################################==================================##
##==========##==========##==========##   Openning Canvas Pads to Draw Histograms   ##==========##==========##==========##
##==================================#################################################==================================##
#########################################################################################################################

                Unfolded_Canvas[out_print_main_binned].Modified()
                Unfolded_Canvas[out_print_main_binned].Update()

                if("phi_t" in out_print_main_binned):
                    # fit_function_title = "A + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h})"
                    # fit_function = "[A] + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180))"
                    fit_function_title = "A + B Cos(#phi_{h}) + C Cos(2#phi_{h})"
                    fit_function = "[A] + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180))"


                    fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
                    fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"


                    # Q2_xB_Bin_Title = "" if("Q2-xB-Bin=All" in str(out_print_main)) else "".join(["Q^{2}-x_{B} Bin: ", "1" if("Q2-xB-Bin=1" in str(out_print_main)) else "2" if("Q2-xB-Bin=2" in str(out_print_main)) else "3" if("Q2-xB-Bin=3" in str(out_print_main)) else "4" if("Q2-xB-Bin=4" in str(out_print_main)) else "5" if("Q2-xB-Bin=5" in str(out_print_main)) else "6" if("Q2-xB-Bin=6" in str(out_print_main)) else "7" if("Q2-xB-Bin=7" in str(out_print_main)) else "8" if("Q2-xB-Bin=8" in str(out_print_main)) else "9" if("Q2-xB-Bin=9" in str(out_print_main)) else "Error"])
                    Q2_xB_Bin_Title = "" if("Q2-xB-Bin=All" in str(out_print_main)) else "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"])
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
                    
                    
                    ###################################################################
                    ##==========##         Bayesian Unfolded Fit         ##==========##
                    ###################################################################
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 1, 0.15)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].Clone()
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(30),"]{RooUnfold Bayesian} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetYaxis().SetTitle("")
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetXaxis().SetTitle(str(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm"])].GetXaxis().GetTitle()).replace("(REC)", ""))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                    A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_bayes_Norm_extra"])])
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

                    A_Unfold, B_Unfold, C_Unfold = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    Parameter_List_Unfold_Methods["Bayes"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, B_Unfold, C_Unfold, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

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
                    Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_upper"])], 2, 0.15)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])] = RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].Clone()
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(46),"]{RooUnfold SVD} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetYaxis().SetTitle("")
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetXaxis().SetTitle(str(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm"])].GetXaxis().GetTitle()).replace("(REC)", ""))
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                    RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                    A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(RooUnfolded_Histos["".join([str(out_print_main_binned), "_svd_Norm_extra"])])
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

                    # A_Unfold, B_Unfold, C_Unfold = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    # Parameter_List_Unfold_Methods["SVD_RooUnfold"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, B_Unfold, C_Unfold, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

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
#                     # A_Unfold, B_Unfold, C_Unfold = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
#                     # Parameter_List_Unfold_Methods["bbb"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, B_Unfold, C_Unfold, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])
#
#                     # statbox_move_new(Histogram=Unfolding_Histogram_1_Norm, Canvas=Unfolded_Canvas["".join([str(out_print_main), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
#                     statbox_move(Histogram=RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
#                     # Unfolded_C_clone.ShowPeaks()
#                     RooUnfolded_Histos["".join([str(out_print_main_binned), "_bbb_Norm_extra"])].GetXaxis().SetRangeUser(0, 360)
#                     #####################################################################
#                     ##==========##   (RooUnfold) Bin-by-Bin Unfolded Fit   ##==========##
#                     #####################################################################
                    
                    
                    
                    ###################################################################
                    ##==========##      (Original) SVD Unfolded Fit      ##==========##
                    ###################################################################
                    try:
                        Draw_Canvas(Unfolded_Canvas["".join([str(out_print_main_binned), "extra_cd_lower"])], 1, 0.15)
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])] = Unfolding_Histogram_1_Norm.Clone()
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].SetTitle("".join(["#splitline{#splitline{", root_color.Bold, "{Fitted #color[", str(root_color.Pink),"]{SVD Unfolded} Distribution of #phi_{h}}}{", root_color.Bold, "{Fit Function = ", str(fit_function_title), "}}}{", str(Q2_xB_Bin_Title), "}"]))
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetTitle("")
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetTitle(str(Unfolding_Histogram_1_Norm.GetXaxis().GetTitle()).replace("(REC)", ""))
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetYaxis().SetRangeUser(0, Unfolded_Max)
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].Draw("PL E1 same")
                        Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])])
                        # # print("\n".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]))
                        # Unfolded_Fit_Function.SetParameter(0, A_Unfold)
                        # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Unfold if(A_Unfold > 0) else 1.25*A_Unfold, 1.25*A_Unfold if(A_Unfold > 0) else 0.85*A_Unfold)
                        # Unfolded_Fit_Function.SetParameter(1, B_Unfold)
                        # Unfolded_Fit_Function.SetParLimits(1, 0.65*B_Unfold if(B_Unfold > 0) else 1.45*B_Unfold, 1.45*B_Unfold if(B_Unfold > 0) else 0.65*B_Unfold)
                        # Unfolded_Fit_Function.SetParameter(2, C_Unfold)
                        # Unfolded_Fit_Function.SetParLimits(2, 0.65*C_Unfold if(C_Unfold > 0) else 1.45*C_Unfold, 1.45*C_Unfold if(C_Unfold > 0) else 0.65*C_Unfold)
                        # # Unfolded_Fit_Function.SetParameter(0, A_Calc_Fit(Unfolded_C_clone))
                        # # Unfolded_Fit_Function.SetParLimits(0, 0.85*A_Calc_Fit(Unfolded_C_clone), 1.25*A_Calc_Fit(Unfolded_C_clone))
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].Fit(Unfolded_Fit_Function, "RQ")

                        A_Unfold, B_Unfold, C_Unfold = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                        Parameter_List_Unfold_Methods["SVD"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, B_Unfold, C_Unfold, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

                        statbox_move(Histogram=Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)#, Print_Method="norm"):
                        # Unfolded_C_clone.ShowPeaks()
                        Unfolding_Histogram_1_Norm_Clone["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetRangeUser(0, 360)
                    except:
                        print("".join([color.RED, "Error in SVD (TSVDUnfold):\n", str(traceback.format_exc()), color.END]))
                    ###################################################################
                    ##==========##      (Original) SVD Unfolded Fit      ##==========##
                    ###################################################################
                    


                    
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
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].Draw("PL E1 same")
                    Unfolded_Fit_Function = ROOT.TF1("Unfolded_Fit_Function", str(fit_function), 0, 360)
                    A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Bin_Unfolded["".join([str(out_print_main_binned), "extra"])])
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

                    A_Unfold, B_Unfold, C_Unfold = Unfolded_Fit_Function.GetParameter(0), Unfolded_Fit_Function.GetParameter(1), Unfolded_Fit_Function.GetParameter(2)
                    Parameter_List_Unfold_Methods["Bin"].append([Q2_xB_Bin_Unfold, z_pT_Bin_Unfold, A_Unfold, B_Unfold, C_Unfold, "" if("Smear-Type=''" in str(out_print_main_binned)) else "Smeared"])

                    # statbox_move_new(Histogram=Unfolding_Histogram_1_Norm, Canvas=Unfolded_Canvas["".join([str(out_print_main), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
                    statbox_move(Histogram=Bin_Unfolded["".join([str(out_print_main_binned), "extra"])], Canvas=Unfolded_Canvas["".join([str(out_print_main_binned), "extra"])], Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)#, Print_Method="norm"):
                    # Unfolded_C_clone.ShowPeaks()
                    Bin_Unfolded["".join([str(out_print_main_binned), "extra"])].GetXaxis().SetRangeUser(0, 360)
                    ###################################################################
                    ##==========##       (Original) Bin-by-Bin Fit       ##==========##
                    ###################################################################
                    


            except:
                print("".join([color.BOLD, color.RED, "ERROR IN UNFOLDING:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))



##===============##     Unfolding Histogram Procedure     ##===============##
#############################################################################





print("".join(["Total: ", str(count)]))



count_of_images = 0


print("".join([color.BOLD, color.GREEN, "\n\n\nDone Creating Unfolded Histograms (Now saving...)\n", color.END]))


for Canvas_name in Unfolded_Canvas:
    if("cd_upper" not in str(Canvas_name) and "cd_lower" not in str(Canvas_name)):
        Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), str(File_Save_Format)])
        if("smear" in str(Canvas_name)):
            Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), "_Smeared", str(File_Save_Format)])
        Save_Name = Save_Name.replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))", "")
        Save_Name = Save_Name.replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))", "")
        Save_Name = Save_Name.replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2'-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))", "")
        Save_Name = Save_Name.replace(", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2_smeared'-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))", "")
        Save_Name = Save_Name.replace("Smear-Type=''", "")
        Save_Name = Save_Name.replace("Smear-Type='smear'", "")
        Save_Name = str(str(Save_Name.replace("(", "")).replace(")", "").replace(", ", "_")).replace("'", "")
        Save_Name = str(Save_Name.replace("_Data-Type=DataFrame_Type", "")).replace("extra", "_Unfolded_Histos")
        Save_Name = str(Save_Name.replace("__", "_"))
        Save_Name = str(Save_Name.replace("Histo-Group=", ""))
        Save_Name = str(Save_Name.replace("Data-", ""))
        Save_Name = str(Save_Name.replace("z-PT-Bin=", "_z_pT_Bin_"))
        Save_Name = str(Save_Name.replace("Q2-xB-Bin=", "Q2_xB_Bin_"))
        Save_Name = str(Save_Name.replace("Binning-Type=2-[" , "_")).replace("]", "")
        Save_Name = str(Save_Name.replace("_Cut=cut_Complete_SIDIS", ""))
        Save_Name = Save_Name.replace("__", "_")
        
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0_MaxBin=1.05_Var-D2=z_pT_Bin_2-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0_MaxBin=1.05_Var-D2=z_pT_Bin_2_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0_MaxBin=1.05", "")
        
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.11944_MaxBin=0.73056_Var-D2=z_pT_Bin_2-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.11944_MaxBin=0.73056_Var-D2=z_pT_Bin_2_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.11944_MaxBin=0.73056", "")
        
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.08977_MaxBin=0.82643_Var-D2=z_pT_Bin_2-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.08977_MaxBin=0.82643_Var-D2=z_pT_Bin_2_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=0.08977_MaxBin=0.82643", "")
        
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=1.4805_MaxBin=11.8705_Var-D2=z_pT_Bin_2-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=1.4805_MaxBin=11.8705_Var-D2=z_pT_Bin_2_smeared-[NumBins=55_MinBin=-3.5_MaxBin=51.5", "")
        Save_Name = Save_Name.replace("-[NumBins=20_MinBin=1.4805_MaxBin=11.8705", "")
        
        Save_Name = Save_Name.replace("Q2_xB_Bin_All_z_pT_Bin_All_1D_Var-D1=", "All_Events_")
        if(Saving_Q):
            Unfolded_Canvas[Canvas_name].SaveAs(Save_Name)
        count_of_images += 1
        print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))

if(Saving_Q):
    print("".join([color.BOLD, color.GREEN, "\n\nDONE SAVING INDIVIDUAL PLOTS\n", color.END]))
else:
    print("".join([color.BOLD, color.RED, "\nNOT SAVING INDIVIDUAL PLOTS\n", color.END]))

    
    
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


print("".join([color.BOLD, color.GREEN, "\n\nDone with main Unfolded Histograms (Now getting parameter plots...)\n", color.END]))
Canvas_Parameters_List, Histo_Par_A_z, Histo_Par_B_z, Histo_Par_C_z, Histo_Par_A_pT, Histo_Par_B_pT, Histo_Par_C_pT, Par_Legends = {}, {}, {}, {}, {}, {}, {}, {}
for Method in ["Bayes", "SVD", "Bin"]:
    try:
        for bin_ii in Parameter_List_Unfold_Methods[Method]:
            Q2_xB_Bin, z_pT_Bin, Par_A, Par_B, Par_C, Smearing_Title = bin_ii
            if(z_pT_Bin == 0):
                continue
            z_value, pT_value = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Default")
            z_value_title, pT_value_title = Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="Title")

            if("Error" in [z_value, pT_value]):
                print("".join([color.BOLD, color.RED, "ERROR IN Q2-xB Bin ",  str(Q2_xB_Bin), " --- z-pT Bin ",  str(z_pT_Bin), color.END]))
                print("".join(["z_value = ", str(z_value), "\tpT_value = ", str(pT_value)]))

            Histo_Name_z  = "".join([str(pT_value_title), "_Unfold_", str(Method), "".join(["_", str(Smearing_Title)]) if("" != Smearing_Title) else "", "_Q2_xB_Bin_", str(Q2_xB_Bin)])
            Histo_Name_pT = "".join([str(z_value_title),  "_Unfold_", str(Method), "".join(["_", str(Smearing_Title)]) if("" != Smearing_Title) else "", "_Q2_xB_Bin_", str(Q2_xB_Bin)])
            Unfolding_Title_Name = "bin-by-bin" if(Method == "Bin") else "Bayesian" if(Method == "Bayes") else str(Method)

            # try:
            #     Histo_Par_A_z[Histo_Name_z]
            # except:
            #     # Histo_Par_A_z[Histo_Name_z] = ROOT.TGraphErrors()
            #     Histo_Par_A_z[Histo_Name_z] = ROOT.TGraph()
            #     Histo_Par_A_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_A"]))
            #     Histo_Par_A_z[Histo_Name_z].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit Parameter A from ", str(Unfolding_Title_Name), " unfolding}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{P_{T} Bin: ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), "}; z; Parameter A"]))
            try:
                Histo_Par_B_z[Histo_Name_z]
            except:
                # Histo_Par_B_z[Histo_Name_z] = ROOT.TGraphErrors()
                Histo_Par_B_z[Histo_Name_z] = ROOT.TGraph()
                Histo_Par_B_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_B"]))
                Histo_Par_B_z[Histo_Name_z].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter B}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{P_{T} Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), " [GeV]}; z; Parameter B"]))
            try:
                Histo_Par_C_z[Histo_Name_z]
            except:
                # Histo_Par_C_z[Histo_Name_z] = ROOT.TGraphErrors()
                Histo_Par_C_z[Histo_Name_z] = ROOT.TGraph()
                Histo_Par_C_z[Histo_Name_z].SetName("".join([str(Histo_Name_z), "_Par_C"]))
                Histo_Par_C_z[Histo_Name_z].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter C}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{P_{T} Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="pT_title")), " [GeV]}; z; Parameter C"]))

            # try:
            #     Histo_Par_A_pT[Histo_Name_pT]
            # except:
            #     # Histo_Par_A_pT[Histo_Name_pT] = ROOT.TGraphErrors()
            #     Histo_Par_A_pT[Histo_Name_pT] = ROOT.TGraph()
            #     Histo_Par_A_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT),  "_Par_A"]))
            #     Histo_Par_A_pT[Histo_Name_pT].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit Parameter A from ", str(Unfolding_Title_Name), " unfolding}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{z Bin: ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title")), "}; P_{T}; Parameter A"]))
            try:
                Histo_Par_B_pT[Histo_Name_pT]
            except:
                # Histo_Par_B_pT[Histo_Name_pT] = ROOT.TGraphErrors()
                Histo_Par_B_pT[Histo_Name_pT] = ROOT.TGraph()
                Histo_Par_B_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT), "_Par_B"]))
                Histo_Par_B_pT[Histo_Name_pT].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter B}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{z Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title")), "}; P_{T} [GeV]; Parameter B"]))
            try:
                Histo_Par_C_pT[Histo_Name_pT]
            except:
                # Histo_Par_C_pT[Histo_Name_pT] = ROOT.TGraphErrors()
                Histo_Par_C_pT[Histo_Name_pT] = ROOT.TGraph()
                Histo_Par_C_pT[Histo_Name_pT].SetName("".join([str(Histo_Name_pT), "_Par_C"]))
                Histo_Par_C_pT[Histo_Name_pT].SetTitle("".join(["#splitline{#splitline{", "(Smeared) " if("" != Smearing_Title) else "", "Fit ", root_color.Bold, "{#color[", str(root_color.Blue), "]{Parameter C}} from ", root_color.Bold, "{#color[", str(root_color.Red), "]{", str(Unfolding_Title_Name), "} unfolding}}{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "}}{", root_color.Bold, "{z Bin:} ", str(Find_z_pT_Bin_Center(Q2_xB_Bin, z_pT_Bin, variable_return="z_title")), "}; P_{T} [GeV]; Parameter C"]))

            # Histo_Par_A_z[Histo_Name_z].SetPoint(Histo_Par_A_z[Histo_Name_z].GetN(), z_value, Par_A)
            Histo_Par_B_z[Histo_Name_z].SetPoint(Histo_Par_B_z[Histo_Name_z].GetN(), z_value, Par_B)
            Histo_Par_C_z[Histo_Name_z].SetPoint(Histo_Par_C_z[Histo_Name_z].GetN(), z_value, Par_C)

            # Histo_Par_A_pT[Histo_Name_pT].SetPoint(Histo_Par_A_pT[Histo_Name_pT].GetN(), pT_value, Par_A)
            Histo_Par_B_pT[Histo_Name_pT].SetPoint(Histo_Par_B_pT[Histo_Name_pT].GetN(), pT_value, Par_B)
            Histo_Par_C_pT[Histo_Name_pT].SetPoint(Histo_Par_C_pT[Histo_Name_pT].GetN(), pT_value, Par_C)


        #################################################################################################################################################################################################################################################################################################################################################
        #################################################################################################################################################################################################################################################################################################################################################
        #################################################################################################################################################################################################################################################################################################################################################
        #################################################################################################################################################################################################################################################################################################################################################
        #################################################################################################################################################################################################################################################################################################################################################


        for name in Histo_Par_B_z:
            if("".join(["Unfold_", str(Method)]) not in str(name)):
                continue
            Q2_xB_Bin_Name = "Q2_xB_Bin_1" if("Q2_xB_Bin_1" in str(name)) else "Q2_xB_Bin_2" if("Q2_xB_Bin_2" in str(name)) else "Q2_xB_Bin_3" if("Q2_xB_Bin_3" in str(name)) else "Q2_xB_Bin_4" if("Q2_xB_Bin_4" in str(name)) else "Q2_xB_Bin_5" if("Q2_xB_Bin_5" in str(name)) else "Q2_xB_Bin_6" if("Q2_xB_Bin_6" in str(name)) else "Q2_xB_Bin_7" if("Q2_xB_Bin_7" in str(name)) else "Q2_xB_Bin_8" if("Q2_xB_Bin_8" in str(name)) else "Q2_xB_Bin_9" if("Q2_xB_Bin_9" in str(name)) else "ERROR"
            canvas_name = "".join(["PT_Pars_", "" if("Smeared" not in str(name)) else "Smeared_", str(Method), "_", str(Q2_xB_Bin_Name)])
            Bin_Range_str = str(name.replace("".join(["_Unfold_", str(Method), "_", "" if("Smeared" not in str(name)) else "Smeared_", str(Q2_xB_Bin_Name)]), ""))
            try:
                Canvas_Parameters_List[canvas_name].GetName()
                root_color_ii += 1
                if(root_color_ii in [5, 10, 19]):
                    root_color_ii += 1
            except:
                Canvas_Parameters_List[canvas_name] = Canvas_Create(Name=canvas_name, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)
                # Canvas_Parameters_List[canvas_name].Draw()
                TMulti_Graph_B_name = "".join([str(canvas_name), "_TMultiGraph_B"])
                TMulti_Graph_C_name = "".join([str(canvas_name), "_TMultiGraph_C"])
                Canvas_Parameters_List[TMulti_Graph_B_name] = ROOT.TMultiGraph(TMulti_Graph_B_name, "".join([str(str(Histo_Par_B_z[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_B_z[name].GetXaxis().GetTitle()), ";", str(Histo_Par_B_z[name].GetYaxis().GetTitle())]))
                Canvas_Parameters_List[TMulti_Graph_C_name] = ROOT.TMultiGraph(TMulti_Graph_C_name, "".join([str(str(Histo_Par_C_z[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_C_z[name].GetXaxis().GetTitle()), ";", str(Histo_Par_C_z[name].GetYaxis().GetTitle())]))
                Par_Legends[TMulti_Graph_B_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
                Par_Legends[TMulti_Graph_B_name].SetNColumns(1)
                Par_Legends[TMulti_Graph_B_name].SetBorderSize(0)
                Par_Legends[TMulti_Graph_B_name].SetFillColor(0)
                Par_Legends[TMulti_Graph_B_name].SetFillStyle(0)

                Par_Legends[TMulti_Graph_C_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
                Par_Legends[TMulti_Graph_C_name].SetNColumns(1)
                Par_Legends[TMulti_Graph_C_name].SetBorderSize(0)
                Par_Legends[TMulti_Graph_C_name].SetFillColor(0)
                Par_Legends[TMulti_Graph_C_name].SetFillStyle(0)

                root_color_ii = 1

            Histo_Par_B_z[name].SetMarkerSize(2)
            Histo_Par_B_z[name].SetMarkerColor(root_color_ii)
            Histo_Par_B_z[name].SetLineColor(root_color_ii)
            Histo_Par_B_z[name].SetLineWidth(1)
            Canvas_Parameters_List[TMulti_Graph_B_name].Add(Histo_Par_B_z[name])
            Par_Legends[TMulti_Graph_B_name].AddEntry(Histo_Par_B_z[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")
            Histo_Par_C_z[name].SetMarkerSize(2)
            Histo_Par_C_z[name].SetMarkerColor(root_color_ii)
            Histo_Par_C_z[name].SetLineColor(root_color_ii)
            Histo_Par_C_z[name].SetLineWidth(1)
            Canvas_Parameters_List[TMulti_Graph_C_name].Add(Histo_Par_C_z[name])
            Par_Legends[TMulti_Graph_C_name].AddEntry(Histo_Par_C_z[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")


        for name in Histo_Par_B_pT:
            if("".join(["Unfold_", str(Method)]) not in str(name)):
                continue
            Q2_xB_Bin_Name = "Q2_xB_Bin_1" if("Q2_xB_Bin_1" in str(name)) else "Q2_xB_Bin_2" if("Q2_xB_Bin_2" in str(name)) else "Q2_xB_Bin_3" if("Q2_xB_Bin_3" in str(name)) else "Q2_xB_Bin_4" if("Q2_xB_Bin_4" in str(name)) else "Q2_xB_Bin_5" if("Q2_xB_Bin_5" in str(name)) else "Q2_xB_Bin_6" if("Q2_xB_Bin_6" in str(name)) else "Q2_xB_Bin_7" if("Q2_xB_Bin_7" in str(name)) else "Q2_xB_Bin_8" if("Q2_xB_Bin_8" in str(name)) else "Q2_xB_Bin_9" if("Q2_xB_Bin_9" in str(name)) else "ERROR"
            canvas_name = "".join(["z_Pars_", str(Method), "_", str(Q2_xB_Bin_Name)])
            Bin_Range_str = str(name.replace("".join(["_Unfold_", str(Method), "_", str(Q2_xB_Bin_Name)]), ""))
            try:
                Canvas_Parameters_List[canvas_name].GetName()
                root_color_ii += 1
                if(root_color_ii in [5, 10, 19]):
                    root_color_ii += 1
            except:
                Canvas_Parameters_List[canvas_name] = Canvas_Create(Name=canvas_name, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=1000, cd_Space=0)
                # Canvas_Parameters_List[canvas_name].Draw()
                TMulti_Graph_B_name = "".join([str(canvas_name), "_TMultiGraph_B"])
                TMulti_Graph_C_name = "".join([str(canvas_name), "_TMultiGraph_C"])
                Canvas_Parameters_List[TMulti_Graph_B_name] = ROOT.TMultiGraph(TMulti_Graph_B_name, "".join([str(str(Histo_Par_B_pT[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_B_pT[name].GetXaxis().GetTitle()), ";", str(Histo_Par_B_pT[name].GetYaxis().GetTitle())]))
                Canvas_Parameters_List[TMulti_Graph_C_name] = ROOT.TMultiGraph(TMulti_Graph_C_name, "".join([str(str(Histo_Par_C_pT[name].GetTitle()).replace(str(Bin_Range_str), "All Bins")).replace(" [GeV]", ""), ";", str(Histo_Par_C_pT[name].GetXaxis().GetTitle()), ";", str(Histo_Par_C_pT[name].GetYaxis().GetTitle())]))
                Par_Legends[TMulti_Graph_B_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
                Par_Legends[TMulti_Graph_B_name].SetNColumns(1)
                Par_Legends[TMulti_Graph_B_name].SetBorderSize(0)
                Par_Legends[TMulti_Graph_B_name].SetFillColor(0)
                Par_Legends[TMulti_Graph_B_name].SetFillStyle(0)

                Par_Legends[TMulti_Graph_C_name] = ROOT.TLegend(0.65, 0.15, 0.95, 0.5)
                Par_Legends[TMulti_Graph_C_name].SetNColumns(1)
                Par_Legends[TMulti_Graph_C_name].SetBorderSize(0)
                Par_Legends[TMulti_Graph_C_name].SetFillColor(0)
                Par_Legends[TMulti_Graph_C_name].SetFillStyle(0)

                root_color_ii = 1

            Histo_Par_B_pT[name].SetMarkerSize(2)
            Histo_Par_B_pT[name].SetMarkerColor(root_color_ii)
            Histo_Par_B_pT[name].SetLineColor(root_color_ii)
            Histo_Par_B_pT[name].SetLineWidth(1)
            Canvas_Parameters_List[TMulti_Graph_B_name].Add(Histo_Par_B_pT[name])
            Par_Legends[TMulti_Graph_B_name].AddEntry(Histo_Par_B_pT[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")
            Histo_Par_C_pT[name].SetMarkerSize(2)
            Histo_Par_C_pT[name].SetMarkerColor(root_color_ii)
            Histo_Par_C_pT[name].SetLineColor(root_color_ii)
            Histo_Par_C_pT[name].SetLineWidth(1)
            Canvas_Parameters_List[TMulti_Graph_C_name].Add(Histo_Par_C_pT[name])
            Par_Legends[TMulti_Graph_C_name].AddEntry(Histo_Par_C_pT[name], "".join(["#color[", str(root_color_ii), "]{", str(Bin_Range_str),"}"]), "lpE")


        for canvas_loop in Canvas_Parameters_List:
            if("_TMultiGraph" not in canvas_loop):
                # Canvas_Parameters_List[canvas_loop].Draw()
                Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=1, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
                Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_B"])].Draw("APL* same")
                Par_Legends[TMulti_Graph_B_name].Draw("same")
                Draw_Canvas(canvas=Canvas_Parameters_List[canvas_loop], cd_num=2, left_add=0.1, right_add=0.1, up_add=0.1, down_add=0.1)
                Canvas_Parameters_List["".join([str(canvas_loop), "_TMultiGraph_C"])].Draw("APL* same")
                Par_Legends[TMulti_Graph_C_name].Draw("same")

    except:
        print("".join([color.BOLD, color.RED, "\nError in getting parameter plots with method: ", color.BLUE, str(Method), color.RED, "\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))        

        
        
print("".join([color.BOLD, color.GREEN, "\n\nDone with getting parameter plots (Now Saving...)\n", color.END]))    
for ii in Canvas_Parameters_List:
    if("TMultiGraph" not in str(ii)):
        Saving_Name_Pars = "".join([str(ii), ".png"])
        # print(Saving_Name_Pars)
#         if(Saving_Q):
#             Canvas_Parameters_List[ii].SaveAs(Saving_Name_Pars)
#         else:
#             Canvas_Parameters_List[ii].Draw()
        count_of_images += 1
        print("".join(["Saved: " if(Saving_Q and False) else "".join([color.RED, "Would be Saving: ", color.END]), color.BOLD, color.BLUE, str(Saving_Name_Pars), color.END]))
    
    
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















if(count != 0):


    print("".join([color.BOLD, color.BLUE, "\n\nStarting Combined Images...\n", color.END]))
    Unfolded_Canvas_Test, Main_Unfolding_Images, Main_Final_Unfolding_Images = {}, {}, {}
    for Q2_xB_Bin in range(0, 9, 1):
        z_pT_Bin_Range = 0 if(Q2_xB_Bin in [0]) else 49 if(Q2_xB_Bin in [1, 2, 3]) else 42 if(Q2_xB_Bin in [4]) else 36 if(Q2_xB_Bin in [5]) else 25 if(Q2_xB_Bin in [6, 7]) else 20 if(Q2_xB_Bin in [8]) else 1

        if(str(Q2_xB_Bin) not in Q2_xB_Bin_List):
            print("Skipping unselected Q2-xB Bin...")
            print("".join(["Bin ", str(Q2_xB_Bin), " is not in Q2_xB_Bin_List = ", str(Q2_xB_Bin_List)]))
            continue
        
        # for DF_Current in [rdf, mdf, gdf]:
        for DF_Current in [rdf]:
            for ii in DF_Current.GetListOfKeys():
                out_print = str(ii.GetName())
                Conditions_For_Histograms = []
                Conditions_For_Histograms.append("Normal_2D" in str(out_print))
                Conditions_For_Histograms.append(("cut_Complete_SIDIS" in str(out_print)) or ("no_cut" in str(out_print) and ("gdf" in str(out_print) or "gen" in str(out_print))))
                Conditions_For_Histograms.append(("Var-D1='Q2'" in str(out_print) and "Var-D2='xB'" in str(out_print)) or ("Var-D1='z'" in str(out_print) and "Var-D2='pT'" in str(out_print)))
                Conditions_For_Histograms.append(("Q2-xB-Bin=All" in str(out_print) and ("Var-D1='Q2'" in str(out_print) and "Var-D2='xB'" in str(out_print))) or (("".join(["Q2-xB-Bin=", str(Q2_xB_Bin)]) in str(out_print)) and ("Var-D1='z" in str(out_print) and "Var-D2='pT" in str(out_print))))
                if(False not in Conditions_For_Histograms):
                    Main_Unfolding_Images[out_print] = DF_Current.Get(out_print)
                    z_pT_Bin = 0
                    if(z_pT_Bin != 0 and ("Var-D1='Q2'" in str(out_print) and "Var-D2='xB'" in str(out_print))):
                        print("Testing Q2-xB bins...")
                        break
                    if("smear" in str(out_print)):
                        print("smeared:")
                        print(out_print)
                    out_print_binned = out_print.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)]))
                    out_print_binned = out_print.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D"]))

                    try:
                        if("3D" in str(type(Main_Unfolding_Images[out_print]))):
                            if(("Response_Matrix" in str(out_print)) and True):
                                bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetZaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetZaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsZ())
                                if(z_pT_Bin != 0):
                                    Main_Unfolding_Images[out_print].GetZaxis().SetRange(bin_2D_0, bin_2D_1)
                                Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('yx')
                                Main_Final_Unfolding_Images[out_print_binned].SetName(str(Main_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])))
                                New_2D_Title = (str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
                                New_2D_Title = str(str(New_2D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
                                Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_2D_Title)

                            elif(("Normal_2D" in str(out_print)) and True):
                                bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetXaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsX())
                                if(z_pT_Bin != 0):
                                    Main_Unfolding_Images[out_print].GetXaxis().SetRange(bin_2D_0, bin_2D_1)
                                if("Var-D1='z'" not in out_print_binned):
                                    Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('yz')
                                else:
                                    Main_Final_Unfolding_Images[out_print_binned] = Main_Unfolding_Images[out_print].Project3D('zy')
                                Main_Final_Unfolding_Images[out_print_binned].SetName(str(Main_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])))
                                New_2D_Title = (str(str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("xy projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
                                New_2D_Title = str(str(New_2D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
                                if("z vs. P_{T}" in New_2D_Title):
                                    New_2D_Title = New_2D_Title.replace("z vs. P_{T}", "P_{T} vs. z")
                                Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_2D_Title)

                            else:
                                bin_2D_0, bin_2D_1 = Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsY())
                                if(z_pT_Bin != 0):
                                    Main_Unfolding_Images[out_print].GetYaxis().SetRange(bin_2D_0, bin_2D_1)
                                New_2D_Title = (str(Main_Unfolding_Images[out_print].GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
                                Main_Unfolding_Images[out_print].SetTitle(New_2D_Title)

                        elif("2D" in str(type(Main_Unfolding_Images[out_print]))):
                            if(("Response_Matrix" in str(out_print)) and True):
                                bin_1D_0, bin_1D_1 = Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else 0), Main_Unfolding_Images[out_print].GetYaxis().FindBin(z_pT_Bin if(z_pT_Bin != 0) else Main_Unfolding_Images[out_print].GetNbinsY())
                                Main_Final_Unfolding_Images[out_print_binned] = Main_Final_Unfolding_Images[out_print].ProjectionX(str(Main_Final_Unfolding_Images[out_print].GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin == 0) else str(z_pT_Bin)])), bin_1D_0, bin_1D_1)
                                New_1D_Title = str(Main_Final_Unfolding_Images[out_print_binned].GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin) if(z_pT_Bin != 0) else "All", "}}}"]))
                                New_1D_Title = str(str(New_1D_Title).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut: ", "")
                                Main_Final_Unfolding_Images[out_print_binned].SetTitle(New_1D_Title)
                    except:
                        print("".join(["Failed...\n", color.RED, color.BOLD, "ERROR before line 2774: \n", color.END, color.RED, str(traceback.format_exc()), color.END]))


        Smearing_final_list = ["", "smear"]
        if(Smearing_Options not in ["no_smear", "both"]):
            Smearing_final_list = ["smear"]
        elif(Smearing_Options in ["no_smear"]):
            Smearing_final_list = [""]
        elif(Smearing_Options in ["both"]):
            Smearing_final_list = ["", "smear"]

            
        Smearing_final_list = ["smear"]
        
        for Smear in Smearing_final_list:
#             # for Histos_Type in ["Data", "Response", "SVD", "Bin", "RooUnfold_bayes", "RooUnfold_svd", "RooUnfold_bbb"]:
            for Histos_Type in ["Data", "Response", "SVD", "Bin", "RooUnfold_bayes", "RooUnfold_svd"]:
#             for Histos_Type in ["Data", "Response", "Bin", "RooUnfold_bayes", "RooUnfold_svd"]:
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ####  Canvas (Main) Creation  ####################################################################################################################################################################################################################################################################################################################################################################################


                    # Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)])] = Canvas_Create(Name="".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)]), Num_Columns=2, Num_Rows=1, Size_X=3999, Size_Y=2250, cd_Space=0.01)
                    Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])] = Canvas_Create(Name="".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])]), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
                    Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].SetFillColor(root_color.LGrey)
                    # Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type)])].Draw()

                    Unfolded_Canvas_Test_cd_1 = Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].cd(1)
                    Unfolded_Canvas_Test_cd_1.SetFillColor(root_color.LGrey)
                    Unfolded_Canvas_Test_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
                    Unfolded_Canvas_Test_cd_1.Divide(1, 2, 0, 0)

                    Unfolded_Canvas_Test_cd_1_Upper = Unfolded_Canvas_Test_cd_1.cd(1)
                    Unfolded_Canvas_Test_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
                    Unfolded_Canvas_Test_cd_1_Upper.Divide(1, 2, 0, 0)

                    Unfolded_Canvas_Test_cd_1_Lower = Unfolded_Canvas_Test_cd_1.cd(2)
                    Unfolded_Canvas_Test_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
                    Unfolded_Canvas_Test_cd_1_Lower.Divide(1, 1, 0, 0)
                    Unfolded_Canvas_Test_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)



                    Unfolded_Canvas_Test_cd_2 = Unfolded_Canvas_Test["".join(["Unfolded_Canvas_All_", str(Q2_xB_Bin), "_", str(Histos_Type), "".join(["" if(Smear != "smear") else "_", str(Smear)])])].cd(2)
                    Unfolded_Canvas_Test_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
                    Unfolded_Canvas_Test_cd_2.SetFillColor(root_color.LGrey)
                    number_of_rows, number_of_cols = z_pT_Border_Lines(Q2_xB_Bin)[0][1]-1, z_pT_Border_Lines(Q2_xB_Bin)[1][1]-1

                    # Unfolded_Canvas_Test_cd_2.Divide(1, number_of_rows, 0.0001, 0.0001)
                    Unfolded_Canvas_Test_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)

                    # for ii in range(1, number_of_rows + 1, 1):
                    for ii in range(1, number_of_cols + 1, 1):
                        Unfolded_Canvas_Test_cd_2_cols = Unfolded_Canvas_Test_cd_2.cd(ii)
                        # Unfolded_Canvas_Test_cd_2_cols.Divide(number_of_cols, 1, 0.0001, 0.0001)
                        Unfolded_Canvas_Test_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)


                ####  Canvas (Main) Creation End #################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################



                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ####  Filling Canvas (Left)  #####################################################################################################################################################################################################################################################################################################################################################################################


                    ##############################################################################################################################################################################################################################################################################################################################################################################################################
                    ####  Upper Left  ############################################################################################################################################################################################################################################################################################################################################################################################
                    cd_test = 1
                    for ii in Main_Final_Unfolding_Images:
                        # if(cd_test > 2 or ("Q2-xB-Bin=All" not in str(ii) and "".join(["Q2-xB-Bin=", str(Q2_xB_Bin) if(Q2_xB_Bin not in [0, "0"]) else "All"]) not in str(ii)) or (("Var-D1='z'" in str(ii)) and ("Var-D2='pT'" in str(ii)) and cd_test != 2) or (("Var-D1='z'" not in str(ii)) and ("Var-D2='pT'" not in str(ii)) and cd_test != 1)):
                        #     continue

                        
                        if(str(ii) == "((Histo-Group='Normal_2D'), (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=''), (Binning-Type='2'-[Q2-xB-Bin=All, z-PT-Bin=All_1D]), (Var-D1='Q2'-[NumBins=100, MinBin=1.48, MaxBin=11.87]), (Var-D2='xB'-[NumBins=100, MinBin=0.09, MaxBin=0.826]))"):
                            cd_test = 1
                        else:
                            cd_test += 1
                            # print(ii)
                            # if(cd_test > 2):
                            #     print(cd_test)
                            #     break

                            

                        Draw_Canvas(Unfolded_Canvas_Test_cd_1_Upper, cd_test, 0.15)
                        # Unfolded_Canvas_Test_cd_1_Upper.cd(cd_test)
                        Main_Final_Unfolding_Images[ii].Draw("colz")

                        Unfolded_Canvas_Test_cd_1_Upper.Modified()
                        Unfolded_Canvas_Test_cd_1_Upper.Update()

                        palette_move(canvas=Unfolded_Canvas_Test_cd_1_Upper, histo=Main_Final_Unfolding_Images[ii], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)

                        if("Var-D1='Q2'" in str(ii) and "Var-D2='xB'" in str(ii)):
                            Main_Final_Unfolding_Images[ii].SetTitle((Main_Final_Unfolding_Images[ii].GetTitle()).replace("Q^{2}-x_{B} Bin: All", "".join(["#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All", "}"])))
                            # print("".join([color.BLUE, "Q2-xB plots:", color.END]))
                            # print(Main_Final_Unfolding_Images[ii].GetTitle())
                            # print(ii)
                            # print("\n\n")
                            Q2_xB_borders = {}
                            line_num = 0
                            for b_lines in Q2_xB_Border_Lines(-1):
                                Q2_xB_borders[line_num] = ROOT.TLine()
                                Q2_xB_borders[line_num].SetLineColor(1)    
                                Q2_xB_borders[line_num].SetLineWidth(5)
                                Q2_xB_borders[line_num].DrawLine(b_lines[0][0], b_lines[0][1], b_lines[1][0], b_lines[1][1])
                                line_num += 1
                            if(Q2_xB_Bin != 0):
                                ##=====================================================##
                                ##==========##     Selecting Q2-xB Bin     ##==========##
                                ##=====================================================##
                                line_num_2 = 0
                                for b_lines_2 in Q2_xB_Border_Lines(Q2_xB_Bin):
                                    Q2_xB_borders[line_num_2] = ROOT.TLine()
                                    Q2_xB_borders[line_num_2].SetLineColor(2)
                                    Q2_xB_borders[line_num_2].SetLineWidth(10)
                                    Q2_xB_borders[line_num_2].DrawLine(b_lines_2[0][0], b_lines_2[0][1], b_lines_2[1][0], b_lines_2[1][1])
                                    line_num_2 += + 1
                                ##=====================================================##
                                ##==========##     Selecting Q2-xB Bin     ##==========##
                                ##=====================================================##


                        if((Q2_xB_Bin != 0) and ("Var-D1='z'" in str(ii)) and ("Var-D2='pT'" in str(ii))):
                            # print("".join([color.GREEN, "z-pT plots:", color.END]))
                            # print(Main_Final_Unfolding_Images[ii].GetTitle())
                            # print(ii)
                            # print((("".join(["Q2-xB-Bin=", str(Q2_xB_Bin)]) in str(ii)) and ("Var-D1='z'" in str(ii) and "Var-D2='pT'" in str(ii))))
                            # print("\n\n")
                            z_pT_borders = {}
                            Max_z  = max(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
                            Min_z  = min(z_pT_Border_Lines(Q2_xB_Bin)[0][2])
                            Max_pT = max(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
                            Min_pT = min(z_pT_Border_Lines(Q2_xB_Bin)[1][2])
                            for zline in z_pT_Border_Lines(Q2_xB_Bin)[0][2]:
                                for pTline in z_pT_Border_Lines(Q2_xB_Bin)[1][2]:
                                    z_pT_borders[zline] = ROOT.TLine()
                                    z_pT_borders[zline].SetLineColor(1)
                                    z_pT_borders[zline].SetLineWidth(4)
                                    z_pT_borders[zline].DrawLine(zline, Max_pT, zline, Min_pT) # z_pT_borders[zline].DrawLine(Max_pT, zline, Min_pT, zline)
                                    z_pT_borders[pTline] = ROOT.TLine()
                                    z_pT_borders[pTline].SetLineColor(1)
                                    z_pT_borders[pTline].SetLineWidth(4)
                                    z_pT_borders[pTline].DrawLine(Max_z, pTline, Min_z, pTline) # z_pT_borders[pTline].DrawLine(pTline, Max_z, pTline, Min_z)

                        # cd_test += 1
                    ####  Upper Left  ############################################################################################################################################################################################################################################################################################################################################################################################
                    ##############################################################################################################################################################################################################################################################################################################################################################################################################

                    ##############################################################################################################################################################################################################################################################################################################################################################################################################
                    ####  Lower Left  ############################################################################################################################################################################################################################################################################################################################################################################################

                    Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)

                    if("Data" in Histos_Type):
                        try:
                            # Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)
                            Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0"])].DrawClone("same")
                            Save_Response_Matrix["".join(["MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0", "_Smeared" if("smear" in str(Smear)) else ""])].DrawClone("same")
                            Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0"])].DrawClone("same")
                        except Exception as e:
                            print("".join([color.BOLD, color.RED, "ERROR IN 1D Histograms:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            # print("".join([color.RED, color.BOLD, "ERROR IN 1D Histograms (line 2714): ", color.END, color.RED, str(e), color.END]))


                    if("Response" in Histos_Type):
                        try:
                            Save_Response_Matrix["".join(["Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:0", "_Smeared" if("smear" in str(Smear)) else ""])].Draw("col")
                        except Exception as e:
                            print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            # print("".join([color.RED, color.BOLD, "ERROR IN Response Matrix (line 2722): ", color.END, color.RED, str(e), color.END]))


                    if("SVD" in Histos_Type):
                        try:
                            Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                        except Exception as e:
                            try:
                                Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN SVD Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            # print("".join([color.RED, color.BOLD, "ERROR IN SVD Method Histogram (line 2730): ", color.END, color.RED, str(e), color.END]))

                    if("Bin" in Histos_Type):
                        try:
                            Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                        except Exception as e:
                            try:
                                Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN Bin-by-bin Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                            # print("".join([color.RED, color.BOLD, "ERROR IN Bin-by-bin Method Histogram (line 2737): ", color.END, color.RED, str(e), color.END]))


                    if("RooUnfold_bayes" in Histos_Type):
                        try:
                            RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
                        except Exception as e:
                            try:
                                RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bayesian) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                    if("RooUnfold_svd" in Histos_Type):
                        try:
                            RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
                        except Exception as e:
                            try:
                                RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (SVD) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                    if("RooUnfold_bbb" in Histos_Type):
                        try:
                            RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
                        except Exception as e:
                            try:
                                RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=All_1D]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bin-by-Bin) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))


                    ####  Lower Left  ############################################################################################################################################################################################################################################################################################################################################################################################
                    ##############################################################################################################################################################################################################################################################################################################################################################################################################


                ####  Filling Canvas (Left) End ##################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################



                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ####  Filling Canvas (Right)  ####################################################################################################################################################################################################################################################################################################################################################################################

                    for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):

                        cd_row = int(z_pT_Bin/number_of_cols) + 1
                        if(0 == (z_pT_Bin%number_of_cols)):
                            cd_row += -1

                        cd_col = z_pT_Bin - ((cd_row - 1)*number_of_cols)

                        # Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row = Unfolded_Canvas_Test_cd_2.cd(cd_row)
                        # Unfolded_Canvas_Test_cd_2_z_pT_Bin     = Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row.cd(cd_col)
                        Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row = Unfolded_Canvas_Test_cd_2.cd((number_of_cols - cd_col) + 1)
                        Unfolded_Canvas_Test_cd_2_z_pT_Bin     = Unfolded_Canvas_Test_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)

                        Unfolded_Canvas_Test_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                        Unfolded_Canvas_Test_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                        Draw_Canvas(Unfolded_Canvas_Test_cd_2_z_pT_Bin, 1, 0.15)

                        try:
                            if("Data" in Histos_Type):
                                try:
                                    # Draw_Canvas(Unfolded_Canvas_Test_cd_1_Lower, 1, 0.15)
                                    Save_Response_Matrix["".join(["ExREAL_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin)])].Draw("same")
                                    Save_Response_Matrix["".join(["MC_REC_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin), "_Smeared" if("smear" in str(Smear)) else ""])].Draw("same")
                                    Save_Response_Matrix["".join(["MC_GEN_1D Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin)])].Draw("same")
                                except Exception as e:
                                    print("".join([color.BOLD, color.RED, "ERROR IN 1D (Data) Histograms:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                            if("Response" in Histos_Type):
                                try:
                                    Save_Response_Matrix["".join(["Q2-xB Bin:", str(Q2_xB_Bin), " z-pT Bin:", str(z_pT_Bin), "_Smeared" if("smear" in str(Smear)) else ""])].Draw("col")
                                except Exception as e:
                                    print("".join([color.BOLD, color.RED, "ERROR IN Response Matrix:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                            if("SVD" in Histos_Type):
                                try:
                                    Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                                except Exception as e:
                                    # try:
                                    #     Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))extra"])].Draw("same")
                                    # except:
                                    #     try:
                                    #         Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))extra"])].Draw("same")
                                    #     except:
                                    #         try:
                                    #             Unfolding_Histogram_1_Norm_Clone["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                                    #         except:
                                    print("".join([color.BOLD, color.RED, "ERROR IN SVD Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                            if("Bin" in Histos_Type):
                                try:
                                    Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                                except Exception as e:
                                    # try:
                                    #     Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))extra"])].Draw("same")
                                    # except:
                                    #     try:
                                    #         Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))extra"])].Draw("same")
                                    #     except:
                                    #         try:
                                    #             Bin_Unfolded["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))extra"])].Draw("same")
                                    #         except:
                                    print("".join([color.BOLD, color.RED, "ERROR IN Bin-by-bin Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                            if("RooUnfold_bayes" in Histos_Type):
                                try:
                                    RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
                                except Exception as e:
                                    # try:
                                    #     RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_bayes_Norm_extra"])].Draw("same")
                                    # except:
                                    #     try:
                                    #         RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_bayes_Norm_extra"])].Draw("same")
                                    #     except:
                                    #         try:
                                    #             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bayes_Norm_extra"])].Draw("same")
                                    #         except:
                                    print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bayesian) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

                            if("RooUnfold_svd" in Histos_Type):
                                try:
                                    RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
                                except Exception as e:
                                    # try:
                                    #     RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_svd_Norm_extra"])].Draw("same")
                                    # except:
                                    #     try:
                                    #         RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_svd_Norm_extra"])].Draw("same")
                                    #     except:
                                    #         try:
                                    #             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_svd_Norm_extra"])].Draw("same")
                                    #         except:
                                    print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (SVD) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                                    for ii in RooUnfolded_Histos:
                                        # if(("".join(["(Smear-Type=", "''" if(Smear != "smear") else "'smear'", ")"]) in str(ii)) and ("".join(["Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin)]) in str(ii)) and ("_svd_Norm_extra" in str(ii))):
                                        if(("".join(["Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin)]) in str(ii)) and ("_svd_Norm_extra" in str(ii))):
                                            print("".join(["RooUnfolded_Histos: ", str(ii)]))

                            if("RooUnfold_bbb" in Histos_Type):
                                try:
                                    RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
                                except Exception as e:
                                    # try:
                                    #     RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_bbb_Norm_extra"])].Draw("same")
                                    # except:
                                    #     try:
                                    #         RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=55, MinBin=-3.5, MaxBin=51.5]))_bbb_Norm_extra"])].Draw("same")
                                    #     except:
                                    #         try:
                                    #             RooUnfolded_Histos["".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='DataFrame_Type'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type=", "''" if(Smear != "smear") else "'smear'", "), (Binning-Type='2'-[Q2-xB-Bin=", str(Q2_xB_Bin), ", z-PT-Bin=", str(z_pT_Bin), "]), (Var-D1='phi_t", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin_2", "'" if(Smear != "smear") else "_smeared'" , "-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))_bbb_Norm_extra"])].Draw("same")
                                    #         except:
                                    print("".join([color.BOLD, color.RED, "ERROR IN RooUnfold (Bin-by-Bin) Method Histogram:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))


                        except:
                            print("".join(["Failed on ", str(z_pT_Bin)]))
                            print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc()), "\n================================================================================================================================================================================================\n\n"]))
                            # continue
                            # break

                ####  Filling Canvas (Right) End #################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################
                ##################################################################################################################################################################################################################################################################################################################################################################################################################



    print("".join([color.BOLD, color.GREEN, "\nDone Combining Unfolded Histograms into one image per bin (Now saving...)\n", color.END]))
    for Canvas_name in Unfolded_Canvas_Test:
        if("cd_upper" not in str(Canvas_name) and "cd_lower" not in str(Canvas_name)):
            Save_Name = "".join([str(Canvas_name).replace("Unfolded_Canvas_All_", "Unfolded_Histos_Q2_xB_Bin_"), str(File_Save_Format)])
            if(Saving_Q):
                Unfolded_Canvas_Test[Canvas_name].SaveAs(Save_Name)
            count_of_images += 1
            print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BOLD, color.BLUE, str(Save_Name), color.END]))
            
    if(Saving_Q):
        print("".join([color.BOLD, color.GREEN, "\nDONE SAVING\n", color.END, color.BOLD, color.BLUE, "Starting final folder creation/image sorting...", color.END]))
    else:
        print("".join([color.BOLD, color.RED, "\nNOT SAVING", color.END]))




    # #############################################################################
    # #############################################################################
    # ##====================##                             ##====================##
    # ##====================##     Final Image Sorting     ##====================##
    # ##====================##                             ##====================##
    # #############################################################################
    # #############################################################################
    # if(Saving_Q):
    #     if(not (Common_Name == REAL_File_Name == MC_REC_File_Name == MC_GEN_File_Name)):
    #         print("".join([color.BOLD, color.RED, "WARNING: A commom file name was NOT used between each of the different data sets.\n", color.END]))
    #     Date_of_Save = "".join([str(datetime_object_full.month), "_", str(startDay_full), "_", str(datetime_object_full.year)])
    #     ##========================================##
    #     ##=====##   Main Folder Creation   ##=====##
    #     destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
    #     version = 1
    #     while(str(destination).replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/", "") in os.listdir()):
    #         destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_V", str(version), "_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
    #         version += 1
    #         if(version > 10):
    #             print("".join([color.BOLD, color.RED, "\nWARNING: Many folders are being saved from the same date. This loop is automatically closed after 10 versions for the same folder.\n\n\tPlease overide this decision manually if this many folders are desired...\n\n", color.END]))
    #             fail
    #     os.mkdir(destination)
    #     ##=====##   Main Folder Creation   ##=====##
    #     ##========================================##
    #     ##============================================##
    #     ##=====##   Category Folder Creation   ##=====##
    #     destination_main = "".join([str(destination), "/Unfolding_Images"])
    #     os.mkdir(destination_main)
    #     ##=====##   Category Folder Creation   ##=====##
    #     ##============================================##
    #     ##===================================================##
    #     ##=====##   z-pT Unfolding Folders Creation   ##=====##
    #     destination_z_pT_Bin_All = "".join([str(destination_main), "/z_pT_Bin_All"])
    #     destination_z_pT_Bin_Individual = "".join([str(destination_main), "/z_pT_Bin_Individual"])
    #     os.mkdir(destination_z_pT_Bin_All)
    #     os.mkdir(destination_z_pT_Bin_Individual)
    #     ##=====##   z-pT Unfolding Folders Creation   ##=====##
    #     ##===================================================##
    #     ##=============================================================##
    #     ##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
    #     destination_Smeared = "".join([str(destination_main), "/Smeared"])
    #     destination_Smeared_z_pT_Bin_All = "".join([str(destination_main), "/Smeared/z_pT_Bin_All"])
    #     destination_Smeared_z_pT_Bin_Individual = "".join([str(destination_main), "/Smeared/z_pT_Bin_Individual"])
    #     os.mkdir(destination_Smeared)
    #     os.mkdir(destination_Smeared_z_pT_Bin_All)
    #     os.mkdir(destination_Smeared_z_pT_Bin_Individual)
    #     ##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
    #     ##=============================================================##
    #     ##====================================================##
    #     ##=====##   Q2-xB Unfolding Folders Creation   ##=====##
    #     for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual]:
    #         for Q2_xB_Bin in range(1, 9, 1):
    #             # print("".join([str(folder), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #             os.mkdir("".join([str(folder), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #     ##=====##   Q2-xB Unfolding Folders Creation   ##=====##
    #     ##====================================================##
    #     ##=================================##
    #     ##=====##   Image Sorting   ##=====##
    #     for Entry in os.listdir():
    #         if(str(File_Save_Format) in str(Entry)):
    #             # print("\n"+str(Entry))
    #             if("Response_Matrix_" in str(Entry) and "_z_pT_Bin_" in str(Entry)):
    #                 for Q2_xB_Bin in range(1, 9, 1):
    #                     if("".join(["Q2_xB_Bin_", str(Q2_xB_Bin)]) in str(Entry)):
    #                         if("Smeared" not in str(Entry)):
    #                             # print("".join([str(destination_z_pT_Bin_Individual), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                             shutil.move(Entry, "".join([str(destination_z_pT_Bin_Individual), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                         else:
    #                             # print("".join([str(destination_Smeared_z_pT_Bin_Individual), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                             shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_Individual), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #             elif("Unfolded_Histos" in str(Entry) and "_z_pT_Bin_" not in str(Entry)):
    #                 for Q2_xB_Bin in range(1, 9, 1):
    #                     if("".join(["Q2_xB_Bin_", str(Q2_xB_Bin)]) in str(Entry)):
    #                         if("Smeared" not in str(Entry)):
    #                             # print("".join([str(destination_z_pT_Bin_All), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                             shutil.move(Entry, "".join([str(destination_z_pT_Bin_All), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                         else:
    #                             # print("".join([str(destination_Smeared_z_pT_Bin_All), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #                             shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_All), "/Q2_xB_Bin_", str(Q2_xB_Bin)]))
    #             else:
    #                 # print(destination)
    #                 shutil.move(Entry, destination)
    #     ##=====##   Image Sorting   ##=====##
    #     ##=================================##
    #     #############################################################################
    #     #############################################################################
    #     ##====================##                             ##====================##
    #     ##====================##     Final Image Sorting     ##====================##
    #     ##====================##                             ##====================##
    #     #############################################################################
    #     #############################################################################
    # else:
    #     print("".join([color.BOLD, color.RED, "NOT SORT/SAVING\n", color.END]))
        

else:
    print("".join([color.RED, color.BOLD, "\n\nMAJOR ERROR: No histograms were made...\n\n", color.END]))
    

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
    print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", str(timeMin_end), " a.m."]))
if(datetime_object_end.hour == 12):
    print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", str(timeMin_end), " p.m."]))
if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
    print("".join(["The time that this code finished is 12:", str(timeMin_end), " a.m."]))

print("".join(["Saved ", str(count_of_images), " Images..."]))

Num_of_Days, Num_of_Hrs, Num_of_Mins = 0, 0, 0

if(startDay_full > endDay_full):
    Num_of_Days = endDay_full + (30 - startDay_full)
else:
    Num_of_Days = endDay_full - startDay_full
if(startHr_full > endHr_full):
    Num_of_Hrs = endHr_full + (24 - startHr_full)
else:
    Num_of_Hrs = endHr_full - startHr_full
if(startMin_full > endMin_full):
    Num_of_Mins = endMin_full + (60 - startMin_full)
else:
    Num_of_Mins = endMin_full - startMin_full
if(Num_of_Hrs > 0 and startMin_full >= endMin_full):
    Num_of_Hrs += -1
if(Num_of_Days > 0 and startHr_full >= endHr_full):
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

