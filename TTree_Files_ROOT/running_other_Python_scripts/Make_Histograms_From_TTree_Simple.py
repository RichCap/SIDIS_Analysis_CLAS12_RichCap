#!/usr/bin/env python3

import argparse
import sys

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir

# Dictionary to define custom binning and range settings for specific variables
variable_settings = {
    "Q2":                        {"bins":  100, "range_min":    0.0, "range_max":  12.0},
    "xB":                        {"bins":  100, "range_min":    0.0, "range_max":   0.9},
    "y":                         {"bins":  100, "range_min":   0.05, "range_max":   0.9},
    "z":                         {"bins":  100, "range_min":    0.0, "range_max":   1.2},
    "pT":                        {"bins":  100, "range_min":    0.0, "range_max":   1.3},
    "W":                         {"bins":  100, "range_min":    1.0, "range_max":   5.0},
    "MM":                        {"bins":  100, "range_min":    0.0, "range_max":   5.0},
    "el":                        {"bins":  100, "range_min":    0.0, "range_max":   9.0},
    "pip":                       {"bins":  100, "range_min":    0.0, "range_max":   9.0},
    "elth":                      {"bins":  120, "range_min":    0.0, "range_max":  60.0},
    "pipth":                     {"bins":  160, "range_min":    0.0, "range_max":  80.0},
    "elPhi":                     {"bins":  120, "range_min":    0.0, "range_max": 360.0},
    "pipPhi":                    {"bins":  120, "range_min":    0.0, "range_max": 360.0},
    "phi_t":                     {"bins":   60, "range_min":    0.0, "range_max": 360.0},
    "Q2_Y_Bin":                  {"bins":   17, "range_min":    0.5, "range_max":  17.5},
    "z_pT_Bin_Y_bin":            {"bins":   39, "range_min":    0.5, "range_max":  39.5},
}

# Argument parser setup
parser = argparse.ArgumentParser(description=f"\n{color.BOLD}This script is for creating and drawing 1D/2D histograms from RDataFrames.{color.END}\n", epilog="""
    """, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-v",  "--variables", nargs='+', required=True,                                                help="Variables to plot as a list of strings, or for 2D plots, a list of lists of strings")
parser.add_argument("-df", "--rdf_list",  nargs='+', choices=['rdf', 'mdf', 'gdf'], default=['rdf', 'mdf', 'gdf'], help="List of RDataFrames to use (default: all)")
parser.add_argument("-t",  "--title",                type=str,                                                     help="Optional additional title text to add")
parser.add_argument('--Q2-y-Bin',         nargs='+', type=int,                                                     help="Cut on Q2_Y_Bin variable")
parser.add_argument('--z-pT-Bin',         nargs='+', type=int,                                                     help="Cut on z_pT_Bin_Y_bin variable (requires Q2_Y_Bin cut)")
parser.add_argument("-c",  "--cut",                  type=str,                                                     help="General cut string")
parser.add_argument("-sc", "--show-cut",             action='store_true',                                          help="Show general cut string in histogram title")
parser.add_argument("-gc", "--gdf-special-cut",      type=str,                                                     help="Special cut for the gdf RDataFrame only")
parser.add_argument("-lr", "--limit-range",          type=int,                                                     help="Apply limit to the number of events allowed in the RDataFrames (applied to all options)")

# Add arguments for bins and range
parser.add_argument(
    '-b', '--bins',
    type=int,
    default=50,
    help="".join(["Number of bins for the histograms (Default: 50).\n   Default by Variable:", "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['bins']).rjust(8)}" for ii in variable_settings)])
)
parser.add_argument(
    '--range_min',
    type=float,
    default=0.0,
    help="".join(["Minimum range for the histogram (Default: 0.0).\n   Default by Variable:",  "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['range_min']).rjust(8)}" for ii in variable_settings)])
)
parser.add_argument(
    '--range_max',
    type=float,
    default=14.0,
    help="".join(["Maximum range for the histogram (Default: 14.0).\n   Default by Variable:", "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['range_max']).rjust(8)}" for ii in variable_settings), "\n\n"])
)

args = parser.parse_args()

from Main_python_Working_with_TTree_Files import *

ROOT.gROOT.SetBatch(1)

# Mapping RDataFrame types to their display names
rdf_labels = {
    'rdf': f"#color[{ROOT.kBlue}]{{Experimental Data}}",
    'mdf': f"#color[{ROOT.kRed}]{{Reconstructed Monte Carlo}}",
    'gdf': f"#color[{ROOT.kGreen}]{{Generated Monte Carlo}}"
}

def create_histograms(variables, rdf_list, extra_title, Q2_Y_Bin_cut, z_pT_Bin_Y_bin_cut, general_cut, show_cut, gdf_special_cut, bins, range_min, range_max, limit_range):
    # Color mapping for RDataFrames
    color_map = {'rdf': ROOT.kBlue, 'mdf': ROOT.kRed, 'gdf': ROOT.kGreen}
    
    print(f"\n{color.BOLD}Starting to create new histogram(s){color.END}\n")
    
    # Apply cuts
    for Q2_cut in (Q2_Y_Bin_cut or [None]):
        for z_cut in (z_pT_Bin_Y_bin_cut or [None]):
            rdf_filtered_list = rdf_list.copy()
            title_suffix = ""
            save_suffix  = ""

            if(Q2_cut is not None):
                rdf_filtered_list = [df.Filter(f"Q2_Y_Bin == {Q2_cut}") for df in rdf_filtered_list]
                title_suffix += f"Q²-y Bin: {Q2_cut}"
                save_suffix  += f"_Q2_y_Bin_{Q2_cut}"

            if(z_cut is not None):
                rdf_filtered_list = [df.Filter(f"z_pT_Bin_Y_bin == {z_cut}") for df in rdf_filtered_list]
                title_suffix += f" #topbar z-P_{{T}} Bin: {z_cut}"
                save_suffix  += f"_z_pT_Bin_{z_cut}"

            # General cut applied to all RDataFrames except "gdf"
            for df_name in rdf_filtered_list:
                if(df_name != 'gdf' and general_cut):
                    rdf_filtered_list[df_name] = rdf_filtered_list[df_name].Filter(general_cut)
                if(df_name != "gdf"):
                    rdf_filtered_list[df_name] = rdf_filtered_list[df_name].Filter("Complete_SIDIS_Cuts && Valerii_DC_Fiducial_Cuts_ele_DC_6 && Valerii_DC_Fiducial_Cuts_ele_DC_18 && Valerii_DC_Fiducial_Cuts_ele_DC_36 && Valerii_DC_Fiducial_Cuts_pip_DC_6 && Valerii_DC_Fiducial_Cuts_pip_DC_18 && Valerii_DC_Fiducial_Cuts_pip_DC_36 && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")

            # Special cut only for "gdf"
            if('gdf' in rdf_filtered_list and gdf_special_cut):
                rdf_filtered_list['gdf'] = rdf_filtered_list['gdf'].Filter(gdf_special_cut)

            # Add cut information to the title
            if(show_cut and general_cut):
                title_suffix = f"#splitline{{{title_suffix}}}{{Cut: {general_cut}}}"

            if(show_cut and gdf_special_cut):
                title_suffix += f" #topbar Cut for MC GEN: {gdf_special_cut}"


            # Separate variables into 1D and 2D based on commas
            for var in variables:
                if(',' in var):  # 2D histogram (comma-separated)
                    var_pair = var.split(',')
                    if(len(var_pair) == 2):
                        y_var, x_var = var_pair
                        print(f"\n{color.BBLUE}Creating a 2D Histogram for {color.UNDERLINE}{x_var} vs {y_var}{color.END}\n")
                        x_bins = variable_settings.get(x_var, {}).get("bins",      bins)
                        x_min  = variable_settings.get(x_var, {}).get("range_min", range_min)
                        x_max  = variable_settings.get(x_var, {}).get("range_max", range_max)

                        y_bins = variable_settings.get(y_var, {}).get("bins",      bins)
                        y_min  = variable_settings.get(y_var, {}).get("range_min", range_min)
                        y_max  = variable_settings.get(y_var, {}).get("range_max", range_max)
                else:
                    print(f"\n{color.BBLUE}Creating a 1D Histogram for {color.UNDERLINE}{var}{color.END}\n")
                    var_bins = variable_settings.get(var, {}).get("bins",      bins)
                    var_min  = variable_settings.get(var, {}).get("range_min", range_min)
                    var_max  = variable_settings.get(var, {}).get("range_max", range_max)
                
                # Loop through each selected dataframe
                for df_name, df in rdf_filtered_list.items():
                    display_name = rdf_labels[df_name]  # Get display name for titles/legends

                    if(limit_range):
                        print(f"{color.Error}Applying an Event Limit ({limit_range} events) to {display_name}{color.END}")
                        df = df.Range(limit_range)

                    if(',' in var):  # 2D histogram (comma-separated)
                        if(len(var_pair) == 2):
                            canvas = ROOT.TCanvas(f"Canvas_{x_var}_{y_var}_{df_name}", f"Canvas for 2D histogram ({display_name})", 800, 600)
                            hist = df.Histo2D((f"Hist_{x_var}_{y_var}_{df_name}", f"#splitline{{#splitline{{{display_name}: {variable_Title_name(y_var)} vs {variable_Title_name(x_var)}}}{{{extra_title or ''}}}}}{{{title_suffix}}}", x_bins, x_min, x_max, y_bins, y_min, y_max), x_var, y_var)
                            hist.GetXaxis().SetTitle(variable_Title_name(x_var))
                            hist.GetYaxis().SetTitle(variable_Title_name(y_var))
                            hist.Draw("COLZ")
                            if(var in ["Q2,y", "Q2,xB"]):
                                bin_borders = {}
                                for Q2_Y_Bin_ii in range(1, 18, 1):
                                    bin_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii, Use_xB=("xB" in str(var)))
                                    for line in bin_borders[Q2_Y_Bin_ii]:
                                        line.DrawClone("same")
                            canvas.Update()
                            SaveName = f"Histogram_{y_var}_{x_var}_{df_name}{save_suffix}.png"
                            print(f"{color.BOLD}Saving: {color.BLUE}{SaveName}{color.END}\n")
                            canvas.SaveAs(SaveName)

                    else:  # 1D histogram
                        if(len(rdf_filtered_list) == 1):  # Single RDataFrame, draw normally
                            canvas = ROOT.TCanvas(f"Canvas_{var}_{df_name}", f"Canvas for 1D histogram ({display_name})", 800, 600)
                            hist = df.Histo1D((f"Hist_{var}_{df_name}", f"#splitline{{#splitline{{{display_name}: {variable_Title_name(var)}}}{{{extra_title or ''}}}}}{{{title_suffix}}}", var_bins, var_min, var_max), var)
                            hist.GetXaxis().SetTitle(variable_Title_name(var))
                            hist.Draw("HIST E0")
                            SaveName = f"Histogram_{var}_{df_name}{save_suffix}.png"
                            print(f"{color.BOLD}Saving: {color.BLUE}{SaveName}{color.END}\n")
                            canvas.SaveAs(SaveName)
                        else:  # Multiple RDataFrames, normalize and draw on same canvas
                            canvas = ROOT.TCanvas(f"Canvas_{var}_combined", f"Canvas for 1D histograms ({variable_Title_name(var)})", 800, 600)
                            legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
                            for df_name, df in rdf_filtered_list.items():
                                hist = df.Histo1D((f"Hist_{var}_{df_name}", f"#splitline{{#splitline{{{variable_Title_name(var)}}}{{{extra_title or ''}}}}}{{{title_suffix}}}", var_bins, var_min, var_max), var)
                                hist.SetLineColor(color_map[df_name])
                                hist.Scale(100 / hist.Integral())  # Normalize the histogram
                                hist.GetXaxis().SetTitle(variable_Title_name(var))
                                hist.Draw("HIST E0 SAME")
                                legend.AddEntry(hist, rdf_labels[df_name], "l")
                            legend.Draw()
                            SaveName = f"Histogram_{var}{save_suffix}.png"
                            print(f"{color.BOLD}Saving: {color.BLUE}{SaveName}{color.END}\n")
                            canvas.SaveAs(SaveName)



if(__name__ == "__main__"):
    # Map the RDataFrame selections to the actual RDataFrames
    rdf_mapping  = {'rdf': rdf, 'mdf': mdf, 'gdf': gdf}
    rdf_selected = {df_name: rdf_mapping[df_name] for df_name in args.rdf_list}

    # Create histograms based on parsed arguments
    create_histograms(args.variables, rdf_selected, args.title, args.Q2_y_Bin, args.z_pT_Bin, args.cut, args.show_cut, args.gdf_special_cut, args.bins, args.range_min, args.range_max, args.limit_range)

print("Done")