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


import subprocess
def ansi_to_html(text):
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
""", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# """, formatter_class=argparse.RawTextHelpFormatter)#formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-ns', '--test', '--time', '--no-save', action='store_true', dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Lower_Acceptance_Cut_AND_Errors_done_with_kCovToy.root",
                   help="Name of ROOT input file.")
    p.add_argument('-sf', '--single_file', action='store_true', dest='single_file',
                   help="Forces all histograms to come from one source (impacts the closure tests that try to draw from multiple files).")
    
    p.add_argument('-ff', '--file_format', type=str, default=".png", choices=['.png', '.pdf', '.root'],
                   help="Output File Formats.")

    p.add_argument('-so', '--smearing_option', type=str, default="Smear", choices=["Smear", "''"],
                  help="Smearing options for unfolding.")
    
    # simulation / modulation / closure
    p.add_argument('-sim', '--simulation', action='store_true', dest='sim',
                   help="Use reconstructed MC instead of experimental data.")
    p.add_argument('-mod', '--modulation', action='store_true', dest='mod',
                   help="Use modulated MC files to create response matrices.")
    p.add_argument('-mod_solo', '--modulation_solo', action='store_true', dest='mod_solo',
                   help="Use modulated MC files to create response matrices, but will not compare to other files (use to get around the `--use_errors_json` restrictions).")
    p.add_argument('-close', '--closure',  action='store_true', dest='closure',
                   help="Run Closure Test (unfold modulated MC with itself).")
    p.add_argument('-data', '--data_compare',  action='store_true', dest='data',
                   help="Compares Data distributions to MC (can run with `-mod` to modify the MC with the injected modulations and acceptance weights).")

    p.add_argument('-rb', '--remake_bin_by_bin',  action='store_true', dest='remake',
                   help="Remakes bin-by-bin acceptance corrections for 'Mod_Test' and 'Sim_Test' while weighing the modulated MC to the same statistics as the normal MC.")

    # # fitting / output control
    p.add_argument('-nf', '--no-fit', action='store_true', dest='no_fit',
                   help="Disable fitting of plots.")
    p.add_argument('-fr', '--fit_root', type=str, default=None,
                   help="Optional ROOT file to save fit outputs (fitted histograms, fit functions, and fit parameter vectors). If omitted, fit outputs are not written to a ROOT file.")
    
    p.add_argument('-t', '--title', type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-sn', '--save_name', type=str, default="",
                   help="Adds an extra string to the end of the file names that the images will be saved as.")

    p.add_argument('-evgen', '--EvGen', action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-u', '--unfold', type=str, default="Bayesian", 
                   help="Histogram type option.")

    p.add_argument('-d', '--dimensions', type=str, default="3D", 
                   help="Unfolding Dimensions option.")

    p.add_argument('-b', '-q2_y', '--bins', nargs="+", type=str, default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
                   help="List of Q2-y bin indices to run.")

    p.add_argument('-z_pt', '--z_pt', nargs="+", type=int, 
                   help="List of z-pT bin indices to run. (Will run all z-pT bins if select ones are not given)")

    p.add_argument('-all', '--all_z_pt', action='store_true',
                   help="Draws all possible z-pT plots together in one image.")

    p.add_argument('-si', '--show_integral', action='store_true',
                   help="Shows the integrals of the phi_h distributions in the `--all_z_pt` image option.")
    
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

    # p.add_argument('-uej', '--use_errors_json', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Mod_Test_Unfolding_Bin_Differences_FirstOrderAcc.json", 
    #                help="Will apply uncertainties to the baseline histograms based on the file given with this argument if the `--use_errors` option is selected. (Is not used for the `--mod` option)")
    
    p.add_argument('-uej', '--use_errors_json', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Mod_Test_Unfolding_Bin_Differences.json", 
                   help="Will apply uncertainties to the baseline histograms based on the file given with this argument if the `--use_errors` option is selected. (Is not used for the `--mod` option)")

    p.add_argument('-ie', '--invert_errors', action='store_true', 
                   help="Inverts the asymmetric errors from the JSON files so that the direction it is applied is reversed (meant to allow me to assign the errors to the acceptance weighted fits).")
    
    p.add_argument('-rad', '--radiation_correction', action='store_true', 
                   help="Applies Radiative Corrections.")
    p.add_argument('-fi', '--fewer_images', action='store_true', 
                   help="Skips saving some images that might not be needed.")
    p.add_argument('-c', '--compare', action='store_true', 
                   help="Compares the same histograms from different ROOT file sources.")
    p.add_argument('-r2', '--root_compare', type=str, default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_Unfolded_Histos_From_FirstOrderAcc_as_of_12_2_2025.root",
                   help="Name of second ROOT input file for using with `--compare`.")
    p.add_argument('-ln1', '--legend_name_1', type=str, default=None,
                   help="Custom Legend Name for histogram 1 (use with `-all` option).")
    p.add_argument('-ln2', '--legend_name_2', type=str, default=None,
                   help="Custom Legend Name for histogram 2 (use with `-all` option).")

    p.add_argument('-mj', '-mjson', '--make_json', action='store_true', 
                   help="Allows for new JSON files to be made (if not used, not JSON file will be outputted).")
    
    return p.parse_args()

args = parse_args()

# if((args.radiation_correction) and (args.use_errors_json == "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Mod_Test_Unfolding_Bin_Differences_FirstOrderAcc.json")):
#     # Changing default based on using the radiative corrections
#     args.use_errors_json = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Mod_Test_Unfolding_Bin_Differences_FirstOrderAcc_Rad.json"

# def silence_root_import():
#     # Flush Python’s buffers so dup2 doesn’t duplicate partial output
#     sys.stdout.flush()
#     sys.stderr.flush()
#     # Save original file descriptors
#     old_stdout = os.dup(1)
#     old_stderr = os.dup(2)
#     try:
#         # Redirect stdout and stderr to /dev/null at the OS level
#         devnull = os.open(os.devnull, os.O_WRONLY)
#         os.dup2(devnull, 1)
#         os.dup2(devnull, 2)
#         os.close(devnull)
#         # Perform the noisy import
#         import RooUnfold
#     finally:
#         # Restore the original file descriptors
#         os.dup2(old_stdout, 1)
#         os.dup2(old_stderr, 2)
#         os.close(old_stdout)
#         os.close(old_stderr)

# # Use it like this:
# silence_root_import()

if((args.compare) and (args.single_file)):
    args.single_file = False
    print(f"\n{color.Error}With `--compare` selected, `--single_file` must be set to false...{color.END}\n")

Saving_Q = not args.test
Fit_Test = not args.no_fit

if(args.remake and (args.unfold not in ["Bin"])):
    print(f"{color.RED}Option to use '--remake_bin_by_bin' requires Bin-by-Bin corrections to be selected.{color.END}")
    args.unfold = "Bin"


Standard_Histogram_Title_Addition = ""
if(args.sim):
    print(f"\n{color.BLUE}Running Simulated Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation"
    if(not args.single_file):
        args.root = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Synthetic_Data_with_kCovToy.root"

if(args.closure):
    print(f"\n{color.BLUE}Running Closure Test{color.END}\n")
    Standard_Histogram_Title_Addition = "Closure Test - Unfolding Simulation with itself"
    if(not args.single_file):
        args.root = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Closure_Test_with_kCovToy.root"

if(args.title):
    if(Standard_Histogram_Title_Addition not in [""]):
        Standard_Histogram_Title_Addition = f"#splitline{{{Standard_Histogram_Title_Addition}}}{{{args.title}}}"
    else:
        Standard_Histogram_Title_Addition = args.title
    print(f"\nAdding the following extra title to the histograms:\n\t{Standard_Histogram_Title_Addition}\n")
    
if(not Fit_Test):
    print(f"\n\n{color.BBLUE}{color_bg.RED}\n\n    Not Fitting Plots    \n{color.END}\n\n")
elif(not args.fit_root):
    print(f"\n{color.Error}Not Saving Fit Outputs to a ROOT File{color.END}\n")
else:
    print(f"\n{color.BGREEN}Saving Fit Outputs to {color.BBLUE}{args.fit_root}{color.END}\n")
    

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
# def Apply_PreBin_Uncertainties(Histo_In, Q2_y_Bin=None, z_pT_Bin=None, Uncertainty_File_In=args.use_errors_json):
#     # Something was going wrong when I updated this function
#     return Histo_In

def Apply_PreBin_Uncertainties(Histo_In, Q2_y_Bin=None, z_pT_Bin=None, Uncertainty_File_In=args.use_errors_json):
    # Modify the bin uncertainties of a histogram using precomputed values
    # from a JSON file. If any condition fails, return the unmodified histogram.
    if(Uncertainty_File_In is None):
        return Histo_In

    # Check histogram validity
    if((not Histo_In) or (not Histo_In.InheritsFrom("TH1"))):
        print(f"{color.Error}Error:{color.END}\n\t{Histo_In} is an invalid histogram that was passed to Apply_PreBin_Uncertainties()")
        return Histo_In
        
    Histo_Name_General = Histo_In.GetName()
    # If Q2_y_Bin / z_pT_Bin were not given, try to parse them from the name
    if((Q2_y_Bin is None) or (z_pT_Bin is None)):
        match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_General))
        if(match):
            Q2_y_Bin = int(match.group(1))
            z_pT_Bin = int(match.group(2))
        else:
            print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
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

    # Build an asymmetric error graph, like in Compare_TH1D_Histograms
    g_asym = ROOT.TGraphAsymmErrors(Histo_In)
    g_asym.SetName(f"{Histo_In.GetName()}_AsymErr")
    g_asym.SetLineColor(Histo_In.GetLineColor())
    g_asym.SetMarkerColor(Histo_In.GetMarkerColor())
    g_asym.SetLineWidth(Histo_In.GetLineWidth())

    # Apply new errors to each bin
    for i, entry in enumerate(bin_data, start=1):
        # Signed difference val2 - val1; magnitude is the systematic envelope
        uncertainty = float(entry.get("uncertainty", 0.0))
        current_err = float(Histo_In.GetBinError(i))
        # sys_mag     = abs(uncertainty)
        sys_mag     = ROOT.sqrt(max([current_err**2, uncertainty**2 + current_err**2]))

        if(args.invert_errors):
            # Set `uncertainty` to `-uncertainty` to invert the direction it is applied below
            uncertainty = -uncertainty

        # # Symmetric envelope (like we used before: max of stat and sys)
        # new_err = max([sys_mag, current_err])
        # Histo_In.SetBinError(i, new_err)
        # # Do not reset the histogram errors since that just makes it more likely that the asymmetric error bars won't be visible

        low_err, high_err = current_err, current_err
        if(uncertainty > 0.0):
            low_err  = current_err
            high_err = sys_mag
        elif(uncertainty < 0.0):
            low_err  = sys_mag
            high_err = current_err
        # # Asymmetric split:
        # #   positive -> upper side enlarged
        # #   negative -> lower side enlarged
        # if(sys_mag > current_err):
        #     if(uncertainty > 0.0):
        #         low_err  = current_err
        #         high_err = sys_mag
        #     elif(uncertainty < 0.0):
        #         low_err  = sys_mag
        #         high_err = current_err
        # # Otherwise systematic smaller than stat → keep symmetric

        # Set asymmetric errors on the graph (bin index → point index i-1)
        g_asym.SetPointEYlow(i  - 1, low_err)
        g_asym.SetPointEYhigh(i - 1, high_err)

    # Attach graph to histogram for later drawing / fitting
    Histo_In.asym_errors = g_asym

    return Histo_In


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
        if(abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol):
            break
        centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
        reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
        if(func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args)):
            simplex[-1] = reflected
            continue
        if(func(reflected, *args) < func(simplex[0], *args)):
            expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
            if(func(expanded, *args) < func(reflected, *args)):
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected
            continue
        contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
        if(func(contracted, *args) < func(simplex[-1], *args)):
            simplex[-1] = contracted
            continue
        for i in range(1, N+1):
            simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]
    return simplex[0]

def Full_Calc_Fit(Histo):
    # Helping the closure tests with known values of B and C
    # if(Closure_Test):
    #     B_opt, C_opt = -0.500, 0.025
    #     Histo_max_bin     = Histo.GetMaximumBin()
    #     Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
    #     Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
    #     A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    # elif(Sim_Test):
    #     B_opt, C_opt = 0, 0
    #     Histo_max_bin     = Histo.GetMaximumBin()
    #     Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
    #     Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
    #     A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    # else:
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
        print(f"{color.Error}Full_Calc_Fit(...) ERROR:\n{color.END}{traceback.format_exc()}\n\n{color.Error}ERROR is with 'Histo' = {Histo}\n{color.END}")
        A_opt, B_opt, C_opt = "Error", "Error", "Error"
        
    return [A_opt, B_opt, C_opt]
    

from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
def Fitting_Phi_Function(Histo_To_Fit_In, Method="FIT", Special="Normal", Overwrite_Fit_Test=Fit_Test):
    if((args.radiation_correction) and ("RC" not in Method)):
        Method = f"RC_{Method}"
    Histo_To_Fit = Histo_To_Fit_In.asym_errors if(hasattr(Histo_To_Fit_In, "asym_errors")) else Histo_To_Fit_In
    if((Method in ["RC"]) and Overwrite_Fit_Test):
        try:
            Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
            Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit_In.GetName()}_{Method}", fit_function, 0, 360)
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
    elif((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true", "RC_Bin", "RC_Bayesian"]) and Overwrite_Fit_Test):
        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit_In)
        fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
        
        Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit_In.GetName()}_{str(Method).replace(' ', '_')}", str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")

        fit_range_lower = 0
        fit_range_upper = 360
        # Number of bins in the histogram
        n_bins = Histo_To_Fit_In.GetNbinsX()

        # Fitting_Function.SetLineColor(Histo_To_Fit_In.GetLineColor())
        
        # Find the lower fit range (first non-empty bin)
        for bin_lower in range(1, n_bins // 2 + 1):  # Search from the start to the center
            if(Histo_To_Fit_In.GetBinContent(bin_lower) != 0):
                fit_range_lower = Histo_To_Fit_In.GetXaxis().GetBinLowEdge(bin_lower)
                break  # Stop the loop once the first non-empty bin is found

        # Find the upper fit range (last non-empty bin)
        for bin_upper in range(n_bins, n_bins // 2, -1):  # Search from the end towards the center
            if(Histo_To_Fit_In.GetBinContent(bin_upper) != 0):
                fit_range_upper = Histo_To_Fit_In.GetXaxis().GetBinUpEdge(bin_upper)
                break  # Stop the loop once the last non-empty bin is found
        
        
        Fitting_Function.SetRange(fit_range_lower, fit_range_upper)

        Fitting_Function.SetLineColor(Histo_To_Fit_In.GetLineColor())
        
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

                if(((Special not in ["Normal"]) and isinstance(Special, list)) and (not args.closure)):
                    try:
                        Q2_y_Bin_Special, z_pT_Bin_Special = str(Special[0]), str(Special[1])
                        # print(f"Fitting_Phi_Function Special: Q2_y_Bin_Special, z_pT_Bin_Special = {Q2_y_Bin_Special}, {z_pT_Bin_Special}")
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
                else:
                    print(f"\n\n\n{color.RED}Fitting_Phi_Function Not Special{color.END}\n\n\n")
                
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
            # Fitting_Function.SetLineColor(Histo_To_Fit_In.GetLineColor())

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
        print(f"\n\n\n{color.Error}ERROR WITH Fitting_Phi_Function()\n\t'Method' is not selected for proper output...\n\n\n{color.END}")
        return "ERROR"
    

def Draw_Fit_Params_Box(TPad_cd=None, Chi_List=None, ParA=None, ParB=None, ParC=None, header="", x1=0.60, y1=0.60, x2=0.95, y2=0.95, text_size=0.030):
    # Draw nothing if we have no pad or no parameters
    # pad = ROOT.gPad
    if(not TPad_cd):
        return None
    if((ParA is None) and (ParB is None) and (ParC is None) and (Chi_List is None)):
        return None

    TPad_cd.cd()
    
    box = ROOT.TPaveText(x1, y1, x2, y2, "NDC")
    box.SetFillColor(0)
    # box.SetFillStyle(1001)
    box.SetFillStyle(0)    # no fill
    box.SetBorderSize(1)
    box.SetTextAlign(13)  # left, top
    box.SetTextSize(text_size)

    if(header not in [None, ""]):
        box.AddText(header)

    chi2, ndf = None, None
    if((Chi_List is not None) and (len(Chi_List) == 2)):
        chi2, ndf = Chi_List[0], Chi_List[1]

    # Helper to add parameter lines safely
    def add_par_line(label, par_list):
        if((par_list is None) or (len(par_list) != 2)):
            return
        val, err = par_list[0], par_list[1]
        try:
            val = float(val)
            err = float(err)
        except:
            return
        # box.AddText(f"{label} = {val:.4g} #pm {err:.4g}")
        box.AddText(f"{label} = {val:.4g} #pm {err:.3g}")

    add_par_line("A", ParA)
    add_par_line("B", ParB)
    add_par_line("C", ParC)

    if((chi2 is not None) and (ndf not in [None, 0, "0"])):
        try:
            chi2     = float(chi2)
            chi2_ndf = chi2/float(ndf)
            box.AddText(f"#chi^{{2}}/ndf = {chi2:.2f} / {int(ndf)}")
            # box.AddText(f"#chi^{{2}}/ndf #approx {chi2_ndf:.2f}")
        except:
            pass

    box.Draw()
    TPad_cd.Modified()
    TPad_cd.Update()
    return box


def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        if(args.verbose):
            print(f"Deleting: '{obj.GetName()};*' (already exists)")
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()

def Save_Fit_Outputs_To_ROOT(Histo_Name, Chi_List, ParA_List, ParB_List, ParC_List, Histo_New=None, Fit_Function=None):
    # If no output file requested, do nothing
    if(args.no_fit or (args.fit_root in [None, ""])):
        return

    # Decide whether to UPDATE or RECREATE
    tfile = ROOT.TFile.Open(args.fit_root, "UPDATE" if(os.path.exists(args.fit_root)) else "RECREATE")
    if((not tfile) or tfile.IsZombie()):
        print(f"""{color.Error}ERROR:{color.END} Could not open fit-output file '{args.fit_root}' in mode '{"UPDATE" if(os.path.exists(args.fit_root)) else "RECREATE"}'.""")
        return

    # Determine the entry_type prefix
    # Histo_Name_str = str(Histo_Name)
    Histo_Name_str = str(Histo_New.GetName())
#     if(args.verbose):
#         print(f"""
# Histo_Name_str (from input) = {Histo_Name_str}
# Histo_Name_str (from histo) = {Histo_New.GetName()}""")
    entry_type = "(1D)_" if(Histo_Name_str.startswith("(1D)_")) else "(MultiDim_3D_Histo)_" if(Histo_Name_str.startswith("(MultiDim_3D_Histo)_")) else "(MultiDim_5D_Histo)_"
    
    Fit_Function_Name    = Histo_Name_str.replace(str(entry_type), "(Fit_Function)_")
    Chi_Squared_Name     = Histo_Name_str.replace(str(entry_type), "(Chi_Squared)_")
    Fit_Par_A_List_Name  = Histo_Name_str.replace(str(entry_type), "(Fit_Par_A)_")
    Fit_Par_B_List_Name  = Histo_Name_str.replace(str(entry_type), "(Fit_Par_B)_")
    Fit_Par_C_List_Name  = Histo_Name_str.replace(str(entry_type), "(Fit_Par_C)_")

    # 1) Overwrite the fitted histogram itself
    if(Histo_New):
        # histo_out = Histo_New.Clone(Histo_Name_str)
        # histo_out.SetName(Histo_Name_str)
        # safe_write(histo_out, tfile)
        safe_write(Histo_New, tfile)

    # 2) Fit function
    if(Fit_Function):
        fit_out = Fit_Function.Clone(Fit_Function_Name)
        fit_out.SetName(Fit_Function_Name)
        safe_write(fit_out, tfile)

    # Helper: Python list -> TVectorD
    def write_vec(name, py_list):
        if(py_list is None):
            print(f"{color.Error}py_list is 'None'{color.END}")
            return
        if(len(py_list) == 0):
            print(f"{color.Error}len(py_list) == 0{color.END}")
            return
        # Fill a TVectorD with the values
        vec = ROOT.TVectorD(len(py_list))
        for i, val in enumerate(py_list):
            vec[i] = float(val)
        keyname = f"TVectorD_{name}"
        # Manually handle overwriting since TVectorD has no SetName/GetName
        existing = tfile.GetListOfKeys().FindObject(keyname)
        if(existing):
            if(args.verbose):
                print(f"Deleting: '{keyname};*' (already exists)")
            tfile.Delete(f"{keyname};*")
        # Store with the desired key name (this sets the *key* name in the file, even though the object itself doesn’t have a SetName method)
        tfile.WriteObject(vec, keyname)


    # 3) Lists (as TVectorD) with the requested names
    write_vec(Chi_Squared_Name,    Chi_List)
    write_vec(Fit_Par_A_List_Name, ParA_List)
    write_vec(Fit_Par_B_List_Name, ParB_List)
    write_vec(Fit_Par_C_List_Name, ParC_List)

    tfile.Close()

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


if(args.radiation_correction):
    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code'
    sys.path.append(script_dir)
    from Find_RC_Fit_Params import Find_RC_Fit_Params, Apply_RC_Factor_Corrections, Get_RC_Fit_Plot
    sys.path.remove(script_dir)
    del script_dir
    print(f"\n{color.BOLD}Loaded `{color.GREEN}Find_RC_Fit_Params{color.END_B}` and `{color.GREEN}Apply_RC_Factor_Corrections{color.END_B}` for applying RC Corrections...{color.END}\n")
    def apply_RC_to_found_histo(histo_In, Q2y_bin=None, zPT_bin=None):
        Histo_Name_General = histo_In.GetName()
        if(not (Q2y_bin and zPT_bin)):
            match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_General))
            if(match):
                Q2y_bin = int(match.group(1))
                zPT_bin = int(match.group(2))
            else:
                print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                return histo_In
                
        if(all(cor not in Histo_Name_General for cor in ["Bayesian", "(Bin)"])):
            # if(args.verbose):
            print(f"\n{color.RED}Warning: Missing the Corrected Distribution for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
            return histo_In
            
        Histo_Name_Rad_Cor = str(Histo_Name_General.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
        RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=Q2y_bin, z_pT_bin=zPT_bin, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
        histo_rad = Apply_RC_Factor_Corrections(hist=histo_In, Par_A=RC_Par_A, Par_B=RC_Par_B, Par_C=RC_Par_C, use_param_errors=True, Par_A_err=RC_Err_A, Par_B_err=RC_Err_B, Par_C_err=RC_Err_C, param_cov=None)
        histo_In = histo_rad.Clone(Histo_Name_Rad_Cor)
        return histo_In
else:
    def apply_RC_to_found_histo(histo_In, Q2y_bin=None, zPT_bin=None):
        print(f"\n\n{color.Error}Did not set up RC code — This function (apply_RC_to_found_histo) shouldn't have been called...{color.END}\n\n")
        return histo_In


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

    if((args.radiation_correction) and (args.unfold in ["Bayesian", "Bin"])):
        if(args.verbose):
            print("Applying Radiative Corrections...")
        histo = apply_RC_to_found_histo(histo_In=histo)
    elif((args.radiation_correction) and (args.verbose)):
        print(f"{color.RED}Cannot apply Radiative Corrections to uncorrected histograms{color.END}")

    if(args.use_errors):
        if(args.verbose):
            print("Applying Uncertainties from JSON File...")
        histo = Apply_PreBin_Uncertainties(Histo_In=histo, Uncertainty_File_In=args.use_errors_json)
        
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
    gdf_histo__mod = ROOT_IN_MODULATED.Get(str(f"{HISTO_NAME_INPUT}_(Mod_Test)".replace(f"({args.unfold})", "(gdf)")).replace("(SMEAR=Smear)", "(SMEAR='')"))
    mdf_histo__mod = ROOT_IN_MODULATED.Get(str(f"{HISTO_NAME_INPUT}_(Mod_Test)".replace(f"({args.unfold})", "(mdf)")))

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
            if(args.single_file):
                histo1     = ROOT_In_1.Get(HISTO_NAME_1)
        elif(args.sim):
            histo1, histo2 = Make_New_BbB_Sim(ROOT_IN_MODULATED=ROOT_In_1, HISTO_NAME_INPUT=HISTO_NAME_1)
        else:
            print(f"{color.Error}ERROR:{color.END} Could not remake the histograms for the test requested.\n\t{color.BOLD}Returning default outputs")
            histo1 = ROOT_In_1.Get(HISTO_NAME_1)
            histo2 = ROOT_In_2.Get(HISTO_NAME_2)
    else:
        histo1 = ROOT_In_1.Get(HISTO_NAME_1)
        histo2 = ROOT_In_2.Get(HISTO_NAME_2)

    if((args.radiation_correction) and (args.unfold in ["Bayesian", "Bin"]) and ("All" not in [Q2y_str, zPT_str])):
        if(args.verbose):
            print("Applying Radiative Corrections...")
        for num, histo_rad in enumerate([histo1, histo2]):
            Histo_Name_General   = histo_rad.GetName()
            if(all(cor not in Histo_Name_General for cor in ["Bayesian", "(Bin)"])):
                if(args.verbose):
                    print(f"\n{color.RED}Warning: Missing the Corrected Distribution for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                continue
            Histo_Name_Rad_Cor   = str(Histo_Name_General.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
            RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=int(Q2y_str), z_pT_bin=int(zPT_str), root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
            histo_rad = Apply_RC_Factor_Corrections(hist=histo_rad, Par_A=RC_Par_A, Par_B=RC_Par_B, Par_C=RC_Par_C, use_param_errors=True, Par_A_err=RC_Err_A, Par_B_err=RC_Err_B, Par_C_err=RC_Err_C, param_cov=None)
            if(num == 0):
                histo1 = histo_rad.Clone(Histo_Name_Rad_Cor)
            if(num == 1):
                histo2 = histo_rad.Clone(Histo_Name_Rad_Cor)
    elif((args.radiation_correction) and (args.verbose)):
        print(f"{color.RED}Cannot apply Radiative Corrections to uncorrected histograms (or to 'All' bins){color.END}")
    
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
    
    normalization_to_histo1, normalization_to_histo2 = 1.0, 1.0
    if(args.normalize):
        histo1, histo2, _, normalization_to_histo1, normalization_to_histo2 = Normalize_To_Shared_Bins(histo1, histo2, threshold=0.0, include_under_over=False, name_suffix="_NormShared")
    
    if(("Pass 2" in histo1.GetTitle()) and ((TITLE not in histo1.GetTitle()) and (TITLE not in histo2.GetTitle()))):
        histo1.SetTitle(str(histo1.GetTitle()).replace("Pass 2", TITLE))
    elif((TITLE not in histo1.GetTitle()) and (TITLE not in histo2.GetTitle())):
        histo1.SetTitle(f"#splitline{{{histo1.GetTitle()}}}{{{TITLE}}}")

    if(histo1.GetLineColor() == histo2.GetLineColor()):
        histo2.SetLineColor((histo2.GetLineColor() + 2) if(histo2.GetLineColor() != 28) else 26)
    histo1.SetLineWidth(3)
    histo2.SetLineWidth(2)
    
    g_asym = None
    if(args.use_errors):
        g_asym = ROOT.TGraphAsymmErrors(histo1)
        g_asym.SetName(f"{histo1.GetName()}_AsymErr")
        g_asym.SetLineColor(histo1.GetLineColor())
        g_asym.SetMarkerColor(histo1.GetMarkerColor())
        g_asym.SetLineWidth(3)

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
        # err         = math.sqrt(err1**2 + err2**2)
        err         = math.sqrt(max([err1**2 - err2**2, 0]))
        # M_uncer     = math.sqrt(max([0, (val2 - val1)**2 - err**2]))
        # M_uncer     = diff
        M_uncer     = val2 - val1 # if M_uncer is negative, then the uncertainty is applied to the lower error bar. If it is positive, then apply it to the upper error bar
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
        # if(args.use_errors):
        #     histo1.SetBinError(bin_idx, math.sqrt(err1**2 + M_uncer**2))
        if(args.use_errors):
            # Default: purely statistical
            # histo1.SetBinError(bin_idx, max([diff, err1]))
            if(g_asym):
                if(diff < err1):
                    low_err, high_err = err1, err1
                elif(val1 > val2):
                    low_err  = diff
                    high_err = err1
                else:
                    low_err  = err1
                    high_err = diff
                g_asym.SetPointEYlow(bin_idx  - 1,  low_err)
                g_asym.SetPointEYhigh(bin_idx - 1, high_err)
    if(args.use_errors and g_asym):
        histo1.asym_errors = g_asym

    h_diff.GetYaxis().SetRangeUser(0,        1.2*max_content)
    h_uncertainty.GetYaxis().SetRangeUser(0, 1.2*max_M_uncer)
    histo1.GetYaxis().SetRangeUser(0,        1.2*max_cd_1)
    histo2.GetYaxis().SetRangeUser(0,        1.2*max_cd_1)
    
    h_diff.SetLineColor(ROOT.kBlack)
    h_diff.SetLineWidth(2)
    h_diff.SetTitle(f"#splitline{{Absolute Bin Content Differences between}}{{{root_color.Bold}{{{legend_labels[0]}}} and {root_color.Bold}{{{legend_labels[1]}}}}}")
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
        if(hasattr(histo1, "asym_errors")):
            histo1.Draw("H P")
            histo1.asym_errors.Draw("P E SAME")
        else:
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
        if(args.radiation_correction):
            Save_Name = str(Save_Name.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
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
    if(args.mod_solo):
        Canvases_to_Make = [f"Mod_Test_{HISTO_NAME}"]
    if(args.mod):
        Canvases_to_Make = [f"Mod_Test_{HISTO_NAME}", f"Mod_Test_DIFF_{HISTO_NAME}", f"Mod_Test_UNCERTAINTY_{HISTO_NAME}"]
        Legend_Labels    = ["Unfolded with Normal MC", "Unfolded with Modulated MC"]
    elif(args.sim or args.closure):
        Canvases_to_Make = [f"Sim_Test_{HISTO_NAME}", f"Sim_Test_DIFF_{HISTO_NAME}", f"Sim_Test_UNCERTAINTY_{HISTO_NAME}"] if(not args.closure) else [f"Closure_Test_{HISTO_NAME}", f"Closure_Test_DIFF_{HISTO_NAME}", f"Closure_Test_UNCERTAINTY_{HISTO_NAME}"]
        Legend_Labels    = ["Unfolded Synthetic (MC) Data", "True Distribution of Synthetic Data"]
        if(args.dimensions   in ["1D"]):
            HISTO_True   = f"(1D)_(tdf)_(SMEAR=Smear)_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_ALL)_(phi_t)"
        elif(args.dimensions in ["3D", "MultiDim_3D_Histo"]):
            HISTO_True   = f"(MultiDim_3D_Histo)_(tdf)_(SMEAR='')_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_ALL)_(MultiDim_z_pT_Bin_Y_bin_phi_t)"
    if(args.single_file):
        HISTO_NAME = f"{HISTO_NAME}{'_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
        # HISTO_NAME = f"{HISTO_NAME}{'_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
        HISTO_True = f"{HISTO_True}{'_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
        HISTO_True = HISTO_True.replace("(tdf)", "(gdf)")
    if(args.compare):
        HISTO_NAME = f"{HISTO_NAME}{'_(Mod_Test)' if(args.mod or args.mod_solo) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
    if((not args.data) and (args.legend_name_1 is not None)):
        Legend_Labels[0] = str(args.legend_name_1)
    if((not args.data) and (args.legend_name_2 is not None)):
        if(len(Legend_Labels) > 1):
            Legend_Labels[1] = str(args.legend_name_2)
        else:
            Legend_Labels.append(str(args.legend_name_2))
    #######################################################################################################################################################################################################
    ####  Histogram Creations     #########################################################################################################################################################################
    Saved_Histos   = {}
    z_pT_Bin_Range = range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1] + 1)
    for z_PT_BIN_NUM  in z_pT_Bin_Range:
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_PT_BIN_NUM, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
            continue
        HISTO_NAME_Binned = HISTO_NAME.replace("(z_pT_Bin_ALL)", f"(z_pT_Bin_{z_PT_BIN_NUM})")
        HISTO_True_Binned = HISTO_True.replace("(z_pT_Bin_ALL)", f"(z_pT_Bin_{z_PT_BIN_NUM})")
        # if(args.compare):
        #     print(f"\n\nHISTO_NAME = {HISTO_NAME}")
        #     print(f"HISTO_NAME_Binned = {HISTO_NAME_Binned}\n\n")
        if(args.data):
            Data_Legend_Titles = ("Experimental Data", "Reconstructed Monte Carlo" if(not (args.mod or args.closure)) else "Reconstructed MC (with weights)")
            Legend_Labels = ["Experimental Data", "Reconstructed Monte Carlo" if(not (args.mod or args.closure)) else "Reconstructed MC (with weights)"]
            if("rdf" in HISTO_NAME_Binned):
                HISTO_NAME_Binned_1 = HISTO_NAME_Binned.replace("SMEAR=Smear", "SMEAR=''")
                for clear_name in ["_(Mod_Test)", "_(Closure_Test)", "_(Sim_Test)"]:
                    HISTO_NAME_Binned_1 = HISTO_NAME_Binned_1.replace(clear_name, "")
                HISTO_NAME_Binned_2 = HISTO_NAME_Binned.replace("rdf", "mdf")
                HISTO_NAME_Binned_2 = HISTO_NAME_Binned_2.replace("SMEAR=''", f"SMEAR={args.smearing_option}")
                if(args.single_file):
                    for string, condition in [['_(Mod_Test)', args.mod], ['_(Closure_Test)', args.closure], ['_(Sim_Test)', args.sim]]:
                        if((string not in str(HISTO_NAME_Binned_2)) and condition):
                            HISTO_NAME_Binned_2 = f"{HISTO_NAME_Binned_2}{string}"
                            break
            else: # mdf in 'HISTO_NAME_Binned'
                HISTO_NAME_Binned_1 = HISTO_NAME_Binned.replace("SMEAR=''", f"SMEAR={args.smearing_option}")
                if(args.single_file):
                    for string, condition in [['_(Mod_Test)', args.mod], ['_(Closure_Test)', args.closure], ['_(Sim_Test)', args.sim]]:
                        if((string not in str(HISTO_NAME_Binned_1)) and condition):
                            HISTO_NAME_Binned_1 = f"{HISTO_NAME_Binned_1}{string}"
                            break
                HISTO_NAME_Binned_2 = HISTO_NAME_Binned.replace("mdf", "rdf")
                HISTO_NAME_Binned_2 = HISTO_NAME_Binned_2.replace("SMEAR=Smear", "SMEAR=''")
                for clear_name in ["_(Mod_Test)", "_(Closure_Test)", "_(Sim_Test)"]:
                    HISTO_NAME_Binned_2 = HISTO_NAME_Binned_2.replace(clear_name, "")
                Data_Legend_Titles = ("Reconstructed Monte Carlo" if(not (args.mod or args.closure)) else "Reconstructed MC (with weights)", "Experimental Data")
                Legend_Labels = ["Reconstructed Monte Carlo" if(not (args.mod or args.closure)) else "Reconstructed MC (with weights)", "Experimental Data"]
            try:
                if(not ROOT_Mod_In):
                    ROOT_Mod_In = ROOT_Input_In
            except:
                ROOT_Mod_In = ROOT_Input_In
            if((HISTO_NAME_Binned_1 in ROOT_Input_In.GetListOfKeys()) and (HISTO_NAME_Binned_2 in ROOT_Mod_In.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned_1}{color.BGREEN} and {color.END_b}{HISTO_NAME_Binned_2}{color.END}")
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Saved_Histos[f"h_diff_{z_PT_BIN_NUM}"], Saved_Histos[f"h_uncertainty_{z_PT_BIN_NUM}"], Unfolding_Diff_Data_Input =  Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input_In, HISTO_NAME_1=HISTO_NAME_Binned_1, ROOT_In_2=ROOT_Mod_In,   HISTO_NAME_2=HISTO_NAME_Binned_2,                                                                                                                                                 legend_labels=Data_Legend_Titles,                                                      output_prefix="Mod_Test_" if(args.mod) else "Closure_Test_" if(args.closure) else "Sim_Test_" if(args.sim) else "", SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_Y_Bin, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data_Input, Return_Histos=True)
        elif(args.mod):
            if(args.single_file):
                try:
                    if(not ROOT_Mod_In):
                        ROOT_Mod_In = ROOT_Input_In
                except:
                    ROOT_Mod_In = ROOT_Input_In
            if((HISTO_NAME_Binned in ROOT_Input_In.GetListOfKeys()) and (f"{HISTO_NAME_Binned}{'' if(not args.single_file) else '_(Mod_Test)'}" in ROOT_Mod_In.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.END}")
                    if(args.single_file):
                        print(f"\t{color.BGREEN}AND {color.END_b}{HISTO_NAME_Binned}_(Mod_Test){color.END}")
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Saved_Histos[f"h_diff_{z_PT_BIN_NUM}"], Saved_Histos[f"h_uncertainty_{z_PT_BIN_NUM}"], Unfolding_Diff_Data_Input =  Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input_In, HISTO_NAME_1=HISTO_NAME_Binned,   ROOT_In_2=ROOT_Mod_In,   HISTO_NAME_2=f"{HISTO_NAME_Binned}{'' if(not args.single_file) else '_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}", legend_labels=("Unfolded with Normal MC", "Unfolded with Modulated MC"),               output_prefix="Mod_Test_",                                                                                          SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_Y_Bin, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data_Input, Return_Histos=True)
        elif(args.sim or args.closure):
            if((HISTO_NAME_Binned in ROOT_Input_In.GetListOfKeys()) and (HISTO_True_Binned in ROOT_Input_In.GetListOfKeys())):
                if(args.verbose):
                    print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.BGREEN} and {color.END_b}{HISTO_True_Binned}{color.END}")
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Saved_Histos[f"h_diff_{z_PT_BIN_NUM}"], Saved_Histos[f"h_uncertainty_{z_PT_BIN_NUM}"], Unfolding_Diff_Data_Input =  Compare_TH1D_Histograms(ROOT_In_1=ROOT_Input_In, HISTO_NAME_1=HISTO_NAME_Binned,   ROOT_In_2=ROOT_Input_In, HISTO_NAME_2=HISTO_True_Binned,                                                                                                                                                   legend_labels=("Unfolded Synthetic (MC) Data", "True Distribution of Synthetic Data"), output_prefix="Sim_Test_",                                                                                          SAVE=args.save_name, Format=args.file_format, TITLE=Standard_Histogram_Title_Addition, Q2y_str=Q2_Y_Bin, zPT_str=z_PT_BIN_NUM, Unfolding_Diff_Data_In=Unfolding_Diff_Data_Input, Return_Histos=True)
            else:
                print(f"{color.Error}Missing one of the following:\n{color.END_B} HISTO_NAME_Binned = {HISTO_NAME_Binned}\n HISTO_True_Binned = {HISTO_True_Binned}\n{color.END}")
        elif(HISTO_NAME_Binned in ROOT_Input_In.GetListOfKeys()):
            if(args.verbose):
                print(f"{color.BGREEN}Found: {color.END_b}{HISTO_NAME_Binned}{color.END}")
            Saved_Histos[str(z_PT_BIN_NUM)] = Save_Histograms_As_Images(ROOT_In=ROOT_Input_In, HISTO_NAME_In=HISTO_NAME_Binned, Format=args.file_format, SAVE=args.save_name, SAVE_prefix="Sim_Test_" if(args.sim) else "Mod_Test_" if(args.mod or args.mod_solo) else "", TITLE=Standard_Histogram_Title_Addition, Return_Histos=True)
        else:
            print(f"\n{color.Error}MISSING: {HISTO_NAME_Binned}{color.END}\n")

        if(Fit_Test and (args.unfold in ["Bayesian", "Bin", "gdf", "tdf"])):
            if(args.mod or args.sim or args.closure):
                Saved_Histos[f"histo1_{z_PT_BIN_NUM}_fitted"],     Saved_Histos[f"Fit_Function_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Chi_Squared_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_A_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_B_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_C_1_{z_PT_BIN_NUM}"] = Fitting_Phi_Function(Histo_To_Fit_In=Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Method=args.unfold, Special=[Q2_Y_Bin, z_PT_BIN_NUM])
                if(hasattr(Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], "asym_errors")):
                    Saved_Histos[f"histo1_{z_PT_BIN_NUM}"].asym_errors = Saved_Histos[f"histo1_{z_PT_BIN_NUM}_fitted"]
                else:
                    Saved_Histos[f"histo1_{z_PT_BIN_NUM}"]             = Saved_Histos[f"histo1_{z_PT_BIN_NUM}_fitted"]
                if(args.sim or args.closure):
                    Saved_Histos[f"histo2_{z_PT_BIN_NUM}_fitted"], Saved_Histos[f"Fit_Function_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Chi_Squared_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_A_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_B_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_C_2_{z_PT_BIN_NUM}"] = Fitting_Phi_Function(Histo_To_Fit_In=Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Method='tdf' if('(tdf)' in str(HISTO_True)) else 'gdf' if('(gdf)' in str(HISTO_True)) else args.unfold, Special=[Q2_Y_Bin, z_PT_BIN_NUM])
                else:
                    Saved_Histos[f"histo2_{z_PT_BIN_NUM}_fitted"], Saved_Histos[f"Fit_Function_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Chi_Squared_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_A_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_B_2_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_C_2_{z_PT_BIN_NUM}"] = Fitting_Phi_Function(Histo_To_Fit_In=Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Method=args.unfold, Special=[Q2_Y_Bin, z_PT_BIN_NUM])
                if(hasattr(Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], "asym_errors")):
                    Saved_Histos[f"histo2_{z_PT_BIN_NUM}"].asym_errors = Saved_Histos[f"histo2_{z_PT_BIN_NUM}_fitted"]
                else:
                    Saved_Histos[f"histo2_{z_PT_BIN_NUM}"]             = Saved_Histos[f"histo2_{z_PT_BIN_NUM}_fitted"]
                # f"{HISTO_NAME_Binned}{'' if(not args.single_file) else '_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"

#                 print(f"""Saving:
# Saved_Histos[f"histo1_{z_PT_BIN_NUM}"].GetName() = {Saved_Histos[f"histo1_{z_PT_BIN_NUM}"].GetName()}
# Saved_Histos[f"histo2_{z_PT_BIN_NUM}"].GetName() = {Saved_Histos[f"histo2_{z_PT_BIN_NUM}"].GetName()}
# """)
                Save_Fit_Outputs_To_ROOT(Histo_Name=HISTO_NAME_Binned,                                                     Chi_List=Saved_Histos[f"Chi_Squared_1_{z_PT_BIN_NUM}"], ParA_List=Saved_Histos[f"Fit_Par_A_1_{z_PT_BIN_NUM}"], ParB_List=Saved_Histos[f"Fit_Par_B_1_{z_PT_BIN_NUM}"], ParC_List=Saved_Histos[f"Fit_Par_C_1_{z_PT_BIN_NUM}"], Histo_New=Saved_Histos[f"histo1_{z_PT_BIN_NUM}"], Fit_Function=Saved_Histos[f"Fit_Function_1_{z_PT_BIN_NUM}"])
                Save_Fit_Outputs_To_ROOT(Histo_Name=HISTO_True_Binned if(args.sim or args.closure) else HISTO_NAME_Binned, Chi_List=Saved_Histos[f"Chi_Squared_2_{z_PT_BIN_NUM}"], ParA_List=Saved_Histos[f"Fit_Par_A_2_{z_PT_BIN_NUM}"], ParB_List=Saved_Histos[f"Fit_Par_B_2_{z_PT_BIN_NUM}"], ParC_List=Saved_Histos[f"Fit_Par_C_2_{z_PT_BIN_NUM}"], Histo_New=Saved_Histos[f"histo2_{z_PT_BIN_NUM}"], Fit_Function=Saved_Histos[f"Fit_Function_2_{z_PT_BIN_NUM}"])
            else:
                Saved_Histos[f"fitted_{z_PT_BIN_NUM}"],            Saved_Histos[f"Fit_Function_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Chi_Squared_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_A_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_B_1_{z_PT_BIN_NUM}"], Saved_Histos[f"Fit_Par_C_1_{z_PT_BIN_NUM}"] = Fitting_Phi_Function(Histo_To_Fit_In=Saved_Histos[str(z_PT_BIN_NUM)],        Method=args.unfold, Special=[Q2_Y_Bin, z_PT_BIN_NUM])
                if(hasattr(Saved_Histos[str(z_PT_BIN_NUM)],        "asym_errors")):
                    Saved_Histos[str(z_PT_BIN_NUM)].asym_errors        = Saved_Histos[f"fitted_{z_PT_BIN_NUM}"]
                else:
                    Saved_Histos[str(z_PT_BIN_NUM)]                    = Saved_Histos[f"fitted_{z_PT_BIN_NUM}"]
                Save_Fit_Outputs_To_ROOT(Histo_Name=HISTO_NAME_Binned, Chi_List=Saved_Histos[f"Chi_Squared_1_{z_PT_BIN_NUM}"], ParA_List=Saved_Histos[f"Fit_Par_A_1_{z_PT_BIN_NUM}"], ParB_List=Saved_Histos[f"Fit_Par_B_1_{z_PT_BIN_NUM}"], ParC_List=Saved_Histos[f"Fit_Par_C_1_{z_PT_BIN_NUM}"], Histo_New=Saved_Histos[str(z_PT_BIN_NUM)], Fit_Function=Saved_Histos[f"Fit_Function_1_{z_PT_BIN_NUM}"])
            
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
        if(args.use_errors):
            Legend_Header = f"#splitline{{{Legend_Header}}}{{Modified Baseline Errors #scale[0.75]{{(if systematics were greater than statistical errors)}}}}"
        if(args.data):
            Legend_Header = f"#splitline{{#scale[1.5]{{Comparing Data and MC}}}}{{{Legend_Header}}}"
        elif(args.closure):
            Legend_Header = f"#splitline{{#splitline{{#scale[1.5]{{Closure Test}}}}{{Corrected the MC with itself}}}}{{{Legend_Header}}}"
        if(args.radiation_correction):
            Legend_Header = f"#splitline{{#scale[1.5]{{Applying Radiative Corrections}}}}{{{Legend_Header}}}"
        legend[Canvas_Name].SetHeader(Legend_Header, "C") # option "C" allows to center the header
        if(args.mod or args.sim or args.closure or args.data):
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
        Blank = Saved_Histos[f"h_diff_1" if(args.mod or args.sim or args.closure or args.data) else "1"].Clone("EMPTY")
        Blank.SetTitle("")
        Blank.Draw("H P E0")
        legend[Canvas_Name].DrawClone()
        ROOT.gPad.Update()
        All_z_pT_Canvas[Canvas_Name].Update()
        for z_pT in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=int(Q2_Y_Bin))[1]+1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT, BINNING_METHOD=Binning_Method)):
                continue

            integral_1, integral_2, integral_single = None, None, None

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
            if(args.mod or args.sim or args.closure or args.data):
                if(canvas_num == 0):
                    if(hasattr(Saved_Histos[f"histo1_{z_pT}"], "asym_errors")):
                        Saved_Histos[f"histo1_{z_pT}"].Draw("H P SAME")
                        Saved_Histos[f"histo1_{z_pT}"].asym_errors.Draw("P E SAME")
                    else:
                        Saved_Histos[f"histo1_{z_pT}"].Draw("H P E0 SAME")
                    Saved_Histos[f"histo2_{z_pT}"].Draw("H P E0 SAME")
                elif(canvas_num == 1):
                    Saved_Histos[f"h_diff_{z_pT}"].Draw("H P E0")
                else:
                    Saved_Histos[f"h_uncertainty_{z_pT}"].Draw("H P E0")
            else:
                if(hasattr(Saved_Histos[str(z_pT)], "asym_errors")):
                    Saved_Histos[str(z_pT)].Draw("H P")
                    Saved_Histos[str(z_pT)].asym_errors.Draw("P E SAME")
                else:
                    Saved_Histos[str(z_pT)].Draw("H P E0")

            # Compute integrals for the histogram(s) drawn on this pad, if requested
            if(args.show_integral):
                if(args.mod or args.sim or args.closure or args.data):
                    if(canvas_num == 0):
                        if(f"histo1_{z_pT}" in Saved_Histos):
                            integral_1 = Saved_Histos[f"histo1_{z_pT}"].Integral()
                        if(f"histo2_{z_pT}" in Saved_Histos):
                            integral_2 = Saved_Histos[f"histo2_{z_pT}"].Integral()
                    elif(canvas_num == 1):
                        if(f"h_diff_{z_pT}" in Saved_Histos):
                            integral_single = Saved_Histos[f"h_diff_{z_pT}"].Integral()
                    else:
                        if(f"h_uncertainty_{z_pT}" in Saved_Histos):
                            integral_single = Saved_Histos[f"h_uncertainty_{z_pT}"].Integral()
                else:
                    if(str(z_pT) in Saved_Histos):
                        integral_single = Saved_Histos[str(z_pT)].Integral()

            if(Fit_Test and (args.unfold in ["Bayesian", "Bin", "gdf", "tdf"]) and (canvas_num == 0)):
                ROOT.gStyle.SetOptFit(0)
                if(f"Chi_Squared_2_{z_pT}" in Saved_Histos):
                    header_1 = f"#color[{Saved_Histos[f'histo1_{z_pT}'].GetLineColor()}]{{{Legend_Labels[0]}}}"
                    header_2 = f"#color[{Saved_Histos[f'histo2_{z_pT}'].GetLineColor()}]{{{Legend_Labels[1]}}}"
                    if(args.show_integral and (integral_1 is not None)):
                        header_1 = f"#splitline{{{header_1}}}{{Integral = {integral_1:.3g}}}"
                    if(args.show_integral and (integral_2 is not None)):
                        header_2 = f"#splitline{{{header_2}}}{{Integral = {integral_2:.3g}}}"
                    Saved_Histos[f"Parameter_textbox_bin_{z_pT}"]    = Draw_Fit_Params_Box(TPad_cd=All_z_pT_Canvas_cd_2_z_pT_Bin, Chi_List=Saved_Histos[f"Chi_Squared_1_{z_pT}"], ParA=Saved_Histos[f"Fit_Par_A_1_{z_pT}"], ParB=Saved_Histos[f"Fit_Par_B_1_{z_pT}"], ParC=Saved_Histos[f"Fit_Par_C_1_{z_pT}"], header=header_1, x1=0.19,  y1=0.10, x2=0.49,  y2=0.34, text_size=0.025)
                    Saved_Histos[f"Parameter_textbox_bin_{z_pT}_H2"] = Draw_Fit_Params_Box(TPad_cd=All_z_pT_Canvas_cd_2_z_pT_Bin, Chi_List=Saved_Histos[f"Chi_Squared_2_{z_pT}"], ParA=Saved_Histos[f"Fit_Par_A_2_{z_pT}"], ParB=Saved_Histos[f"Fit_Par_B_2_{z_pT}"], ParC=Saved_Histos[f"Fit_Par_C_2_{z_pT}"], header=header_2, x1=0.51,  y1=0.10, x2=0.84,  y2=0.34, text_size=0.025)
                else:
                    header_1 = f"#color[{Saved_Histos[str(z_pT)].GetLineColor()}]{{{Legend_Labels[0]}}}"
                    if(args.show_integral and (integral_single is not None)):
                        header_1 = f"#splitline{{{header_1}}}{{Integral = {integral_single:.3g}}}"
                    Saved_Histos[f"Parameter_textbox_bin_{z_pT}"]    = Draw_Fit_Params_Box(TPad_cd=All_z_pT_Canvas_cd_2_z_pT_Bin, Chi_List=Saved_Histos[f"Chi_Squared_1_{z_pT}"], ParA=Saved_Histos[f"Fit_Par_A_1_{z_pT}"], ParB=Saved_Histos[f"Fit_Par_B_1_{z_pT}"], ParC=Saved_Histos[f"Fit_Par_C_1_{z_pT}"], header=header_1,        x1=0.35,  y1=0.10, x2=0.70,  y2=0.34, text_size=0.030)
            elif(args.show_integral):
                # Fits are not being drawn here; draw integral-only boxes in the same locations
                if(args.mod or args.sim or args.closure or args.data):
                    if(canvas_num == 0):
                        if(integral_1 is not None):
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"] = ROOT.TPaveText(0.19, 0.10, 0.49, 0.34, "NDC")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillColor(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillStyle(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetBorderSize(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetTextSize(0.025)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].AddText(f"#color[{Saved_Histos[f'histo1_{z_pT}'].GetLineColor()}]{{{Legend_Labels[0]}}}")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].AddText(f"Integral = {integral_1:.3g}")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].Draw()
                        if(integral_2 is not None):
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"] = ROOT.TPaveText(0.51, 0.10, 0.84, 0.34, "NDC")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].SetFillColor(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].SetFillStyle(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].SetBorderSize(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].SetTextSize(0.025)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].AddText(f"#color[{Saved_Histos[f'histo2_{z_pT}'].GetLineColor()}]{{{Legend_Labels[1]}}}")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].AddText(f"Integral = {integral_2:.3g}")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}_H2"].Draw()
                    else:
                        if(integral_single is not None):
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"] = ROOT.TPaveText(0.35, 0.10, 0.70, 0.34, "NDC")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillColor(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillStyle(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetBorderSize(0)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetTextSize(0.030)
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].AddText(f"Integral = {integral_single:.3g}")
                            Saved_Histos[f"Integral_textbox_bin_{z_pT}"].Draw()
                else:
                    if(integral_single is not None):
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"] = ROOT.TPaveText(0.35, 0.10, 0.70, 0.34, "NDC")
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillColor(0)
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetFillStyle(0)
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetBorderSize(0)
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].SetTextSize(0.030)
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].AddText(f"Integral = {integral_single:.3g}")
                        Saved_Histos[f"Integral_textbox_bin_{z_pT}"].Draw()

            ROOT.gPad.Update()
            All_z_pT_Canvas[Canvas_Name].Update()
                
        ##################################################################### ################################################################ ################################################################
        #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################
        ##################################################################### ################################################################ ################################################################
        Save_Name = f"{Canvas_Name}_{args.save_name}{args.file_format}"
        if(args.radiation_correction):
            Save_Name = str(Save_Name.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
            if("RC" not in Save_Name):
                Save_Name = f"Ran_with_RC_{Save_Name}"
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
        if((args.fewer_images) and any(((short_save in Save_Name) and (short_save not in str(args.save_name))) for short_save in ["DIFF_", "UNCERTAINTY_"])):
            print(f"{color.BOLD}WOULD HAVE{color.END} Saved Image: {color.RED}{Save_Name}{color.END}\n\t(Skipping due to `--fewer_images` option)")
            continue
        else:
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
ROOT_Mod   = ROOT_Input if(args.single_file) else None
if(args.compare):
    ROOT_Mod = ROOT.TFile.Open(args.root_compare, "READ")
    print(f"Comparing to {args.root_compare}.")
elif(args.mod):
    ROOT_Mod = ROOT_Input if(args.single_file) else ROOT.TFile.Open("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Unfolded_Histos_From_Just_RooUnfold_SIDIS_richcap_Modulated_Response_with_kCovToy.root", "READ")
    
for BIN in Q2_y_Bin_List:
    Q2_y_BIN_NUM       = int(BIN) if(str(BIN) not in ["0"]) else "All"
    if(args.all_z_pt):
        Unfolding_Diff_Data = z_pT_Images_Together_For_Comparisons(ROOT_Input_In=ROOT_Input, ROOT_Mod_In=ROOT_Mod, Unfolding_Diff_Data_Input=Unfolding_Diff_Data, Q2_Y_Bin=Q2_y_BIN_NUM, Plot_Orientation="z_pT")
        to_be_saved_count += 3 if((args.mod or args.sim or args.closure) and (not args.fewer_images)) else 1
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
            
        if(args.single_file):
            HISTO_NAME = f"{HISTO_NAME}{'_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
        if(args.data):
            HISTO__mdf = HISTO_NAME.replace(f"({args.unfold})", "(mdf)")
            HISTO_NAME = HISTO_NAME.replace("(SMEAR=Smear)", "(SMEAR='')")
            # if(args.single_file and args.mod):
            #     HISTO__mdf = f"{HISTO__mdf}_(Mod_Test)"
            #     HISTO_NAME = f"{HISTO_NAME}_(Mod_Test)"
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
            if(args.single_file):
                HISTO_True = f"{HISTO_True}{'_(Mod_Test)' if(args.mod) else '_(Closure_Test)' if(args.closure) else '_(Sim_Test)' if(args.sim) else ''}"
                
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
                Saved_Q = Save_Histograms_As_Images(ROOT_In=ROOT_Input, HISTO_NAME_In=HISTO_NAME, Format=args.file_format, SAVE=args.save_name, SAVE_prefix="Sim_Test_" if(args.sim) else "Mod_Test_" if(args.mod or args.mod_solo) else "Closure_Test_" if(args.closure) else "", TITLE=Standard_Histogram_Title_Addition)
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
    if(Saving_Q and ("ERROR" not in json_output_name) and args.make_json):
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
--modulation_solo (no compare) --> {args.mod_solo}
--closure (Full Closure Test)  --> {args.closure}
--data_compare                 --> {args.data}
--title  (added title)         --> {args.title}
--save_name                    --> {args.save_name if(args.save_name not in ['']) else None}
--EvGen                        --> {args.EvGen}
--q2_y   (Q2-y Bins)           --> {args.bins}
--z_pt   (z-pT Bins)           --> {args.z_pt}
--all_z_pt                     --> {args.all_z_pt}
--show_integral                --> {args.show_integral}
--normalize                    --> {args.normalize}
--file_format                  --> {args.file_format}
--single_file                  --> {args.single_file}
--verbose                      --> {args.verbose}
--use_errors                   --> {args.use_errors}
--use_errors_json              --> {args.use_errors_json}
--invert_errors                --> {args.invert_errors}
--no-fit                       --> {args.no_fit}
--fit_root                     --> {args.fit_root}
--remake_bin_by_bin            --> {args.remake}
--radiation_correction         --> {args.radiation_correction}
--fewer_images                 --> {args.fewer_images}
--legend_name_1                --> {args.legend_name_1}
--legend_name_2                --> {args.legend_name_2}
--make_json                    --> {args.make_json}
"""
if(args.compare):
    email_body = f"{email_body}--root_compare                 --> {args.root_compare}"
if(json_output_name):
    email_body = f"""{email_body}
    
JSON File Output:  {"(Not Saved)" if(not args.make_json) else ""}
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
print(email_body)


print(f"""{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

