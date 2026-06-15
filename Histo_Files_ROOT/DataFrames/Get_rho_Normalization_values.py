#!/usr/bin/env python3

import ROOT
# import cppyy
import sys
import numpy as np
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, RuntimeTimer, Draw_Canvas, silence_root_import, Canvas_Create, Get_Num_of_z_pT_Rows_and_Columns, Draw_Q2_Y_Bins, Draw_the_MM_Cut_Lines, Draw_z_pT_Bins_With_Migration, Get_Num_of_z_pT_Bins_w_Migrations, skip_condition_z_pT_bins, variable_Title_name #, root_color, color_bg
from Binning_Dictionaries             import Bin_Converter_4D_to_2D #, Full_Bin_Definition_Array
sys.path.remove(script_dir)
del script_dir
import argparse
from datetime import datetime

Name_of_Script = "Get_rho_Normalization_values.py"
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"{Name_of_Script}: Gets Normalization Parameters for Harut's rho0 files based on input histograms from pre-made ROOT files.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-V', '--verbose',
                        action='store_true',
                        help="Print verbosely.\n")
    parser.add_argument('-f1', '--file1',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V8_z_Bins_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V7_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V5_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V3_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Dynamic_W_pim_cut_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_New_Dynamic_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho_Normalizer_Default_rho_Final_Analysis_Iterations_I0_All.root',
                        help='Path to the ROOT file which contains the required clasdis/data histograms (without rho0).\n')
    parser.add_argument('-f2', '--file2',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V8_Diagnostics_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V6_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V5_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V3_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Dynamic_W_pim_cut_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_New_Dynamic_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho_Normalizer_Default_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho_Normalizer_Default_rho_Final_Analysis_Iterations_I0_Batch170.root',
                        help="Path to the ROOT file which contains the required histograms with Harut's rho0 events (requires rho0).\n")
    parser.add_argument('-usf', '--use_same_file',
                        action='store_true',
                        help="If provided, code will default to just using histograms from '--file1'.\n")
    parser.add_argument('-ns', '--no_save',
                        action='store_true',
                        help='If provided, skip all drawing and file-saving steps.\n')
    parser.add_argument('-ff', '--file_format',
                        default='PDF',
                        choices=['PDF', 'PNG'],
                        help='Controls the saved image format.\n')
    parser.add_argument('-n', '--name',
                        default='',
                        help='Optionally adds a user-provided string to the default output image names.\n')
    parser.add_argument('-ti', '--title',
                        default='',
                        help='Optionally adds extra text to both histogram titles.\n')
    parser.add_argument('-xmin', '--x_min',
                        default=0.08,
                        type=float,
                        help='X-axis minimum (default 0.08/0).\n')
    parser.add_argument('-xmax', '--x_max',
                        default=0.68,
                        type=float,
                        help='X-axis maximum (default 0.68/1.8).\n')
    parser.add_argument('-ymin', '--y_min',
                        default=0.9,
                        type=float,
                        help='Y-axis minimum (default 0.9/-2).\n')
    parser.add_argument('-ymax', '--y_max',
                        default=8.5,
                        type=float,
                        help='Y-axis maximum (default 8.5/3).\n')
    parser.add_argument('-v', '--vars',
                        default='z1z2',
                        # default='Q2xB',
                        choices=['Q2xB', 'q2xb', 'z', 'z1z2', 'Wpions', 'Wp'],
                        help="Controls for which variables to use (either 'Q2 vs xB', 'z1+z2', or fitted 'Wpions').\n")
    parser.add_argument('-u2Dk', '--Use_2D_Kinematic_Binning',
                        action='store_true',
                        help="Uses the 'Q2_Y_Bin' binning instead of the 4D kinematic bins in the 'Wpions' fit mode.\n")
    parser.add_argument('-uzb', '--use_z_bins',
                        action='store_true',
                        help="Uses the 'z_Bins' binning instead of the 4D kinematic bins in the 'Wpions' fit mode.\n")
    parser.add_argument('-ol', '--old_lund',
                        action='store_true',
                        help="Use Harut's old files instead of the newer ones.\n")
    parser.add_argument('-dm', '--draw_mode',
                        default='auto',
                        choices=['auto', '2D', '1D', '1D_dif'],
                        help="Drawing mode. 'auto' chooses based on --vars (Q2xB=2D, z-modes=1D by default).\n\t'1D_dif' draws 1D histograms, but to different canvases (like the '2D' mode).\n")
    parser.add_argument('-ztc', '--z_tot_cut',
                        default=0.9,
                        type=float,
                        help='(Exclusive) Normalization cut for z_tot.\n')
    parser.add_argument('-ztcs', '--z_tot_cut_SIDIS',
                        default=0.6,
                        type=float,
                        help='(SIDIS) Normalization cut for z_tot.\n')
    parser.add_argument('-subbkg', '--subtract_background',
                        action='store_true',
                        help="Subtracts SIDIS background (modeled by normalized clasdis SIDIS) from the exclusive events in the experimental date.\n")
    parser.add_argument('-addbkg', '--add_background',
                        action='store_true',
                        help="Adds SIDIS background (modeled by normalized clasdis SIDIS) to Harut's exclusive events.\n")
    parser.add_argument('-ly', '--legacy',
                        action='store_true',
                        help="Run in legacy mode (use old binning and global normalization instead of per-kinematic-bin mode).\n")
    parser.add_argument('-kb', '--Kinematic_Bin_Select',
                        type=str,
                        default="Full",
                        help=f"Selects the 4D kinematic bin(s) to create weights/images for.\n{color.BOLD}Selecting 'Full' sums all bins using the binned weights while 'All' gives just one normalization factor for all (integrated) bins.{color.END}\nUses bin-axis information for individual bins — {color.RED}must convert between histogram bins and user bin definitions.{color.END}\n")
    parser.add_argument('-ers', '--extra_root_save',
                        action='store_true',
                        help="Saves the TH2D histograms as separate ROOT files for future use.\n")
    parser.add_argument('-rdwi', '--run_diagnostic_weight_images',
                        action='store_true',
                        help="Saves the diagnostic plots to show the comparative statistics between each kinematic bin in the data and MC after the normalization steps.\n")
    parser.add_argument('-rabdi', '--run_all_base_diagnostic_images',
                        action='store_true',
                        help="Saves the diagnostic plots to help show each stage of the procedure including the cuts and normalization evaluations (is separate from '--run_diagnostic_weight_images').\n")
    return parser.parse_args()


def variable_Title_name_new(variable_in):
    if(variable_in in ["k0_cut"]):
        return "E^{Cutoff}_{#gamma}"
    else:
        output = variable_Title_name(variable_in)
        output = output.replace(" (lepton energy loss fraction)", "")
        return output

def check_histo_for_errors(hist, name, file_name):
    if(not hist):
        print(f"\n{color.Error}ERROR: Could not load histogram '{name}' from '{file_name}'{color.END}\n")
        sys.exit(1)
    if(not hist.InheritsFrom("TH3")):
        print(f"\n{color.Error}ERROR: Loaded object '{name}' is not TH3-compatible (got {hist.ClassName()}){color.END}\n")
        sys.exit(1)

def Create_Images(args, Full_List_of_HistosB, Full_List_of_Factors, Kinematic_Bin="All", proj_data_full_for_plot=None):
    print(f"\n{color.BOLD}Setting up drawing style and saving histograms in images...{color.END}\n")
    suffix = f"_{args.name}" if(args.name) else ""
    fmt = args.file_format.lower()
    title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{SIDIS Region Cutoff was z_{{1}}+z_{{2}} < {args.z_tot_cut_SIDIS}}}}}"
    if(Kinematic_Bin in ["Full"]):
        suffix = f"{suffix}_Summed_Bins"
        hist_data_wbkg        = Full_List_of_HistosB["All"]["proj_data_exclz"].Clone("hist_data_wbkg_Full")
        hist_data_excl        = Full_List_of_HistosB["All"]["data_excl_subt"].Clone("hist_data_excl_Full")
        hist_data_sidis       = Full_List_of_HistosB["All"]["proj_data_SIDIS"].Clone("hist_data_sidis_Full")
        proj_data__1d         = proj_data_full_for_plot.ProjectionX("proj_y_1") if(proj_data_full_for_plot is not None) else hist_data_sidis
        # The data histograms above do not have individual binned weights (i.e., just use the 'All' bin)
        hist_clasdis_norm, hist_clasdis_excl, hist_clasdis_ebkg, proj_harut_1d, proj_harut_1d_norm, true_harut_1d = None, None, None, None, None, None
        Clone_Name = f'{Full_List_of_HistosB["All"]["proj_mdf_SIDIS"].GetName()}_norm'.replace("All", "Full")
        for Kinematic_Bin_ii in Full_List_of_HistosB:
            if(Kinematic_Bin_ii in ["All"]):
                continue
            if(hist_clasdis_norm is None):
                hist_clasdis_norm  = Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_SIDIS"].Clone(Clone_Name)
                hist_clasdis_norm.Scale(Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            else:
                hist_clasdis_norm.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_SIDIS"], Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            if(hist_clasdis_excl is None):
                hist_clasdis_excl  = Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_exclz"].Clone(f"hist_clasdis_excl_Full")
                hist_clasdis_excl.Scale(Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            else:
                hist_clasdis_excl.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_exclz"], Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            if(hist_clasdis_ebkg is None):
                hist_clasdis_ebkg  = Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_exbkg"].Clone(f"hist_clasdis_ebkg_Full")
                hist_clasdis_ebkg.Scale(Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            else:
                hist_clasdis_ebkg.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["proj_mdf_exbkg"], Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            if(proj_harut_1d     is None):
                proj_harut_1d      = Full_List_of_HistosB[Kinematic_Bin_ii]["proj_harut_excl"].Clone(f"proj_harut_1d_Full")
                proj_harut_1d_norm = proj_harut_1d.Clone(f"{proj_harut_1d.GetName()}_norm")
                proj_harut_1d_norm.Scale(Full_List_of_Factors[Kinematic_Bin_ii]["N_edf"])
            else:
                proj_harut_1d.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["proj_harut_excl"])
                proj_harut_1d_norm.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["proj_harut_excl"], Full_List_of_Factors[Kinematic_Bin_ii]["N_edf"])
            if(true_harut_1d     is None):
                true_harut_1d      = Full_List_of_HistosB[Kinematic_Bin_ii]["true_harut_excl"].Clone(f"true_harut_1d_Full")
                true_harut_1d.Scale(Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
            else:
                true_harut_1d.Add(Full_List_of_HistosB[Kinematic_Bin_ii]["true_harut_excl"], Full_List_of_Factors[Kinematic_Bin_ii]["N_sdf"])
        if(None not in [hist_clasdis_norm, proj_harut_1d_norm]):
            hist_combined = hist_clasdis_norm.Clone("hist_combined_1D_Binned_Full")
            hist_combined.Add(proj_harut_1d_norm)
    else:
        hist_data_wbkg        = Full_List_of_HistosB[Kinematic_Bin]["proj_data_exclz"].Clone(f"hist_data_wbkg_{Kinematic_Bin}")
        hist_data_excl        = Full_List_of_HistosB[Kinematic_Bin]["data_excl_subt"].Clone(f"hist_data_excl_{Kinematic_Bin}")
        hist_data_sidis       = Full_List_of_HistosB[Kinematic_Bin]["proj_data_SIDIS"].Clone(f"hist_data_sidis_{Kinematic_Bin}")
        if(proj_data_full_for_plot is not None):
            if(Kinematic_Bin in ["All"]):
                proj_data__1d = proj_data_full_for_plot.ProjectionX("proj_y_1")
            else:
                proj_data__1d = proj_data_full_for_plot.ProjectionX("proj_y_1", int(Kinematic_Bin), int(Kinematic_Bin))
        else:
            proj_data__1d     = hist_data_sidis
            if(Kinematic_Bin not in ["All"]):
                suffix        = f"{suffix}_Axis_Bin_{Kinematic_Bin}"
        hist_clasdis_norm     = Full_List_of_HistosB[Kinematic_Bin]["proj_mdf_SIDIS"].Clone(f'{Full_List_of_HistosB[Kinematic_Bin]["proj_mdf_SIDIS"].GetName()}_norm')
        hist_clasdis_norm.Scale(Full_List_of_Factors[Kinematic_Bin]["N_sdf"])
        hist_clasdis_excl     = Full_List_of_HistosB[Kinematic_Bin]["proj_mdf_exclz"].Clone(f"hist_clasdis_excl_{Kinematic_Bin}")
        hist_clasdis_excl.Scale(Full_List_of_Factors[Kinematic_Bin]["N_sdf"])
        hist_clasdis_ebkg     = Full_List_of_HistosB[Kinematic_Bin]["proj_mdf_exbkg"].Clone(f"hist_clasdis_ebkg_{Kinematic_Bin}")
        hist_clasdis_ebkg.Scale(Full_List_of_Factors[Kinematic_Bin]["N_sdf"])
        proj_harut_1d         = Full_List_of_HistosB[Kinematic_Bin]["proj_harut_excl"].Clone(f"proj_harut_1d_{Kinematic_Bin}")
        proj_harut_1d_norm    = proj_harut_1d.Clone(f"{proj_harut_1d.GetName()}_norm")
        proj_harut_1d_norm.Scale(Full_List_of_Factors[Kinematic_Bin]["N_edf"])
        true_harut_1d         = Full_List_of_HistosB[Kinematic_Bin]["true_harut_excl"].Clone(f"true_harut_1d_{Kinematic_Bin}")
        true_harut_1d.Scale(Full_List_of_Factors[Kinematic_Bin]["N_sdf"])
        hist_combined         = hist_clasdis_norm.Clone(f"hist_combined_1D_Binned_{Kinematic_Bin}")
        hist_combined.Add(proj_harut_1d_norm)

    proj_harut_1d.SetLineColor(ROOT.kCyan+3)
    proj_harut_1d.SetLineWidth(1)
    proj_harut_1d.SetLineStyle(2)
    Kinematic_Bin_Number = Kinematic_Bin
    if(proj_data_full_for_plot is not None):
        if(Kinematic_Bin not in ["All", "Full"]):
            Kinematic_Bin_Number = proj_data_full_for_plot.GetYaxis().GetBinCenter(int(Kinematic_Bin))
            # title  = f"#splitline{{{title}}}{{4D Kinematic Bin: {int(Kinematic_Bin_Number)}}}"
            suffix = f"{suffix}_Bin_{int(Kinematic_Bin_Number)}" if("_Bin_" not in suffix) else suffix
        else:
            suffix = f"{suffix}_Bin_{Kinematic_Bin_Number}" if("_Bin_" not in suffix) else suffix
        if(Kinematic_Bin_Number not in [None, "All", Kinematic_Bin]):
            title = f"#splitline{{{title}}}{{#scale[0.75]{{4D Kinematic Bin: {int(Kinematic_Bin_Number)}}}}}"
        elif(Kinematic_Bin not in ["All", "Full"]):
            title = f"#splitline{{{title}}}{{#scale[0.75]{{4D Kinematic Bin (Histogram Axis Def): {int(Kinematic_Bin)}}}}}"
        elif(Kinematic_Bin     in ["Full"]):
            title = f"#splitline{{{title}}}{{#scale[0.75]{{#splitline{{4D Kinematic Bin: {Kinematic_Bin}}}{{#scale[0.75]{{Used Sum of Weighted Histograms}}}}}}}}"
        else:
            title = f"#splitline{{{title}}}{{#scale[0.75]{{All 4D Kinematic Bin}}}}"
        proj_data__1d.SetLineColor(ROOT.kRed)
        proj_data__1d.SetLineWidth(2)
        proj_data__1d.SetTitle(f"#splitline{{{title}}}{{{args.title}}}")

    hist_data_wbkg.SetLineColor(ROOT.kOrange)
    hist_data_wbkg.SetLineWidth(2)
    # hist_data_wbkg.SetLineStyle(1)
    hist_data_wbkg.SetLineStyle(2)
    
    hist_data_excl.SetLineColor(ROOT.kRed)
    hist_data_excl.SetLineWidth(2)
    hist_data_excl.SetLineStyle(1)

    hist_data_sidis.SetLineColor(ROOT.kCyan)
    hist_data_sidis.SetLineWidth(2)
    hist_data_sidis.SetLineStyle(2)
    
    proj_harut_1d_norm.SetLineColor(ROOT.kGreen)
    proj_harut_1d_norm.SetLineStyle(1)
    proj_harut_1d_norm.SetLineWidth(3)

    hist_clasdis_norm.SetLineColor(ROOT.kBlue)
    hist_clasdis_norm.SetLineWidth(2)

    hist_clasdis_excl.SetLineColor(ROOT.kBlack)
    hist_clasdis_excl.SetLineWidth(1)
    hist_clasdis_excl.SetLineStyle(2)

    hist_clasdis_ebkg.SetLineColor(ROOT.kOrange+2)
    hist_clasdis_ebkg.SetLineWidth(2)
    hist_clasdis_ebkg.SetLineStyle(1)

    hist_combined.SetLineColor(ROOT.kMagenta)
    hist_combined.SetLineWidth(2)
    hist_combined.SetLineStyle(1)

    true_harut_1d.SetLineColor(ROOT.kPink+2)
    true_harut_1d.SetLineWidth(1)
    true_harut_1d.SetLineStyle(2)

    for hist_loop in [proj_data__1d, hist_clasdis_norm, proj_harut_1d, true_harut_1d, proj_harut_1d_norm, hist_combined, hist_data_excl, hist_data_wbkg, hist_data_sidis, hist_clasdis_excl]:
        hist_loop.GetXaxis().SetRangeUser(max([args.x_min, 0.1]), args.x_max)
        # hist_loop.GetXaxis().SetRangeUser(0.8, 1.05)

    out_file = f"Plot_of_{args.vars}_for_rho0_Norm_Combined_1D{suffix}.{fmt}"
    canvas = ROOT.TCanvas("c_combined", "", 900, 700)
    canvas.Divide(2, 1, 0.0001, 0.0001)
    canvas.SetGrid()
    ROOT.gStyle.SetAxisColor(16, 'xy')
    ROOT.gStyle.SetOptStat(0)
    Draw_Canvas(canvas, 1, left_add=0.125, right_add=0.025, up_add=0.1, down_add=0.075)
    y_max_cutoff = max([hist_clasdis_norm.GetMaximum(), hist_data_sidis.GetMaximum(), hist_clasdis_excl.GetMaximum()])
    # ROOT.gPad.SetLogy(1)
    # proj_data__1d.Draw("hist")
    hist_clasdis_norm.SetTitle(proj_data__1d.GetTitle())
    hist_clasdis_norm.GetXaxis().SetTitle(str(hist_clasdis_norm.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    hist_clasdis_norm.GetYaxis().SetRangeUser(0, 1.05*y_max_cutoff)
    hist_clasdis_norm.Draw("hist same")
    # hist_combined.Draw("hist same")
    hist_data_sidis.Draw("hist same")
    # proj_harut_1d_norm.Draw("hist same")
    # # hist_data_excl.Draw("hist same")
    # hist_data_wbkg.Draw("hist same")
    hist_clasdis_excl.Draw("hist same")
    # hist_clasdis_ebkg.Draw("hist same")

    Cutoff_Line  = ROOT.TLine(args.z_tot_cut_SIDIS, 0.0, args.z_tot_cut_SIDIS, y_max_cutoff)
    Cutoff_Line.SetLineColor(ROOT.kGray+3)
    Cutoff_Line.SetLineStyle(1)
    Cutoff_Line.SetLineWidth(2)
    Cutoff_Line.Draw("same")
    
    legend_cd_1 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
    legend_cd_1.SetFillStyle(0)
    legend_cd_1.SetBorderSize(0)
    # # legend_cd_1.AddEntry(proj_data__1d,     "#scale[1.5]{Experimental Data (Full)}",                  "l")
    # # legend_cd_1.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized)}",                 "l")
    legend_cd_1.AddEntry(hist_data_sidis,   "#scale[0.75]{#splitline{Experimental Data}{(SIDIS)}}",                 "l")
    legend_cd_1.AddEntry(hist_clasdis_norm, "#scale[0.75]{#splitline{clasdis SIDIS}{(Normalized)}}",                "l")
    legend_cd_1.AddEntry(hist_clasdis_excl, "#scale[0.75]{#splitline{clasdis Exclusive #rho^{0}}{(Normalized)}}",   "l")
    legend_cd_1.Draw("same")
    # canvas.cd(2)
    Draw_Canvas(canvas, 2, left_add=0.095, right_add=0.025, up_add=0.1, down_add=0.075)
    # Shared_Title = proj_data__1d.GetTitle()
    Shared_Title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}}}"
    Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}}}"
    if(Kinematic_Bin_Number not in [None, "All", Kinematic_Bin]):
        Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{4D Kinematic Bin: {int(Kinematic_Bin_Number)}}}}}"
    elif(Kinematic_Bin not in ["All", "Full"]):
        Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{4D Kinematic Bin (Histogram Axis Def): {int(Kinematic_Bin)}}}}}"
    elif(Kinematic_Bin     in ["Full"]):
        Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{#splitline{{4D Kinematic Bin: {Kinematic_Bin}}}{{#scale[0.75]{{Used Sum of Weighted Histograms}}}}}}}}"
    else:
        Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{All 4D Kinematic Bin}}}}"
    hist_clasdis_excl.SetTitle(Shared_Title)
    hist_clasdis_excl.GetXaxis().SetTitle(hist_clasdis_excl.GetXaxis().GetTitle().replace(" (Smeared)", ""))
    proj_harut_1d_norm.SetTitle(Shared_Title)
    proj_harut_1d_norm.GetXaxis().SetTitle(proj_harut_1d_norm.GetXaxis().GetTitle().replace(" (Smeared)", ""))
    hist_data_wbkg.SetTitle(Shared_Title)
    hist_data_wbkg.GetXaxis().SetTitle(hist_data_wbkg.GetXaxis().GetTitle().replace(" (Smeared)", ""))
    # hist_clasdis_excl.Draw("hist")

    y_max_cutoff = max([hist_data_wbkg.GetMaximum(), proj_harut_1d_norm.GetMaximum(), hist_clasdis_ebkg.GetMaximum()])
    hist_data_wbkg.GetYaxis().SetRangeUser(0, 1.15*y_max_cutoff)
    hist_data_wbkg.Draw("hist")
    proj_harut_1d_norm.Draw("hist same")
    hist_data_excl.Draw("hist same")
    if(args.subtract_background):
        hist_data_excl.Draw("hist same")
        y_max_cutoff = max([hist_data_excl.GetMaximum(), y_max_cutoff])
        # merged_excl_MCs = proj_harut_1d_norm.Clone("merged_excl_MCs")
        # merged_excl_MCs.Add(hist_clasdis_ebkg)
        # merged_excl_MCs.SetLineColor(ROOT.kViolet)
        # merged_excl_MCs.Draw("hist same")
    hist_clasdis_ebkg.Draw("hist same")
    # proj_harut_1d.Draw("hist same")
    if(args.add_background):
        true_harut_1d.Draw("hist same")
        y_max_cutoff = max([true_harut_1d.GetMaximum(), y_max_cutoff])

    Cutoff_Line_Exclusive  = ROOT.TLine(args.z_tot_cut, 0.0, args.z_tot_cut, y_max_cutoff)
    Cutoff_Line_Exclusive.SetLineColor(ROOT.kGray+3)
    Cutoff_Line_Exclusive.SetLineStyle(1)
    Cutoff_Line_Exclusive.SetLineWidth(2)
    Cutoff_Line_Exclusive.Draw("same")
    
    legend_cd_2 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
    legend_cd_2.SetFillStyle(0)
    legend_cd_2.SetBorderSize(0)
    if(args.add_background):
        legend_cd_2.AddEntry(proj_harut_1d_norm, "#scale[2.0]{Harut Exclusive+clasdis SIDIS BKG}",    "l")
        legend_cd_2.AddEntry(true_harut_1d,      "#scale[1.65]{Harut Exclusive MC (w/out SIDIS BKG)}","l")
    else:
        legend_cd_2.AddEntry(proj_harut_1d_norm,"#scale[4.0]{Harut Exclusive MC}",                "l")
    if(args.subtract_background):
        legend_cd_2.AddEntry(hist_data_excl,"#scale[2.65]{#splitline{Exclusive Experimental Data}{(w/out SIDIS BKG)}}",   "l")
    legend_cd_2.AddEntry(hist_data_wbkg,    "#scale[2.65]{#splitline{Exclusive Experimental Data}{(with SIDIS BKG)}}",   "l")
    # legend_cd_2.AddEntry(hist_clasdis_excl, "#scale[1.5]{clasdis Exclusive #rho^{0} (Normalized)}",        "l")
    legend_cd_2.AddEntry(hist_clasdis_ebkg, "#scale[3.65]{#splitline{clasdis BKG SIDIS}{in Exclusive Region}}",   "l")
    # legend_cd_2.AddEntry(proj_harut_1d,     "#scale[1.5]{Harut Exclusive MC (Raw)}",                       "l")
    # legend_cd_2.AddEntry(hist_clasdis_norm, "#scale[1.5]{clasdis SIDIS (Normalized to Data)}",             "l")
    # legend_cd_2.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized to Data)}",              "l")

    legend_cd_2.Draw("same")
    
    # Coordinates are NDC because of the "NDC" option
    box = ROOT.TPaveText(0.575, 0.55, 0.975, 0.65, "NDC")
    box.SetFillColor(0)      # white fill
    box.SetFillStyle(1001)   # solid fill
    box.SetBorderSize(1)
    # box.SetTextAlign(12)     # left/center
    box.SetTextAlign(22)      # centered horizontally and vertically
    # box.SetTextFont(42)
    box.SetTextFont(62)  # bold Helvetica
    box.SetTextSize(0.025)
    box.SetMargin(0.02)       # reduce left/right internal padding
    box.AddText("Normalization Factor to bring this")
    box.AddText("Exclusive MC to clasdis SIDIS:")
    final_factor_text = Full_List_of_Factors[Kinematic_Bin]["final_factor"] if(Kinematic_Bin not in ["Full"]) else sum(Full_List_of_Factors[ii]["final_factor"] if(ii not in ["All"]) else 0 for ii in Full_List_of_Factors)/(len(Full_List_of_Factors) - 1)
    box.AddText(f"{final_factor_text:.6f}")
    box.Draw()
    canvas.SaveAs(out_file)
    print(f"{color.BOLD}Saved combined 1D histogram canvas with legend to: {color.BPINK}{out_file}{color.END}")
    return canvas


def project_z_bins_global(h3d, name, z_values_list, args=None, function_or_hist_integration="hist", diagnostic=False):
    if(not h3d):
        return None
    if((getattr(args, "legacy", False) and (function_or_hist_integration in ["hist"])) or diagnostic):
        proj_option = "yx" if(str(getattr(args, "vars", "z1z2")).lower() not in ["q2xb"]) else "xy"
        zaxis = h3d.GetZaxis()
    else:
        proj_option = "zx"
        zaxis = h3d.GetYaxis()
    proj = None
    for zval in z_values_list:
        bin_num = zaxis.FindBin(zval)
        zaxis.SetRange(bin_num, bin_num)
        tmp = h3d.Project3D(proj_option)
        if(proj is None):
            proj = tmp.Clone(name)
            proj.Reset()
        else:
            proj.Add(tmp)
        tmp.Delete()
    # zaxis.SetRange(0, 0)  # reset range
    if((getattr(args, "extra_root_save", False)) and (proj is not None)):
        args_name = getattr(args, "name", '')
        root_name = f"{f'{args_name}_' if(args_name not in ['']) else ''}{name}.root"
        for remove in ["(", ")", " "]:
            root_name = root_name.replace(remove, "")
        out_file = ROOT.TFile.Open(root_name, "RECREATE")
        if((not out_file) or (out_file.IsZombie())):
            raise OSError(f"Could not create ROOT file: {root_name}")
        out_file.cd()
        proj.Write(name)
        out_file.Close()
        print(f"{color.BGREEN}Saved a Sliced TH2D histogram as: {color.BBLUE}{root_name}{color.END}\n")
    return proj

def histo_setup_for_Wpions(args):
    print(f"\n{color.BLUE}Getting the correct histograms...{color.END}\n")
    hist_key___data  =  "(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(W_pippim)_(exclusive_rho_individual)"
    hist_key__harut  = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)_({'lundvpk' if(not args.old_lund) else 'lundrho'})"
    hist_key_clasdis =  "(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)"

    if(getattr(args, "use_z_bins", False)):
        hist_key___data  =  hist_key___data.replace("Q2_y_z_pT_Bin_All", "z_Bins")
        hist_key__harut  =  hist_key__harut.replace("Q2_y_z_pT_Bin_All", "z_Bins")
        hist_key_clasdis = hist_key_clasdis.replace("Q2_y_z_pT_Bin_All", "z_Bins")
    elif(args.Use_2D_Kinematic_Binning or True): # As of 6/13/2026, these histograms always use the Q2-y bins or z-bins
        hist_key___data  =  hist_key___data.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")
        hist_key__harut  =  hist_key__harut.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")
        hist_key_clasdis = hist_key_clasdis.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")

    if(args.verbose):
        print(f"Loading ROOT file: {args.file1}")
        print(f"Loading histogram key 'hist_key___data'  = {hist_key___data}")
        print(f"Loading histogram key 'hist_key__harut'  = {hist_key__harut}")
        print(f"Loading histogram key 'hist_key_clasdis' = {hist_key_clasdis}")

    file1 = ROOT.TFile.Open(args.file1)
    if((not file1) or (file1.IsZombie())):
        print(f"ERROR: Failed to open ROOT file: {args.file1}")
        sys.exit(1)

    h3__data = file1.Get(hist_key___data)
    check_histo_for_errors(h3__data, hist_key___data,  args.file1)
    h3_harut = file1.Get(hist_key__harut)
    check_histo_for_errors(h3_harut, hist_key__harut,  args.file1)
    h3___mdf = file1.Get(hist_key_clasdis)
    check_histo_for_errors(h3___mdf, hist_key_clasdis, args.file1)
    
    print(f"{color.BGREEN}Successfully loaded all TH3D histograms and validated compatibility.{color.END}")
    
    # args.Exclusive_bins = [87, 95, 119, 127, 215, 223, 247, 255]
    args.Exclusive_bins = [23, 31, 55, 63, 87, 95, 119, 127, 151, 159, 183, 191, 215, 223, 247, 255]
    # args.SIDIS_BKG_bins = [92, 94, 124, 126, 220, 222, 252, 254]
    args.SIDIS_BKG_bins = [28, 30, 60, 62, 92, 94, 124, 126, 156, 158, 188, 190, 220, 222, 252, 254]

    # Data
    proj__data_excl = project_z_bins_global(h3__data, "proj__data_excl", args.Exclusive_bins, args, function_or_hist_integration="func")
    # Harut's MC
    proj_harut_excl = project_z_bins_global(h3_harut, "proj_harut_excl", args.Exclusive_bins, args, function_or_hist_integration="func")
    # clasdis MC (SIDIS BKG)
    proj_mdf__exbkg = project_z_bins_global(h3___mdf, "proj_mdf__exbkg", args.SIDIS_BKG_bins, args, function_or_hist_integration="func")

    return args, proj__data_excl, proj_harut_excl, proj_mdf__exbkg, file1

def Create_Wpions_Fit_Images(args, mass_data, mass_harut, fy_data, fy_harut, fy1_data, fy1_harut, fy2_data, fy2_harut, fy3_data, fy3_harut, fy4_data, fy4_harut, N_data_rho, N_harut_rho, n_rho):
    fmt = args.file_format.lower()
    suffix = f"_{args.name}" if(args.name) else ""
    suffix = f"{suffix}_Bin_{getattr(args, 'current_kinematic_bin', 'All')}"
    # Data fit plot
    c_data = ROOT.TCanvas("c_data_fit", "", 900, 600)
    ROOT.gStyle.SetOptStat(0)
    mass_data.SetTitle(f"#splitline{{M_{{#pi^{{+}}#pi^{{-}}}} Distribution from Experimental Data}}{{{args.title}}}")
    if(getattr(args, 'current_kinematic_bin', 'All') not in ["All", "Full"]):
        mass_data.SetTitle(f"#splitline{{{mass_data.GetTitle()}}}{{Kinematic Bin {getattr(args, 'current_kinematic_bin', 'All')}}}")
    mass_data.GetYaxis().SetRangeUser(0, 1.15*mass_data.GetMaximum())
    mass_data.Draw("hist")
    mass_data.SetLineColor(ROOT.kCyan)
    fy_data.SetLineColor(ROOT.kBlack)
    fy_data.Draw("same")
    fy1_data.SetLineColor(ROOT.kMagenta)
    fy1_data.Draw("same")
    fy2_data.SetLineColor(ROOT.kRed)
    fy2_data.Draw("same")
    fy3_data.SetLineColor(ROOT.kBlue)
    fy3_data.Draw("same")
    fy4_data.SetLineColor(ROOT.kOrange)
    fy4_data.Draw("same")
    # leg_d = ROOT.TLegend(0.55, 0.07, 0.92, 0.50)
    leg_d = ROOT.TLegend(0.55, 0.075+0.15, 0.9, 0.525+0.15)
    leg_d.SetFillStyle(0); leg_d.SetBorderSize(0)
    leg_d.AddEntry(mass_data, "Experimental Data", "l")
    leg_d.AddEntry(fy_data,   "Full Fit",          "l")
    leg_d.AddEntry(fy3_data,  "f_{2}",             "l")
    leg_d.AddEntry(fy4_data,  "f_{0}",             "l")
    leg_d.AddEntry(fy1_data,  "#rho^{0} Signal",   "l")
    leg_d.AddEntry(fy2_data,  "General Background","l")
    leg_d.Draw("same")
    box_d = ROOT.TPaveText(0.575, 0.55+0.15, 0.9, 0.65+0.15, "NDC")
    box_d.SetFillColor(0); box_d.SetBorderSize(1); box_d.SetFillStyle(1001)
    box_d.SetTextAlign(22); box_d.SetTextFont(62); box_d.SetTextSize(0.025)
    box_d.SetMargin(0.02)
    box_d.AddText("Number of Experimental")
    box_d.AddText("Exclusive #rho^{0} Events from Fit:")
    box_d.AddText(f"{N_data_rho:.6f}")
    box_d.Draw("same")
    if(not args.no_save):
        c_data.SaveAs(f"Wpions_Fit_Experimental_Data{suffix}.{fmt}")
        print(f"{color.BOLD}Saved Wpions data fit: {color.BBLUE}Wpions_Fit_Experimental_Data{suffix}.{fmt}{color.END}")
    else:
        print(f"{color.Error}Would have saved Wpions data fit: {color.END_B}Wpions_Fit_Experimental_Data{suffix}.{fmt}{color.END}")
    # Harut fit plot
    c_harut = ROOT.TCanvas("c_harut_fit", "", 900, 600)
    ROOT.gStyle.SetOptStat(0)
    mass_harut.SetTitle(f"#splitline{{M_{{#pi^{{+}}#pi^{{-}}}} Distribution from Harut's MC}}{{{args.title}}}")
    if(getattr(args, 'current_kinematic_bin', 'All') not in ["All", "Full"]):
        mass_harut.SetTitle(f"#splitline{{{mass_harut.GetTitle()}}}{{Kinematic Bin {getattr(args, 'current_kinematic_bin', 'All')}}}")
    mass_harut.GetXaxis().SetTitle(str(mass_harut.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    mass_harut.GetYaxis().SetRangeUser(0, 1.2*mass_harut.GetMaximum())
    mass_harut.Draw("hist")
    mass_harut.SetLineColor(ROOT.kGreen)
    fy_harut.SetLineColor(ROOT.kBlack)
    fy_harut.Draw("same")
    fy1_harut.SetLineColor(ROOT.kMagenta)
    fy1_harut.Draw("same")
    fy2_harut.SetLineColor(ROOT.kRed)
    fy2_harut.Draw("same")
    # fy3_harut.SetLineColor(ROOT.kBlue)
    # fy3_harut.Draw("same")
    # fy4_harut.SetLineColor(ROOT.kOrange)
    # fy4_harut.Draw("same")
    leg_h = ROOT.TLegend(0.55, 0.075+0.15, 0.9, 0.525+0.15)
    leg_h.SetFillStyle(0); leg_h.SetBorderSize(0)
    leg_h.AddEntry(mass_harut, "Harut's Monte Carlo", "l")
    leg_h.AddEntry(fy_harut,   "Full Fit",            "l")
    leg_h.AddEntry(fy1_harut,  "#rho^{0} Signal",     "l")
    leg_h.AddEntry(fy2_harut,  "General Background",  "l")
    # leg_h.AddEntry(fy3_harut,  "f_{2}",               "l")
    # leg_h.AddEntry(fy4_harut,  "f_{0}",               "l")
    leg_h.Draw("same")
    box_h = ROOT.TPaveText(0.575, 0.55+0.15, 0.9, 0.65+0.15, "NDC")
    box_h.SetFillColor(0); box_h.SetBorderSize(1); box_h.SetFillStyle(1001)
    box_h.SetTextAlign(22); box_h.SetTextFont(62); box_h.SetTextSize(0.025)
    box_h.SetMargin(0.02)
    box_h.AddText("Number of Harut's MC")
    box_h.AddText("Exclusive #rho^{0} Events:")
    box_h.AddText(f"{N_harut_rho:.6f}")
    box_h.Draw("same")
    if(not args.no_save):
        c_harut.SaveAs(f"Wpions_Fit_Harut_MC{suffix}.{fmt}")
        print(f"{color.BOLD}Saved Wpions Harut fit: {color.BBLUE}Wpions_Fit_Harut_MC{suffix}.{fmt}{color.END}")
    else:
        print(f"{color.Error}Would have saved Wpions Harut fit: {color.END_B}Wpions_Fit_Harut_MC{suffix}.{fmt}{color.END}")

# Nick's original dynamic ipart setup for 2 histograms
par_Num = []
for i in range(0, 2):
    if(i == 0):
        n = [0,1,2, 3,4,5,6, 7,8,9, 10,11,12]
    else:
        j = 13
        n = [j,1,2, j+1,4,5,6, j+2,8,9, j+3,11,12]
    par_Num.append(n)
ipart = np.array(par_Num, dtype=np.int32)
class GlobalChi2(object):
    def __init__(self, f1, numOfHist):
        self._f1 = f1
        self._numOfHist = numOfHist
    def __call__(self, par):
        par_arr = np.frombuffer(par, dtype=np.float64, count=self._numOfHist * 17)
        p = []
        for i in range(0, self._numOfHist):
            p.append(par_arr[ipart[i]])
        tot = 0
        for i in range(0, self._numOfHist):
            tot += self._f1[i](p[i])
        return tot


def fit_W_rho_from_Nick(args, hist_data, hist_harut, minValue, maxValue, useBkg=True, useF2=True, useF0=True):
    useBkg_harut, useF2_harut, useF0_harut = True, False, False
    if(args.verbose):
        minBin, maxBin = hist_data.FindBin(minValue), hist_data.FindBin(maxValue)
        print(f"\n\nfit_W_rho_from_Nick: fitting TWO histograms INDEPENDENTLY | data entries {hist_data.Integral(minBin, maxBin):.0f} | harut entries {hist_harut.Integral(minBin, maxBin):.0f} | Bkg={useBkg} F2={useF2} F0={useF0} | range [{minValue}, {maxValue}]")
    default_data__name =  hist_data.GetName()
    default_harut_name = hist_harut.GetName()
    pol3_or_gaus = "gaus"
    if(pol3_or_gaus == "gaus"):
        fyp_data  = ROOT.TF1(f"{default_data__name}_fy_data",  "breitwigner(0) + [p3] + gaus(4) + breitwigner(7) + breitwigner(10)", minValue, maxValue, 13)
        fyp_harut = ROOT.TF1(f"{default_harut_name}_fy_harut", "breitwigner(0) + [p3] + gaus(4)", minValue, min([maxValue, 1.25]), 7)
    else:
        fyp_data  = ROOT.TF1(f"{default_data__name}_fy_data",  "breitwigner(0) + pol3(3) + breitwigner(7) + breitwigner(10)", minValue, maxValue, 13)
        fyp_harut = ROOT.TF1(f"{default_harut_name}_fy_harut", "breitwigner(0) + pol3(3)", minValue, maxValue, 7)

    fy1p     = [ROOT.TF1(f"{default_data__name}_fy1_rho_experiment",  "breitwigner(0)", minValue, maxValue, 3), ROOT.TF1(f"{default_harut_name}_fy1_rho_harut",  "breitwigner(0)", minValue, maxValue, 3)]
    if(pol3_or_gaus == "gaus"):
        fy2p = [ROOT.TF1(f"{default_data__name}_fy2_bkg_experiment",  "[p0] + gaus(1)", minValue, maxValue, 4), ROOT.TF1(f"{default_harut_name}_fy2_bkg_harut",  "[p0] + gaus(1)", minValue, maxValue, 4)]
    else:
        fy2p = [ROOT.TF1(f"{default_data__name}_fy2_bkg_experiment",  "pol3(0)",        minValue, maxValue, 4), ROOT.TF1(f"{default_harut_name}_fy2_bkg_harut",  "pol3(0)",        minValue, maxValue, 4)]
    fy3p     = [ROOT.TF1(f"{default_data__name}_fy3_f2_experiment",   "breitwigner(0)", minValue, maxValue, 3), ROOT.TF1(f"{default_harut_name}_fy3_f2_harut",   "breitwigner(0)", minValue, maxValue, 3)]
    fy4p     = [ROOT.TF1(f"{default_data__name}_fy4_f0_experiment",   "breitwigner(0)", minValue, maxValue, 3), ROOT.TF1(f"{default_harut_name}_fy4_f0_harut",   "breitwigner(0)", minValue, maxValue, 3)]

    # Data (full 13-parameter model)
    fyp_data.SetParName(0, "#rho Amp");      fyp_data.SetParName(1, "#rho Mean");  fyp_data.SetParName(2, "#rho Sigma")
    if(pol3_or_gaus == "gaus"):
        fyp_data.SetParName(3, "Constant");  fyp_data.SetParName(4, "BKG Amp");    fyp_data.SetParName(5, "BKG Mean");  fyp_data.SetParName(6, "BKG Sigma")
    else:
        fyp_data.SetParName(3, "bkg Amp");   fyp_data.SetParName(4, "bkg p1");     fyp_data.SetParName(5, "bkg p2");    fyp_data.SetParName(6, "bkg p3")
    fyp_data.SetParName(7, "f2 Amp");        fyp_data.SetParName(8, "f2 Mean");    fyp_data.SetParName(9, "f2 Sigma")
    fyp_data.SetParName(10,"f0 Amp");        fyp_data.SetParName(11,"f0 Mean");    fyp_data.SetParName(12,"f0 Sigma")
    # Harut (rho + pol3/gaus background only — 7 parameters)
    fyp_harut.SetParName(0, "#rho Amp");     fyp_harut.SetParName(1, "#rho Mean"); fyp_harut.SetParName(2, "#rho Sigma")
    if(pol3_or_gaus == "gaus"):
        fyp_harut.SetParName(3, "Constant"); fyp_harut.SetParName(4, "BKG Amp");   fyp_harut.SetParName(5, "BKG Mean"); fyp_harut.SetParName(6, "BKG Sigma")
    else:
        fyp_harut.SetParName(3, "bkg Amp");  fyp_harut.SetParName(4, "bkg p1");    fyp_harut.SetParName(5, "bkg p2");   fyp_harut.SetParName(6, "bkg p3")
    

    opt = ROOT.Fit.DataOptions()
    rang = ROOT.Fit.DataRange()
    rang.SetRange(minValue, maxValue)

    # === INDEPENDENT FIT FOR EXPERIMENTAL DATA ===
    hp_data = hist_data.GetPtr() if hasattr(hist_data, "GetPtr") else hist_data
    data_data = ROOT.Fit.BinData(opt, rang)
    ROOT.Fit.FillData(data_data, hp_data)
    wfy_data = ROOT.Math.WrappedMultiTF1(fyp_data, 1)
    chi2_data = ROOT.Fit.Chi2Function(data_data, wfy_data)

    fitter_data = ROOT.Fit.Fitter()
    Npar_data = 13
    if(pol3_or_gaus == "gaus"):
        parTemp_data = [2000.0, 0.77, 0.15,
                                              0.0, 100 if(useBkg) else 0.0, 0.50 if(useBkg) else 0.0, 1.1 if(useBkg) else 0.0,
                        20.0  if(useF2)  else 0.0, 1.2 if(useF2)  else 0.0, 0.18 if(useF2)  else 0.0,
                        20.0  if(useF0)  else 0.0, 0.98 if(useF0) else 0.0, 0.18 if(useF0)  else 0.0]
    else:
        parTemp_data = [2000.0, 0.77, 0.15,
                        800.0 if(useBkg) else 0.0, 1.2 if(useBkg) else 0.0, 0.30 if(useBkg) else 0.0, 1.1 if(useBkg) else 0.0,
                        20.0  if(useF2)  else 0.0, 1.2 if(useF2)  else 0.0, 0.18 if(useF2)  else 0.0,
                        20.0  if(useF0)  else 0.0, 0.98 if(useF0) else 0.0, 0.18 if(useF0)  else 0.0]
    par0_data = np.array(parTemp_data)
    fitter_data.Config().SetParamsSettings(Npar_data, par0_data)

    fitter_data.Config().ParSettings(0).SetLimits(0, 20000)
    fitter_data.Config().ParSettings(1).SetLimits(0.60, 0.95)
    fitter_data.Config().ParSettings(2).SetLimits(0.05, 0.25)
    if(not useBkg):
        fitter_data.Config().ParSettings(3).Fix()
    else:
        if(pol3_or_gaus == "gaus"):
            fitter_data.Config().ParSettings(3).SetLimits(0, 0)
            fitter_data.Config().ParSettings(4).SetLimits(0, 400)
            fitter_data.Config().ParSettings(5).SetLimits(0.2, 0.7)
            fitter_data.Config().ParSettings(6).SetLimits(0, 5)
        else:
            fitter_data.Config().ParSettings(3).SetLimits(0, 1e6)
            fitter_data.Config().ParSettings(4).SetLimits(0, 5)
            fitter_data.Config().ParSettings(5).SetLimits(0.2, 0.4)
            fitter_data.Config().ParSettings(6).SetLimits(0, 5)
    if(not useF2):
        fitter_data.Config().ParSettings(7).Fix()
    else:
        fitter_data.Config().ParSettings(7).SetLimits(0, 1e4)
        fitter_data.Config().ParSettings(8).SetLimits(1.1, 1.6)
        fitter_data.Config().ParSettings(9).SetLimits(0.01, 0.5)
    if(not useF0):
        fitter_data.Config().ParSettings(10).Fix()
    else:
        fitter_data.Config().ParSettings(10).SetLimits(0, 1e4)
        fitter_data.Config().ParSettings(11).SetLimits(0.88, 1.0)
        fitter_data.Config().ParSettings(12).SetLimits(0.01, 0.5)
    fitter_data.Config().MinimizerOptions().SetPrintLevel(0)
    fitter_data.Config().SetMinimizer("Minuit2", "Migrad")
    fitter_data.FitFCN(ROOT.Math.Functor(chi2_data, Npar_data), 0, int(data_data.Size()), True)
    result_data = fitter_data.Result()
    pars_data = result_data.GetParams()

    # === INDEPENDENT FIT FOR HARUT MC (rho + pol3 background only) ===
    hp_harut = hist_harut.GetPtr() if(hasattr(hist_harut, "GetPtr")) else hist_harut
    data_harut = ROOT.Fit.BinData(opt, rang)
    ROOT.Fit.FillData(data_harut, hp_harut)
    wfy_harut = ROOT.Math.WrappedMultiTF1(fyp_harut, 1)
    chi2_harut = ROOT.Fit.Chi2Function(data_harut, wfy_harut)

    fitter_harut = ROOT.Fit.Fitter()
    Npar_harut = 7
    if(pol3_or_gaus == "gaus"):
        parTemp_harut = [1500.0, 0.77, 0.15,         0.0, 100 if(useBkg_harut) else 0.0, 0.50 if(useBkg_harut) else 0.0, 1.1 if(useBkg_harut) else 0.0]
    else:
        parTemp_harut = [1500.0, 0.77, 0.15,
                         800.0 if(useBkg_harut) else 0.0, 1.2 if(useBkg_harut) else 0.0, 0.30 if(useBkg_harut) else 0.0, 1.1 if(useBkg_harut) else 0.0]
    par0_harut = np.array(parTemp_harut)
    fitter_harut.Config().SetParamsSettings(Npar_harut, par0_harut)

    fitter_harut.Config().ParSettings(0).SetLimits(0, 1e6)
    fitter_harut.Config().ParSettings(1).SetLimits(0.60, 0.95)
    fitter_harut.Config().ParSettings(2).SetLimits(0.05, 0.25)
    if(not useBkg_harut):
        fitter_harut.Config().ParSettings(3).Fix()
    else:
        if(pol3_or_gaus == "gaus"):
            fitter_harut.Config().ParSettings(3).SetLimits(0, 0)
            fitter_harut.Config().ParSettings(4).SetLimits(0, 500)
            # fitter_harut.Config().ParSettings(5).SetLimits(0.2, 0.7)
            fitter_harut.Config().ParSettings(5).SetLimits(0.2, 1)
            fitter_harut.Config().ParSettings(6).SetLimits(0, 3)
        else:
            fitter_harut.Config().ParSettings(3).SetLimits(0, 1e6)
            fitter_harut.Config().ParSettings(4).SetLimits(0, 5)
            fitter_harut.Config().ParSettings(5).SetLimits(0.2, 0.4)
            fitter_harut.Config().ParSettings(6).SetLimits(0, 5)
    fitter_harut.Config().MinimizerOptions().SetPrintLevel(0)
    fitter_harut.Config().SetMinimizer("Minuit2", "Migrad")
    fitter_harut.FitFCN(ROOT.Math.Functor(chi2_harut, Npar_harut), 0, int(data_harut.Size()), True)
    result_harut = fitter_harut.Result()
    pars_harut = result_harut.GetParams()

    # transfer results to main TF1s
    fyp_data.SetFitResult(result_data, np.array(range(13), dtype=np.int32))
    fyp_harut.SetFitResult(result_harut, np.array(range(7), dtype=np.int32))
    fyp_data.SetRange(rang().first, rang().second)
    fyp_harut.SetRange(rang().first, rang().second)

    # Data components
    fy1p[0].FixParameter(0, pars_data[0]); fy1p[0].FixParameter(1, pars_data[1]); fy1p[0].FixParameter(2, pars_data[2])
    fy1p[0].FixParameter(3, pars_data[3]); fy1p[0].FixParameter(4, pars_data[4]); fy1p[0].FixParameter(5, pars_data[5])
    fy1p[0].SetLineColor(ROOT.kMagenta)
    bkg_idx = 3
    fy2p[0].FixParameter(0, pars_data[bkg_idx]); fy2p[0].FixParameter(1, pars_data[bkg_idx+1])
    fy2p[0].FixParameter(2, pars_data[bkg_idx+2]); fy2p[0].FixParameter(3, pars_data[bkg_idx+3])
    fy2p[0].SetLineColor(ROOT.kRed)
    fy3p[0].FixParameter(0, pars_data[7]); fy3p[0].FixParameter(1, pars_data[8]); fy3p[0].FixParameter(2, pars_data[9])
    fy3p[0].SetLineColor(ROOT.kBlue)
    fy4p[0].FixParameter(0, pars_data[10]); fy4p[0].FixParameter(1, pars_data[11]); fy4p[0].FixParameter(2, pars_data[12])
    fy4p[0].SetLineColor(ROOT.kOrange)

    # Harut components (rho + pol3 background)
    fy1p[1].FixParameter(0, pars_harut[0]); fy1p[1].FixParameter(1, pars_harut[1]); fy1p[1].FixParameter(2, pars_harut[2])
    fy1p[1].SetLineColor(ROOT.kMagenta)
    fy2p[1].FixParameter(0, pars_harut[3]); fy2p[1].FixParameter(1, pars_harut[4])
    fy2p[1].FixParameter(2, pars_harut[5]); fy2p[1].FixParameter(3, pars_harut[6])
    fy2p[1].SetLineColor(ROOT.kRed)

    return (pars_data[0], result_data.GetErrors()[0], pars_harut[0], result_harut.GetErrors()[0], fyp_data, fyp_harut, fy1p[0], fy1p[1], fy2p[0], fy2p[1], fy3p[0], fy3p[1], fy4p[0], fy4p[1])


def main_Get_rho_Normalization_values_Wpions(args):
    print(f"\n{color.BBLUE}Starting Wpions fit-based rho0 normalization...{color.END}")
    ROOT.ROOT.EnableImplicitMT()
    args, proj__data_excl, proj_harut_excl, proj_mdf__exbkg, file1 = histo_setup_for_Wpions(args)
    args.x_min =  0.2 if(args.x_min == 0.08) else args.x_min
    args.x_max =  2.0 if(args.x_max == 0.68) else args.x_max
    minValue = max([0.1, args.x_min])
    maxValue = min([2.0, args.x_max])
    list_of_Values = {}
    Num_Projections = [getattr(args, "Kinematic_Bin_Select", "All")] if(not (getattr(args, "use_z_bins", False) and (getattr(args, "Kinematic_Bin_Select", "All") in ["Full"]))) else list(range(1, 10))
    for kinematic_bin in Num_Projections:
        # 1D projections used as input distributions for fit (adapted from existing logic)
        if(getattr(args, "Kinematic_Bin_Select", "All") in ["All", "Full"]):
            if(kinematic_bin not in ["All", "Full"]):
                histo__data_Wpions = proj__data_excl.ProjectionX(f"histo__data_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}", int(kinematic_bin), int(kinematic_bin))
                histo_harut_Wpions = proj_harut_excl.ProjectionX(f"histo_harut_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}", int(kinematic_bin), int(kinematic_bin))
                histo_mdfbg_Wpions = proj_mdf__exbkg.ProjectionX(f"histo_mdfbg_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}", int(kinematic_bin), int(kinematic_bin))
            else:
                histo__data_Wpions = proj__data_excl.ProjectionX(f"histo__data_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}")
                histo_harut_Wpions = proj_harut_excl.ProjectionX(f"histo_harut_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}")
                histo_mdfbg_Wpions = proj_mdf__exbkg.ProjectionX(f"histo_mdfbg_Wpions_Bin_{str(kinematic_bin).replace('Full', 'All')}")
        else:
            histo_bin_num = proj__data_excl.GetYaxis().FindBin(int(getattr(args, "Kinematic_Bin_Select", 0)))
            histo__data_Wpions = proj__data_excl.ProjectionX(f"histo__data_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
            histo_harut_Wpions = proj_harut_excl.ProjectionX(f"histo_harut_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
            histo_mdfbg_Wpions = proj_mdf__exbkg.ProjectionX(f"histo_mdfbg_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
        (N_data_rho, rho_err_data, N_harut_rho, rho_err_harut, fy_data, fy_harut, fy1_rho_experiment, fy1_rho_harut, fy2_bkg_experiment, fy2_bkg_harut, fy3_f2_experiment, fy3_f2_harut, fy4_f0_experiment, fy4_f0_harut) = fit_W_rho_from_Nick(args, histo__data_Wpions, histo_harut_Wpions, minValue, maxValue, useBkg=True, useF2=True, useF0=True)
        bin_width_data  = histo__data_Wpions.GetXaxis().GetBinWidth(1)
        bin_width_harut = histo_harut_Wpions.GetXaxis().GetBinWidth(1)
        
        N_data_rho  = (fy1_rho_experiment.Integral(minValue, maxValue))/bin_width_data
        N_harut_rho = (fy1_rho_harut.Integral(minValue, maxValue))/bin_width_harut
        # N_data_rho  = fy1_rho_experiment.Integral(0.2, 2.0)
        # N_harut_rho = fy1_rho_harut.Integral(0.2, 2.0)
        n_rho = N_data_rho / N_harut_rho if(N_harut_rho > 0) else 0.0
        list_of_Values[f"Values_for_Bin_{kinematic_bin}"] = {"N_data_rho": N_data_rho, "N_harut_rho": N_harut_rho, "n_rho": n_rho, "rho_err_data": rho_err_data, "rho_err_harut": rho_err_harut, "fy_data": fy_data, "fy_harut": fy_harut, "fy1_rho_experiment": fy1_rho_experiment, "fy1_rho_harut": fy1_rho_harut, "fy2_bkg_experiment": fy2_bkg_experiment, "fy2_bkg_harut": fy2_bkg_harut, "fy3_f2_experiment": fy3_f2_experiment, "fy3_f2_harut": fy3_f2_harut, "fy4_f0_experiment": fy4_f0_experiment, "fy4_f0_harut": fy4_f0_harut}
        print("")
        print(f"{ color.BBLUE}Fit-based normalization (Wpions):{color.END}")
        print(f"{ color.BOLD }Kinematic Bin Used: {kinematic_bin}{color.END}")
        print(f"{ color.BOLD }N_data_rho (Experimental exclusive signal)        : {N_data_rho:>12.0f}{color.END}")
        print(f"{ color.BOLD }N_harut_rho (Harut's exclusive signal)            : {N_harut_rho:>12.0f}{color.END}")
        print(f"{color.BGREEN}n_rho (brings Harut's files to data)              : {n_rho:>12.6f}{color.END}\n")
        if(args.verbose):
            # Debug: print fitted parameters
            print(f"\n{color.BUNDERLINE}Fitted parameters (data):{color.END}")
            for i in range(13):
                print(f"  par[{i:>2.0f}] = {fy_data.GetParameter(i):>13.4f} ± {fy_data.GetParError(i):.4f}")
            print(f"\n{color.BUNDERLINE}Fitted parameters (harut):{color.END}")
            for i in range(7):
                print(f"  par[{i:>2.0f}] = {fy_harut.GetParameter(i):>13.4f} ± {fy_harut.GetParError(i):.4f}")
        print("\n\n")
        args.current_kinematic_bin = kinematic_bin
        Create_Wpions_Fit_Images(args, histo__data_Wpions, histo_harut_Wpions, fy_data, fy_harut, fy1_rho_experiment, fy1_rho_harut, fy2_bkg_experiment, fy2_bkg_harut, fy3_f2_experiment, fy3_f2_harut, fy4_f0_experiment, fy4_f0_harut, N_data_rho, N_harut_rho, n_rho)
    if(len(Num_Projections) > 1):
        N_data_rho_sum, N_harut_rho_sum, n_rho_sum = 0, 0, 0
        for bin_name in list_of_Values:
            N_data_rho_sum  += list_of_Values[bin_name]["N_data_rho"]
            N_harut_rho_sum += list_of_Values[bin_name]["N_harut_rho"]
            n_rho_sum       += list_of_Values[bin_name]["n_rho"]
        N_data_rho_ave  = N_data_rho_sum/len(Num_Projections)
        N_harut_rho_ave = N_harut_rho_sum/len(Num_Projections)
        n_rho_ave       = n_rho_sum/len(Num_Projections)
        print("")
        print(f"{ color.BBLUE}Fit Averages from All {len(list_of_Values)} Kinematic Bins{color.END}")
        print(f"{ color.BOLD }N_data_rho_ave (Experimental exclusive signal)        : {N_data_rho_ave:>12.0f}{color.END}")
        print(f"{ color.BOLD }N_harut_rho_ave (Harut's exclusive signal)            : {N_harut_rho_ave:>12.0f}{color.END}")
        print(f"{color.BGREEN}n_rho_ave (brings Harut's files to data)              : {n_rho_ave:>12.6f}{color.END}\n")
    else:
        n_rho_ave = n_rho
    file1.Close()
    return n_rho_ave

def main_Get_rho_Normalization_values(args):
    print(f"\n{color.BBLUE}Starting execution of {Name_of_Script}...{color.END}\n")

    # === CORRECT HISTOGRAM KEYS (following our exact procedure) ===
    hist_key1 =  "(Normal_2D)_(gdf)_(no_cut_Remove_rho)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)"                                          if(str(args.vars).lower() in ["q2xb"]) else  "(Normal_2D)_(rdf)_(cut_Complete_SIDIS)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)"                                                                       # Data visible exclusive (exclusive_rho_full == 1)
    hist_key2 = f"(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)_({'lundvpk' if(not args.old_lund) else 'lundrho'})"  if(str(args.vars).lower() in ["q2xb"]) else f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(z1_plus_z2_smeared)_(exclusive_rho_smeared)_({'lundvpk' if(not args.old_lund) else 'lundrho'})" # Harut edf (exclusive_rho_full_smeared == 1)
    hist_key3 = f"(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)_({'lundvpk' if(not args.old_lund) else 'lundrho'})"  if(str(args.vars).lower() in ["q2xb"]) else f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(z1_plus_z2_smeared)_(exclusive_rho_smeared)"                                                    # MDF (the only one we use)
    hist_key4 =  "(Normal_2D)_(gdf)_(no_cut_Remove_rho)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)"                                          if(str(args.vars).lower() in ["q2xb"]) else  "(Normal_2D)_(rdf)_(cut_Complete_SIDIS)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)"                                                                       # Data sideband (exclusive_rho == 0)

    # # === NEW: Two separate mdf histograms (this was the missing piece) ===
    # hist_key_mdf_side  = "(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(z1_plus_z2_smeared)_(exclusive_rho_smeared)"      # loose sideband: exclusive_rho == 0
    # hist_key_mdf_peak  = "(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(z1_plus_z2_smeared)_(exclusive_rho_full_smeared)" # tight peak: non-rho0 + full exclusive reconstructed topology

    # if(args.clasdis_z1z2):
    #     hist_key1 = "(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)"
    #     hist_key2 = "(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)_(lundvpk)"
    #     args.vars = "z1z2"

    if(args.legacy):
        hist_key1 = hist_key1.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
        hist_key2 = hist_key2.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
        hist_key3 = hist_key3.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
        hist_key4 = hist_key4.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
    else:
        hist_key1 = hist_key1.replace("exclusive_rho",  "exclusive_rho_individual")
        hist_key2 = hist_key2.replace("exclusive_rho",  "exclusive_rho_individual")
        hist_key3 = hist_key3.replace("exclusive_rho",  "exclusive_rho_individual")
        hist_key4 = hist_key4.replace("exclusive_rho",  "exclusive_rho_individual")
    hist_key1 = hist_key1.replace("cut_Complete_SIDIS", "cut_Complete_SIDIS_MM_None")
    hist_key2 = hist_key2.replace("cut_Complete_SIDIS", "cut_Complete_SIDIS_MM_None")
    hist_key3 = hist_key3.replace("cut_Complete_SIDIS", "cut_Complete_SIDIS_MM_None")
    hist_key4 = hist_key4.replace("cut_Complete_SIDIS", "cut_Complete_SIDIS_MM_None")

    if(str(args.vars).lower() in ["q2xb"]):
        if(args.draw_mode == "1D"):
            print(f"{color.Error}Warning: 1D mode is not supported for Q2xB. Forcing 2D mode.{color.END}")
        args.draw_mode = "2D"
    else:
        if(args.draw_mode == "auto"):
            args.draw_mode = "1D"

    if(args.verbose):
        print(f"Loading ROOT file 1: {args.file1}")
        print(f"Loading ROOT file 2: {args.file2 if(not args.use_same_file) else args.file1}")
        print(f"Loading histogram key from file 1: {hist_key1}")
        print(f"Loading histogram key from file 2: {hist_key2}")

    file1 = ROOT.TFile.Open(args.file1)
    if((not file1) or (file1.IsZombie())):
        print(f"ERROR: Failed to open ROOT file 1: {args.file1}")
        sys.exit(1)
    if(not args.use_same_file):
        file2 = ROOT.TFile.Open(args.file2)
        if((not file2) or (file2.IsZombie())):
            print(f"ERROR: Failed to open ROOT file 2: {args.file2}")
            sys.exit(1)
    else:
        file2 = file1

    h3d1 = file1.Get(hist_key1)
    check_histo_for_errors(h3d1,    hist_key1, args.file1)
    h3d2 = file2.Get(hist_key2)
    check_histo_for_errors(h3d2,    hist_key2, args.file2)
    h3d4 = file1.Get(hist_key4)
    check_histo_for_errors(h3d4,    hist_key4, args.file1)
    h3d_mdf = file1.Get(hist_key3)
    check_histo_for_errors(h3d_mdf, hist_key3, args.file1)
    
    print(f"{color.BGREEN}Successfully loaded all four TH3D histograms and validated compatibility.{color.END}")
    if(args.verbose):
        print("Creating 2D projections using specific bins on Z-axis (exclusive_rho_individual)...")

    # Helper to safely sum specific Z-bins while preserving "yx" or "xy" projection order
    def project_z_bins(h3d, name, z_values_list):
        if(not h3d):
            return None
        if(args.legacy):
            proj_option = "yx" if(str(args.vars).lower() not in ["q2xb"]) else "xy"
            zaxis = h3d.GetZaxis()
        else:
            proj_option = "zx"
            zaxis = h3d.GetYaxis()
        proj = None
        for zval in z_values_list:
            bin_num = zaxis.FindBin(zval)
            zaxis.SetRange(bin_num, bin_num)
            tmp = h3d.Project3D(proj_option)
            if(proj is None):
                proj = tmp.Clone(name)
                proj.Reset()
            else:
                proj.Add(tmp)
            tmp.Delete()
        # zaxis.SetRange(0, 0)  # reset range
        if((getattr(args, "extra_root_save", False)) and (proj is not None)):
            root_name = f"{f'{args.name}_' if(args.name not in ['']) else ''}{name}.root"
            for remove in ["(", ")", " "]:
                root_name = root_name.replace(remove, "")
            out_file = ROOT.TFile.Open(root_name, "RECREATE")
            if((not out_file) or (out_file.IsZombie())):
                raise OSError(f"Could not create ROOT file: {root_name}")
            out_file.cd()
            proj.Write(name)
            out_file.Close()
            print(f"{color.BGREEN}Saved a Sliced TH2D histogram as: {color.BBLUE}{root_name}{color.END}\n")
        return proj

    if(args.legacy):
        # Tight projections used for normalization
        exclusive_bins = [15, 23, 31, 47, 55, 63]
        exclusive_bins = [15, 31, 47, 63]
        excl_SIDIS_bkg = [14, 30, 46, 62] # These are events that look like they could be exclusive based on the selection cuts, but are in fact background (SIDIS) events to those exclusive distributions
        sidis_bins     = [32, 34, 48, 50, 33, 35, 49, 51] # The odd numbers in this list are only reliable in the experimental data files since the `exclusive_rho` index doesn't carry the generator-level knowledge about exclusivity (for data, the odd bins just indicate that no other particles were detected beyond what is allowable under by exclusive events, so their inclusion here assumes that there are undetected particles that could make the event fall outside of the exclusive region—supported by these exclusive bins being choosen based on the event already failing the exclusive-rho0 cuts from the invariant/missing masses)
                                                          # The odd bins are removed from the mdf SIDIS histograms by only using the events in the bins selected from the `y_bin_0` below (i.e., the bin which sets `exclusive_rho` to 0 regardless of these z-axis cuts)
        all_bins = exclusive_bins + sidis_bins
        # === Loose projections for plotting that MATCH the normalization cuts ===
        # Full data for plotting = exclusive + SIDIS parts (same bins used in normalization)
        proj_data_full_for_plot = project_z_bins(h3d1, "proj_data_full_for_plot", all_bins)
        # proj_harutfull_for_plot = project_z_bins(h3d2, "proj_harutfull_for_plot", all_bins)
        proj_data_excl  = project_z_bins(h3d1, "proj_data_excl",  exclusive_bins)
        proj_harut_excl = project_z_bins(h3d2, "proj_harut_excl", exclusive_bins)
        proj_data_SIDIS = project_z_bins(h3d4, "proj_data_SIDIS", sidis_bins)
    
        proj_mdf_SIDIS = project_z_bins(h3d_mdf, "proj_mdf_SIDIS", sidis_bins)
        proj_mdf_excl  = project_z_bins(h3d_mdf, "proj_mdf_excl",  exclusive_bins)
        proj_mdf_ebkg  = project_z_bins(h3d_mdf, "proj_mdf_ebkg",  excl_SIDIS_bkg)
    else:
        exclusive_bins = [31, 63,  95, 127]
        excl_SIDIS_bkg = [30, 62,  94, 126]
        SIDIS_clasdisB = [68, 70, 100, 102]
        SIDIS_dataBins = [68, 69,  70,  71, 100, 101, 102, 103]
        # clasdis MC
        proj_mdf_SIDIS  = project_z_bins(h3d_mdf, "proj_mdf_SIDIS",  SIDIS_clasdisB)
        proj_mdf_exclz  = project_z_bins(h3d_mdf, "proj_mdf_exclz",  exclusive_bins)
        proj_mdf_exbkg  = project_z_bins(h3d_mdf, "proj_mdf_exbkg",  excl_SIDIS_bkg)
        # proj_mdf_excl   = project_z_bins(h3d_mdf, "proj_mdf_excl",   exclusive_bins)
        # Data
        proj_data_SIDIS = project_z_bins(h3d4,    "proj_data_SIDIS", SIDIS_dataBins)
        proj_data_exclz = project_z_bins(h3d1,    "proj_data_exclz", exclusive_bins)
        # Harut's MC
        proj_harut_excl = project_z_bins(h3d2,    "proj_harut_excl", exclusive_bins)

        all_bins_data = exclusive_bins + SIDIS_dataBins
        # all_bins___MC = exclusive_bins + SIDIS_clasdisB
        proj_data_full_for_plot = project_z_bins(h3d1, "proj_data_full_for_plot", all_bins_data)
        # proj_harutfull_for_plot = project_z_bins(h3d2, "proj_harutfull_for_plot", all_bins___MC)

    if(args.verbose):
        print("Projections created successfully.")
        # === RECREATE 1D PROJECTIONS FROM ORIGINAL 3D HISTOGRAMS FROM SCRATCH (FULL RANGE, NO CUTS) ===
        h1d_data_full  = h3d1.ProjectionX("h1d_data_full")
        h1d_harut_full = h3d2.ProjectionX("h1d_harut_full")
        print(f"{color.BOLD}FULL 1D PROJECTION FROM ORIGINAL 3D (no cuts, full range):{color.END}")
        print(f"  Data full 1D yield  : {h1d_data_full.Integral():.0f}")
        print(f"  Harut full 1D yield : {h1d_harut_full.Integral():.0f}")
        # # === DEBUG: Check raw yields in the exact signal region used by normalization ===
        # signal_x_low  = proj_data_excl.GetXaxis().FindBin(args.z_tot_cut)
        # signal_x_high = proj_data_excl.GetXaxis().GetNbins()
        # y_bin_1 = proj_data_excl.GetYaxis().FindBin(1.0)
        # print(f"{color.BOLD}DEBUG - Raw yields in normalization exclusive signal region (z_tot > {args.z_tot_cut}):{color.END}")
        # print(f"  proj_data_excl (Data, exclusive_rho_full) : {proj_data_excl.Integral(signal_x_low,  signal_x_high, y_bin_1, y_bin_1):.0f}")
        # print(f"  proj_harut_excl (Harut exclusive)         : {proj_harut_excl.Integral(signal_x_low, signal_x_high, y_bin_1, y_bin_1):.0f}")
        # print(f"  proj_data_SIDIS (Data sideband)           : {proj_data_SIDIS.Integral(signal_x_low, signal_x_high, 0, 0):.0f}")

    if(str(args.vars).lower() not in ["q2xb"]):
        args.x_min =  0.0 if(args.x_min == 0.08) else args.x_min
        args.x_max =  1.8 if(args.x_max == 0.68) else args.x_max
        args.y_min = -0.5 if(args.y_min == 0.90) else args.y_min
        args.y_max =  1.5 if(args.y_max == 8.50) else args.y_max

    # === FULL CORRECT NORMALIZATION PROCEDURE (z1+z2 mode) ===
    if(str(args.vars).lower() not in ["q2xb"]):
        print(f"\n{color.BOLD}=== Starting full VMN normalization procedure for z1+z2 mode ==={color.END}")
        Full_List_of_HistosB, Full_List_of_Factors = {}, {}
        if(not args.legacy):
            min_x_plots        = proj_data_exclz.GetXaxis().FindBin(args.x_min)
            max_x_plots        = proj_data_exclz.GetXaxis().FindBin(args.x_max)
            # signal_x_high      = proj_data_exclz.GetXaxis().FindBin(args.x_max)
            SIDIS_signal_x_low = proj_data_exclz.GetXaxis().FindBin(args.z_tot_cut_SIDIS)
            Exclz_signal_x_low = proj_data_exclz.GetXaxis().FindBin(args.z_tot_cut)
            count_empty = 0
            def Kinematic_Bin_Factors_Get(List_of_HistosB={}, List_of_Factors={}, Kinematic_Bin="All", count_empty=0):
                TEMP_clone_mdf_SIDIS  = proj_mdf_SIDIS.Clone(f"proj_mdf_SIDIS_Bin_{Kinematic_Bin}")
                TEMP_clone_mdf_exclz  = proj_mdf_exclz.Clone(f"proj_mdf_exclz_Bin_{Kinematic_Bin}")
                TEMP_clone_mdf_exbkg  = proj_mdf_exbkg.Clone(f"proj_mdf_exbkg_Bin_{Kinematic_Bin}")
                TEMP_clone_data_SIDIS = proj_data_SIDIS.Clone(f"proj_data_SIDIS_Bin_{Kinematic_Bin}")
                TEMP_clone_data_exclz = proj_data_exclz.Clone(f"proj_data_exclz_Bin_{Kinematic_Bin}")
                TEMP_clone_harut_excl = proj_harut_excl.Clone(f"proj_harut_excl_Bin_{Kinematic_Bin}")
                if(Kinematic_Bin in ["All"]):
                    Y_mdf__clean = TEMP_clone_mdf_SIDIS.Integral(min_x_plots,  SIDIS_signal_x_low, 0, -1)
                    Y_data_clean = TEMP_clone_data_SIDIS.Integral(min_x_plots, SIDIS_signal_x_low, 0, -1)
                else:
                    Y_mdf__clean = TEMP_clone_mdf_SIDIS.Integral(min_x_plots,  SIDIS_signal_x_low, int(Kinematic_Bin), int(Kinematic_Bin))
                    Y_data_clean = TEMP_clone_data_SIDIS.Integral(min_x_plots, SIDIS_signal_x_low, int(Kinematic_Bin), int(Kinematic_Bin))
                alpha_SIDIS = Y_data_clean/Y_mdf__clean if(Y_mdf__clean > 0) else 0.0
                # N_sdf       = Y_data_clean/Y_mdf__clean if(Y_mdf__clean > 0) else 0.0
                data_excl_subt = TEMP_clone_data_exclz.Clone(f"data_excl_subt_Bin_{Kinematic_Bin}")
                if(args.subtract_background):
                    # data_excl_subt.Add(TEMP_clone_mdf_exbkg, -alpha_SIDIS)
                    data_excl_subt.Add(TEMP_clone_mdf_exbkg, -1)
                    for     ix in range(0, TEMP_clone_data_exclz.GetNbinsX() + 2):
                        for iy in range(0, TEMP_clone_data_exclz.GetNbinsY() + 2):
                            if(data_excl_subt.GetBinContent(ix, iy) < 0):
                                data_excl_subt.SetBinContent(ix, iy, 0.0)
                true_harut_excl = TEMP_clone_harut_excl.Clone(f"true_harut_excl_Bin_{Kinematic_Bin}")
                if(args.add_background):
                    TEMP_clone_harut_excl.Add(TEMP_clone_mdf_exbkg, alpha_SIDIS)
                    # for     y_val in range(0, TEMP_clone_harut_excl.GetYaxis().GetNbins()):
                    #     for x_val in range(0, TEMP_clone_harut_excl.GetXaxis().GetNbins()):
                    #         TEMP_clone_harut_excl.SetBinContent(x_val, y_val, true_harut_excl.GetBinContent(x_val, y_val) + (alpha_SIDIS*proj_mdf_ebkg.GetBinContent(x_val, y_val)))
                if(Kinematic_Bin in ["All"]):
                    N_data_vis  = data_excl_subt.Integral(Exclz_signal_x_low,        max_x_plots, 0, -1)
                    N_harut_vis = TEMP_clone_harut_excl.Integral(Exclz_signal_x_low, max_x_plots, 0, -1)
                    N_data_side = TEMP_clone_data_SIDIS.Integral(Exclz_signal_x_low, max_x_plots, 0, -1)
                    N_mdf_peak  = TEMP_clone_mdf_SIDIS.Integral(Exclz_signal_x_low,  max_x_plots, 0, -1)
                else:
                    N_data_vis  = data_excl_subt.Integral(Exclz_signal_x_low,        max_x_plots, int(Kinematic_Bin), int(Kinematic_Bin))
                    N_harut_vis = TEMP_clone_harut_excl.Integral(Exclz_signal_x_low, max_x_plots, int(Kinematic_Bin), int(Kinematic_Bin))
                    N_data_side = TEMP_clone_data_SIDIS.Integral(Exclz_signal_x_low, max_x_plots, int(Kinematic_Bin), int(Kinematic_Bin))
                    N_mdf_peak  = TEMP_clone_mdf_SIDIS.Integral(Exclz_signal_x_low,  max_x_plots, int(Kinematic_Bin), int(Kinematic_Bin))
                N_rho = N_data_vis/N_harut_vis    if(N_harut_vis > 0) else 0.0
                # N_edf = N_data_vis/N_harut_vis   if(N_harut_vis > 0) else 0.0
                alpha_Exclz = N_rho / alpha_SIDIS if(alpha_SIDIS > 0) else 0.0
                # final_factor = N_rho / alpha_SIDIS if(alpha_SIDIS > 0) else 0.0
                # if((args.verbose) or (0 in [N_data_vis, N_harut_vis, N_data_side, N_mdf_peak, N_rho, Y_mdf__clean, Y_data_clean, alpha_SIDIS, alpha_Exclz])):
                # if((args.verbose) or (0 in [N_data_vis, N_harut_vis, N_rho, Y_mdf__clean, Y_data_clean, alpha_SIDIS, alpha_Exclz])):
                #     if(0 in [N_data_vis, N_harut_vis, N_data_side, N_mdf_peak, N_rho, Y_mdf__clean, Y_data_clean, alpha_SIDIS, alpha_Exclz]):
                # if((args.verbose) or ((0 in [alpha_Exclz]) and (0 not in [alpha_SIDIS]))):
                #     if(0 in [alpha_Exclz]):
                if((args.verbose) or (0 in [N_rho, alpha_SIDIS, alpha_Exclz])):
                    if(0 in [N_rho, alpha_SIDIS, alpha_Exclz]):
                        count_empty += 1
                        print(f"\n\n{color.ERROR}WARNING{color.END_e}: The following bin has a factor/bin count equal to 0!{color.END_B} (Current Total of Empty Bins/Factors = {count_empty}){color.END}")
                    print(f"{ color.BOLD }\t=     BIN {Kinematic_Bin}    =\t{color.END}\n")
                    print(f"{ color.BOLD }N_data_vis (exclusive signal region)              : {color.Error if(N_data_vis   == 0) else ''}{N_data_vis:>12.0f}{color.END}")
                    print(f"{ color.BOLD }N_harut_vis (Harut signal)                        : {color.Error if(N_harut_vis  == 0) else ''}{N_harut_vis:>12.0f}{color.END}")
                    print(f"{ color.BOLD }N_data_side (SIDIS+exclusive above z_tot cut)     : {color.Error if(N_data_side  == 0) else ''}{N_data_side:>12.0f}{color.END}")
                    print(f"{ color.END  }N_mdf_peak (clasdis in exclusive signal region)   : {color.Error if(N_mdf_peak   == 0) else ''}{N_mdf_peak:>12.0f}{color.END}")
                    # N_mdf_side  = TEMP_clone_mdf_SIDIS.Integral(Exclz_signal_x_low, signal_x_high, y_bin_0, y_bin_0)
                    # print(f"{ color.BOLD }N_mdf_side (clasdis SIDIS in exclusive region)    : {N_mdf_side:>12.0f}{color.END}")
                    # alpha = N_data_side / N_mdf_side  if(N_mdf_side  > 0) else 0.0
                    # print(f"{ color.BOLD }alpha (sideband factor = N_data_side/N_mdf_side)  : {alpha:.4f}{color.END}")
                    print(f"{color.BGREEN}N_rho         (brings Harut's files to data)      : {color.Error if(N_rho        == 0) else ''}{N_rho:>12.6f}{color.END}")
                    print(f"{ color.BOLD }Y_mdf__clean  (SIDIS MC, exclusive_rho==0)        : {color.Error if(Y_mdf__clean == 0) else ''}{Y_mdf__clean:>12.0f}{color.END}")
                    print(f"{ color.BOLD }Y_data_clean  (DATA SIDIS, non-exclusive)         : {color.Error if(Y_data_clean == 0) else ''}{Y_data_clean:>12.0f}{color.END}")
                    print(f"{color.BGREEN}alpha_SIDIS (brings clasdis files to data)        : {color.Error if(alpha_SIDIS  == 0) else ''}{alpha_SIDIS:>12.6f}{color.END}")
                    print(f"{ color.BBLUE}alpha_Exclz (Harut scaled to SIDIS MC level)      : {color.Error if(alpha_Exclz  == 0) else ''}{alpha_Exclz:>12.6f}{color.END}")
                    print(f"{ color.BOLD }\t= END OF BIN {Kinematic_Bin} =\t{color.END}\n")
                List_of_Factors[Kinematic_Bin] = {"N_edf": N_rho, "N_sdf": alpha_SIDIS, "final_factor": alpha_Exclz, "N_data_vis": N_data_vis, "N_harut_vis": N_harut_vis, "N_data_side": N_data_side, "N_mdf_peak": N_mdf_peak, "Y_mdf__clean": Y_mdf__clean, "Y_data_clean": Y_data_clean}
                if(Kinematic_Bin in ["All"]):
                    List_of_HistosB[Kinematic_Bin] = {"proj_mdf_SIDIS":  TEMP_clone_mdf_SIDIS.ProjectionX(f"proj_mdf_SIDIS_1D_Binned_{Kinematic_Bin}"),
                                                      "proj_mdf_exclz":  TEMP_clone_mdf_exclz.ProjectionX(f"proj_mdf_exclz_1D_Binned_{Kinematic_Bin}"),
                                                      "proj_mdf_exbkg":  TEMP_clone_mdf_exbkg.ProjectionX(f"proj_mdf_exbkg_1D_Binned_{Kinematic_Bin}"),
                                                      "proj_data_SIDIS": TEMP_clone_data_SIDIS.ProjectionX(f"proj_data_SIDIS_1D_Binned_{Kinematic_Bin}"),
                                                      "proj_data_exclz": TEMP_clone_data_exclz.ProjectionX(f"proj_data_exclz_1D_Binned_{Kinematic_Bin}"),
                                                      "proj_harut_excl": TEMP_clone_harut_excl.ProjectionX(f"proj_harut_excl_1D_Binned_{Kinematic_Bin}"),
                                                      "data_excl_subt":  data_excl_subt.ProjectionX(f"data_excl_subt_1D_Binned_{Kinematic_Bin}"),
                                                      "true_harut_excl": true_harut_excl.ProjectionX(f"true_harut_excl_1D_Binned_{Kinematic_Bin}")}
                else:
                    List_of_HistosB[Kinematic_Bin] = {"proj_mdf_SIDIS":  TEMP_clone_mdf_SIDIS.ProjectionX(f"proj_mdf_SIDIS_1D_Binned_{Kinematic_Bin}",   int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "proj_mdf_exclz":  TEMP_clone_mdf_exclz.ProjectionX(f"proj_mdf_exclz_1D_Binned_{Kinematic_Bin}",   int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "proj_mdf_exbkg":  TEMP_clone_mdf_exbkg.ProjectionX(f"proj_mdf_exbkg_1D_Binned_{Kinematic_Bin}",   int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "proj_data_SIDIS": TEMP_clone_data_SIDIS.ProjectionX(f"proj_data_SIDIS_1D_Binned_{Kinematic_Bin}", int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "proj_data_exclz": TEMP_clone_data_exclz.ProjectionX(f"proj_data_exclz_1D_Binned_{Kinematic_Bin}", int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "proj_harut_excl": TEMP_clone_harut_excl.ProjectionX(f"proj_harut_excl_1D_Binned_{Kinematic_Bin}", int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "data_excl_subt":  data_excl_subt.ProjectionX(f"data_excl_subt_1D_Binned_{Kinematic_Bin}",         int(Kinematic_Bin), int(Kinematic_Bin)),
                                                      "true_harut_excl": true_harut_excl.ProjectionX(f"true_harut_excl_1D_Binned_{Kinematic_Bin}",       int(Kinematic_Bin), int(Kinematic_Bin))}
                return List_of_HistosB, List_of_Factors, count_empty
            Full_List_of_HistosB, Full_List_of_Factors, count_empty = Kinematic_Bin_Factors_Get(List_of_HistosB=Full_List_of_HistosB, List_of_Factors=Full_List_of_Factors, Kinematic_Bin="All", count_empty=count_empty)
            if(getattr(args, "Kinematic_Bin_Select", "Full") not in ["All"]):
                for kinematic_bins in range(0, proj_mdf_SIDIS.GetYaxis().GetNbins()):
                    if(getattr(args, "Kinematic_Bin_Select", "Full") not in ["Full", str(kinematic_bins), kinematic_bins]):
                        continue
                    Full_List_of_HistosB, Full_List_of_Factors, count_empty = Kinematic_Bin_Factors_Get(List_of_HistosB=Full_List_of_HistosB, List_of_Factors=Full_List_of_Factors, Kinematic_Bin=kinematic_bins, count_empty=count_empty)
                if(getattr(args, "Kinematic_Bin_Select", "Full") in ["Full"]):
                    print(f"\n\n{color.BBLUE}Done Running all Kinematic Bins.{color.END}")
                    if(count_empty != 0):
                        print(f"{color.Error}WARNING:{color.END_R} A total of {color.ERROR}{count_empty} out of {proj_mdf_SIDIS.GetYaxis().GetNbins()}{color.END_R} Bins had a empty bin/normalization factor {color.END_B}(this represents {(count_empty/proj_mdf_SIDIS.GetYaxis().GetNbins())*100:>3.2f}% of the total number of bins){color.END}")
                    print("\n\n")
                    
            # === SAVE PER-BIN C++ WEIGHT FUNCTION (for gInterpreter.Declare) ===
            weight_filename = f"exclusive_rho_weights_lund{'rho' if(args.old_lund) else 'vpk'}_{args.name if(args.name) else 'UnNamed'}.txt"
            if(not args.no_save):
                with open(weight_filename, "w") as f:
                    f.write(f"// Auto-generated per-kinematic-bin weight function for Harut's 'lund{'rho' if(args.old_lund) else 'vpk'}' files\n")
                    f.write("   // Generated by {} on {}\n".format(Name_of_Script, datetime.now().strftime("%m-%d-%Y %H:%M:%S")))
                    f.write(f"   // Used:\n\t   // z_tot_cut (exclusive) = {args.z_tot_cut}\n\t   // z_tot_cut_SIDIS = {args.z_tot_cut_SIDIS}\n\t   // SIDIS Background {'Subtracted from Exclusive Data' if(args.subtract_background) else 'Added to Exclusive rho0 MC' if(args.add_background) else "Ignored"}\n")
                    f.write("double exclusive_rho_weight_function(int kin_bin) {\n")
                    f.write("    switch(kin_bin) {\n")
                    for bin_num in Full_List_of_Factors:
                        if(bin_num in ["All"]):
                            continue
                        factor = Full_List_of_Factors[bin_num]["final_factor"]
                        variable_bin_num = int(proj_mdf_SIDIS.GetYaxis().GetBinCenter(bin_num))
                        f.write(f"        case {variable_bin_num}: return {factor:.8f};\n")
                    f.write("        default: return 1.0;\n")
                    f.write("    }\n")
                    f.write("}\n")
                print(f"{color.BGREEN}Saved per-bin C++ weight function to: {weight_filename}{color.END}")
            canvas = Create_Images(args, Full_List_of_HistosB, Full_List_of_Factors, Kinematic_Bin=getattr(args, "Kinematic_Bin_Select", "Full"), proj_data_full_for_plot=proj_data_full_for_plot)
            file1.Close()
            file2.Close()
            return canvas
        else:
            # print(f"args.z_tot_cut = {args.z_tot_cut}")
            # print(f"args.x_min     = {args.x_min}")
            min_x_plots        = proj_data_excl.GetXaxis().FindBin(args.x_min)
            SIDIS_signal_x_low = proj_data_excl.GetXaxis().FindBin(args.z_tot_cut_SIDIS)
            Exclz_signal_x_low = proj_data_excl.GetXaxis().FindBin(args.z_tot_cut)
            signal_x_high = proj_data_excl.GetXaxis().FindBin(args.x_max)
            # signal_x_high = proj_data_excl.GetXaxis().GetNbins()
            # print(f"min_x_plots   = {min_x_plots}")
            # print(f"SIDIS_signal_x_low  = {SIDIS_signal_x_low}")
            # print(f"signal_x_high = {signal_x_high}")
            y_bin_0 = proj_data_excl.GetYaxis().FindBin(0.0)
            y_bin_1 = proj_data_excl.GetYaxis().FindBin(1.0)

            Y_mdf_clean  = proj_mdf_SIDIS.Integral(min_x_plots,  SIDIS_signal_x_low, y_bin_0, y_bin_0)
            Y_data_clean = proj_data_SIDIS.Integral(min_x_plots, SIDIS_signal_x_low, y_bin_0, y_bin_0)
            N_sdf        = Y_data_clean / Y_mdf_clean if(Y_mdf_clean > 0) else 0.0
            
            data_excl_subt = proj_data_excl.Clone("data_excl_subt")
            if(args.subtract_background):
                # for     y_val in range(0, proj_data_excl.GetYaxis().GetNbins()):
                for x_val in range(0, proj_data_excl.GetXaxis().GetNbins()):
                    if(proj_data_excl.GetBinContent(x_val, y_bin_1) > (N_sdf*proj_mdf_ebkg.GetBinContent(x_val, y_bin_0))):
                        data_excl_subt.SetBinContent(x_val, y_bin_1, proj_data_excl.GetBinContent(x_val, y_bin_1) - (N_sdf*proj_mdf_ebkg.GetBinContent(x_val, y_bin_0)))
                    else:
                        data_excl_subt.SetBinContent(x_val, y_bin_1, 0)
                    # print(f"proj_data_excl.GetBinContent({x_val}, {y_bin_1})      = {proj_data_excl.GetBinContent(x_val, y_bin_1)}")
                    # print(f"N_sdf*proj_mdf_ebkg.GetBinContent({x_val}, {y_bin_0}) = {N_sdf*proj_mdf_ebkg.GetBinContent(x_val, y_bin_0)}")
                    # print(f"data_excl_subt.GetBinContent({x_val}, {y_bin_1}) = {proj_data_excl.GetBinContent(x_val, y_bin_1) - (N_sdf*proj_mdf_ebkg.GetBinContent(x_val, y_bin_0))}")
                    # print("")
            true_harut_excl = proj_harut_excl.Clone("true_harut_excl")
            if(args.add_background):
                for x_val in range(0, proj_harut_excl.GetXaxis().GetNbins()):
                    proj_harut_excl.SetBinContent(x_val, y_bin_1, true_harut_excl.GetBinContent(x_val, y_bin_1) + (N_sdf*proj_mdf_ebkg.GetBinContent(x_val, y_bin_0)))

            # N_data_vis  = proj_data_excl.Integral(Exclz_signal_x_low,  signal_x_high, y_bin_1, y_bin_1)
            N_data_vis  = data_excl_subt.Integral(Exclz_signal_x_low,  signal_x_high, y_bin_1, y_bin_1)
            N_harut_vis = proj_harut_excl.Integral(Exclz_signal_x_low, signal_x_high, y_bin_1, y_bin_1)
            N_data_side = proj_data_SIDIS.Integral(Exclz_signal_x_low, signal_x_high, 0, -1)

            # mdf contributions around the exclusive region
            N_mdf_peak  = proj_mdf_SIDIS.Integral(Exclz_signal_x_low, signal_x_high, y_bin_1, y_bin_1)

            N_edf = N_data_vis  / N_harut_vis if(N_harut_vis > 0) else 0.0
            final_factor = N_edf / N_sdf      if(N_sdf       > 0) else 0.0

            # Print everything
            print(f"{ color.BOLD }N_data_vis (exclusive signal region)              : {N_data_vis:>12.0f}{color.END}")
            print(f"{ color.BOLD }N_harut_vis (Harut signal)                        : {N_harut_vis:>12.0f}{color.END}")
            print(f"{ color.BOLD }N_data_side (SIDIS+exclusive above z_tot cut)     : {N_data_side:>12.0f}{color.END}")
            print(f"{ color.END  }N_mdf_peak (clasdis in exclusive signal region)   : {N_mdf_peak:>12.0f}{color.END}")
            # N_mdf_side  = proj_mdf_SIDIS.Integral(Exclz_signal_x_low, signal_x_high, y_bin_0, y_bin_0)
            # print(f"{ color.BOLD }N_mdf_side (clasdis SIDIS in exclusive region)    : {N_mdf_side:>12.0f}{color.END}")
            # alpha = N_data_side / N_mdf_side  if(N_mdf_side  > 0) else 0.0
            # print(f"{ color.BOLD }alpha (sideband factor = N_data_side/N_mdf_side)  : {alpha:.4f}{color.END}")
            print(f"{color.BGREEN}N_edf (brings Harut's files to data)              : {N_edf:>12.6f}{color.END}")
            print(f"{ color.BOLD }Y_mdf_clean   (SIDIS MC, exclusive_rho==0)        : {Y_mdf_clean:>12.0f}{color.END}")
            print(f"{ color.BOLD }Y_data_clean  (DATA SIDIS, non-exclusive)         : {Y_data_clean:>12.0f}{color.END}")
            print(f"{color.BGREEN}N_sdf (brings clasdis files to data)              : {N_sdf:>12.6f}{color.END}")
            print(f"{ color.BBLUE}final_factor (Harut scaled to SIDIS MC level)     : {final_factor:>12.6f}{color.END}")
            print(f"{ color.BOLD }=== End of normalization procedure ==={color.END}\n")
            
            args.N_edf = N_edf
            args.N_sdf = N_sdf
            args.final_factor = final_factor
    else:
        args.final_factor = 0.0

    # bin-based integration that respects the applied ranges (kept for compatibility)
    # proj_data_excl.GetXaxis().SetRange(0, 0)
    # x_low1  = proj_data_excl.GetXaxis().FindBin(args.x_min)
    # x_high1 = proj_data_excl.GetXaxis().FindBin(args.x_max)
    # y_low1  = proj_data_excl.GetYaxis().FindBin(args.y_min)
    # y_high1 = proj_data_excl.GetYaxis().FindBin(args.y_max)
    # weighted_count1 = proj_data_excl.Integral(x_low1, x_high1, y_low1, y_high1)
    x_low1  = data_excl_subt.GetXaxis().FindBin(args.x_min)
    x_high1 = data_excl_subt.GetXaxis().FindBin(args.x_max)
    y_low1  = data_excl_subt.GetYaxis().FindBin(args.y_min)
    y_high1 = data_excl_subt.GetYaxis().FindBin(args.y_max)
    weighted_count1 = data_excl_subt.Integral(x_low1, x_high1, y_low1, y_high1)
    # proj_harut_excl.GetXaxis().SetRange(0, 0)
    x_low2  = proj_harut_excl.GetXaxis().FindBin(args.x_min)
    x_high2 = proj_harut_excl.GetXaxis().FindBin(args.x_max)
    y_low2  = proj_harut_excl.GetYaxis().FindBin(args.y_min)
    y_high2 = proj_harut_excl.GetYaxis().FindBin(args.y_max)
    weighted_count2 = proj_harut_excl.Integral(x_low2, x_high2, y_low2, y_high2)

    # === PLOTTING SECTION (independent of normalization calculations) ===
    if(args.verbose or (str(args.vars).lower() in ["q2xb"])):
        print("")
        print(f"{color.BOLD}Weighted event count for first histogram (inside selected ranges):  {color.UNDERLINE}{weighted_count1}{color.END}")
        print(f"{color.BOLD}Weighted event count for second histogram (inside selected ranges): {color.UNDERLINE}{weighted_count2}{color.END}")
        print("")

    title_common = f"#splitline{{Plot of Q^{{2}} vs x_{{B}} For #rho^{{0}} Normalization}}{{#splitline{{{args.y_min:.2f} < Q^{{2}} < {args.y_max:.2f}}}{{{args.x_min:.2f} < x_{{B}} < {args.x_max:.2f}}}}}" if(str(args.vars).lower() in ["q2xb"]) else "Plot of z_{1}+z_{2} For #rho^{0} Normalization"
    title1 = f"#splitline{{#splitline{{#scale[1.2]{{From {'clasdis MC' if(str(args.vars).lower() in ['q2xb']) else 'Experimental Data'}}}}}{{{title_common}}}}}{{#scale[0.8]{{Weighted events: {weighted_count1:.0f}}}}}"
    title2 = f"#splitline{{#splitline{{#scale[1.2]{{From Harut's Files}}}}{{{title_common}}}}}{{#scale[0.8]{{Weighted events: {weighted_count2:.0f}}}}}"
    title1 = f"#splitline{{{title1}}}{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}"
    title2 = f"#splitline{{{title2}}}{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}"
    # proj_data_excl.SetTitle(f"#splitline{{{title1}}}{{{args.title}}}"  if(args.title) else title1)
    data_excl_subt.SetTitle(f"#splitline{{{title1}}}{{{args.title}}}"  if(args.title) else title1)
    proj_harut_excl.SetTitle(f"#splitline{{{title2}}}{{{args.title}}}" if(args.title) else title2)

    if(not args.no_save):
        print(f"\n{color.BOLD}Setting up drawing style and saving histograms in {args.draw_mode} mode...{color.END}\n")
        ROOT.gROOT.SetBatch(True)
        suffix = f"_{args.name}" if(args.name) else ""
        fmt = args.file_format.lower()

        if(args.draw_mode in ["2D", "1D_dif"]):
            if(args.draw_mode in ["1D_dif"]):
                # hist1 = proj_data_excl.ProjectionX("proj_y_1")
                hist1 = data_excl_subt.ProjectionX("proj_y_1")
                hist2 = proj_harut_excl.ProjectionX("proj_y_2")
                hist1.SetLineColor(ROOT.kRed)
                hist2.SetLineColor(ROOT.kBlue)
                hist1.SetLineWidth(2)
                hist2.SetLineWidth(2)
            else:
                hist1 = data_excl_subt # proj_data_excl
                hist2 = proj_harut_excl

            hist1.GetXaxis().SetRangeUser(args.x_min, args.x_max)
            hist1.GetYaxis().SetRangeUser(args.y_min, args.y_max)
            hist2.GetXaxis().SetRangeUser(args.x_min, args.x_max)
            hist2.GetYaxis().SetRangeUser(args.y_min, args.y_max)

            ROOT.gStyle.SetOptStat(111111)
            out_file1 = f"Plot_of_{args.vars}_for_rho0_Norm_Main_File{suffix}.{fmt}"
            out_file2 = f"Plot_of_{args.vars}_for_rho0_Norm_Harut{suffix}.{fmt}"

            canvas1 = ROOT.TCanvas("c1", "", 800, 600)
            if(args.draw_mode not in ["1D_dif"]):
                ROOT.gPad.SetLogz(1)
            hist1.Draw("colz" if(args.draw_mode not in ["1D_dif"]) else "hist")
            canvas1.SaveAs(out_file1)
            print(f"{color.BOLD}Saved first histogram canvas to: {color.BPINK}{out_file1}{color.END}")

            canvas2 = ROOT.TCanvas("c2", "", 800, 600)
            if(args.draw_mode not in ["1D_dif"]):
                ROOT.gPad.SetLogz(1)
            hist2.Draw("colz" if(args.draw_mode not in ["1D_dif"]) else "hist")
            canvas2.SaveAs(out_file2)
            print(f"{color.BOLD}Saved second histogram canvas to: {color.BPINK}{out_file2}{color.END}")

        else:  # 1D mode - use loose projections for the diagnostic plot
            # proj_data_full_for_plot.GetXaxis().SetRange(0, 0)
            # proj_data__1d = proj_data_full_for_plot.ProjectionX("proj_y_1", x_low1, x_high1)
            proj_data__1d = proj_data_full_for_plot.ProjectionX("proj_y_1")
            proj_data__1d.SetLineColor(ROOT.kRed)
            proj_data__1d.SetLineWidth(2)
            # proj_harutfull_for_plot.GetXaxis().SetRange(0, 0)
            # proj_harut_1d = proj_harutfull_for_plot.ProjectionX("proj_y_2", x_low2, x_high2)
            # proj_harut_1d = proj_harutfull_for_plot.ProjectionX("proj_y_2")
            proj_harut_1d = proj_harut_excl.ProjectionX("proj_y_2")
            proj_harut_1d.SetLineColor(ROOT.kCyan+3)
            proj_harut_1d.SetLineWidth(1)
            proj_harut_1d.SetLineStyle(2)

            # title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}}}"
            title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{SIDIS Region Cutoff was z_{{1}}+z_{{2}} < {args.z_tot_cut_SIDIS}}}}}"
            proj_data__1d.SetTitle(f"#splitline{{{title}}}{{{args.title}}}")
            # proj_data__1d.GetXaxis().SetRangeUser(args.x_min, args.x_max)
            # proj_harut_1d.GetXaxis().SetRangeUser(args.x_min, args.x_max)

            # Data Exclusive portion (using the same tight cut as normalization)
            # proj_data_full_for_plot.GetXaxis().SetRange(x_low1, x_high1)
            # hist_data_excl = proj_data_full_for_plot.ProjectionX("hist_data_excl", y_bin_1, y_bin_1)
            # proj_data_excl.GetXaxis().SetRange(Exclz_signal_x_low,  signal_x_high)
            # proj_data_excl.GetXaxis().SetRange(0, 0)

            
            hist_data_wbkg = proj_data_excl.ProjectionX("hist_data_wbkg", y_bin_1, y_bin_1)
            hist_data_wbkg.SetLineColor(ROOT.kOrange)
            hist_data_wbkg.SetLineWidth(2)
            hist_data_wbkg.SetLineStyle(2)
            
            hist_data_excl = data_excl_subt.ProjectionX("hist_data_excl", y_bin_1, y_bin_1)
            hist_data_excl.SetLineColor(ROOT.kRed)
            hist_data_excl.SetLineWidth(2)
            hist_data_excl.SetLineStyle(1)

            # Data SIDIS portion (using the same tight cut as normalization)
            # proj_data_full_for_plot.GetXaxis().SetRange(x_low1, x_high1)
            # proj_data_full_for_plot.GetXaxis().SetRange(0, 0)
            # hist_data_sidis = proj_data_full_for_plot.ProjectionX("hist_data_sidis", y_bin_0, y_bin_0)
            # hist_data_sidis = proj_data_full_for_plot.ProjectionX("hist_data_sidis")
            hist_data_sidis = proj_data_SIDIS.ProjectionX("hist_data_sidis", y_bin_0, y_bin_0)
            # proj_data_full_for_plot.GetXaxis().SetRange(0, 0)
            hist_data_sidis.SetLineColor(ROOT.kCyan)
            hist_data_sidis.SetLineWidth(2)
            hist_data_sidis.SetLineStyle(2)

            
            proj_harut_1d_norm = proj_harut_1d.Clone("proj_harut_1d_norm")
            proj_harut_1d_norm.Scale(args.N_edf)
            proj_harut_1d_norm.SetLineColor(ROOT.kGreen)
            proj_harut_1d_norm.SetLineStyle(1)
            proj_harut_1d_norm.SetLineWidth(3)

            # proj_mdf_SIDIS.GetXaxis().SetRange(0, 0)
            # hist_clasdis_norm = proj_mdf_SIDIS.ProjectionX("hist_clasdis_norm", x_low1, x_high1)
            hist_clasdis_norm = proj_mdf_SIDIS.ProjectionX("hist_clasdis_norm", y_bin_0, y_bin_0)
            hist_clasdis_norm.Scale(args.N_sdf)
            hist_clasdis_norm.SetLineColor(ROOT.kBlue)
            hist_clasdis_norm.SetLineWidth(2)

            hist_clasdis_excl = proj_mdf_excl.ProjectionX("hist_clasdis_excl", y_bin_1, y_bin_1)
            # hist_clasdis_excl = proj_mdf_excl.ProjectionX("hist_clasdis_excl")
            hist_clasdis_excl.Scale(args.N_sdf)
            hist_clasdis_excl.SetLineColor(ROOT.kBlack)
            hist_clasdis_excl.SetLineWidth(1)
            hist_clasdis_excl.SetLineStyle(2)

            
            hist_clasdis_ebkg = proj_mdf_ebkg.ProjectionX("hist_clasdis_ebkg", y_bin_0, y_bin_0)
            hist_clasdis_ebkg.Scale(args.N_sdf)
            hist_clasdis_ebkg.SetLineColor(ROOT.kOrange+2)
            hist_clasdis_ebkg.SetLineWidth(2)
            hist_clasdis_ebkg.SetLineStyle(1)

            hist_combined = hist_clasdis_norm.Clone("hist_combined")
            hist_combined.Add(proj_harut_1d_norm)
            hist_combined.SetLineColor(ROOT.kMagenta)
            hist_combined.SetLineWidth(2)
            hist_combined.SetLineStyle(1)

            true_harut_1d = true_harut_excl.ProjectionX("true_harut_1d")
            true_harut_1d.Scale(args.N_sdf)
            true_harut_1d.SetLineColor(ROOT.kPink+2)
            true_harut_1d.SetLineWidth(1)
            true_harut_1d.SetLineStyle(2)

            for hist_loop in [proj_data__1d, hist_clasdis_norm, proj_harut_1d, true_harut_1d, proj_harut_1d_norm, hist_combined, hist_data_excl, hist_data_wbkg, hist_data_sidis, hist_clasdis_excl]:
                hist_loop.GetXaxis().SetRangeUser(max([args.x_min, 0.1]), args.x_max)
                # hist_loop.GetXaxis().SetRangeUser(0.8, 1.05)

            out_file = f"Plot_of_{args.vars}_for_rho0_Norm_Combined_1D{suffix}.{fmt}"
            canvas = ROOT.TCanvas("c_combined", "", 900, 700)
            canvas.Divide(2, 1, 0.0001, 0.0001)
            canvas.SetGrid()
            ROOT.gStyle.SetAxisColor(16, 'xy')
            ROOT.gStyle.SetOptStat(0)
            Draw_Canvas(canvas, 1, left_add=0.125, right_add=0.025, up_add=0.1, down_add=0.075)
            y_max_cutoff = max([hist_clasdis_norm.GetMaximum(), hist_data_sidis.GetMaximum(), hist_clasdis_excl.GetMaximum()])
            # ROOT.gPad.SetLogy(1)
            # proj_data__1d.Draw("hist")
            hist_clasdis_norm.SetTitle(proj_data__1d.GetTitle())
            hist_clasdis_norm.GetXaxis().SetTitle(str(hist_clasdis_norm.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
            hist_clasdis_norm.GetYaxis().SetRangeUser(0, 1.05*y_max_cutoff)
            hist_clasdis_norm.Draw("hist same")
            # hist_combined.Draw("hist same")
            hist_data_sidis.Draw("hist same")
            # proj_harut_1d_norm.Draw("hist same")
            # # hist_data_excl.Draw("hist same")
            # hist_data_wbkg.Draw("hist same")
            hist_clasdis_excl.Draw("hist same")
            # hist_clasdis_ebkg.Draw("hist same")

            Cutoff_Line  = ROOT.TLine(args.z_tot_cut_SIDIS, 0.0, args.z_tot_cut_SIDIS, y_max_cutoff)
            Cutoff_Line.SetLineColor(ROOT.kGray+3)
            Cutoff_Line.SetLineStyle(1)
            Cutoff_Line.SetLineWidth(2)
            Cutoff_Line.Draw("same")
            
            legend_cd_1 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
            legend_cd_1.SetFillStyle(0)
            legend_cd_1.SetBorderSize(0)
            # # legend_cd_1.AddEntry(proj_data__1d,     "#scale[1.5]{Experimental Data (Full)}",                  "l")
            # legend_cd_1.AddEntry(hist_data_sidis,   "#scale[1.5]{Experimental Data (SIDIS)}",                 "l")
            # legend_cd_1.AddEntry(hist_clasdis_norm, "#scale[1.5]{clasdis SIDIS (Normalized)}",                "l")
            # # legend_cd_1.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized)}",                 "l")
            # legend_cd_1.AddEntry(hist_clasdis_excl, "#scale[1.5]{clasdis Exclusive #rho^{0} (Normalized)}",   "l")
            legend_cd_1.AddEntry(hist_data_sidis,   "#scale[0.75]{#splitline{Experimental Data}{(SIDIS)}}",                 "l")
            legend_cd_1.AddEntry(hist_clasdis_norm, "#scale[0.75]{#splitline{clasdis SIDIS}{(Normalized)}}",                "l")
            legend_cd_1.AddEntry(hist_clasdis_excl, "#scale[0.75]{#splitline{clasdis Exclusive #rho^{0}}{(Normalized)}}",   "l")
            legend_cd_1.Draw("same")
            # canvas.cd(2)
            Draw_Canvas(canvas, 2, left_add=0.095, right_add=0.025, up_add=0.1, down_add=0.075)
            Shared_Title = proj_data__1d.GetTitle()
            Shared_Title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}}}"
            Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}}}"
            # if(args.title not in ["", " "]):
            #     Shared_Title = Shared_Title.replace(args.title, f"#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}")
            # else:
            #     Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}}}"
            hist_clasdis_excl.SetTitle(Shared_Title)
            hist_clasdis_excl.GetXaxis().SetTitle(hist_clasdis_excl.GetXaxis().GetTitle().replace(" (Smeared)", ""))
            proj_harut_1d_norm.SetTitle(Shared_Title)
            proj_harut_1d_norm.GetXaxis().SetTitle(proj_harut_1d_norm.GetXaxis().GetTitle().replace(" (Smeared)", ""))
            hist_data_wbkg.SetTitle(Shared_Title)
            hist_data_wbkg.GetXaxis().SetTitle(hist_data_wbkg.GetXaxis().GetTitle().replace(" (Smeared)", ""))
            # hist_clasdis_excl.Draw("hist")

            y_max_cutoff = max([hist_data_wbkg.GetMaximum(), proj_harut_1d_norm.GetMaximum(), hist_clasdis_ebkg.GetMaximum()])
            hist_data_wbkg.GetYaxis().SetRangeUser(0, 1.15*y_max_cutoff)
            hist_data_wbkg.Draw("hist")
            proj_harut_1d_norm.Draw("hist same")
            if(args.subtract_background):
                hist_data_excl.Draw("hist same")
                y_max_cutoff = max([hist_data_excl.GetMaximum(), y_max_cutoff])
                # merged_excl_MCs = proj_harut_1d_norm.Clone("merged_excl_MCs")
                # merged_excl_MCs.Add(hist_clasdis_ebkg)
                # merged_excl_MCs.SetLineColor(ROOT.kViolet)
                # merged_excl_MCs.Draw("hist same")
            hist_clasdis_ebkg.Draw("hist same")
            # proj_harut_1d.Draw("hist same")
            if(args.add_background):
                true_harut_1d.Draw("hist same")
                y_max_cutoff = max([true_harut_1d.GetMaximum(), y_max_cutoff])
            # hist_data_subt = data_excl_subt.ProjectionX("hist_data_subt", y_bin_1, y_bin_1)
            # hist_data_subt.GetXaxis().SetRangeUser(max([args.x_min, 0.01]), args.x_max)
            # hist_data_subt.Draw("hist same")

            Cutoff_Line_Exclusive  = ROOT.TLine(args.z_tot_cut, 0.0, args.z_tot_cut, y_max_cutoff)
            Cutoff_Line_Exclusive.SetLineColor(ROOT.kGray+3)
            Cutoff_Line_Exclusive.SetLineStyle(1)
            Cutoff_Line_Exclusive.SetLineWidth(2)
            Cutoff_Line_Exclusive.Draw("same")
            
            legend_cd_2 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
            legend_cd_2.SetFillStyle(0)
            legend_cd_2.SetBorderSize(0)
            if(args.add_background):
                legend_cd_2.AddEntry(proj_harut_1d_norm, "#scale[2.0]{Harut Exclusive+clasdis SIDIS BKG}",    "l")
                legend_cd_2.AddEntry(true_harut_1d,      "#scale[1.65]{Harut Exclusive MC (w/out SIDIS BKG)}","l")
            else:
                legend_cd_2.AddEntry(proj_harut_1d_norm,"#scale[4.0]{Harut Exclusive MC}",                "l")
            # legend_cd_2.AddEntry(proj_harut_1d_norm,"#scale[1.5]{Harut Exclusive MC (Normalized)}",                "l")
            if(args.subtract_background):
                # legend_cd_2.AddEntry(hist_data_excl,"#scale[1.65]{Exclusive Experimental Data (w/out SIDIS BKG)}",   "l")
                legend_cd_2.AddEntry(hist_data_excl,"#scale[2.65]{#splitline{Exclusive Experimental Data}{(w/out SIDIS BKG)}}",   "l")
            legend_cd_2.AddEntry(hist_data_wbkg,    "#scale[2.65]{#splitline{Exclusive Experimental Data}{(with SIDIS BKG)}}",   "l")
            # legend_cd_2.AddEntry(hist_data_excl,    "#scale[1.5]{Experimental Data (Exclusive #rho^{0}})",         "l")
            # legend_cd_2.AddEntry(hist_clasdis_excl, "#scale[1.5]{clasdis Exclusive #rho^{0} (Normalized)}",        "l")
            legend_cd_2.AddEntry(hist_clasdis_ebkg, "#scale[3.65]{#splitline{clasdis BKG SIDIS}{in Exclusive Region}}",   "l")
            # legend_cd_2.AddEntry(hist_clasdis_ebkg, "#scale[1.575]{clasdis BKG SIDIS in Exclusive}",   "l")
            # legend_cd_2.AddEntry(proj_harut_1d,     "#scale[1.5]{Harut Exclusive MC (Raw)}",                       "l")
            # legend_cd_2.AddEntry(hist_clasdis_norm, "#scale[1.5]{clasdis SIDIS (Normalized to Data)}",             "l")
            # legend_cd_2.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized to Data)}",              "l")

            legend_cd_2.Draw("same")
            
            # Coordinates are NDC because of the "NDC" option
            box = ROOT.TPaveText(0.575, 0.55, 0.975, 0.65, "NDC")
            box.SetFillColor(0)      # white fill
            box.SetFillStyle(1001)   # solid fill
            box.SetBorderSize(1)
            # box.SetTextAlign(12)     # left/center
            box.SetTextAlign(22)      # centered horizontally and vertically
            # box.SetTextFont(42)
            box.SetTextFont(62)  # bold Helvetica
            box.SetTextSize(0.025)
            box.SetMargin(0.02)       # reduce left/right internal padding
            box.AddText("Normalization Factor to bring this")
            box.AddText("Exclusive MC to clasdis SIDIS:")
            box.AddText(f"{args.final_factor:.6f}")
            box.Draw()

            canvas.SaveAs(out_file)
            print(f"{color.BOLD}Saved combined 1D histogram canvas with legend to: {color.BPINK}{out_file}{color.END}")

            # === RATIO OF SCALED INTEGRALS (Z >= 32, FULL X RANGE, WITH Y-AXIS CUTS) ===
            y_bin_0  = h3d_mdf.GetYaxis().FindBin(0.0)   # SIDIS region
            y_bin_1  = h3d_mdf.GetYaxis().FindBin(1.0)   # Exclusive rho region
            z_bin_32 = h3d_mdf.GetZaxis().FindBin(32.0)
            # clasdis SIDIS: Y=0, Z>=32, full X
            raw_clasdis = h3d_mdf.Integral(0, -1, y_bin_0, y_bin_0, z_bin_32, -1)
            # Harut exclusive: Y=1, Z>=32, full X
            raw_harut   = h3d2.Integral(0, -1, y_bin_1, y_bin_1, z_bin_32, -1)
            scaled_clasdis = raw_clasdis * args.N_sdf
            scaled_harut   = raw_harut   * args.N_edf
            ratio = (scaled_harut / scaled_clasdis) if(scaled_clasdis > 0) else 0.0
            print(f"{color.BOLD}Ratio (Harut Y=1 Z>=32 / clasdis Y=0 Z>=32, scaled): {ratio:.5f}{color.END}")
            print(f"{color.BOLD}Harut's Exclusive Events (in the SIDIS region) makes up {color.UNDERLINE}{ratio*100:.3f}%{color.END_B} of the clasdis SIDIS Events{color.END}")
    else:
        print(f"\n{color.Error}No-save mode enabled: skipping drawing and file saving.{color.END}\n")

    file1.Close()
    file2.Close()
    print(f"\n{color.BBLUE}{Name_of_Script}{color.END_B} completed successfully.{color.END}\n")


def create_rho_normalized_diagnostic_plots(args, hist_list_in):
    print(f"\n{color.BBLUE}Applying rho0 normalization weights/background subtractions.{color.END}\n")
    scale_harut   = getattr(args, "n_rho_input", main_Get_rho_Normalization_values_Wpions(args))
    scale_clasdis = getattr(args, "alpha_SIDIS_input", 0.193244)
    histo_list_New = {}
    for hist_name in hist_list_in:
        if("rdf" in hist_name):
            histo_list_New[hist_name] = hist_list_in[hist_name]
        elif("mdf" in hist_name):
            histo_list_New[hist_name] = hist_list_in[hist_name]
            histo_list_New[f"{hist_name}_(Scaled)"] = hist_list_in[hist_name].Clone(f"{hist_name}_(Scaled)")
            histo_list_New[f"{hist_name}_(Scaled)"].Scale(scale_harut if("lund" in hist_name) else scale_clasdis)
    for     var_choice in ["(phi_t)_(Q2_y_z_pT_4D_Bins)", "(Q2)_(xB)", "(Q2)_(y)", "(W_pippim)_(MM_pippim)", "(z)_(pT)"]:
        for stage_name in ["Exclusive", "SIDIS_BKG", "SIDIS_2pi", "Min_ExclC", "Full_SIDIS"]:
            hist_key_data  = f"(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(exclusive_rho_individual)_{var_choice}_{stage_name}"
            hist_key_harut = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_{var_choice.replace(')', '_smeared)')}_({'lundvpk' if(not args.old_lund) else 'lundrho'})_{stage_name}_(Scaled)"
            if(all(names in histo_list_New for names in [hist_key_data, hist_key_harut])):
                histo_list_New[f"{hist_key_data}_(Removed_Background)"] = histo_list_New[hist_key_data].Clone(f"{hist_key_data}_(Removed_Background)")
                histo_list_New[f"{hist_key_data}_(Removed_Background)"].Add(histo_list_New[hist_key_harut], -1)
            else:
                raise SystemError(f"\n{color.Error}ERROR: Missing either '{hist_key_data}' OR '{hist_key_harut}'{color.END}\n")
    return histo_list_New

def make_diagnostic_cut_images(args):
    print(f"\n{color.BBLUE}Starting diagnostic cut-stage image creation...{color.END}")
    cut_stages = {
        "Exclusive": [23, 31, 55, 63, 87, 95, 119, 127, 151, 159, 183, 191, 215, 223, 247, 255],
        "SIDIS_BKG": [28, 30, 60, 62, 92, 94, 124, 126, 156, 158, 188, 190, 220, 222, 252, 254],
        "SIDIS_2pi": [132, 133, 134, 135, 140, 141, 142, 143, 148, 149, 150, 151, 156, 157, 158, 159, 164, 165, 166, 167, 172, 173, 174, 175, 180, 181, 182, 183, 188, 189, 190, 191, 196, 197, 198, 199, 204, 205, 206, 207, 212, 213, 214, 215, 220, 221, 222, 223, 228, 229, 230, 231, 236, 237, 238, 239, 244, 245, 246, 247, 252, 253, 254, 255],
        "Min_ExclC": [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55, 62, 63, 70, 71, 78, 79, 86, 87, 94, 95, 102, 103, 110, 111, 118, 119, 126, 127, 134, 135, 142, 143, 150, 151, 158, 159, 166, 167, 174, 175, 182, 183, 190, 191, 198, 199, 206, 207, 214, 215, 222, 223, 230, 231, 238, 239, 246, 247, 254, 255],
        "Full_SIDIS": list(range(128, 256))
    }
    cut_stages_clasdis = {
        "SIDIS_BKG": [28, 30, 60, 62, 92, 94, 124, 126, 156, 158, 188, 190, 220, 222, 252, 254],
        "SIDIS_2pi": [132, 134, 140, 142, 148, 150, 156, 158, 164, 166, 172, 174, 180, 182, 188, 190, 196, 198, 204, 206, 212, 214, 220, 222, 228, 230, 236, 238, 244, 246, 252, 254],
        "Min_ExclC": [6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102, 110, 118, 126, 134, 142, 150, 158, 166, 174, 182, 190, 198, 206, 214, 222, 230, 238, 246, 254],
        "Full_SIDIS": list(range(128, 256, 2))
    }
    file1 = ROOT.TFile.Open(args.file2)
    if((not file1) or (file1.IsZombie())):
        print(f"{color.Error}ERROR: Could not open {args.file2}{color.END}")
        return
    hist_list = {}
    for var_choice in ["(phi_t)_(Q2_y_z_pT_4D_Bins)", "(Q2)_(xB)", "(Q2)_(y)", "(W_pippim)_(MM_pippim)", "(z)_(pT)"]:
        hist_key_data  = f"(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(exclusive_rho_individual)_{var_choice}"
        hist_key_mdf   = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_{var_choice.replace(')', '_smeared)')}"
        hist_key_harut = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_{var_choice.replace(')', '_smeared)')}_({'lundvpk' if(not args.old_lund) else 'lundrho'})"
        hist_list[hist_key_data]  = file1.Get(hist_key_data)
        hist_list[hist_key_mdf]   = file1.Get(hist_key_mdf)
        hist_list[hist_key_harut] = file1.Get(hist_key_harut)
        for stage_name, z_bin_list in cut_stages.items():
            if(args.verbose):
                print(f"\n{color.BOLD}→ Processing {stage_name} ({len(z_bin_list)} Z-bins){color.END}")
            # Data projections
            hist_list[f"{hist_key_data}_{stage_name}"]    = project_z_bins_global(hist_list[hist_key_data],  f"{hist_key_data}_{stage_name}", z_bin_list, args, diagnostic=True)
            # Harut projections
            hist_list[f"{hist_key_harut}_{stage_name}"]   = project_z_bins_global(hist_list[hist_key_harut], f"{hist_key_harut}_{stage_name}", z_bin_list, args, diagnostic=True)
            # MDF/clasdis projections
            if(stage_name in cut_stages_clasdis):
                hist_list[f"{hist_key_mdf}_{stage_name}"] = project_z_bins_global(hist_list[hist_key_mdf],   f"{hist_key_mdf}_{stage_name}", cut_stages_clasdis[stage_name], args, diagnostic=True)
    file1.Close()
    if((not getattr(args, "extra_root_save", False)) and (not getattr(args, "no_save", False))):
        args_name = f'_{getattr(args, "name", "")}' if(getattr(args, "name", "") not in [""]) else ''
        root_name = f"Diagnostic_ROOT_File_for_2D_Histos_with_Cuts{args_name}.root"
        for remove in ["(", ")", " "]:
            root_name = root_name.replace(remove, "")
        out_file = ROOT.TFile.Open(root_name, "RECREATE")
        if((not out_file) or (out_file.IsZombie())):
            raise OSError(f"Could not create ROOT file: {root_name}")
        out_file.cd()
        for name, hist in hist_list.items():
            hist.Write(name)
        out_file.Close()
        print(f"{color.BGREEN}Saved a Sliced TH2D histogram as: {color.BBLUE}{root_name}{color.END}\n")
    hist_list = create_rho_normalized_diagnostic_plots(args, hist_list_in=hist_list)
    print(f"\n{color.BGREEN}All {len(hist_list)} diagnostic cut-stage histograms were created successfully.{color.END}\n")
    return hist_list

def Slice_4D_Histo_Bins_For_phi_h_Plots(args, Hist_In, Q2_Y_Bin_In, z_pT_Bin_In, Use_All_Name=False):
    bin_4D_val = Bin_Converter_4D_to_2D.get(f"Q2_y_bin_{Q2_Y_Bin_In}_z_pT_bin_{z_pT_Bin_In}", None)
    if(bin_4D_val is None):
        print(f"\n{color.Error}WARNING: Could not find {color.END_B}'Q2_y_bin_{Q2_Y_Bin_In}_z_pT_bin_{z_pT_Bin_In}'{color.Error} in 'Bin_Converter_4D_to_2D'.{color.END}\n")
        return None
    bin_4D_num = Hist_In.GetYaxis().FindBin(bin_4D_val)
    if(args.verbose):
        print(f"\n{color.BOLD}Q2_y_bin_{Q2_Y_Bin_In}_z_pT_bin_{z_pT_Bin_In} -> Q2_y_z_pT_4D_Bin_{bin_4D_val} -> Histo_Bin_{bin_4D_num}{color.END}")
    initial_name = Hist_In.GetName()
    for smearing_options in ["", "_smeared"]:
        initial_name = initial_name.replace(f"Q2_y_z_pT_4D_Bins{smearing_options}", f"Q2_y_bin_{Q2_Y_Bin_In})_(z_pT_bin_{z_pT_Bin_In if(not Use_All_Name) else 'All'}")
    Hist_Binned = Hist_In.ProjectionX(initial_name, int(bin_4D_num), int(bin_4D_num))
    Default_Title = f"#splitline{{Comparisons of #phi_{{h}} Distributions}}{{{args.title}}}"
    if(not Use_All_Name):
        Hist_Binned.SetTitle(f"#splitline{{{Default_Title}}}{{#scale[0.75]{{Q^{{2}}-y Bin {Q2_Y_Bin_In} #topbar z-P_{{T}} Bin {z_pT_Bin_In}}}}}")
    else:
        Hist_Binned.SetTitle(f"#splitline{{{Default_Title}}}{{#scale[0.8]{{Q^{{2}}-y Bin {Q2_Y_Bin_In}}}}}")
    Hist_Binned.GetXaxis().SetTitle(str(Hist_Binned.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    return Hist_Binned


def calculate_weighted_percentage(hist_a, hist_b):
    sum_a = hist_a.Integral()
    sum_b = hist_b.Integral()
    if(sum_a == 0):
        return 0.0  # Avoid division by zero
    percentage = (sum_b / sum_a) * 100.0
    return percentage

def phi_h_1D_Compare_in_z_pT_Images_Together(Hist_List_In, args, Q2_Y_Bin_Range=range(1,18), Comparison_Type="In_Data", stage_name="Full_SIDIS", Draw_Type="data_scale"):
    All_z_pT_Canvas, All_Histos, temp_hists, Ratios_of_Contaminations = {}, {}, {}, {}
    Ratios_of_Contaminations["Global"] = {"Sum_of_Percents": 0, "Number_of_Calcs": 0, "Min_Contamination": 1e10, "Min_Bin_Num": -1, "Max_Contamination": 0, "Max_Bin_Num": -1}
    fmt = f'.{getattr(args, "file_format", "pdf")}'.lower()
    # Q2_y_borders = {}
    hist_key_data_wBG  = f"(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(exclusive_rho_individual)_(phi_t)_(Q2_y_z_pT_4D_Bins)_{stage_name}"
    hist_key_data_woBG = f"{hist_key_data_wBG}_(Removed_Background)"
    hist_key_harut     = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_(phi_t_smeared)_(Q2_y_z_pT_4D_Bins_smeared)_({'lundvpk' if(not args.old_lund) else 'lundrho'})_{stage_name}_(Scaled)"
    hist_key_clasdis   = hist_key_harut.replace(f"_({'lundvpk' if(not args.old_lund) else 'lundrho'})", "")
    hist_data_wBG  = Hist_List_In.get(hist_key_data_wBG,  None)
    hist_data_woBG = Hist_List_In.get(hist_key_data_woBG, None)
    hist_harut     = Hist_List_In.get(hist_key_harut,     None)
    hist_clasdis   = Hist_List_In.get(hist_key_clasdis,   None)
    if(None in [hist_harut]):
        raise ValueError(f"{color.Error}Error: Missing '{hist_key_harut}'{color.END}")
    if((None in [hist_data_wBG, hist_data_woBG]) and (Comparison_Type in ["In_Data", "All_Data_Types"])):
        raise ValueError(f"{color.Error}Error: Missing either '{hist_key_data_wBG}' or '{hist_key_data_woBG}'{color.END}")
    if((None in [hist_clasdis])                  and (Comparison_Type in ["In_MCs",  "All_Data_Types"])):
        raise ValueError(f"{color.Error}Error: Missing '{hist_key_clasdis}'{color.END}")
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"rho0_Comparisons_of_phi_h_{Comparison_Type}_for_Q2_Y_Bin_{Q2_Y_Bin}_with_{stage_name}_Cuts"
        if(Draw_Type == "Normalized"):
            Save_Name = f"{Save_Name}_Normalized"
        Ratios_of_Contaminations[Save_Name] = {"Sum_of_Percents": 0, "Number_of_Calcs": 0, "Min_Contamination": 1e10, "Min_Bin_Num": -1, "Max_Contamination": 0, "Max_Bin_Num": -1}
        All_z_pT_Canvas[Save_Name] = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800*2), Size_Y=int(1500*2), cd_Space=0.01)
        All_z_pT_Canvas[Save_Name].SetFillColor(ROOT.kGray)
        if(args.verbose):
            print(f"{color.BBLUE}Creating TCanvas: {color.END_B}{Save_Name}{color.BBLUE}...{color.END}")
            # args.timer.time_elapsed()
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
        All_z_pT_Canvas_cd_2.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - Individual z-pT Bins  ###########################################################################################################################################################################################################################################################################################################################################################
        All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
        Integrated_Bin_Name_harut, Integrated_Bin_Name_data_wBG, Integrated_Bin_Name_data_woBG, Integrated_Bin_Name_clasdis = None, None, None, None
        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin)):
                continue
            try:
                All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(z_pT_Bin)
                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
                ROOT.gStyle.SetOptStat(0)
                Min_Content, Max_Content = 0, 0
                temp_hists["harut"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_harut, Q2_Y_Bin, z_pT_Bin, Use_All_Name=False)
                if(temp_hists["harut"] is None):
                    continue
                All_Histos[temp_hists["harut"].GetName()] = temp_hists["harut"]
                All_Histos[temp_hists["harut"].GetName()].SetLineWidth(3 if("png" in fmt) else 1)
                All_Histos[temp_hists["harut"].GetName()].SetLineColor(ROOT.kGreen)
                Min_Content = min([Min_Content, All_Histos[temp_hists["harut"].GetName()].GetBinContent(All_Histos[temp_hists["harut"].GetName()].GetMinimumBin())])
                Max_Content = max([Max_Content, All_Histos[temp_hists["harut"].GetName()].GetBinContent(All_Histos[temp_hists["harut"].GetName()].GetMaximumBin())])
                if(Integrated_Bin_Name_harut is None):
                    temp_hists["harut_All"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_harut, Q2_Y_Bin, z_pT_Bin, Use_All_Name=True)
                    Integrated_Bin_Name_harut = temp_hists["harut_All"].GetName()
                    All_Histos[Integrated_Bin_Name_harut] = temp_hists["harut_All"]
                    All_Histos[Integrated_Bin_Name_harut].SetLineWidth(3 if("png" in fmt) else 1)
                    All_Histos[Integrated_Bin_Name_harut].SetLineColor(ROOT.kGreen)
                else:
                    All_Histos[Integrated_Bin_Name_harut].Add(All_Histos[temp_hists["harut"].GetName()])

                if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                    temp_hists["data_wBG"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_data_wBG, Q2_Y_Bin, z_pT_Bin, Use_All_Name=False)
                    if(temp_hists["data_wBG"] is None):
                        continue
                    All_Histos[temp_hists["data_wBG"].GetName()] = temp_hists["data_wBG"]
                    All_Histos[temp_hists["data_wBG"].GetName()].SetLineWidth(3 if("png" in fmt) else 1)
                    All_Histos[temp_hists["data_wBG"].GetName()].SetLineColor(ROOT.kBlue)
                    Min_Content = min([Min_Content, All_Histos[temp_hists["data_wBG"].GetName()].GetBinContent(All_Histos[temp_hists["data_wBG"].GetName()].GetMinimumBin())])
                    Max_Content = max([Max_Content, All_Histos[temp_hists["data_wBG"].GetName()].GetBinContent(All_Histos[temp_hists["data_wBG"].GetName()].GetMaximumBin())])
                    Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"] = calculate_weighted_percentage(All_Histos[temp_hists["data_wBG"].GetName()], All_Histos[temp_hists["harut"].GetName()])
                    for ratio_checks in [Save_Name, "Global"]:
                        Ratios_of_Contaminations[ratio_checks]["Sum_of_Percents"]  += Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]
                        Ratios_of_Contaminations[ratio_checks]["Number_of_Calcs"]  += 1
                        if(min([Ratios_of_Contaminations[ratio_checks]["Min_Contamination"], Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]]) == Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]):
                            Ratios_of_Contaminations[ratio_checks]["Min_Contamination"]    = Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]
                            Ratios_of_Contaminations[ratio_checks]["Min_Bin_Num"]          = f"Bin_({Q2_Y_Bin}-{z_pT_Bin})"
                        if(max([Ratios_of_Contaminations[ratio_checks]["Max_Contamination"], Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]]) == Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]):
                            Ratios_of_Contaminations[ratio_checks]["Max_Contamination"]    = Ratios_of_Contaminations[Save_Name][f"Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})"]
                            Ratios_of_Contaminations[ratio_checks]["Max_Bin_Num"]          = f"Bin_({Q2_Y_Bin}-{z_pT_Bin})"
                    preContamination_Title = All_Histos[temp_hists["harut"].GetName()].GetTitle()
                    All_Histos[temp_hists["harut"].GetName()].SetTitle(f"#splitline{{{preContamination_Title}}}{{#scale[2]{{#splitline{{Percent of #rho^{{0}} Contamination in this Bin:}}{{{Ratios_of_Contaminations[Save_Name][f'Percent_Contamination_for_Bin_({Q2_Y_Bin}-{z_pT_Bin})']:.3f}%}}}}}}")
                    if(Integrated_Bin_Name_data_wBG is None):
                        temp_hists["data_wBG_All"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_data_wBG, Q2_Y_Bin, z_pT_Bin, Use_All_Name=True)
                        Integrated_Bin_Name_data_wBG = temp_hists["data_wBG_All"].GetName()
                        All_Histos[Integrated_Bin_Name_data_wBG] = temp_hists["data_wBG_All"]
                        All_Histos[Integrated_Bin_Name_data_wBG].SetLineWidth(3 if("png" in fmt) else 1)
                        All_Histos[Integrated_Bin_Name_data_wBG].SetLineColor(ROOT.kBlue)
                    else:
                        All_Histos[Integrated_Bin_Name_data_wBG].Add(All_Histos[temp_hists["data_wBG"].GetName()])
                    temp_hists["data_woBG"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_data_woBG, Q2_Y_Bin, z_pT_Bin, Use_All_Name=False)
                    if(temp_hists["data_woBG"] is None):
                        continue
                    All_Histos[temp_hists["data_woBG"].GetName()] = temp_hists["data_woBG"]
                    All_Histos[temp_hists["data_woBG"].GetName()].SetLineWidth(3 if("png" in fmt) else 1)
                    All_Histos[temp_hists["data_woBG"].GetName()].SetLineColor(ROOT.kCyan)
                    Min_Content = min([Min_Content, All_Histos[temp_hists["data_woBG"].GetName()].GetBinContent(All_Histos[temp_hists["data_woBG"].GetName()].GetMinimumBin())])
                    Max_Content = max([Max_Content, All_Histos[temp_hists["data_woBG"].GetName()].GetBinContent(All_Histos[temp_hists["data_woBG"].GetName()].GetMaximumBin())])
                    if(Integrated_Bin_Name_data_woBG is None):
                        temp_hists["data_woBG_All"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_data_woBG, Q2_Y_Bin, z_pT_Bin, Use_All_Name=True)
                        Integrated_Bin_Name_data_woBG = temp_hists["data_woBG_All"].GetName()
                        All_Histos[Integrated_Bin_Name_data_woBG] = temp_hists["data_woBG_All"]
                        All_Histos[Integrated_Bin_Name_data_woBG].SetLineWidth(3 if("png" in fmt) else 1)
                        All_Histos[Integrated_Bin_Name_data_woBG].SetLineColor(ROOT.kCyan)
                    else:
                        All_Histos[Integrated_Bin_Name_data_woBG].Add(All_Histos[temp_hists["data_woBG"].GetName()])
                if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                    temp_hists["clasdis"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_clasdis, Q2_Y_Bin, z_pT_Bin, Use_All_Name=False)
                    if(temp_hists["clasdis"] is None):
                        continue
                    All_Histos[temp_hists["clasdis"].GetName()] = temp_hists["clasdis"]
                    All_Histos[temp_hists["clasdis"].GetName()].SetLineWidth(3 if("png" in fmt) else 1)
                    All_Histos[temp_hists["clasdis"].GetName()].SetLineColor(ROOT.kRed)
                    Min_Content = min([Min_Content, All_Histos[temp_hists["clasdis"].GetName()].GetBinContent(All_Histos[temp_hists["clasdis"].GetName()].GetMinimumBin())])
                    Max_Content = max([Max_Content, All_Histos[temp_hists["clasdis"].GetName()].GetBinContent(All_Histos[temp_hists["clasdis"].GetName()].GetMaximumBin())])
                    if(Integrated_Bin_Name_clasdis is None):
                        temp_hists["clasdis_All"] = Slice_4D_Histo_Bins_For_phi_h_Plots(args, hist_clasdis, Q2_Y_Bin, z_pT_Bin, Use_All_Name=True)
                        Integrated_Bin_Name_clasdis = temp_hists["clasdis_All"].GetName()
                        All_Histos[Integrated_Bin_Name_clasdis] = temp_hists["clasdis_All"]
                        All_Histos[Integrated_Bin_Name_clasdis].SetLineWidth(3 if("png" in fmt) else 1)
                        All_Histos[Integrated_Bin_Name_clasdis].SetLineColor(ROOT.kRed)
                    else:
                        All_Histos[Integrated_Bin_Name_clasdis].Add(All_Histos[temp_hists["clasdis"].GetName()])

                if(Draw_Type == "Normalized"):
                    All_Histos[temp_hists["harut"].GetName()].DrawNormalized("hist E0")
                    if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                        All_Histos[temp_hists["data_wBG"].GetName()].DrawNormalized("hist E0 same")
                        All_Histos[temp_hists["data_woBG"].GetName()].DrawNormalized("hist E0 same")
                    if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                        All_Histos[temp_hists["clasdis"].GetName()].DrawNormalized("hist E0 same")
                else:
                    All_Histos[temp_hists["harut"].GetName()].GetYaxis().SetRangeUser(min([1.2*Min_Content, 0]), max([1.2*Max_Content, 0]))
                    All_Histos[temp_hists["harut"].GetName()].Draw("hist E0")
                    if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                        All_Histos[temp_hists["data_wBG"].GetName()].Draw("hist E0 same")
                        All_Histos[temp_hists["data_woBG"].GetName()].Draw("hist E0 same")
                    if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                        All_Histos[temp_hists["clasdis"].GetName()].Draw("hist E0 same")
                ROOT.gPad.Update()
            except:
                print(f"{color.Error}Error in Drawing the phi_h Plots for Bin ({Q2_Y_Bin}-{z_pT_Bin}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
        All_z_pT_Canvas[Save_Name].cd()
        All_z_pT_Canvas[Save_Name].Modified()
        All_z_pT_Canvas[Save_Name].Update()
    ####  Filling Canvas (Right) End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
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
        Min_Content_Integrated, Max_Content_Integrated = 0, 0
        for legend_name, histnames in [["Harut's Exclusive MC" if(Draw_Type not in ["data_scale"]) else "#splitline{Harut's Exclusive MC}{Scaled to Data}", Integrated_Bin_Name_harut], ["#splitline{Experimental Data}{Before #rho^{0} Subtraction}", Integrated_Bin_Name_data_wBG], ["#splitline{Experimental Data}{After #rho^{0} Subtraction}", Integrated_Bin_Name_data_woBG], ["clasdis (pure SIDIS) MC" if(Draw_Type not in ["data_scale"]) else "#splitline{clasdis (pure SIDIS) MC}{Scaled to Data}", Integrated_Bin_Name_clasdis]]:
            if((histnames is None) or (histnames not in All_Histos)):
                continue
            leg.AddEntry(All_Histos[histnames], f"#scale[0.75]{{{legend_name}}}", "l")
            Min_Content_Integrated = min([Min_Content_Integrated, All_Histos[histnames].GetBinContent(All_Histos[histnames].GetMinimumBin())])
            Max_Content_Integrated = max([Max_Content_Integrated, All_Histos[histnames].GetBinContent(All_Histos[histnames].GetMaximumBin())])
        leg.Draw("same")
        All_z_pT_Canvas[Save_Name].legend_store["legend"] = leg
        pad_leg.Modified()
        pad_leg.Update()
        ###    Legends     ###
        ################################################################
        ### Integral Plots ###
        Integrated_Pad = All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(1)
        # Integrated_Pad.SetFillColor(ROOT.kGray)
        Integrated_Pad.cd()
        # ROOT.gStyle.SetOptStat(0)
        if(Draw_Type == "Normalized"):
            All_Histos[Integrated_Bin_Name_harut].DrawNormalized("hist E0")
            if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                All_Histos[Integrated_Bin_Name_data_wBG].DrawNormalized("hist E0 same")
                All_Histos[Integrated_Bin_Name_data_woBG].DrawNormalized("hist E0 same")
            if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                All_Histos[Integrated_Bin_Name_clasdis].DrawNormalized("hist E0 same")
        else:
            All_Histos[Integrated_Bin_Name_harut].GetYaxis().SetRangeUser(min([1.2*Min_Content_Integrated, 0]), max([1.2*Max_Content_Integrated, 0]))
            All_Histos[Integrated_Bin_Name_harut].Draw("hist E0")
            if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                All_Histos[Integrated_Bin_Name_data_wBG].Draw("hist E0 same")
                All_Histos[Integrated_Bin_Name_data_woBG].Draw("hist E0 same")
            if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                All_Histos[Integrated_Bin_Name_clasdis].Draw("hist E0 same")
        ROOT.gPad.Update()
        ### Integral Plots ###
        ################################################################
        if(Comparison_Type in ["In_Data", "All_Data_Types"]):
            Contamination_Report_Pad = All_z_pT_Canvas[Save_Name].cd(1).cd(1).cd(2)
            # Contamination_Report_Pad.SetFillColor(ROOT.kGray)
            Contamination_Report_Pad.cd()
            Ratios_of_Contaminations[Save_Name]["Report_Box"] = ROOT.TPaveText(0.05, 0.05, 0.95, 0.95, "NDC")
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetFillColor(0)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetBorderSize(1)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetFillStyle(1001)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetTextAlign(22)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetTextFont(62)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetTextSize(0.025)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].SetMargin(0.02)
            Ratios_of_Contaminations[Save_Name]["Report_Box"].AddText(f'Average #rho^{{0}} Contamination Shown:  {Ratios_of_Contaminations[Save_Name]["Sum_of_Percents"]/Ratios_of_Contaminations[Save_Name]["Number_of_Calcs"]:.3f}% of Data')
            Ratios_of_Contaminations[Save_Name]["Report_Box"].AddText(f'Maximum #rho^{{0}} Contamination Shown:  {Ratios_of_Contaminations[Save_Name]["Max_Contamination"]:.3f}% of Data in Q^{{2}}-y-z-P_{{T}} {Ratios_of_Contaminations[Save_Name]["Max_Bin_Num"].replace("_", " ")}')
            Ratios_of_Contaminations[Save_Name]["Report_Box"].AddText(f'Minimum #rho^{{0}} Contamination Shown:  {Ratios_of_Contaminations[Save_Name]["Min_Contamination"]:.3f}% of Data in Q^{{2}}-y-z-P_{{T}} {Ratios_of_Contaminations[Save_Name]["Min_Bin_Num"].replace("_", " ")}')
            Ratios_of_Contaminations[Save_Name]["Report_Box"].Draw("same")
        ################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Saving Canvases  #########################################################################################################################################################################################################################################################################################################################################################################################
        out_name = f"{Save_Name}_{args.name}{fmt}" if(getattr(args, "name", "") not in [None, ""]) else f"{Save_Name}{fmt}"
        if(not getattr(args, "no_save", False)):
            All_z_pT_Canvas[Save_Name].SaveAs(out_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{out_name}{color.END}")
        else:
            print(f"{color.Error}Would be Saving: {color.BCYAN}{out_name}{color.END}")
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    if(Comparison_Type in ["In_Data", "All_Data_Types"]):
        print("\n\n")
        print(f"{color.BBLUE}Average #rho^{0} Contamination Shown:{color.END}")
        print(f'{color.BOLD}\t{Ratios_of_Contaminations["Global"]["Sum_of_Percents"]/Ratios_of_Contaminations["Global"]["Number_of_Calcs"]:.3f}% of Data{color.END}')
        print(f"{color.BBLUE}Maximum #rho^{0} Contamination Shown:{color.END}")
        print(f'{color.BOLD}\t{Ratios_of_Contaminations["Global"]["Max_Contamination"]:.3f}% of Data in Q^{{2}}-y-z-P_{{T}} {Ratios_of_Contaminations["Global"]["Max_Bin_Num"].replace("_", " ")}{color.END}')
        print(f"{color.BBLUE}Minimum #rho^{0} Contamination Shown:{color.END}")
        print(f'{color.BOLD}\t{Ratios_of_Contaminations["Global"]["Min_Contamination"]:.3f}% of Data in Q^{{2}}-y-z-P_{{T}} {Ratios_of_Contaminations["Global"]["Min_Bin_Num"].replace("_", " ")}{color.END}')
        print("\n\n")
    return All_z_pT_Canvas


def Other_1D_Kinematic_Comparison_Images(args, Hist_List_In, Vars_Input="(Q2)_(xB)", Comparison_Type="In_Data", stage_name="Full_SIDIS", Draw_Type="data_scale"):
    Vars_Input_Smeared = Vars_Input.replace(")", "_smeared)")
    fmt = f'.{getattr(args, "file_format", "pdf")}'.lower()
    hist_key_data_wBG  = f"(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(exclusive_rho_individual)_{Vars_Input}_{stage_name}"
    hist_key_data_woBG = f"{hist_key_data_wBG}_(Removed_Background)"
    hist_key_harut     = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(exclusive_rho_individual)_{Vars_Input_Smeared}_({'lundvpk' if(not args.old_lund) else 'lundrho'})_{stage_name}_(Scaled)"
    hist_key_clasdis   = hist_key_harut.replace(f"_({'lundvpk' if(not args.old_lund) else 'lundrho'})", "")
    hist_data_wBG  = Hist_List_In.get(hist_key_data_wBG,  None)
    hist_data_woBG = Hist_List_In.get(hist_key_data_woBG, None)
    hist_harut     = Hist_List_In.get(hist_key_harut,     None)
    hist_clasdis   = Hist_List_In.get(hist_key_clasdis,   None)
    if(None in [hist_harut]):
        raise ValueError(f"{color.Error}Error: Missing '{hist_key_harut}'{color.END}")
    if((None in [hist_data_wBG, hist_data_woBG]) and (Comparison_Type in ["In_Data", "All_Data_Types"])):
        raise ValueError(f"{color.Error}Error: Missing either '{hist_key_data_wBG}' or '{hist_key_data_woBG}'{color.END}")
    if((None in [hist_clasdis])                  and (Comparison_Type in ["In_MCs",  "All_Data_Types"])):
        raise ValueError(f"{color.Error}Error: Missing '{hist_key_clasdis}'{color.END}")
    Hists_Projected, Canvas_List = {}, {}
    def Projection_Function(Hist_In, Min_Content, Max_Content, Project_Var, Project_axis, color_select):
        Hist_In_Clone = Hist_In.Clone(f"{Hist_In.GetName()}_Clone")
        if(Project_axis == 0):
            Hist_Projected = Hist_In_Clone.ProjectionX(f"Projected_{Hist_In.GetName()}_for_{Project_Var}")
        else:
            Hist_Projected = Hist_In_Clone.ProjectionY(f"Projected_{Hist_In.GetName()}_for_{Project_Var}")
        Default_Title = f"#splitline{{#splitline{{Exclusive Background Subtraction Comparisons for}}{{{variable_Title_name_new(Project_Var)} Distributions}}}}{{{args.title}}}"
        if(stage_name not in ["Full_SIDIS"]):
            Default_Title = f"#splitline{{{Default_Title}}}{{Applied Cuts for '{stage_name}' Events}}"
        Hist_Projected.SetTitle(Default_Title)
        Hist_Projected.GetXaxis().SetTitle(str(Hist_Projected.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
        Hist_Projected.GetYaxis().SetTitle("Counts" if(Draw_Type != "Normalized") else "Normalized")
        Hist_Projected.SetLineWidth(3 if("png" in fmt) else 1)
        Hist_Projected.SetLineColor(color_select)
        Min_Content = min([Min_Content, Hist_Projected.GetBinContent(Hist_Projected.GetMinimumBin())])
        Max_Content = max([Max_Content, Hist_Projected.GetBinContent(Hist_Projected.GetMaximumBin())])
        return Hist_Projected, Min_Content, Max_Content
    for num, var in enumerate(Vars_Input.split(")_(")):
        var = str(var.replace(")", "")).replace("(", "")
        Hists_Projected[var] = {}
        if(("(Q2)_(xB)" in Vars_Input) and ("Q2" in var)):
            continue # Handeled by the other 2D histo
        Save_Name = f"Kinematic_Comparisons_of_{var}_{Comparison_Type}_for_Background_Subtraction"
        if(stage_name not in ["Full_SIDIS"]):
            Save_Name = f"{Save_Name}_with_{stage_name}_Cuts"
        Canvas_List[Save_Name] = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=1200, Size_Y=600, cd_Space=0.01)
        ROOT.gStyle.SetOptStat(0)
        Canvas_List[f"{Save_Name}_pad1"] = Canvas_List[Save_Name].cd(1)
        Canvas_List[f"{Save_Name}_pad1"].SetPad(0.0, 0.0, 0.8, 1.0)
        Canvas_List[f"{Save_Name}_pad2"] = Canvas_List[Save_Name].cd(2)
        Canvas_List[f"{Save_Name}_pad2"].SetPad(0.8, 0.0, 1.0, 1.0)
        Canvas_List[Save_Name].cd(2)
        Min_Content, Max_Content = 0, 0
        Canvas_List[f"legend_{var}"] = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
        Canvas_List[f"legend_{var}"].SetNColumns(1)
        Canvas_List[f"legend_{var}"].SetBorderSize(0)
        Canvas_List[f"legend_{var}"].SetFillStyle(0)
        Canvas_List[f"legend_{var}"].SetTextFont(42)
        Canvas_List[f"legend_{var}"].SetTextSize(0.10)
        Hists_Projected[var][f"{Save_Name}_Harut"],         Min_Content, Max_Content = Projection_Function(hist_harut,     Min_Content, Max_Content, var, num, ROOT.kGreen)
        Canvas_List[f"legend_{var}"].AddEntry(Hists_Projected[var][f"{Save_Name}_Harut"], "#scale[0.75]{Harut's Exclusive MC}" if(Draw_Type not in ["data_scale"]) else "#scale[0.75]{#splitline{Harut's Exclusive MC}{Scaled to Data}}", "l")
        if(Comparison_Type in ["In_Data", "All_Data_Types"]):
            Hists_Projected[var][f"{Save_Name}_data_wBG"],  Min_Content, Max_Content = Projection_Function(hist_data_wBG,  Min_Content, Max_Content, var, num, ROOT.kBlue)
            Hists_Projected[var][f"{Save_Name}_data_woBG"], Min_Content, Max_Content = Projection_Function(hist_data_woBG, Min_Content, Max_Content, var, num, ROOT.kCyan)
            Canvas_List[f"legend_{var}"].AddEntry(Hists_Projected[var][f"{Save_Name}_data_wBG"],  "#scale[0.75]{#splitline{Experimental Data}{Before #rho^{0} Subtraction}}", "l")
            Canvas_List[f"legend_{var}"].AddEntry(Hists_Projected[var][f"{Save_Name}_data_woBG"], "#scale[0.75]{#splitline{Experimental Data}{After #rho^{0} Subtraction}}",  "l")
        if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
            Hists_Projected[var][f"{Save_Name}_clasdis"],   Min_Content, Max_Content = Projection_Function(hist_clasdis,   Min_Content, Max_Content, var, num, ROOT.kRed)
            Canvas_List[f"legend_{var}"].AddEntry(Hists_Projected[var][f"{Save_Name}_clasdis"],   "#scale[0.75]{clasdis (pure SIDIS) MC}" if(Draw_Type not in ["data_scale"]) else "#scale[0.75]{#splitline{clasdis (pure SIDIS) MC}{Scaled to Data}}", "l")
        Canvas_List[f"legend_{var}"].Draw("same")
        Canvas_List[Save_Name].Modified()
        Canvas_List[Save_Name].Update()
        Canvas_List[Save_Name].cd(1)
        if(Draw_Type == "Normalized"):
            Hists_Projected[var][f"{Save_Name}_Harut"].DrawNormalized("hist E0")
            if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                Hists_Projected[var][f"{Save_Name}_data_wBG"].DrawNormalized("hist E0 same")
                Hists_Projected[var][f"{Save_Name}_data_woBG"].DrawNormalized("hist E0 same")
            if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                Hists_Projected[var][f"{Save_Name}_clasdis"].DrawNormalized("hist E0 same")
        else:
            Hists_Projected[var][f"{Save_Name}_Harut"].GetYaxis().SetRangeUser(min([1.2*Min_Content, 0]), max([1.2*Max_Content, 0]))
            Hists_Projected[var][f"{Save_Name}_Harut"].Draw("hist E0")
            if(Comparison_Type in ["In_Data", "All_Data_Types"]):
                Hists_Projected[var][f"{Save_Name}_data_wBG"].Draw("hist E0 same")
                Hists_Projected[var][f"{Save_Name}_data_woBG"].Draw("hist E0 same")
            if(Comparison_Type in ["In_MCs",  "All_Data_Types"]):
                Hists_Projected[var][f"{Save_Name}_clasdis"].Draw("hist E0 same")
        ROOT.gPad.Update()
        out_name = f"{Save_Name}_{args.name}{fmt}" if(getattr(args, "name", "") not in [None, ""]) else f"{Save_Name}{fmt}"
        if(not getattr(args, "no_save", False)):
            Canvas_List[Save_Name].SaveAs(out_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{out_name}{color.END}")
        else:
            print(f"{color.Error}Would be Saving: {color.BCYAN}{out_name}{color.END}")
    # return Hists_Projected
    return Canvas_List

def Create_Diagnostic_Weight_Impact_Plots(args):
    print(f"\n{color.BOLD}Creating simplified diagnostic weight impact plots...{color.END}")

    # Hard-coded global scaling factors (no per-bin scaling)
    scale_harut   = 5.184287
    scale_clasdis = 0.193244

    hist_key___data  =  "(Normal_2D)_(rdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(W_pippim)_(exclusive_rho_individual)"
    hist_key__harut  = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)_({'lundvpk' if(not args.old_lund) else 'lundrho'})"
    hist_key_clasdis =  "(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)"

    if(args.Use_2D_Kinematic_Binning):
        hist_key___data  =  hist_key___data.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")
        hist_key__harut  =  hist_key__harut.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")
        hist_key_clasdis = hist_key_clasdis.replace("Q2_y_z_pT_Bin_All", "Q2_Y_Bin")

    if(args.use_same_file):
        args.file2 = args.file1

    if(args.verbose):
        print(f"Loading ROOT file: {args.file2}")
        print(f"Loading histogram key 'hist_key___data'  = {hist_key___data}")
        print(f"Loading histogram key 'hist_key__harut'  = {hist_key__harut}")
        print(f"Loading histogram key 'hist_key_clasdis' = {hist_key_clasdis}")

    file2 = ROOT.TFile.Open(args.file2)
    if((not file2) or (file2.IsZombie())):
        print(f"ERROR: Failed to open ROOT file: {args.file2}")
        sys.exit(1)
        
    h3__data = file2.Get(hist_key___data)
    check_histo_for_errors(h3__data, hist_key___data,  args.file2)
    h3_harut = file2.Get(hist_key__harut)
    check_histo_for_errors(h3_harut, hist_key__harut,  args.file2)
    h3___mdf = file2.Get(hist_key_clasdis)
    check_histo_for_errors(h3___mdf, hist_key_clasdis, args.file2)
    
    print(f"{color.BGREEN}Successfully loaded all TH3D histograms and validated compatibility.{color.END}")
    
    proj_data  = project_z_bins_global(h3__data, "proj_data_diag",    list(range(128, 256, 1)), args)
    proj_harut = project_z_bins_global(h3_harut, "proj_harut_diag",   list(range(128, 256, 1)), args)
    proj_clas  = project_z_bins_global(h3___mdf, "proj_clasdis_diag", list(range(128, 256, 2)), args) # Must use even bins only to avoid the exclusive rho events from generator-level information
    
    # 1D projections for the signal region
    data_kin = proj_data.ProjectionY("data_kin_diag")
    haru_raw = proj_harut.ProjectionY("harut_kin_raw")
    clas_raw = proj_clas.ProjectionY("clasdis_kin_raw")
    # Apply the fixed scaling factors
    haru_scaled = haru_raw.Clone("haru_scaled")
    clas_scaled = clas_raw.Clone("clas_scaled")
    haru_scaled.Scale(scale_harut)
    clas_scaled.Scale(scale_clasdis)
    
    c = ROOT.TCanvas("c_diagnostic", "", 1400, 900)
    c.Divide(2, 1, 0.01, 0.01)
    ROOT.gStyle.SetOptStat(0)
    # Left pad: overlaid 1D yields (Data unscaled + scaled MCs) + legend
    c.cd(1)
    ROOT.gPad.SetPad(0.01, 0.01, 0.49, 0.99)
    data_kin.SetLineColor(ROOT.kBlue)
    data_kin.SetLineWidth(2)
    # data_kin.SetTitle(f"#splitline{{Diagnostic Weight Impact (SIDIS Cuts)}}{{{args.title}}}")
    data_kin.SetTitle(f"#splitline{{#splitline{{Comparison between the Event Counts}}{{Per 4D Kinematic SIDIS Bin}}}}{{{args.title}}}")
    # data_kin.GetXaxis().SetTitle("z_{1} + z_{2}")
    # data_kin.GetYaxis().SetTitle("Yield")
    # data_kin.GetXaxis().SetRangeUser(1, 900)
    ROOT.gPad.SetLogy(1)
    clas_scaled.SetTitle(data_kin.GetTitle())
    clas_scaled.GetXaxis().SetTitle(data_kin.GetXaxis().GetTitle())
    clas_scaled.SetLineColor(ROOT.kRed)
    clas_scaled.SetLineWidth(2)
    clas_scaled.Draw("hist")
    haru_scaled.SetLineColor(ROOT.kGreen+1)
    haru_scaled.SetLineWidth(2)
    haru_scaled.Draw("hist same")
    data_kin.Draw("hist same")
    

    leg = ROOT.TLegend(0.45, 0.75, 0.90, 0.90)
    leg.SetFillStyle(0); leg.SetBorderSize(0)
    leg.AddEntry(data_kin,     "#splitline{Experimental Data}{(No Subtraction)}",                  "l")
    leg.AddEntry(haru_scaled, f"#splitline{{Harut MC}}{{Normalized with: {scale_harut:.6f}}}",     "l")
    leg.AddEntry(clas_scaled, f"#splitline{{clasdis MC}}{{Normalized with: {scale_clasdis:.6f}}}", "l")
    leg.Draw("same")

    # Right column - 3 rows for the three ratios
    c.cd(2)
    right_pad = c.GetPad(2)
    right_pad.Divide(1, 3, 0.0001, 0.0001)

    # Ratio 1: Harut / Data (top row)
    right_pad.cd(1)
    r1 = haru_scaled.Clone("r_harut_over_data")
    r1.Divide(data_kin)
    r1.SetLineColor(ROOT.kGreen+3)
    r1.SetLineWidth(2)
    r1.SetTitle("Ratio of #frac{Harut's MC}{Data}")
    r1.GetYaxis().SetTitle("Ratio")
    r1.GetXaxis().SetTitle(str(r1.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    sum1 = 0.0
    count1 = 0
    max1 = r1.GetMaximum()
    # min1 = r1.GetMinimum()
    min1 = max1
    minBin1, maxBin1 = 0, 0
    for i in range(1, r1.GetNbinsX() + 1):
        val = r1.GetBinContent(i)
        sum1 += val
        count1 += 1
        if(val != 0):
            min1 = min([min1, val])
        if(min1 == val):
            minBin1 = i
        if(max1 == val):
            maxBin1 = i
    avg1 = sum1 / count1 if(count1 > 0) else 0.0
    r1.GetYaxis().SetRangeUser(min([1.2*min1, 0]), max([1.2*max1, 0]))
    r1.Draw("hist")
    box1 = ROOT.TPaveText(0.6, 0.7, 0.90, 0.90, "NDC")
    box1.SetFillColor(0); box1.SetBorderSize(1)
    box1.AddText(f"Avg ratio: {avg1*100:.2f}%")
    box1.AddText(f"Non-Zero Min: {min1*100:.2f}% #scale[0.85]{{(Bin Num {minBin1+1})}}")
    box1.AddText(f"Max: {max1*100:.2f}% #scale[0.85]{{(Bin Num {maxBin1+1})}}")
    box1.Draw("same")


    # Ratio 3: clasdis / Data (middle row)
    right_pad.cd(2)
    r3 = clas_scaled.Clone("r_clas_over_data")
    r3.Divide(data_kin)
    r3.SetLineColor(ROOT.kViolet)
    r3.SetLineWidth(2)
    r3.SetTitle("Ratio of #frac{clasdis MC}{Data}")
    r3.GetYaxis().SetTitle("Ratio")
    r3.GetXaxis().SetTitle(str(r3.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    sum3 = 0.0
    count3 = 0
    max3 = r3.GetMaximum()
    # min3 = r3.GetMinimum()
    min3 = max3
    minBin3, maxBin3 = 0, 0
    for i in range(1, r3.GetNbinsX() + 1):
        val = r3.GetBinContent(i)
        sum3 += val
        count3 += 1
        if(val != 0):
            min3 = min([min3, val])
        if(min3 == val):
            minBin3 = i
        if(max3 == val):
            maxBin3 = i
    avg3 = sum3 / count3 if(count3 > 0) else 0.0
    r3.GetYaxis().SetRangeUser(min([1.2*min3, 0]), max([1.5*max3, 0]))
    r3.Draw("hist")
    box3 = ROOT.TPaveText(0.6, 0.7, 0.90, 0.90, "NDC")
    box3.SetFillColor(0); box3.SetBorderSize(1)
    box3.AddText(f"Avg ratio: {avg3*100:.2f}%")
    box3.AddText(f"Non-Zero Min: {min3*100:.2f}% #scale[0.85]{{(Bin Num {minBin3+1})}}")
    box3.AddText(f"Max: {max3*100:.2f}% #scale[0.85]{{(Bin Num {maxBin3+1})}}")
    box3.Draw("same")

    # Ratio 2: Harut / clasdis (bottom row)
    right_pad.cd(3)
    r2 = haru_scaled.Clone("r_harut_over_clas")
    r2.Divide(clas_scaled)
    r2.SetLineColor(ROOT.kMagenta+2)
    r2.SetLineWidth(2)
    r2.SetTitle("Ratio of #frac{Harut's MC}{clasdis MC}")
    r2.GetYaxis().SetTitle("Ratio")
    r2.GetXaxis().SetTitle(str(r2.GetXaxis().GetTitle()).replace(" (Smeared)", ""))
    sum2 = 0.0
    count2 = 0
    max2 = r2.GetMaximum()
    # min2 = r2.GetMinimum()
    min2 = max2
    minBin2, maxBin2 = 0, 0
    for i in range(1, r2.GetNbinsX() + 1):
        val = r2.GetBinContent(i)
        sum2 += val
        count2 += 1
        if(val != 0):
            min2 = min([min2, val])
        if(min2 == val):
            minBin2 = i
        if(max2 == val):
            maxBin2 = i
    avg2 = sum2 / count2 if(count2 > 0) else 0.0
    r2.GetYaxis().SetRangeUser(min([1.2*min2, 0]), max([1.2*max2, 0]))
    r2.Draw("hist")
    box2 = ROOT.TPaveText(0.6, 0.7, 0.90, 0.90, "NDC")
    box2.SetFillColor(0); box2.SetBorderSize(1)
    box2.AddText(f"Avg ratio: {avg2*100:.2f}%")
    box2.AddText(f"Non-Zero Min: {min2*100:.2f}% #scale[0.85]{{(Bin Num {minBin2+1})}}")
    box2.AddText(f"Max: {max2*100:.2f}% #scale[0.85]{{(Bin Num {maxBin2+1})}}")
    box2.Draw("same")


    fmt = args.file_format.lower()
    suffix = f"_{args.name}" if(args.name) else ""
    save_file_name = f"Diagnostic_Weight_Impact_Combined{suffix}.{fmt}"
    if(args.no_save):
        print(f"\n{color.Error}Would have saved: {color.END}{color.BPINK}{save_file_name}{color.END}")
    else:
        c.SaveAs(save_file_name)
        print(f"{color.BBLUE}Saved combined diagnostic plot: {color.BCYAN}Diagnostic_Weight_Impact_Combined{suffix}.{fmt}{color.END}")

    file2.Close()
    print(f"\n{color.BOLD}Diagnostic weight impact plots completed.{color.END}\n")

if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    if(args.Kinematic_Bin_Select not in ["All", "Full"]):
        args.Kinematic_Bin_Select = int(args.Kinematic_Bin_Select)
    if(getattr(args, "run_all_base_diagnostic_images", False)):
        diagnostic_hist_list = make_diagnostic_cut_images(args)
        canvas_list = phi_h_1D_Compare_in_z_pT_Images_Together(diagnostic_hist_list, args, Comparison_Type="In_Data",        stage_name="Full_SIDIS", Draw_Type="data_scale")
        # canvas_list = phi_h_1D_Compare_in_z_pT_Images_Together(diagnostic_hist_list, args, Comparison_Type="In_MCs",         stage_name="Full_SIDIS", Draw_Type="Normalized")
        # canvas_list = phi_h_1D_Compare_in_z_pT_Images_Together(diagnostic_hist_list, args, Comparison_Type="All_Data_Types", stage_name="Full_SIDIS", Draw_Type="data_scale")
        # canvas_list = phi_h_1D_Compare_in_z_pT_Images_Together(diagnostic_hist_list, args, Comparison_Type="All_Data_Types", stage_name="Full_SIDIS", Draw_Type="Normalized")
        # for     stage_names in ["Full_SIDIS", "Exclusive"]:
        for     stage_names in ["Full_SIDIS"]:
            for var_choices in ["(Q2)_(y)", "(Q2)_(xB)", "(z)_(pT)", "(W_pippim)_(MM_pippim)"]:
                if((var_choices in ["(W_pippim)_(MM_pippim)"]) and (stage_names not in ["Exclusive"])):
                    continue
                canvas_list = Other_1D_Kinematic_Comparison_Images(args, diagnostic_hist_list, Vars_Input=var_choices, Comparison_Type="In_Data", stage_name=stage_names, Draw_Type="data_scale")
    elif(getattr(args, "run_diagnostic_weight_images", False)):
        Create_Diagnostic_Weight_Impact_Plots(args)
    elif("W" in str(args.vars)):
        silence_root_import()
        main_Get_rho_Normalization_values_Wpions(args)
    else:
        main_Get_rho_Normalization_values(args)
    args.timer.stop()

