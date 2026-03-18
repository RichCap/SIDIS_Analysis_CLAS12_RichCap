#!/usr/bin/env python3

import sys
import ROOT
import traceback
import os

from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetStatX(0.80)  # Set the right edge of the stat box (NDC)
ROOT.gStyle.SetStatY(0.45)  # Set the top edge of the stat box (NDC)
ROOT.gStyle.SetStatW(0.3)  # Set the width of the stat box (NDC)
ROOT.gStyle.SetStatH(0.2)  # Set the height of the stat box (NDC)

import argparse
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    p = argparse.ArgumentParser(description="Simple_RooUnfold_SelfContained.py analysis script:\n\tMeant for JUST doing the Unfolding Procedure before saving outputs to a ROOT file.",
                                formatter_class=RawDefaultsHelpFormatter)

    # saving / test modes
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save',
                   action='store_true',
                   dest='test',
                   help="Run full code but without saving any files.")
    p.add_argument('-r', '--root',
                   type=str,
                   default="Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root",
                   help="Name of ROOT output file to be saved (must specify the FULL file name).\n")
    
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Verbose print mode.")

    # smearing selection
    grp_smear = p.add_mutually_exclusive_group()
    grp_smear.add_argument('-smear', '--smear',
                           action='store_true',
                           help="Unfold with smeared Monte Carlo only.")
    grp_smear.add_argument('-no-smear', '--no-smear',
                           action='store_true',
                           help="Unfold with unsmeared Monte Carlo only.")

    # simulation / modulation / closure
    p.add_argument('-wa', '--weighed_acceptance',
                   action='store_true',
                   dest='weighed_acceptance',
                   help=f"Use to control the MC weights. If used, all closure tests will assume that the generated MC distributions should be unweighed (i.e., only acceptance weights are applied).\nUse with the '--single_file' option only.\n{color.RED}WARNING:{color.END} This option does not make sure the reconstructed MC is weighed only for acceptance (weight injections are controlled by the input file).")
    p.add_argument('-sim', '--simulation',
                   action='store_true',
                   dest='sim',
                   help="Use reconstructed MC instead of experimental data.")
    p.add_argument('-mod', '--modulation',
                   action='store_true',
                   dest='mod',
                   help="Use modulated MC files to create response matrices.")
    p.add_argument('-close', '--closure', 
                   action='store_true',
                   dest='closure',
                   help="Run Closure Test (unfold modulated MC with itself).")

    # fitting / output control
    p.add_argument('-f', '-fit', '--fit',
                   action='store_true',
                   dest='fit',
                   help="Enable fitting of plots. (Defaults to no fits)")
    
    p.add_argument('-rf', '-nf', '--remake_fit',
                   action='store_true',
                   dest='remake_fit',
                   help="Forces fitting of plots even if fits were already made (to be used with the '--Use_TTree' option).")
    
    p.add_argument('-N', '-csn', '--CrossSection_Norm',
                   action='store_true',
                   help="Apply Cross Section Normalization before fitting.\nNormalization includes division by bin width.")

    # kinematic comparison & proton modes
    p.add_argument('-tp', '--tag-proton', 
                   action='store_true',
                   dest='tag_proton',
                   help="Use 'Tagged Proton' files.")
    p.add_argument('-cp', '--cut-proton',
                   action='store_true',
                   dest='cut_proton',
                   help="Use 'Cut with Proton Missing Mass' files.")

    p.add_argument('-cib', '-CIB', '--Common_Int_Bins',
                   action='store_true',
                   help="If given then the code will only run the z-pT bins that have been designated to share the same ranges of z-pT (given by Common_Ranges_for_Integrating_z_pT_Bins).\nOtherwise, the code will run normally and include all z-pT bins for the given Q2-y bin.")

    p.add_argument('-bi', '-bayes-it', '--bayes_iterations',
                   type=int,
                   help="Number of Bayesian Iterations performed while Unfolding.\nDefaults to pre-set values in the code, but this argument allows them to be overwritten automatically.")

    p.add_argument('-nt', '-ntoys', '--Num_Toys',
                   type=int,
                   default=500,
                   help="Number of Toys used to estimate the unfolding errors (used with Unfolding_Histo.SetNToys(...)).")

    p.add_argument('-u1D', '--unfolding_1D',
                   action='store_true',
                   help="Run 1D unfolding only. Will still run normally as long as the `--unfolding_3D` is not passed.")
    p.add_argument('-u3D', '--unfolding_3D',
                   action='store_true',
                   help="Run 3D unfolding only. Will still run normally as long as the `--unfolding_1D` is not passed.")
    
    p.add_argument('-um', '--Unfold_Methods',
                   nargs="+",
                   type=str,
                   default=["Bayesian"],
                   choices=["(Bin)", "Bayesian"],
                   help=f"Acceptance Correction Method Options. Select 'Bayesian' for Full Unfolding or '(Bin)' for Bin-by-Bin Corrections.\n{color.BOLD}If RC or BC corrections are applied, this option will not limit you to just using the acceptance-corrected histograms—will just narrow which distributions the other corrections are applied to.\n{color.Error}WARNING: Only applies to runs where the unfolding was already done (i.e., when you are loading plots from a TTree or fitting).{color.END}\n")

    p.add_argument('-sec', '--run_sectors',
                   action='store_true',
                   help="Run Sector Unfolding.")
    p.add_argument('-secU', '--sectors_to_unfold',
                   default=["eS1o", "eS2o", "eS3o", "eS4o", "eS5o", "eS6o"],
                   help="Sectors to Unfold with the `--run_sectors` option.\n")

    p.add_argument('-aov', '--allow_other_variables',
                   action='store_true',
                   help="Allows for other variables to be unfolded other than the 'phi_t' distributions (such as Q2, y, etc. — does not impact the multidimensional unfolding).")
                   
    p.add_argument('-ti', '-title', '--title',
                   type=str,
                   help="Adds an extra title to the histograms.")

    p.add_argument('-evgen', '--EvGen',
                   action='store_true',
                   help="Runs with EvGen instead of clasdis files.")

    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut',
                   type=float,
                   default=0.0005,
                   help="Cut made on acceptance (as the minimum acceptance before a bin is removed from unfolding).")

    p.add_argument('-e', '--email',
                   action='store_true',
                   help="Sends an email to user when done running.")
    
    p.add_argument('-em', '--email_message',
                   type=str,
                   default="",
                   help="Extra email message to be added when given (use with `--email`).")

    p.add_argument('-sfin', '--single_file_input',
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_ZerothOrder.root",
                   help="Path to the Input file.\n")
    
    p.add_argument('-ut', '--Use_TTree',
                   action='store_true',
                   help="Load pre-made ROOT file (post-unfolding) for faster fits+RC Corrections. Control with the '--root' argument.")
    
    p.add_argument('-rc', '--Apply_RC',
                   action='store_true',
                   help="Apply RC Corrections.")
    
    p.add_argument('-bc', '--Apply_BC',
                   action='store_true',
                   help=f"Use the BC Corrections.\n{color.Error}WARNING:{color.END_R} As of 7/8/2026, this feature only works if the corrections are loaded in existing files (does not create new histograms by applying the corrections within this script).{color.END}\n")
    
    p.add_argument('-au', '--Add_Uncertainties',
                   action='store_true',
                   help="Adds systematic uncertainties to histograms before fitting.")

    p.add_argument('-sj', '--save_json',
                   action="store_true",
                   help="Save Fit Parameters to JSON file.")
    
    p.add_argument('-oj', '--old_json',
                   action='store_true',
                   help="Include the older JSON file format when saving with '--save_json'.\n(Will still use the newer format as backup)\n")

    # positional Q2-xB bin arguments
    p.add_argument('bins',
                   nargs='*',
                   metavar='BIN',
                   help="List of Q2-y (or Q2-xB) bin indices to run. '0' means all bins.")

    return p.parse_args()

def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()
    if(hasattr(obj, "asym_errors")): # Also write the 'asym_errors' attribute
        obj_asym_errors = obj.asym_errors
        existing_attr = tfile.GetListOfKeys().FindObject(obj_asym_errors.GetName())
        if(existing_attr):
            tfile.Delete(f"{obj_asym_errors.GetName()};*")  # delete all versions of the object
        obj_asym_errors.Write()

import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    ansi_html_map = {'\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "", '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "", '\033[0m': ""}
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

def Update_Email(args, update_name="", update_message="", verbose_override=False):
    update_email = ""
    if(update_message not in [""]):
        update_email = f"""{update_message}
{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}"""
    elif(update_name not in [""]):
        update_email = f"""
{color.BCYAN}{update_name}{color.END_B} is done running...{color.END}
{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}

"""
    if(update_email not in [""]):
        args.email_message = f"{args.email_message}\n{update_email}"
        if(args.verbose or verbose_override):
            print(update_email)

def Construct_Email(args, Crashed=False, Warning=False, final_count=None):
    start_time = args.timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    if(final_count is None):
        end_time, total_time, rate_line = args.timer.stop(return_Q=True)
    else:
        end_time, total_time, rate_line = args.timer.stop(count_label="Histograms", count_value=final_count, return_Q=True)
    args_list = ""
    for name, value in vars(args).items():
        if(str(name) in ["email", "email_message", "timer", "root", "run_sectors", "sector_list", "sectors_to_unfold", "allow_other_variables", "bins", "sim", "mod", "closure", "weighed_acceptance", "single_file_input", "unfolding_1D", "unfolding_3D", "no_smear", "smear", "standard_histogram_title_addition"]):
            continue
        if((str(name) in ["num_5D_increments_used_to_slice"]) and (not args.Run_5D_Unfold)):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'Simple_RooUnfold_SelfContained.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

Input File:
\t{args.single_file_input}
Output File:
\t{args.root}

{args.email_message}

Arguments:{f'''
--{'unfolding_1D (1D Unfolding Only)':<50s}--> {args.unfolding_1D}''' if(not args.unfolding_3D) else ''}
--{'unfolding_3D (3D Unfolding Only)':<50s}--> {args.unfolding_3D}
--{'run_sectors':<50s}--> {args.run_sectors}
--{'sectors_to_unfold':<50s}--> {"None" if(not args.run_sectors) else args.sectors_to_unfold}
--{'allow_other_variables (for unfolding)':<50s}--> {args.allow_other_variables}
--{'simulation (unfolding synthetic data)':<50s}--> {args.sim}
--{'modulation (data unfolded with modulated MC)':<50s}--> {args.mod}
--{'closure  (modulated MC unfolded with itself)':<50s}--> {args.closure}
--{'weighed_acceptance (use acceptance weights only)':<50s}--> {args.weighed_acceptance}{args_list}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'Simple_RooUnfold_SelfContained.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'Simple_RooUnfold_SelfContained.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
    print(f"\n\n\n\n{color.BOLD}{color_bg.YELLOW}EMAIL MESSAGE TO SEND:{color.END}\n\n{email_body}\n")
    if(Warning):
        print(f"\n\n{color.BOLD}CONTNUE RUNNING...{color.END}\n\n")
    elif(not Crashed):
        print(f"""{color.BGREEN}{color_bg.YELLOW}
    \t                                   \t   
    \tThis code has now finished running.\t   
    \t                                   \t   {color.END}
    
    """)
    else:
        print(f"""{color.BYELLOW}{color_bg.RED}
    \t                                   \t   
    \t       This code has CRASHED!      \t   
    \t                                   \t   {color.END}
    
    """)

def Crash_Report(args, crash_message="The Code has CRASHED!", continue_run=False):
    if(continue_run):
        crash_message = f"\n{color.BYELLOW}ERROR WARNING!{color.END}\n{crash_message}\n\nCONTINUED RUNNING...\n"
    else:
        crash_message = f"\n{color.Error}CRASH WARNING!{color.END}\n{crash_message}\n"
    print(crash_message, file=sys.stderr)
    args.email_message = f"{args.email_message}\n{crash_message}\n"
    Construct_Email(args, Crashed=(not continue_run), Warning=continue_run)
    if(not continue_run):
        sys.exit(1)
    else:
        print(f"\n\n{color.ERROR}WILL CONTINUE RUNNING THROUGH THE ERROR{color.END}\n\n")

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

###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################
from functools import partial
import numpy as np
def func_fit(params, x, y):
    A, B, C = params
    y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi))) for xi in x]
    return sum((y_pred[i] - y[i])**2 for i in range(len(x)))
def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
    N = len(x0)
    simplex = [x0]
    for i in range(N):
        point = list(x0)
        point[i] = x0[i] * 1.1
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
    x_data, y_data = [], []
    try:
        for ii in range(0, Histo.GetNbinsX(), 1):
            x_data.append(Histo.GetBinCenter(ii))
            y_data.append(Histo.GetBinContent(ii))
        # Perform optimization using the Nelder-Mead method
        initial_guess = [np.mean(y_data), 1, 1]  # Initial guess for A, B, C
        optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)
        # Extract the optimized parameters
        A_opt, B_opt, C_opt = optim_params
    except:
        print(f"{color.Error}Full_Calc_Fit(...) ERROR:{color.END}\n{traceback.format_exc()}\n\n{color.Error}ERROR is with 'Histo' = {Histo}\n{color.END}")
        A_opt, B_opt, C_opt = "Error", "Error", "Error"
    return [A_opt, B_opt, C_opt]
###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################


#######################################################################
#####==========#####   Drawing Histogram Options   #####==========#####
#######################################################################
def Draw_Histo_Color_and_Range(Histo, Method="rdf", Hist_or_Line="Histo"):
    color_set = root_color.Black
    if(Method in ["rdf", "Experimental"]):
        color_set = root_color.Blue
    if(Method in ["mdf", "MC REC"]):
        color_set = root_color.Red
    if(Method in ["gdf", "gen", "MC GEN"]):
        color_set = root_color.Green
    if(Method in ["tdf", "true"]):
        color_set = root_color.Cyan
    if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
        color_set = root_color.Brown
    if(Method in ["bayes", "bayesian", "Bayesian"]):
        color_set = root_color.Teal
    if(Method in ["Background"]):
        color_set = root_color.Black
    if(Method in ["SVD"]):
        color_set = root_color.Pink
    Histo.SetLineColor(color_set)
    if(Hist_or_Line in ["Histo"]):
        Histo.SetMarkerColor(color_set)
        Histo.GetYaxis().SetRangeUser(0, 1.5*Histo.GetBinContent(Histo.GetMaximumBin()))
    return Histo
###========###  Setting Method Title   ###========###
def Set_Method_Title(Method, args):
    Method_Title = ""
    if(Method in ["rdf", "Experimental"]):
        Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not args.sim) else "]{(MC REC - Pre-Unfolded)}"])
    if(Method in ["mdf", "MC REC"]):
        Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
    if(Method in ["gdf", "gen", "MC GEN"]):
        Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
    if(Method in ["tdf", "true"]):
        Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
    if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
        Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
    if(Method in ["bayes", "bayesian", "Bayesian"]):
        Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
    if(Method in ["Acceptance", "Background"]):
        Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
    return Method_Title
###========###  Setting Method Title   ###========###
#######################################################################
#####==========#####   Drawing Histogram Options   #####==========#####
#######################################################################

##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default", MC_BGS_1D="None", args="args"):
############################################################################################################
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Original)   #####=====#####=====#####=====###
    if(Method in ["SVD"]):
        print(f"\n{color.Error}ERROR: SVD UNFOLDING IS NO LONGER SUPPORTED...{color.END}\n")
        args.timer.time_elapsed()
        return "ERROR"
#####=====#####=====#####=====#####     End of Method: "SVD" (Original)    #####=====#####=====#####=====###
############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
############################################################################################################
    elif((Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]) or (Response_2D in ["N/A", "None", "Error"])):
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.PURPLE}Bin-by-Bin{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        if(Response_2D in ["N/A", "None", "Error"]):
            print(f"{color.Error}WARNING: NOT Using Response Matrix for unfolding{color.END}")
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        clean_name = str(Name_Print).replace("(Data-Type='mdf'), ", "")
        print(f"\t{color.BOLD}Acceptance Correction of Histogram:{color.END}\n\t{clean_name}")
        del clean_name
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            if(MC_BGS_1D not in ["None"]):
                # Add the background back into the acceptance calculation
                Bin_Acceptance.Add(MC_BGS_1D)
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Acceptance.SetTitle(str(Bin_Acceptance.GetTitle()).replace("Reconstructed (MC) Distribution of", "Bin-by-Bin Acceptance for"))
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Corrected")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Unfolded.Sumw2()
            
            cut_criteria = args.Min_Allowed_Acceptance_Cut

            if(any(Sector_Cut in str(Name_Print) for Sector_Cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"])):
                print(f"{color.RED}NOTE: Reducing Acceptance Cut criteria by 50% for Sector Cut plots{color.END}")
                cut_criteria = 0.5*args.Min_Allowed_Acceptance_Cut
            for ii in range(0, Bin_Acceptance.GetNbinsX() + 1):
                if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
                    if(Bin_Acceptance.GetBinContent(ii) != 0):
                        print(f"{color.RED}\nBin {ii} had a very low acceptance...\n\t(cut_criteria = {cut_criteria})\n\t(Bin_Content  = {Bin_Acceptance.GetBinContent(ii)}){color.END}")
                    # Bin_Unfolded.SetBinError(ii,   Bin_Unfolded.GetBinContent(ii) + Bin_Unfolded.GetBinError(ii))
                    Bin_Unfolded.SetBinError(ii,   0)
                    Bin_Unfolded.SetBinContent(ii, 0)
            print(f"{color.BCYAN}Finished {color.PURPLE}Bin-by-Bin{color.END_B}{color.CYAN} Unfolding Procedure.{color.END}")
            args.timer.time_elapsed()
            if(Response_2D in ["N/A", "None", "Error"]):
                return [Bin_Unfolded, Bin_Acceptance]
        except:
            print(f"\n{color.Error}FAILED TO CORRECT A HISTOGRAM (Bin-by-Bin)...\nERROR:\n{color.END}{traceback.format_exc()}")
            args.timer.time_elapsed()
            return "ERROR"
############################################################################################################
#####=====#####=====#####=====#####     End of Method:  "Bin-by-Bin"     #####=====#####=====#####=====#####
############################################################################################################
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====###
############################################################################################################
    if((("RooUnfold" in str(Method)) or (str(Method) in ["Default"]) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])) and (Response_2D not in ["N/A", "None", "Error"])):
        print(f"{color.BCYAN}Starting {color.UNDERLINE}{color.GREEN}RooUnfold{color.END_B}{color.CYAN} Unfolding Procedure...{color.END}")
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        clean_name = str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")
        if((str(Method) in ["RooUnfold", "RooUnfold_bayes", "Default"]) and ("MultiDim_" in str(Name_Main))):
            Update_Email(args, update_message=f"\n\t{color.BOLD}Began Unfolding Histogram:{color.END}\n\t{clean_name}", verbose_override=True)
        else:
            print(f"\t{color.BOLD}Unfolding Histogram:{color.END}\n\t{clean_name}")
        del clean_name
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width
        ExREAL_1D.GetXaxis().SetRange(0,     nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,     nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0,   nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0,   nBins_CVM)     # Response Matrix (Y axis --> REC)
        if(MC_BGS_1D != "None"):
            MC_BGS_1D.GetXaxis().SetRange(0, nBins_CVM)     # MC Background Subtracted Distribution
        if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name_Main)):
            Response_2D_Input_Title = f"{Response_2D.GetTitle()};{Response_2D.GetYaxis().GetTitle()};{Response_2D.GetXaxis().GetTitle()}"
            Response_2D_Input       = ROOT.TH2D(f"{Response_2D.GetName()}_Flipped", str(Response_2D_Input_Title), Response_2D.GetNbinsY(), MinBinCVM, MaxBinCVM, Response_2D.GetNbinsX(), MinBinCVM, MaxBinCVM)
            # Use the following code if the input Response Matrix plots the generated events on the x-axis
            # # The RooUnfold library takes Response Matrices which plot the true/generated events on the y-axis and the measured/reconstructed events on the x-axis
            ##==============##============================================##==============##
            ##==============##=====##     Flipping Response_2D     ##=====##==============##
            ##=========##   Generated Bins       ##=====##
            for gen_bin in range(0, nBins_CVM + 1):
                ##=====##   Reconstructed Bins   ##=====##
                for rec_bin in range(0, nBins_CVM + 1):
                    Res_Value = Response_2D.GetBinContent(gen_bin,    rec_bin)
                    Res_Error = Response_2D.GetBinError(gen_bin,      rec_bin)
                    Response_2D_Input.SetBinContent(rec_bin, gen_bin, Res_Value)
                    Response_2D_Input.SetBinError(rec_bin,   gen_bin, Res_Error)
            ##==============##=====##     Flipped Response_2D      ##=====##==============##
            ##==============##============================================##==============##
            # Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = f"{Response_2D.GetTitle()};{Response_2D.GetXaxis().GetTitle()};{Response_2D.GetYaxis().GetTitle()}"
            Response_2D_Input       = Response_2D
        del Response_2D

        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, f"{str(Response_2D_Input.GetName()).replace('_Flipped', '')}_RooUnfoldResponse_Object", Response_2D_Input_Title)
                if(MC_BGS_1D != "None"):
                    # Background Subtraction Method 1: Fill the Response_RooUnfold object explicitly with the content of a background histogram with the Fake() function
                    for rec_bin in range(0, nBins_CVM + 1):
                        rec_val = MC_BGS_1D.GetBinCenter(rec_bin)
                        rec_con = MC_BGS_1D.GetBinContent(rec_bin)
                        Response_RooUnfold.Fake(rec_val, w=rec_con)
                    # Background Subtraction Method 2:
                        # Should be possible to add MC_BGS_1D to MC_REC_1D to combine those plots where MC_REC_1D != the projection of Response_2D_Input since MC_REC_1D would (in this case) still contain events which would be identifified as background in MC_BGS_1D
                        # This is likely the better approach computationally, though some testing needs to be done to get the execution working correctly
##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if("svd" in str(Method)):
                    Unfold_Title = "RooUnfold (SVD)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    ##=====##  SVD Regularization Parameter  ##=====##
                    Reg_Par = 13
                    ##=====##  SVD Regularization Parameter  ##=====##
                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)
                elif(("bbb" in str(Method)) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)
                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} Unfolding Procedure...{color.END}")
                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)
                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print(f"\t{color.RED}Method '{color.BOLD}{Method}{color.END_R}' is unknown/undefined...{color.END}")
                        print(f"\t{color.RED}Defaulting to using the {color.BGREEN}{Unfold_Title}{color.END_R} method to unfold...{color.END}")
                    else:
                        print(f"\t{color.CYAN}Using {color.BGREEN}{Unfold_Title}{color.END_C} method to unfold...{color.END}")

                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = (10 if(not args.closure) else 10) if(("Multi_Dim" not in str(Name_Main)) or (("Multi_Dim_z_pT_Bin" in str(Name_Main)) or ("MultiDim_z_pT" in str(Name_Main)))) else 4
                    if(args.pass_version not in ["", "Pass 1"]):
                        bayes_iterations += 3
                    if("MultiDim_Q2_y_z_pT_phi_h" in str(Name_Main)):
                        # 5D Unfolding
                        bayes_iterations = 4
                        print(f"{color.BOLD}Performing 5D Unfolding with {color.UNDERLINE}{bayes_iterations}{color.END_B} iteration(s)...{color.END}")
                    if(args.bayes_iterations):
                        if(args.bayes_iterations != bayes_iterations):
                            bayes_iterations = args.bayes_iterations
                            print(f"{color.BOLD}Performing Unfolding with {color.UNDERLINE}{bayes_iterations}{color.END_B} iteration(s)...{color.END}")
                    else:
                        args.bayes_iterations = bayes_iterations
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)
                    Unfolding_Histo.SetNToys(args.Num_Toys)

##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                if(any(method in str(Method) for method in ["bbb", "svd", "inv"]) or (Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"])):
                    Unfolded_Histo = Unfolding_Histo.Hunfold()
                else:
                    Unfolded_Histo = Unfolding_Histo.Hunfold(ROOT.RooUnfold.kCovToys)
                
                for bin_rec in range(0, MC_REC_1D.GetNbinsX() + 1):
                    if(MC_REC_1D.GetBinContent(bin_rec) == 0):
                        Unfolded_Histo.SetBinError(bin_rec, Unfolded_Histo.GetBinContent(bin_rec) + Unfolded_Histo.GetBinError(bin_rec))

                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    Bin_Acceptance = MC_REC_1D.Clone()
                    Bin_Acceptance.Sumw2()
                    Bin_Acceptance.Divide(MC_GEN_1D)
                for bin_acceptance in range(0, Bin_Acceptance.GetNbinsX() + 1):
                    if((all(cut not in str(Name_Main_Print) for cut in ["_eS1o", "_eS2o", "_eS3o", "_eS4o", "_eS5o", "_eS6o"]) and (Bin_Acceptance.GetBinContent(bin_acceptance) < args.Min_Allowed_Acceptance_Cut)) or (Bin_Acceptance.GetBinContent(bin_acceptance) < 0.5*args.Min_Allowed_Acceptance_Cut)):
                        # Condition above applied normal Acceptance Cuts only when the Sector Cuts are NOT present but will always apply the cuts if the acceptance is less than 50% of the normal set value
                        # Unfolded_Histo.SetBinError(bin_acceptance,   Unfolded_Histo.GetBinContent(bin_acceptance) + Unfolded_Histo.GetBinError(bin_acceptance))
                        Unfolded_Histo.SetBinError(bin_acceptance,   0)
                        Unfolded_Histo.SetBinContent(bin_acceptance, 0)
                        
                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                if((str(Method) in ["RooUnfold", "RooUnfold_bayes", "Default"]) and ("MultiDim_" in str(Name_Main))):
                    Update_Email(args, update_message="\tFinished Unfolding the histogram at:")
                    args.timer.time_elapsed()
                print(f"{color.BCYAN}Finished {color.GREEN}{Unfold_Title}{color.END_B}{color.CYAN} Unfolding Procedure.\n{color.END}")
                if(Method not in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
                    return [Unfolded_Histo, Response_RooUnfold]
                else:
                    return [Unfolded_Histo, Bin_Acceptance]
            except:
                print(f"\n{color.Error}FAILED TO UNFOLD A HISTOGRAM (RooUnfold)...\nERROR:\n{color.END}{traceback.format_exc()}")
        else:
            print(f"{color.RED}Unequal Bins...{color.END}")
            print(f"nBins_CVM = {nBins_CVM}")
            print(f"MC_REC_1D.GetNbinsX() = {MC_REC_1D.GetNbinsX()}")
            print(f"MC_GEN_1D.GetNbinsX() = {MC_GEN_1D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsX() = {Response_2D.GetNbinsX()}")
            print(f"Response_2D.GetNbinsY() = {Response_2D.GetNbinsY()}")
            args.timer.time_elapsed()
            return "ERROR"
    else:
        print(f"Procedure for Method '{Method}' has not yet been defined...")
        args.timer.time_elapsed()
        return "ERROR"
    print(f"\n{color.Error}ERROR: DID NOT RETURN A HISTOGRAM YET...{color.END}\n")
    args.timer.time_elapsed()
    return "ERROR"
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##

######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################
import re
def Histogram_Name_Def(out_print, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="All", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args="args"):
    Pattern_List = []
    Pattern_Histo_General = r"\(Histo-Group='([^']+)'"
    Pattern_Data_Type     = r"\(Data-Type='([^']+)'"
    Pattern_Cut_Type      = r"\(Data-Cut='([^']+)'"
    Pattern_Smear_Type    = r"\(Smear-Type='([^']+)'"
    Pattern_Q2_y_Bin      = r"\[Q2-y-Bin=([^,]+),"
    Pattern_Var_1         = r"\(Var-D1='([^']+)'"
    Pattern_Var_2         = r"\(Var-D2='([^']+)'"
    # Pattern_Var_3         = r"\(Var-D3='([^']+)'"
    
    if(Histo_General  == "Find"):
        Pattern_List.append(Pattern_Histo_General)
    else:
        Pattern_List.append(Histo_General)
    if(Data_Type      == "Find"):
        Pattern_List.append(Pattern_Data_Type)
    else:
        Pattern_List.append(Data_Type)
    if(Cut_Type       == "Find"):
        Pattern_List.append(Pattern_Cut_Type)
    elif(Cut_Type not in ["Skip", "skip"]):
        Pattern_List.append(Cut_Type)
    if(Smear_Type     == "Find"):
        Pattern_List.append(Pattern_Smear_Type)
    else:
        Pattern_List.append(Smear_Type)
        
    if(Bin_Extra      == "Default"):
        Pattern_List.append(str("".join(["Q2_y_Bin_", str(Q2_y_Bin) if(Q2_y_Bin != 0) else "All"])) if(Q2_y_Bin not in ["Find"]) else Pattern_Q2_y_Bin)
        Pattern_List.append("".join(["z_pT_Bin_", str(z_pT_Bin) if(z_pT_Bin != 0) else "All"]))
    elif(Bin_Extra not in ["Skip", "skip"]):
        Pattern_List.append("".join(["Kinematic_Bin_", str(Bin_Extra) if(Bin_Extra != 0) else "All"]))
        
    if(Variable       == "Default"):
        Pattern_List.append(Pattern_Var_1)
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    elif(Variable     in ["Find", "FindAll", "FindOnly"]):
        Pattern_List = [Pattern_Var_1]
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    else:
        Pattern_List.append(Variable)
        
    if(Q2_y_Bin in ["FindOnly"]):
        Pattern_List = [Pattern_Q2_y_Bin]
        
    Name_Output = ""
    for pattern in Pattern_List:
        if(pattern in [r"\(Histo-Group='([^']+)'", r"\(Data-Type='([^']+)'", r"\(Data-Cut='([^']+)'", r"\(Smear-Type='([^']+)'", r"\[Q2-y-Bin=([^,]+),", r"\(Var-D1='([^']+)'", r"\(Var-D2='([^']+)'"]):
            match = re.search(pattern, out_print.replace("''", "' '"))
            if(match):
                histo_group = match.group(1)
                if((histo_group == " ")):
                    histo_group = "''"
                if(pattern == Pattern_Smear_Type):
                    histo_group = "".join(["SMEAR=", "".join(["'", str(histo_group), "'"]) if(histo_group != "''") else str(histo_group)]) 
                if(pattern == Pattern_Q2_y_Bin):
                    histo_group = f"Q2_y_Bin_{histo_group}"
        else:
            histo_group = pattern
            if(pattern == Smear_Type):
                histo_group = "".join(["SMEAR=", pattern if(pattern != "") else "''"])
        Name_Output = "".join([Name_Output, "_(" if(str(Name_Output) != "") else "(", str(histo_group), ")"])
        
    if((Variable in ["Find", "FindAll", "FindOnly"]) and (")_(" not in str(Name_Output))):
        Name_Output = Name_Output.replace("(", "")
        Name_Output = Name_Output.replace(")", "")
    
    Name_Output = str(Name_Output.replace("cut_Complete_SIDIS_Proton",    "Proton"))
    Name_Output = str(Name_Output.replace("cut_Complete_SIDIS_Integrate", "Integrate"))
    if((args.closure or args.mod or args.sim) and (")_(" in str(Name_Output)) and all(extra not in str(Name_Output) for extra in ["Mod_Test", "Closure_Test", "Sim_Test"])):
        Name_Output = f"{Name_Output}_({'Mod_Test' if(args.mod) else 'Closure_Test' if(args.closure) else 'Sim_Test'})"
    
    return Name_Output
######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################

##################################################################################################################################################################
##==========##==========## Function for Creating the Integrated z-pT Bin Histograms     ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################
def Bin_Widths_future_function(args):
    # Run the following code whenever changes are made to the z-pT bins in order to get the correct (new) values for 'Area_of_z_pT_Bins'
    Area_of_z_pT_Bins = {}
    for Q2_y_Bin     in range(1, 18):
        Area_of_z_pT_Bins[f"{Q2_y_Bin}"] = 0
        for z_pT_Bin in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin)[0]):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD="Y_bin")):
                continue
            else:
                z_Max, z_Min, pTMax, pTMin = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT_Bin, Q2_y_Bin_Num=Q2_y_Bin)
                Area_of_z_pT_Bins[f"{Q2_y_Bin}"]           +=       abs((z_Max - z_Min)*(pTMax - pTMin))
                Area_of_z_pT_Bins[f"{Q2_y_Bin}_{z_pT_Bin}"] = round(abs((z_Max - z_Min)*(pTMax - pTMin)), 6)
        Area_of_z_pT_Bins[f"{Q2_y_Bin}"] = round(Area_of_z_pT_Bins[f"{Q2_y_Bin}"], 6)
    print(f"Area_of_z_pT_Bins = {Area_of_z_pT_Bins}")

from Binning_Dictionaries import Full_Bin_Definition_Array #, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D
def Bin_Area_by_Widths_Calc(args, Q2_y_Bin=1, z_pT_Bin=1, phi_t_bin=15):
    # phi_t_bin should be 15 for the default phi_t plots since while the scale is applied to the full histogram, the per bin ∆phi_t is just the normal bin width
        # Update phi_t_bin whenever the bin sizes are changed
        # If the scale is applied to a 2D histogram of the other variables (i.e., integrated over the phi_t variable), then phi_t_bin should be set to 360
    Bin_Area = {"q2yTotal": 0, "zpTTotal": 0, "dQ2": 0, "d_y": 0, "dphi_t": phi_t_bin}
    for q2y_bin in range(1, 18):
        if(str(Q2_y_Bin) not in ["0", "All", str(q2y_bin)]):
            continue
        Bin_Area[f"Q2-y={q2y_bin}"] = {"q2yTotal": 0, "zpTTotal": 0, "dQ2": 0, "d_y": 0, "d_z": 0, "dpT": 0}
        Q2max, Q2min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={q2y_bin}, Q2-y']
        Bin_Area[f"Q2-y={q2y_bin}"]["q2yTotal"] += abs(Q2max - Q2min)*abs(y_max - y_min)
        Bin_Area[f"Q2-y={q2y_bin}"]["dQ2"] += abs(Q2max - Q2min)
        Bin_Area[f"Q2-y={q2y_bin}"]["d_y"] += abs(y_max - y_min)
        Bin_Area["q2yTotal"] += abs(Q2max - Q2min)*abs(y_max - y_min)
        Bin_Area["dQ2"] += abs(Q2max - Q2min)
        Bin_Area["d_y"] += abs(y_max - y_min)
        for zpT_bin in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2y_bin)[0]):
            if((skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpT_bin, BINNING_METHOD="Y_bin")) or (str(z_pT_Bin) not in ["0", "All", str(zpT_bin)])):
                continue
            z_max, z_min, pTmax, pTmin = Full_Bin_Definition_Array[f'Q2-y={q2y_bin}, z-pT={zpT_bin}']
            Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"] = {"q2yTotal": Bin_Area[f"Q2-y={q2y_bin}"]["q2yTotal"], "zpTTotal": abs(z_max - z_min)*abs(pTmax - pTmin), "d_z": abs(z_max - z_min), "dpT": abs(pTmax - pTmin)}
            Bin_Area[f"Q2-y={q2y_bin}"]["zpTTotal"]       += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["zpTTotal"]
            Bin_Area[f"Q2-y={q2y_bin}"]["d_z"]            += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["d_z"]
            Bin_Area[f"Q2-y={q2y_bin}"]["dpT"]            += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["dpT"]
            Bin_Area["zpTTotal"]                          += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["zpTTotal"]
    Bin_Width_Area_Scale = Bin_Area["q2yTotal"]*Bin_Area["zpTTotal"]*Bin_Area["dphi_t"]
    if(args.verbose):
        print(f"Bin Area (∆Q2∆y∆z∆pT∆phi_t) for Bin ({Q2_y_Bin}-{z_pT_Bin}) = {Bin_Width_Area_Scale}")
    return Bin_Width_Area_Scale, Bin_Area

def ApplyCS_Norm(args, Histo, Q2_y_Bin, z_pT_Bin, List_of_All_Histos_For_Unfolding={}):
    # Histo.SetLineWidth(3)
    if(args.CrossSection_Norm):
        Bin_Width_Area_Scale, Bin_Area = Bin_Area_by_Widths_Calc(args, Q2_y_Bin=Q2_y_Bin, z_pT_Bin=z_pT_Bin, phi_t_bin=15)
        if(args.verbose):
            print(f"Scaling Histogram: {color.BOLD}{Histo.GetName()}{color.END} by bin widths/areas.\nFull list of bin widths/areas =\n{Bin_Area}\n")
        if(Bin_Width_Area_Scale != 0.0):
            Histo.Scale(1.0/Bin_Width_Area_Scale)
        else:
            Crash_Report(args, crash_message=f"The Scaling Histogram by Bin Widths Code would have CRASHED! Was trying to normalize: '{Histo.GetName()}'. Bin Area = 0", continue_run=False)
        Histo.GetYaxis().SetTitle("#frac{#sigma}{dQ^{2}dydzdP_{T}d#phi_{h}}")
    return Histo.Clone(f"{Histo.GetName()}_(Normalized)")
    # if(args.Normalize):
    #     if(args.verbose):
    #         print(f"Normalizing Histogram: {Histo.GetName()}")
    #     try:
    #         Integrated_Bins_Histo = List_of_All_Histos_For_Unfolding[str(str(Histo.GetName()).replace(f"(Q2_y_Bin_{Q2_y_Bin})", "(Q2_y_Bin_All)")).replace(f"(z_pT_Bin_{z_pT_Bin})", "(z_pT_Bin_All)")]
    #         integral = Integrated_Bins_Histo.Integral(0, Integrated_Bins_Histo.GetNbinsX() + 1)
    #         if(integral != 0.0):
    #             Histo.Scale(1.0/integral)
    #         Histo.GetYaxis().SetTitle(f"Normalized {Histo.GetYaxis().GetTitle()}")
    #     except:
    #         Crash_Report(args, crash_message=f"The Normalize Histogram Code would have CRASHED! Was trying to normalize: '{Histo.GetName()}'. (Attempting the simple normalization...)\nERROR MESSAGE:\n\n{traceback.format_exc()}", continue_run=True)
    #         try:
    #             integral = Histo.Integral(0, Histo.GetNbinsX() + 1)
    #             if(integral != 0.0):
    #                 Histo.Scale(1.0/integral)
    #             Histo.GetYaxis().SetTitle(f"Normalized {Histo.GetYaxis().GetTitle()}")
    #         except:
    #             Crash_Report(args, crash_message=f"The Normalize Histogram Code would have CRASHED! Was trying to normalize: '{Histo.GetName()}'.\nERROR MESSAGE:\n\n{traceback.format_exc()}", continue_run=False)
    # # if((args.Bin_Width or args.Normalize) and args.save_single_file):
    # #     print(f"{color.BOLD}Updating ROOT file{color.END}")
    # #     List_of_All_Histos_For_Unfolding[f"{Histo.GetName()}_(Normalized)"] = Histo.Clone(f"{Histo.GetName()}_(Normalized)")
    # #     try:
    # #         List_of_All_Histos_For_Unfolding = Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding)
    # #     except:
    # #         Crash_Report(args, crash_message=f"{color.Error}The Code has CRASHED! Failed to finish saving the histograms.\n{color.END_R}ERROR:\n{str(traceback.format_exc())}{color.END}")
    # # return Histo, List_of_All_Histos_For_Unfolding

##################################################################################################################################################################
##==========##==========## Function for Creating the Integrated z-pT Bin Histograms     ##==========##==========##==========##==========##==========##==========##
##################################################################################################################################################################


################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
from Phi_h_Fit_Parameters_Initialize import special_fit_parameters_set
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default", Special="Normal", args="args", Allow_Normalization=False):
    if(Allow_Normalization and args.CrossSection_Norm and (len(Special) == 2)):
        q2y_Bin, zpT_Bin = Special # (Most of) the normalization functions require the value for the kinematic bin numbers
        if("_(Normalized)" in str(Histo_To_Fit.GetName())):
            print(f"{color.Error}Normalization was already applied to {color.END_B}'{Histo_To_Fit.GetName()}'{color.END_R} (skipping right to fitting){color.END}")
        else:
            # if(args.verbose):
            print(f"{color.BBLUE}Applying Normalization for Differential Cross Section before fitting...{color.END}")
            Histo_To_Fit = ApplyCS_Norm(args, Histo_To_Fit, Q2_y_Bin=q2y_Bin, z_pT_Bin=zpT_Bin)
    elif(Allow_Normalization and args.CrossSection_Norm):
        print(f"{color.Error}Cannot Normalize {color.END_B}'{Histo_To_Fit.GetName()}'{color.Error} without the kinematic bin numbers (were attempted to be given as: {color.END_B}'{Special}'{color.Error}){color.END}")
    if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true", "RC_Bin", "RC_Bayesian", "BC_Bayesian", "BC_RC_Bayesian"]) and (Fitting in ["default", "Default"]) and args.fit):
        A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
        fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"

        Fitting_Function = ROOT.TF1(f"Fitting_Function_of_{Histo_To_Fit.GetName()}_{str(Method).replace(' ', '_')}", str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")

        fit_range_lower = 0
        fit_range_upper = 360
        # Number of bins in the histogram
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
            Fitting_Function = Draw_Histo_Color_and_Range(Fitting_Function, Method, "Line")
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
                            if((Q2_y_Bin_Special, z_pT_Bin_Special, "BC") in special_fit_parameters_set):
                                bin_settings = special_fit_parameters_set[(Q2_y_Bin_Special, z_pT_Bin_Special, "BC")]
                            elif((Q2_y_Bin_Special, z_pT_Bin_Special, "RC") in special_fit_parameters_set):
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
                        print(f"\n{color.Error}ERROR in Fitting_Phi_Function() for 'Special' arguement...\n{color.END_B}Traceback:\n{str(traceback.format_exc())}{color.END}\n")
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
        print(f"\n\n\n{color.Error}ERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...{color.END}\n\n\n")
        return "ERROR"
################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################


################################################################################################################################################################################################################################################
##==========##==========##        3D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Multi3D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_z_pT_Bin_Y_bin_phi_t", Smear="", Q2_y_Bin_Select="All", Out_Option="Save", Fitting_Input="default", args="args"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    if((str(Method) not in ["rdf", "gdf"]) or ((str(Method) not in ["gdf"]) and args.sim)):
        if(((args.smearing_options in ["both", "no_smear"]) and (Smear in [""])) or ((args.smearing_options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
        else:
            print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
            return "Error"
    elif(Smear in [""]):
        print(f"\n{color.BLUE}Running Multi3D_Slice(...){color.END}\n")
    else:
        print(f"\n\n{color.Error}Wrong Smearing option for Multi3D_Slice(...){color.END}\n\n")
        return "Error"
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_z_pT_Bin_Y_bin_phi_t" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName = {color.END}{Name}\nMulti3D_Slice() should be used on the histograms with the 'MultiDim_z_pT_Bin_Y_bin_phi_t' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_z_pT_Bin_Y_bin_phi_t"]):
            print(f"{color.RED}ERROR in Multi3D_Slice(): Not set up for other variables (yet)\n{color.END}Variable = {Variable}\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###========###  Setting Method Title   ###========###
        Method_Title = Method_Title = Set_Method_Title(Method, args)
        if((Method in ["rdf", "Experimental"]) and (not args.sim)):
            Variable = Variable.replace("_smeared", "")
            Smear    = ""
        if(Method in ["gdf", "gen", "MC GEN", "tdf", "true"]):
            Variable = Variable.replace("_smeared", "")
            Smear    = ""
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{3-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_3D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and args.fit):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((args.pass_version not in [""]) and (args.pass_version not in str(Title))):
            Title = f"#splitline{{{Title}}}{{{root_color.Bold}{{{args.pass_version}}}}}"
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_3D_Histo", Data_Type=str(Method), Cut_Type="Skip" if(all(cut_checks not in str(Name) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=str(Smear), Q2_y_Bin=Q2_y_Bin_Select, z_pT_Bin="MultiDim_3D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default", args=args)
            if(str(Method) in ["tdf", "true"]):
                Name = str(Name.replace("mdf", "tdf")).replace("gdf", "tdf")
        if(str(Q2_y_Bin_Select) not in ["0", "All"]):
            if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT=1", End_Bins_Name="3D_Bins")):
                raise TypeError(f"Convert_All_Kinematic_Bins(Start_Bins_Name='Q2-y={Q2_y_Bin_Select}, z-pT=1', End_Bins_Name='3D_Bins') == ERROR")
            else:
                z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Select)[1]
                for z_pT in range(0, z_pT_Range+1):
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_Select, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin", Common_z_pT_Range_Q=args.Common_Int_Bins)):
                        continue
                    Name_Out  = str(Name.replace("MultiDim_3D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
                    Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                    Bin_Title = Bin_Title.replace("Common_Int", "Integrated (Over Common Range)")
                    Title_Out = str(Title.replace("MultiDim_3D_Var_Info", Bin_Title))
                    if(z_pT not in [0]):
                        if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT}", End_Bins_Name="3D_Bins")):
                            break
                        else:
                            Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT}",       End_Bins_Name="3D_Bins")
                            End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y_Bin_Select}, z-pT={z_pT+1}",     End_Bins_Name="3D_Bins")
                            if(End___phi_h_bin in ["ERROR"]):
                                End___phi_h_bin = Start_phi_h_bin + phi_h_Binning[2]
                            if(((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]) or skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_Select, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin", Common_z_pT_Range_Q=args.Common_Int_Bins)):
                                continue
                    else:
                        Name_All                = Name_Out
                        Output_Histos[Name_All] = ROOT.TH1D(Name_All, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                        continue
                    Output_Histos[Name_Out]     = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                    #######################################################################
                    #####==========#####   Filling Sliced Histogram    #####==========#####
                    #######################################################################
                    ii_bin_num = Start_phi_h_bin
                    phi_Content, phi___Error = {}, {}
                    for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                        phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                        phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
                    while(ii_bin_num < End___phi_h_bin):
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            if(Histo_Cut is not False):
                                bin_ii = Histo.FindBin(ii_bin_num + 1)
                                MultiDim_cut_num = Histo_Cut.GetBinContent(bin_ii)
                                MultiDim_cut_err = Histo_Cut.GetBinError(bin_ii)
                                if((MultiDim_cut_num == 0) or (MultiDim_cut_num <= MultiDim_cut_err)):
                                    phi_Content[phi_bin + 0.5*phi_h_Binning[3]] += 0
                                    phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0 # Histo.GetBinContent(bin_ii) + Histo.GetBinError(bin_ii)
                                else:
                                    phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                    phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                            else:
                                bin_ii = Histo.FindBin(ii_bin_num + 1)
                                phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                            ii_bin_num += 1
                    for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                        Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],             phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                        Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                        Current_All_Error = Output_Histos[Name_All].GetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]))
                        Output_Histos[Name_All].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],             phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                        Output_Histos[Name_All].SetBinError(Output_Histos[Name_All].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(Current_All_Error**2 + phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                    #######################################################################
                    #####==========#####   Filling Sliced Histogram    #####==========#####
                    #######################################################################
                    for name in [Name_All, Name_Out]:
                        if((name in [Name_All]) and (z_pT not in [z_pT_Range-3, z_pT_Range-2, z_pT_Range-1, z_pT_Range, z_pT_Range+1])):
                            continue # Do not have to set the integrated z-pT bin plot more than once at the end of the z_pT loop
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        Output_Histos[name] = Draw_Histo_Color_and_Range(Output_Histos[name], Method)
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        if(Fitting_Input in ["default", "Default"] and args.fit):
                            Output_Histos[name], Unfolded_Fit_Function[name.replace("MultiDim_3D_Histo", "Fit_Function")], Fit_Chisquared[name.replace("MultiDim_3D_Histo", "Chi_Squared")], Fit_Par_A[name.replace("MultiDim_3D_Histo", "Fit_Par_A")], Fit_Par_B[name.replace("MultiDim_3D_Histo", "Fit_Par_B")], Fit_Par_C[name.replace("MultiDim_3D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[name], Method=Method, Fitting="default", Special=[int(Q2_y_Bin_Select), int(z_pT)], args=args)
                        #######################################################################

        ################################################################################
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    except:
        print(f"{color.Error}Multi3D_Slice(...) ERROR:\n{color.END}{traceback.format_exc()}\n")
        return "Error"
################################################################################################################################################################################################################################################
##==========##==========##        3D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Multi5D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="", Out_Option="Save", Fitting_Input="default", args="args"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    if(str(Method) not in ["rdf", "gdf"]):
        if(((args.smearing_options in ["both", "no_smear"]) and (Smear in [""])) or ((args.smearing_options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(color.BLUE, "\nRunning Multi5D_Slice(...)\n", color.END)
        else:
            print(color.Error, "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE,      "\nRunning Multi5D_Slice(...)\n", color.END)
    else:
        print(color.Error,     "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
        return "Error"
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name)):
                print(color.RED, "ERROR: WRONG TYPE OF HISTOGRAM\nName =", color.END, Name, "\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_Q2_y_z_pT_phi_h"]):
            print(color.RED, "ERROR in Multi5D_Slice(): Not set up for other variables (yet)", color.END, "\nVariable =", Variable, "\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###========###  Setting Method Title   ###========###
        Method_Title = Set_Method_Title(Method, args)
        if((Method in ["rdf", "Experimental"]) and (not args.sim)):
            Variable = Variable.replace("_smeared", "")
            Smear    = ""
        if(Method in ["gdf", "gen", "MC GEN", "tdf", "true"]):
            Variable = Variable.replace("_smeared", "")
            Smear    = ""
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{5-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_5D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and args.fit):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((args.pass_version not in [""]) and (args.pass_version not in str(Title))):
            Title = f"#splitline{{{Title}}}{{{root_color.Bold}{{{args.pass_version}}}}}"
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ################################################################################
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip" if(all(cut_checks not in str(Name) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default", args=args)
            if(str(Method) in ["tdf", "true"]):
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
        for Q2_y in args.Q2_y_Bin_List:
            if(Q2_y not in ["0", "All"]):
                if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                    break
                else:
                    z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
                    for z_pT in range(0, z_pT_Range+1):
                        Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y) if(str(Q2_y) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                        Title_Out = str(Title.replace("MultiDim_5D_Var_Info", Bin_Title))
                        if(z_pT not in [0]):
                            if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                                break
                            else:
                                Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}",       End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT+1}",     End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if(End___phi_h_bin in ["ERROR"]):
                                    End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if(((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]) or skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin")):
                                    continue
                        else:
                            Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1",                End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                            End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1",         End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                        Name_Out = str(Name.replace("MultiDim_5D_Q2_y_Bin_Info",     str(Q2_y) if(str(Q2_y) not in ["0", "All"]) else "All"))
                        Name_Out = str(Name_Out.replace("MultiDim_5D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
                        Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        ii_bin_num,  ii_LastNum  = Start_phi_h_bin, Start_phi_h_bin
                        phi_Content, phi___Error = {}, {}
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
                        while(ii_bin_num < End___phi_h_bin):
                            OverFlow_Con = False
                            if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
                                # Conditions for combining all z-pT bins
                                Q2_y_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="Q2-y") if(ii_bin_num != 0) else 1
                                Q2_y_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="Q2-y")
                                z_pT_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="z-pT") if(ii_bin_num != 0) else 1
                                z_pT_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="z-pT")
                                if((z_pT_bin_0 != z_pT_bin_1) and (Q2_y_bin_0 == Q2_y_bin_1)):
                                    if(ii_LastNum + 1 == ii_bin_num):
                                        OverFlow_Con = True
                                    ii_LastNum = ii_bin_num
                                elif(Q2_y_bin_0 != Q2_y_bin_1):
                                    ii_LastNum = Start_phi_h_bin
                                elif(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_bin_1, Z_PT_BIN=z_pT_bin_1, BINNING_METHOD="Y_bin")):
                                    OverFlow_Con = True
                                    ii_LastNum = ii_bin_num
                            if(OverFlow_Con):
                                ii_bin_num += 1
                                continue
                            else:
                                for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                                    if(Histo_Cut is not False):
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        MultiDim_cut_num = Histo_Cut.GetBinContent(bin_ii)
                                        MultiDim_cut_err = Histo_Cut.GetBinError(bin_ii)
                                        if((MultiDim_cut_num == 0) or (MultiDim_cut_num <= MultiDim_cut_err)):
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] += 0
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0 # Histo.GetBinContent(bin_ii) + Histo.GetBinError(bin_ii)
                                        else:
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                                    else:
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                        phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],            phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                            Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        Output_Histos[name] = Draw_Histo_Color_and_Range(Output_Histos[name], Method)
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        if(Fitting_Input in ["default", "Default"] and args.fit):
                            Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("MultiDim_5D_Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("MultiDim_5D_Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[int(Q2_y), int(z_pT)], args=args)
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
            
        ################################################################################
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    except:
        print(f"{color.Error}Multi5D_Slice(...) ERROR:\n{color.END}{traceback.format_exc()}\n")
        return "Error"
################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Rebuild_Matrix_5D(List_of_Sliced_Histos, Standard_Name, Increment=4, Title="Default"):
    Num__Bins, Min_Range, Max_Range = Find_Bins_From_Histo_Name(Standard_Name)
    Slicing_Name = f"{Standard_Name}_Slice_SLICE-NUM_(Increment='{Increment}')"
    print("\nRunning Rebuild_Matrix_5D(...)")
    Num_Slices   = int(Num__Bins/Increment)
    for test in ["1", str(Num_Slices)]:
        if(Slicing_Name.replace("SLICE-NUM", str(test)) not in List_of_Sliced_Histos):
            missing_name = Slicing_Name.replace("SLICE-NUM", str(test))
            print(f"{color.Error}ERROR IN Rebuild_Matrix_5D(...): {color.END_R}'Slicing_Name' is missing from 'List_of_Sliced_Histos'{color.END_B}\n\tSlicing_Name = {missing_name}\n\tList_of_Sliced_Histos = {List_of_Sliced_Histos}")
            return "ERROR"
    Histo_Title = Title if(Title not in ["Default"]) else "".join([str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetXaxis().GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetYaxis().GetTitle())])
    Rebuilt_5D_Matrix = ROOT.TH2D(str(Standard_Name), str(Histo_Title), Num__Bins, Min_Range, Max_Range, Num__Bins, Min_Range, Max_Range)
    X_Bin_5D = 0
    for slice_num in range(1, Num_Slices + 1):
        Histo_Add     = List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", str(slice_num))]
        X_Bin_5D     += -1
        for     x_bin in range(0, Histo_Add.GetNbinsX() + 1):
            X_Bin_5D +=  1
            for y_bin in range(0, Histo_Add.GetNbinsY() + 1):                
                bin_content = Histo_Add.GetBinContent(x_bin, y_bin)
                bin_error   = Histo_Add.GetBinError(x_bin,   y_bin)
                for ii in range(1, int(bin_content)+1):
                    Rebuilt_5D_Matrix.Fill(X_Bin_5D-1, y_bin-1)
    print("Finished running Rebuild_Matrix_5D(...)\n")
    return Rebuilt_5D_Matrix
################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################

################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def New_Version_of_File_Creation(Histogram_List_All, Out_Print_Main, Response_2D="", ExREAL_1D="", MC_REC_1D="", MC_GEN_1D="", ExTRUE_1D="N/A", Smear_Input="", Q2_Y_Bin="All", Z_PT_Bin="All", MC_BGS_1D="None", args="args"):
    try:
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################
        if("Response" not in str(Out_Print_Main) and (Response_2D not in ["N/A", "None", "Error"])):
            print(f"\n\n\n{color.Error}ERROR IN New_Version_of_File_Creation()...\n{color.END_R}This function is meant to just handle the 'Response_Matrix' Histograms (for Unfolding)\nFlawed Input was: {Out_Print_Main}{color.END}\n\n")
            return Histogram_List_All
        if(type(Histogram_List_All) is not dict):
            print(f"\n\n\n{color.Error}ERROR IN New_Version_of_File_Creation()...\n{color.END_R}This function requires that 'Histogram_List_All' be set as a dict to properly handle the outputs.\n{color.Error}Flawed Input was:\n{color.END_R}Histogram_List_All = {color.ERROR}{Out_Print_Main}{color.END}\n\n")
            return Histogram_List_All
        #######################################################################
        #####==========#####  Checking Inputs for Errors   #####==========#####
        #######################################################################

        Variable_Input = Histogram_Name_Def(Out_Print_Main, Variable="FindAll", args=args)
        # print(f"Variable_Input = {Variable_Input}")
        Allow_Fitting  = ("phi_t" in str(Variable_Input)) or ("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input))

        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        try:
            Bin_Method_Histograms        = Unfold_Function(Response_2D,  ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin", MC_BGS_1D=MC_BGS_1D, args=args)
            Bin_Unfolded, Bin_Acceptance = Bin_Method_Histograms
        except:
            print(f"{color.Error}ERROR IN BIN UNFOLDING ('Bin_Method_Histograms'):\n{color.END_R}{traceback.format_exc()}{color.END}")

        if(("sec" not in Variable_Input) or (Response_2D not in ["N/A", "None", "Error"])):
            try:
                if("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input)):
                    # Temporary restriction on 5D unfolding as method is being tested for computational requirements (copy this line to see other restriction)
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Bin",             MC_BGS_1D=MC_BGS_1D, args=args))[0]
                else:
                    RooUnfolded_Bayes_Histos = (Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="RooUnfold_bayes", MC_BGS_1D=MC_BGS_1D, args=args))[0]
            except:
                print(f"{color.Error}ERROR IN RooUnfold Bayesian METHOD:\n{color.END_R}{traceback.format_exc()}{color.END}")
        else:
            print(f"\n{color.Error}Not running bayesian unfolding method...{color.END}\n")
            RooUnfolded_Bayes_Histos = Bin_Method_Histograms[0]
        #####################################################################
        #####==========#####      Unfolding Histos       #####==========#####
        #####################################################################
        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========##### (3D) MultiDim Histos (New)  #####==========#####
        if(("MultiDim_z_pT_Bin" in str(Variable_Input)) and (Z_PT_Bin in ["All", "Integrated", "Common_Int", -2, -1, 0])):
            # The MultiDim_z_pT_Bin z-pT Plots should only be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All", "Integrated", -1 or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###=============================================###        
                Multi_Dim_ExREAL_1D                                                                                                  = Multi3D_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf",           Variable=Variable_Input, Smear=Smear_Input if(args.sim) else "", Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                Multi_Dim_MC_REC_1D                                                                                                  = Multi3D_Slice(Histo=MC_REC_1D,                             Title="norm", Name=Out_Print_Main, Method="mdf",           Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                if(args.fit and Allow_Fitting):
                    Multi_Dim_MC_GEN_1D,     Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Multi3D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin, args=args)
                else:
                    Multi_Dim_MC_GEN_1D                                                                                              = Multi3D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                if(MC_BGS_1D not in ["None"]):
                    Multi_Dim_MC_BGS_1D                                                                                              = Multi3D_Slice(Histo=MC_BGS_1D,                             Title="norm", Name=Out_Print_Main, Method="Background",    Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                if(ExTRUE_1D not in ["N/A"]):
                    if(args.fit and Allow_Fitting):
                        Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Multi3D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin, args=args)
                    else:
                        Multi_Dim_ExTRUE_1D                                                                                          = Multi3D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",           Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                ###=============================================###
                ###========###   Before Unfolding    ###========###
                ###========###   After Unfolding     ###========###
                ###=============================================###
                Multi_Dim_Bin_Acceptance                                                                                             = Multi3D_Slice(Histo=Bin_Acceptance,                        Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                if(args.fit and Allow_Fitting):
                    Multi_Dim_Bin_Histo,     Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Multi3D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin, args=args)
                    Multi_Dim_Bay_Histo,     Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Multi3D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Complete", Fitting_Input="Default", Q2_y_Bin_Select=Q2_Y_Bin, args=args)
                else:
                    Multi_Dim_Bin_Histo                                                                                              = Multi3D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                    Multi_Dim_Bay_Histo                                                                                              = Multi3D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                         Out_Option="Histos",   Fitting_Input="Off",     Q2_y_Bin_Select=Q2_Y_Bin, args=args)[0]
                ###=============================================###
                ###========###   After Unfolding     ###========###
                ###=============================================###
        #####==========#####   (5D) MultiDim Histos      #####==========#####
        elif(("MultiDim_Q2_y_z_pT_phi_h" in str(Variable_Input)) and (Z_PT_Bin in ["All", "Integrated", "Common_Int", -2, -1, 0]) and (Q2_Y_Bin in ["All", 0])):
            # The 5D MultiDim Histograms should only be able to run if Q2_Y_Bin and Z_PT_Bin are equal to "All", "Integrated", -1 or 0 (all kinematic binning is done through these slices)
            ###=============================================###
            ###========###   Before Unfolding    ###========###
            ###=============================================###
            Multi_Dim_ExREAL_1D                                                                                                  = Multi5D_Slice(Histo=ExREAL_1D,                             Title="norm", Name=Out_Print_Main, Method="rdf",        Variable=Variable_Input, Smear=Smear_Input if(args.sim) else "", Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            Multi_Dim_MC_REC_1D                                                                                                  = Multi5D_Slice(Histo=MC_REC_1D,                             Title="norm", Name=Out_Print_Main, Method="mdf",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            if(args.fit and Allow_Fitting):
                Multi_Dim_MC_GEN_1D,     Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Multi5D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",        Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", args=args)
            else:
                Multi_Dim_MC_GEN_1D                                                                                              = Multi5D_Slice(Histo=MC_GEN_1D,                             Title="norm", Name=Out_Print_Main, Method="gdf",        Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            if(MC_BGS_1D not in ["None"]):
                Multi_Dim_MC_BGS_1D                                                                                              = Multi5D_Slice(Histo=MC_BGS_1D,                             Title="norm", Name=Out_Print_Main, Method="Background", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            if(ExTRUE_1D not in ["N/A"]):
                if(args.fit and Allow_Fitting):
                    Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Multi5D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",        Variable=Variable_Input, Smear="",                               Out_Option="Complete", Fitting_Input="Default", args=args)
                else:
                    Multi_Dim_ExTRUE_1D                                                                                          = Multi5D_Slice(Histo=ExTRUE_1D,                             Title="norm", Name=Out_Print_Main, Method="tdf",        Variable=Variable_Input, Smear="",                               Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            ###=============================================###
            ###========###   Before Unfolding    ###========###
            ###========###   After Unfolding     ###========###
            ###=============================================###
            Multi_Dim_Bin_Acceptance                                                                                             = Multi5D_Slice(Histo=Bin_Acceptance,                        Title="norm", Name=Out_Print_Main, Method="Acceptance", Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            if(args.fit and Allow_Fitting):
                Multi_Dim_Bin_Histo,     Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Multi5D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", args=args)
                Multi_Dim_Bay_Histo,     Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Multi5D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Complete", Fitting_Input="Default", args=args)
            else:
                Multi_Dim_Bin_Histo                                                                                              = Multi5D_Slice(Histo=[Bin_Unfolded,             MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bin",        Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
                Multi_Dim_Bay_Histo                                                                                              = Multi5D_Slice(Histo=[RooUnfolded_Bayes_Histos, MC_REC_1D], Title="norm", Name=Out_Print_Main, Method="Bayesian",   Variable=Variable_Input, Smear=Smear_Input,                      Out_Option="Histos",   Fitting_Input="Off", args=args)[0]
            ###=============================================###
            ###========###   After Unfolding     ###========###
            ###=============================================###
        #####==========#####      Multi_Dim Histos       #####==========#####
        #####==========#####      Fitting 1D Histo       #####==========#####
        elif("phi" in Variable_Input):
            if(args.fit and Allow_Fitting):
                MC_GEN_1D,                   Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=MC_GEN_1D,                Method="gdf",   Special=[Q2_Y_Bin, Z_PT_Bin], args=args)
                Bin_Unfolded,                Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Bin_Unfolded,             Method="bbb",   Special=[Q2_Y_Bin, Z_PT_Bin], args=args)
                RooUnfolded_Bayes_Histos,    Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RooUnfolded_Bayes_Histos, Method="bayes", Special=[Q2_Y_Bin, Z_PT_Bin], args=args)
                if(ExTRUE_1D not in ["N/A"]):
                    ExTRUE_1D,               Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=ExTRUE_1D,                Method="tdf",   Special=[Q2_Y_Bin, Z_PT_Bin], args=args)
        #####==========#####      Fitting 1D Histo       #####==========#####

        ##################################################################################
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ##################################################################################
        Histo_Name_General = Histogram_Name_Def(out_print=Out_Print_Main, Histo_General="1D", Data_Type="METHOD", Cut_Type="Skip" if(all(cut_checks not in str(Out_Print_Main) for cut_checks in ["cut_Complete_SIDIS_Proton", "cut_Complete_SIDIS_Integrate"])) else "Find", Smear_Type=Smear_Input, Q2_y_Bin=Q2_Y_Bin, z_pT_Bin=Z_PT_Bin, Bin_Extra="Default", Variable=Variable_Input, args=args)
        if("cut_Complete_SIDIS_Proton" in str(Histo_Name_General)):
            print(f"\n\n\n{color.Error}'cut_Complete_SIDIS_Proton' is still in 'Histo_Name_General' ({Histo_Name_General}){color.END}\n\n")
            Histo_Name_General = str(Histo_Name_General.replace("cut_Complete_SIDIS_Proton", "Proton"))
        if("sec'-[" in Out_Print_Main):
            Histo_Name_General = Histo_Name_General.replace("((", "(")
            for sec in [1, 2, 3, 4, 5, 6]:
                if(f"sec'-[{sec}]" in Out_Print_Main):
                    Histo_Name_General = Histo_Name_General.replace("sec)_(phi_t))", f"sec_{sec})_(phi_t)")
                    break
        if("sec_smeared'-[" in Out_Print_Main):
            Histo_Name_General = Histo_Name_General.replace("((", "(")
            for sec in [1, 2, 3, 4, 5, 6]:
                if(f"sec_smeared'-[{sec}]" in Out_Print_Main):
                    # print(f"\nBefore: Histo_Name_General = {Histo_Name_General}")
                    Histo_Name_General = Histo_Name_General.replace("sec_smeared)_(phi_t_smeared))", f"sec_{sec})_(phi_t)")
                    # print(f"After:  Histo_Name_General = {Histo_Name_General}\n")
                    break
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "rdf")).replace("Smear", "''")]               = ExREAL_1D.Clone(str(Histo_Name_General.replace("METHOD",   "rdf")).replace("Smear", "''"))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf"))]                                      = MC_REC_1D.Clone(str(Histo_Name_General.replace("METHOD",   "mdf")))
        if(hasattr(Response_2D, 'Clone') and callable(getattr(Response_2D, 'Clone'))):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")] = Response_2D.Clone(str(Histo_Name_General.replace("METHOD", "mdf")).replace("1D",    "Response_Matrix"))
        else:
            Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "mdf")).replace("1D", "Response_Matrix")] = Response_2D
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "gdf")).replace("Smear", "''")]               = MC_GEN_1D.Clone(str(Histo_Name_General.replace("METHOD",   "gdf")).replace("Smear", "''"))
        if(MC_BGS_1D not in ["None"]):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "Background"))]                               = MC_BGS_1D.Clone(str(Histo_Name_General.replace("METHOD",   "Background")))

        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin"))]                                      = Bin_Unfolded.Clone(str(Histo_Name_General.replace("METHOD",             "Bin")))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Acceptance"))]                               = Bin_Acceptance.Clone(str(Histo_Name_General.replace("METHOD",           "Acceptance")))
        Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian"))]                                 = RooUnfolded_Bayes_Histos.Clone(str(Histo_Name_General.replace("METHOD", "Bayesian")))
        if(ExTRUE_1D not in ["N/A"]):
            Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf"))]                                   = ExTRUE_1D.Clone(str(Histo_Name_General.replace("METHOD", "tdf")))
            if((args.fit and Allow_Fitting) and (not (("Multi" in str(Variable_Input)) and (Z_PT_Bin in ["All", 0])))):
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function")] = Unfolded_TDF_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Chi_Squared")]  = Chi_Squared_TDF # .Clone(str(Histo_Name_General.replace("METHOD",           "tdf")).replace("1D", "Chi_Squared"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_A")]    = TDF_Fit_Par_A # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_A"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_B")]    = TDF_Fit_Par_B # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_B"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD", "tdf")).replace("1D", "Fit_Par_C")]    = TDF_Fit_Par_C # .Clone(str(Histo_Name_General.replace("METHOD",             "tdf")).replace("1D", "Fit_Par_C"))
                
        ###==========###         Normal/1D Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        ################################################################### ########################################################################################################################################################################################################################################################################################################################
        ###==========###         Multi-Dim Histos          ###==========### ########################################################################################################################################################################################################################################################################################################################
        if(("Multi" in str(Variable_Input)) and (Z_PT_Bin in ["All", 0])):
            # Only the Multi_Dim z-pT Plots should be able to run if Q2_Y_Bin and Z_PT_Bin do not equal "All" or 0
            if(("z_pT_Bin" in str(Variable_Input)) or (Q2_Y_Bin in ["All", 0])):
                if(ExTRUE_1D not in ["N/A"]):
                    if(args.fit and Allow_Fitting):
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C, Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C, Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C, Multi_Dim_ExTRUE_1D, Unfolded_TDF_Fit_Function, Chi_Squared_TDF, TDF_Fit_Par_A, TDF_Fit_Par_B, TDF_Fit_Par_C]
                    else:
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D,                                                                                          Multi_Dim_Bin_Histo,                                                                                          Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo,                                                                                          Multi_Dim_ExTRUE_1D]
                else:
                    if(args.fit and Allow_Fitting):
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D, Unfolded_GEN_Fit_Function, Chi_Squared_GEN, GEN_Fit_Par_A, GEN_Fit_Par_B, GEN_Fit_Par_C, Multi_Dim_Bin_Histo, Unfolded_Bin_Fit_Function, Chi_Squared_Bin, Bin_Fit_Par_A, Bin_Fit_Par_B, Bin_Fit_Par_C, Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo, Unfolded_Bay_Fit_Function, Chi_Squared_Bay, Bay_Fit_Par_A, Bay_Fit_Par_B, Bay_Fit_Par_C]
                    else:
                        histos_list_loop = [Multi_Dim_ExREAL_1D, Multi_Dim_MC_REC_1D, Multi_Dim_MC_GEN_1D,                                                                                          Multi_Dim_Bin_Histo,                                                                                          Multi_Dim_Bin_Acceptance, Multi_Dim_Bay_Histo]
                if(MC_BGS_1D not in ["None"]):
                    histos_list_loop.append(Multi_Dim_MC_BGS_1D)
                try:
                    for histos_list in histos_list_loop:
                        try:
                            for name in histos_list:
                                Histogram_List_All[name] = histos_list[name]
                        except:
                            print(f"{color.Error}ERROR IN ADDING TO Histogram_List_All (while looping within an item in histos_list):\n{color.END_R}{traceback.format_exc()}{color.END}")
                            print("histos_list =", histos_list)
                            # print("histos_list_loop =", histos_list_loop)
                except:
                    print(f"{color.Error}ERROR IN ADDING TO Histogram_List_All (while looping through items in histos_list):\n{color.END_R}{traceback.format_exc()}{color.END}")
        ###==========###         Multi_Dim Histos          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        elif("phi" in Variable_Input):
            if(args.fit and Allow_Fitting):
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")).replace("Smear", "''")] = Unfolded_GEN_Fit_Function.Clone(str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Function")).replace("Smear", "''"))
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Chi_Squared")).replace("Smear",  "''")] = Chi_Squared_GEN
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_A")).replace("Smear",    "''")] = GEN_Fit_Par_A
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_B")).replace("Smear",    "''")] = GEN_Fit_Par_B
                Histogram_List_All[str(str(Histo_Name_General.replace("METHOD", "gdf")).replace("1D",      "Fit_Par_C")).replace("Smear",    "''")] = GEN_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Function")]                         = Unfolded_Bin_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Chi_Squared")]                          = Chi_Squared_Bin
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_A")]                            = Bin_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_B")]                            = Bin_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bin")).replace("1D",      "Fit_Par_C")]                            = Bin_Fit_Par_C

                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Function")]                         = Unfolded_Bay_Fit_Function.Clone(str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Function"))
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Chi_Squared")]                          = Chi_Squared_Bay
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_A")]                            = Bay_Fit_Par_A
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_B")]                            = Bay_Fit_Par_B
                Histogram_List_All[str(Histo_Name_General.replace("METHOD",     "Bayesian")).replace("1D", "Fit_Par_C")]                            = Bay_Fit_Par_C
        ###==========###         Other Histo Fits          ###==========### #######################################################################################################################################################################################################################################################################################################################
        ################################################################### #######################################################################################################################################################################################################################################################################################################################
        ###==============###   Adding Histos to Histogram_List_All    ###==============###
        ##################################################################################
        return Histogram_List_All
    except:
        print(f"{color.Error}ERROR IN New_Version_of_File_Creation(...):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
        return Histogram_List_All
################################################################################################################################################################################################################################################
##==========##==========##     Function For Creating All Unfolding Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################

import fcntl
def Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding):
    print("\n\nCounting Total Number of/Saving collected histograms...")
    fit_list_tags = ["Chi_Squared", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]
    def write_vec(tfile, name, py_list):
        if(py_list is None):
            print(f"{color.Error}WARNING:{color.END} Fit list '{name}' is None (skipping)")
            return
        if(not isinstance(py_list, (list, tuple))):
            print(f"{color.Error}WARNING:{color.END} Fit list '{name}' is type={type(py_list)} (expected list/tuple; skipping)")
            return
        if(len(py_list) == 0):
            print(f"{color.Error}WARNING:{color.END} Fit list '{name}' is empty (skipping)")
            return
        vec = ROOT.TVectorD(len(py_list))
        for ii, val in enumerate(py_list):
            vec[ii] = float(val)
        keyname = f"TVectorD_{name}" if(not args.EvGen) else f"TVectorD_{name}_EvGen"
        existing = tfile.GetListOfKeys().FindObject(keyname)
        if(existing):
            if(getattr(args, "verbose", False)):
                print(f"{color.BBLUE}Deleting:{color.END} '{keyname};*' (already exists)")
            tfile.Delete(f"{keyname};*")
        tfile.WriteObject(vec, keyname)
    if(not args.test):
        print(f"{color.BBLUE}Saving to: {color.BGREEN}{args.root}{color.END}")
        lock_file_path = args.root + ".lock"
        with open(lock_file_path, "w+") as lock_fd:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            output_file = ROOT.TFile(args.root, "UPDATE")
            File_Name_Lists = [str(args.single_file_input)]
            File_Name_Tlist = ROOT.TList()
            File_Name_Tlist.SetName("Latest_List_of_File_Names")
            for s in File_Name_Lists:
                File_Name_Tlist.Add(ROOT.TObjString(s))
            safe_write(File_Name_Tlist, output_file)
            for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
                try:
                    obj = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
                    if((any(tag in List_of_All_Histos_For_Unfolding_ii for tag in fit_list_tags)) and isinstance(obj, (list, tuple))):
                        write_vec(output_file, List_of_All_Histos_For_Unfolding_ii, obj)
                    elif(type(obj) is list):
                        Temp_Tlist = ROOT.TList()
                        Temp_Tlist.SetName(f"TList_of_{List_of_All_Histos_For_Unfolding_ii}" if(not args.EvGen) else f"TList_of_{List_of_All_Histos_For_Unfolding_ii}_EvGen")
                        for s in obj:
                            Temp_Tlist.Add(ROOT.TObjString(str(s) if(not args.EvGen) else f"{str(s)}_EvGen"))
                        safe_write(Temp_Tlist, output_file)
                    else:
                        if(type(obj) is not ROOT.TObjString):
                            obj.SetName(List_of_All_Histos_For_Unfolding_ii)
                            safe_write(obj, output_file)
                except:
                    Crash_Report(args, crash_message=f"The Save Code would have CRASHED! Was trying to save: '{List_of_All_Histos_For_Unfolding_ii}'. (Was allowed to finish running anyway...)\nERROR MESSAGE:\n\n{traceback.format_exc()}", continue_run=True)
            output_file.Close()
        print(f"\n{color.BCYAN}Done Saving!{color.END}")
    else:
        print(f"{color.PINK}Would be saving to: {color.BCYAN}{args.root}{color.END}")
        for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
            print(f"\n{List_of_All_Histos_For_Unfolding_ii} --> {type(List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii])}")
    print(f"\nFinal Count = {len(List_of_All_Histos_For_Unfolding)}\n")
    args.timer.time_elapsed()
    return List_of_All_Histos_For_Unfolding

def Construct_Run_Info(args):
    Run_Info = {"Start_Time": args.timer.start_find(return_Q=True)}
    for name, value in vars(args).items():
        if(str(name) in ["timer", "sector_list", "sectors_to_unfold", "allow_other_variables", "bins", "smear", "standard_histogram_title_addition"]):
            continue
        Run_Info[name] = value
    return Run_Info

import json
from pathlib import Path
def Save_Fit_Pars_To_JSON(args, List_of_All_Histos_For_Unfolding, cor_type="Bayesian"):
    MainFileName = str(str(args.root).replace("Unfolded_Histos_From_", "")).replace(".root", "")
    if("/" in str(MainFileName)):
        MainFileName = str(MainFileName.split("/")[-1])
    var_type  =  "phi_t" if(args.unfolding_1D) else "MultiDim_z_pT_Bin_Y_bin_phi_t"
    args.json_name = f"Fit_Pars_from_Simple_RooUnfold_SelfContained{f'_using_{MainFileName}' if(MainFileName not in ['']) else ''}.json"
    Common_Key = f"Fit_Pars_from_{'3D' if(args.unfolding_3D) else '1D'}_{cor_type}"
    json_path = Path(args.json_name)
    Fit_Pars_JSON = {Common_Key: {}, "Meta_Data_of_Last_Run": Construct_Run_Info(args)}
    for key_name in List_of_All_Histos_For_Unfolding:
        if(all(pars not in str(key_name) for pars in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"])):
            continue
        if(any(selections not in str(key_name) for selections in [var_type, "SMEAR=Smear"])):
            continue
        keys_split = key_name.split(")_(")
        par = keys_split[0]
        method = keys_split[1]
        # smear_line = keys_split[2]
        q2_y_bin = keys_split[3]
        z_pt_bin = keys_split[4]
        var = keys_split[5]
        par = par.replace("(Fit_Par_", "")
        var = var.replace(")", "")
        if(cor_type not in [method]):
            # print(f"{color.RED}Wrong Correction Method{color.END}")
            continue
        q2_y_bin = q2_y_bin.replace("Q2_y_Bin_", "")
        if(str(q2_y_bin) not in args.Q2_y_Bin_List):
            continue
        z_pt_bin = z_pt_bin.replace("z_pT_Bin_", "")
        val, err = List_of_All_Histos_For_Unfolding[key_name]
        if(args.old_json):
            Fit_Pars_JSON[f"{par}_{q2_y_bin}_{z_pt_bin}"]     = val
            Fit_Pars_JSON[f"{par}_ERR_{q2_y_bin}_{z_pt_bin}"] = err
        bin_key = f"(Q2_y_Bin_{q2_y_bin})-(z_pT_Bin_{z_pt_bin})"
        if(len(keys_split) != 6):
            extra_keys = f"{Common_Key}_({''.join(keys_split[6:])}"
            if(extra_keys not in Fit_Pars_JSON):
                Fit_Pars_JSON[extra_keys] = {}
            if(bin_key not in Fit_Pars_JSON[extra_keys]):
                Fit_Pars_JSON[extra_keys][bin_key] = {}
            Fit_Pars_JSON[extra_keys][bin_key][f"Fit_Par_{par}"]     = val
            Fit_Pars_JSON[extra_keys][bin_key][f"Fit_Par_{par}_ERR"] = err
        else:
            if(bin_key not in Fit_Pars_JSON[Common_Key]):
                Fit_Pars_JSON[Common_Key][bin_key] = {}
            Fit_Pars_JSON[Common_Key][bin_key][f"Fit_Par_{par}"]     = val
            Fit_Pars_JSON[Common_Key][bin_key][f"Fit_Par_{par}_ERR"] = err
    if(args.test):
        print(f"\n{color.BCYAN}Would save JSON: {color.END_B}{args.json_name}{color.END}")
        print(f"{color.BCYAN}New/updated entries in this batch: {color.END_B}{len(Fit_Pars_JSON)}{color.END}")
        return args, Fit_Pars_JSON
    existing_json = {}
    if(json_path.exists()):
        try:
            with open(json_path, "r") as f:
                loaded = json.load(f)
            if(isinstance(loaded, dict)):
                existing_json = loaded
            else:
                Update_Email(args, update_message=f"{color.BYELLOW}WARNING:{color.END} Existing JSON is not a dict. Will overwrite with a dict: {str(json_path)}", verbose_override=True)
        except:
            Crash_Report(args, crash_message=f"{color.Error}WARNING: Failed reading existing JSON.{color.END} Will overwrite: {str(json_path)}\nERROR MESSAGE:\n\n{traceback.format_exc()}", continue_run=True)
    existing_json.update(Fit_Pars_JSON)
    tmp_path = json_path.with_suffix(json_path.suffix + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(existing_json, f, indent=4)
    tmp_path.replace(json_path)
    print(f"\n{color.BBLUE}Saved Fit Parameters JSON as {color.BGREEN}{str(json_path)}{color.BBLUE} (total entries now = {len(existing_json)}){color.END}\n")
    Update_Email(args, update_message=f"{color.BCYAN}Done Saving JSON File.{color.END}", verbose_override=True)
    return args, Fit_Pars_JSON

def main_start():
    args = parse_args()
    silence_root_import()
    args.pass_version = "Pass 2"
    args.sim = args.sim or args.closure
    args.mod = args.mod and (not args.closure)
    args.smearing_options = "no_smear" if(args.no_smear) else "smear" if(args.smear) else "both"
    args.tag_proton = args.tag_proton or args.cut_proton
    args.standard_histogram_title_addition = ""
    if(args.closure):
        print(f"\n{color.BLUE}Running Closure Test (Unfolding the Modulated MC using the unweighted response matrices){color.END}\n")
        args.standard_histogram_title_addition = "Closure Test - Unfolding Modulated Simulation with itself"
    elif(args.sim):
        print(f"\n{color.BLUE}Running Simulated Test{color.END}\n")
        args.standard_histogram_title_addition = "Closure Test - Unfolding Simulation"
    if(args.mod):
        print(f"\n{color.BLUE}Using {color.BOLD}Modulated {color.END_b} Monte Carlo Files (to create the response matrices){color.END}\n")
        if(args.standard_histogram_title_addition not in [""]):
            args.standard_histogram_title_addition = f"{args.standard_histogram_title_addition} - Using Modulated Response Matrix"
        else:
            args.standard_histogram_title_addition = "Closure Test - Using Modulated Response Matrix"
    if(args.weighed_acceptance):
        args.standard_histogram_title_addition = args.standard_histogram_title_addition.replace("Modulated", "Weighted")
    if(args.tag_proton):
        Proton_Type = "Tagged Proton" if(not args.cut_proton) else "Cut with Proton Missing Mass"
        args.standard_histogram_title_addition = "".join([Proton_Type, f" - {args.standard_histogram_title_addition}" if(args.standard_histogram_title_addition not in [""]) else ""])
        print(f"\n{color.BBLUE}Running with the '{color.UNDERLINE}{Proton_Type}{color.END}{color.BBLUE}' Files{color.END}\n")
        del Proton_Type       
    if(args.title):
        if(args.standard_histogram_title_addition not in [""]):
            args.standard_histogram_title_addition = f"#splitline{{{args.standard_histogram_title_addition}}}{{{args.title}}}"
        else:
            args.standard_histogram_title_addition = args.title
        print(f"\nAdding the following extra title to the histograms:\n\t{args.standard_histogram_title_addition}\n")
    if(args.fit):
        print(f"\n\n{color.BGREEN}{color_bg.YELLOW}\n\n    Will be Fitting Plots    \n{color.END}\n\n") 
    print(f"\n{color.BBLUE}Smear option selected is: {'No Smear' if(str(args.smearing_options) in ['', 'no_smear']) else str(args.smearing_options.replace('_s', 'S')).replace('s', 'S')}{color.END}\n")
    args.Q2_y_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    if(any(binning in Binning_Method for binning in ["y_bin", "Y_bin"])):
        args.Q2_y_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    if(args.bins):
        args.Q2_y_Bin_List = args.bins
    if(args.Q2_y_Bin_List == []):
        print(f"{color.Error}ERROR: 'Q2_y_Bin_List' is empty. (Defaulting to running with Bin 1){color.END}")
        args.Q2_y_Bin_List = ['1']
    if('0' not in args.Q2_y_Bin_List):
        args.Q2_y_Bin_List.append('0')
        print(f"\n{color.RED}Running Bin 'All' for Q2-y Bins by default (will skip at end){color.END}\n")
    print(f"\nRunning for Q2-xB/Q2-y Bins: {str(args.Q2_y_Bin_List).replace('[', '')}".replace(']', ''))
    if(args.Common_Int_Bins):
        print(f"\n\n{color.BGREEN}Will ONLY be running the z-pT Bins that have been selected as per the 'Commom Integration Region' given by 'Common_Ranges_for_Integrating_z_pT_Bins'{color.END}\n\n")

    args.Run_5D_Unfold = not True
    args.num_5D_increments_used_to_slice = 422
    args.run_sec_unfold = not True
    args.sector_list = [1, 2, 3, 4, 5, 6]

    print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis\n{color.END}")

    args.timer = RuntimeTimer()
    args.timer.start()

    return args

def main_unfold(args):
    try:
        rdf = ROOT.TFile(args.single_file_input, "READ")
        print(f"The total number of histograms available for the{color.BOLD}RDataFrame{color.END} in '{color.BBLUE}{args.single_file_input}{color.END}' is {color.BOLD}{len(rdf.GetListOfKeys())}{color.END}")
    except:
        print(f"\n{color.Error}ERROR IN GETTING THE RDataFrame...\n{color.END}Traceback:\n{color.END_R}{traceback.format_exc()}{color.END}")
    mdf = ROOT.TFile(args.single_file_input, "READ")
    gdf = ROOT.TFile(args.single_file_input, "READ")
    tdf = ROOT.TFile(args.single_file_input, "READ")
    print(f"\n\n{color.BOLD}Done Loading RDataFrame files...\n{color.END}")

    print(f"{color.BBLUE}\n\nStarting Unfolding Procedures...\n{color.END}")
    Unfolded_Canvas, Legends, Bin_Unfolded, RooUnfolded_Histos, Bin_Acceptance, Unfolding_Histogram_1_Norm_Clone, Save_Response_Matrix, Parameter_List_Unfold_Methods = {}, {}, {}, {}, {}, {}, {}, {}
    Parameter_List_Unfold_Methods["SVD"], Parameter_List_Unfold_Methods["Bin"], Parameter_List_Unfold_Methods["Bayes"] = [], [], []
    List_of_All_Histos_For_Unfolding = {}
    count, count_failed = 0, 0
    for ii in mdf.GetListOfKeys():
        out_print_main = str(ii.GetName()).replace("mdf", "DataFrame_Type")
        if("Q2_y_z_pT_4D_Bins" in out_print_main):
            continue
        if(("_(Weighed)" in out_print_main) and not (args.mod or args.closure)):
            # print(f"\n{color.BOLD}Skipping '{out_print_main}' because it is weighed{color.END}\n")
            continue
        elif(("_(Weighed)" not in out_print_main) and args.mod):
            # print(f"\n{color.BOLD}Skipping '{out_print_main}' because it is unweighed{color.END}\n")
            continue
        ##========================================================##
        ##=====##    Conditions for Histogram Selection    ##=====##
        ##========================================================##
        Conditions_For_Unfolding = ["DataFrame_Type" in str(out_print_main)]
        # The histograms for 'out_print_main' will be skipped if any item in the list 'Conditions_For_Unfolding' is 'False'

        if("5D_Response" in str(out_print_main) and args.Run_5D_Unfold):
            # Found a Response matrix for 5D unfolding (handles differently to other plots selected below)
            if(f"_Slice_1_(Increment='{args.num_5D_increments_used_to_slice}')" not in str(out_print_main)):
                # The full 5D Response matrix is split into multiple slices that are rebuilt into a single 2D histogram in this script
                # For the common key name, only the first slice is needed (not counted as failure)
                continue
            elif((f"_Slice_1_" in str(out_print_main)) and (f"_Slice_1_(Increment='{args.num_5D_increments_used_to_slice}')" not in str(out_print_main))):
                count_failed += 1
                print(f"{color.RED}Potential Reason for Failure: Incorrect number of increments in:\n\tout_print_main = {color.Error}{out_print_main}{color.END}")
                print(f"Number Failed: {count_failed}")
                continue
            ## Correct Histogram Type:
            Conditions_For_Unfolding.append(args.Run_5D_Unfold) # Defined above (will not run 5D unfolding plots unless args.Run_5D_Unfold = True)
            Conditions_For_Unfolding.append("5D_Response_Matrix"        in str(out_print_main))
            Conditions_For_Unfolding.append("5D_Response_Matrix_1D" not in str(out_print_main))
            Conditions_For_Unfolding.append("Background"            not in str(out_print_main))
            ## Correct Cuts:
            Conditions_For_Unfolding.append("no_cut"                not in str(out_print_main))
            Conditions_For_Unfolding.append("cut_Complete_EDIS"     not in str(out_print_main))
            # Do not include the electron sector cuts here
            Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS" not in str(out_print_main))
            # Conditions_For_Unfolding.append("cut_Complete_SIDIS"        in str(out_print_main))
            Conditions_For_Unfolding.append("no_cut_eS"             not in str(out_print_main))
            ## Correct Variable(s):
            Conditions_For_Unfolding.append("MultiDim_Q2_y_z_pT_phi_h"  in str(out_print_main))
            ## Correct Smearing:
            if((args.smearing_options not in ["no_smear", "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"   not in str(out_print_main))
            if((args.smearing_options not in ["smear",    "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"       in str(out_print_main))
            if(False in Conditions_For_Unfolding):
                count_failed += 1
                # print(f"Conditions_For_Unfolding = {Conditions_For_Unfolding}")
                # print(f"{color.RED}{out_print_main}{color.END}")
                # print(f"Number Failed: {count_failed}")
                continue
            else:
                out_print_main_mdf = out_print_main.replace("DataFrame_Type", "mdf")
                if(out_print_main_mdf not in mdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                    continue
                Base_Name             = out_print_main_mdf.replace("_Slice_1_", "_Slice_NUMBER_")
                Slice_Num, Histo_List = 1, {}
                while(Slice_Num < 800):
                    histo_sliced = mdf.Get(Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_"))
                    if(histo_sliced):  # Check if the histogram exists
                        Histo_List[Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_")] = histo_sliced
                        Slice_Num += 1
                    else:
                        break  # Exit the loop if the histogram does not exist
                out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not args.sim) else "mdf")
                if(not args.closure):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
                if(args.weighed_acceptance):
                    out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
                ################################################################################
                ##======##     Removing Sliced Increments from non-TH2D Plot Names    ##======##
                out_print_main_rdf = out_print_main_rdf.replace(f"_Slice_1_(Increment='{args.num_5D_increments_used_to_slice}')", "")
                out_print_main_gdf = out_print_main_gdf.replace(f"_Slice_1_(Increment='{args.num_5D_increments_used_to_slice}')", "")
                out_print_main_mdf = out_print_main_mdf.replace(f"_Slice_1_(Increment='{args.num_5D_increments_used_to_slice}')", "")
                ##======##     Removing Sliced Increments from non-TH2D Plot Names    ##======##
                ################################################################################
                ##=============##    Removing Cuts from the Generated files    ##=============##
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
                for sector_cut_remove in range(1, 7):
                    out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
                del sector_cut_remove
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
                ##=============##    Removing Cuts from the Generated files    ##=============##
                ################################################################################
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                if(not args.sim):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                    out_print_main_rdf = out_print_main_rdf.replace("smear", "")
                out_print_main_gdf     = out_print_main_gdf.replace("smear", "")
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                ################################################################################
                ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
                out_print_main_rdf    = out_print_main_rdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                out_print_main_gdf    = out_print_main_gdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                out_print_main_mdf_1D = out_print_main_mdf.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
                ##======##    Non-MC_REC Response Matrices (these are not 2D plots)   ##======##
                ################################################################################
                if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf_1D}{color.END}\n")
                    for ii in mdf.GetListOfKeys():
                        if(("5D_Response_Matrix_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))
                if(args.sim):
                    out_print_main_rdf = out_print_main_mdf_1D
                    out_print_main_tdf = out_print_main_gdf
                    if(not args.closure):
                        out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                        out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                            continue
                    else:
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                    continue
                
                count += 1
                print(f"\n{color.BGREEN}\n(5D) Unfolding: {out_print_main}){color.END}\n")
                ExREAL_1D   = rdf.Get(out_print_main_rdf)
                MC_REC_1D   = mdf.Get(out_print_main_mdf_1D)
                MC_GEN_1D   = gdf.Get(out_print_main_gdf)
                Response_2D = Rebuild_Matrix_5D(List_of_Sliced_Histos=Histo_List, Standard_Name=out_print_main_mdf, Increment=args.num_5D_increments_used_to_slice)
                del Histo_List
                if(tdf not in ["N/A"]):
                    ExTRUE_1D = tdf.Get(out_print_main_tdf)
                else:
                    ExTRUE_1D = "N/A"
                if("mdf" in str(ExREAL_1D.GetName())):
                    print("\n    ExREAL_1D_initial.GetName() =", ExREAL_1D.GetName())
                    ExREAL_1D.SetName(str(ExREAL_1D_initial.GetName()).replace("mdf", "rdf"))
                    print("New ExREAL_1D_initial.GetName() =",   ExREAL_1D.GetName())
                
                # Getting MC Background Histogram (bgs - stands for BackGroundSubtraction)
                out_print_main_bdf_1D = out_print_main_mdf_1D.replace("'5D_Response_Matrix_1D'", "'Background_5D_Response_Matrix_1D'")
                if(((out_print_main_bdf_1D in mdf.GetListOfKeys()) or (out_print_main_bdf_1D in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf_1D))):
                    MC_BGS_1D = mdf.Get(out_print_main_bdf_1D) if(not args.sim) else rdf.Get(out_print_main_bdf_1D)
                    MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))
                else:
                    MC_BGS_1D = "None"
                    print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
                    raise TypeError("Missing (5D) Background Histogram")
                if(args.sim and (str(MC_BGS_1D) not in ["None"])):
                    # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                    ExREAL_1D.Add(MC_BGS_1D)
                List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin="All", Z_PT_Bin="All", MC_BGS_1D=MC_BGS_1D, args=args)
                continue
        elif(any(sector_particle in out_print_main for sector_particle in ["esec", "pipsec"]) and args.run_sec_unfold):
            if("Var-D2='phi_t" not in out_print_main):
                # Only running with the 1D Unfolding options at this time
                continue
            ## Correct Q2-y Bin:
            for Q2_y_bin in args.Q2_y_Bin_List:
                Q2_xB_Bin_Unfold = Q2_y_bin if(str(Q2_y_bin) not in ["All", "0", 0]) else "All"
                if(f"Q2-y-Bin={Q2_xB_Bin_Unfold}, " in str(out_print_main)):
                    Conditions_For_Unfolding = [True]
                    break
                else:
                    Conditions_For_Unfolding = [False]
            ## Correct Histogram Type:
            Conditions_For_Unfolding.append(args.run_sec_unfold) # Defined above (will not run sector unfolding plots unless args.run_sec_unfold = True)
            Conditions_For_Unfolding.append("Normal_2D"                 in str(out_print_main))
            Conditions_For_Unfolding.append("Background"            not in str(out_print_main))
            ## Correct Cuts:
            Conditions_For_Unfolding.append("no_cut"                not in str(out_print_main))
            Conditions_For_Unfolding.append("cut_Complete_EDIS"     not in str(out_print_main))
            # Do not include the electron sector cuts here
            Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS" not in str(out_print_main))
            # Conditions_For_Unfolding.append("cut_Complete_SIDIS"        in str(out_print_main))
            Conditions_For_Unfolding.append("no_cut_eS"             not in str(out_print_main))
            # Proton Cuts (Can control from the command line arguments: add 'CP' options for 'Cut on Proton' - other inputs will prevent the Proton Missing Mass cuts from being run as of 8/26/2024)
            if(args.cut_proton):
                Conditions_For_Unfolding.append(any(proCuts in str(out_print_main) for proCuts in ["_Proton'), ", "_Proton_Integrate'), "])) # Require Proton MM Cuts
            else:
                Conditions_For_Unfolding.append("_Proton'), "          not in str(out_print_main)) # Remove  Proton MM Cuts
                Conditions_For_Unfolding.append("_Proton_Integrate')"  not in str(out_print_main)) # Remove  Proton MM Cuts (with integrated bins)
            ## Correct Variable(s):
            Particle_Sector = "N/A"
            Conditions_For_Unfolding.append("Var-D1='esec"             in str(out_print_main)) # Electron Sector Only
            if("Var-D1='esec"   in str(out_print_main)):
                Particle_Sector = "Electron Sector"
            # Conditions_For_Unfolding.append("Var-D1='pipsec"           in str(out_print_main)) # Pi+ Pion Sector Only
            if("Var-D1='pipsec" in str(out_print_main)):
                Particle_Sector = "#pi^{+} Pion Sector"
            ## Correct Smearing:
            Smear_Found = "(Smear-Type='')" not in str(out_print_main)
            if((args.smearing_options not in ["no_smear", "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"   not in str(out_print_main))
            if((args.smearing_options not in ["smear",    "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"       in str(out_print_main))
            if(False in Conditions_For_Unfolding):
                count_failed += 1
                # print(f"Conditions_For_Unfolding = {Conditions_For_Unfolding}")
                # print(f"{color.RED}{out_print_main}{color.END}")
                # print(f"Number Failed: {count_failed}\n\n")
                continue
            else:
                out_print_main_mdf     = out_print_main.replace("DataFrame_Type", "mdf")
                out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not args.sim) else "mdf")
                if(not args.closure):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
                if(args.weighed_acceptance):
                    out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
                ################################################################################
                ##=============##          Finding MC Backgound Plots          ##=============##
                out_print_main_bdf = out_print_main_mdf.replace("Normal_2D", "Normal_Background_2D")
                ##=============##          Finding MC Backgound Plots          ##=============##
                ################################################################################
                ##=============##    Removing Cuts from the Generated files    ##=============##
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
                for sector_cut_remove in range(1, 7):
                    out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
                del sector_cut_remove
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
                out_print_main_gdf     = out_print_main_gdf.replace("_Proton",                                    "")
                ##=============##    Removing Cuts from the Generated files    ##=============##
                ################################################################################
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                if(not args.sim):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                    out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                    out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
                out_print_main_gdf     = out_print_main_gdf.replace("_smeared", "")
                out_print_main_gdf     = out_print_main_gdf.replace("smear",    "")
                ##=============##    Removing Smearing from Non-MC_REC files   ##=============##
                ################################################################################
                if(out_print_main_mdf not in mdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                    for ii in mdf.GetListOfKeys():
                        if(("Normal_2D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))
                if(args.sim):
                    out_print_main_rdf     = out_print_main_mdf
                    out_print_main_tdf     = out_print_main_gdf
                    if(not args.closure):
                        out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                        out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                            continue
                    else:
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                    continue

                count += 1
                print(f"\n{color.BGREEN}(Sector) Unfolding: {out_print_main}{color.END}\n")
                ExREAL_3D     = rdf.Get(out_print_main_rdf)
                MC_REC_3D     = mdf.Get(out_print_main_mdf)
                MC_GEN_3D     = gdf.Get(out_print_main_gdf)
                if(args.sim):
                    ExTRUE_3D = tdf.Get(out_print_main_tdf)
                else:
                    ExTRUE_3D = "N/A"
                if("mdf" in str(ExREAL_3D.GetName())):
                    print("\n    ExREAL_3D.GetName() =", ExREAL_3D.GetName())
                    ExREAL_3D.SetName(str(ExREAL_3D_initial.GetName()).replace("mdf", "rdf"))
                    print("New ExREAL_3D.GetName() =",   ExREAL_3D.GetName())
                # Getting MC Background Histogram (BGS - stands for BackGroundSubtraction)
                if(((out_print_main_bdf in mdf.GetListOfKeys()) or (out_print_main_bdf in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf))):
                    MC_BGS_3D = mdf.Get(out_print_main_bdf) if(not args.sim) else rdf.Get(out_print_main_bdf)
                    MC_BGS_3D = mdf.Get(out_print_main_bdf)
                    MC_BGS_3D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_3D.GetTitle()), "};", str(MC_REC_3D.GetXaxis().GetTitle()), ";", str(MC_REC_3D.GetYaxis().GetTitle())]))
                else:
                    MC_BGS_3D = "None"
                    print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf}{color.END_R}){color.END}")
                    raise TypeError("Missing (Sector) Background Histogram")
                if(args.sim and (str(MC_BGS_3D) not in ["None"])):
                    # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                    ExREAL_3D.Add(MC_BGS_3D)
                    
                z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_xB_Bin_Unfold)[1]
                for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
                    if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_xB_Bin_Unfold, Z_PT_BIN=z_pT_Bin_Unfold, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=args.Common_Int_Bins)):
                        continue
                    for Sector in args.sector_list:
                        if(Smear_Found):
                            out_print_main_____1D_Sector     = str(out_print_main.replace("z-PT-Bin=All",     "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                            out_print_main_rdf_1D_Sector     = str(out_print_main_rdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                            out_print_main_mdf_1D_Sector     = str(out_print_main_mdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                            out_print_main_gdf_1D_Sector     = str(out_print_main_gdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                            if(args.sim):
                                out_print_main_tdf_1D_Sector = str(out_print_main_tdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                            out_print_main_bdf_1D_Sector     = str(out_print_main_bdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec_smeared'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec_smeared'-[{Sector}]")
                        else:
                            out_print_main_____1D_Sector     = str(out_print_main.replace("z-PT-Bin=All",     "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                            out_print_main_rdf_1D_Sector     = str(out_print_main_rdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                            out_print_main_mdf_1D_Sector     = str(out_print_main_mdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                            out_print_main_gdf_1D_Sector     = str(out_print_main_gdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                            if(args.sim):
                                out_print_main_tdf_1D_Sector = str(out_print_main_tdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")
                            out_print_main_bdf_1D_Sector     = str(out_print_main_bdf.replace("z-PT-Bin=All", "".join(["z-PT-Bin=", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold not in [0]) else "All"]))).replace("sec'-[NumBins=8, MinBin=-0.5, MaxBin=7.5]", f"sec'-[{Sector}]")                    
                        
                        New_Bin_Title = "".join(["".join(["}{#splitline{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold), "".join([" #topbar z-P_{T} Bin: ", str(z_pT_Bin_Unfold)]) if(z_pT_Bin_Unfold not in [0]) else "", f" #topbar {Particle_Sector} {Sector}"]) if(str(Q2_xB_Bin_Unfold) not in ["All", "0", 0]) else "".join(["}{#splitline{", Particle_Sector, " ", str(Sector)]),  "}{Pass Version: #color[", str(root_color.Blue), "]{", str(args.standard_histogram_title_addition), "}}"])
                        
                        ExREAL_1D = ExREAL_3D.Clone(out_print_main_rdf_1D_Sector)
                        ExREAL_1D_Title = str(ExREAL_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                        ExREAL_1D_Title = ExREAL_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                        MC_REC_1D = MC_REC_3D.Clone(out_print_main_mdf_1D_Sector)
                        MC_REC_1D_Title = str(MC_REC_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                        MC_REC_1D_Title = MC_REC_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                        MC_GEN_1D = MC_GEN_3D.Clone(out_print_main_gdf_1D_Sector)
                        MC_GEN_1D_Title = str(MC_GEN_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                        MC_GEN_1D_Title = MC_GEN_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                        if(args.sim):
                            ExTRUE_1D = ExTRUE_3D.Clone(out_print_main_tdf_1D_Sector)
                            ExTRUE_1D_Title = str(ExTRUE_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                            ExTRUE_1D_Title = ExTRUE_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                        if(MC_BGS_3D not in ["None"]):
                            MC_BGS_1D = MC_BGS_3D.Clone(out_print_main_bdf_1D_Sector)
                            MC_BGS_1D_Title = str(MC_BGS_3D.GetTitle()).replace("".join(["}{Q^{2}-y Bin: ", str(Q2_xB_Bin_Unfold)]), New_Bin_Title)
                            MC_BGS_1D_Title = MC_BGS_1D_Title.replace(f"{Particle_Sector} vs. ", "")
                            
                        # Setting z-pT Bins
                        ExREAL_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                        MC_REC_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                        MC_GEN_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold     if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                        if(args.sim):
                            ExTRUE_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                        if(MC_BGS_3D not in ["None"]):
                            MC_BGS_1D.GetXaxis().SetRangeUser(z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else 1, z_pT_Bin_Unfold if(z_pT_Bin_Unfold not in [0]) else (z_pT_Bin_Range + 1))
                        # Setting Particle Sector
                        ExREAL_1D.GetYaxis().SetRangeUser(Sector,     Sector)
                        MC_REC_1D.GetYaxis().SetRangeUser(Sector,     Sector)
                        MC_GEN_1D.GetYaxis().SetRangeUser(0, 7) # Generated Sector is not useful
                        if(args.sim):
                            ExTRUE_1D.GetYaxis().SetRangeUser(Sector, Sector)
                        if(MC_BGS_3D not in ["None"]):
                            MC_BGS_1D.GetYaxis().SetRangeUser(Sector, Sector)
                            
                        ExREAL_1D = ExREAL_1D.Project3D("z")
                        ExREAL_1D.SetTitle(ExREAL_1D_Title)
                        MC_REC_1D = MC_REC_1D.Project3D("z")
                        MC_REC_1D.SetTitle(MC_REC_1D_Title)
                        MC_GEN_1D = MC_GEN_1D.Project3D("z")
                        MC_GEN_1D.SetTitle(MC_GEN_1D_Title)
                        if(args.sim):
                            ExTRUE_1D = ExTRUE_1D.Project3D("z")
                            ExTRUE_1D.SetTitle(ExTRUE_1D_Title)
                        else:
                            ExTRUE_1D = "N/A"
                        if(MC_BGS_3D not in ["None"]):
                            MC_BGS_1D = MC_BGS_1D.Project3D("z")
                            MC_BGS_1D.SetTitle(MC_BGS_1D_Title)
                        List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main_____1D_Sector, Response_2D="N/A", ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold, MC_BGS_1D=MC_BGS_1D, args=args)
            continue
        else:
            ## Correct Histogram Type:
            Conditions_For_Unfolding.append("Response_Matrix_Normal"    in str(out_print_main))
            Conditions_For_Unfolding.append("Response_Matrix_Normal_1D"    not in str(out_print_main))        
            Conditions_For_Unfolding.append("5D_Response" not in str(out_print_main))

            ## Correct Cuts:
            Conditions_For_Unfolding.append("no_cut"                   not in str(out_print_main))
            Conditions_For_Unfolding.append("cut_Complete_EDIS"        not in str(out_print_main))

            if(args.run_sectors):
                Conditions_For_Unfolding.append(any(f"cut_Complete_SIDIS_{SC}" in str(out_print_main) for SC in args.sectors_to_unfold))
            else:
                # Do not include the electron sector cuts here
                Conditions_For_Unfolding.append("cut_Complete_SIDIS_eS"    not in str(out_print_main))
                Conditions_For_Unfolding.append("no_cut_eS"                not in str(out_print_main))
            
            # Proton Cuts (Can control from the command line arguments: add 'CP' options for 'Cut on Proton' - other inputs will prevent the Proton Missing Mass cuts from being run as of 8/26/2024)
            if(args.cut_proton):
                Conditions_For_Unfolding.append(any(proCuts in str(out_print_main) for proCuts in ["_Proton'), ", "_Proton_Integrate'), "] + [f"_Proton_eS{sec}o'), " for sec in range(1, 7)] + [f"_Proton_Integrate_eS{sec}o'), " for sec in range(1, 7)]))
                # Conditions_For_Unfolding.append("_Proton'), "              in str(out_print_main)) # Require Proton MM Cuts
            else:
                Conditions_For_Unfolding.append("_Proton'), "          not in str(out_print_main)) # Remove  Proton MM Cuts
                Conditions_For_Unfolding.append("_Proton_Integrate')"  not in str(out_print_main)) # Remove  Proton MM Cuts (with integrated bins)
                for sec in range(1, 7):
                    Conditions_For_Unfolding.append(f"_Proton_eS{sec}o'), "          not in str(out_print_main)) # Remove Proton MM Cuts (Sector Cuts)
                    Conditions_For_Unfolding.append(f"_Proton_Integrate_eS{sec}o')"  not in str(out_print_main)) # Remove Proton MM Cuts (with integrated bins - Sector Cuts)

            # # Require Integrated Bin Cuts
            # Conditions_For_Unfolding.append("Integrate')"     in str(out_print_main))
            # # Remove Integrated Bin Cuts
            # Conditions_For_Unfolding.append("Integrate')" not in str(out_print_main))

            ## Correct Variable(s):
            if(not args.allow_other_variables):
                Conditions_For_Unfolding.append("phi_t"          in str(out_print_main)) # Unfolds only the phi_t distributions (skipping any option that does not include them)
            # # Conditions_For_Unfolding.append("'phi_t"      not in str(out_print_main))
            if(args.unfolding_1D):
                Conditions_For_Unfolding.append("Multi"      not in str(out_print_main)) # For REMOVING all Multidimensional Unfolding Plots (1D only)
            if(args.unfolding_3D):
                Conditions_For_Unfolding.append("Multi"          in str(out_print_main)) # For RUNNING only Multidimensional Unfolding Plots (3D only)
            Conditions_For_Unfolding.append("Multi_Dim_" not in str(out_print_main))     # For removing all (Old 3D) Multidimensional Unfolding Plots
            # Conditions_For_Unfolding.append("Multi_Dim_"     in str(out_print_main)) # For running only (Old 3D) Multidimensional Unfolding Plots
            if("y" in Binning_Method):
                # Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
                Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)
            else:
                # Conditions_For_Unfolding.append('''("Multi_Dim_z_pT_Bin_Y_bin_phi_t"  in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected''')
                Conditions_For_Unfolding.append(("Multi_Dim_z_pT_Bin_Y_bin_phi_t"     in str(out_print_main)) or ("Multi_Dim_" not in str(out_print_main))) # Selects only the 3D unfolding (z-pT-phi_t) or the 1D unfolding (assuming that the condition of ("phi_t" in str(out_print_main)) is selected)
            Conditions_For_Unfolding.append("Multi_Dim_Q2_phi_t"                  not in str(out_print_main))
            Conditions_For_Unfolding.append("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t"    not in str(out_print_main))

            # Smearing Options:
            if((args.smearing_options not in ["no_smear", "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"    not in str(out_print_main))
            if((args.smearing_options not in ["smear",    "both"])):
                Conditions_For_Unfolding.append("(Smear-Type='')"        in str(out_print_main))

            ##========================================================##
            ##=====##    Conditions for Histogram Selection    ##=====##
            ##========================================================##

            if(False in Conditions_For_Unfolding):
                # Conditions for unfolding were not met by 'out_print_main'
                count_failed += 1
                # print("Conditions_For_Unfolding =", Conditions_For_Unfolding)
                # print("".join([color.RED, str(out_print_main), color.END]))
                # print("".join(["Number Failed: ", str(count_failed)]))
                continue
            else:
                del Conditions_For_Unfolding # Do not need the list of conditions for the rest of this loop
                
                out_print_main_rdf     = out_print_main.replace("DataFrame_Type", "rdf" if(not args.sim) else "mdf")
                if(not args.closure):
                    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                out_print_main_mdf     = out_print_main.replace("DataFrame_Type", "mdf")
                out_print_main_gdf     = out_print_main.replace("DataFrame_Type", "gdf")
                if(args.weighed_acceptance):
                    out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
                ################################################################################
                ##=============##    Removing Cuts from the Generated files    ##=============##
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_EDIS",                          "no_cut")
                for sector_cut_remove in range(1, 7):
                    out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
                    out_print_main_gdf = out_print_main_gdf.replace(f"Integrate_eS{sector_cut_remove}o",       "Integrate")
                del sector_cut_remove
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS_Proton",                  "no_cut")
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete_SIDIS",                         "no_cut")
                out_print_main_gdf     = out_print_main_gdf.replace("cut_Complete",                               "no_cut")
                ##=============##    Removing Cuts from the Generated files    ##=============##
                ################################################################################


                #############################################################################
                ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
                if(not args.sim):      # Only remove smearing if rdf is supposed to come from the experiment (is not synthetic data)
                    out_print_main_rdf = out_print_main_rdf.replace("_smeared", "")
                    out_print_main_rdf = out_print_main_rdf.replace("smear_",   "")
                    out_print_main_rdf = out_print_main_rdf.replace("smear",    "")
                out_print_main_gdf     = out_print_main_gdf.replace("_smeared", "")
                out_print_main_gdf     = out_print_main_gdf.replace("smear_",   "")
                out_print_main_gdf     = out_print_main_gdf.replace("smear",    "")
                ##=============##  Removing Smearing from Non-MC_REC files  ##=============##
                #############################################################################

                #############################################################################
                ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
                out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
                out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
                out_print_main_rdf = out_print_main_rdf.replace("'Response_Matrix'",        "'Response_Matrix_1D'")
                out_print_main_gdf = out_print_main_gdf.replace("'Response_Matrix'",        "'Response_Matrix_1D'")
                ##======##  Non-MC_REC Response Matrices (these are not 2D plots)  ##======##
                #############################################################################

                if(out_print_main_mdf not in mdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf}{color.END}\n")
                    continue

                out_print_main_mdf_1D = out_print_main_mdf.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
                if(("".join([", (Var-D2='z_pT_Bin", str(Binning_Method)]) not in out_print_main_mdf_1D) and ("Var-D1='phi_t'" in out_print_main_mdf_1D)):
                    out_print_main_mdf_1D = out_print_main_mdf_1D.replace("]))", "".join(["]), (Var-D2='z_pT_Bin", str(Binning_Method), "" if("smear" not in str(out_print_main_mdf_1D)) else "_smeared", "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5]))"]))
                if(out_print_main_mdf_1D not in mdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN MDF...\n{color.END_R}Dataframe is missing: {color.BOLD}{out_print_main_mdf_1D}{color.END}\n")
                    for ii in mdf.GetListOfKeys():
                        if(("Response_Matrix_Normal_1D" in str(ii)) and ("cut_Complete_SIDIS" in str(ii))):
                            print(str(ii.GetName()))

                out_print_main_tdf = None
                if(args.sim):
                    out_print_main_rdf     = out_print_main_mdf_1D
                    out_print_main_tdf     = out_print_main_gdf
                    if(not args.closure):
                        out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
                        out_print_main_tdf = out_print_main_tdf.replace("_(Weighed)", "")
                    if(tdf not in ["N/A"]):
                        if(out_print_main_tdf not in tdf.GetListOfKeys()):
                            print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Dataframe is missing: {color.BCYAN}{out_print_main_tdf}{color.END}\n")
                            continue
                    else:
                        print(f"{color.Error}ERROR IN TDF...\n{color.END_R}Missing Dataframe...{color.END}\n")
                if(out_print_main_rdf not in rdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN RDF...\n{color.END_R}Dataframe is missing: {color.BBLUE}{out_print_main_rdf}{color.END}\n")
                    continue
                if(out_print_main_gdf not in gdf.GetListOfKeys()):
                    print(f"{color.Error}ERROR IN GDF...\n{color.END_R}Dataframe is missing: {color.BGREEN}{out_print_main_gdf}{color.END}\n")
                    continue

                if("Q2-xB-Bin=All" in str(out_print_main) or "Q2-y-Bin=All," in str(out_print_main)):
                    Q2_xB_Bin_Unfold = 0
                elif(any(str(f"{BinType}=-3,") in str(out_print_main) for BinType in ["Q2-xB-Bin", "Q2-y-Bin"])):
                    Q2_xB_Bin_Unfold = -3
                else:
                    for Q2_xB_Bin_Unfold_ii in range(1, 40, 1):
                        if(any(f"{BinType}={Q2_xB_Bin_Unfold_ii}," in str(out_print_main) for BinType in ["Q2-xB-Bin", "Q2-y-Bin"])):
                            Q2_xB_Bin_Unfold = Q2_xB_Bin_Unfold_ii
                            break
                        else:
                            Q2_xB_Bin_Unfold = "Undefined..."

                if(type(Q2_xB_Bin_Unfold) is str):
                    print(f"\n{color.Error}ERROR - Q2_xB_Bin_Unfold = {Q2_xB_Bin_Unfold}\n{color.END}Error is with\n out_print_main = {out_print_main}")

                if((str(Q2_xB_Bin_Unfold) not in args.Q2_y_Bin_List) and ("Multi_Dim_Q2_y_Bin_phi_t" not in str(out_print_main))):
                    print(f"Bin {Q2_xB_Bin_Unfold} is not in Q2_y_Bin_List = {args.Q2_y_Bin_List}")
                    continue

                count += 1
                print(f"\nUnfolding: {out_print_main}")
                ExREAL_1D_initial     = rdf.Get(out_print_main_rdf)
                MC_REC_1D_initial     = mdf.Get(out_print_main_mdf_1D)
                MC_GEN_1D_initial     = gdf.Get(out_print_main_gdf)
                Response_2D_initial   = mdf.Get(out_print_main_mdf)
                if((tdf not in ["N/A"]) and out_print_main_tdf):
                    ExTRUE_1D_initial = tdf.Get(out_print_main_tdf)
                else:
                    ExTRUE_1D_initial = None
                if("mdf" in str(ExREAL_1D_initial.GetName())):
                    print("\n    ExREAL_1D_initial.GetName() =", ExREAL_1D_initial.GetName())
                    ExREAL_1D_initial.SetName(str(ExREAL_1D_initial.GetName()).replace("mdf", "rdf"))
                    print("New ExREAL_1D_initial.GetName() =",   ExREAL_1D_initial.GetName())

                ExREAL_1D_initial.SetTitle(str(ExREAL_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
                MC_REC_1D_initial.SetTitle(str(MC_REC_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
                MC_GEN_1D_initial.SetTitle(str(MC_GEN_1D_initial.GetTitle()).replace("with Proton Cuts",     ""))
                Response_2D_initial.SetTitle(str(Response_2D_initial.GetTitle()).replace("with Proton Cuts", ""))

                # Getting MC Background Histogram (bgs - stands for BackGroundSubtraction)
                out_print_main_bdf_1D = out_print_main_mdf_1D.replace("'Response_Matrix_1D'",        "'Background_Response_Matrix_1D'")
                out_print_main_bdf_1D = out_print_main_bdf_1D.replace("'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'")
                if(((out_print_main_bdf_1D in mdf.GetListOfKeys()) or (out_print_main_bdf_1D in rdf.GetListOfKeys())) and ("Background" in str(out_print_main_bdf_1D))):
                    MC_BGS_1D_initial = mdf.Get(out_print_main_bdf_1D) if(not args.sim) else rdf.Get(out_print_main_bdf_1D)
                else:
                    MC_BGS_1D_initial = "None"
                    print(f"\n{color.Error}ERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
                    raise TypeError("Missing Background Histogram")
                if(args.sim and (str(MC_BGS_1D_initial) not in ["None"])):
                    # When Unfolding Simulated Data with the background histogram, the background should still be included in the 'rdf' histograms
                    ExREAL_1D_initial.Add(MC_BGS_1D_initial)
                    

        ###############################################################################################
        ###==========##==========###     z-pT Binning Dimensions Slice     ###==========##==========###

                z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All"     in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 49 if(Q2_xB_Bin_Unfold in [1, 2, 3] or ("Binning-Type='3'" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [4]) else 36 if(Q2_xB_Bin_Unfold in [5]) else 25 if(Q2_xB_Bin_Unfold in [6, 7]) else 20 if(Q2_xB_Bin_Unfold in [8]) else 1
                if(any(binning in Binning_Method for binning in ["y"])):
                    z_pT_Bin_Range = 0 if(("Q2-xB-Bin=All" in str(out_print_main)) or ("Q2-y-Bin=All" in str(out_print_main))) else 42 if(Q2_xB_Bin_Unfold in [2]) else 36 if(Q2_xB_Bin_Unfold in [4, 5, 9, 10]) else 35 if(Q2_xB_Bin_Unfold in [1, 3]) else 30 if(Q2_xB_Bin_Unfold in [6, 7, 8, 11]) else 25 if(Q2_xB_Bin_Unfold in [13, 14]) else 20 if(Q2_xB_Bin_Unfold in [12, 15, 16, 17]) else 1

                if("Y_bin" in Binning_Method):
                    z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_xB_Bin_Unfold)[1]

                for z_pT_Bin_Unfold in range(0, z_pT_Bin_Range + 1, 1):
                    if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                        if(((Q2_xB_Bin_Unfold in [1, 2]) and (z_pT_Bin_Unfold in [49])) or (Q2_xB_Bin_Unfold == 3 and z_pT_Bin_Unfold in [49, 48, 42]) or (Q2_xB_Bin_Unfold in [1, 4] and z_pT_Bin_Unfold in [42]) or (Q2_xB_Bin_Unfold == 5 and z_pT_Bin_Unfold in [36]) or (Q2_xB_Bin_Unfold == 7 and z_pT_Bin_Unfold in [25])):
                            continue
                    elif(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_xB_Bin_Unfold, Z_PT_BIN=z_pT_Bin_Unfold, BINNING_METHOD=Binning_Method)):
                        continue

            #########################################################
            ##===============##     3D Slices     ##===============##
                    if("3D" in str(type(Response_2D_initial))):
                        try:
                            bin_Response_2D_0, bin_Response_2D_1 = Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), Response_2D_initial.GetZaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else Response_2D_initial.GetNbinsZ())
                            if(z_pT_Bin_Unfold != 0):
                                Response_2D_initial.GetZaxis().SetRange(bin_Response_2D_0, bin_Response_2D_1)
                            Response_2D           = Response_2D_initial.Project3D('yx e')
                            Response_2D.SetName(str(Response_2D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])))
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            else:
                                Response_2D_Title_New = (str(Response_2D.GetTitle()).replace("yx projection", "")).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            if((args.pass_version not in [""]) and (args.pass_version not in Response_2D_Title_New)):
                                Response_2D_Title_New = "".join(["#splitline{", str(Response_2D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                            Response_2D.SetTitle(Response_2D_Title_New)
                        except:
                            print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (Response_2D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                    else:
                        Response_2D = Response_2D_initial

            ##===============##     3D Slices     ##===============##
            #########################################################

            #########################################################
            ##===============##     2D Slices     ##===============##
                    if("2D" in str(type(ExREAL_1D_initial))):
                        try:
                            bin_ExREAL_1D_0, bin_ExREAL_1D_1 = ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), ExREAL_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExREAL_1D_initial.GetNbinsY())
                            ExREAL_1D                        = ExREAL_1D_initial.ProjectionX(str(ExREAL_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExREAL_1D_0, bin_ExREAL_1D_1, "e")
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            else:
                                ExREAL_1D_Title_New          = str(ExREAL_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            if((args.pass_version not in [""]) and (args.pass_version not in ExREAL_1D_Title_New)):
                                ExREAL_1D_Title_New          = "".join(["#splitline{", str(ExREAL_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                            ExREAL_1D.SetTitle(ExREAL_1D_Title_New)
                        except:
                            print("".join([color.Error, "\nERROR IN z-pT BIN SLICING (ExREAL_1D):\n", color.END_R, str(traceback.format_exc()), color.END]))
                    else:
                        # print("\nExREAL_1D already is a 1D Histogram...")
                        ExREAL_1D = ExREAL_1D_initial

                    if("2D" in str(type(MC_REC_1D_initial))):
                        try:
                            bin_MC_REC_1D_0, bin_MC_REC_1D_1 = MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_REC_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_REC_1D_initial.GetNbinsY())
                            MC_REC_1D                        = MC_REC_1D_initial.ProjectionX(str(MC_REC_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_REC_1D_0, bin_MC_REC_1D_1, "e")
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            else:
                                MC_REC_1D_Title_New          = str(MC_REC_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            if((args.pass_version not in [""]) and (args.pass_version not in MC_REC_1D_Title_New)):
                                MC_REC_1D_Title_New          = "".join(["#splitline{", str(MC_REC_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                            MC_REC_1D.SetTitle(MC_REC_1D_Title_New)
                        except:
                            print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (ExREAL_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                    else:
                        # print("\nMC_REC_1D already is a 1D Histogram...")
                        MC_REC_1D = MC_REC_1D_initial

                    if(MC_BGS_1D_initial != "None"):
                        if("2D" in str(type(MC_BGS_1D_initial))):
                            try:
                                bin_MC_BGS_1D_0, bin_MC_BGS_1D_1 = MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_BGS_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_BGS_1D_initial.GetNbinsY())
                                MC_BGS_1D                        = MC_BGS_1D_initial.ProjectionX(str(MC_BGS_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_BGS_1D_0, bin_MC_BGS_1D_1, "e")
                                if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                    MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                                else:
                                    MC_BGS_1D_Title_New          = "".join(["#splitline{BACKGROUND}{", str(MC_BGS_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}}"]))])
                                if((args.pass_version not in [""]) and (args.pass_version not in MC_BGS_1D_Title_New)):
                                    MC_BGS_1D_Title_New          = "".join(["#splitline{", str(MC_BGS_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                                MC_BGS_1D.SetTitle(MC_BGS_1D_Title_New)
                            except:
                                print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (MC_BGS_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                        else:
                            # print("\nMC_BGS_1D already is a 1D Histogram...")
                            MC_BGS_1D = MC_BGS_1D_initial
                    else:
                        MC_BGS_1D = MC_BGS_1D_initial

                    if("2D" in str(type(MC_GEN_1D_initial))):
                        try:
                            bin_MC_GEN_1D_0, bin_MC_GEN_1D_1 = MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), MC_GEN_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else MC_GEN_1D_initial.GetNbinsY())
                            MC_GEN_1D                        = MC_GEN_1D_initial.ProjectionX(str(MC_GEN_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_MC_GEN_1D_0, bin_MC_GEN_1D_1, "e")
                            if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            else:
                                MC_GEN_1D_Title_New          = str(MC_GEN_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                            if((args.pass_version not in [""]) and (args.pass_version not in MC_GEN_1D_Title_New)):
                                MC_GEN_1D_Title_New          = "".join(["#splitline{", str(MC_GEN_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                            MC_GEN_1D.SetTitle(MC_GEN_1D_Title_New)
                        except:
                            print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (MC_GEN_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                    else:
                        # print("\nMC_GEN_1D already is a 1D Histogram...")
                        MC_GEN_1D = MC_GEN_1D_initial

                    if((tdf not in ["N/A"]) and ExTRUE_1D_initial):
                        if("2D" in str(type(ExTRUE_1D_initial))):
                            try:
                                bin_ExTRUE_1D_0, bin_ExTRUE_1D_1 = ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else 1), ExTRUE_1D_initial.GetYaxis().FindBin(z_pT_Bin_Unfold if(z_pT_Bin_Unfold != 0) else ExTRUE_1D_initial.GetNbinsY())
                                ExTRUE_1D                        = ExTRUE_1D_initial.ProjectionX(str(ExTRUE_1D_initial.GetName()).replace("z-PT-Bin=All", "".join(["z-PT-Bin=", "All_1D" if(z_pT_Bin_Unfold == 0) else str(z_pT_Bin_Unfold)])), bin_ExTRUE_1D_0, bin_ExTRUE_1D_1, "e")
                                if(("y_bin" not in Binning_Method) and ("Y_bin" not in Binning_Method)):
                                    ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-x_{B} Bin: ", str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                                else:
                                    ExTRUE_1D_Title_New          = str(ExTRUE_1D.GetTitle()).replace("".join(["Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold)]), "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ",     str(Q2_xB_Bin_Unfold), "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT_Bin_Unfold) if(z_pT_Bin_Unfold != 0) else "All", "}}}"]))
                                if((args.pass_version not in [""]) and (args.pass_version not in ExTRUE_1D_Title_New)):
                                    ExTRUE_1D_Title_New          = "".join(["#splitline{", str(ExTRUE_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                                ExTRUE_1D_Title_New        = str(str(ExTRUE_1D_Title_New.replace("Generated",                  "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                                ExTRUE_1D_Title_X_Axis_New = str(str(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Generated", "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                                ExTRUE_1D.SetTitle(ExTRUE_1D_Title_New)
                                ExTRUE_1D.GetXaxis().SetTitle(ExTRUE_1D_Title_X_Axis_New)
                            except:
                                print(f"\n{color.Error}ERROR IN z-pT BIN SLICING (ExTRUE_1D):\n{color.END_R}{traceback.format_exc()}{color.END}")
                        else:
                            # print("\nExTRUE_1D already is a 1D Histogram...")
                            ExTRUE_1D = ExTRUE_1D_initial
                            ExTRUE_1D_Title_New            = str(str(str(ExTRUE_1D.GetTitle()).replace("Generated",            "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                            if((args.pass_version not in [""]) and (args.pass_version not in ExTRUE_1D_Title_New)):
                                ExTRUE_1D_Title_New        = "".join(["#splitline{", str(ExTRUE_1D_Title_New), "}{", root_color.Bold, "{#scale[1.15]{", str(args.pass_version), "}}}"])
                            ExTRUE_1D_Title_X_Axis_New     = str(str(str(ExTRUE_1D.GetXaxis().GetTitle()).replace("Generated", "True Simulated")).replace("Gen", "True")).replace("GEN", "True")
                            ExTRUE_1D.SetTitle(ExTRUE_1D_Title_New)
                            ExTRUE_1D.GetXaxis().SetTitle(ExTRUE_1D_Title_X_Axis_New)
                    else:
                        ExTRUE_1D = "N/A"
            ##===============##     2D Slices     ##===============##
            #########################################################
        ###==========##==========###     z-pT Binning Dimensions Slice     ###==========##==========###
        ###############################################################################################
                    if((z_pT_Bin_Unfold   != 0)                            and (("Combined_"                 in out_print_main) or ("Multi_Dim_Q2"       in out_print_main))):
                        continue
                    if(((Q2_xB_Bin_Unfold == 0) or (z_pT_Bin_Unfold != 0)) and ("Multi_Dim_z_pT_Bin"         in out_print_main)):
                        continue
                    if(((Q2_xB_Bin_Unfold == 0) or (z_pT_Bin_Unfold != 0)) and ("MultiDim_z_pT_Bin"          in out_print_main)):
                        continue
                    if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("Combined_"                 in out_print_main) or ("Multi_Dim_Q2_phi_t" in out_print_main))):
                        continue
                    if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("MultiDim_Q2_y_z_pT_phi_h"  in out_print_main))):
                        continue

                    if(("'phi_t" not in out_print_main) and ("'phi_t_smeared'" not in out_print_main) and ("Combined_phi_t" not in out_print_main) and ("'W" not in out_print_main) and ("'Multi_Dim" not in out_print_main) and ("'MultiDim_Q2_y_z_pT_phi_h" not in out_print_main) and ("'MultiDim_z_pT_Bin_Y_bin_phi_t" not in out_print_main)):
                        print(f"\nADDING CUTS FOR: {out_print_main}\n")

                        if("'MM" not in out_print_main):
                            if(((Q2_xB_Bin_Unfold != 0) or (z_pT_Bin_Unfold != 0)) and (("Combined_phi_t" not in out_print_main) and ("Multi_Dim" not in out_print_main))):
                                # Do not plot other variables that are not phi_t
                                continue
                            # Extra Y-Bins in 2D Histogram:
                            for ybin in range(0, Response_2D.GetYaxis().GetNbins() + 2, 1):
                                Response_2D.SetBinContent(0, ybin, 0)
                                if("'pT'" not in out_print_main and "'pT_smeared'" not in out_print_main):
                                    Response_2D.SetBinContent(1, ybin, 0)
                            try:
                                # Extra Bins in 1D Histogram:
                                ExREAL_1D.SetBinContent(0, 0)
                                MC_REC_1D.SetBinContent(0, 0)
                                MC_GEN_1D.SetBinContent(0, 0)
                                ExREAL_1D.SetBinContent(ExREAL_1D.GetNbinsX() + 1, 0)
                                MC_REC_1D.SetBinContent(MC_REC_1D.GetNbinsX() + 1, 0)
                                MC_GEN_1D.SetBinContent(MC_GEN_1D.GetNbinsX() + 1, 0)
                                if(MC_BGS_1D != "None"):
                                    MC_BGS_1D.SetBinContent(MC_BGS_1D.GetNbinsX() + 1, 0)
                                if(tdf not in ["N/A"]):
                                    ExTRUE_1D.SetBinContent(ExTRUE_1D.GetNbinsX() + 1, 0)
                                if("'pT'" not in out_print_main and "'pT_smeared'" not in out_print_main):
                                    ExREAL_1D.SetBinContent(1, 0)
                                    MC_REC_1D.SetBinContent(1, 0)
                                    MC_GEN_1D.SetBinContent(1, 0)
                                    if(MC_BGS_1D != "None"):
                                        MC_BGS_1D.SetBinContent(1, 0)
                                    if(tdf not in ["N/A"]):
                                        ExTRUE_1D.SetBinContent(1, 0)
                            except:
                                print(f"{color.RED}ERROR IN SETTING BIT CONTENTS{color.END}")
                                print(type(MC_REC_1D))

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("Cut: No Cuts",     "")).replace("Cut:  No Cuts", ""))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace("Cut: No Cuts", "")).replace("Cut:  No Cuts", ""))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    ExREAL_1D.GetXaxis().SetTitle(str((str(ExREAL_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    MC_REC_1D.GetXaxis().SetTitle(str((str(MC_REC_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")).replace(") (", " - ")))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace("_{t}",                                       "_{h}")))
                    MC_GEN_1D.GetXaxis().SetTitle((str(MC_GEN_1D.GetXaxis().GetTitle()).replace("_{t}",                 "_{h}")))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace("_{t}",                                   "_{h}")))
                        ExTRUE_1D.GetXaxis().SetTitle((str(ExTRUE_1D.GetXaxis().GetTitle()).replace("_{t}",             "_{h}")))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace("_{t}", "_{h}")))
                    Response_2D.GetXaxis().SetTitle(str((str(Response_2D.GetXaxis().GetTitle()).replace("_{t}",         "_{h}")).replace(") (", " - ")))
                    Response_2D.GetYaxis().SetTitle(str((str(Response_2D.GetYaxis().GetTitle()).replace("_{t}",         "_{h}")).replace(") (", " - ")))

                    Q2_Bin_Range         = "Range: 1.4805 #rightarrow 11.8705 - Size: 0.5195 per bin"
                    Q2_Bin_Replace_Range = "Range: 1.48 #rightarrow 11.87 GeV^{2} - Size: 0.52 GeV^{2}/bin"
                    xB_Bin_Range         = "Range: 0.08977 #rightarrow 0.82643 - Size: 0.0368 per bin"
                    xB_Bin_Replace_Range = "Range: 0.0898 #rightarrow 0.826 - Size: 0.0368/bin"
                    z_Bin_Range          = "Range: 0.11944 #rightarrow 0.73056 - Size: 0.0306 per bin"
                    z_Bin_Replace_Range  = "Range: 0.12 #rightarrow 0.73 - Size: 0.0306/bin"
                    pT_Bin_Range         = "Range: 0 #rightarrow 1.05 - Size: 0.0525 per bin"
                    pT_Bin_Replace_Range = "Range: 0 #rightarrow 1.05 GeV - Size: 0.0525 GeV/bin"

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(Q2_Bin_Range),     str(Q2_Bin_Replace_Range))))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(Q2_Bin_Range), str(Q2_Bin_Replace_Range))))

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(xB_Bin_Range),     str(xB_Bin_Replace_Range))))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(xB_Bin_Range), str(xB_Bin_Replace_Range))))

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(z_Bin_Range),      str(z_Bin_Replace_Range))))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(z_Bin_Range),  str(z_Bin_Replace_Range))))

                    ExREAL_1D.SetTitle((str(ExREAL_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    MC_REC_1D.SetTitle((str(MC_REC_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    MC_GEN_1D.SetTitle((str(MC_GEN_1D.GetTitle()).replace(str(pT_Bin_Range),     str(pT_Bin_Replace_Range))))
                    if("N/A" not in [tdf, ExTRUE_1D]):
                        ExTRUE_1D.SetTitle((str(ExTRUE_1D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))
                    Response_2D.SetTitle((str(Response_2D.GetTitle()).replace(str(pT_Bin_Range), str(pT_Bin_Replace_Range))))

                    if("Var-D1='Q2" in out_print_main):
                        ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV^{2}]"]))
                        if("N/A" not in [tdf, ExTRUE_1D]):
                            ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                        Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV^{2}]"]))
                        Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV^{2}]"]))

                    if("Var-D1='pT" in out_print_main):
                        ExREAL_1D.GetXaxis().SetTitle("".join([str(ExREAL_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        MC_REC_1D.GetXaxis().SetTitle("".join([str(MC_REC_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        MC_GEN_1D.GetXaxis().SetTitle("".join([str(MC_GEN_1D.GetXaxis().GetTitle()),     " [GeV]"]))
                        if("N/A" not in [tdf, ExTRUE_1D]):
                            ExTRUE_1D.GetXaxis().SetTitle("".join([str(ExTRUE_1D.GetXaxis().GetTitle()), " [GeV]"]))
                        Response_2D.GetXaxis().SetTitle("".join([str(Response_2D.GetXaxis().GetTitle()), " [GeV]"]))
                        Response_2D.GetYaxis().SetTitle("".join([str(Response_2D.GetYaxis().GetTitle()), " [GeV]"]))

                    for range_strings in ["Range: 0 #rightarrow 360 - Size: 15.0 per bin", "Range: 0 #rightarrow 4.2 - Size: 0.07 per bin"]:
                        ExREAL_1D.SetTitle(str(ExREAL_1D.GetTitle()).replace(range_strings,     ""))
                        MC_REC_1D.SetTitle(str(MC_REC_1D.GetTitle()).replace(range_strings,     ""))
                        MC_GEN_1D.SetTitle(str(MC_GEN_1D.GetTitle()).replace(range_strings,     ""))
                        if("N/A" not in [tdf, ExTRUE_1D]):
                            ExTRUE_1D.SetTitle(str(ExTRUE_1D.GetTitle()).replace(range_strings, ""))
                        Response_2D.SetTitle(str(Response_2D.GetTitle()).replace(range_strings, ""))
                    if(MC_BGS_1D != "None"):
                        MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))

                    List_of_All_Histos_For_Unfolding = New_Version_of_File_Creation(Histogram_List_All=List_of_All_Histos_For_Unfolding, Out_Print_Main=out_print_main, Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, ExTRUE_1D=ExTRUE_1D, Smear_Input="" if("mear" not in out_print_main.replace("Smear-Type", "Type")) else "Smear", Q2_Y_Bin=Q2_xB_Bin_Unfold, Z_PT_Bin=z_pT_Bin_Unfold, MC_BGS_1D=MC_BGS_1D, args=args)
                    continue

    ##===============##     Unfolding Histogram Procedure     ##===============##
    #############################################################################
    print(f"Total: {count}")
    del count
    
    BIN_SEARCH = []
    for BIN in args.Q2_y_Bin_List:
        BIN_SEARCH.append("".join(["Q2_y_Bin_", str(BIN) if(str(BIN) not in ['0', 0]) else "All", ")"]))
    
    for ii in rdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args=args))
            out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
            out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
            out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
            out_print_str     = out_print_str.replace("_smeared",              "")
            out_print_str     = out_print_str.replace("'smear'",               "Smear")
            SEARCH = []
            for BIN in BIN_SEARCH:
                SEARCH.append(str(BIN) in str(out_print_str))
                if(str(BIN) in str(out_print_str)):
                    break
            out_print_str     = out_print_str.replace("mdf",                   "rdf")
            if(True in SEARCH):
                List_of_All_Histos_For_Unfolding[out_print_str] = rdf.Get(str(out_print_main))
                if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                    for particle in ["el", "pip"]:
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        else:
                            continue
                        num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                        out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                        out_print_str_1D_Binned         = out_print_str_1D.replace(f"({particle})_",    "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                        if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                            out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                        else:
                            out_print_str_1D_Binned_Mom = "N/A"
                        for ii in range(4, num_z_pT_bins + 1):
                            z_pT_bin_value = ii - 4
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
    
    for ii in mdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if(("Normal_2D" in out_print_main) or ("Normal_Background_2D" in out_print_main)):
            out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args=args))
            out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
            out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
            out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
            out_print_str     = out_print_str.replace("_smeared",              "")
            out_print_str     = out_print_str.replace("'smear'",               "Smear")
            SEARCH = []
            for BIN in BIN_SEARCH:
                SEARCH.append(str(BIN) in str(out_print_str))
                if(str(BIN) in str(out_print_str)):
                    break
            if(True in SEARCH):
                List_of_All_Histos_For_Unfolding[out_print_str] = mdf.Get(out_print_main)
                if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                    if("Normal_Background_2D" in out_print_main):
                        continue
                    for particle in ["el", "pip"]:
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        else:
                            continue
                        num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                        out_print_str_1D = str(out_print_str.replace("(Normal_2D)",               "(1D)"))
                        out_print_str_1D = str(out_print_str_1D.replace("(Normal_Background_2D)", "(Background_1D)"))
                        out_print_str_1D_Binned = out_print_str_1D.replace(f"({particle})_",    "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                        if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                            out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                        for ii in range(4, num_z_pT_bins + 1):
                            z_pT_bin_value = ii - 4
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                
    for ii in gdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if("Normal_2D" in out_print_main):
            out_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args=args))
            out_print_str     = out_print_str.replace("_(cut_Complete_SIDIS)", "")
            out_print_str     = out_print_str.replace("cut_Complete_SIDIS_",   "")
            out_print_str     = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
            out_print_str     = out_print_str.replace("_smeared",              "")
            out_print_str     = out_print_str.replace("'smear'",               "Smear")
            SEARCH = []
            for BIN in BIN_SEARCH:
                SEARCH.append(str(BIN) in str(out_print_str))
                if(str(BIN) in str(out_print_str)):
                    break
            if(True in SEARCH):
                List_of_All_Histos_For_Unfolding[out_print_str] = gdf.Get(out_print_main)
                if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                    for particle in ["el", "pip"]:
                        if(f"({particle})_({particle}th)"    in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                            List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                        else:
                            continue
                        num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                        out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                        out_print_str_1D_Binned         = out_print_str_1D.replace(f"({particle})_",    "")
                        List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                        if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                            out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                        for ii in range(4, num_z_pT_bins + 1):
                            z_pT_bin_value = ii - 4
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                            List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
        
    if(tdf not in ["N/A"]):
        for ii in tdf.GetListOfKeys():
            out_print_main = str(ii.GetName())
            if("Normal_2D" in out_print_main):
                out_print_str = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args=args))
                out_print_str = out_print_str.replace("_(cut_Complete_SIDIS)", "")
                out_print_str = out_print_str.replace("cut_Complete_SIDIS_",   "")
                out_print_str = out_print_str.replace("(gdf)_(no_cut)",        "(gdf)")
                out_print_str = out_print_str.replace("_smeared",              "")
                out_print_str = out_print_str.replace("'smear'",               "Smear")
                SEARCH = []
                for BIN in BIN_SEARCH:
                    SEARCH.append(str(BIN) in str(out_print_str))
                    if(str(BIN) in str(out_print_str)):
                        break
                if(True in SEARCH):
                    List_of_All_Histos_For_Unfolding[out_print_str.replace("gdf", "tdf")] = tdf.Get(out_print_main)
                    if(any(kinematics in str(out_print_str) for kinematics in ["(el)_(elth)", "(el)_(elPhi)", "(pip)_(pipth)", "(pip)_(pipPhi)"])):
                        for particle in ["el", "pip"]:
                            if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xy")
                                List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                            elif(f"({particle})_({particle}Phi)" in str(out_print_str)):
                                List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")] = List_of_All_Histos_For_Unfolding[out_print_str].Project3D("xz")
                            else:
                                continue
                            num_z_pT_bins    = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].GetNbinsY()
                            out_print_str_1D = str(out_print_str.replace("(Normal_2D)", "(1D)"))
                            out_print_str_1D_Binned = out_print_str_1D.replace(f"({particle})_",    "")
                            List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned]         = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"({particle})_",   "")].ProjectionY(out_print_str_1D_Binned,     4, num_z_pT_bins)
                            if(f"({particle})_({particle}th)" in str(out_print_str_1D)):
                                out_print_str_1D_Binned_Mom = out_print_str_1D.replace(f"_({particle}th)",  "")
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom] = List_of_All_Histos_For_Unfolding[out_print_str.replace(f"_({particle}th)", "")].ProjectionX(out_print_str_1D_Binned_Mom, 4, num_z_pT_bins)
                            for ii in range(4, num_z_pT_bins + 1):
                                z_pT_bin_value = ii - 4
                                List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned].GetYaxis().SetRange(ii, ii)
                                List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")]         = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned.replace("(1D)",     "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned).replace("z_pT_Bin_All",     f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                                if(f"({particle})_({particle}th)"    in str(out_print_str)):
                                    List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom].GetYaxis().SetRange(ii, ii)
                                    List_of_All_Histos_For_Unfolding[str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}")] = List_of_All_Histos_For_Unfolding[out_print_str_1D_Binned_Mom.replace("(1D)", "(Normal_2D)")].ProjectionX(str(out_print_str_1D_Binned_Mom).replace("z_pT_Bin_All", f"z_pT_Bin_{z_pT_bin_value}"), ii, ii)
                
    # Bin-by-Bin Acceptance Corrections for 2D Histograms
    for ii in mdf.GetListOfKeys():
        try:
            out_print_main = str(ii.GetName())
            if(("Normal_2D" in out_print_main) and (not any(f"{cut}_eS" in out_print_main for cut in ["cut_Complete_SIDIS", "no_cut", "cut_Complete_SIDIS_Proton", "no_cut_Integrate", "cut_Complete_SIDIS_Integrate", "cut_Complete_SIDIS_Proton_Integrate"]))):
                mdf_print_str     = str(Histogram_Name_Def(out_print=out_print_main, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="Find", z_pT_Bin="All", Bin_Extra="Default", Variable="Default", args=args))
                mdf_print_str     = mdf_print_str.replace("_(cut_Complete_SIDIS)",           "")
                mdf_print_str     = mdf_print_str.replace("cut_Complete_SIDIS_",             "")
                mdf_print_str     = mdf_print_str.replace("(gdf)_(no_cut)",                  "(gdf)")
                mdf_print_str     = mdf_print_str.replace("_smeared",                        "")
                mdf_print_str     = mdf_print_str.replace("'smear'",                         "Smear")
                if(not args.sim):
                    rdf_print_str = str(mdf_print_str.replace("mdf", "rdf")).replace("Smear", "''")
                else:
                    rdf_print_str = str(mdf_print_str.replace("mdf", "rdf"))
                gdf_print_str     = str(mdf_print_str.replace("mdf", "gdf")).replace("Smear", "''")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(no_cut)",                  "(gdf)")
                for sector_cut_remove in range(1, 7):
                    gdf_print_str = gdf_print_str.replace(f"(gdf)_(eS{sector_cut_remove}o)", "(gdf)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Proton)",                  "(gdf)")
                # gdf_print_str     = gdf_print_str.replace(f"(gdf)_(no_cut_Integrate)",       "(gdf)_(Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Integrate)",               "(gdf)_(no_cut_Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(Proton_Integrate)",        "(gdf)_(no_cut_Integrate)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(RevPro)",                  "(gdf)")
                gdf_print_str     = gdf_print_str.replace("(gdf)_(RevPro_Integrate)",        "(gdf)_(no_cut_Integrate)")
                SEARCH = []
                for BIN in BIN_SEARCH:
                    SEARCH.append(str(BIN) in str(mdf_print_str))
                    if(str(BIN) in str(mdf_print_str)):
                        break
                if(True in SEARCH):
                    Histo_MDF = List_of_All_Histos_For_Unfolding[mdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[mdf_print_str].GetName()), "_Clone"]))
                    Histo_RDF = List_of_All_Histos_For_Unfolding[rdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[rdf_print_str].GetName()), "_Clone"]))
                    Histo_GDF = List_of_All_Histos_For_Unfolding[gdf_print_str].Clone("".join([str(List_of_All_Histos_For_Unfolding[gdf_print_str].GetName()), "_Clone"]))

                    Histo_BBB        = Histo_RDF.Clone(str(mdf_print_str).replace("mdf", "bbb"))
                    Histo_Acceptance = Histo_MDF.Clone(str(mdf_print_str).replace("mdf", "Acceptance"))
                    Histo_Acceptance.Sumw2()

                    if((Histo_MDF.GetNbinsX() != Histo_GDF.GetNbinsX()) or (Histo_MDF.GetNbinsY() != Histo_GDF.GetNbinsY()) or (Histo_MDF.GetNbinsZ() != Histo_GDF.GetNbinsZ())):
                        print(color.RED, "Histograms have different binning!", color.END)
                        print("\nHisto_MDF =",             str(mdf_print_str))
                        print("\tHisto_MDF (type) =",      str(type(Histo_MDF)))
                        print("\tHisto_MDF (Title - X) =", str(Histo_MDF.GetXaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - X) =",   str(Histo_MDF.GetNbinsX()))
                        print("\tHisto_MDF (Title - Y) =", str(Histo_MDF.GetYaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - Y) =",   str(Histo_MDF.GetNbinsY()))
                        print("\tHisto_MDF (Title - Z) =", str(Histo_MDF.GetZaxis().GetTitle()))
                        print("\tHisto_MDF (Bin - Z) =",   str(Histo_MDF.GetNbinsZ()))

                        print("\nHisto_RDF =",             str(rdf_print_str))
                        print("\tHisto_RDF (type) =",      str(type(Histo_RDF)))
                        print("\tHisto_RDF (Title - X) =", str(Histo_RDF.GetXaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - X) =",   str(Histo_RDF.GetNbinsX()))
                        print("\tHisto_RDF (Title - Y) =", str(Histo_RDF.GetYaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - Y) =",   str(Histo_RDF.GetNbinsY()))
                        print("\tHisto_RDF (Title - Z) =", str(Histo_RDF.GetZaxis().GetTitle()))
                        print("\tHisto_RDF (Bin - Z) =",   str(Histo_RDF.GetNbinsZ()))

                        print("\nHisto_GDF =",             str(gdf_print_str))
                        print("\tHisto_GDF (type) =",      str(type(Histo_GDF)))
                        print("\tHisto_GDF (Title - X) =", str(Histo_GDF.GetXaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - X) =",   str(Histo_GDF.GetNbinsX()))
                        print("\tHisto_GDF (Title - Y) =", str(Histo_GDF.GetYaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - Y) =",   str(Histo_GDF.GetNbinsY()))
                        print("\tHisto_GDF (Title - Z) =", str(Histo_GDF.GetZaxis().GetTitle()))
                        print("\tHisto_GDF (Bin - Z) =",   str(Histo_GDF.GetNbinsZ()))

                    Histo_Acceptance.Divide(Histo_GDF)
                    Histo_BBB.Divide(Histo_Acceptance)
                    Histo_BBB.SetName(str(mdf_print_str).replace("mdf", "bbb"))
                    List_of_All_Histos_For_Unfolding[mdf_print_str.replace("mdf", "bbb")] = Histo_BBB
        except:
            print(f"{color.Error}ERROR! See:{color.END_B}\n\tBin-by-Bin Acceptance Corrections for 2D Histograms{color.END}")
            print(f"Traceback:\n{traceback.format_exc()}")
                
    return Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding)

def Load_TTree(args):
    args.single_file_input = args.root
    TTree_Name = args.root
    Relative_Background_Run_Q = False
    print(f"\n{color.Error}Using Existing TTree {color.END_B}(File is: {color.UNDERLINE}{TTree_Name}{color.END_B}){color.Error} instead of Creating New Unfolded Histograms{color.END}\n")
    TTree_Input = ROOT.TFile.Open(TTree_Name, "READ")
    List_of_All_Histos_For_Unfolding = {}
    keys = TTree_Input.GetListOfKeys()
    for key in keys:
        key_name = key.GetName()
        if("_AsymErr" in key_name):
            continue
        if(not Relative_Background_Run_Q):
            Relative_Background_Run_Q = "Relative_Background" in str(key_name)
        if("TList_of_" in key_name):
            List_of_All_Histos_For_Unfolding[key_name] = [float(str(item.GetString())) for item in TTree_Input.Get(key_name)]
        elif("TVectorD_" in key_name):
            List_of_All_Histos_For_Unfolding[key_name.replace("TVectorD_", "")] = list(TTree_Input.Get(key_name))
            # print(f"""List_of_All_Histos_For_Unfolding[{key_name.replace("TVectorD_", "")}] = {list(TTree_Input.Get(key_name))}""")
        else:
            List_of_All_Histos_For_Unfolding[key_name] = TTree_Input.Get(key_name)
            asym_key = f"{key_name}_AsymErr"
            if(keys.FindObject(asym_key)):
                List_of_All_Histos_For_Unfolding[key_name].asym_errors = TTree_Input.Get(asym_key)
    TTree_Input.Close()
    print(f"{color.BBLUE}Recovered: {color.BGREEN}{len(List_of_All_Histos_For_Unfolding)}{color.END_B}{color.BLUE} items{color.END}\n")
    args.timer.time_elapsed()
    return args, List_of_All_Histos_For_Unfolding

def Create_Fits_and_Apply_RC_and_BC(args, List_of_All_Histos_For_Unfolding):
    # TTree_Name = args.root
    if((args.fit and args.Use_TTree) or args.Apply_RC): # does not include 'Apply_BC' because it always assumes that the BC corrections already exist—this function is only useful for the BC corrections in so far as fitting is concerned
        fits_included    = args.remake_fit
        BC_fits_included = not args.Apply_BC # if args.Apply_BC = False, then there is no need to create the BC fits anyway
        RC_fits_included = not args.Apply_RC # if args.Apply_RC = False, then there is no need to create the RC fits anyway
        RC_included      = not args.Apply_RC # checks to see if the RC plots were already created (but not fit)
        for List_of_All_Histos_For_Unfolding_ii in List_of_All_Histos_For_Unfolding:
            if("(Fit_Par" in str(List_of_All_Histos_For_Unfolding_ii)):
                fits_included    = True
            if("(Fit_Par_B)_(BC" in str(List_of_All_Histos_For_Unfolding_ii)):
                BC_fits_included = True
            if("(Fit_Par_B)_(RC" in str(List_of_All_Histos_For_Unfolding_ii)):
                RC_fits_included = True
                RC_included      = True
            if(")_(RC_Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)):
                RC_included      = True
            if(fits_included and RC_fits_included and BC_fits_included):
                break
        if(args.remake_fit):
            fits_included = False
        print(f"{color.BLUE}Normal Unfolding Fits Already Included? -> {color.BGREEN if(fits_included) else color.Error}{fits_included}{color.END}")
        if(not args.Apply_RC):
            print(f"{color.BOLD}Not running RC... Did not check for RC fits.{color.END}")
        else:
            print(f"{color.BLUE}RC Unfolding Fits Already Included?     -> {color.BGREEN if(RC_fits_included) else color.Error}{RC_fits_included}{color.END}")
        if(not args.Apply_BC):
            print(f"{color.BOLD}Not running BC... Did not check for BC fits.{color.END}")
        else:
            print(f"{color.BLUE}BC Unfolding Fits Already Included?     -> {color.BGREEN if(BC_fits_included) else color.Error}{BC_fits_included}{color.END}")

        if((not (fits_included and RC_fits_included and BC_fits_included)) or args.remake_fit):
            print(f"\n{color.BBLUE}Making the fits...{color.END}\n")
            script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code'
            sys.path.append(script_dir)
            from Find_RC_Fit_Params import Find_RC_Fit_Params, Apply_RC_Factor_Corrections, Get_RC_Fit_Plot
            sys.path.remove(script_dir)
            del script_dir
            print(f"\n{color.BOLD}Loaded `{color.GREEN}Find_RC_Fit_Params{color.END_B}` and `{color.GREEN}Apply_RC_Factor_Corrections{color.END_B}` for applying RC Corrections...{color.END}\n")
            Histogram_Fit_List_All = {}
            fit_count = 0
            for ii, List_of_All_Histos_For_Unfolding_ii in enumerate(List_of_All_Histos_For_Unfolding):
                if(any(Fit_objects in str(List_of_All_Histos_For_Unfolding_ii) for Fit_objects in ["Fit_Function", "Chi_Squared", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C"])):
                    continue
                if("Bin_All)"  in str(List_of_All_Histos_For_Unfolding_ii)):
                    continue
                if("_EvGen"    in str(List_of_All_Histos_For_Unfolding_ii)):
                    continue
                if(("BC_"      in str(List_of_All_Histos_For_Unfolding_ii)) and (not args.Apply_BC)):
                    continue
                if(args.EvGen and ("Acceptance" in str(List_of_All_Histos_For_Unfolding_ii)) and ("_EvGen" not in str(List_of_All_Histos_For_Unfolding_ii))):
                    Histo_clasdis        = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
                    Histo_Name_EvGen     = f"{Histo_clasdis.GetName()}_EvGen"
                    Histo_Name_EvGen     = Histo_Name_EvGen.replace("Smear", "''")
                    if(Histo_Name_EvGen not in List_of_All_Histos_For_Unfolding):
                        if(Histo_Name_EvGen.replace("V1", "V2") in List_of_All_Histos_For_Unfolding):
                            Histo_Name_EvGen = Histo_Name_EvGen.replace("V1", "V2")
                            print(f"{color.Error}Warning:{color.END} Needed to switch to 'V2' to use '{Histo_Name_EvGen}'\n")
                        else:
                            print(f"{color.Error}Could not find EvGen Acceptance ({Histo_Name_EvGen}){color.END}")
                            continue
                    match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_EvGen))
                    if(match):
                        Q2_Y_Bin_Fitting = int(match.group(1))
                        Z_PT_Bin_Fitting = int(match.group(2))
                    else:
                        print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                        continue
                    if(str(Q2_Y_Bin_Fitting) not in args.Q2_y_Bin_List):
                        continue
                    Histo_Name_ratio     = str(Histo_clasdis.GetName()).replace("(Acceptance)", "(Acceptance_ratio)")
                    Hist_AcceptanceRatio = List_of_All_Histos_For_Unfolding[Histo_Name_EvGen].Clone(Histo_Name_ratio)
                    Hist_AcceptanceRatio.Divide(Histo_clasdis)
                    Hist_AcceptanceRatio.SetTitle(Hist_AcceptanceRatio.GetTitle().replace("Bin-by-Bin Acceptance", "Ratio of #frac{EvGen}{clasdis} Acceptances"))
                    Hist_AcceptanceRatio.GetYaxis().SetTitle("#frac{EvGen}{clasdis} Acceptance Ratio")
                    Hist_AcceptanceRatio.SetLineColor(ROOT.kAzure + 3)
                    Hist_AcceptanceRatio.SetLineWidth(2)
                    Hist_AcceptanceRatio.SetLineStyle(1)
                    Histogram_Fit_List_All[Histo_Name_ratio] = Hist_AcceptanceRatio
                    fit_count += 1
                if(any(acceptable_unfold in str(List_of_All_Histos_For_Unfolding_ii) for acceptable_unfold in args.Unfold_Methods)):
                    Histo_Original       = List_of_All_Histos_For_Unfolding[List_of_All_Histos_For_Unfolding_ii]
                    Histo_Name_General   = Histo_Original.GetName()
                    match = re.search(r"Q2_y_Bin_(\d+).*z_pT_Bin_(\d+)", str(Histo_Name_General))
                    if(match):
                        Q2_Y_Bin_Fitting = int(match.group(1))
                        Z_PT_Bin_Fitting = int(match.group(2))
                    else:
                        print(f"\n{color.Error}Error: Could not find kinematics bins for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                        continue
                    if(str(Q2_Y_Bin_Fitting) not in args.Q2_y_Bin_List):
                        # print(f"\n{color.RED}Not Using Histograms from Q2-y Bin {color.UNDERLINE}{Q2_Y_Bin_Fitting}{color.END}")
                        continue
                    if((args.Add_Uncertainties) and (not hasattr(Histo_Original, "asym_errors"))):
                        Histo_Original = Apply_PreBin_Uncertainties(Histo_In=Histo_Original, Q2_y_Bin=Q2_Y_Bin_Fitting, z_pT_Bin=Z_PT_Bin_Fitting, Uncertainty_File_In=Uncertainty_File)
                    Dimensions_Original = "1D" if("1D" in Histo_Name_General) else "MultiDim_3D_Histo" if("MultiDim_3D_Histo" in Histo_Name_General) else "MultiDim_5D_Histo" if("MultiDim_5D_Histo" in Histo_Name_General) else "Error"
                    if(Dimensions_Original == "Error"):
                        print(f"\n{color.Error}Error: Could not find unfolding dimensions for {color.UNDERLINE}{Histo_Name_General}{color.END}\n")
                        continue
                    print(f"Fitting for: {color.BOLD}{List_of_All_Histos_For_Unfolding_ii}{color.END} (Histo Num {ii:>5.0f})")
                    Histo_Name_Rad_Cor          = str(Histo_Name_General.replace("(Bin)", "(RC_Bin)")).replace("Bayesian", "RC_Bayesian")
                    RC_RooUnfolded_TTree_Histos = Histo_Original.Clone(Histo_Name_Rad_Cor)
                    if((not fits_included) and args.fit):
                        RooUnfolded_TTree_Histos, Unfolded_TTree_Fit_Function, Chi_Squared_TTree, TTree_Fit_Par_A, TTree_Fit_Par_B, TTree_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=Histo_Original, Method=f'{"BC_" if("BC" in str(List_of_All_Histos_For_Unfolding_ii)) else ""}{"RC_Bayesian" if("RC_Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) else "Bayesian" if("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) else "Bin"}', Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting], args=args)
                        Histogram_Fit_List_All[str(Histo_Name_General)]                                                = RooUnfolded_TTree_Histos.Clone(str(Histo_Name_General))
                        Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Function")]   = Unfolded_TTree_Fit_Function.Clone(str(Histo_Name_General).replace(Dimensions_Original, "Fit_Function"))
                        Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Chi_Squared")]    = Chi_Squared_TTree
                        Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_A")]      = TTree_Fit_Par_A
                        Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_B")]      = TTree_Fit_Par_B
                        Histogram_Fit_List_All[str(Histo_Name_General).replace(Dimensions_Original, "Fit_Par_C")]      = TTree_Fit_Par_C
                        fit_count += 1
                        #FIND SINGLE FILE FITS
                    if(args.Apply_RC and ("BC_" not in str(List_of_All_Histos_For_Unfolding_ii)) and ((not RC_included) or ("RC_Bin" in Histo_Name_Rad_Cor))):
                        RC_Par_A, RC_Err_A, RC_Par_B, RC_Err_B, RC_Par_C, RC_Err_C = Find_RC_Fit_Params(Q2_y_bin=Q2_Y_Bin_Fitting, z_pT_bin=Z_PT_Bin_Fitting, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", cache_in=None, cache_out=None, quiet=True)
                        RC_RooUnfolded_TTree_Histos = Apply_RC_Factor_Corrections(hist=RC_RooUnfolded_TTree_Histos, Par_A=RC_Par_A, Par_B=RC_Par_B, Par_C=RC_Par_C, use_param_errors=True, Par_A_err=RC_Err_A, Par_B_err=RC_Err_B, Par_C_err=RC_Err_C, param_cov=None)
                        RC_RooUnfolded_TTree_Histos, RC_Unfolded_TTree_Fit_Function, RC_Chi_Squared_TTree, RC_TTree_Fit_Par_A, RC_TTree_Fit_Par_B, RC_TTree_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RC_RooUnfolded_TTree_Histos, Method="RC_Bayesian" if("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) else "RC_Bin", Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting], args=args)
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor)]                                                = RC_RooUnfolded_TTree_Histos.Clone(str(Histo_Name_Rad_Cor))
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Function")]   = RC_Unfolded_TTree_Fit_Function.Clone(str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Function"))
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Chi_Squared")]    = RC_Chi_Squared_TTree
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_A")]      = RC_TTree_Fit_Par_A
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_B")]      = RC_TTree_Fit_Par_B
                        Histogram_Fit_List_All[str(Histo_Name_Rad_Cor).replace(Dimensions_Original, "Fit_Par_C")]      = RC_TTree_Fit_Par_C
                        fit_count += 1
                        if(("Bayesian" in str(List_of_All_Histos_For_Unfolding_ii)) and ("1D" in Histo_Name_General)):
                            print(f"\n{color.BBLUE}Grabbing the RC vs phi_h plot for {color.END_B}Bin {Q2_Y_Bin_Fitting}-{Z_PT_Bin_Fitting}{color.BLUE}...{color.END}\n")
                            RC_Factor_Plot = Get_RC_Fit_Plot(Q2_y_bin=Q2_Y_Bin_Fitting, z_pT_bin=Z_PT_Bin_Fitting, root_in="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root", quiet=True, plot_choice="RC_factor")
                            RC_Factor_Plot, RC_Factor_Plot_Fit_Function, RC_Factor_Chi_Squared_Plot, RC_Factor_Fit_Par_A, RC_Factor_Fit_Par_B, RC_Factor_Fit_Par_C = Fitting_Phi_Function(Histo_To_Fit=RC_Factor_Plot, Method="RC", Special=[Q2_Y_Bin_Fitting, Z_PT_Bin_Fitting], args=args)
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC"))]                                                = RC_Factor_Plot.Clone(str(Histo_Name_General).replace("Bayesian", "RC"))
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Function")]   = RC_Factor_Plot_Fit_Function.Clone(str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Function"))
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Chi_Squared")]    = RC_Factor_Chi_Squared_Plot
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_A")]      = RC_Factor_Fit_Par_A
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_B")]      = RC_Factor_Fit_Par_B
                            Histogram_Fit_List_All[str(str(Histo_Name_General).replace("Bayesian", "RC")).replace(Dimensions_Original, "Fit_Par_C")]      = RC_Factor_Fit_Par_C
                            fit_count += 1
            print(f"\n{color.BBLUE}Fit/Added {color.END_B}{fit_count}{color.BBLUE} Histograms{color.END_b}\nAdding to Main List...{color.END}")
            for name_ii in Histogram_Fit_List_All:
                List_of_All_Histos_For_Unfolding[name_ii] = Histogram_Fit_List_All[name_ii]
            print(f"\n{color.BGREEN}Length of Main List of Histograms (After adding Fits): {color.END_B}{len(List_of_All_Histos_For_Unfolding)}{color.END}\n")
        else:
            print(f"{color.BOLD}Fits are all already made{color.END}")
        args.timer.time_elapsed()
        return Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding)
    else:
        print("Conditions for running 'Create_Fits_and_Apply_RC_and_BC' were not set...\nNeed to run: '(args.fit and args.Use_TTree) or args.Apply_RC'")
        return List_of_All_Histos_For_Unfolding

def main():
    args = main_start()
    if(args.Use_TTree):
        try:
            args, List_of_All_Histos_For_Unfolding = Load_TTree(args)
        except:
            Crash_Report(args, crash_message=f"The Load TTree Code has CRASHED!\nERROR MESSAGE:\n\n{traceback.format_exc()}")
    else:
        try:
            List_of_All_Histos_For_Unfolding = main_unfold(args)
        except:
            Crash_Report(args, crash_message=f"The Unfolding Code has CRASHED!\nERROR MESSAGE:\n\n{traceback.format_exc()}")
    try:
        List_of_All_Histos_For_Unfolding = Create_Fits_and_Apply_RC_and_BC(args, List_of_All_Histos_For_Unfolding)
        if(not ((args.fit and args.Use_TTree) or args.Apply_RC)):
            List_of_All_Histos_For_Unfolding =  Save_Histos_To_ROOT(args, List_of_All_Histos_For_Unfolding)
        if(args.save_json and args.fit):
            for acceptable_unfold in args.Unfold_Methods:
                acceptable_unfold           = str(acceptable_unfold.replace("(", "")).replace(")", "")
                args, Fit_Pars_JSON         = Save_Fit_Pars_To_JSON(args, List_of_All_Histos_For_Unfolding, cor_type=acceptable_unfold)
                if(args.Apply_RC):
                    args, Fit_Pars_JSON     = Save_Fit_Pars_To_JSON(args, List_of_All_Histos_For_Unfolding, cor_type=f"RC_{acceptable_unfold}")
                    if(args.Apply_BC):
                        args, Fit_Pars_JSON = Save_Fit_Pars_To_JSON(args, List_of_All_Histos_For_Unfolding, cor_type=f"BC_RC_{acceptable_unfold}")
                elif(args.Apply_BC):
                    args, Fit_Pars_JSON     = Save_Fit_Pars_To_JSON(args, List_of_All_Histos_For_Unfolding, cor_type=f"BC_{acceptable_unfold}")
    except:
        Crash_Report(args, crash_message=f"{color.Error}The Fitting/RC Code has CRASHED!\n{color.END_R}ERROR MESSAGE:\n\n{color.END}{traceback.format_exc()}")
    Construct_Email(args, final_count=len(List_of_All_Histos_For_Unfolding))

if(__name__ == "__main__"):
    main()

