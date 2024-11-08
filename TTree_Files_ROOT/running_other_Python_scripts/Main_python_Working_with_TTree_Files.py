#!/usr/bin/env python3
import ROOT, numpy
import traceback
import sys
# from sys import argv
# import argparse

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from Pion_Test_Fiducial_Cuts_Defs     import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir

import math
import array
import copy

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)

print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis\n{color.END}")

from datetime import datetime
# Function to format time in 12-hour format with a.m./p.m.
def format_time(dt):
    return dt.strftime("%I:%M %p").lstrip('0')  # Remove leading zero for hour
# Start Time
start_time = datetime.now()
print(f"\nStarted running on {color.BOLD}{color.UNDERLINE}{start_time.strftime('%m-%d-%Y')} at {format_time(start_time)}{color.END}")


# Turns off the canvases when running in the command line
ROOT.gROOT.SetBatch(1)


# Load ROOT Files:
def FileLocation(FileName, Datatype):
    location = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/TTree_Files_ROOT/"
    # location = "TTree_Files_ROOT/"
    if(str(Datatype) == 'rdf'):
        file = "".join(["REAL_Data/DataFrame_SIDIS_epip_Data_REC_",         str(FileName), ".root"])
    if(str(Datatype) == 'mdf'):
        file = "".join(["Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_", str(FileName), ".root"])
    if(str(Datatype) == 'gdf'):
        file = "".join(["GEN_MC/DataFrame_SIDIS_epip_MC_GEN_",              str(FileName), ".root"])
    loading  = "".join([location, file])
    return loading

def FileLocation_Load(FileName, Datatype):
    df = ROOT.RDataFrame("h22", str(FileLocation(str(FileName), str(Datatype))))
    return df

################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################

# Smearing_Options = "no_smear"

Common_Name = "Pass_2_New_TTree_V1_*"


# # Cut_Configuration_Name = "_FC_11" # After Valerii's Cuts - Before my Cuts
# # Cut_Configuration_Name = "_FC_12" # After Valerii's Cuts and my new electron DC refinements - Before my π+ DC Cuts
# Cut_Configuration_Name = ""
# # Cut_Configuration_Name = "_FC7" # Before Valerii's Cuts
# Common_Name = f"Pass_2_New_Fiducial_Cut_Test{Cut_Configuration_Name}_V9_All"

Standard_Histogram_Title_Addition = ""

Pass_Version = "Pass 2" if("Pass_2" in Common_Name) else "Pass 1"
if(Pass_Version not in [""]):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"{Pass_Version} - {Standard_Histogram_Title_Addition}"
    else:
        Standard_Histogram_Title_Addition = Pass_Version


print(f"{color.BBLUE}\nRunning with {Pass_Version} files\n\n{color.END}")
        
        
# Use unique file(s) for one of datatypes? (If so, set the following if(...) conditions to 'False')

##################################
##   Real (Experimental) Data   ##
##################################
if(True):
#     print("".join([color.BOLD, "\nNot using the common file name for the Real (Experimental) Data...\n", color.END]))
# if(False):
    REAL_File_Name = Common_Name
else:
    REAL_File_Name = "Pass_2_5D_Unfold_Test_V7_All" if(Pass_Version in ["Pass 2"]) else "5D_Unfold_Test_V7_All"
    REAL_File_Name = "Pass_2_New_TTree_V1_5164"
    # REAL_File_Name = "Pass_2_New_TTree_V1_516*"
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
    # MC_REC_File_Name = f"Unsmeared_{Common_Name}" if(Smearing_Options in ["no_smear"]) else Common_Name
    # if(Pass_Version not in ["Pass 2"]):
    #     MC_REC_File_Name = MC_REC_File_Name.replace("Pass_2_", "")
    MC_REC_File_Name = "Pass_2_New_TTree_V1_7901_4"
    # MC_REC_File_Name = "Pass_2_New_TTree_V1_7901_*"
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
    MC_GEN_File_Name = "Gen_Cuts_V2_Fixed_All"
    MC_GEN_File_Name = "Pass_2_New_Sector_Cut_Test_V9_All"
####################################
##   Generated Monte Carlo Data   ##
####################################


################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################





################################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
try:
    rdf = FileLocation_Load(str(REAL_File_Name), "rdf")
    print("".join(["The (current) total number of columns available for the", color.BLUE,  " Real (Experimental) Data",       color.END, " in       '", color.BOLD, REAL_File_Name,   color.END, "' is ", color.BOLD, str(len(rdf.GetColumnNames())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'rdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    mdf = FileLocation_Load(str(MC_REC_File_Name), "mdf")
    print("".join(["The (current) total number of columns available for the", color.RED,   " Reconstructed Monte Carlo Data", color.END, " in '",       color.BOLD, MC_REC_File_Name, color.END, "' is ", color.BOLD, str(len(mdf.GetColumnNames())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'mdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
try:
    gdf = FileLocation_Load(str(MC_GEN_File_Name), "gdf")
    print("".join(["The (current) total number of columns available for the", color.GREEN, " Generated Monte Carlo Data",     color.END, " in     '",   color.BOLD, MC_GEN_File_Name, color.END, "' is ", color.BOLD, str(len(gdf.GetColumnNames())), color.END]))
except:
    print("".join([color.Error, "\nERROR IN GETTING THE 'gdf' DATAFRAME...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
################################################################################################################################################################
##==========##==========##     Loading Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################


print(f"{color.BOLD}\nPass Version in use is:{color.END_b} {Pass_Version}{color.END_B}\n\n\nDone Loading TTree files...\n\n{color.END}")


ROOT.gStyle.SetTitleOffset(1.5,'y')
ROOT.gStyle.SetTitleOffset(1.2,'x')
def Ratio_of_2D_Histos(out_hist, rdf_hist, mdf_hist):
    for x_bin in range(0,      out_hist.GetNbinsX() + 1):
        for y_bin in range(0,  out_hist.GetNbinsY() + 1):
            Histo_rdf_value  = rdf_hist.GetBinContent(x_bin, y_bin)
            Histo_mdf_value  = mdf_hist.GetBinContent(x_bin, y_bin)
            # Histo_rdf_value  = round(Histo_rdf_value, 10)
            # Histo_mdf_value  = round(Histo_mdf_value, 10)
            if(Histo_rdf_value == 0):
                percent_diff = 10000 if(Histo_mdf_value != 0) else 0
            else:
                percent_diff = (abs(Histo_rdf_value - Histo_mdf_value)/Histo_rdf_value)*100
            if(percent_diff   < 20):
                percent_diff  = 0
            out_hist.SetBinContent(x_bin, y_bin, percent_diff)
    return out_hist

def Normalize_Histogram(histogram, set_total=0):
    if(set_total not in [0]):
        histogram.Scale(100 / set_total)
    else:
        integral = histogram.Integral()
        # Check if the integral is non-zero to avoid division by zero
        if(integral != 0):
            histogram.Scale(100 / integral)
    return histogram

def set_common_yaxis_range(hist1, hist2, hist3="N/A", hist4="N/A"):
    # Initialize variables for global min and max
    global_min = float('inf')
    global_max = float('-inf')
    # Loop over the bins of the first histogram
    for bin_ii in range(1, hist1.GetNbinsX() + 1):
        content = hist1.GetBinContent(bin_ii)
        error   = hist1.GetBinError(bin_ii)
        # Update global min/max with content ± error
        global_min = min(global_min, content - error)
        global_max = max(global_max, content + error)
    # Loop over the bins of the second histogram
    for bin_ii in range(1, hist2.GetNbinsX() + 1):
        content = hist2.GetBinContent(bin_ii)
        error   = hist2.GetBinError(bin_ii)
        # Update global min/max with content ± error
        global_min = min(global_min, content - error)
        global_max = max(global_max, content + error)
    if(hist3 not in ["N/A"]):
        for bin_ii in range(1, hist3.GetNbinsX() + 1):
            content = hist3.GetBinContent(bin_ii)
            error   = hist3.GetBinError(bin_ii)
            # Update global min/max with content ± error
            global_min = min(global_min, content - error)
            global_max = max(global_max, content + error)
    if(hist4 not in ["N/A"]):
        for bin_ii in range(1, hist4.GetNbinsX() + 1):
            content = hist4.GetBinContent(bin_ii)
            error   = hist4.GetBinError(bin_ii)
            # Update global min/max with content ± error
            global_min = min(global_min, content - error)
            global_max = max(global_max, content + error)
    global_min = 1.2*global_min if(global_min < 0) else 0.8*global_min
    global_max = 1.5*global_max if(global_max > 0) else 0.8*global_max

    # Set the y-axis range for both histograms to the common range
    hist1.GetYaxis().SetRangeUser(global_min, global_max)
    hist2.GetYaxis().SetRangeUser(global_min, global_max)
    if(hist3 not in ["N/A"]):
        hist3.GetYaxis().SetRangeUser(global_min, global_max)
    if(hist4 not in ["N/A"]):
        hist4.GetYaxis().SetRangeUser(global_min, global_max)

ROOT.gStyle.SetOptStat("i")

# def Draw_V_W_PCal_Cut_Lines(canvas, hist, esec=0, switch_axes=False):
#     """
#     Draws cut lines on a 2D ROOT histogram based on the specified sector (esec).

#     Parameters:
#     - hist: TH2 histogram object, the histogram on which to draw lines.
#     - canvas: TCanvas object, to control the rendering order of lines.
#     - esec: int, sector number (1–6, 0, 'All')
#         * If 0:     Will NOT draw any sector-dependent cuts (produces the same results as esec = 5)
#         * If 'All': Will draw ALL sector-dependent cuts
#     - switch_axes: bool, optional, if True, switches V_PCal and W_PCal between x and y axes.
#     """
#     # Set the canvas to active
#     canvas.cd()

#     # Get axis limits from the histogram
#     x_min = hist.GetXaxis().GetXmin()
#     x_max = hist.GetXaxis().GetXmax()
#     y_min = hist.GetYaxis().GetXmin()
#     y_max = hist.GetYaxis().GetXmax()

#     # Create a TLine array to store and draw lines later
#     lines = []

#     # Sector-dependent cut conditions
#     if ((esec == 1) or (esec == "All")):
#         lines += [(74.2, 79.6, 'W'), (85.4, 90.8, 'W'), (213, 218.4, 'W'), (224.1, 229.5, 'W')]
#     elif ((esec == 2) or (esec == "All")):
#         lines += [(102, 113, 'V')]
#     elif ((esec == 3) or (esec == "All")):
#         lines += [(306, 324, 'V')]
#     elif ((esec == 4) or (esec == "All")):
#         lines += [(235, 240, 'V')]
#     elif ((esec == 6) or (esec == "All")):
#         lines += [(174.1, 179.5, 'W'), (185.2, 190.6, 'W')]

#     # Global cut (not dependent on sector)
#     lines += [(19, None, 'V'), (19, None, 'W')]

#     # Draw the cut lines based on the conditions
#     for line in lines:
#         if ((len(line) == 3) and (line[2] == 'V')):  # Vertical line for V_PCal
#             if switch_axes:
#                 tline = ROOT.TLine(line[0], y_min, line[0], y_max)  # y-axis line
#             else:
#                 tline = ROOT.TLine(x_min, line[0], x_max, line[0])  # x-axis line
#             tline.SetLineColor(ROOT.kRed)
#             tline.SetLineStyle(2)
#             tline.Draw("SAME")

#             if line[1] is not None:
#                 if switch_axes:
#                     tline = ROOT.TLine(line[1], y_min, line[1], y_max)
#                 else:
#                     tline = ROOT.TLine(x_min, line[1], x_max, line[1])
#                 tline.SetLineColor(ROOT.kRed)
#                 tline.SetLineStyle(2)
#                 tline.Draw("SAME")

#         elif ((len(line) == 3) and (line[2] == 'W')):  # Horizontal line for W_PCal
#             if switch_axes:
#                 tline = ROOT.TLine(x_min, line[0], x_max, line[0])  # x-axis line
#             else:
#                 tline = ROOT.TLine(line[0], y_min, line[0], y_max)  # y-axis line
#             tline.SetLineColor(ROOT.kRed)
#             tline.SetLineStyle(2)
#             tline.Draw("SAME")

#             if line[1] is not None:
#                 if switch_axes:
#                     tline = ROOT.TLine(x_min, line[1], x_max, line[1])
#                 else:
#                     tline = ROOT.TLine(line[1], y_min, line[1], y_max)
#                 tline.SetLineColor(ROOT.kRed)
#                 tline.SetLineStyle(2)
#                 tline.Draw("SAME")

#     # Update the canvas to ensure lines are displayed correctly on top
#     canvas.Modified()
#     canvas.Update()
def Draw_V_W_PCal_Cut_Lines(hist, esec=0, switch_axes=False):
    """
    Returns a list of TLine objects for cut lines based on the specified sector (esec),
    adjusted to the histogram's axis limits.

    Parameters:
    - hist: TH2 histogram object to obtain axis limits
    - esec: int, sector number (1–6, 0, 'All')
        * If 0:     Will NOT draw any sector-dependent cuts (produces same results as esec = 5)
        * If 'All': Will draw ALL sector-dependent cuts
    - switch_axes: bool, optional, if True, switches V_PCal and W_PCal between x and y axes
    
    Returns:
    - lines: list of ROOT.TLine objects that can be drawn later
    """
    # Get axis limits from the histogram
    x_min = hist.GetXaxis().GetXmin()
    x_max = hist.GetXaxis().GetXmax()
    y_min = hist.GetYaxis().GetXmin()
    y_max = hist.GetYaxis().GetXmax()

    lines = []

    # Sector-dependent cut conditions
    if(esec in [1, "All"]):
        lines += [(74.2, 79.6, 'W'), (85.4, 90.8, 'W'), (213, 218.4, 'W'), (224.1, 229.5, 'W')]
    if(esec in [2, "All"]):
        lines += [(102, 113, 'V')]
    # if(esec in [3, "All"]):
    #     lines += [(306, 324, 'V')]
    if(esec in [4, "All"]):
        lines += [(230, 240, 'V')]
    if(esec in [6, "All"]):
        lines += [(174.1, 179.5, 'W'), (185.2, 190.6, 'W')]

    # Global cut (not dependent on sector)
    lines += [(19, None, 'V'), (19, None, 'W')]

    line_width = 3
    # Create TLine objects based on the conditions
    tlines = []
    for line in lines:
        if((len(line) == 3) and (line[2] == 'V')):  # Vertical line for V_PCal
            if(switch_axes):
                tline = ROOT.TLine(line[0], y_min, line[0], y_max)  # Vertical line along y-axis
                tline.SetLineColor(ROOT.kRed)
                tline.SetLineStyle(2)
                tline.SetLineWidth(line_width)
                tlines.append(tline)
                if(line[1] is not None):
                    tline = ROOT.TLine(line[1], y_min, line[1], y_max)
                    tline.SetLineColor(ROOT.kRed)
                    tline.SetLineStyle(2)
                    tline.SetLineWidth(line_width)
                    tlines.append(tline)
            else:
                tline = ROOT.TLine(x_min, line[0], x_max, line[0])  # Horizontal line along x-axis
                tline.SetLineColor(ROOT.kRed)
                tline.SetLineStyle(2)
                tline.SetLineWidth(line_width)
                tlines.append(tline)
                if(line[1] is not None):
                    tline = ROOT.TLine(x_min, line[1], x_max, line[1])
                    tline.SetLineColor(ROOT.kRed)
                    tline.SetLineStyle(2)
                    tline.SetLineWidth(line_width)
                    tlines.append(tline)
        elif((len(line) == 3) and (line[2] == 'W')):  # Horizontal line for W_PCal
            if(switch_axes):
                tline = ROOT.TLine(x_min, line[0], x_max, line[0])  # Horizontal line along x-axis
                tline.SetLineColor(ROOT.kRed)
                tline.SetLineStyle(2)
                tline.SetLineWidth(line_width)
                tlines.append(tline)
                if(line[1] is not None):
                    tline = ROOT.TLine(x_min, line[1], x_max, line[1])
                    tline.SetLineColor(ROOT.kRed)
                    tline.SetLineStyle(2)
                    tline.SetLineWidth(line_width)
                    tlines.append(tline)
            else:
                tline = ROOT.TLine(line[0], y_min, line[0], y_max)  # Vertical line along y-axis
                tline.SetLineColor(ROOT.kRed)
                tline.SetLineStyle(2)
                tline.SetLineWidth(line_width)
                tlines.append(tline)
                if(line[1] is not None):
                    tline = ROOT.TLine(line[1], y_min, line[1], y_max)
                    tline.SetLineColor(ROOT.kRed)
                    tline.SetLineStyle(2)
                    tline.SetLineWidth(line_width)
                    tlines.append(tline)

    return tlines

# Run Checks:
if(__name__ == "__main__"):
    # Check 'rdf':
    if(True and ("class cppyy.gbl.ROOT.RDataFrame" in str(type(rdf)))):
        print(f"For {color.BOLD}'rdf'{color.END}:")
        for num, ii in enumerate(rdf.GetColumnNames()):
            print(f"\tColumn {str(num+1).rjust(3)}) {color.BOLD}{str(ii).ljust(40)}{color.END}")
            # print(f"\tColumn {str(num+1).rjust(3)}) {str(ii).ljust(35)} | (type -> {type(ii)})")
    elif("class cppyy.gbl.ROOT.RDataFrame" not in str(type(rdf))):
        print(f"\n{color.Error}ERROR: 'rdf' is NOT an RDataFrame\n{color.END}")
    
    print("\n")
    
    # Check 'mdf':
    if(True and ("class cppyy.gbl.ROOT.RDataFrame" in str(type(mdf)))):
        print(f"For {color.BOLD}'mdf'{color.END}:")
        for num, ii in enumerate(mdf.GetColumnNames()):
            print(f"\tColumn {str(num+1).rjust(3)}) {color.BOLD}{str(ii).ljust(40)}{color.END}")
    elif("class cppyy.gbl.ROOT.RDataFrame" not in str(type(mdf))):
        print(f"\n{color.Error}ERROR: 'mdf' is NOT an RDataFrame\n{color.END}")
    
    print("\n")
    
    # Check 'gdf':
    if(True and ("class cppyy.gbl.ROOT.RDataFrame" in str(type(gdf)))):
        print(f"For {color.BOLD}'gdf'{color.END}:")
        for num, ii in enumerate(gdf.GetColumnNames()):
            print(f"\tColumn {str(num+1).rjust(3)}) {color.BOLD}{str(ii).ljust(40)}{color.END}")
    elif("class cppyy.gbl.ROOT.RDataFrame" not in str(type(gdf))):
        print(f"\n{color.Error}ERROR: 'gdf' is NOT an RDataFrame\n{color.END}")
    
    print("\n\nDone\n\n")
else:
    print(f"\n{color.BOLD}Not currently checking the RDataFrames' contents\n{color.END}")