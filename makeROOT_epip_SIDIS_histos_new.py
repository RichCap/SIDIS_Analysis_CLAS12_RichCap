# Most recent update notes:
# # All Updates have been moved to the github page/README.md file
# # This Code has been coverted such that 3D histograms are made instead of filtering Q2-xB/Q2-y/z-pT bins


##=================================================================================================================================================================##
##=================================================================================================================================================================##
##=================================================================================================================================================================##
import sys
from sys import argv
# Let there be 4 arguements in argv when running this code
# arguement 1: Name of this code (makeROOT_epip_SIDIS_histos_new.py)
# arguement 2: data-type
    # Options: 
    # 1) rdf --> Real Data
    # 2) mdf --> MC REC Data (Event matching is available)
    # 3) gdf --> MC GEN Data
    # 4) pdf --> Only Matched MC Events (REC events must be matched to their GEN counterparts if this option is selected)
    # Can add the contents of the following lists (SIDIS_Unfold_List, Momentum_Cor_List, Using_Weight_List, Smear_Factor_List, Pass_Version_List - see below) to control how the code is run.
        # 'SIDIS_Unfold_List' options will ensure the histograms used with unfolding are run
        # 'Momentum_Cor_List' options will ensure the options for (exclusive) momentum corrections/smearing are run
        # 'Using_Weight_List' options will run a variety of MC closure tests (including weighing histogram events)
        # 'Smear_Factor_List' options control which smear factor/function is used when smearing the MC (use when testing different options - default option is set within the code if not included in this arguement)
        # 'Pass_Version_List' options control which pass version of the data/MC is used when running the code (currently defaults to Pass 1)
# arguement 3: output type
    # Options: 
    # 1) histo --> root file contains the histograms made by this code
    # 2) data --> root file contains all information from the RDataFrame 
    # 3) tree --> root file contains all information from the RDataFrame (same as option 2)
    # 4) test --> sets arguement 4 to 'time' (does not save info - will test the DataFrame option instead of the histogram option - prints the names of all histograms that would be saved)
    # 5) time --> sets arguement 4 to 'time' (does not save info - will test the histogram option - same as not giving a 4th arguement)
# arguement 4: file number (full file location)

# NOTE: The 3rd arguement is not necessary if the option for "histo" is desired (i.e., code is backwards compatible and works with only 3 arguements if desired)

# EXAMPLE: python3 makeROOT_epip_SIDIS_histos_new.py mdf All

# To see how many histograms will be made without processing any files, let the last arguement given be 'time'
# i.e., run the command:
# # python3 makeROOT_epip_SIDIS_histos_new.py df time
# # # df above can be any of the data-type options given above

try:
    code_name, datatype, output_type, file_location = argv
except:
    try:
        code_name, datatype, output_type = argv
    except:
        print("Error in arguments.")
        
    
datatype, output_type = str(datatype), str(output_type)


# output_all_histo_names_Q = "yes"
output_all_histo_names_Q = "no"


# run_Mom_Cor_Code = "yes"
run_Mom_Cor_Code = "no"

smear_factor = "0.75"


Use_Pass_2 = False


# Use_Weight corresponses to weighing the MC events to add modulations to the generated simulated data (used as a closure test)
Use_Weight = False
# Use_Weight = True

SIDIS_Unfold_List = ["_SIDIS", "_sidis", "_unfold",  "_Unfold"]
Momentum_Cor_List = ["_Mom",   "_mom",   "_Cor",     "_cor"]
Using_Weight_List = ["_mod",   "_close", "_closure", "_weighed", "_use_weight", "_Q4"]
Smear_Factor_List = ["_0.5",   "_0.75",  "_0.7",     "_0.8",     "_0.9", "_1.0", "_1.2", "_1.5", "_2.0", "_FX"]
Pass_Version_List = ["_P2",    "_Pass2", "_P1",      "_Pass1"]

for sidis in SIDIS_Unfold_List:
    if(str(sidis) in str(datatype)):
        run_Mom_Cor_Code = "no"
        datatype         = str(datatype).replace(str(sidis), "")
        break
        
for mom_cor in Momentum_Cor_List:
    if(str(mom_cor) in str(datatype)):
        run_Mom_Cor_Code = "yes"
        datatype         = str(datatype).replace(str(mom_cor), "")
        break
        
for smear in Smear_Factor_List:
    if(str(smear) in str(datatype)):
        smear_factor     = str(smear).replace("_", "")
        datatype         = str(datatype).replace(str(smear), "")
        break
        
for weight_Q in Using_Weight_List:
    if(str(weight_Q) in str(datatype)):
        Use_Weight       = True
        if("_Q4"     in str(datatype)):
            Q4_Weight    = True
        else:
            Q4_Weight    = False
        datatype         = str(datatype).replace(str(weight_Q), "")
        break
        
        
if((run_Mom_Cor_Code in ["yes"]) or ("rdf" in str(datatype))):
    Use_Weight = False
    Q4_Weight  = False
    # Do not use the simulated modulations on the momentum correction code or for the experimental data set

for pass_ver in Pass_Version_List:
    if(str(pass_ver) in str(datatype)):
        if("2" in str(pass_ver)):
            Use_Pass_2 = True
        else:
            Use_Pass_2 = False
        datatype   = str(datatype).replace(str(pass_ver), "")
        break
    
del SIDIS_Unfold_List
del Momentum_Cor_List
del Using_Weight_List
del Pass_Version_List
del sidis
del mom_cor
del smear
del weight_Q
del pass_ver


if(output_type == "test"):
    output_all_histo_names_Q = "yes"
    print("Will be printing the histogram's IDs...")
    file_location   = "time"
    output_type     = "time"
elif(output_type   not in ["histo", "data", "tree"]):
    file_location   = output_type
    if(output_type not in ["test", "time"]):
        output_type = "histo"

print("".join(["Output type will be: ", output_type]))


# Option to turn on and off Momentum Corrections ('yes' will turn the corrections on)
Mom_Correction_Q = "yes"
# Mom_Correction_Q = "no"

if(datatype in ['gdf']):
    Mom_Correction_Q = "no"

# if(datatype not in ['rdf']):
#     Mom_Correction_Q = "no"


import ROOT 
import math
import array
from datetime import datetime
import copy
import traceback
import os

    
class color:
    CYAN      = '\033[96m'
    PURPLE    = '\033[95m'
    BLUE      = '\033[94m'
    YELLOW    = '\033[93m'
    GREEN     = '\033[92m'
    RED       = '\033[91m'
    DARKCYAN  = '\033[36m'
    BOLD      = '\033[1m'
    LIGHT     = '\033[2m'
    ITALIC    = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK     = '\033[5m'
    DELTA     = '\u0394' # symbol
    END       = '\033[0m'
    ERROR     = '\033[91m\033[1m' # Combines RED and BOLD
    Error     = '\033[91m\033[1m' # Same as ERROR
    
    
class color_bg:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'
    END     = '\033[0m'
    
    
class root_color:
    # Colors
    White   = 0
    Black   = 1
    Red     = 2
    Green   = 3
    Blue    = 4
    Yellow  = 5
    Pink    = 6
    Cyan    = 7
    DGreen  = 8 # Dark Green
    Purple  = 9
    DGrey   = 13
    Grey    = 15
    LGrey   = 17
    Brown   = 28
    Gold    = 41
    Rust    = 46
    
    # Fonts
    Bold    = '#font[22]'
    Italic  = '#font[12]'
    
    # Symbols
    Delta   = '#Delta'
    Phi     = '#phi'
    π       = '#pi'
    Degrees = '#circ'
    
    Line    = '#splitline'


if(str(file_location) == 'all'):
    print("\nRunning all files together...\n")
if(str(file_location) == 'time'):
    print("\nRunning Count. Not saving results...\n")
    

if(datatype in ['rdf', 'mdf', 'gdf', 'pdf']):
    file_num = str(file_location)
    if(datatype == "rdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00",              "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00",                                              "")).replace(".hipo.root", "")     
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_00",                                       "")).replace(".hipo.root", "")
    if(datatype in ["mdf", "pdf"]):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_",                                 "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-claspyth_",       "")).replace(".hipo.root", "")
    if(datatype == "gdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_",              "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_",                                              "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.inb-claspyth_",                                    "")).replace(".hipo.root", "")
    
    
    ########################################################################################################################################################################
    ##==================================================================##============================##==================================================================##
    ##===============##===============##===============##===============##     Loading Data Files     ##===============##===============##===============##===============##
    ##==================================================================##============================##==================================================================##
    ########################################################################################################################################################################
    
    
    if(datatype == 'rdf'):
        if(str(file_location) in ['all', 'All', 'time']):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*"              if(not Use_Pass_2) else "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_00*")
            files_used_for_data_frame = "Data_sidis_epip_richcap.inb.qa.skim4_00*"                  if(not Use_Pass_2) else "Data_sidis_epip_richcap.inb.qa.nSidis_00*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["Data_sidis_epip_richcap.inb.qa.skim4_00"          if(not Use_Pass_2) else "Data_sidis_epip_richcap.inb.qa.nSidis_00",            str(file_num), "*"])
            
    if(datatype in ['mdf', 'pdf']):
        if(str(file_location) in ['all', 'All', 'time']):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*" if(not Use_Pass_2) else "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-claspyth_*")
            files_used_for_data_frame = "MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*"          if(not Use_Pass_2) else "MC_Matching_sidis_epip_richcap.inb.qa.inb-claspyth_*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_"  if(not Use_Pass_2) else "MC_Matching_sidis_epip_richcap.inb.qa.inb-claspyth_", str(file_num), "*"])
            
    if(datatype == 'gdf'):
        if(str(file_location) in ['all', 'All', 'time']):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*"              if(not Use_Pass_2) else "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.inb-claspyth_*")
            files_used_for_data_frame = "MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*"               if(not Use_Pass_2) else "MC_Gen_sidis_epip_richcap.inb.qa.inb-claspyth_*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_"       if(not Use_Pass_2) else "MC_Gen_sidis_epip_richcap.inb.qa.inb-claspyth_",      str(file_num), "*"])
            
            
    print("".join(["\nLoading File(s): ", str(files_used_for_data_frame)]))
    
    
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

#     # # # See File_Name_Updates.md file for notes on versions older than "New_Binning_Schemes_V6_"
    
#     Extra_Name = "New_Binning_Schemes_V6_"
#     * Switched to the new Q2-y binning but switched the names so that the Q2-y binning scheme used in the last version of this code is now referred to by "Y_bin" while the new binning scheme uses 'y_bin' (will make updating the other files easier)
#     * Removed the MM and W to the 1D histogram options (no longer running)
#     * Smearing is still turned off (not needed at this time)
#     * Fixed the issue with the 'Multi_Dim' variables' code (was not using the generated information propperly)

#     Extra_Name = "New_Binning_Schemes_V7_"
#     * Added the z-pT bins for the new y-binning scheme
#     * Smearing is still turned off (not needed at this time)
#     * Fixed issues with the 'Multi_Dim' binning function (should work correctly now)
#     * Added new 2D plots for W vs Q2/y and xB vs y (three new plots)
#         * Added later (ran a second time without renaming on 6-12-2023) 

#     Extra_Name = "New_Binning_Schemes_V8_"
#     * Added a 5D response matrix by defining a new 4D Bin variable based on the Q2-xB-z-pT bins
#         * The 4D variable has a total of 566 bins while the 5D Response Matrix only uses 12 bins for the phi_t variable to limit the memory consumption of creating a histogram with more than 12000 bins (with only 12 phi_t bins, the 5D response matrix should have about 6792 bins)
#         * Needed to be fixed after starting to run - the 'Multi_Dim' response matrices no longer use 3D histograms to slice with the z-pT bins
#     * Smearing is still turned off (not needed at this time)
    
    
    Extra_Name = "Gen_Cuts_V1_"
    # * Added new Missing Mass Cut to the generated events (to both 'gdf' and 'gen' - i.e., all matched/unmatched generated events are cut)
    #     * First test of the generated missing mass cut
    #     * The Missing Mass Cut starts at 1.5 GeV (just like the normal cut to the reconstructed events)
    # * Smearing function was modified with a new smearing factor (and slightly modified function)
    # * Modified the 5D histogram to use 24 phi_t bins again instead of 12
    # * Removed the 2D plots for W vs Q2/y and xB vs y (three of the 2D plots)
    
    
    Extra_Name = "Gen_Cuts_V2_"
    # Turned off Generated Missing Mass Cut
    # Otherwise is the same as "Gen_Cuts_V1_"
    
    Extra_Name = "Gen_Cuts_V3_"
    # Generated Cut is not turned on
    # Added the Missing Mass unfolding histogram
    # Modified the number of bins used to plot the 2D z vs pT histograms (did not change the binning scheme itself yet)
    
    Extra_Name = "Gen_Cuts_V3_Mom_Cor_"
    # Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
        # Starting to add the new z-pT bins but not fully updated yet
    # Using smear_factor = 0.8
    # Still using the same MC Momentum Corrections from Unsmeared distribution
    
    Extra_Name = "Gen_Cuts_V3_Mom_Cor_V2_"
    # Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
        # Added the new z-pT bins but not fully tested yet
    # Using smear_factor = 0.75
    
    
    Extra_Name = "Gen_Cuts_V3_Mom_Cor_V3_"
    # Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
    # Using smear_factor = 0.5
    

    Extra_Name = "Gen_Cuts_V3_Mom_Cor_V4_"
    # Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
    # Using smear_factor = 1.0
    
    Extra_Name = "Gen_Cuts_V3_Mom_Cor_FX_"
    # Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
        # Using FX's smearing function
    
    
    Extra_Name = "Gen_Cuts_V4_"
    # Running with new z-pT bins for the Q2-y-z-pT scheme
        # Using fewer bins in some, but not all, cases
        # Data distribution in each bin should be improved (i.e., more evenly distributed)
    # Using fewer phi_h bins for the 5D Response Matrix
        # Current number of bins are as follows:
            # 512 Q2-y-z-pT bins
            # 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
            # TOTAL: 5120 bins
    # Using smear_factor = 0.75
    # No Generated Missing Mass Cuts at this time
    # Turned off MC Momentum Corrections
    
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "Gen_Cuts_V4_Mom_Cor_V1_"
        # Same as 'Gen_Cuts_V4_' but running the momentum correction histograms instead
        # Using smear_factor = 0.75
        # No Generated Missing Mass Cuts at this time
        # Turned off MC Momentum Corrections
        
        Extra_Name = "Gen_Cuts_V4_Mom_Cor_V2_"
        # Same as 'Gen_Cuts_V4_Mom_Cor_V1_' but with a new smear_factor
        # Using smear_factor = 0.5
        
        Extra_Name = "Gen_Cuts_V4_Mom_Cor_V3_"
        # Same as 'Gen_Cuts_V4_Mom_Cor_V2_' but with a new smear_factor
        # Using smear_factor = 1.0
        
        Extra_Name = "Gen_Cuts_V4_Mom_Cor_FX_"
        # Same as 'Gen_Cuts_V4_Mom_Cor_V3_' but with FX's smearing function

        
    Extra_Name = "Gen_Cuts_V5_"
    # Same as 'Gen_Cuts_V4_' except the MC Momentum Corrections are turn back on and a few errors in the Kinematic binning definitions
        # The momentum corrections, upon review, did not need to be turned off/updated (turning the corrections off was done because I forgot that I previously updated them from an inferior version)
        # One binning error was caused by a single missing bin that would throw off the binning scheme used to define the 4D bin variable (it only went up to 512 bins when it should have been 513)
        # Another binning error was with the Q2-y bin number 11 which had a few mistakenly defined z-pT bins (the number of bins was off and some improvements to how they were distributed were possible)
        # NEW number of Q2-y-z-pT bins is 506 (due to the correction of Q2-y bin 11)
            # Using fewer phi_h bins for the 5D Response Matrix
                # Current number of bins are as follows:
                    # 506 Q2-y-z-pT bins
                    # 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
                    # TOTAL: 5060 bins
    # Using smear_factor = 0.75
    
    
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "Gen_Cuts_V5_Mom_Cor_V1_"
        # Same as 'Gen_Cuts_V5_' but running the momentum correction histograms instead and ONLY SMEARING THE PARTICLE'S MOMENTUMS
            # The particle's angles are not being smeared
        # Using smear_factor = 0.75
        # No Generated Missing Mass Cuts at this time
        # MC Momentum Corrections are ON
        
        if(smear_factor == "0.5"):
            Extra_Name = "Gen_Cuts_V5_Mom_Cor_V2_"
            # Same as 'Gen_Cuts_V5_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.5
        
        if(smear_factor == "1.0"):
            Extra_Name = "Gen_Cuts_V5_Mom_Cor_V3_"
            # Same as 'Gen_Cuts_V5_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.0
        
        
    Extra_Name = "Gen_Cuts_V5_No_Cor_"
    # Same as 'Gen_Cuts_V5_' except the MC Momentum Corrections are turn back off due to issues recognized in their development
        # Plotting Dp vs p_corrected causes issues in creating the iterative corrections which exists in this code while not existing in the prior Momentum Correction Development code that this procedure is based on
    # Using smear_factor = 0.75
        # The particle's angles are NOT being smeared
    # MC Momentum Corrections are OFF
    
    
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V1_"
        # Same as 'Gen_Cuts_V5_No_Cor_' but running the momentum correction histograms instead
            # The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
        # Using smear_factor = 0.75
            # The particle's angles are NOT being smeared
        # MC Momentum Corrections are OFF
        
        if(smear_factor == "0.5"):
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V2_"
            # Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.5
        
        if(smear_factor == "1.0"):
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V3_"
            # Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.0
            
        if(smear_factor == "FX"):
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_FX_"
            # Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with FX's smearing function
            
        if(smear_factor == "0.7"):
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V4_"
            # Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.7
            
        if(smear_factor == "1.5"):
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V5_"
            # Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.5
            
        if(datatype == 'rdf'):        
            Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_"
            # Same as 'Gen_Cuts_V5_No_Cor_' but running the momentum correction histograms instead
            # This one is for the Experimental Data (without momentum corrections)
            
            
        
    Extra_Name = "Gen_Cuts_V6_"
    # The MC Momentum Corrections are turn back ON after testing their new versions
        # Only 1 iteration of the correction per particle
    # Using smear_factor = 0.75
        # The particle's angles are NOT being smeared
    # Not making the 5D-Unfolding Histograms
        # Instead, making new 3D-Unfolding Histograms which unfold z+pT+phi_h together for each Q2-y Bin
    # Made some other minor changes (not present in "Gen_Cuts_V6_Mom_Cor_V*" - but should not affect the results)
    
    
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "Gen_Cuts_V6_Mom_Cor_V1_"
        # Same as 'Gen_Cuts_V6_' but running the momentum correction histograms instead
            # The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
        # Using smear_factor = 0.75
            # The particle's angles are NOT being smeared
        # MC Momentum Corrections are ON
        
        if(smear_factor == "0.5"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V2_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.5
        
        if(smear_factor == "1.0"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V3_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.0
            
        if(smear_factor == "FX"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_FX_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with FX's smearing function
            
        if(smear_factor == "0.7"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V4_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.7
            
        if(smear_factor == "1.5"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V5_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.5
            
        if(smear_factor == "0.9"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V6_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.9
            
        if(smear_factor == "0.8"):
            Extra_Name = "Gen_Cuts_V6_Mom_Cor_V7_"
            # Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.8
            
            

    Extra_Name = "Gen_Cuts_V7_"
    # Was the same as "Gen_Cuts_V6_" when started running "SF_Testing_Mom_Cor_V1_" but updated later with new simulated phi_t modulations and MM_gen cuts
    # Added the Missing_Mass_Cut_Gen variable which has a value of -1 if the generated missing mass is below 1.5 GeV. Otherwise, it has a value of 1
        # This does not effect the experimental data histograms
        # These cuts are not available on the mdf 1D phi_h unfolding response matrices as they lack the extra available dimension to make use of the variable
            # Use the multidimensional unfolding plots instead
    # Added Modulations to the Monte Carlo phi_h distributions (effects generated and reconstructed distributions when turned on)
        # This closure test can be turned from the commandline by including "_mod" in the datatype input
        # Modulations are made by weighing the events based on calculations done with the generated phi_h value (using the same function phi_h will be ultimately fitted with)
            # Modulation parameters for this run are:
                # Par_B = -0.050
                # Par_C =  0.025
        # Modulations are applied to all response matrix plots and the 2D histograms
        # Modulations are not allowed as options when running code with the experimental data or for the momentum correction plots (no indication will be given in these cases, but for the other relevant cases, the code will print whether the closure test is being used)
    # Using smear_factor = 0.75
        
            
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "SF_Testing_Mom_Cor_V1_"
        # Same as 'Gen_Cuts_V7_'/'Gen_Cuts_V6_' but running the momentum correction histograms instead
            # The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
        # Using smear_factor = 0.75
            # The particle's angles are NOT being smeared
        # MC Momentum Corrections are ON
        # Added MM and Dp vs local phi plots
        
        if(smear_factor == "0.5"):
            Extra_Name = "SF_Testing_Mom_Cor_V2_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.5
        
        if(smear_factor == "1.0"):
            Extra_Name = "SF_Testing_Mom_Cor_V3_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.0
            
        if(smear_factor == "FX"):
            Extra_Name = "SF_Testing_Mom_Cor_FX_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with FX's smearing function
            
        if(smear_factor == "0.7"):
            Extra_Name = "SF_Testing_Mom_Cor_V4_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.7
            
        if(smear_factor == "1.5"):
            Extra_Name = "SF_Testing_Mom_Cor_V5_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.5
            
        if(smear_factor == "0.9"):
            Extra_Name = "SF_Testing_Mom_Cor_V6_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.9
            
        if(smear_factor == "0.8"):
            Extra_Name = "SF_Testing_Mom_Cor_V7_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 0.8
            
        if(smear_factor == "1.2"):
            Extra_Name = "SF_Testing_Mom_Cor_V8_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 1.2
            
        if(smear_factor == "2.0"):
            Extra_Name = "SF_Testing_Mom_Cor_V9_"
            # Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
            # Using smear_factor = 2.0
            
        if(datatype == "rdf"):
            Extra_Name = "SF_Testing_Mom_Cor_"
            # Same as "SF_Testing_Mom_Cor_V1" but the extra version number is not needed due to the fact that the data is never smeared
            
            
        if(Mom_Correction_Q == "no"):
            # Not using the Momentum Corrections
            Extra_Name = "".join([Extra_Name, "No_Cor_"])
            
            
    Extra_Name = "Gen_Cuts_V8_"
    # Increased the modulations to the Monte Carlo phi_h distributions (increased Par_B by a factor of 10)
        # See 'Gen_Cuts_V7_' for first update
            # Modulation parameters for this run are:
                # Par_B = -0.500
                # Par_C =  0.025
        # Modulations are applied to all response matrix plots and the 2D histograms
        # Modulations are NOT allowed as options when running code with the experimental data or for the momentum correction plots
    # Tried to fix the 'Missing_Mass_Cut_Gen' variable (see See 'Gen_Cuts_V7_' for first update)
        # Now split the 'Gen_MM_Cut' into separate histograms from improved usage
            # A potential error occurred with a difference in the number of events in the 1D simulated unfolding closure tests and the 3D simulated unfolding closure tests
                # Possible cause may have been the lack of the 'Missing_Mass_Cut_Gen' variable in the 1D response matrices
            # The histograms which included 'Missing_Mass_Cut_Gen' in 'Gen_Cuts_V7_' are now split into two separate sets of histograms - one having the 'Missing_Mass_Cut_Gen' variable on an extra axis to be projected later and one that is the same as prior versions of the histogram (i.e., does not include 'Gen_MM_Cut')
            # The 1D Response matrices which did not include 'Missing_Mass_Cut_Gen' in the last update are now split into 3 histograms:
                # The 1st one is the same as before (i.e., no reference to 'Missing_Mass_Cut_Gen')
                # The 2nd one includes just the events that would be EXCLUDED by the Generated Missing Mass Cut (i.e., Missing_Mass_Cut_Gen < 0)
                    # Histogram name includes "Gen_Cut_MM" to pick it out from the other histograms
                # The 3rd one applies the Generated Missing Mass Cut as to only keep the events which survive the cut (i.e., Missing_Mass_Cut_Gen > 0)
                    # Histogram name includes "Gen_MM_Cut" to pick it out from the other histograms
                    # This name is identical to the part of the names of the other histograms which include 'Missing_Mass_Cut_Gen' as a plotted variable
    # Removed the Missing Mass 1D histograms and the 2D MM vs W histograms to reduce the number of histograms being created
        # These histograms were not in regular use at this time
    # Added new Multi_Dim histograms for the purpose of checking the phi_t distribution's dependence on the particles' lab angles
        # Wanted to study possible correlations between these angles and the additional modulations noticed in the phi_t distributions
        # Added elth, pipth, elPhi, and pipPhi
    # Attempted to fix parts of the histogram titles
        # Note: Do not use functions like SetTitle() in this code as they cause it to run much slower (not optimal for testing - likely would require the same amount of time to test as it would take to fully run the code to produce the root files)
    # Slightly modified how the response matrix histograms are saved to be slightly more compact (given that the additional histograms would make it even more difficult to save each one properly)
    # Using smear_factor = 0.75
    # Momentum Corrections are applied
    # Extending the 2D z vs pT plot ranges (not changing bin size)
        # Should be a visual change only - though the even number of bins should help slightly when rebinning during the kinematic comparisons (will avoid error messages)
    # Had to run twice due to a typo that deleted some important histograms
        
        
        
    Extra_Name = "New_Bin_Tests_V1_"
    # Ran on 9/27/2023
    # This file serves only to test new Q2-y Bins (and eventually new z-pT bins as well)
        # The response matrices needed for unfolding are not being run
        # Momentum smearing has also been turned off
    # Running new 3D histograms to plot each particle's kinematics versus the phi_h angle
        # The 3 3D histograms being run are grouped such that a single kinematic variable (i.e., p, theta, phi) for both the electron and pion is plotted vs eachother and phi_h
    # Made new 2D histogram dimensions for the Q2 vs y and z vs pT plots
        # The plots will include extended ranges for better coverage of the generated distributions and more refined binning
            # The y, z, and pT bins all have a width now of 0.01/bin while Q2 now has a bin width of 0.05/bin
    # Added new cut for inverting the MM cut (to see where events removed by this cut are comming from)
    
    
    Extra_Name = "New_Bin_Tests_V2_"
    # Ran on 10/3/2023
    # This file uses the original Q2-y binning scheme ('y_bin')
        # Testing of the newer scheme still ongoing
        # Still not smearing
    # No response matrices will be run
    # Only making 2D Histograms
        # Including new histograms for the lab phi angles vs phi_t
        # Not making any 3D or 1D histograms
    # New Cuts have been introduced (just cutting on generated missing mass)
        # Adding '_Gen' to the cut name makes the normal SIDIS missing mass cut on the generated events
        # Adding '_Exgen' to the cut name inverts the normal SIDIS missing mass cut on the generated events (i.e., sqrt(MM2_gen) < 1.5)
    
    Extra_Name = "New_Bin_Tests_V3_"
    # Ran on 10/4/2023
    # This file is mostly the same as "New_Bin_Tests_V2_" but returned to using the new Q2-y bins (for testing 'Y_bins')
        # Still not smearing
        # Added the generated missing mass cuts on MM_gen < 1.5
            # Is in addition to the inverted versions of these cuts that were run in "New_Bin_Tests_V2_"
    # Fixed minor issue with Q2_y_Bin = -3 (migration only)
        # Cut was not applied propperly
        
        
    Extra_Name = "New_Bin_Tests_V4_"
    # Ran on 10/11/2023
    # This file uses the original Q2-y binning scheme ('y_bin')
        # Still not smearing
    # This file is mainly used to study the additional phi_t modulations
        # More 2D Histograms of variables vs phi_t have been made including:
            # Electron/Pi+ Sectors (esec/pipsec)
            # Polar angles Theta of both particles
            # Momentum of both particles

            
            
    Extra_Name = "MultiDim_Bin_Test_V1_"
    # Ran on 11/1/2023-11/2/2023
    # This file uses the original Q2-y binning scheme ('y_bin')
        # Still not smearing
    # This file is mainly used to study the Multi-Dimensional phi_t histograms to ensure the 1st z-pT bin is constructed correctly for 3D unfolding
        # Turned Response Matrices back on
        # Turned off options from Extra_Name = "New_Bin_Tests_V4_"
        # Added cut on the generated events in z-pT bin 1 (applied to all Q2-y bins)
            # Cut is (basically) rdf = rdf.Filter("z_pT_bin_gen != 1")
                # See line 5991 (as of this note)
                # Cut may be inverted in a later test (ignore this note if this test idea proves to be unnecessary)
                # This cut should remove a single column from the flattened 3D response matrix
        # Removed all extra (generated missing mass) cuts used in prior tests (don't need them for this test)
        # Turned off all 2D histograms
        
        
    Extra_Name = "Sec_Cut_Test_V2_"
    # Ran on 11/21/2023
    # This file uses the original Q2-y binning scheme ('y_bin')
        # Still not smearing
        # Running with momentum corrections
    # Added a new alert to notify the user of the complete set of Response Matricies that are to be made when the code is run
        # Also added an optimizations condition which turns off the Response Matrix code automatically if List_of_Quantities_1D = [] (i.e., if the 1D histogram option is turned off)
        # See 'Alert_of_Response_Matricies'
    # This file is mainly used to study the additional phi_t modulations
        # Made as an extention of Extra_Name = "New_Bin_Tests_V4_"
            # Removed the cut added in Extra_Name = "MultiDim_Bin_Test_V1_" (was on line 5991 in the last note)
                # This cut is now on line 6025 as of this note, and can be found by searching for the following line of code:
                    # DF_Out = DF_Out.Filter("".join([str(str(z_pT_Bin_Filter_str).replace("_smeared", "")).replace("_gen", ""), "_gen != 1"]))
        # Added new set of cuts which cut on the electron sectors (to test the relationship between different sectors)
            # Investigation aims to see if the behavior of the modulations with respect to the pion sector changes when restricting the electron to specific sectors
            # Cuts on the electron sector are applied to both the generated AND reconstructed tracks simultaneously
            # Two versions of this cut are run alongside the typical analysis cuts used in this code:
                # 1) Cut 'eS1a' excludes events where the electron was detected in sector 1 of the detector (keeps all other events where the electron was detected in any other sector)
                # 2) Cut 'eS1o' requires all electrons to have been detected in sector 1 (opposite cut as 'eS1a')
                # These cuts can be added to any existing cut to be applied in addition to them
                    # Started to remove some other outdated code that was meant to perform this same type of cut
                # Cut Naming convension is: 
                    # 1st letter corresponds to the particle being cut (i.e.,'e' -> electron)
                    # 2nd letter is 'S' to signify that it is a Sector cut
                    # 3rd character/1st number corresponse to which sector is to be cut (i.e., '1' -> cut on sector 1)
                    # Last letter is either 'a' for 'all sectors' (just excludes the sector given in the cut's name) or 'o' for 'only' (removes all sectors not given in the cut's name)
                    # # Naming convension is not (currently) modular, so adding additional cuts of this nature will require them to be manually added
        # Set of 2D Histograms of variables vs phi_t in this file include:
            # Electron/Pi+ Sectors (esec/pipsec)
            # Lab Azimuthal angles (Phi) of both particles
            # Polar angles (Theta) of both particles
            # Momentum of both particles
        # Not running any 1D or 3D histogram options
    ## ERROR NOTED ON 12/5/2023: Definitions of 'eS1a' and 'eS1o' were switched (cuts do not match their definitions above - corrected after the code was run)

    
    Extra_Name = "Sec_Cut_Test_V2_"
    # Ran on ...
    # This file uses the original Q2-y binning scheme ('y_bin')
        # Smearing option is still turned off (reset after running Extra_Name = "New_Smearing_V1_" - see below)
        # Running with momentum corrections
        # Reduced the bin options to just run the plots for all Q2-y bins and for Q2-y bin 3 (done to reduce the number of plots to be made due to the greater number of cuts being applied)
    # Added ability to weigh events based on the (generated) Q^4 value (for testing the extra modulations) - See below for when it is used
    # Still making the set of histograms used in "Sec_Cut_Test_V1_" to test the dependence of other variables with the extra modulations in phi_t
        # Error in how sectors are handled has caused these histograms to be skipped when plotting the sector vs the SMEARED phi_t angle (error only affects the smeared plots)
    # Added the ability to make other electron sector cuts like those that where introduced in "Sec_Cut_Test_V1_" (i.e., 'eS2o'-'eS6o' and 'eS2a'-'eS6a')
        # Running with all 'eS1o'-'eS6o' cuts (restricting to a specific electron sector)
    # Added new 3D histogram which shows the hit positions Hx and Hy as functions of the electron phi angle
        # These values are used in Valerii's cuts
        # The purpose of this plot is to help describe the fiducial cuts needed to help account for the edge effects in the electron detector sectors
    # Set of 2D Histograms of variables vs phi_t in this file have been reduced to only include:
        # Electron/Pi+ Sectors (esec/pipsec)
        # Lab Azimuthal angles (Phi) of both particles
    # Not running any Response Matrix histogram options
    
    
    
    
    Extra_Name = "New_Bin_Tests_V5_"
    # Ran on 1/26/2024
    # This file uses the new Q2-y/z-pT binning scheme ('Y_bin')
        # Initial tests of the new binning scheme with 3D unfolding
            # Future tests will try to rework the Multidimensional binning (new code contains the definitions of the 3D/5D kinematic bins that can be used with unfolding)
            # Current version calculates the multidimensional bin number in a more simplistic way (does not account for migration bins)
        # New binning scheme includes more migration bins (i.e., bins which are not meant to be analyzed but will provide details about events migrating into the main kinematic bins from outside the meaningful kinematic ranges)
    # Removed all non-standard options for histograms/cuts that are not required by the unfolding code
    if(Use_Pass_2):
        Extra_Name = "".join(["Pass_2_", str(Extra_Name)])
        # Ran with "New_Bin_Tests_V5_" on 1/29/2024
            # Added the option to run with Pass 2 Data
            
        print(f"\n\n\t{color.BOLD}{color.BLUE}Using Pass 2 Version of Data/MC Files{color.END}")
    
    
    
    if(run_Mom_Cor_Code == "yes"):
        Extra_Name = "New_Smearing_V1_"
        # Ran on 12/12/2023
        # Updated with Extra_Name = "Sec_Cut_Test_V2_" (all the same notes therefore apply)
            # Turned off any cut not related to the Momentum Correction/Smearing code
        # Added new form of the smearing plots to begin developing the smearing corrections as described in Valerii's procedure
        # Added plots to see the impact of the smearing correction within each kinematic bin (hard-coded to use the current Q2-y binning scheme 'y_bin')
        
        
        Extra_Name = "New_Smearing_V2_"
        # Ran on 2/5/2024
        # Updated with Extra_Name = "New_Smearing_V1_" (all the same notes therefore apply)
            # Turned off any cut not related to the Momentum Correction/Smearing code
        # Updated the ∆P/P plots to improve the binning ranges/sizes
        
        if(smear_factor != "0.75"):
            Extra_Name = "".join(["New_Smearing_", str(smear_factor).replace(".", ""), "_V2_"])
            # Same as "New_Smearing_V1_" but with any value of smear_factor not being equal to the default value of 0.75
        
    if(Use_Weight):
        if(not Q4_Weight):
            # Using the modulations of the Generated Monte Carlo
            Extra_Name = "".join([Extra_Name, "Modulated_"])
        else:
            # Using the Q4 wieghts
            Extra_Name = "".join([Extra_Name, "Q4_Wieght_"])
        
    
    if(datatype == 'rdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_Data_REC_",        str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'mdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Matched_",      str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'gdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_GEN_",          str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'pdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Only_Matched_", str(Extra_Name), str(file_num), ".root"])
        
    if(output_type in ["data", "test"]):
        ROOT_File_Output_Name = "".join(["DataFrame_", str(ROOT_File_Output_Name)])
    
    print("".join(["\nFile being made is: \033[1m",    str(ROOT_File_Output_Name), "\033[0m"]))
    
    
    #################     Final ROOT File     #################
    ###########################################################
    
    
    ################################################################     Done Loading Data Files     ################################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ############################################################    Particle Momentum Correction Code    ############################################################
    
    
    New_z_pT_and_MultiDim_Binning_Code = """
    float z_pT_Bin_Borders[18][65][4];
       // z_pT_Bin_Borders[Q2_y_Bin][z_pT_Bin][Border_Num]
        // Border_Num = 0 -> z_max
        // Border_Num = 1 -> z_min
        // Border_Num = 2 -> pT_max
        // Border_Num = 4 -> pT_min
        // (Total of 17 Q2-y bins with defined z-pT borders)
    int Phi_h_Bin_Values[40][65][3];
     // Phi_h_Bin_Values[Q2_y_Bin][z_pT_Bin][Dimension]
        // Dimension = 0 -> Number of phi_h bins (either 24 or 1)
        // Dimension = 1 -> Number of combined z_pT + phi_h bins        (used for 3D unfolding - add the appropiate phi_h bin number to these values to get the 3D bin number - resets with every new Q2-y bin)
        // Dimension = 2 -> Number of combined Q2_y + z_pT + phi_h bins (used for 5D unfolding - add the appropiate phi_h bin number to these values to get the 5D bin number - does not resets with new bins)
        // (Total of 39 Q2-y bins including migration bins)
    z_pT_Bin_Borders[1][1][0] = 0.2; z_pT_Bin_Borders[1][1][1] = 0.16; z_pT_Bin_Borders[1][1][2] = 0.2; z_pT_Bin_Borders[1][1][3] = 0.05;
    Phi_h_Bin_Values[1][1][0] =  24; Phi_h_Bin_Values[1][1][1] = 0; Phi_h_Bin_Values[1][1][2] = 0;
    z_pT_Bin_Borders[1][2][0] = 0.2; z_pT_Bin_Borders[1][2][1] = 0.16; z_pT_Bin_Borders[1][2][2] = 0.3; z_pT_Bin_Borders[1][2][3] = 0.2;
    Phi_h_Bin_Values[1][2][0] =  24; Phi_h_Bin_Values[1][2][1] = 24; Phi_h_Bin_Values[1][2][2] = 24;
    z_pT_Bin_Borders[1][3][0] = 0.2; z_pT_Bin_Borders[1][3][1] = 0.16; z_pT_Bin_Borders[1][3][2] = 0.4; z_pT_Bin_Borders[1][3][3] = 0.3;
    Phi_h_Bin_Values[1][3][0] =  24; Phi_h_Bin_Values[1][3][1] = 48; Phi_h_Bin_Values[1][3][2] = 48;
    z_pT_Bin_Borders[1][4][0] = 0.2; z_pT_Bin_Borders[1][4][1] = 0.16; z_pT_Bin_Borders[1][4][2] = 0.5; z_pT_Bin_Borders[1][4][3] = 0.4;
    Phi_h_Bin_Values[1][4][0] =  24; Phi_h_Bin_Values[1][4][1] = 72; Phi_h_Bin_Values[1][4][2] = 72;
    z_pT_Bin_Borders[1][5][0] = 0.2; z_pT_Bin_Borders[1][5][1] = 0.16; z_pT_Bin_Borders[1][5][2] = 0.6; z_pT_Bin_Borders[1][5][3] = 0.5;
    Phi_h_Bin_Values[1][5][0] =  1; Phi_h_Bin_Values[1][5][1] = 96; Phi_h_Bin_Values[1][5][2] = 96;
    z_pT_Bin_Borders[1][6][0] = 0.2; z_pT_Bin_Borders[1][6][1] = 0.16; z_pT_Bin_Borders[1][6][2] = 0.75; z_pT_Bin_Borders[1][6][3] = 0.6;
    Phi_h_Bin_Values[1][6][0] =  1; Phi_h_Bin_Values[1][6][1] = 97; Phi_h_Bin_Values[1][6][2] = 97;
    z_pT_Bin_Borders[1][7][0] = 0.2; z_pT_Bin_Borders[1][7][1] = 0.16; z_pT_Bin_Borders[1][7][2] = 1.0; z_pT_Bin_Borders[1][7][3] = 0.75;
    Phi_h_Bin_Values[1][7][0] =  1; Phi_h_Bin_Values[1][7][1] = 98; Phi_h_Bin_Values[1][7][2] = 98;
    z_pT_Bin_Borders[1][8][0] = 0.24; z_pT_Bin_Borders[1][8][1] = 0.2; z_pT_Bin_Borders[1][8][2] = 0.2; z_pT_Bin_Borders[1][8][3] = 0.05;
    Phi_h_Bin_Values[1][8][0] =  24; Phi_h_Bin_Values[1][8][1] = 99; Phi_h_Bin_Values[1][8][2] = 99;
    z_pT_Bin_Borders[1][9][0] = 0.24; z_pT_Bin_Borders[1][9][1] = 0.2; z_pT_Bin_Borders[1][9][2] = 0.3; z_pT_Bin_Borders[1][9][3] = 0.2;
    Phi_h_Bin_Values[1][9][0] =  24; Phi_h_Bin_Values[1][9][1] = 123; Phi_h_Bin_Values[1][9][2] = 123;
    z_pT_Bin_Borders[1][10][0] = 0.24; z_pT_Bin_Borders[1][10][1] = 0.2; z_pT_Bin_Borders[1][10][2] = 0.4; z_pT_Bin_Borders[1][10][3] = 0.3;
    Phi_h_Bin_Values[1][10][0] =  24; Phi_h_Bin_Values[1][10][1] = 147; Phi_h_Bin_Values[1][10][2] = 147;
    z_pT_Bin_Borders[1][11][0] = 0.24; z_pT_Bin_Borders[1][11][1] = 0.2; z_pT_Bin_Borders[1][11][2] = 0.5; z_pT_Bin_Borders[1][11][3] = 0.4;
    Phi_h_Bin_Values[1][11][0] =  24; Phi_h_Bin_Values[1][11][1] = 171; Phi_h_Bin_Values[1][11][2] = 171;
    z_pT_Bin_Borders[1][12][0] = 0.24; z_pT_Bin_Borders[1][12][1] = 0.2; z_pT_Bin_Borders[1][12][2] = 0.6; z_pT_Bin_Borders[1][12][3] = 0.5;
    Phi_h_Bin_Values[1][12][0] =  24; Phi_h_Bin_Values[1][12][1] = 195; Phi_h_Bin_Values[1][12][2] = 195;
    z_pT_Bin_Borders[1][13][0] = 0.24; z_pT_Bin_Borders[1][13][1] = 0.2; z_pT_Bin_Borders[1][13][2] = 0.75; z_pT_Bin_Borders[1][13][3] = 0.6;
    Phi_h_Bin_Values[1][13][0] =  1; Phi_h_Bin_Values[1][13][1] = 219; Phi_h_Bin_Values[1][13][2] = 219;
    z_pT_Bin_Borders[1][14][0] = 0.24; z_pT_Bin_Borders[1][14][1] = 0.2; z_pT_Bin_Borders[1][14][2] = 1.0; z_pT_Bin_Borders[1][14][3] = 0.75;
    Phi_h_Bin_Values[1][14][0] =  1; Phi_h_Bin_Values[1][14][1] = 220; Phi_h_Bin_Values[1][14][2] = 220;
    z_pT_Bin_Borders[1][15][0] = 0.31; z_pT_Bin_Borders[1][15][1] = 0.24; z_pT_Bin_Borders[1][15][2] = 0.2; z_pT_Bin_Borders[1][15][3] = 0.05;
    Phi_h_Bin_Values[1][15][0] =  24; Phi_h_Bin_Values[1][15][1] = 221; Phi_h_Bin_Values[1][15][2] = 221;
    z_pT_Bin_Borders[1][16][0] = 0.31; z_pT_Bin_Borders[1][16][1] = 0.24; z_pT_Bin_Borders[1][16][2] = 0.3; z_pT_Bin_Borders[1][16][3] = 0.2;
    Phi_h_Bin_Values[1][16][0] =  24; Phi_h_Bin_Values[1][16][1] = 245; Phi_h_Bin_Values[1][16][2] = 245;
    z_pT_Bin_Borders[1][17][0] = 0.31; z_pT_Bin_Borders[1][17][1] = 0.24; z_pT_Bin_Borders[1][17][2] = 0.4; z_pT_Bin_Borders[1][17][3] = 0.3;
    Phi_h_Bin_Values[1][17][0] =  24; Phi_h_Bin_Values[1][17][1] = 269; Phi_h_Bin_Values[1][17][2] = 269;
    z_pT_Bin_Borders[1][18][0] = 0.31; z_pT_Bin_Borders[1][18][1] = 0.24; z_pT_Bin_Borders[1][18][2] = 0.5; z_pT_Bin_Borders[1][18][3] = 0.4;
    Phi_h_Bin_Values[1][18][0] =  24; Phi_h_Bin_Values[1][18][1] = 293; Phi_h_Bin_Values[1][18][2] = 293;
    z_pT_Bin_Borders[1][19][0] = 0.31; z_pT_Bin_Borders[1][19][1] = 0.24; z_pT_Bin_Borders[1][19][2] = 0.6; z_pT_Bin_Borders[1][19][3] = 0.5;
    Phi_h_Bin_Values[1][19][0] =  24; Phi_h_Bin_Values[1][19][1] = 317; Phi_h_Bin_Values[1][19][2] = 317;
    z_pT_Bin_Borders[1][20][0] = 0.31; z_pT_Bin_Borders[1][20][1] = 0.24; z_pT_Bin_Borders[1][20][2] = 0.75; z_pT_Bin_Borders[1][20][3] = 0.6;
    Phi_h_Bin_Values[1][20][0] =  24; Phi_h_Bin_Values[1][20][1] = 341; Phi_h_Bin_Values[1][20][2] = 341;
    z_pT_Bin_Borders[1][21][0] = 0.31; z_pT_Bin_Borders[1][21][1] = 0.24; z_pT_Bin_Borders[1][21][2] = 1.0; z_pT_Bin_Borders[1][21][3] = 0.75;
    Phi_h_Bin_Values[1][21][0] =  1; Phi_h_Bin_Values[1][21][1] = 365; Phi_h_Bin_Values[1][21][2] = 365;
    z_pT_Bin_Borders[1][22][0] = 0.41; z_pT_Bin_Borders[1][22][1] = 0.31; z_pT_Bin_Borders[1][22][2] = 0.2; z_pT_Bin_Borders[1][22][3] = 0.05;
    Phi_h_Bin_Values[1][22][0] =  24; Phi_h_Bin_Values[1][22][1] = 366; Phi_h_Bin_Values[1][22][2] = 366;
    z_pT_Bin_Borders[1][23][0] = 0.41; z_pT_Bin_Borders[1][23][1] = 0.31; z_pT_Bin_Borders[1][23][2] = 0.3; z_pT_Bin_Borders[1][23][3] = 0.2;
    Phi_h_Bin_Values[1][23][0] =  24; Phi_h_Bin_Values[1][23][1] = 390; Phi_h_Bin_Values[1][23][2] = 390;
    z_pT_Bin_Borders[1][24][0] = 0.41; z_pT_Bin_Borders[1][24][1] = 0.31; z_pT_Bin_Borders[1][24][2] = 0.4; z_pT_Bin_Borders[1][24][3] = 0.3;
    Phi_h_Bin_Values[1][24][0] =  24; Phi_h_Bin_Values[1][24][1] = 414; Phi_h_Bin_Values[1][24][2] = 414;
    z_pT_Bin_Borders[1][25][0] = 0.41; z_pT_Bin_Borders[1][25][1] = 0.31; z_pT_Bin_Borders[1][25][2] = 0.5; z_pT_Bin_Borders[1][25][3] = 0.4;
    Phi_h_Bin_Values[1][25][0] =  24; Phi_h_Bin_Values[1][25][1] = 438; Phi_h_Bin_Values[1][25][2] = 438;
    z_pT_Bin_Borders[1][26][0] = 0.41; z_pT_Bin_Borders[1][26][1] = 0.31; z_pT_Bin_Borders[1][26][2] = 0.6; z_pT_Bin_Borders[1][26][3] = 0.5;
    Phi_h_Bin_Values[1][26][0] =  24; Phi_h_Bin_Values[1][26][1] = 462; Phi_h_Bin_Values[1][26][2] = 462;
    z_pT_Bin_Borders[1][27][0] = 0.41; z_pT_Bin_Borders[1][27][1] = 0.31; z_pT_Bin_Borders[1][27][2] = 0.75; z_pT_Bin_Borders[1][27][3] = 0.6;
    Phi_h_Bin_Values[1][27][0] =  24; Phi_h_Bin_Values[1][27][1] = 486; Phi_h_Bin_Values[1][27][2] = 486;
    z_pT_Bin_Borders[1][28][0] = 0.41; z_pT_Bin_Borders[1][28][1] = 0.31; z_pT_Bin_Borders[1][28][2] = 1.0; z_pT_Bin_Borders[1][28][3] = 0.75;
    Phi_h_Bin_Values[1][28][0] =  24; Phi_h_Bin_Values[1][28][1] = 510; Phi_h_Bin_Values[1][28][2] = 510;
    z_pT_Bin_Borders[1][29][0] = 0.7; z_pT_Bin_Borders[1][29][1] = 0.41; z_pT_Bin_Borders[1][29][2] = 0.2; z_pT_Bin_Borders[1][29][3] = 0.05;
    Phi_h_Bin_Values[1][29][0] =  24; Phi_h_Bin_Values[1][29][1] = 534; Phi_h_Bin_Values[1][29][2] = 534;
    z_pT_Bin_Borders[1][30][0] = 0.7; z_pT_Bin_Borders[1][30][1] = 0.41; z_pT_Bin_Borders[1][30][2] = 0.3; z_pT_Bin_Borders[1][30][3] = 0.2;
    Phi_h_Bin_Values[1][30][0] =  24; Phi_h_Bin_Values[1][30][1] = 558; Phi_h_Bin_Values[1][30][2] = 558;
    z_pT_Bin_Borders[1][31][0] = 0.7; z_pT_Bin_Borders[1][31][1] = 0.41; z_pT_Bin_Borders[1][31][2] = 0.4; z_pT_Bin_Borders[1][31][3] = 0.3;
    Phi_h_Bin_Values[1][31][0] =  24; Phi_h_Bin_Values[1][31][1] = 582; Phi_h_Bin_Values[1][31][2] = 582;
    z_pT_Bin_Borders[1][32][0] = 0.7; z_pT_Bin_Borders[1][32][1] = 0.41; z_pT_Bin_Borders[1][32][2] = 0.5; z_pT_Bin_Borders[1][32][3] = 0.4;
    Phi_h_Bin_Values[1][32][0] =  24; Phi_h_Bin_Values[1][32][1] = 606; Phi_h_Bin_Values[1][32][2] = 606;
    z_pT_Bin_Borders[1][33][0] = 0.7; z_pT_Bin_Borders[1][33][1] = 0.41; z_pT_Bin_Borders[1][33][2] = 0.6; z_pT_Bin_Borders[1][33][3] = 0.5;
    Phi_h_Bin_Values[1][33][0] =  24; Phi_h_Bin_Values[1][33][1] = 630; Phi_h_Bin_Values[1][33][2] = 630;
    z_pT_Bin_Borders[1][34][0] = 0.7; z_pT_Bin_Borders[1][34][1] = 0.41; z_pT_Bin_Borders[1][34][2] = 0.75; z_pT_Bin_Borders[1][34][3] = 0.6;
    Phi_h_Bin_Values[1][34][0] =  24; Phi_h_Bin_Values[1][34][1] = 654; Phi_h_Bin_Values[1][34][2] = 654;
    z_pT_Bin_Borders[1][35][0] = 0.7; z_pT_Bin_Borders[1][35][1] = 0.41; z_pT_Bin_Borders[1][35][2] = 1.0; z_pT_Bin_Borders[1][35][3] = 0.75;
    Phi_h_Bin_Values[1][35][0] =  24; Phi_h_Bin_Values[1][35][1] = 678; Phi_h_Bin_Values[1][35][2] = 678;
    z_pT_Bin_Borders[1][36][0] = 0.16; z_pT_Bin_Borders[1][36][1] = 0; z_pT_Bin_Borders[1][36][2] = 0.05; z_pT_Bin_Borders[1][36][3] = 0;
    Phi_h_Bin_Values[1][36][0] =  1; Phi_h_Bin_Values[1][36][1] = 702; Phi_h_Bin_Values[1][36][2] = 702;
    z_pT_Bin_Borders[1][37][0] = 0.16; z_pT_Bin_Borders[1][37][1] = 0; z_pT_Bin_Borders[1][37][2] = 0.05; z_pT_Bin_Borders[1][37][3] = 0.2;
    Phi_h_Bin_Values[1][37][0] =  1; Phi_h_Bin_Values[1][37][1] = 703; Phi_h_Bin_Values[1][37][2] = 703;
    z_pT_Bin_Borders[1][38][0] = 0.16; z_pT_Bin_Borders[1][38][1] = 0; z_pT_Bin_Borders[1][38][2] = 0.2; z_pT_Bin_Borders[1][38][3] = 0.3;
    Phi_h_Bin_Values[1][38][0] =  1; Phi_h_Bin_Values[1][38][1] = 704; Phi_h_Bin_Values[1][38][2] = 704;
    z_pT_Bin_Borders[1][39][0] = 0.16; z_pT_Bin_Borders[1][39][1] = 0; z_pT_Bin_Borders[1][39][2] = 0.3; z_pT_Bin_Borders[1][39][3] = 0.4;
    Phi_h_Bin_Values[1][39][0] =  1; Phi_h_Bin_Values[1][39][1] = 705; Phi_h_Bin_Values[1][39][2] = 705;
    z_pT_Bin_Borders[1][40][0] = 0.16; z_pT_Bin_Borders[1][40][1] = 0; z_pT_Bin_Borders[1][40][2] = 0.4; z_pT_Bin_Borders[1][40][3] = 0.5;
    Phi_h_Bin_Values[1][40][0] =  1; Phi_h_Bin_Values[1][40][1] = 706; Phi_h_Bin_Values[1][40][2] = 706;
    z_pT_Bin_Borders[1][41][0] = 0.16; z_pT_Bin_Borders[1][41][1] = 0; z_pT_Bin_Borders[1][41][2] = 0.5; z_pT_Bin_Borders[1][41][3] = 0.6;
    Phi_h_Bin_Values[1][41][0] =  1; Phi_h_Bin_Values[1][41][1] = 707; Phi_h_Bin_Values[1][41][2] = 707;
    z_pT_Bin_Borders[1][42][0] = 0.16; z_pT_Bin_Borders[1][42][1] = 0; z_pT_Bin_Borders[1][42][2] = 0.6; z_pT_Bin_Borders[1][42][3] = 0.75;
    Phi_h_Bin_Values[1][42][0] =  1; Phi_h_Bin_Values[1][42][1] = 708; Phi_h_Bin_Values[1][42][2] = 708;
    z_pT_Bin_Borders[1][43][0] = 0.16; z_pT_Bin_Borders[1][43][1] = 0; z_pT_Bin_Borders[1][43][2] = 0.75; z_pT_Bin_Borders[1][43][3] = 1.0;
    Phi_h_Bin_Values[1][43][0] =  1; Phi_h_Bin_Values[1][43][1] = 709; Phi_h_Bin_Values[1][43][2] = 709;
    z_pT_Bin_Borders[1][44][0] = 0.16; z_pT_Bin_Borders[1][44][1] = 0; z_pT_Bin_Borders[1][44][2] = 10; z_pT_Bin_Borders[1][44][3] = 1.0;
    Phi_h_Bin_Values[1][44][0] =  1; Phi_h_Bin_Values[1][44][1] = 710; Phi_h_Bin_Values[1][44][2] = 710;
    z_pT_Bin_Borders[1][45][0] = 0.16; z_pT_Bin_Borders[1][45][1] = 0.2; z_pT_Bin_Borders[1][45][2] = 0.05; z_pT_Bin_Borders[1][45][3] = 0;
    Phi_h_Bin_Values[1][45][0] =  1; Phi_h_Bin_Values[1][45][1] = 711; Phi_h_Bin_Values[1][45][2] = 711;
    z_pT_Bin_Borders[1][46][0] = 0.16; z_pT_Bin_Borders[1][46][1] = 0.2; z_pT_Bin_Borders[1][46][2] = 10; z_pT_Bin_Borders[1][46][3] = 1.0;
    Phi_h_Bin_Values[1][46][0] =  1; Phi_h_Bin_Values[1][46][1] = 712; Phi_h_Bin_Values[1][46][2] = 712;
    z_pT_Bin_Borders[1][47][0] = 0.2; z_pT_Bin_Borders[1][47][1] = 0.24; z_pT_Bin_Borders[1][47][2] = 0.05; z_pT_Bin_Borders[1][47][3] = 0;
    Phi_h_Bin_Values[1][47][0] =  1; Phi_h_Bin_Values[1][47][1] = 713; Phi_h_Bin_Values[1][47][2] = 713;
    z_pT_Bin_Borders[1][48][0] = 0.2; z_pT_Bin_Borders[1][48][1] = 0.24; z_pT_Bin_Borders[1][48][2] = 10; z_pT_Bin_Borders[1][48][3] = 1.0;
    Phi_h_Bin_Values[1][48][0] =  1; Phi_h_Bin_Values[1][48][1] = 714; Phi_h_Bin_Values[1][48][2] = 714;
    z_pT_Bin_Borders[1][49][0] = 0.24; z_pT_Bin_Borders[1][49][1] = 0.31; z_pT_Bin_Borders[1][49][2] = 0.05; z_pT_Bin_Borders[1][49][3] = 0;
    Phi_h_Bin_Values[1][49][0] =  1; Phi_h_Bin_Values[1][49][1] = 715; Phi_h_Bin_Values[1][49][2] = 715;
    z_pT_Bin_Borders[1][50][0] = 0.24; z_pT_Bin_Borders[1][50][1] = 0.31; z_pT_Bin_Borders[1][50][2] = 10; z_pT_Bin_Borders[1][50][3] = 1.0;
    Phi_h_Bin_Values[1][50][0] =  1; Phi_h_Bin_Values[1][50][1] = 716; Phi_h_Bin_Values[1][50][2] = 716;
    z_pT_Bin_Borders[1][51][0] = 0.31; z_pT_Bin_Borders[1][51][1] = 0.41; z_pT_Bin_Borders[1][51][2] = 0.05; z_pT_Bin_Borders[1][51][3] = 0;
    Phi_h_Bin_Values[1][51][0] =  1; Phi_h_Bin_Values[1][51][1] = 717; Phi_h_Bin_Values[1][51][2] = 717;
    z_pT_Bin_Borders[1][52][0] = 0.31; z_pT_Bin_Borders[1][52][1] = 0.41; z_pT_Bin_Borders[1][52][2] = 10; z_pT_Bin_Borders[1][52][3] = 1.0;
    Phi_h_Bin_Values[1][52][0] =  1; Phi_h_Bin_Values[1][52][1] = 718; Phi_h_Bin_Values[1][52][2] = 718;
    z_pT_Bin_Borders[1][53][0] = 0.41; z_pT_Bin_Borders[1][53][1] = 0.7; z_pT_Bin_Borders[1][53][2] = 0.05; z_pT_Bin_Borders[1][53][3] = 0;
    Phi_h_Bin_Values[1][53][0] =  1; Phi_h_Bin_Values[1][53][1] = 719; Phi_h_Bin_Values[1][53][2] = 719;
    z_pT_Bin_Borders[1][54][0] = 0.41; z_pT_Bin_Borders[1][54][1] = 0.7; z_pT_Bin_Borders[1][54][2] = 10; z_pT_Bin_Borders[1][54][3] = 1.0;
    Phi_h_Bin_Values[1][54][0] =  1; Phi_h_Bin_Values[1][54][1] = 720; Phi_h_Bin_Values[1][54][2] = 720;
    z_pT_Bin_Borders[1][55][0] = 10; z_pT_Bin_Borders[1][55][1] = 0.7; z_pT_Bin_Borders[1][55][2] = 0; z_pT_Bin_Borders[1][55][3] = 0.05;
    Phi_h_Bin_Values[1][55][0] =  1; Phi_h_Bin_Values[1][55][1] = 721; Phi_h_Bin_Values[1][55][2] = 721;
    z_pT_Bin_Borders[1][56][0] = 10; z_pT_Bin_Borders[1][56][1] = 0.7; z_pT_Bin_Borders[1][56][2] = 0.05; z_pT_Bin_Borders[1][56][3] = 0.2;
    Phi_h_Bin_Values[1][56][0] =  1; Phi_h_Bin_Values[1][56][1] = 722; Phi_h_Bin_Values[1][56][2] = 722;
    z_pT_Bin_Borders[1][57][0] = 10; z_pT_Bin_Borders[1][57][1] = 0.7; z_pT_Bin_Borders[1][57][2] = 0.2; z_pT_Bin_Borders[1][57][3] = 0.3;
    Phi_h_Bin_Values[1][57][0] =  1; Phi_h_Bin_Values[1][57][1] = 723; Phi_h_Bin_Values[1][57][2] = 723;
    z_pT_Bin_Borders[1][58][0] = 10; z_pT_Bin_Borders[1][58][1] = 0.7; z_pT_Bin_Borders[1][58][2] = 0.3; z_pT_Bin_Borders[1][58][3] = 0.4;
    Phi_h_Bin_Values[1][58][0] =  1; Phi_h_Bin_Values[1][58][1] = 724; Phi_h_Bin_Values[1][58][2] = 724;
    z_pT_Bin_Borders[1][59][0] = 10; z_pT_Bin_Borders[1][59][1] = 0.7; z_pT_Bin_Borders[1][59][2] = 0.4; z_pT_Bin_Borders[1][59][3] = 0.5;
    Phi_h_Bin_Values[1][59][0] =  1; Phi_h_Bin_Values[1][59][1] = 725; Phi_h_Bin_Values[1][59][2] = 725;
    z_pT_Bin_Borders[1][60][0] = 10; z_pT_Bin_Borders[1][60][1] = 0.7; z_pT_Bin_Borders[1][60][2] = 0.5; z_pT_Bin_Borders[1][60][3] = 0.6;
    Phi_h_Bin_Values[1][60][0] =  1; Phi_h_Bin_Values[1][60][1] = 726; Phi_h_Bin_Values[1][60][2] = 726;
    z_pT_Bin_Borders[1][61][0] = 10; z_pT_Bin_Borders[1][61][1] = 0.7; z_pT_Bin_Borders[1][61][2] = 0.6; z_pT_Bin_Borders[1][61][3] = 0.75;
    Phi_h_Bin_Values[1][61][0] =  1; Phi_h_Bin_Values[1][61][1] = 727; Phi_h_Bin_Values[1][61][2] = 727;
    z_pT_Bin_Borders[1][62][0] = 10; z_pT_Bin_Borders[1][62][1] = 0.7; z_pT_Bin_Borders[1][62][2] = 0.75; z_pT_Bin_Borders[1][62][3] = 1.0;
    Phi_h_Bin_Values[1][62][0] =  1; Phi_h_Bin_Values[1][62][1] = 728; Phi_h_Bin_Values[1][62][2] = 728;
    z_pT_Bin_Borders[1][63][0] = 10; z_pT_Bin_Borders[1][63][1] = 0.7; z_pT_Bin_Borders[1][63][2] = 10; z_pT_Bin_Borders[1][63][3] = 1.0;
    Phi_h_Bin_Values[1][63][0] =  1; Phi_h_Bin_Values[1][63][1] = 729; Phi_h_Bin_Values[1][63][2] = 729;
    z_pT_Bin_Borders[2][1][0] = 0.23; z_pT_Bin_Borders[2][1][1] = 0.19; z_pT_Bin_Borders[2][1][2] = 0.25; z_pT_Bin_Borders[2][1][3] = 0.05;
    Phi_h_Bin_Values[2][1][0] =  24; Phi_h_Bin_Values[2][1][1] = 0; Phi_h_Bin_Values[2][1][2] = 730;
    z_pT_Bin_Borders[2][2][0] = 0.23; z_pT_Bin_Borders[2][2][1] = 0.19; z_pT_Bin_Borders[2][2][2] = 0.35; z_pT_Bin_Borders[2][2][3] = 0.25;
    Phi_h_Bin_Values[2][2][0] =  24; Phi_h_Bin_Values[2][2][1] = 24; Phi_h_Bin_Values[2][2][2] = 754;
    z_pT_Bin_Borders[2][3][0] = 0.23; z_pT_Bin_Borders[2][3][1] = 0.19; z_pT_Bin_Borders[2][3][2] = 0.45; z_pT_Bin_Borders[2][3][3] = 0.35;
    Phi_h_Bin_Values[2][3][0] =  24; Phi_h_Bin_Values[2][3][1] = 48; Phi_h_Bin_Values[2][3][2] = 778;
    z_pT_Bin_Borders[2][4][0] = 0.23; z_pT_Bin_Borders[2][4][1] = 0.19; z_pT_Bin_Borders[2][4][2] = 0.54; z_pT_Bin_Borders[2][4][3] = 0.45;
    Phi_h_Bin_Values[2][4][0] =  24; Phi_h_Bin_Values[2][4][1] = 72; Phi_h_Bin_Values[2][4][2] = 802;
    z_pT_Bin_Borders[2][5][0] = 0.23; z_pT_Bin_Borders[2][5][1] = 0.19; z_pT_Bin_Borders[2][5][2] = 0.67; z_pT_Bin_Borders[2][5][3] = 0.54;
    Phi_h_Bin_Values[2][5][0] =  1; Phi_h_Bin_Values[2][5][1] = 96; Phi_h_Bin_Values[2][5][2] = 826;
    z_pT_Bin_Borders[2][6][0] = 0.23; z_pT_Bin_Borders[2][6][1] = 0.19; z_pT_Bin_Borders[2][6][2] = 0.93; z_pT_Bin_Borders[2][6][3] = 0.67;
    Phi_h_Bin_Values[2][6][0] =  1; Phi_h_Bin_Values[2][6][1] = 97; Phi_h_Bin_Values[2][6][2] = 827;
    z_pT_Bin_Borders[2][7][0] = 0.26; z_pT_Bin_Borders[2][7][1] = 0.23; z_pT_Bin_Borders[2][7][2] = 0.25; z_pT_Bin_Borders[2][7][3] = 0.05;
    Phi_h_Bin_Values[2][7][0] =  24; Phi_h_Bin_Values[2][7][1] = 98; Phi_h_Bin_Values[2][7][2] = 828;
    z_pT_Bin_Borders[2][8][0] = 0.26; z_pT_Bin_Borders[2][8][1] = 0.23; z_pT_Bin_Borders[2][8][2] = 0.35; z_pT_Bin_Borders[2][8][3] = 0.25;
    Phi_h_Bin_Values[2][8][0] =  24; Phi_h_Bin_Values[2][8][1] = 122; Phi_h_Bin_Values[2][8][2] = 852;
    z_pT_Bin_Borders[2][9][0] = 0.26; z_pT_Bin_Borders[2][9][1] = 0.23; z_pT_Bin_Borders[2][9][2] = 0.45; z_pT_Bin_Borders[2][9][3] = 0.35;
    Phi_h_Bin_Values[2][9][0] =  24; Phi_h_Bin_Values[2][9][1] = 146; Phi_h_Bin_Values[2][9][2] = 876;
    z_pT_Bin_Borders[2][10][0] = 0.26; z_pT_Bin_Borders[2][10][1] = 0.23; z_pT_Bin_Borders[2][10][2] = 0.54; z_pT_Bin_Borders[2][10][3] = 0.45;
    Phi_h_Bin_Values[2][10][0] =  24; Phi_h_Bin_Values[2][10][1] = 170; Phi_h_Bin_Values[2][10][2] = 900;
    z_pT_Bin_Borders[2][11][0] = 0.26; z_pT_Bin_Borders[2][11][1] = 0.23; z_pT_Bin_Borders[2][11][2] = 0.67; z_pT_Bin_Borders[2][11][3] = 0.54;
    Phi_h_Bin_Values[2][11][0] =  24; Phi_h_Bin_Values[2][11][1] = 194; Phi_h_Bin_Values[2][11][2] = 924;
    z_pT_Bin_Borders[2][12][0] = 0.26; z_pT_Bin_Borders[2][12][1] = 0.23; z_pT_Bin_Borders[2][12][2] = 0.93; z_pT_Bin_Borders[2][12][3] = 0.67;
    Phi_h_Bin_Values[2][12][0] =  1; Phi_h_Bin_Values[2][12][1] = 218; Phi_h_Bin_Values[2][12][2] = 948;
    z_pT_Bin_Borders[2][13][0] = 0.31; z_pT_Bin_Borders[2][13][1] = 0.26; z_pT_Bin_Borders[2][13][2] = 0.25; z_pT_Bin_Borders[2][13][3] = 0.05;
    Phi_h_Bin_Values[2][13][0] =  24; Phi_h_Bin_Values[2][13][1] = 219; Phi_h_Bin_Values[2][13][2] = 949;
    z_pT_Bin_Borders[2][14][0] = 0.31; z_pT_Bin_Borders[2][14][1] = 0.26; z_pT_Bin_Borders[2][14][2] = 0.35; z_pT_Bin_Borders[2][14][3] = 0.25;
    Phi_h_Bin_Values[2][14][0] =  24; Phi_h_Bin_Values[2][14][1] = 243; Phi_h_Bin_Values[2][14][2] = 973;
    z_pT_Bin_Borders[2][15][0] = 0.31; z_pT_Bin_Borders[2][15][1] = 0.26; z_pT_Bin_Borders[2][15][2] = 0.45; z_pT_Bin_Borders[2][15][3] = 0.35;
    Phi_h_Bin_Values[2][15][0] =  24; Phi_h_Bin_Values[2][15][1] = 267; Phi_h_Bin_Values[2][15][2] = 997;
    z_pT_Bin_Borders[2][16][0] = 0.31; z_pT_Bin_Borders[2][16][1] = 0.26; z_pT_Bin_Borders[2][16][2] = 0.54; z_pT_Bin_Borders[2][16][3] = 0.45;
    Phi_h_Bin_Values[2][16][0] =  24; Phi_h_Bin_Values[2][16][1] = 291; Phi_h_Bin_Values[2][16][2] = 1021;
    z_pT_Bin_Borders[2][17][0] = 0.31; z_pT_Bin_Borders[2][17][1] = 0.26; z_pT_Bin_Borders[2][17][2] = 0.67; z_pT_Bin_Borders[2][17][3] = 0.54;
    Phi_h_Bin_Values[2][17][0] =  24; Phi_h_Bin_Values[2][17][1] = 315; Phi_h_Bin_Values[2][17][2] = 1045;
    z_pT_Bin_Borders[2][18][0] = 0.31; z_pT_Bin_Borders[2][18][1] = 0.26; z_pT_Bin_Borders[2][18][2] = 0.93; z_pT_Bin_Borders[2][18][3] = 0.67;
    Phi_h_Bin_Values[2][18][0] =  1; Phi_h_Bin_Values[2][18][1] = 339; Phi_h_Bin_Values[2][18][2] = 1069;
    z_pT_Bin_Borders[2][19][0] = 0.38; z_pT_Bin_Borders[2][19][1] = 0.31; z_pT_Bin_Borders[2][19][2] = 0.25; z_pT_Bin_Borders[2][19][3] = 0.05;
    Phi_h_Bin_Values[2][19][0] =  24; Phi_h_Bin_Values[2][19][1] = 340; Phi_h_Bin_Values[2][19][2] = 1070;
    z_pT_Bin_Borders[2][20][0] = 0.38; z_pT_Bin_Borders[2][20][1] = 0.31; z_pT_Bin_Borders[2][20][2] = 0.35; z_pT_Bin_Borders[2][20][3] = 0.25;
    Phi_h_Bin_Values[2][20][0] =  24; Phi_h_Bin_Values[2][20][1] = 364; Phi_h_Bin_Values[2][20][2] = 1094;
    z_pT_Bin_Borders[2][21][0] = 0.38; z_pT_Bin_Borders[2][21][1] = 0.31; z_pT_Bin_Borders[2][21][2] = 0.45; z_pT_Bin_Borders[2][21][3] = 0.35;
    Phi_h_Bin_Values[2][21][0] =  24; Phi_h_Bin_Values[2][21][1] = 388; Phi_h_Bin_Values[2][21][2] = 1118;
    z_pT_Bin_Borders[2][22][0] = 0.38; z_pT_Bin_Borders[2][22][1] = 0.31; z_pT_Bin_Borders[2][22][2] = 0.54; z_pT_Bin_Borders[2][22][3] = 0.45;
    Phi_h_Bin_Values[2][22][0] =  24; Phi_h_Bin_Values[2][22][1] = 412; Phi_h_Bin_Values[2][22][2] = 1142;
    z_pT_Bin_Borders[2][23][0] = 0.38; z_pT_Bin_Borders[2][23][1] = 0.31; z_pT_Bin_Borders[2][23][2] = 0.67; z_pT_Bin_Borders[2][23][3] = 0.54;
    Phi_h_Bin_Values[2][23][0] =  24; Phi_h_Bin_Values[2][23][1] = 436; Phi_h_Bin_Values[2][23][2] = 1166;
    z_pT_Bin_Borders[2][24][0] = 0.38; z_pT_Bin_Borders[2][24][1] = 0.31; z_pT_Bin_Borders[2][24][2] = 0.93; z_pT_Bin_Borders[2][24][3] = 0.67;
    Phi_h_Bin_Values[2][24][0] =  24; Phi_h_Bin_Values[2][24][1] = 460; Phi_h_Bin_Values[2][24][2] = 1190;
    z_pT_Bin_Borders[2][25][0] = 0.5; z_pT_Bin_Borders[2][25][1] = 0.38; z_pT_Bin_Borders[2][25][2] = 0.25; z_pT_Bin_Borders[2][25][3] = 0.05;
    Phi_h_Bin_Values[2][25][0] =  24; Phi_h_Bin_Values[2][25][1] = 484; Phi_h_Bin_Values[2][25][2] = 1214;
    z_pT_Bin_Borders[2][26][0] = 0.5; z_pT_Bin_Borders[2][26][1] = 0.38; z_pT_Bin_Borders[2][26][2] = 0.35; z_pT_Bin_Borders[2][26][3] = 0.25;
    Phi_h_Bin_Values[2][26][0] =  24; Phi_h_Bin_Values[2][26][1] = 508; Phi_h_Bin_Values[2][26][2] = 1238;
    z_pT_Bin_Borders[2][27][0] = 0.5; z_pT_Bin_Borders[2][27][1] = 0.38; z_pT_Bin_Borders[2][27][2] = 0.45; z_pT_Bin_Borders[2][27][3] = 0.35;
    Phi_h_Bin_Values[2][27][0] =  24; Phi_h_Bin_Values[2][27][1] = 532; Phi_h_Bin_Values[2][27][2] = 1262;
    z_pT_Bin_Borders[2][28][0] = 0.5; z_pT_Bin_Borders[2][28][1] = 0.38; z_pT_Bin_Borders[2][28][2] = 0.54; z_pT_Bin_Borders[2][28][3] = 0.45;
    Phi_h_Bin_Values[2][28][0] =  24; Phi_h_Bin_Values[2][28][1] = 556; Phi_h_Bin_Values[2][28][2] = 1286;
    z_pT_Bin_Borders[2][29][0] = 0.5; z_pT_Bin_Borders[2][29][1] = 0.38; z_pT_Bin_Borders[2][29][2] = 0.67; z_pT_Bin_Borders[2][29][3] = 0.54;
    Phi_h_Bin_Values[2][29][0] =  24; Phi_h_Bin_Values[2][29][1] = 580; Phi_h_Bin_Values[2][29][2] = 1310;
    z_pT_Bin_Borders[2][30][0] = 0.5; z_pT_Bin_Borders[2][30][1] = 0.38; z_pT_Bin_Borders[2][30][2] = 0.93; z_pT_Bin_Borders[2][30][3] = 0.67;
    Phi_h_Bin_Values[2][30][0] =  24; Phi_h_Bin_Values[2][30][1] = 604; Phi_h_Bin_Values[2][30][2] = 1334;
    z_pT_Bin_Borders[2][31][0] = 0.75; z_pT_Bin_Borders[2][31][1] = 0.5; z_pT_Bin_Borders[2][31][2] = 0.25; z_pT_Bin_Borders[2][31][3] = 0.05;
    Phi_h_Bin_Values[2][31][0] =  24; Phi_h_Bin_Values[2][31][1] = 628; Phi_h_Bin_Values[2][31][2] = 1358;
    z_pT_Bin_Borders[2][32][0] = 0.75; z_pT_Bin_Borders[2][32][1] = 0.5; z_pT_Bin_Borders[2][32][2] = 0.35; z_pT_Bin_Borders[2][32][3] = 0.25;
    Phi_h_Bin_Values[2][32][0] =  24; Phi_h_Bin_Values[2][32][1] = 652; Phi_h_Bin_Values[2][32][2] = 1382;
    z_pT_Bin_Borders[2][33][0] = 0.75; z_pT_Bin_Borders[2][33][1] = 0.5; z_pT_Bin_Borders[2][33][2] = 0.45; z_pT_Bin_Borders[2][33][3] = 0.35;
    Phi_h_Bin_Values[2][33][0] =  24; Phi_h_Bin_Values[2][33][1] = 676; Phi_h_Bin_Values[2][33][2] = 1406;
    z_pT_Bin_Borders[2][34][0] = 0.75; z_pT_Bin_Borders[2][34][1] = 0.5; z_pT_Bin_Borders[2][34][2] = 0.54; z_pT_Bin_Borders[2][34][3] = 0.45;
    Phi_h_Bin_Values[2][34][0] =  24; Phi_h_Bin_Values[2][34][1] = 700; Phi_h_Bin_Values[2][34][2] = 1430;
    z_pT_Bin_Borders[2][35][0] = 0.75; z_pT_Bin_Borders[2][35][1] = 0.5; z_pT_Bin_Borders[2][35][2] = 0.67; z_pT_Bin_Borders[2][35][3] = 0.54;
    Phi_h_Bin_Values[2][35][0] =  24; Phi_h_Bin_Values[2][35][1] = 724; Phi_h_Bin_Values[2][35][2] = 1454;
    z_pT_Bin_Borders[2][36][0] = 0.75; z_pT_Bin_Borders[2][36][1] = 0.5; z_pT_Bin_Borders[2][36][2] = 0.93; z_pT_Bin_Borders[2][36][3] = 0.67;
    Phi_h_Bin_Values[2][36][0] =  1; Phi_h_Bin_Values[2][36][1] = 748; Phi_h_Bin_Values[2][36][2] = 1478;
    z_pT_Bin_Borders[2][37][0] = 0.19; z_pT_Bin_Borders[2][37][1] = 0; z_pT_Bin_Borders[2][37][2] = 0.05; z_pT_Bin_Borders[2][37][3] = 0;
    Phi_h_Bin_Values[2][37][0] =  1; Phi_h_Bin_Values[2][37][1] = 749; Phi_h_Bin_Values[2][37][2] = 1479;
    z_pT_Bin_Borders[2][38][0] = 0.19; z_pT_Bin_Borders[2][38][1] = 0; z_pT_Bin_Borders[2][38][2] = 0.05; z_pT_Bin_Borders[2][38][3] = 0.25;
    Phi_h_Bin_Values[2][38][0] =  1; Phi_h_Bin_Values[2][38][1] = 750; Phi_h_Bin_Values[2][38][2] = 1480;
    z_pT_Bin_Borders[2][39][0] = 0.19; z_pT_Bin_Borders[2][39][1] = 0; z_pT_Bin_Borders[2][39][2] = 0.25; z_pT_Bin_Borders[2][39][3] = 0.35;
    Phi_h_Bin_Values[2][39][0] =  1; Phi_h_Bin_Values[2][39][1] = 751; Phi_h_Bin_Values[2][39][2] = 1481;
    z_pT_Bin_Borders[2][40][0] = 0.19; z_pT_Bin_Borders[2][40][1] = 0; z_pT_Bin_Borders[2][40][2] = 0.35; z_pT_Bin_Borders[2][40][3] = 0.45;
    Phi_h_Bin_Values[2][40][0] =  1; Phi_h_Bin_Values[2][40][1] = 752; Phi_h_Bin_Values[2][40][2] = 1482;
    z_pT_Bin_Borders[2][41][0] = 0.19; z_pT_Bin_Borders[2][41][1] = 0; z_pT_Bin_Borders[2][41][2] = 0.45; z_pT_Bin_Borders[2][41][3] = 0.54;
    Phi_h_Bin_Values[2][41][0] =  1; Phi_h_Bin_Values[2][41][1] = 753; Phi_h_Bin_Values[2][41][2] = 1483;
    z_pT_Bin_Borders[2][42][0] = 0.19; z_pT_Bin_Borders[2][42][1] = 0; z_pT_Bin_Borders[2][42][2] = 0.54; z_pT_Bin_Borders[2][42][3] = 0.67;
    Phi_h_Bin_Values[2][42][0] =  1; Phi_h_Bin_Values[2][42][1] = 754; Phi_h_Bin_Values[2][42][2] = 1484;
    z_pT_Bin_Borders[2][43][0] = 0.19; z_pT_Bin_Borders[2][43][1] = 0; z_pT_Bin_Borders[2][43][2] = 0.67; z_pT_Bin_Borders[2][43][3] = 0.93;
    Phi_h_Bin_Values[2][43][0] =  1; Phi_h_Bin_Values[2][43][1] = 755; Phi_h_Bin_Values[2][43][2] = 1485;
    z_pT_Bin_Borders[2][44][0] = 0.19; z_pT_Bin_Borders[2][44][1] = 0; z_pT_Bin_Borders[2][44][2] = 10; z_pT_Bin_Borders[2][44][3] = 0.93;
    Phi_h_Bin_Values[2][44][0] =  1; Phi_h_Bin_Values[2][44][1] = 756; Phi_h_Bin_Values[2][44][2] = 1486;
    z_pT_Bin_Borders[2][45][0] = 0.19; z_pT_Bin_Borders[2][45][1] = 0.23; z_pT_Bin_Borders[2][45][2] = 0.05; z_pT_Bin_Borders[2][45][3] = 0;
    Phi_h_Bin_Values[2][45][0] =  1; Phi_h_Bin_Values[2][45][1] = 757; Phi_h_Bin_Values[2][45][2] = 1487;
    z_pT_Bin_Borders[2][46][0] = 0.19; z_pT_Bin_Borders[2][46][1] = 0.23; z_pT_Bin_Borders[2][46][2] = 10; z_pT_Bin_Borders[2][46][3] = 0.93;
    Phi_h_Bin_Values[2][46][0] =  1; Phi_h_Bin_Values[2][46][1] = 758; Phi_h_Bin_Values[2][46][2] = 1488;
    z_pT_Bin_Borders[2][47][0] = 0.23; z_pT_Bin_Borders[2][47][1] = 0.26; z_pT_Bin_Borders[2][47][2] = 0.05; z_pT_Bin_Borders[2][47][3] = 0;
    Phi_h_Bin_Values[2][47][0] =  1; Phi_h_Bin_Values[2][47][1] = 759; Phi_h_Bin_Values[2][47][2] = 1489;
    z_pT_Bin_Borders[2][48][0] = 0.23; z_pT_Bin_Borders[2][48][1] = 0.26; z_pT_Bin_Borders[2][48][2] = 10; z_pT_Bin_Borders[2][48][3] = 0.93;
    Phi_h_Bin_Values[2][48][0] =  1; Phi_h_Bin_Values[2][48][1] = 760; Phi_h_Bin_Values[2][48][2] = 1490;
    z_pT_Bin_Borders[2][49][0] = 0.26; z_pT_Bin_Borders[2][49][1] = 0.31; z_pT_Bin_Borders[2][49][2] = 0.05; z_pT_Bin_Borders[2][49][3] = 0;
    Phi_h_Bin_Values[2][49][0] =  1; Phi_h_Bin_Values[2][49][1] = 761; Phi_h_Bin_Values[2][49][2] = 1491;
    z_pT_Bin_Borders[2][50][0] = 0.26; z_pT_Bin_Borders[2][50][1] = 0.31; z_pT_Bin_Borders[2][50][2] = 10; z_pT_Bin_Borders[2][50][3] = 0.93;
    Phi_h_Bin_Values[2][50][0] =  1; Phi_h_Bin_Values[2][50][1] = 762; Phi_h_Bin_Values[2][50][2] = 1492;
    z_pT_Bin_Borders[2][51][0] = 0.31; z_pT_Bin_Borders[2][51][1] = 0.38; z_pT_Bin_Borders[2][51][2] = 0.05; z_pT_Bin_Borders[2][51][3] = 0;
    Phi_h_Bin_Values[2][51][0] =  1; Phi_h_Bin_Values[2][51][1] = 763; Phi_h_Bin_Values[2][51][2] = 1493;
    z_pT_Bin_Borders[2][52][0] = 0.31; z_pT_Bin_Borders[2][52][1] = 0.38; z_pT_Bin_Borders[2][52][2] = 10; z_pT_Bin_Borders[2][52][3] = 0.93;
    Phi_h_Bin_Values[2][52][0] =  1; Phi_h_Bin_Values[2][52][1] = 764; Phi_h_Bin_Values[2][52][2] = 1494;
    z_pT_Bin_Borders[2][53][0] = 0.38; z_pT_Bin_Borders[2][53][1] = 0.5; z_pT_Bin_Borders[2][53][2] = 0.05; z_pT_Bin_Borders[2][53][3] = 0;
    Phi_h_Bin_Values[2][53][0] =  1; Phi_h_Bin_Values[2][53][1] = 765; Phi_h_Bin_Values[2][53][2] = 1495;
    z_pT_Bin_Borders[2][54][0] = 0.38; z_pT_Bin_Borders[2][54][1] = 0.5; z_pT_Bin_Borders[2][54][2] = 10; z_pT_Bin_Borders[2][54][3] = 0.93;
    Phi_h_Bin_Values[2][54][0] =  1; Phi_h_Bin_Values[2][54][1] = 766; Phi_h_Bin_Values[2][54][2] = 1496;
    z_pT_Bin_Borders[2][55][0] = 0.5; z_pT_Bin_Borders[2][55][1] = 0.75; z_pT_Bin_Borders[2][55][2] = 0.05; z_pT_Bin_Borders[2][55][3] = 0;
    Phi_h_Bin_Values[2][55][0] =  1; Phi_h_Bin_Values[2][55][1] = 767; Phi_h_Bin_Values[2][55][2] = 1497;
    z_pT_Bin_Borders[2][56][0] = 0.5; z_pT_Bin_Borders[2][56][1] = 0.75; z_pT_Bin_Borders[2][56][2] = 10; z_pT_Bin_Borders[2][56][3] = 0.93;
    Phi_h_Bin_Values[2][56][0] =  1; Phi_h_Bin_Values[2][56][1] = 768; Phi_h_Bin_Values[2][56][2] = 1498;
    z_pT_Bin_Borders[2][57][0] = 10; z_pT_Bin_Borders[2][57][1] = 0.75; z_pT_Bin_Borders[2][57][2] = 0; z_pT_Bin_Borders[2][57][3] = 0.05;
    Phi_h_Bin_Values[2][57][0] =  1; Phi_h_Bin_Values[2][57][1] = 769; Phi_h_Bin_Values[2][57][2] = 1499;
    z_pT_Bin_Borders[2][58][0] = 10; z_pT_Bin_Borders[2][58][1] = 0.75; z_pT_Bin_Borders[2][58][2] = 0.05; z_pT_Bin_Borders[2][58][3] = 0.25;
    Phi_h_Bin_Values[2][58][0] =  1; Phi_h_Bin_Values[2][58][1] = 770; Phi_h_Bin_Values[2][58][2] = 1500;
    z_pT_Bin_Borders[2][59][0] = 10; z_pT_Bin_Borders[2][59][1] = 0.75; z_pT_Bin_Borders[2][59][2] = 0.25; z_pT_Bin_Borders[2][59][3] = 0.35;
    Phi_h_Bin_Values[2][59][0] =  1; Phi_h_Bin_Values[2][59][1] = 771; Phi_h_Bin_Values[2][59][2] = 1501;
    z_pT_Bin_Borders[2][60][0] = 10; z_pT_Bin_Borders[2][60][1] = 0.75; z_pT_Bin_Borders[2][60][2] = 0.35; z_pT_Bin_Borders[2][60][3] = 0.45;
    Phi_h_Bin_Values[2][60][0] =  1; Phi_h_Bin_Values[2][60][1] = 772; Phi_h_Bin_Values[2][60][2] = 1502;
    z_pT_Bin_Borders[2][61][0] = 10; z_pT_Bin_Borders[2][61][1] = 0.75; z_pT_Bin_Borders[2][61][2] = 0.45; z_pT_Bin_Borders[2][61][3] = 0.54;
    Phi_h_Bin_Values[2][61][0] =  1; Phi_h_Bin_Values[2][61][1] = 773; Phi_h_Bin_Values[2][61][2] = 1503;
    z_pT_Bin_Borders[2][62][0] = 10; z_pT_Bin_Borders[2][62][1] = 0.75; z_pT_Bin_Borders[2][62][2] = 0.54; z_pT_Bin_Borders[2][62][3] = 0.67;
    Phi_h_Bin_Values[2][62][0] =  1; Phi_h_Bin_Values[2][62][1] = 774; Phi_h_Bin_Values[2][62][2] = 1504;
    z_pT_Bin_Borders[2][63][0] = 10; z_pT_Bin_Borders[2][63][1] = 0.75; z_pT_Bin_Borders[2][63][2] = 0.67; z_pT_Bin_Borders[2][63][3] = 0.93;
    Phi_h_Bin_Values[2][63][0] =  1; Phi_h_Bin_Values[2][63][1] = 775; Phi_h_Bin_Values[2][63][2] = 1505;
    z_pT_Bin_Borders[2][64][0] = 10; z_pT_Bin_Borders[2][64][1] = 0.75; z_pT_Bin_Borders[2][64][2] = 10; z_pT_Bin_Borders[2][64][3] = 0.93;
    Phi_h_Bin_Values[2][64][0] =  1; Phi_h_Bin_Values[2][64][1] = 776; Phi_h_Bin_Values[2][64][2] = 1506;
    z_pT_Bin_Borders[3][1][0] = 0.28; z_pT_Bin_Borders[3][1][1] = 0.22; z_pT_Bin_Borders[3][1][2] = 0.2; z_pT_Bin_Borders[3][1][3] = 0.05;
    Phi_h_Bin_Values[3][1][0] =  24; Phi_h_Bin_Values[3][1][1] = 0; Phi_h_Bin_Values[3][1][2] = 1507;
    z_pT_Bin_Borders[3][2][0] = 0.28; z_pT_Bin_Borders[3][2][1] = 0.22; z_pT_Bin_Borders[3][2][2] = 0.3; z_pT_Bin_Borders[3][2][3] = 0.2;
    Phi_h_Bin_Values[3][2][0] =  24; Phi_h_Bin_Values[3][2][1] = 24; Phi_h_Bin_Values[3][2][2] = 1531;
    z_pT_Bin_Borders[3][3][0] = 0.28; z_pT_Bin_Borders[3][3][1] = 0.22; z_pT_Bin_Borders[3][3][2] = 0.4; z_pT_Bin_Borders[3][3][3] = 0.3;
    Phi_h_Bin_Values[3][3][0] =  24; Phi_h_Bin_Values[3][3][1] = 48; Phi_h_Bin_Values[3][3][2] = 1555;
    z_pT_Bin_Borders[3][4][0] = 0.28; z_pT_Bin_Borders[3][4][1] = 0.22; z_pT_Bin_Borders[3][4][2] = 0.5; z_pT_Bin_Borders[3][4][3] = 0.4;
    Phi_h_Bin_Values[3][4][0] =  24; Phi_h_Bin_Values[3][4][1] = 72; Phi_h_Bin_Values[3][4][2] = 1579;
    z_pT_Bin_Borders[3][5][0] = 0.28; z_pT_Bin_Borders[3][5][1] = 0.22; z_pT_Bin_Borders[3][5][2] = 0.6; z_pT_Bin_Borders[3][5][3] = 0.5;
    Phi_h_Bin_Values[3][5][0] =  24; Phi_h_Bin_Values[3][5][1] = 96; Phi_h_Bin_Values[3][5][2] = 1603;
    z_pT_Bin_Borders[3][6][0] = 0.28; z_pT_Bin_Borders[3][6][1] = 0.22; z_pT_Bin_Borders[3][6][2] = 0.75; z_pT_Bin_Borders[3][6][3] = 0.6;
    Phi_h_Bin_Values[3][6][0] =  1; Phi_h_Bin_Values[3][6][1] = 120; Phi_h_Bin_Values[3][6][2] = 1627;
    z_pT_Bin_Borders[3][7][0] = 0.35; z_pT_Bin_Borders[3][7][1] = 0.28; z_pT_Bin_Borders[3][7][2] = 0.2; z_pT_Bin_Borders[3][7][3] = 0.05;
    Phi_h_Bin_Values[3][7][0] =  24; Phi_h_Bin_Values[3][7][1] = 121; Phi_h_Bin_Values[3][7][2] = 1628;
    z_pT_Bin_Borders[3][8][0] = 0.35; z_pT_Bin_Borders[3][8][1] = 0.28; z_pT_Bin_Borders[3][8][2] = 0.3; z_pT_Bin_Borders[3][8][3] = 0.2;
    Phi_h_Bin_Values[3][8][0] =  24; Phi_h_Bin_Values[3][8][1] = 145; Phi_h_Bin_Values[3][8][2] = 1652;
    z_pT_Bin_Borders[3][9][0] = 0.35; z_pT_Bin_Borders[3][9][1] = 0.28; z_pT_Bin_Borders[3][9][2] = 0.4; z_pT_Bin_Borders[3][9][3] = 0.3;
    Phi_h_Bin_Values[3][9][0] =  24; Phi_h_Bin_Values[3][9][1] = 169; Phi_h_Bin_Values[3][9][2] = 1676;
    z_pT_Bin_Borders[3][10][0] = 0.35; z_pT_Bin_Borders[3][10][1] = 0.28; z_pT_Bin_Borders[3][10][2] = 0.5; z_pT_Bin_Borders[3][10][3] = 0.4;
    Phi_h_Bin_Values[3][10][0] =  24; Phi_h_Bin_Values[3][10][1] = 193; Phi_h_Bin_Values[3][10][2] = 1700;
    z_pT_Bin_Borders[3][11][0] = 0.35; z_pT_Bin_Borders[3][11][1] = 0.28; z_pT_Bin_Borders[3][11][2] = 0.6; z_pT_Bin_Borders[3][11][3] = 0.5;
    Phi_h_Bin_Values[3][11][0] =  24; Phi_h_Bin_Values[3][11][1] = 217; Phi_h_Bin_Values[3][11][2] = 1724;
    z_pT_Bin_Borders[3][12][0] = 0.35; z_pT_Bin_Borders[3][12][1] = 0.28; z_pT_Bin_Borders[3][12][2] = 0.75; z_pT_Bin_Borders[3][12][3] = 0.6;
    Phi_h_Bin_Values[3][12][0] =  24; Phi_h_Bin_Values[3][12][1] = 241; Phi_h_Bin_Values[3][12][2] = 1748;
    z_pT_Bin_Borders[3][13][0] = 0.45; z_pT_Bin_Borders[3][13][1] = 0.35; z_pT_Bin_Borders[3][13][2] = 0.2; z_pT_Bin_Borders[3][13][3] = 0.05;
    Phi_h_Bin_Values[3][13][0] =  24; Phi_h_Bin_Values[3][13][1] = 265; Phi_h_Bin_Values[3][13][2] = 1772;
    z_pT_Bin_Borders[3][14][0] = 0.45; z_pT_Bin_Borders[3][14][1] = 0.35; z_pT_Bin_Borders[3][14][2] = 0.3; z_pT_Bin_Borders[3][14][3] = 0.2;
    Phi_h_Bin_Values[3][14][0] =  24; Phi_h_Bin_Values[3][14][1] = 289; Phi_h_Bin_Values[3][14][2] = 1796;
    z_pT_Bin_Borders[3][15][0] = 0.45; z_pT_Bin_Borders[3][15][1] = 0.35; z_pT_Bin_Borders[3][15][2] = 0.4; z_pT_Bin_Borders[3][15][3] = 0.3;
    Phi_h_Bin_Values[3][15][0] =  24; Phi_h_Bin_Values[3][15][1] = 313; Phi_h_Bin_Values[3][15][2] = 1820;
    z_pT_Bin_Borders[3][16][0] = 0.45; z_pT_Bin_Borders[3][16][1] = 0.35; z_pT_Bin_Borders[3][16][2] = 0.5; z_pT_Bin_Borders[3][16][3] = 0.4;
    Phi_h_Bin_Values[3][16][0] =  24; Phi_h_Bin_Values[3][16][1] = 337; Phi_h_Bin_Values[3][16][2] = 1844;
    z_pT_Bin_Borders[3][17][0] = 0.45; z_pT_Bin_Borders[3][17][1] = 0.35; z_pT_Bin_Borders[3][17][2] = 0.6; z_pT_Bin_Borders[3][17][3] = 0.5;
    Phi_h_Bin_Values[3][17][0] =  24; Phi_h_Bin_Values[3][17][1] = 361; Phi_h_Bin_Values[3][17][2] = 1868;
    z_pT_Bin_Borders[3][18][0] = 0.45; z_pT_Bin_Borders[3][18][1] = 0.35; z_pT_Bin_Borders[3][18][2] = 0.75; z_pT_Bin_Borders[3][18][3] = 0.6;
    Phi_h_Bin_Values[3][18][0] =  24; Phi_h_Bin_Values[3][18][1] = 385; Phi_h_Bin_Values[3][18][2] = 1892;
    z_pT_Bin_Borders[3][19][0] = 0.7; z_pT_Bin_Borders[3][19][1] = 0.45; z_pT_Bin_Borders[3][19][2] = 0.2; z_pT_Bin_Borders[3][19][3] = 0.05;
    Phi_h_Bin_Values[3][19][0] =  24; Phi_h_Bin_Values[3][19][1] = 409; Phi_h_Bin_Values[3][19][2] = 1916;
    z_pT_Bin_Borders[3][20][0] = 0.7; z_pT_Bin_Borders[3][20][1] = 0.45; z_pT_Bin_Borders[3][20][2] = 0.3; z_pT_Bin_Borders[3][20][3] = 0.2;
    Phi_h_Bin_Values[3][20][0] =  24; Phi_h_Bin_Values[3][20][1] = 433; Phi_h_Bin_Values[3][20][2] = 1940;
    z_pT_Bin_Borders[3][21][0] = 0.7; z_pT_Bin_Borders[3][21][1] = 0.45; z_pT_Bin_Borders[3][21][2] = 0.4; z_pT_Bin_Borders[3][21][3] = 0.3;
    Phi_h_Bin_Values[3][21][0] =  24; Phi_h_Bin_Values[3][21][1] = 457; Phi_h_Bin_Values[3][21][2] = 1964;
    z_pT_Bin_Borders[3][22][0] = 0.7; z_pT_Bin_Borders[3][22][1] = 0.45; z_pT_Bin_Borders[3][22][2] = 0.5; z_pT_Bin_Borders[3][22][3] = 0.4;
    Phi_h_Bin_Values[3][22][0] =  24; Phi_h_Bin_Values[3][22][1] = 481; Phi_h_Bin_Values[3][22][2] = 1988;
    z_pT_Bin_Borders[3][23][0] = 0.7; z_pT_Bin_Borders[3][23][1] = 0.45; z_pT_Bin_Borders[3][23][2] = 0.6; z_pT_Bin_Borders[3][23][3] = 0.5;
    Phi_h_Bin_Values[3][23][0] =  24; Phi_h_Bin_Values[3][23][1] = 505; Phi_h_Bin_Values[3][23][2] = 2012;
    z_pT_Bin_Borders[3][24][0] = 0.7; z_pT_Bin_Borders[3][24][1] = 0.45; z_pT_Bin_Borders[3][24][2] = 0.75; z_pT_Bin_Borders[3][24][3] = 0.6;
    Phi_h_Bin_Values[3][24][0] =  1; Phi_h_Bin_Values[3][24][1] = 529; Phi_h_Bin_Values[3][24][2] = 2036;
    z_pT_Bin_Borders[3][25][0] = 0.22; z_pT_Bin_Borders[3][25][1] = 0; z_pT_Bin_Borders[3][25][2] = 0.05; z_pT_Bin_Borders[3][25][3] = 0;
    Phi_h_Bin_Values[3][25][0] =  1; Phi_h_Bin_Values[3][25][1] = 530; Phi_h_Bin_Values[3][25][2] = 2037;
    z_pT_Bin_Borders[3][26][0] = 0.22; z_pT_Bin_Borders[3][26][1] = 0; z_pT_Bin_Borders[3][26][2] = 0.05; z_pT_Bin_Borders[3][26][3] = 0.2;
    Phi_h_Bin_Values[3][26][0] =  1; Phi_h_Bin_Values[3][26][1] = 531; Phi_h_Bin_Values[3][26][2] = 2038;
    z_pT_Bin_Borders[3][27][0] = 0.22; z_pT_Bin_Borders[3][27][1] = 0; z_pT_Bin_Borders[3][27][2] = 0.2; z_pT_Bin_Borders[3][27][3] = 0.3;
    Phi_h_Bin_Values[3][27][0] =  1; Phi_h_Bin_Values[3][27][1] = 532; Phi_h_Bin_Values[3][27][2] = 2039;
    z_pT_Bin_Borders[3][28][0] = 0.22; z_pT_Bin_Borders[3][28][1] = 0; z_pT_Bin_Borders[3][28][2] = 0.3; z_pT_Bin_Borders[3][28][3] = 0.4;
    Phi_h_Bin_Values[3][28][0] =  1; Phi_h_Bin_Values[3][28][1] = 533; Phi_h_Bin_Values[3][28][2] = 2040;
    z_pT_Bin_Borders[3][29][0] = 0.22; z_pT_Bin_Borders[3][29][1] = 0; z_pT_Bin_Borders[3][29][2] = 0.4; z_pT_Bin_Borders[3][29][3] = 0.5;
    Phi_h_Bin_Values[3][29][0] =  1; Phi_h_Bin_Values[3][29][1] = 534; Phi_h_Bin_Values[3][29][2] = 2041;
    z_pT_Bin_Borders[3][30][0] = 0.22; z_pT_Bin_Borders[3][30][1] = 0; z_pT_Bin_Borders[3][30][2] = 0.5; z_pT_Bin_Borders[3][30][3] = 0.6;
    Phi_h_Bin_Values[3][30][0] =  1; Phi_h_Bin_Values[3][30][1] = 535; Phi_h_Bin_Values[3][30][2] = 2042;
    z_pT_Bin_Borders[3][31][0] = 0.22; z_pT_Bin_Borders[3][31][1] = 0; z_pT_Bin_Borders[3][31][2] = 0.6; z_pT_Bin_Borders[3][31][3] = 0.75;
    Phi_h_Bin_Values[3][31][0] =  1; Phi_h_Bin_Values[3][31][1] = 536; Phi_h_Bin_Values[3][31][2] = 2043;
    z_pT_Bin_Borders[3][32][0] = 0.22; z_pT_Bin_Borders[3][32][1] = 0; z_pT_Bin_Borders[3][32][2] = 10; z_pT_Bin_Borders[3][32][3] = 0.75;
    Phi_h_Bin_Values[3][32][0] =  1; Phi_h_Bin_Values[3][32][1] = 537; Phi_h_Bin_Values[3][32][2] = 2044;
    z_pT_Bin_Borders[3][33][0] = 0.22; z_pT_Bin_Borders[3][33][1] = 0.28; z_pT_Bin_Borders[3][33][2] = 0.05; z_pT_Bin_Borders[3][33][3] = 0;
    Phi_h_Bin_Values[3][33][0] =  1; Phi_h_Bin_Values[3][33][1] = 538; Phi_h_Bin_Values[3][33][2] = 2045;
    z_pT_Bin_Borders[3][34][0] = 0.22; z_pT_Bin_Borders[3][34][1] = 0.28; z_pT_Bin_Borders[3][34][2] = 10; z_pT_Bin_Borders[3][34][3] = 0.75;
    Phi_h_Bin_Values[3][34][0] =  1; Phi_h_Bin_Values[3][34][1] = 539; Phi_h_Bin_Values[3][34][2] = 2046;
    z_pT_Bin_Borders[3][35][0] = 0.28; z_pT_Bin_Borders[3][35][1] = 0.35; z_pT_Bin_Borders[3][35][2] = 0.05; z_pT_Bin_Borders[3][35][3] = 0;
    Phi_h_Bin_Values[3][35][0] =  1; Phi_h_Bin_Values[3][35][1] = 540; Phi_h_Bin_Values[3][35][2] = 2047;
    z_pT_Bin_Borders[3][36][0] = 0.28; z_pT_Bin_Borders[3][36][1] = 0.35; z_pT_Bin_Borders[3][36][2] = 10; z_pT_Bin_Borders[3][36][3] = 0.75;
    Phi_h_Bin_Values[3][36][0] =  1; Phi_h_Bin_Values[3][36][1] = 541; Phi_h_Bin_Values[3][36][2] = 2048;
    z_pT_Bin_Borders[3][37][0] = 0.35; z_pT_Bin_Borders[3][37][1] = 0.45; z_pT_Bin_Borders[3][37][2] = 0.05; z_pT_Bin_Borders[3][37][3] = 0;
    Phi_h_Bin_Values[3][37][0] =  1; Phi_h_Bin_Values[3][37][1] = 542; Phi_h_Bin_Values[3][37][2] = 2049;
    z_pT_Bin_Borders[3][38][0] = 0.35; z_pT_Bin_Borders[3][38][1] = 0.45; z_pT_Bin_Borders[3][38][2] = 10; z_pT_Bin_Borders[3][38][3] = 0.75;
    Phi_h_Bin_Values[3][38][0] =  1; Phi_h_Bin_Values[3][38][1] = 543; Phi_h_Bin_Values[3][38][2] = 2050;
    z_pT_Bin_Borders[3][39][0] = 0.45; z_pT_Bin_Borders[3][39][1] = 0.7; z_pT_Bin_Borders[3][39][2] = 0.05; z_pT_Bin_Borders[3][39][3] = 0;
    Phi_h_Bin_Values[3][39][0] =  1; Phi_h_Bin_Values[3][39][1] = 544; Phi_h_Bin_Values[3][39][2] = 2051;
    z_pT_Bin_Borders[3][40][0] = 0.45; z_pT_Bin_Borders[3][40][1] = 0.7; z_pT_Bin_Borders[3][40][2] = 10; z_pT_Bin_Borders[3][40][3] = 0.75;
    Phi_h_Bin_Values[3][40][0] =  1; Phi_h_Bin_Values[3][40][1] = 545; Phi_h_Bin_Values[3][40][2] = 2052;
    z_pT_Bin_Borders[3][41][0] = 10; z_pT_Bin_Borders[3][41][1] = 0.7; z_pT_Bin_Borders[3][41][2] = 0; z_pT_Bin_Borders[3][41][3] = 0.05;
    Phi_h_Bin_Values[3][41][0] =  1; Phi_h_Bin_Values[3][41][1] = 546; Phi_h_Bin_Values[3][41][2] = 2053;
    z_pT_Bin_Borders[3][42][0] = 10; z_pT_Bin_Borders[3][42][1] = 0.7; z_pT_Bin_Borders[3][42][2] = 0.05; z_pT_Bin_Borders[3][42][3] = 0.2;
    Phi_h_Bin_Values[3][42][0] =  1; Phi_h_Bin_Values[3][42][1] = 547; Phi_h_Bin_Values[3][42][2] = 2054;
    z_pT_Bin_Borders[3][43][0] = 10; z_pT_Bin_Borders[3][43][1] = 0.7; z_pT_Bin_Borders[3][43][2] = 0.2; z_pT_Bin_Borders[3][43][3] = 0.3;
    Phi_h_Bin_Values[3][43][0] =  1; Phi_h_Bin_Values[3][43][1] = 548; Phi_h_Bin_Values[3][43][2] = 2055;
    z_pT_Bin_Borders[3][44][0] = 10; z_pT_Bin_Borders[3][44][1] = 0.7; z_pT_Bin_Borders[3][44][2] = 0.3; z_pT_Bin_Borders[3][44][3] = 0.4;
    Phi_h_Bin_Values[3][44][0] =  1; Phi_h_Bin_Values[3][44][1] = 549; Phi_h_Bin_Values[3][44][2] = 2056;
    z_pT_Bin_Borders[3][45][0] = 10; z_pT_Bin_Borders[3][45][1] = 0.7; z_pT_Bin_Borders[3][45][2] = 0.4; z_pT_Bin_Borders[3][45][3] = 0.5;
    Phi_h_Bin_Values[3][45][0] =  1; Phi_h_Bin_Values[3][45][1] = 550; Phi_h_Bin_Values[3][45][2] = 2057;
    z_pT_Bin_Borders[3][46][0] = 10; z_pT_Bin_Borders[3][46][1] = 0.7; z_pT_Bin_Borders[3][46][2] = 0.5; z_pT_Bin_Borders[3][46][3] = 0.6;
    Phi_h_Bin_Values[3][46][0] =  1; Phi_h_Bin_Values[3][46][1] = 551; Phi_h_Bin_Values[3][46][2] = 2058;
    z_pT_Bin_Borders[3][47][0] = 10; z_pT_Bin_Borders[3][47][1] = 0.7; z_pT_Bin_Borders[3][47][2] = 0.6; z_pT_Bin_Borders[3][47][3] = 0.75;
    Phi_h_Bin_Values[3][47][0] =  1; Phi_h_Bin_Values[3][47][1] = 552; Phi_h_Bin_Values[3][47][2] = 2059;
    z_pT_Bin_Borders[3][48][0] = 10; z_pT_Bin_Borders[3][48][1] = 0.7; z_pT_Bin_Borders[3][48][2] = 10; z_pT_Bin_Borders[3][48][3] = 0.75;
    Phi_h_Bin_Values[3][48][0] =  1; Phi_h_Bin_Values[3][48][1] = 553; Phi_h_Bin_Values[3][48][2] = 2060;
    z_pT_Bin_Borders[4][1][0] = 0.34; z_pT_Bin_Borders[4][1][1] = 0.26; z_pT_Bin_Borders[4][1][2] = 0.2; z_pT_Bin_Borders[4][1][3] = 0.05;
    Phi_h_Bin_Values[4][1][0] =  24; Phi_h_Bin_Values[4][1][1] = 0; Phi_h_Bin_Values[4][1][2] = 2061;
    z_pT_Bin_Borders[4][2][0] = 0.34; z_pT_Bin_Borders[4][2][1] = 0.26; z_pT_Bin_Borders[4][2][2] = 0.29; z_pT_Bin_Borders[4][2][3] = 0.2;
    Phi_h_Bin_Values[4][2][0] =  24; Phi_h_Bin_Values[4][2][1] = 24; Phi_h_Bin_Values[4][2][2] = 2085;
    z_pT_Bin_Borders[4][3][0] = 0.34; z_pT_Bin_Borders[4][3][1] = 0.26; z_pT_Bin_Borders[4][3][2] = 0.38; z_pT_Bin_Borders[4][3][3] = 0.29;
    Phi_h_Bin_Values[4][3][0] =  24; Phi_h_Bin_Values[4][3][1] = 48; Phi_h_Bin_Values[4][3][2] = 2109;
    z_pT_Bin_Borders[4][4][0] = 0.34; z_pT_Bin_Borders[4][4][1] = 0.26; z_pT_Bin_Borders[4][4][2] = 0.48; z_pT_Bin_Borders[4][4][3] = 0.38;
    Phi_h_Bin_Values[4][4][0] =  24; Phi_h_Bin_Values[4][4][1] = 72; Phi_h_Bin_Values[4][4][2] = 2133;
    z_pT_Bin_Borders[4][5][0] = 0.34; z_pT_Bin_Borders[4][5][1] = 0.26; z_pT_Bin_Borders[4][5][2] = 0.61; z_pT_Bin_Borders[4][5][3] = 0.48;
    Phi_h_Bin_Values[4][5][0] =  24; Phi_h_Bin_Values[4][5][1] = 96; Phi_h_Bin_Values[4][5][2] = 2157;
    z_pT_Bin_Borders[4][6][0] = 0.38; z_pT_Bin_Borders[4][6][1] = 0.34; z_pT_Bin_Borders[4][6][2] = 0.2; z_pT_Bin_Borders[4][6][3] = 0.05;
    Phi_h_Bin_Values[4][6][0] =  24; Phi_h_Bin_Values[4][6][1] = 120; Phi_h_Bin_Values[4][6][2] = 2181;
    z_pT_Bin_Borders[4][7][0] = 0.38; z_pT_Bin_Borders[4][7][1] = 0.34; z_pT_Bin_Borders[4][7][2] = 0.29; z_pT_Bin_Borders[4][7][3] = 0.2;
    Phi_h_Bin_Values[4][7][0] =  24; Phi_h_Bin_Values[4][7][1] = 144; Phi_h_Bin_Values[4][7][2] = 2205;
    z_pT_Bin_Borders[4][8][0] = 0.38; z_pT_Bin_Borders[4][8][1] = 0.34; z_pT_Bin_Borders[4][8][2] = 0.38; z_pT_Bin_Borders[4][8][3] = 0.29;
    Phi_h_Bin_Values[4][8][0] =  24; Phi_h_Bin_Values[4][8][1] = 168; Phi_h_Bin_Values[4][8][2] = 2229;
    z_pT_Bin_Borders[4][9][0] = 0.38; z_pT_Bin_Borders[4][9][1] = 0.34; z_pT_Bin_Borders[4][9][2] = 0.48; z_pT_Bin_Borders[4][9][3] = 0.38;
    Phi_h_Bin_Values[4][9][0] =  24; Phi_h_Bin_Values[4][9][1] = 192; Phi_h_Bin_Values[4][9][2] = 2253;
    z_pT_Bin_Borders[4][10][0] = 0.38; z_pT_Bin_Borders[4][10][1] = 0.34; z_pT_Bin_Borders[4][10][2] = 0.61; z_pT_Bin_Borders[4][10][3] = 0.48;
    Phi_h_Bin_Values[4][10][0] =  24; Phi_h_Bin_Values[4][10][1] = 216; Phi_h_Bin_Values[4][10][2] = 2277;
    z_pT_Bin_Borders[4][11][0] = 0.43; z_pT_Bin_Borders[4][11][1] = 0.38; z_pT_Bin_Borders[4][11][2] = 0.2; z_pT_Bin_Borders[4][11][3] = 0.05;
    Phi_h_Bin_Values[4][11][0] =  24; Phi_h_Bin_Values[4][11][1] = 240; Phi_h_Bin_Values[4][11][2] = 2301;
    z_pT_Bin_Borders[4][12][0] = 0.43; z_pT_Bin_Borders[4][12][1] = 0.38; z_pT_Bin_Borders[4][12][2] = 0.29; z_pT_Bin_Borders[4][12][3] = 0.2;
    Phi_h_Bin_Values[4][12][0] =  24; Phi_h_Bin_Values[4][12][1] = 264; Phi_h_Bin_Values[4][12][2] = 2325;
    z_pT_Bin_Borders[4][13][0] = 0.43; z_pT_Bin_Borders[4][13][1] = 0.38; z_pT_Bin_Borders[4][13][2] = 0.38; z_pT_Bin_Borders[4][13][3] = 0.29;
    Phi_h_Bin_Values[4][13][0] =  24; Phi_h_Bin_Values[4][13][1] = 288; Phi_h_Bin_Values[4][13][2] = 2349;
    z_pT_Bin_Borders[4][14][0] = 0.43; z_pT_Bin_Borders[4][14][1] = 0.38; z_pT_Bin_Borders[4][14][2] = 0.48; z_pT_Bin_Borders[4][14][3] = 0.38;
    Phi_h_Bin_Values[4][14][0] =  24; Phi_h_Bin_Values[4][14][1] = 312; Phi_h_Bin_Values[4][14][2] = 2373;
    z_pT_Bin_Borders[4][15][0] = 0.43; z_pT_Bin_Borders[4][15][1] = 0.38; z_pT_Bin_Borders[4][15][2] = 0.61; z_pT_Bin_Borders[4][15][3] = 0.48;
    Phi_h_Bin_Values[4][15][0] =  24; Phi_h_Bin_Values[4][15][1] = 336; Phi_h_Bin_Values[4][15][2] = 2397;
    z_pT_Bin_Borders[4][16][0] = 0.5; z_pT_Bin_Borders[4][16][1] = 0.43; z_pT_Bin_Borders[4][16][2] = 0.2; z_pT_Bin_Borders[4][16][3] = 0.05;
    Phi_h_Bin_Values[4][16][0] =  24; Phi_h_Bin_Values[4][16][1] = 360; Phi_h_Bin_Values[4][16][2] = 2421;
    z_pT_Bin_Borders[4][17][0] = 0.5; z_pT_Bin_Borders[4][17][1] = 0.43; z_pT_Bin_Borders[4][17][2] = 0.29; z_pT_Bin_Borders[4][17][3] = 0.2;
    Phi_h_Bin_Values[4][17][0] =  24; Phi_h_Bin_Values[4][17][1] = 384; Phi_h_Bin_Values[4][17][2] = 2445;
    z_pT_Bin_Borders[4][18][0] = 0.5; z_pT_Bin_Borders[4][18][1] = 0.43; z_pT_Bin_Borders[4][18][2] = 0.38; z_pT_Bin_Borders[4][18][3] = 0.29;
    Phi_h_Bin_Values[4][18][0] =  24; Phi_h_Bin_Values[4][18][1] = 408; Phi_h_Bin_Values[4][18][2] = 2469;
    z_pT_Bin_Borders[4][19][0] = 0.5; z_pT_Bin_Borders[4][19][1] = 0.43; z_pT_Bin_Borders[4][19][2] = 0.48; z_pT_Bin_Borders[4][19][3] = 0.38;
    Phi_h_Bin_Values[4][19][0] =  24; Phi_h_Bin_Values[4][19][1] = 432; Phi_h_Bin_Values[4][19][2] = 2493;
    z_pT_Bin_Borders[4][20][0] = 0.5; z_pT_Bin_Borders[4][20][1] = 0.43; z_pT_Bin_Borders[4][20][2] = 0.61; z_pT_Bin_Borders[4][20][3] = 0.48;
    Phi_h_Bin_Values[4][20][0] =  24; Phi_h_Bin_Values[4][20][1] = 456; Phi_h_Bin_Values[4][20][2] = 2517;
    z_pT_Bin_Borders[4][21][0] = 0.6; z_pT_Bin_Borders[4][21][1] = 0.5; z_pT_Bin_Borders[4][21][2] = 0.2; z_pT_Bin_Borders[4][21][3] = 0.05;
    Phi_h_Bin_Values[4][21][0] =  24; Phi_h_Bin_Values[4][21][1] = 480; Phi_h_Bin_Values[4][21][2] = 2541;
    z_pT_Bin_Borders[4][22][0] = 0.6; z_pT_Bin_Borders[4][22][1] = 0.5; z_pT_Bin_Borders[4][22][2] = 0.29; z_pT_Bin_Borders[4][22][3] = 0.2;
    Phi_h_Bin_Values[4][22][0] =  24; Phi_h_Bin_Values[4][22][1] = 504; Phi_h_Bin_Values[4][22][2] = 2565;
    z_pT_Bin_Borders[4][23][0] = 0.6; z_pT_Bin_Borders[4][23][1] = 0.5; z_pT_Bin_Borders[4][23][2] = 0.38; z_pT_Bin_Borders[4][23][3] = 0.29;
    Phi_h_Bin_Values[4][23][0] =  24; Phi_h_Bin_Values[4][23][1] = 528; Phi_h_Bin_Values[4][23][2] = 2589;
    z_pT_Bin_Borders[4][24][0] = 0.6; z_pT_Bin_Borders[4][24][1] = 0.5; z_pT_Bin_Borders[4][24][2] = 0.48; z_pT_Bin_Borders[4][24][3] = 0.38;
    Phi_h_Bin_Values[4][24][0] =  24; Phi_h_Bin_Values[4][24][1] = 552; Phi_h_Bin_Values[4][24][2] = 2613;
    z_pT_Bin_Borders[4][25][0] = 0.6; z_pT_Bin_Borders[4][25][1] = 0.5; z_pT_Bin_Borders[4][25][2] = 0.61; z_pT_Bin_Borders[4][25][3] = 0.48;
    Phi_h_Bin_Values[4][25][0] =  1; Phi_h_Bin_Values[4][25][1] = 576; Phi_h_Bin_Values[4][25][2] = 2637;
    z_pT_Bin_Borders[4][26][0] = 0.26; z_pT_Bin_Borders[4][26][1] = 0; z_pT_Bin_Borders[4][26][2] = 0.05; z_pT_Bin_Borders[4][26][3] = 0;
    Phi_h_Bin_Values[4][26][0] =  1; Phi_h_Bin_Values[4][26][1] = 577; Phi_h_Bin_Values[4][26][2] = 2638;
    z_pT_Bin_Borders[4][27][0] = 0.26; z_pT_Bin_Borders[4][27][1] = 0; z_pT_Bin_Borders[4][27][2] = 0.05; z_pT_Bin_Borders[4][27][3] = 0.2;
    Phi_h_Bin_Values[4][27][0] =  1; Phi_h_Bin_Values[4][27][1] = 578; Phi_h_Bin_Values[4][27][2] = 2639;
    z_pT_Bin_Borders[4][28][0] = 0.26; z_pT_Bin_Borders[4][28][1] = 0; z_pT_Bin_Borders[4][28][2] = 0.2; z_pT_Bin_Borders[4][28][3] = 0.29;
    Phi_h_Bin_Values[4][28][0] =  1; Phi_h_Bin_Values[4][28][1] = 579; Phi_h_Bin_Values[4][28][2] = 2640;
    z_pT_Bin_Borders[4][29][0] = 0.26; z_pT_Bin_Borders[4][29][1] = 0; z_pT_Bin_Borders[4][29][2] = 0.29; z_pT_Bin_Borders[4][29][3] = 0.38;
    Phi_h_Bin_Values[4][29][0] =  1; Phi_h_Bin_Values[4][29][1] = 580; Phi_h_Bin_Values[4][29][2] = 2641;
    z_pT_Bin_Borders[4][30][0] = 0.26; z_pT_Bin_Borders[4][30][1] = 0; z_pT_Bin_Borders[4][30][2] = 0.38; z_pT_Bin_Borders[4][30][3] = 0.48;
    Phi_h_Bin_Values[4][30][0] =  1; Phi_h_Bin_Values[4][30][1] = 581; Phi_h_Bin_Values[4][30][2] = 2642;
    z_pT_Bin_Borders[4][31][0] = 0.26; z_pT_Bin_Borders[4][31][1] = 0; z_pT_Bin_Borders[4][31][2] = 0.48; z_pT_Bin_Borders[4][31][3] = 0.61;
    Phi_h_Bin_Values[4][31][0] =  1; Phi_h_Bin_Values[4][31][1] = 582; Phi_h_Bin_Values[4][31][2] = 2643;
    z_pT_Bin_Borders[4][32][0] = 0.26; z_pT_Bin_Borders[4][32][1] = 0; z_pT_Bin_Borders[4][32][2] = 10; z_pT_Bin_Borders[4][32][3] = 0.61;
    Phi_h_Bin_Values[4][32][0] =  1; Phi_h_Bin_Values[4][32][1] = 583; Phi_h_Bin_Values[4][32][2] = 2644;
    z_pT_Bin_Borders[4][33][0] = 0.26; z_pT_Bin_Borders[4][33][1] = 0.34; z_pT_Bin_Borders[4][33][2] = 0.05; z_pT_Bin_Borders[4][33][3] = 0;
    Phi_h_Bin_Values[4][33][0] =  1; Phi_h_Bin_Values[4][33][1] = 584; Phi_h_Bin_Values[4][33][2] = 2645;
    z_pT_Bin_Borders[4][34][0] = 0.26; z_pT_Bin_Borders[4][34][1] = 0.34; z_pT_Bin_Borders[4][34][2] = 10; z_pT_Bin_Borders[4][34][3] = 0.61;
    Phi_h_Bin_Values[4][34][0] =  1; Phi_h_Bin_Values[4][34][1] = 585; Phi_h_Bin_Values[4][34][2] = 2646;
    z_pT_Bin_Borders[4][35][0] = 0.34; z_pT_Bin_Borders[4][35][1] = 0.38; z_pT_Bin_Borders[4][35][2] = 0.05; z_pT_Bin_Borders[4][35][3] = 0;
    Phi_h_Bin_Values[4][35][0] =  1; Phi_h_Bin_Values[4][35][1] = 586; Phi_h_Bin_Values[4][35][2] = 2647;
    z_pT_Bin_Borders[4][36][0] = 0.34; z_pT_Bin_Borders[4][36][1] = 0.38; z_pT_Bin_Borders[4][36][2] = 10; z_pT_Bin_Borders[4][36][3] = 0.61;
    Phi_h_Bin_Values[4][36][0] =  1; Phi_h_Bin_Values[4][36][1] = 587; Phi_h_Bin_Values[4][36][2] = 2648;
    z_pT_Bin_Borders[4][37][0] = 0.38; z_pT_Bin_Borders[4][37][1] = 0.43; z_pT_Bin_Borders[4][37][2] = 0.05; z_pT_Bin_Borders[4][37][3] = 0;
    Phi_h_Bin_Values[4][37][0] =  1; Phi_h_Bin_Values[4][37][1] = 588; Phi_h_Bin_Values[4][37][2] = 2649;
    z_pT_Bin_Borders[4][38][0] = 0.38; z_pT_Bin_Borders[4][38][1] = 0.43; z_pT_Bin_Borders[4][38][2] = 10; z_pT_Bin_Borders[4][38][3] = 0.61;
    Phi_h_Bin_Values[4][38][0] =  1; Phi_h_Bin_Values[4][38][1] = 589; Phi_h_Bin_Values[4][38][2] = 2650;
    z_pT_Bin_Borders[4][39][0] = 0.43; z_pT_Bin_Borders[4][39][1] = 0.5; z_pT_Bin_Borders[4][39][2] = 0.05; z_pT_Bin_Borders[4][39][3] = 0;
    Phi_h_Bin_Values[4][39][0] =  1; Phi_h_Bin_Values[4][39][1] = 590; Phi_h_Bin_Values[4][39][2] = 2651;
    z_pT_Bin_Borders[4][40][0] = 0.43; z_pT_Bin_Borders[4][40][1] = 0.5; z_pT_Bin_Borders[4][40][2] = 10; z_pT_Bin_Borders[4][40][3] = 0.61;
    Phi_h_Bin_Values[4][40][0] =  1; Phi_h_Bin_Values[4][40][1] = 591; Phi_h_Bin_Values[4][40][2] = 2652;
    z_pT_Bin_Borders[4][41][0] = 0.5; z_pT_Bin_Borders[4][41][1] = 0.6; z_pT_Bin_Borders[4][41][2] = 0.05; z_pT_Bin_Borders[4][41][3] = 0;
    Phi_h_Bin_Values[4][41][0] =  1; Phi_h_Bin_Values[4][41][1] = 592; Phi_h_Bin_Values[4][41][2] = 2653;
    z_pT_Bin_Borders[4][42][0] = 0.5; z_pT_Bin_Borders[4][42][1] = 0.6; z_pT_Bin_Borders[4][42][2] = 10; z_pT_Bin_Borders[4][42][3] = 0.61;
    Phi_h_Bin_Values[4][42][0] =  1; Phi_h_Bin_Values[4][42][1] = 593; Phi_h_Bin_Values[4][42][2] = 2654;
    z_pT_Bin_Borders[4][43][0] = 10; z_pT_Bin_Borders[4][43][1] = 0.6; z_pT_Bin_Borders[4][43][2] = 0; z_pT_Bin_Borders[4][43][3] = 0.05;
    Phi_h_Bin_Values[4][43][0] =  1; Phi_h_Bin_Values[4][43][1] = 594; Phi_h_Bin_Values[4][43][2] = 2655;
    z_pT_Bin_Borders[4][44][0] = 10; z_pT_Bin_Borders[4][44][1] = 0.6; z_pT_Bin_Borders[4][44][2] = 0.05; z_pT_Bin_Borders[4][44][3] = 0.2;
    Phi_h_Bin_Values[4][44][0] =  1; Phi_h_Bin_Values[4][44][1] = 595; Phi_h_Bin_Values[4][44][2] = 2656;
    z_pT_Bin_Borders[4][45][0] = 10; z_pT_Bin_Borders[4][45][1] = 0.6; z_pT_Bin_Borders[4][45][2] = 0.2; z_pT_Bin_Borders[4][45][3] = 0.29;
    Phi_h_Bin_Values[4][45][0] =  1; Phi_h_Bin_Values[4][45][1] = 596; Phi_h_Bin_Values[4][45][2] = 2657;
    z_pT_Bin_Borders[4][46][0] = 10; z_pT_Bin_Borders[4][46][1] = 0.6; z_pT_Bin_Borders[4][46][2] = 0.29; z_pT_Bin_Borders[4][46][3] = 0.38;
    Phi_h_Bin_Values[4][46][0] =  1; Phi_h_Bin_Values[4][46][1] = 597; Phi_h_Bin_Values[4][46][2] = 2658;
    z_pT_Bin_Borders[4][47][0] = 10; z_pT_Bin_Borders[4][47][1] = 0.6; z_pT_Bin_Borders[4][47][2] = 0.38; z_pT_Bin_Borders[4][47][3] = 0.48;
    Phi_h_Bin_Values[4][47][0] =  1; Phi_h_Bin_Values[4][47][1] = 598; Phi_h_Bin_Values[4][47][2] = 2659;
    z_pT_Bin_Borders[4][48][0] = 10; z_pT_Bin_Borders[4][48][1] = 0.6; z_pT_Bin_Borders[4][48][2] = 0.48; z_pT_Bin_Borders[4][48][3] = 0.61;
    Phi_h_Bin_Values[4][48][0] =  1; Phi_h_Bin_Values[4][48][1] = 599; Phi_h_Bin_Values[4][48][2] = 2660;
    z_pT_Bin_Borders[4][49][0] = 10; z_pT_Bin_Borders[4][49][1] = 0.6; z_pT_Bin_Borders[4][49][2] = 10; z_pT_Bin_Borders[4][49][3] = 0.61;
    Phi_h_Bin_Values[4][49][0] =  1; Phi_h_Bin_Values[4][49][1] = 600; Phi_h_Bin_Values[4][49][2] = 2661;
    z_pT_Bin_Borders[5][1][0] = 0.2; z_pT_Bin_Borders[5][1][1] = 0.16; z_pT_Bin_Borders[5][1][2] = 0.22; z_pT_Bin_Borders[5][1][3] = 0.05;
    Phi_h_Bin_Values[5][1][0] =  24; Phi_h_Bin_Values[5][1][1] = 0; Phi_h_Bin_Values[5][1][2] = 2662;
    z_pT_Bin_Borders[5][2][0] = 0.2; z_pT_Bin_Borders[5][2][1] = 0.16; z_pT_Bin_Borders[5][2][2] = 0.32; z_pT_Bin_Borders[5][2][3] = 0.22;
    Phi_h_Bin_Values[5][2][0] =  24; Phi_h_Bin_Values[5][2][1] = 24; Phi_h_Bin_Values[5][2][2] = 2686;
    z_pT_Bin_Borders[5][3][0] = 0.2; z_pT_Bin_Borders[5][3][1] = 0.16; z_pT_Bin_Borders[5][3][2] = 0.41; z_pT_Bin_Borders[5][3][3] = 0.32;
    Phi_h_Bin_Values[5][3][0] =  24; Phi_h_Bin_Values[5][3][1] = 48; Phi_h_Bin_Values[5][3][2] = 2710;
    z_pT_Bin_Borders[5][4][0] = 0.2; z_pT_Bin_Borders[5][4][1] = 0.16; z_pT_Bin_Borders[5][4][2] = 0.51; z_pT_Bin_Borders[5][4][3] = 0.41;
    Phi_h_Bin_Values[5][4][0] =  24; Phi_h_Bin_Values[5][4][1] = 72; Phi_h_Bin_Values[5][4][2] = 2734;
    z_pT_Bin_Borders[5][5][0] = 0.2; z_pT_Bin_Borders[5][5][1] = 0.16; z_pT_Bin_Borders[5][5][2] = 0.65; z_pT_Bin_Borders[5][5][3] = 0.51;
    Phi_h_Bin_Values[5][5][0] =  1; Phi_h_Bin_Values[5][5][1] = 96; Phi_h_Bin_Values[5][5][2] = 2758;
    z_pT_Bin_Borders[5][6][0] = 0.2; z_pT_Bin_Borders[5][6][1] = 0.16; z_pT_Bin_Borders[5][6][2] = 0.98; z_pT_Bin_Borders[5][6][3] = 0.65;
    Phi_h_Bin_Values[5][6][0] =  1; Phi_h_Bin_Values[5][6][1] = 97; Phi_h_Bin_Values[5][6][2] = 2759;
    z_pT_Bin_Borders[5][7][0] = 0.24; z_pT_Bin_Borders[5][7][1] = 0.2; z_pT_Bin_Borders[5][7][2] = 0.22; z_pT_Bin_Borders[5][7][3] = 0.05;
    Phi_h_Bin_Values[5][7][0] =  24; Phi_h_Bin_Values[5][7][1] = 98; Phi_h_Bin_Values[5][7][2] = 2760;
    z_pT_Bin_Borders[5][8][0] = 0.24; z_pT_Bin_Borders[5][8][1] = 0.2; z_pT_Bin_Borders[5][8][2] = 0.32; z_pT_Bin_Borders[5][8][3] = 0.22;
    Phi_h_Bin_Values[5][8][0] =  24; Phi_h_Bin_Values[5][8][1] = 122; Phi_h_Bin_Values[5][8][2] = 2784;
    z_pT_Bin_Borders[5][9][0] = 0.24; z_pT_Bin_Borders[5][9][1] = 0.2; z_pT_Bin_Borders[5][9][2] = 0.41; z_pT_Bin_Borders[5][9][3] = 0.32;
    Phi_h_Bin_Values[5][9][0] =  24; Phi_h_Bin_Values[5][9][1] = 146; Phi_h_Bin_Values[5][9][2] = 2808;
    z_pT_Bin_Borders[5][10][0] = 0.24; z_pT_Bin_Borders[5][10][1] = 0.2; z_pT_Bin_Borders[5][10][2] = 0.51; z_pT_Bin_Borders[5][10][3] = 0.41;
    Phi_h_Bin_Values[5][10][0] =  24; Phi_h_Bin_Values[5][10][1] = 170; Phi_h_Bin_Values[5][10][2] = 2832;
    z_pT_Bin_Borders[5][11][0] = 0.24; z_pT_Bin_Borders[5][11][1] = 0.2; z_pT_Bin_Borders[5][11][2] = 0.65; z_pT_Bin_Borders[5][11][3] = 0.51;
    Phi_h_Bin_Values[5][11][0] =  24; Phi_h_Bin_Values[5][11][1] = 194; Phi_h_Bin_Values[5][11][2] = 2856;
    z_pT_Bin_Borders[5][12][0] = 0.24; z_pT_Bin_Borders[5][12][1] = 0.2; z_pT_Bin_Borders[5][12][2] = 0.98; z_pT_Bin_Borders[5][12][3] = 0.65;
    Phi_h_Bin_Values[5][12][0] =  1; Phi_h_Bin_Values[5][12][1] = 218; Phi_h_Bin_Values[5][12][2] = 2880;
    z_pT_Bin_Borders[5][13][0] = 0.3; z_pT_Bin_Borders[5][13][1] = 0.24; z_pT_Bin_Borders[5][13][2] = 0.22; z_pT_Bin_Borders[5][13][3] = 0.05;
    Phi_h_Bin_Values[5][13][0] =  24; Phi_h_Bin_Values[5][13][1] = 219; Phi_h_Bin_Values[5][13][2] = 2881;
    z_pT_Bin_Borders[5][14][0] = 0.3; z_pT_Bin_Borders[5][14][1] = 0.24; z_pT_Bin_Borders[5][14][2] = 0.32; z_pT_Bin_Borders[5][14][3] = 0.22;
    Phi_h_Bin_Values[5][14][0] =  24; Phi_h_Bin_Values[5][14][1] = 243; Phi_h_Bin_Values[5][14][2] = 2905;
    z_pT_Bin_Borders[5][15][0] = 0.3; z_pT_Bin_Borders[5][15][1] = 0.24; z_pT_Bin_Borders[5][15][2] = 0.41; z_pT_Bin_Borders[5][15][3] = 0.32;
    Phi_h_Bin_Values[5][15][0] =  24; Phi_h_Bin_Values[5][15][1] = 267; Phi_h_Bin_Values[5][15][2] = 2929;
    z_pT_Bin_Borders[5][16][0] = 0.3; z_pT_Bin_Borders[5][16][1] = 0.24; z_pT_Bin_Borders[5][16][2] = 0.51; z_pT_Bin_Borders[5][16][3] = 0.41;
    Phi_h_Bin_Values[5][16][0] =  24; Phi_h_Bin_Values[5][16][1] = 291; Phi_h_Bin_Values[5][16][2] = 2953;
    z_pT_Bin_Borders[5][17][0] = 0.3; z_pT_Bin_Borders[5][17][1] = 0.24; z_pT_Bin_Borders[5][17][2] = 0.65; z_pT_Bin_Borders[5][17][3] = 0.51;
    Phi_h_Bin_Values[5][17][0] =  24; Phi_h_Bin_Values[5][17][1] = 315; Phi_h_Bin_Values[5][17][2] = 2977;
    z_pT_Bin_Borders[5][18][0] = 0.3; z_pT_Bin_Borders[5][18][1] = 0.24; z_pT_Bin_Borders[5][18][2] = 0.98; z_pT_Bin_Borders[5][18][3] = 0.65;
    Phi_h_Bin_Values[5][18][0] =  1; Phi_h_Bin_Values[5][18][1] = 339; Phi_h_Bin_Values[5][18][2] = 3001;
    z_pT_Bin_Borders[5][19][0] = 0.38; z_pT_Bin_Borders[5][19][1] = 0.3; z_pT_Bin_Borders[5][19][2] = 0.22; z_pT_Bin_Borders[5][19][3] = 0.05;
    Phi_h_Bin_Values[5][19][0] =  24; Phi_h_Bin_Values[5][19][1] = 340; Phi_h_Bin_Values[5][19][2] = 3002;
    z_pT_Bin_Borders[5][20][0] = 0.38; z_pT_Bin_Borders[5][20][1] = 0.3; z_pT_Bin_Borders[5][20][2] = 0.32; z_pT_Bin_Borders[5][20][3] = 0.22;
    Phi_h_Bin_Values[5][20][0] =  24; Phi_h_Bin_Values[5][20][1] = 364; Phi_h_Bin_Values[5][20][2] = 3026;
    z_pT_Bin_Borders[5][21][0] = 0.38; z_pT_Bin_Borders[5][21][1] = 0.3; z_pT_Bin_Borders[5][21][2] = 0.41; z_pT_Bin_Borders[5][21][3] = 0.32;
    Phi_h_Bin_Values[5][21][0] =  24; Phi_h_Bin_Values[5][21][1] = 388; Phi_h_Bin_Values[5][21][2] = 3050;
    z_pT_Bin_Borders[5][22][0] = 0.38; z_pT_Bin_Borders[5][22][1] = 0.3; z_pT_Bin_Borders[5][22][2] = 0.51; z_pT_Bin_Borders[5][22][3] = 0.41;
    Phi_h_Bin_Values[5][22][0] =  24; Phi_h_Bin_Values[5][22][1] = 412; Phi_h_Bin_Values[5][22][2] = 3074;
    z_pT_Bin_Borders[5][23][0] = 0.38; z_pT_Bin_Borders[5][23][1] = 0.3; z_pT_Bin_Borders[5][23][2] = 0.65; z_pT_Bin_Borders[5][23][3] = 0.51;
    Phi_h_Bin_Values[5][23][0] =  24; Phi_h_Bin_Values[5][23][1] = 436; Phi_h_Bin_Values[5][23][2] = 3098;
    z_pT_Bin_Borders[5][24][0] = 0.38; z_pT_Bin_Borders[5][24][1] = 0.3; z_pT_Bin_Borders[5][24][2] = 0.98; z_pT_Bin_Borders[5][24][3] = 0.65;
    Phi_h_Bin_Values[5][24][0] =  24; Phi_h_Bin_Values[5][24][1] = 460; Phi_h_Bin_Values[5][24][2] = 3122;
    z_pT_Bin_Borders[5][25][0] = 0.49; z_pT_Bin_Borders[5][25][1] = 0.38; z_pT_Bin_Borders[5][25][2] = 0.22; z_pT_Bin_Borders[5][25][3] = 0.05;
    Phi_h_Bin_Values[5][25][0] =  24; Phi_h_Bin_Values[5][25][1] = 484; Phi_h_Bin_Values[5][25][2] = 3146;
    z_pT_Bin_Borders[5][26][0] = 0.49; z_pT_Bin_Borders[5][26][1] = 0.38; z_pT_Bin_Borders[5][26][2] = 0.32; z_pT_Bin_Borders[5][26][3] = 0.22;
    Phi_h_Bin_Values[5][26][0] =  24; Phi_h_Bin_Values[5][26][1] = 508; Phi_h_Bin_Values[5][26][2] = 3170;
    z_pT_Bin_Borders[5][27][0] = 0.49; z_pT_Bin_Borders[5][27][1] = 0.38; z_pT_Bin_Borders[5][27][2] = 0.41; z_pT_Bin_Borders[5][27][3] = 0.32;
    Phi_h_Bin_Values[5][27][0] =  24; Phi_h_Bin_Values[5][27][1] = 532; Phi_h_Bin_Values[5][27][2] = 3194;
    z_pT_Bin_Borders[5][28][0] = 0.49; z_pT_Bin_Borders[5][28][1] = 0.38; z_pT_Bin_Borders[5][28][2] = 0.51; z_pT_Bin_Borders[5][28][3] = 0.41;
    Phi_h_Bin_Values[5][28][0] =  24; Phi_h_Bin_Values[5][28][1] = 556; Phi_h_Bin_Values[5][28][2] = 3218;
    z_pT_Bin_Borders[5][29][0] = 0.49; z_pT_Bin_Borders[5][29][1] = 0.38; z_pT_Bin_Borders[5][29][2] = 0.65; z_pT_Bin_Borders[5][29][3] = 0.51;
    Phi_h_Bin_Values[5][29][0] =  24; Phi_h_Bin_Values[5][29][1] = 580; Phi_h_Bin_Values[5][29][2] = 3242;
    z_pT_Bin_Borders[5][30][0] = 0.49; z_pT_Bin_Borders[5][30][1] = 0.38; z_pT_Bin_Borders[5][30][2] = 0.98; z_pT_Bin_Borders[5][30][3] = 0.65;
    Phi_h_Bin_Values[5][30][0] =  24; Phi_h_Bin_Values[5][30][1] = 604; Phi_h_Bin_Values[5][30][2] = 3266;
    z_pT_Bin_Borders[5][31][0] = 0.72; z_pT_Bin_Borders[5][31][1] = 0.49; z_pT_Bin_Borders[5][31][2] = 0.22; z_pT_Bin_Borders[5][31][3] = 0.05;
    Phi_h_Bin_Values[5][31][0] =  24; Phi_h_Bin_Values[5][31][1] = 628; Phi_h_Bin_Values[5][31][2] = 3290;
    z_pT_Bin_Borders[5][32][0] = 0.72; z_pT_Bin_Borders[5][32][1] = 0.49; z_pT_Bin_Borders[5][32][2] = 0.32; z_pT_Bin_Borders[5][32][3] = 0.22;
    Phi_h_Bin_Values[5][32][0] =  24; Phi_h_Bin_Values[5][32][1] = 652; Phi_h_Bin_Values[5][32][2] = 3314;
    z_pT_Bin_Borders[5][33][0] = 0.72; z_pT_Bin_Borders[5][33][1] = 0.49; z_pT_Bin_Borders[5][33][2] = 0.41; z_pT_Bin_Borders[5][33][3] = 0.32;
    Phi_h_Bin_Values[5][33][0] =  24; Phi_h_Bin_Values[5][33][1] = 676; Phi_h_Bin_Values[5][33][2] = 3338;
    z_pT_Bin_Borders[5][34][0] = 0.72; z_pT_Bin_Borders[5][34][1] = 0.49; z_pT_Bin_Borders[5][34][2] = 0.51; z_pT_Bin_Borders[5][34][3] = 0.41;
    Phi_h_Bin_Values[5][34][0] =  24; Phi_h_Bin_Values[5][34][1] = 700; Phi_h_Bin_Values[5][34][2] = 3362;
    z_pT_Bin_Borders[5][35][0] = 0.72; z_pT_Bin_Borders[5][35][1] = 0.49; z_pT_Bin_Borders[5][35][2] = 0.65; z_pT_Bin_Borders[5][35][3] = 0.51;
    Phi_h_Bin_Values[5][35][0] =  24; Phi_h_Bin_Values[5][35][1] = 724; Phi_h_Bin_Values[5][35][2] = 3386;
    z_pT_Bin_Borders[5][36][0] = 0.72; z_pT_Bin_Borders[5][36][1] = 0.49; z_pT_Bin_Borders[5][36][2] = 0.98; z_pT_Bin_Borders[5][36][3] = 0.65;
    Phi_h_Bin_Values[5][36][0] =  24; Phi_h_Bin_Values[5][36][1] = 748; Phi_h_Bin_Values[5][36][2] = 3410;
    z_pT_Bin_Borders[5][37][0] = 0.16; z_pT_Bin_Borders[5][37][1] = 0; z_pT_Bin_Borders[5][37][2] = 0.05; z_pT_Bin_Borders[5][37][3] = 0;
    Phi_h_Bin_Values[5][37][0] =  1; Phi_h_Bin_Values[5][37][1] = 772; Phi_h_Bin_Values[5][37][2] = 3434;
    z_pT_Bin_Borders[5][38][0] = 0.16; z_pT_Bin_Borders[5][38][1] = 0; z_pT_Bin_Borders[5][38][2] = 0.05; z_pT_Bin_Borders[5][38][3] = 0.22;
    Phi_h_Bin_Values[5][38][0] =  1; Phi_h_Bin_Values[5][38][1] = 773; Phi_h_Bin_Values[5][38][2] = 3435;
    z_pT_Bin_Borders[5][39][0] = 0.16; z_pT_Bin_Borders[5][39][1] = 0; z_pT_Bin_Borders[5][39][2] = 0.22; z_pT_Bin_Borders[5][39][3] = 0.32;
    Phi_h_Bin_Values[5][39][0] =  1; Phi_h_Bin_Values[5][39][1] = 774; Phi_h_Bin_Values[5][39][2] = 3436;
    z_pT_Bin_Borders[5][40][0] = 0.16; z_pT_Bin_Borders[5][40][1] = 0; z_pT_Bin_Borders[5][40][2] = 0.32; z_pT_Bin_Borders[5][40][3] = 0.41;
    Phi_h_Bin_Values[5][40][0] =  1; Phi_h_Bin_Values[5][40][1] = 775; Phi_h_Bin_Values[5][40][2] = 3437;
    z_pT_Bin_Borders[5][41][0] = 0.16; z_pT_Bin_Borders[5][41][1] = 0; z_pT_Bin_Borders[5][41][2] = 0.41; z_pT_Bin_Borders[5][41][3] = 0.51;
    Phi_h_Bin_Values[5][41][0] =  1; Phi_h_Bin_Values[5][41][1] = 776; Phi_h_Bin_Values[5][41][2] = 3438;
    z_pT_Bin_Borders[5][42][0] = 0.16; z_pT_Bin_Borders[5][42][1] = 0; z_pT_Bin_Borders[5][42][2] = 0.51; z_pT_Bin_Borders[5][42][3] = 0.65;
    Phi_h_Bin_Values[5][42][0] =  1; Phi_h_Bin_Values[5][42][1] = 777; Phi_h_Bin_Values[5][42][2] = 3439;
    z_pT_Bin_Borders[5][43][0] = 0.16; z_pT_Bin_Borders[5][43][1] = 0; z_pT_Bin_Borders[5][43][2] = 0.65; z_pT_Bin_Borders[5][43][3] = 0.98;
    Phi_h_Bin_Values[5][43][0] =  1; Phi_h_Bin_Values[5][43][1] = 778; Phi_h_Bin_Values[5][43][2] = 3440;
    z_pT_Bin_Borders[5][44][0] = 0.16; z_pT_Bin_Borders[5][44][1] = 0; z_pT_Bin_Borders[5][44][2] = 10; z_pT_Bin_Borders[5][44][3] = 0.98;
    Phi_h_Bin_Values[5][44][0] =  1; Phi_h_Bin_Values[5][44][1] = 779; Phi_h_Bin_Values[5][44][2] = 3441;
    z_pT_Bin_Borders[5][45][0] = 0.16; z_pT_Bin_Borders[5][45][1] = 0.2; z_pT_Bin_Borders[5][45][2] = 0.05; z_pT_Bin_Borders[5][45][3] = 0;
    Phi_h_Bin_Values[5][45][0] =  1; Phi_h_Bin_Values[5][45][1] = 780; Phi_h_Bin_Values[5][45][2] = 3442;
    z_pT_Bin_Borders[5][46][0] = 0.16; z_pT_Bin_Borders[5][46][1] = 0.2; z_pT_Bin_Borders[5][46][2] = 10; z_pT_Bin_Borders[5][46][3] = 0.98;
    Phi_h_Bin_Values[5][46][0] =  1; Phi_h_Bin_Values[5][46][1] = 781; Phi_h_Bin_Values[5][46][2] = 3443;
    z_pT_Bin_Borders[5][47][0] = 0.2; z_pT_Bin_Borders[5][47][1] = 0.24; z_pT_Bin_Borders[5][47][2] = 0.05; z_pT_Bin_Borders[5][47][3] = 0;
    Phi_h_Bin_Values[5][47][0] =  1; Phi_h_Bin_Values[5][47][1] = 782; Phi_h_Bin_Values[5][47][2] = 3444;
    z_pT_Bin_Borders[5][48][0] = 0.2; z_pT_Bin_Borders[5][48][1] = 0.24; z_pT_Bin_Borders[5][48][2] = 10; z_pT_Bin_Borders[5][48][3] = 0.98;
    Phi_h_Bin_Values[5][48][0] =  1; Phi_h_Bin_Values[5][48][1] = 783; Phi_h_Bin_Values[5][48][2] = 3445;
    z_pT_Bin_Borders[5][49][0] = 0.24; z_pT_Bin_Borders[5][49][1] = 0.3; z_pT_Bin_Borders[5][49][2] = 0.05; z_pT_Bin_Borders[5][49][3] = 0;
    Phi_h_Bin_Values[5][49][0] =  1; Phi_h_Bin_Values[5][49][1] = 784; Phi_h_Bin_Values[5][49][2] = 3446;
    z_pT_Bin_Borders[5][50][0] = 0.24; z_pT_Bin_Borders[5][50][1] = 0.3; z_pT_Bin_Borders[5][50][2] = 10; z_pT_Bin_Borders[5][50][3] = 0.98;
    Phi_h_Bin_Values[5][50][0] =  1; Phi_h_Bin_Values[5][50][1] = 785; Phi_h_Bin_Values[5][50][2] = 3447;
    z_pT_Bin_Borders[5][51][0] = 0.3; z_pT_Bin_Borders[5][51][1] = 0.38; z_pT_Bin_Borders[5][51][2] = 0.05; z_pT_Bin_Borders[5][51][3] = 0;
    Phi_h_Bin_Values[5][51][0] =  1; Phi_h_Bin_Values[5][51][1] = 786; Phi_h_Bin_Values[5][51][2] = 3448;
    z_pT_Bin_Borders[5][52][0] = 0.3; z_pT_Bin_Borders[5][52][1] = 0.38; z_pT_Bin_Borders[5][52][2] = 10; z_pT_Bin_Borders[5][52][3] = 0.98;
    Phi_h_Bin_Values[5][52][0] =  1; Phi_h_Bin_Values[5][52][1] = 787; Phi_h_Bin_Values[5][52][2] = 3449;
    z_pT_Bin_Borders[5][53][0] = 0.38; z_pT_Bin_Borders[5][53][1] = 0.49; z_pT_Bin_Borders[5][53][2] = 0.05; z_pT_Bin_Borders[5][53][3] = 0;
    Phi_h_Bin_Values[5][53][0] =  1; Phi_h_Bin_Values[5][53][1] = 788; Phi_h_Bin_Values[5][53][2] = 3450;
    z_pT_Bin_Borders[5][54][0] = 0.38; z_pT_Bin_Borders[5][54][1] = 0.49; z_pT_Bin_Borders[5][54][2] = 10; z_pT_Bin_Borders[5][54][3] = 0.98;
    Phi_h_Bin_Values[5][54][0] =  1; Phi_h_Bin_Values[5][54][1] = 789; Phi_h_Bin_Values[5][54][2] = 3451;
    z_pT_Bin_Borders[5][55][0] = 0.49; z_pT_Bin_Borders[5][55][1] = 0.72; z_pT_Bin_Borders[5][55][2] = 0.05; z_pT_Bin_Borders[5][55][3] = 0;
    Phi_h_Bin_Values[5][55][0] =  1; Phi_h_Bin_Values[5][55][1] = 790; Phi_h_Bin_Values[5][55][2] = 3452;
    z_pT_Bin_Borders[5][56][0] = 0.49; z_pT_Bin_Borders[5][56][1] = 0.72; z_pT_Bin_Borders[5][56][2] = 10; z_pT_Bin_Borders[5][56][3] = 0.98;
    Phi_h_Bin_Values[5][56][0] =  1; Phi_h_Bin_Values[5][56][1] = 791; Phi_h_Bin_Values[5][56][2] = 3453;
    z_pT_Bin_Borders[5][57][0] = 10; z_pT_Bin_Borders[5][57][1] = 0.72; z_pT_Bin_Borders[5][57][2] = 0; z_pT_Bin_Borders[5][57][3] = 0.05;
    Phi_h_Bin_Values[5][57][0] =  1; Phi_h_Bin_Values[5][57][1] = 792; Phi_h_Bin_Values[5][57][2] = 3454;
    z_pT_Bin_Borders[5][58][0] = 10; z_pT_Bin_Borders[5][58][1] = 0.72; z_pT_Bin_Borders[5][58][2] = 0.05; z_pT_Bin_Borders[5][58][3] = 0.22;
    Phi_h_Bin_Values[5][58][0] =  1; Phi_h_Bin_Values[5][58][1] = 793; Phi_h_Bin_Values[5][58][2] = 3455;
    z_pT_Bin_Borders[5][59][0] = 10; z_pT_Bin_Borders[5][59][1] = 0.72; z_pT_Bin_Borders[5][59][2] = 0.22; z_pT_Bin_Borders[5][59][3] = 0.32;
    Phi_h_Bin_Values[5][59][0] =  1; Phi_h_Bin_Values[5][59][1] = 794; Phi_h_Bin_Values[5][59][2] = 3456;
    z_pT_Bin_Borders[5][60][0] = 10; z_pT_Bin_Borders[5][60][1] = 0.72; z_pT_Bin_Borders[5][60][2] = 0.32; z_pT_Bin_Borders[5][60][3] = 0.41;
    Phi_h_Bin_Values[5][60][0] =  1; Phi_h_Bin_Values[5][60][1] = 795; Phi_h_Bin_Values[5][60][2] = 3457;
    z_pT_Bin_Borders[5][61][0] = 10; z_pT_Bin_Borders[5][61][1] = 0.72; z_pT_Bin_Borders[5][61][2] = 0.41; z_pT_Bin_Borders[5][61][3] = 0.51;
    Phi_h_Bin_Values[5][61][0] =  1; Phi_h_Bin_Values[5][61][1] = 796; Phi_h_Bin_Values[5][61][2] = 3458;
    z_pT_Bin_Borders[5][62][0] = 10; z_pT_Bin_Borders[5][62][1] = 0.72; z_pT_Bin_Borders[5][62][2] = 0.51; z_pT_Bin_Borders[5][62][3] = 0.65;
    Phi_h_Bin_Values[5][62][0] =  1; Phi_h_Bin_Values[5][62][1] = 797; Phi_h_Bin_Values[5][62][2] = 3459;
    z_pT_Bin_Borders[5][63][0] = 10; z_pT_Bin_Borders[5][63][1] = 0.72; z_pT_Bin_Borders[5][63][2] = 0.65; z_pT_Bin_Borders[5][63][3] = 0.98;
    Phi_h_Bin_Values[5][63][0] =  1; Phi_h_Bin_Values[5][63][1] = 798; Phi_h_Bin_Values[5][63][2] = 3460;
    z_pT_Bin_Borders[5][64][0] = 10; z_pT_Bin_Borders[5][64][1] = 0.72; z_pT_Bin_Borders[5][64][2] = 10; z_pT_Bin_Borders[5][64][3] = 0.98;
    Phi_h_Bin_Values[5][64][0] =  1; Phi_h_Bin_Values[5][64][1] = 799; Phi_h_Bin_Values[5][64][2] = 3461;
    z_pT_Bin_Borders[6][1][0] = 0.23; z_pT_Bin_Borders[6][1][1] = 0.18; z_pT_Bin_Borders[6][1][2] = 0.22; z_pT_Bin_Borders[6][1][3] = 0.05;
    Phi_h_Bin_Values[6][1][0] =  24; Phi_h_Bin_Values[6][1][1] = 0; Phi_h_Bin_Values[6][1][2] = 3462;
    z_pT_Bin_Borders[6][2][0] = 0.23; z_pT_Bin_Borders[6][2][1] = 0.18; z_pT_Bin_Borders[6][2][2] = 0.32; z_pT_Bin_Borders[6][2][3] = 0.22;
    Phi_h_Bin_Values[6][2][0] =  24; Phi_h_Bin_Values[6][2][1] = 24; Phi_h_Bin_Values[6][2][2] = 3486;
    z_pT_Bin_Borders[6][3][0] = 0.23; z_pT_Bin_Borders[6][3][1] = 0.18; z_pT_Bin_Borders[6][3][2] = 0.41; z_pT_Bin_Borders[6][3][3] = 0.32;
    Phi_h_Bin_Values[6][3][0] =  24; Phi_h_Bin_Values[6][3][1] = 48; Phi_h_Bin_Values[6][3][2] = 3510;
    z_pT_Bin_Borders[6][4][0] = 0.23; z_pT_Bin_Borders[6][4][1] = 0.18; z_pT_Bin_Borders[6][4][2] = 0.51; z_pT_Bin_Borders[6][4][3] = 0.41;
    Phi_h_Bin_Values[6][4][0] =  24; Phi_h_Bin_Values[6][4][1] = 72; Phi_h_Bin_Values[6][4][2] = 3534;
    z_pT_Bin_Borders[6][5][0] = 0.23; z_pT_Bin_Borders[6][5][1] = 0.18; z_pT_Bin_Borders[6][5][2] = 0.65; z_pT_Bin_Borders[6][5][3] = 0.51;
    Phi_h_Bin_Values[6][5][0] =  1; Phi_h_Bin_Values[6][5][1] = 96; Phi_h_Bin_Values[6][5][2] = 3558;
    z_pT_Bin_Borders[6][6][0] = 0.23; z_pT_Bin_Borders[6][6][1] = 0.18; z_pT_Bin_Borders[6][6][2] = 1.05; z_pT_Bin_Borders[6][6][3] = 0.65;
    Phi_h_Bin_Values[6][6][0] =  1; Phi_h_Bin_Values[6][6][1] = 97; Phi_h_Bin_Values[6][6][2] = 3559;
    z_pT_Bin_Borders[6][7][0] = 0.28; z_pT_Bin_Borders[6][7][1] = 0.23; z_pT_Bin_Borders[6][7][2] = 0.22; z_pT_Bin_Borders[6][7][3] = 0.05;
    Phi_h_Bin_Values[6][7][0] =  24; Phi_h_Bin_Values[6][7][1] = 98; Phi_h_Bin_Values[6][7][2] = 3560;
    z_pT_Bin_Borders[6][8][0] = 0.28; z_pT_Bin_Borders[6][8][1] = 0.23; z_pT_Bin_Borders[6][8][2] = 0.32; z_pT_Bin_Borders[6][8][3] = 0.22;
    Phi_h_Bin_Values[6][8][0] =  24; Phi_h_Bin_Values[6][8][1] = 122; Phi_h_Bin_Values[6][8][2] = 3584;
    z_pT_Bin_Borders[6][9][0] = 0.28; z_pT_Bin_Borders[6][9][1] = 0.23; z_pT_Bin_Borders[6][9][2] = 0.41; z_pT_Bin_Borders[6][9][3] = 0.32;
    Phi_h_Bin_Values[6][9][0] =  24; Phi_h_Bin_Values[6][9][1] = 146; Phi_h_Bin_Values[6][9][2] = 3608;
    z_pT_Bin_Borders[6][10][0] = 0.28; z_pT_Bin_Borders[6][10][1] = 0.23; z_pT_Bin_Borders[6][10][2] = 0.51; z_pT_Bin_Borders[6][10][3] = 0.41;
    Phi_h_Bin_Values[6][10][0] =  24; Phi_h_Bin_Values[6][10][1] = 170; Phi_h_Bin_Values[6][10][2] = 3632;
    z_pT_Bin_Borders[6][11][0] = 0.28; z_pT_Bin_Borders[6][11][1] = 0.23; z_pT_Bin_Borders[6][11][2] = 0.65; z_pT_Bin_Borders[6][11][3] = 0.51;
    Phi_h_Bin_Values[6][11][0] =  24; Phi_h_Bin_Values[6][11][1] = 194; Phi_h_Bin_Values[6][11][2] = 3656;
    z_pT_Bin_Borders[6][12][0] = 0.28; z_pT_Bin_Borders[6][12][1] = 0.23; z_pT_Bin_Borders[6][12][2] = 1.05; z_pT_Bin_Borders[6][12][3] = 0.65;
    Phi_h_Bin_Values[6][12][0] =  1; Phi_h_Bin_Values[6][12][1] = 218; Phi_h_Bin_Values[6][12][2] = 3680;
    z_pT_Bin_Borders[6][13][0] = 0.35; z_pT_Bin_Borders[6][13][1] = 0.28; z_pT_Bin_Borders[6][13][2] = 0.22; z_pT_Bin_Borders[6][13][3] = 0.05;
    Phi_h_Bin_Values[6][13][0] =  24; Phi_h_Bin_Values[6][13][1] = 219; Phi_h_Bin_Values[6][13][2] = 3681;
    z_pT_Bin_Borders[6][14][0] = 0.35; z_pT_Bin_Borders[6][14][1] = 0.28; z_pT_Bin_Borders[6][14][2] = 0.32; z_pT_Bin_Borders[6][14][3] = 0.22;
    Phi_h_Bin_Values[6][14][0] =  24; Phi_h_Bin_Values[6][14][1] = 243; Phi_h_Bin_Values[6][14][2] = 3705;
    z_pT_Bin_Borders[6][15][0] = 0.35; z_pT_Bin_Borders[6][15][1] = 0.28; z_pT_Bin_Borders[6][15][2] = 0.41; z_pT_Bin_Borders[6][15][3] = 0.32;
    Phi_h_Bin_Values[6][15][0] =  24; Phi_h_Bin_Values[6][15][1] = 267; Phi_h_Bin_Values[6][15][2] = 3729;
    z_pT_Bin_Borders[6][16][0] = 0.35; z_pT_Bin_Borders[6][16][1] = 0.28; z_pT_Bin_Borders[6][16][2] = 0.51; z_pT_Bin_Borders[6][16][3] = 0.41;
    Phi_h_Bin_Values[6][16][0] =  24; Phi_h_Bin_Values[6][16][1] = 291; Phi_h_Bin_Values[6][16][2] = 3753;
    z_pT_Bin_Borders[6][17][0] = 0.35; z_pT_Bin_Borders[6][17][1] = 0.28; z_pT_Bin_Borders[6][17][2] = 0.65; z_pT_Bin_Borders[6][17][3] = 0.51;
    Phi_h_Bin_Values[6][17][0] =  24; Phi_h_Bin_Values[6][17][1] = 315; Phi_h_Bin_Values[6][17][2] = 3777;
    z_pT_Bin_Borders[6][18][0] = 0.35; z_pT_Bin_Borders[6][18][1] = 0.28; z_pT_Bin_Borders[6][18][2] = 1.05; z_pT_Bin_Borders[6][18][3] = 0.65;
    Phi_h_Bin_Values[6][18][0] =  1; Phi_h_Bin_Values[6][18][1] = 339; Phi_h_Bin_Values[6][18][2] = 3801;
    z_pT_Bin_Borders[6][19][0] = 0.45; z_pT_Bin_Borders[6][19][1] = 0.35; z_pT_Bin_Borders[6][19][2] = 0.22; z_pT_Bin_Borders[6][19][3] = 0.05;
    Phi_h_Bin_Values[6][19][0] =  24; Phi_h_Bin_Values[6][19][1] = 340; Phi_h_Bin_Values[6][19][2] = 3802;
    z_pT_Bin_Borders[6][20][0] = 0.45; z_pT_Bin_Borders[6][20][1] = 0.35; z_pT_Bin_Borders[6][20][2] = 0.32; z_pT_Bin_Borders[6][20][3] = 0.22;
    Phi_h_Bin_Values[6][20][0] =  24; Phi_h_Bin_Values[6][20][1] = 364; Phi_h_Bin_Values[6][20][2] = 3826;
    z_pT_Bin_Borders[6][21][0] = 0.45; z_pT_Bin_Borders[6][21][1] = 0.35; z_pT_Bin_Borders[6][21][2] = 0.41; z_pT_Bin_Borders[6][21][3] = 0.32;
    Phi_h_Bin_Values[6][21][0] =  24; Phi_h_Bin_Values[6][21][1] = 388; Phi_h_Bin_Values[6][21][2] = 3850;
    z_pT_Bin_Borders[6][22][0] = 0.45; z_pT_Bin_Borders[6][22][1] = 0.35; z_pT_Bin_Borders[6][22][2] = 0.51; z_pT_Bin_Borders[6][22][3] = 0.41;
    Phi_h_Bin_Values[6][22][0] =  24; Phi_h_Bin_Values[6][22][1] = 412; Phi_h_Bin_Values[6][22][2] = 3874;
    z_pT_Bin_Borders[6][23][0] = 0.45; z_pT_Bin_Borders[6][23][1] = 0.35; z_pT_Bin_Borders[6][23][2] = 0.65; z_pT_Bin_Borders[6][23][3] = 0.51;
    Phi_h_Bin_Values[6][23][0] =  24; Phi_h_Bin_Values[6][23][1] = 436; Phi_h_Bin_Values[6][23][2] = 3898;
    z_pT_Bin_Borders[6][24][0] = 0.45; z_pT_Bin_Borders[6][24][1] = 0.35; z_pT_Bin_Borders[6][24][2] = 1.05; z_pT_Bin_Borders[6][24][3] = 0.65;
    Phi_h_Bin_Values[6][24][0] =  24; Phi_h_Bin_Values[6][24][1] = 460; Phi_h_Bin_Values[6][24][2] = 3922;
    z_pT_Bin_Borders[6][25][0] = 0.75; z_pT_Bin_Borders[6][25][1] = 0.45; z_pT_Bin_Borders[6][25][2] = 0.22; z_pT_Bin_Borders[6][25][3] = 0.05;
    Phi_h_Bin_Values[6][25][0] =  24; Phi_h_Bin_Values[6][25][1] = 484; Phi_h_Bin_Values[6][25][2] = 3946;
    z_pT_Bin_Borders[6][26][0] = 0.75; z_pT_Bin_Borders[6][26][1] = 0.45; z_pT_Bin_Borders[6][26][2] = 0.32; z_pT_Bin_Borders[6][26][3] = 0.22;
    Phi_h_Bin_Values[6][26][0] =  24; Phi_h_Bin_Values[6][26][1] = 508; Phi_h_Bin_Values[6][26][2] = 3970;
    z_pT_Bin_Borders[6][27][0] = 0.75; z_pT_Bin_Borders[6][27][1] = 0.45; z_pT_Bin_Borders[6][27][2] = 0.41; z_pT_Bin_Borders[6][27][3] = 0.32;
    Phi_h_Bin_Values[6][27][0] =  24; Phi_h_Bin_Values[6][27][1] = 532; Phi_h_Bin_Values[6][27][2] = 3994;
    z_pT_Bin_Borders[6][28][0] = 0.75; z_pT_Bin_Borders[6][28][1] = 0.45; z_pT_Bin_Borders[6][28][2] = 0.51; z_pT_Bin_Borders[6][28][3] = 0.41;
    Phi_h_Bin_Values[6][28][0] =  24; Phi_h_Bin_Values[6][28][1] = 556; Phi_h_Bin_Values[6][28][2] = 4018;
    z_pT_Bin_Borders[6][29][0] = 0.75; z_pT_Bin_Borders[6][29][1] = 0.45; z_pT_Bin_Borders[6][29][2] = 0.65; z_pT_Bin_Borders[6][29][3] = 0.51;
    Phi_h_Bin_Values[6][29][0] =  24; Phi_h_Bin_Values[6][29][1] = 580; Phi_h_Bin_Values[6][29][2] = 4042;
    z_pT_Bin_Borders[6][30][0] = 0.75; z_pT_Bin_Borders[6][30][1] = 0.45; z_pT_Bin_Borders[6][30][2] = 1.05; z_pT_Bin_Borders[6][30][3] = 0.65;
    Phi_h_Bin_Values[6][30][0] =  1; Phi_h_Bin_Values[6][30][1] = 604; Phi_h_Bin_Values[6][30][2] = 4066;
    z_pT_Bin_Borders[6][31][0] = 0.18; z_pT_Bin_Borders[6][31][1] = 0; z_pT_Bin_Borders[6][31][2] = 0.05; z_pT_Bin_Borders[6][31][3] = 0;
    Phi_h_Bin_Values[6][31][0] =  1; Phi_h_Bin_Values[6][31][1] = 605; Phi_h_Bin_Values[6][31][2] = 4067;
    z_pT_Bin_Borders[6][32][0] = 0.18; z_pT_Bin_Borders[6][32][1] = 0; z_pT_Bin_Borders[6][32][2] = 0.05; z_pT_Bin_Borders[6][32][3] = 0.22;
    Phi_h_Bin_Values[6][32][0] =  1; Phi_h_Bin_Values[6][32][1] = 606; Phi_h_Bin_Values[6][32][2] = 4068;
    z_pT_Bin_Borders[6][33][0] = 0.18; z_pT_Bin_Borders[6][33][1] = 0; z_pT_Bin_Borders[6][33][2] = 0.22; z_pT_Bin_Borders[6][33][3] = 0.32;
    Phi_h_Bin_Values[6][33][0] =  1; Phi_h_Bin_Values[6][33][1] = 607; Phi_h_Bin_Values[6][33][2] = 4069;
    z_pT_Bin_Borders[6][34][0] = 0.18; z_pT_Bin_Borders[6][34][1] = 0; z_pT_Bin_Borders[6][34][2] = 0.32; z_pT_Bin_Borders[6][34][3] = 0.41;
    Phi_h_Bin_Values[6][34][0] =  1; Phi_h_Bin_Values[6][34][1] = 608; Phi_h_Bin_Values[6][34][2] = 4070;
    z_pT_Bin_Borders[6][35][0] = 0.18; z_pT_Bin_Borders[6][35][1] = 0; z_pT_Bin_Borders[6][35][2] = 0.41; z_pT_Bin_Borders[6][35][3] = 0.51;
    Phi_h_Bin_Values[6][35][0] =  1; Phi_h_Bin_Values[6][35][1] = 609; Phi_h_Bin_Values[6][35][2] = 4071;
    z_pT_Bin_Borders[6][36][0] = 0.18; z_pT_Bin_Borders[6][36][1] = 0; z_pT_Bin_Borders[6][36][2] = 0.51; z_pT_Bin_Borders[6][36][3] = 0.65;
    Phi_h_Bin_Values[6][36][0] =  1; Phi_h_Bin_Values[6][36][1] = 610; Phi_h_Bin_Values[6][36][2] = 4072;
    z_pT_Bin_Borders[6][37][0] = 0.18; z_pT_Bin_Borders[6][37][1] = 0; z_pT_Bin_Borders[6][37][2] = 0.65; z_pT_Bin_Borders[6][37][3] = 1.05;
    Phi_h_Bin_Values[6][37][0] =  1; Phi_h_Bin_Values[6][37][1] = 611; Phi_h_Bin_Values[6][37][2] = 4073;
    z_pT_Bin_Borders[6][38][0] = 0.18; z_pT_Bin_Borders[6][38][1] = 0; z_pT_Bin_Borders[6][38][2] = 10; z_pT_Bin_Borders[6][38][3] = 1.05;
    Phi_h_Bin_Values[6][38][0] =  1; Phi_h_Bin_Values[6][38][1] = 612; Phi_h_Bin_Values[6][38][2] = 4074;
    z_pT_Bin_Borders[6][39][0] = 0.18; z_pT_Bin_Borders[6][39][1] = 0.23; z_pT_Bin_Borders[6][39][2] = 0.05; z_pT_Bin_Borders[6][39][3] = 0;
    Phi_h_Bin_Values[6][39][0] =  1; Phi_h_Bin_Values[6][39][1] = 613; Phi_h_Bin_Values[6][39][2] = 4075;
    z_pT_Bin_Borders[6][40][0] = 0.18; z_pT_Bin_Borders[6][40][1] = 0.23; z_pT_Bin_Borders[6][40][2] = 10; z_pT_Bin_Borders[6][40][3] = 1.05;
    Phi_h_Bin_Values[6][40][0] =  1; Phi_h_Bin_Values[6][40][1] = 614; Phi_h_Bin_Values[6][40][2] = 4076;
    z_pT_Bin_Borders[6][41][0] = 0.23; z_pT_Bin_Borders[6][41][1] = 0.28; z_pT_Bin_Borders[6][41][2] = 0.05; z_pT_Bin_Borders[6][41][3] = 0;
    Phi_h_Bin_Values[6][41][0] =  1; Phi_h_Bin_Values[6][41][1] = 615; Phi_h_Bin_Values[6][41][2] = 4077;
    z_pT_Bin_Borders[6][42][0] = 0.23; z_pT_Bin_Borders[6][42][1] = 0.28; z_pT_Bin_Borders[6][42][2] = 10; z_pT_Bin_Borders[6][42][3] = 1.05;
    Phi_h_Bin_Values[6][42][0] =  1; Phi_h_Bin_Values[6][42][1] = 616; Phi_h_Bin_Values[6][42][2] = 4078;
    z_pT_Bin_Borders[6][43][0] = 0.28; z_pT_Bin_Borders[6][43][1] = 0.35; z_pT_Bin_Borders[6][43][2] = 0.05; z_pT_Bin_Borders[6][43][3] = 0;
    Phi_h_Bin_Values[6][43][0] =  1; Phi_h_Bin_Values[6][43][1] = 617; Phi_h_Bin_Values[6][43][2] = 4079;
    z_pT_Bin_Borders[6][44][0] = 0.28; z_pT_Bin_Borders[6][44][1] = 0.35; z_pT_Bin_Borders[6][44][2] = 10; z_pT_Bin_Borders[6][44][3] = 1.05;
    Phi_h_Bin_Values[6][44][0] =  1; Phi_h_Bin_Values[6][44][1] = 618; Phi_h_Bin_Values[6][44][2] = 4080;
    z_pT_Bin_Borders[6][45][0] = 0.35; z_pT_Bin_Borders[6][45][1] = 0.45; z_pT_Bin_Borders[6][45][2] = 0.05; z_pT_Bin_Borders[6][45][3] = 0;
    Phi_h_Bin_Values[6][45][0] =  1; Phi_h_Bin_Values[6][45][1] = 619; Phi_h_Bin_Values[6][45][2] = 4081;
    z_pT_Bin_Borders[6][46][0] = 0.35; z_pT_Bin_Borders[6][46][1] = 0.45; z_pT_Bin_Borders[6][46][2] = 10; z_pT_Bin_Borders[6][46][3] = 1.05;
    Phi_h_Bin_Values[6][46][0] =  1; Phi_h_Bin_Values[6][46][1] = 620; Phi_h_Bin_Values[6][46][2] = 4082;
    z_pT_Bin_Borders[6][47][0] = 0.45; z_pT_Bin_Borders[6][47][1] = 0.75; z_pT_Bin_Borders[6][47][2] = 0.05; z_pT_Bin_Borders[6][47][3] = 0;
    Phi_h_Bin_Values[6][47][0] =  1; Phi_h_Bin_Values[6][47][1] = 621; Phi_h_Bin_Values[6][47][2] = 4083;
    z_pT_Bin_Borders[6][48][0] = 0.45; z_pT_Bin_Borders[6][48][1] = 0.75; z_pT_Bin_Borders[6][48][2] = 10; z_pT_Bin_Borders[6][48][3] = 1.05;
    Phi_h_Bin_Values[6][48][0] =  1; Phi_h_Bin_Values[6][48][1] = 622; Phi_h_Bin_Values[6][48][2] = 4084;
    z_pT_Bin_Borders[6][49][0] = 10; z_pT_Bin_Borders[6][49][1] = 0.75; z_pT_Bin_Borders[6][49][2] = 0; z_pT_Bin_Borders[6][49][3] = 0.05;
    Phi_h_Bin_Values[6][49][0] =  1; Phi_h_Bin_Values[6][49][1] = 623; Phi_h_Bin_Values[6][49][2] = 4085;
    z_pT_Bin_Borders[6][50][0] = 10; z_pT_Bin_Borders[6][50][1] = 0.75; z_pT_Bin_Borders[6][50][2] = 0.05; z_pT_Bin_Borders[6][50][3] = 0.22;
    Phi_h_Bin_Values[6][50][0] =  1; Phi_h_Bin_Values[6][50][1] = 624; Phi_h_Bin_Values[6][50][2] = 4086;
    z_pT_Bin_Borders[6][51][0] = 10; z_pT_Bin_Borders[6][51][1] = 0.75; z_pT_Bin_Borders[6][51][2] = 0.22; z_pT_Bin_Borders[6][51][3] = 0.32;
    Phi_h_Bin_Values[6][51][0] =  1; Phi_h_Bin_Values[6][51][1] = 625; Phi_h_Bin_Values[6][51][2] = 4087;
    z_pT_Bin_Borders[6][52][0] = 10; z_pT_Bin_Borders[6][52][1] = 0.75; z_pT_Bin_Borders[6][52][2] = 0.32; z_pT_Bin_Borders[6][52][3] = 0.41;
    Phi_h_Bin_Values[6][52][0] =  1; Phi_h_Bin_Values[6][52][1] = 626; Phi_h_Bin_Values[6][52][2] = 4088;
    z_pT_Bin_Borders[6][53][0] = 10; z_pT_Bin_Borders[6][53][1] = 0.75; z_pT_Bin_Borders[6][53][2] = 0.41; z_pT_Bin_Borders[6][53][3] = 0.51;
    Phi_h_Bin_Values[6][53][0] =  1; Phi_h_Bin_Values[6][53][1] = 627; Phi_h_Bin_Values[6][53][2] = 4089;
    z_pT_Bin_Borders[6][54][0] = 10; z_pT_Bin_Borders[6][54][1] = 0.75; z_pT_Bin_Borders[6][54][2] = 0.51; z_pT_Bin_Borders[6][54][3] = 0.65;
    Phi_h_Bin_Values[6][54][0] =  1; Phi_h_Bin_Values[6][54][1] = 628; Phi_h_Bin_Values[6][54][2] = 4090;
    z_pT_Bin_Borders[6][55][0] = 10; z_pT_Bin_Borders[6][55][1] = 0.75; z_pT_Bin_Borders[6][55][2] = 0.65; z_pT_Bin_Borders[6][55][3] = 1.05;
    Phi_h_Bin_Values[6][55][0] =  1; Phi_h_Bin_Values[6][55][1] = 629; Phi_h_Bin_Values[6][55][2] = 4091;
    z_pT_Bin_Borders[6][56][0] = 10; z_pT_Bin_Borders[6][56][1] = 0.75; z_pT_Bin_Borders[6][56][2] = 10; z_pT_Bin_Borders[6][56][3] = 1.05;
    Phi_h_Bin_Values[6][56][0] =  1; Phi_h_Bin_Values[6][56][1] = 630; Phi_h_Bin_Values[6][56][2] = 4092;
    z_pT_Bin_Borders[7][1][0] = 0.28; z_pT_Bin_Borders[7][1][1] = 0.22; z_pT_Bin_Borders[7][1][2] = 0.2; z_pT_Bin_Borders[7][1][3] = 0.05;
    Phi_h_Bin_Values[7][1][0] =  24; Phi_h_Bin_Values[7][1][1] = 0; Phi_h_Bin_Values[7][1][2] = 4093;
    z_pT_Bin_Borders[7][2][0] = 0.28; z_pT_Bin_Borders[7][2][1] = 0.22; z_pT_Bin_Borders[7][2][2] = 0.29; z_pT_Bin_Borders[7][2][3] = 0.2;
    Phi_h_Bin_Values[7][2][0] =  24; Phi_h_Bin_Values[7][2][1] = 24; Phi_h_Bin_Values[7][2][2] = 4117;
    z_pT_Bin_Borders[7][3][0] = 0.28; z_pT_Bin_Borders[7][3][1] = 0.22; z_pT_Bin_Borders[7][3][2] = 0.38; z_pT_Bin_Borders[7][3][3] = 0.29;
    Phi_h_Bin_Values[7][3][0] =  24; Phi_h_Bin_Values[7][3][1] = 48; Phi_h_Bin_Values[7][3][2] = 4141;
    z_pT_Bin_Borders[7][4][0] = 0.28; z_pT_Bin_Borders[7][4][1] = 0.22; z_pT_Bin_Borders[7][4][2] = 0.48; z_pT_Bin_Borders[7][4][3] = 0.38;
    Phi_h_Bin_Values[7][4][0] =  24; Phi_h_Bin_Values[7][4][1] = 72; Phi_h_Bin_Values[7][4][2] = 4165;
    z_pT_Bin_Borders[7][5][0] = 0.28; z_pT_Bin_Borders[7][5][1] = 0.22; z_pT_Bin_Borders[7][5][2] = 0.6; z_pT_Bin_Borders[7][5][3] = 0.48;
    Phi_h_Bin_Values[7][5][0] =  24; Phi_h_Bin_Values[7][5][1] = 96; Phi_h_Bin_Values[7][5][2] = 4189;
    z_pT_Bin_Borders[7][6][0] = 0.28; z_pT_Bin_Borders[7][6][1] = 0.22; z_pT_Bin_Borders[7][6][2] = 0.83; z_pT_Bin_Borders[7][6][3] = 0.6;
    Phi_h_Bin_Values[7][6][0] =  1; Phi_h_Bin_Values[7][6][1] = 120; Phi_h_Bin_Values[7][6][2] = 4213;
    z_pT_Bin_Borders[7][7][0] = 0.33; z_pT_Bin_Borders[7][7][1] = 0.28; z_pT_Bin_Borders[7][7][2] = 0.2; z_pT_Bin_Borders[7][7][3] = 0.05;
    Phi_h_Bin_Values[7][7][0] =  24; Phi_h_Bin_Values[7][7][1] = 121; Phi_h_Bin_Values[7][7][2] = 4214;
    z_pT_Bin_Borders[7][8][0] = 0.33; z_pT_Bin_Borders[7][8][1] = 0.28; z_pT_Bin_Borders[7][8][2] = 0.29; z_pT_Bin_Borders[7][8][3] = 0.2;
    Phi_h_Bin_Values[7][8][0] =  24; Phi_h_Bin_Values[7][8][1] = 145; Phi_h_Bin_Values[7][8][2] = 4238;
    z_pT_Bin_Borders[7][9][0] = 0.33; z_pT_Bin_Borders[7][9][1] = 0.28; z_pT_Bin_Borders[7][9][2] = 0.38; z_pT_Bin_Borders[7][9][3] = 0.29;
    Phi_h_Bin_Values[7][9][0] =  24; Phi_h_Bin_Values[7][9][1] = 169; Phi_h_Bin_Values[7][9][2] = 4262;
    z_pT_Bin_Borders[7][10][0] = 0.33; z_pT_Bin_Borders[7][10][1] = 0.28; z_pT_Bin_Borders[7][10][2] = 0.48; z_pT_Bin_Borders[7][10][3] = 0.38;
    Phi_h_Bin_Values[7][10][0] =  24; Phi_h_Bin_Values[7][10][1] = 193; Phi_h_Bin_Values[7][10][2] = 4286;
    z_pT_Bin_Borders[7][11][0] = 0.33; z_pT_Bin_Borders[7][11][1] = 0.28; z_pT_Bin_Borders[7][11][2] = 0.6; z_pT_Bin_Borders[7][11][3] = 0.48;
    Phi_h_Bin_Values[7][11][0] =  24; Phi_h_Bin_Values[7][11][1] = 217; Phi_h_Bin_Values[7][11][2] = 4310;
    z_pT_Bin_Borders[7][12][0] = 0.33; z_pT_Bin_Borders[7][12][1] = 0.28; z_pT_Bin_Borders[7][12][2] = 0.83; z_pT_Bin_Borders[7][12][3] = 0.6;
    Phi_h_Bin_Values[7][12][0] =  1; Phi_h_Bin_Values[7][12][1] = 241; Phi_h_Bin_Values[7][12][2] = 4334;
    z_pT_Bin_Borders[7][13][0] = 0.4; z_pT_Bin_Borders[7][13][1] = 0.33; z_pT_Bin_Borders[7][13][2] = 0.2; z_pT_Bin_Borders[7][13][3] = 0.05;
    Phi_h_Bin_Values[7][13][0] =  24; Phi_h_Bin_Values[7][13][1] = 242; Phi_h_Bin_Values[7][13][2] = 4335;
    z_pT_Bin_Borders[7][14][0] = 0.4; z_pT_Bin_Borders[7][14][1] = 0.33; z_pT_Bin_Borders[7][14][2] = 0.29; z_pT_Bin_Borders[7][14][3] = 0.2;
    Phi_h_Bin_Values[7][14][0] =  24; Phi_h_Bin_Values[7][14][1] = 266; Phi_h_Bin_Values[7][14][2] = 4359;
    z_pT_Bin_Borders[7][15][0] = 0.4; z_pT_Bin_Borders[7][15][1] = 0.33; z_pT_Bin_Borders[7][15][2] = 0.38; z_pT_Bin_Borders[7][15][3] = 0.29;
    Phi_h_Bin_Values[7][15][0] =  24; Phi_h_Bin_Values[7][15][1] = 290; Phi_h_Bin_Values[7][15][2] = 4383;
    z_pT_Bin_Borders[7][16][0] = 0.4; z_pT_Bin_Borders[7][16][1] = 0.33; z_pT_Bin_Borders[7][16][2] = 0.48; z_pT_Bin_Borders[7][16][3] = 0.38;
    Phi_h_Bin_Values[7][16][0] =  24; Phi_h_Bin_Values[7][16][1] = 314; Phi_h_Bin_Values[7][16][2] = 4407;
    z_pT_Bin_Borders[7][17][0] = 0.4; z_pT_Bin_Borders[7][17][1] = 0.33; z_pT_Bin_Borders[7][17][2] = 0.6; z_pT_Bin_Borders[7][17][3] = 0.48;
    Phi_h_Bin_Values[7][17][0] =  24; Phi_h_Bin_Values[7][17][1] = 338; Phi_h_Bin_Values[7][17][2] = 4431;
    z_pT_Bin_Borders[7][18][0] = 0.4; z_pT_Bin_Borders[7][18][1] = 0.33; z_pT_Bin_Borders[7][18][2] = 0.83; z_pT_Bin_Borders[7][18][3] = 0.6;
    Phi_h_Bin_Values[7][18][0] =  24; Phi_h_Bin_Values[7][18][1] = 362; Phi_h_Bin_Values[7][18][2] = 4455;
    z_pT_Bin_Borders[7][19][0] = 0.51; z_pT_Bin_Borders[7][19][1] = 0.4; z_pT_Bin_Borders[7][19][2] = 0.2; z_pT_Bin_Borders[7][19][3] = 0.05;
    Phi_h_Bin_Values[7][19][0] =  24; Phi_h_Bin_Values[7][19][1] = 386; Phi_h_Bin_Values[7][19][2] = 4479;
    z_pT_Bin_Borders[7][20][0] = 0.51; z_pT_Bin_Borders[7][20][1] = 0.4; z_pT_Bin_Borders[7][20][2] = 0.29; z_pT_Bin_Borders[7][20][3] = 0.2;
    Phi_h_Bin_Values[7][20][0] =  24; Phi_h_Bin_Values[7][20][1] = 410; Phi_h_Bin_Values[7][20][2] = 4503;
    z_pT_Bin_Borders[7][21][0] = 0.51; z_pT_Bin_Borders[7][21][1] = 0.4; z_pT_Bin_Borders[7][21][2] = 0.38; z_pT_Bin_Borders[7][21][3] = 0.29;
    Phi_h_Bin_Values[7][21][0] =  24; Phi_h_Bin_Values[7][21][1] = 434; Phi_h_Bin_Values[7][21][2] = 4527;
    z_pT_Bin_Borders[7][22][0] = 0.51; z_pT_Bin_Borders[7][22][1] = 0.4; z_pT_Bin_Borders[7][22][2] = 0.48; z_pT_Bin_Borders[7][22][3] = 0.38;
    Phi_h_Bin_Values[7][22][0] =  24; Phi_h_Bin_Values[7][22][1] = 458; Phi_h_Bin_Values[7][22][2] = 4551;
    z_pT_Bin_Borders[7][23][0] = 0.51; z_pT_Bin_Borders[7][23][1] = 0.4; z_pT_Bin_Borders[7][23][2] = 0.6; z_pT_Bin_Borders[7][23][3] = 0.48;
    Phi_h_Bin_Values[7][23][0] =  24; Phi_h_Bin_Values[7][23][1] = 482; Phi_h_Bin_Values[7][23][2] = 4575;
    z_pT_Bin_Borders[7][24][0] = 0.51; z_pT_Bin_Borders[7][24][1] = 0.4; z_pT_Bin_Borders[7][24][2] = 0.83; z_pT_Bin_Borders[7][24][3] = 0.6;
    Phi_h_Bin_Values[7][24][0] =  24; Phi_h_Bin_Values[7][24][1] = 506; Phi_h_Bin_Values[7][24][2] = 4599;
    z_pT_Bin_Borders[7][25][0] = 0.7; z_pT_Bin_Borders[7][25][1] = 0.51; z_pT_Bin_Borders[7][25][2] = 0.2; z_pT_Bin_Borders[7][25][3] = 0.05;
    Phi_h_Bin_Values[7][25][0] =  24; Phi_h_Bin_Values[7][25][1] = 530; Phi_h_Bin_Values[7][25][2] = 4623;
    z_pT_Bin_Borders[7][26][0] = 0.7; z_pT_Bin_Borders[7][26][1] = 0.51; z_pT_Bin_Borders[7][26][2] = 0.29; z_pT_Bin_Borders[7][26][3] = 0.2;
    Phi_h_Bin_Values[7][26][0] =  24; Phi_h_Bin_Values[7][26][1] = 554; Phi_h_Bin_Values[7][26][2] = 4647;
    z_pT_Bin_Borders[7][27][0] = 0.7; z_pT_Bin_Borders[7][27][1] = 0.51; z_pT_Bin_Borders[7][27][2] = 0.38; z_pT_Bin_Borders[7][27][3] = 0.29;
    Phi_h_Bin_Values[7][27][0] =  24; Phi_h_Bin_Values[7][27][1] = 578; Phi_h_Bin_Values[7][27][2] = 4671;
    z_pT_Bin_Borders[7][28][0] = 0.7; z_pT_Bin_Borders[7][28][1] = 0.51; z_pT_Bin_Borders[7][28][2] = 0.48; z_pT_Bin_Borders[7][28][3] = 0.38;
    Phi_h_Bin_Values[7][28][0] =  24; Phi_h_Bin_Values[7][28][1] = 602; Phi_h_Bin_Values[7][28][2] = 4695;
    z_pT_Bin_Borders[7][29][0] = 0.7; z_pT_Bin_Borders[7][29][1] = 0.51; z_pT_Bin_Borders[7][29][2] = 0.6; z_pT_Bin_Borders[7][29][3] = 0.48;
    Phi_h_Bin_Values[7][29][0] =  1; Phi_h_Bin_Values[7][29][1] = 626; Phi_h_Bin_Values[7][29][2] = 4719;
    z_pT_Bin_Borders[7][30][0] = 0.7; z_pT_Bin_Borders[7][30][1] = 0.51; z_pT_Bin_Borders[7][30][2] = 0.83; z_pT_Bin_Borders[7][30][3] = 0.6;
    Phi_h_Bin_Values[7][30][0] =  1; Phi_h_Bin_Values[7][30][1] = 627; Phi_h_Bin_Values[7][30][2] = 4720;
    z_pT_Bin_Borders[7][31][0] = 0.22; z_pT_Bin_Borders[7][31][1] = 0; z_pT_Bin_Borders[7][31][2] = 0.05; z_pT_Bin_Borders[7][31][3] = 0;
    Phi_h_Bin_Values[7][31][0] =  1; Phi_h_Bin_Values[7][31][1] = 628; Phi_h_Bin_Values[7][31][2] = 4721;
    z_pT_Bin_Borders[7][32][0] = 0.22; z_pT_Bin_Borders[7][32][1] = 0; z_pT_Bin_Borders[7][32][2] = 0.05; z_pT_Bin_Borders[7][32][3] = 0.2;
    Phi_h_Bin_Values[7][32][0] =  1; Phi_h_Bin_Values[7][32][1] = 629; Phi_h_Bin_Values[7][32][2] = 4722;
    z_pT_Bin_Borders[7][33][0] = 0.22; z_pT_Bin_Borders[7][33][1] = 0; z_pT_Bin_Borders[7][33][2] = 0.2; z_pT_Bin_Borders[7][33][3] = 0.29;
    Phi_h_Bin_Values[7][33][0] =  1; Phi_h_Bin_Values[7][33][1] = 630; Phi_h_Bin_Values[7][33][2] = 4723;
    z_pT_Bin_Borders[7][34][0] = 0.22; z_pT_Bin_Borders[7][34][1] = 0; z_pT_Bin_Borders[7][34][2] = 0.29; z_pT_Bin_Borders[7][34][3] = 0.38;
    Phi_h_Bin_Values[7][34][0] =  1; Phi_h_Bin_Values[7][34][1] = 631; Phi_h_Bin_Values[7][34][2] = 4724;
    z_pT_Bin_Borders[7][35][0] = 0.22; z_pT_Bin_Borders[7][35][1] = 0; z_pT_Bin_Borders[7][35][2] = 0.38; z_pT_Bin_Borders[7][35][3] = 0.48;
    Phi_h_Bin_Values[7][35][0] =  1; Phi_h_Bin_Values[7][35][1] = 632; Phi_h_Bin_Values[7][35][2] = 4725;
    z_pT_Bin_Borders[7][36][0] = 0.22; z_pT_Bin_Borders[7][36][1] = 0; z_pT_Bin_Borders[7][36][2] = 0.48; z_pT_Bin_Borders[7][36][3] = 0.6;
    Phi_h_Bin_Values[7][36][0] =  1; Phi_h_Bin_Values[7][36][1] = 633; Phi_h_Bin_Values[7][36][2] = 4726;
    z_pT_Bin_Borders[7][37][0] = 0.22; z_pT_Bin_Borders[7][37][1] = 0; z_pT_Bin_Borders[7][37][2] = 0.6; z_pT_Bin_Borders[7][37][3] = 0.83;
    Phi_h_Bin_Values[7][37][0] =  1; Phi_h_Bin_Values[7][37][1] = 634; Phi_h_Bin_Values[7][37][2] = 4727;
    z_pT_Bin_Borders[7][38][0] = 0.22; z_pT_Bin_Borders[7][38][1] = 0; z_pT_Bin_Borders[7][38][2] = 10; z_pT_Bin_Borders[7][38][3] = 0.83;
    Phi_h_Bin_Values[7][38][0] =  1; Phi_h_Bin_Values[7][38][1] = 635; Phi_h_Bin_Values[7][38][2] = 4728;
    z_pT_Bin_Borders[7][39][0] = 0.22; z_pT_Bin_Borders[7][39][1] = 0.28; z_pT_Bin_Borders[7][39][2] = 0.05; z_pT_Bin_Borders[7][39][3] = 0;
    Phi_h_Bin_Values[7][39][0] =  1; Phi_h_Bin_Values[7][39][1] = 636; Phi_h_Bin_Values[7][39][2] = 4729;
    z_pT_Bin_Borders[7][40][0] = 0.22; z_pT_Bin_Borders[7][40][1] = 0.28; z_pT_Bin_Borders[7][40][2] = 10; z_pT_Bin_Borders[7][40][3] = 0.83;
    Phi_h_Bin_Values[7][40][0] =  1; Phi_h_Bin_Values[7][40][1] = 637; Phi_h_Bin_Values[7][40][2] = 4730;
    z_pT_Bin_Borders[7][41][0] = 0.28; z_pT_Bin_Borders[7][41][1] = 0.33; z_pT_Bin_Borders[7][41][2] = 0.05; z_pT_Bin_Borders[7][41][3] = 0;
    Phi_h_Bin_Values[7][41][0] =  1; Phi_h_Bin_Values[7][41][1] = 638; Phi_h_Bin_Values[7][41][2] = 4731;
    z_pT_Bin_Borders[7][42][0] = 0.28; z_pT_Bin_Borders[7][42][1] = 0.33; z_pT_Bin_Borders[7][42][2] = 10; z_pT_Bin_Borders[7][42][3] = 0.83;
    Phi_h_Bin_Values[7][42][0] =  1; Phi_h_Bin_Values[7][42][1] = 639; Phi_h_Bin_Values[7][42][2] = 4732;
    z_pT_Bin_Borders[7][43][0] = 0.33; z_pT_Bin_Borders[7][43][1] = 0.4; z_pT_Bin_Borders[7][43][2] = 0.05; z_pT_Bin_Borders[7][43][3] = 0;
    Phi_h_Bin_Values[7][43][0] =  1; Phi_h_Bin_Values[7][43][1] = 640; Phi_h_Bin_Values[7][43][2] = 4733;
    z_pT_Bin_Borders[7][44][0] = 0.33; z_pT_Bin_Borders[7][44][1] = 0.4; z_pT_Bin_Borders[7][44][2] = 10; z_pT_Bin_Borders[7][44][3] = 0.83;
    Phi_h_Bin_Values[7][44][0] =  1; Phi_h_Bin_Values[7][44][1] = 641; Phi_h_Bin_Values[7][44][2] = 4734;
    z_pT_Bin_Borders[7][45][0] = 0.4; z_pT_Bin_Borders[7][45][1] = 0.51; z_pT_Bin_Borders[7][45][2] = 0.05; z_pT_Bin_Borders[7][45][3] = 0;
    Phi_h_Bin_Values[7][45][0] =  1; Phi_h_Bin_Values[7][45][1] = 642; Phi_h_Bin_Values[7][45][2] = 4735;
    z_pT_Bin_Borders[7][46][0] = 0.4; z_pT_Bin_Borders[7][46][1] = 0.51; z_pT_Bin_Borders[7][46][2] = 10; z_pT_Bin_Borders[7][46][3] = 0.83;
    Phi_h_Bin_Values[7][46][0] =  1; Phi_h_Bin_Values[7][46][1] = 643; Phi_h_Bin_Values[7][46][2] = 4736;
    z_pT_Bin_Borders[7][47][0] = 0.51; z_pT_Bin_Borders[7][47][1] = 0.7; z_pT_Bin_Borders[7][47][2] = 0.05; z_pT_Bin_Borders[7][47][3] = 0;
    Phi_h_Bin_Values[7][47][0] =  1; Phi_h_Bin_Values[7][47][1] = 644; Phi_h_Bin_Values[7][47][2] = 4737;
    z_pT_Bin_Borders[7][48][0] = 0.51; z_pT_Bin_Borders[7][48][1] = 0.7; z_pT_Bin_Borders[7][48][2] = 10; z_pT_Bin_Borders[7][48][3] = 0.83;
    Phi_h_Bin_Values[7][48][0] =  1; Phi_h_Bin_Values[7][48][1] = 645; Phi_h_Bin_Values[7][48][2] = 4738;
    z_pT_Bin_Borders[7][49][0] = 10; z_pT_Bin_Borders[7][49][1] = 0.7; z_pT_Bin_Borders[7][49][2] = 0; z_pT_Bin_Borders[7][49][3] = 0.05;
    Phi_h_Bin_Values[7][49][0] =  1; Phi_h_Bin_Values[7][49][1] = 646; Phi_h_Bin_Values[7][49][2] = 4739;
    z_pT_Bin_Borders[7][50][0] = 10; z_pT_Bin_Borders[7][50][1] = 0.7; z_pT_Bin_Borders[7][50][2] = 0.05; z_pT_Bin_Borders[7][50][3] = 0.2;
    Phi_h_Bin_Values[7][50][0] =  1; Phi_h_Bin_Values[7][50][1] = 647; Phi_h_Bin_Values[7][50][2] = 4740;
    z_pT_Bin_Borders[7][51][0] = 10; z_pT_Bin_Borders[7][51][1] = 0.7; z_pT_Bin_Borders[7][51][2] = 0.2; z_pT_Bin_Borders[7][51][3] = 0.29;
    Phi_h_Bin_Values[7][51][0] =  1; Phi_h_Bin_Values[7][51][1] = 648; Phi_h_Bin_Values[7][51][2] = 4741;
    z_pT_Bin_Borders[7][52][0] = 10; z_pT_Bin_Borders[7][52][1] = 0.7; z_pT_Bin_Borders[7][52][2] = 0.29; z_pT_Bin_Borders[7][52][3] = 0.38;
    Phi_h_Bin_Values[7][52][0] =  1; Phi_h_Bin_Values[7][52][1] = 649; Phi_h_Bin_Values[7][52][2] = 4742;
    z_pT_Bin_Borders[7][53][0] = 10; z_pT_Bin_Borders[7][53][1] = 0.7; z_pT_Bin_Borders[7][53][2] = 0.38; z_pT_Bin_Borders[7][53][3] = 0.48;
    Phi_h_Bin_Values[7][53][0] =  1; Phi_h_Bin_Values[7][53][1] = 650; Phi_h_Bin_Values[7][53][2] = 4743;
    z_pT_Bin_Borders[7][54][0] = 10; z_pT_Bin_Borders[7][54][1] = 0.7; z_pT_Bin_Borders[7][54][2] = 0.48; z_pT_Bin_Borders[7][54][3] = 0.6;
    Phi_h_Bin_Values[7][54][0] =  1; Phi_h_Bin_Values[7][54][1] = 651; Phi_h_Bin_Values[7][54][2] = 4744;
    z_pT_Bin_Borders[7][55][0] = 10; z_pT_Bin_Borders[7][55][1] = 0.7; z_pT_Bin_Borders[7][55][2] = 0.6; z_pT_Bin_Borders[7][55][3] = 0.83;
    Phi_h_Bin_Values[7][55][0] =  1; Phi_h_Bin_Values[7][55][1] = 652; Phi_h_Bin_Values[7][55][2] = 4745;
    z_pT_Bin_Borders[7][56][0] = 10; z_pT_Bin_Borders[7][56][1] = 0.7; z_pT_Bin_Borders[7][56][2] = 10; z_pT_Bin_Borders[7][56][3] = 0.83;
    Phi_h_Bin_Values[7][56][0] =  1; Phi_h_Bin_Values[7][56][1] = 653; Phi_h_Bin_Values[7][56][2] = 4746;
    z_pT_Bin_Borders[8][1][0] = 0.32; z_pT_Bin_Borders[8][1][1] = 0.27; z_pT_Bin_Borders[8][1][2] = 0.21; z_pT_Bin_Borders[8][1][3] = 0.05;
    Phi_h_Bin_Values[8][1][0] =  24; Phi_h_Bin_Values[8][1][1] = 0; Phi_h_Bin_Values[8][1][2] = 4747;
    z_pT_Bin_Borders[8][2][0] = 0.32; z_pT_Bin_Borders[8][2][1] = 0.27; z_pT_Bin_Borders[8][2][2] = 0.31; z_pT_Bin_Borders[8][2][3] = 0.21;
    Phi_h_Bin_Values[8][2][0] =  24; Phi_h_Bin_Values[8][2][1] = 24; Phi_h_Bin_Values[8][2][2] = 4771;
    z_pT_Bin_Borders[8][3][0] = 0.32; z_pT_Bin_Borders[8][3][1] = 0.27; z_pT_Bin_Borders[8][3][2] = 0.4; z_pT_Bin_Borders[8][3][3] = 0.31;
    Phi_h_Bin_Values[8][3][0] =  24; Phi_h_Bin_Values[8][3][1] = 48; Phi_h_Bin_Values[8][3][2] = 4795;
    z_pT_Bin_Borders[8][4][0] = 0.32; z_pT_Bin_Borders[8][4][1] = 0.27; z_pT_Bin_Borders[8][4][2] = 0.5; z_pT_Bin_Borders[8][4][3] = 0.4;
    Phi_h_Bin_Values[8][4][0] =  24; Phi_h_Bin_Values[8][4][1] = 72; Phi_h_Bin_Values[8][4][2] = 4819;
    z_pT_Bin_Borders[8][5][0] = 0.36; z_pT_Bin_Borders[8][5][1] = 0.32; z_pT_Bin_Borders[8][5][2] = 0.21; z_pT_Bin_Borders[8][5][3] = 0.05;
    Phi_h_Bin_Values[8][5][0] =  24; Phi_h_Bin_Values[8][5][1] = 96; Phi_h_Bin_Values[8][5][2] = 4843;
    z_pT_Bin_Borders[8][6][0] = 0.36; z_pT_Bin_Borders[8][6][1] = 0.32; z_pT_Bin_Borders[8][6][2] = 0.31; z_pT_Bin_Borders[8][6][3] = 0.21;
    Phi_h_Bin_Values[8][6][0] =  24; Phi_h_Bin_Values[8][6][1] = 120; Phi_h_Bin_Values[8][6][2] = 4867;
    z_pT_Bin_Borders[8][7][0] = 0.36; z_pT_Bin_Borders[8][7][1] = 0.32; z_pT_Bin_Borders[8][7][2] = 0.4; z_pT_Bin_Borders[8][7][3] = 0.31;
    Phi_h_Bin_Values[8][7][0] =  24; Phi_h_Bin_Values[8][7][1] = 144; Phi_h_Bin_Values[8][7][2] = 4891;
    z_pT_Bin_Borders[8][8][0] = 0.36; z_pT_Bin_Borders[8][8][1] = 0.32; z_pT_Bin_Borders[8][8][2] = 0.5; z_pT_Bin_Borders[8][8][3] = 0.4;
    Phi_h_Bin_Values[8][8][0] =  24; Phi_h_Bin_Values[8][8][1] = 168; Phi_h_Bin_Values[8][8][2] = 4915;
    z_pT_Bin_Borders[8][9][0] = 0.4; z_pT_Bin_Borders[8][9][1] = 0.36; z_pT_Bin_Borders[8][9][2] = 0.21; z_pT_Bin_Borders[8][9][3] = 0.05;
    Phi_h_Bin_Values[8][9][0] =  24; Phi_h_Bin_Values[8][9][1] = 192; Phi_h_Bin_Values[8][9][2] = 4939;
    z_pT_Bin_Borders[8][10][0] = 0.4; z_pT_Bin_Borders[8][10][1] = 0.36; z_pT_Bin_Borders[8][10][2] = 0.31; z_pT_Bin_Borders[8][10][3] = 0.21;
    Phi_h_Bin_Values[8][10][0] =  24; Phi_h_Bin_Values[8][10][1] = 216; Phi_h_Bin_Values[8][10][2] = 4963;
    z_pT_Bin_Borders[8][11][0] = 0.4; z_pT_Bin_Borders[8][11][1] = 0.36; z_pT_Bin_Borders[8][11][2] = 0.4; z_pT_Bin_Borders[8][11][3] = 0.31;
    Phi_h_Bin_Values[8][11][0] =  24; Phi_h_Bin_Values[8][11][1] = 240; Phi_h_Bin_Values[8][11][2] = 4987;
    z_pT_Bin_Borders[8][12][0] = 0.4; z_pT_Bin_Borders[8][12][1] = 0.36; z_pT_Bin_Borders[8][12][2] = 0.5; z_pT_Bin_Borders[8][12][3] = 0.4;
    Phi_h_Bin_Values[8][12][0] =  24; Phi_h_Bin_Values[8][12][1] = 264; Phi_h_Bin_Values[8][12][2] = 5011;
    z_pT_Bin_Borders[8][13][0] = 0.45; z_pT_Bin_Borders[8][13][1] = 0.4; z_pT_Bin_Borders[8][13][2] = 0.21; z_pT_Bin_Borders[8][13][3] = 0.05;
    Phi_h_Bin_Values[8][13][0] =  24; Phi_h_Bin_Values[8][13][1] = 288; Phi_h_Bin_Values[8][13][2] = 5035;
    z_pT_Bin_Borders[8][14][0] = 0.45; z_pT_Bin_Borders[8][14][1] = 0.4; z_pT_Bin_Borders[8][14][2] = 0.31; z_pT_Bin_Borders[8][14][3] = 0.21;
    Phi_h_Bin_Values[8][14][0] =  24; Phi_h_Bin_Values[8][14][1] = 312; Phi_h_Bin_Values[8][14][2] = 5059;
    z_pT_Bin_Borders[8][15][0] = 0.45; z_pT_Bin_Borders[8][15][1] = 0.4; z_pT_Bin_Borders[8][15][2] = 0.4; z_pT_Bin_Borders[8][15][3] = 0.31;
    Phi_h_Bin_Values[8][15][0] =  24; Phi_h_Bin_Values[8][15][1] = 336; Phi_h_Bin_Values[8][15][2] = 5083;
    z_pT_Bin_Borders[8][16][0] = 0.45; z_pT_Bin_Borders[8][16][1] = 0.4; z_pT_Bin_Borders[8][16][2] = 0.5; z_pT_Bin_Borders[8][16][3] = 0.4;
    Phi_h_Bin_Values[8][16][0] =  24; Phi_h_Bin_Values[8][16][1] = 360; Phi_h_Bin_Values[8][16][2] = 5107;
    z_pT_Bin_Borders[8][17][0] = 0.5; z_pT_Bin_Borders[8][17][1] = 0.45; z_pT_Bin_Borders[8][17][2] = 0.21; z_pT_Bin_Borders[8][17][3] = 0.05;
    Phi_h_Bin_Values[8][17][0] =  24; Phi_h_Bin_Values[8][17][1] = 384; Phi_h_Bin_Values[8][17][2] = 5131;
    z_pT_Bin_Borders[8][18][0] = 0.5; z_pT_Bin_Borders[8][18][1] = 0.45; z_pT_Bin_Borders[8][18][2] = 0.31; z_pT_Bin_Borders[8][18][3] = 0.21;
    Phi_h_Bin_Values[8][18][0] =  24; Phi_h_Bin_Values[8][18][1] = 408; Phi_h_Bin_Values[8][18][2] = 5155;
    z_pT_Bin_Borders[8][19][0] = 0.5; z_pT_Bin_Borders[8][19][1] = 0.45; z_pT_Bin_Borders[8][19][2] = 0.4; z_pT_Bin_Borders[8][19][3] = 0.31;
    Phi_h_Bin_Values[8][19][0] =  24; Phi_h_Bin_Values[8][19][1] = 432; Phi_h_Bin_Values[8][19][2] = 5179;
    z_pT_Bin_Borders[8][20][0] = 0.5; z_pT_Bin_Borders[8][20][1] = 0.45; z_pT_Bin_Borders[8][20][2] = 0.5; z_pT_Bin_Borders[8][20][3] = 0.4;
    Phi_h_Bin_Values[8][20][0] =  24; Phi_h_Bin_Values[8][20][1] = 456; Phi_h_Bin_Values[8][20][2] = 5203;
    z_pT_Bin_Borders[8][21][0] = 0.6; z_pT_Bin_Borders[8][21][1] = 0.5; z_pT_Bin_Borders[8][21][2] = 0.21; z_pT_Bin_Borders[8][21][3] = 0.05;
    Phi_h_Bin_Values[8][21][0] =  24; Phi_h_Bin_Values[8][21][1] = 480; Phi_h_Bin_Values[8][21][2] = 5227;
    z_pT_Bin_Borders[8][22][0] = 0.6; z_pT_Bin_Borders[8][22][1] = 0.5; z_pT_Bin_Borders[8][22][2] = 0.31; z_pT_Bin_Borders[8][22][3] = 0.21;
    Phi_h_Bin_Values[8][22][0] =  24; Phi_h_Bin_Values[8][22][1] = 504; Phi_h_Bin_Values[8][22][2] = 5251;
    z_pT_Bin_Borders[8][23][0] = 0.6; z_pT_Bin_Borders[8][23][1] = 0.5; z_pT_Bin_Borders[8][23][2] = 0.4; z_pT_Bin_Borders[8][23][3] = 0.31;
    Phi_h_Bin_Values[8][23][0] =  1; Phi_h_Bin_Values[8][23][1] = 528; Phi_h_Bin_Values[8][23][2] = 5275;
    z_pT_Bin_Borders[8][24][0] = 0.6; z_pT_Bin_Borders[8][24][1] = 0.5; z_pT_Bin_Borders[8][24][2] = 0.5; z_pT_Bin_Borders[8][24][3] = 0.4;
    Phi_h_Bin_Values[8][24][0] =  1; Phi_h_Bin_Values[8][24][1] = 529; Phi_h_Bin_Values[8][24][2] = 5276;
    z_pT_Bin_Borders[8][25][0] = 0.27; z_pT_Bin_Borders[8][25][1] = 0; z_pT_Bin_Borders[8][25][2] = 0.05; z_pT_Bin_Borders[8][25][3] = 0;
    Phi_h_Bin_Values[8][25][0] =  1; Phi_h_Bin_Values[8][25][1] = 530; Phi_h_Bin_Values[8][25][2] = 5277;
    z_pT_Bin_Borders[8][26][0] = 0.27; z_pT_Bin_Borders[8][26][1] = 0; z_pT_Bin_Borders[8][26][2] = 0.05; z_pT_Bin_Borders[8][26][3] = 0.21;
    Phi_h_Bin_Values[8][26][0] =  1; Phi_h_Bin_Values[8][26][1] = 531; Phi_h_Bin_Values[8][26][2] = 5278;
    z_pT_Bin_Borders[8][27][0] = 0.27; z_pT_Bin_Borders[8][27][1] = 0; z_pT_Bin_Borders[8][27][2] = 0.21; z_pT_Bin_Borders[8][27][3] = 0.31;
    Phi_h_Bin_Values[8][27][0] =  1; Phi_h_Bin_Values[8][27][1] = 532; Phi_h_Bin_Values[8][27][2] = 5279;
    z_pT_Bin_Borders[8][28][0] = 0.27; z_pT_Bin_Borders[8][28][1] = 0; z_pT_Bin_Borders[8][28][2] = 0.31; z_pT_Bin_Borders[8][28][3] = 0.4;
    Phi_h_Bin_Values[8][28][0] =  1; Phi_h_Bin_Values[8][28][1] = 533; Phi_h_Bin_Values[8][28][2] = 5280;
    z_pT_Bin_Borders[8][29][0] = 0.27; z_pT_Bin_Borders[8][29][1] = 0; z_pT_Bin_Borders[8][29][2] = 0.4; z_pT_Bin_Borders[8][29][3] = 0.5;
    Phi_h_Bin_Values[8][29][0] =  1; Phi_h_Bin_Values[8][29][1] = 534; Phi_h_Bin_Values[8][29][2] = 5281;
    z_pT_Bin_Borders[8][30][0] = 0.27; z_pT_Bin_Borders[8][30][1] = 0; z_pT_Bin_Borders[8][30][2] = 10; z_pT_Bin_Borders[8][30][3] = 0.5;
    Phi_h_Bin_Values[8][30][0] =  1; Phi_h_Bin_Values[8][30][1] = 535; Phi_h_Bin_Values[8][30][2] = 5282;
    z_pT_Bin_Borders[8][31][0] = 0.27; z_pT_Bin_Borders[8][31][1] = 0.32; z_pT_Bin_Borders[8][31][2] = 0.05; z_pT_Bin_Borders[8][31][3] = 0;
    Phi_h_Bin_Values[8][31][0] =  1; Phi_h_Bin_Values[8][31][1] = 536; Phi_h_Bin_Values[8][31][2] = 5283;
    z_pT_Bin_Borders[8][32][0] = 0.27; z_pT_Bin_Borders[8][32][1] = 0.32; z_pT_Bin_Borders[8][32][2] = 10; z_pT_Bin_Borders[8][32][3] = 0.5;
    Phi_h_Bin_Values[8][32][0] =  1; Phi_h_Bin_Values[8][32][1] = 537; Phi_h_Bin_Values[8][32][2] = 5284;
    z_pT_Bin_Borders[8][33][0] = 0.32; z_pT_Bin_Borders[8][33][1] = 0.36; z_pT_Bin_Borders[8][33][2] = 0.05; z_pT_Bin_Borders[8][33][3] = 0;
    Phi_h_Bin_Values[8][33][0] =  1; Phi_h_Bin_Values[8][33][1] = 538; Phi_h_Bin_Values[8][33][2] = 5285;
    z_pT_Bin_Borders[8][34][0] = 0.32; z_pT_Bin_Borders[8][34][1] = 0.36; z_pT_Bin_Borders[8][34][2] = 10; z_pT_Bin_Borders[8][34][3] = 0.5;
    Phi_h_Bin_Values[8][34][0] =  1; Phi_h_Bin_Values[8][34][1] = 539; Phi_h_Bin_Values[8][34][2] = 5286;
    z_pT_Bin_Borders[8][35][0] = 0.36; z_pT_Bin_Borders[8][35][1] = 0.4; z_pT_Bin_Borders[8][35][2] = 0.05; z_pT_Bin_Borders[8][35][3] = 0;
    Phi_h_Bin_Values[8][35][0] =  1; Phi_h_Bin_Values[8][35][1] = 540; Phi_h_Bin_Values[8][35][2] = 5287;
    z_pT_Bin_Borders[8][36][0] = 0.36; z_pT_Bin_Borders[8][36][1] = 0.4; z_pT_Bin_Borders[8][36][2] = 10; z_pT_Bin_Borders[8][36][3] = 0.5;
    Phi_h_Bin_Values[8][36][0] =  1; Phi_h_Bin_Values[8][36][1] = 541; Phi_h_Bin_Values[8][36][2] = 5288;
    z_pT_Bin_Borders[8][37][0] = 0.4; z_pT_Bin_Borders[8][37][1] = 0.45; z_pT_Bin_Borders[8][37][2] = 0.05; z_pT_Bin_Borders[8][37][3] = 0;
    Phi_h_Bin_Values[8][37][0] =  1; Phi_h_Bin_Values[8][37][1] = 542; Phi_h_Bin_Values[8][37][2] = 5289;
    z_pT_Bin_Borders[8][38][0] = 0.4; z_pT_Bin_Borders[8][38][1] = 0.45; z_pT_Bin_Borders[8][38][2] = 10; z_pT_Bin_Borders[8][38][3] = 0.5;
    Phi_h_Bin_Values[8][38][0] =  1; Phi_h_Bin_Values[8][38][1] = 543; Phi_h_Bin_Values[8][38][2] = 5290;
    z_pT_Bin_Borders[8][39][0] = 0.45; z_pT_Bin_Borders[8][39][1] = 0.5; z_pT_Bin_Borders[8][39][2] = 0.05; z_pT_Bin_Borders[8][39][3] = 0;
    Phi_h_Bin_Values[8][39][0] =  1; Phi_h_Bin_Values[8][39][1] = 544; Phi_h_Bin_Values[8][39][2] = 5291;
    z_pT_Bin_Borders[8][40][0] = 0.45; z_pT_Bin_Borders[8][40][1] = 0.5; z_pT_Bin_Borders[8][40][2] = 10; z_pT_Bin_Borders[8][40][3] = 0.5;
    Phi_h_Bin_Values[8][40][0] =  1; Phi_h_Bin_Values[8][40][1] = 545; Phi_h_Bin_Values[8][40][2] = 5292;
    z_pT_Bin_Borders[8][41][0] = 0.5; z_pT_Bin_Borders[8][41][1] = 0.6; z_pT_Bin_Borders[8][41][2] = 0.05; z_pT_Bin_Borders[8][41][3] = 0;
    Phi_h_Bin_Values[8][41][0] =  1; Phi_h_Bin_Values[8][41][1] = 546; Phi_h_Bin_Values[8][41][2] = 5293;
    z_pT_Bin_Borders[8][42][0] = 0.5; z_pT_Bin_Borders[8][42][1] = 0.6; z_pT_Bin_Borders[8][42][2] = 10; z_pT_Bin_Borders[8][42][3] = 0.5;
    Phi_h_Bin_Values[8][42][0] =  1; Phi_h_Bin_Values[8][42][1] = 547; Phi_h_Bin_Values[8][42][2] = 5294;
    z_pT_Bin_Borders[8][43][0] = 10; z_pT_Bin_Borders[8][43][1] = 0.6; z_pT_Bin_Borders[8][43][2] = 0; z_pT_Bin_Borders[8][43][3] = 0.05;
    Phi_h_Bin_Values[8][43][0] =  1; Phi_h_Bin_Values[8][43][1] = 548; Phi_h_Bin_Values[8][43][2] = 5295;
    z_pT_Bin_Borders[8][44][0] = 10; z_pT_Bin_Borders[8][44][1] = 0.6; z_pT_Bin_Borders[8][44][2] = 0.05; z_pT_Bin_Borders[8][44][3] = 0.21;
    Phi_h_Bin_Values[8][44][0] =  1; Phi_h_Bin_Values[8][44][1] = 549; Phi_h_Bin_Values[8][44][2] = 5296;
    z_pT_Bin_Borders[8][45][0] = 10; z_pT_Bin_Borders[8][45][1] = 0.6; z_pT_Bin_Borders[8][45][2] = 0.21; z_pT_Bin_Borders[8][45][3] = 0.31;
    Phi_h_Bin_Values[8][45][0] =  1; Phi_h_Bin_Values[8][45][1] = 550; Phi_h_Bin_Values[8][45][2] = 5297;
    z_pT_Bin_Borders[8][46][0] = 10; z_pT_Bin_Borders[8][46][1] = 0.6; z_pT_Bin_Borders[8][46][2] = 0.31; z_pT_Bin_Borders[8][46][3] = 0.4;
    Phi_h_Bin_Values[8][46][0] =  1; Phi_h_Bin_Values[8][46][1] = 551; Phi_h_Bin_Values[8][46][2] = 5298;
    z_pT_Bin_Borders[8][47][0] = 10; z_pT_Bin_Borders[8][47][1] = 0.6; z_pT_Bin_Borders[8][47][2] = 0.4; z_pT_Bin_Borders[8][47][3] = 0.5;
    Phi_h_Bin_Values[8][47][0] =  1; Phi_h_Bin_Values[8][47][1] = 552; Phi_h_Bin_Values[8][47][2] = 5299;
    z_pT_Bin_Borders[8][48][0] = 10; z_pT_Bin_Borders[8][48][1] = 0.6; z_pT_Bin_Borders[8][48][2] = 10; z_pT_Bin_Borders[8][48][3] = 0.5;
    Phi_h_Bin_Values[8][48][0] =  1; Phi_h_Bin_Values[8][48][1] = 553; Phi_h_Bin_Values[8][48][2] = 5300;
    z_pT_Bin_Borders[9][1][0] = 0.2; z_pT_Bin_Borders[9][1][1] = 0.16; z_pT_Bin_Borders[9][1][2] = 0.22; z_pT_Bin_Borders[9][1][3] = 0.05;
    Phi_h_Bin_Values[9][1][0] =  24; Phi_h_Bin_Values[9][1][1] = 0; Phi_h_Bin_Values[9][1][2] = 5301;
    z_pT_Bin_Borders[9][2][0] = 0.2; z_pT_Bin_Borders[9][2][1] = 0.16; z_pT_Bin_Borders[9][2][2] = 0.3; z_pT_Bin_Borders[9][2][3] = 0.22;
    Phi_h_Bin_Values[9][2][0] =  24; Phi_h_Bin_Values[9][2][1] = 24; Phi_h_Bin_Values[9][2][2] = 5325;
    z_pT_Bin_Borders[9][3][0] = 0.2; z_pT_Bin_Borders[9][3][1] = 0.16; z_pT_Bin_Borders[9][3][2] = 0.38; z_pT_Bin_Borders[9][3][3] = 0.3;
    Phi_h_Bin_Values[9][3][0] =  24; Phi_h_Bin_Values[9][3][1] = 48; Phi_h_Bin_Values[9][3][2] = 5349;
    z_pT_Bin_Borders[9][4][0] = 0.2; z_pT_Bin_Borders[9][4][1] = 0.16; z_pT_Bin_Borders[9][4][2] = 0.46; z_pT_Bin_Borders[9][4][3] = 0.38;
    Phi_h_Bin_Values[9][4][0] =  24; Phi_h_Bin_Values[9][4][1] = 72; Phi_h_Bin_Values[9][4][2] = 5373;
    z_pT_Bin_Borders[9][5][0] = 0.2; z_pT_Bin_Borders[9][5][1] = 0.16; z_pT_Bin_Borders[9][5][2] = 0.58; z_pT_Bin_Borders[9][5][3] = 0.46;
    Phi_h_Bin_Values[9][5][0] =  24; Phi_h_Bin_Values[9][5][1] = 96; Phi_h_Bin_Values[9][5][2] = 5397;
    z_pT_Bin_Borders[9][6][0] = 0.2; z_pT_Bin_Borders[9][6][1] = 0.16; z_pT_Bin_Borders[9][6][2] = 0.74; z_pT_Bin_Borders[9][6][3] = 0.58;
    Phi_h_Bin_Values[9][6][0] =  1; Phi_h_Bin_Values[9][6][1] = 120; Phi_h_Bin_Values[9][6][2] = 5421;
    z_pT_Bin_Borders[9][7][0] = 0.2; z_pT_Bin_Borders[9][7][1] = 0.16; z_pT_Bin_Borders[9][7][2] = 0.95; z_pT_Bin_Borders[9][7][3] = 0.74;
    Phi_h_Bin_Values[9][7][0] =  1; Phi_h_Bin_Values[9][7][1] = 121; Phi_h_Bin_Values[9][7][2] = 5422;
    z_pT_Bin_Borders[9][8][0] = 0.24; z_pT_Bin_Borders[9][8][1] = 0.2; z_pT_Bin_Borders[9][8][2] = 0.22; z_pT_Bin_Borders[9][8][3] = 0.05;
    Phi_h_Bin_Values[9][8][0] =  24; Phi_h_Bin_Values[9][8][1] = 122; Phi_h_Bin_Values[9][8][2] = 5423;
    z_pT_Bin_Borders[9][9][0] = 0.24; z_pT_Bin_Borders[9][9][1] = 0.2; z_pT_Bin_Borders[9][9][2] = 0.3; z_pT_Bin_Borders[9][9][3] = 0.22;
    Phi_h_Bin_Values[9][9][0] =  24; Phi_h_Bin_Values[9][9][1] = 146; Phi_h_Bin_Values[9][9][2] = 5447;
    z_pT_Bin_Borders[9][10][0] = 0.24; z_pT_Bin_Borders[9][10][1] = 0.2; z_pT_Bin_Borders[9][10][2] = 0.38; z_pT_Bin_Borders[9][10][3] = 0.3;
    Phi_h_Bin_Values[9][10][0] =  24; Phi_h_Bin_Values[9][10][1] = 170; Phi_h_Bin_Values[9][10][2] = 5471;
    z_pT_Bin_Borders[9][11][0] = 0.24; z_pT_Bin_Borders[9][11][1] = 0.2; z_pT_Bin_Borders[9][11][2] = 0.46; z_pT_Bin_Borders[9][11][3] = 0.38;
    Phi_h_Bin_Values[9][11][0] =  24; Phi_h_Bin_Values[9][11][1] = 194; Phi_h_Bin_Values[9][11][2] = 5495;
    z_pT_Bin_Borders[9][12][0] = 0.24; z_pT_Bin_Borders[9][12][1] = 0.2; z_pT_Bin_Borders[9][12][2] = 0.58; z_pT_Bin_Borders[9][12][3] = 0.46;
    Phi_h_Bin_Values[9][12][0] =  24; Phi_h_Bin_Values[9][12][1] = 218; Phi_h_Bin_Values[9][12][2] = 5519;
    z_pT_Bin_Borders[9][13][0] = 0.24; z_pT_Bin_Borders[9][13][1] = 0.2; z_pT_Bin_Borders[9][13][2] = 0.74; z_pT_Bin_Borders[9][13][3] = 0.58;
    Phi_h_Bin_Values[9][13][0] =  1; Phi_h_Bin_Values[9][13][1] = 242; Phi_h_Bin_Values[9][13][2] = 5543;
    z_pT_Bin_Borders[9][14][0] = 0.24; z_pT_Bin_Borders[9][14][1] = 0.2; z_pT_Bin_Borders[9][14][2] = 0.95; z_pT_Bin_Borders[9][14][3] = 0.74;
    Phi_h_Bin_Values[9][14][0] =  1; Phi_h_Bin_Values[9][14][1] = 243; Phi_h_Bin_Values[9][14][2] = 5544;
    z_pT_Bin_Borders[9][15][0] = 0.3; z_pT_Bin_Borders[9][15][1] = 0.24; z_pT_Bin_Borders[9][15][2] = 0.22; z_pT_Bin_Borders[9][15][3] = 0.05;
    Phi_h_Bin_Values[9][15][0] =  24; Phi_h_Bin_Values[9][15][1] = 244; Phi_h_Bin_Values[9][15][2] = 5545;
    z_pT_Bin_Borders[9][16][0] = 0.3; z_pT_Bin_Borders[9][16][1] = 0.24; z_pT_Bin_Borders[9][16][2] = 0.3; z_pT_Bin_Borders[9][16][3] = 0.22;
    Phi_h_Bin_Values[9][16][0] =  24; Phi_h_Bin_Values[9][16][1] = 268; Phi_h_Bin_Values[9][16][2] = 5569;
    z_pT_Bin_Borders[9][17][0] = 0.3; z_pT_Bin_Borders[9][17][1] = 0.24; z_pT_Bin_Borders[9][17][2] = 0.38; z_pT_Bin_Borders[9][17][3] = 0.3;
    Phi_h_Bin_Values[9][17][0] =  24; Phi_h_Bin_Values[9][17][1] = 292; Phi_h_Bin_Values[9][17][2] = 5593;
    z_pT_Bin_Borders[9][18][0] = 0.3; z_pT_Bin_Borders[9][18][1] = 0.24; z_pT_Bin_Borders[9][18][2] = 0.46; z_pT_Bin_Borders[9][18][3] = 0.38;
    Phi_h_Bin_Values[9][18][0] =  24; Phi_h_Bin_Values[9][18][1] = 316; Phi_h_Bin_Values[9][18][2] = 5617;
    z_pT_Bin_Borders[9][19][0] = 0.3; z_pT_Bin_Borders[9][19][1] = 0.24; z_pT_Bin_Borders[9][19][2] = 0.58; z_pT_Bin_Borders[9][19][3] = 0.46;
    Phi_h_Bin_Values[9][19][0] =  24; Phi_h_Bin_Values[9][19][1] = 340; Phi_h_Bin_Values[9][19][2] = 5641;
    z_pT_Bin_Borders[9][20][0] = 0.3; z_pT_Bin_Borders[9][20][1] = 0.24; z_pT_Bin_Borders[9][20][2] = 0.74; z_pT_Bin_Borders[9][20][3] = 0.58;
    Phi_h_Bin_Values[9][20][0] =  24; Phi_h_Bin_Values[9][20][1] = 364; Phi_h_Bin_Values[9][20][2] = 5665;
    z_pT_Bin_Borders[9][21][0] = 0.3; z_pT_Bin_Borders[9][21][1] = 0.24; z_pT_Bin_Borders[9][21][2] = 0.95; z_pT_Bin_Borders[9][21][3] = 0.74;
    Phi_h_Bin_Values[9][21][0] =  1; Phi_h_Bin_Values[9][21][1] = 388; Phi_h_Bin_Values[9][21][2] = 5689;
    z_pT_Bin_Borders[9][22][0] = 0.42; z_pT_Bin_Borders[9][22][1] = 0.3; z_pT_Bin_Borders[9][22][2] = 0.22; z_pT_Bin_Borders[9][22][3] = 0.05;
    Phi_h_Bin_Values[9][22][0] =  24; Phi_h_Bin_Values[9][22][1] = 389; Phi_h_Bin_Values[9][22][2] = 5690;
    z_pT_Bin_Borders[9][23][0] = 0.42; z_pT_Bin_Borders[9][23][1] = 0.3; z_pT_Bin_Borders[9][23][2] = 0.3; z_pT_Bin_Borders[9][23][3] = 0.22;
    Phi_h_Bin_Values[9][23][0] =  24; Phi_h_Bin_Values[9][23][1] = 413; Phi_h_Bin_Values[9][23][2] = 5714;
    z_pT_Bin_Borders[9][24][0] = 0.42; z_pT_Bin_Borders[9][24][1] = 0.3; z_pT_Bin_Borders[9][24][2] = 0.38; z_pT_Bin_Borders[9][24][3] = 0.3;
    Phi_h_Bin_Values[9][24][0] =  24; Phi_h_Bin_Values[9][24][1] = 437; Phi_h_Bin_Values[9][24][2] = 5738;
    z_pT_Bin_Borders[9][25][0] = 0.42; z_pT_Bin_Borders[9][25][1] = 0.3; z_pT_Bin_Borders[9][25][2] = 0.46; z_pT_Bin_Borders[9][25][3] = 0.38;
    Phi_h_Bin_Values[9][25][0] =  24; Phi_h_Bin_Values[9][25][1] = 461; Phi_h_Bin_Values[9][25][2] = 5762;
    z_pT_Bin_Borders[9][26][0] = 0.42; z_pT_Bin_Borders[9][26][1] = 0.3; z_pT_Bin_Borders[9][26][2] = 0.58; z_pT_Bin_Borders[9][26][3] = 0.46;
    Phi_h_Bin_Values[9][26][0] =  24; Phi_h_Bin_Values[9][26][1] = 485; Phi_h_Bin_Values[9][26][2] = 5786;
    z_pT_Bin_Borders[9][27][0] = 0.42; z_pT_Bin_Borders[9][27][1] = 0.3; z_pT_Bin_Borders[9][27][2] = 0.74; z_pT_Bin_Borders[9][27][3] = 0.58;
    Phi_h_Bin_Values[9][27][0] =  24; Phi_h_Bin_Values[9][27][1] = 509; Phi_h_Bin_Values[9][27][2] = 5810;
    z_pT_Bin_Borders[9][28][0] = 0.42; z_pT_Bin_Borders[9][28][1] = 0.3; z_pT_Bin_Borders[9][28][2] = 0.95; z_pT_Bin_Borders[9][28][3] = 0.74;
    Phi_h_Bin_Values[9][28][0] =  24; Phi_h_Bin_Values[9][28][1] = 533; Phi_h_Bin_Values[9][28][2] = 5834;
    z_pT_Bin_Borders[9][29][0] = 0.7; z_pT_Bin_Borders[9][29][1] = 0.42; z_pT_Bin_Borders[9][29][2] = 0.22; z_pT_Bin_Borders[9][29][3] = 0.05;
    Phi_h_Bin_Values[9][29][0] =  24; Phi_h_Bin_Values[9][29][1] = 557; Phi_h_Bin_Values[9][29][2] = 5858;
    z_pT_Bin_Borders[9][30][0] = 0.7; z_pT_Bin_Borders[9][30][1] = 0.42; z_pT_Bin_Borders[9][30][2] = 0.3; z_pT_Bin_Borders[9][30][3] = 0.22;
    Phi_h_Bin_Values[9][30][0] =  24; Phi_h_Bin_Values[9][30][1] = 581; Phi_h_Bin_Values[9][30][2] = 5882;
    z_pT_Bin_Borders[9][31][0] = 0.7; z_pT_Bin_Borders[9][31][1] = 0.42; z_pT_Bin_Borders[9][31][2] = 0.38; z_pT_Bin_Borders[9][31][3] = 0.3;
    Phi_h_Bin_Values[9][31][0] =  24; Phi_h_Bin_Values[9][31][1] = 605; Phi_h_Bin_Values[9][31][2] = 5906;
    z_pT_Bin_Borders[9][32][0] = 0.7; z_pT_Bin_Borders[9][32][1] = 0.42; z_pT_Bin_Borders[9][32][2] = 0.46; z_pT_Bin_Borders[9][32][3] = 0.38;
    Phi_h_Bin_Values[9][32][0] =  24; Phi_h_Bin_Values[9][32][1] = 629; Phi_h_Bin_Values[9][32][2] = 5930;
    z_pT_Bin_Borders[9][33][0] = 0.7; z_pT_Bin_Borders[9][33][1] = 0.42; z_pT_Bin_Borders[9][33][2] = 0.58; z_pT_Bin_Borders[9][33][3] = 0.46;
    Phi_h_Bin_Values[9][33][0] =  24; Phi_h_Bin_Values[9][33][1] = 653; Phi_h_Bin_Values[9][33][2] = 5954;
    z_pT_Bin_Borders[9][34][0] = 0.7; z_pT_Bin_Borders[9][34][1] = 0.42; z_pT_Bin_Borders[9][34][2] = 0.74; z_pT_Bin_Borders[9][34][3] = 0.58;
    Phi_h_Bin_Values[9][34][0] =  24; Phi_h_Bin_Values[9][34][1] = 677; Phi_h_Bin_Values[9][34][2] = 5978;
    z_pT_Bin_Borders[9][35][0] = 0.7; z_pT_Bin_Borders[9][35][1] = 0.42; z_pT_Bin_Borders[9][35][2] = 0.95; z_pT_Bin_Borders[9][35][3] = 0.74;
    Phi_h_Bin_Values[9][35][0] =  24; Phi_h_Bin_Values[9][35][1] = 701; Phi_h_Bin_Values[9][35][2] = 6002;
    z_pT_Bin_Borders[9][36][0] = 0.16; z_pT_Bin_Borders[9][36][1] = 0; z_pT_Bin_Borders[9][36][2] = 0.05; z_pT_Bin_Borders[9][36][3] = 0;
    Phi_h_Bin_Values[9][36][0] =  1; Phi_h_Bin_Values[9][36][1] = 725; Phi_h_Bin_Values[9][36][2] = 6026;
    z_pT_Bin_Borders[9][37][0] = 0.16; z_pT_Bin_Borders[9][37][1] = 0; z_pT_Bin_Borders[9][37][2] = 0.05; z_pT_Bin_Borders[9][37][3] = 0.22;
    Phi_h_Bin_Values[9][37][0] =  1; Phi_h_Bin_Values[9][37][1] = 726; Phi_h_Bin_Values[9][37][2] = 6027;
    z_pT_Bin_Borders[9][38][0] = 0.16; z_pT_Bin_Borders[9][38][1] = 0; z_pT_Bin_Borders[9][38][2] = 0.22; z_pT_Bin_Borders[9][38][3] = 0.3;
    Phi_h_Bin_Values[9][38][0] =  1; Phi_h_Bin_Values[9][38][1] = 727; Phi_h_Bin_Values[9][38][2] = 6028;
    z_pT_Bin_Borders[9][39][0] = 0.16; z_pT_Bin_Borders[9][39][1] = 0; z_pT_Bin_Borders[9][39][2] = 0.3; z_pT_Bin_Borders[9][39][3] = 0.38;
    Phi_h_Bin_Values[9][39][0] =  1; Phi_h_Bin_Values[9][39][1] = 728; Phi_h_Bin_Values[9][39][2] = 6029;
    z_pT_Bin_Borders[9][40][0] = 0.16; z_pT_Bin_Borders[9][40][1] = 0; z_pT_Bin_Borders[9][40][2] = 0.38; z_pT_Bin_Borders[9][40][3] = 0.46;
    Phi_h_Bin_Values[9][40][0] =  1; Phi_h_Bin_Values[9][40][1] = 729; Phi_h_Bin_Values[9][40][2] = 6030;
    z_pT_Bin_Borders[9][41][0] = 0.16; z_pT_Bin_Borders[9][41][1] = 0; z_pT_Bin_Borders[9][41][2] = 0.46; z_pT_Bin_Borders[9][41][3] = 0.58;
    Phi_h_Bin_Values[9][41][0] =  1; Phi_h_Bin_Values[9][41][1] = 730; Phi_h_Bin_Values[9][41][2] = 6031;
    z_pT_Bin_Borders[9][42][0] = 0.16; z_pT_Bin_Borders[9][42][1] = 0; z_pT_Bin_Borders[9][42][2] = 0.58; z_pT_Bin_Borders[9][42][3] = 0.74;
    Phi_h_Bin_Values[9][42][0] =  1; Phi_h_Bin_Values[9][42][1] = 731; Phi_h_Bin_Values[9][42][2] = 6032;
    z_pT_Bin_Borders[9][43][0] = 0.16; z_pT_Bin_Borders[9][43][1] = 0; z_pT_Bin_Borders[9][43][2] = 0.74; z_pT_Bin_Borders[9][43][3] = 0.95;
    Phi_h_Bin_Values[9][43][0] =  1; Phi_h_Bin_Values[9][43][1] = 732; Phi_h_Bin_Values[9][43][2] = 6033;
    z_pT_Bin_Borders[9][44][0] = 0.16; z_pT_Bin_Borders[9][44][1] = 0; z_pT_Bin_Borders[9][44][2] = 10; z_pT_Bin_Borders[9][44][3] = 0.95;
    Phi_h_Bin_Values[9][44][0] =  1; Phi_h_Bin_Values[9][44][1] = 733; Phi_h_Bin_Values[9][44][2] = 6034;
    z_pT_Bin_Borders[9][45][0] = 0.16; z_pT_Bin_Borders[9][45][1] = 0.2; z_pT_Bin_Borders[9][45][2] = 0.05; z_pT_Bin_Borders[9][45][3] = 0;
    Phi_h_Bin_Values[9][45][0] =  1; Phi_h_Bin_Values[9][45][1] = 734; Phi_h_Bin_Values[9][45][2] = 6035;
    z_pT_Bin_Borders[9][46][0] = 0.16; z_pT_Bin_Borders[9][46][1] = 0.2; z_pT_Bin_Borders[9][46][2] = 10; z_pT_Bin_Borders[9][46][3] = 0.95;
    Phi_h_Bin_Values[9][46][0] =  1; Phi_h_Bin_Values[9][46][1] = 735; Phi_h_Bin_Values[9][46][2] = 6036;
    z_pT_Bin_Borders[9][47][0] = 0.2; z_pT_Bin_Borders[9][47][1] = 0.24; z_pT_Bin_Borders[9][47][2] = 0.05; z_pT_Bin_Borders[9][47][3] = 0;
    Phi_h_Bin_Values[9][47][0] =  1; Phi_h_Bin_Values[9][47][1] = 736; Phi_h_Bin_Values[9][47][2] = 6037;
    z_pT_Bin_Borders[9][48][0] = 0.2; z_pT_Bin_Borders[9][48][1] = 0.24; z_pT_Bin_Borders[9][48][2] = 10; z_pT_Bin_Borders[9][48][3] = 0.95;
    Phi_h_Bin_Values[9][48][0] =  1; Phi_h_Bin_Values[9][48][1] = 737; Phi_h_Bin_Values[9][48][2] = 6038;
    z_pT_Bin_Borders[9][49][0] = 0.24; z_pT_Bin_Borders[9][49][1] = 0.3; z_pT_Bin_Borders[9][49][2] = 0.05; z_pT_Bin_Borders[9][49][3] = 0;
    Phi_h_Bin_Values[9][49][0] =  1; Phi_h_Bin_Values[9][49][1] = 738; Phi_h_Bin_Values[9][49][2] = 6039;
    z_pT_Bin_Borders[9][50][0] = 0.24; z_pT_Bin_Borders[9][50][1] = 0.3; z_pT_Bin_Borders[9][50][2] = 10; z_pT_Bin_Borders[9][50][3] = 0.95;
    Phi_h_Bin_Values[9][50][0] =  1; Phi_h_Bin_Values[9][50][1] = 739; Phi_h_Bin_Values[9][50][2] = 6040;
    z_pT_Bin_Borders[9][51][0] = 0.3; z_pT_Bin_Borders[9][51][1] = 0.42; z_pT_Bin_Borders[9][51][2] = 0.05; z_pT_Bin_Borders[9][51][3] = 0;
    Phi_h_Bin_Values[9][51][0] =  1; Phi_h_Bin_Values[9][51][1] = 740; Phi_h_Bin_Values[9][51][2] = 6041;
    z_pT_Bin_Borders[9][52][0] = 0.3; z_pT_Bin_Borders[9][52][1] = 0.42; z_pT_Bin_Borders[9][52][2] = 10; z_pT_Bin_Borders[9][52][3] = 0.95;
    Phi_h_Bin_Values[9][52][0] =  1; Phi_h_Bin_Values[9][52][1] = 741; Phi_h_Bin_Values[9][52][2] = 6042;
    z_pT_Bin_Borders[9][53][0] = 0.42; z_pT_Bin_Borders[9][53][1] = 0.7; z_pT_Bin_Borders[9][53][2] = 0.05; z_pT_Bin_Borders[9][53][3] = 0;
    Phi_h_Bin_Values[9][53][0] =  1; Phi_h_Bin_Values[9][53][1] = 742; Phi_h_Bin_Values[9][53][2] = 6043;
    z_pT_Bin_Borders[9][54][0] = 0.42; z_pT_Bin_Borders[9][54][1] = 0.7; z_pT_Bin_Borders[9][54][2] = 10; z_pT_Bin_Borders[9][54][3] = 0.95;
    Phi_h_Bin_Values[9][54][0] =  1; Phi_h_Bin_Values[9][54][1] = 743; Phi_h_Bin_Values[9][54][2] = 6044;
    z_pT_Bin_Borders[9][55][0] = 10; z_pT_Bin_Borders[9][55][1] = 0.7; z_pT_Bin_Borders[9][55][2] = 0; z_pT_Bin_Borders[9][55][3] = 0.05;
    Phi_h_Bin_Values[9][55][0] =  1; Phi_h_Bin_Values[9][55][1] = 744; Phi_h_Bin_Values[9][55][2] = 6045;
    z_pT_Bin_Borders[9][56][0] = 10; z_pT_Bin_Borders[9][56][1] = 0.7; z_pT_Bin_Borders[9][56][2] = 0.05; z_pT_Bin_Borders[9][56][3] = 0.22;
    Phi_h_Bin_Values[9][56][0] =  1; Phi_h_Bin_Values[9][56][1] = 745; Phi_h_Bin_Values[9][56][2] = 6046;
    z_pT_Bin_Borders[9][57][0] = 10; z_pT_Bin_Borders[9][57][1] = 0.7; z_pT_Bin_Borders[9][57][2] = 0.22; z_pT_Bin_Borders[9][57][3] = 0.3;
    Phi_h_Bin_Values[9][57][0] =  1; Phi_h_Bin_Values[9][57][1] = 746; Phi_h_Bin_Values[9][57][2] = 6047;
    z_pT_Bin_Borders[9][58][0] = 10; z_pT_Bin_Borders[9][58][1] = 0.7; z_pT_Bin_Borders[9][58][2] = 0.3; z_pT_Bin_Borders[9][58][3] = 0.38;
    Phi_h_Bin_Values[9][58][0] =  1; Phi_h_Bin_Values[9][58][1] = 747; Phi_h_Bin_Values[9][58][2] = 6048;
    z_pT_Bin_Borders[9][59][0] = 10; z_pT_Bin_Borders[9][59][1] = 0.7; z_pT_Bin_Borders[9][59][2] = 0.38; z_pT_Bin_Borders[9][59][3] = 0.46;
    Phi_h_Bin_Values[9][59][0] =  1; Phi_h_Bin_Values[9][59][1] = 748; Phi_h_Bin_Values[9][59][2] = 6049;
    z_pT_Bin_Borders[9][60][0] = 10; z_pT_Bin_Borders[9][60][1] = 0.7; z_pT_Bin_Borders[9][60][2] = 0.46; z_pT_Bin_Borders[9][60][3] = 0.58;
    Phi_h_Bin_Values[9][60][0] =  1; Phi_h_Bin_Values[9][60][1] = 749; Phi_h_Bin_Values[9][60][2] = 6050;
    z_pT_Bin_Borders[9][61][0] = 10; z_pT_Bin_Borders[9][61][1] = 0.7; z_pT_Bin_Borders[9][61][2] = 0.58; z_pT_Bin_Borders[9][61][3] = 0.74;
    Phi_h_Bin_Values[9][61][0] =  1; Phi_h_Bin_Values[9][61][1] = 750; Phi_h_Bin_Values[9][61][2] = 6051;
    z_pT_Bin_Borders[9][62][0] = 10; z_pT_Bin_Borders[9][62][1] = 0.7; z_pT_Bin_Borders[9][62][2] = 0.74; z_pT_Bin_Borders[9][62][3] = 0.95;
    Phi_h_Bin_Values[9][62][0] =  1; Phi_h_Bin_Values[9][62][1] = 751; Phi_h_Bin_Values[9][62][2] = 6052;
    z_pT_Bin_Borders[9][63][0] = 10; z_pT_Bin_Borders[9][63][1] = 0.7; z_pT_Bin_Borders[9][63][2] = 10; z_pT_Bin_Borders[9][63][3] = 0.95;
    Phi_h_Bin_Values[9][63][0] =  1; Phi_h_Bin_Values[9][63][1] = 752; Phi_h_Bin_Values[9][63][2] = 6053;
    z_pT_Bin_Borders[10][1][0] = 0.23; z_pT_Bin_Borders[10][1][1] = 0.19; z_pT_Bin_Borders[10][1][2] = 0.21; z_pT_Bin_Borders[10][1][3] = 0.05;
    Phi_h_Bin_Values[10][1][0] =  24; Phi_h_Bin_Values[10][1][1] = 0; Phi_h_Bin_Values[10][1][2] = 6054;
    z_pT_Bin_Borders[10][2][0] = 0.23; z_pT_Bin_Borders[10][2][1] = 0.19; z_pT_Bin_Borders[10][2][2] = 0.31; z_pT_Bin_Borders[10][2][3] = 0.21;
    Phi_h_Bin_Values[10][2][0] =  24; Phi_h_Bin_Values[10][2][1] = 24; Phi_h_Bin_Values[10][2][2] = 6078;
    z_pT_Bin_Borders[10][3][0] = 0.23; z_pT_Bin_Borders[10][3][1] = 0.19; z_pT_Bin_Borders[10][3][2] = 0.4; z_pT_Bin_Borders[10][3][3] = 0.31;
    Phi_h_Bin_Values[10][3][0] =  24; Phi_h_Bin_Values[10][3][1] = 48; Phi_h_Bin_Values[10][3][2] = 6102;
    z_pT_Bin_Borders[10][4][0] = 0.23; z_pT_Bin_Borders[10][4][1] = 0.19; z_pT_Bin_Borders[10][4][2] = 0.5; z_pT_Bin_Borders[10][4][3] = 0.4;
    Phi_h_Bin_Values[10][4][0] =  24; Phi_h_Bin_Values[10][4][1] = 72; Phi_h_Bin_Values[10][4][2] = 6126;
    z_pT_Bin_Borders[10][5][0] = 0.23; z_pT_Bin_Borders[10][5][1] = 0.19; z_pT_Bin_Borders[10][5][2] = 0.64; z_pT_Bin_Borders[10][5][3] = 0.5;
    Phi_h_Bin_Values[10][5][0] =  1; Phi_h_Bin_Values[10][5][1] = 96; Phi_h_Bin_Values[10][5][2] = 6150;
    z_pT_Bin_Borders[10][6][0] = 0.23; z_pT_Bin_Borders[10][6][1] = 0.19; z_pT_Bin_Borders[10][6][2] = 0.9; z_pT_Bin_Borders[10][6][3] = 0.64;
    Phi_h_Bin_Values[10][6][0] =  1; Phi_h_Bin_Values[10][6][1] = 97; Phi_h_Bin_Values[10][6][2] = 6151;
    z_pT_Bin_Borders[10][7][0] = 0.26; z_pT_Bin_Borders[10][7][1] = 0.23; z_pT_Bin_Borders[10][7][2] = 0.21; z_pT_Bin_Borders[10][7][3] = 0.05;
    Phi_h_Bin_Values[10][7][0] =  24; Phi_h_Bin_Values[10][7][1] = 98; Phi_h_Bin_Values[10][7][2] = 6152;
    z_pT_Bin_Borders[10][8][0] = 0.26; z_pT_Bin_Borders[10][8][1] = 0.23; z_pT_Bin_Borders[10][8][2] = 0.31; z_pT_Bin_Borders[10][8][3] = 0.21;
    Phi_h_Bin_Values[10][8][0] =  24; Phi_h_Bin_Values[10][8][1] = 122; Phi_h_Bin_Values[10][8][2] = 6176;
    z_pT_Bin_Borders[10][9][0] = 0.26; z_pT_Bin_Borders[10][9][1] = 0.23; z_pT_Bin_Borders[10][9][2] = 0.4; z_pT_Bin_Borders[10][9][3] = 0.31;
    Phi_h_Bin_Values[10][9][0] =  24; Phi_h_Bin_Values[10][9][1] = 146; Phi_h_Bin_Values[10][9][2] = 6200;
    z_pT_Bin_Borders[10][10][0] = 0.26; z_pT_Bin_Borders[10][10][1] = 0.23; z_pT_Bin_Borders[10][10][2] = 0.5; z_pT_Bin_Borders[10][10][3] = 0.4;
    Phi_h_Bin_Values[10][10][0] =  24; Phi_h_Bin_Values[10][10][1] = 170; Phi_h_Bin_Values[10][10][2] = 6224;
    z_pT_Bin_Borders[10][11][0] = 0.26; z_pT_Bin_Borders[10][11][1] = 0.23; z_pT_Bin_Borders[10][11][2] = 0.64; z_pT_Bin_Borders[10][11][3] = 0.5;
    Phi_h_Bin_Values[10][11][0] =  24; Phi_h_Bin_Values[10][11][1] = 194; Phi_h_Bin_Values[10][11][2] = 6248;
    z_pT_Bin_Borders[10][12][0] = 0.26; z_pT_Bin_Borders[10][12][1] = 0.23; z_pT_Bin_Borders[10][12][2] = 0.9; z_pT_Bin_Borders[10][12][3] = 0.64;
    Phi_h_Bin_Values[10][12][0] =  1; Phi_h_Bin_Values[10][12][1] = 218; Phi_h_Bin_Values[10][12][2] = 6272;
    z_pT_Bin_Borders[10][13][0] = 0.32; z_pT_Bin_Borders[10][13][1] = 0.26; z_pT_Bin_Borders[10][13][2] = 0.21; z_pT_Bin_Borders[10][13][3] = 0.05;
    Phi_h_Bin_Values[10][13][0] =  24; Phi_h_Bin_Values[10][13][1] = 219; Phi_h_Bin_Values[10][13][2] = 6273;
    z_pT_Bin_Borders[10][14][0] = 0.32; z_pT_Bin_Borders[10][14][1] = 0.26; z_pT_Bin_Borders[10][14][2] = 0.31; z_pT_Bin_Borders[10][14][3] = 0.21;
    Phi_h_Bin_Values[10][14][0] =  24; Phi_h_Bin_Values[10][14][1] = 243; Phi_h_Bin_Values[10][14][2] = 6297;
    z_pT_Bin_Borders[10][15][0] = 0.32; z_pT_Bin_Borders[10][15][1] = 0.26; z_pT_Bin_Borders[10][15][2] = 0.4; z_pT_Bin_Borders[10][15][3] = 0.31;
    Phi_h_Bin_Values[10][15][0] =  24; Phi_h_Bin_Values[10][15][1] = 267; Phi_h_Bin_Values[10][15][2] = 6321;
    z_pT_Bin_Borders[10][16][0] = 0.32; z_pT_Bin_Borders[10][16][1] = 0.26; z_pT_Bin_Borders[10][16][2] = 0.5; z_pT_Bin_Borders[10][16][3] = 0.4;
    Phi_h_Bin_Values[10][16][0] =  24; Phi_h_Bin_Values[10][16][1] = 291; Phi_h_Bin_Values[10][16][2] = 6345;
    z_pT_Bin_Borders[10][17][0] = 0.32; z_pT_Bin_Borders[10][17][1] = 0.26; z_pT_Bin_Borders[10][17][2] = 0.64; z_pT_Bin_Borders[10][17][3] = 0.5;
    Phi_h_Bin_Values[10][17][0] =  24; Phi_h_Bin_Values[10][17][1] = 315; Phi_h_Bin_Values[10][17][2] = 6369;
    z_pT_Bin_Borders[10][18][0] = 0.32; z_pT_Bin_Borders[10][18][1] = 0.26; z_pT_Bin_Borders[10][18][2] = 0.9; z_pT_Bin_Borders[10][18][3] = 0.64;
    Phi_h_Bin_Values[10][18][0] =  1; Phi_h_Bin_Values[10][18][1] = 339; Phi_h_Bin_Values[10][18][2] = 6393;
    z_pT_Bin_Borders[10][19][0] = 0.4; z_pT_Bin_Borders[10][19][1] = 0.32; z_pT_Bin_Borders[10][19][2] = 0.21; z_pT_Bin_Borders[10][19][3] = 0.05;
    Phi_h_Bin_Values[10][19][0] =  24; Phi_h_Bin_Values[10][19][1] = 340; Phi_h_Bin_Values[10][19][2] = 6394;
    z_pT_Bin_Borders[10][20][0] = 0.4; z_pT_Bin_Borders[10][20][1] = 0.32; z_pT_Bin_Borders[10][20][2] = 0.31; z_pT_Bin_Borders[10][20][3] = 0.21;
    Phi_h_Bin_Values[10][20][0] =  24; Phi_h_Bin_Values[10][20][1] = 364; Phi_h_Bin_Values[10][20][2] = 6418;
    z_pT_Bin_Borders[10][21][0] = 0.4; z_pT_Bin_Borders[10][21][1] = 0.32; z_pT_Bin_Borders[10][21][2] = 0.4; z_pT_Bin_Borders[10][21][3] = 0.31;
    Phi_h_Bin_Values[10][21][0] =  24; Phi_h_Bin_Values[10][21][1] = 388; Phi_h_Bin_Values[10][21][2] = 6442;
    z_pT_Bin_Borders[10][22][0] = 0.4; z_pT_Bin_Borders[10][22][1] = 0.32; z_pT_Bin_Borders[10][22][2] = 0.5; z_pT_Bin_Borders[10][22][3] = 0.4;
    Phi_h_Bin_Values[10][22][0] =  24; Phi_h_Bin_Values[10][22][1] = 412; Phi_h_Bin_Values[10][22][2] = 6466;
    z_pT_Bin_Borders[10][23][0] = 0.4; z_pT_Bin_Borders[10][23][1] = 0.32; z_pT_Bin_Borders[10][23][2] = 0.64; z_pT_Bin_Borders[10][23][3] = 0.5;
    Phi_h_Bin_Values[10][23][0] =  24; Phi_h_Bin_Values[10][23][1] = 436; Phi_h_Bin_Values[10][23][2] = 6490;
    z_pT_Bin_Borders[10][24][0] = 0.4; z_pT_Bin_Borders[10][24][1] = 0.32; z_pT_Bin_Borders[10][24][2] = 0.9; z_pT_Bin_Borders[10][24][3] = 0.64;
    Phi_h_Bin_Values[10][24][0] =  24; Phi_h_Bin_Values[10][24][1] = 460; Phi_h_Bin_Values[10][24][2] = 6514;
    z_pT_Bin_Borders[10][25][0] = 0.5; z_pT_Bin_Borders[10][25][1] = 0.4; z_pT_Bin_Borders[10][25][2] = 0.21; z_pT_Bin_Borders[10][25][3] = 0.05;
    Phi_h_Bin_Values[10][25][0] =  24; Phi_h_Bin_Values[10][25][1] = 484; Phi_h_Bin_Values[10][25][2] = 6538;
    z_pT_Bin_Borders[10][26][0] = 0.5; z_pT_Bin_Borders[10][26][1] = 0.4; z_pT_Bin_Borders[10][26][2] = 0.31; z_pT_Bin_Borders[10][26][3] = 0.21;
    Phi_h_Bin_Values[10][26][0] =  24; Phi_h_Bin_Values[10][26][1] = 508; Phi_h_Bin_Values[10][26][2] = 6562;
    z_pT_Bin_Borders[10][27][0] = 0.5; z_pT_Bin_Borders[10][27][1] = 0.4; z_pT_Bin_Borders[10][27][2] = 0.4; z_pT_Bin_Borders[10][27][3] = 0.31;
    Phi_h_Bin_Values[10][27][0] =  24; Phi_h_Bin_Values[10][27][1] = 532; Phi_h_Bin_Values[10][27][2] = 6586;
    z_pT_Bin_Borders[10][28][0] = 0.5; z_pT_Bin_Borders[10][28][1] = 0.4; z_pT_Bin_Borders[10][28][2] = 0.5; z_pT_Bin_Borders[10][28][3] = 0.4;
    Phi_h_Bin_Values[10][28][0] =  24; Phi_h_Bin_Values[10][28][1] = 556; Phi_h_Bin_Values[10][28][2] = 6610;
    z_pT_Bin_Borders[10][29][0] = 0.5; z_pT_Bin_Borders[10][29][1] = 0.4; z_pT_Bin_Borders[10][29][2] = 0.64; z_pT_Bin_Borders[10][29][3] = 0.5;
    Phi_h_Bin_Values[10][29][0] =  24; Phi_h_Bin_Values[10][29][1] = 580; Phi_h_Bin_Values[10][29][2] = 6634;
    z_pT_Bin_Borders[10][30][0] = 0.5; z_pT_Bin_Borders[10][30][1] = 0.4; z_pT_Bin_Borders[10][30][2] = 0.9; z_pT_Bin_Borders[10][30][3] = 0.64;
    Phi_h_Bin_Values[10][30][0] =  24; Phi_h_Bin_Values[10][30][1] = 604; Phi_h_Bin_Values[10][30][2] = 6658;
    z_pT_Bin_Borders[10][31][0] = 0.72; z_pT_Bin_Borders[10][31][1] = 0.5; z_pT_Bin_Borders[10][31][2] = 0.21; z_pT_Bin_Borders[10][31][3] = 0.05;
    Phi_h_Bin_Values[10][31][0] =  24; Phi_h_Bin_Values[10][31][1] = 628; Phi_h_Bin_Values[10][31][2] = 6682;
    z_pT_Bin_Borders[10][32][0] = 0.72; z_pT_Bin_Borders[10][32][1] = 0.5; z_pT_Bin_Borders[10][32][2] = 0.31; z_pT_Bin_Borders[10][32][3] = 0.21;
    Phi_h_Bin_Values[10][32][0] =  24; Phi_h_Bin_Values[10][32][1] = 652; Phi_h_Bin_Values[10][32][2] = 6706;
    z_pT_Bin_Borders[10][33][0] = 0.72; z_pT_Bin_Borders[10][33][1] = 0.5; z_pT_Bin_Borders[10][33][2] = 0.4; z_pT_Bin_Borders[10][33][3] = 0.31;
    Phi_h_Bin_Values[10][33][0] =  24; Phi_h_Bin_Values[10][33][1] = 676; Phi_h_Bin_Values[10][33][2] = 6730;
    z_pT_Bin_Borders[10][34][0] = 0.72; z_pT_Bin_Borders[10][34][1] = 0.5; z_pT_Bin_Borders[10][34][2] = 0.5; z_pT_Bin_Borders[10][34][3] = 0.4;
    Phi_h_Bin_Values[10][34][0] =  24; Phi_h_Bin_Values[10][34][1] = 700; Phi_h_Bin_Values[10][34][2] = 6754;
    z_pT_Bin_Borders[10][35][0] = 0.72; z_pT_Bin_Borders[10][35][1] = 0.5; z_pT_Bin_Borders[10][35][2] = 0.64; z_pT_Bin_Borders[10][35][3] = 0.5;
    Phi_h_Bin_Values[10][35][0] =  24; Phi_h_Bin_Values[10][35][1] = 724; Phi_h_Bin_Values[10][35][2] = 6778;
    z_pT_Bin_Borders[10][36][0] = 0.72; z_pT_Bin_Borders[10][36][1] = 0.5; z_pT_Bin_Borders[10][36][2] = 0.9; z_pT_Bin_Borders[10][36][3] = 0.64;
    Phi_h_Bin_Values[10][36][0] =  1; Phi_h_Bin_Values[10][36][1] = 748; Phi_h_Bin_Values[10][36][2] = 6802;
    z_pT_Bin_Borders[10][37][0] = 0.19; z_pT_Bin_Borders[10][37][1] = 0; z_pT_Bin_Borders[10][37][2] = 0.05; z_pT_Bin_Borders[10][37][3] = 0;
    Phi_h_Bin_Values[10][37][0] =  1; Phi_h_Bin_Values[10][37][1] = 749; Phi_h_Bin_Values[10][37][2] = 6803;
    z_pT_Bin_Borders[10][38][0] = 0.19; z_pT_Bin_Borders[10][38][1] = 0; z_pT_Bin_Borders[10][38][2] = 0.05; z_pT_Bin_Borders[10][38][3] = 0.21;
    Phi_h_Bin_Values[10][38][0] =  1; Phi_h_Bin_Values[10][38][1] = 750; Phi_h_Bin_Values[10][38][2] = 6804;
    z_pT_Bin_Borders[10][39][0] = 0.19; z_pT_Bin_Borders[10][39][1] = 0; z_pT_Bin_Borders[10][39][2] = 0.21; z_pT_Bin_Borders[10][39][3] = 0.31;
    Phi_h_Bin_Values[10][39][0] =  1; Phi_h_Bin_Values[10][39][1] = 751; Phi_h_Bin_Values[10][39][2] = 6805;
    z_pT_Bin_Borders[10][40][0] = 0.19; z_pT_Bin_Borders[10][40][1] = 0; z_pT_Bin_Borders[10][40][2] = 0.31; z_pT_Bin_Borders[10][40][3] = 0.4;
    Phi_h_Bin_Values[10][40][0] =  1; Phi_h_Bin_Values[10][40][1] = 752; Phi_h_Bin_Values[10][40][2] = 6806;
    z_pT_Bin_Borders[10][41][0] = 0.19; z_pT_Bin_Borders[10][41][1] = 0; z_pT_Bin_Borders[10][41][2] = 0.4; z_pT_Bin_Borders[10][41][3] = 0.5;
    Phi_h_Bin_Values[10][41][0] =  1; Phi_h_Bin_Values[10][41][1] = 753; Phi_h_Bin_Values[10][41][2] = 6807;
    z_pT_Bin_Borders[10][42][0] = 0.19; z_pT_Bin_Borders[10][42][1] = 0; z_pT_Bin_Borders[10][42][2] = 0.5; z_pT_Bin_Borders[10][42][3] = 0.64;
    Phi_h_Bin_Values[10][42][0] =  1; Phi_h_Bin_Values[10][42][1] = 754; Phi_h_Bin_Values[10][42][2] = 6808;
    z_pT_Bin_Borders[10][43][0] = 0.19; z_pT_Bin_Borders[10][43][1] = 0; z_pT_Bin_Borders[10][43][2] = 0.64; z_pT_Bin_Borders[10][43][3] = 0.9;
    Phi_h_Bin_Values[10][43][0] =  1; Phi_h_Bin_Values[10][43][1] = 755; Phi_h_Bin_Values[10][43][2] = 6809;
    z_pT_Bin_Borders[10][44][0] = 0.19; z_pT_Bin_Borders[10][44][1] = 0; z_pT_Bin_Borders[10][44][2] = 10; z_pT_Bin_Borders[10][44][3] = 0.9;
    Phi_h_Bin_Values[10][44][0] =  1; Phi_h_Bin_Values[10][44][1] = 756; Phi_h_Bin_Values[10][44][2] = 6810;
    z_pT_Bin_Borders[10][45][0] = 0.19; z_pT_Bin_Borders[10][45][1] = 0.23; z_pT_Bin_Borders[10][45][2] = 0.05; z_pT_Bin_Borders[10][45][3] = 0;
    Phi_h_Bin_Values[10][45][0] =  1; Phi_h_Bin_Values[10][45][1] = 757; Phi_h_Bin_Values[10][45][2] = 6811;
    z_pT_Bin_Borders[10][46][0] = 0.19; z_pT_Bin_Borders[10][46][1] = 0.23; z_pT_Bin_Borders[10][46][2] = 10; z_pT_Bin_Borders[10][46][3] = 0.9;
    Phi_h_Bin_Values[10][46][0] =  1; Phi_h_Bin_Values[10][46][1] = 758; Phi_h_Bin_Values[10][46][2] = 6812;
    z_pT_Bin_Borders[10][47][0] = 0.23; z_pT_Bin_Borders[10][47][1] = 0.26; z_pT_Bin_Borders[10][47][2] = 0.05; z_pT_Bin_Borders[10][47][3] = 0;
    Phi_h_Bin_Values[10][47][0] =  1; Phi_h_Bin_Values[10][47][1] = 759; Phi_h_Bin_Values[10][47][2] = 6813;
    z_pT_Bin_Borders[10][48][0] = 0.23; z_pT_Bin_Borders[10][48][1] = 0.26; z_pT_Bin_Borders[10][48][2] = 10; z_pT_Bin_Borders[10][48][3] = 0.9;
    Phi_h_Bin_Values[10][48][0] =  1; Phi_h_Bin_Values[10][48][1] = 760; Phi_h_Bin_Values[10][48][2] = 6814;
    z_pT_Bin_Borders[10][49][0] = 0.26; z_pT_Bin_Borders[10][49][1] = 0.32; z_pT_Bin_Borders[10][49][2] = 0.05; z_pT_Bin_Borders[10][49][3] = 0;
    Phi_h_Bin_Values[10][49][0] =  1; Phi_h_Bin_Values[10][49][1] = 761; Phi_h_Bin_Values[10][49][2] = 6815;
    z_pT_Bin_Borders[10][50][0] = 0.26; z_pT_Bin_Borders[10][50][1] = 0.32; z_pT_Bin_Borders[10][50][2] = 10; z_pT_Bin_Borders[10][50][3] = 0.9;
    Phi_h_Bin_Values[10][50][0] =  1; Phi_h_Bin_Values[10][50][1] = 762; Phi_h_Bin_Values[10][50][2] = 6816;
    z_pT_Bin_Borders[10][51][0] = 0.32; z_pT_Bin_Borders[10][51][1] = 0.4; z_pT_Bin_Borders[10][51][2] = 0.05; z_pT_Bin_Borders[10][51][3] = 0;
    Phi_h_Bin_Values[10][51][0] =  1; Phi_h_Bin_Values[10][51][1] = 763; Phi_h_Bin_Values[10][51][2] = 6817;
    z_pT_Bin_Borders[10][52][0] = 0.32; z_pT_Bin_Borders[10][52][1] = 0.4; z_pT_Bin_Borders[10][52][2] = 10; z_pT_Bin_Borders[10][52][3] = 0.9;
    Phi_h_Bin_Values[10][52][0] =  1; Phi_h_Bin_Values[10][52][1] = 764; Phi_h_Bin_Values[10][52][2] = 6818;
    z_pT_Bin_Borders[10][53][0] = 0.4; z_pT_Bin_Borders[10][53][1] = 0.5; z_pT_Bin_Borders[10][53][2] = 0.05; z_pT_Bin_Borders[10][53][3] = 0;
    Phi_h_Bin_Values[10][53][0] =  1; Phi_h_Bin_Values[10][53][1] = 765; Phi_h_Bin_Values[10][53][2] = 6819;
    z_pT_Bin_Borders[10][54][0] = 0.4; z_pT_Bin_Borders[10][54][1] = 0.5; z_pT_Bin_Borders[10][54][2] = 10; z_pT_Bin_Borders[10][54][3] = 0.9;
    Phi_h_Bin_Values[10][54][0] =  1; Phi_h_Bin_Values[10][54][1] = 766; Phi_h_Bin_Values[10][54][2] = 6820;
    z_pT_Bin_Borders[10][55][0] = 0.5; z_pT_Bin_Borders[10][55][1] = 0.72; z_pT_Bin_Borders[10][55][2] = 0.05; z_pT_Bin_Borders[10][55][3] = 0;
    Phi_h_Bin_Values[10][55][0] =  1; Phi_h_Bin_Values[10][55][1] = 767; Phi_h_Bin_Values[10][55][2] = 6821;
    z_pT_Bin_Borders[10][56][0] = 0.5; z_pT_Bin_Borders[10][56][1] = 0.72; z_pT_Bin_Borders[10][56][2] = 10; z_pT_Bin_Borders[10][56][3] = 0.9;
    Phi_h_Bin_Values[10][56][0] =  1; Phi_h_Bin_Values[10][56][1] = 768; Phi_h_Bin_Values[10][56][2] = 6822;
    z_pT_Bin_Borders[10][57][0] = 10; z_pT_Bin_Borders[10][57][1] = 0.72; z_pT_Bin_Borders[10][57][2] = 0; z_pT_Bin_Borders[10][57][3] = 0.05;
    Phi_h_Bin_Values[10][57][0] =  1; Phi_h_Bin_Values[10][57][1] = 769; Phi_h_Bin_Values[10][57][2] = 6823;
    z_pT_Bin_Borders[10][58][0] = 10; z_pT_Bin_Borders[10][58][1] = 0.72; z_pT_Bin_Borders[10][58][2] = 0.05; z_pT_Bin_Borders[10][58][3] = 0.21;
    Phi_h_Bin_Values[10][58][0] =  1; Phi_h_Bin_Values[10][58][1] = 770; Phi_h_Bin_Values[10][58][2] = 6824;
    z_pT_Bin_Borders[10][59][0] = 10; z_pT_Bin_Borders[10][59][1] = 0.72; z_pT_Bin_Borders[10][59][2] = 0.21; z_pT_Bin_Borders[10][59][3] = 0.31;
    Phi_h_Bin_Values[10][59][0] =  1; Phi_h_Bin_Values[10][59][1] = 771; Phi_h_Bin_Values[10][59][2] = 6825;
    z_pT_Bin_Borders[10][60][0] = 10; z_pT_Bin_Borders[10][60][1] = 0.72; z_pT_Bin_Borders[10][60][2] = 0.31; z_pT_Bin_Borders[10][60][3] = 0.4;
    Phi_h_Bin_Values[10][60][0] =  1; Phi_h_Bin_Values[10][60][1] = 772; Phi_h_Bin_Values[10][60][2] = 6826;
    z_pT_Bin_Borders[10][61][0] = 10; z_pT_Bin_Borders[10][61][1] = 0.72; z_pT_Bin_Borders[10][61][2] = 0.4; z_pT_Bin_Borders[10][61][3] = 0.5;
    Phi_h_Bin_Values[10][61][0] =  1; Phi_h_Bin_Values[10][61][1] = 773; Phi_h_Bin_Values[10][61][2] = 6827;
    z_pT_Bin_Borders[10][62][0] = 10; z_pT_Bin_Borders[10][62][1] = 0.72; z_pT_Bin_Borders[10][62][2] = 0.5; z_pT_Bin_Borders[10][62][3] = 0.64;
    Phi_h_Bin_Values[10][62][0] =  1; Phi_h_Bin_Values[10][62][1] = 774; Phi_h_Bin_Values[10][62][2] = 6828;
    z_pT_Bin_Borders[10][63][0] = 10; z_pT_Bin_Borders[10][63][1] = 0.72; z_pT_Bin_Borders[10][63][2] = 0.64; z_pT_Bin_Borders[10][63][3] = 0.9;
    Phi_h_Bin_Values[10][63][0] =  1; Phi_h_Bin_Values[10][63][1] = 775; Phi_h_Bin_Values[10][63][2] = 6829;
    z_pT_Bin_Borders[10][64][0] = 10; z_pT_Bin_Borders[10][64][1] = 0.72; z_pT_Bin_Borders[10][64][2] = 10; z_pT_Bin_Borders[10][64][3] = 0.9;
    Phi_h_Bin_Values[10][64][0] =  1; Phi_h_Bin_Values[10][64][1] = 776; Phi_h_Bin_Values[10][64][2] = 6830;
    z_pT_Bin_Borders[11][1][0] = 0.27; z_pT_Bin_Borders[11][1][1] = 0.22; z_pT_Bin_Borders[11][1][2] = 0.2; z_pT_Bin_Borders[11][1][3] = 0.05;
    Phi_h_Bin_Values[11][1][0] =  24; Phi_h_Bin_Values[11][1][1] = 0; Phi_h_Bin_Values[11][1][2] = 6831;
    z_pT_Bin_Borders[11][2][0] = 0.27; z_pT_Bin_Borders[11][2][1] = 0.22; z_pT_Bin_Borders[11][2][2] = 0.3; z_pT_Bin_Borders[11][2][3] = 0.2;
    Phi_h_Bin_Values[11][2][0] =  24; Phi_h_Bin_Values[11][2][1] = 24; Phi_h_Bin_Values[11][2][2] = 6855;
    z_pT_Bin_Borders[11][3][0] = 0.27; z_pT_Bin_Borders[11][3][1] = 0.22; z_pT_Bin_Borders[11][3][2] = 0.4; z_pT_Bin_Borders[11][3][3] = 0.3;
    Phi_h_Bin_Values[11][3][0] =  24; Phi_h_Bin_Values[11][3][1] = 48; Phi_h_Bin_Values[11][3][2] = 6879;
    z_pT_Bin_Borders[11][4][0] = 0.27; z_pT_Bin_Borders[11][4][1] = 0.22; z_pT_Bin_Borders[11][4][2] = 0.54; z_pT_Bin_Borders[11][4][3] = 0.4;
    Phi_h_Bin_Values[11][4][0] =  24; Phi_h_Bin_Values[11][4][1] = 72; Phi_h_Bin_Values[11][4][2] = 6903;
    z_pT_Bin_Borders[11][5][0] = 0.27; z_pT_Bin_Borders[11][5][1] = 0.22; z_pT_Bin_Borders[11][5][2] = 0.69; z_pT_Bin_Borders[11][5][3] = 0.54;
    Phi_h_Bin_Values[11][5][0] =  1; Phi_h_Bin_Values[11][5][1] = 96; Phi_h_Bin_Values[11][5][2] = 6927;
    z_pT_Bin_Borders[11][6][0] = 0.32; z_pT_Bin_Borders[11][6][1] = 0.27; z_pT_Bin_Borders[11][6][2] = 0.2; z_pT_Bin_Borders[11][6][3] = 0.05;
    Phi_h_Bin_Values[11][6][0] =  24; Phi_h_Bin_Values[11][6][1] = 97; Phi_h_Bin_Values[11][6][2] = 6928;
    z_pT_Bin_Borders[11][7][0] = 0.32; z_pT_Bin_Borders[11][7][1] = 0.27; z_pT_Bin_Borders[11][7][2] = 0.3; z_pT_Bin_Borders[11][7][3] = 0.2;
    Phi_h_Bin_Values[11][7][0] =  24; Phi_h_Bin_Values[11][7][1] = 121; Phi_h_Bin_Values[11][7][2] = 6952;
    z_pT_Bin_Borders[11][8][0] = 0.32; z_pT_Bin_Borders[11][8][1] = 0.27; z_pT_Bin_Borders[11][8][2] = 0.4; z_pT_Bin_Borders[11][8][3] = 0.3;
    Phi_h_Bin_Values[11][8][0] =  24; Phi_h_Bin_Values[11][8][1] = 145; Phi_h_Bin_Values[11][8][2] = 6976;
    z_pT_Bin_Borders[11][9][0] = 0.32; z_pT_Bin_Borders[11][9][1] = 0.27; z_pT_Bin_Borders[11][9][2] = 0.54; z_pT_Bin_Borders[11][9][3] = 0.4;
    Phi_h_Bin_Values[11][9][0] =  24; Phi_h_Bin_Values[11][9][1] = 169; Phi_h_Bin_Values[11][9][2] = 7000;
    z_pT_Bin_Borders[11][10][0] = 0.32; z_pT_Bin_Borders[11][10][1] = 0.27; z_pT_Bin_Borders[11][10][2] = 0.69; z_pT_Bin_Borders[11][10][3] = 0.54;
    Phi_h_Bin_Values[11][10][0] =  24; Phi_h_Bin_Values[11][10][1] = 193; Phi_h_Bin_Values[11][10][2] = 7024;
    z_pT_Bin_Borders[11][11][0] = 0.4; z_pT_Bin_Borders[11][11][1] = 0.32; z_pT_Bin_Borders[11][11][2] = 0.2; z_pT_Bin_Borders[11][11][3] = 0.05;
    Phi_h_Bin_Values[11][11][0] =  24; Phi_h_Bin_Values[11][11][1] = 217; Phi_h_Bin_Values[11][11][2] = 7048;
    z_pT_Bin_Borders[11][12][0] = 0.4; z_pT_Bin_Borders[11][12][1] = 0.32; z_pT_Bin_Borders[11][12][2] = 0.3; z_pT_Bin_Borders[11][12][3] = 0.2;
    Phi_h_Bin_Values[11][12][0] =  24; Phi_h_Bin_Values[11][12][1] = 241; Phi_h_Bin_Values[11][12][2] = 7072;
    z_pT_Bin_Borders[11][13][0] = 0.4; z_pT_Bin_Borders[11][13][1] = 0.32; z_pT_Bin_Borders[11][13][2] = 0.4; z_pT_Bin_Borders[11][13][3] = 0.3;
    Phi_h_Bin_Values[11][13][0] =  24; Phi_h_Bin_Values[11][13][1] = 265; Phi_h_Bin_Values[11][13][2] = 7096;
    z_pT_Bin_Borders[11][14][0] = 0.4; z_pT_Bin_Borders[11][14][1] = 0.32; z_pT_Bin_Borders[11][14][2] = 0.54; z_pT_Bin_Borders[11][14][3] = 0.4;
    Phi_h_Bin_Values[11][14][0] =  24; Phi_h_Bin_Values[11][14][1] = 289; Phi_h_Bin_Values[11][14][2] = 7120;
    z_pT_Bin_Borders[11][15][0] = 0.4; z_pT_Bin_Borders[11][15][1] = 0.32; z_pT_Bin_Borders[11][15][2] = 0.69; z_pT_Bin_Borders[11][15][3] = 0.54;
    Phi_h_Bin_Values[11][15][0] =  24; Phi_h_Bin_Values[11][15][1] = 313; Phi_h_Bin_Values[11][15][2] = 7144;
    z_pT_Bin_Borders[11][16][0] = 0.53; z_pT_Bin_Borders[11][16][1] = 0.4; z_pT_Bin_Borders[11][16][2] = 0.2; z_pT_Bin_Borders[11][16][3] = 0.05;
    Phi_h_Bin_Values[11][16][0] =  24; Phi_h_Bin_Values[11][16][1] = 337; Phi_h_Bin_Values[11][16][2] = 7168;
    z_pT_Bin_Borders[11][17][0] = 0.53; z_pT_Bin_Borders[11][17][1] = 0.4; z_pT_Bin_Borders[11][17][2] = 0.3; z_pT_Bin_Borders[11][17][3] = 0.2;
    Phi_h_Bin_Values[11][17][0] =  24; Phi_h_Bin_Values[11][17][1] = 361; Phi_h_Bin_Values[11][17][2] = 7192;
    z_pT_Bin_Borders[11][18][0] = 0.53; z_pT_Bin_Borders[11][18][1] = 0.4; z_pT_Bin_Borders[11][18][2] = 0.4; z_pT_Bin_Borders[11][18][3] = 0.3;
    Phi_h_Bin_Values[11][18][0] =  24; Phi_h_Bin_Values[11][18][1] = 385; Phi_h_Bin_Values[11][18][2] = 7216;
    z_pT_Bin_Borders[11][19][0] = 0.53; z_pT_Bin_Borders[11][19][1] = 0.4; z_pT_Bin_Borders[11][19][2] = 0.54; z_pT_Bin_Borders[11][19][3] = 0.4;
    Phi_h_Bin_Values[11][19][0] =  24; Phi_h_Bin_Values[11][19][1] = 409; Phi_h_Bin_Values[11][19][2] = 7240;
    z_pT_Bin_Borders[11][20][0] = 0.53; z_pT_Bin_Borders[11][20][1] = 0.4; z_pT_Bin_Borders[11][20][2] = 0.69; z_pT_Bin_Borders[11][20][3] = 0.54;
    Phi_h_Bin_Values[11][20][0] =  24; Phi_h_Bin_Values[11][20][1] = 433; Phi_h_Bin_Values[11][20][2] = 7264;
    z_pT_Bin_Borders[11][21][0] = 0.69; z_pT_Bin_Borders[11][21][1] = 0.53; z_pT_Bin_Borders[11][21][2] = 0.2; z_pT_Bin_Borders[11][21][3] = 0.05;
    Phi_h_Bin_Values[11][21][0] =  24; Phi_h_Bin_Values[11][21][1] = 457; Phi_h_Bin_Values[11][21][2] = 7288;
    z_pT_Bin_Borders[11][22][0] = 0.69; z_pT_Bin_Borders[11][22][1] = 0.53; z_pT_Bin_Borders[11][22][2] = 0.3; z_pT_Bin_Borders[11][22][3] = 0.2;
    Phi_h_Bin_Values[11][22][0] =  24; Phi_h_Bin_Values[11][22][1] = 481; Phi_h_Bin_Values[11][22][2] = 7312;
    z_pT_Bin_Borders[11][23][0] = 0.69; z_pT_Bin_Borders[11][23][1] = 0.53; z_pT_Bin_Borders[11][23][2] = 0.4; z_pT_Bin_Borders[11][23][3] = 0.3;
    Phi_h_Bin_Values[11][23][0] =  1; Phi_h_Bin_Values[11][23][1] = 505; Phi_h_Bin_Values[11][23][2] = 7336;
    z_pT_Bin_Borders[11][24][0] = 0.69; z_pT_Bin_Borders[11][24][1] = 0.53; z_pT_Bin_Borders[11][24][2] = 0.54; z_pT_Bin_Borders[11][24][3] = 0.4;
    Phi_h_Bin_Values[11][24][0] =  1; Phi_h_Bin_Values[11][24][1] = 506; Phi_h_Bin_Values[11][24][2] = 7337;
    z_pT_Bin_Borders[11][25][0] = 0.69; z_pT_Bin_Borders[11][25][1] = 0.53; z_pT_Bin_Borders[11][25][2] = 0.69; z_pT_Bin_Borders[11][25][3] = 0.54;
    Phi_h_Bin_Values[11][25][0] =  1; Phi_h_Bin_Values[11][25][1] = 507; Phi_h_Bin_Values[11][25][2] = 7338;
    z_pT_Bin_Borders[11][26][0] = 0.22; z_pT_Bin_Borders[11][26][1] = 0; z_pT_Bin_Borders[11][26][2] = 0.05; z_pT_Bin_Borders[11][26][3] = 0;
    Phi_h_Bin_Values[11][26][0] =  1; Phi_h_Bin_Values[11][26][1] = 508; Phi_h_Bin_Values[11][26][2] = 7339;
    z_pT_Bin_Borders[11][27][0] = 0.22; z_pT_Bin_Borders[11][27][1] = 0; z_pT_Bin_Borders[11][27][2] = 0.05; z_pT_Bin_Borders[11][27][3] = 0.2;
    Phi_h_Bin_Values[11][27][0] =  1; Phi_h_Bin_Values[11][27][1] = 509; Phi_h_Bin_Values[11][27][2] = 7340;
    z_pT_Bin_Borders[11][28][0] = 0.22; z_pT_Bin_Borders[11][28][1] = 0; z_pT_Bin_Borders[11][28][2] = 0.2; z_pT_Bin_Borders[11][28][3] = 0.3;
    Phi_h_Bin_Values[11][28][0] =  1; Phi_h_Bin_Values[11][28][1] = 510; Phi_h_Bin_Values[11][28][2] = 7341;
    z_pT_Bin_Borders[11][29][0] = 0.22; z_pT_Bin_Borders[11][29][1] = 0; z_pT_Bin_Borders[11][29][2] = 0.3; z_pT_Bin_Borders[11][29][3] = 0.4;
    Phi_h_Bin_Values[11][29][0] =  1; Phi_h_Bin_Values[11][29][1] = 511; Phi_h_Bin_Values[11][29][2] = 7342;
    z_pT_Bin_Borders[11][30][0] = 0.22; z_pT_Bin_Borders[11][30][1] = 0; z_pT_Bin_Borders[11][30][2] = 0.4; z_pT_Bin_Borders[11][30][3] = 0.54;
    Phi_h_Bin_Values[11][30][0] =  1; Phi_h_Bin_Values[11][30][1] = 512; Phi_h_Bin_Values[11][30][2] = 7343;
    z_pT_Bin_Borders[11][31][0] = 0.22; z_pT_Bin_Borders[11][31][1] = 0; z_pT_Bin_Borders[11][31][2] = 0.54; z_pT_Bin_Borders[11][31][3] = 0.69;
    Phi_h_Bin_Values[11][31][0] =  1; Phi_h_Bin_Values[11][31][1] = 513; Phi_h_Bin_Values[11][31][2] = 7344;
    z_pT_Bin_Borders[11][32][0] = 0.22; z_pT_Bin_Borders[11][32][1] = 0; z_pT_Bin_Borders[11][32][2] = 10; z_pT_Bin_Borders[11][32][3] = 0.69;
    Phi_h_Bin_Values[11][32][0] =  1; Phi_h_Bin_Values[11][32][1] = 514; Phi_h_Bin_Values[11][32][2] = 7345;
    z_pT_Bin_Borders[11][33][0] = 0.22; z_pT_Bin_Borders[11][33][1] = 0.27; z_pT_Bin_Borders[11][33][2] = 0.05; z_pT_Bin_Borders[11][33][3] = 0;
    Phi_h_Bin_Values[11][33][0] =  1; Phi_h_Bin_Values[11][33][1] = 515; Phi_h_Bin_Values[11][33][2] = 7346;
    z_pT_Bin_Borders[11][34][0] = 0.22; z_pT_Bin_Borders[11][34][1] = 0.27; z_pT_Bin_Borders[11][34][2] = 10; z_pT_Bin_Borders[11][34][3] = 0.69;
    Phi_h_Bin_Values[11][34][0] =  1; Phi_h_Bin_Values[11][34][1] = 516; Phi_h_Bin_Values[11][34][2] = 7347;
    z_pT_Bin_Borders[11][35][0] = 0.27; z_pT_Bin_Borders[11][35][1] = 0.32; z_pT_Bin_Borders[11][35][2] = 0.05; z_pT_Bin_Borders[11][35][3] = 0;
    Phi_h_Bin_Values[11][35][0] =  1; Phi_h_Bin_Values[11][35][1] = 517; Phi_h_Bin_Values[11][35][2] = 7348;
    z_pT_Bin_Borders[11][36][0] = 0.27; z_pT_Bin_Borders[11][36][1] = 0.32; z_pT_Bin_Borders[11][36][2] = 10; z_pT_Bin_Borders[11][36][3] = 0.69;
    Phi_h_Bin_Values[11][36][0] =  1; Phi_h_Bin_Values[11][36][1] = 518; Phi_h_Bin_Values[11][36][2] = 7349;
    z_pT_Bin_Borders[11][37][0] = 0.32; z_pT_Bin_Borders[11][37][1] = 0.4; z_pT_Bin_Borders[11][37][2] = 0.05; z_pT_Bin_Borders[11][37][3] = 0;
    Phi_h_Bin_Values[11][37][0] =  1; Phi_h_Bin_Values[11][37][1] = 519; Phi_h_Bin_Values[11][37][2] = 7350;
    z_pT_Bin_Borders[11][38][0] = 0.32; z_pT_Bin_Borders[11][38][1] = 0.4; z_pT_Bin_Borders[11][38][2] = 10; z_pT_Bin_Borders[11][38][3] = 0.69;
    Phi_h_Bin_Values[11][38][0] =  1; Phi_h_Bin_Values[11][38][1] = 520; Phi_h_Bin_Values[11][38][2] = 7351;
    z_pT_Bin_Borders[11][39][0] = 0.4; z_pT_Bin_Borders[11][39][1] = 0.53; z_pT_Bin_Borders[11][39][2] = 0.05; z_pT_Bin_Borders[11][39][3] = 0;
    Phi_h_Bin_Values[11][39][0] =  1; Phi_h_Bin_Values[11][39][1] = 521; Phi_h_Bin_Values[11][39][2] = 7352;
    z_pT_Bin_Borders[11][40][0] = 0.4; z_pT_Bin_Borders[11][40][1] = 0.53; z_pT_Bin_Borders[11][40][2] = 10; z_pT_Bin_Borders[11][40][3] = 0.69;
    Phi_h_Bin_Values[11][40][0] =  1; Phi_h_Bin_Values[11][40][1] = 522; Phi_h_Bin_Values[11][40][2] = 7353;
    z_pT_Bin_Borders[11][41][0] = 0.53; z_pT_Bin_Borders[11][41][1] = 0.69; z_pT_Bin_Borders[11][41][2] = 0.05; z_pT_Bin_Borders[11][41][3] = 0;
    Phi_h_Bin_Values[11][41][0] =  1; Phi_h_Bin_Values[11][41][1] = 523; Phi_h_Bin_Values[11][41][2] = 7354;
    z_pT_Bin_Borders[11][42][0] = 0.53; z_pT_Bin_Borders[11][42][1] = 0.69; z_pT_Bin_Borders[11][42][2] = 10; z_pT_Bin_Borders[11][42][3] = 0.69;
    Phi_h_Bin_Values[11][42][0] =  1; Phi_h_Bin_Values[11][42][1] = 524; Phi_h_Bin_Values[11][42][2] = 7355;
    z_pT_Bin_Borders[11][43][0] = 10; z_pT_Bin_Borders[11][43][1] = 0.69; z_pT_Bin_Borders[11][43][2] = 0; z_pT_Bin_Borders[11][43][3] = 0.05;
    Phi_h_Bin_Values[11][43][0] =  1; Phi_h_Bin_Values[11][43][1] = 525; Phi_h_Bin_Values[11][43][2] = 7356;
    z_pT_Bin_Borders[11][44][0] = 10; z_pT_Bin_Borders[11][44][1] = 0.69; z_pT_Bin_Borders[11][44][2] = 0.05; z_pT_Bin_Borders[11][44][3] = 0.2;
    Phi_h_Bin_Values[11][44][0] =  1; Phi_h_Bin_Values[11][44][1] = 526; Phi_h_Bin_Values[11][44][2] = 7357;
    z_pT_Bin_Borders[11][45][0] = 10; z_pT_Bin_Borders[11][45][1] = 0.69; z_pT_Bin_Borders[11][45][2] = 0.2; z_pT_Bin_Borders[11][45][3] = 0.3;
    Phi_h_Bin_Values[11][45][0] =  1; Phi_h_Bin_Values[11][45][1] = 527; Phi_h_Bin_Values[11][45][2] = 7358;
    z_pT_Bin_Borders[11][46][0] = 10; z_pT_Bin_Borders[11][46][1] = 0.69; z_pT_Bin_Borders[11][46][2] = 0.3; z_pT_Bin_Borders[11][46][3] = 0.4;
    Phi_h_Bin_Values[11][46][0] =  1; Phi_h_Bin_Values[11][46][1] = 528; Phi_h_Bin_Values[11][46][2] = 7359;
    z_pT_Bin_Borders[11][47][0] = 10; z_pT_Bin_Borders[11][47][1] = 0.69; z_pT_Bin_Borders[11][47][2] = 0.4; z_pT_Bin_Borders[11][47][3] = 0.54;
    Phi_h_Bin_Values[11][47][0] =  1; Phi_h_Bin_Values[11][47][1] = 529; Phi_h_Bin_Values[11][47][2] = 7360;
    z_pT_Bin_Borders[11][48][0] = 10; z_pT_Bin_Borders[11][48][1] = 0.69; z_pT_Bin_Borders[11][48][2] = 0.54; z_pT_Bin_Borders[11][48][3] = 0.69;
    Phi_h_Bin_Values[11][48][0] =  1; Phi_h_Bin_Values[11][48][1] = 530; Phi_h_Bin_Values[11][48][2] = 7361;
    z_pT_Bin_Borders[11][49][0] = 10; z_pT_Bin_Borders[11][49][1] = 0.69; z_pT_Bin_Borders[11][49][2] = 10; z_pT_Bin_Borders[11][49][3] = 0.69;
    Phi_h_Bin_Values[11][49][0] =  1; Phi_h_Bin_Values[11][49][1] = 531; Phi_h_Bin_Values[11][49][2] = 7362;
    z_pT_Bin_Borders[12][1][0] = 0.31; z_pT_Bin_Borders[12][1][1] = 0.27; z_pT_Bin_Borders[12][1][2] = 0.22; z_pT_Bin_Borders[12][1][3] = 0.05;
    Phi_h_Bin_Values[12][1][0] =  24; Phi_h_Bin_Values[12][1][1] = 0; Phi_h_Bin_Values[12][1][2] = 7363;
    z_pT_Bin_Borders[12][2][0] = 0.31; z_pT_Bin_Borders[12][2][1] = 0.27; z_pT_Bin_Borders[12][2][2] = 0.32; z_pT_Bin_Borders[12][2][3] = 0.22;
    Phi_h_Bin_Values[12][2][0] =  24; Phi_h_Bin_Values[12][2][1] = 24; Phi_h_Bin_Values[12][2][2] = 7387;
    z_pT_Bin_Borders[12][3][0] = 0.31; z_pT_Bin_Borders[12][3][1] = 0.27; z_pT_Bin_Borders[12][3][2] = 0.41; z_pT_Bin_Borders[12][3][3] = 0.32;
    Phi_h_Bin_Values[12][3][0] =  24; Phi_h_Bin_Values[12][3][1] = 48; Phi_h_Bin_Values[12][3][2] = 7411;
    z_pT_Bin_Borders[12][4][0] = 0.35; z_pT_Bin_Borders[12][4][1] = 0.31; z_pT_Bin_Borders[12][4][2] = 0.22; z_pT_Bin_Borders[12][4][3] = 0.05;
    Phi_h_Bin_Values[12][4][0] =  24; Phi_h_Bin_Values[12][4][1] = 72; Phi_h_Bin_Values[12][4][2] = 7435;
    z_pT_Bin_Borders[12][5][0] = 0.35; z_pT_Bin_Borders[12][5][1] = 0.31; z_pT_Bin_Borders[12][5][2] = 0.32; z_pT_Bin_Borders[12][5][3] = 0.22;
    Phi_h_Bin_Values[12][5][0] =  24; Phi_h_Bin_Values[12][5][1] = 96; Phi_h_Bin_Values[12][5][2] = 7459;
    z_pT_Bin_Borders[12][6][0] = 0.35; z_pT_Bin_Borders[12][6][1] = 0.31; z_pT_Bin_Borders[12][6][2] = 0.41; z_pT_Bin_Borders[12][6][3] = 0.32;
    Phi_h_Bin_Values[12][6][0] =  24; Phi_h_Bin_Values[12][6][1] = 120; Phi_h_Bin_Values[12][6][2] = 7483;
    z_pT_Bin_Borders[12][7][0] = 0.4; z_pT_Bin_Borders[12][7][1] = 0.35; z_pT_Bin_Borders[12][7][2] = 0.22; z_pT_Bin_Borders[12][7][3] = 0.05;
    Phi_h_Bin_Values[12][7][0] =  24; Phi_h_Bin_Values[12][7][1] = 144; Phi_h_Bin_Values[12][7][2] = 7507;
    z_pT_Bin_Borders[12][8][0] = 0.4; z_pT_Bin_Borders[12][8][1] = 0.35; z_pT_Bin_Borders[12][8][2] = 0.32; z_pT_Bin_Borders[12][8][3] = 0.22;
    Phi_h_Bin_Values[12][8][0] =  24; Phi_h_Bin_Values[12][8][1] = 168; Phi_h_Bin_Values[12][8][2] = 7531;
    z_pT_Bin_Borders[12][9][0] = 0.4; z_pT_Bin_Borders[12][9][1] = 0.35; z_pT_Bin_Borders[12][9][2] = 0.41; z_pT_Bin_Borders[12][9][3] = 0.32;
    Phi_h_Bin_Values[12][9][0] =  24; Phi_h_Bin_Values[12][9][1] = 192; Phi_h_Bin_Values[12][9][2] = 7555;
    z_pT_Bin_Borders[12][10][0] = 0.5; z_pT_Bin_Borders[12][10][1] = 0.4; z_pT_Bin_Borders[12][10][2] = 0.22; z_pT_Bin_Borders[12][10][3] = 0.05;
    Phi_h_Bin_Values[12][10][0] =  24; Phi_h_Bin_Values[12][10][1] = 216; Phi_h_Bin_Values[12][10][2] = 7579;
    z_pT_Bin_Borders[12][11][0] = 0.5; z_pT_Bin_Borders[12][11][1] = 0.4; z_pT_Bin_Borders[12][11][2] = 0.32; z_pT_Bin_Borders[12][11][3] = 0.22;
    Phi_h_Bin_Values[12][11][0] =  1; Phi_h_Bin_Values[12][11][1] = 240; Phi_h_Bin_Values[12][11][2] = 7603;
    z_pT_Bin_Borders[12][12][0] = 0.5; z_pT_Bin_Borders[12][12][1] = 0.4; z_pT_Bin_Borders[12][12][2] = 0.41; z_pT_Bin_Borders[12][12][3] = 0.32;
    Phi_h_Bin_Values[12][12][0] =  1; Phi_h_Bin_Values[12][12][1] = 241; Phi_h_Bin_Values[12][12][2] = 7604;
    z_pT_Bin_Borders[12][13][0] = 0.27; z_pT_Bin_Borders[12][13][1] = 0; z_pT_Bin_Borders[12][13][2] = 0.05; z_pT_Bin_Borders[12][13][3] = 0;
    Phi_h_Bin_Values[12][13][0] =  1; Phi_h_Bin_Values[12][13][1] = 242; Phi_h_Bin_Values[12][13][2] = 7605;
    z_pT_Bin_Borders[12][14][0] = 0.27; z_pT_Bin_Borders[12][14][1] = 0; z_pT_Bin_Borders[12][14][2] = 0.05; z_pT_Bin_Borders[12][14][3] = 0.22;
    Phi_h_Bin_Values[12][14][0] =  1; Phi_h_Bin_Values[12][14][1] = 243; Phi_h_Bin_Values[12][14][2] = 7606;
    z_pT_Bin_Borders[12][15][0] = 0.27; z_pT_Bin_Borders[12][15][1] = 0; z_pT_Bin_Borders[12][15][2] = 0.22; z_pT_Bin_Borders[12][15][3] = 0.32;
    Phi_h_Bin_Values[12][15][0] =  1; Phi_h_Bin_Values[12][15][1] = 244; Phi_h_Bin_Values[12][15][2] = 7607;
    z_pT_Bin_Borders[12][16][0] = 0.27; z_pT_Bin_Borders[12][16][1] = 0; z_pT_Bin_Borders[12][16][2] = 0.32; z_pT_Bin_Borders[12][16][3] = 0.41;
    Phi_h_Bin_Values[12][16][0] =  1; Phi_h_Bin_Values[12][16][1] = 245; Phi_h_Bin_Values[12][16][2] = 7608;
    z_pT_Bin_Borders[12][17][0] = 0.27; z_pT_Bin_Borders[12][17][1] = 0; z_pT_Bin_Borders[12][17][2] = 10; z_pT_Bin_Borders[12][17][3] = 0.41;
    Phi_h_Bin_Values[12][17][0] =  1; Phi_h_Bin_Values[12][17][1] = 246; Phi_h_Bin_Values[12][17][2] = 7609;
    z_pT_Bin_Borders[12][18][0] = 0.27; z_pT_Bin_Borders[12][18][1] = 0.31; z_pT_Bin_Borders[12][18][2] = 0.05; z_pT_Bin_Borders[12][18][3] = 0;
    Phi_h_Bin_Values[12][18][0] =  1; Phi_h_Bin_Values[12][18][1] = 247; Phi_h_Bin_Values[12][18][2] = 7610;
    z_pT_Bin_Borders[12][19][0] = 0.27; z_pT_Bin_Borders[12][19][1] = 0.31; z_pT_Bin_Borders[12][19][2] = 10; z_pT_Bin_Borders[12][19][3] = 0.41;
    Phi_h_Bin_Values[12][19][0] =  1; Phi_h_Bin_Values[12][19][1] = 248; Phi_h_Bin_Values[12][19][2] = 7611;
    z_pT_Bin_Borders[12][20][0] = 0.31; z_pT_Bin_Borders[12][20][1] = 0.35; z_pT_Bin_Borders[12][20][2] = 0.05; z_pT_Bin_Borders[12][20][3] = 0;
    Phi_h_Bin_Values[12][20][0] =  1; Phi_h_Bin_Values[12][20][1] = 249; Phi_h_Bin_Values[12][20][2] = 7612;
    z_pT_Bin_Borders[12][21][0] = 0.31; z_pT_Bin_Borders[12][21][1] = 0.35; z_pT_Bin_Borders[12][21][2] = 10; z_pT_Bin_Borders[12][21][3] = 0.41;
    Phi_h_Bin_Values[12][21][0] =  1; Phi_h_Bin_Values[12][21][1] = 250; Phi_h_Bin_Values[12][21][2] = 7613;
    z_pT_Bin_Borders[12][22][0] = 0.35; z_pT_Bin_Borders[12][22][1] = 0.4; z_pT_Bin_Borders[12][22][2] = 0.05; z_pT_Bin_Borders[12][22][3] = 0;
    Phi_h_Bin_Values[12][22][0] =  1; Phi_h_Bin_Values[12][22][1] = 251; Phi_h_Bin_Values[12][22][2] = 7614;
    z_pT_Bin_Borders[12][23][0] = 0.35; z_pT_Bin_Borders[12][23][1] = 0.4; z_pT_Bin_Borders[12][23][2] = 10; z_pT_Bin_Borders[12][23][3] = 0.41;
    Phi_h_Bin_Values[12][23][0] =  1; Phi_h_Bin_Values[12][23][1] = 252; Phi_h_Bin_Values[12][23][2] = 7615;
    z_pT_Bin_Borders[12][24][0] = 0.4; z_pT_Bin_Borders[12][24][1] = 0.5; z_pT_Bin_Borders[12][24][2] = 0.05; z_pT_Bin_Borders[12][24][3] = 0;
    Phi_h_Bin_Values[12][24][0] =  1; Phi_h_Bin_Values[12][24][1] = 253; Phi_h_Bin_Values[12][24][2] = 7616;
    z_pT_Bin_Borders[12][25][0] = 0.4; z_pT_Bin_Borders[12][25][1] = 0.5; z_pT_Bin_Borders[12][25][2] = 10; z_pT_Bin_Borders[12][25][3] = 0.41;
    Phi_h_Bin_Values[12][25][0] =  1; Phi_h_Bin_Values[12][25][1] = 254; Phi_h_Bin_Values[12][25][2] = 7617;
    z_pT_Bin_Borders[12][26][0] = 10; z_pT_Bin_Borders[12][26][1] = 0.5; z_pT_Bin_Borders[12][26][2] = 0; z_pT_Bin_Borders[12][26][3] = 0.05;
    Phi_h_Bin_Values[12][26][0] =  1; Phi_h_Bin_Values[12][26][1] = 255; Phi_h_Bin_Values[12][26][2] = 7618;
    z_pT_Bin_Borders[12][27][0] = 10; z_pT_Bin_Borders[12][27][1] = 0.5; z_pT_Bin_Borders[12][27][2] = 0.05; z_pT_Bin_Borders[12][27][3] = 0.22;
    Phi_h_Bin_Values[12][27][0] =  1; Phi_h_Bin_Values[12][27][1] = 256; Phi_h_Bin_Values[12][27][2] = 7619;
    z_pT_Bin_Borders[12][28][0] = 10; z_pT_Bin_Borders[12][28][1] = 0.5; z_pT_Bin_Borders[12][28][2] = 0.22; z_pT_Bin_Borders[12][28][3] = 0.32;
    Phi_h_Bin_Values[12][28][0] =  1; Phi_h_Bin_Values[12][28][1] = 257; Phi_h_Bin_Values[12][28][2] = 7620;
    z_pT_Bin_Borders[12][29][0] = 10; z_pT_Bin_Borders[12][29][1] = 0.5; z_pT_Bin_Borders[12][29][2] = 0.32; z_pT_Bin_Borders[12][29][3] = 0.41;
    Phi_h_Bin_Values[12][29][0] =  1; Phi_h_Bin_Values[12][29][1] = 258; Phi_h_Bin_Values[12][29][2] = 7621;
    z_pT_Bin_Borders[12][30][0] = 10; z_pT_Bin_Borders[12][30][1] = 0.5; z_pT_Bin_Borders[12][30][2] = 10; z_pT_Bin_Borders[12][30][3] = 0.41;
    Phi_h_Bin_Values[12][30][0] =  1; Phi_h_Bin_Values[12][30][1] = 259; Phi_h_Bin_Values[12][30][2] = 7622;
    z_pT_Bin_Borders[13][1][0] = 0.2; z_pT_Bin_Borders[13][1][1] = 0.16; z_pT_Bin_Borders[13][1][2] = 0.22; z_pT_Bin_Borders[13][1][3] = 0.05;
    Phi_h_Bin_Values[13][1][0] =  24; Phi_h_Bin_Values[13][1][1] = 0; Phi_h_Bin_Values[13][1][2] = 7623;
    z_pT_Bin_Borders[13][2][0] = 0.2; z_pT_Bin_Borders[13][2][1] = 0.16; z_pT_Bin_Borders[13][2][2] = 0.35; z_pT_Bin_Borders[13][2][3] = 0.22;
    Phi_h_Bin_Values[13][2][0] =  24; Phi_h_Bin_Values[13][2][1] = 24; Phi_h_Bin_Values[13][2][2] = 7647;
    z_pT_Bin_Borders[13][3][0] = 0.2; z_pT_Bin_Borders[13][3][1] = 0.16; z_pT_Bin_Borders[13][3][2] = 0.45; z_pT_Bin_Borders[13][3][3] = 0.35;
    Phi_h_Bin_Values[13][3][0] =  24; Phi_h_Bin_Values[13][3][1] = 48; Phi_h_Bin_Values[13][3][2] = 7671;
    z_pT_Bin_Borders[13][4][0] = 0.2; z_pT_Bin_Borders[13][4][1] = 0.16; z_pT_Bin_Borders[13][4][2] = 0.6; z_pT_Bin_Borders[13][4][3] = 0.45;
    Phi_h_Bin_Values[13][4][0] =  1; Phi_h_Bin_Values[13][4][1] = 72; Phi_h_Bin_Values[13][4][2] = 7695;
    z_pT_Bin_Borders[13][5][0] = 0.2; z_pT_Bin_Borders[13][5][1] = 0.16; z_pT_Bin_Borders[13][5][2] = 0.9; z_pT_Bin_Borders[13][5][3] = 0.6;
    Phi_h_Bin_Values[13][5][0] =  1; Phi_h_Bin_Values[13][5][1] = 73; Phi_h_Bin_Values[13][5][2] = 7696;
    z_pT_Bin_Borders[13][6][0] = 0.24; z_pT_Bin_Borders[13][6][1] = 0.2; z_pT_Bin_Borders[13][6][2] = 0.22; z_pT_Bin_Borders[13][6][3] = 0.05;
    Phi_h_Bin_Values[13][6][0] =  24; Phi_h_Bin_Values[13][6][1] = 74; Phi_h_Bin_Values[13][6][2] = 7697;
    z_pT_Bin_Borders[13][7][0] = 0.24; z_pT_Bin_Borders[13][7][1] = 0.2; z_pT_Bin_Borders[13][7][2] = 0.35; z_pT_Bin_Borders[13][7][3] = 0.22;
    Phi_h_Bin_Values[13][7][0] =  24; Phi_h_Bin_Values[13][7][1] = 98; Phi_h_Bin_Values[13][7][2] = 7721;
    z_pT_Bin_Borders[13][8][0] = 0.24; z_pT_Bin_Borders[13][8][1] = 0.2; z_pT_Bin_Borders[13][8][2] = 0.45; z_pT_Bin_Borders[13][8][3] = 0.35;
    Phi_h_Bin_Values[13][8][0] =  24; Phi_h_Bin_Values[13][8][1] = 122; Phi_h_Bin_Values[13][8][2] = 7745;
    z_pT_Bin_Borders[13][9][0] = 0.24; z_pT_Bin_Borders[13][9][1] = 0.2; z_pT_Bin_Borders[13][9][2] = 0.6; z_pT_Bin_Borders[13][9][3] = 0.45;
    Phi_h_Bin_Values[13][9][0] =  24; Phi_h_Bin_Values[13][9][1] = 146; Phi_h_Bin_Values[13][9][2] = 7769;
    z_pT_Bin_Borders[13][10][0] = 0.24; z_pT_Bin_Borders[13][10][1] = 0.2; z_pT_Bin_Borders[13][10][2] = 0.9; z_pT_Bin_Borders[13][10][3] = 0.6;
    Phi_h_Bin_Values[13][10][0] =  1; Phi_h_Bin_Values[13][10][1] = 170; Phi_h_Bin_Values[13][10][2] = 7793;
    z_pT_Bin_Borders[13][11][0] = 0.29; z_pT_Bin_Borders[13][11][1] = 0.24; z_pT_Bin_Borders[13][11][2] = 0.22; z_pT_Bin_Borders[13][11][3] = 0.05;
    Phi_h_Bin_Values[13][11][0] =  24; Phi_h_Bin_Values[13][11][1] = 171; Phi_h_Bin_Values[13][11][2] = 7794;
    z_pT_Bin_Borders[13][12][0] = 0.29; z_pT_Bin_Borders[13][12][1] = 0.24; z_pT_Bin_Borders[13][12][2] = 0.35; z_pT_Bin_Borders[13][12][3] = 0.22;
    Phi_h_Bin_Values[13][12][0] =  24; Phi_h_Bin_Values[13][12][1] = 195; Phi_h_Bin_Values[13][12][2] = 7818;
    z_pT_Bin_Borders[13][13][0] = 0.29; z_pT_Bin_Borders[13][13][1] = 0.24; z_pT_Bin_Borders[13][13][2] = 0.45; z_pT_Bin_Borders[13][13][3] = 0.35;
    Phi_h_Bin_Values[13][13][0] =  24; Phi_h_Bin_Values[13][13][1] = 219; Phi_h_Bin_Values[13][13][2] = 7842;
    z_pT_Bin_Borders[13][14][0] = 0.29; z_pT_Bin_Borders[13][14][1] = 0.24; z_pT_Bin_Borders[13][14][2] = 0.6; z_pT_Bin_Borders[13][14][3] = 0.45;
    Phi_h_Bin_Values[13][14][0] =  24; Phi_h_Bin_Values[13][14][1] = 243; Phi_h_Bin_Values[13][14][2] = 7866;
    z_pT_Bin_Borders[13][15][0] = 0.29; z_pT_Bin_Borders[13][15][1] = 0.24; z_pT_Bin_Borders[13][15][2] = 0.9; z_pT_Bin_Borders[13][15][3] = 0.6;
    Phi_h_Bin_Values[13][15][0] =  1; Phi_h_Bin_Values[13][15][1] = 267; Phi_h_Bin_Values[13][15][2] = 7890;
    z_pT_Bin_Borders[13][16][0] = 0.36; z_pT_Bin_Borders[13][16][1] = 0.29; z_pT_Bin_Borders[13][16][2] = 0.22; z_pT_Bin_Borders[13][16][3] = 0.05;
    Phi_h_Bin_Values[13][16][0] =  24; Phi_h_Bin_Values[13][16][1] = 268; Phi_h_Bin_Values[13][16][2] = 7891;
    z_pT_Bin_Borders[13][17][0] = 0.36; z_pT_Bin_Borders[13][17][1] = 0.29; z_pT_Bin_Borders[13][17][2] = 0.35; z_pT_Bin_Borders[13][17][3] = 0.22;
    Phi_h_Bin_Values[13][17][0] =  24; Phi_h_Bin_Values[13][17][1] = 292; Phi_h_Bin_Values[13][17][2] = 7915;
    z_pT_Bin_Borders[13][18][0] = 0.36; z_pT_Bin_Borders[13][18][1] = 0.29; z_pT_Bin_Borders[13][18][2] = 0.45; z_pT_Bin_Borders[13][18][3] = 0.35;
    Phi_h_Bin_Values[13][18][0] =  24; Phi_h_Bin_Values[13][18][1] = 316; Phi_h_Bin_Values[13][18][2] = 7939;
    z_pT_Bin_Borders[13][19][0] = 0.36; z_pT_Bin_Borders[13][19][1] = 0.29; z_pT_Bin_Borders[13][19][2] = 0.6; z_pT_Bin_Borders[13][19][3] = 0.45;
    Phi_h_Bin_Values[13][19][0] =  24; Phi_h_Bin_Values[13][19][1] = 340; Phi_h_Bin_Values[13][19][2] = 7963;
    z_pT_Bin_Borders[13][20][0] = 0.36; z_pT_Bin_Borders[13][20][1] = 0.29; z_pT_Bin_Borders[13][20][2] = 0.9; z_pT_Bin_Borders[13][20][3] = 0.6;
    Phi_h_Bin_Values[13][20][0] =  24; Phi_h_Bin_Values[13][20][1] = 364; Phi_h_Bin_Values[13][20][2] = 7987;
    z_pT_Bin_Borders[13][21][0] = 0.51; z_pT_Bin_Borders[13][21][1] = 0.36; z_pT_Bin_Borders[13][21][2] = 0.22; z_pT_Bin_Borders[13][21][3] = 0.05;
    Phi_h_Bin_Values[13][21][0] =  24; Phi_h_Bin_Values[13][21][1] = 388; Phi_h_Bin_Values[13][21][2] = 8011;
    z_pT_Bin_Borders[13][22][0] = 0.51; z_pT_Bin_Borders[13][22][1] = 0.36; z_pT_Bin_Borders[13][22][2] = 0.35; z_pT_Bin_Borders[13][22][3] = 0.22;
    Phi_h_Bin_Values[13][22][0] =  24; Phi_h_Bin_Values[13][22][1] = 412; Phi_h_Bin_Values[13][22][2] = 8035;
    z_pT_Bin_Borders[13][23][0] = 0.51; z_pT_Bin_Borders[13][23][1] = 0.36; z_pT_Bin_Borders[13][23][2] = 0.45; z_pT_Bin_Borders[13][23][3] = 0.35;
    Phi_h_Bin_Values[13][23][0] =  24; Phi_h_Bin_Values[13][23][1] = 436; Phi_h_Bin_Values[13][23][2] = 8059;
    z_pT_Bin_Borders[13][24][0] = 0.51; z_pT_Bin_Borders[13][24][1] = 0.36; z_pT_Bin_Borders[13][24][2] = 0.6; z_pT_Bin_Borders[13][24][3] = 0.45;
    Phi_h_Bin_Values[13][24][0] =  24; Phi_h_Bin_Values[13][24][1] = 460; Phi_h_Bin_Values[13][24][2] = 8083;
    z_pT_Bin_Borders[13][25][0] = 0.51; z_pT_Bin_Borders[13][25][1] = 0.36; z_pT_Bin_Borders[13][25][2] = 0.9; z_pT_Bin_Borders[13][25][3] = 0.6;
    Phi_h_Bin_Values[13][25][0] =  24; Phi_h_Bin_Values[13][25][1] = 484; Phi_h_Bin_Values[13][25][2] = 8107;
    z_pT_Bin_Borders[13][26][0] = 0.72; z_pT_Bin_Borders[13][26][1] = 0.51; z_pT_Bin_Borders[13][26][2] = 0.22; z_pT_Bin_Borders[13][26][3] = 0.05;
    Phi_h_Bin_Values[13][26][0] =  24; Phi_h_Bin_Values[13][26][1] = 508; Phi_h_Bin_Values[13][26][2] = 8131;
    z_pT_Bin_Borders[13][27][0] = 0.72; z_pT_Bin_Borders[13][27][1] = 0.51; z_pT_Bin_Borders[13][27][2] = 0.35; z_pT_Bin_Borders[13][27][3] = 0.22;
    Phi_h_Bin_Values[13][27][0] =  24; Phi_h_Bin_Values[13][27][1] = 532; Phi_h_Bin_Values[13][27][2] = 8155;
    z_pT_Bin_Borders[13][28][0] = 0.72; z_pT_Bin_Borders[13][28][1] = 0.51; z_pT_Bin_Borders[13][28][2] = 0.45; z_pT_Bin_Borders[13][28][3] = 0.35;
    Phi_h_Bin_Values[13][28][0] =  24; Phi_h_Bin_Values[13][28][1] = 556; Phi_h_Bin_Values[13][28][2] = 8179;
    z_pT_Bin_Borders[13][29][0] = 0.72; z_pT_Bin_Borders[13][29][1] = 0.51; z_pT_Bin_Borders[13][29][2] = 0.6; z_pT_Bin_Borders[13][29][3] = 0.45;
    Phi_h_Bin_Values[13][29][0] =  24; Phi_h_Bin_Values[13][29][1] = 580; Phi_h_Bin_Values[13][29][2] = 8203;
    z_pT_Bin_Borders[13][30][0] = 0.72; z_pT_Bin_Borders[13][30][1] = 0.51; z_pT_Bin_Borders[13][30][2] = 0.9; z_pT_Bin_Borders[13][30][3] = 0.6;
    Phi_h_Bin_Values[13][30][0] =  1; Phi_h_Bin_Values[13][30][1] = 604; Phi_h_Bin_Values[13][30][2] = 8227;
    z_pT_Bin_Borders[13][31][0] = 0.16; z_pT_Bin_Borders[13][31][1] = 0; z_pT_Bin_Borders[13][31][2] = 0.05; z_pT_Bin_Borders[13][31][3] = 0;
    Phi_h_Bin_Values[13][31][0] =  1; Phi_h_Bin_Values[13][31][1] = 605; Phi_h_Bin_Values[13][31][2] = 8228;
    z_pT_Bin_Borders[13][32][0] = 0.16; z_pT_Bin_Borders[13][32][1] = 0; z_pT_Bin_Borders[13][32][2] = 0.05; z_pT_Bin_Borders[13][32][3] = 0.22;
    Phi_h_Bin_Values[13][32][0] =  1; Phi_h_Bin_Values[13][32][1] = 606; Phi_h_Bin_Values[13][32][2] = 8229;
    z_pT_Bin_Borders[13][33][0] = 0.16; z_pT_Bin_Borders[13][33][1] = 0; z_pT_Bin_Borders[13][33][2] = 0.22; z_pT_Bin_Borders[13][33][3] = 0.35;
    Phi_h_Bin_Values[13][33][0] =  1; Phi_h_Bin_Values[13][33][1] = 607; Phi_h_Bin_Values[13][33][2] = 8230;
    z_pT_Bin_Borders[13][34][0] = 0.16; z_pT_Bin_Borders[13][34][1] = 0; z_pT_Bin_Borders[13][34][2] = 0.35; z_pT_Bin_Borders[13][34][3] = 0.45;
    Phi_h_Bin_Values[13][34][0] =  1; Phi_h_Bin_Values[13][34][1] = 608; Phi_h_Bin_Values[13][34][2] = 8231;
    z_pT_Bin_Borders[13][35][0] = 0.16; z_pT_Bin_Borders[13][35][1] = 0; z_pT_Bin_Borders[13][35][2] = 0.45; z_pT_Bin_Borders[13][35][3] = 0.6;
    Phi_h_Bin_Values[13][35][0] =  1; Phi_h_Bin_Values[13][35][1] = 609; Phi_h_Bin_Values[13][35][2] = 8232;
    z_pT_Bin_Borders[13][36][0] = 0.16; z_pT_Bin_Borders[13][36][1] = 0; z_pT_Bin_Borders[13][36][2] = 0.6; z_pT_Bin_Borders[13][36][3] = 0.9;
    Phi_h_Bin_Values[13][36][0] =  1; Phi_h_Bin_Values[13][36][1] = 610; Phi_h_Bin_Values[13][36][2] = 8233;
    z_pT_Bin_Borders[13][37][0] = 0.16; z_pT_Bin_Borders[13][37][1] = 0; z_pT_Bin_Borders[13][37][2] = 10; z_pT_Bin_Borders[13][37][3] = 0.9;
    Phi_h_Bin_Values[13][37][0] =  1; Phi_h_Bin_Values[13][37][1] = 611; Phi_h_Bin_Values[13][37][2] = 8234;
    z_pT_Bin_Borders[13][38][0] = 0.16; z_pT_Bin_Borders[13][38][1] = 0.2; z_pT_Bin_Borders[13][38][2] = 0.05; z_pT_Bin_Borders[13][38][3] = 0;
    Phi_h_Bin_Values[13][38][0] =  1; Phi_h_Bin_Values[13][38][1] = 612; Phi_h_Bin_Values[13][38][2] = 8235;
    z_pT_Bin_Borders[13][39][0] = 0.16; z_pT_Bin_Borders[13][39][1] = 0.2; z_pT_Bin_Borders[13][39][2] = 10; z_pT_Bin_Borders[13][39][3] = 0.9;
    Phi_h_Bin_Values[13][39][0] =  1; Phi_h_Bin_Values[13][39][1] = 613; Phi_h_Bin_Values[13][39][2] = 8236;
    z_pT_Bin_Borders[13][40][0] = 0.2; z_pT_Bin_Borders[13][40][1] = 0.24; z_pT_Bin_Borders[13][40][2] = 0.05; z_pT_Bin_Borders[13][40][3] = 0;
    Phi_h_Bin_Values[13][40][0] =  1; Phi_h_Bin_Values[13][40][1] = 614; Phi_h_Bin_Values[13][40][2] = 8237;
    z_pT_Bin_Borders[13][41][0] = 0.2; z_pT_Bin_Borders[13][41][1] = 0.24; z_pT_Bin_Borders[13][41][2] = 10; z_pT_Bin_Borders[13][41][3] = 0.9;
    Phi_h_Bin_Values[13][41][0] =  1; Phi_h_Bin_Values[13][41][1] = 615; Phi_h_Bin_Values[13][41][2] = 8238;
    z_pT_Bin_Borders[13][42][0] = 0.24; z_pT_Bin_Borders[13][42][1] = 0.29; z_pT_Bin_Borders[13][42][2] = 0.05; z_pT_Bin_Borders[13][42][3] = 0;
    Phi_h_Bin_Values[13][42][0] =  1; Phi_h_Bin_Values[13][42][1] = 616; Phi_h_Bin_Values[13][42][2] = 8239;
    z_pT_Bin_Borders[13][43][0] = 0.24; z_pT_Bin_Borders[13][43][1] = 0.29; z_pT_Bin_Borders[13][43][2] = 10; z_pT_Bin_Borders[13][43][3] = 0.9;
    Phi_h_Bin_Values[13][43][0] =  1; Phi_h_Bin_Values[13][43][1] = 617; Phi_h_Bin_Values[13][43][2] = 8240;
    z_pT_Bin_Borders[13][44][0] = 0.29; z_pT_Bin_Borders[13][44][1] = 0.36; z_pT_Bin_Borders[13][44][2] = 0.05; z_pT_Bin_Borders[13][44][3] = 0;
    Phi_h_Bin_Values[13][44][0] =  1; Phi_h_Bin_Values[13][44][1] = 618; Phi_h_Bin_Values[13][44][2] = 8241;
    z_pT_Bin_Borders[13][45][0] = 0.29; z_pT_Bin_Borders[13][45][1] = 0.36; z_pT_Bin_Borders[13][45][2] = 10; z_pT_Bin_Borders[13][45][3] = 0.9;
    Phi_h_Bin_Values[13][45][0] =  1; Phi_h_Bin_Values[13][45][1] = 619; Phi_h_Bin_Values[13][45][2] = 8242;
    z_pT_Bin_Borders[13][46][0] = 0.36; z_pT_Bin_Borders[13][46][1] = 0.51; z_pT_Bin_Borders[13][46][2] = 0.05; z_pT_Bin_Borders[13][46][3] = 0;
    Phi_h_Bin_Values[13][46][0] =  1; Phi_h_Bin_Values[13][46][1] = 620; Phi_h_Bin_Values[13][46][2] = 8243;
    z_pT_Bin_Borders[13][47][0] = 0.36; z_pT_Bin_Borders[13][47][1] = 0.51; z_pT_Bin_Borders[13][47][2] = 10; z_pT_Bin_Borders[13][47][3] = 0.9;
    Phi_h_Bin_Values[13][47][0] =  1; Phi_h_Bin_Values[13][47][1] = 621; Phi_h_Bin_Values[13][47][2] = 8244;
    z_pT_Bin_Borders[13][48][0] = 0.51; z_pT_Bin_Borders[13][48][1] = 0.72; z_pT_Bin_Borders[13][48][2] = 0.05; z_pT_Bin_Borders[13][48][3] = 0;
    Phi_h_Bin_Values[13][48][0] =  1; Phi_h_Bin_Values[13][48][1] = 622; Phi_h_Bin_Values[13][48][2] = 8245;
    z_pT_Bin_Borders[13][49][0] = 0.51; z_pT_Bin_Borders[13][49][1] = 0.72; z_pT_Bin_Borders[13][49][2] = 10; z_pT_Bin_Borders[13][49][3] = 0.9;
    Phi_h_Bin_Values[13][49][0] =  1; Phi_h_Bin_Values[13][49][1] = 623; Phi_h_Bin_Values[13][49][2] = 8246;
    z_pT_Bin_Borders[13][50][0] = 10; z_pT_Bin_Borders[13][50][1] = 0.72; z_pT_Bin_Borders[13][50][2] = 0; z_pT_Bin_Borders[13][50][3] = 0.05;
    Phi_h_Bin_Values[13][50][0] =  1; Phi_h_Bin_Values[13][50][1] = 624; Phi_h_Bin_Values[13][50][2] = 8247;
    z_pT_Bin_Borders[13][51][0] = 10; z_pT_Bin_Borders[13][51][1] = 0.72; z_pT_Bin_Borders[13][51][2] = 0.05; z_pT_Bin_Borders[13][51][3] = 0.22;
    Phi_h_Bin_Values[13][51][0] =  1; Phi_h_Bin_Values[13][51][1] = 625; Phi_h_Bin_Values[13][51][2] = 8248;
    z_pT_Bin_Borders[13][52][0] = 10; z_pT_Bin_Borders[13][52][1] = 0.72; z_pT_Bin_Borders[13][52][2] = 0.22; z_pT_Bin_Borders[13][52][3] = 0.35;
    Phi_h_Bin_Values[13][52][0] =  1; Phi_h_Bin_Values[13][52][1] = 626; Phi_h_Bin_Values[13][52][2] = 8249;
    z_pT_Bin_Borders[13][53][0] = 10; z_pT_Bin_Borders[13][53][1] = 0.72; z_pT_Bin_Borders[13][53][2] = 0.35; z_pT_Bin_Borders[13][53][3] = 0.45;
    Phi_h_Bin_Values[13][53][0] =  1; Phi_h_Bin_Values[13][53][1] = 627; Phi_h_Bin_Values[13][53][2] = 8250;
    z_pT_Bin_Borders[13][54][0] = 10; z_pT_Bin_Borders[13][54][1] = 0.72; z_pT_Bin_Borders[13][54][2] = 0.45; z_pT_Bin_Borders[13][54][3] = 0.6;
    Phi_h_Bin_Values[13][54][0] =  1; Phi_h_Bin_Values[13][54][1] = 628; Phi_h_Bin_Values[13][54][2] = 8251;
    z_pT_Bin_Borders[13][55][0] = 10; z_pT_Bin_Borders[13][55][1] = 0.72; z_pT_Bin_Borders[13][55][2] = 0.6; z_pT_Bin_Borders[13][55][3] = 0.9;
    Phi_h_Bin_Values[13][55][0] =  1; Phi_h_Bin_Values[13][55][1] = 629; Phi_h_Bin_Values[13][55][2] = 8252;
    z_pT_Bin_Borders[13][56][0] = 10; z_pT_Bin_Borders[13][56][1] = 0.72; z_pT_Bin_Borders[13][56][2] = 10; z_pT_Bin_Borders[13][56][3] = 0.9;
    Phi_h_Bin_Values[13][56][0] =  1; Phi_h_Bin_Values[13][56][1] = 630; Phi_h_Bin_Values[13][56][2] = 8253;
    z_pT_Bin_Borders[14][1][0] = 0.23; z_pT_Bin_Borders[14][1][1] = 0.19; z_pT_Bin_Borders[14][1][2] = 0.2; z_pT_Bin_Borders[14][1][3] = 0.05;
    Phi_h_Bin_Values[14][1][0] =  24; Phi_h_Bin_Values[14][1][1] = 0; Phi_h_Bin_Values[14][1][2] = 8254;
    z_pT_Bin_Borders[14][2][0] = 0.23; z_pT_Bin_Borders[14][2][1] = 0.19; z_pT_Bin_Borders[14][2][2] = 0.3; z_pT_Bin_Borders[14][2][3] = 0.2;
    Phi_h_Bin_Values[14][2][0] =  24; Phi_h_Bin_Values[14][2][1] = 24; Phi_h_Bin_Values[14][2][2] = 8278;
    z_pT_Bin_Borders[14][3][0] = 0.23; z_pT_Bin_Borders[14][3][1] = 0.19; z_pT_Bin_Borders[14][3][2] = 0.4; z_pT_Bin_Borders[14][3][3] = 0.3;
    Phi_h_Bin_Values[14][3][0] =  24; Phi_h_Bin_Values[14][3][1] = 48; Phi_h_Bin_Values[14][3][2] = 8302;
    z_pT_Bin_Borders[14][4][0] = 0.23; z_pT_Bin_Borders[14][4][1] = 0.19; z_pT_Bin_Borders[14][4][2] = 0.5; z_pT_Bin_Borders[14][4][3] = 0.4;
    Phi_h_Bin_Values[14][4][0] =  24; Phi_h_Bin_Values[14][4][1] = 72; Phi_h_Bin_Values[14][4][2] = 8326;
    z_pT_Bin_Borders[14][5][0] = 0.23; z_pT_Bin_Borders[14][5][1] = 0.19; z_pT_Bin_Borders[14][5][2] = 0.65; z_pT_Bin_Borders[14][5][3] = 0.5;
    Phi_h_Bin_Values[14][5][0] =  1; Phi_h_Bin_Values[14][5][1] = 96; Phi_h_Bin_Values[14][5][2] = 8350;
    z_pT_Bin_Borders[14][6][0] = 0.23; z_pT_Bin_Borders[14][6][1] = 0.19; z_pT_Bin_Borders[14][6][2] = 0.8; z_pT_Bin_Borders[14][6][3] = 0.65;
    Phi_h_Bin_Values[14][6][0] =  1; Phi_h_Bin_Values[14][6][1] = 97; Phi_h_Bin_Values[14][6][2] = 8351;
    z_pT_Bin_Borders[14][7][0] = 0.27; z_pT_Bin_Borders[14][7][1] = 0.23; z_pT_Bin_Borders[14][7][2] = 0.2; z_pT_Bin_Borders[14][7][3] = 0.05;
    Phi_h_Bin_Values[14][7][0] =  24; Phi_h_Bin_Values[14][7][1] = 98; Phi_h_Bin_Values[14][7][2] = 8352;
    z_pT_Bin_Borders[14][8][0] = 0.27; z_pT_Bin_Borders[14][8][1] = 0.23; z_pT_Bin_Borders[14][8][2] = 0.3; z_pT_Bin_Borders[14][8][3] = 0.2;
    Phi_h_Bin_Values[14][8][0] =  24; Phi_h_Bin_Values[14][8][1] = 122; Phi_h_Bin_Values[14][8][2] = 8376;
    z_pT_Bin_Borders[14][9][0] = 0.27; z_pT_Bin_Borders[14][9][1] = 0.23; z_pT_Bin_Borders[14][9][2] = 0.4; z_pT_Bin_Borders[14][9][3] = 0.3;
    Phi_h_Bin_Values[14][9][0] =  24; Phi_h_Bin_Values[14][9][1] = 146; Phi_h_Bin_Values[14][9][2] = 8400;
    z_pT_Bin_Borders[14][10][0] = 0.27; z_pT_Bin_Borders[14][10][1] = 0.23; z_pT_Bin_Borders[14][10][2] = 0.5; z_pT_Bin_Borders[14][10][3] = 0.4;
    Phi_h_Bin_Values[14][10][0] =  24; Phi_h_Bin_Values[14][10][1] = 170; Phi_h_Bin_Values[14][10][2] = 8424;
    z_pT_Bin_Borders[14][11][0] = 0.27; z_pT_Bin_Borders[14][11][1] = 0.23; z_pT_Bin_Borders[14][11][2] = 0.65; z_pT_Bin_Borders[14][11][3] = 0.5;
    Phi_h_Bin_Values[14][11][0] =  24; Phi_h_Bin_Values[14][11][1] = 194; Phi_h_Bin_Values[14][11][2] = 8448;
    z_pT_Bin_Borders[14][12][0] = 0.27; z_pT_Bin_Borders[14][12][1] = 0.23; z_pT_Bin_Borders[14][12][2] = 0.8; z_pT_Bin_Borders[14][12][3] = 0.65;
    Phi_h_Bin_Values[14][12][0] =  1; Phi_h_Bin_Values[14][12][1] = 218; Phi_h_Bin_Values[14][12][2] = 8472;
    z_pT_Bin_Borders[14][13][0] = 0.32; z_pT_Bin_Borders[14][13][1] = 0.27; z_pT_Bin_Borders[14][13][2] = 0.2; z_pT_Bin_Borders[14][13][3] = 0.05;
    Phi_h_Bin_Values[14][13][0] =  24; Phi_h_Bin_Values[14][13][1] = 219; Phi_h_Bin_Values[14][13][2] = 8473;
    z_pT_Bin_Borders[14][14][0] = 0.32; z_pT_Bin_Borders[14][14][1] = 0.27; z_pT_Bin_Borders[14][14][2] = 0.3; z_pT_Bin_Borders[14][14][3] = 0.2;
    Phi_h_Bin_Values[14][14][0] =  24; Phi_h_Bin_Values[14][14][1] = 243; Phi_h_Bin_Values[14][14][2] = 8497;
    z_pT_Bin_Borders[14][15][0] = 0.32; z_pT_Bin_Borders[14][15][1] = 0.27; z_pT_Bin_Borders[14][15][2] = 0.4; z_pT_Bin_Borders[14][15][3] = 0.3;
    Phi_h_Bin_Values[14][15][0] =  24; Phi_h_Bin_Values[14][15][1] = 267; Phi_h_Bin_Values[14][15][2] = 8521;
    z_pT_Bin_Borders[14][16][0] = 0.32; z_pT_Bin_Borders[14][16][1] = 0.27; z_pT_Bin_Borders[14][16][2] = 0.5; z_pT_Bin_Borders[14][16][3] = 0.4;
    Phi_h_Bin_Values[14][16][0] =  24; Phi_h_Bin_Values[14][16][1] = 291; Phi_h_Bin_Values[14][16][2] = 8545;
    z_pT_Bin_Borders[14][17][0] = 0.32; z_pT_Bin_Borders[14][17][1] = 0.27; z_pT_Bin_Borders[14][17][2] = 0.65; z_pT_Bin_Borders[14][17][3] = 0.5;
    Phi_h_Bin_Values[14][17][0] =  24; Phi_h_Bin_Values[14][17][1] = 315; Phi_h_Bin_Values[14][17][2] = 8569;
    z_pT_Bin_Borders[14][18][0] = 0.32; z_pT_Bin_Borders[14][18][1] = 0.27; z_pT_Bin_Borders[14][18][2] = 0.8; z_pT_Bin_Borders[14][18][3] = 0.65;
    Phi_h_Bin_Values[14][18][0] =  1; Phi_h_Bin_Values[14][18][1] = 339; Phi_h_Bin_Values[14][18][2] = 8593;
    z_pT_Bin_Borders[14][19][0] = 0.4; z_pT_Bin_Borders[14][19][1] = 0.32; z_pT_Bin_Borders[14][19][2] = 0.2; z_pT_Bin_Borders[14][19][3] = 0.05;
    Phi_h_Bin_Values[14][19][0] =  24; Phi_h_Bin_Values[14][19][1] = 340; Phi_h_Bin_Values[14][19][2] = 8594;
    z_pT_Bin_Borders[14][20][0] = 0.4; z_pT_Bin_Borders[14][20][1] = 0.32; z_pT_Bin_Borders[14][20][2] = 0.3; z_pT_Bin_Borders[14][20][3] = 0.2;
    Phi_h_Bin_Values[14][20][0] =  24; Phi_h_Bin_Values[14][20][1] = 364; Phi_h_Bin_Values[14][20][2] = 8618;
    z_pT_Bin_Borders[14][21][0] = 0.4; z_pT_Bin_Borders[14][21][1] = 0.32; z_pT_Bin_Borders[14][21][2] = 0.4; z_pT_Bin_Borders[14][21][3] = 0.3;
    Phi_h_Bin_Values[14][21][0] =  24; Phi_h_Bin_Values[14][21][1] = 388; Phi_h_Bin_Values[14][21][2] = 8642;
    z_pT_Bin_Borders[14][22][0] = 0.4; z_pT_Bin_Borders[14][22][1] = 0.32; z_pT_Bin_Borders[14][22][2] = 0.5; z_pT_Bin_Borders[14][22][3] = 0.4;
    Phi_h_Bin_Values[14][22][0] =  24; Phi_h_Bin_Values[14][22][1] = 412; Phi_h_Bin_Values[14][22][2] = 8666;
    z_pT_Bin_Borders[14][23][0] = 0.4; z_pT_Bin_Borders[14][23][1] = 0.32; z_pT_Bin_Borders[14][23][2] = 0.65; z_pT_Bin_Borders[14][23][3] = 0.5;
    Phi_h_Bin_Values[14][23][0] =  24; Phi_h_Bin_Values[14][23][1] = 436; Phi_h_Bin_Values[14][23][2] = 8690;
    z_pT_Bin_Borders[14][24][0] = 0.4; z_pT_Bin_Borders[14][24][1] = 0.32; z_pT_Bin_Borders[14][24][2] = 0.8; z_pT_Bin_Borders[14][24][3] = 0.65;
    Phi_h_Bin_Values[14][24][0] =  1; Phi_h_Bin_Values[14][24][1] = 460; Phi_h_Bin_Values[14][24][2] = 8714;
    z_pT_Bin_Borders[14][25][0] = 0.53; z_pT_Bin_Borders[14][25][1] = 0.4; z_pT_Bin_Borders[14][25][2] = 0.2; z_pT_Bin_Borders[14][25][3] = 0.05;
    Phi_h_Bin_Values[14][25][0] =  24; Phi_h_Bin_Values[14][25][1] = 461; Phi_h_Bin_Values[14][25][2] = 8715;
    z_pT_Bin_Borders[14][26][0] = 0.53; z_pT_Bin_Borders[14][26][1] = 0.4; z_pT_Bin_Borders[14][26][2] = 0.3; z_pT_Bin_Borders[14][26][3] = 0.2;
    Phi_h_Bin_Values[14][26][0] =  24; Phi_h_Bin_Values[14][26][1] = 485; Phi_h_Bin_Values[14][26][2] = 8739;
    z_pT_Bin_Borders[14][27][0] = 0.53; z_pT_Bin_Borders[14][27][1] = 0.4; z_pT_Bin_Borders[14][27][2] = 0.4; z_pT_Bin_Borders[14][27][3] = 0.3;
    Phi_h_Bin_Values[14][27][0] =  24; Phi_h_Bin_Values[14][27][1] = 509; Phi_h_Bin_Values[14][27][2] = 8763;
    z_pT_Bin_Borders[14][28][0] = 0.53; z_pT_Bin_Borders[14][28][1] = 0.4; z_pT_Bin_Borders[14][28][2] = 0.5; z_pT_Bin_Borders[14][28][3] = 0.4;
    Phi_h_Bin_Values[14][28][0] =  24; Phi_h_Bin_Values[14][28][1] = 533; Phi_h_Bin_Values[14][28][2] = 8787;
    z_pT_Bin_Borders[14][29][0] = 0.53; z_pT_Bin_Borders[14][29][1] = 0.4; z_pT_Bin_Borders[14][29][2] = 0.65; z_pT_Bin_Borders[14][29][3] = 0.5;
    Phi_h_Bin_Values[14][29][0] =  24; Phi_h_Bin_Values[14][29][1] = 557; Phi_h_Bin_Values[14][29][2] = 8811;
    z_pT_Bin_Borders[14][30][0] = 0.53; z_pT_Bin_Borders[14][30][1] = 0.4; z_pT_Bin_Borders[14][30][2] = 0.8; z_pT_Bin_Borders[14][30][3] = 0.65;
    Phi_h_Bin_Values[14][30][0] =  1; Phi_h_Bin_Values[14][30][1] = 581; Phi_h_Bin_Values[14][30][2] = 8835;
    z_pT_Bin_Borders[14][31][0] = 0.69; z_pT_Bin_Borders[14][31][1] = 0.53; z_pT_Bin_Borders[14][31][2] = 0.2; z_pT_Bin_Borders[14][31][3] = 0.05;
    Phi_h_Bin_Values[14][31][0] =  24; Phi_h_Bin_Values[14][31][1] = 582; Phi_h_Bin_Values[14][31][2] = 8836;
    z_pT_Bin_Borders[14][32][0] = 0.69; z_pT_Bin_Borders[14][32][1] = 0.53; z_pT_Bin_Borders[14][32][2] = 0.3; z_pT_Bin_Borders[14][32][3] = 0.2;
    Phi_h_Bin_Values[14][32][0] =  24; Phi_h_Bin_Values[14][32][1] = 606; Phi_h_Bin_Values[14][32][2] = 8860;
    z_pT_Bin_Borders[14][33][0] = 0.69; z_pT_Bin_Borders[14][33][1] = 0.53; z_pT_Bin_Borders[14][33][2] = 0.4; z_pT_Bin_Borders[14][33][3] = 0.3;
    Phi_h_Bin_Values[14][33][0] =  24; Phi_h_Bin_Values[14][33][1] = 630; Phi_h_Bin_Values[14][33][2] = 8884;
    z_pT_Bin_Borders[14][34][0] = 0.69; z_pT_Bin_Borders[14][34][1] = 0.53; z_pT_Bin_Borders[14][34][2] = 0.5; z_pT_Bin_Borders[14][34][3] = 0.4;
    Phi_h_Bin_Values[14][34][0] =  1; Phi_h_Bin_Values[14][34][1] = 654; Phi_h_Bin_Values[14][34][2] = 8908;
    z_pT_Bin_Borders[14][35][0] = 0.69; z_pT_Bin_Borders[14][35][1] = 0.53; z_pT_Bin_Borders[14][35][2] = 0.65; z_pT_Bin_Borders[14][35][3] = 0.5;
    Phi_h_Bin_Values[14][35][0] =  1; Phi_h_Bin_Values[14][35][1] = 655; Phi_h_Bin_Values[14][35][2] = 8909;
    z_pT_Bin_Borders[14][36][0] = 0.69; z_pT_Bin_Borders[14][36][1] = 0.53; z_pT_Bin_Borders[14][36][2] = 0.8; z_pT_Bin_Borders[14][36][3] = 0.65;
    Phi_h_Bin_Values[14][36][0] =  1; Phi_h_Bin_Values[14][36][1] = 656; Phi_h_Bin_Values[14][36][2] = 8910;
    z_pT_Bin_Borders[14][37][0] = 0.19; z_pT_Bin_Borders[14][37][1] = 0; z_pT_Bin_Borders[14][37][2] = 0.05; z_pT_Bin_Borders[14][37][3] = 0;
    Phi_h_Bin_Values[14][37][0] =  1; Phi_h_Bin_Values[14][37][1] = 657; Phi_h_Bin_Values[14][37][2] = 8911;
    z_pT_Bin_Borders[14][38][0] = 0.19; z_pT_Bin_Borders[14][38][1] = 0; z_pT_Bin_Borders[14][38][2] = 0.05; z_pT_Bin_Borders[14][38][3] = 0.2;
    Phi_h_Bin_Values[14][38][0] =  1; Phi_h_Bin_Values[14][38][1] = 658; Phi_h_Bin_Values[14][38][2] = 8912;
    z_pT_Bin_Borders[14][39][0] = 0.19; z_pT_Bin_Borders[14][39][1] = 0; z_pT_Bin_Borders[14][39][2] = 0.2; z_pT_Bin_Borders[14][39][3] = 0.3;
    Phi_h_Bin_Values[14][39][0] =  1; Phi_h_Bin_Values[14][39][1] = 659; Phi_h_Bin_Values[14][39][2] = 8913;
    z_pT_Bin_Borders[14][40][0] = 0.19; z_pT_Bin_Borders[14][40][1] = 0; z_pT_Bin_Borders[14][40][2] = 0.3; z_pT_Bin_Borders[14][40][3] = 0.4;
    Phi_h_Bin_Values[14][40][0] =  1; Phi_h_Bin_Values[14][40][1] = 660; Phi_h_Bin_Values[14][40][2] = 8914;
    z_pT_Bin_Borders[14][41][0] = 0.19; z_pT_Bin_Borders[14][41][1] = 0; z_pT_Bin_Borders[14][41][2] = 0.4; z_pT_Bin_Borders[14][41][3] = 0.5;
    Phi_h_Bin_Values[14][41][0] =  1; Phi_h_Bin_Values[14][41][1] = 661; Phi_h_Bin_Values[14][41][2] = 8915;
    z_pT_Bin_Borders[14][42][0] = 0.19; z_pT_Bin_Borders[14][42][1] = 0; z_pT_Bin_Borders[14][42][2] = 0.5; z_pT_Bin_Borders[14][42][3] = 0.65;
    Phi_h_Bin_Values[14][42][0] =  1; Phi_h_Bin_Values[14][42][1] = 662; Phi_h_Bin_Values[14][42][2] = 8916;
    z_pT_Bin_Borders[14][43][0] = 0.19; z_pT_Bin_Borders[14][43][1] = 0; z_pT_Bin_Borders[14][43][2] = 0.65; z_pT_Bin_Borders[14][43][3] = 0.8;
    Phi_h_Bin_Values[14][43][0] =  1; Phi_h_Bin_Values[14][43][1] = 663; Phi_h_Bin_Values[14][43][2] = 8917;
    z_pT_Bin_Borders[14][44][0] = 0.19; z_pT_Bin_Borders[14][44][1] = 0; z_pT_Bin_Borders[14][44][2] = 10; z_pT_Bin_Borders[14][44][3] = 0.8;
    Phi_h_Bin_Values[14][44][0] =  1; Phi_h_Bin_Values[14][44][1] = 664; Phi_h_Bin_Values[14][44][2] = 8918;
    z_pT_Bin_Borders[14][45][0] = 0.19; z_pT_Bin_Borders[14][45][1] = 0.23; z_pT_Bin_Borders[14][45][2] = 0.05; z_pT_Bin_Borders[14][45][3] = 0;
    Phi_h_Bin_Values[14][45][0] =  1; Phi_h_Bin_Values[14][45][1] = 665; Phi_h_Bin_Values[14][45][2] = 8919;
    z_pT_Bin_Borders[14][46][0] = 0.19; z_pT_Bin_Borders[14][46][1] = 0.23; z_pT_Bin_Borders[14][46][2] = 10; z_pT_Bin_Borders[14][46][3] = 0.8;
    Phi_h_Bin_Values[14][46][0] =  1; Phi_h_Bin_Values[14][46][1] = 666; Phi_h_Bin_Values[14][46][2] = 8920;
    z_pT_Bin_Borders[14][47][0] = 0.23; z_pT_Bin_Borders[14][47][1] = 0.27; z_pT_Bin_Borders[14][47][2] = 0.05; z_pT_Bin_Borders[14][47][3] = 0;
    Phi_h_Bin_Values[14][47][0] =  1; Phi_h_Bin_Values[14][47][1] = 667; Phi_h_Bin_Values[14][47][2] = 8921;
    z_pT_Bin_Borders[14][48][0] = 0.23; z_pT_Bin_Borders[14][48][1] = 0.27; z_pT_Bin_Borders[14][48][2] = 10; z_pT_Bin_Borders[14][48][3] = 0.8;
    Phi_h_Bin_Values[14][48][0] =  1; Phi_h_Bin_Values[14][48][1] = 668; Phi_h_Bin_Values[14][48][2] = 8922;
    z_pT_Bin_Borders[14][49][0] = 0.27; z_pT_Bin_Borders[14][49][1] = 0.32; z_pT_Bin_Borders[14][49][2] = 0.05; z_pT_Bin_Borders[14][49][3] = 0;
    Phi_h_Bin_Values[14][49][0] =  1; Phi_h_Bin_Values[14][49][1] = 669; Phi_h_Bin_Values[14][49][2] = 8923;
    z_pT_Bin_Borders[14][50][0] = 0.27; z_pT_Bin_Borders[14][50][1] = 0.32; z_pT_Bin_Borders[14][50][2] = 10; z_pT_Bin_Borders[14][50][3] = 0.8;
    Phi_h_Bin_Values[14][50][0] =  1; Phi_h_Bin_Values[14][50][1] = 670; Phi_h_Bin_Values[14][50][2] = 8924;
    z_pT_Bin_Borders[14][51][0] = 0.32; z_pT_Bin_Borders[14][51][1] = 0.4; z_pT_Bin_Borders[14][51][2] = 0.05; z_pT_Bin_Borders[14][51][3] = 0;
    Phi_h_Bin_Values[14][51][0] =  1; Phi_h_Bin_Values[14][51][1] = 671; Phi_h_Bin_Values[14][51][2] = 8925;
    z_pT_Bin_Borders[14][52][0] = 0.32; z_pT_Bin_Borders[14][52][1] = 0.4; z_pT_Bin_Borders[14][52][2] = 10; z_pT_Bin_Borders[14][52][3] = 0.8;
    Phi_h_Bin_Values[14][52][0] =  1; Phi_h_Bin_Values[14][52][1] = 672; Phi_h_Bin_Values[14][52][2] = 8926;
    z_pT_Bin_Borders[14][53][0] = 0.4; z_pT_Bin_Borders[14][53][1] = 0.53; z_pT_Bin_Borders[14][53][2] = 0.05; z_pT_Bin_Borders[14][53][3] = 0;
    Phi_h_Bin_Values[14][53][0] =  1; Phi_h_Bin_Values[14][53][1] = 673; Phi_h_Bin_Values[14][53][2] = 8927;
    z_pT_Bin_Borders[14][54][0] = 0.4; z_pT_Bin_Borders[14][54][1] = 0.53; z_pT_Bin_Borders[14][54][2] = 10; z_pT_Bin_Borders[14][54][3] = 0.8;
    Phi_h_Bin_Values[14][54][0] =  1; Phi_h_Bin_Values[14][54][1] = 674; Phi_h_Bin_Values[14][54][2] = 8928;
    z_pT_Bin_Borders[14][55][0] = 0.53; z_pT_Bin_Borders[14][55][1] = 0.69; z_pT_Bin_Borders[14][55][2] = 0.05; z_pT_Bin_Borders[14][55][3] = 0;
    Phi_h_Bin_Values[14][55][0] =  1; Phi_h_Bin_Values[14][55][1] = 675; Phi_h_Bin_Values[14][55][2] = 8929;
    z_pT_Bin_Borders[14][56][0] = 0.53; z_pT_Bin_Borders[14][56][1] = 0.69; z_pT_Bin_Borders[14][56][2] = 10; z_pT_Bin_Borders[14][56][3] = 0.8;
    Phi_h_Bin_Values[14][56][0] =  1; Phi_h_Bin_Values[14][56][1] = 676; Phi_h_Bin_Values[14][56][2] = 8930;
    z_pT_Bin_Borders[14][57][0] = 10; z_pT_Bin_Borders[14][57][1] = 0.69; z_pT_Bin_Borders[14][57][2] = 0; z_pT_Bin_Borders[14][57][3] = 0.05;
    Phi_h_Bin_Values[14][57][0] =  1; Phi_h_Bin_Values[14][57][1] = 677; Phi_h_Bin_Values[14][57][2] = 8931;
    z_pT_Bin_Borders[14][58][0] = 10; z_pT_Bin_Borders[14][58][1] = 0.69; z_pT_Bin_Borders[14][58][2] = 0.05; z_pT_Bin_Borders[14][58][3] = 0.2;
    Phi_h_Bin_Values[14][58][0] =  1; Phi_h_Bin_Values[14][58][1] = 678; Phi_h_Bin_Values[14][58][2] = 8932;
    z_pT_Bin_Borders[14][59][0] = 10; z_pT_Bin_Borders[14][59][1] = 0.69; z_pT_Bin_Borders[14][59][2] = 0.2; z_pT_Bin_Borders[14][59][3] = 0.3;
    Phi_h_Bin_Values[14][59][0] =  1; Phi_h_Bin_Values[14][59][1] = 679; Phi_h_Bin_Values[14][59][2] = 8933;
    z_pT_Bin_Borders[14][60][0] = 10; z_pT_Bin_Borders[14][60][1] = 0.69; z_pT_Bin_Borders[14][60][2] = 0.3; z_pT_Bin_Borders[14][60][3] = 0.4;
    Phi_h_Bin_Values[14][60][0] =  1; Phi_h_Bin_Values[14][60][1] = 680; Phi_h_Bin_Values[14][60][2] = 8934;
    z_pT_Bin_Borders[14][61][0] = 10; z_pT_Bin_Borders[14][61][1] = 0.69; z_pT_Bin_Borders[14][61][2] = 0.4; z_pT_Bin_Borders[14][61][3] = 0.5;
    Phi_h_Bin_Values[14][61][0] =  1; Phi_h_Bin_Values[14][61][1] = 681; Phi_h_Bin_Values[14][61][2] = 8935;
    z_pT_Bin_Borders[14][62][0] = 10; z_pT_Bin_Borders[14][62][1] = 0.69; z_pT_Bin_Borders[14][62][2] = 0.5; z_pT_Bin_Borders[14][62][3] = 0.65;
    Phi_h_Bin_Values[14][62][0] =  1; Phi_h_Bin_Values[14][62][1] = 682; Phi_h_Bin_Values[14][62][2] = 8936;
    z_pT_Bin_Borders[14][63][0] = 10; z_pT_Bin_Borders[14][63][1] = 0.69; z_pT_Bin_Borders[14][63][2] = 0.65; z_pT_Bin_Borders[14][63][3] = 0.8;
    Phi_h_Bin_Values[14][63][0] =  1; Phi_h_Bin_Values[14][63][1] = 683; Phi_h_Bin_Values[14][63][2] = 8937;
    z_pT_Bin_Borders[14][64][0] = 10; z_pT_Bin_Borders[14][64][1] = 0.69; z_pT_Bin_Borders[14][64][2] = 10; z_pT_Bin_Borders[14][64][3] = 0.8;
    Phi_h_Bin_Values[14][64][0] =  1; Phi_h_Bin_Values[14][64][1] = 684; Phi_h_Bin_Values[14][64][2] = 8938;
    z_pT_Bin_Borders[15][1][0] = 0.28; z_pT_Bin_Borders[15][1][1] = 0.22; z_pT_Bin_Borders[15][1][2] = 0.23; z_pT_Bin_Borders[15][1][3] = 0.05;
    Phi_h_Bin_Values[15][1][0] =  24; Phi_h_Bin_Values[15][1][1] = 0; Phi_h_Bin_Values[15][1][2] = 8939;
    z_pT_Bin_Borders[15][2][0] = 0.28; z_pT_Bin_Borders[15][2][1] = 0.22; z_pT_Bin_Borders[15][2][2] = 0.33; z_pT_Bin_Borders[15][2][3] = 0.23;
    Phi_h_Bin_Values[15][2][0] =  24; Phi_h_Bin_Values[15][2][1] = 24; Phi_h_Bin_Values[15][2][2] = 8963;
    z_pT_Bin_Borders[15][3][0] = 0.28; z_pT_Bin_Borders[15][3][1] = 0.22; z_pT_Bin_Borders[15][3][2] = 0.47; z_pT_Bin_Borders[15][3][3] = 0.33;
    Phi_h_Bin_Values[15][3][0] =  24; Phi_h_Bin_Values[15][3][1] = 48; Phi_h_Bin_Values[15][3][2] = 8987;
    z_pT_Bin_Borders[15][4][0] = 0.33; z_pT_Bin_Borders[15][4][1] = 0.28; z_pT_Bin_Borders[15][4][2] = 0.23; z_pT_Bin_Borders[15][4][3] = 0.05;
    Phi_h_Bin_Values[15][4][0] =  24; Phi_h_Bin_Values[15][4][1] = 72; Phi_h_Bin_Values[15][4][2] = 9011;
    z_pT_Bin_Borders[15][5][0] = 0.33; z_pT_Bin_Borders[15][5][1] = 0.28; z_pT_Bin_Borders[15][5][2] = 0.33; z_pT_Bin_Borders[15][5][3] = 0.23;
    Phi_h_Bin_Values[15][5][0] =  24; Phi_h_Bin_Values[15][5][1] = 96; Phi_h_Bin_Values[15][5][2] = 9035;
    z_pT_Bin_Borders[15][6][0] = 0.33; z_pT_Bin_Borders[15][6][1] = 0.28; z_pT_Bin_Borders[15][6][2] = 0.47; z_pT_Bin_Borders[15][6][3] = 0.33;
    Phi_h_Bin_Values[15][6][0] =  24; Phi_h_Bin_Values[15][6][1] = 120; Phi_h_Bin_Values[15][6][2] = 9059;
    z_pT_Bin_Borders[15][7][0] = 0.4; z_pT_Bin_Borders[15][7][1] = 0.33; z_pT_Bin_Borders[15][7][2] = 0.23; z_pT_Bin_Borders[15][7][3] = 0.05;
    Phi_h_Bin_Values[15][7][0] =  24; Phi_h_Bin_Values[15][7][1] = 144; Phi_h_Bin_Values[15][7][2] = 9083;
    z_pT_Bin_Borders[15][8][0] = 0.4; z_pT_Bin_Borders[15][8][1] = 0.33; z_pT_Bin_Borders[15][8][2] = 0.33; z_pT_Bin_Borders[15][8][3] = 0.23;
    Phi_h_Bin_Values[15][8][0] =  24; Phi_h_Bin_Values[15][8][1] = 168; Phi_h_Bin_Values[15][8][2] = 9107;
    z_pT_Bin_Borders[15][9][0] = 0.4; z_pT_Bin_Borders[15][9][1] = 0.33; z_pT_Bin_Borders[15][9][2] = 0.47; z_pT_Bin_Borders[15][9][3] = 0.33;
    Phi_h_Bin_Values[15][9][0] =  24; Phi_h_Bin_Values[15][9][1] = 192; Phi_h_Bin_Values[15][9][2] = 9131;
    z_pT_Bin_Borders[15][10][0] = 0.51; z_pT_Bin_Borders[15][10][1] = 0.4; z_pT_Bin_Borders[15][10][2] = 0.23; z_pT_Bin_Borders[15][10][3] = 0.05;
    Phi_h_Bin_Values[15][10][0] =  24; Phi_h_Bin_Values[15][10][1] = 216; Phi_h_Bin_Values[15][10][2] = 9155;
    z_pT_Bin_Borders[15][11][0] = 0.51; z_pT_Bin_Borders[15][11][1] = 0.4; z_pT_Bin_Borders[15][11][2] = 0.33; z_pT_Bin_Borders[15][11][3] = 0.23;
    Phi_h_Bin_Values[15][11][0] =  24; Phi_h_Bin_Values[15][11][1] = 240; Phi_h_Bin_Values[15][11][2] = 9179;
    z_pT_Bin_Borders[15][12][0] = 0.51; z_pT_Bin_Borders[15][12][1] = 0.4; z_pT_Bin_Borders[15][12][2] = 0.47; z_pT_Bin_Borders[15][12][3] = 0.33;
    Phi_h_Bin_Values[15][12][0] =  1; Phi_h_Bin_Values[15][12][1] = 264; Phi_h_Bin_Values[15][12][2] = 9203;
    z_pT_Bin_Borders[15][13][0] = 0.22; z_pT_Bin_Borders[15][13][1] = 0; z_pT_Bin_Borders[15][13][2] = 0.05; z_pT_Bin_Borders[15][13][3] = 0;
    Phi_h_Bin_Values[15][13][0] =  1; Phi_h_Bin_Values[15][13][1] = 265; Phi_h_Bin_Values[15][13][2] = 9204;
    z_pT_Bin_Borders[15][14][0] = 0.22; z_pT_Bin_Borders[15][14][1] = 0; z_pT_Bin_Borders[15][14][2] = 0.05; z_pT_Bin_Borders[15][14][3] = 0.23;
    Phi_h_Bin_Values[15][14][0] =  1; Phi_h_Bin_Values[15][14][1] = 266; Phi_h_Bin_Values[15][14][2] = 9205;
    z_pT_Bin_Borders[15][15][0] = 0.22; z_pT_Bin_Borders[15][15][1] = 0; z_pT_Bin_Borders[15][15][2] = 0.23; z_pT_Bin_Borders[15][15][3] = 0.33;
    Phi_h_Bin_Values[15][15][0] =  1; Phi_h_Bin_Values[15][15][1] = 267; Phi_h_Bin_Values[15][15][2] = 9206;
    z_pT_Bin_Borders[15][16][0] = 0.22; z_pT_Bin_Borders[15][16][1] = 0; z_pT_Bin_Borders[15][16][2] = 0.33; z_pT_Bin_Borders[15][16][3] = 0.47;
    Phi_h_Bin_Values[15][16][0] =  1; Phi_h_Bin_Values[15][16][1] = 268; Phi_h_Bin_Values[15][16][2] = 9207;
    z_pT_Bin_Borders[15][17][0] = 0.22; z_pT_Bin_Borders[15][17][1] = 0; z_pT_Bin_Borders[15][17][2] = 10; z_pT_Bin_Borders[15][17][3] = 0.47;
    Phi_h_Bin_Values[15][17][0] =  1; Phi_h_Bin_Values[15][17][1] = 269; Phi_h_Bin_Values[15][17][2] = 9208;
    z_pT_Bin_Borders[15][18][0] = 0.22; z_pT_Bin_Borders[15][18][1] = 0.28; z_pT_Bin_Borders[15][18][2] = 0.05; z_pT_Bin_Borders[15][18][3] = 0;
    Phi_h_Bin_Values[15][18][0] =  1; Phi_h_Bin_Values[15][18][1] = 270; Phi_h_Bin_Values[15][18][2] = 9209;
    z_pT_Bin_Borders[15][19][0] = 0.22; z_pT_Bin_Borders[15][19][1] = 0.28; z_pT_Bin_Borders[15][19][2] = 10; z_pT_Bin_Borders[15][19][3] = 0.47;
    Phi_h_Bin_Values[15][19][0] =  1; Phi_h_Bin_Values[15][19][1] = 271; Phi_h_Bin_Values[15][19][2] = 9210;
    z_pT_Bin_Borders[15][20][0] = 0.28; z_pT_Bin_Borders[15][20][1] = 0.33; z_pT_Bin_Borders[15][20][2] = 0.05; z_pT_Bin_Borders[15][20][3] = 0;
    Phi_h_Bin_Values[15][20][0] =  1; Phi_h_Bin_Values[15][20][1] = 272; Phi_h_Bin_Values[15][20][2] = 9211;
    z_pT_Bin_Borders[15][21][0] = 0.28; z_pT_Bin_Borders[15][21][1] = 0.33; z_pT_Bin_Borders[15][21][2] = 10; z_pT_Bin_Borders[15][21][3] = 0.47;
    Phi_h_Bin_Values[15][21][0] =  1; Phi_h_Bin_Values[15][21][1] = 273; Phi_h_Bin_Values[15][21][2] = 9212;
    z_pT_Bin_Borders[15][22][0] = 0.33; z_pT_Bin_Borders[15][22][1] = 0.4; z_pT_Bin_Borders[15][22][2] = 0.05; z_pT_Bin_Borders[15][22][3] = 0;
    Phi_h_Bin_Values[15][22][0] =  1; Phi_h_Bin_Values[15][22][1] = 274; Phi_h_Bin_Values[15][22][2] = 9213;
    z_pT_Bin_Borders[15][23][0] = 0.33; z_pT_Bin_Borders[15][23][1] = 0.4; z_pT_Bin_Borders[15][23][2] = 10; z_pT_Bin_Borders[15][23][3] = 0.47;
    Phi_h_Bin_Values[15][23][0] =  1; Phi_h_Bin_Values[15][23][1] = 275; Phi_h_Bin_Values[15][23][2] = 9214;
    z_pT_Bin_Borders[15][24][0] = 0.4; z_pT_Bin_Borders[15][24][1] = 0.51; z_pT_Bin_Borders[15][24][2] = 0.05; z_pT_Bin_Borders[15][24][3] = 0;
    Phi_h_Bin_Values[15][24][0] =  1; Phi_h_Bin_Values[15][24][1] = 276; Phi_h_Bin_Values[15][24][2] = 9215;
    z_pT_Bin_Borders[15][25][0] = 0.4; z_pT_Bin_Borders[15][25][1] = 0.51; z_pT_Bin_Borders[15][25][2] = 10; z_pT_Bin_Borders[15][25][3] = 0.47;
    Phi_h_Bin_Values[15][25][0] =  1; Phi_h_Bin_Values[15][25][1] = 277; Phi_h_Bin_Values[15][25][2] = 9216;
    z_pT_Bin_Borders[15][26][0] = 10; z_pT_Bin_Borders[15][26][1] = 0.51; z_pT_Bin_Borders[15][26][2] = 0; z_pT_Bin_Borders[15][26][3] = 0.05;
    Phi_h_Bin_Values[15][26][0] =  1; Phi_h_Bin_Values[15][26][1] = 278; Phi_h_Bin_Values[15][26][2] = 9217;
    z_pT_Bin_Borders[15][27][0] = 10; z_pT_Bin_Borders[15][27][1] = 0.51; z_pT_Bin_Borders[15][27][2] = 0.05; z_pT_Bin_Borders[15][27][3] = 0.23;
    Phi_h_Bin_Values[15][27][0] =  1; Phi_h_Bin_Values[15][27][1] = 279; Phi_h_Bin_Values[15][27][2] = 9218;
    z_pT_Bin_Borders[15][28][0] = 10; z_pT_Bin_Borders[15][28][1] = 0.51; z_pT_Bin_Borders[15][28][2] = 0.23; z_pT_Bin_Borders[15][28][3] = 0.33;
    Phi_h_Bin_Values[15][28][0] =  1; Phi_h_Bin_Values[15][28][1] = 280; Phi_h_Bin_Values[15][28][2] = 9219;
    z_pT_Bin_Borders[15][29][0] = 10; z_pT_Bin_Borders[15][29][1] = 0.51; z_pT_Bin_Borders[15][29][2] = 0.33; z_pT_Bin_Borders[15][29][3] = 0.47;
    Phi_h_Bin_Values[15][29][0] =  1; Phi_h_Bin_Values[15][29][1] = 281; Phi_h_Bin_Values[15][29][2] = 9220;
    z_pT_Bin_Borders[15][30][0] = 10; z_pT_Bin_Borders[15][30][1] = 0.51; z_pT_Bin_Borders[15][30][2] = 10; z_pT_Bin_Borders[15][30][3] = 0.47;
    Phi_h_Bin_Values[15][30][0] =  1; Phi_h_Bin_Values[15][30][1] = 282; Phi_h_Bin_Values[15][30][2] = 9221;
    z_pT_Bin_Borders[16][1][0] = 0.2; z_pT_Bin_Borders[16][1][1] = 0.16; z_pT_Bin_Borders[16][1][2] = 0.22; z_pT_Bin_Borders[16][1][3] = 0.05;
    Phi_h_Bin_Values[16][1][0] =  24; Phi_h_Bin_Values[16][1][1] = 0; Phi_h_Bin_Values[16][1][2] = 9222;
    z_pT_Bin_Borders[16][2][0] = 0.2; z_pT_Bin_Borders[16][2][1] = 0.16; z_pT_Bin_Borders[16][2][2] = 0.31; z_pT_Bin_Borders[16][2][3] = 0.22;
    Phi_h_Bin_Values[16][2][0] =  24; Phi_h_Bin_Values[16][2][1] = 24; Phi_h_Bin_Values[16][2][2] = 9246;
    z_pT_Bin_Borders[16][3][0] = 0.2; z_pT_Bin_Borders[16][3][1] = 0.16; z_pT_Bin_Borders[16][3][2] = 0.44; z_pT_Bin_Borders[16][3][3] = 0.31;
    Phi_h_Bin_Values[16][3][0] =  24; Phi_h_Bin_Values[16][3][1] = 48; Phi_h_Bin_Values[16][3][2] = 9270;
    z_pT_Bin_Borders[16][4][0] = 0.2; z_pT_Bin_Borders[16][4][1] = 0.16; z_pT_Bin_Borders[16][4][2] = 0.7; z_pT_Bin_Borders[16][4][3] = 0.44;
    Phi_h_Bin_Values[16][4][0] =  1; Phi_h_Bin_Values[16][4][1] = 72; Phi_h_Bin_Values[16][4][2] = 9294;
    z_pT_Bin_Borders[16][5][0] = 0.24; z_pT_Bin_Borders[16][5][1] = 0.2; z_pT_Bin_Borders[16][5][2] = 0.22; z_pT_Bin_Borders[16][5][3] = 0.05;
    Phi_h_Bin_Values[16][5][0] =  24; Phi_h_Bin_Values[16][5][1] = 73; Phi_h_Bin_Values[16][5][2] = 9295;
    z_pT_Bin_Borders[16][6][0] = 0.24; z_pT_Bin_Borders[16][6][1] = 0.2; z_pT_Bin_Borders[16][6][2] = 0.31; z_pT_Bin_Borders[16][6][3] = 0.22;
    Phi_h_Bin_Values[16][6][0] =  24; Phi_h_Bin_Values[16][6][1] = 97; Phi_h_Bin_Values[16][6][2] = 9319;
    z_pT_Bin_Borders[16][7][0] = 0.24; z_pT_Bin_Borders[16][7][1] = 0.2; z_pT_Bin_Borders[16][7][2] = 0.44; z_pT_Bin_Borders[16][7][3] = 0.31;
    Phi_h_Bin_Values[16][7][0] =  24; Phi_h_Bin_Values[16][7][1] = 121; Phi_h_Bin_Values[16][7][2] = 9343;
    z_pT_Bin_Borders[16][8][0] = 0.24; z_pT_Bin_Borders[16][8][1] = 0.2; z_pT_Bin_Borders[16][8][2] = 0.7; z_pT_Bin_Borders[16][8][3] = 0.44;
    Phi_h_Bin_Values[16][8][0] =  1; Phi_h_Bin_Values[16][8][1] = 145; Phi_h_Bin_Values[16][8][2] = 9367;
    z_pT_Bin_Borders[16][9][0] = 0.29; z_pT_Bin_Borders[16][9][1] = 0.24; z_pT_Bin_Borders[16][9][2] = 0.22; z_pT_Bin_Borders[16][9][3] = 0.05;
    Phi_h_Bin_Values[16][9][0] =  24; Phi_h_Bin_Values[16][9][1] = 146; Phi_h_Bin_Values[16][9][2] = 9368;
    z_pT_Bin_Borders[16][10][0] = 0.29; z_pT_Bin_Borders[16][10][1] = 0.24; z_pT_Bin_Borders[16][10][2] = 0.31; z_pT_Bin_Borders[16][10][3] = 0.22;
    Phi_h_Bin_Values[16][10][0] =  24; Phi_h_Bin_Values[16][10][1] = 170; Phi_h_Bin_Values[16][10][2] = 9392;
    z_pT_Bin_Borders[16][11][0] = 0.29; z_pT_Bin_Borders[16][11][1] = 0.24; z_pT_Bin_Borders[16][11][2] = 0.44; z_pT_Bin_Borders[16][11][3] = 0.31;
    Phi_h_Bin_Values[16][11][0] =  24; Phi_h_Bin_Values[16][11][1] = 194; Phi_h_Bin_Values[16][11][2] = 9416;
    z_pT_Bin_Borders[16][12][0] = 0.29; z_pT_Bin_Borders[16][12][1] = 0.24; z_pT_Bin_Borders[16][12][2] = 0.7; z_pT_Bin_Borders[16][12][3] = 0.44;
    Phi_h_Bin_Values[16][12][0] =  24; Phi_h_Bin_Values[16][12][1] = 218; Phi_h_Bin_Values[16][12][2] = 9440;
    z_pT_Bin_Borders[16][13][0] = 0.36; z_pT_Bin_Borders[16][13][1] = 0.29; z_pT_Bin_Borders[16][13][2] = 0.22; z_pT_Bin_Borders[16][13][3] = 0.05;
    Phi_h_Bin_Values[16][13][0] =  24; Phi_h_Bin_Values[16][13][1] = 242; Phi_h_Bin_Values[16][13][2] = 9464;
    z_pT_Bin_Borders[16][14][0] = 0.36; z_pT_Bin_Borders[16][14][1] = 0.29; z_pT_Bin_Borders[16][14][2] = 0.31; z_pT_Bin_Borders[16][14][3] = 0.22;
    Phi_h_Bin_Values[16][14][0] =  24; Phi_h_Bin_Values[16][14][1] = 266; Phi_h_Bin_Values[16][14][2] = 9488;
    z_pT_Bin_Borders[16][15][0] = 0.36; z_pT_Bin_Borders[16][15][1] = 0.29; z_pT_Bin_Borders[16][15][2] = 0.44; z_pT_Bin_Borders[16][15][3] = 0.31;
    Phi_h_Bin_Values[16][15][0] =  24; Phi_h_Bin_Values[16][15][1] = 290; Phi_h_Bin_Values[16][15][2] = 9512;
    z_pT_Bin_Borders[16][16][0] = 0.36; z_pT_Bin_Borders[16][16][1] = 0.29; z_pT_Bin_Borders[16][16][2] = 0.7; z_pT_Bin_Borders[16][16][3] = 0.44;
    Phi_h_Bin_Values[16][16][0] =  24; Phi_h_Bin_Values[16][16][1] = 314; Phi_h_Bin_Values[16][16][2] = 9536;
    z_pT_Bin_Borders[16][17][0] = 0.45; z_pT_Bin_Borders[16][17][1] = 0.36; z_pT_Bin_Borders[16][17][2] = 0.22; z_pT_Bin_Borders[16][17][3] = 0.05;
    Phi_h_Bin_Values[16][17][0] =  24; Phi_h_Bin_Values[16][17][1] = 338; Phi_h_Bin_Values[16][17][2] = 9560;
    z_pT_Bin_Borders[16][18][0] = 0.45; z_pT_Bin_Borders[16][18][1] = 0.36; z_pT_Bin_Borders[16][18][2] = 0.31; z_pT_Bin_Borders[16][18][3] = 0.22;
    Phi_h_Bin_Values[16][18][0] =  24; Phi_h_Bin_Values[16][18][1] = 362; Phi_h_Bin_Values[16][18][2] = 9584;
    z_pT_Bin_Borders[16][19][0] = 0.45; z_pT_Bin_Borders[16][19][1] = 0.36; z_pT_Bin_Borders[16][19][2] = 0.44; z_pT_Bin_Borders[16][19][3] = 0.31;
    Phi_h_Bin_Values[16][19][0] =  24; Phi_h_Bin_Values[16][19][1] = 386; Phi_h_Bin_Values[16][19][2] = 9608;
    z_pT_Bin_Borders[16][20][0] = 0.45; z_pT_Bin_Borders[16][20][1] = 0.36; z_pT_Bin_Borders[16][20][2] = 0.7; z_pT_Bin_Borders[16][20][3] = 0.44;
    Phi_h_Bin_Values[16][20][0] =  24; Phi_h_Bin_Values[16][20][1] = 410; Phi_h_Bin_Values[16][20][2] = 9632;
    z_pT_Bin_Borders[16][21][0] = 0.62; z_pT_Bin_Borders[16][21][1] = 0.45; z_pT_Bin_Borders[16][21][2] = 0.22; z_pT_Bin_Borders[16][21][3] = 0.05;
    Phi_h_Bin_Values[16][21][0] =  24; Phi_h_Bin_Values[16][21][1] = 434; Phi_h_Bin_Values[16][21][2] = 9656;
    z_pT_Bin_Borders[16][22][0] = 0.62; z_pT_Bin_Borders[16][22][1] = 0.45; z_pT_Bin_Borders[16][22][2] = 0.31; z_pT_Bin_Borders[16][22][3] = 0.22;
    Phi_h_Bin_Values[16][22][0] =  24; Phi_h_Bin_Values[16][22][1] = 458; Phi_h_Bin_Values[16][22][2] = 9680;
    z_pT_Bin_Borders[16][23][0] = 0.62; z_pT_Bin_Borders[16][23][1] = 0.45; z_pT_Bin_Borders[16][23][2] = 0.44; z_pT_Bin_Borders[16][23][3] = 0.31;
    Phi_h_Bin_Values[16][23][0] =  24; Phi_h_Bin_Values[16][23][1] = 482; Phi_h_Bin_Values[16][23][2] = 9704;
    z_pT_Bin_Borders[16][24][0] = 0.62; z_pT_Bin_Borders[16][24][1] = 0.45; z_pT_Bin_Borders[16][24][2] = 0.7; z_pT_Bin_Borders[16][24][3] = 0.44;
    Phi_h_Bin_Values[16][24][0] =  1; Phi_h_Bin_Values[16][24][1] = 506; Phi_h_Bin_Values[16][24][2] = 9728;
    z_pT_Bin_Borders[16][25][0] = 0.16; z_pT_Bin_Borders[16][25][1] = 0; z_pT_Bin_Borders[16][25][2] = 0.05; z_pT_Bin_Borders[16][25][3] = 0;
    Phi_h_Bin_Values[16][25][0] =  1; Phi_h_Bin_Values[16][25][1] = 507; Phi_h_Bin_Values[16][25][2] = 9729;
    z_pT_Bin_Borders[16][26][0] = 0.16; z_pT_Bin_Borders[16][26][1] = 0; z_pT_Bin_Borders[16][26][2] = 0.05; z_pT_Bin_Borders[16][26][3] = 0.22;
    Phi_h_Bin_Values[16][26][0] =  1; Phi_h_Bin_Values[16][26][1] = 508; Phi_h_Bin_Values[16][26][2] = 9730;
    z_pT_Bin_Borders[16][27][0] = 0.16; z_pT_Bin_Borders[16][27][1] = 0; z_pT_Bin_Borders[16][27][2] = 0.22; z_pT_Bin_Borders[16][27][3] = 0.31;
    Phi_h_Bin_Values[16][27][0] =  1; Phi_h_Bin_Values[16][27][1] = 509; Phi_h_Bin_Values[16][27][2] = 9731;
    z_pT_Bin_Borders[16][28][0] = 0.16; z_pT_Bin_Borders[16][28][1] = 0; z_pT_Bin_Borders[16][28][2] = 0.31; z_pT_Bin_Borders[16][28][3] = 0.44;
    Phi_h_Bin_Values[16][28][0] =  1; Phi_h_Bin_Values[16][28][1] = 510; Phi_h_Bin_Values[16][28][2] = 9732;
    z_pT_Bin_Borders[16][29][0] = 0.16; z_pT_Bin_Borders[16][29][1] = 0; z_pT_Bin_Borders[16][29][2] = 0.44; z_pT_Bin_Borders[16][29][3] = 0.7;
    Phi_h_Bin_Values[16][29][0] =  1; Phi_h_Bin_Values[16][29][1] = 511; Phi_h_Bin_Values[16][29][2] = 9733;
    z_pT_Bin_Borders[16][30][0] = 0.16; z_pT_Bin_Borders[16][30][1] = 0; z_pT_Bin_Borders[16][30][2] = 10; z_pT_Bin_Borders[16][30][3] = 0.7;
    Phi_h_Bin_Values[16][30][0] =  1; Phi_h_Bin_Values[16][30][1] = 512; Phi_h_Bin_Values[16][30][2] = 9734;
    z_pT_Bin_Borders[16][31][0] = 0.16; z_pT_Bin_Borders[16][31][1] = 0.2; z_pT_Bin_Borders[16][31][2] = 0.05; z_pT_Bin_Borders[16][31][3] = 0;
    Phi_h_Bin_Values[16][31][0] =  1; Phi_h_Bin_Values[16][31][1] = 513; Phi_h_Bin_Values[16][31][2] = 9735;
    z_pT_Bin_Borders[16][32][0] = 0.16; z_pT_Bin_Borders[16][32][1] = 0.2; z_pT_Bin_Borders[16][32][2] = 10; z_pT_Bin_Borders[16][32][3] = 0.7;
    Phi_h_Bin_Values[16][32][0] =  1; Phi_h_Bin_Values[16][32][1] = 514; Phi_h_Bin_Values[16][32][2] = 9736;
    z_pT_Bin_Borders[16][33][0] = 0.2; z_pT_Bin_Borders[16][33][1] = 0.24; z_pT_Bin_Borders[16][33][2] = 0.05; z_pT_Bin_Borders[16][33][3] = 0;
    Phi_h_Bin_Values[16][33][0] =  1; Phi_h_Bin_Values[16][33][1] = 515; Phi_h_Bin_Values[16][33][2] = 9737;
    z_pT_Bin_Borders[16][34][0] = 0.2; z_pT_Bin_Borders[16][34][1] = 0.24; z_pT_Bin_Borders[16][34][2] = 10; z_pT_Bin_Borders[16][34][3] = 0.7;
    Phi_h_Bin_Values[16][34][0] =  1; Phi_h_Bin_Values[16][34][1] = 516; Phi_h_Bin_Values[16][34][2] = 9738;
    z_pT_Bin_Borders[16][35][0] = 0.24; z_pT_Bin_Borders[16][35][1] = 0.29; z_pT_Bin_Borders[16][35][2] = 0.05; z_pT_Bin_Borders[16][35][3] = 0;
    Phi_h_Bin_Values[16][35][0] =  1; Phi_h_Bin_Values[16][35][1] = 517; Phi_h_Bin_Values[16][35][2] = 9739;
    z_pT_Bin_Borders[16][36][0] = 0.24; z_pT_Bin_Borders[16][36][1] = 0.29; z_pT_Bin_Borders[16][36][2] = 10; z_pT_Bin_Borders[16][36][3] = 0.7;
    Phi_h_Bin_Values[16][36][0] =  1; Phi_h_Bin_Values[16][36][1] = 518; Phi_h_Bin_Values[16][36][2] = 9740;
    z_pT_Bin_Borders[16][37][0] = 0.29; z_pT_Bin_Borders[16][37][1] = 0.36; z_pT_Bin_Borders[16][37][2] = 0.05; z_pT_Bin_Borders[16][37][3] = 0;
    Phi_h_Bin_Values[16][37][0] =  1; Phi_h_Bin_Values[16][37][1] = 519; Phi_h_Bin_Values[16][37][2] = 9741;
    z_pT_Bin_Borders[16][38][0] = 0.29; z_pT_Bin_Borders[16][38][1] = 0.36; z_pT_Bin_Borders[16][38][2] = 10; z_pT_Bin_Borders[16][38][3] = 0.7;
    Phi_h_Bin_Values[16][38][0] =  1; Phi_h_Bin_Values[16][38][1] = 520; Phi_h_Bin_Values[16][38][2] = 9742;
    z_pT_Bin_Borders[16][39][0] = 0.36; z_pT_Bin_Borders[16][39][1] = 0.45; z_pT_Bin_Borders[16][39][2] = 0.05; z_pT_Bin_Borders[16][39][3] = 0;
    Phi_h_Bin_Values[16][39][0] =  1; Phi_h_Bin_Values[16][39][1] = 521; Phi_h_Bin_Values[16][39][2] = 9743;
    z_pT_Bin_Borders[16][40][0] = 0.36; z_pT_Bin_Borders[16][40][1] = 0.45; z_pT_Bin_Borders[16][40][2] = 10; z_pT_Bin_Borders[16][40][3] = 0.7;
    Phi_h_Bin_Values[16][40][0] =  1; Phi_h_Bin_Values[16][40][1] = 522; Phi_h_Bin_Values[16][40][2] = 9744;
    z_pT_Bin_Borders[16][41][0] = 0.45; z_pT_Bin_Borders[16][41][1] = 0.62; z_pT_Bin_Borders[16][41][2] = 0.05; z_pT_Bin_Borders[16][41][3] = 0;
    Phi_h_Bin_Values[16][41][0] =  1; Phi_h_Bin_Values[16][41][1] = 523; Phi_h_Bin_Values[16][41][2] = 9745;
    z_pT_Bin_Borders[16][42][0] = 0.45; z_pT_Bin_Borders[16][42][1] = 0.62; z_pT_Bin_Borders[16][42][2] = 10; z_pT_Bin_Borders[16][42][3] = 0.7;
    Phi_h_Bin_Values[16][42][0] =  1; Phi_h_Bin_Values[16][42][1] = 524; Phi_h_Bin_Values[16][42][2] = 9746;
    z_pT_Bin_Borders[16][43][0] = 10; z_pT_Bin_Borders[16][43][1] = 0.62; z_pT_Bin_Borders[16][43][2] = 0; z_pT_Bin_Borders[16][43][3] = 0.05;
    Phi_h_Bin_Values[16][43][0] =  1; Phi_h_Bin_Values[16][43][1] = 525; Phi_h_Bin_Values[16][43][2] = 9747;
    z_pT_Bin_Borders[16][44][0] = 10; z_pT_Bin_Borders[16][44][1] = 0.62; z_pT_Bin_Borders[16][44][2] = 0.05; z_pT_Bin_Borders[16][44][3] = 0.22;
    Phi_h_Bin_Values[16][44][0] =  1; Phi_h_Bin_Values[16][44][1] = 526; Phi_h_Bin_Values[16][44][2] = 9748;
    z_pT_Bin_Borders[16][45][0] = 10; z_pT_Bin_Borders[16][45][1] = 0.62; z_pT_Bin_Borders[16][45][2] = 0.22; z_pT_Bin_Borders[16][45][3] = 0.31;
    Phi_h_Bin_Values[16][45][0] =  1; Phi_h_Bin_Values[16][45][1] = 527; Phi_h_Bin_Values[16][45][2] = 9749;
    z_pT_Bin_Borders[16][46][0] = 10; z_pT_Bin_Borders[16][46][1] = 0.62; z_pT_Bin_Borders[16][46][2] = 0.31; z_pT_Bin_Borders[16][46][3] = 0.44;
    Phi_h_Bin_Values[16][46][0] =  1; Phi_h_Bin_Values[16][46][1] = 528; Phi_h_Bin_Values[16][46][2] = 9750;
    z_pT_Bin_Borders[16][47][0] = 10; z_pT_Bin_Borders[16][47][1] = 0.62; z_pT_Bin_Borders[16][47][2] = 0.44; z_pT_Bin_Borders[16][47][3] = 0.7;
    Phi_h_Bin_Values[16][47][0] =  1; Phi_h_Bin_Values[16][47][1] = 529; Phi_h_Bin_Values[16][47][2] = 9751;
    z_pT_Bin_Borders[16][48][0] = 10; z_pT_Bin_Borders[16][48][1] = 0.62; z_pT_Bin_Borders[16][48][2] = 10; z_pT_Bin_Borders[16][48][3] = 0.7;
    Phi_h_Bin_Values[16][48][0] =  1; Phi_h_Bin_Values[16][48][1] = 530; Phi_h_Bin_Values[16][48][2] = 9752;
    z_pT_Bin_Borders[17][1][0] = 0.23; z_pT_Bin_Borders[17][1][1] = 0.19; z_pT_Bin_Borders[17][1][2] = 0.19; z_pT_Bin_Borders[17][1][3] = 0.05;
    Phi_h_Bin_Values[17][1][0] =  24; Phi_h_Bin_Values[17][1][1] = 0; Phi_h_Bin_Values[17][1][2] = 9753;
    z_pT_Bin_Borders[17][2][0] = 0.23; z_pT_Bin_Borders[17][2][1] = 0.19; z_pT_Bin_Borders[17][2][2] = 0.28; z_pT_Bin_Borders[17][2][3] = 0.19;
    Phi_h_Bin_Values[17][2][0] =  24; Phi_h_Bin_Values[17][2][1] = 24; Phi_h_Bin_Values[17][2][2] = 9777;
    z_pT_Bin_Borders[17][3][0] = 0.23; z_pT_Bin_Borders[17][3][1] = 0.19; z_pT_Bin_Borders[17][3][2] = 0.37; z_pT_Bin_Borders[17][3][3] = 0.28;
    Phi_h_Bin_Values[17][3][0] =  24; Phi_h_Bin_Values[17][3][1] = 48; Phi_h_Bin_Values[17][3][2] = 9801;
    z_pT_Bin_Borders[17][4][0] = 0.29; z_pT_Bin_Borders[17][4][1] = 0.23; z_pT_Bin_Borders[17][4][2] = 0.19; z_pT_Bin_Borders[17][4][3] = 0.05;
    Phi_h_Bin_Values[17][4][0] =  24; Phi_h_Bin_Values[17][4][1] = 72; Phi_h_Bin_Values[17][4][2] = 9825;
    z_pT_Bin_Borders[17][5][0] = 0.29; z_pT_Bin_Borders[17][5][1] = 0.23; z_pT_Bin_Borders[17][5][2] = 0.28; z_pT_Bin_Borders[17][5][3] = 0.19;
    Phi_h_Bin_Values[17][5][0] =  24; Phi_h_Bin_Values[17][5][1] = 96; Phi_h_Bin_Values[17][5][2] = 9849;
    z_pT_Bin_Borders[17][6][0] = 0.29; z_pT_Bin_Borders[17][6][1] = 0.23; z_pT_Bin_Borders[17][6][2] = 0.37; z_pT_Bin_Borders[17][6][3] = 0.28;
    Phi_h_Bin_Values[17][6][0] =  24; Phi_h_Bin_Values[17][6][1] = 120; Phi_h_Bin_Values[17][6][2] = 9873;
    z_pT_Bin_Borders[17][7][0] = 0.35; z_pT_Bin_Borders[17][7][1] = 0.29; z_pT_Bin_Borders[17][7][2] = 0.19; z_pT_Bin_Borders[17][7][3] = 0.05;
    Phi_h_Bin_Values[17][7][0] =  24; Phi_h_Bin_Values[17][7][1] = 144; Phi_h_Bin_Values[17][7][2] = 9897;
    z_pT_Bin_Borders[17][8][0] = 0.35; z_pT_Bin_Borders[17][8][1] = 0.29; z_pT_Bin_Borders[17][8][2] = 0.28; z_pT_Bin_Borders[17][8][3] = 0.19;
    Phi_h_Bin_Values[17][8][0] =  24; Phi_h_Bin_Values[17][8][1] = 168; Phi_h_Bin_Values[17][8][2] = 9921;
    z_pT_Bin_Borders[17][9][0] = 0.35; z_pT_Bin_Borders[17][9][1] = 0.29; z_pT_Bin_Borders[17][9][2] = 0.37; z_pT_Bin_Borders[17][9][3] = 0.28;
    Phi_h_Bin_Values[17][9][0] =  24; Phi_h_Bin_Values[17][9][1] = 192; Phi_h_Bin_Values[17][9][2] = 9945;
    z_pT_Bin_Borders[17][10][0] = 0.45; z_pT_Bin_Borders[17][10][1] = 0.35; z_pT_Bin_Borders[17][10][2] = 0.19; z_pT_Bin_Borders[17][10][3] = 0.05;
    Phi_h_Bin_Values[17][10][0] =  24; Phi_h_Bin_Values[17][10][1] = 216; Phi_h_Bin_Values[17][10][2] = 9969;
    z_pT_Bin_Borders[17][11][0] = 0.45; z_pT_Bin_Borders[17][11][1] = 0.35; z_pT_Bin_Borders[17][11][2] = 0.28; z_pT_Bin_Borders[17][11][3] = 0.19;
    Phi_h_Bin_Values[17][11][0] =  1; Phi_h_Bin_Values[17][11][1] = 240; Phi_h_Bin_Values[17][11][2] = 9993;
    z_pT_Bin_Borders[17][12][0] = 0.45; z_pT_Bin_Borders[17][12][1] = 0.35; z_pT_Bin_Borders[17][12][2] = 0.37; z_pT_Bin_Borders[17][12][3] = 0.28;
    Phi_h_Bin_Values[17][12][0] =  1; Phi_h_Bin_Values[17][12][1] = 241; Phi_h_Bin_Values[17][12][2] = 9994;
    z_pT_Bin_Borders[17][13][0] = 0.19; z_pT_Bin_Borders[17][13][1] = 0; z_pT_Bin_Borders[17][13][2] = 0.05; z_pT_Bin_Borders[17][13][3] = 0;
    Phi_h_Bin_Values[17][13][0] =  1; Phi_h_Bin_Values[17][13][1] = 242; Phi_h_Bin_Values[17][13][2] = 9995;
    z_pT_Bin_Borders[17][14][0] = 0.19; z_pT_Bin_Borders[17][14][1] = 0; z_pT_Bin_Borders[17][14][2] = 0.05; z_pT_Bin_Borders[17][14][3] = 0.19;
    Phi_h_Bin_Values[17][14][0] =  1; Phi_h_Bin_Values[17][14][1] = 243; Phi_h_Bin_Values[17][14][2] = 9996;
    z_pT_Bin_Borders[17][15][0] = 0.19; z_pT_Bin_Borders[17][15][1] = 0; z_pT_Bin_Borders[17][15][2] = 0.19; z_pT_Bin_Borders[17][15][3] = 0.28;
    Phi_h_Bin_Values[17][15][0] =  1; Phi_h_Bin_Values[17][15][1] = 244; Phi_h_Bin_Values[17][15][2] = 9997;
    z_pT_Bin_Borders[17][16][0] = 0.19; z_pT_Bin_Borders[17][16][1] = 0; z_pT_Bin_Borders[17][16][2] = 0.28; z_pT_Bin_Borders[17][16][3] = 0.37;
    Phi_h_Bin_Values[17][16][0] =  1; Phi_h_Bin_Values[17][16][1] = 245; Phi_h_Bin_Values[17][16][2] = 9998;
    z_pT_Bin_Borders[17][17][0] = 0.19; z_pT_Bin_Borders[17][17][1] = 0; z_pT_Bin_Borders[17][17][2] = 10; z_pT_Bin_Borders[17][17][3] = 0.37;
    Phi_h_Bin_Values[17][17][0] =  1; Phi_h_Bin_Values[17][17][1] = 246; Phi_h_Bin_Values[17][17][2] = 9999;
    z_pT_Bin_Borders[17][18][0] = 0.19; z_pT_Bin_Borders[17][18][1] = 0.23; z_pT_Bin_Borders[17][18][2] = 0.05; z_pT_Bin_Borders[17][18][3] = 0;
    Phi_h_Bin_Values[17][18][0] =  1; Phi_h_Bin_Values[17][18][1] = 247; Phi_h_Bin_Values[17][18][2] = 10000;
    z_pT_Bin_Borders[17][19][0] = 0.19; z_pT_Bin_Borders[17][19][1] = 0.23; z_pT_Bin_Borders[17][19][2] = 10; z_pT_Bin_Borders[17][19][3] = 0.37;
    Phi_h_Bin_Values[17][19][0] =  1; Phi_h_Bin_Values[17][19][1] = 248; Phi_h_Bin_Values[17][19][2] = 10001;
    z_pT_Bin_Borders[17][20][0] = 0.23; z_pT_Bin_Borders[17][20][1] = 0.29; z_pT_Bin_Borders[17][20][2] = 0.05; z_pT_Bin_Borders[17][20][3] = 0;
    Phi_h_Bin_Values[17][20][0] =  1; Phi_h_Bin_Values[17][20][1] = 249; Phi_h_Bin_Values[17][20][2] = 10002;
    z_pT_Bin_Borders[17][21][0] = 0.23; z_pT_Bin_Borders[17][21][1] = 0.29; z_pT_Bin_Borders[17][21][2] = 10; z_pT_Bin_Borders[17][21][3] = 0.37;
    Phi_h_Bin_Values[17][21][0] =  1; Phi_h_Bin_Values[17][21][1] = 250; Phi_h_Bin_Values[17][21][2] = 10003;
    z_pT_Bin_Borders[17][22][0] = 0.29; z_pT_Bin_Borders[17][22][1] = 0.35; z_pT_Bin_Borders[17][22][2] = 0.05; z_pT_Bin_Borders[17][22][3] = 0;
    Phi_h_Bin_Values[17][22][0] =  1; Phi_h_Bin_Values[17][22][1] = 251; Phi_h_Bin_Values[17][22][2] = 10004;
    z_pT_Bin_Borders[17][23][0] = 0.29; z_pT_Bin_Borders[17][23][1] = 0.35; z_pT_Bin_Borders[17][23][2] = 10; z_pT_Bin_Borders[17][23][3] = 0.37;
    Phi_h_Bin_Values[17][23][0] =  1; Phi_h_Bin_Values[17][23][1] = 252; Phi_h_Bin_Values[17][23][2] = 10005;
    z_pT_Bin_Borders[17][24][0] = 0.35; z_pT_Bin_Borders[17][24][1] = 0.45; z_pT_Bin_Borders[17][24][2] = 0.05; z_pT_Bin_Borders[17][24][3] = 0;
    Phi_h_Bin_Values[17][24][0] =  1; Phi_h_Bin_Values[17][24][1] = 253; Phi_h_Bin_Values[17][24][2] = 10006;
    z_pT_Bin_Borders[17][25][0] = 0.35; z_pT_Bin_Borders[17][25][1] = 0.45; z_pT_Bin_Borders[17][25][2] = 10; z_pT_Bin_Borders[17][25][3] = 0.37;
    Phi_h_Bin_Values[17][25][0] =  1; Phi_h_Bin_Values[17][25][1] = 254; Phi_h_Bin_Values[17][25][2] = 10007;
    z_pT_Bin_Borders[17][26][0] = 10; z_pT_Bin_Borders[17][26][1] = 0.45; z_pT_Bin_Borders[17][26][2] = 0; z_pT_Bin_Borders[17][26][3] = 0.05;
    Phi_h_Bin_Values[17][26][0] =  1; Phi_h_Bin_Values[17][26][1] = 255; Phi_h_Bin_Values[17][26][2] = 10008;
    z_pT_Bin_Borders[17][27][0] = 10; z_pT_Bin_Borders[17][27][1] = 0.45; z_pT_Bin_Borders[17][27][2] = 0.05; z_pT_Bin_Borders[17][27][3] = 0.19;
    Phi_h_Bin_Values[17][27][0] =  1; Phi_h_Bin_Values[17][27][1] = 256; Phi_h_Bin_Values[17][27][2] = 10009;
    z_pT_Bin_Borders[17][28][0] = 10; z_pT_Bin_Borders[17][28][1] = 0.45; z_pT_Bin_Borders[17][28][2] = 0.19; z_pT_Bin_Borders[17][28][3] = 0.28;
    Phi_h_Bin_Values[17][28][0] =  1; Phi_h_Bin_Values[17][28][1] = 257; Phi_h_Bin_Values[17][28][2] = 10010;
    z_pT_Bin_Borders[17][29][0] = 10; z_pT_Bin_Borders[17][29][1] = 0.45; z_pT_Bin_Borders[17][29][2] = 0.28; z_pT_Bin_Borders[17][29][3] = 0.37;
    Phi_h_Bin_Values[17][29][0] =  1; Phi_h_Bin_Values[17][29][1] = 258; Phi_h_Bin_Values[17][29][2] = 10011;
    z_pT_Bin_Borders[17][30][0] = 10; z_pT_Bin_Borders[17][30][1] = 0.45; z_pT_Bin_Borders[17][30][2] = 10; z_pT_Bin_Borders[17][30][3] = 0.37;
    Phi_h_Bin_Values[17][30][0] =  1; Phi_h_Bin_Values[17][30][1] = 259; Phi_h_Bin_Values[17][30][2] = 10012;
    Phi_h_Bin_Values[18][1][0] = 1; Phi_h_Bin_Values[18][1][1] = 1; Phi_h_Bin_Values[18][1][2] = 10013;
    Phi_h_Bin_Values[19][1][0] = 1; Phi_h_Bin_Values[19][1][1] = 1; Phi_h_Bin_Values[19][1][2] = 10014;
    Phi_h_Bin_Values[20][1][0] = 1; Phi_h_Bin_Values[20][1][1] = 1; Phi_h_Bin_Values[20][1][2] = 10015;
    Phi_h_Bin_Values[21][1][0] = 1; Phi_h_Bin_Values[21][1][1] = 1; Phi_h_Bin_Values[21][1][2] = 10016;
    Phi_h_Bin_Values[22][1][0] = 1; Phi_h_Bin_Values[22][1][1] = 1; Phi_h_Bin_Values[22][1][2] = 10017;
    Phi_h_Bin_Values[23][1][0] = 1; Phi_h_Bin_Values[23][1][1] = 1; Phi_h_Bin_Values[23][1][2] = 10018;
    Phi_h_Bin_Values[24][1][0] = 1; Phi_h_Bin_Values[24][1][1] = 1; Phi_h_Bin_Values[24][1][2] = 10019;
    Phi_h_Bin_Values[25][1][0] = 1; Phi_h_Bin_Values[25][1][1] = 1; Phi_h_Bin_Values[25][1][2] = 10020;
    Phi_h_Bin_Values[26][1][0] = 1; Phi_h_Bin_Values[26][1][1] = 1; Phi_h_Bin_Values[26][1][2] = 10021;
    Phi_h_Bin_Values[27][1][0] = 1; Phi_h_Bin_Values[27][1][1] = 1; Phi_h_Bin_Values[27][1][2] = 10022;
    Phi_h_Bin_Values[28][1][0] = 1; Phi_h_Bin_Values[28][1][1] = 1; Phi_h_Bin_Values[28][1][2] = 10023;
    Phi_h_Bin_Values[29][1][0] = 1; Phi_h_Bin_Values[29][1][1] = 1; Phi_h_Bin_Values[29][1][2] = 10024;
    Phi_h_Bin_Values[30][1][0] = 1; Phi_h_Bin_Values[30][1][1] = 1; Phi_h_Bin_Values[30][1][2] = 10025;
    Phi_h_Bin_Values[31][1][0] = 1; Phi_h_Bin_Values[31][1][1] = 1; Phi_h_Bin_Values[31][1][2] = 10026;
    Phi_h_Bin_Values[32][1][0] = 1; Phi_h_Bin_Values[32][1][1] = 1; Phi_h_Bin_Values[32][1][2] = 10027;
    Phi_h_Bin_Values[33][1][0] = 1; Phi_h_Bin_Values[33][1][1] = 1; Phi_h_Bin_Values[33][1][2] = 10028;
    Phi_h_Bin_Values[34][1][0] = 1; Phi_h_Bin_Values[34][1][1] = 1; Phi_h_Bin_Values[34][1][2] = 10029;
    Phi_h_Bin_Values[35][1][0] = 1; Phi_h_Bin_Values[35][1][1] = 1; Phi_h_Bin_Values[35][1][2] = 10030;
    Phi_h_Bin_Values[36][1][0] = 1; Phi_h_Bin_Values[36][1][1] = 1; Phi_h_Bin_Values[36][1][2] = 10031;
    Phi_h_Bin_Values[37][1][0] = 1; Phi_h_Bin_Values[37][1][1] = 1; Phi_h_Bin_Values[37][1][2] = 10032;
    Phi_h_Bin_Values[38][1][0] = 1; Phi_h_Bin_Values[38][1][1] = 1; Phi_h_Bin_Values[38][1][2] = 10033;
    Phi_h_Bin_Values[39][1][0] = 1; Phi_h_Bin_Values[39][1][1] = 1; Phi_h_Bin_Values[39][1][2] = 10034;
    auto Find_z_pT_Bin = [&](int Q2_y_Bin_Num_Value, double Z_Value, double PT_Value){
        int z_pT_Bin_Max = 1;
        if(Q2_y_Bin_Num_Value == 1){z_pT_Bin_Max = 63;}
        if(Q2_y_Bin_Num_Value == 2){z_pT_Bin_Max = 64;}
        if(Q2_y_Bin_Num_Value == 3){z_pT_Bin_Max = 48;}
        if(Q2_y_Bin_Num_Value == 4){z_pT_Bin_Max = 49;}
        if(Q2_y_Bin_Num_Value == 5){z_pT_Bin_Max = 64;}
        if(Q2_y_Bin_Num_Value == 6){z_pT_Bin_Max = 56;}
        if(Q2_y_Bin_Num_Value == 7){z_pT_Bin_Max = 56;}
        if(Q2_y_Bin_Num_Value == 8){z_pT_Bin_Max = 48;}
        if(Q2_y_Bin_Num_Value == 9){z_pT_Bin_Max = 63;}
        if(Q2_y_Bin_Num_Value == 10){z_pT_Bin_Max = 64;}
        if(Q2_y_Bin_Num_Value == 11){z_pT_Bin_Max = 49;}
        if(Q2_y_Bin_Num_Value == 12){z_pT_Bin_Max = 30;}
        if(Q2_y_Bin_Num_Value == 13){z_pT_Bin_Max = 56;}
        if(Q2_y_Bin_Num_Value == 14){z_pT_Bin_Max = 64;}
        if(Q2_y_Bin_Num_Value == 15){z_pT_Bin_Max = 30;}
        if(Q2_y_Bin_Num_Value == 16){z_pT_Bin_Max = 48;}
        if(Q2_y_Bin_Num_Value == 17){z_pT_Bin_Max = 30;}
        if(Q2_y_Bin_Num_Value < 1 || Q2_y_Bin_Num_Value > 17){return 1;}
        float z_max  = 0;
        float z_min  = 0;
        float pT_max = 0;
        float pT_min = 0;
        for(int Z_PT_BIN = 1; Z_PT_BIN < (z_pT_Bin_Max + 1); Z_PT_BIN++){
            z_max  = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][0];
            z_min  = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][1];
            pT_max = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][2];
            pT_min = z_pT_Bin_Borders[Q2_y_Bin_Num_Value][Z_PT_BIN][3];
            if(((Z_Value <= z_max) && (Z_Value > z_min)) && ((PT_Value <= pT_max) && (PT_Value > pT_min))){
                return Z_PT_BIN;
                break;
            }
        }
        return 0; // ERROR: Events should not return 0 (missed all bin definitions)
    };
    auto Find_phi_h_Bin = [&](int Q2_y_Bin_Num_Value, int Z_PT_Bin_Num_Value, double PHI_H_Value){
        int Num_PHI_BINS = Phi_h_Bin_Values[Q2_y_Bin_Num_Value][Z_PT_Bin_Num_Value][0];
        if(Num_PHI_BINS <= 1){return Num_PHI_BINS;}
        else{
            double bin_size = 360/Num_PHI_BINS;
            int PHI_BIN     = (PHI_H_Value/bin_size) + 1;
            if(PHI_H_Value == 360){PHI_BIN = Num_PHI_BINS;} // Include 360 in the last phi_h bin
            return PHI_BIN;
        }
        return -1; // ERROR: Events should not return -1
    };
    """
        
    Correction_Code_Full_In = """
    auto dppC = [&](float Px, float Py, float Pz, int sec, int ivec, int corON){
    
        // corON == 0 --> DOES NOT apply the momentum corrections (i.e., turns the corrections 'off')
        // corON == 1 --> Applies the momentum corrections for the experimental (real) data
        // corON == 2 --> Applies the momentum corrections for the Monte Carlo (simulated) data

        if(corON == 0){ // Momentum Corrections are OFF
            double dp = 0;
            return dp;
        }

        else{ // corON != 0 --> Applies the momentum corrections (i.e., turns the corrections 'on')
            // ivec = 0 --> Electron Corrections
            // ivec = 1 --> π+ Corrections
            // ivec = 2 --> π- Corrections
            // ivec = 3 --> Proton Corrections

            // Momentum Magnitude
            double pp = sqrt(Px*Px + Py*Py + Pz*Pz);

            // Initializing the correction factor
            double dp = 0;

            // Defining Phi Angle
            double Phi = (180/3.1415926)*atan2(Py, Px);

            // (Initial) Shift of the Phi Angle (done to realign sectors whose data is separated when plotted from ±180˚)
            if(((sec == 4 || sec == 3) && Phi < 0) || (sec > 4 && Phi < 90)){
                Phi += 360;
            }

            // Getting Local Phi Angle
            double PhiLocal = Phi - (sec - 1)*60;

            // Applying Shift Functions to Phi Angles (local shifted phi = phi)
            double phi = PhiLocal;

            // For Electron Shift
            if(ivec == 0){
                phi = PhiLocal - 30/pp;
            }

            // For π+ Pion/Proton Shift
            if(ivec == 1 || ivec == 3){
                phi = PhiLocal + (32/(pp-0.05));
            }

            // For π- Pion Shift
            if(ivec == 2){
                phi = PhiLocal - (32/(pp-0.05));
            }

            if(corON == 2){ // Monte Carlo Simulated Corrections
                // Not Sector or Angle dependent (as of 3-21-2023)
                
                // Both particles were corrected at the same time using Extra_Name = "Multi_Dimension_Unfold_V1_"
                // Used ∆P = GEN - REC so the other particle does not affect how much the correction is needed
                if(ivec == 0){ // Electron Corrections
                    // // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
                    // dp = (-8.2310e-04)*pp*pp + (9.0877e-03)*pp + (-1.5853e-02);
                    
                    // From Normal ∆P corrections:
                    // For MC REC (Unsmeared) ∆P(Electron) Vs Momentum Correction Equation:
                    dp = (-6.9141e-04)*pp*pp + (5.5852e-03)*pp + (-5.2144e-03);
                    // Corrected after the pion
                    
                }
                if(ivec == 1){ // Pi+ Pion Corrections
                    // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
                    dp = (-7.3067e-05)*pp*pp + (-8.1215e-06)*pp + (4.2144e-03);
                    
                    // From Normal ∆P corrections:
                    // For MC REC (Unsmeared) ∆P(Pi+ Pion) Vs Momentum Correction Equation:
                    dp = (-1.8752e-03)*pp*pp + (1.0679e-02)*pp +  (2.5653e-03);
                    // Corrected before the electron
                    
                    // Cannot use iterative corrections as of 7-8-2023 due to the corrections being applied automatically so that dp is no longer a function of the same pp
                    // dp = dp + (-1.8949e-03)*pp*pp + (9.3060e-03)*pp + (-9.7925e-03);
                }
            
                return dp/pp;
            }
            else{
        
                //////////////////////////////////////////////////////////////////////////////////
                //==============================================================================//
                //==========//==========//     Electron Corrections     //==========//==========//
                //==============================================================================//
                //////////////////////////////////////////////////////////////////////////////////

                if(ivec == 0){
                    if(sec == 1){
                        dp = ((-4.3303e-06)*phi*phi +  (1.1006e-04)*phi + (-5.7235e-04))*pp*pp +  ((3.2555e-05)*phi*phi +  (-0.0014559)*phi +   (0.0014878))*pp + ((-1.9577e-05)*phi*phi +   (0.0017996)*phi + (0.025963));
                    }
                    if(sec == 2){
                        dp = ((-9.8045e-07)*phi*phi +  (6.7395e-05)*phi + (-4.6757e-05))*pp*pp + ((-1.4958e-05)*phi*phi +  (-0.0011191)*phi +  (-0.0025143))*pp +  ((1.2699e-04)*phi*phi +   (0.0033121)*phi + (0.020819));
                    }
                    if(sec == 3){
                        dp = ((-5.9459e-07)*phi*phi + (-2.8289e-05)*phi + (-4.3541e-04))*pp*pp + ((-1.5025e-05)*phi*phi +  (5.7730e-04)*phi +  (-0.0077582))*pp +  ((7.3348e-05)*phi*phi +   (-0.001102)*phi + (0.057052));
                    }
                    if(sec == 4){
                        dp = ((-2.2714e-06)*phi*phi + (-3.0360e-05)*phi + (-8.9322e-04))*pp*pp +  ((2.9737e-05)*phi*phi +  (5.1142e-04)*phi +   (0.0045641))*pp + ((-1.0582e-04)*phi*phi + (-5.6852e-04)*phi + (0.027506));
                    }
                    if(sec == 5){
                        dp = ((-1.1490e-06)*phi*phi + (-6.2147e-06)*phi + (-4.7235e-04))*pp*pp +  ((3.7039e-06)*phi*phi + (-1.5943e-04)*phi + (-8.5238e-04))*pp +  ((4.4069e-05)*phi*phi +   (0.0014152)*phi + (0.031933));
                    }
                    if(sec == 6){
                        dp =  ((1.1076e-06)*phi*phi +  (4.0156e-05)*phi + (-1.6341e-04))*pp*pp + ((-2.8613e-05)*phi*phi + (-5.1861e-04)*phi +  (-0.0056437))*pp +  ((1.2419e-04)*phi*phi +  (4.9084e-04)*phi + (0.049976));
                    }
                }

                //////////////////////////////////////////////////////////////////////////////////
                //==============================================================================//
                //==========//==========//  Electron Corrections (End)  //==========//==========//
                //==============================================================================//
                //////////////////////////////////////////////////////////////////////////////////


                /////////////////////////////////////////////////////////////////////////////////
                //=============================================================================//
                //==========//==========//     π+ Pion Corrections     //==========//==========//
                //=============================================================================//
                /////////////////////////////////////////////////////////////////////////////////

                if(ivec == 1){
                    if(sec == 1){
                        dp =      ((-5.4904e-07)*phi*phi + (-1.4436e-05)*phi +  (3.1534e-04))*pp*pp +  ((3.8231e-06)*phi*phi +  (3.6582e-04)*phi +  (-0.0046759))*pp + ((-5.4913e-06)*phi*phi + (-4.0157e-04)*phi + (0.010767));
                        dp = dp +  ((6.1103e-07)*phi*phi +  (5.5291e-06)*phi + (-1.9120e-04))*pp*pp + ((-3.2300e-06)*phi*phi +  (1.5377e-05)*phi +  (7.5279e-04))*pp +  ((2.1434e-06)*phi*phi + (-6.9572e-06)*phi + (-7.9333e-05));
                        dp = dp + ((-1.3049e-06)*phi*phi +  (1.1295e-05)*phi +  (4.5797e-04))*pp*pp +  ((9.3122e-06)*phi*phi + (-5.1074e-05)*phi +  (-0.0030757))*pp + ((-1.3102e-05)*phi*phi +  (2.2153e-05)*phi + (0.0040938));
                    }
                    if(sec == 2){
                        dp =      ((-1.0087e-06)*phi*phi +  (2.1319e-05)*phi +  (7.8641e-04))*pp*pp +  ((6.7485e-06)*phi*phi +  (7.3716e-05)*phi +  (-0.0094591))*pp + ((-1.1820e-05)*phi*phi + (-3.8103e-04)*phi + (0.018936));
                        dp = dp +  ((8.8155e-07)*phi*phi + (-2.8257e-06)*phi + (-2.6729e-04))*pp*pp + ((-5.4499e-06)*phi*phi +  (3.8397e-05)*phi +   (0.0015914))*pp +  ((6.8926e-06)*phi*phi + (-5.9386e-05)*phi + (-0.0021749));
                        dp = dp + ((-2.0147e-07)*phi*phi +  (1.1061e-05)*phi +  (3.8827e-04))*pp*pp +  ((4.9294e-07)*phi*phi + (-6.0257e-05)*phi +  (-0.0022087))*pp +  ((9.8548e-07)*phi*phi +  (5.9047e-05)*phi + (0.0022905));
                    }
                    if(sec == 3){
                        dp =       ((8.6722e-08)*phi*phi + (-1.7975e-05)*phi +  (4.8118e-05))*pp*pp +  ((2.6273e-06)*phi*phi +  (3.1453e-05)*phi +  (-0.0015943))*pp + ((-6.4463e-06)*phi*phi + (-5.8990e-05)*phi + (0.0041703));
                        dp = dp +  ((9.6317e-07)*phi*phi + (-1.7659e-06)*phi + (-8.8318e-05))*pp*pp + ((-5.1346e-06)*phi*phi +  (8.3318e-06)*phi +  (3.7723e-04))*pp +  ((3.9548e-06)*phi*phi + (-6.9614e-05)*phi + (2.1393e-04));
                        dp = dp +  ((5.6438e-07)*phi*phi +  (8.1678e-06)*phi + (-9.4406e-05))*pp*pp + ((-3.9074e-06)*phi*phi + (-6.5174e-05)*phi +  (5.4218e-04))*pp +  ((6.3198e-06)*phi*phi +  (1.0611e-04)*phi + (-4.5749e-04));
                    }
                    if(sec == 4){
                        dp =       ((4.3406e-07)*phi*phi + (-4.9036e-06)*phi +  (2.3064e-04))*pp*pp +  ((1.3624e-06)*phi*phi +  (3.2907e-05)*phi +  (-0.0034872))*pp + ((-5.1017e-06)*phi*phi +  (2.4593e-05)*phi + (0.0092479));
                        dp = dp +  ((6.0218e-07)*phi*phi + (-1.4383e-05)*phi + (-3.1999e-05))*pp*pp + ((-1.1243e-06)*phi*phi +  (9.3884e-05)*phi + (-4.1985e-04))*pp + ((-1.8808e-06)*phi*phi + (-1.2222e-04)*phi + (0.0014037));
                        dp = dp + ((-2.5490e-07)*phi*phi + (-8.5120e-07)*phi +  (7.9109e-05))*pp*pp +  ((2.5879e-06)*phi*phi +  (8.6108e-06)*phi + (-5.1533e-04))*pp + ((-4.4521e-06)*phi*phi + (-1.7012e-05)*phi + (7.4848e-04));
                    }
                    if(sec == 5){
                        dp =       ((2.4292e-07)*phi*phi +  (8.8741e-06)*phi +  (2.9482e-04))*pp*pp +  ((3.7229e-06)*phi*phi +  (7.3215e-06)*phi +  (-0.0050685))*pp + ((-1.1974e-05)*phi*phi + (-1.3043e-04)*phi + (0.0078836));
                        dp = dp +  ((1.0867e-06)*phi*phi + (-7.7630e-07)*phi + (-4.4930e-05))*pp*pp + ((-5.6564e-06)*phi*phi + (-1.3417e-05)*phi +  (2.5224e-04))*pp +  ((6.8460e-06)*phi*phi +  (9.0495e-05)*phi + (-4.6587e-04));
                        dp = dp +  ((8.5720e-07)*phi*phi + (-6.7464e-06)*phi + (-4.0944e-05))*pp*pp + ((-4.7370e-06)*phi*phi +  (5.8808e-05)*phi +  (1.9047e-04))*pp +  ((5.7404e-06)*phi*phi + (-1.1105e-04)*phi + (-1.9392e-04));
                    }
                    if(sec == 6){
                        dp =       ((2.1191e-06)*phi*phi + (-3.3710e-05)*phi +  (2.5741e-04))*pp*pp + ((-1.2915e-05)*phi*phi +  (2.3753e-04)*phi + (-2.6882e-04))*pp +  ((2.2676e-05)*phi*phi + (-2.3115e-04)*phi + (-0.001283));
                        dp = dp +  ((6.0270e-07)*phi*phi + (-6.8200e-06)*phi +  (1.3103e-04))*pp*pp + ((-1.8745e-06)*phi*phi +  (3.8646e-05)*phi + (-8.8056e-04))*pp +  ((2.0885e-06)*phi*phi + (-3.4932e-05)*phi + (4.5895e-04));
                        dp = dp +  ((4.7349e-08)*phi*phi + (-5.7528e-06)*phi + (-3.4097e-06))*pp*pp +  ((1.7731e-06)*phi*phi +  (3.5865e-05)*phi + (-5.7881e-04))*pp + ((-9.7008e-06)*phi*phi + (-4.1836e-05)*phi + (0.0035403));
                    }
                }

                /////////////////////////////////////////////////////////////////////////////////
                //=============================================================================//
                //==========//==========//  π+ Pion Corrections (End)  //==========//==========//
                //=============================================================================//
                /////////////////////////////////////////////////////////////////////////////////
                
                
                /////////////////////////////////////////////////////////////////////////////////
                //=============================================================================//
                //==========//==========//     π- Pion Corrections     //==========//==========//
                //=============================================================================//
                /////////////////////////////////////////////////////////////////////////////////

                if(ivec == 2){
                    if(sec == 1){
                        dp = ((-4.0192658422317425e-06)*phi*phi - (2.660222128967742e-05)*phi + 0.004774434682983547)*pp*pp;
                        dp = dp + ((1.9549520962477972e-05)*phi*phi - 0.0002456062756770577*phi - 0.03787692408323466)*pp; 
                        dp = dp + (-2.128953094937459e-05)*phi*phi + 0.0002461708852239913*phi + 0.08060704449822174 - 0.01;
                    }
                    if(sec == 2){
                        dp = ((1.193010521758372e-05)*phi*phi - (5.996221756031922e-05)*phi + 0.0009093437955814359)*pp*pp;
                        dp = dp + ((-4.89113824430594e-05)*phi*phi + 0.00021676479488147118*phi - 0.01861892053916726)*pp;  
                        dp = dp + (4.446394152208071e-05)*phi*phi - (3.6592784167335244e-05)*phi + 0.05498710249944096 - 0.01;
                    }
                    if(sec == 3){
                        dp = ((-1.6596664895992133e-07)*phi*phi + (6.317189710683516e-05)*phi + 0.0016364212312654086)*pp*pp;
                        dp = dp + ((-2.898409777520318e-07)*phi*phi - 0.00014531513577533802*phi - 0.025456145839203827)*pp;  
                        dp = dp + (2.6432552410603506e-06)*phi*phi + 0.00018447151306275443*phi + 0.06442602664627255 - 0.01;
                    }
                    if(sec == 4){
                        dp = ((2.4035259647558634e-07)*phi*phi - (8.649647351491232e-06)*phi + 0.004558993439848128)*pp*pp;
                        dp = dp + ((-5.981498144060984e-06)*phi*phi + 0.00010582131454222416*phi - 0.033572004651981686)*pp;  
                        dp = dp + (8.70140266889548e-06)*phi*phi - 0.00020137414379966883*phi + 0.07258774523336173 - 0.01;   
                    }
                    if(sec == 5){
                        dp = ((2.5817024702834863e-06)*phi*phi + 0.00010132810066914441*phi + 0.003397314538804711)*pp*pp;
                        dp = dp + ((-1.5116941263931812e-05)*phi*phi - 0.00040679799541839254*phi - 0.028144285760769876)*pp;  
                        dp = dp + (1.4701931057951464e-05)*phi*phi + 0.0002426350390593454*phi + 0.06781682510174941 - 0.01;
                    }
                    if(sec == 6){
                        dp = ((-8.196823669099362e-07)*phi*phi - (5.280412421933636e-05)*phi + 0.0018457238328451137)*pp*pp;
                        dp = dp + ((5.2675062282094536e-06)*phi*phi + 0.0001515803461044587*phi - 0.02294371578470564)*pp;  
                        dp = dp + (-9.459454671739747e-06)*phi*phi - 0.0002389523716779765*phi + 0.06428970810739926 - 0.01;
                    }
                }

                /////////////////////////////////////////////////////////////////////////////////
                //=============================================================================//
                //==========//==========//  π- Pion Corrections (End)  //==========//==========//
                //=============================================================================//
                /////////////////////////////////////////////////////////////////////////////////
                
                
                //////////////////////////////////////////////////////////////////////////////////
                //==============================================================================//
                //==========//==========//      Proton Corrections      //==========//==========//
                //==============================================================================//
                //////////////////////////////////////////////////////////////////////////////////

                if(ivec == 3){
                    if(sec == 1){
                        dp = (5.415e-04)*pp*pp + (-1.0262e-02)*pp + (7.78075e-03);
                        dp = dp + ((1.2129e-04)*pp*pp + (1.5373e-04)*pp + (-2.7084e-04));
                    }
                    if(sec == 2){
                        dp = (-9.5439e-04)*pp*pp + (-2.86273e-03)*pp + (3.38149e-03);
                        dp = dp + ((-1.6890e-03)*pp*pp + (4.3744e-03)*pp + (-2.1218e-03));
                    }
                    if(sec == 3){
                        dp = (-5.5541e-04)*pp*pp + (-7.69739e-03)*pp + (5.7692e-03);
                        dp = dp + ((7.6422e-04)*pp*pp + (-1.5425e-03)*pp + (5.4255e-04));
                    }
                    if(sec == 4){
                        dp = (-1.944e-04)*pp*pp + (-5.77104e-03)*pp + (3.42399e-03);
                        dp = dp + ((1.1174e-03)*pp*pp + (-3.2747e-03)*pp + (2.3687e-03));
                    }
                    if(sec == 5){
                        dp = (1.54009e-03)*pp*pp + (-1.69437e-02)*pp + (1.04656e-02);
                        dp = dp + ((-2.1067e-04)*pp*pp + (1.2266e-03)*pp + (-1.0553e-03));
                    }
                    if(sec == 6){
                        dp = (2.38182e-03)*pp*pp + (-2.07301e-02)*pp + (1.72325e-02);
                        dp = dp + ((-3.6002e-04)*pp*pp + (8.9582e-04)*pp + (-1.0093e-03));
                    }
                }

                //////////////////////////////////////////////////////////////////////////////////
                //==============================================================================//
                //==========//==========//   Proton Corrections (End)   //==========//==========//
                //==============================================================================//
                //////////////////////////////////////////////////////////////////////////////////

                return dp/pp;
            }
        }
    };"""
    
    if(Mom_Correction_Q != "yes"):
        print("".join([color.BOLD, color.RED,  "\n\tNot running with Momentum Corrections\n", color.END]))
    else:
        print("".join([color.BOLD, color.BLUE, "\n\tRunning with Momentum Corrections\n",     color.END]))
        
        
    ###################################################################################################################################################################
    #################################################################   End of Momentum Corrections   #################################################################
    ###----------##----------##----------##----------##----------##-------------------------------------##----------##----------##----------##----------##----------###
    ################################################################# Calculating Kinematic Variables #################################################################
    ###################################################################################################################################################################
    
    
    ######################################################################################
    ##=====##  These calculations may have been made in the groovy code already  ##=====##
    ######################################################################################
    
    
    ##=====## The following is for backwards compatibility ##=====##
    if("pipx" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipx", "px")
    if("pipy" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipy", "py")
    if("pipz" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipz", "pz")
    
    if('calc' not in files_used_for_data_frame):
        #####################     Energy     #####################
        try:
            rdf = rdf.Define("el_E", "".join([str(Correction_Code_Full_In), """
            auto fe    = dppC(ex, ey, ez, esec, 0, """,          "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
            auto ele   = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
            auto ele_E = ele.E();
            return ele_E;"""]))

            rdf = rdf.Define("pip_E", "".join([str(Correction_Code_Full_In), """
            auto fpip   = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
            auto pip0   = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
            auto pip0_E = pip0.E();
            return pip0_E;"""]))
            
        except:
            print("\nMomentum Corrections Failed...\n")
            rdf = rdf.Define("el_E", """
            auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto ele_E = ele.E();
            return ele_E;""")
            rdf = rdf.Define("pip_E", """
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
            auto pip0_E = pip0.E();
            return pip0_E;""")

        
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("el_E_gen", """
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto ele_E_gen = ele.E();
            return ele_E_gen;""")

            rdf = rdf.Define("pip_E_gen", """
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
            auto pip0_E_gen = pip0.E();
            return pip0_E_gen;""")
            
        
        #####################     Momentum     #####################

        try:
            rdf = rdf.Define("el", "".join([str(Correction_Code_Full_In), """
            auto fe     = dppC(ex, ey, ez, esec, 0, """,          "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
            double el_P = fe*(sqrt(ex*ex + ey*ey + ez*ez));
            return el_P;"""]))
            rdf = rdf.Define("pip", "".join([str(Correction_Code_Full_In), """
            auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
            double pip_P = fpip*(sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
            return pip_P;"""]))
            if((run_Mom_Cor_Code == "yes") and (str(datatype) not in ["gdf"])):
                rdf = rdf.Define("el_no_cor",  """
                double el_P_no_cor  = (sqrt(ex*ex + ey*ey + ez*ez));
                return el_P_no_cor;""")
                rdf = rdf.Define("pip_no_cor", """
                double pip_P_no_cor = (sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
                return pip_P_no_cor;""")  
        except:
            print(color.BOLD, color.RED, "\n\nMomentum Corrections Failed...\n\n", color.END)
            rdf = rdf.Define("el",  "sqrt(ex*ex + ey*ey + ez*ez)")
            rdf = rdf.Define("pip", "sqrt(pipx*pipx + pipy*pipy + pipz*pipz)")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("el_gen",  "sqrt(ex_gen*ex_gen + ey_gen*ey_gen + ez_gen*ez_gen)")
            rdf = rdf.Define("pip_gen", "sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen + pipz_gen*pipz_gen)")

        #####################     Theta Angle     #####################

        rdf = rdf.Define("elth",  "atan2(sqrt(ex*ex + ey*ey), ez)*TMath::RadToDeg()")
        rdf = rdf.Define("pipth", "atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*TMath::RadToDeg()")
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

#         rdf = rdf.Define("esec_a", """
#         auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
#         auto ele_phi = (180/3.1415926)*ele.Phi();
#         int esec_a = 0;
#         if(ele_phi >= -30 && ele_phi < 30){
#             esec_a = 1;
#         }
#         if(ele_phi >= 30 && ele_phi < 90){
#             esec_a = 2;
#         }
#         if(ele_phi >= 90 && ele_phi < 150){
#             esec_a = 3;
#         }
#         if(ele_phi >= 150 || ele_phi < -150){
#             esec_a = 4;
#         }
#         if(ele_phi >= -90 && ele_phi < -30){
#             esec_a = 5;
#         }
#         if(ele_phi >= -150 && ele_phi < -90){
#             esec_a = 6;
#         }
#         return esec_a;""")
#         rdf = rdf.Define("pipsec_a", """
#         auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
#         auto pip_phi = (180/3.1415926)*pip0.Phi();
#         int pipsec_a = 0;
#         if(pip_phi >= -45 && pip_phi < 15){
#             pipsec_a = 1;
#         }
#         if(pip_phi >= 15 && pip_phi < 75){
#             pipsec_a = 2;
#         }
#         if(pip_phi >= 75 && pip_phi < 135){
#             pipsec_a = 3;
#         }
#         if(pip_phi >= 135 || pip_phi < -165){
#             pipsec_a = 4;
#         }
#         if(pip_phi >= -105 && pip_phi < -45){
#             pipsec_a = 5;
#         }
#         if(pip_phi >= -165 && pip_phi < -105){
#             pipsec_a = 6;
#         }
#         return pipsec_a;""")
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

        rdf = rdf.Define("vals", "".join([str(Correction_Code_Full_In), """
        auto fe      = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        
        auto beam    = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
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
        
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("vals_gen","""
            auto beam_gen    = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
            auto targ_gen    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
            auto ele_gen     = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto pip0_gen    = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);

            auto epipX_gen   = beam_gen + targ_gen - ele_gen - pip0_gen;
            auto q_gen       = beam_gen - ele_gen;
            auto Q2_gen      = - q_gen.M2();
            auto v_gen       = beam_gen.E() - ele_gen.E();
            auto xB_gen      = Q2_gen/(2*targ_gen.M()*v_gen);
            auto W2_gen      = targ_gen.M2() + 2*targ_gen.M()*v_gen - Q2_gen;
            auto W_gen       = sqrt(W2_gen);
            auto y_gen       = (targ_gen.Dot(q_gen))/(targ_gen.Dot(beam_gen));
            auto z_gen       = ((pip0_gen.E())/(q_gen.E()));
            auto gamma_gen   = 2*targ_gen.M()*(xB_gen/sqrt(Q2_gen));
            auto epsilon_gen = (1 - y_gen - 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen))/(1 - y_gen + 0.5*(y_gen*y_gen) + 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen));

            std::vector<double> vals_gen = {epipX_gen.M(), epipX_gen.M2(), Q2_gen, xB_gen, v_gen, W2_gen, W_gen, y_gen, z_gen, epsilon_gen};

            return vals_gen;""")

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
        
    
    ##############################################################################
    ##=====##  The above calculations used to be run in the groovy code  ##=====##
    ##############################################################################
    
    
    
    ####################################################################################################################################################################
    ###################################################     Done with Calculating (Initial) Kinematic Variables      ###################################################
    ###----------##----------##----------##----------##--------------------------------------------------------------##----------##----------##----------##----------###
    ###################################################       Rotation Matrix and Center-of-Mass/Boosted Frame       ###################################################
    ####################################################################################################################################################################
    
    Rotation_Matrix = """
    /////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////
    
    auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot){
        double Rot_X1 = vector.X();
        double Rot_Y1 = vector.Y();
        double Rot_Z1 = vector.Z();

        double Rot_X = Rot_X1;
        double Rot_Y = Rot_Y1;
        double Rot_Z = Rot_Z1;

        // Lab2CM_or_CM2Lab is a parameter which determines if you rotating from the lab frame to the CM frame, or if you are rotating back in the opposite direction
        // Lab2CM_or_CM2Lab = -1 gives a rotation to the CM frame (from the lab frame)
        // Lab2CM_or_CM2Lab = +1 gives a rotation to the lab frame (from the CM frame)

        Theta_Rot = -1*Theta_Rot;   // Always give the angle of rotation Theta as the value given by .Theta()
                                    // This subroutine will handle the fact that the matrix rotation wants the negative of the angle of rotation

        // Rotation to Lab Frame
        if(Lab2CM_or_CM2Lab == -1){
            Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) - Rot_Z1*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Cos(Theta_Rot)*TMath::Sin(Phi_Rot);
            Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) - Rot_X1*TMath::Sin(Phi_Rot);
            Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) + Rot_X1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
        }

        // Rotation to CM Frame
        if(Lab2CM_or_CM2Lab == 1){
            Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) + Rot_Z1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) - Rot_Y1*TMath::Sin(Phi_Rot);
            Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) + Rot_X1*TMath::Sin(Phi_Rot)*TMath::Cos(Theta_Rot) + Rot_Z1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
            Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) - Rot_X1*TMath::Sin(Theta_Rot);
        }

        TLorentzVector vector_Rotated(Rot_X, Rot_Y, Rot_Z, vector.E());

        return vector_Rotated;

    };

    /////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////"""
    
    rdf = rdf.Define("vals2", "".join([str(Correction_Code_Full_In), """
    auto fe     = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
    auto fpip   = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
    
    auto beamM  = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
    auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0,       0.938272);
    
    auto eleM   = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
    auto pip0M  = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
    
    auto lv_qMM = beamM - eleM;

    TLorentzVector beam(0, 0, 10.6041, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());
    
    TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
    TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
    
    TLorentzVector lv_q = beam - ele;

    ///////////////     Angles for Rotation     ///////////////
    double Theta_q = lv_q.Theta();
    double Phi_el  = ele.Phi();

    """, str(Rotation_Matrix), """

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
    
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define("vals2_gen", "".join(["""
        auto beamM  = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto eleM   = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
        auto pip0M  = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
        auto lv_qMM = beamM - eleM;

        TLorentzVector beam(0, 0, 10.6041, beamM.E());
        TLorentzVector targ(0, 0, 0, targM.E());
        TLorentzVector ele(ex_gen, ey_gen, ez_gen, eleM.E());
        TLorentzVector pip0(pipx_gen, pipy_gen, pipz_gen, pip0M.E());
        TLorentzVector lv_q = beam - ele;

        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el  = ele.Phi();

        """, str(Rotation_Matrix), """

        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);

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
    
#     smearing_function = """
#         //===========================================================================//
#         //=================//     Smearing Function (From FX)     //=================//
#         //===========================================================================//
#         auto smear_func = [&](TLorentzVector V4){
#             // True generated values (i.e., values of the unsmeared TLorentzVector)
#             double inM = V4.M();
#             double smeared_P  = V4.P();
#             double smeared_Th = V4.Theta();
#             double smeared_Phi = V4.Phi();
#             TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());
#             // Calculate resolutions
#             double smeared_ThD = TMath::RadToDeg()*smeared_Th;
#             double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
#             double momS2 = 0.02*smeared_ThD;
#             double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
#             momR *= 2.0;
#             // // From ∆P(El) Sigma distributions:
#             // momR *= (0.02408)*V4.P()*V4.P() + (-0.25556)*V4.P() + (1.33331);
#             double theS1 = 0.004*smeared_ThD + 0.1;
#             double theS2 = 0;
#             double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
#             theR *= 2.5;
#             double phiS1 = 0.85 - 0.015*smeared_ThD;
#             double phiS2 = 0.17 - 0.003*smeared_ThD;
#             double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
#             phiR *= 3.5;
#             // cout<<"Smearing Factor for Phi: "<<phiR<<endl;
#             // cout<<"Smearing Factor for Th: "<<theR<<endl;
#             // cout<<"Smearing Factor for P: "<<momR<<endl;
#             // cout<<"Pre-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
#             // cout<<"Pre-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
#             // cout<<"Pre-Smear P : "<<smeared_P<<endl;
#             // overwrite EB (i.e., applying the smear)
#             smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
#             smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
#             smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();
#             // cout<<"Smear-Factor Phi (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * phiR * gRandom->Gaus(0,1)))<<endl;
#             // cout<<"Smear-Factor Th (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * theR * gRandom->Gaus(0,1)))<<endl;
#             // cout<<"Smear-Factor P : "<<(momR  * gRandom->Gaus(0,1) *  V4.P())<<endl;
#             // cout<<"Post-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
#             // cout<<"Post-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
#             // cout<<"Post-Smear P : "<<smeared_P<<endl;
#             // EB_rec_mom = GEN_mom + resolution_momentum x gaussian x GEN_mom
#             // EB_rec_ang = GEN_ang + resolution_angle x gaussian
#             V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
#             V4_new.SetRho( smeared_P );
#             V4_new.SetTheta( smeared_Th );
#             V4_new.SetPhi( smeared_Phi );
#             return V4_new;
#         };"""
    
    
    
    
    
    
#     smearing_function = """
#         //===========================================================================//
#         //=================//     Modified Smearing Function      //=================//
#         //===========================================================================//
#         auto smear_func = [&](TLorentzVector V4, int ivec){
#             // True generated values (i.e., values of the unsmeared TLorentzVector)
#             double inM = V4.M();
#             double smeared_P  = V4.P();
#             double smeared_Th = V4.Theta();
#             double smeared_Phi = V4.Phi();
#             TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());
#             // Calculate resolutions
#             double smeared_ThD = TMath::RadToDeg()*smeared_Th;
#             double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
#             double momS2 = 0.02*smeared_ThD;
#             double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
#             momR *= 2.0;
#             if(ivec == 0){
#                 // From ∆P(Electron) Sigma distributions:
#                 momR *= (-1.0429e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (1.3654e-03)*(V4.Theta()*TMath::RadToDeg()) + (1.0663e+00);
#                 momR *= (-8.4052e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (9.8234e-03)*(V4.Theta()*TMath::RadToDeg()) + (1.0144e+00);
#                 momR *= (1.5861e-02)*(V4.P())*(V4.P()) + (-1.5747e-01)*(V4.P()) + (1.3121e+00);
#                 momR *= (-9.6572e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (1.6144e-02)*(V4.Theta()*TMath::RadToDeg()) + (9.5746e-01); 
#             }
#             if(ivec == 1){
#                 // From ∆P(Pi+ Pion) Sigma distributions:
#                 momR *= (-1.1676e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (4.3908e-02)*(V4.Theta()*TMath::RadToDeg()) + (4.3709e-01);
#                 momR *= (-2.3121e-02)*(V4.P())*(V4.P()) + (5.6810e-02)*(V4.P()) + (8.7293e-01);
#                 momR *= (-2.5476e-02)*(V4.P())*(V4.P()) + (7.6973e-02)*(V4.P()) + (8.6465e-01);
#                 momR *= (-2.6101e-02)*(V4.P())*(V4.P()) + (1.1440e-01)*(V4.P()) + (7.8815e-01);
#             }
#             double theS1 = 0.004*smeared_ThD + 0.1;
#             double theS2 = 0;
#             double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
#             theR *= 2.5;
#             if(ivec == 0){
#                 // From ∆Theta(Electron) Sigma distributions (Function of Momentum):
#                 theR *= (-7.9405e-02)*(V4.P())*(V4.P()) + (9.3003e-01)*(V4.P()) + (-1.4985e+00);
#                 // From ∆Theta(Electron) Sigma distributions (Function of Theta):
#                 theR *= (-1.5170e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (5.1704e-02)*(V4.Theta()*TMath::RadToDeg()) + (7.9883e-01);
#                 // From ∆Theta(Electron) Sigma distributions (Function of Momentum):
#                 theR *= (-9.9576e-02)*(V4.P())*(V4.P()) + (1.1164e+00)*(V4.P()) + (-1.7216e+00);
#             }
#             if(ivec == 1){
#                 // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
#                 theR *= (-2.2858e-02)*(V4.P())*(V4.P()) + (2.3043e-01)*(V4.P()) + (5.7916e-01);                
#                 // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Theta):
#                 theR *= (-1.5395e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (7.6614e-02)*(V4.Theta()*TMath::RadToDeg()) + (2.3594e-01);
#                 // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
#                 theR *= (-4.8283e-03)*(V4.P())*(V4.P()) + (1.6123e-01)*(V4.P()) + (7.6315e-01);
#                 // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
#                 theR *= (1.9715e-02)*(V4.P())*(V4.P()) + (-4.9812e-02)*(V4.P()) + (1.2059e+00);
#                 theR *= (2.7160e-02)*(V4.P())*(V4.P()) + (-1.0975e-01)*(V4.P()) + (1.2968e+00);
#                 // From ∆Theta(Pi+ Pion) Vs Momentum Sigma distributions:
#                 theR *= (-1.2412e-02)*(V4.P())*(V4.P()) + (1.8465e-01)*(V4.P()) + (7.5162e-01);
#             }   
#             double phiS1 = 0.85 - 0.015*smeared_ThD;
#             double phiS2 = 0.17 - 0.003*smeared_ThD;
#             double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
#             phiR *= 3.5;
#             // overwrite EB (i.e., applying the smear)
#             smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
#             smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
#             smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();
#             V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
#             V4_new.SetRho( smeared_P );
#             V4_new.SetTheta( smeared_Th );
#             V4_new.SetPhi( smeared_Phi );
#             return V4_new;
#         };
#     """
    
    
    
    
    
    
#     smearing_function = """
#         //===========================================================================//
#         //=================//     Modified Smearing Function      //=================//
#         //===========================================================================//
#         auto smear_func = [&](TLorentzVector V4, int ivec){
#             // True generated values (i.e., values of the unsmeared TLorentzVector)
#             double inM = V4.M();
#             double smeared_P  = V4.P();
#             double smeared_Th = V4.Theta();
#             double smeared_Phi = V4.Phi();
#             TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());
#             // Calculate resolutions
#             double smeared_ThD = TMath::RadToDeg()*smeared_Th;
#             double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
#             double momS2 = 0.02*smeared_ThD;
#             double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
#             momR *= 2.0;
#             if(ivec == 0){
#                 // From ∆P(Electron) Sigma Vs Momentum distributions:
#                 momR *= (2.0604e-02)*(V4.P())*(V4.P()) + (-1.1212e-01)*(V4.P()) + (7.1348e-01);
#                 momR *= (-1.1295e-02)*(V4.P())*(V4.P()) + (2.3416e-01)*(V4.P()) + (-1.0974e-01);
#                 // From ∆P(Electron) Sigma Vs Theta distributions:
#                 momR *= (-2.7657e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) +  (8.1714e-02)*(V4.Theta()*TMath::RadToDeg()) + (4.0196e-01);
#                 momR *= (-7.3974e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) +  (1.0908e-02)*(V4.Theta()*TMath::RadToDeg()) + (9.9876e-01);
#             }
#             if(ivec == 1){
#                 // From ∆P(Pi+ Pion) Sigma Vs Momentum distributions:
#                 momR *= (-5.2125e-02)*(V4.P())*(V4.P()) + (2.7110e-01)*(V4.P()) + (4.8534e-01);
#                 momR *= (-3.4607e-02)*(V4.P())*(V4.P()) + (1.5836e-01)*(V4.P()) + (6.8845e-01);
#                 // From ∆P(Pi+ Pion) Sigma Vs Theta distributions:
#                 momR *= (-5.7711e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) +  (2.4354e-02)*(V4.Theta()*TMath::RadToDeg()) + (6.6472e-01);
#                 momR *= (-1.3210e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) +  (3.5065e-02)*(V4.Theta()*TMath::RadToDeg()) + (8.3333e-01);
#                 // From ∆P(Pi+ Pion) Sigma Vs Theta distributions:
#                 momR *=  (6.9462e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (-4.8277e-01)*(V4.Theta()*TMath::RadToDeg()) + (9.8916e+00);
#             }
#             double theS1 = 0.004*smeared_ThD + 0.1;
#             double theS2 = 0;
#             double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
#             theR *= 2.5;
#             double phiS1 = 0.85 - 0.015*smeared_ThD;
#             double phiS2 = 0.17 - 0.003*smeared_ThD;
#             double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
#             phiR *= 3.5;
#             // overwrite EB (i.e., applying the smear)
#             smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
#             smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
#             smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();
#             V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
#             V4_new.SetRho( smeared_P );
#             V4_new.SetTheta( smeared_Th );
#             V4_new.SetPhi( smeared_Phi );
#             return V4_new;
#         };"""
    
    
    
    
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
        };"""]) if((smear_factor not in ["FX"]) and (datatype not in ["rdf", "gdf"])) else """
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
            TLorentzVector ele_no_cor_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
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
            TLorentzVector pip0_no_cor_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """
            //=================//     Vectors have been Smeared     //=================//
            auto pip_no_cor_smeared = pip0_no_cor_smeared.P();
            return pip_no_cor_smeared;
        """]))
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Applying the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define("smeared_vals", "".join(["""
        """, str(smearing_function),       """
        """, str(Correction_Code_Full_In), """
        
        auto fe    = dppC(ex,   ey,   ez,   esec,   0, """, "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;
        auto fpip  = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;

        auto beamM = ROOT::Math::PxPyPzMVector(0,         0,         10.6041,   0);
        auto targM = ROOT::Math::PxPyPzMVector(0,         0,         0,         0.938272);
        auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        TLorentzVector beam(0,         0,         10.6041,      beamM.E());
        TLorentzVector targ(0,         0,         0,            targM.E());
        TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,        eleM.E());
        TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip,    pip0M.E());

        TLorentzVector ele_NO_SMEAR(ex*fe,      ey*fe,     ez*fe,     eleM.E());
        TLorentzVector pip0_NO_SMEAR(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());

        //========================================================================//
        //=================//     Smearing PxPyPzMVector's     //=================//
        //========================================================================//

        TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
        TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

        //=========================================================================//
        //=================//     Vectors have been Smeared     //=================//
        //=========================================================================//

        TLorentzVector lv_q = beam - ele_smeared;

        auto Delta_Smear_El_P   = abs(ele_smeared.P())        - abs(ele_NO_SMEAR.P());                         // Delta_Smear_El.P();
        auto Delta_Smear_El_Th  = (abs(ele_smeared.Theta())   - abs(ele_NO_SMEAR.Theta()))*TMath::RadToDeg();  // Delta_Smear_El.Theta()*TMath::RadToDeg();
        auto Delta_Smear_El_Phi = (abs(ele_smeared.Phi())     - abs(ele_NO_SMEAR.Phi()))*TMath::RadToDeg();    // Delta_Smear_El.Phi()*TMath::RadToDeg();

        auto Delta_Smear_Pip_P   = abs(pip0_smeared.P())      - abs(pip0_NO_SMEAR.P());                        // Delta_Smear_Pip.P();
        auto Delta_Smear_Pip_Th  = (abs(pip0_smeared.Theta()) - abs(pip0_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_Pip.Theta()*TMath::RadToDeg();
        auto Delta_Smear_Pip_Phi = (abs(pip0_smeared.Phi())   - abs(pip0_NO_SMEAR.Phi()))*TMath::RadToDeg();   // Delta_Smear_Pip.Phi()*TMath::RadToDeg();

        // Rest of calculations are performed as normal from here

        auto epipX         = beam + targ - ele_smeared - pip0_smeared;
        auto q_smeared     = beam - ele_smeared;
        auto Q2_smeared    = -q_smeared.M2();
        auto v_smeared     = beam.E() - ele_smeared.E();
        auto xB_smeared    = Q2_smeared/(2*targ.M()*v_smeared);
        auto W2_smeared    = targ.M2() + 2*targ.M()*v_smeared - Q2_smeared;
        auto W_smeared     = sqrt(W2_smeared);
        auto y_smeared     = (targ.Dot(q_smeared))/(targ.Dot(beam));
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

        if(elPhi_smeared < 0){
            elPhi_smeared += 360;
        }

        auto pipPhi_smeared = pip0_smeared.Phi()*TMath::RadToDeg();

        if(pipPhi_smeared < 0){
            pipPhi_smeared += 360;
        }

        //=================================================================================================================================//
        //==============================================//          Rotation Code          //==============================================//
        //=================================================================================================================================//

        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el  = ele_smeared.Phi();

        """, str(Rotation_Matrix), """

        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele_smeared,  -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0_smeared, -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);

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

        if(phi_t_smeared < 0){
            phi_t_smeared += 360;
        }

        //===================================================================================================================================//
        //----------------------------------------------//===================================//----------------------------------------------//
        //==============================================//          Smeared Binning          //==============================================//
        //----------------------------------------------//===================================//----------------------------------------------//
        //===================================================================================================================================//

        //===================================================================================//
        //=======================//          Q2-xB Binning          //=======================//
        //===================================================================================//

        double Q2_xB_Bin_smeared = 0;

        /////////////////////////       Bin 1       /////////////////////////
        if(xB_smeared > 0.0835 && xB_smeared < 0.15){
            // Border lines of Bin 1:
            //                 Upper Border:
            //                          Q2_smeared = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_smeared - 0.0835) + 1.3
            //                 Q2_smeared must be less than the equation above for Bin 1
            //
            //                 Lower Border:
            //                          Q2_smeared = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_smeared - 0.0835) + 1.30   (if xB_smeared < 0.12)
            //                          Q2_smeared = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_smeared - 0.1200) + 1.30   (if xB_smeared > 0.12)
            //                 Q2_smeared must be greater than the equations above for Bin 1

            int Condition_Up = 0;
            int Condition_Down = 0;
            // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
            // Code will verify both conditions seperately before checking that they have been met.
            // If the condition has been met, its value will be set to 1.
            // If either is still 0 when checked, the event will be consided as being outside of Bin 1

            // Testing Upper Border of Bin 1
            if(Q2_smeared <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_smeared - 0.0835) + 1.3){
                Condition_Up = 1; // Condition for upper border of Bin 1 has been met
            }

            // Testing Lower Border of Bin 1
            if(xB_smeared < 0.12){
                if(Q2_smeared >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_smeared - 0.0835) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }
            if(xB_smeared > 0.12){
                if(Q2_smeared >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_smeared - 0.1200) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }

            if(Condition_Up == 1 && Condition_Down == 1){
                Q2_xB_Bin_smeared = 1;
                // Bin 1 Confirmed
            }

        }
        /////////////////////////     End of Bin 1     /////////////////////////

        /////////////////////////       Bin 2 or 3       /////////////////////////
        if(xB_smeared > 0.15 && xB_smeared < 0.24){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98

            // Deciding between Bins
            if(Q2_smeared < ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98){
                BinTest = 2; // Event will NOT go to bin 3
            }

            if(Q2_smeared > ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98){
                BinTest = 3; // Event will NOT go to bin 2
            }
            // Final Border Test
            // Bin 2
            if(BinTest == 2){
                // Border lines of Bin 2:   Q2_smeared = ((1.45 - 1.38)/(0.20 - 0.15))*(xB_smeared - 0.15) + 1.38   (if xB_smeared < 0.2)
                //                          Q2_smeared = ((1.50 - 1.45)/(0.24 - 0.20))*(xB_smeared - 0.24) + 1.50   (if xB_smeared > 0.2)
                if(xB_smeared < 0.2){
                    if(Q2_smeared >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB_smeared - 0.15) + 1.38){
                        Q2_xB_Bin_smeared = 2;
                        // Bin 2 Confirmed
                    }
                }
                if(xB_smeared > 0.2){
                    if(Q2_smeared >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB_smeared - 0.24) + 1.50){
                        Q2_xB_Bin_smeared = 2;
                        // Bin 2 Confirmed
                    }
                }
            }
            // End of Bin 2
            
            // Bin 3
            if(BinTest == 3){
                // Border line of Bin 3:   Q2_smeared = ((3.625 - 2.28)/(0.24 - 0.15))*(xB_smeared - 0.15) + 2.28

                if(Q2_smeared <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB_smeared - 0.15) + 2.28){
                    Q2_xB_Bin_smeared = 3;
                    // Bin 3 Confirmed
                }

            }
            // End of Bin 3
        }
        /////////////////////////     End of Bin 2 and 3     /////////////////////////

        /////////////////////////       Bin 4 or 5       /////////////////////////
        if(xB_smeared > 0.24 && xB_smeared < 0.34){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75

            // Deciding between Bins
            if(Q2_smeared < ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75){
                BinTest = 4; // Event will NOT go to bin 5
            }

            if(Q2_smeared > ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75){
                BinTest = 5; // Event will NOT go to bin 4
            }

            // Final Border Test
            // Bin 4
            if(BinTest == 4){
                // Border lines of Bin 4:   Q2_smeared = ((1.53 - 1.50)/(0.27 - 0.24))*(xB_smeared - 0.24) + 1.50   (if xB_smeared < 0.27)
                //                          Q2_smeared = ((1.56 - 1.53)/(0.30 - 0.27))*(xB_smeared - 0.27) + 1.53   (if 0.27 < xB_smeared < 0.30)
                //                          Q2_smeared = ((1.60 - 1.56)/(0.34 - 0.30))*(xB_smeared - 0.30) + 1.56   (if xB_smeared > 0.3)
                if(xB_smeared < 0.27){
                    if(Q2_smeared >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB_smeared - 0.24) + 1.50){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }
                if(xB_smeared > 0.27 && xB_smeared < 0.30){
                    if(Q2_smeared >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB_smeared - 0.27) + 1.53){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }
                if(xB_smeared > 0.30){
                    if(Q2_smeared >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB_smeared - 0.30) + 1.56){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }
            }
            // End of Bin 4
            // Bin 5
            if(BinTest == 5){
                // Border line of Bin 5:   Q2_smeared = ((5.12 - 3.625)/(0.34 - 0.24))*(xB_smeared - 0.24) + 3.625
                if(Q2_smeared <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB_smeared - 0.24) + 3.625){
                    Q2_xB_Bin_smeared = 5;
                    // Bin 5 Confirmed
                }
            }
            // End of Bin 5
        }
        /////////////////////////     End of Bin 4 and 5     /////////////////////////

        /////////////////////////       Bin 6 or 7       /////////////////////////
        if(xB_smeared > 0.34 && xB_smeared < 0.45){
            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)
            // line between bins: Q2_smeared = ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63
            // Deciding between Bins
            if(Q2_smeared < ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63){
                BinTest = 6; // Event will NOT go to bin 7
            }
            if(Q2_smeared > ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63){
                BinTest = 7; // Event will NOT go to bin 6
            }
            // Final Border Test
            // Bin 6
            if(BinTest == 6){
                // Border line of Bin 6:   Q2_smeared = ((2.52 - 1.60)/(0.45 - 0.34))*(xB_smeared - 0.34) + 1.60
                if(Q2_smeared >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB_smeared - 0.34) + 1.60){
                    Q2_xB_Bin_smeared = 6;
                    // Bin 6 Confirmed
                }
            }
            // End of Bin 6
            // Bin 7
            if(BinTest == 7){
                // Border line of Bin 7:   Q2_smeared = ((6.76 - 5.12)/(0.45 - 0.34))*(xB_smeared - 0.34) + 5.12
                if(Q2_smeared <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB_smeared - 0.34) + 5.12){
                    Q2_xB_Bin_smeared = 7;
                    // Bin 7 Confirmed
                }
            }
            // End of Bin 7
        }
        /////////////////////////     End of Bin 6 and 7     /////////////////////////

        /////////////////////////       Bin 8 or 9       /////////////////////////
        if(xB_smeared > 0.45){
            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)
            // line between bins: Q2_smeared = ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70    
            // Deciding between Bins
            if(Q2_smeared < ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70){
                BinTest = 8; // Event will NOT go to bin 9
            }
            if(Q2_smeared > ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70){
                BinTest = 9; // Event will NOT go to bin 8
            }
            // Final Border Test
            // Bin 8
            if(BinTest == 8){
                // Border lines of Bin 8:   Q2_smeared = ((3.05 - 2.52)/(0.500 - 0.45))*(xB_smeared - 0.45) + 2.52   (if xB_smeared < 0.50)
                //                          Q2_smeared = ((4.05 - 3.05)/(0.570 - 0.50))*(xB_smeared - 0.50) + 3.05   (if 0.50 < xB_smeared < 0.57)
                //                          Q2_smeared = ((5.40 - 4.05)/(0.640 - 0.57))*(xB_smeared - 0.57) + 4.05   (if 0.57 < xB_smeared < 0.64)
                //                          Q2_smeared = ((7.42 - 5.40)/(0.708 - 0.64))*(xB_smeared - 0.64) + 5.40   (if xB_smeared > 0.64)
                if(xB_smeared < 0.50){
                    if(Q2_smeared >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB_smeared - 0.45) + 2.52){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }
                if(xB_smeared > 0.50 && xB_smeared < 0.57){
                    if(Q2_smeared >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB_smeared - 0.50) + 3.05){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }
                if(xB_smeared > 0.57 && xB_smeared < 0.64){
                    if(Q2_smeared >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB_smeared - 0.57) + 4.05){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }
                if(xB_smeared > 0.64){
                    if(Q2_smeared >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB_smeared - 0.64) + 5.40){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }
            }
            // End of Bin 8
            // Bin 9
            if(BinTest == 9){
                // Border lines of Bin 9:
                //                 Uppermost Border:
                //                          Q2_smeared = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_smeared - 0.450) +  6.760   (if xB_smeared < 0.677)
                //                          Q2_smeared = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_smeared - 0.677) + 10.185   (if xB_smeared > 0.677)
                //                 Q2_smeared must be less than the equations above for Bin 9
                //
                //                 Rightmost Border:
                //                          Q2_smeared =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_smeared - 0.708) + 7.42   (if xB_smeared < 0.75)
                //                          Q2_smeared = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_smeared - 0.750) + 9.52   (if xB_smeared > 0.75)
                //                 Q2_smeared must be greater than the equations above for Bin 9

                int Condition_Up = 0;
                int Condition_Right = 0;
                // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 9

                // Testing Uppermost Border of Bin 9
                if(xB_smeared < 0.677){
                    if(Q2_smeared <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_smeared - 0.450) +  6.760){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }
                if(xB_smeared > 0.677){
                    if(Q2_smeared <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_smeared - 0.677) + 10.185){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }

                // Testing Rightmost Border of Bin 9
                if(xB_smeared < 0.75){
                    if(Q2_smeared >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_smeared - 0.708) + 7.42){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }
                if(xB_smeared > 0.75){
                    if(Q2_smeared >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_smeared - 0.750) + 9.52){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }

                if(Condition_Up == 1 && Condition_Right == 1){
                    Q2_xB_Bin_smeared = 9;
                    // Bin 9 Confirmed
                }
            }
            // End of Bin 9
        }
        /////////////////////////     End of Bin 8 and 9     /////////////////////////

        //==================================================================================//
        //=======================//      End of Q2-xB Binning      //=======================//
        //=======================//================================//=======================//
        //=======================//          z-pT Binning          //=======================//
        //==================================================================================//

        double z_pT_Bin_smeared = 0;
        int Num_z_Borders = 0;
        int Num_pT_Borders = 0;

        /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry){
            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1
            if(Q2_xB_Bin_Num == 1){
                float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_Num == 2){
                float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 3
            if(Q2_xB_Bin_Num == 3){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_Num == 4){
                float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_Num == 6){
                float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 7
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_Num == 8){
                float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 9
            if(Q2_xB_Bin_Num == 9){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }

            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };

        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////

        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // For Q2_xB Bin 0
        if(Q2_xB_Bin_smeared== 0){
            z_pT_Bin_smeared = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
            Num_z_Borders = 0;
            Num_pT_Borders = 0;
        }
        // For Q2_xB Bin 1
        if(Q2_xB_Bin_smeared== 1){
            // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 2
        if(Q2_xB_Bin_smeared== 2){
            // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 3
        if(Q2_xB_Bin_smeared== 3){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 4
        if(Q2_xB_Bin_smeared== 4){
            // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 5
        if(Q2_xB_Bin_smeared== 5){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 6
        if(Q2_xB_Bin_smeared== 6){
            // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
            Num_pT_Borders = 6;
        }
        // For Q2_xB Bin 7
        if(Q2_xB_Bin_smeared== 7){
            // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
            Num_pT_Borders = 7;
        }
        // For Q2_xB Bin 8
        if(Q2_xB_Bin_smeared== 8){
            // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
            Num_pT_Borders = 5;
        }
        // For Q2_xB Bin 9
        if(Q2_xB_Bin_smeared== 9){
            // float z_Borders[]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};
            Num_pT_Borders = 6;
        }

        if(Num_z_Borders == 0){
            // float  z_Borders[1]  = {0};
            Num_z_Borders = 1;
            // float  pT_Borders[1] = {0};
            Num_pT_Borders = 1;
        }


        int z_pT_Bin_smeared_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin_smeared != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z_smeared > Borders_function(Q2_xB_Bin_smeared, 0, zbin) && z_smeared < Borders_function(Q2_xB_Bin_smeared, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin_smeared != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT_smeared > Borders_function(Q2_xB_Bin_smeared, 1, pTbin) && pT_smeared < Borders_function(Q2_xB_Bin_smeared, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin_smeared = z_pT_Bin_smeared_count; // The value of the z_pT_Bin_smeared has been set
                        break;
                    }
                    else{
                        z_pT_Bin_smeared_count += 1; // Checking the next bin
                    }
                }

            }
            else{
                z_pT_Bin_smeared_count += (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }

        //===================================================================================//
        //=======================//       End of z-pT Binning       //=======================//
        //===================================================================================//


        //==================================================================================================================================//
        //----------------------------------------------//==================================//----------------------------------------------//
        //==============================================//      End of Smeared Binning      //==============================================//
        //----------------------------------------------//==================================//----------------------------------------------//
        //==================================================================================================================================//

        // std::vector<double> smeared_vals = {epipX.M(), epipX.M2(), Q2_smeared, xB_smeared, v_smeared, W2_smeared, W_smeared, y_smeared, z_smeared, epsilon_smeared, pT_smeared, phi_t_smeared, xF_smeared, pipx_smeared, pipy_smeared, pipz_smeared, qx_smeared, qy_smeared, qz_smeared, beamx_smeared, beamy_smeared, beamz_smeared, elex_smeared, eley_smeared, elez_smeared, Q2_xB_Bin_smeared, z_pT_Bin_smeared, ele_E_smeared, pip0_E_smeared, el_smeared, pip_smeared, elth_smeared, pipth_smeared, elPhi_smeared, pipPhi_smeared};


        std::vector<double> smeared_vals = {epipX.M(), epipX.M2(), Q2_smeared, xB_smeared, v_smeared, W2_smeared, W_smeared, y_smeared, z_smeared, epsilon_smeared, pT_smeared, phi_t_smeared, xF_smeared, Q2_xB_Bin_smeared, z_pT_Bin_smeared, el_smeared, ele_E_smeared, elth_smeared, elPhi_smeared, pip_smeared, pip0_E_smeared, pipth_smeared, pipPhi_smeared, Delta_Smear_El_P, Delta_Smear_El_Th, Delta_Smear_El_Phi, Delta_Smear_Pip_P, Delta_Smear_Pip_Th, Delta_Smear_Pip_Phi};
        //                  smeared_vals = {    1    ,     2     ,      3    ,      4    ,     5    ,      6    ,     7    ,     8    ,     9    ,        10      ,     11    ,        12    ,     13    ,        14        ,       15        ,     16    ,       17     ,       18    ,        19    ,      20    ,        21     ,        22    ,         23    ,      24         ,      25          ,      26           ,      27          ,      28           ,      29            };

        return smeared_vals;"""]))

        rdf = rdf.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
        rdf = rdf.Define('z_pT_Bin_smeared',  'smeared_vals[14]')

#         rdf = rdf.Define('Q2_xB_Bin_2_smeared', '''
#             int Q2_xB_Bin_2_smeared = Q2_xB_Bin_smeared;
#             if(Q2_xB_Bin_smeared > 1 && Q2_xB_Bin_2_smeared%2 != 0){
#                 Q2_xB_Bin_2_smeared += -2;
#             }
#             if(smeared_vals[2] < 2){
#             // if(Q2_smeared < 2){
#                 Q2_xB_Bin_2_smeared = 0; 
#             }
#             return Q2_xB_Bin_2_smeared;''')
#         rdf = rdf.Define('z_pT_Bin_2_smeared', '''
#             double z_smeared = smeared_vals[8];
#             double pT_smeared = smeared_vals[10];
#             auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry){
#                 // z_or_pT = 0 corresponds to z bins
#                 // z_or_pT = 1 corresponds to pT bins
#                 // For Q2_xB Bin 1 (was 3 in old scheme)
#                 if(Q2_xB_Bin_Num == 1){
#                     float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
#                     float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
#                     if(z_or_pT == 0){
#                         return z_Borders[7 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 2
#                 if(Q2_xB_Bin_Num == 2){
#                     float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
#                     float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
#                     if(z_or_pT == 0){
#                         return z_Borders[7 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 3 (was 5 in old scheme)
#                 if(Q2_xB_Bin_Num == 3){
#                     float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
#                     float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
#                     if(z_or_pT == 0){
#                         return z_Borders[7 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 4
#                 if(Q2_xB_Bin_Num == 4){
#                     float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
#                     float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
#                     if(z_or_pT == 0){
#                         return z_Borders[6 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 5 (was 7 in old scheme)
#                 if(Q2_xB_Bin_Num == 5){
#                     float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
#                     float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
#                     if(z_or_pT == 0){
#                         return z_Borders[6 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }    
#                 // For Q2_xB Bin 6
#                 if(Q2_xB_Bin_Num == 6){
#                     float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
#                     float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
#                     if(z_or_pT == 0){
#                         return z_Borders[5 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 7 (was 9 in old scheme)
#                 if(Q2_xB_Bin_Num == 7){
#                     float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
#                     float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};
#                     if(z_or_pT == 0){
#                         return z_Borders[5 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // For Q2_xB Bin 8
#                 if(Q2_xB_Bin_Num == 8){
#                     float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
#                     float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};
#                     if(z_or_pT == 0){
#                         return z_Borders[5 - entry];
#                     }
#                     if(z_or_pT == 1){
#                         return pT_Borders[entry];
#                     }
#                 }
#                 // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
#                 // return empty_Borders;
#                 float empty = 0;
#                 return empty;
#             };
#             /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////
#             // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')
#             // Default:
#             int Num_z_Borders = 8;
#             int Num_pT_Borders = 8;
#             int z_pT_Bin_2_smeared = 0;
#             // For Q2_xB Bin 0
#             if(Q2_xB_Bin_2_smeared == 0){
#                 z_pT_Bin_2_smeared = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
#                 Num_z_Borders = 0; Num_pT_Borders = 0;
#             }
#             // For Q2_xB Bin 1 (Uses Default for both borders)
#             // For Q2_xB Bin 2 (Uses Default for both borders)
#             // For Q2_xB Bin 3 (Uses Default for both borders)
#             // For Q2_xB Bin 4 (Uses Default for pT borders)
#             if(Q2_xB_Bin_2_smeared == 4){
#                 Num_z_Borders = 7;
#             }
#             // For Q2_xB Bin 5 (New scheme)
#             if(Q2_xB_Bin_2_smeared == 5){
#                 Num_z_Borders = 7; Num_pT_Borders = 7;
#             }
#             // For Q2_xB Bin 6
#             if(Q2_xB_Bin_2_smeared == 6){
#                 Num_z_Borders = 6; Num_pT_Borders = 6;
#             }
#             // For Q2_xB Bin 7 (New scheme)
#             if(Q2_xB_Bin_2_smeared == 7){
#                 Num_z_Borders = 6; Num_pT_Borders = 6;
#             }
#             // For Q2_xB Bin 8
#             if(Q2_xB_Bin_2_smeared == 8){
#                 Num_z_Borders = 6; Num_pT_Borders = 5;
#             }
#             if(Num_z_Borders == 0){
#                 Num_z_Borders = 1; Num_pT_Borders = 1;
#             }
#             int z_pT_Bin_2_smeared_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
#                                     // based on the number of times the loop has run
#             // Determining z_pT Bins
#             for(int zbin = 1; zbin < Num_z_Borders; zbin++){
#                 if(z_pT_Bin_2_smeared != 0){
#                     continue;   // If the bin has already been assigned, this line will end the loop.
#                                 // This is to make sure the loop does not run longer than what is necessary.
#                 }    
#                 if(z_smeared > Borders_function(Q2_xB_Bin_2_smeared, 0, zbin) && z_smeared < Borders_function(Q2_xB_Bin_2_smeared, 0, zbin - 1)){
#                     // Found the correct z bin
#                     for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
#                         if(z_pT_Bin_2_smeared != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)
#                         if(pT_smeared > Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin) && pT_smeared < Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin+1)){
#                             // Found the correct pT bin
#                             z_pT_Bin_2_smeared = z_pT_Bin_2_smeared_count; // The value of the z_pT_Bin_2_smeared has been set
#                             // cout<<"The value of the z_pT_Bin_2_smeared has been set as: "<<z_pT_Bin_2_smeared<<endl;
#                             break;
#                         }
#                         else{
#                             z_pT_Bin_2_smeared_count += 1; // Checking the next bin
#                             // cout<<"Checking the next bin"<<endl;
#                         }
#                     }
#                 }
#                 else{
#                     z_pT_Bin_2_smeared_count += (Num_pT_Borders - 1);
#                     // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
#                     // This represents checking each pT bin for the given z bin without going through each entry in the loop.
#                 }    
#             }
#             return z_pT_Bin_2_smeared;''')

        ##==================================================##
        ##==========## End of Smeared DataFrame ##==========##
        ##==================================================##
        
    def smear_frame_compatible(Data_Frame, Variable, Smearing_Q):
        if(Data_Frame == "continue"):
            return Data_Frame
        if("smear" not in Smearing_Q or (datatype not in ["mdf", "pdf"]) or (str(Variable) in Data_Frame.GetColumnNames())):
            # Variable should already be defined/cannot smear real/generated data
            # if(str(Variable) in Data_Frame.GetColumnNames()):
            #     print("".join(["Already defined: ", str(Variable)]))
            return Data_Frame
        elif(Variable in ["esec", "esec_smeared", "pipsec", "pipsec_smeared", "Hx", "Hx_smeared", "Hy", "Hy_smeared"]):
            print(color.Error, "\nCannot smear particle sector\n", color.END)
            Data_Frame = "continue"
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
            
    ##=========================================================================================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=================================##     End of Smearing Functions     ##=================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=========================================================================================================##
    
    
    
    
    
    
    
    
    
    if(Use_Weight):
        if(not Q4_Weight):
            print(color.GREEN, color.BOLD, "".join(["\n", color_bg.BLUE, "Running 'Closure Test' for Modulated Monte Carlo Generated phi_h distributions...", color.END, "\n\n"]))
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
            # if(datatype in ["mdf", "pdf"]):
            #     rdf = rdf.Define('Event_Weight_gen', """
            #     auto   Par_B_Test_gen   = -0.050;
            #     auto   Par_C_Test_gen   =  0.025;
            #     auto   PHI_H_gen        = phi_t_gen*TMath::DegToRad();
            #     auto   Event_Weight_gen = 1 + Par_B_Test_gen*TMath::Cos(PHI_H_gen) + Par_C_Test_gen*TMath::Cos(2*PHI_H_gen);
            #     return Event_Weight_gen;
            #     """)
            #     rdf = rdf.Define('Event_Weight_smeared', """
            #     auto   Par_B_Test_smeared   = -0.050;
            #     auto   Par_C_Test_smeared   =  0.025;
            #     auto   PHI_H_smeared        = smeared_vals[11]*TMath::DegToRad();
            #     auto   Event_Weight_smeared = 1 + Par_B_Test_smeared*TMath::Cos(PHI_H_smeared) + Par_C_Test_smeared*TMath::Cos(2*PHI_H_smeared);
            #     return Event_Weight_smeared;
            #     """)
            ##==========================================================================================================##
            ##------------------------------------##==============================##------------------------------------##
            ##====================================##      Event Weighing End      ##====================================##
            ##------------------------------------##==============================##------------------------------------##
            ##==========================================================================================================##
        else:
            print(color.GREEN, color.BOLD, "".join(["\n", color_bg.BLUE, "Running 'Q4 Weight' for weighing the Monte Carlo distributions...", color.END, "\n\n"]))
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
        print(color.BOLD,                             "".join(["\nNOT running 'Closure Test' for Modulated Monte Carlo Generated phi_h distributions...", color.END, "\n\n"]))
    
    
    
    
    
    
    
    
    
    ##==========================================================================================================##
    ##------------------------------------##==============================##------------------------------------##
    ##====================================##  Generated Missing Mass Cut  ##====================================##
    ##------------------------------------##==============================##------------------------------------##
    ##==========================================================================================================##
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define('Missing_Mass_Cut_Gen', """
        auto Missing_Mass_Cut_Gen = 0;
        if(MM_gen < 1.5){
            Missing_Mass_Cut_Gen = -1;
        }
        else{
            Missing_Mass_Cut_Gen =  1;
        }
        return Missing_Mass_Cut_Gen;
        """)
    if(datatype in ["gdf", "gen"]):
        rdf = rdf.Define('Missing_Mass_Cut_Gen', """
        auto Missing_Mass_Cut_Gen = 0;
        if(MM < 1.5){
            Missing_Mass_Cut_Gen = -1;
        }
        else{
            Missing_Mass_Cut_Gen =  1;
        }
        return Missing_Mass_Cut_Gen;
        """)
    ##==========================================================================================================##
    ##------------------------------------##==============================##------------------------------------##
    ##====================================##  Gen Missing Mass Cut (End)  ##====================================##
    ##------------------------------------##==============================##------------------------------------##
    ##==========================================================================================================##
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

    rdf = rdf.Define("Delta_Pel_Cors", "".join([str(Correction_Code_Full_In), """
        auto fe   = dppC(ex,   ey,   ez,   esec,   0, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
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


    rdf = rdf.Define("Delta_Ppip_Cors", "".join([str(Correction_Code_Full_In), """
        auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
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

    rdf = rdf.Define("Delta_Theta_el_Cors", "".join([str(Correction_Code_Full_In), """
        auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
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


    rdf = rdf.Define("Delta_Theta_pip_Cors",  "".join([str(Correction_Code_Full_In), """
        auto fe   = dppC(ex,   ey,   ez,   esec,   0, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if((Mom_Correction_Q != "yes") or (str(datatype) in ["gdf"])) else "1" if(str(datatype) in ['rdf']) else "2", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
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

    if(datatype not in ["rdf", "gdf"]):

        rdf = rdf.Define("Delta_Pel_Cors_smeared", "".join([str(smearing_function), """
""", str(Correction_Code_Full_In), """
            auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;

            auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

            TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
            TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());

            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
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
""", str(Correction_Code_Full_In), """
            auto fe   = dppC(ex, ey, ez, esec, 0, """,         "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "2", """) + 1;
            
            auto eleM  = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
            
            TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
            TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
            
            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """
            
            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());
            
            auto Beam_Energy = 10.6041;
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
            // Delta_Ppip_Cors_smeared = pip_gen - pipC.P();

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

            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(),  ele_smeared.Y(),  ele_smeared.Z(),  ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
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

            TLorentzVector ele_smeared  = smear_func(ele""",  (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
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
    if(datatype not in ["rdf", "gdf"]):
        rdf = rdf.Define("DP_el_SF_smeared",  "Delta_Pel_Cors_smeared/smeared_vals[15]")
        rdf = rdf.Define("DP_pip_SF_smeared", "Delta_Ppip_Cors_smeared/smeared_vals[19]")
        
        rdf = rdf.Define("Dele_SF", "abs(el  - smeared_vals[15])/el")
        rdf = rdf.Define("Dpip_SF", "abs(pip - smeared_vals[19])/pip")

        
    print("Kinematic Variables have been calculated.")
    
    
    ###################################################################################################################################################################
    ###################################################       Done with Calculating (All) Kinematic Variables       ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################                  Making Cuts to DataFrames                  ###################################################
    ###################################################################################################################################################################
    
    
    def filter_Valerii(Data_Frame, Valerii_Cut):
        if("Valerii_Cut" in Valerii_Cut or "Complete" in Valerii_Cut):
            Data_Frame_Clone = Data_Frame.Filter("""
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
                return BadElementKnockOut(Hx, Hy, esec, 1);""")
            return Data_Frame_Clone
        else:
            return Data_Frame
    
    
    # Meant for the exclusive ep->eπ+(N) reaction
    def Calculated_Exclusive_Cuts(Smear_Q):
        output = "".join(["""
        """, str(smearing_function), """
        auto beam = ROOT::Math::PxPyPzMVector(0,    0,    10.6041, 0);
        auto targ = ROOT::Math::PxPyPzMVector(0,    0,    0,       0.938);
        auto ele  = ROOT::Math::PxPyPzMVector(ex,   ey,   ez,      0);
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz,    0.13957);
        """, "".join(["""
        TLorentzVector eleS(ex, ey, ez, ele.E());
        TLorentzVector pipS(pipx, pipy, pipz, pip0.E());
        
        TLorentzVector ele_smeared = smear_func(eleS""", (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
        TLorentzVector pip_smeared = smear_func(pipS""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """
        
        ele  = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), 0);
        pip0 = ROOT::Math::PxPyPzMVector(pip_smeared.X(), pip_smeared.Y(), pip_smeared.Z(), 0.13957);
        
        """]) if(("smear" in Smear_Q) and (datatype not in ["rdf"])) else "", """

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
            print("".join(["The input: ", color.RED, str(Variable_Type), color.END, " was not recognized by the function Q2_xB_Bin_Standard_Def_Function(Variable_Type).\nFix input to use anything other than the default calculations of Q2 and xB."]))
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
        z_pT_Bin_event_val = Find_z_pT_Bin(""",       str(Q2_xB_Bin_event_name), """, z_event_val, pT_event_val);
        if(Phi_h_Bin_Values[""",                      str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][0] == 1){Phih_Bin_event_val = 1;}
        else{Phih_Bin_event_val = Find_phi_h_Bin(""", str(Q2_xB_Bin_event_name), """, z_pT_Bin_event_val, """, "smeared_vals[11]" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "phi_t", "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """);}
        MultiDim3D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][1] + Phih_Bin_event_val;
        MultiDim5D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][2] + Phih_Bin_event_val;
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
    // }""", """
    std::vector<int> z_pT_and_MultiDim_Bins = {z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val};
    return z_pT_and_MultiDim_Bins;"""])
            
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
        
        # Q2_y_z_pT_4D_Bin_Def = "".join(["""
        # int Q2_y_Bin_event_val = """, str(Q2_y_Bin_event_name), """;
        # int z_pT_Bin_event_val = """, str(z_pT_Bin_event_name), """;
        # int Q2_y_z_pT_4D_Bin_event_val = 0;
        # if(Q2_y_Bin_event_val > 1){
        #     Q2_y_z_pT_4D_Bin_event_val += 49;
        # }
        # if(Q2_y_Bin_event_val > 2){
        #     Q2_y_z_pT_4D_Bin_event_val += 49;
        # }
        # if(Q2_y_Bin_event_val > 3){
        #     Q2_y_z_pT_4D_Bin_event_val += 49;
        # }
        # if(Q2_y_Bin_event_val > 4){
        #     Q2_y_z_pT_4D_Bin_event_val += 42;
        # }
        # if(Q2_y_Bin_event_val > 5){
        #     Q2_y_z_pT_4D_Bin_event_val += 36;
        # }
        # if(Q2_y_Bin_event_val > 6){
        #     Q2_y_z_pT_4D_Bin_event_val += 30;
        # }
        # if(Q2_y_Bin_event_val > 7){
        #     Q2_y_z_pT_4D_Bin_event_val += 49;
        # }
        # if(Q2_y_Bin_event_val > 8){
        #     Q2_y_z_pT_4D_Bin_event_val += 36;
        # }
        # if(Q2_y_Bin_event_val > 9){
        #     Q2_y_z_pT_4D_Bin_event_val += 36;
        # }
        # if(Q2_y_Bin_event_val > 10){
        #     Q2_y_z_pT_4D_Bin_event_val += 30;
        # }
        # if(Q2_y_Bin_event_val > 11){
        #     Q2_y_z_pT_4D_Bin_event_val += 30;
        # }
        # if(Q2_y_Bin_event_val > 12){
        #     Q2_y_z_pT_4D_Bin_event_val += 20;
        # }
        # if(Q2_y_Bin_event_val > 13){
        #     Q2_y_z_pT_4D_Bin_event_val += 25;
        # }
        # if(Q2_y_Bin_event_val > 14){
        #     Q2_y_z_pT_4D_Bin_event_val += 25;
        # }
        # if(Q2_y_Bin_event_val > 15){
        #     Q2_y_z_pT_4D_Bin_event_val += 20;
        # }
        # if(Q2_y_Bin_event_val > 16){
        #     Q2_y_z_pT_4D_Bin_event_val += 20;
        # }
        # Q2_y_z_pT_4D_Bin_event_val += z_pT_Bin_event_val;
        # if(Q2_y_Bin_event_val < 1 || z_pT_Bin_event_val < 1){
        #     Q2_y_z_pT_4D_Bin_event_val = 0;
        # }
        # return Q2_y_z_pT_4D_Bin_event_val;
        # """])
        
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

##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    def Bin_Purity_Filter_Fuction(dataframe, variable, min_range, max_range, number_of_bins):
        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or "Bin_4D" in variable or "Bin_5D" in variable):
            if("sec" in variable):
                gen_variable = gen_variable.replace("_a", "")
            filter_name = "".join([variable, " == ", gen_variable, " && ", variable, " != 0"])
        else:
            bin_size = (max_range - min_range)/number_of_bins
            filter_name = "".join(["""
            // cout<<endl<<"Starting a new line of purity filtering..."<<endl;
            int rec_bin = (""", str(variable),     " - ", str(min_range), ")/", str(bin_size), """;
            int gen_bin = (""", str(gen_variable), " - ", str(min_range), ")/", str(bin_size), """;
            // cout<<endl<<"The reconstructed event (with the value Name_""", str(variable), """ = "<<""",     str(variable), """<<") was found in bin "<<rec_bin<<" (Range = "<<(""", str(min_range), """ + (rec_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (rec_bin + 1)*""", str(bin_size), """)<<")"<<endl;
            // cout<<"The generated event (with the value Name_""",       str(gen_variable), """ = "<<""", str(gen_variable), """<<") was found in bin "<<gen_bin<<" (Range = "<<(""", str(min_range), """ + (gen_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (gen_bin + 1)*""", str(bin_size), """)<<")"<<endl<<endl;
            bool filter_Q = (rec_bin == gen_bin && PID_el != 0 && PID_pip != 0);
            return filter_Q;"""])

        return dataframe.Filter(str(filter_name))
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
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

#     def Multi_Dimensional_Bin_Construction(DF, Variables_To_Combine, Smearing_Q="", Data_Type=datatype, return_option="DF"):
#         # print("".join(["Combining Variables: Multi_Dimensional_Bin_Construction(DF, Variables_To_Combine='", str(Variables_To_Combine), "', Smearing_Q='", str(Smearing_Q), "', Data_Type='", str(Data_Type), "', return_option='", str(return_option), "')"]))
#         # Try to test later in the randomly generated rdataframe (see 'MC_DataFrame_Volume_Calculation.ipynb')
#         # When combining variables, each subsequent entry in the list 'Variables_To_Combine' will be inserted within the previous variable
#             # Therefore, to see the phi_h distribution in a combined Q2-xB-z-pT bin, let Variables_To_Combine = [['Q2-xB bin info'], ['z-pT bin info'], ['phi_h info']]
#             # For the bin info of the Q2-xB/z-pT bins, make sure that the Min_Bin = 0 and Max_Bin = Num_Bin
#             # Note: This function should be able to combine any number of variables, but the rest of the code may not be optimized to combine 4 variables at the same time (rewrite other parts of code if this becomes necessary)
#         DF_Res_Error = False # Helps trigger error message for when this function fails to calculate the variables for the response matrices
#         try:
#             if(DF == "continue"):
#                 return "continue"
#             if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
#                 print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nImproper information was provided to combine multidimensional bins\n", color.END, color.RED, "Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'", color.END]))
#                 if(return_option == "DF"):
#                     return DF
#                 else:
#                     return Variables_To_Combine
#             else:
#                 Vars_Data_Type_Output = [""] if((return_option != "DF_Res") or (Data_Type in ["rdf", "gdf"])) else ["", "_gen"]
#                 for rec_or_gen in Vars_Data_Type_Output:
#                     try:
#                         variable_name_1, Min_Bin_1, Max_Bin_1, Num_Bin_1 = Variables_To_Combine[0]
#                         Bin_Size_1 = (Max_Bin_1 - Min_Bin_1)/Num_Bin_1
#                         Bin_Group_Numbers = Num_Bin_1
#                         if(rec_or_gen == ""):
#                             if((Smearing_Q != "") and ("_smeared" not in variable_name_1)):
#                                 print("".join([color.RED, color.BOLD, "ERROR: MISSING SMEARING OPTION DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
#                                 variable_name_1 = "".join([str(variable_name_1), "_smeared"])
#                             if((Smearing_Q == "") and ("_smeared" in variable_name_1)):
#                                 print("".join([color.RED, color.BOLD, "ERROR: SMEARING OPTION NOT SELECTED DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
#                                 variable_name_1 = str(variable_name_1).replace("_smeared", "")
#                         else:
#                             variable_name_1 = "".join([str(variable_name_1).replace("_smeared", ""), "_gen"])
#                         # Combined_Bin_All = "".join(["""
#                         # int Combined_Bin_Start = ((""", str(variable_name_1), """ - """, str(Min_Bin_1), """)/""", str(Bin_Size_1), """) + 1;
#                         # if(""", str(variable_name_1), """ < """, str(Min_Bin_1), """){
#                         #     // Below binning range
#                         #     Combined_Bin_Start = 0;
#                         # }
#                         # if(""", str(variable_name_1), """ > """, str(Max_Bin_1), """){
#                         #     // Above binning range
#                         #     Combined_Bin_Start = """, str(Num_Bin_1 + 1), """;
#                         # }
#                         # """])
#                         Combined_Bin_All = "".join(["""
#     int Combined_Bin_Final = 0;
#     // int Combined_Bin_Start = ((""", str(variable_name_1), """ - """, str(Min_Bin_1), """)/""", str(Bin_Size_1), """) + 1;
#     int Combined_Bin_Start = ((""",    str(variable_name_1), """ - """, str(Min_Bin_1), """)/""", str(Bin_Size_1), """);
#     if((""", str(variable_name_1), """ < """, str(Min_Bin_1), """) || (""", str(variable_name_1), """ > """, str(Max_Bin_1), """)){
#         // Outside binning range (will only combine events which are within all given binning schemes)
#         Combined_Bin_Final = -1;
#         return Combined_Bin_Final;
#     }
#     Combined_Bin_Final = Combined_Bin_Start;"""])
#                     except:
#                         print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in retriving base variable for new multidimensional bin variable.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   
#                     if(("DF" in return_option) and (rec_or_gen == "")):
#                         try:
#                             if(Smearing_Q != ""):
#                                 DF_Final = smear_frame_compatible(DF, variable_name_1, Smearing_Q)
#                             else:
#                                 DF_Final = DF
#                         except:
#                             print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in smearing.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   
#                     Combined_Bin_Title = "".join(["Combined_", str(variable_name_1)])
#                     for variable_binning in Variables_To_Combine:
#                         variable_name, Min_Bin, Max_Bin, Num_Bin = variable_binning
#                         Bin_Size = (Max_Bin - Min_Bin)/Num_Bin
#                         if(rec_or_gen == ""):
#                             if((Smearing_Q != "") and ("_smeared" not in variable_name)):
#                                 print("".join([color.RED, "ERROR: MISSING (SECONDARY) SMEARING OPTION DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
#                                 variable_name = "".join([str(variable_name), "_smeared"])
#                             if((Smearing_Q == "") and ("_smeared" in variable_name_1)):
#                                 print("".join([color.RED, "ERROR: (SECONDARY) SMEARING OPTION NOT SELECTED DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
#                                 variable_name = str(variable_name).replace("_smeared", "")
#                             if((("_smeared" in variable_name_1) and ("_smeared" not in variable_name)) or (("_smeared" not in variable_name_1) and ("_smeared" in variable_name))):
#                                 print("".join([color.BOLD, color.RED, "/nMAJOR WARNING: COMBINING VARIABLES THAT DO NOT HAVE THE SAME SMEARING OPTION APPLIED (CHECK Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ") MANUALLY)\n", color.END]))
#                         else:
#                             variable_name = "".join([str(variable_name).replace("_smeared", ""), "_gen"])
#                         if(variable_name_1 == variable_name):
#                             # Skip first variable in list
#                             continue
#                         if(("DF" in return_option) and (rec_or_gen == "")):
#                             try:
#                                 if(Smearing_Q != ""):
#                                     DF_Final = smear_frame_compatible(DF_Final, variable_name, Smearing_Q)
#                             except:
#                                 print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in smearing.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   
#                         Combined_Bin_All = "".join([Combined_Bin_All, """
#     int Combined_Add_""", str(variable_name), """ = ((""", str(variable_name), """ - """, str(Min_Bin), """)/""", str(Bin_Size), """);
#     if((""", str(variable_name), """ < """, str(Min_Bin), """) || (""", str(variable_name), """ > """, str(Max_Bin), """)){
#         // Outside binning range (will only combine events which are within all given binning schemes)
#         Combined_Bin_Final = -1;
#         return Combined_Bin_Final;
#     }
#     Combined_Bin_Final += ((""", str(Bin_Group_Numbers), """ + 1)*Combined_Add_""", str(variable_name), """);"""])
#                         Bin_Group_Numbers = (Bin_Group_Numbers + 1)*(Num_Bin + 1)
#                         Combined_Bin_Title = "".join([str(Combined_Bin_Title.replace("_smeared", "")).replace("_gen", ""), "_", str(variable_name)])
#                         if((rec_or_gen != "") and ("_gen" not in Combined_Bin_Title)):
#                             Combined_Bin_Title = "".join([str(Combined_Bin_Title), "_gen"])
#                     Combined_Bin_All = "".join([Combined_Bin_All, """
#     return Combined_Bin_Final;"""])
#                     if(return_option == "DF"):
#                         try:
#                             DF_Final = DF_Final.Define(str(Combined_Bin_Title), str(Combined_Bin_All))
#                             return DF_Final
#                         except:
#                             print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
#                     elif(return_option == "DF_Res"):
#                         try:
#                             # print("".join(["DF_Final = DF_Final.Define(", str(Combined_Bin_Title), ", ", str(Combined_Bin_All), ")"]))
#                             DF_Final = DF_Final.Define(str(Combined_Bin_Title), str(Combined_Bin_All))
#                         except:
#                             print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
#                     else:
#                         return [str(Combined_Bin_Title), -1.5, Bin_Group_Numbers + 1.5, Bin_Group_Numbers + 3]
#         except:
#             print("".join([color.BOLD, color.RED, "\n\nMAJOR ERROR IN Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
#             DF_Res_Error = True
#         if(return_option != "DF_Res" or DF_Res_Error):
#             print("".join([color.BOLD, color.RED, "\n\nMAJOR ERROR IN Multi_Dimensional_Bin_Construction:\nFAILURE TO RETURN ANYTHING", color.END]))
#             return DF
#         else:
#             return DF_Final
        
##########################################################################################################################################################################################
##########################################################################################################################################################################################

#     def Multi_Dim_Bin_Def(DF, Variables_To_Combine, Smearing_Q="", Data_Type=datatype, return_option="DF"):
#         if(DF == "continue"):
#             return "continue"
#         if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
#             print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dim_Bin_Def...\nImproper information was provided to combine multidimensional bins\n", color.END, color.RED, "Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'", color.END]))
#             if(return_option == "DF"):
#                 return DF
#             else:
#                 return Variables_To_Combine
#         Vars_Data_Type_Output = [""] if((return_option != "DF_Res") or (Data_Type in ["rdf", "gdf"])) else ["" if("mear" not in Smearing_Q) else "_smeared", "_gen"]
#         var_name, var_mins, var_maxs, var_bins = zip(*Variables_To_Combine)
#         var_name, var_mins, var_maxs, var_bins = list(var_name), list(var_mins), list(var_maxs), list(var_bins)
#         for list_invert in [var_name, var_mins, var_maxs, var_bins]:
#             list_invert.reverse()
#         Multi_Dim_Bin_Title, combined_bin_formula = {}, {}
#         DF_Final = DF
#         # print("var_name:", var_name, "\nvar_mins:", var_mins, "\nvar_maxs:", var_maxs, "\nvar_bins:", var_bins)
#         for var_type in Vars_Data_Type_Output:
#             Multi_Dim_Bin_Title[var_type] = "Multi_Dim"
#             for ii, var in enumerate(var_name):
#                 Multi_Dim_Bin_Title[var_type] += str("".join(["_", str(var).replace("_smeared", "")])).replace("_gen", "")
#                 if(var_type not in str(var)):
#                     var_name[ii] = "".join([str(var), str(var_type)])
#                 if(var_type in [""]):
#                     var_name[ii] = str((var).replace("_smeared", "")).replace("_gen", "")
#                 else:
#                     var_name[ii] = str((var).replace("_smeared" if("gen" in str(var_type)) else "_gen", ""))
#                 if(str(var_name[ii]) not in list(DF_Final.GetColumnNames()) and var_type in ["_smeared"]):
#                     DF_Final = smear_frame_compatible(DF_Final, str(var_name[ii]), Smearing_Q)
#                 elif(str(var_name[ii]) not in list(DF_Final.GetColumnNames())):
#                     print("".join(["ERROR IN 'Multi_Dim_Bin_Def': Variable '", str(var_name[ii]), "' is not in the DataFrame (check code for errors)"]))
#             Multi_Dim_Bin_Title[var_type] += str(var_type)
#             combined_bin_formula[var_type] = "".join(["int combined_bin", str(var_type), " = "])
#             for ii, var in enumerate(var_name):
#                 if(combined_bin_formula[var_type]  != "".join(["int combined_bin", str(var_type), " = "])):
#                     combined_bin_formula[var_type] += " + "
#                 if("_Bin" not in str(var)):
#                     var_bin_product = str(var_bins[ii])
#                     for jj in range(ii + 1, len(var_name)):
#                         var_bin_product            += "".join(["*", str(var_bins[jj])])
#                     norm_var                        = "".join(["(({0}", str(var_type), " - {1})/({2} - {1}))"]).format(var, var_mins[ii], var_maxs[ii])
#                     combined_bin_formula[var_type] += "".join(["int({0}*{1}) + "]).format(norm_var, var_bin_product)
#                 else:
#                     try:
#                         combined_bin_formula[var_type] += "".join(["(", str(var), str(var_type), "*", str(var_bins[ii + 1]), ")"])
#                     except:
#                         print("ERROR")
#                         combined_bin_formula[var_type] += str(var)
#             combined_bin_formula[var_type] += """1;
#             if("""
#             for ii, var in enumerate(var_name):
#                 combined_bin_formula[var_type] += "".join([str(var), str(var_type), " < ", str(var_mins[ii]), " || ", str(var), str(var_type), " > ", str(var_maxs[ii])])
#                 if(ii != (len(var_name) - 1)):
#                     combined_bin_formula[var_type] += " || "
#             combined_bin_formula[var_type]     += "".join(["){combined_bin", str(var_type), """ = -1;}
#             return combined_bin""", str(var_type), ";"])
#             combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace(" +  + ", " + ")
#             # print(combined_bin_formula[var_type])
#             if(return_option == "DF"):
#                 try:
#                     DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
#                 except:
#                     print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
#             elif(return_option == "DF_Res"):
#                 try:
#                     DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
#                 except:
#                     print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
#             else:
#                 # return [str(Multi_Dim_Bin_Title[var_type]), -1.5, (numpy.prod(var_bins)) + 1.5, (numpy.prod(var_bins)) + 3]
#                 return [str(Multi_Dim_Bin_Title[var_type]), -1.5, (math.prod(var_bins)) + 1.5, (math.prod(var_bins)) + 3]
#         return DF_Final

    def Multi_Dim_Bin_Def(DF, Variables_To_Combine, Smearing_Q="", Data_Type=datatype, return_option="DF"):
        if(DF == "continue"):
            return "continue"
        if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
            print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dim_Bin_Def...\nImproper information was provided to combine multidimensional bins\n", color.END, color.RED, "Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'", color.END]))
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
    #             if((str(var_name[ii]) not in list(DF_Final.GetColumnNames())) and (str(var_name[ii]) not in DF_Final.GetColumnNames())):
    #             if((str(var_name[ii]) not in list(DF_Final.GetColumnNames()))):
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
                    print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
            elif(return_option == "DF_Res"):
                try:
                    DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
                except:
                    print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
            else:
                return [str(Multi_Dim_Bin_Title[var_type]), -1.5, (math.prod(var_bins)) + 1.5, (math.prod(var_bins)) + 3]
        return DF_Final


    
##########################################################################################################################################################################################
##########################################################################################################################################################################################

    def Delta_Matched_DF(dataframe, variable):
        output = "continue"
        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or dataframe == "continue"):
            # Cannot uses these types of variables in this type of histogram
            return "continue"
        else:
            output = dataframe.Define("Delta_Matched_Value", "".join([str(variable), " - ", str(gen_variable)]))

        return output

##########################################################################################################################################################################################
##########################################################################################################################################################################################

    def Delta_Matched_Bin_Calc(Variable, Min_Bin, Max_Bin):
        output = "continue"
        Min_Dif, Max_Dif = (Min_Bin - Max_Bin), (Max_Bin - Min_Bin)
        if("th" in Variable):
            Min_Dif, Max_Dif = -6, 6
        if("Phi" in Variable):
            Min_Dif, Max_Dif = -10, 10
        Num_of_Bins = int((Max_Dif - Min_Dif)/0.005)
        if(Num_of_Bins   < 400):
            Num_of_Bins  = 400
        elif(Num_of_Bins < 200):
            Num_of_Bins  = 200
        elif(Num_of_Bins > 1500):
            Num_of_Bins  = 1500
        elif(Num_of_Bins > 1200):
            Num_of_Bins  = 1200
        elif(Num_of_Bins > 800):
            Num_of_Bins  = 800
        else:
            Num_of_Bins  = 600
        if(((Max_Dif - Min_Dif)/Num_of_Bins) > 1 and (Max_Dif - Min_Dif) < 800):
            Num_of_Bins = int(Max_Dif - Min_Dif)
        output = [Num_of_Bins, Min_Dif, Max_Dif]
        return output
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    ###################################################################################################################################################################
    ###################################################                 Done With Kinematic Binning                 ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################          Defining Helpful Functions for Histograms          ###################################################
    ###################################################################################################################################################################

##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    ###################=========================###################
    ##===============##     Variable Titles     ##===============##
    ###################=========================###################
    
    def variable_Title_name(variable):
        smeared_named, bank_named = '', ''
        if("_smeared" in variable):
            smeared_named = 'yes'
            variable = variable.replace("_smeared", "")
            
        if("_gen" in variable):
            bank_named = 'yes'
            variable = variable.replace("_gen",     "")
        
        output = 'error'    

        if(variable in ['Hx', 'Hy']):
            output = str(variable)       
        if(variable == 'el_E'):
            output = 'E_{el}'
        if(variable == 'pip_E'):
            output = 'E_{#pi^{+}}'
        if(variable == 'el'):
            output = "p_{el}"
        if(variable == 'pip'):
            output = "p_{#pi^{+}}"
        if(variable == 'elth'):
            output = "#theta_{el}"
        if(variable == 'pipth'):
            output = "#theta_{#pi^{+}}"
        if(variable == 'elPhi'):
            output = "#phi_{el}"
        if(variable == 'pipPhi'):
            output = "#phi_{#pi^{+}}"
        if(variable == 'MM'):
            output = "Missing Mass"
        if(variable == 'MM2'):
            output = "Missing Mass^{2}"
        if(variable == 'Q2'):
            output = "Q^{2}"
        if(variable == 'xB'):
            output = "x_{B}"
        if(variable == 'v'):
            output = "#nu (lepton energy loss)"
        if(variable == 's'):
            output = "s (CM Energy^{2})"
        if(variable == 'W'):
            output = "W (Invariant Mass)"
        if(variable == 'y'):
            output = "y (lepton energy loss fraction)"
        if(variable == 'z'):
            output = "z"
        if(variable == 'epsilon'):
            output = "#epsilon"
        if(variable == 'pT'):
            output = "P_{T}"
        if(variable in ['phi_t', 'phi_h']):
            output = "#phi_{h}"
        if(variable == 'xF'):
            output = "x_{F} (Feynman x)"
        if(variable == 'pipx_CM'):
            output = "CM p_{#pi^{+}} in #hat{x}"
        if(variable == 'pipy_CM'):
            output = "CM p_{#pi^{+}} in #hat{y}"
        if(variable == 'pipz_CM'):
            output = "CM p_{#pi^{+}} in #hat{z}"
        if(variable == 'qx_CM'):
            output = "CM p_{q} in #hat{x}"
        if(variable == 'qy_CM'):
            output = "CM p_{q} in #hat{y}"
        if(variable == 'qz_CM'):
            output = "CM p_{q} in #hat{z}"
        if(variable == 'beamX_CM'):
            output = "CM p_{beam} in #hat{x}"
        if(variable == 'beamY_CM'):
            output = "CM p_{beam} in #hat{y}"
        if(variable == 'beamZ_CM'):
            output = "CM p_{beam} in #hat{z}"
        if(variable == 'eleX_CM'):
            output = "CM p_{el} in #hat{x}"
        if(variable == 'eleY_CM'):
            output = "CM p_{el} in #hat{y}"
        if(variable == 'eleZ_CM'):
            output = "CM p_{el} in #hat{z}"
        if(variable == 'event'):
            output = "Event Number"
        if(variable == 'runN'):
            output = "Run Number"
        if(variable == 'ex'):
            output = "Lab p_{el} in #hat{x}"
        if(variable == 'ey'):
            output = "Lab p_{el} in #hat{y}"
        if(variable == 'ez'):
            output = "Lab p_{el} in #hat{z}"
        if(variable == 'px'):
            output = "Lab p_{#pi^{+}} in #hat{x}"
        if(variable == 'py'):
            output = "Lab p_{#pi^{+}} in #hat{y}"
        if(variable == 'pz'):
            output = "Lab p_{#pi^{+}} in #hat{z}"
        if(variable == 'esec'):
            output = "Electron Sector"
        if(variable == 'pipsec'):
            output = "#pi^{+} Sector"
        # if(variable == 'esec_a'):
        if('esec_a' in variable):
            output = "Electron Sector (Angle Def)"
        # if(variable == 'pipsec_a'):
        if('pipsec_a' in variable):
            output = "#pi^{+} Sector (Angle Def)"
        if(variable == 'Q2_xB_Bin'):
            output = "Q^{2}-x_{B} Bin"
        if(variable == 'Q2_xB_Bin_2'):
            output = "Q^{2}-x_{B} Bin (New)"
        if(variable == 'Q2_xB_Bin_Test'):
            output = "Q^{2}-x_{B} Bin (Test)"
        if(variable == 'Q2_xB_Bin_3'):
            output = "Q^{2}-x_{B} Bin (Square)"
        if(variable == 'Q2_xB_Bin_Off'):
            output = "Q^{2}-x_{B} Bin (Off)"
        if(variable == 'Q2_y_Bin'):
            output = "Q^{2}-y Bin"
        if(variable == 'Q2_Y_Bin'):
            output = "Q^{2}-y Bin (New)"
        if(variable == 'z_pT_Bin'):
            output = "z-P_{T} Bin"
        if(variable == 'z_pT_Bin_2'):
            output = "z-P_{T} Bin (New)"
        if(variable == 'z_pT_Bin_Test'):
            output = "z-P_{T} Bin (Test)"
        if(variable == 'z_pT_Bin_3'):
            output = "z-P_{T} Bin (Square)"
        if(variable == 'z_pT_Bin_Off'):
            output = "z-P_{T} Bin (Off)"
        if(variable == 'z_pT_Bin_y_bin'):
            output = "z-P_{T} Bin (y-binning)"
        if(variable == 'z_pT_Bin_Y_bin'):
            output = "z-P_{T} Bin (New y-binning - Testing)"
        if(variable == 'elec_events_found'):
            output = "Number of Electrons Found"
        if(variable == 'Delta_Smear_El_P'):
            output = "#Delta_{Smeared}p_{el}"
        if(variable == 'Delta_Smear_El_Th'):
            output = "#Delta_{Smeared}#theta_{el}"
        if(variable == 'Delta_Smear_El_Phi'):
            output = "#Delta_{Smeared}#phi_{el}"
        if(variable == 'Delta_Smear_Pip_P'):
            output = "#Delta_{Smeared}p_{#pi^{+}}"
        if(variable == 'Delta_Smear_Pip_Th'):
            output = "#Delta_{Smeared}#theta_{#pi^{+}}"
        if(variable == 'Delta_Smear_Pip_Phi'):
            output = "#Delta_{Smeared}#phi_{#pi^{+}}"
        if("Bin_4D" in variable):
            output = "".join(["Combined 4D Bin",         " (Original)" if("OG" in variable) else ""])
        if("Bin_5D" in variable):
            output = "".join(["Combined 5D Bin",         " (Original)" if("OG" in variable) else ""])
        if("Bin_Res_4D" in variable):
            output = "".join(["Q^{2}-x_{B}-z-P_{T} Bin", " (Original)" if("OG" in variable) else ""])
        if("Combined_" in variable or "Multi_Dim" in variable):
            output = "".join(["Combined Binning: ", str(variable.replace("Combined_", ""))]).replace("Multi_Dim_", "")
            
        if(smeared_named == 'yes'):
            output = "".join([output, " (Smeared)"])
            
        if(bank_named == 'yes'):
            output = "".join([output, " (Generated)"])
        
        if(output == 'error'):
            print("".join(["A variable name was not recognized.\nPlease assign a new name for variable = ", str(variable)]))
            output = str(variable)

        return output

    ###################=========================###################
    ##===============##     Variable Titles     ##===============##
    ###################=========================###################
    
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

        if(Data_Type == "udf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el == 0 || PID_pip == 0")

        if(Data_Type == "miss_idf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && (PID_el != 11 || PID_pip != 211)")

        if(Data_Type == "miss_idf_el" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_el != 11")

        if(Data_Type == "miss_idf_pip" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_pip != 211")
            
#         if(Data_Type in ["gen", "mdf"]):
#             DF_Out = DF_Out.Filter("sqrt(MM2_gen) > 1.5")


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
                        DF_Out  = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 2 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                        DF_Out  = filter_Valerii(DF_Out, Cut_Choice)
                    else:
                        DF_Out  = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 2 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                        DF_Out  = filter_Valerii(DF_Out, Cut_Choice)
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
        else:
            # Generated Monte Carlo should not have cuts applied to it (until now...)
#             if(Data_Type in ["gdf", "gen"]):
#                 cutname = "Missing Mass < 1.5 Cut"
#                 if(Titles_or_DF == 'DF'):
#                     if(Data_Type in ["gdf"]):
#                         DF_Out = DF_Out.Filter("sqrt(MM2) > 1.5")
#                     if(Data_Type in ["gen"]):
#                         DF_Out = DF_Out.Filter("sqrt(MM2_gen) > 1.5")
#             else:
            cutname = "No Cuts"
        for sec in range(1, 7, 1):
            if("eS" not in Cut_Choice):
                break
            if("".join(["eS", str(sec), "a"]) in Cut_Choice):
                cutname = "".join([cutname, " (Excluding Sector ", str(sec), " Electrons)"])
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("".join(["esec != ", str(sec)]))
                    if(Data_Type in ["mdf", "pdf", "gen"]):
                        DF_Out  = DF_Out.Filter("".join(["esec_gen != ", str(sec)]))
                break
            if("".join(["eS", str(sec), "o"]) in Cut_Choice):
                cutname = "".join([cutname, " (Sector ", str(sec), " Electrons Only)"])
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("".join(["esec == ", str(sec)]))
                    if(Data_Type in ["mdf", "pdf", "gen"]):
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
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    ###################=======================================###################
    ##===============##   (Other) Histogram Functions Title   ##===============##
    ###################=======================================###################
        
    def Data_Type_Title(Data_Type, Smearing_Q=""):
        Data_Title = "Undefined Data (ERROR)"
        if(Data_Type == 'rdf'):
            Data_Title = "Experimental Data"
        if(Data_Type in ['mdf', 'pdf', 'udf'] or ("miss_idf" in Data_Type)):
            # Data_Title = "".join(["Monte Carlo Data (REC", " - Smeared)" if "smear" in Smearing_Q else ")"])
            Data_Title = "".join(["Monte Carlo Data (REC)"])
        if(Data_Type == 'pdf'):
            Data_Title = Data_Title.replace("REC", "Matched")
        if(Data_Type == 'miss_idf'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified Match")
        if(Data_Type == 'miss_idf_el'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified (Electron) Match")
        if(Data_Type == 'miss_idf_pip'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified (Pi+ Pion) Match")
        if(Data_Type == 'udf'):
            Data_Title = Data_Title.replace("REC", "Unmatched")
        if(Data_Type == 'gdf'):
            Data_Title = "Monte Carlo Data (GEN)"
        if(Data_Type == 'gen'):
            Data_Title = "Monte Carlo Data (GEN - Matched)"

        return Data_Title

    
##########################################################################################################################################################################################

    def Cut_Choice_Title(Cut_Type="no_cut"):
        Cut_Name = "Undefined Cut (ERROR)"
        if("no_cut"   in str(Cut_Type)):
            Cut_Name = "No Cuts"
        if("EDIS"     in str(Cut_Type)):
            Cut_Name = "Exclusive Cuts"
        if("SIDIS"    in str(Cut_Type)):
            Cut_Name = "SIDIS Cuts"
        if("MM"       in str(Cut_Type)):
            Cut_Name = "Cuts with Inverted MM Cut"
        if("Gen"      in str(Cut_Type)):
            Cut_Name = "Cuts with Generated MM Cut"
        if("Exgen"    in str(Cut_Type)):
            Cut_Name = "Cuts with Inverted Generated MM Cut"
        if("Complete" in str(Cut_Type)):
            Cut_Name = "".join(["Complete Set of ", str(Cut_Name)])
        if("eS" in str(Cut_Type)):
            for sec in range(1, 7, 1):
                if("".join(["eS", str(sec), "a"]) in str(Cut_Type)):
                    Cut_Name = "".join([str(Cut_Name), " (Excluding Sector ", str(sec), " Electrons)"])
                if("".join(["eS", str(sec), "o"]) in str(Cut_Type)):
                    Cut_Name = "".join([str(Cut_Name), " (Sector ", str(sec), " Electrons Only)"])
            
        return Cut_Name

##########################################################################################################################################################################################

    def Dimension_Name_Function(Histo_Var_D1, Histo_Var_D2="None", Histo_Var_D3="None"):
        Dimensions_Output = "Variable_Error"
        try:
            Histo_Var_D1_Name = "".join(["Var-D1:'",         str(Histo_Var_D1[0]), "'-[NumBins:", str(Histo_Var_D1[3]), ", MinBin:", str(Histo_Var_D1[1]), ", MaxBin:", str(Histo_Var_D1[2]), "]"])
            Dimensions_Output = Histo_Var_D1_Name
            if(Histo_Var_D2      != "None"):
                Histo_Var_D2_Name = "".join(["Var-D2:'",     str(Histo_Var_D2[0]), "'-[NumBins:", str(Histo_Var_D2[3]), ", MinBin:", str(Histo_Var_D2[1]), ", MaxBin:", str(Histo_Var_D2[2]), "]"])
                if(Histo_Var_D3      != "None"):
                    Histo_Var_D3_Name = "".join(["Var-D3:'", str(Histo_Var_D3[0]), "'-[NumBins:", str(Histo_Var_D3[3]), ", MinBin:", str(Histo_Var_D3[1]), ", MaxBin:", str(Histo_Var_D3[2]), "]"])
                    Dimensions_Output = "".join([str(Histo_Var_D1_Name), "; ", str(Histo_Var_D2_Name), "; ", str(Histo_Var_D3_Name)])
                else:
                    Dimensions_Output = "".join([str(Histo_Var_D1_Name), "; ", str(Histo_Var_D2_Name)])

            Dimensions_Output = (Dimensions_Output.replace(":", "=")).replace("; ", "), (")
            
            # if(Histo_Var_D2 == "None" and Histo_Var_D3 == "None"):
            #     Dimensions_Output = Dimensions_Output.replace("_smeared", "")
            # try:
            #     if(Histo_Var_D2 != "None" and Histo_Var_D3 == "None" and ("smear" in str(Histo_Var_D1[0]) and "smear" in str(Histo_Var_D2[0]))):
            #         Dimensions_Output = Dimensions_Output.replace("_smeared", "")
            # except:
            #     print("".join([color.BOLD, color.RED, "ERROR IN REMOVING '_smeared' FROM VARIABLE NAME:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            
        except:
            print("".join([color.BOLD, color.RED, "ERROR IN DIMENSIONS:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

        return Dimensions_Output

    ###################=======================================###################
    ##===============##    Histogram Functions Title (End)    ##===============##
    ###################=======================================###################
    
    
    ##################################################################################################################################################################
    ###################################################          Done Making the Functions for Histograms          ###################################################
    ###                                              ##------------------------------------------------------------##                                              ###
    ###----------------------------------------------##------------------------------------------------------------##----------------------------------------------###
    ###                                              ##------------------------------------------------------------##                                              ###
    ##################################################################################################################################################################
    ###################################################                    Choices For Graphing                    ###################################################
    ##################################################################################################################################################################
    
    
    ###################################################################
    #####################       Cut Choices       #####################
    

    if(run_Mom_Cor_Code == "yes"):
        print("".join([color.BLUE, color.BOLD, "\nRunning Histograms from Momentum Correction/Smearing Code (i.e., Missing Mass and ∆P Histograms)", color.END]))
        print("".join([color.RED, "NOT Running Default SIDIS Histograms", color.END]))
    else:
        print("".join([color.RED, "\nNOT Running Momentum Correction/Smearing Histograms", color.END]))
        print("".join([color.BLUE, color.BOLD, "Running the Default Histograms for the SIDIS Analysis (i.e., Normal 1D/2D/3D Histograms and/or Unfolding Histograms)", color.END]))

    
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
        
    # # Other than 'no_cut', all of the above cuts can be combined separately by adding them to the str in cut_list as a suffix of another cut
    # # # Example:
        # # cut_list = ["no_cut", "cut_all", "cut_Mom_SIDIS"]
          # # The first two cuts in the above list are the same as describles in entry (1) and (4) in the list above. The 3rd entry is a combination of "Mom" and "SIDIS" where both cuts are applied together (order doesn't matter). This combination can be done with any of the cuts given in the list above (except 'no_cut') and can be done with as many of them as desired (no limits to number of cuts that can be added to one entry).

    # cut_list = ['no_cut', 'cut_Complete', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']
#     cut_list = ['no_cut', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']
    # cut_list = ['no_cut', 'cut_Complete_SIDIS']
    # cut_list = ['cut_Complete_SIDIS']
    
    cut_list = ['no_cut']
    # cut_list.append('no_cut_eS1a')
    # cut_list.append('no_cut_eS1o')
    # cut_list.append('no_cut_eS2o')
    # cut_list.append('no_cut_eS3o')
    # cut_list.append('no_cut_eS4o')
    # cut_list.append('no_cut_eS5o')
    # cut_list.append('no_cut_eS6o')
    if(datatype not in ["gdf"]):
        cut_list.append('cut_Complete_SIDIS')
        # cut_list.append('cut_Complete_SIDIS_eS1a')
        # cut_list.append('cut_Complete_SIDIS_eS1o')
        # cut_list.append('cut_Complete_SIDIS_eS2o')
        # cut_list.append('cut_Complete_SIDIS_eS3o')
        # cut_list.append('cut_Complete_SIDIS_eS4o')
        # cut_list.append('cut_Complete_SIDIS_eS5o')
        # cut_list.append('cut_Complete_SIDIS_eS6o')
        # # cut_list.append('cut_Complete_MM')
        if(run_Mom_Cor_Code == "yes"):
            cut_list.append('cut_Complete_EDIS')
    # if(datatype not in ["rdf"]):
    #     if(datatype not in ["gdf"]):
    #         # cut_list.append('cut_Complete_MM_Gen')
    #         cut_list.append('cut_Complete_SIDIS_Gen')
    #         cut_list.append('cut_Complete_SIDIS_Exgen')
    #     cut_list.append('cut_Gen')
    #     cut_list.append('cut_Exgen')
    print("".join([color.BLUE, color.BOLD, "\nCuts in use: ", color.END]))
    for cuts in cut_list:
        print("".join(["\t(*) ", str(cuts)]))
        
    
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
#     binning_option_list = ["2", "3"]
    binning_option_list = ["Off"]
#     binning_option_list = ["Off", "y_bin"]
    binning_option_list = ["y_bin"]
    binning_option_list = ["Y_bin"]

    # The options ''    or 'Stefan' uses the original binning scheme used by Stefan (may be outdated now based on the option selected)
    # The options '2'   or 'OG'     uses the modified binning schemes developed for this analysis (instead of the binning used by Stefan)
    # The options '3'   or 'Square' uses the modified square Q2-xB binning schemes developed later in this analysis
    # The options 'Off' or 'off'    uses no binning schemes and turns them off by setting their values to always be equal to '1' to improve the runtime when the bins are not needed
    
    
    # # The following are the maximum number of Q2-xB this code recognizes by all of the binning schemes
    # List_of_Q2_xB_Bins_to_include = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # Minimum Default for the binning option 'Off'
    List_of_Q2_xB_Bins_to_include = [-1]
        
    if("2" in binning_option_list or "OG"     in binning_option_list):
        List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8]
        
    if(""  in binning_option_list or "Stefan" in binning_option_list):
        List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
    if("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list):
        # List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # Old version (removed as of 9/27/2023)
        List_of_Q2_xB_Bins_to_include = [-3, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    
    if("3" in binning_option_list or "Square" in binning_option_list):
        List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        
    if("4" in binning_option_list or "y_bin"  in binning_option_list or "y_Bin" in binning_option_list):
        List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        List_of_Q2_xB_Bins_to_include = [-1, 3]
        
    if(run_Mom_Cor_Code == "yes"):
        # # binning_option_list = ["2"]
        # binning_option_list = ["Off"]
        binning_option_list = ["y_bin"]
        List_of_Q2_xB_Bins_to_include = [-1]

        
    # List_of_Q2_xB_Bins_to_include = [-1, 1]
        
    print("")
    if(("Off" in binning_option_list or "off" in binning_option_list)  and ("Q2_xB_Bin_Off" not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_off"   not in list(rdf.GetColumnNames()))):
        print("Binning Scheme --> 'Off'")
        rdf = rdf.Define("Q2_xB_Bin_Off",                                       str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Off")))
        rdf = rdf.Define("z_pT_Bin_Off",                                        str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Off")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_Off_gen",                               str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="Off")))
            rdf = rdf.Define("Q2_xB_Bin_Off_smeared",                           str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="Off")))
            rdf = rdf.Define("z_pT_Bin_Off_gen",                                str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="Off")))
            rdf = rdf.Define("z_pT_Bin_Off_smeared",                            str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="Off")))
    if(("2" in binning_option_list or "OG" in binning_option_list)     and ("Q2_xB_Bin_2"   not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_OG"     not in list(rdf.GetColumnNames()))):
        print("Modified Binning Scheme --> '2'")
        rdf = rdf.Define("Q2_xB_Bin_2",                                         str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="2")))
        rdf = rdf.Define("z_pT_Bin_2",                                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="2")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_2_gen",                                 str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="2")))
            rdf = rdf.Define("Q2_xB_Bin_2_smeared",                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="2")))
            rdf = rdf.Define("z_pT_Bin_2_gen",                                  str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="2")))
            rdf = rdf.Define("z_pT_Bin_2_smeared",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="2")))
    if(("3" in binning_option_list or "Square" in binning_option_list) and ("Q2_xB_Bin_3"   not in list(rdf.GetColumnNames())) and ("Q2_xB_Bin_Square" not in list(rdf.GetColumnNames()))):
        print("New (rectangular) Binning Scheme --> '3'")
        rdf = rdf.Define("Q2_xB_Bin_3",                                         str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="3")))
        rdf = rdf.Define("z_pT_Bin_3",                                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="3")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_xB_Bin_3_gen",                                 str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="3")))
            rdf = rdf.Define("Q2_xB_Bin_3_smeared",                             str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="3")))
            rdf = rdf.Define("z_pT_Bin_3_gen",                                  str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="3")))
            rdf = rdf.Define("z_pT_Bin_3_smeared",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="3")))
    if(("4" in binning_option_list or "y_bin"  in binning_option_list or "y_Bin" in binning_option_list) and ("Q2_y_Bin" not in list(rdf.GetColumnNames()))):
        print("Q2-y Binning Scheme (main) --> 'y_bin'")
        rdf = rdf.Define("Q2_y_Bin",                                            str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="y_bin")))
        rdf = rdf.Define("z_pT_Bin_y_bin",                                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="y_bin")))
        rdf = rdf.Define("Q2_y_z_pT_4D_Bin",                                    str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="")))
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_y_Bin_gen",                                    str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="y_bin")))
            rdf = rdf.Define("Q2_y_Bin_smeared",                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="y_bin")))
            rdf = rdf.Define("z_pT_Bin_y_bin_gen",                              str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="y_bin")))
            rdf = rdf.Define("z_pT_Bin_y_bin_smeared",                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="y_bin")))
            rdf = rdf.Define("Q2_y_z_pT_4D_Bin_gen",                            str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="gen")))
            rdf = rdf.Define("Q2_y_z_pT_4D_Bin_smeared",                        str(Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type="smear")))
    if(("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list) and ("Q2_Y_Bin" not in list(rdf.GetColumnNames()))):
        print("New Q2-y Binning Scheme (Testing) --> 'Y_bin'")
        rdf = rdf.Define("Q2_Y_Bin",                                            str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="",      Bin_Version="Y_bin")))
        rdf = rdf.Define("All_MultiDim_Y_bin",                                  str(z_pT_Bin_Standard_Def_Function(Variable_Type="",       Bin_Version="Y_bin")))
        rdf = rdf.Define("z_pT_Bin_Y_bin",                                      "All_MultiDim_Y_bin[0]")
        # rdf = rdf.Define("Multi_Dim_z_pT_Bin_Y_bin_phi_t",                      "All_MultiDim_Y_bin[1]")
        # rdf = rdf.Define("Multi_Dim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t",             "All_MultiDim_Y_bin[2]")
        if(datatype in ["mdf", "pdf"]):
            rdf = rdf.Define("Q2_Y_Bin_gen",                                    str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="gen",   Bin_Version="Y_bin")))
            rdf = rdf.Define("All_MultiDim_Y_bin_gen",                          str(z_pT_Bin_Standard_Def_Function(Variable_Type="gen",    Bin_Version="Y_bin")))
            rdf = rdf.Define("z_pT_Bin_Y_bin_gen",                              "All_MultiDim_Y_bin_gen[0]")
            # rdf = rdf.Define("Multi_Dim_z_pT_Bin_Y_bin_phi_t_gen",              "All_MultiDim_Y_bin_gen[1]")
            # rdf = rdf.Define("Multi_Dim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t_gen",     "All_MultiDim_Y_bin_gen[2]")
            rdf = rdf.Define("Q2_Y_Bin_smeared",                                str(Q2_xB_Bin_Standard_Def_Function(Variable_Type="smear", Bin_Version="Y_bin")))
            rdf = rdf.Define("All_MultiDim_Y_bin_smeared",                      str(z_pT_Bin_Standard_Def_Function(Variable_Type="smear",  Bin_Version="Y_bin")))
            rdf = rdf.Define("z_pT_Bin_Y_bin_smeared",                          "All_MultiDim_Y_bin_smeared[0]")
            # rdf = rdf.Define("Multi_Dim_z_pT_Bin_Y_bin_phi_t_smeared",          "All_MultiDim_Y_bin_smeared[1]")
            # rdf = rdf.Define("Multi_Dim_Q2_Y_Bin_z_pT_Bin_Y_bin_phi_t_smeared", "All_MultiDim_Y_bin_smeared[2]")
            
            
    
    print("".join([color.BLUE, color.BOLD, "\nBinning Scheme(s) in use: ", color.END]))
    for binning in binning_option_list:
        print("".join(["\t(*) ", "Stefan's binning scheme" if(binning in ["", "Stefan"]) else "Modified binning scheme (developed from Stefan's version)" if(binning in ["2", "OG"]) else "New (rectangular) binning scheme" if(binning in ["3", "Square"]) else "New Q2-y binning scheme" if(binning in ["5", "Y_bin", "Y_Bin"]) else "Q2-y binning scheme (main)" if(binning in ["4", "y_bin", "y_Bin"]) else "".join(["Binning Scheme - ", str(binning)])]))
        
    print("".join([color.BLUE, color.BOLD, "\n(Possible) Q2-xB/Q2-y bins in use: ", color.END, str(List_of_Q2_xB_Bins_to_include)]))
    

    #####################     Bin Choices     #####################
    ###############################################################
    
    # This code is outdated (can remove later)
    # ##################################################################
    # #####################     Sector Choices     #####################
    # # Types_Of_Sectors = ['', 'esec', 'pipsec', 'esec_a', 'pipsec_a']
    # # Types_Of_Sectors = ['', 'esec_a', 'pipsec_a']
    # # Types_Of_Sectors = ['', 'esec', 'pipsec']
    # Types_Of_Sectors = ['']
    # # Types_Of_Sectors = '' --> No Sector Filter
    # # Sector_Numbers = [-1, 1, 2, 3, 4, 5, 6]
    # Sector_Numbers = [-1]
    # # Sector_Numbers = -1 or Types_Of_Sectors = '' --> All Sectors
    # # Sector_Numbers = 0 --> No Sectors (should have no events but if it does, those events exist as errors in the sector definitions)
    # #####################     Sector Choices     #####################
    # ##################################################################
    
        
    
    #####################################################################################################################
    ###############################################     3D Histograms     ###############################################
    

#     # Bin Set Option: 20 bins
# #     Q2_Binning = ['Q2', 0, 12.5, 25]
#     # Bin Set Option: 20 bins (Actual total bins = 27)
#     Q2_Binning = ['Q2', -0.3378, 12.2861, 27]
#     # Bin size: 0.46755 per bin
# #     xB_Binning = ['xB', -0.08, 0.92, 25]
#     # Bin Set Option: 20 bins (Actual total bins = 25)
#     xB_Binning = ['xB', -0.006, 0.8228, 25]
#     # Bin size: 0.03315 per bin
#     z_Binning = ['z', 0.006, 1.014, 28]
#     pT_Binning = ['pT', -0.15, 1.8, 26]
#     y_Binning = ['y', -0.0075, 0.9975, 36]
#     # Bin size: 0.0275
#     phi_t_Binning = ['phi_t', 0, 360, 36]
# #     # Reduced Phi Binning (as of 11-28-2022) -- 15˚ per bin
# #     phi_t_Binning = ['phi_t', 0, 360, 24]

# #     # Bin Set Option: GRC Poster binning
# #     Q2_Binning = ['Q2', 2, 11.351, 5]
# #     # Bin size: 1.8702 per bin
# #     xB_Binning = ['xB', 0.126602, 0.7896, 5]
# #     # Bin size: 0.1325996 per bin
# #     z_Binning = ['z', 0.15, 0.7, 5]
# #     # Bin size: 0.11 per bin
# #     pT_Binning = ['pT', 0.05, 1, 5]
# #     # Bin size: 0.19 per bin
# #     y_Binning = ['y', 0, 1, 5]
# #     # Bin size: 0.2 per bin
# #     phi_t_Binning = ['phi_t', 0, 360, 36]
# #     # Bin size: 10 per bin
    
    # Post-GRC Binning
    Q2_Binning_Old = ['Q2', 1.4805,  11.8705, 20]
    # Bin size: 0.5195 per bin
    xB_Binning_Old = ['xB', 0.08977, 0.82643, 20]
    # Bin size: 0.03683 per bin
    z_Binning_Old  = ['z',  0.11944, 0.73056, 20]
    # Bin size: 0.03056 per bin
    pT_Binning_Old = ['pT', 0,       1.05,    20]
    # Bin size: 0.05 per bin
    y_Binning_Old  = ['y',  0,       1,       20]
    # Bin size: 0.05 per bin

#     # Post-DNP Binning
#     Q2_Binning    = ['Q2',     1.48,  11.87,  20]
#     # Bin size: 0.5195 per bin
#     xB_Binning    = ['xB',     0.09,  0.826,  20]
#     # Bin size: 0.0368 per bin
#     z_Binning     = ['z',      0.119, 0.731,  20]
#     # Bin size: 0.0306 per bin
#     pT_Binning    = ['pT',     0,     1.05,   20]
#     # Bin size: 0.05 per bin
    y_Binning     = ['y',      0,     1,      20]
    # Bin size: 0.05 per bin
    
#     phi_t_Binning = ['phi_t',  0,     360,    36]
#     # Bin size: 10 per bin
    
    phi_t_Binning = ['phi_t',  0,     360,    24]
    # Bin size: 15 per bin
    
#     MM_Binning    = ['MM',     0,     3.5,   500]
#     # Bin size: 0.007 per bin
#     W_Binning     = ['W',      0,     6,     200]
#     # Bin size: 0.03 per bin
    
    # Binning_4D    = ['Bin_4D', -1.5,  303.5, 305]
    # Binning_4D_OG = ['Bin_4D_OG', -1.5, 353.5, 355]
    # Binning_5D  = ['Bin_5D', -1.5, 11625.5, 11627]
    # Binning_5D_OG = ['Bin_5D_OG', -1.5, 13525.5, 13527]
    
#     El_Binning      = ['el',    0, 8,   200]
#     El_Th_Binning   = ['elth',  0, 40,  200]
#     El_Phi_Binning  = ['elPhi', 0, 360, 200]
    
#     Pip_Binning     = ['pip',    0, 6,   200]
#     Pip_Th_Binning  = ['pipth',  0, 40,  200]
#     Pip_Phi_Binning = ['pipPhi', 0, 360, 200]
    
    
    El_Binning      = ['el',    0, 8,   100]
    El_Th_Binning   = ['elth',  0, 40,  100]
    El_Phi_Binning  = ['elPhi', 0, 360, 100]
    
    Pip_Binning     = ['pip',    0, 6,   100]
    Pip_Th_Binning  = ['pipth',  0, 40,  100]
    Pip_Phi_Binning = ['pipPhi', 0, 360, 100]
     
#     # New 2023 2D Binning
#     Q2_Binning = ['Q2', 1.48,  11.87, 100]
#     # Bin size: 0.1039  per bin
#     xB_Binning = ['xB', 0.09,  0.826, 100]
#     # Bin size: 0.00736 per bin
#     z_Binning  = ['z',  0.017, 0.935, 100]
#     # Bin size: 0.00918 per bin
#     pT_Binning = ['pT', 0,     1.26,  120]
#     # Bin size: 0.0105 per bin
    
    # # April 20 2023 2D Binning
    # Q2_Binning = ['Q2', 1.48,  11.87, 50]
    # # Bin size: 0.2078  per bin
    # xB_Binning = ['xB', 0.09,  0.826, 50]
    # # Bin size: 0.01472 per bin
    # z_Binning  = ['z',  0.017, 0.935, 50]
    # # Bin size: 0.01836 per bin
    # pT_Binning = ['pT', 0,     1.26,  60]
    # # Bin size: 0.021 per bin
    
    # # June 23 2023 2D Binning
    # z_Binning  = ['z',  0.01, 0.92, 91]
    # # Bin size: 0.01 per bin
    # pT_Binning = ['pT', 0,    1.25, 125]
    # # Bin size: 0.01 per bin
    
#     # New (September 6 2023) 2D Binning
#     z_Binning  = ['z',  0, 1.20, 120]
#     # Bin size: 0.01 per bin
#     pT_Binning = ['pT', 0, 1.50, 150]
#     # Bin size: 0.01 per bin

    # New (September 27 2023) 2D Binning
    z_Binning  = ['z',  0, 1.20, 120]
    # Bin size: 0.01 per bin
    pT_Binning = ['pT', 0, 2.00, 200]
    # Bin size: 0.01 per bin
    
    # Q2_Binning_Old = ['Q2', 0.0, 12.5, 25]
    # # Bin size: 0.5 per bin
    # xB_Binning_Old = ['xB', -0.003,  0.997, 25]
    # # Bin size: 0.04 per bin
    
    
    # New (May 26 2023) 2D Binning
    # Q2_Binning = ['Q2', 1.154,  12.434, 80]
    # # Bin size: 0.141  per bin
    # y_Binning  = ['y',      0,       1, 80]
    # # Bin size: 0.0125 per bin
    xB_Binning = ['xB', 0.09,  0.826, 50]
    # Bin size: 0.01472 per bin



    # New (September 27 2023) 2D Binning
    Q2_Binning = ['Q2', 0, 14, 280]
    # Bin size: 0.05  per bin
    y_Binning  = ['y',  0,  1, 100]
    # Bin size: 0.01 per bin
    
#     MM_Binning    = ['MM',  0,     3.5, 50]
    MM_Binning    = ['MM',  0,     4.2, 60]
    # Bin size: 0.07 per bin
    W_Binning     = ['W', 0.9,     5.1, 14]
    # Bin size: 0.3 per bin
    
    Q2_y_Binning = ['Q2_y_Bin', -0.5,  18.5, 19]
    # There are 17 Bins (extra bins are for overflow/empty space in histograms)
    
    # Q2_y_z_pT_Binning = ['Q2_y_z_pT_4D_Bin', -0.5,  566.5, 567]
    # # There are 567 Bins (extra bins are for overflow/empty space in histograms)
    
    # New 4D bins as of 7-5-2023
    Q2_y_z_pT_Binning = ['Q2_y_z_pT_4D_Bin', -0.5,  506.5, 507]
    # There are 506 Bins (extra bins are for overflow/empty space in histograms)
    
    # Q2_Y_Binning = ['Q2_Y_Bin', -0.5,  14.5, 15]
    # # There are 13 Bins (extra bins are for overflow/empty space in histograms)
    
    # New as of 9/27/2023
    Q2_Y_Binning = ['Q2_Y_Bin', -0.5,  40.5, 41]
    # There are 17 Main Bins + 22 Migration bins (Total = 39)
    
    
    Hx_Binning = ['Hx', -400, 400, 800]
    Hy_Binning = ['Hy', -400, 400, 800]

    
    # List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, MM_Binning, ['el', 0, 10, 200], ['pip', 0, 8, 200], phi_t_Binning, Binning_4D, W_Binning]
#     List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, phi_t_Binning]
    
#     List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning]
#     List_of_Quantities_1D = [Q2_Binning_Old, xB_Binning_Old, z_Binning_Old, pT_Binning_Old, phi_t_Binning]
    List_of_Quantities_1D = [phi_t_Binning]
#     List_of_Quantities_1D = [Q2_Binning_Old, xB_Binning_Old]
#     List_of_Quantities_1D = [phi_t_Binning, Q2_Binning_Old, xB_Binning_Old]

#     List_of_Quantities_1D = [phi_t_Binning, Q2_y_Binning]
    
#     List_of_Quantities_1D = [phi_t_Binning, MM_Binning, W_Binning]

    List_of_Quantities_1D = [phi_t_Binning, MM_Binning]
    
    List_of_Quantities_1D = [Q2_Y_Binning, MM_Binning]
    
    List_of_Quantities_1D = [phi_t_Binning]
    
    # List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['xB', 0, 0.8, 200]], [['y', 0, 1, 200], ['xB', 0, 0.8, 200]], [['z', 0, 1, 200], ['pT', 0, 1.6, 200]], [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]
    # List_of_Quantities_2D = [[Q2_Binning,         xB_Binning],          [y_Binning,        xB_Binning],          [z_Binning,        pT_Binning],          [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]
#     List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [y_Binning, xB_Binning], [z_Binning, pT_Binning], [El_Binning, El_Th_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
    
    # Reduced Variable Options
    # List_of_Quantities_1D = [Q2_Binning,  xB_Binning,  z_Binning,  pT_Binning, phi_t_Binning]
#     List_of_Quantities_1D = [Q2_Binning, El_Binning, El_Th_Binning, El_Phi_Binning, Pip_Binning, Pip_Th_Binning, Pip_Phi_Binning, phi_t_Binning]
    # List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [z_Binning, pT_Binning]]
    List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [z_Binning, pT_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
#     List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [z_Binning, pT_Binning]]
    
    # List_of_Quantities_2D         = [[['Q2',         0, 12, 200], ['xB',         0, 0.8, 200]], [['y',         0, 1, 200], ['xB',         0, 0.8, 200]], [['z',         0, 1, 200], ['pT',         0, 1.6, 200]], [['el',         0, 8, 200], ['elth',         0, 40, 200]], [['elth',         0, 40, 200], ['elPhi',         0, 360, 200]], [['pip',         0, 6, 200], ['pipth',         0, 40, 200]], [['pipth',         0, 40, 200], ['pipPhi',         0, 360, 200]]]
    # List_of_Quantities_2D         = [[['Q2',         0, 12, 200], ['xB',         0, 0.8, 200]], [['z',         0, 1, 200], ['pT',         0, 1.6, 200]], [['y',         0, 1, 200], ['xF',         -1, 1, 200]], [['el',         0, 8, 200], ['elth',         0, 40, 200]], [['pip',         0, 6, 200], ['pipth',         0, 40, 200]]]

    
    
    # List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [Q2_Binning, y_Binning], [z_Binning, pT_Binning]]
    # List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [Q2_Binning, y_Binning], [z_Binning, pT_Binning], [MM_Binning, W_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
#     List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [Q2_Binning, y_Binning], [Q2_Binning, W_Binning], [W_Binning, y_Binning], [y_Binning, xB_Binning], [z_Binning, pT_Binning], [MM_Binning, W_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
#     List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [Q2_Binning, y_Binning], [z_Binning, pT_Binning], [MM_Binning, W_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
    
    List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [Q2_Binning, y_Binning], [z_Binning, pT_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
    
    # # List_of_Quantities_2D = [[Q2_Binning, y_Binning], [z_Binning, pT_Binning], [El_Phi_Binning, phi_t_Binning], [Pip_Phi_Binning, phi_t_Binning]]
    # List_of_Quantities_2D = [[Q2_Binning, y_Binning], [z_Binning, pT_Binning], [El_Phi_Binning, phi_t_Binning], [Pip_Phi_Binning, phi_t_Binning], [["esec", -0.5, 7.5, 8], phi_t_Binning], [["pipsec", -0.5, 7.5, 8], phi_t_Binning], [El_Binning, phi_t_Binning], [El_Th_Binning, phi_t_Binning], [Pip_Binning, phi_t_Binning], [Pip_Th_Binning, phi_t_Binning]]

    # List_of_Quantities_2D = [[El_Phi_Binning, phi_t_Binning], [Pip_Phi_Binning, phi_t_Binning], [["esec", -0.5, 7.5, 8], phi_t_Binning], [["pipsec", -0.5, 7.5, 8], phi_t_Binning]]
    

    
    List_of_Quantities_3D = [[Q2_Binning, xB_Binning, phi_t_Binning],  [Q2_Binning, y_Binning, phi_t_Binning], [Q2_Binning, xB_Binning, Pip_Phi_Binning], [Q2_Binning, y_Binning, Pip_Phi_Binning], [Q2_Binning, xB_Binning, Pip_Binning], [Q2_Binning, y_Binning, Pip_Binning]]
    List_of_Quantities_3D = [[El_Binning, Pip_Binning, phi_t_Binning], [El_Th_Binning, Pip_Th_Binning, phi_t_Binning], [El_Phi_Binning, Pip_Phi_Binning, phi_t_Binning]]
    
    List_of_Quantities_3D = [[Hx_Binning, Hy_Binning, El_Phi_Binning]]
    
    # # # 1D histograms are turned off with this option
    # List_of_Quantities_1D = []

    # # # 2D histograms are turned off with this option
    # List_of_Quantities_2D = []
    
    # # 3D histograms are turned off with this option
    List_of_Quantities_3D = []
    
    
    if(run_Mom_Cor_Code == "yes"):
        List_of_Quantities_1D, List_of_Quantities_2D, List_of_Quantities_3D = [], [], []
    
    Alert_of_Response_Matricies = True
    
    if(len(List_of_Quantities_1D) == 0):
        print("".join([color.RED,  color.BOLD, "\nNot running 1D histograms...",     color.END]))
    else:
        print("".join([color.BLUE, color.BOLD, "\n1D Histograms Selected Include: ", color.END]))
        for histo_1D in List_of_Quantities_1D:
            print("".join(["\t(*) ", str(histo_1D).replace(",", ",\t")]))
    
    
    if(len(List_of_Quantities_2D) == 0):
        print("".join([color.RED,  color.BOLD, "\nNot running 2D histograms...",     color.END]))
    else:
        print("".join([color.BLUE, color.BOLD, "\n2D Histograms Selected Include: ", color.END]))
        for histo_2D in List_of_Quantities_2D:
            print("".join(["\t(*) ", str(histo_2D).replace(",", ",\t")]))
            
            
    if(len(List_of_Quantities_3D) == 0):
        print("".join([color.RED,  color.BOLD, "\nNot running 3D histograms...",     color.END]))
    else:
        print("".join([color.BLUE, color.BOLD, "\n3D Histograms Selected Include: ", color.END]))
        for histo_3D in List_of_Quantities_3D:
            print("".join(["\t(*) ", str(histo_3D)]))
    
    smearing_options_list = ["", "smear"]
    # smearing_options_list = ["smear"]
    smearing_options_list = [""]
    
    if(datatype in ["rdf", "gdf"]):
        # Do not smear data or generated MC
        for ii in smearing_options_list:
            if("smear" in ii):
                smearing_options_list.remove(ii)
                
    if(("ivec" in smearing_function) and ("smear" in smearing_options_list)):
        print("".join([color.BLUE, color.BOLD, "\nRunning ", "Modified Smearing Funtion" if("Simple Smearing Factor" not in smearing_function) else "".join(["Simple Smearing Factor (", str(smear_factor), ")"]), color.END]))
    elif("smear" in smearing_options_list):
        print("".join([color.BLUE, color.BOLD, "\nRunning FX's Smearing Funtion", color.END]))
    else:
        print("".join([color.RED, "\nNot Smearing...", color.END]))
    
    
    def Print_Progress(Total, Increase, Rate):
        if((Rate == 1) or (((Total+Increase)%Rate) == 0) or (Rate < Increase) or ((Rate-((Total)%Rate)) < Increase)):
            print("".join([str(Total+Increase), "\tHistograms Have Been Made..."]))
    
    
    ##############################################################     End of Choices For Graphing     ##############################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ###########################################################     Graphing Results + Final ROOT File     ##########################################################
    
    ###########################################################
    #################     Final ROOT File     #################
    
    # File to be saved
    if(str(file_location) != 'time' and output_type == "histo"):
        ROOT_File_Output = ROOT.TFile(str(ROOT_File_Output_Name), 'recreate')
        print("\nFinal ROOT file has been created...")
    
    #################     Final ROOT File     #################
    ###########################################################
    
    if(output_type in ["histo", "time"]):
        Histograms_All = {}
        count_of_histograms = 0
        print("".join([color.BOLD, color.BLUE, "\n\nMaking Histograms...\n", color.END]))

######################################################################
##=====##=====##=====##    Top of Main Loop    ##=====##=====##=====##
######################################################################

##======##     Data-Type Loop      ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
        # datatype_list = ["mdf", "pdf", "gen"] if(datatype == "pdf") else ["mdf", "gen"] if(datatype in ["mdf"]) else [datatype]
        datatype_list = ["mdf", "pdf", "gen"] if(datatype == "pdf") else [datatype]
    
        for Histo_Data in datatype_list:

##======##======##     Cut Loop    ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
            for Histo_Cut in cut_list:

                if(Histo_Data == "gdf" and Histo_Cut not in ["no_cut", "cut_Gen", "cut_Exgen", "no_cut_eS1a", "no_cut_eS1o", "no_cut_eS2a", "no_cut_eS2o", "no_cut_eS3a", "no_cut_eS3o", "no_cut_eS4a", "no_cut_eS4o", "no_cut_eS5a", "no_cut_eS5o", "no_cut_eS6a", "no_cut_eS6o"]):
                    # Do not cut data from the MC GEN files
                    continue

##======##======##======##     Smearing Loop       ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                for Histo_Smear in smearing_options_list:

                    if(Histo_Data not in ["mdf", "pdf"] and "smear" in Histo_Smear):
                        # Do not smear data that is not from the MC REC files
                        continue

##======##======##======##======##     Binning Loop        ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                    for Binning in binning_option_list:

                        Histo_Binning = [Binning, "All", "All"]
                        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"

                        if("Off" in Binning or "off" in Binning):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_Off"]),            "".join([z_pT_Bin_Filter_str, "_Off"])
                        elif("2" in Binning or "OG" in Binning):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]),              "".join([z_pT_Bin_Filter_str, "_2"])
                        elif("3" in Binning or "Square" in Binning):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_3"]),              "".join([z_pT_Bin_Filter_str, "_3"])
                        elif("Test" in Binning):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_Test"]),           "".join([z_pT_Bin_Filter_str, "_Test"])
                        elif(Binning in ["4", "y_bin", "y_Bin"]):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_y_Bin", "z_pT_Bin_y_bin"
                        elif(Binning in ["5", "Y_bin", "Y_Bin"]):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_Y_Bin", "z_pT_Bin_Y_bin"
                        elif(Binning not in ["", "Stefan"]):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_", str(Binning)]), "".join([z_pT_Bin_Filter_str, "_", str(Binning)])
                        else:
                            print("\n\nERROR\n\n")

                        Variable_Loop    = copy.deepcopy(List_of_Quantities_1D)
                        Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)
                        Variable_Loop_3D = copy.deepcopy(List_of_Quantities_3D)

                        if("smear" in Histo_Smear):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])
                            Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                            for list1 in Variable_Loop:
                                if(len(list1) == 4):
                                    list1[0] = "".join([str(list1[0]), "_smeared" if("_smeared" not in str(list1[0])) else ""])
                                else:
                                    # Smearing Combined 1D Variables
                                    for combined_vars in list1:
                                        combined_vars[0] = "".join([str(combined_vars[0]), "_smeared" if("_smeared" not in str(combined_vars[0])) else ""])

                            Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)
                            for list2 in Variable_Loop_2D:
                                list2[0][0] = "".join([str(list2[0][0]), "_smeared" if("_smeared" not in str(list2[0][0])) else ""])
                                list2[1][0] = "".join([str(list2[1][0]), "_smeared" if("_smeared" not in str(list2[1][0])) else ""])
                                
                            Variable_Loop_3D = copy.deepcopy(List_of_Quantities_3D)
                            for list3 in Variable_Loop_3D:
                                list3[0][0] = "".join([str(list3[0][0]), "_smeared" if("_smeared" not in str(list3[0][0])) else ""])
                                list3[1][0] = "".join([str(list3[1][0]), "_smeared" if("_smeared" not in str(list3[1][0])) else ""])
                                list3[2][0] = "".join([str(list3[2][0]), "_smeared" if("_smeared" not in str(list3[2][0])) else ""])

                        if("gen" in Histo_Data):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
                            Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                            for list1 in Variable_Loop:
                                if(len(list1) == 4):
                                    list1[0] = "".join([str(list1[0]), "_gen" if("_gen" not in str(list1[0])) else ""])
                                else:
                                    # Matched Gen Combined 1D Variables
                                    for combined_vars in list1:
                                        combined_vars[0] = "".join([str(combined_vars[0]), "_gen" if("_gen" not in str(combined_vars[0])) else ""])
                            Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)
                            for list2 in Variable_Loop_2D:
                                list2[0][0] = "".join([str(list2[0][0]), "_gen" if("_gen" not in str(list2[0][0])) else ""])
                                list2[1][0] = "".join([str(list2[1][0]), "_gen" if("_gen" not in str(list2[1][0])) else ""])
                                
                            Variable_Loop_3D = copy.deepcopy(List_of_Quantities_3D)
                            for list3 in Variable_Loop_3D:
                                list3[0][0] = "".join([str(list3[0][0]), "_gen" if("_gen" not in str(list3[0][0])) else ""])
                                list3[1][0] = "".join([str(list3[1][0]), "_gen" if("_gen" not in str(list3[1][0])) else ""])
                                list3[2][0] = "".join([str(list3[2][0]), "_gen" if("_gen" not in str(list3[2][0])) else ""])


##======##======##======##======##======##     Histogram Option Selection  ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##

                        # histo_options = ["Normal", "Response_Matrix", "Response_Matrix_Normal"]
                        # histo_options = ["Normal", "Response_Matrix_Normal"]
                        # histo_options = ["Response_Matrix_Normal"]
            
                        if(Binning in ["2", "OG", "Off", "off", "4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]):
                            histo_options = ["Normal", "Response_Matrix_Normal"]
                        else:
                            histo_options = ["Normal"]
                            
                        if(len(List_of_Quantities_1D) == 0):
                            if(Alert_of_Response_Matricies):
                                print(color.BOLD, color.BLUE, "\nResponse Matrix Code for Unfolding has been turned off...\n", color.END)
                                Alert_of_Response_Matricies = False
                            histo_options = ["Normal"]
            
                        # # # All options off (will still allow the Momentum Correction plots to run)
                        # histo_options = []

                        # # Types of Histogram Groups (Histo_Group)
                          # # (*) "Normal"                 --> Makes normal 1D and 2D histograms
                          # # (*) "Response_Matrix"        --> Makes a 2D Response Matrix (or equivalent 1D histogram) using the Kinematic Bin Number plotted on each axis
                          # # (*) "Response_Matrix_Normal" --> Makes a 2D Response Matrix (or equivalent 1D histogram) using the Kinematic variable's regular value plotted on each axis (the plotted values will not necessarily be interger values as they would be in the other Response Matrix option)
                          # # (*) "Mom_Cor_Code"           --> Makes the plots used for Momentum Corrections/Smearing Functions

                        if(Histo_Data == 'pdf'):
                            histo_options = ["Has_Matched"]
                            histo_options.append("Bin_Purity")
                            histo_options.append("Delta_Matched")
                            # Meaning of the above options:
                                # # (*) 'Has_Matched'   --> Same as "Normal" but filters unmatched events
                                # # (*) 'Bin_Purity'    --> Filters events in which the reconstructed bin is different from the generated bin
                                # # (*) 'Delta_Matched' --> Makes histograms which plot the difference between the reconstructed and generated (∆val) versus the reconstructed value
                        elif(Histo_Data == "gen"):
                            histo_options = ["Normal"]
                            # Running 'Response_Matrix' options is unnecessary for the matched generated plots (only useful for 2D (or 1D) histograms)

                        if(run_Mom_Cor_Code == "yes" and Histo_Data not in ['pdf', 'gen', 'gdf']):
                            histo_options.append("Mom_Cor_Code")
                            # "Mom_Cor_Code" --> Makes the plots used for Momentum Corrections/Smearing Functions
                            
                        if(run_Mom_Cor_Code == "yes"):
                            histo_options = ["Normal"]
                            histo_options = []
                            if(Histo_Data not in ['pdf', 'gen', 'gdf']):
                                histo_options.append("Mom_Cor_Code")
                                
##======##======##======##======##======##     Histogram Option Loop       ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                        for Histo_Group in histo_options:
                            Histo_Group_Name   = "".join(["Histo-Group:'",  str(Histo_Group), "'"])
                            Histo_Data_Name    = "".join(["Data-Type:'",    str(Histo_Data),  "'"])
                            Histo_Cut_Name     = "".join(["Data-Cut:'",     str(Histo_Cut),   "'"])
                            Histo_Smear_Name   = "".join(["Smear-Type:'",   str(Histo_Smear), "'"])
                            Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-(Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), ")"])

##################################################=================================================##################################################################################################################################
##======##======##======##======##======##======##     Momentum Correction/Smearing Histograms     ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=================================================##################################################################################################################################
                            if(Histo_Group == "Mom_Cor_Code"):

                                # Removed the "_smeared" from all variable names as of 11-29-2022
                                Histo_Var_Dp_Ele_Dimension      = ['Delta_Pel_Cors',       -0.75, 0.75, 125]
                                Histo_Var_Dp_Pip_Dimension      = ['Delta_Ppip_Cors',      -0.75, 0.75, 125]
                                Histo_Var_DTheta_Ele_Dimension  = ['Delta_Theta_el_Cors',  -0.75, 0.75, 125]
                                Histo_Var_DTheta_Pip_Dimension  = ['Delta_Theta_pip_Cors', -0.75, 0.75, 125]
                                Histo_Var_MM_Dimension          = ['MM',                       0, 3.5,  350]
                                Histo_Var_Ele_Dimension         = ['el',                       0, 10,   100]
                                Histo_Var_Pip_Dimension         = ['pip',                      0, 8,    100]
                                Histo_Var_Ele_Theta_Dimension   = ['elth',                     0, 40,   100]
                                Histo_Var_Pip_Theta_Dimension   = ['pipth',                    0, 40,   100]
                                Histo_Var_Ele_Phi_Dimension     = ['elPhi',                    0, 360,  360]
                                Histo_Var_Pip_Phi_Dimension     = ['pipPhi',                   0, 360,  360]
                                
                                # Histo_Var_DP_Ele_SF_Dimension   = ['DP_el_SF',                -5, 5,    500]
                                # Histo_Var_DP_Pip_SF_Dimension   = ['DP_pip_SF',               -5, 5,    500]
                                
                                Histo_Var_DP_Ele_SF_Dimension   = ['DP_el_SF',              -0.8, 0.2, 1000]
                                Histo_Var_DP_Pip_SF_Dimension   = ['DP_pip_SF',             -0.8, 0.2, 1000]
                                
                                if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                    Histo_Var_Dele_SF_Dimension = ['Dele_SF',                  0, 2,    200]
                                    Histo_Var_Dpip_SF_Dimension = ['Dpip_SF',                  0, 2,    200]
                                

                            ###############################################################
                            ##==========##     Correction Histogram ID's     ##==========##
                            ###############################################################

                                Mom_Cor_Histo_Name_Main = ((("".join(["((", "), (".join([Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name])])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                Mom_Cor_Histo_Name_MM_Ele            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_MM_Dimension,         Histo_Var_D2=Histo_Var_Ele_Dimension)),       "))"])
                                Mom_Cor_Histo_Name_MM_Pip            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_MM_Dimension,         Histo_Var_D2=Histo_Var_Pip_Dimension)),       "))"])

                                Mom_Cor_Histo_Name_DP_Ele            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Ele_Dimension,     Histo_Var_D2=Histo_Var_Ele_Dimension)),       "))"])
                                Mom_Cor_Histo_Name_DP_Pip            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Pip_Dimension,     Histo_Var_D2=Histo_Var_Pip_Dimension)),       "))"])
                                
                                Mom_Cor_Histo_Name_DP_Ele_Theta      = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Ele_Dimension,     Histo_Var_D2=Histo_Var_Ele_Theta_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DP_Pip_Theta      = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Pip_Dimension,     Histo_Var_D2=Histo_Var_Pip_Theta_Dimension)), "))"])

                                Mom_Cor_Histo_Name_DTheta_Ele        = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Dimension)),       "))"])
                                Mom_Cor_Histo_Name_DTheta_Pip        = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Dimension)),       "))"])

                                Mom_Cor_Histo_Name_DTheta_Ele_Theta  = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Theta_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DTheta_Pip_Theta  = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Theta_Dimension)), "))"])

                                Mom_Cor_Histo_Name_MM_DP_Ele         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=['elPhi_Local',  -40, 40, 20],  Histo_Var_D2=Histo_Var_MM_Dimension,        Histo_Var_D3=Histo_Var_Dp_Ele_Dimension)),           "))"])
                                Mom_Cor_Histo_Name_MM_DP_Pip         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=['pipPhi_Local', -40, 40, 20],  Histo_Var_D2=Histo_Var_MM_Dimension,        Histo_Var_D3=Histo_Var_Dp_Pip_Dimension)),           "))"])
                                
                                Mom_Cor_Histo_Name_Angle_Ele         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Ele_Theta_Dimension,  Histo_Var_D2=Histo_Var_Ele_Phi_Dimension,   Histo_Var_D3=Histo_Var_Ele_Dimension)),              "))"])
                                Mom_Cor_Histo_Name_Angle_Pip         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Pip_Theta_Dimension,  Histo_Var_D2=Histo_Var_Pip_Phi_Dimension,   Histo_Var_D3=Histo_Var_Pip_Dimension)),              "))"])
                                
                                Mom_Cor_Histo_Name_DP_Ele_Theta_SF   = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Ele_SF_Dimension,  Histo_Var_D2=Histo_Var_Ele_Dimension,       Histo_Var_D3=Histo_Var_Ele_Theta_Dimension)),        "))"])
                                Mom_Cor_Histo_Name_DP_Pip_Theta_SF   = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Pip_SF_Dimension,  Histo_Var_D2=Histo_Var_Pip_Dimension,       Histo_Var_D3=Histo_Var_Pip_Theta_Dimension)),        "))"])
                                # Mom_Cor_Histo_Name_DP_Ele_SF         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Ele_SF_Dimension,  Histo_Var_D2=Histo_Var_Ele_Dimension)),       "))"])
                                # Mom_Cor_Histo_Name_DP_Pip_SF         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Pip_SF_Dimension,  Histo_Var_D2=Histo_Var_Pip_Dimension)),       "))"])
                                # Mom_Cor_Histo_Name_DP_Ele_Phi_SF     = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Ele_SF_Dimension,  Histo_Var_D2=['elPhi_Local',  -40, 40, 20])), "))"])
                                # Mom_Cor_Histo_Name_DP_Pip_Phi_SF     = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Pip_SF_Dimension,  Histo_Var_D2=['pipPhi_Local', -40, 40, 20])), "))"])
                                # Mom_Cor_Histo_Name_DP_Ele_Theta_SF   = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Ele_SF_Dimension,  Histo_Var_D2=Histo_Var_Ele_Theta_Dimension)), "))"])
                                # Mom_Cor_Histo_Name_DP_Pip_Theta_SF   = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DP_Pip_SF_Dimension,  Histo_Var_D2=Histo_Var_Pip_Theta_Dimension)), "))"])
                                
                                Mom_Cor_Histo_Name_MM_Ele            = Mom_Cor_Histo_Name_MM_Ele.replace("; ",           "), ")
                                Mom_Cor_Histo_Name_MM_Pip            = Mom_Cor_Histo_Name_MM_Pip.replace("; ",           "), ")
                                Mom_Cor_Histo_Name_DP_Ele            = Mom_Cor_Histo_Name_DP_Ele.replace("; ",           "), ")
                                Mom_Cor_Histo_Name_DP_Pip            = Mom_Cor_Histo_Name_DP_Pip.replace("; ",           "), ")
                                Mom_Cor_Histo_Name_DP_Ele_Theta      = Mom_Cor_Histo_Name_DP_Ele_Theta.replace("; ",     "), ")
                                Mom_Cor_Histo_Name_DP_Pip_Theta      = Mom_Cor_Histo_Name_DP_Pip_Theta.replace("; ",     "), ")
                                Mom_Cor_Histo_Name_DTheta_Ele        = Mom_Cor_Histo_Name_DTheta_Ele.replace("; ",       "), ")
                                Mom_Cor_Histo_Name_DTheta_Pip        = Mom_Cor_Histo_Name_DTheta_Pip.replace("; ",       "), ")
                                Mom_Cor_Histo_Name_DTheta_Ele_Theta  = Mom_Cor_Histo_Name_DTheta_Ele_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DTheta_Pip_Theta  = Mom_Cor_Histo_Name_DTheta_Pip_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_Angle_Ele         = Mom_Cor_Histo_Name_Angle_Ele.replace("; ",        "), ")
                                Mom_Cor_Histo_Name_Angle_Pip         = Mom_Cor_Histo_Name_Angle_Pip.replace("; ",        "), ")
                                Mom_Cor_Histo_Name_MM_DP_Ele         = Mom_Cor_Histo_Name_MM_DP_Ele.replace("; ",        "), ")
                                Mom_Cor_Histo_Name_MM_DP_Pip         = Mom_Cor_Histo_Name_MM_DP_Pip.replace("; ",        "), ")
                                # Mom_Cor_Histo_Name_DP_Ele_SF         = Mom_Cor_Histo_Name_DP_Ele_SF.replace("; ",        "), ")
                                # Mom_Cor_Histo_Name_DP_Pip_SF         = Mom_Cor_Histo_Name_DP_Pip_SF.replace("; ",        "), ")
                                Mom_Cor_Histo_Name_DP_Ele_Theta_SF   = Mom_Cor_Histo_Name_DP_Ele_Theta_SF.replace("; ",  "), ")
                                Mom_Cor_Histo_Name_DP_Pip_Theta_SF   = Mom_Cor_Histo_Name_DP_Pip_Theta_SF.replace("; ",  "), ")
                                # Mom_Cor_Histo_Name_DP_Ele_Phi_SF     = Mom_Cor_Histo_Name_DP_Ele_Phi_SF.replace("; ",    "), ")
                                # Mom_Cor_Histo_Name_DP_Pip_Phi_SF     = Mom_Cor_Histo_Name_DP_Pip_Phi_SF.replace("; ",    "), ")
                                
                                if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                    Mom_Cor_Histo_Name_Dele_SF       = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dele_SF_Dimension,    Histo_Var_D2=['Q2_y_Bin', -0.5,  18.5, 19], Histo_Var_D3=['z_pT_Bin_y_bin',  -0.5, 42.5,  43])), "))"])
                                    Mom_Cor_Histo_Name_Dpip_SF       = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dpip_SF_Dimension,    Histo_Var_D2=['Q2_y_Bin', -0.5,  18.5, 19], Histo_Var_D3=['z_pT_Bin_y_bin',  -0.5, 42.5,  43])), "))"])
                                    Mom_Cor_Histo_Name_Dele_SF       = Mom_Cor_Histo_Name_Dele_SF.replace("; ",          "), ")
                                    Mom_Cor_Histo_Name_Dpip_SF       = Mom_Cor_Histo_Name_Dpip_SF.replace("; ",          "), ")
                                
                            ###############################################################
                            ##==========##  Correction Histogram ID's (End)  ##==========##
                            ###############################################################


                            ###############################################################
                            ##==========##    Correction Histogram Titles    ##==========##
                            ###############################################################
                                
                                Mom_Cor_Histos_Name_MM_Ele_Title           = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass Histogram (Electron Kinematics",                              " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{el};",                          "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)};",  "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el} Bins"])
                                Mom_Cor_Histos_Name_MM_Pip_Title           = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass Histogram (#pi^{+} Pion Kinematics",                          " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{#pi+};",                        "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)};",  "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+} Bins"])
                                
                                Mom_Cor_Histos_Name_Delta_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram (Electron Kinematics",                                   " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{el};",                          "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{el};",   "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el} Bins"])
                                Mom_Cor_Histos_Name_Delta_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram (#pi^{+} Pion Kinematics",                               " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{#pi+};",                        "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+} Bins"])
                                
                                Mom_Cor_Histos_Name_Delta_Ele_Theta_Title  = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram vs #theta (Electron Kinematics",                         " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el};",                     "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{el};",   "El Sector"])
                                Mom_Cor_Histos_Name_Delta_Pip_Theta_Title  = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram vs #theta (#pi^{+} Pion Kinematics",                     " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+};",                   "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{#pi+};", "#pi^{+} Sector"])
                                
                                Mom_Cor_Histos_Name_Angle_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (Electron Kinematics",                       " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el};",                     "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{el};",      "(Smeared) " if("smear" in Histo_Smear) else " ", "#p_{el}"])
                                Mom_Cor_Histos_Name_Angle_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (#pi^{+} Pion Kinematics",                   " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+};",                   "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{#pi+};",    "(Smeared) " if("smear" in Histo_Smear) else " ", "#p_{#pi+}"])
                                
                                Mom_Cor_Histos_Name_MM_DP_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass vs #DeltaP vs Local #phi Histogram (Electron Kinematics",     " - Corrected" if(Mom_Correction_Q == "yes") else "", ");",                                                   "Local #phi_{el};",                 "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)};",  "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{el};"])
                                Mom_Cor_Histos_Name_MM_DP_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass vs #DeltaP vs Local #phi Histogram (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");",                                                   "Local #phi_{#pi+};",               "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)};",  "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{#pi+};"])
                                
                                # Mom_Cor_Histo_Name_DP_Ele_SF_Title         = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs P_{Electron}",                                        " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{el}}{P_{el}};",     "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{el}"])
                                # Mom_Cor_Histo_Name_DP_Pip_SF_Title         = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs P_{#pi^{+} Pion}",                                    " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{#pi+}}{P_{#pi+}};", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{#pi+}"])
                                Mom_Cor_Histo_Name_DP_Ele_Theta_SF_Title   = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs P_{Electron} vs #theta_{Electron}",                   " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{el}}{P_{el}};",     "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{el};",         "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el}"])
                                Mom_Cor_Histo_Name_DP_Pip_Theta_SF_Title   = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs P_{#pi^{+} Pion} vs #theta_{#pi^{+} Pion}",           " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{#pi+}}{P_{#pi+}};", "(Smeared) " if("smear" in Histo_Smear) else " ", "p_{#pi+};",       "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+}"])
                                # Mom_Cor_Histo_Name_DP_Ele_Phi_SF_Title     = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs Local #phi_{Electron}",                               " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{el}}{P_{el}};",     "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{el}"])
                                # Mom_Cor_Histo_Name_DP_Pip_Phi_SF_Title     = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#frac{#DeltaP}{P} vs Local #phi_{#pi^{+} Pion}",                           " (Corrected)" if(Mom_Correction_Q == "yes") else "",  ";", "(Smeared) " if("smear" in Histo_Smear) else " ", "#frac{#DeltaP_{#pi+}}{P_{#pi+}};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{#pi+}"])
                                
                                if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                    Mom_Cor_Histo_Name_Dele_SF_Title       = "".join(["#frac{P_{Smeared} - P}{P} (Electron",     " - Corrected" if(Mom_Correction_Q == "yes") else "", "); #frac{P_{Smeared} - P}{P}; Q^{2}-y Bin; z-P_{T} Bin"])
                                    Mom_Cor_Histo_Name_Dpip_SF_Title       = "".join(["#frac{P_{Smeared} - P}{P} (#pi^{+} Pion", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); #frac{P_{Smeared} - P}{P}; Q^{2}-y Bin; z-P_{T} Bin"])

                            ###############################################################
                            ##==========## Correction Histogram Titles (End) ##==========##
                            ###############################################################

                                variables_Mom_Cor     = ["MM", "Delta_Pel_Cors", "Delta_Ppip_Cors", "Delta_Theta_el_Cors", "Delta_Theta_pip_Cors", "el", "pip", "elth", "pipth", "elPhi", "pipPhi"]
                                if("smear" in Histo_Smear):
                                    variables_Mom_Cor = ["MM_smeared", "Delta_Pel_Cors_smeared", "Delta_Ppip_Cors_smeared", "Delta_Theta_el_Cors_smeared", "Delta_Theta_pip_Cors_smeared", "el_smeared", "pip_smeared", "elth_smeared", "pipth_smeared", "elPhi_smeared", "pipPhi_smeared", "el", "pip", "elth", "pipth"]

                                MCH_rdf = DF_Filter_Function_Full(DF=rdf, Variables=variables_Mom_Cor, Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                
                                if(MCH_rdf == "continue"):
                                    continue
                                
                            ###################################################################################
                            ##          ##          ##                               ##          ##          ##
                            ##==========##==========##     Correction Histograms     ##==========##==========##
                            ##          ##          ##                               ##          ##          ##
                            ###################################################################################
                            
                                Histograms_All[Mom_Cor_Histo_Name_MM_Ele]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_Ele,           str(Mom_Cor_Histos_Name_MM_Ele_Title),                                             100,  0, 10, 350,     0,  3.5,  10,     0,   40), "el"                 if("smear" not in Histo_Smear) else "el_smeared",         "MM"                   if("smear" not in Histo_Smear) else "MM_smeared",                   "elth"   if("smear" not in Histo_Smear) else  "elth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_MM_Pip]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_Pip,           str(Mom_Cor_Histos_Name_MM_Pip_Title),                                             100,  0,  8, 350,     0,  3.5,  10,     0,   40), "pip"                if("smear" not in Histo_Smear) else "pip_smeared",        "MM"                   if("smear" not in Histo_Smear) else "MM_smeared",                   "pipth"  if("smear" not in Histo_Smear) else "pipth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Ele]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Ele,           str(Mom_Cor_Histos_Name_Delta_Ele_Title),                                          100,  0, 10, 125, -0.75, 0.75,  10,     0,   40), "el_no_cor"          if("smear" not in Histo_Smear) else "el_no_cor_smeared",  "Delta_Pel_Cors"       if("smear" not in Histo_Smear) else "Delta_Pel_Cors_smeared",       "elth"   if("smear" not in Histo_Smear) else  "elth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Pip]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Pip,           str(Mom_Cor_Histos_Name_Delta_Pip_Title),                                          100,  0,  8, 125, -0.75, 0.75,  10,     0,   40), "pip_no_cor"         if("smear" not in Histo_Smear) else "pip_no_cor_smeared", "Delta_Ppip_Cors"      if("smear" not in Histo_Smear) else "Delta_Ppip_Cors_smeared",      "pipth"  if("smear" not in Histo_Smear) else "pipth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele]        = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Ele,       str(Mom_Cor_Histos_Name_Delta_Ele_Title).replace("#DeltaP", "#Delta#theta"),       100,  0, 10, 125, -0.75, 0.75,  10,     0,   40), "el"                 if("smear" not in Histo_Smear) else "el_smeared",         "Delta_Theta_el_Cors"  if("smear" not in Histo_Smear) else "Delta_Theta_el_Cors_smeared",  "elth"   if("smear" not in Histo_Smear) else  "elth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip]        = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Pip,       str(Mom_Cor_Histos_Name_Delta_Pip_Title).replace("#DeltaP", "#Delta#theta"),       100,  0,  8, 125, -0.75, 0.75,  10,     0,   40), "pip"                if("smear" not in Histo_Smear) else "pip_smeared",        "Delta_Theta_pip_Cors" if("smear" not in Histo_Smear) else "Delta_Theta_pip_Cors_smeared", "pipth"  if("smear" not in Histo_Smear) else "pipth_smeared")
                                
                                Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta]      = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Ele_Theta,     str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title),                                    100,  0, 40, 125, -0.75, 0.75,   8,  -0.5,  7.5), "elth"               if("smear" not in Histo_Smear) else "elth_smeared",       "Delta_Pel_Cors"       if("smear" not in Histo_Smear) else "Delta_Pel_Cors_smeared",       "esec")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta]      = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Pip_Theta,     str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title),                                    100,  0, 40, 125, -0.75, 0.75,   8,  -0.5,  7.5), "pipth"              if("smear" not in Histo_Smear) else "pipth_smeared",      "Delta_Ppip_Cors"      if("smear" not in Histo_Smear) else "Delta_Ppip_Cors_smeared",      "pipsec")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele_Theta]  = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Ele_Theta, str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title).replace("#DeltaP", "#Delta#theta"), 100,  0, 40, 125, -0.75, 0.75,   8,  -0.5,  7.5), "elth"               if("smear" not in Histo_Smear) else "elth_smeared",       "Delta_Theta_el_Cors"  if("smear" not in Histo_Smear) else "Delta_Theta_el_Cors_smeared",  "esec")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip_Theta]  = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Pip_Theta, str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title).replace("#DeltaP", "#Delta#theta"), 100,  0, 40, 125, -0.75, 0.75,   8,  -0.5,  7.5), "pipth"              if("smear" not in Histo_Smear) else "pipth_smeared",      "Delta_Theta_pip_Cors" if("smear" not in Histo_Smear) else "Delta_Theta_pip_Cors_smeared", "pipsec")
                                Histograms_All[Mom_Cor_Histo_Name_Angle_Ele]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Ele,        str(Mom_Cor_Histos_Name_Angle_Ele_Title),                                          100,  0, 40, 360,     0,  360, 100,     0,   10), "elth"               if("smear" not in Histo_Smear) else "elth_smeared",       "elPhi"                if("smear" not in Histo_Smear) else "elPhi_smeared",                "el"     if("smear" not in Histo_Smear) else  "el_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_Angle_Pip]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Pip,        str(Mom_Cor_Histos_Name_Angle_Pip_Title),                                          100,  0, 40, 360,     0,  360, 100,     0,    8), "pipth"              if("smear" not in Histo_Smear) else "pipth_smeared",      "pipPhi"               if("smear" not in Histo_Smear) else "pipPhi_smeared",               "pip"    if("smear" not in Histo_Smear) else "pip_smeared")

                                Histograms_All[Mom_Cor_Histo_Name_MM_DP_Ele]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_DP_Ele,        str(Mom_Cor_Histos_Name_MM_DP_Ele_Title),                                          20, -40, 40, 350,     0,  3.5, 125, -0.75, 0.75), "elPhi_Local",  "MM" if("smear" not in Histo_Smear) else "MM_smeared",         "Delta_Pel_Cors"       if("smear" not in Histo_Smear) else "Delta_Pel_Cors_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_MM_DP_Pip]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_DP_Pip,        str(Mom_Cor_Histos_Name_MM_DP_Pip_Title),                                          20, -40, 40, 350,     0,  3.5, 125, -0.75, 0.75), "pipPhi_Local", "MM" if("smear" not in Histo_Smear) else "MM_smeared",         "Delta_Ppip_Cors"      if("smear" not in Histo_Smear) else "Delta_Ppip_Cors_smeared")
                                
                                Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta_SF]   = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Ele_Theta_SF,  str(Mom_Cor_Histo_Name_DP_Ele_Theta_SF_Title),                                     500, -5,  5, 100,     0,   10, 100,     0,   40), "DP_el_SF"           if("smear" not in Histo_Smear) else "DP_el_SF_smeared",   "el"                   if("smear" not in Histo_Smear) else "el_smeared",                   "elth"   if("smear" not in Histo_Smear) else  "elth_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta_SF]   = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Pip_Theta_SF,  str(Mom_Cor_Histo_Name_DP_Pip_Theta_SF_Title),                                     500, -5,  5, 100,     0,    8, 100,     0,   40), "DP_pip_SF"          if("smear" not in Histo_Smear) else "DP_pip_SF_smeared",  "pip"                  if("smear" not in Histo_Smear) else "pip_smeared",                  "pipth"  if("smear" not in Histo_Smear) else "pipth_smeared")
                                
                                if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                    Histograms_All[Mom_Cor_Histo_Name_Dele_SF]       = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Dele_SF,          str(Mom_Cor_Histo_Name_Dele_SF),                                                   200,  0,  2,  19,  -0.5, 18.5,  43,  -0.5, 42.5), "Dele_SF", "Q2_y_Bin", "z_pT_Bin_y_bin")
                                    Histograms_All[Mom_Cor_Histo_Name_Dpip_SF]       = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Dpip_SF,          str(Mom_Cor_Histo_Name_Dpip_SF),                                                   200,  0,  2,  19,  -0.5, 18.5,  43,  -0.5, 42.5), "Dpip_SF", "Q2_y_Bin", "z_pT_Bin_y_bin")

                            ###################################################################################
                            ##          ##          ##                               ##          ##          ##
                            ##==========##==========##  Correction Histograms (End)  ##==========##==========##
                            ##          ##          ##                               ##          ##          ##
                            ###################################################################################
                                # print("Histo_Group = ", Histo_Group)
                                if(str(file_location) != 'time'):
                                    # print("")

                                    # print("Drawing: ", Mom_Cor_Histo_Name_MM_Ele)
                                    Histograms_All[Mom_Cor_Histo_Name_MM_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_MM_Pip].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_DP_Ele)
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Pip].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_DP_Ele_Theta)
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_DTheta_Ele)
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_DTheta_Ele_Theta)
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele_Theta].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip_Theta].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_Angle_Ele)
                                    Histograms_All[Mom_Cor_Histo_Name_Angle_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_Angle_Pip].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_MM_DP_Ele)
                                    Histograms_All[Mom_Cor_Histo_Name_MM_DP_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_MM_DP_Pip].Write()
                                    
                                    # print("Drawing: ", Mom_Cor_Histo_Name_DP_Ele_Theta_SF)
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta_SF].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta_SF].Write()
                                    
                                    if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                        Histograms_All[Mom_Cor_Histo_Name_Dele_SF].Write()
                                        Histograms_All[Mom_Cor_Histo_Name_Dpip_SF].Write()
                                    
                                    del Histograms_All
                                    Histograms_All = {}
                                    # print("")
                                    
                                Print_Progress(count_of_histograms,    16, 200 if(str(file_location) != 'time') else 50)
                                count_of_histograms     += 16
                                if(("smear" in str(Histo_Smear)) and (Histo_Data in ["mdf"])):
                                    Print_Progress(count_of_histograms, 2, 200 if(str(file_location) != 'time') else 50)
                                    count_of_histograms += 2
                                del MCH_rdf

##################################################=========================================##########################################################################################################################################
##======##======##======##======##======##======##     Normal (1D/2D/3D) Histograms        ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=========================================##########################################################################################################################################
                            if(Histo_Group in ["Normal", "Has_Matched", "Bin_Purity", "Delta_Matched"]):

                                Histo_Binning      = [Binning, "All", "All"]
                                Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])

            ###################################################################################
            #####====================#####     1D Histograms     #####====================#####
            ###################################################################################

                                if(Histo_Group in ["Has_Matched", "Bin_Purity", "Delta_Matched"]):
                                    for Vars_1D_Test in Variable_Loop:
                                        if(len(Vars_1D_Test) == 4):
                                            # Normal 1D Variable
                                            Vars_1D = Vars_1D_Test
                                        else:
                                            # Vars_1D = Multi_Dimensional_Bin_Construction(DF=rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")
                                            Vars_1D = Multi_Dim_Bin_Def(DF=rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")
                                            
                                        # if(Binning not in ["2"] and "Bin_4D" in str(Vars_1D[0]) and "OG" not in str(Vars_1D[0])):
                                        #     continue # These 4D bins have only been defined with my new binning schemes
                                        # if(Binning in     ["2"] and "Bin_4D" in str(Vars_1D[0]) and "OG" in     str(Vars_1D[0])):
                                        #     continue # These 4D bins were defined with the original binning scheme
                                            
                                        Histo_Var_D1_Name = Dimension_Name_Function(Histo_Var_D1=Vars_1D, Histo_Var_D2="None")

                                        Histo_Name = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_1D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_D1_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                        Normal_rdf = DF_Filter_Function_Full(DF=rdf, Variables=Vars_1D[0], Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                        if(("Combined_" in Vars_1D[0]) or ("Multi_Dim" in Vars_1D[0])):
                                            # Normal_rdf = Multi_Dimensional_Bin_Construction(DF=Normal_rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF")
                                            Normal_rdf = Multi_Dim_Bin_Def(DF=Normal_rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF")
                                        if(Normal_rdf == "continue"):
                                            continue
                                        Title_1D_L1   = "".join([str(Data_Type_Title(Data_Type=Histo_Data, Smearing_Q=Histo_Smear)), " ", str(variable_Title_name(Vars_1D[0]))])
                                        Title_1D_L2   = "".join(["Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut))])
                                        Title_1D_L3   = "" if(Histo_Group == "Normal") else "Matched" if(Histo_Group == "Has_Matched") else "Bin Purity" if(Histo_Group == "Bin_Purity") else "#Delta Between Matches" if(Histo_Group == "Delta_Matched") else "Error"

                                        Title_1D_Axis     = "".join(["Q^{2}-x_{B} Bin" if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q^{2}-y Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", str(variable_Title_name(Vars_1D[0]))])
                                        if(Histo_Group == "Delta_Matched"):
                                            Title_1D_Axis = "".join(["Q^{2}-x_{B} Bin" if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q^{2}-y Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", "#Delta_{(REC - GEN)}", str(variable_Title_name(Vars_1D[0]))])

                                        Title_1D_Out      = "".join(["#splitline{", str(Title_1D_L1), "}{", str(Title_1D_L2), "};", str(Title_1D_Axis)])
                                        if(Title_1D_L3 != ""):
                                            Title_1D_Out  = "".join(["#splitline{#splitline{", str(Title_1D_L1), "}{", str(Title_1D_L2), "}}{", str(Title_1D_L3), "};", str(Title_1D_Axis)])
                                            
                                        Title_1D_Out  = Title_1D_Out.replace(") (", " - ")

                                        if(Histo_Group == "Delta_Matched"):
                                            D_Matched_rdf = Delta_Matched_DF(Normal_rdf, Vars_1D[0]) # Calculates the different between the matched reconstructed and generated events (rec - gen)
                                            if(Final_DF == "continue"):
                                                continue
                                        if(Histo_Group not in ["Bin_Purity", "Delta_Matched"]):
                                            Histograms_All[Histo_Name] = Normal_rdf.Histo3D((str(Histo_Name), str(Title_1D_Out), 17, -3.5, 14.5, 55, -3.5, 51.5, Vars_1D[3], Vars_1D[1], Vars_1D[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(Vars_1D[0]))
                                        elif(Histo_Group == "Bin_Purity"):
                                            Histograms_All[Histo_Name] = Bin_Purity_Filter_Fuction(Normal_rdf, Vars_1D[0], Vars_1D[1], Vars_1D[2], Vars_1D[3]).Histo3D((str(Histo_Name), str(Title_1D_Out), 17, -3.5, 14.5, 55, -3.5, 51.5, Vars_1D[3], Vars_1D[1], Vars_1D[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(Vars_1D[0]))
                                        elif(Histo_Group == "Delta_Matched"):
                                            if("el" not in Vars_1D[0] and "pip" not in Vars_1D[0]):
                                                continue # Don't need these extra ∆(REC-GEN) histograms (angles/momentum are the only criteria being considered)
                                            delta_bins = Delta_Matched_Bin_Calc(Vars_1D[0], Vars_1D[1], Vars_1D[2])
                                            if("continue" in delta_bins):
                                                continue
                                            Histograms_All[Histo_Name] = D_Matched_rdf.Histo3D((str(Histo_Name), str(Title_1D_Out), Vars_1D[3], Vars_1D[1], Vars_1D[2], delta_bins[0], delta_bins[1], delta_bins[2], 8, -0.5, 7.5), str(Vars_1D[0]), "Delta_Matched_Value", "pipsec" if("pip" in Vars_1D[0]) else "esec")
                                            if("Phi" in Vars_1D[0]):
                                                Histograms_All["".join([str(Histo_Name), "_Extra_3D"])] = DF_Filter_Function_Full(DF=D_Matched_rdf, Variables=str(Vars_1D[0].replace("Phi", "th")), Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1).Histo3D(("".join([str(Histo_Name), "_Extra_3D"]), "".join([Title_1D_Out.replace("".join(["; ", "#pi^{+} Pion" if("pip" in Vars_1D[0]) else "Electron", " Sector"]), ""), ";#theta_{", "el" if "el" in Vars_1D[0] else "#pi+" ,"}"]), Vars_1D[3], Vars_1D[1], Vars_1D[2], delta_bins[0], delta_bins[1], delta_bins[2], 34, 0, 40), str(Vars_1D[0]), "Delta_Matched_Value", str(Vars_1D[0].replace("Phi", "th")))
                                        
                                        # print("(1D) Histo_Group = ", Histo_Group)
                                        if(str(file_location) != 'time'):
                                            Histograms_All[Histo_Name].Write()
                                            if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched"):
                                                Histograms_All["".join([str(Histo_Name), "_Extra_3D"])].Write()
                                        if(output_all_histo_names_Q != "yes"):
                                            del Histograms_All
                                            Histograms_All = {}

                                        # The 1D Histograms are being saved
                                        Print_Progress(count_of_histograms, 2 if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched") else 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1
                                        if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched"):
                                            count_of_histograms += 1
                                        del Normal_rdf
                                
            ###################################################################################
            #####====================#####  1D Histograms (End)  #####====================#####
            ###################################################################################
            ###################################################################################
            #####====================#####     2D Histograms     #####====================#####
            ###################################################################################

                                for Vars_2D in Variable_Loop_2D:

                                    Histo_Var_D2_Name = Dimension_Name_Function(Histo_Var_D1=Vars_2D[0], Histo_Var_D2=Vars_2D[1], Histo_Var_D3="None")
                                    Normal_rdf        = DF_Filter_Function_Full(DF=rdf, Variables=[Vars_2D[0][0], Vars_2D[1][0]], Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                    if(Normal_rdf == "continue"):
                                        continue
                ###################################################################################
                #####====================#####     Q2-xB Bin Loop    #####====================#####
                ###################################################################################
                
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                        if(Q2_xB_Bin_Num > 1  and Binning in ["Off", "off"]):
                                            # This binning scheme only goes up to 1 Q2-xB bin
                                            continue
                                        if(Q2_xB_Bin_Num > 8  and Binning in ["2", "OG", "Test"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        if(Q2_xB_Bin_Num > 9  and Binning in ["", "Stefan"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        # if(Q2_xB_Bin_Num > 13 and Binning in ["5", "Y_bin", "Y_Bin"]):
                                        #     # This binning scheme only goes up to 13 Q2-xB bins # Outdated as of 9/27/2023
                                        #     continue
                                        if(Q2_xB_Bin_Num < -2 and Binning not in ["5", "Y_bin", "Y_Bin"]):
                                            # This is the only binning scheme with a defined value for Q2_xB_Bin_Num = -3 (i.e., only migration bins)
                                            continue
                                        if(Q2_xB_Bin_Num > 17 and Binning in ["4", "y_bin", "y_Bin"]):
                                            # This binning scheme only goes up to 17 Q2-xB bins
                                            continue
                                        Histo_Binning      = [Binning, "All" if(Q2_xB_Bin_Num == -1) else str(Q2_xB_Bin_Num), "All"]
                                        Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:" if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "'-[Q2-y-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])
                                        
                                        Histo_Name    = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_2D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_D2_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")
                                        Title_2D_L1   = "".join([str(Data_Type_Title(Data_Type=Histo_Data, Smearing_Q=Histo_Smear)), " ", str(variable_Title_name(Vars_2D[0][0])).replace(" (Smeared)", ""), " vs. ", str(variable_Title_name(Vars_2D[1][0]))])
                                        Title_2D_L2   = "".join(["Q^{2}-x_{B} Bin: " if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q^{2}-y Bin: ", str(Histo_Binning[1])])
                                        Title_2D_L3   = "".join(["Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut))])
                                        Title_2D_Axis = "".join(["z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", str(variable_Title_name(Vars_2D[0][0])), "; ", str(variable_Title_name(Vars_2D[1][0]))])
                                        Title_2D_Out  = "".join(["#splitline{#splitline{", str(Title_2D_L1), "}{", str(Title_2D_L2), "}}{", str(Title_2D_L3), "};", str(Title_2D_Axis)])
                                        Title_2D_Out  = Title_2D_Out.replace(") (", " - ")
                                        Bin_Filter    = "esec != -2" if(Q2_xB_Bin_Num == -1) else "".join([str(Q2_xB_Bin_Filter_str), " != 0"]) if(Q2_xB_Bin_Num == -2) else "".join([str(Q2_xB_Bin_Filter_str), " > 17"]) if(Q2_xB_Bin_Num == -3) else "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Num)])
                                        
                                        if(Use_Weight):
                                            Histograms_All[Histo_Name] = (Normal_rdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name), str(Title_2D_Out), 55, -3.5, 51.5, Vars_2D[0][3], Vars_2D[0][1], Vars_2D[0][2], Vars_2D[1][3], Vars_2D[1][1], Vars_2D[1][2]), str(z_pT_Bin_Filter_str), str(Vars_2D[0][0]), str(Vars_2D[1][0]), "Event_Weight")
                                        else:
                                            Histograms_All[Histo_Name] = (Normal_rdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name), str(Title_2D_Out), 55, -3.5, 51.5, Vars_2D[0][3], Vars_2D[0][1], Vars_2D[0][2], Vars_2D[1][3], Vars_2D[1][1], Vars_2D[1][2]), str(z_pT_Bin_Filter_str), str(Vars_2D[0][0]), str(Vars_2D[1][0]))

                                        # print("(2D) Histo_Group = ", Histo_Group)
                                        # print("Drawing: ", Histo_Name)
                                        if(str(file_location) != 'time'):
                                            Histograms_All[Histo_Name].Write()
                                        if(output_all_histo_names_Q != "yes"):
                                            del Histograms_All
                                            Histograms_All = {}

                                        # The 2D Histograms are being saved
                                        Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1
                                    del Normal_rdf

            ###################################################################################
            #####====================#####  2D Histograms (End)  #####====================#####
            ###################################################################################
            ###################################################################################
            #####====================#####     3D Histograms     #####====================#####
            ###################################################################################

                                for Vars_3D in Variable_Loop_3D:

                                    Histo_Var_D3_Name = Dimension_Name_Function(Histo_Var_D1=Vars_3D[0], Histo_Var_D2=Vars_3D[1], Histo_Var_D3=Vars_3D[2])
                                    Normal_rdf        = DF_Filter_Function_Full(DF=rdf, Variables=[Vars_3D[0][0], Vars_3D[1][0], Vars_3D[2][0]], Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                    if(Normal_rdf == "continue"):
                                        continue
                ###################################################################################
                #####====================#####     Q2-xB Bin Loop    #####====================#####
                ###################################################################################
                
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                        if(Q2_xB_Bin_Num > 1 and Binning in ["Off", "off"]):
                                            # This binning scheme only goes up to 1 Q2-xB bin
                                            continue
                                        if(Q2_xB_Bin_Num > 8 and Binning in ["2", "OG", "Test"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        if(Q2_xB_Bin_Num > 9 and Binning in ["", "Stefan"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        # if(Q2_xB_Bin_Num > 13 and Binning in ["5", "Y_bin", "Y_Bin"]):
                                        #     # This binning scheme only goes up to 13 Q2-y bins # Outdated as of 9/27/2023
                                        #     continue
                                        if(Q2_xB_Bin_Num < -2 and Binning not in ["5", "Y_bin", "Y_Bin"]):
                                            # This is the only binning scheme with a defined value for Q2_xB_Bin_Num = -3 (i.e., only migration bins)
                                            continue
                                        if(Q2_xB_Bin_Num > 17 and Binning in ["4", "y_bin", "y_Bin"]):
                                            # This binning scheme only goes up to 17 Q2-y bins
                                            continue
                                        Histo_Binning      = [Binning, "All" if(Q2_xB_Bin_Num == -1) else str(Q2_xB_Bin_Num), "All"]
                                        Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:" if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "'-[Q2-y-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])
                                        
                                        Histo_Name    = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_3D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_D3_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")
                                        Title_3D_L1   = "".join([str(Data_Type_Title(Data_Type=Histo_Data, Smearing_Q=Histo_Smear)), " ", str(variable_Title_name(Vars_3D[0][0])).replace(" (Smeared)", ""), " vs ", str(variable_Title_name(Vars_3D[1][0])).replace(" (Smeared)", ""), " vs ", str(variable_Title_name(Vars_3D[2][0]))])
                                        Title_3D_L2   = "".join(["Q^{2}-x_{B} Bin: " if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q^{2}-y Bin: ", str(Histo_Binning[1])])
                                        Title_3D_L3   = "".join(["Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut))])
                                        Title_3D_Axis = "".join([str(variable_Title_name(Vars_3D[2][0])), "; ", str(variable_Title_name(Vars_3D[0][0])), "; ", str(variable_Title_name(Vars_3D[1][0]))])
                                        Title_3D_Out  = "".join(["#splitline{#splitline{", str(Title_3D_L1), "}{", str(Title_3D_L2), "}}{", str(Title_3D_L3), "};", str(Title_3D_Axis)])
                                        Title_3D_Out  = Title_3D_Out.replace(") (", " - ")
                                        Bin_Filter    = "esec != -2" if(Q2_xB_Bin_Num == -1) else "".join([str(Q2_xB_Bin_Filter_str), " != 0"]) if(Q2_xB_Bin_Num == -2) else "".join([str(Q2_xB_Bin_Filter_str), " > 17"]) if(Q2_xB_Bin_Num == -3) else "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Num)])
                                        
                                        Histograms_All[Histo_Name] = (Normal_rdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name), str(Title_3D_Out), Vars_3D[2][3], Vars_3D[2][1], Vars_3D[2][2], Vars_3D[0][3], Vars_3D[0][1], Vars_3D[0][2], Vars_3D[1][3], Vars_3D[1][1], Vars_3D[1][2]), str(Vars_3D[2][0]), str(Vars_3D[0][0]), str(Vars_3D[1][0]))

                                        # print("(3D) Histo_Group = ", Histo_Group)
                                        # print("Drawing: ", Histo_Name)
                                        if(str(file_location) != 'time'):
                                            Histograms_All[Histo_Name].Write()
                                        if(output_all_histo_names_Q != "yes"):
                                            del Histograms_All
                                            Histograms_All = {}

                                        # The 3D Histograms are being saved
                                        Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1
                                    del Normal_rdf
            

##################################################=========================================##########################################################################################################################################
##======##======##======##======##======##======##     Response Matrix (Both Types)        ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=========================================##########################################################################################################################################
                            if(Histo_Group in ["Response_Matrix", "Response_Matrix_Normal"]):
                                if("EDIS" in Histo_Cut):
                                    # Do not need exclusive cuts for the response matrices
                                    continue
                                
                                Res_Binning_2D_Q2_xB = [str(Q2_xB_Bin_Filter_str), -1.5, 10.5 + 4,  12 + 4]
                                Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -1.5, 50.5,  52]
                                
                                # Res_Binning_2D_Q2_xB = [str(Q2_xB_Bin_Filter_str), -3.5, 11.5,  15]
                                # Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -3.5, 51.5,  55]
                                
                                if(Binning in ["4", "y_bin", "y_Bin"]):
                                    Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -0.5, 42.5,  43]
                                if(Binning in ["5", "Y_bin", "Y_Bin"]):
                                    Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -0.5, 65.5,  66]
                                    
                                phi_t_Binning_New = copy.deepcopy(phi_t_Binning)
                                if("smear" in Histo_Smear):
                                    phi_t_Binning_New[0] = "".join([str(phi_t_Binning_New[0]), "_smeared" if("smear" not in phi_t_Binning_New[0]) else ""])
                                    
                                
                                Res_Var_Add = []
                                # # Res_Var_Add = [[[str(Q2_xB_Bin_Filter_str), 0, 8, 8], phi_t_Binning_New], [[str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New], [[str(Q2_xB_Bin_Filter_str), 0, 8, 8], [str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New]]
                                # # Res_Var_Add = [[[str(Q2_xB_Bin_Filter_str), 0, 8, 8], phi_t_Binning_New], [[str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New]]
                                # Res_Var_Add = [[phi_t_Binning_New, [str(Q2_xB_Bin_Filter_str), 0, 8, 8]], [str(Q2_xB_Bin_Filter_str), 0, 8, 8]]
                                Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old]]
                                Res_Var_Add = [[phi_t_Binning_New, [str(Q2_xB_Bin_Filter_str), 0, 8 if(Binning in ["2", "OG", "Test", ""]) else 17 if(Binning in ["4", "y_bin", "y_Bin"]) else 14, 8 if(Binning in ["2", "OG", "Test", ""]) else 17 if(Binning in ["4", "y_bin", "y_Bin"]) else 14]]]
                                # Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old], [phi_t_Binning_New, [str(Q2_xB_Bin_Filter_str), 0, 8 if(Binning in ["2", ""]) else 12, 8 if(Binning in ["2", ""]) else 12]]]
                                
                                if(Binning not in ["2", "OG"]):
                                    Res_Var_Add = []
                                if(Binning in ["4", "y_bin", "y_Bin"]):
                                    # Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old], [phi_t_Binning_New, Q2_y_Binning], [[phi_t_Binning_New[0], 0, 360, 10], Q2_y_z_pT_Binning]]
                                    # # Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old], [phi_t_Binning_New, Q2_y_Binning], [[phi_t_Binning_New[0], 0, 360, 24], Q2_y_z_pT_Binning]]
                                    # Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old], [phi_t_Binning_New, Q2_y_Binning], [[phi_t_Binning_New[0], 0, 360, 24], Res_Binning_2D_z_pT]]
                                    Res_Var_Add = [[phi_t_Binning_New, Q2_y_Binning], [[phi_t_Binning_New[0], 0, 360, 24], Res_Binning_2D_z_pT]]
                                    
                                    # Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["el_smeared"     if("smear" in str(Histo_Smear)) else "el",     2.6,  8,   20]])
                                    # Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["pip_smeared"    if("smear" in str(Histo_Smear)) else "pip",    1.25, 5,   15]])
                                    Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["elth_smeared"   if("smear" in str(Histo_Smear)) else "elth",   5,    35,  30]])
                                    Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["pipth_smeared"  if("smear" in str(Histo_Smear)) else "pipth",  5,    35,  30]])
                                    Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["elPhi_smeared"  if("smear" in str(Histo_Smear)) else "elPhi",  0,    360, 24]])
                                    Res_Var_Add.append([[phi_t_Binning_New[0], 0, 360, 24], ["pipPhi_smeared" if("smear" in str(Histo_Smear)) else "pipPhi", 0,    360, 24]])
                                    
                                if(Binning in ["5", "Y_bin", "Y_Bin"]):
                                    # Res_Var_Add = [[phi_t_Binning_New, Q2_Binning_Old], [phi_t_Binning_New, Q2_Y_Binning]]
                                    Res_Var_Add = [[[phi_t_Binning_New[0], 0, 360, 24], Res_Binning_2D_z_pT]]
                                
                                # # REMOVING ALL ABOVE ADDITIONS (remove this line later)
                                # Res_Var_Add = []
                                
                                if(Alert_of_Response_Matricies):
                                    if(len(List_of_Quantities_1D) == 0):
                                        print(color.BOLD, color.BLUE, "\nResponse Matrix Code for Unfolding has been turned off...\n", color.END)
                                        Res_Var_Add = []
                                    elif(len(Res_Var_Add) == 0):
                                        print(color.BOLD, color.BLUE, "\nOnly running the base 1D options in the Response Matrix Code for Unfolding (i.e., Res_Var_Add is empty)...\n", color.END)
                                    else:
                                        print(color.BOLD, color.GREEN, "\nAdding the following Response Matrix options (for Multidimensional unfolding):", color.END, "\n\tRes_Var_Add =", str(Res_Var_Add), "\n")
                                    Alert_of_Response_Matricies = False
                                
                                Res_Var_List = copy.deepcopy(List_of_Quantities_1D)
                                if(Res_Var_Add != []):
                                    for Response_Added in Res_Var_Add:
                                        Res_Var_List.append(Response_Added)
                                        
                                # Res_Var_List = [[[phi_t_Binning_New[0], 0, 360, 24], Res_Binning_2D_z_pT]]
                                # Res_Var_List = []
                                
                                for Var_List_Test in Res_Var_List:
                                    
                                    if(len(Var_List_Test) == 4):
                                        # Normal 1D Variable
                                        Var_List = Var_List_Test
                                    else:
                                        # Var_List = Multi_Dimensional_Bin_Construction(DF=rdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")
                                        Var_List = Multi_Dim_Bin_Def(DF=rdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")

                                    variable = Var_List[0]
                                    if(("smear" in Histo_Smear) and ("smear" not in variable)):
                                        variable = "".join([variable, "_smeared"])

                                    Min_range, Max_range, Num_of_Bins = Var_List[1], Var_List[2], Var_List[3]

                                    BIN_SIZE  = round((Max_range - Min_range)/Num_of_Bins, 4)
                                    Bin_Range = "".join([str(Min_range), " #rightarrow ", str(Max_range)])

                                    # Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2="None")
                                    Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2=Res_Binning_2D_z_pT)
                                    
                                    sdf = Bin_Number_Variable_Function(DF_Filter_Function_Full(DF=rdf if(Histo_Data in ["rdf", "gdf"]) else rdf.Filter("PID_el != 0 && PID_pip != 0"), Variables=variable, Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning), Variable=variable, min_range=Min_range, max_range=Max_range, number_of_bins=Num_of_Bins, DF_Type=Histo_Data)
                                    if(("Combined_" in variable) or ("Multi_Dim" in variable)):
                                        # sdf = Multi_Dimensional_Bin_Construction(DF=sdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF_Res")
                                        sdf = Multi_Dim_Bin_Def(DF=sdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF_Res")

                                    if(sdf == "continue"):
                                        continue

                ###################################################################################
                #####====================#####     Q2-xB Bin Loop    #####====================#####
                ###################################################################################
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                        if(Q2_xB_Bin_Num > 1 and ((Binning in ["Off", "off"]) or (str(Q2_xB_Bin_Filter_str) == str(variable)))):
                                            # This binning scheme only goes up to 1 Q2-xB bin
                                            # Also prevents bin cuts for instances of the variable being used is the bin being cut
                                            continue
                                        if(Q2_xB_Bin_Num > 8 and Binning in ["2", "OG", "Test"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        if(Q2_xB_Bin_Num > 9 and Binning in ["", "Stefan"]):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue
                                        # if(Q2_xB_Bin_Num > 13 and Binning in ["5", "Y_bin", "Y_Bin"]):
                                        #     # This binning scheme only goes up to 13 Q2-xB bins # Outdated as of 9/27/2023
                                        #     continue
                                        if(Q2_xB_Bin_Num < -2 and Binning not in ["5", "Y_bin", "Y_Bin"]):
                                            # This is the only binning scheme with a defined value for Q2_xB_Bin_Num = -3 (i.e., only migration bins)
                                            continue
                                        if(Q2_xB_Bin_Num > 17 and Binning in ["4", "y_bin", "y_Bin"]):
                                            # This binning scheme only goes up to 17 Q2-xB bins
                                            continue

                                        if((Q2_xB_Bin_Num > 0) and ((str(Q2_xB_Bin_Filter_str) in str(variable)) or (("Bin" in str(variable)) and ("Multi_Dim_z_pT_Bin" not in str(variable))))):
                                        # if((Q2_xB_Bin_Num > 0) and ((str(Q2_xB_Bin_Filter_str) in str(variable)))):
                                            # Making a response matrix with cuts on the Q2-xB/Q2-y bins is unnecessary for the kinematic binned response matrices
                                            continue
                                            
                                        if((Q2_xB_Bin_Num > 0) and (str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "y"])):
                                            # Making a response matrix with cuts on the Q2-xB bins is unnecessary for these response matrices (just using as examples for analysis note)
                                            continue

                                        if((Q2_xB_Bin_Num > 0) and "phi_t" not in str(variable)):
                                            # No need to use the kinematic binning for response matrices that do not include the phi_t variable
                                            continue
                                            
                                            
                                        Histo_Binning      = [Binning, "All" if(Q2_xB_Bin_Num == -1) else str(Q2_xB_Bin_Num), "All"]
                                        Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:" if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "'-[Q2-y-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])
                                        
                                        Histo_Name_No_Cut, Histo_Name_MM_Cut, Histo_Name__No_Cut, Histo_Name_Cutting, Histo_Name__MM_Cut, Histo_Name_1D_MM_Cut, Histo_Name_1D_No_Cut = "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
                                        
                                        Histo_Name    = ((("".join(["((", "; ".join([Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_RM_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")
                                        Histo_Name_1D = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_1D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_RM_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                        Migration_Title_L1 = "".join(["#scale[1.5]{Response Matrix of ", str(variable_Title_name(variable)), "}"]) if(Histo_Data in ["mdf", "pdf"]) else "".join(["#scale[1.5]{", "Experimental" if(Histo_Data == "rdf") else "Generated" if(Histo_Data != "mdf") else "Reconstructed (MC)", " Distribution of ", str(variable_Title_name(variable)), "}"])                                            
                                        Migration_Title_L2 = "".join(["#scale[1.15]{Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut)), "}"])
                                        Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), " - Range (from Bin 1-", str(Num_of_Bins),"): ", str(Bin_Range), " - Size: ", str(BIN_SIZE), " per bin}"])
                                        
                                        if(Histo_Group == "Response_Matrix_Normal"):
                                            Migration_Title_L3 = "".join(["#scale[1.35]{Range: ", str(Bin_Range), " - Size: ", str(BIN_SIZE), " per bin}"])
                                        if("Bin" in variable):
                                            Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), "}"])
                                            
                                        Migration_Title_L4 = "".join(["Q^{2}-x_{B} Bin: " if(Binning not in ["4", "y_bin", "y_Bin", "5", "Y_bin", "Y_Bin"]) else "Q^{2}-y Bin: ", str(Histo_Binning[1])]) if(Q2_xB_Bin_Num > 0) else ""

                                        if(Histo_Group == "Response_Matrix"):
                                            Migration_Title       = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1),   "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable.replace("_smeared", ""))), " GEN Bins; ", str(variable_Title_name(variable)), " REC Bins"])
                                            if(Histo_Data not in ["mdf", "pdf"]):
                                                Migration_Title   = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1),   "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)),                         " REC"  if("g" not in Histo_Data) else " GEN",         " Bins; z-P_{T} Bins"])
                                        else:
                                            Migration_Title       = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1),   "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable.replace("_smeared", ""))), " (GEN); ",    str(variable_Title_name(variable)), " (REC)"])
                                            if(Histo_Data not in ["mdf", "pdf"]):
                                                Migration_Title   = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1),   "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)),                         " (REC" if("g" not in Histo_Data) else " (GEN",            "); z-P_{T} Bins"])

                                        if(Histo_Data == "mdf"):
                                            Migration_Title_L1_2  = "".join(["#scale[1.5]{Reconstructed (MC) Distribution of ", str(variable_Title_name(variable)), "}"])
                                            Migration_Title_2     = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1_2), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)),                                                                            " REC Bins; z-P_{T} Bins"])
                                            if(Histo_Group == "Response_Matrix_Normal"):
                                                Migration_Title_2 = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1_2), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)),                                                                                     "; z-P_{T} Bins"])
                                        
                                        if((Histo_Group == "Response_Matrix") and ("Combined_" not in variable and "Multi_Dim" not in variable)):
                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5) # Num of REC bins needs to equal Num of GEN bins for unfolding
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5)

                                            Variable_Gen = str("".join([str(variable), "_GEN_BIN"])) if("Bin" not in str(variable)) else str("".join([str(variable).replace("_smeared", ""), "_gen"]))
                                            Variable_Rec = str("".join([str(variable), "_REC_BIN"])) if("Bin" not in str(variable)) else str(variable)
                                        else:
                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = Num_of_Bins, Min_range, Max_range
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = Num_of_Bins, Min_range, Max_range

                                            Variable_Gen = str("".join([str(variable).replace("_smeared", ""), "_gen"]))
                                            Variable_Rec = str(variable)
                                            
                                            # print("Variable_Gen = ", Variable_Gen, "\nVariable_Rec = ", Variable_Rec, "\n")
                                            
                                        # if("Combined_" in variable):
                                        #     print("".join([color.BOLD, "Variable_Gen = ", str(Variable_Gen), color.END]))
                                        #     print("".join([color.BOLD, "Variable_Rec = ", str(Variable_Rec), color.END]))
                                        #     print("\n")
                                        #     print("Printing the full list of variables (and their object types) in the DataFrame...")
                                        #     for ii in range(0, len(sdf.GetColumnNames()), 1):
                                        #         print("".join([str((sdf.GetColumnNames())[ii]), " ( type -> ", sdf.GetColumnType(sdf.GetColumnNames()[ii]), " )"]))
                                        #     print("".join(["\tTotal length= ", str(len(sdf.GetColumnNames()))]))
                                        #     print("\n\n\n\n\n")

                                        ## Filter for the Q2-xB Bins
                                        Bin_Filter = "esec != -2" if(Q2_xB_Bin_Num == -1) else "".join([str(Q2_xB_Bin_Filter_str), " != 0"]) if(Q2_xB_Bin_Num == -2) else "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Num)])
                                        
                                        ## Cut for 1D bin migration (don't use for the Q2, xB, z, and pT variables - will result in improper cuts within those plots)
                                        if(("Bin" not in str(variable)) and (Histo_Data in ["mdf", "pdf", "gen"]) and "'phi_t" in str(variable)):
                                            # 1D Unfolding requires events be generated and reconstructed in the same bin
                                            Bin_Filter = "".join(["".join([str(Bin_Filter), " && "]) if(Bin_Filter != "esec != -2") else "", str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter_str).replace("_smeared", "") , "_gen", " && ", str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter_str).replace("_smeared", "") , "_gen"])
                                        
                                        if((Histo_Data in ["mdf", "pdf", "gen"]) and (("Combined" in str(variable) or "Multi_Dim" in str(variable)) and str(Q2_xB_Bin_Filter_str).replace("_smeared", "") in str(variable))):
                                            # Multidimensional unfolding should still exclude bin migration from other kinematic bins not included in the response matrix
                                            Bin_Filter = "".join(["".join([str(Bin_Filter), " && "]) if(Bin_Filter != "esec != -2") else "",                                                                                                        str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter_str).replace("_smeared", "") , "_gen"])
                                        if(("Combined" in str(variable) or "Multi_Dim" in str(variable)) and (str(Q2_xB_Bin_Filter_str).replace("_smeared", "") in str(variable))):
                                            Bin_Filter = "".join([str(Bin_Filter), " && ", str(Q2_xB_Bin_Filter_str), " != 0", "".join([" && ", str((Q2_xB_Bin_Filter_str).replace("_smeared", "")).replace("_gen", ""), "_gen != 0"]) if(Histo_Data in ["mdf", "pdf", "gen"]) else ""])
                                            
                                        Migration_Title       = "".join([str(Migration_Title),   "; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))])
                                        if(Histo_Data in ["mdf"]):
                                            Migration_Title_2 = "".join([str(Migration_Title_2), "; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))])
                                            
                                ##############################################################################################=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                #####====================#####     Making the Histos (START)    #####====================#####=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                ##############################################################################################=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####     Original Version of Histograms                     #####================#####=======================########################################################################################################################################################################################################################################################################################################################################################################################################
                                        # if(False):
                                        #     # Running Original Version without the option of weighing the events/using generated Missing Mass Cuts
                                        #     if(Histo_Data in ["mdf", "pdf"]):
                                        #         if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                        #         # if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable) and "z_pT_Bin" not in str(variable))):
                                        #         # if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                        #             # Do not need to see the z-pT bins for these plots
                                        #             Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
                                        #             Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
                                        #             Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
                                        #             Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                        #             # if("Multi_Dim_" in str(variable)):
                                        #             #     print(color.BOLD, "\nstr(Histo_Name), str(Migration_Title_Simple), str(int(num_of_GEN_bins)), str(min_GEN_bin), str(Max_GEN_bin), str(int(num_of_REC_bins)), str(min_REC_bin), str(Max_REC_bin), str(Variable_Gen), str(Variable_Rec) =\n  ", color.GREEN, ", ".join([str(Histo_Name), str(Migration_Title_Simple), str(int(num_of_GEN_bins)), str(min_GEN_bin), str(Max_GEN_bin), str(int(num_of_REC_bins)), str(min_REC_bin), str(Max_REC_bin), str(Variable_Gen), str(Variable_Rec)]), color.END)
                                        #             #     print(color.BLUE, "\nVar_List =", Var_List, color.END)
                                        #             #     print("\n\nfor column_name in sdf.GetColumnNames():")
                                        #             #     for column_name in sdf.GetColumnNames():
                                        #             #         print("\t", str(column_name))
                                        #             #     print("\n\n")
                                        #             Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),    str(Migration_Title_Simple), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                              str(Variable_Gen), str(Variable_Rec))
                                        #         else:
                                        #             Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name),    str(Migration_Title),        int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                        #         if(Histo_Data == "mdf"):
                                        #             if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin"]) or ("Multi_Dim_" in str(variable))):
                                        #             # if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin"]) or ("Multi_Dim_" in str(variable) and "z_pT_Bin" not in str(variable))):
                                        #             # if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                        #                 # Do not need to see the z-pT bins for these plots
                                        #                 Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
                                        #                 Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
                                        #                 Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
                                        #                 Migration_Title_Simple        = str(Migration_Title_2.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                        #                 Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
                                        #             else:
                                        #                 Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_2),      int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                        #     else:
                                        #         # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                        #         if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin"]) or ("Multi_Dim_" in str(variable))):
                                        #         # if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin"]) or ("Multi_Dim_" in str(variable) and "z_pT_Bin" not in str(variable))):
                                        #         # if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                        #             # Do not need to see the z-pT bins for these plots
                                        #             Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
                                        #             Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
                                        #             Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
                                        #             Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                        #             Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
                                        #         else:
                                        #             Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                    #####================#####                                                        #####================#####=======================########################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####     Original Version of Histograms                     #####================#####=======================########################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####==============#################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####=========######################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####     Generated Missing Mass Cut Version of Histograms   #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####                                                        #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                        # # elif(("phi_" not in str(variable)) or (not Use_Weight)):
                                        # elif(not Use_Weight):
                                        if(not Use_Weight):
                                            # Running with Generated Missing Mass Cuts but without weighing the events
                                            #####         Matched Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            if(Histo_Data in ["mdf", "pdf"]):
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name)):
                                                        Histo_Name_No_Cut  = Histo_Name
                                                        Histo_Name_MM_Cut  = Histo_Name.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_No_Cut  = Histo_Name.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_MM_Cut  = Histo_Name

                                                    Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                    
                                                    Migration_Title_No_Cut            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Count"))
                                                    Migration_Title_MM_Cut            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                    Migration_Title_MM_Cut            = str(Migration_Title_MM_Cut).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    
                                                    # Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),  str(Migration_Title_Simple),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                   str(Variable_Gen), str(Variable_Rec))
                                                    
                                                    Histograms_All[Histo_Name_No_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_No_Cut),  str(Migration_Title_No_Cut),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                    str(Variable_Gen), str(Variable_Rec))
                                                    Histograms_All[Histo_Name_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_MM_Cut),  str(Migration_Title_MM_Cut),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  3, -1.5, 1.5),                                                                     str(Variable_Gen), str(Variable_Rec),                              "Missing_Mass_Cut_Gen")
                                                    
                                                else:
                                                    if((", (Gen_MM_Cut)" not in str(Histo_Name)) and (", (Gen_Cut_MM)" not in str(Histo_Name))):
                                                        Histo_Name__No_Cut = Histo_Name
                                                        Histo_Name_Cutting = Histo_Name.replace("))", "), (Gen_Cut_MM))")
                                                        Histo_Name__MM_Cut = Histo_Name.replace("))", "), (Gen_MM_Cut))")
                                                    elif(", (Gen_MM_Cut)"    in str(Histo_Name)):
                                                        Histo_Name__No_Cut = Histo_Name.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_Cutting = Histo_Name.replace("), (Gen_MM_Cut))", "), (Gen_Cut_MM))")
                                                        Histo_Name__MM_Cut = Histo_Name
                                                    elif(", (Gen_Cut_MM)"    in str(Histo_Name)):
                                                        Histo_Name__No_Cut = Histo_Name.replace("), (Gen_Cut_MM))", "))")
                                                        Histo_Name_Cutting = Histo_Name
                                                        Histo_Name__MM_Cut = Histo_Name.replace("), (Gen_Cut_MM))", "), (Gen_MM_Cut))")
                                                    
                                                    Hist_Title_NCut = str(Migration_Title)
                                                    Hist_Title__Cut = str(Migration_Title).replace("Cuts}}}{#scale[1.35]{", "Cuts - Events Removed by Generated Cut}}}{#scale[1.35]{")
                                                    Hist_Title_WCut = str(Migration_Title).replace("Cuts}}}{#scale[1.35]{", "Cuts - With Generated Missing Mass Cut}}}{#scale[1.35]{")

                                                    Histograms_All[Histo_Name__No_Cut] = (sdf.Filter(         str(Bin_Filter)                                  )).Histo3D((str(Histo_Name__No_Cut), str(Hist_Title_NCut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                    Histograms_All[Histo_Name_Cutting] = (sdf.Filter("".join([str(Bin_Filter), " && Missing_Mass_Cut_Gen < 0"]))).Histo3D((str(Histo_Name_Cutting), str(Hist_Title__Cut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                    Histograms_All[Histo_Name__MM_Cut] = (sdf.Filter("".join([str(Bin_Filter), " && Missing_Mass_Cut_Gen > 0"]))).Histo3D((str(Histo_Name__MM_Cut), str(Hist_Title_WCut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                    
                                                if(Histo_Data in ["mdf"]):
                                                    if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                        # Do not need to see the z-pT bins for these plots
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                        if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                        else:
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D
                                                            
                                                        Migration_Title_Simple   = str(Migration_Title_2.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                        Histo_Title__1D_MM_Cut   = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                        Histo_Title__1D_No_Cut   = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Counts"))

                                                        Histograms_All[Histo_Name_1D_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_MM_Cut), str(Histo_Title__1D_MM_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   3, -1.5, 1.5),                                                                                        str(Variable_Rec),                              "Missing_Mass_Cut_Gen")
                                                        Histograms_All[Histo_Name_1D_No_Cut] = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D_No_Cut), str(Histo_Title__1D_No_Cut).replace("; Gen MM Cut", ""),                                                                                           int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec))
                                                    else:
                                                        if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                        else:
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D
                                                        
                                                        
                                                        Histo_Name_1D_MCut_Title = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                        Histo_Name_1D_NCut_Title = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Counts"))
                                                        
                                                        Histograms_All[Histo_Name_1D_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D_MM_Cut), str(Histo_Name_1D_MCut_Title),                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5),           str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen")
                                                        Histograms_All[Histo_Name_1D_No_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_No_Cut), str(Histo_Name_1D_NCut_Title),                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                        
                                            #####       Generated Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            elif(Histo_Data in ["gdf", "gen"]):
                                                # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen")
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D
                                                    Migration_Title_Simple       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    
                                                    Histo_Title__1D_MM_Cut       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    Histo_Title__1D_No_Cut       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                        
                                                    Histograms_All[Histo_Name_1D_MM_Cut]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_MM_Cut), str(Histo_Title__1D_MM_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                                3, -1.5, 1.5),           str(Variable_Rec),                              "Missing_Mass_Cut_Gen")
                                                    Histograms_All[Histo_Name_1D_No_Cut]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D_No_Cut), str(Histo_Title__1D_No_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec))
                                                    
                                                else:
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D
                                                        
                                                    Histo_Title_1D_MM_Cut        = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    Histo_Title_1D_No_Cut        = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    
                                                    Histograms_All[Histo_Name_1D_MM_Cut]     = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D_MM_Cut), str(Histo_Title_1D_MM_Cut),                                                                                                                        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5),           str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen")
                                                    Histograms_All[Histo_Name_1D_No_Cut]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_No_Cut), str(Histo_Title_1D_No_Cut),                                                                                                                        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))

                                            #####           Experimental Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            else:
                                                # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
                                                    Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple),                                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec))
                                                else:
                                                    Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),                                                                                                                                            int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                    
                                    #####================#####                                                        #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####     Generated Missing Mass Cut Version of Histograms   #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####========================================================#####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####    Generated Missing Mass Cut with Weighed Histograms  #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    #####================#####                                                        #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                        else:
                                            # Running Weighed Version of events with the generated Missing Mass Cuts
                                            #####         Matched Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            if(Histo_Data in ["mdf", "pdf"]):
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name)):
                                                        Histo_Name_No_Cut  = Histo_Name
                                                        Histo_Name_MM_Cut  = Histo_Name.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_No_Cut  = Histo_Name.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_MM_Cut  = Histo_Name

                                                    Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                    
                                                    Migration_Title_No_Cut            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Count"))
                                                    Migration_Title_MM_Cut            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                    Migration_Title_MM_Cut            = str(Migration_Title_MM_Cut).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    
                                                    # Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),  str(Migration_Title_Simple),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                   str(Variable_Gen), str(Variable_Rec))
                                                    
                                                    Histograms_All[Histo_Name_No_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_No_Cut),  str(Migration_Title_No_Cut),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                    str(Variable_Gen), str(Variable_Rec),                                                      "Event_Weight")
                                                    Histograms_All[Histo_Name_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_MM_Cut),  str(Migration_Title_MM_Cut),                                                                                                                                       int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  3, -1.5, 1.5),                                                                     str(Variable_Gen), str(Variable_Rec),                              "Missing_Mass_Cut_Gen", "Event_Weight")
                                                    
                                                else:
                                                    if((", (Gen_MM_Cut)" not in str(Histo_Name)) and (", (Gen_Cut_MM)" not in str(Histo_Name))):
                                                        Histo_Name__No_Cut = Histo_Name
                                                        Histo_Name_Cutting = Histo_Name.replace("))", "), (Gen_Cut_MM))")
                                                        Histo_Name__MM_Cut = Histo_Name.replace("))", "), (Gen_MM_Cut))")
                                                    elif(", (Gen_MM_Cut)"    in str(Histo_Name)):
                                                        Histo_Name__No_Cut = Histo_Name.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_Cutting = Histo_Name.replace("), (Gen_MM_Cut))", "), (Gen_Cut_MM))")
                                                        Histo_Name__MM_Cut = Histo_Name
                                                    elif(", (Gen_Cut_MM)"    in str(Histo_Name)):
                                                        Histo_Name__No_Cut = Histo_Name.replace("), (Gen_Cut_MM))", "))")
                                                        Histo_Name_Cutting = Histo_Name
                                                        Histo_Name__MM_Cut = Histo_Name.replace("), (Gen_Cut_MM))", "), (Gen_MM_Cut))")
                                                    
                                                    Hist_Title_NCut = str(Migration_Title)
                                                    Hist_Title__Cut = str(Migration_Title).replace("Cuts}}}{#scale[1.35]{", "Cuts - Events Removed by Generated Cut}}}{#scale[1.35]{")
                                                    Hist_Title_WCut = str(Migration_Title).replace("Cuts}}}{#scale[1.35]{", "Cuts - With Generated Missing Mass Cut}}}{#scale[1.35]{")

                                                    Histograms_All[Histo_Name__No_Cut] = (sdf.Filter(         str(Bin_Filter)                                  )).Histo3D((str(Histo_Name__No_Cut), str(Hist_Title_NCut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]),                         "Event_Weight")
                                                    Histograms_All[Histo_Name_Cutting] = (sdf.Filter("".join([str(Bin_Filter), " && Missing_Mass_Cut_Gen < 0"]))).Histo3D((str(Histo_Name_Cutting), str(Hist_Title__Cut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]),                         "Event_Weight")
                                                    Histograms_All[Histo_Name__MM_Cut] = (sdf.Filter("".join([str(Bin_Filter), " && Missing_Mass_Cut_Gen > 0"]))).Histo3D((str(Histo_Name__MM_Cut), str(Hist_Title_WCut),                                                                                      int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),      str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]),                         "Event_Weight")
                                                    
                                                if(Histo_Data in ["mdf"]):
                                                    if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                        # Do not need to see the z-pT bins for these plots
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                        Histo_Name_1D            = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                        if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                        else:
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D
                                                            
                                                        Migration_Title_Simple   = str(Migration_Title_2.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
                                                        Histo_Title__1D_MM_Cut   = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                        Histo_Title__1D_No_Cut   = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Counts"))

                                                        Histograms_All[Histo_Name_1D_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_MM_Cut), str(Histo_Title__1D_MM_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   3, -1.5, 1.5),                                                                                        str(Variable_Rec),                              "Missing_Mass_Cut_Gen", "Event_Weight")
                                                        Histograms_All[Histo_Name_1D_No_Cut] = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D_No_Cut), str(Histo_Title__1D_No_Cut).replace("; Gen MM Cut", ""),                                                                                           int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec),                                                      "Event_Weight")
                                                    else:
                                                        if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                        else:
                                                            Histo_Name_1D_No_Cut = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                            Histo_Name_1D_MM_Cut = Histo_Name_1D
                                                        
                                                        
                                                        Histo_Name_1D_MCut_Title = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                        Histo_Name_1D_NCut_Title = str(Migration_Title_2.replace("".join(["; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))]), "; Counts"))
                                                        
                                                        Histograms_All[Histo_Name_1D_MM_Cut] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D_MM_Cut), str(Histo_Name_1D_MCut_Title),                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5),           str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen", "Event_Weight")
                                                        Histograms_All[Histo_Name_1D_No_Cut] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_No_Cut), str(Histo_Name_1D_NCut_Title),                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]),                         "Event_Weight")
                                                        
                                            #####       Generated Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            elif(Histo_Data in ["gdf", "gen"]):
                                                # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen")
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
                                                    Histo_Name_1D                = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D
                                                    Migration_Title_Simple       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    
                                                    Histo_Title__1D_MM_Cut       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    Histo_Title__1D_No_Cut       = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                        
                                                    Histograms_All[Histo_Name_1D_MM_Cut]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_MM_Cut), str(Histo_Title__1D_MM_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                                3, -1.5, 1.5),           str(Variable_Rec),                              "Missing_Mass_Cut_Gen", "Event_Weight")
                                                    Histograms_All[Histo_Name_1D_No_Cut]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D_No_Cut), str(Histo_Title__1D_No_Cut),                                                                                                                       int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec),                                                      "Event_Weight")
                                                    
                                                else:
                                                    if(", (Gen_MM_Cut)" not in str(Histo_Name_1D)):
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D.replace("))", "), (Gen_MM_Cut))")
                                                    else:
                                                        Histo_Name_1D_No_Cut     = Histo_Name_1D.replace("), (Gen_MM_Cut))", "))")
                                                        Histo_Name_1D_MM_Cut     = Histo_Name_1D
                                                        
                                                    Histo_Title_1D_MM_Cut        = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut")).replace("Cuts}}}{#scale[1.35]{", "Cuts - with Generated Cut}}}{#scale[1.35]{")
                                                    Histo_Title_1D_No_Cut        = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    
                                                    Histograms_All[Histo_Name_1D_MM_Cut]     = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D_MM_Cut), str(Histo_Title_1D_MM_Cut),                                                                                                                        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5),           str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen", "Event_Weight")
                                                    Histograms_All[Histo_Name_1D_No_Cut]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D_No_Cut), str(Histo_Title_1D_No_Cut),                                                                                                                        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]),                         "Event_Weight")

                                            #####           Experimental Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
                                            else:
                                                # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
                                                    Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
                                                    Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
                                                    Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple),                                                                                                                                     int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                                                                                        str(Variable_Rec))
                                                else:
                                                    Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),                                                                                                                                            int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),                         str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                                    
#                                             if(Histo_Data in ["mdf", "pdf"]):
#                                                 if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                                     # Do not need to see the z-pT bins for these plots
#                                                     Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                                     Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                                     Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                                     if(count_of_histograms > 150):
#                                                         print("".join([str(count_of_histograms), ") Histo_Name = ", str(Histo_Name)]))
#                                                     Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
#                                                     # Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),  str(Migration_Title_Simple),                                                                                 int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                                            str(Variable_Gen), str(Variable_Rec))
#                                                     Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name),  str(Migration_Title_Simple),                                                                                 int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  3, -1.5, 1.5),                                                                              str(Variable_Gen), str(Variable_Rec),           "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                                     Histograms_All[Histo_Name].GetZaxis().SetTitle("Gen MM Cut")
#                                                 else:
#                                                     if(", (Gen_MM_Cut)" not in str(Histo_Name)):
#                                                         Histo_Name_No_Cut = Histo_Name
#                                                         Histo_Name_MM_Cut = Histo_Name.replace("))", "), (Gen_MM_Cut))")
#                                                     else:
#                                                         Histo_Name_No_Cut = Histo_Name.replace("), (Gen_MM_Cut))", "))")
#                                                         Histo_Name_MM_Cut = Histo_Name
#                                                     if(count_of_histograms > 150):
#                                                         print("".join([str(count_of_histograms), ") Histo_Name_No_Cut = ", str(Histo_Name_No_Cut)]))
#                                                         print("".join([str(count_of_histograms), ") Histo_Name_MM_Cut = ", str(Histo_Name_MM_Cut)]))
#                                                         print("DONE")
#                                                         continue
#                                                     Histograms_All[Histo_Name_No_Cut] = (sdf.Filter(       str(Bin_Filter))).Histo3D((str(Histo_Name_No_Cut),                         str(Migration_Title),                                              int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),               str(Variable_Gen), str(Variable_Rec),           str(Res_Binning_2D_z_pT[0]), "Event_Weight")
#                                                     MM_cut_sdf                        = sdf.Filter("Missing_Mass_Cut_Gen > 0")
#                                                     Histograms_All[Histo_Name_MM_Cut] = (MM_cut_sdf.Filter(str(Bin_Filter))).Histo3D((str(Histo_Name_MM_Cut), "".join(["#splitline{", str(Migration_Title), "}{Added Cut on Generated Missing Mass}"]),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),               str(Variable_Gen), str(Variable_Rec),           str(Res_Binning_2D_z_pT[0]), "Event_Weight")
#                                                 if(Histo_Data in ["mdf"]):
#                                                     if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                                         # Do not need to see the z-pT bins for these plots
#                                                         Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                                         Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                                         Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                                         if(count_of_histograms > 150):
#                                                             print("".join([str(count_of_histograms), ") Histo_Name_1D = ", str(Histo_Name_1D)]))
#                                                             print("\n\n")
#                                                         Migration_Title_Simple        = str(Migration_Title_2.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
#                                                         Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_Simple),                                                                               int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                                3, -1.5, 1.5), str(Variable_Rec),                              "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                                         Histograms_All[Histo_Name_1D].GetYaxis().SetTitle("Gen MM Cut")
#                                                         Histograms_All[Histo_Name_1D].GetZaxis().SetTitle("Counts")
#                                                     else:
#                                                         Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title_2),                                                                                    int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                   int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                                         Histograms_All[Histo_Name_1D].GetZaxis().SetTitle("Gen MM Cut")
#                                             #####       Generated Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
#                                             elif(Histo_Data in ["gdf", "gen"]):
#                                                 # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen")
#                                                 if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                                     # Do not need to see the z-pT bins for these plots
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                                     Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
#                                                     Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                              3, -1.5, 1.5), str(Variable_Rec),                              "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                                     Histograms_All[Histo_Name_1D].GetYaxis().SetTitle("Gen MM Cut")
#                                                     Histograms_All[Histo_Name_1D].GetZaxis().SetTitle("Counts")
#                                                 else:
#                                                     Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                                     Histograms_All[Histo_Name_1D].GetZaxis().SetTitle("Gen MM Cut")
#                                             #####           Experimental Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
#                                             else:
#                                                 # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
#                                                 if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                                     # Do not need to see the z-pT bins for these plots
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
#                                                     Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
#                                                     Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
#                                                     Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                               str(Variable_Rec))
#                                                 else:
#                                                     Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
#                                     #####================#####    Generated Missing Mass Cut with Weighed Histograms  #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################                                    
#                                             #     #######################################
#                                             # #####         Matched Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
#                                             #     #######################################
#                                             # if(Histo_Data in ["mdf", "pdf"]):
#                                             #     if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                             #         # Do not need to see the z-pT bins for these plots
#                                             #         Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
#                                             #         # Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),    str(Migration_Title_Simple), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                              str(Variable_Gen), str(Variable_Rec))
#                                             #         Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name),    str(Migration_Title_Simple), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                              3, -1.5, 1.5), str(Variable_Gen), str(Variable_Rec),           "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #     else:
#                                             #         Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name),    str(Migration_Title),        int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]),               str(Variable_Gen), str(Variable_Rec),           str(Res_Binning_2D_z_pT[0]), "Event_Weight")
#                                             #     if(Histo_Data == "mdf"):
#                                             #         if((str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                             #             # Do not need to see the z-pT bins for these plots
#                                             #             Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                             #             Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                             #             Histo_Name_1D                 = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                             #             Migration_Title_Simple        = str(Migration_Title_2.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), "; Gen MM Cut"))
#                                             #             Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                              3, -1.5, 1.5), str(Variable_Rec),                              "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #         else:
#                                             #             Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title_2),      int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #     #######################################
#                                             # #####       Generated Events Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
#                                             #     #######################################
#                                             # elif(Histo_Data in ["gdf", "gen"]):
#                                             #     # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #     if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                             #         # Do not need to see the z-pT bins for these plots
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ", (Gen_MM_Cut)"))
#                                             #         Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
#                                             #         Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                                                                                              3, -1.5, 1.5), str(Variable_Rec),                              "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #     else:
#                                             #         Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,                                                 int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2], 3, -1.5, 1.5), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Missing_Mass_Cut_Gen",      "Event_Weight")
#                                             #     #######################################
#                                             # #####           Experimental Data         #####################################################################################################################################################################################################################################################################################################################################################################################################################
#                                             #     #######################################
#                                             # else:
#                                             #     # Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
#                                             #     if((str(variable).replace("_smeared", "")     in ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]) or ("Multi_Dim_" in str(variable))):
#                                             #         # Do not need to see the z-pT bins for these plots
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""))
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=45, MinBin=-1.5, MaxBin=43.5])"]), ""))
#                                             #         Histo_Name_1D                     = str((Histo_Name_1D).replace("".join([", (Var-D2='", str(z_pT_Bin_Filter_str), "'-[NumBins=43, MinBin=-0.5, MaxBin=42.5])"]), ""))
#                                             #         Migration_Title_Simple            = str(Migration_Title.replace("".join(["; ", variable_Title_name(z_pT_Bin_Filter_str)]), ""))
#                                             #         Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), int(num_of_REC_bins), min_REC_bin, Max_REC_bin),                                                                               str(Variable_Rec))
#                                             #     else:
#                                             #         Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        int(num_of_REC_bins), min_REC_bin, Max_REC_bin,  int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
#                                     #####================#####    Generated Missing Mass Cut with Weighed Histograms  #####================#####=====##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                    
                                    
                                ##############################################################################################=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                #####====================#####       Made the Histos (END)      #####====================#####=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                ##############################################################################################=======================##########################################################################################################################################################################################################################################################################################################################################################################################################################
                                
                                
                                        for Histo_To_Save in [Histo_Name_No_Cut, Histo_Name_MM_Cut, Histo_Name__No_Cut, Histo_Name_Cutting, Histo_Name__MM_Cut, Histo_Name_1D_MM_Cut, Histo_Name_1D_No_Cut]:
                                            if(Histo_To_Save not in ["N/A"]):
                                                if(Histo_To_Save in Histograms_All):
                                                    if(str(file_location) not in ['time']):
                                                        Histograms_All[Histo_To_Save].Write()
                                                    Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                                    count_of_histograms += 1
                                                else:
                                                    print(color.Error, "\nERROR WHILE SAVING HISTOGRAM:\n", color.END, color.BOLD, "Histograms_All[", Histo_To_Save, "] was not found\n", color.END)
                                        if((str(Histo_Name) not in [Histo_Name_No_Cut, Histo_Name_MM_Cut, Histo_Name__No_Cut, Histo_Name_Cutting, Histo_Name__MM_Cut, Histo_Name_1D_MM_Cut, Histo_Name_1D_No_Cut]) and (Histo_Name in Histograms_All)):
                                            if(str(file_location) not in ['time']):
                                                Histograms_All[Histo_Name].Write()
                                            Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 1
                                        if((str(Histo_Name_1D) not in [Histo_Name_1D_MM_Cut, Histo_Name_1D_No_Cut]) and (Histo_Name_1D in Histograms_All)):
                                            if(str(file_location) not in ['time']):
                                                Histograms_All[Histo_Name_1D].Write()
                                            Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 1
                                        if(output_all_histo_names_Q not in ["yes"]):
                                            del Histograms_All
                                            Histograms_All = {}
#                                         if(Histo_Data == "mdf"):
#                                             if(str(file_location) != 'time'):
#                                                 if("N/A" in [str(Histo_Name_No_Cut), str(Histo_Name_MM_Cut)]):
#                                                     Histograms_All[Histo_Name].Write()
#                                                 else:
#                                                     Histograms_All[Histo_Name_No_Cut].Write()
#                                                     Histograms_All[Histo_Name_MM_Cut].Write()
#                                                 Histograms_All[Histo_Name_1D].Write()
#                                             if(output_all_histo_names_Q != "yes"):
#                                                 del Histograms_All
#                                                 Histograms_All = {}
#                                             if("N/A" in [str(Histo_Name_No_Cut), str(Histo_Name_MM_Cut)]):
#                                                 Print_Progress(count_of_histograms, 2, 200 if(str(file_location) != 'time') else 50)
#                                                 count_of_histograms += 2
#                                             else:
#                                                 Print_Progress(count_of_histograms, 3, 200 if(str(file_location) != 'time') else 50)
#                                                 count_of_histograms += 3
#                                         else:
#                                             if(str(file_location) != 'time'):
#                                                 Histograms_All[Histo_Name_1D].Write()
#                                             if(output_all_histo_names_Q != "yes"):
#                                                 del Histograms_All
#                                                 Histograms_All = {}
#                                             Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
#                                             count_of_histograms += 1
                                            
                                    
                                    del sdf
                                    


######################################################################
##=====##=====##=====##    End of Main Loop    ##=====##=====##=====##
######################################################################

        ######################################===============================######################################
        ##==========##==========##==========##          End of Code          ##==========##==========##==========##
        ######################################===============================######################################

        if(str(file_location) != 'time'):
            ROOT_File_Output.Close()
        # File has been saved
        
        print("".join([color.BOLD, "\nTotal Number of Histograms Made: ", str(count_of_histograms), color.END]))
        
        # See beginning of code...
        if(output_all_histo_names_Q == "yes"):
            ii_num = 1
            print("\nHistograms made:")
            for ii in Histograms_All:
                print("".join(["Histo ", str(ii_num), ") ", color.BOLD, str(ii), color.END]))
                ii_num += 1
                if(";" in str(ii)):
                    print("".join([color.RED, "SEMI-COLON ERROR: ", str(ii), color.END]))
            print("\n")
        elif(str(file_location) == "time"):
            print("\nChoose not to print list of final histograms...\nSet output_all_histo_names_Q = 'yes' or enter 'test' instead of a file name to print a list of histograms made while running...\n")
        
    elif(output_type not in ["histo", "test", "time"]):
        print("Taking Snapshot...")
        rdf.Snapshot("h22", ROOT_File_Output_Name)
        print("Done\n\n")
    
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
        
    print("".join(["Made ", str(count_of_histograms), " histograms..."]))
        
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
    print("".join([str(Num_of_Days), " Day(s), ", str(Num_of_Hrs), " Hour(s), and ", str(Num_of_Mins), " Minute(s)."]))
    
    if((((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins) != 0):
        rate_of_histos = count_of_histograms/(((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins)
        print("".join(["Rate of Histos/Minute = ", str(rate_of_histos), " Histos/Min"]))
    
    if(str(file_location) in ['time' , 'test']):
        print("".join(["\nEstimated time to run: ", "".join([str(round(count_of_histograms/6, 4)), " mins"]) if(round(count_of_histograms/6, 4) < 60) else  "".join([str(int(round(count_of_histograms/6, 4)/60)), " hrs and ", str(round(((round(count_of_histograms/6, 4)/60)%1)*60, 3)), " mins (Total: ", str(round(count_of_histograms/6, 3)), " mins)"])]))
        # Estimate based on observations made on 12-2-2022 (estimates are very rough - based on the "mdf" run option)
    
    print("\n")
    
    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
else:
    print("\nERROR: No valid datatype selected...\n")