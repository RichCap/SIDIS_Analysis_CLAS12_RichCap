#!/usr/bin/env python3

import ROOT
import sys
import argparse
import traceback
# from pathlib import Path
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import RuntimeTimer, Canvas_Create, color, variable_Title_name, Get_Num_of_z_pT_Rows_and_Columns, Get_Num_of_z_pT_Bins_w_Migrations, skip_condition_z_pT_bins, Draw_Canvas, Draw_Q2_Y_Bins, Draw_z_pT_Bins_With_Migration
# from ExtraAnalysisCodeValues import New_z_pT_and_MultiDim_Binning_Code
from Binning_Dictionaries             import Bin_Converter_4D_to_2D #, Full_Bin_Definition_Array
sys.path.remove(script_dir)
del script_dir

# Turns off the canvases when running in the command line
ROOT.gROOT.SetBatch(1)

Name_of_Script = "View_2D_Histos_From_Response_Matrix_Creation.py"
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"{Name_of_Script}\n\nMain executable that merges two ROOT files (with opposite cut meanings) into an in-memory file and runs the 1D comparison plots.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-V', '--var',
                        default="pip",
                        help="Variable to project and plot (el, pip, Q2, z, MM, rho0, etc.).\n")
    parser.add_argument('-ff', '--File_Save_Format',
                        default=".pdf",
                        help="Output file format for saved canvases.\n")
    parser.add_argument('-n', '--name',
                        default="",
                        help="Extra suffix added to output filenames.\n")
    parser.add_argument('-f1', '--file1',
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_without_rho0_with_phi_t_Final_Analysis_Iterations_I0_All.root",
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Default_rho_Final_Analysis_Iterations_I0_All.root",
                        # default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_V2Sbatch_Default_rho_Final_Analysis_Iterations_I0_05_11_2026.root",
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_VSbatch_Exclusive_rho_Final_Analysis_Iterations_I0_05_11_2026.root",
                        help="Path to first ROOT file (e.g. the reject-cut version).\n")
    parser.add_argument('-f2', '--file2',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Required_rho0_with_Only_2D_with_phi_t_Final_Analysis_Iterations_I0_All.root",
                        help="Path to second ROOT file (e.g. the accept-cut version).\n")
    parser.add_argument('-f3', '--file3',
                        default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Required_rho0_with_Only_2D_with_phi_t_Final_Analysis_Iterations_I0_lundvpk_Batch.root",
                        help="Path to third ROOT file (e.g. for the lundvpk files only).\n")
    parser.add_argument('-usf', '--use_same_file',
                        action='store_true',
                        help="If provided, code will default to just using histograms from '--file1'.\n")
    parser.add_argument('-d', '--Data_Compare',
                        type=str,
                        default="mdf",
                        choices=["rdf", "mdf", "gdf"],
                        help="Choice of Main data set to compare.\n")
    parser.add_argument('-q2y', '--Q2_y_Bin_Select',
                        type=int,
                        help=f"Use to select a Q2-y Bin for the 'together' z-pT bin images.\n{color.Error}NOTE: This argument is NOT the one used by the individual bin images.{color.END}\n")
    parser.add_argument('-q2yI', '--Q2_y_Bin_Individual',
                        type=str,
                        choices=["All", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
                        help=f"Use to select a Q2-y Bin for the individual bin images.\n{color.Error}NOTE: Providing this argument will cause the code to produce an image for only one selected bin.{color.END}\n")
    parser.add_argument('-zpt', '--z_pT_Bin_Individual',
                        type=str,
                        help=f"Use to select a z-pT Bin for the individual bin images.\n{color.RED}NOTE: This argument works with the '--Q2_y_Bin_Individual' argument to produce individual images.\n{color.END}Providing this argument can cause the code to produce an image for only one selected bin if the input is 'All' (otherwise, you must also specify a value for '--Q2_y_Bin_Individual' to allow the code to work).\n{color.Error}WARNING: This argument does not ensure the combined Q2-y-z-pT bin selected actually exists — user must verify their inputs themselves to avoid crashes.{color.END}\n")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Print extra runtime information.\n")
    parser.add_argument('-dr', '--dry_run',
                        action='store_true',
                        help="Do not actually save any output files.\n")
    return parser.parse_args()


def Create_Combined_Memory_File(file_path_1, file_path_2, var_restrict=None, file_path_3=None):
    file1 = ROOT.TFile.Open(file_path_1, "READ")
    if((file_path_2 is None) or (str(file_path_2) in ["None"])):
        return file1
    file2 = ROOT.TFile.Open(file_path_2, "READ")
    if((file_path_3 is not None) and (str(file_path_3) not in ["None"])):
        print(f"\n{color.BOLD}Combining the following files:{color.END}\n\t{file_path_1}\n\t\t(Used for no rho/clasdis)\n\t{file_path_2}\n\t\t(Used for rho0)\n\t{file_path_3}\n\t\t(Used for new rho0 — lundvpk)\n")
    else:
        print(f"\n{color.BOLD}Combining the following files:{color.END}\n\t{file_path_1}\n\t\t(Used for no rho/clasdis)\n\t{file_path_2}\n\t\t(Used for rho0)\n")
    combined = ROOT.TMemFile("combined_in_memory", "CREATE")
    for key in file1.GetListOfKeys():
        hname = key.GetName()
        if(var_restrict is not None):
            if(any(need_for_2D           in hname.replace("_smeared", "") for need_for_2D in ["(Q2_y_z_pT_Bin_All)_(Q2)_(y)", "(Q2_y_z_pT_Bin_All)_(z)_(pT)"])):
                pass
            elif(f"({var_restrict})" not in hname.replace("_smeared", "")):
                continue
        if(("(lundrho)" not in hname) and ("(lundvpk)" not in hname)):
            hist = key.ReadObj().Clone()
            if(hist):
                hist.SetDirectory(combined)
                hist.Write()
    for key in file2.GetListOfKeys():
        hname = key.GetName()
        if(var_restrict is not None):
            if(f"({var_restrict})" not in hname.replace("_smeared", "")):
                continue
        if("(lundrho)" in hname):
            hist = key.ReadObj().Clone()
            if(hist):
                hist.SetDirectory(combined)
                hist.Write()
    if((file_path_3 is not None) and (str(file_path_3) not in ["None"])):
        file3 = ROOT.TFile.Open(file_path_3, "READ")
        for key in file3.GetListOfKeys():
            hname = key.GetName()
            if(var_restrict is not None):
                if(f"({var_restrict})" not in hname.replace("_smeared", "")):
                    continue
            if("(lundvpk)" in hname):
                hist = key.ReadObj().Clone()
                if(hist):
                    hist.SetDirectory(combined)
                    hist.Write()
        file3.Close()
    file1.Close()
    file2.Close()
    combined.cd()
    print(f"{color.BOLD}Returning combined file...{color.END}\n")
    return combined
        
def lund_norm(hh, Normalize_Q):
    if(Normalize_Q in ["rhoscale"]):
        # if("(lundrho)" in str(hh.GetName())):
        #     # The numbers below were taken on 5/4/2026
        #     # They represent all of the clasdis generated SIDIS events and all the rho0 (Harut's) events with the kinematics between the ranges of:
        #     #     xB: 0.08 - 0.68
        #     #     Q2: 0.90 - 8.50 (cuts/counts were made using the already created histograms — not event-level cuts)
        #     # Harut's files are scaled so that they will make up 20% of the total number of SIDIS events generated by clasdis (i.e., without rho0 parents)
        #     Num_clasdis_gdf_sidis = 1.181695e+10
        #     Num_lundrho_gdf       = 9914785
        #     hh.Scale((Num_clasdis_gdf_sidis*0.2)/Num_lundrho_gdf)
        #     return hh
        # elif("(lundvpk)" in str(hh.GetName())):
        #     # The numbers below were taken on 5/8/2026
        #     # They represent all of the clasdis generated SIDIS events and all the (new) rho0 (Harut's) events with the kinematics between the ranges of:
        #     #     xB: 0.08 - 0.68
        #     #     Q2: 0.90 - 8.50 (cuts/counts were made using the already created histograms — not event-level cuts)
        #     # Harut's files are scaled so that they will make up 20% of the total number of SIDIS events generated by clasdis (i.e., without rho0 parents)
        #     Num_clasdis_gdf_sidis = 1.181695e+10
        #     Num_lundvpk_gdf       = 9985114
        #     hh.Scale((Num_clasdis_gdf_sidis*0.2)/Num_lundvpk_gdf)
        #     return hh
        # These newer numbers were taken from the fixed plots where `exclusive_rho!=1` for clasdis and `exclusive_rho==1` for Harut's files
        Num_clasdis_gdf_sidis = 1.17679e+10
        Num_lundrho_gdf       = 1.998e+07
        hh.Scale((Num_clasdis_gdf_sidis*0.2)/Num_lundrho_gdf)
    return hh


def HistoName_Return(df_in, Return_Name_or_Histo="Name", data="mdf", cut="cut_Complete_SIDIS_Exclusive_rho", smear="smear", Var_X="el_smeared", Var_Y="elPhi_smeared", lundrho="", Weighed="_(Weighed)"):
    if((data not in ["mdf"]) or any(any(no_smear_var in vars for vars in [Var_X, Var_Y]) for no_smear_var in ["rho0", "Par_PID_pip", "pim_present"])):
        smear = "''" # Do not smear
        Var_X = Var_X.replace("_smeared", "")
        Var_Y = Var_Y.replace("_smeared", "")
    elif(smear == "smear"):
        if("_smeared" not in str(Var_X)):
            Var_X = f"{Var_X}_smeared"
        if("_smeared" not in str(Var_Y)):
            Var_Y = f"{Var_Y}_smeared"
    name_to_find = f"(Normal_2D)_({data})_({cut})_(SMEAR={smear})_(Q2_y_z_pT_Bin_All)_({Var_X})_({Var_Y})"
    if(lundrho not in [False, "", "False", "lundvpk"]):
        name_to_find = f"{name_to_find}_(lundrho)"
    elif(lundrho not in [False, "", "False", "lundrho"]):
        name_to_find = f"{name_to_find}_(lundvpk)"
    if(Weighed not in ['']):
        name_to_find = f"{name_to_find}{Weighed}" if("_(" in Weighed) else f"{name_to_find}_({Weighed})"
    if(name_to_find not in df_in.GetListOfKeys()):
        print(f"{color.Error}ERROR IN 'HistoName_Return'...\n{color.END_R}The file is missing: {color.BBLUE}{name_to_find}{color.END}\n")
        return None
    else:
        return df_in.Get(name_to_find) if(Return_Name_or_Histo not in ["Name"]) else name_to_find
    
def Slice_Histos_for_Plotting(Histo3D, Var_Plot="2D", Q2y_Bin=0, zpT_Bin=0):
    if(Histo3D is None):
        return Histo3D
    HistoName  = Histo3D.GetName()
    Projection = "xy" if(Var_Plot == "2D") else "x" if(f"(Q2_y_z_pT_Bin_All)_({Var_Plot.replace('_smeared', '')})" in HistoName.replace("_smeared", "")) else "y"
    HistoName  = f"From_{HistoName}"
    if(str(Q2y_Bin) in ["All", "0"]):
        HistoName_Sliced = HistoName.replace("(Q2_y_z_pT_Bin_All)", "(Q2_y_Bin_All)_(z_pT_Bin_All)")
        Histo2D = Histo3D.Clone(HistoName_Sliced)
        Histo2D = Histo2D.Project3D(Projection)
        Histo2D.SetName(HistoName_Sliced) # In case the `Projection` string got added to the object's name
        return Histo2D
    elif(str(zpT_Bin) in ["All", "0"]):
        HistoName_Sliced = HistoName.replace("(Q2_y_z_pT_Bin_All)", f"(Q2_y_Bin_{Q2y_Bin})_(z_pT_Bin_All)")
        Histo2D = Histo3D.Clone(HistoName_Sliced)
        if(f"Q2_y_bin_{Q2y_Bin}_z_pT_bin_1" not in Bin_Converter_4D_to_2D):
            print(f"{color.Error}ERROR: Cannot find {color.UNDERLINE}'Q2_y_bin_{Q2y_Bin}_z_pT_bin_1'{color.END_e} in 'Bin_Converter_4D_to_2D'{color.END}\n")
            return None
        Min_Bin_Range_4D = Bin_Converter_4D_to_2D[f"Q2_y_bin_{Q2y_Bin}_z_pT_bin_1"]
        Max_Bin_Range_4D = (Bin_Converter_4D_to_2D[f"Q2_y_bin_{Q2y_Bin+1}_z_pT_bin_1"] - 1) if(f"Q2_y_bin_{Q2y_Bin+1}_z_pT_bin_1" in Bin_Converter_4D_to_2D) else Histo2D.GetZaxis().GetXmax()
        Histo2D.GetZaxis().SetRangeUser(Min_Bin_Range_4D, Max_Bin_Range_4D)
        Histo2D = Histo2D.Project3D(Projection)
        Histo2D.SetName(HistoName_Sliced) # In case the `Projection` string got added to the object's name
        return Histo2D
    else:
        Kinematic_4D_Bin = f"Q2_y_bin_{Q2y_Bin}_z_pT_bin_{zpT_Bin}"
        if(Kinematic_4D_Bin not in Bin_Converter_4D_to_2D):
            print(f"{color.Error}ERROR: Cannot find {color.UNDERLINE}'{Kinematic_4D_Bin}'{color.END_e} in 'Bin_Converter_4D_to_2D'{color.END}\n")
            return None
        HistoName_Sliced = HistoName.replace("(Q2_y_z_pT_Bin_All)", f"(Q2_y_Bin_{Q2y_Bin})_(z_pT_Bin_{zpT_Bin})")
        Histo2D = Histo3D.Clone(HistoName_Sliced)
        Bin_4D = Bin_Converter_4D_to_2D[Kinematic_4D_Bin]
        Bin_Range_4D = Histo2D.GetZaxis().FindBin(Bin_4D)
        Histo2D.GetZaxis().SetRange(Bin_Range_4D, Bin_Range_4D)
        Histo2D = Histo2D.Project3D(Projection)
        Histo2D.SetName(HistoName_Sliced) # In case the `Projection` string got added to the object's name
        return Histo2D

def Return_Match_Vars(Input_Var="el", Input_Var_2D=None):
    X_Var, Y_Var = None, None
    Input_Var = Input_Var.replace("_smeared", "")
    if(Input_Var_2D is not None):
        Input_Var_2D = Input_Var_2D.replace("_smeared", "")
    if(Input_Var in ["el", "pip", "rho0"]):
        X_Var = Input_Var
        Y_Var = f"{Input_Var}th" if(Input_Var_2D not in [f"{Input_Var}Phi"]) else f"{Input_Var}Phi"
        return X_Var, Y_Var
    if(Input_Var in ["elPhi", "pipPhi", "rho0Phi"]):
        X_Var = Input_Var.replace("Phi", "") if(Input_Var_2D in ["el", "pip", "rho0", None]) else Input_Var.replace("Phi", "th")
        Y_Var = Input_Var
        return X_Var, Y_Var
    if(Input_Var in ["elth", "pipth", "rho0th"]):
        X_Var = Input_Var.replace("th", "")  if(Input_Var_2D in ["el", "pip", "rho0", None]) else Input_Var
        Y_Var = Input_Var                    if(Input_Var_2D in ["el", "pip", "rho0", None]) else Input_Var.replace("th", "Phi")
        return X_Var, Y_Var
    if(Input_Var in ["Q2", "y", "xB"]):
        X_Var = "Q2"
        Y_Var = "y" if("xB" not in [Input_Var, Input_Var_2D]) else "xB"
        return X_Var, Y_Var
    if(Input_Var in ["z", "pT"]):
        return "z", "pT"
    if(Input_Var in ["MM", "W"]):
        return "MM", "W"
    if(Input_Var in ["phi_t"]):
        return "phi_t", "exclusive_rho"
    if(Input_Var in ["rho0_parent"]):
        return "rho0_parent", "Par_PID_pip"
    if(Input_Var in ["Par_PID_pip", "pim_present"]):
        return "Par_PID_pip", "pim_present"
    if(Input_Var in ["z1_plus_z2", "exclusive_rho"]):
        return "z1_plus_z2", "exclusive_rho"
    return X_Var, Y_Var

color_mapper  = {"1": ROOT.kRed, "2": ROOT.kBlue, "3": ROOT.kMagenta, "4": ROOT.kGreen, "5": ROOT.kOrange+3, "6": ROOT.kAzure+10, "7": ROOT.kOrange}
def find_color(index_num):
    if(str(index_num) not in color_mapper):
        for find_extra in range(1, 4, 1):
            if(str(int(index_num)-(7*find_extra)) in color_mapper):
                return color_mapper[str(int(index_num)-(7*find_extra))] - find_extra
            else:
                continue
        print(f"{color.Error}WARNING: Returning a color completely outside the 'color_mapper'{color.END} (index was {index_num})\n")
        return ROOT.kBlack
    else:
        return color_mapper[str(index_num)]
    return ROOT.kRed

def legend_naming(names):
    source  = "Reconstructed MC" if("mdf" in str(names)) else "Generated MC" if("gdf" in str(names)) else "Experimental Data" if("rdf" in str(names)) else ""
    source2 = ""
    if("MC" in source):
        source2 = "#scale[0.8]{#rho^{0} Parent (Harut's New Files)}" if("lundvpk" in names) else "#rho^{0} Parent (Harut's Files)" if("lundrho" in names) else "clasdis SIDIS"
    return f"#splitline{{#scale[0.85]{{{source}}}}}{{#scale[0.65]{{{source2}}}}}"

def Kinematic_1D_Compare_in_z_pT_Images_Together(rdf_in, args, Q2_Y_Bin_Range=range(1,18), Data_Compare=["mdf"], Cut_Compare=["cut_Complete_SIDIS_Exclusive_rho"], Smear_Compare=["smear"], Weighed_Compare=[""], lundrho_Compare=["", "lundrho", "lundvpk"], Plot_Var="el", Plot_Orientation="z_pT", Draw_Type="rhoscale"):
    Plot_Title   = variable_Title_name(Plot_Var) # Automatically adds the 'smearing' or 'gen' title as appropriate
    X_Var, Y_Var = Return_Match_Vars(Input_Var=Plot_Var, Input_Var_2D=None)
    All_z_pT_Canvas = {}
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
        All_z_pT_Canvas[Save_Name] = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800*2), Size_Y=int(1500*2), cd_Space=0.01)
        All_z_pT_Canvas[Save_Name].SetFillColor(ROOT.kGray)
        if(args.verbose):
            print(f"{color.BBLUE}Creating TCanvas: {color.END_B}{Save_Name}{color.BBLUE}...{color.END}")
        All_z_pT_Canvas_cd_1 = All_z_pT_Canvas[Save_Name].cd(1)
        All_z_pT_Canvas_cd_1.SetFillColor(ROOT.kGray)
        All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
        All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)
        
        All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
        All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
        All_z_pT_Canvas_cd_1_Upper.Divide(1, 2, 0.001, 0.001)
        
        All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
        All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
        All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
        All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
        
        All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
        All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
        All_z_pT_Canvas_cd_2.SetFillColor(ROOT.kGray)
        
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        if((Plot_Orientation in ["z_pT"])):
            All_z_pT_Canvas_cd_2.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
        else:
            All_z_pT_Canvas_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)
            for ii in range(1, number_of_cols + 1, 1):
                All_z_pT_Canvas_cd_2_cols = All_z_pT_Canvas_cd_2.cd(ii)
                All_z_pT_Canvas_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)
    # if(args.verbose):
    print(f"\t{color.BOLD}Created {len(All_z_pT_Canvas)} TCanvases...{color.END}")
    args.timer.time_elapsed()
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    hist_store = {"Names": []}
    for                    data_comp in Data_Compare:
        for                 cut_comp in Cut_Compare:
            if(data_comp in ["gdf"]):
                cut_comp = cut_comp.replace("cut_Complete_SIDIS", "no_cut")
            for           smear_comp in Smear_Compare:
                if(data_comp in ["gdf"]):
                    smear_comp = "''"
                for      weight_comp in Weighed_Compare:
                    for lundrho_comp in lundrho_Compare:
                        HistoName = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Name", data=data_comp, cut=cut_comp, smear=smear_comp, Var_X=X_Var, Var_Y=Y_Var, lundrho=lundrho_comp, Weighed=weight_comp)
                        if((HistoName is not None) and (HistoName not in hist_store["Names"])):
                            hist_store["Names"].append(HistoName)
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
    Q2_y_borders = {}
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
        # canvas = All_z_pT_Canvas[Save_Name]
        ################################################################
        ###    Legends     ###
        pad_leg = All_z_pT_Canvas[Save_Name].cd(1).cd(2).cd(1)
        pad_leg.SetFillColor(ROOT.kGray)
        pad_leg.cd()
        ROOT.gStyle.SetOptStat(0)
        if(not hasattr(All_z_pT_Canvas[Save_Name], "legend_store")):
            All_z_pT_Canvas[Save_Name].legend_store = {}
            All_z_pT_Canvas[Save_Name].histos_store = {}
        leg = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
        leg.SetNColumns(1)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.10)
        for num, names in enumerate(hist_store["Names"]):
            All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"] = ROOT.TH1F(f"dummy_{names}_Bin_{Q2_Y_Bin}", "", 1, 0, 1)
            All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"].SetLineColor(find_color(num+1))
            # All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"].SetLineWidth(3)
            # legend_name = names.replace("(Normal_2D)_", "")
            # legend_name = legend_name.replace("_smeared", "")
            # legend_name = legend_name.replace(f"{X_Var})_({Y_Var}", Plot_Var)
            legend_name = legend_naming(names)
            leg.AddEntry(All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"], legend_name, "l")
        leg.Draw("same")
        All_z_pT_Canvas[Save_Name].legend_store["legend"] = leg
        pad_leg.Modified()
        pad_leg.Update()
        ###    Legends     ###
        ################################################################
        ### Integral Plots ###
        Integrated_Pad = All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(1)
        # if((not hasattr(All_z_pT_Canvas[Save_Name], "Integrated_Histos"))):
        #     All_z_pT_Canvas[Save_Name].Integrated_Histos = {}
        # Integrated_Pad.SetFillColor(ROOT.kGray)
        Integrated_Pad.cd()
        # ROOT.gStyle.SetOptStat(0)
        Min_Content, Max_Content = 0, 0
        for num, names in enumerate(hist_store["Names"]):
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"] = Slice_Histos_for_Plotting(rdf_in.Get(names), Var_Plot=Plot_Var, Q2y_Bin=Q2_Y_Bin, zpT_Bin="All")
            if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"] is None):
                continue
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"] = lund_norm(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"], Draw_Type)
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].SetLineColor(find_color(num+1))
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].SetLineWidth(3 if("png" in args.File_Save_Format) else 1)
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].SetTitle(f"{Plot_Title} Plots for Q^{{2}}-y Bin: {Q2_Y_Bin}")
            Max_Content = max([Max_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].GetMaximumBin()))])
            Min_Content = min([Min_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].GetMinimumBin()))])
        for num, names in enumerate(hist_store["Names"]):
            if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"] is None):
                continue
            if(Draw_Type == "Normalized"):
                All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].DrawNormalized("hist E0" if(num == 0) else "hist E0 same")
            else:
                All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].GetYaxis().SetRangeUser(Min_Content, Max_Content)
                All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_Integrated"].Draw("hist E0" if(num == 0) else "hist E0 same")
        ### Integral Plots ###
        ################################################################
        ### 2D Kinematics  ###
        Kinematic_2D_Pad = All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(2)
        Kinematic_2D_Pad.Divide(2, 1, 0.01, 0.01)
        Kinematic_2D_Pad.cd(1)
        Histo_2D_Q2y_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="mdf", cut="cut_Complete_SIDIS_Exclusive_rho", smear="smear", Var_X="Q2_smeared", Var_Y="y_smeared", lundrho="", Weighed="")
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"] = Slice_Histos_for_Plotting(Histo3D=Histo_2D_Q2y_Plot_Legend, Var_Plot="2D", Q2y_Bin=Q2_Y_Bin, zpT_Bin="All")
        if(All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"] is not None):
            All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].SetTitle(f"#splitline{{#scale[2.5]{{Q^{{2}} vs y From #color[{ROOT.kRed}]{{Reconstructed clasdis MC}}}}}}{{#scale[1.75]{{Q^{{2}}-y Bin {Q2_Y_Bin}}}}}")
            All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].GetYaxis().SetRangeUser(1, 8.5)
            All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].Draw("colz")
        else:
            raise SystemError("Could not make the 2D Q2-y Histogram\n")
        for Q2_Y_Bin_ii in range(1, 18, 1):
            if(Q2_Y_Bin_ii not in Q2_y_borders):
                Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, line_width=3 if("png" in args.File_Save_Format) else 1)
            for line in Q2_y_borders[Q2_Y_Bin_ii]:
                line.Draw("same")
        Kinematic_2D_Pad.cd(2)
        Histo_2D_zpT_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="mdf", cut="cut_Complete_SIDIS_Exclusive_rho", smear="smear", Var_X="z_smeared", Var_Y="pT_smeared", lundrho="", Weighed="")
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"] = Slice_Histos_for_Plotting(Histo3D=Histo_2D_zpT_Plot_Legend, Var_Plot="2D", Q2y_Bin=Q2_Y_Bin, zpT_Bin="All")
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].SetTitle(f"#splitline{{#scale[2.5]{{z vs P_{{T}} From #color[{ROOT.kRed}]{{Reconstructed clasdis MC}}}}}}{{#scale[1.75]{{Q^{{2}}-y Bin {Q2_Y_Bin}}}}}")
        if(All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"] is not None):
            All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].GetXaxis().SetRangeUser(0, 1.2)
            All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].Draw("colz")
        else:
            raise SystemError("Could not make the 2D z-pT Histogram\n")
        Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2, Plot_Orientation_Input=Plot_Orientation, line_size_overwrite=3 if("png" in args.File_Save_Format) else 1)
        ### 2D Kinematics  ###
        ################################################################
    if(args.verbose):
        print(f"{color.BOLD}Left Canvas Plots Done...{color.END}")
        args.timer.time_elapsed()
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - Individual z-pT Bins  ###########################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
        # canvas = All_z_pT_Canvas[Save_Name]
        All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin)):
                continue
            cd_number_of_z_pT_all_together = z_pT_Bin
            try:
                if((Plot_Orientation in ["z_pT"])):
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(cd_number_of_z_pT_all_together)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                else:
                    cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                    if((0 == (cd_number_of_z_pT_all_together%number_of_cols))):
                        cd_row += -1
                    cd_col = cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                    All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
                # Histo_2D_zpT_Plot_All = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="mdf", cut="cut_Complete_SIDIS_Extra", smear="smear", Var_X="z_smeared", Var_Y="pT_smeared", lundrho=False, Weighed="")
                # All_z_pT_Canvas[Save_Name].histos_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] = Slice_Histos_for_Plotting(Histo3D=Histo_2D_zpT_Plot_All, Var_Plot="2D", Q2y_Bin=Q2_Y_Bin, zpT_Bin=z_pT_Bin)
                # if(All_z_pT_Canvas[Save_Name].histos_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] is not None):
                #     All_z_pT_Canvas[Save_Name].histos_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().SetRangeUser(0, 1.2)
                #     All_z_pT_Canvas[Save_Name].histos_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].Draw("colz")
                # else:
                #     raise SystemError("Could not make the 2D z-pT Histogram(s)\n")
                ROOT.gStyle.SetOptStat(0)
                Min_Content, Max_Content = 0, 0
                for num, names in enumerate(hist_store["Names"]):
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] = Slice_Histos_for_Plotting(rdf_in.Get(names), Var_Plot=Plot_Var, Q2y_Bin=Q2_Y_Bin, zpT_Bin=z_pT_Bin)
                    if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] is None):
                        continue
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] = lund_norm(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"], Draw_Type)
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetLineColor(find_color(num+1))
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetLineWidth(3 if("png" in args.File_Save_Format) else 1)
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetTitle(f"#splitline{{{Plot_Title} Plots}}{{For Q^{{2}}-y Bin: {Q2_Y_Bin} #topbar z-P_{{T}} Bin: {z_pT_Bin}}}")
                    Max_Content = max([Max_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetMaximumBin()))])
                    Min_Content = min([Min_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetMinimumBin()))])
                for num, names in enumerate(hist_store["Names"]):
                    if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] is None):
                        continue
                    if(Draw_Type == "Normalized"):
                        All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].DrawNormalized("hist E0" if(num == 0) else "hist E0 same")
                    else:
                        All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetYaxis().SetRangeUser(Min_Content, Max_Content)
                        All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].Draw("hist E0" if(num == 0) else "hist E0 same")
                    ROOT.gPad.Update()
            except:
                print(f"{color.Error}Error in Drawing {Plot_Var} Plots for Bin ({Q2_Y_Bin}-{z_pT_Bin}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
        All_z_pT_Canvas[Save_Name].cd()
        All_z_pT_Canvas[Save_Name].Modified()
        All_z_pT_Canvas[Save_Name].Update()
        print(f"{color.BOLD}Q2_Y_Bin = {Q2_Y_Bin} Image Done...{color.END}")
        if(args.verbose):
            args.timer.time_elapsed()
    ####  Filling Canvas (Right) End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Saving Canvases  #########################################################################################################################################################################################################################################################################################################################################################################################
    print("\nSaving...\n")
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        # Save_Name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
        out_name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
        if(args.name):
            out_name = f"{out_name}_{args.name}{args.File_Save_Format}"
        else:
            out_name = f"{out_name}{args.File_Save_Format}"
        if(not args.dry_run):
            All_z_pT_Canvas[Save_Name].SaveAs(out_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{out_name}{color.END}")
        else:
            print(f"{color.Error}Would be Saving: {color.BCYAN}{out_name}{color.END}")
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    return All_z_pT_Canvas


def Draw_Zoomed_Panels_For_Special_Vars(pad, histos_store, Min_Content, Max_Content, Draw_Type):
    pad.cd()
    pad.Divide(4, 3, 0.001, 0.001)
    zoom_ranges = [(None, None),
                   (None, -310),
                   (-215, -210),
                   (-15, 25),
                   (90, 135),
                   (210, 225),
                   (305, 335),
                   (1111, 1117),
                   (2110, 2115),
                   (2210, 2228),
                   (3110, 3125),
                   (3210, None)
    ]
    for i_pad, (xlow, xhigh) in enumerate(zoom_ranges, 1):
        Draw_Canvas(pad, i_pad, 0.15)
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat(0)
        for num, h_original in enumerate(histos_store):
            if(h_original is None):
                continue
            h_zoom = h_original.Clone(f"{h_original.GetName()}_zoom_{i_pad}")
            if(i_pad == 1):  # Full range - already set
                pass
            elif(i_pad == 2):
                min_val = h_original.GetXaxis().GetXmin()
                h_zoom.SetTitle(f"#splitline{{{h_zoom.GetTitle()}}}{{PID Values < {xhigh}}}")
                h_zoom.GetXaxis().SetRangeUser(min_val, xhigh)
            elif(i_pad == len(zoom_ranges)):
                max_val = h_original.GetXaxis().GetXmax()
                h_zoom.SetTitle(f"#splitline{{{h_zoom.GetTitle()}}}{{PID Values > {xlow}}}")
                h_zoom.GetXaxis().SetRangeUser(xlow, max_val)
            else:
                h_zoom.SetTitle(f"#splitline{{{h_zoom.GetTitle()}}}{{PID Values between {xlow} and {xhigh}}}")
                h_zoom.GetXaxis().SetRangeUser(xlow, xhigh)
            # if(num == 0):
            #     h_zoom.SetLineWidth(h_zoom.GetLineWidth()+1)
            if(Draw_Type == "Normalized"):
                h_zoom.DrawNormalized("hist E0" if(num == 0) else "hist E0 same")
            else:
                h_zoom.GetYaxis().SetRangeUser(Min_Content, Max_Content)
                h_zoom.Draw("hist E0" if(num == 0) else "hist E0 same")
    pad.Modified()
    pad.Update()
    return True

def Kinematic_Compare_in_Individual_Bins(rdf_in, args, Q2_Y_Bin="All", z_pT_Bin="All", Data_Compare=["mdf"], Cut_Compare=["cut_Complete_SIDIS_Exclusive_rho"], Smear_Compare=["smear"], Weighed_Compare=[""], lundrho_Compare=["", "lundrho", "lundvpk"], Plot_Var="el", Draw_Type="rhoscale"):
    Plot_Title   = variable_Title_name(Plot_Var) # Automatically adds the 'smearing' or 'gen' title as appropriate
    X_Var, Y_Var = Return_Match_Vars(Input_Var=Plot_Var, Input_Var_2D=None)
    All_z_pT_Canvas = {}
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    Save_Name = f"Comparisons_of_{Plot_Var}_for_Q2_Y_Bin_{Q2_Y_Bin}"
    All_z_pT_Canvas[Save_Name] = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800), Size_Y=int(1500), cd_Space=0.01)
    All_z_pT_Canvas[Save_Name].SetFillColor(ROOT.kGray)
    if(args.verbose):
        print(f"{color.BBLUE}Creating TCanvas: {color.END_B}{Save_Name}{color.BBLUE}...{color.END}")
    All_z_pT_Canvas_cd_1 = All_z_pT_Canvas[Save_Name].cd(1)
    All_z_pT_Canvas_cd_1.SetFillColor(ROOT.kGray)
    All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
    All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)
    
    All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
    All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
    All_z_pT_Canvas_cd_1_Upper.Divide(1, 2, 0.001, 0.001)
    
    All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
    All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
    All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
    All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
    
    All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
    All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
    All_z_pT_Canvas_cd_2.SetFillColor(ROOT.kGray)
    
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    hist_store = {"Names": []}
    for                    data_comp in Data_Compare:
        for                 cut_comp in Cut_Compare:
            if(data_comp in ["gdf"]):
                cut_comp = cut_comp.replace("cut_Complete_SIDIS", "no_cut")
            for           smear_comp in Smear_Compare:
                if(data_comp in ["gdf"]):
                    smear_comp = "''"
                for      weight_comp in Weighed_Compare:
                    for lundrho_comp in lundrho_Compare:
                        HistoName = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Name", data=data_comp, cut=cut_comp, smear=smear_comp, Var_X=X_Var, Var_Y=Y_Var, lundrho=lundrho_comp, Weighed=weight_comp)
                        if((HistoName is not None) and (HistoName not in hist_store["Names"])):
                            hist_store["Names"].append(HistoName)
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
    Q2_y_borders = {}
    ################################################################
    ###    Legends     ###
    pad_leg = All_z_pT_Canvas[Save_Name].cd(1).cd(2).cd(1)
    pad_leg.SetFillColor(ROOT.kGray)
    pad_leg.cd()
    ROOT.gStyle.SetOptStat(0)
    if(not hasattr(All_z_pT_Canvas[Save_Name], "legend_store")):
        All_z_pT_Canvas[Save_Name].legend_store = {}
        All_z_pT_Canvas[Save_Name].histos_store = {}
    leg = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
    leg.SetNColumns(1)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.10)
    for num, names in enumerate(hist_store["Names"]):
        All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"] = ROOT.TH1F(f"dummy_{names}_Bin_{Q2_Y_Bin}", "", 1, 0, 1)
        All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"].SetLineColor(find_color(num+1))
        legend_name = legend_naming(names)
        leg.AddEntry(All_z_pT_Canvas[Save_Name].legend_store[f"dummy_{names}_Bin_{Q2_Y_Bin}"], legend_name, "l")
    leg.Draw("same")
    All_z_pT_Canvas[Save_Name].legend_store["legend"] = leg
    pad_leg.Modified()
    pad_leg.Update()
    ###    Legends     ###
    ################################################################
    ### 2D Kinematics  ###
    All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(2).SetFillColor(ROOT.kGray)
    Kinematic_2D_Pad = All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(1)
    Kinematic_2D_Pad.Divide(2, 1, 0.01, 0.01)
    Kinematic_2D_Pad.cd(1)
    plot_type = f"#color[{ROOT.kRed}]{{Reconstructed clasdis MC}}"
    if("mdf" in Data_Compare):
        Histo_2D_Q2y_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="mdf", cut="cut_Complete_SIDIS_Exclusive_rho", smear="smear", Var_X="Q2_smeared", Var_Y="y_smeared", lundrho="", Weighed="")
    elif("gdf" in Data_Compare):
        plot_type = f"#color[{ROOT.kGreen}]{{Generated clasdis MC}}"
        Histo_2D_Q2y_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="gdf", cut="no_cut",             smear="''",    Var_X="Q2",         Var_Y="y",         lundrho="", Weighed="")
    else:
        plot_type = f"#color[{ROOT.kBlue}]{{Experimental Data}}"
        Histo_2D_Q2y_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="rdf", cut="cut_Complete_SIDIS_Exclusive_rho",       smear="''",    Var_X="Q2",         Var_Y="y",         lundrho="", Weighed="")
    All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"] = Slice_Histos_for_Plotting(Histo3D=Histo_2D_Q2y_Plot_Legend, Var_Plot="2D", Q2y_Bin=Q2_Y_Bin, zpT_Bin=z_pT_Bin)
    if(All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"] is not None):
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].SetTitle(f"#splitline{{#scale[2.5]{{Q^{{2}} vs y From {plot_type}}}}}{{#scale[1.75]{{Q^{{2}}-y Bin {Q2_Y_Bin if(str(Q2_Y_Bin) not in ['0']) else 'All'} #topbar z-P_{{T}} Bin {z_pT_Bin if(str(z_pT_Bin) not in ['0']) else 'All'}}}}}")
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].GetYaxis().SetRangeUser(1, 8.5)
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_Q2y_Plot_Legend_Bin_{Q2_Y_Bin}"].Draw("colz")
    else:
        raise SystemError("Could not make the 2D Q2-y Histogram\n")
    for Q2_Y_Bin_ii in range(1, 18, 1):
        if(Q2_Y_Bin_ii not in Q2_y_borders):
            Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, line_width=3 if("png" in args.File_Save_Format) else 1)
        for line in Q2_y_borders[Q2_Y_Bin_ii]:
            line.Draw("same")
    Kinematic_2D_Pad.cd(2)
    if("mdf" in Data_Compare):
        Histo_2D_zpT_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="mdf", cut="cut_Complete_SIDIS_Exclusive_rho", smear="smear", Var_X="z_smeared", Var_Y="pT_smeared", lundrho="", Weighed="")
    elif("gdf" in Data_Compare):
        Histo_2D_zpT_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="gdf", cut="no_cut",             smear="''",    Var_X="z",         Var_Y="pT",         lundrho="", Weighed="")
    else:
        Histo_2D_zpT_Plot_Legend = HistoName_Return(df_in=rdf_in, Return_Name_or_Histo="Hist", data="rdf", cut="cut_Complete_SIDIS_Exclusive_rho",       smear="''",    Var_X="z",         Var_Y="pT",         lundrho="", Weighed="")
    All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"] = Slice_Histos_for_Plotting(Histo3D=Histo_2D_zpT_Plot_Legend, Var_Plot="2D", Q2y_Bin=Q2_Y_Bin, zpT_Bin=z_pT_Bin)
    All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].SetTitle(f"#splitline{{#scale[2.5]{{z vs P_{{T}} From {plot_type}}}}}{{#scale[1.75]{{Q^{{2}}-y Bin {Q2_Y_Bin if(str(Q2_Y_Bin) not in ['0']) else 'All'} #topbar z-P_{{T}} Bin {z_pT_Bin if(str(z_pT_Bin) not in ['0']) else 'All'}}}}}")
    if(All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"] is not None):
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].GetXaxis().SetRangeUser(0, 1.2)
        All_z_pT_Canvas[Save_Name].legend_store[f"Histo_2D_zpT_Plot_Legend_Bin_{Q2_Y_Bin}"].Draw("colz")
    else:
        raise SystemError("Could not make the 2D z-pT Histogram\n")
    Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2, Plot_Orientation_Input="z_pT", line_size_overwrite=3 if("png" in args.File_Save_Format) else 1)
    ### 2D Kinematics  ###
    ################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - Individual z-pT Bin   ###########################################################################################################################################################################################################################################################################################################################################################
    All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
    try:
        All_z_pT_Canvas_cd_2.SetFillColor(ROOT.kGray)
        All_z_pT_Canvas_cd_2.Divide(1, 1, 0, 0)
        All_z_pT_Canvas_cd_2.cd(1)
        using_log = False
        if(Plot_Var in ["rho0_parent", "Par_PID_pip", "Par_PID_el"]):
            ROOT.gPad.SetLogy(1)
            using_log = True
        else:
            ROOT.gPad.SetLogy(0)
        Draw_Canvas(All_z_pT_Canvas_cd_2, 1, 0.15)
        ROOT.gStyle.SetOptStat(0)
        Min_Content, Max_Content = 0, 0
        for num, names in enumerate(hist_store["Names"]):
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] = Slice_Histos_for_Plotting(rdf_in.Get(names), Var_Plot=Plot_Var, Q2y_Bin=Q2_Y_Bin, zpT_Bin=z_pT_Bin)
            if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] is None):
                continue
            if("z1_plus_z2" in names):
                All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().SetRangeUser(0.01, 1.8)
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] = lund_norm(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"], Draw_Type)
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetLineColor(find_color(num+1))
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetLineWidth(3 if("png" in args.File_Save_Format) else 1)
            All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].SetTitle(f"#splitline{{{Plot_Title} Plots}}{{For Q^{{2}}-y Bin: {Q2_Y_Bin} #topbar z-P_{{T}} Bin: {z_pT_Bin}}}")
            if("TH1" in str(type(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"]))):
                xaxis_title = All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().GetTitle()
                if((Plot_Var in xaxis_title) and (Plot_Title not in xaxis_title)):
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().SetTitle(Plot_Title)
            else:
                xaxis_title = All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().GetTitle()
                yaxis_title = All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetYaxis().GetTitle()
                if((X_Var in xaxis_title) and (variable_Title_name(X_Var) not in xaxis_title)):
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetXaxis().SetTitle(variable_Title_name(X_Var))
                if((Y_Var in yaxis_title) and (variable_Title_name(Y_Var) not in yaxis_title)):
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetYaxis().SetTitle(variable_Title_name(Y_Var))
            Max_Content = max([Max_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetMaximumBin()))])
            Min_Content = min([Min_Content, 1.2*(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetBinContent(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetMinimumBin()))])
            if(using_log and (Min_Content == 0)):
                Min_Content = 0.1 if(Draw_Type != "Normalized") else 1e-6
        if(Plot_Var in ["rho0_parent", "Par_PID_pip", "Par_PID_el"]):
            list_of_histos = [All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] for names in hist_store["Names"]]
            Draw_Zoomed_Panels_For_Special_Vars(pad=All_z_pT_Canvas_cd_2.cd(1), histos_store=list_of_histos, Min_Content=Min_Content, Max_Content=Max_Content, Draw_Type=Draw_Type)
        else:
            for num, names in enumerate(hist_store["Names"]):
                if(All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"] is None):
                    continue
                if(Draw_Type == "Normalized"):
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].DrawNormalized("hist E0" if(num == 0) else "hist E0 same")
                else:
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].GetYaxis().SetRangeUser(Min_Content, Max_Content)
                    All_z_pT_Canvas[Save_Name].histos_store[f"{names}_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"].Draw("hist E0" if(num == 0) else "hist E0 same")
                ROOT.gPad.Update()
    except:
        print(f"{color.Error}Error in Drawing {Plot_Var} Plots for Bin ({Q2_Y_Bin}-{z_pT_Bin}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
    All_z_pT_Canvas[Save_Name].cd()
    All_z_pT_Canvas[Save_Name].Modified()
    All_z_pT_Canvas[Save_Name].Update()
    ####  Filling Canvas (Right) End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Saving Canvases  #########################################################################################################################################################################################################################################################################################################################################################################################
    print("\nSaving...\n")
    out_name = f"Comparisons_of_{Plot_Var}_for_Individual_Q2_Y_Bin_{Q2_Y_Bin}_z_pT_Bin_{z_pT_Bin}"
    if(args.name):
        out_name = f"{out_name}_{args.name}{args.File_Save_Format}"
    else:
        out_name = f"{out_name}{args.File_Save_Format}"
    if(not args.dry_run):
        All_z_pT_Canvas[Save_Name].SaveAs(out_name)
        print(f"{color.BOLD}Saved: {color.BBLUE}{out_name}{color.END}")
    else:
        print(f"{color.Error}Would be Saving: {color.BCYAN}{out_name}{color.END}")
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    return All_z_pT_Canvas

if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    if(args.use_same_file):
        args.file2 = None
        args.file3 = None
        combined_file = ROOT.TFile.Open(args.file1, "READ")
    else:
        combined_file = Create_Combined_Memory_File(args.file1, args.file2, var_restrict=args.var, file_path_3=args.file3)
    args.timer.time_elapsed()
    # compare_to_lund = ["", "lundrho", "lundvpk"] if(args.var not in ["rho0_parent", "Par_PID_pip"]) else [""]
    compare_to_lund = ["", "lundvpk"]            if(args.var not in ["rho0_parent", "Par_PID_pip"]) else [""]
    data_compare    = [args.Data_Compare]        if(args.var not in ["rho0_parent", "Par_PID_pip"]) else ["mdf", "gdf"]
    if((getattr(args, "Q2_y_Bin_Individual", None) is None) and (getattr(args, "z_pT_Bin_Individual", None) not in ["All", "0", 0])):
        print(f"\n{color.BOLD}Running the {color.BBLUE}'Kinematic_1D_Compare_in_z_pT_Images_Together()'{color.END_B} function...{color.END}\n")
        run_range = range(1, 18) if(getattr(args, "Q2_y_Bin_Select", None) is None) else [args.Q2_y_Bin_Select]
        Kinematic_1D_Compare_in_z_pT_Images_Together(combined_file, args, Q2_Y_Bin_Range=run_range,       Data_Compare=data_compare, Cut_Compare=["cut_Complete_SIDIS_Exclusive_rho"], Smear_Compare=["smear"], Weighed_Compare=[""], lundrho_Compare=compare_to_lund, Plot_Var=args.var, Draw_Type="rhoscale")
    else:
        print(f"\n{color.BOLD}Running the {color.BBLUE}'Kinematic_Compare_in_Individual_Bins()'{color.END_B} function...{color.END}\n")
        Input_Q2y = getattr(args, "Q2_y_Bin_Individual", "All") if(getattr(args, "Q2_y_Bin_Individual", "All") is not None) else "All"
        Input_zpT = getattr(args, "z_pT_Bin_Individual", "All") if(getattr(args, "z_pT_Bin_Individual", "All") is not None) else "All"
        Kinematic_Compare_in_Individual_Bins(combined_file, args, Q2_Y_Bin=Input_Q2y, z_pT_Bin=Input_zpT, Data_Compare=data_compare, Cut_Compare=["cut_Complete_SIDIS_Exclusive_rho"], Smear_Compare=["smear"], Weighed_Compare=[""], lundrho_Compare=compare_to_lund, Plot_Var=args.var, Draw_Type="rhoscale")
    combined_file.Close()
    args.timer.stop()
    print("\nDone\n")
