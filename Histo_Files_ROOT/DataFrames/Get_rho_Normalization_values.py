#!/usr/bin/env python3

import ROOT
import cppyy
import sys
ROOT.gROOT.SetBatch(True)
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, root_color, color_bg, variable_Title_name, RuntimeTimer, Draw_Canvas, silence_root_import
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
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V5_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V3_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Dynamic_W_pim_cut_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_New_Dynamic_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho_Normalizer_Default_rho_Final_Analysis_Iterations_I0_All.root',
                        help='Path to the ROOT file which contains the required clasdis/data histograms (without rho0).\n')
    parser.add_argument('-f2', '--file2',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_V5_Final_Analysis_Iterations_I0_All.root',
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
                        help=f"Uses the 'Q2_Y_Bin' binning instead of the 4D kinematic bins in the 'Wpions' fit mode.\n\t{color.RED}As of 6/6/2026: Have not generalized it yet to other modes.{color.END}\n")
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
    return parser.parse_args()

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

def Create_Diagnostic_Weight_Impact_Plots(args, h3d1, h3d2, h3d4, h3d_mdf, Full_List_of_Factors, project_z_bins):
    if(getattr(args, "Kinematic_Bin_Select", "Full") not in ["Full", "All"]):
        print(f"{color.Error}Warning: Diagnostic Weight Impact plots only run for Kinematic_Bin_Select='Full' or 'All'. Skipping.{color.END}")
        return
    print(f"\n{color.BOLD}Creating diagnostic weight impact plots (Full kinematic bins)...{color.END}")
    non_all = [k for k in Full_List_of_Factors if(k != "All")]
    if(non_all and getattr(args, "Kinematic_Bin_Select", "Full") == "Full"):
        avg_sdf = sum(Full_List_of_Factors[k]["N_sdf"] for k in non_all)/len(non_all)
        avg_edf = sum(Full_List_of_Factors[k]["N_edf"] for k in non_all)/len(non_all)
        print(f"{color.BOLD}Average alpha_SIDIS (N_sdf): {avg_sdf:.6f}{color.END}")
        print(f"{color.BOLD}Average N_rho (N_edf)     : {avg_edf:.6f}{color.END}")
    yaxis = h3d_mdf.GetYaxis()
    n_y = yaxis.GetNbins()
    data_z = [b for b in range(64, n_y+1)]
    clas_z = [b for b in range(64, n_y+1) if(b%2 == 0)]
    haru_z = [b for b in range(64, n_y+1) if(b%2 == 1)]
    proj_data_d = project_z_bins(h3d1, "proj_data_diag", data_z)
    proj_clas_d = project_z_bins(h3d_mdf, "proj_clasdis_diag", clas_z)
    proj_haru_d = project_z_bins(h3d2, "proj_harut_diag", haru_z)
    if(None in [proj_data_d, proj_clas_d, proj_haru_d]):
        print(f"{color.Error}Failed diagnostic projections{color.END}")
        return
    data_kin = proj_data_d.ProjectionY("data_kin_diag")
    clas_raw = proj_clas_d.ProjectionY("clasdis_kin_raw")
    haru_raw = proj_haru_d.ProjectionY("harut_kin_raw")
    clas_to_data = clas_raw.Clone("clas_to_data")
    haru_to_data = haru_raw.Clone("haru_to_data")
    haru_to_clas = haru_raw.Clone("haru_to_clas")
    use_global = getattr(args, "Kinematic_Bin_Select", "Full") == "All"
    global_f = Full_List_of_Factors.get("All", None)
    for bk in Full_List_of_Factors:
        if(bk in ["All"]): continue
        ibin = int(bk) + 1
        if(use_global and global_f):
            sdf = global_f["N_sdf"]
            edf = global_f["N_edf"]
            final_f = global_f["final_factor"]
        else:
            sdf = Full_List_of_Factors[bk]["N_sdf"]
            edf = Full_List_of_Factors[bk]["N_edf"]
            final_f = Full_List_of_Factors[bk]["final_factor"]
        clas_to_data.SetBinContent(ibin, clas_raw.GetBinContent(ibin) * sdf)
        haru_to_data.SetBinContent(ibin, haru_raw.GetBinContent(ibin) * edf)
        haru_to_clas.SetBinContent(ibin, haru_raw.GetBinContent(ibin) * final_f)
    data_kin.SetLineColor(ROOT.kRed); data_kin.SetLineWidth(2)
    clas_to_data.SetLineColor(ROOT.kBlue); clas_to_data.SetLineWidth(2)
    haru_to_data.SetLineColor(ROOT.kGreen+2); haru_to_data.SetLineWidth(3)
    haru_to_clas.SetLineColor(ROOT.kMagenta); haru_to_clas.SetLineWidth(3)
    for h in [data_kin, clas_to_data, haru_to_data, haru_to_clas]:
        h.GetXaxis().SetTitle("Flattened 4D Kinematic Bin Index")
        h.GetYaxis().SetTitle("Yield")
    fmt = args.file_format.lower()
    suffix = f"_{args.name}" if(args.name) else ""
    c1 = ROOT.TCanvas("c_diag_data", "", 900, 600)
    ROOT.gStyle.SetOptStat(0)
    data_kin.Draw("hist")
    clas_to_data.Draw("hist same")
    haru_to_data.Draw("hist same")
    leg1 = ROOT.TLegend(0.6, 0.7, 0.95, 0.9)
    leg1.SetFillStyle(0); leg1.SetBorderSize(0)
    leg1.AddEntry(data_kin, "Experimental Data (unscaled)", "l")
    leg1.AddEntry(clas_to_data, "clasdis (scaled by N_sdf)", "l")
    leg1.AddEntry(haru_to_data, "Harut (scaled by N_edf)", "l")
    leg1.Draw("same")
    c1.SaveAs(f"Diagnostic_Data_Level_Weight_Impact{suffix}.{fmt}")
    print(f"{color.BOLD}Saved Data-level diagnostic: Diagnostic_Data_Level_Weight_Impact{suffix}.{fmt}{color.END}")
    c2 = ROOT.TCanvas("c_diag_mc", "", 900, 600)
    ROOT.gStyle.SetOptStat(0)
    clas_to_data.Draw("hist")
    haru_to_clas.Draw("hist same")
    leg2 = ROOT.TLegend(0.6, 0.7, 0.95, 0.9)
    leg2.SetFillStyle(0); leg2.SetBorderSize(0)
    leg2.AddEntry(clas_to_data, "clasdis (to data level)", "l")
    leg2.AddEntry(haru_to_clas, "Harut (to clasdis level)", "l")
    leg2.Draw("same")
    c2.SaveAs(f"Diagnostic_MC_Level_Weight_Impact{suffix}.{fmt}")
    print(f"{color.BOLD}Saved MC-level diagnostic: Diagnostic_MC_Level_Weight_Impact{suffix}.{fmt}{color.END}")
    def make_ratio(num, den, name, ttl):
        r = num.Clone(name)
        r.SetTitle(ttl)
        r.SetLineColor(ROOT.kBlack); r.SetLineWidth(2)
        avg_r = 0.0
        nvalid = 0
        for i in range(1, r.GetNbinsX()+1):
            dval = den.GetBinContent(i)
            rval = (num.GetBinContent(i)/dval*100) if(dval > 0) else 0.0
            r.SetBinContent(i, rval)
            if(dval > 0):
                avg_r += rval
                nvalid += 1
        avg_r = avg_r/nvalid if nvalid else 0.0
        c_r = ROOT.TCanvas(f"c_{name}", "", 900, 600)
        ROOT.gStyle.SetOptStat(0)
        r.Draw("hist")
        box = ROOT.TPaveText(0.6, 0.8, 0.95, 0.9, "NDC")
        box.SetFillColor(0); box.SetBorderSize(1)
        box.AddText(f"Avg ratio: {avg_r:.2f}%")
        box.Draw("same")
        c_r.SaveAs(f"Diagnostic_Ratio_{name}{suffix}.{fmt}")
        print(f"{color.BOLD}Saved ratio: Diagnostic_Ratio_{name}{suffix}.{fmt}{color.END}")
        return r
    r1 = make_ratio(haru_to_data, data_kin, "HarutToData_over_Data", "Harut(to-data)/Data x100")
    r2 = make_ratio(clas_to_data, data_kin, "ClasdisToData_over_Data", "clasdis(to-data)/Data x100")
    r3 = make_ratio(clas_to_data, haru_to_data, "ClasdisToData_over_HarutToData", "clasdis(to-data)/Harut(to-data) x100")
    r4 = make_ratio(clas_to_data, haru_to_clas, "ClasdisToData_over_HarutToClasdis", "clasdis(to-data)/Harut(to-clasdis) x100")
    if(getattr(args, "extra_root_save", False)):
        root_name = f"Diagnostic_Weight_Impact_Histos_{args.name if args.name else 'UnNamed'}.root"
        rf = ROOT.TFile.Open(root_name, "RECREATE")
        if(rf and not rf.IsZombie()):
            data_kin.Write(); clas_to_data.Write(); haru_to_data.Write(); haru_to_clas.Write()
            r1.Write(); r2.Write(); r3.Write(); r4.Write()
            rf.Close()
            print(f"{color.BGREEN}Saved diagnostic histograms to {root_name}{color.END}")
    print(f"{color.BOLD}Diagnostic weight impact plots completed.{color.END}\n")

def project_z_bins_global(h3d, name, z_values_list, args=None, function_or_hist_integration="hist"):
    if(not h3d):
        return None
    if(getattr(args, "legacy", False) and (function_or_hist_integration in ["hist"])):
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
    hist_key__harut  =  "(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)"
    hist_key_clasdis = f"(Normal_2D)_(mdf)_(cut_Complete_SIDIS_MM_None)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(W_pippim_smeared)_(exclusive_rho_individual_smeared)_({'lundvpk' if(not args.old_lund) else 'lundrho'})"

    if(args.Use_2D_Kinematic_Binning or True): # As of 6/6/2026, these histograms always use the Q2-y bins only
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
    
    args.Exclusive_bins = [87, 95, 119, 127, 215, 223, 247, 255]
    args.SIDIS_BKG_bins = [92, 94, 124, 126, 220, 222, 252, 254]

    # Data
    proj__data_excl = project_z_bins_global(h3__data, "proj__data_excl", args.Exclusive_bins, args, function_or_hist_integration="func")
    # Harut's MC
    proj_harut_excl = project_z_bins_global(h3_harut, "proj_harut_excl", args.Exclusive_bins, args, function_or_hist_integration="func")
    # clasdis MC (SIDIS BKG)
    proj_mdf__exbkg = project_z_bins_global(h3___mdf, "proj_mdf__exbkg", args.SIDIS_BKG_bins, args, function_or_hist_integration="func")

    return args, proj__data_excl, proj_harut_excl, proj_mdf__exbkg, file1

def Create_Wpions_Fit_Images(args, mass_data, mass_harut, fy_data, fy_harut, fy1_data, fy1_harut, N_data_rho, N_harut_rho, n_rho):
    fmt = args.file_format.lower()
    suffix = f"_{args.name}" if(args.name) else ""
    suffix = f"{suffix}_Bin_{getattr(args, 'Kinematic_Bin_Select', 'All')}"
    # Data fit plot
    c_data = ROOT.TCanvas("c_data_fit", "", 900, 600)
    ROOT.gStyle.SetOptStat(0)
    mass_data.Draw("hist")
    mass_data.SetLineColor(ROOT.kCyan)
    fy_data.SetLineColor(ROOT.kBlack)
    fy_data.Draw("same")
    fy1_data.SetLineColor(ROOT.kMagenta)
    fy1_data.Draw("same")
    # leg_d = ROOT.TLegend(0.55, 0.75, 0.95, 0.95)
    leg_d = ROOT.TLegend(0.575, 0.10, 0.9, 0.45)
    leg_d.SetFillStyle(0); leg_d.SetBorderSize(0)
    leg_d.AddEntry(mass_data, "Experimental Data", "l")
    leg_d.AddEntry(fy_data,   "Full Fit",          "l")
    leg_d.AddEntry(fy1_data,  "#rho^{0} Signal",   "l")
    leg_d.Draw("same")
    # box_d = ROOT.TPaveText(0.15, 0.8, 0.55, 0.9, "NDC")
    box_d = ROOT.TPaveText(0.575, 0.55, 0.9, 0.65, "NDC")
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
    mass_harut.Draw("hist")
    mass_harut.SetLineColor(ROOT.kGreen)
    fy_harut.SetLineColor(ROOT.kBlack)
    fy_harut.Draw("same")
    fy1_harut.SetLineColor(ROOT.kMagenta)
    fy1_harut.Draw("same")
    # leg_h = ROOT.TLegend(0.55, 0.75, 0.95, 0.95)
    leg_h = ROOT.TLegend(0.575, 0.10, 0.9, 0.45)
    leg_h.SetFillStyle(0); leg_h.SetBorderSize(0)
    leg_h.AddEntry(mass_harut, "Harut's Monte Carlo", "l")
    leg_h.AddEntry(fy_harut,   "Full Fit",            "l")
    leg_h.AddEntry(fy1_harut,  "#rho^{0} Signal",     "l")
    leg_h.Draw("same")
    box_h = ROOT.TPaveText(0.575, 0.55, 0.9, 0.65, "NDC")
    box_h.SetFillColor(0); box_h.SetBorderSize(1); box_h.SetFillStyle(1001)
    box_h.SetTextAlign(22); box_h.SetTextFont(62); box_h.SetTextSize(0.025)
    box_h.SetMargin(0.02)
    box_h.AddText("Number of Harut's MC")
    box_h.AddText("Exclusive #rho^{0} Events:")
    box_h.AddText(f"{N_harut_rho:.6f}")
    box_h.Draw("same")
    if(not args.no_save):
        c_harut.SaveAs(f"Wpions_Fit_Harut_MC{suffix}.{fmt}")
        print(f"{color.BOLD}Saved Wpions data fit: {color.BBLUE}Wpions_Fit_Harut_MC{suffix}.{fmt}{color.END}")
    else:
        print(f"{color.Error}Would have saved Wpions data fit: {color.END_B}Wpions_Fit_Harut_MC{suffix}.{fmt}{color.END}")
    # # Normalization summary
    # c_sum = ROOT.TCanvas("c_summary", "", 900, 600)
    # ROOT.gStyle.SetOptStat(0)
    # pave = ROOT.TPaveText(0.1, 0.1, 0.9, 0.9, "NDC")
    # pave.SetFillColor(0); pave.SetBorderSize(1)
    # pave.AddText("Wpions Fit-Based rho0 Normalization")
    # pave.AddText(f"N_data_rho (signal) = {N_data_rho:.2f}")
    # pave.AddText(f"N_harut_rho (signal) = {N_harut_rho:.2f}")
    # pave.AddText(f"n_rho = {n_rho:.6f}")
    # pave.Draw()
    # c_sum.SaveAs(f"Wpions_Fit_Normalization_Summary{suffix}.{fmt}")
    # print(f"{color.BOLD}Saved Wpions normalization summary: Wpions_Fit_Normalization_Summary{suffix}.{fmt}{color.END}")
    # if(getattr(args, "extra_root_save", False)):
    #     root_name = f"Wpions_Fit_Normalization_Histos_{args.name if args.name else 'UnNamed'}.root"
    #     rf = ROOT.TFile.Open(root_name, "RECREATE")
    #     if(rf and not rf.IsZombie()):
    #         mass_data.Write()
    #         mass_harut.Write()
    #         fy_data.Write()
    #         fy_harut.Write()
    #         rf.Close()
    #         print(f"{color.BGREEN}Saved Wpions fit histograms to {root_name}{color.END}")

def main_Get_rho_Normalization_values_Wpions(args):
    print(f"\n{color.BBLUE}Starting Wpions fit-based rho0 normalization...{color.END}")
    args, proj__data_excl, proj_harut_excl, proj_mdf__exbkg, file1 = histo_setup_for_Wpions(args)
    args.x_min =  0.2 if(args.x_min == 0.08) else args.x_min
    args.x_max =  2.0 if(args.x_max == 0.68) else args.x_max
    # 1D projections used as input distributions for fit (adapted from existing logic)
    if(getattr(args, "Kinematic_Bin_Select", "All") in ["All", "Full"]):
        histo__data_Wpions = proj__data_excl.ProjectionX("histo__data_Wpions_Bin_All")
        histo_harut_Wpions = proj_harut_excl.ProjectionX("histo_harut_Wpions_Bin_All")
        histo_mdfbg_Wpions = proj_mdf__exbkg.ProjectionX("histo_mdfbg_Wpions_Bin_All")
    else:
        histo_bin_num = proj__data_excl.GetYaxis().FindBin(int(getattr(args, "Kinematic_Bin_Select", 0)))
        histo__data_Wpions = proj__data_excl.ProjectionX(f"histo__data_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
        histo_harut_Wpions = proj_harut_excl.ProjectionX(f"histo_harut_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
        histo_mdfbg_Wpions = proj_mdf__exbkg.ProjectionX(f"histo_mdfbg_Wpions_Bin_{getattr(args, "Kinematic_Bin_Select", "All")}", int(histo_bin_num), int(histo_bin_num))
    minValue = max([0.3, args.x_min])
    maxValue = max([2.0, args.x_max])
    # C++ fit functions (adapted from Nick's notebook)
    ROOT.gInterpreter.Declare("""
    #include <cmath>
    #include "TMath.h"
    class FunctionSet {
    public:
        double breit_wigner_1(double *x, double *par) {
            double m = x[0];
            double amp = par[0];
            double mu = par[1];
            double gamma = par[2];
            return amp*TMath::BreitWigner(m, mu, gamma);
        }
        double breit_wigner_2(double *x, double *par) {
            double m = x[0];
            double amp = par[7];
            double mu = par[8];
            double gamma = par[9];
            return amp*TMath::BreitWigner(m, mu, gamma);
        }
        double breit_wigner_3(double *x, double *par) {
            double m = x[0];
            double amp = par[10];
            double mu = par[11];
            double gamma = par[12];
            return amp*TMath::BreitWigner(m, mu, gamma);
        }
        double background(double *xx, double *par) {
            double m = xx[0];
            double amp_bkg = par[3];
            double xi = par[4];
            double m0_bkg = par[5];
            double m1_bkg = par[6];
            double cc = m1_bkg-m0_bkg;
            double c2 = cc*cc;
            double x = cc - (m-m0_bkg);
            double ybg = 0;
            if(x>0 && x<cc) ybg = x/c2 * sqrt(1-x*x/c2) * exp(-0.5*xi*xi*(1-x*x/c2));
            return amp_bkg*ybg;
        }
        double total_function_f0(double *x, double *par) {
            double bw1 = breit_wigner_1(x, par);
            double bkg = background(x,par);
            double bw2 = breit_wigner_2(x, par);
            double bw3 = breit_wigner_3(x, par);
            return bw1 + bkg + bw2 + bw3;
        }
    };
    """)
    funcs = cppyy.gbl.FunctionSet()
    # withF0 = True
    # Fit data
    fy_data = ROOT.TF1("fy_data", funcs.total_function_f0, minValue, maxValue, 13)
    # fy_data.SetParameters(200, 0.7, 0.2, 100, 1, 0.3, 1, 20, 1.2, 0.18, 20, 0.98, 0.18)  # old line - remove
    # Use individual SetParameter calls (works for any number of parameters)
    pars_data = [2000, 0.77, 0.2, 500, 1, 0.3, 1, 200, 1.2, 0.18, 200, 0.98, 0.18]
    for i, p in enumerate(pars_data):
        fy_data.SetParameter(i, p)
        fy_data.SetParLimits(i, 0.5*p, 10*p)
    histo__data_Wpions.Fit(fy_data, "Q")
    fy1_data = ROOT.TF1("fy1_data", funcs.breit_wigner_1, minValue, maxValue, 3)
    fy1_data.SetParameters(fy_data.GetParameter(0), fy_data.GetParameter(1), fy_data.GetParameter(2))
    N_data_rho = fy1_data.Integral(minValue, maxValue)
    # Same for Harut
    fy_harut = ROOT.TF1("fy_harut", funcs.total_function_f0, minValue, maxValue, 13)
    pars_harut = [2000, 0.77, 0.2, 10, 1, 0.3, 1, 20, 1.2, 0.18, 20, 0.98, 0.18]
    for i, p in enumerate(pars_harut):
        fy_harut.SetParameter(i, p)
    histo_harut_Wpions.Fit(fy_harut, "Q")
    fy1_harut = ROOT.TF1("fy1_harut", funcs.breit_wigner_1, minValue, maxValue, 3)
    fy1_harut.SetParameters(fy_harut.GetParameter(0), fy_harut.GetParameter(1), fy_harut.GetParameter(2))
    N_harut_rho = fy1_harut.Integral(minValue, maxValue)
    n_rho = N_data_rho / N_harut_rho if(N_harut_rho > 0) else 0.0
    print("")
    print(f"{ color.BBLUE}Fit-based normalization (Wpions):{color.END}")
    print(f"{ color.BOLD }Kinematic Bin Used: {getattr(args, 'Kinematic_Bin_Select', 'All')}{color.END}")
    print(f"{ color.BOLD }N_data_rho (Experimental exclusive signal)        : {N_data_rho:>12.0f}{color.END}")
    print(f"{ color.BOLD }N_harut_rho (Harut's exclusive signal)            : {N_harut_rho:>12.0f}{color.END}")
    print(f"{color.BGREEN}n_rho (brings Harut's files to data)              : {n_rho:>12.6f}{color.END}\n")
    args.N_rho_fit = n_rho
    Create_Wpions_Fit_Images(args, histo__data_Wpions, histo_harut_Wpions, fy_data, fy_harut, fy1_data, fy1_harut, N_data_rho, N_harut_rho, n_rho)
    file1.Close()
    return n_rho


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

if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    if(args.Kinematic_Bin_Select not in ["All", "Full"]):
        args.Kinematic_Bin_Select = int(args.Kinematic_Bin_Select)
    if("W" in str(args.vars)):
        silence_root_import()
        main_Get_rho_Normalization_values_Wpions(args)
    else:
        main_Get_rho_Normalization_values(args)
    args.timer.stop()

