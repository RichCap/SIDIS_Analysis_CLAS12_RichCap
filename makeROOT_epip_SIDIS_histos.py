# This Code was last updated on 7-18-2022
# # Note-to-self: Also always update this note at end of script


# Most recent update notes:

# # On 7-18-2022:
    # # 1) Moved File Locations (new folders and data file)
    # # 2) New File name

# # On 6-7-2022:
    # # 1) Histograms 20 Bin option
    # # 2) Fixed Bin Migration Histograms
        # (*) phi_t not (pre)defined properly for V4
        # (*) Overflow bins set to 0 and bin_option + 1 (unmatched bin is bin_option + 2)
        # (*) One extra bin is given above the unmatched bin so that an empty bin can make room for the z-axis scale
        # (*) Axis is shifted so that the center of each bin is located at the bin's number (easier to read)
    # # 3) Name is now: V25_20_Bin_Test

# # On 6-6-2022:
    # # 1) Histograms 20 Bin option
    # # 2) New Bin Migration Histograms added
        # (*) Runs all bin options at once (bins = 2, 3, 4, 5, 10, 20, and 40)
        # (*) Kinematic ranges are pre-defined for each variable (using max ranges of the 2D binning scheme previously developed)
        # (*) Binning is extended slightly beyond the overflow + unmatched binning ranges for 2 reasons, namely:
                    # 1) Avoid possible issues with getting the bin numbers wrong
                    # 2) If the above note is a non-issue, then to simply give more room in the histograms' borders
    # # 3) Name is now: V24_20_Bin_Test

# # On 6-3-2022:
    # # 1) Using 20 Bin option (rerunning with fixes)
    # # 2) Fixed issues with the bin migration histograms
        # (*) Added information of events outside the given kinematic binning for REC events (previously only applied to GEN events)
        # (*) Fixed issue with some histograms being saved over
        # (*) Flipped the x and y axis (visual change)
    # # 5) Name is now: V23_20_Bin_Test

# # On 6-2-2022:
    # # 1) Using 20 Bin option (rerunning with new options)
    # # 2) Updated Binning for Q2 and xB (other variables remain the same)
    # # 3) Running "gen" variable option
    # # 4) Added new set of bin migration histograms that use variable bins instead of the variable's values to plot
        # (*) Also added information of events outside the given kinematic binning (i.e., above/below the defined range as well as information on unmatched events)
    # # 5) Name is now: V22_20_Bin_Test


# # On 5-25-2022:
    # # 1) Using 20 Bin option (rerunning for bin migration histograms)
    # # 2) Changed bin migration histograms into 1 2D histogram per variable instead of 1 1D histogram for each REC bin of each variable (reduces number of calculations)
    # # 3) Made the (new) bin migration histograms use the kinematic values for plotting instead of the actual bin numbers
    # # 4) Added the kinematic variable 'y' back into the 1D and 2D histogram lists
    # # 2) Name is now: V21_20_Bin_Test

# # On 5-24-2022:
    # # 1) Using 10 Bin option (rerunning for bin migration histograms)
    # # 2) Name is now: V20_10_Bin_Test

# # On 5-24-2022:
    # # 1) Using 4 Bin option (New)
    # # 2) Name is now: V20_4_Bin_Test

# # On 5-24-2022:
    # # 1) Error noticed in migration histograms - needed to rerun (did not use the correct histogram binning)
    # # 2) Using 5 Bin option
    # # 3) Name is now: V20_5_Bin_Test

# # On 5-23-2022:
    # # 1) Another new fewer bin option (3 bins of data)
    # # 2) Name is now: V19_3_Bin_Test

# # On 5-23-2022:
    # # 1) New fewer bin option (2 bins of data - Needed to run twice due to error in option choice)
    # # 2) Name is now: V19_2_Bin_Test

# # On 5-23-2022:
    # # 1) Added information on where the 'non-pure'/migrated events are migrating from (updated name from V18 to V19)
    # # 2) Re-tested version of binning 1D binning (~5 bin option)
    # # 3) Name is now: V19_5_Bin_Test

# # On 5-19-2022:
    # # 1) Tested next version of binning 1D binning (largest option)
    # # 2) Name is now: V18_40_Bin_Test

# # On 5-18-2022:
    # # 1) Tested next version of binning 1D binning (2nd largest option)
    # # 2) Name is now: V18_15_Bin_Test (should have been titles V18_20_Bin_Test)

# # On 5-18-2022:
    # # 1) Tested next version of binning 1D binning (2nd smallest option)
    # # 2) Name is now: V18_10_Bin_Test

# # On 5-18-2022:
    # # 1) Removed many options that are not currently useful including:
        # (*) 2D purity counts
        # (*) All Q2-xB bins (just running "all" events)
        # (*) Cut option without the new Q2 cut
        # (*) Kinematics of the electron and π+ momentum and angles (i.e., only plotting Q2, xB, z, pT, and phi_t)
    # # 2) Changed the new binning and cut to start at Q2 = 2 GeV^2 instead of at 1.95 GeV^2
    # # 3) Starting tests of new 1D binning (currently testing smallest 1D bin option)
    # # 4) Name is now: V18_5_Bin_Test

# # On 5-17-2022:
    # # 1) Error in V16 which caused the 2D bin purity histograms to not be run properly (now fixed)
    # # 2) phi_t binning is now set to 36 bins (i.e., 10˚ per bin)
    # # 3) Name is now up to "Purity_V17"

# # On 5-16-2022:
    # # 1) Forgot to log update for V15
        # (*) Code was updated between 5-10-2022 and 5-16-2022
    # # 2) 2D Binning was not updated properly 
        # (*) z-pT bins always used old binning scheme when making cuts - Fixed in update
    # # 3) phi_t binning is now set to 45 bins (i.e., 8˚ per bin)
    # # 4) "Purity_V15" crashed while running (Now it should be fixed)
    # # 5) Name is now up to "Purity_V16"


# # On 5-10-2022:
    # # 1) Forgot to update the code to use the Rules_5 (from groovy)
        # (*) These rules had the fixed phi matching criteria (Max ∆Phi = 180˚)
    # # 2) Name is now up to "Purity_V14_New_"
        # (*) Did not go up to V15 because all else should be the same

# # On 5-9-2022:
    # # 1) Reduced the number of histograms to be created
      # # Removed:
        # (*) 2D Bin purity cut
        # (*) GEN histograms (matched from pdf) 
    # # 2) Made the 2D histogram binning smaller than the 1D bins (10 times as many bins for the same ranges)
        # (*) Shows the defined binning (based on Stefan's 2D bins) better
    # # 3) Redid how the count histogram works to make the axis labels strings instead of integers (should be easier to read with some formatting help)
    # # 4) Added an option to take a snapshot of the dataframe
        # (*) Produces a ROOT file with the TTree instead of histograms (like what the groovy script does)
        # (*) All old code (i.e., the .sh files) should be compadible with this change, as the code will default to working the same way as before
        # (*) NOTE: Files can be increadibly large. This feature might not be useful unless specific columns from the dataframe are selected to be outputted (option remains despite its current lack of usefulness)
    # # 5) Name is now up to "Purity_V14_"

# # On 5-3-2022:
    # # 1) Reduced the number of histograms to be created
      # # Removed:
        # (*) Some Q2-xB bins
        # (*) Specific particle mis-identification
        # (*) Q2 < 2 cut
        # (*) y plots (1D and 2D), MM plots, and W plots
    # # 2) Name is now up to "Purity_V13_"


# # On 5-2-2022:
    # # 1) Updated Matching criteria (changed best match in groovy code)
    # # 2) Added new type of 2D binning 
      # # (*) Change stefan's binning to accommodate the cut on Q2 < 2
      # # (*) New definition has 1 less bin as Bin 1 is combined with the original Bin 3 (even numbered bins are the same but odd numbered bins are number 2 less than they were - i.e., Bin 5 would now be Bin 3 and Bin 9 is now called Bin 7)
      # # (*) Original binning still being used
    # # 3) Added purity calculation to Q2-xB bins
    # # 4) Changed phi_t binning again (8 degrees per bin - Range = 0-360 and # of Bins = 45)
    # # 5) Name is now up to "Purity_V12_"

# # On 4-26-2022:
    # # 1) Changed phi_t binning (2 degrees per bin)
    # # 2) Added 'Matched' filter condition (i.e., PID != 0) to purity calculation (redundancy)
    # # 3) Name is now up to "Purity_V11_"

# # On 4-25-2022:
    # # 1) Changed Q2 and xB binning
    # # 2) Added y to the histograms being produced (Also y vs xB as a 2D histogram)
    # # 3) Added mis-identified matchs to the histogram options
    # # 4) Not using the 2D binning options
    # # 5) Name is now up to "Purity_V10_"

# # On 4-19-2022:
    # # 1) Changed how smearing was applied so that it remains consistent for the entire time that the code is running
      # # (*) Old method would create a new smearing data set that may not always be consistent with prior uses of that code
      # # (*) The above issue meant that 'matched', 'unmatched', and 'pure' data sets may not be internally compariable in the desired way once the data has been smeared
      # # (*) Code now maintains one set group of smeared data for its entire runtime (this change may cause the code to take longer to run/require more memory - effect currently unknown)
    # # 2) Updated all binning schemes based on results from prior versions
    # # 3) Name is now up to "Purity_V9_"


# # On 4-18-2022:
    # # 1) Adjusted histogram binning (first major update since fixing the purity calculation)
    # # 2) Change file location (new matching criteria + secondary match)
      # #   (*) The feature of the new files which adds the second best match to the data frame was not used at the time of this update
      # #   (*) File locations for 'pdf' are now: /lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_3/MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_*
    # # 3) Reduced the number of histograms must be made before outputing the progress of the code while running (minor update to print progress - does not affect what is produced)
    # # 4) Name is now up to "Purity_V8_"

# # On 4-13-2022:
    # # 1) Added histograms for unmatched data
    # # 2) Name is now up to "Purity_V7_"

# # On 4-11-2022:
    # # 1) Fixed issue with bin purity calculation
    # # 2) Switched files for matched MC data (now using the updated matching criteria)
    # # 3) Name is now up to "Purity_V6_"


# # On 4-4-2022:
    # # 1) Rebinned the histograms again (V4)
    # #   (*) V2 worked in all cases except for the MM, Q2, and pT (Q2 worked before for V2)
    # # 2) Added count info on all (matched/unmatched) events that surived the cuts made (in addition to the existing count of MATCHED events that survived the cuts)
    # # 3) Added a 3rd type of histogram to be produced with 'pdf'
    # #   (*) datatype_2 = "gen" now creates histograms for the matched, generated events (from pdf)

# # On 3-28-2022: 
    # # Updated for use with the event matching/bin purity (too many changes to fully note)

# # On 3-11-2022: 
    # # 1) Fixed how smearing/cuts worked for more appropriate application to the datasets (i.e., smearing only for mdf and not cuts for gdf)
    # # 2) New function for looping through cuts
    # # 3) New cut on Q2 (Q2 < 2 can be cut now)
    # # 4) Cleaned up notes below
    

# # On 2-28-2022: Prepared for Collaboration presentation

# # On 2-7-2022: Removed temp definition of sectors -- Also not running sectors right now (too many histograms to be meaningful right now)

# # On 1-31-2022:
    # # 1) Did not run with pion sector info (did not have time to run before presentation)
    # # 2) Added 3D->2D histograms (in addition to the 1D histograms this code was already designed to create)

    
    
# # This Code has been coverted such that 3D histograms are made instead of filtering Q2-xB/z-pT bins






##=================================================================================================================================================================##
##=================================================================================================================================================================##
##=================================================================================================================================================================##




from sys import argv
# Let there be 4 arguements in argv when running this code
# arguement 1: Name of this code (makeROOT_epip_Matched_histos.py)
# arguement 2: data-type
    # Options: 
    # 1) rdf --> Real Data
    # 2) mdf --> MC REC Data
    # 3) gdf --> MC GEN Data
    # 4) pdf --> Bin Purity (Matched events between the MC Datasets)
# arguement 3: output type
    # Options: 
    # 1) histo --> root file contains the histograms made by this code
    # 2) data --> root file contains all information from the RDataFrame 
    # 3) tree --> root file contains all information from the RDataFrame (same as option 2)
    # 4) test --> sets arguement 4 to 'time' (does not save info - will test the DataFrame option instead of the histogram option)
    # 5) time --> sets arguement 4 to 'time' (does not save info - will test the histogram option - same as not giving a 4th arguement)
# arguement 4: file number (full file location)

# NOTE: The 3rd arguement is not necessary if the option for "histo" is desired (i.e., code is backwards compatible and works with only 3 arguements if desired)

# EXAMPLE: python makeROOT_epip_Matched_histos.py pdf All

# To see how many histograms will be made without processing any files, let the last arguement given be 'time'
# i.e., run the command:
# # python makeROOT_epip_Matched_histos.py df time
# # # df above can be any of the data-type options given above

try:
    code_name, datatype, output_type, file_location = argv
except:
    try:
        code_name, datatype, output_type = argv
    except:
        print("Error in arguments.")
        
    
datatype, output_type = str(datatype), str(output_type)

if(output_type == "test"):
    file_location = "time"
elif(output_type != "histo" and output_type != "data" and output_type != "tree"):
    file_location = output_type
    if(output_type != "test" and output_type != "time"):
        output_type = "histo"


print("".join(["Output type will be: ", output_type]))

import ROOT, numpy
import array
from datetime import datetime
import copy




if(str(file_location) == 'all'):
    print("\nRunning all files together...\n")
if(str(file_location) == 'time'):
    print("\nRunning Count. Not saving results...\n")
    

if(datatype == 'rdf' or datatype == 'mdf' or datatype == 'gdf' or datatype == 'pdf'):
    
    
    file_num = str(file_location)

    if(datatype == "rdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/No_Cut_Batch/Fixing_Sectors/Smearing/calc_sidis_epip_richcap_NC_smearing.inb.qa.skim4_00", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/No_Cut_Batch/Fixing_Sectors/calc_sidis_epip_richcap_NC.inb.qa.skim4_00", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/calc_sidis_epip_richcap.inb.qa.skim4_00", "")).replace(".hipo.root", "")
    if(datatype == "mdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Expanded_MC_REC/No_Cut_Batch/Fixing_Sectors/Smearing/calc_MC_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Expanded_MC_REC/No_Cut_Batch/Fixing_Sectors/calc_MC_sidis_epip_richcap_NC.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Expanded_MC_REC/calc_MC_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
    if(datatype == "gdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Generated_MC/Expanded_MC_GEN/No_Cut_Batch/Smearing/calc_MC_Gen_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Generated_MC/Expanded_MC_GEN/No_Cut_Batch/calc_MC_Gen_sidis_epip_richcap_no_cut.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Generated_MC/Expanded_MC_GEN/calc_MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
    
    if(datatype == "pdf"):
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/MC_Matched_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/MC_Matched_sidis_epip_richcap_New.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        # file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_3/MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
#         file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_4/MC_Matched_sidis_epip_richcap_Test_Rules_New_4.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_5/MC_Matched_sidis_epip_richcap_Test_Rules_New_5.inb.qa.45nA_job_", "")).replace(".hipo.root", "")

    
    
    ########################################################################################################################################################################
    ##==================================================================##============================##==================================================================##
    ##===============##===============##===============##===============##     Loading Data Files     ##===============##===============##===============##===============##
    ##==================================================================##============================##==================================================================##
    ########################################################################################################################################################################
    
    
    
    if(datatype == 'rdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/No_Cut_Batch/calc_sidis_epip_richcap_NC.inb.qa.skim4_00*")
            rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/No_Cut_Batch/Fixing_Sectors/Smearing/calc_sidis_epip_richcap_NC_smearing.inb.qa.skim4_00*")
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Expanded_REAL/calc_sidis_epip_richcap.inb.qa.skim4_00*")
            
            # files_used_for_data_frame = "calc_sidis_epip_richcap.inb.qa.skim4_00*"
            # files_used_for_data_frame = "calc_sidis_epip_richcap_NC.inb.qa.skim4_00*"
            files_used_for_data_frame = "calc_sidis_epip_richcap_NC_smearing.inb.qa.skim4_00*"
            
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            
            # files_used_for_data_frame = "".join(["calc_sidis_epip_richcap_NC.inb.qa.skim4_00", str(file_num), "*"])
            files_used_for_data_frame = "".join(["calc_sidis_epip_richcap_NC_smearing.inb.qa.skim4_00", str(file_num), "*"])
            
    if(datatype == 'mdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Expanded_MC_REC/calc_MC_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Expanded_MC_REC/No_Cut_Batch/Fixing_Sectors/Smearing/calc_MC_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_*")
            
            # files_used_for_data_frame = "calc_MC_sidis_epip_richcap.inb.qa.45nA_job_*"
            files_used_for_data_frame = "calc_MC_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_*"
            
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            
            # files_used_for_data_frame = "".join(["calc_MC_sidis_epip_richcap_no_cut.inb.qa.45nA_job_", str(file_num), "*"])
            files_used_for_data_frame = "".join(["calc_MC_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_", str(file_num), "*"])
            
    if(datatype == 'gdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Generated_MC/Expanded_MC_GEN/calc_MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Generated_MC/Expanded_MC_GEN/No_Cut_Batch/Smearing/calc_MC_Gen_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_*")
            
            files_used_for_data_frame = "calc_MC_Gen_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_*"
            # files_used_for_data_frame = "calc_MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*"
            
        else:
            
            rdf = ROOT.RDataFrame("h22", str(file_location))
            
            # files_used_for_data_frame = "".join(["calc_MC_Gen_sidis_epip_richcap_no_cut.inb.qa.45nA_job_", str(file_num), "*"])
            files_used_for_data_frame = "".join(["calc_MC_Gen_sidis_epip_richcap_NC_smearing.inb.qa.45nA_job_", str(file_num), "*"])
            
            
    if(datatype == 'pdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/MC_Matched_sidis_epip_richcap.inb.qa.45nA_job_*")
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/MC_Matched_sidis_epip_richcap_New.inb.qa.45nA_job_*")
            # rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_3/MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_*")
#             rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_4/MC_Matched_sidis_epip_richcap_Test_Rules_New_4.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22","/lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_5/MC_Matched_sidis_epip_richcap_Test_Rules_New_5.inb.qa.45nA_job_*")

            # files_used_for_data_frame = "MC_Matched_sidis_epip_richcap.inb.qa.45nA_job_*"
            # files_used_for_data_frame = "MC_Matched_sidis_epip_richcap_New.inb.qa.45nA_job_*"
            # files_used_for_data_frame = "MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_*"
#             files_used_for_data_frame = "MC_Matched_sidis_epip_richcap_Test_Rules_New_4.inb.qa.45nA_job_*"
            files_used_for_data_frame = "MC_Matched_sidis_epip_richcap_Test_Rules_New_5.inb.qa.45nA_job_*"

            
        else:
            
            rdf = ROOT.RDataFrame("h22", str(file_location))
            
            # files_used_for_data_frame = "".join(["MC_Matched_sidis_epip_richcap.inb.qa.45nA_job_", str(file_num), "*"])
            # files_used_for_data_frame = "".join(["MC_Matched_sidis_epip_richcap_New.inb.qa.45nA_job_", str(file_num), "*"])
            # files_used_for_data_frame = "".join(["MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_", str(file_num), "*"])
#             files_used_for_data_frame = "".join(["MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_", str(file_num), "*"])
            
            files_used_for_data_frame = "".join(["MC_Matched_sidis_epip_richcap_Test_Rules_New_5.inb.qa.45nA_job_", str(file_num), "*"])
            
            
            
    
    
    print("".join(["\nLoading File(s): ", str(files_used_for_data_frame)]))
    
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##
    
    # getting current date
    datetime_object_full = datetime.now()

    startMin_full, startHr_full, startDay_full = datetime_object_full.minute, datetime_object_full.hour, datetime_object_full.day

    if(datetime_object_full.minute < 10):
        timeMin_full = ''.join(['0', str(datetime_object_full.minute)])
    else:
        timeMin_full = str(datetime_object_full.minute)
    
    # printing current time
    if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
        print("".join(["The time that this code started is ", str((datetime_object_full.hour) - 12), ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour), ":", timeMin_full, " a.m."]))
    if(datetime_object_full.hour == 12):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour), ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour == 0 or datetime_object_full.hour == 24):
        print("".join(["The time that this code started is 12:", timeMin_full, " a.m."]))
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##
    
        
        
    ################################################################     Done Loading Data Files     ################################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ############################################################     Calculating Kinematic Variables     ############################################################

    
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

        rdf = rdf.Define("el_E","""
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto ele_E = ele.E();
        return ele_E;
        """)

        rdf = rdf.Define("pip_E","""
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pip0_E = pip0.E();
        return pip0_E;
        """)
        
        if(datatype == "pdf"):
            rdf = rdf.Define("el_E_gen","""
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto ele_E_gen = ele.E();
            return ele_E_gen;
            """)

            rdf = rdf.Define("pip_E_gen","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
            auto pip0_E_gen = pip0.E();
            return pip0_E_gen;
            """)
        
        
        
        #####################     Momentum     #####################

        rdf = rdf.Define("el","sqrt(ex*ex + ey*ey + ez*ez)")
        rdf = rdf.Define("pip","sqrt(pipx*pipx + pipy*pipy + pipz*pipz)")
        
        if(datatype == "pdf"):
            rdf = rdf.Define("el_gen","sqrt(ex_gen*ex_gen + ey_gen*ey_gen + ez_gen*ez_gen)")
            rdf = rdf.Define("pip_gen","sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen + pipz_gen*pipz_gen)")



        #####################     Theta Angle     #####################

        rdf = rdf.Define("elth","atan2(sqrt(ex*ex + ey*ey), ez)*TMath::RadToDeg()")
        rdf = rdf.Define("pipth","atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*TMath::RadToDeg()")
        
        if(datatype == "pdf"):
            rdf = rdf.Define("elth_gen","atan2(sqrt(ex_gen*ex_gen + ey_gen*ey_gen), ez_gen)*TMath::RadToDeg()")
            rdf = rdf.Define("pipth_gen","atan2(sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen), pipz_gen)*TMath::RadToDeg()")



        #####################     Phi Angle     #####################

        rdf = rdf.Define("elPhi","""
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto elPhi = ele.Phi()*TMath::RadToDeg();
        if(elPhi < 0){
            elPhi += 360;
        }
        return elPhi;
        """)

        rdf = rdf.Define("pipPhi","""
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pipPhi = pip0.Phi()*TMath::RadToDeg();
        if(pipPhi < 0){
            pipPhi += 360;
        }
        return pipPhi;
        """)
        
        
        if(datatype == "pdf"):
            rdf = rdf.Define("elPhi_gen","""
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto elPhi_gen = ele.Phi()*TMath::RadToDeg();
            if(elPhi_gen < 0){
                elPhi_gen += 360;
            }
            return elPhi_gen;
            """)

            rdf = rdf.Define("pipPhi_gen","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipy_gen, 0.13957);
            auto pipPhi_gen = pip0.Phi()*TMath::RadToDeg();
            if(pipPhi_gen < 0){
                pipPhi_gen += 360;
            }
            return pipPhi_gen;
            """)



        #####################     Sectors (angle definitions)     #####################

        rdf = rdf.Define("esec_a","""

        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto ele_phi = (180/3.1415926)*ele.Phi();

        int esec_a = 0;

        if(ele_phi >= -30 && ele_phi < 30){
            esec_a = 1;
        }
        if(ele_phi >= 30 && ele_phi < 90){
            esec_a = 2;
        }
        if(ele_phi >= 90 && ele_phi < 150){
            esec_a = 3;
        }
        if(ele_phi >= 150 || ele_phi < -150){
            esec_a = 4;
        }
        if(ele_phi >= -90 && ele_phi < -30){
            esec_a = 5;
        }
        if(ele_phi >= -150 && ele_phi < -90){
            esec_a = 6;
        }

        return esec_a;
        """)


        rdf = rdf.Define("pipsec_a","""

        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pip_phi = (180/3.1415926)*pip0.Phi();

        int pipsec_a = 0;

        if(pip_phi >= -45 && pip_phi < 15){
            pipsec_a = 1;
        }
        if(pip_phi >= 15 && pip_phi < 75){
            pipsec_a = 2;
        }
        if(pip_phi >= 75 && pip_phi < 135){
            pipsec_a = 3;
        }
        if(pip_phi >= 135 || pip_phi < -165){
            pipsec_a = 4;
        }
        if(pip_phi >= -105 && pip_phi < -45){
            pipsec_a = 5;
        }
        if(pip_phi >= -165 && pip_phi < -105){
            pipsec_a = 6;
        }

        return pipsec_a;
        """)
        
        
        
        if(datatype == "pdf"):
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

            return esec_gen;
            """)


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

            return pipsec_gen;
            """)


        #####################     Other Values     #####################

        rdf = rdf.Define("vals","""
        auto beam = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targ = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

        auto epipX = beam + targ - ele - pip0;

        auto q = beam - ele;

        auto Q2 = - q.M2();

        auto v = beam.E() - ele.E();

        auto xB = Q2/(2*targ.M()*v);

        auto W2 = targ.M2() + 2*targ.M()*v - Q2;

        auto W = sqrt(W2);

        auto y = (targ.Dot(q))/(targ.Dot(beam));

        auto z = ((pip0.E())/(q.E()));

        auto gamma = 2*targ.M()*(xB/sqrt(Q2));

        auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));

        std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};

        return vals;
        """)



        rdf = rdf.Define('MM', 'vals[0]') # Missing Mass

        rdf = rdf.Define('MM2', 'vals[1]') # Missing Mass Squared 

        rdf = rdf.Define('Q2', 'vals[2]') # lepton momentum transfer squared

        rdf = rdf.Define('xB', 'vals[3]') # fraction of the proton momentum that is carried by the struck quark

        rdf = rdf.Define('v', 'vals[4]') # energy of the virtual photon

        rdf = rdf.Define('s', 'vals[5]') # center-of-mass energy squared

        rdf = rdf.Define('W', 'vals[6]') # center-of-mass energy

        rdf = rdf.Define('y', 'vals[7]') # energy fraction of the incoming lepton carried by the virtual photon

        rdf = rdf.Define('z', 'vals[8]') # energy fraction of the virtual photon carried by the outgoing hadron

        rdf = rdf.Define('epsilon', 'vals[9]') # ratio of the longitudinal and transverse photon flux
        
        
        
        if(datatype == "pdf"):
            rdf = rdf.Define("vals_gen","""
            auto beam_gen = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
            auto targ_gen = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
            auto ele_gen = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto pip0_gen = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);

            auto epipX_gen = beam_gen + targ_gen - ele_gen - pip0_gen;

            auto q_gen = beam_gen - ele_gen;

            auto Q2_gen = - q_gen.M2();

            auto v_gen = beam_gen.E() - ele_gen.E();

            auto xB_gen = Q2_gen/(2*targ_gen.M()*v_gen);

            auto W2_gen = targ_gen.M2() + 2*targ_gen.M()*v_gen - Q2_gen;

            auto W_gen = sqrt(W2_gen);

            auto y_gen = (targ_gen.Dot(q_gen))/(targ_gen.Dot(beam_gen));

            auto z_gen = ((pip0_gen.E())/(q_gen.E()));

            auto gamma_gen = 2*targ_gen.M()*(xB_gen/sqrt(Q2_gen));

            auto epsilon_gen = (1 - y_gen - 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen))/(1 - y_gen + 0.5*(y_gen*y_gen) + 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen));

            std::vector<double> vals_gen = {epipX_gen.M(), epipX_gen.M2(), Q2_gen, xB_gen, v_gen, W2_gen, W_gen, y_gen, z_gen, epsilon_gen};

            return vals_gen;
            """)

            rdf = rdf.Define('MM_gen', 'vals_gen[0]')
            rdf = rdf.Define('MM2_gen', 'vals_gen[1]')
            rdf = rdf.Define('Q2_gen', 'vals_gen[2]')
            rdf = rdf.Define('xB_gen', 'vals_gen[3]')
            rdf = rdf.Define('v_gen', 'vals_gen[4]')
            rdf = rdf.Define('s_gen', 'vals_gen[5]')
            rdf = rdf.Define('W_gen', 'vals_gen[6]')
            rdf = rdf.Define('y_gen', 'vals_gen[7]')
            rdf = rdf.Define('z_gen', 'vals_gen[8]')
            rdf = rdf.Define('epsilon_gen', 'vals_gen[9]')
        
    
    #######################################################################
    ##=====##  The above calculations are ran in the groovy code  ##=====##
    #######################################################################
    
    
    
    
    
    ##################################################     Done with Calculating (Initial) Kinematic Variables     ##################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ################################################################     Using CM/boosted frames     ################################################################
    
    
   

    rdf = rdf.Define("vals2","""
    auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
    auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
    auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
    auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
    auto lv_qMM = beamM - eleM;

    TLorentzVector beam(0, 0, 10.6041, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());
    TLorentzVector ele(ex, ey, ez, eleM.E());
    TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());
    TLorentzVector lv_q = beam - ele;


    ///////////////     Angles for Rotation     ///////////////
    double Theta_q = lv_q.Theta();
    double Phi_el = ele.Phi();


    /////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////


    auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot)
    {

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



    /////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////



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

    // Not using these values (see above for these variables)
    // auto epipXboost = beamBoost + targBoost - ele_Boost - pip_Boost;
    // auto Q2boost = - qlv_Boost.M2();
    // auto vboost = beamBoost.E() - ele_Boost.E();
    // auto xBboost = Q2boost/(2*targBoost.M()*vboost);
    // auto W2boost = targBoost.M2() + 2*targBoost.M()*vboost - Q2boost;
    // auto Wboost = sqrt(W2boost);
    // auto yboost = (targBoost.Dot(qlv_Boost))/(targBoost.Dot(beamBoost));
    // auto zboost = ((pip_Boost.E())/(qlv_Boost.E()));
    // auto gammaboost = 2*targBoost.M()*(xBboost/sqrt(Q2boost));
    // auto epsilonboost = (1 - yboost - 0.25*(gammaboost*gammaboost)*(yboost*yboost))/(1 - yboost + 0.5*(yboost*yboost) + 0.25*(gammaboost*gammaboost)*(yboost*yboost));


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


    return vals2;

    """)



    rdf = rdf.Define('pT','vals2[0]')    # transverse momentum of the final state hadron
    rdf = rdf.Define('phi_t','vals2[1]') # Most important angle (between lepton and hadron planes)
    rdf = rdf.Define('xF','vals2[2]')    # x Feynmann

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
    
    
    
    if(datatype == "pdf"):
        rdf = rdf.Define("vals2_gen","""
        auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto eleM = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
        auto lv_qMM = beamM - eleM;

        TLorentzVector beam(0, 0, 10.6041, beamM.E());
        TLorentzVector targ(0, 0, 0, targM.E());
        TLorentzVector ele(ex_gen, ey_gen, ez_gen, eleM.E());
        TLorentzVector pip0(pipx_gen, pipy_gen, pipz_gen, pip0M.E());
        TLorentzVector lv_q = beam - ele;


        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el = ele.Phi();


        /////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////


        auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot)
        {

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



        /////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////



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

        // Not using these values (see above for these variables)
        // auto epipXboost = beamBoost + targBoost - ele_Boost - pip_Boost;
        // auto Q2boost = - qlv_Boost.M2();
        // auto vboost = beamBoost.E() - ele_Boost.E();
        // auto xBboost = Q2boost/(2*targBoost.M()*vboost);
        // auto W2boost = targBoost.M2() + 2*targBoost.M()*vboost - Q2boost;
        // auto Wboost = sqrt(W2boost);
        // auto yboost = (targBoost.Dot(qlv_Boost))/(targBoost.Dot(beamBoost));
        // auto zboost = ((pip_Boost.E())/(qlv_Boost.E()));
        // auto gammaboost = 2*targBoost.M()*(xBboost/sqrt(Q2boost));
        // auto epsilonboost = (1 - yboost - 0.25*(gammaboost*gammaboost)*(yboost*yboost))/(1 - yboost + 0.5*(yboost*yboost) + 0.25*(gammaboost*gammaboost)*(yboost*yboost));


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

        double pipTx_gen = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTy_gen = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTz_gen = pip0.P()*TMath::Cos(theta_t);

        TVector3 pipT(pipTx_gen, pipTy_gen, pipTz_gen);


        double phi_t_cross_product_gen = phi_t_cross_product_gen*TMath::RadToDeg();


        ///////////////   x Feynmann   ///////////////
        double xF_gen = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W_gen);


        // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
        double pT_gen = sqrt(pipx_1_gen*pipx_1_gen + pipy_1_gen*pipy_1_gen);
        double phi_t_gen = pip0_Clone.Phi()*TMath::RadToDeg();


        if(phi_t_gen < 0){
            phi_t_gen += 360;
        }



        // std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen, pipx_1_gen, pipy_1_gen, pipz_1_gen, qx_gen, qy_gen, qz_gen, beamx_gen, beamy_gen, beamz_gen, elex_gen, eley_gen, elez_gen};
        std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen};


        return vals2_gen;

        """)

        rdf = rdf.Define('pT_gen','vals2_gen[0]')
        rdf = rdf.Define('phi_t_gen','vals2_gen[1]')
        rdf = rdf.Define('xF_gen','vals2_gen[2]')
    


    
    ###########################################################     Done with Using CM/boosted frames     ###########################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    #######################################################     Smearing Calculations (Defining Function)     #######################################################
    

    
    
    ##==================================================================================================##
    ##---------------------------------##============================##---------------------------------##
    ##=================================##     Smearing Functions     ##=================================##
    ##---------------------------------##============================##---------------------------------##
    ##==================================================================================================##
    
    
    # def Smear_DF(Data_Frame):
    
        # Data_Frame_Clone = Data_Frame.Define("smeared_vals","""
    rdf = rdf.Define("smeared_vals","""

    //===========================================================================//
    //=================//     Smearing Function (From FX)     //=================//
    //===========================================================================//


    auto smear_func = [&](TLorentzVector V4)
    {

        // true generated values (i.e., values of the unsmeared TLorentzVector)
        double inM = V4.M();
        double smeared_P  = V4.P();
        double smeared_Th = V4.Theta();
        double smeared_Phi = V4.Phi();

        TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());

        //calculate resolutions

        double smeared_ThD = TMath::RadToDeg()*smeared_Th;
        double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
        double momS2 = 0.02*smeared_ThD;
        double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
        momR *= 2.0;

        double theS1 = 0.004*smeared_ThD + 0.1;
        double theS2 = 0;
        double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
        theR *= 2.5;

        double phiS1 = 0.85 - 0.015*smeared_ThD;
        double phiS2 = 0.17 - 0.003*smeared_ThD;
        double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
        phiR *= 3.5;


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

    };

    auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
    auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
    auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
    auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

    TLorentzVector beam(0, 0, 10.6041, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());
    TLorentzVector ele(ex, ey, ez, eleM.E());
    TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

    TLorentzVector ele_NO_SMEAR(ex, ey, ez, eleM.E());
    TLorentzVector pip0_NO_SMEAR(pipx, pipy, pipz, pip0M.E());


    //========================================================================//
    //=================//     Smearing PxPyPzMVector's     //=================//
    //========================================================================//

    // smear_func(beam) //===// DO NOT SMEAR BEAM/TARGET -- ONLY SMEAR OUTGOING PARTICLES //===//
    // smear_func(targ) //===// DO NOT SMEAR BEAM/TARGET -- ONLY SMEAR OUTGOING PARTICLES //===//

    // cout<<endl<<"Electron Smearing: "<<endl;
    // cout<<"Pre-Smear El Phi (degrees): "<<TMath::RadToDeg()*(ele.Phi())<<endl;
    // cout<<"Pre-Smear El Th (degrees): "<<TMath::RadToDeg()*(ele.Theta())<<endl;
    // cout<<"Pre-Smear El P : "<<ele.P()<<endl<<endl;

    TLorentzVector ele_smeared = smear_func(ele);

    // cout<<endl<<"Post-Smear El Phi (degrees): "<<TMath::RadToDeg()*(ele_smeared.Phi())<<endl;
    // cout<<"Post-Smear El Th (degrees): "<<TMath::RadToDeg()*(ele_smeared.Theta())<<endl;
    // cout<<"Post-Smear El P : "<<ele_smeared.P()<<endl;



    // cout<<endl<<"Pi+ Smearing: "<<endl;
    // cout<<"Pre-Smear Pi+ Phi (degrees): "<<TMath::RadToDeg()*(pip0.Phi())<<endl;
    // cout<<"Pre-Smear Pi+ Th (degrees): "<<TMath::RadToDeg()*(pip0.Theta())<<endl;
    // cout<<"Pre-Smear Pi+ P : "<<pip0.P()<<endl<<endl;

    TLorentzVector pip0_smeared = smear_func(pip0);

    // cout<<endl<<"Post-Smear Pi+ Phi (degrees): "<<TMath::RadToDeg()*(pip0_smeared.Phi())<<endl;
    // cout<<"Post-Smear Pi+ Th (degrees): "<<TMath::RadToDeg()*(pip0_smeared.Theta())<<endl;
    // cout<<"Post-Smear Pi+ P : "<<pip0_smeared.P()<<endl;

    //=========================================================================//
    //=================//     Vectors have been Smeared     //=================//
    //=========================================================================//

    TLorentzVector lv_q = beam - ele_smeared;

    // auto Delta_Smear_El = (ele_smeared - ele_NO_SMEAR);
    // auto Delta_Smear_Pip = (pip0_smeared - pip0_NO_SMEAR);


    auto Delta_Smear_El_P = abs(ele_smeared.P()) - abs(ele_NO_SMEAR.P()); // Delta_Smear_El.P();
    auto Delta_Smear_El_Th = (abs(ele_smeared.Theta()) - abs(ele_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_El.Theta()*TMath::RadToDeg();
    auto Delta_Smear_El_Phi = (abs(ele_smeared.Phi()) - abs(ele_NO_SMEAR.Phi()))*TMath::RadToDeg(); // Delta_Smear_El.Phi()*TMath::RadToDeg();

    auto Delta_Smear_Pip_P = abs(pip0_smeared.P()) - abs(pip0_NO_SMEAR.P()); // Delta_Smear_Pip.P();
    auto Delta_Smear_Pip_Th = (abs(pip0_smeared.Theta()) - abs(pip0_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_Pip.Theta()*TMath::RadToDeg();
    auto Delta_Smear_Pip_Phi = (abs(pip0_smeared.Phi()) - abs(pip0_NO_SMEAR.Phi()))*TMath::RadToDeg(); // Delta_Smear_Pip.Phi()*TMath::RadToDeg();


    // cout<<endl<<"Delta Smear El Th = "<<Delta_Smear_El_Th<<endl;
    // cout<<"Delta Smear Pi+ Th = "<<Delta_Smear_Pip_Th<<endl;



    // Rest of calculations are performed as normal from here


    auto epipX = beam + targ - ele_smeared - pip0_smeared;

    auto q_smeared = beam - ele_smeared;

    auto Q2_smeared = -q_smeared.M2();

    auto v_smeared = beam.E() - ele_smeared.E();

    auto xB_smeared = Q2_smeared/(2*targ.M()*v_smeared);

    auto W2_smeared = targ.M2() + 2*targ.M()*v_smeared - Q2_smeared;

    auto W_smeared = sqrt(W2_smeared);

    auto y_smeared = (targ.Dot(q_smeared))/(targ.Dot(beam));

    auto z_smeared = ((pip0_smeared.E())/(q_smeared.E()));

    auto gamma_smeared = 2*targ.M()*(xB_smeared/sqrt(Q2_smeared));

    auto epsilon_smeared = (1 - y_smeared - 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared))/(1 - y + 0.5*(y_smeared*y_smeared) + 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared));




    // Particles' (Smeared) Energies/Momentums/Angles
    auto ele_E_smeared = ele_smeared.E();
    auto pip0_E_smeared = pip0_smeared.E();

    auto el_smeared = ele_smeared.P();
    auto pip_smeared = pip0_smeared.P();

    auto elth_smeared = ele_smeared.Theta()*TMath::RadToDeg();
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
    double Phi_el = ele_smeared.Phi();


    /////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////


    auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot)
    {

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


    /////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////



    ///////////////     Rotating to CM Frame     ///////////////

    auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
    auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
    auto ele_Clone  = Rot_Matrix(ele_smeared,  -1, Theta_q, Phi_el);
    auto pip0_Clone = Rot_Matrix(pip0_smeared, -1, Theta_q, Phi_el);
    auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);


    ///////////////     Saving CM components     ///////////////

    double pipx_smeared = pip0_Clone.X();
    double pipy_smeared = pip0_Clone.Y();
    double pipz_smeared = pip0_Clone.Z();

    double qx_smeared = lv_q_Clone.X();
    double qy_smeared = lv_q_Clone.Y();
    double qz_smeared = lv_q_Clone.Z();

    double beamx_smeared = beam_Clone.X();
    double beamy_smeared = beam_Clone.Y();
    double beamz_smeared = beam_Clone.Z();

    double elex_smeared = ele_Clone.X();
    double eley_smeared = ele_Clone.Y();
    double elez_smeared = ele_Clone.Z();


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

    // Not using these values (see above for these variables)
    // auto epipXboost = beamBoost + targBoost - ele_Boost - pip_Boost;
    // auto Q2boost = - qlv_Boost.M2();
    // auto vboost = beamBoost.E() - ele_Boost.E();
    // auto xBboost = Q2boost/(2*targBoost.M()*vboost);
    // auto W2boost = targBoost.M2() + 2*targBoost.M()*vboost - Q2boost;
    // auto Wboost = sqrt(W2boost);
    // auto yboost = (targBoost.Dot(qlv_Boost))/(targBoost.Dot(beamBoost));
    // auto zboost = ((pip_Boost.E())/(qlv_Boost.E()));
    // auto gammaboost = 2*targBoost.M()*(xBboost/sqrt(Q2boost));
    // auto epsilonboost = (1 - yboost - 0.25*(gammaboost*gammaboost)*(yboost*yboost))/(1 - yboost + 0.5*(yboost*yboost) + 0.25*(gammaboost*gammaboost)*(yboost*yboost));


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
    double theta_t = TMath::ACos(Cos_theta_t);

    double pipTx = pip0_smeared.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTy = pip0_smeared.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTz = pip0_smeared.P()*TMath::Cos(theta_t);

    TVector3 pipT(pipTx, pipTy, pipTz);


    phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();


    ///////////////   x Feynmann   ///////////////
    double xF_smeared = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);


    // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
    double pT_smeared = sqrt(pipx_smeared*pipx_smeared + pipy_smeared*pipy_smeared);
    double phi_t_smeared = pip0_Clone.Phi()*TMath::RadToDeg();


    if(phi_t_smeared < 0){
        phi_t_smeared = phi_t_smeared + 360;
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

    auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
    {

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

    return smeared_vals;

    """)

    # Data_Frame_Clone = Data_Frame_Clone.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
    # Data_Frame_Clone = Data_Frame_Clone.Define('z_pT_Bin_smeared', 'smeared_vals[14]')
    rdf = rdf.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
    rdf = rdf.Define('z_pT_Bin_smeared', 'smeared_vals[14]')
    
    rdf = rdf.Define('Q2_xB_Bin_2_smeared', '''
        int Q2_xB_Bin_2_smeared = Q2_xB_Bin_smeared;

        if(Q2_xB_Bin_smeared > 1 && Q2_xB_Bin_2_smeared%2 != 0){
            Q2_xB_Bin_2_smeared += -2;
        }

        if(smeared_vals[2] < 2){
        // if(Q2_smeared < 2){
            Q2_xB_Bin_2_smeared = 0; 
        }

        return Q2_xB_Bin_2_smeared;
    ''')
        
        
    rdf = rdf.Define('z_pT_Bin_2_smeared', '''
    
        double z_smeared = smeared_vals[8];
        double pT_smeared = smeared_vals[10];
    
        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {
            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1 (was 3 in old scheme)
            if(Q2_xB_Bin_Num == 1){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

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
            // For Q2_xB Bin 3 (was 5 in old scheme)
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
            // For Q2_xB Bin 5 (was 7 in old scheme)
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
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
            // For Q2_xB Bin 7 (was 9 in old scheme)
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
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



            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };


        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // Default:
        int Num_z_Borders = 8;
        int Num_pT_Borders = 8;
        int z_pT_Bin_2_smeared = 0;

        // For Q2_xB Bin 0
        if(Q2_xB_Bin_2_smeared == 0){
            z_pT_Bin_2_smeared = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
            Num_z_Borders = 0; Num_pT_Borders = 0;
        }
        // For Q2_xB Bin 1 (Uses Default for both borders)

        // For Q2_xB Bin 2 (Uses Default for both borders)

        // For Q2_xB Bin 3 (Uses Default for both borders)

        // For Q2_xB Bin 4 (Uses Default for pT borders)
        if(Q2_xB_Bin_2_smeared == 4){
            Num_z_Borders = 7;
        }

        // For Q2_xB Bin 5 (New scheme)
        if(Q2_xB_Bin_2_smeared == 5){
            Num_z_Borders = 7; Num_pT_Borders = 7;
        }

        // For Q2_xB Bin 6
        if(Q2_xB_Bin_2_smeared == 6){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 7 (New scheme)
        if(Q2_xB_Bin_2_smeared == 7){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 8
        if(Q2_xB_Bin_2_smeared == 8){
            Num_z_Borders = 6; Num_pT_Borders = 5;
        }

        if(Num_z_Borders == 0){
            Num_z_Borders = 1; Num_pT_Borders = 1;
        }


        int z_pT_Bin_2_smeared_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin_2_smeared != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z_smeared > Borders_function(Q2_xB_Bin_2_smeared, 0, zbin) && z_smeared < Borders_function(Q2_xB_Bin_2_smeared, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin_2_smeared != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT_smeared > Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin) && pT_smeared < Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin_2_smeared = z_pT_Bin_2_smeared_count; // The value of the z_pT_Bin_2_smeared has been set
                        // cout<<"The value of the z_pT_Bin_2_smeared has been set as: "<<z_pT_Bin_2_smeared<<endl;
                        break;
                    }
                    else{
                        z_pT_Bin_2_smeared_count += 1; // Checking the next bin
                        // cout<<"Checking the next bin"<<endl;
                    }
                }

            }
            else{
                z_pT_Bin_2_smeared_count += (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }

        return z_pT_Bin_2_smeared;
    
    ''')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_El_P', 'smeared_vals[24]')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_El_Th', 'smeared_vals[25]')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_El_Phi', 'smeared_vals[26]')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_Pip_P', 'smeared_vals[27]')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_Pip_Th', 'smeared_vals[28]')
# #         Data_Frame_Clone = Data_Frame_Clone.Define('Delta_Smear_Pip_Phi', 'smeared_vals[29]')
        
#         import ROOT, numpy
# #         display = Data_Frame_Clone.Display({"Delta_Smear_El_P", "Delta_Smear_El_Th", "Delta_Smear_El_Phi", "Delta_Smear_Pip_P", "Delta_Smear_Pip_Th", "Delta_Smear_Pip_Phi"}, 10)
#         display = rdf.Display({"elec_events_found", "ex"}, 10)
#         display.Print()
        
#         return Data_Frame_Clone

        
        
        ##==================================================##
        ##==========## End of Smeared DataFrame ##==========##
        ##==================================================##
        
        
        

    def smear_frame_compatible(Data_Frame, Variable, Smearing_Q):
        
        if("smear" not in Smearing_Q):
            # Variable should already be defined
            return Data_Frame
        
        else:

            done_Q = 'no'
            
            if('MM' == Variable or 'MM_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('MM_smeared', 'smeared_vals[0]')

            if('MM2' == Variable or 'MM2_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('MM2_smeared', 'smeared_vals[1]')

            if('Q2' == Variable or 'Q2_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('Q2_smeared', 'smeared_vals[2]')

            if('xB' == Variable or 'xB_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('xB_smeared', 'smeared_vals[3]')

            if('v' == Variable or 'v_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('v_smeared', 'smeared_vals[4]')

            if('s' == Variable or 's_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('s_smeared', 'smeared_vals[5]')

            if('W' == Variable or 'W_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('W_smeared', 'smeared_vals[6]')

            if('y' == Variable or 'y_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('y_smeared', 'smeared_vals[7]')

            if('z' == Variable or 'z_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('z_smeared', 'smeared_vals[8]')

            if('epsilon' == Variable or 'epsilon_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('epsilon_smeared', 'smeared_vals[9]')

            if('pT' == Variable or 'pT_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pT_smeared', 'smeared_vals[10]')

            if('phi_t' == Variable or 'phi_t_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('phi_t_smeared', 'smeared_vals[11]')

            if('xF' == Variable or 'xF_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('xF_smeared', 'smeared_vals[12]')

            if('el' == Variable or 'el_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('el_smeared', 'smeared_vals[15]')

            if('el_E' == Variable or 'el_E_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('el_E_smeared', 'smeared_vals[16]')

            if('elth' == Variable or 'elth_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('elth_smeared', 'smeared_vals[17]')

            if('elPhi' == Variable or 'elPhi_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('elPhi_smeared', 'smeared_vals[18]')

            if('pip' == Variable or 'pip_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pip_smeared', 'smeared_vals[19]')

            if('pip_E' == Variable or 'pip_E_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pip_E_smeared', 'smeared_vals[20]')

            if('pipth' == Variable or 'pipth_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pipth_smeared', 'smeared_vals[21]')

            if('pipPhi' == Variable or 'pipPhi_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pipPhi_smeared', 'smeared_vals[22]')

            if('Delta_Smear_El_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[23]')
            
            if('Delta_Smear_El_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[24]')
            
            if('Delta_Smear_El_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[25]')
            
            if('Delta_Smear_Pip_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[26]')
            
            if('Delta_Smear_Pip_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[27]')
            
            if('Delta_Smear_Pip_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[28]')


            if(done_Q != 'yes'):
                # Failed to get a new definition
                return Data_Frame
            
        
    
    
    ##=========================================================================================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=================================##     End of Smearing Functions     ##=================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=========================================================================================================##
    
   

    
    
    
    
    
    print("Kinematic Variables have been calculated.")
    ####################################################     Done with Calculating (All) Kinematic Variables     ####################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ###############################################################     Making Cuts to DataFrames     ###############################################################


    
    def filter_Valerii(Data_Frame, Valerii_Cut):
        
        if("Valerii_Cut" in Valerii_Cut):

            Data_Frame_Clone = Data_Frame.Filter("""

                auto func = [&](double x, double k, double b)
                {
                    return k * x + b;
                };

                struct line{
                    double k;
                    double b;
                };

                auto isOutOfLines = [&](double x, double y, line topLine, line botLine)
                {
                    return y > func(x, topLine.k, topLine.b) || y < func(x, botLine.k, botLine.b);
                };

                // bool BadElementKnockOut(double hx, double hy, int sector, int cutLevel);     

                auto BadElementKnockOut = [&](double hx, double hy, int sector, int cutLevel)
                {

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


                return BadElementKnockOut(Hx, Hy, esec, 1);

                """)

            return Data_Frame_Clone
        
        else:
            return Data_Frame
    
    
    
    
    
    #############################################################     Done Making Cuts to DataFrames     #############################################################
    ##                                                                                                                                                              ##
    ##--------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                              ##
    ####################################################################     Kinematic Binning     ###################################################################
    

    
    
    ###################################################################
    #####################     Bin Definitions     #####################
    #-----------------------------------------------------------------#
    ##############     Definitions for Q2 and xB Bins     #############
    
    
    # Q2 and xB Binning (See Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
    rdf = rdf.Define("Q2_xB_Bin","""

        int Q2_xB_Bin = 0;

        /////////////////////////       Bin 1       /////////////////////////
        if(xB > 0.0835 && xB < 0.15){
            // Border lines of Bin 1:
            //                 Upper Border:
            //                          Q2 = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB - 0.0835) + 1.3
            //                 Q2 must be less than the equation above for Bin 1
            //
            //                 Lower Border:
            //                          Q2 = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB - 0.0835) + 1.30   (if xB < 0.12)
            //                          Q2 = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB - 0.1200) + 1.30   (if xB > 0.12)
            //                 Q2 must be greater than the equations above for Bin 1

            int Condition_Up = 0;
            int Condition_Down = 0;
            // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
            // Code will verify both conditions seperately before checking that they have been met.
            // If the condition has been met, its value will be set to 1.
            // If either is still 0 when checked, the event will be consided as being outside of Bin 1


            // Testing Upper Border of Bin 1
            if(Q2 <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB - 0.0835) + 1.3){
                Condition_Up = 1; // Condition for upper border of Bin 1 has been met
            }

            // Testing Lower Border of Bin 1
            if(xB < 0.12){
                if(Q2 >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB - 0.0835) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }
            if(xB > 0.12){
                if(Q2 >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB - 0.1200) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }


            if(Condition_Up == 1 && Condition_Down == 1){
                Q2_xB_Bin = 1;
                return Q2_xB_Bin; // Bin 1 Confirmed
            }

        }
        /////////////////////////     End of Bin 1     /////////////////////////




        /////////////////////////       Bin 2 or 3       /////////////////////////
        if(xB > 0.15 && xB < 0.24){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98

            // Deciding between Bins
            if(Q2 < ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98){
                BinTest = 2; // Event will NOT go to bin 3
            }

            if(Q2 > ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98){
                BinTest = 3; // Event will NOT go to bin 2
            }



            // Final Border Test

            // Bin 2
            if(BinTest == 2){
                // Border lines of Bin 2:   Q2 = ((1.45 - 1.38)/(0.20 - 0.15))*(xB - 0.15) + 1.38   (if xB < 0.2)
                //                          Q2 = ((1.50 - 1.45)/(0.24 - 0.20))*(xB - 0.24) + 1.50   (if xB > 0.2)

                if(xB < 0.2){
                    if(Q2 >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB - 0.15) + 1.38){
                        Q2_xB_Bin = 2;
                        return Q2_xB_Bin; // Bin 2 Confirmed
                    }
                }

                if(xB > 0.2){
                    if(Q2 >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB - 0.24) + 1.50){
                        Q2_xB_Bin = 2;
                        return Q2_xB_Bin; // Bin 2 Confirmed
                    }
                }

            }
            // End of Bin 2


            // Bin 3
            if(BinTest == 3){
                // Border line of Bin 3:   Q2 = ((3.625 - 2.28)/(0.24 - 0.15))*(xB - 0.15) + 2.28

                if(Q2 <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB - 0.15) + 2.28){
                    Q2_xB_Bin = 3;
                    return Q2_xB_Bin; // Bin 3 Confirmed
                }

            }
            // End of Bin 3


        }
        /////////////////////////     End of Bin 2 and 3     /////////////////////////




        /////////////////////////       Bin 4 or 5       /////////////////////////
        if(xB > 0.24 && xB < 0.34){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75

            // Deciding between Bins
            if(Q2 < ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75){
                BinTest = 4; // Event will NOT go to bin 5
            }

            if(Q2 > ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75){
                BinTest = 5; // Event will NOT go to bin 4
            }



            // Final Border Test

            // Bin 4
            if(BinTest == 4){
                // Border lines of Bin 4:   Q2 = ((1.53 - 1.50)/(0.27 - 0.24))*(xB - 0.24) + 1.50   (if xB < 0.27)
                //                          Q2 = ((1.56 - 1.53)/(0.30 - 0.27))*(xB - 0.27) + 1.53   (if 0.27 < xB < 0.30)
                //                          Q2 = ((1.60 - 1.56)/(0.34 - 0.30))*(xB - 0.30) + 1.56   (if xB > 0.3)

                if(xB < 0.27){
                    if(Q2 >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB - 0.24) + 1.50){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

                if(xB > 0.27 && xB < 0.30){
                    if(Q2 >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB - 0.27) + 1.53){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

                if(xB > 0.30){
                    if(Q2 >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB - 0.30) + 1.56){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

            }
            // End of Bin 4


            // Bin 5
            if(BinTest == 5){
                // Border line of Bin 5:   Q2 = ((5.12 - 3.625)/(0.34 - 0.24))*(xB - 0.24) + 3.625

                if(Q2 <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB - 0.24) + 3.625){
                    Q2_xB_Bin = 5;
                    return Q2_xB_Bin; // Bin 5 Confirmed
                }

            }
            // End of Bin 5


        }
        /////////////////////////     End of Bin 4 and 5     /////////////////////////




        /////////////////////////       Bin 6 or 7       /////////////////////////
        if(xB > 0.34 && xB < 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63

            // Deciding between Bins
            if(Q2 < ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63){
                BinTest = 6; // Event will NOT go to bin 7
            }

            if(Q2 > ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63){
                BinTest = 7; // Event will NOT go to bin 6
            }



            // Final Border Test

            // Bin 6
            if(BinTest == 6){
                // Border line of Bin 6:   Q2 = ((2.52 - 1.60)/(0.45 - 0.34))*(xB - 0.34) + 1.60

                if(Q2 >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB - 0.34) + 1.60){
                    Q2_xB_Bin = 6;
                    return Q2_xB_Bin; // Bin 6 Confirmed
                }

            }
            // End of Bin 6


            // Bin 7
            if(BinTest == 7){
                // Border line of Bin 7:   Q2 = ((6.76 - 5.12)/(0.45 - 0.34))*(xB - 0.34) + 5.12

                if(Q2 <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB - 0.34) + 5.12){
                    Q2_xB_Bin = 7;
                    return Q2_xB_Bin; // Bin 7 Confirmed
                }

            }
            // End of Bin 7


        }
        /////////////////////////     End of Bin 6 and 7     /////////////////////////




        /////////////////////////       Bin 8 or 9       /////////////////////////
        if(xB > 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70    

            // Deciding between Bins
            if(Q2 < ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70){
                BinTest = 8; // Event will NOT go to bin 9
            }
            if(Q2 > ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70){
                BinTest = 9; // Event will NOT go to bin 8
            }



            // Final Border Test

            // Bin 8
            if(BinTest == 8){
                // Border lines of Bin 8:   Q2 = ((3.05 - 2.52)/(0.500 - 0.45))*(xB - 0.45) + 2.52   (if xB < 0.50)
                //                          Q2 = ((4.05 - 3.05)/(0.570 - 0.50))*(xB - 0.50) + 3.05   (if 0.50 < xB < 0.57)
                //                          Q2 = ((5.40 - 4.05)/(0.640 - 0.57))*(xB - 0.57) + 4.05   (if 0.57 < xB < 0.64)
                //                          Q2 = ((7.42 - 5.40)/(0.708 - 0.64))*(xB - 0.64) + 5.40   (if xB > 0.64)

                if(xB < 0.50){
                    if(Q2 >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB - 0.45) + 2.52){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.50 && xB < 0.57){
                    if(Q2 >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB - 0.50) + 3.05){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.57 && xB < 0.64){
                    if(Q2 >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB - 0.57) + 4.05){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.64){
                    if(Q2 >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB - 0.64) + 5.40){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

            }
            // End of Bin 8


            // Bin 9
            if(BinTest == 9){
                // Border lines of Bin 9:
                //                 Uppermost Border:
                //                          Q2 = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB - 0.450) +  6.760   (if xB < 0.677)
                //                          Q2 = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB - 0.677) + 10.185   (if xB > 0.677)
                //                 Q2 must be less than the equations above for Bin 9
                //
                //                 Rightmost Border:
                //                          Q2 =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB - 0.708) + 7.42   (if xB < 0.75)
                //                          Q2 = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB - 0.750) + 9.52   (if xB > 0.75)
                //                 Q2 must be greater than the equations above for Bin 9

                int Condition_Up = 0;
                int Condition_Right = 0;
                // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 9


                // Testing Uppermost Border of Bin 9
                if(xB < 0.677){
                    if(Q2 <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB - 0.450) +  6.760){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }
                if(xB > 0.677){
                    if(Q2 <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB - 0.677) + 10.185){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }

                // Testing Rightmost Border of Bin 9
                if(xB < 0.75){
                    if(Q2 >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB - 0.708) + 7.42){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }
                if(xB > 0.75){
                    if(Q2 >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB - 0.750) + 9.52){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }


                if(Condition_Up == 1 && Condition_Right == 1){
                    Q2_xB_Bin = 9;
                    return Q2_xB_Bin; // Bin 9 Confirmed
                }

            }
            // End of Bin 9

        }
        /////////////////////////     End of Bin 8 and 9     /////////////////////////



        return Q2_xB_Bin;

    """)
    
    rdf = rdf.Define('Q2_xB_Bin_2', '''
        int Q2_xB_Bin_2 = Q2_xB_Bin;

        if(Q2_xB_Bin > 1 && Q2_xB_Bin_2%2 != 0){
            Q2_xB_Bin_2 += -2;
        }

        if(Q2 < 2){
            Q2_xB_Bin_2 = 0; 
        }

        return Q2_xB_Bin_2;
    ''')
    
    ###########     End of Definitions for Q2 and xB Bins     ##########
    #------------------------------------------------------------------#
    ###############     Definitions for z and pT Bins     ##############
    
    
    # z and pT Binning (See Table 4.3 on page 20 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
    rdf = rdf.Define("z_pT_Bin","""

        int z_pT_Bin = 0;
        int Num_z_Borders = 0;
        int Num_pT_Borders = 0;


        /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {

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
        if(Q2_xB_Bin == 0){
            return z_pT_Bin; // Cannot create z-pT Bins without propper Q2-xB Bins
        }
        // For Q2_xB Bin 1
        if(Q2_xB_Bin == 1){
            // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 2
        if(Q2_xB_Bin == 2){
            // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 3
        if(Q2_xB_Bin == 3){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 4
        if(Q2_xB_Bin == 4){
            // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 5
        if(Q2_xB_Bin == 5){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 6
        if(Q2_xB_Bin == 6){
            // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
            Num_pT_Borders = 6;
        }
        // For Q2_xB Bin 7
        if(Q2_xB_Bin == 7){
            // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
            Num_pT_Borders = 7;
        }
        // For Q2_xB Bin 8
        if(Q2_xB_Bin == 8){
            // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
            Num_pT_Borders = 5;
        }
        // For Q2_xB Bin 9
        if(Q2_xB_Bin == 9){
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



        int z_pT_Bin_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z > Borders_function(Q2_xB_Bin, 0, zbin) && z < Borders_function(Q2_xB_Bin, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT > Borders_function(Q2_xB_Bin, 1, pTbin) && pT < Borders_function(Q2_xB_Bin, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin = z_pT_Bin_count; // The value of the z_pT_Bin has been set
                        return z_pT_Bin;
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


        return z_pT_Bin;



    """)
    
    
    rdf = rdf.Define('z_pT_Bin_2', '''
    
        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {
            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1 (was 3 in old scheme)
            if(Q2_xB_Bin_Num == 1){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

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
            // For Q2_xB Bin 3 (was 5 in old scheme)
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
            // For Q2_xB Bin 5 (was 7 in old scheme)
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
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
            // For Q2_xB Bin 7 (was 9 in old scheme)
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
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



            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };


        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // Default:
        int Num_z_Borders = 8; 
        int Num_pT_Borders = 8;
        int z_pT_Bin_2 = 0;

        // For Q2_xB Bin 0
        if(Q2_xB_Bin_2 == 0){
            z_pT_Bin_2 = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
            Num_z_Borders = 0; Num_pT_Borders = 0;
        }
        // For Q2_xB Bin 1 (Uses Default for both borders)

        // For Q2_xB Bin 2 (Uses Default for both borders)

        // For Q2_xB Bin 3 (Uses Default for both borders)

        // For Q2_xB Bin 4 (Uses Default for pT borders)
        if(Q2_xB_Bin_2 == 4){
            Num_z_Borders = 7;
        }

        // For Q2_xB Bin 5 (New scheme)
        if(Q2_xB_Bin_2 == 5){
            Num_z_Borders = 7; Num_pT_Borders = 7;
        }

        // For Q2_xB Bin 6
        if(Q2_xB_Bin_2 == 6){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 7 (New scheme)
        if(Q2_xB_Bin_2 == 7){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 8
        if(Q2_xB_Bin_2 == 8){
            Num_z_Borders = 6; Num_pT_Borders = 5;
        }

        if(Num_z_Borders == 0){
            Num_z_Borders = 1; Num_pT_Borders = 1;
        }


        int z_pT_Bin_2_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin_2 != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z > Borders_function(Q2_xB_Bin_2, 0, zbin) && z < Borders_function(Q2_xB_Bin_2, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin_2 != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT > Borders_function(Q2_xB_Bin_2, 1, pTbin) && pT < Borders_function(Q2_xB_Bin_2, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin_2 = z_pT_Bin_2_count; // The value of the z_pT_Bin_2 has been set
                        // cout<<"The value of the z_pT_Bin_2 has been set as: "<<z_pT_Bin_2<<endl;
                        break;
                    }
                    else{
                        z_pT_Bin_2_count += 1; // Checking the next bin
                        // cout<<"Checking the next bin"<<endl;
                    }
                }

            }
            else{
                z_pT_Bin_2_count += (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }


        return z_pT_Bin_2;

    
    ''')
    
    
    ###########     End of Definitions for z and pT Bins     ##########
    #-----------------------------------------------------------------#
    #####################     Bin Definitions     #####################
    ###################################################################
    
    
    
    
    
    if(datatype == "pdf"):
        
        #############################################################################
        #####################     Generated Bin Definitions     #####################
        #---------------------------------------------------------------------------#
        ##############     Definitions for Generated Q2 and xB Bins     #############


        # Q2 and xB Binning (See Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
        rdf = rdf.Define("Q2_xB_Bin_gen","""

            int Q2_xB_Bin_gen = 0;

            /////////////////////////       Bin 1       /////////////////////////
            if(xB_gen > 0.0835 && xB_gen < 0.15){
                // Border lines of Bin 1:
                //                 Upper Border:
                //                          Q2_gen = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_gen - 0.0835) + 1.3
                //                 Q2_gen must be less than the equation above for Bin 1
                //
                //                 Lower Border:
                //                          Q2_gen = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_gen - 0.0835) + 1.30   (if xB_gen < 0.12)
                //                          Q2_gen = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_gen - 0.1200) + 1.30   (if xB_gen > 0.12)
                //                 Q2_gen must be greater than the equations above for Bin 1

                int Condition_Up = 0;
                int Condition_Down = 0;
                // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 1


                // Testing Upper Border of Bin 1
                if(Q2_gen <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_gen - 0.0835) + 1.3){
                    Condition_Up = 1; // Condition for upper border of Bin 1 has been met
                }

                // Testing Lower Border of Bin 1
                if(xB_gen < 0.12){
                    if(Q2_gen >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_gen - 0.0835) + 1.30){
                        Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                    }
                }
                if(xB_gen > 0.12){
                    if(Q2_gen >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_gen - 0.1200) + 1.30){
                        Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                    }
                }


                if(Condition_Up == 1 && Condition_Down == 1){
                    Q2_xB_Bin_gen = 1;
                    return Q2_xB_Bin_gen; // Bin 1 Confirmed
                }

            }
            /////////////////////////     End of Bin 1     /////////////////////////




            /////////////////////////       Bin 2 or 3       /////////////////////////
            if(xB_gen > 0.15 && xB_gen < 0.24){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98

                // Deciding between Bins
                if(Q2_gen < ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98){
                    BinTest = 2; // Event will NOT go to bin 3
                }

                if(Q2_gen > ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98){
                    BinTest = 3; // Event will NOT go to bin 2
                }



                // Final Border Test

                // Bin 2
                if(BinTest == 2){
                    // Border lines of Bin 2:   Q2_gen = ((1.45 - 1.38)/(0.20 - 0.15))*(xB_gen - 0.15) + 1.38   (if xB_gen < 0.2)
                    //                          Q2_gen = ((1.50 - 1.45)/(0.24 - 0.20))*(xB_gen - 0.24) + 1.50   (if xB_gen > 0.2)

                    if(xB_gen < 0.2){
                        if(Q2_gen >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB_gen - 0.15) + 1.38){
                            Q2_xB_Bin_gen = 2;
                            return Q2_xB_Bin_gen; // Bin 2 Confirmed
                        }
                    }

                    if(xB_gen > 0.2){
                        if(Q2_gen >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB_gen - 0.24) + 1.50){
                            Q2_xB_Bin_gen = 2;
                            return Q2_xB_Bin_gen; // Bin 2 Confirmed
                        }
                    }

                }
                // End of Bin 2


                // Bin 3
                if(BinTest == 3){
                    // Border line of Bin 3:   Q2_gen = ((3.625 - 2.28)/(0.24 - 0.15))*(xB_gen - 0.15) + 2.28

                    if(Q2_gen <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB_gen - 0.15) + 2.28){
                        Q2_xB_Bin_gen = 3;
                        return Q2_xB_Bin_gen; // Bin 3 Confirmed
                    }

                }
                // End of Bin 3


            }
            /////////////////////////     End of Bin 2 and 3     /////////////////////////




            /////////////////////////       Bin 4 or 5       /////////////////////////
            if(xB_gen > 0.24 && xB_gen < 0.34){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75

                // Deciding between Bins
                if(Q2_gen < ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75){
                    BinTest = 4; // Event will NOT go to bin 5
                }

                if(Q2_gen > ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75){
                    BinTest = 5; // Event will NOT go to bin 4
                }



                // Final Border Test

                // Bin 4
                if(BinTest == 4){
                    // Border lines of Bin 4:   Q2_gen = ((1.53 - 1.50)/(0.27 - 0.24))*(xB_gen - 0.24) + 1.50   (if xB_gen < 0.27)
                    //                          Q2_gen = ((1.56 - 1.53)/(0.30 - 0.27))*(xB_gen - 0.27) + 1.53   (if 0.27 < xB_gen < 0.30)
                    //                          Q2_gen = ((1.60 - 1.56)/(0.34 - 0.30))*(xB_gen - 0.30) + 1.56   (if xB_gen > 0.3)

                    if(xB_gen < 0.27){
                        if(Q2_gen >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB_gen - 0.24) + 1.50){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                    if(xB_gen > 0.27 && xB_gen < 0.30){
                        if(Q2_gen >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB_gen - 0.27) + 1.53){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                    if(xB_gen > 0.30){
                        if(Q2_gen >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB_gen - 0.30) + 1.56){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                }
                // End of Bin 4


                // Bin 5
                if(BinTest == 5){
                    // Border line of Bin 5:   Q2_gen = ((5.12 - 3.625)/(0.34 - 0.24))*(xB_gen - 0.24) + 3.625

                    if(Q2_gen <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB_gen - 0.24) + 3.625){
                        Q2_xB_Bin_gen = 5;
                        return Q2_xB_Bin_gen; // Bin 5 Confirmed
                    }

                }
                // End of Bin 5


            }
            /////////////////////////     End of Bin 4 and 5     /////////////////////////




            /////////////////////////       Bin 6 or 7       /////////////////////////
            if(xB_gen > 0.34 && xB_gen < 0.45){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63

                // Deciding between Bins
                if(Q2_gen < ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63){
                    BinTest = 6; // Event will NOT go to bin 7
                }

                if(Q2_gen > ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63){
                    BinTest = 7; // Event will NOT go to bin 6
                }



                // Final Border Test

                // Bin 6
                if(BinTest == 6){
                    // Border line of Bin 6:   Q2_gen = ((2.52 - 1.60)/(0.45 - 0.34))*(xB_gen - 0.34) + 1.60

                    if(Q2_gen >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB_gen - 0.34) + 1.60){
                        Q2_xB_Bin_gen = 6;
                        return Q2_xB_Bin_gen; // Bin 6 Confirmed
                    }

                }
                // End of Bin 6


                // Bin 7
                if(BinTest == 7){
                    // Border line of Bin 7:   Q2_gen = ((6.76 - 5.12)/(0.45 - 0.34))*(xB_gen - 0.34) + 5.12

                    if(Q2_gen <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB_gen - 0.34) + 5.12){
                        Q2_xB_Bin_gen = 7;
                        return Q2_xB_Bin_gen; // Bin 7 Confirmed
                    }

                }
                // End of Bin 7


            }
            /////////////////////////     End of Bin 6 and 7     /////////////////////////




            /////////////////////////       Bin 8 or 9       /////////////////////////
            if(xB_gen > 0.45){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70    

                // Deciding between Bins
                if(Q2_gen < ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70){
                    BinTest = 8; // Event will NOT go to bin 9
                }
                if(Q2_gen > ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70){
                    BinTest = 9; // Event will NOT go to bin 8
                }



                // Final Border Test

                // Bin 8
                if(BinTest == 8){
                    // Border lines of Bin 8:   Q2_gen = ((3.05 - 2.52)/(0.500 - 0.45))*(xB_gen - 0.45) + 2.52   (if xB_gen < 0.50)
                    //                          Q2_gen = ((4.05 - 3.05)/(0.570 - 0.50))*(xB_gen - 0.50) + 3.05   (if 0.50 < xB_gen < 0.57)
                    //                          Q2_gen = ((5.40 - 4.05)/(0.640 - 0.57))*(xB_gen - 0.57) + 4.05   (if 0.57 < xB_gen < 0.64)
                    //                          Q2_gen = ((7.42 - 5.40)/(0.708 - 0.64))*(xB_gen - 0.64) + 5.40   (if xB_gen > 0.64)

                    if(xB_gen < 0.50){
                        if(Q2_gen >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB_gen - 0.45) + 2.52){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.50 && xB_gen < 0.57){
                        if(Q2_gen >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB_gen - 0.50) + 3.05){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.57 && xB_gen < 0.64){
                        if(Q2_gen >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB_gen - 0.57) + 4.05){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.64){
                        if(Q2_gen >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB_gen - 0.64) + 5.40){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                }
                // End of Bin 8


                // Bin 9
                if(BinTest == 9){
                    // Border lines of Bin 9:
                    //                 Uppermost Border:
                    //                          Q2_gen = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_gen - 0.450) +  6.760   (if xB_gen < 0.677)
                    //                          Q2_gen = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_gen - 0.677) + 10.185   (if xB_gen > 0.677)
                    //                 Q2_gen must be less than the equations above for Bin 9
                    //
                    //                 Rightmost Border:
                    //                          Q2_gen =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_gen - 0.708) + 7.42   (if xB_gen < 0.75)
                    //                          Q2_gen = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_gen - 0.750) + 9.52   (if xB_gen > 0.75)
                    //                 Q2_gen must be greater than the equations above for Bin 9

                    int Condition_Up = 0;
                    int Condition_Right = 0;
                    // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                    // Code will verify both conditions seperately before checking that they have been met.
                    // If the condition has been met, its value will be set to 1.
                    // If either is still 0 when checked, the event will be consided as being outside of Bin 9


                    // Testing Uppermost Border of Bin 9
                    if(xB_gen < 0.677){
                        if(Q2_gen <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_gen - 0.450) +  6.760){
                            Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                        }
                    }
                    if(xB_gen > 0.677){
                        if(Q2_gen <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_gen - 0.677) + 10.185){
                            Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                        }
                    }

                    // Testing Rightmost Border of Bin 9
                    if(xB_gen < 0.75){
                        if(Q2_gen >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_gen - 0.708) + 7.42){
                            Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                        }
                    }
                    if(xB_gen > 0.75){
                        if(Q2_gen >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_gen - 0.750) + 9.52){
                            Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                        }
                    }


                    if(Condition_Up == 1 && Condition_Right == 1){
                        Q2_xB_Bin_gen = 9;
                        return Q2_xB_Bin_gen; // Bin 9 Confirmed
                    }

                }
                // End of Bin 9

            }
            /////////////////////////     End of Bin 8 and 9     /////////////////////////



            return Q2_xB_Bin_gen;

        """)

        
        rdf = rdf.Define('Q2_xB_Bin_2_gen', '''
            int Q2_xB_Bin_2_gen = Q2_xB_Bin_gen;

            if(Q2_xB_Bin_gen > 1 && Q2_xB_Bin_2_gen%2 != 0){
                Q2_xB_Bin_2_gen += -2;
            }

            if(Q2_gen < 1.94){
                Q2_xB_Bin_2_gen = 0; 
            }

            return Q2_xB_Bin_2_gen;
        ''')
        

        ###########     End of Definitions for Generated Q2 and xB Bins     ##########
        #----------------------------------------------------------------------------#
        ###############     Definitions for Generated z and pT Bins     ##############


        # z and pT Binning (See Table 4.3 on page 20 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
        rdf = rdf.Define("z_pT_Bin_gen","""

            int z_pT_Bin_gen = 0;
            int Num_z_Borders = 0;
            int Num_pT_Borders = 0;


            /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

            auto Borders_function = [&](int Q2_xB_Bin_gen_Num, int z_or_pT_gen, int entry)
            {

                // z_or_pT_gen = 0 corresponds to z bins
                // z_or_pT_gen = 1 corresponds to pT bins

                // For Q2_xB Bin 1
                if(Q2_xB_Bin_gen_Num == 1){
                    float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 2
                if(Q2_xB_Bin_gen_Num == 2){
                    float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 3
                if(Q2_xB_Bin_gen_Num == 3){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 4
                if(Q2_xB_Bin_gen_Num == 4){
                    float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 5
                if(Q2_xB_Bin_gen_Num == 5){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 6
                if(Q2_xB_Bin_gen_Num == 6){
                    float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                    float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 7
                if(Q2_xB_Bin_gen_Num == 7){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 8
                if(Q2_xB_Bin_gen_Num == 8){
                    float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                    float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 9
                if(Q2_xB_Bin_gen_Num == 9){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }


                // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
                // return empty_Borders;
                float empty = 0;
                return empty;
            };




            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////



            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin_gen')

            // For Q2_xB Bin 0
            if(Q2_xB_Bin_gen == 0){
                return z_pT_Bin_gen; // Cannot create z-pT Bins without propper Q2-xB Bins
            }
            // For Q2_xB Bin 1
            if(Q2_xB_Bin_gen == 1){
                // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_gen == 2){
                // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 3
            if(Q2_xB_Bin_gen == 3){
                // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_gen == 4){
                // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                Num_z_Borders = 7;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_gen == 5){
                // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_gen == 6){
                // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                Num_z_Borders = 6;
                // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
                Num_pT_Borders = 6;
            }
            // For Q2_xB Bin 7
            if(Q2_xB_Bin_gen == 7){
                // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                Num_z_Borders = 7;
                // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
                Num_pT_Borders = 7;
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_gen == 8){
                // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                Num_z_Borders = 6;
                // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
                Num_pT_Borders = 5;
            }
            // For Q2_xB Bin 9
            if(Q2_xB_Bin_gen == 9){
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



            int z_pT_Bin_gen_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z_pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_gen != 0){
                    continue;   // If the bin has already been assigned, this line will end the loop.
                                // This is to make sure the loop does not run longer than what is necessary.
                }    

                if(z_gen > Borders_function(Q2_xB_Bin_gen, 0, zbin) && z_gen < Borders_function(Q2_xB_Bin_gen, 0, zbin - 1)){
                    // Found the correct z bin

                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_gen != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_gen > Borders_function(Q2_xB_Bin_gen, 1, pTbin) && pT_gen < Borders_function(Q2_xB_Bin_gen, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_gen = z_pT_Bin_gen_count; // The value of the z_pT_Bin_gen has been set
                            return z_pT_Bin_gen;
                        }
                        else{
                            z_pT_Bin_gen_count = z_pT_Bin_gen_count + 1; // Checking the next bin
                        }
                    }

                }
                else{
                    z_pT_Bin_gen_count = z_pT_Bin_gen_count + (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }


            return z_pT_Bin_gen;



        """)
        
        
        rdf = rdf.Define('z_pT_Bin_2_gen', '''

            auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
            {
                // z_or_pT = 0 corresponds to z bins
                // z_or_pT = 1 corresponds to pT bins

                // For Q2_xB Bin 1 (was 3 in old scheme)
                if(Q2_xB_Bin_Num == 1){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

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
                // For Q2_xB Bin 3 (was 5 in old scheme)
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
                // For Q2_xB Bin 5 (was 7 in old scheme)
                if(Q2_xB_Bin_Num == 5){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[6 - entry];
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
                // For Q2_xB Bin 7 (was 9 in old scheme)
                if(Q2_xB_Bin_Num == 7){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
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

                // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
                // return empty_Borders;
                float empty = 0;
                return empty;
            };


            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

            // Default:
            int Num_z_Borders = 8;
            int Num_pT_Borders = 8;
            int z_pT_Bin_2_gen = 0;

            // For Q2_xB Bin 0
            if(Q2_xB_Bin_2_gen == 0){
                z_pT_Bin_2_gen = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
                Num_z_Borders = 0; Num_pT_Borders = 0;
            }
            // For Q2_xB Bin 1 (Uses Default for both borders)

            // For Q2_xB Bin 2 (Uses Default for both borders)

            // For Q2_xB Bin 3 (Uses Default for both borders)

            // For Q2_xB Bin 4 (Uses Default for pT borders)
            if(Q2_xB_Bin_2_gen == 4){
                Num_z_Borders = 7;
            }

            // For Q2_xB Bin 5 (New scheme)
            if(Q2_xB_Bin_2_gen == 5){
                Num_z_Borders = 7; Num_pT_Borders = 7;
            }

            // For Q2_xB Bin 6
            if(Q2_xB_Bin_2_gen == 6){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 7 (New scheme)
            if(Q2_xB_Bin_2_gen == 7){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 8
            if(Q2_xB_Bin_2_gen == 8){
                Num_z_Borders = 6; Num_pT_Borders = 5;
            }

            if(Num_z_Borders == 0){
                Num_z_Borders = 1; Num_pT_Borders = 1;
            }


            int z_pT_Bin_2_gen_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z_pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_2_gen != 0){
                    continue;   // If the bin has already been assigned, this line will end the loop.
                                // This is to make sure the loop does not run longer than what is necessary.
                }    

                if(z_gen > Borders_function(Q2_xB_Bin_2_gen, 0, zbin) && z_gen < Borders_function(Q2_xB_Bin_2_gen, 0, zbin - 1)){
                    // Found the correct z bin

                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_2_gen != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_gen > Borders_function(Q2_xB_Bin_2_gen, 1, pTbin) && pT_gen < Borders_function(Q2_xB_Bin_2_gen, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_2_gen = z_pT_Bin_2_gen_count; // The value of the z_pT_Bin_2_gen has been set
                            // cout<<"The value of the z_pT_Bin_2_gen has been set as: "<<z_pT_Bin_2_gen<<endl;
                            break;
                        }
                        else{
                            z_pT_Bin_2_gen_count += 1; // Checking the next bin
                            // cout<<"Checking the next bin"<<endl;
                        }
                    }

                }
                else{
                    z_pT_Bin_2_gen_count += (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }


            return z_pT_Bin_2_gen;
        
        
        ''')


        ###########     End of Definitions for Generated z and pT Bins     ##########
        #---------------------------------------------------------------------------#
        #####################     Generated Bin Definitions     #####################
        #############################################################################
        #####################      Matched Bin Definitions      #####################
        
        
        def bin_purity_filter_fuction(dataframe, variable, min_range, max_range, number_of_bins):
            
            gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
            
            
            if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable):
                
                if("sec" in variable):
                    gen_variable = gen_variable.replace("_a", "")
                
                filter_name = "".join([variable, " == ", gen_variable, " && ", variable, " != 0"])
                
            else:
            
                bin_size = (max_range - min_range)/number_of_bins

               
                filter_name = "".join(["""
                
                // cout<<endl<<"Starting a new line of purity filtering..."<<endl;

                int rec_bin = (""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """;
                int gen_bin = (""", str(gen_variable), """ - """, str(min_range), """)/""", str(bin_size), """;

                // cout<<endl<<"The reconstructed event (with the value Name_""", str(variable), """ = "<<""", str(variable), """<<") was found in bin "<<rec_bin<<" (Range = "<<(""", str(min_range), """ + (rec_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (rec_bin + 1)*""", str(bin_size), """)<<")"<<endl;
                // cout<<"The generated event (with the value Name_""", str(gen_variable), """ = "<<""", str(gen_variable), """<<") was found in bin "<<gen_bin<<" (Range = "<<(""", str(min_range), """ + (gen_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (gen_bin + 1)*""", str(bin_size), """)<<")"<<endl<<endl;
                
                
                bool filter_Q = (rec_bin == gen_bin && PID_el != 0 && PID_pip != 0);


                return filter_Q;



                """])
            
            
            return dataframe.Filter(str(filter_name))
        
        
        
        
        def bin_purity_save_fuction(dataframe, variable, min_range, max_range, number_of_bins):
            
            variable = variable.replace("_gen", "")
            
            gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
            
            out_put_DF = dataframe
            
            
            if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable):
                # Already defined
                return dataframe
                
            else:
            
                bin_size = (max_range - min_range)/number_of_bins

               
                rec_bin = "".join(["(", str(variable), " - ", str(min_range), ")/", str(bin_size)])
                
                gen_bin = "".join(["(", str(gen_variable), " - ", str(min_range), ")/", str(bin_size)])
                
                out_put_DF = out_put_DF.Define("".join([str(variable), "_REC_BIN"]), rec_bin)
                out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)
            
            
            return out_put_DF
        
        
        
        def bin_purity_save_fuction_New(dataframe, variable, min_range, max_range, number_of_bins):
            
            gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
            
            out_put_DF = dataframe
            
            
            if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable):
                # Already defined
                return dataframe
                
            else:
            
                bin_size = (max_range - min_range)/number_of_bins
                
                rec_bin = "".join(["""
                
                int rec_bin = ((""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;
                
                if(""", str(variable), """ < """, str(min_range), """){
                    // Below binning range
                    rec_bin = 0;
                }
                
                if(""", str(variable), """ > """, str(max_range), """){
                    // Above binning range
                    rec_bin = """, str(number_of_bins + 1), """;
                }
                
                return rec_bin;

                """])
                
                gen_bin = "".join(["""
                
                int gen_bin = ((""", str(gen_variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;
                
                if(""", str(gen_variable), """ < """, str(min_range), """){
                    // Below binning range
                    gen_bin = 0;
                }
                
                if(""", str(gen_variable), """ > """, str(max_range), """){
                    // Above binning range
                    gen_bin = """, str(number_of_bins + 1), """;
                }
                
                if(PID_el == 0 || PID_pip == 0){
                    // Event is unmatched
                    gen_bin = """, str(number_of_bins + 2), """;
                }

                return gen_bin;



                """])
                
                out_put_DF = out_put_DF.Define("".join([str(variable), "_REC_BIN"]), rec_bin)
                out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)
            
            
            return out_put_DF
            
            
            
        def bin_purity_save_filter_fuction(dataframe, variable, min_range, max_range, number_of_bins, REC_BIN_FILTER):
            
            variable = variable.replace("_gen", "")
            
            gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
            
            variable = variable.replace("_gen", "")
            
            out_put_DF = dataframe
            
            if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable):
                filter_name = "".join([variable, " == ", str(REC_BIN_FILTER), " && PID_el != 0 && PID_pip != 0"])
                
            else:
            
                bin_size = (max_range - min_range)/number_of_bins

                filter_name = "".join(["""

                int rec_bin = (""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """;
                
                bool filter_Q = (rec_bin == """, str(REC_BIN_FILTER), """ && PID_el != 0 && PID_pip != 0);

                return filter_Q;

                """])
                
                gen_bin = "".join(["(", str(gen_variable), " - ", str(min_range), ")/", str(bin_size)])
                
                out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)
            
            
            return out_put_DF.Filter(filter_name)
        
        
        
        
        def Delta_Matched_DF(dataframe, variable):
            output = "continue"
            gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
            if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or dataframe == "continue"):
                # Cannot uses these types of variables in this type of histogram
                return "continue"
            else:
                output = dataframe.Define("Delta_Matched_Value", "".join([str(variable), " - ", str(gen_variable)]))

            return output
        
        
        
        
        
#         def Delta_Matched_Bin_Calc(Variable, Min_Bin, Max_Bin):
#             output = "continue"
#             Min_Dif, Max_Dif = (Min_Bin - Max_Bin), (Max_Bin - Min_Bin)
#             if("th" in Variable):
#                 Min_Dif, Max_Dif = -2, 2
#             if("Phi" in Variable):
#                 Min_Dif, Max_Dif = -6, 6
#             Num_of_Bins = int((Max_Dif - Min_Dif)/0.025)
#             if(Num_of_Bins < 200):
#                 Num_of_Bins = 200
#             elif(Num_of_Bins > 600):
#                 Num_of_Bins = 600
#             else:
#                 Num_of_Bins = 400
#             if(((Max_Dif - Min_Dif)/Num_of_Bins) > 1 and (Max_Dif - Min_Dif) < 800):
#                 Num_of_Bins = int(Max_Dif - Min_Dif)
#             output = [Num_of_Bins, Min_Dif, Max_Dif]
#             return output


        
        def Delta_Matched_Bin_Calc(Variable, Min_Bin, Max_Bin):
            output = "continue"
            Min_Dif, Max_Dif = (Min_Bin - Max_Bin), (Max_Bin - Min_Bin)

            if("th" in Variable):
                Min_Dif, Max_Dif = -6, 6

            if("Phi" in Variable):
                Min_Dif, Max_Dif = -10, 10

            Num_of_Bins = int((Max_Dif - Min_Dif)/0.005)
            if(Num_of_Bins < 400):
                Num_of_Bins = 400
            elif(Num_of_Bins < 200):
                Num_of_Bins = 200
            elif(Num_of_Bins > 1500):
                Num_of_Bins = 1500
            elif(Num_of_Bins > 1200):
                Num_of_Bins = 1200
            elif(Num_of_Bins > 800):
                Num_of_Bins = 800
            else:
                Num_of_Bins = 600
            if(((Max_Dif - Min_Dif)/Num_of_Bins) > 1 and (Max_Dif - Min_Dif) < 800):
                Num_of_Bins = int(Max_Dif - Min_Dif)


            output = [Num_of_Bins, Min_Dif, Max_Dif]

            return output
    
    
    
    
    ##############################################################     Done With Kinematic Binning     ##############################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ############################################################     Helpful Functions for Histograms     ###########################################################
    
    
    ###################=========================###################
    ##===============##     Variable Titles     ##===============##
    ###################=========================###################
    
    def variable_Title_name(variable):

        smeared_named, bank_named = '', ''
        
        if("_smeared" in variable):
            smeared_named = 'yes'
            variable = variable.replace("_smeared","")
            
        if("_gen" in variable):
            bank_named = 'yes'
            variable = variable.replace("_gen","")
        
        output = 'error'    

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
            output = "p_{T}"
        if(variable == 'phi_t'):
            output = "#phi_{t}"
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
        if(variable == 'z_pT_Bin'):
            output = "z-p_{T} Bin"
        if(variable == 'z_pT_Bin_2'):
            output = "z-p_{T} Bin (New)"
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
    
    
    
    
    
    ###################=======================================###################
    ##===============##     Full Filter + Histogram Title     ##===============##
    ###################=======================================###################
    
    def DF_Filter_Function_Full(DF, Sec_type, Sec_num, Q2_xB_Bin_Filter, z_pT_Bin_Filter, Variables, Smearing_Q, Data_Type, Cut_Choice, Titles_or_DF):

        if("2" not in Smearing_Q and "P2" in Cut_Choice):
            return "continue"
        
        if('str' in str(type(Variables)) and Q2_xB_Bin_Filter != -1 and Variables != "2D_Purity"):
            return "continue"

        ##============================================##
        ##----------## Setting Data Title ##----------##
        ##============================================##
        if(Titles_or_DF == 'Title'):
            if(Data_Type == 'rdf'):
                Data_Title = "Real Data"
            if(Data_Type == 'mdf' or Data_Type == 'pdf' or Data_Type == 'udf' or ("miss_idf" in Data_Type)):
                Data_Title = "".join(["Monte Carlo Data (REC", " - Smeared)" if "smear" in Smearing_Q else ")"])
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
        ##============================================##
        ##----------## Setting Data Title ##----------##
        ##============================================##


        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type != "mdf" and Data_Type != "pdf" and Data_Type != "udf" and ("miss_idf" not in Data_Type)) and "smear" in Smearing_Q):
            return "continue"
        # No Cuts for Monte Carlo Generated events
        if((Data_Type == "gdf" or Data_Type == "gen") and "no_cut" not in Cut_Choice):
            return "continue"
        # No PID cuts except for matched MC events
        if((Data_Type != "pdf" and Data_Type != "gen") and "PID" in Cut_Choice):
            return "continue"
        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##

        
        ##=======================================================##
        ##----------## Smeared Binning (MC REC Only) ##----------##
        ##=======================================================##
        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"
        if("2" in Smearing_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
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

        if(Q2_xB_Bin_Filter == -2):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "Only Binned Events", "".join([str(Q2_xB_Bin_Filter_str), " != 0"]), -1

        if(Q2_xB_Bin_Filter == -1):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "All Events", "", -2

        if(Q2_xB_Bin_Filter == 0):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "None - Events without a bin", "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)]), -2

        if(Q2_xB_Bin_Filter > 0):
            Q2_xB_BinList_Name, Filter_1 = "".join([variable_Title_name(Q2_xB_Bin_Filter_str), ": ", str(Q2_xB_Bin_Filter)]), "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)])

        if(z_pT_Bin_Filter == -2): # This skips z-pT bins
            z_pT_BinList_Name, Filter_2 = "", ""

        if(z_pT_Bin_Filter == -1):
            z_pT_BinList_Name, Filter_2 = "Only Binned Events", "".join([str(z_pT_Bin_Filter_str), " != 0"])

        if(z_pT_Bin_Filter == 0):
            z_pT_BinList_Name, Filter_2 = "None - Events without a bin", "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])

        if(z_pT_Bin_Filter > 0):
            z_pT_BinList_Name, Filter_2 = "".join([variable_Title_name(z_pT_Bin_Filter_str), ": ", str(z_pT_Bin_Filter)]), "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])


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
                DF_Out = DF.Filter(Filter_Name)
            else:
                DF_Out = DF

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
        if((Data_Type == "pdf" or Data_Type == "gen") and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el != 0 && PID_pip != 0")
            
        if(Data_Type == "udf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el == 0 || PID_pip == 0")
            
        if(Data_Type == "miss_idf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && (PID_el != 11 || PID_pip != 211)")
            
        if(Data_Type == "miss_idf_el" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_el != 11")
            
        if(Data_Type == "miss_idf_pip" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_pip != 211")

        if(Data_Type != "gdf" and Data_Type != "gen" and "no_cut" != Cut_Choice):
            if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
                cutname = " (Smeared)"
                #-----------------------------#
                #-----# As of 3-10-2022 #-----#
                #-----------------------------#
                if("all" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        # DF_Out = DF_Out.Filter("y < 0.75             && xF > 0               && W > 2               && Q2 > 1              && MM > 1.5                    && pip > 1.25              && pip < 5              && 5 < elth             && elth < 35             && 5 < pipth            && pipth < 35")
                        DF_Out = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 1 && sqrt(smeared_vals[1]) > 1.5 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                    cutname = " All (Smeared) Cuts"
                else:
                    if('SIDIS' in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            # DF_Out = DF_Out.Filter("y < 0.75             && xF > 0               && W > 2               && Q2 > 1")
                            DF_Out = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 1")
                        cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "SIDIS Cuts"])
                    if('Mom' in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            # DF_Out = DF_Out.Filter("pip > 1.25            && pip < 5              && 5 < elth             && elth < 35             && 5 < pipth            && pipth < 35")
                            DF_Out = DF_Out.Filter("smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                        cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "Mom Cuts"])
                if("Q2" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        # DF_Out = DF_Out.Filter("Q2 > 2")
                        DF_Out = DF_Out.Filter("smeared_vals[2] > 2")
                    cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "(new) Q^{2} Cut"])
                if(Data_Type == "pdf" and 'PID' in Cut_Choice):
                    cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "Matched PID Cut"])
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter("PID_el == 11 && PID_pip == 211")
            else:
                if("all" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 1 && sqrt(MM2) > 1.5 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                    cutname = " All Cuts"
                else:
                    if('SIDIS' in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 1")
                        cutname = "".join([cutname, "" if cutname == " " else " + ", "SIDIS Cuts"])
                    if('Mom' in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                        cutname = "".join([cutname, "" if cutname == " " else " + ", "Mom Cuts"])
                if("Q2" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter("Q2 > 2")
                    cutname = "".join([cutname, " " if cutname == " " else " + ", "(New) Q^{2} Cut"])
                if(Data_Type == "pdf" and 'PID' in Cut_Choice):
                    cutname = "".join([cutname, " " if cutname == " " else " + ", "Matched PID Cut"])
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter("PID_el == 11 && PID_pip == 211")
            if('Valerii_Cut' in Cut_Choice):
                if(Titles_or_DF == 'DF'):
                    DF_Out = filter_Valerii(DF_Out, Cut_Choice)
                cutname = "".join([cutname, "" if(" " == cutname or " (Smeared)" == cutname) else " + ", "Valerii Cuts"])
                
            if("P2" in Cut_Choice):
                if(Titles_or_DF == 'DF'):
                    DF_Out = bin_purity_filter_fuction(DF_Out, Q2_xB_Bin_Filter_str, 0, 0, 20)
                cutname = "".join([cutname, "" if(" " == cutname or " (Smeared)" == cutname) else " + ", "Binning Purity (New)"])
                    


        else:
            # Generated Monte Carlo should not have cuts applied to it
            cutname = " No Cuts"
        ##################################################
        ##==========##  General Cuts (End)  ##==========##
        ##################################################




        ##====================================================##
        ##----------## Smearing Variables (Start) ##----------##
        ##====================================================##
        # This information does not need to be run if titles are the only things of interest
        if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q and Titles_or_DF == 'DF'):
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

        ##==========## Title Creation ##==========##
        if(Titles_or_DF == 'Title'):
            Title_out_put = "error"
            if('str' in str(type(Variables))):
                # This indicates that the title is for a 1D histogram
                Title_out_put = "".join(["#splitline{", str(Data_Title), " ", str(variable_Title_name(Variables)), "}{", str(Sector_Title_Name), str(cutname), "}; ", str(variable_Title_name(Q2_xB_Bin_Filter_str)), "; ", str(variable_Title_name(z_pT_Bin_Filter_str)), "; ", str(variable_Title_name(Variables))])
            else:
                # Variables = list of variables (for 2D histograms)
                Title_out_put = "".join(["#splitline{", str(Data_Title), " ", str(variable_Title_name(Variables[0])), " vs ", str(variable_Title_name(Variables[1])), "}{", str(Sector_Title_Name), Q2_xB_BinList_Name, str(cutname), "}; ", z_pT_Bin_Filter_str, "; ", str(variable_Title_name(Variables[0])), "; ", str(variable_Title_name(Variables[1]))])
            return Title_out_put
        ##==========## Title Creation ##==========##


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
    ##===============##     Full Filter + Histogram Title     ##===============##
    ###################=======================================###################

    
    
    
    
    
    #########################################################     Helpful Functions for Histograms (End)     ########################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ##################################################################     Choices For Graphing     #################################################################
    
    
    
    ###############################################################
    #####################     Bin Choices     #####################
    
    # For Q2_xB Bins:
            # A value of -2 --> Only Binned Events
            # A value of -1 --> All Events
            # A value of 0 --> Only Non-Binned Events (Events that do not correspond to a bin)
            
    # For z_pT Bins (relavent to later parts of the analysis):
            # A value of -2 --> Skip z-pT bins (This means that only the option for Q2-xB bins will matter for this value of z-pT)
            # A value of -1 --> Only Binned Events
            # A value of 0 --> Only Non-Binned Events (Events that do not correspond to a bin)

    # Q2_xB Bins have a maximum value of 10 (9 total bins)
    
    
    # The following list should include all the desired kinematic bins to be included.
    # # Only necessary for 3D->2D histograms (All binning is already built into the 3D->1D histograms)
    # # # z-pT bins are built into all 3D histograms that this code creates
    # If a Q2-xB bin is missing from this list, then that bin will be skipped when making the histograms


    # # The following are the maximum number of Q2-xB this code recognizes 
#     List_of_Q2_xB_Bins_to_include = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # List_of_Q2_xB_Bins_to_include = [-1, -2]
#     List_of_Q2_xB_Bins_to_include = [-1]
    
    
    
    #####################     Bin Choices     #####################
    ###############################################################
    
    
    
    ##################################################################
    #####################     Sector Choices     #####################
    
    
    # Types_Of_Sectors = ['', 'esec', 'pipsec', 'esec_a', 'pipsec_a']
    # Types_Of_Sectors = ['', 'esec_a', 'pipsec_a']
    # Types_Of_Sectors = ['', 'esec', 'pipsec']
    Types_Of_Sectors = ['']

    # Types_Of_Sectors = '' --> No Sector Filter

    # Sector_Numbers = [-1, 1, 2, 3, 4, 5, 6]
    Sector_Numbers = [-1]

    # Sector_Numbers = -1 or Types_Of_Sectors = '' --> All Sectors
    # Sector_Numbers = 0 --> No Sectors (should have no events but if it does, those events exist as errors in the sector definitions)
    
    
    #####################     Sector Choices     #####################
    ##################################################################
    
    
    
    ###################################################################
    #####################       Cut Choices       #####################
    
    
    # # Cut Naming Conventions:
        # 1) 'no_cut' --> no new cuts are applied (only cuts are made during particle identification (PID))
        #
        # 2) 'Mom' --> (See below)
          # 1.25 < pip < 5
          # 5 < elth < 35
          # 5 < pipth < 35"
        #
        # 3) 'SIDIS' --> (See below)
          # y < 0.75
          # xF > 0
          # W > 2
          # Q2 > 1
        #
        # 4) 'all' --> Combination of 'Mom', 'SIDIS', with an additional Missing Mass cut of: "MM > 1.5"
          # Do not combine with "Mom" or "SIDIS" separately as doing so will be meaningless (combination is already built in) 
        #
        # 5) 'Valerii_Cut' --> Valerii's Fiducial cuts to remove bad detectors
        #
        # 6) 'Q2'  -> New Q2 cut of "Q2 > 2"
        
    # # Other than 'no_cut', all of the above cuts can be combined separately by adding them to the str in cut_list as a suffix of another cut
    # # # Example:
        # # cut_list = ["no_cut", "cut_all", "cut_Mom_SIDIS"]
          # # The first two cuts in the above list are the same as describles in entry (1) and (4) in the list above. The 3rd entry is a combination of "Mom" and "SIDIS" where both cuts are applied together (order doesn't matter). This combination can be done with any of the cuts given in the list above (except 'no_cut') and can be done with as many of them as desired (no limits to number of cuts that can be added to one entry).
    
    
    
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_Q2_Valerii_Cut', 'cut_all_Q2_PID_Valerii_Cut']
    
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_Q2_Valerii_Cut']
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_Q2_Valerii_Cut', 'cut_all_P2_Valerii_Cut', 'cut_all_P2_Q2_Valerii_Cut']
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_Q2_Valerii_Cut', 'cut_all_P2_Valerii_Cut']
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_P2_Valerii_Cut']
#     cut_list = ['no_cut', 'cut_all_Valerii_Cut', 'cut_all_Q2_Valerii_Cut']
    cut_list = ['no_cut', 'cut_all_Q2_Valerii_Cut']

    
    
    #####################       Cut Choices       #####################
    ###################################################################
    
    
    
    #####################################################################################################################
    ###############################################     3D Histograms     ###############################################
    
    # Longer (but not full) option:
    # List_of_Quantities_1D = [['MM', 0, 4.5, 200], ['Q2', 0, 12, 200], ['W', 1, 5, 200], ['s', 1, 20, 200], ['xB', 0, 0.8, 200], ['v', 1, 12, 200], ['y', 0, 1, 200], ['z', 0, 1, 200], ['xF', -0.6, 0.8, 200], ['pT', 0, 1.6, 200], ["epsilon", 0, 1, 200], ['phi_t', 0, 360, 200], ['el_E', 0, 8, 200], ['el', 0, 8, 200], ['elth', 0, 40, 200], ['elPhi', 0, 360, 200], ['pip_E', 0, 6, 200], ['pip', 0, 6, 200], ['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]
    # List_of_Quantities_1D_smeared = [['MM_smeared', 0, 4.5, 200], ['Q2_smeared', 0, 12, 200], ['W_smeared', 1, 5, 200], ['s_smeared', 1, 20, 200], ['xB_smeared', 0, 0.8, 200], ['v_smeared', 1, 12, 200], ['y_smeared', 0, 1, 200], ['z_smeared', 0, 1, 200], ['xF_smeared', -0.6, 0.8, 200], ['pT_smeared', 0, 1.6, 200], ["epsilon_smeared", 0, 1, 200], ['phi_t_smeared', 0, 360, 200], ['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200], ['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200], ['Delta_Smear_El_P', -1.5, 1.5, 100], ['Delta_Smear_El_Th', -1.5, 1.5, 100], ['Delta_Smear_El_Phi', -1.5, 1.5, 100], ['Delta_Smear_Pip_P', -1.5, 1.5, 100], ['Delta_Smear_Pip_Th', -1.5, 1.5, 100], ['Delta_Smear_Pip_Phi', -1.5, 1.5, 100]]
    
    
    # Normal + 'elec_events_found' Option:
    # List_of_Quantities_1D = [['MM', 0, 4.5, 200], ['Q2', 0, 12, 200], ['W', 1, 5, 200], ['s', 1, 20, 200], ['xB', 0, 0.8, 200], ['v', 1, 12, 200], ['y', 0, 1, 200], ['z', 0, 1, 200], ['xF', -0.6, 0.8, 200], ['pT', 0, 1.6, 200], ['phi_t', 0, 360, 200], ['el', 0, 8, 200], ['elth', 0, 40, 200], ['elPhi', 0, 360, 200], ['pip', 0, 6, 200], ['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200], ['elec_events_found', 0, 1200000000, 1200000000]]
    # List_of_Quantities_1D_smeared = [['MM_smeared', 0, 4.5, 200], ['Q2_smeared', 0, 12, 200], ['W_smeared', 1, 5, 200], ['s_smeared', 1, 20, 200], ['xB_smeared', 0, 0.8, 200], ['v_smeared', 1, 12, 200], ['y_smeared', 0, 1, 200], ['z_smeared', 0, 1, 200], ['xF_smeared', -0.6, 0.8, 200], ['pT_smeared', 0, 1.6, 200], ['phi_t_smeared', 0, 360, 200], ['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200], ['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200], ['elec_events_found', 0, 1200000000, 1200000000]]
    
    
    # Normal + 'epsilon' Option:
    # List_of_Quantities_1D = [["epsilon", 0, 1, 200], ['Q2', 0, 12, 200], ['s', 1, 20, 200], ['W', 1, 5, 200], ['xB', 0, 0.8, 200], ['z', 0, 1, 200], ['pT', 0, 1.6, 200], ['phi_t', 0, 360, 200], ['el', 0, 8, 200], ['elth', 0, 40, 200], ['elPhi', 0, 360, 200], ['pip', 0, 6, 200], ['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]
    # List_of_Quantities_1D_smeared = [["epsilon_smeared", 0, 1, 200], ['Q2_smeared', 0, 12, 200], ['s_smeared', 1, 20, 200], ['W_smeared', 1, 5, 200], ['xB_smeared', 0, 0.8, 200], ['z_smeared', 0, 1, 200], ['pT_smeared', 0, 1.6, 200], ['phi_t_smeared', 0, 360, 200], ['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200], ['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200], ['Delta_Smear_El_P', -1.5, 1.5, 100], ['Delta_Smear_El_Th', -1.5, 1.5, 100], ['Delta_Smear_El_Phi', -1.5, 1.5, 100], ['Delta_Smear_Pip_P', -1.5, 1.5, 100], ['Delta_Smear_Pip_Th', -1.5, 1.5, 100], ['Delta_Smear_Pip_Phi', -1.5, 1.5, 100]]
    
    
    # # Normal Option (True):
    # List_of_Quantities_1D = [['MM', 0, 4.5, 9], ['Q2', -0.1, 12.9, 10], ['W', 1, 5, 100], ['xB', -0.05, 0.95, 10], ['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10], ['phi_t', 0, 360, 20], ['el', 0, 10, 10], ['elth', 0, 40, 24], ['elPhi', 0, 360, 90], ['pip', 0, 8, 8], ['pipth', 0, 40, 22], ['pipPhi', 0, 360, 80]]
    # List_of_Quantities_1D_smeared = [['MM_smeared', 0, 4.5, 9], ['Q2_smeared', -0.1, 12.9, 10], ['W_smeared', 1, 5, 100], ['xB_smeared', -0.05, 0.95, 10], ['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10], ['phi_t_smeared', 0, 360, 20], ['el_smeared', 0, 10, 10], ['elth_smeared', 0, 40, 24], ['elPhi_smeared', 0, 360, 90], ['pip_smeared', 0, 8, 8], ['pipth_smeared', 0, 40, 22], ['pipPhi_smeared', 0, 360, 80]]
    
    # # Just Q2:
    # List_of_Quantities_1D = [['Q2', 0, 12, 240]]
    # List_of_Quantities_1D_smeared = [['Q2_smeared', 0, 12, 240]]
    
    
    # Normal Option (True - New):
    # List_of_Quantities_1D = [['MM', 0, 4.5, 9], ['y', 0, 1, 20], ['Q2', -0.65, 12.35, 20], ['W', 1, 5, 100], ['xB', -0.05, 0.95, 20], ['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10], ['phi_t', 0, 360, 45], ['el', 0, 10, 10], ['elth', 0, 40, 24], ['elPhi', 0, 360, 90], ['pip', 0, 8, 8], ['pipth', 0, 40, 22], ['pipPhi', 0, 360, 80]]
    # List_of_Quantities_1D_smeared = [['MM_smeared', 0, 4.5, 9], ['y_smeared', 0, 1, 20], ['Q2_smeared', -0.65, 12.35, 20], ['W_smeared', 1, 5, 100], ['xB_smeared', -0.05, 0.95, 20], ['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10], ['phi_t_smeared', 0, 360, 45], ['el_smeared', 0, 10, 10], ['elth_smeared', 0, 40, 24], ['elPhi_smeared', 0, 360, 90], ['pip_smeared', 0, 8, 8], ['pipth_smeared', 0, 40, 22], ['pipPhi_smeared', 0, 360, 80]]
#     List_of_Quantities_1D = [['y', 0, 1, 20], ['Q2', -0.65, 12.35, 20], ['xB', -0.05, 0.95, 20], ['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10], ['phi_t', 0, 360, 45], ['el', 0, 10, 10], ['elth', 0, 40, 24], ['elPhi', 0, 360, 90], ['pip', 0, 8, 8], ['pipth', 0, 40, 22], ['pipPhi', 0, 360, 80]]
#     List_of_Quantities_1D_smeared = [['y_smeared', 0, 1, 20], ['Q2_smeared', -0.65, 12.35, 20], ['xB_smeared', -0.05, 0.95, 20], ['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10], ['phi_t_smeared', 0, 360, 45], ['el_smeared', 0, 10, 10], ['elth_smeared', 0, 40, 24], ['elPhi_smeared', 0, 360, 90], ['pip_smeared', 0, 8, 8], ['pipth_smeared', 0, 40, 22], ['pipPhi_smeared', 0, 360, 80]]
    
#     List_of_Quantities_1D = [['Q2', -0.65, 12.35, 20], ['xB', -0.05, 0.95, 20], ['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10], ['phi_t', 0, 360, 36], ['el', 0, 10, 10], ['elth', 0, 40, 24], ['elPhi', 0, 360, 90], ['pip', 0, 8, 8], ['pipth', 0, 40, 22], ['pipPhi', 0, 360, 80]]
#     List_of_Quantities_1D_smeared = [['Q2_smeared', -0.65, 12.35, 20], ['xB_smeared', -0.05, 0.95, 20], ['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10], ['phi_t_smeared', 0, 360, 36], ['el_smeared', 0, 10, 10], ['elth_smeared', 0, 40, 24], ['elPhi_smeared', 0, 360, 90], ['pip_smeared', 0, 8, 8], ['pipth_smeared', 0, 40, 22], ['pipPhi_smeared', 0, 360, 80]]
    
    
    # # For 2D (from 3D) histograms:
    
        # # # Both Binnings and particle momentum kinematics
    # List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['xB', 0, 0.8, 200]], [['z', 0, 1, 200], ['pT', 0, 1.6, 200]], [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['el', 0, 8, 200], ['elPhi', 0, 360, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pip', 0, 6, 200], ['pipPhi', 0, 360, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]

        # # Both Binnings (Only)
    # List_of_Quantities_2D = [[['Q2', -0.65, 12.35, 20], ['xB', -0.05, 0.95, 20]], [['y', 0, 1, 20], ['xB', -0.05, 0.95, 20]], [['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10]]]
    # List_of_Quantities_2D_smeared = [[['Q2_smeared', -0.65, 12.35, 20], ['xB_smeared', -0.05, 0.95, 20]], [['y_smeared', 0, 1, 20], ['xB_smeared', -0.05, 0.95, 20]], [['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10]]]
#     List_of_Quantities_2D = [[['Q2', -0.65, 12.35, 200], ['xB', -0.05, 0.95, 200]], [['z', -0.03, 1.05, 120], ['pT', -0.2, 1.8, 100]]]
#     List_of_Quantities_2D_smeared = [[['Q2_smeared', -0.65, 12.35, 200], ['xB_smeared', -0.05, 0.95, 200]], [['z_smeared', -0.03, 1.05, 120], ['pT_smeared', -0.2, 1.8, 100]]]
    
        # # # Plotting major variables vs phi_t
    # List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['phi_t', 0, 360, 200]], [['xB', 0, 0.8, 200], ['phi_t', 0, 360, 200]], [['z', 0, 1, 200], ['phi_t', 0, 360, 200]], [['pT', 0, 1.6, 200], ['phi_t', 0, 360, 200]]]
    # List_of_Quantities_2D_smeared = [[['Q2_smeared', 0, 12, 200], ['phi_t_smeared', 0, 360, 400]], [['xB_smeared', 0, 0.8, 200], ['phi_t_smeared', 0, 360, 400]], [['z_smeared', 0, 1, 200], ['phi_t_smeared', 0, 360, 400]], [['pT_smeared', 0, 1.6, 200], ['phi_t_smeared', 0, 360, 400]]]
    
    
    
    
#     List_of_Quantities_1D = [['Q2', -0.65, 12.35, 20], ['xB', -0.05, 0.95, 20], ['z', -0.03, 1.05, 12], ['pT', -0.2, 1.8, 10], ['phi_t', 0, 360, 36], ['el', 0, 10, 10], ['elth', 0, 40, 24], ['elPhi', 0, 360, 90], ['pip', 0, 8, 8], ['pipth', 0, 40, 22], ['pipPhi', 0, 360, 80]]
#     List_of_Quantities_1D_smeared = [['Q2_smeared', -0.65, 12.35, 20], ['xB_smeared', -0.05, 0.95, 20], ['z_smeared', -0.03, 1.05, 12], ['pT_smeared', -0.2, 1.8, 10], ['phi_t_smeared', 0, 360, 36], ['el_smeared', 0, 10, 10], ['elth_smeared', 0, 40, 24], ['elPhi_smeared', 0, 360, 90], ['pip_smeared', 0, 8, 8], ['pipth_smeared', 0, 40, 22], ['pipPhi_smeared', 0, 360, 80]]
#     List_of_Quantities_2D = [[['Q2', -0.65, 12.35, 200], ['xB', -0.05, 0.95, 200]], [['z', -0.03, 1.05, 120], ['pT', -0.2, 1.8, 100]]]
#     List_of_Quantities_2D_smeared = [[['Q2_smeared', -0.65, 12.35, 200], ['xB_smeared', -0.05, 0.95, 200]], [['z_smeared', -0.03, 1.05, 120], ['pT_smeared', -0.2, 1.8, 100]]]
    
    
# #     # Bin Set Option: 2 bins
# #     Q2_Binning = ['Q2', -3, 17, 4]
# #     Q2_Binning_Smeared = ['Q2_smeared', -3, 17, 4]
# #     # Bin size: 5.0
#     # Bin Set Option: 2 bins (Actual total bins = 4)
#     Q2_Binning = ['Q2', -2.6755, 16.0265, 4]
#     Q2_Binning_Smeared = ['Q2_smeared', -2.6755, 16.0265, 4]
#     # Bin size: 4.6755 per bin

    
# #     xB_Binning = ['xB', -0.22, 1.14, 4]
# #     xB_Binning_Smeared = ['xB_smeared', -0.22, 1.14, 4]
# #     # Bin size: 0.34

#     # Bin Set Option: 2 bins (Actual total bins = 4)
#     xB_Binning = ['xB', -0.2049, 1.1211, 4]
#     xB_Binning_Smeared = ['xB_smeared', -0.2049, 1.1211, 4]
#     # Bin size: 0.3315 per bin

    
#     z_Binning = ['z', -0.21, 1.23, 4]
#     z_Binning_Smeared = ['z_smeared', -0.21, 1.23, 4]
#     # Bin size: 0.36
    
#     pT_Binning = ['pT', -0.75, 2.25, 4]
#     pT_Binning_Smeared = ['pT_smeared', -0.75, 2.25, 4]
#     # Bin size: 0.75

#     y_Binning = ['y', -0.075, 1.025, 4]
#     y_Binning_Smeared = ['y_smeared', -0.075, 1.025, 4]
#     # Bin size: 0.275
    
#     phi_t_Binning = ['phi_t', 0, 360, 4]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 4]
#     # Bin size: 90
    
    
# #     # Bin Set Option: 3 bins
# #     Q2_Binning = ['Q2', -1.2, 14.8, 5]
# #     Q2_Binning_Smeared = ['Q2_smeared', -1.2, 14.8, 5]
# #     # Bin size: 3.2
#     # Bin Set Option: 3 bins (Actual total bins = 5)
#     Q2_Binning = ['Q2', -1.117, 14.468, 5]
#     Q2_Binning_Smeared = ['Q2_smeared', -1.117, 14.468, 5]
#     # Bin size: 3.117 per bin

    
# #     xB_Binning = ['xB', -0.107, 1.028, 5]
# #     xB_Binning_Smeared = ['xB_smeared', -0.107, 1.028, 5]
# #     # Bin size: 0.227

#     # Bin Set Option: 3 bins (Actual total bins = 5)
#     xB_Binning = ['xB', -0.0944, 1.0106, 5]
#     xB_Binning_Smeared = ['xB_smeared', -0.0944, 1.0106, 5]
#     # Bin size: 0.221 per bin

    
#     z_Binning = ['z', -0.09, 1.11, 5]
#     z_Binning_Smeared = ['z_smeared', -0.09, 1.11, 5]
#     # Bin size: 0.24
    
#     pT_Binning = ['pT', -0.5, 2, 5]
#     pT_Binning_Smeared = ['pT_smeared', -0.5, 2, 5]
#     # Bin size: 0.5

#     y_Binning = ['y', -0.16666, 1.11665, 7]
#     y_Binning_Smeared = ['y_smeared', -0.16666, 1.11665, 7]
#     # Bin size: 0.18333
    
#     phi_t_Binning = ['phi_t', 0, 360, 5]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 5]
#     # Bin size: 72
    
    
# #     # Bin Set Option: 4 bins
# #     Q2_Binning = ['Q2', -0.35, 13.75, 6]
# #     Q2_Binning_Smeared = ['Q2_smeared', -0.35, 13.75, 6]
# #     # Bin size: 2.35
#     # Bin Set Option: 4 bins (Actual total bins = 6)
#     Q2_Binning = ['Q2', -0.3378, 13.6888, 6]
#     Q2_Binning_Smeared = ['Q2_smeared', -0.3378, 13.6888, 6]
#     # Bin size: 2.33775 per bin

    
# #     xB_Binning = ['xB', -0.05, 1.028, 6]
# #     xB_Binning_Smeared = ['xB_smeared', -0.05, 1.028, 6]
# #     # Bin size: 0.17

#     # Bin Set Option: 4 bins (Actual total bins = 6)
#     xB_Binning = ['xB', -0.0391, 0.9554, 6]
#     xB_Binning_Smeared = ['xB_smeared', -0.0391, 0.9554, 6]
#     # Bin size: 0.16575 per bin

    
#     z_Binning = ['z', -0.03, 1.05, 6]
#     z_Binning_Smeared = ['z_smeared', -0.03, 1.05, 6]
#     # Bin size: 0.18
    
#     pT_Binning = ['pT', -0.375, 1.875, 6]
#     pT_Binning_Smeared = ['pT_smeared', -0.375, 1.875, 6]
#     # Bin size: 0.375

#     y_Binning = ['y', -0.075, 1.025, 8]
#     y_Binning_Smeared = ['y_smeared', -0.075, 1.025, 8]
#     # Bin size: 0.1375
    
#     phi_t_Binning = ['phi_t', 0, 360, 6]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 6]
#     # Bin size: 60
    
    
# #     # Bin Set Option: 5 bins
# #     Q2_Binning = ['Q2', 0, 14, 7]
# #     Q2_Binning_Smeared = ['Q2_smeared', 0, 14, 7]
# #     # Bin size: 2
#     # Bin Set Option: 5 bins (Actual total bins = 8)
#     Q2_Binning = ['Q2', -1.7404, 13.2212, 8]
#     Q2_Binning_Smeared = ['Q2_smeared', -1.7404, 13.2212, 8]
#     # Bin size: 1.8702 per bin

    
# #     xB_Binning = ['xB', -0.16, 0.96, 7]
# #     xB_Binning_Smeared = ['xB_smeared', -0.16, 0.96, 7]
# #     # Bin size: 0.16

#     # Bin Set Option: 5 bins (Actual total bins = 7)
#     xB_Binning = ['xB', -0.006, 0.9222, 7]
#     xB_Binning_Smeared = ['xB_smeared', -0.006, 0.9222, 7]
#     # Bin size: 0.1326 per bin

    
#     z_Binning = ['z', 0.006, 1.014, 7]
#     z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 7]
#     # Bin size: 0.144
    
#     pT_Binning = ['pT', -0.3, 1.8, 7]
#     pT_Binning_Smeared = ['pT_smeared', -0.3, 1.8, 7]
#     # Bin size: 0.3

#     y_Binning = ['y', -0.02, 1.08, 10]
#     y_Binning_Smeared = ['y_smeared', -0.02, 1.08, 10]
#     # Bin size: 0.11
    
#     phi_t_Binning = ['phi_t', 0, 360, 12]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 12]
#     # Bin size: 30
    
    
# #     # Bin Set Option: 10 bins
# #     Q2_Binning = ['Q2', 0, 13, 13]
# #     Q2_Binning_Smeared = ['Q2_smeared', 0, 13, 13]
    
#     # Bin Set Option: 10 bins (Actual total bins = 14)
#     Q2_Binning = ['Q2', -0.8053, 12.2861, 14]
#     Q2_Binning_Smeared = ['Q2_smeared', -0.8053, 12.2861, 14]
#     # Bin size: 0.9351 per bin
    
# #     xB_Binning = ['xB', -0.08, 0.96, 13]
# #     xB_Binning_Smeared = ['xB_smeared', -0.08, 0.96, 13]
    
    
#         # Bin Set Option: 10 bins (Actual total bins = 13)
#     xB_Binning = ['xB', -0.006, 0.8559, 13]
#     xB_Binning_Smeared = ['xB_smeared', -0.006, 0.8559, 13]
#     # Bin size: 0.0663 per bin

#     z_Binning = ['z', 0.006, 1.014, 14]
#     z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 14]
    
#     pT_Binning = ['pT', -0.15, 1.8, 13]
#     pT_Binning_Smeared = ['pT_smeared', -0.15, 1.8, 13]
    
#     y_Binning = ['y', -0.02, 1.025, 19]
#     y_Binning_Smeared = ['y_smeared', -0.02, 1.025, 19]
#     # Bin size: 0.055
    
#     phi_t_Binning = ['phi_t', 0, 360, 24]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 24]


    # Bin Set Option: 20 bins
#     Q2_Binning = ['Q2', 0, 12.5, 25]
#     Q2_Binning_Smeared = ['Q2_smeared', 0, 12.5, 25]
    
    # Bin Set Option: 20 bins (Actual total bins = 27)
    Q2_Binning = ['Q2', -0.3378, 12.2861, 27]
    Q2_Binning_Smeared = ['Q2_smeared', -0.3378, 12.2861, 27]
    # Bin size: 0.46755 per bin
    
#     xB_Binning = ['xB', -0.08, 0.92, 25]
#     xB_Binning_Smeared = ['xB_smeared', -0.08, 0.92, 25]
    
    # Bin Set Option: 20 bins (Actual total bins = 25)
    xB_Binning = ['xB', -0.006, 0.8228, 25]
    xB_Binning_Smeared = ['xB_smeared', -0.006, 0.8228, 25]
    # Bin size: 0.03315 per bin

    z_Binning = ['z', 0.006, 1.014, 28]
    z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 28]
    
    pT_Binning = ['pT', -0.15, 1.8, 26]
    pT_Binning_Smeared = ['pT_smeared', -0.15, 1.8, 26]

    y_Binning = ['y', -0.0075, 0.9975, 36]
    y_Binning_Smeared = ['y_smeared', -0.0075, 0.9975, 36]
    # Bin size: 0.0275
    
    phi_t_Binning = ['phi_t', 0, 360, 36]
    phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 36]


# #     # Bin Set Option: 40 bins
# #     Q2_Binning = ['Q2', 0, 12.5, 50]
# #     Q2_Binning_Smeared = ['Q2_smeared', 0, 12.5, 50]
    
#     # Bin Set Option: 40 bins (Actual total bins = 52)
#     Q2_Binning = ['Q2', -0.104, 12.0525, 52]
#     Q2_Binning_Smeared = ['Q2_smeared', -0.104, 12.0525, 52]
#     # Bin size: 0.23378 per bin
    
# #     xB_Binning = ['xB', -0.08, 0.92, 50]
# #     xB_Binning_Smeared = ['xB_smeared', -0.08, 0.92, 50]
    
    
#         # Bin Set Option: 40 bins (Actual total bins = 50)
#     xB_Binning = ['xB', -0.006, 0.8225, 50]
#     xB_Binning_Smeared = ['xB_smeared', -0.006, 0.8225, 50]
#     # Bin size: 0.01657 per bin

#     z_Binning = ['z', 0.006, 1.014, 56]
#     z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 56]
    
#     pT_Binning = ['pT', -0.15, 1.8, 52]
#     pT_Binning_Smeared = ['pT_smeared', -0.15, 1.8, 52]

#     y_Binning = ['y', -0.0075, 0.9975, 72]
#     y_Binning_Smeared = ['y_smeared', -0.0075, 0.9975, 72]
#     # Bin size: 0.01375
    
#     phi_t_Binning = ['phi_t', 0, 360, 45]
#     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 45]
    
    
    List_of_Quantities_1D = [Q2_Binning, y_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning]
    List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, y_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, phi_t_Binning_Smeared]
    
    List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [y_Binning, xB_Binning], [z_Binning, pT_Binning]]
    List_of_Quantities_2D_smeared = [[Q2_Binning_Smeared, xB_Binning_Smeared], [y_Binning_Smeared, xB_Binning_Smeared], [z_Binning_Smeared, pT_Binning_Smeared]]
    
    
    
    
    
        # # # 2D histograms are turned off with these options
    # List_of_Quantities_2D = []
    # List_of_Quantities_2D_smeared = []
    
    if(len(List_of_Quantities_2D) == 0):
        print("Not running 2D histograms...")
    
    
    
    
    
    ##############################################################     End of Choices For Graphing     ##############################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ###########################################################     Graphing Results + Final ROOT File     ##########################################################
    
    
    
    ###########################################################
    #################     Final ROOT File     #################
    
    
    ROOT_File_Output_Name = "Data_REC"
    
#     Extra_Name = "Purity_V9_"
# #     Extra_Name = "Just_Q2_"
#     Extra_Name = "Purity_V11_"
#     Extra_Name = "Purity_V12_"
#     Extra_Name = "Purity_V13_"
    
#     Extra_Name = "Purity_V14_"
    
#     Extra_Name = "Purity_V14_New_"
#     Extra_Name = "Purity_V16_"
    
    
#     Extra_Name = "Purity_V17_"


#     Extra_Name = "Purity_V19_2_Bin_Test_"

#     Extra_Name = "Purity_V19_3_Bin_Test_"
    
#     Extra_Name = "Purity_V20_5_Bin_Test_"
    
#     Extra_Name = "Purity_V20_10_Bin_Test_"

#     Extra_Name = "Purity_V21_20_Bin_Test_"
    
#     Extra_Name = "Purity_V22_20_Bin_Test_"
    
#     Extra_Name = "Purity_V23_20_Bin_Test_"

#     Extra_Name = "Purity_V24_20_Bin_Test_"
    
    Extra_Name = "Purity_V25_20_Bin_Test_"
    
    
    if(datatype == 'rdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_Data_REC_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'mdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_REC_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'gdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_GEN_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'pdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Matched_", str(Extra_Name), str(file_num), ".root"])
        
    if(output_type == "data" or output_type == "test"):
        ROOT_File_Output_Name = "".join(["DataFrame_", ROOT_File_Output_Name])
    
    print("".join(["File being made is: ", ROOT_File_Output_Name]))
    
    
    # File to be saved
    if(str(file_location) != 'time' and output_type == "histo"):
        ROOT_File_Output = ROOT.TFile(str(ROOT_File_Output_Name),'recreate')
    
    
    #################     Final ROOT File     #################
    ###########################################################
    
    
    if(output_type == "histo" or output_type == "time"):
        Kinetic_Histo_3D, histo_for_counts, histo_for_2D_Purity, histo_for_migration, count_of_histograms = {}, {}, {}, {}, 0

        print("Making Histograms...")
        ######################################################################
        ##=====##=====##=====##    Top of Main Loop    ##=====##=====##=====##
        ######################################################################

        ##=====##  Datatype Loop  ##=====##

        if(datatype == "pdf"):
            # datatype_list = ["mdf", "pdf", "gen", "udf", "miss_idf", "miss_idf_el", "miss_idf_pip"]
            # datatype_list = ["mdf", "pdf", "gen", "udf", "miss_idf"]
            # datatype_list = ["mdf", "pdf", "udf", "miss_idf"]
            datatype_list = ["mdf", "pdf", "gen"]
        else:
            datatype_list = [datatype]

        for datatype_2 in datatype_list:

            ##=====##    Smearing Loop    ##=====##

            for smearing_Q in ["", "smear", "2", "smear_2"]:

                Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"

                if("2" in smearing_Q):
                    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])

                if("smear" in smearing_Q and (datatype_2 == "mdf" or datatype_2 == "pdf" or datatype_2 == "udf" or ("miss_idf" in datatype_2))):
                    Variable_Loop, Variable_Loop_2D = List_of_Quantities_1D_smeared, List_of_Quantities_2D_smeared
                    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])

                elif("smear" in smearing_Q and (datatype_2 != "mdf" and datatype_2 != "pdf" and datatype_2 != "udf" and ("miss_idf" not in datatype_2))):
                    # Do not smear anything except for the MC REC Data
                    continue

                else:
                    Variable_Loop, Variable_Loop_2D = List_of_Quantities_1D, List_of_Quantities_2D
                    if(datatype_2 == "gen"):
                        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
                        Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                        for list1 in Variable_Loop:
                            list1[0] = "".join([list1[0], "_gen"])

                ##=====##    Cut Loop     ##=====##

                for cut_choice in cut_list:

                    ##=====##    Sector Type Loop    ##=====##

                    for sec_type in Types_Of_Sectors:
                        if(sec_type == ''):
                            Sector_Numbers_List = [-1]
                        else:
                            Sector_Numbers_List = Sector_Numbers

                        ##=====##    Sector Number Loop    ##=====##

                        for sec_num in Sector_Numbers_List:
                            if(sec_num == -1 and sec_type != '' and '' in Types_Of_Sectors):
                                continue

                            ##=====##    Histogram Option Loop/Selection    ##=====##

                            if(datatype_2 == 'pdf'):
                                # histo_options = ["has_matched", "bin_purity", "delta_matched", "counts"]
                                # histo_options = ["has_matched", "bin_purity", "bin_2D_purity", "counts"]
                                # histo_options = ["has_matched", "bin_purity", "counts"]
#                                 histo_options = ["has_matched", "bin_purity", "counts", "bin_migration"]
                                histo_options = ["has_matched", "bin_purity", "counts", "bin_migration_V2", "bin_migration_V3", "bin_migration_V4"]
                                # Meaning of the above options:
                                # # 'has_matched' --> runs 'pdf' normally (filters unmatched events but otherwise is the same as histo_option = "normal")
                                # # 'bin_purity' --> filters events in which the reconstructed bin is different from the generated bin
                                # # 'delta_matched' --> makes histograms which plot the difference between the reconstructed and generated (∆val) versus the reconstructed value    
                                # # 'counts' --> This option gives information on the number of events that are in the file, have been matched, and survive all cuts
                                # # 'bin_2D_purity' --> Gives the 2D bin purities (like how 'counts' works for giving the number of events in different cuts)
                                # # 'bin_migration' --> shows where events are migrating from
                                # # 'bin_migration_V2' --> similar to 'bin_migration' option but makes a single 2D plot to show the GEN variable vs the REC variable
                                # # 'bin_migration_V3' --> similar to 'bin_migration' option but makes a single 2D plot to show the GEN Bin vs the REC Bin with extra information regarding bins outside the defined range AND regarding the unmatched events
                                # # 'bin_migration_V4' --> similar to 'bin_migration_V3' option but uses a separate binning scheme that is more appropriate to different bin migration study (all binning schemes at once)
                            elif('miss_idf' in datatype_2):
                                histo_options = ["normal", "bin_purity", "delta_matched"]
                            else:
                                histo_options = ["normal"]
                                # runs code normally

                            for option in histo_options:

                                if(option == "normal" or option == "has_matched" or option == "bin_purity" or option == "delta_matched"):
                                # if(option != "counts" and option != "bin_2D_purity" and option != "bin_migration"):
                                    ##====================================##
                                    ##=====##    Variable Loops    ##=====##

                                    #####################################################################################################################
                                    ###############################################     1D Histograms     ###############################################
                                    for list1 in Variable_Loop:
                                        cutname, Histo_Title = "continue", "continue"
                                        if(option == "normal" or option == "has_matched"):
                                            cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                            Histo_Title = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")

                                            Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                            if("2" in smearing_Q):
                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))

                                        if(option == "bin_purity"):
                                            cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                            Histo_Title = (DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")).replace("Matched", "Purity Match")

                                            Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - Purity - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                            if("2" in smearing_Q):
                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - Purity - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))

                                        if(option == "delta_matched"):
                                            final_df = Delta_Matched_DF(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF"), list1[0]) # Calculates the different between the matched reconstructed and generated events (rec - gen)
                                            if(final_df == "continue"):
                                                continue
                                            cutname = DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                            Histo_Title = "".join([((DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")).replace("Matched", "Difference Between Match").replace("; Q^{2}-x_{B} Bin (Smeared); z-p_{T} Bin (Smeared)", "").replace("; Q^{2}-x_{B} Bin; z-p_{T} Bin", "")), "; #Delta(REC - GEN)"])

                                            Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - Dif Match - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                            if("2" in smearing_Q):
                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - Dif Match - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))

                                        if(cutname == "continue" or Histo_Title == "continue"):
                                            continue


                                        if(option != "delta_matched" and option != "bin_purity"):
                                            Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF").Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), 14, -3, 10, 54, -3, 50, list1[3], list1[1], list1[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(list1[0]))
                                        elif(option == "bin_purity"):
                                            Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF"), list1[0], list1[1], list1[2], list1[3]).Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), 14, -3, 10, 54, -3, 50, list1[3], list1[1], list1[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(list1[0]))
                                        elif(option == "delta_matched"):
                                            if("el" not in list1[0] and "pip" not in list1[0]):
                                                continue # Don't need these extra ∆(REC-GEN) histograms (angles/momentum are the only criteria being considered)
                                            delta_bins = Delta_Matched_Bin_Calc(list1[0], list1[1], list1[2])
                                            if("continue" in delta_bins):
                                                continue
                                            Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = final_df.Histo2D((str(Kinetic_Histo_3D_Name), str(Histo_Title), list1[3], list1[1], list1[2], delta_bins[0], delta_bins[1], delta_bins[2]), str(list1[0]), "Delta_Matched_Value")
                                            if("Phi" in list1[0]):
                                                Kinetic_Histo_3D["".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"])] = DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, str(list1[0].replace("Phi", "th")), smearing_Q, datatype_2, cut_choice, "DF").Histo3D(("".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"]), "".join([Histo_Title, ";#theta_{", "el" if "el" in list1[0] else "#pi+" ,"}"]), list1[3], list1[1], list1[2], delta_bins[0], delta_bins[1], delta_bins[2], 34, 0, 40), str(list1[0]), "Delta_Matched_Value", str(list1[0].replace("Phi", "th")))

                                        if(str(file_location) != 'time'):
                                            Kinetic_Histo_3D[Kinetic_Histo_3D_Name].Write()

                                            if("Phi" in list1[0] and option == "delta_matched"):
                                                Kinetic_Histo_3D["".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"])].Write()

                                        # 3D->1D Histogram is saved
                                        count_of_histograms += 1
                                        if("Phi" in list1[0] and option == "delta_matched"):
                                            count_of_histograms += 1

                                        if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))

                                    ###############################################     1D Histograms     ###############################################
                                    #####################################################################################################################
                                    ###############################################     2D Histograms     ###############################################
                                    if((option == "normal" or option == "has_matched") and datatype_2 != "gen"):
                                        for list2 in Variable_Loop_2D:
                                            for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                                if(Q2_xB_Bin_Num > 8 and "2" in smearing_Q):
                                                    continue
                                                    # 2nd definition of the Q2-xB bins do not go above bin 8

                                                cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "Cut")
                                                Histo_Title = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "Title")                                            

                                                if(cutname == "continue" or Histo_Title == "continue"):
                                                    continue
                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 2D Histogram - ', str(cutname)]), datatype_2, sec_type, sec_num, Q2_xB_Bin_Num, str(list2[0][0]), str(list2[1][0]))
                                                if("2" in smearing_Q):
                                                    Kinetic_Histo_3D_Name = (''.join(['3D -> 2D Histogram - New 2D Binning - ', str(cutname)]), datatype_2, sec_type, sec_num, Q2_xB_Bin_Num, str(list2[0][0]), str(list2[1][0]))

                                                Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "DF").Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), 54, -3, 50, list2[0][3], list2[0][1], list2[0][2], list2[1][3], list2[1][1], list2[1][2]), str(z_pT_Bin_Filter_str), str(list2[0][0]), str(list2[1][0]))

                                                if(str(file_location) != 'time'):
                                                    Kinetic_Histo_3D[Kinetic_Histo_3D_Name].Write()
                                                # 3D->2D Histogram is saved
                                                count_of_histograms += 1
                                                if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                                    print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                                if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                                    print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))

                                    ###############################################     2D Histograms     ###############################################
                                    #####################################################################################################################

                                    ##=====##    Variable Loops    ##=====##
                                    ##====================================##
                                    
                                elif(option == "bin_2D_purity"):
                                    cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "Cut")
                                    
                                    if("continue" in cutname or "continue" in str(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "2D_Purity", smearing_Q, "mdf", cut_choice, "Cut"))):
                                        continue
                                        
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                        if((Q2_xB_Bin_Num < 1) or (Q2_xB_Bin_Num > 8 and "2" in smearing_Q)):
                                            continue
                                            # Q2_xB_Bin_Num < 1 will either give 0 purity (no z-pT bins defined) or can be seen in the "counts" option below
                                            # Also, 2nd definition of the Q2-xB bins do not go above bin 8
                                            
                                        Purity_2D_Histo_Name = (''.join(['2D Purity - ', str(cutname)]), datatype_2, smearing_Q, sec_type, sec_num, Q2_xB_Bin_Num)
                                        if("2" in smearing_Q):
                                            Purity_2D_Histo_Name = (''.join(['2D Purity - New 2D Binning - ', str(cutname)]), datatype_2, smearing_Q, sec_type, sec_num, Q2_xB_Bin_Num)

                                        Histo_Title = "".join(["#splitline{Number of Pure Events for ", variable_Title_name(Q2_xB_Bin_Filter_str), "}{Cuts in use: ", cutname if (cutname != "" and cutname != " ") else "No Cuts", "}"])

                                        histo_for_2D_Purity[str(Purity_2D_Histo_Name)] = ROOT.TH1D(str(Purity_2D_Histo_Name), str(Histo_Title), 1, 0, 1)
                                        
                                        if("continue" in str(DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF"))):
                                            continue
                                        
                                        try:
                                            if(str(file_location) != 'time'):
                                                histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Total) ", variable_Title_name(Q2_xB_Bin_Filter_str), " = ", str(Q2_xB_Bin_Num)]), DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF").Count().GetValue())
                                                
                                                # try:
                                                #     histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Total) ", variable_Title_name(Q2_xB_Bin_Filter_str), " = ", str(Q2_xB_Bin_Num)]), DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF").Count().GetValue())
                                                # except:
                                                #     print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))
                                                
                                                for z_pT_Bin_Num in range(1, 49, 1):
                                                    histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Total) ", variable_Title_name(z_pT_Bin_Filter_str), " = ", str(z_pT_Bin_Num)]), DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, z_pT_Bin_Num, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF").Count().GetValue())
                                                    
                                                    # try:
                                                    #     histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Total) ", variable_Title_name(z_pT_Bin_Filter_str), " = ", str(z_pT_Bin_Num)]), DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, z_pT_Bin_Num, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF").Count().GetValue())
                                                    # except:
                                                    #     print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))

                                                histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Pure) ", variable_Title_name(Q2_xB_Bin_Filter_str), " = ", str(Q2_xB_Bin_Num)]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF"), Q2_xB_Bin_Filter_str, 0, 0, 20).Count().GetValue())
                                                
                                                # try:
                                                #     histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Pure) ", variable_Title_name(Q2_xB_Bin_Filter_str), " = ", str(Q2_xB_Bin_Num)]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF"), Q2_xB_Bin_Filter_str, 0, 0, 20).Count().GetValue())
                                                # except:
                                                #     print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))
                                                
                                                for z_pT_Bin_Num in range(1, 49, 1):
                                                    histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Pure) ", variable_Title_name(z_pT_Bin_Filter_str), " = ", str(z_pT_Bin_Num)]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, z_pT_Bin_Num, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF"), z_pT_Bin_Filter_str, 0, 0, 20).Count().GetValue())
                                                    
                                                    # try:
                                                    #     histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Fill("".join(["(Pure) ", variable_Title_name(z_pT_Bin_Filter_str), " = ", str(z_pT_Bin_Num)]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, z_pT_Bin_Num, "2D_Purity", smearing_Q, datatype_2, cut_choice, "DF"), z_pT_Bin_Filter_str, 0, 0, 20).Count().GetValue())
                                                    # except:
                                                    #     print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))

                                                histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Write()
                                                
                                                # try:
                                                #     histo_for_2D_Purity[str(Purity_2D_Histo_Name)].Write()
                                                # except:
                                                #     print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))

                                            # 2D Purity Histogram has been saved
                                            count_of_histograms += 1
                                            if((str(file_location) != 'time') and (count_of_histograms%400 == 0)):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                            if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        except:
                                            print("".join(["\nError with: histo_for_2D_Purity[str(", str(Purity_2D_Histo_Name), ")]\n"]))
                                            
                            
                                elif(option == "counts"):
                                    cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "Counts", smearing_Q, datatype_2, cut_choice, "Cut")

                                    if("continue" in cutname or "continue" in str(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "Cut"))):
                                        continue    
                                    
                                    histo_for_counts[str((cutname, smearing_Q))] = ROOT.TH1D("".join(["Histogram_for_event_counts", "" if smearing_Q == "" else "_", smearing_Q, " ", cutname]), "".join(["" if smearing_Q != "smear" else "(Smeared) ", "Event Counts for: ", cutname]), 1, 0, 1)

                                    if(str(file_location) != 'time'):
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("All REC Events", rdf.Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("All (Completely) MATCHED REC Events", rdf.Filter("PID_el != 0 && PID_pip != 0").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("All (Electron) MATCHED REC Events", rdf.Filter("PID_el != 0").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("All (Pi+) MATCHED REC Events", rdf.Filter("PID_pip != 0").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Correct Electron MATCHED REC Events", rdf.Filter("PID_el == 11").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Correct Pi+ MATCHED REC Events", rdf.Filter("PID_pip == 211").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Perfectly MATCHED REC Events", rdf.Filter("PID_el == 11 && PID_pip == 211").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Mis-Identified Matches of REC Events (Total)", rdf.Filter("PID_el != 11 && PID_el != 0 && PID_pip != 211 && PID_pip != 0").Count().GetValue()) 
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Mis-Identified (Electron) Matches of REC Events", rdf.Filter("PID_el != 11 && PID_el != 0").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("Mis-Identified (Pi+) Matches of REC Events", rdf.Filter("PID_pip != 211 && PID_pip != 0").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("All REC Events (After Cuts)", DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MATCHED REC Events (After Cuts)", DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "Counts", smearing_Q, datatype_2, cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MATCHED (Electron) REC Events (After Cuts)", DF_Filter_Function_Full(rdf.Filter("PID_el != 0"), sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MATCHED (Pi+ Pion) REC Events (After Cuts)", DF_Filter_Function_Full(rdf.Filter("PID_pip != 0"), sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MIS-MATCHED REC Events (After Cuts)", DF_Filter_Function_Full(rdf.Filter("PID_el != 11 && PID_el != 0 && PID_pip != 211 && PID_pip != 0"), sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MIS-MATCHED (Electron) REC Events (After Cuts)", DF_Filter_Function_Full(rdf.Filter("PID_el != 11 && PID_el != 0"), sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("MIS-MATCHED (Pi+ Pion) REC Events (After Cuts)", DF_Filter_Function_Full(rdf.Filter("PID_pip != 211 && PID_pip != 0"), sec_type, sec_num, -1, -2, "Counts", smearing_Q, "mdf", cut_choice, "DF").Count().GetValue())

                                        for list1 in Variable_Loop:
                                            histo_for_counts[str((cutname, smearing_Q))].Fill("".join(["Purity of ", variable_Title_name(list1[0])]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF"), list1[0], list1[1], list1[2], list1[3]).Count().GetValue())
                                            
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("".join(["Purity of ", variable_Title_name("".join(["Q2_xB_Bin", "" if smearing_Q != "smear" else "_smeared"]))]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "".join(["Q2_xB_Bin", "" if smearing_Q != "smear" else "_smeared"]), smearing_Q, datatype_2, cut_choice, "DF"), "".join(["Q2_xB_Bin", "" if smearing_Q != "smear" else "_smeared"]), 0, 1, 1).Count().GetValue())
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("".join(["Purity of ", variable_Title_name("".join(["z_pT_Bin", "" if smearing_Q != "smear" else "_smeared"]))]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "".join(["z_pT_Bin", "" if smearing_Q != "smear" else "_smeared"]), smearing_Q, datatype_2, cut_choice, "DF"), "".join(["z_pT_Bin", "" if smearing_Q != "smear" else "_smeared"]), 0, 1, 1).Count().GetValue())
                                        
                                        histo_for_counts[str((cutname, smearing_Q))].Fill("".join(["Purity of ", variable_Title_name("".join(["Q2_xB_Bin_2", "" if smearing_Q != "smear" else "_smeared"]))]), bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "".join(["Q2_xB_Bin_2", "" if smearing_Q != "smear" else "_smeared"]), smearing_Q, datatype_2, cut_choice, "DF"), "".join(["Q2_xB_Bin_2", "" if smearing_Q != "smear" else "_smeared"]), 0, 1, 1).Count().GetValue())


                                        histo_for_counts[str((cutname, smearing_Q))].Write()
                                        
                                        
                                    # Event Count Histogram has been saved
                                    count_of_histograms += 1
                                    if((str(file_location) != 'time') and (count_of_histograms%400 == 0)):
                                        print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                    if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                        print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        
                                        
                                elif(option == "bin_migration"):
                                    
                                    for list1 in Variable_Loop:
                                        # bin_purity_save_fuction
                                    
                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                        
                                        if("continue" in cutname):
                                            continue
                                            
                                        sdf = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF")
  
                                        BIN_SIZE = (list1[2] - list1[1])/list1[3]
                                            
                                        for REC_Bin in range(0, list1[3] + 1, 1):
                                            
                                            Bin_Range = "".join([str(round(BIN_SIZE*(REC_Bin - 1), 3)), " -> ", str(round(BIN_SIZE*REC_Bin, 3))])
                                            
                                            Migration_Title = "".join(["#splitline{#splitline{Bin Migration of ", variable_Title_name(list1[0]), "}{Cut: ", str(cutname), "}}{#scale[1.5]{REC BIN: ", str(REC_Bin), " - Range: ", Bin_Range, "}}; ", variable_Title_name(list1[0]), " GEN Bin; Counts"])
                                            
                                            Migration_Histo_REF = ("Bin Migration", list1[0], "".join(["REC_Bin_", str(REC_Bin)]), smearing_Q, cut_choice, sec_type, sec_num)
                                    
                                            histo_for_migration[Migration_Histo_REF] = bin_purity_save_filter_fuction(sdf, str(list1[0]), list1[1], list1[2], list1[3], REC_Bin).Histo1D((str(Migration_Histo_REF), str(Migration_Title), list1[3] + 3, -1, list1[3] + 1), "".join([str(list1[0]), "_GEN_BIN"]))
                                        
                                            if(str(file_location) != 'time'):
                                                histo_for_migration[Migration_Histo_REF].Write()
                                                
                                            count_of_histograms += 1
                                            
                                            if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                            if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        
                                elif(option == "bin_migration_V2"):
                                    
                                    for Var_List in Variable_Loop:

                                        variable = Var_List[0].replace("_gen", "")
                                        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
                                            
                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, datatype_2, cut_choice, "Cut")
                                        
                                        if("continue" in cutname):
                                            continue
                                            
  
                                        BIN_SIZE = (Var_List[2] - Var_List[1])/Var_List[3]
                                        Bin_Range = "".join([str(round((Var_List[1]), 3)), " -> ", str(round(Var_List[2], 3))])

                                        Migration_Title = "".join(["#splitline{#splitline{Bin Migration of ", variable_Title_name(variable), "}{Cut: ", str(cutname), "}}{#scale[1.5]{Number of Bins: ", str(Var_List[3]), " - Range: ", str(Bin_Range), ", - Size: ", str(BIN_SIZE), " per bin}}; ", variable_Title_name(variable), "; ", variable_Title_name(gen_variable)])

                                        Migration_Histo_REF = ("Bin Migration V2", variable, smearing_Q, cut_choice, sec_type, sec_num)

                                        histo_for_migration[Migration_Histo_REF] = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, datatype_2, cut_choice, "DF").Histo2D((str(Migration_Histo_REF), str(Migration_Title), Var_List[3], Var_List[1], Var_List[2], Var_List[3], Var_List[1], Var_List[2]), str(variable), str(gen_variable))

                                        if(str(file_location) != 'time'):
                                            histo_for_migration[Migration_Histo_REF].Write()

                                        count_of_histograms += 1

                                        if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                    
                                    
                                elif(option == "bin_migration_V3"):
                                    
                                    for Var_List in Variable_Loop:
                                        
                                        variable = Var_List[0]

                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "Cut")
                                        
                                        if("continue" in cutname):
                                            continue

                                            
  
                                        BIN_SIZE = round((Var_List[2] - Var_List[1])/Var_List[3], 5)
                                        Bin_Range = "".join([str(round((Var_List[1]), 3)), " -> ", str(round(Var_List[2], 3))])

                                        Migration_Title = "".join(["#splitline{#splitline{#splitline{Bin Migration of ", variable_Title_name(variable), "}{Cut: ", str(cutname), "}}{#scale[1.5]{Number of Bins: ", str(Var_List[3]), " - Range: ", str(Bin_Range), ", - Size: ", str(BIN_SIZE), " per bin}}}{Same Binning Scheme as Other (Standard) Histograms}; ", variable_Title_name(variable), " (GEN) Bins; ", variable_Title_name(variable), " (REC) Bins"])

                                        Migration_Histo_REF = ("Bin Migration V3", variable, smearing_Q, cut_choice, sec_type, sec_num)
                                        
                                        sdf = bin_purity_save_fuction_New(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "DF"), variable, Var_List[1], Var_List[2], Var_List[3])
                        
                                        # num_of_REC_bins, min_REC_bin, Max_REC_bin = Var_List[3], 0, Var_List[3]
                                        # num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Var_List[3] + 3), -1, (Var_List[3] + 2)
                                    
                                        num_of_REC_bins, min_REC_bin, Max_REC_bin = (Var_List[3] + 3), -0.5, (Var_List[3] + 2.5)
                                        num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Var_List[3] + 4), -0.5, (Var_List[3] + 3.5)

                                        histo_for_migration[Migration_Histo_REF] = sdf.Histo2D((str(Migration_Histo_REF), str(Migration_Title), num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin), str("".join([str(variable), "_GEN_BIN"])), str("".join([str(variable), "_REC_BIN"])))

                                        if(str(file_location) != 'time'):
                                            histo_for_migration[Migration_Histo_REF].Write()

                                        count_of_histograms += 1

                                        if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                        if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                            print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                           
                                        
                                        
                                        
                                elif(option == "bin_migration_V4"):
                                    
                                    for bin_option in [2, 3, 4, 5, 10, 20, 40]:
                                        
                                        for Var_List in Variable_Loop:

                                            variable = Var_List[0]

                                            cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "Cut")

                                            if("continue" in cutname):
                                                continue

                                            if("Q2" in variable):
                                                Min_range, Max_range = 2, 11.351
                                            if("xB" in variable):
                                                Min_range, Max_range = 0.126602, 0.7896
                                            if("z" in variable):
                                                Min_range, Max_range = 0.15, 0.7
                                            if("pT" in variable):
                                                Min_range, Max_range = 0.05, 1.0
                                            if("y" in variable):
                                                Min_range, Max_range = 0.24, 0.75
                                            if("phi_t" in variable):
                                                Min_range, Max_range = 0, 360
                                            
                                            BIN_SIZE = round((Max_range - Min_range)/bin_option, 5)
                                            Bin_Range = "".join([str(Min_range), " -> ", str(Max_range)])

                                            Migration_Title = "".join(["#splitline{#splitline{Bin Migration of ", variable_Title_name(variable), "}{Cut: ", str(cutname), "}}{#scale[1.5]{Number of Bins: ", str(bin_option), " - Range: ", str(Bin_Range), ", - Size: ", str(BIN_SIZE), " per bin}}; ", variable_Title_name(variable), " (GEN) Bins; ", variable_Title_name(variable), " (REC) Bins"])

                                            Migration_Histo_REF = ("Bin Migration V4", variable, smearing_Q, cut_choice, sec_type, sec_num, bin_option)

                                            sdf = bin_purity_save_fuction_New(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "DF"), variable, Min_range, Max_range, bin_option)
                                            
                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = (bin_option + 3), -0.5, (bin_option + 2.5)
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (bin_option + 4), -0.5, (bin_option + 3.5)

                                            histo_for_migration[Migration_Histo_REF] = sdf.Histo2D((str(Migration_Histo_REF), str(Migration_Title), num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin), str("".join([str(variable), "_GEN_BIN"])), str("".join([str(variable), "_REC_BIN"])))

                                            if(str(file_location) != 'time'):
                                                histo_for_migration[Migration_Histo_REF].Write()

                                            count_of_histograms += 1

                                            if((count_of_histograms%400 == 0) and (str(file_location) != 'time')):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                            if((str(file_location) == 'time') and (count_of_histograms%100 == 0)):
                                                print("".join([str(count_of_histograms), " Histograms Have Been Made..."]))
                                            
                                            
                                            
                                        


        ######################################################################
        ##=====##=====##=====##    End of Main Loop    ##=====##=====##=====##
        ######################################################################



        ######################################===============================######################################
        ##==========##==========##==========##          End of Code          ##==========##==========##==========##
        ######################################===============================######################################

        if(str(file_location) != 'time'):
            ROOT_File_Output.Close()
        # File has been saved

        print("".join(["Total Number of Histograms Made: ", str(count_of_histograms)]))
        
        
    elif(output_type != "histo" and output_type != "test" and output_type != 'time'):
#         ROOT_File_Output_Name = "".join(["DataFrame_", ROOT_File_Output_Name])
        print("Taking Snapshot...")
        rdf.Snapshot("h22", ROOT_File_Output_Name)
        print("Done\n\n")
    
    # Getting current date
    datetime_object_end = datetime.now()

    endMin_full, endHr_full, endDay_full = datetime_object_end.minute, datetime_object_end.hour, datetime_object_end.day

    if(datetime_object_end.minute < 10):
        timeMin_end = ''.join(['0', str(datetime_object_end.minute)])
    else:
        timeMin_end = str(datetime_object_end.minute)
    
    # Printing current time
    if(datetime_object_end.hour > 12 and datetime_object_end.hour < 24):
        print("".join(["The time that this code finished is ", str((datetime_object_end.hour) - 12), ":", timeMin_end, " p.m."]))
    if(datetime_object_end.hour < 12 and datetime_object_end.hour > 0):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", timeMin_end, " a.m."]))
    if(datetime_object_end.hour == 12):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", timeMin_end, " p.m."]))
    if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
        print("".join(["The time that this code finished is 12:", timeMin_end, " a.m."]))
        
        
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
    

    
    
    print("\n")
    
    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
    
else:
    print("\nERROR: No valid datatype selected...\n")
    
# This Code was last updated on 7-18-2022