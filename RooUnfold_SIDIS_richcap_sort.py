#!/usr/bin/env python

import sys
method = "bayes"
if(len(sys.argv) > 1):
    method = sys.argv[1]

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


# getting current date
datetime_object_full = datetime.now()
# print(datetime_object)

startMin_full = datetime_object_full.minute
startHr_full = datetime_object_full.hour

if(datetime_object_full.minute <10):
    timeMin_full = "".join(["0", str(datetime_object_full.minute)])
else:
    timeMin_full = str(datetime_object_full.minute)

    
Date_Day = "".join(["\nStarted running on ", color.BOLD, str(datetime_object_full.month), "-", str(datetime_object_full.day), "-", str(datetime_object_full.year), color.END, " at "])
# printing current time
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

    
for ii in sys.modules:
    if(str(ii) in ["ROOT", "RooUnfold"]):
        # print(ii)
        print(sys.modules[ii])
        
        
        
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




    
########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loading Data Files     ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################



def FileLocation(FileName, Datatype):
    # location = "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/"
    location = "Histo_Files_ROOT/"

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
Common_Name = "Analysis_Note_Update_V6_All"
Common_Name = "Multi_Dimension_Unfold_V3_All"
Common_Name = "Multi_Dimension_Unfold_V3_Simulated_Test_All"

Common_Name = "New_Binning_Schemes_V5_All"
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
    MC_REC_File_Name = "Unfolding_Tests_V11_All"
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










# ###############################################################################################################################################################
# ##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
# ###############################################################################################################################################################
# try:
#     rdf = ROOT.TFile(str(FileLocation(str(REAL_File_Name), "rdf")), "READ")
#     print("".join(["The total number of histograms available for the", color.BLUE , " Real (Experimental) Data", color.END, " in      '", color.BOLD, REAL_File_Name, color.END, "' is ", color.BOLD, str(len(rdf.GetListOfKeys())), color.END]))
# except:
#     print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
# try:
#     mdf = ROOT.TFile(str(FileLocation(str(MC_REC_File_Name), "mdf")), "READ")
#     print("".join(["The total number of histograms available for the", color.RED , " Reconstructed Monte Carlo Data", color.END, " in '", color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetListOfKeys())), color.END]))
# except:
#     print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
# try:
#     gdf = ROOT.TFile(str(FileLocation(str(MC_GEN_File_Name), "gdf")), "READ")
#     print("".join(["The total number of histograms available for the", color.GREEN , " Generated Monte Carlo Data", color.END, " in   '", color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetListOfKeys())), color.END]))
# except:
#     print("".join([color.RED, color.BOLD, "\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
# ###############################################################################################################################################################
# ##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
# ###############################################################################################################################################################
# print("".join(["\n\n", color.BOLD, "Done Loading RDataFrame files...\n", color.END]))


########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loaded Data Files      ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################















print("".join([color.BOLD, color.BOLD, color.BLUE, "Starting final folder creation/image sorting...", color.END]))



Binning_Option = "Q2_xB_Bin"
Binning_Option = "Q2_y_Bin"


#############################################################################
#############################################################################
##====================##                             ##====================##
##====================##     Final Image Sorting     ##====================##
##====================##                             ##====================##
#############################################################################
#############################################################################

if(not (Common_Name == REAL_File_Name == MC_REC_File_Name == MC_GEN_File_Name)):
    print("".join([color.BOLD, color.RED, "WARNING: A commom file name was NOT used between each of the different data sets.\n", color.END]))
Date_of_Save = "".join([str(datetime_object_full.month), "_", str(datetime_object_full.day), "_", str(datetime_object_full.year)])


##========================================##
##=====##   Main Folder Creation   ##=====##
destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
version = 1
while(str(destination).replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/", "") in os.listdir()):
    destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_V", str(version), "_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
    version += 1
    if(version > 10):
        print("".join([color.BOLD, color.RED, "\nWARNING: Many folders are being saved from the same date. This loop is automatically closed after 10 versions for the same folder.\n\n\tPlease overide this decision manually if this many folders are desired...\n\n", color.END]))
        fail

os.mkdir(destination)
##=====##   Main Folder Creation   ##=====##
##========================================##

##============================================##
##=====##   Category Folder Creation   ##=====##
destination_main = "".join([str(destination), "/Unfolding_Images"])
destination_pars = "".join([str(destination), "/Parameter_Images"])
destination_mult = "".join([str(destination), "/Multi_Dim_Histo_Combined"])
os.mkdir(destination_main)
os.mkdir(destination_pars)
os.mkdir(destination_mult)
##=====##   Category Folder Creation   ##=====##
##============================================##


##===================================================##
##=====##   z-pT Unfolding Folders Creation   ##=====##
destination_z_pT_Bin_All        = "".join([str(destination_main), "/z_pT_Bin_All"])
destination_z_pT_Bin_Individual = "".join([str(destination_main), "/z_pT_Bin_Individual"])
os.mkdir(destination_z_pT_Bin_All)
os.mkdir(destination_z_pT_Bin_Individual)
##=====##   z-pT Unfolding Folders Creation   ##=====##
##===================================================##


##=============================================================##
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
destination_Smeared                     = "".join([str(destination_main), "/Smeared"])
destination_Smeared_z_pT_Bin_All        = "".join([str(destination_main), "/Smeared/z_pT_Bin_All"])
destination_Smeared_z_pT_Bin_Individual = "".join([str(destination_main), "/Smeared/z_pT_Bin_Individual"])
os.mkdir(destination_Smeared)
os.mkdir(destination_Smeared_z_pT_Bin_All)
os.mkdir(destination_Smeared_z_pT_Bin_Individual)
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
##=============================================================##


##====================================================##
##=====##   Q2-xB Unfolding Folders Creation   ##=====##
for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual]:
    for Q2_xB_Bin in range(0, 9 if("xB" in Binning_Option) else 14, 1):
        os.mkdir("".join([str(folder), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
##=====##   Q2-xB Unfolding Folders Creation   ##=====##
##====================================================##


##=================================##
##=====##   Image Sorting   ##=====##
for Entry in os.listdir():
    if("Sim_Test_" in str(Entry)):
        os.rename(Entry, str(Entry).replace("Sim_Test_", ""))
        Entry = str(Entry).replace("Sim_Test_", "")
    if('.png' in str(Entry)):
        # print("\n"+str(Entry))
        if("_Pars_" in str(Entry)):
            shutil.move(Entry, destination_pars)
        elif("Multi_Dim_Histo_" in str(Entry)):
            shutil.move(Entry, destination_mult)
        elif("Response_Matrix_" in str(Entry) and "_z_pT_Bin_" in str(Entry)):
            for Q2_xB_Bin in range(0, 9 if("xB" in Binning_Option) else 14, 1):
                if("".join([str(Binning_Option), "_", str(Q2_xB_Bin)]) in str(Entry)):
                    if(("Smear" not in str(Entry)) and ("smear" not in str(Entry))):
                        shutil.move(Entry, "".join([str(destination_z_pT_Bin_Individual),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                    else:
                        shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_Individual), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))

        elif("Unfolded_Histos" in str(Entry) and "_z_pT_Bin_" not in str(Entry)):
            for Q2_xB_Bin in range(0, 9 if("xB" in Binning_Option) else 14, 1):
                if("".join([str(Binning_Option), "_", str(Q2_xB_Bin)]) in str(Entry)):
                    if(("Smear" not in str(Entry)) and ("smear" not in str(Entry))):
                        shutil.move(Entry, "".join([str(destination_z_pT_Bin_All),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                    else:
                        shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_All), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
        else:
            # print(destination)
            shutil.move(Entry, destination)
            
##=====##   Image Sorting   ##=====##
##=================================##


#############################################################################
#############################################################################
##====================##                             ##====================##
##====================##     Final Image Sorting     ##====================##
##====================##                             ##====================##
#############################################################################
#############################################################################
    

print("".join([color.BOLD, color.GREEN, color_bg.YELLOW, """
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
""", color.END]))

