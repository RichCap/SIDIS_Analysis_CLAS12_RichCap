#!/usr/bin/env python3
# Dedicated 5D Bayesian unfolding for MultiDim_Q2_y_z_pT_phi_h histograms.

import sys
import ROOT
import traceback
import os
import re
import argparse
from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

ROOT.gROOT.SetBatch(1)
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')
ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)
ROOT.gStyle.SetStatX(0.80)
ROOT.gStyle.SetStatY(0.45)
ROOT.gStyle.SetStatW(0.3)
ROOT.gStyle.SetStatH(0.2)

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    p = argparse.ArgumentParser(description="Dedicated_5D_Unfold.py analysis script:\n\tMeant for JUST doing the 5D (Bayesian) Unfolding Procedure before saving outputs to a ROOT file.",
                                formatter_class=RawDefaultsHelpFormatter)
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save',
                   action='store_true',
                   dest='test',
                   help="Run full code but without saving any files.\n")
    p.add_argument('-r', '--root',
                   type=str,
                   default="Unfolded_5D_Histos_From_Dedicated_5D_Unfold.root",
                   help="Name of ROOT output file to be saved.\n")
    p.add_argument('-no-smear', '--no_smear',
                   action='store_true',
                   help="Unfold with unsmeared Monte Carlo only.\n")
    p.add_argument('-sim', '--simulation',
                   action='store_true',
                   dest='sim',
                   help="Use reconstructed MC instead of experimental data.\n")
    p.add_argument('-mod', '--modulation',
                   action='store_true',
                   dest='mod',
                   help="Use modulated MC files to create response matrices.\n")
    p.add_argument('-bi', '-bayes-it', '--bayes_iterations',
                   type=int,
                   default=6,
                   help="Number of Bayesian Iterations performed while Unfolding.\n")
    p.add_argument('-nt', '-ntoys', '--Num_Toys',
                   type=int,
                   default=10,
                   help="Number of Toys used to estimate the unfolding errors.\n")
    p.add_argument('-b', '--bins',
                   nargs="+",
                   type=str,
                   default=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                   help="List of Q2-y bin indices to run.\n")
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Prints each Histogram name to be saved.\n")
    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut',
                   type=float,
                   default=0.0005,
                   help="Cut made on acceptance before a bin is removed from unfolding.\n")
    p.add_argument('-sfin', '--single_file_input',
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_wFitIntegration_V5_Response_Matrices_Final_Analysis_Iterations_I0_All.root",
                   help="Path to the INPUT ROOT file.\n")
    p.add_argument('-e', '--email',
                   action='store_true',
                   help="Sends an email to user when done running.\n")
    p.add_argument('-em', '--email_message',
                   type=str,
                   default="",
                   help="Extra email message (use with --email).\n")
    p.add_argument('-bgs', '--background_source',
                   type=str,
                   default="lundvpk",
                   choices=["lundrho", "lundvpk", "None"],
                   help="Source of rho0 background subtractions from rdf.\n")
    p.add_argument('-rw', '--require_weighed',
                   action='store_true',
                   help="Require _(Weighed) on mdf/gdf/slice keys (default: reject weighed).\n")
    p.add_argument('-i', '--increment',
                   type=int,
                   default=None,
                   help="Optional: force slice increment; crashes if mismatch with auto-detect.\n")
    p.add_argument('-nb', '--num_bins',
                   type=int,
                   default=None,
                   help="Optional: force flattened 5D bin count; crashes if mismatch with auto-detect.\n")
    p.add_argument('-mpdf', '--matrix_pdf',
                   action='store_true',
                   help="Rebuild the 5D response matrix and save a PDF only (no unfolding).\n")
    p.add_argument('-pdf', '--pdf_name',
                   type=str,
                   default="Rebuilt_5D_Response_Matrix.pdf",
                   help="PDF output path for --matrix_pdf mode.\n")
    p.add_argument('-lz', '--logz',
                   action='store_true',
                   help="Use log scale on the PDF Z-axis.\n")
    p.add_argument('-rs', '--recover_slices',
                   action='store_true',
                   help="Skip unfolding; load existing args.root, rename/resave the raw 'unfolded' hist if needed, and only run Multi5D_Slice for Bayesian.\n")
    return p.parse_args()

def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()
    
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
    elapsed_line = args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')
    if(update_message not in [""]):
        update_email = f"""{update_message}
{elapsed_line}"""
    elif(update_name not in [""]):
        update_email = f"""
{color.BCYAN}{update_name}{color.END_B} is done running...{color.END}
{elapsed_line}

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
        if(str(name) in ["email", "email_message", "timer", "fit", "increment_5d", "num_bins_5d", "num_slices_5d", "pdf_name", "root", "single_file_input"]):
            continue
        args_list = f"""{args_list}
--{name:<50s}--> {f"'{value}'" if(type(value) is str) else value}"""
    email_body = f"""
The 'Dedicated_5D_Unfold.py' script has {'finished running.' if(not (Crashed or Warning)) else f'{color.ERROR}CRASHED!{color.END}' if(not Warning) else f'{color.BYELLOW}GIVEN A WARNING MESSAGE{color.END}'}
{start_time}

Input File:
\t{args.single_file_input}
Output File:
\t{args.pdf_name if(getattr(args, 'matrix_pdf', False)) else args.root}

{args.email_message}

Detected 5D Configuration:
	increment  = {getattr(args, 'increment', 'N/A')}
	num_bins   = {getattr(args, 'num_bins', 'N/A')}
	num_slices = {getattr(args, 'num_slices_5d', 'N/A')}

Arguments:{args_list}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'Dedicated_5D_Unfold.py' Code" if(not (Crashed or Warning)) else f"{'CRASH' if(Crashed) else 'ERROR'} REPORT: 'Dedicated_5D_Unfold.py' Code {'Failed' if(Crashed) else 'is still running...'}", body=email_body, recipient="richard.capobianco@uconn.edu")
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
                Unfolded_Histo.SetName(f"""(MultiDim_5D_Histo)_(Bayesian)_(SMEAR={"Smear" if("smear" in str(Name_Main).lower()) else "''"})_(Q2_y_z_pT_Bin_All)_(MultiDim_Q2_y_z_pT_phi_h)""")

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

def subtract_bkg_with_zero_floor(hist_data, hist_background):
    original_name = hist_data.GetName()
    orginal_histo = hist_data.Clone(f"{original_name}_(wExclusive_Background)")
    orginal_histo.SetTitle(f"#splitline{{{orginal_histo.GetTitle()}}}{{#scale[2]{{Before the Exclusive #rho^{{0}} Background Subtraction}}}}")
    result_histogram = hist_data.Clone(original_name)
    result_histogram.SetDirectory(0)
    result_histogram.Add(hist_background, -1.0)
    for global_bin in range(result_histogram.GetNcells()):
        if(result_histogram.GetBinContent(global_bin) < 0):
            result_histogram.SetBinContent(global_bin, 0.0)
    return orginal_histo, result_histogram


################################################################################################################################################################################################################################################
##==========##==========##        5D Detection / Validation Helpers                ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
SLICE_INCREMENT_RE = re.compile(r"_Slice_1_\(Increment='(\d+)'\)")

def Passes_Weighed_Filter(name, args):
    if(args.require_weighed):
        if("_(Weighed)" not in name):
            return False
    else:
        if("_(Weighed)" in name):
            return False
    return True

def Is_5D_Matrix_Slice_Candidate(name, args):
    if("MultiDim_Q2_y_z_pT_phi_h" not in name):
        return False
    if("_Slice_1_(Increment='" not in name):
        return False
    if("5D_Response_Matrix_1D" in name):
        return False
    if("Response_Matrix_Normal_1D" in name):
        return False
    if("Background" in name):
        return False
    if("cut_Complete_SIDIS" not in name):
        return False
    if("cut_Complete_SIDIS_eS" in name):
        return False
    if("cut_Complete_EDIS" in name):
        return False
    if("no_cut_eS" in name):
        return False
    if(any(x in name for x in ["_(lundvpk)", "_(lundrho)"])):
        return False
    if(not Passes_Weighed_Filter(name, args)):
        return False
    if(("5D_Response_Matrix" in name) and ("_Slice_" in name)):
        pass
    elif(("Response_Matrix_Normal" in name) and ("_Slice_" in name)):
        pass
    else:
        return False
    if((args.smearing_options not in ["no_smear", "both"]) and ("(Smear-Type='')" in name)):
        return False
    if((args.smearing_options not in ["smear", "both"]) and ("(Smear-Type='smear')" in name)):
        return False
    return True

def Strip_Slice_Increment(name):
    return SLICE_INCREMENT_RE.sub("", name)

def Apply_Matrix_1D_Replacements(name):
    name = name.replace("'5D_Response_Matrix'", "'5D_Response_Matrix_1D'")
    name = name.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
    return name

def Apply_Background_1D_Replacements(name):
    name = name.replace("'5D_Response_Matrix_1D'", "'Background_5D_Response_Matrix_1D'")
    name = name.replace("'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'")
    return name

def Build_5D_Matrix_Candidate(mdf, out_print_main):
    out_print_main_mdf = out_print_main
    m_inc = SLICE_INCREMENT_RE.search(out_print_main_mdf)
    if(not m_inc):
        return None
    detected_increment = int(m_inc.group(1))
    Base_Name = out_print_main_mdf.replace("_Slice_1_", "_Slice_NUMBER_")
    Slice_Num, Histo_List = 1, {}
    while(Slice_Num < 800):
        histo_sliced = mdf.Get(Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_"))
        if(histo_sliced):
            Histo_List[Base_Name.replace("_Slice_NUMBER_", f"_Slice_{Slice_Num}_")] = histo_sliced
            Slice_Num += 1
        else:
            break
    num_slices = len(Histo_List)
    if(num_slices < 1):
        return None
    slice1 = Histo_List[Base_Name.replace("_Slice_NUMBER_", "_Slice_1_")]
    if(detected_increment != slice1.GetNbinsX()):
        detected_increment = int(slice1.GetNbinsX())
    Num__Bins, Min_Range, Max_Range = Find_Bins_From_Histo_Name(out_print_main_mdf)
    out_print_main_mdf_base = Strip_Slice_Increment(out_print_main_mdf)
    out_print_main_mdf_1D = Apply_Matrix_1D_Replacements(out_print_main_mdf_base)
    return {
        "out_print_main": out_print_main,
        "out_print_main_mdf": out_print_main_mdf,
        "out_print_main_mdf_base": out_print_main_mdf_base,
        "out_print_main_mdf_1D": out_print_main_mdf_1D,
        "Histo_List": Histo_List,
        "increment": detected_increment,
        "num_bins": int(Num__Bins),
        "num_slices": num_slices,
        "Min_Range": Min_Range,
        "Max_Range": Max_Range,
    }

def Select_5D_Matrix_Candidate(candidates, mdf, args):
    if(not candidates):
        return None
    filtered = list(candidates)
    if(args.increment is not None):
        filtered = [c for c in filtered if(c["increment"] == int(args.increment))]
        if(not filtered):
            Crash_Report(args, crash_message=f"No 5D matrix found with --increment={args.increment}")
    if(args.num_bins is not None):
        filtered = [c for c in filtered if(c["num_bins"] == int(args.num_bins))]
        if(not filtered):
            Crash_Report(args, crash_message=f"No 5D matrix found with --num_bins={args.num_bins}")
    if(len(filtered) == 1):
        return filtered[0]
    consistent = [c for c in filtered if(c["increment"] * c["num_slices"] == c["num_bins"])]
    if(consistent):
        filtered = consistent
    verified = []
    for c in filtered:
        if(c["out_print_main_mdf_1D"] not in mdf.GetListOfKeys()):
            continue
        MC_REC_1D_test = mdf.Get(c["out_print_main_mdf_1D"])
        if(MC_REC_1D_test and int(MC_REC_1D_test.GetNbinsX()) == c["num_bins"]):
            verified.append(c)
    if(verified):
        filtered = verified
    if(len(filtered) > 1):
        filtered.sort(key=lambda c: c["num_bins"], reverse=True)
        print(f"\n{color.BYELLOW}Multiple 5D matrix configurations found; using increment={filtered[0]['increment']}, num_bins={filtered[0]['num_bins']}, num_slices={filtered[0]['num_slices']}{color.END}\n")
    return filtered[0]

def Detect_5D_Matrix_Config(mdf, args):
    candidates = []
    for ii in mdf.GetListOfKeys():
        out_print_main = str(ii.GetName())
        if(not Is_5D_Matrix_Slice_Candidate(out_print_main, args)):
            continue
        candidate = Build_5D_Matrix_Candidate(mdf, out_print_main)
        if(candidate is not None):
            candidates.append(candidate)
    return Select_5D_Matrix_Candidate(candidates, mdf, args)

def Validate_And_Record_5D_Dimensions(args, detected, MC_REC_1D):
    args.increment_5d = int(detected["increment"])
    args.num_bins_5d = int(detected["num_bins"])
    args.num_slices_5d = int(detected["num_slices"])
    if(MC_REC_1D is not None):
        if(int(MC_REC_1D.GetNbinsX()) != args.num_bins_5d):
            Crash_Report(args, crash_message=f"MC_REC_1D.GetNbinsX()={MC_REC_1D.GetNbinsX()} != auto-detected num_bins={args.num_bins_5d}")
        if(args.increment_5d * args.num_slices_5d != args.num_bins_5d):
            Crash_Report(args, crash_message=f"increment*num_slices ({args.increment_5d}*{args.num_slices_5d}) != num_bins ({args.num_bins_5d})")
    if(args.increment is not None):
        if(int(args.increment) != args.increment_5d):
            Crash_Report(args, crash_message=f"User --increment={args.increment} != auto-detected {args.increment_5d}")
        args.increment_5d = int(args.increment)
    else:
        args.increment = args.increment_5d
    if(args.num_bins is not None):
        if(int(args.num_bins) != args.num_bins_5d):
            Crash_Report(args, crash_message=f"User --num_bins={args.num_bins} != auto-detected {args.num_bins_5d}")
        args.num_bins_5d = int(args.num_bins)
    else:
        args.num_bins = args.num_bins_5d
    print(f"\n{color.BOLD}Auto-detected 5D configuration:{color.END} increment={args.increment_5d}, num_bins={args.num_bins_5d}, num_slices={args.num_slices_5d}\n")

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Rebuild Function            ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Rebuild_Matrix_5D(List_of_Sliced_Histos, Standard_Name, Increment=None, Title="Default"):
    Num__Bins, Min_Range, Max_Range = Find_Bins_From_Histo_Name(Standard_Name)
    if(Increment is None):
        m_inc = SLICE_INCREMENT_RE.search(Standard_Name)
        if(m_inc):
            Increment = int(m_inc.group(1))
        else:
            Slicing_Name_Test = f"{Standard_Name}_Slice_1_(Increment='0')"
            for key in List_of_Sliced_Histos:
                m2 = re.search(r"_Slice_1_\(Increment='(\d+)'\)", key)
                if(m2):
                    Increment = int(m2.group(1))
                    break
            if(Increment is None):
                first_key = list(List_of_Sliced_Histos.keys())[0]
                Increment = List_of_Sliced_Histos[first_key].GetNbinsX()
    Slicing_Name = f"{Standard_Name}_Slice_SLICE-NUM_(Increment='{Increment}')"
    print(f"\n{color.BBLUE}Running Rebuild_Matrix_5D(...){color.END}\n")
    Num_Slices = int(Num__Bins/Increment)
    for test in ["1", str(Num_Slices)]:
        if(Slicing_Name.replace("SLICE-NUM", str(test)) not in List_of_Sliced_Histos):
            missing_name = Slicing_Name.replace("SLICE-NUM", str(test))
            print(f"{color.Error}ERROR IN Rebuild_Matrix_5D(...): {color.END_R}'Slicing_Name' is missing from 'List_of_Sliced_Histos'{color.END_B}\n\tSlicing_Name = {missing_name}")
            return "ERROR"
    Histo_Title = Title if(Title not in ["Default"]) else "".join([str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetXaxis().GetTitle()), ";", str(List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", "1")].GetYaxis().GetTitle())])
    Rebuilt_5D_Matrix = ROOT.TH2D(str(Standard_Name), str(Histo_Title), Num__Bins, Min_Range, Max_Range, Num__Bins, Min_Range, Max_Range)
    X_Bin_5D = 0
    for slice_num in range(1, Num_Slices + 1):
        Histo_Add = List_of_Sliced_Histos[Slicing_Name.replace("SLICE-NUM", str(slice_num))]
        X_Bin_5D += -1
        for x_bin in range(0, Histo_Add.GetNbinsX() + 1):
            X_Bin_5D += 1
            for y_bin in range(0, Histo_Add.GetNbinsY() + 1):
                Rebuilt_5D_Matrix.SetBinContent(X_Bin_5D, y_bin, Histo_Add.GetBinContent(x_bin, y_bin))
                Rebuilt_5D_Matrix.SetBinError(X_Bin_5D,   y_bin, Histo_Add.GetBinError(x_bin,   y_bin))
    print(f"\n{color.BGREEN}Finished running Rebuild_Matrix_5D(...){color.END}\n")
    return Rebuilt_5D_Matrix


def _Coerce_Kinematic_Bin_Value(bin_value):
    if(bin_value in ["ERROR", "Error", None, ""]):
        return None
    try:
        return int(bin_value)
    except(TypeError, ValueError):
        return None


def _First_Valid_MultiDim_Start(Q2_y, z_pT_min=1, z_pT_max=None):
    # First dense-5D MultiDim start bin for this Q2-y (skips migration edge z-pT bins that are not in the map).
    if(z_pT_max is None):
        z_pT_max = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
    for z_pT in range(int(z_pT_min), int(z_pT_max) + 1):
        start_bin = _Coerce_Kinematic_Bin_Value(Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h"))
        if(start_bin is not None):
            return start_bin
    return None


def _Resolve_Phi_h_Slice_Range(Q2_y, z_pT, phi_h_Binning):
    # Dense 5D packing: each kept (Q2-y, z-pT) block is exactly phi_h_Binning[2] MultiDim bins wide.
    # Do NOT require z-pT=1 or contiguous z-pT numbering — skip_condition_z_pT_bins leaves holes (e.g. Q2-y=4 starts at z-pT=7).
    if(z_pT not in [0]):
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y, Z_PT_BIN=z_pT, BINNING_METHOD="Y_bin")):
            return None
        Start_phi_h_bin = _Coerce_Kinematic_Bin_Value(Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h"))
        if(Start_phi_h_bin is None):
            return None
        End___phi_h_bin = Start_phi_h_bin + phi_h_Binning[2]
    else:
        z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
        Start_phi_h_bin = _First_Valid_MultiDim_Start(Q2_y, z_pT_min=1, z_pT_max=z_pT_Range)
        if(Start_phi_h_bin is None):
            return None
        End___phi_h_bin = _First_Valid_MultiDim_Start(int(Q2_y) + 1, z_pT_min=1)
        if(End___phi_h_bin is None):
            last_start = Start_phi_h_bin
            for z_test in range(1, z_pT_Range + 1):
                start_test = _Coerce_Kinematic_Bin_Value(Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_test}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h"))
                if(start_test is not None):
                    last_start = start_test
            End___phi_h_bin = last_start + phi_h_Binning[2]
    return Start_phi_h_bin, End___phi_h_bin


def Build_Multi5D_Slice_Metadata(args):
    phi_h_Binning = [0, 360, 24, 15]
    entries = []
    for Q2_y in args.Q2_y_Bin_List:
        if(Q2_y not in ["0", "All"]):
            # Never break out of the Q2-y loop when z-pT=1 is missing: some Q2-y bins (4, 8, 12, ...) intentionally have no z-pT=1 entry under skip_condition_z_pT_bins / dense-5D packing.
            z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
            for z_pT in range(0, z_pT_Range+1):
                Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y) if(str(Q2_y) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                phi_range = _Resolve_Phi_h_Slice_Range(Q2_y, z_pT, phi_h_Binning)
                if(phi_range is None):
                    continue
                Start_phi_h_bin, End___phi_h_bin = phi_range
                entries.append({"Q2_y": Q2_y,
                                "z_pT": z_pT,
                                "Start_phi_h_bin": Start_phi_h_bin,
                                "End_phi_h_bin": End___phi_h_bin,
                                "Bin_Title": Bin_Title,
                               })
    return {"phi_h_Binning": phi_h_Binning, "entries": entries}


def _Stream_Write_Slice_Hist(hist, Method, output_file, stream_write, save_count_ref, test_mode, args):
    if(not stream_write):
        return False
    hist.GetYaxis().SetTitle("")
    # Do not append _(Iteration_#) to Bayesian sliced 1D names (kept for reference if re-enabled later)
    # if(Method in ["Bayesian", "bayes", "bayesian"]):
    #     hist.SetName(f"{hist.GetName()}_(Iteration_{args.bayes_iterations})")
    if(not test_mode and output_file is not None):
        safe_write(hist, output_file)
    if(save_count_ref is not None):
        save_count_ref[0] += 1
        if(args.verbose):
            prefix = f"{color.BGREEN}Saved Histo {save_count_ref[0]:>4.0f})" if(not test_mode) else f"{color.PINK}Would have saved Histo {save_count_ref[0]:>4.0f})"
            print(f"{prefix}\n\t{color.BBLUE}{hist.GetName()}{color.END}")
    hist.SetDirectory(0)
    # ROOT.Delete(hist)
    return True


def Multi5D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="", Out_Option="Save", Fitting_Input="default", args="args", slice_metadata=None, output_file=None, stream_write=False, save_count_ref=None, test_mode=False):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    print(f"\n{color.BLUE}Running Multi5D_Slice(...){color.END}\n")
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName = {color.END}{Name}\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_Q2_y_z_pT_phi_h"]):
            print(f"{color.RED}ERROR in Multi5D_Slice(): Not set up for other variables (yet)\n{color.END}Variable = {Variable}\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = f"{Variable}_smeared"
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue),  "]{(Experimental)}"       if(not args.sim)      else "]{(MC REC - Pre-Unfolded)}"])
            if(not args.sim):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{5-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_5D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if(False):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((args.pass_version not in [""]) and (args.pass_version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(args.pass_version), "}}"])
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        if(slice_metadata is not None):
            phi_h_Binning = slice_metadata["phi_h_Binning"]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ################################################################################
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable=str(Variable).replace("_smeared", ""), args=args)
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END, "\nName =", str(Name), "\n"]))
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END, "\nName =", str(Name), "\n"]))

        def Process_One_Slice_Entry(Q2_y, z_pT, Start_phi_h_bin, End___phi_h_bin, Bin_Title):
            # Per-slice title: method line on top, entry Bin_Title (Q2-y / z-pT) on the bottom
            Title_Out = f"#splitline{{{root_color.Bold}{{5D #phi_{{h}}{Method_Title} Plot}}}}{{{Bin_Title}}}"
            if((args.pass_version not in [""]) and (args.pass_version not in str(Title_Out))):
                Title_Out = f"#splitline{{{Title_Out}}}{{{root_color.Bold}{{{args.pass_version}}}}}"
            Name_Out = str(Name.replace("MultiDim_5D_Q2_y_Bin_Info",     str(Q2_y) if(str(Q2_y) not in ["0", "All"]) else "All"))
            Name_Out = str(Name_Out.replace("MultiDim_5D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
            Slice_Hist = ROOT.TH1D(Name_Out, f"{Title_Out}; #phi_{{h}} [{root_color.Degrees}]", phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
            ii_bin_num,  ii_LastNum  = Start_phi_h_bin, Start_phi_h_bin
            phi_Content, phi___Error = {}, {}
            for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
            while(ii_bin_num < End___phi_h_bin):
                OverFlow_Con = False
                if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
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
                                phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0
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
                Slice_Hist.Fill(                                       phi_bin + 0.5*phi_h_Binning[3],            phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                Slice_Hist.SetBinError(Slice_Hist.FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
            Slice_Hist.GetYaxis().SetRangeUser(1.5*Slice_Hist.GetBinContent(Slice_Hist.GetMinimumBin()) if(Slice_Hist.GetBinContent(Slice_Hist.GetMinimumBin()) < 0) else 0, 1.5*Slice_Hist.GetBinContent(Slice_Hist.GetMaximumBin()))
            if(Method in ["rdf", "Experimental"]):
                Slice_Hist.SetLineColor(root_color.Blue)
                Slice_Hist.SetMarkerColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Slice_Hist.SetLineColor(root_color.Red)
                Slice_Hist.SetMarkerColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Slice_Hist.SetLineColor(root_color.Green)
                Slice_Hist.SetMarkerColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Slice_Hist.SetLineColor(root_color.Cyan)
                Slice_Hist.SetMarkerColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Slice_Hist.SetLineColor(root_color.Brown)
                Slice_Hist.SetMarkerColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian"]):
                Slice_Hist.SetLineColor(root_color.Teal)
                Slice_Hist.SetMarkerColor(root_color.Teal)
            if(Method in ["Background"]):
                Slice_Hist.SetLineColor(root_color.Black)
                Slice_Hist.SetMarkerColor(root_color.Black)
            if(Fitting_Input in ["default", "Default"] and False):
                Slice_Hist, Unfolded_Fit_Function[Name_Out.replace("MultiDim_5D_Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("MultiDim_5D_Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Slice_Hist, Method=Method, Fitting="default", Special=[int(Q2_y), int(z_pT)])
            if(_Stream_Write_Slice_Hist(Slice_Hist, Method, output_file, stream_write, save_count_ref, test_mode, args)):
                return
            Output_Histos[Name_Out] = Slice_Hist

        if(slice_metadata is not None):
            for entry in slice_metadata["entries"]:
                Process_One_Slice_Entry(entry["Q2_y"], entry["z_pT"], entry["Start_phi_h_bin"], entry["End_phi_h_bin"], entry["Bin_Title"])
        else:
            # slice_metadata=None fallback: same Q2-y / z-pT iteration as Build_Multi5D_Slice_Metadata (no early break on missing z-pT=1)
            for Q2_y in args.Q2_y_Bin_List:
                if(Q2_y not in ["0", "All"]):
                    z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
                    for z_pT in range(0, z_pT_Range+1):
                        Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y) if(str(Q2_y) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                        phi_range = _Resolve_Phi_h_Slice_Range(Q2_y, z_pT, phi_h_Binning)
                        if(phi_range is None):
                            continue
                        Start_phi_h_bin, End___phi_h_bin = phi_range
                        Process_One_Slice_Entry(Q2_y, z_pT, Start_phi_h_bin, End___phi_h_bin, Bin_Title)
        ################################################################################
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(stream_write):
            return 0
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
        print(f"{color.Error}Multi5D_Slice(...) ERROR:{color.END}\n{traceback.format_exc()}\n")
        return "Error"


def main_start():
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    for attr in ['root', 'single_file_input', 'pdf_name']:
        if(hasattr(args, attr) and getattr(args, attr)):
            original = getattr(args, attr)
            cleaned = str(original.replace('"', "")).replace("'", "")
            if(cleaned != original):
                print(f"{color.BYELLOW}Cleaned quotes from --{attr}: '{original}' -> '{cleaned}'{color.END}")
                setattr(args, attr, cleaned)
    args.pass_version = "Pass 2"
    args.closure = False
    args.sim = args.sim or False
    args.mod = args.mod and (not args.closure)
    args.smearing_options = "no_smear" if(args.no_smear) else "smear"
    args.standard_histogram_title_addition = ""
    if(args.sim):
        print(f"\n{color.BLUE}Running Simulated Test\n{color.END}")
        args.standard_histogram_title_addition = "Closure Test - Unfolding Simulation"
    if(args.mod):
        print(f"\n{color.BLUE}Using {color.BOLD}Modulated {color.END_b} Monte Carlo Files\n{color.END}")
        if(args.standard_histogram_title_addition not in [""]):
            args.standard_histogram_title_addition = f"{args.standard_histogram_title_addition} - Using Modulated Response Matrix"
        else:
            args.standard_histogram_title_addition = "Closure Test - Using Modulated Response Matrix"
    args.Q2_y_Bin_List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    if(args.bins):
        args.Q2_y_Bin_List = args.bins
    if('0' not in args.Q2_y_Bin_List):
        args.Q2_y_Bin_List.append('0')
    if(args.matrix_pdf):
        print(f"\n{color.BOLD}Starting Dedicated 5D Response Matrix PDF Mode\n{color.END}")
        if(not args.test):
            print(f"\n{color.BBLUE}Will be saving matrix PDF to {color.END_B}{args.pdf_name}{color.END}\n")
        else:
            print(f"\n{color.RED}Will {color.Error}NOT{color.END_R} be saving results (running as a test)\n{color.END_b}Would have saved to {color.END_B}{args.pdf_name}{color.END}\n")
    elif(args.recover_slices):
        print(f"\n{color.BOLD}Starting Dedicated 5D Bayesian Slice Recovery Mode\n{color.END}")
        if(not args.test):
            print(f"\n{color.BBLUE}Will recover Bayesian slices into {color.END_B}{args.root}{color.END}\n")
        else:
            print(f"\n{color.RED}Will {color.Error}NOT{color.END_R} be saving results (running as a test)\n{color.END_b}Would have recovered Bayesian slices into {color.END_B}{args.root}{color.END}\n")
    else:
        if(not args.test):
            print(f"\n{color.BBLUE}Will be saving results to {color.END_B}{args.root}{color.END}\n")
        else:
            print(f"\n{color.RED}Will {color.Error}NOT{color.END_R} be saving results (running as a test)\n{color.END_b}Would have saved to {color.END_B}{args.root}{color.END}\n")
        print(f"\n{color.BOLD}Starting Dedicated 5D Unfolding Analysis\n{color.END}")
        silence_root_import()
    print(f"\n{color.BBLUE}Smear option selected is: {'No Smear' if(str(args.smearing_options) in ['', 'no_smear']) else str(args.smearing_options.replace('_s', 'S')).replace('s', 'S')}{color.END}\n")
    return args


def Load_And_Rebuild_5D_Response_Matrix(input_file, args):
    detected = Detect_5D_Matrix_Config(input_file, args)
    if(detected is None):
        Crash_Report(args, crash_message="Could not find a 5D response matrix slice-1 entry in the input file.")
    out_print_main_mdf_base = detected["out_print_main_mdf_base"]
    out_print_main_mdf_1D = detected["out_print_main_mdf_1D"]
    if(out_print_main_mdf_1D not in input_file.GetListOfKeys()):
        Crash_Report(args, crash_message=f"Missing mdf 1D histogram: {out_print_main_mdf_1D}")
    MC_REC_1D = input_file.Get(out_print_main_mdf_1D)
    Validate_And_Record_5D_Dimensions(args, detected, MC_REC_1D)
    print(f"\n{color.BGREEN}(5D) Rebuilding Response Matrix: {detected['out_print_main']}{color.END}\n")
    Response_2D = Rebuild_Matrix_5D(List_of_Sliced_Histos=detected["Histo_List"], Standard_Name=out_print_main_mdf_base, Increment=args.increment_5d)
    if(Response_2D in ["ERROR"]):
        Crash_Report(args, crash_message="Rebuild_Matrix_5D returned ERROR")
    return Response_2D, detected


def Save_Rebuilt_Matrix_As_Pdf(Response_2D, pdf_path, args):
    if(args.test):
        print(f"{color.PINK}Would be saving matrix PDF to: {color.BCYAN}{pdf_path}{color.END}")
        Response_2D.SetDirectory(0)
        # ROOT.Delete(Response_2D)
        return 0
    print(f"{color.BBLUE}Saving matrix PDF to: {color.BGREEN}{pdf_path}{color.END}")
    canvas = ROOT.TCanvas("Rebuilt_5D_Response_Matrix", "Rebuilt 5D Response Matrix", 1300, 725)
    canvas.SetRightMargin(0.15)
    canvas.SetLeftMargin(0.15)
    canvas.SetBottomMargin(0.15)
    canvas.SetTopMargin(0.175)
    ROOT.gStyle.SetOptStat('i')
    ROOT.gStyle.SetStatX(0.900)
    ROOT.gStyle.SetStatY(0.875)
    ROOT.gStyle.SetStatW(0.150)
    ROOT.gStyle.SetStatH(0.200)
    Response_2D.SetDirectory(0)
    Response_2D.SetTitle("5D Response Matrix of Q^{2}-y-z-P_{T}-#phi_{h} Bins")
    Response_2D.GetXaxis().SetTitle("Q^{2}-y-z-P_{T}-#phi_{h} - REC Bins")
    Response_2D.GetYaxis().SetTitle("Q^{2}-y-z-P_{T}-#phi_{h} - GEN Bins")
    Response_2D.Draw("colz")
    if(args.logz):
        canvas.SetLogz(True)
    canvas.Update()
    canvas.SaveAs(pdf_path)
    if(args.verbose):
        print(f"{color.BGREEN}Saved matrix PDF:\n\t{color.BBLUE}{pdf_path}{color.END}")
    # ROOT.Delete(canvas)
    # ROOT.Delete(Response_2D)
    return 1


def main_5D_matrix_pdf(args):
    input_file = ROOT.TFile.Open(args.single_file_input, "READ")
    if(not input_file or input_file.IsZombie()):
        Crash_Report(args, crash_message=f"Could not open input ROOT file: {args.single_file_input}")
    print(f"The total number of histograms in '{color.BBLUE}{args.single_file_input}{color.END}' is {color.BOLD}{len(input_file.GetListOfKeys())}{color.END}")
    Response_2D, detected = Load_And_Rebuild_5D_Response_Matrix(input_file, args)
    args.timer.time_elapsed()
    saved_count = Save_Rebuilt_Matrix_As_Pdf(Response_2D, args.pdf_name, args)
    detected["Histo_List"] = {}
    input_file.Close()
    return saved_count


def _Smear_For_Histo(histo):
    return "Smear" if(any(smear_find in histo.GetName() for smear_find in ["'smear'", "'Smear'", "smeared", "SMEAR=Smear"])) else ""


def _Run_Slice_Category(Pre_Sliced_1Ds, method, args, output_file, save_count_ref, MC_BGS_1D):
    if(method == "Background" and MC_BGS_1D in ["None"]):
        return
    result = Multi5D_Slice(Histo=Pre_Sliced_1Ds, Title=Pre_Sliced_1Ds.GetTitle(), Name=Pre_Sliced_1Ds.GetName(), Method=method, Variable="MultiDim_Q2_y_z_pT_phi_h", Smear=_Smear_For_Histo(Pre_Sliced_1Ds), Out_Option="histo", Fitting_Input="off", args=args, slice_metadata=args.multi5d_slice_metadata, output_file=output_file, stream_write=True, save_count_ref=save_count_ref, test_mode=args.test)
    if(type(result) is str):
        print(f"{color.Error}ERROR: Sliced_1Ds = {result}{color.END}")


def main_5D_unfold(args):
    input_file = ROOT.TFile.Open(args.single_file_input, "READ")
    if(not input_file or input_file.IsZombie()):
        Crash_Report(args, crash_message=f"Could not open input ROOT file: {args.single_file_input}")
    print(f"The total number of histograms in '{color.BBLUE}{args.single_file_input}{color.END}' is {color.BOLD}{len(input_file.GetListOfKeys())}{color.END}")
    args.multi5d_slice_metadata = Build_Multi5D_Slice_Metadata(args)
    detected = Detect_5D_Matrix_Config(input_file, args)
    if(detected is None):
        Crash_Report(args, crash_message="Could not find a 5D response matrix slice-1 entry in the input file.")
    out_print_main_mdf = detected["out_print_main_mdf"]
    out_print_main_mdf_base = detected["out_print_main_mdf_base"]
    out_print_main_mdf_1D = detected["out_print_main_mdf_1D"]
    Histo_List = detected["Histo_List"]
    out_print_main_rdf = out_print_main_mdf_base.replace("(Data-Type='mdf')", "(Data-Type='rdf')")
    out_print_main_gdf = out_print_main_mdf_base.replace("(Data-Type='mdf')", "(Data-Type='gdf')")
    out_print_main_rdf = out_print_main_rdf.replace("_(Weighed)", "")
    out_print_main_gdf = out_print_main_gdf.replace("_(Weighed)", "")
    out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_EDIS", "no_cut")
    for sector_cut_remove in range(1, 7):
        out_print_main_gdf = out_print_main_gdf.replace(f"cut_Complete_SIDIS_eS{sector_cut_remove}o", "no_cut")
    out_print_main_gdf = out_print_main_gdf.replace("cut_Complete_SIDIS", "no_cut")
    out_print_main_gdf = out_print_main_gdf.replace("cut_Complete", "no_cut")
    if(not args.sim):
        out_print_main_rdf = out_print_main_rdf.replace("smear", "")
    out_print_main_gdf = out_print_main_gdf.replace("smear", "")
    out_print_main_rdf = Apply_Matrix_1D_Replacements(out_print_main_rdf)
    out_print_main_gdf = Apply_Matrix_1D_Replacements(out_print_main_gdf)
    if(out_print_main_mdf_1D not in input_file.GetListOfKeys()):
        Crash_Report(args, crash_message=f"Missing mdf 1D histogram: {out_print_main_mdf_1D}")
    MC_REC_1D = input_file.Get(out_print_main_mdf_1D)
    Validate_And_Record_5D_Dimensions(args, detected, MC_REC_1D)
    if(args.sim):
        out_print_main_rdf = out_print_main_mdf_1D
    if(out_print_main_rdf not in input_file.GetListOfKeys()):
        Crash_Report(args, crash_message=f"Missing rdf 1D histogram: {out_print_main_rdf}")
    if(out_print_main_gdf not in input_file.GetListOfKeys()):
        Crash_Report(args, crash_message=f"Missing gdf 1D histogram: {out_print_main_gdf}")
    print(f"\n{color.BGREEN}(5D) Unfolding: {detected['out_print_main']}{color.END}\n")
    ExREAL_1D = input_file.Get(out_print_main_rdf)
    MC_GEN_1D = input_file.Get(out_print_main_gdf)
    out_print_main_bdf_1D = Apply_Background_1D_Replacements(out_print_main_mdf_1D)
    if((out_print_main_bdf_1D in input_file.GetListOfKeys()) and ("Background" in str(out_print_main_bdf_1D))):
        MC_BGS_1D = input_file.Get(out_print_main_bdf_1D)
        MC_BGS_1D.SetTitle("".join(["#splitline{BACKGROUND}{", str(MC_REC_1D.GetTitle()), "};", str(MC_REC_1D.GetXaxis().GetTitle()), ";", str(MC_REC_1D.GetYaxis().GetTitle())]))
    else:
        MC_BGS_1D = "None"
        print(f"{color.Error}\nERROR: Missing Background Histogram {color.END_R}(would be named: {color.END_B}{out_print_main_bdf_1D}{color.END_R}){color.END}")
        raise TypeError("Missing (5D) Background Histogram")
    if(args.sim and (str(MC_BGS_1D) not in ["None"])):
        ExREAL_1D.Add(MC_BGS_1D)
    ExREAL_1D_wExclusive_Background = None
    out_print_main_rdf_1D_bgs = out_print_main_rdf
    if(f"{out_print_main_rdf_1D_bgs}_({args.background_source})" in input_file.GetListOfKeys()):
        print(f"{color.BGREEN}Subtracting the '{args.background_source}' files to the 'ExREAL_1D' histogram{color.END}")
        LundrhoHist_rdf = input_file.Get(f"{out_print_main_rdf_1D_bgs}_({args.background_source})")
        ExREAL_1D_wExclusive_Background, ExREAL_1D = subtract_bkg_with_zero_floor(ExREAL_1D, LundrhoHist_rdf)
    elif(f"{out_print_main_mdf_1D}_({args.background_source})" in input_file.GetListOfKeys()):
        print(f"{color.BGREEN}Subtracting the '{args.background_source}' files to the 'ExREAL_1D' histogram{color.END}")
        LundrhoHist_rdf = input_file.Get(f"{out_print_main_mdf_1D}_({args.background_source})")
        ExREAL_1D_wExclusive_Background, ExREAL_1D = subtract_bkg_with_zero_floor(ExREAL_1D, LundrhoHist_rdf)
    elif(args.background_source not in ["None"]):
        print(f"{color.Error}Cannot subtract the '{args.background_source}' files to the 'ExREAL_1D' histogram{color.END}")
    Response_2D = Rebuild_Matrix_5D(List_of_Sliced_Histos=Histo_List, Standard_Name=out_print_main_mdf_base, Increment=args.increment_5d)
    if(Response_2D in ["ERROR"]):
        Crash_Report(args, crash_message="Rebuild_Matrix_5D returned ERROR")
    args.timer.time_elapsed()
    Unfold_Result = Unfold_Function(Response_2D=Response_2D, ExREAL_1D=ExREAL_1D, MC_REC_1D=MC_REC_1D, MC_GEN_1D=MC_GEN_1D, Method="RooUnfold", MC_BGS_1D=MC_BGS_1D, args=args)
    if(Unfold_Result in ["ERROR"]):
        Crash_Report(args, crash_message="Unfold_Function returned ERROR")
    Unfold_1D, Response_RooUnfold = Unfold_Result
    Unfold_1D.SetDirectory(0)
    # 5D unfolding uses the rebuilt matrix in-place inside RooUnfold; caller must release it after Hunfold()
    del Response_RooUnfold
    # ROOT.Delete(Response_2D)
    del Response_2D
    Histo_List.clear()
    detected["Histo_List"] = {}
    print(f"\n{color.BGREEN}Finished Unfolding{color.END}\n")
    args.timer.time_elapsed()
    Histos_To_Slice = [[ExREAL_1D, "rdf"], [MC_REC_1D, "mdf"], [MC_GEN_1D, "gdf"]]
    if(MC_BGS_1D not in ["None"]):
        Histos_To_Slice.append([MC_BGS_1D, "Background"])
    Histos_To_Slice.append([Unfold_1D, "Bayesian"])
    to_be_saved_count = 0
    if(not args.test):
        print(f"{color.BBLUE}Saving to: {color.BGREEN}{args.root}{color.END}")
        output_file = ROOT.TFile(args.root, "UPDATE")
        File_Name_Tlist = ROOT.TList()
        File_Name_Tlist.SetName("Latest_List_of_File_Names")
        File_Name_Tlist.Add(ROOT.TObjString(str(args.single_file_input)))
        safe_write(File_Name_Tlist, output_file)
        Config_Tlist = ROOT.TList()
        Config_Tlist.SetName("Detected_5D_Config")
        Config_Tlist.Add(ROOT.TObjString(f"increment={args.increment_5d}"))
        Config_Tlist.Add(ROOT.TObjString(f"num_bins={args.num_bins_5d}"))
        Config_Tlist.Add(ROOT.TObjString(f"num_slices={args.num_slices_5d}"))
        safe_write(Config_Tlist, output_file)
        if(ExREAL_1D_wExclusive_Background is not None):
            ExREAL_1D_wExclusive_Background.SetDirectory(0)
            safe_write(ExREAL_1D_wExclusive_Background, output_file)
            to_be_saved_count += 1
        try:
            safe_write(Unfold_1D, output_file)
            to_be_saved_count += 1
        except:
            print(f"\n{color.Error}ERROR: Tried to save Unfold_1D\n{color.END}{traceback.format_exc()}\n")
        save_count_ref = [to_be_saved_count]
        for Pre_Sliced_1Ds, method in Histos_To_Slice:
            _Run_Slice_Category(Pre_Sliced_1Ds, method, args, output_file, save_count_ref, MC_BGS_1D)
        to_be_saved_count = save_count_ref[0]
        print(f"\n{color.BBLUE}Done Saving...{color.END}\n")
        output_file.Close()
    else:
        print(f"{color.PINK}Would be saving to: {color.BCYAN}{args.root}{color.END}")
        save_count_ref = [to_be_saved_count]
        for Pre_Sliced_1Ds, method in Histos_To_Slice:
            _Run_Slice_Category(Pre_Sliced_1Ds, method, args, None, save_count_ref, MC_BGS_1D)
        to_be_saved_count = save_count_ref[0]
    input_file.Close()
    return to_be_saved_count

def main_5D_recover_slices(args):
    # Skip matrix rebuild / background / unfolding. Load the existing output ROOT file and only Multi5D_Slice the Bayesian 1D histogram.
    args.multi5d_slice_metadata = Build_Multi5D_Slice_Metadata(args)
    proper_name = f"""(MultiDim_5D_Histo)_(Bayesian)_(SMEAR={"Smear" if(str(args.smearing_options) not in ["", "no_smear"]) else "''"})_(Q2_y_z_pT_Bin_All)_(MultiDim_Q2_y_z_pT_phi_h)"""
    to_be_saved_count = 0
    output_file = None
    if(not args.test):
        print(f"{color.BBLUE}Recovering Bayesian slices into: {color.BGREEN}{args.root}{color.END}")
        output_file = ROOT.TFile(args.root, "UPDATE")
        if(not output_file or output_file.IsZombie()):
            Crash_Report(args, crash_message=f"Could not open output ROOT file for recovery: {args.root}")
    else:
        print(f"{color.PINK}Would be recovering Bayesian slices into: {color.BCYAN}{args.root}{color.END}")
        output_file = ROOT.TFile.Open(args.root, "READ")
        if(not output_file or output_file.IsZombie()):
            Crash_Report(args, crash_message=f"Could not open output ROOT file for recovery (test mode): {args.root}")
    print(f"The total number of histograms in '{color.BBLUE}{args.root}{color.END}' is {color.BOLD}{len(output_file.GetListOfKeys())}{color.END}")
    Unfold_1D = None
    if(proper_name in output_file.GetListOfKeys()):
        print(f"{color.BGREEN}Found properly named Bayesian 1D histogram:\n\t{color.BBLUE}{proper_name}{color.END}")
        Unfold_1D = output_file.Get(proper_name)
    elif("unfolded" in output_file.GetListOfKeys()):
        print(f"{color.BYELLOW}Found raw 'unfolded' histogram; renaming to proper MultiDim Bayesian name...{color.END}")
        Unfold_1D = output_file.Get("unfolded")
        Unfold_1D.SetName(proper_name)
        if(not args.test):
            try:
                safe_write(Unfold_1D, output_file)
                to_be_saved_count += 1
                print(f"{color.BGREEN}Resaved renamed Bayesian 1D histogram as:\n\t{color.BBLUE}{proper_name}{color.END}")
            except:
                print(f"\n{color.Error}ERROR: Tried to save renamed Unfold_1D\n{color.END}{traceback.format_exc()}\n")
        else:
            print(f"{color.PINK}Would have resaved renamed Bayesian 1D histogram as:\n\t{color.BCYAN}{proper_name}{color.END}")
            to_be_saved_count += 1
    else:
        output_file.Close()
        Crash_Report(args, crash_message=f"Recovery mode could not find '{proper_name}' or 'unfolded' in {args.root}")
    Unfold_1D.SetDirectory(0)
    args.timer.time_elapsed()
    save_count_ref = [to_be_saved_count]
    if(not args.test):
        _Run_Slice_Category(Unfold_1D, "Bayesian", args, output_file, save_count_ref, "None")
        to_be_saved_count = save_count_ref[0]
        print(f"\n{color.BBLUE}Done Saving Bayesian slices...{color.END}\n")
        output_file.Close()
    else:
        _Run_Slice_Category(Unfold_1D, "Bayesian", args, None, save_count_ref, "None")
        to_be_saved_count = save_count_ref[0]
        output_file.Close()
    return to_be_saved_count

def main():
    args = main_start()
    to_be_saved_count = 0
    try:
        if(args.recover_slices):
            to_be_saved_count = main_5D_recover_slices(args)
        elif(args.matrix_pdf):
            to_be_saved_count = main_5D_matrix_pdf(args)
        else:
            to_be_saved_count = main_5D_unfold(args)
    except:
        mode_label = "Bayesian Slice Recovery" if(args.recover_slices) else "Matrix PDF" if(args.matrix_pdf) else "5D Unfolding"
        Crash_Report(args, crash_message=f"The {mode_label} Code has CRASHED!\nERROR MESSAGE:\n\n{traceback.format_exc()}")
    Construct_Email(args, final_count=to_be_saved_count)

if(__name__ == "__main__"):
    main()

