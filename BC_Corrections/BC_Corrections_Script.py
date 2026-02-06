#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser(description="Creates BC Corrections from MC GEN Plots.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-t', '--test',
                    action='store_true', 
                    help='Run as test.')

parser.add_argument('-clasdis', '--use_clasdis',
                    action='store_true', 
                    help='Run with clasdis instead of EvGen (assumes that the EvGen weight should be used by default unless this argument is used).')

parser.add_argument('-nb', '--num_sub_bins',
                    default=3,
                    type=int,
                    help="Number of sub-bins used per Q2-y-z-pT bin. Must be a positive, odd number.")

parser.add_argument('-q2y', '-Q2y', '--Q2_y_Bin',
                    default=-1,
                    type=int,
                    choices=[x for x in range(-1, 18) if(x != 0)],
                    help="Selected Q2-y Bin to run. Use '-1' to run all bins.")

parser.add_argument('-zpt', '-zpT', '--z_pT_Bin',
                    default=-1,
                    type=int,
                    help="Selected z-pT Bin (for any given Q2-y Bin) to run. Use '-1' to run all bins. Does not automatically reject incompatible combinations of the '--Q2_y_Bin' and '--z_pT_Bin' options.")

parser.add_argument('-phit', '-phih', '-phi_t', '-phi_h', '--phih_Bin',
                    default=-1,
                    type=int,
                    choices=[x for x in range(-1, 16) if(x != 0)],
                    help="Selected phi_t Bin to run (each bin is given in increments of 15 degrees). Use '-1' to run all bins.")

parser.add_argument('-f', '--file',
                    default="/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new6.inb-EvGen-LUND_EvGen_richcap_GEMC-9729_4.hipo.root",
                    type=str, 
                    help="Path to MC GEN ROOT file used to create the BC corrections. Use EvGen files so that a difference in the modulations is actually observable in the 4D sub-bins.")

parser.add_argument('-sf', '-ff', '--save_format',
                    default=".png",
                    type=str,
                    choices=[".png", ".pdf"],
                    help="Selects the image file format of the images that would be saved by this script when running.")

parser.add_argument('-cdf', '--check_dataframe',
                    action='store_true', 
                    help='Prints full contents of the RDataFrame to see available branches.')

parser.add_argument('-v', '--verbose',
                    action='store_true', 
                    help='Print more information while running.')

args = parser.parse_args()

import ROOT, numpy, re
import traceback
import os

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
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
silence_root_import()
sys.path.remove(script_dir)
del script_dir

if((args.num_sub_bins <= 0) or (args.num_sub_bins%2 == 0)):
    print(f"\n{color.Error}ERROR: Number of sub-bins must a positive, odd number for this script to work properly{color.END}\n")
    sys.exit(0)

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

import math
import array
import copy
import json


import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",  # Styles
                     '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", # Colors
                     '\033[0m': "", # Reset (closes span)
                    }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)



def Canvas_Image_Create(List_of_histograms, Q2_y_Bin=1, z_pT_Bin=1, Q2y_Sbin=1, num_of_subbins=args.num_sub_bins, canvas_w=1400, canvas_h=900, left_frac=0.25, left_top_frac=0.35, pad_margin=0.02, Save_Q=(not args.test), Save_Format=args.save_format):
    # ------------------------------------------------------------------------------------------------
    # Create canvas and do an initial equal divide, then reshape pads to 25%/75%
    # ------------------------------------------------------------------------------------------------
    canvas_name = f"BC_Cor_Image_for_Q2_y_Bin_({Q2_y_Bin}-{Q2y_Sbin})_z_pT_Bin_{z_pT_Bin}"
    canvas = ROOT.TCanvas(canvas_name, canvas_name, canvas_w, canvas_h)
    canvas.Divide(2, 1, 0.0, 0.0)  # equal split first (required by your constraint)

    pad_left  = canvas.cd(1)
    pad_right = canvas.cd(2)

    # Reshape to 25% / 75% (NDC coordinates in the canvas)
    pad_left.SetPad(0.0,      0.0, left_frac, 1.0)
    pad_right.SetPad(left_frac, 0.0, 1.0,      1.0)

    # Optional: margins for nicer spacing
    pad_left.SetLeftMargin(0.15)
    pad_left.SetRightMargin(0.05)
    pad_left.SetTopMargin(0.08)
    pad_left.SetBottomMargin(0.12)

    pad_right.SetLeftMargin(0.10)
    pad_right.SetRightMargin(0.08)
    pad_right.SetTopMargin(0.08)
    pad_right.SetBottomMargin(0.12)

    # ------------------------------------------------------------------------------------------------
    # LEFT pad: divided to create a "top corner image" space
    # Made with 1 column x 2 rows, then resized
    # ------------------------------------------------------------------------------------------------
    pad_left.cd()
    pad_left.Divide(1, 2, 0.0, 0.0)

    pad_left_top    = pad_left.cd(1)
    pad_left_bottom = pad_left.cd(2)

    # Resize the two subpads inside the LEFT pad:
    # Use the pad's own NDC (0..1) coordinates
    if((left_top_frac <= 0.0) or (left_top_frac >= 1.0)):
        left_top_frac = 0.35

    pad_left_top.SetPad(0.0, 1.0 - left_top_frac, 1.0, 1.0)
    pad_left_bottom.SetPad(0.0, 0.0,              1.0, 1.0 - left_top_frac)

    # ------------------------------------------------------------------------------------------------
    # RIGHT pad: divide into an N x N square grid
    # ------------------------------------------------------------------------------------------------
    pad_right.cd()
    if(num_of_subbins < 1):
        num_of_subbins = 1

    pad_right.Divide(num_of_subbins, num_of_subbins, pad_margin, pad_margin)

    # ------------------------------------------------------------------------------------------------
    # Placeholder drawing logic
    # Convention here:
    #   - List_of_histograms[0] goes to left-top pad
    #   - remaining hists fill the right grid pads in order
    # ------------------------------------------------------------------------------------------------

    # Draw the "corner" histogram
    pad_left_top.cd()
    histo_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-0)"
    List_of_histograms[histo_bin_name].Draw("hist")

    # Draw the remaining histograms into the right grid

    for idx in range(1, int((num_of_subbins*num_of_subbins)+1)):
        histo_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-{idx})"
        pad_right.cd(idx)
        List_of_histograms[histo_bin_name].Draw("hist")

    canvas.cd()
    canvas.Update()

    if(Save_Q):
        print(f"{color.BGREEN}Saving Image As: {color.PINK}{canvas_name}{Save_Format}{color.END}")
        canvas.SaveAs(f"{canvas_name}{Save_Format}")
    else:
        print(f"{color.BLUE}Would have saved image as: {color.PINK}{canvas_name}{Save_Format}{color.END}")




################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
from functools import partial
def func_fit(params, x, y):
    A, B, C = params
    y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi))) for xi in x]
    return sum((y_pred[i] - y[i])**2 for i in range(len(x)))

def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
    N = len(x0)
    simplex = [x0]
    for i in range(N):
        point = list(x0)
        point[i] = x0[i] + 1.0
        simplex.append(point)
    for _ in range(max_iter):
        simplex.sort(key=lambda point: func(point, *args))
        if abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol:
            break
        centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
        reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
        if func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args):
            simplex[-1] = reflected
            continue
        if func(reflected, *args) < func(simplex[0], *args):
            expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
            if func(expanded, *args) < func(reflected, *args):
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected
            continue
        contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
        if func(contracted, *args) < func(simplex[-1], *args):
            simplex[-1] = contracted
            continue
        for i in range(1, N+1):
            simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]
    return simplex[0]

def Full_Calc_Fit(Histo):
    # Helping the closure tests with known values of B and C
    x_data, y_data = [], []
    try:
        for ii in range(0, Histo.GetNbinsX(), 1):
            x_data.append(Histo.GetBinCenter(ii))
            y_data.append(Histo.GetBinContent(ii))
        # Perform optimization using the Nelder-Mead method
        initial_guess = [1e6, 1, 1]  # Initial guess for A, B, C
        optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)
        # Extract the optimized parameters
        A_opt, B_opt, C_opt = optim_params
    except:
        print(f"{color.Error}Full_Calc_Fit(...) ERROR:\n{color.END}{traceback.format_exc()}\n")
        print(f"\n{color.Error}ERROR is with 'Histo'= {Histo}\n{color.END}")
        A_opt, B_opt, C_opt = "Error", "Error", "Error"
    return [A_opt, B_opt, C_opt]

def Fitting_Phi_Function(Histo_To_Fit, Method="gdf", Fitting="default", Special="Normal", Fit_Test=True):
    if((Method in ["RC"]) and (Fit_Test)):
        try:
            Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
            Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit.GetName()}_{Method}", fit_function, 0, 360)
            RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=Q2_y_Bin_Special, z_pT_bin=z_pT_Bin_Special, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
            Fitting_Function.SetParameter(0, RC_Par_A)
            Fitting_Function.SetParLimits(0, RC_Par_A - 2*abs(RC_Err_A), RC_Par_A + 2*abs(RC_Err_A))
            Fitting_Function.SetParameter(1, RC_Par_B)
            Fitting_Function.SetParLimits(1, RC_Par_B - 2*abs(RC_Err_B), RC_Par_B + 2*abs(RC_Err_B))
            Fitting_Function.SetParameter(2, RC_Par_C)
            Fitting_Function.SetParLimits(2, RC_Par_C - 2*abs(RC_Err_C), RC_Par_C + 2*abs(RC_Err_C))
            Fitting_Function.SetParName(0, "A")
            Fitting_Function.SetParName(1, "B")
            Fitting_Function.SetParName(2, "C")
            Histo_To_Fit.Fit(Fitting_Function, "QRB")
            A_Unfold       = Fitting_Function.GetParameter(0)
            B_Unfold       = Fitting_Function.GetParameter(1)
            C_Unfold       = Fitting_Function.GetParameter(2)
            A_Unfold_Error = Fitting_Function.GetParError(0)
            B_Unfold_Error = Fitting_Function.GetParError(1)
            C_Unfold_Error = Fitting_Function.GetParError(2)
            try:
                Fit_Chisquared = Fitting_Function.GetChisquare()
                Fit_ndf        = Fitting_Function.GetNDF()
            except:
                Fit_Chisquared = "Fit_Chisquared"
                Fit_ndf        = "Fit_ndf"
            Out_Put = [Histo_To_Fit,  Fitting_Function,   [Fit_Chisquared,    Fit_ndf],  [A_Unfold,    A_Unfold_Error],  [B_Unfold,    B_Unfold_Error],  [C_Unfold,    C_Unfold_Error]]
        except:
            print(f"{color.Error}ERROR IN FITTING:\n{color.END}{str(traceback.format_exc())}\n")
            Out_Put = [Histo_To_Fit, "Fitting_Function",  ["Fit_Chisquared", "Fit_ndf"], ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        return Out_Put
    elif((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true", "RC_Bin", "RC_Bayesian"]) and (Fitting in ["default", "Default"]) and (Fit_Test)):
        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
        fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"

        Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit.GetName()}_{str(Method).replace(' ', '_')}", str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")

        fit_range_lower = 0
        fit_range_upper = 360
        n_bins = Histo_To_Fit.GetNbinsX()
        
        # Find the lower fit range (first non-empty bin)
        for bin_lower in range(1, n_bins // 2 + 1):  # Search from the start to the center
            if(Histo_To_Fit.GetBinContent(bin_lower) != 0):
                fit_range_lower = Histo_To_Fit.GetXaxis().GetBinLowEdge(bin_lower)
                break  # Stop the loop once the first non-empty bin is found

        # Find the upper fit range (last non-empty bin)
        for bin_upper in range(n_bins, n_bins // 2, -1):  # Search from the end towards the center
            if(Histo_To_Fit.GetBinContent(bin_upper) != 0):
                fit_range_upper = Histo_To_Fit.GetXaxis().GetBinUpEdge(bin_upper)
                break  # Stop the loop once the last non-empty bin is found
        
        Fitting_Function.SetRange(fit_range_lower, fit_range_upper)
        
        Fitting_Function.SetLineColor(2)
        if(Special in ["Normal"]):
            if(Method in ["rdf", "Experimental"]):
                Fitting_Function.SetLineColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Fitting_Function.SetLineColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Fitting_Function.SetLineColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Fitting_Function.SetLineColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Fitting_Function.SetLineColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian", "bay"]):
                Fitting_Function.SetLineColor(root_color.Teal)
            if(Method in ["RC_Bin"]):
                Fitting_Function.SetLineColor(ROOT.kOrange + 4)
            if(Method in ["RC_Bayesian"]):
                Fitting_Function.SetLineColor(ROOT.kViolet - 8)
            if(Method in ["SVD"]):
                Fitting_Function.SetLineColor(root_color.Pink)
        
        Allow_Multiple_Fits   = True
        Allow_Multiple_Fits_C = True

        try:
            if("Error" not in [A_Unfold, B_Unfold, C_Unfold]):
                # This is the constant scaling factor - A (should basically always be positive)
                Fitting_Function.SetParameter(0,      abs(A_Unfold))
                Fitting_Function.SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))

                if((Special not in ["Normal"]) and isinstance(Special, list)):
                    try:
                        Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
                        if(len(Special) > 2):
                            Sector_Special = str(Special[2])
                        else:
                            Sector_Special = "N/A"
                        if(str(z_pT_Bin_Special) in ["All", "0"]):
                            print(f"\n\n{color.BBLUE}z_pT_Bin_Special = {z_pT_Bin_Special}{color.END}\n\n\n")
                        if(str(z_pT_Bin_Special) in ["Integrated", "All", "-1", "0"]):
                            if(Sector_Special not in ["N/A"]):
                                if((Q2_y_Bin_Special, z_pT_Bin_Special, "Sectors", "Trusted") in special_fit_parameters_set):
                                    bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "Sectors", "Trusted")]
                                    print(f"\n{color.Error}Using Sector Fit Ranges\n{color.END}")
                                    fit_range_lower = bin_ranges.get("fit_range_lower")
                                    fit_range_upper = bin_ranges.get("fit_range_upper")
                                elif((Q2_y_Bin_Special, "All", "Sectors", "Trusted") in special_fit_parameters_set):
                                    bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, "All", "Sectors", "Trusted")]
                                    print(f"\n{color.Error}Using Sector Fit Ranges\n{color.END}")
                                    fit_range_lower = bin_ranges.get("fit_range_lower")
                                    fit_range_upper = bin_ranges.get("fit_range_upper")
                            elif((Q2_y_Bin_Special, z_pT_Bin_Special, "Trusted") in special_fit_parameters_set):
                                bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "Trusted")]
                                fit_range_lower = bin_ranges.get("fit_range_lower")
                                fit_range_upper = bin_ranges.get("fit_range_upper")
                            elif((Q2_y_Bin_Special, "All", "Trusted") in special_fit_parameters_set):
                                bin_ranges = special_fit_parameters_set[(Q2_y_Bin_Special, "All", "Trusted")]
                                fit_range_lower = bin_ranges.get("fit_range_lower")
                                fit_range_upper = bin_ranges.get("fit_range_upper")
                            else:
                                fit_range_lower =  45 if(str(Q2_y_Bin_Special) in ["1", "5"]) else  30 if(str(Q2_y_Bin_Special) in ["2", "3", "6", "9", "10", "13", "16"]) else  15
                                fit_range_upper = 315 if(str(Q2_y_Bin_Special) in ["1", "5"]) else 330 if(str(Q2_y_Bin_Special) in ["2", "3", "6", "9", "10", "13", "16"]) else 345
                            Fitting_Function.SetRange(fit_range_lower, fit_range_upper)
                        if((z_pT_Bin_Special in ["Integrated", "-1"]) and not ((Q2_y_Bin_Special, z_pT_Bin_Special) in special_fit_parameters_set)):
                            if((Q2_y_Bin_Special, "All") in special_fit_parameters_set):
                                bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, "All")]
                                if(bin_settings.get("B_initial") is not None):
                                    Fitting_Function.SetParameter(1, bin_settings["B_initial"])
                                    if(bin_settings.get("B_limits")):
                                        Fitting_Function.SetParLimits(1, *sorted(bin_settings["B_limits"]))
                                if(bin_settings.get("C_initial") is not None):
                                    Fitting_Function.SetParameter(2, bin_settings["C_initial"])
                                    if(bin_settings.get("C_limits")):
                                        Fitting_Function.SetParLimits(2, *sorted(bin_settings["C_limits"]))
                                Allow_Multiple_Fits   = bin_settings.get("Allow_Multiple_Fits",   True)
                                Allow_Multiple_Fits_C = bin_settings.get("Allow_Multiple_Fits_C", True)
                            else:
                                Par_initial_B = -0.05 if(str(Q2_y_Bin_Special) in ["12"]) else -0.1   if(str(Q2_y_Bin_Special) in ["8", "15"]) else -0.12 if(str(Q2_y_Bin_Special) in ["4", "11", "17"]) else -0.14  if(str(Q2_y_Bin_Special) in ["7", "16"]) else -0.155 if(str(Q2_y_Bin_Special) in ["3",  "6", "13", "14"]) else -0.1625 if(str(Q2_y_Bin_Special) in ["12"]) else -0.174
                                Par_initial_C = -0.05 if(str(Q2_y_Bin_Special) in ["8"])  else -0.075 if(str(Q2_y_Bin_Special) in ["12"])      else -0.04 if(str(Q2_y_Bin_Special) in ["4", "15"])       else -0.029 if(str(Q2_y_Bin_Special) in ["11"])      else -0.021 if(str(Q2_y_Bin_Special) in ["7", "14", "16", "17"]) else -0.01   if(str(Q2_y_Bin_Special) in ["10"]) else -0.006 if(str(Q2_y_Bin_Special) in ["3", "6", "13"]) else 0.0045 if(str(Q2_y_Bin_Special) in ["2"]) else 0.0067 if(str(Q2_y_Bin_Special) in ["9"]) else 0.009
                                Par__range__B = [0.5*Par_initial_B, 1.5*Par_initial_B]
                                Par__range__C = [0.5*Par_initial_C, 1.5*Par_initial_C]
                                # Cos(phi) Moment - B
                                Fitting_Function.SetParameter(1, Par_initial_B)
                                Fitting_Function.SetParLimits(1, min(Par__range__B), max(Par__range__B))
                                # Cos(2*phi) Moment - C
                                Fitting_Function.SetParameter(2, Par_initial_C)
                                Fitting_Function.SetParLimits(2, min(Par__range__C), max(Par__range__C))
                        elif((Q2_y_Bin_Special, z_pT_Bin_Special) in special_fit_parameters_set):
                                if(("RC_" in Method) and ((Q2_y_Bin_Special, z_pT_Bin_Special, "RC") in special_fit_parameters_set)):
                                    print(f"\n{color.BCYAN}Using RC Initial Fit Configs for Bin ({Q2_y_Bin_Special}-{z_pT_Bin_Special}){color.END}\n")
                                    bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "RC")]
                                else:
                                    bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special)]
                                if(bin_settings.get("B_initial") is not None):
                                    Fitting_Function.SetParameter(1, bin_settings["B_initial"])
                                    if(bin_settings.get("B_limits")):
                                        Fitting_Function.SetParLimits(1, *sorted(bin_settings["B_limits"]))
                                if(bin_settings.get("C_initial") is not None):
                                    Fitting_Function.SetParameter(2, bin_settings["C_initial"])
                                    if(bin_settings.get("C_limits")):
                                        Fitting_Function.SetParLimits(2, *sorted(bin_settings["C_limits"]))
                                Allow_Multiple_Fits   = bin_settings.get("Allow_Multiple_Fits",   True)
                                Allow_Multiple_Fits_C = bin_settings.get("Allow_Multiple_Fits_C", True)                        
                    except:
                        print(f"{color.Error}\nERROR in Fitting_Phi_Function() for 'Special' arguement...{color.END_B}\nTraceback:\n{str(traceback.format_exc())}{color.END}\n")
                # else:
                #     print(f"\n\n\n{color.RED}Fitting_Phi_Function Not Special{color.END}\n\n\n")
                Histo_To_Fit.Fit(Fitting_Function, "QRB")
            else:
                # print(f"{color.RED}Error in A_Unfold, B_Unfold, C_Unfold = {A_Unfold}, {B_Unfold}, {C_Unfold}{color.END}")
                Histo_To_Fit.Fit(Fitting_Function, "QR")

            A_Unfold = Fitting_Function.GetParameter(0)
            B_Unfold = Fitting_Function.GetParameter(1)
            C_Unfold = Fitting_Function.GetParameter(2)
            
            # Re-fitting with the new parameters
            # The constant scaling factor - A
            Fitting_Function.SetParameter(0,     abs(A_Unfold))
            Fitting_Function.SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
            
            if(Allow_Multiple_Fits): # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
            else:                    # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - Fitting_Function.GetParError(1), B_Unfold + Fitting_Function.GetParError(1))
                
            if(Allow_Multiple_Fits_C): # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))
            else:                      # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - Fitting_Function.GetParError(2), C_Unfold + Fitting_Function.GetParError(2))

            # Re-Fitting the plots
            Histo_To_Fit.Fit(Fitting_Function, "QRB")

            A_Unfold       = Fitting_Function.GetParameter(0)
            B_Unfold       = Fitting_Function.GetParameter(1)
            C_Unfold       = Fitting_Function.GetParameter(2)

            A_Unfold_Error = Fitting_Function.GetParError(0)
            B_Unfold_Error = Fitting_Function.GetParError(1)
            C_Unfold_Error = Fitting_Function.GetParError(2)
            
            try:
                Fit_Chisquared = Fitting_Function.GetChisquare()
                Fit_ndf        = Fitting_Function.GetNDF()
            except:
                Fit_Chisquared = "Fit_Chisquared"
                Fit_ndf        = "Fit_ndf"

            Out_Put = [Histo_To_Fit,  Fitting_Function,   [Fit_Chisquared,    Fit_ndf],  [A_Unfold,    A_Unfold_Error],  [B_Unfold,    B_Unfold_Error],  [C_Unfold,    C_Unfold_Error]]
        except:
            print(f"{color.Error}ERROR IN FITTING:\n{color.END}{str(traceback.format_exc())}\n")
            Out_Put = [Histo_To_Fit, "Fitting_Function",  ["Fit_Chisquared", "Fit_ndf"], ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        return Out_Put
    else:
        print(f"\n\n\n{color.Error}ERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...\n\n\n{color.END}")
        return "ERROR"
    
################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################






























print(f"\n{color.BBLUE}Ready to Run BC Correction Script...{color.END}\n")
timer = RuntimeTimer()
timer.start()

if(args.test):
    print(f"\t{color.Error}Running as a test of the script...{color.END}\n")


print(f"\n{color.BBLUE}Running with File: {color.BPINK}{args.file.split('/')[-1]}{color.END}\n")

gdf = ROOT.RDataFrame("h22", str(args.file))

if(any(var not in gdf.GetColumnNames() for var in ["Q2", "y", "z", "pT", "phi_t"])):
    print(f"{color.ERROR}WARNING{color.END}{color.Error}:{color.END_B} ROOT file is missing the kinematic variables.{color.END}\n")
    ROOT.gInterpreter.Declare(Rotation_Matrix)
    gdf = gdf.Define("vals", """
    
    auto beam    = ROOT::Math::PxPyPzMVector(0, 0, 10.6, 0);
    auto targ    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
    
    auto ele     = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
    auto pip0    = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

    auto epipX   = beam + targ - ele - pip0;
    auto q       = beam - ele;
    auto Q2      = -q.M2();
    auto v       = beam.E() - ele.E();
    auto xB      = Q2/(2*targ.M()*v);
    auto W2      = targ.M2() + 2*targ.M()*v - Q2;
    auto W       = sqrt(W2);
    auto y       = (targ.Dot(q))/(targ.Dot(beam));
    auto z       = ((pip0.E())/(q.E()));
    auto gamma   = 2*targ.M()*(xB/sqrt(Q2));
    auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));
    
    std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};

    return vals;""")
    
    gdf = gdf.Define('MM',  'vals[0]') # Missing Mass
    gdf = gdf.Define('MM2', 'vals[1]') # Missing Mass Squared 
    gdf = gdf.Define('Q2',  'vals[2]') # lepton momentum transfer squared
    gdf = gdf.Define('xB',  'vals[3]') # fraction of the proton momentum that is carried by the struck quark
    # gdf = gdf.Define('v',   'vals[4]') # energy of the virtual photon
    # gdf = gdf.Define('s',   'vals[5]') # center-of-mass energy squared
    gdf = gdf.Define('W',   'vals[6]') # center-of-mass energy
    gdf = gdf.Define('y',   'vals[7]') # energy fraction of the incoming lepton carried by the virtual photon
    gdf = gdf.Define('z',   'vals[8]') # energy fraction of the virtual photon carried by the outgoing hadron
    # gdf = gdf.Define('epsilon', 'vals[9]') # ratio of the longitudinal and transverse photon flux

    gdf = gdf.Define("vals2", """    
    auto beamM  = ROOT::Math::PxPyPzMVector(0, 0, 10.6, 0);
    auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
    
    auto eleM   = ROOT::Math::PxPyPzMVector(ex,     ey,   ez,       0);
    auto pip0M  = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
    
    auto lv_qMM = beamM - eleM;

    TLorentzVector beam(0, 0, 10.6, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());
    
    TLorentzVector ele(ex,      ey,   ez,  eleM.E());
    TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
    
    TLorentzVector lv_q = beam - ele;

    ///////////////     Angles for Rotation     ///////////////
    double Theta_q = lv_q.Theta();
    double Phi_el  = ele.Phi();

    ///////////////     Rotating to CM Frame     ///////////////

    auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
    auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
    auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
    auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
    auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);

    ///////////////     Saving CM components     ///////////////

    double pipx_1 = pip0_Clone.X();
    double pipy_1 = pip0_Clone.Y();
    double pipz_1 = pip0_Clone.Z();

    double qx = lv_q_Clone.X();
    double qy = lv_q_Clone.Y();
    double qz = lv_q_Clone.Z();

    double beamx = beam_Clone.X();
    double beamy = beam_Clone.Y();
    double beamz = beam_Clone.Z();

    double elex = ele_Clone.X();
    double eley = ele_Clone.Y();
    double elez = ele_Clone.Z();

    ///////////////     Boosting Vectors     ///////////////

    auto fCM   = lv_q_Clone + targ_Clone;
    auto boost = -(fCM.BoostVector());

    auto qlv_Boost(lv_q_Clone);
    auto ele_Boost(ele_Clone);
    auto pip_Boost(pip0_Clone);
    auto beamBoost(beam_Clone);
    auto targBoost(targ_Clone);

    qlv_Boost.Boost(boost);
    ele_Boost.Boost(boost);
    pip_Boost.Boost(boost);
    beamBoost.Boost(boost);
    targBoost.Boost(boost);

    TVector3 v0, v1;
    v0 = qlv_Boost.Vect().Cross(ele_Boost.Vect());
    v1 = qlv_Boost.Vect().Cross(pip_Boost.Vect());
    Double_t c0, c1, c2, c3;
    c0 = v0.Dot(pip_Boost.Vect());
    c1 = v0.Dot(v1);
    c2 = v0.Mag();
    c3 = v1.Mag();

    // Phi Trento (using Stefan's equation)
    double phi_t_cross_product = (c0/TMath::Abs(c0)) * TMath::ACos(c1 /(c2*c3));
    
    double Cos_theta_t = (pip0.Vect().Dot(lv_q.Vect()))/(pip0.Vect().Mag()*lv_q.Vect().Mag());
    double theta_t = TMath::ACos(Cos_theta_t);

    double pipTx = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTy = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTz = pip0.P()*TMath::Cos(theta_t);

    TVector3 pipT(pipTx, pipTy, pipTz);

    phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();
    
    ///////////////   x Feynmann   ///////////////
    double xF = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);

    // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
    double pT = sqrt(pipx_1*pipx_1 + pipy_1*pipy_1);
    double phi_t = pip0_Clone.Phi()*TMath::RadToDeg();

    if(phi_t < 0){phi_t += 360;}

    std::vector<double> vals2 = {pT, phi_t, xF};

    return vals2;""")

    gdf = gdf.Define('pT',    'vals2[0]')    # transverse momentum of the final state hadron
    gdf = gdf.Define('phi_t', 'vals2[1]')    # Most important angle (between lepton and hadron planes)
    gdf = gdf.Define('xF',    'vals2[2]')    # x Feynmann



    def Q2_xB_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin"):
        if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
            print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function Q2_xB_Bin_Standard_Def_Function(Variable_Type).\nFix input to use anything other than the default calculations of Q2 and xB.")
            Variable_Type  = ""
            
        Q2_For_Binning = "smeared_vals[2]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "".join(["Q2", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        y_For_Binning  = "smeared_vals[7]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "".join(["y",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
    
        Q2_xB_Bin_Def = "".join(["""
            int Q2_Y_Bin_New = 0;
            // Q2-y Bins 1-4:
            if(""",     str(Q2_For_Binning), " > 2.0 && ", str(Q2_For_Binning), """ < 2.4){
                // Bin 1
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 1;
                    return Q2_Y_Bin_New;
                }
                // Bin 2
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 2;
                    return Q2_Y_Bin_New;
                }
                // Bin 3
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 3;
                    return Q2_Y_Bin_New;
                }
                // Bin 4
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 4;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 5-8:
            if(""",     str(Q2_For_Binning), " > 2.4 && ", str(Q2_For_Binning), """ < 2.9){
                // Bin 5
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 5;
                    return Q2_Y_Bin_New;
                }
                // Bin 6
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 6;
                    return Q2_Y_Bin_New;
                }
                // Bin 7
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 7;
                    return Q2_Y_Bin_New;
                }
                // Bin 8
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 8;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 9-12:
            if(""",     str(Q2_For_Binning), " > 2.9 && ", str(Q2_For_Binning), """ < 3.7){
                // Bin 9
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 9;
                    return Q2_Y_Bin_New;
                }
                // Bin 10
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 10;
                    return Q2_Y_Bin_New;
                }
                // Bin 11
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 11;
                    return Q2_Y_Bin_New;
                }
                // Bin 12
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 12;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 13-15:
            if(""",     str(Q2_For_Binning), " > 3.7 && ", str(Q2_For_Binning), """ < 5.3){
                // Bin 13
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 13;
                    return Q2_Y_Bin_New;
                }
                // Bin 14
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 14;
                    return Q2_Y_Bin_New;
                }
                // Bin 15
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 15;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 16-17:
            if(""",     str(Q2_For_Binning), " > 5.3 && ", str(Q2_For_Binning), """ < 7.9){
                // Bin 16
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 16;
                    return Q2_Y_Bin_New;
                }
                // Bin 17
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 17;
                    return Q2_Y_Bin_New;
                }
            }
    
            //=====//================//=====//======================================================//
            //=====// Migration Bins //=====//======================================================//
            //=====//================//=====//======================================================//
    
            // Q2-y Bins 18-23:
            if(""",     str(Q2_For_Binning), " > 0.0 && ", str(Q2_For_Binning), """ < 2.0){
                // Bin 18
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 18;
                    return Q2_Y_Bin_New;
                }
                // Bin 19
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 19;
                    return Q2_Y_Bin_New;
                }
                // Bin 20
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 20;
                    return Q2_Y_Bin_New;
                }
                // Bin 21
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 21;
                    return Q2_Y_Bin_New;
                }
                // Bin 22
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 22;
                    return Q2_Y_Bin_New;
                }
                // Bin 23
                if(""", str(y_For_Binning),  " > 0.1 && ", str(y_For_Binning), """ < 0.35){
                    Q2_Y_Bin_New = 23;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 24-25:
            if(""",     str(Q2_For_Binning), " > 2.0 && ", str(Q2_For_Binning), """ < 2.4){
                // Bin 24
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 24;
                    return Q2_Y_Bin_New;
                }
                // Bin 25
                if(""", str(y_For_Binning),  " > 0.1 && ", str(y_For_Binning), """ < 0.35){
                    Q2_Y_Bin_New = 25;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 26-27:
            if(""",     str(Q2_For_Binning), " > 2.4 && ", str(Q2_For_Binning), """ < 2.9){
                // Bin 26
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 26;
                    return Q2_Y_Bin_New;
                }
                // Bin 27
                if(""", str(y_For_Binning),  " > 0.1 && ", str(y_For_Binning), """ < 0.35){
                    Q2_Y_Bin_New = 27;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 28-29:
            if(""",     str(Q2_For_Binning), " > 2.9 && ", str(Q2_For_Binning), """ < 3.7){
                // Bin 28
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 28;
                    return Q2_Y_Bin_New;
                }
                // Bin 29
                if(""", str(y_For_Binning),  " > 0.1 && ", str(y_For_Binning), """ < 0.35){
                    Q2_Y_Bin_New = 29;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 30-32:
            if(""",     str(Q2_For_Binning), " > 3.7 && ", str(Q2_For_Binning), """ < 5.3){
                // Bin 30
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 30;
                    return Q2_Y_Bin_New;
                }
                // Bin 31
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 31;
                    return Q2_Y_Bin_New;
                }
                // Bin 32
                if(""", str(y_For_Binning),  " > 0.1 && ", str(y_For_Binning), """ < 0.35){
                    Q2_Y_Bin_New = 32;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 33-35:
            if(""",     str(Q2_For_Binning), " > 5.3 && ", str(Q2_For_Binning), """ < 7.9){
                // Bin 33
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 33;
                    return Q2_Y_Bin_New;
                }
                // Bin 34
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 34;
                    return Q2_Y_Bin_New;
                }
                // Bin 35
                if(""", str(y_For_Binning),  " > 0.35 && ", str(y_For_Binning), """ < 0.45){
                    Q2_Y_Bin_New = 35;
                    return Q2_Y_Bin_New;
                }
            }
            // Q2-y Bins 36-39:
            if(""",     str(Q2_For_Binning), " > 7.9 && ", str(Q2_For_Binning), """ < 14.0){
                // Bin 36
                if(""", str(y_For_Binning),  " > 0.75 && ", str(y_For_Binning), """ < 0.99){
                    Q2_Y_Bin_New = 36;
                    return Q2_Y_Bin_New;
                }
                // Bin 37
                if(""", str(y_For_Binning),  " > 0.65 && ", str(y_For_Binning), """ < 0.75){
                    Q2_Y_Bin_New = 37;
                    return Q2_Y_Bin_New;
                }
                // Bin 38
                if(""", str(y_For_Binning),  " > 0.55 && ", str(y_For_Binning), """ < 0.65){
                    Q2_Y_Bin_New = 38;
                    return Q2_Y_Bin_New;
                }
                // Bin 39
                if(""", str(y_For_Binning),  " > 0.45 && ", str(y_For_Binning), """ < 0.55){
                    Q2_Y_Bin_New = 39;
                    return Q2_Y_Bin_New;
                }
            }
    
            //=====//================//=====//======================================================//
            //=====// Migration Bins //=====//======================================================//
            //=====//================//=====//======================================================//
    
    
            return Q2_Y_Bin_New;"""])
    
        return Q2_xB_Bin_Def
        
        
        
        
    ##########################################################################################################################################################################################
    ##########################################################################################################################################################################################
        
        
    def z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="Y_bin"):
        if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
            print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function z_pT_Bin_Standard_Def_Function(Variable_Type='{Variable_Type}', Bin_Version='{Bin_Version}').\nFix input to use anything other than the default calculations of z and pT.")
            Variable_Type  = ""
            
        Q2_xB_Bin_event_name = "".join(["Q2_xB_Bin" if(Bin_Version not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q2_y_Bin" if(("y_" in Bin_Version) or (Bin_Version == "4")) else "Q2_Y_Bin", "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in ["", "4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        z_pT_Bin_event_name  = "".join(["z_pT_Bin",                                                                                                                                                          "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in [""])                                               else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
    
        z_pT_Bin_Standard_Def = "".join([str(New_z_pT_and_MultiDim_Binning_Code), """
            double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
            double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
            int z_pT_Bin_event_val = 0;
            int Phih_Bin_event_val = 0;
            int MultiDim3D_Bin_val = 0;
            int MultiDim5D_Bin_val = 0;
            if(""", Q2_xB_Bin_event_name, """ != 0){
                z_pT_Bin_event_val = Find_z_pT_Bin(""",           str(Q2_xB_Bin_event_name), """, z_event_val, pT_event_val);
                if(z_pT_Bin_event_val == 0){
                    MultiDim3D_Bin_val = 0;
                    MultiDim5D_Bin_val = 0;
                }
                else{
                    if(Phi_h_Bin_Values[""",                      str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][0] == 1){Phih_Bin_event_val = 1;}
                    else{Phih_Bin_event_val = Find_phi_h_Bin(""", str(Q2_xB_Bin_event_name), """, z_pT_Bin_event_val, """, "smeared_vals[11]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "phi_t", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """);}
                    MultiDim3D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][1] + Phih_Bin_event_val;
                    MultiDim5D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][2] + Phih_Bin_event_val;
                }
            }
            else{
                z_pT_Bin_event_val = 0;
                MultiDim3D_Bin_val = 0;
                MultiDim5D_Bin_val = 0;
            }
            """, f"""
            // Refinement of Migration/Overflow Bins
            if((({Q2_xB_Bin_event_name} == 1) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 2) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 3) && ((z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 4) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 5) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 6) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 7) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 8) && ((z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 9) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 10) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 11) && ((z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 12) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 13) && ((z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 14) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 15) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 16) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 23) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 17) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30)))){{
                z_pT_Bin_event_val = 0;
                MultiDim3D_Bin_val = 0;
                MultiDim5D_Bin_val = 0;
            }}
            std::vector<int> z_pT_and_MultiDim_Bins = {{z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val}};
            return z_pT_and_MultiDim_Bins;"""])
        
        return z_pT_Bin_Standard_Def
        
    gdf = gdf.Define("Q2_Y_Bin",                                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Y_bin")))
    gdf = gdf.Define("All_MultiDim_Y_bin",                                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Y_bin")))
    gdf = gdf.Define("z_pT_Bin_Y_bin",                                          "All_MultiDim_Y_bin[0]")
    # gdf = gdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t",                           "All_MultiDim_Y_bin[1]")
    # if(Use_5D_Response_Matrix):
    #     gdf = gdf.Define("MultiDim_Q2_y_z_pT_phi_h",                            "All_MultiDim_Y_bin[2]")


print(f"\n{color.BGREEN}Creating New Sub-bins... {color.END_B}({color.ERROR}{args.num_sub_bins}{color.END_B} per variable){color.END}\n")

Find_Q2_y_Bin_Ranges = """
double q2min=0., q2max=0., ymin=0., ymax=0.;

// --- Q2 range from bin ---
if      (Q2_Y_Bin>= 1 && Q2_Y_Bin<= 4)  { q2min=2.0; q2max=2.4; }
else if (Q2_Y_Bin>= 5 && Q2_Y_Bin<= 8)  { q2min=2.4; q2max=2.9; }
else if (Q2_Y_Bin>= 9 && Q2_Y_Bin<=12)  { q2min=2.9; q2max=3.7; }
else if (Q2_Y_Bin>=13 && Q2_Y_Bin<=15)  { q2min=3.7; q2max=5.3; }
else if (Q2_Y_Bin>=16 && Q2_Y_Bin<=17)  { q2min=5.3; q2max=7.9; }

// --- y range from bin ---
if      (Q2_Y_Bin == 1 || Q2_Y_Bin == 5 || Q2_Y_Bin == 9  || Q2_Y_Bin ==13 || Q2_Y_Bin ==16) { ymin=0.65; ymax=0.75; }
else if (Q2_Y_Bin == 2 || Q2_Y_Bin == 6 || Q2_Y_Bin ==10  || Q2_Y_Bin ==14 || Q2_Y_Bin ==17) { ymin=0.55; ymax=0.65; }
else if (Q2_Y_Bin == 3 || Q2_Y_Bin == 7 || Q2_Y_Bin ==11  || Q2_Y_Bin ==15)                  { ymin=0.45; ymax=0.55; }
else if (Q2_Y_Bin == 4 || Q2_Y_Bin == 8 || Q2_Y_Bin ==12)                                    { ymin=0.35; ymax=0.45; }

"""

gdf = gdf.Define("Q2_y_SUB_BINs", f"""{Find_Q2_y_Bin_Ranges}

double delta_Q2 = ((q2max - q2min)/{args.num_sub_bins});
double delta_y  = ((ymax  -  ymin)/{args.num_sub_bins});

int Q2_y_subbin = 0;
for(double Q2_subbin = q2max; Q2_subbin > q2min; Q2_subbin = Q2_subbin - delta_Q2){{
    if((Q2 <= Q2_subbin) && (Q2 >= (Q2_subbin-delta_Q2))){{
        for(int y_subbin = 0; y_subbin < {args.num_sub_bins}; y_subbin++){{
            Q2_y_subbin = Q2_y_subbin + 1;
            if((y >= ymin+(y_subbin*delta_y)) && (y <= ymin+((y_subbin+1)*delta_y))){{
                return Q2_y_subbin;
            }}
        }}
    }}
    else {{ Q2_y_subbin = Q2_y_subbin + {args.num_sub_bins}; }}
}}

return -1; // Error (Should have returned already...)

""")

gdf = gdf.Define("z_pT_SUB_BINs", f"""{New_z_pT_and_MultiDim_Binning_Code}
// From New_z_pT_and_MultiDim_Binning_Code:
   // z_pT_Bin_Borders[Q2_y_Bin][z_pT_Bin][Border_Num]
    // Border_Num = 0 -> z_max
    // Border_Num = 1 -> z_min
    // Border_Num = 2 -> pT_max
    // Border_Num = 3 -> pT_min
    // (Total of 17 Q2-y bins with defined z-pT borders)

double z_max=0., z_min=0., pT_max=0., pT_min=0.;

z_max  = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][0];
z_min  = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][1];
pT_max = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][2];
pT_min = z_pT_Bin_Borders[Q2_Y_Bin][z_pT_Bin_Y_bin][3];

double delta_z  = ((z_max  -  z_min)/{args.num_sub_bins});
double delta_pT = ((pT_max - pT_min)/{args.num_sub_bins});

int z_pT_subbin = 0;
for(double z_subbin = z_max; z_subbin > z_min; z_subbin = z_subbin - delta_z){{
    if((z <= z_subbin) && (z >= (z_subbin-delta_z))){{
        for(int pT_subbin = 0; pT_subbin < {args.num_sub_bins}; pT_subbin++){{
            z_pT_subbin = z_pT_subbin + 1;
            if((pT >= pT_min+(pT_subbin*delta_pT)) && (pT <= pT_min+((pT_subbin+1)*delta_pT))){{
                return z_pT_subbin;
            }}
        }}
    }}
    else {{ z_pT_subbin = z_pT_subbin + {args.num_sub_bins}; }}
}}

return -1; // Error (Should have returned already...)

""")


gdf = gdf.Define("phi_t_bin", """
if(phi_t < 360){ return int(phi_t/15) + 1; }
else { return 1; }
""")

delta_phi_Sbin = float(15.0/float(args.num_sub_bins))
gdf = gdf.Define("phi_t_SUB_BINs", f" int((phi_t - 15*(phi_t_bin - 1))/{delta_phi_Sbin}) + 1 ")

if("Event_Weight" in gdf.GetColumnNames()):
    print(f"\n{color.Error}WARNING: 'Event_Weight' is already defined in the RDataFrame...{color.END}\n")
elif(not args.use_clasdis):
    gdf = gdf.Define("Event_Weight", "weight")
else:
    gdf = gdf.Define("Event_Weight", "1.0")


if(args.check_dataframe):
    print(f"\n{color.BOLD}Print all (currently) defined content of the RDataFrame:{color.END}")
    for num, ii in enumerate(gdf.GetColumnNames()):
        print(f"{num:>3.0f}) {str(ii).ljust(38)} (type -> {gdf.GetColumnType(ii)})")
    print(f"\tTotal length= {len(gdf.GetColumnNames())}\n\n")


def Evaluate_Weights(List_of_BCBins_In, SumOfWeights_L_In, Full_Run__List_In, Run_As_Test=args.test, verbose=args.verbose):
    if(not Run_As_Test):
        print(f"{color.BCYAN}Triggering Event Evaluation on {color.END_B}{len(Full_Run__List_In)}{color.BCYAN} Sub-Bins...{color.END}\n")
        # One trigger for everything
        ROOT.RDF.RunGraphs(Full_Run__List_In)
        for (nom_name, sub_name), ptr in SumOfWeights_L_In.items():
            List_of_BCBins_In[nom_name][sub_name] = float(ptr.GetValue())
        print(f"{color.BGREEN}Evaluations are Complete{color.END}\n")
    elif(verbose):
        print(f"\n{color.RED}Running as a test (no event evaluations)...{color.END}\n")
        timer.time_elapsed()
    else:
        print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}\n")
    SumOfWeights_L_In.clear()
    Full_Run__List_In.clear()
    return List_of_BCBins_In, SumOfWeights_L_In, Full_Run__List_In

print(f"\n{color.BGREEN}Looping through sub-bins...{color.END}\n")
List_of_BCBins = {"keys": {"Nominal-Bins": "Bin (Q2_y_Bin-z_pT_Bin-phih_bin)", "Sub-Bins": "Bin (Q2_y_Bin-Q2y_Sbin)-(z_pT_Bin-zpT_Sbin)-(phih_bin-phi_Sbin)"}}
SumOfWeights_L = {} # Initial List for `List_of_BCBins` that will pass all the sums to the final list after the dataframe evaluations
Full_Run__List = [] # Used to store the sums in `SumOfWeights_L` in a way that is easily calculable at the end of the loops
Q2_y_Bin_Range = range(1, 18) if(args.Q2_y_Bin == -1) else [args.Q2_y_Bin]
z_pT_Bin_Range = range(1, 37) if(args.z_pT_Bin == -1) else [args.z_pT_Bin]
phih_Bin_Range = range(1, 16) if(args.phih_Bin == -1) else [args.phih_Bin]
Total_Num_SBin = 0
for                     Q2_y_Bin in Q2_y_Bin_Range:
    gdf_Q2_y_Bin         = gdf.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")
    for                 z_pT_Bin in z_pT_Bin_Range:
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
            if(z_pT_Bin < 35):
                print(f"{color.Error}Skip Bin {Q2_y_Bin}-{z_pT_Bin}{color.END}")
            continue
        gdf_z_pT_Bin     = gdf_Q2_y_Bin.Filter(f"z_pT_Bin_Y_bin == {z_pT_Bin}")
        for             phih_bin in phih_Bin_Range:
            gdf_phih_Bin = gdf_z_pT_Bin.Filter(f"phi_t_bin == {phih_bin}")
            Nominal_bin_name = f"Bin ({Q2_y_Bin}-{z_pT_Bin}-{phih_bin})"
            List_of_BCBins[Nominal_bin_name] = {}
            for         Q2y_Sbin in range(1, int((args.num_sub_bins*args.num_sub_bins)+1)):
                gdf_Q2y_SBin         = gdf_phih_Bin.Filter(f"Q2_y_SUB_BINs == {Q2y_Sbin}")
                for     zpT_Sbin in range(1, int((args.num_sub_bins*args.num_sub_bins)+1)):
                    gdf_zpT_SBin     = gdf_Q2y_SBin.Filter(f"z_pT_SUB_BINs == {zpT_Sbin}")
                    for phi_Sbin in range(1, int(args.num_sub_bins+1)):
                        gdf_phi_SBin = gdf_zpT_SBin.Filter(f"phi_t_SUB_BINs == {phi_Sbin}")
                        sub_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-{zpT_Sbin})-({phih_bin}-{phi_Sbin})"
                        sumw = gdf_phi_SBin.Sum("Event_Weight") # Book the action; do NOT GetValue() yet
                        SumOfWeights_L[(Nominal_bin_name, sub_bin_name)] = sumw
                        Full_Run__List.append(sumw)
                        if(args.verbose):
                            print(f"\t\t{color.BOLD}Collected Sub-{sub_bin_name}{color.END}")
                            print(f"\t\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
            print(f"\t{color.BBLUE}Collected all sub-bins in {Nominal_bin_name}{color.END}")
            Total_Num_SBin += len(Full_Run__List)
            List_of_BCBins, SumOfWeights_L, Full_Run__List = Evaluate_Weights(List_of_BCBins, SumOfWeights_L, Full_Run__List)
print(f"\n{color.BGREEN}Done Collecting all the bin event counts {color.END_B}(Total Number of Sub-bins Collected = {Total_Num_SBin}){color.END}")
    
timer.stop(return_Q=not True)

# print(f"Done (Ran {len(List_of_histos)} histos)")

# print(f"\n{color.BGREEN}Creating phi_h histograms...{color.END}\n")
# List_of_histos = {}
# List_of_FitPar = {}
# Q2_y_Bin_Range = range(1, 18) if(args.Q2_y_Bin == -1) else [args.Q2_y_Bin]
# z_pT_Bin_Range = range(1, 37) if(args.z_pT_Bin == -1) else [args.z_pT_Bin]
# Title = f"#splitline{{{root_color.Bold}{{Generated #phi_h Distributions from {'EvGen' if(not args.use_clasdis) else 'clasdis'}}}}}{{Made with {args.num_sub_bins} Sub-Bins per Kinematic Variable}}"
# for     Q2_y_Bin in Q2_y_Bin_Range:
#     for z_pT_Bin in z_pT_Bin_Range:
#         if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
#             if(z_pT_Bin < 35):
#                 print(f"{color.Error}Skip Bin {Q2_y_Bin}-{z_pT_Bin}{color.END}")
#             continue
#         for     Q2y_Sbin in range(0, int((args.num_sub_bins*args.num_sub_bins)+1)):
#             for zpT_Sbin in range(0, int((args.num_sub_bins*args.num_sub_bins)+1)):
#                 histo_bin_name = f"Bin ({Q2_y_Bin}-{Q2y_Sbin})-({z_pT_Bin}-{zpT_Sbin})"
#                 # print(histo_bin_name)
#                 main_bin_cut = f"((Q2_Y_Bin == {Q2_y_Bin}) && (z_pT_Bin_Y_bin == {z_pT_Bin}))"
#                 sub__bin_cut = f"(Q2_y_SUB_BINs == {Q2y_Sbin}) && "           if(Q2y_Sbin != 0) else "(Q2_y_SUB_BINs != -1) && "
#                 sub__bin_cut = f"{sub__bin_cut}(z_pT_SUB_BINs == {zpT_Sbin})" if(zpT_Sbin != 0) else f"{sub__bin_cut} (z_pT_SUB_BINs != -1)"
#                 List_of_histos[histo_bin_name] = (gdf.Filter(f"{main_bin_cut} && ({sub__bin_cut})")).Histo1D((histo_bin_name, f"#splitline{{{Title}}}{{(Q^2-y)-(z-P_T) {histo_bin_name}}}", 24, 0, 360), "phi_t", "Event_Weight")
#                 List_of_histos[histo_bin_name].SetLineColor(ROOT.kGreen)
#                 List_of_FitPar[histo_bin_name] = Fitting_Phi_Function(Histo_To_Fit=List_of_histos[histo_bin_name], Method="gdf", Fitting="default", Special="Normal", Fit_Test=True)
#                 if("ERROR" == List_of_FitPar[histo_bin_name]):
#                     continue
#                 # List_of_FitPar[histo_bin_name] = [Histo_To_Fit,  Fitting_Function,   [Fit_Chisquared,    Fit_ndf],  [A_Unfold,    A_Unfold_Error],  [B_Unfold,    B_Unfold_Error],  [C_Unfold,    C_Unfold_Error]]
#                 List_of_histos[histo_bin_name], _, Chisquared_and_ndf, A_Fit_L, B_Fit_L, C_Fit_L = List_of_FitPar[histo_bin_name]
#                 print(f"\nFor: {color.BOLD}'{histo_bin_name}'{color.END}:")
#                 print(f"\tA = {A_Fit_L[0]:>5.3f} ± {A_Fit_L[1]:>5.2f}")
#                 print(f"\tB = {B_Fit_L[0]:>2.7f} ± {B_Fit_L[1]:>2.5e}")
#                 print(f"\tC = {C_Fit_L[0]:>2.7f} ± {C_Fit_L[1]:>2.5e}")
#             Canvas_Image_Create(List_of_histograms=List_of_histos, Q2_y_Bin=Q2_y_Bin, z_pT_Bin=z_pT_Bin, Q2y_Sbin=Q2y_Sbin)
#             timer.time_elapsed()
#             break
#         # print("")
# print(f"Done (Ran {len(List_of_histos)} histos)")
# timer.stop(return_Q=not True)



