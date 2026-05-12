#!/usr/bin/env python3

import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, root_color, color_bg, variable_Title_name, RuntimeTimer
sys.path.remove(script_dir)
del script_dir
import argparse

Name_of_Script = "Get_rho_Normalization_values.py"
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"{Name_of_Script}: Gets Normalization Parameters for Harut's rho0 files based on input histograms from pre-made ROOT files.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-f1', '--file1',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_V2Sbatch_Default_rho_Final_Analysis_Iterations_I0_05_11_2026.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_VSbatch_Exclusive_rho_Final_Analysis_Iterations_I0_05_11_2026.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Remove_rho_Final_Analysis_Iterations_I0_All.root',
                        help='Path to the ROOT file which contains the required clasdis/data histograms (without rho0).\n')
    parser.add_argument('-f2', '--file2',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Default_rho_Final_Analysis_Iterations_I0_All.root',
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
                        default='Q2xB',
                        choices=['Q2xB', 'q2xb', 'z', 'z1z2'],
                        help="Controls for which variables to use (either 'Q2 vs xB' or 'z1+z2').\n")
    parser.add_argument('-cz', '--clasdis_z1z2',
                        action='store_true',
                        help='Runs the z1+z2 plots with clasdis instead of data.\n')

    return parser.parse_args()

def main_Get_rho_Normalization_values(args):
    print(f"\n{color.BBLUE}Starting execution of {Name_of_Script}...{color.END}\n")

    hist_key1 = "(Normal_2D)_(gdf)_(no_cut_Remove_rho)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)" if(str(args.vars).lower() in ["q2xb"]) else "(Normal_2D)_(rdf)_(cut_Complete_SIDIS)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)"
    hist_key2 = "(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(Q2)_(xB)_(lundvpk)"  if(str(args.vars).lower() in ["q2xb"]) else "(Normal_2D)_(mdf)_(cut_Complete_SIDIS)_(SMEAR=smear)_(Q2_y_z_pT_Bin_All)_(z1_plus_z2_smeared)_(exclusive_rho_smeared)_(lundvpk)"
    if(args.clasdis_z1z2):
        hist_key1 = "(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)"
        hist_key2 = "(Normal_2D)_(gdf)_(no_cut)_(SMEAR='')_(Q2_y_z_pT_Bin_All)_(z1_plus_z2)_(exclusive_rho)_(lundvpk)"
        args.vars = "z1z2"

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
    if(not h3d1):
        print(f"ERROR: Could not load histogram '{hist_key1}' from file 1")
        sys.exit(1)
    if(not h3d1.InheritsFrom("TH3")):
        print(f"ERROR: Loaded object '{hist_key1}' is not TH3-compatible (got {h3d1.ClassName()})")
        sys.exit(1)

    h3d2 = file2.Get(hist_key2)
    if(not h3d2):
        print(f"{color.Error}ERROR: Could not load histogram '{hist_key2}' from file 2{color.END}")
        sys.exit(1)
    if(not h3d2.InheritsFrom("TH3")):
        print(f"{color.Error}ERROR: Loaded object '{hist_key2}' is not TH3-compatible (got {h3d2.ClassName()}){color.END}")
        sys.exit(1)
    print(f"{color.BGREEN}Successfully loaded both TH3D histograms and validated compatibility.{color.END}")
    print("Creating 2D projections using only the x- and y-axes...")
    proj_hist1 = h3d1.Project3D("yx" if(str(args.vars).lower() not in ["q2xb"]) else "xy")
    proj_hist1.SetName("proj_xy_1")
    proj_hist2 = h3d2.Project3D("yx" if(str(args.vars).lower() not in ["q2xb"]) else "xy")
    proj_hist2.SetName("proj_xy_2")
    print("Projections created successfully.")
    if(str(args.vars).lower() not in ["q2xb"]):
        args.x_min =   0 if(args.x_min == 0.08) else args.x_min
        args.x_max = 1.8 if(args.x_max == 0.68) else args.x_max
        args.y_min =  -2 if(args.y_min == 0.90) else args.y_min
        args.y_max =   2 if(args.y_max == 8.50) else args.y_max
    if(not args.clasdis_z1z2):
        print(f"{color.BOLD}Applying axis ranges: x [{args.x_min}, {args.x_max}], y [{args.y_min}, {args.y_max}] to both projected histograms.{color.END}")
    proj_hist1.GetXaxis().SetRangeUser(args.x_min, args.x_max)
    proj_hist1.GetYaxis().SetRangeUser(args.y_min if(not args.clasdis_z1z2) else -2, args.y_max if(not args.clasdis_z1z2) else 0)
    proj_hist2.GetXaxis().SetRangeUser(args.x_min, args.x_max)
    proj_hist2.GetYaxis().SetRangeUser(args.y_min if(not args.clasdis_z1z2) else  0, args.y_max if(not args.clasdis_z1z2) else 2)
    # bin-based integration that respects the applied ranges
    x_low1 = proj_hist1.GetXaxis().FindBin(args.x_min)
    x_high1 = proj_hist1.GetXaxis().FindBin(args.x_max)
    y_low1 = proj_hist1.GetYaxis().FindBin(args.y_min  if(not args.clasdis_z1z2) else -2)
    y_high1 = proj_hist1.GetYaxis().FindBin(args.y_max if(not args.clasdis_z1z2) else  0)
    weighted_count1 = proj_hist1.Integral(x_low1, x_high1, y_low1, y_high1)
    x_low2 = proj_hist2.GetXaxis().FindBin(args.x_min)
    x_high2 = proj_hist2.GetXaxis().FindBin(args.x_max)
    y_low2 = proj_hist2.GetYaxis().FindBin(args.y_min  if(not args.clasdis_z1z2) else 0)
    y_high2 = proj_hist2.GetYaxis().FindBin(args.y_max if(not args.clasdis_z1z2) else 2)
    weighted_count2 = proj_hist2.Integral(x_low2, x_high2, y_low2, y_high2)

    print("")
    print(f"{color.BOLD}Weighted event count for first histogram (inside selected ranges):  {color.UNDERLINE}{weighted_count1}{color.END}")
    print(f"{color.BOLD}Weighted event count for second histogram (inside selected ranges): {color.UNDERLINE}{weighted_count2}{color.END}")
    print("")

    title_common = f"#splitline{{Plot of Q^{{2}} vs x_{{B}} For #rho^{{0}} Normalization}}{{#splitline{{{args.y_min:.2f} < Q^{{2}} < {args.y_max:.2f}}}{{{args.x_min:.2f} < x_{{B}} < {args.x_max:.2f}}}}}" if(str(args.vars).lower() in ["q2xb"]) else "Plot of z_{1}+z_{2} For #rho^{0} Normalization"
    title1 = f"#splitline{{#splitline{{#scale[1.2]{{From {'clasdis MC' if(str(args.vars).lower() in ['q2xb']) else 'Experimental Data'}}}}}{{{title_common}}}}}{{#scale[0.8]{{Weighted events: {weighted_count1:.2f}}}}}"
    title2 = f"#splitline{{#splitline{{#scale[1.2]{{From Harut's Files}}}}{{{title_common}}}}}{{#scale[0.8]{{Weighted events: {weighted_count2:.2f}}}}}"
    proj_hist1.SetTitle(f"#splitline{{{title1}}}{{{args.title}}}" if(args.title) else title1)
    proj_hist2.SetTitle(f"#splitline{{{title2}}}{{{args.title}}}" if(args.title) else title2)

    if(not args.no_save):
        print(f"\n{color.BOLD}Setting up drawing style and saving histograms...{color.END}\n")
        ROOT.gROOT.SetBatch(True)
        ROOT.gStyle.SetOptStat(111111)
        suffix = f"_{args.name}" if(args.name) else ""
        fmt = args.file_format.lower()
        out_file1 = f"Plot_of_{args.vars}_for_rho0_Norm_Main_File{suffix}.{fmt}"
        out_file2 = f"Plot_of_{args.vars}_for_rho0_Norm_Harut{suffix}.{fmt}"

        canvas1 = ROOT.TCanvas("c1", "", 800, 600)
        proj_hist1.Draw("colz")
        canvas1.SaveAs(out_file1)
        print(f"{color.BOLD}Saved first histogram canvas to: {color.BPINK}{out_file1}{color.END}")

        canvas2 = ROOT.TCanvas("c2", "", 800, 600)
        proj_hist2.Draw("colz")
        canvas2.SaveAs(out_file2)
        print(f"{color.BOLD}Saved second histogram canvas to: {color.BPINK}{out_file2}{color.END}")
    else:
        print(f"\n{color.Error}No-save mode enabled: skipping drawing and file saving.{color.END}\n")

    file1.Close()
    file2.Close()
    print(f"\n{color.BBLUE}{Name_of_Script}{color.END_B} completed successfully.{color.END}\n")

if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    main_Get_rho_Normalization_values(args)
    args.timer.stop()

