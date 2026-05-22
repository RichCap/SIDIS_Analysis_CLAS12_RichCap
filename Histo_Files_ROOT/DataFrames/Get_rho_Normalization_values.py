#!/usr/bin/env python3

import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, root_color, color_bg, variable_Title_name, RuntimeTimer, Draw_Canvas
sys.path.remove(script_dir)
del script_dir
import argparse

Name_of_Script = "Get_rho_Normalization_values.py"
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description=f"{Name_of_Script}: Gets Normalization Parameters for Harut's rho0 files based on input histograms from pre-made ROOT files.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-V', '--verbose',
                        action='store_true',
                        help="Print verbosely.\n")
    parser.add_argument('-f1', '--file1',                        
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Dynamic_W_pim_cut_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_New_Dynamic_rho_Final_Analysis_Iterations_I0_All.root',
                        # default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho_Normalizer_Default_rho_Final_Analysis_Iterations_I0_All.root',
                        help='Path to the ROOT file which contains the required clasdis/data histograms (without rho0).\n')
    parser.add_argument('-f2', '--file2',
                        default='/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_Dynamic_W_pim_cut_rho_Final_Analysis_Iterations_I0_All.root',
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
                        default='Q2xB',
                        choices=['Q2xB', 'q2xb', 'z', 'z1z2'],
                        help="Controls for which variables to use (either 'Q2 vs xB' or 'z1+z2').\n")
    # parser.add_argument('-cz', '--clasdis_z1z2',
    #                     action='store_true',
    #                     help='Runs the z1+z2 plots with clasdis instead of data.\n')
    parser.add_argument('-ol', '--old_lund',
                        action='store_true',
                        help="Use Harut's old files instead of the newer ones.\n")
    parser.add_argument('-dm', '--draw_mode',
                        default='auto',
                        choices=['auto', '2D', '1D', '1D_dif'],
                        help="Drawing mode. 'auto' chooses based on --vars (Q2xB=2D, z-modes=1D by default).\n\t'1D_dif' draws 1D histograms, but to different canvases (like the '2D' mode).\n")
    parser.add_argument('-ztc', '--z_tot_cut',
                        default=0.6,
                        type=float,
                        help='Normalization cut for z_tot.\n')
    return parser.parse_args()

def check_histo_for_errors(hist, name, file_name):
    if(not hist):
        print(f"ERROR: Could not load histogram '{name}' from '{file_name}'")
        sys.exit(1)
    if(not hist.InheritsFrom("TH3")):
        print(f"ERROR: Loaded object '{name}' is not TH3-compatible (got {hist.ClassName()})")
        sys.exit(1)

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

    hist_key1 = hist_key1.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
    hist_key2 = hist_key2.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
    hist_key3 = hist_key3.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
    hist_key4 = hist_key4.replace("Q2_y_z_pT_Bin_All",  "exclusive_rho_individual")
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
    check_histo_for_errors(h3d1, hist_key1, args.file1)
    h3d2 = file2.Get(hist_key2)
    check_histo_for_errors(h3d2, hist_key2, args.file2)
    h3d4 = file1.Get(hist_key4)
    check_histo_for_errors(h3d4, hist_key4, args.file1)

    print(f"{color.BGREEN}Successfully loaded all four TH3D histograms and validated compatibility.{color.END}")
    if(args.verbose):
        print("Creating 2D projections using specific bins on Z-axis (exclusive_rho_individual)...")

    # Helper to safely sum specific Z-bins while preserving "yx" or "xy" projection order
    def project_z_bins(h3d, name, z_values_list):
        if not h3d:
            return None
        proj_option = "yx" if(str(args.vars).lower() not in ["q2xb"]) else "xy"
        zaxis = h3d.GetZaxis()
        proj = None
        for zval in z_values_list:
            bin_num = zaxis.FindBin(zval)
            zaxis.SetRange(bin_num, bin_num)
            tmp = h3d.Project3D(proj_option)
            if proj is None:
                proj = tmp.Clone(name)
                proj.Reset()
            else:
                proj.Add(tmp)
            tmp.Delete()
        zaxis.SetRange(0, 0)  # reset range
        return proj

    # Tight projections used for normalization
    exclusive_bins = [15, 23, 31, 47, 55, 63]
    exclusive_bins = [15, 31, 47, 63]
    excl_SIDIS_bkg = [14, 30, 46, 62] # These are events that look like they could be exclusive based on the selection cuts, but are in fact background (SIDIS) events to those exclusive distributions
    sidis_bins     = [32, 34, 48, 50, 33, 35, 49, 51] # The odd numbers in this list are only reliable in the experimental data files since the `exclusive_rho` index doesn't carry the generator-level knowledge about exclusivity (for data, the odd bins just indicate that no other particles were detected beyond what is allowable under by exclusive events, so their inclusion here assumes that there are undetected particles that could make the event fall outside of the exclusive region—supported by these exclusive bins being choosen based on the event already failing the exclusive-rho0 cuts from the invariant/missing masses)
                                                      # The odd bins are removed from the mdf SIDIS histograms by only using the events in the bins selected from the `y_bin_0` below (i.e., the bin which sets `exclusive_rho` to 0 regardless of these z-axis cuts)
    # print(f"exclusive_bins = {exclusive_bins}")
    # print(f"sidis_bins     = {sidis_bins}")
    all_bins = exclusive_bins + sidis_bins
    # print(f"all_bins       = {all_bins}")
    # print(f"exclusive_bins = {exclusive_bins}")
    # print(f"sidis_bins     = {sidis_bins}")
    # all_bins = list(range(32, 64))
    # for ii in exclusive_bins:
    #     if(ii not in all_bins):
    #         all_bins.append(ii)
    # all_bins = exclusive_bins
    proj_data_excl  = project_z_bins(h3d1, "proj_data_excl",  exclusive_bins)
    proj_harut_excl = project_z_bins(h3d2, "proj_harut_excl", exclusive_bins)
    proj_data_SIDIS = project_z_bins(h3d4, "proj_data_SIDIS", sidis_bins)

    h3d_mdf = file1.Get(hist_key3)
    proj_mdf_SIDIS = project_z_bins(h3d_mdf, "proj_mdf_SIDIS", sidis_bins)
    proj_mdf_excl  = project_z_bins(h3d_mdf, "proj_mdf_excl",  exclusive_bins)

    # === Loose projections for plotting that MATCH the normalization cuts ===
    # Full data for plotting = exclusive + SIDIS parts (same bins used in normalization)
    proj_data_full_for_plot = project_z_bins(h3d1, "proj_data_full_for_plot", all_bins)
    proj_harutfull_for_plot = project_z_bins(h3d2, "proj_harutfull_for_plot", all_bins)

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

        # print(f"args.z_tot_cut = {args.z_tot_cut}")
        # print(f"args.x_min     = {args.x_min}")
        min_x_plots   = proj_data_excl.GetXaxis().FindBin(args.x_min)
        signal_x_low  = proj_data_excl.GetXaxis().FindBin(args.z_tot_cut)
        # signal_x_high = proj_data_excl.GetXaxis().FindBin(1.2)
        signal_x_high = proj_data_excl.GetXaxis().GetNbins()
        # print(f"min_x_plots   = {min_x_plots}")
        # print(f"signal_x_low  = {signal_x_low}")
        # print(f"signal_x_high = {signal_x_high}")
        y_bin_0 = proj_data_excl.GetYaxis().FindBin(0.0)
        y_bin_1 = proj_data_excl.GetYaxis().FindBin(1.0)

        Y_mdf_clean  = proj_mdf_SIDIS.Integral(min_x_plots,  signal_x_low, y_bin_0, y_bin_0)
        Y_data_clean = proj_data_SIDIS.Integral(min_x_plots, signal_x_low, y_bin_0, y_bin_0)
        N_sdf        = Y_data_clean / Y_mdf_clean if(Y_mdf_clean > 0) else 0.0
        
        data_excl_subt = proj_data_excl.Clone("data_excl_subt")
        # for     x_val in range(0, proj_data_excl.GetXaxis().GetNbins()):
        #     for y_val in range(0, proj_data_excl.GetYaxis().GetNbins()):
        #         if(proj_data_excl.GetBinContent(x_val, y_val) > (N_sdf*proj_mdf_SIDIS.GetBinContent(x_val, y_val))):
        #             data_excl_subt.SetBinContent(x_val, y_val, proj_data_excl.GetBinContent(x_val, y_val) - (N_sdf*proj_mdf_SIDIS.GetBinContent(x_val, y_val)))
        #         else:
        #             data_excl_subt.SetBinContent(x_val, y_val, 0)
        
        # N_data_vis  = proj_data_excl.Integral(signal_x_low,  signal_x_high, y_bin_1, y_bin_1)
        N_data_vis  = data_excl_subt.Integral(signal_x_low,  signal_x_high, y_bin_1, y_bin_1)
        N_harut_vis = proj_harut_excl.Integral(signal_x_low, signal_x_high, y_bin_1, y_bin_1)
        N_data_side = proj_data_SIDIS.Integral(signal_x_low, signal_x_high, 0, -1)

        # mdf contributions around the exclusive region
        N_mdf_side  = proj_mdf_SIDIS.Integral(signal_x_low, signal_x_high, y_bin_0, y_bin_0)
        N_mdf_peak  = proj_mdf_SIDIS.Integral(signal_x_low, signal_x_high, y_bin_1, y_bin_1)

        alpha = N_data_side / N_mdf_side  if(N_mdf_side  > 0) else 0.0
        N_edf = N_data_vis  / N_harut_vis if(N_harut_vis > 0) else 0.0

        final_factor = N_edf / N_sdf              if(N_sdf       > 0) else 0.0

        # Print everything
        print(f"{ color.BOLD }N_data_vis (exclusive signal region)              : {N_data_vis:>12.0f}{color.END}")
        print(f"{ color.BOLD }N_harut_vis (Harut signal)                        : {N_harut_vis:>12.0f}{color.END}")
        print(f"{ color.BOLD }N_data_side (SIDIS+exclusive above z_tot cut)     : {N_data_side:>12.0f}{color.END}")
        # print(f"{ color.BOLD }N_mdf_side (clasdis SIDIS in exclusive region)    : {N_mdf_side:>12.0f}{color.END}")
        print(f"{ color.END  }N_mdf_peak (clasdis in exclusive signal region)   : {N_mdf_peak:>12.0f}{color.END}")
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

            title = f"#splitline{{Plot of z_{{1}}+z_{{2}} For #rho^{{0}} Normalization}}{{#scale[0.8]{{Exclusive Region Cutoff was z_{{1}}+z_{{2}} > {args.z_tot_cut}}}}}"
            proj_data__1d.SetTitle(f"#splitline{{{title}}}{{{args.title}}}")
            # proj_data__1d.GetXaxis().SetRangeUser(args.x_min, args.x_max)
            # proj_harut_1d.GetXaxis().SetRangeUser(args.x_min, args.x_max)

            # Data Exclusive portion (using the same tight cut as normalization)
            # proj_data_full_for_plot.GetXaxis().SetRange(x_low1, x_high1)
            # hist_data_excl = proj_data_full_for_plot.ProjectionX("hist_data_excl", y_bin_1, y_bin_1)
            # proj_data_excl.GetXaxis().SetRange(signal_x_low,  signal_x_high)
            # proj_data_excl.GetXaxis().SetRange(0, 0)
            # hist_data_excl = proj_data_excl.ProjectionX("hist_data_excl", y_bin_1, y_bin_1)
            hist_data_excl = data_excl_subt.ProjectionX("hist_data_excl", y_bin_1, y_bin_1)
            # proj_data_full_for_plot.GetXaxis().SetRange(0, 0)
            hist_data_excl.SetLineColor(ROOT.kOrange)
            hist_data_excl.SetLineWidth(2)
            hist_data_excl.SetLineStyle(2)

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
            hist_clasdis_excl.SetLineColor(ROOT.kOrange+3)
            hist_clasdis_excl.SetLineWidth(1)
            hist_clasdis_excl.SetLineStyle(2)

            hist_combined = hist_clasdis_norm.Clone("hist_combined")
            hist_combined.Add(proj_harut_1d_norm)
            hist_combined.SetLineColor(ROOT.kMagenta)
            hist_combined.SetLineWidth(2)
            hist_combined.SetLineStyle(1)

            for hist_loop in [proj_data__1d, hist_clasdis_norm, proj_harut_1d, proj_harut_1d_norm, hist_combined, hist_data_excl, hist_data_sidis, hist_clasdis_excl]:
                hist_loop.GetXaxis().SetRangeUser(max([args.x_min, 0.1]), args.x_max)

            out_file = f"Plot_of_{args.vars}_for_rho0_Norm_Combined_1D{suffix}.{fmt}"
            canvas = ROOT.TCanvas("c_combined", "", 900, 700)
            canvas.Divide(2, 1, 0.0001, 0.0001)
            canvas.SetGrid()
            ROOT.gStyle.SetAxisColor(16, 'xy')
            ROOT.gStyle.SetOptStat(0)
            Draw_Canvas(canvas, 1, left_add=0.125, right_add=0.025, up_add=0.1, down_add=0.075)
            # canvas.cd(1)
            # ROOT.gPad.SetLogy(1)
            # proj_data__1d.Draw("hist")
            hist_clasdis_norm.SetTitle(proj_data__1d.GetTitle())
            hist_clasdis_norm.Draw("hist same")
            # hist_combined.Draw("hist same")
            hist_data_sidis.Draw("hist same")
            proj_harut_1d_norm.Draw("hist same")
            hist_data_excl.Draw("hist same")
            hist_clasdis_excl.Draw("hist same")
            legend_cd_1 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
            legend_cd_1.SetFillStyle(0)
            legend_cd_1.SetBorderSize(0)
            legend_cd_1.AddEntry(proj_data__1d,     "#scale[1.5]{Experimental Data (Full)}",                  "l")
            legend_cd_1.AddEntry(hist_data_sidis,   "#scale[1.5]{Experimental Data (SIDIS)}",                 "l")
            legend_cd_1.AddEntry(hist_clasdis_norm, "#scale[1.5]{clasdis SIDIS (Normalized)}",                "l")
            legend_cd_1.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized)}",                 "l")
            legend_cd_1.Draw("same")
            # canvas.cd(2)
            Draw_Canvas(canvas, 2, left_add=0.095, right_add=0.025, up_add=0.1, down_add=0.075)
            Shared_Title = proj_data__1d.GetTitle()
            if(args.title not in ["", " "]):
                Shared_Title = Shared_Title.replace(args.title, f"#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}")
            else:
                Shared_Title = f"#splitline{{{Shared_Title}}}{{#scale[0.75]{{#color[{ROOT.kGreen+1}]{{Exclusive #rho^{{0}} Focused Distributions}}}}}}"
            hist_clasdis_excl.SetTitle(Shared_Title)
            hist_clasdis_excl.GetXaxis().SetTitle(hist_clasdis_excl.GetXaxis().GetTitle().replace(" (Smeared)", ""))
            hist_clasdis_excl.Draw("hist")
            proj_harut_1d_norm.Draw("hist same")
            hist_data_excl.Draw("hist same")
            # proj_harut_1d.Draw("hist same")
            # hist_data_subt = data_excl_subt.ProjectionX("hist_data_subt", y_bin_1, y_bin_1)
            # hist_data_subt.GetXaxis().SetRangeUser(max([args.x_min, 0.01]), args.x_max)
            # hist_data_subt.Draw("hist same")
            legend_cd_2 = ROOT.TLegend(0.575, 0.10, 0.975, 0.45)
            legend_cd_2.SetFillStyle(0)
            legend_cd_2.SetBorderSize(0)
            legend_cd_2.AddEntry(proj_harut_1d_norm,"#scale[1.5]{Harut Exclusive MC (Normalized)}",           "l")
            legend_cd_2.AddEntry(hist_data_excl,    "#scale[1.5]{Experimental Data (Exclusive #rho^{0}})",    "l")
            legend_cd_2.AddEntry(hist_clasdis_excl, "#scale[1.5]{clasdis Exclusive #rho^{0} (Normalized)}",   "l")
            # legend_cd_2.AddEntry(proj_harut_1d,     "#scale[1.5]{Harut Exclusive MC (Raw)}",                          "l")
            # legend_cd_2.AddEntry(hist_clasdis_norm, "#scale[1.5]{clasdis SIDIS (Normalized to Data)}",                "l")
            # legend_cd_2.AddEntry(hist_combined,     "#scale[1.5]{Combined MCs (Normalized to Data)}",                 "l")
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
    main_Get_rho_Normalization_values(args)
    # args.timer.stop()

