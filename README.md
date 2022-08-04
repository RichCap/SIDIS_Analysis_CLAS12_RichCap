# SIDIS_Analysis_CLAS12_RichCap
Analysis code for multidimensional SIDIS Analysis of CLAS12 data



## To-do List (General)
This list will be updated as items are completed. Items here may not always relate to the code in the Github repository.
- [ ] Run 1D bin acceptance by plotting the variables against each other, not their bin numbers
    * This will reduce future errors by limiting the confusion when dividing the migration matrix by the 1D generated histograms to get the acceptance matrix
- [ ] Run Q2-xB bins and z-pT bins separately in the same way that the 4D bins are run 
    * want to see the evolution of the multi-dimensional bin migration as more dimensions are considered
- [ ] Add a 5D bin option which includes phi_t (may want to run in the "bin_migration_V4" version of the code to give more options to the number of phi_t bins)
* On the Poster for GRC:
    - [x] Add section which describes the event/reaction being studied
        - [x] Particles involved
        - [x] Cuts used to ensure SIDIS event
        - [x] Where are the particles being detected (answer: the forward detector)
        - [x] Show definition of phi_t
    - [x] Merge existing "Background" and "Motivations" sections into one section
    - [x] The equations showing the bin volume dependance towards the cross-section belongs in a separate section
        * That equation denotes the experimental way of measuring the cross-section
        - [x] **Make a section which describe how I will handle the data experimentally**
            - [x] Introduce Acceptance/Bin Migration concepts here (?)
                * Note how this makes the MC data important to analyze
    - [x] **Show comparison between data and MC**
        - [x] Start with Q2-xB binning (One 2D histogram of Q2 vs xB plus two 1D histograms of both variables)
        - [x] Pick one Q2-xB bin and show the z-pT bin comparisons for it (break down in the same way as the point above)
        - [x] Pick one z-pT bin and show the phi_t distributions for it
    - [x] Show 1D Acceptance Matrix (Show the 2D histograms for a 1D variable)
        - [x] Show for at least one variable if not all 5
        - [x] Potentially try to show the Multi-dimensional matrixes if space allows
            * Start with 2D bins before moving to the 4D/5D bins
            * If space does not allow for this, mention this aspect of the analysis as "Next Step" to be worked on
        
    



## Potential Ideas
These ideas may or may not be implemented later (put here as a reminder to think about later)
- [ ] Add the interactive python code to the GitHub repository 
    * Purpose: so that others can have the more user-friendly version of the code if they are given access to this repository
        * Would give me a greater reason to share this repository with others
    * Would likely include:
        - [ ] Adding the jupyter notebook file (with edits to run using the files available on GitHub)
        - [ ] Adding additional features to that notebook to keep it concurrent with the available code
            * May want to consider it the "master" version of the code while the existing verision would be the "working" version were new code and ideas are tested
- [ ] Add additional kinematic bins to replace bin 0 (i.e., unbinned event)
    * Purpose: Give more information on where the event may be migrating from relative to the existing bins
        * Would give information such as: "Is the unbinned event above/below/to the left/right of the existing binning scheme"
    * Would likely include:
        - [ ] 4 new Q2-xB bins (up, down, left and right of bins)
        - [ ] 8 new z-pT bins (up, down, left and right of bins plus 4 more bins for the corners which are both above/below the existing bins AND to the left/right of them as well)


## Note to self:
- [ ] Add option to jupyter notebook to select user range when defining the variable lists (add later)
- [x] Run and test the additions made to the code on 7-19-2022
    * Specifically: see if the -2 bin option to the 4D bins is useful for the bin migration study
    * [x] Re-familarize myself with the functioning of the bin migration histograms 
    * [x] Make sure the new 4D bins behave in a way that does not conflict with the existing analysis methods
        * Note from investigation: the 4D bins work best for "bin_migration_V3" instead of "bin_migration_V4" since "bin_migration_V4" is primarily useful at testing multiple bin schemes in the 1D cases (does not apply well to the 4D schemes that are already well defined)

- [x] In a future update, add the 4D binning to the original kinematic binning from Stephan **(ADDED ON 7-20-2022)**
    * Should be used to show the improvement made by the new binning scheme to the bin migration caused by low Q2
    * Currently, more bin mirgation is occuring such that high generated Q2 is more likely to migrate than low Q2. This is being explained by the low Q2 events that most contribute to bin migration are already being cut by the Q2 > 2 GeV^2 requirement and (more importantly) by the modified bin scheme itself.
    * This addition should be added to verify that the bin migration is being addressed as intended
    

---


## Commit Updates:


### Update on 8-4-2022:
#### Jupyter Code Updates:
* Formatting update for GRC poster
* Changed phi_t to phi_h in titles (code variable is still called phi_t)
* Changed pT to PT (same note/reason as the change to phi_t)
* Added units to histograms


### Update on 7-22-2022:
#### Python Code Updates:
* Changed binning options to make histograms for the GRC conference 
    * 1D binning now only extends from the minimum 2D bin boundry to the maximum 2D bin boundry (not meant to show the full kinematic distributions, just those that would fall into the 2D binning schemes)
    * 1D bins now set to 5 bins total
    * 2D histograms now being displayed with finer binning (200 bin per variable with the bin size being arbitrary - for display purposes only)
* Added the particle kinematics to the 2D histograms (will use to show event selection with all analysis cuts)
* Only using updated 2D binning schemes (Stephan's orginal scheme is not necessary at this moment)
    * Only running Q2-xB bins up to bin 8
* Removed unnecessary histogram options such as "count" and previous versions of "bin_migration" (versions 1 and 2 are not being run)
#### Jupyter Code Updates:
* Added the Acceptance Matrices
* Updated the formatting of histograms (for GRC poster)
* Removed full list of individual files (existed before I started to use hadd command to combine ROOT files)
#### Other Updates:
* Extra_Name = "Bin_Test_GRC_" output files added
* Cannot upload these files due to size limit


### Update on 7-21-2022:
#### Python Code Updates:
* Updated Variable name function for "Bin_4D_OG" (Files up to "Bin_Test_20_V3_" will have their names be identical)
    * This issue did not corrupt any file
* New Output File Names: Extra_Name = "Bin_Test_20_V3_" (Unchanged right now)
#### Jupyter Code Updates:
* Updates to Data Set Comparison Code (new version of comparison added)
* Other updates to formating and existing outputs
#### Other Updates:
* Extra_Name = "Bin_Test_20_V3_" output files added



### Update on 7-20-2022:
#### Python Code Updates:
* Added 4D binning scheme definition to the original kinematic bins developed by Stephan (Variable name = "Bin_4D_OG")
* Changed the histogram bins of the "Bin_4D" histograms slightly (should primarily make a visual difference only)
* Removed "Bin_4D" histograms from the "bin_migration_V4" option (exclusively to be used by "bin_migration_V3")
* Needed to fix an issue that caused the "pdf" files to crash while running
    * New Output File Names: Extra_Name = "Bin_Test_20_V3_"
#### Jupyter Code Updates:
* Minor changes (so far)
#### Other Updates:
* Added the groovy codes used to process the hipo files into the TTrees used by the python code (did not add the files that they produce)
* Added the new ROOT files (Extra_Name = "Bin_Test_20_V2_") despite the fact that the MC_Matching files crashed while being created
* New idea added to this README.md file that could be incorporated into this analysis later (Notes/Ideas section are now included in this file too)




### Update on 7-19-2022:
#### Python Code Updates:
* (Newer Update) Changed the 4D binning scheme slightly 
    1) 4D bins start at -1 to correspond to events that land outside of the Q2-xB binnning (Bin 0 is for Q2-xB bin 1 events that do not land into a defined z-pT bin)
        * A value of -2 is given to the generated events that are not matched to a reconstructed event (only for the 'pdf' files)
    2) Removed the histograms produced with this binning scheme that do not also use the updated Q2-xB binning scheme (i.e., the one that only goes up to bin 8)
        * The 4D binning scheme is only properly defined for this version of the 2D bins so using the original binning schemes is useless
    3) Files uploaded as of 7-19-2022 do NOT include these updates (Extra_Name will be updated to "Bin_Test_20_V2_" for that update)
* Added new type of kinematic binning which combines the Q2-xB bins with the z-pT bins to form a continuous binning scheme
* Ran all data files
#### Jupyter Code Updates:
* Switched file names to work with current directories
* Updated the code to handle the new 4D binning option (getting ready to go from bin migration to acceptance)
#### Other Updates:
* Added the ROOT files (the python file's outputs) to the github directory (for use on local computers)
* Added the .sh files too

### Update on 7-18-2022:
* Updated file names in python code (Extra_Name = "Bin_Test_20_" - for output file name)




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