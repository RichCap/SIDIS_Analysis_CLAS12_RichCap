#!/usr/bin/env python

import sys

print("Starting...\n")

from datetime import datetime
datetime_object_full = datetime.now() # Getting Current Date

from ROOT import gRandom, TH1, TH1D, TCanvas, cout
import ROOT
import math

# # Turns off the canvases when running in the command line
# ROOT.gROOT.SetBatch(1)

import traceback
import shutil
import os
import re

from MyCommonAnalysisFunction_richcap    import *
from Convert_MultiDim_Kinematic_Bins     import *
from Fit_Related_Functions_For_RooUnfold import *

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)

       
Saving_Q         = True
Fit_Test         = True
Smearing_Options = "both"
if(len(sys.argv) > 1):
    arg_option_1 = str(sys.argv[1])
    if(arg_option_1 in ["test", "Test", "time", "Time"]):
        print("\nNOT SAVING\n")
        Saving_Q = False
    else:
        print("".join(["\nOption Selected: ", str(arg_option_1), " (Still Saving...)" if("no_save" not in str(arg_option_1)) else " (NOT SAVING)"]))
        Saving_Q         = True  if("no_save" not in str(arg_option_1)) else False
        Fit_Test         = True  if("no_fit"  not in str(arg_option_1)) else False
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
        
if(not Fit_Test):
    print("\n")
    print("".join([color.BBLUE, color_bg.RED, """\n\n    Not Fitting Plots    \n""", color.END, "\n\n"]))
    

    

if(str(Smearing_Options) in ["both"]):
    Smearing_Options = "smear"
print(color.BBLUE, "\nSmear option selected is:", "No Smear" if(str(Smearing_Options) in ["", "no_smear"]) else str(Smearing_Options.replace("_s", "S")).replace("s", "S"), color.END, "\n")

File_Save_Format = ".png"
# File_Save_Format = ".root"
# File_Save_Format = ".pdf"


if((File_Save_Format != ".png") and Saving_Q):
    print(color.BGREEN, "\nSave Option was not set to output .png files. Save format is:", "".join([color.END_B, color.UNDERLINE, str(File_Save_Format), color.END, "\n"]))

    
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
# # # # "list of Q2-xB bins to run" options (notes):
#     (*) Can select bins numbered 0-17 (0 is for 'All Bins' histograms) - Order does not matter
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

# # Getting Current Date
# datetime_object_full = datetime.now()

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
    print("".join([color.Error, "ERROR: \n", color.END_R, str(traceback.format_exc()), color.END, "\n"]))
    # print("Somehow the python module was not found, let's try loading the library by hand...")
    # try:
    #     ROOT.gSystem.Load("libRooUnfold.so")
    # except:
    #     print("".join([color.Error, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END_R, str(traceback.format_exc()), color.END]))
        
        
print("\n\n")



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
            Method_Title = "".join([" #color[", str(root_color.Blue),  "]{(Experimental)}"])
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
        if(Method in ["Acceptance"]):
            Method_Title = "".join(["(", str(root_color.Bold),  "{Acceptance})"])
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
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END, "\nName =", str(Name), "\n"]))
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END, "\nName =", str(Name), "\n"]))
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
                                if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
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





##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##










def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default", MC_BGS_1D="None", Test_Bayes_Iterations=False):
#############################################################################################################################################################################
#############################################################################################################################################################################

##############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method(s): "Test"         #####=====#####=====#####=====#####
##############################################################################################################
    if("Test" in str(Method)):
        print("".join([color.ERROR, "Starting ", color.UNDERLINE, color.BLUE, "TEST", color.END_B, color.RED, " Procedure (returning all sliced 1D histos)...", color.END]))
        Sliced_OutPut    = {}
        bayes_iterations = 0
        for Histos_for_Slicing, bayes_iterations in [[MC_GEN_1D, 0], [ExREAL_1D, 1], [MC_REC_1D, 2], [MC_BGS_1D, 3]]:
            Sliced_1D = Multi5D_Slice(Histo=Histos_for_Slicing, Title="Title", Name=Histos_for_Slicing.GetName(), Method=Method, Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="Smear" if("Smear-Type=''" not in MC_REC_1D.GetName()) else "", Out_Option="histo", Fitting_Input="off")[0]
            for ii in Sliced_1D:
                Sliced_OutPut[f"{ii}_(Iteration_{bayes_iterations})"] = Sliced_1D[ii].Clone(f"{ii}_(Iteration_{bayes_iterations})")
        return Sliced_OutPut
##############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method(s): "Test"         #####=====#####=====#####=====#####
##############################################################################################################

##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    if(("RooUnfold" in str(Method)) or (str(Method) in ["Default"])):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END_B, color.CYAN, " Unfolding Procedure...", color.END]))
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
            # Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle())])
            Response_2D_Input       = Response_2D
        del Response_2D

        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, "".join([str(Response_2D_Input.GetName()).replace("_Flipped", ""), "_RooUnfoldResponse_Object"]), Response_2D_Input_Title)
                
                if(MC_BGS_1D != "None"):
                    # Background Subtraction Method 1: Fill the Response_RooUnfold object explicitly with the content of a background histogram with the Fake() function
                    for rec_bin in range(0, nBins_CVM + 1, 1):
                        rec_val = MC_BGS_1D.GetBinCenter(rec_bin)
                        rec_con = MC_BGS_1D.GetBinContent(rec_bin)
                        Response_RooUnfold.Fake(rec_val, w=rec_con)
                    

##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if("bbb" in str(Method)):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print("".join(["\t", color.CYAN, "Using ", color.BGREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)

                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print("".join(["\t", color.CYAN, "Using ", color.BGREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)

                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print("".join(["\t", color.RED, "Method '",                 color.BOLD,   str(Method),       color.END_R,           "' is unknown/undefined...", color.END]))
                        print("".join(["\t", color.RED, "Defaulting to using the ", color.BGREEN, str(Unfold_Title), color.END_R,           " method to unfold...",      color.END]))
                    else:
                        print("".join(["\t", color.CYAN, "Using ",                  color.BGREEN, str(Unfold_Title), color.END, color.CYAN, " method to unfold...",      color.END]))
                    
                    if(not Test_Bayes_Iterations):
                        #########################################
                        ##=====##  Bayesian Iterations  ##=====##
                        #########################################
                        bayes_iterations = 10 if(("Multi_Dim" not in str(Name_Main)) or ("Multi_Dim_z_pT_Bin" in str(Name_Main))) else 4
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
                    else:
                        Bin_Acceptance = MC_REC_1D.Clone()
                        Bin_Acceptance.Sumw2()
                        Bin_Acceptance.Divide(MC_GEN_1D)
                        print(f"{color.BBLUE}Performing Iteration Test of 5D Bayes Unfolding...{color.END}")
                        for bayes_iterations in range(1, 5):
                            Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)
                            for bin_rec in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                                if(MC_REC_1D.GetBinContent(bin_rec) == 0):
                                    Unfolded_Histo.SetBinError(bin_rec,          0)
                                    Unfolded_Histo.SetBinContent(bin_rec,        0)
                            for bin_acceptance in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
                                if(Bin_Acceptance.GetBinContent(bin_acceptance) < 0.02):
                                    Unfolded_Histo.SetBinError(bin_acceptance,   0)
                                    Unfolded_Histo.SetBinContent(bin_acceptance, 0)
                            Sliced_1D = Multi5D_Slice(Histo=Unfolding_Histo, Title=Unfolding_Histo.GetTitle(), Name=Unfolding_Histo.GetName(), Method="bayes", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="Smear" if("Smear" in Unfolding_Histo.GetName()) else "", Out_Option="histo", Fitting_Input="off")[0]
                            for ii in Sliced_1D:
                                Sliced_OutPut[f"{ii}_(Iteration_{bayes_iterations})"] = Sliced_1D[ii].Clone(f"{ii}_(Iteration_{bayes_iterations})")
                        print(f"{color.BOLD}{color.CYAN}Finished {color.GREEN}{str(Unfold_Title)}{color.END_B}{color.CYAN} Unfolding (Iteration Tests).\n{color.END}")
                        return Sliced_OutPut

##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##
                if(not Test_Bayes_Iterations):
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

                    print("".join([color.BOLD, color.CYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END_B, color.CYAN, " Unfolding Procedure.\n", color.END]))
                    return [Unfolded_Histo, Response_RooUnfold]
                        
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

def z_pT_Images_Together_For_Iteration_Test(Histogram_List_All, Default_Histo_Name, Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z", Saving_Q=False):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    All_z_pT_Canvas = Canvas_Create(Name="".join(["5D_Bayesian_Iteration_Test_Q2_y_Bin_", str(Q2_Y_Bin), "_", str(Plot_Orientation)]), Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
    All_z_pT_Canvas.SetFillColor(root_color.LGrey)
    # All_z_pT_Canvas.Draw()
    All_z_pT_Canvas_cd_1       = All_z_pT_Canvas.cd(1)
    All_z_pT_Canvas_cd_1.SetFillColor(root_color.LGrey)
    All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
    All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)
    All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
    All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
    All_z_pT_Canvas_cd_1_Upper.Divide(1, 1, 0, 0)
    All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
    All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
    All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
    All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
    All_z_pT_Canvas_cd_2       = All_z_pT_Canvas.cd(2)
    All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
    All_z_pT_Canvas_cd_2.SetFillColor(root_color.LGrey)
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
    Default_Histo_Method_Name   = Default_Histo_Name.replace("Data_Type", Method)
    for z_pT in range(0, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=int(Q2_Y_Bin))[1]+1):
        Q2_Y_Bin = Q2_Y_Bin if(str(Q2_Y_Bin) not in ["All", "0"]) else "All"
        z_pT     = z_pT     if(str(z_pT)     not in ["All", "0"]) else "All"
        Bin_Title_z_pT_Bin     = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{", "All Binned Events}" if(str(Q2_Y_Bin) in ["All", "0"]) else "".join(["Q^{2}-y Bin: ", str(Q2_Y_Bin), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT)]), "}}}"])
        if(Standard_Histogram_Title_Addition not in [""]):
            Bin_Title_z_pT_Bin = "".join(["#splitline{", str(Bin_Title_z_pT_Bin), "}{", str(Standard_Histogram_Title_Addition), "}"])
        Initial_Response_Matrix_Name = str(Default_Histo_Method_Name.replace("Q2_Y_BIN_NUM", f"Q2_y_Bin_{Q2_Y_Bin}")).replace("Z_PT_BIN_NUM", f"z_pT_Bin_{z_pT}")
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT, BINNING_METHOD=Binning_Method)):
            # print(f"{color.RED}\n{Initial_Response_Matrix_Name}{color.END}")
            continue
        else:
            if(str(z_pT) in ["All", "0"]):
                # legend = ROOT.TLegend(0.9, 0.5, 1.0, 0.9)
                legend = ROOT.TLegend(0.01, 0.01, 0.99, 0.99)
                legend.SetHeader("Number of Bayesian Iterations", "C") # option "C" allows to center the header
                legend.SetNColumns(2)
            if(str(z_pT) not in ["All", "0"]):
                cd_number_of_z_pT_all_together = z_pT
                if(Plot_Orientation in ["z_pT"]):
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(cd_number_of_z_pT_all_together)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                else:
                    cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                    if(0  ==    (cd_number_of_z_pT_all_together%number_of_cols)):
                        cd_row += -1
                    cd_col =     cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                    All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
                    All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
            
            for Iteration in range(0, 4):
                Default_Response_Matrix_Name = Initial_Response_Matrix_Name.replace("ITERATION_NUM", f"Iteration_{Iteration}")
                if(not (Default_Response_Matrix_Name in Histogram_List_All)):
                    continue
                color_of_iteration      = Iteration + 1
                if(Iteration >= 5):
                    color_of_iteration += 1
                if(Iteration >= 10):
                    color_of_iteration += 20
                Histogram_List_All[Default_Response_Matrix_Name].SetLineColor(color_of_iteration)
                Histogram_List_All[Default_Response_Matrix_Name].SetLineWidth(2)
                Histogram_List_All[Default_Response_Matrix_Name].SetLineStyle(1)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerColor(color_of_iteration)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerSize(1)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerStyle(21)
                Histogram_List_All[Default_Response_Matrix_Name].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{5D Bayes Unfold #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}}{Iteration Tests}"]))
                Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetTitle("".join(["#phi_{h}", "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetRangeUser(0, 360)
                if(str(z_pT) in ["All", "0"]):
                    legend.AddEntry(Histogram_List_All[Default_Response_Matrix_Name], f"{Iteration} Iterations", "lep")
                
                if(str(z_pT) in ["All", "0"]):
                    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower,    1, 0.15)
                    Histogram_List_All[Default_Response_Matrix_Name].Draw("H P E0 same")
                    if(Iteration == 3):
                        Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 1, 0.15)
                        Blank = Histogram_List_All[Default_Response_Matrix_Name].Clone("EMPTY")
                        Blank.SetTitle("")
                        Blank.Draw("H P E0")
                        legend.DrawClone()
                        ROOT.gPad.Update()
                        All_z_pT_Canvas.Update()
                else:
                    Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
                    Histogram_List_All[Default_Response_Matrix_Name].Draw("H P E0 same")
            
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    Save_Name = "".join(["5D_Bayesian_Iteration_Test_Q2_y_Bin_", str(Q2_Y_Bin), "_Smeared" if("Smear" in str(Default_Histo_Name)) else "", str(File_Save_Format)])
    if(Plot_Orientation in ["pT_z"]):
        Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Flipped", str(File_Save_Format)]))
    if(Saving_Q):
        if("root" in str(File_Save_Format)):
            All_z_pT_Canvas.SetName(Save_Name.replace(".root", ""))
        All_z_pT_Canvas.SaveAs(Save_Name)
        del All_z_pT_Canvas
    print("".join(["Saved: " if(Saving_Q) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    # return All_z_pT_Canvas
    



##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
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
Common_Name = "Pass_2_5D_Unfold_Test_V1_All"
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
#     print("".join([color.BOLD, "\nNot using the common file name for the Real (Experimental) Data...\n", color.END]))
# if(False):
    REAL_File_Name = Common_Name
else:
    REAL_File_Name = "Unfolding_Tests_V11_All"
    REAL_File_Name = "Pass_2_Correction_Effects_V1_5197"
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
    MC_REC_File_Name = "Unsmeared_Pass_2_5D_Unfold_Test_V1_All" if(Smearing_Options in ["no_smear"]) else "Pass_2_5D_Unfold_Test_V1_All"
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

print("".join(["\n\n", color.BOLD, "Done Loading RDataFrame files...\n", color.END]))


########################################################################################################################################################
########################################################################################################################################################
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##     Loaded Data Files      ##==========##==========##==========##==========##==========##==========##==========##==========##
##==========##==========##                            ##==========##==========##==========##==========##==========##==========##==========##==========##
########################################################################################################################################################
########################################################################################################################################################



rdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type=''),",                                                               " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=12270, MinBin=-0.5, MaxBin=12269.5]))"])
mdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=12270, MinBin=-0.5, MaxBin=12269.5]))"])
gdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='gdf'), (Data-Cut='no_cut'),",             " (Smear-Type=''),",                                                               " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=12270, MinBin=-0.5, MaxBin=12269.5]))"])
bdf_TH1D_Name = "".join(["((Histo-Group='Background_5D_Response_Matrix_1D'),", " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=12270, MinBin=-0.5, MaxBin=12269.5]))"])
mdf_TH2D_Name = "".join(["((Histo-Group='5D_Response_Matrix'),",               " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=12270, MinBin=-0.5, MaxBin=12269.5]))"])

out_print_main = mdf_TH2D_Name.replace("mdf", "DataFrame_Type")

ExREAL_1D   = rdf.Get(rdf_TH1D_Name)
MC_REC_1D   = mdf.Get(mdf_TH1D_Name)
MC_GEN_1D   = gdf.Get(gdf_TH1D_Name)
MC_BGS_1D   = mdf.Get(bdf_TH1D_Name)
Response_2D = mdf.Get(mdf_TH2D_Name)


Unfold_1D = Unfold_Function(Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, Method="RooUnfold", MC_BGS_1D=MC_BGS_1D, Test_Bayes_Iterations=True)

# print(type(Unfold_1D))
# for ii in Unfold_1D:
#     print(ii)

# for     Q2_y in Q2_xB_Bin_List:
#     for z_pT in range(0, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=int(Q2_y))[1]+1):
#         if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y, Z_PT_BIN=z_pT, BINNING_METHOD=Binning_Method)):
#             print(f"{color.RED}{z_pT}{color.END}")
#         else:
#             print(f"{color.BOLD}{z_pT}{color.END}")







# Default_Histo_Name_Test = "(MultiDim_5D_Histo)_(Test)_(SMEAR=Smear)_(Q2_y_Bin_1)_(z_pT_Bin_All)_(MultiDim_Q2_y_z_pT_phi_h)_(Iteration_0)"
# Default_Histo_Name_Test = "(MultiDim_5D_Histo)_(Data_Type)_(SMEAR=Smear)_(Q2_Y_BIN_NUM)_(Z_PT_BIN_NUM)_(MultiDim_Q2_y_z_pT_phi_h)_(ITERATION_NUM)"
# Default_Histo_Name_Test = "(MultiDim_5D_Histo)_(Data_Type)_(SMEAR='')_(Q2_Y_BIN_NUM)_(Z_PT_BIN_NUM)_(MultiDim_Q2_y_z_pT_phi_h)_(ITERATION_NUM)"

canvas, to_be_saved_count = {}, 0
Default_Histo_Name_Test = "".join(["(MultiDim_5D_Histo)_(Data_Type)_(SMEAR=", "Smear" if(Smearing_Options not in ["no_smear"]) else "''", ")_(Q2_Y_BIN_NUM)_(Z_PT_BIN_NUM)_(MultiDim_Q2_y_z_pT_phi_h)_(ITERATION_NUM)"])

print(f"{color.BGREEN}\nDefault_Histo_Name_Test = {Default_Histo_Name_Test}\n{color.END}")

for Q2_y in Q2_xB_Bin_List:
    # canvas[Q2_y] = z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z")
    # canvas[Q2_y] = z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT")
    # canvas[Q2_y] = 
    z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="RooUnfold", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q)
    # canvas[Q2_y].Draw()
    to_be_saved_count += 1


print("DONE")
    


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
    

print("".join([color.BGREEN, color_bg.YELLOW, """
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
""", color.END]))
