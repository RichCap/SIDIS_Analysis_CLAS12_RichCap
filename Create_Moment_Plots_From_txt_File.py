#!/usr/bin/env python3

import argparse
import ROOT
import sys
import time
import glob

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir
from array import array

ROOT.TH1.AddDirectory(0)
# ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetTitleOffset(1.75,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetPadLeftMargin(0.115)   # default is ≃0.10


ROOT.gROOT.SetBatch(1)

# Get the code for defining 'Get_Bin_Center_Dictionary' from Get_Bin_Center_of_Kinematic_Bins.ipynb    
# From REAL_File_Name = Pass_2_Plots_for_Maria_FC_14_V2_All - Defined on: 4-17-2025
    # Ran with Cut_Type = cut_Complete_SIDIS_Integrate
Get_Bin_Center_Dictionary = {'Key': ['mean_Q2', 'ErrorQ2', 'mean__y', 'Error_y', 'mean__z', 'Error_z', 'mean_pT', 'ErrorpT', 'mean_xB', 'ErrorxB'], 'All-All': [3.296, 0.0002905, 0.5652, 2.86e-05, 0.3942, 2.92e-05, 0.269, 2.5e-05, 0.2998, 2.53e-05], '1-All': [2.195, 0.0001228, 0.6978, 3.08e-05, 0.34, 0.0001083, 0.2825, 9.9e-05, 0.1584, 1.22e-05], '2-All': [2.199, 0.0001164, 0.5985, 2.92e-05, 0.3901, 0.0001183, 0.2868, 0.0001062, 0.1851, 1.42e-05], '3-All': [2.202, 0.0001269, 0.4987, 3.2e-05, 0.4196, 0.0001329, 0.2499, 9.82e-05, 0.2226, 2e-05], '4-All': [2.204, 0.000146, 0.3997, 3.68e-05, 0.4594, 0.0001286, 0.2479, 0.0001073, 0.2786, 3.24e-05], '5-All': [2.638, 0.0001651, 0.6973, 3.3e-05, 0.3524, 0.0001162, 0.2727, 0.0001049, 0.1905, 1.57e-05], '6-All': [2.64, 0.0001655, 0.5978, 3.3e-05, 0.4067, 0.0001252, 0.2622, 0.0001081, 0.2224, 1.94e-05], '7-All': [2.64, 0.0001489, 0.4984, 2.98e-05, 0.414, 0.0001292, 0.2445, 8.82e-05, 0.2671, 2.25e-05], '8-All': [2.638, 0.0001382, 0.4042, 2.73e-05, 0.4274, 0.0001002, 0.2827, 9.88e-05, 0.3296, 2.89e-05], '9-All': [3.272, 0.000227, 0.6976, 2.83e-05, 0.3545, 0.0001004, 0.2962, 0.0001034, 0.2361, 1.95e-05], '10-All': [3.27, 0.0002368, 0.598, 2.95e-05, 0.3895, 0.0001154, 0.2557, 9.36e-05, 0.2754, 2.46e-05], '11-All': [3.266, 0.0002197, 0.4987, 2.75e-05, 0.4073, 0.000111, 0.2562, 8.56e-05, 0.3303, 2.9e-05], '12-All': [3.254, 0.0002218, 0.406, 2.71e-05, 0.4199, 9.38e-05, 0.2757, 9.64e-05, 0.4045, 3.86e-05], '13-All': [4.393, 0.0004414, 0.698, 2.79e-05, 0.3584, 0.0001009, 0.2804, 9.79e-05, 0.3169, 3.45e-05], '14-All': [4.378, 0.0004765, 0.5988, 3.01e-05, 0.3995, 0.0001153, 0.2555, 9.47e-05, 0.3682, 4.42e-05], '15-All': [4.338, 0.0004371, 0.5004, 2.83e-05, 0.4036, 0.0001079, 0.2663, 9.24e-05, 0.437, 5e-05], '16-All': [6.254, 0.0009806, 0.6981, 4.02e-05, 0.3612, 0.0001446, 0.2669, 0.0001338, 0.4509, 7.51e-05], '17-All': [6.198, 0.0010117, 0.6014, 4.3e-05, 0.4035, 0.0001506, 0.2809, 0.0001535, 0.519, 9.11e-05]}
    
def Get_Bin_Center_Function(Q2_y_Bin, z_pT_Bin, Variable="All"):
    if(str(z_pT_Bin) in ["0", 0, "all", "Integrated"]):
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
    
def Q2_y_bin_values_New(Q2_Y_Bin_Num, return_type):
    output = "Error"
    Q2_y_Borders = {1:  [2.4, 2.0, 0.75, 0.65],
                    2:  [2.4, 2.0, 0.65, 0.55],
                    3:  [2.4, 2.0, 0.55, 0.45],
                    4:  [2.4, 2.0, 0.45, 0.35],
                    5:  [2.9, 2.4, 0.75, 0.65],
                    6:  [2.9, 2.4, 0.65, 0.55],
                    7:  [2.9, 2.4, 0.55, 0.45],
                    8:  [2.9, 2.4, 0.45, 0.35],
                    9:  [3.7, 2.9, 0.75, 0.65],
                    10: [3.7, 2.9, 0.65, 0.55],
                    11: [3.7, 2.9, 0.55, 0.45],
                    12: [3.7, 2.9, 0.45, 0.35],
                    13: [5.3, 3.7, 0.75, 0.65],
                    14: [5.3, 3.7, 0.65, 0.55],
                    15: [5.3, 3.7, 0.55, 0.45],
                    16: [7.9, 5.3, 0.75, 0.65],
                    17: [7.9, 5.3, 0.65, 0.55]}
    if(Q2_Y_Bin_Num in Q2_y_Borders):
        Q2_max, Q2_min, y_max, y_min = Q2_y_Borders[Q2_Y_Bin_Num]
    else:
        return output
    if("y" in return_type):
        if("Center" in return_type):
            output = f"{(y_max + y_min) / 2:.3f}"
        else:
            output = f"{y_min:.2f} < y < {y_max:.2f}"
    elif("Q2" in return_type):
        if("Center" in return_type):
            output = f"{(Q2_max + Q2_min) / 2:.3f}"
        else:
            output = f"{Q2_min:.2f} < Q2 < {Q2_max:.2f}"
    return output

def create_legend(x1, y1, x2, y2, nColumns=1, Legend_Title="Bin (Range) Information"):
    legend_create = ROOT.TLegend(x1, y1, x2, y2)
    legend_create.SetNColumns(nColumns)  # Start with 1 column
    legend_create.SetHeader("".join(["#scale[1.35]{", str(Legend_Title), "}"]), "C") # option "C" allows to center the header
    return legend_create


def Plot_Fit_Parameter_ShadedSectorGraphs(Fit_Parameters_Input, From_Python_or_Text="Python", Q2_or_y_Group="y", Variable_to_plot_against="Q2", 
                                          Use_Sectors_Q=True, Parameter_List=["Parameter B", "Parameter C"], Correction_Type="Bin-by-Bin Correction", 
                                          Sector_Particle="esec", Saving_Q=True, Save_Name_Extra="", HistoType="1D", Comparison_Info=[1, False, False],
                                          Group_Images_Q=False):
    latex = {}
    if(Variable_to_plot_against in [Q2_or_y_Group]):
        Variable_to_plot_against = "xB" if(Q2_or_y_Group not in ["xB"]) else "Q2"
        print(f"\n{color.Error}Reseting Variable_to_plot_against to be {Variable_to_plot_against}{color.END}\n")

    Q2_bin_group_def = {
        "Group_1": [1, 2, 3, 4, ""],
        "Group_2": [5, 6, 7, 8, ""],
        "Group_3": [9, 10, 11, 12, ""],
        "Group_4": [13, 14, 15, "", ""],
        "Group_5": [16, 17, "", ""]}

    y__bin_group_def = {
        "Group_1": [1, 5, 9, 13, 16],
        "Group_2": [2, 6, 10, 14, 17],
        "Group_3": [3, 7, 11, 15, ""],
        "Group_4": [4, 8, 12, "", ""]}
    
    xB_bin_group_def = {
        "Group_1": [4, 7, 10, "", ""], 
        "Group_2": [8, 11, 13, "", ""], 
        "Group_3": ["", "", "", "", ""], 
        "Group_4": ["", "", "", "", ""], 
        "Group_5": ["", "", "", ""]}


    if(Q2_or_y_Group   in ["Q2"]):
        for group in Q2_bin_group_def:
            print(str(f"Q2-y Bins in Q2 Row/{group} = {Q2_bin_group_def[group]}".replace("_", " ")))
        selected_var_group = Q2_bin_group_def
    elif(Q2_or_y_Group in ["y"]):
        for group in y__bin_group_def:
            print(str(f"Q2-y Bins in y  Row/{group} = {y__bin_group_def[group]}".replace("_", " ")))
        selected_var_group = y__bin_group_def
    else:
        for group in xB_bin_group_def:
            print(str(f"Q2-y Bins in xB Row/{group} = {xB_bin_group_def[group]}".replace("_", " ")))
        selected_var_group = xB_bin_group_def

    x_values, x_errs = {}, {}
    y_values, y_errs = {}, {}
    y_maxs_collect, y_max_errs_collect = {}, {}
    y_mins_collect, y_min_errs_collect = {}, {}
    tgraph_ext_shaded, tgraph_shaded, tgraph_errors = {}, {}, {}
    canvas, legend, mg = {}, {}, {}
    
    # z_pT_Bin_Type = "All"
    z_pT_Bin_Type = "Integrated"

    if(Comparison_Info[0] != 1):
        Comparison_Type = "Tagged_Proton_Comparison" if(Comparison_Info[1]) else "Proton_Cut_Comparison" if(Comparison_Info[2]) else "Other_File_Comparison"
        print(f"{color.BOLD}Running {Comparison_Type.replace('_', ' ')}{color.END}")
        File_Lists = [1, 2]
    else:
        File_Lists = [1]
        Comparison_Type = ""

    # Keep track of ROOT objects to ensure they stay alive
    root_objects = ROOT.TList()

    for Parameter in Parameter_List:
        key_names = f"({Q2_or_y_Group}_Group)_({Parameter})"
        canvas[key_names] = ROOT.TCanvas(f"canvas_{key_names}", "Graph with Extended Shaded Regions", 1200, 1000)
        legend[key_names] = ROOT.TLegend(0.9, 0.1, 0.49, 0.4)
        if(Comparison_Type not in [""]):
            legend[key_names].SetHeader(f"Dotted Lines are for {Comparison_Type.replace('_', ' ')}", "C")
        mg[key_names] = ROOT.TMultiGraph()
        mg[key_names].SetName(key_names)
        root_objects.Add(canvas[key_names])
        root_objects.Add(legend[key_names])
        root_objects.Add(mg[key_names])

        # Initialize group-specific canvases for Group_Images_Q
        if(Group_Images_Q):
            for group_num    in selected_var_group:
                key_row_base = f"{key_names}_({group_num})"
                canvas[key_row_base] = ROOT.TCanvas(f"canvas_{key_row_base}", "Graph with Extended Shaded Regions", 1200, 1000)
                legend[key_row_base] = ROOT.TLegend(0.9, 0.1, 0.49, 0.4)
                if(Comparison_Type not in [""]):
                    legend[key_row_base].SetHeader(f"Dotted Lines are for {Comparison_Type.replace('_', ' ')}", "C")
                mg[key_row_base] = ROOT.TMultiGraph()
                mg[key_row_base].SetName(key_row_base)
                root_objects.Add(canvas[key_row_base])
                root_objects.Add(legend[key_row_base])
                root_objects.Add(mg[key_row_base])

        for group_num in selected_var_group:
            color_ii = ROOT.kOrange if("1" in str(group_num)) else ROOT.kSpring if("2" in str(group_num)) else ROOT.kViolet if("3" in str(group_num)) else ROOT.kAzure if("4" in str(group_num)) else ROOT.kPink
            key_row_base = f"{key_names}_({group_num})"
            
            for File_Num in File_Lists:
                key_row_names = key_row_base if(File_Num == 1) else f"(File_{File_Num})_{key_row_base}"
    
                x_values[key_row_names], x_errs[key_row_names] = [], []
                y_values[key_row_names], y_errs[key_row_names] = [], []
                y_maxs_collect[key_row_names], y_max_errs_collect[key_row_names], y_mins_collect[key_row_names], y_min_errs_collect[key_row_names] = [], [], [], []
    
                for Q2_y_Bin in selected_var_group[group_num]:
                    if(Q2_y_Bin in ['']):
                        continue
    
                    if(From_Python_or_Text in ["Text"]):
                        Fit_Parameter_Key     = f"(Bin {Q2_y_Bin}-{z_pT_Bin_Type})_({Parameter})"
                    else:
                        Fit_Parameter_Key     = f"(Q2-y-z-pT Bin '{Q2_y_Bin}-{z_pT_Bin_Type}')_({Parameter})_(Correction '{'Bin' if('Bin' in Correction_Type) else 'Bayes'}')_{HistoType}"
                        if(File_Num != 1):
                            Fit_Parameter_Key = f"(File_{File_Num})_{Fit_Parameter_Key}"
                        
                    x_values[key_row_names].append(round(Get_Bin_Center_Function(Q2_y_Bin, z_pT_Bin=z_pT_Bin_Type, Variable=f"mean_{Variable_to_plot_against}"), 4))
                    x_errs[key_row_names].append(Get_Bin_Center_Function(Q2_y_Bin,         z_pT_Bin=z_pT_Bin_Type, Variable=f"Error_{Variable_to_plot_against}"))
                    if(From_Python_or_Text in ["Text"]):
                        y_values[key_row_names].append(Fit_Parameters_Input[Fit_Parameter_Key][0][0])
                        y_errs[key_row_names].append(Fit_Parameters_Input[Fit_Parameter_Key][0][1])
                    else:
                        y_values[key_row_names].append(Fit_Parameters_Input[Fit_Parameter_Key][0])
                        y_errs[key_row_names].append(Fit_Parameters_Input[Fit_Parameter_Key][1])
    
                    current_max_val = -float("inf")
                    current_max_err = -float("inf")
                    current_min_val =  float("inf")
                    current_min_err =  float("inf")
    
                    if(Use_Sectors_Q):
                        Fit_Parameter_Key_Sector = f"(Bin {Q2_y_Bin}-{z_pT_Bin_Type})_({Parameter})"
                        for sec in range(1, 7):
                            if(From_Python_or_Text not in ["Python"]):
                                bounds_upper = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0] + Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][1]
                                bounds_lower = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0] - Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][1]
                                center_val = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0][0]
                                center_err = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0][1]
                                if(not (((center_val + center_err) < bounds_upper) and ((center_val - center_err) > bounds_lower))):
                                    if(((center_val + center_err) < Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0]) and (current_max_val < Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0])):
                                        current_max_val = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0]
                                        current_max_err = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][1]
                                    if(((center_val + center_err) > Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0]) and (current_min_val > Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0])):
                                        current_min_val = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][0]
                                        current_min_err = Fit_Parameters_Input[Fit_Parameter_Key_Sector][sec][1]
                            else:
                                Fit_Parameter_Key_Sector = f"{Fit_Parameter_Key}_({Sector_Particle}_{sec})"
                                # print(f"Fit_Parameters_Input[{Fit_Parameter_Key_Sector}] = {Fit_Parameters_Input[Fit_Parameter_Key_Sector]}")
                                bounds_upper = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0] + Fit_Parameters_Input[Fit_Parameter_Key_Sector][1]
                                bounds_lower = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0] - Fit_Parameters_Input[Fit_Parameter_Key_Sector][1]
                                center_val   = Fit_Parameters_Input[Fit_Parameter_Key][0]
                                center_err   = Fit_Parameters_Input[Fit_Parameter_Key][1]
                                if(not (((center_val + center_err) < bounds_upper) and ((center_val - center_err) > bounds_lower))):
                                    if(((center_val + center_err) < Fit_Parameters_Input[Fit_Parameter_Key_Sector][0]) and (current_max_val < Fit_Parameters_Input[Fit_Parameter_Key_Sector][0])):
                                        current_max_val = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0]
                                        current_max_err = Fit_Parameters_Input[Fit_Parameter_Key_Sector][1]
                                    if(((center_val + center_err) > Fit_Parameters_Input[Fit_Parameter_Key_Sector][0]) and (current_min_val > Fit_Parameters_Input[Fit_Parameter_Key_Sector][0])):
                                        current_min_val = Fit_Parameters_Input[Fit_Parameter_Key_Sector][0]
                                        current_min_err = Fit_Parameters_Input[Fit_Parameter_Key_Sector][1]
                    if(current_max_val in [-float("inf")]):
                        current_max_val = Fit_Parameters_Input[Fit_Parameter_Key][0]
                        current_max_err = Fit_Parameters_Input[Fit_Parameter_Key][1]
                    if(current_min_val in [float("inf")]):
                        current_min_val = Fit_Parameters_Input[Fit_Parameter_Key][0]
                        current_min_err = Fit_Parameters_Input[Fit_Parameter_Key][1]
    
                    y_maxs_collect[key_row_names].append(current_max_val)
                    y_max_errs_collect[key_row_names].append(current_max_err)
                    y_mins_collect[key_row_names].append(current_min_val)
                    y_min_errs_collect[key_row_names].append(current_min_err)
    
                x_values_main = array('d', x_values[key_row_names])
                x_errs_main   = array('d', x_errs[key_row_names])
                y_values_main = array('d', y_values[key_row_names])
                y_errs_main   = array('d', y_errs[key_row_names])
                y_maxs        = array('d', y_maxs_collect[key_row_names])
                y_max_errs    = array('d', y_max_errs_collect[key_row_names])
                y_mins        = array('d', y_mins_collect[key_row_names])
                y_min_errs    = array('d', y_min_errs_collect[key_row_names])
                y_err_low     = array('d', [y - min_val   for y,   min_val in zip(y_values_main,   y_mins)])
                y_err_high    = array('d', [max_val - y   for y,   max_val in zip(y_values_main,   y_maxs)])
                ext_err_low   = array('d', [err + min_err for err, min_err in zip(y_err_low,   y_min_errs)])
                ext_err_high  = array('d', [err + max_err for err, max_err in zip(y_err_high,  y_max_errs)])
                n_points = len(x_values_main)
    
                canvas[key_names].cd()
                tgraph_ext_shaded[key_row_names] = ROOT.TGraphAsymmErrors(n_points, x_values_main, y_values_main, array('d', [0]*n_points), array('d', [0]*n_points), ext_err_low, ext_err_high)
                tgraph_ext_shaded[key_row_names].SetName(f"tgraph_ext_shaded_{key_row_names}")
                tgraph_shaded[key_row_names]     = ROOT.TGraphAsymmErrors(n_points, x_values_main, y_values_main, array('d', [0]*n_points), array('d', [0]*n_points), y_err_low,   y_err_high)
                tgraph_shaded[key_row_names].SetName(f"tgraph_shaded_{key_row_names}")
                tgraph_errors[key_row_names]     = ROOT.TGraphAsymmErrors(n_points, x_values_main, y_values_main, x_errs_main, x_errs_main, y_errs_main, y_errs_main)
                tgraph_errors[key_row_names].SetName(f"tgraph_errors_{key_row_names}")
                root_objects.Add(tgraph_ext_shaded[key_row_names])
                root_objects.Add(tgraph_shaded[key_row_names])
                root_objects.Add(tgraph_errors[key_row_names])
    
                row = int(str(group_num).replace("Group_", ""))
                # tgraph_ext_shaded[key_row_names].SetFillColorAlpha(color_ii-9, 0.35-(row*0.01))
                tgraph_ext_shaded[key_row_names].SetFillColorAlpha(color_ii-(10-File_Num), 0.35-(row*0.01))
                tgraph_ext_shaded[key_row_names].GetYaxis().SetRangeUser(-0.9, 0.2)
                # tgraph_shaded[key_row_names].SetFillColorAlpha(color_ii-6, 0.35-(row*0.01))
                tgraph_shaded[key_row_names].SetFillColorAlpha(color_ii-(7-File_Num), 0.35-(row*0.01))
                tgraph_shaded[key_row_names].SetFillStyle(3240+(row*2))
        
                tgraph_errors[key_row_names].SetMarkerStyle(21)
                tgraph_errors[key_row_names].SetMarkerSize(1)
                tgraph_errors[key_row_names].SetLineColor(color_ii)
                tgraph_errors[key_row_names].SetMarkerColor(color_ii)
                tgraph_errors[key_row_names].SetLineWidth(File_Num)
                tgraph_errors[key_row_names].SetLineStyle(File_Num)
                
                # Add to main multigraph
                mg[key_names].Add(tgraph_shaded[key_row_names], "A3")
                mg[key_names].Add(tgraph_errors[key_row_names], "PL")

                if(File_Num == 1):
                    Legend_Titles_str = f"{Q2_or_y_Group if(Q2_or_y_Group not in ['Q2']) else 'Q^{2}'} Bins: {Q2_y_bin_values_New(selected_var_group[group_num][0], Q2_or_y_Group)}"
                    legend[key_names].AddEntry(tgraph_errors[key_row_names], f"#color[{color_ii}]{{{Legend_Titles_str}}}", "PL")
                    if(Use_Sectors_Q):
                        legend[key_names].AddEntry(tgraph_shaded[key_row_names], f"#color[{color_ii-6}]{{Sector Ranges of {Legend_Titles_str}}}", "f")
                canvas[key_names].Modified()
                canvas[key_names].Update()

                if(Group_Images_Q):
                    canvas[key_row_base].cd()
                    # Clone graphs for group-specific multigraph to avoid ownership issues
                    tgraph_shaded_clone = ROOT.TGraphAsymmErrors(tgraph_shaded[key_row_names])
                    tgraph_shaded_clone.SetName(f"tgraph_shaded_clone_{key_row_names}")
                    tgraph_errors_clone = ROOT.TGraphAsymmErrors(tgraph_errors[key_row_names])
                    tgraph_errors_clone.SetName(f"tgraph_errors_clone_{key_row_names}")
                    root_objects.Add(tgraph_shaded_clone)
                    root_objects.Add(tgraph_errors_clone)

                    tgraph_shaded_clone.SetFillColorAlpha(color_ii-(7-File_Num), 0.35-(row*0.01))
                    tgraph_shaded_clone.SetFillStyle(3240+(row*2))
                    tgraph_errors_clone.SetMarkerStyle(21)
                    tgraph_errors_clone.SetMarkerSize(1)
                    tgraph_errors_clone.SetLineColor(color_ii)
                    tgraph_errors_clone.SetMarkerColor(color_ii)
                    tgraph_errors_clone.SetLineWidth(File_Num)
                    tgraph_errors_clone.SetLineStyle(File_Num)

                    mg[key_row_base].Add(tgraph_shaded_clone, "A3")
                    mg[key_row_base].Add(tgraph_errors_clone, "PL")
                    if(File_Num == 1):
                        legend[key_row_base].AddEntry(tgraph_errors_clone,     f"#color[{color_ii}]{{{Legend_Titles_str}}}", "PL")
                        if(Use_Sectors_Q):
                            legend[key_row_base].AddEntry(tgraph_shaded_clone, f"#color[{color_ii-6}]{{Sector Ranges of {Legend_Titles_str}}}", "f")
                    Moment_Title = f"Cos({'2' if('C' in str(Parameter)) else ''}#phi_{{h}})"
                    Multigraph_Title_Line_1 = f"Plot of {Moment_Title} vs {variable_Title_name(Variable_to_plot_against)}"
                    if("Tagged_Proton" in Save_Name_Extra):
                        Multigraph_Title_Line_2 = f"{root_color.Bold}{{Tagged Proton}} #topbar #color[{root_color.Blue}]{{{Correction_Type}}}"
                    elif("ProtonCut"   in Save_Name_Extra):
                        Multigraph_Title_Line_2 = f"{root_color.Bold}{{Cut on Proton MM}} #topbar #color[{root_color.Blue}]{{{Correction_Type}}}"
                    else:
                        Multigraph_Title_Line_2 = f"#color[{root_color.Blue}]{{{Correction_Type}}}"
                    if(HistoType in ["3D", "5D"]):
                        Multigraph_Title_Line_2 = Multigraph_Title_Line_2.replace(f"{{{Correction_Type}}}", f"{{Multidimensional {HistoType} {Correction_Type}}}")
                    if(Comparison_Type in [""]):
                        mg[key_row_base].SetTitle(f"#splitline{{{Multigraph_Title_Line_1}}}{{{Multigraph_Title_Line_2}}}; {variable_Title_name(Variable_to_plot_against)}; {Moment_Title}")
                    else:
                        mg[key_row_base].SetTitle(f"#splitline{{#splitline{{{Multigraph_Title_Line_1}}}{{{Multigraph_Title_Line_2}}}}}{{{Comparison_Type.replace('_', ' ')}}}; {variable_Title_name(Variable_to_plot_against)}; {Moment_Title}")
                    mg[key_row_base].Draw("A")
                    mg[key_row_base].GetYaxis().SetRangeUser(-0.25, 0.1)
                    legend[key_row_base].Draw()
                    canvas[key_row_base].Modified()
                    canvas[key_row_base].Update()
                    draw_annotations(annotations2)
                    Save_Name = "".join([
                        f"{Sector_Particle.replace('s', 'S')}tor_Dependence_" if(Use_Sectors_Q) else "",
                        f"Plot_of_{HistoType}_",
                        "Bin"    if("Bin" in Correction_Type) else "Bayes", "_Corrected_",
                        "CosPhi" if("B"   in Parameter)       else "Cos2Phi",
                        f"_vs_{Variable_to_plot_against}_in_{Q2_or_y_Group}_Bin_{group_num}",
                        f"_{Save_Name_Extra}"     if(Save_Name_Extra not in [""]) else "",
                        f"_{Comparison_Type}.png" if(Comparison_Type not in [""]) else ".png"])
                    if(Saving_Q):
                        canvas[key_row_base].SaveAs(Save_Name)
                        print(f"\n{color.BBLUE}Saved: {color.UNDERLINE}{Save_Name}{color.END}\n")
                    else:
                        print(f"\n{color.RED}Did NOT save: {color.BOLD}{color.UNDERLINE}{Save_Name}{color.END}\n")
    
        canvas[key_names].cd()
        Moment_Title = f"Cos({'2' if('C' in str(Parameter)) else ''}#phi_{{h}})"
        Multigraph_Title_Line_1 = f"Plot of {Moment_Title} vs {variable_Title_name(Variable_to_plot_against)}"
        if("Tagged_Proton" in Save_Name_Extra):
            Multigraph_Title_Line_2 = f"{root_color.Bold}{{Tagged Proton}} #topbar #color[{root_color.Blue}]{{{Correction_Type}}}"
        elif("ProtonCut"   in Save_Name_Extra):
            Multigraph_Title_Line_2 = f"{root_color.Bold}{{Cut on Proton MM}} #topbar #color[{root_color.Blue}]{{{Correction_Type}}}"
        else:
            Multigraph_Title_Line_2 = f"#color[{root_color.Blue}]{{{Correction_Type}}}"
        if(HistoType in ["3D", "5D"]):
            Multigraph_Title_Line_2 = Multigraph_Title_Line_2.replace(f"{{{Correction_Type}}}", f"{{Multidimensional {HistoType} {Correction_Type}}}")
        if(Comparison_Type in [""]):
            mg[key_names].SetTitle(f"#splitline{{{Multigraph_Title_Line_1}}}{{{Multigraph_Title_Line_2}}}; {variable_Title_name(Variable_to_plot_against)}; {Moment_Title}")
        else:
            mg[key_names].SetTitle(f"#splitline{{#splitline{{{Multigraph_Title_Line_1}}}{{{Multigraph_Title_Line_2}}}}}{{{Comparison_Type.replace('_', ' ')}}}; {variable_Title_name(Variable_to_plot_against)}; {Moment_Title}")
    
        mg[key_names].Draw("A")
        # mg[key_names].GetYaxis().SetRangeUser(-0.35 if("C" in str(Parameter)) else -0.9, 0.25 if("C" in str(Parameter)) else 0.2)
        # mg[key_names].GetYaxis().SetRangeUser(-0.2 if("C" in str(Parameter)) else -0.3, 0.1 if("C" in str(Parameter)) else 0.1)
        # mg[key_names].GetYaxis().SetRangeUser(-0.15 if("C" in str(Parameter)) else -0.25, 0.1 if("C" in str(Parameter)) else 0.05)
        mg[key_names].GetYaxis().SetRangeUser(-0.25, 0.1)
        legend[key_names].Draw()
        canvas[key_names].Modified()
        canvas[key_names].Update()
        draw_annotations(annotations2)

        Save_Name = "".join([
            f"{Sector_Particle.replace('s', 'S')}tor_Dependence_" if(Use_Sectors_Q) else "",
            f"Plot_of_{HistoType}_",
            "Bin"    if("Bin" in Correction_Type) else "Bayes", "_Corrected_",
            "CosPhi" if("B"   in Parameter)       else "Cos2Phi",
            f"_vs_{Variable_to_plot_against}_in_{Q2_or_y_Group}_Bin_Groups",
            f"_{Save_Name_Extra}"     if(Save_Name_Extra not in [""]) else "",
            f"_{Comparison_Type}.png" if(Comparison_Type not in [""]) else ".png"])

        if(Saving_Q):
            canvas[key_names].SaveAs(Save_Name)
            print(f"\n{color.BBLUE}Saved: {color.UNDERLINE}{Save_Name}{color.END}\n")
        else:
            print(f"\n{color.RED}Did NOT save: {color.BOLD}{color.UNDERLINE}{Save_Name}{color.END}\n")

    print("Done running Plot_Fit_Parameter_ShadedSectorGraphs(...)\n")
    
    # Add canvases to ROOT's global list
    ROOT.gROOT.GetListOfCanvases().AddAll(root_objects)
    
    return canvas


def Create_Moment_Plots_From_txt_File(file_path, verbose=False, print_file_flag=False, print_table_flag=False, Correction="Both", 
                                      Parameter_In="Both", Smear_In="Both", HistoType="1D", SectorType="esec", Q2_y_Bin="Default",
                                      z_pT_Bin="Default", No_Save=False, Use_Sector_Shading=True, file_path_compare=None, Group_Images=False):

##################################################################################################################
##==========##==========##             Loading File             ##==========##==========##==========##==========##
##################################################################################################################
    file_content = ""
    # Use glob to find all files matching the pattern
    matched_files = glob.glob(file_path)
    if(not matched_files):
        print(f"{color.Error}Error: No files found matching path: {file_path}{color.END}")
        sys.exit(1)

    for files_path in matched_files:
        with open(files_path, 'r') as file:
            file_content += file.read()
            if(verbose):
                print(f"{color.BOLD}File: {color.BLUE}{files_path}{color.END_B} has been found (and added)...{color.END}")

    Pass_Version = "Pass 1"
    if(any(tag in str(file_path) for tag in ["Pass_2", "P2"])):
        Pass_Version = "Pass 2"

    file_name = file_path.split("/")[1] if("/" in file_path) else file_path
    Cut_Proton_Q    = ("_ProtonCut" in file_name)
    Tagged_Proton_Q = ("Tagged_Proton" in file_name) and not Cut_Proton_Q

    file_content = file_content.replace(f"This information is from {color.BOLD}{Pass_Version}{color.END}", "")
    file_content = file_content.replace("""
Note to Reader: Print the text in this file as a string in Python for the best formatting...


""", "")

    file_content_compare = ""
    if(file_path_compare):
        matched_files_compare = glob.glob(file_path_compare)
        if(not matched_files_compare):
            print(f"{color.Error}Error: No files found matching the compare path: {file_path_compare}{color.END}")
            sys.exit(1)
    
        for files_path in matched_files_compare:
            with open(files_path, 'r') as file:
                file_content_compare += file.read()
                if(verbose):
                    print(f"{color.BOLD}File: {color.BLUE}{files_path}{color.END_B} has been found (and added to comparison)...{color.END}")
    
        file_name_compare = file_path_compare.split("/")[1] if("/" in file_path_compare) else file_path_compare
        Cut_Proton_C    = ("_ProtonCut"    in file_name_compare)
        Tagged_Proton_C = ("Tagged_Proton" in file_name_compare) and not Cut_Proton_C
    
        file_content_compare = file_content_compare.replace(f"This information is from {color.BOLD}{Pass_Version}{color.END}", "")
        file_content_compare = file_content_compare.replace("""
Note to Reader: Print the text in this file as a string in Python for the best formatting...


""", "")
    else:
        file_name_compare = ""
        Cut_Proton_C, Tagged_Proton_C = False, False
        

    if(verbose):
        print(f"\n{color.BOLD}Pass Version in use   = {color.UNDERLINE}{color.BLUE}{Pass_Version}{color.END}\n")
        print(f"{color.BOLD}Using Tagged Proton? -> {color.UNDERLINE}{color.BLUE}{Tagged_Proton_Q}{color.END}\n")
        print(f"{color.BOLD}Using Proton Cut?    -> {color.UNDERLINE}{color.BLUE}{Cut_Proton_Q}{color.END}\n")
        print(f"\n{color.BOLD}'file_content'{color.END} has been updated\n")
        if(file_path_compare):
            print(f"{color.BGREEN}Comparing to File: {file_name_compare}{color.END}")
            print(f"{color.BGREEN}Comparison Type: {color.END_B}To {'Tagged Proton' if(Tagged_Proton_C) else 'Proton Cut' if(Cut_Proton_C) else 'Other File'}{color.END}\n")

    if(print_file_flag):
        print("\n\n===== File Content Start =====\n")
        print(file_content)
        print("\n===== File Content End =====\n")
        sys.exit(0)

##################################################################################################################
##==========##==========## File has been loaded and file_content is defined ##==========##==========##==========##
##################################################################################################################
##==========##==========##      Defining Search Functions       ##==========##==========##==========##==========##
##################################################################################################################
    def find_bin_block(data, bin_info, multi_search=False):
        blocks = re.split(r"==+\n", data)
        if(not multi_search):
            for block in blocks:
                if(bin_info in block):
                    if((("SMEARED" in bin_info) and ("SMEARED" in block)) or (("SMEARED" not in bin_info) and ("SMEARED" not in block))):
                        return f"\n======================================================================\n{block.strip()}\n======================================================================\n"
            return "No data found for the specified Q2-y/z-PT Bin."
        else:
            matching_blocks = []
            for block in blocks:
                if(bin_info in block):
                    if((("SMEARED" in bin_info) and ("SMEARED" in block)) or (("SMEARED" not in bin_info) and ("SMEARED" not in block))):
                        matching_blocks.append(f"\n======================================================================\n{block.strip()}\n======================================================================\n")
            return matching_blocks if(matching_blocks) else ["No data found for the specified Q2-y/z-PT Bin."]
    
    def extract_histogram_info(block, histogram_type):
        pattern = rf"\(\*\) {re.escape(histogram_type)} Histograms:(.*?)(?=\(\*\)|$)"
        match = re.search(pattern, block, re.DOTALL)
        if(match):
            return match.group(1).strip()
        else:
            return "No data found for the specified histogram type."
    
    def extract_fit_info(block, fit_type):
        pattern = rf"- {re.escape(fit_type)} Fits:.*?(\n\s+Par A.*?chi2/NDF = \S+)"
        match = re.search(pattern, block, re.DOTALL)
        if(match):
            return f"\n{match.group(1).strip()}"
        else:
            return "No fit details found for the specified type."
    
    def find_parameter(block, parameter, return_err=False):
        for line in block.split("\n"):
            if(parameter in line):
                try:
                    _, par_info = line.split("=")
                    par_val, par_err = map(str.strip, par_info.split("±"))
                    return (par_val, par_err) if(return_err) else par_val
                except ValueError:
                    continue
        return ("ERROR", "ERROR") if(return_err) else "ERROR"
    
    def Full_Search_Parameter(Parameter_File_str, Bin_Info=False, Histogram_Type=False, Fit_Type=False, Parameter=False, return_err=False, multi_search=True):
        if(not Bin_Info):
            print("No kinematic bin given")
            return Parameter_File_str
        if(multi_search):
            blocks = find_bin_block(Parameter_File_str, Bin_Info, multi_search=True)
            for block in blocks:
                if(Histogram_Type and Histogram_Type != "Skip"):
                    histogram_data = extract_histogram_info(block, Histogram_Type)
                    if("No data found" in histogram_data):
                        continue  # Skip to the next block if Histogram_Type not found
                    block = histogram_data
                if(Fit_Type):
                    fit_data = extract_fit_info(block, Fit_Type)
                    if("No fit details found" in fit_data):
                        return ("ERROR", "ERROR") if(return_err) else "ERROR"
                    block = fit_data
                if(Parameter):
                    parameter_data = find_parameter(block, Parameter, return_err)
                    # Ensure the correct structure is returned
                    if(return_err):
                        return (parameter_data if(isinstance(parameter_data, tuple)) else (parameter_data, "ERROR"))
                    return parameter_data
                return block
            return ("ERROR", "ERROR") if(return_err) else "No data found for the specified criteria."
        else:
            block = find_bin_block(Parameter_File_str, Bin_Info)
            if(not Histogram_Type):
                print("No histogram given")
                return block
            if(Histogram_Type != "Skip"):
                block = extract_histogram_info(block, Histogram_Type)
                if("No data found" in block):
                    return ("ERROR", "ERROR") if(return_err) else block
            if(Fit_Type):
                block = extract_fit_info(block, Fit_Type)
                if "No fit details found" in block:
                    return ("ERROR", "ERROR") if(return_err) else block
            if(Parameter):
                parameter_data = find_parameter(block, Parameter, return_err)
                return (parameter_data if(isinstance(parameter_data, tuple)) else (parameter_data, "ERROR")) if(return_err) else parameter_data
    
        return block
##################################################################################################################
##==========##==========##      Defined Search Functions        ##==========##==========##==========##==========##
##################################################################################################################
    Q2_y_Bin = int(Q2_y_Bin) if(Q2_y_Bin not in ["Default", "All", "Integrated"]) else Q2_y_Bin
    z_pT_Bin = int(z_pT_Bin) if(z_pT_Bin not in ["Default", "All", "Integrated"]) else z_pT_Bin
    Q2_y_Bin_Range   = range(1, 18)     if(Q2_y_Bin     in ["Default"]) else [Q2_y_Bin]     if(Q2_y_Bin     in ["All"] + list(range(0, 18))) else "Error"
    Correction_List  = ["Bin", "Bayes"] if(Correction   in ["Both"])    else [Correction]   if(Correction   in ["Bin", "Bayes"])             else "Error"
    Parameter_List   = ["B", "C"]       if(Parameter_In in ["Both"])    else [Parameter_In] if(Parameter_In in ["B", "C"])                   else "Error"
    Smear_List       = ["SMEARED ", ""] if(Smear_In     in ["Both"])    else ["SMEARED "]   if(Smear_In     in ["Smear", "smear"])           else [""]    if(Smear_In in ["Unsmeared", "no_smear", "no"]) else "Error"
    Histo_Type_to_Compare = [HistoType]
    Files_To_Compare = [file_content, file_content_compare] if(file_path_compare) else [file_content]
    for sec in range(1, 7):
        Histo_Type_to_Compare.append(f"{HistoType} ({SectorType} {sec})")
    if(verbose or ("Error" in [Q2_y_Bin_Range, Correction_List, Parameter_List, Smear_List])):
        print("")
        print(f"Q2-y Bin(s)     to be run: {Q2_y_Bin_Range}")
        if(z_pT_Bin not in ["Default"]):
            print(f"z-pT Bin        to be run: {z_pT_Bin}")
        print(f"Correction(s)   to be run: {Correction_List}")
        print(f"Parameter(s)    to be run: {Parameter_List}")
        print(f"Smear Type(s)   to be run: {Smear_List}")
        if("Error" not in [Q2_y_Bin_Range, Correction_List, Parameter_List, Smear_List]):
            print(f"Histogram Types to be run: {Histo_Type_to_Compare}")
        else:
            print(f"{color.Error}Error in arguments!{color.END}\n")
            sys.exit(0)
        print(f"Running {color.BOLD}{len(Files_To_Compare)}{color.END} File(s)")
        print("")

    Comparison_Output = {}
    for File_Num, File_Content          in enumerate(Files_To_Compare):
        for Smear_Type                  in Smear_List:
            for Correction_Type         in Correction_List:
                Fit___Type              =  "Bin-by-Bin Correction" if(Correction_Type in ["Bin"]) else "Bayesian Unfolding"
                if(print_table_flag):
                    if(File_Num == 0):
                        Comparison_Output[f"Title_Info_({Correction_Type})_({Smear_Type})"] = f"{Smear_Type}{Fit___Type} Results"
                    else:
                        Comparison_Output[f"Title_Info_(File_{File_Num+1})_({Correction_Type})_({Smear_Type})"] = f"{Smear_Type}{Fit___Type} Results (from File {File_Num+1})"
                    if("Title" not in Comparison_Output):
                        Comparison_Output_Title = ["Q2-y-z-PT Bin", "Fit Parameter"]
                        for compare in Histo_Type_to_Compare:
                            Comparison_Output_Title.append(compare)
                            Comparison_Output_Title.append(f"{compare} Error")
                        Comparison_Output["Title"] = Comparison_Output_Title
                        del Comparison_Output_Title
                for Q2_y_Bin_ii             in Q2_y_Bin_Range:
                    z_pT_Bin_Range          =  range(-1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_ii)[1] + 1) if(z_pT_Bin in ["Default"]) else [z_pT_Bin]
                    for z_pT_Bin_ii         in z_pT_Bin_Range:
                        if(z_pT_Bin_ii      in [-1]):
                            z_pT_Bin_ii     =  "Integrated"
                        elif(z_pT_Bin_ii    in [0]):
                            z_pT_Bin_ii     =  "All"
                        elif(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_ii, Z_PT_BIN=z_pT_Bin_ii, BINNING_METHOD="Y_bin")):
                            continue
                        Bin___Type          =  f"{Smear_Type}Q2-y Bin {Q2_y_Bin_ii} - z-PT Bin {z_pT_Bin_ii}"
                        for Par___Type      in Parameter_List:
                            if(print_table_flag):
                                Line_to_Add =  [f"Bin {Q2_y_Bin_ii}-{z_pT_Bin_ii}", f"Parameter {Par___Type}"]
                            for Histo_Type  in Histo_Type_to_Compare:
                                Moment_Value_val, Moment_Value_err = Full_Search_Parameter(Parameter_File_str=File_Content, Bin_Info=Bin___Type, Histogram_Type=Histo_Type, Fit_Type=Fit___Type, Parameter=Par___Type, return_err=True)
                                if(Moment_Value_val  not in ["ERROR"]):
                                    Moment_Value_val =   round(float(Moment_Value_val), 9)
                                if(Moment_Value_err  not in ["ERROR"]):
                                    Moment_Value_err =   round(float(Moment_Value_err), 9)
                                Key_For_Compare      = f"(Q2-y-z-pT Bin '{Q2_y_Bin_ii}-{z_pT_Bin_ii}')_(Parameter {Par___Type})_(Correction '{Correction_Type}')_{Histo_Type.replace(' ', '_')}"
                                if(File_Num != 0):
                                    Key_For_Compare  = f"(File_{File_Num+1})_{Key_For_Compare}"
                                # if(verbose):
                                #     print(f"{Key_For_Compare} -> {Moment_Value_val} ± {Moment_Value_err}")
                                if(print_table_flag):
                                    Line_to_Add.append(Moment_Value_val)
                                    Line_to_Add.append(Moment_Value_err)
                                else:
                                    Comparison_Output[Key_For_Compare] = [Moment_Value_val, Moment_Value_err]
                            if(print_table_flag):
                                if(File_Num == 0):
                                    Comparison_Output[f"Par {Par___Type} - ({Q2_y_Bin_ii}, {z_pT_Bin_ii})"] = Line_to_Add
                                else:
                                    Comparison_Output[f"File {File_Num+1} - Par {Par___Type} - ({Q2_y_Bin_ii}, {z_pT_Bin_ii})"] = Line_to_Add
                                    
    if(print_table_flag):
        for ii in Comparison_Output:
            Line_Info = Comparison_Output[ii]
            if("Title_Info_" in ii):
                print("==========================================================================================================================================")
                print(f"{color.BBLUE}{Line_Info}{color.END}")
                Line_Info = ["{:>18}".format(str(item)) for item in Comparison_Output["Title"]]
                print("  ||".join(Line_Info))
            else:
                Line_Info = ["{:>18}".format(str(item)) for item in Comparison_Output[ii]]
                print("  ||".join(Line_Info))
        sys.exit(0)
    # elif(verbose):
    #     for ii in Comparison_Output:
    #         print(f"Comparison_Output[{ii}] = {Comparison_Output[ii]}")

    dump_canvas = {}
    if((Q2_y_Bin in ["Default"]) and (Smear_In not in ["Both"])):
        for Fit___Type in Correction_List:
            Correction_Type=  "Bin-by-Bin Correction"       if(Correction_Type in  ["Bin"]) else "Bayesian Unfolding"
            Parameter_List = ["Parameter B", "Parameter C"] if(Parameter_In    in ["Both"]) else [f"Parameter {Parameter_In}"]
            # for     Group_Variable in ["y", "Q2", "xB"]:
            for     Group_Variable in ["y", "Q2"]:
                if(verbose):
                    print(f"Group_Variable = {Group_Variable}")
                for Plot__Variable in ["y", "Q2", "xB"]:
                    if(Group_Variable == Plot__Variable):
                        continue
                    if((Group_Variable in ["xB"]) and (Plot__Variable not in ["Q2"])):
                        continue
                    if(verbose):
                        print(f"Plot__Variable = {Plot__Variable}\n")
                    dump_canvas[f"{Fit___Type}_{Group_Variable}_{Plot__Variable}"] = Plot_Fit_Parameter_ShadedSectorGraphs(Fit_Parameters_Input=Comparison_Output, 
                                                                                                                           From_Python_or_Text="Python",
                                                                                                                           Q2_or_y_Group=Group_Variable,
                                                                                                                           Variable_to_plot_against=Plot__Variable,
                                                                                                                           Use_Sectors_Q=Use_Sector_Shading,
                                                                                                                           Parameter_List=Parameter_List, 
                                                                                                                           Correction_Type=Correction_Type,
                                                                                                                           Sector_Particle=SectorType,
                                                                                                                           Saving_Q=not No_Save,
                                                                                                                           Save_Name_Extra="ProtonCut" if(Cut_Proton_Q) else "Tagged_Proton" if(Tagged_Proton_Q) else "",
                                                                                                                           HistoType=HistoType,
                                                                                                                           Comparison_Info=[len(Files_To_Compare), Tagged_Proton_C, Cut_Proton_C],
                                                                                                                           Group_Images_Q=Group_Images)
    return [file_content, dump_canvas]


if(__name__ == "__main__"):
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run SIDIS Analysis Script with configurable options.")
    parser.add_argument("-i",   "--input",         help="Optional path to input file. If not provided, default path will be used.",                                 default='Parameters_Pass_2_Sector_Integrated_Tests_FC_14_V2_5_12_2025_Q2_y_Bins_Combined_Smeared.txt')
    parser.add_argument("-ic",  "--input_compare", help="Optional path to second input file for comparing to default file.",                                        default=None)
    parser.add_argument("-p",   "--print_file",    help="If set, print file content and exit.",                                                                     action="store_true")
    parser.add_argument("-pt",  "--print_table",   help="If set, print file content in a table and exits (output is similar to the Notebook's Cell).",              action="store_true")
    parser.add_argument("-v",   "--verbose",       help="If NOT set, code will run quietly (does not effect '-p' option).",                                         action="store_true")
    parser.add_argument("-c",   "--correction",    help="Set Correction Type (Options: 'Bin' and 'Bayes').",                                                        default="Both")
    parser.add_argument("-par", "--parameter",     help="Set Parameter/Cosine Moment Plots (Options: 'B' for 'Cos(phi)' and 'C' for 'Cos(2phi)').",                 default="Both")
    # parser.add_argument("-s",   "--smear",         help="Set Smear Type (Options: 'Smear'/'smear' and 'Unsmeared'/'no_smear'/'no').",                               default="Both")
    parser.add_argument("-s",   "--smear",         help="Set Smear Type (Options: 'Smear'/'smear' and 'Unsmeared'/'no_smear'/'no').",                               default="Smear")
    parser.add_argument("-hist","--histogram",     help="Set Histogram Type (Options: '1D'/'3D').",                                                                 default="3D")
    parser.add_argument("-sec", "--sector",        help="Set Sector Type (Options: 'pipsec' for pion sectors OR 'esec' for electron sectors).",                     default="esec")
    parser.add_argument("-q2y", "--Q2_y_Bin",      help="Set individual Q2-y Bin to run (Defaults to running all 17 bins).",                                        default="Default")
    parser.add_argument("-zpT", "--z_pT_Bin",      help="Set individual z-pT Bin to run (Defaults to running all bins, including the 'All'/'Integrated' options).", default="Default")
    parser.add_argument("-nS",  "--no_save",       help="If set, the code will not save any of the images it makes (used for testing).",                            action="store_true")
    parser.add_argument("-us", "--use_sectors",    help="If set, the code will show the sector information when plotting.",                                         action="store_true")
    parser.add_argument("-gi", "--group_images",   help="If set, the code will create individual image outputs for each kinematic group added to the main image. (Not currently working)",  action="store_true")
    
    args = parser.parse_args()

    
    print(f"{color.BOLD}\nStarting Create_Moment_Plots_From_txt_File.py\n{color.END}")

    if(args.group_images):
        print(f"{color.BGREEN}\n\nWILL BE CREATING MULTIPLE IMAGES FOR EACH GROUP{color.END}\n\n")

    
    # Run the main file processing function
    info_returned = Create_Moment_Plots_From_txt_File(args.input, verbose=args.verbose,
                                                      print_file_flag=args.print_file, print_table_flag=args.print_table,
                                                      Correction=args.correction, Parameter_In=args.parameter,
                                                      Smear_In=args.smear, HistoType=args.histogram,
                                                      SectorType=args.sector, Q2_y_Bin=args.Q2_y_Bin, z_pT_Bin=args.z_pT_Bin,
                                                      No_Save=args.no_save, Use_Sector_Shading=(args.use_sectors),
                                                      file_path_compare=args.input_compare,
                                                      Group_Images=args.group_images)
    # del info_returned
    
    print("\nEnd of Create_Moment_Plots_From_txt_File.py Code\n")
    ROOT.gROOT.GetListOfCanvases().Clear()
    sys.exit(0)
    