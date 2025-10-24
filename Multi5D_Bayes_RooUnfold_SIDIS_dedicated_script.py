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

import argparse

def parse_args():
    p = argparse.ArgumentParser(description="Multi5D_Bayes_RooUnfold_SIDIS_dedicated_script.py analysis script:\n\tMeant for JUST doing the 5D (Bayesian) Unfolding Procedure before saving outputs to a ROOT file.",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save', action='store_true', dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root', type=str, default="Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap.root",
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

    p.add_argument('-bayes-it', '--bayes_iterations', type=int,
                   help="Number of Bayesian Iterations performed while Unfolding (defaults to pre-set values in the code, but this argument allows them to be overwritten automatically)")
    
    p.add_argument('-title', '--title', type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-evgen', '--EvGen', action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut', type=float, default=0.005,
                   help="Cut made on acceptance (as the minimum acceptance before a bin is removed from unfolding - Default: 0.005)")

    # # positional Q2-y bin arguments
    # p.add_argument('bins', nargs='*', metavar='BIN',
    #                help="List of Q2-y bin indices to run. '0' means all bins.")
    p.add_argument("-b", "--bins", nargs="+", type=str,
                   help="List of Q2-y bin indices to run. Defaults to ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']")

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
    else:
        print(f"\n\n{color.Error}Wrong Smearing option for Multi5D_Slice(...){color.END}\n\n")
        return "Error"
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
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END, "\nName =", str(Name), "\n"]))
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END, "\nName =", str(Name), "\n"]))
        for Q2_y in Q2_y_Bin_List:
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
                        Output_Histos[Name_Out].GetYaxis().SetRangeUser(1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMinimumBin()) if(Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMinimumBin()) < 0) else 0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
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
    print(f"\n{color.BBLUE}Running Rebuild_Matrix_5D(...){color.END}\n")
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
    print(f"\n{color.BGREEN}Finished running Rebuild_Matrix_5D(...){color.END}\n")
    return Rebuilt_5D_Matrix

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##        Difference in Bayes Iterations Function         ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Delta_in_Iterations(Sliced_List, Histo_Name, Min_Range_of_Iterations=1, Max_Range_of_Iterations=4):
    if(f"Iteration_{Min_Range_of_Iterations}" not in Histo_Name):
        raise TypeError(f"'Iteration_{Min_Range_of_Iterations}' not in Histo_Name ({Histo_Name})... (Need to include for Delta_in_Iterations(...) function with Min_Range_of_Iterations = {Min_Range_of_Iterations})")
    else:
        for iteration in range(Min_Range_of_Iterations, Max_Range_of_Iterations):
            Histo_Name_Current = Histo_Name.replace(f"Iteration_{Min_Range_of_Iterations}", f"Iteration_{iteration}")
            Histo_Name____Next = Histo_Name.replace(f"Iteration_{Min_Range_of_Iterations}", f"Iteration_{iteration+1}")
            
            Delta_Name_Content = Histo_Name.replace(f"Iteration_{Min_Range_of_Iterations}", f"Delta_Content_{iteration+1}")
            Delta_Name___Error = Histo_Name.replace(f"Iteration_{Min_Range_of_Iterations}", f"Delta_Error_{iteration+1}")
            
            if(all(name in Sliced_List for name in [Histo_Name_Current, Histo_Name____Next])):
                Sliced_List[Delta_Name_Content] = Sliced_List[Histo_Name_Current].Clone(Delta_Name_Content)
                Sliced_List[Delta_Name___Error] = Sliced_List[Histo_Name____Next].Clone(Delta_Name___Error)
                
                Sliced_List[Delta_Name_Content].GetYaxis().SetTitle("Diff in Bin Content")
                Sliced_List[Delta_Name___Error].GetYaxis().SetTitle("Diff in Bin Error")
                
                Sliced_List[Delta_Name_Content].Add(Sliced_List[Histo_Name_Current], -1)
                
                for x_bin in range(1, Sliced_List[Delta_Name___Error].GetNbinsX() + 1):
                    error_diff = Sliced_List[Histo_Name____Next].GetBinError(x_bin) - Sliced_List[Histo_Name_Current].GetBinError(x_bin)
                    Sliced_List[Delta_Name___Error].SetBinContent(x_bin, error_diff)
                    Sliced_List[Delta_Name___Error].SetBinError(x_bin,   0)
            else:
                print(f"""
{color.Error}Missing:{color.END}
Histo_Name_Current = {Histo_Name_Current}")
Histo_Name____Next = {Histo_Name____Next}
{color.BOLD}Content of 'Sliced_List':{color.END}""")
                for ii in Sliced_List:
                    print(f"\t{ii}")
                raise TypeError("Missing either 'Histo_Name_Current' or 'Histo_Name____Next' from 'Sliced_List'")
                
        return Sliced_List
    
################################################################################################################################################################################################################################################
##==========##==========##        Difference in Bayes Iterations Function         ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
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
    Sliced_OutPut = {}
##############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method(s): "Test"         #####=====#####=====#####=====#####
##############################################################################################################
    if("Test" in str(Method)):
        print(f"{color.Error}Starting {color.UNDERLINE}{color.BLUE}TEST{color.END_e} Procedure (returning all sliced 1D histos)...{color.END}")
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
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.GREEN}RooUnfold{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print(f"""\t{color.BOLD}Unfolding Histogram:{color.END}\n\t{str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")}""")
        
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
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, "".join([str(Response_2D_Input.GetName()).replace("_Flipped", ""), "_RooUnfoldResponse_Object"]), Response_2D_Input_Title)
                del Response_2D_Input
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
                        print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                        
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
                        # Bin_Acceptance.Sumw2()
                        Bin_Acceptance.Divide(MC_GEN_1D)
                        print(f"{color.BBLUE}Performing Iteration Test of 5D Bayes Unfolding...{color.END}")
                        Min_Range_of_Iterations = 1
                        Max_Range_of_Iterations = 3
                        for bayes_iterations in range(Min_Range_of_Iterations, Max_Range_of_Iterations + 1):
                            print(f"{color.BOLD}Running with '{bayes_iterations}' iteration(s){color.END}")
                            Time_Start_Running = datetime.now()
                            sys.stdout.flush()
                            Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)
                            # Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)
                            # Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, 1)
                            # Unfolding_Histo.SetVerbose(1)
                            Unfolded_Histo  = Unfolding_Histo.Hunfold()
                            for bin_rec in range(0, MC_REC_1D.GetNbinsX() + 1, 1):
                                if((MC_REC_1D.GetBinContent(bin_rec) == 0) or (Bin_Acceptance.GetBinContent(bin_rec) < 0.02)):
                                    Unfolded_Histo.SetBinError(bin_rec,          0)
                                    Unfolded_Histo.SetBinContent(bin_rec,        0)
                            timer.time_elapsed()
                            Sliced_1D = Multi5D_Slice(Histo=Unfolded_Histo, Title=Unfolding_Histo.GetTitle(), Name=Unfolding_Histo.GetName(), Method="bayes", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="Smear" if(any(smear_find in Unfolding_Histo.GetName() for smear_find in ["'smear'", "'Smear'", "smeared"])) else "", Out_Option="histo", Fitting_Input="off")[0]
                            del Unfolding_Histo
                            del Unfolded_Histo
                            for ii in Sliced_1D:
                                Sliced_1D[ii].GetYaxis().SetTitle("")
                                Sliced_OutPut[f"{ii}_(Iteration_{bayes_iterations})"] = Sliced_1D[ii].Clone(f"{ii}_(Iteration_{bayes_iterations})")
                            del Sliced_1D
                        print(f"{color.BOLD}{color.CYAN}Finished {color.GREEN}{str(Unfold_Title)}{color.END_B}{color.CYAN} Unfolding (Iteration Tests).\n{color.END}")
                        sys.stdout.flush()
                        Sliced_OutPut_With_Diff = Sliced_OutPut.copy()
                        for ii in Sliced_OutPut:
                            # print(ii)
                            if(f"Iteration_{Min_Range_of_Iterations}" in str(ii)):
                                Sliced_OutPut_With_Diff = Delta_in_Iterations(Sliced_List=Sliced_OutPut_With_Diff, Histo_Name=ii, Min_Range_of_Iterations=Min_Range_of_Iterations, Max_Range_of_Iterations=Max_Range_of_Iterations)
                                # for iteration in range(Min_Range_of_Iterations, Max_Range_of_Iterations):
                                #     Delta_Name_Content = ii.replace(f"Iteration_{Min_Range_of_Iterations}", f"Delta_Content_{iteration+1}")
                                #     Delta_Name___Error = ii.replace(f"Iteration_{Min_Range_of_Iterations}", f"Delta_Error_{iteration+1}")
                                #     if(str(Delta_Name_Content) in Sliced_OutPut_With_Diff):
                                #         print(f"{color.BGREEN}\t{Delta_Name_Content}{color.END}")
                                #     else:
                                #         print(f"{color.Error}\tMISSING: {Delta_Name_Content}{color.END}")
                                #     if(str(Delta_Name___Error) in Sliced_OutPut_With_Diff):
                                #         print(f"{color.BGREEN}\t{Delta_Name___Error}{color.END}")
                                #     else:
                                #         print(f"{color.Error}\tMISSING: {Delta_Name___Error}{color.END}")
                        return Sliced_OutPut_With_Diff

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

                    print(f"{color.BCYAN}Finished {color.GREEN}{Unfold_Title}{color.END_B}{color.CYAN} Unfolding Procedure.\n{color.END}")
                    return [Unfolded_Histo, Response_RooUnfold]
                        
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

def z_pT_Images_Together_For_Iteration_Test(Histogram_List_All, Default_Histo_Name, Method="rdf", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z", Saving_Q=False, Compare_Type="Default"):
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
                legend.SetHeader("Number of Bayesian Iterations" if(str(Compare_Type) in ["Default", "Overlap"]) else "".join(["Content" if(str(Compare_Type) in ["Diff", "Content"]) else "Error", " Difference After Number of Iterations"]), "C") # option "C" allows to center the header
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
            
            Min_Range_of_Iterations = 1
            Max_Range_of_Iterations = 3
            if(str(Compare_Type) not in ["Default", "Overlap"]):
                Max_Range_of_Iterations += -1
            for Iteration in range(Min_Range_of_Iterations, Max_Range_of_Iterations + 1):
                Default_Response_Matrix_Name = Initial_Response_Matrix_Name.replace("ITERATION_NUM", f"Iteration_{Iteration}" if(str(Compare_Type) in ["Default", "Overlap"]) else f"Delta_Content_{Iteration+1}" if(str(Compare_Type) in ["Diff", "Content"]) else f"Delta_Error_{Iteration+1}")
                if(not (Default_Response_Matrix_Name in Histogram_List_All)):
                    print(f"{color.Error}Missing: {color.END_R}{Default_Response_Matrix_Name}{color.END}")
                    continue
                color_of_iteration      = Iteration + 1
                if(color_of_iteration  >= 5):
                    color_of_iteration += 1
                if(color_of_iteration  >= 10):
                    color_of_iteration += 20
                Histogram_List_All[Default_Response_Matrix_Name].SetLineColor(color_of_iteration)
                Histogram_List_All[Default_Response_Matrix_Name].SetLineWidth(2)
                Histogram_List_All[Default_Response_Matrix_Name].SetLineStyle(1)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerColor(color_of_iteration)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerSize(1)
                Histogram_List_All[Default_Response_Matrix_Name].SetMarkerStyle(21)
                Histogram_List_All[Default_Response_Matrix_Name].SetTitle("".join(["#splitline{#splitline{#scale[1.5]{5D Bayes Unfold #phi_{h}}}{#scale[1.15]{", str(Bin_Title_z_pT_Bin), "}}}{", "Iteration Tests" if(str(Compare_Type) in ["Default", "Overlap"]) else "".join(["Content" if(str(Compare_Type) in ["Diff", "Content"]) else "Error", " Diff between Iterations"]), "}"]))
                Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetTitle("".join(["#phi_{h}", "" if("Smear" not in str(Default_Histo_Name)) else " (Smeared)"]))
                Histogram_List_All[Default_Response_Matrix_Name].GetXaxis().SetRangeUser(0, 360)
                if(str(Compare_Type) in ["Default", "Overlap"]):
                    Histogram_List_All[Default_Response_Matrix_Name].GetYaxis().SetTitle("")
                    if(str(z_pT) in ["All", "0"]):
                        legend.AddEntry(Histogram_List_All[Default_Response_Matrix_Name], f"{Iteration} Iterations", "lep")
                elif(str(z_pT) in ["All", "0"]):
                    legend.AddEntry(Histogram_List_All[Default_Response_Matrix_Name], f"Diff between Iterations {Iteration}+{Iteration+1}", "lep")
                
                if(str(z_pT) in ["All", "0"]):
                    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower,     1, 0.15)
                    Histogram_List_All[Default_Response_Matrix_Name].Draw("H P E0 same")
                    if(Iteration == Max_Range_of_Iterations):
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
    if(str(Compare_Type)       in ["Diff", "Content"]):
        Save_Name = Save_Name.replace("_Iteration_Test_", "_Diff_In_Iteration_Content_")
    elif(str(Compare_Type) not in ["Default", "Overlap"]):
        Save_Name = Save_Name.replace("_Iteration_Test_", "_Diff_In_Iteration_Error_")

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


# for ii in mdf.GetListOfKeys():
#     conditions = []
#     conditions.append("MultiDim_z_pT_Bin_Y_bin_phi_t" in str(ii.GetName()))
#     conditions.append("Background"                not in str(ii.GetName()))
#     conditions.append("cut_Complete_SIDIS"            in str(ii.GetName()))
#     if(all(conditions)):
#         print(f"{color.BGREEN}{str(ii.GetName())}{color.END}")
# #     else:
# #         print(f"{color.ERROR}{ii}{color.END}")

# for Q2_y_bin in Q2_y_Bin_List:
#     mdf_TH2D_Name = "".join(["((Histo-Group='Response_Matrix_Normal'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=", str(Q2_y_bin), ", z-PT-Bin=All]), (Var-D1='MultiDim_z_pT_Bin_Y_bin_phi_t'-[NumBins=915, MinBin=-1.5, MaxBin=913.5]), (Var-D2='", "z_pT_Bin_Y_bin_smeared" if(Smearing_Options == "smear") else "z_pT_Bin_Y_bin", "'-[NumBins=38, MinBin=-0.5, MaxBin=37.5]))"])
#     Response_2D = mdf.Get(mdf_TH2D_Name)
#     Response_2D.GetXaxis().SetTitleOffset(1.2)
#     Response_2D.GetYaxis().SetTitleOffset(1.4)
#     Line_1 = "".join(["#scale[1.5]{", "(Smeared) " if(Smearing_Options == "smear") else "", "Response Matrix of 3D Kinematic Bins (z+P_{T}+#phi_{h})}"])
#     Line_2 = "".join(["#scale[1.35]{#color[", str(root_color.Blue), "]{", str(Pass_Version), "} #topbar Q^{2}-y Bin ", str(Q2_y_bin), "}"])
#     Response_2D.SetTitle("".join(["#splitline{", str(Line_1), "}{", str(Line_2), "}"]))
#     del Line_1
#     del Line_2
#     # Create a canvas
#     canvas = ROOT.TCanvas(f"canvas_Bin_{Q2_y_bin}", f"3D Response Histogram Canvas Bin {Q2_y_bin}", 1300, 725)
#     canvas.SetRightMargin(0.15)  # Increase if color palette is clipped
#     canvas.SetLeftMargin(0.15)   # Increase for Y-axis label and title
#     canvas.SetBottomMargin(0.15) # Increase for X-axis label and title
#     canvas.SetTopMargin(0.175)   # Increase top margin to give more space for the title

#     ROOT.gStyle.SetOptStat('i')  # Display overflow, underflow, integral, etc.
#     ROOT.gStyle.SetStatX(0.900)   # Position of the top right corner of the stat box
#     ROOT.gStyle.SetStatY(0.875)
#     ROOT.gStyle.SetStatW(0.150)   # Width of the stat box
#     ROOT.gStyle.SetStatH(0.200)   # Height of the stat box
#     Response_2D.Draw("colz")
#     canvas.SetLogz(True)  # Set logarithmic scale on the z-axis if needed
#     canvas.Update()
#     Save_Name = "".join([f"Response_Matrix_Multi_3D_Q2_y_Bin_{Q2_y_bin}_Histogram", ".png" if(str(Smearing_Options) not in ["smear"]) else "_Smeared.png"])
#     canvas.SaveAs(Save_Name)
#     del canvas
#     del Response_2D



rdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='rdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type=''),",                                                               " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=11816, MinBin=-0.5, MaxBin=11815.5]))"])
mdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=11816, MinBin=-0.5, MaxBin=11815.5]))"])
gdf_TH1D_Name = "".join(["((Histo-Group='5D_Response_Matrix_1D'),",            " (Data-Type='gdf'), (Data-Cut='no_cut'),",             " (Smear-Type=''),",                                                               " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=11816, MinBin=-0.5, MaxBin=11815.5]))"])
bdf_TH1D_Name = "".join(["((Histo-Group='Background_5D_Response_Matrix_1D'),", " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=11816, MinBin=-0.5, MaxBin=11815.5]))"])
mdf_TH2D_Name = "".join(["((Histo-Group='5D_Response_Matrix'),",               " (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'),", " (Smear-Type='smear')," if(Smearing_Options == "smear") else " (Smear-Type=''),", " (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=11816, MinBin=-0.5, MaxBin=11815.5]))"])



# out_print_main = mdf_TH2D_Name.replace("mdf", "DataFrame_Type")

ExREAL_1D   = rdf.Get(rdf_TH1D_Name)
MC_REC_1D   = mdf.Get(mdf_TH1D_Name)
MC_GEN_1D   = gdf.Get(gdf_TH1D_Name)
MC_BGS_1D   = mdf.Get(bdf_TH1D_Name)

# # For Simulated Closure Test #
# ExREAL_1D   = MC_REC_1D.Clone(str(rdf_TH1D_Name))
# ExREAL_1D.Add(MC_BGS_1D)
# # For Simulated Closure Test #

# Response_2D = mdf.Get(mdf_TH2D_Name)
Num_5D_Increments_Used_to_Slice = 422
Histo_List = {}
for ii in mdf.GetListOfKeys():
    if(mdf_TH2D_Name in str(ii.GetName())):
        print(f"Grabbing: {ii.GetName()}")
        Histo_List[ii.GetName()] = mdf.Get(ii.GetName())
Response_2D = Rebuild_Matrix_5D(List_of_Sliced_Histos=Histo_List, Standard_Name=mdf_TH2D_Name, Increment=Num_5D_Increments_Used_to_Slice)
del Histo_List

timer.time_elapsed()

# Response_2D.GetXaxis().SetTitleOffset(1.2)
# Response_2D.GetYaxis().SetTitleOffset(1.4)
# Line_1 = "".join(["#scale[1.5]{", "(Smeared) " if(Smearing_Options == "smear") else "", "Response Matrix of 5D Kinematic Bins (Q^{2}+y+z+P_{T}+#phi_{h})}"])
# Line_2 = "".join(["#scale[1.35]{#color[", str(root_color.Blue), "]{", str(Pass_Version), "} #topbar All Q^{2}-y-z-P_{T} Bins #topbar Total Number of Bins: 11816}"])
# Response_2D.SetTitle("".join(["#splitline{", str(Line_1), "}{", str(Line_2), "}"]))
# del Line_1
# del Line_2
# # Create a canvas
# canvas = ROOT.TCanvas("canvas", "Response Histogram Canvas", 1300, 725)
# canvas.SetRightMargin(0.15)  # Increase if color palette is clipped
# canvas.SetLeftMargin(0.15)   # Increase for Y-axis label and title
# canvas.SetBottomMargin(0.10) # Increase for X-axis label and title
# canvas.SetTopMargin(0.25)   # Increase top margin to give more space for the title

# ROOT.gStyle.SetOptStat('i')  # Display overflow, underflow, integral, etc.
# ROOT.gStyle.SetStatX(0.90)   # Position of the top right corner of the stat box
# ROOT.gStyle.SetStatY(0.80)
# ROOT.gStyle.SetStatW(0.15)   # Width of the stat box
# ROOT.gStyle.SetStatH(0.20)   # Height of the stat box
# Response_2D.Draw("colz")
# canvas.SetLogz(True)  # Set logarithmic scale on the z-axis if needed
# canvas.Update()
# Save_Name = "".join(["Response_Matrix_Multi_5D_Histogram", ".png" if(str(Smearing_Options) not in ["smear"]) else "_Smeared.png"])
# canvas.SaveAs(Save_Name)
# del canvas
# # del Response_2D


# No longer need the root files #
del rdf
del mdf
del gdf
# No longer need the root files #


# Unfold_1D = Unfold_Function(Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, Method="RooUnfold", MC_BGS_1D=MC_BGS_1D, Test_Bayes_Iterations=True)
Unfold_1D = Unfold_Function(Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, Method="Test",      MC_BGS_1D=MC_BGS_1D, Test_Bayes_Iterations=True)

timer.time_elapsed()

# print(type(Unfold_1D))
print("Content of Unfold_1D:")

for ii in Unfold_1D:
    print(f"\t{ii}")

sys.stdout.flush()

# for     Q2_y in Q2_y_Bin_List:
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

for Q2_y in Q2_y_Bin_List:
    # canvas[Q2_y] = z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test", Q2_Y_Bin=1, Multi_Dim_Option="Off", Plot_Orientation="pT_z")
    # canvas[Q2_y] = z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT")
    
    # # z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="bayes", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q)
    # z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="bayes", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Default")
    # z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="bayes", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Diff")
    # z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="bayes", Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Error")
    
    # z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test",  Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q)
    z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test",  Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Default")
    z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test",  Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Diff")
    z_pT_Images_Together_For_Iteration_Test(Histogram_List_All=Unfold_1D, Default_Histo_Name=Default_Histo_Name_Test, Method="Test",  Q2_Y_Bin=int(Q2_y), Multi_Dim_Option="Off", Plot_Orientation="z_pT", Saving_Q=Saving_Q, Compare_Type="Error")
    

    # canvas[Q2_y].Draw()
    to_be_saved_count += 3


print("DONE")
    
timer.stop(count_label="Images", count_value=to_be_saved_count)


print(f"""{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

