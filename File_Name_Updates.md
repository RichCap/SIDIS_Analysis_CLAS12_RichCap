# Update Notes by File
The notes in this file contain information about individual file updates made with the python code called "makeROOT_epip_SIDIS_histos_new.py".
These notes are made inside the python code whenever a new set of histograms are made (see where the 'Extra_Name' string is defined to see the most recent notes).
This file will break down individual git updates into the different files that were made between commits, since mutliple files may sometimes be made before they are all commited.
See the README.md file for more general updates (especially those which pertain to things outside of the updates to the python code)




# Notes Commited on 4-21-2023:

## Extra_Name = "Multi_Dimension_Unfold_V5_"
* Just ran the SIDIS Histograms (no momentum correction histograms)
* Updated the kinematic binning with the following updates:
    * 1) Now using the condensed code (with TH2Poly) for all binning schemes (most of the old code has been removed or otherwise commented out)
    * 2) New 'Square' bins (i.e. Binning option '3') now has 14 Q2-xB bins total (extra bins were added to this scheme since the last committed version used in 'Multi_Dimension_Unfold_V4_')
        * Still no z-pT bins for these yet
    * 3) Will be running with both bin option '2' and '3'
* New Multidimensional binning function was written to combine variables (running the same options but the code should be an improvement - still in testing)
    * All overflow bin events are given the value of -1
* Removed a lot of unnecessary code from this script (general clean up) including pre-defined Multidimensional bins (like Bin_4D)
* Reduced the number of bins in some 2D histograms such as the particle momentums and Q2-xB distributions (should have little effect on the plots outside of some minor visual changes)
    * Done to avoid memory overload as the code was crashing even when I wasn't trying to create the root files.


# Notes Committed on 4-16-2023:

## Extra_Name = "Unfolding_Tests_V9_"
* New (Modified) Smearing Functions (Particle-dependant)
    * Modified the momentum smearing (As a function of theta/momentum - not both - choose to smear based on which variable provided the easiest fit to get the smearing factor)
    * New Theta smearing as a function of momentum


## Extra_Name = "Unfolding_Tests_V10_"
* New (Modified) Smearing Functions (Particle-dependant)
* Reduced number of plots made (for faster runtime)

## Extra_Name = "Unfolding_Tests_V11_"
* New (Modified) Smearing Functions (Particle-dependant)
* Increased number of plots made (relative to last version)


## Extra_Name = "Unfolding_Tests_V12_"
* Extended the 2D plots and added more to show the phase space of the data
* Modified the Pi+ Theta smearing function (as function of momentum)


## Extra_Name = "Unfolding_Tests_V13_"
* Running fewer 1D histograms (just phi_t)
* Added new multidimensional response matrix option which combines multiple variables into a new linearized bin definition
* Modified the Pi+ Theta smearing function (as function of momentum) and the Electron Momentum smearing function (as a function of theta)


## Extra_Name = "Unfolding_Tests_V14_"
* Modified the Pi+ Theta smearing function (as function of momentum) 
    * Testing to see if it is better to smear only one variable at a time (other variables could be improved at this moment, but only changing one aspect of the smearing function in this iteration)
* Attempting to fix the issue with the multidimension variable creation function
    * Flipped the order of the Res_Var_Add variable list
* Removed the Combined z-pT-phi_h variable from test (switched with the Q2-xB bin variable as an already defined multidimensional variable that can be unfolded as is)
    * The removed option has to many bins for efficient testing at this stage
* Changed the phase space histograms (in 'Mom_Cor_Code') to include the particle momentum instead of the sector information
    * May be redundant with other histograms (in 'Normal_2D') which should be removed in the future (must make the other scripts compatible with these histograms before removing the 'Normal_2D' options)
* Modified Dimension_Name_Function() to remove all ";"s from the outputs
* Removed notification of "Skipping Normal 1D Histograms..." (now just assumed)


## Extra_Name = "Analysis_Note_Update_"
* Added response matrices for the variables already shown in the analysis note (for update)
* Removed smearing histograms, exclusive cuts, and combined variables (not needed here)


## Extra_Name = "Analysis_Note_Update_V2_"
* Extended the z-pT bin axis for the response matrices (caused errors in the plots without kinematic binning)
* Switched the kinematic variables (other than phi_h) to use the same binning scheme as was used at the last DNP meeting (just for the response matrix/1D plots)


## Extra_Name = "Analysis_Note_Update_V3_"
* Resetted the z-pT bin axis for the response matrices (was not necessary before)
* Fixed the issue with replicating old plots (issue was caused by a cut that prevented bin migration between the kinematic Q2-xB-z-pT bins which is only useful in the phi_t plots)
* Using FX's smearing function


## Extra_Name = "Analysis_Note_Update_V4_"
* Using my smearing function and momentum corrections


## Extra_Name = "New_Smearing_Creation_"
* Only running Mom_Cor_Code plots
* Starting new smearing functions from FX's version
* Running with all versions of the cuts


## Extra_Name = "New_Smearing_Creation_V1_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing as function of momentum


## Extra_Name = "New_Smearing_Creation_V2_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing (again) as function of momentum


## Extra_Name = "New_Smearing_Creation_V3_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing as function of theta


## Extra_Name = "New_Smearing_Creation_V4_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing (again) as function of theta


## Extra_Name = "New_Smearing_Creation_V5_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing as function of momentum


## Extra_Name = "New_Smearing_Creation_V6_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing (again) as function of momentum


## Extra_Name = "New_Smearing_Creation_V7_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing as function of theta


## Extra_Name = "New_Smearing_Creation_V8_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing (again) as function of theta


## Extra_Name = "Analysis_Note_Update_V5_"
* Using my (new) smearing function


## Extra_Name = "Analysis_Note_Update_V6_"
* Using my (new) smearing function (only smearing)


# End of Notes Committed on 4-16-2023



---

## Notes from before 4-16-2023
These notes were moved to this file on '''April 16, 2023'''. They were previously organized in the README.md file of this repository. Everything below this line is from that other markdown file before April, 2023.


These note correspond to updates made between the outputs of the python code. When the output of the python code changes, the updates will be noted here with the name of the file produced. Sorted from OLDEST to NEWEST.

### Extra_Name = "Unfolding_Tests_V1_"
* Groovy Code moved to work directory (safer than keeping these files on the volatile directory)
* Filtered unmatched events from the "normal" 2D Response Matrices (necessary for proper matrix construction when not using pre-defined bin numbers)
* Made the Correction (∆P) plots use the UNSMEARED particle kinematics on the x-axis (this will allow the new smearing functions to be developed as a function of the unsmeared kinematics - this will be the simplest way to create these corrections)
* Turned off momentum corrections (new ones are in development and will be applied soon)

### Extra_Name = "Unfolding_Tests_V2_"
* Major rework and new momentum corrections (not being run at this time)
* Will plot Response Matrices in separate Q2-xB bins


### Extra_Name = "Unfolding_Tests_V3_"
* Same as V2 but needed to change the naming convensions again to remove ";" and ":" (replaced with ")," and "=" instead)
    * Binning now grouped with "[]" instead of "()"

### Extra_Name = "Unfolding_Tests_V4_"
* Replaced (some of) the sector information in the 'Mom_Cor_Code' histograms with theta bins (4˚ per bin)
* Fixed some issues with the Q2-xB bins being skipped (response matrices and 'Normal' histograms)
* Skipping 'Normal_1D' histogram options (unnecessary when running the response matrix code)
* Fixed some binning options (too many bins with the multidimensional bin variables and rounded the 1D variable boundries to have less digits)


### Extra_Name = "Unfolding_Tests_V5_"
* Deleted unused functions including:
    * "bin_purity_save_fuction"
    * "bin_purity_save_filter_fuction"
* Replaced (name of) "bin_purity_save_fuction_New" with "Bin_Number_Variable_Function"
    * Works the same, but the name is more meaningful (and updated) now
* Replaced (name of) "bin_purity_filter_fuction" with "Bin_Purity_Filter_Fuction"
    * Same function, just with a very minor change of name to be easier to read in code
* Made new function called: "Multi_Dimensional_Bin_Construction"
    * Will combine any list of variables into a linearized 1D binning scheme
    * Plan to test in "MC_DataFrame_Volume_Calculation.ipynb" (?) --> Not tested yet (as of this update)
* Using all Q2-xB bin options (-1 to 8)
* Added additional dimension to the "Response_Matrix" histogram options (now includes a dimension for z-pT bins)
* Made the "Normal_2D" histograms use the same number of bins as all of the 1D histograms used (same as the Response_Matrix options)
    
    
### Extra_Name = "Unfolding_Tests_V6_"
* Y-axis in Response Matrices needed to be renamed from "Count" to "z-P_{T} Bins" (due to the additional dimension added to these histograms)
* (Temporarily) Reduced number of histograms being made:
    * Stopped running Mom_Cor_Code
    * Fewer Variables being plotted (only the 2D histograms for binning, and the 1D/unfolded phi_t/Q2 histograms are being run)
    * Removed EDIS cuts from list
    * Only running 'Response_Matrix_Normal' option (for now)
        * Removed 'Response_Matrix' to reduce run-time
* Added 'gen' to 'mdf' run options (only plots the Normal_2D histograms)
* Added run-time estimate to end of code (does not affect the files produced)


### Extra_Name = "Unfolding_Tests_V7_"
* Changed the number of phi_t bins (now 15˚ per bin instead of 10˚ per bin)
* Added the following histograms back:
    * Running Mom_Cor_Code again (with momentum corrections)
    * More Variables being plotted 
        * Same number of 2D histograms as in V6 but now the electron and pion kinematics are also being run (in addition to the 1D/unfolded phi_t/Q2 histograms that were already in V6)
    * Added EDIS cuts back
    * Still removed 'Response_Matrix' to reduce run-time (only running 'Response_Matrix_Normal')
* Ran for all data sets (V6 was only done for 'mdf')


### Extra_Name = "Unfolding_Tests_V8_"
* New (Modified) Smearing Functions (Particle-dependant)
    * Smeared the momentum as a function of theta


### Extra_Name = "Unfolding_Tests_V9_"
* New (Modified) Smearing Functions (Particle-dependant)
    * Modified the momentum smearing (As a function of theta/momentum - not both - choose to smear based on which variable provided the easiest fit to get the smearing factor)
    * New Theta smearing as a function of momentum


### Extra_Name = "Unfolding_Tests_V10_"
* New (Modified) Smearing Functions (Particle-dependant)
* Reduced number of plots made (for faster runtime)


### Extra_Name = "Unfolding_Tests_V11_"
* New (Modified) Smearing Functions (Particle-dependant)
* Increased number of plots made (relative to last version)


### Extra_Name = "Unfolding_Tests_V12_"
* Extended the 2D plots and added more to show the phase space of the data
* Modified the Pi+ Theta smearing function (as function of momentum)


### Extra_Name = "Unfolding_Tests_V13_"
* Running fewer 1D histograms (just phi_t)
* Added new multidimensional response matrix option which combines multiple variables into a new linearized bin definition
* Modified the Pi+ Theta smearing function (as function of momentum) and the Electron Momentum smearing function (as a function of theta)

    
### Extra_Name = "Unfolding_Tests_V14_"
* Modified the Pi+ Theta smearing function (as function of momentum) 
    * Testing to see if it is better to smear only one variable at a time (other variables could be improved at this moment, but only changing one aspect of the smearing function in this iteration)
* Attempting to fix the issue with the multidimension variable creation function
    * Flipped the order of the Res_Var_Add variable list
* Removed the Combined z-pT-phi_h variable from test (switched with the Q2-xB bin variable as an already defined multidimensional variable that can be unfolded as is)
    * The removed option has to many bins for efficient testing at this stage
* Changed the phase space histograms (in 'Mom_Cor_Code') to include the particle momentum instead of the sector information
    * May be redundant with other histograms (in 'Normal_2D') which should be removed in the future (must make the other scripts compatible with these histograms before removing the 'Normal_2D' options)
* Modified Dimension_Name_Function() to remove all ";"s from the outputs
* Removed notification of "Skipping Normal 1D Histograms..." (now just assumed)


### Extra_Name = "Analysis_Note_Update_"
* Added response matrices for the variables already shown in the analysis note (for update)
* Removed smearing histograms, exclusive cuts, and combined variables (not needed here)


### Extra_Name = "Analysis_Note_Update_V2_"
* Extended the z-pT bin axis for the response matrices (caused errors in the plots without kinematic binning)
* Switched the kinematic variables (other than phi_h) to use the same binning scheme as was used at the last DNP meeting (just for the response matrix/1D plots)


### Extra_Name = "Analysis_Note_Update_V3_"
* Resetted the z-pT bin axis for the response matrices (was not necessary before)
* Fixed the issue with replicating old plots (issue was caused by a cut that prevented bin migration between the kinematic Q2-xB-z-pT bins which is only useful in the phi_t plots)
* Using FX's smearing function


### Extra_Name = "Analysis_Note_Update_V4_"
* Using my smearing function and momentum corrections


### Extra_Name = "New_Smearing_Creation_"
* Only running Mom_Cor_Code plots
* Starting new smearing functions from FX's version
* Running with all versions of the cuts


### Extra_Name = "New_Smearing_Creation_V1_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing as function of momentum


### Extra_Name = "New_Smearing_Creation_V2_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing (again) as function of momentum


### Extra_Name = "New_Smearing_Creation_V3_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing as function of theta


### Extra_Name = "New_Smearing_Creation_V4_"
* Only running Mom_Cor_Code plots
* Modified Electron Smearing (again) as function of theta


### Extra_Name = "New_Smearing_Creation_V5_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing as function of momentum


### Extra_Name = "New_Smearing_Creation_V6_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing (again) as function of momentum


### Extra_Name = "New_Smearing_Creation_V7_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing as function of theta


### Extra_Name = "New_Smearing_Creation_V8_"
* Only running Mom_Cor_Code plots
* Modified Pi+ Pion Smearing (again) as function of theta


### Extra_Name = "Analysis_Note_Update_V5_"
* Using my (new) smearing function


### Extra_Name = "Analysis_Note_Update_V6_"
* Using my (new) smearing function (only smearing)


### Extra_Name = "Analysis_Note_Update_VF_APS_"
* Final version of histograms as used in the analysis note for the April APS meetings (released 2/22/2023)


### Extra_Name = "Multi_Dimension_Unfold_V1_"
* ∆P now uses the generated kinematics for comparison instead of the calculated ones for the matched monte carlo files
* Made a general update to some lines of code to 'clean up' their appearance (does not affect how code is run)
* Testing first multidmimensional binning using just Q2 and phi_h


### Extra_Name = "Multi_Dimension_Unfold_V2_"
* Turned off ∆P plots for now (use the version above)
* Testing second multidmimensional binning using Q2_xB_Bins with phi_h
    * Use the prior version for all other plots
    * These plots will be cut as to ignore bin migration in the z-pT bins


### Extra_Name = "Multi_Dimension_Unfold_V3_"
* ∆P plots are still off
* Fixed the multidmimensional binning (had overlapping bins and missed the last bin that was not phi)
    * Running both the Q2_phi and Q2_xB_phi plots
* Added cut to Q2-xB bin 0 in Multidimensional unfolding


---



## Older File Updates (by name):
These updates were removed from the python code and were moved down here as opposed to the more recent updates decribed in the 'File Updates (by name)' section. These updates have been re-ordered so that the more recent notes come first

### Extra_Name = "DNP_V3_"
* Made more 2D histograms to show kinematic cuts

### Extra_Name = "DNP_V2_"
* Turned on Momentum Corrections and new smearing functions

### Extra_Name = "DNP_"
* Turned off Momentum Corrections and new smearing functions
* Only making response matrices

### Extra_Name = "Mom_Cor_Response_Matrix_V5_"
* Modified FX's smearing function for momentum (pol2 function of electron momentum)
* Changed datatype names so that the Matched MC REC data now runs with mdf
    * pdf is no specifically used for selecting ONLY matched events
    * mdf does not run the option for gen histograms (i.e., matched generated events) --> pdf option still runs these options
* Added additional histograms for correction/smearing functions
* Removed unnecessary options including:
    1) option = bin_2D_purity
    2) option = counts
    3) option = bin_migration_V2
    4) option = bin_migration_V4
* Added option to run regular 2D histograms separately from regular 1D histograms (options "normal_1D" and "normal_2D")
* Correction/Smearing Histograms (i.e., option == "Mom_Cor_Code") now requires either fully exclusive events or full SIDIS cuts (requirment for cuts)
    * Calculations are designed only for exclusive reactions, but SIDIS reactions are allowed here for comparison purposes
* Removed cut option: cut_Complete
    * This option is missing final cuts to make the event selection either exclusive or propperly semi-inclusive. Not worth running at this time
* Added phi_t Binning to response matrices

### Extra_Name = "Mom_Cor_Response_Matrix_V4_"
* Testing new smearing functions (failed to update properly)

### Extra_Name = "Mom_Cor_Response_Matrix_V3_"
* Needed the Matrices to be square for unfolding
* Also changed :
    * The reconstructed MC files do not produce 1D histograms anymore (only produce the ∆P histograms and the 2D Response Matrices)
    * The ∆P histograms will now note (in the title) whether or not the momentums were being corrected when run (only affects the experimental files)
    
### Extra_Name = "Mom_Cor_Response_Matrix_V2_"
* Removed everything except the the "Response Matrix" and "Momentum Correction" histograms from 'Mom_Cor_Response_Matrix_V2'





---


## Older Updates:
All of the following updates were written in the Python code directly before this Github was created...


### On 7-18-2022:
     1) Moved File Locations (new folders and data file)
     2) New File name
     3) Updates to be given on GitHub now

### On 6-7-2022:
     1) Histograms 20 Bin option
     2) Fixed Bin Migration Histograms
        * phi_t not (pre)defined properly for V4
        * Overflow bins set to 0 and bin_option + 1 (unmatched bin is bin_option + 2)
        * One extra bin is given above the unmatched bin so that an empty bin can make room for the z-axis scale
        * Axis is shifted so that the center of each bin is located at the bin's number (easier to read)
     3) Name is now: V25_20_Bin_Test

### On 6-6-2022:
     1) Histograms 20 Bin option
     2) New Bin Migration Histograms added
        * Runs all bin options at once (bins = 2, 3, 4, 5, 10, 20, and 40)
        * Kinematic ranges are pre-defined for each variable (using max ranges of the 2D binning scheme previously developed)
        * Binning is extended slightly beyond the overflow + unmatched binning ranges for 2 reasons, namely:
                    1) Avoid possible issues with getting the bin numbers wrong
                    2) If the above note is a non-issue, then to simply give more room in the histograms' borders
     3) Name is now: V24_20_Bin_Test

### On 6-3-2022:
     1) Using 20 Bin option (rerunning with fixes)
     2) Fixed issues with the bin migration histograms
        * Added information of events outside the given kinematic binning for REC events (previously only applied to GEN events)
        * Fixed issue with some histograms being saved over
        * Flipped the x and y axis (visual change)
     5) Name is now: V23_20_Bin_Test

### On 6-2-2022:
     1) Using 20 Bin option (rerunning with new options)
     2) Updated Binning for Q2 and xB (other variables remain the same)
     3) Running "gen" variable option
     4) Added new set of bin migration histograms that use variable bins instead of the variable's values to plot
        * Also added information of events outside the given kinematic binning (i.e., above/below the defined range as well as information on unmatched events)
     5) Name is now: V22_20_Bin_Test


### On 5-25-2022:
     1) Using 20 Bin option (rerunning for bin migration histograms)
     2) Changed bin migration histograms into 1 2D histogram per variable instead of 1 1D histogram for each REC bin of each variable (reduces number of calculations)
     3) Made the (new) bin migration histograms use the kinematic values for plotting instead of the actual bin numbers
     4) Added the kinematic variable 'y' back into the 1D and 2D histogram lists
     2) Name is now: V21_20_Bin_Test

### On 5-24-2022:
     1) Using 10 Bin option (rerunning for bin migration histograms)
     2) Name is now: V20_10_Bin_Test

### On 5-24-2022:
     1) Using 4 Bin option (New)
     2) Name is now: V20_4_Bin_Test

### On 5-24-2022:
     1) Error noticed in migration histograms - needed to rerun (did not use the correct histogram binning)
     2) Using 5 Bin option
     3) Name is now: V20_5_Bin_Test

### On 5-23-2022:
     1) Another new fewer bin option (3 bins of data)
     2) Name is now: V19_3_Bin_Test

### On 5-23-2022:
     1) New fewer bin option (2 bins of data - Needed to run twice due to error in option choice)
     2) Name is now: V19_2_Bin_Test

### On 5-23-2022:
     1) Added information on where the 'non-pure'/migrated events are migrating from (updated name from V18 to V19)
     2) Re-tested version of binning 1D binning (~5 bin option)
     3) Name is now: V19_5_Bin_Test

### On 5-19-2022:
     1) Tested next version of binning 1D binning (largest option)
     2) Name is now: V18_40_Bin_Test

### On 5-18-2022:
     1) Tested next version of binning 1D binning (2nd largest option)
     2) Name is now: V18_15_Bin_Test (should have been titles V18_20_Bin_Test)

### On 5-18-2022:
     1) Tested next version of binning 1D binning (2nd smallest option)
     2) Name is now: V18_10_Bin_Test

### On 5-18-2022:
     1) Removed many options that are not currently useful including:
        * 2D purity counts
        * All Q2-xB bins (just running "all" events)
        * Cut option without the new Q2 cut
        * Kinematics of the electron and π+ momentum and angles (i.e., only plotting Q2, xB, z, pT, and phi_t)
     2) Changed the new binning and cut to start at Q2 = 2 GeV^2 instead of at 1.95 GeV^2
     3) Starting tests of new 1D binning (currently testing smallest 1D bin option)
     4) Name is now: V18_5_Bin_Test

### On 5-17-2022:
     1) Error in V16 which caused the 2D bin purity histograms to not be run properly (now fixed)
     2) phi_t binning is now set to 36 bins (i.e., 10˚ per bin)
     3) Name is now up to "Purity_V17"

### On 5-16-2022:
     1) Forgot to log update for V15
        * Code was updated between 5-10-2022 and 5-16-2022
     2) 2D Binning was not updated properly 
        * z-pT bins always used old binning scheme when making cuts - Fixed in update
     3) phi_t binning is now set to 45 bins (i.e., 8˚ per bin)
     4) "Purity_V15" crashed while running (Now it should be fixed)
     5) Name is now up to "Purity_V16"


### On 5-10-2022:
     1) Forgot to update the code to use the Rules_5 (from groovy)
        * These rules had the fixed phi matching criteria (Max ∆Phi = 180˚)
     2) Name is now up to "Purity_V14_New_"
        * Did not go up to V15 because all else should be the same

### On 5-9-2022:
     1) Reduced the number of histograms to be created
       Removed:
        * 2D Bin purity cut
        * GEN histograms (matched from pdf) 
     2) Made the 2D histogram binning smaller than the 1D bins (10 times as many bins for the same ranges)
        * Shows the defined binning (based on Stefan's 2D bins) better
     3) Redid how the count histogram works to make the axis labels strings instead of integers (should be easier to read with some formatting help)
     4) Added an option to take a snapshot of the dataframe
        * Produces a ROOT file with the TTree instead of histograms (like what the groovy script does)
        * All old code (i.e., the .sh files) should be compadible with this change, as the code will default to working the same way as before
        * NOTE: Files can be increadibly large. This feature might not be useful unless specific columns from the dataframe are selected to be outputted (option remains despite its current lack of usefulness)
     5) Name is now up to "Purity_V14_"

### On 5-3-2022:
     1) Reduced the number of histograms to be created
       Removed:
        * Some Q2-xB bins
        * Specific particle mis-identification
        * Q2 < 2 cut
        * y plots (1D and 2D), MM plots, and W plots
     2) Name is now up to "Purity_V13_"


### On 5-2-2022:
     1) Updated Matching criteria (changed best match in groovy code)
     2) Added new type of 2D binning 
       * Change stefan's binning to accommodate the cut on Q2 < 2
       * New definition has 1 less bin as Bin 1 is combined with the original Bin 3 (even numbered bins are the same but odd numbered bins are number 2 less than they were - i.e., Bin 5 would now be Bin 3 and Bin 9 is now called Bin 7)
       * Original binning still being used
     3) Added purity calculation to Q2-xB bins
     4) Changed phi_t binning again (8 degrees per bin - Range = 0-360 and # of Bins = 45)
     5) Name is now up to "Purity_V12_"

### On 4-26-2022:
     1) Changed phi_t binning (2 degrees per bin)
     2) Added 'Matched' filter condition (i.e., PID != 0) to purity calculation (redundancy)
     3) Name is now up to "Purity_V11_"

### On 4-25-2022:
     1) Changed Q2 and xB binning
     2) Added y to the histograms being produced (Also y vs xB as a 2D histogram)
     3) Added mis-identified matchs to the histogram options
     4) Not using the 2D binning options
     5) Name is now up to "Purity_V10_"

### On 4-19-2022:
     1) Changed how smearing was applied so that it remains consistent for the entire time that the code is running
       * Old method would create a new smearing data set that may not always be consistent with prior uses of that code
       * The above issue meant that 'matched', 'unmatched', and 'pure' data sets may not be internally compariable in the desired way once the data has been smeared
       * Code now maintains one set group of smeared data for its entire runtime (this change may cause the code to take longer to run/require more memory - effect currently unknown)
     2) Updated all binning schemes based on results from prior versions
     3) Name is now up to "Purity_V9_"


### On 4-18-2022:
     1) Adjusted histogram binning (first major update since fixing the purity calculation)
     2) Change file location (new matching criteria + secondary match)
         * The feature of the new files which adds the second best match to the data frame was not used at the time of this update
         * File locations for 'pdf' are now: /lustre19/expphy/volatile/clas12/richcap/Fall2021/Andrey_SIDIS/Monte_Carlo/Purity/Testing_New/Test_New_Rules_3/MC_Matched_sidis_epip_richcap_Test_Rules_New_3.inb.qa.45nA_job_*
     3) Reduced the number of histograms must be made before outputing the progress of the code while running (minor update to print progress - does not affect what is produced)
     4) Name is now up to "Purity_V8_"

### On 4-13-2022:
     1) Added histograms for unmatched data
     2) Name is now up to "Purity_V7_"

### On 4-11-2022:
     1) Fixed issue with bin purity calculation
     2) Switched files for matched MC data (now using the updated matching criteria)
     3) Name is now up to "Purity_V6_"


### On 4-4-2022:
     1) Rebinned the histograms again (V4)
       * V2 worked in all cases except for the MM, Q2, and pT (Q2 worked before for V2)
     2) Added count info on all (matched/unmatched) events that surived the cuts made (in addition to the existing count of MATCHED events that survived the cuts)
     3) Added a 3rd type of histogram to be produced with 'pdf'
       * datatype_2 = "gen" now creates histograms for the matched, generated events (from pdf)

### On 3-28-2022: 
     Updated for use with the event matching/bin purity (too many changes to fully note)

### On 3-11-2022: 
     1) Fixed how smearing/cuts worked for more appropriate application to the datasets (i.e., smearing only for mdf and not cuts for gdf)
     2) New function for looping through cuts
     3) New cut on Q2 (Q2 < 2 can be cut now)
     4) Cleaned up notes below


### On 2-28-2022: Prepared for Collaboration presentation

### On 2-7-2022: Removed temp definition of sectors -- Also not running sectors right now (too many histograms to be meaningful right now)

### On 1-31-2022:
     1) Did not run with pion sector info (did not have time to run before presentation)
     2) Added 3D->2D histograms (in addition to the 1D histograms this code was already designed to create)

