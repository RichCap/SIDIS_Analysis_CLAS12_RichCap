#!/usr/bin/env python3
import sys
from sys import argv
import argparse

from MyCommonAnalysisFunction_richcap import color, color_bg, root_color


def parse_args():
    print("")
    parser = argparse.ArgumentParser(
        description="""
This script processes SIDIS TTree data for ROOT files.
    Options for Positional Arguement 1 (datatype):
        Primary Options (must always include): 
            1) rdf --> Real Data
            2) mdf --> MC REC Data (Event matching is available)
            3) gdf --> MC GEN Data
            4) pdf --> Only Matched MC Events (REC events must be matched to their GEN counterparts if this option is selected)
        Secondary options (add to data-type): 
            * Refer to the following lists to control how the code is run (details in the script)
            * Lists include:
                1) 'SIDIS_Unfold_List' options will ensure the histograms used with unfolding are run
                2) 'Momentum_Cor_List' options will ensure the options for (exclusive) momentum corrections/smearing are run
                3) 'Using_Weight_List' options will run a variety of MC closure tests (including weighing histogram events)
                4) 'Smear_Factor_List' options control which smear factor/function is used when smearing the MC
                    (*) Use when testing different options - default option is set within the code if not included in this argument
                5) 'Pass_Version_List' options control which pass version of the data/MC is used when running the code
                    (*) Currently defaults to Pass 2
                6) 'Use__Mom_Cor_List' options control whether or not momentum corrections are applied
                7) 'Smear_Option_List' options control whether or not momentum smearing is applied
                8) 'Tag___Proton_List' options control whether the tagged proton files (and related plots/cuts) are used
                9) 'SkipFiducial_List' options control which fiducial cut(s) are or are not included in the cuts
            * Also can use the option "Small" to use a secondary set of options set by 'Run_Small' (see script for details)
    Options for Positional Arguement 2 (output_type):
        Output options:
            1) time            --> Runs the code as a test without saving output.
            2) test            --> Prints content names of the output files.
            3) [file location] --> Runs normally, produces an output file.
            4) All             --> Runs all files in the directory based on selected options.
            
    EXAMPLE(S): 
        ./TTree_create_ROOT_epip_SIDIS.py <df>_NewP2 time (Old - 'NewP2' is now the default and is therefore unnecessary)
        ./TTree_create_ROOT_epip_SIDIS.py <df> time
    Note: <df> above can be any of the data-type options given above
        """,
        formatter_class=argparse.RawTextHelpFormatter  # Preserves your formatting
    )
    
    parser.add_argument("datatype",    type=str, help="Data type and options to run")
    parser.add_argument("output_type", type=str, help="Output type/file number (full file location)")
    
    return parser.parse_args()

if((len(argv) < 3) and all(help_options not in argv for help_options in ["--help", "-h"])):
    # If arguments are passed using sys.argv instead of argparse, this fallback ensures compatibility
    print(f"\n{color.Error}Error in arguments. Use '--help' for more information.\n{color.END}")
    sys.exit()
    
args = parse_args()

# Convert the arguments to the existing format
datatype    = str(args.datatype)
output_type = str(args.output_type)

SIDIS_Unfold_List = ["_SIDIS",  "_sidis", "_unfold",   "_Unfold"]
Momentum_Cor_List = ["_Mom",    "_mom"]
Use__Mom_Cor_List = ["_UnCor",  "_Uncor", "mdf",       "gdf"]
Using_Weight_List = ["_mod",    "_close", "_closure",  "_weighed", "_use_weight", "_Q4"]
Smear_Option_List = ["_NSmear", "_NS",    "_no_smear", "rdf",      "gdf"]
Smear_Factor_List = ["_0.5",    "_0.75",  "_0.7",      "_0.8",     "_0.9",        "_1.0",   "_1.2",      "_1.5", "_1.75", "_2.0", "_FX"]
Pass_Version_List = ["_P2",     "_Pass2", "_P1",       "_Pass1",   "_NewP2", "_NewPass2", "_NewP1", "_NewPass1"]
Tag___Proton_List = ["_Pro",    "_Proton"]
SkipFiducial_List = ["_FC0",    "_FC1",   "_FC2",      "_FC3",     "_FC4",        "_FC5",   "_FC6",      "_FC7",  "_FC8", "_FC9", "_FC_10", "_FC_11", "_FC_12", "_FC_13", "_FC_14"]

output_all_histo_names_Q = "yes"
# output_all_histo_names_Q = "no"

# run_Mom_Cor_Code = "yes"
run_Mom_Cor_Code = "no"

smear_factor = "0.75"


Use_Pass_2, Use_New_PF = True, True


# Run Reconstructed MC with Smearing Function (Run_With_Smear is automatically set to False if the datatype inputs include "rdf" or "gdf")
Run_With_Smear = True


# Use_Weight corresponses to weighing the MC events to add modulations to the generated simulated data (used as a closure test)
Use_Weight = False
# Use_Weight = True

# Option to turn on and off Momentum Corrections ('yes' will turn the corrections on)
Mom_Correction_Q = "yes"
# Mom_Correction_Q = "no"

# Option to use the tagged proton files (as of 7/29/2024, only available for the "_NewPass2" version of the files)
# # Let 'Tag_Proton = False' for running without tagged protons, while 'Tag_Proton = True' will use the files/options with the proton being tagged
Tag_Proton = False


for sidis         in SIDIS_Unfold_List:
    if(str(sidis) in str(datatype)):
        run_Mom_Cor_Code = "no"
        datatype         = str(datatype).replace(str(sidis), "")
        break
        
for mom_cor         in Momentum_Cor_List:
    if(str(mom_cor) in str(datatype)):
        run_Mom_Cor_Code = "yes"
        datatype         = str(datatype).replace(str(mom_cor), "")
        break
        
for use_cor         in Use__Mom_Cor_List:
    if(str(use_cor) in str(datatype)):
        Mom_Correction_Q = "no"
        # Default option is to use the momentum corrections whenever possible (unless some other option is automatically selected below due to availability or applicability of the correction)
            # Only applies to experimental data (as of 3-29-2024)
        if("_" in str(use_cor)):
            datatype     = str(datatype).replace(str(use_cor), "")
        break


for smearQ         in Smear_Option_List:
    if(str(smearQ) in str(datatype)):
        if("_" in str(smearQ)):
            datatype     = str(datatype).replace(str(smearQ), "")
        if(run_Mom_Cor_Code == "no"):
            Run_With_Smear   = False
            if("mdf" in str(datatype)):
                print(f"{color.Error}\nNot Smearing\n{color.END}")
        else:
            if("mdf" in str(datatype)):
                print(f"{color.Error}\nIgnoring Option to not smear...\n{color.END}")
        break
    
for smear         in Smear_Factor_List:
    if(str(smear) in str(datatype)):
        smear_factor     = str(smear).replace("_", "")
        datatype         = str(datatype).replace(str(smear), "")
        break
        
for weight_Q         in Using_Weight_List:
    if(str(weight_Q) in str(datatype)):
        Use_Weight       = True
        if("_Q4"     in str(datatype)):
            Q4_Weight    = True
        else:
            Q4_Weight    = False
        datatype         = str(datatype).replace(str(weight_Q), "")
        break
        
for tagging_proton         in Tag___Proton_List:
    if(str(tagging_proton) in str(datatype)):
        Tag_Proton = True
        datatype   = str(datatype).replace(str(tagging_proton), "")
        break
        
        
if((run_Mom_Cor_Code in ["yes"]) or ("rdf" in str(datatype))):
    Use_Weight = False
    Q4_Weight  = False
    # Do not use the simulated modulations on the momentum correction code or for the experimental data set
    
    
for pass_ver in Pass_Version_List:
    if(str(pass_ver) in str(datatype)):
        if((not Use_Pass_2) and (not Use_New_PF)):
            Use_Pass_2 = ("2"   in str(pass_ver))
            Use_New_PF = ("New" in str(pass_ver))
            datatype   = str(datatype).replace(str(pass_ver), "")
        break
        
        
# Setting the skip cut configuration for the New_Fiducial_Cuts_Function() function
# Skipped_Fiducial_Cuts = ["N/A"]
Default_Cut_Option     = ["Hpip", "Electron"]
Skipped_Fiducial_Cuts  = ["My_Cuts"] # My fiducial cuts are not being used
Skipped_Fiducial_Cuts  = Default_Cut_Option
Cut_Configuration_Name = ""
for SkipC         in SkipFiducial_List:
    if(str(SkipC) in str(datatype)):
        Cut_Configuration_Name    = SkipC
        if(SkipC  in ["_FC0"]):
            Skipped_Fiducial_Cuts = ["All",     "Hpip"]            # Skips All new fiducial cuts added after new Pass 2 files
        if(SkipC  in ["_FC1"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "Hpip"]            # Bad PCal Channels for the Pion (Hx_pip and Hy_pip Cuts)
        if(SkipC  in ["_FC2"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "DC_pip"]          # Valerii's DC Cuts (on the Pion)
        if(SkipC  in ["_FC3"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "DC_ele"]          # Valerii's DC Cuts (on the Electron)
        if(SkipC  in ["_FC4"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "PCal"]            # Valerii's PCal Volume Cuts
        if(SkipC  in ["_FC5"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "Hpip", "DC_pip"]  # Skipping New Pion Cuts (from Valerii)
        if(SkipC  in ["_FC6"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "PCal", "DC_ele"]  # Skipping Valerii's (New) Electron Cuts
        if(SkipC  in ["_FC7"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "DC"]              # Skipping all DC cuts
        if(SkipC  in ["_FC8"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "Hpip", "PCal"]    # Skipping all PCal cuts (Only new DC Cuts)
        if(SkipC  in ["_FC9"]):
            Skipped_Fiducial_Cuts = ["All"]                        # Skipping all cuts from within the New_Fiducial_Cuts_Function() function
        if(SkipC  in ["_FC_10"]):
            Skipped_Fiducial_Cuts = ["Hpip", "DC_pip"]             # Skipping Valerii's Pion Cuts but including all of my new fiducial cuts (also includes Valerii's Electron Cuts)
        if(SkipC  in ["_FC_11"]):
            Skipped_Fiducial_Cuts = ["My_Cuts", "Hpip", "DC_pip"]  # Skipping Pion Cuts and all of my DC Cuts (includes just Valerii's Electron Cuts - same as 'FC5')
        if(SkipC  in ["_FC_12"]):
            Skipped_Fiducial_Cuts = ["Hpip", "DC_pip", "Pion"]     # Skipping New Pion Cuts (includes all of Valerii's Electron Cuts and my electron DC refinements)
        if(SkipC  in ["_FC_13"]):
            Skipped_Fiducial_Cuts = ["Hpip", "DC", "Electron"]     # Skipping All Electron DC Fiducial cuts (including Valerii's cuts and my refinements, BUT including my pion DC cuts - Valerii's cuts are also never to be applied to the pion at the point that this option was added)
        if(SkipC  in ["_FC_14"]):
            Skipped_Fiducial_Cuts = ["Hpip", "DC_pip", "Electron"] # Skipping my electron fiducial cuts and not applying any of Valerii's cuts to the pion (Includes all of Valerii's electron cuts and my new pion cuts)
        if(SkipC  in ["_FC7"]):
            Skipped_Fiducial_Cuts = ["Hpip", "DC", "My_Cuts"]      # Skipping all DC cuts (as of 9/3/2024, 'FC7' no longer allows Valerii's PCAL cuts to be applied to the pion - i.e., skipping 'Hpip')
        datatype                  = str(datatype).replace(str(SkipC), "")
        # if("gdf" not in str(datatype)):
        #     print(f"\n\033[1m\033[94mRunning without the following Fiducial Cut Options: {Skipped_Fiducial_Cuts}\033[0m\n")
        break
        
if("gdf" not in str(datatype)):
    print(f"\n\033[1m\033[94mRunning without the following Fiducial Cut Options: {Skipped_Fiducial_Cuts}\033[0m\n")
        
if(Tag_Proton and not Use_New_PF):
    print(f"{color.Error}Cannot Run the Tagged Proton without the newest versions of the Pass 2 root files...\n{color.END}")
    Tag_Proton = False
        
Run_Small = False
if("_Small" in str(datatype)):
    Run_Small = True
    datatype  = datatype.replace("_Small", "")
    print(f"{color.Error}Running reduced histogram options...\n{color.END}")

del SIDIS_Unfold_List
del Momentum_Cor_List
del Use__Mom_Cor_List
del Using_Weight_List
del Smear_Option_List
del Smear_Factor_List
del Pass_Version_List
del sidis
del mom_cor
del use_cor
del smearQ
del smear
del weight_Q
del pass_ver


if(output_type == "test"):
    output_all_histo_names_Q = "yes"
    print("Will be printing the TTree Branches' IDs...")
    file_location   = "time"
    output_type     = "time"
elif("test" in str(datatype)):
    output_all_histo_names_Q = "yes"
    print("Will be printing the TTree Branches' IDs...")
    file_location   = output_type
    output_type     = "time"
    print(f"\t{color.BOLD}Still using the given file of {color.BLUE}{color.UNDERLINE}{file_location}{color.END}\n\n")
    datatype = str(datatype.replace("_test", "")).replace("test_", "")
elif(output_type   not in ["histo", "data", "tree"]):
    file_location   = output_type
    if(output_type not in ["test", "time"]):
        output_type = "tree"
    if(output_all_histo_names_Q == "yes"):
        print("Will be printing the TTree Branches' IDs...")

print(f"The Output type will be: {output_type}")
print(f"The Data type will be:   {datatype}")


if(datatype in ['gdf']):
    Mom_Correction_Q = "no"

# if(datatype not in ['rdf']):
#     Mom_Correction_Q = "no"

if(Use_Pass_2):
    print(f"\n{color.BBLUE}Running the code with Pass 2 Data\n{color.END}")
    if(("rdf" not in str(datatype)) and (Mom_Correction_Q not in ["no"])):
        print(f"\n{color.BOLD}No Pass 2 Momentum Corrections are available (yet) for the Monte Carlo Simulations...\n{color.END}")
        Mom_Correction_Q = "no"
        

if(Use_New_PF):
    print(f"\n{color.BGREEN}Running the code with the newer versions of the Data/MC files (Version updated as of 7/26/2024)\n{color.END}")
    
Beam_Energy = 10.6041 if((datatype in ['rdf']) or (not Use_Pass_2)) else 10.6

print(f"\n{color.BBLUE}Beam Energy in use is: {color.UNDERLINE}{Beam_Energy} GeV{color.END}\n")


import ROOT 
import math
import array
from datetime import datetime
import copy
import traceback
import os

from ExtraAnalysisCodeValues import *



if(str(file_location) == 'all'):
    print("\nRunning all files together...\n")
if(str(file_location) == 'time'):
    print("\nRunning Count. Not saving results...\n")
    

if(datatype in ['rdf', 'mdf', 'gdf', 'pdf']):
    file_num = str(file_location)
    if(datatype == "rdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00",                                  "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00",                                                                  "")).replace(".hipo.root", "")     
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_00",                                                           "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new.nSidis_00",                                         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new2.nSidis_00",                                        "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new4.nSidis_00",                                        "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new5.nSidis_00",                                        "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.wProton.new5.nSidis_00",                                "")).replace(".hipo.root", "")
    if(datatype in ["mdf", "pdf"]):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_",                     "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_",                                                     "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_",                            "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new.inb-clasdis_",          "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new2.inb-clasdis_",         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new4.inb-clasdis_",         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.inb-clasdis_",         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis_", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.inb-clasdis-",         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis-", "")).replace(".hipo.root", "")
    if(datatype == "gdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_",                                  "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_",                                                                  "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.inb-clasdis_",                                                         "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.inb-clasdis_",                                                    "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis_",                                            "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.inb-clasdis-",                                                    "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis-",                                            "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/claspyth_files/MC_Gen_sidis_epip_richcap.inb.qa.new5.inb-claspyth_",                                    "")).replace(".hipo.root", "")
    
    ########################################################################################################################################################################
    ##==================================================================##============================##==================================================================##
    ##===============##===============##===============##===============##     Loading Data Files     ##===============##===============##===============##===============##
    ##==================================================================##============================##==================================================================##
    ########################################################################################################################################################################
    
    if(".root" in file_num):
        print(f"{color.Error}\nUnique File Name has been given as: {color.UNDERLINE}{file_num}{color.END}\n")
        files_used_for_data_frame = file_num
        file_num = str(file_num.replace(".root", "")).replace("/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/Running_Pythia/ROOT_Files/From_Pythia_Text_Files/", "")
        file_num = str(file_num.replace("Other_Channels/", ""))
        rdf = ROOT.RDataFrame("h22", str(files_used_for_data_frame))
        rdf_entry_count = rdf.Count().GetValue()
        print(f"Number of entries in the RDataFrame: {rdf_entry_count}")
    else:
        if(datatype == 'rdf'):
            if(str(file_location) in ['all', 'All', 'time']):
                files_used_for_data_frame =  "Data_sidis_epip_richcap.inb.qa.skim4_00*"                               if(not Use_Pass_2) else "Data_sidis_epip_richcap.inb.qa.nSidis_00*"
                if(Use_New_PF):
                    files_used_for_data_frame = str(files_used_for_data_frame.replace("qa.skim4_00", "qa.new5.skim4_00")).replace("qa.nSidis_00", "qa.new5.nSidis_00")
                    if(Tag_Proton):
                        files_used_for_data_frame = str(files_used_for_data_frame).replace("qa.new", "qa.wProton.new")
                rdf = ROOT.RDataFrame("h22", "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data", "/"      if(not Use_Pass_2) else "/Pass2/", str(files_used_for_data_frame)                 if(not Use_New_PF) else f"More_Cut_Info/{files_used_for_data_frame}"]))
            else:
                rdf = ROOT.RDataFrame("h22", str(file_location))
                files_used_for_data_frame =  "".join(["Data_sidis_epip_richcap.inb.qa", "."                           if(not Use_New_PF) else ".new5.",  "skim4_00"                                     if(not Use_Pass_2) else "nSidis_00", str(file_num), "*"])
        if(datatype in ['mdf', 'pdf']):
            if(str(file_location) in ['all', 'All', 'time']):
                files_used_for_data_frame =  "MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*"                       if(not Use_Pass_2) else "MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_*"
                if(Use_New_PF):
                    files_used_for_data_frame = str(files_used_for_data_frame.replace("qa.45nA_job_", "qa.new5.45nA_job_")).replace("qa.inb-clasdis_", "qa.new5.inb-clasdis")
                    if(Tag_Proton):
                        files_used_for_data_frame = str(files_used_for_data_frame).replace("qa.new", "qa.wProton.new")
                rdf = ROOT.RDataFrame("h22", "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC", "/" if(not Use_Pass_2) else "/With_BeamCharge/Pass2/", str(files_used_for_data_frame) if(not Use_New_PF) else f"More_Cut_Info/{files_used_for_data_frame}"]))
            else:
                rdf = ROOT.RDataFrame("h22", str(file_location))
                files_used_for_data_frame =  "".join(["MC_Matching_sidis_epip_richcap.inb.qa", "."                    if(not Use_New_PF) else ".new5.",  "45nA_job_"                                     if(not Use_Pass_2) else "inb-clasdis_", str(file_num), "*"])
                
        if(datatype == 'gdf'):
            if(str(file_location) in ['all', 'All', 'time']):
                files_used_for_data_frame =  "MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*" if(not Use_Pass_2) else "MC_Gen_sidis_epip_richcap.inb.qa.inb-clasdis_*"
                if(Use_New_PF):
                    files_used_for_data_frame = str(files_used_for_data_frame.replace("qa.45nA_job_", "qa.new5.45nA_job_")).replace("qa.inb-clasdis_", "qa.new5.inb-clasdis")
                    if(Tag_Proton):
                        files_used_for_data_frame = str(files_used_for_data_frame).replace("qa.new", "qa.wProton.new")
                rdf = ROOT.RDataFrame("h22", "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/", "" if(not Use_Pass_2) else "Pass2/", str(files_used_for_data_frame)]))
            else:
                rdf = ROOT.RDataFrame("h22", str(file_location))
                files_used_for_data_frame =  "".join(["MC_Gen_sidis_epip_richcap.inb.qa", "."                 if(not Use_New_PF) else ".new5.",  "45nA_job_" if(not Use_Pass_2) else "inb-clasdis_", str(file_num), "*"])
            
    print("".join(["\nLoading File(s): ", str(files_used_for_data_frame)]))
    
    # if(output_all_histo_names_Q == "yes"):
    #     print(f"{color.BOLD}Columns of the RDataFrame when first loaded:{color.END}")
    #     for ii in range(0, len(rdf.GetColumnNames()), 1):
    #         print(f"{str((rdf.GetColumnNames())[ii])} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    #     print(f"\tTotal length= {str(len(rdf.GetColumnNames()))}\n\n")
    
    print(f"{color.BOLD}\nDefining pre-made functions to be used within the RDataFrame{color.END}")
    # ROOT.gInterpreter.Declare(New_Fiducial_DC_Cuts_Functions)
    ROOT.gInterpreter.Declare(Pion_Energy_Loss_Cor_Function)
    ROOT.gInterpreter.Declare(Correction_Code_Full_In)
    ROOT.gInterpreter.Declare(Rotation_Matrix)
    ROOT.gInterpreter.Declare(New_Integrated_z_pT_and_MultiDim_Binning_Code)
    
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##
    
    # Getting Current Date
    datetime_object_full = datetime.now()
    startMin_full, startHr_full, startDay_full = datetime_object_full.minute, datetime_object_full.hour, datetime_object_full.day
    if(datetime_object_full.minute < 10):
        timeMin_full = ''.join(['0', str(datetime_object_full.minute)])
    else:
        timeMin_full = str(datetime_object_full.minute)
    # Printing Current Time
    if(datetime_object_full.hour >  12 and datetime_object_full.hour <  24):
        print("".join(["The time that this code started is ", str((datetime_object_full.hour) - 12), ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour <  12 and datetime_object_full.hour >   0):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour),        ":", timeMin_full, " a.m."]))
    if(datetime_object_full.hour == 12):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour),        ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour == 0 or   datetime_object_full.hour == 24):
        print("".join(["The time that this code started is 12:", timeMin_full, " a.m."]))
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##
    
    
    
    ###########################################################
    #################     Final ROOT File     #################
    
    ROOT_File_Output_Name = "Data_REC"

    # # # See File_Name_Updates.md file for notes on versions older than "New_Q2_Y_Bins_V5_"
            
    Common_Name = f"New_TTree{Cut_Configuration_Name}_V1_"
    # Ran on 9/10/2024
    # First version of the TTree File Creator

    Common_Name = f"New_TTree{Cut_Configuration_Name}_V2_"
    # Ran on 11/8/2024
    # Second version of the TTree File Creator
        # Modified the Fiducial cut code to no longer need to declare 'New_Fiducial_DC_Cuts_Functions'
    
    if(run_Mom_Cor_Code == "yes"):
        if((smear_factor != "0.75") and ("".join([str(smear_factor).replace(".", ""), "_V"]) not in Common_Name)):
            Common_Name = Common_Name.replace("_V", "".join(["_", str(smear_factor).replace(".", ""), "_V"]))
            # Same as the last version of Common_Name to be run but with any value of smear_factor not being equal to the default value of 0.75
            
            
    if((datatype in ["rdf"]) and (Mom_Correction_Q in ["no"])):
        Common_Name = "".join(["Uncorrected_", str(Common_Name)])
        # Not applying momentum corrections (despite them being available)
            
    if(Use_Weight):
        if(not Q4_Weight):
            # Using the modulations of the Generated Monte Carlo
            Common_Name = "".join([Common_Name, "Modulated_"])
        else:
            # Using the Q4 wieghts
            Common_Name = "".join([Common_Name, "Q4_Wieght_"])
            
    if(not Use_Pass_2):
        Common_Name = "".join(["Pass_1_", str(Common_Name)])
        print(f"\n\n\t{color.Error}Using Pass 1 Version of Data/MC Files{color.END}")
    else:
        Common_Name = "".join(["Pass_2_", str(Common_Name)])
        print(f"\n\n\t{color.BBLUE}Using Pass 2 Version of Data/MC Files{color.END}")
        
    if(Tag_Proton):
        Common_Name = "".join(["Tagged_Proton_", str(Common_Name)])
        print(f"\n\n\t{color.Error}Tagging Proton{color.END}")
    
    if(datatype == 'rdf'):
        ROOT_File_Output_Name     = "".join(["SIDIS_epip_Data_REC_",                      str(Common_Name), str(file_num), ".root"])
    if(datatype == 'mdf'):
        ROOT_File_Output_Name     = "".join(["SIDIS_epip_MC_Matched_",                    str(Common_Name), str(file_num), ".root"])
        if((not Run_With_Smear) and (run_Mom_Cor_Code != "yes")):
            ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Matched_",      "Unsmeared_", str(Common_Name), str(file_num), ".root"])
    if(datatype == 'gdf'):
        ROOT_File_Output_Name     = "".join(["SIDIS_epip_MC_GEN_",                        str(Common_Name), str(file_num), ".root"])
    if(datatype == 'pdf'):
        ROOT_File_Output_Name     = "".join(["SIDIS_epip_MC_Only_Matched_",               str(Common_Name), str(file_num), ".root"])
        if((not Run_With_Smear) and (run_Mom_Cor_Code != "yes")):
            ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Only_Matched_", "Unsmeared_", str(Common_Name), str(file_num), ".root"])
        
    if(output_type in ["data", "test", "tree"]):
        ROOT_File_Output_Name = "".join(["DataFrame_", str(ROOT_File_Output_Name)])
    
    print(f"\nFile being made is: {color.BOLD}{str(ROOT_File_Output_Name)}{color.END}")
    
    
    #################     Final ROOT File     #################
    ###########################################################
    
    
    ################################################################     Done Loading Data Files     ################################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ############################################################    Particle Momentum Correction Code    ############################################################
    
    
    # New_z_pT_and_MultiDim_Binning_Code = """ See ExtraAnalysisCodeValues.py for details
        
    # Correction_Code_Full_In = """ See ExtraAnalysisCodeValues.py for details
    
    if(Mom_Correction_Q != "yes"):
        print("".join([color.Error if(datatype in ["rdf"]) else color.RED, "\n\nNot running with Momentum Corrections\n", color.END]))
    else:
        print("".join([color.BBLUE,                                        "\n\nRunning with Momentum Corrections\n",     color.END]))
        
        
    ###################################################################################################################################################################
    #################################################################   End of Momentum Corrections   #################################################################
    ###----------##----------##----------##----------##----------##-------------------------------------##----------##----------##----------##----------##----------###
    ################################################################# Calculating Kinematic Variables #################################################################
    ###################################################################################################################################################################
    
    
    ######################################################################################
    ##=====##  These calculations may have been made in the groovy code already  ##=====##
    ######################################################################################

    if("beam" not in rdf.GetColumnNames()):
        if("RadState" not in rdf.GetColumnNames()):
            rdf = rdf.Define("RadState", "0")
            rdf = rdf.Define("beam",  f"ROOT::Math::PxPyPzMVector(0, 0, {Beam_Energy}, 0);")
        else:
            rdf = rdf.Define("beam",  f"""
            auto beam_init = ROOT::Math::PxPyPzMVector(0, 0, {Beam_Energy}, 0);
            if(RadState == 1){{ // Initial-State Radiation
                auto rad_photon = ROOT::Math::PxPyPzMVector(gx, gy, gz, sqrt(gE*gE - (gx*gx + gy*gy + gz*gz)));
                auto beam___rad = beam_init - rad_photon;
                return beam___rad;
            }}
            else{{return beam_init;}} // Final-State/No Radiation (i.e. RadState = 2 or RadState = 0)""")
            # for var_coordinate in ["x", "y", "z"]:
            #     rdf = rdf.Define(f"e{var_coordinate}_uncorrected", f"e{var_coordinate}")
            #     rdf = rdf.Redefine(f"e{var_coordinate}", f"""
            #     if(RadState == 2){{return (e{var_coordinate} + g{var_coordinate});}} // Final-State Radiation
            #     else{{return e{var_coordinate};}} // Initial-State/No Radiation (i.e. RadState = 1 or RadState = 0)""")
        rdf = rdf.Define("beamV", """
        TLorentzVector beamV_init(beam.Px(), beam.Py(), beam.Pz(), beam.E());
        return beamV_init;""")
        
    
    ##=====## The following is for the Tagged Proton files ##=====##
    if(Tag_Proton):
        print(f"\n{color.BBLUE}Calculating Variables with the Tagged Proton{color.END}\n")
        rdf = rdf.Define("MM2_pro", "".join(["""
        auto fe       = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip     = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto targ     = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto ele      = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pip0     = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
        auto proV     = ROOT::Math::PxPyPzMVector(prox,  proy,  proz,  0.938272);
        // auto MM_pro_V = beam + targ - ele - pip0 - proV;
        auto MM_pro_V = beam + targ - ele - proV;
        return MM_pro_V.M2();"""]))
        rdf = rdf.Define("MM_pro", "sqrt(MM2_pro)")
        rdf = rdf.Define("pro",    "sqrt(prox*prox + proy*proy + proz*proz)")
    
    ##=====## The following is for backwards compatibility ##=====##
    if("pipx" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipx", "px")
    if("pipy" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipy", "py")
    if("pipz" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipz", "pz")
        
    if(((Mom_Correction_Q in ["yes"]) or True) and (str(datatype) in ["rdf", "mdf"]) and Use_Pass_2):
        print(f"{color.BBLUE}\nApplying Pass 2 (Forward Detector) Energy Loss Corrections to the Pi+ Pion\n{color.END}")
        rdf = rdf.Define("Energy_Loss_Cor_Factor", """
            double pip_mom                  =       sqrt(pipx*pipx + pipy*pipy + pipz*pipz);
            double pip__th                  = atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*(180/3.1415926);
            auto p_pip_loss                 = eloss_pip_In_Forward(pip_mom, pip__th);
            auto pip_Energy_Loss_Cor_Factor = ((pip_mom + p_pip_loss)/pip_mom);
            return pip_Energy_Loss_Cor_Factor;
        """)
        for pion_mom in ["pipx", "pipy", "pipz"]:
            rdf = rdf.Redefine(str(pion_mom), f"Energy_Loss_Cor_Factor*{pion_mom}")
        
    
    if('calc' not in files_used_for_data_frame):
        #####################     Energy     #####################
        # try:
        #     rdf = rdf.Define("el_E", "".join([str(Correction_Code_Full_In), """
        #     auto fe    = dppC(ex, ey, ez, esec, 0, """,          "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        #     auto ele   = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        #     auto ele_E = ele.E();
        #     return ele_E;"""]))
        #     rdf = rdf.Define("pip_E", "".join([str(Correction_Code_Full_In), """
        #     auto fpip   = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        #     auto pip0   = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
        #     auto pip0_E = pip0.E();
        #     return pip0_E;"""]))
        # except:
        #     print(f"{color.Error}\nMomentum Corrections Failed...\n{color.END}")
        #     rdf = rdf.Define("el_E", """
        #     auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        #     auto ele_E = ele.E();
        #     return ele_E;""")
        #     rdf = rdf.Define("pip_E", """
        #     auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        #     auto pip0_E = pip0.E();
        #     return pip0_E;""")
        # if(datatype in ["mdf", "pdf"]):
        #     rdf = rdf.Define("el_E_gen", """
        #     auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
        #     auto ele_E_gen = ele.E();
        #     return ele_E_gen;""")
        #     rdf = rdf.Define("pip_E_gen", """
        #     auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
        #     auto pip0_E_gen = pip0.E();
        #     return pip0_E_gen;""")
        
        #####################     Momentum     #####################

        try:
            rdf = rdf.Define("el",  "".join(["""
            auto fe     = dppC(ex, ey, ez, esec, 0, """,          "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
            double el_P = fe*(sqrt(ex*ex + ey*ey + ez*ez));
            return el_P;"""]))
            rdf = rdf.Define("pip", "".join(["""
            auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
            double pip_P = fpip*(sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
            return pip_P;"""]))
            if((run_Mom_Cor_Code == "yes")   and (str(datatype) not in ["gdf"])):
                rdf = rdf.Define("el_no_cor",  """
                double el_P_no_cor  = (sqrt(ex*ex + ey*ey + ez*ez));
                return el_P_no_cor;""")
                rdf = rdf.Define("pip_no_cor", """
                double pip_P_no_cor = (sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
                return pip_P_no_cor;""")
            if((Mom_Correction_Q in ["yes"]) and (str(datatype)     in ["rdf"])):
                rdf = rdf.Define("Complete_Correction_Factor_Ele", "".join(["""
                auto Correction_Factor_Ele = dppC(ex,     ey,   ez,   esec, 0, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
                return Correction_Factor_Ele;"""]))
                rdf = rdf.Define("Complete_Correction_Factor_Pip", "".join(["""
                auto Correction_Factor_Pip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
                """,  "Correction_Factor_Pip = Correction_Factor_Pip*Energy_Loss_Cor_Factor;" if(Use_Pass_2) else "", """
                return Correction_Factor_Pip;"""]))
        except:
            print(color.Error, "\n\nMomentum Corrections Failed...\n\n", color.END)
            rdf = rdf.Define("el",  "sqrt(ex*ex + ey*ey + ez*ez)")
            rdf = rdf.Define("pip", "sqrt(pipx*pipx + pipy*pipy + pipz*pipz)")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("el_gen",  "sqrt(ex_gen*ex_gen + ey_gen*ey_gen + ez_gen*ez_gen)")
            rdf = rdf.Define("pip_gen", "sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen + pipz_gen*pipz_gen)")

        #####################     Theta Angle     #####################

        rdf = rdf.Define("elth",          "atan2(sqrt(ex*ex + ey*ey), ez)*TMath::RadToDeg()")
        rdf = rdf.Define("pipth",         "atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*TMath::RadToDeg()")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("elth_gen",  "atan2(sqrt(ex_gen*ex_gen + ey_gen*ey_gen), ez_gen)*TMath::RadToDeg()")
            rdf = rdf.Define("pipth_gen", "atan2(sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen), pipz_gen)*TMath::RadToDeg()")

        #####################     Phi Angle     #####################

        rdf = rdf.Define("elPhi", """
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto elPhi = ele.Phi()*TMath::RadToDeg();
        if(elPhi < 0){
            elPhi += 360;
        }
        return elPhi;""")
        rdf = rdf.Define("elPhi_Local", """
        auto           ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto     Phi_Local = ele.Phi()*TMath::RadToDeg();
        if(((esec == 4 || esec == 3) && Phi_Local < 0) || (esec > 4 && Phi_Local < 90)){Phi_Local += 360;}
        auto   elPhi_Local = Phi_Local - (esec - 1)*60;
        return elPhi_Local;""")
        
        rdf = rdf.Define("pipPhi", """
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pipPhi = pip0.Phi()*TMath::RadToDeg();
        if(pipPhi < 0){
            pipPhi += 360;
        }
        return pipPhi;""")
        rdf = rdf.Define("pipPhi_Local", """
        auto          pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto     Phi_Local = pip0.Phi()*TMath::RadToDeg();
        if(((pipsec == 4 || pipsec == 3) && Phi_Local < 0) || (pipsec > 4 && Phi_Local < 90)){Phi_Local += 360;}
        auto   pipPhi_Local = Phi_Local - (pipsec - 1)*60;
        return pipPhi_Local;""")
        
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("elPhi_gen", """
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto elPhi_gen = ele.Phi()*TMath::RadToDeg();
            if(elPhi_gen < 0){
                elPhi_gen += 360;
            }
            return elPhi_gen;""")
            rdf = rdf.Define("pipPhi_gen", """
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipy_gen, 0.13957);
            auto pipPhi_gen = pip0.Phi()*TMath::RadToDeg();
            if(pipPhi_gen < 0){
                pipPhi_gen += 360;
            }
            return pipPhi_gen;""")


        #####################     Sectors (angle definitions)     #####################
        
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("esec_gen","""
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto ele_phi = (180/3.1415926)*ele.Phi();
            int esec_gen = 0;
            if(ele_phi >= -30 && ele_phi < 30){
                esec_gen = 1;
            }
            if(ele_phi >= 30 && ele_phi < 90){
                esec_gen = 2;
            }
            if(ele_phi >= 90 && ele_phi < 150){
                esec_gen = 3;
            }
            if(ele_phi >= 150 || ele_phi < -150){
                esec_gen = 4;
            }
            if(ele_phi >= -90 && ele_phi < -30){
                esec_gen = 5;
            }
            if(ele_phi >= -150 && ele_phi < -90){
                esec_gen = 6;
            }
            return esec_gen;""")
            rdf = rdf.Define("pipsec_gen","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
            auto pip_phi = (180/3.1415926)*pip0.Phi();
            int pipsec_gen = 0;
            if(pip_phi >= -45 && pip_phi < 15){
                pipsec_gen = 1;
            }
            if(pip_phi >= 15 && pip_phi < 75){
                pipsec_gen = 2;
            }
            if(pip_phi >= 75 && pip_phi < 135){
                pipsec_gen = 3;
            }
            if(pip_phi >= 135 || pip_phi < -165){
                pipsec_gen = 4;
            }
            if(pip_phi >= -105 && pip_phi < -45){
                pipsec_gen = 5;
            }
            if(pip_phi >= -165 && pip_phi < -105){
                pipsec_gen = 6;
            }
            return pipsec_gen;""")


        #####################     Other Values     #####################

        rdf = rdf.Define("vals", "".join(["""
        auto fe      = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        
        auto targ    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        
        auto ele     = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pip0    = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto epipX   = beam + targ - ele - pip0;
        auto q       = beam - ele;
        auto Q2      = - q.M2();
        auto v       = beam.E() - ele.E();
        auto xB      = Q2/(2*targ.M()*v);
        auto W2      = targ.M2() + 2*targ.M()*v - Q2;
        auto W       = sqrt(W2);
        auto y       = (targ.Dot(q))/(targ.Dot(beam));
        auto z       = ((pip0.E())/(q.E()));
        auto gamma   = 2*targ.M()*(xB/sqrt(Q2));
        auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));
        
        std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};

        return vals;"""]))
        
        rdf = rdf.Define('MM',  'vals[0]') # Missing Mass
        rdf = rdf.Define('MM2', 'vals[1]') # Missing Mass Squared 
        rdf = rdf.Define('Q2',  'vals[2]') # lepton momentum transfer squared
        rdf = rdf.Define('xB',  'vals[3]') # fraction of the proton momentum that is carried by the struck quark
        # rdf = rdf.Define('v',   'vals[4]') # energy of the virtual photon
        # rdf = rdf.Define('s',   'vals[5]') # center-of-mass energy squared
        rdf = rdf.Define('W',   'vals[6]') # center-of-mass energy
        rdf = rdf.Define('y',   'vals[7]') # energy fraction of the incoming lepton carried by the virtual photon
        rdf = rdf.Define('z',   'vals[8]') # energy fraction of the virtual photon carried by the outgoing hadron
        # rdf = rdf.Define('epsilon', 'vals[9]') # ratio of the longitudinal and transverse photon flux
        
        if(Use_New_PF and (str(datatype) not in ["gdf"])):
            print(f"\n{color.BOLD}Creating variables for Valerii's (New) Fiducial Cuts{color.END}")
            rdf = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=rdf, fidlevel='N/A', Particle="ele")
            rdf = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=rdf, fidlevel='N/A', Particle="pip")
        
        if(datatype not in ["rdf"]):
            print(f"\n{color.BOLD}CONDITIONS FOR IDENTIFYING BACKGROUND EVENTS:\n{color.END}\tBG_Cut_Function(dataframe='{datatype}') = {color.GREEN}{BG_Cut_Function(dataframe=str(datatype))}{color.END}")
        
        if(datatype in ["gdf"]):
            if("MM" in str(BG_Cut_Function(dataframe="mdf"))):
                print(f"{color.BGREEN}\nMAKING A DEFAULT CUT ON GENERATED MISSING MASS (MM > 1.5 required)\n{color.END}")
                # rdf = rdf.Filter("MM > 1.5")
                rdf = rdf.Define("Default_MM_Cut_1_5", "return (MM > 1.5);")
            else:
                print(f"{color.Error}\n{color.UNDERLINE}NOT{color.END_R} making the default cut on Generated Missing Mass (MM_gen > 1.5 is not currently being considered as background based on BG_Cut_Function(dataframe='mdf'))\n{color.END}")
                
        if(datatype in ["mdf"]):
            BG_string = BG_Cut_Function(dataframe="mdf")
            if(("PID_el  == 0" not in str(BG_string)) and ("(PID_el  != 11)"  not in str(BG_string))):
                print(f"\n{color.Error}WARNINING: May be missing the unmatched ELECTRON background cuts\n\t{color.UNDERLINE}RUN WITH CAUTION{color.END}\n")
            if(("PID_pip == 0" not in str(BG_string)) and ("(PID_pip != 211)" not in str(BG_string))):
                print(f"\n{color.Error}WARNINING: May be missing the unmatched PI+ PION background cuts\n\t{color.UNDERLINE}RUN WITH CAUTION{color.END}\n")
            del BG_string
            
        
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("vals_gen", "".join(["""
            auto targ_gen    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
            auto ele_gen     = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto pip0_gen    = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);

            auto epipX_gen   = beam + targ_gen - ele_gen - pip0_gen;
            auto q_gen       = beam - ele_gen;
            auto Q2_gen      = - q_gen.M2();
            auto v_gen       = beam.E() - ele_gen.E();
            auto xB_gen      = Q2_gen/(2*targ_gen.M()*v_gen);
            auto W2_gen      = targ_gen.M2() + 2*targ_gen.M()*v_gen - Q2_gen;
            auto W_gen       = sqrt(W2_gen);
            auto y_gen       = (targ_gen.Dot(q_gen))/(targ_gen.Dot(beam));
            auto z_gen       = ((pip0_gen.E())/(q_gen.E()));
            auto gamma_gen   = 2*targ_gen.M()*(xB_gen/sqrt(Q2_gen));
            auto epsilon_gen = (1 - y_gen - 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen))/(1 - y_gen + 0.5*(y_gen*y_gen) + 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen));

            std::vector<double> vals_gen = {epipX_gen.M(), epipX_gen.M2(), Q2_gen, xB_gen, v_gen, W2_gen, W_gen, y_gen, z_gen, epsilon_gen};

            return vals_gen;"""]))

            rdf = rdf.Define('MM_gen',  'vals_gen[0]')
            rdf = rdf.Define('MM2_gen', 'vals_gen[1]')
            rdf = rdf.Define('Q2_gen',  'vals_gen[2]')
            rdf = rdf.Define('xB_gen',  'vals_gen[3]')
            # rdf = rdf.Define('v_gen',   'vals_gen[4]')
            # rdf = rdf.Define('s_gen',   'vals_gen[5]')
            rdf = rdf.Define('W_gen',   'vals_gen[6]')
            rdf = rdf.Define('y_gen',   'vals_gen[7]')
            rdf = rdf.Define('z_gen',   'vals_gen[8]')
            # rdf = rdf.Define('epsilon_gen', 'vals_gen[9]')
            
            
            PID_Interpertation_Code = """
            int pid_to_index(int pid) {
                using namespace std;
                map<int, pair<int, string>> pid_map = {
                    {-2212, {1, "Anti-Proton"}},
                    {-321,  {2, "K-"}},
                    {-211,  {3, "Pi-"}},
                    {11,    {4, "Electron"}},
                    {0,     {5, "Unidentified"}},
                    {-11,   {6, "Positron"}},
                    {-13,   {7, "Muon+"}},
                    {211,   {8, "Pi+"}},
                    {321,   {9, "K+"}},
                    {2212,  {10, "Proton"}}
                };
                auto it = pid_map.find(pid);
                if (it != pid_map.end()) return it->second.first;
                else return 5; // Other
            };
            """
            ROOT.gInterpreter.Declare(PID_Interpertation_Code)
            # Apply the function and create the histogram
            rdf = rdf.Define("PID_el_idx",  "pid_to_index(PID_el)")
            rdf = rdf.Define("PID_pip_idx", "pid_to_index(PID_pip)")
        
    
    ##############################################################################
    ##=====##  The above calculations used to be run in the groovy code  ##=====##
    ##############################################################################
    
    if(datatype not in ["rdf"]):
        rdf = rdf.Define("Background_Identification_Cuts", BG_Cut_Function(dataframe=str(datatype)))
    
    ####################################################################################################################################################################
    ###################################################     Done with Calculating (Initial) Kinematic Variables      ###################################################
    ###----------##----------##----------##----------##--------------------------------------------------------------##----------##----------##----------##----------###
    ###################################################       Rotation Matrix and Center-of-Mass/Boosted Frame       ###################################################
    ####################################################################################################################################################################
    
    # Rotation_Matrix = """ See ExtraAnalysisCodeValues.py for details
    
    rdf = rdf.Define("vals2", "".join(["""
    auto fe     = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
    auto fpip   = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
    
    auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0,       0.938272);
    
    auto eleM   = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
    auto pip0M  = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
    
    auto lv_qMM = beam - eleM;

    TLorentzVector targ(0, 0, 0, targM.E());
    
    TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
    TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
    
    TLorentzVector lv_q = beamV - ele;

    ///////////////     Angles for Rotation     ///////////////
    double Theta_q = lv_q.Theta();
    double Phi_el  = ele.Phi();

    ///////////////     Rotating to CM Frame     ///////////////

    auto beam_Clone = Rot_Matrix(beamV, -1, Theta_q, Phi_el);
    auto targ_Clone = Rot_Matrix(targ,  -1, Theta_q, Phi_el);
    auto ele_Clone  = Rot_Matrix(ele,   -1, Theta_q, Phi_el);
    auto pip0_Clone = Rot_Matrix(pip0,  -1, Theta_q, Phi_el);
    auto lv_q_Clone = Rot_Matrix(lv_q,  -1, Theta_q, Phi_el);

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

    if(phi_t < 0){
        phi_t += 360;
    }

    // std::vector<double> vals2 = {pT, phi_t, xF, pipx_1, pipy_1, pipz_1, qx, qy, qz, beamx, beamy, beamz, elex, eley, elez};
    std::vector<double> vals2 = {pT, phi_t, xF};

    return vals2;"""]))

    rdf = rdf.Define('pT',    'vals2[0]')    # transverse momentum of the final state hadron
    rdf = rdf.Define('phi_t', 'vals2[1]')    # Most important angle (between lepton and hadron planes)
    rdf = rdf.Define('xF',    'vals2[2]')    # x Feynmann

    # rdf = rdf.Define('pipx_CM','vals2[3]') # CM pi+ x-momentum
    # rdf = rdf.Define('pipy_CM','vals2[4]') # CM pi+ y-momentum
    # rdf = rdf.Define('pipz_CM','vals2[5]') # CM pi+ z-momentum

    # rdf = rdf.Define('qx_CM','vals2[6]') # CM q x-momentum
    # rdf = rdf.Define('qy_CM','vals2[7]') # CM q y-momentum
    # rdf = rdf.Define('qz_CM','vals2[8]') # CM q z-momentum

    # rdf = rdf.Define('beamX_CM','vals2[9]')  # CM beam x-momentum
    # rdf = rdf.Define('beamY_CM','vals2[10]') # CM beam y-momentum
    # rdf = rdf.Define('beamZ_CM','vals2[11]') # CM beam z-momentum

    # rdf = rdf.Define('eleX_CM','vals2[12]') # CM scattered electron x-momentum
    # rdf = rdf.Define('eleY_CM','vals2[13]') # CM scattered electron y-momentum
    # rdf = rdf.Define('eleZ_CM','vals2[14]') # CM scattered electron z-momentum
    
    Run_Uncorrected_phi_t_Info_Q = False
    
    if((datatype in ["rdf"]) and (Mom_Correction_Q in ["yes"]) and Run_Uncorrected_phi_t_Info_Q):
        rdf = rdf.Define("Uncorrected_phi_t_Info", "".join(["""
        auto fpip   = (dppC(pipx, pipy, pipz, pipsec, 1, """, "1" if(not Use_Pass_2) else "3", """) + 1)/(Complete_Correction_Factor_Pip);
        auto eleM   = ROOT::Math::PxPyPzMVector(ex, ey, ez,     0);
        auto pip0M  = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
        auto lv_qMM = beamM - eleM;
        TLorentzVector ele(ex, ey, ez,      eleM.E());
        TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
        TLorentzVector lv_q = beamV - ele;
        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el  = ele.Phi();
        ///////////////     Rotating to CM Frame     ///////////////
        auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
        double phi_h_uncorrected = pip0_Clone.Phi()*TMath::RadToDeg();
        if(phi_h_uncorrected < 0){phi_h_uncorrected += 360;}
        double Delta_phi_h   = phi_t - phi_h_uncorrected;
        double Percent_Phi_h = 0;
        if(Delta_phi_h == 0){Percent_Phi_h = 0;}
        else{
            if(phi_h_uncorrected == 0){Percent_Phi_h = 1;}
            else{Percent_Phi_h = Delta_phi_h/phi_h_uncorrected;}
        }
        Percent_Phi_h = Percent_Phi_h*100;
        std::vector<double> Uncorrected_Phi_h_Info = {phi_h_uncorrected, Delta_phi_h, Percent_Phi_h};

        return Uncorrected_Phi_h_Info;"""]))
        
        
        # rdf = rdf.Define('phi_t_uncorrected', 'Uncorrected_phi_t_Info[0]')
        rdf = rdf.Define('Delta_phi_t',       'Uncorrected_phi_t_Info[1]')
        rdf = rdf.Define('Percent_phi_t',     'Uncorrected_phi_t_Info[2]')
    
    
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define("vals2_gen", "".join(["""
        auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto eleM   = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
        auto pip0M  = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
        auto lv_qMM = beam - eleM;

        TLorentzVector targ(0, 0, 0, targM.E());
        TLorentzVector ele(ex_gen, ey_gen, ez_gen, eleM.E());
        TLorentzVector pip0(pipx_gen, pipy_gen, pipz_gen, pip0M.E());
        TLorentzVector lv_q = beamV - ele;

        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el  = ele.Phi();

        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beamV, -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ,  -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele,   -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0,  -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q,  -1, Theta_q, Phi_el);

        ///////////////     Saving CM components     ///////////////

        double pipx_1_gen = pip0_Clone.X();
        double pipy_1_gen = pip0_Clone.Y();
        double pipz_1_gen = pip0_Clone.Z();

        double qx_gen = lv_q_Clone.X();
        double qy_gen = lv_q_Clone.Y();
        double qz_gen = lv_q_Clone.Z();

        double beamx_gen = beam_Clone.X();
        double beamy_gen = beam_Clone.Y();
        double beamz_gen = beam_Clone.Z();

        double elex_gen = ele_Clone.X();
        double eley_gen = ele_Clone.Y();
        double elez_gen = ele_Clone.Z();

        ///////////////     Boosting Vectors     ///////////////

        auto fCM = lv_q_Clone + targ_Clone;
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

        ///////////////////////////////////     At This Point: The particle vectors have all been rotated and boosted into the CM frame     ///////////////////////////////////

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
        double theta_t     = TMath::ACos(Cos_theta_t);

        double pipTx_gen = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTy_gen = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTz_gen = pip0.P()*TMath::Cos(theta_t);

        TVector3 pipT(pipTx_gen, pipTy_gen, pipTz_gen);

        double phi_t_cross_product_gen = phi_t_cross_product_gen*TMath::RadToDeg();

        ///////////////   x Feynmann   ///////////////
        double xF_gen = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W_gen);

        // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
        double pT_gen    = sqrt(pipx_1_gen*pipx_1_gen + pipy_1_gen*pipy_1_gen);
        double phi_t_gen = pip0_Clone.Phi()*TMath::RadToDeg();

        if(phi_t_gen < 0){
            phi_t_gen += 360;
        }

        // std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen, pipx_1_gen, pipy_1_gen, pipz_1_gen, qx_gen, qy_gen, qz_gen, beamx_gen, beamy_gen, beamz_gen, elex_gen, eley_gen, elez_gen};
        std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen};

        return vals2_gen;"""]))

        rdf = rdf.Define('pT_gen',    'vals2_gen[0]')
        rdf = rdf.Define('phi_t_gen', 'vals2_gen[1]')
        rdf = rdf.Define('xF_gen',    'vals2_gen[2]')
    
    
    
    #################################################################################################################################################################
    ###################################################       Done with Center-of-Mass/Boosted Frame (Main)       ###################################################
    ###----------##----------##----------##----------##-----------------------------------------------------------##----------##----------##----------##----------###
    ###################################################          Defining Smearing Function/Calculations          ###################################################
    #################################################################################################################################################################
    
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Defining the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    
    # smear_factor = "0.75"
    
    smearing_function = "".join(["""
        //=======================================================================//
        //=================//     Simple Smearing Factor      //=================//
        //=======================================================================//
        auto smear_func = [&](TLorentzVector V4, int ivec){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double M_rec   = V4.M();
            double P_rec   = V4.P();
            double Th_rec  = V4.Theta();
            double Phi_rec = V4.Phi();
            
            double P_gen   = V4.P();
            double Th_gen  = V4.Theta();
            double Phi_gen = V4.Phi();
            if(ivec == 0){ // Electron
                auto ele_gen_M = ROOT::Math::PxPyPzMVector(ex_gen,   ey_gen,   ez_gen,   0);
                TLorentzVector ele_gen_V4(ex_gen,   ey_gen,   ez_gen,   ele_gen_M.E());
                P_gen   = ele_gen_V4.P();
                Th_gen  = ele_gen_V4.Theta();
                Phi_gen = ele_gen_V4.Phi();
            }
            if(ivec == 1){ // Pi+ Pion
                auto pip_gen_M = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
                TLorentzVector pip_gen_V4(pipx_gen, pipy_gen, pipz_gen, pip_gen_M.E());
                P_gen   = pip_gen_V4.P();
                Th_gen  = pip_gen_V4.Theta();
                Phi_gen = pip_gen_V4.Phi();
            }
            
            
            // Calculate resolutions
            // double smear_factor = 0.8;
            double smear_factor = """, str(smear_factor), """;
            double P_new_rec    = P_rec   + smear_factor*(P_rec   - P_gen);
            double Th_new_rec   = Th_rec  + smear_factor*(Th_rec  - Th_gen);
            double Phi_new_rec  = Phi_rec + smear_factor*(Phi_rec - Phi_gen);
            Th_new_rec  = Th_rec;
            Phi_new_rec = Phi_rec;
            

            // Making the smeared TLorentzVector:
            TLorentzVector V4_smear(V4.X(), V4.Y(), V4.Z(), V4.E());
            V4_smear.SetE(TMath::Sqrt(P_new_rec*P_new_rec + M_rec*M_rec));
            V4_smear.SetRho(   P_new_rec);
            V4_smear.SetTheta(Th_new_rec);
            V4_smear.SetPhi( Phi_new_rec);
            return V4_smear;
        };"""]) 
    # smearing_function = smearing_function if((smear_factor not in ["FX"]) and (datatype not in ["rdf", "gdf"])) else """
    smearing_function = smearing_function_SF(smear_factor, Use_Pass_2) if((smear_factor not in ["FX"]) and (datatype not in ["rdf", "gdf"])) else """
        //===========================================================================//
        //=================//     Smearing Function (From FX)     //=================//
        //===========================================================================//
        auto smear_func = [&](TLorentzVector V4){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double inM = V4.M();
            double smeared_P  = V4.P();
            double smeared_Th = V4.Theta();
            double smeared_Phi = V4.Phi();
            TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());
            // Calculate resolutions
            double smeared_ThD = TMath::RadToDeg()*smeared_Th;
            double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
            double momS2 = 0.02*smeared_ThD;
            double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
            momR *= 2.0;
            // // From ∆P(El) Sigma distributions:
            // momR *= (0.02408)*V4.P()*V4.P() + (-0.25556)*V4.P() + (1.33331);
            double theS1 = 0.004*smeared_ThD + 0.1;
            double theS2 = 0;
            double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
            theR *= 2.5;
            double phiS1 = 0.85 - 0.015*smeared_ThD;
            double phiS2 = 0.17 - 0.003*smeared_ThD;
            double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
            phiR *= 3.5;
            // cout<<"Smearing Factor for Phi: "<<phiR<<endl;
            // cout<<"Smearing Factor for Th: "<<theR<<endl;
            // cout<<"Smearing Factor for P: "<<momR<<endl;
            // cout<<"Pre-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
            // cout<<"Pre-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
            // cout<<"Pre-Smear P : "<<smeared_P<<endl;
            // overwrite EB (i.e., applying the smear)
            smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
            smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
            smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();
            // cout<<"Smear-Factor Phi (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * phiR * gRandom->Gaus(0,1)))<<endl;
            // cout<<"Smear-Factor Th (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * theR * gRandom->Gaus(0,1)))<<endl;
            // cout<<"Smear-Factor P : "<<(momR  * gRandom->Gaus(0,1) *  V4.P())<<endl;
            // cout<<"Post-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
            // cout<<"Post-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
            // cout<<"Post-Smear P : "<<smeared_P<<endl;
            // EB_rec_mom = GEN_mom + resolution_momentum x gaussian x GEN_mom
            // EB_rec_ang = GEN_ang + resolution_angle x gaussian
            V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
            V4_new.SetRho( smeared_P );
            V4_new.SetTheta( smeared_Th );
            V4_new.SetPhi( smeared_Phi );
            return V4_new;
        };""" if(datatype not in ["rdf", "gdf"]) else ""
    
    
    if((run_Mom_Cor_Code == "yes") and (str(datatype) not in ["rdf", "gdf"])):
        rdf = rdf.Define("el_no_cor_smeared", "".join(["""
        """, str(smearing_function), """
            auto eleM  = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector ele_NO_SMEAR(ex, ey, ez, eleM.E());
            //=================//     Smearing PxPyPzMVector's     //=================//
            TLorentzVector ele_no_cor_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
            //=================//     Vectors have been Smeared     //=================//
            auto el_no_cor_smeared  = ele_no_cor_smeared.P();
            return el_no_cor_smeared;
        """]))
        rdf = rdf.Define("pip_no_cor_smeared", "".join(["""
        """, str(smearing_function), """
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
            TLorentzVector pip0_NO_SMEAR(pipx, pipy, pipz, pip0M.E());
            //=================//     Smearing PxPyPzMVector's     //=================//
            TLorentzVector pip0_no_cor_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """
            //=================//     Vectors have been Smeared     //=================//
            auto pip_no_cor_smeared = pip0_no_cor_smeared.P();
            return pip_no_cor_smeared;
        """]))
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Applying the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    if((datatype in ["mdf", "pdf"]) and Run_With_Smear):
        rdf = rdf.Define("smeared_vals", "".join(["""
        """, str(smearing_function),       """
        
        auto fe    = dppC(ex,   ey,   ez,   esec,   0, """, "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;
        auto fpip  = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;

        auto targM = ROOT::Math::PxPyPzMVector(0,         0,         0,         0.938272);
        auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        TLorentzVector targ(0,         0,         0,            targM.E());
        TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,        eleM.E());
        TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip,    pip0M.E());

        TLorentzVector ele_NO_SMEAR(ex*fe,      ey*fe,     ez*fe,     eleM.E());
        TLorentzVector pip0_NO_SMEAR(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());

        //========================================================================//
        //=================//     Smearing PxPyPzMVector's     //=================//
        //========================================================================//
        
        TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
        TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """

        //=========================================================================//
        //=================//     Vectors have been Smeared     //=================//
        //=========================================================================//

        TLorentzVector lv_q = beamV - ele_smeared;

        auto Delta_Smear_El_P   = abs(ele_smeared.P())        - abs(ele_NO_SMEAR.P());                         // Delta_Smear_El.P();
        auto Delta_Smear_El_Th  = (abs(ele_smeared.Theta())   - abs(ele_NO_SMEAR.Theta()))*TMath::RadToDeg();  // Delta_Smear_El.Theta()*TMath::RadToDeg();
        auto Delta_Smear_El_Phi = (abs(ele_smeared.Phi())     - abs(ele_NO_SMEAR.Phi()))*TMath::RadToDeg();    // Delta_Smear_El.Phi()*TMath::RadToDeg();

        auto Delta_Smear_Pip_P   = abs(pip0_smeared.P())      - abs(pip0_NO_SMEAR.P());                        // Delta_Smear_Pip.P();
        auto Delta_Smear_Pip_Th  = (abs(pip0_smeared.Theta()) - abs(pip0_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_Pip.Theta()*TMath::RadToDeg();
        auto Delta_Smear_Pip_Phi = (abs(pip0_smeared.Phi())   - abs(pip0_NO_SMEAR.Phi()))*TMath::RadToDeg();   // Delta_Smear_Pip.Phi()*TMath::RadToDeg();

        // Rest of calculations are performed as normal from here

        auto epipX         = beamV + targ - ele_smeared - pip0_smeared;
        auto q_smeared     = beamV - ele_smeared;
        auto Q2_smeared    = -q_smeared.M2();
        auto v_smeared     = beamV.E() - ele_smeared.E();
        auto xB_smeared    = Q2_smeared/(2*targ.M()*v_smeared);
        auto W2_smeared    = targ.M2() + 2*targ.M()*v_smeared - Q2_smeared;
        auto W_smeared     = sqrt(W2_smeared);
        auto y_smeared     = (targ.Dot(q_smeared))/(targ.Dot(beamV));
        auto z_smeared     = ((pip0_smeared.E())/(q_smeared.E()));
        auto gamma_smeared = 2*targ.M()*(xB_smeared/sqrt(Q2_smeared));
        auto epsilon_smeared = (1 - y_smeared - 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared))/(1 - y + 0.5*(y_smeared*y_smeared) + 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared));

        // Particles' (Smeared) Energies/Momentums/Angles
        auto ele_E_smeared  = ele_smeared.E();
        auto pip0_E_smeared = pip0_smeared.E();

        auto el_smeared  = ele_smeared.P();
        auto pip_smeared = pip0_smeared.P();

        auto elth_smeared  = ele_smeared.Theta()*TMath::RadToDeg();
        auto pipth_smeared = pip0_smeared.Theta()*TMath::RadToDeg();

        auto elPhi_smeared = ele_smeared.Phi()*TMath::RadToDeg();

        if(elPhi_smeared < 0){elPhi_smeared += 360;}

        auto pipPhi_smeared = pip0_smeared.Phi()*TMath::RadToDeg();

        if(pipPhi_smeared < 0){pipPhi_smeared += 360;}

        //=================================================================================================================================//
        //==============================================//          Rotation Code          //==============================================//
        //=================================================================================================================================//

        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el  = ele_smeared.Phi();

        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beamV,        -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ,         -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele_smeared,  -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0_smeared, -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q,         -1, Theta_q, Phi_el);

        ///////////////     Saving CM components     ///////////////

        double pipx_smeared  = pip0_Clone.X();
        double pipy_smeared  = pip0_Clone.Y();
        double pipz_smeared  = pip0_Clone.Z();

        double qx_smeared    = lv_q_Clone.X();
        double qy_smeared    = lv_q_Clone.Y();
        double qz_smeared    = lv_q_Clone.Z();

        double beamx_smeared = beam_Clone.X();
        double beamy_smeared = beam_Clone.Y();
        double beamz_smeared = beam_Clone.Z();

        double elex_smeared  = ele_Clone.X();
        double eley_smeared  = ele_Clone.Y();
        double elez_smeared  = ele_Clone.Z();

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

        ///////////////////////////////////     At This Point: The particle vectors have all been rotated and boosted into the CM frame     ///////////////////////////////////

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

        double Cos_theta_t = (pip0_smeared.Vect().Dot(lv_q.Vect()))/(pip0_smeared.Vect().Mag()*lv_q.Vect().Mag());
        double theta_t     = TMath::ACos(Cos_theta_t);

        double pipTx = pip0_smeared.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTy = pip0_smeared.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTz = pip0_smeared.P()*TMath::Cos(theta_t);

        TVector3 pipT(pipTx, pipTy, pipTz);

        phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();

        ///////////////   x Feynmann   ///////////////
        double xF_smeared = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);

        // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
        double pT_smeared    = sqrt(pipx_smeared*pipx_smeared + pipy_smeared*pipy_smeared);
        double phi_t_smeared = pip0_Clone.Phi()*TMath::RadToDeg();

        if(phi_t_smeared < 0){phi_t_smeared += 360;}

        double Q2_xB_Bin_smeared = 1;
        double z_pT_Bin_smeared  = 1;

        std::vector<double> smeared_vals = {epipX.M(), epipX.M2(), Q2_smeared, xB_smeared, v_smeared, W2_smeared, W_smeared, y_smeared, z_smeared, epsilon_smeared, pT_smeared, phi_t_smeared, xF_smeared, Q2_xB_Bin_smeared, z_pT_Bin_smeared, el_smeared, ele_E_smeared, elth_smeared, elPhi_smeared, pip_smeared, pip0_E_smeared, pipth_smeared, pipPhi_smeared, Delta_Smear_El_P, Delta_Smear_El_Th, Delta_Smear_El_Phi, Delta_Smear_Pip_P, Delta_Smear_Pip_Th, Delta_Smear_Pip_Phi};
        //                  smeared_vals = {    1    ,     2     ,      3    ,      4    ,     5    ,      6    ,     7    ,     8    ,     9    ,        10      ,     11    ,        12    ,     13    ,        14        ,       15        ,     16    ,       17     ,       18    ,        19    ,      20    ,        21     ,        22    ,         23    ,      24         ,      25          ,      26           ,      27          ,      28           ,      29            };

        return smeared_vals;"""]))

        rdf = rdf.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
        rdf = rdf.Define('z_pT_Bin_smeared',  'smeared_vals[14]')


        ##==================================================##
        ##==========## End of Smeared DataFrame ##==========##
        ##==================================================##
        
    def smear_frame_compatible(Data_Frame, Variable, Smearing_Q):
        if(Data_Frame == "continue"):
            return Data_Frame
        if(("smear" not in Smearing_Q) or (datatype not in ["mdf", "pdf"]) or ((str(Variable) in Data_Frame.GetColumnNames()) and ("mear" in str(Variable))) or ("".join([str(Variable), "_smeared"]) in Data_Frame.GetColumnNames())):
            # Variable should already be defined/cannot smear real/generated data
            # if(str(Variable) in Data_Frame.GetColumnNames()):
            #     print("".join(["Already defined: ", str(Variable)]))
            return Data_Frame
        elif(any(Variable in [test_var, f"{test_var}_smeared"] for test_var in ["esec", "pipsec", "prosec", "Hx", "Hy", "Hx_pip", "Hy_pip", "ele_x_DC_6", "ele_x_DC_18", "ele_x_DC_36", "pip_x_DC_6", "pip_x_DC_18", "pip_x_DC_36", "pro", "MM_pro", "V_PCal", "W_PCal", "U_PCal"])):
            print(f"{color.Error}Cannot smear the variable '{Variable}' {color.UNDERLINE}(Using 'Alias' to the unsmeared variable){color.END}")
            # Data_Frame = "continue"
            Data_Frame = Data_Frame.Define(Variable if("_smeared" in str(Variable)) else f"{Variable}_smeared", str(Variable.replace("_smeared", "")))
            return Data_Frame
        else:
            done_Q = 'no'
            if(Variable in ['MM', 'MM_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('MM_smeared',      'smeared_vals[0]')
            if(Variable in ['MM2', 'MM2_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('MM2_smeared',     'smeared_vals[1]')
            if(Variable in ['Q2', 'Q2_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('Q2_smeared',      'smeared_vals[2]')
            if(Variable in ['xB', 'xB_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('xB_smeared',      'smeared_vals[3]')
            if(Variable in ['v', 'v_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('v_smeared',       'smeared_vals[4]')
            if(Variable in ['s', 's_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('s_smeared',       'smeared_vals[5]')
            if(Variable in ['W', 'W_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('W_smeared',       'smeared_vals[6]')
            if(Variable in ['y', 'y_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('y_smeared',       'smeared_vals[7]')
            if(Variable in ['z', 'z_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('z_smeared',       'smeared_vals[8]')
            if(Variable in ['epsilon', 'epsilon_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('epsilon_smeared', 'smeared_vals[9]')
            if(Variable in ['pT', 'pT_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('pT_smeared',      'smeared_vals[10]')
            if(Variable in ['phi_t', 'phi_t_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('phi_t_smeared',   'smeared_vals[11]')
            if(Variable in ['xF', 'xF_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('xF_smeared',      'smeared_vals[12]')
            if(Variable in ['el', 'el_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('el_smeared',      'smeared_vals[15]')
            if(Variable in ['el_E', 'el_E_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('el_E_smeared',    'smeared_vals[16]')
            if(Variable in ['elth', 'elth_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('elth_smeared',    'smeared_vals[17]')
            if(Variable in ['elPhi', 'elPhi_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('elPhi_smeared',   'smeared_vals[18]')
            if(Variable in ['pip', 'pip_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('pip_smeared',     'smeared_vals[19]')
            if(Variable in ['pip_E', 'pip_E_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('pip_E_smeared',   'smeared_vals[20]')
            if(Variable in ['pipth', 'pipth_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('pipth_smeared',   'smeared_vals[21]')
            if(Variable in ['pipPhi', 'pipPhi_smeared']):
                done_Q = 'yes'
                return Data_Frame.Define('pipPhi_smeared',  'smeared_vals[22]')
            if('Delta_Smear_El_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[23]')
            if('Delta_Smear_El_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[24]')
            if('Delta_Smear_El_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[25]')
            if('Delta_Smear_Pip_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[26]')
            if('Delta_Smear_Pip_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[27]')
            if('Delta_Smear_Pip_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable),     'smeared_vals[28]')

            if(done_Q != 'yes'):
                # Failed to get a new definition
                return Data_Frame
            
            
    def Smear_Compare_Variable(DataFrame, Variable_Input):
        if(DataFrame == "continue"):
            return DataFrame
        Variable_Smear = f"{Variable_Input}_smeared"
        DataFrame_with_Smear     = smear_frame_compatible(Data_Frame=DataFrame, Variable=Variable_Input, Smearing_Q="smear")
        if(DataFrame_with_Smear == "continue"):
            return "continue"
        try:
            DataFrame_with_Smear = DataFrame_with_Smear.Define(f"Smeared_Effect_on_{Variable_Input}",         f"{Variable_Input} - {Variable_Smear}")
            DataFrame_with_Smear = DataFrame_with_Smear.Define(f"Smeared_Effect_on_{Variable_Input}_gen",     f"{Variable_Input} - {Variable_Smear}")
            Smeared_Percent_of_VARIABLE = "".join([f"""
            double Smear_Percent_{Variable_Input} = 0;
            if(Smeared_Effect_on_{Variable_Input} == 0)""", "{", f"Smear_Percent_{Variable_Input} = 0;", """}
            else{""", f"""
                if({Variable_Input} == 0)""", "{", f"Smear_Percent_{Variable_Input} = 1;", """}
                else{""", f"Smear_Percent_{Variable_Input} = (Smeared_Effect_on_{Variable_Input})/({Variable_Input});", """}
            }""", f"""
            Smear_Percent_{Variable_Input} = Smear_Percent_{Variable_Input}*100;
            // cout<<endl<<"Calculating Smeared_Percent_of_{Variable_Input}:"<<endl<<"   "<<endl<<"   Smeared_Effect_on_{Variable_Input} = "<<Smeared_Effect_on_{Variable_Input}<<endl<<"   {Variable_Input} = "<<{Variable_Input}<<endl<<"   Smeared_Percent_of_{Variable_Input} = "<<Smear_Percent_{Variable_Input}<<endl;
            return Smear_Percent_{Variable_Input};"""])
            # print(Smeared_Percent_of_VARIABLE)
            DataFrame_with_Smear = DataFrame_with_Smear.Define(f"Smeared_Percent_of_{Variable_Input}",     Smeared_Percent_of_VARIABLE)
            DataFrame_with_Smear = DataFrame_with_Smear.Define(f"Smeared_Percent_of_{Variable_Input}_gen", Smeared_Percent_of_VARIABLE)
            del Smeared_Percent_of_VARIABLE
        except:
            print(f"{color.Error}Error in Smear_Compare_Variable(DataFrame, {Variable_Input}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
            return "continue"
        return DataFrame_with_Smear
            
    ##=========================================================================================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=================================##     End of Smearing Functions     ##=================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=========================================================================================================##
    
    
    
    if(Use_Weight):
        if(not Q4_Weight):
            print(f"{color.BGREEN}\n{color_bg.BLUE}Running 'Closure Test' for Modulated Monte Carlo Generated phi_h distributions...{color.END}\n\n")
            ##==========================================================================================================##
            ##------------------------------------##==============================##------------------------------------##
            ##====================================##     Event Weighing Begin     ##====================================##
            ##------------------------------------##==============================##------------------------------------##
            ##==========================================================================================================##
            rdf = rdf.Define('Event_Weight', "".join(["""
            """, "".join([""" 
            auto   Par_B_Test   = -0.500;
            auto   Par_C_Test   =  0.025;""", """
            auto   PHI_H        = phi_t*TMath::DegToRad();""" if(datatype in ["gdf"]) else """
            auto   PHI_H        = phi_t_gen*TMath::DegToRad();""", """
            auto   Event_Weight = 1 + Par_B_Test*TMath::Cos(PHI_H) + Par_C_Test*TMath::Cos(2*PHI_H);
            """])  if((datatype in ["mdf", "gdf", "pdf"]) and Use_Weight)             else "auto Event_Weight = 1;", """
            return Event_Weight;
            """]))
            ##==========================================================================================================##
            ##------------------------------------##==============================##------------------------------------##
            ##====================================##      Event Weighing End      ##====================================##
            ##------------------------------------##==============================##------------------------------------##
            ##==========================================================================================================##
        else:
            print(f"{color.BGREEN}\n{color_bg.BLUE}Running 'Q4 Weight' for weighing the Monte Carlo distributions...{color.END}\n\n")
            ##==========================================================================================================##
            ##------------------------------------##==============================##------------------------------------##
            ##====================================##     Event Weighing Begin     ##====================================##
            ##------------------------------------##==============================##------------------------------------##
            ##==========================================================================================================##
            rdf = rdf.Define('Event_Weight', "".join(["".join(["""
            auto   Q4           = Q2*Q2;""" if(datatype in ["gdf"]) else """
            auto   Q4           = Q2_gen*Q2_gen;""", """
            auto   Event_Weight = Q4;
            """])  if((datatype in ["mdf", "gdf", "pdf"]) and Use_Weight)             else "auto Event_Weight = 1;", """
            return Event_Weight;
            """]))
            ##==========================================================================================================##
            ##------------------------------------##==============================##------------------------------------##
            ##====================================##      Event Weighing End      ##====================================##
            ##------------------------------------##==============================##------------------------------------##
            ##==========================================================================================================##
    elif(datatype in ["mdf", "gdf", "pdf"]):
        print(f"{color.BOLD}\nNOT running 'Closure Test' for Modulated Monte Carlo Generated phi_h distributions...{color.END}\n\n")
    
    
    
    
    
    ##==========================================================================================================##
    ##---------------------------------##====================================##---------------------------------##
    ##=================================##   ∆P from Exclusive Calculations   ##=================================##
    ##---------------------------------##====================================##---------------------------------##
    ##==========================================================================================================##

    ########################################################################################
    ####================================================================================####
    ##==========##==========##      ∆P Calculations (Normal)      ##==========##==========##
    ####================================================================================####
    ########################################################################################

    rdf = rdf.Define("Delta_Pel_Cors", "".join(["""
        auto fe   = dppC(ex,   ey,   ez,   esec,   0, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = """, str(Beam_Energy), """;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        // Below are the kinematic calculations of the electron momentum (from el+pro->el+Pip+N) based on the assumption that the electron angle and π+ reconstruction were measured by the detector correctly for elastic events in the epipX channel
        // (The neutron is used as the "missing" particle)

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
        auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

        auto pel_Calculated = (termA + termC)/termB;

        auto Delta_Pel_Cors = pel_Calculated - eleC.P();
        """,  "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Pel_Cors = el_gen - eleC.P();", """
        return Delta_Pel_Cors;"""]))


    rdf = rdf.Define("Delta_Ppip_Cors", "".join(["""
        auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = """, str(Beam_Energy), """;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        // Below are the kinematic calculations of the π+ momentum (from el+pro->el+Pip+N) based on the assumption that the π+ angle and electron reconstruction were measured by the detector correctly for elastic events in the epipX channel
        // (The neutron is used as the "missing" particle)

        auto termA = (neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2;
        auto termB = 0.938*(Beam_Energy - eleC.P()) - Beam_Energy*eleC.P()*(1 - cos(eleC.Theta()));
        auto termC = ((eleC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC))) - (Beam_Energy*cos(pipC.Theta())));

        auto sqrtTerm = ((termA - termB)*(termA - termB)) + (0.13957*0.13957)*((termC*termC) - ((0.938 + Beam_Energy - eleC.P())*(0.938 + Beam_Energy - eleC.P())));
        auto denominator = ((0.938 + Beam_Energy - eleC.P()) + termC)*((0.938 + Beam_Energy - eleC.P()) - termC);
        auto numeratorP = (termA - termB)*termC + (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);
        auto numeratorM = (termA - termB)*termC - (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);

        auto pip_CalculateP = numeratorP/denominator;
        auto pip_CalculateM = numeratorM/denominator;

        auto pip_Calculate = pip_CalculateP;

        if(abs(pipC.P() - pip_CalculateP) >= abs(pipC.P() - pip_CalculateM)){
            pip_Calculate = pip_CalculateM;
        }
        if(abs(pipC.P() - pip_CalculateP) <= abs(pipC.P() - pip_CalculateM)){
            pip_Calculate = pip_CalculateP;
        }

        auto Delta_Ppip_Cors = pip_Calculate - pipC.P();
        """,  "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Ppip_Cors = pip_gen - pipC.P();", """
        return Delta_Ppip_Cors;"""]))
    

    ############################################################################################
    ####====================================================================================####
    ##==========##==========##      ∆Theta Calculations (Normal)      ##==========##==========##
    ####====================================================================================####
    ############################################################################################

    rdf = rdf.Define("Delta_Theta_el_Cors", "".join(["""
        auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = """, str(Beam_Energy), """;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        
        // auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
        //     // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy" - "Proton Mass"
            
        auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

        auto Theta_el_Calculated = acos((1/Beam_Energy)*(((termA + termC)/eleC.P()) - termB));

        auto Delta_Theta_el_Cors = (180/3.1415926)*(Theta_el_Calculated - eleC.Theta());
        
        """,  "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Theta_el_Cors = (180/3.1415926)*(elth_gen - eleC.Theta());", """

        return Delta_Theta_el_Cors;"""]))


    rdf = rdf.Define("Delta_Theta_pip_Cors",  "".join(["""
        auto fe   = dppC(ex,   ey,   ez,   esec,   0, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else ("1" if(str(datatype) in ['rdf']) else "2") if(not Use_Pass_2) else ("3" if(str(datatype) in ['rdf']) else "4"), """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = """, str(Beam_Energy), """;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            
        // auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
        //     // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"
        
        auto termC = Beam_Energy*pipC.E() + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*"π+ Energy" + "Proton Mass"*"π+ Energy"

        auto Theta_pip_Calculated = acos((termA + termC - termB*eleC.P())/(Beam_Energy*pipC.P()));

        auto Delta_Theta_pip_Cors = (180/3.1415926)*(Theta_pip_Calculated - pipC.Theta());
        
        """,  "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Theta_pip_Cors = (180/3.1415926)*(pipth_gen - pipC.Theta());", """

        return Delta_Theta_pip_Cors;"""]))

    

    ###############################################################################################
    ####=======================================================================================####
    ##==========##==========##         ∆P Calculations (Smeared)         ##==========##==========##
    ####=======================================================================================####
    ###############################################################################################

    if((datatype not in ["rdf", "gdf"]) and Run_With_Smear):

        rdf = rdf.Define("Delta_Pel_Cors_smeared", "".join([str(smearing_function), """
            auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;

            auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

            TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
            TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
            
            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = """, str(Beam_Energy), """;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            // Below are the kinematic calculations of the electron momentum (from el+pro->el+Pip+N) based on the assumption that the electron angle and π+ reconstruction were measured by the detector correctly for elastic events in the epipX channel
            // (The neutron is used as the "missing" particle)

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto pel_Calculated = (termA + termC)/termB;

            auto Delta_Pel_Cors_smeared = pel_Calculated - eleC.P();
            // auto Delta_Pel_Cors_smeared = el_gen - eleC.P();

            return Delta_Pel_Cors_smeared;"""]))


        rdf = rdf.Define("Delta_Ppip_Cors_smeared", "".join([str(smearing_function), """
            auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2" if(not Use_Pass_2) else "4", """) + 1;
            
            auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
            
            TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
            TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
            
            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());
            
            auto Beam_Energy = """, str(Beam_Energy), """;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            // Below are the kinematic calculations of the π+ momentum (from el+pro->el+Pip+N) based on the assumption that the π+ angle and electron reconstruction were measured by the detector correctly for elastic events in the epipX channel
            // (The neutron is used as the "missing" particle)

            auto termA = (neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2;
            auto termB = 0.938*(Beam_Energy - eleC.P()) - Beam_Energy*eleC.P()*(1 - cos(eleC.Theta()));
            auto termC = ((eleC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC))) - (Beam_Energy*cos(pipC.Theta())));

            auto sqrtTerm    = ((termA - termB)*(termA - termB)) + (0.13957*0.13957)*((termC*termC) - ((0.938 + Beam_Energy - eleC.P())*(0.938 + Beam_Energy - eleC.P())));
            auto denominator = ((0.938 + Beam_Energy - eleC.P()) + termC)*((0.938 + Beam_Energy - eleC.P()) - termC);
            auto numeratorP  = (termA - termB)*termC + (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);
            auto numeratorM  = (termA - termB)*termC - (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);

            auto pip_CalculateP = numeratorP/denominator;
            auto pip_CalculateM = numeratorM/denominator;

            auto pip_Calculate = pip_CalculateP;

            if(abs(pipC.P() - pip_CalculateP) >= abs(pipC.P() - pip_CalculateM)){
                pip_Calculate = pip_CalculateM;
            }
            if(abs(pipC.P() - pip_CalculateP) <= abs(pipC.P() - pip_CalculateM)){
                pip_Calculate = pip_CalculateP;
            }

            auto Delta_Ppip_Cors_smeared = pip_Calculate - pipC.P();
            // auto Delta_Ppip_Cors_smeared = pip_gen - pipC.P();

            return Delta_Ppip_Cors_smeared;"""]))
    

        ############################################################################################
        ####====================================================================================####
        ##==========##==========##     ∆Theta Calculations (Smeared)      ##==========##==========##
        ####====================================================================================####
        ############################################################################################

        rdf = rdf.Define("Delta_Theta_el_Cors_smeared", "".join([str(smearing_function), """

            auto eleM  = ROOT::Math::PxPyPzMVector(ex,   ey,   ez,   0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
            
            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = """, str(Beam_Energy), """;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"

            // auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            //     // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"

            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy" - "Proton Mass"

            auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto Theta_el_Calculated_smeared = acos((1/Beam_Energy)*(((termA + termC)/eleC.P()) - termB));

            auto Delta_Theta_el_Cors_smeared = (180/3.1415926)*(Theta_el_Calculated_smeared - eleC.Theta());
            
            """, "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Theta_el_Cors_smeared = (180/3.1415926)*(elth_gen - eleC.Theta());", """

            return Delta_Theta_el_Cors_smeared;"""]))


        rdf = rdf.Define("Delta_Theta_pip_Cors_smeared",  "".join([str(smearing_function),  """

            auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
            
            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = """, str(Beam_Energy), """;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"

            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"

            // auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            //     // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto termC = Beam_Energy*pipC.E() + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*"π+ Energy" + "Proton Mass"*"π+ Energy"

            auto Theta_pip_Calculated_smeared = acos((termA + termC - termB*eleC.P())/(Beam_Energy*pipC.P()));

            auto Delta_Theta_pip_Cors_smeared = (180/3.1415926)*(Theta_pip_Calculated_smeared - pipC.Theta());
            
            """, "" if(str(datatype) not in ["mdf", "pdf"] or True) else "Delta_Theta_pip_Cors_smeared = (180/3.1415926)*(pipth_gen - pipC.Theta());", """

            return Delta_Theta_pip_Cors_smeared;"""]))
    
    
    
    ########################################################################################
    ####================================================================================####
    ##==========##==========##         ∆P/P Smear Factors         ##==========##==========##
    ####================================================================================####
    ########################################################################################
    
    rdf = rdf.Define("DP_el_SF",  "Delta_Pel_Cors/el")
    rdf = rdf.Define("DP_pip_SF", "Delta_Ppip_Cors/pip")
    if((datatype not in ["rdf", "gdf"]) and Run_With_Smear):
        rdf = rdf.Define("DP_el_SF_smeared",  "Delta_Pel_Cors_smeared/smeared_vals[15]")
        rdf = rdf.Define("DP_pip_SF_smeared", "Delta_Ppip_Cors_smeared/smeared_vals[19]")
        
        rdf = rdf.Define("Dele_SF", "abs(el  - smeared_vals[15])/el")
        rdf = rdf.Define("Dpip_SF", "abs(pip - smeared_vals[19])/pip")

        
    print("Kinematic Variables have been calculated.")
    
    # if(output_all_histo_names_Q == "yes"):
    #     print(f"\n{color.BOLD}Print all (currently) defined content of the RDataFrame:{color.END}")
    #     for ii in range(0, len(rdf.GetColumnNames()), 1):
    #         print(f"{str((rdf.GetColumnNames())[ii])} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    #     print(f"\tTotal length= {str(len(rdf.GetColumnNames()))}\n\n")
    
    ###################################################################################################################################################################
    ###################################################       Done with Calculating (All) Kinematic Variables       ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################                  Making Cuts to DataFrames                  ###################################################
    ###################################################################################################################################################################
    
    
    def filter_Valerii(Data_Frame, Valerii_Cut, Include_Pion=Use_New_PF, Cut_Flag=False):
        if(("Valerii_Cut" in Valerii_Cut) or ("Complete" in Valerii_Cut) or Cut_Flag):
            Valerii_Cut_Code = "".join(["""
                auto func = [&](double x, double k, double b){
                    return k * x + b;
                };
                struct line{
                    double k;
                    double b;
                };
                auto isOutOfLines = [&](double x, double y, line topLine, line botLine){
                    return y > func(x, topLine.k, topLine.b) || y < func(x, botLine.k, botLine.b);
                };
                auto BadElementKnockOut = [&](double hx, double hy, int sector, int cutLevel){
                    double widthChange = 0;
                    if (cutLevel == 0)  widthChange = -1;
                    if (cutLevel == 2)  widthChange = 1;
                    if (sector == 5) return true;
                    if (sector == 1){
                        double k = tan(29.5*3.1415/180);
                        double b = -92;
                        bool test_sec_1 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 9.1} , {k, b - widthChange - 9.1 - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 127} , {k, b - widthChange - 127 - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 127 - 8} , {k, b - widthChange -127 - 8 - 2.4}) );
                               
                        return test_sec_1;       
                    }
                    if (sector == 2){
                        double k = tan(30.4*3.1415/180);
                        double b = 120.5;
                        bool test_sec_2 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 4.4}));
                        return test_sec_2;
                    }
                    if (sector == 3){
                        bool test_sec_3 = ((hx - widthChange) > - 303 || (hx + widthChange) < -310);
                        return test_sec_3;
                    }
                    if (sector == 4){
                        double k = tan(-29.6*3.1415/180);
                        double b = -232.8;
                        bool test_sec_4 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 3.5}));
                        
                        return test_sec_4;
                    }
                    if (sector == 6){
                        double k = tan(-30.6*3.1415/180);
                        double b = -185;
                        
                        bool test_sec_6 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 2}) && isOutOfLines(hx, hy, {k, b + widthChange - 8.3} , {k, b - widthChange - 8.3 - 2.2}) );
                        
                        return test_sec_6;
                    }
                    return false;
                };
                """, "return BadElementKnockOut(Hx, Hy, esec, 1);" if((not Include_Pion) or ("Hpip" in Skipped_Fiducial_Cuts) or True) else "return (BadElementKnockOut(Hx, Hy, esec, 1) && BadElementKnockOut(Hx_pip, Hy_pip, pipsec, 1));"])
            if(not Cut_Flag):
                Data_Frame_Clone = Data_Frame.Filter(Valerii_Cut_Code)
            else:
                Data_Frame_Clone = Data_Frame.Define("Valerii_OG_Cut", Valerii_Cut_Code)
            return Data_Frame_Clone
        else:
            return Data_Frame
    
    
    # Meant for the exclusive ep->eπ+(N) reaction
    def Calculated_Exclusive_Cuts(Smear_Q):
        output = "".join(["""
        """, str(smearing_function), """
        auto targ = ROOT::Math::PxPyPzMVector(0,    0,    0,       0.938);
        auto ele  = ROOT::Math::PxPyPzMVector(ex,   ey,   ez,      0);
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz,    0.13957);
        """, "".join(["""
        TLorentzVector eleS(ex, ey, ez, ele.E());
        TLorentzVector pipS(pipx, pipy, pipz, pip0.E());
        
        TLorentzVector ele_smeared = smear_func(eleS""", (");" if("ivec" not in str(smearing_function)) else ", 0);" if("stop_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 0, stop_over_smear, less_over_smear);"), """
        TLorentzVector pip_smeared = smear_func(pipS""", (");" if("ivec" not in str(smearing_function)) else ", 1);" if("stop_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear);" if("bool less_over_smear" not in str(smearing_function)) else ", 1, stop_over_smear, less_over_smear);"), """
        
        ele  = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), 0);
        pip0 = ROOT::Math::PxPyPzMVector(pip_smeared.X(), pip_smeared.Y(), pip_smeared.Z(), 0.13957);
        
        """]) if(("smear" in Smear_Q) and (datatype not in ["rdf", "gdf"])) else "", """

        auto MM_Vector = beam + targ - ele - pip0;

        // double elPhi = (180/3.1415926)*atan2(ey, ex);
        auto elPhi_cut = (180/3.1415926)*ele.Phi();

        if(((esec == 4 || esec == 3) && elPhi_cut < 0) || (esec > 4 && elPhi_cut < 90)){
            elPhi_cut += 360;
        }
        double localelPhiS = (elPhi_cut - (esec - 1)*60) - (30/ele.P());

        auto cut_up = 1.1;
        auto cut_down = 0;

        if(esec == 1){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.002512)*ele.P() + (1.025113);  
                cut_down = (-0.006564)*ele.P() + (0.91629);
            }
            if(localelPhiS < -5){
                cut_up   = (-0.002166)*ele.P() + (1.047257);
                cut_down = (-0.00436)*ele.P()  + (0.919216);
            }
            if(localelPhiS > 5){
                cut_up   = (-0.006649)*ele.P() + (1.036503);
                cut_down = (-0.008246)*ele.P() + (0.899835);
            }
        }
        if(esec == 2){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.001108)*ele.P() + (1.012364);
                cut_down = (-0.004842)*ele.P() + (0.894447);
            }

            if(localelPhiS < -5){
                cut_up   = (-0.000811)*ele.P() + (1.015682);
                cut_down = (-0.004621)*ele.P() + (0.898917);
            }

            if(localelPhiS > 5){
                cut_up   = (-0.006132)*ele.P() + (1.03695);
                cut_down = (-0.009834)*ele.P() + (0.915225);
            }
        }
        if(esec == 3){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.00808)*ele.P()  + (1.053207);
                cut_down = (-0.014113)*ele.P() + (0.937174);
            }
            if(localelPhiS < -5){
                cut_up   = (-0.011922)*ele.P() + (1.066027);
                cut_down = (-0.014898)*ele.P() + (0.925886);
            }
            if(localelPhiS > 5){
                cut_up   = (-0.008165)*ele.P() + (1.06216);
                cut_down = (-0.009607)*ele.P() + (0.913684);
            }
        }
        if(esec == 4){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.003636)*ele.P() + (1.040308);
                cut_down = (-0.006253)*ele.P() + (0.919061);
            }
            if(localelPhiS < -5){
                cut_up   = (-0.004512)*ele.P() + (1.036327);
                cut_down = (-0.003965)*ele.P() + (0.88969);
            }
            if(localelPhiS > 5){
                cut_up   = (-0.002362)*ele.P() + (1.045388);
                cut_down = (5.5e-05)*ele.P()   + (0.884049);
            }
        }
        if(esec == 5){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.00373)*ele.P()  + (1.027939);
                cut_down = (-0.007682)*ele.P() + (0.920652);
            }
            if(localelPhiS < -5){
                cut_up   = (-0.000977)*ele.P() + (1.011744);
                cut_down = (-0.003504)*ele.P() + (0.89456);
            }
            if(localelPhiS > 5){
                cut_up   = (-0.007179)*ele.P() + (1.056021);
                cut_down = (-0.005851)*ele.P() + (0.908325);
            }
        }
        if(esec == 6){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up   = (-0.004726)*ele.P() + (1.037422);
                cut_down = (-0.007929)*ele.P() + (0.919135);
            }
            if(localelPhiS < -5){
                cut_up   = (-0.005149)*ele.P() + (1.047543);
                cut_down = (-0.007816)*ele.P() + (0.926179);
            }
            if(localelPhiS > 5){
                cut_up   = (-0.004952)*ele.P() + (1.031514);
                cut_down = (-0.009952)*ele.P() + (0.922387);
            }
        }
        // cut_up   = 1.1*cut_up;
        // cut_down = 0.9*cut_down;
        return (MM_Vector.M() < cut_up && MM_Vector.M() > cut_down);"""])
        
        return output
    
    
    ####################################################################################################################################################################
    ###################################################                Done Making Cuts to DataFrames                ###################################################
    ###                                              ##--------------------------------------------------------------##                                              ###
    ###----------------------------------------------##--------------------------------------------------------------##----------------------------------------------###
    ###                                              ##--------------------------------------------------------------##                                              ###
    ###################################################                  Defining Kinematic Binning                  ###################################################
    ####################################################################################################################################################################
    
    
    def Q2_xB_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="2"):

        if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
            print(f"The input:{color.RED} {str(Variable_Type)}{color.END} was not recognized by the function Q2_xB_Bin_Standard_Def_Function(Variable_Type).\nFix input to use anything other than the default calculations of Q2 and xB.")
            Variable_Type  = ""
            
        Q2_xB_For_Binning = "".join(["smeared_vals[2]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "Q2", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", ", ", "smeared_vals[3]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "xB", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])

    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        # Default Binning Scheme is my (original) modified version of Stefan's binning (see below)
        Q2_xB_Bin_Def = "".join(["""
        TH2Poly Q2_xB_Bin_Poly;
        // Q2-xB Bin 1
        double Q2_1[] = {2,         2.28,  3.625,  2.75,   2,        2};
        double xB_1[] = {0.126602,  0.15,  0.24,   0.24,   0.15,     0.126602};
        // Q2-xB Bin 2
        double Q2_2[] = {2,         2.75,  2,      2};
        double xB_2[] = {0.15,      0.24,  0.24,   0.15};
        // Q2-xB Bin 3
        double Q2_3[] = {2.75,      3.625, 5.12,   3.63,   2.75};
        double xB_3[] = {0.24,      0.24,  0.34,   0.34,   0.24};
        // Q2-xB Bin 4
        double Q2_4[] = {2,         2.75,  3.63,   2,      2};
        double xB_4[] = {0.24,      0.24,  0.34,   0.34,   0.24};
        // Q2-xB Bin 5
        double Q2_5[] = {3.63,      5.12,  6.76,   4.7,    3.63};
        double xB_5[] = {0.34,      0.34,  0.45,   0.45,   0.34};
        // Q2-xB Bin 6
        double Q2_6[] = {2,         3.63,  4.7,    2.52,   2,        2};
        double xB_6[] = {0.34,      0.34,  0.45,   0.45,   0.387826, 0.34};
        // Q2-xB Bin 7
        double Q2_7[] = {4.7,       6.76,  10.185, 11.351, 9.52,     7.42,   4.7};
        double xB_7[] = {0.45,      0.45,  0.677,  0.7896, 0.75,     0.708,  0.45};
        // Q2-xB Bin 8
        double Q2_8[] = {2.52,      4.7,   7.42,   5.4,    4.05,     3.05,   2.52};
        double xB_8[] = {0.45,      0.45,  0.708,  0.64,   0.57,     0.50,   0.45};
        
        Q2_xB_Bin_Poly.AddBin(6, Q2_1, xB_1);
        Q2_xB_Bin_Poly.AddBin(4, Q2_2, xB_2);
        Q2_xB_Bin_Poly.AddBin(5, Q2_3, xB_3);
        Q2_xB_Bin_Poly.AddBin(5, Q2_4, xB_4);
        Q2_xB_Bin_Poly.AddBin(5, Q2_5, xB_5);
        Q2_xB_Bin_Poly.AddBin(6, Q2_6, xB_6);
        Q2_xB_Bin_Poly.AddBin(7, Q2_7, xB_7);
        Q2_xB_Bin_Poly.AddBin(7, Q2_8, xB_8);
        int Q2_xB_Bin_New = 0;
        for(int bin_ii=0; bin_ii < 9; bin_ii++){
            if(Q2_xB_Bin_Poly.IsInsideBin(bin_ii, """, str(Q2_xB_For_Binning), """)){
                Q2_xB_Bin_New = bin_ii + 1;
                return Q2_xB_Bin_New;
                break;
            }
        }
        return Q2_xB_Bin_New;"""])
        
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        # New Q2 and xB Binning (My new original binning scheme)
        if(Bin_Version in ["Square", "3"]):
            Q2_xB_Bin_Def = "".join(["""
            TH2Poly Q2_xB_Bin_Poly;
            double xB_0 = 0.126;
            double xB_1 = 0.17;
            double xB_2 = 0.24;
            double xB_3 = 0.34;
            double xB_4 = 0.464;
            double xB_5 = 0.626;
            
            double Q2_0 = 2;
            double Q2_1 = 2.634;
            double Q2_2 = 3.625;
            double Q2_3 = 5.13;
            double Q2_4 = 6.969;
            double Q2_5 = 11.351;
            //=====// xB Group 1 //=====//
            // Q2-xB Bin 1
            double Q2_1_V[]  = {Q2_0,  Q2_0,  Q2_1,  Q2_0};
            double xB_1_V[]  = {xB_0,  xB_1,  xB_1,  xB_0};
            //=====// xB Group 2 //=====//
            // Q2-xB Bin 2
            double Q2_2_V[]  = {Q2_0,  Q2_0,  Q2_1,  Q2_1,  Q2_0};
            double xB_2_V[]  = {xB_1,  xB_2,  xB_2,  xB_1,  xB_1};
            // Q2-xB Bin 3
            double Q2_3_V[]  = {Q2_1,  Q2_1,  Q2_2,  Q2_1};
            double xB_3_V[]  = {xB_1,  xB_2,  xB_2,  xB_1};
            //=====// xB Group 3 //=====//
            // Q2-xB Bin 4
            double Q2_4_V[]  = {Q2_0,  Q2_0,  Q2_1,  Q2_1,  Q2_0};
            double xB_4_V[]  = {xB_2,  xB_3,  xB_3,  xB_2,  xB_2};
            // Q2-xB Bin 5
            double Q2_5_V[]  = {Q2_1,  Q2_1,  Q2_2,  Q2_2,  Q2_1};
            double xB_5_V[]  = {xB_2,  xB_3,  xB_3,  xB_2,  xB_2};
            // Q2-xB Bin 6
            double Q2_6_V[]  = {Q2_2,  Q2_2,  Q2_3,  Q2_2};
            double xB_6_V[]  = {xB_2,  xB_3,  xB_3,  xB_2};        
            //=====// xB Group 4 //=====//
            // Q2-xB Bin 7
            double Q2_7_V[]  = {Q2_0,  Q2_0,  Q2_1,  Q2_1,   Q2_0};
            double xB_7_V[]  = {xB_3,  0.388, xB_4,  xB_3,   xB_3};
            // Q2-xB Bin 8
            double Q2_8_V[]  = {Q2_1,  Q2_1,  Q2_2,  Q2_2,   Q2_1};
            double xB_8_V[]  = {xB_3,  xB_4,  xB_4,  xB_3,   xB_3};
            // Q2-xB Bin 9
            double Q2_9_V[]  = {Q2_2,  Q2_2,  Q2_3,  Q2_3,   Q2_2};
            double xB_9_V[]  = {xB_3,  xB_4,  xB_4,  xB_3,   xB_3};
            // Q2-xB Bin 10
            double Q2_10_V[] = {Q2_3,  Q2_3,  Q2_4,  Q2_3};
            double xB_10_V[] = {xB_3,  xB_4,  xB_4,  xB_3};
            //=====// xB Group 5 //=====//
            // Q2-xB Bin 11
            double Q2_11_V[] = {Q2_1,  Q2_2,  Q2_2,  3.05,   Q2_1};
            double xB_11_V[] = {xB_4,  xB_4,  0.54,  0.50,   xB_4};
            // Q2-xB Bin 12
            double Q2_12_V[] = {Q2_2,  Q2_2,  4.05,  Q2_3,   Q2_3,  Q2_2};
            double xB_12_V[] = {xB_4,  0.54,  0.57,  xB_5,   xB_4,  xB_4};
            // Q2-xB Bin 13
            double Q2_13_V[] = {Q2_3,  Q2_4,  Q2_4,  Q2_3,   Q2_3};
            double xB_13_V[] = {xB_4,  xB_4,  0.692, xB_5,   xB_4};
            // Q2-xB Bin 14
            double Q2_14_V[] = {Q2_4,  Q2_4,  7.42,  9.52,   Q2_5, 10.185,  Q2_4};
            double xB_14_V[] = {xB_4,  0.692, 0.708, 0.75, 0.7896,  0.677,  xB_4};
            Q2_xB_Bin_Poly.AddBin(4, Q2_1_V,  xB_1_V);   //  1
            Q2_xB_Bin_Poly.AddBin(5, Q2_2_V,  xB_2_V);   //  2
            Q2_xB_Bin_Poly.AddBin(4, Q2_3_V,  xB_3_V);   //  3
            Q2_xB_Bin_Poly.AddBin(5, Q2_4_V,  xB_4_V);   //  4
            Q2_xB_Bin_Poly.AddBin(5, Q2_5_V,  xB_5_V);   //  5
            Q2_xB_Bin_Poly.AddBin(4, Q2_6_V,  xB_6_V);   //  6
            Q2_xB_Bin_Poly.AddBin(5, Q2_7_V,  xB_7_V);   //  7
            Q2_xB_Bin_Poly.AddBin(5, Q2_8_V,  xB_8_V);   //  8
            Q2_xB_Bin_Poly.AddBin(5, Q2_9_V,  xB_9_V);   //  9
            Q2_xB_Bin_Poly.AddBin(4, Q2_10_V, xB_10_V);  // 10
            Q2_xB_Bin_Poly.AddBin(5, Q2_11_V, xB_11_V);  // 11
            Q2_xB_Bin_Poly.AddBin(6, Q2_12_V, xB_12_V);  // 12
            Q2_xB_Bin_Poly.AddBin(5, Q2_13_V, xB_13_V);  // 13
            Q2_xB_Bin_Poly.AddBin(7, Q2_14_V, xB_14_V);  // 14
            int Q2_xB_Bin_New = 0;
            for(int bin_ii=0; bin_ii < 15; bin_ii++){
                if(Q2_xB_Bin_Poly.IsInsideBin(bin_ii, """, str(Q2_xB_For_Binning), """)){
                    Q2_xB_Bin_New = bin_ii + 1;
                    return Q2_xB_Bin_New;
                    break;
                }
            }
            return Q2_xB_Bin_New;"""])

    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    
        # Q2 and xB Binning (See Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
        if(Bin_Version in ["OG", "Stefan"]):
            Q2_xB_Bin_Def = "".join(["""
            TH2Poly Q2_xB_Bin_Poly;
            // Q2-xB Bin 1
            Q2_xB_Bin_Poly.AddBin(5, {1.3,  2.28,  1.38,   1.3,    1.3},              {0.0835, 0.15, 0.15,  0.12,   0.0835});
            // Q2-xB Bin 2
            Q2_xB_Bin_Poly.AddBin(6, {1.38, 1.98,  2.75,   1.5,    1.45, 1.38},       {0.15,   0.15, 0.24,  0.24,   0.2,   0.15});
            // Q2-xB Bin 3
            Q2_xB_Bin_Poly.AddBin(5, {1.98, 2.28,  3.625,  2.75,   1.98},             {0.15,   0.15, 0.24,  0.24,   0.15});
            // Q2-xB Bin 4
            Q2_xB_Bin_Poly.AddBin(7, {1.5,  2.75,  3.63,   1.6,    1.56, 1.53, 1.5},  {0.24,   0.24, 0.34,  0.34,   0.30,  0.27,  0.24});
            // Q2-xB Bin 5
            Q2_xB_Bin_Poly.AddBin(5, {2.75, 3.625, 5.12,   3.63,   2.75},             {0.24,   0.24, 0.34,  0.34,   0.24});
            // Q2-xB Bin 6
            Q2_xB_Bin_Poly.AddBin(5, {1.6,  3.63,  4.7,    2.52,   1.6},              {0.34,   0.34, 0.45,  0.45,   0.34});
            // Q2-xB Bin 7
            Q2_xB_Bin_Poly.AddBin(5, {3.63, 5.12,  6.76,   4.7,    3.63},             {0.34,   0.34, 0.45,  0.45,   0.34});
            // Q2-xB Bin 8
            Q2_xB_Bin_Poly.AddBin(7, {2.52, 4.7,   7.42,   5.4,    4.05, 3.05, 2.52}, {0.45,   0.45, 0.708, 0.64,   0.57,  0.50,  0.45});
            // Q2-xB Bin 9
            Q2_xB_Bin_Poly.AddBin(7, {4.7,  6.76,  10.185, 11.351, 9.52, 7.42, 4.7},  {0.45,   0.45, 0.677, 0.7896, 0.75,  0.708, 0.45});
            int Q2_xB_Bin_New = 0;
            for(int bin_ii=0; bin_ii < 10; bin_ii++){
                if(Q2_xB_Bin_Poly.IsInsideBin(bin_ii, """, str(Q2_xB_For_Binning), """)){
                    Q2_xB_Bin_New = bin_ii + 1;
                    return Q2_xB_Bin_New;
                    break;
                }
            }
            return Q2_xB_Bin_New;"""])
            
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    
        # Uses Q2 and y variables for square kinematic binning instead of Q2 and xB (the variable being defined will likely still contain references to the Q2-xB binning since the name defaults as such)
        if(Bin_Version in ["5", "Y_bin", "Y_Bin"]):
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
        
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    
        # Uses Q2 and y variables for square kinematic binning instead of Q2 and xB (the variable being defined will likely still contain references to the Q2-xB binning since the name defaults as such)
        # Updated version
        if(Bin_Version in ["4", "y_bin", "y_Bin"]):
            Q2_For_Binning = "smeared_vals[2]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "".join(["Q2", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
            y_For_Binning  = "smeared_vals[7]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "".join(["y",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])

            Q2_xB_Bin_Def = "".join(["""
            int Q2_y_Bin_New = 0;
            // Q2-y Bins 1-4:
            if(""",     str(Q2_For_Binning), " > 2.000 && ", str(Q2_For_Binning), """ < 2.423){
                // Bin 1
                if(""", str(y_For_Binning),  " > 0.650 && ", str(y_For_Binning),  """ < 0.750){
                    Q2_y_Bin_New = 1;
                    return Q2_y_Bin_New;
                }
                // Bin 2
                if(""", str(y_For_Binning),  " > 0.550 && ", str(y_For_Binning),  """ < 0.650){
                    Q2_y_Bin_New = 2;
                    return Q2_y_Bin_New;
                }
                // Bin 3
                if(""", str(y_For_Binning),  " > 0.450 && ", str(y_For_Binning),  """ < 0.550){
                    Q2_y_Bin_New = 3;
                    return Q2_y_Bin_New;
                }
                // Bin 4
                if(""", str(y_For_Binning),  " > 0.300 && ", str(y_For_Binning),  """ < 0.450){
                    Q2_y_Bin_New = 4;
                    return Q2_y_Bin_New;
                }
            }

            // Q2-y Bins 5-8:
            if(""",     str(Q2_For_Binning), " > 2.423 && ", str(Q2_For_Binning), """ < 2.987){
                // Bin 5
                if(""", str(y_For_Binning),  " > 0.650 && ", str(y_For_Binning),  """ < 0.750){
                    Q2_y_Bin_New = 5;
                    return Q2_y_Bin_New;
                }
                // Bin 6
                if(""", str(y_For_Binning),  " > 0.550 && ", str(y_For_Binning),  """ < 0.650){
                    Q2_y_Bin_New = 6;
                    return Q2_y_Bin_New;
                }
                // Bin 7
                if(""", str(y_For_Binning),  " > 0.450 && ", str(y_For_Binning),  """ < 0.550){
                    Q2_y_Bin_New = 7;
                    return Q2_y_Bin_New;
                }
                // Bin 8
                if(""", str(y_For_Binning),  " > 0.300 && ", str(y_For_Binning),  """ < 0.450){
                    Q2_y_Bin_New = 8;
                    return Q2_y_Bin_New;
                }
            }

            // Q2-y Bins 9-12:
            if(""",     str(Q2_For_Binning), " > 2.987 && ", str(Q2_For_Binning), """ < 3.974){
                // Bin 9
                if(""", str(y_For_Binning),  " > 0.650 && ", str(y_For_Binning),  """ < 0.750){
                    Q2_y_Bin_New = 9;
                    return Q2_y_Bin_New;
                }
                // Bin 10
                if(""", str(y_For_Binning),  " > 0.550 && ", str(y_For_Binning),  """ < 0.650){
                    Q2_y_Bin_New = 10;
                    return Q2_y_Bin_New;
                }
                // Bin 11
                if(""", str(y_For_Binning),  " > 0.450 && ", str(y_For_Binning),  """ < 0.550){
                    Q2_y_Bin_New = 11;
                    return Q2_y_Bin_New;
                }
                // Bin 12
                if(""", str(y_For_Binning),  " > 0.350 && ", str(y_For_Binning),  """ < 0.450){
                    Q2_y_Bin_New = 12;
                    return Q2_y_Bin_New;
                }
            }
            
            // Q2-y Bins 13-14:
            if(""",     str(Q2_For_Binning), " > 3.974 && ", str(Q2_For_Binning), """ < 5.384){
                // Bin 13
                if(""", str(y_For_Binning),  " > 0.650 && ", str(y_For_Binning),  """ < 0.750){
                    Q2_y_Bin_New = 13;
                    return Q2_y_Bin_New;
                }
                // Bin 14
                if(""", str(y_For_Binning),  " > 0.550 && ", str(y_For_Binning),  """ < 0.650){
                    Q2_y_Bin_New = 14;
                    return Q2_y_Bin_New;
                }
            }
            
            // Q2-y Bin 15:
            if(""", str(Q2_For_Binning), " > 3.974 && ", str(Q2_For_Binning), " < 5.948 && ", str(y_For_Binning), " > 0.450 && ", str(y_For_Binning), """ < 0.550){
                    Q2_y_Bin_New = 15;
                    return Q2_y_Bin_New;
            }
            
            // Q2-y Bin 16
            if(""", str(Q2_For_Binning), " > 5.384 && ", str(Q2_For_Binning), " < 9.896 && ", str(y_For_Binning), " > 0.650 && ", str(y_For_Binning), """ < 0.750){
                Q2_y_Bin_New = 16;
                return Q2_y_Bin_New;
            }
            // Q2-y Bin 17
            if(""", str(Q2_For_Binning), " > 5.384 && ", str(Q2_For_Binning), " < 7.922 && ", str(y_For_Binning), " > 0.550 && ", str(y_For_Binning), """ < 0.650){
                Q2_y_Bin_New = 17;
                return Q2_y_Bin_New;
            }

            return Q2_y_Bin_New;"""])
        
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
            
        # Turns off the kinematic binning options by assigning every 'Q2_xB_Bin_New' to be 1 (should run faster when the kinematic binning is not necessary)
        if(Bin_Version in ["Off", "off"]):
            Q2_xB_Bin_Def = """
            int Q2_xB_Bin_New = 1;
            return Q2_xB_Bin_New;"""
            
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
            

        return Q2_xB_Bin_Def
        
        
        
        
##########################################################################################################################################################################################
##########################################################################################################################################################################################
        
        
        
        
    def z_pT_Bin_Standard_Def_Function(Variable_Type="", Bin_Version="2"):
        if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
            print("".join(["The input: ",     color.RED, str(Variable_Type),        color.END, " was not recognized by the function z_pT_Bin_Standard_Def_Function(Variable_Type='", str(Variable_Type), "', Bin_Version='", str(Bin_Version), "').\nFix input to use anything other than the default calculations of z and pT."]))
            Variable_Type  = ""
            
        Q2_xB_Bin_event_name = "".join(["Q2_xB_Bin" if(Bin_Version not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q2_y_Bin" if(("y_" in Bin_Version) or (Bin_Version == "4")) else "Q2_Y_Bin", "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in ["", "4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        z_pT_Bin_event_name  = "".join(["z_pT_Bin",                                                                                                                                                          "".join(["_", str(Bin_Version)]) if(str(Bin_Version) not in [""])                                               else "" , "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        
        # if(str(Q2_xB_Bin_event_name) not in rdf.GetColumnNames()):
        #     print("".join(["The Q2-xB Bin: ", color.RED, str(Q2_xB_Bin_event_name), color.END, " was not recognized by the function z_pT_Bin_Standard_Def_Function(Variable_Type='", str(Variable_Type), "', Bin_Version='", str(Bin_Version), "').\nNeed to correctly define the Q2-xB bin (using Q2_xB_Bin_2 as default).."]))
        #     Q2_xB_Bin_event_name = "Q2_xB_Bin_2"
        
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        z_pT_Bin_Standard_Def = "".join(["""
            /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

            auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry){
                // z_or_pT = 0 corresponds to z bins
                // z_or_pT = 1 corresponds to pT bins

                // For Q2_xB Bin 1 (was 3 in old scheme)
                if(Q2_xB_Bin_Num == 1){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60,  0.75, 1.0};

                    if(z_or_pT == 0){return z_Borders[7 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 2
                if(Q2_xB_Bin_Num == 2){
                    float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){return z_Borders[7 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 3 (was 5 in old scheme)
                if(Q2_xB_Bin_Num == 3){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60,  0.75, 1.0};

                    if(z_or_pT == 0){return z_Borders[7 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 4
                if(Q2_xB_Bin_Num == 4){
                    float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30,  0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){return z_Borders[6 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 5 (was 7 in old scheme)
                if(Q2_xB_Bin_Num == 5){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22,  0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT == 0){return z_Borders[6 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 6
                if(Q2_xB_Bin_Num == 6){
                    float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                    float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                    if(z_or_pT == 0){return z_Borders[5 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 7
                if(Q2_xB_Bin_Num == 7){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22,  0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT == 0){return z_Borders[6 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 7 (was 9 in old scheme)
                if(Q2_xB_Bin_Num == 7 || Q2_xB_Bin_Num == 9){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39,  0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT == 0){return z_Borders[5 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }
                // For Q2_xB Bin 8
                if(Q2_xB_Bin_Num == 8){
                    float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                    float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45,  0.70};

                    if(z_or_pT == 0){return z_Borders[5 - entry];}
                    if(z_or_pT == 1){return pT_Borders[entry];}
                }

                float empty = 0;
                return empty;
            };

            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////

            double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
            double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;

            int Q2_xB_Bin_event_val = """, str(Q2_xB_Bin_event_name), """;
            int z_pT_Bin_event_val  = 0;
            
            // Default:
            int Num_z_Borders  = 0;
            int Num_pT_Borders = 0;

            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')
            
            // For Q2_xB Bin 0
            if(Q2_xB_Bin_event_val == 0){
                z_pT_Bin_event_val = 0;
                return z_pT_Bin_event_val; // Cannot create z-pT Bins without propper Q2-xB Bins
            }
            // For Q2_xB Bin 1, 2, and 3
            if(Q2_xB_Bin_event_val == 1 || Q2_xB_Bin_event_val == 2 || Q2_xB_Bin_event_val == 3){
                Num_z_Borders  = 8; Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_event_val == 4){
                Num_z_Borders  = 7; Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_event_val == 5){
                Num_z_Borders  = 7; Num_pT_Borders = 7;
            }
            // For Q2_xB Bin 6, 7, and 9
            if(Q2_xB_Bin_event_val == 6 || Q2_xB_Bin_event_val == 7 || Q2_xB_Bin_event_val == 9){
                Num_z_Borders  = 6; Num_pT_Borders = 6;
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_event_val == 8){
                Num_z_Borders  = 6; Num_pT_Borders = 5;
            }
            if(Q2_xB_Bin_event_val == 0){
                Num_z_Borders  = 1; Num_pT_Borders = 1;
            }

            if(Num_z_Borders == 0){
                Num_z_Borders = 1; Num_pT_Borders = 1;
            }

            int z_pT_Bin_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z-pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_event_val != 0){continue;     // If the bin has already been assigned, this line will end the loop.
                                                          // This is to make sure the loop does not run longer than what is necessary.
                }
                if(z_event_val > Borders_function(Q2_xB_Bin_event_val, 0, zbin) && z_event_val < Borders_function(Q2_xB_Bin_event_val, 0, zbin - 1)){
                    // Found the correct z bin
                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_event_val != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_event_val > Borders_function(Q2_xB_Bin_event_val, 1, pTbin) && pT_event_val < Borders_function(Q2_xB_Bin_event_val, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_event_val = z_pT_Bin_count; 
                            // The value of the z_pT_Bin has been set
                            return z_pT_Bin_event_val;
                        }
                        else{
                            z_pT_Bin_count = z_pT_Bin_count + 1; // Checking the next bin
                        }
                    }
                }
                else{
                    z_pT_Bin_count = z_pT_Bin_count + (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }
            return z_pT_Bin_event_val;"""])
        
        
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        if(Bin_Version in ["Square", "3"]):
            z_pT_Bin_Standard_Def = "".join(["""
                /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

                auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry){
                    // z_or_pT = 0 corresponds to z bins
                    // z_or_pT = 1 corresponds to pT bins

                    // For Q2_xB Bin 1
                    if(Q2_xB_Bin_Num == 1){
                        float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60,  0.75, 1.00};

                        if(z_or_pT == 0){return z_Borders[7 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 2
                    if(Q2_xB_Bin_Num == 2){
                        float z_Borders[8]  = {0.17, 0.24, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.00};
                        
                        if(z_or_pT == 0){return z_Borders[7 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 3
                    if(Q2_xB_Bin_Num == 3){
                        float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60,  0.75, 1.00};

                        if(z_or_pT == 0){return z_Borders[7 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 4
                    if(Q2_xB_Bin_Num == 4){
                        float z_Borders[7]  = {0.215, 0.305, 0.36, 0.425, 0.515, 0.615, 0.715};
                        float pT_Borders[8] = {0.05,  0.20,  0.30,  0.40, 0.50,  0.60,  0.75, 1.0};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 5
                    if(Q2_xB_Bin_Num == 5){
                        float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.41, 0.52, 0.73};
                        float pT_Borders[7] = {0.05, 0.22,  0.32, 0.41, 0.51, 0.65, 1.00};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 6
                    if(Q2_xB_Bin_Num == 6){
                        float z_Borders[7]  = {0.15, 0.2,  0.245, 0.305, 0.40, 0.515, 0.73};
                        float pT_Borders[7] = {0.05, 0.22, 0.32,  0.41,  0.51, 0.65,  1.0};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 7/8 (uses old bin 6)
                    if(Q2_xB_Bin_Num == 7 || Q2_xB_Bin_Num == 8){
                        float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                        float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 7 (was 9 in old scheme)
                    if(Q2_xB_Bin_Num == 7 || Q2_xB_Bin_Num == 9){
                        float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39,  0.50, 0.70};
                        float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2_xB Bin 8
                    if(Q2_xB_Bin_Num == 8){
                        float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                        float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45,  0.70};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }

                    float empty = 0;
                    return empty;
                };

                /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////
                
                double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
                double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;

                int Q2_xB_Bin_event_val = """, str(Q2_xB_Bin_event_name), """;
                int z_pT_Bin_event_val  = 0;

                // Default:
                int Num_z_Borders  = 0;
                int Num_pT_Borders = 0;

                // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

                // For Q2_xB Bin 0
                if(Q2_xB_Bin_event_val == 0){
                    z_pT_Bin_event_val = 0;
                    return z_pT_Bin_event_val; // Cannot create z-pT Bins without propper Q2-xB Bins
                }
                else{ 
                    // Using a default number of bins for any event within one of the new Q2-xB bins
                    Num_z_Borders = 8; Num_pT_Borders = 8;
                }
                if(Q2_xB_Bin_event_val == 0){
                    Num_z_Borders  = 1; Num_pT_Borders = 1;
                }
                if(Num_z_Borders == 0){
                    Num_z_Borders = 1; Num_pT_Borders = 1;
                }

                int z_pT_Bin_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                        // based on the number of times the loop has run

                // Determining z-pT Bins
                for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                    if(z_pT_Bin_event_val != 0){continue;     // If the bin has already been assigned, this line will end the loop.
                                                              // This is to make sure the loop does not run longer than what is necessary.
                    }
                    if(z_event_val > Borders_function(Q2_xB_Bin_event_val, 0, zbin) && z_event_val < Borders_function(Q2_xB_Bin_event_val, 0, zbin - 1)){
                        // Found the correct z bin
                        for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                            if(z_pT_Bin_event_val != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                            if(pT_event_val > Borders_function(Q2_xB_Bin_event_val, 1, pTbin) && pT_event_val < Borders_function(Q2_xB_Bin_event_val, 1, pTbin+1)){
                                // Found the correct pT bin
                                z_pT_Bin_event_val = z_pT_Bin_count; 
                                // The value of the z_pT_Bin has been set
                                return z_pT_Bin_event_val;
                            }
                            else{
                                z_pT_Bin_count = z_pT_Bin_count + 1; // Checking the next bin
                            }
                        }
                    }
                    else{
                        z_pT_Bin_count = z_pT_Bin_count + (Num_pT_Borders - 1);
                        // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                        // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                    }    
                }
                return z_pT_Bin_event_val;"""])
            
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        if(Bin_Version in ["5", "Y_bin", "Y_Bin"]):
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
    """, "" if(str(Variable_Type) not in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else """
    // if(PID_el != 11 || PID_pip != 211){
    //     z_pT_Bin_event_val = 0;
    //     MultiDim3D_Bin_val = 0;
    //     MultiDim5D_Bin_val = 0;
    // }""", f"""
    // Refinement of Migration/Overflow Bins
    if((({Q2_xB_Bin_event_name} == 1) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 2) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 3) && ((z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 4) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 5) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 6) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 7) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 8) && ((z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 9) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 10) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 11) && ((z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 12) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 13) && ((z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 14) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 15) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 16) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 23) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 17) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30)))){{
        z_pT_Bin_event_val = 0;
        MultiDim3D_Bin_val = 0;
        MultiDim5D_Bin_val = 0;
    }}
    std::vector<int> z_pT_and_MultiDim_Bins = {{z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val}};
    return z_pT_and_MultiDim_Bins;"""])
            
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        if(Bin_Version in ["6", "Int_bin", "Int_Bin"]):
            z_pT_Bin_Standard_Def = "".join(["""
            double z__event_val = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",     "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;   
            double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT",    "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
            double phi_t_eventV = """, "smeared_vals[11]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "phi_t", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
            int Int_z_pT_Bin_event_val = 0;
            int Int_Phih_Bin_event_val = 0;
            int Int_MultiDim3D_Bin_val = 0;
            int Int_MultiDim5D_Bin_val = 0;
            if(""", Q2_xB_Bin_event_name, """ != 0){
                if(((z__event_val <   0.34) && (z__event_val >  0.27)) && ((pT_event_val <  0.153) && (pT_event_val >   0.05))){Int_z_pT_Bin_event_val =   1;}
                if(((z__event_val <   0.34) && (z__event_val >  0.27)) && ((pT_event_val <  0.258) && (pT_event_val >  0.153))){Int_z_pT_Bin_event_val =   2;}
                if(((z__event_val <   0.34) && (z__event_val >  0.27)) && ((pT_event_val <  0.366) && (pT_event_val >  0.258))){Int_z_pT_Bin_event_val =   3;}
                if(((z__event_val <   0.34) && (z__event_val >  0.27)) && ((pT_event_val <  0.478) && (pT_event_val >  0.366))){Int_z_pT_Bin_event_val =   4;}
                if(((z__event_val <   0.34) && (z__event_val >  0.27)) && ((pT_event_val <   0.59) && (pT_event_val >  0.478))){Int_z_pT_Bin_event_val =   5;}
                if(((z__event_val <  0.415) && (z__event_val >  0.34)) && ((pT_event_val <  0.153) && (pT_event_val >   0.05))){Int_z_pT_Bin_event_val =   6;}
                if(((z__event_val <  0.415) && (z__event_val >  0.34)) && ((pT_event_val <  0.258) && (pT_event_val >  0.153))){Int_z_pT_Bin_event_val =   7;}
                if(((z__event_val <  0.415) && (z__event_val >  0.34)) && ((pT_event_val <  0.366) && (pT_event_val >  0.258))){Int_z_pT_Bin_event_val =   8;}
                if(((z__event_val <  0.415) && (z__event_val >  0.34)) && ((pT_event_val <  0.478) && (pT_event_val >  0.366))){Int_z_pT_Bin_event_val =   9;}
                if(((z__event_val <  0.415) && (z__event_val >  0.34)) && ((pT_event_val <   0.59) && (pT_event_val >  0.478))){Int_z_pT_Bin_event_val =  10;}
                if(((z__event_val <  0.492) && (z__event_val > 0.415)) && ((pT_event_val <  0.153) && (pT_event_val >   0.05))){Int_z_pT_Bin_event_val =  11;}
                if(((z__event_val <  0.492) && (z__event_val > 0.415)) && ((pT_event_val <  0.258) && (pT_event_val >  0.153))){Int_z_pT_Bin_event_val =  12;}
                if(((z__event_val <  0.492) && (z__event_val > 0.415)) && ((pT_event_val <  0.366) && (pT_event_val >  0.258))){Int_z_pT_Bin_event_val =  13;}
                if(((z__event_val <  0.492) && (z__event_val > 0.415)) && ((pT_event_val <  0.478) && (pT_event_val >  0.366))){Int_z_pT_Bin_event_val =  14;}
                if(((z__event_val <  0.492) && (z__event_val > 0.415)) && ((pT_event_val <   0.59) && (pT_event_val >  0.478))){Int_z_pT_Bin_event_val =  15;}
                if(((z__event_val <  0.578) && (z__event_val > 0.492)) && ((pT_event_val <  0.153) && (pT_event_val >   0.05))){Int_z_pT_Bin_event_val =  16;}
                if(((z__event_val <  0.578) && (z__event_val > 0.492)) && ((pT_event_val <  0.258) && (pT_event_val >  0.153))){Int_z_pT_Bin_event_val =  17;}
                if(((z__event_val <  0.578) && (z__event_val > 0.492)) && ((pT_event_val <  0.366) && (pT_event_val >  0.258))){Int_z_pT_Bin_event_val =  18;}
                if(((z__event_val <  0.578) && (z__event_val > 0.492)) && ((pT_event_val <  0.478) && (pT_event_val >  0.366))){Int_z_pT_Bin_event_val =  19;}
                if(((z__event_val <  0.578) && (z__event_val > 0.492)) && ((pT_event_val <   0.59) && (pT_event_val >  0.478))){Int_z_pT_Bin_event_val =  20;}
                if(((z__event_val <  0.665) && (z__event_val > 0.578)) && ((pT_event_val <  0.153) && (pT_event_val >   0.05))){Int_z_pT_Bin_event_val =  21;}
                if(((z__event_val <  0.665) && (z__event_val > 0.578)) && ((pT_event_val <  0.258) && (pT_event_val >  0.153))){Int_z_pT_Bin_event_val =  22;}
                if(((z__event_val <  0.665) && (z__event_val > 0.578)) && ((pT_event_val <  0.366) && (pT_event_val >  0.258))){Int_z_pT_Bin_event_val =  23;}
                if(((z__event_val <  0.665) && (z__event_val > 0.578)) && ((pT_event_val <  0.478) && (pT_event_val >  0.366))){Int_z_pT_Bin_event_val =  24;}
                if(((z__event_val <  0.665) && (z__event_val > 0.578)) && ((pT_event_val <   0.59) && (pT_event_val >  0.478))){Int_z_pT_Bin_event_val =  25;}
                if(Int_z_pT_Bin_event_val == 0){Int_MultiDim3D_Bin_val = 0; Int_MultiDim5D_Bin_val = 0;}
                else{
                    Phih_Bin_event_val     = Find_phi_h_Bin(1, 1, phi_t_eventV); // The reason to use Q2_xB_Bin_event_name, z_pT_Bin_event_val = 1, 1 is that it avoids the issues of the Find_phi_h_Bin() function accounting for 'migration' bins while this definition of the z-pT bins does not use them
                    Int_MultiDim3D_Bin_val = Integrate_Phi_h_Bin_Values[""", str(Q2_xB_Bin_event_name), """][Int_z_pT_Bin_event_val][1] + Phih_Bin_event_val;
                    Int_MultiDim5D_Bin_val = Integrate_Phi_h_Bin_Values[""", str(Q2_xB_Bin_event_name), """][Int_z_pT_Bin_event_val][2] + Phih_Bin_event_val;
                }
            }
            else{Int_z_pT_Bin_event_val = 0; Int_MultiDim3D_Bin_val = 0; Int_MultiDim5D_Bin_val = 0;}
            std::vector<int> Int_z_pT_and_MultiDim_Bins = {Int_z_pT_Bin_event_val, Int_MultiDim3D_Bin_val, Int_MultiDim5D_Bin_val};
            return Int_z_pT_and_MultiDim_Bins;"""])

    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        # if(Bin_Version in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]):
        if(Bin_Version in ["4", "y_bin", "y_Bin"]):
            z_pT_Bin_Standard_Def = "".join(["""
                /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

                auto Borders_function = [&](int Q2_y_Bin_Num, int z_or_pT, int entry){
                    // z_or_pT = 0 corresponds to z bins
                    // z_or_pT = 1 corresponds to pT bins

                    // For Q2-y Bin 1:
                    if(Q2_y_Bin_Num == 1){
                        float z_Borders[6]  = {0.15, 0.20, 0.24, 0.29, 0.40, 0.73};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 2:
                    if(Q2_y_Bin_Num == 2){
                        float z_Borders[7]  = {0.18, 0.23, 0.26, 0.31, 0.38, 0.50, 0.74};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 3:
                    if(Q2_y_Bin_Num == 3){
                        float z_Borders[6]  = {0.22, 0.28, 0.35, 0.45, 0.60, 0.78};
                        float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 4:
                    if(Q2_y_Bin_Num == 4){
                        float z_Borders[7]  = {0.26, 0.32, 0.37, 0.43, 0.50, 0.60, 0.71};
                        float pT_Borders[7] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 5:
                    if(Q2_y_Bin_Num == 5){
                        float z_Borders[7]  = {0.15, 0.19, 0.24, 0.29, 0.38, 0.50, 0.73};
                        float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 6:
                    if(Q2_y_Bin_Num == 6){
                        float z_Borders[6]  = {0.18, 0.23, 0.30, 0.39, 0.50, 0.78};
                        float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 7:
                    if(Q2_y_Bin_Num == 7){
                        float z_Borders[6]  = {0.21, 0.26, 0.30, 0.44, 0.55, 0.78};
                        float pT_Borders[7] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.65, 1.0};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 8:
                    if(Q2_y_Bin_Num == 8){
                        float z_Borders[7]  = {0.26, 0.32, 0.36, 0.40, 0.45, 0.53, 0.72};
                        float pT_Borders[6] = {0.05, 0.20, 0.30, 0.40, 0.52, 0.75};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 9:
                    if(Q2_y_Bin_Num == 9){
                        float z_Borders[7]  = {0.15, 0.20, 0.24, 0.30, 0.38, 0.48, 0.72};
                        float pT_Borders[7] = {0.05, 0.22, 0.30, 0.38, 0.46, 0.60, 0.95};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 10:
                    if(Q2_y_Bin_Num == 10){
                        float z_Borders[7]  = {0.18, 0.23, 0.26, 0.32, 0.40, 0.50, 0.72};
                        float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.00};

                        if(z_or_pT == 0){return z_Borders[6 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 11:
                    if(Q2_y_Bin_Num == 11){
                        float z_Borders[6]  = {0.21, 0.26, 0.32, 0.40, 0.50, 0.70};
                        float pT_Borders[7] = {0.05, 0.20, 0.31, 0.40, 0.50, 0.64, 0.95};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 12:
                    if(Q2_y_Bin_Num == 12){
                        float z_Borders[5]  = {0.26, 0.32, 0.40, 0.50, 0.70};
                        float pT_Borders[6] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.67};
                        
                        if(z_or_pT == 0){return z_Borders[4 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 13:
                    if(Q2_y_Bin_Num == 13){
                        float z_Borders[6]  = {0.15, 0.20, 0.24, 0.30, 0.40, 0.72};
                        float pT_Borders[6] = {0.05, 0.23, 0.34, 0.43, 0.55, 0.90};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 14:
                    if(Q2_y_Bin_Num == 14){
                        float z_Borders[6]  = {0.18, 0.23, 0.27, 0.33, 0.44, 0.74};
                        float pT_Borders[6] = {0.05, 0.23, 0.34, 0.44, 0.55, 0.90};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 15:
                    if(Q2_y_Bin_Num == 15){
                        float z_Borders[5]  = {0.21, 0.28, 0.35, 0.47, 0.72};
                        float pT_Borders[6] = {0.05, 0.23, 0.34, 0.45, 0.58, 0.90};

                        if(z_or_pT == 0){return z_Borders[4 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 16:
                    if(Q2_y_Bin_Num == 16){
                        float z_Borders[6]  = {0.15, 0.20, 0.25, 0.32, 0.41, 0.71};
                        float pT_Borders[5] = {0.05, 0.24, 0.36, 0.55, 0.80};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }
                    // For Q2-y Bin 17:
                    if(Q2_y_Bin_Num == 17){
                        float z_Borders[6]  = {0.18, 0.23, 0.30, 0.38, 0.48, 0.72};
                        float pT_Borders[5] = {0.05, 0.23, 0.36, 0.51, 0.85};

                        if(z_or_pT == 0){return z_Borders[5 - entry];}
                        if(z_or_pT == 1){return pT_Borders[entry];}
                    }

                    float empty = 0;
                    return empty;

                };

                /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////
                
                double z_event_val  = """, "smeared_vals[8]"  if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "z",  "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
                double pT_event_val = """, "smeared_vals[10]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "pT", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;

                int Q2_y_Bin_event_val = """, str(Q2_xB_Bin_event_name), """;
                int z_pT_Bin_event_val = 0;

                // Default:
                int Num_z_Borders  = 0;
                int Num_pT_Borders = 0;

                // Defining Borders for z and pT Bins (based on 'Q2_y_Bin')

                // For Q2_y Bin 0
                if(Q2_y_Bin_event_val == 0){
                    z_pT_Bin_event_val = 0;
                    return z_pT_Bin_event_val; // Cannot create z-pT Bins without propper Q2-y Bins
                }
                
                //==========================//
                //=====//   z Bins   //=====//
                //==========================//
                if(Q2_y_Bin_event_val == 2  || Q2_y_Bin_event_val == 4 || Q2_y_Bin_event_val == 5 || Q2_y_Bin_event_val == 8 || Q2_y_Bin_event_val == 9 || Q2_y_Bin_event_val == 10){
                    Num_z_Borders = 7;
                }
                if(Q2_y_Bin_event_val == 1  || Q2_y_Bin_event_val == 3 || Q2_y_Bin_event_val == 6 || Q2_y_Bin_event_val == 7 || Q2_y_Bin_event_val == 13 || Q2_y_Bin_event_val == 14 || Q2_y_Bin_event_val == 16 || Q2_y_Bin_event_val == 17 || Q2_y_Bin_event_val == 11){
                    Num_z_Borders = 6;
                }
                if(Q2_y_Bin_event_val == 12 || Q2_y_Bin_event_val == 15){
                    Num_z_Borders = 5;
                }
                //===========================//
                //=====//   pT Bins   //=====//
                //===========================//
                if(Q2_y_Bin_event_val == 1  || Q2_y_Bin_event_val == 2  || Q2_y_Bin_event_val == 3){
                    Num_pT_Borders = 8;
                }
                if(Q2_y_Bin_event_val == 4  || Q2_y_Bin_event_val == 5  || Q2_y_Bin_event_val == 6  || Q2_y_Bin_event_val == 7  || Q2_y_Bin_event_val == 9 || Q2_y_Bin_event_val == 10 || Q2_y_Bin_event_val == 11){
                    Num_pT_Borders = 7;
                }
                if(Q2_y_Bin_event_val == 8  || Q2_y_Bin_event_val == 12 || Q2_y_Bin_event_val == 13 || Q2_y_Bin_event_val == 14 || Q2_y_Bin_event_val == 15){
                    Num_pT_Borders = 6;
                }
                if(Q2_y_Bin_event_val == 16 || Q2_y_Bin_event_val == 17){
                    Num_pT_Borders = 5;
                }
                
                
                
                if(Q2_y_Bin_event_val == 0){
                    Num_z_Borders  = 1; Num_pT_Borders = 1;
                }
                if(Num_z_Borders == 0){
                    Num_z_Borders = 1; Num_pT_Borders = 1;
                }

                int z_pT_Bin_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                        // based on the number of times the loop has run

                // Determining z-pT Bins
                for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                    if(z_pT_Bin_event_val != 0){continue;     // If the bin has already been assigned, this line will end the loop.
                                                              // This is to make sure the loop does not run longer than what is necessary.
                    }
                    if(z_event_val > Borders_function(Q2_y_Bin_event_val, 0, zbin) && z_event_val < Borders_function(Q2_y_Bin_event_val, 0, zbin - 1)){
                        // Found the correct z bin
                        for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                            if(z_pT_Bin_event_val != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                            if(pT_event_val > Borders_function(Q2_y_Bin_event_val, 1, pTbin) && pT_event_val < Borders_function(Q2_y_Bin_event_val, 1, pTbin+1)){
                                // Found the correct pT bin
                                z_pT_Bin_event_val = z_pT_Bin_count; 
                                // The value of the z_pT_Bin has been set
                                return z_pT_Bin_event_val;
                            }
                            else{
                                z_pT_Bin_count = z_pT_Bin_count + 1; // Checking the next bin
                            }
                        }
                    }
                    else{
                        z_pT_Bin_count = z_pT_Bin_count + (Num_pT_Borders - 1);
                        // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                        // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                    }    
                }
                return z_pT_Bin_event_val;"""])


    
    
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        # Turns off the kinematic binning options by assigning every 'z_pT_Bin_event_val' to be 1 (should run faster when the kinematic binning is not necessary)
        if(Bin_Version in ["Off", "off"]):
            z_pT_Bin_Standard_Def = """
            int z_pT_Bin_event_val = 1;
            return z_pT_Bin_event_val;"""
            
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    #################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        return z_pT_Bin_Standard_Def
        
        
        
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    def Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type=""):
        # Only defined for the 'y_bin' binning option
        if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
            print("".join(["The input: ", color.RED, str(Variable_Type), color.END, " was not recognized by the function Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type='", str(Variable_Type), "').\nFix input to use anything other than the default calculations of the 4D kinematic bin."]))
            Variable_Type   = ""
        Q2_y_Bin_event_name = "".join(["Q2_y_Bin",       "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        z_pT_Bin_event_name = "".join(["z_pT_Bin_y_bin", "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
        
        Q2_y_z_pT_4D_Bin_Def = "".join(["""
        int Q2_y_Bin_event_val = """, str(Q2_y_Bin_event_name), """;
        int z_pT_Bin_event_val = """, str(z_pT_Bin_event_name), """;
        int Q2_y_z_pT_4D_Bin_event_val = 0;
        if(Q2_y_Bin_event_val > 1){
            Q2_y_z_pT_4D_Bin_event_val += 35;
        }
        if(Q2_y_Bin_event_val > 2){
            Q2_y_z_pT_4D_Bin_event_val += 42;
        }
        if(Q2_y_Bin_event_val > 3){
            Q2_y_z_pT_4D_Bin_event_val += 35;
        }
        if(Q2_y_Bin_event_val > 4){
            Q2_y_z_pT_4D_Bin_event_val += 36;
        }
        if(Q2_y_Bin_event_val > 5){
            Q2_y_z_pT_4D_Bin_event_val += 36;
        }
        if(Q2_y_Bin_event_val > 6){
            Q2_y_z_pT_4D_Bin_event_val += 30;
        }
        if(Q2_y_Bin_event_val > 7){
            Q2_y_z_pT_4D_Bin_event_val += 30;
        }
        if(Q2_y_Bin_event_val > 8){
            Q2_y_z_pT_4D_Bin_event_val += 30;
        }
        if(Q2_y_Bin_event_val > 9){
            Q2_y_z_pT_4D_Bin_event_val += 36;
        }
        if(Q2_y_Bin_event_val > 10){
            Q2_y_z_pT_4D_Bin_event_val += 36;
        }
        if(Q2_y_Bin_event_val > 11){
            Q2_y_z_pT_4D_Bin_event_val += 30;
        }
        if(Q2_y_Bin_event_val > 12){
            Q2_y_z_pT_4D_Bin_event_val += 20;
        }
        if(Q2_y_Bin_event_val > 13){
            Q2_y_z_pT_4D_Bin_event_val += 25;
        }
        if(Q2_y_Bin_event_val > 14){
            Q2_y_z_pT_4D_Bin_event_val += 25;
        }
        if(Q2_y_Bin_event_val > 15){
            Q2_y_z_pT_4D_Bin_event_val += 20;
        }
        if(Q2_y_Bin_event_val > 16){
            Q2_y_z_pT_4D_Bin_event_val += 20;
        }
        
        Q2_y_z_pT_4D_Bin_event_val += z_pT_Bin_event_val;
        
        if(Q2_y_Bin_event_val < 1 || z_pT_Bin_event_val < 1){
            Q2_y_z_pT_4D_Bin_event_val = 0;
        }
        
        return Q2_y_z_pT_4D_Bin_event_val;
        """])
    
        return Q2_y_z_pT_4D_Bin_Def
    

##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
        
    #############################################################################
    #####################      Matched Bin Definitions      #####################
    
    def Bin_Number_Variable_Function(DF, Variable, min_range, max_range, number_of_bins, DF_Type=datatype):
        # if("Q2_xB_Bin" in Variable or "z_pT_Bin" in Variable or "sec" in Variable or "Bin_4D" in Variable or "Bin_5D" in Variable):
        #     # Already defined
        #     return DF
        if((("Bin" in Variable) or ("sec" in Variable)) or (DF == "continue") or ("Combined_" in Variable or "Multi_Dim" in Variable)):
            # Already defined
            return DF
        else:
            GEN_Variable = "".join([Variable.replace("_smeared", ""), "_gen"])
            out_put_DF = DF
            bin_size = (max_range - min_range)/number_of_bins
            rec_bin = "".join(["""
            int rec_bin = ((""", str(Variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;
            if(""", str(Variable), """ < """, str(min_range), """){
                // Below binning range
                rec_bin = 0;
            }
            if(""", str(Variable), """ > """, str(max_range), """){
                // Above binning range
                rec_bin = """, str(number_of_bins + 1), """;
            }
            return rec_bin;"""])
            gen_bin = "".join(["""
            int gen_bin = ((""", str(GEN_Variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;
            if(""", str(GEN_Variable), """ < """, str(min_range), """){
                // Below binning range
                gen_bin = 0;
            }
            if(""", str(GEN_Variable), """ > """, str(max_range), """){
                // Above binning range
                gen_bin = """, str(number_of_bins + 1), """;
            }
            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                gen_bin = """, str(number_of_bins + 2), """;
            }
            return gen_bin;"""])
            out_put_DF = out_put_DF.Define(    "".join([str(Variable), "_REC_BIN"]), rec_bin)
            if(DF_Type not in ["rdf", "gdf"]):
                out_put_DF = out_put_DF.Define("".join([str(Variable), "_GEN_BIN"]), gen_bin)
        return out_put_DF

##########################################################################################################################################################################################
##########################################################################################################################################################################################


    def Multi_Dim_Bin_Def(DF, Variables_To_Combine, Smearing_Q="", Data_Type=datatype, return_option="DF"):
        if(DF == "continue"):
            return "continue"
        if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
            print("".join([color.Error, "ERROR IN Multi_Dim_Bin_Def...\nImproper information was provided to combine multidimensional bins\n", color.END_R, "Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'", color.END]))
            if(return_option == "DF"):
                return DF
            else:
                return Variables_To_Combine
        Vars_Data_Type_Output = [""] if((return_option != "DF_Res") or (Data_Type in ["rdf", "gdf"])) else ["" if("mear" not in Smearing_Q) else "_smeared", "_gen"]
        var_name, var_mins, var_maxs, var_bins = zip(*Variables_To_Combine)
        var_name, var_mins, var_maxs, var_bins = list(var_name), list(var_mins), list(var_maxs), list(var_bins)
        for list_invert in [var_name, var_mins, var_maxs, var_bins]:
            list_invert.reverse()
        Multi_Dim_Bin_Title, combined_bin_formula = {}, {}
        DF_Final = DF
        # print("var_name:", var_name, "\nvar_mins:", var_mins, "\nvar_maxs:", var_maxs, "\nvar_bins:", var_bins)
        for var_type in Vars_Data_Type_Output:
            Multi_Dim_Bin_Title[var_type] = "Multi_Dim"
            for ii, var in enumerate(var_name):
                # if(Smearing_Q != ""):
                #     if(("_smeared" not in str(var_name[ii])) and ("_gen" not in str(var_name[ii]))):
                #         var_name[ii] = "".join([str(var_name[ii]), "_smeared"])
                #     print("var_name[ii] =", var_name[ii])
                Multi_Dim_Bin_Title[var_type] += str("".join(["_", str(var).replace("_smeared", "")])).replace("_gen", "")
                if(var_type not in str(var)):
                    var_name[ii] = "".join([str(var), str(var_type)])
                if(var_type in [""]):
                    var_name[ii] = str((var).replace("_smeared", "")).replace("_gen", "")
                    # print(color.RED, "2) var_name[ii] =", var_name[ii], color.END)
                else:
                    var_name[ii] = str((var).replace("_smeared" if("gen" in str(var_type)) else "_gen", ""))
                    # print(color.RED, "3) var_name[ii] =", var_name[ii], color.END)
                    if(Smearing_Q != ""):
                        if(("_smeared" not in str(var_name[ii])) and ("_gen" not in str(var_name[ii]))):
                            var_name[ii] = "".join([str(var_name[ii]), "_smeared"])
                        # print("var_name[ii] =", var_name[ii])
                if(str(var_name[ii]) not in list(DF_Final.GetColumnNames()) and ((var_type in ["_smeared"]) or (Smearing_Q != ""))):
                    DF_Final = smear_frame_compatible(DF_Final, str(var_name[ii]), Smearing_Q)
                    if(DF_Final == "continue"):
                        return DF_Final
                    # print(color.BLUE, "\nvar_name[ii] =", var_name[ii], color.END)
                    # print("\nfor column_name in DF_Final.GetColumnNames():")
                    # for column_name in DF_Final.GetColumnNames():
                    #     print("\t", str(column_name))
                    # print("\n")
                elif((str(var_name[ii]) not in list(DF_Final.GetColumnNames())) and (str(var_name[ii]) not in DF_Final.GetColumnNames())):
                    print("".join([color.RED, "\nERROR IN 'Multi_Dim_Bin_Def': Variable '", str(var_name[ii]), "' is not in the DataFrame (check code for errors)", color.END]))
                    print("".join([color.RED, "Available Variables include:\n", str(DF_Final.GetColumnNames()), color.END]))
                    for column_name in DF_Final.GetColumnNames():
                        print("str(var_name[ii]) == str(column_name) --> ", (str(var_name[ii]) == str(column_name)), str(var_name[ii]) if(str(var_name[ii]) == str(column_name)) else "")

            Multi_Dim_Bin_Title[var_type] += str(var_type)
            combined_bin_formula[var_type] = "".join(["int combined_bin", str(var_type), " = "])

            for ii, var in enumerate(var_name):
                if(combined_bin_formula[var_type]  != "".join(["int combined_bin", str(var_type), " = "])):
                    combined_bin_formula[var_type] += " + "
                if("_Bin" not in str(var)):
                    norm_var = "int(((({0}{1} - {2})/({3} - {2}))*{4}))".format(var, var_type, var_mins[ii], var_maxs[ii], var_bins[ii])
                else:
                    norm_var = "".join([str(var), str(var_type)])
                var_bin_product = ""
                for jj in range(ii + 1, len(var_name)):
                    if(var_bins[jj] not in ["", 0]):
                        var_bin_product += "".join(["*", str(var_bins[jj])])
                combined_bin_formula[var_type] += "".join(["int({0}{1})"]).format(norm_var, var_bin_product)

            combined_bin_formula[var_type] += """ + 1;
            if("""
            for ii, var in enumerate(var_name):
                combined_bin_formula[var_type] += "".join([str(var), str(var_type), " < ", str(var_mins[ii]), " || ", str(var), str(var_type), " > ", str(var_maxs[ii])])
                if(ii != (len(var_name) - 1)):
                    combined_bin_formula[var_type] += " || "
            combined_bin_formula[var_type]     += "".join(["""){combined_bin""", str(var_type), """ = -1;}
            return combined_bin""", str(var_type), """;
            """])

            combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace(" +  + ", " + ")
            combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace("_smeared_gen",     "_gen")
            combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace("_smeared_smeared", "_smeared")

            # print(color.BOLD, "\n\ncombined_bin_formula[var_type] =\n\n", color.BLUE, combined_bin_formula[var_type], "\n\n", color.END)

            if(return_option == "DF"):
                try:
                    DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
                except:
                    print("".join([color.Error, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END_R, str(traceback.format_exc()), color.END, "\n\n"]))
            elif(return_option == "DF_Res"):
                try:
                    DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
                except:
                    print("".join([color.Error, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END_R, str(traceback.format_exc()), color.END, "\n\n"]))
            else:
                return [str(Multi_Dim_Bin_Title[var_type]), -1.5, (math.prod(var_bins)) + 1.5, (math.prod(var_bins)) + 3]
        return DF_Final


    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    ###################################################################################################################################################################
    ###################################################                 Done With Kinematic Binning                 ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################          Defining Helpful Functions for Histograms          ###################################################
    ###################################################################################################################################################################

##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    ###################=======================================###################
    ##===============##        Full Filter + Cut Title        ##===============##
    ###################=======================================###################
    
    def DF_Filter_Function_Full(DF, Variables, Titles_or_DF, Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type="rdf", Cut_Choice="no_cut", Smearing_Q="", Binning_Q="", Sec_type="", Sec_num=-1):
        # if("2" not in Binning_Q and "P2" in Cut_Choice):
        #     return "continue"
        # if('str' in str(type(Variables)) and Q2_xB_Bin_Filter != -1 and Variables != "2D_Purity"):
        #     return "continue"
        

        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##
        # No smearing frames which are not the Monte Carlo Reconstructed
        if(((Data_Type not in ["mdf", "pdf", "udf"]) and ("miss_idf" not in Data_Type)) and ("smear" in Smearing_Q)):
            return "continue"
        # No Cuts for Monte Carlo Generated events
        if((Data_Type in ["gdf", "gen"]) and (Cut_Choice not in ["no_cut", "cut_Gen", "cut_Exgen", "no_cut_eS1a", "no_cut_eS1o", "no_cut_eS2a", "no_cut_eS2o", "no_cut_eS3a", "no_cut_eS3o", "no_cut_eS4a", "no_cut_eS4o", "no_cut_eS5a", "no_cut_eS5o", "no_cut_eS6a", "no_cut_eS6o"])):
            return "continue"
        # No PID cuts except for matched MC events
        if((Data_Type not in ["pdf", "gen"]) and ("PID" in Cut_Choice)):
            return "continue"
        if((Titles_or_DF in ["DF"]) and (DF in ["continue"])):
            print(f"{color.Error}\nDataFrame given to DF_Filter_Function_Full() is '{DF}'\n{color.END}")
            return "continue"
        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##


        ##=======================================================##
        ##----------## Smeared Binning (MC REC Only) ##----------##
        ##=======================================================##
        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"
        if("2" in Binning_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])
        elif(Binning_Q not in [""]):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_", str(Binning_Q)]), "".join([z_pT_Bin_Filter_str, "_", str(Binning_Q)])
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type in ["mdf", "pdf", "udf"] or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])
        if(Data_Type == "gen"):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
        ##=======================================================##
        ##----------## Smeared Binning (MC REC->End) ##----------##
        ##=======================================================##


        ##==========================================================##
        ##----------## Kinematic Binning (Filter - str) ##----------##
        ##==========================================================##
        Filter_Name, Q2_xB_BinList_Name, z_pT_BinList_Name = "", "", ""

        if(Q2_xB_Bin_Filter == -3):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "Only Migration Bin Events",                                      "".join([str(Q2_xB_Bin_Filter_str), " > 17"]),                       -2
        if(Q2_xB_Bin_Filter == -2):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "Only Binned Events",                                             "".join([str(Q2_xB_Bin_Filter_str), " != 0"]),                       -1
        if(Q2_xB_Bin_Filter == -1):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "All Events",                                                     "",                                                                  -2
        if(Q2_xB_Bin_Filter == 0):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "None - Events without a bin",                                    "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)]), -2
        if(Q2_xB_Bin_Filter > 0):
            Q2_xB_BinList_Name, Filter_1 = "".join([variable_Title_name(Q2_xB_Bin_Filter_str), ": ", str(Q2_xB_Bin_Filter)]), "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)])

        if(z_pT_Bin_Filter  == -2): # This skips z-pT bins
            z_pT_BinList_Name, Filter_2 = "", ""
        if(z_pT_Bin_Filter  == -1):
            z_pT_BinList_Name, Filter_2 = "Only Binned Events",                                                               "".join([str(z_pT_Bin_Filter_str), " != 0"])
        if(z_pT_Bin_Filter  == 0):
            z_pT_BinList_Name, Filter_2 = "None - Events without a bin",                                                      "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])
        if(z_pT_Bin_Filter  > 0):
            z_pT_BinList_Name, Filter_2 = "".join([variable_Title_name(z_pT_Bin_Filter_str),   ": ", str(z_pT_Bin_Filter)]),  "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])
            
            
        if(Filter_2 != ""):
            Filter_Name = "".join([Filter_1, " && ", Filter_2])
        else:
            Filter_Name = Filter_1
        ##==========================================================##
        ##----------## Kinematic Binning (Filter - End) ##----------##
        ##==========================================================##


        ##===============================================##
        ##----------## Sector Filter (Start) ##----------##
        ##===============================================##
        if(Titles_or_DF == 'DF'):
            if(Filter_Name != ""):
                if(Sec_type != '' and Sec_num != -1):
                    Filter_Name = "".join([Filter_Name, " && ", str(Sec_type), " == ", str(Sec_num)])
            elif(Sec_type != '' and Sec_num != -1):
                Filter_Name = "".join([str(Sec_type), " == ", str(Sec_num)])
                
            if(Filter_Name != ""):
                print(Filter_Name)
                DF_Out = DF.Filter(Filter_Name)
            else:
                DF_Out = DF
            
            # if(Data_Type in ["mdf", "pdf"]):
            #     DF_Out = DF_Out.Filter("".join([str(str(z_pT_Bin_Filter_str).replace("_smeared", "")).replace("_gen", ""), "_gen != 1"]))
            # if(Data_Type in ["gdf"]):
            #     DF_Out = DF_Out.Filter("".join([str(str(z_pT_Bin_Filter_str).replace("_smeared", "")).replace("_gen", ""),     " != 1"]))
        else:
            particle_sector = ""
            if(Sec_type != '' and Sec_num != -1):
                if('esec' in Sec_type):
                    particle_sector = 'El'
                if('pipsec' in Sec_type):
                    particle_sector = 'Pi+'
                if('_a' in Sec_type):
                    particle_sector = ''.join([particle_sector, ' (Angle Def)'])

                Sector_Title_Name = ''.join([particle_sector, ' Sector ', str(Sec_num)])
            else:
                Sector_Title_Name = ''
        ##===============================================##
        ##----------##  Sector Filter (End)  ##----------##
        ##===============================================##

        
        ##################################################
        ##==========## General Cuts (Start) ##==========##
        ##################################################
        cutname = " "
        if((Data_Type in ["pdf", "gen"]) and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el != 0 && PID_pip != 0")

        if(Data_Type == "udf"            and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el == 0 || PID_pip == 0")

        if(Data_Type == "miss_idf"       and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && (PID_el != 11 || PID_pip != 211)")

        if(Data_Type == "miss_idf_el"    and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_el != 11")

        if(Data_Type == "miss_idf_pip"   and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_pip != 211")
            
        # if(Data_Type in ["gen", "mdf"]):
        #     DF_Out = DF_Out.Filter("sqrt(MM2_gen) > 1.5")
        
        if((Cut_Choice in ["cut_Gen"])         and (Data_Type not in ["rdf"])):
            cutname         = "Generated MM Cut"
            if(Titles_or_DF == 'DF'):
                if(Data_Type in ["gdf"]):
                    DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
                else:
                    DF_Out  = DF_Out.Filter("sqrt(MM2_gen) > 1.5")       
        elif((Cut_Choice in ["cut_Exgen"])     and (Data_Type not in ["rdf"])):
            cutname         = "Generated MM Cut (Exclusive Events)"
            if(Titles_or_DF == 'DF'):
                if(Data_Type in ["gdf"]):
                    DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
                else:
                    DF_Out  = DF_Out.Filter("sqrt(MM2_gen) < 1.5")
        elif((Data_Type not in ["gdf", "gen"]) and ("no_cut" not in str(Cut_Choice))):
            if("Complete"   in Cut_Choice):
                cutname     = "Complete Set of "
                if(("smear" in Smearing_Q)     and (Data_Type != "rdf")):
                    cutname = "".join([cutname, "(Smeared) "])
                if(Titles_or_DF == 'DF'):
                    if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                        #        DF_Out.Filter("              y < 0.75 &&               xF > 0 &&               W > 2 &&              Q2 > 2 &&              pip > 1.25 &&              pip < 5 && 5 < elth             &&             elth < 35 && 5 < pipth            &&            pipth < 35")
                        if("str" in str(type(DF_Out))):
                            print(f"DF_Out = {type(DF_Out)}({DF_Out})")
                        DF_Out  = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 2 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                        DF_Out  = filter_Valerii(DF_Out, Cut_Choice, Cut_Flag=True)
                        DF_Out  = New_Fiducial_Cuts_Function(Data_Frame_In=DF_Out, Skip_Options=Skipped_Fiducial_Cuts, Cut_Flag=True)
                    else:
                        DF_Out  = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 2 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                        DF_Out  = filter_Valerii(DF_Out, Cut_Choice)
                        DF_Out  = New_Fiducial_Cuts_Function(Data_Frame_In=DF_Out, Skip_Options=Skipped_Fiducial_Cuts, Cut_Flag=True)
                if("EDIS"   in Cut_Choice):
                    cutname = "".join([cutname, "Exclusive "])
                    if(Titles_or_DF == 'DF'):
                        DF_Out      = DF_Out.Filter(str(Calculated_Exclusive_Cuts(Smearing_Q)))
                if("SIDIS"  in Cut_Choice):
                    cutname = "".join([cutname, "SIDIS "])
                    if(Titles_or_DF == 'DF'):
                        if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                            DF_Out  = DF_Out.Filter("sqrt(smeared_vals[1]) > 1.5")
                        else:
                            DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
                if("Proton" in Cut_Choice):
                    cutname = f"{cutname} (Proton Cut) "
                    if(Titles_or_DF == 'DF'):
                        DF_Out  = DF_Out.Filter("MM_pro > 1.35")
                if("Binned"  in Cut_Choice):
                    cutname = "".join([cutname, "(Binned) "])
                    if(Titles_or_DF == 'DF'):
                        if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                            if("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list):
                                DF_Out = DF_Out.Filter("(Q2_Y_Bin_smeared > 0 && Q2_Y_Bin_smeared < 18) && (z_pT_Bin_Y_bin_smeared > 0)")
                            else:
                                DF_Out = DF_Out.Filter("(Q2_y_Bin_smeared > 0 && Q2_y_Bin_smeared < 18) && (z_pT_Bin_y_bin_smeared > 0)")
                        else:
                            if("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list):
                                DF_Out = DF_Out.Filter("(Q2_Y_Bin > 0 && Q2_Y_Bin < 18) && (z_pT_Bin_Y_bin > 0)")
                            else:
                                DF_Out = DF_Out.Filter("(Q2_y_Bin > 0 && Q2_y_Bin < 18) && (z_pT_Bin_y_bin > 0)")
                if("MM" in Cut_Choice):
                    cutname = "".join([cutname, "(Inverted MM) "])
                    if(Titles_or_DF == 'DF'):
                        if("smear" in Smearing_Q   and Data_Type != "rdf"):
                            DF_Out  = DF_Out.Filter("sqrt(smeared_vals[1]) < 1.5")
                        else:
                            DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
                if(("Gen" in Cut_Choice)           and (Data_Type not in ["rdf"])):
                    cutname = "".join([cutname, "(Gen MM) "])
                    if(Titles_or_DF == 'DF'):
                        if(Data_Type in ["gdf"]):
                            DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
                        else:
                            DF_Out  = DF_Out.Filter("sqrt(MM2_gen) > 1.5")
                if(("Exgen" in Cut_Choice)         and (Data_Type not in ["rdf"])):
                    cutname = "".join([cutname, "(Exclusive Gen MM) "])
                    if(Titles_or_DF == 'DF'):
                        if(Data_Type in ["gdf"]):
                            DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
                        else:
                            DF_Out  = DF_Out.Filter("sqrt(MM2_gen) < 1.5")
                cutname = "".join([cutname, "Cuts"])
                if(Skipped_Fiducial_Cuts != Default_Cut_Option):
                    cutname = "".join([cutname, f" (Skipped these Fiducial Cuts: {Skipped_Fiducial_Cuts})"])
        else:
            # Generated Monte Carlo should not have cuts applied to it
            cutname = "No Cuts"
        for sec in range(1, 7, 1):
            if("eS" not in Cut_Choice):
                break
            if("".join(["eS", str(sec), "a"]) in Cut_Choice):
                cutname = "".join([cutname, " (Excluding Sector ", str(sec), " Electrons)"])
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("".join(["esec != ", str(sec)]))
                    if(Data_Type in ["pdf", "gen"]):
                        DF_Out  = DF_Out.Filter("".join(["esec_gen != ", str(sec)]))
                break
            if("".join(["eS", str(sec), "o"]) in Cut_Choice):
                cutname = "".join([cutname, " (Sector ", str(sec), " Electrons Only)"])
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("".join(["esec == ", str(sec)]))
                    if(Data_Type in ["pdf", "gen"]):
                        DF_Out  = DF_Out.Filter("".join(["esec_gen == ", str(sec)]))
                break
        ##################################################
        ##==========##  General Cuts (End)  ##==========##
        ##################################################
        
        
        ##====================================================##
        ##----------## Smearing Variables (Start) ##----------##
        ##====================================================##
        if((Variables not in ["Cuts Only", "Cuts_Only", "Cuts"]) and ("Combined_" not in Variables and "Multi_Dim" not in Variables)):
            # If the above condition is FALSE, then the 'Variables' input does not specify a real variable that can be smeared or is already defined by another function (use to run this function for cuts only)
            # This information does not need to be run if titles are the only things of interest
            if((Data_Type in ["mdf", "pdf", "udf"] or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q and Titles_or_DF == 'DF'):
                if('str' in str(type(Variables))):
                    DF_Out = smear_frame_compatible(DF_Out, Variables, Smearing_Q)
                else:
                    for variable in Variables:
                        DF_Out = smear_frame_compatible(DF_Out, variable, Smearing_Q)
        ##====================================================##
        ##----------##  Smearing Variables (End)  ##----------##
        ##====================================================##


        ###########################################
        ##=======================================##
        ##==========## Final Outputs ##==========##
        ##=======================================##
        ###########################################

        ##==========## Cut Name ##==========##
        if(Titles_or_DF == 'Cut'):
            return cutname
        ##==========## Cut Name ##==========##

        ##==========## Data Frame Output ##==========##
        if(Titles_or_DF == 'DF'): 
            return DF_Out
        ##==========## Data Frame Output ##==========##

        ###########################################
        ##=======================================##
        ##==========## Final Outputs ##==========##
        ##=======================================##
        ###########################################

    ###################=======================================###################
    ##===============##     Full Filter + Cut Title (End)     ##===============##
    ###################=======================================###################
    
    
    ##################################################################################################################################################################
    ###################################################          Done Making the Functions for Histograms          ###################################################
    ###                                              ##------------------------------------------------------------##                                              ###
    ###----------------------------------------------##------------------------------------------------------------##----------------------------------------------###
    ###                                              ##------------------------------------------------------------##                                              ###
    ##################################################################################################################################################################
    ###################################################                    Choices For Graphing                    ###################################################
    ##################################################################################################################################################################    

    # if(run_Mom_Cor_Code == "yes"):
    #     print("".join([color.BBLUE, "\nRunning Histograms from Momentum Correction/Smearing Code (i.e., Missing Mass and ∆P Histograms)", color.END]))
    #     print("".join([color.RED,   "NOT Running Default SIDIS Histograms", color.END]))
    # else:
    #     print("".join([color.RED,   "\nNOT Running Momentum Correction/Smearing Histograms", color.END]))
    #     print("".join([color.BBLUE, "Running the Default Histograms for the SIDIS Analysis (i.e., Normal 1D/2D/3D Histograms and/or Unfolding Histograms)", color.END]))

    
    # # Cut Naming Conventions:
        # 1) 'no_cut' --> no new cuts are applied (only cuts are made during particle identification (PID))
        # 2) 'Mom' --> (See below)
          # 1.25 < pip < 5
          # 5 < elth < 35
          # 5 < pipth < 35"
        # 3) 'SIDIS' --> (See below)
          # y < 0.75
          # xF > 0
          # W > 2
          # Q2 > 1
        # 4) 'all' --> Combination of 'Mom', 'SIDIS', with an additional Missing Mass cut of: "MM > 1.5"
          # Do not combine with "Mom" or "SIDIS" separately as doing so will be meaningless (combination is already built in) 
        # 5) 'Valerii_Cut' --> Valerii's Fiducial cuts to remove bad detectors
        # 6) 'Q2'  -> New Q2 cut of "Q2 > 2"
        
    
    #####################       Cut Choices       #####################
    ###################################################################
    
    
    ###############################################################
    #####################     Bin Choices     #####################
    
    # For Q2_xB Bins:
            # A value of -2 --> Only Binned Events
            # A value of -1 --> All Events
            # A value of 0  --> Only Non-Binned Events (Events that do not correspond to a bin)
            
    # For z_pT Bins (relavent to later parts of the analysis):
            # A value of -2 --> Skip z-pT bins (This means that only the option for Q2-xB bins will matter for this value of z-pT)
            # A value of -1 --> Only Binned Events
            # A value of 0  --> Only Non-Binned Events (Events that do not correspond to a bin)

    # Q2_xB Bins have a maximum value of 10 (9 total bins)
    
    
    # The following list should include all the desired kinematic bins to be included.
    # # Only necessary for 3D->2D histograms (All binning is already built into the 3D->1D histograms)
    # # # z-pT bins are built into all 3D histograms that this code creates
    # If a Q2-xB bin is missing from this list, then that bin will be skipped when making the histograms
    
    # binning_option_list = ["", "2"]
    # binning_option_list = ["2"]
    # binning_option_list = ["2", "3"]
    # binning_option_list = ["Off"]
    # binning_option_list = ["Off", "y_bin"]
    # binning_option_list = ["y_bin"]
    binning_option_list = ["Y_bin"]

    # The options ''    or 'Stefan' uses the original binning scheme used by Stefan (may be outdated now based on the option selected)
    # The options '2'   or 'OG'     uses the modified binning schemes developed for this analysis (instead of the binning used by Stefan)
    # The options '3'   or 'Square' uses the modified square Q2-xB binning schemes developed later in this analysis
    # The options 'Off' or 'off'    uses no binning schemes and turns them off by setting their values to always be equal to '1' to improve the runtime when the bins are not needed
    
    
    # Conditions to make the 5D unfolding plots
    Use_5D_Response_Matrix = (any(option in binning_option_list for option in ["Y_bin", "Int_bin"])) and (run_Mom_Cor_Code != "yes")
    # Use_5D_Response_Matrix = False
    
    if(Use_5D_Response_Matrix):
        print(f"{color.BGREEN}\n\n{color.UNDERLINE}Will be making the plots needed for 5D Unfolding{color.END}\n\n")
    else:
        print(f"{color.BOLD}\n\nWill {color.RED}NOT{color.END_B} be making the plots needed for 5D Unfolding\n\n{color.END}")
        

        
    if(("Off" in binning_option_list or "off" in binning_option_list)  and ("Q2_xB_Bin_Off" not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_off"   not in list(rdf.GetColumnNames()))):
        print("Binning Scheme --> 'Off'")
        rdf = rdf.Define("Q2_xB_Bin_Off",                                           str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Off")))
        rdf = rdf.Define("z_pT_Bin_Off",                                            str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Off")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_Off_gen",                                   str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="Off")))
            rdf = rdf.Define("z_pT_Bin_Off_gen",                                    str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="Off")))
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_xB_Bin_Off_smeared",                           str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="Off")))
                rdf = rdf.Define("z_pT_Bin_Off_smeared",                            str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="Off")))
    if(("2" in binning_option_list or "OG" in binning_option_list)     and ("Q2_xB_Bin_2"   not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_OG"     not in list(rdf.GetColumnNames()))):
        print("Modified Binning Scheme --> '2'")
        rdf = rdf.Define("Q2_xB_Bin_2",                                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="2")))
        rdf = rdf.Define("z_pT_Bin_2",                                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="2")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_2_gen",                                     str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="2")))
            rdf = rdf.Define("z_pT_Bin_2_gen",                                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="2")))
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_xB_Bin_2_smeared",                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="2")))
                rdf = rdf.Define("z_pT_Bin_2_smeared",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="2")))
    if(("3" in binning_option_list or "Square" in binning_option_list) and ("Q2_xB_Bin_3"   not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_Square" not in list(rdf.GetColumnNames()))):
        print("New (rectangular) Binning Scheme --> '3'")
        rdf = rdf.Define("Q2_xB_Bin_3",                                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="3")))
        rdf = rdf.Define("z_pT_Bin_3",                                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="3")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_3_gen",                                     str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="3")))
            rdf = rdf.Define("z_pT_Bin_3_gen",                                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="3")))
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_xB_Bin_3_smeared",                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="3")))
                rdf = rdf.Define("z_pT_Bin_3_smeared",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="3")))
    if(("4" in binning_option_list or "y_bin"  in binning_option_list or "y_Bin" in binning_option_list) and ("Q2_y_Bin" not in list(rdf.GetColumnNames()))):
        print("Q2-y Binning Scheme (old) --> 'y_bin'")
        rdf = rdf.Define("Q2_y_Bin",                                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="y_bin")))
        rdf = rdf.Define("z_pT_Bin_y_bin",                                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="y_bin")))
        rdf = rdf.Define("Q2_y_z_pT_4D_Bin",                                        str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_y_Bin_gen",                                        str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="y_bin")))
            rdf = rdf.Define("z_pT_Bin_y_bin_gen",                                  str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="y_bin")))
            rdf = rdf.Define("Q2_y_z_pT_4D_Bin_gen",                                str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="gen")))
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_y_Bin_smeared",                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="y_bin")))
                rdf = rdf.Define("z_pT_Bin_y_bin_smeared",                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="y_bin")))
                rdf = rdf.Define("Q2_y_z_pT_4D_Bin_smeared",                        str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="smear")))
    if(("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list) and ("Q2_Y_Bin" not in list(rdf.GetColumnNames()))):
        print("New Q2-y Binning Scheme --> 'Y_bin'")
        rdf = rdf.Define("Q2_Y_Bin",                                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Y_bin")))
        rdf = rdf.Define("All_MultiDim_Y_bin",                                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Y_bin")))
        rdf = rdf.Define("z_pT_Bin_Y_bin",                                          "All_MultiDim_Y_bin[0]")
        rdf = rdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t",                           "All_MultiDim_Y_bin[1]")
        if(Use_5D_Response_Matrix):
            rdf = rdf.Define("MultiDim_Q2_y_z_pT_phi_h",                            "All_MultiDim_Y_bin[2]")
        # rdf = rdf.Define("MultiDim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t",                  "All_MultiDim_Y_bin[2]")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_Y_Bin_gen",                                        str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="Y_bin")))
            rdf = rdf.Define("All_MultiDim_Y_bin_gen",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="Y_bin")))
            rdf = rdf.Define("z_pT_Bin_Y_bin_gen",                                  "All_MultiDim_Y_bin_gen[0]")
            rdf = rdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_gen",                   "All_MultiDim_Y_bin_gen[1]")
            if(Use_5D_Response_Matrix):
                rdf = rdf.Define("MultiDim_Q2_y_z_pT_phi_h_gen",                    "All_MultiDim_Y_bin_gen[2]")
            # rdf = rdf.Define("MultiDim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t_gen",          "All_MultiDim_Y_bin_gen[2]")
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_Y_Bin_smeared",                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="Y_bin")))
                rdf = rdf.Define("All_MultiDim_Y_bin_smeared",                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="Y_bin")))
                rdf = rdf.Define("z_pT_Bin_Y_bin_smeared",                          "All_MultiDim_Y_bin_smeared[0]")
                rdf = rdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared",           "All_MultiDim_Y_bin_smeared[1]")
                if(Use_5D_Response_Matrix):
                    rdf = rdf.Define("MultiDim_Q2_y_z_pT_phi_h_smeared",            "All_MultiDim_Y_bin_smeared[2]")
                # rdf = rdf.Define("MultiDim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t_smeared",  "All_MultiDim_Y_bin_smeared[2]")
    if((any(options in binning_option_list for options in ["6", "Int_bin", "Int_Bin"])) and ("Q2_Y_Bin" not in list(rdf.GetColumnNames()))):
        print("New Q2-y Binning Scheme/Integrated z-pT bins --> 'Y_bin'/'Int_bin'")
        rdf = rdf.Define("Q2_Y_Bin",                                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Y_bin")))
        rdf = rdf.Define("All_MultiDim_Int_bin",                                    str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Int_bin")))
        rdf = rdf.Define("z_pT_Bin_Int_bin",                                        "All_MultiDim_Int_bin[0]")
        rdf = rdf.Define("MultiDim_z_pT_Bin_Int_bin_phi_t",                         "All_MultiDim_Int_bin[1]")
        if(Use_5D_Response_Matrix):
            rdf = rdf.Define("MultiDim_Int_Q2_y_z_pT_phi_h",                        "All_MultiDim_Int_bin[2]")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_Y_Bin_gen",                                        str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="Y_bin")))
            rdf = rdf.Define("All_MultiDim_Int_bin_gen",                            str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="Int_bin")))
            rdf = rdf.Define("z_pT_Bin_Int_bin_gen",                                "All_MultiDim_Int_bin_gen[0]")
            rdf = rdf.Define("MultiDim_z_pT_Bin_Int_bin_phi_t_gen",                 "All_MultiDim_Int_bin_gen[1]")
            if(Use_5D_Response_Matrix):
                rdf = rdf.Define("MultiDim_Int_Q2_y_z_pT_phi_h_gen",                "All_MultiDim_Int_bin_gen[2]")
            if(Run_With_Smear):
                rdf = rdf.Define("Q2_Y_Bin_smeared",                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="Y_bin")))
                rdf = rdf.Define("All_MultiDim_Int_bin_smeared",                    str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="Int_bin")))
                rdf = rdf.Define("z_pT_Bin_Int_bin_smeared",                        "All_MultiDim_Int_bin_smeared[0]")
                rdf = rdf.Define("MultiDim_z_pT_Bin_Int_bin_phi_t_smeared",         "All_MultiDim_Int_bin_smeared[1]")
                if(Use_5D_Response_Matrix):
                    rdf = rdf.Define("MultiDim_Int_Q2_y_z_pT_phi_h_smeared",        "All_MultiDim_Int_bin_smeared[2]")
            
            
    
    print("".join([color.BBLUE, "\nBinning Scheme(s) in use: ", color.END]))
    for binning in binning_option_list:
        print("".join(["\t(*) ", "Stefan's binning scheme" if(binning in ["", "Stefan"]) else "Modified binning scheme (developed from Stefan's version)" if(binning in ["2", "OG"]) else "New (rectangular) binning scheme" if(binning in ["3", "Square"]) else "New Q2-y binning scheme" if(binning in ["5", "Y_bin", "Y_Bin"]) else "New Q2-y/Integrated z-pT binning schemes" if(binning in ["6", "Int_bin", "Int_Bin"]) else "Q2-y binning scheme (main)" if(binning in ["4", "y_bin", "y_Bin"]) else "".join(["Binning Scheme - ", str(binning)])]))
    

    #####################     Bin Choices     #####################
    ###############################################################
    
    
    Q2_y_Binning = ['Q2_y_Bin', -0.5,  18.5, 19]
    # There are 17 Bins (extra bins are for overflow/empty space in histograms)
        
    # New as of 5/15/2024
    z_pT_phi_h_Binning = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5, 913.5, 915]
    # This is the exact binning used for 'Multi_Dim_z_pT_Bin_Y_bin_phi_t' (the variable created by a function calculation - predates the creation of this variable/the 5D unfolding variable)

    # New as of 5/7/2024
    Q2_y_z_pT_phi_h_5D_Binning = ['MultiDim_Q2_y_z_pT_phi_h', -0.5, 11814 + 1.5, 11814 + 2]
    # This is the combined Q2-y-z-pT-phi_h bin which is to be used with the 5D unfolding procedure (total bins = 11814 +2 for standard overflow on the plots)
        # This value is only an option if "Y_bin" in binning_option_list
    
    Sliced_5D_Increment = 422 # This is the number of bins that will be used in each slice of the 5D Response Matrix (used to more easily write this histogram to the output root file)
    if((Q2_y_z_pT_phi_h_5D_Binning[3]%Sliced_5D_Increment != 0) and Use_5D_Response_Matrix):
        print(f"{color.Error}Major Error: Improper number of slices for the bin count{color.END}\n\tNum_of_Bins%Sliced_5D_Increment = {Q2_y_z_pT_phi_h_5D_Binning[3]}%{Sliced_5D_Increment} = {Q2_y_z_pT_phi_h_5D_Binning[3]%Sliced_5D_Increment}")
        raise TypeError("Improper number of slices for the bin count")
    
    
    # smearing_options_list = ["", "smear"]
    smearing_options_list = ["smear"]
    # smearing_options_list = [""]
    
    
    if((run_Mom_Cor_Code not in ["no"]) and (datatype in ["mdf"])):
        # When running the momentum correction/smearing code, the smearing options list should include "smear"
        smearing_options_list = ["", "smear"]
        
    if((datatype in ["rdf", "gdf"]) or (not Run_With_Smear)):
        # Do not smear data or generated MC
        smearing_options_list = [""]
                
    if(Use_Pass_2 and ("smear" in smearing_options_list)):
        print(f"\n{color.BOLD}Using Pass 2 momentum smearing function\n{color.END}")
                
    if(("stop_over_smear" in smearing_function) and ("smear" in smearing_options_list)):
        print(f"{color.BGREEN}\nRunning New Smearing Funtion with extra criteria (SF = {smear_factor}){color.END}")
    elif(("ivec"          in smearing_function) and ("smear" in smearing_options_list)):
        print("".join([color.BBLUE, "\nRunning ", f"New Smearing Funtion (SF = {smear_factor})" if("Sigma Smearing Factor" in smearing_function) else "Modified Smearing Funtion" if("Simple Smearing Factor" not in smearing_function) else "".join(["Simple Smearing Factor (", str(smear_factor), ")"]), color.END]))
    elif("smear"          in smearing_options_list):
        print("".join([color.BBLUE, "\nRunning FX's Smearing Funtion", color.END]))
    else:
        print("".join([color.RED,   "\nNot Smearing...", color.END]))

    rdf     = rdf.Define("Complete_SIDIS_Cuts", "sqrt(MM2) > 1.5 && y < 0.75 && xF > 0 && W > 2 && Q2 > 2 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
    if(datatype not in ["gdf"]):
        rdf = filter_Valerii(rdf, "Complete",     Cut_Flag=True)
        rdf = New_Fiducial_Cuts_Function(Data_Frame_In=rdf, Skip_Options=Skipped_Fiducial_Cuts, Cut_Flag=True)
    if(("smear" in smearing_options_list) and (datatype not in ["rdf", "gdf"])):
        rdf = rdf.Define("Complete_SIDIS_Cuts_Smeared", "sqrt(smeared_vals[1]) > 1.5 && smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 2 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
        rdf = rdf.Define('MM_smeared',          'smeared_vals[0]')
        rdf = rdf.Define('MM2_smeared',         'smeared_vals[1]')
        rdf = rdf.Define('Q2_smeared',          'smeared_vals[2]')
        rdf = rdf.Define('xB_smeared',          'smeared_vals[3]')
        rdf = rdf.Define('v_smeared',           'smeared_vals[4]')
        rdf = rdf.Define('s_smeared',           'smeared_vals[5]')
        rdf = rdf.Define('W_smeared',           'smeared_vals[6]')
        rdf = rdf.Define('y_smeared',           'smeared_vals[7]')
        rdf = rdf.Define('z_smeared',           'smeared_vals[8]')
        rdf = rdf.Define('epsilon_smeared',     'smeared_vals[9]')
        rdf = rdf.Define('pT_smeared',          'smeared_vals[10]')
        rdf = rdf.Define('phi_t_smeared',       'smeared_vals[11]')
        rdf = rdf.Define('xF_smeared',          'smeared_vals[12]')
        rdf = rdf.Define('el_smeared',          'smeared_vals[15]')
        rdf = rdf.Define('el_E_smeared',        'smeared_vals[16]')
        rdf = rdf.Define('elth_smeared',        'smeared_vals[17]')
        rdf = rdf.Define('elPhi_smeared',       'smeared_vals[18]')
        rdf = rdf.Define('pip_smeared',         'smeared_vals[19]')
        rdf = rdf.Define('pip_E_smeared',       'smeared_vals[20]')
        rdf = rdf.Define('pipth_smeared',       'smeared_vals[21]')
        rdf = rdf.Define('pipPhi_smeared',      'smeared_vals[22]')
        # rdf = rdf.Define('Delta_Smear_El_P',    'smeared_vals[23]')
        # rdf = rdf.Define('Delta_Smear_El_Th',   'smeared_vals[24]')
        # rdf = rdf.Define('Delta_Smear_El_Phi',  'smeared_vals[25]')
        # rdf = rdf.Define('Delta_Smear_Pip_P',   'smeared_vals[26]')
        # rdf = rdf.Define('Delta_Smear_Pip_Th',  'smeared_vals[27]')
        # rdf = rdf.Define('Delta_Smear_Pip_Phi', 'smeared_vals[28]')

        
    if(output_all_histo_names_Q == "yes"):
        print(f"\n{color.BOLD}Print all (currently) defined content of the RDataFrame:{color.END}")
        for ii in range(0, len(rdf.GetColumnNames()), 1):
            name_of_variable = str((rdf.GetColumnNames())[ii])
            variables_type   = rdf.GetColumnType(rdf.GetColumnNames()[ii])
            print(f"\t{str(ii+1).rjust(3)}) {name_of_variable.ljust(40)} | (type -> {variables_type})")
        print(f"Total length= {str(len(rdf.GetColumnNames()))}\n\n")
    else:
        print(f"\n{color.BOLD}Current length of the RDataFrame is: {color.UNDERLINE}{str(len(rdf.GetColumnNames()))}{color.END}")
    
    
    ###########################################################
    #################     Final ROOT File     #################
    if((str(file_location) not in ['time', 'test']) and output_type in ["data", "tree"]):
        print(f"\n{color.BOLD}Taking Snapshot of the RDataFrame...{color.END}")
        rdf_entry_count = rdf.Count().GetValue()
        print(f"Number of entries in the RDataFrame: {rdf_entry_count}")
        rdf.Snapshot("h22", ROOT_File_Output_Name)
        print(f"{color.BGREEN}Final ROOT file has been created.{color.END}\n")
        
        if(output_all_histo_names_Q == "yes"):
            print(f"{color.BBLUE}Openning the newly created ROOT file to check its contents{color.END}")
            output_file_check = ROOT.TFile.Open(ROOT_File_Output_Name)
            # Access the TTree in the file
            tree_check = output_file_check.Get("h22")
            # Print the names of the branches in the TTree
            print(f"{color.BOLD}Branches in TTree 'h22':{color.END}")
            for ii, branch in enumerate(tree_check.GetListOfBranches()):
                print(f"\t{str(ii+1).rjust(3)}) {branch.GetName()}")
            # Close the file
            output_file_check.Close()
        
    else:
        print(f"\n{color.RED}Not saving ROOT file...{color.END}\n")
    #################     Final ROOT File     #################
    ###########################################################

    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
    # Getting current date
    datetime_object_end = datetime.now()

    endMin_full, endHr_full, endDay_full = datetime_object_end.minute, datetime_object_end.hour, datetime_object_end.day

    timeMin_end = "".join(["0", str(datetime_object_end.minute)]) if(datetime_object_end.minute < 10) else str(datetime_object_end.minute)
    
    # Printing current time
    if(datetime_object_end.hour > 12 and datetime_object_end.hour < 24):
        print("".join(["The time that this code finished is ", str((datetime_object_end.hour) - 12), ":", str(timeMin_end), " p.m."]))
    if(datetime_object_end.hour < 12 and datetime_object_end.hour > 0):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", str(timeMin_end), " a.m."]))
    if(datetime_object_end.hour == 12):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", str(timeMin_end), " p.m."]))
    if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
        print("".join(["The time that this code finished is 12:", str(timeMin_end), " a.m."]))
        
    Num_of_Days, Num_of_Hrs, Num_of_Mins = 0, 0, 0
    
    if(startDay_full > endDay_full):
        Num_of_Days = endDay_full + (30 - startDay_full)
    else:
        Num_of_Days = endDay_full - startDay_full
        
    if(startHr_full > endHr_full):
        Num_of_Hrs = endHr_full + (24 - startHr_full)
    else:
        Num_of_Hrs = endHr_full - startHr_full
        
    if(startMin_full > endMin_full):
        Num_of_Mins = endMin_full + (60 - startMin_full)
    else:
        Num_of_Mins = endMin_full - startMin_full
        
        
    if(Num_of_Hrs > 0 and startMin_full >= endMin_full):
        Num_of_Hrs += -1
        
    if(Num_of_Days > 0 and startHr_full >= endHr_full):
        Num_of_Days += -1
        
    print("\nThe total time the code took to run the given files is:")
    print("".join([str(Num_of_Days), " Day(s), ", str(Num_of_Hrs), " Hour(s), and ", str(Num_of_Mins), " Minute(s).\n\n\n"]))
    
    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
else:
    print("\nERROR: No valid datatype selected...\n")