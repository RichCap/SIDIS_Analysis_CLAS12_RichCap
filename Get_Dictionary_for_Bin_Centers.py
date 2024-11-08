#!/usr/bin/env python3

import ROOT
import numpy
import traceback
from datetime import datetime
from array    import array
from MyCommonAnalysisFunction_richcap import *
import math
import copy
import argparse

# ROOT configuration
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3, 'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gROOT.SetBatch(1) # Turns off the canvases when running in the command line

# Argument parsing setup
parser = argparse.ArgumentParser(description=f"{color.BOLD}Code for print out new definitions of the 'Get_Bin_Center_Dictionary' dictionary use across my SIDIS Analysis.{color.END}", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-cn",    "--common-name",        type=str,            default="Pass_2_New_Fiducial_Cut_Test_FC_14_V13_All",                                   help="Set the Common_Name for file naming (Default: 'Pass_2_New_Fiducial_Cut_Test_FC_14_V13_All')")
parser.add_argument("-so",    "--smearing-options",   type=str,            default="no_smear",                                   choices=["no_smear", "smear"],    help="Set the smearing option (Default: 'no_smear')")
parser.add_argument("-check", "--check-inputs",                             action="store_true",                                                                   help="Enable Check_Inputs (Default: False)")
parser.add_argument("-cA",    "--check-inputs-all",                         action="store_true",                                                                   help="Enable Check_Inputs_All (Default: False)")
parser.add_argument("-Nxb",   "--use-xb",                                   action="store_true",                                                                   help="Disables Use_xB (Default: Use_xB = True)")
parser.add_argument("-df",    "--data-frame",         type=str,            default="rdf",                                        choices=["rdf", "mdf"],           help="Select DataFrame to use (Default: 'rdf')")
parser.add_argument("-cut",   "--cut-type",           type=str,            default="cut_Complete_SIDIS",                                                           help="Set the Cut_Type (Default: 'cut_Complete_SIDIS')")
parser.add_argument("-D",     "--draw-histos",                              action="store_true",                                                                   help="Enable drawing histograms (Default: False)")
parser.add_argument("-s",     "-save",                "--save-histos",      action="store_true",                                                                   help="Enable saving histograms (Default: False)")
parser.add_argument("-pc",    "-print",               "--print-centers",    action="store_true",                                                                   help="Enable printing bin centers (Default: False)")
parser.add_argument("-q2-y",  "--select-q2-y-bin",    type=int, nargs="+", default=range(0, 18),                                                                   help="Select Q2_y bins (Default: range(0, 18))")
parser.add_argument("-zpT",   "--skip-z-pt",                                action="store_true",                                                                   help="Skip z_pT_Q bin selection (Default: False)")
args = parser.parse_args()

print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis\n{color.END}")

# Getting and formatting current date and time
datetime_object_full = datetime.now()

# Formatting date and time into a 12-hour format with a.m./p.m.
formatted_time = datetime_object_full.strftime("%B %d, %Y at %I:%M %p")

# Printing the formatted date and time
print(f"{color.BOLD}Ran on {formatted_time}{color.END}\n")


# Using parsed arguments
Common_Name      = args.common_name
Smearing_Options = args.smearing_options
Check_Inputs     = args.check_inputs
Check_Inputs_All = args.check_inputs_all
Use_xB           = not args.use_xb
Data_Frame       = args.data_frame
Cut_Type         = args.cut_type
Draw_Histos      = args.draw_histos
Save_Histos      = args.save_histos
Print_Centers    = args.print_centers
Select_Q2_y_Bin  = args.select_q2_y_bin
Skip_z_pT_Q      = args.skip_z_pt



# File location function
def FileLocation(FileName, Datatype):
    location = "Histo_Files_ROOT/"
    if(str(Datatype)   in ['rdf']):
        file = f"REAL_Data/SIDIS_epip_Data_REC_{FileName}.root"
    elif(str(Datatype) in ['mdf']):
        file = f"Matching_REC_MC/SIDIS_epip_MC_Matched_{FileName}.root"
    elif(str(Datatype) in ['gdf']):
        file = f"GEN_MC/SIDIS_epip_MC_GEN_{FileName}.root"
    else:
        raise ValueError("Invalid Datatype specified.")
    return location + file

# Additional configuration
Standard_Histogram_Title_Addition = ""
Pass_Version = "Pass 2" if("Pass_2" in Common_Name) else "Pass 1"
if(Pass_Version not in [""]):
    Standard_Histogram_Title_Addition = Pass_Version

if("Tagged_Proton" in Common_Name):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"{Standard_Histogram_Title_Addition} - Tagged Proton"
    else:
        Standard_Histogram_Title_Addition = "Tagged Proton"
    print(f"{color.BGREEN}\nRunning with 'Tagged Proton' files{color.END}")

print(f"{color.BBLUE}\nRunning with {Pass_Version} files\n\n{color.END}")

# Loading files into RDataFrames
print(f"{color.BOLD}DataFrame in use = {color.UNDERLINE}{Data_Frame}{color.END}\n")
try:
    if(Data_Frame == "rdf"):
        # Real (Experimental) Data configuration
        REAL_File_Name = Common_Name
        df = ROOT.TFile(FileLocation(REAL_File_Name, "rdf"), "READ")
        print(f"The total number of histograms available for the {color.BLUE}Real (Experimental) Data{color.END} in '{color.BOLD}{REAL_File_Name}{color.END}' is {color.BOLD}{len(df.GetListOfKeys())}{color.END}")
    else:
        # Reconstructed Monte Carlo Data configuration
        MC_REC_File_Name = f"Unsmeared_{Common_Name}" if(Smearing_Options == "no_smear") else Common_Name
        df = ROOT.TFile(FileLocation(MC_REC_File_Name, "mdf"), "READ")
        print(f"The total number of histograms available for the {color.RED}Reconstructed Monte Carlo Data{color.END} in '{color.BOLD}{MC_REC_File_Name}{color.END}' is {color.BOLD}{len(df.GetListOfKeys())}{color.END}")
except Exception:
    print(f"{color.Error}\nERROR IN GETTING THE '{Data_Frame}' DATAFRAME...\nTraceback:\n{color.END_R}{traceback.format_exc()}{color.END}")


print(f"{color.BOLD}\nPass Version in use is:{color.END_b} {Pass_Version}{color.END_B}\n\n\nDone Loading RDataFrame files...\n\n{color.END}")


# Loop through histograms in the selected DataFrame
histo_count = 0
for df_name in df.GetListOfKeys():
    if(f"'{Data_Frame}'" in str(df_name.GetName())):
        if("Normal_2D" in str(df_name.GetName())):
            if(f"(Data-Cut='{Cut_Type}')" in str(df_name.GetName())):
                if(("Var-D2='xB'" in str(df_name.GetName())) and (not Use_xB)):
                    continue
                if("Var-D1='Q2'" in str(df_name.GetName())):
                    histo_count += 1
                    if(Check_Inputs):
                        print(f"{color.BOLD}Histo {histo_count}:{color.BBLUE}\n\t {df_name.GetName()}{color.END}\n")
                if("Var-D1='z'" in str(df_name.GetName())):
                    histo_count += 1
                    if(Check_Inputs):
                        print(f"{color.BOLD}Histo {histo_count}:{color.BGREEN}\n\t {df_name.GetName()}{color.END}\n")
        if(Check_Inputs_All):
            print(f"{color.RED}\t {df_name.GetName()}{color.END}\n")
    else:
        print(f"{color.Error}Could not find the correct dataframe type (i.e., '{Data_Frame}'){color.END}")
        break

# Check if the histogram count is as expected
if(histo_count not in [36, 54]):
    print(f"{color.Error}histo_count (Total) = {histo_count} is the incorrect number of histograms{color.END_R}\n\tCheck input file with 'Check_Inputs' or 'Check_Inputs_All'{color.END}")
else:
    print(f"{color.BOLD}histo_count (Total) = {histo_count}{color.END}\n")



Q2_y_borders = {}
Q2_xB_border = {}
for Q2_Y_Bin_ii in range(1, 18, 1):
    Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
    Q2_y_borders[f"{Q2_Y_Bin_ii}_RED"] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
    for line in Q2_y_borders[f"{Q2_Y_Bin_ii}_RED"]:
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(5)
    if(Use_xB):
        Q2_xB_border[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii,          Use_xB=Use_xB)
        Q2_xB_border[f"{Q2_Y_Bin_ii}_RED"] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, Use_xB=Use_xB)
        for line in Q2_xB_border[f"{Q2_Y_Bin_ii}_RED"]:
            line.SetLineColor(ROOT.kRed)
            line.SetLineWidth(5)
statbox, Q2_vs_xB_Histo, Q2_vs_y_Histo, z_vs_pT_Histo, canvas_main = {}, {}, {}, {}, {}
Final_Output = {"Key": ["mean_Q2", "ErrorQ2", "mean__y", "Error_y", "mean__z", "Error_z", "mean_pT", "ErrorpT"]}
if(Use_xB):
    Final_Output["Key"].append("mean_xB")
    Final_Output["Key"].append("ErrorxB")
    
for Q2_y_Bin in range(0, 18):
    if(Q2_y_Bin not in Select_Q2_y_Bin):
        continue
    if(Q2_y_Bin     in [0]):
        Q2_y_Bin = "All"
    Q2_vs_y_Name      = f"((Histo-Group='Normal_2D'), (Data-Type='{Data_Frame}'), (Data-Cut='{Cut_Type}'), (Smear-Type=''), (Binning-Type='Y_bin'-[Q2-y-Bin={Q2_y_Bin}, z-PT-Bin=All]), (Var-D1='Q2'-[NumBins=280, MinBin=0, MaxBin=14]), (Var-D2='y'-[NumBins=100, MinBin=0, MaxBin=1]))"
    z_vs_pT_Name      = f"((Histo-Group='Normal_2D'), (Data-Type='{Data_Frame}'), (Data-Cut='{Cut_Type}'), (Smear-Type=''), (Binning-Type='Y_bin'-[Q2-y-Bin={Q2_y_Bin}, z-PT-Bin=All]), (Var-D1='z'-[NumBins=120, MinBin=0, MaxBin=1.2]), (Var-D2='pT'-[NumBins=200, MinBin=0, MaxBin=2.0]))"
    Q2_vs_y_Histo[f"({Q2_y_Bin})"] = df.Get(Q2_vs_y_Name)
    z_vs_pT_Histo[f"({Q2_y_Bin})"] = df.Get(z_vs_pT_Name)
    if(Use_xB):
        Q2_vs_xB_Name = f"((Histo-Group='Normal_2D'), (Data-Type='{Data_Frame}'), (Data-Cut='{Cut_Type}'), (Smear-Type=''), (Binning-Type='Y_bin'-[Q2-y-Bin={Q2_y_Bin}, z-PT-Bin=All]), (Var-D1='Q2'-[NumBins=280, MinBin=0, MaxBin=14]), (Var-D2='xB'-[NumBins=50, MinBin=0.09, MaxBin=0.826]))"
        Q2_vs_xB_Histo[f"({Q2_y_Bin})"] = df.Get(Q2_vs_xB_Name)
    
    z_pT_Bin_List = ["All"]
    if(not Skip_z_pT_Q):
        z_pT_Bin_List.extend(range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin)[1] + 1))
    for z_pT_Bin in z_pT_Bin_List:
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="_Y_bin")):
            continue
            
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_y_Histo[f"({Q2_y_Bin})"].Clone(Q2_vs_y_Name.replace("z-PT-Bin=All",  f"z-PT-Bin={z_pT_Bin}"))
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = z_vs_pT_Histo[f"({Q2_y_Bin})"].Clone(z_vs_pT_Name.replace("z-PT-Bin=All",  f"z-PT-Bin={z_pT_Bin}"))
        
        if(z_pT_Bin not in ["All", "0", 0]):
            Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(z_pT_Bin, z_pT_Bin)
            z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(z_pT_Bin, z_pT_Bin)
        else:
            Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(0.5, 50)
            z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(-0.5 if(Skip_z_pT_Q) else 0.5, 50)
        
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Project3D("yz")
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Project3D("yz")
        
        Kinematic_Bin = "".join(["Q^{2}-y Bin: ", str(Q2_y_Bin), " #topbar z-P_{T} Bin: ", str(z_pT_Bin)])

        Q2_vs_y_Title = "".join(["#splitline{#splitline{#splitline{", "Experimental" if(str(Data_Frame) in ["rdf"]) else "MC REC" if(str(Data_Frame) in ["mdf"]) else "MC GEN" if(str(Data_Frame) in ["gdf"]) else "ERROR", " Data}{", str(root_color.Bold), "{Q^{2} vs y Plot}}}{", str(root_color.Bold), "{", str(Kinematic_Bin), "}}}{", str(root_color.Bold), "{Pass Version:} #color[", str(root_color.Blue), "]{", str(Standard_Histogram_Title_Addition), "}}"])
        z_vs_pT_Title = "".join(["#splitline{#splitline{#splitline{", "Experimental" if(str(Data_Frame) in ["rdf"]) else "MC REC" if(str(Data_Frame) in ["mdf"]) else "MC GEN" if(str(Data_Frame) in ["gdf"]) else "ERROR", " Data}{", str(root_color.Bold), "{z vs P_{T} Plot}}}{", str(root_color.Bold), "{", str(Kinematic_Bin), "}}}{", str(root_color.Bold), "{Pass Version:} #color[", str(root_color.Blue), "]{", str(Standard_Histogram_Title_Addition), "}}"])

        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetTitle(Q2_vs_y_Title)
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetTitle(z_vs_pT_Title)
        
        if(Use_xB):
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_xB_Histo[f"({Q2_y_Bin})"].Clone(Q2_vs_xB_Name.replace("z-PT-Bin=All", f"z-PT-Bin={z_pT_Bin}"))
            if(z_pT_Bin not in ["All", "0", 0]):
                Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(z_pT_Bin, z_pT_Bin)
            else:
                Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(-0.5 if(Skip_z_pT_Q) else 0.5, 50)
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Project3D("yz")
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetTitle(Q2_vs_y_Title.replace("y Plot", "x_{B} Plot"))
        
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetYaxis().SetRangeUser(0 if(Skip_z_pT_Q) else 0.5, 11.5 if(Skip_z_pT_Q) else 9)
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(0.2, 0.9)
        if(Use_xB):
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetYaxis().SetRangeUser(0.5, 9)
        
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetYaxis().SetRangeUser(0.01, 1.0 if(Skip_z_pT_Q) else 0.8)
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetXaxis().SetRangeUser(0,    1.6 if(Skip_z_pT_Q) else 1.1)
        
        canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"] = Canvas_Create(Name=f"({Q2_y_Bin}, {z_pT_Bin})", Num_Columns=3 if(Use_xB) else 2, Num_Rows=1, Size_X=1600, Size_Y=1200, cd_Space=0)
        Draw_Canvas(canvas=canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"], cd_num=1, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Draw("colz")
        Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetStats(ROOT.kTRUE)  # Ensure statistics box is enabled
        ROOT.gStyle.SetOptStat(1100)  # '11' means decimal part of precision, '00'
        
        statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetListOfFunctions().FindObject("stats")
        if(statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"]):
            statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"].SetX1NDC(0.55)   # X position of left edge
            statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"].SetX2NDC(0.85)   # X position of right edge
            statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"].SetY1NDC(0.15)   # Y position of bottom edge
            statbox[f"Q2_vs_y_({Q2_y_Bin}, {z_pT_Bin})"].SetY2NDC(0.25)   # Y position of top edge
        for Q2_Y_Bin_ii in range(1, 18, 1):
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.SetLineColor(ROOT.kBlack)
                line.SetLineWidth(2)
                line.Draw("same")
        if(Q2_y_Bin not in [0, "All"]):
            for line_current in Q2_y_borders[f"{Q2_y_Bin}_RED"]:
                line_current.Draw("same")
            
        Draw_Canvas(canvas=canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"], cd_num=2, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Draw("colz")
        z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetStats(ROOT.kTRUE)  # Ensure statistics box is enabled
        ROOT.gStyle.SetOptStat(1100)  # '11' means decimal part of precision, '00'
        statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"] = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetListOfFunctions().FindObject("stats")
        if(statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"]):
            statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"].SetX1NDC(0.55)   # X position of left edge
            statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"].SetX2NDC(0.85)  # X position of right edge
            statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"].SetY1NDC(0.15)  # Y position of bottom edge
            statbox[f"z_vs_pT_({Q2_y_Bin}, {z_pT_Bin})"].SetY2NDC(0.25)  # Y position of top edge
        if(Q2_y_Bin not in ["All", "0", 0]):
            Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=int(Q2_y_Bin), Set_Max_Y=1.2, Set_Max_X=1.2, Plot_Orientation_Input="z_pT")
            
        if(Use_xB):
            Draw_Canvas(canvas=canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"], cd_num=3, left_add=0.15, right_add=0.15, up_add=0.15, down_add=0.15)
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].Draw("colz")
            Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].SetStats(ROOT.kTRUE)  # Ensure statistics box is enabled
            ROOT.gStyle.SetOptStat(1100)  # '11' means decimal part of precision, '00'
            statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"] = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetListOfFunctions().FindObject("stats")
            if(statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"]):
                statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"].SetX1NDC(0.55)   # X position of left edge
                statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"].SetX2NDC(0.85)  # X position of right edge
                statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"].SetY1NDC(0.15)  # Y position of bottom edge
                statbox[f"Q2_vs_xB_({Q2_y_Bin}, {z_pT_Bin})"].SetY2NDC(0.25)  # Y position of top edge
            for Q2_Y_Bin_ii in range(1, 18, 1):
                for line in Q2_xB_border[Q2_Y_Bin_ii]:
                    line.SetLineColor(ROOT.kBlack)
                    line.SetLineWidth(2)
                    line.Draw("same")
            if(Q2_y_Bin not in [0, "All"]):
                for line_current in Q2_xB_border[f"{Q2_y_Bin}_RED"]:
                    line_current.Draw("same")
            
        mean_Q2 = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(2)  # 2 denotes the Y-axis
        mean__y = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(1)  # 1 denotes the X-axis
        Q2_vs_y_entries = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetEntries()
        sdev_Q2 = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetStdDev(2)
        sdev__y = Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetStdDev(1)
        ErrorQ2 = (sdev_Q2/ROOT.sqrt(Q2_vs_y_entries)) if(Q2_vs_y_entries > 0) else 0
        Error_y = (sdev__y/ROOT.sqrt(Q2_vs_y_entries)) if(Q2_vs_y_entries > 0) else 0
        
        mean__z = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(2)  # 2 denotes the Y-axis
        mean_pT = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(1)  # 1 denotes the X-axis
        z_vs_pT_entries = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetEntries()
        sdev__z = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetStdDev(2)
        sdev_pT = z_vs_pT_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetStdDev(1)
        Error_z = (sdev__z/ROOT.sqrt(z_vs_pT_entries)) if(z_vs_pT_entries > 0) else 0
        ErrorpT = (sdev_pT/ROOT.sqrt(z_vs_pT_entries)) if(z_vs_pT_entries > 0) else 0
        
        if(Use_xB):
            mean_xB     = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(1)  # 1 denotes the X-axis
            mean_Q2_xB  = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(2)
            Q2_vs_xB_entries = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetEntries()
            sdev_xB = Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetStdDev(1)
            ErrorxB = (sdev_xB/ROOT.sqrt(Q2_vs_xB_entries)) if(Q2_vs_xB_entries > 0) else 0
            if(round(mean_Q2, 3) != round(mean_Q2_xB, 3)):
                print(f"""{color.Error}
Q2_vs_y_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(2)  = {mean_Q2}
Q2_vs_xB_Histo[f"({Q2_y_Bin}, {z_pT_Bin})"].GetMean(2) = {mean_Q2_xB}
{color.END}""")
            if(Print_Centers):
                print(f"For ({Q2_y_Bin}-{z_pT_Bin}):\t [mean_Q2, ErrorQ2, mean__y, Error_y, mean__z, Error_z, mean_pT, ErrorpT, mean_xB, ErrorxB] = [{round(mean_Q2, 3)}, {round(ErrorQ2, 7)}, {round(mean__y, 4)}, {round(Error_y, 7)}, {round(mean__z, 4)}, {round(Error_z, 7)}, {round(mean_pT, 4)}, {round(ErrorpT, 7)}, {round(mean_xB, 4)}, {round(ErrorxB, 7)}]")
            Final_Output[f"{Q2_y_Bin}-{z_pT_Bin}"] = [round(mean_Q2, 3), round(ErrorQ2, 7), round(mean__y, 4), round(Error_y, 7), round(mean__z, 4), round(Error_z, 7), round(mean_pT, 4), round(ErrorpT, 7), round(mean_xB, 4), round(ErrorxB, 7)]
        else:
            if(Print_Centers):
                print(f"For ({Q2_y_Bin}-{z_pT_Bin}):\t [mean_Q2, ErrorQ2, mean__y, Error_y, mean__z, Error_z, mean_pT, ErrorpT] = [{round(mean_Q2, 3)}, {round(ErrorQ2, 7)}, {round(mean__y, 4)}, {round(Error_y, 7)}, {round(mean__z, 4)}, {round(Error_z, 7)}, {round(mean_pT, 4)}, {round(ErrorpT, 7)}]")
            Final_Output[f"{Q2_y_Bin}-{z_pT_Bin}"] = [round(mean_Q2, 3), round(ErrorQ2, 7), round(mean__y, 4), round(Error_y, 7), round(mean__z, 4), round(Error_z, 7), round(mean_pT, 4), round(ErrorpT, 7)]
            
        if(Draw_Histos):
            canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"].Draw()
        Save_Name = f"Normal_2D_Histos_For_Q2_y_Bin_{Q2_y_Bin}_z_pT_Bin_{z_pT_Bin}.pdf"
        if(Save_Histos):
            canvas_main[f"({Q2_y_Bin}, {z_pT_Bin})"].SaveAs(Save_Name)
            print(f"\n{color.BBLUE}Saved: {color.UNDERLINE}{Save_Name}{color.END}\n")
        else:
            print(f"\n{color.BLUE}Would be saving: {color.END_B}{color.UNDERLINE}{Save_Name}{color.END}\n")
            




# Final Output:
print("".join([f"""{color.BBLUE}
# From Common_Name = {Common_Name} (Added on {datetime_object_full.strftime("%B %d, %Y")}){color.END_B}
Get_Bin_Center_Dictionary = {Final_Output}
""", """
def Get_Bin_Center_Function(Q2_y_Bin, z_pT_Bin, Variable="All"):
    if(str(z_pT_Bin) in ["0", 0, "all"]):
        z_pT_Bin = "All"
    if(Variable in ["All"]):
        return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"]
    else:
        if(str(Variable) in ["mean_Q2",  "Q2"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][0]
        if(str(Variable) in ["Error_Q2", "error_Q2"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][1]
        if(str(Variable) in ["mean_y",   "y"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][2]
        if(str(Variable) in ["Error_y",  "error_y"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][3]
        if(str(Variable) in ["mean_z",   "z"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][4]
        if(str(Variable) in ["Error_z",  "error_z"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][5]
        if(str(Variable) in ["mean_pT",  "pT"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][6]
        if(str(Variable) in ["Error_pT", "error_pT"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][7]
        if(str(Variable) in ["mean_xB",  "xB"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][8]
        if(str(Variable) in ["Error_xB", "error_xB"]):
            return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"][9]
    print(f"POTENTIAL ERROR: Get_Bin_Center_Function({Q2_y_Bin}, {z_pT_Bin}, {Variable}) did not return anything yet... (returning Variable='All')")
    return Get_Bin_Center_Dictionary[f"{Q2_y_Bin}-{z_pT_Bin}"]
""" if(not True) else "", color.END]))




if(Cut_Type not in ["cut_Complete_SIDIS"]):
    print(f"\n\n{color.RED}Cut used: '{Cut_Type}'{color.END}\n\n")


# Capture the end time
end_time = datetime.now()

# Calculate the duration
duration = end_time - datetime_object_full
# Extract hours, minutes, and seconds from the duration
hours, remainder = divmod(duration.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)

# Format and print the end time and duration
formatted_end_time = end_time.strftime("%I:%M %p")
print(f"{color.BGREEN}\n\n\nDone running at {formatted_end_time}{color.END}")
print(f"{color.BLUE}\tTotal run time: {int(hours)} Hours, {int(minutes)} Minutes, and {float(seconds)} Seconds{color.END}\n\n")

