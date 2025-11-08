#!/usr/bin/env python3

import sys
import ROOT
import math

# Turns off the canvases when running in the command line
ROOT.gROOT.SetBatch(1)

import traceback
import os
import re

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


import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    # Map ANSI codes to HTML spans
    # ansi_html_map = {
    #     # Styles
    #     '\033[1m': '<span style="font-weight:bold;">',           # BOLD
    #     '\033[2m': '<span style="opacity:0.7;">',                # LIGHT (dim)
    #     '\033[3m': '<span style="font-style:italic;">',          # ITALIC
    #     '\033[4m': '<span style="text-decoration:underline;">',  # UNDERLINE
    #     '\033[5m': '<span style="text-decoration:blink;">',      # BLINK
    #     # Colors
    #     '\033[91m': '<span style="color:red;">',                 # RED
    #     '\033[92m': '<span style="color:limegreen;">',           # GREEN
    #     '\033[93m': '<span style="color:gold;">',                # YELLOW
    #     '\033[94m': '<span style="color:dodgerblue;">',          # BLUE
    #     '\033[95m': '<span style="color:orchid;">',              # PURPLE
    #     '\033[96m': '<span style="color:cyan;">',                # CYAN
    #     '\033[36m': '<span style="color:darkcyan;">',            # DARKCYAN
    #     '\033[35m': '<span style="color:violet;">',              # PINK (same code as purple but okay)
    #     # Reset (closes span)
    #     '\033[0m': '</span>',
    # }
    ansi_html_map = {
        # Styles
        '\033[1m': "",
        '\033[2m': "",
        '\033[3m': "",
        '\033[4m': "",
        '\033[5m': "",
        # Colors
        '\033[91m': "",
        '\033[92m': "",
        '\033[93m': "",
        '\033[94m': "",
        '\033[95m': "",
        '\033[96m': "",
        '\033[36m': "",
        '\033[35m': "",
        # Reset (closes span)
        '\033[0m': "",
    }
    # Replacing combinations of `color` codes (like color.Error) in a way that HTML nesting works correctly (example: \033[91m\033[1m -> red + bold)
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    # # Optional: replace newlines with <br> for HTML emails
    # text = text.replace('\n', '<br>\n')
    return text

# def send_email(subject, body, recipient):
#     # Send an email via the system mail command.
#     subprocess.run(["mail", "-s", subject, recipient], input=body.encode(), check=False)

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)
    # subprocess.run(["mail", "--append-header", "Content-Type: text/html", "-s", subject, recipient], input=html_body.encode(), check=False)



import ROOT
import argparse

def parse_args():
    p = argparse.ArgumentParser(description=f"""{color.BOLD}Assign_Uncertainties_to_unfolding.py analysis script:{color.END}
    Meant for looking at the histograms in the output ROOT files from 'Multi5D_Bayes_RooUnfold_SIDIS_dedicated_script.py' and 'Just_RooUnfold_SIDIS_richcap.py'.
    The primary purpose will be to assign uncertainties by comparing the baseline results to the unfolding tests.
""", formatter_class=argparse.RawTextHelpFormatter)#formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-ns', '--test', '--time', '--no-save', action='store_true', dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut_AND_Errors_done_with_kCovToy.root",
                   help="Name of ROOT input file. (Current Default: 'Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut_AND_Errors_done_with_kCovToy.root')")
    p.add_argument('-ff', '--file_format', type=str, default=".png", choices=['.png', '.pdf', '.root'],
                   help="Output File Formats. (Defaults to PNG)")

    p.add_argument('-so', '--smearing_option', type=str, default="Smear", choices=["Smear", "''"],
                  help="Smearing options for unfolding. Defaults to 'Smear' whenever hardcoded not to.")
    
    # simulation / modulation / closure
    p.add_argument('-sim', '--simulation', action='store_true', dest='sim',
                   help="Use reconstructed MC instead of experimental data.")
    p.add_argument('-mod', '--modulation', action='store_true', dest='mod',
                   help="Use modulated MC files to create response matrices.")
    p.add_argument('-close', '--closure',  action='store_true', dest='closure',
                   help="Run Closure Test (unfold modulated MC with itself).")
    p.add_argument('-data', '--data_compare',  action='store_true', dest='data',
                   help="Compares Data distributions to MC (can run with `-mod` to modify the MC with the injected modulations and acceptance weights).")

    p.add_argument('-rb', '--remake_bin_by_bin',  action='store_true', dest='remake',
                   help="Remakes bin-by-bin acceptance corrections for 'Mod_Test' and 'Sim_Test' while weighing the modulated MC to the same statistics as the normal MC.")

    # # fitting / output control
    p.add_argument('-nf', '--no-fit', action='store_true', dest='no_fit',
                   help="Disable fitting of plots.")
    
    p.add_argument('-t', '--title', type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-sn', '--save_name', type=str, default="",
                   help="Adds an extra string to the end of the file names that the images will be saved as.")

    p.add_argument('-evgen', '--EvGen', action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-u', '--unfold', type=str, default="Bayesian", 
                   help="Histogram type option. (Default: 'Bayesian')")

    p.add_argument('-d', '--dimensions', type=str, default="3D", 
                   help="Unfolding Dimensions option. (Default: '3D')")

    p.add_argument('-b', '-q2_y', '--bins', nargs="+", type=str, default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
                   help="List of Q2-y bin indices to run.")

    p.add_argument('-z_pt', '--z_pt', nargs="+", type=int, 
                   help="List of z-pT bin indices to run. (Will run all z-pT bins if select ones are not given)")

    p.add_argument('-all', '--all_z_pt', action='store_true',
                   help="Draws all possible z-pT plots together in one image.")
    
    p.add_argument('-v', '--verbose', action='store_true',
                   help="Prints each Histogram name to be saved.")

    p.add_argument('-e', '--email', action='store_true',
                   help="Sends an email when the script is done running (if selected).")
    
    p.add_argument('-em', '--email_message', type=str, default="", 
                   help="Adds an extra user-defined message to emails sent with the `--email` option.")

    p.add_argument('-n', '--normalize', action='store_true',
                   help="Forces Comparison plots to be normalized using 'Normalize_To_Shared_Bins'. (Only used with `-sim` and `-mod`)")

    p.add_argument('-ue',  '--use_errors', action='store_true',
                   help="Applies uncertainties to the baseline histograms based on their differences to their comparisons. (Calculated during comparisons — will update later to use the output files too)")

    p.add_argument('-uej', '--use_errors_json', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Mod_Test_Unfolding_Bin_Differences.json", 
                   help="Will apply uncertainties to the baseline histograms based on the file given with this argument if the `--use_errors` option is selected. (Is not used for the `--mod` option)")
    
    return p.parse_args()

args = parse_args()


       
Saving_Q = not args.test
Fit_Test = not args.no_fit

if(args.remake and (args.unfold not in ["Bin"])):
    print(f"{color.RED}Option to use '--remake_bin_by_bin' requires Bin-by-Bin corrections to be selected.{color.END}")
    args.unfold = "Bin"


Standard_Histogram_Title_Addition = ""
if(args.sim):
    print(f"\n{color.BLUE}Running Simulated Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
    args.root = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Synthetic_Data_with_kCovToy.root"

if(args.closure):
    print(f"\n{color.BLUE}Running Closure Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation with itself"
    args.root = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Closure_Test_with_kCovToy.root"

if(args.title):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{{args.title}}}"
    else:
        Standard_Histogram_Title_Addition = args.title
    print(f"\nAdding the following extra title to the histograms:\n\t{Standard_Histogram_Title_Addition}\n")
    
if(not Fit_Test):
    print(f"\n\n{color.BBLUE}{color_bg.RED}\n\n    Not Fitting Plots    \n{color.END}\n\n")

if((args.file_format != ".png") and Saving_Q):
    print(f"\n{color.BGREEN}Save Option was not set to output .png files. Save format is: {color.ERROR}{args.file_format}{color.END}\n")

# # 'Binning_Method' is defined in 'MyCommonAnalysisFunction_richcap'

Q2_y_Bin_List = args.bins

if(Q2_y_Bin_List != ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']):
    print(f"\n{color.BOLD}Running with the following Q2-y Bins:\t{color.GREEN}{Q2_y_Bin_List}{color.END}\n")

if(args.use_errors):
    print(f"\n{color.BOLD}Applying the additional uncertainties to the baseline histograms{color.END}\n")

print(f"\n{color.BOLD}Starting RG-A SIDIS Analysis{color.END}\n\n")




################################################################################################################################################
##### Individual Image/Histogram Functions #####################################################################################################
################################################################################################################################################

import json
def Apply_PreBin_Uncertainties(Histo_In, Q2_y_Bin, z_pT_Bin, Uncertainty_File_In=args.use_errors_json):
    # Modify the bin uncertainties of a histogram using precomputed values
    # from a JSON file. If any condition fails, return the unmodified histogram.
    if(Uncertainty_File_In is None):
        return Histo_In
    # Check histogram validity
    if((not Histo_In) or (not Histo_In.InheritsFrom("TH1"))):
        print(f"{color.Error}Error:{color.END}\n\t{Histo_In} is an invalid histogram that was passed to Apply_PreBin_Uncertainties()")
        return Histo_In
    # Load the JSON file
    with open(Uncertainty_File_In, "r") as jf:
        data = json.load(jf)
    # Construct key based on cosmetic naming convention
    key = f"{Q2_y_Bin}_{z_pT_Bin}"
    if(key not in data):
        print(f"{color.RED}Error:{color.END} Key '{key}' not found in {Uncertainty_File_In}")
        return Histo_In
    bin_data = data[key]
    # Check number of bins
    n_bins_hist = Histo_In.GetNbinsX()
    n_bins_data = len(bin_data)
    if(n_bins_data != n_bins_hist):
        print(f"{color.Error}Error:{color.END} Bin count mismatch (JSON={n_bins_data}, Histo={n_bins_hist}). Aborting modification.")
        return Histo_In
    # Apply new errors to each bin
    for i, entry in enumerate(bin_data, start=1):
        diff_val = entry.get("diff", 0.0)
        err_val  = entry.get("err", 0.0)
        current_err = Histo_In.GetBinError(i)
        new_err = ROOT.sqrt(current_err**2 + (diff_val + err_val)**2)
        Histo_In.SetBinError(i, new_err)
    return Histo_In


def Normalize_To_Shared_Bins(histo1, histo2, threshold=0.0, include_under_over=False, name_suffix="_NormShared"):
    # Returns two cloned histograms scaled so that the sum over shared bins equals 1 for each.
    # A "shared" bin is one where both histograms have content strictly greater than 'threshold'.
    # Errors scale automatically via TH1::Scale.

    # Basic checks
    if((not histo1) or (not histo2)):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): one or both histograms are None.")
        return histo1, histo2, [], None, None

    if((not histo1.InheritsFrom("TH1D")) or (not histo2.InheritsFrom("TH1D"))):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): both inputs must be TH1D.")
        return histo1, histo2, [], None, None

    if(histo1.GetNbinsX() != histo2.GetNbinsX()):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): different binning (NbinsX mismatch).")
        return histo1, histo2, [], None, None

    # Determine bin range
    first_bin = 0 if(include_under_over) else 1
    last_bin  = histo1.GetNbinsX() + 1 if(include_under_over) else histo1.GetNbinsX()

    # Find shared bins (both contents > threshold)
    shared_bins = []
    for ib in range(first_bin, last_bin + 1):
        c1 = histo1.GetBinContent(ib)
        c2 = histo2.GetBinContent(ib)
        if((c1 > threshold) and (c2 > threshold)):
            shared_bins.append(ib)

    if(len(shared_bins) == 0):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): no shared bins found with threshold={threshold}.")
        return histo1, histo2, [], None, None

    # Compute integrals over shared bins
    sum1 = 0.0
    sum2 = 0.0
    for ib in shared_bins:
        sum1 += histo1.GetBinContent(ib)
        sum2 += histo2.GetBinContent(ib)

    if((sum1 <= 0.0) or (sum2 <= 0.0)):
        print(f"{color.Error}ERROR:{color.END} Normalize_To_Shared_Bins(): non-positive shared integral (sum1={sum1}, sum2={sum2}).")
        return histo1, histo2, shared_bins

    # Clone and scale (shape-only normalization on shared support)
    h1n = histo1.Clone(histo1.GetName() + name_suffix)
    h2n = histo2.Clone(histo2.GetName() + name_suffix)
    h1n.Scale(1.0 / sum1)
    h2n.Scale(1.0 / sum2)

    # Cosmetic: ensure stats boxes are off for clean overlays
    h1n.SetStats(0)
    h2n.SetStats(0)

    if(args.verbose):
        print(f"{color.BGREEN}Normalized to shared bins:{color.END} {len(shared_bins)} bins; thresholds > {threshold}")
    return h1n, h2n, shared_bins, sum1, sum2



def Save_Histograms_As_Images(ROOT_In, HISTO_NAME_In, Format=args.file_format, SAVE=args.save_name, SAVE_prefix="", TITLE=Standard_Histogram_Title_Addition, Return_Histos=False):
    # Retrieve histogram from ROOT file
    histo = ROOT_In.Get(HISTO_NAME_In)
    if(not histo):
        print(f"Histogram '{HISTO_NAME_In}' not found in file '{ROOT_In.GetName()}'")
        return False
    if(("Pass 2" in histo.GetTitle()) and (TITLE not in histo.GetTitle())):
        histo.SetTitle(str(histo.GetTitle()).replace("Pass 2", TITLE))
    elif(TITLE not in histo.GetTitle()):
        histo.SetTitle(f"#splitline{{{histo.GetTitle()}}}{{{TITLE}}}")
    # Turn off stat box
    histo.SetStats(0)
    if(Return_Histos):
        return histo
    else:
        # Create a canvas
        canvas_name = f"c_{HISTO_NAME_In}"
        c = ROOT.TCanvas(canvas_name, canvas_name, 800, 700)
        c.cd()
        # Draw histogram
        histo.Draw("COLZ" if("TH2" in histo.ClassName()) else "H L P E0 same")
        # Set output file name
        Save_Name = f"{SAVE_prefix}{HISTO_NAME_In}_{SAVE}{Format}"
        for replace in ["(", ")", "'", '"', "'"]:
            Save_Name = Save_Name.replace(replace, "")
        Save_Name = Save_Name.replace("SMEAR=Smear", "Smeared")
        Save_Name = Save_Name.replace("SMEAR=_", "")
        Save_Name = Save_Name.replace("__", "_")
        Save_Name = Save_Name.replace("_.", ".")
        c.SaveAs(str(Save_Name))
        print(f"Saved histogram '{HISTO_NAME_In}' as: {Save_Name}")
        return True


def Make_New_BbB_Mod(ROOT_IN_NORMAL, ROOT_IN_MODULATED, HISTO_NAME_INPUT):
    # Retrieve the unmodulated (baseline) histograms
    rdf_histo_norm =    ROOT_IN_NORMAL.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(rdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    gdf_histo_norm =    ROOT_IN_NORMAL.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(gdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    mdf_histo_norm =    ROOT_IN_NORMAL.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(mdf)")))

    # Retrieve the modulated MC histograms
    gdf_histo__mod = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(gdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    mdf_histo__mod = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(mdf)")))

    # Validate input histograms
    if((not rdf_histo_norm) or (not gdf_histo_norm) or (not mdf_histo_norm) or (not gdf_histo__mod) or (not mdf_histo__mod)):
        print(f"{color.Error}ERROR:{color.END} Missing one or more histograms in Make_New_BbB_Mod().")
        return None, None

    # Clone RDF
    bbb_norm_cor = rdf_histo_norm.Clone(f"{HISTO_NAME_INPUT}_Updated_Norm")
    bbb__mod_cor = rdf_histo_norm.Clone(f"{HISTO_NAME_INPUT}_Updated__Mod")

    # Normalize modulated MC REC to the total MC yield of the normal sample
    norm_mdf_norm = mdf_histo_norm.Integral()
    norm_mdf_mod  = mdf_histo__mod.Integral()
    if(norm_mdf_mod <= 0):
        print(f"{color.Error}ERROR:{color.END} Modulated reconstructed MC has zero or negative integral — cannot normalize.")
        return bbb_norm_cor, bbb__mod_cor
    scale_factor_mdf = norm_mdf_norm / norm_mdf_mod
    mdf_histo__mod.Scale(scale_factor_mdf)
    if(args.verbose):
        print(f"{color.BGREEN}Scaled modulated MC REC by factor {scale_factor_mdf:.4f}{color.END}")
        
    # Normalize modulated MC GEN to the total MC yield of the normal sample
    norm_gdf_norm = gdf_histo_norm.Integral()
    norm_gdf_mod  = gdf_histo__mod.Integral()
    if(norm_gdf_mod <= 0):
        print(f"{color.Error}ERROR:{color.END} Modulated generated MC has zero or negative integral — cannot normalize.")
        return bbb_norm_cor, bbb__mod_cor
    scale_factor_gdf = norm_gdf_norm / norm_gdf_mod
    gdf_histo__mod.Scale(scale_factor_gdf)
    if(args.verbose):
        print(f"{color.BGREEN}Scaled modulated MC GEN by factor {scale_factor_gdf:.4f}{color.END}")
        
    # Recompute Acceptance: ratio (mdf/gdf) using the *unmodulated* (normal) histograms
    adf_histo_norm = mdf_histo_norm.Clone(f"""{HISTO_NAME_INPUT.replace(f"({args.unfold})", "(Acceptance)")}_Updated_Norm""")
    adf_histo_norm.Divide(gdf_histo_norm)
    # Recompute Acceptance: ratio (mdf/gdf) using the *modulated* histograms
    adf_histo__mod = mdf_histo__mod.Clone(f"""{HISTO_NAME_INPUT.replace(f"({args.unfold})", "(Acceptance)")}_Updated__Mod""")
    adf_histo__mod.Divide(gdf_histo__mod)

    bbb_norm_cor.Divide(adf_histo_norm)
    bbb__mod_cor.Divide(adf_histo__mod)
    
    # Cosmetic cleanup
    Original_Title_Norm = (ROOT_IN_NORMAL.Get(HISTO_NAME_INPUT)).GetTitle()
    if("Pass 2" in Original_Title_Norm):
        Original_Title_Norm = Original_Title_Norm.replace("Pass 2", "Remade these plots after the acceptance weights were already applied")
    else:
        Original_Title_Norm = f"#splitline{{{Original_Title_Norm}}}{{Remade these plots after the acceptance weights were already applied}}"
    Original_Title__Mod = (ROOT_IN_MODULATED.Get(HISTO_NAME_INPUT)).GetTitle()
    if("Pass 2" in Original_Title__Mod):
        Original_Title__Mod = Original_Title__Mod.replace("Pass 2", "Remade these plots after the acceptance weights were already applied")
    else:
        Original_Title__Mod = f"#splitline{{{Original_Title__Mod}}}{{Remade these plots after the acceptance weights were already applied}}"
        
    bbb_norm_cor.SetTitle(Original_Title_Norm)
    bbb__mod_cor.SetTitle(Original_Title__Mod)
    bbb_norm_cor.SetLineColor(28)
    bbb_norm_cor.SetMarkerColor(28)
    bbb__mod_cor.SetLineColor(ROOT.kGreen + 2)
    bbb__mod_cor.SetMarkerColor(ROOT.kGreen + 2)

    if(args.verbose):
        print(f"{color.BOLD}Created corrected histograms:{color.END}\n\t{bbb_norm_cor.GetName()}\nand\n\t{bbb__mod_cor.GetName()}")

    return bbb_norm_cor, bbb__mod_cor


def Make_New_BbB_Sim(ROOT_IN_MODULATED, HISTO_NAME_INPUT):
    # The unmodulated (baseline) ROOT file is not loaded by default for `Sim_Test` -> Loading now
    ROOT_IN_NORMAL = ROOT.TFile.Open("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut_AND_Errors_done_with_kCovToy.root", "READ")
    
    # Retrieve the unmodulated (baseline) histograms
    gdf_histo_norm     = ROOT_IN_NORMAL.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(gdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    mdf_histo_norm     = ROOT_IN_NORMAL.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(mdf)")))
    # Retrieve the modulated MC histograms
    try:
        rdf_histo__sim = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(rdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
        if((not rdf_histo__sim)):
            raise ValueError("Synthetic rdf without smearing is missing")
    except:
        rdf_histo__sim = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(rdf)")))
    try:
        tdf_histo__sim = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(tdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
        if((not tdf_histo__sim)):
            raise ValueError("True (modulated) tdf without smearing is missing")
    except:
        tdf_histo__sim = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(tdf)")))
    gdf_histo__mod     = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(gdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    mdf_histo__mod     = ROOT_IN_MODULATED.Get(str(HISTO_NAME_INPUT.replace(f"({args.unfold})", "(mdf)")))

    # # Validate input histograms
    # if((not rdf_histo__sim) or (not gdf_histo_norm) or (not mdf_histo_norm) or (not gdf_histo__mod) or (not mdf_histo__mod)):
    #     print(f"{color.Error}ERROR:{color.END} Missing one or more histograms in Make_New_BbB_Mod().")
    #     return None, None

    # Normalize modulated MC REC to the total MC yield of the normal sample
    norm_mdf_norm    = mdf_histo_norm.Integral()
    for verbose_name, rec_Normalizing in [["Synthetic", rdf_histo__sim], ["Modulated", mdf_histo__mod]]:
        norm_mdf_mod = rec_Normalizing.Integral()
        # if(norm_mdf_mod <= 0):
        #     print(f"{color.Error}ERROR:{color.END} Modulated reconstructed MC has zero or negative integral — cannot normalize.")
        #     return bbb_norm_cor, bbb__mod_cor
        scale_factor_mdf = norm_mdf_norm / norm_mdf_mod
        rec_Normalizing.Scale(scale_factor_mdf)
        if(args.verbose):
            print(f"{color.BGREEN}Scaled {verbose_name} MC REC by factor {scale_factor_mdf:.4f}{color.END}")
            
    # Clone RDF
    bbb_sim_cor = rdf_histo__sim.Clone(f"{HISTO_NAME_INPUT}_Updated_Sim")
        
    # Normalize modulated MC GEN to the total MC yield of the normal sample
    norm_gdf_norm    = gdf_histo_norm.Integral()
    for verbose_name, gen_Normalizing in [["True", tdf_histo__sim], ["Modulated", gdf_histo__mod]]:
        norm_gdf_mod = gen_Normalizing.Integral()
        # if(norm_gdf_mod <= 0):
        #     print(f"{color.Error}ERROR:{color.END} Modulated generated MC has zero or negative integral — cannot normalize.")
        #     return bbb_norm_cor, bbb__mod_cor
        scale_factor_gdf = norm_gdf_norm / norm_gdf_mod
        gen_Normalizing.Scale(scale_factor_gdf)
        if(args.verbose):
            print(f"{color.BGREEN}Scaled {verbose_name} MC GEN by factor {scale_factor_gdf:.4f}{color.END}")
            
        
    # Recompute Acceptance: ratio (mdf/gdf) using the *unmodulated* (normal) histograms
    adf_histo_norm = mdf_histo_norm.Clone(f"""{HISTO_NAME_INPUT.replace(f"({args.unfold})", "(Acceptance)")}_Updated_Norm""")
    adf_histo_norm.Divide(gdf_histo_norm)


    bbb_sim_cor.Divide(adf_histo_norm)
    Original_Title_bbb = (ROOT_IN_MODULATED.Get(HISTO_NAME_INPUT)).GetTitle()
    if("Pass 2" in Original_Title_bbb):
        Original_Title_bbb = Original_Title_bbb.replace("Pass 2", "Remade these plots after the acceptance weights were already applied")
    else:
        Original_Title_bbb = f"#splitline{{{Original_Title_bbb}}}{{Remade these plots after the acceptance weights were already applied}}"
    bbb_sim_cor.SetTitle(Original_Title_bbb)
    tdf_histo__sim.SetTitle(f"#splitline{{{tdf_histo__sim.GetTitle()}}}{{Scaled to Normal Generated MC}}")

    bbb_sim_cor.SetLineColor(28)
    bbb_sim_cor.SetMarkerColor(28)
    
    if(args.verbose):
        print(f"{color.BOLD}Created/scaled histograms:{color.END}\n\t{bbb_sim_cor.GetName()}\nand\n\t{tdf_histo__sim.GetName()}")

    return bbb_sim_cor, tdf_histo__sim





Unfolding_Diff_Data = {}
def Compare_TH1D_Histograms(ROOT_In_1, HISTO_NAME_1, ROOT_In_2, HISTO_NAME_2, legend_labels=("Histogram 1", "Histogram 2"), output_prefix="Compare_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str="1", zPT_str="1", Unfolding_Diff_Data_In=Unfolding_Diff_Data, Return_Histos=False):
    # Retrieve histograms
    if(args.remake and (args.mod or args.sim)):
        output_prefix = f"Resummed_Weights_{output_prefix}"
        if(args.mod):
            histo1, histo2 = Make_New_BbB_Mod(ROOT_IN_NORMAL=ROOT_In_1, ROOT_IN_MODULATED=ROOT_In_2, HISTO_NAME_INPUT=HISTO_NAME_1)
        elif(args.sim):
            histo1, histo2 = Make_New_BbB_Sim(ROOT_IN_MODULATED=ROOT_In_1, HISTO_NAME_INPUT=HISTO_NAME_1)
        else:
            print(f"{color.Error}ERROR:{color.END} Could not remake the histograms for the test requested.\n\t{color.BOLD}Returning default outputs")
            histo1 = ROOT_In_1.Get(HISTO_NAME_1)
            histo2 = ROOT_In_2.Get(HISTO_NAME_2)
    else:
        histo1 = ROOT_In_1.Get(HISTO_NAME_1)
        histo2 = ROOT_In_2.Get(HISTO_NAME_2)
    histo1.SetStats(0)
    histo2.SetStats(0)
    # Ensure both exist
    if((not histo1) or (not histo2)):
        print(f"{color.Error}ERROR:{color.END} Could not retrieve one or both histograms.")
        if(not Return_Histos):
            return False, Unfolding_Diff_Data_In
        else:
            return histo1, histo2, None, Unfolding_Diff_Data_In
    # Ensure both are TH1D
    if((not histo1.InheritsFrom("TH1D")) or (not histo2.InheritsFrom("TH1D"))):
        print(f"{color.Error}ERROR:{color.END} Both histograms must be TH1D.")
        if(not Return_Histos):
            return False, Unfolding_Diff_Data_In
        else:
            return histo1, histo2, None, None, Unfolding_Diff_Data_In
    
    # if(args.use_errors and (not args.mod)):
    #     histo1 = Apply_PreBin_Uncertainties(Histo_In=histo1, Q2_y_Bin=Q2y_str, z_pT_Bin=zPT_str, Uncertainty_File_In=args.use_errors_json)
    # if(args.sim):
    normalization_to_histo1, normalization_to_histo2 = 1.0, 1.0
    if(args.normalize):
        histo1, histo2, _, normalization_to_histo1, normalization_to_histo2 = Normalize_To_Shared_Bins(histo1, histo2, threshold=0.0, include_under_over=False, name_suffix="_NormShared")
    
    if(("Pass 2" in histo1.GetTitle()) and ((TITLE not in histo1.GetTitle()) and (TITLE not in histo2.GetTitle()))):
        histo1.SetTitle(str(histo1.GetTitle()).replace("Pass 2", TITLE))
    elif((TITLE not in histo1.GetTitle()) and (TITLE not in histo2.GetTitle())):
        histo1.SetTitle(f"#splitline{{{histo1.GetTitle()}}}{{{TITLE}}}")
    
    # Clone one histogram to create the difference histogram
    h_diff = histo1.Clone(f"{HISTO_NAME_1}_vs_{HISTO_NAME_2}_absdiff")
    h_diff.Reset("ICES")  # clear contents, keep errors and structure
    h_diff.SetStats(0)

    h_uncertainty = h_diff.Clone(f"{HISTO_NAME_1}_Modeled_Uncertainty")
    h_uncertainty.Reset("ICES")  # clear contents, keep errors and structure
    h_uncertainty.SetStats(0)

    histo_key = f"{Q2y_str}_{zPT_str}"
    # Initialize the dictionary entry if it doesn't exist
    if(histo_key not in Unfolding_Diff_Data_In):
        Unfolding_Diff_Data_In[histo_key] = []
    max_content = 0
    max_cd_1    = 0
    max_M_uncer = 0
    # Fill it with |bin1 - bin2|
    for bin_idx in range(1, histo1.GetNbinsX() + 1):
        val1        = histo1.GetBinContent(bin_idx)
        val2        = histo2.GetBinContent(bin_idx)
        err1        = histo1.GetBinError(bin_idx)
        err2        = histo2.GetBinError(bin_idx)
        max_cd_1    = max([max_cd_1, val1 + err1, val2 + err2])
        diff        = abs(val1 - val2)
        err         = math.sqrt(err1**2 + err2**2)
        # M_uncer     = math.sqrt(max([0, (val2 - val1)**2 - err**2]))
        M_uncer     = diff
        max_content = max([max_content, diff])
        max_M_uncer = max([max_M_uncer, M_uncer])
        # max_content = max([max_content, diff + err])
        h_diff.SetBinContent(bin_idx,           diff)
        h_diff.SetBinError(bin_idx,              err)
        h_uncertainty.SetBinContent(bin_idx, M_uncer)
        h_uncertainty.SetBinError(bin_idx,       0.0)
        Unfolding_Diff_Data_In[histo_key].append({"phi_bin": bin_idx, f"{legend_labels[0]} — Value": val1, f"{legend_labels[0]} — Error": err1, f"{legend_labels[1]} — Value": val2, f"{legend_labels[1]} — Error": err2, "diff": diff, "err": err, "uncertainty": M_uncer, "scale_to_nominal": normalization_to_histo1, "scale_to_variation": normalization_to_histo2})
        # if(args.use_errors and args.mod):
        #     histo1.SetBinError(bin_idx, math.sqrt(err1**2 + (diff + err)**2))
        # if(args.use_errors):
        #     histo1.SetBinError(bin_idx, math.sqrt(err1**2 + diff**2))
        if(args.use_errors):
            histo1.SetBinError(bin_idx, math.sqrt(err1**2 + M_uncer**2))
    h_diff.GetYaxis().SetRangeUser(0,        1.2*max_content)
    h_uncertainty.GetYaxis().SetRangeUser(0, 1.2*max_M_uncer)
    histo1.GetYaxis().SetRangeUser(0,        1.2*max_cd_1)
    histo2.GetYaxis().SetRangeUser(0,        1.2*max_cd_1)

    if(histo1.GetLineColor() == histo2.GetLineColor()):
        histo2.SetLineColor((histo2.GetLineColor() + 2) if(histo2.GetLineColor() != 28) else 26)
    histo1.SetLineWidth(3)
    histo2.SetLineWidth(2)
    
    h_diff.SetLineColor(ROOT.kBlack)
    h_diff.SetLineWidth(2)
    h_diff.SetTitle(f"#splitline{{Absolute Bin Content Differences between}}{{{root_color.Bold}{{{legend_labels[0]}}} and {root_color.Bold}{{{legend_labels[1]}}}}}")
    # if(args.use_errors and args.mod):
    # if(args.use_errors):
    #     h_diff.SetTitle(f"#splitline{{{h_diff.GetTitle()}}}{{#scale[1.25]{{#splitline{{These differences have been added to}}{{the uncertainties of {root_color.Bold}{{{legend_labels[0]}}}}}}}}}")
    h_diff.GetYaxis().SetTitle("#Delta Bin Contents")

    h_uncertainty.SetLineColor(ROOT.kOrange + 2)
    h_uncertainty.SetLineWidth(2)
    h_uncertainty.SetTitle(f"#splitline{{Modeled Uncertainty between}}{{{root_color.Bold}{{{legend_labels[0]}}} and {root_color.Bold}{{{legend_labels[1]}}}}}")
    if(args.use_errors):
        h_uncertainty.SetTitle(f"#splitline{{{h_uncertainty.GetTitle()}}}{{#scale[1.25]{{#splitline{{These uncertainties have been propagated to}}{{{root_color.Bold}{{{legend_labels[0]}}}}}}}}}")
    h_uncertainty.GetYaxis().SetTitle("Model Uncertainty")

    if(Return_Histos):
        return histo1, histo2, h_diff, h_uncertainty, Unfolding_Diff_Data_In
    else:
        # Create canvas
        canvas_name = f"c_{output_prefix}{HISTO_NAME_1}_vs_{HISTO_NAME_2}"
        c = ROOT.TCanvas(canvas_name, canvas_name, 2000, 700)
        c.Divide(3, 1)
    
        # Pad 1: Overlay the two histograms
        c.cd(1)
        histo1.Draw("H P E0")
        histo2.Draw("H P E0 SAME")
    
        # Add legend
        legend = ROOT.TLegend(0.45, 0.15, 0.7, 0.35)
        legend.SetBorderSize(1)
        legend.SetFillStyle(0)
        legend.AddEntry(histo1, f"#scale[1.75]{{{legend_labels[0]}}}", "APL E")
        legend.AddEntry(histo2, f"#scale[1.75]{{{legend_labels[1]}}}", "APL E")
        legend.Draw()

        # Pad 2: Draw the Model Uncertainties
        c.cd(2)
        h_uncertainty.Draw("H P E0")
        
        # Pad 3: Draw the absolute difference
        c.cd(3)
        h_diff.Draw("H P E0")
    
        # Save
        Save_Name = f"{output_prefix}{HISTO_NAME_1}{SAVE}{Format}"
        for replace in ["(", ")", "'", '"', "'"]:
            Save_Name = Save_Name.replace(replace, "")
        Save_Name = Save_Name.replace("__", "_")
        Save_Name = Save_Name.replace("SMEAR=Smear", "Smeared")
        Save_Name = Save_Name.replace("SMEAR=_", "")
        Save_Name = Save_Name.replace("__", "_")
        Save_Name = Save_Name.replace("_.", ".")
        c.SaveAs(Save_Name)
        print(f"Saved comparison as: {Save_Name}")
        return True, Unfolding_Diff_Data_In




################################################################################################################################################
##### Individual Image/Histogram Functions ^ ###################################################################################################
##### Large/Combined Image Function          ###################################################################################################
################################################################################################################################################


def z_pT_Images_Together_For_Comparisons(ROOT_Input_In=None, ROOT_Mod_In=None, Unfolding_Diff_Data_Input={}, Q2_Y_Bin=1, Plot_Orientation="z_pT"):
    HISTO_NAME = f"\n{color.ERROR}ERROR{color.END}\n"
    if(args.dimensions   in ["1D"]):
        HISTO_NAME  = f"(1D)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_ALL)_(phi_t)"
    elif(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
        HISTO_NAME  = f"(MultiDim_3D_Histo)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_ALL)_(MultiDim_z_pT_Bin_Y_bin_phi_t)"

    Canvases_to_Make = [HISTO_NAME]
    HISTO_True = "ERROR"
    Legend_Labels = [f"Plots of {args.dimensions} {args.unfold}"]
    if(args.mod):
        Canvases_to_Make = [f"Mod_Test_{HISTO_NAME}", f"Mod_Test_DIFF_{HISTO_NAME}", f"Mod_Test_UNCERTAINTY_{HISTO_NAME}"]
        Legend_Labels    = ["Unfolded with Normal MC", "Unfolded with Modulated MC"]
    elif(args.sim or args.closure):
        Canvases_to_Make = [f"Sim_Test_{HISTO_NAME}", f"Sim_Test_DIFF_{HISTO_NAME}", f"Sim_Test_UNCERTAINTY_{HISTO_NAME}"] if(not args.closure) else [f"Closure_Test_{HISTO_NAME}", f"Closure_Test_DIFF_{HISTO_NAME}", f"Closure_Test_UNCERTAINTY_{HISTO_NAME}"]
        Legend_Labels    = ["Unfolded Synthetic (MC) Data", "True Distribution of Synthetic Data"]
        if(args.dimensions   in ["1D"]):
            HISTO_True   = f"(1D)_(tdf)_(SMEAR=Smear)_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_ALL)_(phi_t)"
        elif(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
            HISTO_True   = f"(MultiDim_3D_Histo)_(tdf)_(SMEAR='')_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_ALL)_(MultiDim_z_pT_Bin_Y_bin_phi_t)"

    #######################################################################################################################################################################################################
    ####  Histogram Creations     #########################################################################################################################################################################
    Saved_Histos   = {}
    z_pT_Bin_Range = range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1] + 1)
    for z_PT_BIN_NUM  in z_pT_Bin_Range:
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_PT_BIN_NUM, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
            continue
        HISTO_NAME_Binned = HISTO_NAME.replace("(z_pT_Bin_ALL)", f"(z_pT_Bin_{z_PT_BIN_NUM})")
        HISTO_True_Binned = HISTO_True.replace("(z_pT_Bin_ALL)", f"(z_pT_Bin_{z_PT_BIN_NUM})")
        if(args.mod):
            if((HISTO_NAME_Binned in ROOT_Input.GetListOfKeys()) and (HISTO_NAME_Binned in ROOT_Mod.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.END}")
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Saved_Histos[f"h_diff_{z_PT_BIN_NUM}"], Saved_Histos[f"h_uncertainty_{z_PT_BIN_NUM}"], Unfolding_Diff_Data_Input =  Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME_Binned, ROOT_In_2=ROOT_Mod,   HISTO_NAME_2=HISTO_NAME_Binned, legend_labels=("Unfolded with Normal MC", "Unfolded with Modulated MC"),               output_prefix="Mod_Test_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_Y_Bin, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data_Input, Return_Histos=True)
        elif(args.sim or args.closure):
            if((HISTO_NAME_Binned in ROOT_Input.GetListOfKeys()) and (HISTO_True_Binned in ROOT_Input.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.BGREEN} and {color.END_b}{HISTO_True_Binned}{color.END}")
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Saved_Histos[f"h_diff_{z_PT_BIN_NUM}"], Saved_Histos[f"h_uncertainty_{z_PT_BIN_NUM}"], Unfolding_Diff_Data_Input =  Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME_Binned, ROOT_In_2=ROOT_Input, HISTO_NAME_2=HISTO_True_Binned, legend_labels=("Unfolded Synthetic (MC) Data", "True Distribution of Synthetic Data"), output_prefix="Sim_Test_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_Y_Bin, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data_Input, Return_Histos=True)
        elif(HISTO_NAME in ROOT_Input.GetListOfKeys()):
            if(args.verbose):
                print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.END}")
            Saved_Histos[str(z_PT_BIN_NUM)] = Save_Histograms_As_Images(ROOT_In=ROOT_Input, HISTO_NAME_In=HISTO_NAME_Binned, Format=args.file_format, SAVE=args.save_name, SAVE_prefix="Sim_Test_" if(args.sim) else "Mod_Test_" if(args.mod) else "", TITLE=Standard_Histogram_Title_Addition, Return_Histos=True)
        else:
            print(f"\n{color.Error}MISSING: {HISTO_NAME_Binned}{color.END}\n")
            
    ####  Histogram Creations     #########################################################################################################################################################################
    #######################################################################################################################################################################################################
    ####  Canvas (Main) Creation  #########################################################################################################################################################################
    All_z_pT_Canvas, All_z_pT_Canvas_cd_1, All_z_pT_Canvas_cd_1_Upper, All_z_pT_Canvas_cd_1_Lower, All_z_pT_Canvas_cd_2, All_z_pT_Canvas_cd_2_cols, legend = {}, {}, {}, {}, {}, {}, {}
    for canvas_num, Canvas_Name in enumerate(Canvases_to_Make):
        All_z_pT_Canvas[Canvas_Name] = Canvas_Create(Name=Canvas_Name, Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
        All_z_pT_Canvas[Canvas_Name].SetFillColor(root_color.LGrey)
        All_z_pT_Canvas_cd_1[Canvas_Name]       = All_z_pT_Canvas[Canvas_Name].cd(1)
        All_z_pT_Canvas_cd_1[Canvas_Name].SetFillColor(root_color.LGrey)
        All_z_pT_Canvas_cd_1[Canvas_Name].SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
        All_z_pT_Canvas_cd_1[Canvas_Name].Divide(1, 2, 0, 0)
        All_z_pT_Canvas_cd_1_Upper[Canvas_Name] = All_z_pT_Canvas_cd_1[Canvas_Name].cd(1)
        All_z_pT_Canvas_cd_1_Upper[Canvas_Name].SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
        All_z_pT_Canvas_cd_1_Upper[Canvas_Name].Divide(1, 1, 0, 0)
        All_z_pT_Canvas_cd_1_Lower[Canvas_Name] = All_z_pT_Canvas_cd_1[Canvas_Name].cd(2)
        All_z_pT_Canvas_cd_1_Lower[Canvas_Name].SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
        All_z_pT_Canvas_cd_1_Lower[Canvas_Name].Divide(1, 1, 0, 0)
        All_z_pT_Canvas_cd_1_Lower[Canvas_Name].cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
        All_z_pT_Canvas_cd_2[Canvas_Name]       = All_z_pT_Canvas[Canvas_Name].cd(2)
        All_z_pT_Canvas_cd_2[Canvas_Name].SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
        All_z_pT_Canvas_cd_2[Canvas_Name].SetFillColor(root_color.LGrey)
        if(Plot_Orientation in ["z_pT"]):
            number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
            All_z_pT_Canvas_cd_2[Canvas_Name].Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
        else:
            number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
            All_z_pT_Canvas_cd_2[Canvas_Name].Divide(1, number_of_cols, 0.0001, 0.0001)
            for ii in range(1, number_of_cols + 1, 1):
                All_z_pT_Canvas_cd_2_cols[Canvas_Name] = All_z_pT_Canvas_cd_2[Canvas_Name].cd(ii)
                All_z_pT_Canvas_cd_2_cols[Canvas_Name].Divide(number_of_rows, 1, 0.0001, 0.0001)
    ####  Canvas (Main) Creation End ######################################################################################################################################################################
    #######################################################################################################################################################################################################
        legend[Canvas_Name] = ROOT.TLegend(0.01, 0.01, 0.99, 0.99)
        Legend_Header = f"#splitline{{#scale[2]{{Q^{{2}}-y Bin {Q2_Y_Bin}}}}}{{#scale[1.5]{{Plots Shown}}}}"
        if(args.normalize):
            Legend_Header = f"#splitline{{{Legend_Header}}}{{Plots were normalized}}"
        if(args.closure):
            Legend_Header = f"#splitline{{#splitline{{#scale[1.5]{{Closure Test}}}}{{Corrected the MC with itself}}}}{{{Legend_Header}}}"
        legend[Canvas_Name].SetHeader(Legend_Header, "C") # option "C" allows to center the header
        if(args.mod or args.sim or args.closure):
            if(canvas_num   == 0):
                for ii, label in enumerate(Legend_Labels):
                    legend[Canvas_Name].AddEntry(Saved_Histos[f"histo{ii+1}_1"], label, "lep")
            elif(canvas_num == 1):
                legend[Canvas_Name].AddEntry(Saved_Histos[f"h_diff_1"],        f"#scale[0.85]{{#splitline{{Differences Between}}{{#splitline{{'{Legend_Labels[0]}' and}}{{'{Legend_Labels[1]}'}}}}}}",         "lep")
            else:
                legend[Canvas_Name].AddEntry(Saved_Histos[f"h_uncertainty_1"], f"#scale[0.85]{{#splitline{{Modeled Uncertainty between}}{{#splitline{{'{Legend_Labels[0]}' and}}{{'{Legend_Labels[1]}'}}}}}}", "lep")
        else:
            legend[Canvas_Name].AddEntry(Saved_Histos["1"], Legend_Labels[0], "lep")
        Draw_Canvas(All_z_pT_Canvas_cd_1_Upper[Canvas_Name], 1, 0.15)
        Blank = Saved_Histos[f"h_diff_1" if(args.mod or args.sim or args.closure) else "1"].Clone("EMPTY")
        Blank.SetTitle("")
        Blank.Draw("H P E0")
        legend[Canvas_Name].DrawClone()
        ROOT.gPad.Update()
        All_z_pT_Canvas[Canvas_Name].Update()
        # legend[Canvas_Name].SetNColumns(2)
        for z_pT in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=int(Q2_Y_Bin))[1]+1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT, BINNING_METHOD=Binning_Method)):
                continue
            cd_number_of_z_pT_all_together = z_pT
            if(Plot_Orientation in ["z_pT"]):
                All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2[Canvas_Name].cd(cd_number_of_z_pT_all_together)
                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
            else:
                cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                if(0  ==    (cd_number_of_z_pT_all_together%number_of_cols)):
                    cd_row += -1
                cd_col =     cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2[Canvas_Name].cd((number_of_cols - cd_col) + 1)
                All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)

            Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
            if(args.mod or args.sim or args.closure):
                if(canvas_num == 0):
                    Saved_Histos[f"histo1_{z_pT}"].Draw("H P E0 SAME")
                    Saved_Histos[f"histo2_{z_pT}"].Draw("H P E0 SAME")
                elif(canvas_num == 1):
                    Saved_Histos[f"h_diff_{z_pT}"].Draw("H P E0")
                else:
                    Saved_Histos[f"h_uncertainty_{z_pT}"].Draw("H P E0")
            else:
                Saved_Histos[str(z_pT)].Draw("H P E0")
            ROOT.gPad.Update()
            All_z_pT_Canvas[Canvas_Name].Update()
                
        ##################################################################### ################################################################ ################################################################
        #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################
        ##################################################################### ################################################################ ################################################################
        Save_Name = f"{Canvas_Name}_{args.save_name}{args.file_format}"
        if(Plot_Orientation != "z_pT"):
            Save_Name = Save_Name.replace(f"{args.save_name}{args.file_format}", f"{args.save_name}_Flipped{args.file_format}")
        for replace in ["(", ")", "'", '"', "'"]:
            Save_Name = Save_Name.replace(replace, "")
        if(args.remake):
            Save_Name = f"Remade_with_normalization_weights_{Save_Name}"
        Save_Name = Save_Name.replace("__", "_")
        Save_Name = Save_Name.replace("SMEAR=Smear", "Smeared")
        Save_Name = Save_Name.replace("SMEAR=_", "")
        Save_Name = Save_Name.replace("__", "_")
        Save_Name = Save_Name.replace("_.", ".")
        All_z_pT_Canvas[Canvas_Name].SaveAs(Save_Name)
        print(f"Saved Image: {Save_Name}")
        ##################################################################### ################################################################ ################################################################
        #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################
        ##################################################################### ################################################################ ################################################################
    return Unfolding_Diff_Data_Input

################################################################################################################################################
##### Large/Combined Image Function ############################################################################################################
################################################################################################################################################


to_be_saved_count = 0
if(args.data and (args.unfold not in ["rdf"])):
    print(f"{color.Error}Setting 'unfold' argument to 'rdf' for Data to MC comparison.{color.END}\n")
    args.unfold = "rdf"
if((args.unfold in ["tdf"]) and (args.dimensions in ["3D", "MultiDim_3D_Histo"])):
    args.smearing_option = "''"

ROOT_Input = ROOT.TFile.Open(args.root, "READ")
ROOT_Mod   = None
if(args.mod):
    ROOT_Mod = ROOT.TFile.Open("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Modulated_Response_with_kCovToy.root", "READ")
    
for BIN in Q2_y_Bin_List:
    Q2_y_BIN_NUM       = int(BIN) if(str(BIN) not in ["0"]) else "All"
    if(args.all_z_pt):
        Unfolding_Diff_Data = z_pT_Images_Together_For_Comparisons(ROOT_Input_In=ROOT_Input, ROOT_Mod_In=ROOT_Mod, Unfolding_Diff_Data_Input=Unfolding_Diff_Data, Q2_Y_Bin=Q2_y_BIN_NUM, Plot_Orientation="z_pT")
        to_be_saved_count += 2 if(args.mod or args.sim or args.closure) else 1
        continue
    if(args.z_pt):
        z_pT_Bin_Range = args.z_pt
    else:
        z_pT_Bin_Range = range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_BIN_NUM)[1] + 1)
    for z_PT_BIN_NUM  in z_pT_Bin_Range:
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_BIN_NUM, Z_PT_BIN=z_PT_BIN_NUM, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
            if(args.z_pt):
                print(f"{color.Error}WARNING{color.END_e}: The selected (Q2-y)-(z-pT) Bin ({Q2_y_BIN_NUM}-{z_PT_BIN_NUM}) does not exist...{color.END}")
            continue
        HISTO_NAME = f"\n{color.ERROR}ERROR{color.END}\n"
        if(args.dimensions   in ["1D"]):
            HISTO_NAME = f"(1D)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(phi_t)"
        elif(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
            HISTO_NAME = f"(MultiDim_3D_Histo)_({args.unfold})_(SMEAR={args.smearing_option})_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(MultiDim_z_pT_Bin_Y_bin_phi_t)"

        if(args.data):
            HISTO__mdf = HISTO_NAME.replace(f"({args.unfold})", "(mdf)")
            HISTO_NAME = HISTO_NAME.replace("(SMEAR=Smear)", "(SMEAR='')")
            if(args.mod):
                if((HISTO_NAME in ROOT_Input.GetListOfKeys()) and (HISTO__mdf in ROOT_Mod.GetListOfKeys())):
                    if(args.verbose):
                        print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME}{color.END_G} and {color.END_b}{HISTO__mdf}{color.END}")
                    Saved_Q, Unfolding_Diff_Data = Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME, ROOT_In_2=ROOT_Mod, HISTO_NAME_2=HISTO__mdf, legend_labels=("Experimental Data", "Modulated MC"), output_prefix="Mod_Test_Data_Compare_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_y_BIN_NUM, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data)
                    if(not Saved_Q):
                        continue
                    to_be_saved_count += 1
            elif((HISTO_NAME   in ROOT_Input.GetListOfKeys()) and (HISTO__mdf in ROOT_Input.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME}{color.END_G} and {color.END_b}{HISTO__mdf}{color.END}")
                Saved_Q, Unfolding_Diff_Data = Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME, ROOT_In_2=ROOT_Input, HISTO_NAME_2=HISTO__mdf, legend_labels=("Experimental Data", "Normal MC"), output_prefix="Data_Compare_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_y_BIN_NUM, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data)
                if(not Saved_Q):
                    continue
                to_be_saved_count += 1
        elif(args.mod):
            if((HISTO_NAME in ROOT_Input.GetListOfKeys()) and (HISTO_NAME in ROOT_Mod.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME}{color.END}")
                if(Saving_Q):
                    Saved_Q, Unfolding_Diff_Data = Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME, ROOT_In_2=ROOT_Mod, HISTO_NAME_2=HISTO_NAME, legend_labels=("Unfolded with Normal MC", "Unfolded with Modulated MC"), output_prefix="Mod_Test_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_y_BIN_NUM, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data)
                    if(not Saved_Q):
                        continue
                to_be_saved_count += 1
        elif(args.sim or args.closure):
            HISTO_True     = "ERROR"
            if(args.dimensions   in ["1D"]):
                HISTO_True = f"(1D)_(tdf)_(SMEAR=Smear)_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(phi_t)"
            elif(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
                HISTO_True = f"(MultiDim_3D_Histo)_(tdf)_(SMEAR='')_(Q2_y_Bin_{Q2_y_BIN_NUM})_(z_pT_Bin_{z_PT_BIN_NUM})_(MultiDim_z_pT_Bin_Y_bin_phi_t)"
            if((HISTO_NAME in ROOT_Input.GetListOfKeys()) and (HISTO_True in ROOT_Input.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME}{color.BGREEN} and {color.END_b}{HISTO_True}{color.END}")
                if(Saving_Q):
                    Saved_Q, Unfolding_Diff_Data = Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input, HISTO_NAME_1=HISTO_NAME, ROOT_In_2=ROOT_Input, HISTO_NAME_2=HISTO_True, legend_labels=("Unfolded Synthetic (MC) Data", "True Distribution of Synthetic Data"), output_prefix="Sim_Test_" if(not args.closure) else "Closure_Test_", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_y_BIN_NUM, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data)
                    if(not Saved_Q):
                        continue
                to_be_saved_count += 1
        elif(HISTO_NAME in ROOT_Input.GetListOfKeys()):
            if(args.verbose):
                print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME}{color.END}")
            if(Saving_Q):
                Saved_Q = Save_Histograms_As_Images(ROOT_In=ROOT_Input, HISTO_NAME_In=HISTO_NAME, Format=args.file_format, SAVE=args.save_name, SAVE_prefix="Sim_Test_" if(args.sim) else "Mod_Test_" if(args.mod) else "Closure_Test_" if(args.closure) else "", TITLE=Standard_Histogram_Title_Addition)
                if(not Saved_Q):
                    continue
            to_be_saved_count += 1
        else:
            print(f"\n{color.Error}MISSING: {HISTO_NAME}{color.END}\n")
    if(args.verbose):
        print("")

json_output_name = None
if((args.mod or args.sim) and (not args.data)):
    json_output_name = f"{'Mod_Test' if(args.mod) else 'Sim_Test' if(args.sim) else 'ERROR'}_Unfolding_Bin_Differences{f'_{args.save_name}' if(args.save_name not in ['']) else ''}.json"
    if(Saving_Q and ("ERROR" not in json_output_name)):
        # Save all differences to JSON for later uncertainty mapping
        with open(json_output_name, "w") as json_file:
            json.dump(Unfolding_Diff_Data, json_file, indent=4)
        print(f"\n{color.BBLUE}Saved all bin-by-bin differences to:{color.END_B} {json_output_name}{color.END}\n")
    else:
        print(f"\n{color.BCYAN}Would have saved all bin-by-bin differences to:{color.END_B} {json_output_name}{color.END}\n")


start_time = timer.start_find(return_Q=True)
start_time = start_time.replace("Ran", "Started running")

import time
time.sleep(1)

end_time, total_time, rate_line = timer.stop(count_label="Images", count_value=to_be_saved_count, return_Q=True)

email_body = f"""
The 'Assign_Uncertainties_to_unfolding.py' script has finished running.
{start_time}

{args.email_message}

Ran with the following options:

Input File(s):
    {args.root}
Arguments:
--test                         --> {args.test}
--unfold                       --> {args.unfold}
--dimensions                   --> {args.dimensions}
--smearing_option              --> {args.smearing_option}
--simulation (synthetic data?) --> {args.sim}
--modulation (added to MC?)    --> {args.mod}
--closure (Full Closure Test)  --> {args.closure}
--title  (added title)         --> {args.title}
--save_name                    --> {args.save_name if(args.save_name not in ['']) else None}
--EvGen                        --> {args.EvGen}
--q2_y   (Q2-y Bins)           --> {args.bins}
--z_pt   (z-pT Bins)           --> {args.z_pt}
--all_z_pt                     --> {args.all_z_pt}
--normalize                    --> {args.normalize}
--file_format                  --> {args.file_format}
--verbose                      --> {args.verbose}
"""
if(json_output_name):
    email_body = f"""{email_body}
    
JSON File Output:
    {json_output_name}

"""
else:
    email_body = f"""{email_body}

"""

email_body = f"""{email_body}
{end_time}
{total_time}
{rate_line}
"""

if(args.email):
    send_email(subject="Finished Running the 'Assign_Uncertainties_to_unfolding.py' Code", body=email_body, recipient="richard.capobianco@uconn.edu")
else:
    print(email_body)


print(f"""{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

